# Préparation web d'une création gouvernée

Ce prototype est un écran local de préparation et de reprise. Il ne crée
aucun dépôt, ne publie aucune information et n'ouvre aucune session
gouvernée d'exécution. Aucun accès à GitHub Apps ni au MCP dans cet écran.

## Parcours et frontières

| Passage | Sortie attendue |
| --- | --- |
| Ouvrir la demande | Identifiant durable et premier événement avant toute réponse. |
| Qualifier | Compte propriétaire, nom exact, visibilité, modèle de travail, mission et périmètre, puis questions conditionnelles. |
| Préparer la remise | Vue des choix, décisions reportées, modèle GRT épinglé et plan documentaire. |
| Vérifier l'autorité, futur | Hôte web authentifié, décision du demandeur, installation CUG et droits effectifs. Conserver la référence à la demande préparatoire. |
| Créer et vérifier, futur | Exécuteur distinct, reçu GitHub, bootstrap attesté et `HANDOFF_READY`. |
| Entrer dans le projet, futur | Entrée locale, session ou travail selon le contrat du dépôt, baseline approuvée et `LOCAL_HANDOFF_READY`. |
| Héberger ou déployer, hors de ce parcours | Workflow et autorisation propres, cible et révision attestées. |

Le journal SQLite local est une **projection de démonstration**, pas une
nouvelle autorité de production. Il reprend les distinctions du modèle
GRT entre demande/run, réponses, événements, preuves, checkpoints et
remises. Il ne synchronise pas la base GRT ni le stockage d'exécution de
la capsule. En production, rattacher l'historique à l'identité authentifiée
et relier l'ID de préparation, la demande de création, l'ID GitHub, le
run et la session locale. Aucun secret ne doit entrer dans le journal.

## Sources et niveaux de preuve

La projection `grt_catalogue.json` référence GRT au commit
`3d9cba0223ec43003802635dd264f1f266b7b12b`, modèle `2.8.43`.
Les 216 entrées du manifeste sont indexées avec leur type et SHA Git,
dont 71 dans la catégorie réservée à la source. Les entrées ne sont pas
une liste de fichiers à recopier à l'aveugle. Une entrée de type arbre
désigne un répertoire. Le plan rendu par l'interface est une projection
et non une attestation de présence dans le dépôt futur.

Le catalogue adaptatif de GRT comprend 35 questions, dont 24 applicables
à la création. Son statut à la source est `PLANNING_ONLY_NOT_RUNTIME_BOUND`.
Le prototype projette ces 24 questions, quatre choix structurants et
cinq questions de cadrage reprises de la baseline locale. Les questions
à options observées n'inventent aucun serveur ou environnement. Elles
ne montrent que les choix statiques, avec possibilité de report. Si
« sans MCP » est choisi, les questions de transport et de périmètre
MCP ne sont pas posées. La baseline historique reste appliquée et
approuvée par le parcours local, pas par cet écran.

## Architecture documentaire du futur dépôt

1. **Autorités** — `00_START_HERE.md`, `GOVERNANCE.md`, `AGENTS.md`,
   `SOURCE_OF_TRUTH.md`, Loop Engineering, conditions de fin, risques.
2. **État, architecture et continuité** — `PROJECT_CONTEXT.md`,
   `STATUS.md`, `NEXT_ACTION.md`, `HANDOFF.md`, `docs/ARCHITECTURE.md`,
   décisions et modèles ADR.
3. **État machine** — manifeste, profil, modèle de workflow, plan
   d'accès, intentions d'infrastructure, mémoire, sessions, travaux et
   preuves du bootstrap. Différencier valeurs du modèle, valeurs du
   projet, faits observés et données privées.
4. **Automatisation** — bootstrap, validation, entrée locale et
   workflows candidats du modèle. Les fichiers de pilotage central
   réservés à la source n'ont pas vocation à rester dans le client.
   La présence d'un workflow ne prouve pas qu'il a tourné ni qu'il est autorisé.

Il y a **deux modèles de travail GRT** et non seulement deux fichiers Actions.
`STANDARD_GOVERNED_FLOW` couvre le travail gouverné courant.
`REGULATORY_AFRICAFUNDS_GOVERNED_FLOW` ajoute notamment analyse d'impact,
réservation, non-régression et vérification de livraison si autorisée.
Ils ne remplacent pas les workflows techniques central, bootstrap, local
et exécution. Le choix préparatoire est visible avec ses étapes. La
baseline locale enregistre le modèle retenu dans
`.governance/workflow-model.json`.

## Interface locale

```sh
python3 -m capsules.governed_repository_creation.intake.web --db /chemin/prive/intake.sqlite
```

