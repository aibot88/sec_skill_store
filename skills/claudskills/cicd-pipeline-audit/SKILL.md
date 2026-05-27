---
name: cicd-pipeline-audit
description: Audit CI/CD pipelines (GitHub Actions, GitLab CI, CircleCI, Azure Pipelines, Jenkins, Bitbucket) for security, reliability, reproducibility, supply chain, and deploy safety. One sub-agent per workflow. Static, live, apply, and runtime modes.
argument-hint: [workflow-path-or-glob]
allowed-tools: Read Grep Glob Write Edit Bash(bash:*) Agent
effort: high
paths: ".github/workflows/*.{yml,yaml}"
---

# CI/CD Pipeline Audit

ultrathink

<!-- anthril-output-directive -->
> **Output path directive (canonical — overrides in-body references).**
> All file outputs from this skill MUST be written under `.anthril/audits/cicd-pipeline-audit/`.
> Run `mkdir -p .anthril/audits/cicd-pipeline-audit` before the first `Write` call.
> Primary artefact: `.anthril/audits/cicd-pipeline-audit/<artefact>`.
> Do NOT write to the project root or to bare filenames at cwd.
> Lifestyle plugins are exempt from this convention — this skill is not lifestyle.

## When to use

Run this skill when the user mentions:
- CI/CD audit, GitHub Actions review, pipeline security
- Workflow hardening, release pipeline review
- Supply chain (SBOM, provenance, signed artefacts)
- Concerns about third-party action pinning, minimal permissions, OIDC vs long-lived tokens

Covers eight categories across every CI platform: security (minimal permissions, SHA-pinned actions), reliability (timeouts, concurrency, retry), reproducibility (pinned runners and tool versions), speed (cache keys, path filters), supply chain (provenance, SBOM, signing), secrets hygiene, deploy safety (approval gates, environment protection), and observability (failure notifications, required status checks).

## Before You Start

1. **Determine operating mode.** Read `$ARGUMENTS` for mode flags: `--live` enables `gh` / `glab` / `circleci` CLI reads; `--apply` enables per-finding patching; `--runtime` runs `gh workflow run` or equivalent against a non-prod workflow dispatch. Default is static-file audit.
2. **Find all CI configs.** Run `scripts/list-workflows.sh` — it enumerates every known CI system's config files and prints one `platform:path` line per file.
3. **Load `.cicd-ignore`.** If present, parse as suppression rules.
4. **Sub-agent budget.** Phase 4 spawns one `Agent(subagent_type=Explore)` per workflow file. Warn the user if more than 15 workflow files were found and offer to narrow scope.
5. **Production-name guard.** If `--runtime` was passed and any target workflow's name contains `prod`/`production`, refuse without `--i-really-mean-prod`.

## User Context

$ARGUMENTS

Workflow inventory: !`bash "${CLAUDE_PLUGIN_ROOT}/skills/cicd-pipeline-audit/scripts/list-workflows.sh"`

Live mode availability: !`which gh 2>/dev/null || echo "gh:unavailable"`

---

## Audit Phases

---

### Phase 1: Discovery & Mode Selection

**Objective:** Lock in the platform inventory and confirm modes.

1. Parse the workflow inventory output. Group by platform (github-actions, gitlab-ci, circleci, azure-pipelines, jenkins, bitbucket).
2. If `$ARGUMENTS` names a specific path or glob, filter to that set. Otherwise confirm the full list with the user via `AskUserQuestion` if >15 files.
3. Record the operating mode. In `--live` mode, verify platform CLIs are available (`gh --version`, `glab --version`). Fall back to static mode for any platform whose CLI isn't available — announce the fallback.
4. Record selected modes for the rest of the run.

### Phase 2: Per-Workflow Snapshot

**Objective:** Produce a compact JSON snapshot per file so sub-agents start from the same base.

For each workflow file, extract:

- Triggers (`on:` events), branch filters, path filters
- Jobs (names, `runs-on`, `needs`, `if` conditions, `timeout-minutes`, `concurrency`)
- Steps (action references with version pin style — SHA / tag / branch / unpinned)
- Permissions block (job-level + workflow-level)
- Secrets referenced (`${{ secrets.* }}`)
- Environment references (`environment:` blocks)
- Cache usage (`actions/cache@*`, built-in cache config)
- Matrix configuration (fail-fast, parallel, include/exclude)
- Reusable workflow references (`uses: ./.github/workflows/*.yml` or `org/repo/.github/workflows/*.yml@*`)

In `--live` mode, additionally fetch:

