---
name: wealth-management-rfp
description: >-
  Use this skill whenever writing, reviewing, or responding to an RFP that
  involves wealth management, asset management, private banking, financial
  advisory, portfolio management, robo-advisory, trading platforms, financial
  planning, investment management, or related domains. Triggers include any
  mention of wealth management, HNW/UHNW clients, portfolio rebalancing,
  financial planning, advisor workbench, client onboarding/KYC/AML,
  SEC/FINRA/MiFID compliance, trading systems, performance reporting,
  model portfolios, custody, or investment operations. Covers full domain
  knowledge (regulations, processes, personas, data models) plus Aiden AI /
  AIDAP solution patterns (AI advisors, risk engines, portfolio optimization
  agents, compliance bots, client 360). Combine with the base rfp-response
  skill for full proposal structure and with the aiden-ai-rfp skill for
  deep platform details. Use this skill BEFORE writing any wealth management
  solution architecture, module design, or technical narrative.
license: "Internal use — Confidential"
---

# Wealth Management RFP Response Skill

This skill provides **deep domain expertise and Aiden AI solution patterns** for crafting winning RFP responses in the **wealth management, asset management, and private banking** space.

> **Always combine with:**
> - `rfp-response` SKILL.md — overall proposal structure, section templates, pricing format
> - `aiden-ai-rfp` SKILL.md — deep Aiden AI Builder / AIDAP platform details
> - `pricing-calculator` SKILL.md — effort estimation and rate cards

---

## Part 1: Wealth Management Domain Knowledge

### 1.1 Industry Segments & Client Tiers

| Segment | AUM Range | Key Characteristics | Service Model |
|---------|-----------|-------------------|---------------|
| **Mass Affluent** | $250K–$1M | Goal-based planning, digital-first, fee-sensitive | Robo + hybrid advisory |
| **High Net Worth (HNW)** | $1M–$10M | Tax optimization, estate planning, dedicated advisor | Dedicated RM + digital tools |
| **Ultra-HNW (UHNW)** | $10M–$100M+ | Multi-entity, complex structures, family office needs | Private banker + specialist team |
| **Institutional** | $100M+ | Pension, endowment, sovereign wealth, insurance GA | Institutional sales + portfolio mgmt |
| **Family Office** | Varies | Multi-generational, philanthropy, consolidated reporting | Dedicated team, bespoke platform |

**Always ask in RFP analysis:** Which client tier(s) does this RFP target? The answer drives the entire solution design — from UX complexity to compliance depth to AI personalization level.

### 1.2 Core Business Processes

#### 1.2.1 Client Lifecycle

```
Prospect → Onboarding → KYC/AML/Suitability → Account Opening →
Financial Planning → Investment Proposal → Execution → Ongoing Advisory →
Rebalancing → Reporting → Review → Offboarding
```

**Key process details for proposals:**

- **Client Onboarding & KYC/AML**: Identity verification (IDV), beneficial ownership, PEP/sanctions screening, risk profiling, suitability assessment, document collection (W-9, W-8BEN, trust docs). Typical pain point: 15–45 day onboarding cycle → propose AI-driven reduction to 3–5 days.
- **Suitability & Risk Profiling**: Investment questionnaire, risk tolerance scoring (conservative/moderate/aggressive/speculative), time horizon, liquidity needs, concentration limits, ESG preferences. Regulatory requirement — must document and review periodically.
- **Financial Planning**: Goal-based planning (retirement, education, estate), Monte Carlo simulations, cash flow projections, tax-loss harvesting modeling, Social Security optimization, insurance gap analysis.
- **Investment Proposal Generation**: Model portfolio selection, custom portfolio construction, proposal document generation with projections, fee disclosure, risk metrics (Sharpe, Sortino, max drawdown, VaR).
- **Trading & Execution**: Order management, block trading, allocation, best execution (Reg NMS), trade confirmation, settlement (T+1).
- **Portfolio Rebalancing**: Drift monitoring, threshold-based triggers, tax-aware rebalancing, cash flow-aware rebalancing, multi-account household rebalancing.
- **Performance Reporting**: TWR/MWR calculations, benchmark comparison, attribution analysis (Brinson), composite reporting (GIPS), client-facing statements.
- **Billing & Fee Management**: AUM-based fees, tiered fee schedules, performance fees (hedge fund), fee-in-lieu, household billing, fee splits (advisor/firm).

