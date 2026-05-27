---
name: sdd-uc-system-design
description: >
  Produit les documents de conception technique SDD (ARCHITECTURE.md,
  DEPLOYMENT.md, SECURITY.md, COMPLIANCE_MATRIX.md) à partir d'un
  SPEC-racine-*.md (+ extensions). En CLI écrit dans docs/, sur claude.ai
  livre des artefacts Markdown. S'active pour concevoir l'architecture
  technique d'un projet SDD.
metadata:
  version: "3.3.0"
  author: "Franz TRIERWEILER"
license: "MIT"
---

# SDD UC System Design — Conception technique

Version : 3.3.0
Date : 2026-04-21

## Barre de progression — OBLIGATION STRICTE

**Chaque réponse produite sous ce skill DOIT commencer par la barre de
progression ci-dessous. AUCUNE EXCEPTION. Cela inclut le message d'accueil.**

```
📐 skill:sdd-uc-system-design v3.3.0 · [Phase] [barre] étape N/T — [Nom]
```

Caractère plein : `█` — Caractère vide : `░`. Voir la section
« Identification du skill dans les réponses » plus bas pour le détail
des sous-étapes et les exemples complets.

## Prérequis — vérification au démarrage

Avant toute autre action, vérifie que les fichiers suivants existent dans le
répertoire `references/` du skill :

| Fichier | Rôle |
|---|---|
| `references/TEMPLATE-ARCHITECTURE.md` | Template de référence pour ARCHITECTURE.md |
| `references/TEMPLATE-DEPLOYMENT.md` | Template tronc commun pour DEPLOYMENT.md |
| `references/TEMPLATE-DEPLOYMENT-SAAS.md` | Sections spécifiques SaaS (sous-template) |
| `references/TEMPLATE-DEPLOYMENT-DESKTOP.md` | Sections spécifiques client lourd (sous-template) |
| `references/TEMPLATE-DEPLOYMENT-DRIVER.md` | Sections spécifiques driver (sous-template) |
| `references/TEMPLATE-DEPLOYMENT-EMBEDDED.md` | Sections spécifiques logiciel embarqué : mobile, TPE, terminal pro, système embarqué, dev board (sous-template) |
| `references/TEMPLATE-SECURITY.md` | Template de référence pour SECURITY.md |
| `references/TEMPLATE-COMPLIANCE-MATRIX.md` | Template de référence pour COMPLIANCE_MATRIX.md |

Si un ou plusieurs fichiers sont absents, **arrête immédiatement** et affiche :

```
⚠️ Fichier(s) manquant(s) dans references/ : [liste].
Le skill ne peut pas fonctionner sans ces fichiers. Vérifie que le skill
a été installé avec son répertoire references/ complet.
```

Ne tente pas de générer les documents de conception de mémoire si un fichier
de référence manque.

## Déclenchement

### Déclenchement primaire (active le skill directement)

- L'utilisateur demande de produire l'architecture, le déploiement, la sécurité
  ou la conformité d'un projet à partir d'une spec.
- L'utilisateur mentionne la « phase de conception » ou « phase 1 » du flux
  SDD et fournit (ou référence) une spec.
- L'utilisateur demande explicitement un ARCHITECTURE.md, DEPLOYMENT.md,
  SECURITY.md ou COMPLIANCE_MATRIX.md.
- L'utilisateur demande de produire « les documents de conception » ou
  « les livrables de conception technique ».

### Déclenchement secondaire (demande confirmation avant d'activer)

- L'utilisateur mentionne « concevoir le système » sans référence SDD →
  Demande : « Tu veux des documents de conception SDD à partir d'une spec,
  ou une conception libre ? »
- L'utilisateur fournit une spec sans préciser ce qu'il veut → Demande :
  « Tu veux lancer la phase de conception (architecture, déploiement, sécurité,
  conformité) ? »

### Ne pas déclencher (anti-triggers)

- L'utilisateur veut rédiger ou modifier une spec → Utiliser sdd-uc-spec-write.
- L'utilisateur demande de planifier des lots ou des User Stories → Phase 2.
- L'utilisateur demande d'implémenter du code → Phase 3.
- L'utilisateur demande une revue de code → Phase 4.
- L'utilisateur pose une question technique ponctuelle sans contexte de projet.

### Validation du format d'entrée

Ce skill attend une spec structurée par **cas d'utilisation (UC)**, produite
par le skill sdd-uc-spec-write. Les marqueurs d'une spec compatible sont :

- Présence d'identifiants `UC-xxx` (cas d'utilisation numérotés)
- Structure par packages (niveau 2 / niveau 1)
- Étapes au format Na/Nb (acteur/système)
- Critères d'acceptation au format `CA-UC-xxx-yy`
- Règles de gestion `RG-xxxx`

Si la spec fournie utilise un autre format (exigences plates EXG-xxx,
user stories, cahier des charges classique), Claude informe l'utilisateur :

> Ce skill attend une spec structurée par cas d'utilisation (format
> sdd-uc-spec-write). Le document fourni semble utiliser un autre format.
> Veux-tu convertir la spec en format UC d'abord (via sdd-uc-spec-write),
> ou continuer avec le format actuel en mode dégradé ?

## Message d'accueil

Quand le skill est activé et que la spec est validée, Claude affiche :

```
📐 skill:sdd-uc-system-design v3.3.0 · Architecture [░░░░░░░] 0/7 — Démarrage

Ce skill produit les documents de conception technique à partir de ta
spec, selon la méthodologie SDD. Je vais produire jusqu'à 4 documents :

1. ARCHITECTURE.md — Comment le système est construit (composants, stack,
   flux, données, décisions).
2. DEPLOYMENT.md — Comment le système est déployé et opéré (prérequis,
   procédures, CI/CD, monitoring, disaster recovery).
3. SECURITY.md — Comment le système est sécurisé (menaces, exigences,
   code sécurisé, réponse à incident).
4. COMPLIANCE_MATRIX.md — Comment le système est conforme à son cadre
   réglementaire (seulement si applicable).

On commence par l'architecture, qui conditionne tous les autres documents.
La réflexion se fait en 7 étapes avant toute rédaction. Je te poserai des
questions par petits groupes (3-5 max) à chaque étape.

On y va ?
```

