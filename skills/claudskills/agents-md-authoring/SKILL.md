---
name: agents-md-authoring
description: Create or revise repository `AGENTS.md` files using a progressive-disclosure, dispatcher-style structure. Use when an agent needs to author or edit a top-level or directory-local `AGENTS.md`, convert a long instruction file into task-oriented "Start Here for ..." sections, add a concise "Must Follow" section with Always/Never rules, improve skill-discovery cues, or decide whether guidance belongs in root `AGENTS.md`, deeper docs, local `AGENTS.md`, or a repository-local skill.
---

# AGENTS.md Authoring

Use `AGENTS.md` as a routing layer, not as the full knowledge base.

Prefer short, stable guidance that helps an agent decide what to read next. Move long procedures, rationale, and subsystem-specific detail into `docs/`, directory-local `AGENTS.md` files, or repository-local skills.

## Workflow

### 1. Establish scope

Determine whether the file being edited is:

- a root `AGENTS.md` that should act as the repository dispatcher,
- a directory-local `AGENTS.md` that should govern one subsystem,
- or both as part of a broader restructuring.

Read the existing `AGENTS.md` plus the nearby knowledge sources it points to before rewriting structure. For a root file, also inspect the repository map and existing docs layout so the file points to real sources of truth.

### 2. Preserve progressive disclosure

Keep the always-loaded layer small.

For a root `AGENTS.md`:

- Prefer a short `Must Follow` section containing only repo-wide invariants.
- Prefer grouped `Repository Map` sections such as `Start Here for Architecture and Implementation`, `Start Here for Testing`, or `Start Here for Skills and Specialist Workflows`.
- Prefer routing language that tells the agent where to go next.

Do not turn the root file into a long playbook. If guidance needs detailed explanation, examples, rationale, or maintenance-heavy instructions, move it into `docs/` and leave a short pointer in `AGENTS.md`.

### 3. Use strict placement rules

Place guidance according to scope:

- Put it in root `AGENTS.md` if nearly every task benefits from seeing it early and it can stay short and stable.
- Put it in a directory-local `AGENTS.md` if it applies mainly inside one subsystem such as `api/`, `web/`, or `terraform/`.
- Put it in `docs/` if it needs long-form explanation, reference material, rationale, or examples.
- Put it in a repository-local skill if it describes a reusable specialist workflow with clear triggers and validation steps.

When in doubt, keep maps near the top and playbooks deeper down.

### 4. Make retrieval cues explicit

Do not assume an agent will infer when a deeper document or skill applies.

Add short trigger cues such as:

- what kind of task should send the agent to `docs/TESTING.md`,
- when a directory-local `AGENTS.md` must be loaded,
- when repository-local skills should be inspected,
- and how likely user phrases map to internal skill names.

Prefer one-line retrieval cues over embedding the whole workflow.

### 5. Write enforceable invariants

If a `Must Follow` section exists, keep it short and make every line an `ALWAYS` or `NEVER`.

Only include instructions that are:

- repo-wide,
- stable,
- high-cost to miss,
- and actionable without extra interpretation.

Do not put local conventions or fragile implementation details in `Must Follow`.

### 6. Keep the file easy to scan

Prefer compact sections, direct file references, and task-shaped grouping.

Good root-file pattern:

- `## Must Follow`
- `## Repository Map`
- `### Start Here for ...`

Avoid large prose blocks, mixed abstraction levels, and long bullet lists with weak prioritization.

## Editing Patterns

### Converting a long root file

If the existing root `AGENTS.md` mixes routing, detailed workflow instructions, and subsystem rules:

1. Extract the true repo-wide invariants into `Must Follow`.
2. Group the remaining routing pointers under `Start Here for ...` headings.
3. Remove or relocate long procedures into `docs/`, local `AGENTS.md`, or skills.
4. Leave short pointers behind so the deeper guidance remains discoverable.

### Adding skill discoverability

When a repository uses local skills, ensure the root file makes them findable without expanding into skill procedure.

Good pattern:

- point to the skill,
- mention the categories of specialist workflows covered,
- and include short alias mapping when a likely user phrase differs from the skill folder name.

### Editing directory-local `AGENTS.md`

For directory-local files, bias toward:

- working-directory expectations,
- local commands,
- subsystem file maps,
- testing commands,
- and implementation patterns specific to that directory.

Do not duplicate broad repository guidance unless it is truly required in local context.

## Quality Bar

A good `AGENTS.md` should let an agent answer these questions quickly:

- What kind of task is this?
- Which source should I read next?
- Which instructions are mandatory?
- What guidance belongs here versus somewhere deeper?

If the file feels like an encyclopedia, it is probably too large. If it fails to tell the agent where to go next, it is probably too small or too vague.
