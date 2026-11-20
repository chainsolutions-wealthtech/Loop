"""Offline navigation of the Loop project registry and private observations."""
import argparse
from collections import defaultdict
from contextlib import closing
import json
from pathlib import Path
import re
import sqlite3

from .project_anchor import public_index


def read(root, path):
    return json.loads((root / path).read_text(encoding='utf-8'))


def build(root):
    identity = read(root, 'registry/identity.json')
    modules = read(root, 'registry/modules.json')
    subjects = read(root, 'registry/subjects.json')
    work = read(root, 'registry/work.json')
    evidence = read(root, 'registry/evidence.json')['evidence']
    dispatch = read(root, 'registry/dispatch-review.json')
    repos = read(root, 'registry/public-repositories.json')['repositories']
    root_id = identity['project_id']
    anchors_path = 'registry/project-anchors.json'
    anchors = public_index(read(root, anchors_path))
    repository = identity['repository']
    anchor = anchors.by_repository(repository['host'], repository['github_id'])
    if (anchor is None or anchor.project_id != root_id
            or not any(r.full_name == repository['full_name'] and
                       r.key == (repository['host'].lower(), repository['github_id'])
                       for r in anchor.repositories)):
        raise ValueError('public project anchor disagrees with the identity manifest')
    nodes, aliases = {}, {}

    def add(node_id, parent, kind, title, source, **data):
        if node_id in nodes or node_id in aliases:
            raise ValueError(f'duplicate ID: {node_id}')
        nodes[node_id] = dict(id=node_id, parent=parent, kind=kind, title=title,
                              source=source, **data)

    def alias(old, new):
        if old in aliases or old in nodes:
            raise ValueError(f'duplicate alias: {old}')
        aliases[old] = new

    add(root_id, None, 'project', identity['name'], 'registry/identity.json',
        state=identity['status'], responsibility=identity['responsibility'])
    add(identity['repository']['id'], root_id, 'repository', identity['repository']['full_name'],
        'registry/identity.json', repository=identity['repository'])
    for uid, title, source in subjects['subprojects']:
        add(uid, root_id, 'subproject', title, source)
    for uid, parent, title, source in subjects['topics']:
        add(uid, parent, 'subject', title, source)
    for parent, leaves in subjects['levels'].items():
        for suffix, title in leaves.items():
            add(f'{parent}-{suffix}', parent, 'design_element', title, nodes[parent]['source'],
                state='reference_model')
    for m in modules['modules']:
        data = {k: v for k, v in m.items() if k not in ('id', 'parent', 'name')}
        add(m['id'], m['parent'], 'module', m['name'], 'registry/modules.json', **data)
        for i, step in enumerate(m['process'], 1):
            add(f"{m['id']}-STEP-{i:02d}", m['id'], 'process_step', step,
                'registry/modules.json', ordinal=i)
    for m in modules['planned_capabilities']:
        data = {k: v for k, v in m.items() if k not in ('id', 'parent', 'name')}
        add(m['id'], m['parent'], 'planned_capability', m['name'], 'registry/modules.json', **data)
    for uid, parent, title, source, fields in subjects['tables']:
        add(uid, parent, 'table', title, source, fields=fields)
        for i, field in enumerate(fields, 1):
            add(f'{uid}-FIELD-{i:02d}', uid, 'table_field', field, source)
    add('LOOP-ANCHOR-001', 'LOOP-TBL-015', 'project_anchor', 'Ancrage GitHub du projet Loop',
        anchors_path, contract='docs/PROJECT_ANCHOR.md', state='server_not_attested',
        repository=repository, work=['LOOP-W15'])
    for uid, parent, title, source in subjects['operations']:
        add(uid, parent, 'operation', title, source)

    continuity = identity['continuity']
    add(continuity['id'], 'LOOP-SP-04', 'continuity', 'Continuité du chantier Loop',
        'registry/identity.json', next_work=continuity['next_work'], blocked_work=continuity['blocked_work'])
    add(continuity['parent_checkpoint_id'], continuity['id'], 'checkpoint', 'Mémoire initiale du chantier',
        'memory/2026-11-13-loop.md', baseline_sha=continuity['baseline_sha'])
    add(continuity['checkpoint_id'], continuity['id'], 'checkpoint', 'Point de reprise courant',
        continuity['record'], previous=continuity['parent_checkpoint_id'],
        baseline_sha=continuity['baseline_sha'], next_work=continuity['next_work'],
        blocked_work=continuity['blocked_work'], next_action=continuity['next_action'],
        operation_mode=continuity['operation_mode'])
    for timeline in subjects['timelines']:
        event_record = timeline['record']
        event_headings = dict(re.findall(
            r'^## (E\d+) — (.+)$', (root / event_record).read_text(encoding='utf-8'), re.M))
        if set(event_headings) != set(timeline['event_topics']):
            raise ValueError('event mappings must cover the complete timeline')
        for old, parent in timeline['event_topics'].items():
            uid = f"LOOP-EVT-{timeline['date']}-{int(old[1:]):03d}"
            add(uid, parent, 'event', event_headings[old], event_record,
                legacy_id=old, continuity_id=continuity['id'])
            if timeline.get('legacy_short_aliases'):
                alias(old, uid)
    if {w['id'] for w in work['work']} != set(subjects['work_topics']):
        raise ValueError('work mappings must cover the complete registry')
    for w in work['work']:
        data = {k: v for k, v in w.items() if k not in ('id', 'title')}
        add(w['id'], subjects['work_topics'][w['id']], 'work', w['title'], 'registry/work.json', **data)
    for r in work['requirements']:
        uid = f"LOOP-{r['id']}"
        parent = resolve(nodes, aliases, r['events'][0])['parent']
        add(uid, parent, 'requirement', r['need'], 'registry/work.json', events=r['events'], legacy_id=r['id'])
        alias(r['id'], uid)
    for uid, parent, title, source, events in subjects['decisions']:
        add(uid, parent, 'decision', title, source, events=events,
            state='recorded_in_working_branch')
    for p in evidence:
        uid = f"LOOP-{p['id']}"
        add(uid, 'LOOP-TBL-011', 'evidence', p['summary'], 'registry/evidence.json',
            reference=p['reference'], state=p['status'], legacy_id=p['id'])
        alias(p['id'], uid)
    add(dispatch['snapshot_id'], 'LOOP-TBL-001', 'snapshot', 'Relevé privé des dépôts du 13 novembre',
        'registry/evidence.json', evidence=['EV-003', 'EV-010'])
    for d in dispatch['sites']:
        uid = f"LOOP-DSP-{d['id'][1:]}"
        add(uid, 'LOOP-TBL-009', 'dispatch', f"{d['repository']} / {d['path']}:{d['line']}",
            'registry/dispatch-review.json', reference=d['reference'], state=d['status'],
            evidence=['EV-012'], legacy_id=d['id'])
        alias(d['id'], uid)
    for repo in repos:
        uid = f"LOOP-REPO-{repo['github_id']}"
        if uid in nodes:
            nodes[uid]['inventory_projection'] = 'registry/public-repositories.json'
        else:
            add(uid, 'LOOP-TBL-012', 'observed_repository', repo['repository'],
                'registry/public-repositories.json', reference=repo['url'], sha=repo['sha'],
                state=repo['coverage'])

    return root_id, nodes, aliases


