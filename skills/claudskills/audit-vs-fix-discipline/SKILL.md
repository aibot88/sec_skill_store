---
name: audit-vs-fix-discipline
description: Use when the user asks to audit, review, investigate, check, scan, "look at", or "find issues in" code — anything that sounds like a diagnostic request without an explicit fix authorization. Enforces findings-only output with severity tiering, forbids in-place fixes during audit, and blocks the dismissal-as-"pre-existing" rationalisation.
---

<!-- Last updated: 2026-05-19T12:00+10:00 -->

# Audit vs fix discipline

**Audits produce findings. Fixes happen separately, on explicit user request.**

Violating the letter of this rule violates the spirit. "Just one quick fix while I'm here" is the failure mode this skill exists to prevent.

## Triggers — apply this skill when the user says

`audit`, `review`, `investigate`, `check`, `scan`, `look at`, `look over`, `go through`, `inspect`, `find issues in`, `what's wrong with`, `how's the X looking`, `is the X any good`, `tell me about the X`.

If the request contains BOTH a diagnostic verb AND an explicit fix verb (`audit and fix`, `review and clean up`, `find and fix`), the user has authorised fixes — discipline does not apply; proceed normally.

## The discipline

While in audit mode you MUST:

1. **Use read-only tools only.** Read, Grep, Glob, Bash for read-only commands. NO Edit, Write, or mutating Bash. Sub-agents you dispatch inherit this constraint — say so in the prompt.
2. **Produce tiered findings.** Every finding gets a severity label:
	- **P0** — broken behaviour, security, data loss, build/test failures.
	- **P1** — correctness risk, performance, missing types, dead code with side effects.
	- **P2** — style, naming, nits, harmless dead code.
3. **Cite `file:line` for every finding.** No findings without locations.
4. **Separate findings from suggestions.** Refactor proposals ("split this into 5 files") are a separate section labelled "Suggested follow-ups" — NOT mixed into findings.
5. **End with an explicit ask.** `Want me to fix any of these? Specify by number, severity tier, or "fix all P0".` Then stop.

## Calibration

A clean audit is a valid outcome. Empty tiers are signal — `P0: none` is fine, and you must NEVER manufacture findings to fill them. The primary failure mode of LLM reviewers is inventing issues to seem thorough; it erodes trust and wastes the user's time more than missing a real finding does.

**Confidence gate: ≥80% sure it's a real problem, or drop it.** If the only reason you're flagging something is "it might be an issue", that's the failure mode the user reads as "inventing issues". Speculation belongs in `Suggested follow-ups`, not in a tiered finding.

**Pre-report 4-question check.** Before adding any finding to a tier, answer:

1. Can I cite the exact `file:line`?
2. Can I describe the concrete failure mode (what input + state produces what wrong outcome)?
3. Have I read enough surrounding context (callers, imports, related tests) to be sure?
4. Is the severity defensible — P0 = broken/exploitable now, P1 = correctness/perf risk under realistic conditions, P2 = a nit a senior would mention casually?

If any answer is "no" → drop the finding or downgrade to a follow-up suggestion.

**Pre-filtered exclusion list — do NOT flag:**

- "Consider adding error handling" when the framework or callers already handle it
- "Magic numbers" for well-known constants (HTTP 200/404, port 80/443, 60 for seconds, 1024 for KiB)
- "Missing JSDoc / comments" on self-describing helpers
- "Function too long" for switch tables, test fixtures, or data-shape declarations
- "N+1 queries" on fixed-cardinality loops or with batching already in place
- "Math.random()" in non-cryptographic contexts
- "Null dereference" where TS narrowing or type guards exist
- Style preferences unless the project explicitly enforces them
- Issues a linter would already catch (out of audit scope unless asked)
- Speculative "this could be cleaner" without a concrete failure mode

Apply this exclusion list before running the 4-question check.

**Counterintuitive caveat (research):** elaborate review prompts INCREASE false positives. Don't enumerate every potential mismatch, don't ask for long rationales — that pressure biases toward over-criticism. Stay terse, gate hard, drop liberally.

## Forbidden during audit