Ouvrir `http://127.0.0.1:8765`. Écoute locale seulement et identité de
démonstration. Pas d'OAuth, de service publié ni de passerelle de création.
Le prochain travail est de qualifier l'identité de la personne dans
l'interface, puis relier la préparation au préflight CUG et à une preuve
de remise, sans déclencher de génération ou de déploiement à la fin du formulaire.

[Manifeste GRT](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/blob/3d9cba0223ec43003802635dd264f1f266b7b12b/.governance/TEMPLATE_MANIFEST.json)
· [Catalogue adaptatif](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/blob/3d9cba0223ec43003802635dd264f1f266b7b12b/.governance/control-plane-state/adaptive-question-catalogue.json)
· [Modèle du registre GRT](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/blob/3d9cba0223ec43003802635dd264f1f266b7b12b/docs/control-plane/DATA_MODEL.md)
· [Modèles de workflow](https://github.com/chainsolutions-wealthtech/Governed-Repository-Template/blob/3d9cba0223ec43003802635dd264f1f266b7b12b/.governance/workflow-model.json).

## Jonction de la demande à CUG — LOOP-W23

L'hôte authentifié peut injecter `resolve_actor` et le service `CUGPreflight`
dans le prototype. Le résolveur est un adaptateur **côté serveur** : il ne
doit pas faire confiance à un identifiant transmis dans un formulaire ni
à un en-tête client. Le helper `verify_user` observe `GET /user` avec le
jeton utilisateur déjà obtenu par l'hôte et prend l'ID GitHub stable.
Il ne réalise pas lui-même l'échange OAuth. Le mode local par défaut
garde son identité de démonstration et n'affiche pas le préflight.

Le service exige la demande complète de cet acteur, la révision exacte et
une décision positive de la politique hôte pour le compte demandé. Cette
politique autorise une **observation**, pas une création. Le JWT CUG
n'est demandé qu'après ces contrôles. L'adaptateur vérifie l'App 5417646,
son installation et le modèle attendu. Le journal lie le résultat au SHA
du dossier et à la révision observée. Un résultat tardif ne remplace pas
une révision plus récente. Le rapport ne reçoit ni jeton, ni clé, ni
réponse HTTP brute. Les diagnostics ne rendent jamais
`creation_authorized: true`. Un `404` reste non concluant.

Le dossier historique ouvert en mode démonstration n'est pas
automatiquement réattribué à un utilisateur GitHub. Une éventuelle
réconciliation de ces dossiers relève d'une décision explicite de
l'hôte. Le modèle GRT est encore épinglé à la révision de la préparation.
Si le HEAD courant a évolué, réconcilier les sources avant un autre essai.

Prochain contrôle : fournir un résolveur de session et une politique
d'accès réels sur un hôte de confiance, puis vérifier un préflight CUG
nominatif en lecture. Ne pas confondre son résultat avec le droit
d'ouvrir une session d'exécution ou de créer un dépôt.

## Envoi groupé dans Loop — LOOP-W24

Une demande inachevée donne accès à **Ouvrir le questionnaire groupé**.
Loop présente les questions restantes sur une page, par thème, et
affiche en lecture seule les réponses déjà enregistrées. Les options
structurées viennent du même catalogue que le parcours séquentiel.
Les suggestions de cadrage ne sont pas présélectionnées. Le nom du dépôt
et les réponses libres restent saisissables. Une réponse facultative vide
ou explicitement reportée reste à trancher, même si la préparation est
terminée. Les questions conditionnelles sont signalées et désactivées
dans le navigateur quand elles ne s'appliquent pas. Le serveur applique
les mêmes conditions, y compris sans JavaScript.

**Envoyer toutes les réponses** enregistre les choix applicables dans
le journal de la même demande, dans l'ordre du catalogue et dans une
seule transaction SQLite. L'acteur, la révision, les champs et les choix
sont contrôlés avant l'enregistrement. Si la demande a changé depuis
l'ouverture du formulaire, le lot est refusé et la demande doit être
rouverte. Si un choix est invalide à révision inchangée, le formulaire
est réaffiché pour correction sans écrire le lot. Il n'y a ni
import JSON manuel ni migration du journal.

Le parcours séquentiel reste disponible et produit les mêmes événements.
Le plan et l'empreinte d'une préparation sont équivalents pour les mêmes
réponses. Après l'envoi, Loop revient au dossier et indique que la
préparation est terminée. Le préflight CUG reste une action séparée,
disponible seulement dans le mode prévu à la section précédente.
Aucune création GitHub ou Plesk, inscription GitRegistry, session
d'exécution ou opération de déploiement n'est déclenchée par le lot.
