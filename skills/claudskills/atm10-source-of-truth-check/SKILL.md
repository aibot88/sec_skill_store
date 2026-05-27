---
name: atm10-source-of-truth-check
description: Apply the aoa-source-of-truth-check workflow inside an atm10-* repository using repo-relative document maps, canonical-file patterns, and local review posture. Use when contributors need a thin project overlay to identify authoritative docs inside an atm10-* repo. Do not use when the task is broader policy design, purely code-local, or better handled by the base skill without local adaptation.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: project
  aoa_status: evaluated
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/atm10-source-of-truth-check/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0013,AOA-T-0002
  aoa_portable_profile: codex-facing-wave-3
---

# atm10-source-of-truth-check

## Intent
Use this skill to adapt `aoa-source-of-truth-check` to an `atm10-*` repository when the base workflow is right but the local doc map needs repo-relative detail.

## Trigger boundary
Use this skill when:
- the base `aoa-source-of-truth-check` workflow is already correct, but an `atm10-*` repo needs local canonical-file patterns, repo-relative docs, or doc review rules
- contributors need a thin overlay that maps repo-relative docs such as `README.md`, `docs/ARCHITECTURE.md`, or `docs/[canonical-guide].md`
- confusion exists between overview docs and authoritative files inside one local repo
- the family review doc and bundle-local checklist still need to stay aligned

Do not use this skill when:
- the main need is broader policy design rather than local document authority mapping
- the task is purely code-local and has no meaningful docs or guidance ambiguity
- the work would introduce new upstream technique meaning instead of thin local adaptation
- the main need is recording rationale for a decision rather than clarifying authority; use `aoa-adr-write`

## Inputs
- repo-relative docs or guidance surfaces
- local canonical-file candidates
- local review rules for doc changes
- contributor confusion points
- base skill reference

## Outputs
- local source-of-truth map
- bounded clarification note
- repo-relative canonical-file pattern
- pointer to the family review surface
- verification summary for the local docs surface

## Procedure
1. start from `aoa-source-of-truth-check` instead of inventing a family-specific docs doctrine
2. name the repo-relative docs and guidance files involved in the ambiguity
3. map which file should stay authoritative for each local concern
4. keep the adaptation bounded to the local repo surface under review
5. make explicit what still depends on downstream human review or unpublished local policy

## Contracts
- preserve the base skill meaning
- keep local file maps repo-relative and explicit
- surface local authority and review posture without hiding it
- keep the overlay public-safe and reviewable

## Risks and anti-patterns
- inventing a broader docs governance framework inside a thin overlay
- using family labels without reducing local ambiguity
- hiding local review rules in prose that looks canonical
- silently replacing the base skill with project doctrine

## Verification
- confirm the base skill is still the right workflow
- confirm authoritative repo-relative files are named explicitly
- confirm local review posture is visible rather than implied
- confirm the adaptation reduces ambiguity without widening scope
- confirm the family review doc and bundle-local checklist stay aligned

## Technique traceability
Manifest-backed techniques:
- AOA-T-0013 from `8Dionysus/aoa-techniques` at `5c6f0496edc3c2e74590baa35627c85fe58ef765` using path `techniques/docs/single-source-rule-distribution/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `5c6f0496edc3c2e74590baa35627c85fe58ef765` using path `techniques/docs/source-of-truth-layout/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points
- local doc hierarchies
- repo-relative canonical-file patterns
- local review rules for doc changes
- repository-specific authority examples
- family review doc and bundle-local review checklist
