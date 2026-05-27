---
name: sdd-uc-spec-write
description: >
  Rédige et met à jour les spécifications SDD par cas d'utilisation (UC) :
  spec racine (projet principal) ou spec d'extension (fonction ajoutée à
  une racine existante). Exploitable par des agents IA. En CLI écrit dans
  docs/, sur claude.ai livre des artefacts Markdown. S'active dès qu'on
  demande une spec SDD, à formaliser des UC, ou à étendre une spec racine.
metadata:
  version: "2.5.0"
  author: "Franz TRIERWEILER"
license: "MIT"
---

# Spec Driven Development (SDD) — Rédaction par cas d'utilisation

Version : 2.5.0
Date : 2026-04-28

## Barre de progression — OBLIGATION STRICTE

**Chaque réponse produite sous ce skill DOIT commencer par la barre de
progression ci-dessous. AUCUNE EXCEPTION. Cela inclut le message d'accueil.**

```
🖊️ skill:sdd-uc-spec-write v2.5.0 · [Étape] [barre] sous-étape N/T — [Nom]
```

Caractère plein : `█` — Caractère vide : `░`. Voir la section
« Identification du skill dans les réponses » plus bas pour le détail
des sous-étapes et les exemples complets.

## Prérequis — vérification au démarrage

Avant toute autre action, vérifie que les fichiers suivants existent dans le
répertoire `references/` du skill :

| Fichier | Rôle |
|---|---|
| `references/TEMPLATE-SPEC.md` | Template de référence pour la génération d'un document racine |
| `references/TEMPLATE-SPEC-EXTENSION.md` | Template de référence pour la génération d'un document d'extension |
| `references/UC-FORMAT.md` | Format et règles de rédaction des cas d'utilisation |
| `references/UPDATE-WORKFLOW.md` | Workflow de mise à jour d'une spec existante |
| `references/EXTENSION-WORKFLOW.md` | Workflow de création d'une extension fonctionnelle |
| `references/GLOSSARY-SDD.md` | Glossaire méthodologique SDD |

Si un ou plusieurs fichiers sont absents, **arrête immédiatement** et affiche :

```
⚠️ Fichier(s) manquant(s) dans references/ : [liste].
Le skill ne peut pas fonctionner sans ces fichiers. Vérifie que le skill
a été installé avec son répertoire references/ complet.
```

Ne tente pas de générer la spec de mémoire si un fichier de référence manque.

## Message d'accueil

Quand le skill est activé, Claude commence par chercher des fichiers
`docs/SPEC-racine-*.md` et `docs/SPEC-extension-*.md`. Selon le résultat,
il affiche l'un des messages ci-dessous avant toute autre action.

**Logique de détection :**

1. Aucun `SPEC-racine-*.md` trouvé → **Mode 1 (création racine)**
2. Un ou plusieurs documents SPEC trouvés, au moins un incomplet → **Mode 2 (reprise)**
3. Tous les documents SPEC complets + intention d'extension détectée → **Mode 4 (extension)**
4. Tous les documents SPEC complets + pas d'intention d'extension → proposer le choix modification / extension

Un document est considéré incomplet s'il contient des placeholders `[...]`,
des sections vides, des UC sans critères d'acceptation, ou si des sections
attendues du template sont absentes.

**Détection du vocabulaire d'extension (option hybride) :**

- Vocabulaire non ambigu → mode 4 directement : « nouvelle fonction »,
  « extension », « module supplémentaire », « fonctionnalité supplémentaire »,
  « ajouter une fonction au projet ».
- Vocabulaire ambigu → demander clarification : « ajouter une fonction » sans
  « extension » ou « nouvelle ». Question : « Tu veux ajouter une fonction dans
  un UC existant (modification) ou documenter une nouvelle fonction dans un
  SPEC-extension ? »
- Vocabulaire de modification → mode 3 directement : « modifier », « corriger »,
  « mettre à jour », « compléter ».

---

**Mode 1 — Rédaction initiale (aucun SPEC-racine-*.md trouvé) :**
```
🖊️ skill:sdd-uc-spec-write v2.5.0 · Cadrage [░░░░] 0/4 — Démarrage

Ce skill produit des spécifications logicielles structurées par cas d'utilisation (UC),
selon la méthodologie Spec Driven Development (SDD). L'objectif est de produire un
document suffisamment précis pour qu'un agent IA implémente le logiciel sans ambiguïté,
et suffisamment clair pour qu'un décideur non technique comprenne ce qui sera livré.

Je vais te guider en trois étapes :
1. Cadrage — produire un cahier des charges introductif (contexte, acteurs, contraintes, périmètre).
2. Cas d'utilisation — détailler chaque UC avec ses étapes, exceptions, règles de gestion.
3. Compléments — objets participants, exigences non fonctionnelles, périmètre.

On commence par le cadrage.
```

**Mode 2 — Reprise d'une rédaction en cours (document incomplet détecté) :**

