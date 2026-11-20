from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
from tempfile import TemporaryDirectory
from threading import Thread
import unittest
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from capsules.governed_repository_creation.intake.planning import IntakeError, IntakeJournal, next_question, project
from capsules.governed_repository_creation.intake.preflight import GitHubActor, dossier
from capsules.governed_repository_creation.intake.web import make_server


STRUCTURE = {
    "owner": "chainsolutions-wealthtech", "name": "fixture-batch", "visibility": "public",
    "workflow_model": "STANDARD_GOVERNED_FLOW",
}


class BatchJournalTest(unittest.TestCase):
    def setUp(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.journal = IntakeJournal(Path(tmp.name) / "intake.db")
        self.request = self.journal.start("owner")

    def test_resume_and_record_the_lot_in_catalogue_order(self):
        self.journal.answer("owner", self.request, 1, "owner", STRUCTURE["owner"])
        before = self.journal.get("owner", self.request)
        payload = {**STRUCTURE, "mcp_scope": "PROJECT_ONLY", "mcp_linkage": "CREATE_BINDING",
                   "dns_tls_posture": "PLAN_NEW", "domain_posture": "CREATE_NEW",
                   "server_binding_mode": "NONE_PLAN_NEW", "production_server_selection": "PLAN_NEW_SERVER"}
        del payload["owner"]
        self.journal.answer_batch("owner", self.request, 2, payload)
        events = self.journal.get("owner", self.request)
        self.assertEqual(events[:2], before)
        self.assertEqual(events[-1]["kind"], "PREPARATION_COMPLETE")
        self.assertEqual([e["revision"] for e in events], list(range(1, len(events) + 1)))
        answers = project(events)
        for field, expected in payload.items():
            self.assertEqual(answers[field], expected)
        self.assertIsNone(answers["mcp_transport"])
        self.assertIsNone(answers["project_mission"])

    def test_invalid_stale_and_foreign_batches_are_atomic(self):
        for actor, revision, payload in (
            ("owner", 1, {"owner": STRUCTURE["owner"]}),
            ("owner", 1, {**STRUCTURE, "execution_timing": "INVALID"}),
            ("owner", 1, {**STRUCTURE, "unexpected": "value"}),
            ("owner", 0, STRUCTURE),
            ("someone-else", 1, STRUCTURE),
        ):
            with self.subTest(actor=actor, revision=revision, payload=payload):
                with self.assertRaises(IntakeError):
                    self.journal.answer_batch(actor, self.request, revision, payload)
                self.assertEqual(len(self.journal.get("owner", self.request)), 1)

    def test_no_overwrite_and_no_out_of_scope_values(self):
        self.journal.answer("owner", self.request, 1, "owner", STRUCTURE["owner"])
        with self.assertRaises(IntakeError):
            self.journal.answer_batch("owner", self.request, 2, STRUCTURE)
        self.assertEqual(len(self.journal.get("owner", self.request)), 2)
        payload = {**STRUCTURE, "mcp_linkage": "NO_MCP", "mcp_transport": "SSH",
                   "dns_tls_posture": "PLAN_NEW", "production_server_selection": "PLAN_NEW_SERVER"}
        del payload["owner"]
        self.journal.answer_batch("owner", self.request, 2, payload)
        events = self.journal.get("owner", self.request)
        for field in ("mcp_transport", "mcp_scope", "dns_tls_posture", "production_server_selection"):
            self.assertNotIn(field, project(events))

    def test_same_preflight_dossier_as_step_by_step(self):
        choices = {**STRUCTURE, "git_provider": "GITHUB", "project_mission": "Préparer le dossier",
                   "mcp_linkage": "CREATE_BINDING", "mcp_transport": "SSH", "mcp_scope": "PROJECT_ONLY"}
        self.journal.answer_batch("owner", self.request, 1, choices)
        sequential = self.journal.start("owner")
        while True:
            events = self.journal.get("owner", sequential)
            question = next_question(project(events))
            if question is None:
                break
            field = question["field"]
            self.journal.answer("owner", sequential, events[-1]["revision"], field,
                                choices.get(field, ""), defer=field not in choices)
        batch = self.journal.get("owner", self.request)
        self.assertEqual(dossier(events), dossier(batch))
        self.assertEqual(events[-1]["revision"], batch[-1]["revision"])

    def test_parallel_submissions_only_commit_once(self):
        def submit():
            try:
                self.journal.answer_batch("owner", self.request, 1, STRUCTURE)
            except IntakeError:
                return False
            return True

        with ThreadPoolExecutor(max_workers=2) as executor:
            self.assertCountEqual(executor.map(lambda _: submit(), range(2)), [True, False])
        events = self.journal.get("owner", self.request)
        self.assertEqual(sum(e["kind"] == "PREPARATION_COMPLETE" for e in events), 1)


class BatchWebTest(unittest.TestCase):
    def setUp(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.journal = IntakeJournal(Path(tmp.name) / "intake.db")
        self.server = make_server(self.journal, resolve_actor=lambda request: (
            GitHubActor(42) if request.headers.get("X-Fixture") == "owner"
            else GitHubActor(43)
        ))
        self.addCleanup(self.server.server_close)
        thread = Thread(target=self.server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, 5)
        self.addCleanup(self.server.shutdown)
        self.actor = GitHubActor(42).journal_key
        self.request = self.journal.start(self.actor)
        self.request_path = f"/requests/{self.request}"

    def http(self, path, data=None, actor="owner"):
        if data is not None:
            data = urlencode(data).encode()
        return urlopen(Request(f"http://127.0.0.1:{self.server.server_port}" + path,
                               data=data, headers={"X-Fixture": actor}), timeout=5)

    def test_direct_submission_to_the_same_request_and_no_external_action(self):
        self.journal.answer(self.actor, self.request, 1, "owner", STRUCTURE["owner"])
        with self.http(self.request_path) as response:
            self.assertIn("Ouvrir le questionnaire groupé", response.read().decode())
        path = self.request_path + "/batch"
        with self.http(path) as response:
            html = response.read().decode()
            self.assertIn("Envoyer toutes les réponses", html)
            self.assertIn("Réponses déjà enregistrées", html)
            self.assertNotIn('name="owner"', html)
            self.assertIn('name="deployment_strategy"', html)
            self.assertIn('name="mcp_transport"', html)
            self.assertEqual(response.headers["Cache-Control"], "no-store")
            self.assertIn("script-src 'self'", response.headers["Content-Security-Policy"])
        csrf = re.search(r'name="csrf" value="([^"]+)', html)[1]
        with self.http("/assets/intake-batch.js") as response:
            self.assertTrue(response.headers["Content-Type"].startswith("text/javascript"))
            self.assertIn(b"disabled", response.read())
        payload = {**STRUCTURE, "csrf": csrf, "revision": 2, "mcp_linkage": "NO_MCP",
                   "project_mission": "À" * 500, "scope_in": "é" * 500}
        del payload["owner"]
        self.assertGreater(len(urlencode(payload)), 4096)
        for body, status, actor in (
            ({**payload, "csrf": "invalid"}, 403, "owner"),
            (list(payload.items()) + [("name", "duplicate")], 400, "owner"),
            (payload, 403, "other"),
            ({**payload, "execution_timing": "INVALID"}, 422, "owner"),
        ):
            with self.assertRaises(HTTPError) as error:
                self.http(path, body, actor)
            self.assertEqual(error.exception.code, status)
            if status == 422:
                self.assertIn('value="fixture-batch"', error.exception.read().decode())
            self.assertEqual(len(self.journal.get(self.actor, self.request)), 2)
        with self.http(path, payload) as response:
            self.assertTrue(response.geturl().endswith(self.request_path))
            html = response.read().decode()
            self.assertIn("Préparation terminée", html)
            self.assertNotIn("Vérifier avec CUG", html)
            self.assertNotIn("Ouvrir le questionnaire groupé", html)
        with self.assertRaises(HTTPError) as stale:
            self.http(path, payload)
        self.assertEqual(stale.exception.code, 409)
        events = self.journal.get(self.actor, self.request)
        self.assertEqual(project(events)["project_mission"], "À" * 500)
        self.assertEqual(events[-1]["kind"], "PREPARATION_COMPLETE")
