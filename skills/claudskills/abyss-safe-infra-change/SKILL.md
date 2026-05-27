---
name: abyss-safe-infra-change
description: Apply the aoa-safe-infra-change workflow inside an abyss-* repository using repo-relative operational surfaces, explicit local authority notes, rollback posture, and local validation commands. Use when the base infra-change workflow is correct but a thin project overlay is needed for one abyss repo. Do not use when the base skill is sufficient without local adaptation or when the task is really about producing a shareable artifact.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: project
  aoa_status: evaluated
  aoa_invocation_mode: explicit-only
  aoa_source_skill_path: skills/abyss-safe-infra-change/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0028,AOA-T-0001
  aoa_portable_profile: codex-facing-wave-3
---

# abyss-safe-infra-change

## Intent
Use this skill to adapt `aoa-safe-infra-change` to an `abyss-*` repository when the base operational workflow is correct but the local repo still needs repo-relative commands, authority notes, and risk framing.

## Trigger boundary
Use this skill when:
- the base `aoa-safe-infra-change` workflow is already correct, but an `abyss-*` repo needs repo-relative operational surfaces, commands, or approval notes
- the task is a bounded infrastructure, service, configuration, or operational change inside one local repo family
- explicit local authority, rollback posture, or verification commands still need to be named before execution
- the family review doc and bundle-local checklist still need to stay aligned

Do not use this skill when:
- the task is really about producing a shareable public-safe artifact rather than the operational change itself; use `abyss-sanitized-share`
- no `abyss-*` repo adaptation is needed and the base `aoa-safe-infra-change` skill is sufficient
- the overlay would only restate the base workflow without adding a real local surface
- the main question is whether authority exists at all; use `aoa-approval-gate-check`
- the main need is to prefer or interpret a preview path before execution; use `aoa-dry-run-first`
- the work would widen into broader project doctrine instead of a thin local overlay

## Inputs
- target operational change and touched local surface
- repo-relative operational files or commands
- explicit local authority or approval posture
- validation and rollback path
- base skill reference

## Outputs
- bounded local infra-change plan
- repo-relative command or path sketch
- explicit local authority and rollback note
- pointer to the family review surface
- concise verification note for the local repo surface

## Procedure
1. start from `aoa-safe-infra-change` instead of inventing a new project-family workflow
2. name the repo-relative operational files, commands, and authority posture that matter locally
3. keep the adaptation bounded to the local repo surface under change
4. preserve the base risk framing, rollback thinking, and explicit verification posture
5. make explicit what still requires downstream human approval or repo-specific judgment

## Contracts
- preserve the base skill meaning
- keep paths and commands repo-relative
- keep local authority explicit
- keep the overlay explicit-only, public-safe, and reviewable

## Risks and anti-patterns
- hiding downstream authority inside vague local operational notes
- turning a thin overlay into project doctrine or a scenario bundle
- naming repo-relative commands without enough verification or rollback context
- silently changing the base workflow instead of adapting the local repo surface

## Verification
- confirm the base skill is still the correct workflow
- confirm repo-relative paths and commands are named explicitly
- confirm local authority, rollback posture, and verification remain explicit
- confirm the adaptation stays bounded to the local repo surface
- confirm the family review doc and bundle-local checklist stay aligned

## Technique traceability
Manifest-backed techniques:
- AOA-T-0028 from `8Dionysus/aoa-techniques` at `5c6f0496edc3c2e74590baa35627c85fe58ef765` using path `techniques/agent-workflows/confirmation-gated-mutating-action/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0001 from `8Dionysus/aoa-techniques` at `5c6f0496edc3c2e74590baa35627c85fe58ef765` using path `techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md` and sections: Intent, Outputs, Contracts, Risks, Validation

## Adaptation points
- repo-relative operational surfaces
- local authority and approval notes
- local validation commands
- rollback or recovery expectations
- family review doc and bundle-local review checklist
