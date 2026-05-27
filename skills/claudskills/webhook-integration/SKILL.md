---
name: webhook-integration
description: "Use when implementing or reviewing an inbound webhook handler for any third-party provider - verifying signatures, deduplicating retries, choosing the right HTTP status code for retry vs no-retry, persisting raw payloads before canonical mapping, and quarantining unverifiable events. Covers signature schemes, idempotency patterns, provider retry contracts, raw-then-canonical pipelines, quarantine, secret rotation, and PII-capture timing. Do NOT use for outbound webhook publishing (use `event-contract-design`), general background-job orchestration, or chasing a webhook handler that has already failed in production (use `debugging`)."
license: MIT
compatibility: "Provider-agnostic. Examples reference HMAC-SHA256 (the dominant scheme), SDK-style verification helpers (Stripe-style, where the provider ships a library that takes raw body + header + secret), and round-trip verification APIs (PayPal-style, where the receiver POSTs the event back to the provider for validation). Substitute each provider's specific header names, hashing algorithm, and retry-status-code contract from their docs."
allowed-tools: Read Grep Bash Edit
metadata:
  schema_version: "4"
  version: "1.0.0"
  type: capability
  category: engineering
  domain: integrations/webhooks
  scope: portable
  owner: skill-graph-maintainer
  freshness: "2026-05-06"
  drift_check: "{\"last_verified\":\"2026-05-06\"}"
  eval_artifacts: present
  eval_state: unverified
  routing_eval: absent
  stability: experimental
  keywords: "[\"webhook handler\",\"webhook signature\",\"webhook signature verification\",\"HMAC webhook\",\"timing-safe comparison\",\"duplicate webhook delivery\",\"webhook idempotency\",\"idempotency key\",\"webhook retry\",\"retry contract\",\"webhook 200 vs 500\",\"replay attack webhook\",\"webhook quarantine\",\"raw payload archive\",\"webhook canonical mapping\",\"PII capture window\",\"webhook secret rotation\",\"inbound event handler\"]"
  examples: "[\"implement signature verification for a new third-party webhook handler\",\"the same webhook event is being processed twice — fix the idempotency\",\"should I return 200 or 500 when a webhook handler hits a database error?\",\"the provider keeps retrying a webhook we already accepted — what's wrong with our 200 path?\",\"design a quarantine path for webhooks that fail signature verification\",\"extract a stable idempotency key from this provider's webhook payload\",\"reject all webhook deliveries with an invalid HMAC, log them for audit\",\"the provider deletes customer data 30 days after order — how do I capture PII safely on first delivery?\"]"
  anti_examples: "[\"design our outbound webhook product (we want to deliver events to customers)\",\"the production webhook is failing — find the root cause\",\"explain our webhook patterns in the contributor docs\",\"review this AI-generated webhook handler for correctness\",\"refactor the webhook handler helpers for clarity\",\"decide whether this webhook needs an integration test\",\"design the secret-rotation policy for our integration credentials\"]"
  relations: "{\"boundary\":[{\"skill\":\"documentation\",\"reason\":\"documentation produces durable prose about integration patterns; webhook-integration produces the executable handler skeleton and verification path\"},{\"skill\":\"event-contract-design\",\"reason\":\"event-contract-design owns outbound event and webhook contracts; webhook-integration owns inbound third-party handler mechanics\"},{\"skill\":\"debugging\",\"reason\":\"debugging chases an observed handler failure with reproduction; webhook-integration plans the safe handler shape before deployment\"},{\"skill\":\"refactor\",\"reason\":\"refactor is behavior-preserving cleanup; webhook-integration is the contract-enforcement layer that decides what behavior the handler must preserve\"},{\"skill\":\"owasp-security\",\"reason\":\"owasp-security owns the secret-storage and rotation policy; webhook-integration owns the per-request signature-verification mechanics that consume those secrets\"},{\"skill\":\"testing-strategy\",\"reason\":\"testing-strategy decides what deserves a regression test; webhook-integration defines the failure modes (replay, signature mismatch, duplicate delivery) those tests target\"}],\"related\":[\"testing-strategy\",\"debugging\",\"documentation\",\"owasp-security\",\"code-review\",\"event-contract-design\"],\"verify_with\":[\"testing-strategy\",\"code-review\"]}"
  portability: "{\"readiness\":\"scripted\",\"targets\":[\"skill-md\"]}"
  lifecycle: "{\"stale_after_days\":90,\"review_cadence\":\"quarterly\"}"
  skill_graph_source_repo: "https://github.com/jacob-balslev/skill-graph"
  skill_graph_protocol: Skill Metadata Protocol v3
  skill_graph_project: Skill Graph
  skill_graph_canonical_skill: skills/webhook-integration/SKILL.md
