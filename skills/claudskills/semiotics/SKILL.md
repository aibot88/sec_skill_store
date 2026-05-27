---
name: semiotics
description: "Use when designing or auditing icon systems, colors/badges/shapes, visual metaphors, interface signs, or naming-plus-visual surfaces that users misread. Covers semiotic reasoning across icon/index/symbol, signifier/signified, denotation/connotation/myth, color/shape/position/iconography, affordances, code/API signifiers, and semiotic-coherence audits. Do NOT use for actual UI wording (use `microcopy`), palette/typography craft (use `visual-design-foundations`), accessibility or contrast compliance (use `a11y`), formal class hierarchies, or word morphology rules."
license: MIT
compatibility: "Stack-agnostic sign-system analysis. The Peirce / Saussure / Barthes models, color-as-sign rules, iconography principles, and affordance taxonomy apply to any UI; example surfaces use generic e-commerce framings — substitute the equivalents from your domain."
allowed-tools: Read Grep
metadata:
  schema_version: "4"
  version: "1.0.0"
  type: capability
  category: knowledge
  domain: design/ux
  scope: portable
  owner: skill-graph-maintainer
  freshness: "2026-05-06"
  drift_check: "{\"last_verified\":\"2026-05-06\"}"
  eval_artifacts: present
  eval_state: unverified
  routing_eval: absent
  stability: experimental
  keywords: "[\"sign-system analysis\",\"icon polysemy\",\"signifier signified mapping\",\"denotation versus connotation\",\"affordance signifier match\",\"icon-index-symbol trichotomy\",\"visual metaphor clarity\",\"color connotation audit\",\"cross-surface sign drift\",\"semiotic coherence audit\",\"anti-affordance design\",\"icon-system consistency\",\"abstract-mark opacity\",\"sign-conflict detection\",\"visual-meaning audit\",\"code-and-api semiotics\"]"
  examples: "[\"our dashboard uses green for both revenue increase and cost increase, so users read both as good — what semiotic failure is that and how should we correct it?\",\"we use a gear icon for settings on one page and preferences on another — is this just a naming issue, or an interface sign conflict?\",\"a disabled button still looks clickable because only the color changed — which signifier or affordance rule is failing?\",\"we need an icon for reconciliation in a financial workflow — which metaphors are available, and when must text stay paired with the icon?\",\"an API function is named processData() — from a sign-system perspective, what is wrong with that name?\",\"audit this status-badge color system for denotation vs connotation conflicts\",\"explain why users keep clicking a non-interactive label that looks like a link\"]"
  anti_examples: "[\"I need formal class hierarchies, axioms, and what-exists rules for our knowledge base\",\"I need physical database schema design and relationship constraints\",\"I need the relation type between two concepts — synonymy, polysemy, or meronymy\",\"draft the exact wording for a button label or tooltip after the sign system is chosen\",\"give me the live color-token values, APCA contrast math, and palette enforcement\",\"explain the morphology rule behind verb-first function names\"]"
  relations: "{\"boundary\":[{\"skill\":\"semantics\",\"reason\":\"semantics owns meaning encoding for individual textual identifiers and signals (function names, design tokens, HTTP status codes, branded types, SemVer, conventional commits); semiotics owns sign-system analysis for visual + textual sign systems (icons, color as sign, affordances, signifier/signified mappings) — the same 'what does this mean?' prompt routes by whether the trigger is one identifier's encoding or a multi-channel sign system\"},{\"skill\":\"microcopy\",\"reason\":\"microcopy owns the actual UI wording (button labels, empty states, tooltips, dialogs); semiotics owns the sign-system reasoning that determines what the words and accompanying visual signs should communicate — the same 'fix this UI element' prompt routes by whether the trigger is the wording itself or the sign system the wording sits inside\"},{\"skill\":\"semantic-relations\",\"reason\":\"semantic-relations owns the typed connections between concepts (IS-A, PART-OF, thematic roles); semiotics owns the signifier-to-signified mapping in interface and naming surfaces — the same 'how does this relate to that?' prompt routes by whether the trigger is a conceptual relation type or a sign-system relationship\"},{\"skill\":\"visual-design-foundations\",\"reason\":\"visual-design-foundations owns visual craft decisions such as palette, type, spacing, and hierarchy; semiotics owns what those signs communicate\"}],\"related\":[\"linguistics\",\"a11y\",\"intent-recognition\",\"visual-design-foundations\"],\"verify_with\":[\"a11y\",\"code-review\"]}"
  portability: "{\"readiness\":\"scripted\",\"targets\":[\"skill-md\"]}"
  lifecycle: "{\"stale_after_days\":365,\"review_cadence\":\"quarterly\"}"
  skill_graph_source_repo: "https://github.com/jacob-balslev/skill-graph"
  skill_graph_protocol: Skill Metadata Protocol v3
  skill_graph_project: Skill Graph
  skill_graph_canonical_skill: skills/semiotics/SKILL.md
