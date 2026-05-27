---
name: aor-req
description: Author User Needs (UN), Product Requirements (PR), and Software Requirements (SR) using EARS-12 patterns with full UN→PR→SR traceability.
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion
argument-hint: "[scope description, or path to source file]"
---

# /aor-req — Requirements Authoring

Drafts UN, PR, and SR following EARS-12 patterns, INCOSE C1-C9 quality
attributes, and canonical cross-reference syntax. Output is markdown.

> **Note on skills vs agents.** The AOR bundle contains *skills* at
> `.claude/skills/aor-*/SKILL.md` (invocable directly, like this one)
> and *SME agents* at `.claude/agents/aor-sme-*.md` (sub-agent system
> prompts spawned only by `aor-review` / `aor-review-adhoc`). Do NOT
> invoke an agent as a skill — it will fail with "skill not found".

## Operating discipline

Apply throughout. State each at startup so the user sees it.

- **Mode (declared at startup):** ask whether this is an *exploratory*
  session (single requirement, conversational, no files) or a *document*
  session (full specification authoring, files written). Default to
  exploratory if scope arrives as inline text without a file path,
  document otherwise. The mode controls whether Steps 5–7 write to disk.
- **Invocation acknowledgement:** the first response of the skill states
  "Running as `aor-req` in <mode> mode. Files written to <output path>
  unless you ask otherwise." Eliminates the "did the skill actually run?"
  ambiguity.
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

### Step 1: Establish scope

If the user passed scope text or a file path, use it. Otherwise, ask via
AskUserQuestion: "What features or changes should be specified?"

