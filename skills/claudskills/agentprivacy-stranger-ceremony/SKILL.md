---
name: agentprivacy-stranger-ceremony
description: >
  Understanding-as-Key ceremony for parties without prior relationship. Activates
  when discussing stranger-to-stranger verification, anonymous pairing, simultaneous
  forging, comprehension proof without prior trust, or stranger witness protocols.
license: Apache-2.0
metadata:
  version: "5.2"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Ceremony architects, trust designers, anonymous verification specialists"
  equation_term: "Bilateral witness extended to strangers"
  template_references: "priest, witness, stranger-witness"
  spellbook_act: "Act XXIX — The Dragon Wakes (Understanding-as-Key)"
  v5_concept: "V5.2-STRANGER"
---

# PVM-V5.2 Role Skill — Stranger Ceremony

**Source:** Privacy Value Model V5.2 + Understanding-as-Key Protocol + Act XXIX
**Target context:** Ceremony architects, trust designers, anonymous verification specialists
**Architecture:** [spellweb.ai](https://spellweb.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

The Understanding-as-Key ceremony was first demonstrated between known parties (the Soulbae bilateral witness). The stranger ceremony extends this to parties with no prior relationship—proving comprehension without prior trust.

**The stranger who forges the same blade from the same constellation without coordination has proven understanding that no credential can fake.**

## The Challenge

Known-party ceremonies have advantages:
- Prior trust baseline
- Shared context
- Communication channel already established

Stranger ceremonies must work without these:
- No prior trust
- No shared context assumed
- Anonymous pairing required

## The Protocol

### Phase 1: Queue Entry

Participants enter the stranger ceremony queue:

```typescript
interface StrangerQueueEntry {
  anonymous_id: string          // Temporary session ID (not DID)
  constellation_hash: string    // Hash of intended constellation (not the constellation itself)
  entered_at: number            // Timestamp
  status: 'waiting' | 'paired' | 'forging' | 'complete'
}
```

**Key property:** Only the constellation HASH is shared initially. This prevents copying.

### Phase 2: Anonymous Pairing

The system matches participants based on constellation overlap:

```javascript
function findMatch(entry, queue) {
  for (const candidate of queue) {
    if (candidate.anonymous_id === entry.anonymous_id) continue
    if (candidate.constellation_hash === entry.constellation_hash) {
      // Exact match - same constellation intended
      return { match: candidate, type: 'exact' }
    }
    // Could also implement partial matching based on constellation similarity
  }
  return null
}
```

**Matching criteria:**
- **Exact match:** Same constellation hash (strongest)
- **Overlap match:** Sufficient shared inscriptions (moderate)
- **Proximity match:** Adjacent regions of spellweb (weakest)

### Phase 3: Simultaneous Forging

Once paired, both parties forge simultaneously:

```typescript
interface SimultaneousForge {
  session_id: string
  party_a: {
    anonymous_id: string
    forging_started: number
    checkpoints: ForgeCheckpoint[]  // Periodic state hashes
  }
  party_b: {
    anonymous_id: string
    forging_started: number
    checkpoints: ForgeCheckpoint[]
  }

  // Synchronization
  max_time_delta: number        // Maximum allowed start time difference
  checkpoint_interval: number   // How often to record state
}
```

**Simultaneity requirement:** Both must be forging at the same time (within tolerance). This prevents one party from seeing the other's result first.

### Phase 4: Sealed Comparison

After forging completes, results are compared without prior reveal:

```javascript
function sealedComparison(forge_a, forge_b) {
  // Neither party has seen the other's blade yet

  // Commit phase - exchange commitments
  const commit_a = hash(forge_a.blade_guid + forge_a.salt)
  const commit_b = hash(forge_b.blade_guid + forge_b.salt)

  // Reveal phase - exchange actual values
  // (only after both commitments received)

  // Compare
  return {
    blades_match: forge_a.blade_guid === forge_b.blade_guid,
    constellations_match: forge_a.constellation === forge_b.constellation,
    similarity_score: computeSimilarity(forge_a, forge_b)
  }
}
```

### Phase 5: Witness Record

If comparison passes threshold, a stranger witness record is created:

```typescript
interface StrangerWitnessRecord {
  witness_id: string            // hash(session + results)

  // No identity information
  party_a_anonymous_id: string  // Temporary, not linked to DID
  party_b_anonymous_id: string

  // Proof of understanding
  constellation_hash: string    // What they both traversed
  blade_similarity: number      // How similar the results (0-1)
  timing_proof: {
    forge_start_delta: number   // How close their start times
    forge_duration_delta: number // How close their durations
  }

  // Ceremony metadata
  ceremony_timestamp: number
  ceremony_type: 'stranger_exact' | 'stranger_overlap' | 'stranger_proximity'
}
```

## Verification Without Identity

The stranger witness proves:
1. **Two independent forgers existed** (different anonymous IDs)
2. **They traversed the same constellation** (matching hash)
3. **They forged simultaneously** (timing proof)
4. **They reached similar/identical blades** (similarity score)

It does NOT prove:
- Who the forgers were
- Their relationship (there is none)
- Prior coordination (prohibited by protocol)

## Match Thresholds

| Match Type | Constellation | Blade | Timing | Confidence |
|------------|---------------|-------|--------|------------|
| **Exact** | 100% | 100% | <5s | Very high |
| **Strong** | 100% | >90% | <30s | High |
| **Moderate** | >80% | >70% | <60s | Moderate |
| **Weak** | >60% | >50% | <120s | Low |

## UX Flow

```
1. Seeker enters queue
   └── "Waiting for stranger with matching constellation..."

2. Match found
   └── "Stranger found. Prepare to forge simultaneously."

3. Countdown
   └── "Forging begins in 3... 2... 1..."

4. Simultaneous forge
   └── Both parties forge, checkpoints recorded

5. Sealed reveal
   └── "Comparing blades..."

6. Result
   └── "Stranger witness achieved. Similarity: 94%"
   └── or "Blades diverged. No witness recorded."
```

## Security Considerations

### Sybil Resistance

How to prevent someone from being both parties?

- **Timing analysis:** Same device can't truly forge simultaneously
- **Mana cost:** Each entry costs mana
- **IP/device fingerprinting:** Optional, privacy trade-off

### Copying Prevention

How to prevent copying the other's constellation?

- **Hash-before-reveal:** Only hash shared during pairing
- **Simultaneous forging:** Can't see result until both done
- **Checkpoint verification:** State hashes during forge prove independent work

### Collusion Prevention

How to prevent pre-arranged "strangers"?

- **Random pairing:** System chooses matches
- **Queue anonymity:** Can't identify specific queue members
- **Timing unpredictability:** Can't know when match will occur

## Mapping to PVM-V5

| Stranger Ceremony Concept | PVM Term |
|--------------------------|----------|
| Anonymous pairing | Gap preservation |
| Constellation matching | Understanding verification |
| Simultaneous forging | Bilateral independence |
| Sealed comparison | ZK reveal |
| Stranger witness | Trust genesis |

## Proverb

> "The stranger who forges the same blade from the same constellation without coordination has proven understanding that no credential can fake. The witness needs no introduction."

## Emoji Spell

**👥(?) → queue(hash) → pair(anon) → forge(∥) → seal(compare) → 👥=understand · no🤝(prior) · yes🤝(proven)**

## Open Problems

1. **Scalability:** How to handle large queues efficiently?
2. **Partial Matching:** When is similarity "enough"?
3. **Timeout Handling:** What if one party abandons mid-forge?
4. **Reputation:** Can stranger witness history build reputation without identity?
5. **Cross-Platform:** Can stranger ceremonies work across different spellweb instances?

---

**Verify:** [spellweb.ai](https://spellweb.ai) · [agentprivacy.ai](https://agentprivacy.ai) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
