---
name: agentprivacy-separation-enforcement
description: >
  Active maintenance of the dual-agent separation boundary Φ(Σ) for
  0xagentprivacy architecture. Activates when designing the swordsman-mage
  boundary, verifying that signing and viewing capabilities remain
  orthogonal, detecting separation violations, or building the enforcement
  mechanisms that keep det(Σ) ≠ 0 — the mathematical guarantee that no
  single entity can both protect and project.
  Triggers: "separation", "dual-agent boundary", "swordsman mage split",
  "Phi Sigma", "det Sigma", "signing viewing separation", "orthogonality",
  "information-theoretic bound", "separation violation", "gap enforcement".
license: Apache-2.0
metadata:
  version: "5.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  equation_term: "Φ(Σ) — the separation matrix; det(Σ) ≠ 0 is the architecture's core invariant"
  template_references: "soulbis, soulbae, cipher, sentinel, gatekeeper, architect"
---

# PVM-V4 Skill — Separation Enforcement

**Source:** Privacy Value Model V4 + Information-Theoretic Separation Proof + Dual-Agent Architecture
**Target context:** Privacy architecture designers, dual-agent system builders, information-theoretic security researchers, separation verification engineers, sovereignty infrastructure architects
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

Every guarantee in the 0xagentprivacy architecture flows from a single invariant: the swordsman and the mage cannot be collapsed into one entity. The signing key cannot read the data it authorises. The viewing key cannot sign the authorisations it reads. This separation is not a convention, not a policy, not an alignment goal — it is a mathematical constraint enforced through information-theoretic bounds and cryptographic architecture.

Separation enforcement is the discipline of keeping that constraint true through time, through upgrades, through adversarial pressure, and through the daily temptation to make the system "simpler" by merging what must remain apart.

## The separation matrix Φ(Σ)

The separation is formalised as a matrix:

```
Σ = | S_sign   S_view  |
    | M_sign   M_view  |
```

Where S = swordsman observation set, M = mage observation set. The critical requirement:

**det(Σ) ≠ 0**

If the determinant is zero, the rows are linearly dependent — the swordsman and mage can be expressed as functions of each other. One entity can simulate both. The separation collapses. R reaches 1. Sovereignty disappears.

If the determinant is non-zero, the observation sets are linearly independent. No function maps one to the other. No entity holding one set can reconstruct the other. The gap between them is mathematically irreducible.

## What the swordsman knows (and doesn't)

The swordsman's observation set S includes:
- Which keys exist (the full key hierarchy)
- Which authorisations were signed (consent declarations, delegation keys, VRC inscriptions)
- The structure of the trust graph (which bilateral relationships exist)
- The timing of authorisation requests
- The threat environment (elevated/normal/reduced)

The swordsman's observation set S EXCLUDES:
- The content of any data being authorised for disclosure
- The substance of any mage observation or interpretation
- The Person's browsing patterns, preferences, or behavioural model
- The semantic content of Intel Pool contributions
- Anything the viewing key decrypts

**The swordsman signs blind.** It knows that data is being released. It knows the scope (health data, financial data, identity credential). It knows the counterparty. It does NOT know the actual data values. This is the architectural miracle: authorisation without inspection.

## What the mage knows (and doesn't)

