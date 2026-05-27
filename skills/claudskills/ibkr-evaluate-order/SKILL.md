---
name: ibkr-evaluate-order
description: Evaluate a proposed single-leg order through full pre-trade validation. Use when the user requests to buy or sell a specific instrument and you need to assess portfolio impact, concentration, and profile compliance before any approval or execution. Call ibkr-place-order after this skill to execute an approved order.
---

# IBKR Evaluate Order

Evaluate and validate a single-leg order without placing it. Produces a constraint-adjusted order preview with portfolio impact, concentration change, and profile compliance.

## When to Use

- User says "buy X shares of Y" or "sell Y" and you need to validate before execution
- Comparing multiple order scenarios before committing
- Use after `ibkr-portfolio-snapshot` for context
- Follow up with `ibkr-place-order` once the user approves

## Workflow

### Phase 1 — Trading Status Check

1. Call `ibkr_get_trading_status` — read `dryRun`, `ordersEnabled`, `tradingMode`, `blockReason`
2. If `dryRun=true` or `tradingMode=paper`, note it in the output (the user may want to change it before evaluating)
3. If `ordersEnabled=false`, stop here and report the block to the user
   - `blockReason` alone is informational and does NOT block evaluation when `ordersEnabled=true` and `dryRun=false`
   - A safety-lock blockReason (e.g., "Safety lock engaged after environment switch") is cleared automatically when the user intentionally unlocks via `ibkr_admin_update_trading_control`

### Phase 2 — Instrument Qualification

4. Call `ibkr_resolve_contract` to fully qualify the instrument (symbol + securityType + exchange + currency)

### Phase 3 — Pre-Trade Validation

5. Call `ibkr_preview_order` with the full `OrderSpec` — get estimated price, notional, commission, warnings
6. Call `ibkr_assess_order_impact` — get concentration change, buying-power usage, margin impact
7. Call `ibkr_validate_against_profile` — confirm the order is within profile limits

### Phase 4 — Constraint Presentation

8. Present the evaluated order with a clear summary table:

**Instrument:** `<symbol>` | `<securityType>` | `<exchange>` / `<currency>`
**Side:** `<BUY|SELL>` | **Qty:** `<qty>` | **Order Type:** `<orderType>`
**Est. Price:** `<price>` | **Est. Notional:** `<notional>`

**Portfolio Impact:**
| Metric | Value |
|--------|-------|
| Concentration before | `<pct>%` |
| Concentration after | `<pct>%` |
| Buying power used | `<pct>%` |
| Margin utilisation | `<pct>%` |

**Profile Check:** `<passed|failed>` | Violations: `<list or "None">`
**Warnings:** `<list or "None">`

9. If the qty needed adjustment to satisfy profile limits or the minimum remaining position constraint, note the adjusted qty and why.

10. Call `question` to confirm: "Ready to submit for Telegram approval?" with options "Yes, submit" and "No, cancel" (only proceed if they confirm)

## Guardrails

- **This skill is read-only with respect to execution.** Do not call `ibkr_place_order`, `ibkr_request_trade_approval`, or any execution tool inside this skill.
- Use a unique `clientOrderId` for every evaluation (e.g. `{symbol}-{side}-{timestamp}`).
- If `ordersEnabled=false` or `blockReason` is set, stop and report the block reason — do not proceed to evaluation.
- If `dryRun=true` or `tradingMode=paper`, note it but still run the full validation (the user may choose to enable live trading before execution).

## OrderSpec Reference

```
{
  "instrument": { "symbol": "<SYMBOL>", "securityType": "STK", "exchange": "SMART", "currency": "USD" },
  "side": "BUY" | "SELL",
  "quantity": <positive number>,
  "orderType": "MKT" | "LMT" | "STP" | "STP_LMT",
  "limitPrice": <number, required for LMT/STP_LMT>,
  "tif": "DAY" | "GTC" | "IOC",
  "outsideRth": false,
  "clientOrderId": "<unique-id>",
  "transmit": true
}
```

## Resources

- `ibkr_get_trading_status`
- `ibkr_resolve_contract`
- `ibkr_preview_order`
- `ibkr_assess_order_impact`
- `ibkr_validate_against_profile`
