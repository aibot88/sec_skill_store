---
name: roll-onboard
license: MIT
description: Interactive onboarding for legacy projects. Reads existing code, understands the project, asks 9 questions in 3 groups (cognition / scope / privacy), and writes .roll/onboard-plan.yaml as the contract for `roll init --apply` to execute.
---

# Roll Onboard

> Follows the Architecture Constraints, Development Discipline, and Engineering Common Sense defined in the project AGENTS.md.

Interactive onboarding flow for **legacy projects**: existing code that needs to adopt the Roll convention without disrupting how the team already works.

## Trigger

This skill runs when:

- `roll init` detected a legacy project (≥10 source files, no `AGENTS.md`)
- The CLI told the user to open an AI agent and run `$roll-onboard`
- The user has now invoked you here

## Hard responsibility boundary

You are the **认知 (cognition) layer**. Your job ends with writing a plan file.

| You do | You do NOT |
|--------|------------|
| Read project code, infer type/domains/modules | Modify any source file |
| Call `roll-doc --dry-run` to get a gap report | Call `roll-doc` (write mode) |
| Ask the user 9 questions across 3 groups | Decide for the user |
| Produce `.roll/onboard-plan.yaml` | Write `.gitignore` |
| Produce `.roll/onboard-plan.yaml` | Run `roll init --apply` |

Hard constraint: **AI cannot create files in the user's project other than `.roll/onboard-plan.yaml`.** Anything else is `bash`'s job (`roll init --apply`).

## Inputs you must read

1. The repository tree (use the project's own structure to infer technologies)
2. Any existing `README.md` / `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` etc. as evidence
3. `roll-doc --dry-run` output → identifies what documentation gaps exist
4. The path-audit pattern: scan for legacy structure markers (`BACKLOG.md`, `docs/features/`, etc.) — if any are present, REFUSE and tell the user to run `roll migrate` first

## Workflow

### Step 0 — Pre-flight

1. Check that you're in a legacy project root (no `AGENTS.md`, has source code)
2. If `BACKLOG.md` or `docs/features/` already present → STOP, tell user to run `roll migrate` first (this is a partial-migration project, not legacy)
3. Check `.roll/onboard-plan.yaml` doesn't already exist; if it does, ask user whether to overwrite

### Step 1 — Read code, build understanding

Walk the repo. Identify:
- **type**: one of `backend-service` / `frontend-only` / `fullstack` / `cli`
- **description**: 1-2 sentence summary of what this project does
- **domains**: top business/technical domains (e.g., "auth", "billing", "search")
- **key_modules**: top 3-5 modules that hold most of the logic

### Step 2 — Get gap report

Run `roll-doc --dry-run` (READ-ONLY mode). This reports:
- Which standard Roll artifacts (BACKLOG, features, domain models) are missing
- Which existing docs Roll could `include` rather than regenerate

### Step 3 — Three groups of nine questions

Present these in chat. **Aim for total time ≤ 3 minutes.** Group 1 confirms your understanding; group 2 scopes the work; group 3 handles privacy and next steps.

**Group 1 — Project cognition check**

1. I see this is a **[type]** project doing **[description]** — correct?
2. The main business domains look like **[domain A, domain B, …]** — anything to add or correct?
3. The key modules are **[X, Y, Z]** — any missed or mis-identified?

**Group 2 — Generation scope**

4. Which artifacts should I generate? Multi-select:
   - `backlog` — initial BACKLOG with seeded stories
   - `features` — features index + per-feature spec stubs
   - `domain` — DDD context map
   - `briefs` — directory for `$roll-brief` outputs
5. Of these existing docs, which should I `include` rather than regenerate?
   - (list candidates: README.md, docs/architecture.md, etc.)
6. Put drafts inside `.roll/`? (default: yes; "no" means use the legacy `docs/` layout — not recommended for new adoption)

**Group 3 — Privacy & next steps**

7. Add `.roll/` to `.gitignore`? (yes = keep project management private; no = commit it like Roll itself does)
8. Sync Roll conventions to which AI tools? Multi-select from detected agents (claude / cursor / codex / kimi / deepseek / pi / opencode / gemini / trae)
9. Enable `roll loop` autonomous execution after init?

### Step 4 — Write plan file

Write `.roll/onboard-plan.yaml` with this exact schema (validated by `lib/roll-plan-validate.py`):

```yaml
version: 1
generated_at: "2026-05-19T14:30:00+08:00"   # current ISO 8601, your timezone OK

project_understanding:
  type: cli                                  # one of: backend-service / frontend-only / fullstack / cli
  description: "..."
  domains: [...]
  key_modules: [...]

scope:
  approved: [backlog, features, domain]      # user's Q4 multi-select
  declined: [briefs]                         # what they said no to

include_existing:
  - README.md                                # user's Q5 selections
  - docs/architecture.md

privacy:
  gitignore_dot_roll: true                   # user's Q7

sync_targets: [claude, cursor]               # user's Q8
enable_loop: false                            # user's Q9
```

Then tell the user:

> Onboard conversation done. Plan saved to `.roll/onboard-plan.yaml`.
> Return to your terminal and run:
>
>     roll init --apply
>
> The plan expires in 24 hours.

### Step 5 — Stop

Do NOT run `roll init --apply` yourself. Do NOT modify other project files. Your job is done.

## When NOT to use

- **Not a legacy project**: empty dir or fresh project → use plain `roll init` instead
- **Has BACKLOG.md or docs/features/**: this is a pre-2.0 Roll project → run `roll migrate` first
- **Has .roll/ already**: already onboarded → don't re-run

## Failure modes

- User aborts mid-conversation → don't write partial plan; tell user to re-run from scratch
- User answers contradict the gap report (e.g., declines `features` but has lots of code) → ask the contradictory question once more before accepting; if they confirm, respect the choice
- You can't read enough code to fill `project_understanding` (e.g., binary repo) → write a placeholder plan but ask user to fill in `type` and `description` manually before applying
