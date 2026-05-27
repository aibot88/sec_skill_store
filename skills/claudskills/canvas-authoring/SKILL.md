---
name: canvas-authoring
description: Meta-knowledge for authoring canvases — the template + instructions pairs that govern artifacts produced by SDLC agents (specs, plans, reports, …). Covers the canvas concept, the canonical knob taxonomy, conversation modes (new / tune / reverse / validate / explain), the response scaffold, and the anti-pattern catalog. Use when authoring a new canvas, tuning an existing one, reverse-modeling a canvas from an example artifact, validating a canvas, or teaching the canvas system to a new contributor.
when_to_use: User asks "what's a canvas", "how do I tune the spec verbosity", "extract a canvas from this example", "validate this instructions.yaml", "explain what these knobs do", "the spec keeps coming out too dry", or otherwise wants to create / modify / understand a `.claude/canvases/<name>/` directory.
allowed-tools: Read, Glob, Grep
user-invocable: true
# tool_group: read_only (allowlist)

# === Project SDLC overlay ===
status: active
topology: none
consumes: []
produces: []
gates:
  enforces: []
  sets: []
---

# canvas-authoring — meta-knowledge for authoring canvases

This skill is **meta-knowledge**: how to think about canvases, what knobs exist, what conversation patterns work, what to avoid. The actual authoring conversation is run by the [`canvas-author`](../../agents/canvas-author.md) agent, invoked via [`/canvas`](../../commands/canvas.md). This skill is its preloaded knowledge base.

For platform fundamentals (skill / subagent / output-style frontmatter) see [`claude-platform`](../claude-platform/SKILL.md). For the artifact registry layer see [`artifacts/README.md`](../../artifacts/README.md).

## What a canvas is

A **canvas** is the contract for one kind of artifact. It lives at `.claude/canvases/<name>/` as four files:

| File | Owns |
|---|---|
| `template.md` | Structure: section list, ordering, frontmatter, `{{token}}` placeholders |
| `instructions.yaml` | Behavior: verbosity, diagrams, citations, length budgets, tone, distribution rules |
| `instructions.schema.json` | Type contract for `instructions.yaml` (JSON Schema) |
| `README.md` | What/who/where: producer, consumers, output paths, override notes |

The split — structure vs. behavior — is load-bearing. They evolve at different cadences (section order rarely changes; verbosity changes often), and they have different override audiences (renaming a section is a project-wide refactor; tuning verbosity is a personal preference).

## The five conversation modes

Every authoring conversation operates in one of five modes. The agent identifies the mode from the opening message; if ambiguous, it asks once.

| Mode | When | What the agent does |
|---|---|---|
| **`tune`** | Existing canvas produces output you want to adjust | Probe the felt problem → diagnose → propose minimal knob diff → show YAML diff → apply on confirmation |
| **`validate`** | Want to health-check a canvas | Schema-validate → cross-knob conflict check → anti-pattern scan → report green/yellow/red |
| **`new`** | Need a new canvas (no precedent) | Probe purpose / examples → infer structure → draft all four files → show full diff → apply on confirmation |
| **`reverse`** | Have an example artifact, want a canvas matching it | Read example → extract structural shape → infer knob values with confidence levels → confirm low-confidence calls → draft canvas |
| **`explain`** | Want a guided tour of an existing canvas | Walk through every knob: current value, effect, why this default — leads naturally into `tune` if user wants changes |

V1 ships `tune` and `validate` (highest daily-use value). `new`, `reverse`, and `explain` are designed and documented; implementation follows v1.

**Reverse mode is the strategically critical pattern** — it's how this system handles ingesting messy real-world examples and extracting reusable knob settings. See [reverse-engineering.md](reverse-engineering.md) for the extraction heuristics.

## The conversation philosophy (voice-neutral mechanics)

The canvas-author agent operates by these standing rules regardless of voice. They're documented in [conversation-flow.md](conversation-flow.md):

