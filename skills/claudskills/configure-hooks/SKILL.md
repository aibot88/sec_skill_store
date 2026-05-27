---
name: configure-hooks
description: This skill should be used when the user says "configure hooks", "set up quality gates", "add PostToolUse hook", "set up permission hooks", "create hook configuration", "add typecheck hook", "set up secret-scan hook", or wants to configure event-driven hooks for their Claude Code project. Validates against the documented Claude Code event list — catches fictional event names before they end up in settings.json.
argument-hint: "[--project path/to/project] [--hooks quality-gates,typecheck-on-edit,format-on-write,secret-scan,compact-restore]"
user-invocable: true
allowed-tools: Read Glob Grep Write Edit Bash
---

# Configure Hooks

Set up event-driven hooks in `.claude/settings.json`. Hooks execute external commands; their exit codes mechanically affect agent behavior in ways that CLAUDE.md instructions cannot.

**This skill is paired with `validate-hooks.py`.** After writing the config, the skill runs the validator to catch any fictional event names — earlier versions of this plugin propagated four hook events that don't actually exist in Claude Code (`PostToolUseFailure`, `SubagentStart`, `Setup`, `InstructionsLoaded`).

## Source

- Hook event list and semantics: [Claude Code Hooks Reference](https://docs.claude.com/en/docs/claude-code/hooks) (verified April 2026)
- Exit code semantics, matcher behavior, parallel execution: same source

## Hook event semantics (verified April 2026)

```
Exit 0  →  Proceed (stdout added to context for some events; parsed as JSON if applicable)
Exit 2  →  Block the action; stderr becomes feedback to Claude
Other   →  Logged as non-blocking error; stderr shown to Claude
```

Note: Exit `1` is treated as non-blocking error — **not** as "failure" in the Unix sense. If you want to block, use exit `2`.

## Documented hook events

These are the only events Claude Code fires (April 2026). Use any other name and the hook will silently never fire.

| Event | When | Matcher? | Exit 2 blocks? |
|---|---|---|---|
| `PreToolUse` | Before tool executes | Yes | Yes |
| `PostToolUse` | After tool succeeds | Yes | No (tool already ran) |
| `UserPromptSubmit` | User submits prompt | No | Yes |
| `SessionStart` | Session begins or resumes from compact | Yes (`compact`) | No |
| `SessionEnd` | Session ends | No | No |
| `Stop` | Agent about to stop | No | Yes (loop risk — needs guard) |
| `SubagentStop` | Sub-agent completes | No | No |
| `PreCompact` | Before context compaction | No | No |
| `Notification` | Permission prompt, idle, auth, elicitation | No | No |
| `PermissionRequest` | Permission dialog appears | No | No |
| `ConfigChange` | Settings file modified | No | No |
| `WorktreeCreate` / `WorktreeRemove` | Git worktree events | No | No |
| `TeammateIdle` *(Agent Teams, experimental)* | Teammate going idle | No | Yes (keeps teammate working) |
| `TaskCompleted` *(Agent Teams, experimental)* | Task being marked complete | No | Yes (prevents completion) |

**Matcher behavior** (often misunderstood): the `matcher` field uses **exact string match** when no special characters are present. Regex matching kicks in only when the value contains regex metacharacters like `|`, `^`, `$`, `.*`. So `"Bash"` matches the Bash tool exactly; `"Edit|Write"` matches either; `"^Notebook"` is regex.

## Standard hook patterns

### Quality gate on TaskCompleted (experimental — Agent Teams only)

Runs typecheck + tests when a teammate marks a task complete. Blocks completion if either fails. **Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.**

```json
{
  "hooks": {
    "TaskCompleted": [{
      "hooks": [{
        "type": "command",
        "command": "cd \"$CLAUDE_PROJECT_DIR\" && npm run typecheck 2>&1 | tail -20; TC=$?; npm test 2>&1 | tail -30; TEST=$?; if [ $TC -ne 0 ] || [ $TEST -ne 0 ]; then echo 'BLOCKED: typecheck or tests failed' >&2; exit 2; fi",
        "timeout": 120
      }]
    }]
  }
}
```

### Typecheck on edit (PostToolUse)

Warns (does not block — PostToolUse can't block) when an edit introduces TypeScript errors:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "cd \"$CLAUDE_PROJECT_DIR\" && npm run typecheck 2>&1 | tail -5; if [ $? -ne 0 ]; then echo 'Warning: TypeScript errors after edit' >&2; fi; exit 0",
        "timeout": 30
      }]
    }]
  }
}
```

### Context restoration after compaction (SessionStart)

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "compact",
      "hooks": [{
        "type": "command",
        "command": "echo 'Reminder: current sprint focus is [SPRINT_GOAL]. Use the project agents for implementation.'"
      }]
    }]
  }
}
```

