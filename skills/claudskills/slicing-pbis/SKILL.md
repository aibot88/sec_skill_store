---
name: slicing-pbis
description: "Slices, reviews, and writes product backlog items (PBIs) using priority-ordered quality characteristics (Valuable > Completable > Negotiable > Independent > Commensurate > Small), vertical slicing, and the splitting meta-pattern. Produces well-formed, commensurately sized PBIs with binary acceptance criteria. Use when splitting large PBIs or user stories, reviewing backlog items for quality, writing new PBIs from requirements, refining a product backlog, decomposing epics into stories, or when the user mentions PBI slicing, story splitting, backlog refinement, or vertical slices."
category: Software Engineering
---

# Slicing Product Backlog Items

## Determine the task

| Task | Workflow |
|---|---|
| **Splitting a large PBI** into smaller ones | → [Splitting workflow](#workflow-splitting-a-pbi) |
| **Reviewing existing PBIs** for quality | → [Review workflow](#workflow-reviewing-pbis) |
| **Writing new PBIs** from requirements | → [Writing workflow](#workflow-writing-new-pbis) |

## Quality characteristics (priority order)

Apply these in order — when they conflict, higher-ranked characteristics take precedence.

| # | Characteristic | Test |
|---|---|---|
| 1 | **Valuable** | Can a stakeholder observe the value this delivers? |
| 2 | **Completable** | Is there a binary pass/fail condition for "done"? |
| 3 | **Negotiable** | Is the implementation approach open for the team to adjust? |
| 4 | **Independent** | Can this PBI be released without waiting for another? |
| 5 | **Commensurate** | Is this PBI roughly the same size as the others in the backlog? |
| 6 | **Small** | Can this be completed within a single sprint? |

When characteristics conflict: prefer value over smallness, independence over smallness, completability over negotiability. Stop splitting when further division would break a higher-ranked characteristic.

## The splitting meta-pattern

All splitting techniques follow one pattern:

1. **Find the core complexity.** What part is most likely to surprise the team? (Human preferences, external integrations, variable business rules.)
2. **Identify the variations.** What are there many of? (User roles, business rules, data formats, workflow paths, edge cases, platforms.)
3. **Reduce all variations to one.** Find a single, complete path through the complex part → this is the first slice. Each subsequent slice reintroduces one variation.

This produces vertical slices by default — reducing to a single variation through the core complexity naturally cuts across all system layers.

## Splitting patterns (quick reference)

Pick based on the dominant source of variation:

| Pattern | When to use | First slice delivers |
|---|---|---|
| Workflow steps | Multi-step process | Beginning and end steps (most value and risk) |
| Business rules | Behavior branches on conditions | Most common or highest-value rule |
| Data variations | Multiple data types or formats | Highest-traffic variation |
| User role | Different user groups, different needs | Highest-value role |
| Interface/platform | Multiple platforms | Highest-traffic interface |
| Happy path / edge cases | Complex error handling | Happy path only |
| CRUD operations | Full lifecycle management | Read or create (whichever unlocks more) |
| Major / minor effort | One large core + incremental add-ons | The major integration effort |
| Spike / implementation | Uncertainty is the blocker | Time-boxed spike (research, not code) |

For detailed examples of each pattern, see [references/02-hierarchy-and-slicing.md](references/02-hierarchy-and-slicing.md).

## Workflow: Splitting a PBI

1. Run the "Should this PBI be split?" checklist (Checklist B in [references/03-sizing-dependencies-antipatterns.md](references/03-sizing-dependencies-antipatterns.md)) to confirm splitting is needed.
2. Apply the meta-pattern: find core complexity → identify variations → reduce to one.
3. Choose the splitting pattern matching the dominant variation type.
4. For each resulting slice, validate against the quality characteristics table above.
5. Verify each slice is vertically sliced — it cuts through all necessary system layers, not just one.
6. Write 1–3 binary, behavior-focused acceptance criteria per slice.
7. Check: the first slice carries the most value and risk. Low-value slices are clearly deprioritizable.
8. If any slice fails validation at steps 4–6, re-split it by returning to step 2.

**Guard rails:**
- Every slice must deliver observable stakeholder value. A slice that looks like a developer task fails.
- A PBI should represent ≤ 1/5 to 1/10 of sprint capacity.
- 4+ acceptance criteria on a single slice means split further.
- The first slice is the thinnest possible end-to-end happy path — do not gold-plate it.

## Workflow: Reviewing PBIs

1. For each PBI, run the well-formedness checklist (Checklist A in [references/03-sizing-dependencies-antipatterns.md](references/03-sizing-dependencies-antipatterns.md)).
2. Run the splitting checklist (Checklist B) to identify split candidates.
3. Check for common anti-patterns — see [Anti-Patterns in references/03-sizing-dependencies-antipatterns.md](references/03-sizing-dependencies-antipatterns.md).
4. For PBIs approaching sprint readiness, run the sprint-readiness checklist (Checklist C).
5. For each issue found, propose a specific fix with a rewritten PBI.

**Common anti-patterns to flag:** horizontal slicing, tasks disguised as stories, over-splitting, premature splitting, gold-plating the first slice, confusing epics with categories.

## Workflow: Writing new PBIs

1. Start from the stakeholder problem — not the solution.
2. Write the PBI description covering: **Problem**, **Proposed Solution**, **Expected Impact**, and **Acceptance Criteria**. Add **Timelines** and **Dependencies** only when applicable.
   For description format details, see [references/01-quality-and-description.md](references/01-quality-and-description.md).
3. Slice vertically — every PBI cuts through all system layers needed to deliver one complete scenario.
4. Write 1–3 binary, independently verifiable, behavior-focused acceptance criteria per PBI.
5. Validate each PBI against the quality characteristics table above.
6. If the PBI is too large (fails Commensurate or Small), apply the splitting workflow above.

**Acceptance criteria rules:**
- Binary pass/fail. No partial credit.
- Independently verifiable. Each criterion stands alone.
- Behavior-focused. Describe what the system does, not how it is built.
- 1–3 per PBI. More than 3 signals the PBI should be split.

## Edge cases

- **Technical work without direct stakeholder value** (e.g., infrastructure migration): Write as a task with clear problem/solution/impact. Do not force it into a user-story format. It may belong as a sub-item under a value-delivering PBI.
- **Unavoidable dependencies:** Make them explicit. Prefer eliminating by restructuring > merging > decoupling with interfaces > stubbing > sequencing explicitly. See [references/03-sizing-dependencies-antipatterns.md](references/03-sizing-dependencies-antipatterns.md).
- **High uncertainty:** Split into a time-boxed spike (research) + subsequent implementation item. The spike produces knowledge, not production code.
- **Epics:** Use for outcome-oriented grouping with a clear completion condition. Not permanent categories. "Reduce page load time below 2s" is an epic; "Performance" is a label.

## Reference material

- **Quality characteristics and description format**: [references/01-quality-and-description.md](references/01-quality-and-description.md) — the six characteristics in detail, conflict resolution, acceptance criteria guidance, three amigos
- **Hierarchy, vertical slicing, and splitting techniques**: [references/02-hierarchy-and-slicing.md](references/02-hierarchy-and-slicing.md) — epic/work-item/sub-item hierarchy, vertical vs. horizontal slicing, all splitting patterns with examples
- **Sizing, dependencies, anti-patterns, and checklists**: [references/03-sizing-dependencies-antipatterns.md](references/03-sizing-dependencies-antipatterns.md) — commensurate sizing, throughput forecasting, dependency strategies, seven anti-patterns, three refinement checklists
