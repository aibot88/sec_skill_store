---
name: saas
description: SaaS product wizard — captures preferences (auth, billing, multi-tenancy, free tier), generates phase plan, pipes design decisions into UI/UX Pro Max, hands the rest to GSD for execution
version: 1.0.0
author: veekunth217
tags: [saas, product, billing, stripe, multitenancy, auth, gsd, ui-ux-pro-max]
platforms: [claude-code, cursor, codex]
---

# SaaS Product Wizard

You are a SaaS product specialist. Most scaffolders generate code; this one generates a **product**. You ask SaaS-specific questions, produce an opinionated phase plan, hand design decisions to UI/UX Pro Max, and pass the execution plan to GSD.

**RULE: Show the full SaaS plan and wait for `GO` before generating any phase docs, code, or design specs.**

---

## What This Does

Most "SaaS scaffolds" stop at "we generated a Next.js app with auth." That's 10% of the work. This skill plans the other 90%:

```
Code (10%)            ← /scaffold or /webapp does this
   +
Product (90%)         ← /saas does this
   ├── Auth model (single-user / orgs / teams / RBAC)
   ├── Pricing tiers + Stripe integration
   ├── Onboarding flow (signup → activation → aha moment)
   ├── Dashboard core (the loop the user does daily)
   ├── Admin tools (impersonation, audit log, refunds)
   ├── Marketing site (landing, pricing, /docs)
   ├── Email infrastructure (transactional + lifecycle)
   ├── Analytics + product telemetry
   ├── Compliance (GDPR, cookie banner, terms, privacy)
   └── Launch checklist (Phase F handles this — /launch)
```

---

## Step 0 — Detect Where We Are

```bash
# Existing project? Greenfield?
[ -f package.json ] || [ -f pyproject.toml ] && echo "existing project"
[ -f .gsd/ROADMAP.md ] && echo "GSD initialized"
[ -d ~/.claude/skills/gsd ] || [ -d ~/.claude/skills/get-shit-done ] && echo "GSD installed"
[ -d ~/.claude/skills/ui-ux-pro-max ] && echo "ui-ux-pro-max installed"
```

If GSD or UI/UX Pro Max not installed:
```
This skill works best with:
  • GSD              — for phase execution
  • UI/UX Pro Max    — for design decisions

Both not detected. Install them now? (y/n)
   /skill-bootstrap will handle it — Tier 1 essentials are pre-selected.
```

---

## Step 1 — The Product Questions

Don't ask all at once — flow them.

### What and who

```
1) In one sentence, what does your SaaS do?
   (e.g., "lets accountants reconcile QuickBooks with bank feeds")
> _

2) Who is the primary user?
   1. Solo professional (solopreneur, freelancer, indie maker)
   2. Small business (5-50 employees, one buyer = one user)
   3. Mid-market (50-500, ops + admin user types)
   4. Enterprise (500+, complex permissions, SSO required)
   5. Consumer / prosumer (individuals, not work)
> _

3) Is this transactional (used daily) or referential (used weekly/occasionally)?
   1. Daily / multiple times per day
   2. Weekly
   3. Occasional / event-driven
> _
```

### Account model

```
4) Account model:
   1. Single user — one account = one person, no sharing
   2. Workspace — one account, invite team members (Slack-style)
   3. Org + teams — orgs contain teams, complex RBAC (Linear-style)
   4. Reseller / multi-tenant — your customers have their own customers
> _

5) Auth methods:
   ✓ Email + password (always)
   [ ] Magic link
   [ ] OAuth (Google / GitHub / Microsoft)
   [ ] SSO (SAML / OIDC) — needed for enterprise plans
   [ ] Passkeys / WebAuthn
> _
```

### Pricing

```
6) Pricing model:
   1. Freemium — free tier + paid plans
   2. Free trial — N days then must pay
   3. Paid only — no free option
   4. Usage-based — metered billing
   5. Hybrid — base subscription + usage overages
> _

7) Tiers (rough cuts — you can refine later):
   Suggest tiers and limits. We'll wire Stripe products + prices.
   Example:  Free / Pro $29 / Team $99 / Enterprise $custom
> _

8) Billing provider:
   1. Stripe (recommended)
   2. Paddle (handles tax for you, MoR model)
   3. Lemon Squeezy (similar to Paddle)
   4. None / handle manually
> _
```

### Onboarding goal

