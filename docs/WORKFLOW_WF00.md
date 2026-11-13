# WF-00 — Constitution et coordination documentaire

> **Statut : spécification candidate ; aucun orchestrateur exécutant ce workflow n'est installé.**

## Finalité

Concevoir l'organisation documentaire d'un projet avant de développer le code. Ce workflow est réutilisable pour les dépôts vides et les projets existants.

## Entrées

- Identité du dépôt/projet et SHA de référence si existant.
- Instructions brutes, sources historiques, fichiers et registres détectés.
- Contraintes métier et exigences de gouvernance connues.

## Opérations proposées

1. Inventorier les sources avec dates, provenance et portée.
2. Déterminer le mode : nouveau dépôt ou reprise de projet existant.
3. Classer les sources, documents, modèles, registres, autorités et artefacts dérivés.
4. Identifier les doublons, conflits, dépendances et règles déjà en place.
5. Définir la taxonomie et la matrice de registres (sans créer de doublons).
6. Proposer les documents nécessaires et leurs emplacements.
7. Définir les relations : dépendance, production, validation, autorité, version, reprise.
8. Soumettre les contradictions et créations structurantes à arbitrage.
9. Installer uniquement les éléments approuvés.
10. Tester l'intégrité et enregistrer le point de reprise.

## Sorties

Inventaire sourcé, carte d'autorité, taxonomie, matrice registres↔documents, graphe de relations, décisions, plans de création et checkpoint.

## Règles

- Aucun nom de document n'acquiert automatiquement une autorité.
- Pas de suppression ni remplacement silencieux.
- Une source historique n'atteste pas à elle seule l'état opérationnel actuel.
- Toute dérivation doit conserver sa provenance.
