---
name: s4hana-update-record
description: Update existing records in SAP S/4HANA Cloud Public or on-prem private edition via OData V2 PATCH. Use whenever the user wants to update, change, edit, modify, patch, set, rename, adjust, or correct any existing record on S/4HANA — purchase orders (dates, payment terms, item text/qty/price), business partners (name, address, payment terms, recon account), product descriptions (Toblerone-style overrides), service entry sheets (name, qty before approval), purchasing info records, supplier purchasing-org assignments, etc. Triggers on phrases like "update PO X", "change supplier address", "rename product", "backdate PO 4500...", "adjust PIR price for supplier Y", "set new payment terms for X". Handles GET-before-PATCH (to show current state), composite key resolution, CSRF flow, the "204 looks-like-success-but-no-change" trap (verifies via GET-after-PATCH), write-once field detection, and entity-disabled checks. Do NOT use for CREATE operations (use the s4hana-create-* skills), DELETE (most entities don't support DELETE on Cloud Public — block + rename instead), or for entities where update is entirely disabled (Supplier Invoice and Material Document — those return 405 CX_SADL_ENTITY_CUD_DISABLED and need cancel-recreate workflows).
---

# s4hana-update-record

Generic update skill for SAP S/4HANA records. **Verified pattern against `my438741.s4hana.cloud.sap` 2026-05-12 — 6 different entity types successfully PATCH'd; 2 confirmed entity-disabled; 1 "silent success" trap documented.**

## When to trigger
Verbs: update / change / edit / modify / patch / set / rename / adjust / correct / backdate / amend
Objects: any existing S/4HANA record — PO, supplier, customer, BP, PIR, SES, product description, etc.

## When NOT to trigger
- User wants to CREATE a record → use `s4hana-create-*` skills
- User wants to DELETE → Cloud Public blocks DELETE on most entities. Use block-and-rename (PATCH `BusinessPartnerIsBlocked=true` etc.) instead.
- User wants to update Supplier Invoice or Material Document → those are entity-disabled (405). They need cancel-and-recreate (use the cancellation flow in the relevant create skill instead).

## Hard rules (never violate)

1. **GET before PATCH, GET after PATCH.** Always show user the BEFORE state, then PATCH, then VERIFY the change actually took effect with a fresh GET. Many fields return 204 "success" but don't actually update — only the post-PATCH GET reveals the truth.
2. **Confirm with user before PATCHing batches >3.** Show the planned BEFORE/AFTER diff for the first record, get explicit confirmation, then proceed.
3. **If post-PATCH GET shows unchanged value**, surface it as a "silent failure" — DON'T claim success.
4. **Never invent values.** If the user says "set PO X date to Aug 2025", use a specific date they confirmed, not a random one.
5. Scripts go in `mcp-server/src/sap/.tmp/<user>-<YYYYMMDD-HHMM>/update-<entity>/`. Never commit, never modify `.env`.

## Phase 0 — Setup check (always do this first)

Before any other action, run the credential-presence check documented in [`shared/setup-check.md`](../../shared/setup-check.md).

## Phases

### Phase 1 — Identify entity + record + field(s)

Parse the user's intent:
- **Entity**: PO, BP, PIR, etc. — map to OData service + entity set.
- **Record key(s)**: Single-key (e.g. `PurchaseOrder='4500000020'`) or composite (e.g. PIR org-plant has 4 keys).
- **Fields**: What does the user want changed? Translate domain language ("payment terms") to API field names (`PaymentTerms`).

If ambiguous, **ask once** before proceeding. Show the user your planned interpretation: "I'm going to update PO 4500000020's `PurchaseOrderDate` to `2025-08-15`. Correct?"

For known entities, use the table below to find the right endpoint. For unknown entities, switch to research mode (Phase 1b).

### Phase 1b — Research mode (for unknown entities)

If the entity isn't in the verified table:
1. Identify the OData service via `$metadata` lookup or search SAP API Hub.
2. Fetch the entity's `$metadata` and inspect:
   - **Key fields**: which fields make up the primary key
   - **`sap:updatable="false"`** on properties (write-once fields)
   - **`sap:creatable`** annotations (which fields appear in PATCH vs POST)
3. Try minimal PATCH, iterate on errors.
4. Document the working pattern in `references/mutable-fields-catalog.md` for next time.

### Phase 2 — GET current state (before)

```http
GET /sap/opu/odata/sap/<SERVICE>/<EntityKey>?$select=<key fields + target fields>&$format=json
Authorization: Basic <auth>
Accept: application/json
```

Show user: "Current value of `PurchaseOrderDate` is `2026-04-30`. Want me to change it to `2025-08-15`?"

For batch operations, GET each record (or a sample) and show the user a table of planned changes before any PATCH.

### Phase 3 — PATCH

```http
PATCH /sap/opu/odata/sap/<SERVICE>/<EntityKey>?sap-client=<n>
Authorization: Basic <auth>
X-CSRF-Token: <captured>
Cookie: <captured>
Content-Type: application/json
Accept: application/json

{"<field>": "<new value>"}
```

PATCH semantics: **partial update**. Only send the field(s) you want to change — don't echo the full record. Body should be minimal.

Expected response: **HTTP 204 No Content** (success) or **HTTP 400** with `error.innererror.errordetails` for failures.

### Phase 4 — GET to verify (after)

```http
GET /sap/opu/odata/sap/<SERVICE>/<EntityKey>?$select=<target fields>&$format=json
```

Compare BEFORE → AFTER for each field. Report to user:
- ✅ Changed as expected: `PurchaseOrderDate: 2026-04-30 → 2025-08-15`
- ❌ Unchanged despite 204: `NetPriceAmount: 50.00 → 50.00 (silent failure — field may be read-only despite 204 response)`
- ❌ Rejected: log the error details

### Phase 5 — Report

After single or batch: summarize changes, surface any silent failures or rejections, write log to disk.

## Output structure
```
mcp-server/src/sap/.tmp/<user>-<YYYYMMDD-HHMM>/update-<entity>/
├── targets.json             # records to update + proposed changes
├── before.json              # GET-before snapshots
├── update-log.jsonl         # one line per PATCH attempt
├── after.json               # GET-after snapshots
├── diff.md                  # human-readable before/after table
└── results.json
```

## Verified update patterns (mutable-fields catalog)

See `references/mutable-fields-catalog.md` for the full per-entity catalog. Quick summary:

| Entity | Service | What works | Notes |
|---|---|---|---|
| `A_BusinessPartner` | `API_BUSINESS_PARTNER` | `OrganizationBPName1` and most header fields | Single key: `BusinessPartner` |
| `A_BusinessPartnerAddress` | `API_BUSINESS_PARTNER` | `CityName`, `StreetName`, `PostalCode`, `Country` | Composite key: `BusinessPartner` + `AddressID` |
| `A_ProductDescription` | `API_PRODUCT_SRV` | `ProductDescription` | Composite key: `Product` + `Language`. Useful for Toblerone-style overrides |
| `A_PurchaseOrder` | `API_PURCHASEORDER_PROCESS_SRV` | `PurchaseOrderDate`, `PaymentTerms`, header text, most header fields | NOT `Supplier`, `CompanyCode`, `PurchasingOrganization` — write-once |
| `A_PurchaseOrderItem` | `API_PURCHASEORDER_PROCESS_SRV` | `PurchaseOrderItemText`, `NetPriceAmount`, `OrderQuantity`, `Plant`, `StorageLocation` | NOT `Material`, `PurchaseOrderItemCategory` — write-once |
| `A_ServiceEntrySheet` | `API_SERVICE_ENTRY_SHEET_SRV` | `ServiceEntrySheetName`, `PostingDate` (pre-approval) | After approval (workflow status changes), most fields lock |
| `A_PurgInfoRecdOrgPlantData` | `API_INFORECORD_PROCESS_SRV` | Status fields, validity dates | **TRAP: `NetPriceAmount` returns 204 but DOES NOT change** — see known-traps.md. Price is in `to_PurInfoRecdPrcgCndnValidity` |
| `A_SupplierPurchasingOrg` | `API_BUSINESS_PARTNER` | `PaymentTerms`, `PurchaseOrderCurrency` | Composite key: `Supplier` + `PurchasingOrganization` |
| `A_SupplierCompany` | `API_BUSINESS_PARTNER` | `PaymentTerms`, `ReconciliationAccount` | Composite key: `Supplier` + `CompanyCode` |

## Entity-disabled (PATCH always fails)

Don't even try — these entities reject all PATCH with `405 CX_SADL_ENTITY_CUD_DISABLED`. They need cancel-and-recreate flows:

| Entity | Why | Alternative |
|---|---|---|
| `A_SupplierInvoice` | Posted invoices are immutable for audit | Cancel via `Cancel_SupplierInvoice` action + create new |
| `A_MaterialDocumentHeader` (GR) | Material movements are immutable for inventory integrity | Reverse via movement type 102 (creates negative MatDoc) |
| `A_Product` | Cloud Public locks Product master to MDG | Update via `A_ProductDescription` for description; A_ProductPlant for plant data |

## Reference files
- `references/mutable-fields-catalog.md` — full per-entity table of what works
- `references/known-traps.md` — the "204 looks like success but didn't change" cases
- `references/key-resolution.md` — how to construct keys for composite-key entities (PIR org-plant, BP address, etc.)
- `references/cancel-vs-update.md` — when to cancel-recreate vs PATCH
- `scripts/safe-update.mjs` — reference implementation with GET-PATCH-GET verify flow + dry-run mode
