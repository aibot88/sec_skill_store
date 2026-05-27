---
description: "Author a hardened spec through multi-pass adversarial review"
argument-hint: "<feature-id> <title> | <spec-id> --depth-pass-only [--lens <name>]"
effort: high
---

# /spec-author <feature-id> <title>

Author a hardened operational specification for a feature through multi-pass
adversarial review: structured authoring, falsification, and automatic
depth passes when critical findings indicate structural gaps. The output
is a complete spec file ready for `/spec-write` registration.

This skill operates on **design intent**, not implementation. The only code
read during authoring is pre-existing components (for prerequisite stubs).
Checking the spec against the feature's implementation is `/spec-verify`'s
job, not this skill's.

**Two entry paths:**

- **Default (fresh authoring):** `/spec-author <feature-id> <title>` — runs
  Pass 1 (draft) → Pass 2 (falsification) → Pass 3 (depth pass) → register.
- **Depth-pass-only:** `/spec-author <spec-id> --depth-pass-only [--lens <name>]`
  — re-falsify an existing APPROVED spec under the current lens corpus
  (or a specific lens). Skips Pass 1 and Pass 2. See the **Depth-pass-only
  mode** section below.

---

## Inputs expected in context

- The feature ID and title passed as arguments
- The feature brief (from `.feature/<slug>/brief.md` or user description)
- The domain analysis (from `.feature/<slug>/domains.md` if available)
- The work plan (from `.feature/<slug>/work-plan.md` if available)
- Optionally, a resolved spec context bundle from `/spec-resolve`

---

## Depth-pass-only mode

When invoked with `--depth-pass-only`, this skill skips Pass 1 (drafting)
and Pass 2 (initial falsification) and runs only the Pass 3 depth pass
against an existing APPROVED spec. Use this to re-falsify a mature spec
under the current lens corpus — typically because `/curate` flagged the
spec as authored before a falsification lens shipped (e.g., specs from
before the security lens added in v0.14.2).

**Invocation:**

```
/spec-author <spec-id> --depth-pass-only [--lens <lens_name>]
```

- `<spec-id>` — must resolve to an APPROVED spec via the manifest. DRAFT
  specs go through normal Pass 1/2/3; depth-pass-only refuses them.
- `--lens <name>` — optional. Bias the depth pass toward a specific lens
  reference. Without it, the full lens corpus applies. Lens references
  live at `prompts/audit/lens-<name>.md` (e.g., `lens-security.md`).
  See `scripts/lens-registry.txt` for the current set of lens names and
  their introduction dates.

**Behavior:**

1. **Resolve the target spec.** Look up `<spec-id>` via
   `spec_file_for_id` in the manifest. If state is not APPROVED, refuse
   and tell the user to use the default `/spec-author` flow instead.
2. **Validate the lens (if `--lens` given).** Check that
   `.claude/prompts/audit/lens-<name>.md` exists (installed layout) or
   `prompts/audit/lens-<name>.md` (dev-repo). If neither exists, list
   the available lenses (from `scripts/lens-registry.txt`) and stop.
3. **Skip the fresh-authoring pre-flight steps** (revival detection,
   work-group context, layered-spec family load) — they are scoped to
   new authoring. The only pre-flight needed for depth-pass-only is:
   - Read the spec body via the resolved file path.
   - If the spec has `parent_spec` set, run the layered-spec family
     load (Pre-flight Step 6) so siblings are visible to the depth pass.
   - Read any KB adversarial findings for the spec's domains (Pass 2
     "KB adversarial findings" loader).
4. **Skip Pass 1 and Pass 2.**
5. **Run Pass 3 with adapted inputs.** Dispatch the depth-pass subagent
   with:
   - The full spec body as input (not "Pass 1 draft").
   - Empty prior-findings set (the original Pass 2 findings are not
     retrieved — too lossy across kit versions; the depth pass starts
     fresh against the spec as it stands).
   - If `--lens <name>` was given: include the named lens reference
     prompt as additional context, with framing: "Focus your
     falsification on attack categories surfaced by this lens. Other
     lenses may apply but are secondary."
   - If `--lens` was not given: the full standard lens corpus.
