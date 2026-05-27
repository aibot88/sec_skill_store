---
name: backend
description: >
  Use this skill whenever building, designing, reviewing, or debugging backend systems,
  APIs, services, or server-side architecture. Triggers include any mention of REST API
  design, GraphQL, gRPC, database design, SQL optimization, caching (Redis, Memcached),
  authentication/authorization (JWT, OAuth), message queues (Kafka, RabbitMQ), microservices,
  monolith architecture, observability (logging, metrics, tracing), rate limiting, pagination,
  error handling patterns, API versioning, background jobs, webhooks, CI/CD, Docker, or
  deployment. Also use when the user asks to "design an API", "structure a backend",
  "optimize queries", "add caching", "set up auth", "handle errors", or any server-side
  architecture question. This skill is framework-agnostic — for framework-specific guidance
  (FastAPI, Express, Django, etc.), combine this with the relevant framework skill.
  Covers production patterns for 2025–2026: API design, database architecture, caching,
  security, observability, scalability, and deployment.
---

# Backend Skill — Production Backend Engineering (2025–2026)

This skill covers framework-agnostic backend engineering principles: API design, database patterns, caching, security, observability, architecture decisions, and deployment. Combine with framework-specific skills (FastAPI, Express, Django, Spring, etc.) for implementation details.

---

## 1. API Design Fundamentals

### REST URL conventions

Resources are **nouns** (plural). HTTP methods are the **verbs**.

```
GET    /api/v1/users          # List users
POST   /api/v1/users          # Create a user
GET    /api/v1/users/123      # Get user 123
PATCH  /api/v1/users/123      # Partial update
PUT    /api/v1/users/123      # Full replace
DELETE /api/v1/users/123      # Delete user 123

GET    /api/v1/users/123/orders          # User's orders (shallow nesting)
GET    /api/v1/users/123/orders/456      # Specific order

# ❌ Anti-patterns
GET    /api/v1/getAllUsers
POST   /api/v1/createUser
POST   /api/v1/deleteUser
GET    /api/v1/user?id=123
```

### URL design rules

- Use **plural nouns**: `/users`, `/orders`, `/products`.
- Use **lowercase with hyphens**: `/order-items`, not `/orderItems` or `/order_items`.
- Keep nesting **shallow** (max 2 levels): `/users/123/orders` is fine; `/users/123/orders/456/items/789/reviews` is too deep — flatten to `/reviews?item_id=789`.
- Use **query parameters** for filtering, sorting, pagination: `/users?role=admin&sort=-created_at&page=2`.
- Avoid exposing internal IDs when possible — use UUIDs or slugs for public-facing resources.

### HTTP methods and semantics

| Method  | Idempotent | Safe | Use for                          |
|:--------|:-----------|:-----|:---------------------------------|
| GET     | Yes        | Yes  | Read resources                   |
| POST    | No         | No   | Create resources, trigger actions |
| PUT     | Yes        | No   | Full replace of a resource       |
| PATCH   | Yes*       | No   | Partial update                   |
| DELETE  | Yes        | No   | Remove a resource                |
| HEAD    | Yes        | Yes  | Like GET but headers only        |
| OPTIONS | Yes        | Yes  | CORS preflight, capabilities     |

*PATCH is idempotent when using merge-patch semantics (the common case).

### HTTP status codes

Use them correctly — they are part of your API contract.

```
2xx — Success
  200 OK                  — Standard success response
  201 Created             — Resource created (include Location header)
  204 No Content          — Success with no response body (DELETE, PUT)

3xx — Redirection
  301 Moved Permanently   — Resource URL changed permanently
  304 Not Modified        — Cached version is still valid

4xx — Client Errors
  400 Bad Request         — Malformed syntax or invalid input
  401 Unauthorized        — Missing or invalid authentication
  403 Forbidden           — Authenticated but insufficient permissions
  404 Not Found           — Resource doesn't exist
  409 Conflict            — State conflict (e.g., duplicate email)
  422 Unprocessable Entity — Valid syntax but semantic errors
  429 Too Many Requests   — Rate limit exceeded (include Retry-After header)

5xx — Server Errors
  500 Internal Server Error — Unhandled server error
  502 Bad Gateway          — Upstream service failure
  503 Service Unavailable  — Temporary overload or maintenance
  504 Gateway Timeout      — Upstream service timeout
```

