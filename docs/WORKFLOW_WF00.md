# WF-00 — Constitution et coordination documentaire

> Première procédure du chantier de préparation Loop. Spécification manuelle sur branche de travail, non adoptée sur main. Sa publication ne lance ni inventaire, ni installation, ni automatisation.

**Objectif** — Transformer une arrivée (intention, document, ouverture d'un dépôt ou reprise) en un dossier de préparation documenté, doté d'un point d'entrée unique pour le périmètre, d'un inventaire traçable et d'un squelette justifié. WF-00 s'arrête avant le cadrage de fond, la conception applicative et le code.

## Paramètres et entrées

1. Lire le [paramétrage de la branche](preparation/PARAMETRAGE_BRANCHE.md) et le [README de Loop](../README.md).
2. Relever la demande, le projet concerné, le dépôt et le SHA de référence s'il existe, les sources et les limites du mandat.
3. Repérer les sources, inventaires et décisions déjà disponibles, avec leur version et leur statut. Une version de kit non disponible ou non confirmée ne doit pas être traitée comme un modèle adopté.
4. Distinguer **projet neuf / dépôt vide**, **projet existant** et **reprise d'un dossier déjà engagé**. Une absence de dépôt ou de documents n'empêche pas de consigner une première intention.

Ce workflow reprend le [brouillon historique WF-00](https://github.com/chainsolutions-wealthtech/Loop/blob/9db9727ddd6c9e6ead7c5dcaa44db8c6afad780e/docs/WORKFLOW_WF00.md) en précisant les entrées, les sorties et l'arrêt manuel. Il ne crée pas une procédure concurrente dans le même arbre. L'inventaire W1 [déjà conservé pour Patricked-code/MCP](https://github.com/chainsolutions-wealthtech/Loop/tree/e72138dc6e8d707c48994991c37b14de0c73fab4/inventaires/patricked-code-mcp/w1) peut servir de preuve d'inventaire, sans être réexécuté ni importé.

## Enchaînement opératoire

| Ordre | Travail documentaire | Résultat transmis |
|---:|---|---|
| 01 | Identifier le projet, l'événement d'arrivée, le mandat et le périmètre. Ne pas confondre Loop comme projet et Loop comme outil appliqué à une cible. | Fiche d'entrée, avec source du mandat et références de départ. |
| 02 | Recenser avant d'organiser. Sur un dépôt neuf, indexer l'intention et les sources disponibles. Sur un existant, relever les chemins, fichiers, procédures, registres, rôles annoncés et points d'entrée. En reprise, réutiliser le dernier inventaire et comparer les changements s'ils comptent pour le mandat. | Inventaire des sources et documents, avec couverture et révisions. |
| 03 | Lire et qualifier les pièces pertinentes. Distinguer règle applicable, source historique, proposition, état déclaré et observation. Noter les chevauchements et les autorités non établies sans décider par le seul nom de fichier. | Registre des sources et liste des écarts ou questions à instruire. |
| 04 | Définir le squelette minimal adapté au périmètre. Pour chaque rôle, identifier un emplacement existant à conserver ou une création à proposer. Décrire les liens de lecture et d'écriture. Un rôle logique n'exige pas automatiquement un fichier. | Proposition de squelette, avec correspondance rôle ↔ chemin, statut et dépendances. |
| 05 | Vérifier l'intégrité des références, la distinction entre constats et choix, l'absence de doublon involontaire et la séparation des autorités par projet. Si le mandat couvre une installation documentaire, n'installer que les éléments explicitement retenus dans ce périmètre. Sinon, garder le squelette à l'état de proposition. | Verdict du dossier et point de reprise, avec éléments à préserver et action suivante précise. |

## Squelette à préparer, pas à installer par défaut

- **Point d'entrée** — indique par où commencer et comment retrouver la reprise.
- **Règles et autorités** — identifient le périmètre et ce qui fait foi pour chaque type d'information.
- **Registre des sources et documents** — conserve provenance, chemins, versions, rôles et liens.
- **Écarts et questions ouvertes** — consigne les faits à éclaircir, leurs preuves et les parties concernées.
- **Suivi et reprise** — consigne les résultats, ce qui manque et le prochain travail documentaire.

Les noms, le nombre et la disposition des Markdown se déduisent des pièces et des décisions du projet. Aucun nombre prédéfini de fichiers, nouveau point d'entrée concurrent ou transposition de la gouvernance du MCP vers Loop n'est imposé ici.

## Point d'arrêt et passage de relais

WF-00 laisse **l'identité et le mandat du projet, un inventaire sourcé, une proposition de squelette, les écarts et un point de reprise**. Les résultats sont assez clairs pour qu'un autre intervenant les relise sans refaire l'entrée. Si une information nécessaire manque, noter la pièce ou la décision à obtenir et l'effet précis de son absence.

La phase suivante peut reprendre le dossier pour le cadrage documentaire. **Ni ce document ni un verdict de préparation n'autorisent à eux seuls le développement, l'exécution d'une Action GitHub, une fusion, une installation applicative ou un déploiement.**

## État de cette publication

`WF-00` est **rédigé et versionné**. Il **n'a pas été exécuté** et aucun squelette n'a été installé par cette publication.
