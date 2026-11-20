# Découverte et rattachement d’un dépôt

**Statut : planificateur candidat, sans exécution live.** Ce parcours complète
le [contrôle d’entrée](REPOSITORY_ENTRY.md). Il ne le contourne pas.
Il fonctionne sans MCP, GitHub ou serveur lorsque l'hôte lui fournit des
observations locales. Dans le profil MCP–CUG, les adaptateurs doivent utiliser
les autorités désignées, sans substitution silencieuse.

## Décision en lecture seule

| État observé | Sortie du planificateur |
|---|---|
| Rattachement, App et procédure vérifiés | Reprendre le projet avec le même identifiant. |
| Dépôt inconnu, constat confirmé | Demander si c'est un nouveau projet ou un dépôt à joindre à un projet existant. |
| Reconnaissance incertaine ou liaison contradictoire | Réexaminer les preuves. Ne pas proposer d'inscription. |
| Pas d'installation, absence établie | Préparer la demande d'installation de l'App. |
| Installation existante, dépôt non couvert | Proposer d'ajouter ce seul dépôt à l'installation désignée. |
| App suspendue ou couverture incertaine | Signaler le problème et revérifier avant toute suite. |
| Dépôt inconnu, choix explicite, couverture confirmée | Préparer une demande d'inscription. Aucun ID projet n'est émis par Loop. |

## Contrat de transmission pour une future exécution

La demande d'inscription contient le dépôt identifié (hôte, ID stable et nom),
le choix explicite (nouveau projet ou ID existant), la preuve de couverture
de l'App et une clé d'idempotence. Le planificateur ne valide ni l'existence
ni l'autorité d'un ID proposé par le demandeur. Avant une écriture, l'adaptateur
et son autorité doivent vérifier le projet cible, les droits, la fraîcheur
des preuves et l'absence d'association concurrente.

Une relance pour le même dépôt, la même App et le même choix reprend la même
clé, y compris après un changement de nom du dépôt. L'autorité d'inscription
doit assurer elle-même la déduplication et contrôler les demandes concurrentes
sur le dépôt. La clé ne constitue ni un verrou ni une preuve d'inscription.
Pour confirmer le résultat, relire le dépôt depuis la source de reconnaissance
et retrouver le projet et sa procédure via le contrôle d'entrée.
Si la relance d'une demande de création découvre un rattachement existant,
elle reprend ce rattachement. Si elle vise un autre ID existant que celui
observé, elle signale le conflit.

Après une confirmation d'accès CUG ou une inscription autorisée, reprendre
par une nouvelle observation. Aucun webhook, installateur ou connecteur
d'écriture n'est activé par ce module.

## Projet, serveur, checkout et actions

Un projet peut avoir plusieurs dépôts et plusieurs environnements.
L'association du projet à un serveur et à un environnement vient du registre
désigné par l'hôte. Elle ne prouve pas qu'un dépôt est présent sur le serveur.
La preuve d'un checkout existant compare au même point d'observation :

- l'identifiant du projet confirmé à l'entrée et l'identité du dépôt ;
- le serveur, l'environnement et le chemin réel attendus ;
- l'identité du dépôt distant, la branche observée et le SHA Git complet relevé.

Le résultat positif signifie **candidat vérifié**, pas rattachement écrit,
révision déployée ni droit d'intervention. L'hôte conserve les preuves,
la provenance et la référence de procédure selon ses propres autorités.

| Action possible | Prérequis à vérifier séparément |
|---|---|
| Inventorier un environnement | Cible identifiée et accès de lecture autorisé. |
| Vérifier un checkout | Serveur et chemin rattachés au périmètre, observation en lecture seule. |
| Rattacher un checkout existant | Candidat concordant et autorité habilitée à inscrire le lien. |
| Créer ou synchroniser un checkout | Écriture autorisée et conditions du workflow applicable. |
| Déployer une révision | Révision, validations, environnement et décision de mise en service. |

La table est un exemple de suites possibles, pas un catalogue exécutable.
Aucune de ces actions n'est déclenchée par le planificateur.

## Vérification

```sh
python3 -m unittest discover -s tests -v
```
