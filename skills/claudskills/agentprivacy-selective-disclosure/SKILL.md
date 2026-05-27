---
name: agentprivacy-selective-disclosure
description: >
  Selective disclosure and Privacy Pool mechanics for 0xagentprivacy.
  Activates when discussing R(d) minimum disclosure, stratum-weighted
  anonymity, pool entry/exit, disclosure set calculation, or how to prove
  properties without revealing underlying data.
license: Apache-2.0
metadata:
  version: "5.3.2"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Privacy Pool designers, selective disclosure protocol builders, association set architects, compliance engineers"
  equation_term: "R(d) (disclosure as reconstruction control), Network (pool composition)"
  template_references: "cipher, ranger, sentinel, gatekeeper, witness, architect"
---

# PVM-V4 Skill — Selective Disclosure

**Source:** Privacy Value Model V4 + FPS Act 10 (Topology of Revelation) + ZK Spellbook (Privacy Pools)
**Target context:** Privacy Pool designers, association set architects, compliance/disclosure protocol builders
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

The mechanics of revealing exactly enough and no more. Selective disclosure unifies two halves of the agentprivacy architecture: the dark forest strategy (what to reveal, when, to whom) and the ZKP machinery (prove the claim without revealing the data). This skill bridges them — the geometry of minimum disclosure as an optimisation problem.

## The integer bottleneck

From FPS Act 10 (Topology of Revelation): disclosure is not continuous. You cannot reveal half a fact. You reveal a fact or you do not. The topology of disclosure is discrete — integer steps, not smooth gradients.

This creates a fundamental bottleneck. The optimal disclosure point is almost never on an integer boundary. The best mathematical answer may be "reveal 2.7 facts about your identity." But you must round — either reveal 2 (underserving the verifier) or 3 (overexposing yourself). The gap between optimal continuous disclosure and realised integer disclosure is the bottleneck cost.

**ZKP as bottleneck reduction.** Zero-knowledge proofs partially dissolve the bottleneck by transforming the disclosure topology. Instead of "reveal fact X" (binary), ZKP offers "prove a property of X without revealing X itself." This turns one integer disclosure step into a spectrum: prove membership in a set (broad), prove a range (narrower), prove an exact property (narrow but not revealing). The bottleneck does not disappear — the proof itself reveals something (the statement is true) — but the granularity increases dramatically.

## Privacy Pools mechanics

A Privacy Pool is an anonymity set. Participants can prove membership without revealing which member they are. The pool provides cover: the larger and more diverse the pool, the less any individual member is identifiable.

**Association sets.** Subgroups within pools that vouch for each other's legitimacy. "I am a member of this pool, and I am associated with this subset of members who are known-good." This provides compliance cover without full disclosure — regulators can verify that pool members are associated with legitimate activity without identifying specific members.

**Pool composition scoring using PVM-V4.** The network topology skill provides the scoring framework. A pool's value depends on the stratum-weighted distribution of its members:

Pool_value ∝ Σ wᵢ nᵢ where wᵢ follows binomial coefficients.

A pool concentrated at stratum 3 (members with three active sovereignty dimensions) generates maximum value per member. A pool with diverse stratum representation provides maximum anonymity cover. The optimal pool balances both.

## Disclosure as reconstruction control

The R(d) term measures reconstruction resistance as a function of disclosure depth d. Selective disclosure is the mechanism by which the agent manages R(d) — choosing how much to reveal to keep R below the ceiling.

**The tradeoff.** More disclosure (higher d) provides more utility to counterparties — they can verify more about you, trust you more, serve you better. But higher d increases R(d), bringing the reconstruction rate closer to the ceiling. The agent must navigate this tradeoff for every interaction.

**Curved light (from dark forest).** The Swordsman's core technique: reveal just enough to be useful in a specific context, with the revelation shaped by ZKP to prevent leakage to other contexts. "Curved light" means the disclosure illuminates only the intended recipient — observers outside the VRC-gated channel learn nothing.

## Minimum disclosure as geometric constraint

On the sovereignty lattice, each disclosure corresponds to revealing one or more bits of the agent's position. The minimum disclosure for a given verification need is the smallest number of bits that satisfies the verifier's requirements.

