---
name: supabase-projects
description: >
  This skill should be used when managing Supabase projects or organizations, creating new projects,
  listing projects, checking project status, retrieving API keys, pausing or restoring projects,
  or working with project costs and billing.
  Trigger when: "create Supabase project", "list Supabase projects", "Supabase API keys",
  "pause project", "restore project", "Supabase organization", "project cost",
  "get project URL", "publishable key", "secret key", "anon key", "service role key",
  "asymmetric JWT", "JWT signing keys", "key rotation",
  "supabase link", "project settings", or managing Supabase project lifecycle.
---

# Supabase Project Management

Guidance for managing Supabase projects and organizations using the MCP tools and CLI.

## Project Lifecycle

### Creating a Project (MCP)

Creating a project via MCP requires a cost confirmation flow. This is enforced by the MCP server — you cannot skip it.

1. **List organizations** to find the target org:
   ```
   mcp__supabase__list_organizations
   ```

2. **Get cost estimate** — always ask the user which organization:
   ```
   mcp__supabase__get_cost(type: "project", organization_id: "<org_id>")
   ```

3. **Confirm cost** with the user — repeat the cost and get explicit confirmation:
   ```
   mcp__supabase__confirm_cost(type: "project", recurrence: "monthly", amount: <amount>)
   ```

4. **Create the project** — returns a project that takes minutes to initialize:
   ```
   mcp__supabase__create_project(
     name: "my-project",
     region: "us-east-1",
     organization_id: "<org_id>",
     confirm_cost_id: "<cost_id>"
   )
   ```

5. **Check initialization status** by polling:
   ```
   mcp__supabase__get_project(id: "<project_id>")
   ```

### Available Regions

`us-west-1`, `us-east-1`, `us-east-2`, `ca-central-1`, `eu-west-1`, `eu-west-2`, `eu-west-3`, `eu-central-1`, `eu-central-2`, `eu-north-1`, `ap-south-1`, `ap-southeast-1`, `ap-northeast-1`, `ap-northeast-2`, `ap-southeast-2`, `sa-east-1`

Choose the region closest to the application's primary user base.

## API Keys (April 2026)

Supabase ships **two distinct key models**. New projects use the modern model; older projects still support the legacy model.

### Modern model (default for new projects)

| Key | Format | Where it goes | RLS |
|-----|--------|---------------|-----|
| **Publishable key** | `sb_publishable_<rand>` | Browser, mobile clients, public-facing code | Enforced |
| **Secret key** | `sb_secret_<rand>` | Edge Functions, server-only routes, admin scripts | **Bypasses RLS** |

Drop-in replacements anywhere `anon` / `service_role` were used; all client libraries accept them with no code change. Secret keys are hidden by default in the dashboard, audit-logged, and can be rotated independently from JWT signing keys.

### Legacy model

| Key | Format | Status |
|-----|--------|--------|
| **Anon key** | JWT (`eyJ...`) signed with project's HS256 secret | Still works; new projects should prefer publishable keys |
| **Service role key** | JWT (`eyJ...`) signed with project's HS256 secret | Still works; bypasses RLS |

**Key end-of-life:** Projects restored after **Nov 1, 2025** no longer get legacy keys at all. Existing projects retain them for backward compatibility; an exact deprecation date has not been announced. Migrate when convenient — both formats coexist on the same project.

### Asymmetric JWT signing (default since May 1, 2025)

New projects sign JWTs with **ES256 or RS256** (asymmetric), exposing a JWKS endpoint at `https://<project>.supabase.co/auth/v1/.well-known/jwks.json`. Server-side code verifies tokens by fetching the JWKS — no shared secret required. Projects created before May 1, 2025 still use HS256 unless migrated; the dashboard offers a one-click upgrade.

### Retrieving Keys (MCP)

```
mcp__supabase__get_publishable_keys(project_id: "...")
```

Returns both legacy anon keys (JWT-based, if the project still has them) and modern publishable keys (`sb_publishable_*`). **Note:** the older tool `get_anon_key` was removed in MCP server v0.5.9 (Oct 2025) — always use `get_publishable_keys`.

