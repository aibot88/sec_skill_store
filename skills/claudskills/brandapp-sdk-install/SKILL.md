---
name: brandapp-sdk-install
description: Install @reopt-ai/brandapp-sdk in a consumer project. Sets up auth, OAuth client, EAV, API routes, and env config. Triggers on "brandapp-sdk install", "brandapp-sdk init", "brandapp sdk setup", "brandapp sdk bootstrap", "apply SDK", "brandapp integration".
target: "@reopt-ai/brandapp-sdk"
targetMinVersion: "1.6.0"
---

# Brandapp SDK Install

Skill for generating the files and configuration required to adopt
`@reopt-ai/brandapp-sdk` in a consumer project for the first time.

---

## Prerequisites

- Next.js project (App Router)
- `better-auth` installed (required when using Auth)
- A Brandapp created in a Reopt workspace, with OAuth Client ID/Secret issued

---

## Step 0: Optional dev-environment bootstrap (`reopt brandapp init`)

`reopt brandapp init` is a **dev-mode** scaffold, not a full SDK install.
Run it when you also want the offline in-memory dev server.

```bash
npx @reopt-ai/cli brandapp init
# or
pnpm dlx @reopt-ai/cli brandapp init
```

Files it touches:

- `.env.development` (always) — dev-mode env (`REOPT_DEV_MODE=true`,
  Better Auth placeholders).
- `reopt.seed.ts` (always) — seed-data template, applied automatically
  on dev-server start.
- `lib/dev-server.ts` (Next.js projects only) — `startDevServer()` hook
  that spins up `@reopt-ai/brandapp-sdk/dev`.
- `instrumentation.ts` (Next.js projects only) — calls `startDevServer()`
  on server boot when `REOPT_DEV_MODE=true`.
- `package.json` (Next.js projects only) — adds the `dev:local` script
  (`REOPT_DEV_MODE=true next dev`).
- `.gitignore` — appends `.reopt/` so the persisted dev data stays
  local.

Non-Next projects skip `instrumentation.ts`, `lib/dev-server.ts`, and
the `dev:local` script — wire `startDevServer()` from
`@reopt-ai/brandapp-sdk/dev` into your own bootstrap if you need dev
mode. The CLI is non-destructive without `--force`.

`init` does **not** create `.npmrc`, `.env.local`, `lib/sdk.ts`,
`lib/auth.ts`, `lib/auth-client.ts`, the auth route handler, or any
webhook route. The remaining steps in this skill remain required for
the SDK install regardless of whether you ran `init` first.

---

## Step 1: Confirm feature scope

Ask the user which features they need. The **Unified SDK** is the
recommended default for most projects — a single instance covers EAV, AI,
Files, and CMS, and `createLazySDK` removes almost all initialization
boilerplate.

| Feature | Description | Required dependencies |
|---------|-------------|-----------------------|
| **Unified SDK** (recommended) | `createReoptSDK()` → `.eav` / `.ai` / `.files` / `.cms` bundled. **`.cms` is read-only as of 1.8.0** (`getBySlug`, `tags.list`, etc.) — content authoring happens in Reopt Studio. | None (`@ai-sdk/provider` if using the AI SDK Provider) |
| **Auth** (Adapter + OAuth) | Reopt as remote DB + OAuth login | `better-auth` |
| **EAV only** | Minimal install for EAV only | None |
| **External marketing site** (1.8+) | Headless blog / sitemap / RSS /약관 / cross-subdomain session via `cms` + `cms` helpers (`toMetadata`, `toSitemapItems`, `toRssFeed`) + `auth` helpers (`getSessionFromCookies`, `verifySession`) + `files` helpers (`optimizeUrl`, `REOPT_IMAGE_REMOTE_PATTERNS`). | None — all helpers are pure / framework-agnostic |
| **Full Stack** | Unified SDK + Auth + Webhooks | `better-auth` |

---

## Step 2: Install packages

### 2a. Authenticate with the registry first (required)

`@reopt-ai/brandapp-sdk` is published to GitHub Packages (private). Without
an `.npmrc` in place, the install fails with `401 Unauthorized`.

Project-root `.npmrc`:

```
@reopt-ai:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
```

