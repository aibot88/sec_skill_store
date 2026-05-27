---
name: react-state-management-and-data-fetching
description: Use when defining, reviewing, or hardening client state and data fetching for a standalone React SPA after the app scaffold and routing exist and frontend architecture has decided the state-tier model and data-fetching strategy. Produces a 4-tier state discipline (URL, server, global, local), a server-state data-fetching layer (TanStack Query default, or RTK Query/Apollo), query and mutation conventions, cache and revalidation policy, optimistic-update posture, and the auth-token storage, refresh, authorization-header, logout-propagation, and CSRF wiring that the scaffold and routing skills deferred. Do not use for app scaffolding, routing topology, design-system or accessibility work, or performance budgeting; use the other react archetype skills instead.
---

# React State Management and Data Fetching

## When to use

Invoke when introducing or restructuring client state and data fetching in a standalone React SPA, when translating the `frontend-architecture.md` state-tier model and data-fetching strategy into concrete libraries and conventions, or when implementing/hardening the auth-token lifecycle the scaffold and routing skills left as a seam.

Do not use for: project scaffolding or the auth provider baseline (use `react-app-scaffold-and-runtime`), route topology and route gates (use `react-routing-and-rendering-strategy`), design-system or a11y (use `react-design-system-and-accessibility`), or perf/bundle work (use `react-performance-and-delivery-optimization`).

## Inputs

Required:

- An existing react app scaffold (`react-app-scaffold-and-runtime`, provides the auth provider/wrapper seam) and routing (`react-routing-and-rendering-strategy`, consumes session state and exposes the protected-route gate).
- Approved `frontend-architecture.md` with the 4-tier state model (what lives in URL, server cache, global client, local) and the data-fetching strategy (library, cache policy, optimistic posture).
- `architecture/security` decisions on token strategy: token type, storage location (cookie vs memory vs storage), refresh model, CSRF posture, and logout/session-revocation behavior.

Optional:

- `backend-architecture.md` API contracts: endpoints, error envelope, idempotency keys, pagination shape, auth header/cookie expectation.
- Real-time requirements (subscriptions/websocket) feeding server state.
- Multi-tab session-sync requirements.

## Operating rules

- Consume the state model; do not invent it. Which data is URL vs server vs global vs local, and the cache/optimistic policy, come from `frontend-architecture.md`. The token strategy comes from `architecture/security`. If either is missing a decision this skill needs, pause and raise an ADR candidate.
- Enforce the 4-tier discipline strictly: **URL state** (filters, pagination, selected entity) lives in the router and is owned by the routing skill's surface — read it, do not duplicate it into global state; **server state** lives in the data-fetching cache (TanStack Query default), never hand-rolled in `useEffect`; **global client state** (cross-route UI, session-derived flags) lives in a minimal store (Zustand default / RTK); **local state** stays in the component. Data in the wrong tier is a defect to fix, not to work around.
- Server state is not global state. Do not mirror query results into Zustand/Redux. The query cache is the source of truth for server data; derived selections are computed, not copied.
- This skill owns the auth-token lifecycle: storage location per the `architecture/security` decision, refresh (single-flight refresh, request queue during refresh, refresh-failure → logout), authorization-header or cookie attachment at the transport layer, logout state propagation (clear caches, broadcast across tabs), and CSRF token wiring for cookie-based auth. The scaffold's provider seam is populated here.
- Token storage follows the security decision, not convenience. If `architecture/security` mandates httpOnly cookies, do not fall back to `localStorage`; if it mandates in-memory, do not persist. Deviation requires an ADR candidate, not a silent choice.
- Mutations define their cache effect explicitly: invalidate, update, or refetch the affected queries. Optimistic updates require a rollback path and an error reconciliation; no optimistic update without rollback.
- Every query and mutation has consistent conventions: query-key factory, typed errors mapped from the backend error envelope, retry policy (no retry on 4xx auth/validation), and stale/cache-time tied to the architecture's revalidation policy.
- Logout and auth-expiry clear all server-state caches and reset global stores. A stale authenticated cache after logout is a security defect.
- Keep transport concerns (auth headers, refresh, CSRF, base URL, error mapping) in one client/interceptor layer, not scattered per call site.
- Do not couple the data layer to routing internals beyond reading URL state through the router's public API; keep the seam clean both directions.

## Output contract

The state and data-fetching implementation MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — token storage matches the `architecture/security` decision; no tokens in the bundle or logs; CSRF wired for cookie auth; caches cleared on logout/expiry.
- [api-standards](../../../../../standards/api-standards/README.md) — requests honor the backend contract: error envelope mapping, pagination shape, idempotency-key headers on unsafe mutations.
- [observability-standards](../../../../../standards/observability-standards/README.md) — request failures and refresh failures are reported through the scaffold's error sink with correlation context.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — query-key, store, and hook naming.

Upstream contract: `frontend-architecture.md` is the source of truth for the state-tier model and data-fetching/cache strategy; `architecture/security` is the source of truth for token type, storage, refresh, CSRF, and logout behavior. If either is silent on a needed decision, pause and raise an ADR candidate rather than choosing for convenience.

## Process

