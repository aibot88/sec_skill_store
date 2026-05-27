---
name: project-state
description: Use when implementing project state detection, designing STATE.md/TASKS.md templates, or configuring SQLite state store and MCP state protocol
version: "1.0"
owner: platform-governance
tier: full
source: .enterprise/governance/agent-skills/project-state/SKILL.md
quick: .enterprise/governance/agent-skills/project-state/SKILL-QUICK.md
portable: true
---

# Project State — Full Reference

> Tier 2: detection algorithm, fallback chain, SQLite schema, MCP protocol, CLI toolkit, STATE.md/TASKS.md templates.

---

## 1. Mode Configuration

Set once during `hseos install`. Stored in `hseos.config.yaml`:

```yaml
state_management:
  mode: hybrid          # mcp-sqlite | cli-sqlite | skill-only | hybrid
  db_path: .hseos/state/project.db   # used by mcp-sqlite and cli-sqlite
  mcp_port: 3100        # used by mcp-sqlite
  fallback_chain:       # only used when mode = hybrid
    - mcp-sqlite
    - cli-sqlite
    - skill-only
```

---

## 2. Mode Descriptions

### 2.1 `mcp-sqlite` — Structured + Atomic
- MCP server at `localhost:3100` exposes tools: `state_read`, `state_write`, `tasks_list`, `tasks_update`
- SQLite backend: structured queries, transactions, history
- Best for: teams, multi-agent workflows, long-running epics
- Requires: `tools/mcp-project-state/` running (started via `hseos state start`)

### 2.2 `cli-sqlite` — Shell Toolkit
- Shell scripts (`tools/cli-project-state/project-state.sh`) and PowerShell (`project-state.ps1`)
- Same SQLite file, no server process required
- Best for: solo developers, CI pipelines, offline use
- Requires: `sqlite3` on PATH (bash) or `PSSQLite` module (PowerShell)

### 2.3 `skill-only` — Zero Infrastructure
- Direct markdown writes to `STATE.md` and `TASKS.md`
- No dependencies, no install, works everywhere
- Best for: minimal setup, quick projects, environments without tooling
- Limitations: no atomicity, no query capability, no history

### 2.4 `hybrid` — Auto-detect with Fallback
- Runtime detection at session start
- Falls back gracefully when a higher-tier backend is unavailable
- Fallback order: `mcp-sqlite` → `cli-sqlite` → `skill-only`

---

## 3. Hybrid Detection Algorithm

```
function detect_mode():
  config = load hseos.config.yaml → state_management
  if config.mode != hybrid:
    return config.mode

  // Try MCP
  probe = curl -s -o /dev/null -w "%{http_code}" http://localhost:{mcp_port}/health
  if probe == "200":
    return mcp-sqlite

  // Try CLI
  if which sqlite3 || which pwsh:
    if file_exists(config.db_path):
      return cli-sqlite
    if can_create(config.db_path):
      return cli-sqlite

  // Fallback
  return skill-only
```

Agents MUST run detection once per session and cache the result in working memory.

---

## 4. MCP Server Protocol

Server: `tools/mcp-project-state/index.js` (Node.js + better-sqlite3)

### 4.1 Tools exposed

| Tool | Description | Args |
|---|---|---|
| `state_read` | Get current STATE.md content as structured object | `{}` |
| `state_write` | Update one or more state fields atomically | `{ fields: {...} }` |
| `tasks_list` | List tasks with optional status filter | `{ status?: pending\|done\|blocked }` |
| `tasks_update` | Update task status and/or description | `{ id: string, status: string, note?: string }` |
| `tasks_add` | Add a new task to the backlog | `{ id: string, owner: string, description: string, depends?: string[] }` |
| `state_history` | Get last N state transitions | `{ n?: number }` |

### 4.2 Start / stop

```bash
hseos state start    # starts MCP server in background (port 3100)
hseos state stop     # stops MCP server
hseos state status   # shows mode, backend, db path, server status
```

### 4.3 SQLite schema

