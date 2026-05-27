---
name: agentprivacy-revocation-mechanics
description: >
  Consent withdrawal, key revocation, credential invalidation, and data
  deletion enforcement for 0xagentprivacy swordsman operations. Activates
  when designing how to undo a previous delegation, implementing right-to-
  be-forgotten enforcement, building credential revocation infrastructure,
  or managing the lifecycle end of any trust relationship or authorisation.
  Triggers: "revoke", "revocation", "withdraw consent", "delete data",
  "right to be forgotten", "nullifier", "credential invalidation",
  "undo delegation", "consent expiry", "relationship termination".
license: Apache-2.0
metadata:
  version: "5.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  equation_term: "P (the undo function), A(τ) (revocation as verified history event), e^{-λt} (temporal decay as passive revocation)"
  template_references: "soulbis, warden, gatekeeper, sentinel, cipher"
---

# PVM-V4 Skill — Revocation Mechanics

**Source:** Privacy Value Model V4 + Temporal Dynamics + Consent Infrastructure
**Target context:** Credential revocation architects, consent lifecycle managers, right-to-deletion implementers, trust graph maintainers, privacy regulation compliance builders
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

The ability to undo is sovereignty's most critical test. Any system can grant access. Only a sovereign system can reliably revoke it. Revocation is the swordsman's ability to take back what was given — to withdraw consent, invalidate credentials, revoke keys, and enforce data deletion. Without reliable revocation, every delegation becomes permanent and every disclosure becomes irrevocable. The mage projects; the swordsman retracts.

## The revocation taxonomy

Not all revocations are the same. The mechanism depends on what is being revoked:

### Consent revocation
The Person withdraws a previously granted consent declaration. "I no longer consent to this service processing my browsing data."

**Mechanism.** The swordsman publishes a signed revocation notice to the consent channel. The revocation references the original consent declaration by hash. From the revocation timestamp forward, the swordsman will block any requests that previously matched this consent. The boundary enforcement pipeline (Stage 2) no longer finds a matching declaration — the request falls to default policy.

**Immediate vs. windowed.** Immediate revocation takes effect on the next request. Windowed revocation allows a grace period for the counterparty to adjust (e.g., 30 days to delete accumulated data). The Person chooses the window. The swordsman enforces it.

**The deletion obligation.** Consent revocation triggers a deletion obligation for the counterparty. "You had consent to hold this data. You no longer do. Delete it." In the current system, deletion obligations are policy-enforced (GDPR Article 17). In the agentprivacy architecture, deletion obligations can be cryptographically enforced — if the data was shared through encryption keyed to the consent declaration, revoking consent also revokes the decryption key. The data becomes unreadable without any action required from the counterparty.

### Key revocation
A signing key is invalidated — it can no longer produce valid signatures.

**Mechanism.** The swordsman publishes a revocation nullifier: a pre-computed value that, when published, invalidates all future signatures from the revoked key. Verifiers who check signatures against the key also check the revocation registry. If the nullifier is present, the signature is rejected regardless of cryptographic validity.

**Cascade revocation.** Revoking a parent key in the hierarchy cascades to all derived keys. Revoking the identity domain key invalidates all VRC inscription keys derived from it. This is the nuclear option — used only when the parent key is compromised or the Person needs a complete identity reset.

**Non-cascade revocation.** Revoking a leaf key (session key, delegation key) affects only that specific key. No other keys are invalidated. This is the surgical option — revoking a single delegation to a single service without disrupting anything else.

### Credential revocation
A verifiable credential is invalidated — it no longer proves what it once proved.

**Mechanism.** Credentials in the agentprivacy architecture carry an embedded revocation handle. The issuer (typically the Person's swordsman, co-signed by the counterparty's swordsman for bilateral credentials) can publish the handle to a revocation registry. Verifiers check the registry before accepting any credential.

