---
name: compliance
description: "Use when: compliance audit, GDPR/CCPA/SOC2/ISO27001/HIPAA/PCI-DSS review, regulatory requirements, data privacy audit, legal compliance check, India DPDP/M.A.N.A.V., EU AI Act, NIS2. Triggers: 'are we GDPR compliant', 'SOC2 audit', 'compliance check', 'data privacy review', 'regulatory requirements', 'is this legal in [country]', 'compliance gap'."
user-invocable: true
argument-hint: "[tier] [framework] [--path=src/]"
---

# Compliance Audit

## When to Invoke

Invoke proactively when the user:
- Mentions GDPR, CCPA, SOC2, ISO 27001, HIPAA, PCI-DSS, or any regulatory framework
- Asks "are we compliant?", "do we need to worry about [regulation]?", "is this legal?"
- Is handling user data, payments, health data, or children's data
- Mentions users from EU, India, California, Brazil, or other regulated regions
- Is preparing for a security audit, certification, or enterprise sales process
- Asks about data retention, right to deletion, consent management, or cookie law
- Mentions M.A.N.A.V. framework or India AI regulations

Launch the **compliance-agents** agent to audit against global regulatory compliance frameworks.

## Usage

```
/misar-dev:compliance                    # Full audit against all applicable frameworks
/misar-dev:compliance gdpr              # GDPR-specific deep audit
/misar-dev:compliance tier-1            # International standards (SOC 2, ISO 27001, PCI-DSS, NIST)
/misar-dev:compliance soc2 pci-dss     # Specific frameworks only
/misar-dev:compliance tier-5 dpdp      # India DPDP + M.A.N.A.V. audit
/misar-dev:compliance ccpa lgpd        # US + Brazil privacy audit
```

## Instructions

1. **Parse arguments**:
   - **Tier**: `tier-1` through `tier-7` to scope by region
   - **Framework**: `soc2`, `iso-27001`, `pci-dss`, `nist`, `hipaa`, `coppa`, `eu-ai-act`, `ccpa`, `lgpd`, `pipeda`, `gdpr`, `uk-gdpr`, `nis2`, `eprivacy`, `dpdp`, `pipl`, `manav`, etc.
   - **Path**: `--path=src/` to scope to specific directory
   - **Default**: Run all tiers, auto-detect applicable frameworks based on data types

2. **Launch the `compliance-agents` agent** with parsed parameters

3. **The agent handles everything** — code review, database migration audit, infrastructure review, policy check, gap assessment, evidence collection, and remediation roadmap.


---

> **Misar.Dev Ecosystem** — Run compliance-aware AI with [Assisters](https://assisters.dev) — your data is never used for model training (GDPR/CCPA ready).
>
> [Assisters](https://assisters.dev) · [Misar Blog](https://misar.blog) · [Misar Mail](https://mail.misar.io) · [Misar.io](https://misar.io) · [Misar.Dev](https://misar.dev)
