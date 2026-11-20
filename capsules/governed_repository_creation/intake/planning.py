"""Planning only. No GitHub, MCP, or execution hooks."""
from __future__ import annotations

from contextlib import closing, contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sqlite3
from uuid import uuid4

SOURCE = json.loads(Path(__file__).with_name("grt_catalogue.json").read_text(encoding="utf-8"))
OWNERS = ("chainsolutions-wealthtech", "Patricked-code", "Wealthtechinnovations")
BASE = (
    ("owner", "Quel compte GitHub doit posséder le dépôt ?", OWNERS),
    ("name", "Quel est le nom exact du futur dépôt ?", ()),
    ("visibility", "Quelle est la visibilité souhaitée ?", ("private", "public")),
    ("workflow_model", "Quel modèle de travail proposes-tu ?", tuple(SOURCE["workflow_models"])),
)
QUESTIONS = {field: {"field": field, "text": text, "choices": list(choices),
                     "group": "CRÉATION", "id": field, "required": True}
             for field, text, choices in BASE}
for field, text, limit in (
    ("project_mission", "Quelle est la mission du projet ?", 500),
    ("scope_in", "Qu'est-ce qui entre dans le périmètre ?", 500),
    ("scope_out", "Qu'est-ce qui reste hors périmètre ?", 500),
    ("architecture_notes", "Qu'est-ce qui est déjà connu de l'architecture ?", 500),
    ("first_work_objective", "Quel serait le premier travail concret après la remise ?", 500),
):
    QUESTIONS[field] = {"field": field, "text": text, "choices": [], "id": field,
                        "group": "CADRAGE", "required": False, "limit": limit}
for item in SOURCE["questions"]:
    if "CREATE_NEW_REPOSITORY" in item["applies_to"]:
        source = item["choice_source"]
        QUESTIONS[item["field"]] = {**item, "required": False,
                                    "choices": source.get("values", source.get("static_values", []))}


class IntakeError(Exception):
    pass


class BatchValidationError(IntakeError):
    """The lot is correctable at the submitted revision."""


CONDITIONS = {
    "mcp_transport": ("mcp_linkage", ("REUSE_EXISTING_BINDING", "CREATE_BINDING", "VERIFY_EXISTING_BINDING")),
    "mcp_scope": ("mcp_linkage", ("REUSE_EXISTING_BINDING", "CREATE_BINDING", "VERIFY_EXISTING_BINDING")),
    "production_server_selection": ("server_binding_mode", ("EXISTING_SINGLE", "EXISTING_MULTI", "NONE_PLAN_NEW")),
    "dns_tls_posture": ("domain_posture", ("REUSE_EXISTING", "CREATE_NEW", "REUSE_AND_ADD")),
}


def visible(question, answers):
    rule = CONDITIONS.get(question["field"])
    return rule is None or answers.get(rule[0]) in rule[1]


def validated_value(question, value, defer):
    if defer:
        if question["required"]:
            raise IntakeError("Ce choix est requis pour préparer la création.")
        return None
    if not isinstance(value, str):
        raise IntakeError("Format de réponse invalide.")
    if question["field"] == "name":
        if not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}", value) or value in {".", ".."}:
            raise IntakeError("Nom de dépôt invalide.")
    elif question.get("limit"):
        value = value.strip()
        if not value or len(value) > question["limit"] or any(ord(c) < 32 for c in value):
            raise IntakeError("Réponse texte invalide.")
    elif value not in question["choices"]:
        raise IntakeError("Choix non disponible.")
    return value


def next_question(answers):
    return next((q for q in QUESTIONS.values()
                 if q["field"] not in answers and visible(q, answers)), None)


def project(events):
    answers = {}
    for event in events:
        if event["kind"] == "ANSWER_RECORDED":
            answers[event["field"]] = event["value"]
        elif event["kind"] == "QUESTION_DEFERRED":
            answers[event["field"]] = None
    return answers


def preview(answers):
    answer = lambda field: answers.get(field)
    def group(key):
        return [e["path"] for e in SOURCE["entries"] if not e["source_only"] and e["category"] == key]
    return {
        "github": {k: answer(k) for k in ("owner", "name", "visibility")},
        "template": SOURCE["source_repository"],
        "source_sha": SOURCE["source_sha"],
        "model": answer("workflow_model"),
        "model_steps": SOURCE["workflow_models"].get(answer("workflow_model"), []),
        "delivery_intent": {k: answer(k) for k in ("ci_cd_posture", "deployment_strategy", "mcp_linkage")},
        "target_documents": {k: group(k) for k in ("generic_core", "project_state_templates",
                                                 "decision_and_architecture", "machine_governance",
                                                 "schemas", "coordination_docs")},
        "target_workflows": [p for p in group("automation") if p.startswith(".github/workflows/")],
        "source_only": [e["path"] for e in SOURCE["entries"] if e["source_only"]],
        "business_outline": {key: answer(key) for key in (
            "project_mission", "scope_in", "scope_out", "architecture_notes", "first_work_objective")},
        "workflow_decision": {
            "bootstrap": "REQUIRED_FOR_GRT_TEMPLATE",
            "work_model": answer("workflow_model"),
            "deployment": "EXCLUDED_FROM_PLAN" if answer("deployment_strategy") == "NO_DEPLOYMENT"
                          else "SEPARATE_PLAN_NOT_AUTHORIZED",
        },
        "github_only_route": answer("git_provider") in (None, "GITHUB"),
        "unresolved_answers": [key for key, value in answers.items() if value is None],
        "creation_authorized": False,
        "deployment_authorized": False,
        "governed_session_started": False,
    }


