"""Read-only decision seam for LOOP-CAP-006."""
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
import re

from .project_anchor import (
    AnchorStatus, DirectoryBinding, DirectoryRole, ProjectAnchorIndex, RepositoryKey,
)
from .repository_entry import Repository


class HostingStatus(str, Enum):
    REUSE_VERIFIED = "REUSE_VERIFIED"
    NO_HOSTING_REQUESTED = "NO_HOSTING_REQUESTED"
    NEEDS_CHOICE = "NEEDS_CHOICE"
    CONFLICT = "CONFLICT"
    UNOBSERVED = "UNOBSERVED"
    PLAN_ATTACH_EXISTING = "PLAN_ATTACH_EXISTING"
    PLAN_PROVISION = "PLAN_PROVISION"


class DirectoryState(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"


class Exposure(str, Enum):
    PRIVATE = "private"
    SUBPATH = "subpath"
    SUBDOMAIN = "subdomain"
    DOMAIN = "domain"


@dataclass(frozen=True)
class HostingRequest:
    repository: Repository
    environment_id: str | None = None
    role: DirectoryRole | None = None
    hosting_requested: bool = True
    deployment_requested: bool = False
    server_id: str | None = None
    real_path: str | None = None
    exposure: Exposure | None = None
    public_host: str | None = None
    url_path: str | None = None
    project_id: str | None = None


@dataclass(frozen=True)
class RegistryObservation:
    index: ProjectAnchorIndex
    reference: str
    repository_key: RepositoryKey
    # True only for a complete, authoritative view, not a candidate projection.
    complete_for_request: bool = False


@dataclass(frozen=True)
class DirectoryObservation:
    scope: HostingRequest
    state: DirectoryState
    evidence_ref: str
    scope_ref: str
    observed_repository_key: RepositoryKey | None = None


@dataclass(frozen=True)
class HostingDecision:
    status: HostingStatus
    project_id: str | None = None
    target: DirectoryBinding | None = None
    plan_id: str | None = None
    deployment_requested: bool = False
    missing: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    target_scope: HostingRequest | None = None
    candidates: tuple[DirectoryBinding, ...] = ()
    repository_key: RepositoryKey | None = None


_HOST = re.compile(r"(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", re.ASCII,
)
_SUBPATH = re.compile(r"(?:/[A-Za-z0-9_-]+)+", re.ASCII)


def _ref(value: str | None) -> bool:
    return isinstance(value, str) and bool(value) and all(
        c.isprintable() and not c.isspace() for c in value
    )


def _scope(request: HostingRequest) -> tuple[RepositoryKey, str | None, str | None, str | None, DirectoryRole | None]:
    return (request.repository.key, request.server_id, request.real_path,
            request.environment_id, request.role)


def _binding_scope(binding: DirectoryBinding) -> tuple[RepositoryKey, str, str, str, DirectoryRole]:
    return (binding.repository_key, binding.server_id, binding.real_path,
            binding.environment_id, binding.role)


def _public_address(request: HostingRequest) -> tuple[HostingStatus, tuple[str, ...]] | None:
    if request.exposure is None:
        return HostingStatus.NEEDS_CHOICE, ("exposure",)
    if request.exposure is Exposure.PRIVATE:
        if request.public_host is not None or request.url_path is not None:
            return HostingStatus.CONFLICT, ("private_exposure_has_public_address",)
        return None
    if not isinstance(request.exposure, Exposure):
        return HostingStatus.CONFLICT, ("invalid_exposure",)
    if request.public_host is None:
        return HostingStatus.NEEDS_CHOICE, ("public_host",)
    if not isinstance(request.public_host, str) or not _HOST.fullmatch(request.public_host):
        return HostingStatus.CONFLICT, ("invalid_public_host",)
    if request.exposure is Exposure.SUBPATH:
        if request.url_path is None:
            return HostingStatus.NEEDS_CHOICE, ("url_path",)
        if not isinstance(request.url_path, str) or not _SUBPATH.fullmatch(request.url_path):
            return HostingStatus.CONFLICT, ("invalid_url_path",)
    elif request.url_path not in (None, "/"):
        return HostingStatus.CONFLICT, ("unexpected_url_path",)
    return None


def plan_repository_hosting(
    request: HostingRequest, registry: RegistryObservation | None,
    directory: DirectoryObservation | None = None,
) -> HostingDecision:
    """Return one next decision. Inputs must come from the caller's trusted observers.

    No I/O, identity creation, consent, write, or deployment takes place here.
    """
    if type(request.hosting_requested) is not bool or type(request.deployment_requested) is not bool:
        return HostingDecision(HostingStatus.CONFLICT, missing=("invalid_request_flags",))
    if not request.hosting_requested:
        if request.deployment_requested:
            return HostingDecision(HostingStatus.CONFLICT, missing=("deployment_without_hosting",))
        return HostingDecision(HostingStatus.NO_HOSTING_REQUESTED)
    if (not isinstance(request.repository, Repository) or not all(_ref(v) for v in (
            request.repository.host, request.repository.repository_id, request.repository.full_name,
        )) or (request.role is not None and not isinstance(request.role, DirectoryRole))
            or any(v is not None and not _ref(v) for v in (
                request.environment_id, request.server_id, request.project_id))):
        return HostingDecision(HostingStatus.CONFLICT, missing=("invalid_request",))
    if (registry is None or not isinstance(registry.index, ProjectAnchorIndex) or not _ref(registry.reference)
            or registry.complete_for_request is not True
            or registry.repository_key != request.repository.key):
        return HostingDecision(
            HostingStatus.UNOBSERVED, missing=("authoritative_registry",),
            repository_key=request.repository.key, deployment_requested=request.deployment_requested,
        )

    anchor = registry.index.by_repository(*request.repository.key)
    project_id = anchor.project_id if anchor else None
    refs = (registry.reference,)

    def decide(
        status: HostingStatus, missing: tuple[str, ...] = (), *,
        target: DirectoryBinding | None = None, plan_id: str | None = None,
        scope: HostingRequest | None = None, candidates: tuple[DirectoryBinding, ...] = (),
    ) -> HostingDecision:
        return HostingDecision(
            status=status, project_id=project_id, target=target, plan_id=plan_id,
            deployment_requested=request.deployment_requested, missing=missing,
            evidence_refs=refs, target_scope=scope, candidates=candidates,
            repository_key=request.repository.key,
        )

    if request.project_id is not None and project_id is not None and request.project_id != project_id:
        return decide(HostingStatus.CONFLICT, ("project_identity_mismatch",))
    if request.real_path is not None and request.server_id is None:
        return decide(HostingStatus.NEEDS_CHOICE, ("server_id",))
    if request.real_path is not None:
        try:
            occupant = registry.index.by_directory(request.server_id, request.real_path)
        except ValueError:
            return decide(HostingStatus.CONFLICT, ("invalid_real_path",))
        if occupant is not None and (
                occupant.binding.repository_key != request.repository.key
                or (request.environment_id is not None and occupant.binding.environment_id != request.environment_id)
                or (request.role is not None and occupant.binding.role is not request.role)):
            return decide(HostingStatus.CONFLICT, ("directory_already_bound_to_another_scope",))
    if anchor is None:
        missing = "project_identity" if request.project_id is None else "authoritative_project_registration"
        return decide(HostingStatus.NEEDS_CHOICE, (missing,))
    needs = tuple(name for name in ("environment_id", "role") if getattr(request, name) is None)
    if needs:
        return decide(HostingStatus.NEEDS_CHOICE, needs)
    if request.deployment_requested and request.role is not DirectoryRole.RUNTIME:
        return decide(HostingStatus.CONFLICT, ("deployment_requires_runtime_target",))

    scoped = tuple(item for item in anchor.directories if (
        item.repository_key == request.repository.key
        and item.environment_id == request.environment_id and item.role is request.role
        and (request.server_id is None or item.server_id == request.server_id)
        and (request.real_path is None or item.real_path == request.real_path)
    ))
    active = tuple(item for item in scoped if item.status is AnchorStatus.VERIFIED_ACTIVE)
    if len(active) > 1:
        return decide(HostingStatus.NEEDS_CHOICE, ("target",), candidates=tuple(sorted(
            active, key=lambda item: (item.server_id, item.real_path),
        )))
    if active:
        if request.exposure is not None or request.public_host is not None or request.url_path is not None:
            return decide(HostingStatus.UNOBSERVED, ("existing_exposure_not_attested",))
        if directory is not None and _scope(directory.scope) == _binding_scope(active[0]):
            if not _ref(directory.evidence_ref) or not _ref(directory.scope_ref):
                return decide(HostingStatus.UNOBSERVED, ("directory_observation_for_exact_scope",))
            if not isinstance(directory.state, DirectoryState):
                return decide(HostingStatus.UNOBSERVED, ("directory_state",))
            refs += (directory.evidence_ref, directory.scope_ref)
            if directory.state is DirectoryState.ABSENT:
                return decide(HostingStatus.CONFLICT, ("active_link_conflicts_with_directory_observation",))
            if directory.observed_repository_key is None:
                return decide(HostingStatus.UNOBSERVED, ("directory_provenance",))
            if directory.observed_repository_key != request.repository.key:
                return decide(HostingStatus.CONFLICT, ("active_link_conflicts_with_directory_observation",))
        refs += tuple(ref for ref in (active[0].evidence_ref, active[0].authority_ref) if ref is not None)
        return decide(HostingStatus.REUSE_VERIFIED, target=active[0])
    needs = tuple(name for name in ("server_id", "real_path") if getattr(request, name) is None)
    if needs:
        return decide(HostingStatus.NEEDS_CHOICE, needs)
    if (directory is None or _scope(directory.scope) != _scope(request)
            or not _ref(directory.evidence_ref) or not _ref(directory.scope_ref)):
        return decide(HostingStatus.UNOBSERVED, ("directory_observation_for_exact_scope",))

    refs += (directory.evidence_ref, directory.scope_ref)
    if directory.state is DirectoryState.PRESENT:
        if directory.observed_repository_key is None:
            return decide(HostingStatus.UNOBSERVED, ("directory_provenance",))
        if directory.observed_repository_key != request.repository.key:
            return decide(HostingStatus.CONFLICT, ("directory_repository_mismatch",))
        if request.exposure is not None or request.public_host is not None or request.url_path is not None:
            return decide(HostingStatus.UNOBSERVED, ("existing_exposure_not_attested",))
        status = HostingStatus.PLAN_ATTACH_EXISTING
    elif directory.state is DirectoryState.ABSENT:
        if directory.observed_repository_key is not None or scoped:
            return decide(HostingStatus.CONFLICT, ("absence_conflicts_with_known_directory",))
        problem = _public_address(request)
        if problem is not None:
            return decide(*problem)
        status = HostingStatus.PLAN_PROVISION
    else:
        return decide(HostingStatus.UNOBSERVED, ("directory_state",))

    key = [status.value, project_id, *_scope(request), request.exposure,
           request.public_host, request.url_path or ("/" if request.public_host else None)]
    plan_id = "hosting-v1:" + sha256(json.dumps(key, separators=(",", ":")).encode()).hexdigest()
    return decide(status, plan_id=plan_id, scope=request)
