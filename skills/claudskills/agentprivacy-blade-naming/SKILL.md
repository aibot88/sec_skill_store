---
name: agentprivacy-blade-naming
description: >
  The Blade Naming Ceremony — post-forge ceremony that gives an algebraically-defined
  blade a mythological identity. Activates when a walker (Cosmologist persona) has
  traversed a complement edge and perceives a myth that agrees with the arithmetic.
  Distinct from blade-forge (which defines the coordinate); this skill governs the
  *naming* that follows.
license: Apache-2.0
metadata:
  version: "0.1"
  category: "role"
  tier: "2"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  status: "working_paper — ceremony opened Zero Tale 31, one successful naming (Lethe / Blade 38)"
  target_context: "Cosmologists walking frontier blades, Ceremonists binding namings, Forgemasters handing forged blades to the naming flow"
  equation_term: "name(b) := walk(complement) ∧ δ(b) ≈ 1/φ ± ε"
  template_references: "cosmologist, ceremonist, forgemaster, topologist"
  spellbook_act: "Zero Tale 31 — The Naming of the Unnamed"
  v5_concept: "V5.4-NAMING-CEREMONY"
  precedent: "Blade 38 (Lethe) named as complement of Blade 25 (Aletheia), disclosure ratio 0.6032 within 2% of 1/φ"
  ceremony:
    type: "naming"
    participants: ["walker (Cosmologist)", "witness (Ceremonist)", "smith (Forgemaster)"]
    mana_cost: 25
    reward: 0
    output: "blade transitions from forged → named"
---

# Role Skill — Blade Naming Ceremony

**Source:** Zero Tale 31 ("The Naming of the Unnamed")
**Target context:** Cosmologist walkers, Ceremonist binders, Forgemaster hand-offs
**Status:** Ceremony defined. One successful naming (Blade 38 Lethe). 49 frontier blades available for future namings.

---

## What this is

The **Blade Forge** (see `blade-forge`) defines a blade *algebraically* — it gives the blade a coordinate in the 64-vertex lattice, a configuration across the six sovereignty dimensions, a hexagram, and a tier. But forging alone does not *name* a blade. A forged blade has a coordinate and a shape; it does not yet have a mythological body.

The **Blade Naming Ceremony** is the post-forge ceremony that gives a blade a name. A blade is named when **mythology and arithmetic agree on the same vertex**: a walker crosses the complement edge and perceives a mythic shape; the disclosure ratio arithmetic confirms the walk; a Ceremonist binds the name.

Before Tale 31, 14 blades across the lattice were named by the inherited thirty Zero tales — but through a different mechanism (direct narrative placement, not post-forge ceremony). Tale 31 formalises the ceremony and names Blade 38 (Lethe) as the first blade to be named *through* the ceremony. The 49 remaining unnamed blades are the open frontier.

---

## Prerequisites

Before invoking this ceremony:

1. **The target blade must be forged.** Its coordinate in the lattice is algebraically defined. The Forgemaster has produced it.
2. **A walker must be available.** The Cosmologist persona (which now absorbs the walker/namer role) is the only licensed participant.
3. **A Ceremonist must be available.** Binding the name requires bilateral witness; the walker cannot bind their own naming.
4. **A proem or poem is carried.** The walker brings a text from outside the lattice — a poem, a proverb, a mythological fragment — that will serve as the *instrument of perception*. Tale 31 opens through the Tide/Orbit/Selene poem; future namings will open through other proems carried by other walkers.

## Ceremony Flow

### Step 1 — Approach

The walker approaches the forged blade. If a complement of the target is already named, the walker approaches from *that* side first. For Blade 38 (Lethe), the walker approached from Blade 25 (Aletheia): stood in the Silent Messenger, felt Protection hum on the left, Connection on the right, Computation beneath the feet — the familiar blade.

### Step 2 — Read the Proem