6. **Standard arbitration UI.** Findings flow through the Pass 2/3
   arbitration grouping (confirmed gaps, implementation constraints,
   observability, uncertain). User accepts/declines per finding.
7. **Apply accepted findings** to the spec via the standard amendment
   flow (in-place edits + spec-write re-registration; the manifest's
   `version:` field bumps).

**Signal-to-noise expectation.** Lower than a fresh Pass 2 — specs in
production have already encountered real-world inputs and survived
many edge cases. A strong-model depth pass under a newer lens commonly
surfaces 5-15 findings on mature specs that predate the lens; some
will be already-mitigated in code (the spec just doesn't say so) and
others will be genuine gaps. The arbitration UI lets the user judge.

**Decline routing back to /curate.** If the user's arbitration declines
all findings as not-applicable, that's a signal the lens really doesn't
apply to this spec. Append a `falsification-decline` row to
`.curate/curation-state.md` keyed by `<spec-id>:<lens>` so future
`/curate` scans show the prior decline. This step only runs when
invoked via `/curate --verify` routing — manual invocations don't
record declines (the user can still surface them via /curate).

---

## Pre-flight

1. Run `/spec-resolve` if no context bundle is in your context:
   ```bash
   bash .claude/scripts/spec-resolve.sh "<feature description>" 25000
   ```

2. Read `.spec/CLAUDE.md` for the domain taxonomy.

3. Read any relevant KB entries and ADRs referenced in the domain analysis
   or context bundle.

4. **Revival detection:** Check for INVALIDATED specs in matching domains:
   ```bash
   INCLUDE_INVALIDATED=true \
     bash .claude/scripts/spec-resolve.sh "<feature description>" 25000
   ```
   If the bundle contains a `## INVALIDATED Specs (historical reference)`
   section, check whether any INVALIDATED spec's requirements overlap with
   the feature brief's intent (shared subject tokens, related domain).

   If overlap is found, present the INVALIDATED spec(s):
   ```
   ── Revival candidate ──────────────────────────
     <spec_id> — "<spec title>"
     Displaced by: <displacing spec id>
     Reason: <displacement_reason>
     Requirements: <count> (R1-R<N>)
   ```

   Use AskUserQuestion:
   - **"Use as reference"** — load the INVALIDATED spec as additional context
     for Pass 1. The spec is a *reference*, not a template — author the new
     spec fresh through the normal two-pass flow. After registration (via
     spec-write), set `revives: ["<old_spec_id>"]` in the new spec's
     frontmatter and update the old spec's `revived_by` field.
   - **"Author from scratch"** — proceed normally without the INVALIDATED
     spec as context.

   If no INVALIDATED specs overlap or the section is absent, skip silently.

5. **Work group context:** If `.work/` exists, run:
   ```bash
   bash .claude/scripts/work-context.sh --domains "<domains from spec-resolve bundle>"
   ```
   If output is non-empty, read it and note:
   - **Downstream consumers:** Which work definitions depend on specs in this
     domain. Surface: "WD-03 and WD-05 depend on specs in this domain — the
     spec you author will affect their readiness."
   - **Interface contracts:** If any work definition expects an interface
     contract (`kind: interface-contract`) in this domain, note it: "WD-02
     expects an interface contract at <path> — consider whether this spec
     should be authored as an interface contract."
   - This information does not change the authoring flow — it adds awareness
     of who will consume the spec being authored.

6. **Layered-spec family load (if amending a child spec):** If the target
   spec already exists in the manifest AND its frontmatter has a non-empty
   `parent_spec`, this is a child in a layered family. Adversarial review
   needs the parent (cross-cutting requirements) AND all siblings (cross-
   sibling contradictions) loaded as full files, not summaries. Re-run the
   resolver with sibling inclusion:

   ```bash
   EXPLICIT_SPEC_IDS="<target-spec-id>" INCLUDE_SIBLINGS=true \
     bash .claude/scripts/spec-resolve.sh "<feature description>" 40000
   ```

   `spec-resolve.sh` auto-includes the parent chain when a child is
   selected; `INCLUDE_SIBLINGS=true` adds every other child of the same
   parent. The resulting bundle becomes Pass 2 / Pass 3's "resolved
   context bundle" instead of the pre-flight default — falsification
   subagents need this richer family view to spot contradictions across
   the family.

   Also re-run the work-group context query against the family's domains
   (Step 5) so consumers of any sibling are surfaced.

   If the target is a top-level spec (no `parent_spec`), skip this step.

---

## Pass 1 — Structured authoring

**Mode: Author.** Fast, exploratory, high-trust. Produce the draft.

### Step 1a — Extract surface requirements

From the feature brief, domain analysis, and work plan, extract every
explicit requirement. These are the "what to build" requirements —
behavioral contracts, API signatures, storage formats, configuration
options.

Write each as a numbered requirement following the requirement rules:
- One falsifiable claim per requirement
- Explicit subject ("The vector index must..." not "Must...")
- Measurable condition where applicable
- Present tense, active voice
- **Behavioral, not structural:** every requirement must be verifiable by
  observing inputs and outputs, not by reading source code. Never reference
  specific class names, method names, file paths, or call chains. The spec
  describes what must be true; the work planner decides which constructs
  deliver it.
  - BAD: "The LsmVectorIndex.encodeFloat16s method must produce bytes"
  - GOOD: "Float16 encoding must produce big-endian bytes with length
    exactly dimensions * 2"
  - BAD: "IvfFlat.index() must quantize before calling assignCentroid"
  - GOOD: "Centroid assignment must use the quantized vector value, not
    the original float32 input"

### Step 1b — Identify prerequisites

For each surface requirement, ask: **"What must already be true in the
existing system for this requirement to hold?"**

For each assumption identified:
- Check the resolved context bundle for an existing spec that covers it
- If covered: add to the `requires` array
- If not covered: create a prerequisite stub (see /spec-write Step 2)
- Read the relevant existing code ONLY for prerequisite verification —
  do not read the feature's own implementation

### Step 1c — Expand by operational sequence

For each requirement that describes a temporal relationship ("X before Y",
"X uses the result of Y", "X must happen during Z"):

Trace the operational sequence step by step:
1. What is the input to each step?
2. What transformation happens?
3. What is the output?
4. Who consumes the output?
5. At which step does the requirement's constraint apply?

If the trace reveals that the requirement is ambiguous about *when* in the
sequence the constraint applies, split into separate requirements that
specify the exact step.

**Example:** "Centroid assignment must use the quantized vector" is
ambiguous. The operational trace reveals: input arrives as float32 →
encoding quantizes to float16 bytes → decoding produces float32 from
float16. The requirement must specify: "centroid assignment must use the
quantized vector value (the result of encoding to the configured precision
then decoding back to float32), not the original float32 input." Note:
the requirement describes the behavioral constraint (use quantized value),
not the implementation mechanism (which methods to call in which order).

### Step 1d — Expand by failure mode

For each component or technology the feature touches, search for known
failure modes BEFORE reading the design:

- IEEE 754 edge cases for floating point
- Concurrency hazards for shared data structures
- Encoding format ambiguities for serialization
- Input validation gaps for API boundaries
- Precision/rounding issues for numerical computation

Build a checklist from what you find. Then review each surface requirement
against the checklist. For each failure mode that isn't addressed by an
existing requirement, add a requirement.

### Step 1e — Declare concurrency contracts

For every construct introduced by this spec, add a concurrency requirement.
This is not optional — see the concurrency contract probe in Pass 2a for
the full rationale.

For each construct, ask the user (or determine from the domain analysis):
- Will this be used from multiple threads?
- If shared: what concurrency model? (immutable, synchronized, confined)
- If not shared: state it explicitly as a requirement

If the answer is unknown, write the requirement as thread-confined by
default: "This type is not thread-safe. Callers must not share instances
across threads without external synchronization." The user can upgrade
to thread-safe during review if the use case demands it.

This step ensures that Pass 2 falsification has a concurrency contract to
verify against, rather than discovering the gap and having to add it.

### Step 1f — Collapse user decisions, expand requirements

Review the requirements for clusters that stem from the same conceptual
decision. For each cluster:
- State the conceptual decision once in the Design Narrative
- Keep individual requirements separate (they evolve independently)
- Ensure the user would only need to make one decision, not N

### Step 1f — Write the draft

Assemble the requirements into a spec file following the format in
`.spec/CLAUDE.md`. Include:
- All numbered requirements grouped by category
- Design Narrative (Intent, Why this approach, What was ruled out)
- Front matter with domains, requires, decision_refs, kb_refs
- `[UNVERIFIED]` annotations on any requirement you couldn't confirm

Present the draft to the user. Do NOT proceed to Pass 2 until the user
confirms the draft direction is correct. The user may add, remove, or
adjust requirements at this point.

---

## Pass 2 — Adversarial falsification

**Mode: Adversarial.** Slow, zero-deference, exhaustive. Treat the Pass 1
output as a hypothesis to be falsified.

### KB adversarial findings (load before launching subagent)

If `.kb/CLAUDE.md` exists, scan the Topic Map for categories relevant to
this feature's domains. Read any `type: adversarial-finding` entries in
matching categories. These are real bug patterns from prior audits — concrete
attacks that broke real code in similar domains.

Pass these findings to the subagent as additional input. They provide
concrete attack vectors that the falsification pass should check against
each requirement. A KB entry like `nan-score-ordering-corruption` turns
"what about NaN?" from an abstract question into a proven failure pattern
with specific test guidance.

### Implementation grounding (load before launching subagent)

Read the source files that the feature will modify or interact with.
Use the domain analysis (`domains.md`) file list and the work plan stubs
(if available) to identify which files exist. Read method signatures,
type declarations, and API boundaries — not full implementations.

The purpose is NOT to spec implementation details. It is to discover
which concrete technology decisions the implementation will encounter:
- Does the code use floating point? → IEEE 754 edge cases are real, not abstract
- Does it manage resources (streams, connections, handles)? → lifecycle bugs are real
- Does it parse external input? → encoding/validation gaps are real
- Does it share state across threads? → concurrency hazards are real

Without this grounding, the falsification pass reasons about spec text
in isolation and misses gaps that are obvious when you see the actual
types involved. A spec that says "numbers stored as text" doesn't trigger
"what about NaN?" until you see that the implementation uses `double`.

Launch a subagent for this pass. The subagent receives:
- The complete draft spec from Pass 1
- The feature brief and domain analysis
- The resolved context bundle
- The list of prerequisite stubs created in Pass 1
- KB adversarial findings for the feature's domains (if any)
- Key source file signatures from the feature's domain (types, method
  signatures, API boundaries — NOT full implementation bodies)

