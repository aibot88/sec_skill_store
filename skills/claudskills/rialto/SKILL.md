---
name: rialto
description: Use when building UI with the Rialto design system, importing from "rialto" or "@mattbutlerengineering/rialto", choosing components, applying design tokens, composing layouts, or authoring new Rialto components. Triggers on mentions of "Rialto", "component library", "design system", "UI component", or imports from rialto.
---

# Rialto Design System

Rialto is a 62-component React design system with warm-neutral aluminum surfaces, gold accent, spring-physics motion, and CSS token architecture. Import everything from the barrel:

```tsx
import { Button, Input, Card, Stack, Text } from "rialto";
import "rialto/tokens";
```

## Required Providers

```tsx
<RialtoProvider vibe="default" theme="system">
  <ToastProvider>
    <App />
  </ToastProvider>
</RialtoProvider>
```

- `RialtoProvider` — device context, theming, vibe token overrides
- `ToastProvider` — required before calling `useToast()`

## 6 Cardinal Rules

1. **Tokens only** — Never hardcode colors, spacing, radii, or easing. Always `var(--rialto-*)`.
2. **Gold is surgical** — `--rialto-accent` only for focus rings, active/selected states, primary button fills. Never decorative.
3. **forwardRef always** — Every component uses `React.forwardRef`. New components must too.
4. **Respect reduced motion** — Check `useReducedMotion()` from Framer Motion. Skip animation when true.
5. **Logical properties** — Use `margin-inline-start`, `padding-inline-end`, `inset-inline-start` — never `left`/`right`.
6. **Barrel imports** — Always `import { X } from "rialto"`. Never `import X from "rialto/components/X"`.

## Component Selection

> Full details: [decision-trees.md](references/decision-trees.md)

| Need | Start Here |
|------|-----------|
| Form input | Decision tree → Input, TextArea, NumberInput, Select, Toggle, etc. |
| Overlay | Dialog, ConfirmDialog, Drawer, Popover, Tooltip, HoverCard |
| Feedback | Priority routing: P1 ConfirmDialog → P2 Dialog → P3 Banner → P4 Alert → P5 Toast → P6 Tooltip |
| Navigation | Tabs, Breadcrumb, Steps, Pagination, Sidebar, Navbar |
| Data display | Table, Card, Badge, Tag, Stat, DataList, Timeline, Tree |
| Layout | Stack, Divider, Collapsible, Accordion, ScrollArea |

## Composition

> Full details: [composition-patterns.md](references/composition-patterns.md)

| Pattern | Components |
|---------|-----------|
| Data table page | Table + Pagination + Stack |
| Login form | Card + Stack + Input + Button |
| Settings panel | Drawer + Stack + Toggle + Select + Divider |
| Confirmation flow | ConfirmDialog (variant="danger") |
| Toast notifications | ToastProvider + useToast() hook |

## Tokens

> Full details: [token-enforcement.md](references/token-enforcement.md)

| Category | Prefix | Example |
|----------|--------|---------|
| Surfaces | `--rialto-surface-*` | `--rialto-surface-elevated` |
| Text | `--rialto-text-*` | `--rialto-text-secondary` |
| Borders | `--rialto-border*` | `--rialto-border-strong` |
| Accent | `--rialto-accent*` | `--rialto-accent-muted` |
| Semantic | `--rialto-error*`, `--rialto-success*` | `--rialto-error-muted` |
| Shadows | `--rialto-shadow-*` | `--rialto-shadow-elevated` |
| Radius | `--rialto-radius-*` | `--rialto-radius-soft` |
| Spacing | `--rialto-space-*` | `--rialto-space-lg` |
| Easing | `--rialto-ease-*` | `--rialto-ease-precision` |

## Icons

> Full details: [icon-vocabulary.md](references/icon-vocabulary.md)

Use Lucide React icons. Import directly or use `getIcon(concept)` for data-driven UIs. Sizes: 14px (sm buttons), 16px (md buttons), 20px (standalone), 32-48px (hero/empty state).

## Authoring New Components

> Full details: [authoring-guide.md](references/authoring-guide.md)

File structure: `src/components/Name/Name.tsx` + `Name.module.css`. Extend native HTML props, use `forwardRef`, CSS Modules with token variables, all states (hover/active/focus/disabled), WCAG AA contrast.

## Common Mistakes

> Full details: [common-mistakes.md](references/common-mistakes.md)

- Hardcoding `#hex` colors instead of tokens
- Importing from `"rialto/components/Button"` instead of `"rialto"`
- Using gold accent for decorative backgrounds
- Calling `useToast()` without `<ToastProvider>`
- Using CSS transitions for interactive animations (use Framer Motion)
- Skipping `useReducedMotion()` check before animating

## Auto-Generated Reference

For complete per-component props, slots, and character limits, see the generated reference:
[component-reference.md](../../generated/component-reference.md)