---

# Webhook Integration

## Coverage

- The three signature-scheme families: shared-secret HMAC (dominant), provider-SDK verification helpers, and round-trip verification APIs — what each looks like, when each is used, and how to verify correctly
- The four idempotency patterns: processed-flag, payload-hash UPSERT, event-ID deduplication, composite-key UPSERT — and the selection rule for picking the right one for a given provider
- The retry-contract reading discipline: every provider has a documented (or undocumented) policy for how it interprets 4xx vs 5xx; the wrong status code on a duplicate or transient error silently loses events
- The raw-then-canonical pipeline: persist the raw payload before any mapping, so downstream bugs in canonical conversion never lose original data
- Quarantine for unverifiable events: where to put webhooks that fail signature verification or schema validation, and how to keep them auditable without polluting the main pipeline
- PII-capture timing: when a provider has a deletion window (GDPR-driven, often 30 days), the first webhook is the only reliable opportunity to persist customer data
- Webhook handler skeleton: the standard ordering of verify → parse → dedupe → process → respond, and why each step must precede the next
- Secret rotation hooks: the handler-side support for accepting both old and new secrets during a rotation window, without owning the rotation policy itself

## Philosophy

Webhooks are the primary real-time data ingestion channel for any application that integrates with third-party providers. When a webhook handler is wrong, the failure mode is *silent data loss* — events arrive, the handler returns the wrong status code, the provider stops retrying, and the data is gone with no error in your logs. There is no "exception thrown" symptom. The discipline is to treat the handler as a contract negotiation: the provider's retry policy is law, the signature scheme is law, and the handler's job is to honour both *exactly*, not approximately.

The dominant misconception is that REST conventions ("4xx for client error, 5xx for server error") apply uniformly. They do not. Several major providers interpret *any* 4xx as "your endpoint is permanently broken, stop retrying" — including a `409 Conflict` returned for a duplicate delivery, which is the natural REST-ish response. The result: returning a "semantically correct" 409 for a duplicate Stripe-style or HMAC-style webhook ends the retry loop on the *first* duplicate and silently drops every subsequent attempt. The right response for a duplicate is `200 OK` (with a body indicating it was already processed) — telling the provider "we have it, you can stop." For a transient database error, the right response is `500` — telling the provider "retry me." Neither is the REST default.

The second hard problem is timing. Most providers retry on a backoff schedule (one minute, ten minutes, an hour, a day), and most have a deadline beyond which they give up. If your handler does heavy work synchronously (calling third-party APIs, generating PDFs, sending email), the handler can time out, the provider sees a 504 from your gateway, and you start drifting through the retry budget without ever processing the event correctly. The discipline: verify, dedupe, persist the raw payload, return 200 fast, and dispatch the heavy work to a background queue that can fail and retry on its own schedule.

The third trap is forgetting that signature verification *must* run on the raw bytes of the request body, not on a parsed-and-re-serialized version. The moment you parse JSON and re-serialize it, you introduce whitespace and key-ordering changes that make the HMAC mismatch. Capture the raw body first, verify, then parse — never the other way around.

## Webhook Handler Skeleton

Every webhook handler should follow this exact ordering. Steps cannot be reordered without breaking either correctness or the retry contract.

```typescript
export async function POST(req: Request) {
  // 1. Read the RAW body — bytes as delivered, before any parsing
  const rawBody = await req.text();

  // 2. Verify signature against the raw body
  const signature = req.headers.get('x-provider-signature') ?? '';
  if (!verifyProviderSignature(rawBody, signature, providerSecret)) {
    // Quarantine for audit, then return permanent failure
    await quarantineUnverifiableEvent(rawBody, signature, 'signature_mismatch');
    return jsonResponse(401, { error: 'invalid_signature' });
  }

  // 3. Parse the body now that it has been verified
  let event;
  try {
    event = JSON.parse(rawBody);
  } catch {
    return jsonResponse(400, { error: 'malformed_json' });
  }

  // 4. Idempotency check — extract a stable key, dedupe
  const idempotencyKey = extractIdempotencyKey(req, event);
  if (await isAlreadyProcessed(idempotencyKey)) {
    return jsonResponse(200, { ok: true, skipped: true, reason: 'already_processed' });
  }

  // 5. Persist the raw payload BEFORE any canonical mapping
  await persistRawEvent({ idempotencyKey, body: rawBody, receivedAt: new Date() });

  // 6. Dispatch heavy work to a background queue; do not block the response
  await enqueueEventProcessing({ idempotencyKey, event });

  // 7. Mark processed and return 200 fast
  await markProcessed(idempotencyKey);
  return jsonResponse(200, { ok: true, received: true });
}
```

