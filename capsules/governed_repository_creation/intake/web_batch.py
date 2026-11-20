"""Grouped presentation of the same intake catalogue and journal."""
from html import escape
import json

from .planning import CONDITIONS, QUESTIONS, project

ASSET = "/assets/intake-batch.js"
GROUP_LABELS = {
    "IDENTITY_TOPOLOGY": "Identité et organisation",
    "GOVERNANCE_POSTURE": "Gouvernance et environnements",
    "INFRASTRUCTURE": "Hébergement",
    "DOMAIN_NETWORK": "Domaine et réseau",
    "RUNTIME_DATA": "Données et intégrations",
    "DELIVERY_OPERATIONS": "Livraison et exploitation",
    "MCP_ACCESS": "Rattachement MCP",
    "AUTHORITY_SECURITY": "Accès et sécurité",
    "QUALITY_RECOVERY": "Tests et reprise",
}
# Suggestions éditoriales, jamais présélectionnées ni traitées comme des faits.
TEXT_SUGGESTIONS = {
    "project_mission": ("Valider un parcours de création gouvernée", "Concevoir une application web"),
    "scope_in": ("Cadrage, documentation et tests", "Dépôt, application et intégrations"),
    "scope_out": ("Aucun déploiement dans ce premier lot", "Aucune donnée ni écriture externe"),
    "architecture_notes": ("Architecture à définir pendant le cadrage",
                           "Séparer interface, logique métier et stockage"),
    "first_work_objective": ("Définir le périmètre et les critères d’acceptation",
                             "Vérifier le squelette documentaire et les tests"),
}


def esc(value):
    return escape(str(value), quote=True)


def question_row(question, saved, submitted, human):
    field = question["field"]
    value = submitted.get(field, "")
    condition = CONDITIONS.get(field)
    attributes, hint = "", ""
    if condition:
        parent, matches = condition
        attributes = (f' data-depends-on="{esc(parent)}" data-applies-when="{esc(json.dumps(matches))}"'
                      f' data-saved-parent="{esc(saved.get(parent) or "")}"')
        hint = "<br><small>Si la réponse précédente est " + esc(", ".join(map(human, matches))) + ".</small>"
    required = " required" if question["required"] else ""
    if question["choices"]:
        placeholder = "Sélectionner…" if required else "Reporter"
        options = []
        for choice in question["choices"]:
            selected = " selected" if value == choice else ""
            options.append(f'<option value="{esc(choice)}"{selected}>{esc(human(choice))}</option>')
        control = (f'<select id="{esc(field)}" name="{esc(field)}"{required}>'
                   f'<option value="">{placeholder}</option>{"".join(options)}</select>')
    else:
        suggestions = TEXT_SUGGESTIONS.get(field, ())
        picker, datalist = "", ""
        if suggestions:
            picker = f' list="{esc(field)}-suggestions"'
            datalist = (f'<datalist id="{esc(field)}-suggestions">'
                        + "".join(f'<option value="{esc(item)}"></option>' for item in suggestions) + "</datalist>")
        placeholder = "" if required else ' placeholder="Vide = reporté"'
        control = (f'<input id="{esc(field)}" name="{esc(field)}" maxlength="{question.get("limit", 100)}" '
                   f'value="{esc(value)}" autocomplete="off"{picker}{placeholder}{required}>' + datalist)
    return f'<div class="batch-question"{attributes}><label for="{esc(field)}">{esc(question["text"])}</label>{hint}<br>{control}</div>'


def batch_body(events, request_id, hidden_fields, human, *, submitted=None, error=None):
    saved = project(events)
    submitted = {} if submitted is None else submitted
    request_path = f"/requests/{esc(request_id)}"
    groups = {}
    for field, question in QUESTIONS.items():
        if field not in saved:
            groups.setdefault(question["group"], []).append(question_row(question, saved, submitted, human))
    recorded = ""
    if saved:
        recorded = '<details open><summary>Réponses déjà enregistrées</summary><ul>' + "".join(
            f'<li>{esc(QUESTIONS[field]["text"])} <strong>{esc(human(value))}</strong></li>'
            for field, value in saved.items()
        ) + "</ul></details>"
    return (
        f'<p><a href="{request_path}">Revenir au parcours question par question</a></p>'
        '<p>Sélectionne les réponses applicables et envoie-les ensemble. Une réponse facultative vide '
        'est reportée. Les questions qui ne s’appliquent pas ne sont pas enregistrées.</p>'
        '<p>Ne saisis aucun secret. L’envoi ne lance ni création de dépôt, ni rattachement, ni déploiement.</p>'
        + (f'<p role="alert" class="batch-error"><strong>{esc(error)}</strong></p>' if error else "")
        + recorded
        + f'<form id="intake-batch" method="post" action="{request_path}/batch">'
        + hidden_fields
        + "".join(f'<section><h2>{esc(GROUP_LABELS.get(group, group))}</h2>{"".join(rows)}</section>'
                  for group, rows in groups.items())
        + '<button type="submit">Envoyer toutes les réponses</button></form>'
        + f'<script src="{ASSET}" defer></script>'
    )
