---
name: postgres-rls
description: "Guides agents implementing or auditing PostgreSQL Row Level Security in a multi-tenant SaaS codebase. Covers ENABLE+FORCE pairing, USING+WITH CHECK policies, view bypass via security_invoker, SET LOCAL for connection pool safety, superuser/owner bypass detection, and materialized view risks. Do NOT use for application-level authorization logic (use nextauth-patterns), non-PostgreSQL databases, or application query tier questions (use multi-tenancy-rls for orgQuery() usage)."
license: MIT
compatibility: "Targets PostgreSQL 15+ with Neon serverless driver. The security_invoker view pattern requires PG15+. The SET LOCAL / set_config(key, val, true) pattern applies to any connection-pooled PostgreSQL setup. Core ENABLE+FORCE+USING+WITH CHECK rules are PG version-independent."
allowed-tools: Read Grep Glob Bash
metadata:
  grounding: "{\"domain_object\":\"PostgreSQL Row Level Security implementation in Sales Hub\",\"grounding_mode\":\"repo_specific\",\"truth_sources\":[\"../sales-hub/apps/web/src/lib/db.ts\",\"../sales-hub/db/migrations/20260218_rls_hardening.sql\",\"../sales-hub/db/migrations/20260314_rls_expansion.sql\",\"../sales-hub/db/migrations/20260314_rls_with_check_and_security_invoker.sql\",\"../sales-hub/db/migrations/20260315_enable_rls_all.sql\"],\"failure_modes\":[\"security_leak\",\"incorrect_isolation\",\"missing_force_rls\",\"missing_with_check\",\"superuser_bypass\",\"connection_pool_context_leakage\",\"view_security_invoker_missing\"],\"evidence_priority\":\"repo_code_first\"}"
  drift_check: "{\"last_verified\":\"2026-05-18\",\"truth_source_hashes\":{\"../sales-hub/apps/web/src/lib/db.ts\":\"d1d9988d1da4545c58f76b5f44dbd12d5323409b777920d31d5f496db31ad7cb\",\"../sales-hub/db/migrations/20260218_rls_hardening.sql\":\"b5fb6dc74e78a3fb7e77c669af4e4b4303a4e995eaf4993cb6bdcbe7bdca424f\",\"../sales-hub/db/migrations/20260314_rls_expansion.sql\":\"406e2c419b09a6866f10c508e4ff6dc1f7a1ee82b788c5e2515186561c30ffb5\",\"../sales-hub/db/migrations/20260314_rls_with_check_and_security_invoker.sql\":\"2edcb51debd4ab4e7306eb6f8908c7a725217b19962e1429728e911fc57e88fb\",\"../sales-hub/db/migrations/20260315_enable_rls_all.sql\":\"c8de6823684f84b54376284a3a51bb6b52e38acd4f5c29664be26e89e5d39570\"}}"
  metadata: "{\"schema_version\":6,\"version\":\"1.1.0\",\"type\":\"capability\",\"category\":\"engineering\",\"domain\":\"engineering/database-security\",\"scope\":\"codebase\",\"owner\":\"skill-graph-maintainer\",\"freshness\":\"2026-05-18\",\"drift_check\":\"{\\\\\\\"last_verified\\\\\\\":\\\\\\\"2026-05-18\\\\\\\",\\\\\\\"truth_source_hashes\\\\\\\":{\\\\\\\"sales-hub/apps/web/src/lib/db.ts\\\\\\\":\\\\\\\"d1d9988d1da4545c58f76b5f44dbd12d5323409b777920d31d5f496db31ad7cb\\\\\\\",\\\\\\\"sales-hub/db/migrations/20260218_rls_hardening.sql\\\\\\\":\\\\\\\"b5fb6dc74e78a3fb7e77c669af4e4b4303a4e995eaf4993cb6bdcbe7bdca424f\\\\\\\",\\\\\\\"sales-hub/db/migrations/20260314_rls_expansion.sql\\\\\\\":\\\\\\\"406e2c419b09a6866f10c508e4ff6dc1f7a1ee82b788c5e2515186561c30ffb5\\\\\\\",\\\\\\\"sales-hub/db/migrations/20260314_rls_with_check_and_security_invoker.sql\\\\\\\":\\\\\\\"2edcb51debd4ab4e7306eb6f8908c7a725217b19962e1429728e911fc57e88fb\\\\\\\",\\\\\\\"sales-hub/db/migrations/20260315_enable_rls_all.sql\\\\\\\":\\\\\\\"c8de6823684f84b54376284a3a51bb6b52e38acd4f5c29664be26e89e5d39570\\\\\\\"}}\",\"eval_artifacts\":\"none\",\"eval_state\":\"unverified\",\"routing_eval\":\"absent\",\"stability\":\"stable\",\"keywords\":\"[\\\\\\\"rls\\\\\\\",\\\\\\\"row-level-security\\\\\\\",\\\\\\\"postgres\\\\\\\",\\\\\\\"tenant-isolation\\\\\\\",\\\\\\\"org-id\\\\\\\",\\\\\\\"security-policy\\\\\\\",\\\\\\\"set-local\\\\\\\",\\\\\\\"view-bypass\\\\\\\",\\\\\\\"migration\\\\\\\",\\\\\\\"multi-tenant\\\\\\\",\\\\\\\"ENABLE ROW LEVEL SECURITY\\\\\\\",\\\\\\\"FORCE ROW LEVEL SECURITY\\\\\\\",\\\\\\\"security_invoker\\\\\\\",\\\\\\\"USING clause\\\\\\\",\\\\\\\"WITH CHECK\\\\\\\",\\\\\\\"superuser bypass\\\\\\\",\\\\\\\"orgQuery\\\\\\\",\\\\\\\"app.organization_id\\\\\\\",\\\\\\\"connection pool safety\\\\\\\",\\\\\\\"materialized view RLS\\\\\\\"]\",\"examples\":\"[\\\\\\\"adding RLS to a new table — what statements are required and in what order?\\\\\\\",\\\\\\\"auditing our existing RLS migrations for missing FORCE or WITH CHECK\\\\\\\",\\\\\\\"implementing a view on an RLS-protected table in PostgreSQL 15+\\\\\\\",\\\\\\\"debugging a cross-tenant data leak in a multi-tenant SaaS system\\\\\\\",\\\\\\\"ensuring connection pool context (SET LOCAL) does not leak tenant state between requests\\\\\\\",\\\\\\\"reviewing a migration that enables RLS to check for superuser and owner bypass risks\\\\\\\",\\\\\\\"verifying that materialized views over RLS tables are documented as security-sensitive\\\\\\\"]\",\"anti_examples\":\"[\\\\\\\"implementing application-level auth guards (requireAuth, requireOrgAuth) — use nextauth-patterns\\\\\\\",\\\\\\\"choosing when to use orgQuery() vs query() in application code — use multi-tenancy-rls\\\\\\\",\\\\\\\"implementing CSRF protection or webhook HMAC verification — use security-scanning\\\\\\\",\\\\\\\"designing the overall multi-tenant data architecture — use data-architect\\\\\\\",\\\\\\\"designing row-level access control in non-PostgreSQL databases\\\\\\\"]\",\"relations\":\"{\\\\\\\"adjacent\\\\\\\":[\\\\\\\"database-migration\\\\\\\",\\\\\\\"security-scanning\\\\\\\",\\\\\\\"data-architect\\\\\\\",\\\\\\\"guardrails\\\\\\\"],\\\\\\\"boundary\\\\\\\":[{\\\\\\\"skill\\\\\\\":\\\\\\\"nextauth-patterns\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"nextauth-patterns owns application-level authorization (requireAuth, requireOrgAuth, withOrgAuth); postgres-rls owns database-level isolation via PostgreSQL RLS policies\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"multi-tenancy-rls\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"multi-tenancy-rls owns the application query tier (orgQuery, query, withAppSession usage patterns); postgres-rls owns the PostgreSQL server-side RLS policy implementation\\\\\\\"}],\\\\\\\"verify_with\\\\\\\":[\\\\\\\"security-scanning\\\\\\\",\\\\\\\"database-migration\\\\\\\"]}\",\"grounding\":\"{\\\\\\\"domain_object\\\\\\\":\\\\\\\"PostgreSQL Row Level Security implementation in Sales Hub\\\\\\\",\\\\\\\"grounding_mode\\\\\\\":\\\\\\\"repo_specific\\\\\\\",\\\\\\\"truth_sources\\\\\\\":[\\\\\\\"sales-hub/apps/web/src/lib/db.ts\\\\\\\",\\\\\\\"sales-hub/db/migrations/20260218_rls_hardening.sql\\\\\\\",\\\\\\\"sales-hub/db/migrations/20260314_rls_expansion.sql\\\\\\\",\\\\\\\"sales-hub/db/migrations/20260314_rls_with_check_and_security_invoker.sql\\\\\\\",\\\\\\\"sales-hub/db/migrations/20260315_enable_rls_all.sql\\\\\\\"],\\\\\\\"failure_modes\\\\\\\":[\\\\\\\"security_leak\\\\\\\",\\\\\\\"incorrect_isolation\\\\\\\",\\\\\\\"missing_force_rls\\\\\\\",\\\\\\\"missing_with_check\\\\\\\",\\\\\\\"superuser_bypass\\\\\\\",\\\\\\\"connection_pool_context_leakage\\\\\\\",\\\\\\\"view_security_invoker_missing\\\\\\\"],\\\\\\\"evidence_priority\\\\\\\":\\\\\\\"repo_code_first\\\\\\\"}\",\"portability\":\"{\\\\\\\"readiness\\\\\\\":\\\\\\\"declared\\\\\\\",\\\\\\\"targets\\\\\\\":[\\\\\\\"skill-md\\\\\\\"]}\",\"lifecycle\":\"{\\\\\\\"stale_after_days\\\\\\\":90,\\\\\\\"review_cadence\\\\\\\":\\\\\\\"quarterly\\\\\\\"}\",\"skill_graph_source_repo\":\"https://github.com/jacob-balslev/skill-graph\",\"skill_graph_protocol\":\"Skill Metadata Protocol v6\",\"skill_graph_project\":\"Skill Graph\",\"skill_graph_canonical_skill\":\"skills/postgres-rls/SKILL.md\"}"
  skill_graph_source_repo: "https://github.com/jacob-balslev/skill-graph"
  skill_graph_protocol: Skill Metadata Protocol v4
  skill_graph_project: Skill Graph
  skill_graph_canonical_skill: skills/postgres-rls/SKILL.md
