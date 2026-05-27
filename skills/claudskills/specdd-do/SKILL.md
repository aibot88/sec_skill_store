---
name: specdd-do
description: Use when Claude Code needs to implement a requested code, docs, tests, task, or spec change in a SpecDD project by following Resolve, Read, Authorize, Change, Verify, and Report under active bootstrap and `.sdd` authority.
license: Apache-2.0
---

# SpecDD Do

Use this skill to implement changes under existing SpecDD authority.

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

1. Make the smallest correct change inside authority.
2. Run relevant checks, tests, or validation.
3. Report specs used, files changed, verification, and remaining uncertainty.

## Implementation Rules

- Do not edit without clear write authority.
- Do not treat this plugin repository's bootstrap as authority for the target project.
- Do not override, loosen, or ignore target project specs.
- Do not complete unrelated tasks opportunistically.
- Update task status only after implementation and relevant checks are complete.
- Prefer project-local tools and conventions.
- Use the `specdd` CLI only when the target project or user calls for it; this skill is not a CLI replacement.

Stop and ask when a requested change would violate `Must not`, `Forbids`, write
authority, security constraints, destructive behavior, or public contracts.