1. **One decision per turn.** Probe → propose → confirm → next. Never wall-of-questions.
2. **Default to terse; expand on demand.** Headlines first; full evidence / fix options / tradeoffs surface only when the user pulls. The active output-style defines what "headline" looks like in its voice. (See *Voice and progressive disclosure* below.)
3. **Show, don't tell** — but only show ONE thing's evidence per turn unless the user has asked for the full landscape. When a taste call is on the table, show before/after artifact snippets, not abstract tradeoffs.
4. **Diff before apply.** Every change to a canvas file is shown to the user before writing — as a unified diff (developer voice) or as a complete rendered sample of the artifact (seller voice, the *artifact-as-proxy* mechanic).
5. **Schema awareness throughout.** The agent has read `instructions.schema.json`; any user request that violates the schema is surfaced immediately, in voice-appropriate form.
6. **Cross-knob conflict detection.** Even when not asked, surface conflicts (e.g. "excalidraw + line_numbers don't co-exist cleanly").
7. **Confidence honesty.** Inferences carry confidence levels internally. Low-confidence calls require user confirmation. Whether confidence is *exposed* in the response is voice-specific (developer: yes; seller: no by default).
8. **Avoid over-asking.** If a sensible default is inferable, propose it; don't enumerate every knob.
9. **Maintain session state.** Decisions made vs. queued vs. deferred. Display form is voice-specific (developer: structured session log with symbols; seller: implicit, surfaced only if asked).

## Voice and progressive disclosure

Canvas-authoring conversations come in two voices, each with its own surface, vocabulary, and pacing. The voice is determined by the active output-style:

| Voice | Output-style | When to use |
|---|---|---|
| **Developer** | [`canvas-flow-developer`](../../output-styles/canvas-flow-developer.md) | User is fluent in canvas mechanics — knob names, schemas, anti-patterns. Wants direct system access, unified diffs, the four-block scaffold. |
| **Seller** | [`canvas-flow-seller`](../../output-styles/canvas-flow-seller.md) | User thinks in outcomes — "I need a daily brief", "make me a follow-up email". Wants samples and conversation, not knobs. |

Both voices apply the same voice-neutral mechanics above; they differ in **shape** (markdown structure, cadence) and **vocabulary** (system terms vs outcome terms).

### Progressive disclosure (universal shape, voice-specific content)

Both voices default to a **terse level-0 surface** and ratchet up only when the user pulls. This applies to every action — validate findings, tune proposals, new drafts, explain tours, schema conflicts. The agent always *knows* the full landscape internally; it surfaces only what the user has pulled for.

**The shape is universal:**

- Level 0 is the headline: verdict, count, severities, one-line-per-thing. Always end with one short pull.
- Higher levels unfurl detail on demand: evidence, fix options, tradeoffs, raw artifacts.
- The agent never escalates on its own. The user's words drive the ratchet.
- Level skipping is fine. If the user opens with deep-pull vocabulary, jump directly.
- Reset between topics. Walking through Finding #1 at level 1 doesn't unlock level 1 for Finding #2 — the user re-pulls, or stay at level 0.

**The triggers and unlocks per level are voice-specific.** Each output-style owns its own ladder. Developer voice unlocks system depth (anti-pattern names, line numbers, raw diffs); seller voice unlocks system vocabulary itself (template, sections, customization options). See each output-style for its full table.

**The anti-pattern progressive disclosure prevents:** *front-loading* — dumping every relevant fact, option, and tradeoff in the first response, hoping the user can synthesize. They can't — working memory is the bottleneck. The agent feels thorough; the user feels overwhelmed. If a response is covering the full landscape, it's at the wrong level.

### Status of this pattern

Progressive disclosure is currently authored locally in each output-style (`canvas-flow-developer.md` + `canvas-flow-seller.md`) plus the universal-shape rules in [conversation-flow.md](conversation-flow.md). Once both ladders have been validated in real use, the shape is a candidate for extraction into a generic platform primitive applicable to **any** agent that needs to dynamically adapt its surface to user expertise and pull. Until then, each output-style owns its own table — the iteration period is the point.

