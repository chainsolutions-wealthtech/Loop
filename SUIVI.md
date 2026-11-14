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

## Fiches GitHub et carte des raccordements MCP — candidat

- Schéma v2 : une fiche par dépôt, inventaire des workflows et scripts, relations statiques sourcées, identités client et preuves serveur séparées.
- Échantillon privé du 13 novembre 2026 : 45 dépôts, 169 workflows lus et 1 104 fichiers lus. L'inventaire privé et les chemins serveur ne sont pas publiés ici.
- Le rapport n'attribue aucune autorisation et ne confirme pas les clients actifs. Les candidats GitRegistry ne sont pas des rattachements actifs.
- Point de reprise : vérifier les dispatchs dynamiques et les liaisons client à partir de preuves runtime autorisées. Voir [le contrat](docs/MCP_INVENTORY.md).

## Mémoire et registre de travail — candidat PR #2

- Référence de reprise : [mémoire du chantier](memory/README.md), [registre du travail](registry/work.json), [preuves](registry/evidence.json), [architecture](docs/LOOP_ARCHITECTURE.md) et [roadmap](docs/LOOP_ROADMAP.md).
- Instantané `LOOP-INV-20261113-02` : registre SQLite privé contrôlé et référencé, aucune donnée de dépôt privé ni chemin serveur publié ici.
- La revue des 11 sites distingue 5 cibles résolues statiquement, 2 entrées proxy, 2 tests et 2 moteurs à corréler avec un paquet. Aucun appel externe n'a été déclenché.
- Reprise : poursuivre LOOP-W09 et LOOP-W10 en lecture seule. LOOP-W11 attend une preuve nominative CUG et une autorité de reconnaissance. Ni fusion, ni déploiement.

## Identité et continuité de Loop — PR #2

- Projet : `WT-PROJECT-LOOP-001` ; dépôt `LOOP-REPO-1456075212`.
- Continuité : `LOOP-CONV-CONT-20261113-ROOT-01` ; checkpoint `LOOP-CP-20261113-002`.
- [Entrée canonique](docs/LOOP_CANONICAL_REGISTRY.md) et [contrats des modules](registry/modules.json).
- Reprendre LOOP-W09 et LOOP-W10 en lecture seule. LOOP-W11 reste bloqué par la preuve de reconnaissance et l'identité CUG. Ces identifiants n'autorisent ni fusion, ni déploiement, ni action externe.

## Test d’entrée Stablecoin et ancrage global — 13 novembre 2026

- LOOP-W15 est vérifié dans la branche de travail. Le checkout S2 de Stablecoin
  est observé, mais l’entrée retourne `mcp_unverified`. Aucun appel métier.
- L’ID global Loop est résolu par son dépôt GitHub. La réciproque par serveur
  et chemin est testée sur données fictives. Aucun chemin privé ni ancrage
  actif n'est ajouté côté serveur.
- LOOP-W11 reste bloqué. Obtenir une réponse de l’autorité sur le dépôt exact,
  puis une preuve nominative CUG, la procédure approuvée et les preuves
  privées pour chaque répertoire. Voir [le test](docs/PROJECT_ANCHOR.md).

## Extraction du parcours historique MCP vers Loop — 13 novembre 2026

- `LOOP-W16` documenté et lié à `LOOP-CAP-006`, avec les preuves
  `EV-017` et `EV-018`. Le GitRegistry runtime reste V1 au relevé.
- Le [contrat](docs/WORKFLOW_REPOSITORY_HOSTING.md) distingue découverte,
  rattachement, provisionnement et déploiement applicatif. Le chemin
  restant est le routage hors ligne, puis la validation de l’adaptateur
  de lecture. Aucun changement MCP, Regulatory, S1 ou S2.

## Planificateur d’hébergement appelable dans Loop

- `LOOP-W17` vérifié hors ligne. Point d’appel
  `loop.repository_hosting.plan_repository_hosting`.
- `LOOP-CAP-006` compose les identifiants et l’index d’ancrage existants.
  Les retours ne donnent aucun droit d’écriture ni de déploiement.
- Reprise de cette capacité : tester l’adaptateur de lecture séparément,
  sans convertir une observation indisponible en absence.

## Jonction GitRegistry vers Governed Deploy Application

`LOOP-W18` décrit le raccordement à l’arrivée ou en préflight applicatif.
`EV-020` consigne le dry run runtime V1→V2 sans écriture et la différence
entre mapping proposé et chemin attesté. Le planificateur est appelable,
mais le raccordement automatique n’est pas implémenté. Voir le
[relevé et la séquence](docs/WORKFLOW_REPOSITORY_HOSTING.md#jonction-vérifiée-et-point-dappel-du-workflow).

## Précédents GRT, Gouvern, UAES et Regulatory — LOOP-W18

Les [preuves et limites](docs/REPOSITORY_LIFECYCLE_PRECEDENTS.md) sont indexées sous EV-021 à EV-026
et dans la chronologie E20 à E25. Le parcours global débute à l'identification
du dépôt. Reprendre par un adaptateur de lecture testé sur lien vérifié,
répertoire existant sans lien et registre non concluant. La mise en service
exige plus tard la cible relue et une révision exacte. Aucun déploiement
ni raccordement automatique n'a été réalisé dans ce lot documentaire.

## Carte de reprise du fil — LOOP-W18

Depuis `LOOP-CONV-CONT-20261113-ROOT-01`, ouvrir la [carte du cycle](docs/REPOSITORY_LIFECYCLE_MAP.md).
Les E26 à E28 indexent la correction du déclencheur, les capacités et les
limites de la mémoire. Prochaine action du sujet inchangée : tester
l'adaptateur de lecture sur lien attesté, répertoire existant sans lien
actif et vue non concluante. Aucun raccordement ni déploiement dans ce lot.

## Contrat de création gouvernée de dépôt — LOOP-W19

Le [contrat candidat](docs/GOVERNED_REPOSITORY_CREATION_CONTRACT.md) isole `CREATE_NEW_REPOSITORY`
et le bootstrap automatique jusqu'à `HANDOFF_READY`, indépendamment du
lieu d'exécution. L'entrée locale et `LOCAL_HANDOFF_READY` restent en aval.
Rejeu hors ligne `EV-027` sur l'exécuteur GRT épinglé : deux tests réussis.
La reprise après 409 ne fait qu'un POST dans ce scénario. Le manifeste
actuel ne suffit pas à relier un dépôt homonyme à la même demande.

Reprise propre à cette tranche : définir et tester l'adaptateur de
corrélation durable avant d'exposer une exécution réelle. Le checkpoint
global et `LOOP-W18` restent inchangés. Aucun outil MCP déployé.

## Capsule indépendante de création gouvernée — LOOP-W20

Le [noyau portable](capsules/governed_repository_creation/README.md)
implémente soumission, consultation, reprise, réservation atomique et
reçu `HANDOFF_READY`. Les tests `EV-028` couvrent les résultats
incertains, la concurrence, la corrélation et les preuves de remise.
Le dépôt GRT, le MCP, les serveurs, le checkpoint global et `LOOP-W18`
ne changent pas.

Reprise : choisir et qualifier un adaptateur d'exécution sur une cible
isolée. Vérifier l'identité GitHub et la preuve de corrélation sans
modifier GRT. Exposer ensuite le noyau comme outil si le test réel
est concluant. L'hôte MCP et l'identité App restent des choix séparés.
