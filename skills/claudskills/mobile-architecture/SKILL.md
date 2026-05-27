---
name: mobile-architecture
description: Use when a product requires native or cross-platform-native mobile application architecture after an approved system design and before mobile implementation begins. Produces platform strategy, application and navigation architecture, state and offline/sync design, device-capability integration, performance and battery budgets, accessibility and localization, notifications and background behavior, error handling, observability, testing strategy, failure taxonomy, and implementation handoffs. Do not use for mobile-web or PWA (use frontend-architecture), backend service design (use backend-architecture), UI or visual design (use frontend-design), vendor-specific SDK implementation, deep mobile security (use security), or store-release and signing depth (use operations or infrastructure-platform).
---

# Mobile Architecture

## When to use

Invoke after `architecture/system-design` has approved a product that includes a native or cross-platform-native mobile application, and before `implementations/mobile/<ecosystem>` skills generate platform code. Covers iOS, Android, cross-platform-native (React Native / Flutter / KMP), hybrid, tablet/foldable, and companion apps.

Do not use when the product has no mobile client, for pure backend architecture (use [`backend-architecture`](../backend-architecture/SKILL.md)), for mobile-web or PWA (use [`frontend-architecture`](../frontend-architecture/SKILL.md)), for UI or visual design (use [`frontend-design`](../../implementations/frontend/frontend-design/SKILL.md)), for vendor-specific SDK implementation, or when the architecture is finalized and only implementation remains.

## Inputs

Required:

- Approved `system-design.md` and the relevant ADRs.
- Mobile product requirements and the primary user journeys.
- Supported platforms and minimum OS versions.
- Performance and offline expectations.

Optional:

- Backend / API contracts; identity and session model.
- Design system or UX guidelines; accessibility requirements.
- Analytics, notification, and device-capability requirements.
- Security / compliance constraints; release cadence; regional constraints.
- The product's `frontend-architecture.md` (optional, non-binding cross-reference for shared concerns).

## Operating rules

- Treat the mobile app as a constrained distributed system: assume unreliable networks, intermittent connectivity, limited battery, and abrupt termination; design for recovery and resumability.
- Architect before choosing native vs cross-platform-native vs hybrid; the platform-target decision is an ADR, not a prescription, and is never defaulted to cross-platform without evaluating UX, startup, memory, animation, offline, and native-API trade-offs.
- Define device/backend state ownership explicitly; navigation, state, sync, and caching are first-class architectural concerns.
- Minimize background work unless product-critical; define degraded behavior explicitly for every critical journey.
- Native platform conventions take precedence over framework convenience; accessibility and responsiveness are mandatory architectural qualities.
- Mobile security/privacy and release/operations are callouts here, not owned: summarize the mobile-specific concern and raise an ADR candidate against `system-design`; ownership stays with `security` and `operations`/`infrastructure-platform`.
- No device feature without measurable user value; no premature optimization for unsupported platforms; no vendor SDK detail unless it materially changes architecture behavior.
- Mobile-web/PWA is out of scope and belongs to `frontend-architecture`.

## Output contract

`mobile-architecture.md` MUST conform to [standards/architecture-schema](../../../standards/architecture-schema/README.md), which is authoritative for its frontmatter, the 18-section required/conditional structure, conditional-omission rules, the §9/§15 callout framing, and `system-design.md` traceability. Skill structure conforms to [documentation-standards](../../../standards/documentation-standards/README.md). Use `assets/mobile-architecture.template.md` as the scaffold. The artifact is independently valid without a `frontend-architecture.md`; cross-references to it are optional and non-binding.

## Progressive references

- Read `references/mobile-architecture-playbook.md` when defining any owned area or checking the anti-pattern list.
- Read `references/mobile-architecture-quality-rubric.md` before finalizing and use it as the validation checklist.
- Use `assets/mobile-architecture.template.md` for `mobile-architecture.md`.

## Process

ADR candidates are drafted inline as decisions are made (notably the platform-target decision and the §9/§15 callouts). The final step consolidates them; it does not retrofit ADRs from prose.

