---
name: agentprivacy-nullifier-design
description: >
  Nullifier construction, deployment, and verification for 0xagentprivacy
  privacy-preserving invalidation. Activates when designing double-spend
  prevention, privacy-preserving revocation, unlinkable credential usage,
  or any operation where an action must be provably performed exactly once
  without revealing the actor's identity.
  Triggers: "nullifier", "double-spend", "single-use proof",
  "privacy-preserving revocation", "unlinkability", "nullifier set",
  "nullifier tree", "spent set", "serial number".
license: Apache-2.0
metadata:
  version: "5.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  equation_term: "P × C — nullifiers enforce single-use without revealing identity"
  template_references: "soulbis, cipher, gatekeeper, sentinel, sith"
---

# PVM-V4 Skill — Nullifier Design

**Source:** Privacy Value Model V4 + Zero Knowledge Spellbook (Tales 5-7) + Zcash Nullifier Architecture
**Target context:** ZKP circuit designers, privacy protocol engineers, credential system architects, voting system builders, token system designers
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

A nullifier is a deterministic, unique value derived from a secret that, when published, marks a specific action as "done" without revealing who did it or what it was done to. It is the cryptographic answer to a fundamental tension: how do you prevent someone from doing something twice (double-spending, double-voting, double-claiming) while preserving their anonymity?

Without nullifiers, privacy systems face a dilemma: either track who did what (destroying privacy) or allow repeated actions (destroying integrity). Nullifiers resolve the dilemma by tracking THAT something was done without tracking WHO did it.

## The nullifier construction

A nullifier is computed as:

```
nullifier = H(secret || action_context)
```

Where `H` is a collision-resistant hash function, `secret` is known only to the actor, and `action_context` identifies the specific action being nullified (a transaction, a vote, a credential usage, a revocation).

**Properties:**
- **Deterministic.** The same secret + context always produces the same nullifier. This prevents double-action: trying to act twice produces the same nullifier, which the system detects as already published.
- **Unlinkable.** Different action contexts produce different nullifiers from the same secret. Observing two nullifiers reveals nothing about whether they came from the same actor.
- **Irreversible.** The nullifier cannot be traced back to the secret (hash preimage resistance). Publishing the nullifier does not expose the actor.
- **Verifiable.** A zero-knowledge proof accompanies the nullifier, proving it was correctly derived from a valid secret and a legitimate action context, without revealing either.

## Nullifier applications across the architecture

### Transaction nullifiers (Zcash model)
Each shielded note has a commitment (published when created) and a nullifier (published when spent). The nullifier set is a public record of all spent notes. To verify a transaction: check that the nullifier is not in the spent set (no double-spend) and verify the ZKP (valid derivation from a real note).

**In the architecture.** Privacy Pool contributions use transaction nullifiers to prevent the same observation from being counted twice while keeping the contributor anonymous.

### Credential nullifiers (single-use proofs)
A credential can be used exactly once per context. The nullifier is derived from the credential secret and the usage context (e.g., "vote in election 2026-Q1"). Using the credential in the same context twice produces the same nullifier — detected and rejected.

**In the architecture.** VRC ceremonies generate bilateral credentials. Each credential's nullifier ensures it is verified exactly once per verification context. A health provider verifying insurance eligibility gets one verification — not a tracking stream.

### Revocation nullifiers (privacy-preserving cancellation)
Pre-computed at key/credential creation time. Publishing the revocation nullifier invalidates the key/credential without revealing which key/credential was revoked (when the nullifier set is large enough to provide anonymity).

**In the architecture.** Every delegation key created through key_ceremony comes with a pre-computed revocation nullifier. If the Person needs emergency revocation, publishing the nullifier is instantaneous — no need to identify the key publicly.

### Governance nullifiers (anonymous voting)
One person, one vote, zero linkage. The nullifier is derived from the voter's identity secret and the election identifier. Voting twice in the same election produces a duplicate nullifier. But the voter's identity is never connected to their vote.

**In the architecture.** Guild governance uses nullifier-based voting to ensure fair participation without surveillance of voting patterns. The Assessor can verify quorum and outcome without knowing how any individual voted.