- Editing any file. Even "obvious" typos.
- Running `git add`, `git commit`, or any state-changing git command.
- Bundling fixes into the audit report ("I've fixed the P0s and listed the rest…").
- Saying a finding is **"pre-existing"**, **"unrelated"**, **"out of scope"**, or **"not worth fixing"** as a way to skip it. Report it at the appropriate tier and let the user decide.

## Rationalisation table

| Excuse | Reality |
|---|---|
| "It's a one-line fix, faster to just do it." | The user can read a one-line fix from a finding. The cost is consistency, not keystrokes. |
| "Critical security bug — has to be fixed now." | Report it as P0 with the proposed fix in the body. User decides timing. |
| "Lint errors are pre-existing, not part of this audit." | If you see them, report them at P1. The user asked you to audit — that includes whatever you find. |
| "The user clearly meant to fix it." | If they meant fix, they'd say fix. Ambiguous prompts default to audit mode. |
| "I'll just fix the trivial ones and report the rest." | This is the most common violation. Don't. |
| "I'll batch the audit and the fixes into one response to save round-trips." | Round-trips are the point. The audit is a checkpoint for scope. |
| "The diff is small enough that the audit + fix is one logical change." | The audit is the deliverable. The fix is a separate deliverable. |
| "I should fill in P1/P2 to look thorough." | Empty tiers are valid signal. "P0: none" is a correct result. Manufactured findings erode trust. |
| "It might be an issue, I'll flag it just in case." | If you're <80% sure, drop it. Speculation belongs in Suggested follow-ups, not findings. |

## Red flags — STOP and re-anchor

- About to call `Edit` or `Write` during an audit.
- About to type "I've gone ahead and…" or "while I was at it…".
- About to call something "pre-existing" or "out of scope" without naming it.
- About to add a "Suggested split" or refactor proposal in the same list as the findings.
- About to skip the "Want me to fix any of these?" closer.
- About to add a finding because a tier "looks empty".
- About to flag something with "could be cleaner" / "might want to consider" but no concrete failure mode.

**Each of these means: STOP. Go back to findings-only mode.**

## Output template

```
## Audit: <scope> — <criteria>

### P0 (blocking)
- `path/to/file.ts:42` — <one-line finding>. <one-sentence why it matters>.

### P1 (quality / correctness risk)
- `path/to/file.ts:88` — ...

### P2 (nits)
- `path/to/file.ts:120` — ...

### Suggested follow-ups (not findings)
- Optional: bigger refactor ideas surfaced by the audit, clearly separated.

---
Want me to fix any of these? Specify by number, by tier ("fix all P0"), or by file.
```

If a tier is empty, say "P0: none" — don't omit the header. Empty headers are signal.

## When NOT to use

- User explicitly authorises fixes: "audit and fix", "find and clean up", "review and patch".
- User has set context like "we're in fix mode" earlier in the session.
- The diagnostic was a single concrete question ("is `foo()` broken?") with a one-shot answer — no formal audit needed.

## Common mistakes

- **Mixing tiers in one bullet list.** Tiers exist so the user can triage. Collapse them and you've defeated the point.
- **Burying P0s under P2 nits.** P0 first, always.
- **No final ask.** Without the closer, the user is left guessing whether you're waiting or done.
- **Counting refactor proposals as findings.** A finding is "this is wrong". A proposal is "this could be better-shaped". Different sections.
- **Filling tiers to seem thorough.** "P0: none" is a valid result. Inventing nits to populate P2 is the same failure mode as inventing P0s — it erodes trust.
- **Speculation dressed up as a finding.** "Could maybe be cleaner" / "might want to consider X" without a concrete failure mode → drop it or move to Suggested follow-ups.

## Per-project override

Before producing findings, check the project root for `REVIEW.md`. If present, read it — its calibration overrides this skill's defaults. Common overrides:

- Redefining what counts as Important (P0/P1) vs Nit (P2) for the specific codebase
- Exclusion lists tailored to the project (e.g. shell-script demos, doc/config repos, prototypes)
- Scope restrictions (e.g. "this is an educational mirror; don't flag missing test coverage")

When `REVIEW.md` and this skill disagree, `REVIEW.md` wins — it's the user's per-project policy.
