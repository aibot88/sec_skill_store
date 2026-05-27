---
name: s4hana-create-po
description: Create purchase orders (POs) in SAP S/4HANA Cloud Public or on-prem private edition via the OData V2 A_PurchaseOrder deep-insert at API_PURCHASEORDER_PROCESS_SRV. Use whenever the user wants to post, create, add, generate, seed, clone, or backdate purchase orders on S/4HANA — phrases like "make me a few POs", "post 20 POs", "seed PO demo data", "create PO for supplier X material Y", "clone these on-prem POs to cloud". Handles header+item deep-insert, CSRF token flow, master-data resolution (supplier/material/plant/currency from PO ItemCategory 0), idempotent bulk batches, and known field constraints (UoM='PC', no D/9 service item categories, no account-assignment deep-insert). Do NOT use for service-based POs (item category D/9), framework agreements, scheduling agreements, or PO updates — those need different shapes (track under generic skill until verified).
---

# s4hana-create-po

Create purchase orders on SAP S/4HANA. **Verified production-ready — 88 POs migrated to `my438741.s4hana.cloud.sap` from on-prem source, plus continuous use against `s4hana.duvo.inovaflow.io` (on-prem) prior to that.**

## Phase 0 — Setup check (always do this first)

Before any other action, run the credential-presence check documented in [`shared/setup-check.md`](../../shared/setup-check.md). In short:

1. Is there a `.env` in the user's working directory, OR are `SAP_HOST` / `SAP_AUTH_MODE` already exported in shell? If yes, skip and proceed to Phase 1.
2. If neither, find the plugin's `.env.example` (typically under `~/.claude/plugins/`), offer to copy it to the user's `./.env`, append `.env` to `.gitignore` if present, and **wait** for the user to fill in values before running the main task.

## When to trigger
Verbs: create / post / add / generate / seed / make / clone / migrate / backdate
Objects: PO(s), purchase order(s)
Counts: 1 to ~100 records.

## Hard rules (never violate)
1. Always do a 1-record live POST as a probe before bulk (≥3 records).
2. Never invent master-data IDs — verify Supplier, Material, Plant exist in the target tenant first.
3. If a required field has no sensible default and the user didn't specify → **ask once**, then auto-pick.
4. Scripts go in `<cwd>/.s4hana-tmp/create-pos-<YYYYMMDD-HHMM>/`. Never commit, never modify `.env`.
5. POSTs are sequential with 200ms delay; halt on 3 consecutive failures.

## Endpoint
- Service path: `/sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrder`
- Method: POST (deep-insert with `to_PurchaseOrderItem`)
- Communication scenario: `SAP_COM_0053` — "Purchase Order Integration"

## Auth & target
Skill supports three modes (`basic`, `cc`, `oauth`) — see `../../shared/auth-modes.md`. CSRF flow is required (see `references/csrf-flow.md`).

## Phases

### Phase 1 — Parse & gather input
Detect record count and target. Required per record:

| Field | Notes |
|---|---|
| Supplier | Must exist in target. Lookup via `A_Supplier?$filter=Supplier eq '<id>'`. |
| ≥1 item with Material | Must exist + be active in target. `ProcurementType=F` (external) is the common case. |
| Item Quantity | Numeric. |
| Item NetPrice | Numeric, in document currency. |
| Item ItemText | Short free-text description. |

If user said "auto" or "random", pull from tenant defaults (see Phase 2).

### Phase 2 — Tenant defaults (cached)
Cache in `~/.claude/projects/<repo>/memory/sap-tenant-<host>.md`. If missing, discover:
- `A_Supplier?$top=20&$select=Supplier`
- `A_Product?$top=30&$filter=ProductType eq 'FERT'&$select=Product,BaseUnit`
- `A_SupplierPurchasingOrg?$top=5` → CompanyCode, PurchOrg, PurchGroup, Currency, PaymentTerms, Plant

Known good Cloud Public defaults (verify on first run): `CompanyCode=1010` · `PurchasingOrganization=1010` · `PurchasingGroup=001` · `Plant=1010` · `DocumentCurrency=EUR` · `PaymentTerms=0004` · `TaxCode=V0` · `PurchaseOrderType=NB`.

### Phase 3 — Master-data resolution
Pick deterministically using FNV-1a hash on a stable seed (same seed → same picks for reproducible reruns). Round-robin for variety, same-seed for determinism.

### Phase 4 — Build payload
See `references/po-write-quirks.md` for the seven verified gotchas. Key ones:

| Field | Quirk |
|---|---|
| `PurchaseOrderQuantityUnit` | Force to `'PC'` on Cloud Public — non-PC source units (MON/HR/CCM) get rejected as "input field cannot be processed" |
| `to_PurchaseOrderItem` | Multi-item deep-insert works in a single POST |
| `to_PurchaseOrderAccountAssignment` | Account-assignment deep-create does NOT work — keep this out of the payload entirely |
| Item categories | Skip `D` (service) and `9` (limit) — they fail on this tenant |
| System fields | Don't send `CreationDate`/`LastChangeDateTime`/`CreatedByUser` — read-only, SAP stamps at POST time |
| Backdating | Set `PurchaseOrderDate` (settable, legal/business date). System-stamped CreationDate is unavoidable. |
| URL query | Do NOT add `$format=json` to POST URL — SAP rejects it as SystemQueryOption. Use `Accept: application/json` header instead. `sap-client=NNN` is fine. |

### Phase 5 — CSRF + POST
1. `GET <host>/sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV/?sap-client=<n>` with header `X-CSRF-Token: Fetch`. Capture `x-csrf-token` from response headers + every `Set-Cookie`.
2. `POST <host>/sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrder?sap-client=<n>` with:
   - `Authorization: <auth>` (basic or bearer per mode)
   - `X-CSRF-Token: <captured token>`
   - `Cookie: <captured cookies>`
   - `Content-Type: application/json`
   - `Accept: application/json`
3. Reuse token across batch. Refresh on `403 CSRF token validation failed`.

### Phase 6 — Verify & report
After all POSTs, `$expand` 2–3 random target POs to confirm structure:
```
GET .../A_PurchaseOrder('<id>')?$expand=to_PurchaseOrderItem
```

Show user: total created, PO ID range, supplier/material distribution, any failures.

## Output structure
```
<cwd>/.s4hana-tmp/create-pos-<YYYYMMDD-HHMM>/
├── payloads.json          # all transformed POST payloads (dry-run)
├── create-log.jsonl       # one line per attempt
├── results.json           # final summary
└── verify-sample.json     # spot-check
```

## Reference files
- `references/po-write-quirks.md` — verified PO field constraints
- `references/csrf-flow.md` — exact CSRF + POST code pattern
- `references/backdate.md` — seeded backdating algorithm
- `scripts/bulk-po-poster.mjs` — reference implementation
