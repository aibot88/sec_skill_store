---
name: maintain-design-md
description: How to author and maintain a `DESIGN.md` file at the root of any Lossless project (site, splash page, plugin landing, fundraise deck) following Google Stitch's open spec. Use whenever a project is missing a `DESIGN.md` and an agent needs the project's visual identity in machine-readable form; whenever the user mentions "design tokens", "design system", "DESIGN.md", or "Stitch spec"; whenever theme/CSS-token work changes the runtime values (new CSS custom property in `:root`, renamed token, new mode, new component pattern, refreshed palette, refreshed typography scale) and the documented contract has drifted; whenever a sibling skill (`generate-consistent-og-images`, `theme-system`, `astro-knots`) needs to read locked design values; whenever the user says "the agent doesn't know what color we use" or "let's write down the design system." Encodes (1) the Stitch spec's frontmatter token groups (colors, typography, rounded, spacing, components) and the eight prose sections in canonical order, (2) the maintenance triggers — what kinds of code changes should bounce back into the document, (3) the "runtime CSS is source of truth, DESIGN.md is the contract" discipline, (4) the precedent for off-spec extensions like an `imagery:` block, (5) anti-patterns. The skill never sees an API key or makes network calls — it's a pure-document discipline.
---

# Maintain DESIGN.md

> Every Lossless project with a visual surface should have a `DESIGN.md` at its root. It is the **agent-readable contract** that explains the project's visual identity — colors, typography, spacing, components, behavior under hover/focus/dark/light. Both humans and AI agents read it. When the codebase's CSS custom properties drift away from what `DESIGN.md` says, fix `DESIGN.md`.

## When to use this skill

- **Bootstrapping a new project** that needs a `DESIGN.md` from scratch — splash, site, plugin landing, fundraise deck
- **Maintaining an existing `DESIGN.md`** when the runtime CSS / component vocabulary has evolved past what's documented
- **Auditing drift** — the codebase says one thing (e.g. `--radius-md: 12px`), the document says another (e.g. `rounded.md: 8px`); reconcile
- **Adding a project-specific off-spec section** — like the `imagery:` block for the `generate-consistent-og-images` skill — and you want to know where it belongs and how spec-compliant consumers will handle it
- A sibling skill (`generate-consistent-og-images`, `theme-system`, `astro-knots`, `open-graph-share-seo-geo`) needs to read locked design values and they're not in `DESIGN.md` yet
- The user says: "the agent doesn't know what color we use", "let's write down the design system", "we need a DESIGN.md", "is there a DESIGN.md for this site?", "update the design doc"

## The spec

Lossless `DESIGN.md` files follow Google Stitch's open spec, version `alpha` (current):

- **Reference repo:** <https://github.com/google-labs-code/design.md>
- **Full spec:** <https://github.com/google-labs-code/design.md/blob/main/docs/spec.md>
- **Examples:** the `examples/` directory of the spec repo (`atmospheric-glass`, `paws-and-paths`, `totality-festival`)
- **Lossless reference implementation:** `content-farm/splash/DESIGN.md` — full canonical example with both standard Stitch sections and an off-spec `imagery:` extension

A `DESIGN.md` has two parts: **YAML frontmatter** (machine-readable tokens) and a **markdown body** (human-readable rationale).

### YAML frontmatter — token groups

Top-level frontmatter keys (all optional except `name`):

| Key | Type | Notes |
|---|---|---|
| `version` | string | Current: `"alpha"` |
| `name` | string | The design system name (e.g. `"Content Farm — Astro Knots Dark"`) |
| `description` | string | One-paragraph summary |
| `colors` | map\<string, Color\> | Hex (`#rrggbb`) values. At minimum `primary` |
| `typography` | map\<string, Typography\> | fontFamily, fontSize, fontWeight, lineHeight, letterSpacing, fontFeature, fontVariation |
| `rounded` | map\<string, Dimension\> | Common: `sm`, `md`, `lg`, `xl`, `full` |
| `spacing` | map\<string, Dimension \| number\> | Numeric for ratio-style, dimensions (`px`/`em`/`rem`) for sizes |
| `components` | map\<string, map\<string, string\>\> | Component tokens; values may reference others via `{path.to.token}` |

**Token references** use curly-brace syntax: `"{colors.primary}"`, `"{rounded.md}"`. Most references must point to a primitive value (a single token, not a group). Within `components:`, references to composite values like `"{typography.label-md}"` are explicitly permitted.

