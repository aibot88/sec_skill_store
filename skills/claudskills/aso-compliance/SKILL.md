---
name: aso-compliance
description: >
  Store policy compliance checker for iOS App Store and Google Play. Validates
  metadata against Apple App Store Review Guidelines and Google Play Developer
  Program Policies. Catches violations that would cause rejection. Also validates
  ASO recommendations from other agents.
  Triggers on: "compliance", "policy check", "guidelines", "store policies",
  "review guidelines", "will this get rejected", "is this allowed".
user-invokable: true
argument-hint: "[app-id] [--platform ios|android]"
---

# ASO Compliance — Store Policy Checker

Validates app metadata against Apple App Store Review Guidelines and Google Play Developer Program Policies. Catches violations before they cause rejection.

## Two Modes

1. **Standalone**: `/aso compliance` or `/aso compliance <app-id>` — check current metadata
2. **Audit integration**: Runs automatically as part of `/aso audit` after all agents return, validating both current metadata AND recommended changes

## Process

### Step 1: Get Metadata

Same as other skills — local detection or remote fetch:
```bash
uv run python scripts/detect_project.py --json   # local mode
uv run python scripts/fetch_listing.py <id> --json  # remote mode
```

### Step 2: Load Policy Reference

Read `references/store-policies.md` for the complete rule set covering:
- Title restrictions and banned words
- Description content prohibitions
- Keyword spam rules
- Screenshot requirements
- Pricing/IAP disclosure rules
- Health/medical claim restrictions
- Financial claim restrictions
- Review manipulation rules
- AI content policies
- Intellectual property rules

### Step 3: Run Compliance Checks

For each metadata field, check against every applicable rule for the detected platform.

**Title checks:**
- Banned words present? (Google: "#1", "best", "top", "free", "download now", etc.)
- Competitor brand names?
- Trademarked terms without license?
- ALL CAPS? (Google: prohibited unless registered brand)
- Emojis? (Google: prohibited in title)
- Other platform names? (Apple: no "Android")
- Pricing language?

**Description checks:**
- Testimonials? (Google: prohibited)
- Rating/performance claims? ("4.9 stars", "million downloads")
- Pricing info? ("$X off", "free trial", "limited time")
- Call-to-actions? (Google: "download now", "install now")
- Competitor names?
- Keyword stuffing? (unnatural density)
- Misleading functionality claims?

**Category-specific checks:**
- Health apps: disclaimers present? No unvalidated measurement claims?
- Finance apps: APR disclosed? Financial features declaration done?
- AI apps: data sharing disclosed? In-app reporting?
- Gaming: loot box odds disclosed? IAP transparent?

**IAP/pricing checks:**
- If app has IAP: disclosed in description and screenshots?
- If "free": any essential features behind paywall?
- Subscription terms clear?

**Screenshot checks** (if descriptions/captions available):
- Promotional text present? ("#1", "Best", "Sale")
- Ranking claims?
- Non-app UI elements?

### Step 4: Report

**Severity levels:**

| Level | Meaning | Icon |
|-------|---------|------|
| VIOLATION | Will likely cause rejection | Must fix |
| RISK | May trigger review or penalty | Should fix |
| ADVISORY | Best practice recommendation | Consider |

**Output format:**

```markdown
## Compliance Report: [App Name]

**Platform**: [iOS / Android / Both]
**Result**: [X violations, Y risks, Z advisories]
**Compliance Score**: XX/100

### Violations (Must Fix)
| # | Field | Rule | Issue | Fix |
|---|-------|------|-------|-----|
| 1 | title | Google Banned Words | Contains "#1" | Remove and use descriptive keyword |

### Risks (Should Fix)
| # | Field | Rule | Issue | Fix |
|---|-------|------|-------|-----|

### Advisories (Consider)
| # | Field | Rule | Issue | Fix |
|---|-------|------|-------|-----|

### Recommendation Flags
[If running as part of audit — list any agent recommendations that violate policies]
| Source | Recommendation | Violation | Alternative |
|--------|---------------|-----------|-------------|
```

## When Running as Part of Audit

The compliance agent runs AFTER all other agents return (Step 3.5 in audit flow). It receives:
1. Current metadata (same as other agents)
2. Recommendations from all agents (title rewrites, keyword suggestions, description changes)

It validates ALL recommendations against store policies. Any violating recommendation is:
- Flagged in the compliance report
- Removed from the final ASO-ACTION-PLAN.md
- Replaced with a compliant alternative where possible

This ensures the audit NEVER recommends metadata that would get the app rejected.

## Available Tools
Read, Bash, Write, Glob, Grep
