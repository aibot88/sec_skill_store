---
name: quickbooks-api
description: >
  Access QuickBooks Online API for invoices, payments, customers, and bills.
  Covers OAuth token auto-refresh, API queries, and Supabase ingest.
  Use when: checking invoice status, reconciling payments, querying expenses.
  Skip when: expense data already in PIL (check supabase first).
---

# QuickBooks API

> [!IMPORTANT]
> **GFV-Adapted Skill** — This skill runs within the GetFresh Ventures infrastructure.

### GFV Infrastructure Integration

**Credentials**:
```bash
# OAuth tokens (auto-refreshing)
cat ~/.gfv_qb_tokens.json
# Contains: access_token, refresh_token, realm_id, expires_at

# Refresh helper
[STUB AVOIDED] Execute qb_auth.py via available MCP/agent tools rather than a missing local script refresh
```

**Data Sources** — Check PIL FIRST:
- Supabase `entity_embeddings` where `source = 'quickbooks'`
- `gfv-expense-management` skill for organized expense tracking

---

## Overview

Queries QuickBooks Online via REST API with OAuth2 auto-refresh. Covers invoices, payments, customers, vendors, and bills. Used primarily for GFV expense management and client billing reconciliation.

## Authentication

```python
import json, requests, subprocess

# Load tokens
with open(os.path.expanduser('~/.gfv_qb_tokens.json')) as f:
    tokens = json.load(f)

# Auto-refresh if expired
if time.time() >= tokens['expires_at']:
    subprocess.run(['python3', 
        os.path.expanduser('~/Documents/Code/gfv-brain/scripts/qb_auth.py'), 
        'refresh'])
    with open(os.path.expanduser('~/.gfv_qb_tokens.json')) as f:
        tokens = json.load(f)

headers = {
    'Authorization': f"Bearer {tokens['access_token']}",
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}
BASE_URL = f"https://quickbooks.api.intuit.com/v3/company/{tokens['realm_id']}"
```

## Core Endpoints

### Invoices

```bash
# Query invoices
GET /v3/company/{realmId}/query
  ?query=SELECT * FROM Invoice WHERE TxnDate > '2026-01-01' ORDERBY TxnDate DESC MAXRESULTS 100

# Get single invoice
GET /v3/company/{realmId}/invoice/{invoiceId}

# Key fields: TxnDate, DueDate, TotalAmt, Balance, CustomerRef, Line items
```

### Payments

```bash
# Query payments
GET /v3/company/{realmId}/query
  ?query=SELECT * FROM Payment WHERE TxnDate > '2026-01-01'

# Key fields: TotalAmt, CustomerRef, PaymentMethodRef, TxnDate
```

### Bills (Expenses)

```bash
# Query bills
GET /v3/company/{realmId}/query
  ?query=SELECT * FROM Bill WHERE TxnDate > '2026-01-01'

# Key fields: VendorRef, TotalAmt, DueDate, TxnDate, Line (expense details)
```

### Customers

```bash
# Query customers
GET /v3/company/{realmId}/query
  ?query=SELECT * FROM Customer WHERE Active = true
```

### Vendors

```bash
# Query vendors (for expense tracking)
GET /v3/company/{realmId}/query
  ?query=SELECT * FROM Vendor WHERE Active = true
```

## Common Queries

```sql
-- Monthly spend by vendor
SELECT * FROM Bill WHERE TxnDate >= '2026-04-01' AND TxnDate <= '2026-04-30'

-- Outstanding invoices
SELECT * FROM Invoice WHERE Balance > '0'

-- Payments received this month
SELECT * FROM Payment WHERE TxnDate >= '2026-04-01'

-- Tech subscriptions (by vendor name)
SELECT * FROM Bill WHERE VendorRef = '{vendorId}'
```

## Supabase Ingest

```
QuickBooks API → pil_quickbooks_sync.py → Supabase entity_embeddings (source='quickbooks')
                                         → ont_facts (invoice/payment records)
```

## Rate Limits

| Tier | Limit |
|---|---|
| Standard | 500 requests / minute |
| Throttle | 10 concurrent requests |

## Anti-Patterns
- ❌ Creating invoices without the Executive's approval
- ❌ Modifying payment records
- ❌ Ignoring token refresh (will get 401s)
- ❌ Not reconciling with bank statements

## Related Skills
- **gfv-expense-management**: Organizes QB data by category
- **perplexity-invoice-pull**: Cross-references with Perplexity invoices
- **pandadoc-api**: Contract amounts should match QB invoices
- **google-workspace-access**: Invoice PDFs stored in Google Drive

## References
- **API Docs**: https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities
- **Token File**: `~/.gfv_qb_tokens.json`
- **Refresh Script**: `~/Documents/Code/gfv-brain/scripts/qb_auth.py`


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
