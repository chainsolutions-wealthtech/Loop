from pathlib import Path
import re
from tempfile import TemporaryDirectory
from threading import Thread
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from capsules.governed_repository_creation.intake.planning import (
    IntakeError, IntakeJournal, SOURCE, next_question, project,
)
from capsules.governed_repository_creation.intake.preflight import CUGPreflight, GitHubActor, verify_user
from capsules.governed_repository_creation.intake.web import make_server

ACTOR = GitHubActor(123)
BRIDGE = "capsules.governed_repository_creation.intake.preflight.inspect_app"


def prepare(journal, actor=ACTOR):
    rid = journal.start(actor.journal_key)
    choices = {
        "owner": "chainsolutions-wealthtech", "name": "fixture", "visibility": "private",
        "workflow_model": "STANDARD_GOVERNED_FLOW", "git_provider": "GITHUB",
    }
    while True:
        events = journal.get(actor.journal_key, rid)
        q = next_question(project(events))
        if q is None:
            return rid, events[-1]["revision"]
        field = q["field"]
        journal.answer(actor.journal_key, rid, events[-1]["revision"], field,
                       choices.get(field, ""), defer=field not in choices)


def report(**changes):
    return {
        "status": "PREFLIGHT_OBSERVED", "creation_authorized": False, "app_id": 5417646,
        "installation_id": 55, "owner": "chainsolutions-wealthtech",
        "target": "chainsolutions-wealthtech/fixture", "visibility_requested": "private",
        "template": SOURCE["source_repository"].lower(), "template_head_sha": SOURCE["source_sha"],
        "target_observation": "NOT_VISIBLE_404", "token": "not-to-be-stored", **changes,
    }


class BridgeTest(unittest.TestCase):
    def setUp(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.journal = IntakeJournal(Path(tmp.name) / "test.db")
        self.jwt = Mock(return_value="fixture-jwt")
        self.service = CUGPreflight(self.journal, can_preflight=lambda a, o: a == ACTOR and
                                   o == "chainsolutions-wealthtech", app_jwt=self.jwt, api=Mock())

    def test_github_actor_uses_stable_user_id_not_login(self):
        api = Mock(return_value={"type": "User", "id": 123, "login": "name-may-change"})
        self.assertEqual(verify_user(api, "fixture"), ACTOR)
        api.assert_called_once_with("GET", "/user", "fixture")
        api.return_value = {"type": "Bot", "id": 123}
        with self.assertRaises(IntakeError):
            verify_user(api, "fixture")

    def test_wrong_actor_unfinished_or_stale_request_never_gets_app_jwt(self):
        rid, revision = prepare(self.journal)
        for actor, key, rev in ((GitHubActor(999), rid, revision), (ACTOR, rid, revision - 1),
                                (ACTOR, self.journal.start(ACTOR.journal_key), 1)):
            with self.assertRaises(IntakeError):
                self.service.run(actor, key, rev)
        self.jwt.assert_not_called()

    def test_owner_policy_is_checked_before_getting_app_jwt(self):
        actor = GitHubActor(999)
        rid, revision = prepare(self.journal, actor)
        with self.assertRaisesRegex(IntakeError, "non autorisé"):
            self.service.run(actor, rid, revision)
        self.jwt.assert_not_called()

    def test_report_is_bound_to_exact_dossier_and_never_authorizes_create(self):
        rid, revision = prepare(self.journal)
        with patch(BRIDGE, return_value=report()) as inspect:
            event = self.service.run(ACTOR, rid, revision)
        self.assertEqual(inspect.call_args.kwargs["template_sha"], SOURCE["source_sha"])
        self.assertEqual(event["prepared_revision"], revision)
        self.assertRegex(event["dossier_sha256"], r"^[a-f0-9]{64}$")
        self.assertEqual(event["result"]["target_observation"], "NOT_VISIBLE_404")
        self.assertFalse(event["result"]["creation_authorized"])
        self.assertNotIn("token", event["result"])
        self.assertEqual(self.journal.get(ACTOR.journal_key, rid)[-1], event)

    def test_wrong_report_is_a_traced_blocker(self):
        rid, revision = prepare(self.journal)
        with patch(BRIDGE, return_value=report(target="other/repo")):
            event = self.service.run(ACTOR, rid, revision)
        self.assertEqual(event["result"]["reason"], "REPORT_DOES_NOT_MATCH_REQUEST")
        self.assertFalse(event["result"]["creation_authorized"])

    def test_racing_report_cannot_overwrite_a_newer_revision(self):
        rid, revision = prepare(self.journal)

        def competing(*args, **kwargs):
            self.journal.record_preflight(ACTOR.journal_key, rid, revision, "other", {})
            return report()

        with patch(BRIDGE, side_effect=competing), self.assertRaisesRegex(IntakeError, "pendant"):
            self.service.run(ACTOR, rid, revision)
        events = self.journal.get(ACTOR.journal_key, rid)
        self.assertEqual(events[-1]["dossier_sha256"], "other")

    def test_web_preflight_with_injected_identity_and_unauthenticated_refusal(self):
        rid, revision = prepare(self.journal)
        resolve_actor = Mock(return_value=None)
        with make_server(self.journal, resolve_actor=resolve_actor, preflight=self.service) as server:
            thread = Thread(target=server.serve_forever, daemon=True)
            thread.start()
            base = f"http://127.0.0.1:{server.server_port}/requests/{rid}"
            try:
                with self.assertRaises(HTTPError) as exc:
                    urlopen(base, timeout=5)
                self.assertEqual(exc.exception.code, 401)
                resolve_actor.return_value = ACTOR
                with urlopen(base, timeout=5) as response:
                    page = response.read().decode()
                self.assertIn("Vérifier avec CUG", page)
                csrf = re.search(r'name="csrf" value="([^"]+)', page)[1]
                data = urlencode({"csrf": csrf, "revision": revision, "command": "preflight"}).encode()
                with patch(BRIDGE, return_value=report()), urlopen(Request(base, data=data), timeout=5) as response:
                    self.assertIn("PREFLIGHT_OBSERVED", response.read().decode())
            finally:
                server.shutdown()
                thread.join(timeout=5)