Si plusieurs documents existent, lister ceux qui sont incomplets et demander
sur lequel travailler.

```
🖊️ skill:sdd-uc-spec-write v2.5.0 · [Étape détectée] [barre] — Reprise

J'ai trouvé [nom du fichier] mais il est incomplet. Sections manquantes ou
incomplètes :
- [liste des manques détectés]

Je te propose de reprendre la rédaction à partir de [étape détectée].
Tu préfères reprendre là où ça s'est arrêté, ou travailler sur une
section spécifique ?
```

**Mode 3 — Modification d'un document existant (document complet) :**

Si plusieurs documents complets existent, lister et demander lequel modifier.

```
🖊️ skill:sdd-uc-spec-write v2.5.0 · Mise à jour [░░░] 0/3 — Démarrage

J'ai trouvé [nom du fichier]. Ce skill permet de modifier une spécification
SDD existante structurée par cas d'utilisation. Je peux intervenir sur :
- Les cas d'utilisation (ajout, modification, dépréciation)
- Le glossaire
- Les exigences non fonctionnelles
- Les niveaux de support et le hors périmètre
- L'arborescence et les diagrammes
- Toute autre section

Quelle section veux-tu modifier ?
```

**Mode 4 — Création d'une extension (spec racine complète + intention extension) :**

```
🖊️ skill:sdd-uc-spec-write v2.5.0 · Extension [░░░░] 0/4 — Démarrage

J'ai trouvé [nom de la spec racine] ([N] UC, v[X.Y]).

Je vais créer une extension pour documenter la fonction « [nom] ». Ce document
sera autonome et lié à la spec racine. Je te guide en quatre étapes :
1. Cadrage fonction — identifier la fonction, son préfixe, ses dépendances racine.
2. Cas d'utilisation — détailler les UC de la fonction (identifiants préfixés).
3. Compléments — objets participants, exigences non fonctionnelles.
4. Finalisation — vérification des dépendances et passage de relais.

On commence par le cadrage de la fonction.
```

**Choix proposé (spec racine complète, intention non détectée) :**

```
🖊️ skill:sdd-uc-spec-write v2.5.0 · Démarrage

J'ai trouvé [liste des documents SPEC].

Je peux :
1. Modifier un document existant — mise à jour ciblée (UC, RG, ENF, glossaire...)
2. Créer une extension — documenter une nouvelle fonction dans un SPEC-extension lié à la spec racine

Que veux-tu faire ?
```

## Critères de déclenchement

### Déclenchement primaire (haute confiance — active le skill directement)

- L'utilisateur demande explicitement une spec SDD (racine ou extension)
  ou mentionne "Spec Driven Development" / "SDD" comme méthodologie.
- L'utilisateur demande de rédiger des cas d'utilisation (UC) pour un projet logiciel.
- L'utilisateur demande de rédiger une spécification par cas d'utilisation.
- L'utilisateur demande de produire une spécification structurée destinée
  à être implémentée par un agent IA.
- L'utilisateur fournit des notes informelles et demande de les transformer
  en spécification structurée par cas d'utilisation.
- L'utilisateur fournit une spec existante et demande de la modifier, compléter
  ou mettre à jour.

### Déclenchement secondaire (confiance moyenne — demande confirmation)

- L'utilisateur veut "formaliser" ou "structurer" un cahier des charges sans
  mentionner SDD → Demande : "Tu veux un cahier des charges classique ou une
  spec SDD structurée par cas d'utilisation ?"
- L'utilisateur veut documenter des règles métier sans contexte d'implémentation
  → Demande : "Ces règles doivent-elles aboutir à une implémentation logicielle ?"
- L'utilisateur mentionne "spécifier un comportement" ou "documenter des scénarios"
  sans contexte clair → Demande : "Tu veux intégrer ça dans une spec SDD complète
  ou juste documenter ce point isolément ?"

### Anti-triggers (ne pas déclencher)

- L'utilisateur demande de lire, analyser ou résumer une spec existante sans
  intention de la produire ou la modifier.
- L'utilisateur rédige de la documentation utilisateur, un README, ou un guide
  d'utilisation.
- L'utilisateur écrit des tests, même s'il mentionne des critères d'acceptation
  (les tests consomment la spec, ils ne la produisent pas).
- L'utilisateur pose une question technique sur une API ou un format sans vouloir
  produire de spécification.
- L'utilisateur demande une revue de code ou un audit technique.

## Philosophie

Une spec SDD n'est pas un cahier des charges classique destiné à être interprété uniquement
par des humains. C'est un **document de référence exécutable**, construit pour une lecture
humaine mais aussi par un agent IA : suffisamment précis pour qu'un agent IA produise
une implémentation conforme sans poser de questions, et suffisamment clair pour qu'un décideur
non technique comprenne ce qui sera livré.

