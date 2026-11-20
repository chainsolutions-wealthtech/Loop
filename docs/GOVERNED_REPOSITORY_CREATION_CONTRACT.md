# Contrat candidat — création gouvernée de dépôt

**Version proposée** `1.0.0-draft` · **Reprise** `LOOP-W19` · **Continuité du chantier** `LOOP-CONV-CONT-20261113-ROOT-01`.

Ce contrat isole le parcours `CREATE_NEW_REPOSITORY`, pas le dépôt Governed-Repository-Template dans son ensemble. Il couvre la branche « créer » du premier maillon et le bootstrap automatique du maillon suivant. Loop référence le contrat. Il n'est ni le moteur de création, ni une autorité GitHub. GRT est le premier moteur à réutiliser derrière ce contrat, pas un hôte imposé. Un outil MCP, Loop ou un autre client peut être appelant. L'identité d'exécution GitHub App est indépendante du client. Aucun nouveau dépôt ni nouvelle App n'est requis par le contrat.

## Interface portable proposée

| Opération | Entrée | Effet ou résultat |
| --- | --- | --- |
| Soumettre | Clé de demande stable fournie par l'appelant, compte propriétaire, nom, visibilité et référence de continuité du projet si connue. Les champs manquants peuvent faire l'objet de questions. | Crée ou retrouve une demande durable et rend son identifiant, sa révision et la prochaine étape. Ne publie aucun secret. La cible n'est exécutée qu'une fois les réponses nécessaires et l'autorité confirmées. |
| Consulter | Identifiant de demande, dans le périmètre autorisé de l'appelant. | Lecture seule. Rend la phase, le motif d'arrêt, la prochaine action, les preuves disponibles et, s'il est prêt, le reçu de remise. |
| Reprendre | Identifiant, révision attendue et, si l'étape le demande, une réponse ou un signal de reprise autorisé. | Reprend au dernier état durable. Une révision obsolète impose une relecture. Une demande déjà terminée rend le même reçu historique, sans régénérer le dépôt. |

L'identifiant de continuité, la clé de déduplication de l'appelant, l'identifiant de demande du moteur (par exemple `GR-…`) et le `repository_id` GitHub ont des rôles distincts. Le moteur conserve la correspondance et le choix de propriétaire canonique. La même clé dans son périmètre d'autorité retrouve la même demande. Une modification incompatible après validation ou début d'exécution renvoie un conflit explicite, sans rediriger la création. Les demandes concurrentes pour une même cible doivent être sérialisées ou mises en conflit avant une écriture. Le contrat ne prescrit ni le lieu de stockage ni le transport.

## Chronologie et preuve exigée

| État ou phase GRT réutilisée | Ce qui permet d'avancer |
| --- | --- |
| Demande qualifiée | Compte, nom, visibilité, intention de création et droit effectif de l'identité d'exécution sur la cible. Vérifier séparément l'accès au modèle. Ne pas déduire que l'installation utilisée est CUG à partir du nom d'un bot. |
| `PREP-001` — génération ou réconciliation de la génération | Journaliser l'intention de création avant l'appel à GitHub. Associer la réponse de génération et l'ID de dépôt à la demande dès qu'ils sont disponibles. Relire l'identité, la provenance, la branche et le premier SHA. Une réponse de création n'est pas une preuve de bootstrap. |
| `PREP-002` — bootstrap | Vérifier le succès du run du bon dépôt, la version attendue du modèle et le SHA attesté. Si la preuve est indisponible ou que le bootstrap a échoué, ne pas avancer. |
| `PREP-003` — contexte initial | Reprendre l'observation historique si disponible. Sinon, représenter explicitement le contexte d'infrastructure comme non résolu. Aucun raccordement MCP, serveur ou domaine n'est exigé ni effectué par ce contrat. |
| `PREP-004` — relecture de remise | Capturer l'ID du dépôt, sa branche et son HEAD exact après bootstrap. Si le HEAD n'est plus le SHA attendu, arrêter et réconcilier la divergence avant remise. |
| `HANDOFF_READY` — remise centrale | Remettre l'identifiant de demande, la référence de continuité si fournie, l'ID GitHub, le propriétaire et le nom canonique, l'URL, la branche, le premier SHA, le HEAD attesté, le reçu de bootstrap et les références de preuve. L'opération suivante est `DISCOVER_PROJECT_BASELINE`. Cette sortie n'autorise pas une écriture dans le dépôt. |

La première entrée locale et son résultat `LOCAL_HANDOFF_READY` sont hors périmètre. L'adoption d'un dépôt préexistant, son raccordement au MCP, l'hébergement et le déploiement restent des capacités distinctes. `LOOP-CAP-006` et `LOOP-W18` restent attachés à l'hébergement.

