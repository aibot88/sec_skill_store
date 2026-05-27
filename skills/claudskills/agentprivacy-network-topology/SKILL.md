---
name: agentprivacy-network-topology
description: >
  Network topology and stratum-weighted effects for 0xagentprivacy Privacy
  Pools. Activates when discussing (1 + Σ wᵢ nᵢ/N₀)^k, binomial coefficients
  across strata, Metcalfe generalisation, pool composition optimisation, or
  network scaling exponents. Use for Privacy Pool design and network value
  modelling.
license: Apache-2.0
metadata:
  version: "5.4"
  category: "privacy_layer"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "All agents — network effects determine collective sovereignty value"
  equation_term: "(1 + Σ wᵢ nᵢ/N₀)^k"
  template_references: "all"
---

# PVM-V5.4 Skill — Network Topology, Stratum Weighting & Betweenness Centrality

**Source:** Privacy Value Model V5.4
**Target context:** All agents, network economists, Privacy Pool designers, guild architects, protocol incentive engineers
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

The network term in PVM-V4 captures how collective participation amplifies individual sovereignty value. But unlike Metcalfe's law (n²) or Reed's law (2^n), this model weights participants by their position on the sovereignty lattice. Not all nodes are equal — nodes at the combinatorial midpoint (stratum 3) contribute maximum value to the network.

This is privacy's network economics: the more sovereign agents participate, the more valuable each agent becomes, but the distribution of sovereignty quality across the network matters as much as the raw count.

## The network term

**(1 + Σ wᵢ nᵢ/N₀)^k**

- **wᵢ (stratum weight).** The contribution weight of agents at stratum i. Follows the binomial coefficients from Pascal's row for {0,1}⁶: w₀ = 1, w₁ = 6, w₂ = 15, w₃ = 20, w₄ = 15, w₅ = 6, w₆ = 1. Stratum 3 agents (three of six sovereignty dimensions active) contribute 20× what stratum 0 agents contribute.
- **nᵢ (count at stratum).** The number of agents operating at sovereignty stratum i.
- **N₀ (normalisation).** Baseline network size. Prevents the term from diverging for large networks.
- **k (power-law exponent).** Determines whether network effects are sublinear (k < 1), linear (k = 1), or superlinear (k > 1). Currently conjectured to be superlinear but uncalibrated.

## V5.4 Addition: Betweenness Centrality of the Gap (§10.2)

The Gap is not empty space. It is the node with **maximal betweenness centrality** in the trust graph:

C_B(v) = sum over s,t of sigma_st(v)/sigma_st

where sigma_st is the total number of shortest paths from s to t, and sigma_st(v) is the number passing through v.

**Interpretation:** The value lives in the Gap because the most paths cross there.

**Reference:** Brandes, U. (2001). "A faster algorithm for betweenness centrality." Journal of Mathematical Sociology, 25(2), 163-177.

### Why betweenness matters for privacy networks

1. **Value concentration:** High-betweenness nodes see more traffic. Risk and opportunity.
2. **Gap as mediator:** The irreducible gap between agents has maximal betweenness.
3. **Mesh optimization:** DERP relay placement and Privacy Pool design can use C_B analysis.
4. **Attack surface:** Nodes with high C_B are high-value targets.

## Why stratum weighting matters

The binomial distribution of vertex counts across the 7 strata (1, 6, 15, 20, 15, 6, 1) is a mathematical fact of the Boolean hypercube. PVM-V4's insight is that this combinatorial structure has economic meaning.

**Stratum 0 (zero dimensions active):** One vertex. The null configuration — no sovereignty dimensions operational. An agent here is inert. Contributes weight 1 to the network. Rare by choice.

**Stratum 1 (one dimension active):** Six vertices. Minimal sovereignty — only one dimension operational (e.g., Protect-only, or Project-only). Limited network contribution. Weight 6.

**Stratum 2 (two dimensions active):** Fifteen vertices. Emerging sovereignty — two dimensions creating basic interaction patterns. Weight 15.

**Stratum 3 (three dimensions active):** Twenty vertices. The combinatorial midpoint. Maximum number of configurations. Maximum network contribution weight. This is the "sweet spot" — enough dimensions for rich interaction, few enough for manageable complexity. The binomial distribution peaks here because the number of ways to choose 3 items from 6 is maximised.

