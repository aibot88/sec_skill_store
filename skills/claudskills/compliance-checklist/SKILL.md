---
name: compliance-checklist
description: >
  Provides a checklist framework for surfacing potentially applicable
  application-compliance obligations across declared jurisdictions
  (Japan / EU / US-CA / platform stores). The Skill is invoked by
  product-manager, security-reviewer, and technical-writer when a
  capability that may have legal exposure is added (chat / payments /
  PII collection / data export). It emits a checklist with
  primary-source citations and a mandatory disclaimer block; it never
  marks items as "complied with" — only the human reviewer can.

  Skill contents (Progressive Disclosure):
    SKILL.md          — overview, six invariant rules, output contract, navigation
    disclaimers.md    — the mandatory disclaimer block, in EN and JA
    triggers.md       — capability-detection rules and PII-path refusal globs
    jurisdictions/JP.md      — Japan: 電気通信事業法 / 特定商取引法 / 改正個人情報保護法 / 資金決済法
    jurisdictions/EU.md      — GDPR (with Art. 3 extraterritorial scope)
    jurisdictions/US-CA.md   — CCPA / CPRA
    jurisdictions/platform.md — Apple App Store / Google Play

  This Skill is bilingual where its output reaches end users (the
  disclaimer block ships in EN and JA). Reference files for individual
  jurisdictions are written in the jurisdiction's primary language
  plus English headings, so the citation links remain checkable by
  any operator.
disable-model-invocation: true
arguments: []
---

# Compliance Checklist

## Purpose

Surface potentially applicable application-compliance obligations for a
project's declared jurisdictions, citing only primary sources, behind a
mandatory disclaimer that this output is not legal advice.

The Skill's contribution is **structure**, not legal substance. It
ensures that:

1. Recurring failure modes (chat features missed under
   電気通信事業法, payment flows missed under 特定商取引法 §11, PII
   surfaces missed under 改正個人情報保護法 / GDPR Art. 3 / CCPA) are
   *brought to the surface* during release prep, not silently shipped.
2. Every applicability claim points the human reviewer at a primary
   source they can read themselves.
3. The output never asserts non-applicability — only "applies",
   "may apply, verify", or "out of scope for declared jurisdictions".
4. The output never marks items as "complied with" or
   "no further action needed". Compliance status is something only the
   human reviewer (and ultimately a qualified attorney) can confirm.

## When to invoke

This Skill ships **default-off**. It is invoked only when both:

- `.claude/compliance.yml` exists and has `compliance.enabled: true`.
- The CLAUDE.md or sibling config declares `target_jurisdictions:`
  with at least one of `JP`, `EU`, `US-CA`, `platform`.

If `compliance.enabled` is true but `target_jurisdictions` is missing
or empty, the Skill **refuses to run** and emits a single-line error
asking the operator to declare jurisdictions. It does not guess.

Typical invocation triggers (called by other agents):

- `product-manager` — when writing acceptance criteria for any
  capability listed in `triggers.md`.
- `security-reviewer` — when reviewing PII-handling, authentication,
  or external-data-export surfaces.
- `technical-writer` — when authoring or updating Terms of Service,
  Privacy Policy, or refund-policy text.

Do **not** invoke for:

- Internal CLI tools that never reach end users.
- Test fixtures or seed data work (these paths are explicitly
  refused — see Invariant 3).
- Bug fixes that do not change the capability surface.

## Invariant Core

The six rules below are inlined here because they are load-bearing for
the Skill's safety profile. Deviation from any of them is a defect,
not a tuning choice.

For full rationale and original-source citations, see [ADR-011].

1. **No negative-applicability claims.** The Skill must never assert
   "this law does not apply" or "you are exempt". Permitted forms:
   - `applies` — clear positive applicability.
   - `may apply, verify` — likely applicable, requires human
     confirmation.
   - `out of scope for declared jurisdictions` — neutrally states the
     law was not evaluated because it is not in the project's
     `target_jurisdictions`. This is a *scope* statement, not an
     applicability statement.