## Règle de reprise sans doublon

1. **Création acceptée, premier HEAD indisponible.** Conserver l'identifiant de demande et la preuve déjà obtenue. Réessayer seulement la lecture. Un HTTP 409 sur la lecture du commit initial n'autorise pas un nouveau POST de génération.
2. **Résultat du POST inconnu.** Rechercher la cible et corréler la preuve à la même demande avant toute nouvelle décision. Un 404 sans preuve de visibilité, un timeout ou un manifeste de modèle seul ne démontrent ni l'absence, ni l'appartenance à cette demande. Si le lien ne peut pas être établi, remettre un blocage explicite. Aucun nouveau POST par défaut.
3. **Dépôt déjà présent.** Une reprise de la même demande exige un lien probant avec le dépôt exact, par exemple le `repository_id` déjà journalisé ou une preuve de création corrélée. Un autre dépôt au même nom, même issu du même modèle, reste un conflit tant que l'origine n'est pas établie. Ne pas l'adopter, le réinitialiser ou le modifier.
4. **Bootstrap obtenu, remise non confirmée.** Reprendre aux vérifications restantes. Une divergence de HEAD ne doit pas être résolue en réécrivant le dépôt. Les preuves antérieures restent historiques.
5. **Rejeu terminal.** Rendre le même reçu. Toute vérification de l'état actuel est une lecture distincte du reçu historique.

La garantie ci-dessus est une **exigence du futur adaptateur**, pas une assertion sur le moteur actuel. À la révision examinée, l'exécuteur GRT réessaie la lecture du HEAD sur 409. Si le dépôt est trouvé lors d'une reprise, il compare son manifeste à celui du modèle. Ce contrôle ne prouve pas à lui seul la corrélation à la même demande. L'exécuteur ne persiste le PASS PREP-001 qu'après lecture du premier HEAD. L'adaptateur doit couvrir la corrélation durable et les résultats incertains avant d'exposer une création réelle à un nouvel appelant.

## Rejeu et tests d'acceptation

Le [rejeu hors ligne](../scripts/replay_governed_creation.py) charge le code GRT d'un checkout de référence et remplace le transport par une fixture. Il vérifie un seul POST pour une création acceptée dont la lecture du HEAD reste momentanément en 409, puis la reprise de la même demande, le refus d'un dépôt sans manifeste reconnu et la progression centrale jusqu'au reçu. Il ne déploie ni l'outil MCP ni l'adaptateur. Il ne teste pas l'installation de l'App, la concurrence réelle ni le bootstrap GitHub en direct. Les preuves de bootstrap utilisées dans ce rejeu sont des fixtures.

```sh
python3 scripts/replay_governed_creation.py /chemin/vers/checkout-grt
```

Révision de référence `3d9cba0223ec43003802635dd264f1f266b7b12b`. Pour le futur adaptateur, couvrir aussi le timeout après acceptation, le dépôt homonyme avec le même modèle mais sans corrélation, le 404 non concluant, les reprises concurrentes, la révision périmée, le HEAD divergent et la consultation d'une demande terminée sans écriture. Préserver les entrées GRT existantes par issue et dispatch. Un test réel éventuel utilise une cible isolée, avec identité et autorité vérifiées.

[Registre historique GRT](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/blob/3d9cba0223ec43003802635dd264f1f266b7b12b/docs/control-plane/CASE1_REPLAY_LEDGER.md) · [Exécuteur GRT](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/blob/3d9cba0223ec43003802635dd264f1f266b7b12b/scripts/control_plane_create_repository.py) · [Précédent Gouvern](REPOSITORY_LIFECYCLE_PRECEDENTS.md#grt-et-gouvern--création-puis-entrée) · [Run central Ekyc](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/actions/runs/36293599446).

## Capsule indépendante de référence

Le [noyau portable](../capsules/governed_repository_creation/README.md) implémente
le contrat de reprise sur un journal SQLite et un port d'exécution injecté.
Il représente `PREP-003` comme explicitement non résolu, sans requête
d'infrastructure. Les tests du noyau sont distincts du rejeu historique
GRT. Le port GitHub réel et l'exposition MCP ne sont pas encore raccordés.
Suivi `LOOP-W20` et preuve hors ligne `EV-028`.

## Premier raccordement GitHub App

Le [guide de préflight](GOVERNED_CREATION_GITHUB_APP.md) documente la
hiérarchie, les questions et la vérification de l'installation sur le compte
cible. Ce diagnostic ne remplace pas le port `Gateway` d'écriture et ne
fait pas avancer l'état de création. Suivi `LOOP-W21`, preuve `EV-029`.
