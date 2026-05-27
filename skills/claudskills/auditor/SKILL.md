---
name: auditor
description: "Use when: auditing a website URL or codebase, checking site health score, SEO audit, performance audit, security scan, accessibility audit, mobile audit, broken links, meta tags, structured data. Triggers: 'audit my website', 'check https://...', 'what's wrong with my site', 'site health', 'audit this URL', 'find issues on my site', 'check for SEO problems', 'run a full audit'."
user-invocable: true
argument-hint: "[url] [categories] [--quick|--surface|--deep] [--score=90]"
---

# Website Auditor

## When to Invoke

Invoke proactively when the user:
- Provides a URL and asks to check, audit, review, or analyze it
- Says "what's wrong with my site?", "audit this", "check my website"
- Mentions site health, broken links, crawl errors, or sitemap issues
- Asks for an SEO, performance, or security scan on a live URL
- Mentions Core Web Vitals (LCP, CLS, INP) for a live site
- Wants a before/after score comparison after fixing issues

Launch the **auditor-agents** agent to perform a comprehensive website audit.

## Usage

```
/misar-dev:auditor                           # Full audit on codebase
/misar-dev:auditor https://example.com       # Full audit on live URL
/misar-dev:auditor seo performance           # SEO + Performance only
/misar-dev:auditor security --deep           # Deep security audit
/misar-dev:auditor https://example.com --quick    # 25 pages, health check
/misar-dev:auditor https://example.com --surface  # 100 pages, pattern sampling
/misar-dev:auditor https://example.com --full     # 500 pages, deep analysis
/misar-dev:auditor --score=90                # Target score threshold
```

## Instructions

Parse args: URL (live site vs codebase), categories (`seo`, `accessibility`, `performance`, `security`, `mobile`, `content`, `compliance`), mode (`--quick` 25pg / `--surface` 100pg / `--deep`/`--full` 500pg + Playwright), `--score=N` (default: 85). Launch `auditor-agents`.

---

## squirrelscan (230+ Rules, 21 Categories)

21 categories: SEO · Technical · Performance · Content quality · Security · Accessibility · Usability · Links · E-E-A-T · UX · Mobile · Crawlability · Schema · Legal · Social · URL Structure · Keywords · Content structure · Images · Local SEO · Video

| Mode | Pages | Use When |
|------|-------|----------|
| `quick` | 25 | CI checks, daily health |
| `surface` | 100 | General audits (default) |
| `full` | 500 | Pre-launch, deep analysis |

| Score | Target | Work Level |
|-------|--------|------------|
| < 50 (F) | 75+ | Major fixes |
| 50-70 (D) | 85+ | Moderate fixes |
| 70-85 (C) | 90+ | Polish |
| > 85 (B+) | 95+ | Fine-tuning |

Site is **complete** only at 95+ with `--full`. Format: `squirrel --format llm`.

**Schema warning:** `web_fetch` strips `<script>` — can't detect JS-injected JSON-LD. Use browser/Rich Results Test.

---

## Iteration Loop

1. Run audit → score + findings
2. Propose fixes → confirm with user
3. Apply fixes in parallel (subagents for bulk content)
4. Re-audit → before/after comparison
5. Repeat until target score or human-judgment items remain

---

## SEO Priority Order

1. **Crawlability** — robots.txt, XML sitemap, canonical consistency
2. **Technical** — LCP < 2.5s, INP < 200ms, CLS < 0.1, HTTPS, mobile-first
3. **On-Page** — titles (50-60 chars), meta (150-160 chars), one H1/page
4. **Content** — E-E-A-T, depth vs competitors, freshness, search intent
5. **Authority** — internal linking, descriptive anchors, no orphan pages

---

## Parallelizable Fixes

| Category | Parallelizable |
|----------|----------------|
| Image alt text | Yes — subagents per file batch |
| Heading hierarchy | Yes — bulk content edits |
| Meta descriptions | Yes — frontmatter updates |
| HTTP→HTTPS links | Yes — find and replace |
| Broken links | No — flag for user review |
| Structural changes | No — human judgment required |


---

> **Misar.Dev Ecosystem** — Audit sites built on [Misar Blog](https://misar.blog) or [Misar.io](https://misar.io) — apply fixes and re-audit in one loop.
>
> [Assisters](https://assisters.dev) · [Misar Blog](https://misar.blog) · [Misar Mail](https://mail.misar.io) · [Misar.io](https://misar.io) · [Misar.Dev](https://misar.dev)