Une fois la spec produite, un autre agent (ou skill) l'utilise comme entrée pour construire
l'architecture technique, les consignes de sécurité et les plans de développement, en vue de
commencer l'implémentation. La spec est donc le point d'entrée de toute la chaîne de
production logicielle.

Chaque phrase de la spec doit répondre à cette question : **"Un agent IA qui lit uniquement ce
document peut-il implémenter correctement ce comportement, sans deviner ?"** Si la réponse est
non, la spec est incomplète.

La spec est le contrat entre celui qui spécifie et celui qui implémente — qu'il soit humain ou IA.
Elle est le point de vérité unique du projet. Le code en découle et doit être traçable
jusqu'à la spec.

Les critères d'acceptation sont conçus pour être directement convertibles en tests automatisés.
Un agent IA peut générer une suite de tests à partir de la seule lecture des CA, sans
information supplémentaire. Cette propriété est intentionnelle : si un critère d'acceptation
n'est pas transformable en test, il est trop vague — reformule-le.

## Concepts clés

### Acteurs

Un acteur est un type d'utilisateur (un profil) qui **modifie l'état interne du système**.
Un acteur peut être :
- **Humain** : Client, Administrateur, Gestionnaire, Caissière, etc.
- **Système** : Cron, service externe, batch planifié, etc.

**Ne sont PAS des acteurs :**
- Les destinataires d'une action (ex : Imprimante, service de notification).
- Le système qu'on modélise lui-même.

### Relations entre cas d'utilisation

Trois types de relations peuvent exister entre UC :

| Relation | Description | Fréquence |
|---|---|---|
| **Include** | Un UC inclut obligatoirement un autre UC. Le UC inclus est toujours exécuté. | Courante |
| **Extend** | Un UC étend un autre UC de manière optionnelle, sous certaines conditions. | Courante |
| **Généralisation / Spécialisation** | Un UC hérite du comportement d'un UC parent et le spécialise. | Rare |

Chaque UC documente ses relations dans un champ dédié. Les diagrammes Mermaid
sont régénérés à chaque livraison pour refléter ces relations.

### Paquetages et arborescence

Les cas d'utilisation sont organisés en une arborescence de **paquetages**.
Le modèle est volontairement souple : un paquetage peut contenir à la fois
d'autres paquetages **et** des cas d'utilisation (enfants mixtes), à
n'importe quelle profondeur.

**Règles de structuration :**

| Règle | Valeur | Origine |
|---|---|---|
| Sous-paquetages max par paquetage parent | **7** | Loi de Miller (7±2) |
| UC max par paquetage feuille | **10** | Lisibilité d'un diagramme UC |
| Profondeur recommandée | **3 niveaux** | Convergence UML (Fowler, Larman, Booch) |
| Profondeur plafond pratique | **4 niveaux** | Au-delà : signe de sur-décomposition |
| Profondeur > 4 | **Avertissement** | Proposer une fusion |

Aucune limite formelle au-delà de 4, mais Claude alerte l'utilisateur si la
profondeur dépasse ce seuil et propose un regroupement.

**Trois vues complémentaires** structurent la livraison de l'arborescence :

1. **Carte d'ensemble** — liste imbriquée Markdown. Lecture en 10 secondes,
   table des matières du système. Paquetages en gras avec count d'UCs entre
   parenthèses ; UCs listés sous leur parent direct.
2. **Fiches paquetage** — un bloc par paquetage non-feuille, avec objectif
   et tableau à 2 colonnes (Type | Élément) listant ses enfants directs.
   Format constant quelle que soit la profondeur, scannable et parsable.
3. **Diagramme Mermaid** — vue géographique. Si ≤ 20 UC : un seul diagramme
   global avec `subgraph` par paquetage. Si > 20 UC : un diagramme par
   paquetage racine + un diagramme « 30 000 pieds » des paquetages seuls
   (sans les UCs).

L'arborescence sert de cartographie du système et est réutilisable pour le
lotissement et la priorisation du développement.

### Diagramme de contexte

Le diagramme de contexte est un **schéma informel** (pas de formalisme UML) dont
l'objectif est de permettre à une personne extérieure de comprendre le périmètre
du système **en 10 secondes**. C'est un objet de communication.

Caractéristiques :
- Schéma non formel, statique (aucun élément dynamique).
- Éléments qui doivent y apparaître :
  - Les acteurs.
  - Les structures organisationnelles (entreprise, fournisseur, etc.).
  - Les principaux objets (voiture, colis, livre, etc.).
  - Les éléments géographiques (usine, restaurant, bibliothèque, agence, etc.).
  - Les postes clients, les terminaux de consultation.
  - Les applications informatiques ou sites Web (placés dans les structures
    organisationnelles ou géographiques).

L'utilisateur peut fournir ce schéma sous forme d'image que Claude interprète.

## Identification du skill dans les réponses

