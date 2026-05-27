---
name: etsy-shop-doctor
description: End-to-end Etsy shop health audit covering policy compliance, conversion killers, SEO drift, shop-level signals (response time, on-time shipping, reviews), and the 2026 algorithm risk factors. Use when the user wants to audit shop health, prep for launch, troubleshoot declining sales, or run a periodic shop checkup. Outputs prioritized fix list with severity ratings.
---

# Etsy Shop Doctor

You run a comprehensive Etsy shop health audit covering everything that affects discoverability, conversion, and shop standing. Most shops audit individual listings; this skill audits the shop as a system. Run before launch, then monthly.

## When to invoke

- User says "shop health check" / "audit my Etsy shop" / "etsy shop doctor"
- User mentions declining sales or wants a launch readiness check
- Monthly recurring audit
- Before any major shop change (new product line, pricing overhaul, branding update)

## Audit dimensions (in order of weight)

### 1. Compliance (40% weight — failure here = shop suspension risk)

- **AI Disclosure tags** — call `etsy-ai-disclosure-auditor`, summarize gap count
- **Intellectual property** — flag listings that may infringe (WotC IP, Disney, GW): check for "D&D," "Star Wars," "Pokemon," "Marvel," etc. in titles/tags without explicit licensing claim
- **Production partners** — every POD listing must have a registered production partner
- **Prohibited items** — check for items in restricted categories (handmade-only categories with claimed handmade status)
- **Tax setup** — verify shop has tax address + tax ID registered (operator step, just check status)
- **Bank account** — verify connected (operator step, just check status)

### 2. Shop signals (30% weight — direct ranking factor)

- **Response time** — Etsy displays this publicly; target <24h, ideal <4h. Check last 30 days.
- **On-time shipping rate** — Etsy expectation ≥95%. Check last 90 days.
- **Order defect rate** — cancellations, refunds, disputes. Target <1%.
- **Star Seller status** — Etsy's badge for 5★ avg + <24h response + 95%+ on-time + dispute-free. Check current status.
- **Review average** — should be ≥4.8 for premium-positioned shops
- **Reviews per 100 orders** — target ≥20% review rate (most shops get 10-15% organic, 25%+ with review requests)

### 3. Listing portfolio health (15% weight)

- **Listing count** — Etsy's 2026 algorithm rewards 20-50 high-quality listings over 200 mass-listings
- **Stale listing percentage** — listings >90 days with zero views = drag on shop quality score. Recommend renew or deactivate.
- **Photo completeness** — % of listings with <5 photos
- **Variant completeness** — % of listings with variants used (color, size, format)
- **Section organization** — % assigned to a section vs "Default Section"

### 4. SEO + discoverability (10% weight)

- **Title front-loading** — % of titles with primary keyword in first 60 chars
- **Tag slot usage** — average tags per listing (target 13/13)
- **Description length** — % of listings ≥160 chars
- **Cross-shop SEO consistency** — same keyword "dnd notebook" should appear in shop title, about page, multiple listings

### 5. Conversion killers (5% weight)

- **Shop policies completeness** — shipping, returns, gift wrap, custom orders
- **About page word count** — target ≥300 words with brand story
- **Shop announcement** — present, ≤100 chars, contains a hook (not "welcome to my shop")
- **Featured listings** — top 4 spots on shop home page (these get 5× the traffic of other listings)
- **Mobile preview** — verify shop displays cleanly on mobile (most Etsy buyers are mobile)
- **Currency + language settings** — match target market

## Required environment

- All previous skills' env vars
- Token scope: `shops_r`, `listings_r`, `transactions_r`

## Output format

