"""Bridge an authenticated intake to CUG observation, never to execution."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re

from ..adapters.github_app_preflight import APIError, PreflightError, inspect_app
from .planning import IntakeError, SOURCE, next_question, project

CUG_APP_ID = 5417646
SAFE_REPORT = (
    "status", "app_id", "installation_id", "owner", "owner_id", "owner_type",
    "repository_selection", "target", "visibility_requested", "target_observation",
    "target_repository_id", "template", "template_repository_id", "template_head_sha",
    "template_private", "template_same_installation_verified",
    "installation_creation_permissions_declared", "creation_authorized",
)
FIXED_FAILURES = {
    "APP_CREDENTIAL_NOT_CONFIGURED", "APP_JWT_SIGNING_FAILED", "UNEXPECTED_APP_IDENTITY",
    "INSTALLATION_NOT_VERIFIED_FOR_OWNER", "INSTALLATION_PERMISSIONS_UNVERIFIED",
    "INSTALLATION_TOKEN_UNVERIFIED", "PREFLIGHT_TOKEN_NOT_READ_ONLY",
    "TEMPLATE_IDENTITY_UNVERIFIED", "TEMPLATE_HEAD_DIFFERS_FROM_REQUEST",
    "TEMPLATE_BRANCH_UNVERIFIED", "TEMPLATE_VISIBILITY_UNVERIFIED",
    "TARGET_IDENTITY_UNVERIFIED", "PREFLIGHT_TOKEN_REVOCATION_UNCONFIRMED",
}
KNOWN_FAILURE = re.compile(
    r"(?:APP_IDENTITY|INSTALLATION|INSTALLATION_TOKEN|TEMPLATE_METADATA|TEMPLATE_HEAD|"
    r"TEMPLATE_INSTALLATION|TARGET_OBSERVATION)_HTTP_[1-5][0-9]{2}"
)


@dataclass(frozen=True)
class GitHubActor:
    user_id: int

    def __post_init__(self):
        if type(self.user_id) is not int or self.user_id <= 0:
            raise ValueError("invalid verified GitHub user ID")

    @property
    def journal_key(self):
        return f"github:{self.user_id}"


def verify_user(api, user_token):
    """Only call with a GitHub user token obtained by the trusted host."""
    if not user_token:
        raise IntakeError("Connexion GitHub requise.")
    try:
        result = api("GET", "/user", user_token)
    except (APIError, PreflightError):
        raise IntakeError("Identité GitHub non vérifiée.") from None
    if not isinstance(result, dict) or str(result.get("type", "")) != "User":
        raise IntakeError("Une identité GitHub utilisateur est requise.")
    try:
        return GitHubActor(result.get("id"))
    except ValueError:
        raise IntakeError("Identité GitHub non vérifiée.") from None


def dossier(events):
    answers = project(events)
    if next_question(answers) is not None or not any(
        event["kind"] == "PREPARATION_COMPLETE" for event in events
    ):
        raise IntakeError("Termine la préparation avant le préflight.")
    if answers.get("git_provider") not in (None, "GITHUB"):
        raise IntakeError("Cette demande n'est pas qualifiée pour GitHub.")
    digest = hashlib.sha256(json.dumps({
        "answers": answers, "source_sha": SOURCE["source_sha"],
        "catalogue_sha": SOURCE["catalogue_git_sha"],
        "workflow_sha": SOURCE["workflow_model_git_sha"],
    }, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
    return answers, digest


def _match_report(report, answers):
    if (not isinstance(report, dict) or report.get("status") != "PREFLIGHT_OBSERVED"
            or report.get("creation_authorized") is not False
            or report.get("app_id") != CUG_APP_ID
            or type(report.get("installation_id")) is not int or report["installation_id"] <= 0
            or report.get("owner") != answers["owner"].lower()
            or report.get("target") != f"{answers['owner']}/{answers['name']}".lower()
            or report.get("visibility_requested") != answers["visibility"]
            or report.get("template") != SOURCE["source_repository"].lower()
            or report.get("template_head_sha") != SOURCE["source_sha"]
            or report.get("target_observation") not in ("PRESENT", "NOT_VISIBLE_404")):
        raise IntakeError("Le rapport ne correspond pas à la demande ou à CUG.")
    # Persist only fields from the trusted adapter and never tokens, headers or bodies.
    return {key: report[key] for key in SAFE_REPORT if key in report}


class CUGPreflight:
    def __init__(self, journal, *, can_preflight, app_jwt, api):
        self.journal = journal
        self.can_preflight = can_preflight
        self.app_jwt = app_jwt
        self.api = api

    def run(self, actor, request_id, expected_revision):
        if not isinstance(actor, GitHubActor):
            raise IntakeError("Identité GitHub utilisateur requise.")
        events = self.journal.get(actor.journal_key, request_id)
        if events[-1]["revision"] != expected_revision:
            raise IntakeError("La demande a changé. Rouvre-la avant le préflight.")
        answers, digest = dossier(events)
        if not self.can_preflight(actor, answers["owner"]):
            raise IntakeError("Préflight non autorisé pour ce compte.")
        try:
            raw = inspect_app(self.api, self.app_jwt(), app_id=CUG_APP_ID,
                              owner=answers["owner"], name=answers["name"],
                              visibility=answers["visibility"], template=SOURCE["source_repository"],
                              template_sha=SOURCE["source_sha"])
            payload = _match_report(raw, answers)
        except PreflightError as exc:
            reason = str(exc)
            payload = {"status": "BLOCKED", "creation_authorized": False,
                       "reason": reason if reason in FIXED_FAILURES or KNOWN_FAILURE.fullmatch(reason)
                       else "PREFLIGHT_UNAVAILABLE"}
        except IntakeError:
            payload = {"status": "BLOCKED", "creation_authorized": False,
                       "reason": "REPORT_DOES_NOT_MATCH_REQUEST"}
        return self.journal.record_preflight(actor.journal_key, request_id, expected_revision,
                                             digest, payload)
