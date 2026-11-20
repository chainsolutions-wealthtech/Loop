"""Plan repository onboarding and evaluate existing server checkouts.

An application supplies the evidence readers. This module never installs an
app, writes a registry, connects to a server, or executes a suggested action.
"""

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from pathlib import PurePosixPath
import re
from typing import Callable

from .repository_entry import EntryResult, Repository, RepositoryEntry, Status, Unverified

_GIT_REVISION = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", re.IGNORECASE)


class Coverage(str, Enum):
    COVERED = "covered"
    REPOSITORY_NOT_INCLUDED = "repository_not_included"
    NO_INSTALLATION = "no_installation"
    SUSPENDED = "suspended"


@dataclass(frozen=True)
class AppEvidence:
    repository_key: tuple[str, str]
    app_id: int
    coverage: Coverage
    installation_id: int | None = None


class ProjectMode(str, Enum):
    EXISTING = "existing"
    NEW = "new"


@dataclass(frozen=True)
class ProjectChoice:
    mode: ProjectMode
    project_id: str | None = None

    def valid(self) -> bool:
        if self.mode is ProjectMode.NEW:
            return self.project_id is None
        return (
            self.mode is ProjectMode.EXISTING
            and isinstance(self.project_id, str)
            and bool(self.project_id)
            and self.project_id == self.project_id.strip()
        )


class NextStep(str, Enum):
    RESUME = "resume_existing_project"
    RESOLVE_ENTRY = "resolve_entry_evidence"
    RESOLVE_PROJECT_CONFLICT = "resolve_project_conflict"
    CHOOSE_PROJECT = "choose_existing_or_new_project"
    VERIFY_APP = "verify_app_coverage"
    REQUEST_INSTALLATION = "request_app_installation"
    ADD_REPOSITORY = "add_repository_to_existing_installation"
    RESOLVE_SUSPENSION = "resolve_app_suspension"
    REQUEST_REGISTRATION = "request_canonical_registration"


@dataclass(frozen=True)
class OnboardingPlan:
    next_step: NextStep
    entry: EntryResult
    choice: ProjectChoice | None = None
    app: AppEvidence | None = None
    request_key: str | None = None


@dataclass(frozen=True)
class RepositoryOnboarding:
    entry: RepositoryEntry
    observe_app: Callable[[Repository, int], AppEvidence]

    def plan(self, locator: str, choice: ProjectChoice | None = None) -> OnboardingPlan:
        result = self.entry.before_repository_call(locator)
        if result.project_id is not None and choice is not None and (
            not choice.valid()
            or (choice.mode is ProjectMode.EXISTING and choice.project_id != result.project_id)
        ):
            return OnboardingPlan(NextStep.RESOLVE_PROJECT_CONFLICT, result, choice)
        if result.status is Status.READY:
            return OnboardingPlan(NextStep.RESUME, result)
        if result.status is Status.APP_SUSPENDED:
            return OnboardingPlan(NextStep.RESOLVE_SUSPENSION, result)
        if result.status not in (Status.REPOSITORY_UNRECOGNIZED, Status.APP_NOT_INSTALLED):
            return OnboardingPlan(NextStep.RESOLVE_ENTRY, result)
        repo = result.repository
        app_id = self.entry.expected_app_id
        if repo is None or type(app_id) is not int or app_id <= 0:
            return OnboardingPlan(NextStep.RESOLVE_ENTRY, result)
        if result.status is Status.REPOSITORY_UNRECOGNIZED:
            if choice is None or not choice.valid():
                return OnboardingPlan(NextStep.CHOOSE_PROJECT, result)
        else:
            choice = None  # Existing binding is authoritative, not the caller's preference.

        try:
            app = self.observe_app(repo, app_id)
        except Unverified:
            return OnboardingPlan(NextStep.VERIFY_APP, result, choice)
        if (
            app.repository_key != repo.key
            or type(app.app_id) is not int
            or app.app_id != app_id
            or not isinstance(app.coverage, Coverage)
            or (
                app.coverage is Coverage.NO_INSTALLATION and app.installation_id is not None
            )
            or (
                app.coverage is not Coverage.NO_INSTALLATION
                and (type(app.installation_id) is not int or app.installation_id <= 0)
            )
        ):
            return OnboardingPlan(NextStep.VERIFY_APP, result, choice)

        steps = {
            Coverage.NO_INSTALLATION: NextStep.REQUEST_INSTALLATION,
            Coverage.REPOSITORY_NOT_INCLUDED: NextStep.ADD_REPOSITORY,
            Coverage.SUSPENDED: NextStep.RESOLVE_SUSPENSION,
        }
        if app.coverage in steps:
            return OnboardingPlan(steps[app.coverage], result, choice, app)
        if result.status is Status.APP_NOT_INSTALLED:
            # Two observations disagree. Reobserve before suggesting any change.
            return OnboardingPlan(NextStep.VERIFY_APP, result, app=app)
        assert choice is not None
        # Stable across retries and renames. Deduplication must be enforced by
        # the external registry, which must also recheck the current binding.
        data = ["loop-registration-v1", *repo.key, app_id, choice.mode.value, choice.project_id]
        key = hashlib.sha256(json.dumps(data, separators=(",", ":")).encode()).hexdigest()
        return OnboardingPlan(NextStep.REQUEST_REGISTRATION, result, choice, app, key)


@dataclass(frozen=True)
class CheckoutTarget:
    project_id: str
    repository_key: tuple[str, str]
    server_id: str
    environment_id: str
    real_path: str
    branch: str


@dataclass(frozen=True)
class CheckoutEvidence:
    server_id: str
    environment_id: str
    real_path: str
    remote_repository_key: tuple[str, str]
    branch: str
    revision: str


class CheckoutStatus(str, Enum):
    VERIFIED_CANDIDATE = "verified_checkout_candidate"
    TARGET_UNVERIFIED = "checkout_target_unverified"
    OBSERVATION_UNVERIFIED = "checkout_observation_unverified"
    MISMATCH = "checkout_mismatch"


def evaluate_checkout(
    entry: EntryResult, target: CheckoutTarget, observed: CheckoutEvidence | None
) -> CheckoutStatus:
    """Verify a candidate checkout, not a server binding or a deployed revision.

    Target server, environment and real path come from the host's approved
    inventory. Evidence comes from its read-only observer of that exact target.
    """
    path = PurePosixPath(target.real_path)
    if (
        entry.status is not Status.READY
        or entry.repository is None
        or entry.project_id is None
        or entry.project_id != target.project_id
        or entry.repository.key != target.repository_key
        or not all(value.strip() for value in (
            target.server_id, target.environment_id, target.branch
        ))
        or not path.is_absolute()
        or path.anchor != "/"
        or ".." in path.parts
        or path.as_posix() != target.real_path
        or path.as_posix() == "/"
        or "\x00" in target.real_path
    ):
        return CheckoutStatus.TARGET_UNVERIFIED
    if observed is None or _GIT_REVISION.fullmatch(observed.revision) is None:
        return CheckoutStatus.OBSERVATION_UNVERIFIED
    if (
        observed.server_id != target.server_id
        or observed.environment_id != target.environment_id
        or observed.real_path != target.real_path
        or observed.remote_repository_key != target.repository_key
        or observed.branch != target.branch
    ):
        return CheckoutStatus.MISMATCH
    return CheckoutStatus.VERIFIED_CANDIDATE
