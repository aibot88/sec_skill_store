---
name: eresus-remediator
description: >
  Security remediation skill for fixing confirmed or likely SAST findings in source code. Trigger when the user asks to:
  "fix a vulnerability", "patch this security bug", "remediate SAST findings", "harden this endpoint", "make this auth flow safe",
  or wants code changes that remove a confirmed security issue while preserving intended behavior. Best used alongside eresus-sast-scanner.
metadata:
  version: "1.0"
  domain: application-security
  mode: remediation
---

# SAST Remediation

## Purpose

Turn confirmed or likely security findings into safe, minimal, production-ready code changes.
Prefer root-cause fixes over cosmetic mitigations, preserve legitimate behavior, and reduce the
chance of regressions or bypasses.

## Inputs

This skill works best when at least one of the following is available:

- a finding from `eresus-sast-scanner`
- a security review comment or PR thread
- a vulnerable file/function/endpoint
- a proof-of-concept payload or attack path

If `eresus-sast-scanner` is installed, load the matching vulnerability knowledge file(s) from its
`references/` directory before patching.

---

## Workflow

### Step 1: Reconstruct the Vulnerability Path

Before editing code, confirm:

- the attacker-controlled source
- the transformation path
- the vulnerable sink
- the intended business behavior that must still work after the fix

Do not patch from the label alone. Patch the actual code path.

### Step 2: Choose the Right Fix Layer

Prefer the highest-leverage fix that closes the whole class of issue:

| Problem Type | Preferred Fix |
|--------------|---------------|
| SQL / NoSQL injection | Parameterization, safe query builders, strict allowlists |
| XSS | Context-specific output encoding or safe templating APIs |
| SSRF | Destination allowlists, URL parser validation, egress restrictions |
| Path traversal | Canonicalization plus base-directory enforcement |
| Auth / IDOR | Server-side authorization at object/action boundary |
| CSRF | Framework-native CSRF defense, same-site cookies, token checks |
| File upload | Type/content validation, non-webroot storage, random filenames |
| Serialization / deserialization | Explicit DTOs, allowlisted types, safe parser settings, integrity checks |
| Weak crypto | Modern primitives, strong secrets, secure randomness |
| Race conditions | Atomic operations, locking, compare-and-set, transaction boundaries |

Fix at the sink when possible, but move the fix earlier if many sinks share the same unsafe input path.

### Step 3: Implement a Minimal, Safe Patch

While patching:

- preserve public API behavior unless the insecure behavior itself must change
- prefer framework-native security features over custom regex or denylist logic
- keep validation rules explicit and auditable
- update adjacent code when partial fixes would leave equivalent bypasses
- add concise comments only when the security reason is otherwise non-obvious

### Step 4: Add Verification

Add or update tests when the repo supports them. Cover both:

- the blocked attack path
- the expected legitimate flow

If tests are not practical, still perform a manual reasoning pass that explains why the taint path is now broken.

### Step 5: Re-Review the Fix

Run a short post-fix check:

- Can attacker-controlled data still reach the same sink?
- Did the patch move the problem instead of removing it?
- Does sanitization match the exact output context?
- Did the change accidentally create auth, compatibility, or logging regressions?

### Step 6: Report the Remediation

Summarize:

- what was vulnerable
- what changed
- why the new control is effective
- what residual risk or rollout note remains

---

## Remediation Guardrails

- Do not silence findings with comments, feature flags, or dead-code moves unless the execution path is truly removed.
- Do not replace parameterization with string escaping for query sinks.
- Do not trust client-side validation as the primary fix for a server-side issue.
- Do not add broad denylists when a precise allowlist or safer API exists.
- Do not "fix" IDOR by hiding identifiers in the UI; enforce authorization on the server.
- Do not fix SSRF with substring checks alone; parse and validate the normalized destination.
- Do not keep weak password hashing for backward compatibility without a migration or rehash plan.
- Do not claim a fix is complete if equivalent sibling endpoints remain exploitable.

---

## Output Format

When reporting the remediation, use:

```markdown
# Security Remediation Summary

## Finding
<short description of the original issue>

## Root Cause
<why tainted or untrusted data reached a dangerous operation>

## Fix
<what code changed and which control now blocks exploitation>

## Validation
<tests added, reasoning performed, or manual verification steps>

## Residual Risk
<migration note, rollout concern, or "none identified">
```
