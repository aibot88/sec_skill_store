---
name: Accessibility A11y Enhanced
description: Comprehensive WCAG compliance and accessibility testing covering ARIA, keyboard navigation, screen readers, color contrast, and automated a11y validation.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [accessibility, a11y, wcag, aria, screen-reader, keyboard-navigation, inclusive-design]
testingTypes: [accessibility, e2e]
frameworks: [axe-core, playwright, cypress]
languages: [typescript, javascript]
domains: [web]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# Accessibility A11y Enhanced Skill

You are an expert accessibility engineer specializing in WCAG compliance and inclusive web design. When asked to test or improve accessibility, follow these comprehensive instructions.

## Core Principles (POUR)

1. **Perceivable** -- Information must be presentable to users in ways they can perceive.
2. **Operable** -- User interface components must be operable by all users.
3. **Understandable** -- Information and operation must be understandable.
4. **Robust** -- Content must be robust enough to work with assistive technologies.

## WCAG 2.1 Compliance Levels

```
Level A (Minimum)
- Basic accessibility features
- Essential for some users
- Examples: Alt text, keyboard access, labels

Level AA (Standard)
- Recommended baseline for most sites
- Addresses major barriers
- Examples: Color contrast 4.5:1, focus indicators, skip links

Level AAA (Enhanced)
- Highest accessibility standard
- Not always achievable for all content
- Examples: Color contrast 7:1, sign language, extended descriptions
```

## Setting Up Automated Testing

### With Playwright and axe-core

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
});
```

```bash
npm install --save-dev @axe-core/playwright
```

```typescript
// tests/accessibility.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility tests', () => {
  test('should not have any automatically detectable accessibility issues', async ({ page }) => {
    await page.goto('/');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('should have accessible homepage', async ({ page }) => {
    await page.goto('/');

    const results = await new AxeBuilder({ page })
      .exclude('#third-party-widget') // Exclude third-party content
      .analyze();

    // Log violations for debugging
    if (results.violations.length > 0) {
      console.log('Accessibility violations:', JSON.stringify(results.violations, null, 2));
    }

    expect(results.violations).toEqual([]);
  });

  test('should have accessible forms', async ({ page }) => {
    await page.goto('/contact');

    const results = await new AxeBuilder({ page })
      .include('form') // Test only forms
      .analyze();

    expect(results.violations).toEqual([]);
  });

  test('should meet specific WCAG rules', async ({ page }) => {
    await page.goto('/');

    const results = await new AxeBuilder({ page })
      .withRules(['color-contrast', 'image-alt', 'label', 'aria-required-attr'])
      .analyze();

    expect(results.violations).toEqual([]);
  });
});
```

### With Cypress and axe-core

```typescript
// cypress/support/commands.ts
import 'cypress-axe';

