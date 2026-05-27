---
name: server-actions-design
description: "Use when designing or reviewing Server Actions: the 'use server' directive contract, how a server-side function becomes invokable from the browser without an API route, form integration via the `action` attribute, the React 19 hooks useActionState / useFormStatus, progressive enhancement (works without JS), server-side validation and authorization as mandatory rather than optional, revalidation primitives (revalidatePath, revalidateTag, redirect), error handling and bound arguments, and the security boundary that makes Server Actions a public endpoint despite their function-like syntax. Covers Next.js App Router as the canonical implementation. Do NOT use for read-path data fetching with RSC (use server-components-design), for the broader 'use client' / 'use server' boundary semantics (use client-server-boundary), for designing externally-facing API contracts (use api-design), or for form UX patterns at the component level (use form-ux-architecture)."
license: MIT
allowed-tools: Read Grep
metadata:
  metadata: "{\"schema_version\":6,\"version\":\"1.0.0\",\"type\":\"capability\",\"category\":\"engineering\",\"domain\":\"engineering/frontend\",\"scope\":\"reference\",\"owner\":\"skill-graph-maintainer\",\"freshness\":\"2026-05-16\",\"drift_check\":\"{\\\\\\\"last_verified\\\\\\\":\\\\\\\"2026-05-16\\\\\\\"}\",\"eval_artifacts\":\"planned\",\"eval_state\":\"unverified\",\"routing_eval\":\"absent\",\"comprehension_state\":\"present\",\"stability\":\"experimental\",\"keywords\":\"[\\\\\\\"Server Actions\\\\\\\",\\\\\\\"Server Function declaration\\\\\\\",\\\\\\\"form action attribute\\\\\\\",\\\\\\\"useActionState\\\\\\\",\\\\\\\"useFormStatus\\\\\\\",\\\\\\\"forms that work without JavaScript\\\\\\\",\\\\\\\"revalidatePath\\\\\\\",\\\\\\\"revalidateTag\\\\\\\",\\\\\\\"server mutation Next.js\\\\\\\",\\\\\\\"validate Server Action inputs\\\\\\\",\\\\\\\"bound arguments Server Action\\\\\\\",\\\\\\\"redirect after action\\\\\\\"]\",\"triggers\":\"[\\\\\\\"how do I submit a form to the server\\\\\\\",\\\\\\\"do I need an API route for this mutation\\\\\\\",\\\\\\\"how do I call a server function from a button\\\\\\\",\\\\\\\"why is my Server Action exposed as an endpoint\\\\\\\",\\\\\\\"useActionState vs useFormState\\\\\\\",\\\\\\\"how do I revalidate after mutation\\\\\\\",\\\\\\\"can Server Actions run in event handlers\\\\\\\"]\",\"examples\":\"[\\\\\\\"design a 'create comment' form using Server Actions plus useActionState so it works without JavaScript and reports server-side validation errors\\\\\\\",\\\\\\\"decide whether a delete button should call a Server Action or an API route\\\\\\\",\\\\\\\"audit a Server Action for missing authorization (the function looks like a normal call but is publicly invokable)\\\\\\\",\\\\\\\"design the revalidation strategy for a mutation that affects multiple cached routes\\\\\\\"]\",\"anti_examples\":\"[\\\\\\\"design a Server Component that reads data on render (use server-components-design)\\\\\\\",\\\\\\\"design a public REST API consumed by mobile clients (use api-design)\\\\\\\",\\\\\\\"choose between SSR and SSG (use rendering-models)\\\\\\\",\\\\\\\"design the visual UX of a form's validation states (use form-ux-architecture)\\\\\\\",\\\\\\\"design the visual states and accessibility of a form (use form-ux-architecture)\\\\\\\",\\\\\\\"design a public HTTP contract for mobile, third-party, or server-to-server callers (use api-design)\\\\\\\"]\",\"relations\":\"{\\\\\\\"related\\\\\\\":[\\\\\\\"server-components-design\\\\\\\",\\\\\\\"client-server-boundary\\\\\\\",\\\\\\\"form-ux-architecture\\\\\\\",\\\\\\\"api-design\\\\\\\",\\\\\\\"hooks-patterns\\\\\\\"],\\\\\\\"boundary\\\\\\\":[{\\\\\\\"skill\\\\\\\":\\\\\\\"server-components-design\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"server-components-design owns the read path — Server Components fetch data on render; server-actions-design owns the write path — Server Actions execute mutations triggered from the client. They share infrastructure (RSC, 'use server') but solve distinct problems.\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"client-server-boundary\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"client-server-boundary owns the serialization and directive mechanics of the boundary itself; server-actions-design owns the discipline of using the 'use server' side of that boundary for mutations.\\\\\\\"}],\\\\\\\"verify_with\\\\\\\":[\\\\\\\"code-review\\\\\\\",\\\\\\\"api-design\\\\\\\"]}\",\"mental_model\":\"|\",\"purpose\":\"|\",\"boundary\":\"|\",\"analogy\":\"Server Actions are to React mutations what stored procedures are to database access — the function looks like an ordinary call in client code, but the work happens on the privileged side of a trust boundary, with the same security implications: the caller controls the arguments, but cannot see the implementation; the implementation must validate every input and authorize every call as if the caller were a hostile script with curl, because functionally they could be.\",\"misconception\":\"|\",\"concept\":\"{\\\\\\\"definition\\\\\\\":\\\\\\\"A Server Action is a JavaScript function marked with 'use server' (either at the module level or as the first line of the function body) that executes on the server but is invokable from the client. The bundler turns calls to it from Client Components into a network round-trip: arguments are serialized, the function runs server-side, the return value is serialized back. The function itself looks like an ordinary import in client code, which is the design's main strength and its main security trap — what looks like a function call is a public POST endpoint.\\\\\\\",\\\\\\\"mental_model\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"purpose\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"boundary\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"taxonomy\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"analogy\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"misconception\\\\\\\":\\\\\\\"|\\\\\\\"}\",\"skill_graph_source_repo\":\"https://github.com/jacob-balslev/skill-graph\",\"skill_graph_protocol\":\"Skill Metadata Protocol v5\",\"skill_graph_project\":\"Skill Graph\",\"skill_graph_canonical_skill\":\"skills/server-actions-design/SKILL.md\"}"
  skill_graph_source_repo: "https://github.com/jacob-balslev/skill-graph"
  skill_graph_protocol: Skill Metadata Protocol v4
  skill_graph_project: Skill Graph
  skill_graph_canonical_skill: skills/server-actions-design/SKILL.md
