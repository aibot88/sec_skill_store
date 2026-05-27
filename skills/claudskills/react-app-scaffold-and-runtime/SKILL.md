---
name: react-app-scaffold-and-runtime
description: Use when creating, modernizing, or production-hardening a standalone React SPA after frontend architecture is approved or intentionally deferred. Produces a production-ready app shell with Vite (or Webpack) project layout, environment and profile handling, top-level and route-level error boundaries, a structured logging client, RUM and error-reporting wiring, the auth provider/wrapper baseline downstream skills extend, CSP and security-header posture via host config, and container or static-CDN packaging. Do not use for routing topology, rendering strategy, state or data-fetching wiring, design-system integration, performance budgeting, or SSR/meta-framework scaffolding; use the other react archetype skills or the nextjs stack instead.
---

# React App Scaffold and Runtime

## When to use

Invoke when starting a new standalone React SPA, standardizing an internal React app baseline, modernizing a legacy Create-React-App or Webpack app, or preparing a React app for container or CDN deployment.

Do not use for: routing/rendering decisions (use `react-routing-and-rendering-strategy`), state or data-fetching wiring (use `react-state-management-and-data-fetching`), design-system or accessibility integration (use `react-design-system-and-accessibility`), perf budgeting (use `react-performance-and-delivery-optimization`), or any SSR/RSC/server-action scaffolding (that is meta-framework territory — use the `nextjs` stack).

## Inputs

Required:

- App name and the business capability it serves.
- Approved `frontend-architecture.md`, or explicit confirmation that frontend architecture is intentionally deferred.

Optional:

- Approved `architecture/security` decisions on auth provider, session model, and token strategy.
- Bundler preference (Vite default, Webpack on constraint).
- Deployment target (static CDN, container, edge static host).
- RUM and error-reporting vendor (Sentry, Datadog, none).
- Node version and package manager.
- CSP and security-header constraints from the hosting platform.
- Monorepo vs single-repo placement.

## Operating rules

- Never generate tutorial-grade scaffolding. Assume multiple environments, observability, CDN or container deployment, CSP enforcement, and operational ownership.
- Consume the architecture; do not invent it. Rendering mode, routing topology, state model, design-system seam, and perf budgets belong to other archetypes and to `frontend-architecture`. If `frontend-architecture.md` is missing a decision this scaffold needs (auth provider, runtime target), pause and raise an ADR candidate against `frontend-architecture` or `architecture/security`.
- This skill owns the **auth provider/wrapper baseline only** (e.g. `AuthProvider`/`SessionContext` shell, env-aware client ID, CSP headers). Token storage/refresh, protected-route gates, and accessible auth UIs belong to other react archetypes — scaffold the seam, do not implement the flow.
- Secure by default: no secrets in the bundle, env-injected config at deploy time (not build-time-baked secrets), a CSP that is not `unsafe-inline`/`unsafe-eval` without a documented exception, and security headers defined via host config.
- Observability is mandatory in the baseline: a structured logging client, RUM (`web-vitals`) wiring, and error-reporting with release/environment tagging and a top-level error boundary that reports.
- Error boundaries are layered: one top-level boundary that reports and renders a safe fallback, plus the seam for route-level boundaries the routing skill will populate.
- Config is environment-agnostic at build time. The same artifact runs in every environment; configuration arrives via runtime injection (`window.__ENV__`, `/config.json`, or platform env), never via per-environment builds.
- Confirm the target directory before writing files. Recommend `apps/<app-name>/` in a monorepo or repo root for a single-app repo. Refuse to write into a plugin/skill repository (any directory containing `skills/`, `standards/`, `architecture-patterns/`, or `marketplace.json`) without explicit user override.
- A scaffold that does not build and does not pass its smoke test is not done. Run the build and a baseline render/e2e smoke before declaring completion; fix and re-run on failure.

## Output contract

The generated app shell MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — no secrets in the bundle, CSP and security headers defined, token storage discipline deferred to the data-fetching skill but the provider seam not leaking credentials.
- [observability-standards](../../../../../standards/observability-standards/README.md) — RUM and error reporting wired with environment/release tags, browser-to-backend trace correlation seam present.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — env-agnostic build, runtime config injection, CDN/edge or container artifact.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — app name, env vars, asset and image naming.

Upstream contract: `frontend-architecture.md` is the source of truth for runtime target and the auth provider decision; `architecture/security` is the source of truth for the auth provider, session model, and token strategy. If either is silent on a decision this scaffold needs, pause and raise an ADR candidate rather than guessing.

## Process

