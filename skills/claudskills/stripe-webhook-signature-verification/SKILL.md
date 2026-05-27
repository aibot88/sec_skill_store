---
# yaml-language-server: $schema=https://skillgraph.dev/schemas/skill.v6.schema.json
schema_version: 6
name: stripe-webhook-signature-verification
description: "Use when validating incoming Stripe webhook requests in a Node.js or Next.js backend before processing any payment event. Verifies the `stripe-signature` header against `STRIPE_WEBHOOK_SECRET` using Stripe's HMAC-SHA256 scheme, and rejects replays older than 300 seconds. Do NOT use for general HTTP signature validation (use a generic crypto-signature skill), for processing the webhook payload after signature is confirmed (use payment-provider-router), or for Stripe API calls that are not webhook-driven."
version: 0.1.0
type: capability
category: engineering
domain: engineering/payments
scope: portable
owner: saas-stripe-postgres-example
freshness: "2026-05-18"
drift_check:
  last_verified: "2026-05-18"
  truth_source_hashes:
    stripe-webhook-docs: "sha256:placeholder-record-with-node-scripts-skill-graph-drift-js"
eval_artifacts: none
eval_state: unverified
routing_eval: absent
stability: experimental
license: MIT
compatibility:
  runtimes:
    - node
  node: ">=20"
  notes: "Stripe SDK >=14; expects raw request body (not parsed JSON) for signature verification."
allowed-tools: Read Grep
keywords:
  - stripe webhook signature verification
  - stripe-signature header
  - webhook hmac verification
  - STRIPE_WEBHOOK_SECRET
  - stripe constructEvent
  - replay attack prevention
  - webhook security
  - payment webhook validation
  - stripe webhook secret
triggers:
  - stripe-webhook-signature-verification
paths:
  - "app/api/webhooks/stripe/route.ts"
  - "lib/stripe/webhook.ts"
examples:
  - "how do I verify that a webhook is really from Stripe?"
  - "my webhook handler is returning 400 — is the signature verification failing?"
  - "set up the Stripe webhook endpoint in a Next.js App Router API route"
  - "reject replayed webhook events older than 5 minutes"
anti_examples:
  - "process the Stripe payment_intent.succeeded event payload"
  - "call the Stripe API to create a payment intent"
  - "validate a generic HTTP signature that is not from Stripe"
relations:
  boundary:
    - skill: payment-provider-router
      reason: "payment-provider-router decides which downstream handler receives the verified event; this skill verifies authenticity before any routing happens"
    - skill: nextjs-server-action-validation
      reason: "nextjs-server-action-validation validates user-submitted form input via Zod; this skill validates Stripe's HMAC signature — different trust boundary, different mechanism"
  depends_on:
    - skill: postgres-rls-pattern
      reason: "idempotency key lookups that prevent double-processing run inside the RLS-scoped query layer; this skill activates before those lookups"
  verify_with:
    - nextjs-server-action-validation
portability:
  readiness: portable
  targets:
    - skill-md
lifecycle:
  stale_after_days: 90
  review_cadence: quarterly
---

# Stripe Webhook Signature Verification

## Coverage

- The raw-body requirement — why `stripe.webhooks.constructEvent()` requires the unparsed `Buffer` from the request body, and how Next.js App Router routes expose it via `request.arrayBuffer()`
- HMAC-SHA256 verification — how `constructEvent(rawBody, signature, secret)` reconstructs and compares the Stripe signature internally
- Replay protection — the 300-second tolerance window Stripe checks against the `t=` timestamp embedded in the `stripe-signature` header; when to tighten it
- Environment-specific secrets — `STRIPE_WEBHOOK_SECRET` for production vs `whsec_...` from the Stripe CLI `--forward-to` session in development; why they must never be swapped
- Idempotency key pattern — recording the `event.id` in Postgres before processing so a retried delivery does not double-charge or double-fulfill

## Philosophy

A webhook that skips signature verification is an unauthenticated public endpoint that can trigger payment processing. The verification step is load-bearing security, not a convenience check. Stripe's SDK makes verification a single call, but two failure modes are common in practice: the request body gets parsed (by a body-parser middleware) before the raw bytes reach the verification call, which silently corrupts the HMAC comparison; and the wrong webhook secret is loaded from environment variables, producing a 400 that is hard to distinguish from a replay rejection. Both failures look the same to the caller — a rejected webhook — and both are invisible until a real event is dropped.

## Verification

1. **Confirm raw body access.** In Next.js App Router: `const rawBody = Buffer.from(await request.arrayBuffer())`. Do NOT pass `await request.json()` or `await request.text()` — both transform the bytes.

2. **Retrieve and verify.**

   ```typescript
   import Stripe from "stripe";
   const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

   const sig = request.headers.get("stripe-signature") ?? "";
   let event: Stripe.Event;
   try {
     event = stripe.webhooks.constructEvent(
       rawBody,
       sig,
       process.env.STRIPE_WEBHOOK_SECRET!
     );
   } catch (err) {
     return Response.json({ error: "Signature verification failed" }, { status: 400 });
   }
   ```

3. **Check idempotency before processing.**

   ```sql
   INSERT INTO webhook_events (event_id, processed_at)
   VALUES ($1, now())
   ON CONFLICT (event_id) DO NOTHING
   RETURNING event_id;
   ```

   If the `RETURNING` clause returns no rows, the event was already processed — return 200 immediately without re-running side effects.

4. **Route the verified event** to `payment-provider-router`.

## Failure Mode Reference

| Failure | Symptom | Fix |
|---------|---------|-----|
| Body parsed before verification | 400 on every real Stripe event | Use `arrayBuffer()`, not `json()` or `text()` |
| Wrong webhook secret | 400 with "No signatures found matching the expected signature" | Verify `STRIPE_WEBHOOK_SECRET` matches the endpoint in the Stripe dashboard |
| Replay attack | 400 with "Timestamp too old" | Legitimate if tolerance is tight; check `t=` value in the `stripe-signature` header |
| Secret from wrong environment | Events verify in dev but fail in production | Use per-environment secrets; never share between environments |

## Do NOT Use When

| Use instead | When |
|---|---|
| `payment-provider-router` | You have a verified event and need to decide which handler processes it |
| `nextjs-server-action-validation` | You are validating user-submitted form data, not a Stripe webhook |
| (a generic HTTP signature skill) | You are verifying webhooks from a non-Stripe provider with a different signing scheme |
