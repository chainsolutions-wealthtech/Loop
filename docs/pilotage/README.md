# Pilotage documentaire de Loop

**Dépôt** `chainsolutions-wealthtech/Loop` · **Projet** `WT-PROJECT-LOOP-001`  
**Continuité** `LOOP-CONV-CONT-20261113-ROOT-01` · **Périmètre** PR #2, candidat à l’adoption

Commencer à la racine par [SUIVI.md](../../SUIVI.md). Le suivi global
renvoie à chaque sous-projet, puis à ses sujets et travaux. La même
convention s’applique à tout nouveau projet ou sous-projet de Loop.
Les projets externes ne sont pas modifiés par cette organisation.

| Périmètre | Objet | Points d’entrée |
|---|---|---|
| `WT-PROJECT-LOOP-001` | Loop Engineering | [Suivi](WT-PROJECT-LOOP-001/SUIVI-WT-PROJECT-LOOP-001.md) · [Mémoire](WT-PROJECT-LOOP-001/MEMOIRE-CANONIQUE-WT-PROJECT-LOOP-001.md) |
| `LOOP-SP-01` | Fondations et gouvernance | [Suivi](LOOP-SP-01/SUIVI-LOOP-SP-01.md) · [Mémoire](LOOP-SP-01/MEMOIRE-CANONIQUE-LOOP-SP-01.md) |
| `LOOP-SP-02` | Entrée, découverte et rattachement | [Suivi](LOOP-SP-02/SUIVI-LOOP-SP-02.md) · [Mémoire](LOOP-SP-02/MEMOIRE-CANONIQUE-LOOP-SP-02.md) |
| `LOOP-SP-03` | Inventaire GitHub et cartographie MCP | [Suivi](LOOP-SP-03/SUIVI-LOOP-SP-03.md) · [Mémoire](LOOP-SP-03/MEMOIRE-CANONIQUE-LOOP-SP-03.md) |
| `LOOP-SP-04` | Mémoire, registres et continuité | [Suivi](LOOP-SP-04/SUIVI-LOOP-SP-04.md) · [Mémoire](LOOP-SP-04/MEMOIRE-CANONIQUE-LOOP-SP-04.md) |
| `LOOP-SP-05` | Constitution, conception et planification | [Suivi](LOOP-SP-05/SUIVI-LOOP-SP-05.md) · [Mémoire](LOOP-SP-05/MEMOIRE-CANONIQUE-LOOP-SP-05.md) |
| `LOOP-SP-06` | Vérification, intégration et passage à l'exécution | [Suivi](LOOP-SP-06/SUIVI-LOOP-SP-06.md) · [Mémoire](LOOP-SP-06/MEMOIRE-CANONIQUE-LOOP-SP-06.md) |
| `LOOP-SUJ-020` | Rattachement et préparation d’un hébergement applicatif | [Suivi](LOOP-SUJ-020/SUIVI-LOOP-SUJ-020.md) · [Mémoire](LOOP-SUJ-020/MEMOIRE-CANONIQUE-LOOP-SUJ-020.md) |

## Du besoin à la mise en production

| Étape | Entrée principale | Sortie qui permet la suite |
|---|---|---|
| 00 — Identifier et constituer | Dépôt neuf ou existant, identité, sources, état Git et autorité | Dossier de référence WF-00, écarts et point de reprise identifiés. |
| 01 — Capter et qualifier | Instruction et contexte datés | Intentions, exigences et critères observables, avec provenance. |
| 02 — Concevoir et arbitrer | Exigences et baseline du lot | Conception, cartographie, architecture, décisions et analyse d’impact versionnées. |
| 03 — Planifier et ordonner | Lot conçu et décisions applicables | Roadmap, tâches, dépendances, tests et conditions de réception. |
| 04 — Réaliser et vérifier | Tâche éligible et contrat de validation | Résultat, tests et non-régression, références exactes et écarts résiduels. |
| 05 — Préparer et décider | Lot vérifié, révision et cible exactes | Revue, droits et preuves nécessaires, décision de passage et plan de retour. |
| 06 — Mettre en service et attester | Passage admis pour le périmètre | Preuve de livraison, recette après publication et alignement constaté. |
| 07 — Réconcilier et reprendre | Preuves et résultats du cycle | Mémoire à jour, décision et prochain checkpoint. Retour ciblé si une entrée est révisée. |

Cet ordre est une extension documentaire de pilotage du projet. Il ne
renumérote pas les cycles historiques de Loop Engineering. Il s’applique
par lot, pas comme un verrou global. Une absence d’autorité, d’entrée ou
de preuve bloque seulement le passage qu’elle concerne. Les sorties ne
sont pas des autorisations implicites.

## Nommage, rôles et mise à jour

Le nom est `TYPE-ID.md`, par exemple `SUIVI-LOOP-SP-02.md`. L’ID stable
ne dépend pas du libellé métier. Chaque fichier indique dépôt, projet,
périmètre et continuité. Chaque suivi relie la mémoire, les intentions,
la conception, l’architecture, la cartographie, les décisions, la roadmap,
les actions, les tâches et la mise en production.

La mémoire de chaque périmètre indexe ses propres faits. Les chronologies
communes et les registres d’identité, d’exigences, de travaux et de preuves
restent uniques. Un contrat ou une preuve réutilisés sont référencés,
pas transformés en deuxième source. Les journaux locaux et les données
privées ne sont pas recopiés dans le dépôt public.

Quand un jalon change, relever la source et la preuve, qualifier le nouvel
état, mettre à jour le suivi du bon périmètre, puis ajuster sa mémoire et
les références concernées. Le parent renvoie au suivi enfant. Ne pas
confondre un résultat attesté dans un dossier privé, l’état du code sur la
branche et une opération exécutée en production.

[Contrat WF-00 vers conception et planification](../WF00_DESIGN_PLANNING_CONTRACT.md) ·
[Registre canonique](../LOOP_CANONICAL_REGISTRY.md) ·
[Registre des sujets](../../registry/subjects.json) ·
[Mémoire commune](../../memory/README.md)
