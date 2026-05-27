---
name: spawn-internal-links
description: Examine every existing page on the site, build a semantic map across pillars, and add missing internal links so the site becomes a semantic graph anchored on clear topical pillars. Use this skill whenever the user asks to "add internal links", "build internal linking", "build a semantic graph", "link related pages", "strengthen topical authority", "fix orphan pages", "add pillar linking", or wants hub-and-spoke linking between pillars, hubs, and supporting content. Output is an edit list (proposed link insertions) plus optionally direct edits to page source files.
user-invocable: true
argument-hint: "[optional: pillar name]"
license: MIT
allowed-tools: WebSearch,Bash,Read,Edit,Write,Glob,Grep
---

# Overgrow — Spawn Internal Links (Semantic Graph)

This skill turns a flat set of pages into a **semantic graph** organized around pillars. It maps every page to its pillar(s), builds the hub-and-spoke links that should exist (pillar ↔ supporting pages, supporting ↔ supporting where topically adjacent), and proposes the insertions needed to close the gaps.

## Prerequisites

1. Read `.overgrow/inventory.md`. If missing, run `init` first.
2. Read `.overgrow/audit.md` if present — orphan and dead-end flags are the primary targets.
3. Parse `$ARGUMENTS`: if a pillar name is given, scope to it. Otherwise run across all pillars.

## Reference knowledge

Before mapping, read from the plugin's `knowledge/` directory:

- `knowledge/geo.md` — authority, topical clusters, and internal-link sections. The hub-and-spoke / pillar-cluster pattern and anchor-text rules live here.
- `knowledge/pages.md` — H-tag and content-structure rules that the link anchors should align with.

If those files are not reachable, fall back to the summary below but prefer the reference.

## Model of the semantic graph

- **Pillar pages** are topical hubs — one per semantic pillar identified in the inventory. They define a topic and link out to every supporting page.
- **Supporting pages** are narrower pages (blog posts, case studies, feature pages, guides, comparison pages) that each cover a sub-intent of the pillar.
- **Cross-links** connect supporting pages to sibling supporting pages when their sub-intents are topically adjacent.
- **Conversion pages** (pricing, contact, demo) sit outside pillars and should be linked from every pillar + most supporting pages via a consistent CTA pattern.
- **Orphans** are pages with zero inbound links from other content pages. Every non-utility, non-legal page should have at least 2 inbound content links.

## Procedure

1. Build a page-to-pillar map. Each content page belongs to exactly one primary pillar (from the inventory). It may optionally be tagged to one secondary pillar.
2. For each pillar, pick the **pillar hub page**. Usually the inventory already identifies it. If missing, flag it: the user needs to spawn one with `spawn-pages` (for solutions/feature pillars) or `spawn-blogs` (for topic pillars with a "what is X" hub).
3. For each page, compute its current outbound internal links (from its source) and inbound internal links (from other sources pointing to its route).
4. For each page, determine the target set of internal links it should contain:
   - Every supporting page links to its pillar hub (at least once, in the intro or an early section).
   - The pillar hub links to every supporting page (typically in a curated list or contextually within the body).
   - Supporting pages link to 1-3 sibling supporting pages where sub-intents overlap (e.g. a comparison post links to the integration post for the same tool).
   - Every content page links to the primary conversion page (pricing, demo, or signup) at least once.
   - Every content page links to the closest relevant feature or solution page when it mentions a capability by name.
5. Diff current vs. target. Emit one edit per missing link.
6. For each proposed edit, pick an insertion point that reads naturally — never append a stranded list of links at the bottom of an article unless it's a legitimate "related posts" block.
7. Choose anchor text that is **descriptive and keyword-aware**: use the target page's primary keyword or a natural phrase containing it. Never "click here", "read more", "this article", or a raw URL.
8. Avoid over-linking: cap at roughly 1 link per ~150 words of body copy. Cap any single page at 8-10 outbound internal links unless it's a pillar hub.
9. Never link to routes that do not exist in `.overgrow/inventory.md`. If a target page is missing, flag it as a `spawn-pages` or `spawn-blogs` candidate instead of emitting a broken link.

## Output

Write `.overgrow/internal-links.md`:

```markdown
# Overgrow — Internal Link Plan

_Run: <YYYY-MM-DD>_
_Scope: <all | pillar>_

## Pillar map

### <Pillar>
- Hub: <route> — <source path>
- Supporting:
  - <route> — <source path>
  - ...

## Proposed insertions

### <Source route> (<source path>)

- **Insert:** link to `<target route>` with anchor `"<anchor text>"` — near `"<excerpt from source that identifies the insertion point>"`
  - Reason: <e.g. "supporting → pillar hub; currently orphan from pillar">
- ...

## Orphan pages after plan

<routes that will still have < 2 inbound content links even after insertions — candidates for new supporting content or reconsideration of placement>

## Missing targets

<list of would-be link targets that do not exist yet — feed these into `spawn-pages` or `spawn-blogs`>
```

If the user explicitly asks to **apply** the insertions, make the edits directly in the source files. Otherwise leave them as a plan and let the user review.

## Constraints

- Only edit markdown/MDX/JSX source files. Do not touch generated HTML.
- Preserve the file's existing link style (markdown links for `.md/.mdx`, JSX anchor or `<Link>` for React routes, etc.). Match the framework's idiom.
- Do not modify nav, footer, or layout components — those are cross-cutting and belong to a different change set.
- Do not insert reciprocal links that already exist from other directions — check both sides.

## What this skill does NOT do

- Does not add external backlinks (that's off-site link building, out of scope).
- Does not rewrite body copy beyond inserting a link phrase or a short sentence when an insertion requires one.
- Does not create pages. If a needed hub or target does not exist, flag it for `spawn-pages` or `spawn-blogs`.