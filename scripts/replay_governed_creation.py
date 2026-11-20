#!/usr/bin/env python3
"""Offline replay against pinned GRT source, with GitHub replaced by a fixture."""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

PINS = {
    "control_plane_create_repository.py": "d6f407ff58c4d067c840747c62ac51053a725753",
    "control_plane_issue_bridge.py": "0e73bb1ef0b2a4b1963788f0998cca2e5de12055",
    "governed_hold_review.py": "46d1f20bf6af10fb27f64d7a616643e231a01f10",
    "governed_plan_reconciliation.py": "4249af7e3229881c934a3bc82b485bb63a61d294",
    "governed_request.py": "3934f6700bb84e446d76d1b0c0379db7f8c8a0b6",
    "test_control_plane_request.py": "e66a72dac25391c73f1a9b6984d942df68281697",
}
REPO = "chainsolutions-wealthtech/replay-create-fixture"
INITIAL_SHA = "a" * 40
BOOTSTRAP_SHA = "b" * 40
REPOSITORY_ID = 42
RECEIPT = {
    "bootstrap_success": True,
    "template_version": "fixture",
    "final_head_sha": BOOTSTRAP_SHA,
    "run_id": "123456",
}


def verify_sources(scripts: Path) -> None:
    for name, expected in PINS.items():
        content = (scripts / name).read_bytes()
        header = f"blob {len(content)}\0".encode("ascii")
        if hashlib.sha1(header + content).hexdigest() != expected:
            raise SystemExit(f"Source GRT hors révision de référence : {name}")


class GitHubFixture:
    def __init__(self, executor, *, preexisting=False):
        self.executor = executor
        self.repository = self.repo_metadata() if preexisting else None
        self.same_manifest = not preexisting
        self.head_readable = False
        self.posts = 0
        self.head_reads = 0

    @staticmethod
    def repo_metadata():
        return {"full_name": REPO, "id": REPOSITORY_ID, "default_branch": "main"}

    def api(self, token, method, path, payload=None, allow_404=False):
        source = f"{self.executor.TEMPLATE_OWNER}/{self.executor.TEMPLATE_REPO}"
        if (method, path) == ("GET", f"/repos/{source}"):
            return {"is_template": True}
        if (method, path) == ("GET", f"/repos/{REPO}"):
            assert allow_404
            return self.repository
        if (method, path) == ("POST", f"/repos/{source}/generate"):
            self.posts += 1
            assert self.repository is None, "second POST de création"
            assert payload == {
                "owner": "chainsolutions-wealthtech",
                "name": "replay-create-fixture",
                "include_all_branches": False,
                "private": True,
            }
            self.repository = self.repo_metadata()
            return self.repository
        if method == "GET" and path in (
            f"/repos/{REPO}/contents/.governance/TEMPLATE_MANIFEST.json",
            f"/repos/{source}/contents/.governance/TEMPLATE_MANIFEST.json",
        ):
            if path.startswith(f"/repos/{REPO}/") and not self.same_manifest:
                return None
            manifest = {"template_name": "Governed Repository Template", "template_version": "fixture"}
            return {"content": base64.b64encode(json.dumps(manifest).encode()).decode()}
        if (method, path) == ("GET", f"/repos/{REPO}/commits/main"):
            self.head_reads += 1
            if not self.head_readable:
                raise RuntimeError("GitHub API GET commits/main failed: 409 Git Repository is empty")
            return {"sha": INITIAL_SHA}
        raise AssertionError(f"Requête imprévue : {method} {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("grt_checkout", type=Path)
    scripts = (parser.parse_args().grt_checkout / "scripts").resolve()
    verify_sources(scripts)
    sys.path.insert(0, str(scripts))
    executor = importlib.import_module("control_plane_create_repository")
    grt = importlib.import_module("governed_request")

    class Replay(unittest.TestCase):
        def setUp(self):
            self.state = grt.new_request("GR-FIXTURE", "fixture", "offline")
            for field, answer in (
                ("entry_action", "CREATE_NEW_REPOSITORY"),
                ("creation_target_owner", "chainsolutions-wealthtech"),
                ("repository_name", "replay-create-fixture"),
                ("visibility", "private"),
            ):
                self.state = grt.apply_answer(self.state, field, answer)

        def run_executor(self, fixture):
            def read_issue(method, path):
                self.assertEqual((method, path), (
                    "GET", f"/repos/{executor.CONTROL_PLANE_REPOSITORY}/issues/42",
                ))
                return {"body": f"<!-- GOVERNED_REQUEST_STATE:{grt.encode_state(self.state)} -->"}

            def save(issue, _body, state):
                self.assertEqual(issue, 42)
                self.state = state

            with (
                patch.dict(os.environ, {"GOVERNED_CREATOR_TOKEN": "fixture"}, clear=True),
                patch.object(sys, "argv", ["executor", "--issue-number", "42"]),
                patch.object(executor, "control_plane_api", side_effect=read_issue),
                patch.object(executor, "github_api", side_effect=fixture.api),
                patch.object(executor, "persist_state", side_effect=save),
                patch.object(executor, "comment"),
                patch.object(executor.time, "sleep"),
                patch("urllib.request.urlopen", side_effect=AssertionError("Réseau interdit")),
            ):
                executor.main()

        def test_accepted_create_then_head_409_then_same_request_resumes(self):
            fixture = GitHubFixture(executor)
            with self.assertRaisesRegex(RuntimeError, "unable to observe initial target HEAD"):
                self.run_executor(fixture)
            self.assertEqual(fixture.posts, 1)
            self.assertGreater(fixture.head_reads, 1)
            self.assertEqual(fixture.repository["id"], REPOSITORY_ID)
            self.assertEqual(self.state["next_request"]["action_id"], "PREP-001")
            self.assertFalse(self.state["evidence"])

            fixture.head_readable = True
            self.run_executor(fixture)
            self.assertEqual(fixture.posts, 1)
            self.assertEqual(fixture.repository["id"], REPOSITORY_ID)
            self.assertEqual(self.state["request_id"], "GR-FIXTURE")
            self.assertEqual(self.state["next_request"]["action_id"], "PREP-002")
            self.assertTrue(self.state["evidence"][0]["evidence"]["recovered_existing"])

            # PREP-002..004 are simulated evidence, not live GitHub operations.
            for stage, evidence in (
                ("PREP-002", RECEIPT),
                ("PREP-003", {
                    "server_status": "UNRESOLVED", "directory_status": "UNRESOLVED",
                    "database_status": "UNRESOLVED", "access_status": "UNRESOLVED",
                }),
                ("PREP-004", {"default_branch": "main", "head_sha": BOOTSTRAP_SHA}),
            ):
                self.state = grt.apply_evidence(self.state, stage, "PASS", evidence)

            self.assertEqual(self.state["status"], "HANDOFF_READY")
            handoff = self.state["handoff"]
            self.assertEqual(handoff["target_repository"], REPO)
            self.assertEqual(handoff["target_branch"], "main")
            self.assertEqual(handoff["expected_head_sha"], BOOTSTRAP_SHA)
            self.assertEqual(handoff["allowed_next_operation"], "DISCOVER_PROJECT_BASELINE")

        def test_unrecognized_preexisting_repository_is_not_created_or_adopted(self):
            fixture = GitHubFixture(executor, preexisting=True)
            self.run_executor(fixture)
            self.assertEqual((fixture.posts, fixture.head_reads), (0, 0))
            self.assertEqual(self.state["next_request"]["action_id"], "PREP-001")
            self.assertFalse(self.state["evidence"])

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Replay)
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
