---
name: chameleon-disable
description: Use when the user explicitly invokes /chameleon-disable to suppress chameleon's advisory injections for the rest of the current session
---

# /chameleon-disable

Disable chameleon's advisory injections for the current session. Hook stack still fires (safety hard-deny preserved) but no `<chameleon-context>` content is injected.

## When to use

- User runs `/chameleon-disable` (or `/cham-disable`) explicitly
- User expresses frustration with chameleon's latency or pattern advice (the `callout-detector` hook surfaces this command on detected frustration)
- User is doing experimental / one-off work where conformance pressure is unwelcome

## Opt-out hierarchy

```
Most-permanent →    .chameleon/.skip (per-repo, all users, committed → team-wide)
                ↓   CHAMELEON_DISABLE=1   (per-user globally; in shell rc)
                ↓   /chameleon-disable    (this session only)
                ↓   /chameleon-pause-15m  (next 15 minutes)
Most-temporary
```

Use the most-temporary option that solves the immediate need. Revert by:
- `/chameleon-disable` → starts new Claude Code session
- `/chameleon-pause-15m` → expires automatically
- `CHAMELEON_DISABLE=1` → unset the env var
- `.chameleon/.skip` → remove the file from the repo

## The flow

1. Confirm chameleon is currently active in this session.
2. Call `chameleon-mcp::disable_session(repo=<repo_root>, session_id=<current session_id>)`.
3. The PreToolUse hook checks for the resulting `.session_disabled.<session_id>` marker before injecting; if present, skips.
4. Confirm to user: "chameleon disabled for this session. SessionStart primer will re-enable on next session unless you set CHAMELEON_DISABLE=1 globally or `.chameleon/.skip` in this repo."

## Don't suggest disable for the wrong problem

- Pattern advice is wrong → use `/chameleon-teach` instead
- Latency is too high → check `/chameleon-status --health` (Phase 4)
- One archetype's canonical is bad → edit `.chameleon/canonicals.json` directly OR use `/chameleon-refresh`
- Profile drift is causing churn → `/chameleon-refresh`

Disable is the escape hatch for situations where chameleon legitimately isn't useful in the moment, not a tool for fixing other problems.
