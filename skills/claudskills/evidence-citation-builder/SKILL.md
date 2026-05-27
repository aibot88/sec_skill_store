---
name: evidence-citation-builder
description: Get citation records (source URL, retrieved_at, authority level) for a Kokai canonical record by record_id. Returns direct public source refs only (AI-derived evidence excluded).
---

## When to use

Use this skill when:

- You have a record_id (UUID) from a prior `get_entity_profile` or `get_subsidy_detail` call.
- You need cite_required references for AI-generated content.

## How to invoke

Call the kokai MCP server's `get_evidence_refs` tool:

```json
{
  "name": "get_evidence_refs",
  "arguments": {
    "record_id": "<UUID from canonical record>",
    "authority": "official",
    "limit": 20
  }
}
```

The `authority` argument accepts:

- `official` — only official sources (cite_required)
- `kokai_normalized` — Kokai-normalized records
- `ai_summary` — AI-summarized records
- `ai_estimate` — AI-estimated records

For citations in AI-generated briefs, use `authority: "official"` to get cite_required public source refs.

## Output format

For each evidence ref, format as:

```
[source_title] (source_provider) — source_url, retrieved_at, authority: <level>
```

Include in a numbered citation list at the end of your brief.

## Boundary

- Output is signal / 確認材料 / context — NOT a decision.
- Research-artifact-derived AI evidence is excluded from this call by design (memory `feedback_mcp_self_verification_caught_get_subsidy_detail_field_mismatch.md` evidence_refs gap).