#### 1.2.2 Advisor Workflow

```
Morning Book Review → Research & Market Intel → Client Meetings →
Financial Plan Updates → Trade Execution → Compliance Review →
CRM Updates → End-of-Day Reconciliation
```

**Advisor pain points to address in proposals:**
- Toggling between 8–12 systems daily (CRM, portfolio mgmt, planning, compliance, trading, reporting)
- Manual data entry and re-keying across systems
- Compliance documentation burden
- Slow client onboarding reducing time-to-revenue
- Inability to scale personalized advice beyond ~150 clients per advisor

### 1.3 Regulatory & Compliance Landscape

#### U.S. Regulations

| Regulation | Authority | Key Requirements | Solution Implication |
|-----------|-----------|-----------------|---------------------|
| **Reg BI (Best Interest)** | SEC | Document best interest basis for every recommendation | AI-driven suitability engine with audit trail |
| **Form CRS** | SEC | Client Relationship Summary delivery | Automated delivery & acknowledgment tracking |
| **ADV Part 2A/2B** | SEC | Firm brochure & brochure supplement | Document management & version control |
| **AML/BSA** | FinCEN | Customer identification, suspicious activity reporting | Automated SAR filing, transaction monitoring |
| **Reg SHO** | SEC | Short sale regulation | Pre-trade compliance checks |
| **ERISA** | DOL | Fiduciary duty for retirement accounts | Plan-level suitability & fee benchmarking |
| **Reg S-P** | SEC | Privacy of consumer financial information | Data encryption, access controls, privacy notices |
| **Rule 17a-4** | SEC | Electronic records retention | Immutable audit logs, 6-year retention |
| **FINRA Rule 2111** | FINRA | Suitability obligations | Automated suitability checks pre-trade |
| **FINRA Rule 3110** | FINRA | Supervision requirements | Supervisory workflow, exception-based review |

#### Global Regulations (Reference When RFP Has International Scope)

| Regulation | Jurisdiction | Key Impact |
|-----------|-------------|-----------|
| **MiFID II** | EU | Best execution, suitability, cost disclosure, research unbundling |
| **GDPR** | EU | Data privacy, right to erasure, consent management |
| **FCA COBS** | UK | Conduct of business, treating customers fairly |
| **FATCA** | US (global) | Foreign account tax compliance, W-8BEN collection |
| **CRS** | OECD | Common reporting standard, automatic exchange of info |
| **PDPA / PIPA** | APAC | Data protection across Asian jurisdictions |

**Always include in proposals:**
- Compliance is not a bolt-on — it must be embedded in every workflow
- Audit trail for every client interaction, recommendation, and trade
- Configurable rule engine for jurisdiction-specific requirements
- Regulatory change management process

### 1.4 Key Data Entities & Integrations

#### Core Data Model

```
Client/Household
  ├── Accounts (individual, joint, trust, IRA, 401k, custodial)
  │     ├── Holdings (positions, lots, cost basis)
  │     ├── Transactions (trades, dividends, transfers, fees)
  │     └── Performance (TWR, MWR, benchmarks)
  ├── Financial Plan (goals, projections, scenarios)
  ├── Risk Profile (score, questionnaire, suitability)
  ├── Documents (statements, tax forms, agreements)
  └── Interactions (meetings, calls, emails, tasks)

Securities / Instruments
  ├── Equities, Fixed Income, Mutual Funds, ETFs
  ├── Alternatives (PE, hedge funds, real assets)
  ├── Options, Structured Products
  └── Market Data (prices, benchmarks, indices)

Model Portfolios / Strategies
  ├── Asset Allocation Targets
  ├── Security Selection Rules
  ├── Rebalancing Parameters
  └── Restriction / ESG Overlays
```

#### Common Integration Points

