"""Versioned local SQLite store for private Loop inventory observations."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import sqlite3
from urllib.parse import urlsplit


SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS snapshot (
  snapshot_id TEXT PRIMARY KEY, scope TEXT NOT NULL, source_format TEXT NOT NULL,
  source_sha256 TEXT NOT NULL, source_name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS repository (
  snapshot_id TEXT NOT NULL REFERENCES snapshot(snapshot_id),
  github_id TEXT NOT NULL, full_name TEXT NOT NULL, account TEXT NOT NULL,
  url TEXT NOT NULL, payload_json TEXT NOT NULL,
  PRIMARY KEY (snapshot_id, github_id)
);
CREATE TABLE IF NOT EXISTS observation (
  snapshot_id TEXT NOT NULL, github_id TEXT NOT NULL,
  section TEXT NOT NULL, position INTEGER NOT NULL,
  payload_json TEXT NOT NULL,
  PRIMARY KEY (snapshot_id, github_id, section, position),
  FOREIGN KEY (snapshot_id, github_id) REFERENCES repository(snapshot_id, github_id)
);
CREATE INDEX IF NOT EXISTS repo_lookup ON repository(full_name, snapshot_id);
"""


class InventoryHTML(HTMLParser):
    """Read the known Loop HTML export without running it or following links."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self.row = None
        self.table = None
        self.heading = None
        self.section = 'Fiche'
        self.cells = None
        self.cell = None
        self.links = None
        self.paragraph = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'details':
            self.row = {'tables': {}}
            self.section = 'Fiche'
        if self.row is None:
            return
        if tag == 'h3':
            self.heading = []
        elif tag == 'p' and self.section == 'Catalogue des outils du fournisseur observé':
            self.paragraph = []
        elif tag == 'table':
            self.table = {'headers': [], 'rows': []}
        elif tag == 'tr' and self.table is not None:
            self.cells = []
        elif tag in ('th', 'td') and self.cells is not None:
            self.cell, self.links = [], []
        elif tag == 'a' and self.cell is not None:
            url = values.get('href', '')
            if url.startswith('https://github.com/'):
                self.links.append(url)

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)
        if self.heading is not None:
            self.heading.append(data)
        if self.paragraph is not None:
            self.paragraph.append(data)

    def handle_endtag(self, tag):
        if self.row is None:
            return
        if tag == 'h3' and self.heading is not None:
            self.section = ''.join(self.heading)
            self.heading = None
        elif tag == 'p' and self.paragraph is not None:
            self.row.setdefault('provider_catalogue_text', []).append(''.join(self.paragraph))
            self.paragraph = None
        elif tag in ('th', 'td') and self.cell is not None:
            value = ''.join(self.cell)
            if tag == 'th':
                self.table['headers'].append(value)
            else:
                self.cells.append({'text': value, 'links': self.links})
            self.cell, self.links = None, None
        elif tag == 'tr' and self.cells is not None:
            if self.cells:
                self.table['rows'].append(self.cells)
            self.cells = None
        elif tag == 'table' and self.table is not None:
            self.row['tables'][self.section] = self.table
            self.table = None
        elif tag == 'details':
            fields = {r[0]['text']: r[1]['text']
                      for r in self.row['tables'].get('Fiche', {}).get('rows', [])
                      if len(r) == 2}
            if all(fields.get(k) for k in ('Nom', 'URL', 'Compte associé', 'Identifiant GitHub')):
                self.row.update(name=fields['Nom'], url=fields['URL'], account=fields['Compte associé'],
                                repo_id=fields['Identifiant GitHub'])
                self.rows.append(self.row)
            self.row = None


def _validate_repo(row):
    name, account, repo_id, url = (row[k] for k in ('name', 'account', 'repo_id', 'url'))
    u = urlsplit(url)
    if (not isinstance(repo_id, str) or not repo_id.isdecimal() or name.count('/') != 1
            or name.split('/')[0].casefold() != account.casefold()
            or u.scheme != 'https' or u.netloc != 'github.com' or u.query or u.fragment
            or u.path.rstrip('/').casefold() != ('/' + name).casefold()):
        raise ValueError('invalid repository identity')


def import_snapshot(database, source, snapshot_id, scope, *, expected_count=None):
    """Append a snapshot. A repeated ID is accepted only for the same observation."""
    database, source = Path(database), Path(source)
    if not snapshot_id.strip() or not scope.strip():
        raise ValueError('snapshot ID and scope required')
    source_format = source.suffix.lower().removeprefix('.')
    data = source.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if source_format == 'html':
        parser = InventoryHTML()
        parser.feed(data.decode('utf-8'))
        parser.close()
        rows = parser.rows
    elif source_format == 'json':
        rows = json.loads(data)['repositories']
    else:
        raise ValueError('only Loop HTML or JSON reports are supported')
    if not rows or (expected_count is not None and expected_count != len(rows)):
        raise ValueError('repository count does not match the requested scope')
    for row in rows:
        _validate_repo(row)
    if len({r['repo_id'] for r in rows}) != len(rows):
        raise ValueError('duplicate repository ID in snapshot')
    # Create new stores with owner-only permissions. Existing permissions are not changed.
    fd = os.open(database, os.O_CREAT | os.O_WRONLY, 0o600)
    os.close(fd)
    con = sqlite3.connect(database)
    try:
        con.executescript(SCHEMA)
        with con:
            con.execute('BEGIN IMMEDIATE')
            prior = con.execute(
                'SELECT scope,source_format,source_sha256 FROM snapshot WHERE snapshot_id=?',
                (snapshot_id,)).fetchone()
            if prior is not None:
                if prior != (scope, source_format, digest):
                    raise ValueError('snapshot ID already references different content or scope')
                return len(rows), digest
            con.execute('INSERT INTO snapshot VALUES (?,?,?,?,?)',
                        (snapshot_id, scope, source_format, digest, source.name))
            for row in rows:
                rid = row['repo_id']
                con.execute('INSERT INTO repository VALUES (?,?,?,?,?,?)',
                            (snapshot_id, rid, row['name'], row['account'], row['url'],
                             json.dumps(row, ensure_ascii=False)))
                if source_format == 'html':
                    groups = [(k, v['rows']) for k, v in row['tables'].items()]
                    if row.get('provider_catalogue_text'):
                        groups.append(('Catalogue fournisseur observé', row['provider_catalogue_text']))
                else:
                    groups = [(k, row.get(k, [])) for k in (
                        'artifacts', 'relations', 'evidence', 'server_bindings',
                        'declared_mcp_client_links', 'linked_mcp_clients')]
                    if row.get('runtime_tool_catalogue'):
                        groups.append(('runtime_tool_catalogue', [row['runtime_tool_catalogue']]))
                con.executemany('INSERT INTO observation VALUES (?,?,?,?,?)',
                                ((snapshot_id, rid, k, i, json.dumps(item, ensure_ascii=False))
                                 for k, entries in groups for i, item in enumerate(entries)))
        return len(rows), digest
    finally:
        con.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('database', type=Path)
    parser.add_argument('source', type=Path)
    parser.add_argument('--snapshot-id', required=True)
    parser.add_argument('--scope', required=True)
    parser.add_argument('--expected-count', type=int)
    args = parser.parse_args()
    count, digest = import_snapshot(args.database, args.source, args.snapshot_id, args.scope,
                                    expected_count=args.expected_count)
    print(json.dumps({'repositories': count, 'source_sha256': digest}))


if __name__ == '__main__':
    main()
