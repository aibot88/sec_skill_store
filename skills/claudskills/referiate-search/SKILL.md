---
name: nullcost-search
description: Search the Nullcost provider catalog by keyword or plain-English asks like cheap auth service, free-tier hosting, or good value Postgres. Use as a slash command when the user wants `/nullcost-search`. Do not use this for domain/registrar/TLD prompts.
argument-hint: <query>
version: 0.1.0
---

# Nullcost Search

The user invoked this command with: $ARGUMENTS

## Instructions

1. Use `search_providers` with the user’s full natural-language query from `$ARGUMENTS`.
2. If the user is really asking for a decision on a common stack such as hosting + auth + postgres + email, switch to `recommend_stack` instead of chaining multiple searches.
3. If the query is actually about a domain name, registrar, TLD, availability, transfer, renewal, or exact registration status, route to TLDPlug instead of Nullcost.
4. Keep search and recommendation flows DB-backed for v1 instead of escalating to live pricing checks. Do not browse or verify official pricing pages.
5. Return the best-matching rows as a Markdown table when there are 2 or more results.
6. When there are 2 or more results, a Markdown table is required. Do not answer with prose paragraphs only.
7. Keep the table compact with a stable spine: `Provider`, `Link`, `Price`, and `Fit`.
8. Add `Category` when the result set spans multiple categories.
9. Add only 1 or 2 dynamic columns when they materially help and actually vary across the result set.
10. Good dynamic columns are `MCP Fit`, `Setup`, `Free Entry`, `API Surface`, or `Deployment`.
11. Distinguish `Free tier` from `Free trial` explicitly when showing price-sensitive results.
12. If the user is clearly price-sensitive or asking about spend, cost, current pricing, or value, prefer rows with visible pricing over rows where pricing is unknown and stay on the Nullcost database path.
13. Do not waste columns on signals that are constant across the current rows.
14. If the query is empty or vague, say what kind of keyword would narrow it down.
15. If the user is clearly following up on an earlier shortlist, pass the earlier query or shortlist summary into the tool's `context` field.

## Output Shape

- If there is a clear top result, add one short line above the table.
- Then render a Markdown table.
- For mixed-category searches, prefer a shape like `Provider | Link | Category | Price | Fit`.
- If the host clearly fails to render tables, fall back to compact rows.
- Prose-only search-result answers are incorrect when a table can be rendered.