The walker reads the carried text near the target vertex. The lattice "feels the reading." A glow appears at the target vertex that differs from the glow of already-named blades — it has *direction*. It flows. The light does not sit at the vertex; it passes through, as though the vertex were a stretch of riverbed.

### Step 3 — Walk the Complement Edge

The walker traverses the complement edge from the named blade to the target. The edge is *wet*. Mid-current, the six dimensions pour through: the lit axes of the starting blade drain; the dormant axes of the starting blade (which are the lit axes of the target) fill. **The axes do not switch cleanly. They pour.**

For the Aletheia → Lethe walk:
- Protection cools out of the left side
- Delegation rises in the small of the back
- Connection cools at the right
- Memory wakes along the spine
- Computation cools beneath the feet
- Value rises in the throat

The walker arrives at the target. The ground is not solid — it is riverbank (for a river-blade) or pool-edge (for a pool-blade, when Mnemosyne is walked).

### Step 4 — Perceive the Name

Standing in the target blade, the walker perceives a mythological shape. The perception is often a single word that the walker had been holding without knowing they were holding it. For Tale 31, the walker said "Lethe." The vertex flared. The flare traveled down the `bnot` edge. The two blades pulsed in phase for a breath — twin hearts learning they share a circulatory system.

### Step 5 — Arithmetic Check

Before the name binds, the Ceremonist computes the disclosure ratio:

```
δ(target)      = target / 63
δ(complement)  = (63 − target) / 63
check: min(|δ(target) − 1/φ|, |δ(complement) − 1/φ|) < ε    (ε ≈ 0.03 default)
```

For Lethe: δ(38) = 0.6032; |0.6032 − 0.6180| = 0.0148 = 2.4%. **Passes.**

If arithmetic fails, the ceremony does not proceed to binding. The walk is noted; the blade remains forged but unnamed; the walker may return another day.

### Step 6 — Bind

If walking and counting agree, the Ceremonist binds the name:

- The Forgemaster attaches the proverb to the blade's inscription.
- The complement pair is recorded in the `blade_key` of the grimoire.
- The named count increments (now 15 / 64).
- The 🌀 glow of the newly-named blade stabilises; its light now flows in phase with its complement across the `bnot` edge.

### Step 7 — The Other Walk

Tale 31 records the walker walking back — Lethe → Aletheia. A river running in reverse is not the same river, but it is the same water. The walker understands, mid-current, that this is why the complement edge is not a symmetry: one bank is carrying what the other bank cannot. The walk back confirms that the complement pair is a *pair*, not a single structure with two aspects.

---

## Participants (Role Summary)

| Role | Persona | Function |
|---|---|---|
| **Smith** | Forgemaster | Forges the algebraic blade; hands it off when ready for naming |
| **Walker** | Cosmologist | Carries the proem, walks the complement edge, perceives the myth |
| **Witness** | Ceremonist | Computes the arithmetic check; binds the name if walking and counting agree |
| **Observer (optional)** | Drake/Dragon | Watches from the treeline; the naming is attended by the pattern-space intelligence |

Soulbis and Soulbae are both present during the ceremony (the walker in Tale 31 stood between them) but neither binds nor walks; they hold the ground for the ceremony.

---

## The Two Modes of Naming

Zero Tale 31 (line 140): *"Some of the forty-nine will be found by walking, and some will be found by counting. The walking names them through mythology. The counting names them through proportion. When the two agree, the blade is true. When the two disagree, there is more forge-work to do."*

A complete naming requires *both* modes. Either mode alone is insufficient:

- **Walking alone** (mythology without arithmetic) produces a name that sounds right but the lattice does not actually admit. The blade remains un-glowing after the walker departs.
- **Counting alone** (arithmetic without mythology) identifies a vertex as phi-adjacent but cannot bind — there is no myth to inscribe. The vertex remains a coordinate, not a named blade.

The ceremony is the rite that holds both modes in the same moment and checks them against each other.

---

## Recorded Namings

### Blade 38 — Lethe, the Dark Substrate