**OBLIGATION STRICTE — AUCUNE EXCEPTION.** Chaque réponse produite sous ce
skill commence par une barre de progression indiquant le skill actif, l'étape
en cours et l'avancement. Cette règle s'applique dès la toute première réponse
(message d'accueil inclus) et à chaque message suivant. Ne jamais omettre
cette ligne, même si le fichier SKILL.md a été lu partiellement.

**Format :**

```
🖊️ skill:sdd-uc-spec-write v2.5.0 · [Étape] [barre] sous-étape N/T — [Nom]
```

La version affichée est celle indiquée dans l'en-tête du skill (actuellement v2.5.0).

**Règles de la barre de progression :**

- Caractère plein : `█` — Caractère vide : `░`
- Largeur fixe : 4 caractères pour Cadrage (4 sous-étapes), variable pour
  Cas d'utilisation (1 caractère par paquetage racine), 5 caractères pour Compléments.
- La barre reflète la sous-étape en cours (incluse).

**Découpage en sous-étapes (document racine) :**

| Étape | Sous-étapes | Total |
|-------|-------------|-------|
| Cadrage | 1. Questions obligatoires · 2. Questions conditionnelles · 3. Diagramme de contexte · 4. Rédaction & validation sections initiales | 4 |
| Cas d'utilisation | 1. Arborescence & diagramme global · puis 1 sous-étape par paquetage racine (nombre variable, noté N/M) | 1+M |
| Compléments | 1. Machines à états · 2. Phases de livraison · 3. Objets participants · 4. Exigences non fonctionnelles · 5. Rédaction finale & passage de relais | 5 |

**Découpage en sous-étapes (extension) :**

| Étape | Sous-étapes | Total |
|-------|-------------|-------|
| Cadrage fonction | 1. Identification fonction & préfixe · 2. Contexte & dépendances racine · 3. Diagramme de contexte fonction · 4. Rédaction & validation sections initiales | 4 |
| Cas d'utilisation | 1. Arborescence & diagramme · puis 1 sous-étape par paquetage racine | 1+M |
| Compléments | 1. Machines à états · 2. Phases de livraison · 3. Objets participants · 4. Exigences non fonctionnelles | 4 |
| Finalisation | 1. Vérification table des dépendances · 2. Rédaction finale & passage de relais | 2 |

**Exemples :**

```
🖊️ skill:sdd-uc-spec-write v2.5.0 · Cadrage [█░░░] 1/4 — Questions obligatoires
🖊️ skill:sdd-uc-spec-write v2.5.0 · Cadrage [████] 4/4 — Rédaction & validation
🖊️ skill:sdd-uc-spec-write v2.5.0 · Cas d'utilisation [█░░░░] arborescence — Structure des paquetages
🖊️ skill:sdd-uc-spec-write v2.5.0 · Cas d'utilisation [████░] paquetage 3/4 — Export
🖊️ skill:sdd-uc-spec-write v2.5.0 · Compléments [█████] 5/5 — Rédaction finale & passage de relais
```

**Cas particulier — Mise à jour d'une spec existante :**

```
🖊️ skill:sdd-uc-spec-write v2.5.0 · Mise à jour [██░] 2/3 — Application des modifications
```

Sous-étapes de mise à jour : 1. Lecture & périmètre · 2. Application ·
3. Changelog & impacts.

**Cas particulier — Création d'une extension :**

```
🖊️ skill:sdd-uc-spec-write v2.5.0 · Extension [█░░░] 1/4 — Cadrage fonction
🖊️ skill:sdd-uc-spec-write v2.5.0 · Extension [██░░] paquetage 2/3 — Import
🖊️ skill:sdd-uc-spec-write v2.5.0 · Extension [███░] 3/4 — Compléments
🖊️ skill:sdd-uc-spec-write v2.5.0 · Extension [████] 4/4 — Finalisation
```

Si plusieurs messages se succèdent au sein de la même sous-étape (ex :
clarifications, allers-retours), la barre reste identique. Elle avance
uniquement au passage à la sous-étape suivante.

## Processus de rédaction

**RAPPEL OBLIGATOIRE : chaque réponse produite sous ce skill DOIT commencer par
la barre de progression (voir section « Identification du skill dans les réponses »).
Aucune exception. Cela s'applique dès la première réponse, y compris le message
d'accueil.**

La rédaction d'une spec SDD par cas d'utilisation est un dialogue, pas une génération
en un coup. Claude guide l'utilisateur à travers trois étapes successives, en posant
des questions ciblées pour collecter l'information nécessaire avant de rédiger chaque
section. L'objectif est d'extraire la connaissance métier que l'utilisateur possède
et que Claude ne peut pas deviner.

### Étape 1 — Cadrage

Avant de rédiger quoi que ce soit, pose ces questions pour remplir les sections
Contexte, Architecture et périmètre. Pose-les par petits groupes
(3 à 5 questions maximum à la fois) pour ne pas submerger l'utilisateur.

**Questions obligatoires :**

1. Que fait le logiciel en une phrase ?
2. Quel problème résout-il, et pour qui ?
3. Y a-t-il des contraintes techniques imposées (langage, plateforme, dépendances) ?
4. Y a-t-il des contraintes réglementaires ou normatives (RGPD, HDS, certification) ?
5. Qui sont les acteurs du système ? (rappel : un acteur est un profil qui modifie
   l'état interne du système — pas un destinataire d'action)

**Questions conditionnelles** (pose-les si le contexte le suggère) :

- Le logiciel interagit-il avec un système existant, du hardware, ou un environnement
  non contrôlé ? → Déclenche la section Niveaux de support.
- Y a-t-il un cadre réglementaire dont certaines obligations se traduisent en
  comportements implémentables ? → Déclenche des cas d'utilisation spécifiques.
- Y a-t-il des contraintes d'architecture technique à respecter (composants imposés,
  intégrations, flux de données) ? → Déclenche la section Architecture.
