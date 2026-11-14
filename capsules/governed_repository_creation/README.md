# Capsule de création gouvernée de dépôt

Noyau Python autonome. Aucun import du moteur Loop ou de GRT, aucun appel réseau intégré, aucune dépendance externe. Copier le dossier `governed_repository_creation` dans un environnement Python 3.10+ suffit pour l'importer comme paquet. Le reste de Loop n'est pas nécessaire.

## Appels et responsabilités

| Entrée | Effet |
| --- | --- |
| `Capsule.submit(scope, key, ...)` | Enregistre une demande durable ou retrouve la même demande. Aucun appel au fournisseur. |
| `Capsule.consult(scope, request_id)` | Relit la demande dans le périmètre de l'appelant sans écriture. |
| `Capsule.resume(scope, request_id, expected_revision, ...)` | Complète les réponses manquantes ou avance d'une étape vérifiée. Au terme, relit le reçu historique. |

`scope` est fourni par l'hôte après authentification. Il n'est pas un droit que le client peut se donner. Une autorité d'exécution distincte vérifie la cible et le modèle exact, puis valide de nouveau son droit au moment de créer. La réservation SQLite s'applique à tous les appelants qui partagent le même journal. Un hôte multi-instance doit partager un stockage offrant les mêmes garanties de réservation et de révision, pas un fichier par instance. Les bases et les références de preuve doivent rester privées.

## Garanties et limites

Le journal enregistre l'intention et réserve la cible avant la première demande de création. La capsule n'appelle `create_once` que depuis la transition gagnante. Un timeout ou une interruption laisse la demande au point `CREATE_OUTCOME_PENDING`. Un autre appelant peut relire cet état, mais seul un reçu attribuable à la tentative permet d'avancer. Une absence non vérifiée, un nom identique ou un manifeste identique ne suffisent pas. L'adaptateur ne doit jamais rejouer un POST de sa propre initiative.

Si le processus s'arrête après la réservation mais avant l'appel, la capsule ne peut pas distinguer ce cas d'une création acceptée sans réponse. Elle s'arrête donc à la réconciliation en lecture. La version actuelle ne propose pas de levée automatique de la réservation, de suppression du dépôt ni de relance sur un résultat ambigu.

La remise `HANDOFF_READY` contient l'ID stable du dépôt, l'URL, le premier HEAD observé, le HEAD final, le reçu du bootstrap et la prochaine action `DISCOVER_PROJECT_BASELINE`. Le premier HEAD observé peut être postérieur au commit initial si la branche est devenue lisible tardivement. Le bootstrap doit être attribuable au bon dépôt et à la révision attendue du modèle, et le HEAD final doit correspondre au commit attesté. L'infrastructure est laissée non résolue. La capsule ne lance ni entrée locale, ni hébergement, ni déploiement.

## Raccordement futur

Le port `Gateway` est volontairement fourni par l'hôte. Un adaptateur doit démontrer l'autorité réelle, l'absence vérifiée, la corrélation de tentative et les preuves de HEAD et bootstrap. La capsule contrôle leur cohérence, pas l'authenticité d'un adaptateur fourni par l'appelant. Aucun adaptateur d'exécution réelle n'est livré dans cette tranche.

Le **MCP** est une interface d'appel possible pour des clients comme Loop. **CUG**, si l'identité et les droits sont validés, peut fournir à l'adaptateur l'autorité GitHub. Ces rôles sont distincts et optionnels pour le noyau. Le moteur de référence GRT et son modèle restent inchangés. Si un futur adaptateur utilise GRT ou un autre moteur, cela ne change ni l'interface de la capsule ni son point de remise.

[Contrat de référence](../../docs/GOVERNED_REPOSITORY_CREATION_CONTRACT.md) · [Tests de la capsule](../../tests/test_governed_repository_creation_capsule.py)
