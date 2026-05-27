---
name: sonar-quality-gate
description: "SonarQube-style quality gate analyzer + auto-fix. Inspects code for Bugs · Vulnerabilities · Security Hotspots · Code Smells · Duplication · Coverage with severity (BLOCKER/CRITICAL/MAJOR/MINOR/INFO) and Reliability/Security/Maintainability ratings A-E. Follows 'Clean as You Code' — focus changes on new code, leave legacy. Use when running quality gate, fixing sonar issues, pre-commit lint, before PR merge, or any code-smell/coverage/duplication/vulnerability check."
---

# Sonar Quality Gate

> **หลักการ:** ใช้วิธีคิดแบบ SonarQube — **issue ประเภท** + **severity** + **rating** + **Clean as You Code** — ไม่ต้องมี SonarQube server ก็ทำได้

## When to use this skill

Trigger keywords (auto-load): **quality gate · sonar · code smell · vulnerability · security hotspot · bug · duplication · coverage · maintainability · reliability · technical debt · clean code · cognitive complexity**

User intent ที่จับ:
- "ตรวจ quality gate ก่อน push"
- "fix sonar issues"
- "code smell ใน file นี้"
- "duplicate code ที่ไหน"
- "coverage ต่ำตรงไหน"
- "ก่อน merge PR ตรวจอะไรบ้าง"

## Core Concepts (อ้างจาก SonarQube)

### 1. Issue Types

| Type | คือ | ตัวอย่าง |
|------|-----|---------|
| **🐛 Bug** | code ที่ผิดหรือทำงานไม่ถูกต้อง | null dereference, off-by-one, unhandled promise rejection |
| **🔓 Vulnerability** | code ที่ exploitable | SQL injection, XSS, hardcoded secret, weak crypto |
| **🔥 Security Hotspot** | ต้อง review โดยมนุษย์ — ไม่ใช่ vuln แน่ ๆ แต่เสี่ยง | use of cookies, regex, random number, file paths from input |
| **👃 Code Smell** | maintainability issue — ไม่ผิด แต่ดูยาก/แก้ยาก | long method, duplicate, dead code, complex conditional, magic number |

### 2. Severity (ลำดับความสำคัญ)

| Level | คำอธิบาย | Action |
|:-----:|---------|--------|
| 🔴 **BLOCKER** | ทำให้ระบบพัง / security ร้ายแรง | **fix ทันที** ห้าม merge |
| 🟠 **CRITICAL** | กระทบ functionality หรือ security สำคัญ | fix ก่อน release |
| 🟡 **MAJOR** | กระทบ quality พอควร | fix ภายใน sprint |
| 🔵 **MINOR** | กระทบเล็กน้อย | fix เมื่อมีเวลา |
| ⚪ **INFO** | recommendation | optional |

### 3. Ratings A-E (per dimension)

| Rating | Reliability (Bugs) | Security (Vulns) | Maintainability (Smells) |
|:------:|:------------------:|:----------------:|:------------------------:|
| **A** | 0 bug | 0 vuln | tech debt ≤ 5% |
| **B** | ≥ 1 MINOR bug | ≥ 1 MINOR vuln | tech debt 6-10% |
| **C** | ≥ 1 MAJOR bug | ≥ 1 MAJOR vuln | tech debt 11-20% |
| **D** | ≥ 1 CRITICAL bug | ≥ 1 CRITICAL vuln | tech debt 21-50% |
| **E** | ≥ 1 BLOCKER bug | ≥ 1 BLOCKER vuln | tech debt > 50% |

### 4. Quality Gate (default — "Sonar Way")

**ผ่าน Quality Gate ต้องครบทุกข้อ (focus on NEW CODE):**

