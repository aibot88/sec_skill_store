---
name: lossless-flavored-markdown
description: The Lossless Group's extended-markdown flavor — what LFM is, when to use it, how its directives normalize across syntaxes (CommonMark, GFM, Obsidian callouts, remark-directive, Markdoc), how citations and link previews work, and how sites extend it via trigger maps and theme tokens. Use whenever authoring or rendering content in any Astro Knots site, integrating the @lossless-group/lfm package, building or registering custom components for markdown, debugging callouts/embeds/citations, or when the user mentions "LFM", "Lossless Flavored Markdown", "extended markdown", "directive syntax", "wikilink", "trigger map", "callout", or "hex-code citation".
---

# Lossless Flavored Markdown (LFM)

> **MDX power without MDX's opinions.** A polyglot markdown spec where user-configured *syntax-triggers* drive a render pipeline in a frontend framework — so plain `.md` files get the expressive power of MDX, without the JSX-shaped lock-in.

LFM is the Lossless Group's extended-markdown spec, implemented as the `@lossless-group/lfm` package. The package source lives inside the **`astro-knots`** repo today (and may graduate to its own repo later). Downstream sites and apps consume it as a dependency from **JSR (`jsr.io`)**, the canonical public registry. GitHub Packages is a secondary mirror for internal use.

**Canonical spec (the long form, ~4,400 lines):** `lossless-monorepo/astro-knots/context-v/specs/Codifying-a-Comprehensive-Extended-Markdown-Flavor-and-Shared-Package.md`

## The paradigm in one sentence

**User configurations declare syntax-triggers. Each trigger maps a markdown pattern to a component in the consuming framework. The pipeline normalises authoring syntax to component nodes and lets the framework render them.**

That's the whole shape. Everything else — the trigger map, the variant registry, the theme tokens, the polyglot syntax — is implementation of that one idea.

## When to use this skill

**Authoring / consuming side:**
- Writing or rendering content in any Astro Knots site
- Adding `@lossless-group/lfm` to a new project (`pnpm dlx jsr add @lossless-group/lfm`), or upgrading it
- Migrating an Obsidian vault into a publishable Astro site
- Debugging callouts, hex-code citations, link previews, dialog blocks, image floats

**Co-development side (the package itself):**
- Working in `astro-knots/packages/lfm/` (or wherever the LFM source lives at the time)
- Adding a new built-in trigger to the default trigger map
- Modifying the AST normaliser, the OG fetcher, the citation resolver, the wikilink resolver
- Cutting a JSR release of `@lossless-group/lfm`
- Promoting LFM to its own repo (when the team decides to)

**Always:**
- File signals: `.md` content collections in an Astro site, `lfm-triggers.yaml`, `lfm-variants.yaml`, `@lossless-group/lfm` in `package.json` or `jsr.json`
- Frontmatter signals: `lede`, `at_semantic_version`, `augmented_with`, `image_prompt`, `status: Draft|Review|Published|Archived`
- User phrases: "LFM", "Lossless Flavored Markdown", "extended markdown", "syntax-trigger", "trigger map", "MDX without MDX", "polyglot markdown", "callout", "wikilink", "directive"

## The mental model in four paragraphs

**Polyglot syntax, single AST.** Directive syntax (`:::callout{...}`), Obsidian callouts (`> [!warning]`), Markdoc tags (`{% %}`), and bare URLs all parse to the *same* component node. Authors pick the syntax that fits their tool; the renderer doesn't care. This is the "polyglot" half of the spec.

**Syntax-triggers are user-configured.** A trigger map (YAML) declares: *this pattern* → *that component* → *these props*. Sites layer their own trigger map on top of the package's defaults to add components, override built-ins, or disable features. Adding a new component to a site is a YAML entry plus a component file — never a markdown change, never an `import`.

**The render pipeline is framework-agnostic.** `@lossless-group/lfm` is a `unified` / `remark` plugin. It produces a normalised AST with component nodes; the consuming framework (Astro, Svelte, Solid, plain HTML) supplies the components. Astro Knots sites are the primary consumer; the architecture doesn't preclude others.

