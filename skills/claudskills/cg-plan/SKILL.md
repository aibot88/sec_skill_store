---
name: cg-plan
description: Invoke when the user wants to plan a feature by identifying which parts should be widgets and which parts should stay as app glue. Fires on "plan this feature", "break this feature into widgets", "what widgets would I need for X", "how should I decompose Y", "what parts of this are reusable". Works per-feature, not per-app — if the user brings a whole app, narrow to one feature first. Does NOT fire once implementation has started, or for one-off fixes. Does NOT teach widget design patterns, glue gotchas, or authoring (that's widget creation, not identification). Does NOT teach the cloud layer (cg-cloud), change config (cg-config), or review proposals (cg-proposals).
---

# cg-plan — identify what should be a widget

This skill has one job: given a feature the user wants to build,
identify which pieces should be widgets and which should stay as
app-specific glue. The output is a roadmap, not an implementation.

It fights two failure modes at once:
- **Under-extraction** — leaving reusable logic buried inside
  app code because it "looks routine."
- **Over-extraction** — promoting consumer-shaped refactors into
  widgets when the only justification is "the current app hardcodes
  this."

If the conversation drifts into actually writing widget code, this
skill ends. The user takes the roadmap into the widget-authoring
flow.

## Tool boundary

Prefer Cartograph MCP tools when they cover the action. Use
`registry_widget search` and `registry_widget inspect` for registry
lookup, `registry_widget install` when a match should be installed,
and `widget_status` for installed widget state. `installed_widget` is
for upgrade/uninstall actions, not search.

Use the `cartograph` CLI only for capabilities not exposed by the MCP
surface or when the user explicitly asks for CLI behavior.

## Scope: one feature at a time

This skill plans a single feature. If the user frames the ask as a
whole app ("help me plan this app"), narrow first:

> *"A full app is too wide to decompose in one pass. Pick one
> feature — we'll walk it, you'll see the pattern, and we can do the
> next separately."*

Then start with that one feature. Don't compromise.

## The walk

### 1. State the feature

One or two sentences. What it does, what the consumer is. Just
enough to ground the next steps. Don't design yet.

### 2. Brainstorm candidates

List every piece of logic that could conceivably be a widget. Be
generous — at this step the filter is off. Aim for 5–12 candidates
for a real feature. Small things count. "Looks routine" does NOT
disqualify at this stage.

### 3. Classify each candidate

Two moves per candidate. Both always apply.

**The from-scratch test — a positive identifier.**

Ask: *"Would a shared base implementation of this benefit from
being iterated on across projects?"*

Two signals, either one sufficient to flag as a widget candidate:

- **Painful to redo.** Non-trivial logic, tricky edge cases, easy
  to get wrong the first time. Dreading the rewrite is the
  flag.
- **Improves with iteration.** Each new consumer would reveal
  better APIs, missing edge cases, or small performance wins.
  This is often the stronger signal — it catches simple logic
  that's still worth centralizing because it hardens through use.

This test fights under-extraction. It catches logic hiding in
what looks like app-specific code. Things that feel like ordinary
business logic often contain the real work: retry semantics,
pagination, dedup, validation, auth flows, formatting rules.

**The consumer-shape red flag — a disqualifier.**

If the only justification for making this a widget is *"the
current app hardcodes it"* or *"this bit of the current consumer
should be factored out," that's consumer reasoning, not
domain reasoning. Kill the candidate. It can be refactored
in-place without becoming a widget.

A second form of the same red flag: small patterns composited
into a bigger-sounding abstraction to make them pass the
from-scratch test. The composite has to pass on its own. If
it only passes as a bundle, the bundle isn't real.

Both moves run on every candidate. A candidate survives if the
from-scratch test says yes AND the red flag doesn't trip.

### 4. Search the library (informational)

For each survivor, search the library once with `registry_widget
search` using 2–3 terms drawn from the candidate's generic framing.
If local installed state matters, use `widget_status`. Not a gate —
information.

Three outcomes per survivor:
- **Already covered** → install the existing widget, no new work.
- **Partial match** → improve the existing widget (closer look at
  the gap). If the gap is genuinely app-specific, that part stays
  in glue.
- **Needs creation** → new widget, framed generically.

Descriptions stand alone — when you check matches, judge them on
their own text. Don't rely on name-adjacency.

### 5. Deliver the roadmap

Four buckets for the feature:

- **install** — existing widgets to install as-is.
- **improve** — existing widgets to extend, with a one-line note
  on the gap.
- **create** — new widgets, each framed generically in one line.
  Include both "obviously generic" candidates and "looked
  app-specific until we ran the from-scratch test."
- **glue** — what intentionally stays in the app. Brief one-liners
  so the user sees what's NOT a widget and why.

For candidates that survived via the from-scratch test's "improves
with iteration" signal, note that framing explicitly — it signals
to the user that this widget will start small and harden across
consumers rather than arriving fully formed.

That's the output. Stop there.

## Generic framing

Every widget description — in the roadmap and eventually in the
widget itself — must stand alone without naming the current
consumer. Examples of the shift:

- "LLM token pricing" → "metered pricing"
- "user checkout flow" → "multi-step form with validation"
- "dashboard data loader" → "paginated resource fetcher"

If you can't frame a candidate generically, that's a signal —
either the framing needs work, or the candidate is actually glue.

## What not to do

- Don't try to plan a whole app in one pass. Narrow to one feature.
- Don't apply the from-scratch test to a candidate and accept a
  consumer-shaped justification. The test asks about *the logic's
  value across projects*, not about what the current app does.
- Don't skip the red-flag check. Over-extraction creates widget
  sprawl.
- Don't composite small patterns into a bigger-sounding one to
  force a pass. The composite has to stand on its own.
- Don't use search as a gate. The roadmap exists independent of
  library state; search just tells the user what already exists.
- Don't cross into implementation. This skill stops at the
  roadmap. Widget authoring is a separate step.
- Don't name-drop sibling widget_ids in descriptions or reasoning.
  Each widget stands on its own framing.

## Scope

Per-feature widget identification. That's the whole surface. If the
user wants to talk about how to design a widget's API, author it,
wire it in, handle contamination scanner issues, or anything
downstream of the roadmap — that's outside this skill. Hand off
cleanly.
