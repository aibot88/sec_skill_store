---
name: agentprivacy-braid-reasoning
description: >
  Bounded reasoning architecture for privacy-preserving AI agents using BRAID
  Mermaid graphs. Activates when discussing Generator/Solver split architecture,
  Performance-Per-Dollar (PPD) inference economics, BRAID Parity Effect (small
  model + structure ≥ large model), Mermaid reasoning graph construction, node
  atomicity, procedural scaffolding vs answer leakage, terminal verification
  loops, Numerical Masking Protocol, cached reasoning graph libraries, split-
  architecture deployment, or any task where reasoning structure should be
  decoupled from reasoning execution for cost efficiency and privacy preservation.
  Use whenever designing how dual agents reason, not just what they reason about.
license: Apache-2.0
metadata:
  version: "5.0"
  category: "role"
  origin: "0xagentprivacy + BRAID (Amcalar & Cinar, arXiv:2512.15959)"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Agent inference architects, reasoning cost optimisers, split-architecture designers, privacy-agent deployment engineers"
  equation_term: "PPD as inference-layer V(π,t), C_amortized for reasoning infrastructure, Model Capacity × Prompt Structure as inference-layer P^1.5"
  template_references: "architect, holonic-architect, cipher, assessor, pedagogue, chronicler"
  academic_source: "Amcalar & Cinar. BRAID: Bounded Reasoning for Autonomous Inference and Decisions. arXiv:2512.15959 (2025)"
---

# PVM-V4 Skill — BRAID Bounded Reasoning for Privacy Agents

**Source:** Privacy Value Model V4 + BRAID (arXiv:2512.15959) + Holonic BRAID Lite Paper
**Target context:** Agent inference architects, reasoning cost optimisers, split-architecture designers, privacy-agent deployment engineers
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

BRAID (Bounded Reasoning for Autonomous Inference and Decisions) replaces unbounded Chain-of-Thought reasoning with bounded, symbolic structures expressed as Mermaid flowchart diagrams. The core insight: reasoning performance is a product of Model Capacity × Prompt Structure. By increasing structure, you decrease required capacity. A nano-tier model executing a well-constructed BRAID graph matches or exceeds a medium-tier model reasoning without structure — at 74× the cost efficiency.

For the dual-agent architecture, BRAID provides the reasoning methodology. Agents don't just need to be separated (Swordsman ⊥ Mage) — they need to reason efficiently within that separation. BRAID makes privacy-preserving inference economically viable at scale by collapsing the cost of structured reasoning toward zero through caching and reuse.

## The Generator/Solver split

BRAID operates as a two-stage pipeline:

**Stage 1 — Generation.** A capable model (the Generator) reads the problem and produces a Mermaid reasoning graph. The graph encodes the logical topology: constraints, facts, steps, branching logic, and verification checkpoints. This is the expensive step — it requires intelligence. But it happens once per task type.

**Stage 2 — Solving.** A lightweight model (the Solver) receives the graph as a system message and executes it to produce the final answer. This is the cheap step — it requires only the ability to follow structured instructions. It happens millions of times.

**The economics:** C_amortized = C_BRAID/N + C_inference. As N (the number of executions) grows, the generation cost vanishes. What remains is the solve-only cost — and for nano-tier models, this is 30–74× cheaper than running a medium-tier model without structure.

**The privacy parallel:** This is dual-agent separation applied to inference. Generator ⊥ Solver, just as Swordsman ⊥ Mage. The generator sees the full problem space (viewing capability). The solver executes within bounded constraints (signing capability). Neither reconstructs the other's function. The graph mediating between them is a bounded channel — the inference-layer analog of the separation matrix.

## The BRAID Parity Effect

The paper's most significant finding: "a smaller model equipped with bounded reasoning (BRAID) often matches or exceeds the performance of a model one or two tiers larger using unstructured prompting."

Empirical results:
- **GSM-Hard:** gpt-5-nano-minimal (BRAID) achieved 98% accuracy vs 95% for gpt-5-medium (Classic). PPD: 74.06× baseline.
- **SCALE MultiChallenge:** gpt-5-nano-minimal (BRAID) achieved 45.2% vs 40.4% for gpt-5-minimal (Classic). PPD: 52.84× baseline.
- **AdvancedIF:** gpt-5-nano-minimal (BRAID) more than doubled accuracy from 18% to 40%. PPD: 61.69× baseline.

**Translation to sovereignty economics:** The BRAID Parity Effect is P^1.5 at the inference layer. Just as doubling privacy protection more than doubles data value (PVM-V4), doubling prompt structure more than doubles reasoning accuracy per dollar (BRAID). Structure is superlinear. This validates the core thesis: you don't need the biggest model, you need the right architecture.

