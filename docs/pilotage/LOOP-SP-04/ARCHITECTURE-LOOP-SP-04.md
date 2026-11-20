# Architecture — LOOP-SP-04 — Mémoire, registres et continuité

**Dépôt** `chainsolutions-wealthtech/Loop` · **Projet** `WT-PROJECT-LOOP-001` · **Niveau** sous-projet · **Périmètre** `LOOP-SP-04`

**Continuité projet** `LOOP-CONV-CONT-20261113-ROOT-01` · **État documentaire** candidat PR #2

[Suivi de ce périmètre](SUIVI-LOOP-SP-04.md) · [Table de pilotage](../README.md) · [Suivi parent](../WT-PROJECT-LOOP-001/SUIVI-WT-PROJECT-LOOP-001.md)

## Responsabilités et frontières

La mémoire locale du périmètre référence les chronologies et preuves communes. Les données privées sont adressées par référence dans leur stockage autorisé.

## État observé et état cible

Le registre d’identité, les chronologies, l’arbre canonique et les index de preuves sont déjà en place sur la branche. Ils ne prouvent pas une centralisation des journaux locaux.

Les références de conception décrivent les composants et leur contrat.
Le suivi indique l’état du chantier. Seule une attestation permet de
qualifier l’état du service installé.

## Documents techniques reliés

- [README.md](../../../memory/README.md)
- [README.md](../../../registry/README.md)
- [identity.json](../../../registry/identity.json)
- [LOOP_CANONICAL_REGISTRY.md](../../LOOP_CANONICAL_REGISTRY.md)
