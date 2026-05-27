---
name: nta-corporate-number-lookup
description: Get authoritative Japanese corporate-number record from the National Tax Agency (国税庁) with change history (社名変更 / 移転 / 合併 / 解散). Use for M&A DD, KYC verification, dissolved-company detection, gBizINFO fallback.
---

## When to use

Use this skill when:

- The user provides a 13-digit Japanese 法人番号 (corporate number).
- You need authoritative status of the corporation: active / dissolved / merged / closed.
- You need **change history**: name changes, address moves, merger events.
- gBizINFO returned no record (small / new / non-METI-tracked entity) and you want NTA fallback.
- M&A due diligence, KYC verification, or pre-meeting research where past 沿革 matters.

## How to invoke

Call the kokai MCP server's `get_nta_corporate_record` tool:

```json
{
  "name": "get_nta_corporate_record",
  "arguments": {
    "corporate_number": "<13-digit 法人番号>",
    "include_history": true
  }
}
```

## Output structure

The response includes:

- **latest**: the current authoritative record (name, address, kind, process status, assignment date)
- **history**: previous records (name changes / address moves / etc., sorted by date desc)
- **is_dissolved** / **is_merged**: boolean flags for closure status
- **process_summary**: human-readable summary like "3 件の異動履歴あり (商号変更 / 国内所在地の変更 ...)"
- **process_label**: 公式 process classification (01=新規 / 11=商号変更 / 12=移転 / 71=合併解散 / 81=抹消 / 99=削除)
- **source_authority**: "official" (公式 cite_required layer)
- **terms_of_use**: cite gBizINFO terms

## Differentiation from gBizINFO

| 領域 | gBizINFO (`get_entity_profile`) | NTA (this skill) |
|---|---|---|
| 法人番号 master | 派生 source | **authoritative** |
| 異動履歴 (社名変更 / 移転) | 大半未提示 | **公式 + 完全** |
| 解散 / 合併消滅 detection | △ 限定的 | **公式 + 明確** |
| gBizINFO 未登録法人 | ❌ 取得不可 | **✅ カバー** |
| 財務 / 株主 / 認定 | ✅ 充実 | ❌ なし |

Pair this skill with `gbizinfo-entity-lookup` for full coverage.

## Boundary

- Output is signal / 確認材料 / context — NOT a decision.
- Final 申請可否 / 法的判断 requires a certified Japanese 士業 (行政書士 / 中小企業診断士 / 公認会計士 / 弁護士).
- Cite source_url + retrieved_at + 国税庁 attribution in final output.
- Never fictionalize. If NTA returns "no record" for a valid 法人番号, the corporation may have been recently dissolved.
