---
name: server-components-design
description: "Use when designing or reviewing React Server Components: what an RSC can do (async, data fetching, server-only imports) versus what it cannot (state, effects, event handlers, browser APIs), where to draw the server/client boundary in the tree, and how RSC composes with Suspense to stream content without a separate API layer. Covers Next.js App Router as the canonical implementation, but the discipline is framework-agnostic. Do NOT use for the 'use client' directive mechanics (use client-server-boundary), hook discipline on Client Components (use hooks-patterns), rendering strategy choice (use rendering-models), or the server-action mutation surface (use server-actions-design when authored)."
license: MIT
allowed-tools: Read Grep
metadata:
  metadata: "{\"schema_version\":6,\"version\":\"1.0.0\",\"type\":\"capability\",\"category\":\"engineering\",\"domain\":\"engineering/frontend\",\"scope\":\"reference\",\"owner\":\"skill-graph-maintainer\",\"freshness\":\"2026-05-16\",\"drift_check\":\"{\\\\\\\"last_verified\\\\\\\":\\\\\\\"2026-05-16\\\\\\\"}\",\"eval_artifacts\":\"planned\",\"eval_state\":\"unverified\",\"routing_eval\":\"absent\",\"comprehension_state\":\"present\",\"stability\":\"experimental\",\"keywords\":\"[\\\\\\\"React Server Components\\\\\\\",\\\\\\\"RSC\\\\\\\",\\\\\\\"Next.js App Router\\\\\\\",\\\\\\\"async components\\\\\\\",\\\\\\\"server-side data fetching\\\\\\\",\\\\\\\"streaming RSC\\\\\\\",\\\\\\\"server/client component tree\\\\\\\",\\\\\\\"RSC payload\\\\\\\",\\\\\\\"Suspense boundaries with RSC\\\\\\\",\\\\\\\"data flow without API layer\\\\\\\"]\",\"triggers\":\"[\\\\\\\"should this be a Server Component or a Client Component\\\\\\\",\\\\\\\"can I fetch data here\\\\\\\",\\\\\\\"why can't I use useState in this file\\\\\\\",\\\\\\\"how does data move from server to client\\\\\\\",\\\\\\\"do I need an API route\\\\\\\",\\\\\\\"why is the bundle so large\\\\\\\"]\",\"examples\":\"[\\\\\\\"decide whether a dashboard widget should be a Server Component (fetches and renders) or a Client Component (interactive)\\\\\\\",\\\\\\\"explain why a Server Component cannot pass a function as a prop to a Client Component\\\\\\\",\\\\\\\"design a page where the layout fetches user data once and child widgets fetch their own data, with Suspense streaming each in\\\\\\\",\\\\\\\"audit a component tree for unnecessary 'use client' boundaries that pull static rendering into the bundle\\\\\\\"]\",\"anti_examples\":\"[\\\\\\\"add a click handler to an existing component (use hooks-patterns and client-server-boundary)\\\\\\\",\\\\\\\"choose between SSR and SSG for a marketing page (use rendering-models)\\\\\\\",\\\\\\\"build the form-submission mutation flow (use server-actions-design when authored)\\\\\\\",\\\\\\\"design the public API for a third-party integration (use api-design)\\\\\\\"]\",\"relations\":\"{\\\\\\\"related\\\\\\\":[\\\\\\\"client-server-boundary\\\\\\\",\\\\\\\"rendering-models\\\\\\\",\\\\\\\"hooks-patterns\\\\\\\",\\\\\\\"streaming-architecture\\\\\\\",\\\\\\\"suspense-patterns\\\\\\\"],\\\\\\\"boundary\\\\\\\":[{\\\\\\\"skill\\\\\\\":\\\\\\\"client-server-boundary\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"client-server-boundary owns the serialization-and-directive mechanics of the boundary itself ('use client', what can cross, RSC payload format); server-components-design owns the discipline of which work belongs on the server side of that boundary.\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"rendering-models\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"rendering-models owns the strategic decision among SSR, SSG, ISR, and CSR; server-components-design operates within the App Router / RSC paradigm and is one rendering mode among several.\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"hooks-patterns\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"hooks-patterns covers state and effect discipline on Client Components; Server Components cannot use those primitives at all, so the two skills cover disjoint surfaces.\\\\\\\"}],\\\\\\\"verify_with\\\\\\\":[\\\\\\\"code-review\\\\\\\",\\\\\\\"rendering-models\\\\\\\"]}\",\"mental_model\":\"|\",\"purpose\":\"|\",\"boundary\":\"|\",\"analogy\":\"A Server Component is to a React tree what a printed page is to a book — the typesetter (server) sets the lead, presses the ink, and ships the printed page (RSC payload); the reader's table lamp (Client Component) is wired and switchable at the reader's end. You do not ship the typesetter to the reader's living room, and you do not ship the lamp's wiring to the printer — the boundary is where 'this never changes once it leaves my workshop' ends and 'this responds to who touches it' begins.\",\"misconception\":\"|\",\"concept\":\"{\\\\\\\"definition\\\\\\\":\\\\\\\"A React Server Component is a component that runs only on the server, never ships to the browser as JavaScript, can be async, and can directly access server-side resources (databases, file system, secrets) — its output is serialized to a wire format (the RSC payload) and reconstituted into the client tree without a separate API layer. Server Components compose with Client Components in a single tree, but the directionality is one-way: a Server Component can render a Client Component, but a Client Component cannot import a Server Component as a child.\\\\\\\",\\\\\\\"mental_model\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"purpose\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"boundary\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"taxonomy\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"analogy\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"misconception\\\\\\\":\\\\\\\"|\\\\\\\"}\",\"skill_graph_source_repo\":\"https://github.com/jacob-balslev/skill-graph\",\"skill_graph_protocol\":\"Skill Metadata Protocol v5\",\"skill_graph_project\":\"Skill Graph\",\"skill_graph_canonical_skill\":\"skills/server-components-design/SKILL.md\"}"
  skill_graph_source_repo: "https://github.com/jacob-balslev/skill-graph"
  skill_graph_protocol: Skill Metadata Protocol v4
  skill_graph_project: Skill Graph
  skill_graph_canonical_skill: skills/server-components-design/SKILL.md