| System | Examples | Integration Pattern |
|--------|----------|-------------------|
| **Custodian** | Pershing, Schwab, Fidelity, DTCC | FIX/SWIFT, file-based (DTCC), API |
| **Market Data** | Bloomberg, Refinitiv, FactSet, Morningstar | Real-time feeds, batch EOD |
| **CRM** | Salesforce Financial Services Cloud, Redtail, Wealthbox | REST API, event-driven sync |
| **Portfolio Mgmt** | Black Diamond, Orion, Addepar, Envestnet | API, file import/export |
| **Financial Planning** | eMoney, MoneyGuidePro, RightCapital | API, SSO |
| **Trading/OMS** | Charles River, Bloomberg AIM, Flyer | FIX protocol, API |
| **Compliance** | ComplySci, Global Relay, Smarsh | API, file-based |
| **Document Mgmt** | NetDocuments, LaserFiche, DocuSign | API, webhook |
| **Accounting** | Geneva, Eagle, SimCorp | Batch/API |
| **Risk Analytics** | MSCI RiskMetrics, Axioma, Bloomberg PORT | API, batch |

---

## Part 2: Aiden AI Solution Patterns for Wealth Management

### 2.1 Solution Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENT EXPERIENCE LAYER                       │
│  Client Portal │ Advisor Workbench │ Mobile App │ Chatbot       │
├─────────────────────────────────────────────────────────────────┤
│                    AIDEN AI AGENT LAYER                          │
│  Advisor Copilot │ Client Insights │ Compliance │ Rebalancing   │
│  Onboarding Agent │ Research Agent │ Planning Agent │ Risk Agent │
├─────────────────────────────────────────────────────────────────┤
│                    AIDAP ORCHESTRATION LAYER                     │
│  Agent Orchestrator │ MCP 2.0 Tools │ Memory │ Context Engine   │
├─────────────────────────────────────────────────────────────────┤
│                    DATA & INTEGRATION LAYER                      │
│  Client 360 │ Market Data │ Custodian │ CRM │ Portfolio Mgmt    │
│  Vector DB │ Knowledge Graph │ Document Store │ Time Series DB  │
├─────────────────────────────────────────────────────────────────┤
│                    INFRASTRUCTURE LAYER                          │
│  Cloud (AWS/Azure/GCP) │ Security │ Monitoring │ CI/CD          │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 AI Agent Catalog — Wealth Management

Use these pre-designed agent patterns in proposals. Each agent is built on AIDAP's agentic framework with MCP 2.0 tool integration.

#### Agent 1: Advisor Copilot

**Purpose:** AI assistant embedded in the advisor workbench that augments advisor productivity.

**Capabilities:**
- Pre-meeting briefing generation (client summary, recent activity, open items, market impact on portfolio)
- Real-time meeting notes with automatic CRM entry and task creation
- Next-best-action recommendations based on client context, market conditions, and compliance rules
- Natural language portfolio queries ("How is the Smith household performing vs. benchmark YTD?")
- Draft client communications (emails, reviews, proposals) in advisor's tone
- Compliance-aware: flags potential suitability issues before recommendations are made

**MCP Tools:** CRM connector, portfolio data tool, market data tool, compliance checker, email drafter, meeting summarizer

**Estimated Effort:** 8–12 weeks for core capabilities

#### Agent 2: Intelligent Onboarding Agent

**Purpose:** Automates client onboarding from prospect to funded account.

**Capabilities:**
- Document collection orchestration (ID, tax forms, trust docs, beneficiary forms)
- AI-powered document extraction (OCR + NLP for ID verification, tax ID extraction, entity recognition)
- KYC/AML screening automation (PEP, sanctions, adverse media)
- Risk profiling through conversational questionnaire with adaptive follow-ups
- Account opening form pre-population from extracted data
- NIGO (Not In Good Order) detection and automated correction requests
- Status tracking dashboard with SLA monitoring

**MCP Tools:** IDV connector, sanctions screening tool, document extractor, form filler, notification engine, custodian API

**Estimated Effort:** 10–14 weeks

#### Agent 3: Portfolio Intelligence Agent

**Purpose:** Continuous portfolio monitoring, drift detection, and rebalancing recommendations.

