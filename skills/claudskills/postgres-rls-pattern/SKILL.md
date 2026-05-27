---
# yaml-language-server: $schema=https://skillgraph.dev/schemas/skill.v6.schema.json
schema_version: 6
name: postgres-rls-pattern
description: "Use when writing or reviewing Postgres queries in a multi-tenant SaaS where every table row must be scoped to a single organization. Enforces the FORCE ROW LEVEL SECURITY + USING + WITH CHECK triple on every tenant-bound table, and wraps application queries in an `orgQuery(orgId)` helper that sets `app.current_org_id` before each statement. Do NOT use for cross-org system queries such as billing cron jobs or admin panels (those bypass RLS intentionally via the service role); use a service-role query wrapper instead."
version: 0.1.0
type: capability
category: engineering
domain: engineering/database
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
  notes: "Postgres >=14 with row-level security enabled; assumes pg or postgres.js driver."
allowed-tools: Read Grep
keywords:
  - postgres row level security
  - RLS multi-tenant
  - orgQuery wrapper
  - FORCE ROW LEVEL SECURITY
  - SET app.current_org_id
  - tenant data isolation
  - cross-tenant data leak prevention
  - multi-tenant postgres
  - row security policy
  - using with check policy
triggers:
  - postgres-rls-pattern
paths:
  - "lib/db.ts"
  - "db/schema.sql"
  - "db/migrations/*.sql"
examples:
  - "how do I prevent one tenant's data from appearing in another tenant's queries?"
  - "write the RLS policy for the orders table in a multi-tenant SaaS"
  - "set up the orgQuery helper so every query is automatically scoped to the current org"
  - "add row level security to a new subscriptions table"
anti_examples:
  - "run a billing cron job that needs to read all orgs"
  - "write a migration that backfills data across all organizations"
  - "query the database without any tenant context for an admin dashboard"
relations:
  boundary:
    - skill: migrate-orders-to-canonical-schema
      reason: "migrate-orders-to-canonical-schema changes column layout; this skill defines the RLS policy that must be updated alongside any schema change on tenant-bound tables"
    - skill: nextjs-server-action-validation
      reason: "nextjs-server-action-validation validates the input layer; this skill governs the query layer — both are required but at different tiers"
  depends_on: []
  verify_with:
    - migrate-orders-to-canonical-schema
portability:
  readiness: portable
  targets:
    - skill-md
lifecycle:
  stale_after_days: 180
  review_cadence: quarterly
---

# Postgres RLS Pattern

## Coverage

- The three-part policy triple — `FORCE ROW LEVEL SECURITY`, `USING (org_id = current_setting('app.current_org_id')::uuid)`, and `WITH CHECK (org_id = current_setting('app.current_org_id')::uuid)` — and why omitting any one part leaves a gap
- The `orgQuery(orgId)` application wrapper — a single function that opens a transaction, sets `app.current_org_id`, runs the caller's query, and commits; why setting the variable once at session start is unsafe under connection pooling
- Service role bypass — legitimate cross-org operations (billing cron, admin panel, migration backfills) that must use a connection string that skips RLS, and why those code paths must be isolated from application code
- Policy audit checklist — grepping for `query()` calls without a preceding `SET app.current_org_id` as a CI-safe audit gate
- New-table checklist — steps to add RLS to a table that was created before RLS was enforced on the schema

## Philosophy

Row-level security on Postgres is the difference between "we checked org_id in the WHERE clause" and "the database rejects cross-org reads at the storage layer." Application-level checks are deleted by a single missing WHERE clause; RLS cannot be bypassed unless you use the service role explicitly. The cost is a session variable that must be set before every query and a discipline of never using the service role for application queries. Both costs are cheap relative to the consequence of a cross-tenant data leak.

## Schema Pattern

```sql
-- 1. Enable and force RLS on every tenant-bound table
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;

-- 2. SELECT policy — only rows where org_id matches the session variable
CREATE POLICY orders_org_select ON orders
  FOR SELECT
  USING (org_id = current_setting('app.current_org_id', true)::uuid);

-- 3. INSERT policy — only allow inserts that match the session variable
CREATE POLICY orders_org_insert ON orders
  FOR INSERT
  WITH CHECK (org_id = current_setting('app.current_org_id', true)::uuid);

-- 4. UPDATE policy — USING (read filter) AND WITH CHECK (write filter)
CREATE POLICY orders_org_update ON orders
  FOR UPDATE
  USING (org_id = current_setting('app.current_org_id', true)::uuid)
  WITH CHECK (org_id = current_setting('app.current_org_id', true)::uuid);

-- 5. DELETE policy
CREATE POLICY orders_org_delete ON orders
  FOR DELETE
  USING (org_id = current_setting('app.current_org_id', true)::uuid);
```

## Application Wrapper Pattern

```typescript
// lib/db.ts
import postgres from "postgres";

const sql = postgres(process.env.DATABASE_URL!);

/** Tenant-scoped query: sets app.current_org_id for every statement. */
export async function orgQuery<T>(
  orgId: string,
  fn: (sql: postgres.Sql) => Promise<T>
): Promise<T> {
  return sql.begin(async (tx) => {
    await tx`SELECT set_config('app.current_org_id', ${orgId}, true)`;
    return fn(tx);
  });
}

/** System query: bypasses RLS. Use ONLY for cron jobs, migrations, and admin. */
export async function systemQuery<T>(fn: (sql: postgres.Sql) => Promise<T>): Promise<T> {
  return fn(sql);
}
```

Usage in a Server Action:

```typescript
import { orgQuery } from "@/lib/db";

export async function getOrders(orgId: string) {
  return orgQuery(orgId, (tx) => tx`SELECT * FROM orders ORDER BY created_at DESC`);
}
```

## Verification

- [ ] Every tenant-bound table has `ENABLE ROW LEVEL SECURITY` AND `FORCE ROW LEVEL SECURITY`
- [ ] Every DML operation (SELECT, INSERT, UPDATE, DELETE) has a corresponding policy on each table
- [ ] `WITH CHECK` is present on INSERT and UPDATE policies (not just `USING`)
- [ ] `orgQuery` sets the variable inside a transaction, not at session start
- [ ] No application code calls `systemQuery` (grep for `systemQuery` in `apps/` and `lib/` — any hit is a finding)
- [ ] Every new migration that adds a table includes the RLS policy triple in the same migration file

## Do NOT Use When

| Use instead | When |
|---|---|
| `systemQuery` wrapper | The query legitimately crosses org boundaries (billing cron, migration backfill, admin panel) |
| `migrate-orders-to-canonical-schema` | The task is a schema migration that also needs to update RLS policies |
| (a database skill without multi-tenancy scope) | The application is single-tenant and org_id isolation is not a requirement |
