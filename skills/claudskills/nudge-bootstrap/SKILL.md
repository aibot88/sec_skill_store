---
name: nudge-bootstrap
description: Initialise le projet Nudge de zéro avec Expo, expo-router, TypeScript, NativeWind, Drizzle ORM, expo-sqlite, et configure WebStorm pour un confort optimal. Utilise ce skill UNIQUEMENT au tout premier démarrage du projet Nudge, quand l'utilisateur dit "on commence", "j'initialise le projet", "crée le squelette", "setup du repo", "on fait T01", ou équivalent. Ne pas utiliser pour ajouter des dépendances à un projet existant — ce skill est one-shot, pour la création initiale (correspond à la tâche T01 du skill `nudge-project`). Il fournit les commandes exactes à exécuter (pas une génération IA qui peut halluciner des versions), et termine par un commit initial `milestone-T01`.
---

# Nudge — Bootstrap du projet

Ce skill te guide pour initialiser **une seule fois** le projet Nudge. Il n'est pas fait pour être rejoué. Il produit un squelette d'app Expo fonctionnel, ouvrable dans WebStorm, avec toutes les dépendances de la stack figée, et un premier commit.

## Principe important

Tu es dans un environnement où tu **ne peux pas exécuter les commandes à la place de l'utilisateur** (pas d'accès à sa machine). Ton rôle est de lui fournir la séquence exacte de commandes à copier-coller dans son terminal, **dans l'ordre**, en expliquant brièvement chaque étape pour qu'il comprenne ce qu'il fait (important pour un TDAH : comprendre maintient l'attention).

Donne les commandes **bloc par bloc**, pas tout d'un coup. Attends que l'utilisateur confirme que l'étape a marché avant de passer à la suivante. Si une étape échoue, diagnostique avant d'avancer.

## Prérequis à vérifier avec l'utilisateur avant de commencer

Demande-lui de confirmer qu'il a :

1. **Node.js ≥ 20 LTS** installé (`node -v`)
2. **pnpm** installé (`pnpm -v` → sinon : `npm i -g pnpm`)
3. **Git** configuré (`git config --global user.name` / `user.email`)
4. **WebStorm** installé (toute version récente, 2024.3+)
5. **Un téléphone avec Expo Go** installé (App Store / Play Store) OU un émulateur iOS/Android
6. Un dossier parent où il veut créer le projet (ex: `~/dev/`)

Si quelque chose manque, aide-le à l'installer avant de continuer.

## Étape 1 — Création du projet Expo

Dans le dossier parent choisi, faire :

```bash
pnpm create expo-app@latest nudge --template default
cd nudge
```

Le template `default` inclut déjà expo-router et TypeScript, c'est exactement ce qu'on veut.

Ensuite, vérifier que l'app démarre :

```bash
pnpm start
```

Scanner le QR code avec Expo Go sur iOS (appareil photo) ou Android (bouton "Scan QR code" dans Expo Go). Confirmer que l'app de démo s'affiche. Puis arrêter le serveur avec Ctrl+C.

**Si ça ne marche pas** : vérifier que le téléphone et l'ordinateur sont sur le même réseau Wi-Fi. Option de secours : `pnpm start --tunnel` (plus lent mais fonctionne partout).

## Étape 2 — Nettoyage du template

Le template Expo contient un tutoriel de démo. On le retire pour partir d'une base propre :

```bash
pnpm reset-project
```

Répondre **"n"** quand il demande si on veut garder l'ancien dossier `app-example/` (on ne le veut pas, on archive via git de toute façon).

Résultat attendu : `app/index.tsx` et `app/_layout.tsx` minimalistes, rien d'autre.

## Étape 3 — Ajout de NativeWind v4

On utilise NativeWind v4 (stable avec SDK 54), pas v5 (encore en preview). Dans le dossier du projet :

```bash
pnpm add nativewind react-native-reanimated react-native-safe-area-context
pnpm add -D tailwindcss@^3.4.17 prettier-plugin-tailwindcss
npx tailwindcss init
```

### Configurer `tailwind.config.js`

