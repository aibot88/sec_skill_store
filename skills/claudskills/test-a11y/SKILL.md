---
name: test-a11y
description: "[Tier 2 — Non-Functional: Usability · ISO 25010] Accessibility test workflow — WCAG 2.1 AA compliance via axe-core + Playwright. Creates tests if missing, augments if exists. Run after Tier 1 functional tests pass."
---

# Helix — Accessibility Test (a11y)

> 📚 **Knowledge References** (loaded automatically):  
> `a11y-patterns.md` — WCAG rules, axe violation types, common fixes

ตรวจ WCAG 2.1 violations อัตโนมัติ — จับปัญหา contrast, labels, keyboard nav ก่อน user รายงาน

## Step 1: Repo Structure Check

```bash
# หา a11y test folder
find . -type d \( -name "a11y" -o -name "accessibility" \) \
  | grep -v node_modules | grep -v .git

# ตรวจว่า Playwright + axe ติดตั้งแล้วไหม
cat package.json 2>/dev/null | grep -E "playwright|axe-playwright|@axe-core"
npx playwright --version 2>/dev/null || echo "playwright not installed"
```

### กรณี A: ยังไม่มี a11y test

ต้องการ Playwright + axe-core/playwright:

```bash
# ถ้ายังไม่มี Playwright — แจ้ง user ก่อน (browser download ~250MB)
npm init playwright@latest

# เพิ่ม axe integration (ฟรี)
npm install -D @axe-core/playwright
```

สร้าง structure:
```
tests/a11y/
├── pages/           ← list of pages/routes to scan
└── specs/
    └── accessibility.spec.ts
```

### กรณี B: มี Playwright แล้ว

เพิ่ม axe เข้าไปใน setup ที่มีอยู่:
```bash
npm install -D @axe-core/playwright
```
แล้วสร้าง `tests/a11y/` หรือเพิ่มเข้าใน `tests/e2e/` เดิม

## Step 2: Test Case Planning

สแกนทุก page/route สำคัญ:

```
| Page / Route | Auth required? | WCAG level | Priority |
|-------------|---------------|------------|---------|
| /           | No  | AA | High |
| /login      | No  | AA | High |
| /dashboard  | Yes | AA | High |
| /settings   | Yes | AA | Medium |
```

## Step 3: Write Tests

```typescript
// tests/a11y/specs/accessibility.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const PAGES = [
  { name: 'Home',      path: '/',          auth: false },
  { name: 'Login',     path: '/login',     auth: false },
  { name: 'Dashboard', path: '/dashboard', auth: true  },
  { name: 'Settings',  path: '/settings',  auth: true  },
];

for (const page of PAGES) {
  test(`${page.name} has no WCAG violations`, async ({ page: playwright }) => {
    if (page.auth) {
      // use stored auth state (same as E2E)
      await playwright.context().addCookies(/* auth cookies */);
    }
    await playwright.goto(page.path);
    await playwright.waitForLoadState('networkidle');

    const results = await new AxeBuilder({ page: playwright })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
      .analyze();

    expect(results.violations).toEqual([]);
  });
}
```

**การ handle known violations ที่ยังแก้ไม่ได้:**
```typescript
const results = await new AxeBuilder({ page })
  .withTags(['wcag2a', 'wcag2aa'])
  .exclude('#third-party-widget')  // ระบุ element ที่ข้าม
  .analyze();
```

## Step 4: Run & Fix

```bash
npx playwright test tests/a11y/ --reporter=html
```

เมื่อมี violations:
1. อ่าน violation description — axe บอก rule ID + element + วิธีแก้
2. ดู `results.violations[0].helpUrl` — link ไปยัง WCAG documentation
3. แก้ใน source code
4. Re-run เฉพาะหน้าที่ fail ก่อน
5. Re-run ทั้งหมด

รายงานทุก 10 นาที:
```
| Page | Violations | Severity | Fixed |
|------|-----------|---------|-------|
```

## Severity Levels

| Impact | ความหมาย | Action |
|--------|---------|--------|
| `critical` | ทำให้ user บางกลุ่มใช้ไม่ได้เลย | แก้ก่อน merge |
| `serious` | ขัดขวาง user อย่างมีนัยสำคัญ | แก้ใน sprint นี้ |
| `moderate` | ทำให้ยากขึ้น แต่ยังใช้ได้ | แก้ใน sprint ถัดไป |
| `minor` | best practice | ทำได้ตามโอกาส |

## Done

แจ้ง user ผลสรุป violations ตาม page + severity  
ถามว่าต้องการต่อ `/helix:test-visual` ไหม

## HTML Report

```bash
# รัน พร้อม HTML report
npx playwright test --reporter=html

# เปิด report
npx playwright show-report
```

---

## Self-Evaluation Loop

ก่อนส่ง output ให้ user ทำ self-check ทุกครั้ง:

```
1. Output ครบถ้วนตาม scope ที่รับมาไหม?
2. มีจุดไหนที่ยังไม่แน่ใจ ควรถามก่อนไหม?
3. Format ถูกต้องตามที่กำหนดในสกิลไหม?
4. มีอะไรที่อาจทำให้งานพัง / เกิด side effect ที่ไม่ตั้งใจไหม?
```

ตอบ "ไม่ใช่" ข้อไหน → **แก้ก่อนส่ง** เสมอ
