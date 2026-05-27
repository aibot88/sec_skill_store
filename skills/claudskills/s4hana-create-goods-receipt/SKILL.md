---
name: s4hana-create-goods-receipt
description: Create Goods Receipts (Material Documents) in SAP S/4HANA Cloud Public or on-prem private edition via OData V2 A_MaterialDocumentHeader deep-insert at API_MATERIAL_DOCUMENT_SRV. Use whenever the user wants to create, post, add, generate, seed, receive, or confirm receipt of goods on S/4HANA — phrases like "post a goods receipt", "receive goods for PO X", "create GR for these POs", "seed GR demo data", "post GRs", "complete the 3-way match", "post material document". Handles full header + item deep-insert, CSRF flow, partial vs full receipt, idempotent bulk batches with per-record logging, and the GoodsMovementRefDocType=B requirement for PO-based receipts. Do NOT use for goods issues (movement types 201/261/etc.), stock transfers (movement types 311/411/etc.), or inventory counts (use Physical Inventory API).
---

# s4hana-create-goods-receipt

Create Goods Receipts (Material Documents) on SAP S/4HANA Cloud Public. **Verified production-ready against `my438741.s4hana.cloud.sap` 2026-05-12 — Material Documents 5000000001 + 5000000002 posted via API.**

## When to trigger
Verbs: create / post / add / generate / seed / receive / confirm
Objects: GR(s), Goods Receipt(s), Material Document(s), receipt of goods
Counts: 1 to ~100 records.

## Hard rules (never violate)
1. Always do a 1-record live POST as a probe before bulk (≥3 records).
2. Never invent material/PO IDs — Material must match the referenced PO line exactly (`M7/360` if mismatched).
3. If a required field has no sensible default and the user didn't specify → **ask once**, then auto-pick.
4. Scripts go in `<cwd>/.s4hana-tmp/create-grs-<YYYYMMDD-HHMM>/`. Never commit, never modify `.env`.
5. POSTs are sequential with 200ms delay; halt on 3 consecutive failures.
6. **Do NOT include `PurchaseOrder`/`PurchaseOrderItem` fields WITHOUT also including `GoodsMovementRefDocType="B"`** — the API rejects the fields as "not supported for type 101" without that hint.

## Endpoint
- Service path: `/sap/opu/odata/sap/API_MATERIAL_DOCUMENT_SRV`
- Entity sets: `A_MaterialDocumentHeader`, `A_MaterialDocumentItem`
- Method: POST (deep-insert with `to_MaterialDocumentItem`)
- Communication scenario: **`SAP_COM_0108`** — "Material Document Integration"

## Phase 0 — Setup check (always do this first)

Before any other action, run the credential-presence check documented in [`shared/setup-check.md`](../../shared/setup-check.md). In short:

1. Is there a `.env` in the user's working directory, OR are `SAP_HOST` / `SAP_AUTH_MODE` already exported in shell? If yes, skip and proceed to Phase 1.
2. If neither, find the plugin's `.env.example` (typically under `~/.claude/plugins/`), offer to copy it to the user's `./.env`, append `.env` to `.gitignore` if present, and **wait** for the user to fill in values before running the main task.

## Phases

### Phase 1 — Parse & gather input

Per GR, required:

| Field | Notes |
|---|---|
| `PurchaseOrder` + `PurchaseOrderItem` | The PO line being received against |
| `Material` | Must EXACTLY match the PO line's material (`M7/360` otherwise) |
| `Plant` | Match PO line |
| `StorageLocation` | Default `101A` for plant 1010 on `my438741`. Varies by tenant. |
| `QuantityInEntryUnit` + `EntryUnit` | Partial receipts allowed (typical: 25–100% of order qty) |
| `PostingDate` | **Must be in open MM posting period** — same gate as SES (typically 2025/07 or 2025/08 on this tenant) |
| `GoodsMovementType` | `"101"` = Receipt for PO to warehouse (most common) |
| `GoodsMovementRefDocType` | **`"B"`** for PO reference (without this, PURCHASEORDER fields are rejected) |

