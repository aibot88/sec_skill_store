---
name: astro-accessibility
description: >
  This skill should be used when implementing accessibility in Astro, WCAG compliance in Astro, Astro ARIA patterns, keyboard navigation in Astro components, screen reader support in Astro, Astro semantic HTML, focus management in Astro, accessible forms in Astro, Astro accessibility testing, axe-core integration with Astro, accessible Astro islands, alt text for Astro images, focus trapping in modals, accessible view transitions, or color contrast requirements.
---

# Astro Accessibility (WCAG 2.2 AA)

## Core Principle: Semantic HTML First

Astro's static-first model is inherently accessibility-friendly because HTML renders without JavaScript. Leverage this advantage fully.

- Use native HTML elements (`<nav>`, `<button>`, `<dialog>`, `<main>`, `<header>`, `<footer>`) for their intended purpose. NEVER style `<div>` or `<span>` elements to look like interactive controls.
- Native elements provide built-in keyboard support, screen reader announcements, and focus management for free. A `<button>` handles Enter, Space, focus, and role automatically — a styled `<div>` provides none of this.
- The browser builds the accessibility tree from your HTML structure. Using the wrong elements confuses assistive technology and breaks the experience for users who depend on it.
- Structure your document with landmark regions: one `<main>`, a `<nav>` for navigation, `<header>` and `<footer>` for page-level landmarks. Screen reader users navigate by landmarks.
- Maintain a proper heading hierarchy. Use exactly one `<h1>` per page, then `<h2>` through `<h6>` in logical order without skipping levels. Headings are the primary navigation mechanism for screen reader users.

## ARIA Rules

Follow the first rule of ARIA: do NOT use ARIA if a native HTML element or attribute exists that provides the semantics you need. ARIA is a last resort, not a first choice.

- Use ARIA only for custom components that have no native HTML equivalent (tab panels, tree views, custom comboboxes).
- **Roles** define what an element IS: `role="tablist"`, `role="alert"`, `role="status"`, `role="dialog"`. Apply roles only when you cannot use the native element.
- **States** define the current condition of an element: `aria-expanded="true|false"`, `aria-selected="true|false"`, `aria-pressed="true|false"`. Update these dynamically as the UI changes.
- **Properties** define relationships between elements: `aria-labelledby`, `aria-describedby`, `aria-controls`, `aria-owns`. Use these to connect related content that is not adjacent in the DOM.
- NEVER use `aria-label` to override visible text. This creates a mismatch where screen reader users hear one thing while sighted users see another, violating WCAG 2.5.3 (Label in Name).
- For dynamic UI updates (toasts, notifications, live regions), use `role="status"` or `aria-live="polite"`. Content injected into these regions is announced by screen readers without interrupting the user.
- Reserve `aria-live="assertive"` strictly for critical interruptions: form validation errors, time-sensitive alerts, or session expiration warnings. Overusing assertive announcements degrades the experience.

## Keyboard Navigation (Non-Negotiable)

EVERY interactive element must be reachable and operable via keyboard alone. This is not optional — it is a Level A requirement.

- **Tab**: Move between focusable elements in document order.
- **Enter/Space**: Activate buttons, follow links, toggle checkboxes.
- **Escape**: Close modals, dismiss popups, exit expanded menus.
- **Arrow keys**: Navigate within composite widgets (tabs, menus, listboxes, radio groups).
- Tab order must follow the visual reading order. Use logical DOM order to achieve this. Do NOT rely on `tabindex` hacks to reorder focus.
- `tabindex="0"` adds an element to the natural tab order. Use this on custom interactive elements that are not natively focusable.
- `tabindex="-1"` makes an element programmatically focusable (via `element.focus()`) but removes it from the tab order. Use this for focus management targets like headings or containers that receive focus after navigation.
- NEVER use `tabindex` greater than 0. It overrides the natural tab order and creates unpredictable navigation that confuses all keyboard users.

## Focus Management

### Modals and Dialogs

- Use the native `<dialog>` element whenever possible. It provides focus trapping, Escape to close, and `aria-modal` behavior automatically.
- If you build a custom modal, you must trap focus inside it while open. Tab must cycle through interactive elements within the modal and never escape to the page behind it.
- When a modal closes, return focus to the element that triggered it. Users must not lose their place on the page.
- Set initial focus to the first interactive element inside the dialog, or to the dialog heading if no interactive element is immediately relevant.
- Apply `aria-modal="true"` on custom dialog elements to signal to assistive technology that content behind the dialog is inert.

### Focus Indicators (WCAG 2.2 Requirement)

- Focus indicators must be highly visible. Provide a minimum 2px solid outline around the full perimeter of the focused element.
- NEVER remove the default outline with `outline: none` without providing a custom focus style that meets contrast requirements.
- Focus indicators must not be fully obscured by sticky headers, cookie banners, floating action buttons, or any other overlapping content. If a focused element scrolls behind a sticky element, the user loses track of where they are.
- Use `:focus-visible` (not `:focus`) for custom focus styles. This shows outlines only for keyboard users while hiding them for mouse clicks, providing the best experience for both input methods.
- Custom focus style example: use a contrasting color, 2px+ solid outline, and an offset for visibility against the element's background.

### View Transitions

- When using Astro's `<ClientRouter />` (view transitions), focus management can break on page navigation. The browser may leave focus in a stale position or reset it to the document body.
- After a view transition completes, ensure focus moves to the main content area or the page title so keyboard users can continue navigating from a logical position.
- Test keyboard navigation across every page transition in your application. Use `astro:page-load` event to programmatically manage focus after transitions complete.

