import base64
import json
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
import unittest

from capsules.governed_repository_creation.adapters.github_app_preflight import (
    APIError, PreflightError, inspect_app, make_app_jwt,
)


APP = 5417646
SHA = "a" * 40
TPL = "/repos/chainsolutions-wealthtech/governed-template"


class FakeGitHub:
    def __init__(self, owner="chainsolutions-wealthtech"):
        self.owner = owner
        org = owner == "chainsolutions-wealthtech"
        self.path = f"/{'orgs' if org else 'users'}/{owner}/installation"
        self.calls = []
        self.data = {
            ("GET", "/app"): {"id": APP},
            ("GET", self.path): {
                "id": 10, "app_id": APP, "account": {
                    "login": owner, "id": 22, "type": "Organization" if org else "User",
                },
                "suspended_at": None, "repository_selection": "selected",
                "permissions": {"administration": "write", "contents": "read"},
            },
            ("POST", "/app/installations/10/access_tokens"): {
                "token": "fixture-installation-token", "permissions": {"contents": "read", "metadata": "read"},
            },
            ("GET", TPL): {
                "full_name": "chainsolutions-wealthtech/governed-template",
                "id": 100, "is_template": True, "private": True, "default_branch": "main",
            },
            ("GET", TPL + "/commits/main"): {"sha": SHA},
            ("GET", TPL + "/installation"): {"id": 10, "app_id": APP, "suspended_at": None},
            ("GET", f"/repos/{owner}/capsule-pilot"): APIError(404),
            ("DELETE", "/installation/token"): {},
        }

    def __call__(self, method, path, credential, body=None):
        self.calls.append((method, path, body))
        expected_jwt = path in ("/app", self.path, TPL + "/installation") or method == "POST"
        if credential != ("fixture-jwt" if expected_jwt else "fixture-installation-token"):
            raise AssertionError("wrong GitHub identity for endpoint")
        response = self.data[(method, path)]
        if isinstance(response, Exception):
            raise response
        return response


class GitHubAppPreflightTest(unittest.TestCase):
    def inspect(self, api):
        return inspect_app(api, "fixture-jwt", app_id=APP, owner=api.owner,
                           name="capsule-pilot", visibility="private",
                           template="chainsolutions-wealthtech/governed-template", template_sha=SHA)

    def test_organization_preflight_never_grants_write_and_revokes_token(self):
        api = FakeGitHub()
        report = self.inspect(api)
        self.assertEqual(report["target_observation"], "NOT_VISIBLE_404")
        self.assertEqual(report["repository_selection"], "selected")
        self.assertTrue(report["template_same_installation_verified"])
        self.assertTrue(report["installation_creation_permissions_declared"])
        self.assertFalse(report["creation_authorized"])
        self.assertNotIn("fixture-installation-token", json.dumps(report))
        self.assertEqual([c for c in api.calls if c[0] != "GET"], [
            ("POST", "/app/installations/10/access_tokens", {"permissions": {"contents": "read"}}),
            ("DELETE", "/installation/token", None),
        ])

    def test_user_installation_and_present_target(self):
        api = FakeGitHub("patricked-code")
        api.data[("GET", "/repos/patricked-code/capsule-pilot")] = {
            "id": 88, "full_name": "Patricked-code/Capsule-pilot",
        }
        api.data[("GET", TPL + "/installation")] = {
            "id": 30, "app_id": APP, "suspended_at": None,
        }
        report = self.inspect(api)
        self.assertEqual(report["target_repository_id"], 88)
        self.assertEqual(report["target_observation"], "PRESENT")
        self.assertFalse(report["template_same_installation_verified"])
        self.assertIn(("GET", "/users/patricked-code/installation", None), api.calls)

    def test_app_mismatch_before_installation_token(self):
        api = FakeGitHub()
        api.data[("GET", "/app")]["id"] = APP + 1
        with self.assertRaisesRegex(PreflightError, "UNEXPECTED_APP_IDENTITY"):
            self.inspect(api)
        self.assertEqual(len(api.calls), 1)

    def test_mismatched_suspended_or_unconfirmed_installation_never_mints_token(self):
        for key, value in (("suspended_at", "2026-11-01T00:00:00Z"), ("app_id", APP + 1),
                           ("account", {"id": 22, "login": "somewhere-else", "type": "Organization"})):
            with self.subTest(key=key):
                api = FakeGitHub()
                api.data[("GET", api.path)][key] = value
                with self.assertRaisesRegex(PreflightError, "INSTALLATION_NOT_VERIFIED_FOR_OWNER"):
                    self.inspect(api)
                self.assertFalse(any(c[0] == "POST" for c in api.calls))

    def test_template_access_and_head_are_distinct_failures_and_revoke_token(self):
        for path, response, reason in ((TPL, APIError(404), "TEMPLATE_METADATA_HTTP_404"),
                                       (TPL + "/commits/main", {"sha": "b" * 40}, "TEMPLATE_HEAD_DIFFERS")):
            with self.subTest(path=path):
                api = FakeGitHub()
                api.data[("GET", path)] = response
                with self.assertRaisesRegex(PreflightError, reason):
                    self.inspect(api)
                self.assertEqual(api.calls[-1], ("DELETE", "/installation/token", None))

    def test_permissions_declared_without_write_are_visible(self):
        api = FakeGitHub()
        api.data[("GET", api.path)]["permissions"] = {"contents": "read"}
        self.assertFalse(self.inspect(api)["installation_creation_permissions_declared"])

    def test_minted_write_token_is_rejected_and_revoked(self):
        api = FakeGitHub()
        api.data[("POST", "/app/installations/10/access_tokens")]["permissions"]["administration"] = "write"
        with self.assertRaisesRegex(PreflightError, "PREFLIGHT_TOKEN_NOT_READ_ONLY"):
            self.inspect(api)
        self.assertEqual(api.calls[-1], ("DELETE", "/installation/token", None))

    def test_revocation_failure_is_explicit(self):
        api = FakeGitHub()
        api.data[("DELETE", "/installation/token")] = APIError(503)
        with self.assertRaisesRegex(PreflightError, "PREFLIGHT_TOKEN_REVOCATION_UNCONFIRMED"):
            self.inspect(api)

    @unittest.skipUnless(shutil.which("openssl"), "OpenSSL needed by the optional GitHub adapter")
    def test_signs_short_lived_rs256_jwt_with_ephemeral_fixture_key(self):
        def decode(part):
            return base64.urlsafe_b64decode(part + "=" * (-len(part) % 4))

        with TemporaryDirectory() as directory:
            key = Path(directory) / "key.pem"
            pub = Path(directory) / "public.pem"
            signature = Path(directory) / "signature"
            subprocess.run(["openssl", "genrsa", "-out", str(key), "2048"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            subprocess.run(["openssl", "rsa", "-in", str(key), "-pubout", "-out", str(pub)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            h, c, s = make_app_jwt("client_fixture", key.read_text(), now=1000).split(".")
            self.assertEqual(json.loads(decode(h))["alg"], "RS256")
            self.assertEqual(json.loads(decode(c)), {"iat": 940, "exp": 1300, "iss": "client_fixture"})
            signature.write_bytes(decode(s))
            subprocess.run(["openssl", "dgst", "-sha256", "-verify", str(pub), "-signature", str(signature)],
                           input=f"{h}.{c}".encode(), stdout=subprocess.DEVNULL, check=True)
