"""Read-only GitHub.com adapter for the MCP inventory. No MCP or CUG needed."""

import argparse
import base64
import binascii
import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .mcp_inventory import Blob, EmptyRepository, Repo, SourceError, inventory


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


class GitHubSource:
    def __init__(self, tokens: dict[str, str], organizations: set[str]):
        self.tokens = {k.casefold(): v for k, v in tokens.items()}
        self.organizations = {a.casefold() for a in organizations}
        self.opener = build_opener(NoRedirect())

    def _get(self, owner, path):
        token = self.tokens.get(owner.casefold())
        if not token:
            raise SourceError('account_token_missing')
        request = Request('https://api.github.com' + path, headers={
            'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json',
            'User-Agent': 'Loop-MCP-Inventory', 'X-GitHub-Api-Version': '2022-11-28',
        }, method='GET')
        try:
            with self.opener.open(request, timeout=20) as response:
                raw = response.read(32 * 1024 * 1024 + 1)
            if len(raw) > 32 * 1024 * 1024:
                raise SourceError('github_response_too_large')
            return json.loads(raw)
        except HTTPError as exc:
            if exc.code == 409 and '/git/trees/' in path:
                raise EmptyRepository('github_empty_tree') from None
            raise SourceError(f'github_http_{exc.code}') from None
        except (URLError, TimeoutError, ValueError, OSError):
            raise SourceError('github_response_unverified') from None

    def repositories(self, account):
        key = account.casefold()
        if key in self.organizations:
            root = '/orgs/' + quote(account, safe='') + '/repos'
            params = {'type': 'all'}
        else:
            who = self._get(account, '/user')
            if not isinstance(who, dict) or str(who.get('login', '')).casefold() != key:
                raise SourceError('github_user_does_not_match_requested_owner')
            root, params = '/user/repos', {'affiliation': 'owner', 'visibility': 'all'}
        result = []
        for page in range(1, 101):
            query = urlencode(dict(params, per_page=100, page=page, sort='full_name'))
            rows = self._get(account, root + '?' + query)
            if not isinstance(rows, list):
                raise SourceError('github_repository_list_unverified')
            for row in rows:
                if str(row.get('owner', {}).get('login', '')).casefold() == key:
                    result.append(Repo(row['full_name'], str(row['id']), row['default_branch'], row['private']))
            if len(rows) < 100:
                return result
        raise SourceError('github_pagination_limit_reached')

    @staticmethod
    def _repo(repo):
        owner, name = repo.name.split('/', 1)
        return owner, '/repos/' + quote(owner, safe='') + '/' + quote(name, safe='')

    def tree(self, repo):
        owner, root = self._repo(repo)
        # Resolve the branch first to pin the subsequent tree and blob reads.
        branch_path = quote(repo.branch, safe='/')
        try:
            branch = self._get(owner, root + '/branches/' + branch_path)
        except SourceError as exc:
            if str(exc) == 'github_http_404':
                # GitHub can return 404 for the branch of an empty repository.
                # Only the specific Git tree 409 becomes EmptyRepository.
                self._get(owner, root + '/git/trees/' + branch_path)
            raise
        try:
            sha = branch['commit']['sha']
            if not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', sha):
                raise ValueError
            tree = self._get(owner, root + '/git/trees/' + sha + '?recursive=1')
            return sha, [Blob(b['path'], b['sha'], b['size']) for b in tree['tree']
                         if b['type'] == 'blob' and b.get('mode') != '120000'], tree['truncated']
        except (TypeError, KeyError, ValueError):
            raise SourceError('github_tree_unverified') from None

    def read(self, repo, blob):
        owner, root = self._repo(repo)
        if not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', blob.sha):
            raise SourceError('github_blob_id_unverified')
        data = self._get(owner, root + '/git/blobs/' + blob.sha)
        try:
            if data['sha'] != blob.sha or data['encoding'] != 'base64':
                raise ValueError
            return base64.b64decode(''.join(data['content'].split()), validate=True).decode('utf-8')
        except (TypeError, KeyError, ValueError, binascii.Error, UnicodeError):
            raise SourceError('github_blob_not_verified_utf8') from None


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--org', action='append', default=[])
    cli.add_argument('--user', action='append', default=[])
    cli.add_argument('--max-files', type=int, default=125)
    args = cli.parse_args()
    accounts = list(dict.fromkeys(args.org + args.user))
    if not accounts:
        cli.error('specify at least one --org or --user')
    tokens = {a: os.environ.get('LOOP_GH_TOKEN_' + re.sub(r'[^A-Z0-9]', '_', a.upper()), '') for a in accounts}
    report = inventory(GitHubSource(tokens, set(args.org)), accounts, max_files=args.max_files)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report['account_errors'] or any(
        r['status'] == 'tree_unverified' or r.get('tree_truncated') or r.get('file_errors')
        for r in report['repositories']
    ) else 0


if __name__ == '__main__':
    raise SystemExit(main())