**Capabilities:**
- Real-time drift monitoring against model portfolios with configurable thresholds
- Tax-aware rebalancing recommendations (harvest losses, avoid wash sales, manage short-term gains)
- Cash flow-aware rebalancing (incorporate pending deposits/withdrawals)
- Household-level optimization across multiple accounts (asset location)
- ESG/restriction overlay enforcement
- What-if scenario modeling for proposed trades
- Automated rebalancing execution (with advisor approval workflow)

**MCP Tools:** Portfolio data tool, market data tool, tax lot analyzer, trade order tool, compliance pre-check, scenario modeler

**Estimated Effort:** 12–16 weeks

#### Agent 4: Compliance & Surveillance Agent

**Purpose:** Continuous compliance monitoring with exception-based alerting.

**Capabilities:**
- Pre-trade compliance checking (concentration limits, restricted lists, suitability)
- Post-trade surveillance (pattern detection, unusual activity, best execution analysis)
- Reg BI documentation automation (capture rationale for every recommendation)
- Personal trading compliance (employee pre-clearance, restricted period monitoring)
- Marketing material review (AI-assisted review against FINRA advertising rules)
- Regulatory filing preparation (Form ADV, 13F, Blue Sky)
- Configurable rule engine for multi-jurisdiction compliance

**MCP Tools:** Trade data tool, compliance rules engine, regulatory database, alert manager, document generator, audit trail logger

**Estimated Effort:** 14–18 weeks

#### Agent 5: Client Insights & Engagement Agent

**Purpose:** Proactive client engagement through behavioral analytics and lifecycle event detection.

**Capabilities:**
- Life event detection from data signals (marriage, retirement, inheritance, business sale)
- Attrition risk scoring based on engagement patterns, performance, and sentiment
- Personalized content recommendations (market commentary, research, educational content)
- Client sentiment analysis across communication channels
- Referral opportunity identification
- Proactive outreach triggers with draft communications
- Client segmentation and next-best-product recommendations

**MCP Tools:** CRM connector, email analyzer, market content tool, sentiment analyzer, segmentation engine, notification tool

**Estimated Effort:** 8–10 weeks

#### Agent 6: Financial Planning Agent

**Purpose:** AI-augmented financial planning with scenario modeling and goal tracking.

**Capabilities:**
- Goal-based planning with Monte Carlo simulation
- Tax optimization strategies (Roth conversion, charitable giving, estate planning)
- Social Security claiming optimization
- Insurance gap analysis
- Cash flow projection and budgeting
- Plan vs. actual tracking with automatic alerts
- Natural language plan explanations for client-facing reports
- What-if modeling ("What if I retire 2 years early?", "What if market drops 20%?")

**MCP Tools:** Planning engine, tax calculator, Social Security optimizer, insurance analyzer, projection modeler, report generator

**Estimated Effort:** 12–16 weeks

#### Agent 7: Research & Market Intelligence Agent

**Purpose:** Curated market intelligence and investment research for advisors.

**Capabilities:**
- Personalized morning briefing based on advisor's book of business
- Earnings impact analysis on held positions
- Thematic research aggregation (AI reads and summarizes from multiple sources)
- Sector rotation signals and factor analysis
- Fixed income credit monitoring and spread analysis
- Alternative investment due diligence document analysis
- Client portfolio impact alerts (holdings affected by breaking news)

**MCP Tools:** Market data feed, news aggregator, research database, earnings analyzer, portfolio cross-reference, alert engine

**Estimated Effort:** 8–12 weeks

### 2.3 Client 360 — The Data Foundation

Every wealth management proposal must include a **Client 360** data layer. This is the single source of truth that all agents consume.

**Client 360 Components:**

| Component | Data Sources | AI Enhancement |
|-----------|-------------|----------------|
| **Demographics** | CRM, onboarding forms | Entity resolution, deduplication |
| **Financial Profile** | Custodian, held-away assets | Net worth aggregation, asset classification |
| **Goals & Plans** | Planning system, advisor notes | Goal extraction from unstructured notes |
| **Risk Profile** | Questionnaire, behavioral data | Dynamic risk scoring from trading behavior |
| **Interactions** | CRM, email, meetings, calls | Sentiment analysis, topic extraction |
| **Documents** | Document mgmt, custodian | AI classification, data extraction |
| **Preferences** | CRM, portal behavior | Communication channel/frequency preferences |
| **Relationships** | CRM, household data | Relationship mapping, influence analysis |
| **Compliance** | KYC/AML systems | Risk score aggregation, screening status |

