import json
from pathlib import Path
import re
from tempfile import TemporaryDirectory
from threading import Thread
import unittest
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from capsules.governed_repository_creation.intake.planning import (
    IntakeError, IntakeJournal, QUESTIONS, SOURCE, next_question, preview, project,
)
from capsules.governed_repository_creation.intake.web import make_server


class PlanningTest(unittest.TestCase):
    def setUp(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.db = Path(tmp.name) / "intake.sqlite"
        self.journal = IntakeJournal(self.db)
        self.request = self.journal.start("actor")

    def answer(self, field, value, defer=False):
        revision = self.journal.get("actor", self.request)[-1]["revision"]
        self.journal.answer("actor", self.request, revision, field, value, defer=defer)

    def test_source_manifest_and_question_catalogue(self):
        self.assertEqual(len(SOURCE["entries"]), 216)
        self.assertEqual(len({e["path"] for e in SOURCE["entries"]}), 216)
        self.assertEqual(len(SOURCE["questions"]), 35)
        self.assertEqual(len(QUESTIONS), 33)
        self.assertEqual(len(SOURCE["workflow_models"]), 2)
        result = preview({})
        self.assertIn("GOVERNANCE.md", result["target_documents"]["generic_core"])
        self.assertIn(".github/workflows/governance-auto-bootstrap.yml", result["target_workflows"])
        self.assertNotIn(".github/workflows/governed-control-plane.yml", result["target_workflows"])
        self.assertIn("docs/control-plane", result["source_only"])

    def test_request_starts_before_answers_and_reopens_after_restart(self):
        self.assertEqual(self.journal.get("actor", self.request)[0]["kind"], "REQUEST_OPENED")
        self.answer("owner", "chainsolutions-wealthtech")
        self.journal = IntakeJournal(self.db)
        events = self.journal.get("actor", self.request)
        self.assertEqual(next_question(project(events))["field"], "name")
        self.assertEqual(events[-1]["value"], "chainsolutions-wealthtech")
        self.assertEqual(self.journal.recent("actor"), [self.request])
        with self.assertRaises(IntakeError):
            self.journal.get("another", self.request)

    def test_stale_revision_wrong_choice_and_required_deferral_do_not_write(self):
        with self.assertRaises(IntakeError):
            self.journal.answer("actor", self.request, 0, "owner", "Patricked-code")
        with self.assertRaises(IntakeError):
            self.answer("owner", "other")
        with self.assertRaises(IntakeError):
            self.answer("owner", "", defer=True)
        self.assertEqual(len(self.journal.get("actor", self.request)), 1)

    def test_both_workflow_models_resolve_and_no_mcp_hides_transport(self):
        for model in SOURCE["workflow_models"]:
            self.request = self.journal.start("actor")
            given = {"owner": "Patricked-code", "name": "fixture", "visibility": "private",
                     "workflow_model": model, "mcp_linkage": "NO_MCP"}
            while q := next_question(project(self.journal.get("actor", self.request))):
                field = q["field"]
                self.answer(field, given.get(field, ""), defer=field not in given)
            events = self.journal.get("actor", self.request)
            self.assertEqual(events[-1]["kind"], "PREPARATION_COMPLETE")
            answers = project(events)
            self.assertNotIn("mcp_transport", answers)
            self.assertNotIn("mcp_scope", answers)
            plan = preview(answers)
            self.assertEqual(plan["model_steps"], SOURCE["workflow_models"][model])
            self.assertFalse(plan["governed_session_started"])
            self.assertFalse(plan["creation_authorized"])
            self.assertFalse(plan["deployment_authorized"])

    def test_project_outline_is_traceable_without_creating_a_session(self):
        for field, value in (("owner", "Patricked-code"), ("name", "demo"),
                             ("visibility", "private"), ("workflow_model", "STANDARD_GOVERNED_FLOW"),
                             ("project_mission", "Préparer un service de test")):
            self.answer(field, value)
        events = self.journal.get("actor", self.request)
        self.assertEqual(preview(project(events))["business_outline"]["project_mission"],
                         "Préparer un service de test")
        self.assertFalse(preview(project(events))["governed_session_started"])

    def test_preparation_cannot_fabricate_observed_servers(self):
        q = QUESTIONS["production_server_selection"]
        self.assertNotIn("S1", q["choices"])
        self.assertNotIn("S2", q["choices"])
        self.assertEqual(q["choices"], ["PLAN_NEW_SERVER", "DECIDE_LATER"])


class WebTest(unittest.TestCase):
    def test_start_answer_and_resume_over_http(self):
        with TemporaryDirectory() as tmp, make_server(IntakeJournal(Path(tmp) / "intake.db")) as server:
            thread = Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                base = f"http://127.0.0.1:{server.server_port}"
                with urlopen(base, timeout=5) as response:
                    html = response.read().decode()
                csrf = re.search(r'name="csrf" value="([^"]+)', html)[1]
                with self.assertRaises(HTTPError) as failure:
                    urlopen(Request(base + "/requests", data=b"csrf=wrong"), timeout=5)
                self.assertEqual(failure.exception.code, 403)
                with urlopen(Request(base + "/requests", data=urlencode({"csrf": csrf}).encode()), timeout=5) as response:
                    created = response.geturl()
                    html = response.read().decode()
                self.assertIn("REQUEST_OPENED", html)
                self.assertIn("Quel compte GitHub", html)
                data = urlencode({"csrf": csrf, "field": "owner", "revision": "1",
                                  "command": "answer", "value": "Patricked-code"}).encode()
                with urlopen(Request(created, data=data), timeout=5) as response:
                    html = response.read().decode()
                    self.assertEqual(response.headers["Cache-Control"], "no-store")
                self.assertIn("Quel est le nom exact", html)
                self.assertIn("ANSWER_RECORDED", html)
                self.assertNotIn("POST /repos", html)
            finally:
                server.shutdown()
                thread.join(timeout=5)
