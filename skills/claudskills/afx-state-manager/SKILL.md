---
name: state-manager
description: Three-file state management for session continuity. Maintains STATE.md, DECISIONS.md, and PROGRESS.md as human-readable session context alongside the SQLite ticket database. Use this skill when updating workflow state, logging decisions, tracking session progress, or resuming work after a context break.
---

# State Manager Skill

**Version**: 1.0.0
**Category**: Session Management
**Type**: Hybrid (prompt-driven + shell script)

## Purpose

Provide human-readable session continuity across context windows. While the SQLite ticket database tracks ticket status, these three markdown files capture the *working context* that gets lost between sessions:

- **STATE.md** — What am I working on right now? What phase? Any blockers?
- **DECISIONS.md** — What did I decide and why? What alternatives did I reject?
- **PROGRESS.md** — What happened in each work session? What files changed?

These files are designed to be read by both humans and Claude Code. When a session resumes, reading STATE.md provides immediate context without re-analyzing the entire codebase.

## Operations

### update-state

Updates STATE.md with the current ticket, workflow phase, step, and any blockers.

**When to call:** At every phase boundary in the 16-step ticket-implementation workflow.

**Shell command:**
```bash
state-manager.sh update <ticket_id> <phase> <step> [blocker]
```

**Example:**
```bash
state-manager.sh update 2.3 implementation "implement_with_types"
state-manager.sh update 2.3 validation "run_tests" "Tests failing: missing test fixture for auth module"
```

**Phase values** (matching ticket-implementation workflow):
- `preparation` — Steps 1-4: validate state, get ticket, mark in progress, create branch
- `analysis` — Steps 5-7: read requirements, check API schema, list assumptions
- `implementation` — Steps 8-10: implement with types, follow patterns, handle edge cases
- `validation` — Steps 11-13: compile check, run tests, verify acceptance criteria
- `completion` — Steps 14-16: commit changes, mark done, report summary

### log-decision

Prepends a decision entry to DECISIONS.md with date, ticket ID, what was decided, and why.

**When to call:** Whenever making an architectural or implementation choice that future sessions should know about — especially choices where alternatives were considered and rejected.

**Shell command:**
```bash
state-manager.sh decision <ticket_id> "<decision>" "<rationale>"
```

**Example:**
```bash
state-manager.sh decision 2.3 "Use markdown files over YAML for state" "Human-readable, git-diff friendly, no parser dependency"
```

**What qualifies as a decision worth logging:**
- Choosing between two or more viable approaches
- Deviating from an existing pattern for a specific reason
- Accepting a trade-off (e.g., performance vs. simplicity)
- Ruling out an approach that looks obvious but has a hidden issue

**What does NOT need logging:**
- Following an established project pattern (that's expected behavior)
- Trivial formatting or naming choices
- Choices dictated by the ticket requirements with no real alternative

### log-session

Records session start and end in PROGRESS.md. Session-end captures changed files and a summary.

**When to call:**
- `session-start` — At the beginning of working on a ticket (after Step 3: mark in progress)
- `session-end` — When finishing a work session (after Step 16: report summary), or when context is about to be lost

**Shell commands:**
```bash
state-manager.sh session-start <ticket_id>
state-manager.sh session-end <ticket_id> "<summary>"
```

**Example:**
```bash
state-manager.sh session-start 2.3
# ... work happens ...
state-manager.sh session-end 2.3 "Implemented three-file state management: templates, shell script, skill docs"
```

Session-end automatically:
- Captures the list of changed files from git
- Resets STATE.md to idle status

### resume

Reads STATE.md and provides context for resuming work after a break or context loss.

**This operation is prompt-driven** (no shell command). When resuming:

1. Read `STATE.md` to understand current work context
2. Read the most recent entry in `PROGRESS.md` for session history
3. Read the most recent entries in `DECISIONS.md` for decision context
4. Check the ticket database for the active ticket's full details
5. Provide a concise summary:
   - What ticket is in progress
   - What phase and step was last reached
   - Any blockers noted
   - Key decisions made so far
   - Suggested next action

**Example resume summary:**

> Resuming ticket 2.3 (Three-file state management). Last session reached the **implementation** phase, step **follow_patterns**. No blockers. One decision logged: chose markdown over YAML for state files. Next action: continue implementing the shell script commands.

## Integration with the 16-Step Workflow

The state manager hooks into the ticket-implementation workflow at phase boundaries. Here is where each operation should be called:

| Step | Workflow Action | State Manager Call |
|------|----------------|-------------------|
| 3 | Mark ticket IN_PROGRESS | `session-start <ticket_id>` |
| 4 | Create feature branch | `update <ticket_id> preparation create_branch` |
| 5 | Read requirements | `update <ticket_id> analysis read_requirements` |
| 7 | List assumptions | `update <ticket_id> analysis list_assumptions` |
| 8 | Start implementing | `update <ticket_id> implementation implement_with_types` |
| 11 | Compile check | `update <ticket_id> validation compile_check` |
| 13 | Verify acceptance criteria | `update <ticket_id> validation verify_acceptance_criteria` |
| 14 | Commit changes | `update <ticket_id> completion commit_changes` |
| 16 | Report summary | `session-end <ticket_id> "<summary>"` |

Additionally, call `decision` at any point during implementation when a non-trivial architectural or implementation choice is made.

**You do not need to call update at every single step.** The table above shows the recommended phase-boundary checkpoints. If a step is quick and flows directly into the next, skip the intermediate update.

## Initialization

Before first use in a project, run:

```bash
state-manager.sh init
```

This copies the three templates to the project root. It skips files that already exist, so it is safe to run multiple times.

## File Locations

By default, state files live in the project root:
- `./STATE.md`
- `./DECISIONS.md`
- `./PROGRESS.md`

Override with environment variables: `STATE_FILE`, `DECISIONS_FILE`, `PROGRESS_FILE`.

## When NOT to Use This Skill

- For ticket status changes — use `ticket-manager.sh` for that
- For implementation logging — use `IMPLEMENTATION_LOG.md` for the permanent record
- For architecture documentation — use `ARCHITECTURE.md` and `ARCHITECTURE_CHANGES.md`

State files are *working context* that may be cleaned up between milestones. The ticket database and implementation log are the permanent record.