- [ ] Step 1: Load `system-design.md` and relevant ADRs. Identify mobile surfaces, user journeys, supported platforms, device capabilities, network/session assumptions, and operational constraints; mark latency-sensitive and offline-sensitive flows.
- [ ] Step 2: Decide platform strategy (native vs cross-platform-native vs hybrid). Document rationale, trade-offs, unsupported scenarios, minimum OS, device classes, tablet/foldable behavior. Draft an ADR candidate for the platform-target decision.
- [ ] Step 3: Define application architecture: layers, module boundaries, dependency ownership, feature isolation, shared services, state ownership, side-effect handling, concurrency model, lifecycle, dependency injection. Avoid over-abstraction beyond current platform scope.
- [ ] Step 4: Define navigation architecture: hierarchy, route ownership, deep-link handling, modal strategy, auth transitions, tab/shell architecture, back-navigation and state restoration after interruption.
- [ ] Step 5: Define state management: local UI, session, cached remote, persistent storage, synchronization ownership, optimistic updates, conflict resolution, rollback, stale-data handling, cache expiration.
- [ ] Step 6: Define offline & synchronization architecture: offline capabilities, sync model, queueing, retry, conflict resolution, authoritative sources, reconciliation; state explicitly what works offline, what partially works, and what fails gracefully.
- [ ] Step 7: Define device-capability integration: per capability state permission strategy, fallback behavior, privacy expectations, battery impact, failure handling, and platform-specific limits.
- [ ] Step 8: Define performance & battery budgets: cold/warm start, transition latency, interaction responsiveness, memory, background execution, battery, network, storage growth; degradation under low memory, poor connectivity, thermal throttling, and battery-saver.
- [ ] Step 9: Security & privacy callouts: summarize mobile-specific auth/token/secure-storage/jailbreak/encryption concerns and draft ADR candidates. Defer ownership to [`security`](../security/SKILL.md); do not produce an owned security design here.
- [ ] Step 10: Define accessibility & localization: screen-reader support, dynamic text, reduced motion, color contrast, RTL, font scaling, internationalization. Accessibility failures are architectural failures.
- [ ] Step 11: Define notifications & background behavior: push types, delivery expectations, priority classes, background refresh, routing, opt-in, rate-limiting, silent notifications. No background execution without measurable user value.
- [ ] Step 12: Define error handling & recovery: global error strategy, retry ceilings, crash recovery, interrupted-session handling, partial-failure behavior, degraded-mode UX.
- [ ] Step 13: Define observability & analytics: crash reporting, performance telemetry, network tracing, journey/screen analytics, startup and battery telemetry, release monitoring, logging policy, PII redaction, sampling, retention.
- [ ] Step 14: Define testing strategy: unit/integration/UI-automation/offline/device-compat/accessibility/performance-regression scope, emulator vs physical-device expectations, release gating, rollback validation.
- [ ] Step 15: Release & operations callouts: summarize channels, staged rollout, store submission, forced-upgrade, deprecation as ADR candidates. Defer ownership to [`operations`](../operations/SKILL.md) / [`infrastructure-platform`](../infrastructure-platform/SKILL.md).
- [ ] Step 16: Define the failure taxonomy: startup, network, sync conflict, rendering degradation, termination, permission denial, notification failure, API incompatibility, storage exhaustion, background failure; per failure define detection, mitigation, recovery, observability, and user-facing behavior.
- [ ] Step 17: Generate `mobile-architecture.md` from `assets/mobile-architecture.template.md`. Consolidate ADR candidates (numbering, status, alternatives, downsides). Validate against [standards/architecture-schema](../../../standards/architecture-schema/README.md) and `references/mobile-architecture-quality-rubric.md`; revise until both pass or explicitly note any unresolved gap.

## Outputs

Required:

- `mobile-architecture.md` at `docs/architecture/<product-slug>/mobile-architecture.md`, with frontmatter and the 18-section structure per [standards/architecture-schema](../../../standards/architecture-schema/README.md).

Optional, when applicable:

- Navigation diagrams; state-ownership maps; offline-sync diagrams; notification-routing diagrams.
- Performance-budget tables; failure-mode matrices; ADR drafts.

Output rules:

- Keep the architecture decision-oriented and user-impact focused, not framework-decorative.
- Document tradeoffs and the rejected alternative, not only the chosen path.
- Keep security/privacy and release/operations as callouts and ADR candidates, never owned designs.
- No vendor SDK detail unless it materially changes architecture behavior.

## Quality checks

- [ ] `references/mobile-architecture-quality-rubric.md` was loaded before finalizing.
- [ ] `mobile-architecture.md` validates against [standards/architecture-schema](../../../standards/architecture-schema/README.md): frontmatter complete; required sections present; conditional sections present with content or listed under `## Omitted sections` with rationale.
- [ ] Platform strategy records rationale and trade-offs as an ADR candidate.
- [ ] Navigation ownership and state-restoration behavior are defined.
- [ ] State ownership and synchronization rules are explicit.
- [ ] Offline behavior is defined for every critical user journey.
- [ ] Device-capability usage names a permission strategy, privacy posture, and fallback.
- [ ] Performance and battery budgets state measurable targets and degradation behavior.
- [ ] Accessibility posture is explicitly documented.
- [ ] Notification and interruption policies are documented.
- [ ] Error handling and degraded behavior are defined.
- [ ] Observability includes crash, latency, and release telemetry with PII redaction.
- [ ] Testing covers offline, accessibility, and device compatibility.
- [ ] Security/privacy and release/operations appear only as callouts / ADR candidates, not owned designs.
- [ ] No vendor SDK implementation detail appears unless it materially changes architecture behavior.

## References

- Upstream: [`architecture/system-design`](../system-design/SKILL.md).
- Related: [`backend-architecture`](../backend-architecture/SKILL.md), [`security`](../security/SKILL.md) (mobile security callouts), [`operations`](../operations/SKILL.md) / [`infrastructure-platform`](../infrastructure-platform/SKILL.md) (release/signing callouts), [`performance`](../performance/SKILL.md), [`quality-engineering`](../quality-engineering/SKILL.md), [`frontend-architecture`](../frontend-architecture/SKILL.md) (optional shared cross-reference; mobile-web/PWA boundary).
- Downstream implementation skills: future `implementations/mobile/<ecosystem>` (e.g. `ios`, `android`, `cross-platform`).