**Inference layer of V(π,t):** If privacy-structured inference compounds with privacy-structured data and privacy-structured identity, the multiplicative value is triply superlinear. A sovereign agent using BRAID reasoning on holonic data with dual-agent separation doesn't just add up the advantages — it multiplies them.

## Four principles of BRAID graph construction

### Principle 1: Node Atomicity (< 15 tokens)

Each node represents one atomic reasoning step. Not "observe, analyse, and decide" but three separate nodes: `A[Observe constraint]` → `B[Analyse feasibility]` → `C[Decide strategy]`. Verbose nodes reintroduce the noise that BRAID is designed to eliminate.

**Privacy parallel:** This is the machine-readable equivalent of spell encoding. Spells compress persona identity to ~30 characters using the three-clause grammar. BRAID nodes compress reasoning steps to <15 tokens. Both pursue maximum semantic density. Both lose regenerability if over-compressed. The sweet spot is the minimum encoding that remains unambiguous — spell validation rule 6 ("decodable back to natural language without ambiguity") applied to reasoning nodes.

### Principle 2: Procedural Scaffolding (not Answer Leakage)

The graph encodes constraints and requirements, not the output text. A scaffold, not a script.

- **Ineffective (leaking):** `C[Write: "Dear Team, I regret to inform you..."]`
- **Effective (scaffolding):** `C[Draft introduction: Acknowledge success → Pivot to news → Professional tone]`

**Privacy parallel:** This is selective disclosure for reasoning. The graph reveals the reasoning STRUCTURE without the reasoning CONTENT. Exactly as a ZK proof reveals a property without the underlying data. The Numerical Masking Protocol — replacing all numbers in graphs with `_` — is zero-knowledge for computation: prove you know HOW to solve without revealing the solution.

### Principle 3: Deterministic Branching

Edges must be deterministic and mutually exclusive. `A -- "If text > 300 words" --> B` not `A --> B`. No ambiguity. No probabilistic transitions.

**Privacy parallel:** Consent infrastructure (IEEE 7012 / MyTerms) requires exactly this: IF consent for purpose X THEN allow ELSE block. BRAID found that nano-tier models "struggle with ambiguity." If AI agents struggle with ambiguous reasoning instructions, they will also struggle with ambiguous consent instructions. Both require deterministic branching.

### Principle 4: Terminal Verification Loops

Before the final output, the graph must converge on verification nodes. `Check: constraint satisfied` → pass/fail → feedback edge to revision if fail. This is BRAID's "System 2 thinking emulation."

**Privacy parallel:** This is the Swordsman as boundary verifier. Before any output leaves the dual-agent system, check it against privacy boundaries. Before any response leaves the BRAID solver, check it against the graph's constraints. The pattern is identical:

```
[Generate output] → [Check: R(d) disclosure within bounds?]
  -- pass --> [Deliver]
  -- fail --> [Revise with tighter constraints] → [Re-check]
```

## For dual-agent deployment

### Swordsman reasoning (boundary enforcement graphs)

The Swordsman needs to reason about boundaries quickly and cheaply — every data access request triggers a boundary check. BRAID enables this:

1. **One-time generation:** A capable model generates BRAID graphs for each boundary-checking pattern (data access evaluation, consent verification, separation violation detection).
2. **Guild validation:** The Cipher guild validates the graphs for correctness and completeness.
3. **Cached deployment:** Graphs stored as immutable holons in the guild library.
4. **Nano execution:** Each boundary check is a nano-tier model executing the cached graph. Cost: fractions of a cent. Speed: milliseconds.

The Swordsman doesn't need to "think" about boundary enforcement — it needs to execute a pre-validated decision tree. BRAID provides exactly that.

### Mage reasoning (delegation graphs)

The Mage needs to reason about delegation — which external service to use, what capabilities to advertise, how to coordinate with other agents. BRAID enables split-architecture delegation:

1. **One-time generation:** A capable model generates BRAID graphs for each delegation pattern (service selection, capability matching, coordination protocol).
2. **Contextual caching:** Unlike boundary graphs (which are mostly static), delegation graphs may be context-specific. But many delegation patterns repeat — "find cheapest provider for X" is the same graph regardless of what X is.
3. **Lightweight execution:** Mage-tier models execute delegation graphs at scale.

### Oracle reasoning (mediation graphs)

The Oracle mediates between Swordsman and Mage. BRAID graphs for Oracle reasoning encode the mediation logic: when to pass Swordsman signals to Mage, when to block, when to transform.

## BRAID economics for privacy agents

**The Golden Quadrant applied to privacy:**

