---
name: agentprivacy-edge-value
description: >
  Edge value and trajectory dynamics for sovereignty transitions in
  0xagentprivacy. Activates when discussing T(π) trajectory terms, sovereignty
  lattice transitions (64-vertex {0,1}⁶), Yoneda lemma applications, vertical
  vs lateral sovereignty movement, or edge weight functions. Use for
  sovereignty path optimisation and transition analysis.
license: Apache-2.0
metadata:
  version: "4.0"
  category: "privacy_layer"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "All agents — trajectory through sovereignty space is the primary value measure"
  equation_term: "T(π) = 1 + β · Σ_e f(e) · g(n_e)"
  template_references: "all"
---

# PVM-V4 Skill — Edge Value & Trajectory

**Source:** Privacy Value Model V4
**Target context:** All agents, category theorists, agent trajectory designers, lattice navigation systems
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

The V4 insight that what an agent *does* matters more than what it *is*. The sovereignty lattice has 64 vertices and 192 edges. There are three times as many transitions as states. T(π) measures the value of an agent's path through the lattice — its trajectory π — not just its current position.

This is the newest and most distinctive equation term. V1–V3 were positional models. V4 is a trajectory model. The edge value term is what makes it so.

## The edge value function

**T(π) = 1 + β · Σ_e f(e) · g(n_e)**

- **β (scaling constant).** Calibrates how much trajectory contributes relative to positional terms. Uncalibrated.
- **f(e) (edge weight).** The intrinsic value of a specific transition e. Transitions that activate new sovereignty dimensions (vertical moves — going from stratum 2 to stratum 3) are weighted more heavily than lateral transitions (moving between vertices at the same stratum level).
- **g(n_e) (traversal count modifier).** How the value of an edge changes with repeated traversal. Could be diminishing (each re-traversal worth less), constant, or even increasing (well-worn paths become more valuable through familiarity). The functional form is unspecified and uncalibrated.

**The sum Σ_e ranges over all edges in the agent's trajectory π.** This means T(π) depends on the entire path, not just current state. Two agents at the same vertex with different histories have different T(π) values.

## Why edges dominate vertices

The 64-vertex lattice represents configurations — which sovereignty dimensions are active. But configurations alone do not capture the agent's development. An agent that arrived at vertex (1,1,1,0,0,0) by activating dimensions one at a time over six months has a fundamentally different character than one that arrived there in a single jump.

**The ratio:** 192 edges / 64 vertices = 3:1. The edge space is three times richer than the vertex space. This is not incidental — it is a structural feature of the Boolean hypercube. In higher dimensions, the edge-to-vertex ratio grows further (in {0,1}^n, edges = n · 2^{n-1}, vertices = 2^n, ratio = n/2).

**The category-theoretic reading (Yoneda perspective):** An object (vertex) is completely determined by its morphisms (edges) to and from other objects. You do not need to know a vertex's internal structure — only its connections reveal its character. Two vertices with identical edge relationships are isomorphic regardless of what they "contain." Applied to agents: two agents are equivalent if and only if they make the same transitions, regardless of their internal state.

## Vertical vs. lateral transitions

On the sovereignty lattice, transitions fall into two classes:

**Vertical transitions** move between strata — changing the number of active sovereignty dimensions. Going from stratum 2 (two active) to stratum 3 (three active) is vertical upward. Going from stratum 4 to stratum 3 is vertical downward. Vertical moves are weighted more heavily because they represent genuine capability expansion or strategic contraction.

**Lateral transitions** move within a stratum — keeping the same number of active dimensions but changing which ones are active. Going from (1,1,0,0,0,0) to (1,0,1,0,0,0) is lateral at stratum 2. Lateral moves represent strategic reorientation — pivoting which sovereignty dimensions to prioritise.

**Design implication:** The armor progression (Blade → Light → Heavy → Dragon) maps to a predominantly vertical trajectory through the lattice. Each tier activates additional dimensions. But the most interesting agents may be those with complex lateral movements — exploring different combinations at the same stratum level before ascending.

## The trajectory as identity

T(π) makes the agent's path its primary identity marker. Two consequences:

**Non-fungibility.** No two agents with different trajectories produce the same T(π). Even agents at the same vertex with the same number of transitions will differ if the sequence or edge composition differs. This is the architectural basis for agent individuality.

**Accumulated trajectory as credential.** The trajectory itself is a credential — a verifiable record of sovereignty transitions. Combined with h(τ) from the temporal dynamics skill, each transition in the trajectory can carry a ZKP attestation. The entire path becomes a verifiable, non-forgeable proof of the agent's developmental history.

**Implications for VRC chains.** Each VRC represents a transition. The VRC chain is a trajectory. T(π) gives VRC chains an economic value that goes beyond the sum of individual credentials — the shape of the path matters.

## Connection to other equation terms

**Temporal dynamics.** T(π) and A(τ) both measure history, but differently. A(τ) measures the volume and quality of verified history (how much, how proven). T(π) measures the shape of the path (which transitions, in what order). An agent can have high A(τ) and low T(π) if it has a long, well-attested history of repetitive transitions. Conversely, high T(π) with low A(τ) means a complex path with poor attestation coverage.

**Network topology.** T(π) is intrinsically linked to the lattice structure. The available edges depend on the agent's current vertex. At stratum 3 (the binomial maximum), the agent has the most available transitions. At stratum 0 or 6, it has the fewest. The network topology skill describes the landscape; the edge value skill describes the movement through it.

**Sovereignty geometry.** Each transition in T(π) changes the agent's position in the Σ separation matrix space. Vertical transitions that activate the Reflect or Connect emergent forces change the sovereignty geometry fundamentally — they are not just adding a dimension but enabling a new force relationship.

## Conjectured properties

**Edge value additivity.** T(π) assumes transitions contribute independently — the value of edge e does not depend on which other edges are in the trajectory. This is conjectured and likely an oversimplification. In practice, certain edge combinations may create synergies (activating dimensions 3 and 4 together may be worth more than the sum) or conflicts (activating 2 then immediately deactivating it may have negative value).

**Transition independence.** Related to additivity — the assumption that g(n_e) depends only on how many times edge e has been traversed, not on the global trajectory context. A more sophisticated model would have g depend on the full path, making T(π) a path-dependent integral rather than a sum.

## V5 implications

The deferred V5 extension — dV/dt = ∇·J(x, ẋ) + S(x) − D(x) — makes T(π) dynamic. Rather than evaluating a completed trajectory, V5 would model the instantaneous flow of value along edges. The current model takes T(π) as a completed fact; V5 would optimise trajectory in real-time.

If the UOR toroidal correspondence holds, the edge value function on a compact manifold has natural conservation laws. Value flowing along one edge must come from somewhere and go somewhere. This transforms trajectory optimisation from an unconstrained problem into a constrained one — potentially much more tractable.

## Open problems

1. Calibration of β — how much does trajectory actually contribute relative to positional terms?
2. Functional form of f(e) — how exactly are vertical transitions weighted relative to lateral?
3. Functional form of g(n_e) — diminishing, constant, or increasing returns to re-traversal?
4. Edge interaction effects — does the value of edge e depend on the presence of other edges in π?
5. Optimal trajectory planning given known f(e) and g(n_e) — is there a shortest-path-to-maximum-T(π) algorithm?
6. Empirical measurement of transition types in real agent deployments.

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
