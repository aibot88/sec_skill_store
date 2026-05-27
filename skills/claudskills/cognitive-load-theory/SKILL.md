---
name: cognitive-load-theory
description: "Sweller's Cognitive Load Theory (CLT) for agents writing skill content, designing prompts, building UI/dashboards, and authoring documentation. Working memory holds roughly 4 chunks at a time; CLT classifies load into three types — intrinsic (irreducible task difficulty), extraneous (unnecessary load from poor presentation, ELIMINATE), and germane (load that builds schemas, PROMOTE). Use when writing a SKILL.md body (does this section add extraneous load?), designing prompts (am I asking the model to hold too much at once?), building dashboards (what is the per-screen cognitive budget?), or authoring docs (is intrinsic load minimized via segmentation?). Do NOT use for retrieval and context-loading design (use context-management), prompt engineering tactics (use prompt-craft), or instructional design beyond what grounds the theory."
license: MIT
compatibility:
  notes: "Markdown, Git, any agent-skill runtime"
allowed-tools: Read Grep
metadata:
  schema_version: 7
  version: "1.0.0"
  type: capability
  category: quality
  domain: quality/cognition
  scope: portable
  owner: skill-graph-maintainer
  freshness: "2026-05-19"
  drift_check: "{\"last_verified\":\"2026-05-19\"}"
  eval_artifacts: present
  eval_state: unverified
  routing_eval: absent
  stability: experimental
  keywords: "[\"cognitive load theory\",\"working memory\",\"intrinsic load\",\"extraneous load\",\"germane load\",\"chunking\",\"segmentation\",\"schema formation\",\"Sweller\",\"prompt design\",\"skill writing\",\"documentation load\",\"dashboard cognitive budget\",\"information design\"]"
  triggers: "[\"cognitive-load-skill\",\"working-memory-skill\",\"clt-skill\"]"
  relations: "{\"adjacent\":[\"teaching-patterns\",\"context-window\",\"compression\",\"editorial-standards\",\"prompt-craft\"],\"boundary\":[{\"skill\":\"context-management\",\"reason\":\"context-management owns retrieval and session working-set design; CLT owns the cognitive-load taxonomy applied to authored content\"},{\"skill\":\"memory-gardener\",\"reason\":\"memory-gardener owns memory pruning and consolidation; CLT owns the cognitive-load framing for what to keep vs cut\"}],\"verify_with\":[\"context-management\",\"teaching-patterns\",\"best-practice\"]}"
  skill_graph_source_repo: "https://github.com/jacob-balslev/skill-graph"
  skill_graph_protocol: Skill Metadata Protocol v5
  skill_graph_project: Skill Graph
  skill_graph_canonical_skill: skills/cognitive-load-theory/SKILL.md
  structural_verdict: UNVERIFIED
  truth_verdict: UNVERIFIED
  comprehension_verdict: UNVERIFIED
  application_verdict: UNVERIFIED
---

## Concept Card

**What it is:** Cognitive Load Theory (CLT) is a psychological framework originating with John Sweller (1988) that explains how human working memory processes new information and what design decisions help or hinder schema formation. It is the scientific backbone behind "keep it simple" intuitions — but with actionable precision about *which* complexity to cut and which to preserve.

