---
name: monocloud-auth-fastify
description: Use when integrating MonoCloud access-token validation into a Fastify API — installing or configuring `@monocloud/backend-node/fastify`, wiring the `protectApi()` `onRequest` hook factory, validating JWT or opaque (introspection) bearer tokens, enforcing scopes/groups, attaching `claims` to `request` via `AuthenticatedFastifyRequest`, or troubleshooting `MONOCLOUD_BACKEND_*` env vars / audience / JWKS / mTLS certificate binding.
license: MIT
---

# MonoCloud Fastify API protection (`@monocloud/backend-node/fastify`)

Backend SDK for validating MonoCloud-issued access tokens in Fastify APIs. Same engine as the Express adapter — handles JWT signature verification (via JWKS) and opaque-token introspection automatically based on token format.

## Package identity — read this first

**Use:** `@monocloud/backend-node` with the `/fastify` subpath. This is a single npm package that also ships `/express`.

This is **not** the same SDK as `@monocloud/auth-nextjs` (frontend, user sessions) or `@monocloud/auth-node-core` (server-side auth flows). This package is purely for **API protection** — validating tokens issued elsewhere, not signing users in.

If you see these symbols, they belong to a different package or an older SDK — do not use them here:

- `@fastify/jwt`, `fastify-jwt`, `fastify-auth` (other libraries)
- `fastify.register(monoCloudAuth)` style plugin registration (this SDK exposes a per-route `onRequest` hook, not a Fastify plugin)
- Importing from `@monocloud/backend-node` root for Fastify hooks (use the `/fastify` subpath)

## Installation

```bash
npm install @monocloud/backend-node
```

## Environment variables

Required:

| Variable                          | Purpose                                                    |
| --------------------------------- | ---------------------------------------------------------- |
| `MONOCLOUD_BACKEND_TENANT_DOMAIN` | MonoCloud tenant URL, e.g. `https://acme.us.monocloud.com` |
| `MONOCLOUD_BACKEND_AUDIENCE`      | Expected audience claim, e.g. `https://api.example.com`    |

Required only when validating **opaque tokens** (or when `MONOCLOUD_BACKEND_INTROSPECT_JWT_TOKENS=true`):

| Variable                               | Purpose                                                                                                                                                |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `MONOCLOUD_BACKEND_CLIENT_ID`          | Client used to call the introspection endpoint                                                                                                         |
| `MONOCLOUD_BACKEND_CLIENT_SECRET`      | Client secret                                                                                                                                          |
| `MONOCLOUD_BACKEND_CLIENT_AUTH_METHOD` | One of `client_secret_basic`, `client_secret_post` (default), `client_secret_jwt`, `private_key_jwt`, `tls_client_auth`, `self_signed_tls_client_auth` |

Optional tuning:

| Variable                                    | Default | Purpose                                                    |
| ------------------------------------------- | ------- | ---------------------------------------------------------- |
| `MONOCLOUD_BACKEND_INTROSPECT_JWT_TOKENS`   | `false` | If `true`, skip local JWT validation and always introspect |
| `MONOCLOUD_BACKEND_CLOCK_SKEW`              | `0`     | Allowed clock drift (seconds)                              |
| `MONOCLOUD_BACKEND_CLOCK_TOLERANCE`         | `300`   | Extra tolerance on time-based claims                       |
| `MONOCLOUD_BACKEND_GROUPS_CLAIM`            | —       | Claim name that carries group memberships                  |
| `MONOCLOUD_BACKEND_GROUPS_MATCH_ALL`        | `false` | If `true`, all listed groups must match                    |
| `MONOCLOUD_BACKEND_JWKS_CACHE_DURATION`     | —       | Seconds to cache the JWKS                                  |
| `MONOCLOUD_BACKEND_METADATA_CACHE_DURATION` | —       | Seconds to cache the OIDC discovery doc                    |

## Basic wiring

```ts
import Fastify from "fastify";
import {
  protectApi,
  type AuthenticatedFastifyRequest,
} from "@monocloud/backend-node/fastify";

const fastify = Fastify();

// Reads MONOCLOUD_BACKEND_* env vars. Build it once and reuse.
const protect = protectApi();

// Bare protection — any valid token works
fastify.get("/api/me", { onRequest: protect() }, async (request) => {
  const { claims } = request as AuthenticatedFastifyRequest;
  return { sub: claims.sub };
});

// Scope-gated
fastify.post(
  "/api/posts",
  { onRequest: protect({ scopes: ["posts:write"] }) },
  async (request, reply) => {
    reply.code(201);
  },
);

// Group-gated
fastify.delete(
  "/api/posts/:id",
  { onRequest: protect({ groups: ["admin"] }) },
  async (request, reply) => {
    reply.code(204);
  },
);

await fastify.listen({ port: 3000 });
```

