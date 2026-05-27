---
name: a11y-aria-patterns
description: >
  Use this skill when the user asks about ARIA, ARIA roles, ARIA attributes, aria-label,
  aria-labelledby, aria-describedby, aria-expanded, aria-hidden, aria-live, aria-required,
  aria-invalid, "WAI-ARIA", "ARIA Authoring Practices", "APG pattern", "accessible name",
  "accessible description", live regions, custom widgets, dialogs, menus, tabs, accordions,
  comboboxes, tooltips, tree views, carousels, or is building any custom interactive component
  that requires ARIA roles and keyboard behavior beyond native HTML elements.
---

# ARIA Patterns and Authoring Practices

> **Skill type: Reference.** This is teaching/pattern content — it explains the WAI-ARIA APG keyboard contracts and ARIA state rules for custom widgets. It is not a scanner. For static review of existing ARIA usage, use `/a11y-review`. For runtime verification of ARIA validity against resolved roles, use the `a11y-testing` skill to set up real axe.

ARIA (Accessible Rich Internet Applications) extends HTML semantics for custom, dynamic UI components. It supplements — never replaces — native HTML.

**The ARIA First Principles:**
1. **No ARIA is better than bad ARIA.** Incorrect ARIA is worse than no ARIA.
2. **Native HTML first.** Use a `<button>` before `role="button"`. Use `<select>` before a custom combobox.
3. **You own the keyboard.** Using an ARIA widget role means you are fully responsible for its keyboard behavior per the APG spec.
4. **Keep states synchronized.** Every ARIA state attribute must reflect the current UI state — never hardcode them.

---

## ARIA Fundamentals

### How ARIA Works

ARIA adds three things to elements in the accessibility tree:
- **Roles** — what the element *is* (`role="dialog"`, `role="tab"`)
- **Properties** — static characteristics (`aria-label`, `aria-required`)
- **States** — dynamic, changing values (`aria-expanded`, `aria-checked`, `aria-invalid`)

### Accessible Names (WCAG 4.1.2)

Every interactive element needs an accessible name. The browser computes it in this priority order:

