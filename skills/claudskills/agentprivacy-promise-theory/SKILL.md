---
name: agentprivacy-promise-theory
description: >
  Promise Theory foundations for 0xagentprivacy bilateral relationships.
  Activates when discussing polarity (±), cooperation semantics, conditional
  promises, VRC-as-promise architecture, or Jan Bergstra / Mark Burgess
  promise frameworks. Use when designing bilateral trust relationships or
  consent infrastructure.
license: Apache-2.0
metadata:
  version: "4.0"
  category: "privacy_layer"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Promise Theory researchers, distributed systems architects, autonomous agent protocol designers"
  equation_term: "Cooperation substrate beneath all equation terms"
  template_references: "all"
---

# PVM-V4 Skill — Promise Theory Integration

**Source:** Privacy Value Model V4 + Bergstra & Burgess Promise Theory + Act XIII (Book of Promises)  
**Target context:** Promise Theory researchers, distributed systems architects, voluntary cooperation modellers, autonomous agent protocol designers  
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

Promise Theory (Bergstra & Burgess) provides the cooperation substrate beneath the Privacy Value Model. Where PVM-V4 quantifies the value of privacy-preserving architectures, Promise Theory explains why those architectures must be voluntary. The core principle: only autonomous agents can make promises. Promises reduce uncertainty. Impositions increase it. Cooperation emerges from aligned promises, never from forced compliance.

Every term in the PVM-V4 equation is a promise. P (privacy strength) is a promise to enforce cryptographic boundaries. C (credential verifiability) is a promise that claims can be independently verified. The separation matrix Σ is a promise that four sovereignty forces remain conditionally independent. The equation's multiplicative structure encodes the Promise Theory insight that breaking any single promise collapses the entire cooperative structure.

## Polarity mapping

Promise Theory defines two polarities: + (gives/offers) and − (uses/accepts). Cooperative binding occurs when + meets − with compatible scope.

In the dual-agent architecture, the Swordsman is + polarity — it gives protection, offers boundaries, promises data minimisation. The Mage is − polarity — it uses the protected space, accepts the boundaries as constraints, promises delegation within scope. The binding between them is the separation matrix Σ: the quality of their cooperative binding is measured by the conditional independence of their respective promises.

The golden ratio conjecture (φ ≈ 1.618 as optimal protect/project ratio) reinterprets under Promise Theory as a balance claim: the optimal cooperative binding occurs when the giving agent (Swordsman, + polarity) maintains approximately φ times the scope of the using agent (Mage, − polarity). More protection than delegation. More boundary than projection. The sword slightly larger than the spell.

## Promise graphs and the sovereignty lattice

Promise Theory represents agent interactions as directed graphs where edges are promises with typed polarity. The 64-vertex sovereignty lattice maps onto this framework directly. Each vertex is a configuration of active promises (six binary sovereignty dimensions, each either promised-active or promised-inactive). Each edge is a promise transition — activating or deactivating a sovereignty dimension, which means making or withdrawing a promise.

The edge value term T(π) = 1 + β Σ f(e)·g(n_e) measures the value of a promise trajectory — the sequence of promises made and honoured over time. The repetition discount g(n_e) reflects the Promise Theory insight that repeating the same promise yields diminishing cooperative value. New promises (novel transitions) contribute more than repeated ones.

The stratum weighting follows from Promise Theory's concept of superagency — agents whose promises compose to create capabilities beyond what individual promises achieve. Agents at stratum 3 (three active sovereignty promises out of six) have the maximum number of compositional possibilities, which is why the binomial coefficient peaks there. More active promises means more potential cooperative bindings with other agents.

## Bilateral assessment and VRCs

Promise Theory requires bilateral assessment: both parties evaluate the other's promise-keeping. This maps directly to VRC architecture. A VRC is a bilateral assessment inscribed as a cryptographic credential. Alice assesses Bob's promise-keeping (α_Alice(Bob)). Bob assesses Alice's promise-keeping (α_Bob(Alice)). The VRC encodes both assessments plus a bilateral proverb — the compressed cipher of their shared promise history.

The temporal memory term A(τ) = α · ln(1+|τ|) · h(τ) is the formal model of promise reputation. |τ| counts the number of assessed promise transitions. h(τ) measures the integrity fraction — what proportion of promises were verifiably kept. The logarithmic growth reflects Promise Theory's observation that early promises matter most for trust establishment (steep initial curve, flattening over time).

## Conditional promises and the armor progression

Promise Theory includes conditional promises: "I promise X if you promise Y." The armor progression (Blade → Light → Heavy → Dragon) is a chain of conditional promises:

The system promises Blade-level capabilities (cookie slashing) if the First Person promises personhood verification. The system promises Light-level capabilities (MyTerms negotiation) if the agent promises sustained privacy-respecting behaviour over time. The system promises Heavy-level capabilities (identity delegation) if the agent promises verified MyTerms compliance across multiple counterparties. The system promises Dragon-level capabilities (autonomous commerce) if the agent promises deep VRC history with high integrity fraction.

Each tier is a conditional promise that becomes active only when the preceding promise chain is fulfilled. No tier can be purchased or bypassed because the conditional structure requires demonstrated promise-keeping, not payment.

## Promise Theory corrections to PVM-V4

Promise Theory suggests a refinement the current model does not capture: promises are not just kept or broken (binary h(τ)). They are assessed with belief and evidence: β(π) (belief about whether the promise will be kept) and ε(π) (evidence about past keeping). The integrity fraction h(τ) should arguably be decomposed into these components — an agent with strong evidence of past keeping but currently uncertain belief (due to changed circumstances) is valued differently from one with weak evidence but strong current belief.

This decomposition is flagged as an open question. The current binary h(τ) ∈ [0,1] may be insufficient for agents operating in rapidly changing environments where past behaviour is a weak predictor of future promises.

## Open problems for Promise Theory researchers

1. Does the golden ratio φ emerge from Promise Theory's polarity balance, or is it a coincidence of the current parameterisation?
2. Can the bilateral assessment structure (α, β, ε) replace the binary integrity fraction h(τ) without making A(τ) computationally intractable?
3. How do conditional promise chains interact with the edge value function — does a conditional promise count as one transition or two?
4. What is the Promise Theory interpretation of the reconstruction ceiling R < 1 — is it a limit on what promises can reveal, or a limit on what assessments can infer?
5. Can Promise Theory's concept of "promise scope" formally bound the information leakage channels C_S and C_M in the separation theorem?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
