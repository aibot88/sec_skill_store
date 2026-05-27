---
name: ticket-manager
description: SQLite-based ticket tracking for structured development workflows. Use this skill when the user asks to initialize a ticket database, import requirements, list tickets, get the next ticket to work on, mark tickets as done, or check ticket status. Essential for managing epics, user stories, and acceptance criteria.
---

# Ticket Manager Skill

**For Claude Code AI Assistant**

This skill provides SQLite-based ticket tracking for structured development workflows.

## Purpose

The ticket-manager skill enables systematic ticket-based development by:
- Storing tickets (epics and stories) in a local SQLite database
- Tracking ticket status (TO_DO, IN_PROGRESS, DONE, SHELVED)
- Managing acceptance criteria and technical notes
- Providing workflow commands for ticket progression

## Database Location

- Default: `./.artifex/tickets.db` in the project's Artifex directory
- Can be overridden with `TICKET_DB` environment variable

## Available Commands

### 1. Initialize Database

```bash
ticket-manager.sh init
```

Creates a new `.artifex/tickets.db` file with the schema. Use `init force` to recreate an existing database.

**When to use**: At project start, before importing requirements

### 2. Import Requirements

```bash
ticket-manager.sh import [--no-validate] requirements.json
```

Imports tickets from a requirements JSON file. For each story, both `acceptance_criteria` and `technical_notes` arrays are persisted into their respective tables; stories without a `technical_notes` field (or with an empty array) are imported cleanly with no warning, preserving backward compatibility with pre-10.8 requirements files. By default, each story is validated before insertion: acceptance criteria must be in Gherkin form (`Given ... When ... Then ...`), every story must have a non-empty title and id, and empty descriptions emit an informational note. Warnings and errors are written to stderr; a single summary line (`imported N epics, M stories, K technical notes, E errors, W warnings`) is written to stdout. Stories with errors are skipped; warnings do not block insertion. Pass `--no-validate` to disable all validation (useful when migrating a project whose tickets predate the Gherkin convention).

The expected JSON structure:

```json
{
  "epics": [
    {
      "id": "1",
      "title": "Epic Title",
      "description": "Epic description",
      "user_stories": [
        {
          "id": "1.1",
          "title": "Story Title",
          "description": "Story description",
          "complexity": "Medium",
          "implementation_order": 1,
          "acceptance_criteria": [
            "Given... When... Then..."
          ],
          "technical_notes": [
            "Optional implementation hint or constraint"
          ]
        }
      ]
    }
  ]
}
```

**When to use**: After database initialization, to load project tickets

### 3. Get Next Ticket

```bash
ticket-manager.sh next
```

Returns the next TO_DO story ordered by implementation_order and ID.

**Output includes**:
- Story ID, title, epic, complexity
- Full description
- Acceptance criteria

**When to use**: When ready to start implementing a new ticket

### 4. Update Ticket Status

```bash
ticket-manager.sh update <ticket_id> <status> [note]
```

Valid statuses: `TO_DO`, `IN_PROGRESS`, `DONE`, `SHELVED`

