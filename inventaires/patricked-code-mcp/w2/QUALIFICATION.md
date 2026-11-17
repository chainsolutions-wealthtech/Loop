# W2 — Qualification et critères d’acceptation

Qualification documentaire du corpus inventorié en W1. Cette vue dérive du [registre de données W2](exigences-w2.json). Un candidat vérifiable n’est ni une règle Loop adoptée, ni un contrôle runtime exécuté.

## Lire la qualification

- **Commun candidat** désigne un principe transposable, soumis à revue avant adoption.
- **Profil candidat** désigne une règle qui ne s’applique que si le projet sélectionne ce type de situation.
- **Historique non prescriptif** désigne un choix ou besoin local conservé comme preuve, sans promotion au tronc commun.
- **R01–R15** conservent leurs identifiants historiques. **W2-G01/G02** sont des synthèses proposées ici et ne sont pas des identifiants de la matrice d’origine.

## R01 — Reprendre la mémoire et le dernier état vérifié

**Qualification** — `commun-candidat` · Périmètre `reprendre`.

Avant de déterminer le travail, résoudre la source d’autorité, la version du dossier et le checkpoint applicable. Identifier une contradiction ou une lacune au lieu d’inventer la reprise.

- **Critère positif** — Un projet existant dispose d’un checkpoint vérifié et de références versionnées. Le dossier d’entrée cite l’autorité, l’état, la révision et la prochaine action applicables.
- **Cas négatif ou arrêt** — Deux checkpoints incompatibles ou aucune référence vérifiable. Le dossier conserve l’ambiguïté et n’attribue pas un travail à partir d’un état supposé.
- **Preuve attendue** — Fiche d’entrée, référence de checkpoint, liste des écarts.
- **Ce qui n’est pas transféré** — Ordre de lecture et noms GPT.md, SUIVI.md ou équivalents définis pour chaque projet.

