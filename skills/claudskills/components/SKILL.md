---
name: remix-components
description: The shipped `remix/ui/<component>` headless library — Accordion, Anchor (positioning), Breadcrumbs, Button, Combobox, Glyph (icons), Listbox, Menu (dropdown / context), Popover (with focus management), Scroll Lock, Select, Separator, Animation (entrance / exit / layout / spring / tween), and Theme (CSS variables + design tokens). Plus first-class web-components interop — bring in third-party custom elements (Shoelace, Lit, Web Awesome) or author your own. Load whenever the user needs a button, dropdown, modal, tooltip, popover, autocomplete, breadcrumb, accordion, icon, animation, color tokens, dark/light theme, or is about to install Radix UI / shadcn/ui / Headless UI / Floating UI / Framer Motion / lucide-react / heroicons / react-select / body-scroll-lock. Also load on questions like "how do I do a tooltip in Remix?" or "what's the equivalent of Radix Popover?".
---

# Components

Remix v3 ships a headless component library at `remix/ui/<name>`. They are *not* React components — they target the Remix JSX runtime and use the same mixin-on-`mix` pattern as the rest of the [ui](../ui/SKILL.md) framework. Most are *unstyled by default*; they ship `CSSMixinDescriptor` exports you opt into.

If you're about to install Radix UI, shadcn/ui, Headless UI, Floating UI, or Framer Motion — stop and check this list first. Almost everything is bundled.

## Imports

```ts
import { Accordion } from 'remix/ui/accordion'
import { anchor, type AnchorOptions } from 'remix/ui/anchor'
import { Breadcrumbs, type BreadcrumbItem } from 'remix/ui/breadcrumbs'
import { Button, type ButtonProps, type ButtonTone } from 'remix/ui/button'
import { Combobox } from 'remix/ui/combobox'
import { Glyph, createGlyphSheet, type GlyphName } from 'remix/ui/glyph'
import { Listbox } from 'remix/ui/listbox'
import { Menu } from 'remix/ui/menu'
import { Popover } from 'remix/ui/popover'
import { lockScroll, lockScrollOnToggle } from 'remix/ui/scroll-lock'
import { Select } from 'remix/ui/select'
import { separatorStyle } from 'remix/ui/separator'
import { animateEntrance, animateExit, animateLayout, spring, tween, easings } from 'remix/ui/animation'
import { createTheme, theme, RMX_01 } from 'remix/ui/theme'
```

Each subpath is also published as `@remix-run/ui/<name>` — pick one form per file.

## The catalogue

| Subpath | Default export(s) | Replaces |
|---|---|---|
| `remix/ui/accordion` | `Accordion`, `AccordionItem`, `AccordionTrigger`, `AccordionContent` (single / multiple modes, controlled & uncontrolled) | Radix Accordion, Headless UI Disclosure |
| `remix/ui/anchor` | `anchor(floating, target, options)` — positioning primitive (placement, offset, `relativeTo`) | Floating UI core |
| `remix/ui/breadcrumbs` | `Breadcrumbs` (props: `items: BreadcrumbItem[]`, optional `separator`) | hand-rolled `<nav>` ladders |
| `remix/ui/button` | `Button` with `tone: 'primary' \| 'secondary' \| 'ghost' \| 'danger'`, `startIcon`, `endIcon` + opt-in style mixins (`baseStyle`, `primaryStyle`, …) | shadcn Button, Radix-themed buttons |
| `remix/ui/combobox` | `Combobox` (filterable input + popover), `ComboboxOption`, `ComboboxHandle` ref API, `rmx:combobox-change` event | Headless UI Combobox, Downshift, react-select (filterable) |
| `remix/ui/glyph` | `Glyph name={...}`, `createGlyphSheet(values)` for project-local icon sets | lucide-react, heroicons, react-icons |
| `remix/ui/listbox` | `Listbox` low-level option-list primitive (used by `select`/`combobox`/`menu`) | Headless UI Listbox base |
| `remix/ui/menu` | `Menu`, `MenuTrigger`, `MenuItem` (item / checkbox / radio types), submenus, typeahead, `rmx:menu-select` event | Radix DropdownMenu / ContextMenu, Headless UI Menu |
| `remix/ui/popover` | `Popover.Context`, `popover.anchor()`, `popover.surface()`, `focusOnShow`, `focusOnHide` mixins | Radix Popover, Headless UI Popover, Floating UI react bindings |
| `remix/ui/scroll-lock` | `lockScroll()`, `lockScrollOnToggle()` mixin | body-scroll-lock, react-remove-scroll |
| `remix/ui/select` | `Select` (native-feeling, keyboard-driven), `SelectOption`, `rmx:select-change` event | Radix Select, Headless UI Select, react-select (single-value) |
| `remix/ui/separator` | `separatorStyle` mixin (no component — apply to any element) | shadcn Separator |
| `remix/ui/animation` | `animateEntrance`, `animateExit`, `animateLayout` mixins · `spring(...)`, `tween(...)`, `easings` | Framer Motion, AutoAnimate |
| `remix/ui/theme` | `createTheme(...)`, `theme` proxy, `RMX_01` preset, `glyphContract`, `glyphNames` | CSS-in-JS theme providers, Tailwind config |

