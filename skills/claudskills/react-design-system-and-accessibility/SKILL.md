---
name: react-design-system-and-accessibility
description: Use when integrating, reviewing, or hardening the design system and accessibility posture of a React app after the app scaffold exists and frontend architecture has defined the design-system seam and a11y target. Produces design-token wiring (CSS variables / Tailwind theme / vanilla-extract), primitive composition over an accessible headless library (Radix / React Aria / Headless UI), theming and dark-mode strategy, WCAG 2.2 AA conformance posture, keyboard-navigation and focus-management discipline, ARIA usage rules, screen-reader testing, and the internationalization seam. This is the React archetype meta-frameworks (e.g. nextjs) inherit rather than re-author. Do not use for app scaffolding, routing, state or data-fetching, or performance budgeting; use the other react archetype skills instead.
---

# React Design System and Accessibility

## When to use

Invoke when integrating a design system into a React app, building the accessible component layer over headless primitives, establishing theming/dark-mode, or auditing/hardening WCAG conformance, keyboard, focus, ARIA, and i18n.

Do not use for: scaffolding or the runtime baseline (use `react-app-scaffold-and-runtime`), routing/route UIs structurally (use `react-routing-and-rendering-strategy`), state/data wiring (use `react-state-management-and-data-fetching`), or perf/bundle work (use `react-performance-and-delivery-optimization`).

## Meta-framework note

This is the one React archetype meta-frameworks **inherit** rather than re-author. When consumed by the `nextjs` stack, the consumer must additionally observe React Server Component constraints: interactive primitives are client components (`'use client'`), the token layer must work without client JS where the architecture server-renders, and the headless library must be RSC-compatible. Those constraints are documented for the consumer here but not implemented in this base skill.

## Inputs

Required:

- An existing react app scaffold (`react-app-scaffold-and-runtime`).
- Approved `frontend-architecture.md` defining the design-system seam (what the design system owns: tokens, primitives, patterns; vs what the app owns) and the accessibility target (WCAG level, keyboard/SR expectations per surface).

Optional:

- An existing design system, brand system, or token source (Figma tokens, Style Dictionary).
- Headless primitive library preference (Radix / React Aria / Headless UI).
- Styling approach constraint (Tailwind, vanilla-extract, CSS modules).
- i18n requirements: locales, RTL, message-format library.
- `architecture/security` accessible-auth-UI requirements (login, MFA, recovery) — this skill owns their a11y.

## Operating rules

- Consume the seam; do not invent it. What the design system owns vs the app owns, and the WCAG target, come from `frontend-architecture.md`. If the seam or a11y target is unstated, pause and raise an ADR candidate against `frontend-architecture`.
- Accessibility is non-optional and is the WCAG level the architecture specifies, defaulting to **WCAG 2.2 AA**. Every component-producing decision states its keyboard behavior, focus management, and screen-reader expectation. "We'll add a11y later" is a rejected posture.
- Build interactive components on an accessible headless library (Radix / React Aria / Headless UI). Do not hand-roll dialogs, menus, comboboxes, tabs, or tooltips — accessible interaction state is delegated to the primitive, styling is the app's.
- Tokens are the single source of design truth. Color, type, spacing, radius, motion are token-driven (CSS variables / Tailwind theme / vanilla-extract); components reference tokens, never hard-coded values.
- Theming and dark-mode are token-layer concerns, not per-component overrides. Contrast is verified at the token level for every theme against the WCAG target.
- Focus management is explicit: visible focus indicators (never `outline: none` without a replacement), focus trap in modals/overlays, focus restore on close, skip links, and logical tab order. Route-change focus handoff is coordinated with the routing skill's seam.
- ARIA is a last resort, not a default. Prefer native semantic elements; use ARIA only where no native element suffices, and never contradict native semantics. No `role` that the headless primitive already provides.
- Motion respects `prefers-reduced-motion`; color is never the sole information channel; targets meet WCAG 2.2 target-size where applicable.
- The i18n seam is established even if one locale ships: externalized strings, a message-format library, locale-aware formatting, and RTL-readiness in the token/layout layer. Hard-coded user-facing strings are a defect.
- This skill owns the accessibility of auth UIs named by `architecture/security` (login, MFA, recovery): labelled fields, error association, focus on error, no keyboard traps.
- Verify a11y, do not assert it: automated checks (axe) plus a documented keyboard-only and screen-reader pass on the core flows. An unverified a11y claim is not a pass.

## Output contract

The design-system and accessibility implementation MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — auth UIs are accessible and do not leak credentials via autofill/logging; no a11y workaround weakens the auth flow.
- [observability-standards](../../../../../standards/observability-standards/README.md) — a11y violations surfaced by automated tooling are reported in CI, not silently dropped.
- [deployment-standards](../../../../../standards/deployment-standards/README.md) — the token/theme layer ships env-agnostic; no per-environment theming build.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — token, component, and locale-key naming.

Upstream contract: `frontend-architecture.md` is the source of truth for the design-system seam and the WCAG target; `architecture/security` is the source of truth for which auth UIs exist and their requirements. If a needed decision is unstated, pause and raise an ADR candidate. RSC/`'use client'` constraints apply only when a meta-framework consumes this skill and are the consumer's responsibility.

