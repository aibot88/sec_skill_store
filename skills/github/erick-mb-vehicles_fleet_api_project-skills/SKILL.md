---
name: frontend-vanilla-admin
description: Vanilla HTML/CSS/JS admin interface development for Fleet Management. Use for creating dashboard, CRUD tables, forms, modals, and E2E tests without frameworks.
---

# Frontend Development Standards (Vanilla HTML/CSS/JS)

## Technology Stack
- **HTML5:** Semantic markup only
- **CSS3:** Custom properties (variables), Grid/Flexbox, BEM naming
- **JavaScript:** ES6+ modules, vanilla Web APIs (Fetch, DOM)
- **Testing:** Playwright for E2E tests
- **Containerization:** Served via Python http.server or similar during development

## Architecture Philosophy

### No Frameworks ≠ Less Structure
Frameworks abstract structure. Here, **we define structure explicitly**:
- Clear separation of concerns (HTML, CSS, JS)
- Reusable components built with functions
- Single responsibility per file/component
- Modularity through ES6 imports

This mirrors your backend architecture (services, repositories, routes) but in the browser.

---

## File Organization

### Directory Structure
```
frontend/
├── index.html              # Dashboard page
├── vehicles.html           # Vehicles CRUD page
├── drivers.html            # Drivers CRUD page
├── assignments.html        # Assignments CRUD page
│
├── css/
│   ├── main.css           # Global: reset, variables, typography
│   ├── components.css     # Reusable: button, form, card, modal, table
│   └── pages/
│       ├── dashboard.css  # Dashboard-specific overrides
│       ├── crud.css       # CRUD table pages (vehicles, drivers, assignments)
│       └── modals.css     # Modal-specific styles
│
└── js/
    ├── main.js            # App initialization, routing, shared utilities
    ├── api-client.js      # Centralized Fetch API wrapper
    │
    ├── components/        # Reusable JS components
    │   ├── modal.js       # Modal component (constructor pattern)
    │   ├── table.js       # Table component (CRUD operations)
    │   └── form.js        # Form component (validation, submission)
    │
    └── pages/             # Page-specific logic (import components)
        ├── dashboard.js   # Dashboard: display stats
        ├── vehicles.js    # Vehicles: CRUD operations
        ├── drivers.js     # Drivers: CRUD operations
        └── assignments.js # Assignments: CRUD operations
```

**Why this structure:**
- Each HTML file is a page (easy to navigate)
- CSS organized by scope (global → components → pages)
- JS organized by reusability (shared components → page logic)
- Clear data flow: user clicks → page script → component → api-client → backend

---

## HTML Standards

### Semantic Markup
Use semantic HTML elements instead of `<div>` everywhere. This helps:
- Accessibility (screen readers understand structure)
- SEO (search engines understand content)
- readability (your code is self-documenting)

**Good (semantic):**
```html
<nav>
  <a href="/">Dashboard</a>
  <a href="/vehicles.html">Vehicles</a>
</nav>

<main>
  <h1>Fleet Dashboard</h1>
  <section id="stats">
    <article class="stat">
      <h2>Total Vehicles</h2>
      <p id="vehicle-count">0</p>
    </article>
  </section>
</main>

<form id="create-vehicle">
  <label for="placa">License Plate</label>
  <input type="text" id="placa" name="placa" required>
  <button type="submit">Create</button>
</form>
```

**Bad (no semantics):**
```html
<div class="nav">
  <div class="link"><a href="/">Dashboard</a></div>
</div>
<div class="container">
  <div class="title">Fleet Dashboard</div>
  <div class="stats">
    <div class="stat">Total Vehicles: <span id="vehicle-count">0</span></div>
  </div>
</div>
```

### Accessibility in HTML
- **Always use `<label>` with forms:** Connects label to input, clickable on label text
- **Use `for` attribute:** `<label for="placa">` matches `<input id="placa">`
- **Semantic headings:** Use `<h1>`, `<h2>`, `<h3>` in order (not for styling)
- **ARIA labels:** For icon buttons, info icons, etc.
  ```html
  <button aria-label="Close modal">✕</button>
  <span aria-label="Loading spinner">⟳</span>
  ```
- **Alt text for images:** Always (even if decorative, use `alt=""`)

---

## CSS Standards