Every step in this skeleton is load-bearing. Skipping signature verification opens the endpoint to forged events; parsing before verifying breaks signature correctness; processing synchronously blocks the response and risks timeouts; not persisting the raw body first means a bug in canonical mapping silently destroys the original data.

## Signature Schemes

There are three families. Identify which one your provider uses before writing a single line of handler code; verifying the wrong way fails open in subtle ways.

### Family 1: Shared-Secret HMAC (most common)

The provider sends a header containing an HMAC of the raw body, computed with a secret you both know. You recompute the HMAC and compare in constant time.

```typescript
import { createHmac, timingSafeEqual } from 'crypto';

function verifyHmacSha256(rawBody: string, signatureHeader: string, secret: string): boolean {
  if (!signatureHeader || !secret) return false;

  // Some providers prefix the hex signature with "sha256=" — strip if present
  const expectedHex = signatureHeader.replace(/^sha256=/i, '');

  const computedHex = createHmac('sha256', secret)
    .update(rawBody, 'utf8')
    .digest('hex');

  // Buffers must be equal length for timingSafeEqual; bail early if not
  if (expectedHex.length !== computedHex.length) return false;

  return timingSafeEqual(
    Buffer.from(expectedHex, 'hex'),
    Buffer.from(computedHex, 'hex')
  );
}
```

Critical details:

- **Constant-time comparison.** A naive `===` leaks the signature length and prefix via response timing, enabling a forge-by-timing attack. Always use `timingSafeEqual` (Node) or its equivalent.
- **Hash algorithm.** Most providers use HMAC-SHA256. A few still use HMAC-SHA1 (legacy GitHub) or HMAC-SHA512. Match the algorithm in the docs exactly — using SHA-1 against an SHA-256 signature looks like a mismatch.
- **Encoding.** Some providers send hex; others send base64. Decode according to the docs, not a guess.
- **Header prefix.** GitHub uses `sha256=<hex>`; Shopify uses bare base64; Slack uses `v0=<hex>`. Read the docs and strip exactly what the provider sends.
- **Body encoding.** The HMAC is over the *bytes* of the request body. If your framework auto-parses JSON before you can grab the raw body, the verification will fail because re-serialized JSON differs from the original bytes.

### Family 2: Provider SDK Verification (Stripe-style)

Some providers ship a verification function in their SDK that takes the raw body, the header, and the secret, and returns either a parsed event object or throws. Use the SDK call directly — do not reimplement.

```typescript
// Pseudocode shape — substitute the actual SDK import for your provider
import { providerSdk } from 'provider-sdk';

let event;
try {
  event = providerSdk.webhooks.constructEvent(rawBody, signatureHeader, secret);
} catch (err) {
  await quarantineUnverifiableEvent(rawBody, signatureHeader, 'sdk_construct_failed');
  return jsonResponse(401, { error: 'invalid_signature' });
}

// `event` is now both verified AND parsed — proceed to idempotency
```

The SDK form is the safer default when available because it encapsulates timestamp tolerance (rejecting replays older than N minutes), version checks, and the exact algorithm + encoding combination.

### Family 3: Round-Trip Verification API (PayPal-style)

A few providers do not give you a secret. Instead, on receiving a webhook, you POST a subset of the headers and the body back to a verification endpoint, and they return a yes/no.

```typescript
const verification = await fetch(`${providerBaseUrl}/v1/notifications/verify-webhook-signature`, {
  method: 'POST',
  headers: { Authorization: `Bearer ${oauthToken}`, 'Content-Type': 'application/json' },
  body: JSON.stringify({
    auth_algo:        req.headers.get('auth-algo'),
    cert_url:         req.headers.get('cert-url'),
    transmission_id:  req.headers.get('transmission-id'),
    transmission_sig: req.headers.get('transmission-sig'),
    transmission_time: req.headers.get('transmission-time'),
    webhook_id:       providerWebhookId,
    webhook_event:    JSON.parse(rawBody),
  }),
});

const { verification_status } = await verification.json();
if (verification_status !== 'SUCCESS') {
  await quarantineUnverifiableEvent(rawBody, '<round-trip>', 'verification_api_rejected');
  return jsonResponse(401, { error: 'invalid_signature' });
}
```

Round-trip verification adds a network hop and an external dependency to the hot path. If the provider's verification API is degraded, your webhook endpoint is degraded too. Plan accordingly: a short timeout on the verification call, a quarantine path for verification timeouts, and a circuit breaker if the verification endpoint is consistently slow.