---

# PostgreSQL Row Level Security

## Domain Context

**What is postgres-rls?** Guides agents implementing or auditing PostgreSQL Row Level Security in Sales Hub. Covers ENABLE+FORCE pairing, USING+WITH CHECK policies, view bypass via security_invoker, SET LOCAL for connection pool safety, superuser/owner bypass detection, and materialized view risks.

## Key Files

| File | Purpose |
|------|------|
| `apps/web/src/lib/db.ts` | orgQuery(), query(), withReportingCurrency(), withAppSession() wrapper pattern (lines 1-895) |
| `db/migrations/20260218_rls_hardening.sql` | RLS hardening migration — ENABLE+FORCE patterns |
| `db/migrations/20260314_rls_expansion.sql` | RLS expansion to additional tables |
| `db/migrations/20260314_rls_with_check_and_security_invoker.sql` | WITH CHECK and security_invoker additions |
| `db/migrations/20260315_enable_rls_all.sql` | Full RLS enablement across all tables |

## Project-Specific Rules

This skill captures project-local rules and constraints that narrow or refine a broader pattern. Treat the repo-specific guidance and key files below as authoritative for this project.

Sales Hub uses `org_id` (not `tenant_id`) as the tenant column. Session variable is `app.organization_id`. All application queries go through `orgQuery()` (auto-sets session variable) or `query()` (system-only, bypasses RLS). The `db.ts` module manages a connection pool via `pg.Pool`; RLS context is set per-transaction using `set_config('app.organization_id', orgId, true)` (the third parameter `true` makes it transaction-local, equivalent to `SET LOCAL`).

