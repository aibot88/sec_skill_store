---
name: sf-apex
description: Generates and reviews Salesforce Apex code (Brite edition) with 150-point scoring. TRIGGER when user writes, reviews, or fixes Apex classes, triggers, test classes, batch/queueable/schedulable jobs, touches .cls/.trigger files, works in brite-salesforce, asks about LeadTriggerHandler / LeadAfterInsertService dispatch, Queueable BATCH_SIZE=90 self-chaining, @TestVisible + Test.isRunningTest() escape hatches, Bypass_Validation_Rules pattern, DisqualifiedRecycleScheduler, or Apex-first automation decisions. DO NOT TRIGGER when LWC JavaScript (use sf-lwc), Flow XML (use sf-flow), SOQL-only queries (use sf-soql), permission metadata (use sf-permissions), or non-Salesforce code.
user-invocable: false
license: MIT
metadata:
  version: "1.1.0-brite.1"
  author: "Jag Valaiyapathy (upstream); Brite Company (customization)"
  upstream: "Jaganpro/sf-skills@ff1ab74"
  scoring: "150 points across 8 categories"
---

<!-- Adapted from Jaganpro/sf-skills@ff1ab74 (MIT). This file layers Brite conventions from brite-salesforce/CLAUDE.md §Apex & Automation (lines 175-196) + §Engineering Standards (lines 41-42). -->

# sf-apex: Salesforce Apex Code Generation and Review (Brite edition)

Use this skill when the user needs **production Apex**: new classes, triggers, selectors, services, async jobs, invocable methods, test classes, or evidence-based review of existing `.cls` / `.trigger` code.

## Brite Context

Brite's Apex stance:

- **Apex-first automation.** Flows are limited to screen flows and simple notifications; all business logic lives in Apex (`brite-salesforce/CLAUDE.md` §Engineering Standards line 41).
- **Trigger handler dispatch.** One trigger per object delegates to a handler class. After-insert work goes through a `*AfterInsertService` interface and per-LeadSource registries — new services register themselves under the matching source list, never in the handler body directly. Canonical example: `LeadTriggerHandler` + `LeadAfterInsertService` with `webFormAfterInsertServices` / `newsletterAfterInsertServices` registries.
- **Test coverage target.** 100% per class (not the 75% SF floor); 90%+ org-wide. Required for all triggers and service classes (`brite-salesforce/CLAUDE.md` §Engineering Standards line 42).
- **Async defaults.** Queueable for standard async, Schedulable for recurring work, Batch only for very large record volumes. Governor-limit discipline is enforced through `BATCH_SIZE=90` self-chaining and `LIMIT 2500` per Schedulable query.

**See also:** `brite-salesforce/CLAUDE.md` §Apex & Automation (lines 175-196 — the 20 gotchas this section summarizes), §Engineering Standards (Apex-first principle, coverage targets), §Permissions & Security line 171 (`Bypass_Validation_Rules` pattern), and `brite-salesforce/docs/artifacts/testing-strategy.md`.

## Brite Apex Conventions

These rules are non-negotiable on `brite-salesforce` and must surface during trigger handler work, async job design, validation-rule changes, and test authoring.

### 1. Apex-first — Flows only for screen flows and simple notifications

Business logic, data mutations, and anything with meaningful conditional branching belongs in Apex. Flows are reserved for Screen Flows (user-facing forms) and thin notification flows where Apex would be overkill. Source: §Engineering Standards line 41.

### 2. Trigger handler pattern — one trigger, one handler, per-source service registries

One trigger per object delegates to a handler class. After-insert services implement a `*AfterInsertService` interface and register in per-LeadSource lists on the handler. Canonical: `LeadTriggerHandler` holds `webFormAfterInsertServices` (for `LeadSource = 'Web_Form'`) and `newsletterAfterInsertServices` (for `LeadSource = 'Newsletter_Signup'`); the handler filters incoming leads by source and dispatches only to the matching registry. **Add new services via the interface and register them under the correct source — never inline business logic in the handler itself.** Source: §Apex line 177.

