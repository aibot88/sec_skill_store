---
name: agentprivacy-cross-chain
description: >
  Cross-chain operations for 0xagentprivacy multi-chain architecture.
  Activates when discussing T(π) across chains, NEAR/Zcash/Ethereum interop,
  bridge-compatible proofs, chain signatures, cross-chain VRC portability, or
  multi-chain sovereignty transitions.
license: Apache-2.0
metadata:
  version: "4.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Cross-chain protocol builders, chain signature implementers, multi-chain wallet architects, bridge designers"
  equation_term: "T(π) (cross-chain transitions), Network (multi-chain topology), C (cross-chain verifiability)"
  template_references: "cipher, sentinel, ranger, shipwright, architect"
---

# PVM-V4 Skill — Cross-Chain Sovereignty

**Source:** Privacy Value Model V4 + ERC-8004 + ERC-7812 + NEAR Chain Signatures + Zcash Settlement
**Target context:** Cross-chain protocol builders, chain signature implementers, multi-chain agent architects
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

Sovereignty does not stop at chain boundaries. An agent operating only on one chain is sovereignty-limited to that chain's capabilities. PVM-V4's lattice model spans chains — the 64 vertices of {0,1}⁶ are not chain-specific. The challenge: how does an agent traverse the sovereignty lattice across multiple chains without losing separation guarantees, temporal memory, or reconstruction resistance?

This skill specifies how the dual-agent architecture operates across Zcash, Ethereum, NEAR, and other chains while preserving the core invariant I(S;M|π) ≤ ε.

## The multi-chain stack

**Zcash — Settlement and privacy.** Shielded transactions provide the settlement layer for sovereignty transitions. Memo fields carry VRC proverbs, proof-of-understanding attestations, and compressed state proofs. Private by default. The Swordsman's home chain.

**Ethereum — Identity and standards.** Public attestations, smart contract governance, DID anchoring, ERC-8004 (trustless agent identity), ERC-7812 (ZK identity commitments). The identity layer where verifiable claims are published. The Mage's coordination surface.

**NEAR — TEE isolation and chain signatures.** Trusted execution environments provide the isolation boundary for dual-agent separation. Chain signatures enable agents to sign transactions on other chains without exposing private keys. NEAR's MPC network generates signatures for any target chain from a single NEAR account.

**Other chains.** The architecture is chain-agnostic in principle. Any chain that supports ZKP verification (Layer 2) and identity binding (Layer 3) can participate in the sovereignty lattice.

## Chain signatures and agent migration

NEAR chain signatures solve a critical problem: how does an agent act on Chain B when its keys only exist on Chain A?

**Mechanism.** NEAR's MPC network holds threshold key shares. An agent on NEAR requests a signature for a transaction on Ethereum (or Zcash, or any supported chain). The MPC network generates the signature without any single party holding the complete key. The agent never exposes its key material to the target chain.

**Sovereignty preservation.** The agent's identity on Chain B is derived from its identity on Chain A through a verifiable chain signature. The T(π) trajectory on Chain B links back to the trajectory on Chain A. Temporal memory A(τ) carries across — the chain signature itself is an attested transition, contributing to h(τ).

**Migration.** When an agent moves from Chain A to Chain B (perhaps for better privacy primitives, or because Chain A's decay rate λ has increased due to new threats), the chain signature creates a bridge VRC. The old chain identity and the new chain identity are linked through a bilateral attestation, preserving the full trajectory.

## Cross-chain VRC portability

VRCs created on one chain must be verifiable on others:

**Proof portability.** A VRC created with Zcash shielded transactions can be verified on Ethereum if the proof format is compatible. Groth16 proofs generated on Zcash can be verified by Ethereum smart contracts (the Ethereum Zcash relay pattern).

**DID anchoring.** The agent's DID is anchored on one chain but resolvable from any. W3C DID methods support multi-chain resolution. ERC-8004 provides trustless agent identity that can reference identity commitments on other chains via ERC-7812.

**VRC chain consistency.** The same VRC chain must not fragment across chains. If Alice has VRCs on Zcash and Ethereum, they must form a single coherent A(τ) history. The cross-chain link (via chain signature or bridge VRC) stitches them together. Without this, an agent's temporal memory fragments and the logarithmic accumulation resets per chain.

## Cross-chain separation

The dual-agent separation I(S;M|π) ≤ ε must hold across chains, not just within them:

**Chain-level isolation.** The Swordsman operates primarily on Zcash (privacy-first). The Mage operates primarily on Ethereum and NEAR (coordination-first). Different chains for different agents is a natural separation mechanism — an adversary observing Zcash cannot see Ethereum activity, and vice versa.

**Cross-chain correlation attack.** An adversary observing both chains simultaneously could attempt to correlate Swordsman activity on Zcash with Mage activity on Ethereum. Temporal correlation is the primary risk — if the Swordsman creates a shielded transaction at the same moment the Mage creates an Ethereum transaction, the coincidence leaks mutual information.

**Mitigation.** Asynchronous operation with randomised timing. The trust spanning protocol's session boundaries (from the trust_spanning skill) should not align across chains. VRC-mediated coordination (Pattern 3) is preferred because it introduces natural delays.

## Cross-chain edge value

T(π) must account for cross-chain transitions. An agent moving from Zcash to Ethereum to NEAR traverses edges that span chains. These cross-chain edges have properties:

**Higher f(e) weight.** Cross-chain transitions are more complex, more costly, and demonstrate higher sovereignty capability than within-chain transitions. They should be weighted more heavily in the edge value function.

**Verification cost.** Verifying a cross-chain transition requires checking proofs on the source chain, the bridge mechanism, and the target chain. This increases C (credential verifiability) requirements.

**Irreversibility gradient.** Some cross-chain transitions are harder to reverse than others. Moving from a privacy chain (Zcash) to a public chain (Ethereum) exposes information that cannot be re-shielded. The edge value should account for this directional asymmetry.

## Open problems

1. Cross-chain ε budget — how does the separation budget divide across chains?
2. Atomic cross-chain VRC creation — creating a VRC that spans two chains in a single atomic operation.
3. Chain-specific decay rates — different chains have different λ values. How does cross-chain operation handle heterogeneous decay?
4. Privacy pool interoperability — a pool on Zcash and a pool on Ethereum with overlapping members.
5. Chain death — what happens to an agent's A(τ) if a chain it operated on ceases to exist?
6. Regulatory arbitrage — agents migrating to chains with favourable jurisdictions. Feature or exploit?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