`GITHUB_TOKEN` is a PAT with the `read:packages` scope. Inject it through
your shell env (`.zshrc`/`.bashrc`) or a CI secret. Never hardcode the
token value into `.npmrc`.

### 2b. Install the package

```bash
# EAV only
npm install @reopt-ai/brandapp-sdk
# or
pnpm add @reopt-ai/brandapp-sdk
# or
yarn add @reopt-ai/brandapp-sdk

# Including Auth
pnpm add @reopt-ai/brandapp-sdk better-auth
```

Optional peer deps:
- `@ai-sdk/provider` (when using the Vercel AI SDK Provider)
- `@tanstack/react-query` (when using `/react/hooks`)

---

## Step 3: Set up environment variables

Append to `.env.local` (dev-only, git-ignored):

```env
# ── Reopt Brandapp credentials (required) ─────────────────────────────
REOPT_CLIENT_ID=your-client-id
REOPT_CLIENT_SECRET=your-client-secret
REOPT_BRANDAPP_ID=your-brandapp-id

# ── Optional: custom Reopt URL ────────────────────────────────────────
# When unset, the SDK picks a production/dev endpoint based on NODE_ENV.
# REOPT_BASE_URL=https://your-reopt-host.example

# ── Better Auth (when using Auth) ─────────────────────────────────────
# Generate with: openssl rand -base64 32
BETTER_AUTH_SECRET=replace-me-32-bytes-base64
# Must match the origin the browser uses to reach the app
# (for example https://myapp.example.com, http://localhost:3000)
BETTER_AUTH_URL=http://localhost:3000

# ── Webhook (when receiving webhooks) ─────────────────────────────────
# HMAC secret issued in Studio → BrandApp settings
REOPT_WEBHOOK_SECRET=replace-me

# ── Dev Mode (optional) ───────────────────────────────────────────────
# If true, instrumentation.ts boots an in-memory dev server automatically.
# REOPT_DEV_MODE=true

# ── Debug (optional, troubleshooting only) ────────────────────────────
# REOPT_SDK_DEBUG=1             # Log SDK requests/retries
# REOPT_SDK_LOG_FORMAT=json     # Structured JSON logs for AI agents
```

> **`REOPT_BRANDAPP_ID` is not `brandId`.** Use the brandappId (app
> identifier), not the brandId (brand identifier) issued in Studio. The
> SDK adapter URL takes the `/api/v1/brandapp/{brandappId}/...` form. You
> can look it up via the MCP tool `reopt_brandapp_list`.

> **`BETTER_AUTH_URL` must match the browser-facing origin exactly.**
> Setting it to `localhost:3000` while browsing from
> `https://myapp.example.com` triggers an `Invalid origin` error.

> **If you use a self-signed cert in dev**, inject
> `NODE_TLS_REJECT_UNAUTHORIZED=0` **per script only**
> (`NODE_TLS_REJECT_UNAUTHORIZED=0 next dev`). Do not put it in `.env` —
> that disables TLS verification for build/production code too, opening
> the door to MITM attacks. **Never use it in production.**

### env validation (strongly recommended)

`process.env.REOPT_CLIENT_ID!` non-null assertions only reveal `undefined`
at runtime. Validate at application startup with zod / t3-env so
misconfiguration fails fast:

```typescript
// lib/env.ts
import { z } from "zod";

const schema = z.object({
  REOPT_CLIENT_ID: z.string().min(1),
  REOPT_CLIENT_SECRET: z.string().min(1),
  REOPT_BRANDAPP_ID: z.string().uuid(),
  REOPT_BASE_URL: z.string().url().optional(),
  BETTER_AUTH_SECRET: z.string().min(32).optional(),
  BETTER_AUTH_URL: z.string().url().optional(),
  REOPT_WEBHOOK_SECRET: z.string().min(1).optional(),
});

export const env = schema.parse(process.env);
```

Or use `@t3-oss/env-nextjs` to handle the server/client boundary
automatically.

---

## Step 4: Generate files

### When using Auth

#### `lib/auth.ts` (server)