The mage's observation set M includes:
- Everything the viewing key decrypts (the Person's data as stored)
- The Person's behavioural patterns as observed through the viewing key
- Intel Pool contributions and received intelligence
- The semantic content of bilateral proverbs and VRC ceremonies
- Context for minimum disclosure calculations

The mage's observation set M EXCLUDES:
- The signing key material
- The ability to authorise any operation
- The structure of active delegations (which counterparties have which access)
- Revocation capabilities
- Consent scope definitions

**The mage observes without touching.** It can see everything about the Person's data. It can recommend disclosure sets. It can calculate minimum information. It CANNOT sign anything. Without the swordsman's signature, no data moves.

## The mutual information bound

The information-theoretic foundation:

```
I(S; M | π) < H(X) - ε
```

The mutual information between the swordsman's observations and the mage's observations, conditioned on the Person's identity, is strictly less than the total entropy of the Person's behavioural model minus some positive ε. This means: even combining both observation sets leaves a gap. The Person's complete model is never reconstructable, even by the agents themselves.

This bound holds because:
- The signing key is generated independently of the viewing key
- Authorisation metadata (who, when, scope) is insufficient to reconstruct content
- Observation metadata (what was seen) is insufficient to reconstruct authorisation patterns
- The cryptographic protocols are designed to minimise cross-set leakage

## Separation violation modes

The separation can be undermined through:

**Key merger.** A single key or system gains both signing and viewing capabilities. This is the most direct violation: det(Σ) = 0 immediately. Defence: hardware-enforced separation (enclave_operations), separate key generation ceremonies, no shared key material between swordsman and mage.

**Side-channel leakage.** The swordsman's signing patterns leak information about the mage's observations. Example: the swordsman signs immediately after the mage observes sensitive data — the timing correlation reveals that sensitive data was observed. Defence: timing decorrelation (metadata_resistance), batch signing (accumulate requests, sign at fixed intervals).

**Collusion by host.** If both agents run on the same machine under the same OS, the OS can read both agents' memory. The host can reconstruct what neither agent alone can see. Defence: separate enclave execution (enclave_operations), or separate physical machines for highest threat models.

**Inference from intersection.** Even without direct leakage, the intersection of metadata from both sets may be reconstructive. If the swordsman's authorisation log shows "health data disclosed at 14:03" and the mage's observation log shows "diabetes query at 14:02", the two logs together reveal more than either alone. Defence: temporal decorrelation, metadata minimisation in both logs.

**Protocol evolution drift.** Over time, protocol updates might introduce shared state between swordsman and mage. A "convenience feature" that lets the swordsman preview data before signing. A "performance optimisation" that caches viewing key outputs in swordsman-accessible memory. Each such change erodes det(Σ). Defence: separation audits at every protocol upgrade.

## Separation verification

The separation must be continuously verified, not assumed:

**Static analysis.** Code review of both agents' codebases to verify no shared memory, no shared keys, no direct communication channel that bypasses the Person. The Cipher runs formal verification tools to prove that information flow between the two agents' code paths satisfies the separation constraint.

**Dynamic monitoring.** Runtime monitoring of both agents' I/O to detect unexpected cross-set information. If the swordsman's log contains any content-level information, or the mage's log contains any authorisation-level information, the Sentinel flags a potential violation.

**Cross-attestation.** Both agents run in separate TEEs and cross-attest: the swordsman's enclave proves it cannot access the mage's enclave, and vice versa. This hardware-level proof is stronger than any software analysis.

**Adversarial testing.** The Sith runs separation attacks: given full access to one agent's observations, attempt to reconstruct the other agent's observations. If any reconstruction succeeds beyond the bound ε, the separation is insufficient. Regular adversarial testing is the separation's stress test.

**Formal proof verification.** The information-theoretic bound I(S; M | π) < H(X) - ε is a theorem, not a measurement. But the theorem's assumptions must hold in practice. Formal verification checks that the implementation satisfies the proof's preconditions: independent key generation, minimal cross-set leakage, correct protocol execution.

## The Person in the gap

The gap between swordsman and mage is not empty — the Person lives there. This is by design:

The Person is the only entity that can bridge both observation sets. The Person tells the swordsman what to sign. The Person tells the mage what to interpret. The Person sees both the data (through the mage's reports) and the authorisations (through the swordsman's audit trail). The Person is the only complete observer of their own sovereignty.

This means the Person cannot be automated away. No AI agent, no smart contract, no automation layer can replace the Person in the gap without collapsing the separation. Delegation (letting the mage act on the Person's behalf) is bounded precisely because the mage cannot sign. Automation (letting the swordsman auto-approve based on rules) is bounded precisely because the swordsman cannot see content.

The gap is where human sovereignty persists. Closing it — however tempting for convenience — destroys the architecture's core guarantee.

## Inference-layer separation: Generator ⊥ Solver

BRAID (Amcalar & Cinar, arXiv:2512.15959) provides empirical validation that separation is superlinear at the inference layer, not just at the agent layer. The Generator/Solver split decouples reasoning planning from reasoning execution:

- Generator: sees the full problem, produces the bounded reasoning graph. Analogous to Soulbae (viewing key — sees the full context).
- Solver: executes the graph without seeing the full problem context. Analogous to Soulbis (signing key — acts without full visibility).
- The Mermaid graph between them is a bounded channel with I(G;S|task) ≤ δ.

This yields 30–74× PPD improvement — empirical proof that separation creates superlinear value at the inference layer, just as Φ(Σ) creates superlinear value at the agent layer.

**Three-axis separation model.** The full architecture now enforces separation at three layers:

| Axis | Separation | Enforcement | Value |
|---|---|---|---|
| Agent layer | Swordsman ⊥ Mage | I(S;M|π) ≤ ε | Privacy preservation |
| Data layer | Shielded providers ⊥ Public providers | Holonic provider splitting | Reconstruction resistance |
| Inference layer | Generator ⊥ Solver | BRAID bounded graph | 30–74× cost efficiency |

Each axis strengthens the others. Agent separation is cheaper when inference separation reduces per-operation costs. Data separation is more durable when agent separation prevents cross-domain leakage. The three-axis model is multiplicative, not additive.

## Connection to the equation

**Φ(Σ) — the separation matrix.** This skill IS the Φ(Σ) term. Every other term in the equation assumes Φ(Σ) holds. If det(Σ) = 0, the entire equation collapses: P becomes meaningless (protection without separation is surveillance with extra steps), C becomes unverifiable (what was computed by whom?), R reaches 1 (full reconstruction becomes possible).

**R<1 — reconstruction ceiling.** The reconstruction ceiling is a direct consequence of separation. R<1 holds precisely because no single observation set contains enough information to reconstruct the Person's complete behavioural model. R = (C_S + C_M) / H(X) < 1 only if C_S and C_M are genuinely independent channels, not a single channel wearing two masks.

**V(π,t) — privacy value.** The 31,000× privacy value premium over surveillance depends entirely on det(Σ) ≠ 0. In a surveillance architecture (det(Σ) = 0), V collapses to V_surv. In the privacy architecture (det(Σ) ≠ 0), V compounds superlinearly through all terms. The separation is not a feature — it is the difference between the two architectures.

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
