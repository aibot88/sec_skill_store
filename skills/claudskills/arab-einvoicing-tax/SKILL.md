---
name: arab-einvoicing-tax
description: Use this skill when working with Arab tax, e-invoicing, e-receipt, QR, clearance, reporting, and government tax APIs including Egypt ETA, Saudi ZATCA/Fatoora, Jordan JoFotara, UAE e-invoicing, Bahrain NBR, Oman Tax Authority, and provider integrations.
---

# Arab E-Invoicing and Tax

## When To Use

Use this skill for tax work in Arab/MENA contexts, especially when the prompt includes: e-invoice, e-receipt, tax, ZATCA, Fatoora, ETA, JoFotara, QR.

## When Not To Use

- Do not submit live tax documents.
- Do not provide legal advice or fabricate compliance rules.

## Required Inputs

- Country or market.
- Target vendor, if already selected.
- Desired flow: identify, read, separate, return.
- Sandbox vs production state.
- Whether live customer, payment, tax, identity, bank, or payroll data is involved.

## Default Workflow

1. Read `sources.yml` to see available vendors and confidence.
2. If a vendor is named, read only `vendors/<vendor-id>.md` for that vendor.
3. If choosing vendors, compare only vendors in this skill's registry: bahrain-national-bureau-for-revenue, egypt-eta-e-invoicing, egypt-eta-e-receipt, egyptian-tax-authority-einvoicing-ereceipt-sdk, jordan-jofotara, saudi-zatca-fatoora, uae-einvoicing-framework, uae-fta-e-invoicing, wafeq-zatca-api, zatca-fatoora-developer-portal.
4. Load `references/integration-checklist.md` only for implementation, review, or launch-readiness work.
5. Use `scripts/list-vendors.mjs` for a deterministic vendor list when needed.
6. Answer with source-backed facts, explicit unknowns, and validation steps.

## Decision Tree

- Named vendor: read that vendor file, then answer narrowly.
- Vendor selection: filter by country, docs access, maturity, and source quality before recommending.
- Implementation: include auth, sandbox, webhook/callback, retries, idempotency, logging, and error handling only where source-backed.
- Missing docs: say `Needs vendor access` or `Unknown from public docs`.

## Files To Read

- Routing and process: `SKILL.md`.
- Vendor facts: `vendors/*.md`.
- Source map: `sources.yml`.
- Implementation review: `references/integration-checklist.md`.
- Example response style: `examples/source-backed-answer.md`.

## Safety Rules

- Treat tax submissions and identity certificates as high-risk.
- Use official sandbox/test environments before production.
- Do not alter live invoices or tax data without explicit approval.
- Keep certificates, private keys, and OTPs out of the repo.

## Validation Checklist

- Vendor facts map back to `source_urls`.
- Unknowns are labeled instead of guessed.
- Sandbox and production are separated.
- Secrets are not printed or committed.
- High-risk live actions require explicit human approval.
- Evals in `evals/prompts.yml` still cover the changed workflow.

## Done Criteria

- The answer names the files read or source-backed references used.
- The implementation plan includes tests and rollback/verification steps.
- No unsupported regional, API, compliance, pricing, or endpoint claims are included.