1. Gather context: app name, business capability, **target directory**, bundler, deployment target, RUM/error vendor, Node version, package manager, and the auth provider decision from `skills/architecture/security`. Recommend Vite, current LTS Node, and static-CDN deployment unless constraints say otherwise. Verify the target directory is not a plugin/skill repository.
2. Generate the project layout: Vite (or Webpack) configuration, TypeScript config, directory structure (capability- or feature-oriented), entry point, and the app root with a single mount.
3. Generate environment and profile handling: typed env access, the runtime-config injection mechanism (no build-time secrets), and per-environment config documentation.
4. Generate the layered error-boundary baseline: a reporting top-level boundary with a safe fallback UI, plus the seam (provider/exported boundary component) for route-level boundaries the routing skill will use.
5. Generate the observability baseline: a structured logging client (level-aware, environment-aware), `web-vitals` RUM wiring, error-reporting init with release and environment tags, and the trace-correlation header seam for browser-to-backend.
6. Generate the auth provider/wrapper baseline only: the provider shell and context seam named per the `architecture/security` decision, env-aware client/app ID handling, and CSP/security headers via host config. Explicitly leave token storage/refresh and route gates as documented seams for the data-fetching and routing skills.
7. Generate packaging: a static-CDN build (with cache-control guidance) or a container image (env-agnostic, runtime config injected), plus ignore files and a `.env.example` with no real secrets.
8. Generate local-run and configuration documentation: how to run, the environment variables, the runtime-config contract, and the explicit list of seams downstream archetypes will fill.
9. Build verification (mandatory): run the production build and a baseline smoke test (render + minimal e2e). If e2e tooling is unavailable, document the skipped check in the README rather than declaring success silently. Fix and re-run on failure.
10. Validate against [security-standards](../../../../../standards/security-standards/README.md), [observability-standards](../../../../../standards/observability-standards/README.md), [deployment-standards](../../../../../standards/deployment-standards/README.md), and [naming-conventions](../../../../../standards/naming-conventions/README.md). Revise until all pass or explicitly document any unresolved gap.

## Outputs

Required:

- React app source tree with bundler and TypeScript configuration.
- Environment/profile handling with runtime config injection.
- Layered error-boundary baseline (top-level reporting boundary + route-boundary seam).
- Observability baseline: structured logging client, `web-vitals` RUM, error-reporting init.
- Auth provider/wrapper baseline (seam only) per the `architecture/security` decision.
- Packaging: static-CDN build or container image, ignore files, `.env.example`.
- Local-run documentation listing environment variables and the seams downstream skills fill.

Output rules:

- Generated files are functional, not placeholder-heavy.
- No secrets in the bundle, in `.env.example`, or in committed config.
- The auth baseline is a seam, not a flow — token logic and gates are explicitly deferred.
- The same build artifact must run in every environment via runtime config.

## Quality checks

- [ ] The production build succeeds and the baseline smoke test passes (or the gap is explicitly documented).
- [ ] No secrets appear in the bundle, `.env.example`, or committed config.
- [ ] A CSP and security headers are defined; `unsafe-inline`/`unsafe-eval` are absent or have a documented exception.
- [ ] A top-level error boundary reports to the error-reporting sink and renders a safe fallback.
- [ ] `web-vitals` RUM and error reporting are wired with environment and release tags.
- [ ] Configuration is injected at runtime; no per-environment build or build-time secret exists.
- [ ] The auth provider/wrapper baseline is a seam tied to a named `architecture/security` decision; token storage and route gates are explicitly deferred to the relevant react skills.
- [ ] The README lists the seams downstream archetypes (routing, state/data, design-system, performance) are expected to fill.

## References

- Upstream: [`architecture/frontend-architecture`](../../../../architecture/frontend-architecture/SKILL.md), [`architecture/security`](../../../../architecture/security/SKILL.md).
- Related react archetype skills (extend this baseline): [`react-routing-and-rendering-strategy`](../react-routing-and-rendering-strategy/SKILL.md), [`react-state-management-and-data-fetching`](../react-state-management-and-data-fetching/SKILL.md), [`react-design-system-and-accessibility`](../react-design-system-and-accessibility/SKILL.md), [`react-performance-and-delivery-optimization`](../react-performance-and-delivery-optimization/SKILL.md).
- Compatible patterns: [`microservices`](../../../../../architecture-patterns/microservices/README.md) (BFF-backed SPA), [`cqrs`](../../../../../architecture-patterns/cqrs/README.md), [`real-time-systems`](../../../../../architecture-patterns/real-time-systems/README.md).