- Y a-t-il des contraintes de performance, de sécurité, de fiabilité ou de
  portabilité ? → Déclenche la section Exigences non-fonctionnelles.
- Qu'est-ce que le logiciel ne fait explicitement pas ? Quelles demandes prévisibles
  des utilisateurs doivent être refusées ? → Alimente la section Hors périmètre.
- As-tu un **diagramme de contexte** à fournir pour expliquer le périmètre du système ?
  Si tu n'en as pas, je peux en produire un à partir des informations du cadrage.

Quand les réponses sont suffisantes, rédige les sections initiales du document
(cartouche, contexte, diagramme de contexte si fourni, architecture si applicable,
niveaux de support si applicable, hors périmètre) et présente-les à l'utilisateur
pour validation avant de poursuivre. Le fichier est créé dans `docs/` avec le
nommage défini dans la section « Format de livraison ».

### Étape 2 — Cas d'utilisation

Avant de commencer la rédaction des UC, demande à l'utilisateur :

1. **"As-tu un diagramme des cas d'utilisation à fournir ?"** — Si oui, interprète
   le schéma fourni (image) pour identifier les UC, les acteurs et les relations.

2. **Propose l'arborescence des paquetages :** "Voici la structure que je
   propose pour ton système : [arborescence]. Profondeur : N niveaux,
   M paquetages racine. Tu valides, tu corriges, tu complètes ?"

   Si la profondeur dépasse 4, signale-le explicitement et propose une
   fusion : "L'arborescence dépasse 4 niveaux, ce qui est généralement
   un signe de sur-décomposition. Veux-tu fusionner [paquetages X et Y] ?"

Pour chaque paquetage racine :

1. **Propose** un lot de cas d'utilisation (2 à 4) avec leur structure complète.
   Consulte `references/UC-FORMAT.md` pour le format exact et les questions à poser.
2. **Demande validation** : "Tu valides, tu corriges, tu complètes ?"
3. **Intègre** les retours et passe au lot suivant.

Ne cherche pas l'exhaustivité dès le premier passage. Il vaut mieux couvrir les UC
principaux de chaque paquetage, puis revenir affiner.

Si l'utilisateur fournit des informations que tu ne maîtrises pas entièrement,
demande des précisions plutôt que de deviner. Un UC faux est pire qu'un UC absent.

**Régénération des diagrammes :** À chaque livraison du document, régénère les
diagrammes Mermaid des relations entre UC. Si > 20 UC, découpe par paquetage
racine et ajoute un diagramme « 30 000 pieds » des paquetages seuls (sans
les UCs) en complément.

### Étape 3 — Compléments

Une fois les UC principaux posés, aborde successivement :

1. **Machines à états** : "Y a-t-il un ou plusieurs objets métier dont le cycle
   de vie passe par des états bien définis avec des transitions contraintes
   (ex. intervention, commande, dossier, alerte) ? Si oui, je centralise le
   diagramme et la table des transitions dans une section dédiée — sinon les
   transitions restent éparpillées dans les RGs des UCs et un implémenteur
   doit reconstituer le graphe lui-même."
2. **Phases de livraison** : "Le projet est-il livré en plusieurs incréments
   (phases, jalons) ou en une seule fois ? Si plusieurs, je documente chaque
   phase avec son périmètre (liste des UCs), son livrable et ses dépendances.
   La répartition des UCs sur les phases sert de matrice de traçabilité pour
   le découpage en lots aval (`/sdd-plan`)."
   Si le cadrage a déjà mentionné des phases (CDC, brief), proposer la
   répartition des UCs et demander validation. Vérifier que **chaque UC
   figure dans exactement une phase** avant de livrer.
3. **Objets participants** : "Veux-tu documenter une liste d'objets métier identifiés
   (entités, agrégats) ? Tu peux aussi fournir des diagrammes d'objets."
4. **Exigences non fonctionnelles** : "Y a-t-il des contraintes non fonctionnelles
   à documenter (performance, sécurité, fiabilité, portabilité, etc.) ?"
5. **Passage de relais** — Voir section dédiée.

### Format de livraison

