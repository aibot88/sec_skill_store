---
name: triaging-board
description: |
  Use when the user wants to investigate blocked cards, release stale claim
  branches, or triage the board for stuck or abandoned work.
  Triggers on: "what's blocked", "triage the board", "release stale claims",
  "check blockers", "stale claims", "blocked cards", "who's stuck",
  "abandoned work", "ghost claims". Use even when the user phrases it
  casually ("anything stuck?", "any ghost branches?") — the signal of wanting
  to investigate stuck or stale work is what matters.
  Do NOT use when the user wants to see overall board state (that's
  briefing-daily), bring in new work (intaking-requirement), or review open
  PRs for contract compliance (reviewing-pr-queue).
when_to_use: |
  Trigger on: "what's blocked", "triage the board", "release stale claims",
  "blocked cards", "stale claims", "check blockers", "ghost branches",
  "who's stuck", "abandoned work". Apply when the Producer wants to process
  the Blocked queue or release stale claim branches.
---

# triaging-board

This is the Producer's triage routine. It scans Blocked cards (3-class
blocker remediation) and stale claim branches (>72h flag; >7 days release
recommendation), then recommends or takes unblocking actions.

**Required sub-skills**:
- `board-superpowers:board-canon` — state machine; Blocked status semantics;
  WIP counting.
- `board-superpowers:operating-kanban` — dispatch the `read_board` protocol
  action (with status filter `Blocked`), `release_claim` for stale-claim
  cancellation, and `transition_card` for Blocked → In Progress unblock;
  resolves the active projection from settings.
- `board-superpowers:composing-siblings` — consult before any sibling-plugin
  handoff (rare in triage; included per mandatory declaration).
- `board-superpowers:classifying-actions` + `board-superpowers:auditing-actions`
  — applied at every mutating action in this routine.

## Overview

The triage routine answers two questions:

1. **What is blocked and why?** — for each Blocked card, classify the blocker
   (external-dependency / decision-pending / stale-block) and recommend an
   action.
2. **What is stale?** — for each claim branch older than 72h with no progress,
   flag or recommend release.

This routine does NOT resolve blockers itself (except stale-block, which is a
simple Status flip). Architecture decisions go back to intake; external
dependencies get surfaced to the Producer for status check.

The triage routine is the board's health check: it surfaces problems and
recommends remediation paths, but the Producer makes the actual decisions.
No card transition or branch delete happens without explicit approval.

## Step 1 — Scan Blocked cards

Invoke `board-superpowers:board-canon` to load the Blocked status semantics.
Then invoke `board-superpowers:operating-kanban` with action `read_board` and
status filter `Blocked`. This returns only Blocked cards.

For each Blocked card:

1. Read the card body. Find the blocker (per `board-superpowers:board-canon`
   § state machine, Blocked entries name their blocker in a card comment or
   in the card body Notes section).

2. Classify the blocker per the 3-class schema:
   - **External-dependency** (waiting on another team / service / vendor /
     external PR): Keep blocked. Surface to the Producer for a status check
     or escalation decision.
   - **Decision-pending** (architect needs to decide something before the
     Consumer can continue): Surface to the Producer for an explicit decision.
     If the decision maps to a fresh requirement, route to
     `board-superpowers:intaking-requirement`.
   - **Stale-block** (the blocker resolved long ago but the card was never
     moved back): Unblock. Propose the transition Blocked → In Progress and
     wait for Producer acknowledgement.

3. Report the classification and recommended action.

See `references/triage-detail.md` for blocker detection mechanics and
the stale-block evidence criteria.

## Step 2 — Scan stale claim branches

List all `claim/N-...` branches on origin:

```bash
git branch -r --list 'origin/claim/*'
```

For each branch, compute age and progress:

```bash
# Age since first commit (or branch creation):
git log origin/<branch> --not main --format="%cr" | tail -1

# Progress: count commits beyond the initial claim marker:
git log origin/<branch> --not main --oneline | wc -l
```

Interpretation:
- Count = 0 or 1 (empty claim or initial marker only): branch is stale.
- Age > 72h AND count ≤ 1: **flag** with warning.
- Age > 7 days AND count ≤ 1 AND the original Consumer was previously
  notified: **recommend release**.

Surface the flagged list to the Producer.

## Step 3 — Recommended actions

For each item in the triage output:

| Classification | Recommended action |
|----------------|--------------------|
| External-dependency | "Surface to the Producer for status check. No card transition needed unless the dependency has resolved." |
| Decision-pending | "Route to intake — the blocking question is a new requirement that needs shaping." |
| Stale-block | "Propose Blocked → In Progress transition (mutating — needs Producer approval). Evidence: [blocker last mentioned X days ago]." |
| Stale claim (>72h, no progress) | "Flag: #<N> has no commits beyond the claim marker. Consumer may need a nudge." |
| Stale claim (>7 days, no progress, previously notified) | "Recommend release (mutating — needs Producer approval). The card returns to Ready for re-claim." |
| Suspended card (> 30 days) | "Recommend release — work has gone cold. Consumer should restart from a fresh card." |

## Step 4 — Stale-claim release procedure

If the Producer approves a release, apply the 5-step governance sequence
(action_id = 8 — cancel claim). Then:

