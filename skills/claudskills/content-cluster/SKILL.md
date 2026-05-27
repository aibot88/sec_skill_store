---
name: content-cluster
description: SEO content cluster strategy — design pillar pages with 10-20 satellite articles, internal link maps, and keyword hierarchies. Build topical authority on note through organized content architecture. The systematic approach to dominating search for your niche.
---

# Content Cluster Designer

Build topical authority through organized content architecture — dominate search for your niche.

## When to Activate

- User says `/cluster` or `/cluster {pillar_topic}`
- User asks "plan a content cluster"
- User asks "how do I build topical authority?"
- User wants to systematically improve note SEO

## Prerequisites

- `~/.content-autopilot/profile.json` must exist
- `~/.content-autopilot/content-history.json` (to map existing content)

## Commands

### `/cluster {pillar_topic}` — Design a cluster around a pillar topic
### `/cluster map` — Visualize existing content as clusters
### `/cluster gaps` — Find missing articles in existing clusters
### `/cluster link-map` — Generate internal linking recommendations

## Workflow

### Step 1: Define Pillar Topic

```
Content Cluster for: "{pillar_topic}"

Pillar page: The comprehensive guide to {topic}
  Target keyword: "{primary_keyword}"
  Length: 5,000-10,000 chars (most comprehensive article)
  Purpose: The definitive resource — links to all satellite articles

Satellite articles: 10-20 focused sub-topics
  Each targets a long-tail keyword
  Each links back to the pillar page
  Each links to 2-3 related satellites
```

### Step 2: Research Sub-Topics

Use WebSearch to identify sub-topics:
```
Search: "{pillar_topic} guide"
Search: "{pillar_topic} topics"
Search: "{pillar_topic} questions"
Search: "People Also Ask" for "{pillar_topic}"
```

### Step 3: Generate Cluster Map

```
============================================
  Content Cluster: "{pillar_topic}"
============================================

PILLAR: "{pillar_article_title}"
  Keyword: "{primary_keyword}"
  Status: {exists / to create}
  |
  ├── Satellite 1: "{title}" — "{long_tail_keyword}"
  │   Status: {exists / to create} | Internal links: pillar, S3, S5
  │
  ├── Satellite 2: "{title}" — "{keyword}"
  │   Status: {to create} | Internal links: pillar, S1, S4
  │
  ├── Satellite 3: "{title}" — "{keyword}"
  │   ...
  │
  ... (10-20 satellites)
  │
  └── Satellite N: "{title}" — "{keyword}"

--- Link Structure ---
  Pillar → links to ALL satellites
  Each satellite → links to pillar + 2-3 related satellites
  Total internal links: ~{count}

--- Existing Content Mapping ---
  Already written: {count} articles match this cluster
  To create: {count} new articles needed
  Gap priority: {highest-value missing article}

============================================
```

### Step 4: Prioritized Creation Plan

```
Creation priority (by SEO value):

1. [HIGH] PILLAR: "{title}" — must exist first
2. [HIGH] "{satellite}" — high search volume keyword
3. [HIGH] "{satellite}" — fills biggest content gap
4. [MEDIUM] "{satellite}" — medium competition
...
10. [LOW] "{satellite}" — low volume but completes cluster

Estimated time to complete cluster: {N} articles over {N} weeks
Use /batch 7 to create satellite articles efficiently.
```

## Integration with Other Skills

- **seo-optimizer**: Keyword research for each satellite
- **batch-generator**: Create satellites in weekly batches
- **content-writer**: Write with internal linking instructions
- **content-analytics**: Track cluster completion and performance
- **content-refresh**: Refresh pillar page as satellites are added

## Quality Gate

- [ ] Pillar topic is broad enough for 10+ satellites
- [ ] Each satellite targets a unique long-tail keyword
- [ ] Internal link structure is bidirectional
- [ ] Existing content is mapped before creating duplicates
- [ ] Creation priority is based on SEO value, not arbitrary order
