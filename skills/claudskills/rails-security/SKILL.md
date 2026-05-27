---
name: rails-security
description: Use when auditing a Rails app for SQL injection, XSS, CSRF, mass-assignment, or Gemfile.lock CVEs, or when reviewing only NEW security regressions in a PR vs base branch.
user-invocable: true
allowed-tools:
  - Read
  - Bash
---

# /rails-security — Brakeman + bundler-audit

Combined Rails security scan. No credentials. Subcommands:
`vulns`, `cves`, `audit`, `diff`, `ignore`, `update`.

## Overview

Combined Brakeman (static analysis) + bundler-audit (CVE) scan for Rails apps. `diff` mode is the killer feature: shows only NEW issues vs base branch via git worktree (non-destructive — never touches your working tree).

## When to Use

- Pre-PR security gate (new SQL injection, XSS, CSRF, mass-assignment)
- Auditing `Gemfile.lock` for known CVEs
- PR review: only see what THIS PR introduced, not pre-existing noise
- Adding ignored issues with documented reason for audit trail

## When NOT to Use

- Non-Rails projects → Brakeman is Rails-specific
- Runtime / dynamic security testing → use OWASP ZAP, not static scanners
- Dependency updates not security-related → use Dependabot / Renovate
- Auditing infrastructure (Docker, k8s) → wrong scope

## Dependencies

```bash
gem install brakeman bundler-audit
```

If a tool is missing, the relevant subcommand is skipped with a clear message.

## Helpers

```bash
brakeman_cmd() {
  if [ -f "${1:-.}/Gemfile" ] && grep -q "brakeman" "${1:-.}/Gemfile" 2>/dev/null; then
    echo "bundle exec brakeman"
  else
    echo "brakeman"
  fi
}
```

## Dispatch

### `vulns [path] [--severity high|medium|low|all]` — Brakeman scan
```bash
PATH_ARG="${1:-.}"; SEV="${SEV:-medium}"
mapfile -t CMD < <(brakeman_cmd "$PATH_ARG" | tr ' ' '\n')
"${CMD[@]}" -p "$PATH_ARG" -f json -o /tmp/brakeman.json --no-progress 2>/dev/null

jq -r --arg sev "$SEV" '
  .warnings[] | select(
    ($sev=="all") or
    ($sev=="high" and .confidence=="High") or
    ($sev=="medium" and (.confidence=="High" or .confidence=="Medium")) or
    ($sev=="low" and true))
  | "[\(.confidence)] \(.warning_type): \(.message)\n  \(.file):\(.line)"
' /tmp/brakeman.json

jq -r '.warnings | group_by(.confidence) | .[] | "\(.[0].confidence): \(length)"' /tmp/brakeman.json
```

### `cves [path]` — bundler-audit CVE scan
```bash
PROJ="${1:-.}"
[ -f "$PROJ/Gemfile.lock" ] || { echo "No Gemfile.lock" >&2; return 1; }

bundle-audit update --quiet 2>/dev/null || true
(cd "$PROJ" && bundle-audit check --format json) > /tmp/bundler-audit.json 2>/dev/null

jq -r '
  .results[]? | "[\(.advisory.criticality // "unknown" | ascii_upcase)] \(.gem.name) \(.gem.version)
  CVE: \(.advisory.cve // .advisory.id)  Fix: upgrade to \(.advisory.patched_versions | join(", "))
  \(.advisory.title)"
' /tmp/bundler-audit.json
```

### `audit [path]` — both + pre-PR gate (exit non-zero on HIGH or any CVE)
```bash
"$0" vulns "$1"; echo ""; "$0" cves "$1"

HIGH_BR=$(jq -r '[.warnings[] | select(.confidence=="High")] | length' /tmp/brakeman.json 2>/dev/null || echo 0)
CVES=$(jq -r '(.results // []) | length' /tmp/bundler-audit.json 2>/dev/null || echo 0)

[ "$HIGH_BR" -gt 0 ] || [ "$CVES" -gt 0 ] && {
  echo "GATE: $HIGH_BR HIGH Brakeman + $CVES CVEs"
  return 1
}
```