**Dimension values** are strings with a unit suffix: `px`, `em`, `rem`. Unitless numbers in `lineHeight` are treated as multipliers of `fontSize` (this is CSS-idiomatic).

### Markdown body — eight sections in canonical order

```
1. Overview              (also: "Brand & Style")
2. Colors
3. Typography
4. Layout                (also: "Layout & Spacing")
5. Elevation & Depth     (also: "Elevation")
6. Shapes
7. Components
8. Do's and Don'ts
```

Sections can be omitted if not relevant, but those present must appear in this order. All section headings are `<h2>` (`##`). An optional `<h1>` may appear for titling but is not parsed as a section. The spec's "Consumer Behavior for Unknown Content" table guarantees that unknown sections and tokens are preserved without errors — so project-specific extensions (see §"Off-spec extensions" below) are safe.

## Bootstrapping a new `DESIGN.md`

When a project is missing a `DESIGN.md`, follow this flow:

1. **Don't invent values out of thin air.** Read the project's actual runtime CSS first. The `:root` block of a `BaseLayout.astro` or `theme.css` or `global.css` is where the source-of-truth values live today. The `DESIGN.md` is a *description* of those values, not a parallel decision.
2. **Copy the shape, not the values, of the Lossless reference implementation** (`content-farm/splash/DESIGN.md`). The eight section order is canonical; the token-group names (`colors`, `typography`, `rounded`, `spacing`, `components`) are canonical; the *values* belong to whichever project you're documenting.
3. **Walk the runtime CSS top-to-bottom** and translate it into frontmatter tokens. Surfaces (backgrounds) → `colors.surface-*`. Text → `colors.on-surface-*`. Borders → `colors.border*`. Brand accents → `colors.primary` / `colors.primary-soft` / `colors.accent-*`. Spacing scale → `spacing.*`. Border radii → `rounded.*`. Font stacks → `typography.*`.
4. **Author the eight prose sections** in canonical order. Each section answers a different question:
   - **Brand & Style:** What's the *emotional* register? Playful or professional? Dense or spacious? What metaphors recur?
   - **Colors:** Why these colors and not others? How do they signal (primary = the action, magenta = noteworthy)?
   - **Typography:** Why two families (or one, or three)? What does each cue?
   - **Layout & Spacing:** Container model (fixed-max / fluid / grid)? Vertical rhythm rule?
   - **Elevation & Depth:** Flat or shadow-heavy? What signals "higher in the stack"?
   - **Shapes:** Rounded scale, why these levels?
   - **Components:** What's the actual component vocabulary — button, card, callout, pill, etc.?
   - **Do's and Don'ts:** Hard rules distilled from prior mistakes.
5. **Note the runtime source of truth at the top of the file.** Convention: `> The runtime source of truth is <path-to-css-file>; this document is the human- and agent-readable contract that explains intent. Keep the two in sync when either changes.`

Template scaffold: `templates/design-md-scaffold.md` in this skill.

## Maintaining an existing `DESIGN.md`

### What changes in code trigger an update?

A `DESIGN.md` update is needed whenever any of these happen in the runtime CSS or component layer:

| Trigger | Update to `DESIGN.md` |
|---|---|
| New CSS custom property added to `:root` | Add a token to `colors:` / `typography:` / `rounded:` / `spacing:` |
| Existing token's value changed | Update the token value in frontmatter; if the change is non-trivial (e.g. palette shift, font-family swap), update the matching prose section too |
| Token renamed | Rename in frontmatter; grep prose for references and update those too |
| New reusable component shipped (`<CtaButton>`, `<PluginCard>`, etc.) | Add a `components.<name>:` entry with the relevant style tokens; add a subsection under `## Components` with the component's vocabulary |
| Component prop / variant added | Update the existing component entry; add a paragraph in the matching `## Components` subsection |
| New mode added (e.g. `vibrant` next to `light` and `dark`) | Extend the color tokens or add a `modes:` extension block; update `## Brand & Style` to describe the mode |
| Spacing or radius scale extended | Add the new step to `spacing:` / `rounded:`; update prose in `## Layout & Spacing` or `## Shapes` |
| New illustrative-asset recipe (e.g. an Ideogram template) | Add an `imagery:` extension block (see `generate-consistent-og-images` skill); add an `## Imagery` prose section |
| A `Don't` was learned the hard way | Add a bullet to `## Do's and Don'ts` capturing the rule + the why |

