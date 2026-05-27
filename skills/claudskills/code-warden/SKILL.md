---
name: code-warden
description: >
  AI development governance protocol for Codex, Claude Code, and Cowork.
  Enforces modular architecture, adversarial feedback, patch-first editing,
  blast radius safety, zero-trust secrets, and context drift prevention. Use at
  the start of any coding session, when generating or modifying modules, when
  refactoring existing code, when making architectural changes, or when any of
  the following are said: "load protocol", "apply dev rules", "check the rules",
  "start a new module", "review this before we write", "are we following the
  rules", "new session", "begin coding", "load code-warden", "governance check",
  or any request to begin writing code.
metadata:
  author: Justin Davis
  version: 3.1.1
  category: development-governance
  changelog: |
    v3.1.1 (2026-05-15): Stabilization. Behavioral tests (8 scanner/hook pass/fail
      cases via node:test). Shared policy modules: lib/line-count.js, lib/secret-patterns.js,
      lib/file-collection.js, lib/config.js. Line-count off-by-one fixed (trailing newline).
      Secret-pattern drift fixed (GitHub token gh[posx]_ → gh[pousr]_ unified across all consumers).
      README wording: zero-trust secrets policy (governance) vs hardcoded credential scanner (impl).
    v3.1.0 (2026-05-15): Codex partial hook enforcement. --hooks=codex installs
      PreToolUse hooks for apply_patch (secrets + estimated size) and Bash (secrets).
      Hooks live in tools/hooks/codex/. Claude hooks moved to tools/hooks/claude/.
      Doctor and verify-target validate Codex hook paths via ~/.codex/hooks.json.
    v3.0.0 (2026-05-15): Optional Claude Code hooks package. --hooks=claude installs
      PreToolUse hooks that block writes violating file-length or zero-trust secrets
      policy before they happen. --uninstall-hooks=claude removes them. Doctor and
      verify-target validate hook script paths when hooks are registered.
    v2.8.0 (2026-05-15): Added --verify-target=<id> strict per-target health check.
      Unknown target IDs exit nonzero. Known but not-installed targets exit nonzero.
      Added npm scripts: install-list, install-doctor.
    v2.7.1 (2026-05-15): Added Scope Gate and Plan Gate pre-implementation declaration
      blocks. Both gates must be confirmed before any code is written. Covers goal,
      non-goals, files in/out, patch order, blast radius class, and post-patch checks.
    v2.7.0 (2026-05-15): Added GitHub Actions CI template and npm run ci script.
      Code-Warden now enforces file length and zero-trust secrets outside the chat session.
    v2.6.0 (2026-05-15): Added cross-platform auto-installer with app detection,
      atomic install, --doctor health checks, and Windsurf flat-file adapter.
    v2.5.0 (2026-05-14): Added Research and Fit governance to force live research
      for current facts and challenge default stack/product assumptions.
    v2.4.0 (2026-05-14): Added operational governance for verification evidence,
      source-control hygiene, dependency control, and technical claim sourcing.
    v2.3.1 (2026-05-14): Added Codex/shared-agent install support, AGENTS.md context discovery,
      ASCII tool output for reliable terminals, and refreshed setup docs.
    v2.3.0 (2026-03-26): Added stronger secret scanner, Windows installer, README, version sync,
      and broader Claude context discovery.
    v2.2.3 (2026-03-25): Replaced soft checklist with mandatory Hard Gate output block.
    v2.2.2 (2026-03-25): Added verifiable Pre-Flight manifest, CONFIGURE.md, and examples.
    v2.2.1 (2026-03-25): Fixed reference paths, triggers, DECISIONS.md stub, and checkpoint threshold.
    v2.2.0: Added anti-drift.md, Anchor Check, and Drift Trigger Response Protocol.
    v2.1.0: Added modular references for safety, cognition, cleanup, architecture, and anti-drift.
    v2.0.0: Initial production release.
---

# code-warden v3.1.1

Production-grade AI development governance skill.
Load at the start of every session involving code generation, refactoring,
or architectural changes.

## Session Start - HARD GATE

Do not ask implementation questions. Do not gather requirements. Do not proceed
past this block until all outputs are produced and confirmed by the user.

Mandatory sequence — produce in order, each confirmed before the next:

1. **Architecture State** (below)
2. **Session Scope** (below)
3. **Reference Files** (below)
4. **Scope Gate** — see [references/planning-gates.md](references/planning-gates.md)
5. **Plan Gate** — see [references/planning-gates.md](references/planning-gates.md) (fires after Scope Gate confirmed)

Before responding, execute `node <installed-skill-dir>/tools/get-context.js` if
you lack architectural context.

