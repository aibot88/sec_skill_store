---
name: fastify-production
description: >
  This skill should be used when deploying Fastify to production, configuring Fastify security headers, setting up reverse proxy with Fastify, implementing graceful shutdown, configuring @fastify/helmet, @fastify/cors, @fastify/rate-limit, trustProxy settings, Kubernetes Fastify deployment, Fastify performance tuning, request timeouts, handler timeouts, return503OnClosing, prototype poisoning protection, production Fastify checklist, or hardening Fastify server.
---

# Fastify Production Hardening

When helping a user prepare a Fastify application for production, follow every section below. These are non-negotiable requirements for a production-grade Fastify deployment. Do not skip sections. If the user's codebase is missing any of these, flag it explicitly and provide the fix.

## Reverse Proxy (Non-Negotiable)

NEVER allow a Fastify server to be exposed directly to the internet. This is an explicit anti-pattern called out by the Fastify team themselves. ALWAYS deploy Fastify behind a reverse proxy such as Nginx, HAProxy, AWS ALB, GCP Load Balancer, or Cloudflare.

The reverse proxy is responsible for:

- **TLS termination** -- Node.js is significantly less efficient at encryption than dedicated proxy software. Offloading TLS to the proxy frees the event loop for request handling.
- **Static file serving** -- serve assets from the proxy layer, not from Fastify.
- **Load balancing** -- distribute traffic across multiple Fastify instances.
- **Connection management** -- handle keep-alive, timeouts, and slow clients at the proxy layer.

When Fastify runs behind a proxy, configure `trustProxy` so that `request.ip` and `request.hostname` resolve correctly from forwarded headers:

```javascript
const app = fastify({
  trustProxy: true // trusts all proxies
})

// Or be specific with IP/CIDR:
const app = fastify({
  trustProxy: '10.0.0.0/8'
})
```

Without `trustProxy`, the `X-Forwarded-For`, `X-Forwarded-Host`, and `X-Forwarded-Proto` headers can be spoofed by any client. Always set this when behind a proxy. Never set it when not behind a proxy.

## Security Headers & Plugins

### @fastify/helmet (Required)

Register `@fastify/helmet` on every production Fastify instance. It sets critical security headers including `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, `Strict-Transport-Security`, and others.

Register it early, before any route definitions, so that headers apply to all responses including error responses:

```javascript
import helmet from '@fastify/helmet'

await app.register(helmet, {
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", 'data:'],
    },
  },
})
```

Customize the CSP directives to match the application's actual needs. The defaults are strict -- adjust only what is necessary.

### @fastify/cors

Configure CORS with explicit allowed origins, methods, and headers. Never use `origin: '*'` when credentials are involved -- browsers will reject the response and the combination is a security risk:

```javascript
import cors from '@fastify/cors'

