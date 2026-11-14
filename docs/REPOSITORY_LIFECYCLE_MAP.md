# Carte de reprise — du dépôt GitHub à l'application en service

**Projet** `WT-PROJECT-LOOP-001` · **Continuité** `LOOP-CONV-CONT-20261113-ROOT-01`
· **Sujet** `LOOP-SUJ-020` · **Reprise du sujet** `LOOP-W18`.

Cette carte réunit les éléments du fil de travail visible du 13 novembre
2026. Elle indexe les échanges et décisions, sans prétendre archiver les
messages mot pour mot ni leurs heures exactes. La [chronologie](../memory/2026-11-13-loop.md)
porte les événements et le [registre des preuves](../registry/evidence.json)
porte leurs sources. Les [précédents](REPOSITORY_LIFECYCLE_PRECEDENTS.md)
portent les observations historiques. Cette carte n'est ni une nouvelle
autorité MCP ni un nouvel état d'exécution.

## 1. Fil des échanges et évolution de la compréhension

| Repère local | Question ou travail | Résultat à conserver |
| --- | --- | --- |
| X01 | Retrouver la procédure des trois périmètres GitHub vers S1/S2, et la noter **dans Loop** | Inventaire, registre, questionnaire, sélection de l'hébergement et mise en service sont des maillons distincts. Le planificateur de rattachement existe dans la PR #2. |
| X02 | « Governed Deploy Application c'est quoi ? » | La mise en service contrôlée d'une version d'application exige une source exacte, une cible vérifiée, une admission, une recette et une preuve. Ne pas la confondre avec la mise à jour de MCP. |
| X03 | « Bon il commence ou ? » | La première réponse a situé le départ au préflight d'un SHA. Cela décrit le **sous-cycle de mise en service**, pas le début du parcours historique complet. Cette limite est corrigée par X04. |
| X04 | Rechercher le vrai départ dans MCP et les pistes Regulatory | L'addendum MCP #349 place l'entrée à la sélection du dépôt, puis vérification de la connexion Bridge, recherche du lien et bifurcation premier rattachement, reprise ou réconciliation. Le dépôt Regulatory de l'organisation est attesté. La piste `Patricked-code/Regulatory` n'a pas pu être vérifiée. |
| X05 | Vérifier les échanges GRT / Gouvern / UAES avec MCP et le rôle de CUG | GRT a créé Gouvern à partir du template et a lu MCP. Le premier bootstrap est GitHub, la découverte MCP est ultérieure. Le statut Git de Gouvern a divergé de la preuve historique. Pour UAES, bypass de ruleset, couverture d'installation App, accès Bridge et runtime sont des preuves différentes. |
| X06 | Mémoriser les précédents et reconstituer Regulatory | Gouvern a été généré. Regulatory a été constitué progressivement à partir d'un dépôt initial avec README. Build et tests HTTP de Regulatory attestés, préparation S1 bloquée par deux cibles incompatibles, mise en service non attestée. Voir E20 à E25 et EV-021 à EV-026. |
| X07 | Vérifier ce qui est faisable de la création au déploiement | Création depuis GRT et bootstrap observés sur pilotes. Configuration versionnée et build distincts du paramétrage GitHub et des droits MCP. Pas d'exécution universelle attestée jusqu'au serveur pour un nouveau dépôt. |
| X08 | Confirmer le dépôt Loop | Accès GitHub observé et PR #2 identifiée. Cette observation n'atteste aucun lien de Loop avec S1 ou S2. |
| X09 | Localiser les réponses précédentes | Le texte original reste dans la conversation visible. Loop conserve des décisions et preuves navigables, pas une transcription exhaustive. |
| X10 | Reconstituer la hiérarchie et retrouver les étapes, capacités et cycles | La présente carte associe le fil des questions, les capacités et leurs sorties, les exemples historiques et la reprise du sujet. |

