---
name: monocloud-auth-express
description: Use when integrating MonoCloud access-token validation into an Express API — installing or configuring `@monocloud/backend-node/express`, wiring the `protectApi()` middleware factory, validating JWT or opaque (introspection) bearer tokens, enforcing scopes/groups, attaching `claims` to `req` via `AuthenticatedExpressRequest`, or troubleshooting `MONOCLOUD_BACKEND_*` env vars / audience / JWKS / mTLS certificate binding.
license: MIT
---

# MonoCloud Express API protection (`@monocloud/backend-node/express`)

Backend SDK for validating MonoCloud-issued access tokens in Express APIs. Handles JWT signature verification (via JWKS) and opaque-token introspection automatically based on token format.

## Package identity — read this first

**Use:** `@monocloud/backend-node` with the `/express` subpath. This is a single npm package that also ships `/fastify`.

This is **not** the same SDK as `@monocloud/auth-nextjs` (frontend, user sessions) or `@monocloud/auth-node-core` (server-side auth flows). This package is purely for **API protection** — validating tokens issued elsewhere, not signing users in.

If you see any of these symbols, they belong to a different package or an older SDK — do not use them here:

- `expressJwt`, `expressOAuth2BearerToken`, `passport-*` (other libraries)
- `requireAuth`, `requireScopes` as standalone functions (this SDK uses one chained call)
- Importing from `@monocloud/backend-node` root for Express middleware (use the `/express` subpath)

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
import express from "express";
import {
  protectApi,
  type AuthenticatedExpressRequest,
} from "@monocloud/backend-node/express";

const app = express();

// Reads MONOCLOUD_BACKEND_* env vars. Build it once and reuse.
const protect = protectApi();

// Bare protection — any valid token works
app.get("/api/me", protect(), (req, res) => {
  const { claims } = req as AuthenticatedExpressRequest;
  res.json({ sub: claims.sub });
});

// Scope-gated
app.post("/api/posts", protect({ scopes: ["posts:write"] }), (req, res) => {
  res.status(201).end();
});

// Group-gated (uses MONOCLOUD_BACKEND_GROUPS_CLAIM or override per call)
app.delete("/api/posts/:id", protect({ groups: ["admin"] }), (req, res) => {
  res.status(204).end();
});

app.listen(3000);
```

Two-call pattern: `protectApi()` builds a **factory** once (parses env, loads JWKS lazily); calling the factory with options returns the actual middleware. Build the factory outside the request hook, call the factory inline per route.

## What `protect(options)` accepts

`options` (all optional):

```ts
interface ProtectOptions {
  scopes?: string[]; // require all listed scopes
  groups?: string[]; // require group membership (any-of by default)
  validateCertificateBinding?: boolean; // mTLS-bound token validation
}
```

- **scopes**: AND semantics — the token must carry every listed scope (string match against the `scope` claim).
- **groups**: OR by default; flip with `MONOCLOUD_BACKEND_GROUPS_MATCH_ALL=true` (or per-client `groupOptions.matchAll`). The claim name comes from `MONOCLOUD_BACKEND_GROUPS_CLAIM`.
- **validateCertificateBinding**: enforces the `cnf.x5t#S256` confirmation claim against the client's TLS cert. Requires a `certificateResolver` to be wired (see "Advanced" below).

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
- Token is valid but missing required scopes or groups: `403 { "message": "forbidden" }`

The middleware does not call `next(err)` — it sends the response directly. If you want custom error responses, wrap the middleware or implement your own using `MonoCloudBackendNodeClient.validateAccessToken()`.

## Reading the validated claims

After `protect()` runs successfully, `req.claims` is populated with `AccessTokenClaims`. Cast the request:

```ts
import type { AuthenticatedExpressRequest } from "@monocloud/backend-node/express";

app.get("/api/me", protect(), (req, res) => {
  const { claims } = req as AuthenticatedExpressRequest;
  // claims.sub, claims.scope, claims.exp, claims.iat, etc.
  res.json(claims);
});
```

Alternatively, declare a global Express namespace augmentation if you don't want to cast per-route:

```ts
import type { AccessTokenClaims } from "@monocloud/backend-node";
declare global {
  namespace Express {
    interface Request {
      claims?: AccessTokenClaims;
    }
  }
}
```

## Advanced: shared client, custom resolvers, caching

