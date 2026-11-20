# Inventaire multi-compte des usages MCP

Loop distingue la visibilité GitHub, le code qui appelle ou expose MCP, une
configuration, une mention documentaire et une exécution prouvée. Le module
ne lance ni workflow, ni code de dépôt, ni MCP. Il ne confond pas un autre
fournisseur MCP avec le pont WealthTech.

## Utilisation

Le CLI lit les dépôts visibles par chaque identité sur GitHub.com. Configurer
des identités de lecture déjà autorisées pour les propriétaires demandés,
avec accès métadonnées et contenu en lecture sur le périmètre voulu.
Ne pas déposer de jeton dans Git. Le résultat peut contenir des noms et des
chemins de dépôts privés. Le conserver hors du dépôt et ne pas le publier
dans les logs d'une CI publique ni dans une PR publique.

```sh
python3 -m loop.github_inventory_source --org chainsolutions-wealthtech --user Patricked-code --user Wealthtechinnovations > inventaire-prive.json
```

Variables injectées par le gestionnaire de secrets de l'hôte
`LOOP_GH_TOKEN_CHAINSOLUTIONS_WEALTHTECH`,
`LOOP_GH_TOKEN_PATRICKED_CODE` et
`LOOP_GH_TOKEN_WEALTHTECHINNOVATIONS`.
Pour un compte personnel, le CLI vérifie l'identité authentifiée.
Le noyau accepte toute source implémentant le contrat `Source`.
Aucune dépendance à CUG ni au serveur MCP.

Les branches par défaut sont observées à un SHA précis. La pagination et les
limites par dépôt sont explicites. `--max-files` augmente le nombre de fichiers
inspectés par dépôt. Un arbre tronqué, une lecture refusée ou une limite
atteinte ne permettent pas de conclure à l'absence d'usage. Les résultats
sont des signaux à vérifier, pas une analyse statique complète. Une mention
dans du code ne prouve pas à elle seule l'appel à WealthTech. Le rapport ne
restitue aucun extrait de fichier et ne vérifie pas le runtime.

## Première observation publique — 13 novembre 2026

Périmètre visible par les connecteurs : 17 dépôts d'organisation,
15 dépôts Patricked-code et 13 dépôts Wealthtechinnovations. Branches par
défaut : 44 arbres lus et un dépôt signalé vide par GitHub. Une lecture
ciblée initiale a porté sur 227 fichiers, complétée par des recherches
et des lectures de confirmation. Ce n'est pas un scan exhaustif de tous
les fichiers ou de toutes les branches. Le relevé ci-dessous exclut les
dépôts privés. Aucun workflow externe n'a été déclenché par l'inventaire.