**Important:** Only use keys where `disabled` is `false` or undefined.

### Retrieving Project URL (MCP)

```
mcp__supabase__get_project_url(project_id: "...")
```

Returns the API URL: `https://<project-ref>.supabase.co`

### Via CLI

After linking a project, keys and URLs are available via:
```bash
supabase status   # Shows local URLs and keys
```

For remote keys, use the dashboard or `get_publishable_keys` MCP tool.

## Listing and Inspecting Projects

### Via MCP
```
mcp__supabase__list_projects          # All projects
mcp__supabase__get_project(id: "...")  # Single project details
```

### Via CLI
```bash
supabase projects list                # List all projects
supabase link --project-ref <id>      # Link local to remote project
```

## Organization Management

### List Organizations (MCP)
```
mcp__supabase__list_organizations
```

### Get Organization Details (MCP)
```
mcp__supabase__get_organization(id: "...")
```
Returns organization details including the subscription plan (Free, Pro, Team, Enterprise).

### Via CLI
```bash
supabase orgs list
```

## Pausing and Restoring Projects

Free-tier projects automatically pause after inactivity. Pro/Team/Enterprise projects can be manually paused.

### Pause (MCP)
```
mcp__supabase__pause_project(project_id: "...")
```

### Restore (MCP)
```
mcp__supabase__restore_project(project_id: "...")
```

Restoring a paused project takes a few minutes. Poll `get_project` to check status.

**Restore caveat:** projects restored after **Nov 1, 2025** no longer issue legacy `anon` / `service_role` keys. If your codebase still references those env vars, switch to `sb_publishable_*` / `sb_secret_*` before restoring or the restore will leave you without working keys.

## Linking Local to Remote

The CLI uses `link` to associate a local project with a remote Supabase project:

```bash
supabase link --project-ref <project-id>
```

The project ID is found in the dashboard URL: `https://supabase.com/dashboard/project/<project-id>`

After linking:
- `supabase db push` pushes migrations to the linked project
- `supabase db pull` pulls the remote schema
- `supabase functions deploy` deploys to the linked project

## Cost Awareness

Always follow this protocol when creating projects or branches:

1. Call `get_cost` first — never assume costs across organizations
2. Present the cost clearly to the user
3. Wait for explicit confirmation
4. Pass the `confirm_cost_id` to the create operation

This applies to both `create_project` and `create_branch` operations.

## MCP Server Modes (`@supabase/mcp-server-supabase` v0.7+)

The Supabase MCP server supports flags that change which tools are available:

- `--read-only` — `execute_sql` runs as a read-only Postgres role; **all mutating tools are disabled** (`apply_migration`, `create_project`, `pause_project`, `restore_project`, `deploy_edge_function`, all branch mutations, `update_storage_config`). Recommended default.
- `--project-ref <id>` — scopes the server to one project; account-level tools (`list_projects`, `create_project`, `list_organizations`, etc.) are disabled. Useful when you only operate on one project.
- `--features=<list>` — enables tool groups beyond defaults. Storage tools (`list_storage_buckets`, `get_storage_config`, `update_storage_config`) are off by default; enable with `--features=database,docs,storage`.

**Authentication:**
- Hosted MCP (`mcp.supabase.com/mcp`) uses OAuth 2.1 (browser flow).
- Self-hosted (`npx @supabase/mcp-server-supabase`) uses a Personal Access Token via `SUPABASE_ACCESS_TOKEN` env var or `--access-token` flag.

## CLI vs MCP Decision Matrix

| Task | Use CLI | Use MCP |
|------|---------|---------|
| Create project | When scripting CI/CD | Interactive Claude Code session |
| List projects | Quick terminal check | When operating on results programmatically |
| Get API keys | `supabase status` (local) | `get_publishable_keys` (remote) |
| Pause/restore | Not available in CLI | Always use MCP |
| Link project | Always CLI | Not applicable |
| Organization info | `supabase orgs list` | `get_organization` for subscription details |
