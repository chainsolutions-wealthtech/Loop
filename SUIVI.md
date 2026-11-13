# Suivi et continuité — Loop

## POINT DE REPRISE COURANT

- **Projet :** `chainsolutions-wealthtech/Loop`
- **Date de fondation :** 2026-11-13 (Europe/Paris).
- **Référence d'audit local :** `AUDIT-LOOP-20261113-001` (rapport hors dépôt).
- **État initial vérifié :** dépôt vide, aucune branche/commit avant la fondation.
- **Premier commit main :** `07a35de18de9bbe46022aa87eaafe1ed1898350a` — README initial.
- **Branche de préparation :** `bootstrap/governance-setup-20261113`.
- **Objectif :** paramétrage documentaire et CI du dépôt AVANT installation du moteur Software Design.
- **Limites :** protections GitHub/rulesets non activées par ces fichiers ; elles nécessitent une opération d'administration séparée.
- **Pull Request de configuration :** [#1 (Draft)](https://github.com/chainsolutions-wealthtech/Loop/pull/1), non fusionnée.
- **Contrôle CI initial :** GitHub Actions `structure-and-policy` SUCCESS, exécution #43356722778 sur la branche avant mise à jour de ce checkpoint.
- **Protection de main :** `protected: false` dans la liste des branches ; zéro ruleset de dépôt retournée, activation nécessaire dans GitHub Settings.
- **Prochaine action :** activer/vérifier la ruleset de main, revérifier la CI, réviser puis approuver explicitement la PR ; établir le registre historique exhaustif avant d'installer le kit v0.1.
- **Interdictions :** pas d'action sur `Patricked-code/MCP`, pas de fusion non approuvée, pas de déploiement.

## Chantiers

| ID | Objet | État |
|---|---|---|
| LOOP-P0 | Audit initial dépôt | fait en lecture seule |
| LOOP-P1 | Constitution du registre historique | à démarrer |
| LOOP-P2 | Coordination documentaire et taxonomie WF-00 | conception requise |
| LOOP-P3 | Méthodologie Software Design | conception requise |
| LOOP-SETUP-01 | Fondation GitHub / docs / contrôle CI | PR #1 Draft, CI initiale PASS, protections à configurer |
| LOOP-P4+ | Architecture moteur puis intégration | bloqué par P1–P3 |

## Journal des décisions

- D-BOOT-01 (proposée) : constituer `Loop` comme dépôt source autonome du système.
- D-BOOT-02 (proposée) : ne pas installer le prototype v0.1 avant la gouvernance documentaire.
- D-BOOT-03 (proposée) : tout changement ultérieur sur branche et PR, sans fusion automatique.

Les décisions « proposées » ne constituent pas une approbation. Mettre à jour ce document après revue de la PR et vérification des paramètres GitHub.
