---
name: ship-loop
description: "Full cycle: audit site, check Dependabot alerts, fix issues, push, verify CI, deploy, close. Prioritizes Security > Availability > New features. Parallel dispatch for speed."
user-invocable: true
---

# Ship Loop

Autonomous continuous improvement loop with **parallel dispatch**. Runs discovery, implementation, and verification concurrently to maximize throughput.

**Priority principle: Security > Availability > New features.**

**Speed principle: Parallelize everything. Never block when you can pipeline.**

## Architecture: Pipelined Parallel Loop

```
┌─────────────────────────────────────────────────────────┐
│ ITERATION N                                             │
│                                                         │
│  Phase A: Discover (parallel)                           │
│  ├── A1. CI health check          ─┐                    │
│  ├── A2. Dependabot alerts         ├── all in parallel  │
│  ├── A2.5. Smoke audit (if merge)  │                    │
│  └── A3. Check previous PRs/CI    ─┘                    │
│            │                                            │
│  Phase B: Dispatch (parallel batch)                     │
│  ├── Agent 1: issue #59 ──┐                             │
│  ├── Agent 2: issue #62   ├── up to 5 in parallel      │
│  └── Agent 3: issue #63 ──┘                             │
│            │                                            │
│  Phase C: Collect & verify (parallel)                   │
│  ├── Check CI for PR from iteration N-1 ─┐             │
│  ├── Health check deploys                 ├── parallel  │
│  └── Close verified issues               ─┘             │
│            │                                            │
│  Phase D: Loop or stop                                  │
└─────────────────────────────────────────────────────────┘
```

Key insight: **Phase C checks results from the PREVIOUS iteration** while Phase B works on the CURRENT batch. No blocking waits.

## Phase A: Discover Work (all steps in parallel)

Run ALL discovery steps simultaneously:

### A1. CI Health Check (parallel)

```bash
gh run list --branch main --limit 5 --json status,conclusion,name,databaseId \
  | jq '[.[] | select(.conclusion == "failure")]'
```

If failures exist, create `ci-fix` issues (or pick up existing ones).

### A2. Security Audit — Dependabot Alerts (parallel, cached)

**Cache logic:** Read `.claude/state/dependabot-cache.json` before calling the API. Skip the API call when `lastAlertCount == 0` AND `iterationsSinceCheck < 10` (~30 min). Always check when the cache is missing, stale, or had alerts last time.

```bash
# Read cache (create .claude/state/ if missing)
mkdir -p .claude/state
CACHE_FILE=".claude/state/dependabot-cache.json"
if [ -f "$CACHE_FILE" ]; then
  LAST_COUNT=$(jq -r '.lastAlertCount // -1' "$CACHE_FILE")
  ITERS=$(jq -r '.iterationsSinceCheck // 99' "$CACHE_FILE")
else
  LAST_COUNT=-1
  ITERS=99
fi

# Skip if no alerts last time and checked recently
if [ "$LAST_COUNT" -eq 0 ] && [ "$ITERS" -lt 10 ]; then
  echo "Dependabot: cached (0 alerts, $ITERS iterations ago) — skipping"
  # Increment iteration counter
  jq '.iterationsSinceCheck += 1' "$CACHE_FILE" > "${CACHE_FILE}.tmp" && mv "${CACHE_FILE}.tmp" "$CACHE_FILE"
else
  # Run the actual API check
  ALERTS=$(gh api repos/{owner}/{repo}/dependabot/alerts \
    --jq '[.[] | select(.state=="open") | select(.security_advisory.severity=="critical" or .security_advisory.severity=="high")] | .[] | {number, severity: .security_advisory.severity, package: .security_vulnerability.package.name, summary: .security_advisory.summary}')
  ALERT_COUNT=$(echo "$ALERTS" | jq -s 'length')

  # Update cache
  echo "{\"lastAlertCount\": $ALERT_COUNT, \"iterationsSinceCheck\": 0, \"lastCheckTime\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > "$CACHE_FILE"

  # Process alerts if any
  echo "$ALERTS"
fi
```

For each critical/high alert without an existing issue:

```bash
gh issue create \
  --title "fix(security): <package> — <summary>" \
  --body "Dependabot alert #<number>. Severity: <severity>.\n\n<details from alert>" \
  --label "ci-fix,ready"
```

### A2.5. Smoke Audit (parallel, if recent merge)

```bash
git diff HEAD~1 --name-only
```

