# VibeCollab — Setup Instructions for AI Assistants

You are helping a user set up VibeCollab in their project.
Execute the following steps in order. Stop and report if any step fails.

## Prerequisites

VibeCollab requires **Python 3.10 or higher**. Recommended version: **Python 3.12** (best balance of performance and compatibility).

Before installing, check the user's Python version:

```bash
python --version
```

If Python is not installed or is below 3.10, guide the user to install Python 3.12+ from https://www.python.org/downloads/

**Virtual environment** (strongly recommended): To keep the user's system clean and avoid dependency conflicts, always create a virtual environment before installing:

```bash
# Create a virtual environment (run once)
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

> If the project already has a virtual environment (`.venv/`, `venv/`, or similar), activate it instead of creating a new one.

## Step 1: Install

```bash
pip install vibe-collab
```

## Step 2: Initialize

Run in the user's project root directory:

```bash
vibecollab init -n "<PROJECT_NAME>" -d <DOMAIN>
```

- `<PROJECT_NAME>`: Ask the user for their project name
- `<DOMAIN>`: Ask the user to choose: `web` / `mobile` / `game` / `data` / `generic`

This creates `project.yaml`, `CONTRIBUTING_AI.md`, and `docs/` directory with protocol documents.

### For Existing Projects

If the project already has code (not an empty directory), do the following **after** `vibecollab init`:

1. **Backfill CONTEXT.md**: Review recent git commits and summarize the project's current state, active tasks, and recent decisions into `docs/CONTEXT.md`

2. **Backfill DECISIONS.md**: Look for important architectural choices in git history and record them in `docs/DECISIONS.md` with proper decision levels (S/A/B/C)

3. **Create ROADMAP.md**: If the project has future plans, create `docs/ROADMAP.md` following the milestone format (see ROADMAP Format section below)

4. **Capture Insights**: If reusable development experiences are found (debugging tricks, architectural patterns, workflow optimizations), capture them using `insight_add` MCP tool

### Quick Start After Init

After initialization completes, tell the user:

> VibeCollab is ready! Here's how to start:
> 
> 1. **Describe your current task** — I'll help you work on it while following the collaboration protocol
> 2. **Or say "onboard"** — I'll read the project context and suggest what to do next
> 3. **Or show me a file/feature** — I'll understand it within the project's structured context

This gives users an immediate path forward instead of leaving them wondering "what now?"

## Step 2.5: Install Git Hooks (Recommended)

Install the pre-commit hook to ensure every commit passes consistency checks:

```bash
vibecollab hooks install
```

**What it does:**
- Automatically runs `vibecollab check` before every `git commit`
- Validates insight fingerprints, protocol compliance, and document freshness
- Blocks the commit if critical errors are found (prevents bad commits)

**Why use it:**
- Catches consistency issues before they reach the repository
- Ensures all insights have valid fingerprints
- Maintains protocol compliance automatically

**If a commit is blocked:**
- Fix the reported errors (recommended)
- Or bypass with `git commit --no-verify` (emergency only)

> **Note**: If `vibecollab hooks` command is not available (older versions), the hook can be manually installed. The hook will be auto-installed in future versions during `vibecollab init`.

## Step 3: Connect MCP to IDE

Ask the user which IDE they use, then run:

```bash
vibecollab mcp inject --ide cursor   # or: cline / codebuddy / all
```

This injects VibeCollab MCP Server config into the IDE config file.
Use `--ide all` to inject config for all supported IDEs at once.

**OpenClaw / other MCP agents**: VibeCollab is a standard MCP Server. Any MCP-compatible agent can connect directly:

```bash
openclaw mcp add --transport stdio vibecollab vibecollab mcp serve
```

## Step 4: Verify

```bash
vibecollab check
```

Should return zero errors. Warnings about document staleness are normal for new projects. Insight consistency checks and guard protection checks are included by default (use `--no-insights` or `--no-guards` to skip).

## Setup Complete

VibeCollab is ready. You now have MCP tools available in your IDE:

| Tool | When to use |
|------|-------------|
| `onboard` | **Start of every conversation** — get project context |
| `check` | **End of every conversation** — verify protocol compliance |
| `next_step` | When unsure what to do next |
| `insight_search` | Search past development experience |
| `insight_add` | Save a reusable insight |
| `insight_suggest` | Get signal-driven insight recommendations |
| `insight_graph` | View insight relationship graph |
| `insight_export` | Export insights in YAML format |
| `insight_import` | Import insights from other projects |
| `search_docs` | Semantic search across project documents |
| `task_list` | List current tasks |
| `task_create` | Create a new task (auto-links insights, **permission-checked**) |
| `task_transition` | Move task status (TODO → IN_PROGRESS → REVIEW → DONE, **permission-checked**) |
| `task_solidify` | Solidify a task through validation gates |
| `guard_check` | Pre-flight check before file operations (block/warn/allow) |
| `guard_list_rules` | List all configured guard protection rules |
| `role_context` | Get a specific role's context (for multi-role projects) |
| `role_list` | List all roles and their permissions |
| `project_prompt` | Generate full context prompt |
| `roadmap_status` | View milestone progress |
| `roadmap_sync` | Sync ROADMAP.md <-> tasks.json |
| `session_save` | **End of conversation** — save session summary |

---

## Execution Plan — YAML-Driven Workflow Automation

### v0.12.0+ Best Practice: CLI-Driven Workflows

VibeCollab v0.12.0+ uses **CLI-driven workflows** where all actions are executed through `action: cli` steps:

```yaml
name: "Feature Development"
steps:
  # Guard check before file operations
  - action: cli
    command: "vibecollab guard check --operation create --file-path docs/"
    expect: { exit_code: 0 }
    on_fail: abort

  # Task lifecycle management
  - action: cli
    command: "vibecollab task create --id TASK-FEAT-001 --role DEV --feature 'Login System'"
    expect: { exit_code: 0 }

  # Role switching
  - action: cli
    command: "vibecollab role switch DEV"
    expect: { exit_code: 0 }

  # Execute micro-plan with prompts
  - action: cli
    command: "vibecollab plan run .vibecollab/plans/agents/dev/step-01.yaml"
    expect: { exit_code: 0 }

  # Task transition
  - action: cli
    command: "vibecollab task transition TASK-FEAT-001 IN_PROGRESS"
    expect: { exit_code: 0 }

  # Insight capture
  - action: cli
    command: 'vibecollab insight add --title "Login implementation" --tags "auth,security" --category technique'
    expect: { exit_code: 0 }
    on_fail: continue

  # Git commit
  - action: cli
    command: 'git add -A && git commit -m "[FEAT] Implement login"'
    expect: { exit_code: 0 }
    on_fail: continue
