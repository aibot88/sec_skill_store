---
name: authority-strip-formatter
description: Format the ACBS 4-layer authority strip in Kokai-generated outputs. Apply to all briefs that include Kokai data.
---

## When to use

Apply this skill when generating any brief / report / output that includes Kokai data. The 4-layer authority strip is a core part of the Kokai brand promise: every data point in a brief should be classified into one of 4 authority tiers.

## The 4 layers

| Layer | Name | Cite requirement | Examples |
|---|---|---|---|
| 1 | 公式 (official) | **cite_required** | gBizINFO records, J-Grants public registry, 国税庁 法人番号 公表 |
| 2 | Kokai normalized | **cite_required** | Kokai-normalized records derived from official sources |
| 3 | AI summary | recommended | AI-generated summary of cited records |
| 4 | AI estimate | recommended | AI-estimated values where official data is absent |

## Output format

At the footer of every Kokai brief, include:

```
---
出典 4 階層:
- 公式: <count> records (cite_required)
- Kokai 正規化: <count> records (cite_required)
- AI 要約: <count>
- AI 推定: <count>

詳細出典: <list of source URLs with retrieved_at>
```

In English:

```
---
Authority strip (4 layers):
- Official: <count> records (cite_required)
- Kokai normalized: <count> records (cite_required)
- AI summary: <count>
- AI estimate: <count>

Sources: <list of source URLs with retrieved_at>
```

## Boundary

- Never present AI estimates or AI summaries as official facts.
- Always cite source URLs for the top 2 layers.
