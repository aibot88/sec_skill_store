---
name: threat-modeling
description: "Produces structured threat models for software systems using STRIDE on data flow diagrams. Generates DFDs with trust boundaries, identifies threats per element, scores risks, and defines concrete mitigations. Outputs a complete threat model Markdown document through phased, interactive delivery. Use when threat modeling a system, analyzing security threats, identifying attack surfaces, performing STRIDE analysis, assessing security risks in architecture, creating a threat model document, or when the user mentions threat model, attack surface, trust boundaries, STRIDE, or security risk analysis."
category: System Architecture
---

# Threat Modeling

Produce a threat model for a user-described system using STRIDE-per-element on a data flow diagram.

## Workflow

Deliver in phases, presenting each for user review before proceeding. For "quick" or "draft" requests, produce the full document in one pass.

### Phase 1: Scope and system model

1. Gather from the user: system purpose, components, data flows, actors, deployment context.
2. Ask about:
   - Trust boundaries (where privilege, network, or ownership changes)
   - Data classifications (PII, secrets, financial, health, IP)
   - Threat actors (external attacker, insider, automated, nation-state)
3. Draw a **Level-1 DFD** in ASCII art showing processes (`⬭`), data stores (`▭▭`), external entities (`⬜`), data flows (`→`), and trust boundaries (`┄┄┄`).
4. List **assets** with Confidentiality / Integrity / Availability ratings.

Present the DFD and asset list. Ask the user to confirm or correct before proceeding.

Trust boundaries to check:

- Internet ↔ DMZ / edge
- App tier ↔ data tier
- Authenticated ↔ admin scope
- Your org ↔ vendor / 3rd-party API
- Tenant A ↔ Tenant B (multi-tenant)
- Host ↔ container / serverless
- LLM system prompt ↔ untrusted user or tool input

For DFD construction details, see [references/01-foundations-and-system-modeling.md](references/01-foundations-and-system-modeling.md).

### Phase 2: Identify threats

Apply **STRIDE-per-element**, starting at trust boundary crossings.

| STRIDE | Threat | Violates | Applies to |
|---|---|---|---|
| **S** Spoofing | Forged identity | Authenticity | Processes, external entities |
| **T** Tampering | Modified data | Integrity | Processes, data stores, data flows |
| **R** Repudiation | Deniable action | Non-repudiability | Processes, data stores\*, external entities |
| **I** Info disclosure | Data leak | Confidentiality | Processes, data stores, data flows |
| **D** Denial of service | Unavailability | Availability | Processes, data stores, data flows |
| **E** Elevation of privilege | Unauthorized access | Authorization | Processes |

\* Only if the store serves as an audit log.

For each element or flow crossing a trust boundary:

1. Walk S-T-R-I-D-E. Ask: "How could this happen here?"
2. Record each credible threat as: **asset, adversary, method, consequence**.
3. Consider chained threats — an I enabling an E enabling a T.

Present the threat list. Ask the user to confirm before proceeding.

**Example threat row** (data flow: User → Web Frontend over HTTPS):

| STRIDE | Element/Flow | Threat | Mitigation |
|---|---|---|---|
| S | User → Frontend | Attacker impersonates user with stolen session token | TLS 1.3, short-lived tokens, MFA |
| I | User → Frontend | Session cookie leaked via XSS | `HttpOnly`, `Secure`, `SameSite=Lax`, strict CSP |

Does this system include **AI, LLM, or agentic components**? If yes, read [references/05-ai-and-agentic-threats.md](references/05-ai-and-agentic-threats.md) and apply its additional threat categories.

For STRIDE session details and pitfalls, see [references/02-methodologies-and-stride.md](references/02-methodologies-and-stride.md).

### Phase 3: Score and prioritize

| Field | Values |
|---|---|
| Likelihood | Low (1) / Medium (2) / High (3) |
| Impact | Low (1) / Medium (2) / High (3) / Severe (4) |
| Exposure | Internal (1) / Authenticated (2) / Public (3) |
| **Score** | **Likelihood × Impact × Exposure** |
| Tier | 1–5 Low · 6–12 Medium · 13–24 High · 25+ Critical |

For each threat, assign disposition:

| Disposition | When |
|---|---|
| **Mitigate** | Reduce likelihood/impact with controls |
| **Transfer** | Shift to a party better positioned to bear it |
| **Accept** | Below tolerance; document owner + review date |
| **Eliminate** | Remove the feature or asset |

For alternative scoring schemes (CVSS, OWASP Risk Rating), see [references/03-risk-scoring-and-mitigations.md](references/03-risk-scoring-and-mitigations.md).

### Phase 4: Define mitigations

