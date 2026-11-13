"""Inventory MCP integration evidence without invoking MCP or running repo code."""

from dataclasses import dataclass
import re
from typing import Protocol


@dataclass(frozen=True)
class Repo:
    name: str
    repo_id: str
    branch: str
    private: bool


@dataclass(frozen=True)
class Blob:
    path: str
    sha: str
    size: int


class SourceError(Exception):
    pass


class EmptyRepository(SourceError):
    pass


class Source(Protocol):
    def repositories(self, account: str) -> list[Repo]: ...
    def tree(self, repo: Repo) -> tuple[str, list[Blob], bool]: ...
    def read(self, repo: Repo, blob: Blob) -> str: ...


_WEALTHTECH = re.compile(r'mcp\.wealthtechinnovations\.com|wealthtech[_-]ssh[_-]bridge', re.I)
_RPC = re.compile(r'\btools/(call|list)\b')
_PROVIDER = re.compile(r'\bFastMCP\s*\(|\b(?:McpServer|Server)\s*\(|\.registerTool\s*\(')
_SDK = re.compile(r'@modelcontextprotocol/sdk|\bfrom mcp\.server\b|\bfrom fastmcp\b')
_TRANSPORT = re.compile(r'urlopen\(|\bfetch\(|\brequests\.|\bhttpx\.|\bcurl\b|\.send\(')
_RUN = re.compile(r'^\s*(?:-\s+)?run\s*:|\b(?:python3?|node|curl|bash)\b', re.M)
_CONFIG = re.compile(r'GOVERNED_MCP_URL|\bMCP_(?:ENDPOINT|URL|SERVER_URL)\b|mcp_repository_discovery|mcp-target\.json')
_DOC = re.compile(r'\.(?:md|rst|txt)$', re.I)
_CODE = re.compile(r'\.(?:py|js|mjs|cjs|ts|tsx|go|rs|rb|sh|ps1)$', re.I)
_TEST = re.compile(r'(^|/)(tests?|__tests__|fixtures|examples)(/|$)|(?:^|/)test_|[._](?:spec|test)\.', re.I)
_IGNORE = re.compile(r'(^|/)(node_modules|vendor|dist|\.git|\.next|archive)(/|$)|(^|/)(\.env[^/]*|secrets?|credentials?|private[_-]?key)(/|\.|$)|\.(?:pem|key|p12|map|min\.js)$', re.I)
_PINNED = re.compile(r'(^\.github/workflows/|(^|/)(mcp[^/]*|[^/]*mcp[^/]*)\.|(^|/)deploy/|^\.governance/|(^|/)(README|AGENTS|ARCHITECTURE|GOVERNANCE)\.md$)', re.I)


def select(path: str) -> int | None:
    if _IGNORE.search(path):
        return None
    if not (_CODE.search(path) or _DOC.search(path) or path.lower().endswith(('.json', '.yaml', '.yml', '.toml'))):
        return None
    if _PINNED.search(path):
        return 0
    if _CODE.search(path) and not _TEST.search(path):
        return 1
    return None


def inspect(path: str, data: str) -> dict | None:
    # Remove obvious comment-only lines before claiming code execution evidence.
    code = '\n'.join('' if line.lstrip().startswith(('#', '//', '*')) else line
                     for line in data.splitlines())
    markers = {
        'wealthtech': _WEALTHTECH.search(data),
        'rpc': _RPC.search(code),
        'provider': _PROVIDER.search(code) if _SDK.search(code) else None,
        'config': _CONFIG.search(data),
    }
    if not any(markers.values()):
        return None
    if _DOC.search(path) or _TEST.search(path):
        kind = 'reference'
    elif _CODE.search(path) and markers['provider']:
        kind = 'mcp_provider_code'
    elif _CODE.search(path) and markers['rpc'] and _TRANSPORT.search(code):
        kind = 'mcp_client_code'
    elif path.startswith('.github/workflows/') and _RUN.search(code):
        kind = ('wealthtech_workflow_http_candidate'
                if _WEALTHTECH.search(code) and _TRANSPORT.search(code)
                else 'workflow_wiring_candidate')
    else:
        kind = 'configuration_or_reference'
    return {
        'path': path, 'kind': kind,
        'mentions_wealthtech': bool(markers['wealthtech']),
        'signals': sorted(k for k, value in markers.items() if value),
    }


def inventory(source: Source, accounts: list[str], *, max_files: int = 125,
              max_bytes: int = 100_000) -> dict:
    if max_files <= 0 or max_bytes <= 0:
        raise ValueError('scan limits must be positive')
    results, errors, seen = [], [], set()
    for account in accounts:
        try:
            repos = source.repositories(account)
        except SourceError as exc:
            errors.append({'account': account, 'error': str(exc)})
            continue
        for repo in repos:
            if repo.repo_id in seen:
                continue
            seen.add(repo.repo_id)
            row = dict(name=repo.name, repo_id=repo.repo_id, branch=repo.branch,
                       private=repo.private, evidence=[], file_errors=0)
            results.append(row)
            try:
                revision, blobs, truncated = source.tree(repo)
            except EmptyRepository:
                row['status'] = 'empty_repository'
                continue
            except SourceError as exc:
                row.update(status='tree_unverified', error=str(exc))
                continue
            paths = sorted(((priority, b.path, b) for b in blobs
                            if (priority := select(b.path)) is not None), key=lambda x: x[:2])
            eligible = [b for _, _, b in paths if b.size <= max_bytes]
            row.update(revision=revision, tree_truncated=truncated, eligible=len(eligible),
                       omitted_by_size=len(paths) - len(eligible),
                       omitted_by_limit=max(0, len(eligible) - max_files), examined=0)
            for blob in eligible[:max_files]:
                try:
                    data = source.read(repo, blob)
                except SourceError:
                    row['file_errors'] += 1
                    continue
                row['examined'] += 1
                found = inspect(blob.path, data)
                if found:
                    row['evidence'].append(found)
            row['status'] = 'signals_found' if row['evidence'] else 'no_signal_in_examined_files'
    return {'schema_version': 1, 'accounts': accounts, 'account_errors': errors,
            'runtime_verified': False, 'repositories': results}
