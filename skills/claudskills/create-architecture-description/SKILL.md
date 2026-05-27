---
name: create-architecture-description
description: >-
  Analyze a codebase and draft stakeholder-focused architecture description
  documents in Swedish from a supplied template, architecture brief, or output
  path. Use when Codex needs to inspect project structure, processes,
  integrations, data flows, deployment, identity, security, testing, or
  migration concerns and synthesize only the relevant architecture perspectives
  with overview-level text, concrete component references, forward-looking
  notes, mermaid diagrams, and ArchiMate-style sketches.
---

# Create Architecture Description

Draft a Swedish architecture description from code, docs, and a supplied
template or prompt.

Keep the narrative concise, high-level, and tied to specific components and
repository evidence. Make it useful for stakeholders across technical and
non-technical roles.

## Workflow

1. Read the user prompt, requested output path, and any provided template or
   architecture instructions.
2. Inspect the codebase and docs to identify the solution purpose, actors,
   workflows, major components, data stores, integrations, environments,
   identity model, security controls, and delivery flow.
3. If the user provides a template, follow its perspective names and overall
   structure first.
4. If the user does not provide a template, use
   `references/perspectives.md` as the default template. Choose only the
   perspectives that clarify the solution.
5. If `references/perspectives.md` is used, treat each `Swedish heading` value
   as the canonical output heading and follow the file's order unless a
   different order improves clarity.
6. Create the requested markdown file after analysis. If no
   output path is given, suggest a `docs/arkitekturbeskrivning-<subject>.md`
   filename and continue if the intent is otherwise clear.
7. For each selected perspective, write in Swedish.
8. Describe `Current state` and `Target state` at overview level while
   referencing concrete systems, modules, APIs, tables, jobs, or environments.
9. Add brief `Forward look` notes when roadmap, scaling, governance, or
   migration implications are visible in the code or docs.
10. If `Implementation and Transition Perspective` is included, use
    `Transition` to explain how the change will be implemented.
11. Add diagrams only where they improve comprehension.
12. Mark gaps as assumptions or open questions. Do not invent hidden
    integrations, controls, or processes.

## Output Contract

- Write the final document in Swedish.
- Preserve the provided template's headings, ordering, and terminology when a
  template is supplied.
- Keep headings unique across the full document. If the same concept recurs,
  contextualize the heading with the perspective or scope.
- Keep the text concise and architectural. Explain relationships and intent
  before implementation detail.
- Reference concrete repository evidence such as packages, routes, jobs, data
  stores, integrations, infrastructure files, or test and deploy workflows.
- Speak to stakeholders in each perspective, not only to developers.
- Prefer clear markdown sections over long prose blocks.
- Include a short overall summary near the top when the template allows it.
- Include mermaid diagrams when they clarify boundaries, flows, or
  responsibilities.
- Include one ArchiMate model per selected perspective.
  Use an ArchiMate-capable text diagram syntax or tool when available.
  If none is available, use compact ASCII.
- Use proper Swedish characters in the generated document even if the skill
  instructions use ASCII transliterations for some labels.

## Default Template

When the user does not provide a template, use
`references/perspectives.md` as the default template.

- Use the `Output labels` block in `references/perspectives.md` as the base
  Swedish terms for subsection names.
- Keep the selected perspectives in the same general order as the reference
  file unless a different order is clearer.
- Use each perspective's `Swedish heading` value as the section heading in the
  generated document.
- Use each perspective's `Stakeholders`, `Use when`, and `Cover` lines to shape
  the section content, not as literal output labels.
- Render repeated subsection concepts as unique headings by combining the base
  term with the perspective or scope, for example `Övergripande nuläge`,
  `Målläge för informationssäkerhet`, or `Framåtblick för applikationsstruktur`.
- Within each selected perspective, cover `Current state` and `Target state`
  when they help the reader understand the architecture.
- Add `Forward look` when it helps the reader understand strategic direction,
  next steps, or expected evolution.
- Use `Transition` only in `Implementation and Transition Perspective`.
  Focus it on how change will be implemented, such as phased retirement,
  component replacement, installation of new capability, or technology shifts.
- Add mermaid and ArchiMate-style diagrams only when they improve clarity.

## Diagram Guidance

- Use one overall diagram when the reader needs a fast orientation.
- Use sequence or flow diagrams for process and integration perspectives.
- Use component or dependency diagrams for application structure.
- Use deployment-style diagrams for infrastructure use and environment mapping.
- Do not present Mermaid as native ArchiMate support.
- Keep diagram labels in Swedish unless external system names are fixed.
- If an ArchiMate view would add no value, keep it minimal rather than forcing
  detail.

## Evidence Checklist

Check the most relevant sources before writing:

- `README`, `docs/`, ADRs, architecture notes, onboarding guides
- top-level app and service folders
- API routes, UI entry points, workers, schedulers, message handlers
- database schema, migrations, seeds, or model definitions
- infrastructure and deployment files
- auth, permissions, audit, logging, and security-related code
- test, CI, and environment configuration

## Constraints

- Do not mirror source code structure mechanically; explain the architecture in
  business-relevant terms.
- Do not drop important perspectives just because the implementation is thin;
  describe the current maturity honestly.
- Do not create low-level design documentation unless the user explicitly asks
  for it.
