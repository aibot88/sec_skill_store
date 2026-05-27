---
name: spec-driven-stories
description: >
  Create user stories with acceptance criteria, technical specifications, and UI
  specifications through an 8-phase workflow with structural anti-skip enforcement.
  Prevents token optimization bias through per-phase reference loading, checkpoint
  persistence, Execute-Verify-Record enforcement, and artifact verification. Use when
  transforming feature descriptions into structured stories, generating stories from
  epic features, or creating follow-up stories for deferred work. Supports CRUD,
  authentication, workflow, and reporting story types with complete technical and UI
  specifications.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - AskUserQuestion
  - Skill
model: claude-opus-4-7
effort: High
---

# Spec-Driven Stories

Create comprehensive, implementation-ready user stories through an 8-phase workflow with structural anti-skip enforcement.

**Context files are THE LAW:** tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**If ambiguous or conflicts detected: HALT and use AskUserQuestion**

---

## Execution Model

This skill expands inline. After invocation, execute Phase 00 Initialization immediately. Do not wait passively, ask permission, or offer execution options.

**Self-Check (if ANY box is true = VIOLATION):**

- [ ] Stopping to ask about token budget
- [ ] Stopping to offer execution options
- [ ] Waiting passively for user to say "go"
- [ ] Asking "should I execute this?"
- [ ] Skipping a phase because it "seems simple"
- [ ] Combining multiple phases into one
- [ ] Summarizing instead of loading a reference file
- [ ] Skipping verification because "I already wrote the file"

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase 00 Initialization now.

---

## Anti-Skip Enforcement Contract

This skill enforces 4 independent anti-skip layers. ALL FOUR must fail for a step to be skipped:

1. **Per-phase reference loading** - Each phase loads its reference files fresh via `Read()`. NOT consolidated. Prevents "already covered" rationalization.
2. **Binary CLI gates** - `devforgeai-validate phase-check/phase-complete` at phase boundaries. Cannot be forged by LLM.
3. **Checkpoint-based state tracking** - Phase completion verified by checking checkpoint JSON data keys and `current_phase` field.
4. **Artifact verification** - Checkpoint JSON existence checked via `Glob()`, story files verified on disk, epic/sprint entries verified via `Grep()`.

**Execute-Verify-Record Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact action to perform (Read, Write, AskUserQuestion, Task, Grep, Glob)
- **VERIFY:** How to confirm the action happened (file exists, content contains expected text, data key populated)
- **RECORD:** Update checkpoint JSON with captured data; call `devforgeai-validate phase-record`

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary.

---

## Story Template Versions

**Current Version:** 3.0 (as of 2026-03-23)

| Version | Date | Change | Reference |
|---------|------|--------|-----------|
| v3.0 | 2026-03-23 | Implementation Guide with 6 subsections; Patterns and References | STORY-578, STORY-583, ADR-047 |
| v2.8 | 2026-02-04 | Advisory story fields (`advisory`, `source_gap`, `source_story`) | STORY-348, EPIC-054 |
| v2.1 | 2025-01-21 | AC header format: `### 1. [ ]` to `### AC#1:` | RCA-012 |
| v2.0 | 2025-10-30 | Structured YAML `technical_specification` block | RCA-006 |
| v1.0 | Initial | Original template (legacy, still supported) | -- |

**Format Specification:** `devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md` (loaded in Phase 03)

**Migration Script (v2.0 to v2.1):** `scripts/migrate-ac-headers.sh`

**Backward Compatibility:** All versions (v1.0, v2.0, v2.1, v2.8, v3.0) supported. Migration is optional.

**Template Location:** `assets/templates/story-template.md` (loaded in Phase 05)

---

## When to Use This Skill

### Trigger Scenarios

- User runs `/create-story [feature-description]` command
- `/create-stories-from-rca` decomposes RCA recommendations into stories
- spec-driven-lifecycle decomposes epic features into stories
- spec-driven-dev creates tracking stories for deferred DoD items
- Sprint planning requires story generation
- Manual invocation: `Skill(command="spec-driven-stories")`

### When NOT to Use

- Epic creation (use spec-driven-lifecycle epic mode instead)
- Sprint planning (use spec-driven-lifecycle sprint mode instead)
- Story already exists (use Edit tool to modify existing story)

---

## Batch Mode Support

**Batch mode triggered when:**
- Context marker `**Batch Mode:** true` present in conversation

