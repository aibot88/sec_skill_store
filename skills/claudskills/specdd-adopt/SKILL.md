---
name: specdd-adopt
description: Use when Claude Code needs to create, add, restructure, or improve SpecDD `.sdd` contract files, define ownership or write authority, clean up missing or unclear specs, or introduce SpecDD adoption without changing implementation unless explicitly requested.
license: Apache-2.0
---

# SpecDD Adopt

Use this skill to create or improve specs. Do not change implementation files
unless the user explicitly asks for implementation work too.

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

1. Read existing ancestor specs for the target area before adding new specs.
2. Identify the smallest useful spec boundary for the requested adoption work.
3. Treat the user's explicit request as target scope, then create or edit `.sdd` files only inside authority granted by the active spec chain.
4. Keep specs short, local, behavioral, and constraint-oriented.

## Adoption Rules

- Prefer a root or nearest-area spec before adding narrow child specs.
- Use path-based ownership and explicit `References`; do not imply authority from similar names or nearby files.
- Include only sections that add useful local authority, constraints, behavior, tasks, or context.
- Use `Can modify` or `Owns` to make write authority discoverable.
- Do not copy the full SpecDD framework rules into project specs.
- Do not turn uncertain observations into durable contracts.
- If write authority, ownership, public behavior, or security scope is unclear, stop and ask.

## Reporting

Report the bootstrap files read, specs created or changed, intended governing scope,
and any unresolved adoption decisions.