---

# Server Actions Design

## Coverage

The discipline of designing Server Actions: what `'use server'` actually does (turns a function into a public POST endpoint with serialized arguments), how Server Actions integrate with HTML forms via the `action` attribute, how `useActionState` and `useFormStatus` give React-aware state and pending UI, why progressive enhancement (form works without JavaScript) is the design's load-bearing feature, why server-side validation and authorization are not optional, how `revalidatePath` / `revalidateTag` / `redirect` participate in the mutation pipeline, how bound arguments propagate state across action calls, and the central security insight: a Server Action that looks like a function call is a publicly-reachable endpoint and must be treated as one.

## Philosophy

Before Server Actions, a "mutation from the browser" required two parallel structures: a client-side function that called `fetch('/api/foo', { method: 'POST', body: JSON.stringify({...}) })`, and a server-side route handler that parsed the body, validated, authorized, executed the mutation, and serialized a response. The two had to agree on a wire format, type contracts had to be duplicated or shared via a runtime validator, and CSRF tokens had to be plumbed through.

Server Actions collapse that into one declaration. A function with `'use server'` at its top is invokable from Client Components as if it were imported normally. The bundler rewrites the call site to a network round-trip; the function executes server-side. There is no manual wire format, no client-side fetch boilerplate, no separate API route to keep in sync.

