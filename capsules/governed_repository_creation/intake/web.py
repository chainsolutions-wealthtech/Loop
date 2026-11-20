"""Local-only preview of the intake. No credentials or execution endpoints."""
from __future__ import annotations

import argparse
from html import escape
import hashlib
import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
from secrets import token_urlsafe
from urllib.parse import parse_qs, urlsplit

from .preflight import GitHubActor
from .planning import (
    BatchValidationError, IntakeError, IntakeJournal, QUESTIONS, SOURCE, next_question, preview, project,
)
from .web_batch import ASSET, batch_body

ACTOR = "local-preview"
REQUEST = re.compile(r"/requests/([0-9a-f-]{36})(/batch)?")
BATCH_MAX_BYTES = 48 * 1024
LABELS = {
    "STANDARD_GOVERNED_FLOW": "Standard gouverné",
    "REGULATORY_AFRICAFUNDS_GOVERNED_FLOW": "Renforcé, issu de Regulatory / AfricaFunds",
    "private": "Privé", "public": "Public", "NO_MCP": "Sans MCP",
    "DECIDE_LATER": "Décider plus tard", "UNKNOWN_DISCOVER": "À observer",
}
STYLE = """
:root{font-family:system-ui,sans-serif;color:#152538;background:#f3f6f8}
main{max-width:52rem;margin:2rem auto;padding:0 1rem}
section,details{background:#fff;border:1px solid #dbe3ea;border-radius:.6rem;padding:1rem;margin:1rem 0}
h1,h2{line-height:1.15}button,input,select{font:inherit;padding:.55rem;max-width:100%}
button{background:#174c60;color:white;border:0;border-radius:.3rem;margin:.6rem .35rem 0 0}
label,summary{font-weight:650}code,li{overflow-wrap:anywhere}small{color:#465970}
a{color:#075166}pre{white-space:pre-wrap;overflow-wrap:anywhere}
.batch-question{margin:1rem 0}
.batch-question input,.batch-question select{box-sizing:border-box;width:min(100%,32rem)}
.batch-question select:disabled{background:#edf1f4;color:#526474}
.batch-question.inactive label{color:#526474}
.batch-error{color:#812522}
"""


def esc(value):
    return escape(str(value), quote=True)


def document(title, body):
    return (
        '<!doctype html><html lang="fr"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{esc(title)}</title><style>{STYLE}</style><main>'
        f'<p><a href="/">Registre des demandes</a></p><h1>{esc(title)}</h1>{body}</main></html>'
    )


def fields(csrf, **values):
    return "".join(f'<input type="hidden" name="{esc(key)}" value="{esc(value)}">'
                   for key, value in {"csrf": csrf, **values}.items())


def human(value):
    if value is None:
        return "Reporté"
    return LABELS.get(value, str(value).replace("_", " "))


def page(events, request_id, csrf, preflight_enabled=False):
    answers = project(events)
    question = next_question(answers)
    if question:
        if question["choices"]:
            options = "".join(f'<option value="{esc(v)}">{esc(human(v))}</option>'
                              for v in question["choices"])
            control = f'<select id="value" name="value"><option value="">Sélectionner…</option>{options}</select>'
        else:
            control = (f'<input id="value" name="value" maxlength="{question.get("limit", 100)}" '
                       'autocomplete="off">')
        defer = '' if question["required"] else '<button name="command" value="defer">Reporter</button>'
        status = (
            f'<section><small>{esc(question["group"])} · {esc(question["id"])}</small>'
            f'<h2>Question suivante</h2>'
            f'<p><a href="/requests/{esc(request_id)}/batch">Ouvrir le questionnaire groupé</a></p>'
            f'<form method="post" action="/requests/{esc(request_id)}">'
            + fields(csrf, revision=events[-1]["revision"], field=question["field"])
            + f'<p><label for="value">{esc(question["text"])}</label></p>{control}'
            + '<p><button name="command" value="answer">Enregistrer et continuer</button>'
            + f'{defer}</p></form></section>'
        )
    else:
        status = '<section><h2>Préparation terminée</h2><p>Plan consultable. Aucune session d’exécution ouverte.</p></section>'
        if preflight_enabled:
            status += (
                f'<form method="post" action="/requests/{esc(request_id)}">'
                + fields(csrf, revision=events[-1]["revision"])
                + '<button name="command" value="preflight">Vérifier avec CUG</button></form>'
            )
    plan = preview(answers)
    evidence = next((e for e in reversed(events) if e["kind"] == "CUG_PREFLIGHT_RECORDED"), None)
    if evidence:
        status += '<details open><summary>Dernier préflight CUG</summary><pre>' + esc(
            json.dumps(evidence, indent=2, ensure_ascii=False)) + '</pre></details>'
    history = "".join(
        f'<li>{esc(e["recorded_at"])} · r{esc(e["revision"])} · {esc(e["kind"])}'
        + (f' · {esc(e["question_id"])} — {esc(human(e.get("value")))}' if "question_id" in e else "") + '</li>'
        for e in events
    )
    return document("Préparer un dépôt gouverné",
                    f'<p>Demande <code>{esc(request_id)}</code> · {len(events)} événements</p>'
                    '<p>Aperçu local. Aucun dépôt ni déploiement n’est déclenché. Ne saisis aucun secret.</p>'
                    + status + '<details open><summary>Historique</summary><ol>' + history + '</ol></details>'
                    + '<details><summary>Plan documentaire et workflows issus de GRT</summary><pre>'
                    + esc(json.dumps(plan, indent=2, ensure_ascii=False)) + '</pre></details>')