```

### Complete Workflow Best Practices

Every workflow should include these **essential steps**:

```yaml
# 1. Pre-flight checks
- action: cli
  command: "vibecollab hooks install"          # Ensure hooks are installed
- action: cli
  command: "vibecollab guard list-rules"       # Verify guard rules

# 2. Task creation
- action: cli
  command: "vibecollab task create --id TASK-XXX ..."

# 3. Guard check before operations
- action: cli
  command: "vibecollab guard check --operation modify --file-path <path>"

# 4. Role context management
- action: cli
  command: "vibecollab role switch <role>"
- action: cli
  command: "vibecollab role context --export ctx.json"

# 5. Execute micro-plan
- action: cli
  command: "vibecollab plan run <micro-plan.yaml>"

# 6. Task transition
- action: cli
  command: "vibecollab task transition TASK-XXX <status>"

# 7. Insight capture
- action: cli
  command: "vibecollab insight add --title ... --tags ..."

# 8. Git commit
- action: cli
  command: "git add -A && git commit -m '[PREFIX] Description'"

# 9. Final checks
- action: cli
  command: "vibecollab role sync"
- action: cli
  command: "vibecollab check"
```

### Plan Step Actions Reference

| Action | Purpose | Example |
|--------|---------|---------|
| `cli` | Run shell command | `command: "vibecollab check"` |
| `assert` | Check file/content | `file: "README.md"`, `contains: "test"` |
| `wait` | Delay | `seconds: 1` |
| `prompt` | Send single message to host | `message: "Create a task"` |
| `loop` | Multi-round iteration | `max_rounds: 20`, `state_command: "..."` |

### Micro-Plan Format (agents/*.yaml)

Micro-plans use `host: file_exchange` to enable `action: prompt`:

```yaml
name: "Requirement Analysis"
description: "Analyze requirements with Smart Probe"
host: file_exchange  # Required for prompt actions

# Soft-constraint fields (AI reads and follows)
smart_probe:
  dimensions:
    - name: "User Value"
      question: "Why do users need this?"
      max_score: 5

insights:
  required:
    - id: INS-011
      title: "Smart Probe Pattern"

on_complete:
  cli_actions:
    - "vibecollab insight add --title '...'"
  context_update:
    - "Update roles/producer/context.yaml"

steps:
  - action: prompt
    content: |
      ## Smart Probe Analysis
      
      Evaluate these dimensions:
      {{smart_probe.dimensions}}