```typescript
import "server-only"; // Prevents clientSecret + BETTER_AUTH_SECRET from leaking into the client bundle
import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";
import { createReoptBetterAuth } from "@reopt-ai/brandapp-sdk/better-auth";

const reopt = createReoptBetterAuth({
  clientId: process.env.REOPT_CLIENT_ID!,
  clientSecret: process.env.REOPT_CLIENT_SECRET!,
  brandappId: process.env.REOPT_BRANDAPP_ID!,
  baseUrl: process.env.REOPT_BASE_URL,
});

export const auth = betterAuth({
  baseURL: process.env.BETTER_AUTH_URL,
  secret: process.env.BETTER_AUTH_SECRET,
  database: reopt.database,
  plugins: [nextCookies(), reopt.oauth],
});
```

> In v1.6+, `createReoptAdapter` / `createReoptOAuth` throw immediately
> when invoked in a browser runtime (they check
> `typeof window !== "undefined"`). The `server-only` import adds a
> bundler-level safety net on top.

#### `lib/auth-client.ts` (client)

```typescript
"use client";

import { createAuthClient } from "better-auth/react";
import {
  createReoptOAuthClient,
  REOPT_PROVIDER_ID,
} from "@reopt-ai/brandapp-sdk/better-auth/client";

export const authClient = createAuthClient({
  plugins: [createReoptOAuthClient()],
});

/**
 * OAuth sign-in. Returns an error so callers can surface it to the user.
 * Returning `void` would silently swallow network/OAuth-server failures.
 */
export async function signInWithReopt(
  callbackURL = "/",
): Promise<{ error?: string }> {
  try {
    await authClient.signIn.oauth2({
      providerId: REOPT_PROVIDER_ID,
      callbackURL,
    });
    return {};
  } catch (err) {
    return {
      error: err instanceof Error ? err.message : "Sign-in failed",
    };
  }
}
```

#### `app/api/auth/[...all]/route.ts`

```typescript
import { toNextJsHandler } from "better-auth/next-js";
import { auth } from "@/lib/auth";

export const { GET, POST } = toNextJsHandler(auth);
```

### When using the Unified SDK (recommended)

#### `lib/sdk.ts`

```typescript
import "server-only"; // Keep clientSecret out of the client bundle
import { createLazySDK } from "@reopt-ai/brandapp-sdk";
import schema from "./eav.schema"; // Optional — enables a type-safe entity client

// v1.3+ — no manual Proxy pattern required. Initializes on first property access.
// In v1.6.1+ the SDK reports its real package version in `X-SDK-Version` (the
// constant is now injected at build time), so request telemetry is reliable.
export const sdk = createLazySDK(() => ({
  clientId: process.env.REOPT_CLIENT_ID!,
  clientSecret: process.env.REOPT_CLIENT_SECRET!,
  brandappId: process.env.REOPT_BRANDAPP_ID!,
  baseUrl: process.env.REOPT_BASE_URL,
  schema, // Omit if you have no schema
}));

// Optional convenience re-exports
export const eav = sdk.eav;
export const ai = sdk.ai;
export const files = sdk.files;
export const cms = sdk.cms;
```

### When using EAV only

The same pattern is recommended even if you only use EAV:

```typescript
import "server-only";
import { createLazySDK } from "@reopt-ai/brandapp-sdk";

export const sdk = createLazySDK(() => ({
  clientId: process.env.REOPT_CLIENT_ID!,
  clientSecret: process.env.REOPT_CLIENT_SECRET!,
  brandappId: process.env.REOPT_BRANDAPP_ID!,
  baseUrl: process.env.REOPT_BASE_URL,
}));

export const eav = sdk.eav;
```

### (Optional) EAV schema definition — type-safe entity client

Passing a schema to `createReoptSDK({ schema })` makes the values in
`sdk.eav.entity("name")` fully type-inferred. Strongly recommended for
larger projects.

#### `lib/eav.schema.ts`

```typescript
import { defineEntity, defineSchema } from "@reopt-ai/brandapp-sdk/eav/schema";

const contacts = defineEntity({
  name: "contacts",
  attributes: {
    name: { dataType: "string", label: "Name", isRequired: true },
    email: { dataType: "email", label: "Email", isUnique: true },
    status: {
      dataType: "select",
      label: "Status",
      // `as const` makes TS infer the literal union ("active" | "inactive")
      options: [
        { value: "active", label: "Active" },
        { value: "inactive", label: "Inactive" },
      ] as const,
    },
  },
});

export default defineSchema({ entities: { contacts } });
```

