---
name: docs-pipeline
domain: meta
description: |
  [PROTOCOL] Documentation backfill after an engagement changes
  code, architecture, deployment, or public contracts. Defines when to trigger,
  which doc files to update, and what the diff artefact must contain.
  Preloaded by lead agents (dev-lead, design-lead, marketing-lead). Pure
  reference — no triggers, not invoked by secretary.
---

# docs-pipeline

Orchestrates documentation backfill as a cross-cutting pipeline run by leads before handoff. Keeps project-knowledge in sync with the code/artefacts actually produced.

## Trigger — when to run

Lead MUST run docs-pipeline if the engagement changed ANY of:

| Domain | Trigger |
|---|---|
| dev | architecture (new service, layer, pattern), deployment (new target, env, secret), public API contract, build/CI topology, security posture, data model |
| design | brand voice/identity doc, design-system tokens/components, accessibility convention |
| marketing | brand voice/messaging, semantic core, reporting template, campaign pattern |

If engagement changed NONE of these, skip — but log "docs: no change" in `engagement/docs-diff.md`.

## Project-knowledge layout

Canonical path: `.claude/skills/project-knowledge/references/` in the project working directory.

| File | Owner content |
|---|---|
| `project.md` | project overview, stack, environments, contacts |
| `architecture.md` | system topology, services, layers, data flow |
| `patterns.md` | code conventions, naming, folder layout, git workflow |
| `deployment.md` | deploy targets, CI/CD pipeline, secrets table, rollback steps |
| `ux-guidelines.md` | interaction patterns, voice, accessibility standards |

Design engagements may add: `brand.md`, `design-system.md`.
Marketing engagements may add: `voice.md`, `semantic-core.md`, `campaigns-log.md`.

## Steps

### 1. Identify required updates

Lead diffs the engagement against existing docs:
- What decisions were made that are NOT in the docs yet?
- What code/pattern is now canonical that wasn't before?
- What operational step was added (new secret, new CI job, new rollback)?

List them in `engagement/docs-diff.md` under "Proposed updates".

### 2. Dispatch `dev-technical-writer`

Via Task tool. Pass:
- Absolute paths to the engagement artefacts (spec, PRs, decisions).
- Absolute path to `engagement/docs-diff.md` (proposed updates list).
- Absolute path to project-knowledge references directory.
- Engagement domain (dev / design / marketing).

Writer output: edits applied to references/*.md + a changelog section in `docs-diff.md` showing before/after per file.

### 3. Verify (lead)

Lead reads the diff. Checks:
- Every proposed update landed in the right file.
- No doc bloat (writer didn't add redundant sections).
- Code blocks contain only canonical snippets, not one-off engagement examples.
- No generic prose padding ("We value clean code. Our architecture is robust.").

If issues: re-dispatch writer with specific fix list. Max 2 writer re-dispatches per iteration.

### 4. `documentation-reviewer` pass

Dispatch `documentation-reviewer` via Task tool to check:
- Document quality against documentation-writing principles.
- No code blocks where prose suffices.
- Operational specifics present (paths, commands, secret names).
- No duplication across files.

Log verdict in `engagement/validation-log.md` under `documentation-reviewer`.

### 5. Record in docs-diff

`engagement/docs-diff.md` must contain by end of pipeline:

```markdown
# Docs diff — {engagement-name}

## Files changed
- `references/architecture.md` — added section §3 Service X
- `references/deployment.md` — added secret NEW_API_KEY + rollback for Service X
- `references/patterns.md` — no change (no new pattern introduced)

## Review
- documentation-reviewer verdict: clean (or N findings + resolutions)

## Not yet written
- {if anything was deferred with reason}
```

## Skip rules

Allowed skip scenarios — log in docs-diff:

| Case | Justified because |
|---|---|
| Pure bugfix with no new pattern | nothing to document |
| Refactor within existing module, no API change | convention already captured |
| Copy tweak on existing landing | brand voice doc already lists voice rules |

Director will verify the skip justification matches engagement scope. Do NOT skip to save time if change is user-visible or operationally relevant.

## Anti-patterns

- **Don't treat docs as optional.** Director rejects handoffs where architecture changed but `architecture.md` doesn't reflect it.
- **Don't dump code into docs.** Project-knowledge is prose + tables + short canonical snippets, not a code dump.
- **Don't write generic prose.** "We value clean code" is doc bloat. Write specifics: "Folder `src/services/` contains class-per-file, each class exports a single default."
- **Don't duplicate across files.** If `deployment.md` lists the pipeline, `patterns.md` references it — doesn't repeat it.
- **Don't skip `documentation-reviewer`.** Cheap check, catches rot.
