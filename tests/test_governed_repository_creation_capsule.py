from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Barrier
import unittest

from capsules.governed_repository_creation import (
    Authorization, Bootstrap, BootstrapFailed, Capsule, Conflict, CreationReceipt,
    GatewayUnavailable, Head, NotFound, Observation, SQLiteStore, StaleRevision,
)


class FakeGateway:
    def __init__(self):
        self.authority = Authorization("d" * 40, "auth-fixture")
        self.observation = Observation("absent", "absence-fixture")
        self.posts = 0
        self.recovery_calls = 0
        self.raise_during_create = None
        self.attempt = None
        self.recovered = None
        self.head = None
        self.proof = None

    def authorize_create(self, state):
        return self.authority

    def observe_target(self, target):
        return self.observation

    def create_once(self, intent):
        self.posts += 1
        self.attempt = intent
        if self.raise_during_create:
            raise self.raise_during_create
        return self.receipt(intent)

    def receipt(self, intent):
        return CreationReceipt(intent.attempt_id, intent.target, 42,
                               f"https://github.com/{intent.owner}/{intent.name}", "creation-fixture")

    def recover_creation(self, intent):
        self.recovery_calls += 1
        return self.recovered

    def read_head(self, creation):
        return self.head

    def read_bootstrap(self, creation, authorization):
        if isinstance(self.proof, Exception):
            raise self.proof
        return self.proof


