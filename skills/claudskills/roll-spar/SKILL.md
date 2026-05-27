---
name: roll-spar
license: MIT
model: sonnet
allowed-tools: "Read, Edit, Write, Bash, Agent, Skill"
description: Adversarial TDD mode with Attacker/Defender agents. Attacker writes tests to break the system, Defender writes minimal code to pass. Use for high-risk logic like auth, payments, data integrity, or complex state machines.
---

# Spar

Adversarial TDD: two agents collaborate in attack-and-defend mode to build a more robust system.

## When to Use

**Manual trigger:**
- User explicitly requests `$roll-spar`
- Involves core business logic requiring higher quality assurance

**Auto trigger (agent judgment):** Recommend enabling when any of these conditions are met
- Involves authentication / authorization / security
- Involves money / payments / billing
- Involves data integrity (writes are irreversible)
- Complex state machines / concurrency logic
- Module has had previous bugs (BACKLOG has related FIX records)

**Do not use for:**
- UI styling adjustments, copy changes
- Simple CRUD
- Configuration changes
- Small tasks not worth the overhead of two-agent collaboration

## Roles

### Attacker (Red Agent)

**Goal: Find weaknesses in the code and write tests that break the system.**

- Think about boundary conditions, invalid inputs, concurrency scenarios, state inconsistencies
- Write the trickiest test cases possible
- Don't care about implementation difficulty — only care about "can the system handle this scenario"
- Write at least 1 RED test per round, can write multiple

### Defender (Green Agent)

**Goal: Make all tests pass with the simplest, most robust code possible.**

- Cannot modify tests written by the Attacker (unless the test itself has a bug)
- Aim for minimal implementation, avoid over-engineering
- Make all tests GREEN each round, then commit
- May refactor, but must stay GREEN

## Workflow

```
User: "$roll-spar implement transfer logic" or agent auto-triggers
    │
    ▼
┌─────────────────────────────────────┐
│ 0. Setup                            │
│    - Define feature scope and AC    │
│    - Create test file skeleton      │
│    - Context brief for Attacker     │
│      and Defender                    │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Spar Loop (repeat until converged)  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ 🔴 Attacker Turn             │  │
│  │    - Analyze current code/API │  │
│  │    - Write 1+ RED tests      │  │
│  │    - State attack intent:     │  │
│  │      "Test balance consistency│  │
│  │       during concurrent       │  │
│  │       transfers"              │  │
│  └──────────────┬────────────────┘  │
│                 │                    │
│                 ▼                    │
│  ┌───────────────────────────────┐  │
│  │ 🟢 Defender Turn             │  │
│  │    - Read Attacker's tests   │  │
│  │    - Write minimal code to   │  │
│  │      make tests pass         │  │
│  │    - Run all tests → GREEN   │  │
│  │    - git commit              │  │
│  └──────────────┬────────────────┘  │
│                 │                    │
│                 ▼                    │
│  ┌───────────────────────────────┐  │
│  │ 🔴 Attacker Turn (again)     │  │
│  │    - Review Defender's impl  │  │
│  │    - Find new weaknesses,    │  │
│  │      write new RED tests     │  │
│  │    - Or: "No new weaknesses  │  │
│  │      found"                  │  │
│  └──────────────┬────────────────┘  │
│                 │                    │
│        ┌────────┴────────┐          │
│        │                 │          │
│   Has new tests    No new tests     │
│   → Continue loop  → Exit Spar      │
│                                     │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Wrap-up                             │
│    - Attacker summarizes attack     │
│      coverage                       │
│    - Defender summarizes defense    │
│      strategy                       │
│    - Merged report                  │
│    - Continue normal roll-build     │
│      flow                           │
│      (push → CI → deploy → verify)  │
└─────────────────────────────────────┘
```

## Spar Convergence Conditions

Attacker declares completion when any of these are met:
- Cannot write a new RED test for 2 consecutive rounds
- Already covered: happy path + boundary values + invalid inputs + concurrency/race conditions + state consistency
- Reached the agreed maximum number of rounds (default: 5 rounds)

## Agent Context Brief

### Attacker Brief Template

