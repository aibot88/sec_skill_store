---
name: web-scraper-seo
description: Scrape, download, and analyze websites for mockup generation, design system extraction, accessibility auditing, and web development brainstorming. Use this skill whenever the user wants to clone a website's look and feel, reverse-engineer a page's design, capture a site's CSS/JS/HTML structure, extract design tokens (colors, typography, spacing scales), analyze SEO techniques, run a WCAG accessibility audit, crawl multi-level navigation menus, scrape JavaScript-rendered SPAs (React, Next.js, Vue, Angular), download site assets for offline viewing, generate a navigable local mirror of a website for reference, detect broken links, record redirect chains, or brainstorm web development ideas based on existing sites. Produces a local copy with rewritten internal links for full page-to-page navigation, faithful inline CSS reproduction, comprehensive design system extraction, keyword density analysis, WCAG 2.1 accessibility scoring, automatic cookie/consent banner dismissal, and structured design tokens in CSS/JSON/Tailwind formats. Also triggers when the user mentions scraping URLs, downloading websites, site cloning, design inspiration from live sites, SEO auditing, accessibility checking, WCAG compliance, design token extraction, or wants to serve scraped content locally. Accepts a single URL or a list of URLs with optional depth control for multi-level crawling. Make sure to use this skill whenever the user mentions website cloning, site scraping, design system extraction, SEO analysis, accessibility audit, broken link detection, or design token generation — even if they don't explicitly say "scrape".
---

# Web Scraper & SEO Analyzer

Scrapes websites, downloads their assets (HTML, CSS, JS, images, fonts), rewrites all paths for local serving (including internal page links and inline styles), extracts SEO metadata and design system patterns, detects broken links, records redirect chains, performs keyword density analysis, and produces a fully navigable local mirror. Scraped content can be served via a built-in HTTP server and verified with Playwright screenshots. Design tokens can be extracted in CSS custom properties, W3C JSON, or Tailwind config format.

## When This Skill Fires

- User provides a URL (or list of URLs) and wants to capture, clone, or analyze the site
- User wants design inspiration or design tokens from a live website
- User asks to reverse-engineer a page's structure or design system
- User wants to audit SEO techniques on one or more pages
- User wants a local copy of a site for offline reference or mockup generation
- User wants to scrape a JavaScript-rendered SPA (React, Next.js, Vue, Angular)
- User wants to detect broken links or analyze redirect chains
- User wants to extract design tokens (colors, spacing, typography) from a site
- User wants an accessibility audit or WCAG compliance check on a website

## Parameters

The user provides:

1. **url** (required): A single URL string or a list of URLs to scrape
2. **depth** (optional, default: 0): How many levels of child/navigation links to follow
   - `0` = single page only
   - `1` = the page + all direct child links found in navigation menus
   - `2` = children + grandchildren
   - `3+` = deeper crawls (warn the user this can be large)
3. **render-js** (optional, default: off): Use Playwright to render JS before scraping — captures SPA/React/Vue content invisible to HTTP-only scraping. Also enables shadow DOM flattening and same-domain iframe extraction
4. **sitemap** (optional, default: off): Fetch sitemap.xml to discover pages not linked from navigation
5. **resume** (optional, default: off): Resume an interrupted crawl from the last checkpoint
6. **proxy** (optional): Route all requests through an HTTP/HTTPS/SOCKS5 proxy (e.g., `socks5://proxy:1080`)
7. **cookies** (optional): Inject auth cookies — inline `key=value;key=value` pairs or a path to a JSON file `{"name": "value"}`
8. **headers** (optional): Inject custom HTTP headers — `Key:Value;Key:Value` format (e.g., `Authorization:Bearer token123`)
9. **basic-auth** (optional): HTTP Basic Auth as `user:password`

## Which Script to Use