### 3. Queueable callout limit = 100 — BATCH_SIZE=90, self-chain, MAX_RETRIES=3

Any Queueable that performs callouts must cap processing to under the 100-callouts-per-transaction governor limit. Canonical pattern: `SlackWebformAlertJob` sets `BATCH_SIZE = 90` and self-chains for overflow, with `MAX_RETRIES = 3` to cap the retry fan-out. Source: §Apex line 178.

### 4. Queueable silent-retry diagnostic — N consecutive "Completed" jobs = silent failure

N consecutive `AsyncApexJob` rows with `Status = 'Completed'` for the same class = 1 original + (N-1) silent retries. This is the signature of a callout failure inside a self-chaining Queueable where the exception was caught (e.g., Named Credential misconfigured — jobs appear "Completed" because the exception did not propagate). **First debug step: check the Named Credential endpoint, not the Apex logic.** Source: §Apex line 179.

### 5. Schedulable DML row limit = 10,000 — use multiple LIMIT 2500 queries

Schedulable Apex has a hard 10,000-DML-row ceiling per execution. `DisqualifiedRecycleScheduler` runs 4 separate queries (DQ Contacts, DQ Leads, Lost Contacts, Lost Leads) each with `LIMIT 2500`, totaling exactly 10,000. Do not raise individual `LIMIT`s above 2500 without switching to Batchable. Source: §Apex line 184.

### 6. Scheduled Apex jobs don't survive sandbox refresh — re-schedule manually

`CronTrigger` records are copied on refresh but do not execute. After every sandbox refresh, re-schedule via Developer Console:

```apex
System.schedule('Annual Disqualified Recycle', '0 0 6 1 1 ?', new DisqualifiedRecycleScheduler());
```

Source: §Apex line 182.

### 7. Test escape hatches — `@TestVisible` + `Test.isRunningTest()` together

Security-critical handler bypass flags must use **both** `@TestVisible` (access-gate: keeps a `private` member callable from test classes without widening production access — note that any class in the same namespace can still write it, so this is not a write-time guard) and `Test.isRunningTest()` (runtime-gate: the bypass effect only fires in test context, so a non-test Apex write becomes a no-op). Narrow the scope — if only one check needs the hatch (e.g., free-email Name block), don't let the flag disable sibling checks (Website block). Canonical: `AccountTriggerHandler.skipFreeEmailNameBlockInTestsOnly`. Source: §Apex line 192.

### 8. `@TestSetup` static state doesn't persist into `@IsTest` methods

Each `@IsTest` method runs in its own transaction with fresh static state — mutations inside `@TestSetup` are rolled back for the test body. **To enable a flag for every test, set it as the first line of each `@IsTest` method** (or in a shared helper called from each), not inside `@TestSetup`. Source: §Apex line 191.

### 9. Queueables in `Test.stopTest()` re-enter handlers with current static state

`Test.stopTest()` synchronously drains enqueued Queueables. If a test flipped a `@TestVisible` handler-bypass flag and never reset it, the flag is **still active** when the Queueable fires — any DML it performs goes through the handler with the bypass on. **Reset the flag immediately after the specific fixture DML that needs it, before any `Test.startTest()` / `Test.stopTest()` block.** Source: §Apex line 193.

### 10. Before-update self-query caveat — exclude trigger records

SOQL inside a `before update` trigger sees the **pre-update** database state, so when checking "does this Contact have other open Opps?" while closing an Opp, the closing Opp still appears as open. Exclude the current trigger records from the query:

```apex
AND OpportunityId NOT IN :closedLostOpps.keySet()
```

Source: §Apex line 183.

### 11. `with sharing` does not restrict `User` queries

