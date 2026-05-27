---
name: swiss-foia-builder
description: Use when researching, specifying, designing, or QAing a Swiss FOI / Öffentlichkeitsgesetz / LTrans / transparency-law request builder, including “MuckRock for Switzerland” or FragDenStaat-style tools. Covers federal BGÖ/LTrans and cantonal workflows, authority discovery, deadlines, fees, EDÖB/FDPIC mediation, privacy/source protection, benchmarking, and product spec output.
version: 1.0.0
author: Buried Signals
license: MIT
metadata:
  hermes:
    tags: [switzerland, foia, public-records, product-spec, journalism, transparency]
    related_skills: [obsidian, strategy, threat-modeling]
---

# Swiss FOIA Builder

## Overview

Use this skill to turn the Swiss public-access regime into a practical product spec or implementation plan for a modern FOI builder. The product target is **not** a legal explainer. It is a guided workflow that helps a journalist, citizen, NGO, lawyer, or researcher identify the right authority, draft a precise request, track deadlines, handle fees/denials, and escalate to mediation or appeal.

Known incumbent: `oeffentlichkeitsgesetz.ch` has a functional online request generator, with federal and cantonal flows, request preview/download, and user accounts for managing submitted requests. Treat it as a serious baseline, but not automatically as the product-quality answer meant by “nice FOIA builder.” Benchmark it against modern request-builder expectations: search-first discovery, guided request shaping, multilingual UX, authority database quality, deadline tracking, escalation templates, public/private archive choices, and source-protection defaults.

## When to Use

Load this skill when the task mentions any of:

- Swiss FOI, FOIA, BGÖ, Öffentlichkeitsgesetz, Öffentlichkeitsprinzip, access to documents, `Einsichtsgesuch`, `Zugangsgesuch`, `Akteneinsicht`, EDÖB mediation, cantonal transparency law.
- French/Italian Swiss terms: `LTrans`, `loi sur la transparence`, `demande d'accès`, `accès aux documents officiels`, `PFPDT`, `legge sulla trasparenza`, `accesso agli atti`, `principio di trasparenza`.
- Designing or researching a Swiss request builder, public-records request generator, MuckRock/FragDenStaat/WhatDoTheyKnow-style product, or document-access workflow.
- Drafting a spec file, PRD, MVP scope, data model, UX flow, or evaluation rubric for a Swiss transparency tool.
- Testing whether an existing Swiss FOI tool is “good enough.”

Do **not** use this skill for:

- Drafting a one-off Swiss FOI request only. Use the legal checks here if useful, but keep the output narrow.
- General legal advice. Provide product/research guidance and mark legal uncertainty; consult primary law or counsel for legal conclusions.
- Non-Swiss FOIA requests unless benchmarking comparable tools.

## Source Discipline

Swiss FOI details vary by authority, level of government, date, and canton. For every spec claim about law, deadlines, fees, jurisdiction, appeal route, or covered authority:

1. Fetch the current primary or specialist source with Firecrawl before relying on it.
2. Mark confidence:
   - `high` — primary law/official page/current specialist page fetched and inspected.
   - `medium` — specialist source or official summary, but not primary law or potentially stale.
   - `low` — secondary/inferred/unsourced.
3. Preserve source URLs and scrape dates in the spec.
4. Distinguish `functional incumbent exists` from `modern product-quality builder exists`.

Starter sources to verify before quoting:

| Need | Source | Use |
|---|---|---|
| Incumbent builder | `https://www.oeffentlichkeitsgesetz.ch/deutsch/online-antrag/` | Confirm existing federal/cantonal request generator. |
| Federal flow | `https://www.oeffentlichkeitsgesetz.ch/deutsch/online-antrag/eidgenoessischer-antrag/` | Inspect step model and authority selection. |
| Cantonal flow | `https://www.oeffentlichkeitsgesetz.ch/deutsch/online-antrag/kantonaler-antrag/` | Inspect canton selector and flow. |
| Swiss BGÖ FAQ | `https://www.oeffentlichkeitsgesetz.ch/deutsch/faq/` | Practical guidance, coverage, exceptions, mediation. |
| Canton pages | `https://www.oeffentlichkeitsgesetz.ch/deutsch/die-kantone/` | Canton-by-canton differences. |
| Federal commissioner | `https://www.edoeb.admin.ch/` | EDÖB/FDPIC mediation process, forms, recommendations. |
| Federal law, DE | `https://www.fedlex.admin.ch/eli/cc/2006/355/de` | BGÖ / Öffentlichkeitsgesetz primary text. |
| Federal ordinance, DE | `https://www.fedlex.admin.ch/eli/cc/2006/357/de` | VBGÖ implementing rules. |

For canton-specific legal claims, use Öffentlichkeitsgesetz.ch as a discovery/specialist source, then verify current law, deadlines, fees, and appeal routes against the canton’s official statute page or official administration guidance before marking confidence `high`.

Use Firecrawl CLI in this repo:

```bash
firecrawl scrape "https://www.oeffentlichkeitsgesetz.ch/deutsch/online-antrag/"
firecrawl search "site:edoeb.admin.ch BGÖ Schlichtungsantrag Öffentlichkeitsgesetz"
firecrawl search "Fedlex BGÖ Öffentlichkeitsprinzip Verwaltung SR 152.3"
```

## Skill-File / Spec-Research Best Practices

When the user asks for a “skill file” or “make it as good as possible,” apply these authoring rules:

- **Frontmatter triggers matter.** `name` and `description` are the always-loaded discovery layer. The description must name the real task triggers, not just the topic.
- **Progressive disclosure.** Keep `SKILL.md` self-contained enough to act, but avoid dumping raw law. Link/fetch source pages and split huge reference material only if needed.
- **Concrete workflows beat explanation.** Include exact research steps, evaluation rubrics, output templates, validation gates, and pitfalls.
- **Appropriate degrees of freedom.** Legal/source verification is low-freedom; UX/product synthesis is medium/high-freedom.
- **Test with real scenarios.** Validate YAML/frontmatter, check trigger phrasing, run a dry-run against at least one realistic prompt, and verify the file path under `kit/shared/<skill>/SKILL.md`.

These rules are grounded in Anthropic’s published Skill guidance: concise instructions, progressive disclosure, trigger-rich descriptions, and testing with real use cases.

## Core Workflow

### 1. Frame the product question

Before researching, write the threshold in one sentence:

```text
We are not asking whether any Swiss FOI request page exists; we are asking whether Switzerland has a modern, user-friendly FOI builder that reliably helps non-experts file, track, escalate, and optionally publish requests across federal and cantonal regimes.
```

Then classify the ask:

| Ask | Output |
|---|---|
| “Does this exist?” | Short market check with incumbent assessment. |
| “Set a goal” | Obsidian todo note with evidence, gap, and research/spec tasks. |
| “Make a spec” | Full PRD/spec file using template below. |
| “Build it” | Repo inspection, architecture plan, implementation tasks, tests. |
| “Create a skill” | `kit/shared/swiss-foia-builder/SKILL.md` or update this file. |

### 2. Map Swiss legal/workflow surface

At minimum, research and capture:

- **Federal BGÖ scope**: covered federal administration, excluded bodies, official-document definition, database/export treatment, exceptions, time limits, fees, consultation of third parties, mediation path.
- **Cantonal variation**: which cantons have public-access laws, which authorities are covered, whether municipalities/churches/public-task bodies are included, deadlines, fees, appeal/mediation model, language/legal naming.
- **Authority identification**: federal office hierarchy, decentralized federal bodies, commissions, cantonal departments, municipalities, public-law bodies, public-task private bodies.
- **User roles**: journalist/media, private citizen, NGO, researcher, lawyer, subject requesting own data, anonymous/source-sensitive user.
- **Submission channels**: email, web form, postal, download-only letter, account-based platform, published/public request.
- **Escalation**: reminder, clarification, fee objection, partial denial, third-party consultation, mediation with EDÖB or cantonal body, court/appeal path.

