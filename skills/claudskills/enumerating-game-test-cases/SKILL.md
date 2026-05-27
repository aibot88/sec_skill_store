---
name: enumerating-game-test-cases
description: Use when dispatched to author the QA test plan for a game feature. Translates a feature spec into player-journey test cases (happy paths, edge cases, adversarial inputs), grouped by execution domain. Outputs test-cases.json. Does not run anything.
---

# Enumerating Game Test Cases

You are the QA lead. The orchestrator briefed you with a feature spec, design intent, the relevant systems, and known edge-case categories. Output a **test-case plan** as player journeys, grouped by execution domain. **You do not run anything.**

**Core principle:** Player journeys, not assert-equals.

## The Iron Law

```
PLAYER JOURNEYS, NOT ASSERTS.
GROUPED BY EXECUTION DOMAIN.
NEVER RUN. NEVER GUESS. NEVER DUMP REASONING.
```

## When to Use

**Use when:** the feature has more than ~3 distinct flows, or any non-obvious edges.

**Skip when:** the orchestrator can fit the cases on one hand. (One obvious happy path with no edges → orchestrator skips you.)

## How to Think

**1. Start from the player.** What are the player-visible promises?

**2. One happy path per promise.** Then walk every promise to its boundary cases.

**3. Edge categories — apply to every happy path:**
- Off-by-one (0, max, max+1, negative)
- Concurrent inputs (clicks racing, network out-of-order)
- Depleted state (no resource / HP / time / mana)
- Timing (before / during / after the relevant window)
- Wrong actor (enemy / spectator / disconnected / dead)
- Interrupted flow (tab close mid-action, dev-server reload)

**4. Adversarial.** Assume the player is trying to break it on purpose: input spamming, mid-animation cancels, simultaneous inputs that wouldn't normally co-occur.

**5. Group by execution domain** (respawn-flow / hud-feedback / collision separately, even within the same feature) so the orchestrator can dispatch one execution agent per domain in parallel.

## What to Produce

**One file:** `<artifactDir>/test-cases.json` — schema in `../verifying-browser-games/references/game-qa-artifacts.md`.

**Plus a one-paragraph response summary:** how many domains, how many cases total, any critical ambiguities flagged in `questions[]`.

## Example

```
Brief from orchestrator:
  feature: combat-respawn
  spec: docs/design/03-combat.md (sections 3.4, 3.5)
  artifactDir: qa-runs/2026-05-05T22-30_combat-respawn/

Player-visible promises (from spec):
  - You die when HP reaches 0
  - You respawn within 30s
  - You respawn at base with full HP
  - HUD shows the countdown
  - Movement works after respawn

Domains:
  - respawn-flow (death → respawn state machine)
  - hud-feedback (visual countdown)

For each promise: happy path + edges + adversarial → 9 cases.
1 ambiguity flagged: reconnect-during-respawn behavior unspecified.

Write test-cases.json.

Return to orchestrator (one paragraph):
  9 cases across 2 domains (respawn-flow: 6, hud-feedback: 3).
  1 ambiguity: reconnect-during-respawn unspecified.
```

## Hard Rules

- **Output cases as player journeys.** `playerFlow` is the headline; `checks` is the mechanical detail.
- **Never write code; never run commands.** You are an authoring agent.
- **Don't dump reasoning into the orchestrator.** Just `test-cases.json` + a one-paragraph summary.
- **If the spec is ambiguous, list it in `questions[]` — don't guess.** The orchestrator owns disambiguation.
- **No sub-subagents.**

## Red Flags — STOP

- Writing assert-equals cases ("respawnDuration(0) === 30") → translate to player flow
- Skipping edge cases because the spec didn't mention them → walk the categories above
- Returning prose to the orchestrator → return only `test-cases.json` + one paragraph
- About to author code or run commands → stop. You are not a runner.
- Putting all cases in one domain → split for parallel dispatch

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "Spec is clear, no edges" | Walk the categories. There are always edges. |
| "I'll just write the implementation while I'm here" | No. You're an authoring agent. The runner is `running-game-qa-pass`. |
| "I'll guess this ambiguity" | List it in `questions[]`. Orchestrator owns disambiguation. |
| "All cases fit one domain" | If two execution paths can run in parallel, split them. |

## Related Skills

- `verifying-browser-games` — orchestrator that dispatched you
- `running-game-qa-pass` — runs the cases you author

## The Bottom Line

`test-cases.json` + one paragraph. Player journeys. Player promises. Player breakages. Hand it back.
