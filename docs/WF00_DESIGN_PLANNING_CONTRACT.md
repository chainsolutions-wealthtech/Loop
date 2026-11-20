# Loop Engineering — Contrat de passage de la constitution documentaire à la planification

**Version 0.1 — 13 novembre 2026 — Proposition de conception à relire.**

**Projet concerné** — `chainsolutions-wealthtech/Loop`.

**Référence documentaire** — contenu de la PR #1 au commit `9db9727ddd6c9e6ead7c5dcaa44db8c6afad780e`. Ce document n'est ni une règle GitHub, ni un workflow exécutable, ni une décision adoptée.

## 1. Objet et frontières

Une instruction nouvelle n'est pas directement une tâche de développement. Loop la rattache à sa source, à l'état du projet et à ses décisions précédentes. Il produit ensuite des exigences et des modèles révisables. La planification reçoit un périmètre de conception suffisamment établi pour décomposer et ordonner les travaux. Elle ne tranche pas à la place de la conception.

**WF-00** constitue ou réconcilie le cadre documentaire. **Software Design** transforme le besoin en modèles et décisions de conception. **La planification** transforme un lot conçu en travaux dépendants et vérifiables. **L'exécution** est un cycle en aval, hors de cette version. Une entrée peut lancer un travail de clarification ou un plan conditionnel sans rendre une tâche de réalisation exécutable.

Ce contrat relie trois cycles pour la première tranche. Il ne fixe ni le nombre total de cycles de Loop ni leur nomenclature définitive. Les douze spécialités SD-01 à SD-12 restent des domaines mobilisables selon le besoin, pas douze étapes obligatoires.

## 2. Ce qui existe avant l'intention qualifiée

Le point de départ est une **entrée identifiée**. Elle peut être un brief, une instruction isolée, une source retrouvée, un changement demandé ou un point de reprise. L'entrée associe le dépôt ou projet visé, l'origine de la demande et le périmètre de travail connu. Si l'identité métier du projet n'est pas encore établie, elle reste à confirmer. La capture de l'instruction peut commencer sans attendre un cahier des charges complet.

`Entrée identifiée → source et instruction capturées → intention qualifiée → exigence proposée → conception → planification`

Une source et une instruction ne sont pas équivalentes. Un seul document peut contenir plusieurs instructions, et plusieurs instructions peuvent éclairer une même exigence. Le texte original reste à son emplacement autorisé. Le registre conserve sa référence, sa version, son emplacement précis si connu et les liens vers les objets qui en dérivent. Un contenu privé ne doit pas être dupliqué dans un dépôt public.

## 3. Trois cycles et leurs sorties

| Cycle | Déclencheur et entrées | Opérations et sortie | Condition de passage | Consommateur ou retour |
|---|---|---|---|---|
| **WF-00 — Constitution et coordination documentaire** | Première constitution, adoption d'un dépôt existant, reprise sans point fiable ou changement d'autorité. Identité, sources, état Git si disponible, documents et règles observés. | Inventorier, qualifier le mode, cartographier les autorités, rapprocher les documents des registres, consigner écarts et manques. Produire un **dossier de référence documentaire** et un checkpoint. | Les sources et autorités utiles au périmètre sont identifiées ou signalées comme inconnues. Chaque écart bloquant a un responsable à identifier ou désigné et une prochaine action. La publication ou l'installation du squelette reste une opération distincte. | Software Design pour le périmètre utilisable. Retour à l'inventaire pour une source non identifiée ou un conflit d'autorité. Une lacune locale ne bloque pas les sujets indépendants. |
| **Software Design — Conception** | Dossier documentaire utilisable sur le périmètre concerné, instruction versionnée et références du projet. En reprise, modèles et engagements antérieurs pertinents. | Qualifier intention et exigences, modéliser les comportements et interfaces concernés, arbitrer les options qui changent les contrats, relier exigences et critères de validation. Produire un **dossier de conception versionné** et une analyse d'impact. | Les exigences de la tranche ont des critères vérifiables. Les interfaces et décisions nécessaires au lot sont explicites. Les inconnues et désaccords restants sont qualifiés et leurs impacts visibles. Une décision non adoptée ne devient pas une contrainte. | Planification pour préparer les lots. Retour vers WF-00 pour un conflit de provenance ou d'autorité. Retour au domaine de conception concerné si une règle métier, un état, une interface ou un arbitrage manque. |
| **Planification — Lots, dépendances et vérification** | Dossier de conception versionné, périmètre et contraintes d'équipe ou de livraison connus. | Découper en lots livrables, identifier les travaux de clarification, ordonner les dépendances et préciser les critères de réception, les tests et les preuves attendues. Produire un **plan versionné** et des unités de travail identifiables. | Chaque unité de réalisation renvoie à une exigence ou à une décision du lot et à une vérification attendue. Les dépendances nécessaires sont identifiées. Le plan indique ce qui est conditionnel, bloqué ou prêt du point de vue de la conception. | L'exécution peut examiner les unités éligibles lorsque ses propres conditions sont remplies. Retour vers la conception si une dépendance révèle une interface ou un choix non résolu. |