### Consistent error response format

Follow RFC 9457 (Problem Details for HTTP APIs):

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 422,
  "detail": "The email field is required and must be a valid email address.",
  "instance": "/api/v1/users",
  "errors": [
    {
      "field": "email",
      "message": "This field is required.",
      "code": "required"
    }
  ]
}
```

Rules for error responses:
- Always return a consistent structure across all endpoints.
- Include machine-readable error codes alongside human-readable messages.
- Include field-level validation errors so clients can fix all issues in one round-trip.
- **Never leak internal details** (stack traces, SQL queries, file paths) in production errors.
- Log the full error server-side; return a sanitized version to the client.

---

## 2. API Versioning

### Strategies

| Strategy      | Example                         | Pros                    | Cons                     |
|:--------------|:--------------------------------|:------------------------|:-------------------------|
| URL path      | `/api/v1/users`                 | Explicit, easy to route | URL pollution            |
| Header        | `Accept: application/vnd.api+json;version=2` | Clean URLs | Hidden, harder to test   |
| Query param   | `/api/users?version=2`          | Simple                  | Inconsistent             |

**Recommendation**: Use **URL path versioning** (`/api/v1/`). It's the most explicit, easiest to route, cache, and document. When introducing a breaking change, create a new version (`/api/v2/`) and run both in parallel with a deprecation timeline.

### Deprecation protocol

1. Announce deprecation with a `Deprecation` header and `Sunset` header on old endpoints.
2. Provide a migration guide.
3. Give clients at least 6–12 months before removal.
4. Monitor usage of deprecated endpoints before turning them off.

---

## 3. Pagination

### Cursor-based pagination (recommended)

Best for real-time data, large datasets, and infinite scroll. Immune to offset drift when data changes.

```
GET /api/v1/orders?limit=20&after=eyJpZCI6MTIzfQ

Response:
{
  "data": [...],
  "pagination": {
    "has_next": true,
    "next_cursor": "eyJpZCI6MTQzfQ",
    "has_previous": true,
    "previous_cursor": "eyJpZCI6MTI0fQ"
  }
}
```

### Offset-based pagination (simpler)

Fine for admin dashboards, small datasets, or when users need to jump to specific pages.

```
GET /api/v1/users?page=3&per_page=25

Response:
{
  "data": [...],
  "pagination": {
    "page": 3,
    "per_page": 25,
    "total": 482,
    "total_pages": 20
  }
}
```

### Pagination rules

- Always set a **maximum page size** (e.g., `per_page` capped at 100).
- Default to a reasonable page size (20–50).
- Include pagination metadata in every list response.
- For very large datasets (millions of rows), cursor-based is the only performant option.

---

## 4. Filtering, Sorting, and Field Selection

```
# Filtering
GET /api/v1/products?category=electronics&price_min=100&price_max=500&in_stock=true

# Sorting (prefix with - for descending)
GET /api/v1/products?sort=-price,name

# Field selection (reduce payload size)
GET /api/v1/users?fields=id,name,email

# Full-text search
GET /api/v1/products?q=wireless+headphones
```

Be consistent across all endpoints. Document every supported filter, sort field, and selection parameter.

---

## 5. Authentication & Authorization

### Authentication methods by use case

| Use case               | Method                  |
|:-----------------------|:------------------------|
| User-facing apps       | OAuth 2.0 / OIDC        |
| Server-to-server       | API keys + HMAC signing |
| Microservice-to-microservice | Mutual TLS (mTLS) or JWT |
| Simple internal tools  | API keys in headers     |

### JWT best practices

```
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

