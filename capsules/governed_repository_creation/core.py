"""Portable governed creation. The caller supplies identity scope and a trusted gateway."""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import re
from typing import Protocol
from uuid import uuid4


class Conflict(Exception):
    """The request or its target cannot be changed by this operation."""


class StaleRevision(Conflict):
    """Read the durable state again before resuming."""


class NotFound(Exception):
    """The request is not visible in this scope."""


class GatewayUnavailable(Exception):
    """The gateway cannot currently supply a definitive result."""


class BootstrapFailed(Exception):
    """The bootstrap execution is attested as unsuccessful."""


class InvalidEvidence(Exception):
    """A gateway response does not match the operation or the pinned source."""


@dataclass(frozen=True)
class Target:
    owner: str
    name: str
    visibility: str


@dataclass(frozen=True)
class Authorization:
    template_revision: str
    evidence_ref: str


@dataclass(frozen=True)
class Observation:
    # Unknown, confirmed absent, or present. A raw 404 is not confirmed absence.
    kind: str
    evidence_ref: str | None = None
    repository_id: int | None = None


@dataclass(frozen=True)
class CreationReceipt:
    attempt_id: str
    target: Target
    repository_id: int
    repository_url: str
    evidence_ref: str


@dataclass(frozen=True)
class Head:
    repository_id: int
    branch: str
    sha: str
    evidence_ref: str


@dataclass(frozen=True)
class Bootstrap:
    repository_id: int
    template_revision: str
    sha: str
    run_ref: str


@dataclass(frozen=True)
class State:
    request_id: str
    scope: str
    key: str
    continuity_id: str | None = None
    owner: str | None = None
    name: str | None = None
    visibility: str | None = None
    revision: int = 1
    phase: str = "QUALIFY"
    reason: str | None = None
    authorization: Authorization | None = None
    absence_ref: str | None = None
    attempt_id: str | None = None
    creation: CreationReceipt | None = None
    initial_head: Head | None = None
    bootstrap: Bootstrap | None = None
    final_head: Head | None = None

    @property
    def missing(self) -> tuple[str, ...]:
        return tuple(name for name in ("owner", "name", "visibility") if not getattr(self, name))

    @property
    def target(self) -> Target:
        if self.missing:
            raise ValueError("incomplete target")
        return Target(self.owner, self.name, self.visibility)

    @property
    def next_action(self) -> str | None:
        if self.phase == "QUALIFY":
            return "ANSWER_CREATION_QUESTIONS" if self.missing else "VERIFY_AUTHORITY_AND_TARGET"
        return {
            "CREATE_OUTCOME_PENDING": "RECONCILE_CREATION_WITHOUT_RESUBMITTING",
            "READ_INITIAL_HEAD": "READ_INITIAL_HEAD",
            "VERIFY_BOOTSTRAP": "VERIFY_BOOTSTRAP",
            "READ_HANDOFF_HEAD": "RECONCILE_HANDOFF_HEAD" if self.reason == "HEAD_DIVERGED" else "READ_HANDOFF_HEAD",
            "HANDOFF_READY": "DISCOVER_PROJECT_BASELINE",
        }[self.phase]

    @property
    def handoff(self) -> dict | None:
        if self.phase != "HANDOFF_READY":
            return None
        return {
            "request_id": self.request_id,
            "continuity_id": self.continuity_id,
            "repository_id": self.creation.repository_id,
            "repository": self.creation.repository_url.rstrip("/").removeprefix("https://github.com/"),
            "repository_url": self.creation.repository_url,
            "branch": self.final_head.branch,
            "initial_observed_head_sha": self.initial_head.sha,
            "head_sha": self.final_head.sha,
            "bootstrap": asdict(self.bootstrap),
            "evidence_refs": (
                self.authorization.evidence_ref, self.absence_ref, self.creation.evidence_ref,
                self.initial_head.evidence_ref, self.bootstrap.run_ref, self.final_head.evidence_ref,
            ),
            "infrastructure": "UNRESOLVED",
            "next_action": self.next_action,
        }


