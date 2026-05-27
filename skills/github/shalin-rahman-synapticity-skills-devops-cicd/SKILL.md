# Skill: CI/CD & DevOps Best Practices (Staff Engineer)
# Usage: Use when configuring pipelines, deployments, and operational infrastructure.

## 🚀 Continuous Integration (CI)
- **Automated Testing**: Every push must trigger a comprehensive suite of Unit and Integration tests. The build must fail if tests fail.
- **Static Analysis & Linting**: Enforce code style and quality gates automatically. The build must fail on critical code smells or security flaws.
- **Fast Feedback**: The CI loop should be as fast as possible to keep developers productive.
- **Immutable Artifacts**: Build once, deploy many. The exact same container/artifact tested in CI must be what runs in Production.

## 🚢 Continuous Deployment / Delivery (CD)
- **Zero-Downtime Deployments**: Use strategies like Blue/Green, Canary, or Rolling Updates.
- **Infrastructure as Code (IaC)**: Provision and manage infrastructure using code (Terraform, CloudFormation, Bicep). Never configure environments manually via a UI console.
- **Configuration Management**: Externalize configurations. Applications should read configs from Environment Variables or secure stores (e.g., Azure Key Vault, AWS Secrets Manager), not hardcoded files.

## 🔭 Observability & Telemetry
- **Structured Logging**: Log in JSON format to allow easy searching and indexing in tools like ELK, Datadog, or Application Insights.
- **Correlation IDs**: Attach a unique request ID to every incoming request and pass it through all downstream services to trace the entire lifecycle of a transaction.
- **Health Checks**: Expose a `/health` or `/ready` endpoint so load balancers and orchestrators (like Kubernetes) know the application's state.

## 🔐 DevSecOps
- **Shift Left Security**: Integrate security scans (SAST, DAST, dependency checking) directly into the CI pipeline.
- **Secret Hygiene**: Never commit secrets to version control. Use secret management tools.
- **Principle of Least Privilege**: Grant applications and CI runners only the minimum permissions necessary to perform their tasks.

## 🚫 Anti-Patterns
- Manual deployments or "copying files to the server".
- Committing secrets or API keys to the repository.
- Treating Infrastructure as "pets" (hand-crafted, hard to replace) rather than "cattle" (easily replaceable, reproducible via code).
