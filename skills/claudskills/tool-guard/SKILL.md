---
name: tool-guard
description: >-
  Allowlist/denylist for AI agent tool calls with approval gates for destructive
  operations. Define which tools the agent can use freely, which require
  confirmation, and which are blocked entirely. Combines LOCO-Agent's resource
  authorization with Flare's anomaly-aware security heuristics.
  Trigger phrases: "restrict tools", "tool permissions", "block bash",
  "approval gate", "limit what you can do", "tool whitelist", "tool blacklist".
argument-hint: "[allow|deny|gate] [tool-name]"
---

# Tool Guard

Control which tools the agent can use and which need approval.

## When to Use

- User wants to restrict the agent's capabilities for a sensitive task
- Working in production environments where certain operations are dangerous
- Reviewing unfamiliar code where unrestricted shell access is risky
- Pair programming where the user wants to approve every write/edit

## Commands

Parse arguments to configure tool permissions:

- `/tool-guard allow Read,Grep,Glob` — only these tools, deny everything else
- `/tool-guard deny Bash` — block Bash, allow everything else
- `/tool-guard gate Edit,Write` — allow these tools but ask before each use
- `/tool-guard gate Bash --pattern "rm|kill|drop|chmod"` — gate Bash only for matching commands
- `/tool-guard status` — show current permissions
- `/tool-guard reset` — clear all restrictions

## Permission Levels

### Allow (default for all tools)
Tool can be used freely without notification.

### Gate
Tool can be used, but the agent must explain what it's about to do and wait
for user confirmation before proceeding.

Gate prompt format:
```
🔒 Tool Guard: requesting [tool-name]
   Action: [what the tool call will do, in plain English]
   Target: [file path, command, or URL]
   Why: [how this serves the current task]
   Proceed? (y/n)
```

### Deny
Tool cannot be used. If the task requires it, explain to the user what you
need and why, and ask them to either run the command themselves or adjust
permissions.

## Preset Profiles

For convenience, support named profiles:

### `readonly`
- Allow: Read, Grep, Glob, Agent
- Gate: (none)
- Deny: Edit, Write, Bash, NotebookEdit

### `careful`
- Allow: Read, Grep, Glob
- Gate: Edit, Write, Bash, Agent
- Deny: (none)

### `untrusted-repo`
- Allow: Read, Grep, Glob
- Gate: Edit, Write
- Deny: Bash (no shell execution in untrusted code)

### `production`
- Allow: Read, Grep, Glob
- Gate: Edit, Write, Bash (every shell command needs approval)
- Deny: (none, but all mutations gated)

Usage: `/tool-guard profile readonly`

## Contextual Gating

Beyond static rules, apply contextual awareness:

1. **Path-based gating**: Gate writes to sensitive paths even if Write is allowed
   - `.env*`, `*.key`, `*.pem`, `credentials*` — always gate
   - `**/config/production*` — always gate
   - `.claude/`, `.cursor/` — gate (agent config modification)

2. **Command-based gating**: When Bash is allowed, still gate commands matching:
   - Destructive patterns: `rm -rf`, `git push --force`, `DROP TABLE`
   - Network egress: `curl -X POST`, `wget --post-data`, `scp`
   - Privilege escalation: `sudo`, `chmod 777`, `chown`
   - Package publishing: `npm publish`, `pip upload`

3. **Escalation**: If the same tool is gated 3+ times in a row and the user
   approves each time, suggest: "You've approved [tool] 3 times — want me to
   allow it for the rest of this session?"

## Status Report

When the user asks `/tool-guard status`:

```
## Tool Guard Status

Profile: careful (custom modifications)

| Tool    | Permission | Notes                          |
|---------|------------|--------------------------------|
| Read    | ✓ Allow    |                                |
| Grep    | ✓ Allow    |                                |
| Glob    | ✓ Allow    |                                |
| Edit    | 🔒 Gate    | Approved 2x this session       |
| Write   | 🔒 Gate    |                                |
| Bash    | 🔒 Gate    | + deny pattern: rm|kill|drop   |
| Agent   | ✓ Allow    |                                |

Gated calls this session: 4 (3 approved, 1 skipped)
```

## Behavior

- Tool Guard is advisory — it instructs the agent to self-restrict, not a
  system-level enforcement mechanism. The agent follows these rules because
  they are well-structured instructions, not because they are technically
  enforced.
- Always explain what you would have done with a denied tool, so the user
  can take that action themselves if needed.
- Never try to work around a denied tool by using a different tool for the
  same purpose (e.g., using Bash `cat` when Read is denied).
- Persist permissions for the duration of the session. They reset when the
  conversation ends.