Common install directories:
- Codex shared agents: `~/.agents/skills/code-warden`
- Codex local skills: `~/.codex/skills/code-warden`
- Claude Code: `~/.claude/skills/code-warden`

Output this block as your first response before anything else:

---

**ARCHITECTURE STATE** (Re-injection Rule)

[Paste the context found by `get-context.js` or provided by user. If none found, write:]

> [WARN] No architecture doc found - applying Re-injection Fallback:
> - Last known files: [list any files mentioned in this session]
> - Current data flow: [unknown - user must provide before proceeding]
>
> **REQUEST:** Paste your architecture doc, PRD, or a 3-sentence scope
> summary before we continue.

**SESSION SCOPE** (Session Scoping Rule)

> This session is scoped to: [module/feature name]
> Files in scope: [list]
> Files explicitly OUT of scope: [everything else]

[If scope is unknown, write:]

> [WARN] Scope undefined - user must confirm before proceeding.

**REFERENCE FILES LOADED** (Blueprint Rule)

> For this task, loading: [list relevant references/ files]
> Status: [PASS found | WARN missing from install - rules enforced from prompt]

---

Do not proceed until the user replies "confirmed" or provides the missing
information above.

## Quick Rules

- **Scope Gate**: Required before every session. Declare goal, non-goals, files in/out, verify commands, rollback plan. See `references/planning-gates.md`.
- **Plan Gate**: Required before any multi-file or >30-line change. Declare patch order, blast radius class, post-patch checks. See `references/planning-gates.md`.
- **Max file size**: Enforced by `warden-lint.js` (default 400 lines). Split into modules at the limit.
- **Editing mode**: Patch/diff first. No full rewrites without blast radius check.
- **Feedback mode**: Adversarial. Correctness over comfort; push back on weak logic.
- **Secrets**: Zero-trust. Enforced by `verify-secrets.js`; no hardcoded keys.
- **Uncertainty**: Say so. Never guess niche syntax or stale API behavior.
- **Concerns**: One responsibility per file. Support human auditing.
- **Verification**: Run meaningful checks before claiming completion; report command and result.
- **Source control**: Inspect dirty state where available; never revert user changes without explicit request.
- **Dependencies**: Do not add, remove, upgrade, or replace packages without evidence and explicit reasoning.
- **Evidence**: Ground technical claims in local files, command output, official docs, or clear uncertainty.
- **Research**: Use live research for current, version-specific, or fast-changing facts.
- **Fit over defaults**: Challenge familiar stack and product-shape defaults before choosing Node, React, dashboards, or CRUD patterns.

## Reference Files

Load these when relevant to the current task:

- Scope Gate, Plan Gate, blast radius class, patch order -> [references/planning-gates.md](references/planning-gates.md)
- Architecture decisions, Blueprint Rule, Re-injection -> [references/architecture.md](references/architecture.md)
- Blast Radius, Patch-First, Zero-Trust, Dependency Freeze -> [references/safety.md](references/safety.md)
- Think Before Coding, Don't Guess Syntax, Human Checkpoint -> [references/cognition.md](references/cognition.md)
- Tech Debt flag format, Test Contract, Decision Log -> [references/cleanup.md](references/cleanup.md)
- Anchor Check, Session Scoping, Drift Trigger -> [references/anti-drift.md](references/anti-drift.md)
- Verification, git hygiene, dependency control, evidence -> [references/operations.md](references/operations.md)
- Live research, anti-default stack choices, product-shape fit -> [references/research-and-fit.md](references/research-and-fit.md)

## Drift Signals - Hard Stop

Stop and re-anchor immediately if any of these appear:

| Signal | Action |
|--------|--------|
| Began implementing without a confirmed Scope Gate | Stop, produce Scope Gate, await confirmation |
| Began implementing without a confirmed Plan Gate | Stop, produce Plan Gate, await confirmation |
| Touched a file not declared in Scope Gate | Stop, declare scope expansion, await approval |
| Guessed library syntax without searching docs | Search live docs, correct output |
| Used stale training data for current facts | Run live research or mark unverified |
| Chose a default stack/product shape without fit check | Compare alternatives against project constraints |
| Unexplained contiguous block > limit | Run `warden-lint.js`, split if needed |
| Skipped Blast Radius Check before a rewrite | Run check before proceeding |
| Claimed completion without verification evidence | Run relevant checks or state residual risk |
| Changed dependencies without version/source evidence | Stop, inspect package metadata and lockfile |
| Edited in a dirty repo without checking ownership | Inspect status and preserve user changes |
| No `[AWAITING CONFIRMATION]` before >2-file change | Pause and request confirmation |
| Monolithic file output without module split | Refactor into separated concerns |

All limits and thresholds are defined in `codewarden.json`.