---

# Semiotics

## Coverage

Semiotic analysis as the study of sign systems in software interfaces and communication. Covers:

- **Foundational models** — Peirce's icon / index / symbol trichotomy; Saussure's signifier / signified dyad; Barthes' denotation / connotation / myth layers
- **Visual semiotics for interfaces** — color as sign (denotation + connotation, with the never-color-alone rule), shape and position as sign channels (top-left, top-right, bottom-right, circle, triangle, pill)
- **Iconography as a sign system** — consistency, metaphor clarity, pairing rules, system coherence; common breakdowns (icon polysemy, opacity, cultural collision, obsolete metaphor)
- **Affordance theory** — real affordance, perceived affordance, signifier, anti-affordance; the rule that disabled states need a strong anti-affordance
- **Code and API semiotics** — naming, variable, endpoint, and error-message signs; the rule that vague names like `processData()` are signifier failures even when the implementation works
- **Semiotic-coherence audit** — the checklist for reviewing a surface across color, icon, affordance, and cross-surface consistency

The skill operates *above* microcopy execution and color-token math, and *below* formal ontology. It owns the question "what does this sign communicate to a user?", not "what should the button say?", "what hex value is this?", or "what class hierarchy do these things belong to?".

## Philosophy

Every interface element is already communicating, whether the designer intended it to or not. Semiotics exists to make that communication explicit and coherent. A button that looks clickable but is disabled, a green badge that signals "good" when the metric is actually worsening, or a gear icon that means different things on different pages are not visual quirks; they are sign failures that erode user trust one micro-misread at a time.

The core rule is: **one signifier should point clearly to one intended signified within a given system context.** The more a sign drifts, the more users (and agents) are forced to infer meaning from guesswork rather than from the system itself. Sign drift compounds — a single ambiguous icon is a small cost; ten ambiguous icons across a product is a learned distrust of the entire surface.

This skill is sign *analysis*, not visual *craft*. It tells you whether a sign communicates the right meaning. It does not tell you how to lay out the screen, what hex value to use, what class hierarchy to formalize, or what wording to put on a button. Each of those belongs to a different skill in the design / language / data cluster.

## When to Use

- Designing or auditing icon systems
- Checking whether a color, badge, or shape communicates the wrong judgment
- Explaining why users misread a button, state, or symbol
- Choosing or critiquing visual metaphors for abstract concepts
- Auditing naming and interface signs together when a surface feels semantically off

---

## 1. Foundations — How Signs Work

### Peirce's Trichotomy

| Sign type | Relationship to meaning | UI example | Strength |
|-----------|------------------------|------------|----------|
| **Icon** | Resembles what it represents | Magnifying glass = search | Intuitive but culturally variable |
| **Index** | Causally connected to meaning | Loading spinner = something is happening | Direct but context-dependent |
| **Symbol** | Arbitrary convention | Red = danger, hamburger = menu | Efficient once learned |

Rules:

- Prefer icons for first-use discoverability.
- Prefer symbols for expert fluency when the convention is already learned.
- Use indexes when the system needs to signal that a process or state is actively occurring.

### Saussure's Dyad

| Component | Definition | Application |
|-----------|-----------|-------------|
| **Signifier** | The perceivable form | Color, shape, text, icon, animation |
| **Signified** | The concept or meaning | Action, state, category, judgment |

Rules:

- The same signifier should not point to multiple signifieds within one product surface unless that ambiguity is deliberate and documented.
- Changing the signifier can break learned meaning even if the redesign seems visually improved.

### Barthes' Three Layers

| Layer | What it is | Example |
|-------|-----------|---------|
| **Denotation** | Literal reading | Up arrow = increase |
| **Connotation** | Associated judgment / cultural meaning | Green = positive / good |
| **Myth** | Systemic or ideological framing | Growth as inherently desirable |

Rules:

- Separate direction from judgment in financial UI. An *increase* is not always *good*.
- A sign can be denotationally correct while still semantically wrong because the connotation misleads.

---

## 2. Visual Semiotics for Interfaces

### Color as Sign

| Color | Common denotation | Common connotation | Risk |
|-------|-------------------|--------------------|------|
| Red | Error, stop, danger | Bad, urgent, loss | Overuse dulls alarm meaning |
| Green | Success, active, up | Good, growth, healthy | Wrong when used for *undesirable* increases |
| Yellow / Amber | Warning, caution | Attention needed | Easily confused with error |
| Blue | Information, trust, link | Calm, corporate, neutral authority | Can become semantically empty if overused |
| Grey | Inactive, secondary, disabled | Neutral, quiet | May fail as an anti-affordance if too subtle |

Rules:

- Color should not be the *only* sign channel for important meaning.
- Audit color decisions at both denotation and connotation levels.
- Live token values, contrast compliance, and visual craft belong to `a11y` or `visual-design-foundations`; semiotics evaluates only whether the *sign* itself is coherent.