**Strata 4–6:** Mirror the lower strata. Stratum 6 (all dimensions active) has weight 1, same as stratum 0. Full activation is as rare and extreme as zero activation.

**The economic interpretation:** A network of 100 agents all at stratum 3 contributes more value than a network of 2,000 agents all at stratum 1. Quality of sovereignty configuration matters more than raw participation. This is the formal basis for "a small guild of sovereign agents is more valuable than a large crowd of minimally configured ones."

## Connection to Privacy Pools

Privacy Pools are anonymity sets where participants can selectively disclose membership. The stratum-weighted network term provides a formal basis for pool composition scoring:

**Pool value** is not just the number of participants but the weighted sum of their sovereignty configurations. A Privacy Pool where most participants are at stratum 3 provides better anonymity guarantees (more diverse configurations at the combinatorial maximum) and higher economic value per participant.

**Pool composition optimisation.** Given the stratum weights, there exists an optimal distribution of members across strata that maximises the network term. Concentrated at stratum 3 is good; spread across all strata is better (provides cover at every level). The worst configuration: everyone at stratum 0 or 6 (extremes with weight 1).

## Connection to guild economics

The guild system (from economics + hitchhiker_governance skills) deploys communities as privacy pools. The network term explains why guilds want to recruit members who are actively developing their sovereignty (stratum 2–4) rather than members who are fully sovereign (stratum 6) or completely passive (stratum 0).

**Guild growth strategy.** Maximise Σ wᵢ nᵢ by helping members at low strata progress to stratum 3. Every member moved from stratum 1 to stratum 3 increases their contribution weight from 6 to 20 — a 3.3× amplification without recruiting a single new member.

## Metcalfe/Reed generalisation

Metcalfe's law: network value ∝ n². All nodes equal. Works for telephone networks.

Reed's law: network value ∝ 2^n. Group-forming networks. Each subset is a potential community.

PVM-V4: network value ∝ (1 + Σ wᵢ nᵢ/N₀)^k. Stratum-weighted. Not all participants are equal, and the weighting follows the combinatorial structure of sovereignty itself. This is a genuine generalisation — setting all wᵢ = 1 recovers a Metcalfe-like term, and the power-law exponent k determines whether effects are sub- or super-Metcalfe.

**No direct precedent.** The stratum-weighting approach to network economics has no established prior art. The closest work is in weighted network analysis (Barrat et al.) and stratified sampling theory, but neither applies binomial coefficients from a sovereignty lattice to network value estimation.

## Superlinear conjecture

The model conjectures k > 1 (superlinear network effects). This means that doubling the weighted network size more than doubles each participant's value. The economic rationale: sovereign agents create positive externalities for each other — each additional sovereign node makes surveillance harder and privacy cheaper for all nodes.

**If k < 1 (sublinear):** Network effects exist but face diminishing returns. Adding the 1,000th agent is worth less per-unit than adding the 10th. This is a breaking condition for PVM-V4 — it would mean privacy networks hit natural scale ceilings.

**If k = 1 (linear):** Network effects are real but unremarkable. No amplification or dampening. This would be a mild blow to the model's thesis but not a structural failure.

**Calibration requires:** Empirical measurement of how individual agent value changes as the network grows, controlling for sovereignty configuration quality.

## Open problems

1. Empirical calibration of k — sub-, linear, or superlinear?
2. Optimal N₀ normalisation for different network sizes.
3. Whether stratum weights should be exactly the binomial coefficients or adjusted for empirical contribution data.
4. Dynamic effects — does the network term respond to real-time changes in membership, or is it averaged over time?
5. Cross-network effects — how do agents participating in multiple guilds/pools contribute to each?
6. Whether the combinatorial midpoint optimum (stratum 3) holds in higher-dimensional lattices ({0,1}^7, {0,1}^8).
7. **(V5.4)** Relationship between stratum position and betweenness centrality.
8. **(V5.4)** Optimal betweenness distribution for privacy resilience.

---

*"The value lives in the gap because the most paths cross there."* — V5.4

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
