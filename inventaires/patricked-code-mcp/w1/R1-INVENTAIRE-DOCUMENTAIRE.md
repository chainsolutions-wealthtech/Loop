# R1 — Inventaire des sources et des documents

Relevé W1 de `Patricked-code/MCP`, arrêté sur [`main@e8cfaf7246abb20151a8b439913d97ecf87a4979`](https://github.com/Patricked-code/MCP/tree/e8cfaf7246abb20151a8b439913d97ecf87a4979). Il ne désigne aucune nouvelle source d’autorité pour Loop.

## Couverture et méthode

- L’[index complet des chemins](R1-INDEX-ARBRE.csv) contient **888 entrées Git suivies**. Il conserve le chemin exact, le mode, le SHA du blob et la taille. Les entrées non documentaires ne sont pas interprétées comme des composants fonctionnels.
- Les **233 Markdown** du snapshot ont été ouverts pour relever leur titre et leur structure. L’ensemble de leurs chemins correspond exactement à celui de l’[inventaire Markdown déjà maintenu dans MCP](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/docs/governance/markdown-inventory.json). Les catégories du CSV sont reprises de cet inventaire source et ne valent pas adoption par Loop.
- La table des pièces prioritaires qualifie **36 fichiers**. Le reste du corpus est repérable dans le CSV. Une lecture de structure ne vaut ni lecture sémantique exhaustive ni validation d’une autorité.
- **3 PDF et 6 TXT** sont repérés en tant que pièces hors Markdown. Les PDF ne sont pas transcrits ni déclarés lus. Les documents externes non récupérés restent explicitement ouverts.
- Les identifiants `MCP-F-…` sont des références locales à ce relevé, dérivées du chemin, non des identifiants canoniques du MCP. Une recherche de version s’appuie sur le commit source et le SHA du blob, pas seulement sur l’identifiant de ligne.

| Catégorie dans l’index du MCP | Markdown |
|---|---:|
| canonical | 7 |
| documentation | 82 |
| engineering-plan | 8 |
| engineering-spec | 10 |
| history | 1 |
| memory | 61 |
| migration-history | 7 |
| root-documentation | 50 |
| runtime-mirror-tracked | 7 |

## Pièces prioritaires qualifiées

| ID de relevé | Chemin au SHA observé | Rôle qualifié | Observation W1 |
|---|---|---|---|
| `MCP-F-b335630551682c19` | [`README.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/README.md) | Entree annoncee | Renvoie explicitement à INTAKE global dans AGENTS.md et documente également des parcours de reprise. |
| `MCP-F-a54ff182c7e8acf5` | [`AGENTS.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/AGENTS.md) | Regles et entree | Décrit INTAKE global, priorités, reprises et bifurcation. Identifier l’ordre et le contexte de chaque procédure avant toute transposition. |
| `MCP-F-6ebdb617a8104a77` | [`CLAUDE.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/CLAUDE.md) | Porte agent | Renvoie à l’accueil commun AGENTS.md avant profils spécialisés. Contient aussi des consignes Claude et des chemins de reprise. |
| `MCP-F-7c1dac293c1bcb4f` | [`GPT.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/GPT.md) | Memoire agent | Mémoire générale de l’IA à la racine et références de gouvernance. |
| `MCP-F-2f41a784d95be0f1` | [`CODEX.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/CODEX.md) | Porte agent | Guide spécifique à Codex. Référence descriptive pour Loop, pas procédure à déclencher. |
| `MCP-F-2e8b8fb664b17164` | [`SOURCE_OF_TRUTH.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/SOURCE_OF_TRUTH.md) | Autorite declaree dans MCP | Hiérarchie déclarée des sources. SUIVI.md pour le point de reprise, docs/ et memory/ pour l’historique et le contexte. Aucun transfert d’autorité vers Loop. |
| `MCP-F-e13daf549e33e2af` | [`SUIVI.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/SUIVI.md) | Suivi versionne | Historique et point de reprise du projet MCP. Un état déclaré doit rester distinct d’une observation runtime. |
| `MCP-F-aafad4c01ce6bd66` | [`ACTIVITY_LOG.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/ACTIVITY_LOG.md) | Journal versionne | Trace des interventions significatives, distincte de GitHub Activity et du point de reprise. |
| `MCP-F-48a5e5ceae8920c6` | [`DECISIONS_LOG.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/DECISIONS_LOG.md) | Journal de decisions | Fiches et traces de décisions MCP, à référencer sans transfert d’autorité. |
| `MCP-F-090cf623ff58d9ba` | [`NO_REGRESSION_POLICY.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/NO_REGRESSION_POLICY.md) | Regle de travail | Formalise la non-régression et la séparation d’une passe documentaire d’une modification applicative. |
| `MCP-F-5095665987de1635` | [`PROJECT_BRIEF.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/PROJECT_BRIEF.md) | Cadrage | Brief du projet logiciel MCP. Ne vaut pas brief du projet Loop. |
| `MCP-F-140f0d50a026ca12` | [`PROJECT_SCOPE.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/PROJECT_SCOPE.md) | Cadrage | Périmètre et exclusions documentés du projet logiciel MCP. |
| `MCP-F-5fe115e887d2627c` | [`MCP_PROJECT.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/MCP_PROJECT.md) | Contexte projet | Objectif et rattachement d’organisation déclarés pour le MCP. |
| `MCP-F-023c21f1266d0976` | [`MCP_REPO_BOOTSTRAP.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/MCP_REPO_BOOTSTRAP.md) | Procedure distincte | Procédure de rendre un dépôt compatible MCP, à ne pas assimiler au parcours documentaire W1 de Loop. |
| `MCP-F-9557e87e242c2589` | [`MCP_REPO_INVENTORY.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/MCP_REPO_INVENTORY.md) | Inventaire existant | Référentiel d’inventaire du dépôt dans le MCP, à comparer sans le remplacer. |
| `MCP-F-f29753586c28f9ec` | [`docs/governance/README.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/docs/governance/README.md) | Index de gouvernance | Index de navigation vers les chantiers, sources et reprises du MCP. |
| `MCP-F-a2a46ca40553851a` | [`docs/governance/markdown-inventory.json`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/docs/governance/markdown-inventory.json) | Inventaire versionne existant | Index de chemins et catégories Markdown. Comparaison de couverture avec l’arbre Git de ce relevé. |
| `MCP-F-d7da071b25db9d59` | [`docs/governance/agent-historical-continuity-breadcrumbs-20261016.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/docs/governance/agent-historical-continuity-breadcrumbs-20261016.md) | Index historique | Fil d’Ariane explicitement référencé depuis README.md et AGENTS.md. |
| `MCP-F-6ddf9da62e83614d` | [`docs/runbooks/GITHUB_FIRST_GOVERNED_RECOVERY.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/docs/runbooks/GITHUB_FIRST_GOVERNED_RECOVERY.md) | Procedure specialisee | Runbook GitHub-first pour la reprise gouvernée externe. Ne pas confondre avec l’accueil général ni l’exécuter dans W1. |
| `MCP-F-bb4c9b2ba6305eba` | [`docs/governance/pilots/E2-MCP-ENTRY-RECONCILIATION-PROTOCOL.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/docs/governance/pilots/E2-MCP-ENTRY-RECONCILIATION-PROTOCOL.md) | Protocole pilote | Protocole spécialisé E2. La présence du document ne prouve pas l’activation du pilote. |
| `MCP-F-6f6d53a77401c740` | [`.mcp/github-first-operational-policy.json`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/.mcp/github-first-operational-policy.json) | Politique structuree | Politique MCP citée par les documents d’entrée. Indexation de la référence, sans application dans Loop. |
| `MCP-F-c86e40afacc38cc0` | [`PRODUCTION_STATE.json`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/PRODUCTION_STATE.json) | Etat declare | Déclaration versionnée des états observés par ailleurs. Ne constitue pas un constat frais de production. |
| `MCP-F-031b094758fb06ee` | [`LOOP_ENGINEERING.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/LOOP_ENGINEERING.md) | Boucle MCP formalisee | Boucle opérationnelle MCP à la racine, distincte des formulations historiques WealthTech. |
| `MCP-F-bb937a8c0fab0d81` | [`docs/GPT.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/docs/GPT.md) | Source historique | Premier emplacement historique de GPT.md. Les anciennes règles sont utiles pour reconstituer la chronologie. |
| `MCP-F-8af872715889edc7` | [`docs/SUIVI.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/docs/SUIVI.md) | Source historique | Ancien journal et point de reprise du dépôt initial. |
| `MCP-F-e8a298cb326f4cf6` | [`memory/GPT.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/GPT.md) | Memoire historique | Version issue de la mémoire WealthTech et MCP. À qualifier par périmètre et date, sans la substituer au parcours actuel. |
| `MCP-F-a31f3ad396fe71e7` | [`memory/SUIVI.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/SUIVI.md) | Memoire historique | Suivi historique de périmètre WealthTech, MCP et Stablecoin. Pas un état live. |
| `MCP-F-5462740fe4988797` | [`memory/CONVERSATION_PART_02_ECOSYSTEM_LOOP_ENGINEERING_2026-07-01.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/CONVERSATION_PART_02_ECOSYSTEM_LOOP_ENGINEERING_2026-07-01.md) | Conversation compilee | Description précoce de l’écosystème, des documents obligatoires et de l’ordre de lecture. Ce n’est pas le transcript brut. |
| `MCP-F-63c1820d78825ac9` | [`memory/CONVERSATION_20260701_LOOP_ENGINEERING.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/CONVERSATION_20260701_LOOP_ENGINEERING.md) | Conversation compilee | Pièce de mémoire Loop Engineering datée du 1er juillet. |
| `MCP-F-3dfb8bc9c4cc479e` | [`memory/LOOP_ENGINEERING_INSTRUCTIONS_DOCX_EXTRACT_20260702.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_INSTRUCTIONS_DOCX_EXTRACT_20260702.md) | Extrait historique | H-LOOP-001 selon le registre candidat de Loop. Source dérivée du DOCX original, pas équivalence avec l’original. |
| `MCP-F-dc33231ad47b9c12` | [`memory/LOOP_ENGINEERING_WEALTHTECH_MASTER_PLAN_20260702.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_MASTER_PLAN_20260702.md) | Plan historique | H-LOOP-002 selon le registre candidat de Loop. Ordre de lecture, préparation, boucle en dix étapes et tracks. |
| `MCP-F-ee423cead14dbe21` | [`memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md) | Playbook historique | H-LOOP-003 selon le registre candidat de Loop. Préconditions, chantiers, livrables et points de passage. |
| `MCP-F-a65df0eec96d96dc` | [`memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md) | Matrice historique | H-LOOP-004 selon le registre candidat de Loop. Liens entre sources, exigences et tracks. |
| `MCP-F-010c21a815afb1d1` | [`memory/LOOPBACK_WEALTHTECH_CURRENT.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOPBACK_WEALTHTECH_CURRENT.md) | Point de reprise historique | Point d’entrée Loopback WealthTech. Son intitulé ne vaut pas état actuel de Loop ni du MCP. |
| `MCP-F-be67a41d127dabf8` | [`docs/gwc/README.md`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/docs/gwc/README.md) | Index programme GWC | Point de navigation dans GWC, distinct de la genèse de juillet et du mode d’accueil général. |
| `MCP-F-b2ef1782ff44421f` | [`docs/governance/pilots/PILOT-E2-01-entry.json`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/docs/governance/pilots/PILOT-E2-01-entry.json) | Donnees pilote | Fiche structurée de référence du pilote E2, sans activation. |

## Sources fondatrices à préserver séparément

Les quatre identifiants ci-dessous sont ceux du **registre de sources candidat** dans [la PR Loop #1](https://github.com/chainsolutions-wealthtech/Loop/pull/1). Ils sont réutilisés ici comme références de rapprochement, sans créer une seconde autorité.

| Repère existant | Version introduite dans Git |
|---|---|
| H-LOOP-001 | [`memory/LOOP_ENGINEERING_INSTRUCTIONS_DOCX_EXTRACT_20260702.md`](https://github.com/Patricked-code/MCP/blob/ec4cd5e0f0f27a75209ef9aaefcbe6e461b163a9/memory/LOOP_ENGINEERING_INSTRUCTIONS_DOCX_EXTRACT_20260702.md) |
| H-LOOP-002 | [`memory/LOOP_ENGINEERING_WEALTHTECH_MASTER_PLAN_20260702.md`](https://github.com/Patricked-code/MCP/blob/ec4cd5e0f0f27a75209ef9aaefcbe6e461b163a9/memory/LOOP_ENGINEERING_WEALTHTECH_MASTER_PLAN_20260702.md) |
| H-LOOP-003 | [`memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md`](https://github.com/Patricked-code/MCP/blob/ec4cd5e0f0f27a75209ef9aaefcbe6e461b163a9/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md) |
| H-LOOP-004 | [`memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md`](https://github.com/Patricked-code/MCP/blob/ec4cd5e0f0f27a75209ef9aaefcbe6e461b163a9/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md) |

L’existence de l’extrait du document Word ne prouve pas que l’original est dans Git. Le DOCX original et les transcripts bruts complets ne sont pas attestés par ce relevé. Les dates figurant dans le nom ou le texte d’un document ne sont pas confondues avec sa première version Git.

## Pièces PDF et texte repérées

- [`Migration/PDF/conversation_migration_part_01_of_05_2026-07-04.pdf`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/Migration/PDF/conversation_migration_part_01_of_05_2026-07-04.pdf) — métadonnées de l’arbre.
- [`Migration/PDF/conversation_migration_part_02_of_05_2026-07-04.pdf`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/Migration/PDF/conversation_migration_part_02_of_05_2026-07-04.pdf) — métadonnées de l’arbre.
- [`Migration/conversation_migration_disponible.pdf`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/Migration/conversation_migration_disponible.pdf) — métadonnées de l’arbre.
- [`docs/governance/pilots/PILOT-E2-01.txt`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/docs/governance/pilots/PILOT-E2-01.txt) — métadonnées de l’arbre.
- [`docs/gwc/PRECODE_ACTION_TASK_FLOW.txt`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/docs/gwc/PRECODE_ACTION_TASK_FLOW.txt) — métadonnées de l’arbre.
- [`docs/gwc/PRECODE_EXECUTION_PLAN.txt`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/docs/gwc/PRECODE_EXECUTION_PLAN.txt) — métadonnées de l’arbre.
- [`docs/gwc/canonical-memory/pr95-task-reconciliation-ready/sources/program-procedure.txt`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/docs/gwc/canonical-memory/pr95-task-reconciliation-ready/sources/program-procedure.txt) — métadonnées de l’arbre.
- [`scripts/amf_registry_native_export.txt`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/scripts/amf_registry_native_export.txt) — métadonnées de l’arbre.
- [`scripts/brvmdata_amf_push.txt`](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/scripts/brvmdata_amf_push.txt) — métadonnées de l’arbre.

## Renvois d’arrivée observés

| Point de départ | Renvoi constaté | Qualification |
|---|---|---|
| `README.md`, arrivée universelle | `AGENTS.md`, section INTAKE global | Parcours d’accueil annoncé sur ce snapshot. Le recenser ne signifie pas l’exécuter. |
| `CLAUDE.md`, accueil commun | Même section de `AGENTS.md` | Confirmation documentaire du renvoi commun avant les profils spécialisés. |
| `README.md` et `AGENTS.md`, fil d’Ariane | `docs/governance/agent-historical-continuity-breadcrumbs-20261016.md` | Source de navigation historique, pas preuve d’un état live. |
| `AGENTS.md`, reprise guidée | `SUIVI.md`, index de gouvernance, carte de priorité et directives GitHub citées | Instructions contextuelles, à comparer selon le type d’arrivée. |
| `CLAUDE.md`, mode de bifurcation externe | `docs/runbooks/GITHUB_FIRST_GOVERNED_RECOVERY.md` et politique .mcp | Parcours spécialisé, distinct du recensement documentaire W1. |
| `SOURCE_OF_TRUTH.md` | `SUIVI.md` pour la reprise, `docs/` et `memory/` pour l’historique et le contexte | Priorité déclarée dans le MCP, à la révision source. Ne résout pas par elle-même tous les cas ni ne s’applique automatiquement à Loop. |

## Références GitHub hors du corpus de main

| Référence | Statut observé à la collecte | Utilité documentaire |
|---|---|---|
| [MCP #372](https://github.com/Patricked-code/MCP/pull/372) | Brouillon ouvert, non fusionné | Matrice historique et contrats de rapprochement. |
| [MCP #373](https://github.com/Patricked-code/MCP/pull/373) | Brouillon ouvert, non fusionné | Arbre documentaire vivant et identifiants de continuité. |
| [MCP #374](https://github.com/Patricked-code/MCP/pull/374) | Brouillon ouvert, non fusionné | Nomenclature et séparation des chantiers historiques. |
| [MCP #377](https://github.com/Patricked-code/MCP/pull/377) | Fusionnée | Source de chronologie sur le raccordement de continuité, sans exécution dans W1. |
| [MCP #378](https://github.com/Patricked-code/MCP/pull/378) | Brouillon ouvert, non fusionné | Inventaire de dépôt sur un autre snapshot, utile pour comparaison, non agrégé aux chiffres de W1. |
| [MCP #389](https://github.com/Patricked-code/MCP/pull/389) | Brouillon ouvert, non fusionné | Identifiant de projet `WT-PROJECT-MCP-001` et registres proposés, à distinguer d’un état adopté sur main. |
| [Loop #1](https://github.com/chainsolutions-wealthtech/Loop/pull/1) | Branche de proposition distincte | Registre de sources et WF-00 existants en proposition. Ce relevé peut les documenter sans les remplacer. |
| [Loop #2](https://github.com/chainsolutions-wealthtech/Loop/pull/2) | Branche de proposition distincte | Autre chantier d’admission et d’inventaire multi-dépôts, distinct du recensement documentaire de ce seul dépôt. |
