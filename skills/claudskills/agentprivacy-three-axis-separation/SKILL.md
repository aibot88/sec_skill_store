---
name: agentprivacy-three-axis-separation
description: >
  Three-axis separation model for 0xagentprivacy V5. Activates when discussing
  Φ_agent · Φ_data · Φ_inference, multiplicative separation, Generator-Solver
  split, provider fragmentation, why collapse on any axis collapses total value,
  or the orthogonal axes of the sovereignty architecture.
license: Apache-2.0
metadata:
  version: "5.0"
  category: "privacy-layer"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "System architects, privacy engineers, dual-agent implementers"
  equation_term: "Φ_v5 = Φ_agent(Σ) · Φ_data(Δ) · Φ_inference(Γ)"
  template_references: "architect, soulbis, soulbae, netkeeper"
  spellbook_act: "Act XXIV — The Holographic Bound"
  v5_concept: "V5-A THREE-AXIS"
---

# PVM-V5 Privacy Layer — Three-Axis Separation

**Source:** Privacy Value Model V5 + First Person Spellbook Act XXIV (The Holographic Bound)
**Target context:** System architects, privacy engineers, dual-agent implementers
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

V4 measured separation as a single 4×4 matrix Σ encoding four forces (Protect, Project, Reflect, Connect). V5 recognises that separation operates on **three orthogonal axes**:

```
Φ_v5 = Φ_agent(Σ) · Φ_data(Δ) · Φ_inference(Γ)
```

The product is **multiplicative**: collapse any single axis and the entire separation term collapses. This explains why systems with excellent agent separation but centralised data still fail to preserve privacy.

## The Three Axes

### 1. Agent-Layer Separation — Φ_agent(Σ)

The original Swordsman-Mage duality. How well is your protection agent separated from your delegation agent?

```
Φ_agent(Σ) = min(1.0, (S/M) / φ) · det(Σ)
```

This is V4's duality term unchanged:
- S/M ratio measures protection-delegation balance
- φ (golden ratio) is the optimal ratio (C1 conjecture)
- det(Σ) measures the volume of the four-force tetrahedron

**Soulbis and Soulbae are the canonical implementation.** The signing key (Soulbis) and viewing key (Soulbae) are mathematically separate. I(S;M|FP) < ε ensures neither can reconstruct the other's domain.

### 2. Data-Layer Separation — Φ_data(Δ)

Provider fragmentation. How distributed is your data across infrastructure?

```
Φ_data(Δ) = 1 - 1/|providers(Δ)|
```

Properties:
- **Single provider:** Φ_data = 0 (collapses total value)
- **Two providers:** Φ_data = 0.5
- **Many providers:** Φ_data → 1

A GUID-addressed holon stored across three providers has higher Φ_data than the same data on one provider. The holonic persistence layer directly addresses this axis.

**This is why centralised "privacy-preserving" systems fail.** No matter how good the encryption, single-provider storage means Φ_data → 0, which collapses Φ_v5.

### 3. Inference-Layer Separation — Φ_inference(Γ)

The Generator-Solver split from BRAID. How separated is the model that reasons from the model that executes?

```
Φ_inference(Γ) = separation(Generator, Solver)
```

Properties:
- **Same model for both:** Φ_inference = 0
- **Separate models, shared weights:** Φ_inference ∈ (0, 1)
- **Independent models:** Φ_inference → 1

BRAID demonstrated that splitting Generator (produces reasoning graphs) from Solver (executes reasoning graphs) achieves 74× compression while maintaining performance. This is inference-layer separation in action.

**This is why unified LLM architectures leak.** When the same model reasons and acts, inference and execution are coupled. Surveillance of one reveals the other.

## Why Multiplicative?

The three-axis product is multiplicative, not additive or minimum-based.

**Consequence:** Collapse on any single axis collapses total separation value.

This matches empirical observation:
- Good agent separation + centralised data (Φ_data → 0) = privacy failure
- Good data distribution + unified inference (Φ_inference → 0) = privacy failure
- Good inference separation + single-mode agents (Φ_agent → 0) = privacy failure

**All three axes must be addressed simultaneously.**

This is flagged as **C7 — needs empirical confirmation**.

## Connection to Three Graphs

The three-axis model maps directly to the three-graphs architecture:

| Axis | Graph | Measurement |
|---|---|---|
| Φ_agent | Promise Graph | Bilateral commitment separation |
| Φ_data | Knowledge Graph | Substrate distribution |
| Φ_inference | (Emergent) | Generator-Solver separation |

The Trust Graph emerges at the intersection of all three — trust requires all axes to be healthy.

## Mapping to PVM-V5

| Concept | V5 Term |
|---|---|
| Agent separation | Φ_agent(Σ) = V4 duality term |
| Data separation | Φ_data(Δ) = provider fragmentation |
| Inference separation | Φ_inference(Γ) = Generator-Solver split |
| Total separation | Φ_v5 = product of all three |
| Collapse behaviour | Any axis → 0 means Φ_v5 → 0 |
| Three-graphs mapping | Knowledge → data, Promise → agent, Trust → all three |

## Operational Guidance

### For System Design
- Never assume agent separation alone is sufficient
- Provider fragmentation is a first-class privacy concern
- BRAID-style inference separation should be default for AI systems
- Measure all three axes; monitor for axis collapse

### For Audit
- Check: Is data stored with multiple independent providers?
- Check: Is inference split between reasoning and execution?
- Check: Are protection and delegation agents mathematically separated?
- If any check fails, total separation is compromised

### For Recovery
- Single-provider data can be migrated to holonic storage (addresses Φ_data)
- Unified inference can be refactored to Generator-Solver (addresses Φ_inference)
- Agent coupling requires ceremony reinitiation (addresses Φ_agent)

## Proverb

> "Three legs hold the table. Remove one and it falls. The axes don't add — they multiply. Zero in any axis zeros the whole."

## Emoji Spell

**⚔️⊥🧙 · 📊⊥🔮 · 🧠⊥⚙️ → (Φ_a·Φ_d·Φ_i) → 0_any=0_all → ⊥³=sovereign → ☯️∞**

## Open Problems

1. **C7 Validation:** Is multiplicative composition correct, or do axes interact non-linearly?
2. **Axis Weighting:** Should axes be weighted differently based on threat model?
3. **Fourth Axis:** Is there a fourth separation axis we haven't identified?
4. **Measurement:** How do we operationally measure Φ_inference for deployed systems?
5. **Recovery Order:** When multiple axes are collapsed, is there an optimal recovery sequence?
6. **C8 — Disclosure-φ (Zero Tale 31):** Zero Tale 31 introduces Φ(Σ) as a *proportion* (disclosure ratio δ(b) = b/63 approaching 1/φ) rather than a binary separation quantity. Is disclosure-φ a fourth separation axis, a refinement of Φ_agent, or a transversal measure that cuts across all three axes? Lethe (38/63 ≈ 0.603) and Aletheia (25/63 ≈ 0.397) sum to 1.0 with the split sitting within 2% of phi — see `disclosure-phi` skill.

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