class Store(Protocol):
    def submit(self, state: State) -> State: ...
    def get(self, scope: str, request_id: str) -> State: ...
    def compare_and_save(self, previous: State, replacement: State) -> State: ...


class Gateway(Protocol):
    """Only create_once may mutate externally. Other methods must be reads.

    A recover result is evidence of this attempt, not just template provenance.
    authorize_create must enforce actual authority and return the pinned template.
    create_once must enforce authority at execution and not blindly retry POST.
    """
    def authorize_create(self, state: State) -> Authorization | None: ...
    def observe_target(self, target: Target) -> Observation: ...
    def create_once(self, intent: State) -> CreationReceipt: ...
    def recover_creation(self, intent: State) -> CreationReceipt | None: ...
    def read_head(self, creation: CreationReceipt) -> Head | None: ...
    def read_bootstrap(self, creation: CreationReceipt, authorization: Authorization) -> Bootstrap | None: ...


def _string(value: str | None, field: str, pattern: str | None = None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip() or len(value) > 200:
        raise ValueError(f"invalid {field}")
    if pattern and re.fullmatch(pattern, value) is None:
        raise ValueError(f"invalid {field}")
    return value


def _answers(owner: str | None, name: str | None, visibility: str | None) -> dict:
    owner = _string(owner, "owner", r"[A-Za-z0-9][A-Za-z0-9-]{0,38}")
    name = _string(name, "name", r"[A-Za-z0-9_.-]{1,100}")
    if name in {".", ".."} or (visibility is not None and visibility not in ("public", "private")):
        raise ValueError("invalid repository name or visibility")
    return {"owner": owner.lower() if owner else None, "name": name.lower() if name else None,
            "visibility": visibility}


class Capsule:
    def __init__(self, store: Store, gateway: Gateway):
        self.store = store
        self.gateway = gateway

    def submit(self, scope: str, key: str, *, continuity_id: str | None = None,
               owner: str | None = None, name: str | None = None,
               visibility: str | None = None) -> State:
        if scope is None or key is None:
            raise ValueError("scope and key are required")
        _string(scope, "scope")
        _string(key, "key")
        _string(continuity_id, "continuity_id")
        return self.store.submit(State(str(uuid4()), scope, key, continuity_id,
                                       **_answers(owner, name, visibility)))

    def consult(self, scope: str, request_id: str) -> State:
        return self.store.get(scope, request_id)

    def resume(self, scope: str, request_id: str, expected_revision: int, *,
               owner: str | None = None, name: str | None = None,
               visibility: str | None = None) -> State:
        state = self.consult(scope, request_id)
        if state.revision != expected_revision:
            raise StaleRevision("request revision changed")
        answers = {k: v for k, v in _answers(owner, name, visibility).items() if v is not None}
        if any(getattr(state, k) not in (None, v) for k, v in answers.items()):
            raise Conflict("an established creation answer cannot be replaced")
        new_answers = {k: v for k, v in answers.items() if getattr(state, k) is None}
        if new_answers:
            if state.phase != "QUALIFY":
                raise Conflict("creation answers are closed")
            return self._save(state, **new_answers, reason=None)
        if state.phase == "HANDOFF_READY" or state.missing:
            return state
        try:
            if state.phase == "QUALIFY":
                return self._begin(state)
            if state.phase == "CREATE_OUTCOME_PENDING":
                receipt = self.gateway.recover_creation(state)
                if receipt is None:
                    return self._save(state, reason="CREATION_NOT_CORRELATED")
                return self._record_creation(state, receipt)
            if state.phase == "READ_INITIAL_HEAD":
                head = self.gateway.read_head(state.creation)
                if head is None:
                    return self._save(state, reason="INITIAL_HEAD_NOT_AVAILABLE")
                self._check_head(state, head)
                return self._save(state, phase="VERIFY_BOOTSTRAP", initial_head=head, reason=None)
            if state.phase == "VERIFY_BOOTSTRAP":
                proof = self.gateway.read_bootstrap(state.creation, state.authorization)
                if proof is None:
                    return self._save(state, reason="BOOTSTRAP_NOT_ATTESTED")
                if (proof.repository_id != state.creation.repository_id
                        or proof.template_revision != state.authorization.template_revision
                        or not _is_sha(proof.sha) or not proof.run_ref):
                    raise InvalidEvidence("bootstrap proof mismatch")
                return self._save(state, phase="READ_HANDOFF_HEAD", bootstrap=proof, reason=None)
            if state.phase == "READ_HANDOFF_HEAD":
                head = self.gateway.read_head(state.creation)
                if head is None:
                    return self._save(state, reason="HANDOFF_HEAD_NOT_AVAILABLE")
                self._check_head(state, head)
                if head.branch != state.initial_head.branch or head.sha != state.bootstrap.sha:
                    return self._save(state, reason="HEAD_DIVERGED")
                return self._save(state, phase="HANDOFF_READY", final_head=head, reason=None)
            raise ValueError("unknown durable phase")
        except BootstrapFailed:
            return self._save(state, reason="BOOTSTRAP_FAILED")
        except GatewayUnavailable:
            return self._save(state, reason="GATEWAY_UNAVAILABLE")
        except InvalidEvidence:
            return self._save(state, reason="EVIDENCE_CONFLICT")

    def _save(self, state: State, **changes) -> State:
        updated = replace(state, **changes)
        if updated == state:
            return state
        return self.store.compare_and_save(state, replace(updated, revision=state.revision + 1))

    def _begin(self, state: State) -> State:
        approval = self.gateway.authorize_create(state)
        if approval is None:
            return self._save(state, reason="AUTHORITY_NOT_VERIFIED")
        if not _is_sha(approval.template_revision) or not approval.evidence_ref:
            raise InvalidEvidence("incomplete creation authorization")
        observed = self.gateway.observe_target(state.target)
        if observed.kind == "present":
            return self._save(state, reason="TARGET_ALREADY_EXISTS")
        if observed.kind != "absent" or not observed.evidence_ref or observed.repository_id is not None:
            return self._save(state, reason="TARGET_ABSENCE_NOT_VERIFIED")

        # CAS and durable commit come first. Only their winner may create.
        intent = self._save(
            state, phase="CREATE_OUTCOME_PENDING", reason=None, attempt_id=str(uuid4()),
            authorization=approval, absence_ref=observed.evidence_ref,
        )
        try:
            receipt = self.gateway.create_once(intent)
            return self._record_creation(intent, receipt)
        except GatewayUnavailable:
            return self._save(intent, reason="CREATION_OUTCOME_UNKNOWN")
        except InvalidEvidence:
            return self._save(intent, reason="EVIDENCE_CONFLICT")

    def _record_creation(self, state: State, receipt: CreationReceipt) -> State:
        if (receipt.attempt_id != state.attempt_id or receipt.target != state.target
                or type(receipt.repository_id) is not int or receipt.repository_id < 1
                or not receipt.repository_url.startswith("https://github.com/")
                or receipt.repository_url.rstrip("/").lower()
                != f"https://github.com/{state.owner}/{state.name}"
                or not receipt.evidence_ref):
            raise InvalidEvidence("creation receipt mismatch")
        for _ in range(3):
            try:
                return self._save(state, phase="READ_INITIAL_HEAD", creation=receipt, reason=None)
            except StaleRevision:
                latest = self.consult(state.scope, state.request_id)
                if latest.attempt_id != state.attempt_id:
                    raise
                if latest.creation:
                    if latest.creation.repository_id != receipt.repository_id:
                        raise StaleRevision("conflicting receipts for the same attempt")
                    return latest
                if latest.phase != "CREATE_OUTCOME_PENDING":
                    raise
                state = latest
        raise StaleRevision("request changed while recording creation receipt")

    @staticmethod
    def _check_head(state: State, head: Head) -> None:
        if (head.repository_id != state.creation.repository_id
                or not head.branch or not _is_sha(head.sha) or not head.evidence_ref):
            raise InvalidEvidence("HEAD proof mismatch")


def _is_sha(value: str) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None
