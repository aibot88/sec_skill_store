---
name: store-fixer
description: Authenticated Shopify implementation skill for fixing SEO, data quality, and theme issues after an audit or from a specific request. Use when a user wants to fix, implement, update, or roll out changes to product/collection content, SEO fields, image alt text, tags, schema markup, robots rules, internal linking, or other store data that requires Shopify authentication. Supports Admin GraphQL API, theme code, and mixed changes. Do not use for public-only audits (use store-analyzer), non-Shopify sites, backlink work, paid ads, or app distribution.
---

# Store Fixer

Implement Shopify store changes safely and reversibly via the Admin GraphQL API.

## Bundled Resources

Read progressively — only load what the current task needs:

- [references/access-setup.md](references/access-setup.md) — credential paths, token fetch, scope reference
- [references/graphql-mutations.md](references/graphql-mutations.md) — exact mutation syntax and gotchas
- [references/theme-fixes.md](references/theme-fixes.md) — Tier 2 Liquid code and theme backup
- [references/safety-and-rollback.md](references/safety-and-rollback.md) — canonical rollback manifest schema
- [assets/fix-plan-template.md](assets/fix-plan-template.md) — approval step format
- [assets/fix-summary-template.md](assets/fix-summary-template.md) — delivery format

## What It Can Fix

### Tier 1 — Data fixes (safe, API-only)

| Fix | API Mutation | Scope |
|-----|-------------|-------|
| Product descriptions | `productUpdate` → `descriptionHtml` | `write_products` |
| Collection descriptions | `collectionUpdate` → `descriptionHtml` | `write_products` |
| Product SEO titles/descriptions | `productUpdate` → `seo { title, description }` | `write_products` |
| Collection SEO titles/descriptions | `collectionUpdate` → `seo { title, description }` | `write_products` |
| Image alt text | `fileUpdate` → `alt` (batch) | `write_products` |
| Product type cleanup | `productUpdate` → `productType` | `write_products` |
| Vendor normalization | `productUpdate` → `vendor` | `write_products` |
| Tag cleanup | `tagsAdd` / `tagsRemove` | `write_products` |
| compare_at_price cleanup | `productVariantsBulkUpdate` | `write_products` |
| URL redirects | `urlRedirectCreate` | `write_content` |
| Article SEO tags | `metafieldsSet` on Article | `write_content` |
| Variant SKUs | `inventoryItemUpdate` → `sku` | `write_inventory` |

### Tier 2 — Theme fixes (requires `write_themes`, higher risk)

| Fix | Approach | Risk |
|-----|----------|------|
| Structured data / JSON-LD | Add `snippets/seo-schema.liquid` | Medium |
| Collection-prefixed links | Remove `within: collection` | High |
| Dawn H1-on-logo | Edit `sections/header.liquid` | Medium |
| Robots.txt AI bot rules | Create `templates/robots.txt.liquid` | Medium |

Tier 2 always requires backup before editing. See [references/theme-fixes.md](references/theme-fixes.md).

## Critical Rules

1. **Never write without explicit user approval.** Show exact changes, wait for "yes." If scope changes mid-execution, stop and re-ask.
2. **Rollback is mandatory.** Save current values before every write. Format: [references/safety-and-rollback.md](references/safety-and-rollback.md). If rollback cannot be prepared, stay in Plan mode.
3. **Use GraphQL, not REST** — except theme asset reads where REST is acceptable as fallback. See [references/graphql-mutations.md](references/graphql-mutations.md) for rate limits and mutation costs.
4. **Do NOT generate content by default.** Present the fix plan first, then ask: "Should I generate content, or do you want to provide it?"
5. **Tier 2 requires explicit opt-in.** Never modify theme files unless specifically asked.
6. **One batch at a time.** Complete one fix category, verify, then proceed.
7. **Report every failure.** Show `userErrors` immediately. On error, stop the current batch and ask how to proceed.
8. **Execute only approved scope.** Do not modify fields or resources outside the approved fix plan.

## Workflow

### 1. Confirm task mode

- **Execute**: Changes will be made (after approval).
- **Plan**: Implementation plan only, no writes.
- **Review**: User already changed the store, verify the work.

### 2. Classify the fix channel

- **Data** (Tier 1): Admin GraphQL API mutations.
- **Theme** (Tier 2): Liquid template edits. Read [references/theme-fixes.md](references/theme-fixes.md).
- **Mixed**: Both. Confirm both access paths before starting.
- **Manual**: Requires merchant-only settings or third-party app config. Provide exact manual steps.

### 3. Confirm access

Read [references/access-setup.md](references/access-setup.md). Verify with a shop query (see graphql-mutations.md). If access is missing, switch to Plan mode and tell the user exactly what they need.

### 4. Present fix plan

Use [assets/fix-plan-template.md](assets/fix-plan-template.md). Include exact counts, mutations, and scopes. Wait for approval.

### 5. Save rollback manifest

Query and save current state for every resource you'll modify. Use the canonical format in [references/safety-and-rollback.md](references/safety-and-rollback.md). Save to local file: `store-fixer-rollback-{domain}-{timestamp}.json`.

### 6. Execute in batches

Process 10-20 mutations per batch. For 50+ items, use `bulkOperationRunMutation` (see graphql-mutations.md). Check `userErrors` on every response. On error, stop and report.

### 7. Verify

**Data**: Follow-up read on 2-3 resources to confirm values changed.
**Theme**: Fetch the modified page HTML and check the target element is present/changed.

### 8. Deliver summary

Use [assets/fix-summary-template.md](assets/fix-summary-template.md). Include changes, failures, rollback file path, and any remaining manual steps.

## Rollback

1. Read the rollback manifest
2. Show what will be reverted
3. Wait for approval
4. Execute reverse mutations using `old_value` from each entry
5. For theme files: restore `original_content` or delete created files via `themeFileDelete`
6. Verify

## Content Generation Guidelines

When the user approves AI-generated content:

**Product descriptions**: 150-300 words. Write for shoppers. Include materials, sizing, care if derivable from product data. HTML with `<p>` and `<ul>` tags.

**SEO titles**: Format `{Product Name} - {Key Attribute} | {Brand}`. Under 60 chars. Note: character counts are generation constraints, not audit findings — the store-analyzer correctly ignores character-count violations because Google rewrites freely.

**SEO descriptions**: 120-155 chars. Include a benefit and product category.

**Image alt text**: Describe what's in the image. Include product name and distinguishing feature. If you can't see the image, use: `"{Product Title} - Image {n}"`.

## Examples

**Example 1**: `Fix the issues from this audit report`
→ Parse report, classify findings, present fix plan, execute with approval.

**Example 2**: `Tell me what access the client needs before we can fix product SEO and theme schema`
→ Plan-only response with exact access requirements and scopes.
