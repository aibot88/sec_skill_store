---
name: cache-warm-before-cache-only-fanout
description: "Warm the authoritative cache path first, then fan out cache-only readers in parallel so derived loaders never race stale state."
metadata:
  author: ychampion
---

# SKILL: Cache Warm Before Cache-Only Fanout
**Domain:** extensions-mcp  
**Trigger:** Apply when one authoritative load populates caches that several cheaper readers depend on, and parallel reads would race the warm path.
**Source Pattern:** Distilled from reviewed extension lifecycle and source-reconciliation patterns.

## Core Method
Run the expensive authoritative loader first, let it materialize and warm the shared caches, and only then fan out cache-only readers in parallel. This preserves a single source of truth for cache population while still recovering parallelism for the cheap derived reads. The result is deterministic: every downstream reader sees the same fresh state without each one redoing install or clone work.

## Key Rules
- Identify which loader actually populates the canonical cache and make it run before any cache-only consumers.
- Keep derived readers cache-only; they should assume the warm path already handled the expensive side effects.
- Use parallel fanout only after the warm step resolves successfully.
- Document why the ordering matters so later refactors do not collapse everything back into a premature `Promise.all`.
- Let the warm path own cache population and reuse; do not make each consumer silently fall back to heavyweight work.

## Example Application
If an extension refresh must first scan and clone any missing plugins before separate readers build the command list and agent list, await the full plugin load once, then run command extraction and agent extraction in parallel against the warmed cache.

## Anti-Patterns (What NOT to do)
- Do not launch cache-only readers in parallel with the warm path if they can read stale manifests or miss newly materialized content.
- Do not duplicate heavy install logic in each derived loader just to hide ordering bugs.
- Do not remove the sequencing comment when the dependency is subtle; future maintainers will reintroduce the race.
