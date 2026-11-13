# Entrée canonique du projet Loop

| Objet | Identifiant |
|---|---|
| Projet | `WT-PROJECT-LOOP-001` |
| Dépôt GitHub | `LOOP-REPO-1456075212` — `chainsolutions-wealthtech/Loop` |
| Continuité du chantier | `LOOP-CONV-CONT-20261113-ROOT-01` |
| Point de reprise courant | `LOOP-CP-20261113-002` |

Ces identités sont inscrites dans la branche de la PR #2. Elles ne sont pas
une inscription dans MCP, un ID de session, ni une fusion sur `main`.
Le dépôt est lié par le nom complet **et** son identifiant stable GitHub.
Le suivi du projet est distinct de l'autorité du propriétaire.

## Hiérarchie et relations

**Projet → sous-projet → sujet ou module → élément, opération ou table.**
Un travail est classé sous son sujet. Il garde ses relations transversales
avec les exigences, événements, preuves et dépendances. La continuité a
ses checkpoints et renvoie aux travaux à reprendre ou bloqués. Une table
ou une preuve n'est pas dupliquée lorsqu'elle sert plusieurs modules.

| Sous-projet interne | Périmètre |
|---|---|
| `LOOP-SP-01` | Fondations, gouvernance et sources historiques |
| `LOOP-SP-02` | Entrée, découverte, App et rattachement |
| `LOOP-SP-03` | Inventaire GitHub et cartographie MCP |
| `LOOP-SP-04` | Mémoire, registres et continuité |
| `LOOP-SP-05` | Constitution documentaire, conception et planification |
| `LOOP-SP-06` | Vérification, intégration et passage à l'exécution |

Ce sont des subdivisions du même projet. Aucun dépôt GitHub supplémentaire
n'est créé. Les projets externes restent des sources ou des cibles observées.

## Modules implémentés dans le brouillon

| ID | Module | Entrée → sortie principale |
|---|---|---|
| `LOOP-MOD-001` | Repository Entry Guard | Dépôt et preuves → contexte vérifié ou refus |
| `LOOP-MOD-002` | Repository Onboarding Planner | État d'un dépôt et preuves → suite proposée et vérification du checkout |
| `LOOP-MOD-003` | GitHub Inventory Source | Comptes et identités de lecture → arbres, blobs et export |
| `LOOP-MOD-004` | MCP Inventory Engine | Source et limites → inventaire qualifié et couverture |
| `LOOP-MOD-005` | MCP Catalog & Call Graph | Artefacts et observations → fiches et relations sourcées |
| `LOOP-MOD-006` | Evidence Snapshot Store | Rapport et ID d'instantané → registre SQLite historisé |
| `LOOP-MOD-007` | Canonical Project Registry | ID, alias ou clé privée → fiche, descendance et continuité |

Chaque fiche de [modules.json](../registry/modules.json) contient
responsabilité, code, contrat, modes, entrées, processus, sorties, limites,
exigences, travaux et preuves. WF-00 et Software Design/planification sont
des **capacités spécifiées**, pas des modules déployés. Le raccordement
CUG/MCP et l'intégration à un hôte restent distincts.

## Adresser et retrouver un élément

Les ID stables ne changent pas quand on réorganise un parent. Les anciens
repères E01, REQ-001, EV-001 et D01 restent utilisables comme alias.
Les ID LOOP-W existants sont conservés. Une nouvelle unité reçoit un ID
nouveau. Le SHA de base du checkpoint décrit l'état repris et ne prétend
pas être le SHA du commit qui introduit le checkpoint.

```sh
python3 -m loop.canonical_registry validate
python3 -m loop.canonical_registry tree --depth 3
python3 -m loop.canonical_registry show LOOP-MOD-002
python3 -m loop.canonical_registry show LOOP-CONV-CONT-20261113-ROOT-01
python3 -m loop.canonical_registry show LOOP-CP-20261113-002
```

**Détail privé.** La hiérarchie publique contient l'instantané et ses tables.
Chaque fiche privée est adressable par `SNAPSHOT:GITHUB_ID`. Chaque ligne
d'observation l'est par `SNAPSHOT:GITHUB_ID:SECTION:POSITION`, dans
l'instantané où elle a été capturée. La position est locale à ce snapshot.
La commande ci-dessous lit une base privée existante, sans la modifier.
Aucune ligne privée, aucun chemin serveur sensible et aucune session ne
sont inscrits dans l'arbre public.

```sh
python3 -m loop.canonical_registry private registre-prive.sqlite 'LOOP-INV-20261113-02:1456075212'
```

[Registre de navigation](../registry/README.md) · [Mémoire](../memory/README.md) ·
[Architecture](LOOP_ARCHITECTURE.md) · [Roadmap](LOOP_ROADMAP.md)

Pour prolonger la mémoire à une autre date, ajouter une chronologie et sa
carte de sujets dans `timelines`. Les nouveaux liens doivent citer les ID
datés complets. Seule la première chronologie fournit les alias courts
historiques E01…E16. Les étapes et champs numérotés d'un contrat publié
gardent leur numéro. Un changement structurel se versionne sans réaffecter
un ancien identifiant à un autre objet.

Le [contrat d’ancrage](PROJECT_ANCHOR.md) complète LOOP-MOD-007.
La projection publique `registry/project-anchors.json` est contrôlée avec
le manifeste d’identité. L’index privé peut résoudre le même ID depuis
un serveur et un chemin réel attesté, sans publier ce chemin.
