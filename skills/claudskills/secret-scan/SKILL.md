---
name: secret-scan
description: 'Hardcoded-secret detection — AWS keys, GitHub PATs, Slack tokens, Stripe keys, generic high-entropy strings. Pre-commit (`--staged-only`), explicit paths, or full repo. Use when guarding `git commit`, auditing a repo for leaked credentials, validating no secrets entered the diff before push, or producing a rotation list for an exposed-secret incident.'
argument-hint: "[--paths file1 file2] [--staged-only]"
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
model: sonnet
triggers:
  - "secret scan"
  - "detect secrets"
  - "credential scan"
  - "api key check"
chain:
  - verify-fix
outputBudget: short
cooldown: per-session
---

# Vulnetix Secret Scan Skill

## Use when

- Pre-commit: confirm no secrets in staged files (`--staged-only`).
- Pre-push: scan diff vs `origin/HEAD` for high-confidence leaks.
- Audit: full-repo scan for an exposed-secret incident.
- Producing a rotation list — which provider keys need to be revoked NOW.
- CI gate: block merge if any high-confidence secret detected.

## Don't use for

- Vulnerability detection — use `/vulnetix:sast-scan` or `/vulnetix:sca-scan`.
- Validating an already-fixed leak — use git filter-repo or BFG to remove from history.

## Conventions

This skill follows [`_lib/contract.md`](../_lib/contract.md): the Vulnetix CLI is auto-installed by hooks, `.vulnetix/capabilities.yaml` is always present, every `vulnetix vdb` call is piped through a verified `jq` filter from [`_lib/jq/`](../_lib/jq/), independent calls run in parallel as concurrent Bash tool calls, and trailing follow-ups are limited to one line. See the contract for output style, memory write rules, and cooldowns.

## Step 1: Load capabilities

Read `.vulnetix/capabilities.yaml`. Note `binaries.git` (required for `--staged-only`).

## Step 2: Decide scope

- `--staged-only`: `git diff --cached --name-only` for the file list.
- `--paths`: explicit list.
- Default: changed files vs. main branch, fallback to whole repo.

## Step 3: Run scan

```bash
vulnetix secrets --paths "$PATHS" -o json > .vulnetix/secrets.${TIMESTAMP}.json
```

Or via integrated scan:

```bash
vulnetix scan --evaluate-secrets --paths "$PATHS" -o json
```

## Step 4: Render

```
Secret findings: N (high-confidence: M)

| Type | File:Line | Snippet (redacted) | Confidence |
```

For each finding, emit a redacted snippet (replace 60% of the secret with `*`). Never print the full secret.

## Step 5: Remediation guidance

For each unique secret type, surface the standard rotation/revocation steps (AWS, GCP, GitHub PAT, Slack, Stripe, etc.). Do not auto-rotate.

If a secret is found in a committed file (not just staged):
- Suggest `git filter-repo` or BFG repo-cleaner
- Strongly recommend rotating the credential since it's in git history

## Memory update

Append a sanitized record to `.vulnetix/secrets/${TIMESTAMP}.summary.yaml` (counts by type, file paths, no values).

## Edge cases & gotchas

- Output redacts 60% of each detected secret. Never re-print the un-redacted value.
- High-confidence findings include AWS / GitHub PAT / Slack / Stripe patterns. Generic high-entropy strings are medium-confidence; tune your CI gate accordingly.
- `--staged-only` reads `git diff --cached --name-only` — files not yet staged are skipped. Run AFTER `git add`.
- Detection is regex-based; obfuscated secrets (split across vars, base64-wrapped) may be missed. Pair with a hand review for high-stakes audits.
- For secrets ALREADY in git history, this skill detects them on next change only. Use `gitleaks --log-opts="--all"` for full history scan, then BFG / filter-repo to remove.
- False-positive suppression uses inline comments (`# pix-ignore-secret`) on the next line; the suppression is per-line, not per-pattern.
