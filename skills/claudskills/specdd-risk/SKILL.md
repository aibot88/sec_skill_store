---
name: specdd-risk
description: Use when Claude Code needs to classify risk before SpecDD work starts, especially around write authority, public contracts, security, data, migrations, dependencies, verification gaps, rollback, or destructive operations.
license: Apache-2.0
---

# SpecDD Risk

Use this skill before starting risky work or when the user asks for a risk call.
Do not edit files while assessing risk unless explicitly asked.

## Bootstrap Resolution

Before doing anything else in the target project, read bootstrap files in this exact order:

1. `.specdd/bootstrap.md`
2. `.specdd/bootstrap.project.md`, if it exists
3. `.specdd/bootstrap.local.md`, if it exists

Apply them in that order. Later files may narrow or specialize earlier rules, but must not silently weaken project contracts, inherited constraints, or write authority.

## Spec Chain Resolution

Before planning, editing, reviewing, testing, or reporting on a target:

1. Identify the target path, task, behavior, or changed files.
2. Resolve the effective spec chain using the active bootstrap rules.
3. Include same-directory basename specs when applicable.
4. Walk ancestor specs from the selected content root to the target.
5. Read explicit `References` only when they affect the requested work.
6. Identify the nearest local spec that grants write authority before any edit.

Do not infer authority from similar filenames, nearby files, symbols, module names, or conventions unless the active bootstrap or a governing spec explicitly defines that mapping.

## Workflow

1. Identify write authority and stop conditions.
2. Check affected public contracts, security boundaries, data shape, migrations, dependencies, and verification.
3. Classify risk as low, medium, or high with concrete reasons.

## Risk Factors

Raise risk when the change:

- Has unclear write authority or conflicting specs.
- Touches public APIs, persistent data, auth, secrets, payments, releases, or migrations.
- Crosses spec boundaries or changes ownership.
- Lacks tests for specified scenarios.
- Requires destructive operations or irreversible state changes.
- Depends on external systems, live credentials, or time-sensitive behavior.

End with the smallest safe next step and the verification needed before the work
can be considered complete.
