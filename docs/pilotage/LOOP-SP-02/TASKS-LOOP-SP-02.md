# Registre des tâches — LOOP-SP-02 — Entrée, découverte et rattachement

**Dépôt** `chainsolutions-wealthtech/Loop` · **Projet** `WT-PROJECT-LOOP-001` · **Niveau** sous-projet · **Périmètre** `LOOP-SP-02`

**Continuité projet** `LOOP-CONV-CONT-20261113-ROOT-01` · **État documentaire** candidat PR #2

[Suivi de ce périmètre](SUIVI-LOOP-SP-02.md) · [Table de pilotage](../README.md) · [Suivi parent](../WT-PROJECT-LOOP-001/SUIVI-WT-PROJECT-LOOP-001.md)

## Travaux rattachés à ce périmètre

| Unité | Objet | État dans le registre | Dépendances | Preuves |
|---|---|---|---|---|
| LOOP-W04 | Contrôle d'entrée dépôt et procédure | draft_verified | — | EV-011 |
| LOOP-W05 | Planifier découverte, CUG et rattachement | draft_verified | LOOP-W04 | EV-011, EV-005 |
| LOOP-W15 | Tester l’entrée sur Stablecoin et modéliser l’ancrage global | draft_verified | LOOP-W14 | EV-015, EV-016 |
| LOOP-W16 | Isoler le parcours de rattachement et d’hébergement applicatif | documented | LOOP-W15 | EV-017, EV-018 |
| LOOP-W17 | Implémenter et vérifier le planificateur portable de rattachement | draft_verified | LOOP-W16 | EV-019 |
| LOOP-W18 | Raccorder l’arrivée et le préflight applicatif au planificateur d’hébergement | conditional | LOOP-W17 | EV-020, EV-021, EV-022, EV-023, EV-024, EV-025, EV-026 |
| LOOP-W19 | Spécifier et rejouer la création gouvernée jusqu’à HANDOFF_READY | draft_verified | — | EV-021, EV-027 |
| LOOP-W20 | Implémenter la capsule autonome de création gouvernée | draft_verified | LOOP-W19 | EV-028 |
| LOOP-W21 | Relier la capsule à un préflight GitHub Apps nominatif | draft_verified | LOOP-W20 | EV-029 |
| LOOP-W22 | Projeter le questionnaire GRT et journaliser la préparation web | draft_verified | LOOP-W19 | EV-030 |
| LOOP-W23 | Joindre la demande préparée à l’identité GitHub et au préflight CUG | draft_verified | LOOP-W21, LOOP-W22 | EV-031 |
| LOOP-W24 | Enregistrer les réponses groupées dans Loop | draft_verified | LOOP-W22, LOOP-W23 | EV-032 |

Le registre JSON fait référence pour les états structurés et les dépendances.
En cas d’écart avec cette vue, réconcilier à partir des preuves plutôt que
de déclarer une tâche terminée.

[work.json](../../../registry/work.json) · [evidence.json](../../../registry/evidence.json)
