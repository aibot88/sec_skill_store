---
name: react-security
description: This skill should be used when the user is securing a React application, asking about "XSS in React", "dangerouslySetInnerHTML security", "Server Actions security", "React data exposure", "sensitive data in React", "auth token storage", "IDOR in Next.js", "React security audit", "secure React forms", "Server Component secrets", "server-only package", "React taint API", "DOMPurify React", "prototype pollution React", "hardcoded secrets React", or reviewing React code for security vulnerabilities.
---

# React Security

Security patterns for React applications — XSS prevention, Server Actions authorization, sensitive data protection, and client-side security. These issues cause real breaches; treat each section as mandatory for production code.

## XSS — Cross-Site Scripting

React automatically escapes string values rendered in JSX. The primary XSS risk is intentionally bypassing that protection.

### dangerouslySetInnerHTML

Every use requires sanitization. No exceptions.

```tsx
import DOMPurify from 'dompurify'; // or isomorphic-dompurify for SSR

// BAD: XSS if content contains <script> or event attributes
<div dangerouslySetInnerHTML={{ __html: userContent }} />

// GOOD: sanitize before rendering
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userContent) }} />
```

Sanitize at the point of use, not earlier. Data transforms lose sanitization guarantees.

### Other XSS Vectors

- **`eval()`, `new Function(string)`, `setTimeout(string)`** — Never pass strings. Use function references.
- **URL injection:** Validate `href` values — `javascript:` URLs are XSS vectors. Use URL parsing and allow-lists for external links.
- **`innerHTML` via refs** — Same risk as `dangerouslySetInnerHTML`. Use `textContent` for text-only updates.

## Server Actions — Authorization

Server Actions are **public HTTP POST endpoints**. They run on the server but are callable by anyone — treat them like API routes.

### Required Pattern: Auth + Authorization in Every Action

```tsx
// app/actions.ts
'use server'
import { auth } from '@/lib/auth';
import { db } from '@/lib/db';

export async function deletePost(postId: string) {
  // 1. Verify the user is authenticated
  const session = await auth();
  if (!session?.user) throw new Error('Unauthorized');

  // 2. Verify the user owns THIS resource (prevents IDOR)
  const post = await db.post.findUnique({ where: { id: postId } });
  if (!post || post.authorId !== session.user.id) {
    throw new Error('Forbidden');
  }

  await db.post.delete({ where: { id: postId } });
}
```

**IDOR (Insecure Direct Object Reference):** If you skip the ownership check, any authenticated user can delete any post by guessing IDs. Page-level auth does NOT protect actions.

### Server Action Security Rules

1. **Authenticate** — verify session inside the action, not only in middleware
2. **Authorize** — verify the user has rights to the specific resource being modified
3. **Validate inputs** — parse all `FormData` through Zod before using it
4. **Sanitize errors** — return generic messages to clients; log details server-side
5. **Never return** raw DB records, stack traces, or internal field names

## Sensitive Data Exposure

### Data Access Layer (DAL) Pattern

```tsx
// lib/dal.ts — SERVER ONLY
import 'server-only';
import { auth } from './auth';

export async function getCurrentUser() {
  const session = await auth();
  if (!session) return null;
  // Return minimal DTO — never the full DB record
  return { id: session.user.id, name: session.user.name, role: session.user.role };
}
```

```tsx
// Any server-only file
import 'server-only'; // Build error if imported from a Client Component
```

The `server-only` package causes a **build-time error** if the module is accidentally imported into a Client Component. Use it on every file that accesses secrets, env vars, or the database.

### React Taint APIs (Experimental)

Explicitly mark objects and values as un-passable to Client Components:

```tsx
import { experimental_taintObjectReference, experimental_taintUniqueValue } from 'react';

// Mark entire object — prevents passing to Client Component
experimental_taintObjectReference('Do not pass user record to client', user);

// Mark specific value — prevents passing token to client
experimental_taintUniqueValue('Do not pass token to client', process, process.env.API_SECRET);
```

### Environment Variables

- `NEXT_PUBLIC_*` variables are exposed to the browser. Use for non-secret config only.
- All other `process.env.*` variables stay server-side — never read them in Client Components.
- Never hardcode API keys, tokens, or credentials in source code.

## Authentication Token Storage

| Storage | Risk | Recommendation |
|---------|------|----------------|
| `localStorage` | Accessible to any JS on the page — XSS attack steals token | **Never for auth tokens** |
| `sessionStorage` | Same XSS risk as localStorage | **Never for auth tokens** |
| `httpOnly` cookie | JS cannot read it — XSS cannot steal it | **Use this** |

```tsx
// BAD: XSS can steal the token
localStorage.setItem('auth_token', token);

// GOOD: set from server response with httpOnly flag
// res.cookie('session', token, { httpOnly: true, secure: true, sameSite: 'lax' });
```

## Prototype Pollution

```tsx
// BAD: deep merging user-controlled objects can inject __proto__ keys
import merge from 'lodash.merge';
const config = merge({}, userInput); // if userInput contains __proto__

// GOOD: validate schema before merging
import { z } from 'zod';
const schema = z.object({ theme: z.string(), language: z.string() });
const safe = schema.parse(userInput);
const config = Object.assign({}, defaults, safe);
```

Always validate `JSON.parse` results against a Zod schema before using user-controlled data.

## Hardcoded Secrets Detection

Patterns that indicate hardcoded secrets in React code (flag in every code review):

- `apiKey = "..."`, `api_key: "..."`, `API_KEY = "..."`
- `token = "Bearer ..."`, `authorization: "..."`, `password = "..."`
- Strings starting with `sk-`, `pk_`, `ghp_`, `xoxb-`, `AKIA`
- Long alphanumeric strings (32+ chars) assigned directly in component files

These must be moved to environment variables and accessed via `process.env` on the server.

## Sensitive Data in console.log

```tsx
// BAD: user PII and tokens visible in browser DevTools
console.log('User:', user); // may include email, address, token

// GOOD: guard dev-only logging
if (process.env.NODE_ENV === 'development') {
  console.log('User ID:', user.id); // log only what you need
}
```

## Additional Resources

### Reference Files

- **`references/detailed-patterns.md`** — Complete Server Action auth patterns, Zod validation for form inputs, Content Security Policy headers, and Electron-specific React security
