---
name: mission-control-api-provider-mode
description: Use or explain API-provider mode through Mission Control. Use when the user explicitly wants API-backed execution, needs billing implications explained, or wants confirmation that configured secret storage rather than chat-provided keys will be used.
---

# Mission Control Api Provider Mode

## Purpose

Explain or request API-provider mode while keeping billing and secret handling explicit.

The Codex chat agent is not the Mission Control Manager. It is the bridge between the user and the Mission Control Manager.

## Use when

- The user explicitly wants API-backed providers.
- A configured API provider policy needs explanation.
- Billing and secret-storage implications matter.

## Workflow

1. Review current status and model policy.
2. Explain that API billing may apply and that raw keys should not be pasted into chat.
3. If the user still wants API-provider mode, route the request through Mission Control settings or task controls using configured secret storage only.

## Mission Control calls

Tools:
- `mission_control_get_status`
- `mission_control_start_task`

Resources:
- `mission-control://projects/{project_id}/status`

## User-facing output

- Warn about billing, explain the configured-secret-store expectation, and state whether API-provider mode is active or only requested.
- Keep the summary safe and non-secret-bearing.

## Approval behavior

Use explicit user awareness before switching to API-billed providers or any secret-backed mode.

## Never do

- Do not ask the user to paste raw keys into chat.
- Do not hide billing impact.
- Do not claim secure secret storage exists if Mission Control has not exposed it.

## Failure and fallback

If API-provider controls are not exposed yet, document the desired mode and keep the current provider policy unchanged until Mission Control can apply it safely.

## Example invocation

`Explain the API-provider mode for this Mission Control project.`