`SHELVED` is a terminal state for deliberately-parked tickets. Shelved stories:
- Are excluded from `next-ticket` selection (they won't be picked up as the next unit of work)
- Are excluded from epic progress denominators (a shelved ticket doesn't drag a phase's completion percentage down forever)
- Still appear in `show <id>` and `status` summaries so you can see why they were parked
- Use the tool's regular `update <id> SHELVED "<reason>"` path with a note explaining the trigger that would revive them

**Examples**:
```bash
# Mark ticket as in progress
ticket-manager.sh update 2.4 IN_PROGRESS "Starting implementation"

# Mark ticket as done
ticket-manager.sh update 2.4 DONE "Completed with tests"
```

**When to use**:
- When starting work (TO_DO → IN_PROGRESS)
- When completing work (IN_PROGRESS → DONE)
- When reverting status changes

### 5. Mark Ticket Done

```bash
ticket-manager.sh done <ticket_id> [note]
```

Shortcut for updating status to DONE.

**Example**:
```bash
ticket-manager.sh done 2.4 "Implemented with 95% test coverage"
```

**When to use**: At the end of ticket implementation workflow (Step 15-16)

### 6. Show Ticket Details

```bash
ticket-manager.sh show <ticket_id>
```

Displays complete ticket information:
- Title, epic, status, complexity
- Description
- Acceptance criteria
- Technical notes
- Implementation notes
- Status history with timestamps

**When to use**: When you need complete context about a specific ticket

### 7. Show Overall Status

```bash
ticket-manager.sh status
```

Shows summary statistics:
- Total stories count
- Breakdown by status (TO_DO, IN_PROGRESS, DONE, SHELVED) with percentages
- Progress per epic

**When to use**: To check project progress, report status

### 8. Export to JSON

```bash
ticket-manager.sh export [output.json]
```

Exports all tickets back to JSON format (default: `requirements-export.json`).

**When to use**:
- Creating backups
- Sharing ticket state
- Migrating to other systems

## Database Schema

### Tables

1. **epics** - Epic-level tickets
   - id (TEXT PRIMARY KEY)
   - title (TEXT)
   - description (TEXT)
   - created_at, updated_at (TIMESTAMP)

2. **stories** - User story tickets
   - id (TEXT PRIMARY KEY)
   - epic_id (TEXT, foreign key)
   - title (TEXT)
   - description (TEXT)
   - status (TEXT: TO_DO, IN_PROGRESS, DONE, SHELVED)
   - complexity (TEXT: Low, Medium, High, Very High)
   - implementation_order (INTEGER)
   - notes (TEXT)
   - created_at, updated_at (TIMESTAMP)

3. **acceptance_criteria** - Story acceptance criteria
   - id (INTEGER PRIMARY KEY)
   - story_id (TEXT, foreign key)
   - criterion (TEXT)
   - created_at (TIMESTAMP)

4. **technical_notes** - Technical implementation notes
   - id (INTEGER PRIMARY KEY)
   - story_id (TEXT, foreign key)
   - note (TEXT)
   - created_at (TIMESTAMP)

5. **status_history** - Audit trail of status changes
   - id (INTEGER PRIMARY KEY)
   - story_id (TEXT, foreign key)
   - old_status (TEXT)
   - new_status (TEXT)
   - note (TEXT)
   - changed_at (TIMESTAMP)

## Typical Workflow

1. **Project Setup**:
   ```bash
   ticket-manager.sh init
   ticket-manager.sh import requirements.json
   ticket-manager.sh status  # Verify import
   ```

2. **Start New Ticket**:
   ```bash
   ticket-manager.sh next  # Get ticket to work on
   ticket-manager.sh update <ID> IN_PROGRESS "Starting work"
   ```

3. **During Implementation**:
   ```bash
   ticket-manager.sh show <ID>  # Reference details as needed
   ```

4. **Complete Ticket**:
   ```bash
   ticket-manager.sh done <ID> "Implementation note"
   ticket-manager.sh status  # Check progress
   ```

5. **Export/Backup**:
   ```bash
   ticket-manager.sh export backup.json
   ```

## Integration with ticket-implementation Agent

The ticket-manager skill is designed to work seamlessly with the ticket-implementation agent workflow:

- **Step 1** (Validation): Use `status` to verify clean state
- **Step 2** (Select Ticket): Use `next` to get ticket ID
- **Step 2** (Mark In Progress): Use `update <ID> IN_PROGRESS`
- **Step 3-14** (Implementation): Reference `show <ID>` for context
- **Step 15** (Mark Done): Use `done <ID>` with implementation notes
- **Step 16** (Progress Check): Use `status` to see overall progress

## Error Handling

The skill exits with non-zero status on errors:
- Database not initialized
- Ticket not found
- Invalid status value
- Missing required dependencies (sqlite3, jq)

Always check for error messages before proceeding.

## Dependencies

- **Required**: sqlite3, bash 4.0+
- **Recommended**: jq (for JSON import/export)

## Best Practices

1. **Always initialize first**: Run `init` before any other commands
2. **Import once**: Import requirements at project start, manage via commands thereafter
3. **Track status changes**: Include meaningful notes when updating status
4. **Regular exports**: Periodically export to JSON for backup
5. **Check status**: Use `status` command to monitor overall progress
6. **Reference details**: Use `show` to get complete ticket context during implementation

## Version

1.0.0
