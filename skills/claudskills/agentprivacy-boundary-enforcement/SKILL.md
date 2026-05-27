---
name: agentprivacy-boundary-enforcement
description: >
  Real-time access control decision engine for 0xagentprivacy swordsman
  agents. Activates when evaluating incoming data requests against consent
  preferences, designing allow/block/transform rule sets, implementing
  the swordsman's moment-to-moment operational logic, or building the
  enforcement layer that turns consent declarations into cryptographic actions.
  Triggers: "boundary", "access decision", "allow block", "consent enforcement",
  "data request evaluation", "rules engine", "policy enforcement",
  "request filtering", "permission check".
license: Apache-2.0
metadata:
  version: "5.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  equation_term: "P — boundary enforcement IS protection in real-time operation"
  template_references: "soulbis, warden, gatekeeper, sentinel, archer"
---

# PVM-V4 Skill — Boundary Enforcement

**Source:** Privacy Value Model V4 + Consent Infrastructure (IEEE 7012) + Dual-Agent Separation
**Target context:** Access control designers, privacy middleware builders, consent enforcement implementers, browser extension architects, API gateway designers
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

Every second, the swordsman makes decisions: this request gets through, that one gets blocked, this other one gets transformed before passing. Boundary enforcement is the operational core of the P term — not the mathematics of protection (that's crypto_zkp), not the progressive tiers (that's armor_progression), not the browser-specific implementation (that's swordsman_browser), but the decision logic itself.

A data request arrives. The swordsman evaluates: Who is asking? What are they asking for? Is there valid consent? Does this exceed the minimum disclosure set? What's the current threat level? The answer — allow, block, or transform — must be instantaneous, consistent, auditable, and cryptographically enforced.

## The decision pipeline

Every incoming request passes through a six-stage pipeline:

**Stage 1 — Authentication.** Who is the requestor? Verify identity against the trust graph. Unknown requestors are not automatically blocked — they enter the evaluation pipeline with zero trust score. Known requestors enter with their accumulated trust weight from A(τ).

**Stage 2 — Consent lookup.** Does the Person have an active consent declaration covering this request? Consent declarations are structured (IEEE 7012 bilateral terms): what data, for what purpose, for how long, with what restrictions. The swordsman matches the request against active declarations. No matching declaration → proceed to default policy.

**Stage 3 — Scope check.** Even with valid consent, does this specific request fit within the declared scope? A consent to share "prescription status" does not authorise sharing "complete medical history." The swordsman evaluates request scope against declaration scope. Over-broad requests are narrowed, not blocked — the swordsman transforms the request to match the consent scope.

**Stage 4 — Minimum disclosure.** What is the least information that satisfies this request? The swordsman consults the mage (Soulbae) for disclosure set calculation — the mage can see the data and determine the minimum. But the swordsman makes the authorisation decision. This is the dual-agent handshake in real-time: mage recommends, swordsman decides.

**Stage 5 — Threat assessment.** What is the current threat environment? Elevated threat (active adversary detected by Sentinel, recent breach documented by Witness, Sith red team warning) tightens all boundaries. Normal threat applies standard policy. Reduced threat (trusted environment, verified counterparty, established relationship) may relax specific boundaries within consent scope.

**Stage 6 — Execution.** The decision is executed cryptographically. Allow: swordsman signs the authorisation, data flows through the mage's disclosure channel. Block: no signature, request returns empty or with a privacy-preserving denial (no information about why the request was blocked). Transform: request is modified, swordsman signs the transformed version, modified data flows.

## Decision types

**Allow.** The request matches active consent, fits within scope, meets minimum disclosure, and the threat environment is acceptable. The swordsman signs. The signature is the authorisation — without it, the mage cannot release data. The allow decision is logged (encrypted, accessible only to the Person) for audit.

**Block.** The request fails any pipeline stage. No consent exists, scope exceeds declaration, threat level too high, or requestor authentication fails. The swordsman returns nothing — not an error message (which leaks information about what exists), not a redirect (which leaks the swordsman's address), nothing. Silence is the swordsman's block.

**Transform.** The request is valid but over-broad. The swordsman narrows it to the minimum disclosure set. "Give me your medical history" transforms to "Here is proof of insurance eligibility." The original request is never fulfilled — the transformed version satisfies the legitimate need while protecting everything else. Transform is where the Archer's precision meets the Warden's enforcement.

## Policy layers

Boundary enforcement operates across multiple policy layers, evaluated in order:

**Layer 0 — Immutable rules.** Hardcoded in the swordsman agent. Never overridable by the Person, the mage, or any external party. Examples: never release the signing key material, never combine signing and viewing keys in a single operation, never authorise a request that would reduce R below the reconstruction ceiling.

**Layer 1 — Person's standing policy.** The Person's default preferences. "Block all third-party data sharing unless I've explicitly consented." "Transform all age verification requests to ZKP proofs." "Allow all requests from entities in my trust graph with reputation score above threshold." Standing policy is configurable by the Person and persists across sessions.

**Layer 2 — Contextual policy.** Adjustments based on current context. Higher protection in public WiFi. Lower friction for verified healthcare providers during a medical appointment. Contextual policy is suggested by the mage (who can observe context) and approved by the swordsman (who enforces it).

**Layer 3 — Consent declarations.** Specific bilateral agreements (IEEE 7012 terms) with specific counterparties. These override standing policy for the declared scope — a consent to share prescription data with a pharmacy overrides the general "block third-party sharing" rule for that specific data category with that specific counterparty.

**Layer 4 — Emergency overrides.** Pre-authorised emergency disclosures. "If I'm unconscious in a hospital, release my blood type and allergies to the treating physician." Emergency overrides are the most carefully designed policies — the Person defines them in advance, the swordsman stores them securely, and they activate only under specified conditions.

## The consent-enforcement gap

Current systems have a gap between what consent is declared and what is actually enforced. Cookie consent banners are the canonical failure: "I consent to necessary cookies only" → the site loads 47 tracking scripts anyway. The consent was declared but never enforced.

Boundary enforcement closes this gap by making consent cryptographically binding. The swordsman's signature IS the enforcement. No signature, no data flow. A site that ignores the consent declaration gets nothing — not because of a policy promise but because the cryptographic channel doesn't open without the swordsman's key.

This is the MyTerms (IEEE 7012) integration: bilateral privacy agreements enforced by the Warden's cookie-slashing capability at the browser level, backed by the swordsman's signing authority at the cryptographic level.

## Audit trail

Every decision is logged in an encrypted audit trail accessible only to the Person:

- Timestamp of request
- Requestor identity (or "unknown")
- Request type and scope
- Decision (allow/block/transform)
- Policy layer that determined the decision
- Consent declaration referenced (if any)
- Threat level at decision time

The audit trail enables the Person to review their swordsman's behaviour — "show me every request that was blocked last week" or "show me every transform decision involving health data." The Witness can access the audit trail (with the Person's consent) to document patterns — systematic over-requesting by a specific service, for example.

## Connection to the equation

**P — protection.** Boundary enforcement is P in its most operational form. The P^1.5 superlinear return means that consistent, well-calibrated enforcement compounds: each correctly blocked request strengthens the overall protection posture. Inconsistent enforcement (blocking sometimes, allowing others for the same request type) undermines P and reduces V(π,t).

**C — verifiability.** Every enforcement decision is cryptographically verifiable. The swordsman's signature (or absence of signature) is proof of the decision. This verifiability — C in the equation — is what distinguishes enforcement from policy: enforcement is provable.

**R(d) — reconstruction.** Each allow decision contributes to potential reconstruction. The swordsman's job is to ensure that the cumulative effect of all allow decisions keeps R(d) < 1. The minimum disclosure principle at Stage 4 is the mechanism: each allow releases the least possible information, keeping total leakage bounded.

## BRAID verification loops as inference-layer boundary enforcement

BRAID's terminal verification loops (arXiv:2512.15959) encode the same pattern as Swordsman boundary checking:

```
[Generate output] → [Check: R(d) disclosure within bounds?]
  -- pass --> [Deliver]
  -- fail --> [Feedback edge to revision] → [Re-check]
```

This "System 2 thinking emulation" is the Swordsman as boundary verifier at the inference layer. Before any output leaves the dual-agent system, verify against privacy boundaries using pre-validated verification nodes.

For Swordsman deployment: generate BRAID boundary-checking graphs once (expensive), cache as holons, execute via nano-tier models for every access request (cheap). Real-time boundary enforcement becomes economically viable at millions of checks per day.

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