**JSR for consumption, astro-knots for development.** Sites and apps install via `jsr add @lossless-group/lfm`. Agents working *on* LFM itself work in `astro-knots/packages/lfm/` (or the dedicated repo, if/when it spins out). Releases go to JSR first; GitHub Packages is a mirror for internal-only consumers.

## Five non-negotiable rules

### 1. Polyglot syntax normalises — don't fight it

Authors may write `:::callout{type="warning"}` *or* `> [!warning]`. The parser produces the same AST node. **Don't enforce one syntax across a vault.** Pick one per document for readability; let the team migrate at their own pace. Obsidian-first authors keep callout syntax; Astro-first authors keep directive syntax. Both ship to the same site.

### 2. Hex-code citations, not sequential numbers

Inline references use `[^1ucdcd]`, never `[^1]`. Sequential numbers break the moment content is reordered, split, or copy-pasted between documents. Hex codes are stable. The bibliography definition still uses footnote syntax:

```markdown
Inline:
…aging is accelerating toward 2.1B people 60+ by 2050.[^1ucdcd]

Definition (anywhere in the doc):
[^1ucdcd]: 2025-09-21. [Population ageing](https://helpage.org/...). Published: 2024-07-11
```

### 3. Component registry is the single source of truth

Every custom component name maps to **exactly one** file path via the trigger map. No imports in markdown. No two definitions of the same name. Adding a component means a YAML entry and a component file — nothing else.

### 4. OG metadata is fetched at **build time**, not client-side

Hover popovers and link previews must work offline and appear instantly on hover. That means the build step fetches OpenGraph metadata for every external link and embeds it in the page. Default config: `timeout: 5000ms`, `maxConcurrent: 10`. Never bump timeout above 10s in CI — one slow URL stalls every build.

### 5. CSS-in-markdown is sandboxed

Authors may pass `style="…"`, `class="…"`, or scoped CSS blocks. The renderer strips `url()`, `javascript:`, and `@import`. Don't try to inject content via styles; use a registered component instead.

## Feature inventory — what LFM ships

**Stable (Tier 1, in production):** CommonMark + GFM, YAML frontmatter with Zod, Shiki-highlighted code fences, Mermaid diagrams, callouts (directive + Obsidian forms), inline badges, hex-code citations with hover popovers, scrollable/sortable tables, slide separators (`---slide---`), `:::details` collapsibles, zero-friction media embeds (bare YouTube/Vimeo URLs auto-detect).

**Beta (Tier 2):** `::image` directive (float / caption / source attribution), `:::image-gallery`, auto-generated TOC, wikilinks / backlinks, custom code-block components (`card-carousel`, `image-grid`).

**Wish list (Tier 3):** Math/LaTeX, `==highlights==`, Obsidian transclusion (`![[file.md]]`), wikilink aliases, dialog/chat UI (`:::dialog`), Tufte sidenotes, JSON Canvas, Obsidian Bases (`.base` database views), multi-column layouts, tabs, numbered procedures, scoped CSS-in-markdown.

For the per-feature syntax, see [references/syntax-and-directives.md](references/syntax-and-directives.md).

## The five most-used syntaxes