1. `aria-labelledby` (references another element's text — highest priority)
2. `aria-label` (inline text string)
3. Native label element (`<label for="id">`)
4. Element's own text content (for buttons and links)
5. `title` attribute (last resort — inconsistent screen reader support)

```html
<!-- Priority 1: aria-labelledby -->
<h2 id="section-title">Billing Address</h2>
<section aria-labelledby="section-title">...</section>

<!-- Priority 2: aria-label (when no visible text exists) -->
<button aria-label="Close dialog">
  <svg aria-hidden="true">...</svg>
</button>

<!-- Priority 3: Associated label -->
<label for="card-number">Card Number</label>
<input id="card-number" type="text">

<!-- Priority 4: Button text -->
<button>Submit Order</button>
```

### Accessible Descriptions

`aria-describedby` provides supplementary information — announced after the name, often as a separate speech unit:

```html
<label for="password">Password</label>
<input
  id="password"
  type="password"
  aria-describedby="password-hint password-error"
>
<p id="password-hint">Must be at least 8 characters.</p>
<p id="password-error" aria-live="polite"></p>
```

Multiple IDs in `aria-describedby` are read in order.

---

## Common Widget Patterns (APG)

### Dialog / Modal (role="dialog")

```html
<!-- Background content inert when modal open -->
<main inert aria-hidden="true">...</main>

<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-desc"
>
  <h2 id="dialog-title">Confirm Deletion</h2>
  <p id="dialog-desc">This action cannot be undone.</p>

  <button type="button">Cancel</button>
  <button type="button">Delete</button>
</div>
```

**Required behavior:**
- On open: Move focus inside the dialog (first focusable element or the dialog itself)
- While open: Trap `Tab` and `Shift+Tab` within the dialog
- On `Escape`: Close dialog, return focus to the trigger element
- On close: Return focus to the element that opened the dialog

**`role="alertdialog"`** — for urgent dialogs requiring immediate response (e.g., unsaved changes warning). Screen readers interrupt current speech to announce it.

### Tabs Pattern (WCAG 2.1.1)

```html
<div role="tablist" aria-label="Settings Sections">
  <button role="tab" aria-selected="true"  aria-controls="panel-general" id="tab-general">General</button>
  <button role="tab" aria-selected="false" aria-controls="panel-security" id="tab-security" tabindex="-1">Security</button>
  <button role="tab" aria-selected="false" aria-controls="panel-billing"  id="tab-billing"  tabindex="-1">Billing</button>
</div>

<div role="tabpanel" id="panel-general"  aria-labelledby="tab-general">...</div>
<div role="tabpanel" id="panel-security" aria-labelledby="tab-security" hidden>...</div>
<div role="tabpanel" id="panel-billing"  aria-labelledby="tab-billing"  hidden>...</div>
```

**Keyboard behavior (roving tabindex):**
| Key | Action |
|-----|--------|
| `Tab` | Enter tablist on active tab; `Tab` again exits to tabpanel |
| `→` / `←` | Move to next/previous tab (wraps); auto-activates tab |
| `Home` | Move to first tab |
| `End` | Move to last tab |
| `Enter` / `Space` | Activate tab (manual activation variant) |

**Roving tabindex:** Only the active tab has `tabindex="0"`. All others have `tabindex="-1"`. JavaScript updates both on navigation.

### Accordion / Disclosure (aria-expanded)

```html
<h3>
  <button
    type="button"
    aria-expanded="false"
    aria-controls="faq-1-content"
    id="faq-1-btn"
  >
    What is your return policy?
  </button>
</h3>
<div id="faq-1-content" role="region" aria-labelledby="faq-1-btn" hidden>
  <p>You may return items within 30 days...</p>
</div>
```

**Rules:**
- `aria-expanded="true/false"` on the trigger button — must be JS-driven, never hardcoded
- `aria-controls` links button to its panel (ID reference)
- Wrap in heading element for document outline
- `hidden` / `aria-hidden="true"` on collapsed panels

### Combobox / Autocomplete

```html
<label for="country-input">Country</label>
<div role="combobox"
     aria-expanded="false"
     aria-haspopup="listbox"
     aria-owns="country-listbox">
  <input
    id="country-input"
    type="text"
    autocomplete="off"
    aria-autocomplete="list"
    aria-controls="country-listbox"
    aria-activedescendant=""
  >
</div>
<ul id="country-listbox" role="listbox" aria-label="Countries">
  <li role="option" id="opt-us" aria-selected="false">United States</li>
  <li role="option" id="opt-ca" aria-selected="false">Canada</li>
</ul>
```

**Keyboard behavior:**
| Key | Action |
|-----|--------|
| `↓` | Open list, move to first option |
| `↑` / `↓` | Navigate options |
| `Enter` | Select focused option |
| `Escape` | Close list |
| `Home` / `End` | Jump to first/last option |

Update `aria-activedescendant` on the input to the ID of the currently highlighted option.

### Menu / Menubar (role="menu")

Use `role="menu"` for **application menus** (File, Edit, View), NOT for navigation. Use `<nav>` + `<ul>` for site navigation.

```html
<button
  type="button"
  aria-haspopup="menu"
  aria-expanded="false"
  aria-controls="actions-menu"
  id="actions-btn"
>
  Actions ▾
</button>
<ul role="menu" id="actions-menu" aria-labelledby="actions-btn">
  <li role="menuitem"><button type="button">Edit</button></li>
  <li role="menuitem"><button type="button">Duplicate</button></li>
  <li role="separator"></li>
  <li role="menuitem" aria-disabled="true"><button type="button" disabled>Archive</button></li>
  <li role="menuitem"><button type="button">Delete</button></li>
</ul>
```

**Keyboard behavior:**
| Key | Action |
|-----|--------|
| `↓` / `↑` | Navigate items (wraps) |
| `Enter` / `Space` | Activate item |
| `Escape` | Close menu, return focus to trigger |
| `Home` / `End` | Jump to first/last item |
| `A–Z` | Type-ahead selection |

---

## ARIA Live Regions

Live regions announce dynamic content changes to screen readers without requiring a focus move.

### `aria-live` Values

| Value | Behavior | Use For |
|-------|----------|---------|
| `polite` | Waits for user to finish current action | Status updates, form feedback, search results loading |
| `assertive` | Interrupts immediately | Critical errors, urgent alerts |
| `off` (default) | No announcement | Most content |

```html
<!-- Status messages (polite) -->
<div role="status" aria-live="polite" aria-atomic="true">
  <!-- Inject text here when status changes -->
</div>

<!-- Error alerts (assertive) -->
<div role="alert" aria-live="assertive">
  <!-- Inject critical error message here -->
</div>
```

### Semantic Shortcuts

- `role="alert"` = implicit `aria-live="assertive"` + `aria-atomic="true"`
- `role="status"` = implicit `aria-live="polite"` + `aria-atomic="true"`
- `role="log"` = implicit `aria-live="polite"` for sequential messages (chat, audit trail)
- `role="timer"` = implicit `aria-live="off"` — only announce value when directly focused

### Live Region Patterns

**Toast notifications:**
```html
<!-- Single persistent container in DOM; inject/clear text dynamically -->
<div id="toast-region" role="status" aria-live="polite" aria-atomic="true" class="sr-only">
  <!-- JS sets textContent here; empty string clears it -->
</div>
```

**Loading state:**
```html
<div aria-busy="true" aria-live="polite">
  <p>Loading search results...</p>
</div>
<!-- When complete, set aria-busy="false" and replace content -->
```

**Form error summary:**
```html
<div role="alert" aria-live="assertive" id="error-summary">
  <!-- Inject on submit: "3 errors found. Please correct: Email is required, ..." -->
</div>
```

**Critical rule:** The live region container must exist in the DOM *before* you inject content into it. Adding both the container and the content simultaneously often fails to trigger announcements.

---

## aria-hidden — Rules and Common Mistakes

`aria-hidden="true"` removes an element and all its descendants from the accessibility tree.

### Correct Uses
```html
<!-- Decorative icon inside a labeled button -->
<button type="button" aria-label="Close">
  <svg aria-hidden="true" focusable="false">...</svg>
</button>

<!-- Decorative image -->
<img src="hero-bg.jpg" alt="" aria-hidden="true">

<!-- Modal: hide background content -->
<main aria-hidden="true" inert>...</main>
```

### Forbidden Uses

```html
<!-- ❌ CRITICAL: aria-hidden on a focusable element -->
<button aria-hidden="true">Submit</button>
<!-- Screen reader can't see it; keyboard user can still Tab to it — disorienting -->

<!-- ❌ CRITICAL: aria-hidden ancestor contains focusable descendants -->
<div aria-hidden="true">
  <button>Click me</button>  <!-- Keyboard reaches it; screen reader can't -->
</div>

<!-- ❌ Never hide content that provides information without a visible alternative -->
<nav aria-hidden="true">
  <a href="/">Home</a>  <!-- Navigation is now invisible to AT users -->
</nav>
```

**Rule:** If `aria-hidden="true"` is on an element, that element and all its children must be non-focusable. Use `inert` attribute as the modern alternative (removes focus AND hides from AT simultaneously).

---

## React ARIA Patterns

### Boolean vs. String ARIA States

```tsx
// ❌ WRONG: String "true"/"false" — technically works, but brittle
<button aria-expanded="true">Toggle</button>

// ✅ CORRECT: JSX boolean expression — stays in sync with state
const [isOpen, setIsOpen] = useState(false);
<button aria-expanded={isOpen}>Toggle</button>
```

### Radix UI asChild — Preserve ARIA Plumbing

```tsx
// ✅ CORRECT: Radix passes all ARIA props through asChild
<Dialog.Trigger asChild>
  <Button variant="outline">  {/* Button must spread props + forwardRef */}
    Open
  </Button>
</Dialog.Trigger>

// ❌ WRONG: Custom component that swallows props
const Button = ({ children, onClick }) => (
  <button onClick={onClick}>{children}</button>
  // Missing: {...props} spread — loses aria-haspopup, aria-expanded, etc.
);
```

---

## Roving Tabindex Pattern — Implementation

Used in: tablist, toolbar, menu, listbox, tree, radiogroup, grid

```tsx
const [focusedIndex, setFocusedIndex] = useState(0);
const itemRefs = useRef([]);

function handleKeyDown(e, index) {
  const count = items.length;
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
    const next = (index + 1) % count;
    setFocusedIndex(next);
    itemRefs.current[next]?.focus();
  }
  if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
    const prev = (index - 1 + count) % count;
    setFocusedIndex(prev);
    itemRefs.current[prev]?.focus();
  }
  if (e.key === 'Home') { setFocusedIndex(0); itemRefs.current[0]?.focus(); }
  if (e.key === 'End')  { const last = count-1; setFocusedIndex(last); itemRefs.current[last]?.focus(); }
}

return (
  <div role="tablist">
    {items.map((item, i) => (
      <button
        key={item.id}
        role="tab"
        tabIndex={i === focusedIndex ? 0 : -1}
        aria-selected={i === focusedIndex}
        ref={el => itemRefs.current[i] = el}
        onKeyDown={e => handleKeyDown(e, i)}
        onClick={() => setFocusedIndex(i)}
      >
        {item.label}
      </button>
    ))}
  </div>
);
```
