---
name: fireworks-security
description: Security hardening superbrain — CWE Top 25, STRIDE threat modeling, Electron hardening, encryption, dependency audits, OWASP compliance
version: 2.0.0
author: mneme
tags: [security, vulnerability, CWE, OWASP, hardening, encryption, audit, XSS, injection]
triggers: [security, vulnerability, CWE, OWASP, hardening, encryption, audit, credential, XSS, injection, CSP]
---

# Fireworks Security — Enterprise Security Superbrain

## Purpose

This skill consolidates ALL security knowledge into a single reference brain.
It replaces the need to invoke separate security-scanner, security-reviewer,
security-hardener, and encryption agents. One skill, total coverage.

Activate this skill whenever:
- Scanning code for vulnerabilities
- Hardening an Electron app
- Reviewing IPC channels or preload scripts
- Implementing or auditing encryption
- Running dependency audits
- Preparing for a security review or compliance check

---

## 1. Security Scan Protocol — 5-Phase Pipeline

### Phase 1: Target Identification
1. Identify the project type (Electron, Node.js CLI, web app, library).
2. List all entry points: main process, renderer processes, preload scripts, IPC channels, HTTP endpoints.
3. Map the trust boundary: what runs with Node.js privileges vs. sandboxed renderer.
4. Identify all external inputs: user input fields, file uploads, URL parameters, IPC messages, environment variables.

### Phase 2: CWE Top 25 Scan
1. For each CWE in the quick-reference table below, run the detection pattern against the codebase.
2. Log every match with file path, line number, and severity.
3. Cross-reference with `references/cwe-detection.md` for Electron-specific variants.
4. Classify findings: CRITICAL (blocks release), HIGH (must fix before merge), MEDIUM (fix in next sprint).

### Phase 3: STRIDE Threat Modeling
1. For each STRIDE category, answer the guiding question against the project architecture.
2. Document threats discovered with likelihood (HIGH/MEDIUM/LOW) and impact (HIGH/MEDIUM/LOW).
3. Map each threat to a mitigation strategy.

### Phase 4: Auto-Fix Suggestions
1. For each finding from Phase 2, generate a concrete code fix.
2. Fixes must be minimal — change only what is necessary.
3. Each fix must include a before/after code snippet.
4. Never introduce new dependencies without explicit user approval.

### Phase 5: Security Report
1. Generate the report using the format in Section 7.
2. Summary statistics: total findings by severity.
3. Include verification commands the user can run to confirm fixes.

---

## 2. CWE Top 25 Quick-Reference

| CWE ID | Vulnerability | Detection Pattern | Severity |
|--------|--------------|-------------------|----------|
| CWE-787 | Out-of-bounds Write | Buffer operations without bounds checking, `Buffer.alloc` misuse | CRITICAL |
| CWE-79 | Cross-site Scripting (XSS) | `innerHTML`, `dangerouslySetInnerHTML`, `document.write`, `v-html`, `{@html}` | CRITICAL |
| CWE-89 | SQL Injection | String concatenation in SQL queries, template literals in `.run()`, `.exec()`, `.all()` | CRITICAL |
| CWE-416 | Use After Free | Manual memory management in native addons, double `.destroy()` calls | CRITICAL |
| CWE-78 | OS Command Injection | `child_process.exec()` with user input, `shell: true` in spawn options | CRITICAL |
| CWE-20 | Improper Input Validation | Missing Zod/Joi schemas on IPC handlers, unvalidated function arguments | HIGH |
| CWE-125 | Out-of-bounds Read | Array access without length check, Buffer.read beyond size | HIGH |
| CWE-22 | Path Traversal | `path.join` with user input not validated against base directory, `../` in paths | HIGH |
| CWE-352 | Cross-Site Request Forgery | Missing CSRF tokens on mutation endpoints (less relevant for desktop, still check webview) | HIGH |
| CWE-434 | Unrestricted Upload | File dialog without extension filtering, no MIME type validation | HIGH |
| CWE-862 | Missing Authorization | IPC handlers without permission checks, no role-based access on channels | HIGH |
| CWE-476 | NULL Pointer Dereference | Optional chaining missing on potentially null DB results, unchecked `.get()` | MEDIUM |
| CWE-287 | Improper Authentication | Hardcoded credentials, plaintext password storage, missing bcrypt/argon2 | CRITICAL |
| CWE-190 | Integer Overflow | Large number arithmetic without BigInt, unchecked parseInt results | MEDIUM |
| CWE-502 | Deserialization of Untrusted Data | `JSON.parse` on external input without schema validation, `eval()` | CRITICAL |
| CWE-77 | Command Injection | Template strings in exec/spawn commands, unsanitized shell arguments | CRITICAL |
| CWE-119 | Buffer Overflow | Native addon buffer operations, `Buffer.allocUnsafe` without fill | HIGH |
| CWE-798 | Hardcoded Credentials | API keys in source, passwords in config files, tokens in constants | CRITICAL |
| CWE-918 | Server-Side Request Forgery | `fetch`/`axios` with user-controlled URLs, no allowlist validation | HIGH |
| CWE-306 | Missing Authentication | Endpoints/IPC channels without any auth check | HIGH |
| CWE-362 | Race Condition | Shared state mutation without locks, TOCTOU in file operations | MEDIUM |
| CWE-269 | Improper Privilege Management | `nodeIntegration: true`, missing sandbox, elevated permissions | CRITICAL |
| CWE-94 | Code Injection | `eval()`, `new Function()`, `vm.runInNewContext` with user input | CRITICAL |
| CWE-863 | Incorrect Authorization | Role checks with wrong operator, bypassed permission middleware | HIGH |
| CWE-276 | Incorrect Default Permissions | World-writable files, overly permissive file modes on config/data | MEDIUM |

See `references/cwe-detection.md` for complete detection patterns and fix templates.

---

## 3. STRIDE Threat Model

| Category | Guiding Question | Desktop App Examples |
|----------|-----------------|---------------------|
| **S**poofing | Can an attacker pretend to be someone/something else? | Fake IPC messages between renderer and main, spoofed auto-update server, modified preload script |
| **T**ampering | Can an attacker modify data they should not? | Modify SQLite database file on disk, tamper with ASAR archive, alter localStorage, MITM update downloads |
| **R**epudiation | Can an attacker deny performing an action? | No audit log for destructive operations, missing transaction history, no action timestamps |
| **I**nformation Disclosure | Can an attacker access data they should not? | Credentials in plaintext config, sensitive data in renderer console, unencrypted database, verbose error messages exposing internals |
| **D**enial of Service | Can an attacker crash or slow the app? | Infinite loop in IPC handler, massive file upload crashing renderer, uncaught promise rejection crashing main process |
| **E**levation of Privilege | Can an attacker gain higher access? | Renderer escaping sandbox via nodeIntegration, IPC channel granting filesystem access without auth, prototype pollution |

---

---

## Full Reference

For complete patterns, examples, and advanced usage, see [`references/full-guide.md`](./references/full-guide.md).
Read that file when you need deeper context than the summary above.