**Batch mode behavior:**
- **Phase 01 modified:** Skip interactive questions, extract metadata from context markers
- **Phases 02-07:** Execute normally (requirements, tech spec, UI spec, file creation, linking, validation)
- **Phase 08 modified:** Skip next action AskUserQuestion, return immediately to batch loop

**Required context markers for batch mode:**
```
**Story ID:** STORY-009
**Epic ID:** EPIC-001
**Feature Number:** 1.1
**Feature Name:** User Registration Form
**Feature Description:** Implement user registration form with email validation...
**Priority:** High
**Points:** 5
**Type:** feature
**Sprint:** Sprint-1
**Batch Mode:** true
**Batch Index:** 0
```

**When batch mode detected:**
1. Extract all metadata from conversation context
2. Validate all required markers present (Story ID, Epic ID, Feature Description, Priority, Points, Type, Sprint)
3. Skip Phase 01 interactive questions (epic/sprint/priority/points/type selection)
4. Use provided values instead of asking user
5. Execute Phases 02-07 normally (full story generation)
6. Skip Phase 08 next action question (batch loop handles this)
7. Return control to command for next feature in batch

**Fallback:** If required markers missing, switch to interactive mode and ask questions

**See `references/story-discovery.md` for batch mode detection and metadata extraction logic.** (loaded in Phase 01)

### Batch Reference Caching (RCA-049)

In batch mode, stable reference files are pre-loaded ONCE before the loop (Step 0.4.5) to reduce token pressure. This is the ONLY authorized token optimization for batch mode. Per-story subagent invocations and dynamic files (epic/sprint modified by linking) are still loaded fresh each iteration.

**Caching does NOT authorize skipping any Execute-Verify-Record triplet.** All phase steps must still execute for every story.

See `references/story-discovery.md` Step 0.4.5 for the complete caching protocol.

### Post-Batch Structural Validation (RCA-049)

After the batch loop completes (see `references/story-discovery-batch.md` Step 0.6: Batch Summary), `references/story-discovery-batch.md` Step 0.7 validates every created story against the SECTION_MANIFEST. This is a HALT gate — if any story is missing required sections, component IDs, or format_version, the batch fails with a specific error listing the story ID and missing elements.

**Validation checks:**
1. All Required H2 sections from SECTION_MANIFEST present
2. All Required H3 subsections present
3. Implementation Guide present for >= 5pt stories (WARNING only)
4. Tech spec contains format_version and COMP-NNN IDs
5. Provenance depth >= 2 origins for epic-linked stories (WARNING only)

See `references/story-discovery.md` Step 0.7 for the complete validation protocol.

---

## Parameter Extraction

Extract from conversation context markers set by invoking command:

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$MODE` | `/create-story` | SINGLE_STORY or EPIC_BATCH |
| `$EPIC_ID` | `/create-story` | EPIC-NNN identifier |
| `$FEATURE_DESCRIPTION` | `/create-story` | Feature description text |
| `$STORY_ID` | batch mode | STORY-NNN identifier |
| `$FEATURE_NUMBER` | batch mode | Feature number (e.g., 1.1) |
| `$FEATURE_NAME` | batch mode | Feature name |
| `$PRIORITY` | batch mode | High/Medium/Low |
| `$POINTS` | batch mode | Story points |
| `$TYPE` | batch mode | feature/bug/refactor/documentation |
| `$SPRINT` | batch mode | Sprint-N identifier |
| `$BATCH_MODE` | batch mode | true/false |
| `$BATCH_INDEX` | batch mode | 0-based index |

---

## Command Integration

These commands delegate to this skill. When invoked via a command, context markers are already set.

| Command | Purpose | Markers Set |
|---------|---------|-------------|
| `/create-story` | Create single story or batch from epic | Mode, Epic ID or Feature Description |
| `/create-stories-from-rca` | Create stories from RCA recommendations | Mode, Story metadata from RCA |

---

## State Persistence

- **Checkpoint:** `devforgeai/workflows/checkpoints/${SESSION_ID}.checkpoint.json`
- **References:** `references/` (self-contained within this skill)
- **Contracts:** `contracts/` (self-contained within this skill)
- **Templates:** `assets/templates/` (self-contained within this skill)
- **Scripts:** `scripts/` (self-contained within this skill)

---

## Phase 00: Initialization [INLINE - Bootstraps State]

This phase runs inline because it creates the state that all other phases depend on. It CANNOT be skipped.

### Step 0.1: Parse Arguments

```
IF context markers already set by /create-story command (Mode, Epic ID, Next Session ID present in conversation):
  Confirm (one line): "Context from /create-story: MODE=${MODE}, EPIC_ID=${EPIC_ID}, SESSION_ID=${NEXT_SESSION_ID}"
  Skip Steps 0.2-0.3 (preflight CLI already handled resume detection + session ID generation)
  Go directly to Step 0.4 (CLI Initialization) using the preflight-provided SESSION_ID