**Implementation in AIDAP:**
- **Vector DB** stores embeddings of all client documents, interactions, and notes for semantic search
- **Knowledge Graph** maps relationships between clients, accounts, securities, advisors, and households
- **Time Series DB** stores portfolio values, performance, and market data
- **Event Store** captures every state change for full audit trail

### 2.4 Key Differentiators to Emphasize

When competing against traditional wealth management platforms (Salesforce Financial Services Cloud, SS&C, FIS, Broadridge), emphasize these Aiden AI differentiators:

| Traditional Platform | Aiden AI Advantage |
|---------------------|-------------------|
| Rule-based alerts | AI-driven predictive insights with reasoning |
| Manual CRM updates | Automatic CRM enrichment from every interaction |
| Static reports | Natural language queries with dynamic visualizations |
| Batch rebalancing | Real-time drift detection with tax-aware optimization |
| Form-based onboarding | Conversational AI onboarding with document intelligence |
| Keyword search | Semantic search across all client data |
| Fixed workflows | Adaptive agent-driven workflows that learn and improve |
| Siloed data | Unified Client 360 with knowledge graph relationships |
| One-size-fits-all | Hyper-personalized experiences per client tier |

### 2.5 Implementation Approach

**Recommended phased approach for wealth management proposals:**

#### Phase 1: Foundation (Weeks 1–8)
- Client 360 data model and integration framework
- Core custodian/CRM integrations
- Advisor Workbench UI shell
- Authentication, RBAC, audit logging
- **Deliverable:** Integrated data foundation + basic advisor portal

#### Phase 2: Advisory Intelligence (Weeks 9–18)
- Advisor Copilot agent (meeting prep, CRM automation, queries)
- Client Insights agent (engagement analytics, attrition scoring)
- Research & Market Intelligence agent
- **Deliverable:** AI-augmented advisor experience

#### Phase 3: Operations & Compliance (Weeks 19–28)
- Intelligent Onboarding agent
- Compliance & Surveillance agent
- Portfolio Intelligence agent (drift, rebalancing)
- **Deliverable:** Automated operations with compliance guardrails

#### Phase 4: Advanced Capabilities (Weeks 29–36)
- Financial Planning agent
- Client-facing portal with AI chatbot
- Advanced analytics & reporting
- Multi-entity/household optimization
- **Deliverable:** Full-featured wealth management platform

#### Phase 5: Optimization & Scale (Weeks 37–42)
- Performance tuning and load testing
- Model fine-tuning based on advisor feedback
- Advanced personalization
- Operational readiness and training
- **Deliverable:** Production-ready, scaled platform

### 2.6 Non-Functional Requirements — Wealth Management Specifics

Always address these in proposals:

| NFR | Requirement | Aiden AI Approach |
|-----|------------|------------------|
| **Data Encryption** | AES-256 at rest, TLS 1.3 in transit | AIDAP native encryption layer |
| **Data Residency** | U.S. data must stay in U.S. (SEC requirement) | Cloud region pinning |
| **Audit Trail** | Every action logged, immutable, 7-year retention | Event sourcing with append-only store |
| **Availability** | 99.95% for trading hours, 99.9% off-hours | Multi-AZ deployment, failover |
| **RTO/RPO** | RTO < 1 hour, RPO < 15 minutes | Cross-region replication, automated DR |
| **Performance** | Portfolio queries < 2s, trade execution < 500ms | Caching, read replicas, edge compute |
| **Scalability** | Support 10K+ concurrent advisors | Horizontal auto-scaling, queue-based processing |
| **PII Protection** | Mask SSN, account numbers in non-prod | Dynamic data masking, tokenization |
| **SOC 2 Type II** | Annual audit requirement | AIDAP inherits cloud SOC 2; app-level controls documented |
| **Penetration Testing** | Annual pen test required | Automated DAST/SAST + annual third-party pen test |

### 2.7 Pricing Considerations — Wealth Management

When estimating wealth management engagements, account for:

- **Integration complexity is the #1 cost driver** — custodian integrations (Pershing, Schwab, Fidelity) are notoriously complex with proprietary formats and slow certification processes. Budget 4–6 weeks per custodian.
- **Compliance adds 20–30% to base effort** — every feature needs compliance review, audit trail, and regulatory documentation.
- **Data migration is substantial** — historical portfolio data, client records, and documents from legacy systems. Budget 15–20% of total effort.
- **UAT cycles are longer** — wealth management firms require extensive UAT with real advisor testing. Plan 6–8 weeks minimum.
- **Training is critical** — advisors resist change; budget for comprehensive training program with champions network.

**Typical engagement sizes:**

| Scope | Duration | Team Size | AUM Range |
|-------|----------|-----------|-----------|
| **Robo-Advisory MVP** | 16–20 weeks | 6–8 | Mass affluent |
| **Advisor Workbench** | 24–32 weeks | 10–14 | HNW |
| **Full WM Platform** | 36–48 weeks | 16–22 | Multi-tier |
| **Enterprise Transformation** | 48–60+ weeks | 20–30+ | UHNW + Institutional |

---

## Part 3: Proposal Writing Guidance

### 3.1 Win Themes for Wealth Management RFPs

Use 3–4 of these win themes based on the specific RFP:

1. **AI-First, Not AI-Bolted**: Unlike legacy platforms adding AI as a feature, Aiden AI Builder is designed from the ground up for AI-driven wealth management. Every workflow has an intelligent agent, not just a chatbot.

2. **Advisor Empowerment, Not Replacement**: Our AI copilot makes advisors superhuman — handling data grunt work, compliance documentation, and meeting prep — so advisors spend 70% more time with clients instead of systems.

3. **Compliance by Design**: Regulatory compliance isn't a module — it's woven into every agent, every workflow, every data access. Full audit trail, real-time surveillance, and configurable rules that adapt as regulations evolve.

4. **Time-to-Value**: Phase 1 delivers a working Client 360 and advisor portal in 8 weeks. Advisors see value immediately while the platform grows around them.

5. **Future-Proof Architecture**: MCP 2.0, multi-model AI, and knowledge graph foundation means the platform evolves with new AI capabilities, new regulations, and new business needs without rearchitecting.

6. **Proven at Scale**: Reference Aiden AI case studies showing enterprise-grade AI deployments in financial services.

### 3.2 Common RFP Questions — Wealth Management

Prepare answers for these frequently asked questions:

| Question | Key Points to Cover |
|----------|-------------------|
| How do you handle fiduciary documentation? | Automatic Reg BI documentation, recommendation rationale capture, audit trail |
| What custodians do you integrate with? | Pershing, Schwab, Fidelity, DTCC — via FIX, proprietary APIs, file-based |
| How does your AI handle market volatility? | Circuit breakers, human-in-the-loop for large trades, configurable risk thresholds |
| What about held-away assets? | Plaid/Yodlee integration, manual entry, document extraction from statements |
| How do you support multi-entity households? | Household-level aggregation, account-level permissioning, unified reporting |
| GIPS compliance? | GIPS-compliant composite construction and reporting |
| What happens when the AI is wrong? | Human-in-the-loop checkpoints, confidence scoring, explainable recommendations |
| Data migration from legacy? | Proven migration framework, data quality scoring, parallel run validation |

### 3.3 Competitor Positioning

| Competitor | Their Strength | Our Counter |
|-----------|---------------|-------------|
| **Salesforce FSC** | CRM dominance, ecosystem | We integrate with Salesforce; our AI layer is far superior to Einstein for WM |
| **SS&C Advent/Black Diamond** | Deep portfolio accounting | We complement or replace with modern, AI-native portfolio intelligence |
| **Envestnet/Tamarac** | UMA/SMA, turnkey asset mgmt | We offer custom AI agents that go beyond rules-based rebalancing |
| **Orion** | Advisor-friendly, good reporting | We match UX and add AI copilot, compliance automation, and Client 360 |
| **Broadridge** | Back-office strength | We focus on front/middle office AI; can integrate with Broadridge back-office |
| **InvestCloud** | Digital client experience | Our agentic AI and knowledge graph are a generation ahead |