The subagent's prompt must include:

### 2a — Requirement-level falsification

For each requirement in the draft, begin with the assertion: **"This
requirement is complete and unfalsifiable."** The adversary's job is to
disprove this by constructing a concrete attack — a specific input,
sequence of operations, or initial state that produces wrong behavior
while technically satisfying the requirement text.

For each successful disproof, produce:
1. **Requirement:** the specific requirement being challenged (by number)
2. **Attack:** the concrete scenario — exact input values, operation
   sequence, or initial state that triggers the failure
3. **Expected wrong behavior:** what breaks, and how an observer would
   detect it
4. **Gap in requirement text:** which specific words are ambiguous,
   missing, or overly broad, and why they permit the attack
5. **Tightened requirement:** suggested replacement text that closes
   the gap

**KB adversarial pattern check (mandatory if findings were provided).**
For each adversarial-finding entry provided, check whether any requirement
in the draft is vulnerable to the same pattern. The entry's `domain` field
tells you which requirements to focus on. The `## Test guidance` section
describes the specific attack. The `## What happens` section describes the
failure mode.

For each match: construct a concrete attack against the specific
requirement (not just "this pattern might apply" — show exactly which
requirement, which input, what breaks). If the requirement already handles
the case, note it and move on. If it doesn't, produce a finding.

