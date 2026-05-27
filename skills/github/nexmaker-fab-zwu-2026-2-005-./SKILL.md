---
name: community-web-dev
description: Community-proven website development workflow using AI coding agents. Use when building websites with Claude/Codex/AI agents to avoid common pitfalls like vague requirements, endless refactoring cycles, and poor UX. Triggers on phrases like "build a website", "make a site", "create a web app", "frontend project", or when user expresses frustration with AI-generated websites.
---

# Community Website Development Skill

AI coding agents (Claude, Codex, etc.) excel at implementation but are terrible at mind-reading. This skill provides a battle-tested workflow to get human-friendly, production-ready websites.

## Core Principle: Research → Spec → Ship

Never skip stages. Each stage prevents the next stage from becoming a disaster.

---

## Stage 1: Research (Don't Write Code Yet)

**Goal:** Understand the landscape before committing to a direction.

### Prompt Template
```
I want to build [describe your website/app].

Before writing any code, help me research:

1. Find 3 excellent reference websites with similar functionality
   - Analyze their information architecture (navigation, content flow)
   - Note their visual style (colors, typography, spacing)
   - Study their interaction patterns (animations, feedback, error handling)

2. Identify common user pain points in this type of website
   - What do users complain about most?
   - What features are often implemented poorly?

3. List technical decisions I'll need to make:
   - Framework/library choices
   - State management approach
   - Styling strategy
   - Potential technical debt areas

4. Give me a "reality check" - what usually goes wrong?
```

### Why This Works
- Forces AI to analyze existing solutions rather than inventing from scratch
- Surfaces UX considerations before you're locked into code
- Identifies technical pitfalls early (e.g., "this approach doesn't scale")

---

## Stage 2: Spec (Write the Blueprint)

**Goal:** Transform fuzzy ideas into concrete, testable requirements.

### Prompt Template
```
Based on the research above, create a technical specification:

## 1. Core Features (Priority Order)
List features from MVP → Full Feature Set. Be specific:
- ❌ "User profiles" 
- ✅ "User can upload avatar, edit bio (max 500 chars), view public profile"

## 2. Page Structure
Provide an ASCII sitemap or wireframe:
```
Homepage
├── Hero section (tagline + CTA)
├── Features grid (3 cards)
└── Footer

Dashboard
├── Sidebar navigation
├── Main content area
└── Notification panel
```

## 3. Visual Direction
- Color scheme: [primary/secondary/accent]
- Typography: [font choices]
- Overall feel: [minimal/bold/playful/professional]
- Reference: "Like [site X] but with [difference]"

## 4. Technical Stack
- Framework: [React/Vue/Svelte/etc]
- Styling: [CSS modules/Tailwind/styled-components]
- State: [Context/Zustand/Redux]
- Build tool: [Vite/Next.js/etc]

## 5. Acceptance Criteria
Define "done" for each feature:
- [ ] Dark mode toggle works without flash
- [ ] Mobile layout doesn't break below 375px
- [ ] Form validation shows inline errors
- [ ] Loading states for all async actions
```

### Red Flags to Avoid
- Vague descriptions: "modern", "clean", "user-friendly"
- Missing edge cases: What happens on error? Empty state? Slow connection?
- No visual references: "I'll know it when I see it" = guaranteed rework

---

## Stage 3: Ship (Incremental Delivery)

**Goal:** Build in small, verifiable chunks. Never the "full website" in one shot.

### Milestone-Based Approach

**Milestone 1: Static Shell**
```
Build only the HTML structure and CSS styling:
- Static homepage with placeholder content
- Responsive layout working
- Dark mode toggle functional (even if just placeholder)

NO JavaScript logic yet. Just structure and style.
```

**Milestone 2: Core Interaction**
```
Add ONE core feature:
- If it's a blog: Show article list + single article view
- If it's a dashboard: Show data table + filter
- If it's an e-commerce: Product grid + product detail

Keep it read-only. No auth, no mutations.
```

**Milestone 3: Full Feature Set**
```
Add remaining features one by one:
- Authentication (if needed)
- Forms and mutations
- Edge cases and error states
```

**Milestone 4: Polish**
```
- Loading states
- Error handling
- Animations and micro-interactions
- Performance optimization
- Accessibility audit
```

### Why Incremental?
- Catch design/UX issues early when they're cheap to fix
- Validate technical choices before committing
- Maintain momentum with frequent wins
- AI performs better on focused, bounded tasks

---

## Common Anti-Patterns (Don't Do These)

### ❌ "Build me a website like [famous site]"
- AI copies structure but misses the UX subtleties
- Results in "technically works, feels wrong"

### ❌ "Make it look professional"
- Subjective terms = endless revision cycles
- Instead: Provide 3 specific visual references

### ❌ One-shot full implementation
- "Generate the complete React app with auth, database, payments..."
- Results in Frankenstein code that technically runs but is unmaintainable

### ❌ Skipping the "boring" parts
- Error handling, loading states, empty states, responsive edge cases
- These differentiate amateur from professional work

---

## Quick-Start Checklist

Before starting any website project:

- [ ] Can I describe the target user in one sentence?
- [ ] Do I have 3 visual references I can point to?
- [ ] Have I listed the MVP features vs nice-to-have?
- [ ] Do I know what "done" looks like for each feature?
- [ ] Am I prepared to review static HTML before adding JS?

If any answer is "no", go back to Research or Spec stage.

---

## Emergency Escape Hatches

**If you're already in refactoring hell:**

1. **Stop adding features** - Freeze scope immediately
2. **Take a screenshot** - Document current state
3. **Write a reset spec** - What's the minimum that needs to work?
4. **Scrap and rebuild from spec** - Counter-intuitive but faster than patching

**If the AI keeps missing your vision:**
- You're being too abstract. Give concrete examples.
- "Not like that" → "See [site X]? Do [specific thing] like them."

**If you have 47 "small" fixes:**
- That's not fixes, that's "the spec was incomplete"
- Go back to Stage 2 and write proper acceptance criteria

---

## Summary

| Stage | Output | Time Investment |
|-------|--------|-----------------|
| Research | Reference analysis + tech decisions | 10-15 min |
| Spec | Detailed blueprint | 15-20 min |
| Ship | Working code (incremental) | 30-60 min per milestone |

**Total:** 1-2 hours of planning saves 5-10 hours of refactoring.

Remember: AI amplifies your clarity. Vague input = garbage output. Specific input = magic.
