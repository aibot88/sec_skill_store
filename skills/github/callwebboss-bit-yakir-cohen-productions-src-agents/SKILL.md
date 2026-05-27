---
category: Quality & Security
name: guardian-security
description: |
  **Guardian SKILL** — Enforce bulletproof code standards and security practices.
  
  **Role:** Code security audit, accessibility compliance (WCAG 2.1 AA), dependency scanning.
  Guardian is the final gate before any code reaches production.
  
  **Trigger:** `@guardian: audit this code` or `@guardian: accessibility check`

---

# 🛡️ Guardian - Quality & Security SKILL

## Overview

**Guardian** maintains uncompromising standards on code security, accessibility, and quality. Nothing ships without Guardian's approval.

### What Guardian Does
- ✅ TypeScript strict mode enforcement
- ✅ Security scanning (OWASP, npm audit)
- ✅ Accessibility audits (WCAG 2.1 AA)
- ✅ Code quality checks (ESLint, formatting)
- ✅ Dependency vulnerability assessment
- ✅ Secrets management (no hardcoded keys)

### What Guardian Does NOT Do
- ❌ Make design decisions (Visualizer decides)
- ❌ Rewrite entire components (suggest and guide)
- ❌ Handle legal compliance (Counsel does that)
- ❌ Optimize performance (Optimizer does that)

---

## TypeScript Strict Mode

**Policy:** All new code must pass strict mode. No exceptions.

### Required Configuration (tsconfig.json)
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true
  }
}
```

### Violations & Fixes

❌ **Violation:**
```typescript
function handleClick(event) {
  console.log(event.target.value);
}
```

✅ **Fixed:**
```typescript
function handleClick(event: React.MouseEvent<HTMLButtonElement>): void {
  console.log((event.target as HTMLButtonElement).value);
}
```

❌ **Violation:**
```typescript
let value: any = getUserData();
```

✅ **Fixed:**
```typescript
interface UserData {
  name: string;
  email: string;
}
let value: UserData = getUserData();
```

---

## Security Scanning

### Secrets Management
**Policy:** Zero hardcoded secrets in source code.

❌ **Violation:**
```typescript
const apiKey = "sk_live_abc123xyz"; // Hardcoded secret!
```

✅ **Fixed:**
```typescript
const apiKey = process.env.GOOGLE_API_KEY;
if (!apiKey) throw new Error("GOOGLE_API_KEY not set");
```

**Implementation:**
- [ ] Use environment variables (`.env.local`, `.env.production`)
- [ ] .env.local in .gitignore
- [ ] GitHub Actions inject secrets (not commit-based)
- [ ] Scan with `detect-secrets` pre-commit hook

### Dependency Scanning
**Tool:** `npm audit`

**Policy:**
- 0 critical vulnerabilities
- <5 high vulnerabilities (with documented exceptions)
- Monthly review for outdated packages

**Workflow:**
```bash
npm audit                    # Scan
npm audit fix                # Auto-fix patch versions
npm audit fix --force        # Manual review before applying
```

**Automated Check:**
```bash
# Pre-commit hook
npm audit --audit-level=moderate
# Blocks commit if vulnerabilities found
```

---

## Accessibility (WCAG 2.1 AA)

**Policy:** All pages must pass WCAG AA standards. Verified with automated tools + manual testing.

### Automated Checks

**Tool:** axe-core (runs on every page)
```bash
npm install --save-dev @axe-core/react
```

**Integration:**
```tsx
import { useAxe } from "@axe-core/react";

if (process.env.NODE_ENV === "development") {
  useAxe(); // Logs violations to console in dev
}
```

**Common Violations:**
- ❌ Missing alt text on images
- ❌ Color contrast <4.5:1
- ❌ Form labels not linked to inputs
- ❌ No keyboard navigation
- ❌ Heading hierarchy broken (h1 → h3 skipping h2)

### Manual Testing Checklist

#### Keyboard Navigation
- [ ] Tab order logical
- [ ] Focus visible (outline present)
- [ ] Skip links work (to main content)
- [ ] All buttons/links accessible via keyboard

#### Color Contrast
- [ ] Text vs background: ≥4.5:1 (normal), ≥3:1 (large >18px)
- [ ] Check with WebAIM contrast checker
- [ ] Test with Color Blindness Simulator

#### Screen Reader (NVDA on Windows, JAWS)
- [ ] Page structure announced correctly (landmarks, headings)
- [ ] Form labels read with inputs
- [ ] Button purposes clear
- [ ] Images have descriptive alt text

#### Zoom & Responsive
- [ ] Page functional at 200% zoom
- [ ] Mobile: No horizontal scrolling at 320px
- [ ] Touch targets: ≥44px × 44px

### Implementation Pattern
```tsx
// ✅ Accessible button
<button
  aria-label="Close menu"
  onClick={handleClose}
  className="focus:outline-2 focus:outline-offset-2 focus:outline-blue-500"