Produis chaque document comme un fichier téléchargeable, pas comme du texte dans
le chat. Le chat sert au dialogue (questions, validations, arbitrages). Les fichiers
portent le contenu livrable.

**Création initiale :** Le fichier **ne doit jamais s'appeler `SPEC.md`**. Utilise
la convention de nommage décrite ci-dessous pour nommer le fichier dès la première
écriture (exemple : `docs/SPEC-racine-MaintiX.md`).
Le nom du fichier sur disque doit correspondre exactement au champ `Document`
du cartouche. Rédige le document au fil des étapes en utilisant le template
défini dans `references/TEMPLATE-SPEC.md`. À chaque validation de section par
l'utilisateur, mets à jour le fichier. Livre les documents complémentaires
(DATA-MODEL.md, etc.) séparément.

**Mise à jour :** Produis le document modifié complet, pas un diff. Régénère les
diagrammes Mermaid. Consulte `references/UPDATE-WORKFLOW.md` pour les règles
d'identifiants, le changelog et le workflow détaillé.

**Nommage :** Le nom du fichier encode uniquement le type et le projet (et la
fonction pour les extensions). Les métadonnées (version, date, statut) restent
dans le cartouche — le fichier n'est jamais renommé.

- Document racine : `SPEC-racine-<NomProjet>.md`
- Document d'extension : `SPEC-extension-<NomProjet>-<NomFonction>.md`

Exemples :
- `SPEC-racine-MaintiX.md`
- `SPEC-extension-MaintiX-Alertes.md`

Le `<NomProjet>` et `<NomFonction>` utilisent le PascalCase sans espaces ni
caractères spéciaux. Le champ `Document` du cartouche contient le nom complet
du fichier.

Schéma de données : `DATA-MODEL.md` (nommage inchangé).

### Passage de relais

Quand les trois étapes sont terminées et que le document contient un cadrage validé,
des cas d'utilisation couvrant les paquetages principaux, et des compléments documentés,
informe l'utilisateur que le document est suffisamment structuré pour qu'il puisse le
compléter et l'enrichir lui-même.

Dis-le explicitement, par exemple : "[nom du fichier] a maintenant une structure solide
avec [N] cas d'utilisation répartis en [paquetages]. Tu peux désormais le compléter
directement — ajouter des UC, affiner les étapes et exceptions, préciser les règles de
gestion — en suivant le format et les conventions établis. Le glossaire et la structure
des identifiants (UC/RG/IHM/ENF/CA) te guident."

L'objectif du skill n'est pas de rédiger 100% de la spec. C'est d'amorcer le document
avec suffisamment de structure, de rigueur et d'exemples concrets pour que l'utilisateur
soit autonome pour la suite. La spec est un document vivant qui s'enrichit au fil du
projet.

Avant de remettre la spec à l'utilisateur, vérifie chaque point de la checklist et
signale les manques.

Le skill suivant dans la chaîne SDD est `sdd-uc-system-design`, qui prend ce document
comme entrée pour produire l'architecture technique, le déploiement, la sécurité et
la matrice de conformité.

### Mise à jour d'une spec existante

Pour le workflow complet de mise à jour (types de modifications, règles d'identifiants,
changelog, processus), consulte `references/UPDATE-WORKFLOW.md`. Ce workflow s'applique
aussi bien aux documents racine qu'aux extensions (modes 2 et 3 polymorphes).

### Création d'une extension

Pour le workflow complet de création d'extension, consulte
`references/EXTENSION-WORKFLOW.md`. Les grandes étapes sont :

**Étape 1 — Cadrage fonction :**

1. Identifier la fonction à documenter (nom court, objectif).
2. Dériver et valider le préfixe (3-4 lettres, ex : ALR pour « Alertes »).
   Scanner les extensions existantes pour éviter les collisions.
3. Lire la spec racine pour extraire l'UUID, les acteurs, les UC et RG
   disponibles pour les références croisées.
4. Créer le fichier `docs/SPEC-extension-<NomProjet>-<NomFonction>.md` en
   utilisant le template `references/TEMPLATE-SPEC-EXTENSION.md`.
5. Rédiger le contexte de la fonction, le diagramme de contexte (si fourni),
   et les sections initiales. Présenter à l'utilisateur pour validation.

**Étape 2 — Cas d'utilisation :**

Même processus que pour un document racine (arborescence, puis UC par paquetage),
avec deux différences :
- Tous les identifiants portent le préfixe de l'extension (UC-ALR-001, RG-ALR-0001).
- À chaque référence à un identifiant racine (UC, RG, ENF, IHM ou CA — sans préfixe),
  mettre à jour la table « Dépendances vers la spec racine ». Inclure les
  références citées dans les étapes, exceptions, RGs, IHMs et critères
  d'acceptation, pas seulement dans les relations Include / Extend.

**Étape 3 — Compléments :**

Objets participants et exigences non fonctionnelles spécifiques à la fonction
(identifiants préfixés : ENF-ALR-001).

