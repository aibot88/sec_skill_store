---
name: agile-project
description: "Use this skill whenever you are working on a Go project following the agile-team-v2 workflow — features in .features/, sprints in .sprints/, strategic ADRs in .adrs/, tactical/strategic decisions log in .decisions/, global architecture in .architecture/ (VISION.md + ARCHITECTURE.md + CONVENTIONS.md + INTEGRATIONS.md). The architect absorbs the ex-scaffolder role: scaffolds Go contracts (signatures with `panic(\"not implemented\")` bodies), inlines `// AC: <criterion>` + `// TODO(impl-<feat>, ac-<NNN>)` markers above each scaffolded body, and decides the `mechanical: true|false` flag in FEATURE.md frontmatter. The PM has two passes: passe 1 (FEATURE.md narrative — Why/Context/User journey/Out of scope/Open questions), passe 2 (inline `// SCENARIO:` + `t.Skip(\"not implemented\")` in business test skeletons within `pm_test_territories`, skipped if `mechanical: true`). The sprint-planner lists tasks **by code marker** in SPRINT.md (no separate TASK.md / TASK-red.md / TASK-green.md / SCAFFOLD.md / TASKS.md files — those v1 artifacts no longer exist). Spec isolation between red and green is preserved by **discipline**: red reads `// AC:` + `// SCENARIO:`, green reads `// AC:` + red's committed test assertions. There is one `red` agent and one `green` agent (no per-tier variants — anticipates bloc 3). Tactical DECISIONS authored by green during a sprint (under R2 strict rules) are surfaced in RETRO.md `decisions_to_statue:` and statued by the architect at the start of the next sprint via a Wave 1 task. The reviewer runs three passes (DoD via `scripts/check.sh`, Scenarios narrative-vs-tests, Security checklist). The `## Human override` section of REVIEW.md is human-only with strict 5-field format; security findings cannot be overridden without a Decision reference. Triggers: any Go file editing in this kind of project (must use go-surgeon — never generic Edit/Write/Read), sprint planning, feature breakdown, FEATURE.md / SPRINT.md / REVIEW.md / RETRO.md / DECISION-NNN-*.md mentions, dispute files in .disputes/, any of the product-manager/architect/sprint-planner/red/green/e2e-tester/reviewer/bug-detective agents, `Authored-By:` commit trailer, the `// AC:` / `// SCENARIO:` / `TODO(impl-...)` markers, or any repository containing .features/ / .sprints/ / .adrs/ / .architecture/ / .decisions/ directories. Consult before planning a sprint, before starting any task, before writing a commit, before responding to a dispute, or whenever you need to know what artifact goes where. Detailed marker conventions and lifecycle live in `markers` skill. Decision-log format and R2/R6 rules live in the separate `decisions-and-adrs` skill (loaded by architect/green/sprint-planner only)."
---

# Agile Project Workflow — v2

Workflow for Go projects using strict TDD, sprint-based agile, **intent-in-code** (no prose intermediaries), and the new `.decisions/` log with two-zone frontmatter and `Authored-By:` trailer audit.

The intent of v2 is captured in one sentence: **the code and the tests are the authority of execution.** No `TASK.md`, no `TASK-red.md`, no `TASK-green.md`, no `SCAFFOLD.md`, no per-feature `ARCHITECTURE.md`, no `TASKS.md`. Acceptance criteria live as `// AC:` comments above scaffolded function bodies. User-journey scenarios live as `// SCENARIO:` comments above business test skeletons. The sprint-planner lists tasks by code marker, not by prose file. Spec isolation between red and green is preserved by **discipline**, not by separate files.

**Companion documents:**

- `markers` skill — full marker conventions and lifecycle. Load when you need the exact format.
- `skills/decisions-and-adrs/SKILL.md` — separate skill for `.decisions/` and `.adrs/` write rules. Loaded by architect, green, sprint-planner only.

---

# Go file editing — ABSOLUTE RULE

