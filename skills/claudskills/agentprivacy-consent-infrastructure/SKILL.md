---
name: agentprivacy-consent-infrastructure
description: >
  Consent infrastructure and IEEE 7012 MyTerms integration for
  0xagentprivacy. Activates when discussing bilateral consent,
  cookie-slashing, consent receipts, Customer Commons, MyTerms Alliance, or
  how P·C·Σ creates enforceable consent rather than checkbox compliance.
license: Apache-2.0
metadata:
  version: "4.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Consent UX designers, IEEE 7012 implementers, Customer Commons contributors, cookie management builders, GDPR/ePrivacy architects"
  equation_term: "P (consent enforcement), C (verifiable consent terms), Σ (consent as bilateral promise)"
  template_references: "warden, ambassador, pedagogue, witness, assessor"
---

# PVM-V4 Skill — Consent Infrastructure

**Source:** Privacy Value Model V4 + IEEE 7012 (MyTerms) + Customer Commons + First Person Spellbook
**Target context:** Consent UX designers, IEEE 7012 implementers, Customer Commons contributors, browser agent builders
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

The legal-technical bridge. Consent is where privacy architecture meets the real world — where mathematical guarantees translate into actual human agreements about data use. This skill covers the MyTerms standard (IEEE 7012), the Customer Commons framework, and how the Swordsman browser agent implements consent as a bilateral protocol rather than a checkbox.

Currently a footnote in policy_governance. This is the closest thing to a shipped product in the agentprivacy stack and deserves its own specification.

## The consent problem

Current consent infrastructure is broken in a specific, structural way:

**The take-it-or-leave-it pattern.** Websites present terms of service. Users accept or leave. There is no negotiation, no counterproposal, no bilateral agreement. This is not consent — it is capitulation. In Promise Theory terms, it is an imposition (+/−), not a cooperative promise.

**The checkbox theatre.** GDPR cookie banners present an illusion of choice. "Accept all" is one click; "manage preferences" is seventeen clicks across five screens. The interface design encodes a preference for maximum data collection while providing legal cover through the appearance of informed consent.

**The dark pattern economy.** Consent interfaces are optimised for acceptance, not comprehension. Deceptive design patterns — pre-checked boxes, confusing double negatives, hidden "reject all" buttons — systematically undermine informed consent. The regulation requires consent; the implementation undermines it.

**The structural failure.** All of these share a root cause: consent is currently unilateral. One party (the site) writes the terms. The other party (the user) can only accept or reject. There is no mechanism for the user to propose their own terms.

## IEEE 7012 — MyTerms

IEEE 7012 is the standard that inverts the consent flow. Instead of sites proposing terms to users, users propose terms to sites:

**The inversion.** The user (through their agent) presents their consent terms to the site. "Here are my conditions for data use. Do you accept?" The site can accept, reject, or counter-propose. This is bilateral negotiation — Promise Theory cooperation, not imposition.

**Term structure.** MyTerms are machine-readable consent documents. They specify: what data the user permits to be collected, for what purposes, for how long, with what sharing restrictions, and under what conditions the consent can be revoked. The terms are not prose — they are structured data that agents can parse and enforce.

**Automation.** Because MyTerms are machine-readable, the negotiation can be automated. The Swordsman browser agent carries the user's default MyTerms. When visiting a new site, the Swordsman presents the terms. The site's system evaluates them. If compatible, the visit proceeds under the user's terms. If incompatible, the Swordsman either negotiates or blocks.

**The standard's status.** IEEE 7012 is published. Customer Commons maintains the community framework. Adoption is early — the standard exists but widespread implementation requires browser agent infrastructure (which the Swordsman provides).

## Customer Commons

Customer Commons is the organisational home for user-side consent terms. Where Creative Commons standardised content licensing from the creator's perspective, Customer Commons standardises data consent from the customer's perspective.

**Standard terms.** Customer Commons maintains a library of standard MyTerms that users can adopt: "Do not track me across sites," "Do not sell my data," "Delete my data after 30 days," "Only use my data for the service I requested." These are the consent equivalent of CC-BY, CC-BY-SA, CC-BY-NC — recognisable, standardised, machine-enforceable.