- Recent run success/failure rates (`gh run list --workflow=<file> --limit 50 --json status,conclusion,createdAt`)
- Repository-level permissions and required status checks (`gh api repos/:owner/:repo`)
- Branch protection rules for `main` / `master` / default branch

Store snapshots as a dict keyed by workflow filename.

### Phase 3: Cross-Workflow Inventory

**Objective:** Detect duplication and shared-concern candidates before sub-agents go deep.

1. Cluster jobs by step pattern similarity (identical or near-identical sequences suggest reusable-workflow candidates).
2. Map which workflows deploy to which environments.
3. Identify the canonical release workflow (the one that actually publishes to production) for later weighting in the risk register.

### Phase 4: Parallel Sub-Agent Audit

**Objective:** Walk each workflow through the eight audit categories in parallel.

For each workflow in scope, spawn one `Agent(subagent_type=Explore)` using `templates/subagent-prompt-template.md`. Issue all sub-agent calls in a single assistant message.

Each sub-agent receives:
- The workflow file path and its Phase 2 snapshot JSON
- The audit taxonomy (A–H) from `reference.md` §1
- The severity rubric from `reference.md` §2
- The operating mode (static / live / apply / runtime)
- Permission to call read-only `gh` / `glab` commands if mode is live+
- The list of identified canonical release workflows (for weighting)

Categories each sub-agent walks:

- **A. Security** — minimal `permissions:`? `pull_request_target` misuse? third-party actions pinned by commit SHA, not tag? secrets not used in `if:` conditions (leaks via logs)? OIDC cloud auth instead of long-lived tokens? `GITHUB_TOKEN` scope?
- **B. Reliability** — concurrency group with `cancel-in-progress`? `timeout-minutes` on every job? retry strategy on flaky steps? matrix `fail-fast`?
- **C. Reproducibility** — runner pinned to a specific version (no `ubuntu-latest` on release)? tool versions pinned (`setup-node@vN` with exact `node-version`)? lockfiles checked in and used?
- **D. Speed & Cache** — dependency cache keyed on lockfile hash? path filters on `on.push.paths`? artefact reuse between jobs? parallel matrix sensibly bounded?
- **E. Supply chain** — `--provenance` on `npm publish`? SBOM generated and attached to releases? artefacts signed (cosign / sigstore)? third-party actions from trusted orgs?
- **F. Secrets hygiene** — no `echo ${{ secrets.* }}`? secrets not interpolated into shell strings? secrets masked in logs? env var names don't mirror the secret name?
- **G. Deploy safety** — manual approval gate on prod deploys? `environment:` protection rules referenced? required reviewers on prod environment?
- **H. Observability** — failure notifications (Slack / email) configured? required status checks on protected branches? runtime failure rates acceptable (live mode only)?

Each sub-agent returns structured JSON matching `templates/findings-schema.json`: one finding per issue with `id`, `file:line`, `evidence`, `severity`, `remediation`.

Sub-agents MUST NOT:
- Modify any workflow file (only the main skill applies changes in Phase 7)
- Call `gh` write operations (`gh run cancel`, `gh workflow disable`)
- Fabricate findings without `file:line` evidence

### Phase 5: Cross-Workflow Risk Synthesis

**Objective:** Roll findings up and identify cross-cutting issues.

1. Merge all sub-agent JSONs.
2. Deduplicate near-identical findings across workflows into "pattern" findings (e.g., "five workflows reference `actions/checkout@v4` by tag, not SHA" → one pattern finding with five targets).
3. Apply severity adjustments:
   - Findings on the canonical release workflow keep severity (or upgrade one tier if Supply Chain).
   - Findings on disabled workflows downgrade two tiers.
   - Findings matched by `.cicd-ignore` are suppressed to an appendix.
4. Assign stable IDs: `CI-001`, `CI-002`, … in severity-then-category order.

### Phase 6: Remediation Drafting

**Objective:** For every CRITICAL / HIGH / MEDIUM finding, emit a commented YAML block into `cicd-suggested.yml`.

Template per finding:

```yaml
# =============================================================================
# CI-NNN — <severity> — <category>.<subtype>
# Target: <workflow-file>:<line>
# Evidence: <one-line>
# MANUAL REVIEW REQUIRED — DO NOT APPLY BLINDLY
# =============================================================================
# Suggested change (replace the matching block in the workflow):
<yaml snippet>
```

Rules:

- Third-party action pin suggestions include the exact commit SHA looked up via `gh api repos/<owner>/<repo>/commits/<tag>` in `--live` mode, or a placeholder `<SHA_OF_vX.Y.Z>` in static mode.
- Secret-handling fixes show both the broken pattern and the fix side-by-side.
- Permission-minimisation blocks list the specific permissions needed for the job (not a blanket `contents: read`).
- INFO / FLAG-ONLY findings do not emit YAML — they reference the finding ID in the markdown report only.

