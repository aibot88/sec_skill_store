---
name: term-sheet-analysis
description: Analyze and compare term sheets — valuation, liquidation preferences, anti-dilution, board composition, protective provisions, and option pool dynamics. Use when the user asks about analyzing a term sheet, comparing term sheets, understanding liquidation preferences, modeling exit outcomes, or evaluating board and control provisions.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, fundraising, term-sheet, negotiation, legal-terms]
related_skills:
  - fundraising-financials
  - cap-table-management
  - fundraising-process-management
  - cost-optimization
inputs_required:
  - term-sheets-from-investors-full-document
  - current-cap-table-from-cap-table-management
  - exit-scenario-assumptions-for-waterfall-modeling
deliverables:
  - term-sheet-comparison-table-markdown
  - waterfall-analysis-for-3-5-exit-scenarios
  - scorecard-recommendation-and-negotiation-priorities
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Term Sheet Analysis

Analyze and compare term sheets from multiple investors. Deconstruct each clause's economic and control impact, model real-world outcomes under different exit scenarios, and support the negotiation. Goal: the CEO understands exactly what they're signing up for.

## Purpose

A term sheet is a binding commitment dressed in non-binding language — once accepted, the economics and control dynamics are locked in for the life of the company. Founders who sign without understanding liquidation preferences, anti-dilution mechanics, or board composition often discover painful surprises at exit. This skill makes every term transparent and models what they actually mean at different exit values.

## When to Use

- "Analyze this term sheet"
- "Compare these term sheets"
- "What does this liquidation preference mean?"
- "Which term sheet is better?"
- "Model the economic outcome of these terms"
- "Explain the board and control provisions"

## Inputs Required

1. **Term sheets from investors** — full document with all economic and control terms.
2. **Current cap table** — from `cap-table-management`.
3. **Exit scenario assumptions** — range of exit values to model (low, mid, high).

## Quick Reference

| Economic Term | Normal Range | Red Flag |
|---|---|---|
| Liquidation preference | 1x non-participating (standard) | >1x, participating, cumulative dividends |
| Anti-dilution | Weighted average, broad-based | Full ratchet |
| Dividends | None (for startups) | Cumulative > 8% |
| Option pool | 10-20% post-Series A | Pre-money + oversized = hidden price cut |
| **Control Term** | **Normal** | **Red Flag** |
| Board composition | Balanced (2 founders, 2 investors, 1 independent) | Investor majority |
| Protective provisions | Approval for sale, new financing, amend charter | Approval for budget, hiring, contracts over $X |
| Exclusivity / no-shop | 30-45 days | > 60 days |

## Procedure

### 1. Term Sheet Decomposition

For each term sheet, extract and standardize all terms into a comparison table.

### 2. Economic Modeling Under Exit Scenarios

Model what everyone gets paid at different exit values:

**Scenario: $50M exit**

| | Term Sheet A (1x non-part., 12% ownership) | Term Sheet B (1x part., 15% ownership) |
|---|---|---|
| Liquidation preference | $12M | $12M |
| Participation (remaining) | — ($50M - $12M) × 12% = $4.56M | $12M + ($50M - $12M) × 15% = $17.7M |
| Total to investor | $4.56M | $17.7M |
| **Total to common/founders/employees** | $45.44M | $32.3M |

**Scenario: $200M exit**

| | Term Sheet A | Term Sheet B |
|---|---|---|
| Investor prefers non-part. | Converts to common: 12% × $200M = $24M | Converts to common: 15% × $200M = $30M |
| Common gets | $176M | $170M |

### 3. Effective Valuation (Real Price)

The headline pre-money valuation can be misleading. Calculate the **effective pre-money**:

```
Effective pre-money = (Pre-money × Post-money shares existing holders) / Post-money shares total
```

Adjust for:
- **Option pool**: if the pool increase comes from pre-money, the dilution hits existing holders, not new investors. This is a hidden price reduction.
- **Liquidation preference overhang**: a 2x liquidation preference makes that $10M investment feel like a $20M "debt" before common gets anything.

### 4. Recommendation

