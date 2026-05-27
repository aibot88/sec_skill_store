---
name: supabase-edge-functions
description: >
  This skill should be used when developing, deploying, or managing Supabase Edge Functions,
  working with Deno in Supabase, or building serverless endpoints.
  Trigger when: "edge function", "deploy function", "supabase functions", "Deno function",
  "serverless endpoint", "functions serve", "functions deploy", "create function",
  "webhook handler", "Supabase function secrets", "function logs",
  "supabase functions new", "invoke function", "edge runtime", "Deno.serve",
  "Supabase Cron", "scheduled function", "pg_cron", "scheduled edge function",
  "Stripe in Supabase", "Stripe v22",
  or building any server-side TypeScript function for Supabase.
---

# Supabase Edge Functions

Guidance for developing, deploying, and managing Edge Functions on Supabase Edge Runtime (Deno 2.1.4 as of April 2026), using both MCP tools and CLI.

## Overview

Edge Functions are globally distributed TypeScript functions running on Deno. They serve as server-side endpoints for webhooks, API routes, scheduled tasks, and third-party integrations.

## Creating Edge Functions

### Via CLI (recommended for local development)

```bash
supabase functions new my-function
```

Creates `supabase/functions/my-function/index.ts` with a starter template.

### Function Structure

```
supabase/functions/
├── _shared/              # Shared modules across functions
│   └── cors.ts
├── my-function/
│   ├── index.ts          # Entry point (required)
│   └── deno.json         # Deno config (optional)
└── another-function/
    └── index.ts
```

### Basic Function Template (Deno 2.x)

```typescript
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

Deno.serve(async (req: Request) => {
  const { name } = await req.json();

  return new Response(
    JSON.stringify({ message: `Hello ${name}!` }),
    { headers: { "Content-Type": "application/json" } }
  );
});
```

**Don't** import `serve` from `https://deno.land/std@*/http/server.ts` — it's deprecated. `Deno.serve` is built-in in Deno 2.x and is the only pattern current docs recommend. Caught by `audit-edge-functions.py`.

### Function with Supabase Client

```typescript
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

Deno.serve(async (req: Request) => {
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  );

  const { data, error } = await supabase
    .from("profiles")
    .select("*")
    .limit(10);

  return new Response(JSON.stringify({ data, error }), {
    headers: { "Content-Type": "application/json" },
  });
});
```

The fallback chain (`SECRET_KEY ?? SERVICE_ROLE_KEY`) covers both modern (`sb_secret_*`) and legacy (`service_role` JWT) projects.

### CORS Headers (Shared Module)

Restrict origins by default — wildcard (`*`) is flagged by `audit-edge-functions.py`:

```typescript
// supabase/functions/_shared/cors.ts
const ALLOWED_ORIGINS = [
  "https://myapp.com",
  "https://staging.myapp.com",
];

export function corsHeaders(origin: string | null) {
  const isAllowed = origin && ALLOWED_ORIGINS.includes(origin);
  return {
    "Access-Control-Allow-Origin": isAllowed ? origin : ALLOWED_ORIGINS[0],
    "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
    "Vary": "Origin",
  };
}
```

A wildcard `*` is acceptable for genuinely public endpoints (unauthenticated webhooks, public health checks); document why in a comment so reviewers and the static validator can recognize the intent.

## Deploying Edge Functions

### Via MCP

```
mcp__supabase__deploy_edge_function(
  project_id: "<project_id>",
  name: "my-function",
  entrypoint_path: "index.ts",
  verify_jwt: true,
  files: [
    { "name": "index.ts", "content": "<function code>" },
    { "name": "deno.json", "content": "<deno config if exists>" }
  ]
)
```

The `verify_jwt` flag has been a deploy-time parameter since MCP server v0.5.10 (Dec 2025). Default is `true`.

**JWT Verification (`verify_jwt`):**
- **Default `true`** — Supabase rejects requests without a valid Authorization Bearer token.
- Set `false` only when the function implements its own auth (webhook signature verification, public health checks, or API-key auth). Document why in a comment in `config.toml`:
  ```toml
  [functions.stripe-webhook]
  # Stripe webhook signature replaces JWT auth — see verifyEvent() in index.ts
  verify_jwt = false
  ```
  `audit-edge-functions.py` flags `verify_jwt = false` without an accompanying `#` comment.

### Via CLI

```bash
# Deploy single function
supabase functions deploy my-function

# Deploy all functions
supabase functions deploy

# Deploy without JWT verification (webhooks, public endpoints)
supabase functions deploy my-function --no-verify-jwt
```

### Listing Functions

```
# MCP
mcp__supabase__list_edge_functions(project_id: "<id>")

# CLI
supabase functions list
```

### Getting Function Code (MCP)

```
mcp__supabase__get_edge_function(
  project_id: "<id>",
  function_slug: "my-function"
)
```