Two-call pattern: `protectApi()` builds a **factory** once (parses env, loads JWKS lazily); calling the factory with options returns an `onRequest` hook. Build the factory at startup, attach the hook per-route.

## What `protect(options)` accepts

`options` (all optional):

```ts
interface ProtectOptions {
  scopes?: string[]; // require all listed scopes
  groups?: string[]; // require group membership (any-of by default)
  validateCertificateBinding?: boolean; // mTLS-bound token validation
}
```

- **scopes**: AND semantics — the token must carry every listed scope.
- **groups**: OR by default; flip with `MONOCLOUD_BACKEND_GROUPS_MATCH_ALL=true` (or per-client `groupOptions.matchAll`). Claim name comes from `MONOCLOUD_BACKEND_GROUPS_CLAIM`.
- **validateCertificateBinding**: enforces the `cnf.x5t#S256` confirmation claim against the client's TLS cert. Requires a `certificateResolver` (see "Advanced" below).

## Client constructor options

`new MonoCloudBackendNodeClient(options)` accepts the backend-node option shape. Use this when you need a shared client, non-env configuration, or a custom token-claims cache:

```ts
interface MonoCloudBackendNodeClientOptions {
  tenantDomain: string;
  audience: string;
  clientId?: string;
  clientSecret?: string;
  clientAuthMethod?: ClientAuthMethod;
  groupOptions?: { groupsClaim?: string; matchAll?: boolean };
  clockSkew?: number;
  clockTolerance?: number;
  jwksCacheDuration?: number;
  metadataCacheDuration?: number;
  introspectJwtTokens?: boolean;
  cache?: ICache;
  fetcher?: (input: RequestInfo, init?: RequestInit) => Promise<Response>;
}
```

`cache?: ICache` is constructor-only; pass it in code to cache validated access-token claims by raw token until the token expires.

## Default responses

- No `Authorization: Bearer <token>` header (and no custom `tokenResolver`): `401 { "message": "unauthorized" }`
- Token validation fails (signature, audience, issuer, expiry, mismatched cnf, etc.): `401 { "message": "unauthorized" }`
- Token valid but missing required scopes or groups: `403 { "message": "forbidden" }`

The hook calls `reply.status(...).send(...)` directly on failure — `done()` is not invoked. Customise responses by wrapping the hook or by calling `MonoCloudBackendNodeClient.validateAccessToken()` from your own `onRequest`.

## Reading the validated claims

After the hook runs, `request.claims` is populated. Cast the request:

```ts
import type { AuthenticatedFastifyRequest } from "@monocloud/backend-node/fastify";

fastify.get("/api/me", { onRequest: protect() }, async (request) => {
  const { claims } = request as AuthenticatedFastifyRequest;
  return claims;
});
```

Alternatively, declare a module augmentation to avoid casting:

```ts
import type { AccessTokenClaims } from "@monocloud/backend-node";
declare module "fastify" {
  interface FastifyRequest {
    claims?: AccessTokenClaims;
  }
}
```

## Applying to many routes — patterns

```ts
// Apply to every route on the instance
fastify.addHook("onRequest", protect());

// Per-encapsulated-context (Fastify plugins / prefixes)
fastify.register(async (instance) => {
  instance.addHook("onRequest", protect({ scopes: ["admin"] }));
  instance.get("/admin/users", async () => {
    /* ... */
  });
});

// Different options on different routes — just attach inline as in the basic example
```

`fastify.addHook` applies to every subsequent route in that encapsulation context, so registering it inside a plugin scopes it to that plugin's routes.

## Advanced: shared client, custom resolvers, caching

```ts
import {
  protectApi,
  MonoCloudBackendNodeClient,
  type ICache,
} from "@monocloud/backend-node/fastify";

const client = new MonoCloudBackendNodeClient({
  tenantDomain: "https://acme.us.monocloud.com",
  audience: "https://api.example.com",
  cache: redisCache, // your ICache implementation — caches by token until exp
  introspectJwtTokens: false,
});

const protect = protectApi(client, {
  // Pull token from somewhere other than Authorization: Bearer
  tokenResolver: async (req) =>
    (req.cookies as Record<string, string>).access_token,
  // Provide the client cert for mTLS-bound tokens (use with validateCertificateBinding)
  certificateResolver: async (req) =>
    req.headers["x-client-cert"] as string | undefined,
});

fastify.get(
  "/api/secure",
  { onRequest: protect({ validateCertificateBinding: true }) },
  async (request) => (request as AuthenticatedFastifyRequest).claims,
);
```