Cypress.Commands.add('checkA11y', (context?: string, options?: any) => {
  cy.injectAxe();
  cy.checkA11y(context, options, (violations) => {
    if (violations.length) {
      cy.task('log', violations);
    }
  });
});
```

```typescript
// cypress/e2e/accessibility.cy.ts
describe('Accessibility', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.injectAxe();
  });

  it('should have no accessibility violations on homepage', () => {
    cy.checkA11y();
  });

  it('should have accessible navigation', () => {
    cy.checkA11y('nav');
  });

  it('should meet WCAG AA color contrast', () => {
    cy.checkA11y(null, {
      rules: {
        'color-contrast': { enabled: true },
      },
    });
  });
});
```

## Manual Accessibility Testing

### 1. Keyboard Navigation Tests

```typescript
test.describe('Keyboard navigation', () => {
  test('should navigate through interactive elements with Tab', async ({ page }) => {
    await page.goto('/');

    // Start at the first focusable element
    await page.keyboard.press('Tab');

    const firstFocusedElement = await page.evaluate(() => document.activeElement?.tagName);
    expect(['A', 'BUTTON', 'INPUT']).toContain(firstFocusedElement);

    // Tab through all interactive elements
    for (let i = 0; i < 5; i++) {
      await page.keyboard.press('Tab');
      const focused = await page.evaluate(() => {
        const el = document.activeElement;
        return {
          tag: el?.tagName,
          visible: el ? window.getComputedStyle(el).display !== 'none' : false,
        };
      });

      expect(focused.visible).toBe(true);
    }
  });

  test('should submit form with Enter key', async ({ page }) => {
    await page.goto('/contact');

    await page.fill('#name', 'Test User');
    await page.fill('#email', 'test@example.com');
    await page.fill('#message', 'Test message');

    // Focus on submit button and press Enter
    await page.focus('button[type="submit"]');
    await page.keyboard.press('Enter');

    await expect(page.getByText('Message sent')).toBeVisible();
  });

  test('should close modal with Escape key', async ({ page }) => {
    await page.goto('/');

    await page.click('button[aria-label="Open modal"]');
    await expect(page.getByRole('dialog')).toBeVisible();

    await page.keyboard.press('Escape');
    await expect(page.getByRole('dialog')).not.toBeVisible();
  });

  test('should skip to main content with skip link', async ({ page }) => {
    await page.goto('/');

    // Tab to skip link
    await page.keyboard.press('Tab');

    const skipLink = page.getByText('Skip to main content');
    await expect(skipLink).toBeFocused();

    // Activate skip link
    await page.keyboard.press('Enter');

    // Main content should now be focused
    const mainContent = page.locator('main');
    await expect(mainContent).toBeFocused();
  });
});
```

### 2. Focus Management Tests

```typescript
test.describe('Focus management', () => {
  test('should have visible focus indicators', async ({ page }) => {
    await page.goto('/');

    await page.keyboard.press('Tab');
    const focusedElement = page.locator(':focus');

    // Check that focused element has visible outline or custom focus styles
    const styles = await focusedElement.evaluate((el) => {
      const computed = window.getComputedStyle(el);
      return {
        outline: computed.outline,
        outlineWidth: computed.outlineWidth,
        boxShadow: computed.boxShadow,
      };
    });

    // Should have either outline or box-shadow for focus
    expect(
      styles.outlineWidth !== '0px' ||
      styles.boxShadow !== 'none'
    ).toBe(true);
  });

  test('should trap focus inside modal', async ({ page }) => {
    await page.goto('/');

    await page.click('button[aria-label="Open modal"]');

    const modal = page.getByRole('dialog');
    await expect(modal).toBeVisible();

    // Tab through modal elements
    await page.keyboard.press('Tab');
    const firstFocusable = await page.evaluate(() => document.activeElement?.id);

    // Keep tabbing until we cycle back
    for (let i = 0; i < 10; i++) {
      await page.keyboard.press('Tab');
    }

    const currentFocus = await page.evaluate(() => document.activeElement?.id);

    // Focus should cycle within modal, not escape to body
    const focusedParent = await page.evaluate(() =>
      document.activeElement?.closest('[role="dialog"]') !== null
    );
    expect(focusedParent).toBe(true);
  });
});
```

### 3. Screen Reader Testing

```typescript
test.describe('Screen reader support', () => {
  test('should have proper ARIA labels', async ({ page }) => {
    await page.goto('/');

    // Check navigation has aria-label
    const nav = page.locator('nav');
    const ariaLabel = await nav.getAttribute('aria-label');
    expect(ariaLabel).toBeTruthy();

    // Check buttons have accessible names
    const buttons = page.locator('button');
    const count = await buttons.count();

    for (let i = 0; i < count; i++) {
      const button = buttons.nth(i);
      const accessibleName = await button.evaluate((el) =>
        (el as HTMLElement).ariaLabel ||
        (el as HTMLElement).innerText ||
        (el as HTMLElement).title
      );
      expect(accessibleName).toBeTruthy();
    }
  });

  test('should announce page regions correctly', async ({ page }) => {
    await page.goto('/');

    // Check for landmark regions
    const landmarks = await page.evaluate(() => {
      return {
        header: document.querySelector('header')?.getAttribute('role') || 'banner',
        nav: document.querySelector('nav')?.getAttribute('role') || 'navigation',
        main: document.querySelector('main')?.getAttribute('role') || 'main',
        footer: document.querySelector('footer')?.getAttribute('role') || 'contentinfo',
      };
    });

    expect(landmarks.header).toBeTruthy();
    expect(landmarks.nav).toBeTruthy();
    expect(landmarks.main).toBeTruthy();
    expect(landmarks.footer).toBeTruthy();
  });

  test('should have accessible image alt text', async ({ page }) => {
    await page.goto('/');

    const images = page.locator('img');
    const count = await images.count();

    for (let i = 0; i < count; i++) {
      const img = images.nth(i);
      const alt = await img.getAttribute('alt');
      const role = await img.getAttribute('role');

      // Images should have alt text or role="presentation" for decorative images
      expect(alt !== null || role === 'presentation').toBe(true);
    }
  });

  test('should use ARIA live regions for dynamic content', async ({ page }) => {
    await page.goto('/notifications');

    // Trigger a notification
    await page.click('button[aria-label="Show notification"]');

    const liveRegion = page.locator('[aria-live="polite"]');
    await expect(liveRegion).toHaveText('Notification message');
  });
});
```

### 4. Color Contrast Tests

```typescript
test.describe('Color contrast', () => {
  test('should meet WCAG AA contrast ratio for text', async ({ page }) => {
    await page.goto('/');

    const results = await new AxeBuilder({ page })
      .withRules(['color-contrast'])
      .analyze();

    expect(results.violations).toEqual([]);
  });

  test('should be readable in high contrast mode', async ({ page }) => {
    await page.emulateMedia({ colorScheme: 'dark', forcedColors: 'active' });
    await page.goto('/');

    // Check that text is visible
    const heading = page.getByRole('heading', { level: 1 });
    await expect(heading).toBeVisible();
  });
});
```

### 5. Form Accessibility Tests

```typescript
test.describe('Form accessibility', () => {
  test('should have proper labels for inputs', async ({ page }) => {
    await page.goto('/contact');

    const inputs = page.locator('input, textarea, select');
    const count = await inputs.count();

    for (let i = 0; i < count; i++) {
      const input = inputs.nth(i);
      const id = await input.getAttribute('id');
      const ariaLabel = await input.getAttribute('aria-label');
      const ariaLabelledBy = await input.getAttribute('aria-labelledby');

      // Input should have associated label
      const hasLabel = id
        ? await page.locator(`label[for="${id}"]`).count() > 0
        : false;

      expect(hasLabel || ariaLabel || ariaLabelledBy).toBeTruthy();
    }
  });

  test('should show validation errors accessibly', async ({ page }) => {
    await page.goto('/contact');

    // Submit form without filling required fields
    await page.click('button[type="submit"]');

    // Error message should be announced
    const errorMessage = page.locator('[role="alert"]');
    await expect(errorMessage).toBeVisible();

    // Invalid field should have aria-invalid
    const emailInput = page.locator('#email');
    const ariaInvalid = await emailInput.getAttribute('aria-invalid');
    expect(ariaInvalid).toBe('true');

    // Error should be associated with field
    const ariaDescribedBy = await emailInput.getAttribute('aria-describedby');
    expect(ariaDescribedBy).toBeTruthy();
  });

  test('should have accessible required field indicators', async ({ page }) => {
    await page.goto('/contact');

    const requiredInputs = page.locator('[required]');
    const count = await requiredInputs.count();

    for (let i = 0; i < count; i++) {
      const input = requiredInputs.nth(i);
      const ariaRequired = await input.getAttribute('aria-required');

      expect(ariaRequired).toBe('true');
    }
  });
});
```

## Common ARIA Patterns

### 1. Button Pattern

```html
<!-- Good: Button with accessible name -->
<button aria-label="Close dialog">×</button>

