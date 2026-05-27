---
name: "ops-scale-engine"
description: "Startup operations and scaling engine covering process design (SOPs), metrics/KPI dashboards, financial operations, vendor management, supply chain, customer success operations, data governance, business continuity planning, quality management, build vs buy vs partner decisions, tech stack selection, infrastructure scaling, and operational maturity modeling. Includes India operations stack covering GST compliance, TDS, transfer pricing, import/export (DGFT), labour compliance, factory licensing, FSSAI/CDSCO/BIS certifications, and India-specific vendor/logistics ecosystem. Use when user mentions operations, ops, process, SOP, metrics, KPI, dashboard, vendor management, supply chain, logistics, customer success, data governance, quality, scaling, infrastructure, tech stack, build vs buy, operational efficiency, automation, workflow, India GST, TDS, import export, DGFT, factory license, FSSAI, or any operational scaling need."
license: MIT
metadata:
  version: 2.0.0
  author: TechKnowmad AI
  category: operations
  domain: startup-scaling
  updated: 2026-03-22
  frameworks: operations-management, process-design, scaling-playbooks
  data-sources: McKinsey Operations, BCG, Bain, First Round Capital, YC, Stripe Atlas, AWS Well-Architected, Google SRE, India DGFT, CBIC, MCA
---

# Ops Scale Engine

The startup operations scaling system. Frameworks for building repeatable, efficient operations from 5 to 5,000 people — processes, metrics, vendor management, and infrastructure that scale without breaking.

## Keywords

operations, ops, process, SOP, standard operating procedure, metrics, KPI, dashboard, OKR, vendor, vendor management, supply chain, logistics, fulfillment, customer success, CS ops, data governance, quality, QA, QMS, ISO, scaling, infrastructure, tech stack, build vs buy, partner, outsource, automation, workflow, efficiency, cost optimization, unit economics, margin, COGS, financial operations, FP&A, accounts payable, accounts receivable, treasury, procurement, IT operations, DevOps, SRE, incident management, on-call, monitoring, SLA, uptime, disaster recovery, BCP, business continuity, India, GST, TDS, transfer pricing, import export, DGFT, FSSAI, BIS, CDSCO, factory license, MSME, Udyam

---

## How to Use This Skill

| Mode | Trigger | What It Does |
|------|---------|--------------|
| **Assess** | "ops maturity", "how are our operations" | Maturity assessment, gap identification |
| **Design** | "build process for X", "SOP" | Process design, SOP creation, workflow mapping |
| **Measure** | "what metrics", "KPI dashboard" | Metrics framework, dashboard design |
| **Scale** | "we're growing fast", "breaking at scale" | Scaling playbooks, automation, hiring vs tooling |
| **Optimize** | "reduce costs", "improve efficiency" | Cost optimization, process improvement |
| **India** | "GST compliance", "India ops" | India-specific regulatory and operational compliance |

---

## 1. Operational Maturity Model

### Stage Assessment

| Level | Stage | Characteristics | Team Size | Priority |
|-------|-------|----------------|-----------|----------|
| **1: Chaos** | Pre-seed | No processes, founders do everything | 2-5 | Don't over-process. Ship fast. |
| **2: Reactive** | Seed | Ad-hoc processes, fire-fighting | 5-15 | Document critical paths only |
| **3: Defined** | Series A | Core SOPs exist, roles defined | 15-50 | Standardize customer-facing ops |
| **4: Managed** | Series B | Metrics-driven, predictable | 50-150 | Automation, efficiency focus |
| **5: Optimized** | Series C+ | Continuous improvement, data-driven | 150+ | Scale without proportional headcount |

### When to Add Process (Decision Framework)

```
Is this thing breaking or causing pain?
├── No → Don't add process yet (premature process kills speed)
├── Yes →
│   ├── Has it broken 3+ times?
│   │   ├── Yes → Write an SOP, assign an owner
│   │   └── No → Fix it, monitor, don't over-engineer
│   ├── Does it affect customers?
│   │   ├── Yes → Prioritize immediately
│   │   └── No → Queue for next ops sprint
│   └── Can it be automated?
│       ├── Yes → Automate first, document second
│       └── No → SOP + training + owner
```