The bigger ones (Accordion, Combobox, Menu, Select, Popover) are stateful and emit DOM events that bubble: `rmx:accordion-change`, `rmx:combobox-change`, `rmx:menu-select`, `rmx:select-change`. Listen with `on(...)` like any DOM event.

## Shape of a Remix UI component

Everything is a function `(handle: Handle<Props>) => () => RemixElement` — the same two-phase model as `remix/ui` (setup once, render on `handle.update()`). See [ui](../ui/SKILL.md) for the model.

Quick example with `Button`:

```tsx
import { Button } from 'remix/ui/button'
import { Glyph } from 'remix/ui/glyph'
import { on } from 'remix/ui'

export function SaveBar(handle: Handle<{ onSave: () => void }>) {
  return () => (
    <div>
      <Button tone="primary" startIcon={<Glyph name="check" />}
              mix={on('click', handle.props.onSave)}>
        Save
      </Button>
      <Button tone="ghost">Cancel</Button>
    </div>
  )
}
```

## Styling: opt in, don't fight it

Components in this library are *headless by default*. Each component module also exports `CSSMixinDescriptor`s (e.g. `baseStyle`, `primaryStyle`, `secondaryStyle`, `ghostStyle`, `dangerStyle` from `remix/ui/button`; `separatorStyle` from `remix/ui/separator`). Compose them via `mix={[...]}` to get a reasonable default, then layer your own `css({...})` on top.

```tsx
import { Button, primaryStyle } from 'remix/ui/button'
import { css } from 'remix/ui'

<Button mix={[primaryStyle, css({ borderRadius: '999px' })]}>
  Rounded primary
</Button>
```

## Anchor + Popover: the floating-UI replacement

The positioning primitive lives at `remix/ui/anchor`:

```ts
import { anchor } from 'remix/ui/anchor'

const cleanup = anchor(floatingEl, anchorEl, { placement: 'bottom-start', offset: 4 })
// cleanup() to detach
```

For surfaces with focus management, dismiss handling, and outside-click — use `Popover` directly. It exposes mixins, not children components:

```tsx
import { Popover } from 'remix/ui/popover'
import { on } from 'remix/ui'

export function Tooltip(handle: Handle<{ children: RemixNode }>) {
  let open = false
  const triggerRef = { current: null as HTMLElement | null }
  const floatingRef = { current: null as HTMLElement | null }

  return () => (
    <Popover.Context>
      <button ref={triggerRef}
              mix={[on('mouseenter', () => { open = true; handle.update() }),
                    Popover.anchor({ placement: 'top' })]}>
        Hover me
      </button>
      <div ref={floatingRef}
           mix={[Popover.surface({ open, onHide: () => { open = false; handle.update() } }),
                 Popover.focusOnShow()]}>
        {handle.props.children}
      </div>
    </Popover.Context>
  )
}
```

## Icons: `Glyph` + `createGlyphSheet`

