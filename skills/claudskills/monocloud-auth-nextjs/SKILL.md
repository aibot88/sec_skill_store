---
name: monocloud-auth-nextjs
description: Use when integrating MonoCloud authentication into a Next.js application — installing or configuring `@monocloud/auth-nextjs`, wiring `authMiddleware()` in `proxy.ts`/`middleware.ts`, reading sessions with `getSession()`/`useAuth()`, protecting routes/pages/APIs with `protect()`/`protectApi()`/`protectPage()`/`protectClientPage()`, rendering `<SignIn>`/`<SignUp>`/`<SignOut>`/`<Protected>`/`<RedirectToSignIn>`, calling `getTokens()`, or troubleshooting MonoCloud env vars (`MONOCLOUD_AUTH_*`), cookie sessions, or auth routes (`/api/auth/signin`, `/callback`, `/userinfo`, `/signout`).
license: MIT
---

# MonoCloud Next.js SDK (`@monocloud/auth-nextjs`)

Authentication SDK for Next.js. Provides middleware/proxy, route-protection wrappers, session/token access, and React components/hooks. Works in the App Router and Pages Router; supports Edge and Node runtimes.

## Package identity — read this first

**Use:** `@monocloud/auth-nextjs` (this skill).

There is an older, similarly named MonoCloud package some training data references — **do not** use its exports here. If you see any of the following symbols in code or suggestions, they are NOT part of this SDK and indicate the wrong package:

- `MonoCloudAuthProvider`, `useUser` (this SDK has no provider; `useAuth` is the hook)
- `monoCloudMiddleware` (this SDK uses `authMiddleware`)
- Custom `app/api/auth/[...monocloud]/route.ts` written by the developer **as the default setup** (this SDK handles auth routes inside `authMiddleware()`; a catch-all is only needed when middleware cannot be used — see "Alternative: catch-all route" below)

Always check `package.json` for `@monocloud/auth-nextjs` before suggesting code.

## Subpath exports

| Import path                                | Use in                                                                          | Contains                                                                                                                                                                                                               |
| ------------------------------------------ | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `@monocloud/auth-nextjs`                   | Server (RSC, route handlers, middleware/proxy, Pages API, `getServerSideProps`) | `authMiddleware`, `monoCloudAuth`, `getSession`, `getTokens`, `isAuthenticated`, `isUserInGroup`, `protect`, `protectApi`, `protectPage`, `redirectToSignIn`, `redirectToSignOut`, `MonoCloudNextClient`, types/errors |
| `@monocloud/auth-nextjs/client`            | Client Components (`"use client"`)                                              | `useAuth`, `protectClientPage`                                                                                                                                                                                         |
| `@monocloud/auth-nextjs/components`        | Server OR Client Components                                                     | `<SignIn>`, `<SignUp>`, `<SignOut>` (render as `<a>`)                                                                                                                                                                  |
| `@monocloud/auth-nextjs/components/client` | Client Components only                                                          | `<RedirectToSignIn>`, `<Protected>`                                                                                                                                                                                    |

## Environment variables

Required (read automatically from `process.env`):

| Variable                       | Purpose                                                                        |
| ------------------------------ | ------------------------------------------------------------------------------ |
| `MONOCLOUD_AUTH_TENANT_DOMAIN` | Your MonoCloud tenant URL, e.g. `https://acme.eu.monocloud.com`                |
| `MONOCLOUD_AUTH_CLIENT_ID`     | OIDC client id                                                                 |
| `MONOCLOUD_AUTH_CLIENT_SECRET` | OIDC client secret                                                             |
| `MONOCLOUD_AUTH_APP_URL`       | Public origin of the app, e.g. `http://localhost:3000`                         |
| `MONOCLOUD_AUTH_COOKIE_SECRET` | 32-byte hex string for cookie encryption. Generate with `openssl rand -hex 32` |

Optional:

| Variable                       | Default                | Purpose                            |
| ------------------------------ | ---------------------- | ---------------------------------- |
| `MONOCLOUD_AUTH_SCOPES`        | `openid profile email` | Default scopes                     |
| `MONOCLOUD_AUTH_RESOURCE`      | —                      | Default resource for access tokens |
| `MONOCLOUD_AUTH_GROUPS_CLAIM`  | `groups`               | Claim name used by group checks    |
| `MONOCLOUD_AUTH_CALLBACK_URL`  | `/api/auth/callback`   | Customize auth routes              |
| `MONOCLOUD_AUTH_SIGNIN_URL`    | `/api/auth/signin`     |                                    |
| `MONOCLOUD_AUTH_SIGNOUT_URL`   | `/api/auth/signout`    |                                    |
| `MONOCLOUD_AUTH_USER_INFO_URL` | `/api/auth/userinfo`   |                                    |

