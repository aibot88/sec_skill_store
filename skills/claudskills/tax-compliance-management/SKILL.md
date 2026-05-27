---
name: tax-compliance-management
description: Manage the full tax compliance lifecycle — calendar management, federal and state filings, payroll taxes, sales tax, corporate income tax, R&D credits, and multi-state nexus tracking.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, tax-compliance, tax-filing, sales-tax, payroll-tax, rd-credit]
related_skills: [payroll-processing, monthly-close-process, financial-statement-generation, audit-preparation, internal-controls-design, headcount-and-comp-planning]
inputs_required: [current-state-tax-obligations, payroll-register-and-tax-filings, revenue-data-by-state, rd-activity-documentation, vendor-w9-forms]
deliverables: [annual-tax-compliance-calendar, monthly-compliance-checklist, sales-tax-nexus-map, quarterly-estimated-tax-calculation, rd-credit-eligibility-assessment]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Tax Compliance Management

Manage all tax obligations — from the compliance calendar to filing deadlines to payment processing. Federal, state, local, payroll, sales tax, and income tax. Goal: nothing is ever filed late, underpaid, or missed.

## Purpose

Tax compliance is non-negotiable — missed deadlines mean penalties, interest, and in extreme cases, personal liability for payroll taxes. Yet most startup finance teams manage taxes reactively, scrambling when deadlines approach. This skill provides a proactive, calendar-driven approach to tax compliance: tracking every filing obligation, managing the R&D credit (the single most valuable tax incentive for startups), and ensuring multi-state nexus is properly managed as the company grows.

## When to Use

- "What taxes do we need to file?"
- "When is our next tax deadline?"
- "File payroll taxes / sales tax / income tax"
- "Calculate our estimated tax payment"
- "Are we compliant in all states we operate in?"
- "Track our R&D tax credit eligibility"

## Inputs Required

- Current state tax obligations and filing history
- Payroll register and tax filings (941, 940, state)
- Revenue data by state (for sales tax nexus)
- R&D activity documentation (projects, engineers, time tracking)
- Vendor W-9/W-8BEN forms
- Prior year tax returns
- State registration status for all nexus states

## Quick Reference

| Filing Frequency | Key Obligations | Due Date |
|-----------------|----------------|----------|
| Monthly | Payroll tax deposits, state payroll tax, sales tax | 15th-30th of following month |
| Quarterly | Form 941, FUTA deposit, estimated income tax | Last day of month following quarter |
| Annual | W-2/W-3 (Jan 31), 1099-NEC (Jan 31), Form 940 (Jan 31), Corporate income tax (Mar 15 or Apr 15) | Varies |

| Tax Type | Startup Relevance | Risk Level |
|----------|------------------|------------|
| Payroll tax | Every company with employees | CRITICAL — personal liability |
| Sales tax | SaaS/software companies | HIGH — unregistered nexus = back taxes |
| Income tax (federal) | C-corps pay 21% | MEDIUM — estimated payments |
| R&D credit | Any company building software | OPPORTUNITY — up to $500k/yr payroll tax offset |

## Procedure

### 1. Build the Tax Calendar

For the current year, list every filing obligation with:
- Due date
- Responsible party (internal, CPA, payroll provider)
- Form/agency
- Estimated amount (if applicable)
- Status: `Not Started | In Progress | Filed | Confirmed`

### 2. Monthly Check

First week of every month:
1. Review what was due last month — was everything filed?
2. Review what's due this month — who's handling it?
3. Flag any upcoming deadlines within 7 days.

### 3. Quarterly Estimated Tax Calculation

For C-corps making estimated payments:
```
Estimated taxable income for the year (from budget / forecast)
× Federal corporate tax rate (21%)
÷ 4 quarterly payments
```

For pass-through entities (S-corps, LLCs), estimated taxes flow to individual owners.

### 4. Year-End Preparation (November-December)

- [ ] Verify all W-9/W-8BEN forms from vendors are current.
- [ ] Confirm contractor vs employee classification for all 1099 recipients.
- [ ] Gather data for 1099-NEC and 1099-MISC.
- [ ] Verify payroll data for W-2s.
- [ ] Review R&D credit eligibility and gather documentation.
- [ ] Schedule year-end tax planning call with CPA.

