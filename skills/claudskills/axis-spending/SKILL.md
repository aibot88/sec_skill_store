---
name: axis-spending
description: "Fetches Axis Bank transaction emails via Himalaya, categorizes them using notebook-style regex rules, stores them in SQLite, generates weekly and monthly dashboards from stored history, and sends a WhatsApp summary. Use when asked about weekly spending reports, category summaries, or transaction analysis."
metadata: {"clawdbot":{"emoji":"💸","requires":{"bins":["himalaya","python3"]}}}
---

# Axis Bank Spending Tracker

## Description
Use this skill when the user asks to:
- Generate a spending report or weekly summary
- Show how much was spent this week or last week
- Analyze Axis Bank transactions by category or payee/target
- View spending dashboard
- Check food / transport / rent / any category spend
- Run the spending report manually

## Tool: generate_weekly_report

Fetches Axis Bank transaction emails from the last 7 days, categorizes them
using notebook-style regex rules, stores them in SQLite, generates stored-history
dashboards, and sends a WhatsApp summary with the latest dashboard link.

### Usage
```bash
cd /home/zain/zainclaw/axis_spending
python3 axis_tracker.py
```

From a checked-out repo root, this also works:
```bash
python3 zainclaw/axis_tracker.py
```

### Custom date range (optional)
```bash
# Last 14 days
cd /home/zain/zainclaw/axis_spending
python3 axis_tracker.py 14

# Last 30 days
python3 axis_tracker.py 30
```

### Output
- HTML dashboard at: https://claw.mohdzain.com/spending/latest.html
- Current month dashboard at: https://claw.mohdzain.com/spending/current-month.html
- All-time dashboard at: https://claw.mohdzain.com/spending/all-time.html
- Archive page at: https://claw.mohdzain.com/spending/archive.html
- SQLite database at: `/home/zain/zainclaw/axis_spending/data/transactions.db`
- Per-category debit / credit / net summary table
- Category target drill-down table grouped by extracted payee/merchant
- WhatsApp message with summary and link
- Console output with debit / credit totals and top category rows

### Categories tracked
emi, rent, food, transport, credit, recharge, airticket, grocery, medical,
shopping, maintainence, friends, home, juice_below_vsai, hair, vydehi,
snapchat, bank, self, ais, interest, subscriptions, gym_and_health,
kayakalp, other

### Notes
- Only processes emails from alerts@axis.bank.in
- Requires Himalaya configured at ~/.config/himalaya/config.toml
- Categorization order: regex notebook rules → "other"
- Transactions are deduplicated and stored in SQLite using a stable source id
- Dashboard includes weekly totals, category summary, grouped target-level drill-down, and separate stored-history views for current month and prior months
- Dashboard files are written inside `/home/zain/zainclaw/axis_spending/dashboard`
- Runs automatically every Monday at 12:00 AM IST via cron