Invoke `/site-audit smoke` — maps changed files to surfaces, runs Lighthouse + console checks in parallel, creates `ci-fix` + `audit` issues for regressions.

### A3. Check Previous Batch Results (parallel)

Check PRs and CI from the **previous iteration's** agents:

```bash
# Find all PRs from agent branches that are still open
gh pr list --author "@me" --json number,title,headRefName,statusCheckRollup,reviewDecision \
  --jq '.[] | select(.headRefName | startswith("agent/"))'
```

For each agent PR, first classify the PR's risk level:

```bash
# Get the list of changed files for the PR
gh pr diff <number> --name-only
```

**Low-risk patterns** — a PR is low-risk when ALL changed files fall into one of:
- Test files: `*.test.ts`, `*.test.tsx`, `*.spec.ts`, `*.spec.tsx`, `*.test.js`, `*.spec.js`, `*.test.jsx`, `*.spec.jsx`
- Documentation: `*.md`, `docs/**`
- Dependency manifests: `package.json`, `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`
- Config files: `.github/**`, `.claude/**`, `turbo.json`, `*.config.ts`, `*.config.js`, `*.config.mjs`

Use `isLowRiskPR(files)` from `@mbe/agent-core` if scripting this check.

**Decision matrix:**

| CI status | Risk level | Action |
|-----------|-----------|--------|
| passed | low-risk | **Merge immediately** — do not wait for next iteration |
| passed | other | Merge it, close the linked issue |
| failed | any | Create `ci-fix` issue, label original as `agent-failed` |
| changes requested | any | Queue for PR feedback loop (if wired in) |
| pending | any | Skip — check again next iteration |

```bash
# Auto-merge PRs where CI passed (low-risk: merge right now)
gh pr merge <number> --squash --delete-branch

# Close linked issue
gh issue close <linked-number> --comment "Merged via ship-loop. Deployed."
```

**Why immediate merge for low-risk PRs?** Test/docs/deps/config changes cannot break the running application. Merging them right away frees up issue slots and keeps the backlog moving without wasting an entire loop iteration on a trivial wait.

### A4. Gather & Claim Batch

After all discovery steps complete, gather the full issue backlog:

```bash
gh issue list --label "ready" --state open --json number,title,body,labels --limit 20
```

**Sort by priority:**
1. Security vulnerabilities (`ci-fix` + `fix(security):`)
2. CI failures (other `ci-fix`)
3. Features (`feature`)
4. Audit findings (`audit`)

**Filter for independence:**
- Skip issues with unresolved `Depends on: #N` in their body
- Skip issues in the same zone as another issue in this batch (prevent merge conflicts)
- Skip issues labeled `in-progress` or `stealable`

**Claim up to 5 independent issues:**

```bash
# Claim each issue in the batch
for NUMBER in $BATCH; do
  gh issue edit $NUMBER --add-label "in-progress" --remove-label "ready"
done
```

## Phase B: Implement in Parallel Agents

Launch **one worktree agent per issue**, all simultaneously:

```bash
# Dispatch all agents in parallel (use & for background)
for issue in $BATCH; do
  mbe agent run "<issue title> (closes #<issue_number>)" \
    --model claude-sonnet-4-6 \
    --max-budget 1.00 \
    --max-turns 50 &
done

# Wait for all to complete
wait
```

Or use `mbe agent orchestrate` for managed parallel dispatch:

```bash
mbe agent orchestrate "Fix issues: #59, #62, #63" \
  --max-budget 1.00 \
  --max-concurrent 5
```

### Security Instructions for ALL Worktree Agents

Every worktree agent prompt MUST include:

> **Security rules (non-negotiable):**
>
> - Never introduce hardcoded secrets, SQL injection, XSS, or other OWASP Top 10 vulnerabilities.
> - Never commit `.env` files, credentials, API keys, tokens, or secrets of any kind.
> - Use parameterized queries for all database operations.
> - Sanitize all user input before rendering in HTML.
> - Validate all external data at system boundaries.
> - Follow the security checklist in `~/.claude/rules/common/security.md`.
> - If you discover an existing security vulnerability, stop feature work and fix it first.

### Built-in Agent Resilience

Agent-core includes automatic protections:

- **Stuck detection** — 6 failure patterns detected, aborts early to save budget
- **LLM success evaluation** — haiku verifies the diff actually addresses the issue
- **Draft PRs on failure** — partial work preserved for human inspection
- **Failure memory** — past failure context injected so agents try different approaches

### Agent Outcome Handling (per agent, as they complete)