The default surface is `Glyph name={'check'}`. The icon set is contributed by your theme (or by `RMX_01`'s built-in glyph values). For project-local icons, define a sheet:

```ts
import { createGlyphSheet } from 'remix/ui/glyph'
const sheet = createGlyphSheet({ /* glyphValues */ })
```

Then render `<sheet />` once near the top of `<body>` and use `<Glyph name="…" />` anywhere. See `references/glyph.md` for the glyph-contract shape.

## Theme: contract → values → CSS variables

```ts
import { createTheme, RMX_01 } from 'remix/ui/theme'

export const appTheme = createTheme(RMX_01, {
  // override colors, spacing, radii, glyph values, ...
})
```

`createTheme` returns mixins you apply to `<html>` / `<body>` to emit CSS custom properties. The exported `theme` proxy gives you typed access to those variable references inside `css({...})`. See `references/theme.md`.

## Animation: mixins + curves

Use the entrance/exit/layout mixins on any element. `spring` and `tween` are the underlying iterators for custom code:

```tsx
import { animateEntrance, animateExit, animateLayout, spring } from 'remix/ui/animation'

<div mix={[
  animateEntrance({ opacity: [0, 1], transform: ['translateY(8px)', 'translateY(0)'] }),
  animateLayout(),
]}>
  …
</div>
```

For more, see `references/animation.md`.

## Web components are first-class

Because Remix's JSX runtime emits DOM, you can mix in plain custom elements anywhere — both elements you author and elements from third-party libraries. Two patterns:

**1. Use an existing custom element directly.** Type the tag in `JSX.IntrinsicElements` (or use a `key`-suffixed name) and it slots into JSX:

```tsx
declare global {
  namespace JSX {
    interface IntrinsicElements {
      'sl-button': { variant?: 'primary' | 'default'; onClick?: (e: Event) => void; children?: RemixNode }
    }
  }
}

return () => <sl-button variant="primary">From Shoelace</sl-button>
```

Import the custom element's registration once at hydration time (e.g. `import '@shoelace-style/shoelace/dist/components/button/button.js'`).

**2. Author your own custom element** when you need an island of behaviour that lives outside the Remix component tree (long-lived widget, third-party integration, drop-in for non-Remix pages):

```ts
class CountBadge extends HTMLElement {
  static observedAttributes = ['count']
  attributeChangedCallback() { this.textContent = `(${this.getAttribute('count')})` }
}
customElements.define('count-badge', CountBadge)
```

Then in JSX: `<count-badge count={items.length} />`. Custom elements ignore the Remix update protocol (no `handle.update`), which is exactly what you want for self-contained widgets.

When to reach for a custom element instead of a Remix component:

- Wrapping a non-Remix JS library that needs a long-lived DOM root (charting libs, video players, editors)
- Sharing a widget between Remix and non-Remix pages
- You want browser-native lifecycle hooks (`connectedCallback`, `disconnectedCallback`)

Otherwise, prefer the Remix component model — typed handles, mixins, and the rest of `remix/ui` integrate more cleanly.

## Don't reach for these — Remix bundles them

| Reflex install | Use instead |
|---|---|
| Radix UI primitives | `remix/ui/*` (Accordion, Menu, Popover, Select, Separator) |
| Headless UI | `remix/ui/*` (Combobox, Listbox, Menu, Select) |
| shadcn/ui | `remix/ui/button` + `remix/ui/theme` + project-local components |
| Floating UI | `remix/ui/anchor` (core) + `remix/ui/popover` (focus & dismiss) |
| Framer Motion | `remix/ui/animation` (`animateEntrance`, `animateLayout`, `spring`, `tween`) |
| lucide-react / heroicons | `remix/ui/glyph` + `createGlyphSheet` |
| body-scroll-lock / react-remove-scroll | `remix/ui/scroll-lock` |
| react-select (single value) | `remix/ui/select` or `remix/ui/combobox` |

## Further reading

- `references/catalogue.md` — full prop tables for every component
- `references/anchor-popover.md` — positioning + focus management deep dive
- `references/glyph.md` — `createGlyphSheet`, `GlyphContract`, theming icons
- `references/theme.md` — `createTheme` + the `theme` proxy
- `references/animation.md` — mixin signatures, `spring`/`tween`/`easings`
- See also: [ui](../ui/SKILL.md) — the JSX runtime + component model these are built on; [templating](../templating/SKILL.md) — HTML responses without JSX; [build](../build/SKILL.md) — how the client JS for these components is compiled
