---
name: payroll-processing
description: Run payroll end-to-end — gross-to-net calculations, tax withholding, benefits deductions, contractor payments, and compliance filings.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, payroll, compensation, tax-withholding, benefits, contractors]
related_skills:
  - ledger-management
  - tax-compliance-management
  - cash-forecasting
  - headcount-and-comp-planning
  - transaction-processing
inputs_required:
  - employee-roster
  - pay-period-data
  - prior-payroll-register
  - tax-rate-tables
  - benefits-elections
deliverables:
  - payroll-register
  - payroll-summary
  - journal-entry-for-ledger
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Payroll Processing

## Purpose

Every employee and contractor must be paid correctly and on time, with all tax withholdings, benefits deductions, and compliance filings handled accurately. This skill calculates gross-to-net pay, applies federal/state/local tax tables, handles benefits deductions, and prepares the payroll register for review. Without it, payroll errors lead to compliance penalties, employee dissatisfaction, and cash flow surprises.

## When to Use

- "Run payroll for this period"
- "Review payroll before processing"
- "Calculate net pay for these employees"
- "Process contractor payments"
- "File payroll taxes"
- "Update benefit deductions"

## Inputs Required

1. **Employee roster** — name, salary/hourly rate, pay frequency, tax withholding elections (W-4), benefit elections, state of employment.
2. **Pay period data** — hours worked (hourly), PTO taken, commissions/bonuses earned, expense reimbursements.
3. **Prior payroll register** — last period's numbers for sanity check.
4. **Tax rate tables** — federal, state, local for each employee location.
5. **Benefits elections** — health, dental, vision, 401(k) deferrals, HSA/FSA.

## Quick Reference

| Calculation | Formula / Rule | Why It Matters |
|------------|---------------|---------------|
| Gross Pay (Salaried) | Annual salary / Pay periods per year | Base for all deductions |
| Gross Pay (Hourly) | Hours worked × Rate (OT at 1.5× over 40 hrs) | Accurate for variable-hour employees |
| Federal Income Tax Withholding | IRS Pub 15-T tables based on W-4 and taxable wages | Largest single withholding; errors trigger penalties |
| FICA (Social Security + Medicare) | SS: 6.2% up to wage base / MC: 1.45% (0.9% additional over $200k) | Mandatory employer + employee portions |
| Benefits Deductions | Pre-tax: 401(k), medical, HSA / Post-tax: Roth 401(k), life insurance | Correct treatment prevents tax filing errors |
| Net Pay | Gross − Taxes − Deductions + Reimbursements | What employees actually receive |
| Total Employer Cost | Gross pay × 1.25–1.4× (incl. employer taxes, benefits, workers comp) | True cost of headcount for planning |

## Procedure

### 1. Gross Pay Calculation

- **Salaried**: annual salary / pay periods. Prorate for mid-period hires/terminations.
- **Hourly**: hours worked × rate. Overtime at 1.5× for > 40 hours.
- **Commissions**: apply the commission plan. Validate against deals closed.
- **Bonuses**: apply the bonus formula. Confirm eligibility and approval.
- **Contractors**: flat amount per invoice, NO tax withholding.

### 2. Tax Withholding

- **Federal income tax**: IRS Pub 15-T tables based on W-4 elections, pay frequency, taxable income.
- **Social Security**: 6.2% up to the annual wage base.
- **Medicare**: 1.45% + 0.9% additional above $200k.
- **State income tax**: per-state tables.
- **Local taxes**: where applicable (NYC, SF, etc.).

### 3. Benefits Deductions

- Pre-tax: 401(k), medical/dental/vision premiums, HSA, FSA, commuter.
- Post-tax: life insurance, disability, Roth 401(k).
- Employer contributions listed separately.

### 4. Net Pay = Gross − Taxes − Deductions + Reimbursements

### 5. Payroll Register Review

Generate a payroll register:

| Employee | Gross | Federal WH | FICA | State WH | Benefits (Pre) | Benefits (Post) | Net Pay | Employer Taxes & Benefits |
|---|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

- Flag any net-pay anomalies: change > 20% from prior period, zero net pay (garnishment/error), negative net pay.
- Verify total employer-side taxes and benefits: FICA match (~7.65%), FUTA, SUTA, 401(k) match, health insurance contribution.

### 6. Payment & Filing

- Present the payroll register for **human approval**.
- After approval, prepare the journal entry: debit salaries/benefits/taxes expense, credit cash/bank, credit tax liabilities.
- **Filing calendar** hand-off to `tax-compliance-management` for: 941 (quarterly), 940 (annual), state quarterly filings, W-2/W-3 (annual), 1099-NEC (annual).

## Output Format

**Payroll Summary:**
- Total gross payroll
- Total net pay to employees
- Total employer taxes
- Period-over-period change (headcount and dollars)
- Runway impact

## Done Criteria

The skill is complete when:
1. Gross pay is calculated correctly for all employees and contractors (salaried, hourly, commission, bonus)
2. Tax withholdings are applied using current federal, state, and local tables
3. Benefits deductions (pre-tax and post-tax) are applied correctly
4. Net pay is calculated and anomalies are flagged
5. Employer-side taxes and benefits costs are calculated and documented
6. The payroll register is presented for human approval (not auto-disbursed)
7. Journal entry is prepared for hand-off to `ledger-management`

## Pitfalls

- **Misclassifying employees as contractors (1099 vs W-2)**: If they work full-time, on your schedule, with your equipment → they're likely an employee. Misclassification carries heavy penalties
- **Using outdated tax tables**: Tax withholding tables change annually. Always use the current year's IRS Pub 15-T and current state tables
- **Forgetting multi-state withholding**: Withholding by state based on physical work location, not company HQ. Remote employees trigger nexus in their state
- **Ignoring bonus supplemental rate**: Federal supplemental rate is flat 22% for bonuses under $1M. Using regular withholding tables over-withholds
- **Skipping period-over-period comparison**: Not comparing the register to the prior period. A sudden 20% swing in net pay for an employee is usually an error worth catching before disbursement
- **Auto-disbursing without human approval**: Processing payroll directly to the bank without a review step. Payroll errors are expensive and embarrassing — always present for review first

## Verification

Is each employee's gross pay calculated correctly based on their pay type (salaried, hourly, commission)? Are tax rates verified against current tables for each employee's work location? Are pre-tax and post-tax deductions applied to the correct income basis? Is the payroll register compared to the prior period for anomaly detection? Is the register presented for human approval before any disbursement?

## Example

**Example 1: Standard Payroll Run**
> User: "Run payroll for the bi-weekly period ending April 18 — we have 12 employees and 3 contractors"

→ You load the employee roster, pull W-4 elections and state info, collect timesheets for hourly employees and commission data for sales, calculate gross pay ($124,500 total), apply federal/state tax withholding ($31,200), apply benefits deductions ($8,900 pre-tax, $2,100 post-tax), compute net pay ($82,300), calculate employer-side taxes and benefits ($18,675), flag one employee with a 35% net pay increase (bonus included — confirmed), and present the full payroll register for human approval with a total cash outflow of $100,975 (net pay + employer taxes).

**Example 2: Contractor Payment Run**
> User: "Process May contractor payments — 5 contractors totaling $28,000"

→ You verify each contractor's invoice against their agreement, confirm no tax withholding applies (all 1099-NEC eligible), run a quick worker classification check (all are genuinely independent — separate schedule, own tools, multiple clients), present the payment summary for approval, and note the 1099-NEC tracking requirement for year-end filing.