**Degenerate value checklist (mandatory).** For every requirement that
involves a typed value (numeric, string, collection, or nullable), check
these cases mechanically. These are language-agnostic — they apply
regardless of implementation language.

Numeric types:
- NaN — not-a-number. Can the value be NaN? What happens downstream?
- Positive and negative infinity — same questions.
- Negative zero — does -0.0 vs 0.0 matter for equality, ordering, display?
- Boundary values — if the spec declares a precision or range, what
  happens at and beyond the boundary? (overflow, underflow, truncation)
- Zero — does zero have special semantics? Division, indexing, sizing?

String/text types:
- Empty string — vs null vs absent. Are these three cases distinguished?
- Null bytes — embedded \0 in strings. Truncation risk.
- Unicode boundaries — surrogate pairs, BOM, RTL markers, combining chars.

Collection types:
- Empty collection — zero elements. Does downstream code assume non-empty?
- Single element — boundary between "one" and "many" behavior.
- Null elements — can the collection contain nulls? What happens?

Nullable/optional types:
- Null vs absent vs default — are these three states distinguished?
  A field that is null, a field that is missing, and a field that has its
  default value may need different behavior.

Size/capacity:
- Maximum size — if the spec declares a limit, what happens at the
  limit and one beyond it? Is the error behavior specified?

