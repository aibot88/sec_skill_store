---
name: nextjs-troubleshooting
description: >
  This skill should be used when debugging or troubleshooting issues in a Next.js application.
  Trigger when: encountering hydration mismatch errors; debugging serialization failures across
  Server/Client boundaries; investigating stale data or auth checks in layouts; diagnosing
  request waterfall performance issues; troubleshooting memory leaks in Docker or development;
  debugging build failures or static generation errors; investigating middleware bypass issues;
  fixing environment variable problems; diagnosing caching issues; troubleshooting deployment
  failures; encountering "Cannot read properties of undefined" in Server Components; fixing
  OOM crashes in containers; debugging slow page loads; or resolving any Next.js error,
  warning, or unexpected behavior.
---

# Next.js Troubleshooting: Diagnostic Guide

Use this systematic approach to diagnose and fix common Next.js issues. Start with the diagnostic decision tree, then drill into the specific problem category.

## Diagnostic Decision Tree

```
Issue Type?
├── Build/Deploy Error → Section 1
├── Runtime Error → Section 2
├── Performance Problem → Section 3
├── Data/Caching Issue → Section 4
├── Security/Auth Issue → Section 5
└── Memory/Resource Issue → Section 6
```

---

## 1. Build & Deployment Errors

### Static Generation Failures
**Symptom:** Build fails with "Error occurred prerendering page" or dynamic API calls during static generation.

**Diagnosis:** A page being statically generated is calling a runtime API (`cookies()`, `headers()`, `searchParams`) or a dynamic data source without proper configuration.

**Fix:** Either:
- Wrap the dynamic component in `<Suspense>` to enable Partial Prerendering
- Export `const dynamic = 'force-dynamic'` for fully dynamic pages
- Move the dynamic call inside a Client Component or Server Action

### Missing Environment Variables
**Symptom:** Build succeeds but runtime errors like "Cannot read property of undefined" or API calls failing in production.

**Diagnosis:** Variables available in `.env.local` during dev are not configured in the production environment.

**Fix:** Verify all required env vars are set in the deployment platform. Use `NEXT_PUBLIC_` only for browser-safe values. Check `instrumentation.ts` for startup validation.

---

## 2. Runtime Errors

### Serialization Failures Across Boundaries
**Symptom:** "Error: Only plain objects, and a few built-ins, can be passed to Client Components" or silently stripped data.

**Cause:** Passing non-serializable props from Server to Client Components — `Date` objects, `Map`, `Set`, functions, class instances.

**Fix:** Convert to serializable types before passing:
```typescript
// Server Component
const date = await getDate();
return <ClientComponent dateString={date.toISOString()} />;

// Client Component
const date = new Date(dateString);
```

### Hydration Mismatches
**Symptom:** "Warning: Text content did not match" or "Hydration failed because the server rendered HTML didn't match the client."

**Cause:** Server-rendered HTML differs from client-rendered output. Common triggers:
- Browser extensions injecting elements
- `Date.now()` or `Math.random()` in render
- Conditional rendering based on `window` or `localStorage`
- `typeof window !== 'undefined'` checks in render path

**Fix:**
- Use `useEffect` for browser-only logic (runs only on client)
- Use `suppressHydrationWarning` only for intentional mismatches (e.g., timestamps)
- Wrap browser-dependent UI in a Client Component with `useEffect` state initialization

### "Cannot read properties of undefined"
**Symptom:** Server Component crashes accessing properties on data that should exist.

**Diagnosis:** Usually a data fetching issue — the query returned `null`/`undefined` due to missing auth, wrong params, or database connectivity.

**Fix:** Add null checks and verify the DAL function returns data. Check auth state. Use TypeScript strict null checks.

---

## 3. Performance Issues

### Unintentional Request Waterfalls
**Symptom:** Page loads slowly despite fast individual queries.

**Diagnosis:** Sequential `await` calls where queries don't depend on each other:
```typescript
// BAD: Waterfall — total time = query1 + query2 + query3
const user = await getUser(id);
const posts = await getPosts(id);
const comments = await getComments(id);
```

**Fix:** Parallelize independent requests:
```typescript
// GOOD: Parallel — total time = max(query1, query2, query3)
const [user, posts, comments] = await Promise.all([
  getUser(id),
  getPosts(id),
  getComments(id),
]);
```

### Large JavaScript Bundle
**Symptom:** Slow TTI, large "First Load JS" in build output.