```
[ ] Reliability Rating on New Code  = A      (0 new bugs)
[ ] Security Rating on New Code     = A      (0 new vulnerabilities)
[ ] Security Hotspots Reviewed      = 100%   (review ครบทุก hotspot)
[ ] Maintainability Rating on New   = A      (tech debt ≤ 5%)
[ ] Coverage on New Code            ≥ 80%
[ ] Duplicated Lines on New Code    ≤ 3%
```

> **Clean as You Code:** จัดการ "new code" เป็นหลัก — legacy code ไม่ต้อง fix หมดในรอบเดียว แต่ห้ามเพิ่ม technical debt

### 5. Cognitive Complexity (Sonar's metric)

ไม่ใช่ cyclomatic — Sonar คิดเพิ่มน้ำหนัก nested control flow:

```
+1 ต่อ if/else/switch/for/while/catch/...
+1 ต่อ nesting level (nested → 2, doubly nested → 3)
+1 ต่อ logical operator chain (&& || sequence)
```

Threshold: **method > 15** = MAJOR smell

---

## Workflow: รัน Quality Gate Check

### Step 1 — Scope: NEW vs ALL

```
ถาม / ตรวจ: "ตรวจเฉพาะ diff หรือ ทั้ง codebase?"
- diff (NEW code)      → git diff <base>..HEAD          [Clean as You Code]
- ALL                  → ทั้ง src/                       [baseline scan]
```

### Step 2 — เก็บ Issues 4 ประเภท

ใช้ tools/methods ที่มีอยู่ — ไม่ต้องใช้ SonarQube server:

| Issue Type | วิธีตรวจ (ไม่ต้องใช้ Sonar server) |
|-----------|----------------------------------|
| **🐛 Bug** | ESLint (`error`-level rules), TypeScript strict errors, manual review patterns ใน `references/bug-patterns.md` |
| **🔓 Vulnerability** | `pnpm audit --prod`, grep `references/vuln-patterns.md`, check `08-performance-security.md` checklist |
| **🔥 Security Hotspot** | grep patterns ใน `references/hotspot-patterns.md` (cookies, regex, random, file path) |
| **👃 Code Smell** | ESLint (`warn`-level), cognitive complexity calc, duplicate detection, dead code |
| **Coverage** | `pnpm test --coverage` → ดู %statements บน new file |
| **Duplication** | `jscpd` หรือ regex check ของ block ≥ 10 บรรทัดเหมือนกัน |

### Step 3 — จัด Severity + คำนวณ Rating

ตามตาราง Core Concept #2-3

### Step 4 — Check Quality Gate

ตามตาราง Core Concept #4 — ทุกข้อต้องผ่าน "on New Code"

### Step 5 — Report + Auto-fix

รูปแบบ output (เลียนแบบ Sonar dashboard):

```
╭──────────────────────────────────────────────────╮
│  Quality Gate: PASSED / FAILED                   │
├──────────────────────────────────────────────────┤
│  Reliability:      A  ✅  (0 bug on new code)    │
│  Security:         A  ✅  (0 vuln)                │
│  Hotspots Review:  100% ✅                        │
│  Maintainability:  B  ⚠️  (tech debt 7%)          │
│  Coverage:         82% ✅  (target ≥ 80%)         │
│  Duplication:      1.2% ✅ (target ≤ 3%)          │
╰──────────────────────────────────────────────────╯

Issues on new code (3 total):
  🟠 CRITICAL — src/auth/login.ts:42
     [Vulnerability] Hardcoded JWT secret
  🟡 MAJOR — src/utils/parser.ts:88
     [Code Smell] Cognitive complexity 18 (>15) — extract method
  🔵 MINOR — src/components/Form.tsx:23
     [Bug] useEffect missing dependency 'userId'

Auto-fix plan:
  1. login.ts:42 → move to process.env.JWT_SECRET
  2. parser.ts:88 → extract parseToken() helper
  3. Form.tsx:23 → add userId to dep array
```

### Step 6 — Auto-fix (ถ้า user ขอ)

