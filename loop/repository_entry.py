"""Read-only repository admission for repository-scoped calls.

The application supplies observers and an approved binding lookup. Nothing in
this module opens a session, grants a permission, or executes a procedure.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Callable, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Repository:
    host: str
    repository_id: str
    full_name: str

    @property
    def key(self) -> tuple[str, str]:
        return (self.host.lower(), self.repository_id)


@dataclass(frozen=True)
class Procedure:
    procedure_id: str
    version: str


@dataclass(frozen=True)
class Binding:
    repository_key: tuple[str, str]
    project_id: str
    app_id: int
    procedure: Procedure


@dataclass(frozen=True)
class Recognition:
    repository_key: tuple[str, str]
    project_id: str


@dataclass(frozen=True)
class Installation:
    repository_key: tuple[str, str]
    app_id: int
    installation_id: int
    suspended: bool


class Status(str, Enum):
    READY = "ready_for_procedure"
    REPOSITORY_UNVERIFIED = "repository_unverified"
    MCP_UNVERIFIED = "mcp_unverified"
    REPOSITORY_UNRECOGNIZED = "repository_unrecognized"
    BINDING_MISSING = "binding_missing"
    BINDING_AMBIGUOUS = "binding_ambiguous"
    BINDING_MISMATCH = "binding_mismatch"
    BINDING_UNVERIFIED = "binding_unverified"
    APP_UNVERIFIED = "app_unverified"
    APP_NOT_INSTALLED = "app_not_installed"
    APP_MISMATCH = "app_mismatch"
    APP_SUSPENDED = "app_suspended"
    PROCEDURE_UNVERIFIED = "procedure_unverified"
    PROCEDURE_UNAPPROVED = "procedure_unapproved"


class Unverified(Exception):
    """An observer could not provide authoritative evidence."""


@dataclass(frozen=True)
class EntryResult:
    status: Status
    repository: Repository | None = None
    project_id: str | None = None
    installation_id: int | None = None
    procedure: Procedure | None = None


class EntryRejected(Exception):
    """The repository-scoped call did not pass preflight."""

    def __init__(self, result: EntryResult):
        super().__init__(result.status.value)
        self.result = result


@dataclass(frozen=True)
class RepositoryEntry:
    identify: Callable[[str], Repository]
    recognize: Callable[[Repository], Recognition | None]
    bindings: Callable[[Repository], tuple[Binding, ...]]
    installation: Callable[[Repository, int], Installation | None]
    procedure_approved: Callable[[Procedure], bool]
    expected_app_id: int

    def guard(
        self, locator: str, continue_admission: Callable[[EntryResult], T]
    ) -> T:
        """Gate a scoped call, then hand off to the caller's authorization layer."""
        result = self.before_repository_call(locator)
        if result.status != Status.READY:
            raise EntryRejected(result)
        return continue_admission(result)

    def before_repository_call(self, locator: str) -> EntryResult:
        """Run on each scoped call before any business tool is dispatched.

        Observers raise Unverified on missing access, uncertainty, or outage.
        None denotes a negative answer only from the relevant authority.
        """
        if not isinstance(locator, str) or not locator.strip():
            return EntryResult(Status.REPOSITORY_UNVERIFIED)
        try:
            repo = self.identify(locator)
        except Unverified:
            return EntryResult(Status.REPOSITORY_UNVERIFIED)
        if not (repo.host.strip() and repo.repository_id.strip() and repo.full_name.strip()):
            return EntryResult(Status.REPOSITORY_UNVERIFIED)
        try:
            recognition = self.recognize(repo)
        except Unverified:
            return EntryResult(Status.MCP_UNVERIFIED, repo)
        if recognition is None:
            return EntryResult(Status.REPOSITORY_UNRECOGNIZED, repo)
        if recognition.repository_key != repo.key or not recognition.project_id.strip():
            return EntryResult(Status.BINDING_MISMATCH, repo)
        try:
            candidates = self.bindings(repo)
        except Unverified:
            return EntryResult(Status.BINDING_UNVERIFIED, repo)
        if not candidates:
            return EntryResult(Status.BINDING_MISSING, repo)
        if len(candidates) != 1:
            return EntryResult(Status.BINDING_AMBIGUOUS, repo)
        binding = candidates[0]
        if (
            binding.repository_key != repo.key
            or binding.project_id != recognition.project_id
            or type(binding.app_id) is not int
            or type(self.expected_app_id) is not int
            or self.expected_app_id <= 0
            or binding.app_id != self.expected_app_id
        ):
            return EntryResult(Status.BINDING_MISMATCH, repo)
        try:
            install = self.installation(repo, binding.app_id)
        except Unverified:
            return EntryResult(Status.APP_UNVERIFIED, repo, binding.project_id)
        if install is None:
            return EntryResult(Status.APP_NOT_INSTALLED, repo, binding.project_id)
        if (
            install.repository_key != repo.key
            or install.app_id != binding.app_id
            or type(install.installation_id) is not int
            or install.installation_id <= 0
        ):
            return EntryResult(Status.APP_MISMATCH, repo, binding.project_id)
        if install.suspended:
            return EntryResult(Status.APP_SUSPENDED, repo, binding.project_id)
        procedure = binding.procedure
        if not (procedure.procedure_id.strip() and procedure.version.strip()):
            return EntryResult(Status.PROCEDURE_UNAPPROVED, repo, binding.project_id)
        try:
            approved = self.procedure_approved(procedure)
        except Unverified:
            return EntryResult(Status.PROCEDURE_UNVERIFIED, repo, binding.project_id)
        if approved is not True:
            return EntryResult(Status.PROCEDURE_UNAPPROVED, repo, binding.project_id)
        return EntryResult(
            Status.READY, repo, binding.project_id, install.installation_id, procedure
        )