## Philosophie

Les documents de conception sont le pont entre la spécification (ce que le
système doit faire) et l'implémentation (comment il le fait). Ils constituent
le cadre de référence pour tout agent IA ou ingénieur qui implémentera le
projet.

Chaque document répond à une question précise :

| Document | Question |
|---|---|
| ARCHITECTURE.md | **Comment** le système est-il construit ? |
| DEPLOYMENT.md | **Comment** le système est-il déployé et opéré ? |
| SECURITY.md | **Comment** le système est-il sécurisé ? |
| COMPLIANCE_MATRIX.md | **Comment** le système est-il conforme à son cadre réglementaire ? |

Ces documents sont produits itérativement par un dialogue entre Claude et
l'ingénieur/PO. Claude pose des questions, propose des choix, et rédige
progressivement. L'ingénieur valide, corrige, complète.

### Principes directeurs

1. **Traçabilité** : chaque décision d'architecture doit être rattachable à
   un cas d'utilisation (UC-xxx), une règle de gestion (RG-xxxx), une
   exigence non fonctionnelle (ENF-xxx), ou un critère d'acceptation
   (CA-UC-xxx-yy) de la spec.
2. **Détail sans redondance** : être exhaustif mais ne jamais répéter la même
   information dans deux documents. Utiliser des renvois croisés.
3. **Spécificité** : pas de généralités vagues. Si on choisit PostgreSQL,
   expliquer pourquoi et dans quelle version.
4. **Autonomie du lecteur** : un agent IA lisant ces documents avec la spec
   doit pouvoir implémenter sans poser de questions d'architecture.

## Entrées requises

- **`SPEC-racine-*.md` (+ extensions éventuelles)** (obligatoire) : les
  fichiers de spécification SDD structurés par cas d'utilisation, produits
  par sdd-uc-spec-write.
- **Fichiers référencés par la spec** (si présents) : DATA-MODEL.md,
  ou tout document listé dans la section « Documents de référence » de la spec.
- **Contexte organisationnel** (collecté par Q&A) : contraintes d'infrastructure,
  politiques de sécurité internes, cadre réglementaire applicable.

### Exploitation de la structure UC

Le format UC offre une richesse d'information architecturale que Claude
exploite systématiquement :

| Élément de la spec | Exploitation architecturale |
|---|---|
| **Diagramme de contexte** | Vue d'ensemble du périmètre, acteurs, systèmes adjacents — base pour la vue d'ensemble (§ 1) |
| **Section Architecture** | Contraintes techniques imposées — entrée directe pour le cadrage macro (A.1) |
| **Packages niveau 2** | Pistes pour le découpage en composants ou modules |
| **Packages niveau 1** | Pistes pour le découpage en sous-modules ou services |
| **Étapes Na/Nb** | Source directe pour les flux métier (flowcharts) |
| **État initial / État final** | Source pour les diagrammes de transition d'état (state diagrams) |
| **Exceptions** | Source directe pour les flux d'erreur et de rattrapage |
| **Relations include** | Dépendances obligatoires entre composants |
| **Relations extend** | Points d'extension optionnels de l'architecture |
| **Objets participants** | Base du modèle de données |
| **Règles de gestion (RG)** | Contraintes métier à implémenter dans le bon composant |
| **Acteurs** | Points d'entrée du système (interfaces utilisateur, APIs) |
| **Fréquence d'utilisation** | Données de dimensionnement (performance, scalabilité, coûts) |
| **Priorité** (Critique/Important/Souhaité) | Priorisation des arbitrages architecturaux |
| **IHM-xxx** | Contraintes d'interface et de couche présentation |
| **ENF-xxx** | Propriétés non-fonctionnelles transverses |
| **CA-UC-xxx-yy** | Critères de validation de l'architecture |
| **Niveaux de support** | Frontières du système (ce qui est émulé, ignoré, rejeté) |
| **Hors périmètre** | Délimitation de ce que l'architecture ne doit PAS couvrir |
| **Glossaire projet** | Source pour le glossaire technique de l'ARCHITECTURE.md (§ 6) |

## Sorties produites

| Fichier | Quand le produire |
|---|---|
| `docs/ARCHITECTURE.md` | Toujours |
| `docs/DEPLOYMENT.md` | Toujours |
| `docs/SECURITY.md` | Toujours |
| `docs/COMPLIANCE_MATRIX.md` | Seulement si un cadre réglementaire est identifié |

## Identification du skill dans les réponses

Chaque réponse produite sous ce skill commence par une barre de progression
indiquant le skill actif, la phase en cours et l'avancement. Cette ligne est
obligatoire, sans exception.

**Format :**

```
📐 skill:sdd-uc-system-design v3.3.0 · [Phase] [barre] étape N/T — [Nom de l'étape]
```

La version affichée est celle indiquée dans l'en-tête du skill (actuellement v3.3.0).

**Règles de la barre de progression :**

- Caractère plein : `█` — Caractère vide : `░`
- Largeur fixe : 7 caractères pour les phases A (7 étapes + rédaction),
  5 caractères pour les phases B/D, 3 caractères pour la phase C.
- La barre reflète l'étape en cours (incluse).

**Exemples par phase :**

```
📐 skill:sdd-uc-system-design v3.3.0 · Architecture [█░░░░░░] étape 1/7 — Cadrage macro
📐 skill:sdd-uc-system-design v3.3.0 · Architecture [███░░░░] étape 3/7 — Modèle de données
📐 skill:sdd-uc-system-design v3.3.0 · Architecture [███████] étape 7/7 — Synthèse et arbitrages
📐 skill:sdd-uc-system-design v3.3.0 · Architecture [████████] rédaction
📐 skill:sdd-uc-system-design v3.3.0 · Déploiement [██░░░] étape 2/5 — Questions
📐 skill:sdd-uc-system-design v3.3.0 · Sécurité [█░░] étape 1/3 — Modèle de menaces
📐 skill:sdd-uc-system-design v3.3.0 · Sécurité [██░] étape 2/3 — Questions de cadrage
📐 skill:sdd-uc-system-design v3.3.0 · Sécurité [███] étape 3/3 — Rédaction
📐 skill:sdd-uc-system-design v3.3.0 · Conformité [█████] étape 5/5 — Rédaction
```