If you override a route (e.g. `MONOCLOUD_AUTH_SIGNIN_URL`), also set the matching `NEXT_PUBLIC_MONOCLOUD_AUTH_SIGNIN_URL` so client-side helpers (`useAuth`, `<SignIn>`, `<SignOut>`, etc.) discover it, AND update the redirect URI in the MonoCloud dashboard.

## Programmatic client options

The package-level helpers (`authMiddleware`, `getSession`, `protectPage`, etc.) use a singleton configured from `MONOCLOUD_AUTH_*` env vars. For constructor-only options, create and share a `MonoCloudNextClient` instance instead.

`MonoCloudNextClient(options?: MonoCloudOptions)` accepts the node-core `MonoCloudOptions` shape. Notable nested session options:

```ts
interface MonoCloudSessionOptions {
  cookie?: Partial<MonoCloudCookieOptions>;
  sliding?: boolean;
  duration?: number;
  maximumDuration?: number;
  store?: MonoCloudSessionStore;
}

interface MonoCloudSessionStore {
  get(key: string): Promise<MonoCloudSession | undefined | null>;
  set(
    key: string,
    data: MonoCloudSession,
    lifetime: SessionLifetime,
  ): Promise<void>;
  delete(key: string): Promise<void>;
}
```

Use `session.store` for Redis/database-backed sessions. There is no env var for a custom store; pass it in code:

```ts
import { MonoCloudNextClient } from "@monocloud/auth-nextjs";

export const monoCloud = new MonoCloudNextClient({
  session: {
    store: redisSessionStore,
  },
});
```

Then use that shared client wherever the SDK helper is needed, for example `monoCloud.authMiddleware()` in `proxy.ts`/`middleware.ts` and `monoCloud.getSession()` in server code.

## Wiring the middleware/proxy

The middleware/proxy handles auth routes (`/api/auth/signin`, `/callback`, `/userinfo`, `/signout`) internally **and** enforces route protection. You do not need a `[...monocloud]` catch-all when using the middleware.

**File location depends on Next.js version:**

- Next.js **16+**: `src/proxy.ts` (or `proxy.ts` at the root, mirroring your `app/`/`pages/` layout)
- Next.js **13–15**: `src/middleware.ts` (or `middleware.ts`)

The export and body are the same; only the filename differs.

```ts
// src/proxy.ts (Next 16+) or src/middleware.ts (Next 13–15)
import { authMiddleware } from "@monocloud/auth-nextjs";

export default authMiddleware();

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)",
  ],
};
```

By default, **every route matched by `config.matcher` requires authentication**. To protect only specific routes:

```ts
export default authMiddleware({
  protectedRoutes: ["/dashboard", /^\/api\/admin(\/.*)?$/],
});
```

To protect nothing (auth routes still handled, but the rest is public):

```ts
export default authMiddleware({ protectedRoutes: [] });
```

Dynamic predicate (full custom logic):

```ts
export default authMiddleware({
  protectedRoutes: (req) => req.nextUrl.pathname.startsWith("/api/protected"),
});
```

Group-based protection in the middleware:

```ts
export default authMiddleware({
  protectedRoutes: [
    {
      groups: ["admin", "editor"],
      routes: ["/internal", /^\/api\/internal(\/.*)?$/],
    },
  ],
});
```

## Reading the session — server

`getSession()` is exported from the package root and works in Server Components, Server Actions, App Router Route Handlers, middleware/proxy, Pages API routes, and `getServerSideProps`. Returns `MonoCloudSession | undefined`.

```tsx
// app/page.tsx (Server Component — no args needed)
import { getSession } from "@monocloud/auth-nextjs";

export default async function Page() {
  const session = await getSession();
  if (!session) return <p>Not signed in</p>;
  return <p>Hello {session.user.name}</p>;
}
```

```ts
// app/api/me/route.ts (App Router Route Handler)
import { getSession } from "@monocloud/auth-nextjs";
import { NextResponse } from "next/server";

export const GET = async () => {
  const session = await getSession();
  return NextResponse.json(session?.user ?? null);
};
```

```ts
// pages/api/me.ts (Pages Router — pass req, res)
import { getSession } from "@monocloud/auth-nextjs";
import type { NextApiRequest, NextApiResponse } from "next";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  const session = await getSession(req, res);
  res.json(session?.user ?? null);
}
```