The collapse is *syntactic*, not *semantic*. The function is still invoked over the network, by anyone who finds the action's identifier, with arguments they control. The server has none of the type guarantees the call site appears to provide. **The discipline of Server Actions is to treat the function as a public endpoint disguised as a function**: validate every input, authorize every call, fail loudly on any assumption that the caller is your own UI rather than an attacker with curl.

The second principle of Server Actions is **progressive enhancement**. A Server Action attached to an HTML form via `<form action={serverAction}>` works without JavaScript: the browser performs a native POST to the action's endpoint, the server returns a redirect, the page navigates. With JavaScript, React intercepts the submission, runs the action, applies the result without a full page reload, and updates `useFormStatus` while the action is in flight. The form does not have two code paths — it has one path that gracefully upgrades when JS arrives. Designing actions that rely on JS-only state defeats the architecture; designing actions that work form-first and JS-second uses it well.

## The `'use server'` Contract

Three ways to declare a Server Action:

1. **Module-level directive**: a file with `'use server'` at the top exports only Server Actions.
   ```ts
   // app/actions/comments.ts
   'use server'
   export async function createComment(formData: FormData) { ... }
   export async function deleteComment(id: string) { ... }
   ```

2. **Inline directive in a Server Component**: a function defined inside a Server Component, with `'use server'` as its first statement.
   ```tsx
   // app/posts/[id]/page.tsx (Server Component)
   export default async function Post({ params }) {
     async function addComment(formData: FormData) {
       'use server'
       // runs on the server, can close over server-side state
     }
     return <form action={addComment}>...</form>
   }
   ```

3. **Re-exported from a `'use server'` module to a Client Component**: client code imports the function and invokes it directly.

The bundler treats `'use server'`-marked functions specially: it strips the function body from the client bundle, replacing it with a reference that the runtime resolves to a network call. The function's *signature* (name, parameter types) is preserved at the call site; the function's *implementation* never reaches the client.

Arguments and return values must be serializable across the boundary — strings, numbers, plain objects, arrays, FormData, Date, Map, Set, typed arrays, Promise (React 19). Functions, class instances, and DOM nodes cannot cross.

## The Form Integration Pattern

The canonical Server Action consumes a `FormData` object via the `action` prop on a `<form>`:

```tsx
'use server'
import { z } from 'zod'
import { db } from '@/db'
import { revalidatePath } from 'next/cache'
import { auth } from '@/auth'

const CommentSchema = z.object({
  postId: z.string().uuid(),
  body: z.string().min(1).max(1000),
})

export async function addComment(formData: FormData) {
  const session = await auth()
  if (!session) throw new Error('Unauthorized')   // public endpoint — must check
  
  const parsed = CommentSchema.safeParse({
    postId: formData.get('postId'),
    body: formData.get('body'),
  })
  if (!parsed.success) return { error: parsed.error.flatten() }
  
  await db.comment.create({
    data: { ...parsed.data, authorId: session.userId },
  })
  
  revalidatePath(`/posts/${parsed.data.postId}`)
  return { success: true }
}
```

```tsx
// In a Server Component (or Client Component):
<form action={addComment}>
  <input type="hidden" name="postId" value={postId} />
  <textarea name="body" required />
  <button type="submit">Post</button>
</form>
```

The form posts to the action. Without JavaScript, the browser navigates to the action's endpoint and back. With JavaScript, React handles the submission inline. Either way, `revalidatePath` instructs Next.js to invalidate the cached version of the post page, so the new comment appears on next render.

## `useActionState` and `useFormStatus`

These two React 19 hooks let Client Components observe action state without imperative wiring.

**`useActionState`** wraps an action and returns the action's last result alongside a wrapper function:

```tsx
'use client'
import { useActionState } from 'react'
import { addComment } from '@/app/actions/comments'

export function CommentForm({ postId }) {
  const [state, formAction, isPending] = useActionState(addComment, { error: null })
  return (
    <form action={formAction}>
      <input type="hidden" name="postId" value={postId} />
      <textarea name="body" />
      {state?.error && <p className="error">{state.error.body?.[0]}</p>}
      <button disabled={isPending}>{isPending ? 'Posting…' : 'Post'}</button>
    </form>
  )
}
```