Usage:

```typescript
const c = sdk.eav.entity("contacts");
const r = await c.records.create({
  values: { name: "John", email: "john@test.com", status: "active" },
  //                                                         ^ type-checked
});
r.values.status; // "active" | "inactive" | undefined
```

Sync the schema to the server with the CLI:

```bash
npx @reopt-ai/cli brandapp eav sync   # Based on lib/eav.schema.ts
```

#### `linkedTo` — 1:1 metadata entities (1.7+)

Pass `linkedTo: 'brandappAuthUser'` on a `defineEntity` call when the
entity should be a 1:1 metadata host on a `BrandappAuthUser` (for
example, per-user preferences). Default is `'brandapp'` (free-form
table). The dev server enforces 1:1 via `409` (duplicate host) and
`422` (missing host); production behaves the same way. `record.id`
deterministically equals `authUserId` for these entities, so `entity()`
lookups can use `authUserId` directly without a prior list.

### (Optional) Dev Server — offline development

Develop without the remote Reopt server by running an in-memory API. On
first start it auto-seeds entities based on the schema. Useful for E2E
tests or disconnected development.

#### `instrumentation.ts` (Next.js root)

```typescript
export async function register() {
  // Next.js edge runtime cannot host the dev server — target nodejs only
  if (process.env.NEXT_RUNTIME !== "nodejs") return;
  if (process.env.REOPT_DEV_MODE !== "true") return;

  const { createDevServer } = await import("@reopt-ai/brandapp-sdk/dev");
  const { default: schema } = await import("./lib/eav.schema");

  const dev = await createDevServer({
    port: 4300,
    brandappId: "dev-app",
    schema: schema as never, // Convert to SDK DevSchema (map explicitly if needed)
  });

  // Point the SDK client at the dev server
  process.env.REOPT_BASE_URL = dev.url;
  process.env.REOPT_CLIENT_ID = "dev";
  process.env.REOPT_CLIENT_SECRET = "dev";
  process.env.REOPT_BRANDAPP_ID = "dev-app";

  console.log(`[reopt-dev] ${dev.url}`);
}
```

`package.json`:

```json
{
  "scripts": {
    "dev": "next dev",
    "dev:local": "REOPT_DEV_MODE=true next dev"
  }
}
```

`pnpm dev:local` runs offline. `pnpm dev` hits the remote Reopt server as usual.

### (Optional) External marketing site — 1.8+ helpers

When the consumer is a separate Next.js site (blog, marketing page,
docs) that reads from a Reopt brandapp, pull these helpers in. They are
pure functions — no React or Next runtime dependency — and ship without
adding a peer dep on `@reopt-ai/opt-editor`.

#### Blog routing — `getBySlug` + `toMetadata`

```typescript
// app/blog/[slug]/page.tsx
import type { Metadata } from "next";
import { sdk } from "@/lib/sdk";
import { toMetadata } from "@reopt-ai/brandapp-sdk/cms";

export async function generateMetadata(
  { params }: { params: Promise<{ slug: string }> },
): Promise<Metadata> {
  const { slug } = await params;
  const post = await sdk.cms.posts.getBySlug(slug);
  return toMetadata(post); // pulls Post.seo + falls back to title/excerpt
}

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = await sdk.cms.posts.getBySlug(slug);
  // post.document.contentRich is now typed as EditorSpec — pass straight to opt-editor StaticRenderer.
  return /* ... */;
}
```

#### Sitemap + RSS

```typescript
// app/sitemap.ts
import type { MetadataRoute } from "next";
import { sdk } from "@/lib/sdk";
import { toSitemapItems } from "@reopt-ai/brandapp-sdk/cms";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const { posts } = await sdk.cms.posts.list({ limit: 1000 });
  return toSitemapItems(posts, { baseUrl: "https://example.com" });
}

// app/rss.xml/route.ts
import { sdk } from "@/lib/sdk";
import { toRssFeed } from "@reopt-ai/brandapp-sdk/cms";

export async function GET() {
  const { posts } = await sdk.cms.posts.list({ limit: 50 });
  const xml = toRssFeed(posts, {
    title: "Example Blog",
    link: "https://example.com",
    description: "Latest posts",
  });
  return new Response(xml, { headers: { "Content-Type": "application/rss+xml" } });
}
```