Si plusieurs messages se succèdent au sein de la même étape (ex : questions
de clarification, réponses intermédiaires), la barre reste identique. Elle
avance uniquement au passage à l'étape suivante.

## Processus de conception

La conception suit un processus en 4 phases séquentielles. Chaque phase
produit un document. Claude guide l'utilisateur par des questions ciblées
(3 à 5 maximum à la fois) avant de rédiger chaque section.

### Phase A — Architecture (ARCHITECTURE.md)

La conception de l'architecture est la phase la plus critique. Elle conditionne
tous les documents suivants. La réflexion doit être **exhaustive et profonde**
avant toute rédaction. Claude ne rédige RIEN tant que la réflexion n'est pas
terminée et validée.

#### A.0 — Activation du mode plan

Dès l'entrée en Phase A, Claude active le **mode plan** : il présente à
l'utilisateur la feuille de route complète de la réflexion architecturale
avant de poser la moindre question. L'objectif est que l'utilisateur sache
exactement où il va et combien d'étapes l'attendent.

**Annonce obligatoire (à adapter au contexte) :**

> La conception de l'architecture va se dérouler en 7 étapes de réflexion
> avant que je ne rédige quoi que ce soit. Chaque étape approfondit un axe
> différent. Je te poserai des questions par petits groupes (3-5 max) et je
> synthétiserai ma compréhension entre chaque étape pour que tu puisses
> corriger le tir.
>
> **Étapes de réflexion :**
>
> 1. **Cadrage macro** — Type de solution, contraintes imposées, écosystème
> 2. **Analyse de la spec** — Exploitation des UC, packages, flux et objets
> 3. **Modèle de données** — Entités (objets participants), relations, volumes
> 4. **Flux et interactions** — Flux métier (étapes UC), intégrations, événements
> 5. **Choix technologiques** — Stack, justifications, alternatives écartées
> 6. **Propriétés non-fonctionnelles** — Performance, résilience, observabilité
> 7. **Synthèse et arbitrages** — Consolidation, trade-offs, décisions ouvertes
>
> Après l'étape 7, je te présenterai une **synthèse architecturale complète**
> pour validation avant de rédiger le document.
>
> On commence ?

Si l'utilisateur souhaite sauter ou fusionner des étapes, Claude s'adapte
mais l'informe des risques (ex : « Si on ne creuse pas le modèle de données
maintenant, l'inventaire des données dans l'ARCHITECTURE.md sera incomplet
et devra être repris plus tard. »).

#### A.1 — Cadrage macro

**Objectif :** Comprendre la nature du système et ses contraintes structurantes
avant toute réflexion technique.

**Exploitation préalable de la spec :**

Avant de poser les questions, Claude exploite les sections de la spec qui
fournissent déjà du contexte architectural :

- **Diagramme de contexte** (si présent) — Identifier les acteurs, systèmes
  adjacents, éléments géographiques et organisationnels. Ce schéma donne une
  vue d'ensemble du périmètre qui alimente directement la § 1 (Vue d'ensemble)
  de l'ARCHITECTURE.md.
- **Section Architecture** (si présente) — Contraintes techniques imposées
  (langage, plateforme, composants). Ces contraintes sont non négociables et
  réduisent l'espace des questions à poser.
- **Section Hors périmètre** — Délimite ce que l'architecture ne doit PAS
  couvrir. Évite de concevoir des composants pour des fonctionnalités exclues.

Claude synthétise ce qu'il a trouvé dans la spec et adapte ses questions
en conséquence (ne pas redemander ce qui est déjà documenté).

**Questions obligatoires :**

1. Quel type de solution développez-vous ? (SaaS, client lourd, driver,
   logiciel embarqué — mobile, TPE, terminal professionnel, système
   embarqué, dev board —, bibliothèque, CLI, API, microservices,
   monolithe, autre)
2. Le système est-il autonome ou s'insère-t-il dans un écosystème existant ?
   Si oui, lequel ? (décrire les systèmes adjacents)
3. Quelles sont les contraintes **imposées** et non négociables ? (langage,
   plateforme, fournisseur cloud, protocoles, normes)
4. Qui sont les parties prenantes techniques ? (équipe de dev, ops, intégrateurs,
   utilisateurs finaux techniques)
5. Y a-t-il un existant technique à prendre en compte ? (code legacy, base de
   données existante, infrastructure en place)

**Questions conditionnelles :**

- Si SaaS ou microservices → Quel fournisseur cloud ? Multi-cloud ?
  Quelles régions ? Budget infrastructure mensuel ?
- Si driver ou client lourd → Quels OS cibles ? Quelles versions ?
  Architecture processeur ? Privilèges requis (kernel, admin) ?
- Si logiciel embarqué → Quelle catégorie de cible (téléphone mobile,
  TPE, terminal professionnel, système embarqué, dev board) ? Quels
  modèles / plateformes ? Quel OS / runtime (Android, iOS, FreeRTOS,
  bare metal) ? Connectivité (Wi-Fi, 4G, intermittente, filaire) ?
  Mode hors-ligne requis ? Y a-t-il une HAL pour abstraire le matériel ?
  Gestionnaire de terminaux / MDM (TOMS, SOTI, autre) ?
- Si intégration hardware → Quels protocoles matériels ? Quels équipements ?
  Firmwares à supporter ?
- Si système distribué → Combien de nœuds ? Réseau fiable ou intermittent ?
  Tolérance à la partition ?

**Livrable intermédiaire :** Claude synthétise le cadrage en 5-10 lignes et
le présente pour validation : « Voici ce que je comprends du contexte. Tu
confirmes / tu corriges ? »

#### A.2 — Analyse de la spec