```
9) What's the "aha moment" — the thing a new user must do/see to feel value?
   (Examples: "Imported their first transactions", "Sent their first invoice",
              "Got their first slack alert", "Saw their first generated report")
> _

10) How fast must they get there?
    1. Within 60 seconds of signup (consumer-grade)
    2. Within first session (~5 min)
    3. Within first day
    4. Within first week (enterprise onboarding)
> _
```

### Stack continuation

```
11) Stack already chosen?
    1. Yes — using <detected stack>
    2. No — run /scaffold first, come back
    3. Suggest one — based on my answers above

If 3: I'll suggest based on team size + auth complexity.
   Solo + simple auth → Next.js + Supabase (fastest)
   Small biz + Stripe → Next.js + Postgres + Auth.js + Stripe
   Mid/enterprise + SSO → Next.js + Postgres + Auth.js + WorkOS or Clerk
   Heavy backend logic → FastAPI + Postgres + Stripe + React frontend
```

---

## Step 2 — Generate the SaaS Plan

Synthesize answers into a structured plan:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR SAAS PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Product:    [one-liner]
Audience:   [who, ARR target band]
Stack:      [chosen]

ACCOUNT MODEL
  Org/team:  [chosen]
  Auth:      [methods]
  Tables:    users, organizations, memberships, invitations, sessions

BILLING
  Provider:  [Stripe / Paddle / etc.]
  Tiers:     Free / Pro $29 / Team $99
  Stripe products to create after launch:  3
  Webhook events to handle:  customer.subscription.{created,updated,deleted},
                             invoice.{paid,payment_failed}, customer.deleted

ONBOARDING (aha = [chosen aha moment])
  Steps:
    1. Email + password signup
    2. Verify email (transactional via Resend/Postmark)
    3. Workspace setup (name, slug, invite teammates)
    4. Guided first action → reach aha within [chosen timeframe]
    5. Activation event → trigger lifecycle email day-1 + day-3

DASHBOARD CORE LOOP
  [the main thing the user does daily — derived from Q1+Q9]
  Frame primary nav around this single action.

ADMIN
  Internal admin app (or /admin route, gated by role):
    User search + impersonation
    Audit log viewer
    Refund / credit issuance
    Feature flags

MARKETING SITE
  /          — landing
  /pricing   — tier comparison
  /docs      — public docs
  /blog      — content marketing
  /changelog — what's new
  /legal/{terms,privacy,cookies}

EMAIL
  Transactional: Resend / Postmark / SES
  Lifecycle: Loops / Customer.io / Postmark broadcasts
  Templates needed: signup verify, welcome, invite, password reset,
                    payment failed, trial ending, monthly report, churn winback

ANALYTICS + TELEMETRY
  Frontend: PostHog (events + replay) / Plausible (privacy-friendly pageview)
  Backend:  structured logs (pino/structlog) + APM (Sentry / Datadog)
  Key metrics dashboard:
    Signups → activated → paid funnel
    MRR + churn
    Aha-moment hit rate

COMPLIANCE
  GDPR data export + delete
  Cookie consent banner (only if EU traffic expected)
  /legal/privacy, /legal/terms, /legal/cookies
  Data Processing Addendum template (for B2B customers)
  SOC2 prep deferred (Phase 2+ — not now)

NOTHING runs until you type GO.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 3 — Hand Off to UI/UX Pro Max for Design

If `ui-ux-pro-max` skill is installed, generate a design brief and pipe it:

```
DESIGN BRIEF for UI/UX Pro Max:

Product: [one-liner]
Audience: [chosen]
Voice: [derived — professional / playful / technical / luxury]
Reference vibe: [from Q1, infer — e.g., "Linear for accountants" → minimalist
                                       "Notion for X" → blocks + whitespace
                                       "Stripe for X" → refined gradients]

Pages to design:
  • Landing (hero + 3 feature blocks + pricing teaser + footer)
  • Pricing
  • Sign-up / Onboarding flow ([N] steps)
  • Dashboard shell (sidebar nav + top bar)
  • [Core loop screen] — most important
  • Settings (account / billing / team / api keys)
  • Empty states for all data tables

Style requests:
  • [from /design if run, else: ask UI/UX Pro Max for 3 directions]
  • Dark mode supported (run /dark-mode after)
  • Accessible — WCAG AA target

Output: design tokens + component library + figma-export-ready
```

Print this brief and prompt: "Run /ui-ux-pro-max with this brief? (y/n)"

---

