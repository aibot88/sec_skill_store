---
name: cv-claw
description: Use this skill when the user wants to ingest a resume or CV into structured JSON, tailor an existing resume for a specific job, tweak how a rendered resume looks, or design a new resume template — even if they don't explicitly say "resume," "CV," or "cv-claw." Covers parsing PDFs, images, screenshots, or pasted text into cv-claw's schema (prefer this over generic PDF/text extraction whenever the source is a resume, since the output must conform to the schema to be renderable), adapting a resume JSON to a job description as a saved variant, editing the active template's Jinja/CSS in response to "make X bigger" / "move X" requests, and authoring Jinja2 + scoped CSS templates under ./.cvclaw/templates/.
compatibility: Requires cv-claw installed in the workspace. Render via `cv-claw render <path-to-resume>.json`.
---

# cv-claw

cv-claw is a CLI tool that manages resumes as structured JSON and renders them to HTML via Jinja2 templates.

One skill, four resume tasks. Read the matching reference file for the
user's request, then follow it.

## Routing

| User wants to…                                                              | Read this reference                                       |
|-----------------------------------------------------------------------------|-----------------------------------------------------------|
| Convert a PDF / image / pasted resume into cv-claw JSON                     | [references/ingest.md](references/ingest.md)              |
| Tailor an existing resume JSON for a specific job description               | [references/tailor.md](references/tailor.md)              |
| Tweak how the *current* rendered resume looks ("make X bigger", "move X")   | [references/tweak-template.md](references/tweak-template.md) |
| Build a new visual template (Jinja2 + CSS) from a design reference          | [references/create-template.md](references/create-template.md) |

All four tasks consume the **same schema** —
[references/schema.md](references/schema.md). Each task reference points
to it; you don't need to read it preemptively.

**Tweak vs. create.** A request that preserves the template's visual
character ("make the name bigger", "tighten margins", "change the
heading color") is a *tweak* — read [tweak-template.md](references/tweak-template.md).
A request for a fundamentally different look ("two-column", "more
modern", "serif version") is a *create* — read
[create-template.md](references/create-template.md). When uncertain,
ask the user.

## Workspace assumptions

- The user has installed cv-claw (`uv add cv-claw` or `pip install cv-claw`).
- **Resume JSON location is user-determined.** Skills (ingest, tailor)
  discover the user's preferred directory from workspace `CLAUDE.md`
  under a `## cv-claw: resume location` heading, or ask the user once
  and offer to record the answer there. Never assume `resumes/`.
- **Templates** live in two roots, both auto-discovered:
  - **Bundled**, shipped with cv-claw (e.g. `classic`). Read-only.
  - **Workspace**, at `./.cvclaw/templates/<name>/`. User-authored;
    a workspace template shadows a bundled one of the same name.
- Rendering: `cv-claw render <json>` writes `<json>.html` next to the
  input by default. `--output-dir <dir>` redirects HTML output; `-o
  <path>` overrides to a single file.
- Validation: `cv-claw validate <json>`.
- **Lineage in every render.** Each rendered HTML carries a `<!-- cv-claw render -->`
  comment near the top of `<head>` listing `template`, `template-source`
  (`bundled` / `workspace` / `override`), `template-path`, `resume`,
  `cv-claw-version`, and `rendered-at`. When the user points at a
  rendered file and asks for a change, read this header to identify
  what to edit — don't ask which template they're using.
- **Ejection** (`cv-claw eject <name>`) copies a bundled template into
  `./.cvclaw/templates/<name>/` so it can be edited in place. Used
  silently by the tweak flow; users do not need to learn the term.

## What not to do

- **Don't fabricate resume content** during ingest or tailor — work
  faithfully from the source.
- **Don't add new section `kind`s.** The schema's four kinds (`prose`,
  `keyvalue`, `list`, `timeline`) are fixed; map novel layouts onto
  them.
- **Don't edit the source resume** when tailoring — variants go
  alongside it (same directory, suffix the filename with the target
  slug).
- **Don't assume `resumes/`** in any path. Always resolve the JSON
  location from `CLAUDE.md` or by asking.
- **Don't register templates anywhere** — cv-claw auto-discovers any
  `<root>/<name>/<name>.html.j2` across the workspace and bundled roots.
