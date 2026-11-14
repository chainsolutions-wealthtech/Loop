# Capsule de création gouvernée — raccordement GitHub Apps

État candidat dans Loop, sans modification GRT. Aucune identité CUG réelle ni création attestée.

## Hiérarchie

| Niveau | Parcours GRT historique | Capsule Loop |
| --- | --- | --- |
| Entrée | `governed-control-plane.yml` reçoit une issue, un commentaire ou un dispatch. | L'appelant s'authentifie auprès de son hôte et soumet la demande. Le préflight Actions est un diagnostic distinct. |
| Demande et décisions | `control_plane_issue_bridge.py` tient l'état de l'issue. `governed_request.py` calcule questions, étapes PREP et handoff. | `core.py` expose `submit`, `consult` et `resume`. `sqlite_store.py` conserve la demande et réserve la cible. |
| Identité | Le workflow obtient un jeton d'installation GitHub App du propriétaire cible. Le jeton qui tient l'issue et celui qui crée le dépôt sont distincts. | L'adaptateur de préflight vérifie CUG, l'installation et un jeton temporaire de lecture. |
| Création | `scripts/control_plane_create_repository.py` exécute seulement PREP-001. Il génère depuis le modèle, relit le premier HEAD ou réconcilie une création, puis verse la preuve. | Le port `Gateway` isole l'exécution. La capsule exige une preuve liée à la tentative. L'exécuteur GitHub d'écriture n'est pas raccordé. |
| Bootstrap et remise | PREP-002 vérifie le bootstrap, PREP-003 observe ou laisse le contexte non résolu, PREP-004 relève la branche et le HEAD avant `HANDOFF_READY`. | Le noyau vérifie la cohérence des preuves du dépôt, du bootstrap et du HEAD avant de passer la main. |

[Workflow GRT](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/blob/3d9cba0223ec43003802635dd264f1f266b7b12b/.github/workflows/governed-control-plane.yml)
· [Exécuteur PREP-001](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/blob/3d9cba0223ec43003802635dd264f1f266b7b12b/scripts/control_plane_create_repository.py).

## Questions à poser dans l'ordre

1. S'agit-il d'une demande neuve ou d'une reprise avec un identifiant existant ? L'adoption d'un dépôt existant relève d'un autre parcours.
2. Quel propriétaire GitHub exact ? Organisation `chainsolutions-wealthtech`, compte personnel `Patricked-code` ou `Wealthtechinnovations`.
3. Quel nom et quelle visibilité ? Un dépôt au même nom n'est pas repris automatiquement.
4. Quel dépôt modèle, quelle révision attendue et quel bootstrap ? Distinguer le compte du modèle et le compte du futur dépôt.
5. Qui peut demander la création et quelle identité App est approuvée pour agir ? L'installation est-elle active sur la cible ? Que couvre-t-elle effectivement ?
6. S'agit-il d'un préflight ou d'une création autorisée ? Ce raccordement n'exécute que le préflight.

Le questionnaire ne demande ni mot de passe GitHub, ni clé privée, ni jeton personnel.
Le demandeur s'authentifie auprès de l'interface qui reçoit sa demande. Le workflow
manuel GitHub repose sur une session GitHub habilitée à le lancer. Si le MCP
devient l'interface, il devra fournir un contexte authentifié et vérifier
l'autorité du demandeur sur la cible. CUG s'authentifie séparément avec sa clé,
un JWT signé et un jeton d'installation. Le compte du demandeur, le
propriétaire cible et l'installation GitHub App restent trois entités distinctes.

## Préflight CUG

Le [workflow](../.github/workflows/governed-creation-app-preflight.yml)
vérifie l'App authentifiée `5417646` et l'installation du propriétaire exact
par la route organisation ou compte personnel. Il lit les permissions
déclarées, demande un jeton limité à `Contents: read`, vérifie le modèle
et le SHA courant de sa branche par défaut, et observe la cible. Il
distingue lecture du modèle et preuve de couverture par la même installation.
Une lecture publique ne prouve pas une couverture privée. Un `404` de la
cible signifie `NOT_VISIBLE_404`, pas absence. Le jeton est révoqué à la fin
du contrôle. Le rapport ne contient aucun jeton et indique toujours
`creation_authorized: false`.

Pour exécuter le workflow, configurer la variable `CREATION_APP_CLIENT_ID`
et le secret `CREATION_APP_PRIVATE_KEY` dans l'environnement GitHub
`governed-creation-app-preflight`, restreint à la branche de confiance.
Ne pas transmettre la clé dans un input, un fichier, un commentaire ou la
conversation. Le workflow ne s'exécute pas sur une PR et doit être présent
sur la branche par défaut pour être déclenché manuellement. On peut aussi
appeler l'adaptateur depuis un hôte de confiance avec injection sécurisée
des secrets, sans attendre cette activation.

## Avant d'activer une création

GRT demande historiquement `Administration: write` et `Contents: read`.
GitHub documente aussi `Repository creation: write` avec `Contents: read`
pour la génération depuis un modèle. Il reste à qualifier le droit effectif
le plus étroit, les politiques du compte, l'accès au modèle avec **le jeton
qui générera le dépôt**, la relecture après création et la corrélation
en cas de réponse perdue. Un préflight vert n'atteste pas ces effets.
L'API de génération ne permet pas de passer un SHA source au POST. Comparer
le HEAD au préflight ne fige donc pas le modèle entre lecture et création.

[Authentification GitHub App](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation)
· [Génération depuis un modèle](https://docs.github.com/en/rest/repos/repos#create-a-repository-using-a-template)
· [Déclenchement manuel](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow).

## Séparer les opérations GitHub App

Le dispatch d'un workflow déjà présent peut utiliser un jeton
d'installation avec `Actions: write` si le workflow accepte
`workflow_dispatch`. Modifier du code ou un registre versionné relève
de `Contents: write`, et la modification de fichiers
`.github/workflows/` exige aussi la permission Workflows applicable.
PR, rulesets et administration se qualifient séparément. Ces capacités
de la plateforme ne prouvent pas les droits effectifs de CUG.

Le [parcours web](GOVERNED_CREATION_WEB_INTAKE.md) prépare les choix et
le dossier sans demander de jeton et sans ouvrir de session d'exécution.
Le MCP peut rester en dehors du premier raccordement.

[Permissions GitHub App](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app)
· [Déclencher un workflow](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event).