2. **Primary-source-only citation, with a Tier 1.5 allowance for
   issuing-regulator official interpretive guidance.** Every
   applicability claim must cite a Tier 1 primary source. Tier 1.5
   guidance is admissible only paired with a Tier 1 citation on the
   same item. Secondary sources are disqualifying. The full tier
   structure is fixed by [ADR-013] and propagates to the rest of
   the verification-layer.

   - **Tier 1 — primary statute and first-party platform spec.**
     e-Gov 法令検索 for Japanese statutes, EUR-Lex for EU
     regulations and directives, California Legislative Information
     for CCPA / CPRA, the official Apple App Store Review Guidelines
     and Google Play Policy Center for platform rules.
   - **Tier 1.5 — issuing-regulator official interpretive
     guidance.** Closed allowlist, fixed at the ADR layer (extending
     it requires a new ADR, not a Skill body edit):
     - **EDPB** Guidelines, Recommendations, Opinions adopted under
       GDPR Art. 70(1)(e).
     - **個人情報保護委員会 (PPC)** ガイドライン, Q&A, 通達
       under 個人情報保護法 §147–§149 delegation.
     - **California Privacy Protection Agency (CPPA)** Regulations
       under CCPA §1798.185.
     - **Apple** Privacy Manifest specification and Required
       Reasons API documentation under Apple's first-party platform
       authority.
     - **Google** Play User Data policy and SDK Index documentation
       under Google's first-party platform authority.

     Tier 1.5 admits only formal instruments under the regulator's
     enabling-statute authority. Excluded as Tier 1.5: regulator
     blog posts, press releases, staff op-eds, social-media posts,
     FAQ landing pages. A Tier 1.5 citation must always appear
     alongside a Tier 1 citation on the same checklist item.

   - **Disqualifying.** Blog summaries, Q&A sites, AI summaries,
     news articles, law-firm explainers, regulator informal output
     (blog posts, press releases). Same rule as the research domain
     of ADR-008/010.

3. **PII path refusal.** The Skill must refuse to ingest paths likely
   to contain test data, seeds, environment files, or database dumps.
   The concrete glob list and PII regex masks live in
   [`triggers.md`](./triggers.md). On refusal, the Skill emits a
   single-line message naming the offending path and stops.

4. **Default-off, opt-in per project.** The Skill runs only when both
   `compliance.enabled: true` (in `.claude/compliance.yml`) and a
   non-empty `target_jurisdictions` are declared. Either condition
   missing is a hard refusal, not a fallback.

5. **Project-declared jurisdictions, never guessed.** The Skill does
   not infer jurisdiction from currency, language, domain TLD, or
   user-list samples. Jurisdiction is a project assertion. If the
   declared list is wrong, that is a project-level configuration
   defect surfaced by the Skill's behavior, not a bug for the Skill
   to compensate around.

6. **Capability-based triggers only.** Trigger detection works on
   capabilities (manifest dependencies, AST patterns of HTTP routes,
   form-field schemas), not on file or route names. The trigger
   rules are in [`triggers.md`](./triggers.md). When a dependency
   signal is ambiguous, the Skill asks the human a closed-form
   question (yes / no / "I don't know — skip and re-run later") and
   records the answer in the output's audit trail.

## Output contract

Every invocation produces a Markdown report with these sections, in
this order, all required:

```markdown
# Compliance Checklist — <feature or release name>

## Disclaimer

<contents of disclaimers.md, EN + JA, verbatim — must not be edited
or removed by the Skill>

## Project context

- target_jurisdictions: [<list from CLAUDE.md / compliance.yml>]
- triggered capabilities: [<list from triggers.md detection>]
- ambiguous-trigger answers: [<list of human Q&A, if any>]
- evaluation date: <YYYY-MM-DD>

## Findings per jurisdiction

### JP (if in scope)
- 電気通信事業法 — `applies` | `may apply, verify` | `out of scope ...`
  - Citation: <e-Gov URL>
  - Reason: <one-line rationale tied to the triggered capability>
  - Human action: <what the human reviewer must verify or decide>
- 特定商取引法 §11 — ...
- 改正個人情報保護法 — ...
- 資金決済法 — ...

### EU (if in scope)
- GDPR — ...

### US-CA (if in scope)
- CCPA / CPRA — ...

### platform (if in scope)
- App Store Review Guidelines — ...
- Google Play Policy Center — ...

## Required human follow-up

- [ ] Qualified-attorney review before launch (always, never marked
      complete by the Skill).
- [ ] Each `applies` and `may apply, verify` item above resolved by a
      human.
- [ ] If Terms of Service / Privacy Policy / refund-policy text was
      derived from this checklist, that text reviewed by counsel
      before publication.

## Audit trail

- Skill version: <semver from this SKILL.md frontmatter, when
  introduced>
- Jurisdiction reference files consulted:
  [`JP.md`](./jurisdictions/JP.md), [`EU.md`](./jurisdictions/EU.md),
  ...
- Operator: <git user.email if available, else "unknown">
```

The Skill **never** writes a `## Compliance status` section. There is
no field for "complied with" or "verified". The closest the report gets
is the unchecked checkbox under "Required human follow-up". A
human checks those boxes outside the Skill's authoring path.

