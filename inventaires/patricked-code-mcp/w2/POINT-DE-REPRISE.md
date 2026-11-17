# W2 — Point de reprise

| Élément | État |
| --- | --- |
| Chantier | W2, qualification des exigences historiques du corpus Patricked-code/MCP pour Loop Engineering. |
| Origine | [W1 au commit de référence](https://github.com/chainsolutions-wealthtech/Loop/tree/e72138dc6e8d707c48994991c37b14de0c73fab4/inventaires/patricked-code-mcp/w1). Le dossier W1 reste intact. |
| Destination | Dépôt `chainsolutions-wealthtech/Loop`, branche documentaire existante `docs/w1-inventaire-patricked-mcp-20261117`, dossier frère `w2/`. |
| Sources | Quatre sources historiques H-LOOP-001 à H-LOOP-004. Même identité de blob pour chacune entre le commit d’introduction retenu par W1 et le snapshot analysé. |
| Résultat | [Qualification](QUALIFICATION.md) · [Registre W2](exigences-w2.json). 15 exigences historiques et 2 règles de passage proposées, 6 cas d’acceptation non exécutés. |
| Qualification | 8 candidats communs en incluant les deux propositions W2, 7 profils candidats, 2 historiques non prescriptifs. Aucun de ces états ne signifie adopté. |
| Contrôles documentaires | Références de provenance par SHA, blobs et plages de lignes vérifiés. Couverture R01–R15, présence des critères positifs/négatifs et des preuves attendues, références des six cas vérifiées. |
| Limites | L’extrait ne prouve pas que le DOCX original est disponible. Les conversations brutes restent non attestées par W1. Aucun kit n’est comparé, installé ou confondu avec le corpus historique. Les PR Loop #1 et #2 restent séparées. |
| Hors du mandat réalisé | Adoption de la méthode, arbitrage d’architecture, installation du moteur ou du squelette, activation d’un workflow, action MCP/serveur, modification d’un dépôt source ou fusion. |

## Reprise exacte

**Prochaine action `REVUE_W2_COMMUNS_ET_PROFILS`** — Revoir séparément les 8 candidats communs, les 7 profils et les 2 éléments historiques. Pour chaque candidat, consigner la décision et le périmètre d’adoption éventuelle. Pour les deux règles de passage W2, vérifier notamment que les deux familles d’entrée, constitution et reprise, restent reconnaissables et que la conception/planification ne soient pas remplacées par une prise de tâche de code.

La première décision à instruire est le **socle minimal commun**. Séparer les conditions du tronc commun des contrôles propres à la migration, au nettoyage, à l’inventaire multi-sources et aux autres profils. La qualification ne fixe pas le format du moteur ni le nombre de fichiers par projet.

Comparer le kit seulement comme **corpus distinct**, après identification d’une archive ou d’une révision immuable, de sa version et de son inventaire. Conserver les écarts de [W1 R4](../w1/R4-ECARTS-ET-LIMITES.md) sans les résoudre par déduction. Ne pas désigner le kit comme source normative et ne pas le confondre avec la spécification candidate WF-00.

**Passage à la conception** — Le dossier peut être soumis à revue. Il ne vaut pas adoption et ne déclenche pas à lui seul une nouvelle phase d’exécution. Une décision d’architecture doit garder distinctes sa source, les exigences retenues et sa preuve de validation.
