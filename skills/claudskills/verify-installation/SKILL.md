---
name: verify-installation
description: Self-test the maxvision-orchestration plugin after install. Runs five read-only checks (index, cheatsheets, gh auth, jq+sqlite3 in PATH, sample BM25 query) and reports pass/info/fail. Use immediately after /plugin install, /plugin update, or whenever the orchestrator behaves unexpectedly.
when_to_use: |
  Trigger phrases: "/maxvision-orchestration:verify-installation",
  "is the plugin healthy", "self-test the orchestrator", "5/5 sanity".
disable-model-invocation: true
allowed-tools: Read Bash(test *) Bash(test -f *) Bash(test -o *) Bash(sqlite3 *) Bash(gh auth status) Bash(gh release view *) Bash(jq *) Bash(grep *) Bash(date *) Bash(mkdir *) Bash(cat *) Bash(command *) Bash(which *) Bash(printf *) Bash(echo *)
---

# Verify installation

No arguments. Runs in <5 s. All 5 checks always run; the summary aggregates.

Three result states:
- **PASS** — check succeeded
- **INFO** — first-run state, expected on a fresh install before bootstrap (counts toward healthy)
- **FAIL** — real problem, remediation hint included

## Workflow

### 1. Setup result accumulator + dependency preflight

Detect tooling availability FIRST so dependent checks can cascade to INFO instead of FAIL when an upstream dependency is missing (`sqlite3 not in PATH` → Check 1 and Check 5 cannot query the index, but that's not the index's fault).

```bash
set -euo pipefail
PASS_COUNT=0
INFO_COUNT=0
TOTAL=5
RESULTS=()
DB="$HOME/.claude/cache/maxv-orchestration/index.db"
INDEX_MISSING=0

# Dependency preflight (silent — formal report happens in Check 4)
HAS_JQ=0
HAS_SQLITE3=0
which jq >/dev/null 2>&1 && HAS_JQ=1
which sqlite3 >/dev/null 2>&1 && HAS_SQLITE3=1
```

### 2. Check 1 — `index.db` exists and has ≥75% of the documented baseline

The baseline is read dynamically from the `catalog-index-latest` release
notes (which contain `${ITEM_COUNT} items indexed across ${SOURCE_COUNT} sources`).
Cached for 24h in `~/.claude/cache/maxv-orchestration/baseline.txt` to avoid
hitting GitHub API on every verify (FU-2).

```bash
set -euo pipefail

# Resolve the dynamic baseline (cached 24h)
BASELINE_FILE="$HOME/.claude/cache/maxv-orchestration/baseline.txt"
BASELINE=0
if [[ -f "$BASELINE_FILE" ]]; then
  AGE_HOURS=$(( ( $(date +%s) - $(date +%s -r "$BASELINE_FILE") ) / 3600 ))
  if [[ "$AGE_HOURS" -lt 24 ]]; then
    BASELINE=$(cat "$BASELINE_FILE" 2>/dev/null || echo 0)
  fi
fi
if [[ "$BASELINE" -eq 0 ]]; then
  # Cache miss or stale — refresh from GitHub release notes
  if command -v gh >/dev/null 2>&1 && command -v jq >/dev/null 2>&1; then
    NOTES=$(gh release view catalog-index-latest \
      -R produtoramaxvision/claude-code-maxvision-orchestration \
      --json body --jq .body 2>/dev/null || echo "")
    BASELINE=$(echo "$NOTES" | grep -oE '[0-9]+ items indexed' | head -1 | grep -oE '[0-9]+' || echo 0)
    if [[ "$BASELINE" -gt 0 ]]; then
      mkdir -p "$(dirname "$BASELINE_FILE")"
      echo "$BASELINE" > "$BASELINE_FILE"
    fi
  fi
fi

# Fall back to a hardcoded floor if dynamic resolution failed (e.g., offline,
# no gh, no jq). This floor is intentionally low (1500) so a degraded local
# environment doesn't false-FAIL; the cascade in Check 4 surfaces missing deps.
if [[ "$BASELINE" -eq 0 ]]; then
  BASELINE=1500
fi

THRESHOLD=$(( BASELINE * 75 / 100 ))   # 75% of baseline = "still healthy"

if [[ "$HAS_SQLITE3" -eq 0 ]]; then
  INFO_COUNT=$((INFO_COUNT+1))
  INDEX_MISSING=1
  RESULTS+=("INFO 1: cannot query index.db without sqlite3 in PATH — see Check 4 for remediation")
elif [[ -f "$DB" ]]; then
  N=$(sqlite3 "$DB" 'SELECT count(*) FROM item' 2>/dev/null || echo 0)
  if [[ "$N" -ge "$THRESHOLD" ]]; then
    PASS_COUNT=$((PASS_COUNT+1))
    RESULTS+=("PASS 1: index has $N items (baseline=$BASELINE, threshold=$THRESHOLD)")
  else
    RESULTS+=("FAIL 1: only $N items (threshold=$THRESHOLD = 75% of baseline=$BASELINE) — index may be corrupted; run /maxvision-orchestration:index-catalog --rebuild")
  fi
else
  INFO_COUNT=$((INFO_COUNT+1))
  INDEX_MISSING=1
  RESULTS+=("INFO 1: index.db not yet bootstrapped (first-run state) — run /maxvision-orchestration:index-catalog --bootstrap")
fi
```