## Process

1. Load the design-system seam and a11y target from `frontend-architecture.md`; load auth-UI requirements from `architecture/security`. Confirm the scaffold exists. If inputs are missing, pause and escalate.
2. Establish the token layer: import or define tokens (color, type, spacing, radius, motion) in the chosen mechanism (CSS variables / Tailwind theme / vanilla-extract). Verify per-theme color contrast against the WCAG target at the token level.
3. Establish theming and dark-mode at the token layer: theme switching strategy, system-preference detection, persisted preference (coordinated with the state skill's global tier), and contrast verification per theme.
4. Select and wire the headless primitive library. Compose styled components over its primitives (dialog, menu, combobox, tabs, tooltip, popover, etc.); do not reimplement interaction/a11y state.
5. Define the component composition rules: what the design system owns (tokens, primitives, patterns) vs what the app composes, matching the architecture seam. Document the contract for adding/extending components.
6. Implement focus management: global visible-focus styling, modal/overlay focus trap and restore, skip links, logical tab order, and the route-change focus handoff coordinated with the routing skill.
7. Apply ARIA discipline: prefer native semantics; add ARIA only where required and non-duplicative of the primitive; document each non-trivial ARIA usage with its justification.
8. Implement motion/color/target rules: `prefers-reduced-motion` handling, no color-only information, target-size compliance.
9. Establish the i18n seam: externalized strings, message-format library, locale-aware number/date/currency formatting, and RTL-readiness in tokens/layout — even if a single locale ships.
10. Implement and harden the accessible auth UIs from `architecture/security`: labelled inputs, programmatic error association, focus-to-error, no keyboard traps in MFA/recovery flows.
11. Verify a11y: run automated checks (axe/eslint-jsx-a11y) in CI, then perform and document a keyboard-only pass and a screen-reader pass on the core flows including auth. Capture findings; fix or log as explicit gaps.
12. Validate against [security-standards](../../../../../standards/security-standards/README.md), [observability-standards](../../../../../standards/observability-standards/README.md), [deployment-standards](../../../../../standards/deployment-standards/README.md), and [naming-conventions](../../../../../standards/naming-conventions/README.md). Revise until all pass or document the gap.

## Outputs

Required:

- Token layer (color/type/spacing/radius/motion) with per-theme contrast verification against the WCAG target.
- Theming/dark-mode strategy at the token layer with persisted preference.
- Accessible component layer composed over the chosen headless primitive library, with the design-system-vs-app ownership contract documented.
- Focus-management implementation (visible focus, trap/restore, skip links, tab order, route-change handoff).
- ARIA usage rules with justifications for non-trivial usage.
- i18n seam (externalized strings, formatter, RTL-readiness) even for a single locale.
- Accessible auth UIs for the flows named by `architecture/security`.
- A11y verification report: automated results + documented keyboard and screen-reader passes.

Output rules:

- Functional components, not placeholders; no hand-rolled interactive primitives.
- No hard-coded design values (tokens only) and no hard-coded user-facing strings.
- WCAG target met and verified, not asserted.
- RSC/meta-framework constraints are documented for consumers, not implemented here.

## Quality checks

- [ ] The design-system seam and WCAG target are sourced from `frontend-architecture.md` (or an ADR candidate is raised).
- [ ] Interactive components are built on an accessible headless library; none are hand-rolled.
- [ ] All design values are token-driven; per-theme contrast is verified against the WCAG target at the token layer.
- [ ] Theming/dark-mode is token-layer, with persisted preference and verified contrast per theme.
- [ ] Focus is always visible; modals trap and restore focus; skip links and logical tab order exist; route-change focus handoff is coordinated with the routing skill.
- [ ] ARIA is used only where native semantics are insufficient and never duplicates the primitive; non-trivial usage is justified.
- [ ] `prefers-reduced-motion` is honored; color is not the sole information channel.
- [ ] An i18n seam exists (externalized strings, formatter, RTL-readiness) even with one locale.
- [ ] Auth UIs from `architecture/security` are accessible (labels, error association, focus-to-error, no traps).
- [ ] A11y is verified: automated checks in CI plus documented keyboard-only and screen-reader passes on core + auth flows.
- [ ] Meta-framework RSC/`'use client'` constraints are documented for consumers.

## References

- Upstream: [`architecture/frontend-architecture`](../../../../architecture/frontend-architecture/SKILL.md), [`architecture/security`](../../../../architecture/security/SKILL.md) (accessible auth UIs).
- Builds on: [`react-app-scaffold-and-runtime`](../react-app-scaffold-and-runtime/SKILL.md).
- Coordinates with: [`react-routing-and-rendering-strategy`](../react-routing-and-rendering-strategy/SKILL.md) (route-change focus handoff), [`react-state-management-and-data-fetching`](../react-state-management-and-data-fetching/SKILL.md) (theme-preference global state).
- Inherited by meta-frameworks: the `nextjs` stack inherits this archetype; see the frontend layer README meta-framework strategy.
- Compatible patterns: [`microservices`](../../../../../architecture-patterns/microservices/README.md), [`cqrs`](../../../../../architecture-patterns/cqrs/README.md), [`real-time-systems`](../../../../../architecture-patterns/real-time-systems/README.md).
