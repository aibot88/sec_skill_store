---
name: affiliate-writer
description: Affiliate and sponsored content generator — create natural product review, comparison, and recommendation articles that comply with ステマ規制. Integrates compliance-checker for automatic legal safety. Supports review, comparison, and experience-based formats.
---

# Affiliate Content Writer

Create product content that converts AND complies — natural recommendations, not hard sells.

## When to Activate

- User says `/affiliate {product}` or `/affiliate`
- User asks "write a product review"
- User asks "create a comparison article"
- User wants to monetize through affiliate/sponsored content

## Prerequisites

- `~/.content-autopilot/profile.json` must exist

## Commands

### `/affiliate {product}` — Generate affiliate content for a product
### `/affiliate compare {product1} vs {product2}` — Comparison article
### `/affiliate roundup {category}` — "Best X for Y" roundup

## Content Formats

| Format | Best For | Conversion | Trust |
|--------|----------|-----------|-------|
| Personal review | Single product, used it | High | Highest |
| Comparison | 2-3 products, help decide | Very High | High |
| Roundup | 5-10 products, category guide | Medium | Medium |
| Tutorial with tool | Product as part of how-to | High | Highest |
| Problem → Solution | Product solves a pain point | High | High |

## Workflow

### Step 1: Gather Product Info

```
Product details:
1. Product name: {name}
2. Category: {type}
3. Price: ¥{price}
4. Affiliate link: {url}
5. Relationship: {purchased / gifted / sponsored / affiliate only}
6. Have you used it? (yes / no)
7. Key features: {list}
8. Target user: {who benefits most}
```

### Step 2: Generate Content

**Personal Review Format:**
```markdown
PR（※本記事にはアフィリエイトリンクが含まれます）

# {Product} を{N}ヶ月使ってみた正直レビュー

## なぜ{product}を使い始めたか
{Personal story — what problem you had}

## 良かったポイント
### 1. {benefit_1}
{Specific experience with detail}

### 2. {benefit_2}
{Specific experience}

### 3. {benefit_3}
{Specific experience}

## 正直イマイチだったポイント
### 1. {drawback_1}
{Honest criticism — builds trust}

### 2. {drawback_2}
{Honest criticism}

## こんな人におすすめ / おすすめしない
おすすめ:
- {target user 1}
- {target user 2}

おすすめしない:
- {anti-target 1}
- {anti-target 2}

## まとめ
{Honest verdict — not a hard sell}

{Affiliate link with clear disclosure}

※本記事の内容は個人の使用体験に基づくものです。
効果や使用感には個人差があります。
```

**Comparison Format:**
```markdown
PR

# {Product A} vs {Product B} — {category}で選ぶならどっち？

| 項目 | {Product A} | {Product B} |
|------|-----------|-----------|
| 価格 | ¥{price} | ¥{price} |
| {feature_1} | {rating} | {rating} |
| {feature_2} | {rating} | {rating} |
| {feature_3} | {rating} | {rating} |

## {Product A}の特徴
{Details}

## {Product B}の特徴
{Details}

## 結論: こんな人は{A}、こんな人は{B}
{Nuanced recommendation — not one-sided}
```

### Step 3: Compliance Auto-Check

Automatically run compliance-checker:
```
Running compliance check...

  [x] PR表記: 記事冒頭に配置済み
  [x] アフィリエイト開示: 明記済み
  [x] 誇大表現: なし
  [x] 薬機法: 該当なし
  [x] 景品表示法: 適合

  Status: COMPLIANT — safe to publish
```

### Step 4: Save Output

```
~/Desktop/content-autopilot-output/
  affiliate_{product_slug}_{date}.md
```

## Trust-Building Rules (built into generation)

1. **Always include drawbacks** — one-sided reviews destroy trust
2. **Specifics over superlatives** — "saved 2 hours" > "amazing product"
3. **Personal experience** — "I used it for X" > "this product does X"
4. **Include "not for everyone"** — exclusion builds credibility
5. **Honest verdict** — sometimes "don't buy" IS the recommendation

## Integration with Other Skills

- **compliance-checker**: Auto-run on every affiliate piece
- **content-writer**: Affiliate format as content template option
- **launch-sequence**: Affiliate products in launch campaigns
- **testimonial-framework**: Reader testimonials about the product
- **content-grader**: Grade includes affiliate-specific criteria

## Quality Gate

- [ ] PR/affiliate disclosure at the top of content
- [ ] Both pros AND cons included (honest review)
- [ ] Specific personal experience (not generic marketing copy)
- [ ] Compliance check passed (景表法, ステマ規制)
- [ ] "Who should / shouldn't buy" section included
- [ ] Affiliate link clearly labeled
