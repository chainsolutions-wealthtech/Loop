# Contrôle d’entrée d’un dépôt

**Statut : noyau candidat, sans intégration live.** Ce module prépare une
entrée de workflow avant WF-00. Il ne change ni les autorités ni les règles
de mise en service.

## Profil MCP + GitHub App CUG

L'hôte d'intégration branche `RepositoryEntry.guard` en amont de chaque
appel MCP ciblant un dépôt. Le garde bloque le passage en cas d'échec.
En cas de succès, il transmet le résultat à la couche d'autorisation
de l'hôte. `before_repository_call` peut aussi être appelé seul pour un
diagnostic. L'hôte doit fournir le dépôt de l'appel
courant, issu de son contexte explicite, jamais celui du dernier appel. Une
simple connexion, une liste d'outils ou un appel de santé sans dépôt n'ouvre
aucun contexte projet. Une intégration externe à Loop n'est pas interceptée
automatiquement.

1. **Dépôt exact.** Résoudre l'hôte Git et l'identifiant du dépôt auprès du
   fournisseur. Le nom `owner/repo` est un localisateur, pas la clé de liaison.
2. **Reconnaissance.** Demander au serveur ou à son registre autorisé s'il
   reconnaît exactement cette clé et quel identifiant canonique il lui associe.
   Un serveur joignable ne constitue pas une preuve de cette association.
3. **Liaison approuvée.** Chercher une seule liaison exacte dans le registre
   désigné par le projet. Elle contient la clé du dépôt, l'identifiant
   canonique, l'App ID attendu et la référence versionnée de la procédure.
4. **Installation effective.** Confirmer auprès de GitHub que c'est bien
   cette App, que son installation couvre ce dépôt et qu'elle n'est pas
   suspendue. Une App connue ou installée sur l'organisation ne suffit pas.
   Utiliser une observation authentifiée par l'App et l'API GitHub dédiée
   (`GET /repos/{owner}/{repo}/installation`). Un défaut de preuve ne
   doit pas devenir une déclaration d'absence.
5. **Procédure.** Confirmer la référence et la version dans le catalogue
   approuvé. Le résultat positif est une référence prête à transmettre, pas
   une exécution, une inscription, une session, un claim ni un droit d'écrire.

L'App ID et les références réelles restent dans la configuration du
déploiement. Le module ne conserve aucune clé privée, aucun jeton, ni aucun
registre d'un autre projet. Les droits réels et l'autorisation de l'action
doivent être contrôlés séparément par le système qui l'exécute.

## Contrats des adaptateurs

Le noyau ne dépend d'aucun SDK et n'effectue lui-même aucun accès réseau.
L'hôte fournit cinq fonctions d'observation et l'App ID attendu. L'adaptateur
de reconnaissance pourra utiliser MCP, un autre registre compatible ou une
source locale pour les tests. Un profil MCP ne peut pas remplacer
silencieusement sa source par une autre en cas de panne.

Chaque observation est bornée au dépôt demandé et doit être fiable au moment
du contrôle. Renvoyer `None`, un ensemble vide ou `False` uniquement pour
une réponse négative faisant autorité. En cas de preuve manquante, de refus
d'accès, de réponse mal formée ou de panne, lever `Unverified`. Ne pas
transformer un 404 ambigu en absence démontrée. Le noyau retourne un statut
explicite et ne fournit une procédure que si toute la chaîne concorde.

## Reste à raccorder

- Choisir le point de passage commun des appels MCP utilisés par Loop et
  l'identité qui le consulte. Aucun changement dans `Patricked-code/MCP`.
- Identifier une interface de reconnaissance capable de recevoir le dépôt
  cible et de renvoyer une preuve de sa liaison canonique. Ne pas assimiler
  un contexte MCP courant ou un manifeste candidat à ce contrat.
- Désigner le registre des liaisons et le catalogue des procédures approuvés.
- Raccorder l'observation GitHub CUG avec une identité autorisée, puis
  attester un dépôt reconnu et un dépôt inconnu en lecture seule.

Tests hors ligne depuis la racine du dépôt

```sh
python3 -m unittest discover -s tests -v
```

## Dépôt découvert sans rattachement

Le [parcours de découverte et de rattachement](REPOSITORY_ONBOARDING.md) traite séparément l'identité projet et l'accès App manquants, sans laisser passer l'appel métier.
