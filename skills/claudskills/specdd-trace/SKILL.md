---
name: specdd-trace
description: Use when Claude Code needs to map SpecDD specs to code, tests, docs, changed files, public behavior, references, verification coverage, or gaps while preserving the distinction between read context and write authority.
license: Apache-2.0
---

# SpecDD Trace

Use this skill to explain how specs, files, tests, and changes relate. Do not
edit files unless the user explicitly asks for changes.

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

1. Inspect implementation, tests, or diffs needed to connect contracts to behavior.
2. Identify the reason each file or spec is included.
3. Report missing links, stale specs, untested scenarios, or unclear authority.

## Trace Output

For each relevant item, identify:

- Why it was included, such as bootstrap, ancestor spec, nearest local spec, explicit reference, requested file, or changed file.
- The active constraints or behaviors it contributes.
- The code, tests, docs, or tasks that satisfy or fail to satisfy it.
- Any missing link, stale spec, untested scenario, or unclear authority.

Do not expand write authority. Referenced files remain read context unless the
active spec chain grants modification authority.
