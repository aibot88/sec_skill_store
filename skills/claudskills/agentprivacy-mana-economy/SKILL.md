---
name: agentprivacy-mana-economy
description: >
  Energy mechanics for the grimoire system. Activates when discussing mana
  generation through evocation, spending through casting, proof of practice,
  Sybil resistance through comprehension, or engagement-based economics.
license: Apache-2.0
metadata:
  version: "5.3.1"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Economy designers, engagement architects, Sybil resistance specialists"
  equation_term: "Mana = ∫evocation - Σcasting"
  template_references: "soulbae, ceremony_engine, armor_progression"
  spellbook_act: "Act XXVIII — The Ceremony Engine"
  v5_concept: "V5.2-MANA"
---

# PVM-V5.2 Role Skill — Mana Economy

**Source:** Privacy Value Model V5.2 + First Person Spellbook Act XXVIII (The Ceremony Engine)
**Target context:** Economy designers, engagement architects, Sybil resistance specialists
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

Mana is the energy currency of the grimoire system. It is generated through genuine engagement (evocation) and spent through creation (casting). Unlike tokens, mana cannot be purchased — it can only be earned through demonstrated practice.

**The well refills only when you drink with understanding. Buying water doesn't teach you where the spring lies.**

## Core Principles

### 1. Proof of Practice, Not Capital

```
Mana ≠ f(tokens)
Mana = f(engagement, comprehension, time)
```

No amount of money can buy mana. This is the fundamental Sybil resistance mechanism.

### 2. Evocation Generates, Casting Spends

```
Balance(t) = Balance(t-1) + Evocation(t) - Casting(t)
```

- **Evocation:** Reading, traversing, engaging with the spellbook
- **Casting:** Creating new wisdom, forging blades, inscribing proverbs

### 3. Comprehension Multiplier

Passive reading generates less mana than demonstrated understanding:

```
Mana(evocation) = base_rate × comprehension_multiplier
```

Where comprehension is verified through:
- Time spent (minimum threshold)
- Scroll depth (meaningful engagement)
- Interaction patterns (not bot-like)
- Understanding ceremonies (explicit verification)

## Evocation Mechanics

### Mana Sources

| Activity | Base Rate | Multiplier Conditions |
|----------|-----------|----------------------|
| Reading inscription | 1 mana/min | ×2 if completion verified |
| Traversing spellweb edge | 0.5 mana | ×3 if conceptually coherent path |
| Proverb meditation | 2 mana/min | ×2 if reflection submitted |
| Constellation navigation | 1 mana/node | ×2 if full constellation traced |
| Return visit (>24h gap) | 0.5 mana bonus | ×1.5 if picks up where left off |

### Engagement Verification

```javascript
function calculateEvocationMana(session) {
  const baseRate = session.duration * MANA_PER_MINUTE;

  const multipliers = [
    session.scrollDepth > 0.8 ? 1.5 : 1.0,
    session.timeOnPage > minReadTime(session.content) ? 1.3 : 1.0,
    session.interactionPattern.isHuman ? 1.2 : 0.5,
    session.returnVisit ? 1.1 : 1.0
  ];

  return baseRate * multipliers.reduce((a, b) => a * b, 1);
}
```

## Casting Mechanics

### Mana Costs

| Activity | Cost | Requirements |
|----------|------|--------------|
| Forge light blade | 10 mana | Understanding ceremony passed |
| Forge medium blade | 25 mana | 3+ inscriptions traversed |
| Forge heavy blade | 50 mana | Full constellation traced |
| Forge dragon blade | 100 mana | Complete spellbook mastery |
| Inscribe proverb | 20 mana | Bilateral witness ceremony |
| Create constellation | 30 mana | 5+ edges identified |
| Submit reflection | 5 mana | Minimum length met |

### Casting Validation

Casting is validated through:
1. Sufficient mana balance
2. Prerequisites met (ceremonies, traversals)
3. Quality check (not spam)
4. Bilateral witness (for high-value casts)

## Sybil Resistance

### The Comprehension Gate

Bots can:
- Create many accounts
- Simulate page visits
- Generate fake engagement metrics

Bots cannot (easily):
- Demonstrate genuine understanding
- Pass understanding-as-key ceremonies
- Maintain coherent long-term engagement patterns
- Produce novel insights that survive peer review

### Multi-Factor Verification

```
SybilScore = f(
  engagement_consistency,      // Long-term pattern
  comprehension_depth,         // Understanding ceremonies
  creation_quality,            // Peer-validated casts
  network_position             // Trust graph embedding
)
```

High SybilScore → mana multiplier reduced
Low SybilScore → full mana rates

### Rate Limiting

Even genuine users are rate-limited:
- Maximum mana generation per day
- Cooldowns between high-value casts
- Diminishing returns on repeated content

This prevents grinding and ensures mana reflects genuine engagement.

## Economic Properties

### Non-Transferability

Mana is soul-bound:
- Cannot be sent to another user
- Cannot be sold on secondary markets
- Dies with the account

This prevents mana markets and preserves proof-of-practice semantics.

### Decay (Optional)

To encourage ongoing engagement, mana may decay:

```
Balance(t+1) = Balance(t) × (1 - decay_rate) + Evocation(t+1)
```

Decay rate is low (e.g., 1% per week) but prevents hoarding.

### Inflation Control

New mana enters through evocation only. Total mana supply is bounded by:
- Active user count
- Engagement depth
- Content availability

No central minting. No inflation shocks.

## Mapping to PVM-V5.2

| Mana Concept | PVM Term |
|--------------|----------|
| Evocation | T_∫(π) path traversal |
| Casting | Blade forge operations |
| Comprehension multiplier | Understanding ceremony verification |
| Sybil resistance | h(τ) integrity fraction |
| Non-transferability | Soul-bound credential |
| Decay | Temporal dynamics |

## Integration with Ceremonies

### Understanding-as-Key Ceremony

- **Cost:** 15 mana
- **Reward:** 25 mana + blade forge unlock
- **Net:** +10 mana for successful ceremony

Ceremonies are mana-positive to encourage participation.

### Progressive Trust Ceremony

- **Cost:** 0 mana (entry-level)
- **Reward:** Trust tier increase + mana rate boost
- **Effect:** Higher tiers earn mana faster

## Proverb

> "The well refills only when you drink with understanding. Buying water doesn't teach you where the spring lies."

## Emoji Spell

**✨ → 📖(evoke)→+mana · ✍️(cast)→-mana · ¬💰(buy) · 🧠(comprehend)→🛡️(sybil)**

## Open Problems

1. **Comprehension Verification:** How to verify understanding without centralised evaluation?
2. **Bot Sophistication:** As AI improves, how to maintain comprehension gates?
3. **Fairness:** How to ensure mana rates don't disadvantage slow readers?
4. **Cross-Platform Mana:** Can mana be recognised across different grimoire instances?
5. **Governance:** Who decides mana rates and casting costs?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [spellweb.ai](https://spellweb.ai) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