Returns the function's file contents. Use this to inspect deployed function code.

## Local Development

### Serve Functions Locally

```bash
supabase functions serve
```

Starts a local edge runtime. Functions are available at:
```
http://localhost:54321/functions/v1/<function-name>
```

### Test Locally with curl

```bash
curl -i --location --request POST \
  'http://localhost:54321/functions/v1/my-function' \
  --header 'Authorization: Bearer <publishable_or_anon_key>' \
  --header 'Content-Type: application/json' \
  --data '{"name": "World"}'
```

### Environment Variables

Edge Functions access environment variables via `Deno.env.get()`. Built-in variables available in deployed functions:

| Variable | Description |
|----------|-------------|
| `SUPABASE_URL` | Project API URL |
| `SUPABASE_PUBLISHABLE_KEY` | Modern publishable key (`sb_publishable_*`) |
| `SUPABASE_ANON_KEY` | Legacy anon key (still injected for compatibility) |
| `SUPABASE_SECRET_KEY` | Modern secret key (`sb_secret_*`, bypasses RLS) |
| `SUPABASE_SERVICE_ROLE_KEY` | Legacy service role key (still injected for compatibility) |
| `SUPABASE_DB_URL` | Direct Postgres connection string |

### Managing Secrets

```bash
supabase secrets set MY_API_KEY=sk-xxx ANOTHER_SECRET=value
supabase secrets list
supabase secrets unset MY_API_KEY
```

Secrets are available as environment variables in deployed edge functions.

## Common Patterns

### Webhook Handler (Stripe v22)

Stripe Node SDK v22 (March 2026) introduced a real ES6 class — `new Stripe(...)` is now required:

```typescript
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import Stripe from "npm:stripe@22";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY")!);
const webhookSecret = Deno.env.get("STRIPE_WEBHOOK_SECRET")!;

Deno.serve(async (req: Request) => {
  const body = await req.text();
  const signature = req.headers.get("stripe-signature")!;

  let event;
  try {
    event = await stripe.webhooks.constructEventAsync(body, signature, webhookSecret);
  } catch (err) {
    return new Response(`Webhook signature verification failed: ${err.message}`, { status: 400 });
  }

  switch (event.type) {
    case "checkout.session.completed":
      // Handle completed checkout
      break;
  }

  return new Response(JSON.stringify({ received: true }), {
    headers: { "Content-Type": "application/json" },
  });
});
```

`audit-edge-functions.py` flags Stripe imports below v22 with the upgrade hint.

### Scheduled Functions — Supabase Cron (recommended)

Supabase ships **Supabase Cron** as a first-class scheduling module. The dashboard UI generates and manages the schedule for you, with sub-minute resolution (down to 1 second between executions). Under the hood it uses `pg_cron` + `pg_net` — same machinery, easier UX.

In SQL (or via dashboard):

```sql
-- Enable the module if not already
create extension if not exists pg_cron;
create extension if not exists pg_net;

-- Schedule via the cron schema (dashboard generates the same)
select cron.schedule(
  'daily-cleanup',
  '0 3 * * *',
  $$
  select net.http_post(
    url := 'https://<project>.supabase.co/functions/v1/cleanup',
    headers := jsonb_build_object(
      'Authorization', 'Bearer ' || current_setting('app.settings.service_role_key')
    )
  );
  $$
);
```

The dashboard's Cron page presents three job types: Database Function, HTTP Request, and Supabase Edge Function — choose Edge Function for the simplest path. See [Supabase Cron docs](https://supabase.com/docs/guides/cron) and [Scheduling Edge Functions](https://supabase.com/docs/guides/functions/schedule-functions).

## Function Logs

### Via MCP

```
mcp__supabase__get_logs(
  project_id: "<id>",
  service: "edge-function"
)
```

Returns logs from the last 24 hours for all edge functions.

## Static audit before deploying

```bash
python plugins/rad-supabase/scripts/audit-edge-functions.py
```

Catches: deprecated `serve` import, CORS wildcard, hardcoded secrets, Stripe < v22, undocumented `verify_jwt = false`.

## CLI vs MCP Decision Matrix

| Task | Use CLI | Use MCP |
|------|---------|---------|
| Create function scaffold | `functions new` | Not available |
| Deploy function | `functions deploy` | `deploy_edge_function` |
| List functions | `functions list` | `list_edge_functions` |
| Get function code | `functions download` | `get_edge_function` |
| Serve locally | `functions serve` | Not available |
| Manage secrets | `secrets set/list/unset` | Not available |
| View logs | Dashboard | `get_logs` (service: edge-function) |
| Delete function | `functions delete` | Not available |
| Schedule | `pg_cron` migration or dashboard Cron UI | `apply_migration` for the `cron.schedule(...)` SQL |
