# Skill: DevOps & CI/CD

Design, automate, and optimise continuous integration pipelines, continuous delivery workflows, infrastructure-as-code, containerisation, and operational processes.

---

## Overview

Claude can write CI/CD pipeline configurations, Dockerfiles, Kubernetes manifests, Terraform modules, and operational runbooks. Use this skill to accelerate delivery pipelines, reduce toil, and build reliable infrastructure.

---

## Task Patterns

### 1. Write a CI/CD Pipeline

**Prompt template:**
```
Write a [GitHub Actions / GitLab CI / Jenkins / CircleCI] pipeline for a [language/framework] project.

Pipeline stages required:
1. [e.g., lint and static analysis]
2. [e.g., unit tests with coverage report]
3. [e.g., build and tag Docker image]
4. [e.g., deploy to staging on merge to main]
5. [e.g., deploy to production on manual approval]

Requirements:
- Cache dependencies between runs
- Fail fast on first error
- Publish test results and coverage as artifacts
- Use secrets management for credentials
- Send notifications on failure
```

---

### 2. Write a Dockerfile

**Prompt template:**
```
Write an optimised, production-ready Dockerfile for a [language/framework] application.

Application details:
- Language/runtime: [e.g., Node.js 20, Python 3.12, Go 1.22]
- Entry point: [command to start the app]
- Port: [N]
- Build tool: [e.g., npm, pip, cargo]

Requirements:
- Multi-stage build to minimise image size
- Run as non-root user
- No development dependencies in final image
- Use `.dockerignore` appropriately
- Pin base image to a specific digest or version
```

---

### 3. Write a Docker Compose Configuration

**Prompt template:**
```
Write a `docker-compose.yml` for a local development environment for [application stack].

Services:
- [service 1, e.g., web API on port 8080]
- [service 2, e.g., PostgreSQL with persistent volume]
- [service 3, e.g., Redis]
- [service 4, e.g., adminer for DB management]

Requirements:
- Health checks for all services
- Dependency ordering with `depends_on` and `condition: service_healthy`
- Volume mounts for live reload in development
- `.env` file for all configuration values
```

---

### 4. Write Kubernetes Manifests

**Prompt template:**
```
Write Kubernetes manifests for deploying [application name].

Resources needed:
- Deployment: [N] replicas, image [image:tag]
- Service: [ClusterIP / LoadBalancer / NodePort]
- ConfigMap: [list config keys]
- Secret: [list secret keys]
- HorizontalPodAutoscaler: scale between [min] and [max] replicas on [metric]
- Ingress: host [hostname], TLS, path [path]

Requirements:
- Resource requests and limits defined
- Liveness and readiness probes configured
- Rolling update strategy with zero downtime
- Pod disruption budget
```

---

### 5. Write Terraform Infrastructure

**Prompt template:**
```
Write Terraform (HCL) to provision [infrastructure component] on [AWS / GCP / Azure].

Resources to create:
- [resource 1, e.g., VPC with public/private subnets]
- [resource 2, e.g., ECS Fargate service]
- [resource 3, e.g., RDS PostgreSQL with Multi-AZ]
- [resource 4, e.g., Application Load Balancer]

Requirements:
- Use variables for all environment-specific values
- Use outputs for values needed by other modules
- Tag all resources with: environment, project, team
- Remote state in [S3/GCS/Azure Blob] with state locking
```

---

### 6. Design a Deployment Strategy

**Prompt template:**
```
Design a deployment strategy for [service] that achieves zero-downtime deployments.

Current setup:
- [describe current deployment process]
- Traffic: [N] RPS
- Acceptable error budget: [e.g., <0.1% error rate during deploy]

Compare: rolling, blue/green, canary, and feature flags.
Recommend the best approach for our context and provide the implementation plan.
```

---

### 7. Automate an Operational Task

**Prompt template:**
```
Write a [Bash / Python / Go] script to automate [operational task].

Task description: [describe what needs to happen]

Inputs: [describe]
Outputs / side effects: [describe]

Requirements:
- Idempotent (safe to run multiple times)
- Dry-run mode with `--dry-run` flag
- Logging with timestamps
- Error handling with non-zero exit codes
- Compatible with [Linux / macOS / both]
```

---

## Advanced Techniques

### GitOps Workflow Design

```
Design a GitOps workflow for deploying microservices to Kubernetes using [ArgoCD / Flux].

Repository structure:
- [app repos] contain application code and Dockerfiles
- [config repo] contains Kubernetes manifests and Helm charts

Define:
1. How application versions flow from code commit to production
2. Branch/environment mapping strategy
3. Promotion process (dev → staging → production)
4. Secret management approach (Sealed Secrets / External Secrets Operator)
5. Rollback process
```

### Observability Stack Setup

```
Set up a complete observability stack for [application] using [Prometheus + Grafana / Datadog / OpenTelemetry].

Requirements:
- Metrics: RED (Rate, Errors, Duration) for all services
- Logs: structured JSON logs shipped to [Loki / Elasticsearch / CloudWatch]
- Traces: distributed tracing across all service calls
- Alerts: PagerDuty/Slack notifications for SLO breaches

Provide: instrumentation code, dashboard config, and alert rules.
```

### Disaster Recovery Plan

```
Design a disaster recovery plan for [system].

RPO (Recovery Point Objective): [e.g., 1 hour]
RTO (Recovery Time Objective): [e.g., 4 hours]
Components: [list databases, services, storage]

Define:
1. Backup strategy for each component
2. Replication and failover approach
3. Step-by-step recovery runbook
4. DR test plan and frequency
```

---

## DevOps Best Practices

| Practice | Why |
|---|---|
| Everything as code (IaC) | Reproducible, version-controlled infrastructure |
| Immutable infrastructure | No config drift; rollback is instant |
| Build once, deploy everywhere | Same artefact across all environments |
| Shift security left | Scan in CI, not after deployment |
| Feature flags over feature branches | Decouple deployment from release |
| Runbooks for every alert | Reduces MTTR; enables on-call rotation |
| Chaos engineering | Proves resilience before incidents do |

---

## CI/CD Pipeline Checklist

- [ ] Pipeline runs on every pull request
- [ ] Linting and static analysis in CI
- [ ] Tests run with coverage threshold enforced
- [ ] Security scanning (SAST, dependency audit) in CI
- [ ] Docker image built and scanned in CI
- [ ] Staging deployment automated on merge to main
- [ ] Production deployment requires manual approval or passes canary criteria
- [ ] Rollback procedure documented and tested
- [ ] Alerts configured for deployment failures
- [ ] Pipeline runtime under [N] minutes
