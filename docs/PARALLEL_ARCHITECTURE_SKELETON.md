# Squelette de référence — Dossier de conception Loop

**Version 0.1 — Modèle réutilisable à renseigner.** Pour un logiciel, une application web, une API ou un serveur MCP. Ce document est une proposition de conception, sans décision de stack ni modification GitHub.

## Niveau 0 — Projet

| Champ de cadrage | À renseigner |
|---|---|
| Identité | Nom, identifiant du projet, dépôt ou espace de travail |
| Type et situation | Web, MCP, API ou autre. Projet neuf ou reprise d'un existant |
| Mission et périmètre | Résultat recherché, utilisateurs principaux, hors périmètre |
| Références | Sources initiales, état Git ou technique observé s'il existe, décisions à préserver |
| Version et reprise | Version du dossier, dernier état confirmé, prochaine branche à renseigner |

Le dossier contient **deux cartes au même niveau**. L'architecture fonctionnelle ne se range pas dans le Back. L'architecture technique ne se réduit pas à l'hébergement. Les deux cartes sont des vues du même projet, reliées par une matrice. La planification et les tickets Jira sont des travaux dérivés, pas une troisième architecture.

## Niveau 1 — Architecture fonctionnelle

| Repère | Grande branche | Ce qu'on vient renseigner | État initial |
|---|---|---|---|
| F1 | Acteurs et rôles | Personnes, agents et systèmes qui utilisent le logiciel. Responsabilités et droits métier | À renseigner |
| F2 | Domaines et capacités | Grandes responsabilités du produit, sous-domaines si utiles et ce que le produit doit savoir faire | À renseigner |
| F3 | Fonctionnalités, cas d'utilisation et parcours | Ce qu'un acteur veut accomplir, déclencheur, déroulement, étapes et résultat. Un parcours peut traverser plusieurs domaines | À renseigner |
| F4 | Règles, états et exceptions | Conditions d'acceptation et de refus, transitions, exceptions, reprises et limites d'action | À renseigner |
| F5 | Informations et résultats métier | Objets métier, signification, relations, entrées, sorties et changements attendus. Aucun choix de base de données à ce niveau | À renseigner |
| F6 | Exigences et critères d'acceptation | Comportements attendus, qualités mesurables, contraintes et conditions qui permettent de dire qu'une demande est satisfaite | À renseigner |

**Exemple de descente sur le métier.** Domaine → capacité → fonctionnalité → cas d'utilisation, si ces niveaux apportent une distinction utile. Les acteurs, parcours transversaux, règles et informations sont des objets liés, pas des parents obligatoires dans une arborescence.

## Niveau 1 — Architecture technique

| Repère | Grande branche | Ce qu'on vient renseigner | État initial |
|---|---|---|---|
| T1 | Interfaces et Front | Interfaces réellement utilisées, clients web ou autres, administration éventuelle, points d'entrée machine comme l'interface MCP | À renseigner |
| T2 | Back et modules applicatifs | Composants qui coordonnent les opérations, appliquent les règles et rendent les fonctionnalités. Le serveur MCP au sens logiciel peut être situé ici, avec une interface décrite en T1 | À renseigner |
| T3 | Données, état et persistance | Modèles techniques, sources de vérité, stockage éventuel, accès, migrations, conservation et état de session ou de chantier si pertinent | À renseigner |
| T4 | Contrats, échanges et intégrations | Contrats internes et externes, adaptateurs, erreurs, échanges synchrones et événements si nécessaires. La définition d'un contrat peut être reliée à son point d'entrée en T1 | À renseigner |
| T5 | Serveur, infrastructure et exploitation | Environnement d'exécution local ou distant, configuration, déploiement, supervision, sauvegarde et restauration selon le périmètre | À renseigner |
| T6 | Sécurité et contrôles | Identité technique, autorisations, protection des données et secrets, traçabilité et contrôles aux frontières du système | À renseigner |
| T7 | Tests et qualité | Tests unitaires, d'intégration, de contrat ou de parcours, non-régression et preuves attendues selon le besoin | À renseigner |
| T8 | Outils de construction et de maintenance | Scripts, outils de développement et de diagnostic, CI/CD, génération et validations automatisées | À renseigner |

**Exemple de descente sur le technique.** Back → module → composant ou service interne → contrat ou interface. Dans l'infrastructure, on descend plutôt d'un environnement vers ses unités déployables et leurs mécanismes d'exploitation. Il n'est pas nécessaire de forcer les branches à employer les mêmes niveaux.

**Front, Back et Serveur d'hébergement** sont trois repères familiers, pas l'intégralité de la carte. Pour un serveur MCP, une application IA existante peut suffire comme interface d'utilisation. Un Front web propriétaire peut être non applicable. Le Back qui répond au protocole et l'environnement où il tourne restent distincts. Un contrat peut exister sans API séparée, et une information métier sans base de données propre.

## Fiche à remplir quand on ouvre une branche

