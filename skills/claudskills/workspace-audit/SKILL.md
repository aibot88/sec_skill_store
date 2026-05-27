---
name: workspace-audit
description: Audit all git repos under ~/dev for dirty state, unpushed commits, exposed .env files, and tracked context files (CLAUDE.md, AGENTS.md, GEMINI.md). Use when the user wants to know if their workspace is clean, before a deploy, or when something feels off. Triggers on "audit workspace", "check repos", "anything unpushed", "is my workspace clean", "check for dirty repos", "any exposed secrets".
compatibility: Designed for Claude Code on WSL. Requires git, find, and repos under ~/dev.
allowed-tools: Bash Read
---

# Workspace Audit

Scans all git repos under `~/dev` for issues that need attention. The script handles all detection — your job is to synthesize the output and tell the user what needs action.

## Step 1 — Collect

```bash
~/.claude/commands/workspace-audit/scripts/audit.sh
```

## Step 2 — Synthesize

Read the labeled sections and produce a concise report:

### Git Repos
List every `NEEDS ATTENTION` entry with its flags. Group by type:
- **DIRTY** — uncommitted changes
- **UNTRACKED** — files not in git
- **NO-REMOTE** — no origin configured
- **AHEAD:N** — commits not pushed

Clean repos don't need a mention unless the user asks.

### Security Checks
Report any `EXPOSED:` .env files or `TRACKED:` context files immediately — these are high-priority.

### Disk Usage
Report `~/dev/` total size.

### Summary
- N repos clean, N repos need attention
- If `STATUS: CLEAN` → tell the user everything looks good
- If `STATUS: NEEDS ATTENTION` → list the top actions in priority order

Keep it tight. Flag security issues first, then unpushed work, then cosmetic.
