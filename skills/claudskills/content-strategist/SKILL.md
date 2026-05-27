---
name: content-strategist
description: >
  Content strategy, content gaps, editorial calendar, topical authority, content plan,
  what should I write about. Covers topical authority mapping, gap analysis, brief
  generation, and 12-week editorial calendar. Most of this skill is strategic reasoning
  over observable content + WebSearch — no Path B dependencies except for Phase 3 traffic
  scoring (requires GSC/GA data, which the user can paste in or skip).
argument-hint: "[site URL or topic area] [--non-interactive]"
allowed-tools: Read Glob Grep Write Bash WebFetch WebSearch
---

# Content Strategist

Build a content strategy that establishes topical authority, fills competitive gaps, and produces "last click" content — pages so thorough that readers never need to return to the search results.

Work through every phase in order. Present findings and recommendations in structured tables and outlines the user can act on immediately.

## Cross-model note

Works identically on Opus 4.7 / Sonnet 4.6 / Haiku 4.5. Opus/Sonnet batch content-file Reads + competitor WebSearch calls in parallel. Haiku may prefer sequential for large content inventories.

## Execution: parallel-first

- **Phase 3 content audit**: per-page Reads independent — batch
- **Phase 2.3 + Phase 4.1 competitor topical coverage**: WebSearch per competitor independent — batch
- **Phase 4.2 question gaps**: WebSearch for PAA independent — batch
- **Phase 5 content brief generation**: per-brief reasoning, serializable (synthesis-heavy)

## Capability Honesty

Read `references/CAPABILITIES.md`. Key notes:
- **Phase 3.1 "Traffic Performance" scoring** requires the user to paste in GSC or GA data, OR integrate a GSC MCP (Path B). Without data, skip traffic scoring and rely on the other four dimensions.
- **Phase 4 gap analysis via observable signals** is fully supported (WebSearch + WebFetch).
- **"Publishing X posts per week yields Y traffic"** predictions are directional, not measured.

---

## Phase 1: Business Understanding

Gather the following before any analysis begins. Ask the user directly for
anything that cannot be inferred from the site.

### 1.1 Business Profile
- Business name, URL, and industry vertical
- Core products or services (ranked by revenue priority)
- Unique selling propositions — what differentiates this business?
- Geographic focus (local, national, international)

### 1.2 Target Audience
- Primary audience segments (demographics, job titles, pain points)
- Buyer journey stages the content must serve (awareness, consideration, decision)
- Language, tone, and reading level expectations

### 1.3 Current Content Inventory
- CMS platform and sitemap URL (request or crawl)
- Total indexed pages (check via `site:domain.com`)
- Content types already in use (blog, landing pages, docs, video, tools)

### 1.4 Content Creation Resources
- Who writes? (in-house team, freelancers, agency, AI-assisted)
- Publishing cadence today (posts per week/month)
- Budget constraints or approval workflows worth noting

---

## Phase 2: Topical Authority Mapping

### 2.1 Define Core Topics
Identify 3-7 core topics the business must own in search. Each core topic
becomes a **pillar page** — a comprehensive, long-form resource.

### 2.2 Hub-and-Spoke Architecture
For every pillar, map a cluster of **spoke pages** (supporting articles) using
this structure:

```
Pillar: [Core Topic]
  ├── Spoke: [Subtopic A] — targets long-tail keyword
  ├── Spoke: [Subtopic B] — targets question keyword
  ├── Spoke: [Subtopic C] — targets comparison keyword
  └── Spoke: [Subtopic D] — targets how-to keyword
```

Each spoke links back to the pillar. The pillar links out to every spoke.
Cross-link spokes where topically relevant.

### 2.3 Competitor Topical Coverage
For the top 3-5 organic competitors:
- List topics they cover that the user does not
- Identify topics the user covers more deeply (defend these)
- Note any topical clusters competitors have built that rank well

### 2.4 Topical Gap Summary
Produce a table:

| Topic | User Coverage | Competitor Coverage | Priority | Action |
|-------|--------------|--------------------:|----------|--------|
| ...   | None / Thin / Strong | Strong / Moderate | High / Med / Low | Create / Expand |

---

## Phase 3: Content Audit (Existing Content)

For every existing page worth evaluating, score on five dimensions.

### 3.1 Scoring Criteria

**Traffic Performance** (1-5) — *requires GSC/GA data or Path B GSC MCP integration*
- 5 = growing traffic trend over 6 months
- 3 = stable
- 1 = declining or near-zero traffic
- **If user has not provided traffic data**, skip this dimension and score across the other four only. Recommend integrating a Google Search Console MCP for ongoing traffic-aware scoring.

