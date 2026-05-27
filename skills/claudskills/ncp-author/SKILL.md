---
name: ncp-author
description: >-
  Schema cheatsheet, canonical vocabulary (463 appreciations + 144
  narrative_functions), validation rules, 10-stage authoring workflow, and
  runnable schema validator for NCP (ncp-schema.json v1.3.0). Actively
  co-invokes dramatica-theory (storyform decisions, why a Class/Type/Variation
  is correct) and dramatica-vocabulary (Dynamic-Pair validation, KTAD coherence,
  Element-Quad checks) at explicit workflow checkpoints — this skill owns
  JSON-IO and enum-compliance; the two Dramatica skills own meaning. Use when
  the user mentions NCP, narrative-context-protocol, ncp-schema, .ncp.json,
  'convert to NCP', 'validate NCP', 'storyform JSON', or Subtxt export. Trigger
  auch auf Deutsch — Storyform anlegen, NCP-Datei validieren, NCP-Skelett,
  Storyform aus Outline. Do NOT use for general Dramatica theory (defer to
  dramatica-theory or dramatica-vocabulary) or prose drafting. Path A per
  TODO T-1.
metadata:
  category: narrative-systems
  source: user
  status: active
  version: "0.4.0"
  date_added: "2026-05-03"
  upstream_pin: "0b9ab1223d3822a49eddc139bcdf2669aa067734"
  upstream_repo: "https://github.com/narrative-first/narrative-context-protocol"
  granularity: "Path A (single skill)"
  language: "EN primary, DE supplementary"
  triggers: >-
    NCP, narrative context protocol, ncp-schema, ncp-author, .ncp.json,
    storyform JSON, ideation JSON, complete-storyform-template, convert to NCP,
    validate NCP, NCP authoring, schema/ncp-schema.json, NCP storyform,
    Subtxt export, NCP file, Storyform anlegen, NCP-Datei validieren,
    NCP-Skelett, Storyform aus Outline
skill_bundles_tools:
  - tools/dramatica-nav
---

# ncp-author

**Status:** MVP, version 0.4.0. Single-skill scope committed (Path A per TODO T-1). The full target architecture — eight phase routers and ~14 sub-skills in a hexagonal pattern — is described in `SPEC.md` and remains an optional later refactor; not currently planned. See `TODO.md` for the open queue.

## What this skill does

