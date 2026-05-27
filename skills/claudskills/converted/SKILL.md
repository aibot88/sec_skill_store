---
name: api-crud-generator
description: "Generate production-ready CRUD REST API endpoints with validation, auth, error handling, pagination, tests, and OpenAPI docs. Auto-triggers when asked to create API endpoints, REST resources, or backend CRUD operations."
---

# API CRUD Generator

When this skill triggers, execute the following gated pipeline.
One step at a time. Do NOT skip ahead.

## Pipeline

1. **Scope** -- Read `references/01-scope.md`. Detect stack, define resource.
2. **Plan** -- Read `references/02-plan.md`. Map endpoints, auth, and file layout.
3. **Build** -- Read `references/03a-build-endpoints.md` then `references/03b-build-infra.md`. Generate code.
4. **Check** -- Read `references/04-check.md`. Answer every gate question YES or NO. Any NO = fix.
5. **Deliver** -- Read `references/05-deliver.md`. Finalize and present.

## Failure Log

Read `failure-log.md` before starting. Every pattern is a mandatory constraint.

## Rules

- Read each reference file when you reach that step, not all at once.
- Step 4 (Check) is the hard gate. "Mostly yes" counts as NO.
- On Check failure: fix, re-run full checklist, append pattern to `failure-log.md`.
