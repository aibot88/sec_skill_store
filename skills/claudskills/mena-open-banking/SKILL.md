---
name: mena-open-banking
description: Use this skill when working with MENA open banking, open finance, account information, payments initiation, consent, aggregator, and regulatory API references such as Lean, Tarabut, Dapi, Salt Edge, UAE Open Finance, Saudi Open Banking, and Bahrain open banking.
---

# MENA Open Banking

## When To Use

Use this skill for open-banking work in Arab/MENA contexts, especially when the prompt includes: open banking, open finance, consent, AIS, PIS, Lean, Tarabut, Dapi.

## When Not To Use

- Do not initiate bank payments or access real account data.
- Do not provide legal/regulatory advice.

## Required Inputs

- Country or market.
- Target vendor, if already selected.
- Desired flow: classify, read, separate, return.
- Sandbox vs production state.
- Whether live customer, payment, tax, identity, bank, or payroll data is involved.

## Default Workflow

1. Read `sources.yml` to see available vendors and confidence.
2. If a vendor is named, read only `vendors/<vendor-id>.md` for that vendor.
3. If choosing vendors, compare only vendors in this skill's registry: bahrain-open-banking, dapi, lean-technologies, salt-edge, saudi-open-banking-framework, tarabut, uae-open-finance-api-hub.
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

- Treat bank data and payment initiation as high-risk.
- Use sandbox consent and test institutions first.
- Require explicit approval before live bank-data access or payment-initiation work.
- Do not store bank credentials.
- Document consent lifecycle, revocation, and data minimization.

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
