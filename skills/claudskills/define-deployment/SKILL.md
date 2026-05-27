---
name: define-deployment
description: Capture deployment characteristics for both production and development — hosting, IaC, CI/CD, secrets, observability, local dev environment, containerization, hot reload, and seed data. Use when the project-builder agent is gathering deployment information.
---

# Purpose

Ground the project in *where* and *how* it runs — for the developer inner loop and for production.

# Questions to ask (in order)

## Production

1. Hosting target: self-hosted (VM or Kubernetes), managed PaaS (Fly, Render, Railway, Heroku), serverless (AWS Lambda, Cloudflare Workers, Vercel, Netlify), managed containers (ECS, Cloud Run, App Runner), on-prem, or hybrid.
2. Cloud provider (if any): AWS, GCP, Azure, Cloudflare, DigitalOcean, other.
3. Infrastructure as Code: none (manual), Terraform, Pulumi, CDK, CloudFormation, or provider-native manifests (`fly.toml`, `render.yaml`, etc.).
4. CI/CD: GitHub Actions, GitLab CI, CircleCI, Jenkins, Buildkite, or none.
5. Environments: prod only / prod + staging / prod + staging + preview-per-PR.
6. Secrets management: `.env` plus platform secrets, HashiCorp Vault, AWS Secrets Manager, Doppler, 1Password CLI, SOPS.
7. Observability in production: log sink, metrics sink, tracing sink.
8. Backup and disaster-recovery expectations: none, daily snapshot, point-in-time recovery, multi-region.

## Development

9. Local dev environment: native toolchain, devcontainer, Nix, Docker Compose, Vagrant, or remote dev (Codespaces, Gitpod).
10. Containerization: not used, optional, or required (include Dockerfile).
11. Hot reload / fast feedback expectations.
12. Seed data strategy: none, fixtures, factories, synthetic generator, or anonymized prod snapshot.
13. Database migrations tool (if applicable).

Use `AskUserQuestion` for the multi-choice items.

# Solution space to present

- **Hosting tradeoffs**: serverless (scale-to-zero, cold starts, vendor shape) vs. managed containers (flexible, some ops) vs. PaaS (simple, opinionated) vs. Kubernetes (powerful, heavy).
- **IaC tradeoffs**: Terraform (ubiquitous, HCL), Pulumi/CDK (real languages, narrower ecosystem), provider-native (fast start, vendor-locked), manual (only acceptable for prototypes).
- **Local dev tradeoffs**: native (fastest inner loop, more per-machine setup) vs. devcontainer/Docker (reproducible, slower iteration) vs. remote dev (zero local setup, requires connectivity).

# Required schema

- `prod`: `{hosting, cloud, iac, ci_cd, environments, secrets, observability, dr}`
- `dev`: `{environment, containerization, hot_reload, seed_data, migrations}`

# Output

Write to `PROJECT_BRIEF.md` under a `## Deployment` heading. Replace any prior `## Deployment` section when re-run.

# Frontmatter contribution

Update these YAML frontmatter fields (see `CLAUDE.md` for the full schema). Leave every other field untouched:

- `deployment.provider` — the cloud provider or hosting target (e.g., `aws`, `gcp`, `azure`, `fly`, `render`, `self-hosted`, `on-prem`)
- `deployment.iac` — the IaC tool (`terraform`, `pulumi`, `cdk`, `cloudformation`, `sam`, `none`)
- `deployment.environments` — list of environments (e.g., `[prod]`, `[dev, staging, prod]`)
