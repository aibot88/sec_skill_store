---
name: specdd-debug
description: Use when Claude Code needs to diagnose or fix a bug in a SpecDD project by reproducing or inspecting failure, comparing observed behavior to active `.sdd` contracts, and applying the smallest authorized fix.
license: Apache-2.0
---

# SpecDD Debug

Use this skill to diagnose failures against the specified contract.

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

1. Reproduce or inspect the failure before changing code when practical.
2. Compare observed behavior with applicable `Must`, `Must not`, `Scenario`, `Handles`, `Returns`, and `Raises` entries.
3. Identify whether the issue is implementation drift, test drift, spec ambiguity, or missing spec coverage.
4. Fix the smallest root cause inside write authority.
5. Add or update focused regression verification when appropriate.

## Debug Rules

- Do not change specs to match broken behavior unless the user asks for a spec change.
- Do not hide ambiguous public behavior behind implementation assumptions.
- Do not broaden error handling or dependencies beyond the governing specs.
- If the spec and observed desired behavior conflict, ask before editing.

Report the contract used, root cause, files changed, and verification result.