LINK_FIELDS = (
    'requirements', 'evidence', 'work', 'depends_on', 'events', 'next_work',
    'blocked_work', 'previous', 'continuity_id',
)


def resolve(nodes, aliases, uid):
    return nodes[aliases.get(uid, uid)]


def validate(root, root_id, nodes, aliases):
    children = defaultdict(list)
    for node in nodes.values():
        parent = node['parent']
        if parent is None and node['id'] != root_id:
            raise ValueError(f"unexpected root: {node['id']}")
        if parent is not None:
            if parent not in nodes:
                raise ValueError(f'missing parent: {parent}')
            children[parent].append(node['id'])
        for field in ('source', 'contract', 'implementation'):
            if (path := node.get(field)) and not (root / path).is_file():
                raise ValueError(f'missing file: {path}')
        for field in LINK_FIELDS:
            links = node.get(field, [])
            for ref in [links] if isinstance(links, str) else links:
                resolve(nodes, aliases, ref)
        if node['kind'] == 'module':
            for field in ('purpose', 'modes', 'inputs', 'process', 'outputs', 'boundary', 'work'):
                if not node.get(field):
                    raise ValueError(f"missing module {field}: {node['id']}")
    seen, pending = set(), [root_id]
    while pending:
        uid = pending.pop()
        if uid in seen:
            raise ValueError(f'cycle: {uid}')
        seen.add(uid)
        pending.extend(children[uid])
    if seen != set(nodes):
        raise ValueError('disconnected hierarchy')
    if any(uid not in nodes for uid in aliases.values()):
        raise ValueError('invalid alias')
    return children


