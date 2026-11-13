"""Resolve canonical project anchors from an injected registry snapshot.

The caller supplies records from the chosen authority. This module never opens
a repository, follows a symlink, makes a remote call, or writes an anchor.
"""
from dataclasses import dataclass
from enum import Enum
from pathlib import PurePosixPath
import re

from .repository_entry import Repository

RepositoryKey = tuple[str, str]
_REVISION = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", re.IGNORECASE)


class AnchorStatus(str, Enum):
    DECLARED = "declared"
    CANDIDATE = "candidate"
    OBSERVED = "observed"
    VERIFIED_ACTIVE = "verified_active"


class DirectoryRole(str, Enum):
    CHECKOUT = "checkout"
    RUNTIME = "runtime"
    PROJECT_DATA = "project_data"


def _token(value: str) -> bool:
    return isinstance(value, str) and bool(value) and not any(
        c.isspace() or ord(c) < 32 or ord(c) == 127 for c in value
    )


def _valid_path(value: str) -> bool:
    if not isinstance(value, str) or any(ord(c) < 32 or ord(c) == 127 for c in value):
        return False
    path = PurePosixPath(value)
    return (
        path.anchor == "/" and value != "/" and path.as_posix() == value
        and ".." not in path.parts
    )


@dataclass(frozen=True)
class DirectoryBinding:
    repository_key: RepositoryKey
    server_id: str
    environment_id: str
    real_path: str
    role: DirectoryRole
    status: AnchorStatus
    # Evidence and authority references are produced by the host, not Loop.
    evidence_ref: str | None = None
    authority_ref: str | None = None
    revision: str | None = None

    def validate(self) -> None:
        if not (
            _token(self.server_id) and _token(self.environment_id)
            and _valid_path(self.real_path)
            and isinstance(self.role, DirectoryRole)
            and isinstance(self.status, AnchorStatus)
        ):
            raise ValueError("invalid server directory binding")
        if self.revision is not None and not _REVISION.fullmatch(self.revision):
            raise ValueError("a recorded revision must be a complete Git object ID")
        if self.status in (AnchorStatus.OBSERVED, AnchorStatus.VERIFIED_ACTIVE):
            if not _token(self.evidence_ref):
                raise ValueError("observed binding requires an evidence reference")
        if self.status is AnchorStatus.VERIFIED_ACTIVE:
            if not _token(self.authority_ref):
                raise ValueError("active binding requires an authority reference")
            if self.role in (DirectoryRole.CHECKOUT, DirectoryRole.RUNTIME) and not self.revision:
                raise ValueError("active checkout or runtime requires a complete revision")


@dataclass(frozen=True)
class ProjectAnchor:
    project_id: str
    repositories: tuple[Repository, ...]
    directories: tuple[DirectoryBinding, ...] = ()


@dataclass(frozen=True)
class DirectoryMatch:
    project: ProjectAnchor
    binding: DirectoryBinding


class ProjectAnchorIndex:
    """Reject ambiguous snapshots and resolve stable keys in either direction."""

    def __init__(self, projects: tuple[ProjectAnchor, ...]):
        self._projects: dict[str, ProjectAnchor] = {}
        self._repos: dict[RepositoryKey, ProjectAnchor] = {}
        self._paths: dict[tuple[str, str], DirectoryMatch] = {}
        for project in projects:
            if not _token(project.project_id) or not project.repositories:
                raise ValueError("project anchor requires an ID and at least one repository")
            if project.project_id in self._projects:
                raise ValueError("duplicate project ID")
            self._projects[project.project_id] = project
            local_keys = set()
            for repo in project.repositories:
                if not all(_token(x) for x in (repo.host, repo.repository_id, repo.full_name)):
                    raise ValueError("invalid repository identity")
                if repo.key in self._repos:
                    raise ValueError("ambiguous stable repository key")
                self._repos[repo.key] = project
                local_keys.add(repo.key)
            for binding in project.directories:
                binding.validate()
                if binding.repository_key not in local_keys:
                    raise ValueError("directory must bind to a repository in the same project")
                key = (binding.server_id, binding.real_path)
                if key in self._paths:
                    raise ValueError("ambiguous server directory")
                self._paths[key] = DirectoryMatch(project, binding)

    def by_project(self, project_id: str) -> ProjectAnchor | None:
        return self._projects.get(project_id)

    def by_repository(self, host: str, repository_id: str) -> ProjectAnchor | None:
        return self._repos.get((host.lower(), repository_id))

    def by_directory(self, server_id: str, real_path: str) -> DirectoryMatch | None:
        if not _token(server_id) or not _valid_path(real_path):
            raise ValueError("expected server ID and canonical absolute path")
        return self._paths.get((server_id, real_path))


def public_index(snapshot: dict) -> ProjectAnchorIndex:
    """Load the Git projection, which deliberately has no server directory records."""
    if snapshot.get("schema_version") != 1 or set(snapshot) != {"schema_version", "projects"}:
        raise ValueError("unsupported public anchor projection")
    projects = []
    for row in snapshot["projects"]:
        if set(row) != {"project_id", "repositories"}:
            raise ValueError("unexpected field in public project anchor")
        repos = []
        for repo in row["repositories"]:
            if set(repo) != {"host", "repository_id", "full_name"}:
                raise ValueError("unexpected field in public repository identity")
            repos.append(Repository(**repo))
        projects.append(ProjectAnchor(row["project_id"], tuple(repos)))
    return ProjectAnchorIndex(tuple(projects))