```markdown
# 1. Callout (directive form)
:::callout{type="warning" title="Heads up"}
This is important.
:::

# 2. Callout (Obsidian alias — same render)
> [!warning] Heads up
> This is important.

# 3. Image with float + caption + source attribution
::image{src="/chart.png" alt="Market sizing" float="right"
  caption="GLP-1 projection through 2030"
  source="Goldman Sachs Research" source-url="https://gs.com/research"}

# 4. Hex-code citation
…aging accelerates toward 2.1B people 60+ by 2050.[^1ucdcd]

[^1ucdcd]: 2025-09-21. [Population ageing](https://helpage.org/...).

# 5. Zero-friction media embed (bare URL on its own line)
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

For the full directive form (`:text-directive`, `::leaf-directive`, `:::container-directive`), link previews, dialog blocks, and code-fence component routing, see [references/syntax-and-directives.md](references/syntax-and-directives.md).

## Common pitfalls

- **Sequential `[^1]` citations.** Always hex codes. See rule 2.
- **Missing alt text.** `::image` requires `alt=""` even for decorative images. Empty string is the explicit "screen-reader skip" signal.
- **Forgetting the auto-unfurl opt-out.** A URL on its own line embeds. To keep it as a plain link, prefix with a backslash: `\https://example.com`.
- **Unbalanced `:::` delimiters.** Container directives are strict about open/close pairs. Lint with `pnpm lfm:check` in CI.
- **Unquoted prop values.** `columns="3"` works; `columns=3` doesn't. All directive props are strings; the component coerces types.
- **Reserved attribute overrides.** `format`, `type`, and a few others are component-managed and silently ignored when set on `::leaf-directive`s. See [references/extensibility.md](references/extensibility.md) for the full list.
- **OG fetch timeouts ≥ 10s in CI.** A single unreachable URL stalls the whole build. Keep `timeout: 5000`.

## Quick install (JSR — recommended path)

```bash
# In any Astro Knots (or other) site:
pnpm dlx jsr add @lossless-group/lfm
pnpm dlx jsr add @lossless-group/lfm-astro

# Then in astro.config.mjs:
import lfm from '@lossless-group/lfm-astro';
export default defineConfig({ integrations: [lfm()] });
```

JSR needs no auth tokens — clone-and-`pnpm install` works for any contributor. For the GitHub Packages mirror (internal-only), the local-development workflow when modifying LFM itself, full `remarkLfm` options, and the trigger-map override pattern, see [references/package-and-setup.md](references/package-and-setup.md).

## Cross-skill seams

- **[astro-knots](../astro-knots/)** — LFM is the markdown layer *inside* Astro Knots. Every Astro Knots site uses it.
- **[context-vigilance](../context-vigilance/)** — LFM frontmatter (`status`, `at_semantic_version`, `date_authored_*`) follows context-v conventions. The LFM spec itself lives in `astro-knots/context-v/specs/`.
- **[theme-system](../theme-system/)** — LFM components consume CSS custom properties (`--lfm-card-bg`, `--lfm-accent`). Layer 3 of LFM extensibility is pure theme tokens.
- **[open-graph-share-seo-geo](../open-graph-share-seo-geo/)** — LFM's build-time OG fetch (rule 4) feeds both hover popovers *and* the page's `og:*` meta tags. Same metadata pipeline.
- **[changelog-conventions](../changelog-conventions/)** — Changelog entries are LFM markdown. Frontmatter conventions overlap (`date_published`, `date_modified`).
- **[pseudomonorepos](../pseudomonorepos/)** — `@lossless-group/lfm` is one of the shared packages that ties submodule sites together.

## See also

- [references/triggers-to-component-pipeline.md](references/triggers-to-component-pipeline.md) — the paradigm itself: how the pipeline turns syntax into components, the current trigger catalogue (versatility evidence), the OG/popover/source-promotion sub-pipelines, and the recipe for adding a new trigger
- [references/syntax-and-directives.md](references/syntax-and-directives.md) — every directive form, all syntactic aliases, citation hex-code rules, code-fence component routing, dialog blocks, link-preview cards
- [references/extensibility.md](references/extensibility.md) — the three customization layers (per-instance attributes, variant registry, theme tokens), reserved attribute names, validation policies
- [references/frontmatter-schema.md](references/frontmatter-schema.md) — recommended fields, Zod schemas, status workflow, AI-co-authorship markers
- [references/package-and-setup.md](references/package-and-setup.md) — JSR-first install, the GitHub Packages mirror, `remarkLfm` config, the co-development workflow when working *on* LFM
- **Canonical spec:** `lossless-monorepo/astro-knots/context-v/specs/Codifying-a-Comprehensive-Extended-Markdown-Flavor-and-Shared-Package.md` (the long form — 4,400 lines)