- Use **short-lived access tokens** (5–15 minutes) with **long-lived refresh tokens** (days/weeks).
- Store JWTs in **httpOnly, Secure, SameSite=Strict cookies** for browser clients — never in localStorage.
- Use **asymmetric signing** (RS256/ES256) for distributed systems so services can verify without the private key.
- Include minimal claims: `sub` (user ID), `exp`, `iat`, `iss`, `roles/scopes`.
- Validate `exp`, `iss`, and `aud` on every request.
- Implement **token revocation** via a short blocklist or by keeping access tokens very short-lived.

### OAuth 2.0 / OIDC

- Use **Authorization Code flow with PKCE** for all client types (web, mobile, SPA).
- Never use the Implicit flow — it's deprecated.
- Use established providers (Auth0, Clerk, Keycloak, Supabase Auth) rather than rolling your own.
- Always validate the `state` parameter to prevent CSRF.
- Store client secrets server-side only.

### Authorization patterns

- **RBAC (Role-Based Access Control)**: Assign roles (admin, editor, viewer) with predefined permissions. Works for most applications.
- **ABAC (Attribute-Based Access Control)**: Policies based on user attributes, resource attributes, and context. More flexible but more complex.
- **Check authorization at every layer**: Middleware for route-level checks, service layer for business-logic checks. Never rely on a single layer.

---

## 6. Database Design

### Schema design principles

- **Normalize first, denormalize intentionally.** Start with 3NF; denormalize specific tables for read performance when you have evidence (not speculation) of a bottleneck.
- **Use appropriate data types**: Don't store dates as strings, don't use TEXT for short fixed-length fields, use DECIMAL/NUMERIC for money (never FLOAT).
- **Always have a primary key**: Prefer auto-incrementing integers for internal IDs; use UUIDs (v7 for sortability) for public-facing IDs.
- **Add created_at and updated_at** to every table (with timezone).
- **Use foreign keys** for referential integrity in OLTP databases.
- **Index strategically**: Index columns used in WHERE, JOIN, ORDER BY. Composite indexes follow the leftmost prefix rule. Don't over-index — each index slows writes.

### Query optimization

```sql
-- ✅ Use EXPLAIN ANALYZE to understand query plans
EXPLAIN ANALYZE
SELECT u.id, u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2026-01-01'
GROUP BY u.id, u.name
ORDER BY order_count DESC
LIMIT 20;

-- ✅ Avoid SELECT * — fetch only needed columns
SELECT id, name, email FROM users WHERE active = true;

-- ❌ N+1 queries — the most common performance killer
-- Fetching users, then looping to fetch each user's orders separately
-- ✅ Fix: JOIN or batch fetch in a single query
```

### Common query pitfalls

| Pitfall | Fix |
|:--------|:----|
| N+1 queries | Use JOINs, eager loading, or batch fetching |
| Missing indexes on foreign keys | Always index FK columns |
| Full table scans on large tables | Add appropriate indexes; use LIMIT |
| Using OFFSET for deep pagination | Switch to cursor/keyset pagination |
| Locking issues on hot tables | Use row-level locking; consider read replicas |
| Not using connection pooling | Use PgBouncer, HikariCP, or framework-level pools |

### SQL vs NoSQL decision

| Choose SQL (PostgreSQL, MySQL) when | Choose NoSQL when |
|:------------------------------------|:------------------|
| Complex relationships and JOINs | Document-shaped data (MongoDB) |
| ACID transactions required | High write throughput at scale (Cassandra) |
| Structured, well-known schema | Key-value lookups / caching (Redis) |
| Reporting and aggregation | Graph relationships (Neo4j) |
| Most CRUD applications | Time-series data (InfluxDB, TimescaleDB) |

**Default to PostgreSQL** for most applications. It handles JSON (jsonb), full-text search, geospatial data, and scales to millions of rows before you need anything exotic.

---

## 7. Caching

### Caching layers

```
Client ──→ CDN ──→ API Gateway ──→ Application Cache ──→ Database
             ↑          ↑                ↑
          Static     Response         Redis/Memcached
          assets     caching          or in-memory
```

### Caching strategies

