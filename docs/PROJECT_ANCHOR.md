# Ancrage canonique d’un projet

Un grand projet conserve un **ID global stable**, attribué ou retrouvé dans
le registre choisi par son propriétaire. Le dépôt Git est identifié par
l'hôte Git et l'ID stable du dépôt. Le serveur et ses répertoires sont des
rattachements de cet ID, pas des éléments dont dépend le calcul de l'ID.
Un changement de nom, de répertoire, de serveur ou de version déployée ne
crée donc pas un autre projet. La continuité et les sous-projets restent
des identités distinctes, rattachables à l'ID global.

| Objet | Clé | Contenu |
| --- | --- | --- |
| Projet | ID global | Dépôt principal, éventuels autres dépôts et références vers les objets du projet |
| Dépôt | Hôte Git + ID stable | Nom actuel, ID global auquel il appartient |
| Répertoire | ID serveur + chemin réel | Dépôt associé, environnement, rôle, état, preuve, référence d'autorité et révision si requise |

## Contrat du composant Project Anchor Index

- **Entrées** — Un instantané de l'autorité choisie et une clé projet, dépôt ou serveur + chemin réel.
- **Mode** — Résolution et contrôle de cohérence hors ligne. Le chemin réel vient d'un observateur autorisé sur le serveur. Le composant ne résout pas lui-même les liens symboliques et ne contacte pas l'hôte.
- **Processus** — Indexer les trois clés, rejeter les collisions et les références incohérentes, puis restituer le rattachement avec son état d'origine.
- **Sorties** — Projet et rattachements, absence dans l'instantané, ou erreur de cohérence. L'absence dans un instantané partiel ne signifie pas que le projet est inconnu de l'autorité.
- **États** — Déclaré, candidat, observé, actif vérifié. Le composant contrôle la présence de références de preuve et d'autorité pour un lien actif. Il ne les authentifie pas et ne promeut aucun état. Pour un checkout ou un runtime actif, un identifiant Git complet est requis. Un chemin de données n'est pas un checkout.
- **Limite** — Un rattachement ne vaut pas installation CUG, autorisation d'exécution ou approbation d'une procédure. La garde d'entrée continue de les évaluer séparément.

## Persistance et mode d'opération

Le registre ou la table **privée** de l'autorité conserve le lien
complet. Dans un environnement géré par MCP, c'est le registre privé côté
serveur MCP qui est visé. Une référence dans le répertoire projet peut
faciliter la découverte, mais n'est pas une seconde autorité. Hors MCP,
un autre adaptateur peut fournir le même instantané à Loop. La projection
Git publique conserve les identités non sensibles. Aucun chemin serveur
privé, secret ou identifiant de session n'y est recopié.

Pour ajouter un rattachement, l'autorité doit établir l'identité du dépôt,
vérifier le serveur, le chemin réel et le rôle du répertoire, puis contrôler
que la clé dépôt et la clé serveur/chemin ne désignent pas un autre projet.
Un checkout exige une preuve de son remote. Un runtime exige une preuve de
sa provenance et ne se déduit pas du seul checkout. Plusieurs répertoires
peuvent pointer vers le même ID. Les désaccords se réconcilient avant toute
activation. L'écriture privée et sa relecture sont une étape distincte,
non exécutée dans ce lot.

## Test réel en lecture seule — 13 novembre 2026

| Cas | Observation | Conclusion |
| --- | --- | --- |
| Stablecoin, ID GitHub `1227251709` | Un checkout S2 sur `main` présente le remote attendu. La révision observée, abrégée à `65f116e`, diffère du préfixe de la [révision GitHub lue](https://github.com/Patricked-code/Stablecoin/commit/a8c5580b925f26588a06b458e15d4921f7fc54db). Le rapprochement ne détermine pas l'ascendance. | Le rapprochement physique est observé, mais la projection reste candidate. Aucun rattachement actif n'est attesté. |
| Garde Loop sur Stablecoin | L'observation ciblée ne fournit pas de reconnaissance officielle. Le rejeu du module avec ces constats retourne `mcp_unverified`, puis la planification retourne `resolve_entry_evidence`. | Aucun appel métier ni demande d'inscription ne part. CUG n'est pas vérifiée nominativement. |
| MCP comme projet sur S1 | GitHub, checkout S1 et runtime Docker ont présenté la même [révision](https://github.com/Patricked-code/MCP/commit/c775709fdaf490eef2e1d43345e0b26e460a072c) lors du relevé de 08 h 36 à Paris, mais l'état global demandait une réconciliation. | Exemple de vérification technique. Ni enregistrement actif de l'ID dans le serveur, ni présence de plusieurs répertoires ne sont démontrés par cette seule observation. |

Les répertoires multiples sont couverts par les tests hors ligne avec des
chemins fictifs. Loop publie uniquement sa propre identité GitHub dans
la projection initiale, sans rattachement serveur attesté. Les deux cas
ci-dessus restent des preuves séparées et ne sont pas importés comme
projets actifs.

Quand le lien manque ou reste à qualifier, voir le [workflow séparé de
rattachement et de préparation d’un hébergement](WORKFLOW_REPOSITORY_HOSTING.md).
Il distingue absence constatée, observation indisponible et conflit.
