---
name: aoa-invariant-coverage-audit
description: Audit whether existing tests and checks actually constrain the stable invariants that matter. Use when you need to judge if current coverage proves a rule or only repeats examples, and you want the smallest bounded follow-up gaps. Do not use when the invariant itself is still undefined or when the real task is to author new invariants rather than audit coverage.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: core
  aoa_status: canonical
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/aoa-invariant-coverage-audit/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0017
  aoa_portable_profile: codex-facing-wave-3
---

# aoa-invariant-coverage-audit

## Intent
Use invariant-oriented coverage to judge whether an existing validation surface really constrains the stable truth, and turn that judgment into a bounded audit package instead of a loose example review.

## Trigger boundary
Use this skill when:
- an existing test or check surface needs a review for invariant strength
- the question is whether current checks really constrain the stable rule
- you need to turn a loose example set into a bounded coverage audit
- you want an audit result that names the gap, not just the invariant

Do not use this skill when:
- the main problem is defining the invariant itself rather than auditing coverage; use `aoa-property-invariants` first
- the invariant itself is still unknown and you need discovery work first
- the task is mostly about presentation details or a narrow snapshot
- you need a full boundary contract review rather than a coverage audit

## Inputs
- target rule or stable truth
- current tests, checks, or examples
- known edge cases and stress cases
- the input space or states that matter most

## Outputs
- invariant coverage map
- gap list for weak or missing checks
- bounded follow-up checks or revisions
- concise verification summary
- audit verdict on whether coverage is strong enough for the current stable truth

## Procedure
1. name the stable truth in plain language
2. map each existing check to the invariant it constrains
3. mark weak, redundant, or missing coverage
4. add only bounded cases that strengthen the weakest invariant first
5. separate the audit result from any invariant-authoring work that should happen elsewhere
6. report what the suite now proves and what it still does not

## Contracts
- every claimed invariant must be traceable to at least one check
- the audit should distinguish real constraint from mere example repetition
- the result should stay reviewable without sprawling into a full test strategy
- the skill should stay an audit package rather than a general testing doctrine
- the output should make the next coverage move obvious

## Risks and anti-patterns
- counting examples as if they were invariants
- letting random data hide thin coverage
- widening into generic test design or full suite architecture
- making the audit so abstract that no one can act on it
- drifting into invariant authoring when the task is really coverage review
- turning the audit into a generic quality sermon instead of a bounded package

## Verification
- confirm each core invariant is named and mapped to a check
- confirm the coverage gap list is specific and bounded
- confirm another human can follow why the existing surface is or is not sufficient
- confirm the result names the next bounded follow-up, if one is needed
- confirm the skill reads like an operational audit rather than a plain technique lift

## Technique traceability
Manifest-backed techniques:
- AOA-T-0017 from `8Dionysus/aoa-techniques` at `5c6f0496edc3c2e74590baa35627c85fe58ef765` using path `techniques/evaluation/property-invariants/TECHNIQUE.md` and sections: Intent, When to use, When not to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points
Project overlays should add:
- local test or check commands
- domain-specific invariants and edge cases
- notes on where coverage gaps are recorded
- rules for when a coverage audit should escalate into a deeper review