The first argument is the action; the second is the initial state. `formAction` is what you pass to the form's `action` prop. `state` is whatever the action last returned. `isPending` tracks the in-flight status.

**`useFormStatus`** is read from inside a `<form>`'s descendant components — it gives the pending status without prop drilling:

```tsx
'use client'
import { useFormStatus } from 'react-dom'

export function SubmitButton({ label }) {
  const { pending } = useFormStatus()
  return <button disabled={pending}>{pending ? 'Saving…' : label}</button>
}
```

`useFormStatus` only reads the status of the nearest ancestor `<form>` — it cannot observe arbitrary form state. It is for the submit button's UI, not for global form state.

## Revalidation — `revalidatePath`, `revalidateTag`, `redirect`

A mutation that the user sees must invalidate the cached read paths it affects. Three primitives:

| Primitive | What it does |
|---|---|
| `revalidatePath('/posts/123')` | Invalidates the cached Server Component output for the path; next request re-renders it |
| `revalidatePath('/posts/[id]', 'page')` | Invalidates the dynamic route pattern (all `/posts/*` pages) |
| `revalidateTag('comments')` | Invalidates all `fetch` calls or `cache(...)` reads tagged `'comments'`; finer-grained than path-based |
| `redirect('/posts/123')` | Throws a special redirect signal that becomes a `Location:` header in the response |

Design rule: every action that mutates state visible to a Server Component must call `revalidatePath` or `revalidateTag` to update the cache. Forgetting to revalidate produces stale UI after submission — the mutation succeeded server-side, but the page still shows the pre-mutation data.

`redirect` is for actions that should navigate after success (e.g., create-and-redirect-to-detail-page). It cannot be inside a try/catch — `redirect` throws, and catching swallows the redirect signal.

## Bound Arguments

`.bind()` (the JavaScript built-in) pre-fills action arguments at the server side — useful for passing IDs without exposing them as form fields:

```tsx
// Server Component
export default async function Post({ params }) {
  const deletePost = deletePostAction.bind(null, params.id)
  return (
    <form action={deletePost}>
      <button type="submit">Delete</button>
    </form>
  )
}

// 'use server' module
export async function deletePostAction(id: string, formData: FormData) {
  // id is bound; formData comes from the form
}
```

Bound arguments do not need to be serialized at submission time because they were captured server-side. They are also not user-controllable from the form, so they are safer than `<input type="hidden">` for IDs that the user must not change. But they are still visible to anyone reading the network request — never bind a secret.

## Security Discipline

| Concern | Reality | Required action |
|---|---|---|
| Authorization | The function is publicly invokable by anyone who finds its identifier | Check the session in every action; reject anonymous calls explicitly |
| Authentication of the *acting user* | The function does not know who's calling unless you check | Read the session from cookies/headers; do not trust client-supplied user IDs |
| Input validation | The function receives FormData / serialized arguments; the server has no type guarantee from the call-site types | Validate every input with a runtime schema (Zod, Valibot, ArkType) |
| Authorization of the *operation* | Even authenticated users may not be allowed to delete this post | Check ownership / permission inside the action body before mutating |
| CSRF | Server Actions in Next.js include built-in same-origin checks; cross-origin POSTs are rejected | Default protection is on; configure `serverActions.allowedOrigins` only when explicitly proxying |
| Rate limiting | The endpoint is public; spam is possible | Implement per-action rate limits in middleware or inside the action |
| Bound arguments | Visible in the network request despite not being a form field | Never bind secrets, even via `.bind()` |

The single most common Server Action bug: forgetting that the function is publicly reachable. A function called `deletePost(postId: string)` is a `POST` that any browser can craft with any `postId` — the type signature does not protect the server. Treat actions like API routes that happen to share types with your UI.

## Common Anti-Patterns

