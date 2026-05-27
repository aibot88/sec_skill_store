---
name: salesforce-architecture
description: Use for org-level Salesforce architecture work — capacity planning, security/sharing review, integration patterns, multi-org strategy, tech-debt assessment.
---

# Salesforce architecture skill

## Capacity model

| Limit class | Soft signal at |
|---|---|
| Storage (data + file) | 70% utilisation |
| Active users | 80% of license |
| Custom objects | 80% of edition cap |
| API calls | sustained &gt; 60% of 24h limit |
| Async Apex slots | &gt; 50% concurrent |
| Workflow/Flow per object | 5+ active |
| Triggers per object | &gt; 1 (use a single dispatcher) |

When any soft signal is hit, surface it in the architecture review.

## Sharing & security

Security model layers (top-down):
1. Org-wide defaults (OWD)
2. Role hierarchy
3. Sharing rules (criteria/owner-based)
4. Manual sharing
5. Apex managed sharing
6. Restricted views via field-level security & profile/permset
7. Implicit sharing (parent ↔ child)

Review checklist:
- OWD set to most restrictive sustainable level (Private &gt; Public Read Only &gt; Public Read/Write)
- No "View All Data" / "Modify All Data" on profiles for non-admins
- Permission sets &gt; profile permissions (more granular, easier audit)
- Field-level security explicit on PII fields
- Apex `with sharing` / `without sharing` audited per class

## Integration patterns

| Pattern | When | How |
|---|---|---|
| Request-Reply (sync) | UI need-to-know now | Apex callout + Named Credential |
| Fire-and-forget | downstream system can be slow | Platform Events, Change Data Capture |
| Batch sync | volume, off-hours | Bulk API 2.0 from MuleSoft / fivetran / etc |
| Pub/sub | many subscribers, real-time | Pub/Sub API (gRPC) |
| Composite | multiple ops in one round-trip | Composite REST |

## Multi-org

- **Production + sandboxes:** standard. Use Source Tracking.
- **Multiple production orgs:** integrate via Salesforce Connect / API / iPaaS, not direct DB
- **Org strategy decisions:** dictated by data residency, license cost, M&amp;A history, business unit autonomy

## Tech-debt assessment heuristics

Score the org on:
- Apex coverage (target &gt; 85%)
- Active triggers per object (target ≤ 1, use dispatcher)
- Active Flows per object (target ≤ 3, consolidate)
- Custom fields per object (review at &gt; 200, dangerous at &gt; 500)
- API call volume vs limit
- Hardcoded ids in code/Flow (target = 0)
- Unmanaged metadata diff between orgs (target = 0 unintended)

## Deliverable shape

When asked for an architecture review, produce:

1. **One-page summary** — score + top 3 risks + top 3 wins
2. **Capacity table** — current vs limit, headroom
3. **Risk register** — risk, likelihood, impact, owner, mitigation
4. **Roadmap** — quick wins (≤ 1 sprint), structural fixes (1 quarter), strategic bets (1 year)

Use diagrams (Mermaid) for: data model, integration topology, environment topology.
