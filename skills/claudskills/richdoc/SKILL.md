---
name: richdoc
description: This skill should be used when the user asks to "write a research report", "create a plan document for review", "produce a polished design doc", "draft a comparison sheet", "generate a richdoc", "make a one-pager", "write a status report", "produce an executive summary", "create a decision document", "build a dashboard page", or any other rich HTML deliverable intended for human review in a browser. Authors plain .html files using a small fixed vocabulary of rd-* web components for layout and rich blocks. Includes a CLI for scaffolding, asset installation, schema introspection, and validation.
---

# richdoc

richdoc is for **AI-authored, human-read HTML documents**. The agent writes a normal `.html` file using a closed vocabulary of `rd-*` custom elements. Two shipped assets (`richdoc.css`, `richdoc.js`) give every component its editorial look and behavior. No build step on the consumer side; the file opens in any browser, with or without a server.

## When to use richdoc

Plans, research reports, design docs, status one-pagers, decision memos, comparisons, postmortems, dashboards — anything where the reader is a person in a browser. Use markdown only when the renderer might be anything else (GitHub, chat, CLI). Anywhere else, richdoc is the better default.

## Authoring rules

When writing a richdoc, the agent **must**:

1. Produce a complete HTML5 document with exactly one `<rd-page>` directly inside `<body>`. Link `richdoc.css` and `richdoc.js` from `<head>`.
2. Use **only** the `rd-*` tags listed below. Inventing new ones causes lint errors and renders as empty boxes.
3. For prose, use plain semantic HTML — `<p>`, `<ul>`, `<ol>`, `<li>`, `<a>`, `<strong>`, `<em>`, `<code>`, `<pre>`, `<h1>`–`<h6>`, `<blockquote>`, `<hr>`, `<img>`, `<table>`. These are styled automatically.
4. Prefer `<rd-callout>` over bold-italic emphasis for asides longer than a few words.
5. Use `<rd-cols>` for genuinely parallel content (cards, stats, comparisons). Do not use it to force a two-column paragraph layout.
6. Put code in `<rd-code lang="…">`, diffs in `<rd-diff lang="…">`, math in `<rd-math>`, diagrams in `<rd-diagram lang="…">`. Don't fall back to `<pre>`.
7. **Never self-close custom elements.** Write `<rd-foo ...></rd-foo>`, not `<rd-foo ... />` — HTML5 ignores the slash on non-void custom elements and the tag silently absorbs the following siblings. `richdoc lint` catches this as `self-closing-custom-element`.
8. Run `richdoc lint <file>` before declaring the doc done.

## CLI