```markdown
## Role: Attacker (Red Agent)

Your goal is to find weaknesses in this code.

### Feature Description
{Feature AC and interface definition}

### Current Implementation
{Defender's latest code, or "not yet implemented"}

### Existing Tests
{Currently existing test cases}

### Your Task
Write 1+ new test cases that make the current implementation fail (RED).
Directions to explore:
- Boundary values (0, -1, MAX_INT, empty string, null)
- Exception flows (network disconnect, timeout, duplicate requests)
- Concurrency (two requests arriving simultaneously)
- State consistency (is system state clean after mid-process failure)

### Output Format
For each test, state the attack intent:
  "Attack: {scenario description} — expected system behavior: {expected behavior}"
```

### Defender Brief Template

```markdown
## Role: Defender (Green Agent)

Your goal is to make all tests pass with the simplest implementation.

### Feature Description
{Feature AC and interface definition}

### Current Code
{Your previously written code, or empty}

### New RED Tests
{Tests written by the Attacker this round}

### Your Task
Modify/add code to make all tests (including previous ones) pass.
Rules:
- Cannot modify tests written by the Attacker
- Aim for minimal changes
- Keep the code clear
- Commit after all tests are GREEN
```

## Status Report

Report to the user after each round:

```
⚔️ Spar Round {N}

  🔴 Attacker:
     Attack: {scenario 1} — {result}
     Attack: {scenario 2} — {result}

  🟢 Defender:
     Defense strategy: {brief description of how it was defended}
     Test status: {passed}/{total} ✅

  📊 Cumulative: {total tests} tests, {total rounds} rounds
  🔄 Next round: Attacker continues looking for weaknesses...
```

## Hard Rules

1. **Attacker does not write implementation code** — only writes tests and attack analysis
2. **Defender does not modify tests** — unless the test itself has a bug (must explain the reason)
3. **Must commit each round** — Defender commits immediately after making tests GREEN, keeping the repo clean
4. **Attack intent must be explained** — cannot just write tests without explaining "why this scenario matters"
5. **Maximum round limit** — default 5 rounds, prevents infinite loops

## Integration with roll-build

Spar replaces steps 4-5 in roll-build (Test Design + TCR Implementation):

```
roll-build normal flow:
  1. Clarify Story
  2. Split Actions
  3. Define verification
  ──────────────────────
  4. Test Design Review    ← Spar replaces this step
  5. TCR Implementation    ← and this step
  ──────────────────────
  6. Local CI check        ← Back to normal flow
  7. Quality Review
  ...
```

**Auto-switching from roll-build to Spar:**

When the agent assesses an Action as high-risk at step 3:
```
⚔️ High-risk Action detected: {description}
   Risk factors: {auth/payment/data integrity/...}
   Recommend enabling Spar mode — confirm? [Y/n]
```

After user confirms, enter Spar. Once complete, return to roll-build step 6 to continue.

## Example

```
User: "$roll-spar implement user balance transfer"

⚔️ Spar: User Balance Transfer

── Round 1 ──

🔴 Attacker:
   Attack 1: Transfer amount is 0 — should reject
   Attack 2: Transfer amount is negative — should reject
   Attack 3: Transfer amount exceeds balance — should reject and keep balance unchanged

🟢 Defender:
   Implementation: transfer(from, to, amount) basic validation
   Tests: 3/3 ✅
   commit: "tcr: transfer basic validation"

── Round 2 ──

🔴 Attacker:
   Attack 4: Transfer to self — should reject
   Attack 5: Two concurrent transfers whose total exceeds balance — only one should succeed

🟢 Defender:
   Implementation: add self-transfer check + optimistic lock
   Tests: 5/5 ✅
   commit: "tcr: transfer self-check and concurrency lock"

── Round 3 ──

🔴 Attacker:
   Attack 6: Database error mid-transfer — both balances should remain unchanged (atomicity)
   Attack 7: Recipient account does not exist — should reject and keep sender's balance

🟢 Defender:
   Implementation: database transaction wrapper + recipient existence check
   Tests: 7/7 ✅
   commit: "tcr: transfer atomicity and recipient validation"

── Round 4 ──

🔴 Attacker:
   No new weaknesses found. Covered: input validation, self-transfer, concurrency, atomicity, related accounts.

⚔️ Spar Complete!
   📊 4 rounds, 7 tests, 3 commits
   🔴 Attack coverage: input boundaries + business rules + concurrency + atomicity
   🟢 Defense strategy: upfront validation + optimistic lock + transactions
```
