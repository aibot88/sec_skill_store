---
name: agentprivacy-ai-agent
description: >
  AI agent architecture and dual-agent separation for 0xagentprivacy.
  Activates when discussing I(S;M|π) mutual information bounds, TEE isolation,
  agent lifecycle (spawn/operate/rotate/recover/retire), Oracle architecture,
  or the fundamental design of privacy-preserving AI agents.
license: Apache-2.0
metadata:
  version: "4.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "AI agent frameworks, multi-agent coordination, AI safety"
  equation_term: "I(S;M|π) ≤ ε — dual-agent separation"
  template_references: "architect, assessor, ambassador, weaver, healer, witness"
---

# PVM-V4 Context — AI Agent Architecture & Coordination

**Source:** Privacy Value Model V4 Formal Specification (Travers, Feb 2026)  
**Target context:** AI agent frameworks, multi-agent coordination, AI safety research, agent economy infrastructure  
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## The privacy-delegation paradox

AI agents face a fundamental tension: to act on your behalf, an agent needs to know your preferences, constraints, and goals. But any agent that knows all of these can reconstruct your complete behavioural model — and so can anyone who compromises that agent. Delegation requires disclosure; disclosure destroys privacy. PVM-V4 resolves this through architectural separation, not policy constraints.

## Dual-agent separation (the core architectural claim)

The model proves that a single agent holding both privacy boundaries and delegation preferences can reconstruct its principal's behavioural profile. The solution: two mathematically separated agents.

**Swordsman** — handles privacy protection, boundary enforcement, data minimisation. Knows what to hide but not what to do.

**Mage** — handles delegation, external coordination, action execution. Knows what to do but not what to hide.

The proven reconstruction ceiling: R_max = (C_S + C_M)/H(X) < 1, where C_S and C_M are the information leakage from each agent's channel, and H(X) is the entropy of the principal's private state. Because the agents are conditionally independent, their leakages are additive (not multiplicative), keeping total reconstructable information below the threshold needed for full behavioural recovery.

This is an information-theoretic bound, not a policy constraint. It holds against any adversary with access to both agents' outputs, provided the conditional independence is maintained with ε < 0.1.

## Why this matters for agent architectures

**Single-agent systems are structurally unsafe.** Any architecture where one agent manages both "what to protect" and "what to delegate" creates an internal information channel that violates the separation requirement. This applies to monolithic LLM agents with system prompts containing both privacy rules and action permissions, tool-using agents with unified context windows, and memory-augmented agents that store privacy preferences alongside task history.

**The separation is enforced mathematically, not by instruction.** Telling an agent "don't use privacy preferences when making decisions" is not separation. The agents must operate in isolated execution environments (TEEs, separate processes, distinct key domains) where cross-contamination is physically prevented.

**Four forces emerge from two agents.** Protect (Swordsman primary function) and Project (Mage primary function) generate two emergent forces through sustained operation: Reflect (the temporal integral of protection decisions — an accumulated record of boundary-setting that itself becomes an asset) and Connect (the network effect of delegation patterns — how the Mage's coordination creates relationship value). The 4×4 separation matrix Σ measures pairwise independence across all four forces.

## Agent coordination model

The 64-vertex sovereignty lattice defines the configuration space for agent coordination. Each vertex is a binary 6-tuple representing which sovereignty dimensions are active. Agents coordinate across strata — the number of simultaneously active dimensions. Key coordination properties:

**Stratum-weighted network effects.** Not all agents contribute equally to network value. Agents at stratum 3 (the combinatorial midpoint, with 20 of 64 vertices) contribute most. This means agent ecosystems should optimise for diverse, mid-sovereignty participants rather than maximising the count of fully-sovereign or fully-surveilled agents.

**Edge value dominates vertex value.** The lattice has 192 undirected edges versus 64 vertices. PVM-V4's T(π) term captures the insight — drawn from category theory's Yoneda lemma and neural network architecture — that what an agent does (transitions between configurations) matters more than what an agent is (its current configuration). Agent reputation systems should weight demonstrated sovereignty transitions above static sovereignty claims.

**Repetition decays.** Traversing the same sovereignty transition repeatedly yields diminishing returns. This penalises agents stuck in loops and rewards agents that explore the configuration space — a formal incentive for sovereignty growth rather than sovereignty performance.

## Integration with existing agent frameworks

**Tool-use agents.** Each tool invocation is a potential sovereignty transition. The Swordsman evaluates whether the tool call respects privacy boundaries; the Mage evaluates whether it achieves delegation goals. Their independent assessments must agree before execution. This maps to existing approval/guardrail patterns but with formal separation requirements.

**Multi-agent systems.** In systems with multiple cooperating agents (AutoGen, CrewAI, etc.), PVM-V4 suggests that each agent should be internally separated (its own Swordsman/Mage pair) rather than having a single privacy layer wrapping the entire system. A shared privacy boundary for a multi-agent system creates a single point where full behavioural reconstruction becomes possible.

**Memory and context.** The temporal memory term A(τ) provides a formal model for how agent memory accumulates value. Memory that is ZK-attested (h(τ) → 1) grows in value logarithmically. Unattested memory contributes nothing. This argues for verifiable memory architectures where past actions carry cryptographic proof rather than plain-text logs.

**Agent-to-agent trust.** The separation matrix Σ can be shared between agents as a trust credential. An agent that can prove high det(Σ) — meaning its four sovereignty forces are well-separated — is demonstrably safer to delegate to. This creates a formal basis for agent reputation beyond task performance metrics.

## Implications for AI safety

The model reframes a core AI safety concern. The worry is usually: "how do we prevent agents from doing harmful things?" PVM-V4 adds a structural concern: "how do we prevent agents from knowing enough to reconstruct their principal's full behavioural model?" The separation theorem shows these are related — an agent that can reconstruct your behaviour can also predict and manipulate it. Architectural separation addresses both simultaneously.

The multiplicative gating property means safety is not graceful degradation — if any sovereignty dimension fails, total value collapses to zero. This aligns with safety engineering principles where certain failure modes should be catastrophic rather than gradual, because gradual failure creates false confidence.

## Split-architecture inference for dual agents

When a Swordsman or Mage agent needs to reason, the reasoning itself should be split. BRAID's Generator/Solver pattern (arXiv:2512.15959) applied to dual-agent inference:

**Swordsman reasoning:** A capable model generates BRAID boundary-checking graphs. A nano-tier model executes them for every data access request. Cost per check: fractions of a cent. This makes real-time boundary enforcement economically viable at scale.

**Mage reasoning:** A capable model generates BRAID delegation graphs. A lightweight model executes them for coordination and service selection. Delegation reasoning cached and reused across similar contexts.

**Oracle reasoning:** BRAID mediation graphs encode when to pass Swordsman signals to Mage, when to block, when to transform. The Oracle doesn't need intelligence — it needs to follow a pre-validated decision tree.

BRAID's future work proposes fine-tuned "Architect" models specialised for reasoning graph generation. This is the Architect persona (☯️🤖) applied to inference: the entity that designs reasoning structures, separate from the entities that execute within them.

## Open problems for agent researchers

1. Can dual-agent separation be maintained in practice with latency acceptable for real-time agent operation?
2. What is the minimum isolation guarantee (ε threshold) needed for the reconstruction ceiling to hold under realistic adversaries?
3. How does the four-force model interact with RLHF and constitutional AI training approaches?
4. Can det(Σ) be computed and verified without revealing the individual separation coefficients?
5. What agent communication protocols maintain conditional independence while allowing sufficient coordination?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