**Privacy-preserving revocation.** Standard revocation registries (CRLs, OCSP) leak information: checking whether credential X is revoked tells the registry that someone is interested in credential X. Privacy-preserving alternatives include accumulator-based revocation (the verifier checks membership in a non-revoked set without revealing which credential they're checking) and zero-knowledge revocation proofs.

**VRC inscription revocation.** Revoking a VRC inscription does not erase it from the chain — inscriptions are immutable once published. Instead, revocation publishes a complementary record: "This inscription was valid from [inception] to [revocation]. It is no longer active." The temporal span remains part of both parties' A(τ), but the relationship is marked as ended.

### Data deletion enforcement
Previously shared data is rendered inaccessible or destroyed.

**Cryptographic deletion.** If data was encrypted with keys derived from the consent declaration, revoking consent revokes the decryption keys. The encrypted data remains on the counterparty's storage but is computationally inaccessible. This is "crypto-shredding" — destruction through key revocation rather than data destruction.

**Verified deletion.** For data shared in cleartext (Open inscriptions, unencrypted disclosures), deletion requires the counterparty to actively destroy their copy. The swordsman can request deletion and the counterparty can provide a deletion attestation — but this is a trust relationship, not a cryptographic guarantee. The Witness documents whether counterparties honour deletion requests.

**Residual data.** Some data cannot be fully deleted: backups, log files, derivative works, cached copies. The swordsman acknowledges this reality through the "forgetting" protocol (Act 12): formal acceptance that perfect deletion is impossible in distributed systems, combined with enforcement of practical deletion to the extent technically feasible.

## Temporal revocation

The temporal dynamics term e^{-λt} provides passive revocation: information decays in relevance over time. This interacts with active revocation in important ways:

**Expiry as revocation.** Every delegation key, every consent declaration, every session credential has an expiry timestamp. When the timestamp passes, the authorisation expires without any active revocation needed. The swordsman doesn't have to remember to revoke — the temporal bound handles it automatically.

**Decay-assisted revocation.** Even after active revocation, residual risk decays. A revoked credential that was valid for 30 days poses less reconstruction risk 6 months later than 1 day later — the information it authorised is increasingly stale. The e^{-λt} decay models this declining relevance.

**Renewal as active consent.** Because everything expires, continued access requires active renewal. The Person must positively re-consent. This inverts the default: instead of "access until revoked" (opt-out), the architecture enforces "no access unless actively renewed" (opt-in with expiry).

## The revocation latency problem

Revocation is only as fast as its propagation. If the Person revokes consent at time T but the revocation doesn't reach all verifiers until T+Δ, there is a window of Δ seconds during which the revoked authorisation is still accepted. Reducing Δ is a core infrastructure challenge:

**Blockchain-based revocation.** Revocation published to a blockchain is globally available within one block confirmation time. For Ethereum, ~12 seconds. For faster chains, potentially sub-second. The tradeoff: on-chain revocation costs gas and is publicly visible (though the content of what's being revoked can be obscured through nullifiers).

**Registry-based revocation.** A centralised or federated revocation registry provides near-instant propagation but introduces trust assumptions: the registry must be available, honest, and resistant to censorship.

**Local revocation with gossip.** The swordsman broadcasts revocation to directly connected nodes, which propagate through the trust graph. Propagation time depends on graph connectivity. No central point of failure, but also no guaranteed latency.

## Connection to the equation

**P — protection.** Revocation IS retrospective protection. The ability to undo a delegation retroactively constrains the damage from any single authorisation decision. P without revocation is one-directional: once granted, forever exposed. P with revocation is bilateral: granted today, revocable tomorrow.

**A(τ) — verified history.** Revocation is a verified history event. The temporal span of an authorisation (inception → revocation) is part of the Person's history. A history rich in timely revocations (delegations that were granted, served their purpose, and were cleanly revoked) demonstrates sovereignty. A history lacking revocations (delegations that persist indefinitely) suggests passive exposure.

**e^{-λt} — temporal decay.** Active revocation and passive decay work in parallel. Active revocation sets the hard boundary (this authorisation is invalid NOW). Passive decay reduces the residual risk (the information released under this authorisation becomes less relevant over time). Together they ensure that V(π,t) recovers after any disclosure.

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