### 3. Benchmark incumbents

Compare at least these tools/classes:

| Tool | Jurisdiction | What to inspect |
|---|---|---|
| Öffentlichkeitsgesetz.ch | Switzerland | Federal/cantonal generation, authority coverage, account model, download/send flow, escalation support. |
| FragDenStaat | Germany/EU | Public request archive, authority database, campaigns, legal escalation, community workflow. |
| WhatDoTheyKnow | UK/global Alaveteli | Public-by-default requests, email proxying, authority contact quality, status tracking. |
| MuckRock | US | Professional workflow, request tracking, assignments, paid/legal services, document hosting. |
| FOIA.gov | US federal | Agency wizard, guided filing, official API-like authority structure. |
| Secret Canada FOI letter generator | Canada | Guided letter generation and request-shaping UX. |

Use this scoring rubric:

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Authority discovery | None | Static list | Search/filter | Smart routing + confidence |
| Request drafting | Blank text | Template | Guided prompts | AI/heuristic specificity checks |
| Swiss law coverage | Generic | Federal only | Federal + cantonal | Federal/cantonal/municipal with edge cases |
| Submission | Download only | Email link | Sends/tracks | Sends/tracks/escalates |
| Deadline tracking | None | Manual | Automatic reminders | Jurisdiction-aware timeline |
| Privacy/source protection | None | Account privacy | Private/public toggle | Redaction, aliases, sensitive-mode defaults |
| Escalation | None | Basic text | Mediation templates | Full denial/fee/appeal decision tree |
| Document/archive | None | User uploads | Public archive | Searchable archive + redaction/provenance |
| Multilingual | One language | Static translated pages | UI translated | Law/request text localized by jurisdiction |
| Trust/provenance | Unsourced | Some links | Source-backed guidance | Primary-law citations + confidence tags |

Interpretation:

- Average `<1.5`: gap is wide open.
- `1.5–2.3`: functional incumbent, weak product opportunity remains.
- `>2.3`: incumbent is strong; spec should target a differentiated wedge.

### 4. Define MVP wedge

A good Swiss FOIA builder MVP should not try to solve every canton perfectly on day one. Pick a wedge:

1. **Journalist-first federal + top cantons** — best for Buried Signals; focuses on repeatable newsroom workflows and source protection.
2. **Citizen self-service** — broad civic tool; prioritizes simple language and handholding.
3. **Public archive / campaign platform** — like FragDenStaat/Alaveteli; prioritizes public requests and community reuse.
4. **Professional request desk** — paid workflow for reporters/NGOs/lawyers; prioritizes case management and escalation.

Default recommendation for Buried Signals: **journalist-first federal + selected canton MVP**, with private-by-default drafts, export/send tracking, and escalation templates. Public archive can come later because source protection and legal review are non-trivial.

## Product Requirements Checklist

### Request builder

- [ ] Authority picker with jurisdiction confidence and “not sure” fallback.
- [ ] Authority/contact records store `source_checked_at`, `next_check_due_at`, `verification_method`, and confidence; stale records degrade after a defined interval such as 6–12 months depending on source reliability.
- [ ] Document specificity assistant: asks for date range, document type, office, sender/recipient, subject, existing report names, database/export shape.
- [ ] Legal basis insertion: federal/cantonal law name, no overclaiming.
- [ ] Fee handling: threshold warning, fee waiver/media/public-interest language where supported, ask-before-cost escalation.
- [ ] Delivery preference: electronic copy, inspection, machine-readable data/export when appropriate.
- [ ] Tone modes: neutral citizen, journalist/public interest, lawyerly.
- [ ] Multilingual output: German, French, Italian, English helper UI; request language follows authority/canton.
- [ ] Preview/export: copy, PDF/letter, email draft, platform-send.