### Phase 7: Apply Mode (opt-in)

**Objective:** When `--apply` was passed, offer per-finding application.

1. For each CRITICAL / HIGH / MEDIUM finding with an auto-applicable remediation:
   - Show the user the diff.
   - Ask `[a]pply / [s]kip / apply [A]ll remaining / [q]uit`.
   - If applied, use `Edit` to patch the workflow file and append an entry to `apply-log.md` with timestamp, target, before/after, and the revert command (`git checkout HEAD -- <file>` or the inverse patch).
2. Destructive apply (removing a workflow, disabling an environment) requires a second confirmation with literal word `DESTROY` — no typeahead.
3. Findings without auto-applicable remediations are listed as "manual follow-up required" at the end of the apply loop.

### Phase 8: Runtime Testing (opt-in)

**Objective:** When `--runtime` was passed, trigger a one-time workflow dispatch against a non-prod target to verify the audit findings and measure baseline speed.

1. Identify a safe dispatchable target: workflow_dispatch enabled, NOT the prod release workflow, matching ref `main` or similar.
2. Run `gh workflow run <file> --ref <safe-branch>` with a benign input set.
3. Poll for completion via `gh run watch`.
4. Record duration, step-level timings, cache hit/miss, artefact sizes.
5. Attach the run summary to the report as "Runtime baseline".

### Phase 9: Reporting

**Objective:** Render the final artefacts using `templates/output-template.md`.

Required sections in `cicd-pipeline-audit.md`:

1. Header (platforms found, total workflows audited, mode, date)
2. Executive summary (verdict tier, top three risks)
3. Per-platform findings tables
4. Cross-workflow pattern findings
5. Runtime baseline (if `--runtime`)
6. Apply log reference (if `--apply`)
7. Risk register with stable IDs
8. Prioritised action batches
9. Suppressed appendix

Also write `cicd-pipeline-audit.json` (all findings, machine-readable) and `cicd-suggested.yml` (commented remediations).

---

## Scoring

Score per category using the rubric in `reference.md` §3. Aggregate to a single verdict:

| Total | Verdict |
|---|---|
| 90–100 | PASS |
| 70–89 | PASS WITH WARNINGS |
| 50–69 | CONDITIONAL — significant issues |
| < 50 | FAIL |

---

## Important Principles

- **Evidence or it doesn't exist.** Every finding carries `file:line` and the excerpt.
- **Third-party actions are a supply-chain risk.** Tag pins are not pins. A tag can be moved. SHA pins are immutable. Flag every non-SHA third-party action.
- **`GITHUB_TOKEN` default is too broad.** Most workflows only need `contents: read`. Flag any workflow relying on the default scope.
- **Secrets in `if:` leak.** `if: ${{ secrets.FOO != '' }}` prints the secret in the evaluation log on some platforms. Treat as CRITICAL.
- **The canonical release workflow matters most.** Weight findings on it higher.
- **Never modify disabled workflows silently.** If `--apply` would edit a disabled workflow, surface that and ask.
- **Runtime mode is non-prod only.** Refuse matching target names against `prod`/`production` without `--i-really-mean-prod`.
- **Australian English. DD/MM/YYYY. Markdown-first.**

---

## Edge Cases

1. **No CI configs found.** Emit a short report with the single finding "No CI/CD configured" at CRITICAL (if repo size > trivial) or INFO (if repo is pre-launch).
2. **Mixed platforms (GitHub + GitLab).** Audit each independently. Sub-agents are platform-aware via their prompt.
3. **Reusable workflows (`uses: org/repo/.github/workflows/*.yml@*`).** Audit the caller's reference (pinned?) but do not recurse into the called workflow unless it's in this repo.
4. **Monorepo with many workflows.** Cluster by service/directory and offer per-cluster audit.
5. **Jenkins Jenkinsfile (Groovy).** Parse as text; flag `sh` / `bat` steps that embed credentials.
6. **Workflow with no runs in 6+ months (live mode).** Flag as "possibly dead" and downgrade severity of findings on it.
7. **OIDC already configured.** Flag any long-lived cloud tokens co-existing with OIDC as redundant.
8. **GitHub Actions matrix with `include:` overrides.** Cross-check that every matrix cell has consistent timeout / permissions.
9. **`--apply` disabled via hook.** Respect a repo-level `.cicd-ignore` entry `no-apply` that disables Phase 7 even when `--apply` flag is present.
10. **No network access.** If `--live` was passed but network calls fail, fall back to static audit with a note.