ELSE:
  Extract all context markers from the Parameter Extraction table above.
  Defaults: $MODE = "SINGLE_STORY", $TYPE = "feature", $BATCH_MODE = false.
  All other markers default to null if not present.
```

### Step 0.2: Resume Detection

```
# FROM_RECOMMENDATIONS EARLY-EXIT (do NOT call story-preflight with STORY-NNN)
# ---------------------------------------------------------------------------
# When /create-story --from-recommendations=STORY-NNN is used, the command
# HALTs before story-preflight (STORY-NNN is not a valid story-preflight arg).
# Resume detection for this mode uses a filesystem scan instead of the CLI.
IF $MODE == "FROM_RECOMMENDATIONS":
  # Scan for today's existing sessions. Prior-day sessions are NOT candidates
  # for resume (FROM_RECOMMENDATIONS is a single-shot remediation flow).
  today = current date (YYYY-MM-DD)
  existing_checkpoints = Glob(pattern="devforgeai/workflows/checkpoints/SC-${today}-*.checkpoint.json")

  resumable = []
  FOR each cp in existing_checkpoints:
      Read(cp)
      # A resumable session has: mode == FROM_RECOMMENDATIONS, source_story_id == $SOURCE_STORY_ID,
      # and current_phase != "08" (completion). Match on source story to avoid cross-story collisions.
      IF cp.mode == "FROM_RECOMMENDATIONS" AND cp.source_story_id == $SOURCE_STORY_ID AND cp.current_phase != "08":
          resumable.append(cp.session_id)

  IF resumable is non-empty:
      AskUserQuestion:
          Question: "Found existing FROM_RECOMMENDATIONS session(s) for ${SOURCE_STORY_ID}: ${resumable}. Resume or start fresh?"
          Options: [{label: "Resume", description: "Continue last checkpoint"},
                    {label: "Start fresh", description: "New session for ${SOURCE_STORY_ID}"}]
      IF "Resume": Restore state, GOTO Phase Orchestration Loop at CURRENT_PHASE

  # Either no resumable session OR user chose fresh — continue to Step 0.3
  # (SKIP the story-preflight fallback below)
  GOTO Step 0.3

# Other modes — existing flow
# ---------------------------------------------------------------------------
# The /create-story command already ran story-preflight CLI (no Glob needed).
# If exit code 3, a resume_session was returned. Check context markers:

IF conversation contains resume_session from story-preflight:
  Read the checkpoint file at resume_session.checkpoint_file
  AskUserQuestion:
    Question: "Found existing story creation session {resume_session.session_id}. Resume or start fresh?"
    Header: "Resume"
    Options:
      - label: "Resume session"
        description: "Continue from last checkpoint"
      - label: "Start fresh"
        description: "Begin new story creation session"
  IF "Resume": Restore state, GOTO Phase Orchestration Loop at CURRENT_PHASE
ELSE:
  Continue to Step 0.3

# FALLBACK (if story-preflight was not used, e.g., direct skill invocation):
# Use Bash CLI to find checkpoints (NOT Glob):
result = Bash(command="devforgeai-validate story-preflight ${EPIC_ID} --project-root=. --format=json 2>&1")
# Parse resume_session from JSON result
```

### Step 0.3: Generate Session ID

```
# FROM_RECOMMENDATIONS EARLY-EXIT (do NOT call story-preflight with STORY-NNN)
# ---------------------------------------------------------------------------
# story-preflight accepts only EPIC-NNN or 10+ word feature description.
# Passing $SOURCE_STORY_ID (STORY-NNN) produces exit 2. Generate SESSION_ID
# deterministically from today's checkpoints instead.
IF $MODE == "FROM_RECOMMENDATIONS":
  today = current date (YYYY-MM-DD)
  existing_checkpoints = Glob(pattern="devforgeai/workflows/checkpoints/SC-${today}-*.checkpoint.json")

  IF existing_checkpoints is empty:
      SESSION_ID = "SC-${today}-001"
  ELSE:
      # Parse the 3-digit sequence from each filename; take max + 1
      max_seq = max(parse_int(regex_extract(basename(f), r"SC-\d{4}-\d{2}-\d{2}-(\d{3})"))
                    for f in existing_checkpoints)
      SESSION_ID = f"SC-${today}-{format(max_seq + 1, 03d)}"

  Display: "FROM_RECOMMENDATIONS session ID (filesystem-scan): ${SESSION_ID}"
  # SKIP the story-preflight fallback below
  GOTO Step 0.4

