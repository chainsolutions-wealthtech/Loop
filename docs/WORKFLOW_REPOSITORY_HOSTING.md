# Rattachement et préparation d’un hébergement applicatif

**Capacité Loop** `LOOP-CAP-006` · **Travail** `LOOP-W16` · **État** spécifié dans la branche de travail, non exécutable.
**Précédent MCP** [issue #349](https://github.com/Patricked-code/MCP/issues/349), continuité historique `GD-U-CONT-20261030-ROOT-01`.

## Ce que MCP possède et ce qu’il manque

| Maillon | Existant vérifié | Limite à ne pas franchir par supposition |
| --- | --- | --- |
| Comptes, dépôts et hébergement | [Configuration des comptes](https://github.com/Patricked-code/MCP/blob/c775709fdaf490eef2e1d43345e0b26e460a072c/data/github-accounts.json), [GitRegistry](https://github.com/Patricked-code/MCP/blob/c775709fdaf490eef2e1d43345e0b26e460a072c/src/github/registry.ts) et version Git [du registre](https://github.com/Patricked-code/MCP/blob/c775709fdaf490eef2e1d43345e0b26e460a072c/data/mcp-git-registry.json). | Le registre en service répond encore **V1**. La simulation V2 en lecture seule compte 3 connexions, 6 dépôts projetés, 5 mappings et 1 migration en attente. Des chemins restent non vérifiés. Ce n’est ni la liste exhaustive des dépôts des trois comptes, ni un registre V2 activé. |
| Question de rattachement | La [complétion du contexte](https://github.com/Patricked-code/MCP/blob/c775709fdaf490eef2e1d43345e0b26e460a072c/src/governedContext/contextCompletion.ts#L131-L169) alimente la page Git. Elle distingue absence, choix entre plusieurs mappings, présence et absence d’observation. | Un mapping présent n’est pas attesté. La [sélection de l’hébergement](https://github.com/Patricked-code/MCP/blob/c775709fdaf490eef2e1d43345e0b26e460a072c/src/provisioning/repositoryPleskHostingRoute.ts) exige un registre source V2, un mapping et un rattachement de production uniques et prêts. Zéro mapping dans un registre valide appelle la découverte, pas la création. La fonction a été retrouvée dans son module et ses tests, pas dans le parcours de la page Git. |
| Découverte et création | [PR #350](https://github.com/Patricked-code/MCP/pull/350) fusionnée. [Prévisualisation Plesk S1/S2](https://github.com/Patricked-code/MCP/blob/c775709fdaf490eef2e1d43345e0b26e460a072c/src/tools/pleskProvisioning.ts), planificateur et exécuteur borné de sous-domaine, et [routes de provisionnement](https://github.com/Patricked-code/MCP/blob/c775709fdaf490eef2e1d43345e0b26e460a072c/src/server.ts#L508-L745) dans le code. | La prévisualisation ne crée rien. Le parcours Project Runtime lu est câblé **sur S1**. Le sous-domaine n’est pas le sous-chemin d’un hôte existant. La [PR #362](https://github.com/Patricked-code/MCP/pull/362), non fusionnée au relevé, propose de renforcer la validation des chemins avant réutilisation. |
| Accès et admission | [PR #355](https://github.com/Patricked-code/MCP/pull/355), [#357](https://github.com/Patricked-code/MCP/pull/357) et [#361](https://github.com/Patricked-code/MCP/pull/361) fusionnées. Le code actuel possède un pont web Plesk vers les autorités existantes. Le [checkpoint historique](https://github.com/Patricked-code/MCP/issues/349#issuecomment-6529432146) distingue preuve d’accès GitHub App, admission OAuth/E3, tâche, session, claim, verrou, CI et revue. | La présence du code et une permission observée ne prouvent pas une opération Plesk admise. Le pilote GRT `/gouvern` conserve une garde qui refuse l’écriture sur le SHA lu, et [sa PR #351](https://github.com/Patricked-code/MCP/pull/351) reste brouillon. Ce refus explicite du pilote ne doit pas être généralisé à toutes les routes Plesk. |
| Orchestration et recette | Le [blueprint universel](https://github.com/Patricked-code/MCP/blob/c775709fdaf490eef2e1d43345e0b26e460a072c/src/provisioning/universalDeploymentBlueprint.ts) compose source, hôte, build, déploiement, vérification et retour arrière. Le [run #39884876866](https://github.com/Patricked-code/MCP/actions/runs/39884876866) a bien déployé le **MCP** après #350. | Le blueprint ne lance aucune action, et l’adaptateur sous-chemin n’y est pas attesté. Aucun résultat bout en bout du parcours universel application n’a été établi par les sources examinées. |
| Pilote Regulatory | Le [mandat du pilote #352](https://github.com/Patricked-code/MCP/pull/352) vise un sous-chemin sur S1. Le [manifeste produit au SHA lu](https://github.com/chainsolutions-wealthtech/Regulatory/blob/15933ff9ea1e9b83ae5c1cb23725169667af4969/deploy/mcp-target.json) vise un sous-domaine. [Issue produit #3](https://github.com/chainsolutions-wealthtech/Regulatory/issues/3), [PR #353](https://github.com/Patricked-code/MCP/pull/353) et [#364](https://github.com/Patricked-code/MCP/pull/364) documentent l’écart et l’admission. | Choix de cible et manifeste à réconcilier, puis adaptateur ingress adapté. Une prévisualisation de sous-domaine ne satisfait pas le mandat sous-chemin. |

**Frontière de preuve.** Relevé du 13 novembre 2026. Source MCP `main` au SHA
`c775709fdaf490eef2e1d43345e0b26e460a072c`. Le constat V1 est confirmé
par une simulation runtime MCP réussie et sans écriture. Les autres états
runtime et les permissions par dépôt ne se déduisent ni de ce relevé
ni de la configuration des comptes. La [PR d’archives #356](https://github.com/Patricked-code/MCP/pull/356)
conserve la filiation historique, pas l’autorité opérationnelle.

### Deux difficultés concrètes à conserver dans l’historique

- Le [checkpoint B3i](https://github.com/Patricked-code/MCP/blob/c7d7b44b1fedf1954e63b0d921f992362daae4b3/docs/history/governed-deploy-integral/13_20261029_EXECUTION_B3I_CONTINUITE.md) documente l’absence initiale de liaison prouvée entre la session web et le transport OAuth MCP. L’issue #349 documente ensuite le contrôle manquant du reçu de bootstrap dans le lecteur d’autorité et une tentative de correction. Ce sont des défauts historiques, pas un diagnostic d’échec de la route en production aujourd’hui. [Constat et correction historique](https://github.com/Patricked-code/MCP/issues/349#issuecomment-6513464182).
- Stablecoin montre pourquoi l’absence d’un mapping **actif** ne doit pas lancer une création. Un checkout S2 a déjà été observé, mais le contrôle d’entrée n’a pas attesté l’activation du lien. L’étape correcte est la réconciliation du lien, pas un second checkout. [Test Loop](PROJECT_ANCHOR.md).

## Contrat portable de Loop

**Déclenchement.** Le parcours d’entrée, un opérateur ou le planificateur
de déploiement appelle cette capacité lorsqu’il faut obtenir un
rattachement vérifié. Une absence autoritaire déclenche une découverte.
Une observation indisponible déclenche un diagnostic en lecture seule,
sans la convertir en absence. L’inventaire des trois périmètres
(`chainsolutions-wealthtech`, `Patricked-code`, `Wealthtechinnovations`)
est une entrée, pas un droit. Ne pas ajouter une cible à tous les dépôts
automatiquement.

**Entrées.** Hôte et ID stable du dépôt, compte propriétaire, ID global
retrouvé ou décision explicite de création, éventuel SHA source,
environnement et rôle, choix opérateur s’il existe, observations versionnées
des registres et de l’hébergement. Le compte GitHub propriétaire, l’identité
de connexion et l’installation GitHub App sont trois champs distincts.

| État observé | Transition | Sortie attendue |
| --- | --- | --- |
| Rattachement vérifié pour le rôle et l’environnement demandés | Réutiliser et relire l’ID global. | `REUSE_VERIFIED`, référence du lien. Aucune création. |
| Plusieurs cibles valides ou contradiction | Choisir un rattachement ou réconcilier les sources. | `NEEDS_CHOICE` ou `CONFLICT`. Aucune sélection tacite. Plusieurs répertoires d’un projet ne sont pas une ambiguïté si leurs rôles les distinguent. |
| Registre ou observation indisponible | Identifier la preuve ou l’autorité manquante. | `UNOBSERVED`. Aucun nouvel ID, répertoire ou déploiement. |
| Pas de rattachement, répertoire candidat déjà présent | Attester le chemin réel, le rôle, le dépôt ou la provenance, l’absence de collision et les droits exacts. Préparer le rattachement. | `PLAN_ATTACH_EXISTING`. Écriture du lien seulement via l’autorité, suivie de sa relecture. |
| Pas de rattachement ni de répertoire, absence prouvée | Demander les décisions nécessaires et préparer un plan. | `PLAN_PROVISION`. L’autorité approuve l’action et le périmètre avant toute création. |
| Aucun hébergement demandé | Conserver le dépôt dans l’inventaire sans cible. | `NO_HOSTING_REQUESTED`. Aucun serveur forcé. |

**Questions conditionnelles.** Projet existant ou nouveau si l’ID n’est
pas connu. Rattacher ou créer si les deux sont possibles. S1 ou S2,
environnement et rôle si indéterminés. Hébergement privé, sous-chemin,
sous-domaine ou domaine si une exposition est nécessaire. Runtime,
dépendances, branche/SHA et recette seulement si le périmètre va jusqu’au
déploiement. Réutiliser les réponses déjà attestées.

**Séquence d’exécution future.** Lire et résoudre → découvrir et qualifier →
rendre le plan et ses preuves → obtenir l’admission par l’hôte → rattacher
ou provisionner → attester le répertoire et relire le lien enregistré →
remettre le résultat au cycle de déploiement applicatif **seulement si
demandé et admis séparément**. Celui-ci fixe la révision, valide l’artefact,
la santé et la possibilité de retour arrière. Un répertoire prêt ne vaut
pas une application déployée. Réessayer la même demande doit retrouver
l’opération et le lien existants. Si une étape a abouti mais que l’écriture
ou la relecture du lien échoue, rendre un état à réconcilier et reprendre
depuis les preuves, sans recréer le répertoire.

**Interface.** Le cœur ne choisit pas une autorité et ne modifie rien.
L’adaptateur fournit lecture du dépôt et de l’installation, lecture et
écriture gouvernée du registre, découverte d’hébergement, exécution
bornée et attestations. Les sorties incluent ID global, clé dépôt,
références privées des cibles, état, décision ou preuve manquante,
référence du plan et point de reprise. Ne jamais recopier de chemins
privés ou de credentials dans Loop public.

**Prochaine tranche.** Implémenter et tester hors ligne le routage et
ses refus. Puis valider avec un adaptateur de lecture l’existence d’un
rattachement et l’absence réelle d’un autre, séparément de la création.
Garder l’exécution et la recette applicative dans des tranches distinctes.
