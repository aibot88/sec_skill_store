---
name: flutter-design-system-and-accessibility
description: Use when integrating a design system, theming, the component library, accessibility posture, the internationalization seam, or permission-request UX into a Flutter application after the app scaffold exists and mobile architecture is approved or intentionally deferred. Produces the token and theming layer extending the scaffold's ThemeData placeholder, a composed component library, the accessibility posture from mobile-architecture.md (screen reader, dynamic text, reduced motion, contrast, touch targets, RTL), an i18n seam, accessible auth UIs, and permission-request UX (rationale, denied, and blocked states). Do not use for app scaffolding, navigation topology or layout placement, state management or token logic, the native permission engine, or performance budget enforcement; use the other Flutter archetype skills instead.
---

# Flutter Design System and Accessibility

## When to use

Invoke when adding a design system and accessible component library to a scaffolded Flutter app, hardening accessibility (screen-reader semantics, dynamic text, contrast, touch targets, RTL), wiring the internationalization seam, or building permission-request and accessible auth UIs.

Do not use for: app scaffolding or the ThemeData placeholder itself (use `flutter-app-scaffold-and-runtime`); navigation topology, route-level layout placement, or auth-gate redirects (use `flutter-navigation-and-routing`); state management, token logic, or the native permission-request engine (use `flutter-state-and-data-fetching`); performance budget enforcement (use `flutter-performance-and-reliability`).

## Inputs

Required:

- A scaffolded Flutter app with the `app/app.dart` ThemeData placeholder and the `// TODO(flutter-design-system-and-accessibility)` seam.
- Approved `mobile-architecture.md`, or explicit confirmation that mobile architecture is intentionally deferred.

Optional:

- Design tokens or a brand spec (color, type scale, spacing, elevation, motion).
- Approved `architecture/security` decisions where auth UIs are built (no secret exposure, masked input, paste/autofill posture).
- Permission strategy and fallback from the Device Capability Integration section of `mobile-architecture.md`.
- Target locales and RTL requirement.

## Operating rules

- Never generate tutorial-grade UI. Assume a screen-reader user, a 200% font-scale user, a reduced-motion user, an RTL locale, and a user who denied a permission twice.
- Consume `mobile-architecture.md`; do not invent decisions. The accessibility posture, RTL decision, i18n constraints, and permission strategy belong to `mobile-architecture.md`; auth-UI security posture belongs to `architecture/security`. If either is silent on a decision this layer needs, pause and raise an ADR candidate rather than guessing.
- Extend the scaffold ThemeData seam — never replace the app root or hardcode a second theme source. Fill the scaffold's `// TODO(flutter-design-system-and-accessibility)` marker.
- Tokens are the single source of truth. Components consume semantic tokens (color, type, spacing, radius, motion) — no raw hex, magic numbers, or ad-hoc `TextStyle` in feature code.
- Accessibility is non-optional and is part of every component, not a later pass. Each interactive component declares its semantics, has a ≥48dp touch target, meets WCAG AA contrast, and is reachable and operable by a screen reader.
- Text scales; layout does not break. Components remain usable at the largest supported font scale — no clipped, overlapped, or truncated critical content.
- Honor reduced motion. Animations check the platform reduced-motion setting and degrade to an instant or minimal transition.
- RTL is a first-class direction. Use directional insets/alignment (`EdgeInsetsDirectional`, `start`/`end`) — never hardcoded left/right — when RTL is in scope.
- All user-facing strings go through the i18n seam. No literal display strings in widgets when localization is in scope; the seam exists even if only one locale ships initially.
- Permission UX requests the minimum, explains before asking, and handles denied and permanently-blocked states distinctly — with a settings-deep-link path for blocked. This skill owns the *UX*; the native permission engine is not requested or implemented here.
- Auth UIs never expose secrets: masked entry, no credential in logs or screenshots, autofill/paste posture per `architecture/security`.
- A component library not tested with a screen reader and at maximum font scale is not done.

## Output contract

The generated design-system and accessibility layer MUST conform to:

- [security-standards](../../../../../standards/security-standards/README.md) — permission minimization; auth UIs mask secrets and keep them out of logs and screenshots.
- [observability-standards](../../../../../standards/observability-standards/README.md) — permission-decision and accessibility-relevant analytics wired through the scaffold seam without capturing PII or secrets.
- [naming-conventions](../../../../../standards/naming-conventions/README.md) — token, component, and file naming.

Accessibility conformance target is WCAG AA adapted to mobile (screen-reader operability, ≥48dp targets, AA contrast, font-scale resilience, reduced motion, RTL). This is a non-optional part of the output, not a separate standard.

Upstream contract: `mobile-architecture.md` is the source of truth for accessibility posture, RTL, i18n constraints, and permission strategy; `architecture/security` is the source of truth for auth-UI security posture. If either is silent on a decision this layer needs, pause and raise an ADR candidate rather than guessing.

## Progressive references