Remplacer le fichier généré par :

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,jsx,ts,tsx}", "./components/**/*.{js,jsx,ts,tsx}"],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors: {
        // Palette shame-free : pas de rouge vif, pas d'alerte agressive
        bg: "#FAFAF7",
        fg: "#1A1A1A",
        muted: "#6B6B6B",
        accent: "#5B8DEF",       // bleu calme
        soft: "#F0EDE6",
        success: "#7CB88F",      // vert doux, pas criard
      },
    },
  },
  plugins: [],
};
```

### Créer `global.css` à la racine

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Configurer `babel.config.js` à la racine

Créer ou remplacer :

```js
module.exports = function (api) {
  api.cache(true);
  return {
    presets: [
      ["babel-preset-expo", { jsxImportSource: "nativewind" }],
      "nativewind/babel",
    ],
    plugins: ["react-native-reanimated/plugin"],
  };
};
```

### Configurer `metro.config.js` à la racine

```js
const { getDefaultConfig } = require("expo/metro-config");
const { withNativeWind } = require("nativewind/metro");

const config = getDefaultConfig(__dirname);
module.exports = withNativeWind(config, { input: "./global.css" });
```

### Importer `global.css` dans `app/_layout.tsx`

Ajouter tout en haut du fichier :

```tsx
import "../global.css";
```

### Test rapide

Modifier `app/index.tsx` pour utiliser une classe Tailwind :

```tsx
import { Text, View } from "react-native";

export default function Index() {
  return (
    <View className="flex-1 items-center justify-center bg-bg">
      <Text className="text-fg text-2xl">Nudge</Text>
    </View>
  );
}
```

Relancer `pnpm start`, recharger l'app (secouer le téléphone → Reload). Confirmer que le fond est bien crème (`bg-bg`) et le texte sombre. Si NativeWind ne s'applique pas, refaire un build natif propre : `pnpm start --clear`.

## Étape 4 — Ajout de la stack de données : Drizzle + expo-sqlite

```bash
pnpm add drizzle-orm expo-sqlite
pnpm add -D drizzle-kit
```

### Créer `db/schema.ts`

Crée le dossier `db/` puis le fichier, avec le schéma encodant le modèle figé (Task, Step, TaskInstance) :

```ts
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";

export const tasks = sqliteTable("tasks", {
  id: text("id").primaryKey(),
  title: text("title").notNull(),
  outcome: text("outcome").notNull(),
  stepsJson: text("steps_json").notNull(), // Step[] sérialisé
  recurrenceJson: text("recurrence_json"), // Recurrence | null
  scheduledAt: integer("scheduled_at", { mode: "timestamp" }),
  notifyAt: integer("notify_at", { mode: "timestamp" }),
  musicQuery: text("music_query"),
  createdAt: integer("created_at", { mode: "timestamp" }).notNull(),
  archivedAt: integer("archived_at", { mode: "timestamp" }),
});

export const taskInstances = sqliteTable("task_instances", {
  id: text("id").primaryKey(),
  taskId: text("task_id").notNull().references(() => tasks.id),
  date: text("date").notNull(), // YYYY-MM-DD
  completedStepsJson: text("completed_steps_json").notNull().default("[]"),
  completedAt: integer("completed_at", { mode: "timestamp" }),
  skippedAt: integer("skipped_at", { mode: "timestamp" }),
});
```

### Créer `db/client.ts`

```ts
import { openDatabaseSync } from "expo-sqlite";
import { drizzle } from "drizzle-orm/expo-sqlite";
import * as schema from "./schema";

const sqlite = openDatabaseSync("nudge.db");
export const db = drizzle(sqlite, { schema });
```

### Configurer `drizzle.config.ts` à la racine

```ts
import type { Config } from "drizzle-kit";

