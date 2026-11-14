# Précédents vérifiés — création, entrée, MCP et déploiement

Relevé du 13 novembre 2026. Sources externes en lecture seule. Ce dossier
conserve les faits utilisables par Loop, pas une autorisation ni une
nouvelle source de vérité sur les projets étudiés.

## GRT et Gouvern — création puis entrée

1. **Demande centrale.** `GR-000004` a fixé la création d'un dépôt public
   `Patricked-code/Gouvern` depuis Governed-Repository-Template. Le premier
   essai bloquait sur l'ancien secret de création. V2.3.3 a utilisé un jeton
   temporaire d'installation GitHub App du compte cible.
   [Demande GRT #4](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/issues/4).
2. **Création et relecture distinctes.** Le run central a obtenu le jeton
   puis échoué en relisant `main` sur HTTP 409, dépôt Git encore vide.
   Le dépôt et le premier commit ont bien été matérialisés. GitHub attribue
   ce commit à `patricked-mcp-publisher[bot]`, sans preuve qu'il s'agisse de
   CUG. Le reçu de création a ensuite été rapporté dans l'issue.
   [Run central](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/actions/runs/36090669133/job/107932226249)
   · [premier commit](https://github.com/Patricked-code/Gouvern/commit/bd1875ef7948bc74cedae13c6ab1065bf1c0d279)
   · [preuve PREP-001](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/issues/4#issuecomment-5826237643).
3. **Bootstrap GitHub.** Le premier push a déclenché Governance Auto
   Bootstrap. L'initialisation `98c8fec` et l'attestation `4ad855c`
   ont donné `DISCOVER_PROJECT_BASELINE`, pas un hébergement.
   [Run et étapes](https://github.com/Patricked-code/Gouvern/actions/runs/36090689981)
   · [attestation](https://github.com/Patricked-code/Gouvern/commit/4ad855c16e9e9058daf9ebd4aace8a105419b1d4).
4. **Entrée et découverte MCP.** La baseline `23975e0` a enregistré
   `BOTH`, découverte `PASS` en lecture seule, domaine non résolu et
   enregistrement projet non vérifié. La mise à niveau v2.8.1 a remis
   la projection Git à `UNCONFIGURED`. Le succès historique n'est pas
   une preuve de liaison actuelle et le reset documentaire ne démontre
   pas une suppression côté serveur. Relire l'autorité avant de rejouer.
   [Baseline et état historique](https://github.com/Patricked-code/Gouvern/blob/23975e0435e63fb45d7436d1f23ce8ce0a450a5f/.governance/mcp-binding.json)
   · [diff v2.8.1](https://github.com/Patricked-code/Gouvern/commit/0aaa276c75f5fe46cacaf9c636ddbad65ca66ee1).

Le **GRT central** a lui-même lu le catalogue MCP dans le run
`36652696942`. Le jeton MCP authentifie la lecture du Bridge. Le jeton
d'installation GitHub App sert séparément à enregistrer la preuve par PR.
Le [contrat des clients générés](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/blob/2f2333bd9f0724e9119f4de9ab72108ebf74b94e/docs/MCP_REPOSITORY_BINDING.md)
distingue Direct MCP, SSH à certificat temporaire en lecture seule et
`BOTH` avec repli gouverné.
[Run de lecture MCP du GRT](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/actions/runs/36652696942).

## UAES et CUG — portée de chaque preuve

Le ruleset UAES `26883048` est actif sur `main` et admet l'intégration
`5417646`, référencée comme CUG par UAES, en bypass `always`.
Un bypass n'atteste ni la couverture du dépôt par une installation
nominative, ni ses permissions effectives, ni l'obtention d'un jeton.
Une installation appartient au propriétaire GitHub du dépôt et son
périmètre doit être relu pour le dépôt exact.
[Ruleset UAES](https://github.com/chainsolutions-wealthtech/universal-agent-engineering-system/rules/26883048)
· [Configuration des installations GitHub App](https://docs.github.com/en/apps/using-github-apps/reviewing-and-modifying-installed-github-apps).

Le Bridge a servi à un préflight S1 en lecture seule pour UAES. Cela
ne prouve pas un appel MCP par le worker UAES. Son workflow de préflight
OIDC vérifie la disponibilité du mécanisme, sans demander de jeton ni
contacter S1. La PR #12 prépare un candidat Compose, sans runtime UAES
attesté, mapping GitRegistry ni identité de déploiement prouvée.
[Plan U02](https://github.com/chainsolutions-wealthtech/universal-agent-engineering-system/blob/f4b49771a4b4a7e7dbed2a204a79ccf31b584fb5/docs/U02_S1_GOVERNED_DEPLOYMENT_PLAN.md)
· [Préflight OIDC](https://github.com/chainsolutions-wealthtech/universal-agent-engineering-system/blob/f4b49771a4b4a7e7dbed2a204a79ccf31b584fb5/.github/workflows/s1-oidc-preflight.yml)
· [PR #12](https://github.com/chainsolutions-wealthtech/universal-agent-engineering-system/pull/12).

## Regulatory — constitution du dépôt et du produit

- **4 août 2026.** GitHub date le dépôt `chainsolutions-wealthtech/Regulatory`
  (ID `1323383289`) de 21:11:21 UTC. Le premier commit, attribué à
  `Patricked-code` une seconde après, ne contient que `README.md`. Puis
  viennent la gouvernance du projet prospectus et la première cartographie
  machine de la circulaire 05 FCP. GitHub ne déclare ni fork ni template
  parent. Rien ne prouve ici le geste précis de création ou un transfert
  depuis un autre propriétaire. Ce dépôt d'août précède le GRT créé en
  septembre et ne suit pas le parcours de génération attesté pour Gouvern.
  [Premier commit](https://github.com/chainsolutions-wealthtech/Regulatory/commit/55c6dd3da247f604e5b30da7a4a5bf5de265614f)
  · [gouvernance](https://github.com/chainsolutions-wealthtech/Regulatory/commit/cb60b1dfc0ad5611f0e31c14da16bb5b471b0e56)
  · [cartographie](https://github.com/chainsolutions-wealthtech/Regulatory/commit/7433be04ce00d0108c1e01441d5e49f01fb994f4).
- **Nuit du 4 au 5 août.** `LOOP-GOV-001` intègre le kit documentaire
  `loop-engineering-starter-kit` v1.0.0 de façon additive. Le relevé du
  dépôt distingue les 176 chemins Markdown présents des fragments
  historiques invalides, qui ne prouvent pas le ZIP binaire exact.
  [Entrée Loop](https://github.com/chainsolutions-wealthtech/Regulatory/commit/566b3296772232ac53e6ae27ace6d306a2519161)
  · [contrôle et limite d'archive](https://github.com/chainsolutions-wealthtech/Regulatory/blob/15933ff9ea1e9b83ae5c1cb23725169667af4969/docs/09-loop/LOOP_HEALTH_CHECK.md).
- **5 août.** Première tranche exécutable du prospectus FCP, CI de
  génération et tests, puis application Next.js `apps/web`.
  La Regulatory CI a réellement construit Next.js et testé l'API HTTP
  et PostgreSQL dans un runner. C'est une preuve de build/test,
  pas un environnement applicatif permanent.
  [Moteur initial](https://github.com/chainsolutions-wealthtech/Regulatory/commit/a5fdf3c2e33990f461d3e37bd7b7f07987301f52)
  · [première CI](https://github.com/chainsolutions-wealthtech/Regulatory/commit/bc61bbbce09e5dcc570fae6e9f553d44cdeb2162)
  · [application](https://github.com/chainsolutions-wealthtech/Regulatory/commit/85ab43f5f88ed665c167cd61331f2ff5a8906fa5)
  · [run CI avec tests HTTP](https://github.com/chainsolutions-wealthtech/Regulatory/actions/runs/32057602211).

## Regulatory — préparation S1 et limite de preuve

Le 23 octobre, le [premier manifeste](https://github.com/chainsolutions-wealthtech/Regulatory/commit/10edba52a0637f9d1c261568342d0294e4927320)
déclare S1 et le sous-chemin `wealthtechinnovations.com/regulatory`.
Huit minutes plus tard, le [commit suivant](https://github.com/chainsolutions-wealthtech/Regulatory/commit/27e749b6384062c820d479c7d79e24b75b4de3c8)
choisit le sous-domaine `regulatory.wealthtechinnovations.com/`. Le
[manifeste au HEAD lu](https://github.com/chainsolutions-wealthtech/Regulatory/blob/15933ff9ea1e9b83ae5c1cb23725169667af4969/deploy/mcp-target.json)
garde ce sous-domaine, `REQUESTED_NOT_PROVISIONED`, répertoire applicatif
non résolu et provisioning automatique désactivé.

Le pilote MCP [#352](https://github.com/Patricked-code/MCP/pull/352) reste
sur le sous-chemin. [#353](https://github.com/Patricked-code/MCP/pull/353/files)
reste en brouillon et son admission refuse l'écriture tant que les preuves
serveur ne sont pas raccordées. La primitive référencée crée un sous-domaine,
pas une route sous-chemin. Le [ticket produit #3](https://github.com/chainsolutions-wealthtech/Regulatory/issues/3)
consigne la réconciliation nécessaire. La [sonde S1 historique](https://github.com/chainsolutions-wealthtech/Regulatory/issues/3#issuecomment-6529294283)
observe les hôtes, sans attester la route de l'application ni son SHA.

Le [run MCP #39884876866](https://github.com/Patricked-code/MCP/actions/runs/39884876866)
a déployé **MCP**, pas Regulatory. Dans le [run Regulatory #43417811237](https://github.com/chainsolutions-wealthtech/Regulatory/actions/runs/43417811237),
seul le plan a tourné. Claim, réconciliation et release ont été sautés.
Les sources lues n'attestent aucun déploiement durable de l'application,
sur S1, S2 ou un autre hébergeur. Elles ne démontrent pas une absence
universelle d'hébergement. Un environnement test n'est pas la production.

## Règles à reprendre dans Loop

Le [mandat d'arrivée MCP](https://github.com/Patricked-code/MCP/issues/349#issuecomment-6461939290)
commence à la sélection du dépôt. Séparer dans les preuves **création
GitHub → bootstrap → entrée → accès MCP → rattachement serveur →
provisionnement → mise en service → attestation du runtime**. Un premier
provisionnement se prépare avant d'avoir un SHA à livrer. La mise en
service reçoit, elle, un lien vérifié et la révision exacte.

- Une création suivie d'une relecture incomplète doit reprendre par
  vérification du dépôt exact, sans présumer qu'il faut le recréer.
- Une découverte MCP réussie ne vaut ni lien GitRegistry, ni droits d'écrire.
  Une projection écrasée lors d'une mise à niveau n'annule pas les preuves
  historiques et ne certifie pas l'état présent.
- Un sous-chemin HTTP, un sous-domaine et un répertoire réel sont trois
  champs séparés. Une contradiction suspend la préparation d'une mutation.
- Un déploiement est attesté par la cible, le SHA ou l'artefact en service,
  la santé applicative et une preuve de sortie. Ni un manifeste, ni la
  CI, ni un déploiement de MCP ne valent cette preuve.

Reprise Loop `LOOP-W18` · mémoire `LOOP-EVT-20261113-020` à
`LOOP-EVT-20261113-025` · preuves `EV-021` à `EV-026`.
