---
name: agentprivacy-vrc-identity
description: >
  Verifiable Relationship Credential (VRC) identity system for
  0xagentprivacy. Activates when discussing A(τ) bilateral trust, VRC
  issuance/verification/revocation, Relationship Proverb Protocol (RPP), trust
  flow mechanics, ceremony-to-credential pipeline, or how identity is
  expressed through relationships rather than attributes.
license: Apache-2.0
metadata:
  version: "4.0"
  category: "privacy_layer"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Decentralised identity builders, KERI/DID implementers, IIW community, trust framework architects"
  equation_term: "A(τ) — temporal memory; h(τ) — integrity fraction"
  template_references: "all"
---

# PVM-V4 Skill — Verifiable Relationship Credentials (VRCs)

**Source:** Privacy Value Model V4 + 0xagentprivacy VRC Protocol  
**Target context:** Decentralised identity builders, KERI/DID implementers, IIW community, verifiable credential toolchains, trust framework architects  
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

Verifiable Relationship Credentials are the temporal memory term A(τ) made concrete. They are cryptographic proofs of bilateral trust — not identity documents but relationship documents. A VRC does not say "Alice is trustworthy." It says "Alice and Bob have a demonstrated relationship of this quality, attested by both parties, verifiable by anyone, forgeable by neither."

The VRC is the integrity fraction h(τ) in the equation. Without it, temporal memory contributes nothing — unverified claims produce A(τ) = 0 regardless of history length. With it, every sovereignty transition accumulates value that compounds logarithmically.

## How VRCs work

**Creation (Promise Bundle).** Two First Persons create a VRC together. Neither can forge alone. Both must sign. The credential encodes: Alice's commitment, Bob's commitment, a bilateral proverb derived from shared context, and the cost signal (0.01 ZEC each — a ceremony, not a transaction). This maps directly to Promise Theory: the VRC is a bundle of mutual promises that can be verified but not forged.

**The bilateral proverb.** Each VRC contains a compressed cipher derived from the relationship context. This proverb is meaningless outside the relationship — it requires the shared decoder that only the two parties possess. The proverb serves as both a trust signal (proof that the relationship has enough depth to generate shared meaning) and a recovery mechanism (proof-of-personhood through demonstrated understanding rather than biometrics or personal questions).

**Progressive accumulation.** VRCs are not binary (trusted/untrusted). They accumulate through sustained interaction. The temporal memory function A(τ) = α · ln(1+|τ|) · h(τ) means early VRCs contribute the most marginal value (logarithmic growth), creating strong incentives for establishing trust early. Later VRCs add value but at diminishing rates — the thousandth VRC matters less than the tenth.

**Recovery.** If Alice loses her keys, Bob can help verify Alice's identity using their bilateral proverb. Alice claims identity. Bob asks for the proverb. Alice derives the correct proverb from relationship context. Bob verifies. Recovery proceeds (with multiple VRCs providing redundancy). No biometrics. No personal questions. Just bilateral promise verification — the Relationship Proverb Protocol (RPP) as both security mechanism and proof-of-personhood.

## VRC properties as equation terms

**Bilateral (Σ matrix).** VRCs require two parties maintaining separation. Alice's Swordsman and Bob's Swordsman each attest to their respective boundary conditions. Alice's Mage and Bob's Mage each attest to their delegation conditions. The cross-attestation creates entries in the separation matrix Σ — the quality of the VRC depends on the conditional independence of the attesting agents.

**Context-specific (edge value).** Each VRC maps to a specific sovereignty transition. The proverb maps to shared context. This means VRCs are not fungible — they carry the specific trajectory T(π) of the relationship, not a generic trust score. An agent's VRC portfolio is a graph of demonstrated sovereignty transitions, not a number.

**Scoped (reconstruction resistance).** A VRC reveals only what the relationship requires. The proverb is meaningless outside the bilateral context. The underlying data that generated the proverb remains private. This enforces the reconstruction ceiling R < 1 at the credential level — no single VRC, and no collection of VRCs from different relationships, allows full behavioural reconstruction.

**Recoverable (temporal memory).** If forgotten, the proverb can be re-derived because it is based on relationship context rather than arbitrary secrets. This is the temporal memory's deepest property: verified history is not a brittle key but a robust pattern that can be regenerated from sufficient shared context.

## Trust flow architecture

The trust chain for any First Person entering the 0xagentprivacy network:

First Person Network (personhood credential — stored on-device, never uploaded) → agentprivacy (first VRC — you're in the network) → Swordsman (agent-specific VRC — you wield the blade) → site-specific VRCs (relationship credentials with each MyTerms counterparty).

No traditional blockchain wallet required at any step. The first personhood credential sits locally and spawns the agent hierarchy through delegation, not key derivation.

## Integration with existing identity standards

**DIDs.** Each First Person has a DID. Each Swordsman and Mage has a derived DID. VRCs are verifiable credentials in the W3C sense but with the bilateral constraint — they require two DID signatures, not one issuer and one holder.

**KERI (Key Event Receipt Infrastructure).** VRC key rotation and recovery map to KERI's event-driven key management. The bilateral proverb serves as the semantic layer over KERI's cryptographic layer — human-meaningful recovery over machine-verifiable key events.

**Trust Over IP.** VRCs operate at ToIP Layer 3 (credential exchange) and Layer 4 (governance). The progressive trust tiers (Traveler → Contributor → Author → Mentor → Fellow) map to the armor progression, with each tier requiring demonstrated VRC depth.

## Open problems for identity builders

1. What is the minimum VRC density needed for robust key recovery across a First Person's relationship network?
2. How do VRC proverbs scale — does proverb quality degrade when a person maintains hundreds of bilateral relationships?
3. Can VRCs interoperate across different personhood verification systems (First Person Network, Gitcoin Passport, WorldCoin)?
4. What happens to VRCs when one party's agent is compromised — how does revocation propagate without revealing the relationship graph?
5. Can the bilateral proverb mechanism be formalised as a zero-knowledge proof of shared context?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