For each case that produces wrong or unspecified behavior: produce a
finding using the standard format above.

**Boundary validation probe (mandatory).** For every requirement that uses
"reject", "validate", "must not accept", or "throw on invalid":
- Is the validation unconditional? Could it be bypassed by configuration,
  optimization, debug flags, or assertion settings?
- Are ALL entry points that could send invalid data enumerated? For each
  entry point, does validation happen there or does a requirement on the
  caller guarantee validity?
- Is the validation complete? If the requirement says "reject invalid X",
  does it enumerate what "invalid" means, or could an implementation
  interpret it narrowly?
- For mutable inputs: is the validation on the value at call time, or
  could the caller mutate the input after validation but before use?

**Standards compliance probe (mandatory).** For every requirement that
references a standard, specification, or protocol (RFC, IEEE, Unicode,
HTTP, SQL, etc.):

A compliance claim is a contract. "Compliant with RFC 8259" means the
implementation MUST accept everything the RFC says is valid and MUST
reject everything the RFC says is invalid. No exceptions, no "we're
stricter." If the spec rejects something the standard allows, the spec
is non-compliant — period.

- Identify every OTHER requirement in the spec that restricts or extends
  the standard's behavior. For each one: does the standard allow what the
  spec rejects? If yes, the compliance claim is false. The spec must
  either remove the restriction, or replace the compliance claim with an
  explicit deviation list: "Implements RFC 8259 with the following
  deviations: (1) duplicate keys rejected, (2) trailing content rejected."
  These are not stricter compliance — they are deviations from the
  standard that must be documented as requirements.
- For every degenerate case in the standard (empty values, maximum sizes,
  optional features, deprecated behaviors): does the spec handle it? If
  the standard allows empty string keys and the spec says "non-blank
  keys", that is a contradiction — produce a finding.
- Every deviation from the standard must be its own numbered requirement
  so it can be tested independently. "Stricter than RFC 8259" is not a
  requirement — it's a vague claim. "Rejects duplicate keys (deviation
  from RFC 8259 Section 4)" is a testable requirement.