### 3. Check 2 — ≥1 cheatsheet present

```bash
set -euo pipefail
if [[ -f "$HOME/.claude/CLAUDE-agents.md" || -f "$HOME/.claude/CLAUDE-skills.md" ]]; then
  PASS_COUNT=$((PASS_COUNT+1))
  RESULTS+=("PASS 2: cheatsheet found at ~/.claude/CLAUDE-agents.md or ~/.claude/CLAUDE-skills.md")
else
  RESULTS+=("FAIL 2: no cheatsheet at ~/.claude/CLAUDE-{agents,skills}.md — see ~/.claude/CLAUDE.md for the documented standard")
fi
```

### 4. Check 3 — `gh` authenticated

```bash
set -euo pipefail
if gh auth status >/dev/null 2>&1; then
  PASS_COUNT=$((PASS_COUNT+1))
  RESULTS+=("PASS 3: gh authenticated")
else
  RESULTS+=("FAIL 3: gh not authenticated — run: gh auth login")
fi
```

### 5. Check 4 — `jq` + `sqlite3` in PATH

(Detection already done in step 1's preflight; this step formally reports the result and explains the cascade if anything is missing.)

```bash
set -euo pipefail
if [[ "$HAS_JQ" -eq 1 && "$HAS_SQLITE3" -eq 1 ]]; then
  PASS_COUNT=$((PASS_COUNT+1))
  RESULTS+=("PASS 4: jq + sqlite3 ready")
else
  MISSING=()
  [[ "$HAS_JQ" -eq 0 ]] && MISSING+=("jq (winget install jqlang.jq)")
  [[ "$HAS_SQLITE3" -eq 0 ]] && MISSING+=("sqlite3 (winget install SQLite.SQLite). After install close+reopen terminal so PATH refreshes.")
  RESULTS+=("FAIL 4: missing in PATH: ${MISSING[*]}")
fi
```

### 6. Check 5 — discover-skill sample query "shadcn" returns ≥1 match

```bash
set -euo pipefail
if [[ "$HAS_SQLITE3" -eq 0 || "$INDEX_MISSING" -eq 1 ]]; then
  # Cascading INFO — Check 1 already flagged either the missing dep or the missing index
  INFO_COUNT=$((INFO_COUNT+1))
  RESULTS+=("INFO 5: BM25 query skipped (see INFO 1 above for the cascade root)")
elif [[ -f "$DB" ]]; then
  N=$(sqlite3 "$DB" "SELECT count(*) FROM item_fts WHERE item_fts MATCH 'shadcn'" 2>/dev/null || echo 0)
  if [[ "$N" -ge 1 ]]; then
    PASS_COUNT=$((PASS_COUNT+1))
    RESULTS+=("PASS 5: discovery works ($N matches for 'shadcn')")
  else
    RESULTS+=("FAIL 5: 0 matches for 'shadcn' — index may be empty or corrupted; run /maxvision-orchestration:index-catalog --rebuild")
  fi
else
  RESULTS+=("FAIL 5: index.db missing (covered by check 1, but FTS5 query also blocked)")
fi
```

### 7. Print summary

```bash
set -euo pipefail
echo "maxvision-orchestration verify-installation:"
for line in "${RESULTS[@]}"; do
  printf "  %s\n" "$line"
done
echo
HEALTHY=$((PASS_COUNT + INFO_COUNT))
FAIL_COUNT=$((TOTAL - HEALTHY))

if [[ "$FAIL_COUNT" -eq 0 ]]; then
  if [[ "$INFO_COUNT" -gt 0 ]]; then
    # Some INFO present — first-run; suggest bootstrap
    echo "${PASS_COUNT}/${TOTAL} PASS + ${INFO_COUNT} INFO — plugin healthy (first-run state)"
    echo "Next: run /maxvision-orchestration:index-catalog --bootstrap to bring the index online."
    exit 0
  else
    echo "${PASS_COUNT}/${TOTAL} PASS — plugin healthy"
    exit 0
  fi
else
  echo "${PASS_COUNT}/${TOTAL} PASS, ${INFO_COUNT} INFO, ${FAIL_COUNT} FAIL — plugin needs attention (see FAIL messages above)"
  exit 1
fi
```

## Output examples

### Steady-state (post-bootstrap, all 5 PASS)

```
maxvision-orchestration verify-installation:
  PASS 1: index has 1992 items
  PASS 2: cheatsheet found at ~/.claude/CLAUDE-agents.md or ~/.claude/CLAUDE-skills.md
  PASS 3: gh authenticated
  PASS 4: jq + sqlite3 ready
  PASS 5: discovery works (13 matches for 'shadcn')

5/5 PASS — plugin healthy
```

### First-run (immediately after `/plugin install`, before bootstrap)

```
maxvision-orchestration verify-installation:
  INFO 1: index.db not yet bootstrapped (first-run state) — run /maxvision-orchestration:index-catalog --bootstrap
  PASS 2: cheatsheet found at ~/.claude/CLAUDE-agents.md or ~/.claude/CLAUDE-skills.md
  PASS 3: gh authenticated
  PASS 4: jq + sqlite3 ready
  INFO 5: BM25 query skipped (index.db not yet bootstrapped — see INFO 1)

3/5 PASS + 2 INFO — plugin healthy (first-run state)
Next: run /maxvision-orchestration:index-catalog --bootstrap to bring the index online.
```

Exit 0 in BOTH cases (first-run + steady-state) — INFO does not block. Exit 1 only on real FAIL.

If any FAIL, the line after "FAIL N:" includes a specific remediation hint.

## Guardrails

- **All 5 checks always run.** No early exit on first failure — caller wants the full picture.
- **PASS / INFO / FAIL trichotomy.** PASS = success; INFO = expected first-run state, not an error; FAIL = real problem requiring action. Healthy = PASS + INFO; only FAIL counts against health.
- **Read-only.** Never writes anywhere. `allowed-tools` excludes `Bash(rm *)`, `Bash(mv *)`, `Bash(python *)`, etc.
- **Exit code semantics.** 0 = healthy (PASS + INFO sum to 5); 1 = at least one FAIL. Useful for CI gating and for `verify-installation && some-other-skill` chains. INFO never blocks downstream chain.
- **No network calls except `gh auth status`.** That call is local-cache lookup; it doesn't hit GitHub API.
- **Strict-mode discipline.** Every bash block declares `set -euo pipefail` at its top as defense-in-depth. State (variables, arrays) carries across blocks via the SKILL interpretation contract — blocks are NOT fresh shells in current Claude Code semantics. The per-block directive is redundant when state shares correctly, but acts as a safety net if a future interpreter regresses to fresh-shell-per-block. The walker test `tests/unit/test_skill_bash_contract.py` enforces the directive's presence.
