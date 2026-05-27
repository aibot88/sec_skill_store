---
name: titan-memory-loom
description: Initialize or update Titan Memory Loom records as candidate memory with source refs, confidence, and authority warnings. Use when a Titan service-cohort route needs this explicit bounded step. Do not use for hidden background agents, silent mutation, unreviewed proof sovereignty, or memory canonization without owner confirmation.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: project
  aoa_status: scaffold
  aoa_invocation_mode: explicit-only
  aoa_source_skill_path: skills/titan-memory-loom/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-PENDING-TITAN-GATE-DISCIPLINE,AOA-T-PENDING-TITAN-RECEIPT-LINEAGE
  aoa_portable_profile: codex-facing-wave-3
---

# titan-memory-loom

## Intent
Use this skill to ingest Titan receipts or events into candidate-grade remembrance records.

## Trigger boundary
Use this skill when:
- a Titan receipt or event should become recallable later
- cross-session digest needs candidate memory entries
- Mneme needs provenance-preserving memory posture

Do not use this skill when:
- memory would be canonized without owner confirmation
- the input lacks source refs
- redaction or retention policy has not been considered for sensitive material

## Inputs
- receipt or event source
- bearer id or Titan name
- source refs
- confidence note
- redaction or retention hints

## Outputs
- candidate remembrance record
- recall authority warning
- source and confidence fields
- redaction or tombstone candidates
- digest note

## Procedure
1. identify the source receipt or event
2. extract candidate memory facts
3. preserve bearer and session identity
4. attach source refs and confidence
5. return recall limits and any redaction needs

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
