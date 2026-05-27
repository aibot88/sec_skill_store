---
name: link-building-strategy
description: >
  Link building, backlink strategy, link acquisition, outreach plan. Covers linkable
  asset identification, tactic selection, and 12-week outreach playbook with templates.
  This is a tactics generator — it does NOT measure the user's backlink profile,
  domain authority, referring domain counts, or competitor backlink gaps numerically.
  Those require an Ahrefs / Majestic / Semrush / Moz MCP (Path B). The user can still
  hand-paste exported data from those tools if they have it.
argument-hint: "[optional: path to Ahrefs/Moz export] [--non-interactive]"
allowed-tools: Read Glob Grep Write Bash WebSearch WebFetch
---

# Link Building Strategy Skill

Generate a complete link acquisition tactics playbook and a 12-week action plan. This skill is a **tactics generator + outreach system**, not a backlink analyzer. If the user wants numerical backlink profile data, direct them to a Path B MCP integration.

## Cross-model note

Works identically on Opus 4.7 / Sonnet 4.6 / Haiku 4.5. Most of this skill is reasoning + planning; WebSearch calls in Phase 2 parallelize cleanly across competitors.

## Execution: parallel-first

- **Phase 2 link gap discovery**: WebSearch calls per competitor independent — batch
- **Phase 3 linkable asset audit**: content file Reads in parallel
- **Phase 4 tactic selection**: reasoning step
- **Phase 5-7**: planning/template generation

## Capability Honesty

Read `references/CAPABILITIES.md`. Key constraints:
- **Numerical backlink counts / referring domains / DA/DR** require Ahrefs / Majestic / Semrush / Moz — Path B
- **"Expected DA from tactic X" estimates** cannot be verified without those tools — treated as directional, NOT measured
- **What this skill DOES**: identify linkable asset opportunities, generate outreach tactics + templates, structure a 12-week outreach cadence, observe link opportunities via WebSearch mentions

If the user pastes exported data from Ahrefs / Moz / Semrush, parse and use it. Without that data, the skill runs in qualitative mode.

---

## Phase 1: Current Link Profile Assessment (qualitative OR data-driven)

### If User Has Exported Backlink Data

If the user provides Ahrefs / Moz / Semrush / Ubersuggest exports or paste, parse and summarize:
- Total referring domains
- Total backlinks
- DA / DR score
- Top 10 linking domains by authority
- Toxic link patterns (spam farms, PBNs, irrelevant foreign domains)

Classify domains into qualitative tiers:

| Tier | Quality Label | Typical Examples |
|------|---------------|------------------|
| A | Premium | Major publications, .edu, .gov |
| B | Solid | Industry blogs, established sites |
| C | Low-mid | Small blogs, directories |
| D | Low/Risky | Spam farms, PBNs, foreign junk |

### If User Does NOT Have Exported Data

Run in qualitative mode. Ask the user:
- "Do you know of any recent backlinks to your site?"
- "Have you had any press mentions, guest post placements, or podcast appearances?"
- "Do you maintain any free tools, calculators, or original research that others might link to?"
- "Are you in any niche directories or industry lists?"

Recommend the user integrate a link-data MCP (Ahrefs / Majestic / Moz / Semrush) to unlock numerical assessment. In the meantime, proceed with qualitative planning.

### Toxic Link Check (only with data)

Flag patterns visible in the export:
- Domains with DA < 5 and no real content
- Sites in unrelated foreign languages with no topical connection
- Known link farms or PBN patterns
- Exact-match anchor text appearing suspiciously often

Recommend submitting a Google Disavow file if Tier D links exceed ~15% of total.

---

## Phase 2: Link Gap Analysis (observable via WebSearch)

### Step 1 — Identify Competitors

Use the 3 competitor URLs the user provides, or suggest top 3 ranking sites for the user's primary keyword (via WebSearch).

### Step 2 — Discover Observable Mentions (parallel WebSearch per competitor)

For each competitor:
```
WebSearch('"competitor.com" -site:competitor.com')
WebSearch('"competitor brand name" recommendation OR review OR resource')
```

Collect domains that appear in results and cross-reference across competitors to find sites linking to multiple competitors but not the user.

**Note**: This finds *observable mentions*, not a complete link graph. Comprehensive backlink audit requires Path B. Observable mentions are still the highest-leverage outreach targets — these are sites that already demonstrated willingness to link to similar content.

### Step 3 — Prioritize Opportunities