**Fix:**
1. Run `@next/bundle-analyzer` to identify heavy dependencies
2. Move non-interactive components to Server Components (zero JS)
3. Use `next/dynamic` for below-the-fold interactive components
4. Check for barrel file imports pulling in entire libraries

### Slow LCP
**Symptom:** Largest Contentful Paint > 2.5s.

**Fix:** Ensure the LCP image uses `next/image` with `priority` prop. Remove `loading="lazy"` from above-the-fold images. Check server response time (TTFB).

---

## 4. Data & Caching Issues

### Stale Data After Mutations
**Symptom:** Form submits successfully but the page shows old data.

**Fix:** Call `revalidatePath()` or `revalidateTag()` in the Server Action after the mutation. Ensure the revalidation target matches the cached route/tag.

### Stale Auth Checks in Layouts
**Symptom:** User logs out but still sees authenticated content, or auth state is stale across navigation.

**Cause:** `layout.tsx` does not re-render on sibling navigation — auth checks placed there become stale.

**Fix:** Move authorization checks to `page.tsx` or the Data Access Layer. Call the DAL directly in each page that needs auth verification.

### Unexpected Caching (Next.js 14 and earlier)
**Symptom:** Data seems frozen, changes don't appear.

**Cause:** Prior to Next.js 15, fetch was cached by default.

**Fix:** Upgrade to Next.js 15+ (uncached by default). Or explicitly configure `cache: 'no-store'` on fetch calls. Use the `"use cache"` directive for intentional caching.

---

## 5. Security & Auth Issues

### Middleware Bypass
**Symptom:** Unauthenticated users accessing protected routes despite middleware checks.

**Cause:** Middleware can be bypassed via spoofed headers (CVE-2025-29927) or misconfigured matchers.

**Fix:** Never rely solely on middleware for auth. Re-verify authentication in every Server Action, Route Handler, and DAL function independently.

### Environment Variable Leakage
**Symptom:** Secret API keys visible in browser DevTools network tab or page source.

**Cause:** Using `NEXT_PUBLIC_` prefix on sensitive variables, or importing a server module into a Client Component.

**Fix:** Remove `NEXT_PUBLIC_` prefix from secrets. Add `import 'server-only'` to modules with env var access. Restrict `process.env` to the DAL.

---

## 6. Memory & Resource Issues

### Memory Leaks in Development
**Symptom:** Dev server RAM climbs to several GB over time, eventually crashing.

**Cause:** Known issue with Next.js dev server memory management, especially with large codebases and frequent HMR.

**Fix:** Restart the dev server periodically. Consider using Turbopack (`next dev --turbopack`) which has improved memory characteristics.

### OOM Crashes in Docker/Kubernetes
**Symptom:** Container killed with OOM (Out of Memory) signal in production.

**Cause:** Documented linear memory growth in recent Next.js versions when containerized.

**Fix:**
- Set explicit Node.js memory limits: `NODE_OPTIONS="--max-old-space-size=512"`
- Configure container resource limits and health checks
- Use a minimal base image with non-root user
- Monitor memory with Prometheus/Grafana and set alerts
- Consider process restarts on memory thresholds

### Encryption Key Mismatch (Multi-Instance)
**Symptom:** Server Actions fail intermittently in multi-instance deployments.

**Cause:** Each instance generates a different encryption key for Server Actions.

**Fix:** Set `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` environment variable consistently across all instances.

---

---

## 7. General Debugging Approach

When encountering an unknown error:

1. **Read the full error message** — Next.js errors are usually descriptive.
2. **Check the error location** — server (terminal) vs client (browser console).
3. **Identify the boundary** — is the error at the Server→Client boundary?
4. **Check the rendering mode** — is the page static, dynamic, or streaming?
5. **Reproduce in production build** — run `npm run build && npm run start` (dev and prod behave differently).
6. **Check Next.js version** — behavior changes significantly between 14, 15, and 16.
7. **Search Next.js GitHub issues** — many errors are known with documented workarounds.

---

## Additional Resources

### Reference Files

For additional errors not covered above:
- **`references/common-errors.md`** — Supplementary error lookup table covering build/module errors, TypeScript errors, middleware/routing issues, and additional caching problems

### Related Skills

- **`nextjs-best-practices`** — Correct patterns that prevent these issues
- **`nextjs-security`** — Security-specific debugging (auth, middleware, headers)
- **`nextjs-testing`** — Testing to catch these issues before production