---

# Server Components Design

## Coverage

The discipline of designing React Server Components (RSC): what an RSC is *for*, what it can do that Client Components cannot, what it cannot do, how the server/client boundary shapes the component graph and the data-flow graph, how RSC composes with Suspense to stream content from the server in chunks, why Server Components remove the need for a separate API layer for read-path data, and the recurring design questions a reviewer asks of any RSC tree. Next.js App Router is the canonical implementation referenced throughout; the discipline applies to any RSC implementation (Remix RSC, Waku, hand-rolled RSC servers) since the underlying primitive is the React RFC, not a single framework.

## Philosophy

The original React component model collapsed two roles into one function: produce HTML for the initial render, and produce a virtual DOM update in response to client-side state. Server-Side Rendering pre-React-18 tried to make that single function run twice — once on the server to produce HTML, once on the client to produce the interactive tree — and pay for it with hydration: a full re-execution on the client to bind event handlers and reconstruct state.

Hydration has two costs the industry tolerated for a decade: every component must ship to the client (bundle size grows with the page), and every component re-runs on the client (CPU cost grows with the page). React Server Components separate the two roles into different *kinds* of component. A Server Component runs once, on the server, and produces a serialized output that the client uses directly — no shipping, no re-execution. A Client Component is what we used to call "a component": ships to the browser, runs on render and on every interaction.

The discipline of RSC design is to push as much of the tree as possible to the server side of the boundary, and to draw the line as close to the actual interactive leaves as possible. A button needs `useState`; the dashboard surrounding the button does not. A chart that responds to filter clicks is interactive; the page header above it is not. The win is real: bundle size shrinks toward "only the interactive parts," and the server has direct access to databases, file systems, and secrets without an intermediating API layer.

But the boundary is unforgiving. A Server Component cannot use hooks. It cannot read state. It cannot attach event handlers. Anything that crosses to a Client Component must be serializable — strings, numbers, plain objects, arrays, Promises (in React 19), JSX, and React elements; not functions, not class instances, not symbols, not Maps. The discipline is to express the work in shapes that respect that constraint, and to use Suspense boundaries to let the server-rendered tree stream piece by piece rather than blocking on the slowest piece.

## What a Server Component Can Do (And What a Client Component Cannot)

| Capability | Server Component | Client Component |
|---|---|---|
| `async` / `await` at the component level | Yes | No (React 18); promises must be unwrapped via `use()` (React 19) |
| Direct database queries, file reads, secret access | Yes | No — would leak to the browser |
| Read environment variables (including `PROCESS_SECRET`-style) | Yes | No — only `NEXT_PUBLIC_*` vars are safe |
| Import server-only libraries (Postgres driver, file system) | Yes | No — bundling would fail (or worse, succeed and leak) |
| Subscribe to browser events (`onClick`, `onChange`) | No | Yes |
| Manage state (`useState`, `useReducer`) | No | Yes |
| Side effects (`useEffect`) | No | Yes |
| Read browser APIs (`window`, `localStorage`) | No | Yes |
| Render Client Components as children | Yes — boundary crosses here | Yes |
| Be rendered *as a child* of a Client Component | Only via the `children` prop pattern | n/a |

