---
name: speckit-threat-model
description: Generate a threat model from spec.md using STRIDE methodology. Use when you need to identify security threats, attack surfaces, and mitigations for a feature before implementation. Triggers on "threat model", "security analysis", "attack surface", "STRIDE analysis".
effort: high
---

# Threat Model Generation

Generate a structured threat model from a feature specification using STRIDE methodology.

## Prerequisites

Before starting, locate:
1. The feature spec (`.speckit/features/<feature>/spec.md` or provided by user)
2. The project constitution (`.speckit/constitution.md`) for security constraints
3. The project stack (check `package.json`, `CLAUDE.md`)

## Process

### Step 1: Identify Assets and Trust Boundaries

Read the spec and identify:
- **Data assets**: What data does this feature handle? (PII, credentials, financial, content)
- **Entry points**: API routes, form inputs, webhooks, file uploads
- **Trust boundaries**: Client/server, authenticated/anonymous, admin/user, internal/external services
- **Dependencies**: Third-party services, databases, auth providers

### Step 2: STRIDE Analysis

For each entry point, evaluate all 6 STRIDE categories:

| Category | Question |
|----------|----------|
| **S**poofing | Can an attacker impersonate a legitimate user or service? |
| **T**ampering | Can data be modified in transit or at rest without detection? |
| **R**epudiation | Can a user deny performing an action without accountability? |
| **I**nformation Disclosure | Can sensitive data leak through responses, logs, or errors? |
| **D**enial of Service | Can the feature be overwhelmed or made unavailable? |
| **E**levation of Privilege | Can a user gain access beyond their authorization level? |

### Step 3: Risk Assessment

For each identified threat, assess:
- **Likelihood**: Low / Medium / High
- **Impact**: Low / Medium / High / Critical
- **Risk Level**: Likelihood x Impact matrix
- **Existing mitigations**: What the current stack already handles (e.g., Supabase RLS, Next.js CSRF)

### Step 4: Mitigation Recommendations

For each Medium+ risk threat, propose:
- Specific code-level mitigation (Zod validation, RLS policy, rate limiting, etc.)
- Which story/task should implement it
- Whether it blocks the feature or can be addressed post-MVP

### Step 5: Generate Report

Output to `docs/security/<feature>-threat-model.md`:

```markdown
# Threat Model: <Feature Name>

**Date**: YYYY-MM-DD
**Spec**: .speckit/features/<feature>/spec.md
**Author**: Claude (automated)

## 1. Overview

Brief description of the feature and its security context.

## 2. Assets

| Asset | Type | Sensitivity |
|-------|------|------------|
| ... | PII / Financial / Content / System | High / Medium / Low |

## 3. Trust Boundaries

Diagram (text-based):
```
[Browser] --HTTPS--> [Next.js API] --SQL--> [Database]
              |                        |
         Trust Boundary 1        Trust Boundary 2
```

## 4. Threats (STRIDE)

### T-001: <Threat Name>
- **Category**: Spoofing / Tampering / ...
- **Entry Point**: POST /api/xxx
- **Description**: ...
- **Likelihood**: Medium
- **Impact**: High
- **Risk**: HIGH
- **Existing Mitigation**: Supabase RLS on table X
- **Recommended Mitigation**: Add Zod validation on input field Y
- **Priority**: Must-fix before MVP / Post-MVP acceptable

### T-002: ...

## 5. Risk Matrix

|          | Low Impact | Medium Impact | High Impact | Critical Impact |
|----------|-----------|--------------|-------------|----------------|
| **High** | Medium    | High         | Critical    | Critical       |
| **Medium** | Low     | Medium       | High        | Critical       |
| **Low**  | Info      | Low          | Medium      | High           |

## 6. Summary

- Total threats identified: N
- Critical: N | High: N | Medium: N | Low: N
- Must-fix before MVP: N
- Status: PASS / WARN / FAIL
```

## Status Levels

- **PASS**: No Critical or High threats without mitigation
- **WARN**: High threats exist but have proposed mitigations
- **FAIL**: Critical threats without clear mitigation path

## Common Patterns by Stack

### Supabase + Stripe
- Check RLS policies cover all tables touched by the feature
- Verify webhook signature validation for Stripe events
- Ensure `service_role` key is never exposed client-side
- Check that Supabase auth tokens are validated server-side

### Next.js (both starters)
- Server Actions: validate all inputs with Zod
- API routes: check authentication before processing
- Middleware: verify redirect targets are same-origin
- Environment variables: ensure no `NEXT_PUBLIC_` prefix on secrets