---

## 2. Metrics & KPI Framework

### The Startup Metrics Stack

| Layer | Metrics | Cadence | Owner |
|-------|---------|---------|-------|
| **North Star** | The ONE metric that best captures value delivery | Weekly | CEO |
| **Health** | Revenue, burn, runway, headcount | Weekly | CEO/CFO |
| **Growth** | MRR, growth rate, CAC, LTV, NRR | Weekly | Growth/Sales |
| **Product** | DAU/MAU, activation, retention, NPS | Weekly | Product |
| **Engineering** | Velocity, uptime, deployment frequency, MTTR | Weekly | CTO |
| **Support** | CSAT, response time, resolution time, ticket volume | Daily | CS |
| **People** | Attrition, eNPS, offer acceptance, time-to-hire | Monthly | HR |
| **Finance** | Gross margin, burn multiple, cash position, AR/AP aging | Monthly | Finance |

### North Star Metric by Business Type

| Business Type | North Star | Why |
|--------------|-----------|-----|
| **B2B SaaS** | Weekly active teams/orgs | Captures adoption + retention |
| **Marketplace** | GMV or transactions/week | Captures both sides of marketplace |
| **Consumer subscription** | Weekly active subscribers | Captures engagement + retention |
| **E-commerce/D2C** | Revenue per customer per month | Captures purchase frequency + AOV |
| **Fintech** | Assets under management or txn volume | Captures trust + utility |
| **Enterprise** | # of enterprise contracts signed | Captures sales + product fit |
| **Developer tools** | API calls per week | Captures integration depth |

---

## 3. Build vs Buy vs Partner Decision Matrix

| Factor | Build | Buy (SaaS) | Partner/Outsource |
|--------|-------|-----------|-------------------|
| **When** | Core differentiator, unique to your business | Commodity function, well-served market | Non-core, specialized expertise needed |
| **Cost** | High upfront, low marginal | Low upfront, recurring | Medium, variable |
| **Time** | Months | Days-weeks | Weeks |
| **Control** | Full | Limited to vendor features | Negotiated |
| **Risk** | Technical debt, maintenance burden | Vendor lock-in, price increases | Quality variability, dependency |
| **Example** | Core algorithm, proprietary ML model | CRM, email, analytics | Payroll, legal, accounting |

