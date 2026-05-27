---
name: write-path-mapping
description: Map the write path of a project across multiple frameworks — entry points, validation, auth, persistence, side-effects. Outputs report, Mermaid diagrams, JSON sidecar. Flags unauth writes, missing RLS, cache gaps. Use for write path, mutation audit, RLS audit.
argument-hint: [target-directory-or-package]
allowed-tools: Read Grep Glob Write Edit Bash(git:*, ls:*, wc:*, find:*, cat:*, mkdir:*, test:*) Agent
effort: high
---

# Write Path Mapping

ultrathink

<!-- anthril-output-directive -->
> **Output path directive (canonical — overrides in-body references).**
> All file outputs from this skill MUST be written under `.anthril/reports/write-path-mapping/`.
> Run `mkdir -p .anthril/reports/write-path-mapping` before the first `Write` call.
> Primary artefact: `.anthril/reports/write-path-mapping/<artefact>`.
> Do NOT write to the project root or to bare filenames at cwd.
> Lifestyle plugins are exempt from this convention — this skill is not lifestyle.

## Before You Start

1. **Locate the target.** Use `$ARGUMENTS` if provided, otherwise the current working directory. If neither resolves to a real directory, ask the user for the target path before continuing.
2. **Detect the stack.** Run `scripts/detect-stack.sh` to identify languages, frameworks, and monorepo layout. This determines which framework matrix to apply in Phase 2.
3. **Detect the persistence layer.** Run `scripts/detect-db.sh` to identify Supabase, Prisma, Drizzle, TypeORM, SQLAlchemy, Django ORM, ActiveRecord, Eloquent, Doctrine, Redis, etc. This determines which mutation matrix to apply in Phase 5.
4. **Check tooling availability.** Run `scripts/check-tools.sh`. Missing tools degrade depth but never abort the mapping — ripgrep is the only strongly recommended tool.
5. **Load `.write-path-ignore`.** If the target contains this file, parse it and treat entries as suppression rules during Phase 8.
6. **Map project structure.** Inventory the codebase excluding `node_modules/`, `.venv/`, `venv/`, `target/`, `dist/`, `build/`, `.next/`, `.nuxt/`, `coverage/`, `.git/`, `.turbo/`.

## User Context

$ARGUMENTS

Detected stack: !`bash "${CLAUDE_PLUGIN_ROOT}/skills/write-path-mapping/scripts/detect-stack.sh" .`

Detected persistence: !`bash "${CLAUDE_PLUGIN_ROOT}/skills/write-path-mapping/scripts/detect-db.sh" .`

Tool availability: !`bash "${CLAUDE_PLUGIN_ROOT}/skills/write-path-mapping/scripts/check-tools.sh" .`

Candidate write entries (fast ripgrep seed): !`bash "${CLAUDE_PLUGIN_ROOT}/skills/write-path-mapping/scripts/find-write-endpoints.sh" .`

---

## Mapping Phases

Execute every phase in order. For each path, record: entry (type, file, line, verb, route, framework), middleware chain, validator, auth layer, handler, persistence targets, fan-out count, downstream effects, risks, verification depth. Use the rubric in `${CLAUDE_PLUGIN_ROOT}/skills/write-path-mapping/reference.md` §7 for completeness scoring. Never skip a phase — mark as `N/A` if genuinely not applicable to the detected stack.

**Read-only guarantee.** This skill never modifies source files. It emits three new artifacts into the target project:

- `write-path-map.md` — the main report
- `write-path-map.json` — the JSON sidecar
- `risk-register.md` — the standalone risk register

**Completeness, not quality.** The completeness score measures how thoroughly the skill traced the system, NOT how good the system is. A clean codebase and a messy codebase can both score 100%. System quality is captured separately in the Risk Register.

---

### Phase 1: Discovery & Inventory (context only — no score)

**Objective:** Build an accurate picture of the codebase and its persistence layer before any mapping begins.