**Objectif :** Exploiter la structure UC de la spec pour extraire toutes les
implications architecturales. Le format UC fournit une matière beaucoup plus
riche qu'une liste d'exigences plates : les flux sont déjà documentés dans
les étapes, les dépendances dans les relations, les données dans les objets
participants.

**Travail d'analyse (Claude, en autonomie) :**

Claude lit la spec complète et les documents référencés, puis produit :

1. **Cartographie des flux à partir des UC** — Pour chaque UC, les étapes
   Na/Nb fournissent directement le flux nominal. Claude les regroupe par
   package de niveau 2 pour identifier les grands blocs fonctionnels du
   système. Les relations include révèlent les dépendances obligatoires
   entre blocs, les relations extend révèlent les points d'extension.

2. **Inventaire des implications architecturales par UC** — Pour chaque
   UC-xxx, Claude évalue si le cas d'utilisation contraint l'architecture
   (choix de composant, pattern, protocole, stockage). Attention
   particulière aux :
   - **Exceptions** : chaque exception peut impliquer un mécanisme
     architectural (retry, fallback, circuit breaker, queue de rattrapage).
   - **Règles de gestion (RG-xxxx)** : certaines RG imposent des
     contraintes transactionnelles, de validation, ou de calcul qui
     impactent le placement des composants.
   - **IHM-xxx** : les contraintes d'interface peuvent imposer des
     choix de couche présentation (SSR, SPA, WebSocket).

3. **Analyse des objets participants** — La liste des objets participants
   et les éventuels diagrammes d'objets/interactions de la spec fournissent
   le brouillon du modèle de données. Claude les exploite comme point de
   départ pour l'étape A.3.

4. **Détection des besoins implicites** — Claude identifie les besoins
   architecturaux qui ne sont pas explicitement formulés dans les UC mais
   qui en découlent logiquement (ex : un UC avec une étape « Le système
   envoie une notification » implique un mécanisme de notification ; un UC
   avec une relation include vers un UC d'authentification implique une
   couche de sécurité).

5. **Identification des tensions** — Claude repère les UC ou ENF dont les
   contraintes pourraient être en tension (ex : un UC exigeant un temps de
   réponse < 200ms + une RG imposant un calcul complexe → besoin de cache
   ou de pré-calcul).

**Présentation à l'utilisateur :**

Claude présente cette analyse sous forme structurée :

> **Analyse de la spec — Implications architecturales**
>
> J'ai identifié **N cas d'utilisation à impact architectural**, **M besoins
> implicites** non formulés dans la spec, et **P tensions** à arbitrer.
>
> [Tableau structuré par package de niveau 2]
>
> Questions de clarification :

**Questions de clarification (3-5 max) :**

Les questions portent sur les zones d'ombre révélées par l'analyse. Elles ne
sont pas pré-définies — elles émergent de la lecture de la spec. Exemples
typiques :

- « UC-012 décrit une étape 3b (notification) mais ne précise pas le canal
  (email, SMS, push). Quel est le mécanisme attendu ? »
- « La relation include entre UC-005 et UC-003 implique que [composant X]
  dépend de [composant Y]. Tu confirmes ce couplage ? »
- « RG-0015 impose [contrainte] mais ENF-002 demande [performance]. Ces deux
  exigences sont en tension. Quel compromis privilégier ? »
- « Les exceptions de UC-020 (étapes 2b, 4b) impliquent un mécanisme de
  retry. Est-ce un besoin réel ou le système doit-il simplement échouer ? »

#### A.3 — Modèle de données

**Objectif :** Cartographier exhaustivement les données du système avant de
choisir comment les stocker et les transporter.

**Travail d'analyse (Claude, en autonomie) :**

Claude part des **objets participants** de la spec comme base. Cette section
de la spec liste les entités métier identifiées à travers les cas
d'utilisation. Claude enrichit cette liste avec :

- Les attributs principaux déduits des étapes et règles de gestion des UC
- Les relations entre entités déduites des relations entre UC (include,
  extend) et des diagrammes d'objets/interactions (si présents dans la
  spec)
- La classification de sensibilité par entité (public, interne,
  confidentiel, secret)
- L'estimation des volumes (nombre d'enregistrements, taille, croissance)
- Le cycle de vie des données (création, modification, archivage,
  suppression)

Si la spec contient un DATA-MODEL.md référencé, Claude l'utilise
directement comme point de départ au lieu des objets participants.

**Questions obligatoires :**

1. Le brouillon d'inventaire basé sur les objets participants est-il
   complet ? Manque-t-il des entités ?
2. Quelles sont les données les plus sensibles ? Y a-t-il des données
   soumises à des réglementations spécifiques ?
3. Quels sont les volumes réalistes ? (nombre d'utilisateurs, de transactions
   par jour/mois, de fichiers, taille des fichiers)
4. Y a-t-il des données qui doivent être purgées ou archivées après un délai ?

**Questions conditionnelles :**

- Si données de santé → Classification spécifique ? Pseudonymisation ?
  Séparation des données directement identifiantes ?
- Si données en temps réel → Fréquence d'arrivée ? Taille des événements ?
  Fenêtre de rétention en mémoire ?
- Si multi-tenant → Isolation des données par tenant ? Données partagées
  entre tenants ?
- Si système distribué → Données répliquées ? Stratégie de cohérence ?
  (CAP theorem)

**Livrable intermédiaire :** Inventaire des données validé par l'utilisateur.

#### A.4 — Flux et interactions

**Objectif :** Identifier tous les flux de données et d'interactions entre
composants, systèmes externes, et utilisateurs. Le format UC fournit une
matière directement exploitable : les étapes Na/Nb sont les flux nominaux,
les exceptions sont les flux d'erreur.

**Travail d'analyse (Claude, en autonomie) :**

À partir des UC de la spec et des étapes précédentes, Claude identifie :

1. **Flux métier principaux** — Extraits directement des étapes Na/Nb des
   UC. Claude regroupe les UC liés par des relations include/extend pour
   reconstituer les parcours de bout en bout (ex : le parcours « inscription
   → commande → paiement → livraison » correspond à une chaîne de UC liés).
   Pour chaque flux, Claude note les composants impliqués et les données
   transportées.

