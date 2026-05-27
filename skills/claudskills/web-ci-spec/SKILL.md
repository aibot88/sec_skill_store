---
name: web-ci-spec
description: Produce a sprint CI.md covering pipeline stages, secrets handling, deployment strategy, and rollback for GitHub Actions / Cloud Build / GitLab CI / etc. Coordinator-only — produces drafts, never modifies live workflows. Pauses for user confirmation.
disable-model-invocation: true
---

# /magi:web-ci-spec — CI/CD elaboration

You are the coordinator. Plan a CI/CD pipeline change and capture the
analysis in `magi/<num>-<slug>/CI.md`. **You never push to the workflow,
trigger a deploy, or rotate a secret.** Read
`references/domain/web/ci-cd.md` before starting.

## 0. Preflight

```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-}"
[[ -z "$PLUGIN_ROOT" ]] && PLUGIN_ROOT="$(cd "$(dirname "$BASH_SOURCE[0]")/../.." 2>/dev/null && pwd)"
USER_CONFIG="$HOME/.config/magi-workflow/config.json"
```

If config missing → tell user to run `/magi:setup`.


## 0.5. State preflight (auto-refuse if not allowed)

```bash
STATE_JSON=$(bash "$PLUGIN_ROOT/scripts/shared/detect-state.sh")
blocked=$(jq -r '.disallowed_skills["web-ci-spec"] // empty' <<<"$STATE_JSON")
if [[ -n "$blocked" ]]; then
  reason=$(jq -r '.disallowed_skills["web-ci-spec"].reason' <<<"$STATE_JSON")
  suggest=$(jq -r '.disallowed_skills["web-ci-spec"].suggest' <<<"$STATE_JSON")
  echo "Cannot run /magi:web-ci-spec: $reason"
  echo "Suggested: $suggest"
  exit 1
fi
```

`--force` skips preflight (advanced/recovery only).

## 1. Locate sprint + CI tool

Find the sprint folder (default: most recent; or `--sprint <num>-<slug>`).

Detect the CI tool per `references/domain/web/ci-cd.md` "Discovery":

- `.github/workflows/*.yml` → GitHub Actions
- `cloudbuild.yaml` / `cloudbuild/*.yaml` → Cloud Build
- `.gitlab-ci.yml` → GitLab CI
- `azure-pipelines.yml` → Azure DevOps
- `Jenkinsfile` → Jenkins
- `vercel.json` → Vercel
- `wrangler.toml` → Cloudflare

If multiple coexist (e.g. GHA for tests + Cloud Build for prod deploy),
document the boundary explicitly.

## 2. Read existing pipeline + spec

- List existing workflow files; for each, summarise: trigger, stages,
  duration, last failure rate (if available via `gh run list` or
  `gcloud builds list`).
- Read PLAN/SPEC.md to understand what change is needed:
  - New tests added → wire them into `test` stage?
  - New deployable surface → new deploy job?
  - New secret needed → secret store + scoping plan?
  - Performance budget regression → add budget check?

## 3. Identify CI-relevant scope

Out-of-scope: pure code changes that don't touch the pipeline. Be honest
if the user invoked this skill for something the existing pipeline
already handles — recommend they skip this skill.

## 4. Generate the CI section

Following `references/domain/web/ci-cd.md` "Deliverable":

### a. Triggers

`on: push / pull_request / workflow_dispatch / schedule / tag`. Justify
each.

### b. Stages & jobs

A table or list of stages (preflight / static / test / build / e2e /
security / publish / deploy / smoke). For each:

- What runs?
- What artifacts are produced?
- What blocks the next stage?
- Approximate duration target (so regressions can be flagged later).

Use the templates in the reference for GHA / Cloud Build skeletons.

### c. Secrets & permissions

- Which secrets does this change need?
- Where do they live? (GH Actions secrets / Secret Manager / Vault)
- Workload Identity Federation used? (preferred over key files)
- Token scope per job (`permissions:` in GHA).
- Rotation plan + owner.

Forbidden patterns to flag (echoing secrets, committing `.env.*`,
service-account JSON keys when WIF is available, `pull_request_target`
without input sanitisation): if any are proposed, mark 🔴 and push back.

### d. Caching

- Cache keys (lockfile hashes; per-OS / per-language version).
- Cache size budget if the project has hit limits.
- Layer cache strategy for Docker (`buildx --cache-from`).

### e. Deployment strategy

For deploy stages:

| Field | Spec |
|-------|------|
| Targets | staging / canary / prod |
| Strategy | rolling / blue-green / canary (% cuts) |
| Approval gate | auto / manual via environment protection rule |
| Rollback trigger | smoke fail auto / manual |
| Rollback time budget | <duration> |
| DB migration order | before / after / dual-deploy window |
| Feature flag involved? | yes/no, default state, ramp plan |

### f. Smoke tests post-deploy

Required for any shared-env deploy. Use the curl + jq pattern from the
reference. Document expected response shape.

### g. Observability for the pipeline

- Workflow run summaries (`$GITHUB_STEP_SUMMARY`).
- Notifications: Slack / Chat — what triggers them, on which channel.
- DORA tracking: deploy frequency / lead time / change failure rate / MTTR
  (only if the team tracks these).

### h. Test plan for the workflow itself

How will the user validate this change before merging?

- Draft PR run.
- `act` for GHA local sim.
- `gcloud builds submit --config=... --no-source` for Cloud Build dry-run.
- Diff the rendered config (`gh workflow view`, `gcloud builds describe`)
  against the previous version.

### i. Open questions

## 5. Generate workflow draft

Based on the section above, generate a draft workflow file:

- GHA: `magi/<num>-<slug>/.github/workflows/<name>.yml`
- Cloud Build: `magi/<num>-<slug>/cloudbuild-<name>.yaml`
- etc.

The path is **inside the doc dir** so it does not pollute the project's
real workflow directory until the user reviews and moves it.

Use the skeletons from the reference. Fill in concrete values from the
project (Node version from `.nvmrc`, package manager from lockfile, etc.).
Pin third-party actions to a specific SHA, not `@v1`.

## 6. Write CI.md

Use the deliverable template. Reference the draft workflow path.

## 7. Stop and hand off

Show the user:
- `CI.md` path
- Draft workflow path inside the sprint dir
- Top 3 risks (especially secret-handling concerns)
- Recommendation to test via `act` / draft PR / Cloud Build dry-run
  before moving the workflow to its real location.

Recommend next:
- Manual review of the draft workflow.
- `/magi:review-plan` to have other models inspect it.
- After review, user moves the file to its real location and opens a PR.

**Never push the workflow to its live location, never trigger a build,
never rotate a secret.**

## Argument parsing

- `--sprint <num>-<slug>` — explicit sprint folder.
- `--ci gha|cloudbuild|gitlab|azure|jenkins|vercel|cloudflare` — skip detection.
- `--draft-name <name>` — name for the draft workflow file.

## Conventions

- **Draft, not deploy** — outputs land in the sprint dir, never the real
  workflow path.
- **Pin third-party actions to SHA** — never `@vN` or `@main`.
- **Least privilege by default** — `permissions: contents: read` baseline,
  raise per job.
- **WIF over key files** — push back hard on any service account JSON key
  proposal.
- **Smoke tests are mandatory** for shared-env deploys.
- For very small CI changes (e.g., bumping a Node version in matrix),
  this skill is overkill — recommend an inline edit to the existing
  workflow with manual review.
