# Parcours d'entrée des agents — Loop

> Applicable uniquement au dépôt `chainsolutions-wealthtech/Loop`. Ne remplace pas les politiques supérieures applicables à l'agent.

## Lecture initiale

1. README.md — nature du projet.
2. GOVERNANCE.md — règles, limites, interdictions.
3. SOURCE_OF_TRUTH.md — carte des autorités et de leur statut.
4. SUIVI.md — checkpoint et prochaine action.
5. docs/SOURCE_REGISTER.md — sources et degré de vérification.
6. docs/SOFTWARE_DESIGN_SCOPE.md — périmètre provisoire du spécialiste.
7. Documents du chantier concerné, puis code et tests existants.

## Avant de travailler

- Identifier explicitement le dépôt, la branche, le commit SHA et l'objectif de l'intervention.
- Distinguer le **projet Loop** du **moteur Loop comme outil** appliqué à un dépôt externe.
- Distinguer un dépôt nouveau d'une reprise de dépôt existant.
- Faire l'inventaire des documents et mécanismes existants avant de proposer de nouveaux fichiers.
- Enregistrer les contradictions, limites de preuve et risques, sans les résoudre par une supposition.
- Ne pas installer, supprimer, migrer ou déployer implicitement.
- Proposer une modification minimale et des tests vérifiables.

## Après travail

Présenter l'état avant/après, les chemins modifiés, le SHA/PR, les contrôles réellement exécutés, les limites, les décisions en attente et un point de reprise exact. Ne pas déclarer une règle « active » si elle n'existe que dans la documentation.

## Reprise du chantier de la PR #2

Après le checkpoint, lire [la mémoire du chantier](memory/README.md) et [la roadmap](docs/LOOP_ROADMAP.md). Les décisions et preuves du registre sont bornées à leur périmètre. Ne jamais publier les instantanés privés dans ce dépôt public.

Pour une reprise par ID, lire [l'entrée canonique](docs/LOOP_CANONICAL_REGISTRY.md) et résoudre `LOOP-CONV-CONT-20261113-ROOT-01`. Cette référence ne remplace pas les vérifications d'autorité et de périmètre.