| Champ | Valeur |
|---|---|
| ID stable et branche parente | [ex. F2-C01 ou T2-M01] |
| Objet et responsabilité | [ce que cet élément fait, ce qu'il ne fait pas] |
| Source et version | [instruction, décision ou observation qui le justifie] |
| Sous-parties proposées | [niveau suivant seulement, si l'information le permet] |
| Entrées et sorties | [ce que l'élément reçoit, produit ou transmet] |
| Règles, dépendances et exceptions | [conditions, prérequis, refus et reprise selon le cas] |
| Liens vers l'autre carte | [identifiants, type de lien, raison] |
| Critères et preuve attendue | [ce qui sera vérifié, comment et dans quel périmètre] |
| Statut et prochaine action | [à renseigner, proposé, retenu, à réconcilier ou non applicable avec motif] |

Sur un projet existant, séparer **l'état observé** de **la cible proposée**. Une inconnue reste à renseigner. Le statut « non applicable » doit être motivé. Le statut « retenu » ne constitue pas une preuve d'implémentation ni une autorisation d'intervenir.

## Matrice de raccordement

| Référence fonctionnelle | Relation | Référence technique | Critère ou preuve | Source / statut |
|---|---|---|---|---|
| [F…@version] | [est exposé par / est réalisé par / dépend de / est vérifié par] | [T…@version] | [critère, test ou preuve] | [instruction, décision, observation / état] |

Une fonctionnalité peut mobiliser plusieurs composants et un composant peut servir plusieurs fonctionnalités. On crée plusieurs liens vers le même objet au lieu de le recopier. Les décisions justifient les liens retenus. Une modification permet de retrouver les éléments dépendants, sans reconstituer toute la carte.

## Exemple — Serveur MCP pour reprendre un chantier

Ce scénario est fictif. Les repères illustrent la méthode, sans décrire une architecture décidée pour un dépôt existant.

| Carte | Descente illustrée | Contenu initial |
|---|---|---|
| Fonctionnelle | F2 → Continuité des projets → Reprise → Retrouver un point de reprise | L'utilisateur veut obtenir l'état du chantier, la prochaine action et les écarts éventuels. Si plusieurs chantiers conviennent, signaler l'ambiguïté. Si le dépôt diverge du checkpoint, ne pas présenter la reprise comme vérifiée. |
| Technique | T1 → Interface MCP | Point d'entrée candidat pour recevoir les références du projet et du chantier. Interface web propre non décidée. |
| Technique | T2 → Module de continuité | Compare le point de reprise à l'état observé et construit le résultat. |
| Technique | T3 → Source de continuité | Lit le registre désigné par le projet, sans imposer une nouvelle base. |
| Technique | T4 → Raccordement GitHub | Observe les références Git nécessaires dans le périmètre prévu. Ce composant peut aussi servir d'autres fonctionnalités. |
| Technique | T5 → Exécution | Local ou distant à décider. Le cas d'utilisation ne suffit pas pour choisir un mode d'hébergement. |
| Technique | T7 → Vérification de la reprise | Vérifie un état concordant, un point absent, un chantier ambigu et un écart de référence. |

La lecture et la restitution de la prochaine action ne valent pas exécution de cette action.

## Comment Loop utilise le squelette

1. **Ouvrir la carte de niveau 1** dès que le type de projet est reconnu. Prévoir toutes les branches, sans en déduire des dossiers, services ou technologies obligatoires.
2. **Inventorier et conserver** les autorités, modèles et comportements existants pour un projet déjà lancé. Pour un projet neuf, laisser visibles les branches non renseignées.
3. **Capturer l'instruction une fois**, puis la rattacher aux branches concernées sur une ou deux cartes. Distinguer le contenu fourni des propositions et des questions ouvertes.
4. **Descendre d'un niveau à la fois**, sur la branche concernée. Mobiliser DDD pour éclairer les frontières métier, Atomic Design pour une interface visuelle à composer, ou l'architecture hexagonale pour maîtriser les dépendances. Microservices, EDA, CQRS, Docker et Kubernetes restent des choix à justifier, pas des cases à implémenter par défaut.
5. **Relier, vérifier et préparer la suite**. Rattacher les critères aux exigences et les travaux aux versions des objets concernés. La planification peut produire des tickets de clarification, de conception, de réalisation ou de vérification. Jira suit ces travaux sans remplacer les cartes.
6. **Enregistrer le point de reprise** avec la branche à rouvrir, l'objet et sa version, les décisions ou questions ouvertes, les preuves et la prochaine action.

**Raccord au contrat déjà rédigé.** WF-00 prépare les emplacements logiques, les sources et les autorités. Software Design renseigne les deux cartes et leurs liens. La planification consomme les éléments suffisamment définis pour en faire des travaux. Ce modèle complète le [contrat de passage v0.1](WF00_DESIGN_PLANNING_CONTRACT.md) sans modifier le kit ni le dépôt GitHub.