The `User` object is always org-wide-visible to any authenticated Apex context (including Guest and Integration Users) — sharing rules don't apply. `public with sharing` on a handler that queries `User` is misleading; the queries stay safe via parameter binding (bind variables, no injection), but **add a comment noting this distinction**. Does not apply to other standard objects. Source: §Apex line 196.

### 12. `Bypass_Validation_Rules` pattern

Every validation rule at Brite **must** include `NOT($Permission.Bypass_Validation_Rules)` as the first `AND` argument. Source: §Permissions & Security line 171. Activation caveat: the `Bypass_Validation_Rules` custom permission sits on `HubSpot_Migration` (`hasActivationRequired: true`) and only activates per UI session via `SessionPermissionSetActivation` — it does **not** take effect in Bulk API or `sf` CLI sessions. For data loads needing the bypass, verify with `FeatureManagement.checkPermission()`; workarounds: `sf data create record` (single REST call), patch after load, or temporarily flip `hasActivationRequired: false`. Source: §Permissions & Security line 172.

---

## When This Skill Owns the Task

Use `sf-apex` when the work involves:
- Apex class generation or refactoring
- trigger design and trigger-framework decisions
- `@InvocableMethod`, Queueable, Batch, Schedulable, or test-class work
- review of bulkification, sharing, security, testing, or maintainability

Delegate elsewhere when the user is:
- editing LWC JavaScript / HTML / CSS → [sf-lwc](../sf-lwc/SKILL.md)
- building Flow XML or Flow orchestration → [sf-flow](../sf-flow/SKILL.md)
- writing SOQL only → [sf-soql](../sf-soql/SKILL.md)
- deploying or validating metadata to orgs → [sf-deploy](../sf-deploy/SKILL.md)

---

## Required Context to Gather First

Ask for or infer:
- class type: trigger, service, selector, batch, queueable, schedulable, invocable, test
- target object(s) and business goal
- whether code is net-new, refactor, or fix
- org / API constraints if known
- expected test coverage or deployment target

Before authoring, inspect the project shape:
- existing classes / triggers
- current trigger framework or handler pattern
- related tests, flows, and selectors
- whether TAF is already in use

---

## Recommended Workflow

### 1. Discover local architecture
Check for:
- existing trigger handlers / frameworks
- service-selector-domain conventions
- related tests and data factories
- invocable or async patterns already used in the repo

### 2. Choose the smallest correct pattern
| Need | Preferred pattern |
|---|---|
| simple reusable logic | service class |
| query-heavy data access | selector |
| single object trigger behavior | one trigger + handler / TAF action |
| Flow needs complex logic | `@InvocableMethod` |
| background processing | Queueable by default |
| very large datasets | Batch Apex or `Database.Cursor` patterns |
| repeatable verification | dedicated test class + test data factory |

### 3. Author with guardrails
Generate code that is:
- bulk-safe
- sharing-aware
- CRUD/FLS-safe where applicable
- testable in isolation
- consistent with project naming and layering

### 4. Validate and score
Evaluate against the 150-point rubric before handoff.

### 5. Hand off deploy/test next steps
When org validation is needed, hand off to:
- [sf-testing](../sf-testing/SKILL.md) for test execution loops
- [sf-deploy](../sf-deploy/SKILL.md) for deploy / dry-run / verification

---

## Generation Guardrails

Never generate these without explicitly stopping and explaining the problem:

| Anti-pattern | Why it blocks |
|---|---|
| SOQL in loops | governor-limit failure |
| DML in loops | governor-limit failure |
| missing sharing model | security / data exposure risk |
| hardcoded IDs | deployment and portability failure |
| empty `catch` blocks | silent failure / poor observability |
| string-built SOQL with user input | injection risk |
| tests without assertions | false-positive test suite |

Default fix direction:
- query once, operate on collections
- use `with sharing` unless justified otherwise
- use bind variables and `WITH USER_MODE` where appropriate
- create assertions for positive, negative, and bulk cases

See [references/anti-patterns.md](references/anti-patterns.md) and [references/security-guide.md](references/security-guide.md).

---