```ts
// pages/index.tsx (getServerSideProps — pass ctx.req, ctx.res)
export const getServerSideProps: GetServerSideProps = async (ctx) => {
  const session = await getSession(ctx.req, ctx.res);
  return { props: { session: session ?? null } };
};
```

## Reading the user — client

`useAuth()` reads the user from `/api/auth/userinfo` via SWR. **No provider/wrapper is required** — just call the hook inside a Client Component.

```tsx
"use client";
import { useAuth } from "@monocloud/auth-nextjs/client";

export default function Profile() {
  const { user, isLoading, isAuthenticated, error, refetch } = useAuth();
  if (isLoading) return null;
  if (!isAuthenticated) return <p>Sign in to view your profile</p>;
  return (
    <>
      <pre>{JSON.stringify(user, null, 2)}</pre>
      <button onClick={() => refetch(true)}>Refresh</button>
    </>
  );
}
```

`refetch(true)` re-fetches and asks the server to refresh from the OP's userinfo endpoint; `refetch()` just re-fetches the cached endpoint.

## Sign-in, sign-up, sign-out

`<SignIn>`, `<SignUp>`, and `<SignOut>` render an `<a>` tag pointing at the configured auth routes. They work in Server **or** Client Components. Pass any extra anchor props through (className, etc.).

```tsx
import { SignIn, SignUp, SignOut } from '@monocloud/auth-nextjs/components';

// Sign in / sign up
<SignIn>Sign In</SignIn>
<SignIn returnUrl="/dashboard" loginHint="user@example.com">Sign In</SignIn>
<SignUp returnUrl="/welcome">Sign Up</SignUp>

// Sign out
<SignOut>Sign Out</SignOut>
<SignOut federated postLogoutUrl="/goodbye">Sign Out</SignOut>
```

For programmatic redirects on the server (RSC, server actions, route handlers), use `redirectToSignIn()` / `redirectToSignOut()` from the root package. They throw a Next.js redirect and never resolve.

```ts
"use server";
import { redirectToSignIn } from "@monocloud/auth-nextjs";

export async function startLogin() {
  await redirectToSignIn({ returnUrl: "/dashboard" });
}
```

On the client, render `<RedirectToSignIn />` (from `/components/client`) to redirect once mounted.

## Protecting routes — at a glance

| What you're protecting                                        | Helper                                     | Where it lives               |
| ------------------------------------------------------------- | ------------------------------------------ | ---------------------------- |
| Whole groups of routes (broadest)                             | `authMiddleware({ protectedRoutes })`      | `proxy.ts` / `middleware.ts` |
| App Router Server Component page                              | `protectPage(Component, options?)`         | the page file                |
| Pages Router `getServerSideProps`                             | `protectPage(options?)` (no component arg) | the page file                |
| App Router Route Handler                                      | `protectApi(handler, options?)`            | `app/api/*/route.ts`         |
| Pages Router API route                                        | `protectApi(handler, options?)`            | `pages/api/*.ts`             |
| Server Component / Server Action / Route Handler — imperative | `await protect()` (App Router only)        | inline                       |
| Client Component page (rendering only)                        | `protectClientPage(Component, options?)`   | the page file                |
| Conditional UI in client component                            | `<Protected fallback={...}>`               | inside JSX                   |

Quick examples:

```tsx
// App Router page
import { protectPage } from "@monocloud/auth-nextjs";
export default protectPage(function Dashboard({ user }) {
  return <p>Hi {user.email}</p>;
});

// App Router page, admins only
export default protectPage(
  function AdminPanel({ user }) {
    return <p>Hi {user.email}</p>;
  },
  { groups: ["admin"], returnUrl: "/admin" },
);
```

```ts
// App Router API
import { protectApi } from "@monocloud/auth-nextjs";
import { NextResponse } from "next/server";
export const GET = protectApi(async () => NextResponse.json({ ok: true }));
```

```tsx
// Pages Router page
import { protectPage } from "@monocloud/auth-nextjs";
export default function Page({ user }) {
  return <p>Hi {user.email}</p>;
}
export const getServerSideProps = protectPage();
```

```tsx
// Imperative (App Router only — Server Component / Server Action / Route Handler)
import { protect } from "@monocloud/auth-nextjs";
export default async function SecretPage() {
  await protect(); // redirects to sign-in if not authenticated
  await protect({ groups: ["admin"] }); // also enforces group membership
  return <p>Top secret</p>;
}
```

```tsx
// Client page
"use client";
import { protectClientPage } from "@monocloud/auth-nextjs/client";
export default protectClientPage(function Page({ user }) {
  return <p>Hi {user.email}</p>;
});
```

