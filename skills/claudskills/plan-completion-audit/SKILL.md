---
name: plan-completion-audit
description: Audit a project plan against the actual implementation — verifying code, types, security, and Supabase backend alignment.
argument-hint: [path-to-project-root-or-plan-file]
allowed-tools: Read Grep Glob Write Edit Bash(npx:*) Bash(npm:*) Bash(yarn:*) Bash(pnpm:*) Bash(supabase:*) Bash(grep:*) Bash(find:*) Bash(ls:*) Bash(cat:*) Bash(bash:*) Bash(timeout:*) Bash(python3:*) Bash(mypy:*) Bash(pyright:*) Bash(ruff:*)
effort: high
---

# Plan Completion Audit

<!-- anthril-output-directive -->
> **Output path directive (canonical — overrides in-body references).**
> All file outputs from this skill MUST be written under `.anthril/audits/plan-completion-audit/`.
> Run `mkdir -p .anthril/audits/plan-completion-audit` before the first `Write` call.
> Primary artefact: `.anthril/audits/plan-completion-audit/<artefact>`.
> Do NOT write to the project root or to bare filenames at cwd.
> Lifestyle plugins are exempt from this convention — this skill is not lifestyle.

You are performing a rigorous, full-stack audit comparing a project plan against the actual codebase. Your primary job is to determine what has been built, what hasn't, and whether what was built is correct. Do NOT assume all work is complete — you are here to verify that. Treat the plan as the source of truth and the codebase as what needs to be measured against it.

## User Context

The user invoked the audit with: `$ARGUMENTS`

Treat this as a path to the project root or a specific plan/requirements file. If empty, default to the current working directory and locate the plan as described under "Before You Start". If a specific file path is provided, treat it as the canonical plan.

## Requirements

The audit invokes a number of external tools. None are mandatory — phases gracefully degrade when a tool is missing — but better coverage is achieved when these are available on PATH:

- **Node.js & npm** (or yarn/pnpm) — needed for `npx tsc`, `npx eslint`, `npm run build`, `npx madge`, `npx depcheck`, `npm audit`
- **Supabase CLI** (`supabase`) — preferred for Phase 10 schema inspection
- **Python tooling** — `python3`, `mypy`, `pyright`, `ruff` for Python projects (skipped otherwise)
- **bash** — required to run the helper scripts under `scripts/`
- **grep / find** — POSIX shell utilities (assumed)

If a dependency is missing, the corresponding step degrades to a warning rather than aborting the audit.

## Before You Start

1. **Locate the plan.** Find the project plan, task list, or requirements document. Check for: `PLAN.md`, `TODO.md`, `TASKS.md`, `README.md`, `CHANGELOG.md`, `requirements.md`, `.cursor/rules`, `CLAUDE.md`, GitHub issues, or inline `TODO`/`FIXME`/`HACK` comments. If no plan is found, ask the user to provide one — do not proceed without a plan to audit against.

2. **Identify the tech stack.** Scan `package.json`, `pyproject.toml`, `tsconfig.json`, or equivalent. Determine the framework (Next.js, React, Python/FastAPI, etc.), database (Supabase, Postgres), and tooling (ESLint, Prettier, tsc, etc.).

3. **Map the project structure.** Run:
   ```bash
   find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.sql" \) | grep -v node_modules | grep -v .next | grep -v dist | grep -v .git | sort
   ```

4. **Determine Supabase access method.** Try in this order:
   - **Supabase CLI** (preferred): Check if `supabase` CLI is available and a project is linked (`supabase status`)
   - **Supabase MCP**: Check if a Supabase MCP server/connector is available in the current environment
   - **Supabase Management API**: Use as last resort if CLI and MCP are unavailable
   
   If none are available, note it and perform the backend audit using local migration files and type definitions only.

## Audit Phases

Execute every phase in order. Report findings per phase using the format in the Reporting section. Never skip a phase — mark as N/A if genuinely not applicable, and mark as NOT IMPLEMENTED if the plan specifies work for that phase but no code exists.

---

### Phase 1: Plan Completion Verification

**Objective:** Build a complete inventory of every planned task and determine its implementation status. This phase gates the entire audit — its output defines what subsequent phases evaluate.

