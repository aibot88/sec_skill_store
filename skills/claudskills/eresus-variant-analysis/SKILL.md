---
name: eresus-variant-analysis
description: >
  GHSA/CVE variant analysis workflow for finding similar vulnerability patterns across a codebase.
  Trigger when the user asks to: "find variants of this CVE", "GHSA variant analysis",
  "find similar bugs", "hunt for the same pattern", "are there other places with this vulnerability?",
  or when a known vulnerability is discovered and the user wants to know if the same pattern
  exists elsewhere.
metadata:
  version: "1.0"
  domain: application-security
  mode: variant-analysis
  persona: security-researcher
---

# GHSA / CVE Variant Analysis

## Purpose

When a known vulnerability (GHSA, CVE, or manually discovered bug) is identified, systematically
search the entire codebase for similar patterns. The goal is to find every instance of the same
underlying weakness — not just the one that was reported.

This skill operates like a GitHub Security Lab researcher performing variant analysis after
a vulnerability disclosure.

---

## Workflow

### Phase 1: Decompose the Known Vulnerability

Extract the structural components of the known bug:

1. **Source** — where does attacker-controlled data enter?
2. **Sink** — which dangerous API/function receives the data?
3. **Missing guard** — what validation/sanitization is absent?
4. **Trust boundary** — which trust boundary was violated?
5. **Language pattern** — what does the vulnerable code look like structurally?

Example decomposition:
```
CVE-2024-XXXX:
  Source: HTTP request body → `req.body.username`
  Sink: `db.query("SELECT * FROM users WHERE name = '" + username + "'")`
  Missing guard: No parameterized query, no input sanitization
  Trust boundary: User input → Database query
  Pattern: String concatenation in SQL query construction
```

### Phase 2: Generalize the Pattern

Abstract away specific variable names and file paths to create search queries:

- **Exact sink search** — search for the dangerous function/method name
- **Pattern search** — search for the structural pattern (e.g., string concatenation + SQL keywords)
- **Framework search** — search for framework-specific equivalents

Use `view_file` and `grep_search` to locate all candidate instances.

### Phase 3: Triage Each Match

For every match found, answer these questions:

1. Is the source actually attacker-controlled in this context?
2. Is the sink reachable from the source in the execution flow?
3. Are there mitigations present that neutralize this specific instance?
4. Does the framework provide implicit protection here?

Classify each match:
- **CONFIRMED** — same pattern, exploitable, no mitigation
- **LIKELY** — same pattern, probably exploitable, needs deeper trace
- **MITIGATED** — same pattern exists but protection is present
- **FALSE POSITIVE** — pattern match but not actually exploitable

### Phase 4: Chain Variants

When multiple variants exist, check if they can combine:

- Can variant A bypass a control that protects variant B?
- Do multiple low-severity variants chain into a high-severity exploit?
- Does fixing one variant reveal or enable another?

### Phase 5: Report

For each confirmed variant, report:

```
### Variant: [ID]

**Original CVE/GHSA**: [reference]
**File**: [path]:[line]
**Category**: [Same-function | Same-pattern | Cross-language | Framework-level]

**Vulnerable Code**:
[show the code]

**Exploit Path**:
[source] → [intermediaries] → [sink]

**Impact**: [what an attacker achieves]
**Remediation**: [specific fix for this instance]
```

---

## Variant Categories

| Category | Description | Example |
|----------|-------------|---------|
| Same-function | Same vulnerable function called from different entry points | `exec()` called from 3 different API handlers |
| Same-pattern | Same dangerous pattern in different functions | SQL concatenation in `getUser()`, `getOrder()`, `getProduct()` |
| Cross-language | Same logical flaw in different language implementations | SQLi in both the Python API and the Go microservice |
| Framework-level | Vulnerable pattern in framework/library code affecting multiple consumers | Custom ORM `rawQuery()` method used by 12 models |

---

## Tooling Constraints

Use ONLY these tools for variant search:
- `view_file` — read source code
- `grep_search` — find pattern matches across the codebase

Do NOT use terminal commands like `grep`, `rg`, `ag`, `sed`, `awk`, or any shell-based search.

---

## Integration

Use this skill AFTER discovering an initial vulnerability with:
- `eresus-manual-security-audit` (manual finding)
- `eresus-sast-scanner` (automated finding)
- External advisory (GHSA, CVE, bug bounty report)

Feed confirmed variants INTO:
- `eresus-remediator` (for batch patching)
- `eresus-pr-security-review` (for ongoing monitoring)