| Anti-pattern | Why it's wrong | Fix |
|---|---|---|
| Trusting client-supplied user ID as the actor | Anyone can submit any ID | Read user ID from the server-side session, not from form fields |
| Validating only on the client | Server has no guarantee of client-side validation | Mandatory server-side validation; client-side is UX, not security |
| Calling fetch('/api/...') instead of a Server Action for an internal mutation | Duplicate code, type drift between client and server | Use a Server Action — one declaration, one wire format |
| Forgetting `revalidatePath` / `revalidateTag` | Cached Server Component shows stale data after mutation | Call the appropriate revalidation primitive in every mutation |
| Wrapping `redirect` in try/catch | The redirect signal is swallowed | Place `redirect` outside the try block, or rethrow caught redirect signals |
| Server Action that returns a non-serializable value (Date object with methods, function, class instance) | Cannot cross the boundary back to the client | Return plain objects only |
| Form that doesn't work without JavaScript (e.g., requires a click handler that calls the action) | Defeats progressive enhancement | Use `<form action={serverAction}>`, not `<button onClick={() => serverAction()}>` |
| Action that performs side effects regardless of validation result | Partial failure with database state changed and error returned | Validate before any mutation; structure as parse-then-mutate |

## Verification

After applying this skill, verify:

- [ ] Every Server Action checks authentication before any mutation.
- [ ] Every Server Action validates inputs with a runtime schema, not just TypeScript types.
- [ ] Every Server Action that mutates Server-Component-visible state calls `revalidatePath` or `revalidateTag`.
- [ ] No action trusts client-supplied user IDs, role flags, or permission claims.
- [ ] Forms work without JavaScript: native browser submission to the action's endpoint produces the same result as the React-intercepted path.
- [ ] No `redirect` is inside a try/catch (or, if it must be, redirect signals are explicitly rethrown).
- [ ] Bound arguments via `.bind()` carry only non-secret data.
- [ ] Rate limiting exists for actions that can be invoked frequently or anonymously.
- [ ] Server Actions return only serializable values to Client Components.

## Grounding Sources

- React docs — [`'use server'`](https://react.dev/reference/rsc/use-server). The directive contract.
- React docs — [`useActionState`](https://react.dev/reference/react/useActionState) and [`useFormStatus`](https://react.dev/reference/react-dom/hooks/useFormStatus). The React 19 hooks for action state and pending UI.
- Next.js docs — [Server Actions and Mutations](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations). The canonical implementation reference.
- Next.js docs — [`revalidatePath`](https://nextjs.org/docs/app/api-reference/functions/revalidatePath) and [`revalidateTag`](https://nextjs.org/docs/app/api-reference/functions/revalidateTag). Cache invalidation primitives.
- Next.js docs — [`redirect`](https://nextjs.org/docs/app/api-reference/functions/redirect). The redirect-as-throw mechanism.
- Vercel — [Server Actions security model and the Same-Origin Check](https://nextjs.org/blog/security-nextjs-server-components-actions). The framework's security defaults and what they don't cover.
- Wieruch, R. — [Server Actions in Next.js](https://www.robinwieruch.de/next-server-actions/). Comprehensive walkthrough with progressive-enhancement and form-state patterns.

## Do NOT Use When

| Instead of this skill | Use | Why |
|---|---|---|
| Designing the read path (fetching data on render with Server Components) | `server-components-design` | server-components-design owns the read path; this skill owns the write path. They share infrastructure but solve different problems. |
| The serialization mechanics of the `'use client'` / `'use server'` boundary | `client-server-boundary` | client-server-boundary owns the boundary semantics; this skill applies them to mutations specifically. |
| Designing a public REST API consumed by mobile clients or third parties | `api-design` | api-design owns HTTP contracts intended for external consumption. Server Actions are internal to one app's UI. |
| Form UX patterns (validation states, layout, accessibility, microcopy) | `form-ux-architecture` | form-ux-architecture owns the visual/interaction design of the form; this skill owns the server execution model. |
| Hook discipline (Rules of Hooks, dependency arrays, custom hooks) | `hooks-patterns` | hooks-patterns covers Client Component hook usage. `useActionState` is a hook called inside Client Components but governed by hooks-patterns' rules. |