[Décision d'entrée MCP #349](https://github.com/Patricked-code/MCP/issues/349#issuecomment-6461939290)
· [Précédents et preuves](REPOSITORY_LIFECYCLE_PRECEDENTS.md).

## 2. Hiérarchie de travail et responsabilités

Le **projet Loop** est le conteneur. Le sous-projet `LOOP-SP-02`
porte l'entrée, la découverte et le rattachement. Le **sujet**
`LOOP-SUJ-020` porte la préparation de l'hébergement. La **capacité**
`LOOP-CAP-006` est le planificateur réutilisable de ce sujet. Les
**travaux** `LOOP-W16`, `LOOP-W17` et `LOOP-W18` décrivent
respectivement l'extraction du contrat, son implémentation hors ligne
et le raccordement restant. Le [module d'entrée et le planificateur
d'onboarding](../registry/modules.json) sont des composants voisins,
pas des synonymes de cette capacité.

La **continuité** traverse cette hiérarchie. Elle donne accès aux
événements, preuves et points de reprise sans être une étape du
workflow, une session MCP ou une autorisation. Le checkpoint global
du projet et la reprise particulière de `LOOP-W18` restent distincts.
[Entrée canonique](LOOP_CANONICAL_REGISTRY.md) · [Travaux et dépendances](../registry/work.json).

## 3. Processus, entrées, sorties et niveau de preuve

Les noms des étapes ci-dessous structurent la lecture. Ils ne créent
pas de nouveaux identifiants de modules ni de nouveaux workflows déployés.

| Bloc | Quand il commence et ce qu'il reçoit | Ce qu'il remet au bloc suivant | Où en est-on |
| --- | --- | --- | --- |
| Créer ou adopter un dépôt | Intentions, propriétaire, nom, visibilité, ou dépôt existant identifié | Dépôt exact, ID GitHub et premier commit. Reçu de bootstrap si applicable. | Création et bootstrap GRT observés sur Gouvern et Ekyc. Regulatory illustre la constitution progressive d'un dépôt existant. |
| Entrer et reconnaître | Dépôt sélectionné, identité et contexte du client, état du projet | Identité du dépôt et du projet, entrée nouvelle ou reprise, contexte de travail. | Contrats et noyaux Loop en brouillon. Le mandat historique n'atteste pas un déclenchement automatique depuis chaque client. |
| Vérifier l'accès GitHub et la connexion MCP | Dépôt exact et contexte d'authentification | Preuves séparées de couverture App et de lecture Bridge, ou blocage précis. | GRT et Gouvern ont des preuves de lecture. Bypass CUG sur UAES n'est ni preuve d'installation nominative ni droit serveur. |
| Lire le registre et observer S1/S2 | Clé stable du dépôt, projet, environnement et rôle demandés | Correspondances et preuves du chemin réel, ou absence de lien vérifiée, ambiguïté ou inconnu. | La page Git lit la correspondance. Le sélecteur MCP exige une source V2. Le relevé runtime est V1 avec simulation V2, pas une migration. |
| Planifier l'hébergement | Demande et observations qualifiées | Réutilisation, choix, preuve manquante, conflit ou plan. | `LOOP-CAP-006` est appelable via `plan_repository_hosting`, testé hors ligne. Raccordement réel `LOOP-W18` restant. |
| Rattacher ou provisionner | Plan exact et opération autorisée | Répertoire attesté, lien enregistré et relu par l'autorité, ou checkpoint de réconciliation. | Capacités MCP partielles et bornées. Aucune exécution universelle S1/S2 attestée pour un dépôt arbitraire. |
| Concevoir, construire et qualifier la version | Objectif du projet, gouvernance, plan et code | Version candidate traçable. Commit exact admis par les règles du projet, sur `main` si exigé, avec preuves de build et de contrôle. | Peut avancer sans production. Build et tests Regulatory attestés, pas son déploiement. La promotion de la version est en amont de la mise en service. |
| Mettre en service l'application | Demande de livraison, dépôt, SHA exact, cible relue et autorisation | Exécution, SHA ou artefact en service, santé, et retour arrière ou point de reprise en cas d'échec. | Governed Deploy Application n'est pas MCP Governed Deploy. Blueprint MCP de planification, pas exécuteur universel. |
| Conserver les preuves et reprendre | Résultat et preuves de chaque bloc | État attesté, décisions ouvertes et prochaine action, sans repartir de zéro. | Mémoire, registres et suivi versionnés dans la PR #2. Pas de publication intégrale du fil. |

Le planificateur distingue `REUSE_VERIFIED`, `PLAN_ATTACH_EXISTING`,
`PLAN_PROVISION`, `NEEDS_CHOICE`, `CONFLICT`, `UNOBSERVED` et
`NO_HOSTING_REQUESTED`. Une vue indisponible ou partielle ne prouve
pas l'absence. L'ID GitHub stable, le compte propriétaire, l'identité
de connexion et l'installation App sont distincts. Un dépôt peut
n'avoir aucune cible ou en avoir plusieurs, distinguées par serveur,
environnement, rôle et chemin réel. Un checkout, un répertoire de
runtime et une adresse HTTP ne sont pas la même ressource.
[Contrat d'hébergement](WORKFLOW_REPOSITORY_HOSTING.md)
· [Ancrage du projet](PROJECT_ANCHOR.md).

## 4. Le nom du workflow et ses deux points d'appel

**Nom fonctionnel dans Loop** — *Rattachement et préparation d'un
hébergement applicatif*, `LOOP-CAP-006`. On l'appelle **à l'arrivée** si le
dépôt doit être reconnu ou rattaché, ou **depuis le préflight de mise en
service** si la cible manque ou n'est plus vérifiée. Il peut s'achever
sans déploiement. Si un plan est exécuté, le résultat à transmettre
est le **lien vérifié et relu**, pas le plan seul. Si un répertoire a
été créé mais que l'inscription a échoué, reprendre l'inscription et
la relecture, sans recréer le répertoire.

Le programme historique **Governed Deploy Application**, au sens
large, commence à la sélection du dépôt. Son **sous-cycle de mise en
service** ne commence que lorsque le dépôt et la version candidate
sont désignés et que la livraison est demandée. Une fusion sur `main`
ne donne pas à elle seule le droit de déployer. Un résultat vert sur
le build ne prouve pas la santé du runtime. Un déploiement vert de
MCP ne prouve pas celui de l'application.
[Déclencheur historique](https://github.com/Patricked-code/MCP/issues/349#issuecomment-6461939290)
· [Point d'appel et sortie](WORKFLOW_REPOSITORY_HOSTING.md#jonction-vérifiée-et-point-dappel-du-workflow).

## 5. Reprendre sans relire tout le fil

1. Reprendre la continuité `LOOP-CONV-CONT-20261113-ROOT-01`.
2. Pour ce sujet, ouvrir `LOOP-W18` et son [suivi](../SUIVI.md).
3. Vérifier le raccordement de lecture sur trois scénarios. Un lien
   attesté, un répertoire existant sans lien actif, puis une vue
   non concluante. Préserver le refus en cas de conflit.
4. Ne pas modifier GitRegistry, S1/S2 ou Regulatory pour valider cette
   tranche. L'admission et le provisionnement restent une suite distincte.

## 6. Branche créer un dépôt neuf — LOOP-W19

Le [contrat portable de création](GOVERNED_REPOSITORY_CREATION_CONTRACT.md)
isole la branche créer du premier maillon et le bootstrap automatique du
deuxième, jusqu'à `HANDOFF_READY`. Il ne couvre ni le premier passage local
jusqu'à `LOCAL_HANDOFF_READY` ni l'hébergement. Le contrat et le rejeu
hors ligne sont suivis par `LOOP-W19` et `EV-027`. Le parcours d'hébergement
et sa prochaine action `LOOP-W18` ne changent pas.
