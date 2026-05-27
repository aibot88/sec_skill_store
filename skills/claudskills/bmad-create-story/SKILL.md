---
name: bmad-create-story
description: "Unified story creation and enrichment engine (story-spec v2). Produces implementation-ready stories with real-data confrontation (provider/DB/cloud), external research (docs/RFC/gotchas), structured NFRs (7 categories), binary security gate, observability requirements, deployment chain audit, impact analysis, BACs in Given/When/Then, TACs in EARS notation, INVEST self-check, out-of-scope register, risks/assumptions register, boundaries triple, and multi-validator review. Discovery mode creates a new tracker issue from conversational spec engineering; Enrichment mode loads full context (PRD, Architecture, UX, completed stories, git history) and enriches an existing Backlog issue. Use when 'create story', 'enrich story', 'spec story', 'write spec', 'nouvelle story', 'enrichir story', 'preparer story', 'creer story' is mentioned."
disable-model-invocation: true
---

# Create Story (v2)

## Overview

Unified story creation and enrichment engine producing implementation-ready stories per the **story-spec v2 schema** (`bmad-shared/spec-completeness-rule.md`). The pipeline runs three evidence-gathering steps (access verification → real-data investigation → external research) before any spec content is written, then proceeds through code investigation, modeling, NFR / Security / Observability, audit, plan composition with EARS-formatted technical ACs, and a multi-validator review gate.

Discovery mode creates a new tracker issue from conversational spec engineering; Enrichment mode loads full context (PRD, Architecture, UX, completed stories, git history) and enriches an existing Backlog issue. Both modes share the 14-step pipeline.

## Conventions

- Bare paths (e.g. `steps/step-01-init.md`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory (where `customize.toml` lives).
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

### Step 1: Resolve the Workflow Block

Run: `python3 ~/.claude/skills/bmad-shared/scripts/resolve_customization.py --skill {skill-root} --key workflow`

**If the script fails**, resolve the `workflow` block yourself by reading these three files in base → team → user order and applying the same structural merge rules as the resolver:

1. `{skill-root}/customize.toml` — defaults
2. `{project-root}/_bmad/custom/{skill-name}.toml` — team overrides
3. `{project-root}/_bmad/custom/{skill-name}.user.toml` — personal overrides

Any missing file is skipped. Scalars override, tables deep-merge, arrays of tables keyed by `code` or `id` replace matching entries and append new entries, and all other arrays append.

### Step 2: Execute Prepend Steps

Execute each entry in `{workflow.activation_steps_prepend}` in order before proceeding.

### Step 3: Load Persistent Facts

Treat every entry in `{workflow.persistent_facts}` as foundational context you carry for the rest of the workflow run. Entries prefixed `file:` are paths or globs under `{project-root}` — load the referenced contents as facts. All other entries are facts verbatim.

### Step 4: Load Project Workflow Context

Resolve the main project root (worktree-aware): run `MAIN_PROJECT_ROOT=$(dirname "$(git rev-parse --git-common-dir)")`.

Load `{MAIN_PROJECT_ROOT}/.claude/workflow-context.md` and resolve from its YAML frontmatter:
- Use `{user_name}` for greeting
- Use `{communication_language}` for all communications
- Use `{document_output_language}` for output documents
- Use `{planning_artifacts}` for output location and artifact scanning
- Use `{project_knowledge}` for additional context scanning

If `workflow-context.md` is missing, ask the user for their name and preferred language, then continue.

### Step 5: Greet the User

Greet `{user_name}`, speaking in `{communication_language}`. Be warm but efficient.

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

---

**Activation complete.** Read FULLY and follow `./workflow.md` — load the file with the Read tool, do not summarise from memory, do not skip sections.
