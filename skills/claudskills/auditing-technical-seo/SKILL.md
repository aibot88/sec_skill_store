---
name: auditing-technical-seo
description: Use when running a technical SEO audit, debugging Core Web Vitals regressions, checking indexability, validating schema and sitemaps, diagnosing why a site isn't ranking, or preparing a site for AI-search visibility (GPTBot, ClaudeBot, PerplexityBot). Covers crawlability, indexability, rendering, Core Web Vitals, schema, AI-search readiness, mobile, security, and meta basics. Lifecycle-aware — pre-launch, growth, mature. Produces a prioritized SEO_AUDIT.md and a low-risk fix PR.
---

# Auditing Technical SEO

## Overview

Technical SEO is the foundation. Content strategy, keyword work, and link building all assume that Google, Bing, and AI-search crawlers can actually fetch, render, and trust your pages. If any of those fail, nothing else compounds. In 2026 that surface is wider than it used to be: Core Web Vitals are still the user-experience signal Google measures at the **75th percentile** with thresholds **LCP < 2.5s, INP < 200ms, CLS < 0.1** [1], and a new tier of AI crawlers — GPTBot, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended, Applebot-Extended — now decides whether your content shows up in ChatGPT, Claude, and Perplexity answers [2][3].

## What this skill checks

- **Crawlability:** `robots.txt` parses cleanly, no accidental site-wide `Disallow: /`, sitemap referenced as absolute URL, sitemap reachable and valid, file under 500 KiB (Google's hard cap) [6][7].
- **Indexability:** GSC index coverage cross-referenced via `gsc-mcp`, canonical tags consistent and self-referential where appropriate, hreflang correct on i18n sites, no duplicate content via tracking parameters, no `noindex` on pages that should rank [5].
- **Rendering:** SSR/SSG vs CSR-only routes (CSR-only pages are largely invisible to GPTBot/ClaudeBot/PerplexityBot, which do not execute JS reliably), critical content not hidden behind hydration [2][3].
- **Core Web Vitals:** LCP, INP, CLS, TTFB measured at p75 via `lighthouse-mcp` (PageSpeed Insights / CrUX field data) [1].
- **Schema:** JSON-LD present in `<head>` or root layout, types valid against schema.org (Article, BlogPosting, Organization, FAQPage, BreadcrumbList, Product as appropriate), validates via `validator.schema.org` [4].
- **AI-search readiness:** `robots.txt` makes a deliberate choice on GPTBot, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended (allow or block — both are valid; absence is the bug) [2][3]. `llms.txt` presence noted but not required: adoption is ~10% of domains and effect on AI citations is unproven [8].
- **Mobile:** viewport meta present, mobile-friendly via PSI mobile run.
- **Security:** HTTPS only, HSTS header, no mixed content, valid certificate.
- **Meta basics:** unique `<title>` (50–60 chars) and `meta description` (150–160 chars) per page; Lighthouse SEO category flags these explicitly [5].

## The audit flow

**1. Gather.** Read repo files: `package.json` (framework detection), `app/robots.ts` or `public/robots.txt`, `app/sitemap.ts` or `public/sitemap.xml`, `app/layout.tsx` (or Astro `Layout.astro` / SvelteKit `+layout.svelte`) for `<head>` schema, `next.config.js` / `astro.config.mjs` / `svelte.config.js` for redirect/rewrite rules. Then fetch the live site's `/robots.txt`, `/sitemap.xml`, `/llms.txt`. Call `lighthouse-mcp` for PSI on the homepage and 2–3 representative inner pages (mobile + desktop). Call `gsc-mcp` if connected for index coverage and submitted-sitemap status.

**2. Cross-reference.** Does the deployed sitemap match what GSC has on file? Are CSR-only routes leaking into the sitemap? Does `robots.txt` block any URL that's also in the sitemap (the classic conflict) [7]? Are GSC-reported "Discovered – currently not indexed" URLs concentrated in one route group?

**3. Write `SEO_AUDIT.md`** to repo root. Findings ranked by **traffic-impact × fix-effort** in a quadrant — high-impact / low-effort first.

**4. Open ONE PR** with the highest-confidence, low-risk fixes only: adding viewport meta, adding missing meta descriptions, adding `Sitemap:` line to `robots.txt`, adding explicit GPTBot/ClaudeBot allow-or-block stanza, adding root `Organization` JSON-LD. Leave architectural calls (CSR → SSR migration, image pipeline rework) for human decision in the audit doc.

## Output format — `SEO_AUDIT.md` shape

```
# SEO Audit — example.com — 2026-04-26

## Quadrant
                 LOW EFFORT          HIGH EFFORT
HIGH IMPACT  | Add meta descriptions | Migrate /blog to SSR
LOW IMPACT   | Tidy llms.txt         | Refactor schema graph

## Findings

### [P0] Sitemap not referenced in robots.txt
Severity: high · Effort: 5 min · Confidence: 100%
Fix: Add `Sitemap: https://example.com/sitemap.xml` to `app/robots.ts`.

### [P0] LCP 4.1s on /pricing (p75 mobile)
Severity: high · Effort: medium · Confidence: 90%
Cause: hero image not preloaded, no priority hint.
Fix: <Image priority fetchPriority="high" /> on hero.

### [P1] No GPTBot/ClaudeBot stanza in robots.txt
Severity: medium · Effort: 2 min · Confidence: 100%
Decision required: allow or block? Both are valid choices.
```

## Lifecycle awareness

Mirroring the lifecycle pattern in `finding-underserved-keywords`:

- **Initial (pre-launch / first 3 months):** focus on indexability, schema, sitemap correctness, canonical hygiene, robots.txt sanity. Core Web Vitals data isn't statistically meaningful yet — CrUX needs traffic.
- **Growth (3–12 months):** add CWV regressions and mobile-friendliness; cross-reference GSC index coverage to catch routes silently dropping out.
- **Mature (12+ months):** decay defense — schema drift (types deprecated upstream at schema.org), CWV regressions from third-party script creep, sitemap bloat from old URLs, AI-crawler policy review as new bots emerge.

## Common mistakes

- Running the audit before the site is deployed — most checks need a live URL.
- Conflating crawlability with rankings — fixing robots.txt won't lift a thin-content page.
- Skipping mobile — Google indexes mobile-first; desktop-only Lighthouse misses real failures.
- Blocking AI-search bots without realizing — broad `Disallow: /` against `User-agent: *` blocks ClaudeBot too [3].
- Treating Lighthouse SEO score as the audit — it's 8 pass/fail checks, not a strategy [5].

## Common false positives

- Lighthouse flagging "image elements do not have explicit width and height" on the LCP image when it's *intentionally* the hero — that's correct architecture, not a bug.
- Schema.org validator "warnings" that are recommendations, not errors — distinguish before opening a PR.
- PSI showing CWV "needs improvement" on a brand-new page — CrUX field data is sparse; lab data only at this stage.
- `llms.txt` missing — flag as suggestion only; no measurable AI-citation effect yet [8].

Citations and verification tags in [SOURCES.md](SOURCES.md).
