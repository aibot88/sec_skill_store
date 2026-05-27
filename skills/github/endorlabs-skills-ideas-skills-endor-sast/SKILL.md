---
name: endor-sast
description: >
  Static application security testing for code-level vulnerabilities. Use when the user
  says "SAST scan", "find SQL injection", "check for XSS", "static analysis", "endor
  sast", "code security scan", or wants to find injection flaws, hardcoded credentials,
  and insecure patterns in source code. Do NOT use for dependency vulnerabilities
  (/endor-sca), secrets scanning (/endor-secrets), or viewing pre-computed AI SAST
  findings (/endor-ai-sast).
---

# Endor Labs SAST Scanner

Static application security testing for code-level vulnerabilities.

## Vulnerability Categories

| Category | CWE | Risk |
|----------|-----|------|
| SQL Injection | CWE-89 | Critical |
| Command Injection | CWE-78 | Critical |
| XSS | CWE-79 | High |
| Path Traversal | CWE-22 | High |
| Insecure Deserialization | CWE-502 | High |
| Hardcoded Credentials | CWE-798 | High |
| Weak Cryptography | CWE-327 | Medium |
| Information Disclosure | CWE-200 | Medium |
| CORS Misconfiguration | CWE-942 | Medium |
| Debug Mode in Production | CWE-489 | Medium |

## AI False Positive Reduction

Endor Labs offers AI-powered false positive filtering (requires Code Pro license). Before scanning, ask user if they want to enable it:

- **Without AI** (default): Faster, may include false positives
- **With AI** (Code Pro): Slower, filters false positives via AI review

Enable with `--ai-sast-analysis=agent-fallback` flag. If licensing error occurs, explain Code Pro requirement.

## Workflow

### Step 1: Run SAST Scan

Use `scan` MCP tool: `scan_types: ["sast"]`, `scan_options: { "quick_scan": true }`.

The MCP `scan` tool accepts structured JSON only (`path`, `scan_types`, `scan_options`, optional `namespace`); it does **not** pass through arbitrary `endorctl scan` CLI flags such as `--ai-sast-analysis`. Use the CLI fallback below for AI false-positive reduction.

CLI fallback:
```bash
# Standard
npx -y endorctl scan --path $(pwd) --sast --output-type summary 2>/dev/null

# With AI false positive reduction
npx -y endorctl scan --path $(pwd) --sast --ai-sast-analysis=agent-fallback --output-type summary 2>/dev/null
```

### Step 2: Retrieve Details

Use `get_resource` (resource_type: `Finding`) for each finding UUID from scan results.

### Step 3: Analyze Code Context

Read source files referenced in findings. Show vulnerable code with surrounding context using file path and line numbers.

### Step 4: Present Results

```markdown
## SAST Analysis Results

**Path:** {path} | **Issues:** {count} | **AI FP Reduction:** {Enabled/Disabled}

### Critical Issues

#### {Issue #1}: {Title} ({CWE-ID})
**File:** {path}:{line} | **Severity:** Critical

**Vulnerable Code:**
```{lang}
{code snippet with line numbers}
```

**Why dangerous:** {brief explanation}

**Fix:**
```{lang}
{fixed code}
```

### Summary

| Severity | Count | Categories |
|----------|-------|------------|
| Critical | {n} | {list} |
| High | {n} | {list} |
| Medium | {n} | {list} |

### Next Steps
1. Fix critical issues first
2. `/endor-sast` — Verify fixes
3. `/endor-scan-full` — Full analysis
4. `/endor-review` — Pre-PR check
```

## Language-Specific Secure Patterns

**JS/TS:** `===` not `==`; avoid `eval()`, `Function()`, `setTimeout(string)`; `textContent` not `innerHTML`; `crypto.randomUUID()` not `Math.random()`

**Python:** parameterized queries not f-strings; `subprocess.run([], shell=False)` not `os.system()`; `secrets` module for crypto; avoid `pickle.loads()` on untrusted data

**Go:** `html/template` not `text/template`; `crypto/rand` not `math/rand`; `filepath.Clean()` for paths

**Java:** `PreparedStatement` for SQL; `SecureRandom` for randomness; avoid `Runtime.exec()` with user input

For data source policy, read references/data-sources.md.

## Error Handling

| Error | Action |
|-------|--------|
| No issues found | Confirm scan completed; suggest `/endor-scan-full` for deeper analysis |
| Auth error | Suggest `/endor-setup` |
| Unsupported language | List supported languages and alternatives |