## Nullifier set management

The nullifier set (the record of all published nullifiers) is the system's memory of what has been done. Managing it is a critical infrastructure concern:

**Storage.** The nullifier set grows monotonically — nullifiers are added, never removed. For high-volume systems (millions of transactions), the set becomes large. Efficient data structures (Merkle trees, sparse Merkle trees, accumulator-based sets) keep lookup time logarithmic.

**Availability.** Every verifier must access the current nullifier set to check for duplicates. If the set is unavailable, verification stalls. Decentralised storage (blockchain state) provides availability guarantees but at cost. Centralised registries are faster but introduce trust assumptions.

**Privacy of the set itself.** The nullifier set is public by necessity (everyone needs to check it). But the set's growth pattern can leak information: a burst of nullifiers suggests a burst of activity. Constant-rate nullifier publication (dummy nullifiers filling quiet periods) mitigates timing analysis.

## Nullifier circuit design

The zero-knowledge circuit that accompanies a nullifier must prove:

1. **Knowledge of secret.** The prover knows the secret from which the nullifier was derived (without revealing the secret).
2. **Correct derivation.** The nullifier was computed as H(secret || context) — not arbitrarily chosen.
3. **Membership.** The secret corresponds to a valid commitment in the system (the prover actually has the credential/note/key they're nullifying).
4. **Freshness.** The action context is current (prevents replaying old proofs in new contexts).

**Circuit complexity.** Nullifier circuits are relatively simple compared to general ZKP circuits. The core operation is a hash function inside a SNARK/STARK. The main design choice is the hash function: Pedersen (efficient in SNARKs), Poseidon (designed for arithmetic circuits), MiMC (minimal constraints). Each has different performance profiles inside different proof systems.

**Composability.** Nullifier proofs compose with other proofs. A transaction proof that includes a nullifier also proves the transaction's validity (correct amounts, valid sender). A voting proof that includes a nullifier also proves eligibility (registered voter, correct election). The nullifier is one component of a larger proof — not a standalone operation.

## Nullifier anti-patterns

**Predictable nullifiers.** If an adversary can predict a nullifier before it's published, they can pre-emptively publish it (denial of service). Mitigation: include sufficient entropy in the secret component.

**Correlated nullifiers.** If nullifiers from the same actor are correlated (e.g., sequential in some space), publishing multiple nullifiers deanonymises the actor. Mitigation: use independent randomness per action context, not sequential derivation.

**Nullifier reuse across contexts.** Using the same nullifier scheme across different applications can create cross-application linkability. If the same secret produces nullifiers in both a voting system and a payment system, and the nullifier sets are publicly compared, cross-context linking becomes possible. Mitigation: domain separation — include a unique application identifier in the action context.

**Insufficient set size.** A nullifier set with 3 entries provides no meaningful anonymity — an adversary can enumerate. Minimum set sizes depend on the threat model, but k-anonymity principles apply: the set should be large enough that any individual nullifier is indistinguishable from at least k-1 others.

## Connection to the equation

**P — protection.** Nullifiers enable protection without surveillance. The system enforces rules (no double-spend, no double-vote) without knowing who is acting. This is P in its purest form: the rule is enforced, the actor is invisible.

**C — verifiability.** Every nullifier is accompanied by a zero-knowledge proof. The verifier can check correctness without learning anything beyond the fact of correct derivation. This is C: verifiable computation that reveals nothing unnecessary.

**R(d) — reconstruction.** Nullifiers are designed to be unlinkable. Two nullifiers from the same actor reveal nothing about their shared origin. This directly maintains R<1 for the actions protected by nullifiers — even an adversary with the complete nullifier set cannot reconstruct which actor produced which subset.

**h(τ) — integrity.** The nullifier set IS the integrity record. A correctly maintained set (no duplicates accepted, no valid nullifiers rejected) means h(τ) = 1 for nullifier-protected operations. Corruption of the set (accepting duplicates, censoring valid submissions) directly reduces h(τ).

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