The boundary is not just about what's available; it's about what makes sense. A Server Component that renders the same output regardless of any client state is doing the right thing. A Server Component that wants to know "what tab did the user click on" is asking the wrong primitive — that's Client Component territory.

## The Composition Pattern: Client at the Leaves, Server Everywhere Else

A naive boundary draws the line at the page level: "this page needs interactivity, so the whole page is a Client Component." This loses most of the RSC benefit.

A disciplined boundary draws the line at the *interactive leaves*: the button that toggles a dropdown is a Client Component; the dropdown's structure, the surrounding layout, the data feeding it — all Server Components.

The enabling pattern is **passing Server Components as `children` to Client Components**:

```tsx
// app/dashboard/page.tsx — Server Component
import { ServerData } from './ServerData'
import { ClientFilterBar } from './ClientFilterBar'

export default async function Dashboard() {
  const data = await db.getDashboardData()
  return (
    <ClientFilterBar>
      <ServerData data={data} />
    </ClientFilterBar>
  )
}

// ClientFilterBar.tsx — Client Component with state
'use client'
import { useState } from 'react'

export function ClientFilterBar({ children }: { children: React.ReactNode }) {
  const [filter, setFilter] = useState('all')
  return (
    <div>
      <select onChange={e => setFilter(e.target.value)}>...</select>
      {children}  {/* Server Component renders here */}
    </div>
  )
}
```

The `children` prop is *content*, not *components-to-import*. The Client Component receives the already-rendered React element from the server tree. This is the only way to put a Server Component "inside" a Client Component visually without violating the import rule.

## The Import Rule and Why It Matters

A Client Component cannot `import` a Server Component. Not "should not" — *cannot*, because the bundler running on the client would have to bundle the Server Component, and Server Components are not allowed to ship.

But a Server Component *can* `import` a Client Component. The Client Component file is marked `'use client'` at its top, the bundler treats it as a client-bundle entry point, and the Server Component renders a reference to it (in the RSC payload) that the client runtime resolves to the bundled component.

The directionality matters for tree design:

- Top-down: Server → Server → Server → Client → (only more Client below this point).
- Pierce-through via children: Server → Client → (children prop receives) → Server → Server.

A tree that follows the first pattern naturally pushes work to the server. A tree that violates it (a Client Component near the root that needs to render a Server Component as a non-children child) cannot be expressed; you'll be forced to restructure.

## Data Flow Without an API Layer

The classic React data-fetching pattern:

1. Browser requests page → SSR returns HTML
2. Browser hydrates page
3. Client Component mounts, runs `useEffect`, calls `/api/data`
4. API route handler runs, queries database, returns JSON
5. Component re-renders with data

RSC collapses steps 1–5 to:

1. Browser requests page → Server Component runs, queries database directly, returns RSC payload (with data already baked in)

The `/api/data` route does not need to exist. The Server Component reaches into the database, passes the result to a child component as a prop, and the prop arrives at the client *as the rendered output* — serialized in the RSC payload, never round-tripped through a JSON API.

When does an API route still make sense? When something *outside* this app needs to read the data: a mobile app, a third-party integration, a server-to-server call. The API layer is no longer the only way to get data into the page; it's only what you need when there are multiple consumers.

## Suspense and Streaming RSC

A Server Component that awaits a slow query blocks the entire HTML response. Suspense unblocks the pattern: wrap the slow component in `<Suspense fallback={...}>` and the server flushes the surrounding tree immediately, then streams in the slow component's output when it resolves.

```tsx
// app/dashboard/page.tsx — Server Component
export default async function Dashboard() {
  return (
    <>
      <Header />
      <Suspense fallback={<SkeletonChart />}>
        <SlowChartData />  {/* awaits a 2-second query */}
      </Suspense>
      <Suspense fallback={<SkeletonTable />}>
        <SlowTableData />  {/* awaits a 1.5-second query */}
      </Suspense>
    </>
  )
}
```

Both `SlowChartData` and `SlowTableData` start their queries in parallel (the Server Component renders both subtrees, and each `await` is a Promise that the renderer holds open). The chart and table fallback HTML ships immediately; the actual content streams in as each query resolves. Time-to-first-byte is bounded by the fastest non-Suspended path; time-to-interactive of each section is bounded by that section's own query.

Two design rules:

1. **Co-locate the Suspense boundary with the slow data, not above it.** A boundary too high makes more of the page wait; a boundary too low produces visible layout shift as content pops in.
2. **Trigger parallel data fetches at the same level.** If two queries don't depend on each other, render their components as siblings (not parent/child) so their awaits happen in parallel.

See `suspense-patterns` (when authored) for the wider Suspense discipline including error boundaries, nested fallbacks, and the relationship to React's transition APIs.

## Common Anti-Patterns

| Anti-pattern | Why it's wrong | Fix |
|---|---|---|
| Whole page marked `'use client'` to use one button | Loses all RSC benefit; ships entire page as client bundle | Move `'use client'` to the leaf component that actually needs it |
| `useEffect` to fetch data on mount | Hydration delay + double-fetch + lost streaming | Fetch in a Server Component ancestor and pass data as prop |
| Importing a Client Component that wraps `children` and trying to put a Server Component import inside | Bundler treats the Server Component as client code | Pass the Server Component as `children` from a Server Component parent |
| `await fetch('/api/data')` in a Server Component | Spending a round-trip for data you could query directly | Query the database directly; the API route is now redundant |
| Passing a function (`onClick`) from Server Component to Client Component | Not serializable across the boundary | Define the handler in the Client Component, pass primitive props instead |
| Reading `window` or `document` in a Server Component | Will crash at render time | Move browser-API code to a Client Component or to a `useEffect` |
| One giant Suspense boundary at the page root | All slow content blocks together — no streaming benefit | Place boundaries near the slow data, one per independent slow section |

## Verification

After applying this skill, verify:

- [ ] `'use client'` appears at the leaf where interactivity actually starts, not higher in the tree.
- [ ] No Server Component imports a Client Component's internals; the Client Component imports from `'use client'`-marked files only at its top level.
- [ ] No serialization-breaking values cross the boundary (no functions, no class instances, no Maps/Sets unless explicitly supported).
- [ ] Slow data fetches are wrapped in Suspense boundaries co-located with the data.
- [ ] No `useEffect` fetches for data that could be fetched server-side.
- [ ] Server Components do not call hooks, do not attach event handlers, and do not read browser APIs.
- [ ] Client Components do not import server-only libraries (DB drivers, file system modules, secret-reading helpers).
- [ ] The component tree expresses the actual interactivity boundary; rebuild it if a Client Component is forced to wrap Server Components it should be a sibling of.

## Grounding Sources

- React RFC — [Server Components RFC](https://github.com/reactjs/rfcs/blob/main/text/0188-server-components.md). The original proposal and the formal model.
- React docs — [Server Components](https://react.dev/reference/rsc/server-components). Official reference for the runtime contract.
- React docs — [`'use client'`](https://react.dev/reference/rsc/use-client) and [`'use server'`](https://react.dev/reference/rsc/use-server). The directive semantics.
- Next.js docs — [Server and Client Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components) and [Composition Patterns](https://nextjs.org/docs/app/building-your-application/rendering/composition-patterns). The canonical working implementation.
- Vercel — [How React Server Components Work](https://vercel.com/blog/understanding-react-server-components). Walk-through of the RSC payload and rendering pipeline.
- Markbåge, S. et al. — [Introducing Zero-Bundle-Size React Server Components](https://legacy.reactjs.org/blog/2020/12/21/data-fetching-with-react-server-components.html). The first public introduction; useful for the design rationale.
- Akinmade Adeleke, A. — [The Forensics of React Server Components](https://www.smashingmagazine.com/2024/05/forensics-react-server-components/). Deep dive on the RSC payload format and tree reconstruction.

## Do NOT Use When

| Instead of this skill | Use | Why |
|---|---|---|
| The mechanics of the `'use client'` / `'use server'` directive boundary itself (serialization rules, what crosses, RSC payload format) | `client-server-boundary` | client-server-boundary owns the boundary as a serialization mechanism; this skill owns the *design discipline* of where to draw the boundary in your component graph. |
| Hook discipline on the Client Component side (Rules of Hooks, useEffect, useMemo) | `hooks-patterns` | hooks-patterns covers what Client Components do correctly. Server Components cannot use hooks at all. |
| Choosing between SSR, SSG, ISR, and CSR rendering strategies | `rendering-models` | rendering-models owns the strategic rendering choice. RSC is one rendering mode among several. |
| Designing the Server Actions / form-mutation surface | `server-actions-design` (when authored) | Server Actions are the *write* path; Server Components are the *read* path. They share infrastructure but have distinct design concerns. |
| Streaming patterns broader than RSC (HTTP/2 push, SSE, WebSockets, AI streaming) | `streaming-architecture` | streaming-architecture covers streaming as a general protocol concern. RSC streaming is one application of that toolkit. |