| Goal | Script | Key flags |
|------|--------|-----------|
| Scrape a website (HTML + assets) | `scripts/scrape_site.py` | `--urls`, `--depth`, `--output` |
| Scrape JS-heavy / SPA site | `scripts/scrape_site.py` | `--urls`, `--depth`, `--output`, `--render-js` |
| Include sitemap pages | `scripts/scrape_site.py` | `--urls`, `--output`, `--sitemap` |
| Resume interrupted crawl | `scripts/scrape_site.py` | `--urls`, `--output`, `--resume` |
| Scrape via proxy | `scripts/scrape_site.py` | `--urls`, `--output`, `--proxy` |
| Scrape authenticated site | `scripts/scrape_site.py` | `--urls`, `--output`, `--cookies` or `--headers` or `--basic-auth` |
| Extract design tokens | `scripts/extract_tokens.py` | `--input`, `--format` |
| Run accessibility audit | `scripts/a11y_analyzer.py` | `--input`, `--format` |
| Serve scraped content locally | `scripts/serve_site.py` | `--directory`, `--port` |
| Take a screenshot | `scripts/playwright_view.py screenshot` | `--url`, `--output`, `--viewport` |
| Test responsive layouts | `scripts/playwright_view.py responsive` | `--url`, `--output-dir` |
| Run deeper SEO scoring | `scripts/seo_analyzer.py` | `--input`, `--format` |
| Get rendered HTML from SPA | `scripts/playwright_view.py render` | `--url`, `--output` |

## Error Handling

The scraper handles common issues gracefully — know these before running:
- **403/401 responses**: Logged, page skipped, crawl continues
- **Timeout**: 30-second timeout per request, retries once, then skips
- **SSL errors**: Falls back to `verify=False`, warns user
- **Binary files**: Detected and downloaded without HTML parsing
- **Relative URLs**: All resolved against the page's base URL
- **JavaScript-rendered content**: Use `--render-js` to render pages with Playwright before processing. Falls back to HTTP-only if Playwright is not installed.
- **Interrupted crawls**: Use `--resume` to continue from where you left off. Checkpoint saved after every page.
- **Broken links**: Automatically detected and reported in `broken-links.json` with source pages and anchor text
- **Redirect chains**: Automatically recorded in `redirect-chains.json` with hop count and status codes
- **Cookie/consent overlays**: In `--render-js` mode, common consent banners (OneTrust, CookieBot, Osano, Quantcast, generic GDPR) are automatically dismissed before content extraction. Also applies to Playwright screenshots.
- **Proxy routing**: Use `--proxy` to route through HTTP/HTTPS/SOCKS5 proxies. Applied to both HTTP requests and Playwright browser.
- **Authentication**: Use `--cookies`, `--headers`, or `--basic-auth` to access login-protected pages. Tokens/cookies must be obtained externally.
- **iframe content**: Same-domain `<iframe>` sources are fetched and saved to `pages/_iframes/`. Cross-origin iframes are skipped.
- **Shadow DOM**: In `--render-js` mode, shadow DOM content is flattened into the page HTML before extraction (best-effort).

## Workflow Steps

### Post-Scrape Checklist (Do This After Every Scrape)

After running `scrape_site.py` (Step 2), complete ALL of these before moving on — these follow-up offers are a core part of the skill's value, not optional extras:

1. **Present the results** — Summarize pages scraped, assets downloaded, SEO highlights, broken links found, and redirect chains recorded
2. **Offer design token extraction** — Ask: "I can also extract the design system (colors, fonts, spacing) into CSS custom properties, W3C JSON, or Tailwind config. Want me to run that?" Then run `extract_tokens.py` if they say yes (or if they originally asked about design/styling)
3. **Offer accessibility audit** — Ask: "I can run a WCAG 2.1 accessibility audit on the scraped pages. Want me to check that?"
4. **Offer local server** — Ask: "Would you like me to start a local HTTP server so you can browse the scraped site in your browser?"

Even if the user didn't explicitly ask for tokens, audit, or server — offer them. Users often don't know these capabilities exist until prompted. If the user's original request already implies one of these (e.g., "clone the look and feel" implies design tokens), run it proactively without asking.

### Step 1: Install Dependencies

```bash
cd /path/to/this/skill
pip install requests beautifulsoup4 lxml cssutils --break-system-packages -q
pip install playwright --break-system-packages -q
playwright install chromium 2>/dev/null || true
```

If `playwright install` fails (common in sandboxed environments), that's fine — scraping still works without JS rendering. The Playwright viewing step and `--render-js` become unavailable.

### Step 2: Run the Scraper

```bash
python scripts/scrape_site.py \
  --urls "https://example.com" \
  --depth 1 \
  --output /home/claude/scraped-sites/example.com
```