For each threat not accepted or transferred, define a mitigation that is **concrete** (specific control, not "improve security"), **testable**, **layered** (multiple controls for Critical/High), and **owned**.

| STRIDE | Canonical controls |
|---|---|
| S | MFA, mTLS, FIDO2, token binding, service identity (SPIFFE) |
| T | Input validation, parameterized queries, HMAC/signing, CSP |
| R | Append-only audit logs, signed actions, centralized SIEM |
| I | Encryption (transit + rest), least privilege, data minimization, output sanitization |
| D | Rate limiting, circuit breakers, autoscaling, quotas, WAF, CDN |
| E | Least privilege, authz on every request, separation of duties, sandboxing |

Present mitigations. Ask the user to confirm before producing the final document.

For mitigation catalogs and MITRE ATT&CK/D3FEND integration, see [references/03-risk-scoring-and-mitigations.md](references/03-risk-scoring-and-mitigations.md).

### Phase 5: Produce the threat model document

Assemble the final document using this template:

```markdown
# Threat Model: <System Name>

## Metadata
- **Owner(s):**
- **Last reviewed:** YYYY-MM-DD
- **Next review due:** YYYY-MM-DD

## System Description
<1–3 paragraphs: what the system does, who uses it.>

## Scope
- **In scope:**
- **Out of scope:**
- **Assumptions:**

## Assets
| Asset | Description | C | I | A | Notes |
|---|---|---|---|---|---|

## Actors
| Actor | Legitimate? | Motivation | Capability |
|---|---|---|---|

## Data Flow Diagram
<ASCII DFD with trust boundaries marked.>

## Trust Boundaries
| Boundary | Separates | Controls |
|---|---|---|

## Threats
| ID | STRIDE | Element/Flow | Threat | L | I | E | Score | Tier | Mitigation | Owner | Status |
|----|--------|--------------|--------|---|---|---|-------|------|-----------|-------|--------|

## Accepted Risks
| ID | Description | Rationale | Owner | Review Date |
|---|---|---|---|---|

## Open Questions
-

## Change Log
- YYYY-MM-DD: Initial threat model
```

## Edge cases

- **Very large system**: Focus the first pass on the highest-risk trust boundary crossings. Expand iteratively.
- **AI/LLM/agentic system**: Read [references/05-ai-and-agentic-threats.md](references/05-ai-and-agentic-threats.md) and add AI-specific threat categories.
- **Privacy-sensitive system (GDPR/CCPA/HIPAA)**: Apply LINDDUN categories alongside STRIDE. See [references/02-methodologies-and-stride.md](references/02-methodologies-and-stride.md).
- **User requests a different methodology**: Consult the decision matrix in [references/02-methodologies-and-stride.md](references/02-methodologies-and-stride.md).
- **User wants CI/CD integration**: See [references/04-devsecops-and-cloud-native.md](references/04-devsecops-and-cloud-native.md).
- **Cloud-native or microservices system**: See [references/04-devsecops-and-cloud-native.md](references/04-devsecops-and-cloud-native.md) for additional trust boundaries and threat classes.

## Reference material

Load on demand for deeper guidance:

- **Foundations & system modeling**: [references/01-foundations-and-system-modeling.md](references/01-foundations-and-system-modeling.md) — DFD construction, trust boundary patterns, asset inventory, the four-question framework, when to threat model
- **Methodologies & STRIDE**: [references/02-methodologies-and-stride.md](references/02-methodologies-and-stride.md) — methodology decision matrix, STRIDE-per-element details, PASTA, LINDDUN, attack trees, other methodologies
- **Risk scoring & mitigations**: [references/03-risk-scoring-and-mitigations.md](references/03-risk-scoring-and-mitigations.md) — DREAD, CVSS, OWASP risk rating, mitigation catalogs, MITRE ATT&CK/D3FEND integration
- **DevSecOps & cloud-native**: [references/04-devsecops-and-cloud-native.md](references/04-devsecops-and-cloud-native.md) — threat modeling as code (pytm), CI/CD integration, cloud-specific threats
- **AI & agentic threats**: [references/05-ai-and-agentic-threats.md](references/05-ai-and-agentic-threats.md) — MAESTRO framework, OWASP LLM Top 10, AI-specific mitigations
- **Worked example & templates**: [references/06-worked-example-and-templates.md](references/06-worked-example-and-templates.md) — CommentHub end-to-end example, elicitation checklists, validation checklist
- **Anti-patterns, tooling & maturity**: [references/07-anti-patterns-tooling-and-maturity.md](references/07-anti-patterns-tooling-and-maturity.md) — common pitfalls, tool landscape, program metrics