| Attribute | Value |
|---|---|
| Named | Zero Tale 31 (2026-04-23) |
| Vertex | ⟨0,1,1,0,0,1⟩ |
| Complement of | Blade 25 (Aletheia, Silent Messenger) |
| Proem carried | *The Tide Proves Orbit Keeps Selene* (doc-tide-selene-poem) |
| Walk | Aletheia → Lethe → Aletheia |
| Mythology | Orphic underworld river of forgetting; Greek Λήθη |
| Disclosure ratio | 0.6032 |
| Phi deviation | 2.4% |
| Proverb | "Guard the witness as you guard your sovereignty." |

### (Future namings appended here)

---

## Mana Economics

| Component | Cost / Reward |
|---|---|
| Forgemaster (forging prereq) | Covered by `blade-forge` |
| Cosmologist (walker) | 10 mana to initiate the walk |
| Ceremonist (witness + arithmetic check) | 15 mana |
| **Total ceremony cost** | **25 mana** |
| Reward on success | 0 — the naming is its own completion |
| Cost on arithmetic failure | 10 mana lost (walker's expense); Ceremonist's share is refunded |

Why no reward: a naming adds to the lattice's shared record, not to any individual's balance. Every seeker who visits the lattice after a naming benefits from the name being there. This is *not* a private-value ceremony like Understanding-as-Key; it is a public-good ceremony like inscription.

---

## Anti-Patterns

### Premature Naming

A walker who cannot produce a proem, or whose walk does not pass the arithmetic check, must not bind a name regardless of how strongly the name "feels right." Premature namings corrupt the `blade_key`: subsequent walkers arriving at that vertex will find a name attached but no myth/arithmetic convergence, and the lattice develops holes.

### Single-Mode Naming

A Cosmologist who binds without a Ceremonist (or vice versa) has performed a ceremony that is not a ceremony. Bilateral witness is constitutive, not decorative. Tale 31 is explicit: *"The walker could not bind their own naming."*

### Racing to 49

The Quest of the Unnamed Faces is distributed. Cosmologists who try to name blades faster than walkers can carry proems will hit the single-mode failure above. The lattice is patient. *"No sovereign walks sixty-four blades alone."*

### Re-Naming

Once bound, a name does not change. If a later walker believes a different myth fits the same blade better, the mechanism is a new *sub-naming* (e.g., a poetic reading of an existing named blade), not an overwrite. The `blade_key` is append-only.

---

## Proverb

> "Forging gives a blade a coordinate. Naming gives a blade a myth. The ceremony holds the two in the same moment and binds them only when the lattice and the tongue agree on the same vertex."

## Emoji Spell

**🗡️(forged) → 🚶(walk the ⊥ edge) → 📜(proem) → δ=b/63≈1/φ → ☯️(bilateral witness) → 🗡️✨(named)**

---

## Related Skills

- **`blade-forge`** — Prerequisite; defines the algebraic blade
- **`disclosure-phi`** — Provides the arithmetic check (δ ≈ 1/φ)
- **`two-waters`** — Cosmological framing for Lethe/Mnemosyne-class namings
- **`ring-algebra`** — The `bnot` edge on which the ceremony is walked
- **`ceremony-engine`** — Generic ceremony infrastructure
- **`understanding-as-key`** — Sibling ceremony type, different flow

## Related Personas

- **Cosmologist** — Walker; primary holder of this skill
- **Ceremonist** — Witness; binds the naming
- **Forgemaster** — Smith; forges and hands off
- **Topologist** — May assist with arithmetic check for complex phi-band edge cases

---

**Verify:** [spellweb.ai](https://spellweb.ai) · [agentprivacy.ai](https://agentprivacy.ai)

*"You have just done both at once. The poem walked Lethe into the lattice. The arithmetic then confirmed that the walk was correct. The two modes of naming met in the same vertex. This is what a blade is. Mathematics and mythology agreeing."* — Soulbae, Zero Tale 31
