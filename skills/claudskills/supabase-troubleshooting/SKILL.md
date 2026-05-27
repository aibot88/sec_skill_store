---
name: supabase-troubleshooting
description: >
  This skill should be used when debugging Supabase issues, viewing logs, running performance
  advisors, diagnosing common errors, or searching Supabase documentation for solutions.
  Trigger when: "Supabase logs", "debug Supabase", "Supabase error", "performance issue",
  "slow query", "connection error", "Supabase not working", "function error",
  "auth error", "storage error", "realtime issue", "Supabase troubleshooting",
  "search Supabase docs", "inspect database", "performance advisor",
  "db lint", "diagnose Supabase", or resolving any Supabase operational issue.
---

# Supabase Troubleshooting

Guidance for debugging issues, viewing logs, running advisors, and searching documentation using MCP tools and CLI.

## Viewing Logs (MCP)

The `get_logs` tool retrieves logs from the last 24 hours by service:

```
mcp__supabase__get_logs(project_id: "<id>", service: "<service>")
```

### Available Services

| Service | What It Captures |
|---------|-----------------|
| `api` | PostgREST API requests, errors, response codes |
| `postgres` | Database queries, errors, slow queries, connection issues |
| `edge-function` | Edge Function invocations, runtime errors, timeouts |
| `auth` | Sign-in attempts, token issues, provider errors |
| `storage` | File operations, upload/download errors, policy denials |
| `realtime` | WebSocket connections, channel subscriptions, broadcast |
| `branch-action` | Branch operations (create, merge, rebase, reset) |

### Debugging Strategy

Start with the service most relevant to the issue:

1. **API errors (4xx/5xx)** → Check `api` logs for PostgREST errors
2. **Query failures** → Check `postgres` logs for SQL errors
3. **Function crashes** → Check `edge-function` logs for runtime errors
4. **Login failures** → Check `auth` logs for provider/token issues
5. **File access denied** → Check `storage` logs for policy violations
6. **Connection drops** → Check `realtime` logs for WebSocket issues

## Security Advisors (MCP)

```
mcp__supabase__get_advisors(project_id: "<id>", type: "security")
```

The advisor runs Supabase's [Splinter lint catalog](https://supabase.github.io/splinter/) against the live database. Common security lint codes you'll see:

| Code | Name | Catches |
|------|------|---------|
| 0002 | `auth_users_exposed` | Views in non-internal schemas selecting from `auth.users` |
| 0007 | `policy_exists_rls_disabled` | Policies defined on a table where RLS is disabled |
| 0008 | `rls_enabled_no_policy` | Table with RLS enabled and zero policies |
| 0010 | `security_definer_view` | Views with SECURITY DEFINER (privilege escalation risk) |
| 0011 | `function_search_path_mutable` | SECURITY DEFINER functions without `set search_path` |
| 0013 | `rls_disabled_in_public` | Public-schema tables without RLS |
| 0015 | `rls_references_user_metadata` | Policies reading `raw_user_meta_data` (user-writable) |
| 0017 | `foreign_table_in_api` | Foreign tables exposed via the auto-generated API |
| 0019 | `insecure_queue_exposed_in_api` | pg_mq queues exposed via the API |

The advisor also surfaces performance lints (e.g. `0001 unindexed_foreign_keys`, `0003 auth_rls_initplan`, `0006 multiple_permissive_policies`) when called with `type: "performance"`.

**Include remediation URLs as clickable links** in responses — each lint has a dedicated docs page at `https://supabase.github.io/splinter/<code>_<name>/`.

**Static counterpart:** for the lints that can be detected without a live database (0002, 0003, 0008, 0011, 0013, 0015), run `python scripts/audit-rls.py` against your migration files. Useful in CI before push.

## Performance Advisors (MCP)

```
mcp__supabase__get_advisors(project_id: "<id>", type: "performance")
```

Returns performance advisory notices:
- Missing indexes on frequently queried columns
- Bloated tables needing VACUUM
- Unused indexes consuming space
- Slow query patterns

**Run after DDL changes** to catch performance regressions early.

## Searching Documentation (MCP)

The `search_docs` tool queries Supabase's documentation via GraphQL:

```
mcp__supabase__search_docs(
  graphql_query: "{ searchDocs(query: \"<search terms>\", limit: 5) { nodes { title href content } } }"
)
```

### Effective Search Queries

| Issue | Search Query |
|-------|-------------|
| RLS not working | `"Row Level Security policy not applied"` |
| Auth redirect issue | `"OAuth redirect URL configuration"` |
| Edge function timeout | `"edge function timeout limit configuration"` |
| Connection pooling | `"connection pooling pgbouncer supavisor"` |
| Migration errors | `"migration repair conflict resolution"` |
| Realtime not receiving | `"realtime subscription not receiving changes"` |