class GovernedCreationTest(unittest.TestCase):
    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / "private.sqlite"
        self.gateway = FakeGateway()
        self.capsule = Capsule(SQLiteStore(self.path), self.gateway)

    def submit(self, key="request-key", scope="authorized-caller"):
        return self.capsule.submit(scope, key, owner="Example", name="Capsule",
                                   visibility="private", continuity_id="continuity-fixture")

    def step(self, state, **answers):
        return self.capsule.resume(state.scope, state.request_id, state.revision, **answers)

    def through_bootstrap(self):
        state = self.step(self.submit())
        self.gateway.head = Head(42, "main", "a" * 40, "initial-head")
        state = self.step(state)
        self.gateway.proof = Bootstrap(42, "d" * 40, "b" * 40, "bootstrap-run")
        return self.step(state)

    def test_qualified_create_initial_head_delay_and_handoff_replay(self):
        state = self.step(self.submit())
        self.assertEqual(self.capsule.consult(state.scope, state.request_id).creation.repository_id, 42)
        state = self.step(state)
        self.assertEqual(state.reason, "INITIAL_HEAD_NOT_AVAILABLE")
        self.gateway.head = Head(42, "main", "a" * 40, "initial-head")
        state = self.step(state)
        self.assertEqual(self.step(state).reason, "BOOTSTRAP_NOT_ATTESTED")
        state = self.capsule.consult(state.scope, state.request_id)
        self.gateway.proof = Bootstrap(42, "d" * 40, "b" * 40, "bootstrap-run")
        state = self.step(state)
        self.gateway.head = Head(42, "main", "b" * 40, "final-head")
        ready = self.step(state)
        self.assertEqual(ready.phase, "HANDOFF_READY")
        self.assertEqual(ready.next_action, "DISCOVER_PROJECT_BASELINE")
        self.assertEqual(json.loads(json.dumps(ready.handoff))["bootstrap"]["run_ref"], "bootstrap-run")
        self.assertEqual(ready.handoff["initial_observed_head_sha"], "a" * 40)
        self.assertEqual(ready.handoff["head_sha"], "b" * 40)
        self.assertEqual(ready.handoff["continuity_id"], "continuity-fixture")
        self.capsule = Capsule(SQLiteStore(self.path), self.gateway)
        self.assertEqual(self.step(self.submit()), ready)
        self.assertEqual(self.gateway.posts, 1)

    def test_inflight_reconciliation_does_not_lose_a_later_create_receipt(self):
        def create_with_readback_race(intent):
            observed = self.step(intent)
            self.assertEqual(observed.reason, "CREATION_NOT_CORRELATED")
            return self.gateway.receipt(intent)

        self.gateway.create_once = create_with_readback_race
        state = self.step(self.submit())
        self.assertEqual(state.creation.repository_id, 42)
        self.assertEqual(state.phase, "READ_INITIAL_HEAD")

    def test_timeout_and_restart_never_send_a_second_create(self):
        self.gateway.raise_during_create = GatewayUnavailable()
        pending = self.step(self.submit())
        self.assertEqual((pending.phase, pending.reason), ("CREATE_OUTCOME_PENDING", "CREATION_OUTCOME_UNKNOWN"))
        self.capsule = Capsule(SQLiteStore(self.path), self.gateway)
        pending = self.step(pending)
        self.assertEqual(pending.reason, "CREATION_NOT_CORRELATED")
        self.gateway.recovered = self.gateway.receipt(self.gateway.attempt)
        recovered = self.step(pending)
        self.assertEqual(recovered.creation.repository_id, 42)
        self.assertEqual(self.gateway.posts, 1)

    def test_crash_after_intent_commit_does_not_reissue_create(self):
        class SimulatedCrash(BaseException):
            pass
        self.gateway.raise_during_create = SimulatedCrash()
        state = self.submit()
        with self.assertRaises(SimulatedCrash):
            self.step(state)
        self.capsule = Capsule(SQLiteStore(self.path), self.gateway)
        pending = self.capsule.consult(state.scope, state.request_id)
        self.assertEqual(pending.phase, "CREATE_OUTCOME_PENDING")
        self.assertEqual(self.step(pending).reason, "CREATION_NOT_CORRELATED")
        self.assertEqual(self.gateway.posts, 1)

    def test_incorrect_correlation_is_not_accepted(self):
        self.gateway.raise_during_create = GatewayUnavailable()
        pending = self.step(self.submit())
        self.gateway.recovered = replace(self.gateway.receipt(self.gateway.attempt), attempt_id="another-request")
        state = self.step(pending)
        self.assertEqual(state.reason, "EVIDENCE_CONFLICT")
        self.assertIsNone(state.creation)
        self.assertEqual(self.gateway.posts, 1)

    def test_target_presence_and_unknown_404_never_create(self):
        state = self.submit()
        self.gateway.observation = Observation("unknown")
        state = self.step(state)
        self.assertEqual(state.reason, "TARGET_ABSENCE_NOT_VERIFIED")
        self.gateway.observation = Observation("present", "same-template-is-not-correlation", 7)
        self.assertEqual(self.step(state).reason, "TARGET_ALREADY_EXISTS")
        self.assertEqual(self.gateway.posts, 0)

    def test_scope_idempotency_and_stale_revision(self):
        state = self.capsule.submit("scope", "key")
        self.assertEqual(state.missing, ("owner", "name", "visibility"))
        completed = self.step(state, owner="example", name="capsule", visibility="public")
        self.assertEqual(self.capsule.submit("scope", "key"), completed)
        with self.assertRaises(Conflict):
            self.capsule.submit("scope", "key", owner="different")
        with self.assertRaises(NotFound):
            self.capsule.consult("other", state.request_id)
        with self.assertRaises(StaleRevision):
            self.step(state)
        self.assertEqual(self.gateway.posts, 0)

    def test_missing_authority_never_creates(self):
        self.gateway.authority = None
        self.assertEqual(self.step(self.submit()).reason, "AUTHORITY_NOT_VERIFIED")
        self.assertEqual(self.gateway.posts, 0)

    def test_final_head_divergence_and_wrong_repository_block_handoff(self):
        state = self.through_bootstrap()
        self.gateway.head = Head(11, "main", "b" * 40, "wrong-repository")
        state = self.step(state)
        self.assertEqual(state.reason, "EVIDENCE_CONFLICT")
        self.gateway.head = Head(42, "main", "c" * 40, "diverged-head")
        state = self.step(state)
        self.assertEqual(state.reason, "HEAD_DIVERGED")
        self.assertIsNone(state.handoff)
        self.assertEqual(self.gateway.posts, 1)

    def test_bootstrap_failure_and_wrong_template_do_not_advance(self):
        state = self.step(self.submit())
        self.gateway.head = Head(42, "main", "a" * 40, "initial-head")
        state = self.step(state)
        self.gateway.proof = BootstrapFailed()
        state = self.step(state)
        self.assertEqual(state.reason, "BOOTSTRAP_FAILED")
        self.gateway.proof = Bootstrap(42, "e" * 40, "b" * 40, "foreign-run")
        state = self.step(state)
        self.assertEqual(state.reason, "EVIDENCE_CONFLICT")
        self.assertEqual(state.phase, "VERIFY_BOOTSTRAP")

    def _race(self, states):
        barrier = Barrier(2)
        self.gateway.observe_target = lambda target: (
            barrier.wait(timeout=5), Observation("absent", "absence-fixture")
        )[1]

        def attempt(state):
            try:
                return self.step(state)
            except Conflict as exc:
                return exc

        with ThreadPoolExecutor(max_workers=2) as pool:
            return list(pool.map(attempt, states))

    def test_concurrent_same_request_only_one_create(self):
        state = self.submit()
        results = self._race([state, state])
        self.assertEqual(sum(isinstance(r, StaleRevision) for r in results), 1)
        self.assertEqual(self.gateway.posts, 1)

    def test_concurrent_distinct_requests_cannot_reserve_same_target(self):
        results = self._race([self.submit(), self.submit(key="other", scope="other")])
        self.assertEqual(sum(isinstance(r, Conflict) for r in results), 1)
        self.assertEqual(self.gateway.posts, 1)
