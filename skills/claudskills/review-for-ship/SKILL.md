---
name: review-for-ship
description: >
  User-invoked skill to run a comprehensive pre-ship review using all review agents
  relevant to the project's tech stack, with rad-code-review as the final gate.
  Reads the stack profile and dispatches specialist agents in parallel, then runs
  rad-code-review for AI slop detection, architecture, security, and release readiness.
  Trigger when the user says "/review-for-ship", "review before shipping",
  "is this ready to deploy", "pre-ship review", "run all reviews", "comprehensive review",
  "final check before shipping", "production readiness check", "is this ready to merge",
  "ship check", "pre-deploy review", "audit everything".
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Agent
  - Skill
  - AskUserQuestion
---

# Pre-Ship Review

Run all relevant review agents for this project's tech stack, then invoke rad-code-review as the final gate. This is the comprehensive quality gate — use it before deploying, merging a major feature, or shipping a release.

**Announce at start:** "Running pre-ship review — dispatching specialist reviewers for your stack, then rad-code-review as final gate..."

---

## Step 1: Read Stack Profile

Read `.claude/stack-profile.local.md` from the project root.

**If the file does not exist:**
Tell the user: "No stack profile found. Run `/detect-stack` first to scan your project and identify which review agents apply. Then come back and run `/review-for-ship`."
Stop here.

**If the file exists:**
Parse the YAML frontmatter. Extract:
- `project_name`
- `project_type`
- `technologies` (the list)
- `review_agents` (the list of agents with their `subagent_type` values)
- `plugins.core`, `plugins.supporting`, `plugins.pre_ship`, `plugins.final_gate`

### Profile Drift Warning

Parse the `detected` date from the YAML frontmatter. If it is older than 90 days:

> "Your stack profile is [N] days old. Dependencies and technologies may have changed. Consider running `/detect-stack --update` to refresh before review. Continue with current profile?"

Wait for user confirmation. If they want to update, stop and suggest `/detect-stack --update`.

---

## Step 2: Confirm with User

Before dispatching agents, show the user what will run:

```
## Pre-Ship Review Plan

**Project:** [project_name]
**Type:** [project_type]
**Stack:** [comma-separated technology names]

### Phase 1: Specialist Reviewers (run in parallel)
[For each agent in review_agents:]
- **[agent name]** — [one-line description of what it reviews]

### Phase 2: Final Gate
- **rad-code-review** — AI slop detection, architecture, security, release readiness verdict

This will run [N] specialist agents in parallel, then rad-code-review as the final pass.

Proceed? (This uses context and tokens proportional to the number of agents.)
```

Wait for user confirmation before proceeding. If the user says no or wants to skip certain agents, adjust accordingly.

---

## Step 3: Dispatch Specialist Review Agents

Launch all specialist review agents **in parallel** using the Agent tool. For each agent:

- Set `subagent_type` to the value from the stack profile
- Set `run_in_background` to `true` so all agents run concurrently
- Give each agent a clear prompt:

```
Review the project at [current working directory] for [what this agent reviews].
This is a [project_type] project using [technology list].
Scan the full codebase and report findings organized by severity (Critical, Warning, Info).
Be thorough but practical — focus on issues that would cause real problems in production.
```

### Available Specialist Review Agents

Only dispatch agents that are listed in the stack profile's `review_agents` field:

| Agent | subagent_type | Reviews |
|---|---|---|
| Astro Reviewer | `rad-astro:astro-reviewer` | Astro anti-patterns, performance, hydration, SSR/SSG issues |
| Next.js Reviewer | `rad-nextjs:nextjs-reviewer` | App Router violations, Server Actions security, IDOR, middleware bypass |
| React Reviewer | `rad-react:react-reviewer` | Hooks violations, stale closures, performance, accessibility, XSS/IDOR |
| TypeScript Reviewer | `rad-typescript:typescript-reviewer` | Strict-mode compliance, type safety, API boundaries, AI codegen anti-patterns |
| Fastify Reviewer | `rad-fastify:fastify-reviewer` | Encapsulation violations, decorator traps, validation, production readiness |
| Zod Reviewer | `rad-zod:zod-reviewer` | Schema safety, coercion attacks, over-posting, validation boundaries |
| Accessibility Reviewer | `rad-a11y:a11y-reviewer` | WCAG 2.2 AA compliance, ARIA, keyboard navigation, focus management |
| Chrome Extension Reviewer | `rad-chrome-extension:chrome-ext-reviewer` | MV3 security, permissions, Chrome Web Store compliance |
| SEO Auditor | `rad-seo-optimizer:seo-dominator` | Full SEO audit, Core Web Vitals, schema markup, AEO readiness |
| Coolify Reviewer | `rad-coolify-orchestrator:coolify-reviewer` | Dockerfile, compose, CI/CD, environment variables, security |
| Supabase Reviewer | `rad-supabase:supabase-reviewer` | Schema, RLS policies, edge functions, migrations, configuration |

