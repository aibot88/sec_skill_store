---
name: mission-control-import
description: Use when Codex should attach an existing repo or folder to Mission Control and keep the first pass read-only until the user authorizes more.
---

# Mission Control Import

Use this skill when the user wants Mission Control to work on an existing codebase, imported folder, cloned repo, or documentation-heavy workspace.

## Bridge boundary

- Codex chat relays the import request and reports what Mission Control discovered.
- Codex chat is not allowed to treat an imported repo as implicitly approved for edits.
- Mission Control Manager decides what the imported codebase means and when it is ready for execution.

## Mission Control MCP tools to call

- `mission_control_import_folder`
- `mission_control_scan_codebase`
- `mission_control_get_codebase_understanding`
- `mission_control_get_import_safety`
- `mission_control_set_import_interview_choice`
- `mission_control_update_write_permission`
- `mission_control_send_manager_message`

## Mission Control resources it may read

- `mission-control://projects/current/summary`
- `mission-control://projects/current/codebase-map`
- `mission-control://projects/current/codebase-understanding`
- `mission-control://projects/current/import-safety`
- `mission-control://projects/current/agents-md/status`

## Decisions that must be passed to the user

- Which folder or repo to attach
- Which import interview mode to use: skip, quick clarification, full interview, or manager decides
- Whether Mission Control may move from read-only understanding to writable execution
- Whether suggested `AGENTS.md` guidance or import safety changes should be accepted

## Workflow

1. Attach the requested folder through `mission_control_import_folder`.
2. Run a read-only scan and understanding pass before any write path is considered.
3. Surface the import safety state, write-permission state, and interview choices to the user.
4. Send the user's import decisions back through the matching Mission Control tools.
5. Only after Mission Control and the user are aligned should Codex relay the real work request to the manager.

## Codex chat must not do

- Do not start editing just because the folder was imported successfully.
- Do not run builds, tests, installs, or dependency changes during import unless the user explicitly approves that path.
- Do not expose secrets from `.env`, credential files, or private config while summarizing the scan.
- Do not reinterpret a read-only scan as write approval.