## Target Size (WCAG 2.2 New Requirement)

All interactive click/tap targets must be at least 24x24 CSS pixels (WCAG 2.5.8 Target Size Minimum).

- This applies to buttons, links, form inputs, checkboxes, radio buttons, icon buttons, and any other tappable element.
- Inline text links within paragraphs are exempt from this requirement.
- For small icons or compact controls, add padding to increase the hit area without changing the visual appearance:

```css
.icon-button {
  min-width: 24px;
  min-height: 24px;
  padding: 4px; /* Increases tap target beyond visual bounds */
}
```

- Test on actual touch devices. Desktop pointer precision is much higher than mobile finger taps.

## Images and Media

- ALWAYS provide meaningful `alt` text that describes the purpose and context of the image, not just its appearance. Write "Submit order form" not "green button."
- For decorative images that add no information, use `alt=""` (empty string). Do NOT omit the `alt` attribute entirely — that causes screen readers to announce the file name.
- For complex images (charts, graphs, diagrams), use `aria-describedby` pointing to a detailed text description elsewhere on the page.
- Astro's `<Image />` component requires the `alt` attribute — this is enforced at build time. Treat build errors about missing `alt` as accessibility defects, not annoyances.
- Provide captions and transcripts for all video content. Provide transcripts for all audio content.

## Forms

- EVERY form input must have an associated `<label>` element. Use the `for` attribute on the label matching the `id` on the input. Placeholder text is NOT a substitute for a label.
- Group related inputs (like address fields or radio button sets) with `<fieldset>` and `<legend>`. The legend provides context that individual labels cannot.
- Associate error messages with their inputs using `aria-describedby` on the input pointing to the error message element's `id`. Screen readers announce the error when the user focuses the input.
- Mark required fields with the `required` attribute AND a visible indicator (asterisk, "(required)" text). Do not rely on color alone to indicate required status.
- Astro Actions provide built-in form handling with progressive enhancement. Combine them with proper labeling and error association patterns.
- For live validation feedback, inject error text into an `aria-live="polite"` region so screen readers announce validation results without requiring the user to navigate to the error.

## Astro-Specific Accessibility Patterns

### Islands and Hydration

- Components without `client:*` directives render as static HTML. They are inherently accessible because they require no JavaScript to present their content.
- `client:only="react|vue|svelte"` components have NO server-rendered HTML. Screen readers see nothing until JavaScript loads and executes. This creates a blank gap in the accessibility tree during loading.
- Prefer server-rendered content with progressive enhancement (`client:load`, `client:visible`, `client:idle`) over `client:only`. Server rendering ensures content is available immediately in the accessibility tree.
- Provide meaningful fallback content or loading indicators for islands that take time to hydrate. A blank space with no announcement confuses assistive technology users.

### Content Collections

- Markdown rendered from Content Collections preserves heading hierarchy automatically. Ensure content authors maintain proper heading levels (`h1` to `h2` to `h3`, never skipping from `h1` to `h3`).
- Auto-generated IDs on headings enable anchor linking, which benefits all users including those using assistive technology to navigate by heading.
- Validate heading structure in your content pipeline. Consider a remark plugin that warns on skipped heading levels.

## Testing Requirements (Non-Negotiable)

### Automated Testing (Catches 30-40% of Issues)

- Integrate axe-core into your test suite and CI pipeline. Automated tests catch structural issues reliably and prevent regressions.
- Use `@axe-core/playwright` for end-to-end accessibility testing against your built pages.
- Configure your CI pipeline to fail builds on: missing form labels, color contrast failures, invalid ARIA attributes, missing alt text, and duplicate IDs.
- Run Lighthouse accessibility audit in CI against the production build. Set a minimum score threshold (aim for 100, accept no lower than 95).

### Manual Testing (Catches the Remaining 60-70%)

- Perform a 20-minute keyboard-only navigation test on every critical user journey before shipping. No mouse, no trackpad.
- Tab through the entire page flow. Verify logical order, visible focus indicators, no focus traps (except intentional ones in modals), and that all interactive elements are reachable.
- Conduct a screen reader walkthrough using NVDA on Windows/Firefox, VoiceOver on macOS/Safari, or TalkBack on Android/Chrome. Each combination exposes different issues.
- Verify that dynamic content (toast notifications, modal dialogs, form validation errors, live updates) is announced properly by the screen reader without requiring manual navigation to the updated region.

## Accessibility Checklist

Before shipping any page or component, verify all of the following:

1. All interactive elements are keyboard-accessible (Tab, Enter, Space, Escape, Arrow keys as appropriate)
2. Logical tab order with no `tabindex` greater than 0
3. Focus indicators are visible with minimum 2px perimeter outline
4. All images have appropriate alt text (meaningful or empty for decorative)
5. Forms have labels, fieldsets for groups, and error messages associated via `aria-describedby`
6. Modals trap focus while open and return focus to the trigger on close
7. All interactive targets are at least 24x24 CSS pixels
8. Native HTML elements are used instead of styled divs for interactive controls
9. ARIA is used only when no native HTML element provides the needed semantics
10. Dynamic updates use `aria-live` regions for screen reader announcements
11. axe-core runs in the CI pipeline with builds failing on violations
12. Manual keyboard and screen reader testing is completed for every critical user flow