## Coverage

This skill covers PostgreSQL Row Level Security implementation and auditing in Sales Hub: ENABLE+FORCE pairing, USING+WITH CHECK policies, view bypass via security_invoker, SET LOCAL for connection pool safety, superuser/owner bypass detection, materialized view risks, the `orgQuery()` wrapper pattern, and the `app.organization_id` session variable convention.

## Philosophy

RLS is the last line of defense against cross-tenant data leaks. When agents implement it incorrectly (missing FORCE, missing WITH CHECK, using SET instead of SET LOCAL), the system appears to work in testing but silently leaks data in production. This skill captures the exact footguns that have caused or nearly caused data breaches in multi-tenant SaaS systems.

## Overview

Row Level Security (RLS) provides defense-in-depth for data isolation. When implemented correctly, it prevents data leaks even if application code misses a filter. When implemented incorrectly, it creates false security confidence while data bleeds between tenants.

**Core principle:** RLS is your last line of defense, not your only one. Get it wrong and you have a data breach.

**Announce at start:** "I'm applying postgres-rls to verify Row Level Security implementation."

## When This Skill Applies

This skill is MANDATORY when ANY of these patterns are touched:

| Pattern | Examples |
|---------|----------|
| `**/migrations/**/*tenant*` | migrations/001_add_tenant_id.sql |
| `**/migrations/**/*rls*` | migrations/005_enable_rls.sql |
| `**/migrations/**/*policy*` | migrations/010_create_policies.sql |
| `**/*policy*.sql` | db/policies.sql |
| `**/auth/**` | src/auth/context.ts |
| `**/*tenant*` | lib/tenant.ts, services/tenantService.ts |
| `**/*multi-tenant*` | docs/multi-tenant-architecture.md |

