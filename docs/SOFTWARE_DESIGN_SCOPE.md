# Software Design — périmètre conceptuel initial

> **Statut : proposition de taxonomie et de conception.** Aucun des domaines ci-dessous n'est déjà implémenté dans ce dépôt.

## Mission

Transformer une succession d'idées, instructions, exigences et modèles en une conception cohérente, versionnée, contrôlable et transmissible au moteur de planification puis au développement.

## Domaines spécialisés proposés

| ID | Domaine | Sorties attendues |
|---|---|---|
| SD-01 | Product Discovery & Vision | intention qualifiée, objectifs, contraintes |
| SD-02 | Requirements Engineering | exigences versionnées, cahier des charges |
| SD-03 | Functional Design | cas d'utilisation, scénarios, parcours |
| SD-04 | Domain & Business Design | domaines, sous-domaines, règles métier |
| SD-05 | UX/UI & Web Design | navigation, écrans, design system |
| SD-06 | Application Architecture | couches, modules, composants, interactions |
| SD-07 | Data Architecture & Modeling | entités, modèles, flux, contraintes |
| SD-08 | API & Integration Design | contrats et échanges |
| SD-09 | Infrastructure & Deployment Design | environnements et déploiement cible |
| SD-10 | Security & Quality Design | exigences et contrôles transversaux |
| SD-11 | Technical Design & Decisions | alternatives, ADR, justifications |
| SD-12 | Design Validation & Readiness | cohérence, couverture, préparation |

## Contrat attendu de chaque sous-système

`inputs → preconditions → analysis → model → validation → evidence → outputs → checkpoint`.

Les relations entre domaines forment un graphe, et non un simple enchaînement linéaire. Une exigence nouvelle peut déclencher la révision d'un modèle validé : le mécanisme doit conserver l'ancien état et ouvrir un changement gouverné.

## Ordre de constitution recommandé

1. Inventaire et classification des sources historiques.
2. Constitution des registres et du workflow documentaire WF-00.
3. Spécification des modèles, contrats et frontières Software Design.
4. Conception du moteur d'orchestration et de persistance.
5. Implémentation et validation sur un projet fictif, sans impact externe.

Ne pas confondre **méthodologie conçue** et **capacité logicielle opérationnelle**.