### Advanced GraphQL Queries

Search with subsections for deeper results:
```graphql
{
  searchDocs(query: "connection pooling", limit: 3) {
    nodes {
      title
      href
      content
      ... on Guide {
        subsections {
          nodes {
            title
            content
          }
        }
      }
    }
  }
}
```

Search for CLI command references:
```graphql
{
  searchDocs(query: "supabase db push", limit: 3) {
    nodes {
      title
      href
      ... on CLICommandReference {
        content
      }
    }
  }
}
```

Look up specific error codes:
```graphql
{
  error(code: "user_already_exists", service: AUTH) {
    code
    service
    httpStatusCode
    message
  }
}
```

## CLI Diagnostic Tools

### Database Linting

```bash
supabase db lint
```

Checks the schema for common issues: missing primary keys, unindexed foreign keys, naming inconsistencies.

### Database Inspection

```bash
supabase inspect db calls           # Most frequently called queries
supabase inspect db long-running    # Long-running queries
supabase inspect db outliers        # Queries with worst time/calls ratio
supabase inspect db bloat           # Table bloat estimates
supabase inspect db cache-hit       # Buffer cache hit ratios
supabase inspect db index-usage     # Index utilization
supabase inspect db locks           # Current lock contention
supabase inspect db replication-slots  # Replication slot status
supabase inspect db role-connections   # Connection counts per role
supabase inspect db seq-scans       # Tables with high sequential scans
supabase inspect db table-sizes     # Table size breakdown
supabase inspect db unused-indexes  # Indexes that are never used
supabase inspect db vacuum-stats    # Last vacuum/analyze timestamps
```

### Local Stack Diagnostics

```bash
supabase status     # Show all local service URLs and health
supabase stop       # Stop and optionally reset local stack
supabase start      # Restart local stack
```

## Common Issues and Solutions

### "Permission Denied" on Table Access

**Cause:** RLS is enabled but no policy grants access for the user's role.

**Diagnosis:**
1. Check RLS status: `SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';`
2. Check policies: `SELECT * FROM pg_policies WHERE tablename = '<table>';`
3. Run security advisor: `get_advisors(type: "security")`

**Fix:** Create appropriate RLS policies for the table.

### Edge Function Returns 500

**Diagnosis:**
1. Check function logs: `get_logs(service: "edge-function")`
2. Check if secrets are set: `supabase secrets list`
3. Test locally: `supabase functions serve`

**Common causes:**
- Missing environment variable / secret
- Unhandled exception in function code
- Incorrect import path or missing dependency
- JWT verification failure (check `verify_jwt` setting)

### Slow Queries

**Diagnosis:**
1. Run performance advisor: `get_advisors(type: "performance")`
2. Check for missing indexes
3. Use `EXPLAIN ANALYZE` via `execute_sql`

```sql
EXPLAIN ANALYZE SELECT * FROM public.posts WHERE author_id = '<uuid>';
```

**Fix:** Add indexes on columns used in WHERE clauses, JOINs, and RLS policies.

### Auth Provider Not Working

**Diagnosis:**
1. Check auth logs: `get_logs(service: "auth")`
2. Verify provider configuration in Dashboard
3. Check redirect URLs match exactly

**Common causes:**
- Mismatched redirect URLs
- Invalid client ID/secret
- Missing scopes for the provider

### Realtime Not Receiving Updates

**Diagnosis:**
1. Check realtime logs: `get_logs(service: "realtime")`
2. Verify RLS policies allow the subscription
3. Verify the table has `REPLICA IDENTITY FULL` if needed

```sql
ALTER TABLE public.messages REPLICA IDENTITY FULL;
```

### Migration Push Fails

**Diagnosis:**
1. List applied migrations: `list_migrations`
2. Check for conflicts with `supabase db diff`
3. Verify migration SQL is valid

**Common causes:**
- Migration already applied (different hash)
- Dependency ordering issue
- Syntax error in SQL

**Fix:** Use `supabase migration repair` to fix migration history, or write a corrective migration.

## Diagnostic Workflow

For any Supabase issue, follow this sequence:

1. **Identify the service** — Which Supabase component is involved?
2. **Check logs** — `get_logs` for the relevant service
3. **Run advisors** — `get_advisors` for security and performance
4. **Search docs** — `search_docs` for the specific error or pattern
5. **Test locally** — Reproduce the issue with `supabase start` if possible
6. **Inspect database** — Use `supabase inspect db` commands for deep analysis
