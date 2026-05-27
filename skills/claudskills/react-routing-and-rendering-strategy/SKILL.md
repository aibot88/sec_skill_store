---
name: react-routing-and-rendering-strategy
description: Use when defining, reviewing, or hardening the routing topology and client rendering strategy of a standalone React SPA after the app scaffold exists and frontend architecture has decided rendering modes per route. Produces React Router 6 data-router topology (nested routes, loaders, actions, deferred data), CSR-only rendering posture with suspense and transition boundaries, per-route loading and error UI, route-level metadata and SEO posture, and protected-route gates and redirect flows wired to the auth provider baseline from the scaffold. Do not use for app scaffolding, global state or data-fetching libraries, design-system or accessibility work, performance budgeting, or any SSR/RSC/server-action rendering; use the other react archetype skills or the nextjs stack instead.
---

# React Routing and Rendering Strategy

## When to use

Invoke when adding or restructuring routing in a standalone React SPA, when translating a `frontend-architecture.md` route map into a React Router topology, or when hardening route-level loading, error, and auth-gate behavior.

Do not use for: project scaffolding or the auth provider baseline (use `react-app-scaffold-and-runtime`), global/server state libraries and data-fetching conventions (use `react-state-management-and-data-fetching`), design-system or a11y of route UIs (use `react-design-system-and-accessibility`), perf budgeting and code-split topology (use `react-performance-and-delivery-optimization`), or SSR/SSG/ISR/RSC/server actions (meta-framework territory — use the `nextjs` stack).

## Inputs

Required:

- An existing react app scaffold from `react-app-scaffold-and-runtime` (provides the auth provider/wrapper seam and error-boundary seam).
- Approved `frontend-architecture.md` with the route map and the rendering mode per route. For a standalone React SPA every route is CSR; if the architecture assigns SSR/SSG/streaming to any route, that route is out of scope here.

Optional:

- `architecture/security` decisions on the session model and which routes are protected and at what role/scope.
- `backend-architecture.md` for the API/loader data contracts routes depend on.
- SEO requirements (which routes need indexable metadata; a SPA's limits).
- Deep-link, redirect, and not-found UX requirements.

## Operating rules

- Consume the route map; do not invent it. Route hierarchy, which routes are protected, and the rendering mode per route come from `frontend-architecture.md` and `architecture/security`. If the route map or a protection rule is missing, pause and raise an ADR candidate against `frontend-architecture` or `architecture/security`.
- CSR only. This is the standalone-React rendering posture. If `frontend-architecture.md` assigns SSR, SSG, ISR, streaming, or RSC to a route, this skill does not implement it — it flags the route as belonging to the `nextjs` (meta-framework) stack and stops there.
- Use the React Router 6 data-router API (`createBrowserRouter`, route `loader`/`action`, `defer`/`Await`) as the default. Loaders fetch route-critical data; they do not replace the server-state layer the data-fetching skill owns — keep loader use to route-gating and route-critical bootstrapping, not application-wide caching.
- Every route defines its loading and error UI. A route without a `errorElement`/error boundary and a loading state is incomplete. Reuse the scaffold's error-boundary seam; do not introduce a competing top-level boundary.
- Protected routes gate via the auth provider seam from the scaffold. The gate checks session state from that provider, redirects unauthenticated users with a return-to target, and renders an accessible interstitial — it does not implement token storage or refresh (that is the data-fetching skill).
- Suspense and transitions are deliberate: route transitions use `startTransition`/router pending state; suspense boundaries are placed at route segments, not sprinkled per component. Justify each boundary.
- Route-level metadata is explicit. Each route sets its title and meta; the skill states the SPA's SEO limitation honestly (client-rendered metadata is weak for crawlers) and recommends escalation to the `nextjs` stack if real SEO is required by the architecture.
- Redirects and not-found are first-class: a typed not-found route, auth redirect with return-to, and post-login restore. No silent dead ends.
- Do not couple routing to a specific global-state library. The router owns URL state; the data-fetching skill owns server/global state. Keep the seam clean.

## Output contract

The routing and rendering implementation MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — protected-route gates enforce the session model from `architecture/security`; no auth bypass via client-only checks presented as security (the gate is UX; the API is the security boundary — state this).
- [observability-standards](../../../../../standards/observability-standards/README.md) — route transitions and route-level errors are reported through the scaffold's logging/error sink with the route as context.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — client-side routing works under a CDN/static host (SPA fallback to `index.html`, correct base path).
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — route path and route-id naming.

Upstream contract: `frontend-architecture.md` is the source of truth for the route map and per-route rendering mode; `architecture/security` is the source of truth for which routes are protected and the session model. If either is silent on a needed decision, pause and raise an ADR candidate. Any non-CSR route is handed off to the `nextjs` stack, not implemented here.

## Process

1. Load the route map and per-route rendering mode from `frontend-architecture.md` and the protection rules from `architecture/security`. Confirm the scaffold (auth provider seam, error-boundary seam) exists. If inputs are missing, pause and escalate.
2. Partition routes by rendering mode. Keep CSR routes in scope. List any SSR/SSG/streaming/RSC routes explicitly as out-of-scope handoffs to the `nextjs` stack and stop on those.
3. Build the React Router 6 data-router topology: nested route hierarchy, layout routes, dynamic segments, index routes, and the not-found route. Use `createBrowserRouter` with route objects.
4. Define route loaders for route-critical bootstrapping and gating data only. Use `defer`/`Await` for slow non-critical data. Do not turn loaders into the app's caching layer — document the seam to the data-fetching skill.
5. Define per-route loading UI (pending states via router `state`/`useNavigation`) and per-route `errorElement` wired to the scaffold's error-boundary seam. No route lacks both.
6. Implement protected-route gates: a gate component/loader that reads session state from the scaffold's auth provider seam, redirects unauthenticated/under-scoped users to login with a return-to param, renders an accessible interstitial, and restores the target post-login. State explicitly that this is UX enforcement and the API remains the security boundary.
7. Implement redirect and not-found behavior: typed not-found, legacy-path redirects, and trailing-slash/base-path handling for CDN hosting.
8. Wire route transitions: `startTransition`/router pending state for navigation, deliberate suspense boundaries at route segments with a one-line justification each.
9. Set route-level metadata (title/meta per route). State the SPA SEO limitation; if `frontend-architecture.md` requires crawlable SEO, raise the handoff to the `nextjs` stack rather than faking it.
10. Report route transitions and route errors through the scaffold's observability sink with route context.
11. Verify: build, run the route smoke (navigation across the hierarchy, a protected route unauthenticated → redirect → return, a not-found, a loader error → error UI). Document any skipped check rather than declaring success silently.
12. Validate against [security-standards](../../../../../standards/security-standards/README.md), [observability-standards](../../../../../standards/observability-standards/README.md), [deployment-standards](../../../../../standards/deployment-standards/README.md), and [naming-conventions](../../../../../standards/naming-conventions/README.md). Revise until all pass or document the gap.

## Outputs

Required:

- React Router 6 data-router configuration: route tree, layout/index routes, dynamic segments, not-found.
- Per-route loading UI and per-route error elements wired to the scaffold error-boundary seam.
- Protected-route gate(s) wired to the scaffold auth provider seam, with redirect + return-to + accessible interstitial.
- Route-level metadata wiring and an explicit SEO-limitation statement.
- Route transition/suspense configuration with per-boundary justification.

Output rules:

- Functional code, not placeholder routes.
- No non-CSR rendering implemented; such routes are documented handoffs to the `nextjs` stack.
- The auth gate consumes the scaffold seam and does not implement token logic.
- Loaders are scoped to route-critical/gating data, not used as the app cache.

## Quality checks

- [ ] The route map and per-route rendering mode are sourced from `frontend-architecture.md` (or an ADR candidate is raised).
- [ ] Every in-scope route is CSR; any SSR/SSG/streaming/RSC route is documented as a `nextjs`-stack handoff, not implemented.
- [ ] The topology uses the React Router 6 data-router API with a typed not-found route.
- [ ] Every route has both a loading state and an `errorElement` wired to the scaffold error-boundary seam.
- [ ] Protected routes gate via the scaffold auth provider seam with redirect, return-to, and an accessible interstitial; the code/comment states the API is the real security boundary.
- [ ] Loaders are limited to route-critical/gating data; the server-state seam to the data-fetching skill is documented.
- [ ] Suspense/transition boundaries are at route segments and each has a justification.
- [ ] Route-level metadata is set and the SPA SEO limitation is stated (with a `nextjs` handoff if real SEO is required).
- [ ] Route transitions and errors are reported through the scaffold observability sink with route context.
- [ ] Client routing works under a CDN/static host (SPA fallback, base path).

## References

- Upstream: [`architecture/frontend-architecture`](../../../../architecture/frontend-architecture/SKILL.md), [`architecture/security`](../../../../architecture/security/SKILL.md).
- Builds on: [`react-app-scaffold-and-runtime`](../react-app-scaffold-and-runtime/SKILL.md) (auth provider + error-boundary seams).
- Related react archetype skills: [`react-state-management-and-data-fetching`](../react-state-management-and-data-fetching/SKILL.md) (server/global state; token logic), [`react-design-system-and-accessibility`](../react-design-system-and-accessibility/SKILL.md) (accessible interstitials/auth UIs), [`react-performance-and-delivery-optimization`](../react-performance-and-delivery-optimization/SKILL.md) (route-level code splitting).
- Compatible patterns: [`microservices`](../../../../../architecture-patterns/microservices/README.md), [`cqrs`](../../../../../architecture-patterns/cqrs/README.md), [`real-time-systems`](../../../../../architecture-patterns/real-time-systems/README.md).