### Secret scan before write (PreToolUse)

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "echo \"$TOOL_INPUT_CONTENT\" | grep -iE '(api[_-]?key|secret|password|token)\\s*[=:]\\s*[\"'\\'']?[A-Za-z0-9+/]{20,}' && echo 'BLOCKED: possible secret in content' >&2 && exit 2 || exit 0",
        "timeout": 5
      }]
    }]
  }
}
```

### Stop hook with guard (avoid infinite loop)

If you want a Stop hook that exits 2 sometimes (preventing the agent from stopping), use a sentinel file or counter to ensure the hook eventually allows the stop:

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "COUNT=$(cat /tmp/stop-count 2>/dev/null || echo 0); if [ $COUNT -ge 3 ]; then rm -f /tmp/stop-count; exit 0; fi; echo $((COUNT+1)) > /tmp/stop-count; echo 'Continuing — N more cycles allowed' >&2; exit 2",
        "timeout": 5
      }]
    }]
  }
}
```

Without the guard, an unconditional `exit 2` on Stop creates an infinite loop. The validator script flags this pattern.

## Workflow

### Step 1: Determine target

Find `.claude/settings.json`. Read existing if present (so the merge preserves other config). Create otherwise.

### Step 2: Select hook patterns

Present the menu. If `--hooks` specifies a subset, use those. Standard options:

| Pattern | Event | Behavior |
|---|---|---|
| `quality-gates` | TaskCompleted (Agent Teams only) | Block completion if tests/typecheck fail |
| `typecheck-on-edit` | PostToolUse (Write\|Edit) | Warn on TypeScript errors after edits |
| `format-on-write` | PostToolUse (Write\|Edit) | Auto-format with Prettier |
| `secret-scan` | PreToolUse (Write\|Edit) | Block writes containing apparent secrets |
| `compact-restore` | SessionStart (compact) | Re-inject context after compaction |
| `stop-guard` | Stop | Loop guard pattern (use carefully) |

### Step 3: Customize commands per stack

- `npm run typecheck` → `pnpm typecheck`, `bun typecheck`, `mypy app/`
- `npm test` → `pnpm test`, `pytest`, `cargo test`
- Adjust timeouts based on test-suite duration

### Step 4: Merge into settings.json

Read existing `.claude/settings.json` (if any), merge in the new hook entries, preserve other config. Write the result.

### Step 5: Run the validator

```bash
python3 ${plugin_root}/scripts/validate-hooks.py <path-to-settings.json>
```

If the validator finds fictional events, broken handler shapes, or unguarded Stop-exit-2 patterns, surface them before declaring done. The validator is the safety net; do not skip this step.

### Step 6: Report

Tell the user:
- Which hooks were added
- What each will do (block / warn / inform)
- Important caveats (Agent Teams experimental flag if `TaskCompleted` was used; loop risk for unguarded Stop hooks)

## What this skill does NOT do

- Does not invent hook events. Anything not in the documented event list will be rejected by `validate-hooks.py`.
- Does not test that the hooks fire correctly — restart Claude Code and exercise the relevant tool to verify.
- Does not configure Agent Teams (experimental — see `agentic-operations` for the env var to enable).
- Does not handle hook removal — edit `settings.json` directly.

## Reference

- `references/hook-patterns.md` — Additional patterns (auto-format, advanced secret-scan, stop-guard variations)
