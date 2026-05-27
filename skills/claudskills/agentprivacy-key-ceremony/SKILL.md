---
name: agentprivacy-key-ceremony
description: >
  Key generation, rotation, delegation, revocation, and hardware binding
  for the 0xagentprivacy dual-agent architecture. Activates when designing
  key hierarchies, implementing signing key operations, managing the
  swordsman's core material, or building ceremonies around key lifecycle
  events. The swordsman's most fundamental operational skill.
  Triggers: "key generation", "key rotation", "key ceremony", "signing key",
  "key hierarchy", "hardware binding", "key delegation", "master key",
  "derivation path", "key material".
license: Apache-2.0
metadata:
  version: "5.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  equation_term: "P — the signing key IS the swordsman; key lifecycle IS protection lifecycle"
  template_references: "soulbis, cipher, gatekeeper, sentinel, person"
---

# PVM-V4 Skill — Key Ceremony

**Source:** Privacy Value Model V4 + Dual-Agent Separation + VRC Identity System
**Target context:** Key management architects, wallet designers, HSM implementers, ceremony coordinators, identity infrastructure builders
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

The signing key is the swordsman made material. Without the key, there is no boundary enforcement, no consent authorisation, no protection. Every operation Soulbis performs — blocking a data request, signing a VRC inscription, authorising a selective disclosure — begins with a cryptographic signature from the signing key.

Key ceremony covers the full lifecycle: how signing keys are born, how they grow (derivation hierarchies), how they delegate (sub-keys for specific operations), how they rotate (planned replacement), how they revoke (emergency invalidation), and how they die (graceful retirement). Each lifecycle event is a ceremony — a structured, witnessed, verifiable transition — not a background process.

## The dual-key architecture

The 0xagentprivacy separation is enforced through two key types that cannot be combined:

**Signing key (swordsman / Soulbis).** Authorises operations. Signs consent, approves disclosures, validates inscriptions. The signing key can approve a data release but CANNOT read the data being released. This is the fundamental separation: the swordsman signs blind.

**Viewing key (mage / Soulbae).** Observes and interprets. Reads encrypted data, matches disclosure requests to minimum sets, processes Intel Pool contributions. The viewing key can see everything but CANNOT authorise anything. The mage observes without touching.

**The gap between them is sovereignty.** No single key — no single agent — can both see the data AND approve its release. This gap is where human control persists. The Person bridges the gap through bilateral consent: telling the swordsman what to sign, telling the mage what to interpret.

## Key generation ceremony

Key generation is not `openssl genrsa`. It is the first ceremony in a Person's sovereignty journey — the moment the dual agents spawn.

**Entropy requirements.** Minimum 256 bits of entropy from a hardware random number generator. Software PRNGs are insufficient — they are deterministic from their seed, and seed compromise means total key compromise. The entropy source must be verifiable (attestable hardware, auditable process).

**Generation environment.** Air-gapped device or hardware security module (HSM). No network connection during generation. No persistent storage of intermediate state. The generation environment is destroyed after the ceremony — the key exists only in its final storage location.

**Witness structure.** Key generation can be self-witnessed (solo ceremony) or socially witnessed (participants attest they observed a valid generation process without seeing the key material). Social witnessing creates a VRC inscription: "I witnessed this Person's key generation ceremony. The process was valid."

**Split generation.** For high-value keys, Shamir's Secret Sharing or multi-party computation generates the key such that no single party ever holds the complete key material. Threshold reconstruction (k-of-n) requires k shareholders to cooperate for any signing operation. This distributes trust across the Person's social graph.

## Key hierarchy

A single master key is fragile. The architecture uses hierarchical deterministic (HD) derivation to create a tree of purpose-specific sub-keys:

**Level 0 — Master key.** Never used directly for operations. Cold storage only. Generates all lower levels. If compromised, everything below is compromised — hence the extreme generation ceremony.

**Level 1 — Domain keys.** One per operational domain. Identity domain (VRC inscriptions). Consent domain (data authorisations). Governance domain (voting, delegation). Economic domain (transactions, guild contributions). Each domain key can be rotated independently without affecting other domains.

**Level 2 — Session keys.** Ephemeral keys derived for specific interactions. A session key for this browser session. A session key for this VRC ceremony. A session key for this Privacy Pool contribution. Session keys expire automatically. Their compromise exposes only the single session.

