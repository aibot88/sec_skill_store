---
name: bmad-advanced-elicitation
description: 'Push the LLM to reconsider, refine, and improve its recent output. Use when user asks for deeper critique or mentions a known deeper critique method, e.g. socratic, first principles, pre-mortem, red team.'
disable-model-invocation: true
---

# Advanced Elicitation

**Goal:** Push the LLM to reconsider, refine, and improve its recent output.

## Conventions

- Bare paths (e.g. `methods.csv`) resolve from the skill root.
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
- Use `{communication_language}` for all communications
- Use `{document_output_language}` for output documents

If `workflow-context.md` is missing, default to English and continue.

### Step 5: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

---

**Activation complete.** Proceed to the FLOW section below.

---

## CRITICAL LLM INSTRUCTIONS

- **MANDATORY:** Execute ALL steps in the flow section IN EXACT ORDER
- DO NOT skip steps or change the sequence
- HALT immediately when halt-conditions are met
- Each action within a step is a REQUIRED action to complete that step
- Sections outside flow (validation, output, critical-context) provide essential context - review and apply throughout execution
- **YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the `communication_language`**

---

## INTEGRATION (When Invoked Indirectly)

When invoked from another prompt or process:

1. Receive or review the current section content that was just generated
2. Apply elicitation methods iteratively to enhance that specific content
3. Return the enhanced version back when user selects 'x' to proceed and return back
4. The enhanced content replaces the original section content in the output document

---

## FLOW

### Step 1: Method Registry Loading

**Action:** Load `./methods.csv` for elicitation methods. If party-mode may participate, resolve the agent roster via:

```bash
python3 {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key agents
```

The resolver merges four layers in order: `_bmad/config.toml` (installer base, team-scoped), `_bmad/config.user.toml` (installer base, user-scoped), `_bmad/custom/config.toml` (team overrides), and `_bmad/custom/config.user.toml` (personal overrides). Each entry under `agents` is keyed by the agent's `code` and carries `name`, `title`, `icon`, `description`, `module`, and `team`.

#### CSV Structure

- **category:** Method grouping (core, structural, risk, etc.)
- **method_name:** Display name for the method
- **description:** Rich explanation of what the method does, when to use it, and why it's valuable
- **output_pattern:** Flexible flow guide using arrows (e.g., "analysis -> insights -> action")

#### Context Analysis

- Use conversation history
- Analyze: content type, complexity, stakeholder needs, risk level, and creative potential

#### Smart Selection

1. Analyze context: Content type, complexity, stakeholder needs, risk level, creative potential
2. Parse descriptions: Understand each method's purpose from the rich descriptions in CSV
3. Select 5 methods: Choose methods that best match the context based on their descriptions
4. Balance approach: Include mix of foundational and specialized techniques as appropriate

---

### Step 2: Present Options and Handle Responses

#### Display Format

```
**Advanced Elicitation Options**
_If party mode is active, agents will join in._
Choose a number (1-5), [r] to Reshuffle, [a] List All, or [x] to Proceed:

1. [Method Name]
2. [Method Name]
3. [Method Name]
4. [Method Name]
5. [Method Name]
r. Reshuffle the list with 5 new options
a. List all methods with descriptions
x. Proceed / No Further Actions
```

#### Response Handling

**Case 1-5 (User selects a numbered method):**

- Execute the selected method using its description from the CSV
- Adapt the method's complexity and output format based on the current context
- Apply the method creatively to the current section content being enhanced
- Display the enhanced version showing what the method revealed or improved
- **CRITICAL:** Ask the user if they would like to apply the changes to the doc (y/n/other) and HALT to await response.
- **CRITICAL:** ONLY if Yes, apply the changes. IF No, discard your memory of the proposed changes. If any other reply, try best to follow the instructions given by the user.
- **CRITICAL:** Re-present the same 1-5,r,x prompt to allow additional elicitations

**Case r (Reshuffle):**

- Select 5 random methods from methods.csv, present new list with same prompt format
- When selecting, try to think and pick a diverse set of methods covering different categories and approaches, with 1 and 2 being potentially the most useful for the document or section being discovered

**Case x (Proceed):**

- Complete elicitation and proceed
- Return the fully enhanced content back to the invoking skill
- The enhanced content becomes the final version for that section
- Signal completion back to the invoking skill to continue with next section

**Case a (List All):**

- List all methods with their descriptions from the CSV in a compact table
- Allow user to select any method by name or number from the full list
- After selection, execute the method as described in the Case 1-5 above

**Case: Direct Feedback:**

- Apply changes to current section content and re-present choices

**Case: Multiple Numbers:**

- Execute methods in sequence on the content, then re-offer choices

---

### Step 3: Execution Guidelines

- **Method execution:** Use the description from CSV to understand and apply each method
- **Output pattern:** Use the pattern as a flexible guide (e.g., "paths -> evaluation -> selection")
- **Dynamic adaptation:** Adjust complexity based on content needs (simple to sophisticated)
- **Creative application:** Interpret methods flexibly based on context while maintaining pattern consistency
- Focus on actionable insights
- **Stay relevant:** Tie elicitation to specific content being analyzed (the current section from the document being created unless user indicates otherwise)
- **Identify personas:** For single or multi-persona methods, clearly identify viewpoints, and use party members if available in memory already
- **Critical loop behavior:** Always re-offer the 1-5,r,a,x choices after each method execution
- Continue until user selects 'x' to proceed with enhanced content, confirm or ask the user what should be accepted from the session
- Each method application builds upon previous enhancements
- **Content preservation:** Track all enhancements made during elicitation
- **Iterative enhancement:** Each selected method (1-5) should:
  1. Apply to the current enhanced version of the content
  2. Show the improvements made
  3. Return to the prompt for additional elicitations or completion