#### Next.js `<Image>` + Reopt files

```typescript
// next.config.ts
import type { NextConfig } from "next";
import { REOPT_IMAGE_REMOTE_PATTERNS } from "@reopt-ai/brandapp-sdk/files";

export default {
  images: {
    remotePatterns: [...REOPT_IMAGE_REMOTE_PATTERNS],
  },
} satisfies NextConfig;
```

For inline transforms, use `optimizeUrl(url, { width, quality })` — or
`createImageLoader()` to drop into `<Image loader={...}>`.

#### Cross-subdomain session (`*.reopt.ai`)

```typescript
// app/page.tsx
import { headers } from "next/headers";
import { verifySession } from "@reopt-ai/brandapp-sdk/auth";

const session = await verifySession(await headers(), {
  brandappId: process.env.REOPT_BRANDAPP_ID!,
});
if (session) {
  /* session.user is the reopt user — no OAuth flow on the marketing site */
}
```

`getSessionFromCookies(cookieHeader, opts)` is the lower-level form for
non-Next runtimes. Both delegate verification to `apps/id` Better Auth
`/api/auth/get-session`, so they do not require a Better Auth instance
on the consumer site.

### (Optional) Receive webhooks — handle Reopt events

To handle Auth/EAV events in real time, build a webhook endpoint. v1.6+
enables 5-minute replay protection by default, so the sender must include
`timestamp` in the payload (Reopt does so by default).

#### `app/api/webhooks/reopt/route.ts`

```typescript
import { createWebhookHandler } from "@reopt-ai/brandapp-sdk/webhooks";

const handler = createWebhookHandler({
  secret: process.env.REOPT_WEBHOOK_SECRET!,
  // toleranceMs default: 5 * 60_000. Opt out with 0 (not recommended).
  handlers: {
    "record.created": async (payload) => {
      // Handle payload.data
    },
    "record.updated": async (payload) => {
      //
    },
    "subscription.changed": async (payload) => {
      //
    },
    // Available event types: record.*, entity.*, subscription.changed,
    // customer.created (six total). Note: `post.published / post.updated /
    // post.deleted` were removed in 1.8.0 — production never dispatched
    // them.
  },
  onError: (err, payload) => {
    console.error("[webhook]", err, payload.id);
  },
});

export async function POST(req: Request) {
  return handler(req);
}
```

Add `REOPT_WEBHOOK_SECRET` to `.env` (issue it from Studio → BrandApp settings).

### API error handling (recommended)

Starting in v1.6.0, 4xx errors are split into dedicated classes by status
code: `BadRequestError` (400) / `ForbiddenError` (403) /
`NotFoundError` (404) / `ConflictError` (409). All extend `ReoptSDKError`.

#### `lib/api-error.ts`

```typescript
import { NextResponse } from "next/server";
import {
  isReoptSDKError,
  isValidationError,
  AuthError,
  ForbiddenError,
  NotFoundError,
  ConflictError,
  RateLimitError,
} from "@reopt-ai/brandapp-sdk";

