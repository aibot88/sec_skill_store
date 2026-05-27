---
name: aor-test-trace
description: Author Test Cases (TCs) and the traceability matrix linking UN→PR→SR→TC. Verify every SR clause has at least one TC.
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion
argument-hint: "[path to specification file]"
---

# /aor-test-trace — Test Cases + Traceability Matrix

Drafts test cases for each Software Requirement using the appropriate format,
then builds the trace matrix linking UN → PR → SR → TC.

> **Note on skills vs agents.** The AOR bundle contains *skills* at
> `.claude/skills/aor-*/SKILL.md` (invocable directly, like this one)
> and *SME agents* at `.claude/agents/aor-sme-*.md` (sub-agent system
> prompts spawned only by `aor-review` / `aor-review-adhoc`). Do NOT
> invoke an agent as a skill — it will fail with "skill not found".

## Operating discipline

Apply throughout. State each at startup so the user sees it.

- **Mode (declared at startup):** ask whether this is an *exploratory*
  session (single SR, conversational, no files written) or a *document*
  session (full TC + traceability authoring against a `SPECIFICATION.md`).
  Default to document mode if a specification path is provided; default
  to exploratory if SR text appears inline in the conversation without
  a file path.
- **Invocation acknowledgement:** the first response of the skill states
  "Running as `aor-test-trace` in <mode> mode. Files written to
  `TEST_CASES.md` / `TRACEABILITY.md` unless you ask otherwise."
  Eliminates the "did the skill actually run?" ambiguity.
- **Q&A discipline:** ask one clarifying question at a time. Wait for
  the user's answer before asking the next. Do not stack questions.
  A single `AskUserQuestion` call presenting one decision with multiple
  alternatives (e.g., a multi-choice menu) is *one* question; presenting
  two unrelated decisions in one call is stacking.
- **Failure-disclosure:** if any prescribed step cannot be completed
  (file write blocked, sub-agent invocation failed, reference file
  unavailable, partial completion, timeout, permission denied), state
  it in chat. After disclosing, halt and ask whether to retry, fall
  back to disclosed manual emulation, or abort — do not continue
  silently. One retry is permitted for clearly transient failures
  (e.g., network timeout) before mandatory disclosure.

## Workflow

### Step 1: Locate or accept the specification

Three input modes, in priority order:

1. **File path provided.** Use the given path.
2. **Default file present.** Use `./requirements/SPECIFICATION.md`
   (the default output of `/aor-req`).
3. **Inline SR text in the conversation.** If no path is given and no
   default file exists but the conversation contains SR text or a single
   SR-NNN body, use that as the input — do not error out. This is the
   exploratory-mode entry point: TC drafting on a single requirement
   without a file-system dependency.

If none of the three apply, error out and direct the user to `/aor-req`
first.

### Step 2: Draft Test Cases (TC-NNN)

For each SR (or each SR clause), generate at least:

1. **Happy path** — 1-2 scenarios with concrete data
2. **Edge cases** — boundary values, empty inputs, max/min, off-by-one
3. **Unwanted behaviour** — every If/Then in the spec gets a negative TC
4. **Security cases** — when input/auth/data storage is involved
5. **Property assertions** — invariants that must hold for any valid input

See `test-formats.md` for which format fits each EARS pattern.

**Clause-level traceability:** every TC tags the specific clause(s) it
verifies, e.g. `[SR-001.c1]`, not just `[SR-001]`. This catches partial
implementations that pass coarse-grained tests.

### Step 3: Verify TC quality

Apply the TC drafting checklist in `tc-checklist.md`. Each TC must satisfy
ISTQB T1-T10 (Correct, Complete, Feasible, Necessary, Traceable, Consistent,
Precise, Atomic, Observable, Independent).

### Step 4: Build the traceability matrix

Create or update `./requirements/TRACEABILITY.md` with:

- A UN→PR→SR→TC mapping table
- Coverage indicator per SR clause (covered / partial / gap)
- Any unresolved gaps flagged explicitly

See `templates.md` for format.

### Step 5: Validation plan

For each UN, draft a validation entry — this is human acceptance, distinct
from automated test cases:

| UN | Validator | Scenario | Question |
|----|-----------|----------|----------|
| UN-001 | {role} | {realistic usage scenario} | Does this serve the user need described in UN-001? |

### Step 6: Coverage check

Before declaring done:

- Every SR clause (`SR-NNN.cN`) has at least one TC
- Every If/Then (Unwanted Behaviour) SR has a negative TC
- Every input field has at least one error-condition TC
- Boundary values tested (min, min-1, max, max+1)
- Every cross-reference resolves to an existing identifier
- Validation plan covers every UN

## Large input handling

When the specification has more than ~100 SRs:

1. Process by SR-ID range in batches of 25 SRs.
2. For each batch:
   a. Draft TCs for the SRs in the batch.
   b. **Append** to the TC file (do not overwrite).
   c. Update `TRACEABILITY.md` incrementally with the new mappings.
   d. Report progress: "Batch <N> of <M> complete; <K> TCs drafted."
3. After all batches, run the coverage check on the full set.

If an SR is ambiguous, pause and request clarification before proceeding —
do not draft speculative TCs.

## Output paths

- `./requirements/TEST_CASES.md` — TC definitions
- `./requirements/TRACEABILITY.md` — UN→PR→SR→TC matrix and validation plan

(Some teams prefer to keep TCs inline in `SPECIFICATION.md`. If the user has
that convention, append TCs there instead.)

## Reference files

- `test-formats.md` — five TC formats with EARS-pattern mapping
- `tc-checklist.md` — TC drafting checklist
- `templates.md` — TRACEABILITY.md format and validation plan template