### Tax Calendar

#### Monthly

| Filing | Due Date | Agency | Form |
|---|---|---|---|
| Federal payroll tax deposit | 15th of following month (or next business day) | IRS | 941 deposit |
| State payroll tax deposit | Varies by state (typically monthly) | State DOR | Varies |
| State unemployment tax | Varies by state | State DOL | Varies |
| Sales tax return | Varies by state (typically 20th-30th) | State DOR | Varies |

#### Quarterly

| Filing | Due Date | Agency | Form |
|---|---|---|---|
| Federal payroll tax return | Last day of month following quarter | IRS | Form 941 |
| Federal unemployment tax deposit | Last day of month following quarter (if > $500) | IRS | Form 940 deposit |
| State payroll tax reconciliation | Varies | State | Varies |
| Estimated income tax payments | Apr 15, Jun 15, Sep 15, Jan 15 | IRS + State | Form 1040-ES (federal), varies (state) |

#### Annual

| Filing | Due Date | Agency | Form |
|---|---|---|---|
| W-2 to employees + SSA | Jan 31 | SSA | Form W-2 / W-3 |
| 1099-NEC to contractors + IRS | Jan 31 | IRS | Form 1099-NEC / 1096 |
| 1099-MISC (other payments) | Jan 31 to recipients, Feb 28 to IRS | IRS | Form 1099-MISC |
| Federal unemployment tax return | Jan 31 | IRS | Form 940 |
| Corporate income tax return (C-corp) | Apr 15 (15th day of 4th month after year-end) | IRS | Form 1120 |
| Corporate income tax return (S-corp) | Mar 15 (15th day of 3rd month after year-end) | IRS | Form 1120-S |
| State income tax returns | Varies (typically same as federal) | State DOR | Varies |
| Annual report / franchise tax | Varies by state (often anniversary of incorporation) | Secretary of State | Varies |
| Property tax returns | Varies by locality | Local | Varies |

### Sales Tax Compliance

For startups selling software:

#### Nexus Determination

You have sales tax nexus in a state if you have:
- Physical presence (office, employees, inventory).
- Economic nexus (> $100k in sales or > 200 transactions, varies by state).
- Marketplace facilitator laws may apply (selling through app stores, Stripe).

#### Collection & Remittance

1. Register in every state where you have nexus.
2. Determine taxability: SaaS is taxable in most states, but rules vary.
3. Collect tax on every invoice to customers in nexus states.
4. File returns monthly, quarterly, or annually (based on volume).
5. Remit collected tax.

#### Common Pitfalls

- **Not registering soon enough**: penalties and interest + liability for uncollected tax.
- **Not taxing SaaS correctly**: some states exempt SaaS, others tax it. Rules change annually.
- **Marketplace facilitator confusion**: if you sell through an app store, they may handle tax for you.

### Payroll Tax Compliance

Hand off to `payroll-processing` for calculation and filing execution. This skill manages the calendar and compliance verification.

#### Key Compliance Checks

- [ ] All new hires have completed W-4 (federal) and state equivalent.
- [ ] E-Verify completed where required.
- [ ] New hire reporting filed with the state (typically within 20 days).
- [ ] Multi-state withholding set up for remote employees (withhold for the state where they WORK, not where HQ is).
- [ ] FICA tip reporting for any tipped employees.
- [ ] All tax deposits made on time (late deposits trigger penalties starting at 2% at day 1-5, scaling to 15%).

### R&D Tax Credit

For startups doing software development:

#### Qualification Checklist

- [ ] Developing new or improved products/processes?
- [ ] Technical uncertainty existed at the start?
- [ ] Process of experimentation (trying approaches, evaluating alternatives)?
- [ ] Technical in nature (engineering, computer science)?

#### Qualified Research Expenses (QREs)

- Wages of employees doing qualified research (engineers, designers, product managers doing technical work).
- Supplies used in R&D.
- Contract research (65% of contractor costs if for qualified research).
- Cloud computing costs (infrastructure for dev/test).

#### Benefit