`ncp-author` helps an agent (or a human collaborating with an agent) produce, validate, and iterate JSON documents conforming to the open-source [Narrative Context Protocol](https://github.com/narrative-first/narrative-context-protocol) — the JSON-Schema-based interchange format for Dramatica-style storyform data.

The skill is the **JSON-IO and schema-compliance** layer. It deliberately does NOT duplicate Dramatica theory reasoning or Dynamic-Pair logic — those live in `dramatica-theory` and `dramatica-vocabulary` respectively, and this skill **actively delegates to them at explicit checkpoints** in each workflow path. See `references/related-skills.md` for the full delegation map.

## Dramatica Integration Map

> Call these skills at the checkpoints marked **[→ dramatica-theory]** or **[→ dramatica-vocabulary]** below. Don't improvise reasoning that belongs to them. **For mechanical lookups** (dynamic-pair partner, Quad membership, alias resolution, NCP enum closure), prefer `tools/dramatica-nav/nav.py` — it answers in JSON without loading the source chapters. The cross-skill load contract is documented in [`AGENTS.md § Narrative Ontology`](../../AGENTS.md), with rule **NO.2** binding NCP authoring directly: every Dramatica-flavored slot MUST resolve through the canonical ontology ID before the value is written into the JSON.

| NCP entity / question | Skill to invoke | Navigator shortcut |
|---|---|---|
| *Why* is this Class / Type / Variation correct? (theory reasoning) | **dramatica-theory** | (prose; conceptual) |
| Storyform diagnosis — flat draft, unmotivated characters, act structure | **dramatica-theory** | (prose; conceptual) |
| Story Mind, Grand Argument Story, four throughlines — conceptual | **dramatica-theory** | (prose; conceptual) |
| Archetype definitions (Protagonist, Antagonist, Guardian …) | **dramatica-theory** | `nav.py by-id arc.<slug>` |
| Dynamic Pair check on any Element or Variation | **dramatica-vocabulary** | `nav.py by-id <id> --include-pairs` |
| KTAD coherence — Knowledge/Thought/Ability/Desire matrix | **dramatica-vocabulary** | `nav.py by-ktad K\|T\|A\|D` |
| Element-Quad lookup (which 4 Elements share a Quad?) | **dramatica-vocabulary** | `nav.py by-quad quad.<name>-el` |
| Encoding-Vorschlag: abstract Element → concrete scene / lyric | **dramatica-vocabulary** | (prose; conceptual) |
| Konsistenz-Check gegen die 75 Dynamic Pairs | **dramatica-vocabulary** | `nav.py by-pair <member-id>` |
| NCP enum value for an `appreciation` or `narrative_function` field | **this skill** (canonical-vocabulary.md) | `nav.py by-ncp '<enum-string>'` |
| Schema required-fields map, JSON validation, template population | **this skill** | `tools/dramatica-nav/validate.py` |

> **DE-Notiz** — Schema-Felder bleiben Englisch (kanonisch). Die Skill-Anleitung ist EN-primär; deutschsprachige Sessions können trotzdem alle Workflows nutzen. Trigger und kanonische Slot-Namen werden bei Bedarf zweisprachig in den Reference-Dateien notiert.

## When to use this skill

Use when:

- The user mentions the Narrative Context Protocol or NCP by name
- The user wants to author, edit, validate, or audit a `.ncp.json` / `*.json` file conforming to `ncp-schema.json`
- The user wants to convert an existing outline, storyform, or pitch into NCP structure
- The user wants to know which `appreciation`, `narrative_function`, `dynamic`, or `vector` enum value is canonical for a given Storyform slot
- The user wants the schema-level required-fields map for any NCP entity
- The user is exporting from Subtxt / Dramatica software and wants the output validated against the spec

Do **not** use when:

- The user wants Dramatica theory explanation independent of NCP — defer to `dramatica-theory`
- The user is mid-flow in a German narrative session and needs Dynamic Pair reasoning — defer to `dramatica-vocabulary`
- The user wants prose drafting, scene writing, or chapter generation — NCP doesn't hold prose
- The user wants to update SPEC.md itself — defer to `spec-skill`
- The user wants to build a runnable agentic loop from this skill's SPEC — defer to `ralph-skill`

## Workflow

### Quick path (one-shot authoring)

1. Copy `assets/template-empty.json` (minimal valid skeleton) or `assets/template-storyform.json` (pre-filled with the canonical Storypoint slot list per throughline) as the starting point
2. Read `references/authoring-order.md` to orient on the 10-stage practical workflow
3. Open `references/schema-cheatsheet.md` for required-field maps for each entity touched
4. Use `references/canonical-vocabulary.md` whenever filling an `appreciation`, `narrative_function`, `dynamic`, `vector`, or `throughline` field — this gives the canonical enum string
   - **[→ dramatica-theory]** If the user asks *why* a particular Class, Type, or Variation is the right choice theoretically, delegate; ncp-author only knows the *name*, not the *reason*
   - **[→ dramatica-vocabulary]** If filling an Element-level slot and the Dynamic Pair or KTAD position matters, delegate before writing the value into the JSON
5. Run `node scripts/validate.js path/to/your.json` early and often
6. **[→ dramatica-vocabulary]** Run a Dynamic-Pair coherence check: confirm no throughline carries both halves of a dynamic pair at the Element level, and that KTAD positions are consistent
7. Cross-check with `references/validation-rules.md` §8 checklist before declaring complete

### Audit path (validate an existing document)

1. Run schema validation: `node scripts/validate.js path/to/doc.json` (PASS/FAIL with first error)
2. Walk `references/validation-rules.md` §1–§6 in order
3. **[→ dramatica-vocabulary]** Run meaning-layer audit: for each Element-level slot, check Dynamic Pair consistency and KTAD position. Schema validation cannot catch a value that is a valid enum string but is theoretically incoherent with the adjacent slots.
4. **[→ dramatica-theory]** If throughline-level choices (Class assignments, MC Resolve, Story Outcome/Judgment) look questionable, delegate for a structural diagnosis before marking the document clean.
5. Use the checklist at §8 as final gate
6. Report findings; do not silently fix

### Conversion path (existing outline → NCP)

1. Identify the source format (free-text outline, beat sheet, Subtxt export, etc.)
2. **[→ dramatica-theory]** If the source outline has no explicit Storyform, reconstruct one before mapping to NCP. Use `dramatica-theory`'s storyforming workflow (essential questions, Class assignments, eight dynamics) to produce a defensible storyform first — then use `ncp-author` to encode it into JSON.
3. Map source structures to NCP entities using the table in `references/schema-cheatsheet.md` ("Mapping NCP entities to where novel-craft artifacts go")
4. Start from `assets/template-storyform.json` and fill slots in the order from `references/authoring-order.md`
5. **[→ dramatica-vocabulary]** At Element-level slots, confirm Dynamic Pair assignments before committing; use `dramatica-vocabulary`'s `element-quads.md` and `storyform-mechanics.md` as the authority
6. Preserve traceability: keep `id` references stable so source-to-NCP mappings are reproducible

## Setup

The validator depends on `ajv`. Run once per skill install:

```bash
cd <path-to-this-skill>
npm install
```

This creates `node_modules/` next to `package.json`. The validator then works against any path (absolute or relative to your CWD).

## Files in this skill

```
ncp-author/
├── SKILL.md                          ← this file
├── SPEC.md                           ← target hexagonal architecture (not currently planned)
├── TODO.md                           ← open items, blocking decisions, build queue
├── package.json                      ← npm dependency stub (ajv) for validate.js
├── references/
│   ├── schema-cheatsheet.md          ← required fields, common pitfalls
│   ├── canonical-vocabulary.md       ← all enum lists (appreciations, narrative_functions, etc.)
│   ├── validation-rules.md           ← semantic rules beyond JSON-Schema
│   ├── authoring-order.md            ← 10-stage practical workflow
│   └── related-skills.md             ← delegation map to dramatica-*, spec-skill, ralph-skill, novel-architect
├── scripts/
│   └── validate.js                   ← ajv wrapper, runs against pinned upstream schema
├── assets/
│   ├── template-empty.json           ← minimal valid NCP skeleton (Stage 0 starting point)
│   └── template-storyform.json       ← canonical Storypoint slot scaffold per throughline
└── upstream/                         ← pinned snapshot of the NCP repo at 0b9ab12
    ├── _PINNED_AT.md
    ├── schema/                       ← ncp-schema.json + .yaml (source of truth)
    ├── docs/                         ← terminology references (perspectives, appreciations, narrative-functions, dynamics, vectors, dramatica-translation)
    ├── examples/                     ← canonical valid + invalid examples
    ├── tests/                        ← upstream's own validate-*.js
    ├── SPECIFICATION.md              ← upstream NCP spec (~509 lines)
    └── README.md, HISTORY.md, etc.
```

## How to read this skill

For a one-shot NCP authoring task: load `SKILL.md` (this file) + `references/schema-cheatsheet.md` + `references/canonical-vocabulary.md`. Other references load on demand.

For conceptual / design / architecture questions about NCP itself: also load `references/related-skills.md` and skim `upstream/SPECIFICATION.md`.

For "what's next" / iteration planning: load `SPEC.md` + `TODO.md`.

## Project memory

This skill is a co-authored artifact between Michael (sabbatical, GSD/spec-driven, Köln/Bonn) and Claude. Decisions made during co-authoring sessions land in Claude's memory at session end — see `references/related-skills.md` → `memory-sync` section.

The granularity question (T-1) is settled: **Path A — single skill**. Splitting into `ncp-io` + `ncp-storyform` + `ncp-storyweaver` (Path B) or the full hexagonal suite from SPEC §8 (Path C) remain available as later refactors but are not on the roadmap.

The language question (T-12) is settled: **EN-primary with DE supplementary callouts** for terminology and triggers. Schema fields stay English (canonical).

## Limits and caveats

1. **Quad / KTAD integrity is not validated here.** NCP encodes appreciations and narrative_functions but not the Knowledge/Thought/Ability/Desire matrix Dramatica uses to constrain Element selection. **Always delegate KTAD coherence to `dramatica-vocabulary`** — use its `element-quads.md` and `storyform-mechanics.md` files. This is a required step in the Quick and Audit paths, not an optional one.

2. **Validator is a thin wrapper.** `scripts/validate.js` adds nothing the upstream `tests/validate-file.js` doesn't already do; it just relocates the entry point to a stable, skill-internal path. Same Ajv settings (`strict: false`, `allErrors: true`), same PASS/FAIL parity. If upstream's validator changes meaningfully, re-pin.

3. **Upstream drift exists.** At the pinned SHA, NCP's own example fixtures fail validation against the schema in this same SHA (legacy `signpost` field on Storybeats; `narrative.title` missing in some). The schema and SPEC are slightly desynchronized. `references/validation-rules.md` documents the tested rules; defer to schema when conflicts arise. The `assets/template-storyform.json` shipped with this skill has been cleaned of the legacy fields and validates clean against the pinned schema — use it rather than the upstream `complete-storyform-template.json` as a starting point.

4. **Multi-narrative authoring (multiple Storyforms per Story) is supported by NCP but not exercised by this skill's references.** Default to a single narrative until the multi-narrative case is needed.

5. **Prose lives outside NCP.** This skill scaffolds the structural intent only. Actual chapter/scene prose belongs in separate files with cross-references to `moment.id`. For Kohärenz-Protokoll-style novel work, `novel-architect` is the orchestrator; `ncp-author` is the structured-intent backend.
