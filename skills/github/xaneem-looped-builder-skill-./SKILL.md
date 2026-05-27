# Looped Builder Skill

You are helping the user scaffold a large implementation task that will be executed iteratively using Claude in a bash loop. Your job is to create the planning documents that guide the implementation.

## Overview

This skill creates scaffolding for complex features, large refactors, deep explorations, or any multi-step coding task. The output is a set of files that enable iterative, autonomous implementation:

- `spec.md` - Detailed specification of what to build
- `implementation_plan.md` - Phased checklist with small, context-aware steps
- `prompt.md` - Static prompt that drives each iteration
- `run.sh` - Bash loop that runs Claude iteratively

## Step 1: Gather Context

First, understand what the user wants to build:

1. **Ask clarifying questions** if the user's description is vague:
   - What is the end goal?
   - What codebase/project is this for?
   - Are there constraints or preferences?
   - What does success look like?

2. **Explore the codebase** to understand:
   - Project structure and patterns
   - Relevant existing code
   - Dependencies and integration points
   - Testing patterns used

3. **Identify the scope**:
   - What files will likely be touched?
   - What are the key technical challenges?
   - What needs to be researched vs. what is known?

## Step 2: Create the Spec

Create `spec.md` in the feature directory. The spec should include:

```markdown
# [Feature Name] - Specification

## Overview
[1-2 paragraph summary of what we're building]

## User Stories
1. **As a [user type]**, I want [goal] so that [benefit].
[Add 3-5 user stories]

## Functional Requirements
### FR1: [Requirement Name]
- [Specific requirement detail]
- [Another detail]

[Add all functional requirements, grouped logically]

## Technical Requirements
### TR1: [Requirement Name]
- [Technical detail]

[Add technical requirements]

## Non-Functional Requirements
### NFR1: [Requirement Name]
- [Performance, security, UX requirements]

## Out of Scope
- [What this feature does NOT include]

## Success Criteria
1. [Measurable success criterion]
2. [Another criterion]
```

## Step 3: Create the Implementation Plan

Create `implementation_plan.md` with phases and small, atomic steps.

### Critical: Chunk Size Guidelines

Each step must be completable within **50-60% of Claude's context window**. This means:

- **Exploration steps**: Focus on ONE area at a time (e.g., "Find where X is defined" not "Understand the entire system")
- **Implementation steps**: Touch 1-3 files maximum per step
- **Each step should be self-contained**: Include enough context that Claude can complete it without reading the entire codebase

### Plan Structure

```markdown
# [Feature Name] - Implementation Plan

## Overview
[One sentence summary]

---

## Phase 1: Codebase Exploration

- [ ] **Explore [specific area]**
  - Find where [X] is defined/implemented
  - Identify integration points for [Y]
  - Document file paths and line numbers

  **Findings:**
  [Leave empty - Claude fills this during execution]

- [ ] **Explore [another area]**
  ...

---

## Phase 2: Implementation - [Component Name]

- [ ] **[Specific atomic task]**
  - [Detailed instruction 1]
  - [Detailed instruction 2]

  **Implementation:**
  [Leave empty - Claude fills this during execution]

- [ ] **[Next atomic task]**
  ...

---

## Phase 3: Implementation - [Next Component]
...

---

## Phase 4: Integration & Wiring
...

---

## Phase 5: Testing & Verification

- [ ] **[Build/compile step]**
  - Build command: `[exact command]`
  - Verify no compilation errors

- [ ] **[Manual testing step]**
  - [Specific test scenario]
  - Expected behavior: [what should happen]

- [ ] **[Edge case testing]**
  ...

---

## Notes

### Build Commands
```bash
[relevant build commands for the project]
```

### Key Files
[Leave empty - populated during exploration]
```

### Step Writing Guidelines

Good steps:
- "Add `PREF_FONT_SIZE` constant to Settings.java"
- "Create getter/setter methods for font size in Settings.java"
- "Add slider XML element to fragment_settings.xml"

Bad steps (too broad):
- "Implement the settings UI" (touches many files, unclear scope)
- "Set up the persistence layer" (vague, could mean many things)

## Step 4: Create Static Files

### prompt.md

Create the implementation prompt that drives each iteration:

```markdown
# [Feature Name] - Implementation Prompt

You are implementing [feature description]. Read the spec and implementation plan, then execute the next step.

## Step 1: Check Progress

Read `[path]/implementation_plan.md` and find the **first unchecked item** (marked with `- [ ]`).

If all items are complete, respond with:
```
<promise>COMPLETE</promise>
```

Otherwise, note the step description and continue.

## Step 2: Implement the Step

Based on the step found, implement ONLY that specific step.

### Important Guidelines

1. **Exploration steps**: Document findings (file paths, line numbers, patterns) directly in the plan.
2. **Implementation steps**: Write clean, working code that follows existing patterns.
3. **Testing steps**: Run the specified commands and document results.

## Step 3: Update Progress

After completing the step, edit `[path]/implementation_plan.md`:
1. Change the completed item from `- [ ]` to `- [x]`
2. Add findings/implementation notes under the step
3. If you discovered the plan needs new steps, add them as new bullet points

## Step 4: Report

Output a summary:
```
## Step Completed: {brief step description}

**What was done:**
- [Brief description]

**Files modified:**
- [List of files]

**Next step:**
- {next step description}
```

---

## Rules

1. **One step per run** - Complete exactly ONE checkbox item, then stop
2. **Read before writing** - Always read a file before modifying it
3. **Follow existing patterns** - Match the code style of surrounding code
4. **Mark completion** - Always update the checkbox when done
5. **No placeholders** - Write real, working code
6. **Document findings** - Exploration steps should capture useful info for later steps
```

### run.sh

Create the bash loop script:

```bash
#!/bin/bash

# Looped Builder - Feature Implementation Loop
# Usage: ./run.sh [max_iterations]

set -e

MAX_ITERATIONS=${1:-50}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"  # Adjust based on actual structure
FEATURE_NAME=$(basename "$SCRIPT_DIR")

BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

cd "$PROJECT_DIR"

echo ""
echo -e "${BOLD}$FEATURE_NAME${NC}"
echo -e "${DIM}Project: $PROJECT_DIR${NC}"
echo ""

for i in $(seq 1 $MAX_ITERATIONS); do
  echo -e "${BOLD}--- Iteration $i / $MAX_ITERATIONS ---${NC}"
  echo ""

  OUTPUT=$(claude --dangerously-skip-permissions --print < "$SCRIPT_DIR/prompt.md" 2>&1 | tee /dev/stderr) || {
    echo "Error in iteration $i, continuing..."
    sleep 2
    continue
  }

  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    echo ""
    echo -e "${BOLD}Done.${NC} Completed in $i iteration(s)."
    exit 0
  fi

  echo ""
  sleep 2
done

echo ""
echo "Reached max iterations ($MAX_ITERATIONS). Check implementation_plan.md for remaining steps."
exit 1
```

## Step 5: Present for Review

After creating all files, present a summary to the user:

```
## Looped Builder Scaffolding Complete

I've created the following files in `[feature_directory]/`:

### spec.md
[Brief summary of the spec]

### implementation_plan.md
[Number] phases, [number] total steps:
- Phase 1: [name] ([n] steps)
- Phase 2: [name] ([n] steps)
...

### prompt.md & run.sh
Static files ready for iterative execution.

---

**To review:** Read through spec.md and implementation_plan.md

**To execute:**
```bash
cd [feature_directory]
chmod +x run.sh
./run.sh
```

Would you like me to adjust anything before you run it?
```

## Important Notes

1. **Directory structure**: Create all files in a dedicated feature directory (e.g., `docs/feature-name/` or `.claude/builds/feature-name/`)

2. **Context window management**: The key to success is keeping each step small enough that Claude can:
   - Load the prompt
   - Read the plan
   - Read relevant source files
   - Make changes
   - All within 50-60% of context window

3. **Exploration before implementation**: Always have exploration phases that document the codebase structure. This information gets captured in the plan and helps later implementation steps.

4. **Testing is mandatory**: Every plan should end with testing/verification steps.

5. **Adjust PROJECT_DIR in run.sh**: The script assumes a specific directory structure. Adjust the `PROJECT_DIR` line based on where the feature directory is relative to the project root.