### CSS Custom Properties (Variables)
Define colors, spacing, fonts once in `main.css`, reuse everywhere:

```css
:root {
  /* Colors */
  --color-primary: #007bff;
  --color-success: #28a745;
  --color-danger: #dc3545;
  --color-text: #333;
  --color-border: #ddd;
  
  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 2rem;
  
  /* Typography */
  --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-size-base: 1rem;
  --font-size-sm: 0.875rem;
  --font-size-lg: 1.125rem;
  
  /* Transitions */
  --transition-fast: 100ms ease-in-out;
  --transition-base: 200ms ease-in-out;
}

/* Usage */
body {
  font-family: var(--font-family);
  color: var(--color-text);
}

.button {
  background-color: var(--color-primary);
  padding: var(--spacing-md) var(--spacing-lg);
  transition: background-color var(--transition-base);
}
```

### BEM Naming Convention
**Block-Element-Modifier** = predictable, self-documenting CSS

```css
/* Block (standalone component) */
.button { }
.card { }
.table { }

/* Element (part of block, separated by __) */
.button__text { }
.card__header { }
.table__row { }

/* Modifier (variation, separated by --) */
.button--primary { background-color: var(--color-primary); }
.button--danger { background-color: var(--color-danger); }
.button--disabled { opacity: 0.5; cursor: not-allowed; }

.card--error { border-color: var(--color-danger); }

/* Usage in HTML */
<button class="button button--primary">Submit</button>
<div class="card card--error">Error message</div>
```

### Responsive Design (Mobile-First)
Start with mobile styles, add complexity for bigger screens:

```css
/* Mobile (default, smallest screen) */
.grid { display: block; }
.sidebar { display: none; }

/* Tablet and up */
@media (min-width: 768px) {
  .grid { display: grid; grid-template-columns: 1fr 1fr; }
  .sidebar { display: block; }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .grid { grid-template-columns: 1fr 1fr 1fr; }
}
```

### CSS Organization in Files
**main.css** (global):
```css
* { /* reset */ }
:root { /* variables */ }
body { /* typography */ }
a { /* links */ }
button { /* buttons */ }
/* Repeat for all HTML elements */
```

**components.css** (reusable):
```css
/* Only component classes */
.button { }
.button--primary { }
.button--danger { }
.form { }
.form__field { }
.modal { }
.modal__backdrop { }
/* etc. */
```

**pages/*.css** (page-specific overrides):
```css
/* Only use for page-specific adjustments */
#dashboard .stats { grid-template-columns: 1fr; }
```

---

## JavaScript Standards

### ES6 Modules
Each file exports one "thing" (component, utility, page):

```javascript
// js/components/modal.js
export class Modal {
  constructor(selector) {
    this.element = document.querySelector(selector);
  }
  
  open() {
    this.element.classList.add('modal--open');
  }
  
  close() {
    this.element.classList.remove('modal--open');
  }
}

// js/pages/vehicles.js
import { Modal } from '../components/modal.js';
import { Table } from '../components/table.js';

const vehicleModal = new Modal('#vehicle-modal');
const vehicleTable = new Table('#vehicles-table');

// Usage
document.getElementById('create-btn').addEventListener('click', () => {
  vehicleModal.open();
});
```

### API Client (Centralized)
Single source for all API calls (like your repository layer):

```javascript
// js/api-client.js
class ApiClient {
  constructor(baseUrl = 'http://localhost:8000/api/v1') {
    this.baseUrl = baseUrl;
  }
  
  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const { method = 'GET', body = null, ...rest } = options;
    
    try {
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: body ? JSON.stringify(body) : null,
        ...rest,
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`ApiClient.request(${method} ${endpoint}):`, error);
      throw error;
    }
  }
  
  getVehicles(params = {}) {
    return this.request('/vehicles', { 
      method: 'GET',
      // Optional: add query params if needed
    });
  }
  
  createVehicle(data) {
    return this.request('/vehicles', { 
      method: 'POST',
      body: data
    });
  }
  
  updateVehicle(id, data) {
    return this.request(`/vehicles/${id}`, { 
      method: 'PUT',
      body: data
    });
  }
  
  deleteVehicle(id) {
    return this.request(`/vehicles/${id}`, { 
      method: 'DELETE'
    });
  }
}

export const apiClient = new ApiClient();

// Usage in page
import { apiClient } from '../api-client.js';

