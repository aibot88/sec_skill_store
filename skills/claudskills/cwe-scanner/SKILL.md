---
name: cwe-scanner
description: Run deterministic CWE Top 25 checks (Semgrep + custom rules) before and after edits to enforce Constitution principle 7 at G2 Validate. Activate on file edits at risk moderate or high.
version: 0.0.1
---

# CWE Scanner

Constitution principle 7 (§4.1) requires every conforming Constitution to map at minimum a subset of the CWE Top 25 (cwe.mitre.org/top25/) and WCAG 2.2 AA to project-local enforcement rules. This skill runs those rules.

## When to invoke

- Before any code edit at risk moderate or high (G2 Validate PreToolUse).
- At G3 Evaluate as part of the deterministic constitutional scan.
- Inside a PR review when scanning a diff.

## Process

1. Read the change's `risk` from the primary record: `.axis/changes/<id>/proposal.md` for Change Records, or `.axis/tasks/<id>.md` for low-risk Task Records. If `low`, skip unless explicitly invoked.
2. Resolve the project's CWE rule set:
   - `.axis/cwe/` (project rules)
   - `constitution.md` "CWE Top 25 Mappings" table (canonical list)
3. Run Semgrep (or equivalent) against changed files: `semgrep --config=.axis/cwe/ <files> --error`.
4. Produce a JSON record per finding: `{ file, line, cwe, rule, severity, evidence }`.
5. Decision (G2 Validate §6.2):
   - Any MUST-tagged violation → block. Output `{"decision": "block", "reason": "<rule>"}` per Claude Code hook conventions.
   - SHOULD violation → require ADR; emit a warning, do not block.
   - At risk high → also require the threat model to be signed before promotion (§8.2).

## Default rule set (CWE Top 25 — 2024 edition)

Implementations expand each in `.axis/cwe/` with project-specific Semgrep rules.

| CWE | Title | Project rule slug |
|---|---|---|
| CWE-79 | XSS | `xss-output-encoding` |
| CWE-787 | Out-of-bounds Write | `bounds-check` |
| CWE-89 | SQL Injection | `sql-injection` |
| CWE-352 | CSRF | `csrf-token` |
| CWE-22 | Path Traversal | `path-traversal` |
| CWE-125 | Out-of-bounds Read | `bounds-check` |
| CWE-78 | OS Command Injection | `command-injection` |
| CWE-416 | Use After Free | `use-after-free` |
| CWE-862 | Missing Authorization | `authz-missing` |
| CWE-434 | Unrestricted Upload | `upload-restrict` |
| CWE-94 | Code Injection | `code-injection` |
| CWE-20 | Improper Input Validation | `input-validate` |
| CWE-77 | Command Injection | `command-injection` |
| CWE-287 | Improper Authentication | `authn-improper` |
| CWE-269 | Improper Privilege Mgmt | `privilege-mgmt` |
| CWE-502 | Deserialization of Untrusted Data | `deserialize-untrusted` |
| CWE-200 | Sensitive Info Exposure | `pii-exposure` |
| CWE-863 | Incorrect Authorization | `authz-incorrect` |
| CWE-918 | SSRF | `ssrf` |
| CWE-119 | Memory Buffer Bounds | `bounds-check` |
| CWE-476 | NULL Pointer Deref | `null-deref` |
| CWE-798 | Hard-coded Credentials | `hardcoded-secret` |
| CWE-190 | Integer Overflow | `int-overflow` |
| CWE-400 | Uncontrolled Resource Consumption | `resource-limit` |
| CWE-306 | Missing Authentication | `authn-missing` |

## Anti-patterns to flag

- Suppressing scanner findings (`# nosemgrep`, `// semgrep-ignore`) without a linked Security ADR.
- Adding code that handles user-controlled data with no entry in the CWE table.
- Skill-injection patterns: skills that exfiltrate environment variables, write outside the workspace, or chain shell calls without need (§10).
