---
name: chameleon-pause-15m
description: Use when the user explicitly invokes /chameleon-pause-15m to temporarily suppress chameleon's advisory injections for 15 minutes
---

# /chameleon-pause-15m

Pause chameleon's advisory injections for exactly 15 minutes. Auto-resumes after the timer expires. Use when latency is unwelcome for a short focused window (e.g., live coding, code review walkthrough, demo).

## When to use

- User is presenting / demoing and wants minimal hook latency
- User is doing rapid scratch experimentation in a TS repo
- User wants to compare AI output with vs without chameleon active over a short window
- Frustration detected → callout-detector hook surfaces this as a less-permanent option than `/chameleon-disable`

## When NOT to use

- The frustration is about pattern advice quality → `/chameleon-teach` to capture the missed pattern
- The frustration is about session-long latency → `/chameleon-disable` (session-scope) or check `/chameleon-status --health`

## The flow

1. Call `chameleon-mcp::pause_session(repo=<repo_root>, minutes=15)`.
2. The tool writes `${PLUGIN_DATA}/<repo_id>/.pause_until` with the ISO 8601 expiry.
3. PreToolUse hook checks `.pause_until`:
   - If file missing or expired → inject normally (auto-cleans expired markers)
   - If timestamp in future → skip injection
4. Confirm to user: "chameleon paused for 15 minutes (until <expires_at returned by the tool>). Will auto-resume."

## Opt-out hierarchy

See `chameleon-disable` skill for the full hierarchy. `pause-15m` is the most-temporary option.

## Implementation status

Hook integration is wired: preflight-and-advise calls `is_chameleon_suppressed` before injecting, which honors `.pause_until` (auto-expires), `.session_disabled.<session_id>`, `CHAMELEON_DISABLE=1`, and `.chameleon/.skip`.

## Future variants

If `15m` is the wrong duration for some users, future versions may add `/chameleon-pause-1h` and `/chameleon-pause-until-restart`. The `pause_session` MCP tool already accepts a `minutes` arg up to 240 (4 hours).