Rate each opportunity on a 1-5 scale:
- **Relevance** — How closely does the linking site match the target niche?
- **Authority signal** — Is the site clearly a well-known publication vs. a small blog? (qualitative without Path B)
- **Accessibility** — Does the site accept contributions, have a contact form, list an editor?
- **Link type potential** — Could a contextual, in-content link be earned?

Priority = (Relevance + Authority Signal + Accessibility + Link Type) / 4. Pursue 4.0+ first.

---

## Phase 3: Linkable Asset Audit

Links cannot be earned without something worth linking to.

### Existing Content Review

Evaluate the user's current content for link-worthiness. Strong linkable assets include:

- **Original research or data** — Surveys, studies, industry benchmarks
- **Comprehensive guides** — "Ultimate guide to X" that genuinely earns the title
- **Free tools or calculators** — Interactive resources people reference
- **Templates and frameworks** — Downloadable resources others cite
- **Infographics or visual data** — Shareable visual content
- **Controversial or unique opinions** — Strong takes that spark discussion

### Content Gap: What to Create

Recommend 3-5 new "citation magnet" ideas based on the user's industry:

1. **Original Data Play** — Survey customers or analyze internal data; publish findings with charts. Journalists and bloggers cite original data.
2. **The Definitive Resource** — Single best page on a subtopic, 3x better than what currently ranks.
3. **Free Tool or Calculator** — Even a simple spreadsheet hosted as a Google Sheet earns links.
4. **Named Framework** — Branded methodology (e.g., "The 3R Content Framework"). Named concepts get cited.
5. **Annual Report or Index** — Yearly state-of-the-industry report. Becomes a recurring link magnet.

### Branded Strategy Opportunities

Help the user coin a term or framework unique to their brand. Requirements:
- Simple and memorable (3-5 words max)
- Genuinely useful as a mental model
- Easy to reference in other people's content
- Searchable (someone who hears it can Google it and find you)

---

## Phase 4: Tactic Selection

Reference: `references/link-building-tactics.md` for expanded playbooks.

Based on the user's available time, budget, and business type, recommend 3-5 tactics.

### Tactic Menu

| # | Tactic | Effort | Success Signal (qualitative) |
|---|--------|--------|------------------------------|
| 1 | **Skyscraper Technique** | 15-20 hrs | Low-to-moderate hit rate; higher on genuine 10x content |
| 2 | **Broken Link Building** | 8-12 hrs | Low hit rate but warm prospects (they already linked) |
| 3 | **Moving Man Method** | 10-15 hrs | Moderate hit rate when replacing rebranded/shut-down resources |
| 4 | **Resource Page Link Building** | 5-8 hrs | Low-to-moderate; works best with strong topical fit |
| 5 | **Digital PR / Original Research** | 20-40 hrs | High authority when landed; lower frequency |
| 6 | **HARO / Media Requests** | 3-5 hrs/week | Moderate authority, steady cadence if you stay consistent |
| 7 | **Strategic Guest Posting** | 8-15 hrs | 10-30% acceptance on well-targeted niche pitches |
| 8 | **Link Reclamation** | 2-4 hrs | High hit rate on unlinked brand mentions — quick win |
| 9 | **Competitor Link Gap Outreach** | 10-15 hrs | Low hit rate but pre-qualified prospects |
| 10 | **Link Roundups** | 2-3 hrs/week | Low-to-moderate; compounds over time |
| 11 | **Podcast Guesting** | 3-5 hrs per appearance | Moderate-to-high booking rate in niche shows |
| 12 | **Testimonial Link Building** | 1-2 hrs | High hit rate — easy win for tools you actually use |
| 13 | **Content Transformation** | 5-10 hrs | Passive earning via distribution |
| 14 | **Local Community Links** | 2-5 hrs | High hit rate for local businesses |
| 15 | **Affiliate / Partner Programs** | 20+ hrs setup | Ongoing passive earning |

**Honest framing on success rates**: The rates above are qualitative ("low / moderate / high hit rate") because actual rates vary wildly by niche, pitch quality, and relationship building. Any percentage numbers in industry guides (e.g., "5-15% success") should be treated as ballpark, not measured.

For detailed descriptions and execution steps, consult `references/outreach-templates.md`.

---

## Phase 5: LLM Co-Citation Strategy (AEO-Specific)

Modern link building accounts for AI-generated answers. Links train the data AI models use to recommend brands.

### Goal: Get Mentioned Alongside Industry Leaders