### The 70/20/10 Rule for Startups
- **70% Buy** (SaaS tools for everything non-core)
- **20% Build** (only what creates competitive advantage)
- **10% Partner** (specialized expertise you can't hire for)

---

## 4. Financial Operations

### Startup Finance Stack by Stage

| Stage | Finance Tool | Accounting | FP&A |
|-------|-------------|-----------|------|
| **Pre-Seed** | Mercury/Brex bank | QuickBooks/Zoho Books | Spreadsheet |
| **Seed** | Mercury + Brex/Ramp (cards) | QuickBooks + bookkeeper | Spreadsheet + Runway |
| **Series A** | Multi-bank + treasury | NetSuite or Xero + fractional CFO | Mosaic/Jirav/Cube |
| **Series B+** | Full treasury management | NetSuite + controller + CFO | Enterprise FP&A tool |

### Cash Management Protocol

| Runway | Action | Treasury |
|--------|--------|---------|
| >18 months | Optimize returns | Split: operating account + high-yield savings + T-bills |
| 12-18 months | Preserve | Operating + high-yield savings, no risk |
| 6-12 months | Conserve | Single operating account, cut discretionary |
| <6 months | Survival | See crisis-war-room cash crisis protocol |

### Unit Economics Health Check

| Metric | Formula | Healthy | Concerning |
|--------|---------|---------|-----------|
| **Gross Margin** | (Revenue - COGS) / Revenue | >65% SaaS, >40% marketplace | <50% SaaS, <30% marketplace |
| **LTV:CAC** | Customer LTV / Customer Acquisition Cost | >3:1 | <2:1 |
| **CAC Payback** | CAC / Monthly Gross Profit per Customer | <12 months | >18 months |
| **Burn Multiple** | Net Burn / Net New ARR | <1.5x | >2.5x |
| **Magic Number** | Net New ARR / Prior Quarter S&M Spend | >0.75 | <0.5 |

---

## 5. Infrastructure & Tech Ops

### Uptime Targets by Stage

| Stage | Target Uptime | Acceptable Downtime/Month | Monitoring |
|-------|-------------|--------------------------|-----------|
| **Pre-Seed** | 95% | ~36 hours | Basic (UptimeRobot) |
| **Seed** | 99% | ~7 hours | APM (Datadog/New Relic) |
| **Series A** | 99.5% | ~3.6 hours | Full observability stack |
| **Series B** | 99.9% | ~43 minutes | SRE team, on-call rotation |
| **Series C+** | 99.95%+ | ~22 minutes | Multi-region, DR tested |

### Incident Management Protocol

| Severity | Response Time | Escalation | Communication |
|----------|-------------|-----------|---------------|
| **SEV1 (down)** | 5 minutes | On-call → CTO → CEO | Status page + customer email |
| **SEV2 (degraded)** | 15 minutes | On-call → engineering lead | Status page update |
| **SEV3 (minor)** | 1 hour | Assigned engineer | Internal only |
| **SEV4 (cosmetic)** | Next business day | Backlog | None |

---

## 6. Customer Success Operations

### CS Maturity by Stage

| Stage | CS Model | Ratio | Priority |
|-------|----------|-------|----------|
| **Seed** | Founder-led success | Founders know all customers | Learn, don't scale |
| **Series A** | First CSM hires | 1 CSM : 30-50 accounts | Onboarding + retention |
| **Series B** | Tiered CS | Enterprise: 1:15, Mid: 1:50, SMB: tech-touch | Expansion revenue |
| **Series C+** | Full CS org | + CS Ops, Onboarding, Technical | Net revenue retention |

### Health Score Framework

| Signal | Weight | Data Source | Green | Yellow | Red |
|--------|--------|-----------|-------|--------|-----|
| Product usage | 30% | Analytics | Daily active | Weekly | Monthly or declining |
| Support tickets | 20% | Helpdesk | Low, feature requests | Medium, bugs | High, complaints |
| NPS/CSAT | 15% | Surveys | >50 NPS | 20-50 | <20 |
| Contract value trend | 15% | CRM | Expanding | Flat | Contracting |
| Engagement | 10% | Meetings, responses | Proactive | Responsive | Unresponsive |
| Champion status | 10% | CSM intel | Strong champion | Champion at risk | Champion left |

---

## 7. India Operations Stack

### India Annual Compliance Calendar

| Month | Compliance | Authority | Penalty for Non-Compliance |
|-------|-----------|-----------|---------------------------|
| **Monthly** | GST returns (GSTR-1, GSTR-3B) | CBIC | 18% interest + INR 50/day late fee |
| **Monthly** | TDS deposit (7th of month) | Income Tax | 1.5%/month interest |
| **Quarterly** | TDS returns (31st post-quarter) | Income Tax | INR 200/day late fee |
| **Quarterly** | Advance tax installments | Income Tax | Interest under 234B/234C |
| **July 31** | Income tax return (non-audit) | Income Tax | INR 5,000-10,000 |
| **September 30** | AGM (Annual General Meeting) | MCA/ROC | INR 1 lakh fine |
| **October 31** | Income tax return (audit cases) | Income Tax | INR 5,000-10,000 |
| **October 30** | Annual return (MGT-7/MGT-7A) | MCA/ROC | INR 100/day late fee |
| **October 30** | Financial statements (AOC-4) | MCA/ROC | INR 100/day late fee |
| **Various** | PF/ESI returns | EPFO/ESIC | Heavy penalties + prosecution |
| **Various** | Professional tax | State government | State-specific penalties |

### India Sector-Specific Operational Licenses

| Sector | License/Registration | Authority | Timeline |
|--------|---------------------|-----------|----------|
| **Food/Beverage** | FSSAI license | FSSAI | 30-60 days |
| **Pharma/Health** | Drug license, CDSCO approval | CDSCO/State FDA | 3-12 months |
| **Manufacturing** | Factory license | State Factory Inspector | 30-60 days |
| **Import/Export** | IEC (Import Export Code) | DGFT | 3-7 days |
| **Fintech** | RBI license (NBFC/PPI/PA) | RBI | 6-24 months |
| **EdTech** | No specific license (state regulations emerging) | State govts | Varies |
| **Telecom** | DOT/TRAI license | DOT | 3-6 months |
| **Defence** | Industrial license | DPIIT | 3-12 months |
| **E-commerce** | DPIIT registration, FDI compliance | DPIIT/RBI | 1-2 weeks |
| **Real Estate** | RERA registration | State RERA | 30-60 days |

### India GST Essentials

| Threshold | Requirement |
|-----------|-------------|
| Turnover >INR 20L (services) / >INR 40L (goods) | GST registration mandatory |
| Interstate supply | GST registration mandatory (no threshold) |
| E-commerce seller | GST registration mandatory (no threshold) |
| Composition scheme | Turnover <INR 1.5Cr, simplified returns, no ITC |

---

## Reference Files

For detailed guides, load:
- [`reference/sop-templates.md`](reference/sop-templates.md) — SOP templates for common startup operations
- [`reference/india-ops-compliance.md`](reference/india-ops-compliance.md) — Detailed India regulatory compliance by sector

## Systems Thinking & Complexity Layer

### Cynefin Decision Framework

```
CLEAR: Cause-effect obvious → Sense-Categorize-Respond (fixing known bugs)
COMPLICATED: Experts can analyze → Sense-Analyze-Respond (tax strategy)
COMPLEX: Only visible in retrospect → Probe-Sense-Respond (PMF search)
CHAOTIC: No cause-effect → Act-Sense-Respond (active crisis)
CONFUSED: Don't know → Break into parts, classify each
CRITICAL: Most founders treat Complex as Complicated (analysis vs experimentation)
```

### Meadows' Leverage Points

```
WEAK: Parameters (pricing $5), buffers (runway), flows (pipeline)
MEDIUM: Feedback loops, information flows, rules/incentives
STRONG: Self-organization, goals, paradigms, transcending paradigms
RULE: Stop optimizing Level 12 (parameters). Change Level 3-5 for 100x impact.
```

### Antifragility for Operations

```
BARBELL: 90% boring/reliable/automated + 10% bold bets/experiments
VIA NEGATIVA: Kill bottom 20% processes, cancel empty meetings, fire toxic customers
HORMESIS: Monthly chaos exercises, quarterly reorgs, regular postmortems
```

### Homeostasis Protocol

```
Define 5-7 vital signs with homeostatic ranges:
  Burn rate ($X-$Y/mo), NPS (40-60), Deploy frequency (daily-weekly),
  Engagement (70-85%), Pipeline velocity (historical range)
Each has: sensor (dashboard alert), effector (response team), SLA
Review ranges quarterly — set points evolve with growth.
```

### Evolutionary Product Development

```
VARIATION: 3-5 parallel experiments monthly (each with kill criteria)
SELECTION: Ruthless. Kill experiments missing criteria. No extensions.
RETENTION: Document winners in "Product Genome" repo
MUTATION: Monthly "wild card" experiment to escape local optima
```

### Ensemble Financial Modeling (Climate Science)

Instead of single "base case" forecasts, run 50+ simulations with randomized assumptions. Report as probability distributions: "70% chance revenue $5-8M." Separate aleatory uncertainty (market randomness — build resilience) from epistemic uncertainty (knowledge gaps — do more research). More honest than pretending certainty.

### Mise en Place Protocol

Before any major initiative, complete preparation checklist: tools tested, content ready, roles assigned, workspace organized, contingencies planned. No execution begins until mise en place is complete.
