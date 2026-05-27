---
name: agentprivacy-recovery-rpp
description: >
  Recovery mechanisms and Relationship Proverb Protocol for 0xagentprivacy.
  Activates when discussing key loss recovery, bilateral proverb verification,
  three-attester recovery ceremonies, RPP as social recovery, or how
  relationships recover what keys cannot.
license: Apache-2.0
metadata:
  version: "4.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Key recovery designers, identity restoration architects, Zcash inscription builders, understanding-based verification systems"
  equation_term: "A(τ) (recovery through history), VRC bilateral proverbs"
  template_references: "soulbis, soulbae, cipher, gatekeeper, chronicler, pedagogue"
---

# PVM-V4 Skill — Recovery & The Relationship Proverb Protocol

**Source:** Privacy Value Model V4 + First Person Spellbook + Zcash Inscription Protocol
**Target context:** Key recovery architects, identity restoration designers, understanding-based verification builders, Zcash application developers
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

The Relationship Proverb Protocol (RPP) is the agentprivacy recovery mechanism. When keys are lost, identity is recovered through demonstrated contextual understanding — proving you understand a relationship, not proving you possess a biometric or a backup phrase. It is also the trust verification mechanism: proving you belong to a community by answering the riddle that only participants could answer.

This is one of the most original contributions of the architecture, currently compressed into a subsection of VRC identity. It deserves depth.

## The core insight

Traditional key recovery asks: "Prove you are the same person." This requires either something you have (backup keys, hardware tokens) or something you are (biometrics). Both are surveillance vectors — hardware can be seized, biometrics cannot be revoked.

RPP asks instead: "Prove you understand this relationship." The question is not identity but context. Two people who have a genuine relationship share context that no third party can replicate. This context, compressed into a bilateral proverb, becomes the recovery credential.

## The bilateral proverb

Every VRC contains a bilateral proverb: a compressed cipher derived from the relationship context between the two participants. Both parties contribute to its creation. Neither can forge it alone.

**Properties:**
- Meaningless outside the relationship. A third party reading the proverb learns nothing actionable.
- Memorable to participants. The proverb encodes shared experience in a form both parties can reconstruct.
- Verifiable by both. Either party can confirm the other's understanding by asking for the proverb or a derivative.
- Non-replayable. The proverb is bound to the specific VRC and cannot be lifted to a different context.

**Example pattern:** Alice and Bob create a VRC. Their bilateral proverb might encode: the circumstance of their first collaboration, a shared joke, a technical insight discovered together, or a mutual commitment. The specific content is private — the system only needs to verify that both parties produce the same proverb when asked independently.

## Recovery protocol

When Alice loses her keys:

1. Alice contacts Bob (or another VRC counterparty) through an out-of-band channel.
2. Bob challenges Alice with a proverb verification request — a question whose answer requires knowledge of their bilateral proverb.
3. Alice demonstrates understanding by producing the proverb or a cryptographic derivative.
4. Bob attests to Alice's identity through a recovery VRC that bridges the old and new key pair.
5. The recovery VRC preserves Alice's accumulated A(τ) — her temporal memory transfers to the new key.

**Multi-party recovery.** For higher-security contexts, recovery requires multiple counterparties. The two-of-three lock pattern (from FPS Act 8, the Ancient Rule) applies: three VRC counterparties each hold a recovery share. Any two can attest to Alice's identity, but no single counterparty can forge recovery.

**Time gate.** Recovery is not instant. A waiting period between challenge and attestation prevents adversaries from pressuring counterparties into snap decisions. The time gate gives counterparties space to verify through additional out-of-band channels.

## Proof-of-understanding vs. proof-of-identity

The RPP inverts the standard identity verification model:

| Traditional | RPP |
|------------|-----|
| Prove who you are | Prove what you understand |
| Biometric binding | Context binding |
| Cannot be revoked | Can be rotated (new proverbs) |
| Surveillance vector | Relationship vector |
| Centralised verification | Bilateral verification |
| Scales with databases | Scales with relationships |

**The deeper claim:** Understanding-based verification creates stronger trust than surveillance-based identity. A database can be hacked, a biometric can be spoofed, but genuine contextual understanding of a relationship is extremely difficult to fake. The adversary would need not just Alice's data but Alice's lived experience with Bob.

## Zcash inscriptions

The RPP extends to Zcash's blockchain through the inscription mechanism:

**Proverb inscriptions.** Bilateral proverbs inscribed in Zcash shielded memo fields. The inscription is private (only visible to transaction participants), timestamped (blockchain provides ordering), and permanent (immutable after confirmation). This creates a tamper-proof record of the proverb's existence without revealing its content.

**Proof-of-understanding attestations.** When a proverb verification occurs, the result can be inscribed as a shielded transaction. The memo field contains a hash of the proverb, the challenge, and the response. This creates a verifiable record of successful understanding-based verification.

**Recovery chain.** The sequence of VRCs, proverb inscriptions, and recovery attestations forms a chain on Zcash. This chain is private (shielded) but verifiable (any participant can confirm the chain's integrity). The chain constitutes the cryptographic proof of A(τ) — verified temporal memory inscribed on-chain.

## RPP as community gate

Beyond recovery, RPP serves as a trust verification mechanism for community membership:

**Guild entry.** "Answer the riddle to prove you belong." A guild can define a shared proverb that encodes community values, inside knowledge, or completion of a learning journey. New members demonstrate understanding by producing the proverb after walking the required path.

**Spellbook completion.** The First Person Spellbook's reconstruction prompts generate proverbs. Completing the spellbook means generating a set of proverbs that demonstrate understanding of the privacy architecture. These proverbs become credentials — proof that the seeker has internalised the concepts, not just read them.

**Anti-extraction pattern.** The RPP prevents extractive engagement. An entity that wants to access the community's knowledge must first demonstrate understanding. This cannot be faked by scraping a document or running a bot — the proverb requires genuine comprehension of relationship context.

## The compression property

Proverbs are radically compressed. A bilateral relationship that may span months or years of interaction is compressed into a single portable cipher. The compression ratios observed in spellbook narratives (70:1 to 125:1) apply to relationship proverbs as well — the entire context of a relationship compressed into a sentence or phrase.

This compression is not lossy in the way data compression is lossy. The proverb is a holographic fragment — it encodes enough structure that both parties can reconstruct the full context from the compressed form, but an outsider cannot expand it without the shared experiential key.

## Connection to equation terms

**A(τ) preservation.** RPP enables temporal memory to survive key loss. Without RPP, losing a key means losing all accumulated A(τ). With RPP, the recovery VRC bridges old and new key pairs, carrying the temporal accumulation forward.

**R(d) management.** The proverb reveals something — the existence of a relationship and the fact that understanding is shared. But it reveals far less than identity verification would. The reconstruction resistance R(d) from proverb disclosure is significantly lower than from biometric or KYC disclosure.

**T(π) continuity.** The recovery creates a special transition in the agent's trajectory — a key rotation edge. This edge should be weighted in T(π) as a high-value transition because it demonstrates resilience without compromise.

## Open problems

1. Proverb entropy requirements — how much shared context is needed for a proverb to be unforgeable?
2. Proverb aging — do proverbs become less reliable as relationships evolve and shared context fades?
3. Adversarial proverb extraction — can an adversary with access to one party's communications reconstruct the proverb?
4. Multi-cultural proverb patterns — how does the compression work across language and cultural boundaries?
5. Machine-assisted proverb generation — can agents help create proverbs that are both memorable and cryptographically strong?
6. Proverb rotation protocol — when and how should bilateral proverbs be updated without weakening recovery?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
