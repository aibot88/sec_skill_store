---
name: titan-recall
description: Retrieve Titan candidate memory records with source, record id, authority note, confidence, and verification path. Use when a Titan service-cohort route needs this explicit bounded step. Do not use for hidden background agents, silent mutation, unreviewed proof sovereignty, or memory canonization without owner confirmation.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: project
  aoa_status: scaffold
  aoa_invocation_mode: explicit-only
  aoa_source_skill_path: skills/titan-recall/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-PENDING-TITAN-GATE-DISCIPLINE,AOA-T-PENDING-TITAN-RECEIPT-LINEAGE
  aoa_portable_profile: codex-facing-wave-3
---

# titan-recall

## Intent
Use this skill to retrieve and present Titan remembrance records without treating recall as source truth.

## Trigger boundary
Use this skill when:
- a user asks what a Titan remembers
- a session needs bearer memory candidates
- Mneme needs recall with source refs and confidence

Do not use this skill when:
- recall would replace owner-repo evidence
- records lack source refs
- confidence or authority notes cannot be shown

## Inputs
- query text
- bearer id or Titan name
- memory index path
- time or session filter
- verification target

## Outputs
- matching remembrance records
- record ids and source refs
- authority warning
- confidence notes
- verification path

## Procedure
1. search the candidate memory index
2. filter by bearer or session when provided
3. return source-backed matches only
4. include confidence and authority limits
5. point to owner verification when needed

## Contracts
- The skill is explicit-only and must not be invoked as hidden background behavior.
- Titan receipts, bridge ledgers, console state, and memory records are witnesses, not final owner truth.
- Forge mutation and Delta judgment gates must remain distinct and visible.
- Owner-repo validation and human judgment remain stronger than the local skill output.

## Risks and anti-patterns
- treating Titan vocabulary as permission to widen authority
- letting receipt or replay state replace owner-repo evidence
- auto-approving Forge or Delta because a plan looks plausible
- canonizing candidate memory without source-owned confirmation

## Verification
- confirm the request and outputs stayed inside the declared Titan lane
- confirm any mutation or judgment gate was explicit and recorded
- confirm source refs, receipt refs, or ledger refs are preserved when available
- confirm the result names stop lines and remaining owner validation needs

## Technique traceability
Pending Titan workflow techniques:
- AOA-T-PENDING-TITAN-GATE-DISCIPLINE
- AOA-T-PENDING-TITAN-RECEIPT-LINEAGE

## Adaptation points
- Replace pending technique refs with published aoa-techniques refs after the Titan workflow techniques are promoted.
- Keep repo-local command examples in owner docs or examples rather than hard-coding them into the skill law.
- If a Titan surface graduates from scaffold to reviewed, add review evidence before changing status.
