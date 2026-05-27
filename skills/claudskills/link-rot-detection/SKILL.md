---
# yaml-language-server: $schema=https://skillgraph.dev/schemas/skill.v4.schema.json
schema_version: 4
name: link-rot-detection
description: "Use when authoring or reviewing a periodic-scan job that walks every external link in a markdown content set and flags 404s, redirects to unrelated content, and connection failures. Activate this skill whenever the task says 'check our links' or mentions a link-rot scan, broken-link audit, or link-health report. Do NOT use for live runtime link checking inside the rendered page (use a frontend a11y / UX skill) or for chasing a specific broken-link incident from a user report (use debugging)."
version: 0.1.0
type: capability
category: content
domain: content/maintenance
scope: portable
owner: markdown-static-site-maintainer
freshness: "2026-05-06"
drift_check:
  last_verified: "2026-05-06"
eval_artifacts: none
eval_state: unverified
routing_eval: absent
stability: experimental
license: MIT
compatibility:
  runtimes:
    - node
  node: ">=20"
  notes: "Portable across any markdown-content project; no codebase grounding required."
allowed-tools: Read Grep Bash
keywords:
  - link rot
  - link-rot detection
  - broken link audit
  - link health
  - dead link scan
  - 404 audit
  - external link check
  - periodic scan
  - markdown link extraction
  - link-rot report
triggers:
  - link-rot-detection
examples:
  - "design a periodic link-rot scan that runs nightly and posts a report"
  - "review the link-rot detector — does it handle redirects correctly?"
  - "explain how to test the link-rot scanner against a fixture set without hitting the network"
  - "should the scan retry on transient 5xx, or only flag persistent failures?"
anti_examples:
  - "validate this internal route in the live app"
  - "the link to example.com just broke for one user"
  - "design the rendering of broken-link badges in the UI"
relations:
  boundary:
    - skill: documentation
      reason: "documentation writes prose about link-health policy; this skill enforces the detection primitive in code"
    - skill: debugging
      reason: "debugging chases a specific reported broken link; this skill is the periodic audit applied before user reports"
    - skill: refactor
      reason: "refactor changes scanner code shape; this skill enforces the detection contract that any refactor must preserve"
  verify_with:
    - testing-strategy
portability:
  readiness: scripted
  targets:
    - skill-md
workspace_tags:
  - content
  - markdown
lifecycle:
  stale_after_days: 180
  review_cadence: quarterly
---

# Link-Rot Detection

## Coverage

- Markdown link extraction — pulling every `[text](url)` and `[text][ref]` reference link out of every `.md` and `.mdx` file in the content tree
- External vs internal classification — what counts as external (different host) and what gets skipped (relative path, anchor link, mailto, tel)
- Status-code interpretation — 200 is healthy, 301/308 is a redirect (record the new URL but don't fail), 302/307 is transient (re-check next run), 404/410 is dead (flag), 5xx is transient (retry with backoff before flagging)
- Soft-404 detection — pages that return HTTP 200 but render an "unknown page" interstitial (compare body length / content against known soft-404 patterns)
- Rate-limiting and politeness — concurrent request budget per origin host, honoring `robots.txt` crawl-delay, exponential backoff on 429
- Reporting shape — the scanner's output is a structured report (JSON + markdown summary), not a live alert; the report is the audit artifact

## Philosophy

External links rot. Every site that's older than two years has at least a few. The choice is between knowing about them on a schedule or finding out from a user. A periodic scan with a published report turns link health into a maintenance task instead of an emergency. The discipline is to be conservative — distinguish persistent failures (404 across 3 runs) from transient ones (one 503 on a Tuesday) — and to never let the scanner itself become a denial-of-service vector against the targets it's checking.

## Verification

Before merging any change to the link-rot scanner or its config:

- [ ] The scanner extracts every link in `[text](url)` and `[text][ref]` form from `.md` and `.mdx` files; reference links resolve their targets before classification
- [ ] Internal links (relative paths, same-host absolute, anchors, mailto, tel) are explicitly excluded — confirmed by a fixture test with mixed link types
- [ ] Persistent failures are distinguished from transient ones — a link is only flagged after N consecutive failures across separate runs (default N=3)
- [ ] The scanner respects per-host concurrency limits and honors `robots.txt` crawl-delay; a single host getting many requests in tight sequence is a bug
- [ ] Soft-404 detection has a defined pattern set and an explicit "unknown" bucket for cases that don't match any known soft-404
- [ ] The scanner produces both a JSON report (machine-readable) and a markdown summary (human-readable) with link, status code, last-seen-OK timestamp, and recommendation

## Do NOT Use When

| Use instead | When |
|---|---|
| (a frontend a11y / UX skill) | The task is rendering a "this link may be broken" badge in the live UI |
| `debugging` | A specific link broke for a specific user and you need to reproduce |
| `documentation` | The task is writing the link-health policy doc, not the scanner |
| `refactor` | The task is restructuring the scanner without changing the detection contract |