1. Read the full plan/requirements document.
2. Build a numbered checklist of every discrete task, feature, or deliverable mentioned in the plan.
3. For each item, search the codebase for its implementation. Assign one of these statuses:
   - âœ… **COMPLETE** — Code exists, is functional, and matches the plan specification
   - ðŸŸ¡ **PARTIAL** — Code exists but is incomplete, stubbed out, or missing key functionality described in the plan
   - âŒ **NOT STARTED** — No implementation found anywhere in the codebase
   - âš ï¸ **DEVIATES** — Implemented but differently than the plan specified (describe the deviation)
   
   Read the actual code to determine status — do not just confirm a file or function name exists. A file with a placeholder return, an empty function body, or a TODO comment inside it is PARTIAL, not COMPLETE.
4. Items marked NOT STARTED or PARTIAL are **CRITICAL** findings. List every one explicitly with a description of what is missing or incomplete.
5. Scan for unfinished work markers:
   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/skills/plan-completion-audit/scripts/check-todos.sh" .
   ```
   Or if the script is unavailable, run the grep manually:
   ```bash
   grep -rn "TODO\|FIXME\|HACK\|XXX\|PLACEHOLDER\|TEMP\|STUB\|@todo\|INCOMPLETE\|WIP" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --include="*.py" --include="*.sql" . | grep -v node_modules | grep -v .git | grep -v dist | grep -v .next
   ```
6. Summarise: total tasks, completed, partial, not started, deviates. Express as a percentage: "X of Y tasks complete (Z%)".
7. **Verdict rule:** If ANY items are NOT STARTED or PARTIAL, the Phase 1 verdict **MUST be FAIL**. Phase 1 can only PASS if 100% of plan items have COMPLETE status. There is no PASS WITH WARNINGS for this phase.

---

### Phase 2: Type Safety & Static Analysis

**Objective:** Zero type errors and zero lint violations across the entire codebase.

*Only audit code that exists. If Phase 1 found large portions NOT STARTED, note which planned modules could not be type-checked because they don't exist yet.*

Run the automated check if available:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/plan-completion-audit/scripts/check-types.sh" .
```

Or manually:
1. **TypeScript:** `npx tsc --noEmit 2>&1`
2. **ESLint:** `npx eslint . 2>&1` or the project's configured lint command from `package.json`
3. **Python (if applicable):** `mypy .` or `pyright .`
4. Report every error. Do not dismiss warnings without justification.
5. Check for `any` type abuse — flag files with excessive `as any`, `// @ts-ignore`, or `// @ts-expect-error` that suppress real issues.

---

### Phase 3: Bug & Logic Audit

**Objective:** Identify bugs, logic errors, and broken functionality through manual code review.

*Only audit code that exists. Reference the Phase 1 inventory — skip items marked NOT STARTED (there is nothing to review). Flag items marked PARTIAL and note what logic is missing.*

Review every source file containing application logic. For each file check:
- **Null/undefined:** Unguarded access to values that could be null, especially data from Supabase queries
- **Async errors:** Missing `await`, unhandled promise rejections, race conditions
- **Error handling:** Empty catch blocks, swallowed errors, missing try/catch around I/O and database calls
- **Conditional logic:** Flipped booleans, missing edge cases, unreachable branches
- **State management:** Stale closures in React, incorrect useEffect dependency arrays, mutation of state
- **API misuse:** Wrong HTTP methods, incorrect payload shapes, missing auth headers
- **Off-by-one errors:** Pagination, array slicing, loop boundaries
- **Resource leaks:** Unclosed subscriptions, listeners not cleaned up in useEffect returns

If tests exist, run them:
```bash
npm test 2>&1 || npx jest 2>&1 || npx vitest run 2>&1 || echo "No test runner found"
```

Check for dead code — functions, components, hooks, or utilities that are defined but never imported.

---

### Phase 4: Code Structure & Optimisation

**Objective:** Confirm code is well-structured, maintainable, and performant.

1. **Architecture:**
   - Clear separation of concerns (routes, components, services, hooks, utils, types)?
   - God files over 500 lines that should be split?
   - Copy-paste duplication that should be abstracted?

2. **Import hygiene:**
   - Unused imports across all files
   - Circular dependencies:
     ```bash
     npx madge --circular --extensions ts,tsx,js,jsx src/ 2>/dev/null || echo "madge not available"
     ```

3. **Performance:**
   - N+1 query patterns in Supabase calls (multiple sequential queries that should be joins or single RPCs)
   - Missing `useMemo`/`useCallback` where expensive computations re-run on every render
   - Unbounded data fetches without pagination or limits
   - Large bundle imports (full lodash, full date-fns, etc.)
   - Unnecessary re-renders — components subscribing to state they don't use