**Resource lifecycle probe (mandatory).** For every requirement that
introduces a closeable, disposable, or acquirable resource — or any
construct that wraps streams, connections, handles, buffers, or locks:
- What happens to objects derived from this resource (iterators, streams,
  cursors, views) after the resource is closed? Must they throw, or can
  they silently return stale data?
- What happens if creation/construction fails partway? Are partially
  allocated sub-resources released?
- What happens if close/dispose itself fails? Is the resource left in a
  usable state, an unusable state, or an undefined state?
- What happens if close is called twice? Must it be idempotent?

**Cross-construct atomicity probe (mandatory).** Review the full
requirement set for groups of requirements that describe the same
logical operation across multiple constructs (e.g., "insert updates
index A" + "insert updates index B"):
- If one succeeds and the other fails, what state is the system in?
- Is partial completion acceptable, or must the operation be atomic?
- If atomic: is the rollback mechanism specified? What state do
  observers see during the operation?
- If not atomic: is the partial-failure state documented? Can the
  system recover, or is manual intervention required?

**Error propagation probe (mandatory).** For every requirement that
specifies an error, exception, or failure condition:
- After the error occurs, what is the state of the object that threw?
  Is it reusable without re-initialization?
- If the operation was mid-stream (writing, parsing, iterating), what
  happens to output written so far? Is it visible to observers? Is it
  valid?
- If the object holds shared resources (streams, buffers, connections),
  what state are those resources in after the error? Must the caller
  close/dispose them explicitly?
- Can the error propagate to a context where it's unexpected? (e.g.,
  a checked exception thrown through an interface that doesn't declare it)

**Identity and equality probe (mandatory).** For every data type
introduced by the spec that will participate in comparison, lookup,
deduplication, caching, or sorting:
- What does equality mean? Reference identity, structural equality, or
  domain-specific equivalence?
- If the type contains fields with non-obvious equality semantics
  (floating point, opaque handles, lazy-loaded values), does the spec
  define how those fields affect equality?
- If two instances are "equal", can they be substituted for each other
  in all contexts? If not, the spec needs a weaker equivalence relation.

**Concurrency contract probe (mandatory).** Every construct introduced
by the spec must declare its thread-safety model. This is not optional
— the absence of a concurrency statement is a spec gap, because it
leaves the implementer guessing and the test writer unable to verify.

For every construct (type, interface, resource, service) in the spec:
- Is it designed to be called from multiple threads? If yes: what is
  the concurrency model? (immutable, internally synchronized, requires
  external synchronization, thread-confined)
- If NOT designed for concurrent use: the spec must say so explicitly.
  "This type is not thread-safe — callers must not share instances
  across threads without external synchronization" is a requirement.
- For constructs that manage shared resources (caches, pools, registries,
  indexes): concurrent access is likely regardless of intent. The spec
  must declare whether concurrent operations are safe, and if so, what
  guarantees hold (atomicity of individual operations, consistency of
  compound operations, visibility of mutations).
- For compound operations (check-then-act, get-or-create, position-then-
  read): are they atomic? If not, the spec must state that callers are
  responsible for atomicity.

A spec that says nothing about concurrency is incomplete. The test writer
cannot write concurrency tests without knowing the contract. The
implementer cannot choose between synchronized and unsynchronized without
knowing the intent. Declare it.

**Trust boundary probe (mandatory).** For every requirement that
describes a predicate, status check, or query consumed by other
constructs:
- Does the predicate have sub-states within "true"? (e.g., "is member"
  could mean active, joining, or leaving.) Do all consumers agree on
  which sub-states count as true?
- If the input comes from another construct (not user input), does the
  spec explicitly trust it ("assumes X is valid, validated by Y") or
  validate it? Implicit trust is a spec gap.

For each case that produces wrong or unspecified behavior: produce a
finding using the standard format above.

If the adversary cannot construct a concrete attack for a requirement,
the requirement stands as written. No changes.

Bare assertions that a requirement "could be" violated without a concrete
attack are not findings. The burden of proof is on disproof, not on the
requirement.

### 2b — Enforcement path tracing

For each NEW requirement proposed in this pass:
- If it adds validation ("must reject X"): identify all callers that
  could send X. For each caller, either add a filtering requirement or
  confirm the caller already prevents X.
- If it changes behavior ("must do X instead of Y"): identify all
  consumers that depend on old behavior Y.
- **A requirement that creates a cascading failure when enforced is a
  spec defect, not a finding.**

### 2c — Cross-requirement interaction

Review the full requirement set (Pass 1 + new additions) for:
- **Contradictions:** two requirements that cannot both be satisfied
- **Cascading failures:** requirement A, when enforced, causes
  requirement B to fail
- **Ordering dependencies:** requirement A must be implemented before B
  but this ordering isn't stated
- **Atomicity gaps:** multiple requirements that describe the same
  logical operation on different constructs. If one can succeed while
  another fails, the partial-failure state must be specified.
- **Ambiguous alternatives:** a requirement that uses "either X or Y",
  "may", or conditional language allowing two mutually exclusive
  implementations. If two test writers could independently write tests
  that contradict each other while both satisfying the requirement,
  the requirement is ambiguous and must be tightened. Replace "either
  X or Y" with a concrete choice. The spec makes the decision — the
  implementer should not have to choose.

### 2d — Cross-module boundaries

Search the codebase for other implementations of the same concepts:
- Are there multiple encode/decode paths for the same data?
- Are there utility classes in other modules that duplicate functionality?
- Could a maintainer accidentally use the wrong implementation?

For each found: add a requirement that specifies which implementation
to use and prohibits cross-use.

### 2e — Observability of silent failures

For each failure mode in the spec that produces no error (silent
degradation, invisible data, suppressed exceptions):
- Is there a way for an operator to detect it?
- If not, add a requirement that the behavior is documented in the
  public API, or add a diagnostic mechanism.

### 2f — Uncertainty disclosure

For each finding where you are uncertain whether it's a real gap:
- State what you're uncertain about
- State what would need to be true for it to be a real gap
- Let the user decide — don't suppress uncertain findings

---

## Arbitration

**Mode: Arbitration.** User has design authority, agent has technical
accuracy.

Present the Pass 2 findings to the user, grouped by:
1. **Confirmed gaps** — requirements that are definitely missing
2. **Implementation constraints** — requirements that clarify how
   something must be done (operational sequence, enforcement path)
3. **Observability** — silent failure modes that need documentation
4. **Uncertain** — findings where you couldn't determine if it's a real gap

For each finding, provide:
- What's missing (the unspecified behavior)
- What breaks (the concrete failure scenario)
- Suggested requirement text

The user decides what to include, adjust, or drop. Apply their decisions
to the spec.

### Just-in-time subdivision signal (after arbitration applied)

After applying the user's arbitration decisions, evaluate the spec's
post-amendment shape against the natural-progression heuristic. The
goal is a non-blocking heads-up — if this amendment has tipped the
spec into "multiple distinct concerns at scale" territory,
`/spec-split` is now an option.

Mechanical check (apply mentally — no script needed):

1. Count R-numbered requirements (lines matching `^R[0-9]+`).
2. Count distinct concern-style section headers in the machine section
   (`## <Concern>` or `### <Concern>` — exclude headers named
   "Notes", "Narrative", "Design", "History", "Appendix").
3. For each section, count the requirements under it. Track the
   largest section's count.
4. Apply the same thresholds `/curate` uses (so detection here matches
   what /curate would flag at the next housekeeping pass):

   - Reqs ≥ 50 OR machine-section size ≥ ~15K tokens (~60 KB)
   - Section count ≥ 2
   - Largest section's share < 90% of total reqs (otherwise the spec
     is large-but-singular, not a real subdivision candidate)
   - Spec does NOT already have `parent_spec` set (skip — already
     part of a layered family)