If user said "auto" or "random", pull eligible PO lines:
```
GET /sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrderItem?$filter=ProductType eq '1' and PurchaseOrderItemCategory eq '0' and IsCompletelyDelivered eq false&$select=PurchaseOrder,PurchaseOrderItem,Material,Plant,OrderQuantity,PurchaseOrderQuantityUnit
```

Skip PO lines whose Material is `M7/175: Maintain serial numbers` (serialized materials need extra fields).

### Phase 2 — Tenant defaults
Cache via tenant memory. For `my438741`:

| Setting | Value |
|---|---|
| Plant | `1010` |
| StorageLocation default | `101A` |
| GoodsMovementCode (header) | `"01"` |
| GoodsMovementType (item) | `"101"` |
| GoodsMovementRefDocType (item) | `"B"` |
| Open MM posting period | `2025/07`, `2025/08` (verify with M7/053 if uncertain) |

### Phase 3 — Build payload

**Verified working envelope:**

```json
{
  "DocumentDate": "/Date(<ms>)/",
  "PostingDate": "/Date(<ms>)/",
  "MaterialDocumentHeaderText": "API GR batch ABC",
  "GoodsMovementCode": "01",
  "to_MaterialDocumentItem": [
    {
      "Material": "FG041",
      "Plant": "1010",
      "StorageLocation": "101A",
      "GoodsMovementType": "101",
      "GoodsMovementRefDocType": "B",
      "PurchaseOrder": "4500000000",
      "PurchaseOrderItem": "10",
      "QuantityInEntryUnit": "250",
      "EntryUnit": "PC"
    }
  ]
}
```

**Critical field — `GoodsMovementRefDocType="B"`**: SAP V2 OData treats type 101 with `PurchaseOrder` fields as ambiguous unless you also pass `GoodsMovementRefDocType="B"` (B = Purchase Order). Without it: `MM_IM_ODATA_API_MDOC/011: Property PURCHASEORDER is not supported for GoodsMovementType 101`. Easy fix, but unintuitive — easy to miss.

### Phase 4 — CSRF + POST
Standard OData V2 CSRF flow — see `../s4hana-create-po/references/csrf-flow.md`. MaterialDocument ID is auto-assigned in `500000000x` range, paired with `MaterialDocumentYear`.

### Phase 5 — Verify
```
GET /A_MaterialDocumentHeader(MaterialDocument='<id>',MaterialDocumentYear='<yr>')?$expand=to_MaterialDocumentItem
```

After GR posting, the referenced PO line's `IsCompletelyDelivered`, `GoodsReceiptQuantity`, and related stock fields update automatically.

## Known error catalog

| Code | Cause | Fix |
|---|---|---|
| `MM_IM_ODATA_API_MDOC/011` | "Property PURCHASEORDER not supported for GoodsMovementType 101" | Add `GoodsMovementRefDocType="B"` on the item |
| `MM_IM_ODATA_API_MDOC/014` | "Material Document processing failed" | Generic — read other error rows in the response for specifics |
| `M7/360` | "Material document data and PO data do not match (Material)" | Material on GR item must match PO line material exactly |
| `M7/001` | "Check table EKPO: entry ... does not exist" | The PurchaseOrderItem doesn't exist on the PO. Verify with a GET first |
| `M7/175` | "Maintain serial numbers for total quantity" | Material requires serial-number tracking — needs `to_SerialNumber` deep-insert (out of scope for typical demo) |
| `M7/053` | "Posting only possible in periods YYYY/MM" | `PostingDate` outside open MM period — backdate or open current period |
| `ME/006` | "User X already processing Purchasing doc item Y" | Lock — another session is editing the PO. Wait 5–30s and retry, or pick a different PO |
| `403 You do not have start authorization for R3TR IWSV API_MATERIAL_DOCUMENT_SRV` | Comm arrangement `SAP_COM_0108` not added | Add the arrangement in Fiori → Communication Arrangements → New → `SAP_COM_0108` |

## Output structure
```
<cwd>/.s4hana-tmp/create-grs-<YYYYMMDD-HHMM>/
├── eligible-po-lines.json
├── create-log.jsonl
├── results.json
└── verify-sample.json
```

## Reference files
- `references/envelope-template.md` — full schema with optional fields
- `references/movement-types.md` — common movement-type codes and their semantics
- `scripts/bulk-gr-poster.mjs` — reference implementation
