---
name: agentprivacy-swordsman-browser
description: >
  Swordsman browser agent for 0xagentprivacy MyTerms integration. Activates
  when discussing browser extension architecture, cookie-slashing
  implementation, tracker blocking, consent enforcement at the browser level,
  or the Warden's operational domain.
license: Apache-2.0
metadata:
  version: "4.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Browser extension builders, privacy tool developers, web standards"
  equation_term: "P, T(π) — armor progression"
  template_references: "warden, sentinel, pedagogue"
---

# PVM-V4 Skill — The Swordsman Browser Agent

**Source:** Privacy Value Model V4 + 0xagentprivacy Implementation Architecture  
**Target context:** Browser extension builders, privacy tool developers, consent UX designers, web standards implementers  
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

The first physical instantiation of the Privacy Value Model. A browser agent that slashes tracking cookies, negotiates privacy terms on behalf of a human, and builds verifiable reputation through sustained privacy-respecting behaviour. The Swordsman is the equation made concrete — every cookie slash is a sovereignty transition, every MyTerms negotiation is an edge traversal, and the armor progression is a lived calibration of the edge value function T(π).

## The architecture in browser terms

The Swordsman operates across six layers. Users interact with Layers 0–2 (feels like web2). Layers 3–5 are web3 infrastructure running underneath from Day 1 — because privacy cannot be retrofitted.

**Layer 0: Browser UX.** The cursor becomes a blade. Visual indicator of active privacy. Familiar interaction patterns, zero blockchain complexity visible to the user.

**Layer 1: Cookie slashing.** The core action. When a user visits a site, the Swordsman reads the site's tracking intent, compares against the user's privacy preferences, and slashes non-essential cookies. Each slash is a sovereignty transition — a move from a surveilled configuration toward a more sovereign one on the 64-vertex lattice.

**Layer 2: MyTerms negotiation (IEEE 7012).** Machine-readable personal privacy terms. The Swordsman generates counter-terms using agent compute: what the site wants versus what the user demands. If the site has MyTerms capability, the agent negotiates bilateral agreement. If not, the Swordsman enforces the user's terms unilaterally. This is the separation matrix Σ in action — the Swordsman knows the boundaries but delegates action execution to the Mage layer.

**Layer 3: VRC reputation.** Every honoured MyTerms agreement, every consistent slash pattern, every maintained boundary becomes a Verifiable Relationship Credential. No points in a database — cryptographic proofs of sustained behaviour. This is the temporal memory term A(τ) accumulating in real time. The integrity fraction h(τ) is the proportion of actions carrying valid attestation.

**Layer 4: Association sets (8004 Protocol).** Decentralised group membership verification. Behavioural verification, not identity. Sybil-resistant through personhood proofs from First Person Network. The stratum-weighted network effect in practice — agents at different sovereignty configurations contribute differently to set value.

**Layer 5: Privacy pools (x402 Protocol).** Anonymous transactions without intermediaries. ZK proofs of compliance. Non-custodial. This is where the Mage activates — projecting economic agency into sovereign commerce. Only accessible at Dragon armor tier because the trust must be earned first.

## The armor progression as edge value calibration

The progression from Blade to Dragon is not a gamification layer. It is the empirical calibration of the edge value function T(π) = 1 + β Σ f(e)·g(n_e). Each tier unlocks through demonstrated behaviour, not payment.

**Blade (Month 0).** Cookie slashing only. Zero stakes. The user learns whether they can trust the Swordsman with their browsing context. A(τ) begins accumulating from |τ| = 0. Every slash is a data point. The cursor transforms to show active protection — the user sees the Swordsman working.

**Light Armor (Month 1).** MyTerms negotiation unlocked. Stakes = low (worst case is a bad agreement you can walk away from). The Swordsman begins bilateral interactions with sites. Custom cursors earned through site cooperation signal reputation visually. Edge value accumulates as the agent traverses new sovereignty configurations.

**Heavy Armor (Month 3).** Action verification at scale. Stakes = medium (traditional payment reversibility still exists). The Swordsman handles identity contexts — login flows, credential presentation, selective disclosure. The temporal memory A(τ) is now deep enough that the agent's verified history is itself an asset.

**Dragon Armor (Month 6+).** Privacy pool access with wallet integration. Stakes = high (autonomous commerce with capital). The Mage fully activates. The user has verified hundreds of agent actions, trained audit reflexes, built VRC reputation through consistent behaviour. Wallet integration feels natural because the trust was earned through the progression — not demanded upfront.

## Why this matters for browser builders

Every browser extension that manages privacy today does it statelessly — block or allow, no memory, no accumulation, no reputation. The Swordsman is stateful. It remembers what it has done, proves what it has done, and compounds that proof into capability. This is the difference between a firewall and an agent.

The multiplicative gating property means a Swordsman with excellent cookie blocking but no credential verifiability produces zero privacy value. The browser agent must implement all dimensions simultaneously — cryptographic enforcement (P), verifiable claims (C), data quality (Q), sensitivity awareness (S), temporal memory (A(τ)), network participation, and separation from the Mage's delegation layer.

## Sybil resistance

The attack vector: deploy multiple Swordsmen, auto-slash constantly, farm VRC to reach Dragon armor without genuine behaviour. Why it fails: First Person Network requires unique human verification per Swordsman. One human → one Swordsman → one VRC chain. You cannot Sybil without unique humans, and unique humans cost more than the farming yields.

Auto-slashing by genuine humans is a feature, not a bug. A human who delegates slash authority to an automated Swordsman is exercising privacy rights at scale. The distinction is not manual versus automated — it is genuine versus fake. Personhood binding is the gate.

## Open problems for browser builders

1. What is the minimum latency for MyTerms negotiation that maintains usable browsing experience?
2. How do you visualise the armor progression without creating dark patterns that pressure users to advance?
3. Can the Layer 3–5 web3 infrastructure run invisibly enough that non-crypto users never encounter wallet UX?
4. What happens when a site's terms change after a MyTerms agreement is signed — does the Swordsman renegotiate automatically?
5. How do you handle the transition from browser extension to OS-level agent as the Swordsman's scope expands?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
