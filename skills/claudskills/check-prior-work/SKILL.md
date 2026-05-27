---
name: check-prior-work
description: Use BEFORE starting any non-trivial coding task in an existing project — feature work, refactors, bugfixes, or "look at this codebase" requests. Triggers when the user asks to add/change/fix something inside a repo (e.g. "add X to the dashboard", "refactor the auth flow", "fix the bug in cost calculation", "why is this slow"). Surfaces recent prior sessions in the same project so the agent isn't redoing work or contradicting decisions made in past sessions.
---

# Check prior work in this project

## Why this skill exists

Claude Code sessions are stateless. The user has likely worked on this codebase before — possibly recently, possibly with a different agent — and made decisions, tried approaches, or left half-finished work. Diving straight into the new request risks duplicating effort, contradicting prior choices, or missing context the user assumes you have.

StackUnderflow indexes every prior Claude / Codex / Cursor session by `cwd`. One CLI call surfaces what's been done in this project recently.

## When this skill fires

Trigger on the FIRST substantive coding request in a project, when ANY of these hold:

- The user asks for new feature work, a refactor, or a bugfix in a repo (not a one-off question or read).
- The user says "let's continue", "pick up where we left off", or otherwise implies prior context.
- The cwd is a git repo with commits, AND the conversation has not already established what's been worked on recently.

Do NOT fire for:

- Pure read/explain questions ("what does this function do?")
- Greenfield work in an empty directory
- The user has already pasted a full HANDOFF / context block

## Step 1: surface prior sessions

Run from the project root (the user's cwd):

```bash
stackunderflow find-sessions-in-path "$(pwd)" --format json --limit 5 --since 30d
```

Optional flags:
- `--provider claude` to filter to Claude Code sessions only (default: all providers)
- `--limit N` if 5 isn't enough — bump to 10 if the repo is high-traffic
- `--since 7d` to tighten the window for fast-moving projects

The JSON shape (one entry per session):

```json
{
  "sessions": [
    {"session_id": "...", "project_slug": "...", "project_path": "/abs/path",
     "provider": "claude", "first_ts": "...", "last_ts": "...",
     "message_count": 42, "cost_usd": 0.85, "snippet": "first user message of the session"}
  ]
}
```

If `sessions` is empty: there's no prior history; proceed normally.

## Step 2: read the snippets

For each returned session, the `snippet` is the first user message — usually a one-line statement of what that session was for. Scan them for:

- **Same task already done** — "add agent-teams tab" might already be merged. Check before re-implementing.
- **Conflicting direction** — prior session went one way; user is now asking for the opposite. Surface the contradiction before coding.
- **Incomplete work** — last session may have stopped mid-feature. Pick up where it left off rather than starting fresh.
- **Decision context** — "we decided to use SQLite not Postgres" affects the new task even if it's about something else.

## Step 3: ground the new task

Once you have the prior context:

- If the user's new request conflicts with prior work, **ask them about it** before coding. Cite the session timestamp.
- If prior work is relevant background, mention it briefly ("I see last week's session added the X helper — I'll use that") and proceed.
- If nothing is relevant, just start the task. The check is cheap (one CLI call); finding nothing is a valid outcome.

## Showing the user vs. consuming internally

The default `--format json` is for the agent to consume. If the user explicitly asks "show me what we worked on recently" or "what was the last session about", run the human-readable form instead:

```bash
stackunderflow find-sessions-in-path "$(pwd)" --limit 10 --since 30d
# or for everything (omit --since):
stackunderflow find-sessions-in-path "$(pwd)" --limit 20
```

The text output is meant for the user to read directly — sessions sorted newest-first, with timestamps, message counts, and cost.

## Alternate path: MCP

If the StackUnderflow MCP server is connected, the equivalent tool is `find_sessions_in_path` with the same arguments. Skills target the CLI because it's universally available; MCP is faster when configured.

## Cost

The CLI hits a local SQLite store — no network, no LLM call. Latency: <100 ms even on a 200K-event store. Always cheap to run; never skip out of efficiency concerns.
