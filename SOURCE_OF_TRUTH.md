# Carte des autorités — Loop Engineering

> **Statut : initial / proposé.** Il s'agit d'un plan d'autorité, non d'une approbation automatique des documents historiques.

## Autorités locales proposées

| Objet | Emplacement | Rôle | Statut |
|---|---|---|---|
| Présentation | README.md | Introduction, non normative | initial |
| Principes de gouvernance | GOVERNANCE.md | Règles du dépôt après adoption | proposé |
| Carte des autorités | SOURCE_OF_TRUTH.md | Périmètres et liens entre autorités | proposé |
| Instructions agents | AGENTS.md | Parcours d'entrée des agents | proposé |
| Continuité | SUIVI.md | État, preuves, prochaine action | initial |
| Sources historiques | docs/SOURCE_REGISTER.md | Inventaire/provenance, **pas autorité par défaut** | à qualifier |
| Méthode Software Design | docs/SOFTWARE_DESIGN_SCOPE.md | Hypothèses de périmètre et modèles | proposé |
| Configuration GitHub | .github/ | Workflows et modèles de contribution | à valider dans une PR |

## Règles de résolution

- Une **source brute** fait foi pour ce qu'elle énonce, pas pour l'état courant d'un système.
- Un **modèle approuvé et versionné** fait foi pour les décisions de son périmètre, sous réserve de décisions ultérieures explicites.
- Le **code à un SHA identifié** décrit l'implémentation, pas nécessairement la conformité au besoin.
- Les **registres dérivés** ne supplantent jamais une décision approuvée.
- Un conflit entre autorités est **bloquant pour l'action concernée** jusqu'à résolution documentée.
- Les documents de `Patricked-code/MCP` restent des **références historiques externes** : aucune importation ni autorité croisée implicite.

## Processus de révision

Toute promotion d'une source ou d'un modèle au rang d'autorité requiert : provenance, périmètre, justification, version/commit, décision, revue d'impact et inscription dans SUIVI.md. Les versions précédentes restent traçables.