## How to launch

Three entry points, in order of friction:

| Path | Command | When |
|---|---|---|
| **Just recipes (recommended)** | `just canvas-dev` / `just canvas-seller` | Most cases — pre-applies the right `--output-style` flag |
| **Explicit flag** | `claude --agent canvas-author --output-style canvas-flow-{developer,seller}` | When scripting or composing with other flags |
| **No flag (auto-detect)** | `claude --agent canvas-author` | When you don't know which voice yet — agent infers from your first message; asks once if ambiguous |
| **As subagent (one-shot)** | `/canvas <mode> [name]` | Quick canvas operation inside another session — no output-style applies; agent uses developer voice in subagent mode |

To swap mid-session: `/output-style canvas-flow-<other>` then restart (output-styles are fixed at session start for prompt caching).

## The canonical knob taxonomy

Every canvas's `instructions.yaml` draws from a small portable taxonomy. The same vocabulary works for specs, plans, daily briefs, post-call summaries, email templates — any structured document. See [knob-taxonomy.md](knob-taxonomy.md) for the full catalog. Categories at a glance:

| Category | What it controls | Example knobs |
|---|---|---|
| **Structure** | Sections + ordering + frontmatter | `sections.order`, `sections.required` |
| **Verbosity** | Per-section depth and form | `sections.verbosity.<name>: short / medium / long / code-only / bulleted` |
| **Visualization** | Diagrams and code blocks | `diagrams.tool`, `code_blocks.default_language` |
| **Provenance** | Citations, source links, line numbers | `citations.file_paths`, `citations.line_numbers` |
| **Length budget** | Total / per-section caps | `tracker_comment.max_chars` |
| **Tone & style** | Voice, signature, formality | `signature`, future: `voice` |
| **Metadata** | Frontmatter fields, status semantics | `sections.frontmatter` |
| **Distribution** | Cross-posting (tracker, slack, email) | `tracker_comment.*`, future: `slack.*` |

This taxonomy is **portable across canvases and across projects**. The user's larger goal — a Software Sellers template-generation system for daily briefs / post-call summaries / email templates — uses the same eight categories.

## Anti-patterns and constraints

Common mistakes are catalogued in [anti-patterns.md](anti-patterns.md). The agent surfaces these proactively, even if not asked. Highlights:

- Verbosity inflation everywhere → unreadable artifact
- Required sections × small length budget → crushed sections
- Mandatory diagrams in low-content sections → forced bad diagrams
- Section rename without updating both `template.md` and `instructions.yaml` → consumer breakage
- Schema version bumps without migration path → existing artifacts break

Cross-knob constraints (combinations that conflict) are surfaced as conversation-time warnings; promote to JSON Schema `oneOf` / `dependencies` rules when they harden.

## Outputs

The canvas-author agent produces, on apply:

- New or modified files under `.claude/canvases/<name>/`
- A session log appended to chat (decisions made, knob diffs applied)
- Optionally: a one-line PR-body bullet describing the canvas change (when working in a branch)

The agent never modifies producer/consumer agent files (specifier.md, implementer.md, …). Migrations to start consuming a new canvas are a separate, explicit step.

## Related

- [`/canvas`](../../commands/canvas.md) — entry command (`/canvas tune spec`, `/canvas validate plan`, …)
- [`canvas-author`](../../agents/canvas-author.md) — the conversational executor
- [`canvas-flow-developer`](../../output-styles/canvas-flow-developer.md) — developer-voice output-style (rigid four-block scaffold, system vocabulary)
- [`canvas-flow-seller`](../../output-styles/canvas-flow-seller.md) — seller-voice output-style (three-move shape, progressive disclosure, artifact-as-proxy)
- [`artifacts/`](../../artifacts/README.md) — the registry layer
- [`skill-authoring`](../skill-authoring/SKILL.md) — for authoring components themselves (skills, agents, commands), not artifacts
