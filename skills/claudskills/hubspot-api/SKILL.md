---
name: hubspot-api
description: >
  Access HubSpot CRM API for deals, contacts, companies, and engagements.
  Covers PAT auth, deal pipeline queries, contact search, and Supabase ingest.
  Use when: querying CRM data, checking deal status, enriching contacts, syncing to PIL.
  Skip when: data already in PIL ontology (check there first).
---

# HubSpot API

> [!IMPORTANT]
> **GFV-Adapted Skill** — This skill runs within the GetFresh Ventures infrastructure.

### GFV Infrastructure Integration

**Credentials**:
```bash
# Private App Token (PAT)
security find-generic-password -s "HUBSPOT_API_KEY" -w
```

**Data Sources** — Check PIL FIRST before hitting HubSpot API:
- `search_pil` / `get_entity` MCP tools — 81K entities, many from HubSpot
- Supabase `entity_embeddings` where `source = 'hubspot'`
- `ont_entities` and `ont_facts` for relationship data

---

## Overview

Queries HubSpot CRM via REST API using a Private App Token (PAT). Covers deals, contacts, companies, and engagements. All data synced to Supabase via PIL ingest pipeline.

## Authentication

```bash
# All requests use Bearer token
HUBSPOT_API_KEY=$(security find-generic-password -s "HUBSPOT_API_KEY" -w)

curl -s "https://api.hubapi.com/crm/v3/objects/deals" \
  -H "Authorization: Bearer $HUBSPOT_API_KEY" \
  -H "Content-Type: application/json"
```

## Core Endpoints

### Deals

```bash
# List all deals
GET /crm/v3/objects/deals
  ?properties=dealname,amount,closedate,dealstage,pipeline
  &limit=100

# Get single deal
GET /crm/v3/objects/deals/{dealId}
  ?properties=dealname,amount,closedate,dealstage,pipeline,hubspot_owner_id

# Search deals by name
POST /crm/v3/objects/deals/search
{
  "filterGroups": [{
    "filters": [{
      "propertyName": "dealname",
      "operator": "CONTAINS_TOKEN",
      "value": "Acme Corp"
    }]
  }],
  "properties": ["dealname", "amount", "dealstage", "closedate"]
}
```

### Contacts

```bash
# Search contacts by email
POST /crm/v3/objects/contacts/search
{
  "filterGroups": [{
    "filters": [{
      "propertyName": "email",
      "operator": "EQ",
    }]
  }],
  "properties": ["email", "firstname", "lastname", "phone", "company"]
}

# Get contact with associations
GET /crm/v3/objects/contacts/{contactId}
  ?associations=deals,companies
```

### Companies

```bash
# Search companies
POST /crm/v3/objects/companies/search
{
  "filterGroups": [{
    "filters": [{
      "propertyName": "name",
      "operator": "CONTAINS_TOKEN",
      "value": "Acme Corp"
    }]
  }],
  "properties": ["name", "domain", "industry", "numberofemployees"]
}
```

### Engagements (emails, calls, meetings)

```bash
# Get recent engagements for a contact
GET /crm/v3/objects/contacts/{contactId}/associations/emails
GET /crm/v3/objects/contacts/{contactId}/associations/calls
GET /crm/v3/objects/contacts/{contactId}/associations/meetings
```

## Deal Pipeline Stages

| Stage ID | Stage Name | Description |
|---|---|---|
| `appointmentscheduled` | Appointment Scheduled | Initial meeting set |
| `qualifiedtobuy` | Qualified to Buy | Budget + authority confirmed |
| `presentationscheduled` | Presentation Scheduled | Demo/proposal scheduled |
| `decisionmakerboughtin` | Decision Maker Bought-In | Verbal yes |
| `contractsent` | Contract Sent | PandaDoc sent |
| `closedwon` | Closed Won | Revenue recognized |
| `closedlost` | Closed Lost | Deal dead |

## Supabase Ingest

HubSpot data is ingested into PIL via `pil_hubspot_sync.py`:
```
HubSpot API → pil_hubspot_sync.py → Supabase entity_embeddings (source='hubspot')
                                   → ont_entities (entity_type='deal'|'person'|'company')
                                   → ont_facts (subject→predicate→object)
```

## Rate Limits

| Tier | Limit |
|---|---|
| Standard | 100 requests / 10 seconds |
| Search | 4 requests / second |
| Burst | 150 requests / 10 seconds |

Always implement exponential backoff on 429 responses.

## Anti-Patterns
- ❌ Hitting HubSpot API without checking PIL first
- ❌ Stating deal status from memory — always verify from API
- ❌ Modifying deals without the Executive's approval
- ❌ Creating duplicate contacts

## Related Skills
- **hubspot-contact-enrichment**: Enrich incomplete contacts
- **pandadoc-api**: Contract status linked to deals
- **supabase-access**: Where HubSpot data lands in PIL
- **linear-api-access**: Deal tasks synced to Linear

## References
- **API Docs**: https://developers.hubspot.com/docs/api/crm
- **GFV Standard**: Three-System Sync (HubSpot + Linear + CAAI)


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