แก้ตามลำดับ severity: **BLOCKER → CRITICAL → MAJOR → MINOR → INFO**

แต่ละ fix:
1. อ่าน rule rationale จาก `references/rules-catalog.md`
2. write fix (`Edit` tool)
3. write unit test กัน regression (ถ้าเป็น bug หรือ vulnerability)
4. log ใน `docs/12-log-issues.md` ถ้า severity ≥ MAJOR
5. re-run quality gate ตรวจซ้ำ

---

## Integration กับ Workflow ของ template

### ก่อน commit
```
1. รัน skill นี้บน git diff (NEW code)
2. ผ่าน Quality Gate → commit
3. fail → fix ตาม severity → commit
```

### ก่อน mark task [x] (DoD)
เพิ่มเข้า `scripts/check-dod.sh`:
- ข้อ 8 (optional): "Quality Gate on new code = PASSED"

### ใน CI (`.github/workflows/quality-pipeline.yml`)
- ใช้ `sonar-scanner` (server-based) ใน Job A — เป็น "production-grade quality gate"
- skill นี้ใช้ **local + lightweight** — ตรวจก่อน push (ไม่ต้องรอ CI)

---

## Reference Files

อ่านได้เมื่อต้องใช้ pattern หรือ rule rationale:

| File | When to read |
|------|-------------|
| `references/issue-types.md` | รายละเอียดเต็มแต่ละ Issue Type + ตัวอย่าง |
| `references/severity-rating.md` | logic การคำนวณ rating A-E จาก issue list |
| `references/quality-gate-conditions.md` | เงื่อนไข Quality Gate "Sonar Way" + custom presets |
| `references/bug-patterns.md` | bug patterns ที่พบบ่อย + วิธีตรวจ |
| `references/vuln-patterns.md` | OWASP Top 10 patterns + grep/regex |
| `references/hotspot-patterns.md` | Security Hotspot ที่ต้อง review (ไม่ auto-fix) |
| `references/smell-patterns.md` | Code Smell ที่พบบ่อย + refactor patterns |
| `references/cognitive-complexity.md` | วิธีคำนวณ Cognitive Complexity |

---

## Anti-Patterns (อย่าทำ)

| ❌ | ✅ |
|----|----|
| fix legacy code ทั้งหมดในครั้งเดียว | Clean as You Code — focus new diff |
| ignore Security Hotspot | review ทุก hotspot — mark "safe" หรือ fix |
| รวม fix หลาย severity ใน 1 commit | แยก commit ตาม severity (BLOCKER ก่อน) |
| auto-fix Security Hotspot โดยไม่ถาม | hotspot ต้อง human review เสมอ |
| สแกน vendor / node_modules | ตรวจเฉพาะ src/ (exclude generated, lib) |

---

## Quick Commands

```bash
# 1. รัน quality gate บน NEW code (diff)
git diff main...HEAD --name-only -- '*.ts' '*.tsx' | xargs <tools>

# 2. รัน coverage
pnpm test --coverage --reporter=json-summary

# 3. รัน dependency audit (vulnerability)
pnpm audit --prod --json

# 4. หา duplicate code (ใช้ jscpd ถ้าติดตั้ง)
npx jscpd src/ --threshold 3 --min-lines 10

# 5. รัน full check ทั้งหมด
bash scripts/quality-check.sh   # (สร้างได้ถ้าต้องการ)
```

---

## Output Contract

skill นี้ output ตามรูปแบบที่กำหนดเสมอ:
1. **Quality Gate verdict** (PASSED/FAILED)
2. **6 metrics dashboard** (rating + value + threshold)
3. **Issues list** เรียงจาก BLOCKER → INFO
4. **Auto-fix plan** (ก่อนทำจริง รอ user OK ถ้า fail หนัก)

---

## Changelog

| version | date | changes |
|---------|------|---------|
| v1.0 | 2026-05-20 | initial — Sonar concepts + workflow integration |
