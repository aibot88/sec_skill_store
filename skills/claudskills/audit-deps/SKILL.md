---
name: audit-deps
description: >
  Audit open dependabot PRs in this repo. Spawns one investigator per PR
  (each with a codebase-walk sub-agent), produces a comparison table with
  per-PR risk + recommendation, and proposes a merge order that minimizes
  rebase churn. Audit-only — stops at recommendations; user authorizes
  execution. Use when dependabot has stacked up multiple open PRs and you
  want a structured pass before merging.
allowed-tools: Bash, Read, Glob, Grep, WebFetch, WebSearch, Agent, TaskCreate, TaskUpdate, TaskList, AskUserQuestion
argument-hint: "[pr-number ...] (optional, defaults to all open dependabot PRs)"
---

# Audit Dependabot PRs

Audit open dependabot PRs and propose a safe merge order.

You are the **team lead**. You orchestrate. You do NOT read source code or run grep yourself
during investigation — every codebase walk goes through a sub-agent inside a per-PR investigator.
You handle GitHub queries, worktree setup, synthesis, and the merge-order proposal.

The skill is **audit-only**. It never merges, pushes, comments on PRs, or removes worktrees. It
ends by presenting findings + a proposed sequence and asking the user what to do next.

## Phase 0 — Discovery

Args: an optional list of PR numbers (`/audit-deps 77 78 79`). If omitted, audit every open
dependabot PR.

Run once:

```bash
gh pr list --state open --json number,title,headRefName,author,createdAt,mergeable,statusCheckRollup \
  --jq '.[] | select(.author.login=="app/dependabot" or (.headRefName | startswith("dependabot/")))'
```

If args were passed, narrow to those PR numbers. From each PR object extract:

- PR number, title, head ref
- `mergeable` state (`MERGEABLE` / `CONFLICTING` / `UNKNOWN`)
- `statusCheckRollup` — count and roll up to "all green" / "N failing"
- Age in days (today − `createdAt`)

If the result is empty, exit early with a one-line message — no work to do.

If any PR has `CONFLICTING` AND age > 7 days, note it as "stale-conflict — rebase candidate" but do
NOT trigger a rebase. Rebase decisions belong to Phase 4 (user authorization).

State briefly to the user what you found before moving on:

> Found N open dependabot PRs: #77 paging, #78 AGP 9.2.1, #79 kotlinx-datetime. Setting up worktrees.

## Phase 1 — Worktree setup

Project worktree convention: `.claude/worktrees/deps/pr-<N>` on a local branch named `pr-<N>`.

For each PR:

```bash
# fetch dependabot branch as local pr-<N>
git fetch origin <head-ref>:pr-<N>

# create worktree (or refresh if it exists from a prior audit run)
if [ -d ".claude/worktrees/deps/pr-<N>" ]; then
  git -C .claude/worktrees/deps/pr-<N> fetch origin
  git -C .claude/worktrees/deps/pr-<N> reset --hard pr-<N>
else
  git worktree add .claude/worktrees/deps/pr-<N> pr-<N>
fi
```

Never auto-remove worktrees from prior runs — they may be useful for the user post-audit. Worktree
cleanup happens only after Phase 4 if the user approves.

## Phase 2 — Parallel investigation

Spawn **one investigator per PR** in a **single message** (multiple `Agent` tool calls together so
they run concurrently).

Each investigator is a one-shot `Agent` call (no `team_name` — Agent Teams are unnecessary here).
The investigator's job has two parts:

1. **Upstream research** — the investigator does this itself via `WebFetch` / `WebSearch`. Read
   release notes, changelog, and (if available) the GitHub compare view between the two versions.
2. **Codebase impact** — the investigator MUST delegate this to a nested sub-agent via its own
   `Agent` call. The sub-agent reads the project root (not the worktree — current `develop` is the
   real merge target). The investigator synthesizes upstream + codebase findings into one report.

### Investigator prompt template

Pass the investigator everything it needs so it doesn't re-discover:

- PR number, worktree path, project root path
- Exact files changed in the PR (extract from `gh pr diff <N> --name-only` before spawning)
- CI status rollup from Phase 0 (don't make the investigator re-fetch)
- Targeted WebFetch URLs — release notes, changelog, GitHub compare view
- Word cap on the report (250–400 depending on bump complexity)
- Required report fields:
  - **Breaking changes**: bullet list, or `none — patch`
  - **Codebase impact**: file count + specific call sites with `path:line`, authored by the sub-agent
  - **Sequencing constraints**: e.g., "requires Gradle 9.5+ — depends on PR #76", or `none`
  - **Risk**: `Low` / `Medium` / `High` + one-line justification
  - **Recommendation**: `merge as-is` / `merge with caveats (...)` / `hold (...)`

Include these flags in the prompt when applicable:

- **Kotlin/KMP bump** (Kotlin, AGP, Compose, KSP, Ktor, Koin, serialization, SKIE, mokkery, anything
  hooking the K2 compiler): the investigator MUST first **enumerate every plugin in
  `gradle/libs.versions.toml` that touches the Kotlin compiler or Kotlin/Native**, then check each
  for compatibility. Do NOT pre-list dependencies for the investigator to verify — pre-listing
  causes blind spots. SKIE specifically has been missed twice this way (2026-04-25, 2026-05-06);
  check [touchlab/SKIE releases](https://github.com/touchlab/SKIE/releases) and open issues
  directly, not just variant attributes.
- **Pre-1.0 minor bump** (`0.x.y → 0.z.0`): apply extra scrutiny — pre-1.0 minor bumps can break
  source/binary API even on green CI. Explicitly check for renamed/relocated symbols that still
  compile via deprecated aliases.
- **AGP bump**: if the release notes touch R8, proguard, manifest merger, or lint, the
  recommendation must include "release-build smoke test (login → conversations → chat)" as a
  caveat.

### Sub-agent prompt template (codebase walk)

The investigator constructs this and passes it to a nested `Agent` call:

- Project root path (the live `develop` checkout, not the worktree)
- A grep list specific to the library — symbols, imports, common type names, build-script keys
  (e.g., for paging: `import androidx.paging`, `PagingSource`, `Pager(`, `LazyPagingItems`,
  `RemoteMediator`, `paging-compose`)
- The new API surface and any deprecations from the upstream changelog the investigator just
  fetched (so the sub-agent knows which call sites are at risk)
- Report format:
  - File count: how many files touch this library?
  - Call sites: list with `file:line`
  - Deprecation/removal exposure: which call sites use APIs flagged by the upstream changelog as
    changed/deprecated/removed, with explicit `file:line`
  - KMP source-set coverage: does usage live in commonMain, androidMain, iosMain, or tests?
  - Word cap: 200 words

The investigator returns a combined report. Word cap is the investigator's, not the sum.

## Phase 3 — Synthesis and merge-order proposal

After all investigators return, produce two artifacts in the response.

### 1. Comparison table

One row per PR. Columns:

```
| # | Bump | CI | Breaking changes | Codebase impact | Sequencing | Risk | Recommendation |
```

Include every PR Phase 0 enumerated. No silent drops — if an investigator failed, surface the
failure rather than omitting the row.

### 2. Proposed merge order

A numbered list, each entry naming the PR and a one-line rationale. Ordering rules (priority
order):

1. **Independent green low-risk first** — CI-green + Low risk + no sequencing constraints. These
   are warm-ups; merging them first reduces rebase churn for everything that follows.
2. **Respect sequencing constraints** — if PR B requires PR A (e.g., Gradle ≥ 9.5 → AGP), A goes
   first.
3. **Config-patch-needed last among non-blocked** — PRs that need a small config tweak alongside
   the bump (detekt rule overrides, proguard addition, etc.) sit at the end of the non-blocked
   set, so green PRs don't get gated behind config work.
4. **Hold last with a `BLOCKED` tag** — PRs flagged "hold" (CI blocker, breaking change requiring
   code, awaiting upstream fix) sit at the end with the unblocking condition stated explicitly.

State the *why* on every line. The user reads the rationale to override the order if needed.

## Phase 4 — User authorization

Ask the user via `AskUserQuestion` what to do. Typical options to offer:

- Merge all green / merge a subset
- Push config patch for PR #X (if applicable)
- Trigger `@dependabot rebase` on stale-conflict PRs
- Hold all (leave PRs untouched, exit)
- Cancel

The skill exits after presenting. **Execution happens outside the skill** — the user authorizes
each action explicitly so per-action control is preserved. This is intentional; don't try to bundle
"merge + push patch + comment" behind a single approval inside the skill.

## Anti-patterns to avoid

These come from prior runs (sessions `3ae98b8c` 2026-05-05 and the 2026-05-11 follow-up):

- **Don't pre-list dependencies for the investigator to check.** Make them enumerate from
  `libs.versions.toml`. Pre-listing causes blind spots (SKIE missed twice).
- **Don't trust "CI green" to mean "safe"** for pre-1.0 minor bumps. Deprecated aliases still
  compile; flag them anyway.
- **Don't auto-trigger rebases or auto-merge.** Both are user-authorized actions even when "the
  fix is obvious." The cost of pausing is low; the cost of a wrong auto-merge is high.
- **Don't drop a PR from the table** if the investigator failed. Surface the failure as a row
  marked `[INVESTIGATOR FAILED]` so the user sees it.
- **Don't read source files yourself as the team lead.** Codebase walks always go through the
  per-PR investigator's sub-agent.