```

---

## Soft-Constraint Fields in Plan YAML

The following fields in plan/micro-plan YAML are **soft constraints** — PlanRunner does not automatically execute them, but **AI should read and follow** them:

| Field | Location | Purpose | AI Action |
|-------|----------|---------|-----------|
| `smart_probe` | Micro-plan | 5-dimension scoring | Execute scoring after reading |
| `insights.required` | Micro-plan | Required insights to read | `vibecollab insight search` before step |
| `on_start` | Micro-plan | Pre-step setup | Execute CLI actions before main steps |
| `on_complete` | Micro-plan | Post-step cleanup | Execute CLI actions after main steps |
| `completion_criteria` | Micro-plan | Checklist to pass | Verify all items before transition |
| `transition` | Micro-plan | Next step routing | Follow next pointer if conditions met |
| `knowledge_capture` | Workflow | Insight suggestions | Create insight if valuable |
| `quality_gate` | Workflow step | Block if check fails | Run `vibecollab check --strict` |

### Soft-Constraint Execution Flow

```
AI reads micro-plan YAML
  │
  ├─ on_start → Execute CLI actions (软约束)
  │
  ├─ insights.required → Search and read insights (软约束)
  │
  ├─ smart_probe → Perform scoring (软约束)
  │
  ├─ steps → PlanRunner executes (硬执行)
  │     └─ action: prompt via host adapter
  │
  ├─ completion_criteria → Verify checklist (软约束)
  │
  ├─ on_complete → Execute CLI actions (软约束)
  │     └─ insight add, context update, git commit
  │
  └─ transition → Route to next step (软约束)
```

---

## Guard Protection System

Guards protect critical files from accidental operations:

### CLI Usage

```bash
# Check if operation is allowed
vibecollab guard check --operation delete --file-path "important.md"

# List all guard rules
vibecollab guard list-rules
```

### In Workflow

```yaml
- action: cli
  command: "vibecollab guard check --operation modify --file-path Assets/Scripts/"
  expect: { exit_code: 0 }
  on_fail: abort  # Stop workflow if guard blocks
```

### MCP Tool

AI should call `guard_check` before file operations:

```python
guard_check(operation="delete", file_path="docs/CONTEXT.md")
# Returns: { "allowed": true/false, "matched_rule": {...} }
```

---

## Git Hooks Integration

Hooks enforce quality gates at Git lifecycle points:

### Pre-commit Hook (Installed via `vibecollab hooks install`)

```bash
#!/bin/bash
# .git/hooks/pre-commit
vibecollab check --strict
if [ $? -ne 0 ]; then
    echo "❌ Commit blocked: fix errors or use --no-verify"
    exit 1
fi
```

### In Workflow

```yaml
# Ensure hooks are installed
- action: cli
  command: |
    if [ ! -f .git/hooks/pre-commit ]; then
      vibecollab hooks install
    fi
  expect: { exit_code: 0 }
```

---

## Task-Insight-Git Integration

### Complete Development Cycle

```
Conversation Start
  │
  ├─ vibecollab onboard           # Load context
  ├─ vibecollab role whoami       # Confirm role
  │
  ▼
Task Creation
  ├─ vibecollab task create --id TASK-FEAT-001 ...
  │
  ▼
Development Loop
  ├─ vibecollab guard check ...   # Pre-flight
  ├─ vibecollab insight search ... # Find relevant experience
  ├─ [Do the work]
  ├─ vibecollab task transition TASK-FEAT-001 IN_PROGRESS
  │
  ▼
Insight Capture
  ├─ vibecollab insight add --title "..." --tags "..."
  │
  ▼
Git Sync
  ├─ git add -A
  ├─ git commit -m "[FEAT] ..."   # Hook runs vibecollab check
  │
  ▼
Task Completion
  ├─ vibecollab task solidify TASK-FEAT-001
  ├─ vibecollab role sync
  ├─ vibecollab check
  └─ vibecollab session_save
```

---

## Daily Workflow

```
Conversation start → call onboard
                      ↓
                 Work on tasks
                      ↓
    Reusable experience? → call insight_add (capture knowledge)
                      ↓
    Need past experience? → call insight_search
                      ↓
    Important decisions → record in docs/DECISIONS.md
                      ↓
    Conversation end → update docs/CONTEXT.md
                     → update docs/CHANGELOG.md
                     → call check (includes Insight consistency + Guard protection by default)
                     → call session_save
                     → git commit
```

> **Key**: Insight and Guard checks are enabled by default in `check`. Every conversation should consider capturing reusable knowledge via `insight_add`.

---

## Best Practice: Task-Insight Iteration Cycle

When using `vibecollab --help` to drive development, follow this systematic workflow:

### 1. State Assessment
```bash
# Check current tasks and insights
vibecollab task list                    # View TODO tasks
vibecollab task suggest <TASK-ID>       # Get relevant insights
git status                              # Verify sync state
```

### 2. Task-Insight Loop
```
Select Task → Query Insights → Execute → Capture Insight → Git Sync
     ↑                                                    ↓
     └──────────────── Next Task ←──────────────←────────┘
