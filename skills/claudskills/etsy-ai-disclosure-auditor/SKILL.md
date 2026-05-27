---
name: etsy-ai-disclosure-auditor
description: Scans every listing in an Etsy shop for missing AI Disclosure tags required by Etsy's 2025 generative-AI policy. Use when the user wants to audit AI compliance, check AI Disclosure tags, prepare a shop for the AI policy enforcement, or avoid shop suspension. Categorizes listings by risk level (clear AI / partial AI / human-made), tags accordingly with operator approval, flags ambiguous cases for manual review.
---

# Etsy AI Disclosure Auditor

You audit an entire Etsy shop for compliance with Etsy's 2025 generative-AI disclosure policy. Listings that use AI-generated images, AI-written descriptions, or AI-assisted designs without the AI Disclosure tag get hidden from search and risk shop suspension. This skill prevents that.

## When to invoke

- User says "audit AI compliance" / "check AI Disclosure tags" / "AI disclosure audit"
- User mentions Etsy's AI policy or concerns about shop suspension
- User is preparing to publish multiple new listings
- Operator wants a periodic compliance sweep (recommended monthly)

## Etsy's 2025 AI Disclosure Policy — what it actually requires

Per Etsy's published seller policy (effective 2025, enforcement increased throughout 2026):

**Listings MUST disclose AI involvement if:**
- Product images are AI-generated (Midjourney, DALL-E, Stable Diffusion, Flux, etc.)
- Product designs are AI-generated (graphics, patterns, illustrations made by AI)
- Listing descriptions are written by AI without substantial human editing
- The product itself is delivered as AI output (e.g., custom AI portraits)

**Disclosure mechanism:**
- Add the tag `ai_generated` to the listing's tag set (uses one of 13 slots)
- OR register an AI tool as a "Production Partner" under Shop Manager → Settings → Production Partners and reference it in the listing
- The Production Partner approach is preferred for shops with many AI-involved listings (doesn't waste a tag slot per listing)

**Listings do NOT need disclosure if:**
- Photos are human-taken
- Designs are human-drawn or human-designed
- Descriptions are human-written (operator typing or operator-edited from AI draft)
- AI was only used for ideation / brainstorming, not for delivered output

## Audit categories

Every listing in the shop falls into one of:

| Category | Definition | Action |
|---|---|---|
| **CLEAR AI** | AI-generated images, AI illustrations on product, AI-generated text in description (unedited) | Tag required — refuse to skip |
| **PARTIAL AI** | Human-designed cover with AI-generated interior pages, or AI-assisted layouts, or AI-edited copy | Tag recommended — flag for operator |
| **HUMAN-MADE** | No AI involvement in delivered output (operator photography, hand-drawn design, human writing) | No tag needed — log the no-AI declaration |
| **AMBIGUOUS** | Operator-uncertain or mixed-source assets | Flag for manual review — do not tag |

## Required environment

- `ETSY_API_KEY`, `ETSY_OAUTH_TOKEN`, `ETSY_SHOP_ID` set
- Token scope: `listings_r` to read, `listings_w` to apply tags

## Audit flow

1. **Pull all active listings** via `GET /v3/application/shops/{shop_id}/listings/active?limit=100` (paginate)
2. **For each listing**, score AI involvement based on heuristic signals:
   - **Image filenames** (if exposed via API metadata) — keywords like `flux`, `midjourney`, `dalle`, `_ai_`, `generated` suggest AI source
   - **Image inspection** — if image looks like AI output (uncanny details, AI-style proportions, characteristic background), flag
   - **Description style** — em-dash overuse (—), structured "Furthermore/Additionally/Moreover" phrasing, generic AI cadence
   - **Production partner declarations** — already-declared partners count as disclosed
3. **Ask the operator** for confirmation on PARTIAL and AMBIGUOUS categories
4. **Apply tags** only after explicit per-listing approval
5. **Log every decision** to audit trail

## Heuristic AI-detection signals

These are signals only — never tag based on heuristics alone, always confirm with operator:

**Strong signals (90%+ likely AI):**
- Image dimensions exactly match common AI output (1024×1024, 1024×1792, etc.)
- Filename contains AI tool names
- Operator-flagged in shop metadata

**Medium signals (50-90%):**
- Description starts with "Discover the [adjective] [product]…"
- Heavy em-dash usage with parallel structure
- "Crafted with [emotion]" phrasing
- Uncanny micro-details in product photos (extra fingers, distorted text, impossible reflections)

**Weak signals (<50%):**
- Polished writing without typos
- Stylized photography
- Modern fonts

## Output format

```
=== ETSY AI DISCLOSURE AUDIT ===

Shop: {shop_name}
Listings scanned: 47
Compliance status: 32 OK, 8 needs review, 7 missing tag

┌─ CLEAR AI (7 listings — tag missing, action required) ───────┐
│                                                              │
│ 1. listing 1234567890                                        │
│    "Custom DnD Portrait AI Art Print"                        │
│    Heuristic: filename "midjourney_v6_portrait.png"          │
│    Recommended: add tag "ai_generated"                       │
│    Apply? (y/N): _                                           │
│                                                              │
│ ... (6 more)                                                 │
└──────────────────────────────────────────────────────────────┘

┌─ PARTIAL AI (8 listings — tag recommended) ──────────────────┐
│                                                              │
│ 1. listing 1234567891                                        │
│    "Hand-bound Notebook with AI-generated Interior Art"      │
│    Description: human-written. Cover: human-photographed.    │
│    Interior pages: AI-generated decorative borders.          │
│    Recommended: add tag "ai_generated" (interior art)        │
│    Apply? (y/N/skip): _                                      │
│                                                              │
│ ... (7 more)                                                 │
└──────────────────────────────────────────────────────────────┘

┌─ HUMAN-MADE (32 listings — no action needed) ────────────────┐
│ Logged 32 listings as no-AI per operator confirmation        │
└──────────────────────────────────────────────────────────────┘

┌─ AMBIGUOUS (0 listings) ─────────────────────────────────────┐
│ No ambiguous cases found                                     │
└──────────────────────────────────────────────────────────────┘

=== ACTIONS TO APPLY ===

7 tags to add. Estimated API calls: 7.
Apply all? (y/N/per-listing): _
```

## Strict rules

- **Never apply a tag without operator confirmation** — even on CLEAR AI listings, always show the listing and ask
- **Never remove an AI Disclosure tag** — only adds
- **Never make a definitive AI/not-AI claim without operator input** — phrase as "appears to be" or "heuristic suggests"
- **Always log the audit** even if no tags applied — operator may need to prove compliance attempt later
- **If ≥50% of shop is AI-flagged**, recommend the operator register an AI Production Partner instead of per-listing tagging

## Output log

Save audit results to `keepr-ops/logs/etsy-ai-audit-YYYY-MM-DD.json`:

```json
{
  "audit_date": "2026-05-18T14:32:11Z",
  "shop_id": "...",
  "listings_scanned": 47,
  "clear_ai": [{"listing_id": "...", "tag_applied": true}, ...],
  "partial_ai": [...],
  "human_made_count": 32,
  "ambiguous": [],
  "operator_signature": "jack@reimaginemediagroup.com"
}
```

This log is the operator's proof of due diligence if Etsy ever requests it.

## Related skills

- `etsy-listing-publisher` — calls this audit as a pre-flight check
- `etsy-listing-optimizer` — runs alongside for SEO + compliance combined audit
- `etsy-shop-doctor` — broader shop health audit that includes this one
