"""GitHub App preflight, without repository writes or a creation Gateway."""
from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import HTTPRedirectHandler, Request, build_opener

ACCOUNTS = {
    "chainsolutions-wealthtech": "Organization",
    "patricked-code": "User",
    "wealthtechinnovations": "User",
}
PREFLIGHT_PERMISSIONS = {"contents": "read"}
SLUG = r"[A-Za-z0-9][A-Za-z0-9-]{0,38}"
NAME = r"[A-Za-z0-9_.-]{1,100}"
SHA = r"[a-f0-9]{40}"


class APIError(Exception):
    def __init__(self, status):
        self.status = status
        super().__init__(f"GitHub API returned {status}")


class PreflightError(Exception):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def github(method, path, credential, body=None):
    request = Request("https://api.github.com" + path, method=method, headers={
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2026-03-10",
        "User-Agent": "governed-creation-app-preflight",
    }, data=json.dumps(body).encode() if body is not None else None)
    try:
        with build_opener(NoRedirect).open(request, timeout=15) as response:
            raw = response.read(2_000_001)
            if len(raw) > 2_000_000:
                raise PreflightError("GITHUB_RESPONSE_TOO_LARGE")
            return json.loads(raw) if raw else {}
    except HTTPError as exc:
        status = exc.code
        exc.close()
        raise APIError(status) from None
    except (URLError, TimeoutError, OSError, ValueError):
        raise PreflightError("GITHUB_RESPONSE_UNAVAILABLE") from None


def _segment(value):
    return base64.urlsafe_b64encode(value).rstrip(b"=")


def make_app_jwt(client_id, private_key, now=None):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,120}", client_id) or not private_key:
        raise PreflightError("APP_CREDENTIAL_NOT_CONFIGURED")
    now = int(time.time()) if now is None else now
    header = _segment(b'{"alg":"RS256","typ":"JWT"}')
    claims = _segment(json.dumps({"iat": now - 60, "exp": now + 300, "iss": client_id}).encode())
    message = header + b"." + claims
    try:
        with TemporaryDirectory() as directory:
            pem = Path(directory) / "app.pem"
            with os.fdopen(os.open(pem, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600), "w") as handle:
                handle.write(private_key)
            result = subprocess.run(
                ["openssl", "dgst", "-sha256", "-sign", str(pem)],
                input=message, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                timeout=10, check=True, env={"PATH": os.defpath + ":/usr/local/bin"},
            )
    except (OSError, subprocess.SubprocessError):
        raise PreflightError("APP_JWT_SIGNING_FAILED") from None
    return (message + b"." + _segment(result.stdout)).decode()


def _matches(value, pattern):
    return isinstance(value, str) and re.fullmatch(pattern, value) is not None


def _id(value):
    return type(value) is int and value > 0


def _repo_path(owner, name):
    if not _matches(owner, SLUG) or not _matches(name, NAME) or name in {".", ".."}:
        raise PreflightError("INVALID_REPOSITORY_COORDINATES")
    return f"/repos/{owner.lower()}/{name.lower()}"


def _metadata_call(api, path, credential, operation):
    try:
        data = api("GET", path, credential)
    except APIError as exc:
        raise PreflightError(f"{operation}_HTTP_{exc.status}") from None
    if not isinstance(data, dict):
        raise PreflightError(f"{operation}_INVALID_RESPONSE")
    return data


def inspect_app(api, jwt, *, app_id, owner, name, visibility, template, template_sha):
    """A successful report still does not authorize a creation."""
    if not _matches(owner, SLUG):
        raise PreflightError("INVALID_OWNER_OR_VISIBILITY")
    owner = owner.lower()
    owner_type = ACCOUNTS.get(owner)
    if not owner_type or visibility not in ("private", "public"):
        raise PreflightError("INVALID_OWNER_OR_VISIBILITY")
    target_path = _repo_path(owner, name)
    parts = template.split("/") if isinstance(template, str) else []
    if len(parts) != 2 or not _matches(template_sha, SHA):
        raise PreflightError("INVALID_TEMPLATE_OR_REVISION")
    template_path = _repo_path(*parts)
    if target_path == template_path:
        raise PreflightError("TARGET_IS_THE_TEMPLATE")
    app = _metadata_call(api, "/app", jwt, "APP_IDENTITY")
    if not _id(app_id) or not _id(app.get("id")) or app["id"] != app_id:
        raise PreflightError("UNEXPECTED_APP_IDENTITY")
    root = "orgs" if owner_type == "Organization" else "users"
    install = _metadata_call(api, f"/{root}/{owner}/installation", jwt, "INSTALLATION")
    account = install.get("account") or {}
    selection = install.get("repository_selection")
    if (install.get("app_id") != app_id or not _id(install.get("id"))
            or not isinstance(account, dict) or not _id(account.get("id"))
            or str(account.get("login", "")).lower() != owner
            or account.get("type") != owner_type
            or "suspended_at" not in install or install["suspended_at"] is not None
            or selection not in {"all", "selected"}):
        raise PreflightError("INSTALLATION_NOT_VERIFIED_FOR_OWNER")
    perms = install.get("permissions") or {}
    if not isinstance(perms, dict):
        raise PreflightError("INSTALLATION_PERMISSIONS_UNVERIFIED")
    creation_permission = (
        perms.get("contents") in {"read", "write"}
        and (perms.get("administration") == "write" or perms.get("repository_creation") == "write")
    )
    try:
        minted = api("POST", f"/app/installations/{install['id']}/access_tokens", jwt,
                     {"permissions": dict(PREFLIGHT_PERMISSIONS)})
    except APIError as exc:
        raise PreflightError(f"INSTALLATION_TOKEN_HTTP_{exc.status}") from None
    token = minted.get("token") if isinstance(minted, dict) else None
    if not isinstance(token, str) or not token:
        raise PreflightError("INSTALLATION_TOKEN_UNVERIFIED")
    try:
        report = _inspect_repositories(api, jwt, token, minted, app_id, owner, name, visibility, account,
                                       install["id"], selection, creation_permission,
                                       target_path, template_path, template_sha)
    finally:
        try:
            api("DELETE", "/installation/token", token)
        except (APIError, PreflightError):
            raise PreflightError("PREFLIGHT_TOKEN_REVOCATION_UNCONFIRMED") from None
    return report


