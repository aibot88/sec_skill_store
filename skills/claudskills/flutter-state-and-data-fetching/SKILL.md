---
name: flutter-state-and-data-fetching
description: Use when wiring state management, the network layer, caching, offline behavior, auth-token plumbing, push-notification delivery, or background sync into a Flutter application after the app scaffold exists and mobile architecture is approved or intentionally deferred. Produces the state-management wiring named in mobile-architecture.md (extending the scaffold's DI/session shell), a typed network layer honoring the API contract, secure token storage with single-flight refresh, a durable offline mutation queue, optimistic-update posture with rollback, push-notification delivery wiring, and background-sync tasks feeding the data layer. Do not use for app scaffolding, navigation topology or route-level auth gates, deep-link route resolution, design-system or accessibility integration, or performance budget enforcement; use the other Flutter archetype skills instead.
---

# Flutter State and Data Fetching

## When to use

Invoke when adding state management and a data layer to a scaffolded Flutter app, hardening an existing data layer (token refresh, offline resilience, cache invalidation), or wiring push-notification delivery and background sync into the state graph.

Do not use for: app scaffolding, flavors, or the DI/session shell itself (use `flutter-app-scaffold-and-runtime`); navigation topology, protected-route gates, or resolving a notification payload to a route (use `flutter-navigation-and-routing`); design-system or accessibility integration (use `flutter-design-system-and-accessibility`); performance budget enforcement (use `flutter-performance-and-reliability`).

## Inputs

Required:

- A scaffolded Flutter app with the DI/session provider shell in place (the `// TODO(flutter-state-and-data-fetching)` seams this skill fills).
- Approved `mobile-architecture.md`, or explicit confirmation that mobile architecture is intentionally deferred.

Optional:

- Approved `architecture/security` decisions on token strategy, session model, and secure-storage posture.
- API contract from `backend-architecture` (REST/GraphQL/event shapes the network layer honors).
- State mechanism preference if `mobile-architecture.md` is silent (Riverpod default; Bloc if event-sourced flows dominate).
- Offline scope: which journeys must work offline and which degrade.
- Push provider (FCM, APNs direct, or none) and background-execution constraints.

## Operating rules

- Never generate tutorial-grade data code. Assume token refresh under concurrency, process death mid-mutation, degraded networks, and stale-cache reconciliation.
- Consume `mobile-architecture.md`; do not invent decisions. State mechanism, state ownership, offline/sync model, and notification behavior belong to `mobile-architecture.md`; token strategy and session model belong to `architecture/security`. If either is silent on a decision this layer needs, pause and raise an ADR candidate rather than guessing.
- Extend the scaffold seam — never re-register or re-implement the DI/session shell. Fill the scaffold's `// TODO(flutter-state-and-data-fetching)` markers; do not create a parallel container.
- Tokens never touch plaintext. Secure storage only (`flutter_secure_storage` → Keychain/Keystore). Never `SharedPreferences`, never logged, never in crash or analytics payloads.
- Token refresh is single-flight. Concurrent 401s trigger exactly one refresh; in-flight requests queue and replay after it resolves. A failed refresh propagates logout through the scaffold session shell.
- The offline queue is durable. It survives process death (persisted, not in-memory), replays idempotently, and bounds retry with backoff and an explicit poison-message ceiling.
- Every optimistic update has a rollback path. Conflict resolution follows the rules in `mobile-architecture.md` — it is not invented here.
- The network layer honors the API contract. Typed models with explicit (de)serialization; no ad-hoc response maps; transport errors mapped to a domain failure type.
- Push wiring delivers payload and updates state; it does not navigate. Route resolution from a notification payload is deferred to `flutter-navigation-and-routing`.
- Every network call is traced and logged per observability-standards with token and PII redaction.
- A data layer not tested against single-flight refresh, offline replay idempotency, and optimistic rollback is not done.

## Output contract

The generated state and data layer MUST conform to:

- [api-standards](../../../../../standards/api-standards/README.md) — honors the REST/GraphQL/event contracts produced by `backend-architecture`; typed models, no ad-hoc shapes.
- [security-standards](../../../../../standards/security-standards/README.md) — tokens in secure storage only, never logged or persisted in plaintext, no secrets in the bundle.
- [observability-standards](../../../../../standards/observability-standards/README.md) — network tracing and structured request/response logging with token and PII redaction, wired through the scaffold's tracing seam.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — repository, provider/notifier, model, and file naming.

Upstream contract: `mobile-architecture.md` is the source of truth for state mechanism, state ownership, offline/sync model, and notification behavior; `architecture/security` is the source of truth for token strategy, session model, and secure-storage posture. If either is silent on a decision this layer needs, pause and raise an ADR candidate rather than guessing.

## Progressive references

- Read `references/flutter-state-data-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/flutter-state-data-quality-rubric.md` before declaring the data layer complete.
- Use `assets/flutter-state-data.template.md` as the layer-layout and code-pattern reference.

## Process

1. Gather context: load `mobile-architecture.md` and extract the State Management Strategy table (local UI / session / cached-remote / persistent ownership, mechanism, sync, persistence, invalidation), the Offline & Synchronization Design, the Notifications & Background Behavior section, and Application Architecture (state ownership, side-effect handling, concurrency model). Extract token strategy, session model, and secure-storage posture from `architecture/security`. Confirm the scaffold's DI/session seam exists. If a needed decision is missing, raise an ADR candidate before proceeding.
2. State management wiring: install the mechanism named in `mobile-architecture.md`, extending the scaffold's `ProviderScope`/GetIt root — not a new container. Map each row of the State Management Strategy table to a concrete provider/notifier/bloc with the declared ownership and invalidation lifecycle.
3. Network layer: build a typed client (`dio` or `http` per architecture) with the flavor base URL from `app_config.dart`, request/response interceptors, and transport-error-to-domain-failure mapping. Models honor the API contract with explicit (de)serialization.
4. Auth-token plumbing: implement a secure-storage token adapter, an auth interceptor attaching the access token, single-flight refresh on 401 with a request replay queue, and logout propagation that flips the scaffold session shell. Fill the scaffold's `// TODO(flutter-state-and-data-fetching)` markers.
5. Caching & revalidation: implement the cache store per the chosen mechanism with stale-while-revalidate and the invalidation rules from the State Management Strategy table.
6. Offline queue: implement a persisted mutation queue, a connectivity listener, idempotent replay on reconnect, and backoff with a poison-message ceiling per the Offline & Synchronization Design.
7. Optimistic updates: implement apply/rollback wrappers and conflict resolution exactly as specified in `mobile-architecture.md`.
8. Push delivery wiring: register the push token, implement foreground/background/terminated handlers that update state, and hand the payload to the navigation seam (`// TODO(flutter-navigation-and-routing)`) — no `Navigator` calls here.
9. Background sync: wire the background task (`workmanager` or platform background fetch) feeding repositories, within the background-execution budget from the Performance & Battery and Notifications & Background sections.
10. Test and verify: unit-test single-flight refresh under concurrent 401s, offline-replay idempotency, and optimistic rollback. Run `flutter analyze` (zero issues). Document any skipped check rather than declaring success silently.
11. Standards validation: check api-standards (contract fidelity), security-standards (token storage and redaction), observability-standards (network tracing), naming-conventions. Document any unresolved gap explicitly.

## Outputs

Required:

- State-management wiring extending the scaffold DI/session shell, mapped to the State Management Strategy table.
- Typed network layer with interceptors and domain-failure mapping, honoring the API contract.
- Secure token storage, auth interceptor, single-flight refresh, and logout propagation (scaffold seams filled).
- Cache store with stale-while-revalidate and architecture-defined invalidation.
- Durable offline mutation queue with idempotent replay and bounded retry.
- Optimistic-update wrappers with rollback and architecture-defined conflict resolution.
- Push-notification delivery wiring (payload → state; route resolution deferred to navigation).
- Background-sync task feeding the data layer within budget.
- Unit tests for refresh concurrency, offline replay idempotency, and optimistic rollback.

Output rules:

- Generated code is functional and tested, not placeholder-heavy.
- No tokens or secrets in `SharedPreferences`, logs, crash payloads, committed config, or the build artifact.
- The DI/session shell is extended, never duplicated — the scaffold remains the single container.
- Push wiring updates state only; it does not navigate.

## Quality checks

- [ ] `flutter analyze` reports zero issues.
- [ ] State mechanism matches `mobile-architecture.md`; each State Management Strategy row maps to a concrete provider/notifier with the declared invalidation lifecycle.
- [ ] Tokens are stored only via `flutter_secure_storage`; no token appears in `SharedPreferences`, logs, crash, or analytics payloads.
- [ ] Concurrent 401s trigger exactly one refresh; queued requests replay after it; a failed refresh propagates logout through the scaffold session shell.
- [ ] The offline mutation queue is persisted (survives process death), replays idempotently, and has a bounded-retry poison ceiling.
- [ ] Every optimistic update has a rollback path; conflict resolution matches `mobile-architecture.md`.
- [ ] Network models honor the API contract; transport errors map to a domain failure type.
- [ ] Push handlers update state and defer route resolution to `flutter-navigation-and-routing` (no `Navigator` calls).
- [ ] Network calls are traced and logged through the scaffold seam with token and PII redaction.
- [ ] Unit tests cover single-flight refresh, offline replay idempotency, and optimistic rollback.

## References

- Upstream: [`architecture/mobile-architecture`](../../../../architecture/mobile-architecture/SKILL.md), [`architecture/security`](../../../../architecture/security/SKILL.md).
- Baseline this skill extends: `flutter-app-scaffold-and-runtime` (DI/session shell, observability seams).
- Related Flutter archetype skills: `flutter-navigation-and-routing` (consumes session state and push payloads), `flutter-design-system-and-accessibility`, `flutter-performance-and-reliability`.
- Standards: [`api-standards`](../../../../../standards/api-standards/README.md), [`security-standards`](../../../../../standards/security-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md).