# Other modes — existing flow
# ---------------------------------------------------------------------------
# Use next_session_id from story-preflight CLI (set by /create-story command)
IF conversation contains "**Next Session ID:**":
  SESSION_ID = extract from "**Next Session ID:**" context marker
  Display: "Using session ID from preflight: ${SESSION_ID}"
ELSE:
  # FALLBACK: direct skill invocation without /create-story command
  # Use CLI to get next session ID (scans both checkpoints + state files)
  result = Bash(command="devforgeai-validate story-preflight ${EPIC_ID} --project-root=. --format=json 2>&1")
  SESSION_ID = parse result.next_session_id from JSON
  IF SESSION_ID empty:
    SESSION_ID = "SC-{YYYY-MM-DD}-001"
```

### Step 0.4: CLI Initialization

```bash
devforgeai-validate phase-init ${SESSION_ID} --workflow=stories --project-root=. 2>&1
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file AND checkpoint file created atomically. Set CURRENT_PHASE = "01". Proceed to Step 0.5. |
| 1 | Existing workflow | Resume. Run `devforgeai-validate phase-status ${SESSION_ID} --workflow=stories` to get CURRENT_PHASE. |
| 2 | Invalid session ID | HALT. Must match SC-YYYY-MM-DD-NNN pattern. |
| 127 | CLI not installed | Continue without CLI enforcement (backward compatibility). Manually Write() the checkpoint file if needed. |

**Trust the CLI.** Exit 0 is the contract: both the state file AND the checkpoint file have been created. Do NOT Glob/Search to verify — the CLI's "Checkpoint: <path>" text output already names the path it created. Any defensive verification step here reintroduces the exact anti-pattern this CLI replaces.

### Step 0.5: Display Session Banner

```
Display:
"------------------------------------------------------------
  DevForgeAI Story Creation Session
------------------------------------------------------------

Session: ${SESSION_ID}
Mode: ${MODE}
Epic: ${EPIC_ID || 'None'}
Feature: ${FEATURE_DESCRIPTION || 'None provided'}
Batch: ${BATCH_MODE || false}

Phases: 8 (Discovery > Requirements > Tech Spec > UI Spec > File Creation > Linking > Validation > Completion)
------------------------------------------------------------"
```

Set CURRENT_PHASE = 1.

---

## Phase Orchestration Loop

```
FOR phase_num in range(CURRENT_PHASE, 9):  # Phases 01-08

    1. ENTRY GATE:
       IF phase_id == "01":
         SKIP phase-check (phase-init IS the entry gate for Phase 01 — there is no Phase 00)
       ELSE:
         devforgeai-validate phase-check ${SESSION_ID} --workflow=stories --from={prev} --to={phase_id} --project-root=.
         IF exit != 0 AND exit != 127: HALT

    2. LOAD: Read(file_path=".claude/skills/spec-driven-stories/phases/{phase_files[phase_num]}")
       Load the phase file FRESH. Do NOT skip this step. Do NOT rely on memory of previous reads.

    3. REFERENCE: Read the phase's reference files as specified in the phase Contract section.
       References are in references/ (self-contained within this skill).
       Load ALL listed references. Do not skip any.

    4. EXECUTE: Follow EVERY step in the phase file using EXECUTE-VERIFY-RECORD triplets.

    5. EXIT GATE: devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase={phase_id} --checkpoint-passed --project-root=.
       IF exit != 0 AND exit != 127: HALT

    6. CHECKPOINT: Update checkpoint JSON with phase completion.
       Write updated checkpoint to disk. Write() returns cleanly on success — do NOT Glob to verify. The return value is the contract.
```

---

## Phase-Output Cache (Sprint 3)

Phases write per-phase JSON cache files to `tmp/${SESSION_ID}/phase-outputs/phase-NN.json`
to share processed data without redundant disk reads or re-parsing.

- **Schema contract:** `contracts/phase-output-schema.json` (oneOf of 7 phase definitions,
  each carrying `schema_version` + `phase_id` discriminator constants).
- **Cache-miss behavior:** Readers ALWAYS fall through to fresh compute on missing file,
  schema_version mismatch, phase_id mismatch, or null payload. **Cache miss is NEVER a HALT.**