**Content Quality** (1-5)
- Depth and completeness vs. top-ranking competitors
- Originality (unique data, insights, or angles)
- Readability (clear structure, scannable, no walls of text)

**E-E-A-T Compliance** (1-5)
- Experience, Expertise, Authoritativeness, Trustworthiness
- Score using the criteria in `eeat-checklist.md`
- Check for author bios, citations, credentials, first-hand experience

**AEO Readiness** (1-5)
- Semantic chunking with clear H2/H3 hierarchy
- Quotable statements (concise, factual sentences AI can extract)
- FAQ sections with question-formatted headings
- Structured data / schema markup present

**Keyword Coverage** (1-5)
- Primary keyword targeted and present in title, H1, URL
- Secondary keywords covered in subheadings and body
- Search intent alignment (does the content match what the user wants?)

### 3.2 Audit Output Table

| URL | Traffic | Quality | E-E-A-T | AEO | Keywords | Total | Recommendation |
|-----|--------:|--------:|--------:|----:|---------:|------:|----------------|
| /page-a | 4 | 3 | 4 | 2 | 5 | 18 | Update |
| /page-b | 1 | 2 | 1 | 1 | 2 | 7  | Remove |

### 3.3 Recommendations

Assign every audited page one action:

- **Keep** — Score 20-25. Performing well. Monitor, no immediate changes.
- **Update** — Score 14-19. Solid foundation but needs a refresh: add new data,
  improve formatting, expand thin sections, add schema markup, improve AEO
  formatting.
- **Consolidate** — Multiple pages scoring below 14 on the same topic. Merge
  into one authoritative page. Redirect old URLs to the consolidated page.
- **Create** — No existing page covers this important topic. Net-new content
  required.
- **Remove** — Score below 8, or content is thin/duplicate with no strategic
  value. Redirect or noindex.

---

## Phase 4: Content Gap Analysis

### 4.1 Topic Gaps
Topics competitors rank for that the user has zero coverage on. Pull from
Phase 2.3 competitor analysis.

### 4.2 Question Gaps
Questions the target audience asks (People Also Ask, forums, support tickets)
that the user's content does not answer. These are high-value AEO targets.

### 4.3 Search Intent Gaps
Map existing content by intent type:

| Intent Type | User Pages | Competitor Pages | Gap? |
|-------------|-----------|-----------------|------|
| Informational | 45 | 60 | Yes |
| Commercial | 10 | 25 | Yes |
| Transactional | 8 | 12 | Moderate |
| Navigational | 5 | 5 | No |

If the user has only informational content but competitors serve commercial
and transactional intent, flag this as a critical gap.

### 4.4 Format Gaps
Content formats competitors use that the user does not:
- Interactive tools or calculators
- Video content or embeds
- Comparison tables
- Templates or downloadable resources
- Infographics or original data visualizations

---

## Phase 5: Content Brief Generation

For every piece of content recommended in Phases 3-4, produce a structured
brief.

### Brief Template

```
CONTENT BRIEF
=============
Target Keyword:       [primary keyword]
Secondary Keywords:   [3-5 related terms]
Search Intent:        [informational | commercial | transactional | navigational]
Recommended Format:   [guide | listicle | comparison | tool | FAQ | case study | how-to]
Suggested Word Count: [based on top-5 competitor average, +10-20%]

H1 TITLE OPTIONS
1. [Option A — includes primary keyword]
2. [Option B — question format for AEO]
3. [Option C — number/data-driven hook]

OUTLINE (H2/H3 with keyword mapping)
H2: [Section Title] — targets [keyword]
  H3: [Subsection] — targets [long-tail keyword]
  H3: [Subsection] — targets [question keyword]
H2: [Section Title] — targets [keyword]
  H3: ...
H2: FAQ — targets PAA questions
  H3: [Question 1]?
  H3: [Question 2]?

INTERNAL LINKING PLAN
- Link TO:    [list existing pages this content should link to]
- Link FROM:  [list existing pages that should add links to this content]

SCHEMA MARKUP
- Recommended types: [Article, FAQ, HowTo, etc.]

AEO FORMATTING REQUIREMENTS
- Use question-format H2/H3 headings where appropriate
- Lead each section with a direct, quotable 1-2 sentence answer
- Include a "Key Takeaway" or "Quick Answer" box at the top
- Add FAQ section with concise Q&A pairs
- Use statistics and data points that AI systems can cite

CTA RECOMMENDATION
- Primary CTA: [what action should the reader take?]
- CTA placement: [inline, end of article, sidebar, sticky]
```

---

