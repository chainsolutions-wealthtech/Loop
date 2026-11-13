#!/usr/bin/env python3
"""Contrôle minimal de structure du dépôt Loop (stdlib uniquement).

Un succès ne certifie ni la sécurité ni la cohérence totale du référentiel.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = (
    "README.md",
    "GOVERNANCE.md",
    "SOURCE_OF_TRUTH.md",
    "AGENTS.md",
    "SUIVI.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "docs/SOURCE_REGISTER.md",
    "docs/SOFTWARE_DESIGN_SCOPE.md",
    "docs/REPOSITORY_CONFIGURATION.md",
    "docs/WORKFLOW_WF00.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/governance.yml",
)

def main() -> int:
    failures: list[str] = []
    for rel in REQUIRED:
        path = ROOT / rel
        if not path.is_file():
            failures.append(f"Fichier absent : {rel}")
            continue
        data = path.read_text(encoding="utf-8")
        if not data.strip():
            failures.append(f"Fichier vide : {rel}")
        if "<<<<<<< HEAD" in data or ">>>>>>> " in data:
            failures.append(f"Marqueur de conflit : {rel}")
    if failures:
        for failure in failures:
            print("FAIL:", failure)
        return 1
    print(f"PASS: {len(REQUIRED)} fichiers de configuration présents et non vides.")
    print("Attention : contrôle documentaire partiel, pas un audit de sécurité.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