Check with:
```bash
git diff --name-only HEAD~1 | grep -iE '(tenant|rls|policy|auth.*sql|multi.?tenant)'
```

## Sales Hub Specifics

Sales Hub uses `org_id` (not `tenant_id`) as the tenant column. Session variable is `app.organization_id`.

**Current state (2026-03-14):** 22 tables with RLS. Policies use:
```sql
CREATE POLICY {table}_org_isolation ON {table}
  FOR ALL
  USING (org_id IS NOT NULL AND org_id = (current_setting('app.organization_id', true))::uuid)
  WITH CHECK (org_id IS NOT NULL AND org_id = (current_setting('app.organization_id', true))::uuid);
```

**Query wrappers (in `apps/web/src/lib/db.ts` — orgQuery, query, withAppSession):**
- `orgQuery(orgId, sql, params)` — auto-sets session variable + validates (preferred)
- `query(sql, params)` — raw query without validation (system operations only)
- `withAppSession(settings, fn)` — manual session variable injection

**Views:** All views use `ALTER VIEW ... SET (security_invoker = true)` (PG15+).

## The Critical Vulnerabilities

### 1. Superuser Bypass (CRITICAL)

Superusers and roles with `BYPASSRLS` ignore ALL policies.

```sql
-- DANGEROUS: Testing as superuser shows RLS "working" when it's bypassed
SET ROLE postgres;
SELECT * FROM orders;  -- Returns ALL rows, RLS ignored

-- CORRECT: Test as application role
SET ROLE app_user;
SELECT * FROM orders;  -- Returns only permitted rows
```

**Checklist:**
- [ ] Application connects as non-superuser role
- [ ] No roles have `BYPASSRLS` attribute
- [ ] Tests run as application role, NOT superuser

### 2. Table Owner Bypass (CRITICAL)

Table owners bypass RLS unless `FORCE ROW LEVEL SECURITY` is set.

```sql
-- INCOMPLETE: Owners bypass this
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- COMPLETE: Everyone including owners must obey policies
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;
```

**Checklist:**
- [ ] All RLS tables have both ENABLE and FORCE
- [ ] Migration includes both statements

### 3. View Bypass (CRITICAL)

Views run with creator's privileges by default. Views owned by superusers bypass RLS entirely.

```sql
-- DANGEROUS: View owned by superuser bypasses RLS
CREATE VIEW all_orders AS SELECT * FROM orders;

-- SAFE (PostgreSQL 15+): Security invoker respects caller's RLS
CREATE VIEW user_orders
WITH (security_invoker = true)
AS SELECT * FROM orders;

-- Or retrofit existing views:
ALTER VIEW user_orders SET (security_invoker = true);
```

**Checklist:**
- [ ] All views on RLS tables use `security_invoker = true` (PG15+)
- [ ] Views not owned by superuser roles
- [ ] Materialized views documented as bypassing RLS

### 4. USING vs WITH CHECK Mismatch (HIGH)

`USING` filters reads; `WITH CHECK` validates writes. Missing `WITH CHECK` allows inserting data you can't see.

