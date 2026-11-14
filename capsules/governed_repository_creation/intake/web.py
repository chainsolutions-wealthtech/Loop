"""Local-only preview of the intake. No credentials or execution endpoints."""
from __future__ import annotations

import argparse
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import re
from secrets import token_urlsafe
from urllib.parse import parse_qs, urlsplit

from .planning import IntakeError, IntakeJournal, SOURCE, next_question, preview, project

ACTOR = "local-preview"
REQUEST = re.compile(r"/requests/([0-9a-f-]{36})")
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


def page(events, request_id, csrf):
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
            f'<h2>Question suivante</h2><form method="post" action="/requests/{esc(request_id)}">'
            + fields(csrf, revision=events[-1]["revision"], field=question["field"])
            + f'<p><label for="value">{esc(question["text"])}</label></p>{control}'
            + '<p><button name="command" value="answer">Enregistrer et continuer</button>'
            + f'{defer}</p></form></section>'
        )
    else:
        status = '<section><h2>Préparation terminée</h2><p>Plan consultable. Aucune session d’exécution ouverte.</p></section>'
    plan = preview(answers)
    history = "".join(
        f'<li>{esc(e["recorded_at"])} · r{esc(e["revision"])} · {esc(e["kind"])}'
        + (f' · {esc(e["question_id"])} — {esc(human(e.get("value")))}' if "question_id" in e else "") + '</li>'
        for e in events
    )
    return document("Préparer un dépôt gouverné",
                    f'<p>Demande <code>{esc(request_id)}</code> · {len(events)} événements</p>'
                    '<p>Aperçu local. Aucun dépôt, déploiement ou accès externe n’est déclenché. Ne saisis aucun secret.</p>'
                    + status + '<details open><summary>Historique</summary><ol>' + history + '</ol></details>'
                    + '<details><summary>Plan documentaire et workflows issus de GRT</summary><pre>'
                    + esc(json.dumps(plan, indent=2, ensure_ascii=False)) + '</pre></details>')


def make_server(journal, port=0):
    csrf = token_urlsafe(32)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send_page(self, text, status=200):
            data = text.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Security-Policy",
                             "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def check_host(self):
            host = self.headers.get("Host", "")
            expected = self.server.server_port
            return host in {f"127.0.0.1:{expected}", f"localhost:{expected}"}

        def do_GET(self):
            if not self.check_host():
                self.send_error(403)
                return
            path = urlsplit(self.path).path
            if path == "/":
                links = "".join(f'<li><a href="/requests/{esc(r)}">{esc(r)}</a></li>'
                                for r in journal.recent(ACTOR))
                self.send_page(document("Registre des demandes",
                    '<p>Préparer un dépôt à partir de GRT et reprendre les réponses enregistrées.</p>'
                    '<form method="post" action="/requests">' + fields(csrf)
                    + '<button>Ouvrir une demande</button></form><h2>Demandes récentes</h2><ul>'
                    + links + f'</ul><small>Catalogue GRT {esc(SOURCE["manifest_version"])}</small>'))
                return
            match = REQUEST.fullmatch(path)
            if not match:
                self.send_error(404)
                return
            try:
                self.send_page(page(journal.get(ACTOR, match[1]), match[1], csrf))
            except IntakeError as exc:
                self.send_page(document("Reprise indisponible", f'<p>{esc(exc)}</p>'), 409)

        def do_POST(self):
            if not self.check_host():
                self.send_error(403)
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 4096 or self.headers.get_content_type() != "application/x-www-form-urlencoded":
                    raise ValueError
                form = parse_qs(self.rfile.read(size).decode(), keep_blank_values=True, max_num_fields=8)
                if any(len(items) != 1 for items in form.values()):
                    raise ValueError
                values = {key: items[0] for key, items in form.items()}
                if values.get("csrf") != csrf:
                    self.send_error(403)
                    return
                path = urlsplit(self.path).path
                if path == "/requests":
                    request_id = journal.start(ACTOR)
                else:
                    match = REQUEST.fullmatch(path)
                    if not match or values.get("command") not in {"answer", "defer"}:
                        raise ValueError
                    request_id = match[1]
                    journal.answer(ACTOR, request_id, int(values["revision"]), values["field"],
                                   values.get("value", ""), defer=values["command"] == "defer")
            except (KeyError, ValueError, UnicodeError):
                self.send_error(400)
                return
            except IntakeError as exc:
                self.send_page(document("Réponse non enregistrée", f'<p>{esc(exc)}</p>'), 409)
                return
            self.send_response(303)
            self.send_header("Location", f"/requests/{request_id}")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()

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
