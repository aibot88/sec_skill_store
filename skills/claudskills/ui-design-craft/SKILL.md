---
name: ui-design-craft
description: Use when designing, polishing, prototyping, or reviewing user-facing UI, frontend screens, visual systems, interaction prototypes, slide decks, motion/effects, artifact handoff, or anti-slop visual quality. Trigger for "make this UI look better", "design a dashboard", "create frontend mockup", "prototype this flow", "author a design system", "make a deck", "add motion", "prepare handoff", or "review visual craft". Do not use for pure accessibility audits without visual design work; use ux-accessibility-heuristics for that.
license: MIT
---

# UI Design Craft

Design and ship interface artifacts that feel grounded, specific, usable, and
visibly intentional. Provenance lives in `skill.json`; this file is runtime
routing only.

## Core Principle

**Context before craft, show early, iterate small.** Read the product,
system, code, screenshots, and source before inventing visuals. Put a runnable
artifact in front of the user as soon as it can communicate direction.

## Activation

- **Bare invocation** (`"use ui-design-craft"`, `"UI designer"`, `"start"`):
  load `references/starter-scenarios.csv` and `references/use-case-registry.csv`,
  then show the use-case menu with the named starter scenarios on top (each
  pre-routes use-case + mode) and offer the full mode choice. Wait. No file
  inspection, network calls, or writes.
- **Concrete invocation** with use case inferable: proceed in Guided Draft
  unless the user requests Autopilot or Grill Me.
- **Ambiguous concrete invocation**: ask one blocker question about audience,
  format, design system, or variation axis before editing.

## Modes

Three shared modes — Guided Draft (default), Autopilot, Grill Me — set
depth-vs-speed up front. Canonical contract in
[`references/modes.md`](./references/modes.md) (sourced from
`skills/_shared/modes.md`). UI-design-craft specifics:

- **Guided Draft (default):** ask one optionized question round only when the
  answer changes format, audience, design-system binding, or variation count;
  then design, show early, verify, and state assumptions.
- **Autopilot:** proceed from available context; make conservative calls;
  stop only for missing assets, legal/IP risk, destructive edits, or
  credential-bound tooling.
- **Grill Me:** use open questions one at a time to lock audience, system,
  content, interaction, motion, and handoff decisions before drafting.

## Workflow

1. **Route.** Load `references/use-case-registry.csv`; pick one or more of:
   `product-ui`, `design-system`, `prototype`, `deck`, `motion-scene`,
   `host-handoff`, `quality-review`.
2. **Load details.** Load only the registry row's `detail_files` and mapped
   templates. If multiple rows apply, prefer the smallest set that covers the
   deliverable.
3. **Ground the work.** Inspect the brief, product vocabulary, design system,
   tokens, existing components, assets, screenshots, and relevant files.
   If no system exists, use `references/brief-and-format.md` and state the
   chosen aesthetic commitments.
4. **Ask or decide.** Ask one focused question round when blocked. If the user
   says "decide for me", decide and record the call in the artifact or plan.
5. **Plan.** Use `templates/design-brief.md` plus the use-case template to
   name audience, format, constraints, direction, variation axes, and checks.
6. **Show early.** Start with layout skeleton, type/color direction, and honest
   placeholders. Open or surface the artifact as soon as it runs.
7. **Build.** Compose layout, typography, color, content, components, motion,
   and host protocol support in that order. Avoid silent design-system
   invention.
8. **Verify.** Check load, console, responsive viewports, hover/focus/press,
   overflow, reduced motion, editability, export needs, and the anti-slop pass.
9. **Hand off.** Summarize files changed, decisions, verification, remaining
   risks, and any prepared host/export instructions.

## Operational Memory

For recurring work, use explicit workflow artifacts first:
`templates/workflow-state.json` copied into the target repo or an approved
host-provided operational memory surface. Store only non-secret run defaults:
mode, output format, artifact paths, viewport set, and accepted design-system
choices. Do not create hidden memory files unless the environment policy
explicitly allows it, and never store private user facts or identity data.

## Subagent Dispatch

Use subagents only when the host/session permits and independent critique helps:
one visual-craft reviewer, one user-task reviewer, and one implementation/handoff
reviewer. Do not delegate tiny tweaks or work requiring private credentials.
If subagents are unavailable, run the same three lenses sequentially using
`references/subagent-dispatch.md`.

## Output Requirements

Every output names the user/audience, chosen format, design-system binding or
from-scratch commitments, files/artifacts produced, verification performed, and
the anti-slop checks applied. Visual artifacts must be runnable or viewable,
not merely described.

## Reference Map

- `references/use-case-registry.csv` - use-case router.
- `references/starter-scenarios.csv` - named worked examples for bare invocation.
- `references/modes.md` - Guided Draft / Autopilot / Grill Me contract (shared).
- `references/*.md` - routed craft, workflow, host, and review playbooks.
- `templates/*.md` - repeatable brief, plan, system, deck, prototype, and
  review outputs.
- `templates/workflow-state.json` - resumable state skeleton for long runs.
- `evals/*` - activation, scenario, and static checks.