```sql
CREATE TABLE state (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE tasks (
  id TEXT PRIMARY KEY,
  owner TEXT NOT NULL,
  description TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',  -- pending | done | blocked
  depends_on TEXT,  -- JSON array of task IDs
  note TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE state_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  key TEXT NOT NULL,
  old_value TEXT,
  new_value TEXT NOT NULL,
  changed_by TEXT NOT NULL,  -- agent code
  changed_at TEXT NOT NULL DEFAULT (datetime('now'))
);
```

---

## 5. CLI Toolkit

### 5.1 Bash — `tools/cli-project-state/project-state.sh`

```bash
./project-state.sh state read
./project-state.sh state write branch feature/my-feature
./project-state.sh state write phase execution
./project-state.sh tasks list
./project-state.sh tasks list --status pending
./project-state.sh tasks add T5 GHOST "Implement auth endpoint"
./project-state.sh tasks done T5
./project-state.sh tasks block T6 "waiting on T5"
```

### 5.2 PowerShell — `tools/cli-project-state/project-state.ps1`

```powershell
./project-state.ps1 state read
./project-state.ps1 state write -key branch -value feature/my-feature
./project-state.ps1 tasks list
./project-state.ps1 tasks add -id T5 -owner GHOST -desc "Implement auth endpoint"
./project-state.ps1 tasks done -id T5
```

---

## 6. STATE.md Template

Location: `STATE.md` (project root)

```markdown
# Project State

> Managed by HSEOS. Do not edit manually — use `hseos state write` or let agents update this.
> Last updated: {{updated_at}}

## Current State

- **branch:** {{branch}}
- **epic_id:** {{epic_id}}
- **phase:** {{phase}}
- **active_agent:** {{active_agent}}
- **status:** {{status}}
- **last_updated:** {{last_updated}}

## Features

| ID | Feature | Status | Branch |
|---|---|---|---|
| F1 | {{name}} | {{status}} | {{branch}} |

## Deployment

| Environment | Version | Status | Last Deploy |
|---|---|---|---|
| dev | {{version}} | {{status}} | {{timestamp}} |
| staging | — | — | — |
| prod | — | — | — |

## Notes

{{freeform notes — cleared on each phase transition}}
```

---

## 7. TASKS.md Template

Location: `TASKS.md` (project root)

```markdown
# Task Backlog

> Managed by HSEOS. Agents update this file on every task transition.
> Prune completed tasks when > 5 done and no open task depends on them.

## In Progress

- [~] T{{id}} — [{{owner}}] {{description}} *(depends: {{deps}})*

## Pending

- [ ] T{{id}} — [{{owner}}] {{description}} *(depends: {{deps}})*

## Blocked

- [~] T{{id}} — [{{owner}}] {{description}} — **Blocked:** {{reason}}

## Completed (last sprint)

- [x] T{{id}} — [{{owner}}] {{description}}
```

---

## 8. Agent Responsibilities

| Agent | STATE.md writes | TASKS.md writes |
|---|---|---|
| ORBIT | phase, active_agent, status, epic_id | tasks_add (all tasks at epic start) |
| NYX | phase=discovery | tasks_update (discovery tasks) |
| VECTOR | phase=planning | tasks_update (planning tasks) |
| CIPHER | phase=solutioning | tasks_update (design tasks) |
| RAZOR | phase=coordination | tasks_update (sprint tasks) |
| GHOST | active_agent, phase=execution | tasks_update (story tasks) |
| GLITCH | phase=validation | tasks_update (QA tasks) |
| FORGE | phase=release | tasks_update (release tasks) |
| KUBE | phase=gitops, deployment row | tasks_update (deploy tasks) |
| SABLE | status (healthy/degraded) | tasks_update (runtime tasks) |
| QUILL | phase=knowledge | tasks_update (docs tasks) |

---

## 9. Escalation

Escalate (inform user) when:
- Hybrid detection falls back from MCP to CLI (log warning: "MCP unavailable, using CLI")
- Hybrid detection falls back from CLI to skill-only (log warning: "CLI unavailable, using markdown")
- STATE.md or TASKS.md is absent and the project config expects them
- Concurrent write conflict detected (two agents wrote in the same minute — check timestamps)


## Quick Mode

For low-context activation, load `.enterprise/governance/agent-skills/project-state/SKILL-QUICK.md` or `QUICK.md` first. Load this full skill for deep analysis, violation fixing, or formal review gates.