Les passages sont évalués **par tranche**, sur la version des entrées utilisée. Ils n'exigent pas la clôture de tout le cahier des charges ni ne déclarent l'ensemble du projet prêt.

### Dossier de conception minimal par tranche

1. **Objectif, périmètre et hors périmètre**, liés aux instructions et au contexte retenu.
2. **Exigences versionnées**, règles métier et critères observables, avec statut explicite.
3. **Modèles affectés**, choisis selon le lot parmi parcours, domaine, données, interface, API, architecture, qualité ou exploitation. Pour un projet existant, distinguer l'observé de la cible.
4. **Décisions et options ouvertes**, avec justification, périmètre et effets sur les modèles. Les choix structurants peuvent être tracés dans un ADR.
5. **Analyse d'impact et de vérification**, dont les comportements à préserver et les scénarios d'échec pertinents.
6. **Prochaine action et blocages**, avec références vers les objets concernés.

Le chemin n'est pas un ordre rigide entre spécialités. Le besoin peut conduire du fonctionnel au domaine et à l'UX en parallèle. La conception de l'API peut ensuite révéler une règle métier oubliée. Dans ce cas, seule la partie dépendante revient en conception.

### Plan minimal par tranche

Pour chaque unité de travail, indiquer son objectif, son type (`clarification`, `conception`, `réalisation` ou `vérification`), ses références d'entrée versionnées, ses prédécesseurs, le résultat attendu et les preuves de réception. Le plan conserve les dépendances sous forme de graphe. Un cycle de dépendances entre tâches de réalisation doit être clarifié ou redécoupé avant de déclarer ces tâches prêtes. Les travaux non affectés par un blocage restent distincts.

## 4. Deux parcours, un contrat commun

| Question | Dépôt neuf ou projet nouveau | Projet existant ou adoption |
|---|---|---|
| **Qu'observer avant de créer ?** | Identité, objectif initial, sources hors dépôt, règles applicables et présence éventuelle d'un socle technique. Un README initial n'est pas la preuve d'un produit déjà conçu. | Branche et commit de référence, autorités, registres, décisions, modèles et travaux ouverts. Comparer les comportements observables aux intentions et documents pertinents. |
| **Que produire dans WF-00 ?** | Squelette minimal proposé et justifié, carte de responsabilités, registre de sources, premières zones à qualifier, point de reprise initial. | Inventaire et classification des éléments conservés, à relier, manquants ou contradictoires. Point de reprise aligné sur les éléments observés. |
| **Que reçoit Software Design ?** | Brief et premières exigences. Modèles candidats, sans technologie imposée ni faux état opérationnel. | Baseline existante, demande de changement, écarts, contraintes et décisions à préserver. |
| **Que planifier ?** | Une première tranche cohérente à concevoir, réaliser et vérifier, avec hypothèses explicites. | Un changement ciblé, les dépendances touchées et les scénarios de non-régression. Ne pas créer une deuxième baseline. |

## 5. Contrat de passage et reprise

Chaque passage transmet des **références**, pas une deuxième copie des autorités. Le format ci-dessous est un modèle conceptuel pour les deux transitions principales. Les valeurs en chevrons ne sont ni des identifiants adoptés ni un schéma validé.

```yaml
project_ref: "<identité du projet>"
continuity_ref: "<identité du chantier>"
source_cycle: "<WF-00 ou SOFTWARE_DESIGN>"
target_cycle: "<SOFTWARE_DESIGN ou PLANIFICATION>"
scope_ref: "<périmètre et version>"
reference_state:
  git_commit: "<SHA observé, ou null si aucun commit>"
  inputs: ["<objet@version>"]
outputs: ["<objet@version>"]
evidence_refs: ["<preuve ou décision référencée>"]
status: "<CANDIDAT, TRANSMISSIBLE, BLOQUÉ ou À_RÉCONCILIER>"
open_items:
  - ref: "<question, conflit ou lacune>"
    affects: ["<objet ou lot affecté>"]
    next_action: "<action vérifiable>"
checkpoint:
  last_verified_step: "<dernière opération attestée>"
  resume_cycle: "<cycle à reprendre>"
  next_action: "<action précise>"
```

- **CANDIDAT** signifie que la sortie est disponible pour examen, sans valeur d'autorisation.
- **TRANSMISSIBLE** signifie que le consommateur nommé peut utiliser cette version, pour le périmètre déclaré. Ce statut n'autorise ni un changement GitHub ni un déploiement.
- **BLOQUÉ** signifie qu'une condition identifiée empêche le passage du périmètre affecté. Une question ou une clarification peut être planifiée.
- **À_RÉCONCILIER** signifie que les références, une décision ou le périmètre ont changé depuis le dernier contrôle. Comparer les versions et réévaluer les objets dépendants avant d'utiliser la sortie.

**Règle de reprise.** Relire le checkpoint, comparer les versions déclarées aux sources d'autorité, identifier la première dépendance modifiée et réexaminer seulement ce qui en dépend. Conserver les versions et preuves antérieures. Une interruption n'est pas une raison de réinitialiser le registre ni de rejouer les opérations déjà attestées.