export default {
  schema: "./db/schema.ts",
  out: "./db/migrations",
  dialect: "sqlite",
  driver: "expo",
} satisfies Config;
```

Générer la première migration :

```bash
pnpm drizzle-kit generate
```

Cela crée `db/migrations/` avec les fichiers SQL. Tu appliqueras ces migrations au runtime lors de la tâche T02 (pas besoin de le faire maintenant).

## Étape 5 — Zustand pour le state

```bash
pnpm add zustand
```

Pas de config nécessaire. Les stores seront créés au fur et à mesure dans `stores/`.

## Étape 6 — Dépendances utilitaires

```bash
pnpm add uuid date-fns
pnpm add -D @types/uuid
pnpm add expo-notifications expo-linking
```

- `uuid` : génération d'IDs pour les tasks
- `date-fns` : manipulation des dates (plus léger que moment, plus explicite que dayjs)
- `expo-notifications` : notifications locales (opt-in only, rappel dans le skill projet)
- `expo-linking` : deep links vers Spotify et autres apps musique

## Étape 7 — Structure des dossiers

Créer la structure cible :

```bash
mkdir -p components stores lib templates assets/images
```

Organisation :

```
nudge/
├── app/                  # expo-router, écrans
│   ├── _layout.tsx
│   ├── index.tsx        # écran accueil (liste du jour)
│   ├── focus/           # mode focus plein écran
│   └── task/            # CRUD task
├── components/           # composants réutilisables
├── db/
│   ├── schema.ts
│   ├── client.ts
│   └── migrations/
├── stores/               # zustand stores
├── lib/                  # helpers purs (pas de state, pas de React)
├── templates/            # les 20 templates de tâches livrés (TS objects)
├── assets/
├── global.css
├── tailwind.config.js
├── babel.config.js
├── metro.config.js
├── drizzle.config.ts
└── tsconfig.json
```

## Étape 8 — TypeScript strict

Éditer `tsconfig.json` pour passer en strict complet :

```json
{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["**/*.ts", "**/*.tsx", ".expo/types/**/*.ts", "expo-env.d.ts"]
}
```

`noUncheckedIndexedAccess` est important : il évite des bugs subtils et pousse à écrire du code défensif (bienvenu dans une app qu'on veut fiable).

## Étape 9 — Scripts pnpm pratiques

Éditer `package.json`, section `scripts` :

```json
{
  "scripts": {
    "start": "expo start",
    "android": "expo start --android",
    "ios": "expo start --ios",
    "web": "expo start --web",
    "doctor": "npx expo-doctor",
    "db:generate": "drizzle-kit generate",
    "db:studio": "drizzle-kit studio",
    "reset-project": "node ./scripts/reset-project.js",
    "typecheck": "tsc --noEmit"
  }
}
```

Vérifier que tout est sain :

```bash
pnpm doctor
pnpm typecheck
```

Si `expo-doctor` signale des mismatches de versions, laisser faire `npx expo install --fix`.

## Étape 10 — Git initial et .gitignore

`create-expo-app` a déjà initialisé git et créé un `.gitignore` correct. Ajouter ces lignes à la fin du `.gitignore` pour Drizzle et WebStorm :

```
# Drizzle
db/migrations/meta/_journal.json.bak

