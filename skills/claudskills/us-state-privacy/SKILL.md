---
description: Assess US state privacy law compliance — VCDPA, CPA, CTDPA, UCPA, and emerging laws
---

# US State Privacy Law Assessment

Assess US state privacy law compliance for "$ARGUMENTS". Map applicable state laws, compare requirements, and create a cross-state compliance matrix.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **Applicable state law mapping:**
   - Determine which state laws apply based on organizational operations and customer base
   - Assess applicability for established laws: Virginia VCDPA, Colorado CPA, Connecticut CTDPA, Utah UCPA
   - Assess applicability for newer laws: Texas TDPSA, Oregon OCPA, Montana MCDPA, Iowa ICDPA, Delaware DPDPA, New Jersey NJDPA, New Hampshire, Kentucky, Nebraska, Maryland, Minnesota, and others
   - Document applicability thresholds per state (consumer count, revenue, data processing volume)

3. **Cross-state requirement comparison:**
   - Compare consumer rights across states (access, delete, correct, portability, opt-out)
   - Identify opt-out vs opt-in consent models per state
   - Compare right to cure periods (30 days, 60 days, or none)
   - Map enforcement mechanisms (AG only vs private right of action)
   - Assess universal opt-out signal requirements per state

4. **Common baseline identification:**
   - Identify the most restrictive state as the compliance floor
   - Map common requirements shared across all applicable states
   - Highlight unique or unusual state-specific requirements
   - Assess whether a single compliance program can satisfy all states

5. **Unique state requirements:**
   - Assess Data Protection Impact Assessment (DPIA) requirements by state
   - Evaluate profiling and automated decision-making rights per state
   - Review sensitive data definitions and consent requirements (varies by state)
   - Assess children's data protections by state
   - Evaluate data broker registration requirements where applicable

6. **State-by-state compliance matrix:**
   - Create matrix: state vs requirement category (rights, notice, consent, DPIAs, enforcement)
   - Score compliance per state per category
   - Identify states with highest compliance gap
   - Prioritize remediation by enforcement risk and gap severity

7. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/us-state-privacy.md` following the assessment template structure with:
   - **Applicable States** — list of states with applicability rationale
   - **Cross-State Matrix** — requirements comparison across all applicable states
   - **Common Baseline** — most restrictive floor requirements
   - **Unique Requirements** — state-specific obligations not covered by baseline
   - **Per-State Compliance Score** — readiness per state
   - **Gap Analysis** — areas where current practices fall short per state
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The US state privacy law assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/us-state-privacy.md`. Present a summary to the user highlighting:
- Number of applicable state laws and highest-risk states
- Common baseline compliance score
- States with the largest compliance gaps
- Top 3 gaps requiring remediation
