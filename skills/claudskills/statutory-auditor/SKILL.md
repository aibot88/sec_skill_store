---
name: statutory-auditor
metadata:
  last_updated: 2026-05-03
includes:
  - data/**
  - scripts/**
  - templates/**
  - company.example.json
description: |
  नेपाली नियमित लेखा परीक्षण (statutory audit under NCA Act 2053)। NFRS अनुपालन,
  ब्यालेन्स शीट / P&L सत्यापन, लेखा परीक्षण मत। Statutory audit under NCA Act 2053.
  NFRS compliance, balance sheet/P&L verification, audit opinion. Use for audit planning,
  NFRS compliance checks, or audit report generation.
---

# नियमित परीक्षक (Statutory Auditor) — Nepal

Performs statutory audit analysis under the Nepal Chartered Accountants Act 2053 (NCA Act) and Nepal Standards on Auditing (NSA).

## Prerequisites: company.json

At conversation start, check if `company.json` exists. If not, ask the user for:
- Company name, PAN, registration number
- Legal form and industry
- Audit period (fiscal year)
- Prior audit findings (if any)

Read `company.json` before proceeding.

## Audit Standards Framework

Nepal's audit framework:
- **NCA Act 2053** — Governs CA profession and audit requirements
- **NSA (Nepal Standards on Auditing)** — Equivalent to ISA, published by ICAN
- **NFRS (Nepal Financial Reporting Standards)** — Equivalent to IFRS
- **NAS (Nepal Accounting Standards)** — Older standards, being replaced by NFRS
- **NEP (Nepal Engagement Standards)** — Standards for audit engagements

Companies requiring statutory audit:
- All Private Limited and Public Limited companies
- Banks and financial institutions (NFRS/NRB guidelines)
- Insurance companies (as per Insurance Board)
- Government entities (as per Auditor General's office)
- Companies above NPR 2 crore annual turnover

## Audit Phases

### Phase 1: Engagement Planning

```
📋 लेखा परीक्षण योजना (AUDIT PLAN)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Company: [Name]
Period: FY [BS year] ([AD dates])
Auditor: [Name / Firm]

1. Understand the business and industry
2. Assess risk of material misstatement
3. Determine materiality level
4. Plan audit procedures
5. Assign audit team
```

Key planning questions:
- Materiality: Typically 1-2% of revenue or 5-10% of profit before tax
- Risk assessment: Industry risks, fraud risks, going concern
- Related parties: Identify and plan for disclosure verification
- Prior year adjustments: Any carried forward items

### Phase 2: Internal Control Evaluation

Assess:
- Authorization procedures for transactions
- Segregation of duties
- Physical safeguards for assets
- IT controls (if applicable)
- Documentation and record-keeping

### Phase 3: Substantive Testing

#### Balance Sheet Verification

| Item | Procedures |
|------|-----------|
| Cash and bank | Bank reconciliation, confirmation from banks, cash count |
| Receivables | Confirmation, aging analysis, subsequent collection check |
| Inventory | Physical verification, valuation (lower of cost/NRV per NFRS) |
| Fixed assets | Physical verification, title deeds, depreciation recalculation |
| Investments | Confirmation from brokers/custodians, fair value check |
| Payables | Supplier confirmation, subsequent payment check |
| Loans | Bank confirmation, terms verification, disclosure check |
| Capital | ROC filing verification, share certificate inspection |

#### P&L Verification

| Item | Procedures |
|------|-----------|
| Revenue | Sales register to bank deposits reconciliation, cut-off testing |
| COGS | Purchase verification, inventory movement, gross margin analysis |
| Employee costs | Salary register, PF/CIT contribution verification, TDS check |
| Operating expenses | Invoice verification, authorization, TDS compliance |
| Depreciation | Recalculate per NFRS, compare with tax rates |
| Tax expense | Income tax computation verification, advance tax check |

### Phase 4: NFRS Compliance Check

Key NFRS standards to verify:

| Standard | Topic | Key Check |
|----------|-------|-----------|
| NFRS 1 | Revenue Recognition | Revenue recognized when performance obligation satisfied |
| NFRS 2 | Inventories | Lower of cost and NRV, FIFO/weighted average |
| NFRS 3 | Property, Plant & Equipment | Cost model or revaluation model, useful life |
| NFRS 7 | Financial Instruments: Disclosures | Fair value, credit risk, liquidity |
| NFRS 9 | Financial Instruments | Classification, impairment (ECL model) |
| NFRS 15 | Leases | Right-of-use assets, lease liabilities |
| NFRS 16 | Income Taxes | Current and deferred tax |
| NFRS 10 | Consolidated Financial Statements | If parent company |
| NAS 1 | Presentation of Financial Statements | BS, P&L, Cash Flow, Notes |

### Phase 5: Going Concern Assessment

Evaluate:
- Financial performance trends (profitability, liquidity)
- Debt obligations and repayment capacity
- Operating cash flows
- Key customer/supplier dependencies
- Regulatory changes impacting business
- Management's plans for any adverse conditions

### Phase 6: Subsequent Events

Check for events between balance sheet date and audit report date:
- Adjusting events (conditions existing at BS date)
- Non-adjusting events (disclosure required if material)

### Phase 7: Audit Opinion

```
लेखा परीक्षण प्रतिवेदन (AUDIT REPORT)

[Company Name]
PAN: [number]

हामीले [Company] को आर्थिक विवरणहरूको लेखा परीक्षण गरेका छौं।

मत (Opinion):
[UNQUALIFIED / QUALIFIED / ADVERSE / DISCLAIMER]

आधार (Basis for Opinion):
[Explanation]

महत्त्वपूर्ण लेखा परीक्षण मुद्दाहरू (Key Audit Matters):
[If applicable]

निरन्तरताको आधार (Going Concern):
[Assessment]

उत्तरदायित्व (Responsibilities):
- प्रबन्धको उत्तरदायित्व: आर्थिक विवरण तयार गर्ने
- लेखा परीक्षको उत्तरदायित्व: मत दिने
```

### Opinion Types

| Type | When to Use |
|------|-------------|
| **Unqualified** (बिनासर्ते) | Financial statements give true and fair view |
| **Qualified** (सर्तसहित) | Except for specific matters, statements give true and fair view |
| **Adverse** (प्रतिकूल) | Financial statements do NOT give true and fair view |
| **Disclaimer** (अभिव्यक्तिको अभाव) | Unable to obtain sufficient audit evidence |

## Audit Report Structure

Use `templates/audit-report.md` as the base template. Fill with:
1. Title and addressee
2. Opinion paragraph
3. Basis for opinion
4. Key audit matters (if applicable)
5. Going concern (if applicable)
6. Responsibilities of management and auditor
7. Report on other legal requirements
8. Signature, date, and place

## Response Language

Reply in the language the user writes in. Default to English for technical terms.

## Disclaimer

This skill does not replace a statutory audit by a CA registered with ICAN. It is a preparation and analysis tool. Only a licensed CA can issue a statutory audit opinion. For actual audit engagements, consult a CA firm with valid ICAN registration and professional indemnity insurance.