## High-Signal Build Rules

### Trigger architecture
- Prefer **one trigger per object**.
- If TAF is already installed and used, extend it instead of inventing a second trigger pattern.
- Triggers should delegate logic; avoid heavy business logic directly in trigger bodies.

### Async choice
| Scenario | Default |
|---|---|
| standard async work | Queueable |
| very large record processing | Batch Apex |
| recurring schedule | Scheduled Flow or Schedulable |
| post-job cleanup | Finalizer |
| long-running Lightning callouts | `Continuation` |

### Testing minimums
Use the **PNB** pattern for every feature:
- **Positive** path
- **Negative** / error path
- **Bulk** path (251+ records where relevant)

### Modern Apex expectations
Prefer current idioms when available:
- safe navigation: `obj?.Field__c`
- null coalescing: `value ?? fallback`
- `Assert.*` over legacy assertion style
- `WITH USER_MODE` and explicit security handling where relevant

---

## Output Format

When finishing, report in this order:
1. **What was created or reviewed**
2. **Files changed**
3. **Key design decisions**
4. **Risk / guardrail notes**
5. **Test guidance**
6. **Deployment guidance**

Suggested shape:

```text
Apex work: <summary>
Files: <paths>
Design: <pattern / framework choices>
Risks: <security, bulkification, async, dependency notes>
Tests: <what to run / add>
Deploy: <dry-run or next step>
```

---

## LSP Validation Note

This skill supports an LSP-assisted authoring loop for `.cls` and `.trigger` files:
- syntax issues can be detected immediately after write/edit
- the skill can auto-fix common syntax errors in a short loop
- semantic quality still depends on the 150-point review rubric

Full guide: [references/troubleshooting.md](references/troubleshooting.md#lsp-based-validation-auto-fix-loop)

---

## Cross-Skill Integration

| Need | Delegate to | Reason |
|---|---|---|
| describe objects / fields first | [sf-metadata](../sf-metadata/SKILL.md) | avoid coding against wrong schema |
| seed bulk or edge-case data | [sf-data](../sf-data/SKILL.md) | create realistic test datasets |
| run Apex tests / fix failing tests | [sf-testing](../sf-testing/SKILL.md) | execute and iterate on failures |
| deploy to org | [sf-deploy](../sf-deploy/SKILL.md) | validation and deployment orchestration |
| build Flow that calls Apex | [sf-flow](../sf-flow/SKILL.md) | declarative orchestration |
| build LWC that calls Apex | [sf-lwc](../sf-lwc/SKILL.md) | UI/controller integration |

---

## Reference Map

### Start here
- [references/patterns-deep-dive.md](references/patterns-deep-dive.md)
- [references/security-guide.md](references/security-guide.md)
- [references/bulkification-guide.md](references/bulkification-guide.md)
- [references/testing-patterns.md](references/testing-patterns.md)

### High-signal checklists
- [references/code-review-checklist.md](references/code-review-checklist.md)
- [references/anti-patterns.md](references/anti-patterns.md)
- [references/naming-conventions.md](references/naming-conventions.md)

### Specialized patterns
- [references/trigger-actions-framework.md](references/trigger-actions-framework.md)
- [references/automation-density-guide.md](references/automation-density-guide.md)
- [references/flow-integration.md](references/flow-integration.md)
- [references/triangle-pattern.md](references/triangle-pattern.md)
- [references/design-patterns.md](references/design-patterns.md)
- [references/solid-principles.md](references/solid-principles.md)

### Troubleshooting / validation
- [references/troubleshooting.md](references/troubleshooting.md)
- [references/llm-anti-patterns.md](references/llm-anti-patterns.md)
- [references/testing-guide.md](references/testing-guide.md)

---

## Score Guide

| Score | Meaning |
|---|---|
| 120+ | strong production-ready Apex |
| 90–119 | good implementation, review before deploy |
| 67–89 | acceptable but needs improvement |
| < 67 | block deployment |