await app.register(cors, {
  origin: ['https://app.example.com', 'https://admin.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  credentials: true,
  allowedHeaders: ['Content-Type', 'Authorization'],
})
```

For APIs that genuinely need public access without credentials, `origin: true` (reflect the request origin) is acceptable but document why.

### @fastify/rate-limit

Protect every production Fastify server against brute-force attacks and denial-of-service with `@fastify/rate-limit`. Configure it globally or per-route:

```javascript
import rateLimit from '@fastify/rate-limit'

await app.register(rateLimit, {
  max: 100,
  timeWindow: '1 minute',
  // For distributed deployments, use Redis:
  // redis: redisClient,
})

// Per-route override for sensitive endpoints:
app.post('/login', {
  config: {
    rateLimit: {
      max: 5,
      timeWindow: '5 minutes',
    },
  },
}, loginHandler)
```

When running multiple Fastify instances (horizontal scaling, Kubernetes pods), you MUST use a Redis store for rate limiting. Without it, each instance tracks limits independently, effectively multiplying the allowed request rate by the number of instances.

## Prototype Poisoning Protection

Fastify has built-in protection against JSON prototype poisoning via two server options: `onProtoPoisoning` and `onConstructorPoisoning`. These guard against malicious JSON payloads that include `__proto__` or `constructor` properties to pollute object prototypes.

KEEP the defaults at `'error'` (which rejects the request) or set to `'remove'` (which strips the dangerous properties). NEVER set these to `'ignore'` -- doing so disables protection and opens the application to prototype pollution attacks:

```javascript
const app = fastify({
  onProtoPoisoning: 'error',       // default -- keep it
  onConstructorPoisoning: 'error', // default -- keep it
})
```

If the user has set either to `'ignore'`, flag it as a critical security issue and change it immediately.

## Graceful Shutdown

### return503OnClosing (Critical)

You MUST enable `return503OnClosing: true` in the Fastify server options. This is essential for zero-downtime deployments:

```javascript
const app = fastify({
  return503OnClosing: true,
})
```

When `fastify.close()` is called, the server immediately begins rejecting new incoming requests with a `503 Service Unavailable` status and a `Connection: close` header. This signals the load balancer to stop routing traffic to this instance while in-flight requests finish draining. Without this, the load balancer continues sending requests to a shutting-down instance, causing user-facing errors.

### Resource Cleanup

Use the `onClose` hook to release database connection pools, file handles, message queue connections, and any other resources that need explicit cleanup:

```javascript
app.addHook('onClose', async (instance) => {
  await instance.pg.pool.end()       // close database pool
  await instance.redis.quit()         // close Redis connection
  await instance.amqp.close()         // close message queue
})
```

The `onClose` hooks execute in REVERSE order of registration. Child plugins close before parent plugins. This ensures dependent resources shut down before the resources they depend on.

### Signal Handling

Implement signal handlers for `SIGINT` (Ctrl+C) and `SIGTERM` (container orchestrator stop signal) to trigger graceful shutdown:

```javascript
const signals = ['SIGINT', 'SIGTERM']
signals.forEach(signal => {
  process.on(signal, async () => {
    await app.close()
    process.exit(0)
  })
})
```

In Kubernetes, `SIGTERM` is sent when a pod is being terminated. The pod gets a grace period (default 30 seconds) to finish in-flight requests before `SIGKILL`. Make sure your shutdown completes within this window.

## Timeouts

Configure both request and handler timeouts to protect against slow clients and runaway business logic:

- **`requestTimeout`** -- the maximum time allowed for the client to send the complete request (headers + body). This protects against slowloris attacks where a client sends data extremely slowly to hold connections open:

```javascript
const app = fastify({
  requestTimeout: 30000, // 30 seconds
})
```

- **`handlerTimeout`** -- the maximum time allowed for your route handler to produce a response. When this fires, Fastify responds with a 503 and the handler can use `request.signal` (an `AbortSignal`) to cooperatively cancel in-progress work:

```javascript
const app = fastify({
  handlerTimeout: 60000, // 60 seconds
})

// Cooperative cancellation in handlers:
app.get('/data', async (request, reply) => {
  const result = await db.query('SELECT ...', {
    signal: request.signal, // cancel query if timeout fires
  })
  return result
})
```

Always set both timeouts. The defaults may be too generous for your use case. Tune them based on your application's expected response times.

## Performance

### The "2 vCPU" Rule

Allocate 2 vCPUs per Fastify application instance (per Kubernetes pod). One thread handles main JavaScript execution while the second handles V8 garbage collection and the libuv threadpool (DNS lookups, filesystem operations, native crypto). This configuration yields the lowest possible latency because GC pauses do not compete with request handling for CPU time.

If you are writing Kubernetes resource requests, set:

```yaml
resources:
  requests:
    cpu: "2"
    memory: "512Mi"
  limits:
    cpu: "2"
    memory: "1Gi"
```

Scale horizontally by adding more pods rather than giving more CPU to a single pod.

### Response Schemas

ALWAYS define response schemas on every route. This is one of the most impactful performance optimizations in Fastify. When a response schema is defined, Fastify uses `fast-json-stringify` to JIT-compile a serializer specific to that schema. This is 2-3x faster than native `JSON.stringify`.

```javascript
app.get('/users/:id', {
  schema: {
    response: {
      200: {
        type: 'object',
        properties: {
          id: { type: 'integer' },
          name: { type: 'string' },
          email: { type: 'string' },
        },
      },
    },
  },
}, handler)
```

Without response schemas, Fastify falls back to `JSON.stringify`, and you lose one of the framework's primary performance advantages. If the user has routes without response schemas, flag every one of them.

### Ajv allErrors

KEEP `allErrors: false` in production (this is the default). Setting `allErrors: true` instructs Ajv to collect every validation error instead of stopping at the first one. This enables a denial-of-service vector where algorithmically complex payloads cause Ajv to spend excessive time evaluating all possible error paths:

```javascript
// DO NOT do this in production:
const app = fastify({
  ajv: {
    customOptions: {
      allErrors: true, // DoS risk -- remove this
    },
  },
})
```

If the user has `allErrors: true`, change it to `false` and explain the DoS risk.

## Kubernetes Deployment

When deploying Fastify in containers (Docker, Kubernetes, ECS), you MUST bind to `0.0.0.0` instead of the default `127.0.0.1`. The default loopback address is unreachable from outside the container:

```javascript
await app.listen({ port: 3000, host: '0.0.0.0' })
```

Configure readiness and liveness probes to monitor the Fastify instance:

```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 10

livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 15
  periodSeconds: 20
```

With `return503OnClosing: true`, the readiness probe automatically fails when the server begins shutting down, causing Kubernetes to remove the pod from the service endpoints before it terminates. This is how you achieve zero-downtime rolling updates.

## Error Handling in Production

Set a global error handler with `setErrorHandler` to intercept all errors. The handler must distinguish between client errors (4xx) and server errors (5xx):

```javascript
app.setErrorHandler((error, request, reply) => {
  // Validation errors (400)
  if (error.validation) {
    return reply.status(400).send({
      error: 'Validation Error',
      message: error.message,
    })
  }

  // All other errors -- mask internals
  request.log.error(error)
  return reply.status(500).send({
    error: 'Internal Server Error',
    message: 'An unexpected error occurred',
  })
})
```

For 400-level errors, return clean validation messages that help the client fix their request. For 500-level errors, NEVER leak stack traces, internal error messages, database details, or file paths. Log the full error server-side and return a generic message to the client.

Use `pino.final` for fatal errors that should crash the process. Never swallow `uncaughtException` or `unhandledRejection` -- log them and exit:

```javascript
import pino from 'pino'

const logger = pino()

process.on('uncaughtException', pino.final(logger, (err, finalLogger) => {
  finalLogger.error(err, 'uncaughtException')
  process.exit(1)
}))

process.on('unhandledRejection', pino.final(logger, (err, finalLogger) => {
  finalLogger.error(err, 'unhandledRejection')
  process.exit(1)
}))
```

## Production Checklist

Before any Fastify application goes to production, verify every item on this checklist. If any item is missing, it is a blocker:

1. **Behind reverse proxy** -- Nginx, HAProxy, ALB, or equivalent. Fastify is never internet-facing.
2. **trustProxy configured** -- set to `true` or specific CIDR matching your proxy infrastructure.
3. **@fastify/helmet registered** -- with a customized Content-Security-Policy.
4. **@fastify/cors with explicit origins** -- never `origin: '*'` with credentials.
5. **@fastify/rate-limit active** -- global and per-route for sensitive endpoints. Redis store for multi-instance.
6. **Response schemas on all routes** -- enables fast-json-stringify for 2-3x serialization speedup.
7. **allErrors: false in Ajv** -- the default. Never enable in production.
8. **Pino logging with redaction** -- redact sensitive fields (passwords, tokens, PII) from logs.
9. **Async logging (sync: false)** -- prevent logging from blocking the event loop.
10. **return503OnClosing: true** -- reject new requests during shutdown for clean load balancer draining.
11. **Graceful shutdown with signal handlers** -- handle SIGINT and SIGTERM, call `app.close()`.
12. **Request and handler timeouts set** -- protect against slow clients and runaway handlers.
13. **onProtoPoisoning: 'error'** -- keep the default, never set to 'ignore'.
14. **Bind to 0.0.0.0 in containers** -- the default 127.0.0.1 is unreachable from outside the container.

Walk through this checklist with the user. For each item, check the codebase and report whether it passes or needs remediation. Provide the exact code fix for every failing item.