4. List specific improvements with file paths and line numbers.

---

### Phase 5: Failsafes & Guardrails

**Objective:** Verify defensive programming patterns are in place.

*For features marked NOT STARTED in Phase 1, list them here as "cannot verify — not implemented" rather than skipping silently. These are CRITICAL findings.*

1. **Input validation:** All user inputs validated before processing — forms, API params, URL params, file uploads
2. **Error boundaries:** React ErrorBoundary components wrapping major UI sections
3. **Loading states:** Every async operation has a loading indicator
4. **Empty states:** UI handles zero-data scenarios gracefully (no blank screens)
5. **Error states:** User-facing errors are clear, actionable, and don't expose internals
6. **Rate limiting:** API routes protected against abuse where applicable
7. **Timeouts:** External API calls and long-running operations have timeouts
8. **Graceful degradation:** Failures in non-critical services don't crash the app
9. **Environment guards:** Required env vars validated at startup, not at first use
10. **Data integrity:** Supabase writes use transactions where atomicity matters

---

### Phase 6: Security Audit

**Objective:** Identify security vulnerabilities.

Run the automated check:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/plan-completion-audit/scripts/check-secrets.sh" .
```

Then manually verify:
1. **Secrets:** No hardcoded API keys, passwords, tokens, or private keys in source
2. **`.gitignore`:** `.env`, `.env.local`, credential files, and key files are excluded
3. **Dependency vulnerabilities:** `npm audit 2>&1`
4. **Injection:** No raw SQL with string interpolation, no unsanitised HTML rendering (dangerouslySetInnerHTML without sanitisation), no command injection
5. **Auth & authorisation:** Protected routes require auth, RBAC enforced server-side via Supabase RLS — not just client-side checks
6. **CORS:** Not set to `*` in production config
7. **Data exposure:** API responses and Supabase queries don't leak sensitive fields, error messages don't expose stack traces in production
8. **Supabase-specific:** RLS enabled on all user-facing tables, service role key never exposed to client, anon key permissions are minimal

---

### Phase 7: Feature Hardening

**Objective:** Verify features are robust and handle edge cases.

For each major feature from Phase 1 (**only those marked COMPLETE or PARTIAL — list NOT STARTED features explicitly as "not implemented, cannot harden" and count them as CRITICAL findings**):
1. **Empty states:** Zero-data UI is handled
2. **Loading states:** Spinners/skeletons during async operations
3. **Error states:** Clear, actionable error messages
4. **Boundary conditions:** Max input lengths, file size limits, pagination limits enforced
5. **Concurrent access:** Multiple users editing the same resource won't corrupt data
6. **Idempotency:** Duplicate form submissions, payment retries, and webhook replays are safe
7. **Placeholder text:** No "Lorem ipsum", "TODO: write copy", or "test" strings in production UI
8. **Accessibility basics:** Interactive elements are keyboard-accessible, images have alt text, form fields have labels

---

### Phase 8: Deprecated Code Cleanup

**Objective:** No orphaned files, dead code, or legacy artefacts remain.

Run the automated check:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/plan-completion-audit/scripts/check-deprecated.sh" .
```

Then verify:
1. **Orphaned files:** Source files not imported or referenced anywhere
2. **Commented-out code:** Blocks of >5 lines of commented code that should be removed
3. **Deprecated APIs:** Usage of deprecated framework/library methods (e.g., deprecated Next.js APIs, old React patterns)
4. **Unused dependencies:**
   ```bash
   npx depcheck 2>/dev/null || echo "depcheck not available"
   ```
5. **Build artefacts in repo:** `dist/`, `build/`, `.next/`, `__pycache__/` committed to source
6. **Stale config:** Unused env vars, orphaned config entries
7. **Old migration files:** Supabase migrations that were superseded but not cleaned up (check `supabase/migrations/`)

---

### Phase 9: Build Verification

**Objective:** The project builds cleanly with zero errors and zero warnings.

1. Run the full production build:
   ```bash
   npm run build 2>&1 || yarn build 2>&1 || pnpm build 2>&1
   ```
2. Capture full output. A pass requires **zero errors** and **zero unacknowledged warnings**.
3. If the project has multiple build targets (e.g., monorepo packages), build each one.
4. Run a final type check after the build:
   ```bash
   npx tsc --noEmit 2>&1
   ```
5. If a dev server or preview mode exists, verify it starts without errors:
   ```bash
   timeout 15 npm run dev 2>&1 || echo "Dev server check skipped"
   ```

