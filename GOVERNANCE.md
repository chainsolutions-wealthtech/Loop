# Gouvernance — Loop Engineering

> État : **proposition de configuration** tant que la Pull Request de fondation n'a pas été approuvée et fusionnée. Ce fichier ne remplace aucune autorité externe.

## Périmètre

Ce dépôt porte le **projet logiciel Loop Engineering**, notamment son moteur de conception de logiciels et applications web. Il ne représente pas le connecteur MCP, ni les dépôts des applications sur lesquels Loop pourra agir.

## Principes contraignants du projet

1. **Historique vérifiable** : conserver l'origine des instructions, les décisions, les versions et les points de reprise.
2. **Conception avant code** : inventorier les exigences et l'existant, qualifier, modéliser, arbitrer, planifier, puis développer.
3. **Deux modes** : constitution depuis un dépôt vide ; reprise d'un dépôt existant sans régression.
4. **Autorité par périmètre** : distinguer sources historiques, documents approuvés, registres, modèles et vues dérivées.
5. **Non-régression** : aucune suppression, remplacement, migration ou déploiement sans analyse d'impact, tests et plan de retour si nécessaire.
6. **Sécurité** : aucun secret, mot de passe, clé privée, token ou donnée personnelle dans le dépôt public.
7. **Gouvernance GitHub** : travailler sur branche dédiée et proposer une PR ; ne pas fusionner vers main sans accord explicite du responsable.
8. **Continuité** : mettre à jour SUIVI.md et le point de reprise pour chaque chantier significatif.
9. **Contradictions** : enregistrer les divergences et arbitrages ; ne pas écraser silencieusement une source.
10. **Séparation des projets** : ne pas modifier Patricked-code/MCP ni d'autres dépôts au titre de cette configuration.

## Cycle d'une contribution

Entrée → identification projet/source → lecture de l'existant et du checkpoint → classification → analyse d'impact → conception → plan et validations → modification limitée → tests et preuves → revue → continuité.

## Contrôles

- Validation documentaire automatisée par CI : **contrôle indicatif**, non certification exhaustive.
- Règles de protection de main et revues obligatoires : **à configurer dans les paramètres GitHub** ; la documentation seule ne les applique pas.
- Tout document marqué « proposé » reste une hypothèse, jusqu'à décision adoptée et traçable.
