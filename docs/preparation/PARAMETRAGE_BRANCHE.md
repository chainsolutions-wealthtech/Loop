# Paramétrage de la branche de préparation Loop

## Identité et périmètre

| Paramètre | Valeur retenue sur cette branche |
|---|---|
| Dépôt et identifiant GitHub | `chainsolutions-wealthtech/Loop` · 1456075212 |
| Branche | `docs/initialisation-wf00-20261117` |
| Base observée | [`main@07a35de18de9bbe46022aa87eaafe1ed1898350a`](https://github.com/chainsolutions-wealthtech/Loop/commit/07a35de18de9bbe46022aa87eaafe1ed1898350a) |
| Mandat | Préparer la branche de travail, puis publier la procédure documentaire du premier workflow. |
| Nature du chantier | Préparation et pilotage documentaires. Aucun code, aucun moteur, aucune Action GitHub. |
| Entrée de référence du dépôt | [`README.md` au SHA de base](https://github.com/chainsolutions-wealthtech/Loop/blob/07a35de18de9bbe46022aa87eaafe1ed1898350a/README.md). |
| Première procédure à ajouter après contrôle de ce paramétrage | `docs/WORKFLOW_WF00.md`. |
| Langue du dossier | Français. Les identifiants et chemins Git restent inchangés. |

## Sources et limites d'autorité

- La [PR Loop #1](https://github.com/chainsolutions-wealthtech/Loop/pull/1) porte une fondation proposée et un WF-00 candidat. C'est une référence de continuité, pas une gouvernance déjà adoptée sur main.
- La [PR Loop #2](https://github.com/chainsolutions-wealthtech/Loop/pull/2) relève de l'admission des dépôts et de l'inventaire multi-dépôts. Son chantier reste séparé.
- Le [relevé W1 de Patricked-code/MCP](https://github.com/chainsolutions-wealthtech/Loop/tree/e72138dc6e8d707c48994991c37b14de0c73fab4/inventaires/patricked-code-mcp/w1) est une preuve documentaire existante. Il reste sur sa branche et n'est ni recopié ni érigé en autorité pour Loop.
- Le projet Loop, le projet logiciel MCP et le connecteur MCP restent des objets distincts. Aucun accès runtime ne découle de ce paramétrage.

## Écriture et point de reprise

- Écriture limitée à cette branche et aux documents du chantier. Aucun transfert de contenu depuis les branches existantes, aucune modification de main, aucun déploiement ni réglage global GitHub.
- Vérifier sur GitHub la référence de branche, le parent de départ et la présence de ce fichier avant d'ajouter la première procédure.
- Une fois ce contrôle effectué, publier WF-00 dans un commit distinct. Le publier ne signifie pas l'exécuter et n'installe pas le squelette.
