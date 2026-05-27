---
name: auth-package
description: This skill should be used when the user asks to "add authentication", "protect a route", "use auth hooks", "integrate Auth0", "add login/logout", "use AuthProvider", "verify JWT", or mentions @mbe/auth, OIDC, access tokens, or authentication in React or Fastify.
---

# Auth Package Development Skill

This skill provides patterns for using the `@mbe/auth` package, a portable OIDC-compliant authentication layer with React hooks for frontend and a Fastify plugin for backend JWT validation.

## Package Overview

**Location**: `packages/auth/`
**Package**: `@mbe/auth`
**Auth Provider**: Auth0 (OIDC-compliant)

### Module Entry Points

| Import | Purpose |
|--------|---------|
| `@mbe/auth` | All exports (React + Fastify + types) |
| `@mbe/auth/react` | React hooks and AuthProvider only |
| `@mbe/auth/fastify` | Fastify plugin only |
| `@mbe/auth/types` | Type definitions only |

## React Authentication

### Setting Up AuthProvider

Wrap the app with `AuthProvider` in the root component:

```typescript
import { AuthProvider } from "@mbe/auth/react";
import type { OIDCConfig } from "@mbe/auth/types";

const config: OIDCConfig = {
  authority: import.meta.env.VITE_AUTH_AUTHORITY,
  clientId: import.meta.env.VITE_AUTH_CLIENT_ID,
  redirectUri: import.meta.env.VITE_AUTH_REDIRECT_URI,
  audience: import.meta.env.VITE_AUTH_AUDIENCE,
  scope: "openid profile email",  // default
};

function App() {
  return (
    <AuthProvider config={config}>
      <RouterProvider router={router} />
    </AuthProvider>
  );
}
```

### useAuth Hook

Primary hook for authentication state and actions:

```typescript
import { useAuth } from "@mbe/auth/react";

function MyComponent() {
  const {
    isLoading,        // true while initializing auth state
    isAuthenticated,  // true if user has valid session
    user,             // AuthUser | null
    accessToken,      // string | null (for API calls)
    signIn,           // () => void - redirect to login
    signOut,          // () => void - redirect to logout
    signInSilent,     // () => Promise - refresh token
    error,            // Error | null
  } = useAuth();

  if (isLoading) return <Spinner />;
  if (!isAuthenticated) return <LoginPrompt onLogin={signIn} />;

  return <div>Welcome, {user?.name}</div>;
}
```

### useAccessToken Hook

Convenience hook for getting the access token:

```typescript
import { useAccessToken } from "@mbe/auth/react";

function ApiComponent() {
  const accessToken = useAccessToken();

  const fetchData = async () => {
    const res = await fetch("/api/v1/users/me", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    return res.json();
  };
}
```

### useRequireAuth Hook

Auto-triggers login if not authenticated:

```typescript
import { useRequireAuth } from "@mbe/auth/react";

function ProtectedPage() {
  const { isLoading, user } = useRequireAuth();

  if (isLoading) return <Spinner />;
  // User is guaranteed authenticated here
  return <Dashboard user={user} />;
}
```

### Logout Pattern

```typescript
function Header() {
  const { user, signOut } = useAuth();

  return (
    <header>
      <span>{user?.name}</span>
      <button onClick={signOut}>Logout</button>
    </header>
  );
}
```

## Fastify Authentication

### Using the Auth Plugin

Register the plugin to protect all routes:

```typescript
import Fastify from "fastify";
import { authPlugin, getAuthPluginOptionsFromEnv } from "@mbe/auth/fastify";

const app = Fastify();

// Load config from AUTH_AUTHORITY and AUTH_AUDIENCE env vars
const authOptions = getAuthPluginOptionsFromEnv();

await app.register(authPlugin, {
  ...authOptions,
  excludePaths: ["/health", "/docs"],  // Skip auth for these
});

// All routes now have request.user populated (if valid JWT)
```

### Manual Plugin Configuration