Sources — [H-LOOP-004, L9–9](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md#L9) · [H-LOOP-002, L60–75](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_MASTER_PLAN_20260702.md#L60-L75) · [H-LOOP-003, L44–54](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L44-L54) · [H-LOOP-001, L552–569](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_INSTRUCTIONS_DOCX_EXTRACT_20260702.md#L552-L569).

## R02 — Gouverner une action irréversible

**Qualification** — `commun-candidat` · Périmètre `action-irreversible`.

Avant CHAQUE action irréversible, identifier la cible exacte, les dépendances et effets, puis vérifier la validation qui s’applique à cette action et cible.

- **Critère positif** — La cible, ses dépendances, les impacts et l’autorité sur l’opération sont attestés séparément. Le dossier rend le candidat examinable, sans exécuter l’action.
- **Cas négatif ou arrêt** — Cible ambiguë, impact incomplet ou autorisation absente. L’action reste non admissible, même si la connexion technique fonctionne.
- **Preuve attendue** — Inventaire versionné, analyse d’impact, référence de décision applicable.
- **Ce qui n’est pas transféré** — Forme de la matrice et contrôle effectif propres au profil.

Sources — [H-LOOP-004, L10–10](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md#L10) · [H-LOOP-003, L23–32](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L23-L32) · [H-LOOP-001, L552–569](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_INSTRUCTIONS_DOCX_EXTRACT_20260702.md#L552-L569).

## R03 — Identifier les actifs ou originaux protégés

**Qualification** — `profil-candidat` · Périmètre `actif-protege`.

Un profil de projet peut déclarer des actifs protégés et leur périmètre. Les sélectionner par identité et preuve, pas par ressemblance de nom.

- **Critère positif** — Le profil identifie les actifs à protéger et les relie aux cibles et contraintes du mandat.
- **Cas négatif ou arrêt** — Un actif protégé n’est pas identifié sans ambiguïté ou est incompatible avec l’opération. Ne pas l’altérer dans ce parcours.
- **Preuve attendue** — Liste de cibles protégées et motif de non-admission.
- **Ce qui n’est pas transféré** — S2 et les originaux Stablecoin restent dans le périmètre WealthTech.

Sources — [H-LOOP-004, L11–11](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md#L11) · [H-LOOP-003, L23–32](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L23-L32).

## R04 — Séparer les preuves des valeurs sensibles

**Qualification** — `commun-candidat` · Périmètre `tous`.

Conserver les références nécessaires, sans reproduire les secrets, identifiants sensibles ou données interdites dans les livrables et journaux.

- **Critère positif** — Une preuve exploitable conserve sa provenance et le résultat du contrôle, sans inclure la valeur sensible.
- **Cas négatif ou arrêt** — Un artefact de qualification contient une valeur sensible. Ne pas le publier tel quel et conserver un constat sans valeur divulguée.
- **Preuve attendue** — Résultat de contrôle expurgé ou référence de preuve contrôlée, sans secret reproduit.
- **Ce qui n’est pas transféré** — Catégories sensibles et mécanisme de contrôle du projet.

Sources — [H-LOOP-004, L12–12](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md#L12) · [H-LOOP-003, L23–32](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L23-L32).

## R05 — Préserver une mémoire persistante lors d’une synchronisation

**Qualification** — `profil-candidat` · Périmètre `synchronisation`.

Dans un profil avec projections ou synchronisations, séparer la référence qui fait autorité, ses répliques et les mises à jour concurrentes.

- **Critère positif** — La révision de lecture et celle de destination sont enregistrées, et un candidat de synchronisation ne remplace pas silencieusement une preuve plus récente.
- **Cas négatif ou arrêt** — Une divergence de version ou un résultat partiel demeure. Conserver les références concurrentes et suspendre l’écrasement.
- **Preuve attendue** — Versions source/destination, référence de conflit ou trace de vérification.
- **Ce qui n’est pas transféré** — Les répertoires et la procédure de synchronisation MCP de juillet ne deviennent pas universels.

Sources — [H-LOOP-004, L13–13](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md#L13) · [H-LOOP-003, L56–69](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L56-L69).

## R06 — Préparer la modification hors production

**Qualification** — `profil-candidat` · Périmètre `changement-sur-existant`.

Préparer le changement dans un périmètre séparé et vérifier l’impact avant de proposer une mise en service.

- **Critère positif** — Le plan distingue environnement de préparation, cible de production, compatibilité et contrôles. Aucun effet de production n’est déduit du plan.
- **Cas négatif ou arrêt** — La cible de préparation ne peut pas être distinguée de la production. Le dossier n’autorise pas la mise en service.
- **Preuve attendue** — Cartographie des environnements, plan de tests et conditions de promotion.
- **Ce qui n’est pas transféré** — La refonte et la préproduction de WealthTech restent spécifiques.

Sources — [H-LOOP-004, L14–14](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md#L14) · [H-LOOP-003, L71–83](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L71-L83) · [H-LOOP-003, L70–83](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L70-L83).

## R07 — Séparer audit et opération métier mutative

**Qualification** — `profil-candidat` · Périmètre `audit-lecture`.

Un mandat d’audit peut exclure explicitement l’écriture ou l’opération métier même lorsque le système propose une capacité correspondante.

- **Critère positif** — Le dossier nomme les observations admissibles et les opérations métier hors périmètre.
- **Cas négatif ou arrêt** — L’étape requiert une transaction ou une autre mutation exclue par le mandat. La consigner comme hors audit.
- **Preuve attendue** — Mandat, liste d’opérations et résultat de l’audit.
- **Ce qui n’est pas transféré** — L’audit Stablecoin 6BI-B et l’interdiction de transaction appartiennent à leur mandat.

Sources — [H-LOOP-004, L15–15](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md#L15) · [H-LOOP-003, L85–98](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L85-L98) · [H-LOOP-003, L84–97](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L84-L97).

## R08 — Vérifier la non-régression de l’existant

**Qualification** — `commun-candidat` · Périmètre `changement-sur-existant`.

Identifier la baseline, les comportements protégés, les contrôles et les preuves requises avant de proposer un changement.

- **Critère positif** — Les comportements à préserver sont reliés à des observations ou tests, avec des résultats à obtenir avant de déclarer la non-régression.
- **Cas négatif ou arrêt** — Aucune baseline pertinente ou un contrôle requis est en échec ou absent. Ne pas conclure que le changement est sans régression.
- **Preuve attendue** — Baseline datée, critères et résultats vérifiables.
- **Ce qui n’est pas transféré** — Les contrôles OPCVM/FundAfrica restent spécifiques.

Sources — [H-LOOP-004, L16–16](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md#L16) · [H-LOOP-003, L194–202](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L194-L202) · [H-LOOP-003, L98–110](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L98-L110).

## R09 — Qualifier une cible de nettoyage et ses dépendances

**Qualification** — `profil-candidat` · Périmètre `nettoyage`.

Le profil décrit les objets candidats, leur état, les dépendances et le traitement de conservation, déplacement ou suppression envisagé.

- **Critère positif** — L’objet et ses consommateurs sont identifiés et le traitement proposé est relié à une analyse. La préparation ne modifie aucun objet.
- **Cas négatif ou arrêt** — Dépendance ou identité non résolue. La cible reste à qualifier plutôt que sélectionnée pour suppression.
- **Preuve attendue** — Inventaire ciblé, matrice ou preuve équivalente, décision par objet.
- **Ce qui n’est pas transféré** — Les seuils et catégories du nettoyage S1/S2 ne sont pas généralisés.

Sources — [H-LOOP-004, L17–17](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md#L17) · [H-LOOP-003, L23–32](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L23-L32) · [H-LOOP-003, L111–123](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L111-L123).

## R10 — Préparer une migration et sa reprise

**Qualification** — `profil-candidat` · Périmètre `migration`.

Identifier les révisions et environnements source/cible, la protection des données, les tests d’arrivée et les conditions de retour ou reprise.

- **Critère positif** — Le dossier rattache sauvegarde, contrôles et procédure de retour ou de reprise à la migration exacte.
- **Cas négatif ou arrêt** — Source ou cible ambiguë, preuve de sauvegarde exigée absente, ou validation requise indisponible. Aucune migration déduite du dossier.
- **Preuve attendue** — Inventaire source/cible, plan et preuves requises.
- **Ce qui n’est pas transféré** — S2 vers S1 et les artefacts précis du mandat de migration WealthTech.

Sources — [H-LOOP-004, L18–18](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md#L18) · [H-LOOP-002, L65–75](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_MASTER_PLAN_20260702.md#L65-L75) · [H-LOOP-003, L124–138](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L124-L138).

## R11 — Conserver une option d’architecture historique sans l’imposer

**Qualification** — `historique-non-prescriptif` · Périmètre `choix-architecture`.

Conserver la provenance de l’orientation historique. Un arbitrage d’architecture cible nécessite ses propres critères et une décision explicite.

- **Critère positif** — La source décrit le choix historique comme tel. Le dossier de conception peut le comparer à d’autres options sans le présenter comme une obligation Loop.
- **Cas négatif ou arrêt** — Une fiche impose ces technologies comme condition d’entrée ou comme choix approuvé à partir de la seule source historique.
- **Preuve attendue** — Référence historique et, le cas échéant, décision d’architecture distincte.
- **Ce qui n’est pas transféré** — Redis/ClickHouse/Docker et Kubernetes futur sont des orientations historiques WealthTech.

Sources — [H-LOOP-004, L19–19](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md#L19) · [H-LOOP-002, L120–125](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_MASTER_PLAN_20260702.md#L120-L125) · [H-LOOP-003, L139–151](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L139-L151).

## R12 — Conserver un exemple d’expression de besoin sans le généraliser

**Qualification** — `historique-non-prescriptif` · Périmètre `besoin-produit`.

Indexer le besoin produit sous sa bonne autorité. Ne pas importer ses fonctionnalités comme exigences de la méthode Loop.

- **Critère positif** — La fiche attribue au bon projet les fonctions demandées et les laisse hors du tronc commun.
- **Cas négatif ou arrêt** — Une fonction du site devient une condition de création de tout projet Loop par simple import historique.
- **Preuve attendue** — Référence de besoin produit, rattachement au projet concerné.
- **Ce qui n’est pas transféré** — SSR/SEO, admin, blog et contact du site ChainSolutions restent des besoins du site.

Sources — [H-LOOP-004, L20–20](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md#L20) · [H-LOOP-003, L152–164](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L152-L164).

## R13 — Rapprocher des inventaires par identité et preuve

**Qualification** — `profil-candidat` · Périmètre `inventaire-multi-sources`.

Identifier l’objet, la portée, la révision et l’autorité de chaque inventaire avant rapprochement. Distinguer présent dans Git, déclaré pour la production et attesté en service.

- **Critère positif** — Un lien dépôt vers cible renvoie à une preuve de jointure. Les états Git et runtime restent distincts même si leurs identifiants concordent.
- **Cas négatif ou arrêt** — Le rapprochement repose uniquement sur un nom de dépôt, de chemin ou de domaine. Laisser le lien candidat ou non vérifié.
- **Preuve attendue** — Index de sources, identifiants et preuve de jointure.
- **Ce qui n’est pas transféré** — Les dépôts, serveurs et domaines réellement associés relèvent du portefeuille WealthTech.

Sources — [H-LOOP-004, L21–21](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md#L21) · [H-LOOP-003, L165–179](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L165-L179).

## R14 — Produire un résultat transmissible

**Qualification** — `commun-candidat` · Périmètre `fin-de-boucle`.

En fin de boucle, conserver l’objectif, les résultats observés, les tests, les écarts, les risques, la preuve et la prochaine action. Indiquer si la phase n’a pas exécuté de tests d’application.

- **Critère positif** — Un autre intervenant retrouve le dernier état, les artefacts vérifiés et les décisions à prendre, sans recalculer le travail.
- **Cas négatif ou arrêt** — Un livrable se dit fini mais ne distingue pas ce qui a été exécuté de ce qui est prévu. Ne pas lui attribuer une clôture probante.
- **Preuve attendue** — Résultat, vérifications, limitations et checkpoint.
- **Ce qui n’est pas transféré** — Markdown et JSON sont des formats du corpus, pas une obligation universelle.

Sources — [H-LOOP-004, L22–22](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md#L22) · [H-LOOP-003, L194–202](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L194-L202).

## R15 — Distinguer provenance historique, autorité et état courant

**Qualification** — `commun-candidat` · Périmètre `tous`.

Porter séparément date/version, nature de la source, périmètre et état d’adoption. Une observation ancienne ne vaut pas constat actuel.

- **Critère positif** — Une citation indique la version et ce qu’elle prouve. Une contradiction ou un manque de couverture demeure visible.
- **Cas négatif ou arrêt** — Un brouillon, une ancienne preuve ou un document homonyme est promu source de vérité actuelle par son intitulé ou sa présence dans Git.
- **Preuve attendue** — Carte de provenance, statuts et écarts.
- **Ce qui n’est pas transféré** — Les autorités précises sont déterminées par le projet et par le moment de l’opération.

Sources — [H-LOOP-004, L23–23](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/MATRICE_TRACABILITE_SOURCES_EXIGENCES_TRACKS_20260702.md#L23) · [H-LOOP-003, L23–32](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_PLAYBOOK_COMPLET_20260702.md#L23-L32) · [LOOP-PR1-SOURCES, L5–16](https://github.com/chainsolutions-wealthtech/Loop/blob/9db9727ddd6c9e6ead7c5dcaa44db8c6afad780e/docs/SOURCE_REGISTER.md#L5-L16).

## W2-G01 — Distinguer constitution, entrée sur existant et reprise

**Qualification** — `commun-candidat` · Périmètre `entree-projet`.

Préserver deux familles et les branches d’entrée pertinentes. Sans dépôt ou historique requis, conserver l’intention initiale et l’identité provisoire sans inventer de SHA ou de checkpoint. Avec un existant, établir la baseline et l’autorité avant tout changement.

- **Critère positif** — Le dossier identifie l’un des cas projet neuf, projet existant ou reprise d’un travail engagé. Dans le neuf, on prépare les emplacements et les sources. Dans l’existant, on retrouve l’autorité et l’inventaire avant d’ajouter un support. En reprise, on réévalue le checkpoint.
- **Cas négatif ou arrêt** — Un agent utilise le cycle d’exécution ou de prise de tâche avant de qualifier l’intention et le type d’arrivée. Ou il fabrique un checkpoint pour un projet neuf. Le dossier ne passe pas le contrôle.
- **Preuve attendue** — Fiche d’entrée, source du mandat, registre de sources, décision de mode et point d’arrêt.
- **Ce qui n’est pas transféré** — Ni nom de fichier imposé, ni granularité de workflow ou architecture cible adoptée.

Sources — [LOOP-README-WF00, L7–14](https://github.com/chainsolutions-wealthtech/Loop/blob/c523c64f5c42dbd2115b5575772c1d5e1f9992df/README.md#L7-L14) · [LOOP-WF00-CANDIDAT, L7–24](https://github.com/chainsolutions-wealthtech/Loop/blob/c523c64f5c42dbd2115b5575772c1d5e1f9992df/docs/WORKFLOW_WF00.md#L7-L24) · [LOOP-WF00-CANDIDAT, L36–44](https://github.com/chainsolutions-wealthtech/Loop/blob/c523c64f5c42dbd2115b5575772c1d5e1f9992df/docs/WORKFLOW_WF00.md#L36-L44) · [H-LOOP-002, L60–75](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_MASTER_PLAN_20260702.md#L60-L75).

## W2-G02 — Séparer préparation, conception, planification et exécution

**Qualification** — `commun-candidat` · Périmètre `conception-avant-code`.

Faire passer les exigences qualifiées et les questions ouvertes au cadrage et à la conception. Ne pas déduire une autorité d’exécution d’un inventaire fini ou de l’acceptation d’un besoin.

- **Critère positif** — L’intention et les exigences ont une source et un périmètre. Les choix d’architecture sont traçables. Le plan explicite dépendances, validation et conditions de passage à l’exécution.
- **Cas négatif ou arrêt** — Le dossier propose directement une tâche de code, un moteur, une Action ou un déploiement en tirant la permission de W1, WF-00 ou W2. Le passage reste non admissible.
- **Preuve attendue** — Exigences et sources, questions, décisions de conception distinctes et plan vérifiable.
- **Ce qui n’est pas transféré** — Ni nom de fichier imposé, ni granularité de workflow ou architecture cible adoptée.

Sources — [LOOP-README-WF00, L7–14](https://github.com/chainsolutions-wealthtech/Loop/blob/c523c64f5c42dbd2115b5575772c1d5e1f9992df/README.md#L7-L14) · [LOOP-WF00-CANDIDAT, L7–24](https://github.com/chainsolutions-wealthtech/Loop/blob/c523c64f5c42dbd2115b5575772c1d5e1f9992df/docs/WORKFLOW_WF00.md#L7-L24) · [LOOP-WF00-CANDIDAT, L36–44](https://github.com/chainsolutions-wealthtech/Loop/blob/c523c64f5c42dbd2115b5575772c1d5e1f9992df/docs/WORKFLOW_WF00.md#L36-L44) · [H-LOOP-002, L60–75](https://github.com/Patricked-code/MCP/blob/e8cfaf7246abb20151a8b439913d97ecf87a4979/memory/LOOP_ENGINEERING_WEALTHTECH_MASTER_PLAN_20260702.md#L60-L75).

## Cas d’acceptation transversaux

Il s’agit de scénarios de contrôle proposés, non de tests de runtime exécutés.

| Cas | Mise en situation | Résultat attendu | Exigences |
| --- | --- | --- | --- |
| `W2-C01` · Projet neuf sans dépôt | Intention et sources initiales, aucun dépôt ou checkpoint prouvé. | Squelette et emplacements proposés. Aucun SHA inventé ni travail de code engagé. | R01, R15, W2-G01, W2-G02 |
| `W2-C02` · Projet existant avec deux checkpoints incompatibles | Deux références documentaires prétendent faire autorité pour le même périmètre. | Contradiction tracée. Reprise opérationnelle non déduite avant résolution. | R01, R05, R15, W2-G01 |
| `W2-C03` · Plesk ou nettoyage avec cible ambiguë | Connexion disponible, cible et dépendances non résolues ou autorité absente. | Préparation ou diagnostic uniquement. Aucune écriture ni suppression. | R02, R03, R09, R13 |
| `W2-C04` · Migration sans preuve de sauvegarde requise | Une cible est proposée, mais le prérequis de protection des données n’est pas établi. | Candidat non admissible à l’exécution. Précondition manquante explicite. | R06, R08, R10, W2-G02 |
| `W2-C05` · Observation, secret et trace de clôture | Audit réalisé sans droit d’écriture ni preuve d’un contrôle attendu. | Restitution sans donnée sensible, résultat qualifié, opérations non effectuées et reprise explicite. | R04, R07, R14, R15 |
| `W2-C06` · Import d’une orientation historique ou d’un kit non qualifié | Une technologie, un besoin produit ou une règle de kit est proposée comme règle universelle sans adoption. | Conserver la proposition et sa provenance, ne pas l’activer ni la promouvoir. | R11, R12, R15, W2-G02 |

[Point de reprise W2](POINT-DE-REPRISE.md)