| Strategy | How it works | Best for |
|:---------|:-------------|:---------|
| **Cache-aside** (Lazy loading) | App checks cache → miss → query DB → write to cache | General-purpose; most common |
| **Write-through** | App writes to cache AND DB simultaneously | Strong consistency requirements |
| **Write-behind** (Write-back) | App writes to cache; cache async writes to DB | High write throughput |
| **Read-through** | Cache itself fetches from DB on miss | Simpler app code |

### Cache invalidation

Cache invalidation is one of the two hard problems in CS. Strategies:

- **TTL (Time-to-Live)**: Set expiration. Simple but can serve stale data.
- **Event-driven invalidation**: Invalidate cache when the underlying data changes (e.g., after a write).
- **Tag-based invalidation**: Tag cache entries; invalidate all entries with a given tag.
- **Versioned keys**: Include a version number in the cache key; bump it on changes.

### Redis patterns

```
# Cache-aside pattern (pseudocode)
def get_user(user_id):
    cached = redis.get(f"user:{user_id}")
    if cached:
        return deserialize(cached)

    user = db.query("SELECT * FROM users WHERE id = %s", user_id)
    redis.setex(f"user:{user_id}", 300, serialize(user))  # TTL: 5 min
    return user

# Distributed locking (prevent thundering herd)
lock = redis.set(f"lock:user:{user_id}", "1", nx=True, ex=10)
if lock:
    # Only one process rebuilds the cache
    ...
```

### What to cache

- **Cache**: Expensive query results, computed aggregations, API responses from third parties, session data, frequently-read and rarely-changed data.
- **Don't cache**: User-specific sensitive data without proper scoping, rapidly-changing data where staleness is unacceptable, one-time reads.

---

## 8. Rate Limiting

Protect your API from abuse, ensure fair usage, and prevent cascading failures.

### Algorithms

| Algorithm | Behavior | Best for |
|:----------|:---------|:---------|
| **Token bucket** | Tokens refill at a steady rate; requests consume tokens | Smooth rate limiting with burst allowance |
| **Sliding window** | Counts requests in a rolling time window | Precise rate limiting |
| **Fixed window** | Counts requests per fixed time window | Simplest to implement |

### Implementation

```
# Response headers for rate limiting
X-RateLimit-Limit: 1000        # Max requests per window
X-RateLimit-Remaining: 847     # Requests remaining
X-RateLimit-Reset: 1712800000  # Unix timestamp when window resets
Retry-After: 30                # Seconds to wait (on 429 response)
```

- Apply rate limits **per API key/user**, not just per IP (IPs are shared behind NATs/VPNs).
- Use different limits for different tiers (free: 100/hr, pro: 10,000/hr).
- Return `429 Too Many Requests` with a `Retry-After` header.
- Implement at the **API gateway or reverse proxy** level for efficiency.
- Use Redis or a distributed counter for multi-instance deployments.

---

## 9. Background Jobs & Async Processing

### When to use background jobs

- Email/notification sending
- PDF/report generation
- Image/video processing
- Data import/export
- Webhook delivery and retries
- Scheduled tasks (cron-like)
- Any operation that takes > 1–2 seconds

### Architecture

```
API Server ──→ Message Queue ──→ Workers
   │            (Redis, RabbitMQ,    │
   │             Kafka, SQS)        │
   │                                ↓
   └── Returns 202 Accepted    Process job
       with job status URL      Update status
                                Notify on completion
```

### Job design principles

- **Idempotent**: Jobs should be safe to retry. If a job runs twice, the result should be the same.
- **Small and focused**: Each job does one thing. Chain jobs for complex workflows.
- **Observable**: Log job start/end/failure. Track duration, success rate, and queue depth.
- **Retry with backoff**: Use exponential backoff with jitter (e.g., 1s, 2s, 4s, 8s + random jitter).
- **Dead letter queue**: Failed jobs after max retries go to a DLQ for manual inspection.
- **Timeout**: Set maximum execution time to prevent zombie jobs.

### Tools

| Language/Ecosystem | Tool |
|:-------------------|:-----|
| Python | Celery + Redis/RabbitMQ, ARQ, Dramatiq |
| Node.js | BullMQ + Redis, Temporal |
| Java/Kotlin | Spring Batch, Quartz |
| Language-agnostic | Kafka, RabbitMQ, AWS SQS, Temporal |