### What does NOT trigger an update?

- Bug fixes that don't change values (e.g. fixing an unused `--var`)
- Refactors that move CSS between files without changing values
- One-off page-specific styles that don't belong to the system (e.g. a hero treatment unique to one route)
- New utility CSS classes that don't introduce new tokens

### Drift audit — a quick check

When a `DESIGN.md` exists but you're not sure if it's current, run this audit (mental or scripted):

1. **Frontmatter `colors:` vs runtime.** Grep the codebase for `--clr-` (or whatever the project's CSS-variable prefix is). Every distinct token should appear in `colors:`. Any with different values is drift; reconcile in favor of the runtime (the codebase ships; the doc describes).
2. **Frontmatter `components:` vs `src/components/`.** Every reusable component in the components directory that has its own styling should have a `components.<name>:` entry. Recent additions are usually the gap.
3. **Prose `## Components` subsections.** Each component entry in frontmatter should have a matching prose subsection explaining its purpose. Frontmatter-only entries are tolerable; prose-only entries (no token equivalent) are usually a sign that someone *almost* added a component but the actual token block didn't make it.
4. **`## Do's and Don'ts` recency.** If the project has a `changelog/` with entries describing visual-fix rounds, every "we tried X and it didn't work" should leave a trace in `## Do's and Don'ts`. Otherwise you'll re-make the same mistake.

## Source-of-truth discipline

A `DESIGN.md` *describes* a system; it doesn't *implement* one. The runtime CSS is what actually ships. So:

- **When code and doc disagree:** trust the code. Fix the doc.
- **When the user asks "what color should this be?":** read the runtime CSS first, then check that the doc agrees. If the doc disagrees with the code, surface the drift before answering.
- **When designing something new:** decide in CSS first (because that's what ships), then document the decision in `DESIGN.md`. Don't try to "design in the doc" and then ask the user to implement what the doc says — the doc will read confidently but the runtime won't match.

Always note the runtime source-of-truth path at the top of `DESIGN.md` in a blockquote:

```markdown
> The runtime source of truth is `src/layouts/BaseLayout.astro`'s `:root` block.
> This document is the human- and agent-readable contract that explains intent.
> Keep the two in sync when either changes.
```

## Off-spec extensions

The Stitch spec's "Consumer Behavior for Unknown Content" table guarantees:

| Scenario | Behavior |
|---|---|
| Unknown section heading | Preserve; do not error |
| Unknown frontmatter top-level key | Preserve |
| Unknown color / typography token name | Accept if value is valid |
| Unknown component property | Accept with warning |

So **project-specific extensions are safe** as long as you keep the standard sections in canonical order and don't break the YAML structure. Three known Lossless extensions:

| Extension | Lives in | Owned by skill |
|---|---|---|
| `imagery:` block (Ideogram request recipe) | Frontmatter, after `components:`; `## Imagery` prose section before `## Do's and Don'ts` | `generate-consistent-og-images` |
| `modes:` block (light/dark/vibrant variants) | Frontmatter; mode-specific overrides in `## Brand & Style` or `## Colors` | `theme-system` |
| `icons:` / `iconography:` block (icon set, stroke conventions) | Frontmatter; prose under `## Shapes` or a new section | (no skill yet — add when a project needs one) |

**Rule for adding new extensions:** the extension's *frontmatter token block* lives in the spec-compliant YAML; the extension's *prose section* uses an `<h2>` heading and slots in before `## Do's and Don'ts`. Don't break the eight canonical sections — extend after them, not in the middle.

## A small worked example — adding a new component to an existing `DESIGN.md`

Scenario: shipped a new `<CtaButton>` component. The `DESIGN.md` doesn't mention it yet.

1. **Identify the component's tokens.** Read the component's CSS scope. For `<CtaButton>` (3 variants — primary, ghost, link):
   - `cta-primary`: gradient bg, dark text, mono typography, pill radius, 12px×22px padding
   - `cta-ghost`: translucent bg, light text, neutral border
   - `cta-link`: no bg, dim text
2. **Add to `components:` frontmatter:**
   ```yaml
   components:
     # ...existing entries...
     cta-primary:
       backgroundColor: "linear-gradient(120deg, {colors.primary}, {colors.primary-soft})"
       textColor: "{colors.surface-base}"
       typography: "{typography.mono-md}"
       rounded: "{rounded.full}"
       padding: "12px 22px"
     cta-ghost:
       backgroundColor: "rgba(255, 255, 255, 0.04)"
       textColor: "{colors.on-surface}"
       typography: "{typography.mono-md}"
       rounded: "{rounded.full}"
       padding: "12px 22px"
     cta-link:
       backgroundColor: transparent
       textColor: "{colors.on-surface-dim}"
       typography: "{typography.mono-md}"
       padding: "12px 4px"
   ```
3. **Add a `### CtaButton` subsection** under `## Components`:
   ```markdown
   ### CtaButton (the primary CTA)
   
   Reusable primary action button. Three variants:
   - **Primary:** Cyan→aquamarine gradient, dark text, pill-shaped.
   - **Ghost:** Translucent surface; pairs with primary as secondary action.
   - **Link:** No surface, dim text. Tertiary inline action.
   
   Any card-scope override (e.g. tighter padding inside a card footer) is
   documented in the scope's own subsection, not here.
   ```
4. **If a "Don't" was learned**, add it under `## Do's and Don'ts`. E.g. "Don't keep the resting cyan glow shadow on the CTA when it lives inside a card footer — drop it; hover restores a softer version."

## Anti-patterns

- **Authoring a `DESIGN.md` for project A by copying project B's values.** The *shape* is canonical (eight prose sections in order + the five standard token groups). The *values* are project-specific and must be re-authored from the runtime CSS.
- **Treating `DESIGN.md` as the source of truth instead of runtime CSS.** It's the contract, not the implementation. When the two disagree, fix the doc to match the code.
- **Letting `## Do's and Don'ts` calcify.** It's the section most likely to teach the next agent something. Add a bullet whenever a visual mistake gets corrected.
- **Skipping `## Brand & Style`.** "We'll fill in the brand voice later" usually means never. The Brand & Style section is what makes an agent's stylistic decisions feel *like the project* rather than generic. It's worth writing even when short.
- **Inventing token names that drift from the runtime CSS variables.** If the CSS uses `--clr-cyan`, the frontmatter should say `colors.primary: "#04e5e5"` *and* the prose should mention "the brand cyan" — i.e., both ends of the rename should be present. Renaming in the doc without grepping the code produces "ghost" tokens nobody can find.
- **Off-spec extensions in the middle of the canonical sections.** Extensions go after `## Components`, before `## Do's and Don'ts`. Don't insert them at random positions.

## Cross-skill ties

| Sibling skill | Relationship |
|---|---|
| `theme-system` | Owns the *architecture* of the design system (two-tier tokens, three-mode contract, theme.css organization). This skill owns the *document* that describes that architecture. They compose: when you ship new theme work via `theme-system`, you maintain its `DESIGN.md` via this one. |
| `generate-consistent-og-images` | Reads `imagery:` extension from `DESIGN.md`. If `DESIGN.md` is missing, that skill calls back into this one. |
| `astro-knots` | Defines the family of sites that should each have a `DESIGN.md`. When scaffolding a new Astro Knots site via that skill, hand off to this one to author the first-pass `DESIGN.md` after `Brand & Style` is decided. |
| `open-graph-share-seo-geo` | The delivery side of imagery (CDN host, headers, JPEG-over-WebP, the `og:image:type` invariant). Cares that imagery *exists*; doesn't care how it was generated. Composes with the `imagery:` extension owned by `generate-consistent-og-images` but documented in `DESIGN.md`. |
| `context-vigilance` | Governs *how* we document in `context-v/` (specs, blueprints, prompts, plans). `DESIGN.md` lives at the project root, not in `context-v/`, because it's product-facing — but the same discipline (sense-make first, mention the why, keep it current) applies. |

## See also

- `templates/design-md-scaffold.md` — the canonical empty-file scaffold for a new `DESIGN.md`. Drop in, fill in the ★-marked fields, delete the placeholder values, author the prose.
- `content-farm/splash/DESIGN.md` — the canonical full-example, including the off-spec `imagery:` extension.
- Google Stitch spec — <https://github.com/google-labs-code/design.md>
- Spec text — <https://github.com/google-labs-code/design.md/blob/main/docs/spec.md>
- Example DESIGN.md files in the spec repo — `examples/atmospheric-glass`, `examples/paws-and-paths`, `examples/totality-festival`