### Tracking and escalation

- [ ] Deadline calculator per jurisdiction.
- [ ] Reminder templates before/after deadline.
- [ ] Clarification-response template.
- [ ] Fee objection / fee cap response.
- [ ] Partial access / redaction response.
- [ ] Denial analysis checklist mapped to exceptions.
- [ ] EDÖB/cantonal mediation template where applicable.
- [ ] Timeline with evidence: sent, received, call notes, attachments, authority replies.

### Privacy and source protection

- [ ] Private-by-default projects for journalists.
- [ ] No unnecessary PII; collect only what submission requires.
- [ ] Sensitive-mode that disables public archive, AI processing of request contents, and third-party telemetry.
- [ ] Redaction workflow before publication.
- [ ] Clear separation between user identity, public display name, and authority-facing sender details.
- [ ] Local export for source-sensitive investigations.
- [ ] Abuse controls for sending: rate limits, clear user accountability, no bulk filing without human review, audit logs, and explicit confirmation before authority-facing messages.

### Data model

Minimum entities:

```text
Authority(id, name, jurisdiction_level, canton, parent_id, contact_channels, languages, law_basis, coverage_notes, source_url, source_checked_at, confidence)
LawRegime(id, jurisdiction, name, scope, deadline_rules, fee_rules, escalation_route, source_url, confidence)
Request(id, user_id, authority_id, regime_id, title, body, language, status, privacy_mode, created_at, sent_at)
Event(id, request_id, type, occurred_at, actor, summary, attachment_ids)
Template(id, regime_id, language, scenario, body, source_url)
Document(id, request_id, filename, mime, storage_uri, redaction_status, provenance)
```

## Spec File Template

When asked to prepare a spec, output a markdown file with this structure:

```markdown
---
title: Swiss FOIA Builder Spec
status: draft
source:: <origin/task>
updated: YYYY-MM-DD
---

# Swiss FOIA Builder Spec

## 1. Executive summary
One paragraph: gap, user, wedge, MVP.

## 2. Evidence and incumbent assessment
| Claim | Evidence | Confidence |
|---|---|---|
| Öffentlichkeitsgesetz.ch has a federal/cantonal request generator | <URL + scrape date> | high |

## 3. User problem
Personas, jobs-to-be-done, current pain.

## 4. Product principles
Source-backed, privacy-first, jurisdiction-aware, request-specific, escalation-ready.

## 5. MVP scope
In / out / later.

## 6. Workflow
Discovery → authority selection → request drafting → preview/send/export → tracking → escalation → archive/redaction.

## 7. Legal/jurisdiction model
Federal and selected canton assumptions, unresolved research questions.

## 8. Authority database
Fields, source ingestion, update cadence, confidence scoring.

## 9. Request templates
Per-language/per-regime templates and variables.

## 10. UX wireflow
Step-by-step screens or CLI/API flow.

## 11. Data model
Entities and relationships.

## 12. Privacy/security/threat model
PII, source protection, public archive, retention, abuse risks.

## 13. Build plan
Milestones, tests, acceptance criteria.

Example acceptance criteria:
- Given a federal request, the builder identifies the likely authority, inserts the correct legal basis, and calculates the initial response deadline from a cited source.
- Given an uncertain authority, the builder offers a fallback forwarding/identification clause.
- Given a journalist-sensitive request, the default privacy mode does not publish request contents or send them to third-party AI services.

## 14. Open questions
Legal, product, data, operations.
```

## Request Drafting Heuristics

Good requests are narrow enough for compliance and broad enough not to miss the records. Apply this checklist:

- Name the document class: report, memo, email, meeting minutes, contract, dataset, correspondence, briefing, agenda entry.
- Bound the time range.
- Name offices/people/units only when helpful; avoid narrowing too much if unknown.
- Ask for metadata and attachments if relevant.
- Ask for machine-readable export for tabular/database records.
- Include “if this authority is not responsible, please forward or identify the responsible authority” where legally/practically appropriate.
- Ask for electronic delivery.
- For journalists, include public-interest/fee language but do not overstate legal entitlement.
- Avoid explaining motive unless strategically useful.

