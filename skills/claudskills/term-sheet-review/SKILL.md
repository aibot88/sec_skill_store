---
user-invocable: true
name: term-sheet-review
description: Understand investment term sheets and what terms matter
tokens: ~450
cloud-ok: true
---

# Term Sheet Review
#claudeai

## When to Use
You received a term sheet from an investor and need to understand what you're agreeing to.

## What I Need
- The term sheet (paste or upload)
- Stage (pre-seed, seed, Series A, etc.)
- Any specific concerns?

## ⚠️ Disclaimer
This helps you understand term sheets. It is NOT legal advice. Always have a startup lawyer review before signing.

## Term Sheet Anatomy

### Economic Terms (The Money)

**Valuation**
- **Pre-money:** What the company is worth before investment
- **Post-money:** Pre-money + investment amount
- Your dilution = Investment / Post-money

Example:
- $2M investment at $8M pre-money
- Post-money = $10M
- Dilution = 20%

**Option Pool**
- Reserve for future employee equity
- Watch: Is it taken from pre-money? (increases dilution)
- Typical: 10-20% for seed/A

**Liquidation Preference**
- Who gets paid first if company sells
- **1x non-participating:** Standard, fair
- **1x participating:** Investors get preference AND pro-rata (double dip)
- **>1x:** Red flag - investors get 2x+ before you see anything

### Control Terms (The Power)

**Board Composition**
- Who controls the board?
- Typical seed: 2 founders, 1 investor, or 2-1-0
- Watch: Losing board control too early

**Protective Provisions**
- Things investors can veto
- Standard: Sale of company, new equity, debt, changing charter
- Watch: Overly broad veto rights

**Pro-Rata Rights**
- Right to maintain ownership % in future rounds
- Standard and usually fine
- Benefits you if company does well

### Founder Terms

**Vesting**
- Standard: 4 years, 1 year cliff
- Watch: Acceleration on change of control (single vs double trigger)

**Founder Restrictions**
- Non-compete, non-solicit
- Watch: Overly broad restrictions

### Key Red Flags

| Term | Red Flag | Standard |
|------|----------|----------|
| Liquidation preference | >1x or participating | 1x non-participating |
| Anti-dilution | Full ratchet | Broad-based weighted average |
| Board seats | Majority to investors | Founder majority or balanced |
| Option pool | >20% from pre-money | 10-15% |
| Founder vesting | Restart from zero | Credit for time served |
| Redemption rights | Any | None |
| Dividends | Cumulative | Non-cumulative or none |

## Output Format

```
## Term Sheet Review: [Investor Name]

**Deal Summary:**
- Investment: $X
- Pre-money valuation: $Y
- Post-money: $Z
- Your dilution: X%

**Economic Terms:**
| Term | Offered | Standard | Status |
|------|---------|----------|--------|
| Liquidation pref | X | 1x non-part | 🟢/🟡/🔴 |
| Option pool | X% | 10-15% | 🟢/🟡/🔴 |
| Anti-dilution | Type | Broad-based WA | 🟢/🟡/🔴 |

**Control Terms:**
| Term | Offered | Status |
|------|---------|--------|
| Board seats | X-Y-Z | 🟢/🟡/🔴 |
| Protective provisions | [List] | 🟢/🟡/🔴 |

**Concerns:**
🔴 [Serious issue]
🟡 [Should negotiate]

**Negotiation Priority:**
1. [Most important to change]
2. [Second priority]
3. [Nice to have]

**Questions for Investor:**
1. [Clarification]
2. [Clarification]

**Recommendation:**
[Negotiate these points / Accept as-is / Major concerns]
```

## Negotiation Leverage

High leverage:
- Multiple term sheets
- Strong traction
- Hot market

Low leverage:
- Running out of money
- Only one offer
- Down market

Focus negotiations on what matters most, don't fight everything.
