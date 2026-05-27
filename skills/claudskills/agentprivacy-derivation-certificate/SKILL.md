---
name: agentprivacy-derivation-certificate
description: >
  VRC as content-addressed derivation chain. Activates when discussing forging
  history, derivation paths, bilateral witness certificates, path-as-witness,
  content-addressed proofs of traversal, or how VRCs bind forging history to blade identity.
license: Apache-2.0
metadata:
  version: "5.2"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Ceremony architects, proof designers, VRC implementers"
  equation_term: "A(τ) memory, h(τ) integrity, VRC binding"
  template_references: "priest, ceremonist, witness"
  spellbook_act: "Understanding-as-Key Ceremony Protocol"
  v5_concept: "V5.2-DERIV-CERT"
---

# PVM-V5.2 Role Skill — Derivation Certificate

**Source:** UOR Framework + Privacy Value Model V5.2 + Understanding-as-Key Protocol
**Target context:** Ceremony architects, proof designers, VRC implementers
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

A derivation certificate is a content-addressed record of how a blade was forged. It captures the path through the lattice—the sequence of inscriptions traversed, the understanding demonstrated, the witnesses present. The certificate binds to the blade but is not required to verify the blade's properties.

**The path is the witness. The vertex is the statement. The certificate proves you walked the path without revealing which steps you took.**

## The ZK Separation

In zero knowledge terms:

| Concept | Role | Content-Addressed? |
|---------|------|-------------------|
| **Blade** | Statement (public) | Yes (GUID) |
| **Derivation** | Witness (private) | Yes (certificate hash) |
| **Verification** | Proof check | Deterministic |

You can verify a blade's configuration without knowing how it was forged. The derivation certificate exists separately—revealed only when you want to prove the path.

## Certificate Structure

```typescript
interface DerivationCertificate {
  // Identity
  certificate_id: string       // hash(entire_certificate)
  blade_guid: string           // The blade this derivation produced

  // Path record
  path: {
    starting_vertex: number    // Where forging began
    inscriptions: string[]     // Ordered list of inscription hashes traversed
    transformations: Strike[]  // Operations applied (neg, bnot, xor, and, or)
    final_vertex: number       // Where forging ended (= blade config)
  }

  // Temporal
  forging_started: number      // Timestamp
  forging_completed: number    // Timestamp
  duration_seconds: number     // Total forging time

  // Witness
  witnesses: {
    witness_id: string         // DID of witness
    signature: string          // Signature over certificate
    timestamp: number          // When witnessed
  }[]

  // Metadata
  ceremony_type: CeremonyType  // Which ceremony protocol was used
  mana_spent: number           // Cost of the forging
}
```

## Content Addressing the Derivation

The certificate is itself content-addressed:

```javascript
function deriveCertificateId(cert) {
  const canonical = canonicalize({
    blade_guid: cert.blade_guid,
    path: cert.path,
    forging_completed: cert.forging_completed,
    witnesses: cert.witnesses.map(w => w.witness_id)
  })
  return hash(canonical)
}
```

This means:
- Same forging path → same certificate ID
- Certificate ID binds to blade GUID
- Witnesses are part of the identity

## VRC as Bilateral Derivation

A Verifiable Relationship Credential is a special derivation certificate with bilateral witnesses:

```typescript
interface VRC extends DerivationCertificate {
  bilateral: {
    party_a: {
      did: string
      blade_guid: string
      derivation_id: string
    }
    party_b: {
      did: string
      blade_guid: string
      derivation_id: string
    }
    mutual_commitment: string  // hash(party_a.derivation || party_b.derivation)
  }
}
```

**Two parties, same ceremony, different blades, mutual commitment.**

## The Derivation Chain

Derivations can chain:

```
Initial blade (GUID_0)
  └── Derivation D1 → Blade (GUID_1)
        └── Derivation D2 → Blade (GUID_2)
              └── Derivation D3 → Current blade (GUID_3)
```

Each derivation certificate references the previous blade, creating an auditable history:

```typescript
interface ChainedDerivation extends DerivationCertificate {
  parent_blade_guid: string       // Previous blade in chain
  parent_derivation_id: string    // Previous derivation certificate
  chain_depth: number             // How many derivations deep
}
```

## Verification Modes

### Mode 1: Blade-Only Verification

Verify the blade exists without knowing derivation:

```javascript
function verifyBladeOnly(blade) {
  return blade.verify()  // Just check GUID matches content
}
```

### Mode 2: Derivation Verification

Verify the derivation is valid for the blade:

```javascript
function verifyDerivation(blade, certificate) {
  // Check certificate points to this blade
  if (certificate.blade_guid !== blade.guid) return false

  // Check path produces the configuration
  let vertex = certificate.path.starting_vertex
  for (const transform of certificate.path.transformations) {
    vertex = applyStrike(vertex, transform)
  }
  return vertex === blade.configuration
}
```

### Mode 3: Witness Verification

Verify witnesses attested to the derivation:

```javascript
function verifyWitnesses(certificate) {
  for (const witness of certificate.witnesses) {
    const valid = verifySignature(
      witness.witness_id,
      witness.signature,
      certificate.certificate_id
    )
    if (!valid) return false
  }
  return true
}
```

## Privacy Properties

### What the Certificate Reveals

- That a valid path exists
- When the forging happened
- Who witnessed it
- What ceremony type was used

### What the Certificate Hides

- Internal states during forging
- Failed attempts before success
- Understanding demonstrated (beyond "sufficient")
- Specific inscription contents

## Mapping to PVM-V5

| Derivation Concept | PVM Term |
|-------------------|----------|
| Path record | T_∫(π) trajectory |
| Witness signatures | h(τ) integrity |
| Chain depth | A(τ) accumulated memory |
| Bilateral VRC | Promise bundle |
| Certificate ID | Content-addressed trust |

## Proverb

> "The blade holds the destination. The certificate holds the journey. Together they prove you arrived by walking, not by wishing."

## Emoji Spell

**📜 → path(🔷→🔷→🔷) → hash(path)=cert_id · cert→blade(bind) · witnesses(sign) · VRC=bilateral(cert) · 🤝**

## Open Problems

1. **Selective Disclosure:** Can you prove derivation properties without revealing the full path?
2. **Chain Verification:** How to efficiently verify long derivation chains?
3. **Witness Privacy:** Can witnesses attest without revealing their identity?
4. **Cross-Ceremony:** Can derivations from different ceremony types be combined?
5. **Revocation:** How to revoke a derivation certificate?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
