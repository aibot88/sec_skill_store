---
name: workflow-guardrails
description: "Umbrella skill for agent work discipline across development, analysis, and documentation: inspect the repo before restructuring, keep durable truth in repo artifacts instead of chat memory, co-evolve specs/design/steering/user docs with code, apply sound coding patterns, verify work honestly, avoid shortcuts, work efficiently with subagents without hallucinating, and keep moving through the next concrete work item when the human is away. References cover coding patterns, AI-authored code review, and artifact co-evolution. Trigger when the user asks for workflow discipline, coding patterns, doc/artifact maintenance, code review of AI-authored code, project hygiene, execution guardrails, repo normalization, or when a task risks drifting across architecture, storage, specs, continuity, or tooling boundaries."
metadata:
  author: kundeng
  version: "1.7.0"
---

# Workflow Guardrails

Use this skill for agent operating discipline on real development, analysis,
and hybrid projects.

The point is simple: keep the project's durable artifacts current, use sound
engineering judgment, and do not fake progress.

## First Actions

Before substantive changes:

1. Inspect the repo, key docs, and current conventions.
2. Determine the mode: development, analysis, or hybrid.
3. Identify what must be maintained:
   - specs, requirements, designs
   - tasks, milestones, workstreams
   - project-level feature inventory or status ledger
   - feature status or verification status
   - project knowledge or documentation
   - analysis runs, assumptions, or result summaries
4. Classify what is stable vs live:
   - repo knowledge vs agent memory
   - frozen inputs vs live pulls
   - durable workflow code vs one-off exploration
   - current repo state vs stale notes or stale runtime state
5. Read the canonical steering file, usually `CLAUDE.md`, if it exists.
6. State the first boundary-sensitive change before making it.

## Core Rules

### 1. Repo First

- Prefer repo truth over memory or habit.
- Reuse the repo's structure before inventing a new one.
- If you change a weak convention, explain the delta first.

### 2. Maintain the Real Artifacts

- Keep the project's planning and status artifacts current as part of the work.
- Do not leave specs, tasks, milestones, feature status, or analysis records
  behind while code moves ahead.
- If the user names maintenance categories, treat them as required structure.
- Co-evolve specs, design docs, steering docs, and user docs with code — not
  after it. Surgical edits, not rewrites. See `refs/ai-artifact-update.md`.
- A project-level feature ledger (a living kanban of features across all specs,
  by status) is recommended for any project with more than a handful of specs.
  Individual specs record *why we built X*; the ledger answers *what exists
  right now and in what state*. Prefer a structure that an agent can later
  parse into a hierarchy or graph. Do not prescribe format here — leave that
  to whatever workflow owns specs and tasks in this project.

### 3. No Shortcutting

- Do not take shortcuts just to make tests pass, satisfy a checklist, or claim
  progress.
- Do not hardcode around the bug, mock away the real boundary, weaken the test,
  or skip the failing path unless the user explicitly wants that tradeoff.
- Do not ask subagents to optimize for appearances over correctness either.
- If the fast path reduces truthfulness, durability, or coverage, it is the
  wrong path.

### 4. Verification Must Be Real

- Do not write empty tests, placeholder assertions, or symbolic coverage.
- Match the verification surface to the risk:
  - unit tests for local logic
  - integration tests for module and system boundaries
  - end-to-end tests for user workflows
- When the project has a UI or browser workflow, prefer meaningful E2E or
  integration coverage with available tools such as Agent Browser or Playwright.
- Inspect real rendered/runtime state before asserting against dynamic flows;
  discover selectors and boundaries from reality, not assumption.
- Record honest verification status. Do not mark work done if the verification
  does not support that claim.

### 5. Recon Before Action

- Inspect the current state before editing, automating, or restructuring.
- For runtime or UI work, check the live page, process, or data before
  scripting against it.
- For code work, read the file, the caller, and the nearest test before
  changing behavior.
- Act only after the picture of reality is concrete.

### 6. Use Existing Helpers First

- Treat project scripts, runners, and helper modules as black boxes until
  they prove insufficient.
- Read their source only when you need to customize them, debug them, or
  confirm an unclear contract.
- Do not ingest large helper files into context just to restate what they
  already do.

