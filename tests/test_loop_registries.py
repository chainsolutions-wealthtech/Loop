import json
from pathlib import Path
import unittest

from loop.canonical_registry import build, resolve


ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


class LoopRegistryTest(unittest.TestCase):
    def test_requirements_work_and_evidence_references(self):
        registry = load('registry/work.json')
        proof = load('registry/evidence.json')['evidence']
        _, nodes, aliases = build(ROOT)
        requirements = {r['id'] for r in registry['requirements']}
        proof_ids = {p['id'] for p in proof}
        work_ids = {w['id'] for w in registry['work']}
        self.assertEqual(len(proof_ids), len(proof))
        self.assertEqual(len(work_ids), len(registry['work']))
        self.assertEqual(len(requirements), len(registry['requirements']))
        for req in registry['requirements']:
            for e in req['events']:
                self.assertEqual(resolve(nodes, aliases, e)['kind'], 'event')
        graph = {}
        for work in registry['work']:
            self.assertIn(work['state'], registry['states'])
            self.assertTrue(set(work['requirements']) <= requirements)
            self.assertTrue(set(work['evidence']) <= proof_ids)
            self.assertTrue(set(work['depends_on']) <= work_ids)
            graph[work['id']] = work['depends_on']
        done = set()
        while pending := work_ids - done:
            ready = {key for key in pending if set(graph[key]) <= done}
            self.assertTrue(ready, 'work dependency cycle')
            done |= ready

    def test_private_snapshot_index_and_dispatch_counts_match(self):
        proof = {p['id']: p for p in load('registry/evidence.json')['evidence']}
        review = load('registry/dispatch-review.json')
        self.assertEqual(review['snapshot_id'], proof['EV-003']['reference'])
        self.assertEqual(proof['EV-003']['storage'], 'private')
        self.assertEqual(len(review['sites']), proof['EV-003']['counts']['generic_dispatch_sites'])
        self.assertEqual(len({site['id'] for site in review['sites']}), len(review['sites']))
        for site in review['sites']:
            self.assertFalse(site['execution_attested'])
            self.assertIn(site['sha'], site['reference'])
            self.assertEqual(bool(site['tools']), site['status'] == 'static_resolved')

    def test_public_projection_counts_without_private_details(self):
        public = load('registry/public-repositories.json')
        self.assertEqual(public['visibility'], 'public_only')
        rows = public['repositories']
        proof = {x['id']: x for x in load('registry/evidence.json')['evidence']}
        self.assertEqual(len(rows) + public['private_repository_count'],
                         proof['EV-003']['counts']['repositories'])
        self.assertEqual(len(rows), len({row['github_id'] for row in rows}))
        for row in rows:
            self.assertEqual(set(row), {'github_id', 'repository', 'account', 'url',
                                        'branch', 'sha', 'coverage', 'counts'})