apiClient.getVehicles()
  .then(vehicles => renderTable(vehicles))
  .catch(error => showError('Failed to load vehicles'));
```

### Component Pattern
Reusable components as constructor functions with methods:

```javascript
// js/components/table.js
export class Table {
  constructor(selector) {
    this.element = document.querySelector(selector);
    this.rows = [];
  }
  
  setData(data) {
    this.rows = data;
    this.render();
  }
  
  render() {
    const tbody = this.element.querySelector('tbody');
    tbody.innerHTML = this.rows.map(row => this.createRow(row)).join('');
    this.attachListeners();
  }
  
  createRow(data) {
    // Return HTML string for row
    return `<tr data-id="${data._id}">
      <td>${data.placa}</td>
      <td>${data.estado_vehiculo}</td>
      <td>
        <button class="btn-edit" data-id="${data._id}">Edit</button>
        <button class="btn-delete" data-id="${data._id}">Delete</button>
      </td>
    </tr>`;
  }
  
  attachListeners() {
    this.element.querySelectorAll('.btn-edit').forEach(btn => {
      btn.addEventListener('click', (e) => this.onEdit(e.target.dataset.id));
    });
    this.element.querySelectorAll('.btn-delete').forEach(btn => {
      btn.addEventListener('click', (e) => this.onDelete(e.target.dataset.id));
    });
  }
  
  onEdit(id) {
    // Emit event or call callback
    this.element.dispatchEvent(new CustomEvent('edit', { detail: { id } }));
  }
  
  onDelete(id) {
    this.element.dispatchEvent(new CustomEvent('delete', { detail: { id } }));
  }
}

// Usage
import { Table } from '../components/table.js';
import { apiClient } from '../api-client.js';

const table = new Table('#vehicles-table');

table.element.addEventListener('edit', (e) => {
  const vehicleId = e.detail.id;
  apiClient.getVehicle(vehicleId).then(vehicle => {
    showEditForm(vehicle);
  });
});

table.element.addEventListener('delete', (e) => {
  if (confirm('Delete vehicle?')) {
    apiClient.deleteVehicle(e.detail.id).then(() => {
      loadTable(); // Refresh
    });
  });
});
```

### Event Delegation
Single listener on parent instead of listeners on every child:

```javascript
// BAD: Create a listener for EACH delete button
document.querySelectorAll('.btn-delete').forEach(btn => {
  btn.addEventListener('click', deleteVehicle);
});

// GOOD: Single listener on table
const table = document.querySelector('#vehicles-table');
table.addEventListener('click', (e) => {
  if (e.target.classList.contains('btn-delete')) {
    deleteVehicle(e.target.dataset.id);
  }
});
```

### State Management (Component-Level)
For simple admin app, keep state at component level (no global store needed):

```javascript
export class Form {
  constructor(selector) {
    this.element = document.querySelector(selector);
    this.data = {}; // Component-level state
    this.setupSubmit();
  }
  
  setupSubmit() {
    this.element.addEventListener('submit', (e) => this.onSubmit(e));
  }
  
  onSubmit(e) {
    e.preventDefault();
    
    // Gather form data
    this.data = new FormData(this.element);
    const body = Object.fromEntries(this.data);
    
    // Validate locally
    if (!this.validate(body)) {
      this.showError('Please fill all required fields');
      return;
    }
    
    // Send to backend
    this.submit(body);
  }
  
  validate(data) {
    // Fail early (same as backend)
    return data.placa && data.placa.length === 6;
  }
  
  async submit(data) {
    this.disableSubmit();
    
    try {
      await apiClient.createVehicle(data);
      this.reset();
      this.showSuccess('Vehicle created');
    } catch (error) {
      this.showError(error.message);
    } finally {
      this.enableSubmit();
    }
  }
  
  disableSubmit() {
    const btn = this.element.querySelector('button[type="submit"]');
    btn.disabled = true;
    btn.textContent = 'Creating...';
  }
  
  enableSubmit() {
    const btn = this.element.querySelector('button[type="submit"]');
    btn.disabled = false;
    btn.textContent = 'Create Vehicle';
  }
}
```

---

## Accessibility (WCAG 2.1 AA)

### Keyboard Navigation
- **Tab:** Navigate between interactive elements
- **Enter:** Submit forms, activate buttons
- **Escape:** Close modals, dropdowns
- **Arrow keys:** Navigate within lists/tables (optional but nice)

**Implementation:**
```html
<!-- Buttons should be focusable -->
<button class="btn">Submit</button>