- **Payroll tax offset** (startups with < $5M revenue and < 5 years old): up to $500k/yr offset against employer FICA.
- **Income tax credit**: ~6-10% of QREs. Carryforward 20 years.

This is the single most valuable tax incentive for startups — often worth $50k-$250k+/year.

## Output Format

- Annual tax compliance calendar (with status tracking)
- Monthly compliance checklist
- Sales tax nexus map (states registered, states pending)
- Quarterly estimated tax calculation
- Year-end tax preparation checklist
- R&D credit eligibility assessment

## Done Criteria

The skill is complete when:
1. The annual tax compliance calendar is built with all federal, state, and local filing obligations, due dates, and responsible parties.
2. Monthly compliance check process is established to review past and upcoming deadlines.
3. Sales tax nexus determination is completed and a registration plan is created for all nexus states.
4. R&D credit eligibility is assessed with QRE documentation gathered.
5. Quarterly estimated tax calculations are prepared (if applicable).
6. Year-end preparation checklist is ready with November-December timeline.

## Pitfalls

- **Missing payroll tax deadlines** — the IRS is unforgiving on payroll taxes. The Trust Fund Recovery Penalty can pierce the corporate veil and hold owners personally liable.
- **Not tracking sales tax nexus changes** — a single remote employee in a new state can create sales tax nexus. Track new hires against the nexus map.
- **Missing the R&D credit** — most startup founders don't know they qualify. If you have engineers building software, you almost certainly do.
- **Waiting until April to start tax preparation** — year-end tax planning should start in November. Waiting until filing season means missed opportunities (R&D credit, estimated tax planning, state registration timing).
- **Relying entirely on your CPA to track deadlines** — a CPA prepares returns, but the CFO owns the calendar. Don't outsource the responsibility for knowing what's due when.

### Heuristics

- **Never miss a payroll tax deadline**: the IRS is unforgiving on payroll taxes. The Trust Fund Recovery Penalty can pierce the corporate veil and hold owners personally liable.
- **Sales tax nexus changes when you hire**: a single remote employee in a new state can create sales tax nexus. Track new hires against the nexus map.
- **R&D credit is underclaimed**: most startup founders don't know they qualify. If you have engineers building software, you almost certainly do.
- **Outsource the heavy lifting, own the calendar**: a CPA prepares the returns, but the CFO owns the calendar and ensures nothing falls through the cracks.

### Edge Cases

- **International subsidiaries**: local country tax obligations, transfer pricing rules, VAT/GST instead of sales tax.
- **Acquisitions**: tax due diligence, step-up in basis, NOL limitations (Section 382).
- **State tax amnesty programs**: some states offer amnesty from penalties if you voluntarily register. Worth checking before registering in a new state.
- **Delaware franchise tax**: two methods — authorized shares method (often very expensive) and assumed par value method (usually cheaper). File using the cheaper method.

## Verification

Can you answer "What's our next tax deadline and is everything ready for it?" without checking a calendar? Is there a documented R&D credit assessment showing whether the company qualifies and how much it's worth? Are all states where you have nexus properly registered for sales tax? If not, tax compliance management is incomplete.

## Example

> **User**: "Set up our tax compliance tracking for the year."
> **Expected behavior**: You build the full annual tax calendar with every federal, state, and local filing obligation listed by month with due dates, forms, and responsible parties. You set up a monthly review process. You assess sales tax nexus based on current operations and employees, identify states that need registration, and create a registration plan.

> **User**: "Are we eligible for the R&D tax credit?"
> **Expected behavior**: You review the company's engineering activities against the four-part qualification test (technical uncertainty, process of experimentation, technical in nature, new/improved product), estimate qualified research expenses (wages, supplies, contract research, cloud costs), calculate the potential credit value (up to $500k payroll tax offset), and document the methodology for the CPA to file.

## Linked Skills

- Payroll tax filing execution → `payroll-processing`
- Financial data for returns → `monthly-close-process`, `financial-statement-generation`
- Audit support → `audit-preparation`
- Controls around tax → `internal-controls-design`
- Headcount data for payroll tax & nexus → `headcount-and-comp-planning`