---

## 10. Security

### OWASP Top 10 awareness (2025–2026)

The most critical backend security risks. Every backend engineer should know these:

1. **Broken Access Control** — Enforce authorization at every endpoint and data access layer.
2. **Cryptographic Failures** — Use TLS everywhere. Hash passwords with bcrypt/argon2. Encrypt sensitive data at rest.
3. **Injection** — Use parameterized queries / ORMs. Never concatenate user input into SQL/commands.
4. **Insecure Design** — Threat model during design, not after deployment.
5. **Security Misconfiguration** — Disable debug endpoints in production. Remove default credentials. Set security headers.
6. **Vulnerable Components** — Keep dependencies updated. Audit with `npm audit`, `pip-audit`, Snyk, or Dependabot.
7. **Authentication Failures** — Implement account lockout, rate limiting on login, MFA.
8. **Data Integrity Failures** — Verify software updates and CI/CD pipelines. Use SRI for CDN assets.
9. **Logging & Monitoring Failures** — Log security events. Set up alerts for anomalies.
10. **SSRF** — Validate and sanitize URLs the server fetches. Allowlist permitted domains.

### Security headers

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; script-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

### Input validation

- Validate **all** input: request body, query params, path params, headers.
- Validate on the server — client validation is for UX, not security.
- Use schema validation libraries (Pydantic, Zod, Joi, JSON Schema).
- Reject unexpected fields (strict mode).
- Sanitize output when rendering user content to prevent XSS.

### Password storage

- **Never** store passwords in plain text or with reversible encryption.
- Use **bcrypt** (cost factor ≥ 12) or **argon2id** (preferred for new systems).
- Salt is built into bcrypt/argon2 — don't roll your own salting scheme.

---

## 11. Observability

Observability = Logs + Metrics + Traces. Design it alongside your application, not as an afterthought.

### The three pillars

**Logs** — Structured event records.
```json
{
  "timestamp": "2026-04-10T14:32:01Z",
  "level": "error",
  "service": "order-service",
  "request_id": "req_abc123",
  "user_id": "usr_456",
  "message": "Payment processing failed",
  "error": "stripe_timeout",
  "duration_ms": 30042
}
```

- Use **structured logging** (JSON) — not unstructured text.
- Include **request IDs / correlation IDs** that propagate across services.
- Log at appropriate levels: DEBUG (development only), INFO (significant events), WARN (recoverable issues), ERROR (failures requiring attention).
- **Never log** passwords, tokens, PII, or credit card numbers.

**Metrics** — Aggregated numerical measurements.

Key metrics to track (the RED method):
- **Rate**: Requests per second
- **Errors**: Error rate (4xx, 5xx)
- **Duration**: Response time (p50, p95, p99)

Additional: CPU/memory usage, queue depth, active connections, cache hit ratio, DB query time.

**Traces** — Request flow across services.

- Use **OpenTelemetry** (the industry standard) for instrumentation.
- Propagate trace context (`traceparent` header) across service boundaries.
- Trace critical paths: API → service → database → external API.

### Alerting rules

- Alert on **symptoms** (high error rate, slow response times), not causes.
- Set thresholds based on **SLOs** (Service Level Objectives), e.g., "99.9% of requests complete in < 500ms."
- Use severity levels: critical (paging), warning (next business day), info (dashboard only).
- Avoid alert fatigue — every alert should be actionable.

### Tools

| Category | Tools |
|:---------|:------|
| Logging | ELK Stack, Loki + Grafana, Datadog |
| Metrics | Prometheus + Grafana, Datadog, CloudWatch |
| Tracing | Jaeger, Tempo, Datadog APM, Honeycomb |
| All-in-one | Datadog, New Relic, Grafana Cloud |
| Instrumentation | OpenTelemetry (universal standard) |

---

## 12. Architecture Patterns

### Monolith vs Microservices

