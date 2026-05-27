---
name: afx-cicd-scaffold
description: Bootstrap a complete .github/workflows/ set for a new project: CI (build/test/lint), CD (workflow_dispatch with env choice + OIDC + ECR), security-scan (gitleaks + dependency scan + CodeQL), and optional database-migration. Use this skill when the user wants to add GitHub Actions CI/CD to a project that does not already have it, or when they want to add missing workflows alongside existing ones.
---

# Artifex CI/CD Scaffold Skill

**For Claude Code AI Assistant**

This skill generates a production-ready `.github/workflows/` set for a project, replicating the patterns used in `zoe` and `xenia/pms`. It auto-detects the project stack and produces correctly-wired workflow files with all required secrets and variables documented inline.

## What this skill generates

| File | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | Runs on PR open/sync: build, test, lint. Stack-aware. |
| `.github/workflows/cd.yml` | Manual deploy via `workflow_dispatch` with environment choice (staging / prod). OIDC auth, ECR image build/push, ECS deploy. |
| `.github/workflows/security-scan.yml` | GitLeaks secret scan + OWASP dependency check + CodeQL SAST. Scheduled daily + PR trigger. |
| `.github/workflows/database-migration.yml` | Optional. Flyway migrations via Gradle. Validates on PR, deploys on `workflow_dispatch`. |
| `.gitleaks.toml` | GitLeaks configuration (dropped at project root alongside `.github/`). |

## Stack detection

The script scans the project root for these marker files:

| Marker | Detected stack |
|--------|---------------|
| `gradlew` or `pom.xml` | JVM/Gradle (default) |
| `package.json` | Node.js |
| `Cargo.toml` | Rust |
| `go.mod` | Go |

If none is found, JVM/Gradle is used (the user's primary stack).

## Key design decisions

- **Manual deploy only.** `cd.yml` uses `workflow_dispatch` with an environment input — no auto-deploy on push to main. This is intentional and must not be changed.
- **OIDC for AWS auth.** No long-lived credentials. The required IAM role pattern is documented in the `cd.yml` header as `arn:aws:iam::<account>:role/<project>-gha-deploy-<env>`.
- **Concurrency group `deploy-${{ inputs.environment }}`** with `cancel-in-progress: false`. Prevents two prod deploys racing. This is the xenia/pms pattern.
- **`--force` required to overwrite.** Existing files are never silently clobbered. New files are always added side-by-side.

## Conversational Routing

| User phrasing | Action |
|---------------|--------|
| "add CI/CD to my project", "scaffold GitHub Actions", "set up workflows" | Run `init` in the project directory |
| "add CI/CD without the database migration" | Run `init --no-db-migration` |
| "preview what would be created" | Run `init --dry-run` |
| "overwrite my existing workflows" | Run `init --force` |
| "add security scanning" | Run `init` — security-scan.yml is always included |

If the user is working in a specific project directory, use that directory as the target. If no project directory is given, default to the current working directory.

## How to run this skill

### Standard scaffolding

1. Confirm the target project directory.
2. Preview with `--dry-run`:
   ```bash
   ~/.claude/skills/afx-cicd-scaffold/afx-cicd-scaffold.sh init /path/to/project --dry-run
   ```
3. Show the user what would be generated.
4. If they approve, run for real (with optional `--no-db-migration` if they do not use a database):
   ```bash
   ~/.claude/skills/afx-cicd-scaffold/afx-cicd-scaffold.sh init /path/to/project
   ```
5. Walk the user through the next steps printed by the script:
   - Review and customise the generated files
   - Set the secrets and variables listed in the file header comments
   - Create the OIDC IAM roles for `cd.yml`
   - Commit the files

### Adding workflows to an existing project

If `.github/workflows/` already exists:
- New files (ones not already present) are added automatically without `--force`.
- Existing files are skipped with a warning.
- If the user wants to regenerate all files from scratch, re-run with `--force`.

### Database migration workflow

When the script runs interactively, it prompts whether to include `database-migration.yml`. The user can suppress the prompt with `--no-db-migration`. If the session is non-interactive (piped), the migration file is skipped by default.

## Required secrets and variables reference

All are documented inline in the generated file headers. Key ones for `cd.yml`:

| Name | Type | Description |
|------|------|-------------|
| `AWS_ROLE_ARN_STAGING` | Secret | OIDC role ARN for staging: `arn:aws:iam::<acct>:role/<project>-gha-deploy-staging` |
| `AWS_ROLE_ARN_PROD` | Secret | OIDC role ARN for production: `arn:aws:iam::<acct>:role/<project>-gha-deploy-prod` |
| `STAGING_URL` | Secret | Base URL for staging smoke tests |
| `PROD_URL` | Secret | Base URL for production smoke tests |
| `AWS_REGION` | Variable | AWS region (e.g. `us-east-1`) |
| `ECR_REPOSITORY` | Variable | ECR repository name |
| `ECS_SERVICE` | Variable | ECS service name |
| `ECS_CLUSTER_STAGING` | Variable | ECS cluster name for staging |
| `ECS_CLUSTER_PROD` | Variable | ECS cluster name for production |

## Version

1.0.0 (ticket 12.2)
