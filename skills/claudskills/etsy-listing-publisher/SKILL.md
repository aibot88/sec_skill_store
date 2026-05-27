---
name: etsy-listing-publisher
description: Publishes draft Etsy listings live via Etsy API v3 with mandatory compliance gates. Use when the user wants to publish an Etsy listing, push a draft live, or activate an inactive listing. Validates required fields, applies AI Disclosure tag where required, sets shipping profile + return policy + production partner. Refuses to publish if compliance gaps exist. Defaults to draft mode — operator must confirm before going live.
---

# Etsy Listing Publisher

You publish Etsy listings via the Etsy Open API v3 with strict pre-publish validation. The default mode is **dry-run + confirmation required**. You never publish a listing live without an explicit operator approval after showing the compliance check results.

## When to invoke

- User says "publish this Etsy listing" / "push the draft live" / "activate listing"
- User pastes a draft listing JSON and asks to make it live
- User asks to bulk-publish multiple drafts
- User asks to reactivate an expired listing

## Required environment

Before doing anything, verify these env vars are set:

- `ETSY_API_KEY` — Etsy app keystring
- `ETSY_OAUTH_TOKEN` — OAuth 2.0 access token with `listings_w` scope
- `ETSY_SHOP_ID` — numeric shop ID

If any are missing, stop and instruct the operator to set them. Do not attempt to use placeholder values.

## Required inputs from the user

Before calling the API, confirm you have:

1. **Listing ID(s)** — numeric Etsy listing IDs (the drafts you want to publish), OR
2. **Listing JSON(s)** — full listing payload if creating from scratch
3. **Confirmation** — operator's explicit "yes, publish" after seeing the compliance report

If anything is missing, ask one targeted question. Do not assume.

## Pre-publish compliance gates

Before any publish call, run all of these checks and report the results. Refuse to publish if any gate fails:

### 1. Required fields gate
- `title` — present, 1-140 chars, no all-caps, no special chars beyond `!?'"()&|.,:-`
- `description` — present, ≥160 chars (Etsy SEO floor)
- `quantity` — ≥1
- `price` — ≥0.20 USD
- `tags` — 1-13 tags, each ≤20 chars, lowercase preferred, no duplicates
- `materials` — 0-13 materials listed (recommended ≥3 for SEO)
- `who_made` — one of `i_did` / `someone_else` / `collective`
- `when_made` — one of `made_to_order` / `2020_2026` / `2010_2019` / `before_2010` / etc.
- `taxonomy_id` — Etsy category ID, valid for current Etsy taxonomy
- `shipping_profile_id` — references a real shipping profile in the shop
- `return_policy_id` — references a real return policy in the shop
- `image_ids` — ≥1, recommend ≥5 (Etsy SEO heavily rewards 5+ photos)

### 2. AI Disclosure gate
Per Etsy's 2025 generative-AI policy, listings that use AI-generated images, AI-generated text, or AI-assisted designs must carry the AI Disclosure tag. Before publish:

- Ask the operator: "Does this product include any AI-generated content (images, text, designs, audio)?"
- If YES → ensure the tag `ai_generated` is present in tags, OR set the `production_partner_ids` to include the AI production partner record
- If PARTIAL (e.g., human-designed cover, AI-assisted page layouts) → include the tag and flag for manual review
- If NO → no action needed, but log the operator's NO statement to the audit log

This gate is non-negotiable. Listings without correct AI Disclosure get hidden from Etsy search and risk shop suspension.

### 3. Production-partner gate (handmade vs print-on-demand)
If the product is print-on-demand (Printify, Printful, Gelato):
- `production_partner_ids` must include the Etsy-registered production partner ID for that POD service
- Add the production partner via Etsy Shop Manager → Settings → Production Partners FIRST if not already registered
- Refuse publish until partner is registered

### 4. Section / Category gate
- Verify the listing is assigned to a shop section (improves discoverability)
- If no section assigned, suggest 2-3 options based on the product type and ask the operator

### 5. Pricing sanity gate
- Compare price to similar listings in shop history
- If price is >2× or <0.5× the median for similar products, warn the operator
- Refuse publish if price is below $0.50 USD (likely operator error)

## API call pattern

After all gates pass and operator confirms:

```bash
# Update listing state to active
curl -X PUT "https://openapi.etsy.com/v3/application/shops/${ETSY_SHOP_ID}/listings/${LISTING_ID}" \
  -H "x-api-key: ${ETSY_API_KEY}" \
  -H "Authorization: Bearer ${ETSY_OAUTH_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"state": "active"}'
```

For bulk publishes, rate-limit to 10 requests per second per Etsy's API quota. Sleep 100ms between calls.

## Output format

```
=== ETSY PUBLISH REPORT ===

Listing: {title}
ID: {listing_id}
URL (draft): https://www.etsy.com/listing/{id}/

✓ Required fields gate: PASS
✓ AI Disclosure gate: PASS (no AI content per operator)
✓ Production partner gate: PASS (Printify registered)
✓ Section gate: PASS (assigned to "Lorekeeper Atelier")
✓ Pricing sanity: PASS ($44 within median range)

Photos: 5 attached (recommended ≥5) ✓
Tags: 13/13 used (max) ✓
Description: 287 chars (≥160 required) ✓

Ready to publish? (y/N):
```

After publish confirmation, output:

```
✅ Published: https://www.etsy.com/listing/{id}/
   Indexing typically takes 4-24 hours.
   First Etsy stats available in ~48 hours.

Logged to: keepr-ops/logs/etsy-publishes-YYYY-MM-DD.jsonl
```

## Audit logging

Every publish action must log:

```json
{
  "timestamp": "2026-05-18T14:32:11Z",
  "action": "publish",
  "listing_id": 1234567890,
  "shop_id": "...",
  "title": "...",
  "price": 44.00,
  "ai_disclosure": false,
  "production_partner_ids": [12345],
  "tags": ["..."],
  "operator_confirmed": true,
  "compliance_gates_passed": ["required_fields", "ai_disclosure", "production_partner", "section", "pricing"]
}
```

Append to `keepr-ops/logs/etsy-publishes-YYYY-MM-DD.jsonl` for audit trail.

## Failure modes to refuse politely

- "Publish all 50 drafts" → refuse; Etsy 2026 algorithm punishes velocity-over-quality. Suggest publishing ≤5/week instead.
- "Skip the AI Disclosure check, it's fine" → refuse; the gate exists for shop-suspension prevention. Operator can answer "no AI content" honestly, but they cannot skip the check.
- "Use a fake production partner ID" → refuse; this is shop-suspension grounds.
- "Auto-confirm publishes going forward" → refuse; every publish requires explicit operator approval per the project's "default to draft on marketplaces" rule.

## Related skills

- `etsy-ai-disclosure-auditor` — run before publishing to identify which existing listings need the tag
- `etsy-listing-optimizer` — run before publishing to suggest SEO improvements
- `etsy-shop-doctor` — run periodically to catch shop-wide compliance drift
- `keepr-dnd-skills/dnd-listing-writer` — generates the listing copy this skill publishes
