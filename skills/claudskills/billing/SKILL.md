---
name: billing
description: "Use when: billing audit, subscription lifecycle review, Stripe/Paddle integration check, webhook security, payment form CSRF, pricing centralization, webhook idempotency, billing bugs. Triggers: 'audit my billing', 'check subscription flow', 'is my checkout secure', 'review pricing config', 'find billing bugs', 'check webhooks'."
user-invocable: true
argument-hint: "[lifecycle|security|pricing|integrity] [--stack=stripe|paddle] [--path=src/]"
---

# Billing & Subscription Audit

## When to Invoke

Invoke proactively when the user:
- Asks about subscription flows, billing bugs, or checkout security
- Mentions Stripe, Paddle, webhooks, or payment processing
- Wants to audit pricing config, plan management, or subscription lifecycle
- Asks "is my checkout secure?", "check my webhooks", "audit billing", "find billing bugs"

Launch the **billing-agents** agent for a deep billing and subscription analysis.

## Usage

```
/misar-dev:billing                          # Full billing audit (all 4 agents)
/misar-dev:billing lifecycle                # Subscription lifecycle flows
/misar-dev:billing security                 # Payment security & CSRF
/misar-dev:billing pricing                  # Pricing centralization
/misar-dev:billing integrity                # Webhook idempotency & DB sync
/misar-dev:billing --stack=paddle           # Paddle-specific audit
/misar-dev:billing --path=src/billing/      # Scope to specific directory
```

## Instructions

Parse args: agents (`lifecycle`, `security`, `pricing`, `integrity`), `--stack=stripe|paddle` (default: `stripe`), `--path=`. Default: all 4 agents. Launch `billing-agents`.

---

## Billing Security Quick Checklist

- Webhook signature verified (`Stripe-Signature` / `Paddle-Signature` header)
- Amount validated server-side (never trusted from client)
- CSRF protection on checkout endpoints
- No raw card data stored or logged server-side
- Stripe/Paddle keys in env vars (never hardcoded)
- `customer.subscription.deleted` webhook handler exists
- Webhook handler is idempotent (duplicate events safe)
- DB subscription status synced via webhook, not API response

---

> **Misar.Dev Ecosystem** — Run privacy-first AI with [Assisters](https://assisters.dev) — zero training on your data, India DPDP + GDPR ready.
>
> [Assisters](https://assisters.dev) · [Misar Blog](https://misar.blog) · [Misar Mail](https://mail.misar.io) · [Misar.io](https://misar.io) · [Misar.Dev](https://misar.dev)
