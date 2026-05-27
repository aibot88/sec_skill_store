---
name: architecture-md-authoring
description: Create or revise repository `ARCHITECTURE.md` files as short, stable architecture codemaps. Use when an agent needs to author or edit `ARCHITECTURE.md`, restructure an architecture document around a bird's-eye view and code map, clarify system boundaries, add architectural invariants or cross-cutting concerns, or decide which implementation detail should stay out of `ARCHITECTURE.md` and live in deeper design documents instead.
---

# ARCHITECTURE.md Authoring

Write `ARCHITECTURE.md` as a durable map of the repository, not as a detailed implementation manual.

Prefer high-level structure, explicit boundaries, and stable invariants over low-level walkthroughs. The goal is to help a new contributor answer "where does this kind of change belong?" faster than they could by reading files one by one.

## Workflow

### 1. Build the map before writing

Read the current `ARCHITECTURE.md`, inspect the top-level repository structure, and identify the main subsystems, boundaries, and external dependencies.

When revising an existing file, preserve the stable ideas and remove detail that will rot quickly. Use nearby design docs only to confirm boundaries and terminology, not to copy detailed implementation notes into the architecture file.

### 2. Keep the document short and stable

Bias toward information that changes slowly:

- the problem the system solves,
- the major runtime parts,
- the main directories or modules,
- the boundaries between subsystems,
- the important architectural invariants,
- and the key cross-cutting concerns.

Do not turn `ARCHITECTURE.md` into an atlas of every implementation detail. If a section needs operational steps, deep rationale, or subsystem-specific procedure, move that material into `docs/` or inline code documentation and leave `ARCHITECTURE.md` as the map.

### 3. Use a codemap structure

A strong default structure is:

- short introduction,
- `## Bird's Eye View`,
- `## System Boundaries` when boundaries matter,
- `## Code Map`,
- `## Cross-Cutting Concerns`.

Inside the code map, describe coarse-grained directories, modules, or layers and what each one owns. Name important files, modules, or types when they help orientation, but avoid brittle deep linking.

The code map should help a reader answer:

- where code for a feature or concern probably lives,
- what a directory or subsystem is responsible for,
- and which concerns deliberately do not belong in that area.

### 4. State invariants explicitly

Architecture documents are especially valuable when they say what must remain true or what is intentionally absent.

Call out invariants such as:

- a subsystem that must stay independent from another,
- responsibilities that should not move across a boundary,
- external systems that remain the source of truth,
- or categories of work that should happen client-side rather than server-side.

When an invariant is really an absence, say it plainly. Those are the hardest properties to infer from code alone.

### 5. Emphasize boundaries, not internals

A good architecture document explains how the main parts relate without explaining every internal mechanism.

Prefer boundary language such as:

- which layer owns a concern,
- which system is the source of truth,
- what crosses the network boundary,
- which directories are API boundaries,
- and what should remain stateless, local, generated, or provider-agnostic.

Avoid deep call-flow narration unless it is necessary to explain the overall system shape.

### 6. Keep cross-cutting concerns separate

After the code map, gather concerns that span multiple areas into a dedicated section. Typical examples include:

- authentication and identity,
- persistence,
- external providers,
- secrets,
- observability,
- CI/CD,
- and generation or migration workflows.

This keeps the codemap readable while still surfacing the important concerns that show up everywhere.

## Editing Patterns

### Writing a new `ARCHITECTURE.md`

Start with a plain-language description of what the system does for a user. Then describe the major runtime split and the top-level repository shape. Add only the invariants and boundaries that materially affect where contributors should make changes.

### Tightening an existing architecture file

If the file is too long or too implementation-heavy:

1. Remove detail that belongs in design docs or subsystem docs.
2. Merge repetitive sections into a higher-level codemap.
3. Keep only stable directory/module descriptions.
4. Pull out explicit invariants and cross-cutting concerns into their own sections.

### Adapting to repo style

Match the repository's actual architecture and vocabulary.

For example, if the repo already frames itself in terms of client, API, and infrastructure boundaries, keep that framing. If it uses product-specific terms consistently, use those terms rather than inventing a new taxonomy.

## Quality Bar

A good `ARCHITECTURE.md` should let a new contributor answer these questions quickly:

- What does this system do at a high level?
- What are the main runtime parts and repository areas?
- Where should I look to change a given concern?
- Which boundaries and invariants should I avoid violating?

If the file reads like a detailed design doc, it is too deep. If it names directories without explaining responsibilities or boundaries, it is too shallow.