**Mental model:** Working memory is a small workspace — roughly 4 independent chunks at once (Miller's 7±2, revised by Cowan to ~4). CLT divides the total load on that workspace into three additive buckets: intrinsic (the task itself), extraneous (how you presented the task), and germane (the effort of building a mental model). Total load must stay below capacity or learning and comprehension fail.

**Why it exists:** Without CLT, agents default to "simplify" without knowing what to cut. They might remove worked examples (germane load, valuable) while keeping verbose prose around a table (extraneous load, wasteful). CLT gives a precise vocabulary for the tradeoff.

**What it is NOT:** Not a general UX heuristic. Not the same as plain-language writing. Not about reducing all complexity — germane load (building schemas) is *desirable* and should not be minimized. Not retrieval design (see `context-management`).

**Adjacent concepts:** working memory, chunking, schema theory, dual-channel processing (Mayer's multimedia learning), segmentation principle, split-attention effect, redundancy effect.

**One-line analogy:** CLT is like RAM management for humans — intrinsic load is the program you must run, extraneous load is unnecessary background processes, and germane load is the OS caching data so the next run is faster.

**Common misconception:** "Reducing cognitive load always means making things shorter or simpler." Wrong — cutting worked examples, removing context, or over-abstracting increases intrinsic load and destroys germane load. The correct target is *extraneous load only*.

# Cognitive Load Theory

## Domain Context

**What is this skill?** Sweller's Cognitive Load Theory for agents writing skill content, designing prompts, building UI/dashboards, and authoring documentation. Use when evaluating whether a skill body, prompt, UI screen, or doc section is imposing unnecessary cognitive load on its reader or user. Do NOT use for retrieval and context-loading design (use `context-management`), prompt engineering tactics (use `prompt-craft`), or instructional design beyond what grounds the theory here.

## Coverage

The three-load taxonomy (intrinsic, extraneous, germane) with definitions and examples; working memory limits and chunking strategies; application to skill writing, prompt design, and UI/dashboard cognitive budgets; a worked example reducing extraneous load in agent audit output; and common failure modes including the "simplify to lose germane content" trap. Does not cover Mayer's multimedia learning extensions, split-attention effect research design, or assessment/test design.

## Philosophy

Every agent output — a SKILL.md body, a prompt, a dashboard widget, a Linear comment — competes for space in the reader's working memory alongside everything else they hold. An agent that generates a 3-paragraph preamble before the actual answer forces the reader to hold that prose until they reach the substance. An agent that uses a consistent table format for comparative data lets the reader chunk the format into a single schema slot and spend their remaining capacity on the content. CLT is the theoretical justification for structure-over-prose, examples-before-explanation, and segmentation. Without it, quality guidance is cargo-culted. With it, agents can reason precisely about *why* a design choice reduces or increases cognitive burden.

## Cross-Domain Synergy

CLT is the theoretical foundation that neighboring skills draw on implicitly:
- **`teaching-patterns`**: Uses CLT when choosing progressive disclosure (segmentation), worked examples (germane load promotion), and scaffolding removal.
- **`context-management`**: The discipline of controlling what enters a session is CLT applied to the agent's own working memory, not just the human reader's.
- **`context-window`**: Token budget management mirrors the working-memory budget — both measure available capacity against load.
- **`compression`**: Token-efficient compression is an application of extraneous-load elimination.
- **`editorial-standards`**: Structure-over-prose editorial rules are CLT operationalized for written output.

---

## 1. When to Invoke CLT

Use this skill when answering any of these questions:

| Question | CLT lens |
|----------|----------|
| "Is this skill section too long?" | Which load type is the length adding? Cut only extraneous. |
| "Should I split this prompt into two?" | Intrinsic load exceeds single-session working-memory capacity → segment. |
| "Why is this dashboard hard to read?" | Per-screen load budget exceeded; identify extraneous elements to remove. |
| "Should I remove this example from the skill?" | Only if it's redundant (extraneous). If it builds a schema, it's germane — keep it. |
| "Does this doc section need more context?" | Yes if removing context increases intrinsic load for the reader. |
| "Should I use a table or prose here?" | Table chunks multiple dimensions into one schema slot → lower extraneous load. |

**Do NOT invoke this skill for:**
- Deciding *what* retrieval files to load in a session (use `context-management`)
- Writing the actual copy / prose (use `editorial-standards`)
- Choosing prompt phrasing strategies (use `prompt-craft`)

---

## 2. The Three Load Types

### 2.1 Intrinsic Load — irreducible difficulty of the task itself

Determined by the element interactivity of the material: how many things must be held *simultaneously* because they interact with each other. High interactivity = high intrinsic load.

| Signal | Example |
|--------|---------|
| Many interdependent concepts | Debugging a recursive algorithm while tracking stack frames |
| Prior knowledge required | Reading a diff that assumes familiarity with a domain-specific pattern |
| Multiple steps that reference each other | A 7-step migration guide where step 4 depends on step 2's output |

**Management strategies:**
- **Segmentation**: Break into sub-tasks where each segment can be completed before the next is shown.
- **Prior-knowledge activation**: Surface prerequisite concepts before the main material so they pre-load as chunks.
- **Worked examples**: Replace problem-solving with example-study while schemas are forming (reduces intrinsic load during early learning).

**Rule:** Intrinsic load cannot be eliminated — the task is what it is. It can only be managed by sequencing and scaffolding.

### 2.2 Extraneous Load — unnecessary load from poor presentation

Load that arises from the *way* the information is presented, not from the information itself. This is the only load type that should be aggressively eliminated.

| Source | Example |
|--------|---------|
| Split-attention effect | Having to look at a diagram in one place and its legend somewhere else |
| Redundancy effect | Restating in prose what a table already communicates clearly |
| Coherence violation | Including interesting-but-irrelevant context that the reader must process and then discard |
| Verbose preamble | Three paragraphs explaining what you're about to say before saying it |
| Inconsistent formatting | Different heading levels for the same type of content across sections |
| Missing visual hierarchy | A flat wall of text with no structural cues |

**Elimination tactics:**
- Integrate labels directly into diagrams (remove the need to look between locations).
- Use tables for comparative data (reader chunks the format as a single schema slot).
- Remove decorative prose around already-clear structures.
- Apply consistent formatting so structure itself becomes a chunk the reader can ignore.

### 2.3 Germane Load — load that builds schemas

Cognitive effort spent constructing, organizing, or automating a mental model. This load is *desirable* — it is the mechanism of learning and skill acquisition. The goal is to maximize germane load *within* available capacity (total load ≤ capacity).

| Source | Example |
|--------|---------|
| Worked examples | Step-by-step solutions with explicit reasoning |
| Variability practice | Multiple examples of the same concept in different contexts |
| Self-explanation prompts | "Why does this rule apply here?" nudges the reader to generate their own connections |
| Analogies | Mapping a new concept onto a familiar schema (e.g., "CLT is like RAM management") |
| Contrasting cases | Showing what's wrong alongside what's right |

**Promotion tactics:**
- Include worked examples even when they lengthen the skill body.
- Provide multiple instantiations of abstract rules (varied examples increase schema strength).
- Use analogies that map onto known structures.
- Show failure modes alongside success patterns.

---

## 3. Working Memory Limits

### The ~4-chunk finding

Cowan (2001) revised Miller's 7±2 downward: *the reliable limit of working memory is approximately 4 independent chunks* — not 7. Crucially, what counts as a "chunk" depends on expertise: an expert chess player chunks a board position into one unit; a novice processes each piece separately.

**Implications:**

| Situation | Working-memory implication |
|-----------|---------------------------|
| Novice reader encountering an unfamiliar pattern | Each element is a separate chunk; total capacity exhausted quickly |
| Expert reader encountering a known pattern | The entire pattern is one chunk; more capacity for novel details |
| An agent writing for a mixed audience | Design for the novice's chunking capacity; experts will auto-compress |
| A 10-column dashboard widget | If column meanings are not already chunked, viewer hits capacity before first insight |

### Chunking strategies

1. **Label by type, not by instance**: Instead of 10 separate data points, introduce a category that chunks them (e.g., "fulfillment metrics" as a header that frames the following 5 rows).
2. **Consistent structure as a free chunk**: When every SKILL.md section follows the same format, the reader chunks the format itself — freeing all 4 slots for content.
3. **Pre-load schemas**: Front-load the concept card / summary so the reader builds a lightweight schema before encountering detail.
4. **Segment before elaborating**: Deliver the simplest complete unit first, add complexity in subsequent passes.

---

## 4. Application: Writing Skills

When authoring a `SKILL.md` body, apply the three-load taxonomy to each section before committing.

### Checklist

| Question | If YES → action |
|----------|-----------------|
| Does this section restate what the heading already conveys? | Extraneous redundancy → cut the restatement |
| Is this section longer than the information it communicates? | Extraneous verbosity → compress to table or bullets |
| Does this section require the reader to cross-reference another section to understand it? | Split-attention → integrate or re-sequence |
| Does this section contain a worked example? | Germane → keep it; do not cut for length |
| Does this section use a consistent format with neighboring sections? | If YES: format-as-chunk is working → maintain consistency |
| Is this section building a schema the reader will use in practice? | Germane → expand if needed |

### Anti-patterns in skill bodies

| Anti-pattern | Load type | Fix |
|---|---|---|
| Four-paragraph intro before the actual content | Extraneous (preamble) | Move preamble to Concept Card; open sections with the content |
| "This section covers X. X is important because..." | Extraneous (redundancy) | Remove the meta-commentary; start with X |
| Removing the worked example to save tokens | Germane destruction | Keep the example; cut prose around it instead |
| Using different heading levels for equivalent content | Extraneous (inconsistency) | Normalize heading hierarchy |

---

## 5. Application: Designing Prompts

Prompt design is working-memory design for the model. The model's context window is not the same as working memory, but the principles transfer: a prompt that requires holding many interdependent instructions simultaneously creates functional equivalents of high cognitive load.

### High-intrinsic-load prompt signals

| Signal | Why it's high load |
|--------|-------------------|
| Multiple tasks stated in one prompt without sequencing | Model must track all tasks simultaneously |
| Later instructions that modify earlier ones | Model must retroactively reinterpret prior context |
| Abstract instructions with no examples | Model must construct the intent without schema |
| Long preamble before the actual instruction | Model must retain preamble while processing what follows |

### CLT-informed prompt design

| Strategy | What it does |
|----------|--------------|
| **Segment high-intrinsic tasks** | Split into sequential prompts; each builds on the prior output |
| **Example-first for novel formats** | Show the output format before describing it abstractly |
| **Front-load the primary task** | State what you want in sentence 1; justification follows |
| **Consistent instruction schema** | Reuse the same structure across related prompts so the format becomes a chunk |
| **One constraint per instruction** | Avoid compound constraints ("do X but not Y, unless Z") |

### Example: refactoring a high-load prompt

**Before (high extraneous load):**
```
I need you to look at this audit output from our skill review system and think about which findings are the most important ones and then also consider whether any of them might actually be incorrect given the context of how skills work in our system, and then write a summary that could be used in a Linear comment explaining what needs to be done.
```

**After (segmented, reduced extraneous load):**
```
Step 1: Classify each finding below as VALID or INVALID. A finding is invalid if it misunderstands how our skill schema works.

[findings]

Step 2: Of the VALID findings, rank by severity: BLOCKING, ADVISORY, NITPICK.

Step 3: Write a Linear comment summarizing the BLOCKING findings and their required fixes.
```

The second version segments intrinsic load, removes preamble verbosity, and provides a consistent schema for each step.

---

## 6. Application: UI / Dashboards

Per-screen cognitive budget is a CLT concept: a screen imposes load through the number of independent data points, interaction affordances, and visual decisions the viewer must process simultaneously.

### Budget heuristics

| Guideline | Rationale |
|-----------|-----------|
| Max 4-5 independent data points per widget | Matches working-memory chunk limit |
| Group related metrics under a labeled category | The label becomes a single chunk |
| Consistent card structure across the dashboard | Format chunked → all capacity for content |
| Progressive disclosure for detail | Show summary first; reveal detail on demand |
| Avoid same-visual-weight competing CTAs | Multiple salient actions compete for the same chunk slot |

### Common dashboard extraneous-load sources

| Source | Fix |
|--------|-----|
| 12-column table with no grouping | Group by category; hide secondary columns behind expand |
| Redundant title + axis label + legend | Integrate axis label into chart; remove redundant title |
| Color-coded data with no legend visible | Move legend adjacent to chart or encode in tooltip |
| Mixed decimal precision across a single widget | Normalize precision so reader doesn't parse each format separately |
| Status indicators without consistent icon meaning | Define a fixed icon vocabulary (same icon = same meaning everywhere) |

---

## 7. Worked Example: Reducing Extraneous Load in Audit Output

**Before (high extraneous load):**
```
Audit Results for skills/my-skill/SKILL.md:

After reviewing the skill carefully I noticed that there are a few things that 
could be improved. The first issue I want to mention is that the description field 
in the frontmatter doesn't actually have the use_when and not_for patterns that 
we require. Also, looking at the relations section, I see that verify_with is 
empty which means the skill has no verification partners. Additionally, the eval 
file has only one eval which is below the minimum we set.

I think these should be fixed but the skill is otherwise in reasonable shape.
```

**After (low extraneous load, structured):**

```
## Audit: skills/my-skill/SKILL.md

| Finding | Severity | Fix |
|---------|----------|-----|
| description missing use_when / not_for pattern | BLOCKING | Add "Use when: ... Do NOT use for: ..." |
| relations.verify_with is empty | ADVISORY | Add at least one verify_with skill |
| evals/evals.json has 1 eval (min: 2) | BLOCKING | Add a second eval case |

Overall: 2 BLOCKING. Fix before marking PASS.
```

**What changed:**
- Removed verbal preamble ("After reviewing the skill carefully I noticed...")
- Replaced prose with a table — each finding is now one chunk
- Made severity and fix explicit rather than embedded in prose
- Removed hedging ("I think", "otherwise in reasonable shape") — extraneous load with no information content

---

## 8. Common Failure Modes

| Failure mode | Load consequence | Detection signal |
|---|---|---|
| "Simplify" interpreted as "make shorter" | Cuts germane content (worked examples, analogies) | The reader now has less schema, more confusion |
| Removing context to reduce word count | Increases intrinsic load (reader must infer what was removed) | Reader asks follow-up questions that context would have answered |
| Adding beautiful prose to describe what a table already shows | Extraneous redundancy | Section length ≠ information density |
| Designing a prompt in one large block | High intrinsic load; model can't segment | Model produces mixed output or drops constraints |
| Consistent formatting abandoned mid-document | Format chunk broken; reader spends capacity re-orienting | Mixed heading levels, inconsistent table structures |
| Equating "expert content" with "high cognitive load" | False: experts chunk more; appropriate material for audience reduces load | Ask: who is the reader? What do they already chunk? |

---

## 9. Rating Criteria

Rate any output (skill body, prompt, doc section, dashboard widget) against CLT:

| Score | Criterion |
|-------|-----------|
| **5** | Extraneous load eliminated. Germane load preserved or promoted. Structure is consistent and chunks the format. Worked examples present where schema-formation is the goal. Intrinsic load segmented where it exceeds single-pass capacity. |
| **4** | Extraneous load mostly eliminated. Minor redundancy remains but does not impede comprehension. Germane content intact. |
| **3** | Some extraneous elements (preamble, redundant prose) present but not dominant. Germane content mostly intact. Structure inconsistent in places. |
| **2** | Significant extraneous load (verbose intro, split-attention, redundancy). Some germane content removed. Reader must do significant work to find substance. |
| **1** | Dominant extraneous load (wall of text, no structure, redundancy throughout). Germane content absent or destroyed. Reader cannot reliably extract the core information. |

---

## Health Block

| Field | Value |
|-------|-------|
| structural_verdict | UNVERIFIED |
| truth_verdict | UNVERIFIED |
| comprehension_verdict | UNVERIFIED |
| application_verdict | UNVERIFIED |
| last_audited | 2026-05-19 |
| eval_failed_ids | [] |
| drift_status | UNKNOWN |
| freshness | 2026-05-19 |

The four-verdict shape is per [ADR 0011](../../../../skill-graph/docs/adr/0011-split-audit-verdict-into-four-verdicts.md). All four verdicts default to `UNVERIFIED` on a fresh port; gates 1–8 and the application-eval pilot populate them in subsequent audits.

---

## Do NOT Use When

| Instead of this skill | Use | Why |
|---|---|---|
| `cognitive-load-theory` | `context-management` | `context-management` owns retrieval and session working-set design |
| `cognitive-load-theory` | `prompt-craft` | `prompt-craft` owns the full prompt engineering tactic set |
| `cognitive-load-theory` | `teaching-patterns` | `teaching-patterns` owns explanation and pedagogy methods |
| `cognitive-load-theory` | `compression` | `compression` owns token-efficiency strategies for context windows |

---