- Read `references/flutter-design-system-playbook.md` when implementing any owned area or checking the anti-pattern list.
- Read `references/flutter-design-system-quality-rubric.md` before declaring the design-system layer complete.
- Use `assets/flutter-design-system.template.md` as the token, theming, and component-pattern reference.

## Process

1. Gather context: load `mobile-architecture.md` and extract the Accessibility & Localization section (screen reader, dynamic text, reduced motion, contrast, RTL, i18n) and the permission strategy/fallback from Device Capability Integration. Extract auth-UI security posture from `architecture/security` where auth UIs are in scope. Confirm the scaffold ThemeData seam exists. If a needed decision is missing, raise an ADR candidate before proceeding.
2. Token layer: define semantic tokens (color, type scale, spacing, radius, elevation, motion) as the single source of truth, with light/dark and any brand variants.
3. Theming: build `ThemeData` (and Cupertino theme where used) from tokens and install it into the scaffold `app/app.dart` ThemeData seam — not a second theme source.
4. Component library: compose accessible primitives and components consuming tokens only, each declaring semantics, a ≥48dp touch target, and AA contrast.
5. Accessibility posture: implement screen-reader semantics, font-scale resilience, reduced-motion handling, and AA contrast verification per the architecture posture.
6. RTL & i18n seam: install the localization delegate and the i18n seam; use directional layout primitives; verify mirrored layout when RTL is in scope.
7. Permission-request UX: build the pre-permission rationale, the granted path, and distinct denied and permanently-blocked states with a settings-deep-link for blocked — consuming the permission strategy, not requesting the native permission.
8. Accessible auth UIs: build login/MFA/recovery surfaces with masked input and the autofill/paste posture from `architecture/security`, screen-reader-labeled and font-scale-resilient.
9. Test and verify: screen-reader traversal of core flows, rendering at maximum font scale, reduced-motion behavior, and RTL mirroring where in scope. Run `flutter analyze` (zero issues). Document any skipped check.
10. Standards validation: check security-standards (permission minimization, auth-UI secret handling), observability-standards (analytics without PII), naming-conventions, and the WCAG AA mobile posture. Document any unresolved gap explicitly.

## Outputs

Required:

- Semantic token layer (color, type, spacing, radius, elevation, motion) with light/dark/brand variants.
- Theming built from tokens, installed into the scaffold ThemeData seam.
- Accessible component library consuming tokens only, with declared semantics and ≥48dp targets.
- Accessibility posture: screen-reader semantics, font-scale resilience, reduced motion, AA contrast.
- RTL support and an internationalization seam with the localization delegate.
- Permission-request UX with rationale, granted, denied, and permanently-blocked states.
- Accessible auth UIs with masked secrets per `architecture/security`.
- Tests for screen-reader traversal and maximum-font-scale rendering.

Output rules:

- Generated UI is functional and accessible, not placeholder-heavy.
- No raw hex, magic numbers, or ad-hoc `TextStyle` in feature widgets — tokens only.
- The theme is installed into the scaffold seam — there is no second theme source or parallel app root.
- The native permission engine is consumed, not implemented here; this layer owns the permission *UX* only.

## Quality checks

- [ ] `flutter analyze` reports zero issues.
- [ ] Theme is built from semantic tokens and installed into the scaffold `app/app.dart` seam — no second theme source.
- [ ] No raw hex, magic-number spacing, or ad-hoc `TextStyle` in feature widgets; components consume tokens only.
- [ ] Every interactive component declares screen-reader semantics and has a ≥48dp touch target.
- [ ] Text and key UI meet WCAG AA contrast in light and dark themes.
- [ ] Core screens remain usable at the largest supported font scale — no clipped or overlapped critical content.
- [ ] Animations honor the platform reduced-motion setting.
- [ ] RTL uses directional primitives and mirrors correctly where RTL is in scope.
- [ ] User-facing strings go through the i18n seam where localization is in scope.
- [ ] Permission UX explains before asking, requests the minimum, and handles denied vs permanently-blocked distinctly with a settings-deep-link for blocked.
- [ ] Auth UIs mask secrets, keep them out of logs/screenshots, and follow the `architecture/security` autofill/paste posture.
- [ ] Tests cover screen-reader traversal of core flows and maximum-font-scale rendering.

## References

- Upstream: [`architecture/mobile-architecture`](../../../../architecture/mobile-architecture/SKILL.md), [`architecture/security`](../../../../architecture/security/SKILL.md).
- Baseline this skill extends: `flutter-app-scaffold-and-runtime` (ThemeData seam).
- Related Flutter archetype skills: `flutter-navigation-and-routing` (owns layout placement), `flutter-state-and-data-fetching` (owns the native permission engine and auth state), `flutter-performance-and-reliability`.
- Standards: [`security-standards`](../../../../../standards/security-standards/README.md), [`observability-standards`](../../../../../standards/observability-standards/README.md), [`naming-conventions`](../../../../../standards/naming-conventions/README.md).