def _inspect_repositories(api, jwt, token, minted, app_id, owner, name, visibility, account,
                          installation_id, selection, creation_permission,
                          target_path, template_path, template_sha):
    token_permissions = minted.get("permissions")
    if (not isinstance(token_permissions, dict) or token_permissions.get("contents") != "read"
            or any(p not in {"contents", "metadata"} or v != "read" for p, v in token_permissions.items())):
        raise PreflightError("PREFLIGHT_TOKEN_NOT_READ_ONLY")
    meta = _metadata_call(api, template_path, token, "TEMPLATE_METADATA")
    expected_name = template_path.removeprefix("/repos/")
    if (str(meta.get("full_name", "")).lower() != expected_name
            or meta.get("is_template") is not True or not _id(meta.get("id"))):
        raise PreflightError("TEMPLATE_IDENTITY_UNVERIFIED")
    default_branch = meta.get("default_branch")
    if not isinstance(default_branch, str) or not default_branch:
        raise PreflightError("TEMPLATE_BRANCH_UNVERIFIED")
    head = _metadata_call(api, f"{template_path}/commits/{quote(default_branch, safe='')}", token, "TEMPLATE_HEAD")
    if head.get("sha") != template_sha:
        raise PreflightError("TEMPLATE_HEAD_DIFFERS_FROM_REQUEST")
    # For public as well as private templates, prove actual installation coverage.
    try:
        coverage = api("GET", f"{template_path}/installation", jwt)
    except APIError as exc:
        if exc.status != 404:
            raise PreflightError(f"TEMPLATE_INSTALLATION_HTTP_{exc.status}") from None
        coverage = None
    same_installation = (
        isinstance(coverage, dict) and coverage.get("id") == installation_id
        and coverage.get("app_id") == app_id
        and "suspended_at" in coverage and coverage["suspended_at"] is None
    )
    if not isinstance(meta.get("private"), bool):
        raise PreflightError("TEMPLATE_VISIBILITY_UNVERIFIED")
    try:
        target = api("GET", target_path, token)
    except APIError as exc:
        if exc.status != 404:
            raise PreflightError(f"TARGET_OBSERVATION_HTTP_{exc.status}") from None
        target = None
    if target is not None and (
        not isinstance(target, dict) or not _id(target.get("id"))
        or str(target.get("full_name", "")).lower() != f"{owner}/{name.lower()}"
    ):
        raise PreflightError("TARGET_IDENTITY_UNVERIFIED")
    return {
        "status": "PREFLIGHT_OBSERVED",
        "app_id": app_id,
        "installation_id": installation_id,
        "owner": owner,
        "owner_id": account["id"],
        "owner_type": account["type"],
        "repository_selection": selection,
        "target": f"{owner}/{name.lower()}",
        "visibility_requested": visibility,
        "target_observation": "PRESENT" if target is not None else "NOT_VISIBLE_404",
        "target_repository_id": target["id"] if target is not None else None,
        "template": expected_name,
        "template_repository_id": meta["id"],
        "template_head_sha": template_sha,
        "template_private": meta["private"],
        "template_same_installation_verified": same_installation,
        "installation_creation_permissions_declared": creation_permission,
        "creation_authorized": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-id", required=True, type=int)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--visibility", choices=("private", "public"), required=True)
    parser.add_argument("--template", required=True)
    parser.add_argument("--template-sha", required=True)
    args = parser.parse_args()
    try:
        jwt = make_app_jwt(os.environ.get("CREATION_APP_CLIENT_ID", ""),
                           os.environ.pop("CREATION_APP_PRIVATE_KEY", ""))
        report = inspect_app(github, jwt, **vars(args))
    except PreflightError as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc), "creation_authorized": False}))
        return 1
    print(json.dumps(report, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