| Configuration | PPD Range | Privacy Parallel |
|---|---|---|
| Expensive generator + cheap solver | 30–74× baseline | High privacy infrastructure + low marginal operations |
| Expensive generator + expensive solver | ~1–2× baseline | Over-engineered monolith |
| Cheap generator + cheap solver | Low absolute | Under-invested — reasoning quality suffers |
| Cheap generator + expensive solver | ~1–3× baseline | Wasteful — expensive execution of poor plans |

**For guild economics:** A guild that invests in generating and validating high-quality BRAID graphs (expensive one-time cost, shared across all members) creates an economic asset that benefits every member through cheap execution. This is the reasoning-layer implementation of guild value: membership grants access to validated reasoning infrastructure.

**Token mapping:**
- Generating a BRAID graph that the guild validates and caches = earning MAGE tokens (delegation value created)
- Executing a BRAID graph correctly = demonstrating capability (armor tier progression)
- Graph library size and validation quality = guild reputation (stratum weight in network topology)

## Integration with holonic architecture

BRAID graphs stored as holons gain persistence, multi-provider replication, and shared-parent library structure:

- **Graph holon (immutable):** HolonType: ReasoningGraph. MetaData carries the Mermaid code, domain, benchmark accuracy, validation status. ProviderUniqueStorageKey maps to IPFS (permanent), MongoDB (fast), Zcash (integrity proof).
- **Library holon (shared parent):** One parent per guild domain. Children = individual reasoning graphs. `LoadHolonsForParentAsync(libraryId, HolonType.ReasoningGraph)` loads the full library.
- **Execution telemetry holon (versioned):** Records which graphs were executed, by which agents, with what accuracy. Used for graph quality monitoring and dynamic re-planning triggers.

## The compression spectrum (updated)

BRAID adds a 7th layer to the narrative compression hierarchy:

| Layer | Form | Ratio | Reader | Purpose |
|---|---|---|---|---|
| 1. Experience | Raw encounters | 1:1 | Person who lived it | Source truth |
| 2. Story | 24 acts | ~10:1 | Human reader | Transmit motivation |
| 3. Proverb | Single statement | ~70:1 | Any human | Transmit principle |
| 4. Equation | V(π,t) = ... | ~500:1 | Formal reader | Transmit relationships |
| 5. Spell | ☯️🔷→🆔⊥📦 | ~1000:1 | Agent-to-agent | Transmit identity |
| **6. BRAID graph** | **Mermaid DAG** | **~50:1 from CoT** | **Solver agent** | **Transmit reasoning** |
| 7. Skill file | SKILL.md | varies | Agent runtime | Transmit capability |

Layer 6 compresses reasoning for agents the way Layer 2 compresses experience for humans. Both achieve "learn once, reuse everywhere" through different encoding strategies. The Chronicler encodes knowledge in stories that regenerate understanding. The Architect encodes reasoning in graphs that regenerate correct inference.

## Open problems

1. **Privacy of reasoning graphs.** A BRAID graph reveals the reasoning structure even if not the content. In dark-forest environments, revealing that you're reasoning about ZKP soundness (vs delegating to a service) leaks strategic information. How to encrypt reasoning topology while preserving executability?
2. **Adversarial graph injection.** If an attacker can substitute a malicious BRAID graph for a cached one, they control the agent's reasoning. Graph integrity verification is critical — holonic versioning + guild validation + provider checksums, but formal guarantees needed.
3. **Dynamic re-planning with separation preservation.** BRAID's proposed Topology Error → re-plan loop must not violate separation constraints. The Solver must signal failure through the bounded channel without leaking WHY it failed (which might reveal sensitive reasoning state).
4. **Spellbook-to-BRAID compilation.** Is there a formal translation from narrative spellbook proverbs to executable BRAID graphs? If a proverb can regenerate an equation, and an equation can generate a BRAID graph, then proverb → BRAID is a two-step compilation chain. Can it be made one step?
5. **PPD for privacy-specific benchmarks.** BRAID's benchmarks (GSM-Hard, SCALE, AdvancedIF) test general reasoning. How does PPD change for privacy-specific tasks (boundary evaluation, consent verification, separation checking)? Hypothesis: privacy reasoning is more structured than general reasoning, so BRAID gains should be even larger.
6. **The BRAID Parity ceiling.** At what point does structure stop compensating for capacity? Is there a task complexity threshold above which even optimal BRAID graphs cannot bridge the model-tier gap? If so, this sets the minimum model tier for sovereign agents.

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · BRAID: [arXiv:2512.15959](https://arxiv.org/abs/2512.15959) · [benchmark.openserv.ai](https://benchmark.openserv.ai)