**Étape 4 — Finalisation :**

1. **Passe de consolidation des dépendances** — scanner le document final pour chaque identifiant racine cité (sans préfixe : `UC-\d+`, `RG-\d+`, `ENF-\d+`, `IHM-\d+`, `CA-(UC|ENF)-\d+-\d+`), et vérifier qu'il figure dans la table « Dépendances vers la spec racine » avec sa nature de dépendance. Toute référence orpheline (citée dans le corps mais absente de la table) doit être ajoutée à la table avant livraison.
2. Vérifier le glossaire fonction (pas de doublons avec la racine).
3. Passer la checklist extension (voir `references/EXTENSION-WORKFLOW.md`).
4. Passage de relais.

## Structure d'un cas d'utilisation

Pour le format exact d'un UC, les règles de rédaction, le format des critères
d'acceptation Soit/Quand/Alors, et les questions à poser à l'utilisateur, consulte
`references/UC-FORMAT.md`.

## Glossaire SDD

Le glossaire SDD est défini dans `references/GLOSSARY-SDD.md`. Reproduis-le en
dernière section de chaque spec produite, tel quel. Ces termes sont imposés par
la méthodologie SDD et ne doivent pas être remplacés par des synonymes.

## Structure d'un document racine (SPEC-racine)

Le document racine suit cet ordre de sections. Le template complet est dans
`references/TEMPLATE-SPEC.md`.

1. **Cartouche** — Blockquote avec tableau : Document, UUID, version, date, auteur, statut, type (`Document racine`), skill générateur. L'UUID (v4) est généré une seule fois à la création du document et ne change jamais par la suite.
2. **Changelog** (à partir de la v1.1) — Entre le cartouche et le contexte.
3. **Contexte et objectifs** — Ce que le projet fait, pourquoi, pour qui, contraintes, acteurs.
4. **Diagramme de contexte** (si fourni) — Schéma informel du périmètre.
5. **Architecture** (si applicable) — Contraintes techniques, composants imposés.
6. **Documents de référence** (si applicable) — Liens vers documents complémentaires.
7. **Niveaux de support** (si applicable) — Supporté / Ignoré / Erreur explicite.
8. **Hors périmètre** — Ce que le logiciel ne fait explicitement pas.
9. **Arborescence des cas d'utilisation** — Trois vues : carte d'ensemble (liste imbriquée), fiches paquetage (tableaux 2 colonnes), diagramme Mermaid avec `subgraph`. Voir `references/TEMPLATE-SPEC.md`.
10. **Diagramme global des cas d'utilisation** — Mermaid avec `subgraph` par paquetage. Découper en diagrammes par paquetage racine si > 20 UC.
11. **Cas d'utilisation détaillés** — Regroupés par paquetage. Format : voir `references/UC-FORMAT.md`.
12. **Machines à états** (si applicable) — Pour chaque objet métier à cycle de vie significatif : diagramme Mermaid des états + tableau des transitions autorisées (De / Vers / Déclencheur / Condition / RG-UC). Centralise une information autrement éparpillée dans les RGs.
13. **Phases de livraison** (si applicable) — Pour chaque phase : périmètre (liste des UCs), livrable, dépendances. Sert aussi de matrice de traçabilité UC ↔ Phase pour le découpage en lots aval.
14. **Objets participants** (si applicable) — Entités métier, diagrammes d'objets/interaction.
15. **Exigences non fonctionnelles** — ENF-XXX avec CA au format Soit/Quand/Alors.
16. **Glossaire projet** — Termes spécifiques au domaine.
17. **Glossaire SDD** — Vocabulaire méthodologique. Voir `references/GLOSSARY-SDD.md`.

## Structure d'un document d'extension (SPEC-extension)

Le document d'extension suit cet ordre de sections. Le template complet est dans
`references/TEMPLATE-SPEC-EXTENSION.md`.

1. **Cartouche** — 11 champs : Document, UUID, version, date, auteur, statut, type (`Document d'extension`), spec racine, UUID racine, préfixe (3-4 lettres), skill générateur.
2. **Changelog** (à partir de la v1.1) — Entre le cartouche et le contexte.
3. **Contexte de la fonction** — Ce que la fonction fait, pourquoi, acteurs concernés, contraintes structurantes.
4. **Diagramme de contexte** (si fourni) — Schéma de la fonction dans son environnement.
5. **Dépendances vers la spec racine** — Tableau des UC/RG racine référencés.
6. **Niveaux de support** (si applicable) — Supporté / Ignoré / Erreur explicite.
7. **Hors périmètre** — Ce que la fonction ne fait explicitement pas.
8. **Arborescence des cas d'utilisation** — Trois vues (carte d'ensemble, fiches paquetage, diagramme Mermaid) avec identifiants préfixés. Voir `references/TEMPLATE-SPEC-EXTENSION.md`.
9. **Diagramme des cas d'utilisation** — Mermaid avec `subgraph` par paquetage de l'extension. UCs racine référencés en pointillés.
10. **Cas d'utilisation détaillés** — Regroupés par paquetage. Identifiants préfixés. Format : voir `references/UC-FORMAT.md`.
11. **Machines à états** (si applicable) — Si l'extension introduit un nouvel objet à cycle de vie ou étend une machine racine, documenter le delta (nouveaux états et transitions) avec identifiants préfixés. Les états et RGs racine restent référencés sans préfixe.
12. **Phases de livraison** (si applicable) — Soit une ligne unique « livrée dans la Phase X de la racine », soit un découpage propre à l'extension avec UCs préfixés.
13. **Objets participants** (si applicable) — Spécifiques à la fonction.
14. **Exigences non fonctionnelles** — ENF préfixées, spécifiques à la fonction.
15. **Glossaire fonction** — Termes nouveaux uniquement.