For JS-heavy SPAs (React, Next.js, Vue, Angular):
```bash
python scripts/scrape_site.py \
  --urls "https://spa-site.com" \
  --depth 1 --render-js \
  --output /home/claude/scraped-sites/spa-site
```

With sitemap discovery for content-heavy sites (blogs, docs, e-commerce):
```bash
python scripts/scrape_site.py \
  --urls "https://docs-site.com" \
  --depth 0 --sitemap \
  --output /home/claude/scraped-sites/docs-site
```

Resume an interrupted crawl:
```bash
python scripts/scrape_site.py \
  --urls "https://example.com" \
  --depth 2 --resume \
  --output /home/claude/scraped-sites/example.com
```

Through a proxy:
```bash
python scripts/scrape_site.py \
  --urls "https://example.com" \
  --depth 1 --proxy "socks5://proxy:1080" \
  --output /home/claude/scraped-sites/example.com
```

Authenticated site (cookies + headers):
```bash
python scripts/scrape_site.py \
  --urls "https://dashboard.example.com" \
  --depth 1 \
  --cookies "session_id=abc123;csrf_token=xyz" \
  --headers "Authorization:Bearer eyJhbGci..." \
  --output /home/claude/scraped-sites/dashboard
```

The script handles:
- **Breadth-first crawling** with a visited-set to avoid cycles
- **Depth limiting** via the `--depth` flag
- **Navigation-scoped link discovery** — only follows links inside `<nav>`, `<header>`, or elements with menu/nav roles
- **Sitemap discovery** (`--sitemap`) — fetches sitemap.xml/sitemap_index.xml to find pages not in navigation
- **JS rendering** (`--render-js`) — uses Playwright to get the fully rendered DOM for SPAs before processing with the standard pipeline
- **Asset downloading** — CSS, JS, images, fonts from HTML and CSS `@import`/`url()` references
- **Internal link rewriting** — after all pages are scraped, a second pass rewrites `<a href>` links between pages to relative local paths, making multi-page sites fully navigable when served locally
- **Inline style processing** — `url()` references in `<style>` tags and `style=""` attributes are rewritten to local asset paths; design patterns (colors, fonts, layout) from inline styles are included in the analysis
- **Keyword density analysis** — top 20 keywords with density percentages, stop word filtering, and prominence detection (keywords appearing in title/H1)
- **Redirect chain recording** — captures the full redirect path (each hop's URL and status code) whenever HTTP redirects are followed
- **Checkpoint/resume** (`--resume`) — saves state after every page so interrupted crawls can continue from the last checkpoint
- **Broken link detection** — automatically tracks which pages link to which URLs and generates `broken-links.json` with source pages, anchor text, and error details
- **Proxy routing** (`--proxy`) — routes all HTTP requests and Playwright browser through an HTTP/HTTPS/SOCKS5 proxy
- **Authentication** (`--cookies`, `--headers`, `--basic-auth`) — injects session cookies, custom headers, or HTTP Basic Auth into both requests and Playwright contexts
- **iframe extraction** — same-domain `<iframe>` content is fetched, saved to `pages/_iframes/`, and the parent page's src rewritten to point locally
- **Shadow DOM flattening** (`--render-js` only) — serializes shadow root content into `<template shadowrootmode>` elements so downstream parsers can see web component content
- **robots.txt** respect, **rate limiting** (1 req/sec default), and honest **User-Agent** identification

### Step 3: Understand the Output Structure

```
scraped-sites/example.com/
├── site-report.json          # Master manifest + SEO + design analysis
├── broken-links.json         # Broken link report with source pages + anchor text
├── redirect-chains.json      # Redirect chain data (hops, status codes)
├── pages/
│   ├── index.html            # Rewritten HTML (local asset + page link paths)
│   ├── about.html
│   └── products/
│       └── index.html
├── assets/
│   ├── css/                  # Downloaded stylesheets (url() paths rewritten)
│   ├── js/                   # Downloaded scripts
│   ├── images/               # Downloaded images, favicons, icons
│   └── fonts/                # Downloaded web fonts
├── seo/
│   ├── seo-summary.json      # Aggregated SEO findings
│   └── per-page/
│       ├── index.json        # Per-page SEO data (including keyword density)
│       └── about.json
├── a11y/                     # Generated by a11y_analyzer.py (Step 5b)
│   ├── a11y-summary.json     # Aggregated accessibility findings
│   ├── a11y-analysis.json    # Full analysis with per-page scores
│   └── per-page/
│       ├── index.json        # Per-page WCAG checks
│       └── about.json
└── design-tokens/            # Generated by extract_tokens.py (Step 5a)
    ├── tokens-raw.json       # Raw extracted values
    ├── tokens-w3c.json       # W3C Design Tokens format
    ├── tokens.css            # CSS custom properties
    └── tailwind.config.js    # Tailwind theme config
```

### Step 4: Review the Site Report

`site-report.json` is the master document. It contains: scrape metadata (including JS rendering mode, sitemap discovery, broken link count, redirect chain count), a hierarchical sitemap tree, asset inventory by type, SEO highlights and issues, and design system extraction (colors, fonts, layout approach, responsive detection, framework detection).

See `references/site-report-schema.md` for the full schema with field descriptions and example JSON.

### Step 5: Review SEO Data

`seo/seo-summary.json` aggregates findings across all pages. Per-page files in `seo/per-page/` contain granular data covering: title tags, meta descriptions, heading hierarchy, URL structure, canonical URLs, Open Graph/Twitter Card tags, hreflang, robots directives, JSON-LD structured data, internal/external link analysis, image alt text audit, keyword density (top 20 keywords with density percentages and prominence in title/H1), and technical signals (viewport, charset, script loading, resource hints).

For the full element-by-element reference, see `references/seo-checklist.md`.

For deeper analysis with per-page scoring (0-100, graded A-F), run:
```bash
python scripts/seo_analyzer.py --input /path/to/scraped-site --format json
```

### Step 5a: Extract Design Tokens (Per Post-Scrape Checklist)

Run proactively if the user asked about design, styling, or cloning — otherwise offer per the checklist above:

```bash
# All formats (CSS + JSON + Tailwind)
python scripts/extract_tokens.py --input /path/to/scraped-site --format all

# CSS custom properties only
python scripts/extract_tokens.py --input /path/to/scraped-site --format css

# W3C JSON design tokens only
python scripts/extract_tokens.py --input /path/to/scraped-site --format json

# Tailwind config only
python scripts/extract_tokens.py --input /path/to/scraped-site --format tailwind
```

The extractor analyzes all CSS sources (external stylesheets, inline `<style>` blocks, and `style=""` attributes on elements) and produces:
- **Color classification** — primary, neutral, and accent colors grouped by saturation/usage
- **Typography scale** — font families, font sizes sorted into a scale
- **Spacing scale detection** — identifies base-4, base-8, or custom spacing systems
- **Border radius scale** — extracted and sorted
- **Shadow tokens** — box-shadow values cataloged
- **Breakpoint detection** — media query breakpoints extracted
- **CSS custom properties** — ready-to-use `:root { --color-primary: ... }` file
- **W3C Design Tokens** — structured JSON following the draft W3C spec
- **Tailwind config** — `theme.extend` snippet for `tailwind.config.js`

### Step 5b: Run Accessibility Audit (Per Post-Scrape Checklist)

Run proactively if the user asked about accessibility — otherwise offer per the checklist above:

```bash
python scripts/a11y_analyzer.py --input /path/to/scraped-site --format json
```

The analyzer checks each page against 10 WCAG criteria and produces a 0-100 score (graded A-F):
- **Language** (3.1.1) — `<html lang="...">` present and valid
- **Document title** (2.4.2) — descriptive `<title>` tag
- **Heading hierarchy** (1.3.1) — sequential levels, single H1
- **Image alt text** (1.1.1) — missing alt, empty alt in links, suspicious placeholder alt
- **Form labels** (1.3.1, 4.1.2) — explicit `<label>`, `aria-label`, or wrapping `<label>`
- **Link purpose** (2.4.4) — no empty links, no generic "click here" text
- **ARIA validity** (4.1.2) — valid roles, required attributes, no hidden focusables
- **Focus indicators** (2.4.7) — detects `outline: none` without replacement
- **Skip navigation** (2.4.1) — skip-to-content link present
- **Landmark regions** (1.3.6) — `<main>`, `<nav>`, `<header>` presence
- **Table headers** (1.3.1) — `<th>`, `scope`, and `<caption>` on data tables
- **Color contrast** (1.4.3) — heuristic detection of low-contrast inline styles

Output is saved to `a11y/a11y-analysis.json` and `a11y/a11y-summary.json`, with per-page detail in `a11y/per-page/`.

### Step 6: Offer Local Server (Per Post-Scrape Checklist)

Per the checklist above, offer the local server. If the user accepts:
```bash
python scripts/serve_site.py \
  --directory /home/claude/scraped-sites/example.com \
  --port 8080
```

The server maps `/` to `pages/index.html`, resolves page paths with `.html` extension fallback, serves `/assets/*` directly, and adds CORS headers.

### Step 7: View with Playwright (Optional)

**Use when:** You need visual verification that the scrape is faithful, responsive screenshots for mockup reference, or the user wants to see the site before working with it. **Skip when:** The user only needs raw HTML/CSS/JSON data, or Playwright isn't installed.

```bash
# Single screenshot
python scripts/playwright_view.py screenshot \
  --url "http://localhost:8080" \
  --output screenshot.png --viewport 1280x800

# Responsive screenshots (desktop + tablet + mobile)
python scripts/playwright_view.py responsive \
  --url "http://localhost:8080" --output-dir /path/to/screenshots
```

### Step 8: Deep Analysis with web-analyzer (Optional)

For multi-site comparison, detailed design briefs, or when the scraped CSS data is too verbose for the main conversation, delegate to the **web-analyzer** companion subagent. It reads the scraped output directory and returns a structured summary — keeping the main conversation context lean.

The web-analyzer handles:
- **Design system deep-dive** — component patterns, motion/animation, layout grid analysis
- **Site comparison** — side-by-side analysis of 2+ scraped sites
- **Design brief generation** — actionable specifications for recreating or remixing the design
- **SEO recommendations** — prioritized improvements with concrete examples

## Post-Scrape: Using Results

With the scraped data in hand, Claude can:

1. **Recreate the page** — Read `site-report.json` for structure, reference downloaded HTML/CSS for implementation details
2. **Remix the design** — Use `design-tokens/tokens.css` or `tailwind.config.js` as a foundation for new projects
3. **Apply SEO best practices** — Use `seo-summary.json` as a checklist for new pages, fix issues found in `broken-links.json`
3a. **Fix accessibility issues** — Use `a11y/a11y-analysis.json` to identify and prioritize WCAG violations
4. **Brainstorm variations** — Compare multiple scraped sites side-by-side to identify patterns and differentiation opportunities
5. **Fix redirect chains** — Review `redirect-chains.json` to identify SEO-impacting redirect hops
6. **Target keywords** — Use keyword density data to understand content strategy and replicate it

Prioritize the design system (colors, fonts, spacing) over pixel-perfect reproduction.

## Important Notes

- This skill is for learning, brainstorming, and development reference. Always respect website terms of service and copyright.
- The scraper identifies itself honestly via User-Agent and respects robots.txt.
- Large sites with deep crawls can produce substantial downloads. The skill warns when depth > 2.
- Rate limiting (1 req/sec default) prevents overwhelming target servers.
- Downloaded content is for local development reference only.

## Reference Files

- `scripts/scrape_site.py` — Main scraping engine (crawl, download, rewrite links, JS rendering, sitemap, broken links, redirects, keyword density, cookie dismissal)
- `scripts/extract_tokens.py` — Design token extractor (CSS custom properties, W3C JSON, Tailwind config)
- `scripts/a11y_analyzer.py` — Accessibility audit (WCAG 2.1 AA, 12 checks, 0-100 scoring)
- `scripts/serve_site.py` — Local HTTP server for viewing scraped content
- `scripts/playwright_view.py` — Playwright integration for screenshots, responsive testing, JS rendering, cookie dismissal
- `scripts/seo_analyzer.py` — Standalone deep SEO analysis with scoring
- `agents/web-analyzer.md` — Companion subagent for deep design analysis and site comparison
- `references/seo-checklist.md` — Comprehensive SEO elements reference
- `references/site-report-schema.md` — Full site-report.json schema with field descriptions