`ICache` interface (implement for Redis, in-memory, etc.):

```ts
interface ICache {
  get(token: string): Promise<AccessTokenClaims | null | undefined>;
  set(
    token: string,
    claims: AccessTokenClaims,
    expiresAt: number,
  ): Promise<void>;
  delete(token: string): Promise<void>;
}
```

Caching is keyed on the raw token string and respects `claims.exp` minus the configured clock skew/tolerance — short-lived tokens self-expire.

## JWT vs. introspection — how the SDK decides

- Three dot-separated parts (`xxx.yyy.zzz`) **and** `introspectJwtTokens` is false (default): the SDK validates the JWT locally using JWKS fetched from the tenant. After JWKS warms, no network call per request.
- Otherwise (opaque tokens, or `introspectJwtTokens=true`): the SDK calls the OIDC introspection endpoint. Requires `clientId` + `clientSecret` (or another `clientAuthMethod`).

**JWT tokens don't require client credentials.** Opaque tokens do. `MonoCloudValidationError: clientId is required` on an opaque-token request means you need to add the introspection env vars.

## Common pitfalls

1. **Wrong import path.** Import from `@monocloud/backend-node/fastify`, not the root. The root only exports the framework-agnostic `MonoCloudBackendNodeClient`.
2. **Attaching `protect` instead of `protect()` to `onRequest`.** The factory returns a function — you must call it to get the hook. `{ onRequest: protect }` is wrong; `{ onRequest: protect() }` is right.
3. **Audience mismatch.** `MONOCLOUD_BACKEND_AUDIENCE` must exactly match the `aud` claim. Trailing slashes and http/https differences fail validation.
4. **Building the factory per request.** `protectApi()` is a startup-time call — invoking it inside a handler creates a new client per request.
5. **Calling `done()` or `reply.send()` after the hook failed.** The hook sends its own 401/403 — if you wrap it, check `reply.sent` first.
6. **Cookies but no `@fastify/cookie`.** If you use a `tokenResolver` that reads cookies, register `@fastify/cookie` first or `request.cookies` is undefined.
7. **Group claim missing.** If `groups` is set but the token doesn't carry the configured `groupsClaim`, requests are forbidden. Configure it in the MonoCloud dashboard or via the env var.

## Onboarding checklist

1. `npm install @monocloud/backend-node`.
2. Add `MONOCLOUD_BACKEND_TENANT_DOMAIN` and `MONOCLOUD_BACKEND_AUDIENCE` to your env. For opaque tokens, also `MONOCLOUD_BACKEND_CLIENT_ID` + `_CLIENT_SECRET`.
3. Register an **API** (audience) in the MonoCloud dashboard matching `MONOCLOUD_BACKEND_AUDIENCE`.
4. Build the factory once: `const protect = protectApi();`
5. Attach per-route: `fastify.get(path, { onRequest: protect({ scopes: [...] }) }, handler);`
6. Cast `request` to `AuthenticatedFastifyRequest` inside handlers to read `claims`.

## Related types and errors

Re-exported from `@monocloud/auth-core` via `@monocloud/backend-node`:

- `AccessTokenClaims`, `JwtClaims`, `Jwk`, `Jwks`, `IssuerMetadata`, `ClientAuthMethod`
- `MonoCloudAuthBaseError`, `MonoCloudValidationError`, `MonoCloudOPError`, `MonoCloudHttpError`, `MonoCloudTokenError`

A failed scope/group check throws `MonoCloudTokenError` with the message `'Token is missing required scopes'` or `'Token is missing required groups'` — the hook converts these to 403. Other validation failures throw `MonoCloudTokenError` / `MonoCloudValidationError` and become 401.

## Deeper reference

- `references/api-surface.md` — every export from `@monocloud/backend-node/fastify`, full type signatures, env-var → option mapping, defaults.
- `references/troubleshooting.md` — symptom → cause → fix index for the most common failure modes (audience mismatch, opaque-token introspection, scope/group claims, mTLS binding, `onRequest` vs plugin confusion, JWKS thrash).