```ts
import {
  protectApi,
  MonoCloudBackendNodeClient,
  type ICache,
} from "@monocloud/backend-node/express";

// Build a client explicitly when you need a cache or non-env config
const client = new MonoCloudBackendNodeClient({
  tenantDomain: "https://acme.us.monocloud.com",
  audience: "https://api.example.com",
  cache: redisCache, // your ICache implementation — caches by token until exp
  introspectJwtTokens: false,
});

const protect = protectApi(client, {
  // Pull token from somewhere other than Authorization: Bearer
  tokenResolver: async (req) => req.cookies.access_token,
  // Provide the client cert for mTLS-bound tokens (use with validateCertificateBinding)
  certificateResolver: async (req) => req.headers["x-client-cert"] as string,
});

app.get(
  "/api/secure",
  protect({ validateCertificateBinding: true }),
  (req, res) => {
    res.json((req as AuthenticatedExpressRequest).claims);
  },
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

- If the token has three dot-separated parts (`xxx.yyy.zzz`) **and** `introspectJwtTokens` is false (default): the SDK validates the JWT locally using JWKS fetched from the tenant. No network call per request after the JWKS cache warms.
- Otherwise (opaque tokens, or `introspectJwtTokens=true`): the SDK calls the OIDC introspection endpoint. Requires `clientId` + `clientSecret` (or another `clientAuthMethod`).

This means: **JWT tokens don't require client credentials.** Opaque tokens do. If you see `MonoCloudValidationError: clientId is required` when receiving opaque tokens, set the introspection env vars.

## Common pitfalls

1. **Wrong import path.** `protectApi` must be imported from `@monocloud/backend-node/express`, not the root. The root only exports the framework-agnostic `MonoCloudBackendNodeClient` class.
2. **Audience mismatch.** `MONOCLOUD_BACKEND_AUDIENCE` must exactly match the `aud` claim minted by your authorization server for this API. A trailing slash or http vs https difference will fail validation.
3. **Building the factory per request.** `protectApi()` is meant to be called **once** at startup. Calling it inside a route handler creates a new client per request and re-fetches the JWKS each time.
4. **Forgetting to install body-parser before protect.** `protect()` doesn't read the body, but if your route does, register body parsers normally. Order doesn't matter for the auth middleware.
5. **Calling `next()` after the auth middleware sent a 401/403.** The middleware sends the response synchronously on failure and doesn't call `next`. If you wrap it, check `res.headersSent`.
6. **Group claim missing.** If `groups` is set but the token doesn't carry the claim named by `MONOCLOUD_BACKEND_GROUPS_CLAIM` (or the default), the request is forbidden. Configure the claim in the MonoCloud dashboard or set `groupsClaim` explicitly.
7. **Local JWT validation suddenly hitting the network.** If you set `MONOCLOUD_BACKEND_INTROSPECT_JWT_TOKENS=true`, every JWT request also calls introspection. Usually unwanted; only enable if you specifically need server-side revocation checks.

## Onboarding checklist

1. `npm install @monocloud/backend-node`.
2. Add `MONOCLOUD_BACKEND_TENANT_DOMAIN` and `MONOCLOUD_BACKEND_AUDIENCE` to your env. If you'll accept opaque tokens, also add `MONOCLOUD_BACKEND_CLIENT_ID` and `MONOCLOUD_BACKEND_CLIENT_SECRET`.
3. Register an **API** (audience) in the MonoCloud dashboard matching `MONOCLOUD_BACKEND_AUDIENCE`.
4. Build the factory once: `const protect = protectApi();`
5. Apply per-route: `app.get('/path', protect({ scopes: [...] }), handler);`
6. Cast `req` to `AuthenticatedExpressRequest` inside handlers to read `claims`.

## Related types and errors

Re-exported from `@monocloud/auth-core` via `@monocloud/backend-node`:

- `AccessTokenClaims`, `JwtClaims`, `Jwk`, `Jwks`, `IssuerMetadata`, `ClientAuthMethod`
- `MonoCloudAuthBaseError`, `MonoCloudValidationError`, `MonoCloudOPError`, `MonoCloudHttpError`, `MonoCloudTokenError`

A failed scope/group check throws `MonoCloudTokenError` with the message `'Token is missing required scopes'` or `'Token is missing required groups'` — these get converted to 403 by the middleware. Other validation failures throw `MonoCloudTokenError` or `MonoCloudValidationError` and become 401.

## Deeper reference

- `references/api-surface.md` — every export from `@monocloud/backend-node/express`, full type signatures, env-var → option mapping, defaults.
- `references/troubleshooting.md` — symptom → cause → fix index for the most common failure modes (audience mismatch, opaque-token introspection config, scope/group enforcement quirks, mTLS binding errors, JWKS thrash).
