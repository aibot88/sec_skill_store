---
name: stripe-webhook-security
description: >
  This skill should be used when implementing security for Stripe webhook endpoints, handling
  "webhook rate limiting", "Stripe secret management", "webhook abuse prevention",
  "log redaction for billing", "STRIPE_WEBHOOK_SECRET storage", "webhook endpoint protection",
  "Stripe API key security", "billing security review", "sensitive data in logs",
  "production webhook hardening", "DDoS protection for webhooks", or when the user asks about
  securing Stripe webhook endpoints and billing infrastructure in Fastify.
---

# Stripe Webhook Security

## Security Boundaries

Webhook endpoints face unique security challenges: they receive POST requests from the public internet, process financial data, and must be available 24/7. Every layer must be hardened.

## Signature Verification Is the Firewall

The `Stripe-Signature` header + raw body HMAC check is the primary security boundary. Without it, any attacker can forge webhook events and manipulate subscription state.

**Hard rules:**
- Verify the signature on EVERY webhook request, no exceptions
- Use the **raw, unparsed body** — never the JSON-parsed result
- Use the correct webhook signing secret (`whsec_...`), not the API key (`sk_...`)
- Reject requests missing the `stripe-signature` header with `400`
- Log failed verification attempts (without exposing the secret or raw body)

```typescript
try {
  event = stripe.webhooks.constructEvent(rawBody, sig, env.STRIPE_WEBHOOK_SECRET);
} catch (err) {
  // Log warning — NEVER log the secret, raw body, or full signature
  request.log.warn({ error: (err as Error).message }, 'Webhook signature failed');
  return reply.status(400).send({ error: 'Invalid signature' });
}
```

## Rate Limiting

Apply layered rate limits using `@fastify/rate-limit`:

### Global Rate Limit

```typescript
fastify.register(rateLimitPlugin, {
  max: 1000,
  timeWindow: '1 minute',
});
```

### Webhook-Specific Rate Limit

Stripe can burst webhook deliveries during batch operations. Set webhook limits higher than API limits but still bounded:

```typescript
fastify.register(async function webhookContext(instance) {
  instance.register(rateLimitPlugin, {
    max: 500,
    timeWindow: '1 minute',
    keyGenerator: () => 'stripe-webhooks', // Single bucket for all webhook traffic
  });

  instance.post('/stripe', stripeWebhookHandler);
}, { prefix: '/webhooks' });
```

### Authentication Endpoint Rate Limit

```typescript
// Prevent brute-force credential stuffing
fastify.register(rateLimitPlugin, {
  max: 5,
  timeWindow: '1 minute',
  keyGenerator: (request) => request.ip,
  routeConfig: { rateLimit: { max: 5 } },
});
```

### 404 Rate Limit

```typescript
// Prevent automated scanning for valid routes
fastify.setNotFoundHandler({
  preHandler: fastify.rateLimit({ max: 10, timeWindow: '1 minute' }),
}, (request, reply) => {
  reply.status(404).send({ error: 'Not found' });
});
```

## Secret Management

### Secrets That Must Never Leave the Server

| Secret | Format | Storage |
|--------|--------|---------|
| `STRIPE_SECRET_KEY` | `sk_live_...` or `sk_test_...` | Environment variable only |
| `STRIPE_WEBHOOK_SECRET` | `whsec_...` | Environment variable only |
| `JWT_SECRET` (symmetric) | 32+ character string | Environment variable only |
| JWT private key (asymmetric) | PEM file | Environment variable or mounted secret |
| `DATABASE_URL` | Connection string | Environment variable only |

### Validation at Startup

Validate all secrets exist and have the correct format before the application starts. See the `stripe-zod-contracts` skill for the full `envSchema` definition. The key principle: fail fast — do not start the server with missing or malformed secrets. Use Zod's `regex` and `startsWith` validators to enforce format (`sk_test_`, `whsec_`, etc.).
```

### What Must Never Be Committed

- `.env` files containing real secrets
- Stripe API keys in source code
- Webhook signing secrets in configuration files
- JWT private keys in the repository

Add to `.gitignore`:
```
.env
.env.*
!.env.example
```

Provide `.env.example` with placeholder values for documentation.

## Log Redaction

### What to Redact

- Stack traces in production (expose internal paths)
- JWT token values in authentication logs
- Stripe customer IDs in public-facing error messages
- Full webhook payloads (may contain PII)
- Internal database IDs in API responses

### Pino Logger Configuration

```typescript
const fastify = Fastify({
  logger: {
    level: process.env.NODE_ENV === 'production' ? 'info' : 'debug',
    redact: {
      paths: [
        'req.headers.authorization',
        'req.headers["stripe-signature"]',
        'req.body.card',
        'req.body.email',
      ],
      censor: '[REDACTED]',
    },
  },
});
```

### Response Schema as Security Filter

Use Fastify response schemas to automatically strip internal fields:

```typescript
const subscriptionResponseSchema = z.object({
  id: z.string(),
  planName: z.string(),
  status: z.string(),
  currentPeriodEnd: z.number(),
  // Internal fields like stripe_customer_id are NOT in this schema
  // — Fastify's serializer automatically excludes them
});
```

## Webhook Endpoint Isolation

Register webhook routes in a separate Fastify plugin context:

1. **No JWT authentication** — webhooks authenticate via Stripe signature, not JWT
2. **No CORS** — webhooks are server-to-server, browsers never call them
3. **Custom body parser** — raw body preservation instead of JSON parsing
4. **Separate rate limits** — higher limits than user-facing API

```typescript
// Root application
fastify.register(corsPlugin);          // CORS for browser clients
fastify.register(jwtAuthPlugin);       // JWT for API routes
fastify.register(billingApiRoutes);    // Protected billing API

// Isolated webhook context — no CORS, no JWT, custom parser
fastify.register(webhookRoutes, { prefix: '/webhooks' });
```

## Abuse Prevention Checklist

- [ ] Stripe signature verification on every webhook request
- [ ] Rate limiting on webhook endpoints
- [ ] Rate limiting on authentication endpoints
- [ ] All secrets validated at startup with Zod
- [ ] No secrets in source control
- [ ] Log redaction configured for production
- [ ] Response schemas strip internal fields
- [ ] Webhook routes isolated from API routes
- [ ] Error responses do not expose internal details
- [ ] Failed verification logged without sensitive data

## Related Skills

- **stripe-zod-contracts** — For the full `envSchema` with all secret format validators
- **stripe-webhook-handling** — For signature verification implementation details
- **stripe-webhook-best-practices** — For the complete 5-rule framework