Don't wait for all agents — handle results as each finishes:

```bash
# On success (evaluation passed)
gh issue edit <number> --add-label "has-pr" --remove-label "in-progress"

# On partial success (draft PR from failed/stuck session)
gh issue edit <number> --add-label "needs-review" --remove-label "in-progress"

# On failure (no changes produced)
gh issue edit <number> --add-label "agent-failed" --remove-label "in-progress"

# On second failure of same issue
gh issue edit <number> --add-label "stealable"
```

## Phase C: Verify Previous Batch (pipelined, parallel)

**This runs at the START of each iteration (in Phase A3), not after Phase B.** By the time we're dispatching new agents, the previous batch's PRs have had time to go through CI and deploy.

### Health Verification (parallel with other Phase A steps)

```bash
# All health checks in parallel
curl -sf https://mattbutlerengineering.com/ > /dev/null &
curl -sf https://mattbutlerengineering.com/hospitality > /dev/null &
curl -sf https://mattbutlerengineering.com/rialto > /dev/null &

for endpoint in \
  "https://mattbutlerengineering.com/api/v1/users/health" \
  "https://mattbutlerengineering.com/api/health"; do
  curl -sf "$endpoint" | jq -e '.status == "ok"' > /dev/null &
done

wait
```

**If verification fails:**
1. Rollback (CF: `wrangler rollback`, DO: `git revert HEAD -m 1`)
2. Create `ci-fix` issue
3. Counts as failure toward circuit breaker

## Phase D: Loop or Stop

- If time/budget remains, return to **Phase A**
- **Circuit breaker:** 3 consecutive failures (across all agents in a batch) → stop and report
- Log iteration metrics: issues claimed, PRs created, PRs merged, failures
- Report throughput: "Iteration N: 4 issues dispatched, 3 PRs created, 2 merged from last batch"

## Concurrency Rules

### Safe to Parallelize
- Issues in **different zones** (hospitality page + rialto component + API endpoint)
- Issues that touch **different files** (check sourceFiles in audit inventory)
- Discovery steps (CI check + Dependabot + smoke audit)
- Health checks across different endpoints

### NOT Safe to Parallelize
- Issues in the **same zone** that likely touch the same files → merge conflicts
- Issues with `Depends on: #N` where #N is in the same batch
- Multiple changes to the same service's schema/migrations

### Conflict Prevention

Before adding an issue to the batch, check:

```bash
# Get the zone from issue body or title prefix
# Ensure no other issue in this batch shares the zone
```

If two issues would conflict, pick the higher-priority one. The other waits for the next iteration.

### Max Batch Size

- **Default: 5** concurrent agents
- Adjust based on: available budget ($1/agent × 5 = $5/iteration max), CI capacity, deploy pipeline throughput
- Security issues always get a slot regardless of batch size

## Safety Rails

### Security Rails (highest priority)

- **Security > Availability > New features.** Security issues always get priority slots in the batch.
- Never commit `.env` files, credentials, or secrets.
- Dependabot critical/high alerts block feature work — fill remaining batch slots with security fixes first.
- Every worktree agent inherits security instructions.

### General Rails

- Never force-push to `main`
- Never skip CI checks or pre-commit hooks
- Never delete production data or resources
- Each agent gets its own worktree — no shared state between parallel agents
- If CI fails after merge, create `ci-fix` issue and handle it next iteration
- Circuit breaker: 3 consecutive batch failures → stop and report
- Keep commits small and focused — one issue per PR, one PR per agent

## GitHub Labels (State Machine)

| Label | Meaning |
|-------|---------|
| `ready` | Available for agent pickup |
| `in-progress` | Agent is working on it |
| `has-pr` | PR created, awaiting merge/review |
| `agent-failed` | Agent could not complete — needs manual review |
| `needs-review` | Agent created draft PR from failed/partial work |
| `stealable` | Agent failed twice — needs different approach or human help |
| `audit` | Found by site-audit |
| `ci-fix` | CI failure or security vulnerability needing fix |
| `feature` | New feature (created by `/decompose`) |
| `tracking` | Parent issue tracking multi-part feature |
| `meta-improvement` | Process improvement suggestion |

## Throughput Targets

| Metric | Serial (old) | Parallel (new) |
|--------|-------------|----------------|
| Issues per iteration | 1 | 3-5 |
| Time per iteration | 10-20 min | 8-12 min |
| Issues per hour | 3-6 | 15-30 |
| CI wait overhead | Blocking | Pipelined (zero) |