### `diff [base-branch]` — only NEW issues vs base (non-destructive)

Uses `git worktree add` — your working tree is NEVER modified.

```bash
BASE="${BASE:-main}"
WT="$(mktemp -d)/rails-security-base"
trap "git worktree remove --force $WT 2>/dev/null; rm -rf $WT" EXIT INT TERM

git worktree add --quiet "$WT" "$BASE" || { echo "Cannot worktree at $BASE" >&2; return 1; }

mapfile -t CMD < <(brakeman_cmd "." | tr ' ' '\n')
(cd "$WT" && "${CMD[@]}" -f json -o /tmp/brakeman-base.json --no-progress 2>/dev/null) || true
"${CMD[@]}" -f json -o /tmp/brakeman-head.json --no-progress 2>/dev/null

echo "=== NEW Brakeman ==="
jq -s '(.[0].warnings|map(.fingerprint)) as $b | .[1].warnings | map(select(.fingerprint as $f | $b | index($f) | not)) | .[] | "[\(.confidence)] \(.warning_type) — \(.file):\(.line)"' /tmp/brakeman-base.json /tmp/brakeman-head.json

(cd "$WT" && bundle-audit check --format json) > /tmp/ba-base.json 2>/dev/null || echo '{}' > /tmp/ba-base.json
bundle-audit check --format json > /tmp/ba-head.json 2>/dev/null || echo '{}' > /tmp/ba-head.json

echo ""; echo "=== NEW CVEs ==="
jq -s '(.[0].results//[]|map(.advisory.id)) as $b | (.[1].results//[]) | map(select(.advisory.id as $id | $b | index($id) | not)) | .[] | "\(.gem.name) \(.gem.version) — \(.advisory.cve // .advisory.id)"' /tmp/ba-base.json /tmp/ba-head.json
```

**Why worktree, not stash:** stash is destructive on Ctrl-C/OOM, swallows merge conflicts. Worktree creates isolated checkout in temp dir.

### `ignore brakeman <fingerprint> [note]` / `ignore cve <CVE-ID> [note]`
```bash
# Brakeman:
mkdir -p config; [ -f config/brakeman.ignore ] || echo '{"ignored_warnings":[]}' > config/brakeman.ignore
jq --arg fp "$FP" --arg note "${NOTE:-no reason given}" \
  '.ignored_warnings += [{fingerprint:$fp, note:$note}]' config/brakeman.ignore > config/brakeman.ignore.tmp \
  && mv config/brakeman.ignore.tmp config/brakeman.ignore

# CVE:
[ -f .bundler-audit.yml ] || echo "ignore: []" > .bundler-audit.yml
echo "Edit .bundler-audit.yml to add: $CVE_ID  # ${NOTE:-add reason}"
```

ALWAYS require a reason — without it future maintainers can't audit decisions.

### `update` — refresh advisory DB
```bash
bundle-audit update     # hits GitHub; fallback: bundle-audit check --no-update
```

## Common Mistakes

- Ignoring without a reason → future maintainers can't audit decisions
- Running scanner on full codebase every PR → use `diff` mode for noise reduction
- Stash-based diff instead of worktree → destructive on Ctrl-C / OOM
- Skipping `bundle-audit update` → stale CVE database misses recent vulns
- Brakeman ignore by line number → use fingerprint (survives refactors)
- Treating Brakeman `Low` as noise → some are real, just rare paths

## Safety

- Scan output reveals attack surface (file paths, gem versions). Don't paste raw output publicly.
- `brakeman.ignore` and `.bundler-audit.yml` MUST be committed (audit trail of accepted-risk decisions).
- Never bypass scanners in CI without an approved exception (PR comment + ignore entry with reason).
- Use `diff` mode for PR review — only see NEW issues, drastically cuts noise.
