---
name: typescript-anti-patterns
description: >
  This skill should be used when reviewing TypeScript code for anti-patterns, when code
  contains unsafe practices, when identifying common TypeScript mistakes, when auditing
  AI-generated TypeScript code, or when enforcing production-grade TypeScript standards.
  Trigger on: "review TypeScript code", "TypeScript anti-patterns", "unsafe TypeScript",
  "type assertion smell", "any type misuse", "non-null assertion", "TypeScript code review",
  "AI generated TypeScript", "TypeScript best practices audit", "code smells TypeScript",
  "silent catch", "type widening", "generic soup", "mutable exports", "enum pitfalls",
  "numeric enum", "TypeScript security review", "unsafe cast".
---

# TypeScript Anti-Patterns

These patterns represent the most common ways TypeScript's type safety is subverted in production code — including patterns specifically introduced by AI coding assistants. Recognizing and eliminating them is essential for maintaining a trustworthy type system.

## The Zero-Any Policy

**`any` is never acceptable in production code.** It is a silent type system bypass.

```typescript
// ❌ any — disables all type checking on this variable
function processData(data: any) {
  return data.userId.trim(); // No error — crashes if userId missing
}

// ❌ Implicit any in function parameters
function log(message) { // noImplicitAny catches this
  console.log(message);
}

// ✅ Use unknown — forces proof before use
function processData(data: unknown) {
  if (!isUser(data)) throw new Error('Invalid user data');
  return data.email.trim(); // Narrowed — safe
}
```

**When AI generates `any`:** Replace with `unknown` + type guard or Zod parsing. Never accept `// @ts-ignore` or `// @ts-expect-error` without a specific documented reason.

## The Assertion Smell (`as Type`)

Type assertions at API boundaries or around `unknown` data are red flags.

```typescript
// ❌ Classic assertion smell — lies to the compiler
const user = response.json() as User;
user.email.trim(); // Compiles, but crashes if API schema changed

// ❌ Double assertion — bypasses type checking entirely
const hack = value as unknown as SpecificType;

// ❌ Object literal assertion — excess property checks bypassed
const config = { url: '/api', timeout: 5000, typoKey: true } as Config;

// ✅ Correct — parse and prove at the boundary
const result = UserSchema.safeParse(await response.json());
if (!result.success) return sendError(400, result.error.flatten());
const user = result.data; // Typed and verified
```

**Acceptable uses of `as`:**
- `as const` — literal preservation and immutability (encouraged)
- Within type predicate implementations (acceptable)
- Narrowing after a runtime check when type predicate syntax is too verbose

## Non-Null Assertion Abuse (`!`)

The `!` operator is a lie: it tells the compiler "trust me, this is not null/undefined."

```typescript
// ❌ Fragile — breaks when code is moved or refactored
const name = user!.profile!.name!;

// ❌ AI-generated: spray ! to silence null check errors
const element = document.querySelector('.btn')!.addEventListener('click', handler);

// ✅ Explicit null checks
const profile = user?.profile;
if (!profile?.name) return;
const name = profile.name; // Narrowed — safe

// ✅ Discriminated union eliminates the need for !
type LoggedInUser = { status: 'authenticated'; profile: Profile };
if (user.status === 'authenticated') {
  const name = user.profile.name; // Compiler proves profile exists
}
```

## Silent Catch Blocks

Empty catches hide bugs. They make debugging nearly impossible.

```typescript
// ❌ Silent swallow
try {
  await processOrder(order);
} catch { } // Bug disappears here

// ❌ Logging is not handling
try {
  await processOrder(order);
} catch (err) {
  console.error(err); // Logged in dev, missing in prod log aggregation
}

// ✅ Actually handle or re-throw with context
try {
  await processOrder(order);
} catch (err) {
  if (err instanceof ValidationError) {
    return { ok: false, error: 'VALIDATION_FAILED', details: err.fields };
  }
  throw new Error(`Order processing failed for order ${order.id}`, { cause: err });
}
```

## Widened Literals (Loss of Specificity)

Annotating with a broad type loses the specific type information.

```typescript
// ❌ Type annotation widens literals
const config: Record<string, string> = {
  theme: 'dark',
  locale: 'en-US',
};
config.theme; // Type: string (lost 'dark')
config.nonexistent; // No error!

// ✅ satisfies validates without widening
const config = {
  theme: 'dark',
  locale: 'en-US',
} satisfies Record<string, string>;
config.theme; // Type: 'dark' (preserved)
config.nonexistent; // Error! (key validation)

// ✅ as const for complete immutability
const THEMES = ['dark', 'light', 'system'] as const;
type Theme = typeof THEMES[number]; // 'dark' | 'light' | 'system'
```

