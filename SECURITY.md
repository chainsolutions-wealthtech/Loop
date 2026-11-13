# Politique de sécurité — amorçage

Le dépôt `Loop` est **public**. Toute information qui y est publiée doit être considérée comme accessible à tous.

## Ne jamais publier

Identifiants, tokens OAuth, clés SSH/API, fichiers .env, données de santé ou personnelles, journaux contenant des secrets, dumps ou sauvegardes, clés de production et chemins confidentiels.

## Signalement

Pour toute vulnérabilité ou fuite potentielle, éviter d'ouvrir une issue publique contenant les détails sensibles. Contacter un responsable du dépôt par un canal privé préalablement convenu. Aucun contact de sécurité particulier n'est déclaré dans cette version.

## Développement

- Privilégier les droits minimaux pour les workflows.
- Examiner les dépendances avant adoption.
- Vérifier les modifications et les journaux CI avant merge.
- Protéger main avec ruleset et revue obligatoire dans les paramètres GitHub.
- Ne jamais utiliser la présence d'un test « PASS » comme preuve de sécurité exhaustive.