1. Read top-level config: `package.json`, `pyproject.toml` / `setup.py` / `requirements*.txt`, `go.mod`, `Cargo.toml`, `pom.xml` / `build.gradle*`, `composer.json`, `Gemfile`, `*.csproj` / `*.sln`.
2. Detect monorepo layout: `pnpm-workspace.yaml`, `lerna.json`, `nx.json`, `turbo.json`, `Cargo.toml [workspace]`, `go.work`, `rush.json`. Each package becomes a mapping target.
3. Run `scripts/extract-schema.sh` to collect tables, columns, and schema file inventory.
4. Run `scripts/extract-triggers.sh` to collect `CREATE TRIGGER`, `CREATE FUNCTION`, and `CREATE POLICY` statements.
5. Run `scripts/extract-cron.sh` to collect scheduled job sources (BullMQ repeat, pg_cron, Celery beat, Rails whenever, GitHub Actions schedule, Vercel Cron, etc.).
6. Run `scripts/extract-queues.sh` to collect queue producers and consumers (BullMQ, SQS, Kafka, NATS, Celery, Sidekiq, Supabase queue, Cloudflare Queues).
7. **Live DB enrichment (optional):** run `scripts/live-db-probe.sh`. If Supabase MCP is configured or `DATABASE_URL` is set, enrich the schema data with live `pg_policies`, `pg_trigger`, and `information_schema` queries. **When Supabase MCP is available, prefer the `mcp__*Supabase__execute_sql` (SELECT only) and `mcp__*Supabase__list_tables` tools over psql.** If no live source is available, continue with static data.
8. Load `.write-path-ignore` if present. Surface unjustified entries and stale patterns as Phase 1 warnings.

This phase produces the context block at the top of the report. No completeness score of its own — phase 1 failures become adjustments to overall completeness.

---

### Phase 2: Entry-Point Discovery

**Objective:** Find every write entry point in the project.

1. Consume the seed list from `scripts/find-write-endpoints.sh` (already run in User Context).
2. Optionally run `python3 scripts/ast-entrypoints.py` for richer AST-level extraction. Its output is merged with the seed list via `scripts/normalize-findings.py`.
3. Classify every candidate using the taxonomy in `reference.md` §1.
4. **MANDATORY sub-agent sweep when >30 candidates.** Partition the seed list by top-level domain folder (e.g. `app/`, `src/api/`, `supabase/functions/`, `workers/`, each monorepo package) and spawn one `Agent(subagent_type=Explore)` per domain **in parallel** (multiple tool calls in one assistant message). Each sub-agent receives the prompt shape from `reference.md` §9 and returns a JSON array. Merge via `scripts/normalize-findings.py`.
5. Deduplicate by `(file, line, verb)`.
6. Drop entries that are clearly read-only (GET routes, pure-query GraphQL queries, reader RPCs).

Phase completeness = `traced_entries / discovered_candidates` × 100.

---

### Phase 3: Middleware & Auth Layer Capture

**Objective:** For every entry, capture the middleware chain and the auth layer.

1. For each entry, walk the router registration back to the framework bootstrap and record every `use()`, decorator, guard, `before_action`, `Depends(...)`, middleware alias, or firewall entry. Use the matrix in `reference.md` §5.
2. Resolve framework-specific auth: Next.js `middleware.ts`, NestJS `@UseGuards(AuthGuard)`, FastAPI `Depends(get_current_user)`, Django `@login_required` / permission classes, Rails `before_action :authenticate_user!`, Laravel `->middleware('auth')`, Symfony firewalls.
3. **Supabase RLS cross-reference.** For Supabase projects, run `scripts/rls-policy-check.sh` and intersect each write target table with the RLS policies discovered in Phase 1. Tables with no policy covering the relevant role become `missing-rls` candidates.
4. **Tentatively flag risks** (final resolution in Phase 7):
   - Entry with no resolvable auth layer → `unauth-write`
   - Webhook entry with no signature verification → `unverified-webhook`
   - Edge function using `SUPABASE_SERVICE_ROLE_KEY` to write on behalf of user input → `service-role-overreach`
5. Record the middleware chain in each path's `middleware` array.

Phase completeness = `entries_with_auth_layer_recorded / entries` × 100.