If all thresholds match, surface alongside the Pass 2 findings with
this exact framing — note its non-blocking nature explicitly so the
user knows it's information, not a request:

```
── Just-in-time subdivision signal ───────────────
This spec now sits in subdivision territory:
  N requirements across M concern sections
  Largest section: <section name>  (K reqs, P% of total)

After this amendment lands, consider:
  /spec-split <spec-id>

This is a heads-up, not a blocker. Proceed to Pass 3 normally. The
candidate will also surface at the next /curate run.
```

If the thresholds do NOT match, do not surface anything — silence is
the default when subdivision isn't applicable. Don't draw attention
to the absence of the signal.

This signal does NOT block Pass 3. It does NOT modify any file. It
just informs the user that natural subdivision has become an option.

---

## Pass 3 — Depth pass (mandatory)

After applying the user's arbitration decisions from Pass 2, automatically
run a depth pass. Do not prompt — this is mandatory.

(Pass 3 is also the entry point for **depth-pass-only mode** — see the
top-of-file section. When entered via `--depth-pass-only`, the depth
pass runs against the existing spec body with empty prior-findings,
optionally biased toward a single lens reference.)

Round 2 fixes create new attack surface that round 1 could not see.
Empirical data across multiple specs shows round 2 consistently finds
critical/high issues that are *consequences* of round 1 fixes: deadlocks
from new thread models, budget fictions from abstraction changes,
duplicate data from retry semantics. These are invisible to a single
falsification pass.