export function handleApiError(error: unknown): NextResponse {
  // Field-level validation error (422) — forward fieldErrors to the client
  if (isValidationError(error)) {
    return NextResponse.json(
      {
        error: error.message,
        code: error.code,
        fieldErrors: error.toFieldMap(),
      },
      { status: error.status },
    );
  }

  if (isReoptSDKError(error)) {
    // Branch on specific classes when UI feedback needs to differ
    if (error instanceof AuthError) {
      // Session expired — prompt re-login
    } else if (error instanceof ForbiddenError) {
      // Permission missing — guide the user to workspace/scope
    } else if (error instanceof NotFoundError) {
      // Resource deleted — refresh the list
    } else if (error instanceof ConflictError) {
      // Concurrent edit — re-fetch and retry
    } else if (error instanceof RateLimitError) {
      // Honor the Retry-After header
    }

    return NextResponse.json(
      { error: error.message, code: error.code },
      { status: error.status },
    );
  }

  const message =
    error instanceof Error ? error.message : "Internal Server Error";
  return NextResponse.json({ error: message }, { status: 500 });
}
```

---

## Step 5: Verify

### Compile check

```bash
npx tsc --noEmit
```

### Auth connectivity check (when using Auth)

```bash
pnpm dev
curl -I http://localhost:3000/api/auth/ok
# Expect: HTTP/1.1 200 OK
```

### SDK connectivity check (any module)

The cheapest call validates credentials, network, and permissions:

```typescript
// In a server component or route handler
import { sdk } from "@/lib/sdk";
const entities = await sdk.eav.entities.list();
// Or AI
const models = await sdk.ai.models();
```

401 AuthError → re-check clientId/secret. 404 NotFoundError → re-check brandappId.

### Full health check (playground reference)

Mirror the `apps/brandapp-playground/app/health/` pattern to build a
`/health` page that verifies every SDK service in one click before each
deploy. Twelve probes are defined in `lib/health-checks.ts`.

---

## Notes

- `isProduction` is auto-detected from `NODE_ENV` — no explicit setting needed.
- When `REOPT_BASE_URL` is undefined, the production/development URL is chosen automatically.
- `better-auth` is an optional peer dep — not required for EAV-only usage.
- Prefer the `isReoptSDKError()` type guard for error handling (bundle-safe versus `instanceof` — works even when multiple SDK copies coexist).
- v1.6+ splits 4xx into `BadRequestError` / `ForbiddenError` / `NotFoundError` / `ConflictError`, enabling per-status UX.
- v1.6.1 adds React mutation hooks `useUpsertRecord`, `useBulkCreateRecords`, `useBulkUpdateRecords`, `useBulkDeleteRecords`, `useDeleteRecordsWhere` (mutation surface now matches `sdk.eav.records.*`); `sdk.files.upload()` accepts `{ signal, timeout }` per call.
- v1.7 adds `linkedTo: 'brandappAuthUser'` on `defineEntity` for 1:1 user-metadata entities; dev server enforces 409 / 422.
- v1.8 makes `cms` read-only and ships marketing-site helpers (`toMetadata`, `toSitemapItems`, `toRssFeed`, `optimizeUrl`, `verifySession`). `PostDetail.document.contentRich` is now typed as `EditorSpec`. `usePostBySlug` and `useCmsTags` are the new TanStack Query hooks.
- Reference project: `apps/brandapp-playground/` (ships E2E tests + the `/health` SDK dashboard).

---

## Output format

After initialization, report in the format below. **List only the files
you actually created.** Skip entries for optional steps you didn't run
(no false reports).

```
## @reopt-ai/brandapp-sdk initialization complete

### Files created
- .npmrc — GitHub Packages registry
- .env.local — env template (values still need to be filled in)
- lib/sdk.ts — Unified SDK (createLazySDK)
- lib/auth.ts — Better Auth server config              (if Auth selected)
- lib/auth-client.ts — OAuth client                    (if Auth selected)
- lib/api-error.ts — SDK error handler
- lib/eav.schema.ts — type-safe schema                 (optional)
- lib/env.ts — zod-based env validation                (optional)
- instrumentation.ts — auto-boot the dev server        (optional)
- app/api/auth/[...all]/route.ts — Auth API            (if Auth selected)
- app/api/webhooks/reopt/route.ts — webhook receiver   (optional)

### Next steps
1. Fill REOPT_CLIENT_ID / REOPT_CLIENT_SECRET / REOPT_BRANDAPP_ID in .env.local
   - Generate BETTER_AUTH_SECRET with `openssl rand -base64 32`
   - Inject GITHUB_TOKEN (read:packages PAT) via a shell env var
2. Run `pnpm install` (after registry auth is configured)
3. Start with `pnpm dev` or `pnpm dev:local` (dev-server mode)
4. Verify:
   - Compile: `npx tsc --noEmit`
   - Auth:    `curl -I http://localhost:3000/api/auth/ok` → 200
   - SDK:     `await sdk.eav.entities.list()` succeeds from a server component
```
