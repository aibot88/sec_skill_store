---
# yaml-language-server: $schema=https://skillgraph.dev/schemas/skill.v6.schema.json
schema_version: 6
name: nextjs-server-action-validation
description: "Use when writing a Next.js Server Action that accepts user-submitted form data, mutation parameters, or any client-originated input. Every Server Action is a public HTTP endpoint regardless of how it is called — validate with Zod and check authentication as the first two operations before touching the database. Do NOT use for GET route handlers or Server Components that fetch data (those have no user-supplied input); do NOT use for Stripe webhook handlers (use stripe-webhook-signature-verification instead)."
version: 0.1.0
type: capability
category: engineering
domain: engineering/web
scope: portable
owner: saas-stripe-postgres-example
freshness: "2026-05-18"
drift_check:
  last_verified: "2026-05-18"
eval_artifacts: none
eval_state: unverified
routing_eval: absent
stability: experimental
license: MIT
compatibility:
  runtimes:
    - node
  node: ">=20"
  notes: "Next.js App Router >=14 with server actions enabled; Zod >=3."
allowed-tools: Read Grep
keywords:
  - next.js server action validation
  - zod input validation
  - server action security
  - server action auth check
  - server action public endpoint
  - use server directive
  - form action security
  - server action pattern
  - mutation validation
  - next.js app router actions
triggers:
  - nextjs-server-action-validation
paths:
  - "app/actions/*.ts"
  - "lib/actions/*.ts"
examples:
  - "write a Server Action for the checkout form that validates the selected plan before creating a Stripe session"
  - "secure a Server Action so it rejects unauthenticated requests"
  - "validate user input with Zod in a Server Action before writing to Postgres"
  - "my Server Action is being called directly via fetch — is that safe?"
anti_examples:
  - "validate the stripe-signature header in a webhook route handler"
  - "fetch data in a Server Component to display on a page"
  - "write a GET route handler that returns public product data"
relations:
  boundary:
    - skill: stripe-webhook-signature-verification
      reason: "stripe-webhook-signature-verification validates Stripe's HMAC signature on webhook route handlers; this skill validates user-submitted input on Server Actions — different trust model, different entry point"
    - skill: postgres-rls-pattern
      reason: "postgres-rls-pattern governs the database layer; this skill governs the action layer — both are required in a secure Server Action, but at separate tiers"
  depends_on:
    - skill: postgres-rls-pattern
      reason: "Server Actions that write to Postgres must call orgQuery to enforce tenant isolation after input is validated"
  verify_with:
    - stripe-webhook-signature-verification
portability:
  readiness: portable
  targets:
    - skill-md
lifecycle:
  stale_after_days: 90
  review_cadence: quarterly
---

# Next.js Server Action Validation

## Coverage

- The public endpoint reality — `'use server'` functions are exposed as POST endpoints that any HTTP client can call directly; the Next.js call graph is not a security boundary
- Validation order — auth check BEFORE Zod parse, Zod parse BEFORE database access; any other order produces an exploitable window
- Zod schema design for actions — using `.safeParse()` over `.parse()` to return structured errors rather than throwing; returning `{ error: ... }` shapes that the calling Client Component can render
- Org-scoping after authentication — verifying that `input.orgId` matches the session's org, not just that the user is logged in
- Error surface control — how `try/catch` around database calls prevents internal errors from propagating to the client response

## Philosophy

Server Actions are a convenience feature that makes form submission feel like a function call. That convenience obscures a critical fact: the action is a public HTTP POST endpoint. A developer who writes `const { data } = await myAction(formData)` in a Client Component is writing what looks like a local function call, but the runtime sends an HTTP request that any script can replicate. Skipping auth or validation because "it's called from our own UI" is the same reasoning that made `getServerSideProps` data-fetching functions leaky in the Pages Router — the server boundary does not restrict callers.

## Standard Action Pattern

```typescript
"use server";
import { z } from "zod";
import { getServerSession } from "@/lib/auth";
import { orgQuery } from "@/lib/db";

const CreateOrderSchema = z.object({
  orgId: z.string().uuid(),
  planId: z.string().min(1),
  quantity: z.number().int().positive(),
});

export async function createOrder(input: unknown) {
  // 1. Auth check — before anything else
  const session = await getServerSession();
  if (!session?.user) {
    return { error: "Unauthorized" };
  }

  // 2. Zod parse — structured errors, not thrown exceptions
  const parsed = CreateOrderSchema.safeParse(input);
  if (!parsed.success) {
    return { error: parsed.error.flatten() };
  }

  // 3. Org-scope check — user must belong to the org they are acting on
  if (session.user.orgId !== parsed.data.orgId) {
    return { error: "Forbidden" };
  }

  // 4. Database write — inside orgQuery for RLS enforcement
  try {
    const [order] = await orgQuery(parsed.data.orgId, (tx) =>
      tx`INSERT INTO orders (org_id, plan_id, quantity) VALUES (
          ${parsed.data.orgId}, ${parsed.data.planId}, ${parsed.data.quantity}
        ) RETURNING *`
    );
    return { data: order };
  } catch {
    return { error: "Failed to create order" };
  }
}
```

## Validation Order Rationale

| Order | Risk |
|---|---|
| Auth → Zod → orgScope → DB | Correct — each gate eliminates the next attack surface |
| Zod → Auth → DB | Attacker can probe the schema structure without authenticating |
| Auth → DB (no Zod) | Malformed input reaches the query layer; injection risk |
| DB → Auth (anywhere) | Unauthenticated database reads before rejection |

## Verification

- [ ] Every `'use server'` function calls `getServerSession()` as its first statement
- [ ] Every `'use server'` function runs `Schema.safeParse()` before any database call
- [ ] The session org ID is compared to the input org ID before the database call
- [ ] Database calls are wrapped in `orgQuery`, not bare SQL
- [ ] Errors returned to the client do not include stack traces or query text

## Do NOT Use When

| Use instead | When |
|---|---|
| `stripe-webhook-signature-verification` | The entry point is a webhook route handler, not a Server Action |
| (a data-fetching skill) | The function is a Server Component that fetches data, with no user-submitted input |
| `postgres-rls-pattern` | The task is defining the database-layer policy, not the action-layer validation |
