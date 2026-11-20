import json
import os
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest

from loop.evidence_store import import_snapshot
from loop.mcp_catalog import render_html, repository_row


class EvidenceStoreTest(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.db = self.root / 'registry.sqlite'
        self.row = repository_row('owner/demo', '42', 'main', True, 'owner')
        self.row['relations'] = [{'kind': 'file_reference', 'target': 'code.py',
                                  'status': 'declared', 'source': {'path': 'wf.yml', 'line': 12, 'sha': 'abc'}}]

    def json(self, rows):
        p = self.root / 'source.json'
        p.write_text(json.dumps({'repositories': rows}))
        return p

    def test_idempotent_snapshot_with_provenance_and_private_mode(self):
        p = self.json([self.row])
        result = import_snapshot(self.db, p, 'inv-1', 'branch default', expected_count=1)
        self.assertEqual(import_snapshot(self.db, p, 'inv-1', 'branch default'), result)
        with sqlite3.connect(self.db) as con:
            self.assertEqual(con.execute('SELECT count(*) FROM repository').fetchone()[0], 1)
            self.assertIn('code.py', con.execute('SELECT payload_json FROM observation').fetchone()[0])
        if os.name == 'posix':
            self.assertEqual(self.db.stat().st_mode & 0o777, 0o600)

    def test_snapshot_id_cannot_overwrite_changed_evidence(self):
        p = self.json([self.row])
        import_snapshot(self.db, p, 'inv-1', 'one')
        self.row['branch'] = 'release'
        self.json([self.row])
        with self.assertRaises(ValueError):
            import_snapshot(self.db, p, 'inv-1', 'one')
        import_snapshot(self.db, p, 'inv-2', 'two')
        with sqlite3.connect(self.db) as con:
            self.assertEqual(con.execute('SELECT count(*) FROM snapshot').fetchone()[0], 2)

    def test_rejects_missing_or_duplicate_repository_before_writing(self):
        p = self.json([self.row, self.row])
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            import_snapshot(self.db, p, 'inv-1', 'one')
        self.assertFalse(self.db.exists())
        p = self.json([self.row])
        with self.assertRaisesRegex(ValueError, 'count'):
            import_snapshot(self.db, p, 'inv-1', 'one', expected_count=2)
        self.assertFalse(self.db.exists())

    def test_html_export_import_is_data_only_and_preserves_tables(self):
        self.row['runtime_tool_catalogue'] = {
            'tools': ['ping'], 'observed_at': 'date', 'revision': 'abc'}
        p = self.root / 'source.html'
        p.write_text(render_html({'repositories': [self.row]}))
        import_snapshot(self.db, p, 'html-1', 'one')
        with sqlite3.connect(self.db) as con:
            self.assertEqual(con.execute('PRAGMA integrity_check').fetchone()[0], 'ok')
            kinds = {x[0] for x in con.execute('SELECT section FROM observation')}
            self.assertIn('Raccordements et appels', kinds)
            self.assertIn('Catalogue fournisseur observé', kinds)