**Level 3 — Delegation keys.** Keys issued to authorised agents for bounded operations. "This key can sign data authorisations for my health provider, for the next 30 days, for prescription verification only." Delegation keys are the mechanism by which the Person delegates without surrendering — each delegation key is scoped, temporal, and revocable.

## Key rotation ceremony

Keys age. Cryptographic advances, accumulating usage metadata, and the passage of time all reduce key security. Rotation is planned replacement — not emergency, not crisis, but scheduled maintenance.

**Rotation cadence.** Master key: never rotated (too risky; replaced only if compromised). Domain keys: annual rotation recommended, enforced by credential expiry. Session keys: per-session (automatic). Delegation keys: at scope expiry (automatic).

**Rotation process.** New key generated with full ceremony. New key signs a rotation declaration: "I am the successor to [old key hash]." Old key co-signs the declaration: "I confirm [new key] as my successor." Both signatures published as a verifiable credential. The old key enters a grace period (accepts no new operations, completes pending operations) then retires.

**Continuity of identity.** Key rotation must NOT break the Person's identity chain. A(τ) — verified history — spans across rotations. The rotation declaration creates a cryptographic link: old key → new key. Any verifier can trace the chain from current key back through all rotations to the genesis ceremony. The Person's identity is the chain, not any single key.

## Key delegation protocol

The swordsman delegates cautiously. Each delegation key is bound by four constraints:

**Scope.** What operations can this key authorise? "Health data disclosure to providers" — not "all data disclosure." Scope is encoded in the delegation credential and enforced at verification time.

**Temporal bound.** When does this delegation expire? Every delegation key has an expiry timestamp. No perpetual delegations. The Person must actively renew — consent is ongoing, not one-time.

**Audience.** Who can verify signatures from this key? A delegation key for health providers is verifiable only by health providers. Audience restriction prevents cross-domain linkability.

**Revocation handle.** Every delegation key comes with a pre-computed revocation nullifier. If the Person needs to revoke the delegation before expiry, publishing the nullifier invalidates all future signatures from that key. The revocation can be instantaneous — no waiting for expiry.

## Emergency key procedures

**Suspected compromise.** If the Person suspects any key is compromised: immediately publish revocation for the suspected key, rotate all keys derived from the same parent, notify all counterparties through the VRC trust graph, invoke the Witness to document the incident.

**Confirmed compromise.** If compromise is confirmed: execute full key tree rotation from master key, revoke ALL delegation keys (scorched earth), rebuild trust graph with new key material through fresh VRC ceremonies, update all inscriptions with new key references.

**Key loss (not compromise).** The key is gone but not stolen. This triggers the recovery_rpp protocol: bilateral proverb verification through the Person's trust graph to recover identity continuity. The lost key is revoked. A new key is generated. The identity chain is restored through social attestation rather than cryptographic derivation.

## Hardware binding

For maximum security, signing keys are bound to hardware security modules that enforce:

**Non-exportability.** The key material never leaves the hardware boundary. Signing operations happen inside the HSM. The HSM outputs signatures, never keys.

**Physical attestation.** The HSM can prove (via remote attestation) that the signing key is hardware-bound. This proof is published as part of the Person's trust profile — counterparties can verify that signatures come from tamper-resistant hardware, not software.

**Biometric gating (optional).** The HSM requires a biometric (fingerprint, face) to unlock signing operations. This creates a physical-presence requirement — even if the HSM is stolen, signing requires the Person's body. Note: biometric data is processed locally within the HSM. It is never transmitted, never stored remotely, never available to the mage agent.

## Connection to the equation

**P — protection.** The signing key IS P. Every term in the equation that involves protection (P^1.5, Φ(Σ) separation, R<1 enforcement) ultimately depends on the signing key's integrity. If the key fails, P fails. If P fails, V(π,t) collapses.

**h(τ) — integrity.** The h(τ) fraction measures key infrastructure quality. Properly rotated keys, hardware-bound storage, witnessed ceremonies — all increase h(τ). Expired keys, software storage, unwitnessed generation — all decrease h(τ). The integrity fraction gates A(τ): only cryptographically sound operations count toward verified history.

**Φ(Σ) — separation matrix.** The dual-key architecture IS the separation matrix's enforcement mechanism. Signing key ⊥ viewing key. If key ceremony fails to maintain this separation (e.g., a combined key that can both sign and view), Φ(Σ) collapses and det(Σ) = 0 — the architecture's mathematical guarantees evaporate.

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
