---
name: mission-control-codex-cli-mode
description: Use or prefer Codex CLI runner mode through Mission Control. Use when the user wants Codex CLI as the runner, needs its status explained, or wants the distinction between subscription auth and API-based providers kept clear.
---

# Mission Control Codex Cli Mode

## Purpose

Explain or request Codex CLI runner mode while preserving local auth and approval boundaries.

The Codex chat agent is not the Mission Control Manager. It is the bridge between the user and the Mission Control Manager.

## Use when

- The user asks for Codex CLI mode.
- Runner selection is being reviewed.
- The user is confused about local Codex login versus API-billed mode.

## Workflow

1. Check Mission Control status for Codex CLI runner availability.
2. Explain runner availability, login state if surfaced, and the difference between local Codex auth and API provider mode.
3. Route any runner-policy change through Mission Control controls.

## Mission Control calls

Tools:
- `mission_control_get_status`
- `mission_control_start_task`

Resources:
- `mission-control://projects/{project_id}/status`

## User-facing output

- Summarize Codex CLI availability, auth posture, and fallback if unavailable.
- Preserve the distinction between subscription-backed local auth and API-billed provider modes when relevant.

## Approval behavior

Changing runner mode may affect cost or behavior, so confirm it before requesting the switch.

## Never do

- Do not ask for raw API keys for Codex CLI mode.
- Do not break local Codex auth by improvising a replacement flow.
- Do not claim CLI availability without verification.

## Failure and fallback

If Mission Control does not expose Codex CLI status yet, mark it as expected or future and preserve the current runner choice.

## Example invocation

`Check whether Mission Control can run this project in Codex CLI mode.`
