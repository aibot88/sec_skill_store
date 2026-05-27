---
name: api-conventions
description: >
  REST API design conventions and standards. Apply when writing, reviewing,
  or discussing API endpoints, routes, controllers, serializers, or HTTP
  handlers. Covers URL structure, HTTP methods, response formats, error
  handling, pagination, versioning, and authentication headers.
user-invocable: false
---

## URL Design

- Use kebab-case for URL path segments: `/user-profiles`, not `/userProfiles` or `/user_profiles`
- Use plural nouns for resource collections: `/orders`, `/products`, `/users`
- Nest resources at most one level deep: `/orders/{id}/items` is fine; `/orders/{id}/items/{id}/notes` is too deep - promote `notes` to a top-level resource
- Never use verbs in URLs. The HTTP method is the verb: `DELETE /sessions/{id}` not `POST /logout`
- Resource IDs go in the path; filters go in query params: `GET /products?category=books&min_price=10`

## HTTP Methods

| Method | Semantics | Idempotent | Safe |
|--------|-----------|------------|------|
| GET | Read resource(s) | Yes | Yes |
| POST | Create resource or trigger action | No | No |
| PUT | Replace resource entirely | Yes | No |
| PATCH | Partial update | No | No |
| DELETE | Remove resource | Yes | No |

- Use `POST /resources` to create. Return `201 Created` with `Location` header pointing to the new resource.
- Use `PATCH` for partial updates, not `PUT`, unless clients always send the full representation.

## Response Format

All responses use JSON. Property names use camelCase:

```json
{
  "id": "ord_01HXZ",
  "userId": "usr_abc",
  "status": "pending",
  "createdAt": "2025-03-15T10:00:00Z",
  "items": [
    { "productId": "prd_xyz", "quantity": 2, "unitPrice": 9.99 }
  ]
}
```

- Dates and times are ISO 8601 in UTC: `"2025-03-15T10:00:00Z"`
- IDs are strings (never expose raw database integer IDs)
- Monetary amounts are integers in the smallest currency unit (cents), with a separate `currency` field
- Booleans use true/false (not 0/1 or "yes"/"no")
- Omit null fields by default; include them only when the absence is meaningful

## Error Responses

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [
      { "field": "email", "issue": "Must be a valid email address" }
    ],
    "requestId": "req_01HXZ"
  }
}
```

- Use a machine-readable `code` (snake_case string) for programmatic handling
- Use a human-readable `message` for display
- Always include `requestId` for support and tracing

## HTTP Status Codes

| Code | When to use |
|------|-------------|
| 200 | Successful GET, PATCH, or DELETE with body |
| 201 | Successful POST that created a resource |
| 204 | Successful DELETE or action with no response body |
| 400 | Client sent an invalid request (validation errors) |
| 401 | Authentication required or invalid credentials |
| 403 | Authenticated but not authorized for this resource |
| 404 | Resource not found (or deliberately hidden) |
| 409 | Conflict (duplicate, optimistic lock failure) |
| 422 | Request is valid JSON but semantically wrong |
| 429 | Rate limit exceeded |
| 500 | Unexpected server error |

Never return 200 with an error body.

## Pagination

Use cursor-based pagination for all list endpoints returning potentially large data:

```
GET /orders?limit=25&cursor=eyJpZCI6IjEwMCJ9
```

Response:
```json
{
  "data": [ ... ],
  "pagination": {
    "limit": 25,
    "nextCursor": "eyJpZCI6IjEyNSJ9",
    "hasMore": true
  }
}
```

- Default page size: 25. Maximum: 100.
- Use offset pagination only for admin UIs where jumping to a page is required.

## Versioning

- Version in the URL path: `/v1/orders`, `/v2/orders`
- Increment the major version only for breaking changes (removed fields, changed semantics)
- Deprecate old versions with a `Deprecation` response header; support them for at least 12 months
- New optional fields added to responses are non-breaking and do not require a version bump

## Authentication

- Use `Authorization: Bearer <token>` for API keys and JWT tokens
- Never put tokens in URL query parameters (they appear in server logs)
- For API keys: prefix them with a product identifier for easy detection: `sk_live_...`, `pk_test_...`
- Use `WWW-Authenticate` header in 401 responses

## Filtering, Sorting, and Searching

- Filters: `GET /products?status=active&category=books`
- Sorting: `GET /orders?sort=createdAt&order=desc` (default to `asc`)
- Full-text search: `GET /products?q=wireless+headphones`
- Range filters: `GET /orders?createdAfter=2025-01-01&createdBefore=2025-03-01`

## Idempotency

- Accept an `Idempotency-Key` header on POST requests that create resources or trigger payments
- Store the key and return the same response if the same key is replayed within 24 hours
- Return `409 Conflict` if the same key is used with a different request body

## Rate Limiting

Always return these headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 487
X-RateLimit-Reset: 1741694400
Retry-After: 30  (only on 429)
```
