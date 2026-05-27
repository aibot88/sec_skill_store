---
name: nullcost-recommend
description: Recommend the best providers for a specific development use case, including plain asks like cheap hosting, best value auth, free-tier database, or good email service for a SaaS. Use as a slash command when the user wants `/nullcost-recommend`. Do not use this for domain/registrar/TLD prompts.
argument-hint: <use-case>
version: 0.1.0
---

# Nullcost Recommend

The user invoked this command with: $ARGUMENTS

## Instructions

1. If `$ARGUMENTS` clearly asks for multiple stack parts such as hosting, auth, postgres, and email, use `recommend_stack` with the full natural-language request.
2. Otherwise use `recommend_providers` with the user's full natural-language use case.
3. If `$ARGUMENTS` is actually about domain availability, registrar pricing, TLD choice, transfers, renewals, or exact domain registration status, stop and route to TLDPlug instead of Nullcost.
4. Keep the answer DB-backed and catalog-first for v1. Do not browse, web-search, or verify official pricing pages.
5. If one result clearly wins and the user wants more detail on that exact provider, call `get_provider_detail` on that top provider before answering.
6. Preserve the tool's Markdown table output. Do not rewrite a table result into prose paragraphs when the host can render Markdown.
7. Return one short winner line first, unless the DB cannot confirm a requested feature from structured fields. In that case, say it is a shortlist instead of naming a hard winner.
8. Then render the top results as a Markdown table.
9. When there are 2 or more results, a Markdown table is required. Do not answer with prose paragraphs only.
10. Keep the table compact with a stable spine: `Provider`, `Link`, `Price`, and `Fit`.
11. Add only 1 compact dynamic column when it materially helps and actually varies across the returned rows. Use 2 only when the comparison really needs it.
12. Prefer dynamic columns like `MCP Fit`, `Setup`, `Free Entry`, `API Surface`, or `Deployment` based on the request.
13. Distinguish `Free tier` from `Free trial` in the `Price` or `Free Entry` cell. Do not collapse them into the same label.
14. If the user asks for `best value`, `affordable`, `good value`, `cheap`, `spend`, `cost`, `current pricing`, or `SSR costs`, stay on the Nullcost database path and prefer providers with visible pricing while calling out when pricing is unknown.
15. Do not waste columns on signals that are constant across the current rows.
16. Mention the main tradeoff for each row in the `Fit` text instead of adding a generic `Notes` column unless the comparison truly needs it. Keep `Fit` short.
17. Mention any verified program or discount signal only after the fit-based recommendation.
18. If the user is following up on an earlier shortlist, pass the earlier use case or shortlist summary into the tool's `context` field so modifiers like `cheaper`, `self-hosted`, or `only show auth` are interpreted correctly.
19. If the user asks for features the DB does not confirm cleanly, explicitly say that and present a shortlist table rather than overstating certainty.

## Output Shape

Prefer this structure in normal chat:

```md
**Best fit:** Provider name

| Provider | Link | Price | MCP Fit | Fit |
| --- | --- | --- | --- | --- |
| Winner | [Official](https://example.com) | ... | ... | ... |
| Alt 1 | [Official](https://example.com) | ... | ... | ... |
| Alt 2 | [Official](https://example.com) | ... | ... | ... |
```

If the host clearly fails to render Markdown tables, fall back to compact rows.
Prose-only recommendation answers are incorrect when a table can be rendered.