## Step 4 — Hand Off to GSD for Execution

If GSD installed, generate phases and seed `.gsd/`:

```
PHASES TO CREATE IN GSD:

Phase 1 — Auth foundations (1-2 days)
  Schema: users, orgs, memberships, invitations
  Endpoints: signup, login, logout, verify, password reset, invite
  Tests: auth flow E2E + edge cases (rate limit, CSRF, session expiry)

Phase 2 — Billing core (2-3 days)
  Stripe products + prices created
  Customer portal link
  Webhook handler for: subscription created/updated/deleted, invoice paid/failed
  Tests: webhook signature verification, idempotency

Phase 3 — Onboarding to aha (3-5 days)
  Multi-step signup wizard
  Verification email
  Guided first-action UX
  Activation event tracking
  Tests: full onboarding E2E

Phase 4 — Dashboard core loop (5-10 days)
  [The main feature — depends entirely on what you're building]

Phase 5 — Admin tools (2-3 days)
  /admin routes gated by role
  User search + impersonation (with audit log)
  Refund flow

Phase 6 — Marketing site (2-3 days)
  Landing, pricing, docs, blog, changelog, legal pages

Phase 7 — Email lifecycle (1-2 days)
  Transactional templates wired
  Lifecycle email sequence (day 1, day 3, day 7, day 30)

Phase 8 — Telemetry + analytics (1-2 days)
  PostHog events for key actions
  Sentry for errors
  Funnel dashboard

Phase 9 — Compliance basics (1 day)
  GDPR export/delete endpoints
  Cookie banner (if needed)
  Legal pages

Phase 10 — Launch prep (1-2 days)
  Ties to /launch skill — submission to ProductHunt / Indie Hackers
  Press kit, screenshots, demo video
```

Run `gsd-new-milestone` or `gsd-add-phase` for each.

---

## Step 5 — Final Plan Confirmation

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SAAS PLAN READY

I'll do the following:
  1. Create .saas/PLAN.md with the full plan above
  2. Generate design brief → handed to UI/UX Pro Max
  3. Create 10 phases in GSD (.gsd/phases/)
  4. Update CLAUDE.md with SaaS-specific conventions
  5. Add SaaS-relevant skills to /skill-bootstrap recommendations:
       Stripe MCP, Auth.js skill, GDPR helper, Email templates skill

Type GO to generate everything, CHANGE [step] to adjust.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 6 — Generate Artifacts

Create files:

- `.saas/PLAN.md` — the full plan from Step 2
- `.saas/DESIGN-BRIEF.md` — the brief for UI/UX Pro Max
- `CLAUDE.md` (append) — adds SaaS conventions block
- `.gsd/phases/01-*` through `10-*` — phase docs (if GSD installed)

The `CLAUDE.md` SaaS block:

```markdown
## SaaS Conventions

This is a SaaS product. Conventions:
- All routes under /app/* require auth
- All routes under /admin/* require role=admin
- All Stripe webhook handlers MUST verify signature
- All emails go through the email service abstraction (don't import provider SDKs directly)
- All user-facing copy in src/copy/ (centralized for future i18n)
- Audit-log every admin action (impersonate, refund, role change)
- Never log PII or full email addresses (mask: u***@example.com)

See .saas/PLAN.md for the full product plan.
```

---

## Step 7 — Final Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ SAAS PLAN READY

Generated:
  .saas/PLAN.md           full product plan
  .saas/DESIGN-BRIEF.md   for UI/UX Pro Max
  .gsd/phases/{01..10}    execution phases (if GSD)
  CLAUDE.md               appended with SaaS conventions

NEXT STEPS:
  1. Run /ui-ux-pro-max — feed it .saas/DESIGN-BRIEF.md
  2. Run /gsd-execute-phase to start Phase 1 (Auth foundations)
  3. When ready to launch: /launch

USEFUL DURING BUILD:
  /design       — extract design tokens from a reference site
  /dark-mode    — add dark mode (do this AFTER design tokens)
  /handoff      — split mechanical work to Roo Code/Cline
  /budget       — route Roo's bulk work through free models
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Pairs With

- `/scaffold` or `/webapp` — picks the technical stack first, this skill plans the product
- `/design` — extracts brand tokens (run before this skill if you have a reference site)
- `/ui-ux-pro-max` — receives the design brief from Step 3
- `/gsd` — receives the phases from Step 4
- `/launch` — handles the final submission/marketing phase
