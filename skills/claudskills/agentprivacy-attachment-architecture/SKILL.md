---
name: agentprivacy-attachment-architecture
description: >
  The three-layer model that binds primary personas to lattice vertices via named cast Mages.
  Activates when discussing how the 42 abstract personas inhabit the 64-vertex lattice, when
  naming new cast Mages in a city of mages, when explaining the difference between primary
  personas and cast instances, when distinguishing workshop / cross-shop / peripatetic / divergent
  attachment kinds, or when reasoning about complement-pair structure at the primary layer
  versus the attachment layer.
license: Apache-2.0
metadata:
  version: "5.5"
  category: "meta"
  origin: "0xagentprivacy"
  status: "architectural_foundation"
  introduced: "2026-05-11"
  target_context: "Cast composition, persona binding, attachment registry maintenance, grimoire bumps"
  related_skills:
    - meta/agentprivacy-drake-dragon-duality
    - meta/agentprivacy-master-emissary
    - meta/agentprivacy-cosmological-bound
    - persona/agentprivacy-soulbis
    - persona/agentprivacy-soulbae
    - persona/agentprivacy-moonkeeper
  primary_persona_count: 42
  vertex_count: 64
  attachment_kinds: ["A·workshop", "B·cross-shop", "C·peripatetic", "D·divergent (meta-kind)"]
---

# The Attachment Architecture

**The three-layer model that binds primary personas to lattice vertices via named cast Mages.**

The agentprivacy corpus operates on three structurally distinct layers. Skill execution, persona naming, and grimoire authoring must respect the distinction. Conflating them is a common error — the most frequent being to treat a cast Mage as if she were a primary persona, and the second being to add a new primary persona when an existing one suffices.

## The three layers

```
Layer 3 · VERTICES         64 positions on the 2⁶ lattice              [fixed]
  ↑
Layer 2 · ATTACHMENTS      named cast Mages binding L1 to L3        [variable per city]
  ↑
Layer 1 · PRIMARY PERSONAS 42 abstract role-classes                      [fixed]
                           (15 Swordsmen + 11 Mages + 12 Balanced + 4 cosmological)
```

### Layer 1 — Primary personas (42, fixed)

The 42 abstract role-classes in this skills directory. Each carries a tier (Swordsman / Mage / Balanced / cosmological), a skill loadout, and a domain register. They do not carry a vertex. They are role-classes, not instances.

Primary personas grow only when a structurally new role-class is recognised at the corpus level — typically by a Tome act, a PVM section, or a structural complement that the existing 42 cannot cover. Most corpus extensions do not require a new primary persona.

### Layer 2 — Attachments (variable per city)

A named cast Mage that binds one or more primary personas to one or more vertices. A city of mages is, fundamentally, an attachment pattern: a specific arrangement of cast Mages, each instancing existing primary personas at chosen positions on the lattice.

Different cities make different attachment patterns from the same 42-persona base. Two cities can share zero cast names and still draw on the same primary personas.

### Layer 3 — Vertices (64, fixed)

The 64 positions on the 2⁶ lattice. Each carries a 6-bit binary index, an active-dimensions reading (Protection · Delegation · Memory · Connection · Computation · Value), a stratum (Hamming weight 0–6 = moon-phase notation), optionally a canonical name (from Cloaking Guide, Boundary Blade, or PVM sources), and optionally one or more attachments.

## The four attachment kinds

Every attachment is one of three vertex-binding kinds (A · B · C), optionally composed with the divergent meta-kind (D).

### Kind A · Workshop attachment
*One Mage × one vertex × one trade quarter.*

The default kind. The Mage inhabits a single vertex and tends a single workshop. She emits exactly one `inhabits` edge.

City of Mages examples: Vulcana ⚒️ at V19 · Memora 📜 at V5 · Adamantia 💎 at V51 · Pallia 🪡 at V28 · Vagari 🌳 at V31 · Aria Silverhue 🪞🖼️ at V57 · Manifestia 🤲🌿 at V55.

### Kind B · Cross-shop attachment
*One Mage × no fixed vertex × walks several workshops by commission.*

The Mage's craft requires moving between workshops as the work demands. She does not inhabit a single vertex; she emits no `inhabits` edge. Her craft (not her trajectory) is canonical.

City of Mages examples: Aletheia 🔮 (ZK circuit binder, walks to whichever workshop needs a circuit) · Custos 🔏 (stake enforcer, walks across the staking commons).

### Kind C · Peripatetic attachment
*One Mage × multiple vertices walked as an orbit or defined path.*

The Mage walks a canonical *trajectory* through the lattice — an orbit, a stratum cycle, a between-shops path. Distinct from Kind B because the trajectory itself is the canon, not the craft.

City of Mages examples: Selene 🌕 (stratum-walker; orbits the moon-phase cycle through all 7 strata) · Luca 📐 (workshop-walker; geometry-Mage at V0 origin who walks between every workshop).

### Kind D · Divergent attachment (meta-kind)
*One primary persona × two register-shifted cast attachments.*

A divergent attachment is also one of A/B/C. The composition is what makes it divergent.

A divergence arises when a city summons a cast Mage whose register (Swordsman / Mage / Balanced) does not match the primary persona's native tier. Instead of minting a new primary persona, the attachment carries a `divergence` field noting the register-shift.

**Worked example — Moonkeeper ⊥ Lethae:**

