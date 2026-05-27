---
description: Pre-push adversarial review for personal repos before git push. Runs adversarial-input sweep, parallel-implementation symmetry audit, project AGENTS.md compliance, dead-code sweep, secrets scan. Use before any push; mandatory for repos that will become public or shared. Tier 2 sub-agent does the bulk; Tier 3 main synthesizes.
---

# personal-pre-push-review

Mechanical pre-push review. Catches what your own re-read misses. The one-line rule: **Before any `git push` on a non-trivial change, run this skill.**

## Trigger phrases

- "Pre-push check"
- "Review before I push"
- `/pre-push`
- Auto-suggested when the AI is about to call `git push` after a multi-commit feature branch

## Inputs

- The current git working directory
- The base branch (default `main`, configurable)
- The repo's `AGENTS.md` if present

## Process

### Gate 1 — Adversarial input sweep (Tier 2 sub-agent)

Delegate `review` sub-agent. Pass it `git diff main...HEAD`. Returns ≤800-token findings:

- BLOCKING: input-type / edge-value / missing-field / silent-failure issues
- WARNING: dead code, unclear logic, unsymmetric parallel impl
- NIT: style, naming, comments

### Gate 2 — Parallel-implementation symmetry audit

If the diff touches 2+ implementations of the same logic (JS + Python, client + server, multiple platforms), the sub-agent diffs them mentally for behavior parity. Reports any drift.

### Gate 3 — Project AGENTS.md compliance

If the repo has its own `AGENTS.md`, the AI re-reads it and checks each rule against the diff. Common categories:

- File organization conventions
- Sync requirements (code + README + frontend in sync)
- Language choices
- Build/test gates that must pass

### Gate 4 — Dead-code sweep

Grep the diff for:

- New functions that aren't called
- New imports that aren't used
- New variables that are computed then discarded

### Gate 5 — Secrets/PII scan

Grep tracked files in the diff for:

- JWT patterns: `eyJ[A-Za-z0-9_-]{20,}\.eyJ`
- API key shapes: `sk-`, `xoxb-`, `ghp_`, `gho_`, `ya29.`, etc.
- AWS access keys: `AKIA[0-9A-Z]{16}`
- Generic high-entropy strings in `.env`-shaped lines
- Personal email addresses other than Josh's main one
- Phone numbers
- Physical addresses

If any hit: BLOCKING. Surface to Josh for decision (false positive vs real leak).

### Gate 6 — Repo readiness for visibility level

If the repo is private but Josh's about to make it public (or is pushing to a public namespace):

- Run the full secrets/PII scan over ALL tracked files (not just the diff)
- Verify .gitignore covers `.env`, `*.key`, `*.pem`, master-cv files
- Verify README doesn't leak personal info

### Gate 7 — Em-dash check

If the diff modifies any file in scope of the em-dash ban (cover letters, resumes, blog posts intended for human readers), grep for em-dashes. Count must be zero.

## Output

```markdown
# Pre-push Review — [repo] [branch]

**Base:** main
**HEAD:** [SHA] ([N] commits ahead)
**Files changed:** [N]
**Lines:** +[N] / -[M]

## Gates

| Gate | Status | Findings |
|---|---|---|
| 1. Adversarial sweep | ✅ / ⚠️ / 🚫 | [N findings] |
| 2. Parallel-impl symmetry | ✅ / N/A | [...] |
| 3. AGENTS.md compliance | ✅ / ⚠️ | [...] |
| 4. Dead-code sweep | ✅ / ⚠️ | [...] |
| 5. Secrets/PII scan | ✅ / 🚫 | [N hits] |
| 6. Visibility readiness | ✅ / N/A | [...] |
| 7. Em-dash check | ✅ / N/A | [N hits] |

## BLOCKING findings (must fix before push)

[file:line] [finding] [recommended fix]

## WARNING findings (consider before push)

[...]

## NIT findings (optional)

[...]

## Recommendation

- [ ] PUSH — all green
- [ ] BLOCK — fix blocking findings, re-run
- [ ] PROCEED WITH JUDGMENT — warnings present, Josh decides
```

## Per-push, not per-session

Run BEFORE every push. Not once at session start. Each diff is its own input set; each repo has its own AGENTS.md; the cost asymmetry is brutal.

If the AI is about to call `git push` and pre-push-review hasn't been run on the current commits, the AI MUST either run it OR explicitly state why it's skipping (e.g., "trivial 5-line README typo, skill overhead exceeds value").

## When pre-push-review is overkill

- Pure documentation typo fixes
- Single-file config bumps
- README-only edits with no code

Trust your judgment. The skill exists to catch what you'd miss, not to be a religious gate on every commit.