2. **Flux d'intégration** — Identifiés via les étapes où le système
   interagit avec un acteur de type « système » ou un service externe
   mentionné dans la spec.

3. **Flux d'événements** — Identifiés via les étapes asynchrones des UC
   (notifications, traitements différés, jobs planifiés) et les acteurs de
   type « système » (cron, batch).

4. **Flux d'erreur** — Extraits directement des exceptions des UC. Chaque
   exception documentée dans la spec correspond à un chemin d'erreur
   que l'architecture doit supporter.

5. **Cycles de vie des entités** — Les champs **État initial** et **État
   final** de chaque UC révèlent les transitions d'état des entités métier.
   En chaînant les UC qui partagent les mêmes entités, Claude reconstitue
   les diagrammes de transition d'état complets (source pour § 4.3 de
   l'ARCHITECTURE.md).

Pour chaque flux, Claude note : UC source, déclencheur (étape Na), étapes,
composants impliqués, données transportées, cas d'erreur (exceptions).

**Présentation à l'utilisateur :**

> J'ai identifié **N flux métier** (issus des UC), **M intégrations** et
> **P flux d'événements**. Voici la liste. Je vais te poser des questions
> sur les flux les plus complexes.

**Questions obligatoires :**

1. La liste des flux est-elle complète ?
2. Pour chaque intégration externe : quel protocole ? Quelle authentification ?
   Quel SLA du système tiers ?
3. Y a-t-il des flux qui doivent être transactionnels (tout ou rien) ?
4. Y a-t-il des flux asynchrones nécessitant une garantie de livraison
   (at-least-once, exactly-once) ?

**Questions conditionnelles :**

- Si événements → Message broker dédié ou queues simples ? Ordre garanti ?
- Si fichiers échangés → Formats ? Taille max ? Fréquence ? Validation ?
- Si temps réel → WebSocket, SSE, polling ? Latence acceptable ?

**Livrable intermédiaire :** Cartographie des flux validée.

#### A.5 — Choix technologiques

**Objectif :** Sélectionner et justifier chaque brique de la stack technique.
Pas de technologie sans raison documentée. Pour chaque choix, au moins une
alternative écartée doit être mentionnée.

**Travail d'analyse (Claude, en autonomie) :**

À partir des contraintes (A.1), des données (A.3) et des flux (A.4), Claude
propose une stack technique en respectant ces principes :

1. **Contraintes d'abord** — Les technologies imposées par la spec ou
   l'utilisateur sont non négociables.
2. **Cohérence de l'écosystème** — Préférer des technologies qui fonctionnent
   bien ensemble (ex : ne pas mixer 4 langages sans raison).
3. **Maturité et support** — Préférer des technologies stables, bien
   documentées, avec une communauté active.
4. **Pérennité** — Évaluer le risque d'obsolescence de chaque brique
   (mainteneur, fréquence des releases, taille de la communauté). Si le
   risque est modéré ou plus, documenter un plan de mitigation (migration,
   fork, remplacement).
5. **Coût total** — Inclure les coûts de licence, d'hébergement, de formation,
   de maintenance.

**Présentation à l'utilisateur :**

Pour chaque brique, Claude présente :

> | Besoin | Proposition | Pourquoi | Alternative écartée | Pourquoi écartée |
> |--------|-------------|----------|---------------------|------------------|
> | [ex: API REST] | [ex: FastAPI] | [ex: Async, typage natif, perf] | [ex: Django REST] | [ex: Plus lourd, sync par défaut] |

**Questions obligatoires :**

1. Valides-tu ces choix ? Y a-t-il des technologies que tu veux imposer ou
   exclure ?
2. Y a-t-il des contraintes de licence ? (open source uniquement, licence
   commerciale interdite, etc.)
3. L'équipe maîtrise-t-elle ces technologies ou faut-il prévoir une montée
   en compétence ?

**Livrable intermédiaire :** Stack technique validée avec justifications.

#### A.6 — Propriétés non-fonctionnelles

**Objectif :** Traduire les exigences non-fonctionnelles de la spec (ENF-xxx)
et les contraintes non fonctionnelles rattachées aux UC en décisions
architecturales concrètes. Couvrir aussi les propriétés non explicitement
demandées mais nécessaires.

**Exploitation préalable de la spec :**

Claude exploite le champ **Fréquence d'utilisation** de chaque UC pour
alimenter le dimensionnement. Les UC à haute fréquence (ex : « 500 fois/jour »)
orientent les choix de performance, cache et scalabilité. Les UC à faible
fréquence (ex : « mensuel ») peuvent tolérer des traitements plus lourds.

**Axes d'analyse systématique :**

Claude passe en revue chaque axe et évalue sa pertinence pour le projet :

| Axe | Questions clés | Impact architectural |
|-----|---------------|---------------------|
| **Performance** | Temps de réponse cible ? Débit max ? Latence max ? | Cache, CDN, index, pré-calcul |
| **Scalabilité** | Croissance attendue ? Pics de charge ? | Horizontal vs vertical, stateless, sharding |
| **Disponibilité** | SLA cible ? Tolérance aux pannes ? | Réplication, failover, multi-AZ |
| **Résilience** | Que se passe-t-il si un composant tombe ? | Circuit breaker, retry, DLQ, graceful degradation |
| **Observabilité** | Comment savoir que le système fonctionne ? | Métriques, logs structurés, traces, alertes |
| **Maintenabilité** | Facilité à modifier, corriger, étendre ? | Modularité, tests, documentation, DX |
| **Portabilité** | Dépendance à un fournisseur ? Migration possible ? | Abstraction, standards, IaC |
| **Coût** | Budget contraint ? Optimisation nécessaire ? | Sizing, auto-scaling, reserved instances |

Pour chaque axe pertinent, Claude pose 1-2 questions ciblées à l'utilisateur
pour préciser les attentes et les seuils.

**Livrable intermédiaire :** Tableau des propriétés non-fonctionnelles avec
seuils chiffrés et décisions architecturales associées.