## Numeric Enum Pitfalls

Numeric enums create runtime IIFE objects, allow reverse mapping, and accept any `number`.

```typescript
// ❌ Numeric enum — runtime overhead, numeric assignment allowed
enum Status {
  Pending,   // = 0
  Active,    // = 1
  Inactive,  // = 2
}
const s: Status = 999; // No error! Any number is assignable

// ❌ Regular string enum — generates runtime object, breaks tree-shaking
enum Role {
  Admin = 'ADMIN',
  User = 'USER',
}

// ✅ String literal union — zero runtime cost, no ambiguity
type Status = 'pending' | 'active' | 'inactive';

// ✅ as const for runtime array + type (when iteration needed)
const STATUS_OPTIONS = ['pending', 'active', 'inactive'] as const;
type Status = typeof STATUS_OPTIONS[number];

// ✅ const enum — inlined at compile time (but avoid with bundlers)
const enum Direction { Up, Down, Left, Right }
// Compiles to: 0, 1, 2, 3 at use sites — no runtime object
// Warning: requires --isolatedModules: false, breaks with esbuild/swc
```

## Generic Soup

Overly abstract generics reduce readability and increase compile times.

```typescript
// ❌ Generic soup — unreadable, confusing, poor DX
type DeepNested<T, K extends keyof T, V extends T[K], R extends Record<K, V>> =
  R extends Record<infer KK, infer VV> ? VV extends string ? KK : never : never;

// ❌ Too many generic parameters
function transform<T, K extends keyof T, V extends T[K], R>(
  obj: T, key: K, transform: (v: V) => R, fallback: R
): Record<K, R> { ... }

// ✅ If you can't describe the generic in one sentence, simplify
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

**Rule:** If a function has more than 3 generic parameters, refactor. If you cannot describe what `T` represents in one sentence, the abstraction is too complex.

## Mutable Shared State

Exported mutable objects can be modified by any importer — a major source of hidden state bugs.

```typescript
// ❌ Exported mutable array — any importer can push/splice
export const adminUsers: User[] = [];
// Elsewhere: adminUsers.push(maliciousUser); // Undetected

// ❌ Exported mutable config
export const config = {
  apiUrl: 'https://api.example.com',
  retries: 3,
};
// Elsewhere: config.retries = 0; // Silently breaks retry logic

// ✅ Export readonly types
export const adminUsers: ReadonlyArray<User> = Object.freeze([]);
export const config = Object.freeze({
  apiUrl: 'https://api.example.com',
  retries: 3,
} as const);

// ✅ Expose mutation through controlled functions
let users: User[] = [];
export const userStore = {
  get: (): ReadonlyArray<User> => users,
  add: (user: User): void => { users = [...users, user]; },
};
```

## AI Codegen Specific Anti-Patterns

AI coding assistants consistently introduce these patterns — always review AI-generated TypeScript:

| Pattern | What AI Does | Correct Pattern |
|---------|-------------|----------------|
| `any` spray | Uses `any` for "complex" types | `unknown` + type guard |
| `!` spray | Adds `!` to silence null warnings | Explicit null check or discriminated union |
| `.parse()` instead of `.safeParse()` | Throws on invalid input | `.safeParse()` + check `.success` |
| Empty `catch {}` | Swallows errors silently | Classify and handle |
| Manual type-only imports | Uses `import` instead of `import type` | `import type` |
| Missing `override` keyword | Shadows base class methods | Add `override` |
| Broad type annotations | `const x: object = { key: 'value' }` | `satisfies` or `as const` |
| String `JSON.parse()` | `JSON.parse(str) as MyType` | `MySchema.safeParse(JSON.parse(str))` |
| Enum over union | `enum Status { Active, Inactive }` | `type Status = 'active' | 'inactive'` |

## The Engineering Backpressure System

To prevent anti-patterns from persisting in the codebase:

1. **Compiler enforcement**: `strict: true` + `noUncheckedIndexedAccess` + `exactOptionalPropertyTypes`
2. **ESLint rules**: `no-explicit-any`, `no-non-null-assertion`, `consistent-type-assertions`
3. **Verification loop for AI**: run `tsc --noEmit && eslint . --max-warnings 0` before review
4. **Code review checklist**: Flag all `as`, `!`, `any`, and empty `catch` blocks

## Additional Resources

For the complete anti-patterns audit guide and AI codegen guardrails, consult:
- **`references/anti-patterns-checklist.md`** — Comprehensive code review checklist for TypeScript anti-patterns
- **`references/ai-codegen-guardrails.md`** — Specific rules for reviewing and correcting AI-generated TypeScript