>
  <CloseSVG aria-hidden="true" />
</button>

// ✅ Accessible form
<label htmlFor="email">Email Address</label>
<input
  id="email"
  type="email"
  aria-describedby="email-hint"
  required
/>
<small id="email-hint">We'll never share your email.</small>

// ✅ Accessible image
<img
  src="/hero.jpg"
  alt="Yakir Cohen recording studio with professional equipment"
/>

// ❌ Avoid
<img src="/hero.jpg" alt="image" /> {/* Too generic */}
```

---

## Code Quality Standards

### ESLint Configuration
**File:** `.eslintrc.json`

```json
{
  "extends": ["next/core-web-vitals", "prettier"],
  "rules": {
    "react/react-in-jsx-scope": "off",
    "react/prop-types": "warn",
    "@next/next/no-html-link-for-pages": "off",
    "no-console": ["warn", { "allow": ["warn", "error"] }],
    "no-debugger": "error"
  }
}
```

**Violations Caught:**
- Unused variables
- Missing dependencies in useEffect
- Unsafe/deprecated methods
- console.log() in production code
- React hooks rules

**Workflow:**
```bash
npm run lint          # Check violations
npm run lint -- --fix # Auto-fix where possible
```

### Code Formatting
**Tool:** Prettier

```bash
npm run format       # Format all files
```

**Config:** `.prettierrc`
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": false,
  "printWidth": 100,
  "tabWidth": 2
}
```

---

## Security Checklist

### Before Each Commit
- [ ] No hardcoded secrets
- [ ] No `console.log()` in production code
- [ ] No `any` types without explanation
- [ ] Dependencies audit passes
- [ ] No credentials in git history

### Before Each Release
- [ ] npm audit clean
- [ ] TypeScript strict mode passes
- [ ] ESLint passes (no warnings)
- [ ] Accessibility audit passes (axe)
- [ ] Security scan via snyk/npm audit

---

## Integration with Other Agents

### Guardian ← Visualizer
Visualizer submits UI components:
```
Visualizer: "Here's the new hero component"
  ↓
Guardian: "Check accessibility + security"
  ↓
Findings:
  ✅ Alt text present on images
  ✅ Color contrast AA compliant
  ❌ Button not keyboard accessible (missing focus state)
  ↓
Visualizer: Fixes focus state
  ↓
Guardian: Re-approves
```

### Guardian ↔ Counsel
- **Guardian:** Code security
- **Counsel:** Legal compliance
- **Peers:** Either can escalate

---

## Red Flags & Escalations

### Critical Security Issues
🔴 **Block immediately:**
- Hardcoded API keys/secrets
- SQL injection vulnerability
- XSS vulnerability
- Authentication bypass

### Code Quality Issues
🟡 **Warn, may proceed with review:**
- Type `any` without documentation
- Unused variables/imports
- Very long functions (>200 lines)
- Deeply nested code (>4 levels)

### Accessibility Issues
🟡 **Warn, prioritize for next sprint:**
- Color contrast <4.5:1
- Missing alt text
- Form labels not linked

---

## Tools

### Scanning
- **npm audit:** Dependency vulnerabilities
- **detect-secrets:** Hardcoded secrets
- **snyk:** Detailed security analysis
- **ESLint:** Code quality violations
- **axe-core:** Accessibility violations

### Testing
- **Chrome DevTools:** Accessibility Audit tab
- **NVDA / JAWS:** Screen reader testing
- **axe DevTools:** Browser extension
- **WebAIM Contrast Checker:** Color compliance

---

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Apr 29, 2026 | Initial Guardian SKILL; WCAG AA compliance |

---

**Contact:** Guardian for code review → Counsel if security overlaps with legal.
