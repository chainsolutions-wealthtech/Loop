from dataclasses import replace
import unittest

from loop.repository_entry import (
    Binding, Installation, Procedure, Recognition, Repository, RepositoryEntry,
    Status, Unverified,
)
from loop.repository_onboarding import (
    AppEvidence, CheckoutEvidence, CheckoutStatus, CheckoutTarget, Coverage,
    NextStep, ProjectChoice, ProjectMode, RepositoryOnboarding, evaluate_checkout,
)


class RepositoryOnboardingTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repository("git.example", "42", "org/example")
        self.project = "EXAMPLE-001"
        self.choice = ProjectChoice(ProjectMode.NEW)
        self.procedure = Procedure("intake", "1.0")
        self.app = AppEvidence(self.repo.key, 17, Coverage.COVERED, 123)
        self.recognized = False
        self.installed = True
        self.app_reads = 0
        self.entry = RepositoryEntry(
            identify=lambda locator: self.repo,
            recognize=lambda repo: Recognition(repo.key, self.project) if self.recognized else None,
            bindings=lambda repo: (Binding(repo.key, self.project, 17, self.procedure),),
            installation=lambda repo, app: Installation(repo.key, app, 123, False)
            if self.installed else None,
            procedure_approved=lambda procedure: procedure == self.procedure,
            expected_app_id=17,
        )
        self.workflow = RepositoryOnboarding(self.entry, self.read_app)

    def read_app(self, repository, app_id):
        self.assertEqual(repository.key, self.repo.key)
        self.assertEqual(app_id, 17)
        self.app_reads += 1
        return self.app

    @staticmethod
    def unavailable(*args):
        raise Unverified()

    def plan(self, choice=None):
        return self.workflow.plan(self.repo.full_name, choice)

    def test_known_repository_resumes_without_reinstalling_or_registering(self):
        self.recognized = True
        result = self.plan()
        self.assertEqual(result.next_step, NextStep.RESUME)
        self.assertEqual(result.entry.project_id, self.project)
        self.assertEqual(result.entry.installation_id, 123)
        self.assertEqual(result.entry.procedure, self.procedure)
        self.assertIsNone(result.request_key)
        self.assertEqual(self.app_reads, 0)

    def test_unknown_repository_does_not_imply_new_project(self):
        for choice in (None, ProjectChoice(ProjectMode.EXISTING),
                       ProjectChoice(ProjectMode.NEW, self.project)):
            with self.subTest(choice=choice):
                self.assertEqual(self.plan(choice).next_step, NextStep.CHOOSE_PROJECT)
        self.assertEqual(self.app_reads, 0)

    def test_unreachable_recognition_is_not_unknown_repository(self):
        self.workflow = replace(self.workflow, entry=replace(self.entry, recognize=self.unavailable))
        result = self.plan(self.choice)
        self.assertEqual(result.next_step, NextStep.RESOLVE_ENTRY)
        self.assertEqual(result.entry.status, Status.MCP_UNVERIFIED)
        self.assertEqual(self.app_reads, 0)

    def test_app_access_states_have_different_next_steps(self):
        cases = (
            (Coverage.NO_INSTALLATION, None, NextStep.REQUEST_INSTALLATION),
            (Coverage.REPOSITORY_NOT_INCLUDED, 123, NextStep.ADD_REPOSITORY),
            (Coverage.SUSPENDED, 123, NextStep.RESOLVE_SUSPENSION),
        )
        for coverage, installation_id, step in cases:
            with self.subTest(step=step):
                self.app = replace(self.app, coverage=coverage, installation_id=installation_id)
                result = self.plan(self.choice)
                self.assertEqual(result.next_step, step)
                self.assertIsNone(result.request_key)

    def test_unavailable_or_mismatched_app_evidence_cannot_trigger_registration(self):
        for app in (replace(self.app, app_id=18),
                    replace(self.app, repository_key=("other.example", "42")),
                    replace(self.app, installation_id=0)):
            with self.subTest(app=app):
                self.app = app
                self.assertEqual(self.plan(self.choice).next_step, NextStep.VERIFY_APP)
        self.workflow = replace(self.workflow, observe_app=self.unavailable)
        self.assertEqual(self.plan(self.choice).next_step, NextStep.VERIFY_APP)

    def test_registration_key_is_stable_across_retries_and_repo_rename(self):
        first = self.plan(self.choice)
        self.assertEqual(first.next_step, NextStep.REQUEST_REGISTRATION)
        self.assertTrue(first.request_key)
        self.assertIsNone(first.entry.project_id)
        self.repo = replace(self.repo, full_name="org/renamed")
        self.assertEqual(first.request_key, self.plan(self.choice).request_key)
        self.assertNotEqual(first.request_key,
                            self.plan(ProjectChoice(ProjectMode.EXISTING, self.project)).request_key)

    def test_registration_round_trip_uses_the_id_observed_on_reentry(self):
        pending = self.plan(self.choice)
        self.assertEqual(pending.next_step, NextStep.REQUEST_REGISTRATION)
        # An external registry is simulated as applying the authorized request.
        self.recognized = True
        for _ in range(2):
            result = self.plan(self.choice)
            self.assertEqual(result.next_step, NextStep.RESUME)
            self.assertEqual(result.entry.project_id, self.project)
            self.assertIsNone(result.request_key)

    def test_does_not_overwrite_known_project_with_a_different_choice(self):
        self.recognized = True
        for choice in (ProjectChoice(ProjectMode.EXISTING, "OTHER"),
                       ProjectChoice(ProjectMode.NEW, "OTHER")):
            with self.subTest(choice=choice):
                self.assertEqual(self.plan(choice).next_step, NextStep.RESOLVE_PROJECT_CONFLICT)
        self.assertEqual(self.app_reads, 0)

    def test_missing_app_on_existing_project_is_repaired_without_registration(self):
        self.recognized = True
        self.installed = False
        self.app = replace(self.app, coverage=Coverage.REPOSITORY_NOT_INCLUDED)
        result = self.plan()
        self.assertEqual(result.next_step, NextStep.ADD_REPOSITORY)
        self.assertEqual(result.entry.project_id, self.project)
        self.assertIsNone(result.request_key)
        self.app = replace(self.app, coverage=Coverage.COVERED)
        self.assertEqual(self.plan().next_step, NextStep.VERIFY_APP)

    def checkout(self):
        self.recognized = True
        entry = self.plan().entry
        target = CheckoutTarget(self.project, self.repo.key, "server-a", "test", "/apps/demo", "main")
        evidence = CheckoutEvidence("server-a", "test", "/apps/demo", self.repo.key, "main", "a" * 40)
        return entry, target, evidence

    def test_checkout_matches_the_confirmed_project_and_target(self):
        self.assertEqual(evaluate_checkout(*self.checkout()), CheckoutStatus.VERIFIED_CANDIDATE)

    def test_checkout_missing_or_mismatched_evidence_is_not_verified(self):
        entry, target, evidence = self.checkout()
        for change in (
            {"remote_repository_key": ("git.example", "43")}, {"server_id": "server-b"},
            {"environment_id": "production"}, {"real_path": "/other"}, {"branch": "dev"},
        ):
            with self.subTest(change=change):
                self.assertEqual(evaluate_checkout(entry, target, replace(evidence, **change)),
                                 CheckoutStatus.MISMATCH)
        self.assertEqual(evaluate_checkout(entry, target, None),
                         CheckoutStatus.OBSERVATION_UNVERIFIED)
        self.assertEqual(evaluate_checkout(entry, target, replace(evidence, revision="main")),
                         CheckoutStatus.OBSERVATION_UNVERIFIED)

    def test_checkout_cannot_use_unconfirmed_project_or_noncanonical_path(self):
        entry, target, evidence = self.checkout()
        for change in ({"project_id": "OTHER"}, {"real_path": "/a/../apps/demo"},
                       {"real_path": "//apps/demo"}, {"real_path": "/"}):
            with self.subTest(change=change):
                self.assertEqual(evaluate_checkout(entry, replace(target, **change), evidence),
                                 CheckoutStatus.TARGET_UNVERIFIED)
        self.assertEqual(evaluate_checkout(replace(entry, status=Status.APP_SUSPENDED), target,
                                           evidence), CheckoutStatus.TARGET_UNVERIFIED)


if __name__ == "__main__":
    unittest.main()