| Dépôt public | Qualification issue de la revue | Preuve versionnée |
|---|---|---|
| chainsolutions-wealthtech/Governed-Repository-Template | Client WealthTech, inventaire des capacités par appels MCP et workflow de rafraîchissement. | [Source](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/blob/9d8fd277dc113aacb2e171fbb6cde00bded982fd/scripts/control_plane_mcp_capability_snapshot.py) |
| chainsolutions-wealthtech/Looping- | Client MCP, moteur d'exécution gouvernée. Le workflow désigne le point d'accès WealthTech. | [Source](https://github.com/chainsolutions-wealthtech/Looping-/blob/86f0317905eb1eaf790e4f2f58a7e3e41735c2bf/scripts/governed_execution_engine.py) |
| Patricked-code/Ekyc | Client MCP, découverte reliée au workflow d'entrée gouvernée. | [Source](https://github.com/Patricked-code/Ekyc/blob/3e889a2bdac78312ebcc7e31d1388ead65c9fceb/scripts/mcp_repository_discovery.py) |
| Patricked-code/Gouvern | Client MCP, découverte reliée au workflow d'entrée gouvernée. | [Source](https://github.com/Patricked-code/Gouvern/blob/671774dfc8e8be8eac2b50d5fb8f0928591694b3/scripts/mcp_repository_discovery.py) |
| Patricked-code/MCP | Fournisseur WealthTech et workflows propres de preuve et de déploiement. | [Source](https://github.com/Patricked-code/MCP/blob/c775709fdaf490eef2e1d43345e0b26e460a072c/.github/workflows/mcp-readonly-evidence.yml) |
| chainsolutions-wealthtech/Regulatory | Cible déclarée, admission et exécution non attestées par ce fichier. | [Source](https://github.com/chainsolutions-wealthtech/Regulatory/blob/15933ff9ea1e9b83ae5c1cb23725169667af4969/deploy/mcp-target.json) |
| Patricked-code/Stablecoin | WealthTech déclaré comme canal principal. Le secours SSH n'est pas un appel direct. | [Source](https://github.com/Patricked-code/Stablecoin/blob/a8c5580b925f26588a06b458e15d4921f7fc54db/.mcp/manifest.json) |
| Wealthtechinnovations/api_opcv | WealthTech référencé dans le contexte nominal. Ce marqueur ne prouve pas un appel. | [Source](https://github.com/Wealthtechinnovations/api_opcv/blob/fcee6ac9ff61e6491113522470799185a8bafd08/scripts/governance/reconstruct_context.py) |
| Wealthtechinnovations/front_end_opcvm | Usage documenté. Appel exécutable non démontré dans les sources examinées. | [Source](https://github.com/Wealthtechinnovations/front_end_opcvm/blob/a2cc791605234b563be8ebcc96d82602124b6509/MCP_AUTONOMY.md) |
| Wealthtechinnovations/immo- | Architecture MCP distincte avec connecteur SIGFU. Aucun lien WealthTech démontré. | [Source](https://github.com/Wealthtechinnovations/immo-/blob/ae2cc25a779fc0b92b5279f570807b24efde57a5/docs/MCP_CONTRACT.md) |

`Loop` et `Looping-` sont distincts. Le premier porte ce module candidat.
Le second contient déjà du code qui appelle MCP. Aucune dépendance entre
les deux dépôts n'est introduite ici.

La collecte initiale a utilisé les accès GitHub déjà connectés. Le nouvel
adaptateur est testé hors ligne. Son activation et la configuration des
identités de lecture restent à faire. Aucun octroi de droits n'est inclus.

## Fiche par dépôt et graphe des raccordements

Le rapport JSON v2 est additif par rapport à v1. Il conserve les indices
initiaux et leur ajoute une classification normalisée : code client,
code fournisseur, workflow candidat, configuration ou référence.

Pour chaque dépôt, la fiche contient son nom, son URL, son compte propriétaire,
son ID GitHub, la branche observée et le SHA. Elle distingue :

- les outils nommés dans le code client des outils exposés par le fournisseur ;
- les points d'accès déclarés, les variables non résolues et les
  rattachements au serveur ou au répertoire, chacun avec son statut ;
- les implémentations et identités MCP déclarées des clients dont la
  connexion effective au dépôt a été attestée par une source de runtime ;
- les workflows, scripts et configurations repérés dans l'arbre ;
- les liens workflow → action / workflow réutilisable / script, les
  références vers les scripts de package, et les appels MCP repérés ;
- les dispatchs dont la cible n'est pas déterminée au point d'appel.

Le SHA, le chemin et la ligne accompagnent les relations lorsqu'ils sont
disponibles. Un lien statique n'est pas une preuve d'exécution. Les scripts
listés par leur chemin ne sont pas tous lus. Les erreurs, exclusions,
limites de taille et plafonds de lecture restent visibles. Les commandes
construites à l'exécution, les imports indirects et les autres branches
peuvent nécessiter une analyse complémentaire.

```sh
python3 -m loop.github_inventory_source --org chainsolutions-wealthtech --user Patricked-code --user Wealthtechinnovations --all-eligible --format html > inventaire-prive.html
```

Un instantané facultatif obtenu séparément en lecture seule peut être
fourni avec `--observations observations-privees.json`. Le format accepte
`registry_candidates` (objets `repo`, `project_id`, `server`, `directory`,
`binding_status`, `source`) et `runtime_catalogue` (`repository`,
`observed_at`, `revision`, `tools`). Un candidat du registre reste un
candidat. Le catalogue du fournisseur ne prouve ni la connexion d'un
client ni l'utilisation d'un outil par un dépôt. Le CLI ne collecte pas
automatiquement ces observations, ne lit pas les sessions clientes
actives et ne lance aucun appel MCP.