Path: `./richdoc-cli/richdoc` (relative to this SKILL.md). Requires [`uv`](https://docs.astral.sh/uv/); the first call provisions the Python environment.

| Command | Description |
| --- | --- |
| `richdoc new <output> [-t <template>]` | Scaffold a new `.html` from a template. |
| `richdoc init [dir]` | Copy `richdoc.css` and `richdoc.js` into a directory. |
| `richdoc update [dir] [--apply]` | Refresh stale shipped assets. |
| `richdoc lint <file-or-dir> [--fix]` | Validate against the rd-* schema and book-mode authoring rules. `--fix` autofixes `hero-nav-redundant`. |
| `richdoc components [--tag <name>]` | Print the vocabulary from the live schema. |
| `richdoc export md\|docx <file>` | Export to markdown or DOCX. (HTML is the source format — no export needed.) See [references/export.md](references/export.md). |
| `richdoc export confluence <file-or-dir>` | Build an offline Confluence storage bundle (storage XML + attachments + manifest). Runs `richdoc lint` first. The bundle is published by the separate `confluence` skill, never by `richdoc` itself. See [references/export.md](references/export.md). |

Templates: `plan`, `research`, `comparison`, `onepager`, `adr`, `runbook`, `book-index`, `book-chapter`.

## Minimal example

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>My plan</title>
  <link rel="stylesheet" href="./richdoc.css">
  <script src="./richdoc.js" defer></script>
</head>
<body>
<rd-page>
  <rd-hero title="My plan" eyebrow="Design doc"></rd-hero>

  <rd-callout type="tldr">
    <p>Two-sentence summary of what changes and why it matters.</p>
  </rd-callout>

  <rd-section title="Problem">
    <p>Plain prose, lists, and links work as usual.</p>
  </rd-section>

  <rd-section title="Options">
    <rd-cols n="2">
      <rd-card title="Option A" accent="success">Pros, cons.</rd-card>
      <rd-card title="Option B" accent="warn">Pros, cons.</rd-card>
    </rd-cols>
  </rd-section>
</rd-page>
</body>
</html>
```

## Element index

One line per tag, grouped by purpose. For attributes, run `richdoc components --tag rd-xxx` or see [references/elements.md](references/elements.md).

### Structure
- `<rd-page>` — outer container. Exactly one per doc, directly under `<body>`. Supports `theme`, `mode`, `width`, `toc`, `prefs`, `diagram-endpoint`.
- `<rd-hero>` — magazine title block.
- `<rd-section>` — titled section with eyebrow numeral.
- `<rd-cols>` — multi-column grid (`n="2|3|4"` or `template="2fr 1fr"`).
- `<rd-card>` — bordered block with optional accent.

### Information
- `<rd-callout>` — `info|success|warn|danger|note|tldr` aside.
- `<rd-kv>` / `<rd-row>` — spec block (`layout="inline"`) or glossary (`layout="stacked"`).
- `<rd-badge>` — inline status tag.
- `<rd-stat>` — big-number tile, optional sparkline slot.
- `<rd-progress>` — capacity bar.
- `<rd-update>` — dated changelog entry (`release|change|note`).

### Code, math, diagrams
- `<rd-code lang="…">` — fenced code with syntax highlighting.
- `<rd-diff lang="…">` — unified diff.
- `<rd-shell>` / `<rd-prompt>` / `<rd-output>` — terminal session.
- `<rd-math>` — KaTeX math.
- `<rd-diagram lang="…">` — Kroki diagram. See [Diagrams](#diagrams).
- `<rd-chart>` — Observable Plot chart or sparkline.

### Comparison, decision, planning
- `<rd-compare>` / `<rd-row-cells>` / `<rd-cell>` — decision matrix.
- `<rd-rubric>` / `<rd-criterion>` / `<rd-score>` — weighted scoring grid.
- `<rd-pros-cons>` / `<rd-pro>` / `<rd-con>` — ✓/✗ evaluation.
- `<rd-decision>` — ADR-style record (`proposed|accepted|superseded|rejected`).

### Sequenced & interactive
- `<rd-steps>` / `<rd-step>` — numbered procedure.
- `<rd-timeline>` / `<rd-event>` — vertical timeline.
- `<rd-checklist>` / `<rd-task>` — task list.
- `<rd-detail>` — collapsible (`panel|hairline|question|reveal`).
- `<rd-tabs>` / `<rd-tab>` — tabbed content (specialist; usually a section is clearer).

### Reference & navigation
- `<rd-api>` / `<rd-param>` / `<rd-response>` — single-endpoint API doc.
- `<rd-references>` / `<rd-ref>` / `<rd-cite>` — bibliography + inline citations.
- `<rd-toc>` / `<rd-chapter>` — auto TOC; book-mode for multi-file docs. See [references/multi-file-books.md](references/multi-file-books.md).
- `<rd-icon>` — Lucide icon (~1,900 names; see [ICONS.md](ICONS.md)).
- `<rd-figure>` — captioned media wrapper.
- `<rd-banner>` — doc-status ribbon (`draft|frozen|archived|confidential|info`).

## Pick the right element

| You want to … | Use |
| --- | --- |
| Show a side-by-side options matrix with headers | `<rd-compare>` |
| Score options on weighted criteria | `<rd-rubric>` |
| List ✓ / ✗ trade-offs for one or more options | `<rd-pros-cons>` |
| Show a key / value spec block at the top | `<rd-kv>` (inline) |
| Define terms in a glossary | `<rd-kv layout="stacked">` |
| Show a fenced code sample | `<rd-code>` |
| Show a terminal session with commands and output | `<rd-shell>` (NOT `<rd-code>`) |
| Show a diff between two versions | `<rd-diff>` |
| Highlight a single number with trend | `<rd-stat>` |
| Show progress / capacity / utilisation | `<rd-progress>` |
| Show a trend over time | `<rd-chart kind="line">` or sparkline in `<rd-stat>` |
| Mark a doc as draft / frozen / confidential | `<rd-banner>` (top of page) |
| Status-tag a row of content inline | `<rd-badge>` |
| Aside or "callout" of any length | `<rd-callout>` (not bold/italic emphasis) |
| Render a flow / sequence / state / class diagram | `<rd-diagram lang="…">` |
| Pull-quote, epigraph | native `<blockquote>` (auto-styled) |
| Cite a source inline | `<rd-cite key="…">` paired with `<rd-ref>` |

## Recipes

Each recipe lists the 5–10 tags you'll actually need. Reach beyond the list only with reason.

**Status one-pager** — `rd-page`, `rd-hero`, `rd-kv`, `rd-stat`, `rd-progress`, `rd-callout`, `rd-update`, `rd-checklist`.

**Plan / design doc** — `rd-page`, `rd-hero`, `rd-callout` (tldr + problem), `rd-section`, `rd-pros-cons`, `rd-steps`, `rd-detail` (open questions).

**Research report** — `rd-page`, `rd-hero`, `rd-callout` (tldr), `rd-toc`, `rd-section`, `rd-rubric`, `rd-decision`, `rd-cite`, `rd-ref`.

**Comparison sheet** — `rd-page`, `rd-hero`, `rd-callout`, `rd-rubric`, `rd-compare`, `rd-pros-cons`, `rd-decision`.

**ADR (architecture decision record)** — `rd-page`, `rd-hero`, `rd-decision`, `rd-section`, `rd-pros-cons`, `rd-cite`, `rd-ref`.

**Runbook** — `rd-page`, `rd-hero`, `rd-callout`, `rd-checklist`, `rd-steps`, `rd-shell`, `rd-detail` (failure modes).

**API reference** — `rd-page`, `rd-hero`, `rd-section`, `rd-api`, `rd-param`, `rd-response`, `rd-code`, `rd-callout`.

**Multi-file book** — `rd-toc` with `<rd-chapter>` children in every chapter file. See [references/multi-file-books.md](references/multi-file-books.md).

**With diagrams** — any of the above + `<rd-diagram lang="mermaid|plantuml|d2|graphviz|…">`.

## Diagrams

```html
<rd-diagram lang="mermaid" caption="Auth flow">
graph TD
  Browser -->|POST /login| API
  API -->|verify| DB
  API -->|set cookie| Browser
</rd-diagram>
```

One element covers ~25 diagram languages: `mermaid`, `plantuml`, `graphviz`, `d2`, `dbml`, `bpmn`, `c4plantuml`, `erd`, `excalidraw`, `nomnoml`, `pikchr`, `structurizr`, `svgbob`, `tikz`, `vega`, `vegalite`, `wavedrom`, `wireviz`, `bytefield`, `blockdiag` family, `ditaa`. See [references/diagram-langs.md](references/diagram-langs.md) for guidance on which to pick.

**Rendering is server-side.** The source is sent to a Kroki endpoint (`https://kroki.io` by default) and the returned SVG is embedded inline. Override the endpoint per-element with `endpoint="…"` or doc-wide with `<rd-page diagram-endpoint="https://kroki.internal">`. For confidential content, point at a self-hosted Kroki or PlantUML server. If the endpoint is unreachable, the source falls back to a `<rd-code>` block so it still travels with the doc.

For `lang="plantuml"` / `lang="c4plantuml"`, the `theme` attribute can name any PlantUML theme; dark-mode docs auto-inject `cyborg-outline` unless overridden. Other langs ignore `theme`.

## Books (multi-file docs)

For handbooks, runbook sets, or reference manuals that don't fit in one file: put an `<rd-toc>` with `<rd-chapter>` children in every page. The same block lives in every file; `<rd-toc>` handles active-chapter detection, prev/next nav, and the sidebar at runtime. No build step, no cross-file fetch.

`richdoc lint` enforces the contract: every chapter listed in the book must carry a matching `<rd-toc>` block (rule `book-toc-drift`, no autofix), and `<rd-hero>` must not contain hand-written prev/next `<a>` links or `Prev:/Next:/Up:` segments in `meta` (rule `hero-nav-redundant`, autofixable with `richdoc lint --fix`). `richdoc export confluence` runs lint before producing the bundle and refuses to emit one if there are errors.

See [references/multi-file-books.md](references/multi-file-books.md), [references/migrating-to-book-mode.md](references/migrating-to-book-mode.md), and `examples/book/`.

## Themes and reader prefs

`<rd-page theme="editorial-warm|graphite-modern" mode="light|dark|auto" width="narrow|standard|wide|full" toc="auto|right|left|top">`. A floating preview picker auto-appears in the bottom-right corner so readers can switch all four at runtime; selections persist per origin+path. Set `prefs="off"` to suppress it. Details in [references/motion-and-themes.md](references/motion-and-themes.md).

## Limits and trust

- **JS required** for: tabs, math, syntax highlighting, charts, sparklines, citations, TOC, count-up / fill / reveal animations, copy buttons. The rest renders with CSS alone.
- **Internet on first render** for: `rd-math` (KaTeX), `rd-code` with a `lang` set (highlight.js), `rd-chart` (Observable Plot), `rd-diagram` (Kroki), and any `rd-icon` not in the prewarmed framework set (Lucide). All degrade to a readable fallback offline.
- **Diagram trust**: every `<rd-diagram>` POSTs its source to the configured Kroki endpoint. Default is the public `kroki.io`. For sensitive content, set `diagram-endpoint` on `<rd-page>`.
- **Books duplicate the chapter list** by design — re-ordering means editing every chapter file. `richdoc lint` catches stale `href`s and inconsistent `<rd-toc>` blocks across chapters (rule `book-toc-drift`).

## Publishing to Confluence

`richdoc` produces an **offline bundle**; the separate `confluence` skill
publishes it. The two skills are deliberately decoupled — `richdoc`
never opens a Confluence connection, and `confluence` never imports
richdoc code. They communicate through the documented
`richdoc.confluence.bundle.v1` directory format.

**Agent recipe (do not deviate):**

1. Build the bundle:
   `richdoc export confluence INPUT [-o OUTPUT]`.
2. Read the `nextStep.argv` array from the JSON envelope. It contains
   the exact `["confluence", "publish-bundle", "<bundle-path>"]` to run
   next. Pass it straight to your shell tool — don't reconstruct the
   path by hand (it may contain spaces or platform-specific separators).
3. If the publish call fails with `code: CONFIG_MISSING`, ask the user
   to set up authentication first — see `confluence/SKILL.md` for the
   `confluence auth init` workflow.

```bash
# 1. In this skill: build the bundle.
richdoc export confluence docs/ -o build/confluence-docs

# 2. In the confluence skill: publish it (path from nextStep.argv).
confluence publish-bundle build/confluence-docs --profile work --parent-id 12345
```

See [references/export.md](references/export.md) for the bundle
structure and `confluence/SKILL.md` for the publish side.

## See also

- [references/elements.md](references/elements.md) — full attribute reference per tag (mirror of the schema).
- [references/export.md](references/export.md) — markdown / DOCX / Confluence bundle export semantics.
- [references/multi-file-books.md](references/multi-file-books.md) — book-mode authoring.
- [references/diagram-langs.md](references/diagram-langs.md) — which diagram lang to pick for what.
- [references/motion-and-themes.md](references/motion-and-themes.md) — motion vocabulary, themes, limitations.
- [ICONS.md](ICONS.md) — full Lucide icon name list for `<rd-icon>`.
- `examples/` — `showcase.html` exercises every component; `data-design.html`, `status-onepager.html`, and `book/` are realistic uses.
