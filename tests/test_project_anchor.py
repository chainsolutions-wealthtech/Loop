from dataclasses import replace
import unittest

from loop.project_anchor import (
    AnchorStatus, DirectoryBinding, DirectoryRole, ProjectAnchor,
    ProjectAnchorIndex, public_index,
)
from loop.repository_entry import Repository


REPO = Repository("github.com", "42", "example/repo")
OTHER = Repository("github.com", "43", "example/other")
SHA = "a" * 40
CHECKOUT = DirectoryBinding(
    REPO.key, "S1", "production", "/fixture/project/checkout",
    DirectoryRole.CHECKOUT, AnchorStatus.VERIFIED_ACTIVE, "EV-42", "REG-42", SHA,
)
RUNTIME = replace(CHECKOUT, real_path="/fixture/project/runtime", role=DirectoryRole.RUNTIME)
PROJECT = ProjectAnchor("TEST-PROJECT-01", (REPO,), (CHECKOUT, RUNTIME))


class ProjectAnchorTests(unittest.TestCase):
    def test_one_id_resolves_repository_and_multiple_directories(self):
        index = ProjectAnchorIndex((PROJECT,))
        self.assertEqual(index.by_project(PROJECT.project_id), PROJECT)
        self.assertEqual(index.by_repository("GitHub.com", "42"), PROJECT)
        for binding in PROJECT.directories:
            match = index.by_directory(binding.server_id, binding.real_path)
            self.assertEqual(match.project, PROJECT)
            self.assertEqual(match.binding, binding)

    def test_rename_does_not_change_repository_lookup(self):
        renamed = replace(PROJECT, repositories=(replace(REPO, full_name="new/repo"),))
        self.assertEqual(ProjectAnchorIndex((renamed,)).by_repository("github.com", "42"), renamed)

    def test_unattested_project_may_have_no_server_binding(self):
        declared = replace(PROJECT, directories=())
        index = ProjectAnchorIndex((declared,))
        self.assertEqual(index.by_project(PROJECT.project_id), declared)
        self.assertIsNone(index.by_directory("S1", CHECKOUT.real_path))

    def test_candidate_and_observed_states_are_not_promoted(self):
        for state in (AnchorStatus.DECLARED, AnchorStatus.CANDIDATE, AnchorStatus.OBSERVED):
            with self.subTest(state=state):
                pending = replace(CHECKOUT, status=state, authority_ref=None, revision=None)
                index = ProjectAnchorIndex((replace(PROJECT, directories=(pending,)),))
                self.assertIs(index.by_directory("S1", pending.real_path).binding.status, state)

    def test_active_binding_requires_authority_evidence_and_exact_revision(self):
        for bad in (
            replace(CHECKOUT, authority_ref=None), replace(CHECKOUT, evidence_ref=None),
            replace(CHECKOUT, revision=None), replace(CHECKOUT, revision="abc123"),
        ):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                ProjectAnchorIndex((replace(PROJECT, directories=(bad,)),))

    def test_ambiguous_repository_and_directory_are_rejected(self):
        conflicting_path = replace(CHECKOUT, repository_key=OTHER.key, environment_id="test")
        for other in (
            ProjectAnchor("TEST-PROJECT-02", (REPO,)),
            ProjectAnchor("TEST-PROJECT-02", (OTHER,), (conflicting_path,)),
        ):
            with self.subTest(other=other), self.assertRaises(ValueError):
                ProjectAnchorIndex((PROJECT, other))

    def test_same_absolute_path_on_distinct_servers_is_allowed(self):
        target = replace(CHECKOUT, server_id="S2")
        index = ProjectAnchorIndex((replace(PROJECT, directories=(CHECKOUT, target)),))
        self.assertEqual(index.by_directory("S2", target.real_path).binding, target)

    def test_checkout_cannot_bind_a_repository_from_another_project(self):
        with self.assertRaises(ValueError):
            ProjectAnchorIndex((replace(PROJECT, repositories=(OTHER,)),))

    def test_reject_noncanonical_paths(self):
        for path in ("relative/path", "/fixture//project", "/fixture/../project", "/", "//root/path"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                ProjectAnchorIndex((replace(PROJECT, directories=(replace(CHECKOUT, real_path=path),)),))

    def test_public_projection_does_not_accept_server_paths(self):
        with self.assertRaises(ValueError):
            public_index({"schema_version": 1, "projects": [
                {"project_id": "TEST-PROJECT-01", "repositories": [], "directories": ["/fixture"]}
            ]})


if __name__ == "__main__":
    unittest.main()