**Distinguishing scope text from a file path** (REQ-B): treat the input
as a path if any of (a) it contains `/` or `\`, (b) it ends in `.md` /
`.txt` / `.xlsx` / `.csv` / `.docx`, or (c) it resolves to an existing
file on disk via `Read()`. Otherwise treat it as scope text — including
multi-word descriptions like "patient appointment booking system".

**Tie-breaker:** if only rule (c) matches (no `/` or `\`, no recognized
extension, but `Read()` resolves) AND the input is a single word,
confirm with the user before treating as path: "I see a file named
`<input>` exists. Did you mean that file, or is that a scope
description?"

For Excel-sourced inputs, expect the host LLM to have transcribed rows into
a working markdown buffer before this skill runs (the bundle doesn't parse
Excel directly).

### Step 1a: Classify the level

If exploratory mode, ask:

> "Is this a User Need (UN), Product Requirement (PR), or Software
> Requirement (SR)?"

Skip unused steps once the level is known: UN review needs Step 2; PR
review needs Step 3 + Echo Gate; SR review needs Steps 4–6.

**Multi-level input in exploratory mode:** if the user provides a
UN+PR+SR set (or any combination of multiple levels) instead of
selecting one, treat as a multi-level review — walk Steps 2–4 across
the provided levels in order, but keep exploratory file-write
discipline (no automatic disk writes; surface findings inline).

If document mode, default to walking all three levels (UN → PR → SR)
across Steps 2–4 unless the user specifies otherwise.

### Step 2: Write User Needs (UN-NNN)

For each distinct stakeholder need, write one UN. Rules:

- Technology-agnostic, stakeholder-voiced
- Plain narrative (NOT EARS syntax)
- Include problem statement (2-3 sentences) + need statement
- Tag a persona via `traces_to::UN->Persona [<persona-id>]`
- Priority: Critical | High | Medium | Low

See `templates.md` for format.

### Step 3: Write Product Requirements (PR-NNN)

For each UN, derive PRs:

- Technology-agnostic, measurable, objective
- EARS syntax (see `ears-guide.md` for the 12 patterns)
- Each PR traces backward: `derived_from::PR->UN [UN-NNN]`
- Each PR traces forward: `traces_to::PR->SR [SR-NNN]`
- Every happy-path PR must have at least one If/Then (Unwanted) PR companion
- The same If/Then companion rule applies at the SR level in Step 4 — every happy-path SR must have an If/Then SR companion specifying the implementation-level recovery
- Every EARS-N (negative/`shall not`) PR must have at least one positive companion PR (Ubiquitous, Event-Driven, or State-Driven) specifying the expected correct behaviour; the same rule applies at the SR level

**"Happy-path" defined** (REQ-E): a PR is happy-path if it uses one of
the positive EARS patterns — Ubiquitous, Event-Driven, State-Driven,
Optional, Complex, EARS-E, EARS-T, EARS-P. Excluded: Unwanted Behaviour,
EARS-N (negative/`shall not`), EARS-F (failure-mode declarative).

Run **Adversarial Error Decomposition** for each UN:

1. How does it fail silently?
2. How does it fail noisily?
3. How does it fail under load?
4. How does it fail under malice?
5. How does it fail over time?

Each failure mode becomes either an EARS If/Then PR (tag with `[ADV]` in the
heading; identifier stays canonical, e.g., `PR-007 [ADV]`) or a note for a
separate risk register.

**Worked example.** UN: "preserve every uploaded file". Failure mode: "fails
silently when disk free space is exhausted". Resulting PR:

```
### PR-007 [ADV]: Reject upload when disk pressure is high
If disk free space drops below 5%, then the system shall reject new uploads
with HTTP 507 Insufficient Storage and return a Retry-After header.
derived_from::PR->UN [UN-001]
traces_to::PR->SR [SR-014]
```

Note that the failure mode is concrete and quantified (5%, HTTP 507,
Retry-After) — that's what makes the PR verifiable (C7).

### Step 4: Write Software Requirements (SR-NNN)

For each PR, derive SRs:

- Implementation-specific: name services, APIs, databases, error codes
- EARS syntax with specific component names
- Each SR traces backward: `derived_from::SR->PR [PR-NNN]`
- Each SR traces forward: `traces_to::SR->TC [TC-NNN]`
- Use clause-level granularity (`SR-NNN.c1`, `.c2`) to consolidate related
  behaviours under a single SR ID
- Every happy-path SR must have at least one If/Then (Unwanted) SR
  companion (see Step 3 for the "happy-path" definition)
- Every EARS-N SR must have at least one positive companion SR

### Step 5: Field Specification Tables

For features with data input/display, add field specification tables in the
SR section:

| Field ID | Name | Label | Type | Min | Max | Unit | Default | Required | UI Exposure | Validation Rule | Error Msg | Parent SR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

UI Exposure values: `editable` | `display-only` | `hidden`.

### Step 6: Echo Gate

For each SR clause, write a one-line testable assertion:

```
VERIFY: [SR-NNN.c1] — [restatement of the requirement as a testable assertion]
```

If you cannot write the assertion, the requirement is untestable — rewrite it.

### Step 7: Completeness check

Run the checklist in `completeness.md` before declaring authoring done.

## Large input handling

When input exceeds ~200 source items (e.g., a large Excel paste):

1. Split into batches of 50 rows.
2. For each batch:
   a. Read the batch.
   b. Transcribe to markdown UN/PR/SR per the steps above.
   c. **Append** to the working file (do not overwrite).
   d. Report progress: "Batch <N> of <M> complete; <K> requirements drafted."
3. After all batches, run the completeness check on the full file.

If a batch contains ambiguous input, pause and ask for clarification before
continuing — do not skip rows silently.

## Output paths

Default: `./requirements/SPECIFICATION.md` for the consolidated UN/PR/SR.
The user can override.

When updating an existing file, preserve existing IDs — append new ones with
the next sequential number.

## Cross-reference syntax (cheat sheet)

```
relation_type::SOURCE->TARGET [ID-list]
```

| Type | Direction | Use |
|---|---|---|
| `traces_to` | forward | UN→PR, PR→SR, SR→TC, UN→Persona |
| `derived_from` | backward | PR→UN, SR→PR, TC→SR |
| `validates` | verification | TC→SR |
| `mitigates` | risk control | SR→RISK |
| `conflicts_with` | contradiction | any→any |

## Identifier format

Regex: `^(UN|PR|SR|TC)-\d{3}(\.[A-Z])?$`

- Base IDs: `UN-001`, `PR-001`, `SR-001`
- Sub-IDs (EARS-P tabular): `PR-010.A`, `PR-010.B`
- Clause notation: `SR-001.c1`, `SR-001.c2`

## Reference files

- `ears-guide.md` — the 12 EARS patterns
- `templates.md` — markdown templates for UN/PR/SR sections
- `completeness.md` — exit checklist (UN→PR→SR coverage)
