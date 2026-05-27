---
name: arabic-nlp
description: Use this skill when selecting or applying Arabic NLP, tokenization, stemming, diacritization, morphological analysis, stopword, OCR, speech, or language-model tools including CAMeL Tools, Farasa, PyArabic, Tashaphyne, Qalsadi, and Arabic corpora.
---

# Arabic NLP

## When To Use

Use this skill for arabic-nlp work in Arab/MENA contexts, especially when the prompt includes: Arabic NLP, tokenization, stemming, diacritization, morphology, Farasa, CAMeL, PyArabic.

## When Not To Use

- Do not claim model accuracy without benchmark sources.
- Do not send private text to third-party APIs without approval.

## Required Inputs

- Country or market.
- Target vendor, if already selected.
- Desired flow: identify, prefer, separate, return.
- Sandbox vs production state.
- Whether live customer, payment, tax, identity, bank, or payroll data is involved.

## Default Workflow

1. Read `sources.yml` to see available vendors and confidence.
2. If a vendor is named, read only `vendors/<vendor-id>.md` for that vendor.
3. If choosing vendors, compare only vendors in this skill's registry: arabic-stopwords, camel-tools, farasa, pyarabic, qalsadi, tashaphyne.
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

- Check license and data handling before production use.
- Avoid sending sensitive Arabic text to external APIs by default.
- Benchmark on the target dialect and domain.
- Document tokenizer/stemmer limitations.

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