# WebStorm
.idea/workspace.xml
.idea/usage.statistics.xml
.idea/shelf/
.idea/dictionaries/
.idea/httpRequests/
.idea/dataSources/
.idea/dataSources.local.xml
```

**Note** : on garde `.idea/` partiellement versionné (pour le code style, inspections), mais on exclut les fichiers personnels.

## Étape 11 — Configuration WebStorm

Ouvrir le projet dans WebStorm :

```bash
webstorm .
```

(ou `open -a WebStorm .` sur macOS, ou simplement File > Open > choisir le dossier)

### 11.1 — Marquer les dossiers

Clic droit sur chaque dossier → "Mark Directory as" :

- `app/`, `components/`, `stores/`, `lib/`, `templates/`, `db/` → **Sources Root**
- `db/migrations/` → **Excluded** (généré, ne pas indexer)
- `node_modules/` et `.expo/` sont déjà excluded par défaut

### 11.2 — Activer Tailwind dans WebStorm

Settings → Plugins → chercher "Tailwind CSS" → installer si pas déjà fait → redémarrer.
Settings → Languages & Frameworks → Style Sheets → Tailwind CSS → activer et pointer sur `tailwind.config.js`.

### 11.3 — Configurer ESLint & Prettier

Le template Expo fournit déjà eslint. Vérifier :
Settings → Languages & Frameworks → JavaScript → Code Quality Tools → ESLint → "Automatic ESLint configuration" coché.

Installer Prettier :

```bash
pnpm add -D prettier
```

Créer `.prettierrc` à la racine :

```json
{
  "semi": true,
  "singleQuote": false,
  "tabWidth": 2,
  "printWidth": 100,
  "trailingComma": "all",
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

Settings → Languages & Frameworks → JavaScript → Prettier → sélectionner le Prettier package du projet, cocher "On save" et "On 'Reformat Code' action".

### 11.4 — Configuration de lancement

Settings → Tools → npm → Run configuration :
Créer une config "Start Expo" : type `npm`, scripts `start`, package manager `pnpm`.
Créer une config "Typecheck" : scripts `typecheck`.

Tu peux maintenant lancer l'app avec le bouton Play de WebStorm.

### 11.5 — Code style

File → Settings → Editor → Code Style → TypeScript :
- Indent: 2 spaces
- Continuation indent: 2
- Right margin: 100

Cocher "Use tab character" : **non**. Cocher "Smart tabs" : non.

### 11.6 — Database tool (bonus)

WebStorm intègre un client SQL. Pour inspecter la DB SQLite de ton app en dev :
View → Tool Windows → Database → + → Data Source → SQLite → pointer vers le fichier `.db` dans `~/Library/Developer/CoreSimulator/Devices/.../nudge.db` (iOS simulator) ou via `adb pull` sur Android. Pratique pour debug. Peut attendre que tu en aies besoin.

## Étape 12 — Fichier README minimal

Créer/remplacer `README.md` :

```markdown
# Nudge

Une app mobile TDAH-first pour décomposer les tâches du quotidien.

Local-first. Pas de compte. Pas de jugement.

## Stack

Expo SDK 54 · TypeScript · expo-router · NativeWind v4 · Drizzle ORM · expo-sqlite · Zustand

## Commandes

- `pnpm start` — lance le dev server
- `pnpm ios` / `pnpm android` — lance sur simulateur
- `pnpm typecheck` — vérifie les types
- `pnpm doctor` — diagnostique Expo
- `pnpm db:generate` — génère les migrations Drizzle
- `pnpm db:studio` — ouvre Drizzle Studio

## Roadmap

Voir `ROADMAP.md` ou le skill `nudge-project` pour le détail.
```

## Étape 13 — Premier commit milestone

```bash
git add -A
git commit -m "chore: bootstrap Expo + NativeWind + Drizzle + WebStorm setup

- Expo SDK 54 avec expo-router
- TypeScript strict
- NativeWind v4 avec palette shame-free
- Drizzle ORM + expo-sqlite, schéma Task/TaskInstance
- Zustand pour le state
- Config WebStorm (Tailwind plugin, Prettier, run configs)

Refs: milestone-T01"

git tag milestone-T01
```

## Check-list finale

Avant de considérer le bootstrap fini, vérifier :

- [ ] `pnpm start` lance l'app, elle s'affiche sur le téléphone
- [ ] Une classe Tailwind (`bg-bg`, `text-fg`) s'applique visuellement
- [ ] `pnpm typecheck` passe sans erreur
- [ ] `pnpm doctor` ne signale que des warnings, pas d'erreurs bloquantes
- [ ] WebStorm autocomplete les classes Tailwind
- [ ] Le tag git `milestone-T01` existe (`git tag --list`)

Si tout est coché : **la tâche T01 est officiellement finie.** Ouvrir le skill `nudge-project` pour voir la tâche T02 et ses sous-tâches ("Première Task persistée").

## Si ça foire

Les pièges classiques et leurs solutions :

- **"Tailwind classes ne s'appliquent pas"** → `pnpm start --clear` pour vider le cache Metro. Si ça persiste, vérifier que `global.css` est bien importé dans `_layout.tsx`.
- **"Expo Go déconnecte"** → passer en `--tunnel`, ou s'assurer que firewall/Wi-Fi n'isolent pas les clients.
- **"Peer dep conflict sur Reanimated"** → `npx expo install --fix` aligne toutes les versions sur celles attendues par le SDK.
- **"Drizzle Studio ne voit pas la DB"** → normal en RN, la DB est dans le sandbox de l'app. Utiliser l'outil Database de WebStorm pointé vers le fichier `.db` du simulateur.

Ne pas bricoler les versions manuellement. Toujours passer par `npx expo install <package>` plutôt que `pnpm add` pour les packages Expo — ça garantit la compat avec le SDK en cours.
