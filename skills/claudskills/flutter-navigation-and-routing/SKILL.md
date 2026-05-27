---
name: flutter-navigation-and-routing
description: Use when wiring the navigation graph, deep links, back-stack behavior, auth-gate routing, or OS-interruption state restoration into a Flutter application after the app scaffold exists and mobile architecture is approved or intentionally deferred. Produces the router named in mobile-architecture.md (extending the scaffold's router placeholder), the route hierarchy and tab/shell structure, validated deep-link / app-link handling, session-driven auth-gate redirects, modal strategy, back-stack and predictive-back behavior, state restoration across process death, and notification-payload-to-route resolution consuming the state layer's push seam. Do not use for app scaffolding, state management or token logic, push payload ingestion, design-system or accessibility integration, or performance budget enforcement; use the other Flutter archetype skills instead.
---

# Flutter Navigation and Routing

## When to use

Invoke when adding navigation to a scaffolded Flutter app, hardening an existing navigation graph (deep-link validation, auth-gate correctness, restoration after process death), or resolving notification payloads to routes.

Do not use for: app scaffolding or the router placeholder itself (use `flutter-app-scaffold-and-runtime`); state management, token storage/refresh, or push payload ingestion (use `flutter-state-and-data-fetching`); design-system or accessibility integration (use `flutter-design-system-and-accessibility`); performance budget enforcement (use `flutter-performance-and-reliability`).

## Inputs

Required:

- A scaffolded Flutter app with the `app/app.dart` router placeholder and the `// TODO(flutter-navigation-and-routing)` seams.
- Approved `mobile-architecture.md`, or explicit confirmation that mobile architecture is intentionally deferred.

Optional:

- A wired state layer exposing a session shell and a push-payload seam (`flutter-state-and-data-fetching`); navigation consumes session state but does not manage tokens.
- Approved `architecture/security` decisions on auth transitions (where unauthenticated users go, post-login redirect rules).
- Router preference if `mobile-architecture.md` is silent (`go_router` default; `auto_route` if codegen-typed routes are required).
- Deep-link / universal-link / app-link domains and the platform association files.

## Operating rules

- Never generate tutorial-grade navigation. Assume deep links from untrusted sources, auth state changing mid-navigation, and the OS killing the app on any screen.
- Consume `mobile-architecture.md`; do not invent decisions. Navigation hierarchy, route ownership, deep-link handling, modal strategy, tab/shell architecture, and back/restoration behavior belong to `mobile-architecture.md`; auth-transition policy belongs to `architecture/security`. If either is silent on a decision this layer needs, pause and raise an ADR candidate rather than guessing.
- Extend the scaffold router placeholder — never replace the app root or create a parallel router. Fill the scaffold's `// TODO(flutter-navigation-and-routing)` markers.
- Auth gating reads session state; it does not touch tokens. The redirect decision derives from the `flutter-state-and-data-fetching` session shell. Token storage and refresh are out of scope here.
- Every deep link is untrusted input. Validate and sanitize path and query parameters before routing; reject or fall back on malformed links; never use a deep-link parameter as an open redirect target or to bypass an auth gate.
- A protected route never paints protected content before the gate resolves. The redirect happens before the protected screen builds — no flash of authenticated UI for an unauthenticated user.
- State restoration is mandatory. Routes, scroll positions, and in-progress flow state survive process death via `RestorationMixin` / restoration IDs, restoring to the screen the user left.
- Back-stack behavior is explicit. System back, predictive back (Android), and the iOS interactive pop follow the back-navigation rules in `mobile-architecture.md` — including unsaved-changes interception where declared.
- Notification-to-route resolution consumes the state layer's push seam. This skill maps a payload to a route; it does not ingest, persist, or own the payload.
- Navigation and screen-view events are traced per observability-standards through the scaffold seam.
- A navigation graph not tested against an unauthenticated deep link into a protected route, and against restoration after process death, is not done.

## Output contract

The generated navigation layer MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — deep-link input validation, no open redirect, no auth-gate bypass via link parameters, no protected content painted before the gate resolves.
- [observability-standards](../../../../../standards/observability-standards/README.md) — navigation and screen-view tracing wired through the scaffold tracing seam.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — route names, path segments, and file naming.

Upstream contract: `mobile-architecture.md` is the source of truth for navigation hierarchy, route ownership, deep-link handling, modal strategy, tab/shell architecture, and back/restoration behavior; `architecture/security` is the source of truth for auth-transition policy. If either is silent on a decision this layer needs, pause and raise an ADR candidate rather than guessing.

## Progressive references

- Read `references/flutter-navigation-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/flutter-navigation-quality-rubric.md` before declaring the navigation layer complete.
- Use `assets/flutter-navigation.template.md` as the router-layout and code-pattern reference.

## Process

1. Gather context: load `mobile-architecture.md` and extract the Navigation Architecture section (hierarchy, route ownership, deep-link handling, modal strategy, auth transitions, tab/shell architecture, back-navigation & restoration) and the routing/deep-link behavior in Notifications & Background Behavior. Extract auth-transition policy from `architecture/security`. Confirm the scaffold router placeholder and the state-layer session shell exist. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Router installation: install the router named in `mobile-architecture.md`, extending the scaffold `app/app.dart` placeholder — not a new app root. Wire it to the scaffold session shell as a refresh listenable.
3. Route hierarchy: build the route tree, nested/shell routes, and tab/shell architecture per the Navigation Architecture decisions, with route ownership matching the document.
4. Auth-gate routing: implement the redirect derived from session state — unauthenticated users to the declared destination, authenticated users away from auth screens, post-login redirect to the originally requested route. No token logic.
5. Deep-link / app-link handling: register the universal-link / app-link domains and association files; parse, validate, and sanitize every path and query parameter; route valid links, fall back safely on invalid ones, and never bypass the auth gate.
6. Modal & back-stack: implement the modal strategy and system/predictive/interactive back behavior per the document, including unsaved-changes interception where declared.
7. State restoration: assign restoration IDs and `RestorationMixin` so route stack and in-progress flow state survive process death and restore to the screen the user left.
8. Notification-to-route resolution: consume the state layer's push-payload seam and map payloads to routes; do not ingest or persist the payload.
9. Test and verify: integration-test an unauthenticated deep link into a protected route (must redirect, not flash), post-login redirect to the requested route, and restoration after simulated process death. Run `flutter analyze` (zero issues). Document any skipped check.
10. Standards validation: check security-standards (deep-link validation, no bypass, no protected-content flash), observability-standards (navigation tracing), naming-conventions. Document any unresolved gap explicitly.

## Outputs

Required:

- Router installation extending the scaffold placeholder, wired to the session shell.
- Route hierarchy, nested/shell routes, and tab/shell structure per architecture.
- Session-driven auth-gate redirects with post-login return-to-requested-route.
- Validated deep-link / app-link handling with safe fallback and no auth-gate bypass.
- Modal strategy and explicit system/predictive/interactive back behavior.
- State restoration across process death (route stack + in-progress flow state).
- Notification-payload-to-route resolution consuming the state-layer push seam.
- Integration tests for unauthenticated-deep-link redirect, post-login redirect, and restoration.

Output rules:

- Generated code is functional and tested, not placeholder-heavy.
- The router extends the scaffold app root — there is no parallel router or second app widget.
- No token or session-storage logic in this layer — it reads session state only.
- No deep-link parameter is trusted without validation; none can bypass the auth gate.

## Quality checks

- [ ] `flutter analyze` reports zero issues.
- [ ] Router matches `mobile-architecture.md`; route hierarchy and tab/shell structure match the document's route ownership.
- [ ] The router extends the scaffold `app/app.dart` placeholder — no parallel router or second app root.
- [ ] Auth-gate redirects derive from the state-layer session shell; no token logic exists here.
- [ ] An unauthenticated request to a protected route redirects before any protected content paints (no authenticated-UI flash).
- [ ] Post-login redirect returns the user to the originally requested route.
- [ ] Every deep-link path/query parameter is validated and sanitized; malformed links fall back safely; no parameter bypasses the auth gate or acts as an open redirect.
- [ ] Modal strategy and system/predictive/interactive back behavior match `mobile-architecture.md`, including unsaved-changes interception where declared.
- [ ] Route stack and in-progress flow state survive process death and restore to the screen the user left.
- [ ] Notification-payload-to-route resolution consumes the state-layer push seam without ingesting or persisting the payload.
- [ ] Navigation and screen-view events are traced through the scaffold seam.
- [ ] Integration tests cover unauthenticated-deep-link redirect, post-login redirect, and restoration after process death.

## References

- Upstream: [`architecture/mobile-architecture`](../../../../architecture/mobile-architecture/SKILL.md), [`architecture/security`](../../../../architecture/security/SKILL.md).
- Baseline this skill extends: `flutter-app-scaffold-and-runtime` (router placeholder, observability seams).
- Consumes: `flutter-state-and-data-fetching` (session shell, push-payload seam).
- Related Flutter archetype skills: `flutter-design-system-and-accessibility`, `flutter-performance-and-reliability`.
- Standards: [`security-standards`](../../../../../standards/security-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md).
