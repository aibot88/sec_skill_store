---
name: competitor-intelligence
description: >
  Competitor analysis, competitor SEO, who ranks for, competitive audit, compare my SEO,
  competitor gap. Covers content gaps, technical SEO comparison (observable signals),
  SERP feature ownership, AI citation pattern observation, and qualitative link
  opportunity mapping. Does NOT report numerical backlink counts, domain authority,
  organic traffic, or actual AI citation rates — those require a backlink / traffic /
  AI-platform MCP (Path B).
argument-hint: "[competitor URL or domain] [--non-interactive] [--resume <run-id>]"
allowed-tools: Read Glob Grep Write Bash WebFetch WebSearch Agent
---

# Competitor Intelligence Skill

Perform a competitor SEO analysis via observable signals. Every finding includes a concrete, prioritized action. Be honest about what's measured vs. observed vs. requiring Path B integration.

## Cross-model note

Works identically on Opus 4.7 / Sonnet 4.6 / Haiku 4.5. Opus/Sonnet batch WebFetch calls + WebSearch queries in parallel. Haiku may prefer sequential for large competitor sets.

## Execution: parallel-first

- **Phase 1B (digital competitor discovery)**: WebSearch per target keyword independent — batch
- **Phase 2A (competitor top pages)**: WebSearch per (competitor × keyword) pair independent — batch
- **Phase 2C (content depth per top gap)**: WebFetch per gap URL independent — batch
- **Phase 3 (technical comparison)**: WebFetch per competitor independent — batch
- **Phase 4 (link opportunities)**: WebSearch per competitor independent — batch
- **Phase 5 (SERP features)**: WebSearch per target keyword independent — batch
- **Phase 6 (AI citation patterns)**: WebSearch per keyword independent — batch

## Capability Honesty

Read `references/CAPABILITIES.md`. Key constraints for this skill:
- **Backlink counts + referring domains** require Ahrefs / Majestic / Semrush / Moz — Path B
- **Domain authority / Domain Rating** same link-graph dependency — Path B
- **Organic traffic estimates** require Similarweb / Semrush — Path B
- **Actual AI citation rates in ChatGPT / Perplexity / Gemini** require direct AI-platform APIs — Path B
- **What this skill DOES observe**: competitor content (WebFetch), SERP feature ownership (WebSearch), schema markup (parsed from fetched HTML), content patterns that earn AI citations (WebSearch surfaces AI Overviews + related content)

Report observable signals; mark gaps in `measurement_gaps[]`; never fabricate numbers.

## Mode Flags

- `--non-interactive` — Skip confirmation prompts, use defaults, emit trailing JSON
- `--resume <run-id>` — Load `.seo/state/<run-id>.json` and continue from last saved phase

---

## Pre-Flight: Gather Inputs

Before starting, collect from the user. Do not proceed without all three:

1. **Target site URL** — the domain to benchmark
2. **2-3 known competitors** — direct business competitors
3. **5-10 target keywords** — queries they most want to win

If only a URL is provided, ask:
> "Provide 2-3 competitors already known, plus 5-10 keywords to rank for. The analysis will also discover *digital* competitors — sites actually beating the target site in search, which are often different from direct business competitors."

In `--non-interactive` mode, use reasonable defaults and record unanswered items.

---

## Phase 1: Competitor Identification

### 1A — Confirm Known Competitors

Accept the user's 2-3 competitors. Validate each URL loads via WebFetch (head-level check).

### 1B — Discover Digital Competitors

Digital competitors rank in top 10 for target keywords regardless of whether they're direct rivals. For each target keyword (in parallel):

```
WebSearch("[keyword]")
```

