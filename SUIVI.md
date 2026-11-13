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

## Module d'entrée d'un dépôt — candidat

- **Objet :** vérifier dépôt exact → reconnaissance → ID canonique → installation GitHub App → procédure versionnée avant admission.
- **Preuve :** tests unitaires hors ligne du noyau et de sa garde. Aucun raccordement MCP/CUG en service ni nouvelle autorité.
- **Point de reprise :** choisir l'hôte d'intégration et les sources autorisées, puis tester en lecture seule un dépôt reconnu et un inconnu. Voir [le contrat](docs/REPOSITORY_ENTRY.md).

## Découverte et rattachement d'un dépôt — candidat

- **Objet :** séparer la découverte en lecture, la préparation CUG, l'inscription par une autorité et la vérification d'un checkout.
- **Preuve :** scénarios hors ligne de reprise, réconciliation d'accès, réessai après inscription et comparaison du checkout.
- **Limites :** aucune installation, inscription ni association serveur exécutée.
- **Point de reprise :** identifier l'interface de reconnaissance et d'inscription autorisée, puis éprouver un dépôt connu et un inconnu sur des adaptateurs en lecture seule. Voir [le parcours](docs/REPOSITORY_ONBOARDING.md).

## Inventaire des usages MCP — candidat

- Périmètre initial observé : 45 dépôts visibles sur trois comptes, 44 arbres de branche par défaut lus et un dépôt vide.
- Module réutilisable : découverte GitHub paginée et classification indicative en lecture seule. Aucun workflow externe lancé.
- Relevé public et contrat : [Inventaire des usages MCP](docs/MCP_INVENTORY.md). Les détails privés ne sont pas publiés.
- Reprise : configurer les identités de lecture sur l'hôte, exécuter le CLI en contexte privé et examiner les candidats retenus. Aucun octroi de droits implicite.