| | Modular Monolith | Microservices |
|:--|:-----------------|:--------------|
| **Start with** | ✅ Always start here | Migrate to when needed |
| **Deploy** | Single artifact | Independent per service |
| **Complexity** | Lower operational overhead | Higher (networking, observability, consistency) |
| **Team size** | < 20–30 engineers | Large orgs with team boundaries |
| **Data** | Single database | Database per service |

**Start with a well-structured monolith.** Extract services only when you have clear domain boundaries and team/scaling needs that justify the operational complexity.

### Layered architecture (for any backend)

```
┌─────────────────────────────────┐
│  Presentation (Routes/Handlers) │  ← HTTP layer, input validation
├─────────────────────────────────┤
│  Service / Business Logic       │  ← Domain rules, orchestration
├─────────────────────────────────┤
│  Repository / Data Access       │  ← Database queries, external APIs
├─────────────────────────────────┤
│  Infrastructure                 │  ← DB connections, caches, queues
└─────────────────────────────────┘
```

Rules:
- Each layer only calls the layer directly below it.
- Routes should be thin — delegate to services.
- Services contain business logic — no HTTP concepts (no request/response objects).
- Repositories abstract data access — services don't write SQL directly.

### Communication patterns

| Pattern | Protocol | Use when |
|:--------|:---------|:---------|
| Synchronous request/response | HTTP/REST, gRPC | Direct queries, CRUD |
| Async messaging | RabbitMQ, Kafka, SQS | Decoupled processing, event-driven workflows |
| Streaming | gRPC streams, WebSockets, SSE | Real-time updates, live feeds |
| Webhooks | HTTP callbacks | Notifying external systems of events |

### Resilience patterns

- **Circuit breaker**: Stop calling a failing service; fail fast and recover gracefully.
- **Retry with exponential backoff + jitter**: Retry transient failures without thundering herd.
- **Timeout**: Set timeouts on all external calls. A missing timeout is a bug.
- **Bulkhead**: Isolate failures — don't let one slow dependency bring down the entire system.
- **Health checks**: Expose `/health` (liveness) and `/ready` (readiness) endpoints.

---

## 13. Webhooks

### Sending webhooks

- Sign payloads with HMAC-SHA256 so receivers can verify authenticity.
- Use exponential backoff for retries (e.g., 5 attempts: 1m, 5m, 30m, 2h, 24h).
- Consider successful delivery as 2xx response within a timeout (e.g., 30s).
- Log all delivery attempts for debugging.
- Provide a webhook event log / dashboard in your API.
- Send a minimal payload with an event type and resource ID; let receivers fetch details via API.

### Receiving webhooks

- Verify the signature before processing.
- Respond with `200 OK` quickly; process asynchronously.
- Handle duplicate deliveries gracefully (idempotent processing).
- Use a queue for processing to avoid blocking the webhook endpoint.

---

## 14. Testing Backend Systems

### Testing pyramid

```
        ╱  E2E Tests  ╲         ← Few: Full user flows
       ╱  Integration   ╲       ← Some: API endpoints with real DB
      ╱  Unit Tests      ╲      ← Many: Business logic, utilities
     ╱────────────────────╲
```

### What to test at each level

**Unit tests** (fast, isolated):
- Business logic functions
- Validation rules
- Data transformations
- Edge cases and error paths

**Integration tests** (with real dependencies):
- API endpoints end-to-end (HTTP → handler → service → DB → response)
- Database queries against a test database
- Cache behavior
- Authentication/authorization flows

**Contract tests** (for API consumers):
- Verify your API responses match the documented schema.
- Use tools like Pact or Schemathesis.

**Load tests** (before production):
- Use k6, Locust, or Gatling.
- Test at 2–3× expected peak traffic.
- Identify bottlenecks: slow queries, memory leaks, connection exhaustion.

### Testing rules

- Test **behavior**, not implementation.
- Use **factories** (Factory Boy, Faker) to generate test data — not fixtures.
- Isolate tests — each test should set up and tear down its own data.
- Test **error paths** as thoroughly as happy paths.
- Run tests in CI on every pull request.

---

## 15. Deployment & Infrastructure

### Container best practices (Docker)

