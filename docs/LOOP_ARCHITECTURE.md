# Architecture de travail de Loop

Statut : version candidate de la PR #2. Aucun déploiement.
Le noyau de Loop ne dépend pas du serveur MCP. Un adaptateur peut lire des
preuves provenant de GitHub, de MCP ou d'une autre autorité configurée.

## Composants et contrats

| Composant | Entrées | Sortie | Frontière |
|---|---|---|---|
| Entrée et découverte | Demande, dépôt, branche, révision et sources | Identité exacte ou divergence, parcours neuf/existant | Pas de dépôt implicite, pas d'inscription automatique. |
| Contrôle de rattachement | Reconnaissance, ID projet, preuve App et procédure | Contexte transmis ou cause de blocage | Autorisation distincte. Client direct hors Loop non intercepté. |
| Planificateur | Dépôt connu, inconnu ou non vérifiable, choix de projet et preuve App | Action proposée et clé de relance | L'autorité externe déduplique et applique. Aucune installation CUG. |
| Inventaire GitHub | Trois périmètres, source en lecture, SHA et contenu borné | Fiches, classifications et relations sourcées | Pas d'exécution des workflows ni du code inspecté. |
| Registre et preuves | Snapshots HTML ou JSON, provenance, demandes et décisions | SQLite privé historisé, index Git public et mémoire | Pas de duplication du détail privé dans Git. |
| WF-00 | Identité, inventaire, état initial et autorités | Dossier documentaire, incohérences et checkpoint | Squelette minimal neuf ou réconciliation de l'existant. |
| Conception et planification | Dossier, exigences et contraintes | Cartes fonctionnelle et technique reliées, lots et critères | Les inconnues restent visibles. Prêt à développer ne vaut pas prêt à déployer. |
| Exécution et continuité | Lot validé, autorisations et conditions propres à la cible | Code, tests, preuves, checkpoint et suite | Développement, synchronisation et déploiement sont des opérations distinctes. |

## Méthode et séquence

1. **Identifier et conserver** la demande, le projet exact, sa provenance et
   le contexte observé. Distinguer fait, hypothèse, décision et action.
2. **Inventorier avant de créer**. Relier les autorités et l'existant
   par WF-00. Conserver l'historique et signaler les contradictions.
3. **Qualifier et concevoir**. Examiner besoins, acteurs, périmètre, accès,
   infrastructure, moyens, données, période, autorisations, risques,
   acceptation, mise en service et reprise. Ne choisir que les vues utiles.
4. **Planifier par lot**. Lier chaque unité à ses exigences, à ses
   prédécesseurs et à ses preuves de réception.
5. **Vérifier le passage**. Une preuve statique, un candidat de registre
   et une attestation opérationnelle ne sont pas interchangeables.
6. **Réaliser et attester** uniquement dans un périmètre autorisé. Inscrire
   les résultats, les limites et la prochaine action dans la mémoire.

## Conservation et autorités

- `memory/` tient la chronologie de ce chantier. `registry/work.json`
  versionne les demandes et unités. `registry/evidence.json` indexe leurs preuves.
- `docs/SOURCE_REGISTER.md` conserve son rôle d'inventaire historique.
  `SOURCE_OF_TRUTH.md` et `GOVERNANCE.md` restent distincts.
- La base privée référence un snapshot par identifiant et empreinte SHA-256.
  Les tables `snapshot`, `repository` et `observation` séparent le relevé,
  la fiche et ses observations. Un nouvel état reçoit un autre snapshot ID.
  Le fichier privé fourni n'est pas une base déployée sur un serveur.
- L'import HTML conserve les sections et liens visibles du rapport. Les
  nouvelles collectes doivent privilégier JSON pour conserver les champs
  structurés directement. Aucune valeur manquante n'est reconstituée.
- Une connexion réellement liée exige une preuve de runtime corrélée.
  Une relation avec un serveur exige une preuve du checkout exact.
  L'App CUG, l'inscription et l'autorisation restent des preuves distinctes.

Voir [la mémoire](../memory/README.md), [le contrat d'inventaire](MCP_INVENTORY.md),
[WF-00](WORKFLOW_WF00.md), [le contrat de passage](WF00_DESIGN_PLANNING_CONTRACT.md),
[le squelette des cartes parallèles](PARALLEL_ARCHITECTURE_SKELETON.md)
et [la feuille de route](LOOP_ROADMAP.md).

## Registre descendant

Le projet et ses six sous-projets internes ont leurs propres identifiants. Les [contrats de modules](../registry/modules.json) précisent modes, entrées, opérations, sorties et limites. L'[entrée canonique](LOOP_CANONICAL_REGISTRY.md) distingue parenté et relations de traçabilité.

L'[ancrage canonique](PROJECT_ANCHOR.md) relie l'ID projet au dépôt et à ses
répertoires. Le noyau valide des données injectées. La collecte et la
persistance des rattachements appartiennent aux adaptateurs de l'autorité.

La [préparation d’un hébergement](WORKFLOW_REPOSITORY_HOSTING.md) est une
capacité distincte de l’entrée, de l’index d’ancrage et du déploiement.
Elle rend un plan et un point de reprise, jamais une autorisation.