**Stratum-aware disclosure.** An agent at stratum 4 (four active dimensions) may need to prove it is "at least stratum 3" to qualify for a guild. The minimum disclosure: prove Hamming weight ≥ 3 without revealing which specific dimensions are active or the exact count. This is a natural ZKP application — prove a property of the lattice position without revealing the position itself.

**The 64-vertex proof space.** Sovereignty-class proofs attest to membership in subsets of the 64 vertices. "I am at one of the 20 vertices in stratum 3" reveals stratum but not position. "I am at one of the 35 vertices in stratum 3 or higher" reveals a lower bound. The proof's anonymity set size is the subset cardinality.

### Moon Phase as Visibility Ratio

The moon phase notation encodes stratum as a visual indicator of the sovereignty posture:

| Phase | Stratum | Disclosure Level |
|-------|---------|------------------|
| 🌑 | 0 | Nothing disclosed — total darkness |
| 🌒🌓 | 1-2 | Minimal disclosure — sliver of visibility |
| 🌔 | 3 | Balanced disclosure — half sovereignty |
| 🌖🌗 | 4-5 | Substantial disclosure — near-full |
| 🌕 | 6 | Full sovereignty posture — all dimensions visible |

The moon is the whole information space. The lit portion is what the Swordsman's boundary allows to be reflected. The dark portion remains private.

**The ZK distinction:** The phase shows the sovereignty POSTURE (which dimensions are active) but NOT the CONTENT (what was discussed within those dimensions). A 🌗 blade proves "five dimensions active" without revealing which nodes activated them.

## Disclosure protocols

**Type 1 — Existence proof.** "I have a VRC with counterparty X." Proves relationship exists without revealing terms, history, or bilateral proverb. Minimum disclosure for trust establishment.

**Type 2 — Property proof.** "My sovereignty score is above threshold T." Proves a property of the agent's state without revealing the state itself. Used for guild membership, pool qualification.

**Type 3 — Transition proof.** "I transitioned from configuration A to configuration B through a valid path." Proves trajectory history without revealing specific intermediate states. Combined with h(τ) attestation, proves the transition was cryptographically verified.

**Type 4 — Association proof.** "I am a member of association set S, and S meets compliance standard C." Proves association without identifying which member. The Privacy Pool use case.

## Tornado's Eye — what went wrong

The ZK Spellbook includes Tornado Cash as a case study in selective disclosure failure. Tornado provided perfect anonymity (Type 4 proof — "I am a member of this pool") but no association set mechanics. Without association sets, the pool included both legitimate and illegitimate participants. Regulators could not distinguish, so they sanctioned the entire pool.

**PVM-V4 design response.** Association sets allow selective disclosure of legitimacy without sacrificing anonymity. "I am in this pool, and I am associated with the subset of pool members who passed legitimacy verification" — without revealing which member or which specific legitimacy criteria were verified. This is the compliance-preserving anonymity that Tornado lacked.

## Scaffolding as selective disclosure for reasoning

BRAID's procedural scaffolding principle (arXiv:2512.15959) is selective disclosure applied to inference. The graph reveals the reasoning STRUCTURE (constraints, steps, branching logic) without the reasoning CONTENT (the actual output text).

The Numerical Masking Protocol makes the ZK parallel explicit: all numerical literals in the graph are replaced with `_`, ensuring the solver receives only logical topology, not computational state. This is zero-knowledge for computation — prove you know HOW to solve without revealing the solution.

**Reasoning disclosure topology:** Just as data disclosure has an integer bottleneck (reveal fact X or don't), reasoning disclosure has a graph-topology bottleneck. You can share the graph structure (node types, edge conditions) without sharing node contents. The graph is the scaffold; the content is the output. Scaffolding without answer. Structure without content. Proof without data.

## Open problems

1. Optimal disclosure depth d as a function of counterparty trust level and interaction type.
2. Formal cost function for the integer bottleneck — quantifying the gap between optimal continuous and realised discrete disclosure.
3. Dynamic pool composition — how should pools rebalance as members progress through armor tiers?
4. Cross-pool disclosure — how does proving membership in Pool A interact with membership in Pool B?
5. Regulatory acceptance — will association set proofs satisfy compliance requirements in practice?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