---

### Phase 4: Validator Detection

**Objective:** Confirm each entry validates its input.

1. Detect the project's validator libraries (Zod, Yup, Joi, class-validator, Valibot, ArkType, Pydantic, DRF serializers, Go struct tags, PHP voters, Rails strong parameters).
2. For each entry, walk the first N lines of the handler for a `.parse(...)`, `.validate(...)`, `@Body(new ValidationPipe())`, `class SomeDto`, `schema=ModelSerializer`, `request.validate(...)`, or struct-binding pattern.
3. Record the validator in `path.validator = { lib, schema, file, line }`. If none is found, tentatively flag `missing-validation` (confirmed in Phase 7).
4. Where possible, cross-reference validator fields against target table columns to detect fields accepted without validation.

Phase completeness = `entries_with_validator_recorded_or_confirmed_none / entries` × 100.

---

### Phase 5: Handler & Persistence Trace

**Objective:** For every entry, walk the handler into every persistence target.

1. For each handler, resolve imports transitively and enumerate every call matching the persistence matrix in `reference.md` §4. Start with `python3 scripts/ast-write-calls.py` on the handler file (and the files it imports). Record each target: `kind`, `target`, `file`, `line`.
2. Run `python3 scripts/transaction-boundary-check.py` on the handler file(s) and merge `in_transaction` flags into the target records.
3. **MANDATORY sub-agent sweep** when any of:
   - Project has >30 entries total.
   - Any single handler reaches 3+ service-layer hops (e.g. `route → service → repo → util`).
   - The stack is polyglot (JS frontend + Python worker + Go gateway).

   Partition handlers into **batches of 10** and spawn parallel `Agent(subagent_type=Explore)` calls. Each sub-agent receives the prompt shape from `reference.md` §9 Phase 5 and returns JSON per handler matching the `path` block of `templates/paths-schema.json`.

4. Merge all outputs via `scripts/normalize-findings.py`.
5. Count `fan_out_count = len(persistence_targets)` for every path.
6. Paths with zero targets are reclassified as read-only and dropped from the write map (surfaced in §11 Suppressed Paths).

Phase completeness = `entries_with_at_least_one_persistence_target / entries` × 100. Depth = `% of handlers where every delegate was resolved vs. stopped at dynamic dispatch`.

---

### Phase 6: Async / Fan-Out / DB-Side Effects

**Objective:** Map non-obvious writes that run after the initial handler returns.

1. **Queue fan-out.** For every `queue-publish` found in Phase 5, locate the consumer. If not found in the immediate directory, **spawn one sub-agent per unresolved queue** with the Phase 6 playbook prompt in `reference.md` §9. Cross-package search includes `../cloudflare-workers/`, `../workers/`, docker-compose services, and `supabase/functions/`. Record consumers as secondary entry points and run Phases 2–5 on them.
2. **Cron / scheduled jobs.** Using the `extract-cron.sh` output from Phase 1, treat every scheduled job as a secondary entry point and run Phases 2–5 on its handler.
3. **DB trigger chains.** For every table touched in Phase 5, look up triggers from the `extract-triggers.sh` output. For each trigger, record its target table(s) as `downstream_effects` of kind `db-trigger`. If there are >5 triggers on the project's schema, **spawn one sub-agent** to walk the full trigger graph.
4. **Domain events.** For every `event-emit` found in Phase 5, locate the subscribers. Record as `downstream_effects` of kind `event-subscriber`.
5. **Supabase realtime broadcasts.** For every `channel.send({type: 'broadcast'})` found, note the channel as a downstream effect.
6. **Orphan detection.** Queues with producers but no consumer → `orphan-queue-consumer` (HIGH). Consumers with no producer → `orphan-queue-publish` (LOW). Triggers referencing functions that no longer exist → `dead-trigger` (HIGH).

Phase completeness = `resolved_async_targets / discovered_async_targets` × 100.

---

### Phase 7: Risk Analysis

**Objective:** Walk every mapped path through the risk taxonomy and record evidence.

For each path, check every risk subtype from `reference.md` §6. Record evidence per flagged risk. Apply context-aware severity adjustments:

