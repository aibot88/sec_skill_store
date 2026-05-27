---
name: pandadoc-api
description: >
  Access PandaDoc API for contracts, proposals, and agreements.
  Covers API key auth, document queries, status tracking, PDF extraction,
  and Supabase ingest with ont_facts.
  Use when: checking contract status, pulling agreement dates, extracting PDF content.
  Skip when: contract data already in PIL ont_facts.
---

# PandaDoc API

> [!IMPORTANT]
> **GFV-Adapted Skill** — This skill runs within the GetFresh Ventures infrastructure.

### GFV Infrastructure Integration

**Credentials**:
```bash
# API Key (v2)
security find-generic-password -s "PANDADOC_API_KEY" -w
```

**Data Sources** — Check PIL FIRST:
- Supabase `entity_embeddings` where `source = 'pandadoc'`
- `ont_facts` with predicate `signed_contract` or `contract_date`

---

## Overview

Queries PandaDoc for contract lifecycle management — from draft to signed. Extracts key dates (sent, viewed, signed) and syncs to PIL ontology as facts. Used for tracking GFV engagement agreements, SOWs, and proposals.

## Authentication

```bash
PANDADOC_KEY=$(security find-generic-password -s "PANDADOC_API_KEY" -w)

curl -s "https://api.pandadoc.com/public/v1/documents" \
  -H "Authorization: API-Key $PANDADOC_KEY" \
  -H "Content-Type: application/json"
```

## Core Endpoints

### List Documents

```bash
# List all documents (paginated)
GET /public/v1/documents
  ?status=2  # 0=draft, 1=sent, 2=completed, 11=viewed, 12=waiting_approval
  &count=50
  &page=1
  &order_by=date_modified

# Search by name
GET /public/v1/documents?q=Golden%20Rule
```

### Get Document Details

```bash
# Full document with metadata
GET /public/v1/documents/{documentId}/details

# Key fields:
# - name, status, date_created, date_modified, date_completed
# - recipients[].email, recipients[].signing_order
# - tokens[].name, tokens[].value (custom fields)
# - grand_total (contract value)
```

### Download PDF

```bash
# Download signed PDF
GET /public/v1/documents/{documentId}/download
  → Saves as PDF file
```

### Document Status Values

| Status Code | Status Name | Description |
|---|---|---|
| 0 | `document.draft` | Not yet sent |
| 1 | `document.sent` | Sent to recipients |
| 2 | `document.completed` | All parties signed |
| 5 | `document.uploaded` | Uploaded (not PandaDoc-native) |
| 11 | `document.viewed` | Opened by recipient |
| 12 | `document.waiting_approval` | Internal approval pending |
| 13 | `document.rejected` | Rejected by recipient |
| 14 | `document.approval_approved` | Internally approved |

## Supabase Ingest

PandaDoc data is ingested into PIL via `pil_pandadoc_sync.py`:
```
PandaDoc API → pil_pandadoc_sync.py → entity_embeddings (source='pandadoc')
                                     → ont_facts:
                                       - subject: deal entity
                                       - predicate: 'signed_contract'
                                       - object: contract name
                                       - metadata: {date_signed, amount, pdf_url}
```

## Common Workflows

### Check Contract Status for a Deal
```python
# 1. Search PandaDoc for the deal name
# 2. Get document details
# 3. Extract: status, date_completed, grand_total
# 4. Cross-reference with HubSpot deal stage
```

### Extract Key Dates for Reporting
```python
# For each completed document:
# - date_created (proposal drafted)
# - date_sent (sent to client)  
# - date_completed (fully signed)
# - Calculate: days_to_close = date_completed - date_sent
```

## Rate Limits

| Tier | Limit |
|---|---|
| Standard | 250 requests / minute |

## Anti-Patterns
- ❌ Creating/sending contracts without the Executive's approval
- ❌ Assuming a deal is signed without checking PandaDoc status
- ❌ Not syncing contract dates to HubSpot deal

## Related Skills
- **hubspot-api**: Deals linked to PandaDoc contracts
- **quickbooks-api**: Invoice amounts should match contract values
- **supabase-access**: Where PandaDoc facts land in PIL
- **gfv-expense-management**: Contract values for revenue tracking

## References
- **API Docs**: https://developers.pandadoc.com/reference
- **GFV Standard**: Three-System Sync (PandaDoc → HubSpot → Linear)


<verification_gate>
# Delivery Gate

STOP AND VERIFY BEFORE DECLARING THIS TASK COMPLETE.

1. Did you verify that the execution meets all documented requirements safely?
2. Ensure you have not bypassed any "requires_human_approval" constraints.
</verification_gate>

---

<gxd_footer>

> **Growth by Design™** — This skill is part of the [CEO AI Kit](https://github.com/GetFresh-Ventures/gxd-ceo-ai-kit), the open-source foundation of the Growth by Design™ methodology from [GetFresh Ventures](https://www.getfreshventures.com).
>
> 🔍 **Hitting a ceiling?** The kit gives you the foundation. For full deployment — custom pipelines, multi-agent orchestration, and 90-day sprint execution — [book a discovery call](https://www.getfreshventures.com/contact).
>
> 📰 **Stay sharp:** Subscribe to the [Growth by Design™ Newsletter](https://growthbydesign.substack.com/) for operator-written playbooks on AI-powered GTM.

</gxd_footer>