**Community governance.** The terms are maintained by a community process. New terms are proposed, discussed, and standardised through open governance. This parallels the guild system in the agentprivacy architecture — communities defining their own consent standards.

## The Swordsman as consent agent

The swordsman_browser skill defines the browser agent. This skill specifies how that agent handles consent:

**Default terms loading.** At Blade tier, the Swordsman carries the user's default MyTerms. These are the minimum acceptable conditions. Any site that cannot meet them is blocked.

**Negotiation at Light tier.** When the Swordsman recognises a site (through repeated visits or VRC-established trust), it can negotiate modified terms. "For this specific site, I will allow analytics cookies but not third-party tracking." The negotiation produces a site-specific VRC that encodes the agreed terms.

**Enforcement at Heavy tier.** Multi-party consent locks. The Swordsman, the site, and a third-party auditor each hold a key. Consent changes require two-of-three agreement. This prevents either party from unilaterally modifying the terms after agreement.

**Ecosystem consent at Dragon tier.** The Swordsman's consent terms propagate across associated sites. A guild's standard MyTerms are recognised by all sites that participate in the guild's Privacy Pool. Consent scales through network effects rather than per-site negotiation.

## Consent as VRC

The agentprivacy architecture treats consent agreements as a specific type of VRC:

**Bilateral.** Both parties (user and site) attest to the terms. Neither can forge the other's agreement.

**Verifiable.** The terms and both attestations can be independently verified. A regulator can confirm that consent was genuinely bilateral without accessing the specific data involved.

**Temporal.** Consent VRCs accumulate in A(τ). Sites that maintain consent agreements over time build verified trust history. Sites that repeatedly violate or renegotiate terms show a degraded h(τ).

**Revocable.** Unlike a blockchain transaction, consent can be withdrawn. The consent VRC includes a revocation mechanism — the user can revoke at any time, and the revocation is itself attested and timestamped.

## Cookie sovereignty

The most immediate, practical application of consent infrastructure:

**Current state.** Cookies are set by sites, managed (poorly) by browsers, and governed (ineffectively) by regulation. The user's control is limited to "accept," "reject," or "manage" through hostile interfaces.

**Sovereign state.** The Swordsman manages cookies according to the user's MyTerms. Cookies that comply with the user's terms are accepted. Non-compliant cookies are blocked. The decision is automatic, consistent, and aligned with the user's stated preferences — not the site's desired preferences.

**The cursor chronicle.** Every cookie decision is logged by the Swordsman as a micro-transition in the sovereignty lattice. Accept a cookie = maintain current position. Block a cookie = enforce boundary (Protect dimension active). Negotiate terms = bilateral exchange (Project dimension active). The accumulated chronicle contributes to T(π).

## Connection to equation terms

**P (privacy strength).** Consent enforcement is the primary mechanism for P. A system where the user's consent terms are mathematically enforced (not just legally asserted) has higher P than one relying on site compliance.

**C (credential verifiability).** Consent VRCs are verifiable credentials. The consent itself becomes a credential — "this user consented to these terms at this time" is independently verifiable.

**Σ (separation matrix).** Bilateral consent is a Promise Theory cooperation. The user proposes (+), the site accepts (−). The bilateral structure maps directly to the separation matrix — consent terms define the boundary between what the user reveals (Project) and what the user withholds (Protect).

## BRAID deterministic branching validation

BRAID's deterministic branching principle (arXiv:2512.15959) provides external validation: their research found that nano-tier models "struggle with ambiguity" when graph edges are non-deterministic. If AI agents struggle with ambiguous reasoning instructions, consent instructions to AI agents must be equally unambiguous. IEEE 7012 / MyTerms deterministic consent logic is not just a governance preference — it is a technical requirement for reliable agent execution.

## Open problems

1. Browser implementation — how does the Swordsman agent integrate with existing browser cookie APIs?
2. Site adoption incentives — what motivates sites to accept user-proposed terms rather than imposing their own?
3. Term compatibility checking — how are MyTerms from different users compared for consistency within a Privacy Pool?
4. Regulatory recognition — will courts and regulators recognise automated bilateral consent as legally valid?
5. Legacy compatibility — how does MyTerms-based consent coexist with existing GDPR consent mechanisms?
6. The cold start problem — how does the system work before critical mass of sites accept MyTerms?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
