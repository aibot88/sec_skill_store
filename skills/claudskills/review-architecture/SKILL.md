---
name: review-architecture
description: Reviews an architecture (file, repo, design doc, or pasted text) against scalability, security, reliability, compliance, and anti-pattern checklists plus fitness functions. Use when the user asks to "review my architecture", "critique this design", "audit this system", or invokes /sdd:review-architecture.
argument-hint: "<path to design doc, repo path, or pasted architecture text>"
allowed-tools: Read, Grep, Glob, Write
---

# review-architecture

Principal-engineer review. Be direct, not diplomatic. Cite evidence. Propose concrete fixes.

## Process

1. **Ingest the target.** File path → Read it. Directory/repo → Glob for README, docs/, ADRs, manifests; sample 3–5 critical files. Pasted text → use directly. Never try to read a whole repo.
2. **Run each checklist.** Load only the ones relevant to the target:
   - Scalability → `scalability-checklist.md`
   - Reliability → `reliability-checklist.md`
   - Security → `security-checklist.md`
   - Compliance → `compliance-checklist.md` (regulated domains only: finance, health, EU)
   - Anti-patterns → `anti-patterns.md`
   - Fitness functions → `arch-fitness-functions.md`
3. **Classify each finding:** ✅ Pass · ⚠️ Risk · 🔴 Violation · ❓ Unknown. Never generate findings you can't evidence. "I didn't see auth mentioned" is an unknown, not a violation.
4. **Severity + remediation** for every ⚠️ and 🔴:
   - Severity: critical / high / medium / low (blast radius × likelihood)
   - Evidence: specific line, file, or statement
   - Why it matters: the scenario where it bites
   - Fix: concrete change; link to a `design-system` / `design-database` reference if one fits
5. **Fitness functions.** Suggest 3–5 automated checks to prevent regression (executable pass/fail, not dashboards).

## Output skeleton

```markdown
# Architecture Review: <name>

## Summary
- Critical: N · High: N · Medium: N · Low: N
- Overall: <one-paragraph judgement>

## Findings
### 🔴 Critical
### 🔴 / ⚠️ High
### ⚠️ Medium
### ⚠️ Low
### ❓ Unknowns (need user input)

## Recommended fitness functions

## What's working well  (2–4 callouts)
```

Offer to save to `./reviews/<target>-<date>.md`.

## Stance

- No bikeshedding — only things that fail in prod.
- Quantitative — "likely slow" → "at 10k QPS this hop adds ~50 ms tail (see latency-numbers)".
- Assume good intent — the designer had context you don't.
- Prioritize — a 20-item list with no severity sort is useless. Top criticals first.