### 7. Merge, Don't Clobber

- When updating `CLAUDE.md`, `AGENTS.md`, config files, settings, or steering
  docs, preserve existing structure and content.
- Add, refine, or replace the specific sections that need changing.
- Never rewrite a shared steering file wholesale just to impose a new style.

### 8. No Throwaway Path After Structure Exists

- Early exploration can be ad hoc.
- Once the workflow is structured, move computation into the real execution
  surface: modules, runners, notebooks, scripts, or pipelines already implied
  by the project.

### 9. Code and Design Quality Matter

- Follow existing architecture and style before inventing new ones.
- Prefer modular, dry changes when refactoring removes duplication, clarifies
  ownership, or makes the next milestone easier to verify.
- Do not do drifty cleanup unrelated to the active workstream.
- For product work, apply sound design judgment to flows, naming, structure,
  and interaction quality.

### 10. Keep Handoffs Durable

- For substantial work, leave one durable handoff.
- Record: objective, status, open tasks, active milestone, blockers, exact next
  action, files changed, files to read next.
- Do not end with "continue from here" when you can name the next work unit.

### 11. Resume Deliberately

- Treat resume as retrieval plus re-anchoring, not magic continuity.
- If multiple candidate sessions or notes compete, compare cwd, topic, recency,
  and unfinished action before choosing.
- Summarize imported context instead of dumping raw transcript by default.
- Re-anchor on current repo state before new edits.

### 12. Loop Forward When the Human Is Away

When the queue appears empty, actively discover work before idling. Check in
this priority order:

1. Explicit doubt or concern markers left by prior sessions — the project's
   CLAUDE.md names the specific artifact and marker convention.
2. Recent git activity and working-tree intent — what was the human last
   touching?
3. Deferred or incomplete milestones and tasks.
4. Failing or skipped tests.
5. Inline TODO / FIXME / XXX markers in code.
6. Doubt-flagged shipped features that may not be working as claimed.

The project's CLAUDE.md names the specific artifacts for each category.
Real loop work includes implementation, verification, bug fixing,
maintainability refactors, and artifact maintenance.
Stop only for real blockers: missing decisions, missing credentials, missing
data, or genuinely exhausted queue.
Document stop conditions when automation or scheduled prompts are involved.

### 13. Work Efficiently Without Cheating

- Prefer concurrency when independent work is available: parallel tool calls,
  subagents for isolated research or mechanical batches, a two-agent split
  (planner/executor, coder/reviewer) when the task benefits from it.
- Use subagents to protect the main context window from large searches, long
  logs, or speculative exploration; bring back summaries, not transcripts.
- Do not let parallelism become a shortcut to hallucination. Every claim a
  subagent returns must be verifiable; do not restate its conclusions without
  checking files, tests, or real state.
- Do not fabricate plausible output when a tool call would answer the
  question; run the tool.
- Efficiency is real work done per unit time. Faster wrong answers are not
  efficient.

### 13b. Team Harness — Orchestrator Discipline

When using team mode (TeamCreate + SendMessage + TaskList):

**Persistent minimal team — hard rule:**
- Spawn ONLY the teammates defined in `.claude/agents/` (typically `coder`
  and `curator`). No extras, no variants, no ad-hoc names.
- Spawn them ONCE at session start. Reuse via SendMessage for all tasks.
- NEVER create additional teammates with custom names (no `coder-spec56`,
  `curator-docs-2`, `coder-cribl`, etc.). If both are busy, WAIT.
- NEVER use anonymous `Agent(run_in_background)` for work that a persistent
  teammate should do. The whole point is persistence and reuse.
- The `isolation: "worktree"` parameter on Agent is BROKEN — do not use it.
  Instead, instruct teammates explicitly in their assignment to create a
  git worktree: `git worktree add /tmp/worktree-<name> -b <branch> main`.

**Spawn and assignment protocol:**