def describe(nodes, aliases, children, uid):
    node = resolve(nodes, aliases, uid)
    path, cursor = [], node
    while cursor:
        path.append(cursor['id'])
        cursor = nodes.get(cursor['parent'])
    links = {}
    backlinks = []
    for field in LINK_FIELDS:
        refs = node.get(field, [])
        if refs:
            links[field] = [resolve(nodes, aliases, r)['id']
                            for r in ([refs] if isinstance(refs, str) else refs)]
    for other in nodes.values():
        for field in LINK_FIELDS:
            refs = other.get(field, [])
            if any(aliases.get(r, r) == node['id'] for r in ([refs] if isinstance(refs, str) else refs)):
                backlinks.append({'from': other['id'], 'relation': field})
    return {**node, 'hierarchy': path[::-1], 'children': children[node['id']],
            'canonical_links': links, 'referenced_by': backlinks}


_PRIVATE_ID = re.compile(
    r'(?P<snapshot>LOOP-INV-[0-9]{8}-[0-9]+):(?P<repo>[0-9]+)'
    r'(?::(?P<section>[^:]+):(?P<position>[0-9]+))?'
)


def private_lookup(database, identifier):
    """Resolve a private key without creating or mutating the database."""
    match = _PRIVATE_ID.fullmatch(identifier)
    if not match:
        raise ValueError('expected SNAPSHOT:GITHUB_ID[:SECTION:POSITION]')
    key = (match['snapshot'], match['repo'])
    database = Path(database).resolve()
    with closing(sqlite3.connect(database.as_uri() + '?mode=ro', uri=True)) as con:
        if match['section'] is None:
            row = con.execute(
                'SELECT payload_json FROM repository WHERE snapshot_id=? AND github_id=?', key
            ).fetchone()
        else:
            row = con.execute(
                'SELECT payload_json FROM observation WHERE snapshot_id=? AND github_id=? AND section=? AND position=?',
                (*key, match['section'], int(match['position']))
            ).fetchone()
    if row is None:
        raise KeyError(identifier)
    return json.loads(row[0])


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    sub = cli.add_subparsers(dest='cmd', required=True)
    sub.add_parser('validate')
    show = sub.add_parser('show')
    show.add_argument('id')
    tree = sub.add_parser('tree')
    tree.add_argument('id', nargs='?')
    tree.add_argument('--depth', type=int, default=2)
    private = sub.add_parser('private')
    private.add_argument('database', type=Path)
    private.add_argument('id')
    args = cli.parse_args()
    try:
        if args.cmd == 'private':
            print(json.dumps(private_lookup(args.database, args.id), indent=2, ensure_ascii=False))
            return
        root_id, nodes, aliases = build(args.root)
        children = validate(args.root, root_id, nodes, aliases)
        if args.cmd == 'validate':
            print(f'{root_id}: {len(nodes)} nodes, {len(aliases)} aliases, valid')
        elif args.cmd == 'show':
            print(json.dumps(describe(nodes, aliases, children, args.id), indent=2, ensure_ascii=False))
        else:
            if args.depth < 0:
                raise ValueError('depth must be non-negative')
            uid = resolve(nodes, aliases, args.id or root_id)['id']
            pending = [(uid, 0)]
            while pending:
                current, depth = pending.pop()
                print(f'{"  " * depth}{current} — {nodes[current]["title"]}')
                if depth < args.depth:
                    pending.extend((child, depth + 1) for child in reversed(children[current]))
    except (OSError, ValueError, KeyError, sqlite3.Error) as exc:
        cli.exit(1, f'Registry: {exc}\n')


if __name__ == '__main__':
    main()
