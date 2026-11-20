"""Offline acceptance tests for the public hosting planner."""
from dataclasses import replace
import unittest

from loop.project_anchor import AnchorStatus, DirectoryBinding, DirectoryRole, ProjectAnchor, ProjectAnchorIndex
from loop.repository_entry import Repository
from loop.repository_hosting import (
    DirectoryObservation, DirectoryState, Exposure, HostingRequest, HostingStatus,
    RegistryObservation, plan_repository_hosting,
)


REPO = Repository("github.com", "42", "example/app")
PROJECT_ID = "WT-PROJECT-FIXTURE"
TARGET = DirectoryBinding(
    REPO.key, "S2", "production", "/fixture/app",
    DirectoryRole.RUNTIME, AnchorStatus.VERIFIED_ACTIVE, "EV-TARGET", "REG-TARGET", "a" * 40,
)
REQUEST = HostingRequest(REPO, "production", DirectoryRole.RUNTIME)
TARGETED = replace(REQUEST, server_id="S2", real_path="/fixture/app")
PRESENT = DirectoryObservation(TARGETED, DirectoryState.PRESENT, "PROBE-1", "SCOPE-1", REPO.key)
ABSENT = DirectoryObservation(TARGETED, DirectoryState.ABSENT, "PROBE-2", "SCOPE-1")


def registry(*bindings):
    anchor = ProjectAnchor(PROJECT_ID, (REPO,), bindings)
    return RegistryObservation(ProjectAnchorIndex((anchor,)), "REG-VERSION", REPO.key, True)


