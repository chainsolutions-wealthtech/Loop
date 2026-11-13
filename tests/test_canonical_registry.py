import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from loop.canonical_registry import build, describe, private_lookup, resolve, validate
from loop.evidence_store import import_snapshot

ROOT = Path(__file__).resolve().parents[1]


class CanonicalRegistryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project, cls.nodes, cls.aliases = build(ROOT)
        cls.children = validate(ROOT, cls.project, cls.nodes, cls.aliases)

    def test_project_and_continuity_are_separate_from_repo(self):
        self.assertEqual(self.project, 'WT-PROJECT-LOOP-001')
        self.assertEqual(self.nodes['LOOP-REPO-1456075212']['repository']['github_id'], '1456075212')
        node = describe(self.nodes, self.aliases, self.children, 'LOOP-CP-20261113-002')
        self.assertEqual(node['hierarchy'], [self.project, 'LOOP-SP-04',
                         'LOOP-CONV-CONT-20261113-ROOT-01', 'LOOP-CP-20261113-002'])
        self.assertEqual(node['canonical_links']['next_work'], ['LOOP-W09', 'LOOP-W10'])

    def test_aliases_remain_resolvable_with_reverse_links(self):
        self.assertEqual(resolve(self.nodes, self.aliases, 'E15')['id'], 'LOOP-EVT-20261113-015')
        self.assertEqual(resolve(self.nodes, self.aliases, 'D11')['id'], 'LOOP-DSP-11')
        req = describe(self.nodes, self.aliases, self.children, 'REQ-011')
        self.assertIn({'from': 'LOOP-MOD-007', 'relation': 'requirements'}, req['referenced_by'])

    def test_tables_and_module_contracts_remain_separate_from_planned_capabilities(self):
        self.assertEqual(sum(n['kind'] == 'module' for n in self.nodes.values()), 7)
        self.assertEqual(self.nodes['LOOP-TBL-003']['parent'], 'LOOP-MOD-006')
        self.assertEqual(self.nodes['LOOP-CAP-001']['state'], 'specified_not_implemented')
        self.assertNotIn('implementation', self.nodes['LOOP-CAP-001'])

    def test_private_lookup_uses_exact_snapshot_and_is_read_only(self):
        with TemporaryDirectory() as tmp:
            d = Path(tmp)
            f = d / 'fixture.json'
            f.write_text(json.dumps({'repositories': [
                {'name':'example/demo','url':'https://github.com/example/demo','repo_id':'42','account':'example',
                 'artifacts':[{'path':'script.py'}]}
            ]}))
            db = d / 'private.sqlite'
            import_snapshot(db, f, 'LOOP-INV-20261113-02', 'fixture')
            before = db.read_bytes()
            self.assertEqual(private_lookup(db, 'LOOP-INV-20261113-02:42')['name'], 'example/demo')
            self.assertEqual(private_lookup(db, 'LOOP-INV-20261113-02:42:artifacts:0')['path'], 'script.py')
            with self.assertRaises(KeyError):
                private_lookup(db, 'LOOP-INV-20261113-03:42')
            self.assertEqual(db.read_bytes(), before)