```dockerfile
# Multi-stage build for smaller images
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
# Run as non-root user
RUN adduser --disabled-password appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- Use **multi-stage builds** for smaller images.
- Run as a **non-root user**.
- Pin **exact versions** for base images and dependencies.
- Use `.dockerignore` to exclude unnecessary files.
- Scan images for vulnerabilities (Trivy, Snyk).

### CI/CD pipeline

```
Push → Lint → Unit Tests → Build Image → Integration Tests → Security Scan → Deploy to Staging → E2E Tests → Deploy to Production
```

- **Every commit** triggers lint + unit tests.
- **Every PR merge** triggers full pipeline including integration tests.
- Use **blue-green** or **canary deployments** for zero-downtime releases.
- **Rollback** must be a single command / automated on error spike.

### Health checks

```json
// GET /health (liveness — is the process alive?)
{ "status": "ok" }

// GET /ready (readiness — can the service handle traffic?)
{
  "status": "ok",
  "checks": {
    "database": "connected",
    "redis": "connected",
    "queue": "connected"
  }
}
```

---

## 16. API Documentation

- Use **OpenAPI 3.1** (Swagger) for REST APIs.
- Generate docs **from code** (not maintained separately) — most frameworks support this.
- Include: authentication instructions, endpoint references, request/response examples, error format, rate limits, pagination details.
- Provide **runnable examples** (curl, HTTPie, or language-specific snippets).
- Keep docs in sync — stale docs are worse than no docs.
- Consider publishing an `llms.txt` for AI agent consumption.

---

## 17. Common Pitfalls

| Pitfall | Fix |
|:--------|:----|
| No input validation | Validate everything server-side with schema libraries |
| Leaking internal errors to clients | Return generic errors; log details server-side |
| N+1 database queries | Use JOINs, eager loading, or DataLoader patterns |
| No rate limiting | Implement at API gateway level; return 429 with Retry-After |
| OFFSET-based pagination on large datasets | Switch to cursor/keyset pagination |
| Rolling your own auth | Use established providers or battle-tested libraries |
| No timeouts on external calls | Set timeouts on every HTTP client, DB connection, and queue consumer |
| Monolithic error handling | Use structured error types with consistent response format |
| No request/correlation IDs | Generate and propagate IDs for cross-service tracing |
| Testing only happy paths | Test error cases, edge cases, and auth failures |
| Skipping database migrations | Use Alembic, Flyway, or Prisma Migrate — never ALTER in production manually |
| No health check endpoints | Expose `/health` and `/ready` for orchestrator probes |
| Storing secrets in code/env files in git | Use secret managers (Vault, AWS Secrets Manager, etc.) |
| Ignoring CORS until frontend integration | Configure CORS from day one with explicit origins |

---

## 18. Production Readiness Checklist

Before shipping to production, verify:

**API Design:**
- [ ] Consistent URL structure and naming
- [ ] Proper HTTP status codes on all endpoints
- [ ] Structured error responses (RFC 9457)
- [ ] API versioning in place
- [ ] Pagination on all list endpoints
- [ ] Rate limiting configured

**Security:**
- [ ] HTTPS only (TLS 1.2+ minimum)
- [ ] Authentication on all non-public endpoints
- [ ] Authorization checks at route AND service layer
- [ ] Input validation on all endpoints
- [ ] Security headers set (HSTS, CSP, etc.)
- [ ] Secrets in secret manager (not in code)
- [ ] Dependencies scanned for vulnerabilities

**Database:**
- [ ] Connection pooling configured
- [ ] Indexes on frequently-queried columns and foreign keys
- [ ] Migrations managed with a migration tool
- [ ] Backups automated and tested

**Observability:**
- [ ] Structured logging with correlation IDs
- [ ] Key metrics exported (request rate, error rate, latency)
- [ ] Alerting configured on SLO thresholds
- [ ] Health check endpoints (`/health`, `/ready`)

**Infrastructure:**
- [ ] Containerized with non-root user
- [ ] CI/CD pipeline with automated tests
- [ ] Rollback procedure documented and tested
- [ ] Load tested at 2–3× expected peak