1. **Publish comparison content** — "X vs Y vs [Brand]" articles. AI models learn brand-peer associations.
2. **Reddit and Quora presence** — Answer questions in niche threads; mention the product naturally where relevant. These platforms are heavily used as AI training data.
3. **Earn roundup mentions** — Get included in "Top 10 tools for X" and "Best resources for Y" articles.
4. **Third-party reviews** — G2, Capterra, Trustpilot, niche review sites. AI models reference these aggregators.
5. **Build cross-platform consensus** — If multiple independent sources mention the brand in similar context, AI models are more likely to recommend. Aim for consistent messaging across earned mentions.

---

## Phase 6: The 50/50 Plan

Link building fails when only creating content or only doing outreach. Split effort evenly.

### 50% — Creating Link-Worthy Content

- Publish 1 linkable asset every 2-4 weeks
- Each piece targets a specific tactic (data study for Digital PR, guide for Skyscraper)
- Quality over quantity

### 50% — Active Promotion and Outreach

- Outreach emails every week
- Track every email in a simple spreadsheet (date, recipient, tactic, status, result)
- Follow up exactly once, 5-7 days after first email

### Weekly Targets by Available Hours

| Monthly Hours | Weekly Outreach | Monthly Content | Expected Links (qualitative) |
|--------------|-----------------|-----------------|-----------------|
| 10 | 10-15 emails | 1 piece | Trickle |
| 20 | 20-30 emails | 1-2 pieces | Steady |
| 40 | 40-60 emails | 2-3 pieces | Strong cadence |
| 60+ | 60-100 emails | 3-4 pieces | Aggressive |

**Note**: Numerical link-count forecasts are unreliable without real measurement. The qualitative labels reflect observed cadence differences, not predictions.

---

## Phase 7: Outreach Templates

Six ready-to-use templates: broken link notification, skyscraper outreach, resource page pitch, guest post pitch, link reclamation request, roundup submission.

For all email templates with full text, consult `references/outreach-templates.md`.

**Always customize** with specific details. Never send a generic email.

---

## Output: 12-Week Link Building Plan

Generate a week-by-week plan tailored to available hours and selected tactics.

### Weeks 1-2: Foundation
- Phase 1 link profile assessment (qualitative if no data)
- Phase 2 link gap analysis via WebSearch
- Phase 3 linkable asset audit
- Set up outreach tracking spreadsheet
- Create target list of 50 prospects
- **Outreach**: 0 emails (prep)
- **Content**: Outline 1 linkable asset

### Weeks 3-4: First Outreach
- Start with highest-hit-rate tactics: link reclamation + testimonials
- Send first outreach batch
- Publish first linkable asset
- Submit to 3-5 link roundups
- Sign up for HARO / Connectively
- **Outreach**: 15-25 emails/week

### Weeks 5-6: Scale Up
- Launch first skyscraper or broken link campaign
- Follow up on unanswered emails from weeks 3-4
- Respond to 5+ HARO queries per week
- Engage in Reddit / Quora threads (Phase 5)
- **Outreach**: 20-30 emails/week
- **Content**: Publish second linkable asset

### Weeks 7-8: Diversify
- Resource page outreach
- First guest post pitches (3-5)
- Write 2-3 testimonials for tools the business uses
- Analyze what's working — double down on best-converting tactic
- **Outreach**: 25-35 emails/week

### Weeks 9-10: Optimize
- Review response rates — refine subject lines + templates
- Publish third linkable asset (original data or free tool)
- Pitch 2-3 podcasts
- Create comparison content for LLM co-citation (Phase 5)
- **Outreach**: 25-35 emails/week

### Weeks 11-12: Systematize
- Document repeatable process per tactic
- Build recurring monthly calendar
- Set up Google Alerts for brand mentions (link reclamation pipeline)
- Plan next quarter's linkable assets based on what earned most links
- **Outreach**: 30-40 emails/week

### 12-Week Outputs (Qualitative)

What you can track: outreach emails sent, replies received, mentions earned, confirmed new links, content published.

What requires Path B to track: total referring domain count, DA/DR change, numerical "DA improvement +2-5".

---

## Key Reminders

1. **Personalize every email.** Generic mass emails get ignored.
2. **Track everything.** Log every outreach email + outcome.
3. **Follow up once.** 5-7 days later. More than that is spam.
4. **Focus on relevance over authority.** A perfectly relevant DA 30 link often outperforms an irrelevant DA 60 link.
5. **Be patient.** Link building compounds over months.
6. **Never buy links.** Purchased links violate Google's guidelines.
7. **Honest about measurement.** Track what you can observe. Recommend Path B MCPs for numerical backlink data.