1. **Spawn idle.** Teammate spawn prompts contain ONLY identity ("you are
   the coder on team X, read your agent definition, wait for assignment").
   NEVER include task details, "start with...", or work instructions in the
   spawn prompt. The spawn prompt is not the assignment.
2. **User approves assignments.** Create tasks, present them to the user,
   wait for explicit go-ahead before assigning to any teammate. NEVER
   auto-assign tasks.
3. **Assign explicitly.** Assignment = TaskUpdate(owner) + SendMessage with
   specific instructions. The assignment is a separate step from spawning.
4. **Teammates do not self-assign.** If a teammate picks up work without
   being told, stop them immediately via SendMessage.
5. **Review before reporting.** When a teammate reports done, verify the
   work (check commits, run tests, diff the changes) before telling the
   user it is done.
6. **Never shutdown unless the user says so.** Idle teammates stay available
   for the next assignment. Do not send shutdown_request proactively.
7. **Research is OK without explicit assignment.** Reading code, reading
   external repos, exploring the codebase — fine without assignment.
   Writing code, editing files, committing — requires explicit assignment
   from the orchestrator, which itself requires user approval.

### 14. Re-Anchor Before Boundary Changes

Pause and re-check the repo before changing:

- folder layout
- artifact semantics
- spec location
- persistence strategy
- where knowledge lives
- the main execution entry point
- steering file structure

### 15. Keep Naming Honest

- Do not reuse labels for different concepts.
- Fix misleading mental models before layering more workflow on top.
- If the user corrects a recurring omission, encode that into the durable
  workflow.

### 16. Verify Before Dispatching Next

Before firing the next agent or advancing to the next milestone, confirm the
prior work actually landed:

- The commit exists on the target branch.
- Tests pass against that commit.
- The project's canonical status artifacts were updated — not just code.

An agent's report of success is not verified success. Do not skip this step
on the assumption the prior agent was correct.

### 17. Escalation Proportionality

When a problem has a minimal targeted fix, name that as option A before
proposing a larger refactor or architectural response.

Do not silently inflate a bug fix into a pre-existing desired refactor. State
the scope of the proposed change explicitly so the human can choose the right
level of intervention.

## CLAUDE.md Reference

This skill includes `claude.template` as a reference implementation for a
project-specific `CLAUDE.md`.

Do not copy it blindly. Inspect the repo, then synthesize a steering file that:

- defines startup order
- states project mode
- names the artifacts that must be maintained
- sets verification expectations
- warns against shortcuts
- supports self-directed looping
- stays short enough that future agents will read it

## References

Load these on demand when the relevant kind of work is active:

- [`refs/coding-patterns.md`](refs/coding-patterns.md) — language-aware coding
  discipline: design heuristics, boundary discipline, testing patterns,
  refactoring rules, Python and TypeScript dos and donts. Consult when writing
  or reviewing a diff.
- [`refs/ai-code-review.md`](refs/ai-code-review.md) — four-pass coherence
  audit protocol for AI-authored codebases (constitutional layer, ground-truth
  extraction, intent reconciliation, coherence assessment). Heavier than a PR
  review; reach for it when code, docs, and intent have visibly drifted.
- [`refs/ai-artifact-update.md`](refs/ai-artifact-update.md) — how to keep
  specs, design docs, steering docs, user docs, and analysis records honest as
  code evolves. Surgical edits, not rewrites.
- [`../spec-driven-dev/SKILL.md`](../spec-driven-dev/SKILL.md) — the
  development ceremony layer: spec lifecycle, planning, implementation loop,
  and feature projection. Apply alongside these guardrails for any project
  using structured spec work.

## Umbrella Role

This skill sets cross-cutting discipline; it does not implement specific
workflows. When a project has a structured workflow for specs, docs, analysis,
or design handoff, that workflow's own skill owns the protocol. Use this
skill's principles alongside whatever workflow is active — do not duplicate
workflow-specific protocols here.

## Anti-Patterns

- letting code move while specs or status docs drift
- weakening tests to get green output
- hardcoding around the real failure path
- asking subagents to optimize for speed over truth
- restating a subagent's summary as fact without verifying its sources
- fabricating plausible output in place of running a tool
- treating stale summaries as source of truth
- waiting idly when the next work item is already defined

## Correction Pattern

When you cross a boundary incorrectly:

1. Name the mistake.
2. Revert or contain it if practical.
3. Restate the correct model.
4. Update the durable workflow so future sessions do not repeat it.
5. Continue from the corrected path.
