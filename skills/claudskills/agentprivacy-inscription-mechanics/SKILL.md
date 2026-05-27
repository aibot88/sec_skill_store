---
name: agentprivacy-inscription-mechanics
description: >
  Operational mechanics of the three inscription paths (Shadow, Guarded, Open)
  for 0xagentprivacy trust commitments. Activates when designing how bilateral
  proverbs get committed onchain, choosing inscription visibility levels,
  implementing ceremony outputs as verifiable credentials, or building the
  infrastructure that turns understanding into persistent trust records.
  Triggers: "inscription path", "Shadow inscription", "Guarded inscription",
  "Open inscription", "onchain commitment", "ceremony output",
  "bilateral proverb commitment", "trust record".
license: Apache-2.0
metadata:
  version: "5.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  equation_term: "A(τ) — inscriptions are how verified history accumulates; h(τ) — integrity through commitment"
  template_references: "priest, chronicler, cipher, gatekeeper, person"
---

# PVM-V4 Skill — Inscription Mechanics

**Source:** Privacy Value Model V4 + VRC Identity System + Ceremony Architecture
**Target context:** Trust infrastructure builders, verifiable credential implementers, onchain identity architects, ceremony designers, bilateral agreement systems
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

An inscription is the act of committing a trust relationship to persistent, verifiable storage. When two Persons complete a VRC ceremony, the output must be inscribed — written somewhere that both parties can later verify without either party being able to forge or deny.

Inscription is where the abstract (understanding, trust, bilateral promises) becomes the concrete (cryptographic commitments, verifiable credentials, onchain records). This skill covers the operational mechanics: what gets inscribed, at what visibility, through which infrastructure, and with what guarantees.

## The three inscription paths

The visibility spectrum runs from maximum privacy to maximum transparency. The choice of path is itself a signal about the relationship.

### Shadow Inscription 🌑

**Visibility:** Only the two ceremony participants know the inscription exists. No external observer can detect it.

**Mechanism:** Both parties hold a shared secret derived from their bilateral proverb. The inscription is a zero-knowledge commitment: a hash of the proverb, the timestamp, and both parties' blinded identifiers. Published to a privacy-preserving chain (Zcash shielded pool or equivalent). The commitment proves the inscription exists at a specific time without revealing who inscribed it, what was inscribed, or that any relationship exists at all.

**What gets committed:**
- `H(proverb || timestamp || blind_id_A || blind_id_B)` — the commitment hash
- ZKP that both parties contributed to the hash — proof of bilateral creation
- Nothing else. No metadata. No relationship type. No visibility to anyone.

**Use cases:** Maximum-sensitivity relationships. Whistleblower-source trust. Dissidents in hostile jurisdictions. Any relationship where the existence of the relationship itself is dangerous to reveal.

**Recovery implications:** Shadow inscriptions are hardest to recover. If both parties lose their local copies, the onchain commitment is uninterpretable. The commitment proves *something* was inscribed but cannot be decoded without both parties' keys. This is the tradeoff: maximum privacy, minimum recoverability.

**Ceremony type:** Shadow ceremonies (VRC type 1). The Priest designs the ceremony. The Cipher builds the ZKP circuit. The Gatekeeper verifies both participants are unique Persons (∃! binding) without learning their identities.

### Guarded Inscription 🛡️

**Visibility:** The inscription is visible to a defined set of verifiers beyond the two participants. The relationship type may be known, but the bilateral proverb remains private.

**Mechanism:** The commitment includes a verifiable credential structure: issuer (both parties, co-signed), holder (both parties), verifier set (defined at inscription time). The credential attests to relationship type and inception time. The bilateral proverb is committed as a separate, encrypted payload accessible only to the two parties.

**What gets committed:**
- Verifiable credential: relationship type, inception timestamp, verifier set
- `Enc(proverb, shared_key)` — encrypted proverb accessible only to participants
- Co-signatures from both parties' swordsman agents (proving bilateral consent)
- Verifier set definition (which third parties can verify the credential exists)

**Use cases:** Professional relationships where existence is not sensitive but content is. Guild memberships. Mentorship relationships. Business partnerships. Any relationship where you want others to know it exists but not what understanding underpins it.

**Recovery implications:** Guarded inscriptions are recoverable through the verifier set. If one party loses their keys, the other party plus a threshold of verifiers can attest to the relationship's existence (though the proverb itself requires both parties' keys to decrypt).

**Ceremony type:** Guarded ceremonies (VRC type 2). More structured than Shadow — both parties agree on the verifier set before inscription. The Ambassador may facilitate if the verifier set includes institutional entities.

### Open Inscription 📖

**Visibility:** The inscription is publicly visible. The relationship type, participants (by pseudonym or real identity), and inception time are all on the public record. The bilateral proverb may be published or kept private.

**Use cases:** Public trust declarations. Endorsements. Guild leadership attestations. Any relationship where public visibility IS the value — the inscription serves as a public signal of trust.

