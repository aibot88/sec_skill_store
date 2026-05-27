---
description: Assess payment network compliance — Nacha ACH rules, Visa/Mastercard requirements, state MTLs
---

# Payment Network Compliance Assessment

Assess payment network compliance for "$ARGUMENTS". Evaluate Nacha ACH Operating Rules, card network requirements, and state money transmitter licensing obligations.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **Nacha ACH Operating Rules:**
   - Assess authorization requirements (consumer and corporate, written/electronic/oral)
   - Evaluate ACH processing procedures (origination, file formatting, settlement timelines)
   - Review return handling procedures (return reason codes, timeframes, re-initiation rules)
   - Assess risk management requirements (exposure limits, monitoring, ACH audit)
   - Evaluate Nacha Third-Party Sender (TPS) registration and obligations if applicable
   - Review WEB debit authorization and fraud detection requirements
   - Assess compliance with Supplementary Fraud Detection Standards for WEB debits

3. **Visa Core Rules and Product Rules:**
   - Assess compliance with Visa Core Rules and Visa Product and Service Rules for card programs
   - Evaluate BIN sponsorship arrangement and registered agent/third-party agent status
   - Review cardholder agreement and disclosure requirements
   - Assess dispute resolution and chargeback management procedures
   - Evaluate Visa Operating Regulations for program-specific requirements (prepaid, credit, debit)
   - Review PCI DSS compliance requirements as mandated by Visa

4. **Mastercard Standards and Rules:**
   - Assess compliance with Mastercard Standards (formerly Mastercard Rules)
   - Evaluate registration requirements (Service Provider, Payment Facilitator, Staged Digital Wallet Operator)
   - Review Mastercard Identity Check and Strong Customer Authentication requirements
   - Assess chargeback and dispute management compliance
   - Evaluate Mastercard program-specific requirements for applicable products

5. **State money transmitter licensing:**
   - Determine which states require money transmitter licenses (MTL) based on business model
   - Assess applicability of exemptions (bank exemption, agent of the payee, licensed entity agent)
   - Review current licensing status across all required states
   - Evaluate NMLS (Nationwide Multistate Licensing System) registration and filings
   - Assess bonding, net worth, and permissible investment requirements per state
   - Review state examination and reporting obligations (call reports, audited financials)
   - Evaluate Uniform Money Services Act adoption in applicable states

6. **Federal registration requirements:**
   - Assess Money Services Business (MSB) registration with FinCEN
   - Evaluate biennial renewal and update filing compliance
   - Review state-level MSB registration requirements where applicable
   - Assess compliance with MSB-specific BSA/AML program requirements

7. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/payment-network.md` following the assessment template structure with:
    - **ACH Compliance** — Nacha rule adherence, authorization, returns, and risk management
    - **Visa Compliance** — Core Rules adherence, registration, and program requirements
    - **Mastercard Compliance** — Standards adherence, registration, and program requirements
    - **State Licensing** — MTL coverage map, exemption analysis, and gap identification
    - **Federal Registration** — FinCEN MSB status and BSA/AML program
    - **Evidence Inventory** — existing evidence and evidence gaps
    - **Remediation Priorities** — ranked list of gaps to address

## Output

The payment network assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/payment-network.md`. Present a summary to the user highlighting:
- ACH rule compliance status and key gaps
- Card network registration and compliance status
- State licensing coverage and gaps (number of states licensed vs. required)
- Top 3 gaps requiring remediation