---

### Phase 10: Supabase Backend Audit

**Objective:** Verify all database tables, RPC functions, RLS policies, triggers, and indexes are correct, complete, and aligned with the application.

Read [`reference.md`](reference.md) (which routes to `references/supabase-audit-guide.md`) for the full checklist. The dense per-sub-phase content lives there to keep this SKILL.md scannable.

Sub-phases — each detailed in the guide:

- **10a. Schema Inspection** — column types/nullability, PK/FK, defaults, indexes, timestamps.
- **10b. RPC Function Audit** — signature match, body correctness, `SECURITY DEFINER` vs `INVOKER`, `search_path`, API-schema exposure.
- **10c. RLS Policy Audit** — RLS enabled per table, policies per CRUD verb, `auth.uid()` predicates, intentional service-role bypasses.
- **10d. Triggers & Realtime** — trigger definitions, replication settings, frontend subscription alignment.
- **10e. Storage & Edge Functions** — bucket RLS, MIME/size limits, deployed function endpoints.

Schema retrieval — use the first method available:

```bash
# Option 1: Supabase CLI / MCP
bash "${CLAUDE_PLUGIN_ROOT}/skills/plan-completion-audit/scripts/audit-supabase.sh"

# Option 2: Inspect local migration files
ls -la supabase/migrations/ 2>/dev/null
cat supabase/migrations/*.sql 2>/dev/null
```

---

### Phase 11: Frontend ↔ Backend Alignment

**Objective:** Confirm the frontend application and Supabase backend are in complete agreement — types, queries, RPC calls, and data flow.

Detailed checklist in [`reference.md`](reference.md). Five things to verify:

1. **Type alignment** — Supabase-generated types vs frontend interfaces, RPC signatures, and enum values.
2. **Query audit** — every `.from()`, `.rpc()`, `.select()`, `.insert()`, `.update()`, `.delete()` references real tables/columns of the correct type, with all required payload fields.
3. **Auth flow alignment** — providers, protected routes, token refresh handling.
4. **Missing backend objects** — frontend calls that reference non-existent tables or RPC functions.
5. **Missing frontend consumers** — tables/functions created by the plan but never called.

---

## Reporting

After all phases, produce a structured report. Use the template in `${CLAUDE_PLUGIN_ROOT}/skills/plan-completion-audit/templates/audit-report.md` as the base structure.

The report must include:
- A clear PASS / FAIL / NOT IMPLEMENTED / PASS WITH WARNINGS verdict per phase
- Phases where the underlying plan items were never built must be marked NOT IMPLEMENTED, not PASS
- A phase with no errors only because the code doesn't exist yet is NOT IMPLEMENTED, never PASS
- Every finding must include a **file path and line number** (or table/function name for backend findings)
- Severity ratings: **CRITICAL** (must fix), **WARNING** (should fix), **SUGGESTION** (nice to have)
- The Phase 1 completion summary (X of Y tasks complete, Z%) must appear prominently at the top of the report
- A prioritised action list at the end, with NOT STARTED items listed first

After the report is written, surface the next-step hint to the user:

> *To begin executing the action list, run `/utilities:audit-resolve` (or invoke the `[[audit-resolver]]` skill directly). It will parse this report, triage every finding, get your confirmation, then apply fixes batch-by-batch with verifier checks.*

## Important Principles

- **Be thorough.** Read actual code and run actual commands. Don't scan file names and guess.
- **Be specific.** Every finding needs a file path + line number or a table/function name. "Consider improving error handling" is useless — say exactly where and what.
- **Don't fix during the audit.** This is a report, not a refactor. List findings and let the user decide.
- **Verify, don't assume.** If the plan says "implement org-level access control" and you see an auth file, read it to confirm it works — don't check the box because the file exists.
- **Run commands.** Use the scripts in `scripts/` and run build/lint/type commands. Real output beats eyeballing.
- **Cross-reference constantly.** The frontend and backend must agree. A table without a consumer or a query against a non-existent column are both failures.
- **Absence of code is a failure.** If the plan specifies a feature and no code exists for it, that is a CRITICAL finding — not a pass. A phase with nothing to audit because nothing was built is NOT IMPLEMENTED, never PASS. Do not silently skip unbuilt features.
- **Do not conflate "no errors found" with "complete."** An empty room has no bugs in it — that does not mean the room is finished. If code doesn't exist, you cannot pass it.