### Depth pass execution

The depth pass is structurally identical to Pass 2 (same subagent setup,
same falsification lenses, same arbitration mode) with two additions:

1. **Prior findings as input.** The subagent receives all accepted findings
   from Pass 2 as additional context. These are attack vectors — knowing
   "credits shifted from physical slabs to logical budget" tells the depth
   pass to probe whether the budget actually bounds what it claims to.

2. **Duplicate suppression.** The subagent must not re-report findings
   already accepted in Pass 2. If a finding overlaps with an existing
   requirement added during arbitration, skip it.

After the depth pass, present findings in the same arbitration format.
Apply the user's decisions to the spec.

### Pass 4+ — Prompted on severity

After the depth pass, evaluate the accepted findings:

**If any critical or high findings were found:** use AskUserQuestion:
- "Run another pass" (description: "Critical/high findings suggest more may remain")
- "Done" (description: "Proceed to output")

**If only medium/low findings:** proceed to output. Diminishing returns
are likely.

There is no limit on passes, but each subsequent offer beyond pass 3
should note diminishing returns. Empirically: pass 3 captures the
fix-consequence bugs, pass 4+ is rarely productive.

---

## Output — Register the spec

After all adversarial passes are complete and arbitration decisions applied,
register the spec by invoking `/spec-write "<id>" "<title>"` directly.

**This is mandatory.** `/spec-author` owns the full lifecycle: draft →
falsify → arbitrate → register. The caller should never need to call
`/spec-write` separately. This prevents the shortcut where an unfalsified
draft gets registered without adversarial review.

After `/spec-write` completes, verify the spec is in APPROVED state in
`.spec/registry/manifest.json`. If it registered as DRAFT (due to
unresolved conflicts), report the issue — do not silently return.

---

## Hard constraints

- Never read the feature's implementation during authoring — only
  pre-existing code for prerequisite stubs
- Never skip Pass 2 — nothing advances past a draft without a
  falsification pass
- Never skip Pass 3 — the depth pass is mandatory, not severity-gated
- Never suppress uncertain findings — surface them for arbitration
- Never add a validation requirement without tracing its enforcement path
- Always present the draft to the user between Pass 1 and Pass 2
- The subagent for Pass 2 must receive the complete Pass 1 output, not
  a summary — summaries lose the detail that adversarial review needs
- Always register the spec via `/spec-write` at the end — the caller
  must never need to call `/spec-write` separately