Collect every domain in the top 10 across all keyword searches. Rank by keyword overlap. Top 3-5 recurring domains (excluding user's own) are digital competitors.

Present combined list:

| # | Competitor | Type | Overlapping Keywords |
|---|-----------|------|---------------------|
| 1 | example.com | Business + Digital | 8 of 10 |
| 2 | blog-rival.com | Digital only | 6 of 10 |
| 3 | toolsite.io | Digital only | 5 of 10 |

Ask user to confirm which to include (recommend 3). Save Phase 1 checkpoint.

---

## Phase 2: Content Gap Analysis

### 2A — Map Competitor Top Pages (parallel)

For each confirmed competitor × target keyword pair:

```
WebSearch("site:competitor.com [keyword]")
WebSearch("site:competitor.com")
```

Build a list of each competitor's top-performing URLs and the topics they cover.

### 2B — Identify Content Gaps

Compare competitor topic lists against the user's site. Classify each gap:
- **Missing entirely** — user has no page on the topic
- **Thin coverage** — user has a page but significantly less comprehensive
- **Format gap** — competitor uses a superior format (calculator, tool, video, infographic)

### 2C — Assess Content Depth (parallel WebFetch)

For the top 5 content gaps, WebFetch the competitor's page. Evaluate:
- Word count (approximate from fetched content)
- Heading structure (H2/H3 depth)
- Use of images, tables, embedded media
- Presence of original data, quotes, case studies
- Internal linking density

### 2D — Identify 10x Content Opportunities

A "10x opportunity" is a topic where:
1. Competitors rank but content is mediocre (thin, outdated, or poorly structured)
2. The user has domain expertise or data that could produce significantly better
3. Search signals (SERP feature presence, autocomplete prominence) justify the investment

Flag top 3 10x opportunities with rationale.

---

## Phase 3: Technical Comparison (observable signals)

WebFetch the homepage + one key landing page from each competitor. Benchmark:

### 3A — Page-Speed Risk Factors (NOT numerical CWV)

Load behavior via WebFetch headers + HTML inspection. Note:
- Minified assets, lazy-load attributes, CDN hints
- Large hero images / render-blocking scripts

Do NOT report numerical CWV scores — that requires Lighthouse/PSI (Path B). Report as risk factors.

### 3B — Mobile Experience Signals

HTML inspection:
- Viewport meta tag
- Responsive CSS indicators
- Touch-friendly element sizing

### 3C — Schema Markup

Parse `<script type="application/ld+json">` from fetched HTML. Catalog schema types per competitor:
- Organization / LocalBusiness
- Article / BlogPosting
- Product / Review
- FAQ / HowTo
- BreadcrumbList
- VideoObject

Flag schema types competitors use that the user does not.

### 3D — URL Structure

| Site | Pattern | Depth | Keyword in URL |
|------|---------|-------|----------------|
| user.com | /blog/post-title | 2 levels | Sometimes |
| comp1.com | /guides/category/topic | 3 levels | Always |

---

## Phase 4: Qualitative Link Opportunity Mapping

**Honest framing**: This skill cannot measure backlink counts, referring domain counts, or domain authority. Those require Ahrefs / Majestic / Semrush / Moz APIs (Path B). Instead, this phase identifies **observable link opportunities** via mentions in WebSearch.

### 4A — Discover Observable Mentions

For each competitor (in parallel):

```
WebSearch('"competitor.com" -site:competitor.com')
WebSearch('"competitor brand name" recommendation OR review OR resource')
```

Collect referring domains that appear in results. Cross-reference across competitors to find sites that mention multiple competitors but not the user — these are the highest-value observable opportunities.

### 4B — Classify Link Opportunities

For each opportunity:
- **Source type**: editorial, resource page, directory, guest post, mention
- **Relevance**: topical relatedness (High / Medium / Low)
- **Feasibility**: qualitative (High / Medium / Low)
- **Suggested tactic**: specific approach to earn the link

See `references/link-building-tactics.md` for detailed playbooks.

### 4C — Prioritize

Sort by combined score of (relevance × feasibility). Present top 10.

**Measurement gap**: Actual backlink counts, referring domains, and DA/DR numbers require Path B integrations — surface in `measurement_gaps[]`.

---

## Phase 5: SERP Feature Ownership

Map who currently owns SERP features for each target keyword (parallel WebSearch).

### 5A — Featured Snippets

For each target keyword:
```
WebSearch("[keyword]")
```

Note whether a featured snippet appears + who holds it. Record format (paragraph / list / table) + approximate content.

### 5B — Rich Results

Check for: FAQ accordions, HowTo steps, review stars, product cards, video carousels, image packs. Map which competitors own each type for which keywords.

### 5C — People Also Ask

Collect PAA questions that appear. Note which competitors' pages are surfaced. These questions are direct content-brief opportunities.

### 5D — Knowledge Panel Presence

Check whether any competitor has a knowledge panel. If user doesn't, note steps to establish one (Google Business Profile, Wikidata, structured data).

### 5E — Opportunity Map

| Keyword | Feature | Current Owner | User Eligible? | Action to Win |
|---------|---------|--------------|----------------|---------------|
| best crm | Featured snippet (list) | comp1.com | Yes | Add H2 list format |
| crm pricing | FAQ rich result | comp2.com | Yes | Add FAQPage schema |

---

## Phase 6: AI Citation Pattern Observation

**Honest framing**: This phase observes **what content patterns earn AI citations** — NOT the user's or competitors' actual citation rates. Measuring actual citation rates requires direct AI-platform API integration (Path B).

### 6A — Observe AI-Cited Content via WebSearch

For each target keyword:

```
WebSearch("[keyword]")
```

If Google surfaces an AI Overview, note:
- Which domains get cited
- What content format was cited (FAQ? comparison table? structured list?)
- What content patterns the cited passages share

Also search for related patterns:

```
WebSearch("[keyword] site:perplexity.ai")
WebSearch("[keyword] what does ai say")
```

### 6B — Catalog Observable Citation Patterns

For competitor content that gets cited by AI Overviews (observable via WebSearch), investigate:
- **Format**: Q&A, comparison table, structured list, bolded definition
- **Schema**: does the page use FAQPage, HowTo, or similar schema?
- **Structure**: how does the cited section read? Question heading + direct-answer lead?
- **Authority signals**: author byline, citations, original data

### 6C — Identify AI-Extractability Gaps (user vs. competitors)

For keywords where a competitor is cited by AI but the user isn't:
- What content patterns do the cited passages share?
- Does the user's equivalent content match those patterns?
- What's the specific structural gap?

This is NOT a "how often am I cited" score — it's a diagnostic of *why my content isn't structurally ready to be cited*.

### 6D — Build AEO Action Plan

Reference `references/aeo-playbook.md` and `skills/aeo-optimizer` Phase 1 (AI-Extractability Content Linter) for detailed structural rules.

For each observable gap, recommend a specific action: reformat with question-format H2, add direct-answer lead, add FAQ schema, add comparison table, add original data.

**Measurement gap**: Actual AI citation rates across ChatGPT / Perplexity / Gemini / Claude / Copilot require direct platform APIs — surface in `measurement_gaps[]`.

---

## Output Format

```
# Competitor Intelligence Report: [Your Site] vs. [Competitors]
# Generated: [Date]

## Executive Summary
[3-5 sentence overview of competitive position, biggest observable gaps, biggest opportunities.
Name the measurement gaps honestly.]

## Competitor Overview (observable signals)
| Metric | Your Site | Comp 1 | Comp 2 | Comp 3 |
|--------|-----------|--------|--------|--------|
| Type | — | Business | Digital | Digital |
| Keyword Overlap | — | 8/10 | 6/10 | 5/10 |
| Content Depth Signal | [qualitative] | [qualitative] | [qualitative] | [qualitative] |
| Schema Types Used | [count] | [count] | [count] | [count] |
| SERP Features Owned | [count] | [count] | [count] | [count] |
| AI Overview Citations Observed | [count] | [count] | [count] | [count] |

## Measurement Gaps (Path B integrations would unlock)
- Backlink counts + DR/DA: Ahrefs / Majestic / Semrush / Moz MCP
- Organic traffic estimates: Similarweb / Semrush MCP
- Actual AI citation rates across all platforms: direct AI-platform API MCPs

## Content Gaps (observable)
1. **[Topic]** — Competitor X has [URL], user has nothing. **Action**: [specific content to create].
2. ...

## 10x Content Opportunities
1. **[Topic]** — Existing competitor content is [weakness]. User can win by [strategy].

## Technical SEO Comparison
[Observable technical signals; code-level risk factors for page speed — not numerical CWV]

## Qualitative Link Opportunities
1. **[Referring Site]** — Observed to link to Comp 1 + Comp 2 not user. Type: [resource page]. **Tactic**: [outreach approach].

## SERP Feature Opportunities
1. **[Keyword]** — Featured snippet held by [competitor]. Format: [list/table/paragraph]. **Strategy**: [restructure to win snippet].

## AI Citation Pattern Observations
[What content patterns competitors use that get cited — NOT their citation rates]

### Observable Gaps
- [Keyword] — Competitor X cited by Google AI Overview with [format]. User's equivalent page missing [specific structural pattern].

### User AI-Extractability Action Plan
1. **[Action]** — Target: [page]. Pattern to apply: [specific structural rule]. See skills/aeo-optimizer Phase 1.

## Prioritized Action Plan
Sorted by (Impact / Effort). Max 15 items.

| # | Action | Category | Impact | Effort | Timeline |
|---|--------|----------|--------|--------|----------|
| 1 | [action] | Content Gap | High | Low | 1 week |
| 2 | [action] | SERP Feature | High | Low | 2 days |
...
```

---

## Execution Notes

- **Be specific**: "add a comparison table with pricing columns to the /crm-guide page, matching the format comp1.com uses at /pricing" beats "improve content"
- **Cite sources**: include competitor URL when referencing their page
- **Quantify observable signals**: "competitor ranks #1 for 7 of 10 keywords" is observable; "competitor has 45,000 backlinks" is not (without Path B)
- **Cross-reference plugin resources**: point to `references/aeo-playbook.md` for AI strategies and `references/link-building-tactics.md` for link playbooks
- **Prioritize ruthlessly**: no more than 15 action items. Rank by impact × feasibility.
- **Flag time-sensitive opportunities**: outdated competitor content, weakly-held SERP features
- **Re-run quarterly**: recommend 90-day cadence to track progress
- **Surface measurement gaps honestly**: never invent numbers for things requiring Path B