---

## Step 4: Final Gate — rad-code-review

After **all specialist agents have completed** and their results are collected, run rad-code-review as the final gate.

### Invocation

Invoke the `rad-code-review` skill with these parameters:
- Scope: the current project (full codebase)
- Strictness: `production` (default) — user can override to `mvp` or `public`
- Let rad-code-review run its full workflow: bug finder, architecture reviewer, release gate

### What the Final Gate Covers

rad-code-review provides the generalist layer that complements the specialist reviewers:

1. **AI Slop Detection** — 14 patterns for hallucinated imports, fake error handling, placeholder stubs, cargo-cult patterns, silent failures
2. **Architecture Review** — Coupling, boundaries, naming, extensibility, test gaps
3. **General Security** �� OWASP 12 categories (catches gaps the specialists might miss)
4. **Release Readiness** — Config separation, secrets, dependencies, migrations, monitoring, documentation
5. **Documentation** — README, setup instructions, env var documentation
6. **Dependency Audit** �� CVEs, outdated packages, lockfile integrity

### Final Gate Verdict

rad-code-review's release verdict becomes the ship/no-ship decision:
- **Ship** — No critical or major findings blocking release
- **Conditional** — Issues found but not release-blocking at the specified strictness
- **No Ship** — Critical or major findings that block release

---

## Step 5: Compile Unified Report

Once all specialists AND the final gate have reported, compile a unified report.

### Report Format

```
# Pre-Ship Review Report

**Project:** [name]
**Date:** [today's date]
**Stack:** [technologies]
**Specialist Agents:** [count] run
**Final Gate:** rad-code-review (strictness: [level])

---

## Overall Assessment

**Verdict:** [Ready to Ship / Needs Work / Critical Issues Found]

| Source | Critical | Warning | Info |
|--------|----------|---------|------|
| [Each specialist agent] | [n] | [n] | [n] |
| rad-code-review (final gate) | [n] | [n] | [n] |
| **Total** | **[n]** | **[n]** | **[n]** |

---

## Specialist Findings

### [Agent Name]
**Status:** [Clean / Issues Found]

[If issues found, list organized by severity:]

#### Critical
- [Issue description + file:line + recommended fix]

#### Warnings
- [Issue description + file:line + recommended fix]

#### Info
- [Improvement suggestion]

[Repeat for each specialist agent]

---

## Final Gate: rad-code-review

**Verdict:** [Ship / Conditional / No Ship]
**Strictness:** [mvp / production / public]

### Findings
[rad-code-review findings organized by its standard severity model]

### AI Slop Detection
[Any AI-generated code issues flagged]

### Release Readiness
[Release gate assessment]

---

## Recommended Actions

Priority order for fixing issues before shipping:

1. **[Critical item from any source]** — [why it matters, what to do]
2. **[Critical item]** — [why it matters, what to do]
3. **[Warning item]** — [why it matters, what to do]
...

---

## What's Next?

[Based on overall verdict:]
- **Critical Issues Found:** "Fix the critical issues above, then run /review-for-ship again to verify."
- **Needs Work:** "The warnings above are worth addressing but may not be blockers depending on your timeline."
- **Ready to Ship:** "Your project looks good! No critical issues found across all reviewers and the final gate."
```

### Overall Verdict Logic

1. If rad-code-review (final gate) says **No Ship** �� overall = **Critical Issues Found**
2. If any specialist has Critical findings ��� overall = **Needs Work**
3. If rad-code-review says **Ship** and no specialist Criticals ��� overall = **Ready to Ship**
4. If rad-code-review says **Conditional** and no specialist Criticals → overall = **Needs Work**

---

## Step 6: Offer Follow-Up

After the report, offer:
- "Want me to fix any of these issues?" (if issues were found)
- "Want me to run a specific reviewer again after fixes?" (for targeted re-check)
- "Want me to save this report to a file?" (write to `.ucr/history/` or user-specified path)

---

## Edge Cases

- **Specialist agent fails or times out:** Note which agent failed, report results from successful ones, suggest re-running the failed agent individually.
- **rad-code-review fails:** Report specialist results without the final gate. Note that the release verdict is incomplete.
- **No review agents in profile:** Still run rad-code-review as the final gate (it works on any project). Note that specialist coverage is missing and suggest `/detect-stack --update`.
- **User wants partial review:** Only dispatch the requested subset. Still offer the final gate unless explicitly skipped.
- **User wants to skip final gate:** If the user says "skip code review" or "specialists only", compile the report from specialist findings only.
