---
name: ctrl-c-v-tdd
description: |
  Test-pattern doctrine. Tests are copyable from
  ~/.claude/patterns/tests/, three categories: input boundary,
  contract, effect. Make sure to consult this skill whenever code
  changes touch a boundary where someone else's code meets yours,
  even if the user doesn't say "test" or "TDD" — Claude tends to
  ship untested boundary code, and this skill prevents the Saturday
  phone call.
  TRIGGER when: code under change has external callers (other
  modules, cron, CLI, HTTP/RPC clients, "外部调用", "被外部调用");
  persists state (DB write, file write, redis/cache, session
  storage, anything that survives the request); calls third-party
  API/SDK; task is classified as LARGE per ctrl-c-v sizing (4+
  files, new capability, new architecture, new external contract)
  — LARGE always triggers TDD regardless of caller scope; user
  mentions tests, TDD, 测试, boundary, contract, mock, fixture,
  red/green; business domain involves payments, queues, webhooks,
  auth, external integration.
  SKIP when: code change is purely internal helpers used only by
  caller in same file; pure UI rendering with no validation/state;
  accessor < 10 lines with no if/loop/exception; one-file fix that
  ctrl-c-v classifies as SMALL.
  Examples that trigger: "implement Stripe webhook handler",
  "add retry to the upload pipeline", "this database migration",
  "build a multi-step checkout form with validation across steps".
  Examples that skip: "rename this private function", "fix
  formatting in style.css".
extends: ctrl-c-v
---

# Ctrl+C Ctrl+V — TDD Extension

You are the same engineer. Same Friday flight to the Alps. Same system.
You learned one thing the hard way: the code that gets you called back
on Saturday is never the code you wrote — it is the code you forgot to
test at the boundary.

So you built a second pattern library. Tests, like code, are copyable.
A test for "rejects bad input" is the same shape whether the input is
an email or a date. You copy, change the assertion, change the fixture,
ship. You do not write every test. You write tests where it matters:
at boundaries where someone else's code meets yours.

---

## § T0 — When TDD activates

The question is never "should I follow TDD?" — it is "who calls this?"

| Caller of the code under change | Tests? |
|---|---|
| Only this file (private helper) | NO |
| Only this module (internal use) | NO unless logic is non-trivial |
| Other modules in this project | YES — contract test |
| External processes, jobs, CLI users | YES — contract + boundary |
| Third-party API or DB (you call out) | YES — effect test (mock the boundary) |
| HTTP / RPC client (you are callee) | YES — contract + boundary + effect |
| Pure UI rendering, no logic | NO |
| UI with state machine or input validation | YES — contract on the logic |

Two-question fallback when the table feels ambiguous:

1. If this returns the wrong value silently, who notices? "Nobody for a week" → write the test.
2. If someone refactors this next month, what tells them they broke it? "Nothing" → write the test.

## § T1 — TDD integrates with task sizing

Same SMALL / MEDIUM / LARGE. TDD slots into each.

- **SMALL** — no tests. § 6 self-review is the gate.
- **MEDIUM** — § T0 decides. If YES: copy test pattern → RED → implement → GREEN → § 6 → § 7.
- **LARGE** — tests required and written FIRST. Active spec lists test cases as part of Plan. Boundary tests all RED before any implementation. Each task in Tasks: turns specific tests GREEN.

When in doubt, the § T0 table decides — not vibes.

## § T2 — Find before you write (test version)

Same hierarchy as § 1. Different library.

```
0. ~/.claude/patterns/tests/INDEX.md → match? → copy that .md
1. THIS PROJECT     grep "TEST PATTERN:" in tests/
2. FRAMEWORK        does the test framework provide this fixture?
3. APPROVED DEPS    approved test helper / mock library?
4. TEMPLATES        tests/templates/ or example test files
5. OFFICIAL DOCS    framework's docs → copy example
6. FROM SCRATCH     last resort → save to patterns/tests/
```

Step 6 has the same tax as § 5: tag, save, index. Details → @${CLAUDE_SKILL_DIR}/playbooks/test-search.md

## § T3 — Test the boundary, not the implementation

Three categories. Pick by what the code does, not by framework.

| Category | Tests this question | Example shape |
|---|---|---|
| **Input boundary** | Does it reject bad input? | empty / null / oversize / wrong type / malicious |
| **Contract** | Does it return what callers expect? | shape, field names, error types, success vs failure |
| **Effect** | Does it produce the right side effect? | DB row, API call, file write, event emitted |

Write ONE of each. Not three of the same kind. Per-category templates → @${CLAUDE_SKILL_DIR}/playbooks/test-boundaries.md

## § T4 — Tests are also patterns

```
# TEST PATTERN: contract — pure function, happy + 2 errors
# USE WHEN: input → output mapping, no side effects
# COPY THIS: change function name, fixture, expected output, error cases
```

Tag, copy, save. Identical mechanics to § 3 and § 5. The library at
`~/.claude/patterns/tests/` is your second library — grepped together
with code patterns, not separately.

Copying a pattern → @${CLAUDE_SKILL_DIR}/playbooks/test-copy.md

When no pattern fits → @${CLAUDE_SKILL_DIR}/playbooks/test-scratch.md

## § T5 — Test self-review

```
□  Test name reads as a sentence: "rejects_empty_email"
□  One test, one assertion focus
□  No test depends on another's order
□  No real network / real DB (mock the boundary)
□  Test fails for the right reason: comment out impl → does it RED?
□  TEST PATTERN tag added if shape is reusable
□  Test file mirrors source (framework convention)
```

Red flag: a test that still passes when you delete the implementation
under test. That test is testing nothing.

Full checklist → @${CLAUDE_SKILL_DIR}/playbooks/test-review.md

## § T6 — LARGE tasks: spec drives tests drives code

LARGE task's Active spec gets one extra subsection:

```
### Test plan
- [ ] T1 boundary: rejects [bad inputs]
- [ ] T2 contract: returns [shape] when [condition]
- [ ] T3 effect: writes [row] to [table] on success
- [ ] T4 effect: does NOT call [external] when [condition]
```

All boundary tests RED before any implementation task starts. Each
task maps to specific tests turning GREEN. "Verify" in Tasks checklist
= "test Tn passes."

LARGE-specific rhythm → @${CLAUDE_SKILL_DIR}/playbooks/test-large.md

---

## — Completion criteria —

**Boundary coverage** — every external caller has a contract test.
Every effect has an effect test.

**Pattern reuse** — second similar test next month: copy, change 5
lines, ship.

**Refactor safety** — colleague rewrites your function next quarter.
Tests catch the break before merge. You stay on the slopes.

---

*See you on the slopes.* ⛷️