class IntakeJournal:
    """Private append-only event stream; authorization belongs to the host."""
    def __init__(self, path):
        self.path = Path(path).resolve()
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            pass
        else:
            os.close(fd)
        with self._write() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS intake_events(
                request_id TEXT NOT NULL, actor TEXT NOT NULL, revision INTEGER NOT NULL,
                data TEXT NOT NULL, PRIMARY KEY(request_id, revision))""")

    @contextmanager
    def _write(self):
        with closing(sqlite3.connect(self.path, timeout=5)) as db:
            db.execute("PRAGMA synchronous=FULL")
            db.execute("BEGIN IMMEDIATE")
            with db:
                yield db

    def _append(self, db, actor, request_id, revision, kind, **data):
        event = {"revision": revision, "kind": kind,
                 "recorded_at": datetime.now(timezone.utc).isoformat(), **data}
        db.execute("INSERT INTO intake_events VALUES (?,?,?,?)",
                   (request_id, actor, revision, json.dumps(event, ensure_ascii=False)))

    def start(self, actor):
        request_id = str(uuid4())
        with self._write() as db:
            self._append(db, actor, request_id, 1, "REQUEST_OPENED", catalogue_sha=SOURCE["catalogue_git_sha"],
                         source_sha=SOURCE["source_sha"], workflow_sha=SOURCE["workflow_model_git_sha"])
        return request_id

    def _load(self, db, actor, request_id):
        events = [json.loads(row[0]) for row in db.execute(
            "SELECT data FROM intake_events WHERE actor=? AND request_id=? ORDER BY revision",
            (actor, request_id),
        )]
        if not events:
            raise IntakeError("Demande introuvable.")
        if (events[0]["catalogue_sha"] != SOURCE["catalogue_git_sha"]
                or events[0]["source_sha"] != SOURCE["source_sha"]
                or events[0]["workflow_sha"] != SOURCE["workflow_model_git_sha"]):
            raise IntakeError("Révision du catalogue différente, réconciliation nécessaire.")
        return events

    def get(self, actor, request_id):
        with closing(sqlite3.connect(self.path, timeout=5)) as db:
            return self._load(db, actor, request_id)

    def recent(self, actor):
        with closing(sqlite3.connect(self.path, timeout=5)) as db:
            return [row[0] for row in db.execute(
                "SELECT request_id FROM intake_events WHERE actor=? AND revision=1 ORDER BY rowid DESC LIMIT 30",
                (actor,),
            )]

    def _append_answer(self, db, actor, request_id, revision, question, value):
        data = {"field": question["field"], "question_id": question["id"]}
        if value is None:
            self._append(db, actor, request_id, revision, "QUESTION_DEFERRED", **data)
        else:
            self._append(db, actor, request_id, revision, "ANSWER_RECORDED", value=value, **data)

    def answer(self, actor, request_id, revision, field, value, defer=False):
        with self._write() as db:
            events = self._load(db, actor, request_id)
            if revision != events[-1]["revision"]:
                raise IntakeError("La demande a changé. Rouvre-la avant de répondre.")
            answers = project(events)
            q = next_question(answers)
            if not q or field != q["field"]:
                raise IntakeError("Cette question n'est pas celle attendue.")
            answers[field] = validated_value(q, value, defer)
            self._append_answer(db, actor, request_id, revision + 1, q, answers[field])
            if next_question(answers) is None:
                self._append(db, actor, request_id, revision + 2, "PREPARATION_COMPLETE")

    def answer_batch(self, actor, request_id, revision, submitted):
        """Commit one lot against the current revision, with the same answer events as the step-by-step flow."""
        with self._write() as db:
            events = self._load(db, actor, request_id)
            if revision != events[-1]["revision"]:
                raise IntakeError("La demande a changé. Rouvre-la avant d’envoyer le lot.")
            answers = project(events)
            if next_question(answers) is None:
                raise IntakeError("La préparation est déjà terminée.")
            if set(submitted) - QUESTIONS.keys():
                raise BatchValidationError("Le lot contient une question inconnue.")
            if set(submitted) & answers.keys():
                raise BatchValidationError("Le lot contient une réponse déjà enregistrée.")
            pending = []
            while question := next_question(answers):
                field = question["field"]
                value = submitted.get(field)
                try:
                    answers[field] = validated_value(question, value, defer=value in (None, ""))
                except IntakeError as exc:
                    raise BatchValidationError(f'{question["text"]} {exc}') from exc
                pending.append((question, answers[field]))
            for offset, (question, value) in enumerate(pending, start=1):
                self._append_answer(db, actor, request_id, revision + offset, question, value)
            self._append(db, actor, request_id, revision + len(pending) + 1, "PREPARATION_COMPLETE")

    def record_preflight(self, actor, request_id, revision, digest, result):
        """Internal write path for the trusted preflight service only."""
        with self._write() as db:
            events = self._load(db, actor, request_id)
            if events[-1]["revision"] != revision:
                raise IntakeError("La demande a changé pendant le préflight. Relance le contrôle.")
            self._append(db, actor, request_id, revision + 1, "CUG_PREFLIGHT_RECORDED",
                         prepared_revision=revision, dossier_sha256=digest, result=result)
            return self._load(db, actor, request_id)[-1]