**Mechanism:** Full verifiable credential published to a public chain or credential registry. May include the bilateral proverb in cleartext (if both parties consent) as a public proof-of-understanding.

**What gets committed:**
- Full verifiable credential: participants, relationship type, inception time
- Optional: bilateral proverb in cleartext (published proof of mutual understanding)
- Co-signatures from both parties' swordsman agents
- Public verification: anyone can verify the credential's validity

**Recovery implications:** Open inscriptions are fully recoverable from the public record. The tradeoff: maximum recoverability, minimum privacy.

**Ceremony type:** Open ceremonies (VRC type 3). The most ceremonial of the three — both parties publicly declare their trust relationship. The Priest may conduct a formal ceremony with witnesses.

## The inscription lifecycle

**1. Ceremony completion.** Two Persons complete a VRC ceremony. They have exchanged context, generated a bilateral proverb, and demonstrated mutual understanding.

**2. Path selection.** Both parties agree on an inscription path. This is itself a bilateral decision — neither party can force a visibility level. If they disagree, they negotiate down to the more private option (Shadow).

**3. Commitment construction.** The technical commitment is constructed according to the selected path's mechanism. Soulbis (swordsman) signs the consent. Soulbae (mage) constructs the credential. The Cipher (if Shadow) builds the ZKP.

**4. Publication.** The commitment is published to the appropriate chain/registry. Shadow → privacy chain. Guarded → permissioned registry + encrypted payload. Open → public registry.

**5. Verification.** Both parties independently verify the inscription matches their ceremony output. This mutual verification is the final step — if either party detects a discrepancy, the inscription is contested.

**6. Accumulation.** The inscription becomes part of both parties' A(τ) — verified history. Over time, inscriptions accumulate into a trust constellation that reflects the Person's relationship network. The h(τ) integrity gate ensures only cryptographically valid inscriptions count toward A(τ).

## The bilateral proverb as inscription content

The bilateral proverb is not just authentication material — it is the inscription's semantic content. Unlike a conventional credential that attests to a fact ("Alice knows Bob"), a VRC inscription attests to understanding ("Alice and Bob share this compressed insight about their relationship").

**Proverb properties for inscription:**
- **Bilateral.** Neither party can generate it alone. It emerges from the ceremony interaction.
- **Contextual.** It encodes the specific relationship context, not a generic truth.
- **Compressible.** It fits within commitment size limits while retaining regenerative capacity.
- **Verifiable.** Both parties can independently verify it matches their ceremony experience.
- **Non-forgeable.** A third party cannot construct a valid bilateral proverb without having participated in the ceremony.

## Inscription infrastructure

**Chain selection.** Shadow inscriptions require a privacy-preserving chain (Zcash, Aztec, or equivalent with shielded transaction support). Guarded inscriptions can use any chain with verifiable credential support. Open inscriptions can use any public chain or W3C-compliant credential registry.

**Key management.** Inscriptions involve both the swordsman signing key (consent to inscribe) and the mage viewing key (ability to read inscribed content). The dual-key requirement ensures no single agent can both authorise and interpret inscriptions — maintaining the separation.

**Temporal anchoring.** Every inscription carries a cryptographic timestamp (block height on the publication chain). This anchoring prevents backdating — you cannot inscribe a trust relationship in the past. The temporal anchor feeds directly into A(τ): verified history that accumulates forward in time.

**Revocation.** Inscriptions can be revoked by either party through their swordsman agent. Revocation publishes a nullifier (for Shadow: a ZKP that the commitment is revoked without revealing which commitment). Revocation does not delete — the inscription existed, and its temporal span (inception to revocation) remains part of both parties' A(τ).

## Connection to the equation

**A(τ) — verified history.** Inscriptions ARE the mechanism by which A(τ) accumulates. Each inscription adds a verified data point to the Person's trust history. The temporal dynamics term e^{-λt} · (1 + A(τ)) means that recent inscriptions contribute more than distant ones, but all inscriptions compound the Person's verified history.

**h(τ) — integrity fraction.** The h(τ) gate ensures only cryptographically valid inscriptions count. An inscription that fails verification (corrupted commitment, invalid ZKP, missing co-signature) is excluded from A(τ). The integrity fraction is the proportion of inscriptions that pass verification — a measure of the Person's trust infrastructure quality.

**C — verifiability.** Each inscription is a verifiable claim. The C term in V(π,t) measures the system's verifiability capacity. More inscription infrastructure (more chains supported, more credential formats, more verification methods) increases C.

**The visibility spectrum as privacy signal.** The choice of inscription path reveals the relationship's sensitivity level. A Person whose constellation is all Shadow inscriptions operates in maximum privacy. A Person with mixed paths demonstrates nuanced judgment about what to reveal and what to protect. The spectrum itself is a privacy-preserving metadata — it reveals the distribution of sensitivity levels without revealing any specific relationship.

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