**STRICTLY FORBIDDEN** to use `Edit`, `Write`, `Read`, `Grep`, or any generic tool to read or modify a `.go` file.

For **every** `.go` file without exception:

- Reading → `go-surgeon symbol` or `go-surgeon overview`.
- Creation → `go-surgeon create`.
- Modification → `go-surgeon patch_function`, `patch_struct`, `patch_interface`, `update`, `insert_call`, etc.

Applies even for a single-line change. No exceptions.

---

# Parallelization — ABSOLUTE RULE

Use sub-agents (`Agent` tool) or agent teams for any task composed of independent parts (no file conflicts, no result dependencies).

- Launch parallel work in a single message (multiple simultaneous tool calls, or a team spawn).
- Never execute sequentially what can be parallelized.

**Default heuristic — feature as the unit of parallelism:**

- One agent per feature, traversing all tasks of that feature (all reds first, then all greens, in dependency order).
- Features run in parallel with each other.
- Within a feature, tasks run sequentially under one agent — that agent keeps the feature context warm across tasks.

This caps live agents to roughly the number of features in scope (typically 2–4 per sprint). It trades some theoretical parallelism for crash containment: a rate-limit on one feature does not corrupt three others' in-flight state.

**What to avoid:**

- Spawning N agents where N equals task count (the v1 anti-pattern: 23 reds in parallel, 3 crashed mid-run, batch-commit lost work across all 23).
- Mixing red and green of the same task on the same agent — spec-isolation discipline breaks.
- Two agents writing to the same package concurrently (file-level races on `go-surgeon` edits).

The sprint-planner documents the chosen fan-out in `SPRINT.md` under `## Parallelization plan`, with a one-sentence rationale. Crash recovery procedure: see the `sprint-planner` agent for the salvage/revert/re-spawn protocol.

---

# Tests — ABSOLUTE RULE

Every non-mechanical feature **must** include:

- **Unit tests** for any logic in domain and application layers (table-driven, mocks via interfaces).
- **Contract tests** for each repository adapter (via testcontainers).
- **E2E / integration tests** at least one end-to-end scenario per `// SCENARIO:` marker.

Tests are produced **after scaffolding and before implementation**, following the strict red/green pattern. A non-mechanical feature without tests is not done.

For `mechanical: true` features, the test bar drops to "existing tests still pass" — there is no `// SCENARIO:` to materialize.

---

# Complexity classification — ABSOLUTE RULE

Every feature carries a `## Complexity` field in its FEATURE.md, one of `mechanical`, `standard`, `architectural`. **Distinct from the `mechanical:` frontmatter flag** — see `task-complexity-routing` skill for the discussion.

- Missing complexity field fails DoR.
- The sprint-planner decides pipeline routing based on this field.
- A task can be **upgraded** in complexity during execution (via dispute type G), **never downgraded** while in flight. Over-classification is corrected in the retro for future calibration, not by demoting the running task.

Detailed classification heuristics, escalation signals, and retro calibration live in the `task-complexity-routing` skill. Load that skill only when classifying, routing, or reviewing classification accuracy — not for routine implementation work.

---

# Scaffolding-first — ABSOLUTE RULE (architect-owned)

Before red and green start a feature, the **architect** produces the testable contract — all exported types, interfaces, and function/method signatures with empty bodies (`panic("not implemented: ...")` or zero-value returns). The architect inlines `// AC: <criterion>` + `// TODO(impl-<slug>, ac-<NNN>)` above each scaffolded body that maps to an acceptance criterion derived from the user journey.

There is **no separate scaffolder agent** in v2 — the architect does both. The v1 `SCAFFOLD.md` artifact does not exist; the scaffolding evidence is the diff itself.

