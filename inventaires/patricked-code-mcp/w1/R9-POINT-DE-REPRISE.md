# R9 — Point d'arrêt W1

| Champ | Valeur |
|---|---|
| Identifiant local de reprise | `LOOP-W1-PATRICKED-MCP-20261117` |
| Date de collecte | 17 novembre 2026 |
| Projet source | `Patricked-code/MCP` en tant que projet logiciel. `wealthtech_ssh_bridge` est l'outil mentionné par ses sources, non actionné pour ce relevé. |
| Révision source | `e8cfaf7246abb20151a8b439913d97ecf87a4979` |
| Destination | `chainsolutions-wealthtech/Loop`, branche `docs/w1-inventaire-patricked-mcp-20261117` |
| Verdict W1 | **Inventaire W1 constitué sur le snapshot retenu, avec réserves de couverture consignées.** Aucun arbitrage d'architecture ni décision d'autorité pour Loop. |
| Produits | [Inventaire R1](R1-INVENTAIRE-DOCUMENTAIRE.md), [index de l'arbre](R1-INDEX-ARBRE.csv) et [constats R4](R4-ECARTS-ET-LIMITES.md). |
| Non exécuté | W2 à W6, choix d'architecture cible, installation de kit, modification du MCP, exécution de ses procédures d'admission, action sur S1/S2, déploiement et fusion. |

## Reprendre sans refaire l'inventaire

1. Relire le [mandat et le périmètre W1](README.md), puis les pièces prioritaires de [R1](R1-INVENTAIRE-DOCUMENTAIRE.md).
2. Vérifier le SHA source lorsqu'une information actuelle est nécessaire. Pour décrire l'état de cette collecte, conserver le SHA du snapshot et ses liens figés.
3. Distinguer les sources **historiques**, les règles **publiées dans le MCP** et celles qui pourraient être **retenues pour Loop**. Une source historique n'est pas promue implicitement.
4. Réutiliser les références déjà proposées dans le registre Loop au lieu de créer une seconde autorité.

**Prochaine action proposée, non commencée** — Quand le cadrage W2 sera demandé, qualifier les exigences et contraintes d'origine à partir des quatre sources fondatrices identifiées dans R1. Distinguer celles qui appartiennent au contexte WealthTech/MCP de celles qui pourraient être reprises dans une méthode générique Loop. Conserver les limites R4 et ouvrir la comparaison du kit uniquement comme corpus distinct.

**Conditions de reprise** — Si le DOCX original ou un transcript complet devient disponible, l'indexer comme pièce distincte et vérifier l'extrait correspondant. Si une nouvelle révision du dépôt doit servir de référence, relever explicitement les différences. Ne pas écraser le snapshot W1.
