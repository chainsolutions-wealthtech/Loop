# Feuille de route de Loop

Périmètre : `chainsolutions-wealthtech/Loop`. Le
[registre du travail](../registry/work.json) conserve l'état, les dépendances
et les critères de chaque unité. L'ordre ci-dessous n'empêche pas
l'avancement d'une unité indépendante en lecture seule.

| Lot | Unités | État et sortie attendue |
|---|---|---|
| 0 — Fondations | LOOP-W01, LOOP-W02 | PR de fondation en revue. Corpus historique partiel à qualifier. |
| 1 — Constitution, conception, planification | LOOP-W03, LOOP-W13 | Contrats documentés. Préparer un premier lot vérifiable, sans lancer l'orchestrateur. |
| 2 — Entrée, découverte et inventaire | LOOP-W04 à LOOP-W07 | Modules candidats avec tests. Fiches et relations au SHA observé. |
| 3 — Mémoire et registre | LOOP-W08 | Chronologie et index Git publics. SQLite privé historisé, contrôlé et référencé. |
| 4 — Vérifier les liens MCP | LOOP-W09, LOOP-W10, LOOP-W11 | Résoudre les dispatchs prouvables, distinguer exécutions et bootstrap, obtenir la preuve CUG et l'autorité de reconnaissance. |
| 5 — Brancher et valider l'hôte | LOOP-W12 | Conditionnel. Intégration Loop et relances en lecture, aucune activation implicite. |

## Reprise immédiate

Continuer **LOOP-W09** à partir de la [revue des onze dispatchs](../registry/dispatch-review.json). Cinq cibles de code sont résolues, deux sites sont des entrées proxy, deux sont des tests et deux moteurs exigent encore leur paquet d'exécution. Vérifier les preuves autorisées correspondantes, puis élargir la couverture des branches utiles.

Poursuivre **LOOP-W10** en parallèle des lectures indépendantes. Les preuves
existantes montrent un bootstrap ou un plan, pas la connexion effective.
Chercher une trace autorisée reliant dépôt, client, action et révision.
Ne pas déclencher de workflow ni utiliser de session d'un autre projet pour
combler un manque de preuve.

**LOOP-W11** reste bloqué tant que l'identité CUG et l'autorité de
reconnaissance relisible ne sont pas établies. Une cible S1 déclarée,
un projet candidat et la couverture d'une autre App ne débloquent pas ce lot.

Les actions d'écriture externes, l'installation d'une App, un déploiement ou
une fusion ne font pas partie de cette feuille de route exécutable.

**LOOP-W14** complète le lot 3 avec l'[identité canonique et l'arbre de reprise](LOOP_CANONICAL_REGISTRY.md). Il ne remplace ni LOOP-W09/W10, ni leurs preuves opérationnelles manquantes.

**LOOP-W15 — Ancrage global** est préparé et testé dans la branche de travail.
La lecture du registre privé faisant autorité, la vérification de CUG et
l’attestation de chaque répertoire sont les prérequis d'un premier passage
réel. La persistance côté serveur reste distincte de la projection Git.
Voir [le contrat d’ancrage et le test Stablecoin](PROJECT_ANCHOR.md).
