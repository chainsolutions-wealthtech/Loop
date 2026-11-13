# Paramétrage GitHub — registre de configuration

> Les valeurs ci-dessous sont des **paramètres recommandés**, non la preuve qu'ils sont déjà appliqués dans les paramètres GitHub.

## État initial vérifié le 13 novembre 2026

- Dépôt `chainsolutions-wealthtech/Loop` public, non archivé, `main` déclarée comme branche par défaut.
- Initialement aucun commit, aucune branche, aucune PR, aucune issue.
- Aucune ruleset de dépôt retournée par l'API lors de l'audit.
- Lecture de la protection de branche refusée à l'intégration GitHub (403). Ne pas conclure à une protection inexistante au seul motif de ce refus.
- Auto-merge désactivé dans les métadonnées consultées.
- Premier commit ajouté sur main pour amorcer l'historique.

## À configurer manuellement dans GitHub

1. **Settings → Rules → Rulesets → New branch ruleset**.
2. Cible : branche par défaut `main`, état **Active**.
3. Bloquer les suppressions de branche et les force-pushs.
4. Exiger une Pull Request avant toute fusion.
5. Exiger au moins une approbation de revue (à ajuster selon taille de l'équipe).
6. Envisager l'invalidation des anciennes approbations en cas de nouveaux commits.
7. Après le premier run CI réussi, sélectionner le statut requis `structure-and-policy`. Vérifier son nom exact dans l'interface GitHub.
8. Contrôler les éventuelles règles d'organisation et éviter les exemptions inutiles.
9. Vérifier les paramètres Actions (permissions minimales du GITHUB_TOKEN, pas de secrets pour les PR externes).
10. Vérifier les paramètres de confidentialité, descriptions et équipe propriétaires ; ne pas transformer automatiquement le dépôt public en privé ni choisir une licence sans décision.

## Définition de prêt

- [ ] Premier commit présent et SHA connu
- [ ] Documentation de gouvernance revue
- [ ] Contrôles CI passés
- [ ] Ruleset main active et relue
- [ ] Pull Request de configuration approuvée et fusionnée
- [ ] Source register et plan de conception décidés
- [ ] Checkpoint de reprise actualisé

**Ne pas démarrer l'intégration du moteur logiciel** avant revue du paramétrage et décision explicite.