#### A.7 — Synthèse et arbitrages

**Objectif :** Consolider toute la réflexion en une vision architecturale
cohérente. Identifier les trade-offs et les décisions ouvertes. C'est la
dernière étape avant la rédaction.

**Travail de synthèse (Claude, en autonomie) :**

Claude produit un document de synthèse structuré :

1. **Vision architecturale** — Description en 5-10 phrases du système tel
   qu'il sera construit.
2. **Composants identifiés** — Liste des composants avec leurs responsabilités.
   Les packages de niveau 2 de la spec servent de piste initiale pour le
   découpage, mais l'architecture n'est pas tenue de reproduire exactement
   la structure des packages (un package peut être éclaté en plusieurs
   composants, ou plusieurs packages fusionnés dans un composant).
3. **Matrice de traçabilité UC → Composants** — Tableau montrant quel
   composant implémente quel UC. Cela garantit la couverture complète.
   La **priorité** de chaque UC (Critique/Important/Souhaité) est reportée
   dans la matrice pour guider les arbitrages : un UC Critique impose des
   choix architecturaux non négociables, un UC Souhaité peut accepter des
   compromis.
4. **Trade-offs explicites** — Pour chaque compromis fait, documenter ce qui
   a été sacrifié et pourquoi (ex : « On choisit la cohérence éventuelle
   plutôt que la cohérence forte pour gagner en disponibilité »).
5. **Décisions ouvertes** — Points qui restent à trancher, avec les options
   et leurs conséquences.
6. **Risques architecturaux** — Points de fragilité identifiés, avec des
   pistes de mitigation.

**Présentation à l'utilisateur :**

> **Synthèse architecturale — Validation avant rédaction**
>
> [Synthèse complète incluant la matrice UC → Composants]
>
> **Décisions ouvertes (à trancher maintenant) :**
> 1. [Décision 1] — Option A vs Option B
> 2. [Décision 2] — ...
>
> **Risques identifiés :**
> 1. [Risque 1] — Mitigation proposée : [...]
>
> Tu valides cette vision ? Une fois validée, je rédige le ARCHITECTURE.md.

Claude ne passe à la rédaction que lorsque l'utilisateur valide explicitement
la synthèse. Si l'utilisateur demande des modifications, Claude revient à
l'étape concernée.

#### A.8 — Rédaction

**Prérequis :** La synthèse A.7 est validée par l'utilisateur.

Rédige le ARCHITECTURE.md section par section en suivant le template
`references/TEMPLATE-ARCHITECTURE.md`. La rédaction s'appuie intégralement sur les livrables intermédiaires
validés aux étapes A.1 à A.7 :

