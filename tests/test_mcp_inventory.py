import unittest

from loop.github_inventory_source import GitHubSource
from loop.mcp_inventory import Blob, EmptyRepository, Repo, SourceError, inspect, inventory, select


class FixtureSource:
    repos = {'org': [Repo('org/a', '1', 'main', False), Repo('org/b', '2', 'main', True),
                     Repo('org/empty', '3', 'main', False)],
             'user': [Repo('org/a', '1', 'main', False)]}

    def repositories(self, account):
        if account not in self.repos:
            raise SourceError('denied')
        return self.repos[account]

    def tree(self, repo):
        if repo.repo_id == '3':
            raise EmptyRepository()
        return 'a' * 40, [Blob('README.md', '1', 100), Blob('client.py', '2', 80),
                           Blob('secret.pem', '3', 80), Blob('huge.py', '4', 500)], repo.private

    def read(self, repo, blob):
        if repo.private and blob.path == 'client.py':
            raise SourceError('blob denied')
        return 'from urllib.request import urlopen\nurlopen(req)\nmethod = "tools/call"\n' if blob.path == 'client.py' else 'wealthtech_ssh_bridge'


class MCPInventoryTest(unittest.TestCase):
    def test_scans_and_deduplicates_preserving_limits_and_errors(self):
        r = inventory(FixtureSource(), ['org', 'user', 'unreadable'], max_bytes=200)
        self.assertFalse(r['runtime_verified'])
        self.assertEqual(len(r['repositories']), 3)
        a, b, empty = r['repositories']
        self.assertEqual(a['omitted_by_size'], 1)
        self.assertEqual(a['examined'], 2)
        self.assertEqual([x['kind'] for x in a['evidence']], ['reference', 'mcp_client_code'])
        self.assertTrue(b['private'])
        self.assertTrue(b['tree_truncated'])
        self.assertEqual(b['file_errors'], 1)
        self.assertEqual(empty['status'], 'empty_repository')
        self.assertEqual(r['account_errors'][0]['account'], 'unreadable')

    def test_reports_scan_cap(self):
        row = inventory(FixtureSource(), ['org'], max_files=1)['repositories'][0]
        self.assertEqual(row['examined'], 1)
        self.assertEqual(row['omitted_by_limit'], 2)

    def test_comment_is_not_a_client_call(self):
        self.assertEqual(inspect('client.py', '# tools/call wealthtech_ssh_bridge\nfetch(x)')['kind'],
                         'configuration_or_reference')

    def test_other_mcp_is_not_wealthtech(self):
        self.assertEqual(inspect('server.py', 'from mcp.server.fastmcp import FastMCP\nFastMCP()')['kind'],
                         'mcp_provider_code')
        self.assertFalse(inspect('server.py', 'from mcp.server.fastmcp import FastMCP\nFastMCP()')['mentions_wealthtech'])

    def test_does_not_emit_source_content(self):
        out = inspect('README.md', 'wealthtech_ssh_bridge placeholder-sensitive')
        self.assertNotIn('placeholder-sensitive', str(out))
        self.assertIsNone(select('.env.production'))
        self.assertIsNone(select('vendor/a/mcp.py'))

    def test_wrong_account_fails_before_enumeration(self):
        s = GitHubSource({'expected': 'unused'}, set())
        s._get = lambda owner, path: {'login': 'other'}
        with self.assertRaisesRegex(SourceError, 'does_not_match'):
            s.repositories('expected')

    def test_github_organization_pagination(self):
        s = GitHubSource({'Org': 'unused'}, {'org'})
        calls = []
        def response(owner, path):
            calls.append(path)
            ids = range(100) if 'page=1&' in path else range(100, 101)
            return [dict(owner={'login': 'org'}, id=i, full_name=f'org/{i}', default_branch='main',
                         private=True) for i in ids]
        s._get = response
        self.assertEqual(len(s.repositories('Org')), 101)
        self.assertEqual(len(calls), 2)

    def test_missing_branch_distinguishes_empty_from_access_failure(self):
        s = GitHubSource({'Org': 'unused'}, {'org'})
        repo = Repo('org/a', '1', 'main', False)
        def read(owner, path):
            if '/branches/' in path:
                raise SourceError('github_http_404')
            raise EmptyRepository('github_empty_tree')
        s._get = read
        with self.assertRaises(EmptyRepository):
            s.tree(repo)
        def denied(owner, path):
            raise SourceError('github_http_404')
        s._get = denied
        with self.assertRaisesRegex(SourceError, 'github_http_404'):
            s.tree(repo)
