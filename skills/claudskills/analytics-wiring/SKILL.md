---
name: analytics-wiring
description: When a page or stack needs analytics instrumentation - event tracking, conversion goals, funnel events, consent banners. Triggers - "analytics setup", "GA4", "Plausible", "PostHog", "track conversions", "event tracking", "set up tracking", "conversion goals", "consent banner", "cookie consent". Wires Plausible by default (privacy-first), GA4 if the operator insists, PostHog if event-tracking funnels need it. Standardizes event names across the toolkit.
metadata:
  version: 0.1.0
---

# Analytics Wiring

You instrument pages with analytics so the operator can measure what's converting. The default is **Plausible** (privacy-first, $9/mo, no cookie banner needed in most jurisdictions). GA4 is the fallback if a client insists. PostHog is the layer when funnels need event-level tracking.

## Standard event taxonomy

Every page in the toolkit fires a consistent set of events. Standardization matters — it lets the operator copy the same dashboards across every client.

| Event | When | Required props |
|---|---|---|
| `page_view` | Every page load (auto from analytics provider) | `page_path`, `page_title` |
| `cta_clicked` | Primary or transitional CTA clicked | `cta_id` (slug like `hero-primary`), `cta_label`, `cta_destination` |
| `lead_submitted` | Form submitted successfully | `form_id`, `form_type` (`contact`, `audit-request`, `lead-magnet`, `application`) |
| `call_booked` | Cal.com / SavvyCal booking confirmed | `booking_type`, `service` |
| `pricing_viewed` | Pricing block enters viewport | none |
| `funnel_step_advanced` | User advances in a multi-step funnel | `funnel_id`, `from_step`, `to_step` |
| `video_played` | VSL or demo video starts | `video_id`, `video_title` |
| `video_25/50/75/100` | Video progress milestones | `video_id`, `progress_pct` |
| `quiz_started` / `quiz_completed` | Quiz funnel | `quiz_id`, `result` (on completion) |

Don't deviate without a reason. Custom events are added to `references/event-taxonomy-extensions.md` and reviewed quarterly.

## Workflow

### Step 1 — load context

Read `.agents/agency-context.md` §13 (Tech / Domain Inventory). Determine which provider(s) are configured.

If §13 is empty or vague, ask via `AskUserQuestion`:
> "Which analytics setup?"
> - "Plausible (recommended — privacy-first, no cookie banner)"
> - "GA4 (operator client requirement)"
> - "PostHog (event-tracking funnel)"
> - "Combo: Plausible + PostHog (funnels)"

Persist the choice to §13.

### Step 2 — install the provider

For Plausible:
- Add the Plausible script to the `Layout` component:
  ```html
  <script defer data-domain="{domain}" src="https://plausible.io/js/script.js"></script>
  ```
- Use the custom-events extension for our event taxonomy:
  ```html
  <script defer data-domain="{domain}" src="https://plausible.io/js/script.tagged-events.js"></script>
  ```
- Verify install via Plausible's installation checker.

For GA4:
- Add the GA4 gtag script to Layout.
- Configure events via `gtag('event', '{event_name}', { ...props })`.
- Add a cookie consent banner (we ship one in `design-system/primitives/CookieBanner.tsx`).

For PostHog:
- Install the JS SDK: `npm i posthog-js`.
- Initialize in a client-only script in Layout:
  ```ts
  import posthog from 'posthog-js';
  if (typeof window !== 'undefined') {
    posthog.init('{PUBLIC_POSTHOG_KEY}', { api_host: 'https://app.posthog.com' });
  }
  ```
- Wire `posthog.capture('{event_name}', props)` to our event taxonomy.

### Step 3 — wire CTA tracking

Every CTA component (`Button` with `as="a"`, or `<a class="cta">`) needs an `onClick` (or analytics-aware Link wrapper) that fires `cta_clicked`. The `Button` primitive in `design-system/primitives/Button.tsx` has this baked in via a `trackingId` prop.

```tsx
<Button trackingId="hero-primary" href="/audit">Get my dental SEO audit</Button>
```

The Button's onClick fires the event with `cta_id="hero-primary", cta_label="Get my dental SEO audit", cta_destination="/audit"` automatically.

### Step 4 — wire form tracking

Every form (`<Form>` primitive in our shadcn integration) wraps its submit handler to fire `lead_submitted` on success.

For Resend / Formspree forms:
- Server action returns success → fire `lead_submitted`.
- Server action returns error → fire `lead_submission_error`.

### Step 5 — wire funnel tracking

For multi-step funnels (`/new-funnel` outputs), every step transition fires `funnel_step_advanced`.

For VSL pages:
- Wire the video player events (HTML5 `play`, `timeupdate`, `ended`) to `video_played` + the 25/50/75/100 milestones.

### Step 6 — wire conversion goals

Configure the provider's goal/conversion settings:

- Plausible: goals for `lead_submitted`, `call_booked`, `cta_clicked` (per CTA ID if needed).
- GA4: conversion events for the same.
- PostHog: insights for funnels (page_view → cta_clicked → lead_submitted → call_booked).

### Step 7 — verify

Run the test suite:
1. Open the dev preview.
2. Click each primary CTA — verify `cta_clicked` fires with correct props.
3. Submit each form with test data — verify `lead_submitted` fires.
4. (For funnels) walk all steps — verify each `funnel_step_advanced`.
5. Check the analytics dashboard within 5 min for event ingestion.

If any step fails, fix before passing the page to `qa-reviewer`.

---

## Hard rules

### Privacy & consent

- **Plausible** doesn't require a cookie banner in most jurisdictions (no PII, no cross-site tracking).
- **GA4** requires an explicit consent banner with reject-all option. We ship `CookieBanner` primitive that handles GDPR / CCPA defaults.
- **PostHog** with autocapture on requires consent. Recommend "session recording off" by default; enable only on operator request with explicit consent UX.
- Never store PII in event props (no email, no phone, no name in `lead_submitted` props — those go to the CRM, not the analytics tool).

### Event-name discipline

- All event names are `snake_case`, lowercase.
- Use the standard taxonomy. Don't invent `clicked_button` when `cta_clicked` exists.
- Custom events are added to the extensions doc with rationale.

### No tracking on dev / staging

- Use `NODE_ENV` checks to skip analytics on dev / staging. Otherwise the operator's local clicks pollute the production analytics.
- Plausible has a "exclude pages" config that does this server-side.

## Anti-patterns

- **Track every click on the page.** Noise. Track CTAs and conversion-relevant events.
- **Tracking that double-fires.** A common bug — both `onClick` and `onSubmit` firing the same event. Fix at the primitive level.
- **PII in event props.** Never. Use the CRM for PII; analytics for behavior.

## References

- `references/event-taxonomy-extensions.md` — custom events the agency has added.
- `references/plausible-setup.md` — full Plausible install + goals setup.
- `references/ga4-setup.md` — GA4 install + conversion events + GTM if needed.
- `references/posthog-setup.md` — PostHog install + funnels + insights.
- `references/cookie-consent-implementations.md` — GDPR / CCPA / hybrid implementations.

## Related skills

- `agency-context` — §13 holds analytics provider IDs.
- `component-library` — provides `Button` primitive with `trackingId` prop.
- `ship-checklist` — verifies analytics fire correctly during QA.