class RepositoryHostingTests(unittest.TestCase):
    def test_reuse_verified_runtime_by_stable_repository_id_without_creating(self):
        renamed = replace(REPO, full_name="example/renamed")
        result = plan_repository_hosting(replace(REQUEST, repository=renamed), registry(TARGET))
        self.assertEqual(result.status, HostingStatus.REUSE_VERIFIED)
        self.assertEqual(result.project_id, PROJECT_ID)
        self.assertEqual(result.repository_key, REPO.key)
        self.assertEqual(result.target, TARGET)
        self.assertIsNone(result.plan_id)
        self.assertFalse(result.deployment_requested)
        self.assertEqual(result.evidence_refs, ("REG-VERSION", "EV-TARGET", "REG-TARGET"))


    def test_registry_unobserved_cannot_be_treated_as_an_absent_mapping(self):
        for observation in (None, replace(registry(), complete_for_request=False)):
            result = plan_repository_hosting(TARGETED, observation, ABSENT)
            self.assertEqual(result.status, HostingStatus.UNOBSERVED)
            self.assertIsNone(result.plan_id)

    def test_existing_directory_is_planned_for_attach_only(self):
        result = plan_repository_hosting(TARGETED, registry(), PRESENT)
        self.assertEqual(result.status, HostingStatus.PLAN_ATTACH_EXISTING)
        self.assertEqual(result.project_id, PROJECT_ID)
        self.assertEqual(result.evidence_refs, ("REG-VERSION", "PROBE-1", "SCOPE-1"))
        self.assertIsNone(result.target)
        self.assertTrue(result.plan_id)

    def test_provision_requires_proven_absence_and_an_explicit_exposure_choice(self):
        result = plan_repository_hosting(TARGETED, registry(), ABSENT)
        self.assertEqual((result.status, result.missing), (HostingStatus.NEEDS_CHOICE, ("exposure",)))
        private = replace(TARGETED, exposure=Exposure.PRIVATE)
        result = plan_repository_hosting(private, registry(), ABSENT)
        self.assertEqual(result.status, HostingStatus.PLAN_PROVISION)
        self.assertTrue(result.plan_id)

    def test_another_repository_at_target_is_a_conflict(self):
        evidence = replace(PRESENT, observed_repository_key=("github.com", "99"))
        self.assertEqual(plan_repository_hosting(TARGETED, registry(), evidence).status, HostingStatus.CONFLICT)

    def test_multiple_runtime_targets_require_a_choice(self):
        alt = replace(TARGET, server_id="S1")
        result = plan_repository_hosting(REQUEST, registry(TARGET, alt))
        self.assertEqual(result.status, HostingStatus.NEEDS_CHOICE)
        self.assertEqual(result.missing, ("target",))
        self.assertIsNone(result.target)
        self.assertEqual(result.candidates, (alt, TARGET))
        self.assertEqual(plan_repository_hosting(TARGETED, registry(TARGET, alt)).target, TARGET)


    def test_no_hosting_short_circuits_and_rejects_deployment_without_hosting(self):
        skip = replace(REQUEST, hosting_requested=False)
        self.assertEqual(plan_repository_hosting(skip, None).status, HostingStatus.NO_HOSTING_REQUESTED)
        contradiction = replace(skip, deployment_requested=True)
        self.assertEqual(plan_repository_hosting(contradiction, None).status, HostingStatus.CONFLICT)

    def test_deployment_intent_is_carried_but_not_admitted(self):
        deploy = replace(TARGETED, deployment_requested=True)
        ready = plan_repository_hosting(deploy, registry(TARGET))
        self.assertEqual(ready.status, HostingStatus.REUSE_VERIFIED)
        self.assertTrue(ready.deployment_requested)
        planned = plan_repository_hosting(deploy, registry(), PRESENT)
        self.assertEqual(planned.status, HostingStatus.PLAN_ATTACH_EXISTING)
        self.assertTrue(planned.deployment_requested)
        self.assertIsNone(planned.target)
        checkout = replace(deploy, role=DirectoryRole.CHECKOUT)
        self.assertEqual(plan_repository_hosting(checkout, registry()).status, HostingStatus.CONFLICT)

    def test_repository_registry_evidence_must_be_scoped_and_referenced(self):
        for observed in (
            replace(registry(TARGET), reference=""),
            replace(registry(TARGET), repository_key=("github.com", "99")),
            replace(registry(TARGET), complete_for_request=1),
            replace(registry(TARGET), index=None),
        ):
            self.assertEqual(plan_repository_hosting(REQUEST, observed).status, HostingStatus.UNOBSERVED)

    def test_unknown_project_is_not_created_or_assumed_from_request(self):
        empty = RegistryObservation(ProjectAnchorIndex(()), "REG-EMPTY", REPO.key, True)
        for project, expected in ((None, "project_identity"), (PROJECT_ID, "authoritative_project_registration")):
            result = plan_repository_hosting(replace(TARGETED, project_id=project), empty, PRESENT)
            self.assertEqual((result.status, result.missing), (HostingStatus.NEEDS_CHOICE, (expected,)))
            self.assertIsNone(result.project_id)
            self.assertIsNone(result.plan_id)

    def test_requested_project_cannot_replace_the_authoritative_project(self):
        result = plan_repository_hosting(replace(REQUEST, project_id="OTHER"), registry(TARGET))
        self.assertEqual(result.status, HostingStatus.CONFLICT)

    def test_other_roles_environments_and_servers_do_not_create_ambiguity(self):
        alternatives = (replace(TARGET, server_id="S1", role=DirectoryRole.CHECKOUT),
                        replace(TARGET, server_id="S1", environment_id="staging", real_path="/fixture/stage"))
        result = plan_repository_hosting(REQUEST, registry(TARGET, *alternatives))
        self.assertEqual(result.target, TARGET)

    def test_path_bound_to_a_foreign_project_is_not_reusable(self):
        foreign = Repository("github.com", "123", "other/project")
        foreign_target = replace(TARGET, repository_key=foreign.key)
        index = ProjectAnchorIndex((ProjectAnchor(PROJECT_ID, (REPO,)),
                                    ProjectAnchor("OTHER", (foreign,), (foreign_target,))))
        result = plan_repository_hosting(TARGETED, RegistryObservation(index, "REG", REPO.key, True), PRESENT)
        self.assertEqual(result.status, HostingStatus.CONFLICT)
        self.assertIsNone(result.plan_id)

    def test_partial_question_does_not_repeat_known_values(self):
        missing = plan_repository_hosting(HostingRequest(REPO, role=DirectoryRole.RUNTIME), registry())
        self.assertEqual(missing.missing, ("environment_id",))
        missing = plan_repository_hosting(replace(REQUEST, server_id="S2"), registry())
        self.assertEqual(missing.missing, ("real_path",))

    def test_unsafe_directory_target_is_rejected(self):
        for path in ("relative", "/", "/fixture/../app", "//fixture/app", "/fixture//app"):
            with self.subTest(path=path):
                result = plan_repository_hosting(replace(TARGETED, real_path=path), registry(), ABSENT)
                self.assertEqual(result.status, HostingStatus.CONFLICT)
                self.assertIsNone(result.plan_id)

    def test_directory_evidence_cannot_be_reused_for_a_different_scope(self):
        private = replace(TARGETED, exposure=Exposure.PRIVATE)
        for directory in (None, replace(ABSENT, scope=replace(TARGETED, server_id="S1")),
                          replace(ABSENT, scope=replace(TARGETED, real_path="/fixture/other")),
                          replace(ABSENT, scope=replace(TARGETED, environment_id="test")),
                          replace(ABSENT, scope=replace(TARGETED, role=DirectoryRole.CHECKOUT)),
                          replace(ABSENT, scope_ref=""), replace(ABSENT, evidence_ref="")):
            with self.subTest(directory=directory):
                result = plan_repository_hosting(private, registry(), directory)
                self.assertEqual(result.status, HostingStatus.UNOBSERVED)
                self.assertIsNone(result.plan_id)

    def test_present_directory_without_provenance_is_not_assumed_ours(self):
        result = plan_repository_hosting(TARGETED, registry(), replace(PRESENT, observed_repository_key=None))
        self.assertEqual(result.missing, ("directory_provenance",))
        self.assertEqual(result.status, HostingStatus.UNOBSERVED)

    def test_observed_registry_candidate_never_becomes_a_verified_link(self):
        candidate = replace(TARGET, status=AnchorStatus.OBSERVED, authority_ref=None)
        self.assertEqual(plan_repository_hosting(TARGETED, registry(candidate)).status, HostingStatus.UNOBSERVED)
        result = plan_repository_hosting(TARGETED, registry(candidate), PRESENT)
        self.assertEqual(result.status, HostingStatus.PLAN_ATTACH_EXISTING)
        self.assertIsNone(result.target)

    def test_known_directory_and_absence_proof_conflict(self):
        for state in (AnchorStatus.DECLARED, AnchorStatus.CANDIDATE, AnchorStatus.VERIFIED_ACTIVE):
            with self.subTest(state=state):
                result = plan_repository_hosting(TARGETED, registry(replace(TARGET, status=state)), ABSENT)
                self.assertEqual(result.status, HostingStatus.CONFLICT)
                self.assertIsNone(result.plan_id)

    def test_public_provisioning_questions_separate_host_and_subpath(self):
        subpath = replace(TARGETED, exposure=Exposure.SUBPATH)
        self.assertEqual(plan_repository_hosting(subpath, registry(), ABSENT).missing, ("public_host",))
        subpath = replace(subpath, public_host="example.test")
        self.assertEqual(plan_repository_hosting(subpath, registry(), ABSENT).missing, ("url_path",))
        result = plan_repository_hosting(replace(subpath, url_path="/app"), registry(), ABSENT)
        self.assertEqual(result.status, HostingStatus.PLAN_PROVISION)
        self.assertEqual(result.target_scope.url_path, "/app")
        for exposure in (Exposure.DOMAIN, Exposure.SUBDOMAIN):
            result = plan_repository_hosting(replace(subpath, exposure=exposure), registry(), ABSENT)
            self.assertEqual(result.status, HostingStatus.PLAN_PROVISION)

    def test_public_host_and_ingress_conflicts_do_not_create_a_plan(self):
        for request in (
            replace(TARGETED, exposure=Exposure.SUBPATH, public_host="example.test", url_path="/../app"),
            replace(TARGETED, exposure=Exposure.SUBDOMAIN, public_host="https://example.test"),
            replace(TARGETED, exposure=Exposure.DOMAIN, public_host="example.test", url_path="/app"),
            replace(TARGETED, exposure=Exposure.PRIVATE, public_host="example.test"),
        ):
            with self.subTest(request=request):
                self.assertEqual(plan_repository_hosting(request, registry(), ABSENT).status, HostingStatus.CONFLICT)

    def test_new_public_address_is_not_assumed_on_an_existing_directory(self):
        public = replace(TARGETED, exposure=Exposure.DOMAIN, public_host="example.test")
        for observed in (registry(), registry(TARGET)):
            result = plan_repository_hosting(public, observed, PRESENT)
            self.assertEqual(result.status, HostingStatus.UNOBSERVED)
            self.assertIsNone(result.plan_id)

    def test_plan_key_survives_rename_and_changes_when_target_changes(self):
        base = plan_repository_hosting(TARGETED, registry(), PRESENT)
        renamed = replace(TARGETED, repository=replace(REPO, full_name="other/renamed"))
        retry = plan_repository_hosting(renamed, registry(), replace(PRESENT, evidence_ref="NEW-PROBE"))
        self.assertEqual(base.plan_id, retry.plan_id)
        another = replace(TARGETED, server_id="S1")
        new = plan_repository_hosting(another, registry(), replace(PRESENT, scope=another))
        self.assertNotEqual(base.plan_id, new.plan_id)

    def test_three_owner_names_use_the_same_stable_id_contract(self):
        for i, owner in enumerate(("chainsolutions-wealthtech", "Patricked-code", "Wealthtechinnovations"), 1):
            with self.subTest(owner=owner):
                repo = Repository("github.com", str(i), owner + "/fixture")
                target = replace(TARGET, repository_key=repo.key)
                anchor = ProjectAnchor(PROJECT_ID, (repo,), (target,))
                observed = RegistryObservation(ProjectAnchorIndex((anchor,)), "REG", repo.key, True)
                result = plan_repository_hosting(replace(REQUEST, repository=repo), observed)
                self.assertEqual(result.status, HostingStatus.REUSE_VERIFIED)


    def test_attach_then_replay_only_reuses_after_authoritative_reread(self):
        planned = plan_repository_hosting(TARGETED, registry(), PRESENT)
        self.assertEqual(planned.status, HostingStatus.PLAN_ATTACH_EXISTING)
        self.assertIsNone(planned.target)
        recorded = plan_repository_hosting(TARGETED, registry(TARGET), PRESENT)
        self.assertEqual(recorded.status, HostingStatus.REUSE_VERIFIED)
        self.assertEqual(recorded.target, TARGET)
        self.assertIsNone(recorded.plan_id)

    def test_invalid_input_flags_cannot_be_interpreted_as_user_intent(self):
        request = replace(REQUEST, deployment_requested="false")
        result = plan_repository_hosting(request, registry(TARGET))
        self.assertEqual(result.status, HostingStatus.CONFLICT)
        self.assertFalse(result.deployment_requested)

    def test_present_but_unattributed_exact_probe_blocks_runtime_reuse(self):
        for observation in (replace(PRESENT, observed_repository_key=None),
                            replace(PRESENT, state="absent")):
            result = plan_repository_hosting(TARGETED, registry(TARGET), observation)
            self.assertEqual(result.status, HostingStatus.UNOBSERVED)
            self.assertEqual(result.repository_key, REPO.key)
            self.assertIsNone(result.target)


if __name__ == "__main__":
    unittest.main()