## Directives de rédaction

### Langue et registre

Rédige dans la langue de l'utilisateur. Utilise un registre professionnel accessible :
compréhensible par un directeur métier, exploitable par un développeur ou un agent IA.
Évite le jargon technique non défini dans le glossaire projet.

### Identifiants — convention de nommage

**Document racine :**
```
UC-001        Cas d'utilisation numéro 1
CA-UC-001-01  Premier critère d'acceptation du UC-001
RG-0001       Règle de gestion numéro 1
IHM-001       Écran / maquette numéro 1
ENF-001       Exigence non-fonctionnelle numéro 1
CA-ENF-001-01  Premier critère d'acceptation de ENF-001
```

**Document d'extension (préfixe ALR pour « Alertes ») :**
```
UC-ALR-001        Cas d'utilisation n°1 de l'extension
CA-UC-ALR-001-01  Premier critère d'acceptation du UC-ALR-001
RG-ALR-0001       Règle de gestion n°1 de l'extension
IHM-ALR-001       Écran n°1 de l'extension
ENF-ALR-001       Exigence non-fonctionnelle n°1 de l'extension
CA-ENF-ALR-001-01 Premier CA de ENF-ALR-001
```

Identifiant sans préfixe = spec racine. Identifiant avec préfixe = extension.
Consulte `references/EXTENSION-WORKFLOW.md` pour les détails.

Numérote séquentiellement. Ne réutilise jamais un identifiant supprimé.
Les identifiants sont référencés dans le code (commentaires) pour assurer la traçabilité.

### Complétude — checklist avant livraison

Avant de considérer la spec comme terminée, vérifie :

- [ ] Le glossaire SDD est présent et intact.
- [ ] Le glossaire projet couvre tous les termes spécifiques utilisés.
- [ ] L'arborescence des UC est complète et cohérente.
- [ ] Aucun paquetage ne dépasse 7 sous-paquetages directs.
- [ ] Aucun paquetage feuille ne dépasse 10 UCs.
- [ ] La profondeur de l'arborescence est ≤ 4 (avertissement au-delà).
- [ ] Chaque UC a au moins un critère d'acceptation.
- [ ] Chaque critère d'acceptation est au format Soit/Quand/Alors.
- [ ] Les étapes de chaque UC suivent la convention Na/Nb (acteur/système).
- [ ] Les exceptions sont rattachées à un id d'étape précis.
- [ ] Les règles de gestion sont identifiées (RG-XXXX) et rattachées à une étape.
- [ ] Les relations entre UC (include, extend) sont documentées.
- [ ] Les diagrammes Mermaid des relations sont à jour.
- [ ] Si un objet métier a un cycle de vie significatif, une section *Machines à états* est présente avec diagramme et table des transitions, et chaque transition est tracée vers une RG / un UC.
- [ ] Si le projet est livré en plusieurs incréments, une section *Phases de livraison* est présente, et chaque UC figure dans exactement une phase (matrice de traçabilité UC ↔ Phase complète).
- [ ] La section Hors périmètre est renseignée.
- [ ] Les niveaux de support sont documentés (si applicable).
- [ ] Les exigences non fonctionnelles pertinentes sont documentées.
- [ ] Un agent IA pourrait implémenter chaque UC sans poser de question.

**Checklist complémentaire pour les extensions :**

- [ ] Le cartouche contient les 11 champs requis (dont Spec racine, UUID racine, Préfixe).
- [ ] Le préfixe est unique (pas de collision avec une autre extension du projet).
- [ ] Tous les identifiants de l'extension portent le préfixe.
- [ ] La table « Dépendances vers la spec racine » est complète et à jour : couvre UC, RG, ENF, IHM et CA. Aucune référence racine orpheline (citée dans le corps mais absente de la table).
- [ ] Les références aux UC/RG/ENF/IHM/CA de la racine utilisent les identifiants sans préfixe.
- [ ] Le glossaire fonction ne duplique pas les termes du glossaire racine.
- [ ] Les diagrammes Mermaid incluent les UC racine référencés (en pointillés).
