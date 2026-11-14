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