- One scaffolding pass per feature (one architect commit) before any red or green task starts.
- The architect couples with `scaffor` (https://github.com/JLugagne/scaffor) when configured to generate mocks and test scaffolds from the interfaces declared.
- All red tasks of the feature are blocked until scaffolding is committed.
- **Red cannot modify scaffolded signatures** or `// AC:` comments. If a signature is untestable, red raises a dispute (decision A — architect revises).
- **Green cannot modify scaffolded signatures** or add new exported symbols. Green may add **private (unexported)** helpers; logged in `RETRO.md helpers_added:` for retroactive coverage in a sub-sprint.

Detailed SCAFFOLD Definition of Done (the per-item checklist the architect ticks at end of scaffolding) lives in the `architect.md` agent spec.

---

# Red/Green pattern — ABSOLUTE RULE

All **production-code feature work** at `standard` or `architectural` complexity follows strict TDD with **paired teammates** and **discipline-based spec isolation**:

- **Red phase**: the `red` agent writes failing tests against the scaffolded contract. Cannot edit production code or scaffolded signatures.
- **Green phase**: the `green` agent implements scaffolded function bodies. Cannot edit test code, cannot modify scaffolded signatures, cannot add exported symbols.
- **Spec isolation by discipline**: in v2 there are no `TASK.md` / `TASK-red.md` / `TASK-green.md` files. Red and green find their work via the inline marker `TODO(impl-<slug>, ac-<NNN>)` in code (`grep`); the only handoff is committed code/tests. Neither reads the other's in-flight work.

**Detailed isolation rules, in-scope / out-of-scope discrimination, mono-assistant safeguard, and the marker lookup procedure live in the `tdd-pattern` skill — loaded by `red` and `green` only.** Other agents do not need those rules.

---

# Commit cadence — ABSOLUTE RULE

Each agent **commits after every completed task**, never in batches. One commit per `<TASK_ID>`. A teammate finishing two tasks in a row produces two commits, not one squashed commit.

This bounds the blast radius of an agent crash, rate-limit interruption, or session loss to **one task** instead of a whole wave.

---

# Commits — ABSOLUTE RULE

Every commit message **must** reference feature and task:

```
<short description>

Feature: <feature-slug>
Task: <TASK_ID>
[Authored-By: <agent-id>]   <-- mandatory on .decisions/ and mechanical: changes (R6)
```

- `Feature:` slug under `.features/<slug>/`. `maintenance` for non-feature work.
- `Task:` includes a phase suffix matching the agent's role (e.g., `<slug>-scaffold`, `<slug>-T<NNN>-red`, `<slug>-T<NNN>-green`, `<slug>-E<NNN>`, `<slug>-REVIEW`, `SPRINT_00X-REVIEW`, `SPRINT_00X-retro`, `<slug>-T<NNN>` for mono-agent, `<slug>-T<NNN>-bugfix`, `<slug>-decision-review`, `H<NNN>-red`). Each agent spec documents the suffix it uses.

**`Authored-By:` trailer** — mandatory whenever the commit creates/modifies/deletes any file under `.decisions/`, modifies the `mechanical:` field in any FEATURE.md frontmatter, or modifies the `review.reviewed_by` field in any DECISION. Values: `architect` or `green`. `check.sh` cross-checks `git blame` against the trailer (R6); mismatch is a CI block. **Full rules and examples in the `decisions-and-adrs` skill.**

Branches: `<feature-slug>/<TASK_ID>-<short-description>` (e.g., `auth-login/T003-green-impl`).

---

# Push timing — ABSOLUTE RULE

A red wave produces tests that fail by design. A pre-push hook running `go test ./...` will reject these commits, and bypassing it (`--no-verify`) defeats the gate for everyone.

The rule:

- **Never push to `main`** (or any shared branch with a green-tests pre-push hook) **in the middle of a red wave.**
- A push to a shared branch is allowed **only** at the end of a complete green wave, when `go test ./...` passes locally.
- Within a wave, commits stay local (or on a per-feature branch) until the matching green completes.

Allowed branching strategies, pick one per project (document in `.architecture/CONVENTIONS.md`):

1. **Trunk + delayed push** (default for solo / small teams) — commit red and green locally on `main`, push only when the green wave finishes.
2. **Per-feature branch + sprint-end PR** — each feature lives on `<feature-slug>` branch; red and green commits push freely there (no green-tests gate on feature branches); sprint review opens a PR to `main` once all greens are complete.

What is **not** allowed:

- `git push --no-verify` to bypass the green-tests hook during a red wave.
- A custom hook escape hatch keyed off the commit message.

`check.sh` in CI mode audits `git log` over the sprint window for `--no-verify` markers (R4).

---

# Roles summary (8 agents)

| Role             | Owns                                                                                              | Model  |
|------------------|---------------------------------------------------------------------------------------------------|--------|
| product-manager  | FEATURE.md (Why/Context/User journey/Out of scope/Open questions); `// SCENARIO:` markers in `pm_test_territories`; `.features/INDEX.md` (todo / ready transitions). | sonnet |
| architect        | `.architecture/`, `.adrs/` (strategic), `.decisions/` (strategic + reviewing tactical); scaffolded production signatures with `// AC:` + `panic`; `mechanical:` flag in FEATURE.md; `## Relevant decisions` section. | opus   |
| sprint-planner   | `.sprints/SPRINT_00X/SPRINT.md` (tasks listed by code marker); dispute decisions; `RETRO.md` `## Metrics` and YAML frontmatter (incl. `decisions_to_statue:`); sub-sprint creation; INDEX.md `ready` → `in-progress`. | opus   |
| red              | `*_test.go`, `testdata/`, `testutil/`, `mocks/` (replaces PM's `t.Skip` with assertions in business tests; writes fresh tests in non-business areas).            | sonnet |
| green            | Non-test `.go` files (function bodies in scaffolded stubs; private helpers); tactical DECISIONS in `.decisions/` under R2 strict rules; `RETRO.md helpers_added:` (append-only). | sonnet |
| e2e-tester       | E2E scenarios in `pm_test_territories` (transforms PM's `t.Skip` into real e2e against testcontainers).                                                            | sonnet |
| reviewer         | REVIEW.md `## Findings` (feature and sprint level); `.features/INDEX.md` `done`/`blocked` for feature it just signed off; `.sprints/INDEX.md` `done`. | sonnet |
| bug-detective    | `.bugs/<bug-id>.md` (post-mortem investigation; classification implementation-bug / spec-bug / architectural-bug; never proposes the fix).                          | sonnet |

---

# Project workflow

## Principles

- Work happens in sprints. Maintenance (typos, dep updates, linting, small refactors) can happen outside sprints.
- Every non-trivial decision is documented either as a strategic ADR (`.adrs/`) or as a DECISION (`.decisions/`). Format and R2/R6 rules in the `decisions-and-adrs` skill.
- Blockers and open questions **always** require human input — no auto-resolution. No sprint, feature, or task starts while a blocker or open question is pending.
- Red and green operate with **discipline-based** spec isolation. Cross-reading in-flight work is forbidden; the only handoff is committed code/tests.
- DECISIONS and ADRs listed in FEATURE.md `## Relevant decisions` propagate naturally — every agent reads them via that section.

## Global architecture (.architecture/)

Owned by the **architect**. The directory replaces the v1 `OVERVIEW.md` with two distinct files:

- `VISION.md` — why the project exists. 50–100 lines. Audience: any new contributor or agent.
- `ARCHITECTURE.md` — data model, layer boundaries, runtime topology, technical choices. 200–400 lines.
- `CONVENTIONS.md` — coding conventions, error handling, logging, observability, branching, push timing, **`pm_test_territories`** glob block, marker formats (`// AC:`, `// SCENARIO:`, `TODO(impl-...)`).
- `INTEGRATIONS.md` — external services and contracts.
- Topic-specific files as needed: `AUTH.md`, `PERSISTENCE.md`, `OBSERVABILITY.md`, etc.

Every agent **reads** `.architecture/`. Only the architect writes.

## Code markers — quick summary

The intent of every feature lives in two marker conventions, declared in `.architecture/CONVENTIONS.md`:

- **`// AC: <criterion>` + `// TODO(impl-<feat>, ac-<NNN>)` + `panic("not implemented")`** — inlined by the architect during scaffolding above each scaffolded body that maps to an acceptance criterion.
- **`// SCENARIO: <narrative>` + `// TODO(impl-<feat>, scenario-<NNN>)` + `t.Skip("not implemented")`** — inlined by the PM in passe 2 inside business test skeletons within `pm_test_territories`.

`<NNN>` is local to the feature, zero-padded to three digits, starting at `001`. Stable for the feature's lifetime.

**Detailed conventions, full lifecycle, and strict format rules live in `markers` skill.** Load when you need the exact format (architect during scaffolding, PM in passe 2, red and e2e-tester locating their work, reviewer pass 2 verifying alignment).

## Decisions and ADRs — quick summary

Two distinct stores:

- `.adrs/` — strategic ADRs only. Multi-feature, project-direction. Architect writes.
- `.decisions/` — tactical or strategic DECISIONS, with two-zone frontmatter (zone author + zone review) and a review lifecycle. Architect writes strategic. Green writes tactical under R2 strict rules.

Every commit modifying `.decisions/` carries `Authored-By:` trailer (R6). Tactical DECISIONS by green are surfaced in `RETRO.md decisions_to_statue:` and statued by the architect at the start of the next sprint.

**Format details, R2 strict rules, R6 three-level defence, and the architect's confirm/reformulate/supersede protocol live in the `decisions-and-adrs` skill** — loaded by architect, green, and sprint-planner only. Other agents read DECISION/ADR files freely without that skill.

## Features (.features/)

`INDEX.md` schema:

```markdown
| Slug                | Status      | Complexity     | Priority |
|---------------------|-------------|----------------|----------|
| auth-login          | ready       | architectural  | 1        |
| audit-log           | ready       | standard       | 2        |
| rename-user-field   | ready       | mechanical     | 3        |
```

`<slug>/FEATURE.md` — co-authored:

```markdown
---
title: <feature-slug>
status: ready
mechanical: false       # set by architect at end of scaffolding (R1)
# mechanical_rationale: <only if mechanical: true>
---

# Why                   <-- PM
# Context                <-- PM
# User journey           <-- PM
# Out of scope           <-- PM
# Open questions         <-- PM

## Complexity            <-- architect (with PM input)
<mechanical | standard | architectural>

## Complexity rationale  <-- architect

## Relevant decisions    <-- architect
- [.decisions/DECISION-051-...](...) — short reason
- [.adrs/007-...](...) — short reason
```

The architect adds **only** the `mechanical:` and `mechanical_rationale:` frontmatter fields and the `## Complexity`, `## Complexity rationale`, `## Relevant decisions` body sections. The PM owns everything else.

## Tasks — by code marker (no TASK*.md files)

Every red/green/e2e task corresponds to one `TODO(impl-<slug>, ac-<NNN>)` or `TODO(impl-<slug>, scenario-<NNN>)` marker in the code. The agent locates its work via `grep`.

There are **no** `TASK.md`, `TASK-red.md`, `TASK-green.md`, `SCAFFOLD.md`, or per-feature `TASKS.md` files. Anyone tempted to create one should stop — the v2 convention is markers in code, not prose intermediaries. Spec isolation is preserved by discipline.

### Pipeline routing by complexity

The sprint-planner routes per the `task-complexity-routing` skill:

- `mechanical` → **mono-agent task**. Single line in SPRINT.md execution plan. No red/green pair.
- `standard` → **reduced pipeline**. Architect scaffolds → PM passe 2 (if `mechanical: false`) → red → green → e2e-tester (if `mechanical: false`) → reviewer.
- `architectural` → **full pipeline**. Same as standard plus a mandatory strategic ADR before scaffolding starts.

`SPRINT.md` `## Routing decisions` section documents the choice per feature.

### Task types

- **Architect scaffold** (one per feature, first): inlines `// AC:`, scaffolds test skeletons, sets `mechanical:`.
- **PM passe 2** (one per non-mechanical feature): inlines `// SCENARIO:` in test skeletons.
- **Red task** (one per `// AC:` marker in scope): writes failing assertions.
- **Green task** (one per red task, paired): implements the body.
- **E2E task** (one per `// SCENARIO:` marker in scope, only on non-mechanical features): translates `t.Skip` into real e2e.
- **Feature REVIEW** (one per feature): reviewer's three passes, signs off `done` in INDEX.md.
- **Sprint REVIEW** (one per sprint): reviewer's cross-cutting checks.
- **Sprint retro** (one per sprint): sprint-planner generates `## Metrics` + YAML.
- **Architect DECISION-statuing** (when previous retro has `decisions_to_statue:` non-empty): Wave 1 task in the new sprint.

## Reviews (.features/<slug>/REVIEW.md and .sprints/SPRINT_00X/REVIEW.md)

The **reviewer** agent produces these. Two sections per file:

- `## Findings` — the reviewer's three passes (DoD via `scripts/check.sh`, Scenarios narrative-vs-tests, Security checklist).
- `## Human override` — human-only, strict 5-field format (R3). Empty by default.

**Detailed three-pass procedure, sprint-level cross-cutting checks, and `## Human override` format live in the `reviewer.md` agent spec.** The skill provides only the high-level summary and R3 below.

## Sprints (.sprints/)

- `INDEX.md` — sprints with start/end dates and status.
- `SPRINT_00X/SPRINT.md` — focus, features, execution plan as todo list **with code markers**.
- `SPRINT_00X/REVIEW.md` — sprint review checklist.
- `SPRINT_00X/RETRO.md` — retrospective (YAML frontmatter + `## Metrics` by sprint-planner + `## Reflection` by human).
- Sub-sprints `SPRINT_00X-Y` — micro-work that can't wait (helper coverage, tooling).

### Scope: single source of truth — ABSOLUTE RULE

Sprint scope (which features and tasks are in flight) lives in **one place only**: `.sprints/SPRINT_00X/SPRINT.md`. Every other artifact references it without duplicating.

| Artifact                                  | Role re: scope                                                            |
|-------------------------------------------|---------------------------------------------------------------------------|
| `.sprints/SPRINT_00X/SPRINT.md`           | **Source of truth.** Lists features in scope, wave graph, parallelization plan, agent assignments, code markers. |
| `.features/INDEX.md`                      | Backlog. `status: in-progress` is set for features currently in `SPRINT.md` scope, but `INDEX.md` does not list which sprint or which markers. |

Rules:

- The sprint-planner edits `SPRINT.md`. No other agent edits it.
- A change to scope mid-sprint (added unplanned task, descoped feature) is made in `SPRINT.md` first; `.features/INDEX.md` reflects derived status only.

**RETRO.md YAML schema, sub-sprint helper-coverage protocol, and tooling-extension routing live in the `sprint-planner.md` agent spec.**

## Bugs (.bugs/)

`bug-detective` agent (sonnet, on-demand) investigates. Writes `.bugs/<bug-id>.md` with classification (implementation-bug / spec-bug / architectural-bug). Does **not** propose the fix.

The sprint-planner reads the report and routes:

- **implementation-bug** → corrective task `<slug>-T<NNN>-bugfix` (red reproduces as failing test, green fixes).
- **spec-bug** → `.questions/` for PM and/or architect. PM extends `# User journey`, architect revises `// AC:` and re-scaffolds.
- **architectural-bug** → architect amends or supersedes a DECISION / ADR. No corrective task until the decision layer is consistent.

Bug-detective is post-mortem; spec isolation rules don't apply to its reads (everything is committed).

## Blockers (.blockers/SPRINT_00X/)

- Multiple solutions as a checklist.
- **Always require human input.** Affected teammates stop.

## Questions (.questions/SPRINT_00X/)

```markdown
---
id: Q069
phase: planning              # prep | planning | execution
raised_by: architect
raised_on: 2026-04-22
references: [auth-login, TODO(impl-auth-login, ac-001)]
blocking_scope: planning     # feature-DoR | sprint-kickoff | task | sprint | none
---

# Question
## Suggested resolutions
- [ ] option A — ...
- [ ] option B — ...
## Answer
[free text, written by the human or — for technical-only questions — by the architect]
```

Phase semantics:

- `prep` — drafted while writing FEATURE.md. Blocks the feature, not the sprint.
- `planning` — raised while authoring SPRINT.md. Blocks sprint kickoff.
- `execution` — mid-sprint. Default `blocking_scope: task` (only the task waits); `sprint` if the question reveals a missing DECISION (rare, triggers planner pause).

## Disputes (.disputes/SPRINT_00X/)

One file per disputed task, named after the marker:

```
.disputes/SPRINT_00X/TODO_impl-auth-login_ac-001.md
```

The sprint-planner decides citing **only public artifacts** (the inlined `// AC:`, `// SCENARIO:`, FEATURE.md, ARCHITECTURE.md, DECISIONS, ADRs, scaffolded code, committed tests). There are no private specs to read in v2.

**Decision types A–G, full arbitration procedure, hat-switching mono-assistant safeguard, and acknowledgement protocol live in the `sprint-planner.md` agent spec.** Agents that may raise disputes (architect, red, green, e2e-tester) cover their dispute-raising procedure in their own spec.

## Tooling feedback (.tools/<tool-name>/)

Friction reports for tools (`go-surgeon`, `scaffor`, the workflow itself). Bug reports or improvement suggestions. Template-evolution routing (blocking vs non-blocking) is detailed in the `sprint-planner.md` spec under retro processing.

---

# Transverse rules R1 → R6

These rules cross-cut the workflow. Brief here; details in the agent specs that own the rule.

## R1 — `mechanical:` flag (architect's exclusive authority)

The `mechanical: true|false` field in FEATURE.md frontmatter is set by the architect at end of scaffolding. The PM **never** touches it.

- `true` if every `// AC:` is wiring/plumbing pure (DI registration, DTO mapping 1-to-1, trivial adapter pass-through, schema migration, secret rotation, rename, dep bump, lint config, no-behaviour-change refactor).
- `false` as soon as any `// AC:` contains a business condition, an invariant, a calculation, an observable user interaction, or an effect on business state.

`mechanical_rationale:` mandatory if `true`, optional if `false`.

`check.sh`:

- Pre-`scaffolded` status: absence of `mechanical:` is OK.
- At status `scaffolded` or beyond: presence is mandatory; absence is a CI block.
- Modification of `mechanical:` by a commit whose `Authored-By:` trailer is not `architect`: CI block.

If `mechanical: true`: PM passe 2 is skipped, no `// SCENARIO:` markers expected, no e2e tasks planned. Reviewer pass 2 inverts (verifies zero `// SCENARIO:`).

## R2 — Green's tactical DECISIONS

Summary: green may write a tactical DECISION under four strict conditions (`scope: tactical`, `revisit: true` at creation, necessary to unblock current task, DECISION-NNN referenced in code or commit). The architect statues each at the start of the next sprint via a Wave 1 task.

**Full rules, statuing outcomes (confirm/reformulate/supersede), and CI enforcement live in the `decisions-and-adrs` skill.**

## R3 — `## Human override` strict format

REVIEW.md `## Human override` requires 5 fields per override block:

```markdown
### Override <NNN>

- **Finding overridden:** <path:line | finding-id>
- **Reason:** <1–3 sentences>
- **Decision reference:** <DECISION-NNN | null>
- **Date:** <YYYY-MM-DD>
- **Author:** <github username or name>
```

The reviewer **never** writes in `## Human override`. `check.sh` enforces format at pre-commit and CI. A security-finding override without a `Decision reference: DECISION-NNN` is rejected.

## R4 — Marker linter and `--no-verify` audit

Two levels:

**Pre-commit (bypassable with `--no-verify` technically):**

- `// SCENARIO:` outside `pm_test_territories` → block.
- `TODO(impl-...)` malformed → block.
- DECISION authored by green without `revisit: true` or with `scope: strategic` → block.
- Zone author modified post-creation → block.
- Zone review modified without all four fields → block.
- REVIEW.md `## Human override` malformed → block.
- Security override without `Decision reference` → block.
- `mechanical:` modified without `Authored-By: architect` trailer → block.

**CI (no bypass):**

- All pre-commit checks.
- Unresolved `TODO(impl-<slug>, ...)` on a feature `done` in INDEX.md → block.
- Tactical DECISIONS not statued after one sprint window → block.
- INDEX.md ↔ reality divergence → block.
- `--no-verify` commits on the sprint window → block.
- `review.reviewed_by` modified without `Authored-By: architect` → block.
- `mechanical:` flag missing on scaffolded+ features → block.

The reviewer's pass 1 invokes `scripts/check.sh --mode ci` and treats the output as findings.

## R5 — `.features/INDEX.md` lifecycle

Status posted by the agent that **finishes** the step, never a supervisor:

| Status         | Posted by                        | When                                                   |
|----------------|----------------------------------|--------------------------------------------------------|
| `todo`         | PM (passe 1)                      | FEATURE.md drafted with narrative                      |
| `scaffolded`   | architect                         | Code scaffolded, `// AC:` inlined, `mechanical:` set    |
| `ready`        | PM (passe 2) or architect (if `mechanical: true`) | After SCENARIO inlining or directly if mechanical |
| `in-progress`  | sprint-planner                    | Feature enters active SPRINT.md                         |
| `done`         | reviewer                          | After REVIEW.md feature-level passes all three passes   |
| `blocked`      | any agent                         | When a `.blockers/` entry references the feature        |

`check.sh` verifies:

- `done` with leftover `TODO(impl-<slug>, ...)` → block.
- `ready` without scaffolding evidence (no AC markers, no `mechanical:` flag) → block.
- `in-progress` without an active SPRINT.md mentioning it → block.

## R6 — `.decisions/` zone review and `Authored-By:` trailer

Three-level defence (pre-commit YAML format → CI git-blame ↔ trailer cross-check → reviewer pass DoD sanity check). Mandatory trailer values: `architect` (for architect's writes), `green` (for green's tactical DECISIONS only).

**Full three-level defence, declarative-vs-cryptographic discussion, and commit examples live in the `decisions-and-adrs` skill.**

---

# Skill loading by role

| Skill                                    | Loaded by                                                                                            |
|------------------------------------------|------------------------------------------------------------------------------------------------------|
| `agile-project` (this file)              | every agent                                                                                          |
| `markers` skill    | every agent that touches markers — architect, PM, red, green, e2e-tester, reviewer, sprint-planner   |
| `task-complexity-routing`                | product-manager, architect, sprint-planner                                                           |
| `decisions-and-adrs`                     | architect, green, sprint-planner, reviewer (pass DoD audit), bug-detective (architectural-bug class) |
| `tdd-pattern`                            | red, green                                                                                           |

bug-detective is the only agent that doesn't load markers reference (it reads `// AC:` from committed code post-mortem, no need for the format spec).

`tdd-pattern` is loaded only by red and green because spec-isolation discipline, in-scope/out-of-scope, and the mono-assistant safeguard apply only to the live red/green pair. Other agents operate outside that flow.
