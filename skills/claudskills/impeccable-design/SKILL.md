---
name: impeccable-design
description: >
  Bind agent-authored `.DESIGN.md` files to paperboard's design doctrine. Loads
  the impeccable anti-slop methodology (vendored, Apache 2.0, pinned to commit
  `4af581e23f17d112d8f9d6b7a5b7ff37823494e1`) and the binding rules in
  `core/designs/DESIGN-AUTHORITY.md`. Read these BEFORE writing or editing any
  `.DESIGN.md` file.
---

# impeccable-design

Paperboard's design authority skill. It does not run a CLI — it loads doctrine
into the agent's context so that every authored or modified `.DESIGN.md` file
respects the same anti-slop rules. Methodology is imported from
[pbakaus/impeccable](https://github.com/pbakaus/impeccable); aesthetic tokens
remain paperboard's own.

## When to invoke

- The user asks you to **create**, **edit**, or **audit** a `.DESIGN.md` file
  (a design tier, a starter, or the default `paperboard.DESIGN.md`).
- The user asks for a new design tier, a new starter pack entry, or a redesign
  of an existing tier.
- You are reviewing a PR that touches anything under `core/designs/`.
- A `.DESIGN.md` lint fails and you need to reason about why a token or rule is
  banned.

Do **not** invoke for plain HTML/CSS work that does not touch a `.DESIGN.md`
contract, or for documentation prose unrelated to design tokens.

## Doctrine sources

Read these files, in order, before authoring or modifying a `.DESIGN.md`:

1. **`core/designs/DESIGN-AUTHORITY.md`** — the binding rules. The single source
   of truth for what is allowed in any paperboard `.DESIGN.md`.
2. **`core/designs/impeccable-context/typography.md`** — type scale, weights,
   tracking, mono-vs-serif decisions.
3. **`core/designs/impeccable-context/color-and-contrast.md`** — palette
   discipline, accent budget, tinted neutrals, contrast floor.
4. **`core/designs/impeccable-context/spatial-design.md`** — spacing scale,
   border discipline, depth from negative space (not shadows).
5. **`core/designs/impeccable-context/motion-design.md`** — easing curves
   (`cubic-bezier(0.16, 1, 0.3, 1)` only; no bounce), durations,
   `prefers-reduced-motion`.
6. **`core/designs/impeccable-context/interaction-design.md`** — affordance,
   state, focus, hit-target rules.
7. **`core/designs/impeccable-context/responsive-design.md`** — breakpoint
   philosophy, fluid type, container query intent.
8. **`core/designs/impeccable-context/ux-writing.md`** — voice, hedging bans,
   expert-decisive tone.

Provenance: vendored verbatim under Apache 2.0 from `pbakaus/impeccable` at
commit `4af581e23f17d112d8f9d6b7a5b7ff37823494e1`. See
`core/designs/impeccable-context/UPSTREAM.md` and `NOTICE.md`.

## Absolute bans (non-negotiable)

These are restated from `DESIGN-AUTHORITY.md` so the skill is self-contained.
Every `.DESIGN.md` Don't list must enforce all of them:

- **Glassmorphism** — no `backdrop-filter: blur`, no frosted-translucent
  surfaces, no glow-on-blur cards.
- **Gradient text** — no `-webkit-background-clip: text` with a gradient fill.
- **Side-stripe borders** — no `border-left` / `border-right` greater than 1px
  used as a colored stripe on cards, list items, callouts, or alerts.
- **Nested card-in-card** — no card containers visually nested inside other
  cards. Flatten the hierarchy; depth comes from negative space.
- **Generic AI emoji decoration** — no ✨ 🚀 ⚡ 🎯 🔥 💎 or comparable cliché
  glyphs used decoratively. Status dots, mono `·`, and typographic emphasis
  are the only allowed ornaments.
- **Identical-card feature grids** — no `repeat(auto-fit, minmax(280px, 1fr))`
  endlessly tiling same-shaped icon-heading-text cards.
- **Hero-metric SaaS layouts** — no big-number-with-tiny-label-and-gradient
  template.
- **Bounce / elastic easing** — animations decelerate via expo-out only.
- **Pure `#000` / `#fff`** — always tinted neutrals (paperboard ships
  `#08090A` / `#F7F8F8`).
- **Hedging prose** — "maybe consider," "could be helpful," "might want to" are
  banned. Design rules are decisive.

If a request asks for any of the above, refuse and explain which ban applies.

## How to use this when authoring or modifying a `.DESIGN.md` file

1. **Read `core/designs/DESIGN-AUTHORITY.md` in full** before writing any token
   or rule. Then read the relevant impeccable-context file for the dimension
   you are touching (typography, color, spatial, motion, etc.).
2. **Audit the existing file (if any) against the bans** above. List every
   violation found. Do not silently fix — list, then fix.
3. **Write or edit tokens** in paperboard's voice: cold, dark, technical,
   expert-decisive. No hedging. Every Don't is a hard, enforceable ban.
4. **Add or update the audit comment** at the very top of the file, in HTML
   comment form:
   `<!-- YYYY-MM-DD: audited against impeccable doctrine; <N> violations corrected: <list> -->`
   or `<!-- YYYY-MM-DD: audited against impeccable doctrine; no violations found -->`.
5. **Verify** by running `pytest -q` and (when Node.js is available)
   `npm run lint:artifacts`. Neither must regress.

## Methodology vs. aesthetic — the load-bearing distinction

Paperboard adopts impeccable's **methodology** (how design rules are authored
and enforced), **not** its **aesthetic** (the warm Cormorant Garamond editorial
palette). Impeccable's own tokens — Cormorant Garamond, Warm Ash Cream,
Editorial Magenta — are **not** adopted by any paperboard tier.

Paperboard's canonical aesthetic remains cold, dark, technical:

- `#08090A` near-black canvas; `#F7F8F8` tinted off-white.
- Geist Mono eyebrows in UPPERCASE with `0.12em` tracking.
- Indigo / rose accents capped at ≤ 15% of visible surface area.
- 1px hairline borders; depth via tonal layering, not drop shadows.
- Numbered sections (`00`, `01`, `02`) with tightened heading tracking
  (`-0.02em` to `-0.04em`).

If you find yourself writing tokens that look "warm editorial," stop — you have
crossed from methodology into aesthetic import. Roll back.