```
=== ETSY SHOP HEALTH AUDIT — 2026-05-18 ===

Shop: NoteKeepr (shop_id 12345678)
Status: ACTIVE
Audit baseline: 2026-04-18 (last audit)

OVERALL HEALTH SCORE: 73/100  ⚠ NEEDS ATTENTION

┌─ COMPLIANCE (28/40) — 1 critical issue ────────────────────┐
│ ✓ Tax setup: registered                                    │
│ ✓ Bank: connected                                          │
│ ⚠ AI Disclosure: 7 listings missing tag (see audit log)   │
│ ✗ IP risk: 2 listings use "Dungeons & Dragons" in title    │
│   without WotC fan-content disclaimer                      │
│   → Refactor titles per WotC Fan Content Policy            │
│ ✓ Production partners: 1 registered (Printify)             │
│                                                            │
│ Priority: HIGH — fix IP issues this week                   │
└────────────────────────────────────────────────────────────┘

┌─ SHOP SIGNALS (22/30) ─────────────────────────────────────┐
│ ⚠ Response time: 18h avg (target <4h, ideal <2h)           │
│ ✓ On-time shipping: 100% (3 orders, small sample)          │
│ ✓ Order defect rate: 0%                                    │
│ ⚠ Star Seller: NOT QUALIFIED (need 5+ orders for badge)    │
│ ✓ Review avg: 5.0★ (3 reviews — small sample)              │
│ ⚠ Review rate: 75% (3/4 orders reviewed — strong)          │
│                                                            │
│ Priority: MEDIUM — improve response time via mobile app    │
└────────────────────────────────────────────────────────────┘

┌─ LISTING PORTFOLIO (12/15) ────────────────────────────────┐
│ ✓ Listing count: 21 (in healthy 20-50 range)               │
│ ⚠ Stale listings: 3 with zero views in 60 days             │
│ ⚠ Photo completeness: 19/21 have ≥5 photos                 │
│ ✓ Variant completeness: 8/8 physical SKUs have variants    │
│ ✓ Section organization: 19/21 in named sections            │
│                                                            │
│ Priority: LOW — renew or deactivate 3 stale listings       │
└────────────────────────────────────────────────────────────┘

┌─ SEO + DISCOVERABILITY (8/10) ─────────────────────────────┐
│ ✓ Title front-loading: 18/21                               │
│ ⚠ Tag slot usage: avg 11/13 (3 listings under-using)       │
│ ✓ Description length: 21/21 ≥160 chars                     │
│ ⚠ Cross-shop consistency: "lorekeeper" missing from shop   │
│   announcement and about page                              │
│                                                            │
│ Priority: LOW — quick wins on tags + announcement          │
└────────────────────────────────────────────────────────────┘

┌─ CONVERSION KILLERS (3/5) ─────────────────────────────────┐
│ ✓ Shop policies: all set                                   │
│ ⚠ About page: 142 words (target ≥300)                      │
│ ⚠ Shop announcement: generic "Welcome to NoteKeepr"        │
│ ✗ Featured listings: 0 of 4 slots used                     │
│ ✓ Mobile preview: clean                                    │
│                                                            │
│ Priority: HIGH — featured listings = 5× traffic on hero    │
│ SKUs. Free fix.                                            │
└────────────────────────────────────────────────────────────┘

=== TOP 7 ACTIONS (ranked by impact / effort) ===

1. [10 min, HIGH] Add 4 featured listings to shop home
   → Pick hero SKUs (Atelier line). 5× traffic lift per Etsy data.

2. [15 min, HIGH] Refactor 2 IP-risk titles
   → Replace "Dungeons & Dragons" with "5e-compatible" or
     "fantasy RPG." See WotC Fan Content Policy.

3. [20 min, HIGH] Tag 7 listings missing AI Disclosure
   → Run etsy-ai-disclosure-auditor; auto-tags after operator
     approval per listing.

4. [30 min, MEDIUM] Rewrite About page (target 300+ words)
   → Use product-first framing (per brand guidelines), not
     founder bio. Highlight craft + specs + ritual.

5. [10 min, MEDIUM] Rewrite shop announcement
   → Replace "Welcome to NoteKeepr" with hook ≤100 chars,
     e.g., "Hand-bound D&D notebooks designed to outlast
     the campaign. New quarterly drop May 22."

6. [60 min, MEDIUM] Improve response time
   → Enable Etsy mobile app notifications. Set up auto-reply
     template for common questions (shipping ETA, materials,
     custom orders).

7. [Per listing, LOW] Fill remaining tag slots on 3 listings
   → Run etsy-listing-optimizer per listing.

=== TRACKING ===

Baseline saved: keepr-ops/logs/etsy-health-2026-05-18.json
Next audit: 2026-06-18 (or after major shop changes)
Expected next-audit score (if all 7 actions taken): 87/100
```

## Strict rules

- **Never auto-fix anything** — this is a diagnostic skill; pair with `etsy-listing-publisher` / `etsy-listing-optimizer` for applies
- **Always show severity** for every gap — operator decides what to address
- **Cite the impact estimate** for every recommendation ("5× traffic per Etsy data" not just "do this")
- **Compare to baseline** if a previous audit exists — show progress or regression
- **Flag false positives** — if a "gap" is intentional (e.g., shop deliberately uses 5/13 tags for niche positioning), let the operator override

## Audit log

Save full audit to `keepr-ops/logs/etsy-health-YYYY-MM-DD.json`:

```json
{
  "audit_date": "2026-05-18T14:32:11Z",
  "shop_id": "...",
  "overall_score": 73,
  "scores_by_dimension": {
    "compliance": 28,
    "shop_signals": 22,
    "portfolio": 12,
    "seo": 8,
    "conversion": 3
  },
  "issues_found": [...],
  "top_actions": [...],
  "baseline_compared_to": "2026-04-18"
}
```

## Related skills

- All other `etsy-*` skills — the doctor calls them as sub-audits
- `keepr-dnd-skills/dnd-brand-voice` — for rewriting About page + announcements
- `coreyhaines31/marketingskills/cro` — for deeper conversion analysis