## Builder Intake Question Flow

Yes: a Swiss FOIA builder should behave like a guided interview, not a blank text box. The best product pattern is a **research gate**: start from a small user prompt, scrape/lookup what can be inferred, propose a request plan for review, then ask only the questions that remain genuinely blocking.

### Research gate pattern

1. **Tiny initial prompt** — accept a rough user goal such as “methane emissions methodology at BAFU” or “Zurich police drone procurement.” Do not require the user to know the authority, law, template, or exact document names.
2. **Automatic enrichment** — before asking follow-up questions, research likely authority, jurisdiction, law basis, contact route, language, candidate document classes, relevant programmes/reports, plausible date range, and fee/deadline rules. Use Firecrawl for web pages and keep source URLs + confidence.
3. **Propose a request plan** — show a short review card:
   - likely authority and confidence;
   - legal basis/jurisdiction;
   - proposed document classes;
   - proposed date range;
   - delivery/format request;
   - sensitivity/privacy mode;
   - unknowns/risks.
4. **Ask targeted questions** — ask only the 3–5 questions that would materially improve routing, specificity, deadline/fee handling, or source protection.
5. **Generate preview** — draft the request with explicit assumptions and source/confidence notes.
6. **Human gate before side effects** — require explicit confirmation before sending, publishing, or revealing identity/source-sensitive details.

Default intake questions, used only when not inferable:

1. **What are you trying to find?** Topic, event, programme, contract, decision, dataset, or investigation angle in plain language.
2. **Which authority or level is likely involved?** Federal, canton, municipality, public-law body, private body performing a public task, or “not sure.”
3. **What document types should be requested?** Reports, emails, minutes, contracts, datasets, correspondence, briefings, audits, permits, invoices, attachments, metadata.
4. **What date range?** Require a bounded period by default; if unknown, suggest a reasonable narrow range and state it as an assumption.
5. **Which language/jurisdiction?** German/French/Italian output and federal/cantonal legal basis should follow the authority unless the user requests otherwise.
6. **How sensitive is the request?** Public archive, private draft, source-sensitive/local-only mode, alias/display-name needs, and whether third-party AI processing is allowed.
7. **What delivery format?** Electronic copy, inspection, machine-readable export, PDF copies, original attachments, metadata.
8. **Fee posture?** Ask-before-cost cap, public-interest/media fee language, or willingness to pay up to a stated threshold.
9. **Escalation preference?** Reminder only, mediation-ready language, or full tracking/escalation workflow.
10. **Sender details.** Collect only what is required for authority-facing submission; keep product user identity, public display name, and authority-facing identity separate.

Question discipline:

- Default to **research first, ask second**.
- Do not ask all ten questions if the answer is already implied by context or can be safely researched.
- For a first draft, ask at most 3–5 high-value questions, then generate a provisional request with assumptions.
- If the user is unavailable, proceed with explicit assumptions and mark missing fields.
- For irreversible actions — actually sending the request, publishing it, or revealing identity/source-sensitive details — stop and require explicit confirmation.
- Always show the generated request preview before sending.

## PDF / Letter Export Formatting


Supporting file included in this marketplace skill:

- `scripts/render_foia_pdf.py` — dependency-free A4 PDF renderer for generated request letters. Use it or adapt it when `pandoc`, `weasyprint`, or a browser renderer is unavailable; it avoids the bad `cupsfilter` mid-word wrapping failure mode.

For generated FOIA request PDFs, do **not** pipe raw Markdown or long unwrapped text through `cupsfilter`; it can justify strangely and break words mid-word. Prefer a controlled letter renderer:

- Use A4 page size, 20–25 mm margins, 10.5–11 pt readable body text, 14–16 pt title.
- Left-align text; do not fully justify.
- Word-wrap paragraphs before rendering with `break_long_words=False` and `break_on_hyphens=False`.
- Separate title, subject, salutation, numbered request items, closing, and signature placeholders.
- Keep dry-run verification notes visually separate and clearly marked “not part of request.”
- Verify the generated file with `file <pdf>` and a PDF-header check before sharing.

If no proper HTML/PDF renderer is installed, generate a simple PDF directly or pre-wrap a text export before `cupsfilter`; never send the raw long-line PDF as the polished artifact.

## Testing Protocol

When creating or updating this skill, test it before reporting done:

1. **Filesystem check**
   ```bash
   test -f kit/shared/swiss-foia-builder/SKILL.md
   ```
2. **Frontmatter validation**
   ```bash
   python3 - <<'PY'
from pathlib import Path
import re, yaml
p = Path('kit/shared/swiss-foia-builder/SKILL.md')
content = p.read_text()
assert content.startswith('---')
end = content.find('\n---\n', 3)
assert end != -1
fm = yaml.safe_load(content[3:end])
assert fm['name'] == 'swiss-foia-builder'
assert 0 < len(fm['description']) <= 1024
assert re.fullmatch(r'[a-z0-9-]{1,64}', fm['name'])
assert content[end+5:].strip()
assert len(content) <= 100000
print('valid')
PY
   ```
3. **Trigger dry-run** — verify the description clearly matches prompts like:
   - “Research a Swiss FOIA builder and draft a spec.”
   - “Make a MuckRock for Switzerland.”
   - “Compare Öffentlichkeitsgesetz.ch with FragDenStaat.”
4. **Content dry-run** — use the workflow to produce a one-page mini spec from the incumbent source set; confirm the output includes evidence/confidence and does not mistake the incumbent for proof the product gap is closed.
5. **Request-generation dry-run** — generate one realistic Swiss federal or cantonal access request without sending it. Verify the output has: correct legal basis, sufficiently specific document description, date range, electronic delivery, fee-warning language, authority-forwarding fallback, redaction/partial-access language, media/public-interest language when relevant, and source/confidence notes for legal claims.
6. **Repo hygiene** — run `git status --short`; do not overwrite unrelated dirty files.

## Common Pitfalls

1. **Calling the Swiss system “FOIA” without translation.** FOIA is shorthand for Tom; Swiss sources use BGÖ, Öffentlichkeitsgesetz, Öffentlichkeitsprinzip, `Zugangsgesuch`, `Einsichtsgesuch`, access to official documents.

2. **Treating existence as quality.** A download-oriented request generator may exist and still leave room for a modern builder.

3. **Flattening cantons.** Cantonal rules differ; do not promise uniform deadlines, fees, or escalation.

4. **Over-lawyering the UX.** Users need a request that works, not a treatise. Keep legal nuance in tooltips/source links and decision logic.

5. **Ignoring municipalities/public-task bodies.** Many valuable local records are outside federal administration; authority coverage is product-critical.

6. **Public-by-default danger.** Public archives are powerful but can expose sources, strategies, personal data, and unpublished investigation leads.

7. **Skipping authority contact verification.** Bad addresses silently kill request workflows. Store `source_checked_at` and confidence.

8. **No escalation path.** A builder without reminders, fee/denial responses, and mediation templates is just a prettier letter generator.

9. **Unsourced legal claims.** Every deadline, exception, fee rule, and appeal route needs a current source or a `confidence: low` tag.

## Verification Checklist for Final Outputs

- [ ] Incumbent assessment distinguishes functionality from product quality.
- [ ] Federal and cantonal scope are separated.
- [ ] Every legal/process claim has source + confidence.
- [ ] MVP wedge is explicit.
- [ ] Authority database requirements are specified.
- [ ] Request, tracking, escalation, privacy, and archive flows are covered.
- [ ] Spec includes acceptance criteria and tests.
- [ ] Risks include legal accuracy, PII/source protection, stale authority data, and public-archive harms.
