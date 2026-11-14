from dataclasses import replace
import unittest

from loop.repository_entry import (
    Binding, EntryRejected, Installation, Procedure, Recognition, Repository, RepositoryEntry,
    Status, Unverified,
)


class RepositoryEntryTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repository("github.example", "42", "example/repository")
        self.procedure = Procedure("project-intake", "1.0")
        self.binding = Binding(self.repo.key, "EXAMPLE-001", 17, self.procedure)
        self.recognition = Recognition(self.repo.key, self.binding.project_id)
        self.installation = Installation(self.repo.key, 17, 345, False)
        self.calls = []
        self.entry = RepositoryEntry(
            identify=lambda locator: self.observed("identify", self.repo),
            recognize=lambda repo: self.observed("recognize", self.recognition),
            bindings=lambda repo: self.observed("bindings", (self.binding,)),
            installation=lambda repo, app: self.observed("installation", self.installation),
            procedure_approved=lambda proc: self.observed("procedure", True),
            expected_app_id=17,
        )

    def observed(self, name, value):
        self.calls.append(name)
        return value

    def check(self, entry=None, locator="example/repository"):
        return (entry or self.entry).before_repository_call(locator)

    @staticmethod
    def unavailable(*args):
        raise Unverified()

    def test_valid_chain_returns_versioned_procedure_without_running_it(self):
        result = self.check()
        self.assertEqual(result.status, Status.READY)
        self.assertEqual(result.project_id, "EXAMPLE-001")
        self.assertEqual(result.installation_id, 345)
        self.assertEqual(result.procedure, self.procedure)
        self.assertEqual(self.calls, ["identify", "recognize", "bindings", "installation", "procedure"])

    def test_unscoped_call_does_not_assume_previous_repository(self):
        self.assertEqual(self.check(locator="").status, Status.REPOSITORY_UNVERIFIED)
        self.assertEqual(self.calls, [])

    def test_repository_observer_failure(self):
        self.assertEqual(self.check(replace(self.entry, identify=self.unavailable)).status,
                         Status.REPOSITORY_UNVERIFIED)

    def test_unknown_repository_and_unavailable_registry_are_distinct(self):
        for observe, status in (
            (lambda repo: None, Status.REPOSITORY_UNRECOGNIZED),
            (self.unavailable, Status.MCP_UNVERIFIED),
        ):
            with self.subTest(status=status):
                self.assertEqual(self.check(replace(self.entry, recognize=observe)).status, status)
        self.assertEqual(self.calls, ["identify", "identify"])

    def test_another_repository_on_same_or_other_host_is_rejected(self):
        for key in (("github.example", "43"), ("different.example", "42")):
            with self.subTest(key=key):
                self.recognition = replace(self.recognition, repository_key=key)
                self.assertEqual(self.check().status, Status.BINDING_MISMATCH)

    def test_missing_and_multiple_bindings_are_distinct(self):
        for bindings, status in (
            ((), Status.BINDING_MISSING), ((self.binding, self.binding), Status.BINDING_AMBIGUOUS),
        ):
            with self.subTest(status=status):
                entry = replace(self.entry, bindings=lambda repo: bindings)
                self.assertEqual(self.check(entry).status, status)
        self.assertNotIn("installation", self.calls)

    def test_registry_failure_is_not_an_absent_binding(self):
        self.assertEqual(self.check(replace(self.entry, bindings=self.unavailable)).status,
                         Status.BINDING_UNVERIFIED)

    def test_binding_must_match_canonical_id_and_expected_app(self):
        for data in ({"project_id": "OTHER"}, {"app_id": 18}):
            with self.subTest(data=data):
                changed = replace(self.binding, **data)
                self.assertEqual(
                    self.check(replace(self.entry, bindings=lambda repo: (changed,))).status,
                    Status.BINDING_MISMATCH,
                )

    def test_app_unverified_missing_mismatched_and_suspended(self):
        wrong_repo = replace(self.installation, repository_key=("github.example", "43"))
        wrong_app = replace(self.installation, app_id=18)
        suspended = replace(self.installation, suspended=True)
        for observe, status in (
            (self.unavailable, Status.APP_UNVERIFIED),
            (lambda repo, app: None, Status.APP_NOT_INSTALLED),
            (lambda repo, app: wrong_repo, Status.APP_MISMATCH),
            (lambda repo, app: wrong_app, Status.APP_MISMATCH),
            (lambda repo, app: suspended, Status.APP_SUSPENDED),
        ):
            with self.subTest(status=status):
                result = self.check(replace(self.entry, installation=observe))
                self.assertEqual(result.status, status)
                self.assertIsNone(result.procedure)
        self.assertNotIn("procedure", self.calls)

    def test_procedure_must_be_approved_and_verifiable(self):
        for observe, status in (
            (lambda proc: False, Status.PROCEDURE_UNAPPROVED),
            (self.unavailable, Status.PROCEDURE_UNVERIFIED),
        ):
            with self.subTest(status=status):
                result = self.check(replace(self.entry, procedure_approved=observe))
                self.assertEqual(result.status, status)
                self.assertIsNone(result.procedure)

    def test_renamed_repository_uses_the_stable_id(self):
        self.repo = replace(self.repo, full_name="new-owner/new-name")
        self.assertEqual(self.check(locator=self.repo.full_name).status, Status.READY)

    def test_rechecks_installation_on_each_call(self):
        self.assertEqual(self.check().status, Status.READY)
        self.installation = replace(self.installation, suspended=True)
        self.assertEqual(self.check().status, Status.APP_SUSPENDED)
        self.assertEqual(self.calls.count("installation"), 2)

    def test_hook_checks_before_handing_off_to_authorization(self):
        def authorization(result):
            self.assertEqual(result.procedure, self.procedure)
            return self.observed("authorization", "handoff")

        self.assertEqual(self.entry.guard("example/repository", authorization), "handoff")
        self.assertEqual(self.calls[-2:], ["procedure", "authorization"])
        self.installation = None
        with self.assertRaises(EntryRejected) as blocked:
            self.entry.guard("example/repository", authorization)
        self.assertEqual(blocked.exception.result.status, Status.APP_NOT_INSTALLED)
        self.assertEqual(self.calls.count("authorization"), 1)


if __name__ == "__main__":
    unittest.main()
