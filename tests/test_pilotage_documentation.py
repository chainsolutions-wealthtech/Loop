"""Check the linked Markdown control files without changing runtime behaviour."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PILOTAGE = ROOT / "docs" / "pilotage"
TYPES = {
    "SUIVI", "MEMOIRE-CANONIQUE", "INTENTIONS", "CONCEPTION", "ARCHITECTURE",
    "CARTOGRAPHIE", "DECISIONS", "ROADMAP", "TODO", "TASKS", "MISE-EN-PRODUCTION",
}


def link_targets(path):
    text = path.read_text(encoding="utf-8")
    for url in re.findall(r"\]\(([^)]+)\)", text):
        target = url.split("#", 1)[0]
        if target and "://" not in target:
            yield (path.parent / target).resolve()


class PilotageDocumentationTest(unittest.TestCase):
    def setUp(self):
        self.identity = json.loads((ROOT / "registry" / "identity.json").read_text())
        self.subjects = json.loads((ROOT / "registry" / "subjects.json").read_text())
        self.project = self.identity["project_id"]
        self.parents = {key: self.project for key, _, _ in self.subjects["subprojects"]}
        self.topics = {key: parent for key, parent, _, _ in self.subjects["topics"]}

    def test_project_and_every_subproject_have_a_scoped_dossier(self):
        actual = {p.name for p in PILOTAGE.iterdir() if p.is_dir()}
        self.assertTrue({self.project, *self.parents} <= actual)
        self.assertTrue(actual <= {self.project, *self.parents, *self.topics})
        self.assertIn("LOOP-SUJ-020", actual)
        self.assertIn((PILOTAGE / "README.md").resolve(), link_targets(ROOT / self.identity["continuity"]["record"]))
        for scope in actual:
            with self.subTest(scope=scope):
                folder = PILOTAGE / scope
                docs = {folder / f"{kind}-{scope}.md" for kind in TYPES}
                self.assertTrue(docs <= set(folder.glob("*.md")))
                followup = folder / f"SUIVI-{scope}.md"
                self.assertTrue(docs - {followup} <= set(link_targets(followup)))
                self.assertIn(followup, link_targets(PILOTAGE / "README.md"))
                parent = self.parents.get(scope) or self.topics.get(scope)
                if parent:
                    parent_followup = PILOTAGE / parent / f"SUIVI-{parent}.md"
                    self.assertIn(parent_followup, link_targets(followup))
                    self.assertIn(followup, link_targets(parent_followup))
                for path in docs:
                    content = path.read_text(encoding="utf-8")
                    self.assertIn(f"`{scope}`", content)
                    self.assertIn(f"`{self.identity['repository']['full_name']}`", content)
                    self.assertIn(f"`{self.identity['continuity']['id']}`", content)

    def test_links_resolve_within_the_same_repository(self):
        for path in PILOTAGE.rglob("*.md"):
            for target in link_targets(path):
                with self.subTest(path=path.relative_to(ROOT), target=target):
                    self.assertTrue(target.is_relative_to(ROOT))
                    self.assertTrue(target.is_file())