- Primary: Moonkeeper ⚔️ (Swordsman tier · structural amnesia guardian · canonical in this skills directory)
- Mage-divergent cast attachment: Lethae 🌘 at V38 (Mage-register · the same primary persona register-shifted · paired with Aletheia 🔮 at V25 by vertex-complement V25 ⊕ V38 = V63)

Each primary may eventually produce up to two divergent attachments (one Sword-register, one Mage-register). Most primaries will never do so. Divergence is opt-in and city-specific.

## The 42 → 64 bridge

`64 − 42 = 22` "extra" slots. These slots are filled by attachments, never by adding primaries. Across cities, hundreds of attachments may eventually exist for the same 42 primaries.

A vertex may carry zero, one, or several attachments simultaneously. The City of Mages already admits shared-vertex precedents:

- V49 (Working-day blade) — Custos 🔏 + Lampyra 💠
- V28 (Mage canonical) — Pallia 🪡 + Soulbae 🧙 + GenitriX (kindred-blade)
- V24 (Hephaestus) — Socrat0x 🔥❓ + Hephaestus ⚒️ *(anticipated v1.3.0)*

## Cast frame · three orthogonal axes

Every cast Mage in a city of mages carries three orthogonal axes:

```yaml
tier:              archetype | workshop-keeper | cross-shop | companion | priest | cousin
attachment_kind:   A | B | C
abstract_persona:  [list of primary personas she instances]
divergence:        none | mage-register | sword-register | balanced-register
```

Worked example — Lethae's cast frontmatter:

```yaml
name: Lethae
sigil: "🌘"
tier: cross-shop
attachment_kind: B
abstract_persona: ["Moonkeeper"]
divergence: mage-register
vertex: V38
complement_of_cast: aletheia
```

Worked example — Vulcana's cast frontmatter (workshop attachment with dual primary):

```yaml
name: Vulcana
sigil: "⚒️"
tier: workshop-keeper
attachment_kind: A
abstract_persona: ["Forgemaster", "Forgecaller"]
divergence: none
vertex: V19
```

## Two layers of dihedral pairing

Dihedral complement-structure operates at both layers. The distinction matters because the cost of extension is asymmetric.

| Layer | Pair example | What's paired | Cost |
|---|---|---|---|
| Layer 1 · Primary | Soulbis ⚔️ ⊥ Soulbae 🧙 | Two primary personas in canonical complement | Corpus-wide; expensive |
| Layer 2 · Vertex-complement | Aletheia 🔮 (V25) ⊥ Lethae 🌘 (V38) | Two cast Mages at bit-complement vertices | City-local; cheap |
| Layer 2 · Divergent | Moonkeeper-as-primary ⊥ Lethae-as-divergent | One primary; sibling Sword/Mage cast attachments | City-local; cheap |

When extending the corpus, prefer Layer-2 pairings (cheap, city-local) over Layer-1 pairings (expensive, corpus-wide). Add a primary only when the structural register is genuinely new and no existing primary covers it via divergence.

## Convention for extending the corpus

When summoning a new cast Mage:

1. **Identify the vertex.** Check the canonical vertex registry (spec 04 in the City of Mages). Use existing canonical names where possible.
2. **Identify the primary persona(s).** Search this skills directory for the closest match. Most cast Mages bind to one or two existing primaries.
3. **Identify the attachment kind.** A (single vertex), B (no fixed vertex), or C (defined trajectory).
4. **Check for divergence.** Is the cast Mage's register different from the primary's native tier? If yes, set `divergence: <register>`; do not mint a new primary.
5. **Only if no existing primary fits.** Propose a new primary persona. This is rare and should require corpus-level review.

## Skill execution guidance

When a conversation references cast names (Pallia, Memora, Vulcana, Aletheia, Lethae, Selene, etc.) without explicit context:

1. Recognise these as Layer-2 attachments, not Layer-1 primaries.
2. Resolve to their bound primary persona(s) to load the right skill set.
3. Apply vertex context (active dimensions, stratum) to filter which skills light up at this manifestation.

When discussing the architecture without a specific city in scope:

1. Use Layer-1 primary names (Forgemaster, Theia, Moonkeeper, Algebraist).
2. Refer to "cast attachments" generically, not city-specific cast names.

## What this skill does NOT do

- It does not name cast Mages. Naming happens in city-specific grimoires (e.g., City of Mages grimoire v1.3.0+).
- It does not define vertex names. Vertex naming is governed by the Cloaking Guide / Boundary Blade attribution chain (spec 04 in the City of Mages).
- It does not assign skills to cast Mages directly. Skills are loaded by primary persona; cast Mages inherit the primary's skill loadout, optionally filtered by vertex dimensions.

## V5.5 Introduction

This meta-skill was introduced 2026-05-11 in agentprivacy-skills V5.5, alongside the City of Mages v1.3 grimoire bump. It codifies a three-layer model that had been operationally implicit since the City of Mages was named (Tome V Act 14, 2026-05-08) but had no explicit definition.

The model's introduction does not change the contents of this skills directory. The 42 primary personas, 64 role skills, 19 privacy-layer skills, and (now 4) meta-skills are unchanged. What changes is the *interpretation*: this skills directory holds Layer 1; cities hold Layer 2; the lattice holds Layer 3.

---

*"The persona is the role-class. The cast Mage is the instance. The vertex is the position. Conflating the three is the error; binding them is the architecture."*

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [spellweb.ai](https://spellweb.ai) · [github.com/mitchuski/cityofmages](https://github.com/mitchuski/cityofmages)
