---
name: specdd-refactor
description: Use when Claude Code needs to refactor code, tests, docs, specs, or project structure in a SpecDD project while preserving specified behavior, public contracts, scenarios, ownership, and local write authority.
license: Apache-2.0
---

# SpecDD Refactor

Use this skill for structure changes that should not change specified behavior.

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

1. Identify public contracts, scenarios, invariants, dependencies, and forbidden boundaries.
2. Confirm write authority for every file that would move or change.
3. Prefer small mechanical steps with verification between risky changes.
4. Run baseline checks before refactoring when practical, then rerun after.

## Refactor Rules

- Preserve behavior described by active specs.
- Do not move responsibility across spec boundaries unless the specs or user request require it.
- Do not widen dependencies or add forbidden imports.
- Do not rename public symbols, paths, or contracts unless explicitly in scope.
- Update specs, docs, and tests only when the refactor changes structure they describe.

If behavior must change to complete the request, stop treating it as a pure
refactor and resolve authority for the behavior change.