## Override Protocol

Adopting projects can disable individual Invariant rules **only**
when the rule does not fit their context, and only with an explicit
declaration in the project's own `CLAUDE.md`:

```markdown
## Compliance Skill overrides

- Invariant 5 (project-declared jurisdictions): partially overridden.
  We auto-derive `target_jurisdictions` from the customer-billing
  country code at runtime because we serve >40 jurisdictions and
  manual declaration is impractical.
  Reason: <why>. Date: <YYYY-MM-DD>. Risk acceptance signed by:
  <human name>.
```

What you **cannot** override:

- Invariants 1 (no negative-applicability claims), 2 (primary-source
  citation), and 3 (PII path refusal). These are safety-critical;
  removing them turns the Skill from "useful but limited" into
  "actively harmful".
- The mandatory disclaimer block (Invariant — implicit in
  `disclaimers.md`).
- The English-only meta-files of this Skill (this `SKILL.md` and
  `triggers.md` are operator-facing references).

If you find yourself overriding two or more invariants, the Skill is
not a fit for your project. Delete the directory; that is also a
supported state.

## Skill update cadence

This Skill's jurisdiction reference files (`jurisdictions/*.md`) cite
laws that change. Re-verification cadence:

- **Half-yearly** (180 days) for the `JP`, `EU`, and `US-CA`
  jurisdictions, manually, by `docs-researcher` per the
  research-domain protocol of `verification-layer` (ADR-008/010).
  Citations are re-fetched from primary sources only.
- **Quarterly** (90 days) for the `platform` jurisdiction, because
  Apple App Store Review Guidelines and Google Play policies change
  materially more often than statutory text. The shorter cadence is
  reflected in `.claude/compliance.yml.example`'s
  `reverification_days.platform` default.
- **On amendment notice**, when an operator becomes aware of a law
  change in any of `target_jurisdictions`. The operator opens an
  Issue using the citation as evidence; the next half-yearly pass
  picks it up sooner if needed.

If a re-verification finds that a cited statute or platform policy
has changed, the right response is: (1) update the relevant
`jurisdictions/<X>.md`, (2) record the change in the project
CHANGELOG with the verification date, (3) re-run the Skill on any
recently-shipped capability that depended on the changed citation.

If the cadence is missed for two consecutive intervals (i.e., one
year without re-verification), the Skill's output should include a
prominent staleness warning in the Disclaimer section. Implementation
of that warning is part of `disclaimers.md`'s rendering logic, not
this overview.

## Out-of-scope by design

The Skill does **not**:

- Author Terms of Service, Privacy Policy, refund-policy, or any
  other legal document text. It produces the *requirements list* that
  `technical-writer` uses as input. Document drafting, even derived
  from a Skill checklist, has too high a blast radius for LLM-only
  output.
- Cover vertical-specific compliance regimes. For healthcare PHI,
  point to ECC's `hipaa-compliance` and `healthcare-phi-compliance`
  Skills. For financial KYC/AML, point to the operator's specialized
  legal counsel — ECC has no equivalent Skill, and this Skill should
  not pretend to. The same applies to broadcasting, gambling, gun
  sales, alcohol, controlled substances, and any other regime where
  a small mistake has large legal consequences.
- Make cross-jurisdictional decisions. If a capability triggers
  obligations in JP and EU and US-CA simultaneously, the Skill lists
  each independently. Synthesizing "if you do X for JP, you also
  satisfy EU" is the kind of cross-regime reasoning that requires a
  qualified attorney.

## See also

- [`disclaimers.md`](./disclaimers.md) — the mandatory disclaimer
  block, EN and JA.
- [`triggers.md`](./triggers.md) — capability-detection rules and
  PII-path refusal globs.
- [`jurisdictions/JP.md`](./jurisdictions/JP.md),
  [`jurisdictions/EU.md`](./jurisdictions/EU.md),
  [`jurisdictions/US-CA.md`](./jurisdictions/US-CA.md),
  [`jurisdictions/platform.md`](./jurisdictions/platform.md) —
  per-jurisdiction citation tables.
- [ADR-011] — design rationale, the six invariants, and the
  rejected-alternatives table that produced this Skill rather than an
  agent.
- [ADR-013] — Invariant 2 source tier model. Defines Tier 1 / Tier 1.5
  / disqualifying, the closed Tier 1.5 regulator allowlist, the
  pairing rule, and the verification-layer-wide scope.

[ADR-011]: ../../meta/adr/011-compliance-checklist-skill.md
[ADR-013]: ../../meta/adr/013-invariant-2-source-tier-model.md