<!-- Links are focusable by default -->
<a href="/vehicles.html">Vehicles</a>

<!-- Don't forget tabindex for custom interactive elements -->
<div class="custom-button" tabindex="0" role="button">
  Click me
</div>

<!-- Close button gets focus (not just hover) -->
<button class="modal__close" onclick="modal.close()">✕</button>
```

### Focus Indicators
Always show where keyboard user is:
```css
button:focus, input:focus, a:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Remove default ugly outline only if you provide custom one above */
/* Never do: *:focus { outline: none; } without providing alternative */
```

### Color Contrast
Text and background must have sufficient ratio (dark text on light OR light text on dark):
```css
/* WCAG AA: 4.5:1 ratio for normal text */
.text-dark { color: #333; background: white; } /* Good */
.text-light { color: #ccc; background: white; } /* Bad */

/* Use tools: https://webaim.org/resources/contrastchecker/ */
```

### ARIA Labels
For non-text content and icon buttons:
```html
<!-- Icon button needs label -->
<button aria-label="Delete vehicle">🗑</button>

<!-- Loading spinner needs label -->
<span aria-label="Loading" class="spinner">⟳</span>

<!-- Info icon needs explanation -->
<span aria-label="This vehicle is inactive">ℹ</span>

<!-- Custom select needs proper role -->
<div role="combobox" aria-expanded="false">Custom select</div>
```

---

## Error Handling & User Feedback

### Three States for Every Action
1. **Loading:** Disable button, show spinner
2. **Success:** Show success message, reset form
3. **Error:** Show error message, keep form data

```javascript
async function submitForm(data) {
  // STATE 1: Loading
  showSpinner();
  disableSubmit();
  clearMessages();
  
  try {
    // STATE 2: Success
    const result = await apiClient.createVehicle(data);
    showSuccess('Vehicle created successfully');
    resetForm();
  } catch (error) {
    // STATE 3: Error
    showError(`Failed to create vehicle: ${error.message}`);
    console.error('submitForm():', error);
  } finally {
    hideSpinner();
    enableSubmit();
  }
}
```

### Error Messages
- **User-friendly:** "Failed to create vehicle" (not "500 Internal Server Error")
- **Actionable:** "Email is required" (not "Field validation failed")
- **Logged:** console.error() with function name and full error

```javascript
function showError(message) {
  const errorEl = document.getElementById('error-message');
  errorEl.textContent = message;
  errorEl.classList.remove('hidden');
  
  // Scroll to error
  errorEl.scrollIntoView({ behavior: 'smooth' });
}
```

---

## Testing (E2E with Playwright)

### Test Structure: Given-When-Then
```javascript
// tests/vehicles.spec.js
import { test, expect } from '@playwright/test';

test.describe('Vehicles CRUD', () => {
  test('should create a new vehicle', async ({ page }) => {
    // GIVEN: User is on vehicles page
    await page.goto('http://localhost:5500/vehicles.html');
    
    // WHEN: User fills form and clicks create
    await page.fill('#placa', 'ABC1234');
    await page.fill('#numero_economico', 'ECON-001');
    await page.click('button[type="submit"]');
    
    // THEN: Vehicle appears in table
    await expect(page.locator('text=ABC1234')).toBeVisible();
  });
  
  test('should delete a vehicle', async ({ page }) => {
    // GIVEN: Vehicle exists in table
    await page.goto('http://localhost:5500/vehicles.html');
    
    // WHEN: User clicks delete button
    await page.click('button.btn-delete:first-child');
    
    // THEN: Vehicle is removed
    await expect(page.locator('text=ABC1234')).not.toBeVisible();
  });
});
```

### What NOT to Test
- Don't mock API calls (use real backend)
- Don't test CSS pixel-perfect styling (browser renders differently)
- Don't test third-party libraries (assume they work)

### What to Test
- User workflows (create → read → update → delete)
- Error messages display
- Form validation works
- Navigation between pages
- Loading states appear and disappear

---

## Common Patterns

### Modal Form for CRUD
```html
<!-- HTML: Reusable modal structure -->
<div id="vehicle-modal" class="modal">
  <div class="modal__backdrop"></div>
  <div class="modal__content">
    <h2 class="modal__title">Create Vehicle</h2>
    <form id="vehicle-form">
      <!-- Form fields -->
    </form>
    <button class="modal__close" aria-label="Close">✕</button>
  </div>
</div>

<!-- CSS: Modal hidden by default -->
<style>
  .modal {
    display: none;
  }
  
  .modal--open {
    display: flex;
  }
</style>

<!-- JavaScript: Show/hide modal -->
<script>
  const modal = new Modal('#vehicle-modal');
  
  document.getElementById('create-btn').addEventListener('click', () => {
    modal.open();
  });
  
  document.getElementById('vehicle-form').addEventListener('submit', (e) => {
    e.preventDefault();
    // Create vehicle, then close modal
    modal.close();
  });
</script>
```

### Table with Actions
```html
<table id="vehicles-table">
  <thead>
    <tr>
      <th>Placa</th>
      <th>Estado</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    <!-- Rows inserted by JS -->
  </tbody>
</table>

<script>
  const table = new Table('#vehicles-table');
  
  table.element.addEventListener('edit', (e) => {
    const vehicleId = e.detail.id;
    // Load vehicle and show edit modal
  });
  
  table.element.addEventListener('delete', (e) => {
    const vehicleId = e.detail.id;
    // Delete from API and refresh table
  });
</script>
```

---

## What I NEVER Do

❌ **HTML/CSS:**
- NEVER use `<div>` for everything (use semantic elements)
- NEVER inline styles (use CSS classes)
- NEVER forget `<label>` for form inputs
- NEVER skip alt text on images
- NEVER create custom selects without proper ARIA

❌ **JavaScript:**
- NEVER use `eval()` or `innerHTML` with user input (XSS vulnerability)
- NEVER create global variables (use modules)
- NEVER attach many listeners (use delegation)
- NEVER forget to remove listeners (memory leaks)
- NEVER mock API calls in production code

❌ **Accessibility:**
- NEVER skip focus indicators (users can't see where they are)
- NEVER use color alone to communicate (red = error, but also provide text)
- NEVER forget WCAG contrast ratios
- NEVER auto-play audio/video
- NEVER hijack browser keyboard shortcuts

❌ **Performance:**
- NEVER load CSS/JS at bottom of HTML (load CSS in head, JS before closing body)
- NEVER have render-blocking JavaScript
- NEVER refresh entire table (update only changed rows)
- NEVER make multiple API calls in parallel unless necessary

---

## File Template: New Page

When adding a new page, follow this template:

**new-feature.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>New Feature - Fleet Admin</title>
  <link rel="stylesheet" href="css/main.css">
  <link rel="stylesheet" href="css/components.css">
  <link rel="stylesheet" href="css/pages/new-feature.css">
</head>
<body>
  <nav><!-- Navigation --></nav>
  
  <main>
    <h1>New Feature</h1>
    <!-- Page content -->
    <div id="app"></div>
  </main>
  
  <!-- Modals, etc. -->
  
  <script type="module" src="js/pages/new-feature.js"></script>
</body>
</html>
```

**js/pages/new-feature.js**
```javascript
import { apiClient } from '../api-client.js';
import { Table } from '../components/table.js';
import { Modal } from '../components/modal.js';

// Initialize components
const table = new Table('#items-table');
const modal = new Modal('#item-modal');

// Load data
async function loadData() {
  try {
    const items = await apiClient.getItems();
    table.setData(items);
  } catch (error) {
    console.error('loadData():', error);
    // Show error to user
  }
}

// Event listeners
document.getElementById('create-btn').addEventListener('click', () => {
  modal.open();
});

// Load on page load
loadData();
```

---

## Summary

**Frontend Philosophy (aligned with backend):**
1. **Modularity:** Components as functions/classes, not monolith HTML
2. **Clarity:** Semantic HTML + clear CSS class names = self-documenting
3. **Validation:** Fail early on client, validate safely on server
4. **Error handling:** Clear error messages with context
5. **Testing:** Real data, real workflows (E2E with Playwright)
6. **Accessibility:** First-class concern, not afterthought
7. **No over-engineering:** Vanilla is simpler than frameworks for small admin UI

Your admin interface will be lightweight, fast, and maintainable.
