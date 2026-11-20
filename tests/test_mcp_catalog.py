import unittest

from loop.mcp_catalog import Catalog, render_html, repository_row, supplement
from loop.mcp_inventory import inspect


class CatalogTest(unittest.TestCase):
    def test_workflow_package_script_and_mcp_calls(self):
        workflow = '.github/workflows/run.yml'
        script = 'scripts/client.py'
        catalog = Catalog([workflow, 'package.json', script, 'scripts/unread.sh'], 'sha')
        catalog.read(workflow, 'steps:\n  - run: npm run discover\n  - uses: owner/tool@v1')
        catalog.read('package.json', '{"scripts":{"discover":"python scripts/client.py"}}')
        data = '''
TOOLS = {"ping": "health", "get_project_context": "context"}
unrelated = "not-a-tool"
for i, name in enumerate(TOOLS):
    call_tool(endpoint, token, session, i, name)
req = {"method": "tools/call", "params": {"name": "list_domains_s1"}}
initialize = {"clientInfo": {"name": "loop-agent"}}
urlopen(req)
'''
        catalog.read(script, data, inspect(script, data))
        row = catalog.project(repository_row('org/repo', '42', 'main', True, 'org'))
        self.assertEqual(row['account'], 'org')
        self.assertEqual(row['url'], 'https://github.com/org/repo')
        self.assertEqual(row['mcp_tools_used'], ['get_project_context', 'list_domains_s1', 'ping'])
        self.assertEqual(row['declared_mcp_client_names'], ['loop-agent'])
        self.assertEqual(row['linked_mcp_clients'], [])
        self.assertIn({'path': 'scripts/unread.sh', 'type': 'script', 'read_status': 'not_read'}, row['artifacts'])
        self.assertIn(('package_script_reference', 'package.json#scripts.discover'),
                      [(x['kind'], x['target']) for x in row['relations']])
        self.assertIn(('file_reference', script), [(x['kind'], x['target']) for x in row['relations']])

    def test_declaration_and_registry_candidate_remain_separate(self):
        p = 'deploy/mcp-target.json'
        c = Catalog([p], 'abc')
        c.read(p, '{"destination":{"server":"s1","applicationDirectory":"UNRESOLVED"},'
                  '"orchestrator":{"endpoint":"https://host.example/mcp?secret=test"}}')
        row = c.project(repository_row('org/repo', '42', 'main', False, 'org'))
        report = {'repositories': [row]}
        supplement(report, registry_candidates=[
            {'repo': 'github:org/repo', 'server': 's2', 'directory': '/apps/example',
             'binding_status': 'proposed'},
            {'repo': 'github:org/other', 'directory': '/wrong'},
        ])
        self.assertEqual(row['mcp_server_links'], ['https://host.example/mcp'])
        self.assertEqual([x['status'] for x in row['server_bindings']], ['declared', 'registry_candidate'])
        self.assertIsNone(row['server_bindings'][0]['directory'])
        self.assertNotIn('secret=test', str(row))
        self.assertIn('proposed', render_html(report))
        self.assertNotIn('/wrong', render_html(report))

    def test_provider_registration_is_not_a_consumer_call(self):
        p = 'tools.ts'
        c = Catalog([p], 'sha')
        c.read(p, "server.registerTool('ping', {});\nserver.tool('health', {});")
        row = c.project(repository_row('org/repo', '1', 'main', False, 'org'))
        self.assertEqual(row['mcp_tools_exposed'], ['health', 'ping'])
        self.assertEqual(row['mcp_tools_used'], [])

    def test_escape_untrusted_report_fields(self):
        row = repository_row('org/<script>', '1', 'main', True, 'org')
        row['status'] = 'tree_unverified'
        output = render_html({'repositories': [row]})
        self.assertNotIn('org/<script>', output)
        self.assertIn('org/&lt;script&gt;', output)

    def test_classifier_emits_one_requested_category(self):
        p = 'README.md'
        c = Catalog([p], 'sha')
        data = 'wealthtech_ssh_bridge'
        signal = inspect(p, data)
        c.read(p, data, signal)
        self.assertEqual(signal['classification'], 'reference')
        self.assertEqual(signal['source']['sha'], 'sha')
