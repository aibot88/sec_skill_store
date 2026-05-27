---
name: State Management & Auth Contexts
description: Gestion de l'état global dans Next.js — contextes d'auth Sanctuaire/Expert, entitlements, et hooks React personnalisés.
---

# State Management & Auth Contexts

## Context

Lumira V2 utilise **React Context API** (pas Redux, pas Zustand) pour la gestion d'état global. Deux contextes d'authentification coexistent selon la zone de l'app.

---

## Contextes disponibles

```
apps/web/context/
├── SanctuaireAuthContext.tsx  // JWT client (Sanctuaire)
├── SanctuaireContext.tsx      // Entitlements & capabilities
├── AuthContext.tsx            // Auth générale (legacy)
└── ExpertAuthContext.tsx      // JWT expert (Admin Desk)
```

---

## SanctuaireAuthContext

Gère la session de l'utilisateur final (client).

### Storage des tokens

```typescript
// Clés localStorage
const SANCTUAIRE_TOKEN_KEY = 'sanctuaire_token';
const LUMIRA_TOKEN_KEY = 'lumira_token'; // alias legacy

// Lecture du token
const token = localStorage.getItem('sanctuaire_token') 
           || localStorage.getItem('lumira_token');
```

### Hook d'utilisation

```typescript
'use client';
import { useSanctuaireAuth } from '@/context/SanctuaireAuthContext';

function MyComponent() {
  const { user, isLoading, isAuthenticated, login, logout } = useSanctuaireAuth();

  if (isLoading) return <Spinner />;
  if (!isAuthenticated) return <Redirect to="/sanctuaire/login" />;

  return <div>Bienvenue {user.firstName}</div>;
}
```

### Interface User

```typescript
interface SanctuaireUser {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: 'CLIENT' | 'EXPERT' | 'ADMIN';
  profile?: UserProfile;
}
```

---

## SanctuaireContext — Entitlements

Gère les capacités débloquées selon le niveau d'achat.

### Hook principal

```typescript
'use client';
import { useSanctuaire } from '@/context/SanctuaireContext';

function FeatureGate() {
  const {
    capabilities,        // string[] — liste des capabilities actives
    hasCapability,       // (cap: string) => boolean
    highestLevel,        // 0 | 1 | 2 | 3 | 4
    levelMetadata,       // { name, color, price }
    isLoading,
  } = useSanctuaire();

  // Vérification par capability
  if (!hasCapability('chat_unlimited')) {
    return <UpgradePrompt requiredLevel={3} />;
  }

  // Vérification par niveau
  if (highestLevel < 2) {
    return <LockedFeature minLevel={2} />;
  }

  return <Feature />;
}
```

### Capabilities par niveau

| Capability | Niveau 1 | Niveau 2 | Niveau 3 | Niveau 4 |
|-----------|----------|----------|----------|----------|
| `reading_basic` | ✅ | ✅ | ✅ | ✅ |
| `insights_3` | ✅ | ✅ | ✅ | ✅ |
| `timeline` | ❌ | ✅ | ✅ | ✅ |
| `chat_limited` | ❌ | ✅ | ✅ | ✅ |
| `chat_unlimited` | ❌ | ❌ | ✅ | ✅ |
| `rituals` | ❌ | ❌ | ✅ | ✅ |
| `akashic_record` | ❌ | ❌ | ❌ | ✅ |
| `priority_support` | ❌ | ❌ | ❌ | ✅ |

---

## ExpertAuthContext

Gère la session de l'expert/admin dans le tableau de bord.

```typescript
// Storage key
localStorage.getItem('expert_token');

// Hook
import { useExpertAuth } from '@/context/ExpertAuthContext';

function AdminPage() {
  const { expert, isAdmin, logout } = useExpertAuth();
  // expert.role: 'EXPERT' | 'ADMIN'
}
```

---

## Intercepteur Axios

L'API client injecte automatiquement le token dans les requêtes :

```typescript
// apps/web/lib/api.ts
import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('sanctuaire_token') 
             || localStorage.getItem('lumira_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Intercepteur de réponse pour gérer les 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('sanctuaire_token');
      window.location.href = '/sanctuaire/login';
    }
    return Promise.reject(error);
  }
);
```

---

## Fournisseur de contexte — Root Layout

```tsx
// apps/web/app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <SanctuaireAuthProvider>
          <SanctuaireProvider>         {/* Entitlements */}
            <ExpertAuthProvider>
              {children}
            </ExpertAuthProvider>
          </SanctuaireProvider>
        </SanctuaireAuthProvider>
      </body>
    </html>
  );
}
```

---

## Hooks personnalisés utiles

```typescript
// hooks/useEntitlement.ts
export function useEntitlement(capability: string) {
  const { hasCapability, highestLevel } = useSanctuaire();
  return { 
    isAllowed: hasCapability(capability),
    highestLevel 
  };
}

// hooks/useIsAuthenticated.ts
export function useIsAuthenticated() {
  const { isAuthenticated, isLoading } = useSanctuaireAuth();
  return { isAuthenticated, isLoading };
}
```

---

## Pattern de protection de route

```tsx
// components/guards/AuthGuard.tsx
'use client';

export function AuthGuard({ children, requiredLevel = 0 }) {
  const { isAuthenticated, isLoading } = useSanctuaireAuth();
  const { highestLevel } = useSanctuaire();

  if (isLoading) return <FullPageSpinner />;
  if (!isAuthenticated) redirect('/sanctuaire/login');
  if (highestLevel < requiredLevel) return <UpgradeModal level={requiredLevel} />;

  return children;
}
```

---

## Best Practices

| ✅ DO | ❌ DON'T |
|-------|----------|
| Utiliser `hasCapability()` pour les gates | Comparer directement les niveaux dans les composants |
| Protéger les layouts avec `AuthGuard` | Vérifier l'auth dans chaque composant feuille |
| Stocker sous `sanctuaire_token` | Créer de nouvelles clés localStorage |
| Gérer le `isLoading` avant d'afficher | Flash du contenu privé avant auth check |
| Centraliser la logique d'auth dans les contextes | Dupliquer la logique de refresh token |
