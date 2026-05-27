---
description: Assess breach notification compliance — requirements by jurisdiction, SLA obligations
---

# Breach Notification Compliance Assessment

Assess breach notification compliance for "$ARGUMENTS". Map notification requirements by jurisdiction, evaluate contractual SLA obligations, and create a notification decision tree and template library.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **GDPR breach notification (Art 33-34):**
   - Assess notification to supervisory authority procedures (72-hour timeline from awareness)
   - Evaluate notification content requirements (nature of breach, categories/numbers affected, DPO contact, consequences, measures taken)
   - Review notification to data subjects procedures (without undue delay if high risk to rights and freedoms)
   - Assess breach severity assessment methodology (risk to individuals determination)
   - Evaluate cross-border notification procedures (lead supervisory authority identification)
   - Review breach record-keeping obligations (all breaches, not just notifiable ones)

3. **US state breach notification laws:**
   - Map notification requirements across all applicable states
   - Assess state-specific timelines (varies 30-90 days; some states have specific deadlines: Colorado 30 days, Florida 30 days, Washington 30 days)
   - Evaluate Attorney General notification thresholds per state (e.g., 500+ individuals in many states)
   - Review definition of "personal information" variations by state (some include login credentials, biometrics, health data)
   - Assess consumer reporting agency notification requirements (typically 1,000+ individuals)
   - Evaluate encryption and redaction safe harbors by state
   - Review content requirements for notification letters per state

4. **HIPAA breach notification (if applicable):**
   - Assess individual notification procedures (60 days from discovery, written notification)
   - Evaluate HHS/OCR notification requirements (60 days for 500+ affected, annual log for under 500)
   - Review media notification requirements (500+ individuals in a single state/jurisdiction)
   - Assess breach risk assessment methodology (4-factor test: nature of PHI, unauthorized person, actual access/use, mitigation extent)
   - Evaluate Business Associate notification obligations to Covered Entity (without unreasonable delay, no later than 60 days)

5. **PCI DSS breach notification:**
   - Assess card brand notification procedures and timelines
   - Evaluate acquiring bank notification requirements
   - Review forensic investigation requirements (PFI engagement)
   - Assess card reissuance cost liability and recovery procedures
   - Evaluate PCI Forensic Investigator engagement readiness

6. **NIS2 breach notification (if applicable):**
   - Assess early warning notification procedures (24 hours to CSIRT/competent authority)
   - Evaluate incident notification requirements (72 hours with initial assessment)
   - Review final report requirements (1 month with root cause analysis, mitigation measures, cross-border impact)
   - Assess significant incident determination criteria
   - Evaluate voluntary notification provisions for near-misses

7. **Contractual SLA obligations:**
   - Map customer notification timelines from DPAs and BAAs
   - Assess vendor/partner notification obligations (upstream and downstream)
   - Evaluate contractual penalties for notification delays
   - Review cooperation and information sharing obligations with customers
   - Assess cyber insurance notification requirements and timelines
   - Evaluate board and executive notification procedures (internal escalation)

8. **Notification decision tree:**
   - Assess existence and accuracy of breach classification criteria (severity levels)
   - Evaluate decision tree for determining notification obligations by breach type and jurisdiction
   - Review escalation procedures from detection to notification decision
   - Assess parallel notification workflow management (multiple jurisdictions simultaneously)
   - Evaluate legal hold and privilege considerations in breach investigation

9. **Template library and readiness:**
   - Assess existence of pre-drafted notification templates per jurisdiction
   - Evaluate template content compliance with jurisdiction-specific requirements
   - Review communication channel readiness (email, postal, website substitute notice, media)
   - Assess call center and response team readiness for individual notifications
   - Evaluate credit monitoring and identity protection service arrangements
   - Review regulatory filing templates and portal access (state AG portals, HHS portal)

10. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/breach-notification.md` following the assessment template structure with:
    - **GDPR Notification** — 72-hour process, content, and data subject notification readiness
    - **US State Laws** — jurisdiction map, timelines, AG thresholds, and safe harbors
    - **HIPAA Notification** — individual, HHS, and media notification procedures (if applicable)
    - **PCI DSS Notification** — card brand and forensic investigation readiness (if applicable)
    - **NIS2 Notification** — early warning, incident notification, and final report procedures (if applicable)
    - **Contractual SLAs** — customer and vendor notification timeline compliance
    - **Decision Tree** — breach classification, determination workflow, and escalation
    - **Template Library** — pre-drafted templates and communication readiness
    - **Evidence Inventory** — existing evidence and evidence gaps
    - **Remediation Priorities** — ranked list of gaps to address

## Output

The breach notification assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/breach-notification.md`. Present a summary to the user highlighting:
- Number of jurisdictions mapped and notification timeline compliance readiness
- Fastest required notification timeline and current capability to meet it
- Template and communication readiness score
- Top 3 gaps requiring remediation