- **`unauth-write` on a path protected by RLS** → downgrade to HIGH. Note the RLS mitigation in evidence.
- **`missing-transaction` where only one persistence target exists** → suppress.
- **`missing-rls` confirmed via `rls-policy-check.sh`** → CRITICAL.
- **`cross-tenant-leak` detected when a Supabase/ORM write omits `workspace_id` (or equivalent) on a workspace-scoped table** → CRITICAL.
- **`dynamic-dispatch-write`** → always INFO. The skill cannot evaluate dynamic dispatch; the human reviewer must.
- **`fan-out-write` with ≥3 targets but all inside a transaction** → INFO. Without a transaction → HIGH.

**Deep-dive sub-agents (optional).** For any CRITICAL-flagged path with ≥3 middleware layers, spawn one `Agent(subagent_type=Explore)` to deep-verify the finding before publishing it. The sub-agent confirms whether a compensating control (RLS policy, signature verification, rate limit, tenancy filter) exists elsewhere in the chain and returns `{confirmed, evidence, severity_adjustment}`.

Phase completeness = `paths_with_all_risks_checked / paths` × 100.

---

### Phase 8: Reporting

**Objective:** Produce the final artifact set.

1. **Merge all findings.** Run `python3 scripts/normalize-findings.py` one final time to produce the unified `write-path-map.json` under the target project root.
2. **Render the main report.** Use `templates/output-template.md` as the structural skeleton. The report must include:
   - Header table (date, stack, persistence, totals, risks by severity, completeness, tier)
   - §1 Executive summary (top paths by fan-out, top risks, top data-domain hotspots)
   - §2 Stack & persistence
   - §3 Write paths by severity (CRITICAL/HIGH/MEDIUM/INFO/OK)
   - §4 Write paths by domain
   - §5 Per-endpoint detail blocks (top 20, ordered severity then fan-out)
   - §6 Data-domain write map (tables, caches, queues, external APIs, file stores)
   - §7 Risk register (inline copy)
   - §8 Suggested `.write-path-ignore` entries
   - §9 Visual artifacts (all four Mermaid diagrams)
   - §10 JSON sidecar pointer with example
   - §11 Suppressed paths
3. **Render the Mermaid diagrams.** Run `python3 scripts/mermaid-render.py write-path-map.json --out diagrams.md` and paste the four diagrams into §9 of the main report. All four are required:
   - A. System write flowchart
   - B. Per-endpoint sequence diagrams (top 20)
   - C. Data-domain write map (bipartite)
   - D. DB trigger / function graph
4. **Render the standalone risk register.** Use `templates/risk-register-template.md`. Write to `risk-register.md` alongside the main report. Cross-link from §7 of the main report.
5. **Write artifacts.** Using the `Write` tool, create `write-path-map.md`, `write-path-map.json`, and `risk-register.md` at the project root (or under `.claude/` if the project has one). Never overwrite an existing file without asking first.
6. **Emit completeness summary.** Print the final tier and score to the chat response. Surface any phase that scored <80% as a known gap the user should rerun.

Phase completeness = `required_report_sections_rendered / 11` × 100.

---

## Completeness Summary

| Phase | Focus | Weight |
|---|---|---|
| Phase 1 — Discovery | Schema, triggers, cron, queues, ignore file | Phase-1 adjustments |
| Phase 2 — Entry points | Every write entry found | Coverage |
| Phase 3 — Middleware & auth | Auth layer recorded per entry | Depth |
| Phase 4 — Validators | Input validation recorded | Depth |
| Phase 5 — Persistence trace | Targets + transaction state | Coverage + depth |
| Phase 6 — Async / triggers | Queue consumers, cron, triggers | Coverage |
| Phase 7 — Risk analysis | Every risk subtype walked | Depth |
| Phase 8 — Reporting | All required sections rendered | Depth |

**Tiers:**

- **95–100** — FULLY MAPPED
- **80–94** — MOSTLY MAPPED (gaps listed)
- **60–79** — PARTIALLY MAPPED
- **<60** — INSUFFICIENT — rerun with sub-agents or narrower scope

