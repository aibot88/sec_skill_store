---
name: domain-setup
description: Configure your industry domain, country, and regulatory context — agents automatically adapt to your business
---

# Domain Setup

Configure the platform for your specific industry and region. This is optional — everything works with generic enterprise patterns if unconfigured.

## Quick Setup Examples

Tell me your industry and country, and I'll configure the agents. Examples:

- "We're a SEBI-regulated mutual fund AMC in India"
- "We're a HIPAA-compliant telehealth startup in the US"
- "We're a PCI-DSS payment processor in the UK"
- "We're an e-commerce platform in Singapore"
- "We're a SaaS company serving EU customers"

## What Gets Configured

Based on your input, I'll update the plugin configuration:

1. **Industry** — financial-services, healthcare, e-commerce, saas, edtech, logistics
2. **Country** — india, us, uk, eu, singapore, etc.
3. **Domain Details** — specific regulatory context (SEBI, HIPAA, PCI-DSS, GDPR, etc.)
4. **Currency** — ₹, $, £, €, etc.

## How Agents Adapt

| Agent | What changes |
|-------|-------------|
| **Product Manager** | Uses your regulatory framework for BRS, domain terminology for stories |
| **Devil's Advocate** | Challenges against your specific compliance requirements |
| **Forge Agents** | Currency formatting, audit patterns, entity naming, validation rules |
| **Reviewers** | Checks for your industry's compliance violations |
| **Test Forge** | Generates domain-specific test scenarios (e.g., KYC validation, HIPAA PHI handling) |

## Supported Presets

### Financial Services
- **India**: SEBI, RBI, AMFI, KYC/KRA, PAN, ₹ Indian format
- **US**: SEC, FINRA, SOX, AML/BSA, SSN, $ US format
- **UK/EU**: FCA, MiFID II, GDPR, KYC/AML, £/€

### Healthcare
- **US**: HIPAA, PHI encryption, consent management
- **EU**: GDPR, DISHA, patient data protection
- **India**: DISHA, Ayushman Bharat, ABDM

### E-Commerce
- PCI-DSS, consumer protection, multi-currency, tax calculations

### SaaS
- SOC 2, GDPR, multi-tenant, subscription billing

## To Configure

Just tell me about your business and I'll set it up. Or manually update the plugin config:

```
/plugin configure neuraforge-ai
```
