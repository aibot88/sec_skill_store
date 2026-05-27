---
name: mission-control-github-ready-docs
description: Prepare Mission Control docs for public GitHub. Use when documentation should be cleaned for publication, internal AI notes removed, secrets and private paths scrubbed, and install or run guidance made public-ready.
---

# Mission Control Github Ready Docs

## Purpose

Prepare documentation for a public GitHub audience through Mission Control-aware review.

The Codex chat agent is not the Mission Control Manager. It is the bridge between the user and the Mission Control Manager.

## Use when

- The repo may go public.
- The user wants README-friendly documentation.
- Docs need secret and private-path cleanup before sharing.

## Workflow

1. Review handoff, codebase map, and current docs outputs.
2. Ask Mission Control to prepare GitHub-ready docs or treat the request as a docs-heavy change set.
3. Summarize what will be cleaned, added, or redacted before any file write.

## Mission Control calls

Tools:
- `mission_control_start_task`
- `mission_control_get_handoff_summary`

Resources:
- `mission-control://projects/{project_id}/handoff`
- `mission-control://projects/{project_id}/codebase-map`
- `mission-control://projects/{project_id}/risk-register`

## User-facing output

- Call out removal of internal AI notes, secrets, and private paths.
- Include install, run, test, limitations, and screenshot-placeholder expectations if relevant.

## Approval behavior

Ask before overwriting public-facing docs or removing existing internal notes that the user still wants preserved elsewhere.

## Never do

- Do not leak private paths or tokens.
- Do not leave internal-only AI workflow notes in public docs.
- Do not claim screenshots or examples exist if they do not.

## Failure and fallback

If no dedicated docs-publication tool exists, route the task through Mission Control with a docs-heavy and GitHub-ready objective, then summarize the planned cleanup items.

## Example invocation

`Use Mission Control to make the docs GitHub-ready.`