### Shape and Position as Sign

| Sign channel | Common reading |
|--------------|----------------|
| Top-left placement | Primary or first-scanned element |
| Top-right placement | Tools, account, utility actions |
| Bottom-right placement | Primary CTA in a dialog |
| Circle | Status, avatar, completion |
| Triangle / arrow | Direction, expansion, movement |
| Pill / badge | Category, state, count |

Rules:

- Position and shape carry meaning even without text; treat them as part of the sign system.
- If a layout or component breaks a strong convention, ensure the surrounding cues are strong enough to retrain the interpretation.

---

## 3. Iconography as a Sign System

| Principle | Rule |
|-----------|------|
| **Consistency** | Same concept = same icon across the product |
| **Metaphor clarity** | The metaphor should be legible without specialist training |
| **Pairing** | Abstract or unfamiliar icons need text pairing until learned |
| **System coherence** | Use one icon family unless there is a compelling reason not to |

Common breakdowns:

- **Icon polysemy** — one icon means several things
- **Opacity** — abstract mark with no clear signified
- **Cultural collision** — metaphor fails outside one audience's assumptions
- **Obsolete metaphor** — the convention is still learned by some but dead to others (e.g., the floppy-disk save icon)

---

## 4. Affordance Theory

| Concept | Application |
|---------|-------------|
| **Real affordance** | What the element can actually do |
| **Perceived affordance** | What the element appears to allow |
| **Signifier** | The cue that tells the user action is possible |
| **Anti-affordance** | The cue that tells the user action is *not* possible |

Rules:

- If an element looks interactive, it should be interactive.
- Disabled states need a strong anti-affordance, not just a mild color change.
- Semiotic failures most often appear when the signifier and the true affordance disagree.

---

## 5. Code and API Semiotics

Semiotics also applies to textual and code-facing signs.

| Sign surface | Semiotic question |
|--------------|-------------------|
| Function name | Does the signifier actually tell me what the behavior is? |
| Variable name | Does the label point clearly to the value's meaning? |
| API endpoint | Does the route name communicate the resource / action correctly? |
| Error message | Does it communicate both what happened and how to respond? |

**Rule**: a vague name like `processData()` is a signifier failure even when the implementation works. The reader has to *open the function* to learn its meaning — which is exactly the inference cost a good sign eliminates.

This overlaps with `semantics` (which owns identifier-level meaning encoding); semiotics adds the sign-system lens — *is the same concept signed consistently across both code names and visual interface elements?*

---

## 6. Semiotic-Coherence Audit

Use this checklist when reviewing a surface:

- Does each color carry one stable meaning across the product?
- Does each icon represent one intended concept?
- Do interactive elements look interactive?
- Do disabled states look unavailable rather than merely quiet?
- Are abstract concepts paired with enough textual support?
- Is the same concept being signed consistently across UI and code-facing surfaces?

---

## Evals

This skill ships a comprehension-eval artifact at [`examples/evals/semiotics.json`](https://github.com/jacob-balslev/skill-graph/blob/main/examples/evals/semiotics.json). The checklist below is the authoring gate for sign-system decisions; the eval file is the grader surface.

## Verification

After applying this skill, verify:

- [ ] No signifier points to multiple unintended signifieds within the same system context
- [ ] Important interface meanings are not encoded through color alone
- [ ] Interactive and non-interactive states have distinct affordance signals
- [ ] Icon metaphors are coherent, learnable, and consistent across surfaces
- [ ] Direction (denotation) and judgment (connotation) are separated in financial / metric UI
- [ ] Code-facing signs (function, variable, endpoint names) are not vague signifier failures

## Do NOT Use When

| Instead, use | Why |
|---|---|
| `microcopy` | Drafting the actual button labels, empty states, tooltips, or toasts. Microcopy owns the wording; semiotics owns the sign system the wording lives inside. |
| `semantics` | Deciding the meaning encoding of a single identifier, design token, HTTP status code, or commit type. Semantics owns identifier-level meaning; semiotics owns the multi-channel sign system. |
| `semantic-relations` | Typing the connection between two concepts (IS-A, PART-OF, thematic, causal). Semantic-relations owns concept-to-concept relations; semiotics owns sign-to-meaning mappings. |
| `linguistics` | Word morphology, compound-word ordering, abbreviation policy. Linguistics owns word-form rules; semiotics owns broader sign systems including visual ones. |
| `a11y` | Auditing aria-label correctness, focus management, screen-reader semantics. A11y owns accessibility contracts; semiotics may inform them but does not own them. |
| `visual-design-foundations` | Palette, typography, spacing, hierarchy, craft quality, and motion feel. Visual-design-foundations owns visual craft; semiotics asks what the visual element *signifies*. |
| (an ontology skill) | Formal class hierarchies, existence axioms, reasoning constraints. Ontology owns formal classification; semiotics owns sign meaning in interfaces. |