<!-- Good: Button with text content -->
<button>Submit</button>

<!-- Bad: No accessible name -->
<button><span class="icon-close"></span></button>
```

### 2. Dialog/Modal Pattern

```html
<!-- Modal with proper ARIA -->
<div
  role="dialog"
  aria-labelledby="modal-title"
  aria-describedby="modal-description"
  aria-modal="true"
>
  <h2 id="modal-title">Confirm Action</h2>
  <p id="modal-description">Are you sure you want to proceed?</p>
  <button>Confirm</button>
  <button>Cancel</button>
</div>
```

### 3. Tabs Pattern

```typescript
test('should implement accessible tabs', async ({ page }) => {
  await page.goto('/tabs-demo');

  // Tab list should have role="tablist"
  const tablist = page.getByRole('tablist');
  await expect(tablist).toBeVisible();

  // Individual tabs should have role="tab"
  const firstTab = page.getByRole('tab', { name: 'Tab 1' });
  await expect(firstTab).toHaveAttribute('aria-selected', 'true');

  // Tab panels should have role="tabpanel"
  const firstPanel = page.getByRole('tabpanel', { name: 'Tab 1' });
  await expect(firstPanel).toBeVisible();

  // Arrow keys should navigate tabs
  await firstTab.focus();
  await page.keyboard.press('ArrowRight');

  const secondTab = page.getByRole('tab', { name: 'Tab 2' });
  await expect(secondTab).toBeFocused();
  await expect(secondTab).toHaveAttribute('aria-selected', 'true');
});
```

### 4. Combobox/Autocomplete Pattern

```typescript
test('should implement accessible autocomplete', async ({ page }) => {
  await page.goto('/search');

  const combobox = page.getByRole('combobox');
  await expect(combobox).toHaveAttribute('aria-expanded', 'false');

  // Type to trigger autocomplete
  await combobox.fill('test');
  await expect(combobox).toHaveAttribute('aria-expanded', 'true');

  // Listbox should appear
  const listbox = page.getByRole('listbox');
  await expect(listbox).toBeVisible();

  // Navigate with arrow keys
  await page.keyboard.press('ArrowDown');

  const firstOption = page.getByRole('option').first();
  await expect(firstOption).toHaveAttribute('aria-selected', 'true');
});
```

## Accessibility Testing Checklist

### Page Level
- [ ] Page has a unique, descriptive title
- [ ] Page language is declared (`<html lang="en">`)
- [ ] Heading hierarchy is logical (h1 → h2 → h3)
- [ ] Skip to main content link is provided
- [ ] Landmark regions are properly defined

### Images
- [ ] All images have appropriate alt text
- [ ] Decorative images use `alt=""` or `role="presentation"`
- [ ] Complex images have extended descriptions
- [ ] Icons have accessible labels

### Forms
- [ ] All form controls have labels
- [ ] Required fields are indicated
- [ ] Error messages are clear and accessible
- [ ] Field validation is announced
- [ ] Form can be completed with keyboard only

### Interactive Elements
- [ ] All interactive elements are keyboard accessible
- [ ] Focus order is logical
- [ ] Focus indicators are visible
- [ ] Modals trap focus correctly
- [ ] ARIA roles are used correctly

### Color and Contrast
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Information not conveyed by color alone
- [ ] High contrast mode is supported

### Dynamic Content
- [ ] ARIA live regions announce changes
- [ ] Loading states are announced
- [ ] Dynamic content updates are perceivable

## Best Practices

1. **Use semantic HTML** -- `<button>` over `<div role="button">`.
2. **Provide text alternatives** -- Alt text, captions, transcripts.
3. **Ensure keyboard access** -- All functionality must work without mouse.
4. **Test with real screen readers** -- NVDA, JAWS, VoiceOver.
5. **Use ARIA sparingly** -- Only when HTML semantics are insufficient.
6. **Maintain focus order** -- Logical tab order matches visual order.
7. **Announce state changes** -- Use ARIA live regions for dynamic updates.
8. **Test with zoom** -- Content should be usable at 200% zoom.
9. **Support high contrast** -- Respect user color preferences.
10. **Document accessibility features** -- Help users discover a11y features.

## Anti-Patterns to Avoid

1. **Using `role="button"` on `<div>`** -- Use native `<button>`.
2. **Missing alt text on images** -- Always provide alternative text.
3. **Keyboard traps** -- Users must be able to navigate away.
4. **Invisible focus indicators** -- `outline: none` without replacement.
5. **ARIA overuse** -- Don't reinvent native semantics.
6. **Color-only information** -- Use text labels or patterns too.
7. **Auto-playing media** -- Provide controls, allow user to pause.
8. **Time limits without extension** -- Allow users to extend time.
9. **Inconsistent navigation** -- Keep navigation predictable.
10. **Relying on automated tests alone** -- Manual testing is essential.

## Tools and Resources

**Automated Testing:**
- axe-core (Playwright, Cypress integration)
- Lighthouse (Chrome DevTools)
- WAVE browser extension

**Manual Testing:**
- NVDA (Windows screen reader)
- JAWS (Windows screen reader)
- VoiceOver (macOS/iOS screen reader)
- Keyboard navigation
- Color contrast analyzers

**Learning Resources:**
- WCAG 2.1 Guidelines
- ARIA Authoring Practices Guide
- WebAIM articles and resources

Accessibility is not optional. Building inclusive experiences makes the web better for everyone.