## Idempotency Patterns

Duplicate delivery is *normal*, not an error. Every provider retries on transient failures, and you will see the same event twice, ten times, or hundreds of times during a network blip. The handler must dedupe.

Pick one of these four patterns based on what the provider's payload gives you:

| Pattern | When to use | How |
|---|---|---|
| **Processed-flag** | Provider gives you a stable event ID and you want to record per-event metadata | Insert event with `processed_at = NULL`; on second delivery, check `processed_at` is non-null and return 200 skipped |
| **Payload-hash UPSERT** | Provider gives you no stable ID, but the same logical event always serializes identically | Compute SHA-256 of canonical payload; UPSERT with `ON CONFLICT (hash) DO NOTHING`; affected-rows = 0 means duplicate |
| **Event-ID dedup** | Provider gives a UUID per delivery; you only need to know it was seen | Track in a small `seen_event_ids (id, received_at)` table with a TTL of (provider's retry window + buffer) |
| **Composite-key UPSERT** | Same logical entity arrives across multiple providers | UPSERT on `(source_provider, external_id)` so each provider has its own idempotent slot |

The processed-flag and event-ID-dedup patterns are the cleanest for new handlers. Reach for payload-hash only when the provider gives you no ID at all (rare on modern APIs).

A worked example of processed-flag for a provider that ships a stable `event.id`:

```sql
-- Idempotent insert: returns true if this is the first time we have seen this event
INSERT INTO inbound_events (provider, event_id, raw_payload, received_at)
VALUES ($1, $2, $3, NOW())
ON CONFLICT (provider, event_id) DO NOTHING
RETURNING id;
```

If `RETURNING id` produces no row, the event was already inserted and you can return `200 { skipped: true }` immediately without re-running any side effects.

## Retry Contract Per Provider

This is the part agents get wrong most often. There is no universal answer; every provider has a documented retry policy and you must read each one and write it down before implementing the handler.

The questions to answer for each provider:

| Question | Why it matters |
|---|---|
| Which response codes trigger a retry? | Determines the right code for transient errors — usually `5xx`, sometimes `429`, occasionally specific codes only |
| Which response codes are treated as permanent failure? | Tells you the code for duplicates and bad payloads — usually `4xx`, but the *threshold* matters: some providers retry on `408` and `429` while treating `400-407` as permanent |
| What is the retry schedule? | Tells you how long the deduplication window must remain valid (a provider that retries for 24 hours requires 24 hours of seen-ID retention plus a buffer) |
| What is the request timeout? | Tells you how fast the handler must return; usually 5-30 seconds |
| Does the provider sign retried deliveries with the original timestamp or a fresh one? | Some signature schemes embed a timestamp; if retries use a fresh timestamp, replay protection at the receiver must be tolerant |

A worked example of writing this down for a hypothetical provider:

```
Provider: example-vendor
Retry on:        500, 502, 503, 504, 408, 429
Permanent on:    400, 401, 403, 404, 409, 410, 422
Schedule:        2m, 10m, 1h, 6h, 24h (5 retries over 32 hours)
Timeout:         15 seconds
Signature time:  fresh per retry (timestamp tolerance: 5 minutes)
```

With this in hand, the handler's response strategy is mechanical:

| Handler condition | Response |
|---|---|
| Signature mismatch | `401` (permanent — replaying a bad signature gains nothing) |
| Malformed JSON | `400` (permanent — payload will not parse on retry) |
| Already processed (duplicate) | `200` with `{ skipped: true }` — *not* `409`, which would be permanent |
| Transient DB error during processing | `500` — provider retries |
| Persisted, dispatched to background queue | `200` with `{ received: true }` — provider stops, queue owns success/failure |

Returning `409` for a duplicate against this provider would silently lose every retry of that event after the first.

## Raw-Then-Canonical Pipeline

Persist the raw payload before any conversion to your application's canonical schema. Two reasons:

1. **Bugs in canonical mapping are common.** A new field, a renamed field, or a type-coercion edge case can lose data during conversion. If you persisted only the canonical version, the original is gone and you cannot reprocess. With the raw version stored, you can re-run the canonical mapper after fixing the bug and recover the data.
2. **Audit trail.** Disputes ("we never sent that order!") are resolved by replaying the raw bytes the provider sent, signed and timestamped. A canonical-only store loses that.

```sql
CREATE TABLE inbound_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  provider TEXT NOT NULL,
  event_id TEXT NOT NULL,
  raw_payload JSONB NOT NULL,
  raw_signature TEXT,
  received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  processed_at TIMESTAMPTZ,
  UNIQUE (provider, event_id)
);
```

Canonical mapping runs *after* the raw insert succeeds, often asynchronously in a background job. If the canonical mapper fails, the raw row remains and can be replayed.

## Quarantine for Unverifiable Events

Webhooks that fail signature verification or schema validation should not silently drop. Persist them to a quarantine table with the failure reason and the original headers — both for audit (was someone trying to forge events?) and for forensics (did we change a secret without coordinating?).

```sql
CREATE TABLE quarantined_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  provider TEXT NOT NULL,
  raw_payload TEXT,
  raw_headers JSONB,
  failure_reason TEXT NOT NULL, -- 'signature_mismatch' | 'malformed_json' | 'sdk_construct_failed' | ...
  received_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

Quarantine inserts must be best-effort and never throw — if the quarantine table is unavailable, log to whatever logging your application uses and continue returning 401/400 to the provider. Do not let a quarantine failure cascade into a 500, which would trigger a retry of an event that should be permanently rejected.

## PII-Capture Timing

If a provider has a deletion window (GDPR-driven, often 30 days), the *first* webhook delivery is the only reliable opportunity to persist customer data. After the deletion window, calls to the provider's API will return redacted records.

The discipline:

- Capture all PII fields the provider includes in the webhook payload at the moment of receipt — email, phone, address, name — into your own storage, *not* a deferred "we'll fetch it later" step.
- The capture lives in the same transaction as the raw-event insert; if the insert succeeds, the PII is durably stored.
- Treat the PII as your application's data from that moment on; subsequent provider API calls cannot replace it.

This is one of the few cases where a synchronous side-effect inside the webhook handler is correct: deferring it to a background job is exactly the bug that causes data loss.

## Secret Rotation

Handlers should accept either the *current* or the *previous* secret during a rotation window. The handler does not own the rotation policy (that belongs to the security model), but it must support it:

```typescript
function verifyWithRotation(rawBody: string, sig: string, current: string, previous?: string): boolean {
  if (verifyHmacSha256(rawBody, sig, current)) return true;
  if (previous && verifyHmacSha256(rawBody, sig, previous)) return true;
  return false;
}
```

The previous secret stays valid for the provider's maximum retry window after rotation, then is removed. Without this, every rotation drops every event still in the retry queue from the old secret.

## Evals

This skill ships a comprehension-eval artifact at [`examples/evals/webhook-integration.json`](https://github.com/jacob-balslev/skill-graph/blob/main/examples/evals/webhook-integration.json). The checklist below is the authoring gate for inbound webhook-handler decisions; the eval file is the grader surface.

## Verification

- [ ] Signature verification runs on the *raw* request body, before any JSON parsing
- [ ] Comparison uses constant-time equality (`timingSafeEqual` or equivalent), not `===`
- [ ] The signature scheme matches the provider's documented algorithm, encoding, and header format exactly
- [ ] An idempotency key is extracted from each event and checked before any side effects run
- [ ] The retry-status-code table for each provider is documented in code comments or a per-provider README, not inferred
- [ ] Duplicate deliveries return `200 { skipped: true }`, never `409` or any other 4xx
- [ ] Transient errors (DB unavailable, downstream API down) return `5xx` so the provider retries
- [ ] Permanent errors (signature mismatch, malformed JSON, schema violation) return `4xx` and are quarantined
- [ ] The raw payload is persisted before canonical mapping; the canonical mapping runs in a background job
- [ ] Heavy processing is dispatched to a queue, not run synchronously in the handler
- [ ] Quarantine inserts cannot themselves throw and cascade into a 500
- [ ] If the provider has a deletion window, PII fields are captured synchronously on first delivery
- [ ] Secret rotation is supported by accepting both current and previous secrets during the rotation window
- [ ] At least one regression test simulates duplicate delivery; at least one simulates a forged signature

## Do NOT Use When

| Use instead | When |
|---|---|
| `documentation` | Writing the integration-conventions page for the contributor docs, or explaining your outbound webhook product to consumers |
| `event-contract-design` | Designing outbound webhook or async event schemas, envelopes, topics, compatibility, and consumer-facing fixtures |
| `debugging` | Chasing a webhook handler that is failing in production and reproducing the failure |
| `refactor` | Reorganizing webhook helper code or consolidating duplicated handler logic |
| `testing-strategy` | Deciding whether a particular webhook handler needs a regression test |
| `code-review` | Reviewing an AI-generated webhook handler for correctness |
| `owasp-security` | Designing the secret-storage and rotation policy itself, or auditing your application's webhook attack surface |