---

## Part 4: Technical Deep Dives (Use When RFP Requires Detail)

### 4.1 Tax-Aware Rebalancing Algorithm

When proposals require rebalancing detail, describe this approach:

```
Input: Current holdings, target allocation, tax lots, wash sale calendar,
       pending cash flows, restrictions, client tax bracket

Steps:
1. Calculate drift per asset class (current vs. target weight)
2. Identify tax-loss harvesting opportunities (lots with unrealized losses)
3. Check wash sale window (31 days before/after)
4. Prioritize sells: losses first (harvest), then long-term gains, then short-term
5. Apply restriction overlays (ESG, concentrated positions, client restrictions)
6. Optimize across household accounts (asset location: tax-exempt vs. taxable)
7. Generate trade list with estimated tax impact
8. Submit for compliance pre-check
9. Route to advisor for approval (or auto-execute if within parameters)

Output: Approved trade list, estimated tax savings, before/after allocation,
        compliance confirmation, audit trail entry
```

### 4.2 Client Risk Scoring Model

```
Risk Score = f(Questionnaire Score, Behavioral Score, Capacity Score)

Questionnaire Score (40%):
  - Time horizon, loss tolerance, income stability, experience level
  - Adaptive: follow-up questions based on inconsistent answers

Behavioral Score (30%):
  - Trading frequency, reaction to drawdowns, cash holding patterns
  - Derived from historical data, updated continuously

Capacity Score (30%):
  - Income-to-expense ratio, emergency fund, insurance coverage, debt levels
  - Calculated from financial plan data

Output: 1–100 score mapped to:
  1–20: Conservative | 21–40: Moderate Conservative | 41–60: Moderate
  61–80: Moderate Aggressive | 81–100: Aggressive

AI Enhancement: LLM analyzes free-text responses and advisor notes to detect
risk tolerance signals not captured by numeric questionnaire.
```

### 4.3 Performance Attribution (Brinson Model)

When RFP requires performance reporting detail:

```
Total Active Return = Allocation Effect + Selection Effect + Interaction Effect

Allocation Effect: Did the manager over/underweight the right sectors?
Selection Effect: Did the manager pick the right securities within sectors?
Interaction Effect: Cross-product of allocation and selection decisions

Implementation in AIDAP:
- Nightly batch calculation against configurable benchmarks
- Multi-level attribution (asset class → sector → industry → security)
- Currency attribution for international portfolios
- Fixed income attribution (duration, credit, yield curve)
- Visual drill-down in advisor workbench and client portal
```

---

## Appendix: Glossary of Wealth Management Terms

Use these terms correctly in proposals:

| Term | Definition |
|------|-----------|
| **AUM** | Assets Under Management — total market value of assets managed |
| **TWR** | Time-Weighted Return — performance measure eliminating cash flow impact |
| **MWR** | Money-Weighted Return (IRR) — performance including cash flow timing |
| **UMA** | Unified Managed Account — single account with multiple strategies |
| **SMA** | Separately Managed Account — individually managed portfolio |
| **TAMP** | Turnkey Asset Management Program — outsourced portfolio management |
| **RIA** | Registered Investment Advisor — SEC or state-registered advisory firm |
| **BD** | Broker-Dealer — firm executing securities transactions |
| **IAR** | Investment Advisor Representative — individual advisor at an RIA |
| **GIPS** | Global Investment Performance Standards — CFA Institute standards |
| **Reg BI** | Regulation Best Interest — SEC rule for BD recommendations |
| **Form ADV** | SEC registration and disclosure document for RIAs |
| **13F** | Quarterly holdings report for institutional investment managers |
| **Held-Away** | Assets custodied elsewhere but included in reporting |
| **NIGO** | Not In Good Order — document/form with errors or missing info |
| **Wash Sale** | IRS rule disallowing loss deduction if similar security bought within 31 days |
| **Asset Location** | Optimizing which assets go in which account type for tax efficiency |
| **Direct Indexing** | Owning individual securities to replicate an index for tax harvesting |
| **ESG** | Environmental, Social, Governance — sustainable investing criteria |
| **OCIO** | Outsourced Chief Investment Officer — institutional service model |
