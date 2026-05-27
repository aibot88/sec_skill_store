---
name: eresus-pr-security-review
description: >
  Security-focused pull request and diff review skill for finding newly introduced vulnerabilities, risky regressions,
  and missing security tests in changed code. Trigger when the user asks to: "review this PR for security", "check this diff for vulns",
  "do a security code review", "audit changed files", or wants findings on a patch instead of a full-repo scan. Best used alongside eresus-sast-scanner.
metadata:
  version: "1.0"
  domain: application-security
  mode: review
---

# Security PR Review

## Purpose

Review changed code with a security-review mindset: prioritize introduced bugs, exploitable regressions,
and missing coverage in the modified attack surface. Focus on what the diff changes, not on writing a
general audit of the whole repository.

## Scope Rules

- Prioritize vulnerabilities introduced or exposed by the diff.
- Inspect surrounding code when needed to confirm reachability, auth context, or sanitizer behavior.
- Mention pre-existing issues only when the change makes them reachable, worse, or security-relevant now.
- Findings come first; summary is secondary.

---

## Workflow

### Step 1: Read the Diff as an Attack Surface Change

Identify:

- newly added endpoints, handlers, controllers, jobs, or CLI paths
- changed authorization checks or middleware wiring
- new deserialization, template rendering, file, network, or command execution paths
- config changes that weaken defaults or widen trust boundaries

### Step 2: Map New Sources, Sinks, and Guards

For changed code, locate:

- attacker-controlled inputs
- dangerous sinks
- sanitization, validation, auth, and feature-flag guards

Do not stop at the edited hunk if the actual sink or protection lives nearby.

### Step 3: Trace Security-Sensitive Data Flow

Apply lightweight taint reasoning through:

- helper calls
- serializers and DTOs
- middleware layers
- ORM/query helpers
- template/view rendering
- background job enqueue/dequeue boundaries

### Step 4: Review Diff-Specific Risk Patterns

Pay extra attention to:

- string-built queries, filters, or shell commands
- unsafe deserialization, polymorphic typing, object revival, or parser feature flags
- auth checks moved later in the flow
- newly trusted headers, cookies, or client-supplied role fields
- open redirects added through `next`, `returnTo`, or `redirect_url`
- debug logging of secrets, tokens, or PII
- upload handling, archive extraction, or path joins
- new outbound HTTP fetches or webhook callbacks
- security settings changed from strict to permissive

### Step 5: Judge Before Reporting

For every candidate finding, verify:

- the input is actually attacker-controlled
- the changed path is reachable
- protections are not already effective
- the issue is materially exploitable

Drop speculative findings that cannot survive this check.

### Step 6: Report Findings and Testing Gaps

Report confirmed issues with:

- severity
- exact changed file and line
- exploit path in one short paragraph
- concrete remediation direction
- missing test coverage if the diff should have added one

If no confirmed issue exists, say so explicitly and note any residual uncertainty or testing gaps.

---

## Review Guardrails

- Do not file a security finding purely because code "looks risky"; explain the actual exploit path.
- Do not ignore new trust boundaries just because the sink is in an unchanged helper.
- Do not report infra-only assumptions as app bugs unless the diff depends on them.
- Do not downgrade auth bugs simply because the endpoint is "internal" without evidence.
- Do not confuse code-quality concerns with security findings unless they create exploitability.

---

## Output Format

Use this structure:

```markdown
[SEVERITY] <short title>
File: <path>:<line>
Why it matters: <reachability + impact in 2-4 sentences>
Fix: <specific remediation>
Tests: <missing or recommended coverage>
```

When there are no findings:

```markdown
No confirmed security findings in the reviewed diff.
Residual risk: <short note or "none identified">
Testing gap: <short note or "none identified">
```