- **Sprint 3.2:** Phase 03.6 persists `parsed_manifest`; Phase 05.2 reads it before re-parsing
  the SECTION_MANIFEST.
- **Sprint 3.3:** Phase 01.3 captures epic content into in-context `$EPIC_CONTENT` plus
  `phase-01.json.epic_content` for resume resilience. Phases 05/06 prefer the in-context
  variable. **POST-EPIC-EDIT RE-READ CAVEAT:** Phase 06.1 mutates the epic file via Edit();
  Phase 07.2.5 (AC fidelity) MUST re-read from disk and ignore the cache.
- **Sprint 3.4:** Phase 07 caches `$STORY_CONTENT` at Step 7.1; Step 7.5 reuses it unless
  the Step 7.1 auto-correct Edit invalidated `$STORY_CONTENT_FRESH`.

The cache is a **performance optimization**, not a correctness requirement. Sessions
without write access to `tmp/` (or sessions resumed across reboots without a preserved
tmp tree) degrade gracefully to fresh re-compute on every read.

---

## Phase Table

| Phase | Name | File | Steps | Required Subagents |
|-------|------|------|-------|--------------------|
| 00 | Initialization | (inline above) | 6 | none |
| 01 | Story Discovery & Context | `phases/phase-01-story-discovery.md` | 6 | none |
| 02 | Requirements Analysis | `phases/phase-02-requirements-analysis.md` | 4 | story-requirements-analyst (BLOCKING) |
| 03 | Technical Specification | `phases/phase-03-technical-specification.md` | 5 | api-designer (CONDITIONAL) |
| 04 | UI Specification | `phases/phase-04-ui-specification.md` | 3 | none |
| 05 | Story File Creation | `phases/phase-05-story-file-creation.md` | 5 | none |
| 06 | Epic/Sprint Linking | `phases/phase-06-epic-sprint-linking.md` | 3 | none |
| 07 | Self-Validation | `phases/phase-07-self-validation.md` | 4 | none |
| 08 | Completion Report | `phases/phase-08-completion-report.md` | 3 | none |

---

## Required Subagents Per Phase

| Phase | Subagent | Enforcement |
|-------|----------|-------------|
| 02 | story-requirements-analyst | BLOCKING - Must invoke and use output |
| 03 | api-designer | CONDITIONAL - Only if API endpoints detected |

**All other phases:** No subagents required. Direct tool calls (Read, Write, Glob, Grep, AskUserQuestion).

---

## Subagent Coordination

This skill delegates specialized tasks to subagents:

- **story-requirements-analyst** (Phase 02) - Generates user story and acceptance criteria from feature description. BLOCKING: Phase 02 cannot complete without subagent output. The subagent produces the user story (As a/I want/So that), 3+ acceptance criteria (Given/When/Then), edge cases, and non-functional requirements.
- **api-designer** (Phase 03, conditional) - Designs API contracts when endpoints are detected in the requirements. CONDITIONAL: Only invoked when Phase 02 output contains API-related acceptance criteria or when the feature description implies REST/GraphQL endpoints.

**Subagent contracts (loaded per-phase, not upfront):**
- `contracts/requirements-analyst-contract.yaml` (loaded in Phase 02)
- `contracts/api-designer-contract.yaml` (loaded in Phase 03, conditional)

**Template Authority:** The `contracts/template-consumer-contract.yaml` defines a schema-authority relationship between the story template and consuming phase files. It enforces that phase files MUST derive structural constants (template version, section lists, subsection names) from the template's SECTION_MANIFEST rather than hardcoding shadow copies. This prevents the class of template-workflow drift bugs documented in RCA-048, where 7 hardcoded values across 3 phase files drifted independently from the authoritative template.

---

## Integration Points

**Invoked by:**
- `/create-story` command (user-initiated)
- `/create-stories-from-rca` command (RCA recommendation decomposition)
- spec-driven-lifecycle skill (epic/sprint decomposition)
- spec-driven-dev skill (deferred work tracking)

**Provides output to:**
- spec-driven-ui (AC to UI requirements)
- spec-driven-dev (AC to test generation)
- spec-driven-qa (AC to validation targets)

**See `references/integration-guide.md` for complete integration patterns.** (loaded on-demand, not upfront)

---

## Workflow Completion Validation