Score each term sheet on:
1. **Economics** (the money outcome)
2. **Control** (who makes decisions)
3. **Partner quality** (who's the person on the other side)
4. **Certainty of close** (how likely this closes)

Present a clear recommendation: "Term sheet A is better economically at exits below $80M. Term sheet B is better above $120M. Given our likely exit range of $80-150M, we recommend A."

## Key Terms to Analyze

### Economic Terms

| Term | What it Means | Normal Range | Red Flag |
|---|---|---|---|
| **Valuation (pre-money)** | Value of the company before the new investment | Varies by stage | — |
| **Amount raised** | Total new capital | — | — |
| **Liquidation preference** | Who gets paid first in an exit | 1x non-participating (standard) | >1x, participating, cumulative dividends |
| **Participation** | Can the investor "double dip"? | No (non-participating) | Yes = participating preferred |
| **Dividends** | Accruing payments on preferred stock | None (for startups) | Cumulative > 8% |
| **Anti-dilution** | Price protection for investors | Weighted average, broad-based | Full ratchet |
| **Redemption rights** | Can investors force the company to buy back their shares? | None or > 5 years | < 5 years |
| **Option pool** | Shares reserved for employee grants | 10-20% post-Series A | If the pool is pre-money and oversized — it's a way to lower the effective valuation |

### Control Terms

| Term | Normal | Red Flag |
|---|---|---|
| **Board composition** | Balanced: 2 founders, 2 investors, 1 independent | Investor majority |
| **Protective provisions** | Standard: approval for sale, new financing, amend charter | Approval for budget, hiring, contracts over $X |
| **Drag-along rights** | Standard, majority vote | Low threshold (< majority) |
| **Founder vesting** | Standard 4-year with 1-year cliff, double-trigger acceleration | Immediate acceleration on single trigger, no vesting |
| **Information rights** | Quarterly financials, annual budget | Weekly or overly granular |
| **Right of first refusal / co-sale** | Standard | — |
| **Pro-rata rights** | Standard for lead investor | Also extends to "major investors" broadly |
| **Exclusivity / no-shop** | 30-45 days | > 60 days |
| **Legal fee cap** | Company pays investor counsel up to $X | Uncapped |

## Output Format

- Term sheet comparison table (Markdown)
- Waterfall analysis for 3-5 exit scenarios
- "Red flag" summary — terms outside market norms
- Scorecard and recommendation
- Negotiation priorities (what to push back on, what to accept)

## Done Criteria

The skill is complete when:
1. All term sheets are decomposed into a standardized comparison table
2. Waterfall analysis shows what each shareholder class receives at 3-5 exit values (low, mid, high)
3. Effective pre-money valuation is calculated (adjusting for option pool and liquidation preference)
4. Each term sheet is scored on economics, control, partner quality, and certainty of close
5. Negotiation priorities are ranked — what to push back on, what to accept
6. Red flags outside market norms are clearly highlighted

## Pitfalls

- **Focusing only on valuation**: a high pre-money with participating preferred or a pre-money option pool increase can be worse than a lower headline with clean terms. Model the economics at actual exit values.
- **Ignoring board control**: board composition matters more than valuation. A board that can fire the CEO has more impact on the founder's future than an extra $2M in valuation.
- **Letting full ratchet anti-dilution through**: full ratchet is rare but devastating. It can destroy common stock value in a down round. Fight it hard — weighted average broad-based is the market standard.
- **Missing pre-money option pool tricks**: a $15M pre-money with a 15% pre-money pool increase is effectively a $12.75M pre-money for existing holders. Always adjust for this.
- **Prioritizing terms over partner**: the investor partner is more important than the firm name or the terms. A bad partner at a top firm with great terms will make life miserable for 5-10 years.

## Verification

Can you answer "which term sheet is better for the company at our likely exit range?" from the analysis? Is the effective pre-money (net of option pool and liquidation preference) calculated for each term sheet? Are red flags highlighted with explanations? Are negotiation priorities ranked with rationale? If not, the analysis is incomplete.

## Example

**User prompt**: "Analyze this term sheet."
**What should happen**: Decompose all economic terms (valuation, liquidation preference, participation, dividends, anti-dilution, option pool) and control terms (board composition, protective provisions, drag-along, vesting, no-shop), model the outcome for common shareholders at 3-5 exit scenarios, calculate the effective pre-money valuation, flag any red-flag terms outside market norms, and provide a scorecard with recommended negotiation priorities.

**User prompt**: "Compare these term sheets."
**What should happen**: Standardize both term sheets into a side-by-side comparison table, model waterfall outcomes at 3-5 exit values for each, score each on economics, control, partner quality, and certainty of close, highlight key differences, and provide a clear recommendation with rationale for which to accept and what to negotiate.

## Linked Skills

- Build financial model to test scenarios → `fundraising-financials`
- Model dilution impact → `cap-table-management`
- Track in fundraise pipeline → `fundraising-process-management`
- Vendor negotiation tactics (transferable skill) → `cost-optimization`