**Relations minimales proposées.** Une exigence `dérive_de` une instruction. Un modèle `satisfait` une exigence. Une décision `arbitre` un choix ou contraint un modèle. Une tâche `met_en_œuvre` une version de modèle ou d'exigence. Un test `vérifie` une exigence. Un objet peut `dépendre_de` ou `remplacer_la_version_de` un autre objet. Les noms et la représentation physique des registres ne sont pas figés ici.

## 6. Scénario fictif — Ajouter un téléchargement de facture

**État initial.** Un projet web existant permet à un client de consulter ses propres factures. L'équipe souhaite maintenant autoriser leur téléchargement en PDF. Les identifiants ci-dessous sont illustratifs.

| Moment | Décision du cycle | Trace attendue |
|---|---|---|
| WF-00 retrouve l'existant | Le dossier identifie l'exigence de consultation, le modèle de permissions et le test d'accès existant. | `INT-042` est capturée et liée à `REQ-017@v1`, qui reste inchangée. |
| La conception démarre | Le téléchargement devient `REQ-042@v1` en proposition. Le dossier identifie une question non résolue sur les statuts de facture éligibles. | Le contrat du téléchargement reste candidat. Les règles de consultation ne sont pas redéfinies. |
| La question est arbitrée | Dans ce scénario, la décision fictive `DEC-011` retient le téléchargement des factures émises uniquement, par leur propriétaire. | La règle et ses critères sont rattachés à la nouvelle version du modèle. Le point de reprise renvoie au contrat API et aux états de l'interface. |
| La planification reçoit le lot | Ordonner le travail sur l'autorisation serveur et le contrat, puis l'intégration de l'interface. Prévoir la vérification du parcours complet. | Tests attendus pour facture émise du propriétaire, facture d'un autre client, statut non éligible et consultation historique inchangée. |
| Une nouvelle décision arrive après le plan | Si le périmètre d'éligibilité change, réévaluer la règle, le contrat, les états UI et les travaux dépendants. | Passer ces éléments à `À_RÉCONCILIER`. Conserver les anciens résultats et ne pas redémarrer WF-00 si les autorités et sources n'ont pas changé. |

## 7. Vérifications d'acceptation de la conception

Ces scénarios sont à démontrer avant d'automatiser le contrat. Ils ne sont pas des tests du moteur déjà exécutés.

| Scénario | Résultat attendu |
|---|---|
| Projet neuf avec brief incomplet | Squelette et sources qualifiés. Les décisions absentes restent ouvertes. Aucun modèle cible n'est présenté comme existant. |
| Projet existant avec un registre déjà canonique | Rattacher les nouveaux objets à ce registre. Aucun deuxième registre concurrent, aucune perte de l'historique. |
| Deux sources de même portée se contredisent | Consigner les deux versions et isoler les travaux dépendants. Le plan peut proposer une clarification, pas choisir silencieusement. |
| Modification d'un modèle après création du plan | Identifier les tâches et preuves affectées, préserver les versions et réévaluer le lot avant exécution. |
| Reprise d'un chantier interrompu, entrées inchangées | Repartir à la prochaine opération indiquée. Aucun deuxième bootstrap et aucune réécriture de la première baseline. |
| Défaut générique constaté sur le pilote | Corriger la règle générique au bon niveau, ajouter le scénario de non-régression, puis reprendre au point affecté. |

## 8. Provenance, adoption et prochain point de travail

**Appuis propres à Loop** — [WF-00 proposé](https://github.com/chainsolutions-wealthtech/Loop/blob/9db9727ddd6c9e6ead7c5dcaa44db8c6afad780e/docs/WORKFLOW_WF00.md), [périmètre Software Design](https://github.com/chainsolutions-wealthtech/Loop/blob/9db9727ddd6c9e6ead7c5dcaa44db8c6afad780e/docs/SOFTWARE_DESIGN_SCOPE.md), [carte des autorités proposée](https://github.com/chainsolutions-wealthtech/Loop/blob/9db9727ddd6c9e6ead7c5dcaa44db8c6afad780e/SOURCE_OF_TRUTH.md).

**Précédents externes** — [reçu de bootstrap de Gouvern](https://github.com/Patricked-code/Gouvern/blob/4ad855c16e9e9058daf9ebd4aace8a105419b1d4/.governance/bootstrap-receipt.json), [programme et preuves de reprise](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/blob/9d8fd277dc113aacb2e171fbb6cde00bded982fd/docs/control-plane/PROGRAM.md), [PR #29, architecture et mémoire révisées](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/pull/29), [PR #55, séparation de la configuration et de l'autorité d'exécution](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/pull/55). Les exemples et contrats du présent document sont une adaptation à Loop, pas une copie ni une adoption des autorités externes.

**Point de reprise proposé** — construire la matrice `objet produit ↔ registre logique ↔ autorité ↔ version ↔ cycle consommateur` à partir des documents déjà proposés. Utiliser cette matrice pour préciser le squelette minimal de WF-00 et vérifier les deux parcours. Les noms de fichiers, le choix du stockage et l'orchestration restent ouverts. Aucun fichier, paramètre ni statut de la PR #1 n'a été changé pour produire cette proposition.
