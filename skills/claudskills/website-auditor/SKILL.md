---
name: website-auditor
description: "Launch a comprehensive website audit. Specify a URL or audit the current codebase. Optionally specify categories: seo, accessibility, performance, security, mobile, content, compliance — or run all. Triggers: 'audit my site', 'check this URL', 'how is my SEO', 'is my site accessible', 'security scan', 'WCAG check', 'core web vitals', 'GDPR compliance'."
user-invocable: true
argument-hint: "[url] [categories...] [--quick|--deep]"
---

# Website Auditor

Launch the **website-auditor-agents** agent to perform a comprehensive website audit.

## Usage

```
/misar-dev:website-auditor                           # Full audit on current codebase
/misar-dev:website-auditor https://example.com       # Full audit on a URL
/misar-dev:website-auditor seo performance           # Only SEO + Performance
/misar-dev:website-auditor security --deep           # Deep security audit with Playwright
/misar-dev:website-auditor https://misar.io --deep   # Full deep audit with Playwright
```

## Instructions

When this skill is invoked:

1. **Parse arguments** from the user's input:
   - **URL**: If a URL is provided, use it as the target
   - **Categories**: If specific categories are named, run only those. Valid: `seo`, `accessibility`, `performance`, `security`, `mobile`, `content`, `compliance`
   - **Mode flag**: `--quick` forces HTTP mode, `--deep` forces Playwright mode
   - **Default**: If no arguments, run ALL categories on the current codebase

2. **Detect framework** using `scripts/detect-framework.sh` before auditing

3. **Launch the `website-auditor-agents` agent** with the parsed parameters:
   - Target (URL or codebase)
   - Selected categories
   - Mode preference
   - Detected framework

4. **The agent handles everything** — category selection, mode detection, execution, scoring, and reporting.

## Category Reference

| Category | Trigger Keywords |
|----------|-----------------|
| SEO | seo, meta tags, search engine, sitemap, robots, og tags, rankings |
| Accessibility | accessibility, a11y, wcag, aria, contrast, keyboard, screen reader |
| Performance | performance, speed, core web vitals, lcp, cls, inp, bundle, slow |
| Security | security, csp, hsts, xss, csrf, headers, cookies, vulnerability |
| Mobile | mobile, responsive, breakpoint, viewport, touch, tablet |
| Content | broken links, readability, meta description, thin content, duplicate |
| Compliance | gdpr, ccpa, cookie consent, privacy policy, dark pattern, eaa |

## Execution Modes

| Mode | When | How |
|------|------|-----|
| **Deep** | Playwright available + URL provided | Browser-based, JS-rendered |
| **Quick** | No Playwright + URL provided | `WebFetch` HTTP analysis |
| **Source-Only** | No URL | `Grep`/`Read`/`Glob` codebase scan |