## Phase 6: 12-Week Content Calendar

### 6.1 Content Mix — 70/20/10 Rule

| Category | Share | Description | Examples |
|----------|------:|-------------|----------|
| Foundation | 70% | Proven formats, reliable traffic drivers | How-to guides, FAQ pages, glossary entries, comparison posts |
| Growth | 20% | Builds on foundation with moderate risk | Original research, expert roundups, detailed case studies |
| Innovation | 10% | Experimental, high-risk/high-reward | Interactive tools, controversial takes, new content formats |

### 6.2 Calendar Format

Present the calendar as a table with one row per content piece:

| Week | Pub Date | Title | Target Keyword | Type | Mix | Author | Links To | Promotion |
|------|----------|-------|---------------|------|-----|--------|----------|-----------|
| 1 | YYYY-MM-DD | ... | ... | Guide | 70% | ... | /pillar-a | Social, Email |
| 1 | YYYY-MM-DD | ... | ... | FAQ | 70% | ... | /pillar-b | Social |
| 2 | YYYY-MM-DD | ... | ... | Research | 20% | ... | /pillar-a | Outreach, Social |

### 6.3 Calendar Rules
- Publish pillar pages before their supporting spokes
- Distribute content evenly across topic clusters (do not front-load one topic)
- Schedule updates and relaunches alongside new content
- Align with seasonal or industry events where relevant
- Include at least one AEO-optimized FAQ or Q&A piece per week

---

## Phase 7: Content Relaunch Strategy

### 7.1 Relaunch Candidates
Pull from Phase 3 audit — any page marked **Update** with a traffic score of
3+ is a relaunch candidate. Prioritize pages that:
- Rank positions 4-20 (within striking distance of page 1 or top 3)
- Target high-volume keywords
- Have existing backlinks worth preserving

### 7.2 Relaunch Process
For each candidate:

1. **Refresh content** — Add new data, statistics, and examples from the
   current year. Remove outdated references.
2. **Expand coverage** — Compare against the current top-3 ranking pages. Add
   any sections or subtopics they cover that yours does not.
3. **Improve formatting** — Add table of contents, comparison tables, key
   takeaway boxes, and better visual hierarchy.
4. **Add schema markup** — Implement Article, FAQ, or HowTo structured data.
5. **Optimize for AEO** — Add question headings, direct answer leads, and
   quotable statistics.
6. **Update the published date** — Signal freshness to search engines.
7. **Promote as new** — Share on social, include in newsletters, conduct
   outreach for fresh links.

### 7.3 Relaunch Tracking
Track each relaunch with before/after metrics:
- Organic traffic (30/60/90 days post-relaunch)
- Keyword rankings for target terms
- Featured snippet or AI answer appearances
- Engagement metrics (time on page, bounce rate)

---

## Phase 8: "Last Click" Content Philosophy

Every piece of content produced under this strategy must aim to be the
**definitive resource** on its topic. If a user clicks through from search,
they should find everything they need — and never hit the back button.

### 8.1 Last Click Checklist

Apply to every content brief and review:

- [ ] **More complete** than any page currently ranking in the top 5
- [ ] **Original value** — unique data, proprietary insights, or first-hand
      experience not available elsewhere
- [ ] **Superior formatting** — scannable, well-structured, with visual aids
      (tables, diagrams, screenshots) where they add clarity
- [ ] **E-E-A-T compliant** — author credentials visible, sources cited,
      claims backed by evidence (see `eeat-checklist.md`)
- [ ] **AEO-ready** — structured so AI systems can extract accurate, attributed
      answers from the site's content
- [ ] **Actionable** — reader can implement advice immediately, not just
      understand theory
- [ ] **Current** — all data, links, and references verified within the last
      90 days

### 8.2 Quality Gate
Before publishing, every piece must pass the "Last Click" test:

> "If I were searching for this topic and landed on this page, would I need
> to check any other result?"

If the answer is yes, the content is not ready. Identify what is missing and
address it before publication.

---

## Output Checklist

Before delivering the final strategy, confirm every deliverable is present:

- [ ] Business profile and audience summary (Phase 1)
- [ ] Topical authority map with hub-and-spoke clusters (Phase 2)
- [ ] Content audit table with scores and recommendations (Phase 3)
- [ ] Content gap analysis with prioritized opportunities (Phase 4)
- [ ] Content briefs for all recommended new/updated content (Phase 5)
- [ ] 12-week content calendar with 70/20/10 mix (Phase 6)
- [ ] Relaunch candidates and process (Phase 7)
- [ ] Last Click quality checklist applied to all briefs (Phase 8)
