---
name: cross-layer-contract-audit
description: Audit client, API, database, and docs for contract mismatches. Use for schema drift, auth/session/payment changes, migrations, or integration regressions.
---

# Cross-Layer Contract Audit

Find mismatches between layers. Code and schema evidence outrank documentation.

## When To Use

Use this for cross-layer behavior where two or more implementation layers must agree.

Do not use this for a general repo status snapshot; use `project-status-dashboard`. Do not use it for planning a new feature from scratch; use `feature-spec-delivery-pipeline`.

## Scope

Adapt the layer map to the repo. Common layers include:

- Client models, forms, screens, state, and generated API clients.
- API routes, handlers, serializers, validators, and service methods.
- Database schema, migrations, views, policies, triggers, and seed data.
- Background jobs, queues, webhooks, and third-party integration contracts.
- Documentation and specs as supporting context only.

## Input Signals

Start from concrete signals such as changed files, failing tests, route names, migration names, API schemas, generated clients, UI forms, webhook payloads, or user-reported mismatches. If the user gives only a broad area, map the smallest boundary that can be verified end to end.

## Workflow

1. Identify the user-requested contract or feature area.
2. Map callers and callees across layers.
3. Compare:
   - Field names, types, nullability, defaults, enums, and units.
   - Required vs optional values.
   - Error formats and status codes.
   - Auth, permissions, tenancy, and ownership checks.
   - State transitions and side effects.
4. Revalidate each suspected mismatch against source files.
5. Produce a severity-ranked report.

For sample prompts and report shape, see `references/examples.md`.
For a compact field-by-field audit checklist, see `references/contract-checklist.md`.

## Output

For each finding:

- **Severity:** blocker, high, medium, low.
- **Contract:** the layer boundary that is inconsistent.
- **Evidence:** file paths, symbols, routes, migrations, or schema names.
- **Impact:** likely user or data effect.
- **Fix Direction:** smallest safe repair, noting which layer should change.
- **Verification:** targeted tests or commands that would prove the fix.

## Guardrails

- Do not trust docs as truth when implementation differs.
- Do not fix during the audit unless the user explicitly approves implementation changes.
- Flag unclear product behavior as an open question rather than deciding it.
- Treat auth, payments, sessions, data migration, and destructive changes as high-risk.

## Avoid

- Do not report a mismatch without naming both sides of the boundary.
- Do not collapse product uncertainty into an implementation recommendation.
- Do not broaden the audit into unrelated refactors.

## Final Checks

- Every finding has source-backed evidence.
- Each impact explains the likely user, data, or operational effect.
- Each fix direction names the layer that should change.
- Unknown product behavior is listed as an open question, not resolved by assumption.
