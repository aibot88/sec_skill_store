---
name: mission-control-release-prep
description: Prepare a project for release through Mission Control. Use when validation, docs, versioning, changelog, limitations, evidence, deployment readiness, and security concerns need one coordinated release-prep review.
---

# Mission Control Release Prep

## Purpose

Coordinate release-prep review through Mission Control without skipping evidence or approvals.

The Codex chat agent is not the Mission Control Manager. It is the bridge between the user and the Mission Control Manager.

## Use when

- The user asks if the project is ready to ship.
- A release candidate needs a final checklist.
- Docs, validation, and security all need coordinated review.

## Workflow

1. Review handoff, validation, risk, and status resources.
2. Ask Mission Control for a release-prep pass if needed.
3. Summarize validation, docs, versioning, changelog, limitations, evidence, deployment readiness, and security concerns.
4. Surface any remaining approvals or blockers.

## Mission Control calls

Tools:
- `mission_control_start_task`
- `mission_control_get_handoff_summary`
- `mission_control_get_status`

Resources:
- `mission-control://projects/{project_id}/handoff`
- `mission-control://projects/{project_id}/validation-summary`
- `mission-control://projects/{project_id}/risk-register`
- `mission-control://projects/{project_id}/status`

## User-facing output

- Give a release-readiness summary and list unresolved blockers.
- Be specific about whether versioning, changelog, docs, and security are complete or still thin.

## Approval behavior

If release-prep implies deployments, publishing, or policy shifts, keep those actions behind explicit approvals.

## Never do

- Do not announce release readiness without evidence.
- Do not skip limitations or unresolved risks.
- Do not publish anything from chat directly.

## Failure and fallback

If release-prep is not a dedicated workflow yet, synthesize the checklist from the available resources and clearly mark missing evidence.

## Example invocation

`Use Mission Control to do a release-prep review for this project.`