```tsx
// Conditional rendering inside a client component
"use client";
import { Protected } from "@monocloud/auth-nextjs/components/client";
<Protected fallback={<p>Sign in to view</p>} groups={["admin"]}>
  <AdminPanel />
</Protected>;
```

For full option lists (custom `onAccessDenied`, `onGroupAccessDenied`, `authParams`, etc.), see `references/protecting.md`.

## Access tokens

`getTokens()` returns the current token set and refreshes the default access token if needed. Throws `MonoCloudValidationError` if there is no session. Same calling conventions as `getSession()` (no args in App Router server context; pass `req`/`res` in Pages Router).

```ts
import { getTokens } from "@monocloud/auth-nextjs";

const { accessToken, idToken, refreshToken, isExpired } = await getTokens();

// Force a refresh:
await getTokens({ forceRefresh: true });

// Request a token for a specific resource / scopes (must have been consented):
await getTokens({
  resource: "https://api.example.com",
  scopes: "read:things write:things",
});
```

## Alternative: catch-all route (only when middleware can't be used)

The middleware handles auth routes for you. If you cannot use middleware (rare — e.g. infrastructure constraints), mount `monoCloudAuth()` on a catch-all instead:

```ts
// App Router
// src/app/api/auth/[...monocloud]/route.ts
import { monoCloudAuth } from "@monocloud/auth-nextjs";
export const GET = monoCloudAuth();
```

```ts
// Pages Router
// src/pages/api/auth/[...monocloud].ts
import { monoCloudAuth } from "@monocloud/auth-nextjs";
export default monoCloudAuth();
```

Do not do this **in addition** to `authMiddleware()` — pick one. The default and recommended path is `authMiddleware()`.

## Common pitfalls

1. **Wrong filename for the version.** `proxy.ts` only works on Next 16+. On Next 13–15 the file must be named `middleware.ts`. Check `next` in `package.json` before suggesting a filename.
2. **Adding `[...monocloud]/route.ts` while middleware is in place.** Double-mounted auth routes lead to weird redirect loops. Use middleware OR `monoCloudAuth()` — not both.
3. **`useAuth()` returning no user after sign-in.** Usually means the matcher excludes `/api/auth/userinfo`, or the middleware isn't matching the userinfo path. Make sure `config.matcher` covers it (the recommended matcher above does).
4. **Calling `protect()` / `redirectToSignIn()` / `redirectToSignOut()` outside the App Router.** They throw with a clear message — these helpers are App-Router-only (RSC, server actions, route handlers). For the Pages Router, use `protectPage()` / `protectApi()` or call `getSession(req, res)` and respond yourself.
5. **`protectApi()` returning 401/403 without a sign-in redirect.** That's by design — API routes return JSON, not redirects. If you want a redirect, do it from a page or middleware.
6. **Putting `<Protected>` or `useAuth()` in a Server Component.** Both require `"use client"`. Use `getSession()` for server-side conditional rendering.
7. **Forgetting `NEXT_PUBLIC_*` mirror when overriding auth routes.** Client helpers won't find the new URL otherwise.
8. **Mutating cookies after `getSession()` in middleware.** Pass the response object to `getSession(req, res)` (and return that response) so cookie refreshes are preserved.

## Onboarding checklist for a fresh integration

1. `npm install @monocloud/auth-nextjs` (or pnpm/yarn).
2. Add the five required env vars to `.env.local`. Generate `MONOCLOUD_AUTH_COOKIE_SECRET` with `openssl rand -hex 32`.
3. In the MonoCloud dashboard, add `http://localhost:3000/api/auth/callback` to allowed redirect URIs and `http://localhost:3000` to allowed post-logout URIs.
4. Create `src/proxy.ts` (Next 16+) **or** `src/middleware.ts` (Next ≤15) with `export default authMiddleware()` and the recommended `config.matcher`.
5. Add a header with `<SignIn>` / `<SignOut>` (and optionally `<SignUp>`) so users can authenticate.
6. Use `getSession()` for server-side reads, `useAuth()` for client-side reads. Add `protectPage`/`protectApi` only on routes that need stricter enforcement than the middleware.
7. For protected fetches that need an access token, call `getTokens()` and forward `accessToken` in the `Authorization` header.

## Deeper reference

- `references/api-surface.md` — every export by subpath, with signatures.
- `references/protecting.md` — full option shapes for `protect`, `protectApi`, `protectPage`, `protectClientPage`, and the `<Protected>` component.
- `references/troubleshooting.md` — extended symptom → cause → fix index covering the items in "Common pitfalls" above, plus less frequent issues (cookie refresh in middleware, route-override + `NEXT_PUBLIC_*` mirror, training-data SDK ghosts).
