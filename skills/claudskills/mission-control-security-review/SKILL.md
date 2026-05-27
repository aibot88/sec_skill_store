---
name: mission-control-security-review
description: Ask Mission Control for a security review. Use when the user wants secrets risk, auth risk, dependency risk, command safety, file permission risk, deployment exposure, risky code patterns, or remediation planning summarized through Mission Control.
---

# Mission Control Security Review

## Purpose

Request or summarize a Mission Control security review without exposing secrets.

The Codex chat agent is not the Mission Control Manager. It is the bridge between the user and the Mission Control Manager.

## Use when

- The user asks for a security review.
- A release or handoff should include security posture.
- A risky codebase needs threat-focused triage.

## Workflow

1. Request a security review through Mission Control.
2. Read status, diagnostics, and risk resources.
3. Summarize the findings across secrets, auth, dependencies, permissions, deployment exposure, and risky patterns.
4. Return remediation steps and any user decisions needed.

## Mission Control calls

Tools:
- `mission_control_start_task`
- `mission_control_get_status`

Resources:
- `mission-control://projects/{project_id}/risk-register`
- `mission-control://projects/{project_id}/diagnostics`
- `mission-control://projects/{project_id}/status`

## User-facing output

- Cover secrets risk, auth or session issues, dependency risk, command safety, file permission risk, deployment exposure, risky code patterns, and remediation plan.
- Keep secrets redacted and findings bridge-safe.

## Approval behavior

If remediation implies destructive changes, deployment toggles, or tool-policy changes, present them as approvals rather than applying them silently.

## Never do

- Do not paste secrets or vulnerable payloads into chat.
- Do not claim a clean bill of health without evidence.
- Do not replace a real review with vague reassurance.

## Failure and fallback

If dedicated security review tooling is not exposed yet, route the request through Manager-led task execution and summarize backed findings from risk and diagnostics resources.

## Example invocation

`Ask Mission Control for a security review of this project.`