```
completed_count = len(checkpoint.progress.phases_completed)
IF completed_count < 8:
    HALT "WORKFLOW INCOMPLETE - {completed_count}/8 phases completed"
IF completed_count == 8:
    Display "All 8 phases completed - Workflow validation passed"
    Update checkpoint status to "completed"
```

---

## Success Criteria

Complete story generated with:
- [ ] Valid story ID (STORY-NNN format)
- [ ] User story (As a/I want/So that)
- [ ] 3+ acceptance criteria (Given/When/Then)
- [ ] Technical specification (complete)
- [ ] UI specification (if applicable)
- [ ] Non-functional requirements (measurable)
- [ ] Edge cases documented
- [ ] Definition of Done (checkboxes)
- [ ] File written to devforgeai/specs/Stories/
- [ ] Epic/sprint updated (if applicable)
- [ ] Self-validation passed
- [ ] Token usage <90K (isolated context)

---

## Reference Files Inventory

Load these on-demand during workflow execution:

### Phase Files (8 files in `phases/`)

| Phase File | Primary Reference (in `references/`) | Additional References |
|------------|--------------------------------------|----------------------|
| `phase-01-story-discovery.md` | `story-discovery.md` | `user-input-integration-guide.md`, `story-type-classification.md` |
| `phase-02-requirements-analysis.md` | `requirements-analysis.md` | `acceptance-criteria-core.md`, `acceptance-criteria-domains.md`, `acceptance-criteria-refactor.md` (conditional) |
| `phase-03-technical-specification.md` | `technical-specification-creation.md` | `technical-specification-guide.md` |
| `phase-04-ui-specification.md` | `ui-specification-creation.md` | `ui-specification-guide.md` |
| `phase-05-story-file-creation.md` | `story-file-creation.md` | `story-structure-guide.md`, `story-examples.md` |
| `phase-06-epic-sprint-linking.md` | `epic-sprint-linking.md` | -- |
| `phase-07-self-validation.md` | `story-validation-workflow.md` | `validation-checklists.md`, `context-validation.md` |
| `phase-08-completion-report.md` | `completion-report.md` | -- |

### Supporting Guides (8 files in `references/`)
- **acceptance-criteria-core.md** - Core principles + universal patterns (always loaded)
- **acceptance-criteria-domains.md** - 13 domain libraries: CRUD, Auth, Workflow, Data Validation, Search, Pagination, Upload, Async, Reporting, Integration, Performance, Security, Accessibility
- **acceptance-criteria-refactor.md** - Refactor story templates (conditional, only for `type: refactor`)
- **story-examples.md** - 4 complete story examples (CRUD, auth, workflow, reporting)
- **story-structure-guide.md** - YAML frontmatter, section formatting rules
- **technical-specification-guide.md** - API contract patterns, data modeling
- **ui-specification-guide.md** - Component design, ASCII mockups, accessibility
- **validation-checklists.md** - Quality validation procedures
- **user-input-integration-guide.md** - User input guidance integration
- **story-type-classification.md** - Story type enum, phase skip matrix

### Workflow & Error References (4 files in `references/`)
- **error-handling.md** - Error recovery procedures across all phases
- **integration-guide.md** - Skill integration patterns and downstream consumers
- **batch-mode-configuration.md** - Batch processing detection and metadata
- **custody-chain-workflow.md** - Provenance chain tracking

### Additional References (4 files in `references/`)
- **context-validation.md** - Context file constraint validation
- **gap-to-story-conversion.md** - Gap ID to story conversion logic
- **parameter-extraction.md** - Context marker parsing and validation
- **checkpoint-schema.md** - Checkpoint JSON schema and update protocol

### Contracts (3 YAML files)
- **contracts/requirements-analyst-contract.yaml** - story-requirements-analyst interface
- **contracts/api-designer-contract.yaml** - api-designer interface
- **contracts/template-consumer-contract.yaml** - template-to-phase-file schema authority contract

### Assets (1 template)
- **assets/templates/story-template.md** - Base story template (YAML + markdown)

**Total:** 8 phase files + 24 reference files + 3 contracts + 1 template = 36 files

---

## Best Practices

**Top 5 practices for story creation:**

1. **Provide clear feature description** - Minimum 10 words, specific WHO/WHAT
2. **Associate with epic when possible** - Enables traceability and feature tracking
3. **Ensure AC are testable** - All criteria must be verifiable (Given/When/Then)
4. **Include UI specs for frontend work** - Mockups prevent implementation ambiguity
5. **Trust self-validation** - Phase 07 auto-corrects common issues, high quality output

**See phase-specific reference files for detailed best practices.**
