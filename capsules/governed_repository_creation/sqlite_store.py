"""Private durable store for one host. All revisions and reservations are atomic."""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import asdict, replace
import json
import os
from pathlib import Path
import sqlite3

from .core import (
    Authorization, Bootstrap, Conflict, CreationReceipt, Head, NotFound,
    StaleRevision, State, Target,
)


def _decode(payload: str) -> State:
    values = json.loads(payload)
    for key, kind in (
        ("authorization", Authorization), ("bootstrap", Bootstrap),
        ("initial_head", Head), ("final_head", Head),
    ):
        if values[key] is not None:
            values[key] = kind(**values[key])
    if values["creation"] is not None:
        values["creation"]["target"] = Target(**values["creation"]["target"])
        values["creation"] = CreationReceipt(**values["creation"])
    return State(**values)


def _encode(state: State) -> str:
    return json.dumps(asdict(state), ensure_ascii=False, separators=(",", ":"))


class SQLiteStore:
    def __init__(self, path: str | Path):
        self.path = Path(path).resolve()
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            pass
        else:
            os.close(fd)
        with self._connection(write=True) as db:
            version = db.execute("PRAGMA user_version").fetchone()[0]
            if version not in (0, 1):
                raise ValueError("unsupported capsule database version")
            db.execute("""
                CREATE TABLE IF NOT EXISTS creation_requests (
                    request_id TEXT PRIMARY KEY,
                    scope TEXT NOT NULL,
                    request_key TEXT NOT NULL,
                    revision INTEGER NOT NULL,
                    reserved_target TEXT UNIQUE,
                    payload TEXT NOT NULL,
                    UNIQUE(scope, request_key)
                )
            """)
            if version == 0:
                db.execute("PRAGMA user_version = 1")

    @contextmanager
    def _connection(self, *, write=False):
        db = sqlite3.connect(self.path, timeout=5, isolation_level=None)
        try:
            if write:
                db.execute("PRAGMA synchronous = FULL")
                db.execute("BEGIN IMMEDIATE")
            yield db
            if write:
                db.commit()
        except BaseException:
            if write:
                db.rollback()
            raise
        finally:
            db.close()

    def submit(self, state: State) -> State:
        with self._connection(write=True) as db:
            row = db.execute(
                "SELECT payload FROM creation_requests WHERE scope = ? AND request_key = ?",
                (state.scope, state.key),
            ).fetchone()
            if row:
                existing = _decode(row[0])
                provided = {
                    field: getattr(state, field)
                    for field in ("continuity_id", "owner", "name", "visibility")
                    if getattr(state, field) is not None
                }
                if any(getattr(existing, field) != value for field, value in provided.items()):
                    raise Conflict("request key already has different or incomplete input; use resume for answers")
                return existing
            db.execute("INSERT INTO creation_requests VALUES (?, ?, ?, ?, NULL, ?)",
                       (state.request_id, state.scope, state.key, state.revision, _encode(state)))
            return state

    def get(self, scope: str, request_id: str) -> State:
        with self._connection() as db:
            row = db.execute(
                "SELECT payload FROM creation_requests WHERE scope = ? AND request_id = ?",
                (scope, request_id),
            ).fetchone()
            if row is None:
                raise NotFound("creation request not found")
            return _decode(row[0])

    def compare_and_save(self, previous: State, replacement: State) -> State:
        if replacement != replace(
            replacement, request_id=previous.request_id, scope=previous.scope,
            key=previous.key, continuity_id=previous.continuity_id, revision=previous.revision + 1,
        ):
            raise ValueError("request identity or revision changed")
        reservation = f"{replacement.owner}/{replacement.name}" if replacement.attempt_id else None
        with self._connection(write=True) as db:
            try:
                result = db.execute("""
                    UPDATE creation_requests SET revision = ?, reserved_target = ?, payload = ?
                    WHERE request_id = ? AND scope = ? AND revision = ?
                """, (replacement.revision, reservation, _encode(replacement),
                      previous.request_id, previous.scope, previous.revision))
            except sqlite3.IntegrityError as exc:
                raise Conflict("target already reserved by a governed request") from exc
            if result.rowcount != 1:
                raise StaleRevision("request revision changed")
            return replacement