---

## Important Principles

- **The map is a hypothesis backed by trace evidence.** Reports describe what the skill observed; they never refactor or delete code.
- **This skill never modifies source files.** It only emits three new artifacts (`write-path-map.md`, `write-path-map.json`, `risk-register.md`) at the project root. If those files already exist, ask before overwriting.
- **Every mapped path must carry:** entry → middleware chain → validator → auth layer → handler → persistence target(s) → downstream effects. A path missing any of these is incomplete.
- **Paths without a persistence target are not writes.** Drop them or reclassify as reads. Listing GETs in the write map is a bug.
- **Completeness measures trace thoroughness, not quality.** A 100%-complete map of a broken system is still 100% complete. Quality is captured in the Risk Register.
- **DB writes include triggers, functions, policies, and cron jobs.** A write path is incomplete until DB-side effects are enumerated via Phase 6.
- **Never trust dynamic dispatch silently.** Flag `dynamic-dispatch-write` wherever a write target is resolved at runtime and leave it as INFO for human review.
- **Prefer live DB data when available.** Static schema files can be out of sync with the live database. If Supabase MCP or `DATABASE_URL` is available, enrich via Phase 1 step 7.
- **Respect `.write-path-ignore`.** Treat entries as load-bearing and surface stale patterns as warnings.
- **Sub-agents must be used aggressively.** Phase 2 and Phase 5 MUST spawn parallel `Explore` agents when the project has >30 candidates or any handler has 3+ service-layer hops. Cutting corners here directly reduces completeness.
- **Document tool versions** (ripgrep, Python, Node) in the report header so runs are reproducible.

---

## Edge Cases

1. **Empty / prototype project.** If fewer than 10 candidate entries exist, produce a minimal map without spawning sub-agents. Completeness tier "FULLY MAPPED" is achievable on small projects.
2. **Monorepo.** Treat each workspace package as a separate mapping target and produce a per-package map plus a workspace-level rollup. Cross-package writes (a service in package A writing via an import from package B) become fan-out edges.
3. **Serverless / edge functions.** Each function file is an entry point. Cold-start logic (auth clients, DB pool init) counts as middleware.
4. **GraphQL.** Every mutation resolver is an entry point. Subscriptions are NOT writes unless they trigger DB publishes. GraphQL queries are never writes.
5. **Event-driven / CQRS.** Commands are writes. Events emitted from commands are fan-out. Projections that write to read stores are secondary entry points.
6. **Multi-tenant.** Missing `workspace_id` / `tenant_id` filter on a scoped table is `cross-tenant-leak` CRITICAL. Verify every Supabase/ORM write against the table's column list.
7. **Background workers.** Queue consumers are secondary entry points. Map both the producer and the consumer. Orphans (producer with no consumer, or vice versa) are flagged in Phase 6.
8. **DB triggers and functions.** These are persistence-layer write paths with no application code entry point. Map them in Phase 6 from `extract-triggers.sh`. Include them in the DB trigger graph (Diagram D).
9. **Dynamic SQL.** Flag `sqli-risk` if the skill detects string interpolation with user input. Flag `dynamic-dispatch-write` if routing is resolved at runtime. Never attempt to evaluate dynamic SQL — it's the human reviewer's responsibility.
10. **Generated clients** (tRPC codegen, Prisma client, GraphQL codegen). Trace to the generator input (schema, router definition), not the generated output. Add generator directories to the suggested `.write-path-ignore`.
11. **Pure read-only project.** If zero write paths are detected, emit a "zero write paths detected" report with only Phase 1 output and exit cleanly. This is a valid outcome, not a failure.
12. **Unsupported language** (Elixir, Haskell, OCaml, Crystal, Zig). Emit "stack not fully supported" in Phase 1 and dump the ripgrep seed list as the map without structural guarantees. Do not fabricate findings.
13. **Tool failures.** If `ast-entrypoints.py` or any other helper crashes, record it as a Phase 1 limitation and continue. The skill must never abort on a single-tool failure.