```typescript
import { authPlugin } from "@mbe/auth/fastify";

await app.register(authPlugin, {
  authority: "https://dev-ytbgmz5ls3wh4xdx.us.auth0.com",
  audience: "https://api.mattbutlerengineering.com",
  excludePaths: ["/health"],
});
```

### Protecting Individual Routes

Use `requireAuth` as a preHandler:

```typescript
import { requireAuth } from "@mbe/auth/fastify";

fastify.get(
  "/me",
  {
    preHandler: requireAuth,
    schema: {
      security: [{ bearerAuth: [] }],
      // ...
    },
  },
  async (request, reply) => {
    // request.user is guaranteed to exist
    const { id, email, name } = request.user!;
    return { data: { id, email, name } };
  }
);
```

### Accessing the Authenticated User

After auth validation, `request.user` contains:

```typescript
interface AuthUser {
  id: string;           // User ID (from JWT sub claim)
  email?: string;
  name?: string;
  picture?: string;
  emailVerified?: boolean;
  raw: JWTPayload;      // Full decoded token
}

// Usage in route handler
async (request, reply) => {
  const user = request.user;
  if (!user) {
    return reply.code(401).send({ error: "Unauthorized" });
  }
  // Use user.id, user.email, etc.
}
```

## Type Definitions

### OIDCConfig

```typescript
interface OIDCConfig {
  authority: string;              // OIDC provider URL
  clientId: string;               // OAuth client ID
  redirectUri: string;            // Post-login redirect
  postLogoutRedirectUri?: string; // Post-logout redirect
  scope?: string;                 // Default: "openid profile email"
  audience?: string;              // API audience
}
```

### JWTPayload

```typescript
interface JWTPayload {
  sub: string;              // Subject (user ID)
  iss: string;              // Issuer
  aud: string | string[];   // Audience
  exp: number;              // Expiration timestamp
  iat: number;              // Issued at timestamp
  email?: string;
  email_verified?: boolean;
  name?: string;
  picture?: string;
  [key: string]: unknown;   // Custom claims
}
```

## Environment Variables

### Frontend (Vite)

```bash
VITE_AUTH_AUTHORITY=https://dev-ytbgmz5ls3wh4xdx.us.auth0.com
VITE_AUTH_CLIENT_ID=<Auth0 App Client ID>
VITE_AUTH_REDIRECT_URI=http://localhost:3002/hospitality/callback
VITE_AUTH_AUDIENCE=https://api.mattbutlerengineering.com
```

### Backend (Node.js)

```bash
AUTH_AUTHORITY=https://dev-ytbgmz5ls3wh4xdx.us.auth0.com
AUTH_AUDIENCE=https://api.mattbutlerengineering.com
```

## Auth0 Configuration

- **Domain**: `dev-ytbgmz5ls3wh4xdx.us.auth0.com`
- **API Identifier**: `https://api.mattbutlerengineering.com`
- **Management**: Pulumi IaC in `infrastructure/pulumi/`

## Common Patterns

### Protected Route with Loading State

```typescript
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isLoading, isAuthenticated, signIn } = useAuth();

  if (isLoading) return <LoadingSpinner />;
  if (!isAuthenticated) {
    signIn();
    return <div>Redirecting to login...</div>;
  }
  return <>{children}</>;
}
```

### API Client with Auth Token

```typescript
import { useAccessToken } from "@mbe/auth/react";

function useApiClient() {
  const accessToken = useAccessToken();

  return {
    get: async (path: string) => {
      const res = await fetch(`/api${path}`, {
        headers: accessToken
          ? { Authorization: `Bearer ${accessToken}` }
          : {},
      });
      return res.json();
    },
  };
}
```

### Conditional UI Based on Auth

```typescript
function Navigation() {
  const { isAuthenticated, user, signIn, signOut } = useAuth();

  return (
    <nav>
      {isAuthenticated ? (
        <>
          <span>{user?.name}</span>
          <button onClick={signOut}>Logout</button>
        </>
      ) : (
        <button onClick={signIn}>Login</button>
      )}
    </nav>
  );
}
```

## Testing

### Test Commands

