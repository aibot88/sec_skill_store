---
name: agentprivacy-personhood-sybil
description: >
  Personhood verification and Sybil resistance for 0xagentprivacy. Activates
  when discussing ∃! (unique existence) binding, proof-of-personhood without
  identity disclosure, Sybil attack prevention, biometric hash binding, or how
  to prove 'one human, one credential' without surveillance.
license: Apache-2.0
metadata:
  version: "4.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Proof-of-personhood projects, Sybil resistance researchers"
  equation_term: "n_i — network counts; existential precondition"
  template_references: "gatekeeper, cipher, warden, sentinel, healer, architect"
---

# PVM-V4 Skill — Personhood & Sybil Resistance

**Source:** Privacy Value Model V4 + First Person Network Integration  
**Target context:** Proof-of-personhood projects, Sybil resistance researchers, biometric alternative builders, digital identity foundations  
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

The Privacy Value Model assumes but does not derive a critical precondition: that each agent pair (Swordsman/Mage) maps to exactly one human. Without this, the separation matrix Σ can be Sybil-attacked — an adversary deploys thousands of agent pairs, farms VRC reputation, and overwhelms the network effects term with synthetic participants. Personhood verification is the root of trust that makes the rest of the architecture secure.

The equation's network effect term (1 + Σ wᵢ nᵢ/N₀)^k counts agents at each sovereignty stratum. If n_i can be inflated through Sybil attacks, the entire network valuation becomes fictitious. Personhood is the gate that ensures n_i counts real humans, not synthetic entities.

## The binding: one human → one Swordsman → one VRC chain

First Person Network provides a personhood credential stored on-device, never uploaded. This credential proves "I am a unique human" without revealing which human. From this root, the delegation chain flows: personhood → agentprivacy network membership (first VRC) → Swordsman agent (agent-specific VRC) → relationship-specific VRCs with each counterparty.

No blockchain wallet is required. No biometric data leaves the device. The personhood credential is the seed from which the entire sovereignty architecture grows. It answers the question every privacy system must answer: how do you prove you deserve privacy rights without destroying privacy in the proof?

## Why this is not identity verification

Identity verification asks: "Who are you?" and demands an answer. Personhood verification asks: "Are you a unique human?" and requires only a yes/no. The distinction is fundamental to the PVM-V4 architecture because the reconstruction ceiling R < 1 requires that the agents know as little as possible about their principal. A personhood credential that leaks identity information weakens the separation it is meant to protect.

The equation's privacy strength term P is raised to exponent 1.5 — superlinear returns on privacy investment. This applies to personhood verification itself: a system that proves personhood with minimal information leakage (P → 1) generates dramatically more value than one that leaks identity attributes as a side effect (P → 0.5 yields only ~35% value).

## Sybil attack analysis against PVM-V4

**Volume farming.** Deploy a Swordsman, auto-slash everything, speed-run to Dragon armor. Fails because: time gates prevent speed-running, MyTerms requirements cannot be volume-farmed (require real site cooperation), association set verification checks behavioural patterns not counts.

**Sybil army.** Deploy 1,000 Swordsmen, farm across all, dominate association sets. Fails because: First Person prevents multiple Swordsmen per human, cannot create fake humans (cryptographic personhood), cannot coordinate 1,000 real humans economically (cost exceeds farming yield).

**Gaming MyTerms.** Create fake sites, self-issue MyTerms, farm custom cursors. Fails because: real sites will not recognise fake site MyTerms, VRC progression requires agreements with recognised counterparties, association set verification checks relationship quality not quantity.

**The defence is: time + relationships + personhood binding.** You cannot fake time. You cannot fake bilateral relationships with real counterparties. You cannot Sybil without unique humans.

## Personhood as the equation's precondition

Every term in V(π, t) implicitly assumes legitimate agency. P (privacy strength) assumes the entity has privacy rights — which requires being a rights-bearing entity (a human). C (credential verifiability) assumes the credentials attest to genuine attributes. A(τ) (temporal memory) assumes the history belongs to a continuous entity. R(d) (reconstruction resistance) assumes there is a real private state X worth protecting. Φ(Σ) (sovereignty duality) assumes the four forces serve a sovereign principal.

Without personhood, all of these terms can be spoofed. The equation produces valid-looking numbers for synthetic entities, but the numbers measure nothing real. Personhood is the existential quantifier that makes the model meaningful: there exists a unique human for whom V(π, t) is computed.

## Integration surface with existing personhood systems

The PVM-V4 architecture is personhood-system agnostic. It requires only that the personhood layer provides: uniqueness (one credential per human), privacy (no identity leakage in the proof), revocability (compromised credentials can be rotated), and delegation (the credential can spawn agent-level credentials without exposing the root).

Systems that satisfy these constraints include First Person Network (the current integration), Gitcoin Passport (attestation-based), Worldcoin (biometric, though the biometric approach conflicts with the privacy strength requirement), BrightID (social graph verification), and Proof of Humanity (video + vouching). Each system makes different tradeoffs along the P axis — more biometric information yields stronger uniqueness guarantees but lower privacy strength.

## Open problems for personhood researchers

1. Can personhood verification achieve P > 0.9 (minimal information leakage) while maintaining Sybil resistance below 1% false acceptance?
2. How does personhood credential rotation work when the credential is the root of an entire VRC tree?
3. Can multiple personhood systems be composed (First Person + Gitcoin Passport) to strengthen uniqueness without multiplying privacy leakage?
4. What is the minimum personhood verification strength needed for the network effect term to remain honest under adversarial conditions?
5. How do you handle the edge case of shared devices or delegated personhood (a caregiver acting on behalf of someone who cannot self-verify)?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