- § 1 (Vue d'ensemble) ← A.1 cadrage + A.7 vision + diagramme de contexte de la spec
- § 2 (Principes) ← A.7 trade-offs + A.6 propriétés
- § 3.1 (Choix technologiques) ← A.5 choix avec alternatives écartées
- § 3.2 (Pérennité) ← A.5 évaluation du risque d'obsolescence par technologie
- § 3.3 (Coûts) ← A.5 estimation des coûts de fonctionnement
- § 4.1 (Diagramme d'architecture) ← A.7 composants + A.4 flux principaux
- § 4.2 (Composants) ← A.7 composants identifiés + matrice UC → Composants
- § 4.3 (Flowcharts) ← A.4 flux métier (issus des étapes Na/Nb des UC)
- § 4.4 (Séquences intégrations) ← A.4 flux d'intégration et d'événements
- § 4.5 (State diagrams) ← A.4 cycles de vie (états initiaux/finaux des UC)
- § 4.6 (Inventaire données) ← A.3 modèle de données (basé sur objets participants)
- § 4.7 (Initialisation) ← A.3 données initiales
- § 5 (Propriétés non-fonctionnelles) ← A.6 seuils chiffrés + décisions
- § 6 (Décisions d'architecture) ← A.7 trade-offs + décisions ouvertes tranchées
- § 7 (Structure répertoire) ← A.7 composants + A.5 stack
- § 8 (Glossaire) ← termes accumulés + glossaire projet de la spec
- § 9 (Documents de référence) ← documents utilisés et produits

Présente chaque section majeure à l'utilisateur pour validation avant de
passer à la suivante. Les diagrammes Mermaid doivent être syntaxiquement
corrects et refléter fidèlement les flux validés en A.4.

**Convention de traçabilité dans l'ARCHITECTURE.md :**

Les références à la spec utilisent les identifiants suivants :
- `UC-xxx` — Cas d'utilisation
- `CA-UC-xxx-yy` — Critère d'acceptation d'un UC
- `RG-xxxx` — Règle de gestion
- `ENF-xxx` — Exigence non fonctionnelle
- `CA-ENF-xxx-yy` — Critère d'acceptation d'une ENF
- `IHM-xxx` — Référence d'interface

### Phase B — Déploiement (DEPLOYMENT.md)

#### Questions obligatoires

1. Comment le logiciel est-il distribué aujourd'hui (ou comment doit-il
   l'être) ? (conteneurs, packages, installeur, téléchargement, store)
2. Quels sont les environnements cibles ? (dev, staging, production, on-premise)
3. Y a-t-il un pipeline CI/CD existant ? (outils, plateforme)
4. Qui opère le système en production ? (équipe interne, client, managé)
5. Quelle est la stratégie de mise à jour ? (rolling, blue-green, canary,
   manuelle)

#### Questions conditionnelles

- Si SaaS → Multi-tenant ? Isolation des données ? CDN ?
- Si client lourd → Mécanisme de mise à jour automatique ? Signature du code ?
- Si driver → Processus de certification ? Signature noyau ?
- Si logiciel embarqué → Quel mécanisme de distribution (TMS/MDM, app
  store, flashage firmware) ? Parc homogène ou hétérogène ? Si parc
  hétérogène, y a-t-il une HAL ? Mode hors-ligne requis ? Contraintes
  de certification (PCI-PTS, EMVCo, App Store Review) ?
- Si on-premise → Prérequis réseau ? Proxy ? Pare-feu ?

#### Rédaction

Le DEPLOYMENT.md est construit à partir du tronc commun
(`references/TEMPLATE-DEPLOYMENT.md`) complété par le sous-template
correspondant au type de solution identifié en A.1 :

| Type de solution | Sous-template |
|---|---|
| SaaS | `references/TEMPLATE-DEPLOYMENT-SAAS.md` |
| Client lourd / Desktop | `references/TEMPLATE-DEPLOYMENT-DESKTOP.md` |
| Driver / Firmware | `references/TEMPLATE-DEPLOYMENT-DRIVER.md` |
| Logiciel embarqué (mobile, TPE, terminal pro, dev board) | `references/TEMPLATE-DEPLOYMENT-EMBEDDED.md` |
| Bibliothèque / CLI / Autre | Pas de sous-template — tronc commun uniquement |

Les sections du sous-template sont insérées après le tronc commun,
numérotées à la suite. Si le type de solution ne correspond à aucun
sous-template, le tronc commun suffit.

### Phase C — Sécurité (SECURITY.md)

#### C.1 — Modèle de menaces

**Travail d'analyse (Claude, en autonomie) :**

Claude exploite la spec (acteurs, interfaces, points d'entrée) et
l'ARCHITECTURE.md (composants, flux, exposition réseau) pour produire :

1. **Surface d'attaque** — Points d'entrée du système, exposition, données
   accessibles.
2. **Acteurs malveillants** — Profils d'attaquants, motivations, capacités.
3. **Frontières de confiance** — Zones de confiance et contrôles requis à
   chaque franchissement.

Claude présente ce modèle à l'utilisateur pour validation avant de
poursuivre.

#### C.2 — Questions de cadrage

**Questions obligatoires :**

1. Quels sont les actifs à protéger ? (données, accès, disponibilité)
2. Qui sont les utilisateurs et quels rôles ont-ils ? (exploiter la section
   Acteurs de la spec)
3. Y a-t-il des politiques de sécurité internes à respecter ?
4. Le système est-il exposé sur Internet ?
5. Quels référentiels de sécurité appliquer ? (ANSSI, OWASP ASVS, CIS,
   ISO 27001, interne)
6. Existe-t-il un plan de réponse à incident ? Si non, qui serait
   responsable en cas d'incident ?

**Questions conditionnelles :**

- Si données de santé → Exigences HDS ? Pseudonymisation ?
- Si données personnelles → Traitements RGPD identifiés ? DPO nommé ?
- Si API publique → Rate limiting ? Authentification ? CORS ?
- Si upload de fichiers → Types autorisés ? Taille max ? Scan antimalware ?
- Si driver/client lourd → Signature du binaire ? Analyse statique ?
  Protection mémoire ?

#### C.3 — Rédaction

Le SECURITY.md suit le template `references/TEMPLATE-SECURITY.md` et
couvre les axes suivants :

1. **Modèle de menaces** (§ 2) : surface d'attaque, acteurs malveillants,
   frontières de confiance.
2. **Exigences organisationnelles** (§ 3) : politiques internes.
3. **Bonnes pratiques** (§ 4) : authentification, sessions, cryptographie,
   protection applicative, gestion des erreurs, sécurité API, upload,
   journalisation, segmentation réseau, continuité.
4. **Référentiels sectoriels** (§ 5) : exigences de sécurité induites par
   les référentiels du marché (PGSSI-S, PCI-DSS, DORA, NIS2, etc.)
   identifiés dans la spec. Supprimer si non applicable.
5. **Principes de développement sécurisé** (§ 6) : règles de codage
   sécurisé (effacement mémoire, fail securely, encodage contextuel, etc.).
6. **SDLC sécurisé et supply chain** (§ 7) : SAST, DAST, audit dépendances,
   SBOM, hardening, signature.
7. **Stack technique** (§ 8) : exigences spécifiques par technologie.
8. **Réponse à incident** (§ 9) : rôles, procédure, notification.
9. **Conformité et privacy** (§ 10) : renvoi vers COMPLIANCE_MATRIX.md,
   obligations RGPD liées à la sécurité.
10. **Spécificités** (§ 11) : exigences propres au contexte du projet.

Chaque exigence est numérotée selon la convention définie dans le template.

### Phase D — Conformité (COMPLIANCE_MATRIX.md)

#### Évaluation préalable

Avant de rédiger, Claude évalue si un fichier de conformité est pertinent :

- Si la spec ne mentionne aucun cadre réglementaire → Informer
  l'utilisateur que le fichier n'est pas nécessaire et proposer de passer.
- Si la spec mentionne un cadre réglementaire (HDS, RGPD, PGSSI-S,
  PCI-DSS, SOC2, etc.) → Identifier les référentiels applicables et
  confirmer avec l'utilisateur.

#### Questions obligatoires (si applicable)

1. Quels référentiels réglementaires s'appliquent au projet ?
2. Y a-t-il des UC ou ENF de la spec qui déclenchent ces obligations ?
   (identifier les UC-xxx / ENF-xxx « mères »)
3. Qui est responsable de la conformité ? (rôle, équipe)
4. Y a-t-il des certifications à obtenir ?
5. Pour chaque exigence, qui en porte l'implémentation ? (responsable par
   exigence ou par lot d'exigences)
6. Y a-t-il des échéances réglementaires ou contractuelles ? (dates butoirs
   de mise en conformité)

#### Rédaction

Les exigences de conformité sont numérotées avec un préfixe propre au
référentiel (HDS-xx, RGPD-xx, PGSSI-xx, etc.) et rattachées à leur
exigence « mère » dans la spec (UC-xxx ou ENF-xxx). Elles ne
réutilisent jamais la numérotation UC-xxx / ENF-xxx de la spec.

## Format de livraison

Produis chaque document comme un fichier téléchargeable, pas comme du texte
dans le chat. Le chat sert au dialogue (questions, validations, arbitrages).

**Création initiale :**
1. Rédige chaque document au fil des phases. À chaque validation de section
   par l'utilisateur, mets à jour le fichier.
2. Commence toujours par ARCHITECTURE.md — les autres documents en dépendent.
3. Livre chaque document séparément dans `docs/`.

**Mise à jour :**
1. Produis le document modifié complet, pas un diff.
2. Si une modification d'architecture impacte le déploiement ou la sécurité,
   signale-le et propose de mettre à jour les documents concernés.
3. Mets à jour le changelog en fin de fichier.

**Convention de versioning :**
- **Majeure (X.0)** : changement structurel d'architecture, ajout ou retrait
  d'un composant majeur, changement de stack.
- **Mineure (X.Y)** : ajout de détail, précision, correction, ajout d'une
  exigence de sécurité.

## Renvois croisés entre documents

Les documents de conception forment un tout cohérent. Utilise des renvois
croisés pour éviter la redondance :

- ARCHITECTURE.md → référence les UC (UC-xxx), règles de gestion (RG-xxxx),
  exigences non fonctionnelles (ENF-xxx) et critères d'acceptation
  (CA-UC-xxx-yy, CA-ENF-xxx-yy) de la spec
- DEPLOYMENT.md → référence les composants de ARCHITECTURE.md
- SECURITY.md → référence les composants de ARCHITECTURE.md et les UC /
  ENF de la spec
- COMPLIANCE_MATRIX.md → référence les UC / ENF « mères » de la spec et les
  exigences de SECURITY.md quand elles se recoupent

Format de renvoi : `Voir ARCHITECTURE.md § 4.2` ou `Réf. UC-007`.

## Checklist de validation

Avant de remettre chaque document à l'utilisateur, vérifie :

### ARCHITECTURE.md
- [ ] Le diagramme d'architecture haut niveau (§ 4.1) est présent et lisible.
- [ ] Chaque composant (§ 4.2) a une responsabilité unique et claire.
- [ ] La matrice de traçabilité UC → Composants couvre tous les UC de la spec avec leur priorité.
- [ ] Les diagrammes Mermaid (flowcharts § 4.3, séquences § 4.4, states § 4.5) sont syntaxiquement corrects.
- [ ] La stack technique (§ 3.1) est justifiée (chaque choix avec alternative écartée).
- [ ] La pérennité des choix (§ 3.2) est évaluée (risque d'obsolescence, plan de mitigation si risque modéré+).
- [ ] Les propriétés non-fonctionnelles (§ 5) ont des seuils chiffrés et des décisions associées.
- [ ] Les décisions d'architecture (§ 6) documentent les trade-offs et leurs conséquences.
- [ ] L'inventaire des données (§ 4.6) couvre les objets participants de la spec.
- [ ] La structure du répertoire (§ 7) est cohérente avec l'architecture.
- [ ] Le glossaire technique (§ 8) couvre les termes spécifiques sans dupliquer le glossaire projet.
- [ ] Les coûts de fonctionnement (§ 3.2) sont estimés.

### DEPLOYMENT.md
- [ ] Les prérequis sont listés exhaustivement (infra, logiciels, réseau, secrets).
- [ ] La configuration par environnement (§ 4) est documentée.
- [ ] La procédure de déploiement est reproductible par un agent IA.
- [ ] La stratégie de rollback est documentée.
- [ ] Les health checks et critères de readiness (§ 8) sont définis.
- [ ] Le monitoring et les alertes sont définis.
- [ ] Le disaster recovery (§ 11) documente RPO/RTO et les scénarios de sinistre.
- [ ] Le sous-template spécifique au type de solution est intégré (si applicable).

### SECURITY.md
- [ ] Le modèle de menaces est documenté (surface d'attaque, acteurs, frontières de confiance).
- [ ] Chaque exigence a un ID unique, une description et un statut.
- [ ] Les exigences organisationnelles sont couvertes.
- [ ] Les bonnes pratiques couvrent : auth, sessions, crypto, protection applicative, gestion des erreurs, API, upload (si applicable), journalisation, segmentation réseau, continuité.
- [ ] Le SDLC sécurisé est documenté (SAST, DAST, dépendances, SBOM, hardening).
- [ ] Les exigences spécifiques à la stack sont documentées.
- [ ] Le plan de réponse à incident est renseigné (rôles, procédure, notification).
- [ ] Les obligations de conformité/privacy sont résumées (avec renvoi vers COMPLIANCE_MATRIX.md si applicable).

### COMPLIANCE_MATRIX.md
- [ ] Chaque exigence est rattachée à son référentiel source.
- [ ] Les UC / ENF « mères » de la spec sont identifiés.
- [ ] Chaque exigence a un responsable et une échéance.
- [ ] La numérotation est indépendante de la spec.
- [ ] La légende des statuts est présente.

## Passage de relais

Quand les documents de conception sont produits et validés, Claude informe
l'utilisateur de la suite du flux SDD :

```
Les documents de conception sont prêts :
- ARCHITECTURE.md v1.0
- DEPLOYMENT.md v1.0
- SECURITY.md v1.0
- COMPLIANCE_MATRIX.md v1.0 (si applicable)

La prochaine étape du flux SDD est la planification : découper le travail
en lots et plans d'implémentation à partir de l'architecture et de la
spec. Tu peux le faire manuellement ou avec un skill de planification.

Ces documents sont vivants — ils seront mis à jour au fil du développement
si des décisions d'architecture évoluent.
```

## Utilisation des templates

Les templates sont définis dans le répertoire `references/` du skill. Ne génère
jamais la structure d'un document de mémoire — les templates sont la
référence. Remplis les sections au fil du dialogue, supprime les sections
marquées comme optionnelles si elles ne s'appliquent pas, et retire les
commentaires HTML avant livraison.

| Document | Template |
|---|---|
| ARCHITECTURE.md | `references/TEMPLATE-ARCHITECTURE.md` |
| DEPLOYMENT.md | `references/TEMPLATE-DEPLOYMENT.md` + sous-template selon le type de solution |
| SECURITY.md | `references/TEMPLATE-SECURITY.md` |
| COMPLIANCE_MATRIX.md | `references/TEMPLATE-COMPLIANCE-MATRIX.md` |