```

**Pattern**: Always link tasks with insights:
- Before starting: `vibecollab task suggest <task>` to find relevant experience
- During work: Apply insights from registry (INS-XXX.yaml files)
- After completion: Create new insight via `vibecollab insight add` or manual INS-XXX.yaml

### 3. Git Synchronization Rules
- **Immediate**: After every insight creation (`git add .vibecollab/insights/`)
- **Batch**: After documentation updates (`git add docs/`)
- **Atomic**: One logical change = one commit with conventional format:
  ```
  feat(insight): INS-XXX brief description
  
  - Detail 1
  - Detail 2
  
  Refs: TASK-XXX
  ```

### 4. Documentation Update Sequence
1. **CHANGELOG.md**: Add to `[Unreleased]` section immediately
2. **ROADMAP.md**: Mark milestones, update task status
3. **Context files**: Update `docs/roles/<role>/CONTEXT.md`
4. **Re-index**: `vibecollab index` to update vector search

### 5. Continuous Accumulation
Each iteration should:
- ✅ Complete at least one task
- ✅ Create or update at least one insight
- ✅ Synchronize to git
- ✅ Update relevant documentation
- ✅ Verify with `vibecollab check`

---

## ROADMAP Format

If the project has a `docs/ROADMAP.md`, milestones must use this format for `roadmap_status` / `roadmap_sync` to work:

```markdown
### v0.1.0 - Milestone title

- [ ] Feature description (TASK-DEV-001)
- [x] Completed feature TASK-DEV-002
```

- Only `###` (H3) headers are recognized — `####` or `##` will not be parsed
- Version must start with `v` (semantic versioning)
- Task IDs follow `TASK-{ROLE}-{SEQ}` format (e.g., `TASK-DEV-001`)

---

## v0.12.3+ New Features: Step-by-Step Workflow Execution

### Single-Step Execution (v0.12.3+)

Execute workflows step by step with full state persistence:

```bash
# List all steps in a workflow
vibecollab plan steps daily-sync

# Execute a single step by index (0-based)
vibecollab plan step daily-sync 0

# Check execution status
vibecollab plan status daily-sync

# Resume from where you left off
vibecollab plan run daily-sync --resume

# Interactive mode: pause after each step
vibecollab plan run daily-sync --interactive

# Execute steps 2-4 only
vibecollab plan run daily-sync --from-step 2 --to-step 4

# Reset/clear saved state
vibecollab plan reset daily-sync --force
```

### Step Execution State Persistence

State is automatically saved to `.vibecollab/plan_state/<plan_name>.json`:

| Command | Purpose |
|---------|---------|
| `plan step <workflow> <index>` | Execute single step, save state |
| `plan status [workflow]` | Show execution progress |
| `plan reset <workflow>` | Clear saved state |

### Interactive Workflow Development

Perfect for AI agents working through complex workflows:

```bash
# 1. View all steps
vibecollab plan steps daily-sync

# 2. Execute first step
vibecollab plan step daily-sync 0

# 3. Check status (shows completed steps)
vibecollab plan status daily-sync

# 4. Continue with next step
vibecollab plan step daily-sync 1

# 5. Or resume full execution
vibecollab plan run daily-sync --resume
```

State persists across CLI invocations, allowing workflows to be completed across multiple sessions.

---

## v0.12.0+ New Features Summary

### YAML Document Management
- `vibecollab docs list` — List renderable documents
- `vibecollab docs render --all` — Render YAML to Markdown
- `vibecollab docs validate` — Validate YAML structure

### Workflow Automation
- `vibecollab plan list` — List available workflows
- `vibecollab plan run <workflow>` — Execute workflow
- `vibecollab plan validate <workflow>` — Validate syntax
- `vibecollab plan step <workflow> <index>` — Single-step execution (v0.12.3+)
- `vibecollab plan status <workflow>` — Check execution status (v0.12.3+)
- `vibecollab plan steps <workflow>` — List steps with status (v0.12.3+)
- `vibecollab plan reset <workflow>` — Reset execution state (v0.12.3+)

### CLI-Driven Best Practice
- All workflows use `action: cli` steps
- No custom actions (role_switch/check/decision) in workflow
- Task/Insight/Guard/Git commands as CLI steps
- Micro-plans use `host: file_exchange` for prompts

### Insight Derivation
- `vibecollab insight graph --show-derivation`
- `vibecollab insight derive --from-task TASK-XXX`

> **Note**: YAML files (`docs/*.yaml`) are the source of truth. Markdown files (`docs/*.md`) are generated views. Always edit YAML, render to Markdown.
