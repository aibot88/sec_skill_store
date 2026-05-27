---
name: deploying-azure-static-web-apps
description: Deploys React + Azure Functions apps to Azure Static Web Apps with managed API functions, including the CommonJS / index.ts import / route-registration gotchas that make new functions 404 silently. Provides the SWA Bicep module, staticwebapp.config.json routing + security headers, and the API entrypoint convention. Use when scaffolding a SWA-based project, adding a new API function, or fixing a deployed function that returns 404 even though it compiled successfully.
---

# Deploying Azure Static Web Apps

The default deployment target for React + Functions web apps. Free tier, global CDN, managed Functions baked in, zero ongoing cost when idle.

## When to use SWA vs FC1 vs Container Apps

| Need | Use |
|------|-----|
| CRUD REST API, React frontend, HTTP-only, < 30s requests | **SWA managed functions** (this skill) |
| Timer triggers, queue triggers, AI workloads, > 30s execution | [FC1 Flex Consumption](../deploying-fc1-flex-consumption-functions/SKILL.md) |
| Long-running server, WebSocket/SSE, custom Docker runtime | [Container Apps](../deploying-azure-container-apps/SKILL.md) |

## Project structure

```
frontend/                        — React 19 + Vite 6 + TypeScript
├── src/
│   ├── App.tsx
│   └── services/api.ts
├── public/
│   └── staticwebapp.config.json — routing + security headers
├── vite.config.ts               — proxy /api/* → localhost:7071
└── package.json

api/                              — Managed Azure Functions v4 (Node 22)
├── src/
│   ├── index.ts                 — Entry point — IMPORT EVERY FUNCTION FILE HERE
│   ├── functions/
│   │   ├── hello.ts             — app.http(...) at the bottom registers the route
│   │   ├── getItems.ts
│   │   └── createItem.ts
│   └── lib/
│       └── database.ts          — mssql pool, module-level singleton
├── host.json
├── tsconfig.json                — "module": "commonjs" required for SWA
├── package.json                 — "main": "dist/index.js" (specific path, not glob)
└── local.settings.json.example  — empty strings + __HINT_* keys
```

## The two SWA gotchas you WILL hit

### 1. New function returns 404 — forgot to import in `index.ts`

```typescript
// api/src/index.ts — every function file imported as a side effect
import './functions/hello';
import './functions/getItems';
import './functions/createItem';
import './functions/newThing';    // ← add this when you create newThing.ts
```

The `app.http(...)` registration in each function file only runs when the module is loaded. If `index.ts` doesn't import it, the route silently doesn't exist. The TypeScript compiles fine. The deploy succeeds. The URL returns 404.

**Make this part of your "add a function" muscle memory:** create the file, write the function, **add the import**.

### 2. CommonJS, not ESM

SWA managed functions require:

```json
// api/tsconfig.json
{ "compilerOptions": { "module": "commonjs" } }

// api/package.json
{ "main": "dist/index.js" }      // ← specific path, not "dist/**/*.js"
// (do NOT add "type": "module")
```

This differs from standalone FC1 which uses ESM. If you migrate api/ to FC1 later, you must flip both settings.

## Function file template

```typescript
// api/src/functions/getItems.ts
import { app, HttpRequest, HttpResponseInit, InvocationContext } from '@azure/functions';
import { getPool } from '../lib/database';

export async function getItems(req: HttpRequest, ctx: InvocationContext): Promise<HttpResponseInit> {
  // Mock when DB not configured (local dev convenience)
  if (!process.env.SQL_CONNECTION_STRING) {
    ctx.warn('SQL_CONNECTION_STRING not set — returning mock');
    return { status: 200, jsonBody: { items: [{ id: 1, name: '[MOCK] Item' }] } };
  }

  const pool = await getPool();
  const result = await pool.request().query('SELECT * FROM dbo.Items');
  return { status: 200, jsonBody: { items: result.recordset } };
}

// Route registration — runs when this module is imported by index.ts
app.http('getItems', {
  methods: ['GET'],
  authLevel: 'anonymous',
  route: 'items',
  handler: getItems,
});
```

## `local.settings.json.example` pattern

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_EXTENSION_VERSION": "~4",
    "FUNCTIONS_WORKER_RUNTIME": "node",
    "SQL_CONNECTION_STRING": "",
    "__HINT_SQL_CONNECTION_STRING": "Server=tcp:{org}-{project}-sql-test.database.windows.net,1433;Database={org}-{project}-sqldb-test;User Id=sqladmin;Password=YOUR_PASSWORD;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
  }
}
```

**Use `""` for all user-input values.** Placeholder strings like `"sk-YOUR_KEY"` are truthy in JavaScript and fool `if (!value)` checks, causing confusing runtime errors instead of clean "not configured" mocks. Use `__HINT_*` keys for format documentation (Functions ignores `__`-prefixed keys).

## Mock pattern

Always check the env var; fall back to a mock when not set. This makes local dev work without provisioning:

```typescript
if (!process.env.AI_PROJECT_ENDPOINT) {
  ctx.warn('AI_PROJECT_ENDPOINT not set — returning mock response');
  return { status: 200, jsonBody: { result: '[MOCK] Set AI_PROJECT_ENDPOINT.' } };
}

if (process.env.SQL_CONNECTION_STRING) {
  await saveToDB(...);
} else {
  ctx.warn('SQL_CONNECTION_STRING not set — skipping DB write');
}
```

## `staticwebapp.config.json`

```json
{
  "navigationFallback": { "rewrite": "/index.html", "exclude": ["/api/*", "/assets/*", "*.{css,js,png,svg}"] },
  "globalHeaders": {
    "Strict-Transport-Security": "max-age=63072000; includeSubDomains; preload",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
  }
}
```

See [references/swa-config.md](references/swa-config.md) for the full routing + auth pattern.

## Bicep

The SWA Bicep module lives in [`scaffolding-azure-bicep-infrastructure/templates/infra/modules/staticWebApp.bicep`](../scaffolding-azure-bicep-infrastructure/templates/infra/modules/staticWebApp.bicep). It exposes:

- `skuName` — per-env (`Free` in test, `Standard` in prod)
- `sqlConnectionString` — `@secure()`, sets the `SQL_CONNECTION_STRING` app setting

## Composes with

- [scaffolding-azure-bicep-infrastructure](../scaffolding-azure-bicep-infrastructure/SKILL.md) — generates the SWA Bicep + workflow
- [managing-azure-sql-migrations](../managing-azure-sql-migrations/SKILL.md) — for the DB schema
- [diagnosing-azure-deployment-failures](../diagnosing-azure-deployment-failures/SKILL.md) — when functions 404 or return 500
