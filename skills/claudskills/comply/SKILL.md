---
name: comply
description: Run full import compliance analysis — classify, duty, PGA, entry type, and declaration readiness in one shot using AskRosetta. Use for end-to-end import analysis.
argument-hint: "<product description> <value> from <country>"
---

# Full Compliance Analysis

Run the complete AskRosetta pipeline: HTS classification, duty calculation, PGA screening, entry type recommendation, and declaration readiness — all in one pass.

## When to Use

- User asks "how much will it cost to import X?"
- User wants a complete compliance picture
- User is preparing for a specific shipment

## How It Works

Use the `analyze_product` MCP tool, or call the quote endpoint:

```bash
curl -s -X POST "https://api.askrosetta.ai/api/v1/quote" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${ASKROSETTA_API_KEY}" \
  -d '{
    "products": [{
      "description": "<description>",
      "country_of_origin": "<country>",
      "unit_value": <number>,
      "quantity": <number>
    }],
    "shipping_method": "<ocean|air|truck>"
  }'
```

## Response Format

Present as a structured compliance report:

---
**COMPLIANCE REPORT**

**1. Classification**
- HTS: `XXXX.XX.XXXX` — Description
- Confidence: XX%

**2. Duty & Fees**
| Component | Amount |
|-----------|--------|
| Base Duty | $XXX.XX |
| Section 301 | $XXX.XX |
| MPF | $XX.XX |
| HMF | $XX.XX |
| **Landed Cost** | **$X,XXX.XX** |

**3. PGA Requirements**
- FDA: Required / Not required
- EPA: Required / Not required

**4. Entry Type**
- Recommended: Type XX — Informal/Formal
- Bond required: Yes/No
- Broker required: Yes/No
---

## Important

This is intelligence, not legal advice. For actual customs filing, the user must work with a licensed customs broker.