```sql
-- INCOMPLETE: User can INSERT rows they can't SELECT
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- COMPLETE: Both read and write protected
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id')::uuid)
  WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
```

**Checklist:**
- [ ] All policies have both USING and WITH CHECK
- [ ] WITH CHECK logic matches security intent

### 5. Thread-Local Context Leakage (HIGH)

Connection pooling can leak tenant context between requests.

```sql
-- DANGEROUS: Context persists across pooled connections
SET app.tenant_id = 'tenant-123';

-- SAFE: Use SET LOCAL inside transaction (auto-resets)
BEGIN;
SET LOCAL app.tenant_id = 'tenant-123';
-- ... queries ...
COMMIT;  -- Context automatically cleared
```

**Application pattern:**
```typescript
// DANGEROUS: Leaks between requests
await db.query(`SET app.tenant_id = '${tenantId}'`);

// SAFE: Transaction-scoped context (Sales Hub pattern)
await client.query("SELECT set_config('app.organization_id', $1, true)", [orgId]);
// The `true` parameter = transaction-local, equivalent to SET LOCAL
```

**Checklist:**
- [ ] Always use `SET LOCAL` or `set_config(key, val, true)`
- [ ] Context set inside transactions
- [ ] Post-request handler resets context (defense in depth)

### 6. SQL Injection in Policy Functions (HIGH)

Functions used in policies can be injection vectors.

```sql
-- The function must be injection-safe:
CREATE OR REPLACE FUNCTION current_tenant()
RETURNS uuid AS $$
BEGIN
  -- SAFE: Casts to UUID, not string concatenation
  RETURN current_setting('app.tenant_id')::uuid;
END;
$$ LANGUAGE plpgsql STABLE;
```

### 7. Materialized Views and Data Export (MEDIUM)

Materialized views don't respect source table RLS. Data exports may bypass policies.

**Checklist:**
- [ ] Materialized views documented as security-sensitive
- [ ] Export jobs run as application role
- [ ] Audit log for bulk data access

## Migration Pattern

### Safe RLS Migration

```sql
-- Step 1: Add column (if needed)
ALTER TABLE orders ADD COLUMN IF NOT EXISTS org_id uuid REFERENCES organizations(id);

-- Step 2: Backfill data (batched for large tables)
UPDATE orders SET org_id = (...) WHERE org_id IS NULL;

-- Step 3: Create index
CREATE INDEX IF NOT EXISTS idx_orders_org_id ON orders(org_id);

-- Step 4: Enable RLS (both statements!)
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;

-- Step 5: Create policies with USING and WITH CHECK
DROP POLICY IF EXISTS orders_org_isolation ON orders;
CREATE POLICY orders_org_isolation ON orders
  FOR ALL
  USING (org_id IS NOT NULL AND org_id = (current_setting('app.organization_id', true))::uuid)
  WITH CHECK (org_id IS NOT NULL AND org_id = (current_setting('app.organization_id', true))::uuid);

-- Step 6: Verify
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'orders' AND policyname = 'orders_org_isolation') THEN
    RAISE EXCEPTION 'ASSERTION FAILED: RLS policy not found on orders';
  END IF;
END; $$;
```

## Verification

Before completing RLS implementation:

- [ ] All tables have ENABLE and FORCE ROW LEVEL SECURITY
- [ ] All policies have both USING and WITH CHECK
- [ ] Application connects as non-superuser, non-BYPASSRLS role
- [ ] Context set with SET LOCAL / set_config(key, val, true) inside transactions
- [ ] Views use security_invoker = true (PG15+)
- [ ] Policy columns indexed
- [ ] Cross-tenant isolation tests passing

## References

- [PostgreSQL RLS Documentation](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [Common RLS Footguns](https://www.bytebase.com/blog/postgres-row-level-security-footguns/)
- [RLS Performance Optimization](https://scottpierce.dev/posts/optimizing-postgres-rls/)


## Do NOT Use When

| Instead of this skill | Use | Why |
|---|---|---|
| Application-level auth logic | `nextauth-patterns` | RLS is DB-level; app auth is a separate layer |
| Non-PostgreSQL databases | General security patterns | RLS is PostgreSQL-specific |
| orgQuery() wrapper usage questions | `multi-tenancy-rls` | That skill owns the application query tier |
