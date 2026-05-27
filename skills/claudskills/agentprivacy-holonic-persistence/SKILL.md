---
name: agentprivacy-holonic-persistence
description: >
  Multi-provider data persistence for privacy-preserving agents. Activates when
  discussing HyperDrive auto-failover, multi-provider replication, provider-agnostic
  storage, privacy-aware routing, write-all-or-fail for separation-critical state,
  TEE rotation with state persistence, or any task requiring durable agent state
  across backends, chains, and environments.
license: Apache-2.0
metadata:
  version: "5.0"
  category: "role"
  origin: "0xagentprivacy + OASIS Holonic Architecture"
  author: "Mitchell Travers / Max Gershfield integration"
  affiliation: "0xagentprivacy, BGIN, OASIS"
  status: "integration_draft"
  target_context: "Infrastructure architects, multi-chain developers, TEE engineers, data persistence designers"
  equation_term: "T(π) (provider-as-sovereignty-transition), D (reconstruction difficulty through provider splitting)"
  template_references: "architect, sentinel, shipwright, cipher, ranger"
---

# PVM-V4 Skill — Holonic Persistence

**Source:** Privacy Value Model V4 + OASIS Holonic Architecture Whitepaper v1.2
**Target context:** Infrastructure architects, multi-chain developers, data persistence designers
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

Privacy-preserving agents need somewhere to persist state that survives TEE rotation, chain migration, and provider failure. The OASIS holonic architecture provides identity-independent data persistence across heterogeneous backends. This skill integrates holonic persistence with the dual-agent separation model.

The key insight: provider diversity is a sovereignty dimension. An agent whose state exists on only one backend is sovereignty-limited to that backend's availability, jurisdiction, and privacy guarantees. Multi-provider persistence transforms T(π) from chain transitions to provider transitions — a richer sovereignty lattice.

## HyperDrive architecture

HyperDrive is the multi-provider orchestration layer:

**Auto-failover.** If the primary provider fails, HyperDrive automatically routes to the next provider in the failover list. The agent continues operating without interruption. This maps to dark forest resilience — never depend on a single point of failure.

**Auto-replication.** Holons are replicated across multiple providers according to the replication policy. Write operations can be configured as write-one (fast, eventual consistency), write-majority (balanced), or write-all-or-fail (strict, for separation-critical state).

**Load balancing.** Read operations distribute across healthy providers. The agent benefits from the fastest available provider without explicit routing logic.

**Privacy-aware routing.** Providers are classified by privacy characteristics:
- **Shielded providers:** Zcash, encrypted databases, privacy-first backends. Swordsman state routes here.
- **Public providers:** Ethereum, public APIs, transparent chains. Mage coordination state routes here.
- **Neutral providers:** IPFS, MongoDB with encryption-at-rest. Shared state routes here.

## Provider as sovereignty transition

In V(π,t), the term T(π) captures sovereignty transitions across the lattice. Holonic persistence expands the transition space:

**Each provider change is a sovereignty transition.** Moving a holon from MongoDB to Zcash is a transition from neutral to shielded — a movement in the privacy dimension of the sovereignty lattice.

**ProviderUniqueStorageKey tracks sovereignty history.** Each holon maintains a map of `{provider_type → storage_key}`. This map is the audit trail of where sovereignty has been exercised. Migration doesn't erase history — it accumulates.

**Provider diversity increases D.** The reconstruction difficulty term D benefits from provider splitting. Swordsman holons on Zcash + Mage holons on Ethereum = no single provider holds the complete agent model. Even if one provider is compromised, the holon fragments don't reconstruct.

## Consistency models and separation guarantees

The dual-agent separation requires mathematical guarantees. Best-effort replication is insufficient for I(S;M|π) ≤ ε enforcement:

**Separation-critical holons use write-all-or-fail.** Any holon that participates in the separation boundary must be replicated to ALL configured providers or the write fails. This prevents partial states that could leak cross-agent information.

**Non-critical holons use write-majority.** Memory fragments, cached reasoning, temporary coordination state can tolerate eventual consistency. Lower latency, higher availability.

**The separation invariant lives in the agent layer.** Holons carry the state; the dual-agent architecture enforces the constraint. Consistency for separation-critical holons is a data-layer requirement to support an agent-layer guarantee.

## TEE rotation with holonic persistence

When a TEE rotates (TEE-A → TEE-B), agent state must persist:

1. **Load root holon from primary provider.** The agent's memory tree loads from HyperDrive.
2. **Generate new TEE attestation.** TEE-B produces its attestation.
3. **Update ProviderMetaData.** The attestation field updates: `TEEAttestation → TEE-B_hash`.
4. **Replicate to TEE-B's provider set.** HyperDrive replicates to the new TEE's preferred providers.
5. **Retain previous attestation in history.** ProviderMetaData preserves the audit trail.
6. **GUID unchanged.** The holon's identity persists. ParentHolonId unchanged. Children unchanged.

The write policy determines rotation safety:
- **Write-all-or-fail** for the root holon (separation-critical)
- **Best-effort** for children (can be re-loaded from failover providers if needed)

## Integration with cross-chain skill

Multi-provider persistence complements multi-chain sovereignty:

**Provider types map to chains.** Zcash as a provider type, Ethereum as a provider type, NEAR as a provider type. The chain IS the provider for blockchain-backed holons.

**Cross-chain VRC migration is a provider transition.** A VRC holon loading from Ethereum, saving to NEAR, retaining both keys — this is holonic persistence in action.

**HyperDrive failover list = sovereignty preference order.** The order of providers in the failover list expresses sovereignty priority. Privacy chains first for Swordsman holons; coordination chains first for Mage holons.

## Operational patterns

**Development → Production.** Same holon trees, different provider configuration. MongoDB in development, Zcash+NEAR+IPFS in production. Application code unchanged.

**Provider failure recovery.** HyperDrive detects failure → routes to failover → agent continues → ops team investigates → provider restored → HyperDrive resumes normal routing.

**Migration.** Add new provider to holon → update HyperDrive config → replicate → remove old provider. The holon's GUID never changes. The application never notices.

**Audit.** ProviderUniqueStorageKey + ProviderMetaData create a complete audit trail: where the holon has lived, which TEEs have touched it, which providers currently hold it.

## Open problems

1. **Cross-provider consistency models** — can we achieve stronger-than-eventual consistency without write-all-or-fail latency?
2. **Privacy-aware replication** — should replication itself be shielded? Replication traffic patterns leak information.
3. **Provider trust ranking** — how to dynamically rank providers by trustworthiness, latency, and privacy guarantees?
4. **Cost optimisation** — blockchain providers cost gas; database providers cost compute. How to optimise the provider mix?
5. **Regulatory compliance** — some jurisdictions require data residency. How does HyperDrive handle geo-aware routing?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
