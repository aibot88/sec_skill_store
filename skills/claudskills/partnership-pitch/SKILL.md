---
name: partnership-pitch
description: Generate brand partnership proposals and media kits — auto-compile your audience stats, engagement rates, content quality metrics, and niche authority into a professional pitch deck. Give individual creators corporate negotiation power.
---

# Partnership Pitch

Negotiate with brands as an equal. Your data is your leverage.

## When to Activate

- User says `/partnership-pitch` or `/pitch`
- User says `/pitch media-kit`
- User asks "how do I approach brands for sponsorship?"

## Commands

### `/pitch {brand}` — Generate tailored pitch for specific brand
### `/pitch media-kit` — Generate your media kit
### `/pitch rate-card` — Generate rate card for sponsored content

## Workflow

### Media Kit

```markdown
# {Name} — Media Kit

## About
{Professional bio from profile.json}

## Audience
  Total reach: {X followers + IG followers + note followers}
  Monthly impressions: ~{estimate from performance data}
  Engagement rate: {avg from performance-log}
  Audience profile: {demographics from profile}

## Platforms
| Platform | Followers | Avg Engagement | Content Type |
|----------|-----------|---------------|-------------|
| X | {N} | {rate}% | Threads, singles |
| note | {N} | {PV}/article | Articles (free + paid) |
| Instagram | {N} | {rate}% | Carousels, Reels |

## Past Work
  Top content:
  1. "{title}" — {engagement metrics}
  2. "{title}" — {metrics}

## Partnership Options
  A. Sponsored article: ¥{price}
  B. X thread mention: ¥{price}
  C. Multi-platform campaign: ¥{price}
  D. Ambassador (ongoing): ¥{price}/month

## Contact
{contact information}
```

### Tailored Pitch

```
Pitch to: {brand_name}

Subject: {brand}の{product} × {your_name}のコンテンツコラボのご提案

{Personalized pitch showing:
  - Why your audience matches their target
  - Specific content ideas for the partnership
  - Expected reach and engagement
  - Your rate and deliverables}
```

## Quality Gate

- [ ] Numbers based on actual performance data
- [ ] Media kit is professionally formatted
- [ ] Rate card reflects market standards
- [ ] Pitch is personalized to the specific brand
- [ ] Partnership options are clear with deliverables