def make_server(journal, port=0, *, resolve_actor=None, preflight=None):
    """Loopback server. An optional trusted host supplies verified actor context."""
    if preflight is not None and resolve_actor is None:
        raise ValueError("preflight requires an authenticated actor resolver")
    csrf_secret = token_urlsafe(32).encode()
    batch_script = Path(__file__).with_name("intake-batch.js").read_bytes()

    def csrf_for(key):
        return hmac.new(csrf_secret, key.encode(), hashlib.sha256).hexdigest()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send_content(self, data, content_type, status=200, *, batch=False):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy",
                             "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'"
                             + ("; script-src 'self'" if batch else ""))
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def send_page(self, text, status=200, *, batch=False):
            self.send_content(text.encode("utf-8"), "text/html; charset=utf-8", status, batch=batch)

        def send_batch(self, events, request_id, csrf, status=200, **correction):
            hidden = fields(csrf, revision=events[-1]["revision"])
            body = batch_body(events, request_id, hidden, human, **correction)
            self.send_page(document("Questionnaire groupé", body), status, batch=True)

        def redirect_request(self, request_id):
            self.send_response(303)
            self.send_header("Location", f"/requests/{request_id}")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()

        def check_host(self):
            host = self.headers.get("Host", "")
            expected = self.server.server_port
            return host in {f"127.0.0.1:{expected}", f"localhost:{expected}"}

        def actor_context(self):
            if resolve_actor is None:
                return ACTOR, None
            try:
                actor = resolve_actor(self)
            except IntakeError:
                actor = None
            if not isinstance(actor, GitHubActor):
                self.send_error(401)
                return None
            return actor.journal_key, actor

        def do_GET(self):
            if not self.check_host():
                self.send_error(403)
                return
            context = self.actor_context()
            if context is None:
                return
            key, actor = context
            csrf = csrf_for(key)
            path = urlsplit(self.path).path
            if path == "/":
                links = "".join(f'<li><a href="/requests/{esc(r)}">{esc(r)}</a></li>'
                                for r in journal.recent(key))
                self.send_page(document("Registre des demandes",
                    '<p>Préparer un dépôt à partir de GRT et reprendre les réponses enregistrées.</p>'
                    '<form method="post" action="/requests">' + fields(csrf)
                    + '<button>Ouvrir une demande</button></form><h2>Demandes récentes</h2><ul>'
                    + links + f'</ul><small>Catalogue GRT {esc(SOURCE["manifest_version"])}</small>'))
                return
            if path == ASSET:
                self.send_content(batch_script, "text/javascript; charset=utf-8")
                return
            match = REQUEST.fullmatch(path)
            if not match:
                self.send_error(404)
                return
            try:
                events = journal.get(key, match[1])
                if match[2]:
                    if next_question(project(events)) is None:
                        self.redirect_request(match[1])
                    else:
                        self.send_batch(events, match[1], csrf)
                else:
                    self.send_page(page(events, match[1], csrf,
                                        preflight_enabled=preflight is not None and actor is not None))
            except IntakeError as exc:
                self.send_page(document("Reprise indisponible", f'<p>{esc(exc)}</p>'), 409)

        def do_POST(self):
            if not self.check_host():
                self.send_error(403)
                return
            context = self.actor_context()
            if context is None:
                return
            key, actor = context
            csrf = csrf_for(key)
            path = urlsplit(self.path).path
            match = REQUEST.fullmatch(path)
            batch = bool(match and match[2])
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if (not 0 < size <= (BATCH_MAX_BYTES if batch else 4096)
                        or self.headers.get_content_type() != "application/x-www-form-urlencoded"):
                    raise ValueError
                form = parse_qs(self.rfile.read(size).decode(), keep_blank_values=True,
                                max_num_fields=len(QUESTIONS) + 2 if batch else 8,
                                errors="strict" if batch else "replace")
                if any(len(items) != 1 for items in form.values()):
                    raise ValueError
                values = {key: items[0] for key, items in form.items()}
                if not hmac.compare_digest(values.get("csrf", "").encode(), csrf.encode()):
                    self.send_error(403)
                    return
                if path == "/requests":
                    request_id = journal.start(key)
                else:
                    if not match:
                        raise ValueError
                    request_id = match[1]
                    revision = int(values["revision"])
                    command = values.get("command")
                    if batch:
                        submitted = {k: v for k, v in values.items() if k not in {"csrf", "revision"}}
                        try:
                            journal.answer_batch(key, request_id, revision, submitted)
                        except BatchValidationError as exc:
                            events = journal.get(key, request_id)
                            if events[-1]["revision"] != revision:
                                raise IntakeError("La demande a changé. Rouvre-la avant d’envoyer le lot.") from exc
                            self.send_batch(events, request_id, csrf, 422, submitted=submitted, error=exc)
                            return
                    elif command == "preflight" and preflight is not None and actor is not None:
                        preflight.run(actor, request_id, revision)
                    elif command in {"answer", "defer"}:
                        journal.answer(key, request_id, revision, values["field"],
                                       values.get("value", ""), defer=command == "defer")
                    else:
                        raise ValueError
            except (KeyError, ValueError, UnicodeError):
                self.send_error(400)
                return
            except IntakeError as exc:
                self.send_page(document("Réponse non enregistrée", f'<p>{esc(exc)}</p>'), 409)
                return
            self.redirect_request(request_id)

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True, help="Private SQLite file outside the Git checkout")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    with make_server(IntakeJournal(args.db), args.port) as server:
        print(f"http://127.0.0.1:{server.server_port}", flush=True)
        server.serve_forever()


if __name__ == "__main__":
    main()
