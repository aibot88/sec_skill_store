---
name: aoa-source-of-truth-check
description: Clarify which files are authoritative for repository guidance, operational instructions, architecture, and status, and keep entrypoint docs short and link-driven once canonical homes exist. Use when docs overlap, conflict, or confuse contributors about which file to trust. Do not use for purely code-local tasks or when authoritative files are already clear and the main need is decision rationale.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: core
  aoa_status: canonical
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/aoa-source-of-truth-check/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0013,AOA-T-0002,AOA-T-0009
  aoa_portable_profile: codex-facing-wave-3
---

# aoa-source-of-truth-check

## Intent
Use this skill to clarify which files are authoritative for status, architecture, run instructions, policy, and change guidance.

## Trigger boundary
Use this skill when:
- a repository has several docs that may overlap or conflict
- contributors may not know which file to trust first
- a change touches docs, process, or operational guidance and the question is which file is authoritative
- confusion exists between overview docs and authoritative docs
- one authoritative source must stay aligned across multiple downstream consumer surfaces
- top-level status docs such as `README` or `MANIFEST` are accumulating status/history that should live in canonical homes instead
- the repository already has canonical detail surfaces and the summary docs should stay short, navigable, and link-driven

Do not use this skill when:
- the repository is tiny and has no meaningful source-of-truth ambiguity
- the task is purely code-local with no documentation or policy impact
- the authoritative files are already clear and the main need is recording rationale for a decision; use `aoa-adr-write`
- the main problem is deciding whether logic belongs in the core or at the edge; use `aoa-core-logic-boundary` first
- the main problem is broader policy design rather than document authority or ownership
- the task is only about building or maintaining a derived docs surface; that belongs in a separate review-surface workflow

## Inputs
- repository docs surface
- target area of ambiguity or overlap
- known canonical files if any
- current contributor confusion points

## Outputs
- clearer source-of-truth map
- fan-out map when one source feeds multiple downstream consumers
- note of overlaps or conflicts
- proposed or implemented document role clarification
- lightweight snapshot guidance for entrypoint docs when canonical homes already exist
- verification summary

## Procedure
1. identify the main docs or guidance files involved in the target area
2. determine which file should be authoritative for each concern
3. note any overlap, contradiction, or role ambiguity
4. if one source feeds multiple consumers, name each consumer and refresh them from the same source
5. if top-level status docs are bloating, trim them into short snapshots and route detail to canonical homes
6. clarify or propose clarifying document ownership and purpose
7. keep the change bounded to the guidance surface under review
8. verify that the result reduces ambiguity for future changes

## Contracts
- authoritative sources should be visible and named explicitly
- overview documents should not silently replace canonical ones
- lightweight entrypoint docs should link outward instead of duplicating chronology or changing counters
- role separation should reduce confusion, not create extra ceremony
- the resulting guidance should be understandable to another human or agent

## Risks and anti-patterns
- over-formalizing a tiny docs surface
- creating many labels without reducing ambiguity
- moving truth across files without clearly signaling the change
- letting summaries masquerade as canonical instructions
- trimming top-level docs too aggressively before canonical homes are actually available
- widening the skill into generic docs hygiene or derived surface maintenance

## Verification
- confirm the main source-of-truth ambiguity was reduced
- confirm authoritative files are named explicitly
- confirm overlaps or conflicts were surfaced rather than hidden
- confirm summary docs stay short and route detail to canonical homes where those already exist
- confirm the result helps future contributors orient faster

## Technique traceability
Manifest-backed techniques:
- AOA-T-0013 from `8Dionysus/aoa-techniques` at `5c6f0496edc3c2e74590baa35627c85fe58ef765` using path `techniques/docs/single-source-rule-distribution/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `5c6f0496edc3c2e74590baa35627c85fe58ef765` using path `techniques/docs/source-of-truth-layout/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0009 from `8Dionysus/aoa-techniques` at `5c6f0496edc3c2e74590baa35627c85fe58ef765` using path `techniques/docs/lightweight-status-snapshot/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points
Future project overlays may add:
- local doc hierarchies
- mixed ADR, architecture, and operations doc maps that split authority by concern
- preferred canonical-file patterns
- local review rules for doc changes
- repository-specific examples of authoritative surfaces
- lightweight snapshot rules for README or MANIFEST surfaces
- rules for keeping entrypoint docs short once deeper canonical homes already exist
