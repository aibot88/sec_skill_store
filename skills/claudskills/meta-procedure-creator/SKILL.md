---
name: meta-procedure-creator
description: Author a new procedure file in procedures/. Use when asked to create or rewrite a procedure, or when designing an agent's behavior.
paths:
  - 'procedures/**'
---

Write all procedure files in **English**, regardless of the project's primary language.

A procedure defines **What** an agent does — never How. How details belong in skills, which are injected at runtime.

## Decision flowchart

Follow this flowchart for every procedure authoring task:

```mermaid
flowchart TD
    Start([Start]) --> Understand[Understand the agent's goal from the request]
    Understand --> Exists{Procedure already\nexists for this goal?}

    Exists -- Yes --> Scope{Scope of change?}
    Scope -- Minor --> Patch[Patch the existing procedure file]
    Scope -- Major --> Rewrite[Rewrite as new procedure]
    Patch --> Done([Done])
    Rewrite --> NameFile

    Exists -- No --> NameFile[Choose a procedure name]

    NameFile --> DesignFlow[Draft a What-only flowchart]

    DesignFlow --> HasHow{Flowchart node\ncontains How?}
    HasHow -- Yes --> Strip[Remove How detail;\nreplace with What outcome node]
    Strip --> HasHow
    HasHow -- No --> NeedsSkill{How detail needed\nfor this procedure?}

    NeedsSkill -- Yes --> NoteSkill[Record which skill provides the How;\nadd Consult line at bottom of file]
    NeedsSkill -- No --> WriteFile
    NoteSkill --> WriteFile[Write procedures/<skill>/<name>.md]

    WriteFile --> Verify[Verify all nodes describe What,\nnot How]
    Verify --> Valid{All nodes\nWhat-only?}
    Valid -- No --> DesignFlow
    Valid -- Yes --> Done([Done])
```

## What-only rule

A node is **What** if it names an outcome or decision. It is **How** if it describes an implementation step.

| What (keep) | How (remove) |
|:---|:---|
| `Classify the entry` | `Check if title contains "Error"` |
| `Write the output file` | `Use Write tool with frontmatter template` |
| `Verify completeness` | `Check that Keywords line is present` |

Strip How nodes and add a `Consult the \`<skill>\` skill` line at the bottom instead.

## File format

```markdown
# <Agent Role Title>

One sentence describing what the agent is and its sole job.

\`\`\`mermaid
flowchart TD
    ...
\`\`\`

Consult the `<skill-name>` skill for <what the skill provides>.
```

Rules:
- Title is the agent's role, not the file name
- Opening sentence must name the sole job
- Flowchart is the only structural element — no extra sections
- `Consult` lines appear only when a skill is needed for How details
- Target **20–40 lines** per procedure file

## Naming

- Lowercase, hyphens only: `code-reviewer`, `meta-procedure-creator`
- Name reflects the agent's role, not the task it was invoked for
- File lives at `procedures/<skill>/<name>.md`

**Name by purpose, not by the skill reused.**

A procedure orchestrates one or more skills — its name must describe what it accomplishes, not which skill it calls.

| Good | Bad | Why bad |
|:---|:---|:---|
| `create` | `create-planning-pipeline` | verb alone suffices; skill dir provides context |
| `curate` | `curate-knowledge` | subject (`knowledge`) is redundant with skill dir |
| `review` | `arch-reviewer` | adjective before noun — role, not task |

Use a single **verb**: `create`, `review`, `implement`, `curate`, `inspect`.

## Placement

File lives at `procedures/<skill>/<verb>.md` where `<skill>` is the **subject** — the skill that acts as the agent's primary role — not the domain being operated on.

| Procedure | Skill dir | Reason |
|:---|:---|:---|
| `improve` | `meta-skill-creator/` | subject is skill improvement; arch is the target |
| `curate` | `meta-librarian/` | subject is the librarian; knowledge is the target |
| `review` | `arch/` | subject is arch review; arch is both actor and domain |

When in doubt: ask "which skill describes what this agent *is*?" — not "what does it operate on?"