1. Load the state-tier model and data-fetching strategy from `frontend-architecture.md` and the token strategy from `architecture/security`. Confirm the scaffold (auth provider seam) and routing (URL state, protected gate) exist. If inputs are missing, pause and escalate.
2. Map every piece of application data to exactly one tier (URL / server / global / local) with a one-line justification. Flag any data the architecture placed ambiguously and resolve via ADR candidate if needed.
3. Establish the server-state layer: install and configure the chosen library (TanStack Query default), the query client (stale/cache time per revalidation policy), a query-key factory, and typed error mapping from the backend error envelope.
4. Establish the transport/client layer: base URL from runtime config, the interceptor that attaches auth (header or cookie), maps errors, and triggers refresh; idempotency-key headers on unsafe mutations per `api-standards`.
5. Implement the auth-token lifecycle into the scaffold's provider seam: storage per the security decision, single-flight refresh with a request queue, refresh-failure → logout, and session-derived flags exposed to the routing gate (without duplicating server state).
6. Implement logout and auth-expiry handling: clear the query cache, reset global stores, broadcast across tabs (storage event/BroadcastChannel), and route to login via the routing skill's redirect.
7. Establish the global client store (Zustand default / RTK): only cross-route UI and session-derived flags; explicitly exclude server data. Document what belongs here vs the query cache.
8. Define query conventions: list/detail/infinite patterns, pagination aligned to the backend shape, suspense vs status-based usage consistent with the routing skill's boundaries, and retry policy (no retry on auth/validation 4xx).
9. Define mutation conventions: per mutation, the cache effect (invalidate/update/refetch), optimistic-update posture with an explicit rollback and error reconciliation, and idempotency for unsafe operations.
10. Wire real-time sources (if in scope) into the server-state cache (subscription → cache update), not into a parallel store.
11. Verify: build and run the data-layer smoke — a query renders, a mutation updates the cache, an expired token triggers single-flight refresh then retry, a refresh failure logs out and clears caches, logout propagates across tabs. Document any skipped check.
12. Validate against [security-standards](../../../../../standards/security-standards/README.md), [api-standards](../../../../../standards/api-standards/README.md), [observability-standards](../../../../../standards/observability-standards/README.md), and [naming-conventions](../../../../../standards/naming-conventions/README.md). Revise until all pass or document the gap.

## Outputs

Required:

- A tier map: every application data category assigned to URL/server/global/local with justification.
- Server-state configuration: query client, query-key factory, typed error mapping, retry/stale/cache policy.
- Transport/client layer: auth attachment, error mapping, idempotency headers, base URL from runtime config.
- Auth-token lifecycle implementation populating the scaffold provider seam: storage, single-flight refresh, refresh-failure logout, session flags for the routing gate.
- Logout/expiry handling: cache clear, store reset, cross-tab propagation.
- Query and mutation convention examples (list/detail/infinite; invalidate/optimistic with rollback).

Output rules:

- Functional code, not placeholder hooks.
- No server data mirrored into global stores.
- Token storage matches the security decision exactly; deviations are ADR candidates.
- No optimistic update without a rollback and error reconciliation.
- Transport concerns live in one layer, not per call site.

## Quality checks

- [ ] The state-tier model and data-fetching strategy are sourced from `frontend-architecture.md`; token strategy from `architecture/security` (or an ADR candidate is raised).
- [ ] Every application data category is mapped to exactly one tier with justification.
- [ ] Server state lives only in the query cache; it is not mirrored into Zustand/Redux.
- [ ] Token storage matches the `architecture/security` decision exactly (no convenience fallback).
- [ ] Token refresh is single-flight with a request queue; refresh failure triggers logout.
- [ ] Logout/auth-expiry clears the query cache, resets global stores, and propagates across tabs.
- [ ] Mutations declare their cache effect; every optimistic update has a rollback and error reconciliation.
- [ ] Retry policy does not retry on auth/validation 4xx; errors are mapped from the backend envelope.
- [ ] Unsafe mutations send idempotency-key headers per `api-standards`.
- [ ] Transport concerns (auth, refresh, CSRF, error mapping) are centralized in one client layer.
- [ ] No tokens appear in the bundle, logs, or error reports.

## References

- Upstream: [`architecture/frontend-architecture`](../../../../architecture/frontend-architecture/SKILL.md), [`architecture/security`](../../../../architecture/security/SKILL.md), [`architecture/backend-architecture`](../../../../architecture/backend-architecture/SKILL.md) (API contracts).
- Builds on: [`react-app-scaffold-and-runtime`](../react-app-scaffold-and-runtime/SKILL.md) (auth provider seam), [`react-routing-and-rendering-strategy`](../react-routing-and-rendering-strategy/SKILL.md) (URL state, protected gate consume session flags from here).
- Related react archetype skills: [`react-design-system-and-accessibility`](../react-design-system-and-accessibility/SKILL.md), [`react-performance-and-delivery-optimization`](../react-performance-and-delivery-optimization/SKILL.md).
- Compatible patterns: [`cqrs`](../../../../../architecture-patterns/cqrs/README.md) (read-model-driven UI), [`real-time-systems`](../../../../../architecture-patterns/real-time-systems/README.md) (subscription-fed cache), [`microservices`](../../../../../architecture-patterns/microservices/README.md).
