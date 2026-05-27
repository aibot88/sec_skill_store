---
name: Zod Security
description: This skill should be used when the user asks about "Zod security", "Zod over-posting attack", "mass assignment Zod", "z.strictObject security", "z.custom security", "Zod coercion vulnerability", "Zod default PATCH bug", "Zod data loss", "Zod reportInput PII", "exposing ZodError to client", "Zod security review", "reviewing Zod validation code", or when performing a code review on TypeScript files that use Zod. Provides a comprehensive security model and review checklist for Zod usage.
version: 1.0.0
---

# Zod Security

## The Security Surface: What Zod Guards and What It Doesn't

Zod guards **data correctness at runtime boundaries**. It cannot prevent logic errors in business code, SQL injection in query strings, or XSS in template rendering. What it does prevent — when used correctly — is:

- Unvalidated data entering business logic
- Unexpected keys being processed (over-posting)
- Type coercion confusion attacks
- Silent data corruption from default value injection

When used incorrectly, Zod creates a **false sense of security** — code appears to validate but allows unsafe data through.

## Critical Rule: `z.strictObject()` at Public API Boundaries

`z.object()` silently **strips** unknown keys. `z.strictObject()` actively **rejects** them. The distinction is security-critical at external-facing endpoints:

```typescript
// VULNERABLE: Strips extra keys but never rejects them
// POST /user { name: "Alice", role: "admin" } — "role" is silently stripped
// Developer assumes "role" can't be injected; business logic still may be unsafe
const CreateUserSchema = z.object({ name: z.string() });

// SECURE: Rejects requests containing unexpected keys
const CreateUserSchema = z.strictObject({ name: z.string() });
// POST /user { name: "Alice", role: "admin" } → 400 Bad Request
```

**Use `z.strictObject()` for:** All POST/PUT/PATCH body schemas at API entry points.
**Use `z.object()` for:** Internal data transformation, reshaping data between layers.

## Critical Rule: Never Use `z.custom()` Without a Validator

`z.custom()` with no argument (or a validator that always returns `true`) is **a validation bypass** — it accepts any value:

```typescript
// DANGEROUS: Equivalent to z.unknown() — validates nothing
const DangerousSchema = z.custom();
const AlsoDangerous = z.custom(() => true);

// SAFE: Always provide a type guard
const SafeSchema = z.custom<Date>((val) => val instanceof Date);
const SafeBuffer = z.custom<Buffer>((val) => Buffer.isBuffer(val));
```

Flag any `z.custom()` call in a code review that lacks a meaningful predicate function.

## Critical Rule: Separate Schemas for PATCH Endpoints

In Zod 4, **`.default()` values are always applied**, even when a field is wrapped in `.optional()` or `.partial()`. Reusing a create-schema (which has defaults) for a PATCH endpoint causes silent data corruption:

```typescript
const UserSchema = z.object({
  name: z.string(),
  bio: z.string().default(""),   // Default: empty string
  role: z.enum(["user", "admin"]).default("user"), // Default: "user"
});

// DANGEROUS: PATCH with partial user (only updating name)
// Input: { name: "Alice" }
// After parse: { name: "Alice", bio: "", role: "user" }
// → Overwrites existing bio and role with defaults!
const PatchUserSchema = UserSchema.partial(); // Still applies defaults ❌

// SAFE: Create a dedicated patch schema without defaults
const PatchUserSchema = z.object({
  name: z.string().optional(),
  bio: z.string().optional(),
  role: z.enum(["user", "admin"]).optional(),
});
// Input: { name: "Alice" } → Output: { name: "Alice" }
// Only provided fields are present; omitted fields stay undefined
```

**Always create dedicated schemas for partial update endpoints.** Never reuse creation schemas with `.partial()`.

## Coercion Security: Constrain Before You Coerce

`z.coerce.*` accepts `unknown` input and applies the JavaScript constructor. Unconstrained coercion can produce surprising values:

```typescript
// Surprising coercions:
z.coerce.number().parse("0xff")   // → 255 (hex string parsed as number!)
z.coerce.number().parse("")       // → 0
z.coerce.boolean().parse("false") // → true (any non-empty string is truthy)
z.coerce.date().parse("garbage")  // → Invalid Date (no error!)
```

Constrain input before coercing:

```typescript
// SAFE: Constrain to expected types, then coerce
const AgeSchema = z.string().regex(/^\d+$/, "Must be a numeric string")
  .pipe(z.coerce.number().int().min(0).max(150));

// SAFE: Reject non-finite numbers after coercion
const PriceSchema = z.string()
  .pipe(z.coerce.number().finite().positive());
```

## Do Not Expose Raw ZodErrors to Clients

Returning the raw `ZodError` or its `.issues` array in HTTP responses exposes internal schema structure:

```typescript
// VULNERABLE: Reveals field names, path structure, internal model
res.status(400).json({ error: validationError });

// SECURE: Sanitize for client consumption
res.status(400).json({
  message: "Validation failed",
  errors: z.flattenError(validationError).fieldErrors,
});
```

## The `reportInput: true` PII Risk

Setting `reportInput: true` in error configuration causes Zod to include the raw input value in error issues. In production, this logs passwords, tokens, and personal data:

```typescript
// NEVER in production
z.config({ reportInput: true });
```

Only enable `reportInput` in local development when debugging. Treat it like a debug flag — commit it off, never ship it on.

## `.passthrough()` and `z.looseObject()` at Boundaries

Both explicitly allow unknown keys through. Never use at public API entry points:

```typescript
// VULNERABLE: Allows any extra fields through
const Schema = z.object({ name: z.string() }).passthrough();
const Schema = z.looseObject({ name: z.string() });

// Only use .passthrough() when explicitly proxying data you don't own
// (e.g., forwarding third-party webhook payloads)
```

## Security Review Checklist

When reviewing TypeScript code that uses Zod, verify:

| Check | Good | Red Flag |
|---|---|---|
| Object schemas at API boundaries | `z.strictObject()` | `z.object()` |
| Custom validators | `z.custom(val => val instanceof X)` | `z.custom()` or `z.custom(() => true)` |
| PATCH/partial update schemas | Dedicated schema, no defaults | `CreationSchema.partial()` |
| Coercion pattern | Constrained input → pipe → coerce | Bare `z.coerce.*` on untrusted input |
| Error responses | `z.flattenError()` / `z.treeifyError()` | Raw `ZodError` to client |
| reportInput flag | Not present in production code | `reportInput: true` committed |
| Unknown key handling | `.passthrough()` only for explicit proxy use | `.passthrough()` at API endpoints |
| Schema hoisting | Module-level constants | Schemas defined inside handlers |

## Additional Resources

- **`references/security-checklist.md`** — Detailed security review checklist with code examples for every vulnerability pattern
- **`references/attack-scenarios.md`** — Worked attack scenarios: over-posting, coercion confusion, PATCH data loss — with before/after fixes