```bash
git push origin --delete claim/<N>-<slug>
```

And transition the card Status: In Progress → Ready via `operating-kanban`
`transition_card` action (separate mutating action, action_id = 7).

Both actions — branch delete AND status transition — must be covered by
separate audit entries. See `references/triage-detail.md` § "Claim release
procedure" for the exact shell command sequence and error handling.

## How mutating actions are handled

Every mutating action this skill performs (Status transition, branch delete)
follows the 5-step governance sequence:

At each mutating action point:
1. Resolve the action_id (from `board-superpowers:classifying-actions`
   `references/action-id-catalog.md`).
2. Invoke `board-superpowers:classifying-actions` with that action_id;
   receive A (auto), R (requires approval), or N (forbidden).
3. If A: act → invoke `board-superpowers:auditing-actions` to record one
   entry.
4. If R:
   a. Invoke `board-superpowers:auditing-actions` to record the proposal.
   b. Surface the proposal to the Producer.
   c. Wait for the Producer's reply (approve / decline).
   d. On approve: act → invoke auditing-actions to record the result.
   e. On decline: invoke auditing-actions to record the decline; abort.
5. If N: refuse the action and surface the block reason; no audit entry.

**Typical autonomy class for this routine:**
- Status flip Blocked → In Progress (stale-block) → R-class.
- Stale-claim release (branch delete + Status flip to Ready) → R-class.

## Summary format

```
## Triage summary — <YYYY-MM-DD>

### Blocked cards (<count>)
- #<N> <title> — <blocker class>: <one-line>. Recommended: <action>

### Stale claims (<count>)
- #<N> <title> — <age>, <commit count> commits. Recommended: <action>
```

If nothing is blocked or stale: "Triage clean — no Blocked cards, no stale
claims. Board health is good."

## Sibling-plugin handoffs in this routine

The triage routine has two sibling-plugin handoff points. Both go through
`board-superpowers:composing-siblings` before routing.

### Handoff 1 — Decision-pending blocker that needs investigation

When a card's blocker is classified as `decision-pending` AND the blocking
question is technically complex (e.g., "we don't know which cache invalidation
strategy is correct"), the Producer may need systematic investigation help
before making the decision.

1. Invoke `board-superpowers:composing-siblings` with the "technical
   investigation" intent to confirm sibling routing.
2. Surface the routing decision: "Card #<N>'s blocker is a technical decision
   ('which cache strategy?'). Routing to `gstack:/investigate` for a
   structured investigation."
3. Route to `gstack:/investigate` with the blocking question and relevant
   context (the card body, the blocked card's spec pointer).

After `gstack:/investigate` completes with a recommendation, re-enter triage
at Step 1: the decision is now available, the blocker may have resolved to
a stale-block or a new intake requirement.

### Handoff 2 — Decision-pending blocker that generates a fresh requirement

When the decision-pending blocker surfaces a new design requirement (e.g.,
"we need to decide on the schema before this card can proceed"), route it to
intake rather than investigate:

1. Invoke `board-superpowers:composing-siblings` with the "new-requirement"
   intent.
2. Surface: "The blocking question for #<N> is a new requirement.
   Routing to `board-superpowers:intaking-requirement`."
3. Route to `board-superpowers:intaking-requirement` with the new requirement
   as input. The blocker card stays in Blocked status until the intake
   requirement's card lands and is addressed.

## Autonomy defaults for this routine

| Action | Default class | Rationale |
|--------|--------------|-----------|
| Status flip Blocked → In Progress (stale-block evidence) | R (requires approval) | Reversible but the Consumer's context is affected. |
| Stale-claim branch delete | R (requires approval) | Destructive; irreversible without git reflog. |
| Status flip In Progress → Ready (after branch delete) | R (requires approval) | Linked to branch delete — must both be approved together. |
| `gstack:/investigate` handoff | A (auto) | Informational routing; no board mutation. |

Both the branch delete and the status flip are proposed together as a single
R-class unit — do NOT propose them separately. The Producer approves or
declines the pair as one atomic action.

## Failure modes

| Situation | Correct handling |
|-----------|-----------------|
| `read_board` with Blocked filter returns empty | "No Blocked cards." Proceed to Step 2 (stale-claim scan). |
| Blocked card body has no blocker note | Flag as "blocker evidence missing". Recommend the Producer comment on the card with the blocker. Do NOT classify — the 3-class schema requires a named blocker. |
| Branch age computation fails (no commits, shallow clone) | Note the computation failure. Flag the branch as potentially stale. Do NOT recommend release without evidence. |
| `gstack:/investigate` returns an inconclusive result | Record the investigation result in the triage summary. Surface to the Producer: "Investigation returned inconclusive — manual decision required." |

## What this triage routine does NOT cover

Per design, this routine focuses on Blocked + stale-claim sweep. It does NOT:
- Backlog grooming (rotating items between Backlog and Ready).
- Cross-card dependency cycle detection.
- Estimate calibration (S/M/L drift).
- Velocity tracking.

Those are out of scope. See `references/triage-detail.md` for the full list
with rationale. The triage routine is intentionally narrow; scope creep degrades
its speed and reliability as a health-check primitive.
