---
name: agentprivacy-pretext-measurement
description: >
  DOM-free text measurement technique for privacy-preserving browser interactions.
  Activates when discussing pretext discovery, shadow measurement, orb mechanics,
  text property extraction without DOM access, or browser-layer privacy.
license: Apache-2.0
metadata:
  version: "5.3.1"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  target_context: "Browser extension developers, privacy engineers, measurement specialists"
  equation_term: "Pretext = measure(text) where DOM ⊥ measurement"
  template_references: "soulbae, swordsman_browser, ceremony_engine"
  spellbook_act: "Act XXVIII — The Ceremony Engine"
  v5_concept: "V5.2-PRETEXT"
---

# PVM-V5.2 Role Skill — Pretext Measurement

**Source:** Privacy Value Model V5.2 + First Person Spellbook Act XXVIII (The Ceremony Engine)
**Target context:** Browser extension developers, privacy engineers, measurement specialists
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

Pretext measurement is a technique for extracting text properties without accessing DOM content. The measurement touches the shadow, not the surface. It knows the weight without reading the words.

**The shadow tells you the height without climbing the tower. The orb measures the text without reading the words.**

This enables privacy-preserving interactions where:
- Text properties are needed (length, structure, patterns)
- Text content must remain private
- DOM access would leak information

## The Measurement Problem

### Traditional Approach (Privacy-Leaking)

```javascript
// This reads the content
const text = document.getElementById('content').innerText;
const length = text.length;
const wordCount = text.split(' ').length;
// Content is now in memory, accessible, loggable
```

### Pretext Approach (Privacy-Preserving)

```javascript
// This measures without reading
const pretext = measurePretext(element);
// pretext.length exists
// pretext.wordCount exists
// pretext.content does NOT exist
```

## Shadow Measurement Technique

### Principle

The DOM casts shadows through:
- Computed styles (width, height)
- Scroll dimensions
- Selection ranges
- Intersection observations

These shadows reveal properties without exposing content.

### Implementation Sketch

```javascript
function measurePretext(element) {
  // Create measurement probe
  const probe = document.createElement('div');
  probe.style.cssText = `
    position: absolute;
    visibility: hidden;
    white-space: pre-wrap;
    font: inherit;
  `;

  // Mirror element's text styling
  const computed = getComputedStyle(element);
  probe.style.width = computed.width;
  probe.style.font = computed.font;
  probe.style.letterSpacing = computed.letterSpacing;

  // Measure shadow (scroll dimensions indicate content size)
  // WITHOUT reading innerText
  const metrics = {
    scrollHeight: element.scrollHeight,
    scrollWidth: element.scrollWidth,
    lineHeight: parseFloat(computed.lineHeight),
    charWidth: measureCharWidth(computed.font)
  };

  // Derive properties from shadow
  return {
    estimatedLines: Math.ceil(metrics.scrollHeight / metrics.lineHeight),
    estimatedChars: Math.ceil(metrics.scrollWidth / metrics.charWidth),
    hasOverflow: element.scrollHeight > element.clientHeight,
    // Content is NEVER accessed
  };
}
```

## The Pretext Orb

The orb is the visual representation of pretext measurement:

```
     ╭──────────╮
    ╱   📊      ╲
   │  Metrics   │
   │  without   │
   │  Content   │
    ╲   🔮      ╱
     ╰──────────╯
```

### Orb Properties

| Property | Derived From | Content Access |
|----------|--------------|----------------|
| `estimatedLength` | Scroll dimensions | No |
| `lineCount` | Height / line-height | No |
| `hasStructure` | DOM child count | No |
| `complexityScore` | Tag variety | No |
| `languageHint` | Direction, font features | No |

### Orb Limitations

The orb cannot determine:
- Actual text content
- Specific words
- Semantic meaning
- Named entities

This is by design. The limitation IS the feature.

## Use Cases

### 1. Progressive Disclosure Check

Before revealing content, check if the reader has spent enough time:

```javascript
const pretext = measurePretext(article);
const estimatedReadTime = pretext.estimatedChars / 200; // 200 wpm
const actualTimeSpent = getTimeOnPage();

if (actualTimeSpent >= estimatedReadTime * 0.8) {
  // Reader likely read the content
  unlockNextSection();
}
```

### 2. Mana Calculation

Mana earned depends on content engagement without reading content:

```javascript
const pretext = measurePretext(spellbookPage);
const engagementScore = calculateEngagement(pretext, scrollDepth, timeSpent);
const manaEarned = engagementScore * MANA_RATE;
```

### 3. Ceremony Verification

Verify understanding ceremony without accessing submission:

```javascript
const originalPretext = measurePretext(originalContent);
const responsePretext = measurePretext(userResponse);

// Check structural similarity without reading either
if (responsePretext.complexity >= originalPretext.complexity * 0.7) {
  // Response demonstrates engagement
  proceedToCeremony();
}
```

## Security Properties

### What Pretext Protects Against

- Content logging by measurement code
- Content exfiltration through metrics API
- Side-channel content reconstruction (within limits)

### What Pretext Does NOT Protect Against

- Timing attacks on specific content patterns
- High-precision scroll position analysis
- Intersection observer abuse with fine targets

### Threat Model

Pretext assumes:
- Measurement code is potentially untrusted
- Content must remain in DOM (visible to user)
- Approximate properties are acceptable

## Mapping to PVM-V5.2

| Pretext Concept | PVM Term |
|-----------------|----------|
| Shadow measurement | Bounded leakage |
| Content isolation | Three-axis separation |
| Orb properties | Compressed representation |
| DOM perpendicularity | Φ_data separation |
| Engagement scoring | T_∫(π) contribution |

## Proverb

> "The shadow tells you the height without climbing the tower. The orb measures the text without reading the words."

## Emoji Spell

**📐⊥DOM → 📏(text) → weight(shadow) → measure·¬touch → 🔮(orb)**

## Open Problems

1. **Measurement Precision:** How precise can shadow measurement get before it leaks content?
2. **Cross-Browser Consistency:** Do shadow measurements work consistently across browsers?
3. **Dynamic Content:** How to handle content that changes during measurement?
4. **Adversarial Content:** Can content be crafted to fool pretext measurement?
5. **Formal Guarantees:** Can we prove information-theoretic bounds on pretext leakage?

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [spellweb.ai](https://spellweb.ai) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