```bash
cd packages/auth

pnpm test                    # Run all tests
pnpm test:watch              # Watch mode
pnpm test:coverage           # Coverage report
```

### Mocking useAuth in Tests

```typescript
import { vi } from "vitest";

vi.mock("@mbe/auth/react", () => ({
  useAuth: () => ({
    isLoading: false,
    isAuthenticated: true,
    user: { id: "123", email: "test@example.com", name: "Test User" },
    accessToken: "mock-token",
    signIn: vi.fn(),
    signOut: vi.fn(),
  }),
}));
```

### Testing Fastify Routes with Auth

```typescript
import { buildApp } from "../app.js";

describe("Protected Routes", () => {
  it("should return 401 without auth header", async () => {
    const app = await buildApp();
    const response = await app.inject({
      method: "GET",
      url: "/v1/users/me",
    });
    expect(response.statusCode).toBe(401);
  });
});
```

## Development Commands

```bash
cd packages/auth

pnpm dev          # Watch mode build
pnpm build        # Build package
pnpm lint         # ESLint check
pnpm typecheck    # TypeScript validation
pnpm test         # Run tests
```

## Auth Flow Summary

```
Frontend Login:
1. User clicks login → signIn() called
2. Redirect to Auth0 login page
3. Auth0 authenticates → redirects to callback URL
4. AuthProvider processes callback, stores tokens
5. useAuth() returns isAuthenticated: true

API Call:
1. useAccessToken() provides Bearer token
2. Request sent with Authorization header
3. Fastify authPlugin validates JWT via JWKS
4. request.user populated with decoded claims
5. Route handler accesses user info

Logout:
1. signOut() called → redirect to Auth0 logout
2. Tokens cleared from browser storage
3. Redirect back to app
```

## E2E Testing with Playwright

Playwright can test authenticated features using programmatic Auth0 login (Resource Owner Password Grant). This bypasses the browser login UI entirely — fast, reliable, CI-friendly.

### Required Environment Variables

```bash
E2E_AUTH0_DOMAIN=dev-ytbgmz5ls3wh4xdx.us.auth0.com
E2E_AUTH0_CLIENT_ID=<Auth0 client ID with Password grant enabled>
E2E_AUTH0_AUDIENCE=https://api.mattbutlerengineering.com
E2E_AUTH_EMAIL=<test user email>
E2E_AUTH_PASSWORD=<test user password>
```

### Auth0 Prerequisites

1. The Auth0 application must have the **Password** grant type enabled (Settings > Advanced > Grant Types)
2. The test user must use email/password (no MFA, no social login)
3. The default directory in Auth0 must be set to `Username-Password-Authentication`

### Using the authPage Fixture

```typescript
import { test, expect } from "./fixtures.js";

test("authenticated page works", async ({ authPage }) => {
  await authPage.goto("/reservations");
  await expect(authPage.getByTestId("dashboard-layout")).toBeVisible();
});
```

### How It Works

1. `injectAuth0Session()` fetches tokens via Auth0's `/oauth/token` endpoint (ROPC grant)
2. Tokens are injected into `sessionStorage` as an `oidc-client-ts` user entry
3. Page reloads — `react-oidc-context` AuthProvider reads the session and treats user as authenticated
4. No browser login flow, no Auth0 UI interaction, no consent screens

### Running E2E Tests

```bash
cd apps/hospitality
pnpm test:e2e  # Requires E2E_AUTH* env vars
```

## Quick Checklist

### Adding Auth to React App
1. [ ] Wrap app with `AuthProvider`
2. [ ] Configure OIDC settings from env vars
3. [ ] Use `useAuth()` for auth state
4. [ ] Handle loading state before rendering
5. [ ] Use `useAccessToken()` for API calls

### Adding Auth to Fastify Route
1. [ ] Register `authPlugin` or use inline JWT verification
2. [ ] Add `preHandler: requireAuth` for protected routes
3. [ ] Add `security: [{ bearerAuth: [] }]` to schema
4. [ ] Access user via `request.user`
5. [ ] Handle 401 responses for unauthenticated requests
