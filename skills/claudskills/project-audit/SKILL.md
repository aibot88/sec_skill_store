---
name: project-audit
description: Run a comprehensive audit on any Claude Code project. Scores 10 categories from 0-10 (total /100), identifies gaps, and generates a prioritized fix kit with copy-pasteable solutions. Use when you want to evaluate and improve your Claude Code setup, developer experience, security posture, or project quality.
---

# Elite Project Audit Skill

## Purpose

Audit any Claude Code project across 10 categories. Produce a score out of 100, identify gaps, and generate a prioritized fix kit with actionable solutions.

Elite performance comes from elite structure. This audit shows you where the structure is missing.

## How to Run

When this skill is invoked, execute the full audit below. Read the actual project files — don't guess or assume. Every score must be evidence-based.

**Output format:** Write the full audit report to `docs/audit-report.md` with:
1. Score summary table (all 10 categories)
2. Detailed findings per category (what exists, what's missing, evidence)
3. Prioritized fix kit (ordered by impact-to-effort ratio)
4. Top 3 quick wins (things fixable in under 15 minutes)

---

## Category 1: CLAUDE.md Quality (0-10)

CLAUDE.md is the highest-leverage file in any Claude Code project. It loads every session and shapes every response.

**What to check:**
- Does `CLAUDE.md` exist at the project root?
- Does it follow the WHAT / WHY / HOW framework?
  - WHAT: Tech stack, project structure, key files
  - WHY: Project purpose, what each part does
  - HOW: Build commands, test commands, conventions, how to verify changes
- Is it lean? (Under ~150 instructions. Claude Code's system prompt already contains ~50 instructions — bloated CLAUDE.md files cause instruction-following to degrade)
- Does it include common mistakes to avoid? (The highest-value section — only include things Claude gets wrong)
- Are critical rules emphasized with "IMPORTANT:" or "NEVER"?
- Does it avoid duplicating information available in skills or other docs?
- Are build/test/lint commands documented?
- Is there a clear git workflow defined?

**Scoring guide:**
- 0-2: Missing or just a project description with no actionable instructions
- 3-4: Exists but bloated, unstructured, or missing key sections
- 5-6: Covers basics but missing conventions, common mistakes, or emphasis on critical rules
- 7-8: Well-structured, lean, covers WHAT/WHY/HOW with clear conventions
- 9-10: Tight, battle-tested, every line earns its place, iterated based on real mistakes

**Also check for:**
- `CLAUDE.local.md` for personal overrides (should be in .gitignore)
- `~/.claude/CLAUDE.md` for global preferences
- Subdirectory CLAUDE.md files in monorepos

---

## Category 2: Skills & Commands (0-10)

Skills provide on-demand context that loads only when relevant. Commands are reusable prompt templates. Together they prevent re-explaining standards every session and save significant tokens.

**What to check:**

*Skills (`.claude/skills/`):*
- Do any project-specific skills exist?
- Does each skill have a clear `SKILL.md` with a descriptive name and trigger description?
- Are skills focused on a single domain? (design system, API patterns, database migrations, etc.)
- Do skills reference actual project files rather than generic advice?
- Is domain knowledge moved OUT of CLAUDE.md and INTO skills? (key for token efficiency)

*Commands (`.claude/commands/`):*
- Do any slash commands exist?
- Essential commands to look for:
  - Session start / catchup (review branch status, errors)
  - Pre-deploy check (lint, typecheck, build, test, security scan)
  - PR creation (cleanup, commit, push, create PR)
  - Planning (create implementation plan before coding)
  - Test generation (scaffold tests for existing code)

**Scoring guide:**
- 0-2: No skills or commands configured
- 3-4: 1-2 basic commands, no skills
- 5-6: Some commands exist but no skills, or skills exist but are generic
- 7-8: 3+ skills with clear triggers, 4+ commands covering key workflows
- 9-10: Comprehensive skill + command library tailored to the project, with supporting reference files

---

## Category 3: Hooks Configuration (0-10)

Hooks are deterministic guardrails — unlike CLAUDE.md rules (which are advisory), hooks are guaranteed to execute. They are your safety net.

**What to check:**
- Read `.claude/settings.json` (or equivalent) for hook configuration
- Essential hooks to look for:

| Hook | Event | Purpose |
|------|-------|---------|
| Auto-format | PostToolUse (Write/Edit) | Runs formatter (Prettier, Biome, etc.) on every file Claude edits |
| Safety guard | PreToolUse (Bash) | Blocks dangerous commands: rm -rf, DROP TABLE, DROP DATABASE, DELETE FROM...WHERE 1, git push --force |
| Notification | Notification | Desktop alert when Claude needs attention |
| Lint check | PostToolUse (Write/Edit) | Runs linter after edits (optional, can be noisy) |
| Pre-compact | PreCompact | Preserves critical context before compaction |

**Scoring guide:**
- 0-2: No hooks configured
- 3-4: One hook (usually auto-format)
- 5-6: Auto-format + one other hook
- 7-8: Auto-format + safety guard + notification
- 9-10: All three essential hooks plus project-specific hooks (e.g., migration file protection, test runner)

---

## Category 4: MCP Servers (0-10)

MCP servers connect Claude Code to external tools and services. The right MCPs eliminate context-switching. Too many bloat startup time and context.

**What to check:**
- Run `claude mcp list` or check `.claude/settings.json` for MCP configuration
- Evaluate based on project stack:

| Stack Component | Recommended MCP |
|----------------|----------------|
| GitHub repos | GitHub MCP |
| Supabase / Postgres | Supabase MCP or PostgreSQL MCP |
| Library docs needed | Context7 |
| Browser testing needed | Playwright MCP |
| Figma designs | Figma MCP |
| Slack communication | Slack MCP |
| Project management | Linear / Notion MCP |
| Web scraping needed | Firecrawl MCP |

**Scoring guide:**
- 0-2: No MCP servers configured
- 3-4: 1 MCP that's not critical to the workflow
- 5-6: 1-2 relevant MCPs for the stack
- 7-8: 2-3 well-chosen MCPs matching the primary workflow
- 9-10: Right MCPs for the stack, not overloaded, wildcard permissions configured for trusted servers

**Important:** More is NOT better. Score DOWN if there are 5+ MCPs that bloat context without clear value.

---

## Category 5: Project Structure (0-10)

Clean project structure helps both humans and Claude navigate the codebase efficiently.

**What to check:**
- Scan for files over 500 lines (flag any over 300 as warnings)
- Check for clear directory organization (components, lib, utils, hooks, types separated)
- Look for barrel exports / index files where appropriate
- Check for code duplication across files
- Monorepo: packages clearly separated with their own configs
- Are there any "junk drawer" directories? (utils/ with 30 unrelated files)
- Is there a clear separation between UI, business logic, API, and configuration layers?

**Scoring guide:**
- 0-2: No clear structure, files scattered, large monolithic files
- 3-4: Basic structure but multiple files over 500 lines, unclear separation
- 5-6: Good directory structure but some large files or unclear boundaries
- 7-8: Clean separation, most files under 300 lines, clear naming
- 9-10: Well-organized, modular, every directory has a clear purpose, no file over 500 lines

---

## Category 6: Security (0-10)

Security basics that should be in place before any production deployment. Score based on what is actually implemented, not what is planned.

**What to check:**

*Authentication & Authorization:*
- Are all API routes behind authentication? (check for unprotected endpoints)
- Is there role-based access control where needed?
- Are auth tokens validated on every request?

*Data Protection:*
- Database: Is Row Level Security (RLS) enabled? (Supabase/Postgres)
- Are environment variables used for ALL secrets? (check for hardcoded keys)
- Is `.env` in `.gitignore`?
- Does `.env.example` exist with placeholder values?
- Is PII excluded from server logs?

*Input Validation:*
- Are request bodies validated? (Zod, Joi, or equivalent)
- Is there SQL injection prevention? (ORM or parameterized queries)
- Is there XSS prevention? (output encoding, sanitization)

*Headers & Configuration:*
- Check for security headers: Content-Security-Policy, X-Frame-Options, X-Content-Type-Options
- Is CORS configured (not wildcard * in production)?
- Are rate limits on API routes? (especially auth, payment, and AI endpoints)

*Dependencies:*
- Run npm audit / pnpm audit / yarn audit and check severity
- Are there known critical vulnerabilities?

**Scoring guide:**
- 0-2: Major gaps — no auth on routes, no RLS, hardcoded secrets
- 3-4: Auth exists but inconsistent, secrets in env but some gaps
- 5-6: Auth on most routes, RLS enabled, env vars used, but missing validation or headers
- 7-8: Solid auth, RLS, validation, env management, basic security headers
- 9-10: Comprehensive — auth + RLS + validation + headers + rate limiting + clean audit + no PII in logs

---

## Category 7: Testing (0-10)

Not about 100% coverage. About whether the paths that matter are tested.

**What to check:**

*Infrastructure:*
- Is a test runner configured? (Vitest, Jest, Mocha, etc.)
- Is there a test setup file with proper mocks?
- Can tests run with a single command?
- Are tests in the CI/CD pipeline?

*Coverage of critical paths:*
- Authentication flows (login, signup, token refresh, logout)
- Payment / billing webhooks (if applicable)
- Core API routes (the ones that handle user data)
- Input validation (do bad inputs get rejected?)
- Business logic (state machines, calculations, transformations)
- Data integrity (deduplication, idempotency)

*E2E tests:*
- Is Playwright / Cypress configured?
- Are there E2E tests for critical user flows?

**Scoring guide:**
- 0-2: No test runner or tests
- 3-4: Test runner configured, 1-5 test files, minimal coverage
- 5-6: Test infrastructure solid, critical auth and API paths tested, in CI
- 7-8: Good unit + integration coverage of critical paths, E2E for core flows
- 9-10: Comprehensive testing, E2E for all critical flows, edge cases covered, tests run in CI with coverage thresholds

**How to count:** List the total number of API routes and the number with tests. Below 30% coverage = score capped at 5.

---

## Category 8: Git & CI/CD (0-10)

Version control hygiene and automated quality gates.

**What to check:**

*Git practices:*
- Is there a clear branching strategy? (feature branches from main)
- Are commits following a convention? (conventional commits: feat/, fix/, etc.)
- Is there a PR template?
- Are there branch protection rules on main?

*CI/CD pipeline:*
- Does a CI config exist? (.github/workflows/, etc.)
- What checks run automatically? (typecheck, lint, tests, build, security audit)
- Does deployment happen automatically on merge to main?
- Is there a staging/preview environment?

**Scoring guide:**
- 0-2: No CI/CD, no branch strategy
- 3-4: Basic CI with lint or build check only
- 5-6: CI runs lint + typecheck + build, manual deployment
- 7-8: CI runs full suite, auto-deploy on merge, preview environments
- 9-10: Full pipeline with branch protection, PR template, automated security audit, preview deployments, and rollback capability

---

## Category 9: Performance & Production Readiness (0-10)

The gap between "it works" and "it's production-ready."

**What to check:**

*Error handling:*
- Global error boundary (React: error.tsx / ErrorBoundary component)
- API error responses are structured and consistent
- Errors are logged with context (not swallowed silently)
- User-facing error states exist (not blank screens)

*Loading states:*
- Skeleton loaders or loading indicators on data-fetching pages
- Suspense boundaries where appropriate
- No blank/flash states during navigation

*Performance:*
- Images optimized (next/image, srcset, lazy loading)
- No N+1 database queries
- Proper caching headers on static assets
- Bundle size reasonable
- Lazy loading for below-fold content

*Production configuration:*
- Environment-specific config (dev vs. production)
- Error monitoring configured (Sentry, LogRocket, etc.)
- Analytics configured (even basic)
- Favicon, meta tags, Open Graph tags

**Scoring guide:**
- 0-2: No error boundaries, no loading states, unoptimized images
- 3-4: Basic error handling, some loading states, no monitoring
- 5-6: Error boundaries exist, loading states on key pages, images optimized
- 7-8: Solid error handling + loading states + optimized assets + monitoring
- 9-10: Comprehensive — error monitoring, analytics, optimized bundle, proper caching, all production configs

---

## Category 10: Cost Efficiency (0-10)

How efficiently the Claude Code setup uses tokens and context window.

**What to check:**

*CLAUDE.md bloat:*
- Count lines in CLAUDE.md. Over 200 = concern. Over 300 = problem.
- Does CLAUDE.md load large files unconditionally?
- Calculate token impact: each line ≈ 12 tokens
- Are reference docs loaded via skills (on-demand) or CLAUDE.md (every session)?

*Context management:*
- Is domain knowledge in skills (loads when relevant) vs. CLAUDE.md (loads always)?
- Are there conditional reading instructions? ("Read X only when working on Y")
- Are there duplicate instructions between CLAUDE.md and skills/MEMORY.md?

*Workflow efficiency:*
- Do specific file references use @file syntax?
- Are prompts specific enough to avoid multi-turn clarification?
- Is there a model switching strategy? (Sonnet for routine, Opus for complex)

**Scoring guide:**
- 0-2: CLAUDE.md over 300 lines, loads multiple large files every session, no skills
- 3-4: Moderately bloated CLAUDE.md, some redundancy, no skills for offloading
- 5-6: Reasonable CLAUDE.md size, some skills exist but knowledge isn't fully migrated
- 7-8: Lean CLAUDE.md, skills handle domain knowledge, conditional doc loading
- 9-10: Optimized — lean CLAUDE.md, comprehensive skills, conditional loading, model strategy, no redundancy

---

## Generating the Fix Kit

After scoring all 10 categories, generate a prioritized fix kit.

### Prioritization Rules

1. **Sort by impact-to-effort ratio** — a 5-minute hook setup that gains +8 points ranks above a half-day refactor that gains +1 point
2. **Group into tiers:**
   - **Tier 1: Do Today** (under 15 minutes each, zero/low risk)
   - **Tier 2: Do This Week** (30-60 minutes each, low/medium risk)
   - **Tier 3: Do This Month** (1+ hours, may need staging/local dev to test)
   - **Tier 4: Backlog** (nice-to-have, do when convenient)
3. **For each fix, include:**
   - What to change (specific files)
   - How to change it (code, commands, or configs — copy-pasteable when possible)
   - Risk level (None / Low / Medium / High)
   - Production impact (will this affect live users?)
   - Dependencies (needs Docker, staging environment, etc.?)

### Stage-Appropriate Advice

Consider the project's maturity when prioritizing:

| Stage | User Count | Priority |
|-------|-----------|----------|
| Pre-launch | 0 | Foundation: CLAUDE.md, skills, hooks, basic security |
| Early | 1-50 | Ship features, maintain security basics, don't over-optimize |
| Growing | 50-500 | Testing coverage, performance, monitoring, CSP headers |
| Scale | 500+ | Comprehensive security, E2E testing, performance optimization |

**IMPORTANT:** Always note when a fix is "best practice" vs. "critical for current stage." A solo developer with 5 users has different priorities than a team with 500 users. Don't recommend spending a day on test coverage when the developer should be shipping features.

---

## Report Template

```markdown
# Project Audit Report

**Project:** [name]
**Date:** [date]
**Overall Score:** [X]/100

## Score Summary

| Category | Score | Status | Notes |
|----------|-------|--------|-------|
| CLAUDE.md Quality | X/10 | 🟢/🟡/🔴 | [one-line summary] |
| Skills & Commands | X/10 | 🟢/🟡/🔴 | |
| Hooks Configuration | X/10 | 🟢/🟡/🔴 | |
| MCP Servers | X/10 | 🟢/🟡/🔴 | |
| Project Structure | X/10 | 🟢/🟡/🔴 | |
| Security | X/10 | 🟢/🟡/🔴 | |
| Testing | X/10 | 🟢/🟡/🔴 | |
| Git & CI/CD | X/10 | 🟢/🟡/🔴 | |
| Performance | X/10 | 🟢/🟡/🔴 | |
| Cost Efficiency | X/10 | 🟢/🟡/🔴 | |

Status: 🟢 8-10 | 🟡 5-7 | 🔴 0-4

## Detailed Findings

[Per-category breakdown with evidence]

## Fix Kit

### Tier 1: Do Today
### Tier 2: Do This Week
### Tier 3: Do This Month
### Tier 4: Backlog

## Top 3 Quick Wins

1. [Specific action] — [time estimate] — [point impact]
2. [Specific action] — [time estimate] — [point impact]
3. [Specific action] — [time estimate] — [point impact]
```

---

## How to Use This Skill

**Run a full audit:**
```
Run the project-audit skill on this project. Read all relevant files and produce the full report.
```

**Audit a specific category:**
```
Run the project-audit skill — Security category only. Detailed findings and fixes.
```

**Re-audit after fixes:**
```
Run the project-audit skill again. Compare against docs/audit-report.md and show what improved.
```

**Audit a new project:**
```
Run the project-audit skill. Fresh project — focus on foundation setup.
```

---

## Installation

1. Create the directory: `.claude/skills/project-audit/`
2. Save this file as `SKILL.md` inside that directory
3. Restart Claude Code

The skill auto-loads whenever you ask Claude to audit, review, or evaluate your project setup.
