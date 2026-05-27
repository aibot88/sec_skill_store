---
description: Assess international privacy compliance — PIPEDA (Canada), PDPA (Singapore), APPI (Japan)
---

# International Privacy Assessment

Assess international privacy law compliance for "$ARGUMENTS". Evaluate requirements under PIPEDA (Canada), PDPA (Singapore), and APPI (Japan), and create a cross-jurisdiction compliance matrix.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **PIPEDA (Canada) assessment:**
   - Assess applicability (commercial activity, federal vs provincial jurisdiction)
   - Evaluate 10 fair information principles: accountability, identifying purposes, consent, limiting collection, limiting use/disclosure/retention, accuracy, safeguards, openness, individual access, challenging compliance
   - Assess consent requirements (express, implied, deemed, opt-out)
   - Review PIPEDA vs provincial privacy laws (Alberta PIPA, Quebec Law 25, BC PIPA)
   - Evaluate breach notification requirements (real risk of significant harm)
   - Assess cross-border transfer obligations
   - Review Privacy Commissioner complaint and investigation process readiness

3. **PDPA (Singapore) assessment:**
   - Assess applicability and exemptions
   - Evaluate consent obligations (notification, purpose limitation)
   - Assess Do Not Call (DNC) Registry compliance
   - Review data protection obligations: purpose limitation, notification, consent, access/correction, accuracy, protection, retention limitation, transfer limitation
   - Evaluate Data Protection Officer appointment
   - Assess data breach notification (notify PDPC within 3 days of assessment, notify affected individuals)
   - Review PDPC enforcement and financial penalty exposure

4. **APPI (Japan) assessment:**
   - Assess applicability under amended 2022 APPI requirements
   - Evaluate consent requirements for personal information handling
   - Assess consent for international transfers (country name disclosure, recipient's system)
   - Review pseudonymized and anonymized data processing rules
   - Evaluate individual rights (disclosure, correction, cessation of use, third-party provision record)
   - Assess Personal Information Protection Commission (PPC) compliance
   - Review data breach notification requirements (PPC notification and individual notification)
   - Evaluate academic, journalistic, and religious exemptions if applicable

5. **Cross-jurisdiction compliance matrix:**
   - Create matrix comparing: consent models, data subject rights, cross-border transfer rules, breach notification timelines, DPO requirements, enforcement mechanisms
   - Identify common baseline across all applicable jurisdictions
   - Highlight jurisdiction-specific requirements not covered by baseline
   - Score compliance per jurisdiction per requirement area

6. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/intl-privacy.md` following the assessment template structure with:
   - **Applicable Jurisdictions** — which laws apply with rationale
   - **PIPEDA Assessment** — fair information principles scoring (if applicable)
   - **PDPA Assessment** — obligation scoring per category (if applicable)
   - **APPI Assessment** — requirement scoring per category (if applicable)
   - **Cross-Jurisdiction Matrix** — comparative requirement and compliance view
   - **Common Baseline** — shared requirements and unified compliance approach
   - **Jurisdiction-Specific Gaps** — unique requirements per law
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The international privacy assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/intl-privacy.md`. Present a summary to the user highlighting:
- Applicable jurisdictions and overall compliance score per jurisdiction
- Cross-jurisdiction common baseline compliance
- Jurisdiction-specific requirements needing attention
- Top 3 gaps requiring remediation
