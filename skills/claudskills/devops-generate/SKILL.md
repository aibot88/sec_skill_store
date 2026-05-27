---
name: devops-generate
description: Use when called by the devops dispatcher after security review to generate all DevOps config files based on analysis.json and security-findings.json
---

# DevOps Config Generation

## Overview

Reads `devops/report/analysis.json` and `devops/report/security-findings.json`. Generates working config templates to `devops/working/`. All files are templates — the user reviews and adapts them.

## Inputs

Read both JSON files before generating anything. Key fields:
- `stack.language` — determines Dockerfile and CI templates to use
- `choices.ci_cd_platform` — primary platform (generate ALL three regardless)
- `choices.deployment_target` — determines if k8s/ and/or infra/ are generated
- `choices.cloud_provider` — determines if infra/ is generated
- `selected_tools` — from security-findings.json, determines which security steps are injected

## Always Generate

Generate these for every project regardless of choices.

---

### Dockerfile (production)

`devops/working/containers/Dockerfile`

Generate a multi-stage production Dockerfile for the detected language. Always: non-root user, specific version pins, multi-stage build to minimize final image size.

**Node.js / TypeScript:**
```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS prod
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD wget --spider -q http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

**Python:**
```dockerfile
FROM python:3.12-slim AS base
WORKDIR /app
RUN addgroup --system appgroup && adduser --system --group appuser

FROM base AS deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS prod
COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin
COPY . .
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD wget --spider -q http://localhost:8000/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Go:**
```dockerfile
FROM golang:1.22-alpine AS build
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/server ./cmd/server

FROM gcr.io/distroless/static-debian12 AS prod
COPY --from=build /app/server /server
USER 65532:65532
EXPOSE 8080
# distroless has no shell or wget — HEALTHCHECK requires the binary to expose a health endpoint.
# If your binary doesn't support a health flag, use HEALTHCHECK NONE and rely on k8s probes.
HEALTHCHECK NONE
CMD ["/server"]
```

For other languages: adapt the pattern — official base image, pinned version, multi-stage, non-root user, HEALTHCHECK.

---

### Dockerfile.dev (local dev)

`devops/working/containers/Dockerfile.dev`

**Node.js / TypeScript:**
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
EXPOSE 3000
CMD ["npx", "ts-node-dev", "--respawn", "--transpile-only", "src/index.ts"]
```

**Python:**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Go:**
```dockerfile
FROM golang:1.22-alpine
WORKDIR /app
RUN go install github.com/air-verse/air@latest
COPY go.mod go.sum ./
RUN go mod download
COPY . .
EXPOSE 8080
CMD ["air"]
```

---

### .dockerignore

`devops/working/containers/.dockerignore`

```
node_modules
.git
.env*
!.env.example
dist
build
*.log
.DS_Store
coverage
.nyc_output
__pycache__
*.pyc
.pytest_cache
tmp
```

---

### docker-compose.yml (local dev)

`devops/working/compose/docker-compose.yml`

Generate based on detected `stack.database` list. Include only detected services. Comment out undetected services rather than removing them (useful reference).

```yaml
version: '3.9'

services:
  app:
    build:
      context: ../../../
      dockerfile: devops/working/containers/Dockerfile.dev
    ports:
      # Adapt container port: 3000 (Node.js), 8000 (Python), 8080 (Go)
      - "${APP_PORT:-3000}:3000"
    volumes:
      - ../../../src:/app/src
    env_file:
      - ../../../.env.local
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  # Include if PostgreSQL detected:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME:-app_dev}
      POSTGRES_USER: ${DB_USER:-app}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-devpassword}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-app}"]
      interval: 5s
      timeout: 5s
      retries: 5

  # Include if Redis detected:
  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  # Include if MongoDB detected:
  # mongo:
  #   image: mongo:7
  #   ports:
  #     - "27017:27017"
  #   environment:
  #     MONGO_INITDB_DATABASE: app_dev

volumes:
  postgres_data:
```

---

### docker-compose.team.yml

`devops/working/compose/docker-compose.team.yml`

```yaml
version: '3.9'

# Team dev — extends local compose with stricter resource limits
# Mirrors staging more closely than local dev

services:
  app:
    extends:
      file: docker-compose.yml
      service: app
    environment:
      # Replace NODE_ENV with the language-appropriate env var:
      # Node.js: NODE_ENV=development | Python: FLASK_ENV=development / APP_ENV=development | Go: APP_ENV=development
      NODE_ENV: development
      LOG_LEVEL: debug
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'

  db:
    extends:
      file: docker-compose.yml
      service: db
    deploy:
      resources:
        limits:
          memory: 256M
```

---

### docker-compose.prod.yml (reference)

`devops/working/compose/docker-compose.prod.yml`

```yaml
version: '3.9'

# Production-like reference — not for direct deployment
# Use this as the source of truth for staging/prod environment config

services:
  app:
    image: ${IMAGE_NAME}:${IMAGE_TAG:-latest}
    restart: unless-stopped
    environment:
      NODE_ENV: production
      LOG_LEVEL: warn
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 256M
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

---

### devcontainer.json

`devops/working/devcontainer/.devcontainer/devcontainer.json`

```json
{
  "name": "App Dev Container",
  "dockerComposeFile": [
    "../../compose/docker-compose.yml",
    "docker-compose.devcontainer.yml"
  ],
  "service": "app",
  "workspaceFolder": "/app",
  "features": {
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },
  "postCreateCommand": "npm install",
  "forwardPorts": [3000],
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-azuretools.vscode-docker"
      ],
      "settings": {
        "editor.formatOnSave": true
      }
    }
  }
}
```

Adapt to the detected language:
- **Node.js/TypeScript:** `"postCreateCommand": "npm install"`, ports: `[3000]`, extensions: `["dbaeumer.vscode-eslint", "esbenp.prettier-vscode"]`
- **Python:** `"postCreateCommand": "pip install -r requirements.txt -r requirements-dev.txt"`, ports: `[8000]`, extensions: `["ms-python.python", "charliermarsh.ruff"]`
- **Go:** `"postCreateCommand": "go mod download"`, ports: `[8080]`, extensions: `["golang.go"]`

`devops/working/devcontainer/.devcontainer/docker-compose.devcontainer.yml`:

```yaml
version: '3.9'
services:
  app:
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

---

### Setup Scripts

`devops/working/scripts/setup-local.sh`:

```bash
#!/bin/bash
set -euo pipefail

echo "Setting up local dev environment..."

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "ERROR: Docker is required. Install from https://docs.docker.com/get-docker/"; exit 1; }

# Create .env.local if it doesn't exist
if [ ! -f .env.local ]; then
  if [ -f .env.example ]; then
    cp .env.example .env.local
    echo "Created .env.local from .env.example — update with your local values"
  else
    cat > .env.local << 'EOF'
# Local dev environment variables — gitignored
# Replace NODE_ENV with your language env var; replace APP_PORT with your app port (3000/Node, 8000/Python, 8080/Go)
NODE_ENV=development
APP_PORT=3000
DB_NAME=app_dev
DB_USER=app
DB_PASSWORD=devpassword
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379
EOF
    echo "Created .env.local — update with your local values"
  fi
fi

# Start services
echo "Starting services..."
docker compose -f devops/working/compose/docker-compose.yml up -d

# Wait for health
echo "Waiting for services to be healthy..."
sleep 3

echo ""
echo "Local dev environment ready."
echo "  App:   http://localhost:${APP_PORT:-3000}"
echo "  DB:    localhost:5432"
echo ""
echo "Run 'docker compose -f devops/working/compose/docker-compose.yml logs -f' to see logs."
```

`devops/working/scripts/setup-team.sh`:

```bash
#!/bin/bash
set -euo pipefail

echo "Setting up team dev environment..."

command -v docker >/dev/null 2>&1 || { echo "ERROR: Docker is required."; exit 1; }
command -v code >/dev/null 2>&1 || { echo "WARN: VS Code not found. Install from https://code.visualstudio.com/"; }

echo ""
echo "Team dev uses a VS Code Dev Container."
echo "To open:"
echo "  1. Open this repo in VS Code"
echo "  2. Install the 'Dev Containers' extension (ms-vscode-remote.remote-containers)"
echo "  3. Run: Cmd+Shift+P → 'Dev Containers: Reopen in Container'"
echo ""
echo "Or run the local dev setup first: ./devops/working/scripts/setup-local.sh"
```

---

## CI/CD Pipeline Generation

Generate ALL three CI platforms regardless of which was selected. Place each in its own subdirectory.

**Security tool injection:** Before generating each CI file, check `selected_tools` from `security-findings.json`. Include a step for each tool only if it appears in `selected_tools`. Rules:
- `trivy` in selected_tools → include Trivy image scan step in security-scan stage
- `semgrep` in selected_tools → include Semgrep SAST step in lint stage
- `codeql` in selected_tools → include CodeQL step in lint stage (GitHub Actions only)
- `dependabot` in selected_tools → generate `dependabot.yml` (GitHub Actions only)
- `gitleaks` in selected_tools → include Gitleaks step in lint stage
- `owasp-zap` in selected_tools → include ZAP scan step in dast stage (after deploy-staging)
- `snyk` in selected_tools → include Snyk scan step in security-scan stage

The gitleaks step references `devops/working/ci/security/.gitleaks.toml` — this file was generated by `devops-security`. It will exist when this skill runs.

---

### GitHub Actions

`devops/working/ci/github-actions/ci.yml` (compatible with `.github/workflows/ci.yml`):

```yaml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint:
    name: Lint + SAST
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Adapt setup to detected language:
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint

      - name: Semgrep SAST
        uses: semgrep/semgrep-action@v1
        with:
          config: auto

      - name: CodeQL Analysis
        uses: github/codeql-action/init@v3
        with:
          languages: javascript-typescript

      - name: Gitleaks secret scan
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  test:
    name: Test
    runs-on: ubuntu-latest
    needs: lint
    services:
      # Include services matching detected databases:
      db:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test
          POSTGRES_PASSWORD: testpass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test
        env:
          DATABASE_URL: postgresql://test:testpass@localhost:5432/test_db

  build:
    name: Build + Push Image
    runs-on: ubuntu-latest
    needs: test
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          file: devops/working/containers/Dockerfile
          push: ${{ github.event_name != 'pull_request' }}
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  security-scan:
    name: Security Scan (Trivy)
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name != 'pull_request'
    steps:
      - name: Trivy image scan
        uses: aquasecurity/trivy-action@0.20.0
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'table'
          exit-code: '1'
          severity: 'CRITICAL,HIGH'
          ignore-unfixed: true

  deploy-staging:
    name: Deploy → Staging
    runs-on: ubuntu-latest
    needs: security-scan
    if: github.ref == 'refs/heads/main'
    environment:
      name: staging
      url: https://staging.your-app.example.com
    steps:
      - uses: actions/checkout@v4
      # Replace with your cloud-specific deploy step:
      - name: Deploy to staging
        run: |
          echo "Deploying ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} to staging"
          # AWS ECS: aws ecs update-service --cluster staging --service app --force-new-deployment
          # GCP Cloud Run: gcloud run deploy app --image ... --region us-central1
          # K8s: kubectl set image deployment/app app=...

  dast-scan:
    name: DAST Scan (OWASP ZAP)
    runs-on: ubuntu-latest
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    steps:
      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.9.0
        with:
          target: 'https://staging.your-app.example.com'
          allow_issue_writing: false

  deploy-prod:
    name: Deploy → Production
    runs-on: ubuntu-latest
    needs: dast-scan
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://your-app.example.com
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: |
          echo "Deploying ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} to production"
          # Same deploy command as staging, targeting prod cluster/service
```

`devops/working/ci/github-actions/dependabot.yml` (compatible with `.github/dependabot.yml`):

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5

  - package-ecosystem: "docker"
    directory: "/devops/working/containers"
    schedule:
      interval: "weekly"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

Adapt `package-ecosystem` to detected language (pip for Python, gomod for Go, maven for Java).

---

### GitLab CI

`devops/working/ci/gitlab-ci/.gitlab-ci.yml`:

```yaml
stages:
  - lint
  - test
  - build
  - security-scan
  - deploy-staging
  - dast
  - deploy-prod

variables:
  IMAGE_NAME: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  DOCKER_BUILDKIT: "1"
  FF_USE_FASTZIP: "true"

.node-base: &node-base
  image: node:20-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/

lint:
  stage: lint
  <<: *node-base
  script:
    - npm ci
    - npm run lint
    - npx semgrep --config=auto --error .
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"

gitleaks:
  stage: lint
  image: zricethezav/gitleaks:latest
  script:
    - gitleaks detect --source . --config devops/working/ci/security/.gitleaks.toml

test:
  stage: test
  <<: *node-base
  services:
    - name: postgres:16-alpine
      alias: db
  variables:
    POSTGRES_DB: test_db
    POSTGRES_USER: test
    POSTGRES_PASSWORD: testpass
    DATABASE_URL: postgresql://test:testpass@db/test_db
  script:
    - npm ci
    - npm test
  coverage: '/Lines\s*:\s*(\d+\.?\d*)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - |
      docker build \
        -f devops/working/containers/Dockerfile \
        -t $IMAGE_NAME \
        --cache-from $CI_REGISTRY_IMAGE:latest \
        .
    - docker push $IMAGE_NAME
    - docker tag $IMAGE_NAME $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:latest

trivy-scan:
  stage: security-scan
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity CRITICAL,HIGH --ignore-unfixed $IMAGE_NAME
  only:
    - main

snyk-scan:
  stage: security-scan
  image: node:20-alpine
  script:
    - npm install -g snyk
    - snyk auth $SNYK_TOKEN
    - snyk test --severity-threshold=high
  only:
    - main
  allow_failure: true

deploy-staging:
  stage: deploy-staging
  environment:
    name: staging
    url: https://staging.your-app.example.com
  script:
    - echo "Deploy $IMAGE_NAME to staging"
    # Add your cloud-specific deploy command
  only:
    - main

zap-scan:
  stage: dast
  image: zaproxy/zap-stable
  script:
    - zap-baseline.py -t https://staging.your-app.example.com -r zap-report.html
  artifacts:
    paths:
      - zap-report.html
  only:
    - main
  allow_failure: true

deploy-prod:
  stage: deploy-prod
  environment:
    name: production
    url: https://your-app.example.com
  when: manual
  script:
    - echo "Deploy $IMAGE_NAME to production"
    # Add your cloud-specific deploy command
  only:
    - main
```

---

### CircleCI

`devops/working/ci/circleci/.circleci/config.yml`:

```yaml
version: 2.1

orbs:
  node: circleci/node@5
  docker: circleci/docker@2
  snyk: snyk/snyk@1

executors:
  node-executor:
    docker:
      - image: cimg/node:20.0

jobs:
  lint:
    executor: node-executor
    steps:
      - checkout
      - node/install-packages
      - run: npm run lint
      - run:
          name: Semgrep SAST
          command: |
            pip install semgrep
            semgrep --config=auto --error .
      - run:
          name: Gitleaks
          command: |
            curl -sSfL https://github.com/gitleaks/gitleaks/releases/download/v8.18.2/gitleaks_8.18.2_linux_x64.tar.gz | tar -xz
            ./gitleaks detect --source . --config devops/working/ci/security/.gitleaks.toml

  test:
    docker:
      - image: cimg/node:20.0
      - image: cimg/postgres:16.0
        environment:
          POSTGRES_DB: test_db
          POSTGRES_USER: test
          POSTGRES_PASSWORD: testpass
    steps:
      - checkout
      - node/install-packages
      - run:
          name: Wait for DB
          command: dockerize -wait tcp://localhost:5432 -timeout 1m
      - run:
          name: Run tests
          command: npm test
          environment:
            DATABASE_URL: postgresql://test:testpass@localhost:5432/test_db

  build-push:
    docker:
      - image: cimg/base:2024.01
    steps:
      - checkout
      - setup_remote_docker:
          docker_layer_caching: true
      - docker/check
      - docker/build:
          dockerfile: devops/working/containers/Dockerfile
          image: $DOCKER_IMAGE
          tag: $CIRCLE_SHA1
      - docker/push:
          image: $DOCKER_IMAGE
          tag: $CIRCLE_SHA1

  trivy-scan:
    docker:
      - image: aquasec/trivy:latest
    steps:
      - run:
          name: Trivy scan
          command: trivy image --exit-code 1 --severity CRITICAL,HIGH $DOCKER_IMAGE:$CIRCLE_SHA1

  snyk-scan:
    executor: node-executor
    steps:
      - checkout
      - snyk/scan:
          severity-threshold: high
          fail-on-issues: true

  deploy-staging:
    docker:
      - image: cimg/base:2024.01
    steps:
      - run: echo "Deploy $DOCKER_IMAGE:$CIRCLE_SHA1 to staging"

  deploy-prod:
    docker:
      - image: cimg/base:2024.01
    steps:
      - run: echo "Deploy $DOCKER_IMAGE:$CIRCLE_SHA1 to production"

workflows:
  ci-cd:
    jobs:
      - lint
      - test:
          requires: [lint]
      - build-push:
          requires: [test]
      - trivy-scan:
          requires: [build-push]
          filters:
            branches:
              only: main
      - snyk-scan:
          requires: [build-push]
          filters:
            branches:
              only: main
      - deploy-staging:
          requires: [trivy-scan, snyk-scan]
          filters:
            branches:
              only: main
      - deploy-prod:
          requires: [deploy-staging]
          type: approval
          filters:
            branches:
              only: main
```

---

## Kubernetes Manifests (conditional)

Only generate if `choices.deployment_target` is "Kubernetes".

`devops/working/k8s/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: app
    version: "1.0.0"
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
        - name: app
          image: IMAGE_NAME:IMAGE_TAG
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 3000
          envFrom:
            - secretRef:
                name: app-secrets
            - configMapRef:
                name: app-config
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
            failureThreshold: 3
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 15
            periodSeconds: 20
            failureThreshold: 3
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: [ALL]
      imagePullSecrets:
        - name: registry-credentials
```

`devops/working/k8s/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  selector:
    app: app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: ClusterIP
```

`devops/working/k8s/ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app
                port:
                  number: 80
```

`devops/working/k8s/configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  NODE_ENV: "production"
  LOG_LEVEL: "warn"
  PORT: "3000"
```

---

## Terraform (conditional)

Only generate if `choices.cloud_provider` is AWS, GCP, or Azure AND `choices.deployment_target` is Containers, Kubernetes, or Serverless.

**AWS ECS example** (`devops/working/infra/terraform/main.tf`):

```hcl
terraform {
  required_version = ">= 1.7.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "your-terraform-state-bucket"
    key    = "app/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_ecs_cluster" "main" {
  name = "${var.app_name}-${var.environment}"
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "app" {
  family                   = "${var.app_name}-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([{
    name  = var.app_name
    image = "${var.ecr_repository_url}:${var.image_tag}"
    portMappings = [{
      containerPort = var.app_port
      protocol      = "tcp"
    }]
    environment = []
    secrets = [{
      name      = "DATABASE_URL"
      valueFrom = "arn:aws:secretsmanager:${var.aws_region}:${data.aws_caller_identity.current.account_id}:secret:${var.app_name}-db-url"
    }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/${var.app_name}"
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "ecs"
      }
    }
  }])
}

resource "aws_iam_role" "ecs_execution" {
  name = "${var.app_name}-ecs-execution-${var.environment}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
  ]
}

resource "aws_iam_role" "ecs_task" {
  name = "${var.app_name}-ecs-task-${var.environment}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

data "aws_caller_identity" "current" {}
```

`devops/working/infra/terraform/variables.tf`:

```hcl
variable "app_name" {
  type        = string
  description = "Application name (used for resource naming)"
}

variable "environment" {
  type        = string
  description = "Environment: dev, staging, prod"
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "ecr_repository_url" {
  type        = string
  description = "ECR repository URL (without tag)"
}

variable "image_tag" {
  type        = string
  description = "Docker image tag to deploy"
}

variable "app_port" {
  type    = number
  default = 3000
}

variable "task_cpu" {
  type    = string
  default = "256"
}

variable "task_memory" {
  type    = string
  default = "512"
}
```

`devops/working/infra/environments/dev.tfvars`:
```hcl
app_name    = "your-app-dev"
environment = "dev"
aws_region  = "us-east-1"
image_tag   = "latest"
task_cpu    = "256"
task_memory = "512"
```

`devops/working/infra/environments/staging.tfvars`:
```hcl
app_name    = "your-app-staging"
environment = "staging"
aws_region  = "us-east-1"
task_cpu    = "512"
task_memory = "1024"
```

`devops/working/infra/environments/prod.tfvars`:
```hcl
app_name    = "your-app-prod"
environment = "prod"
aws_region  = "us-east-1"
task_cpu    = "1024"
task_memory = "2048"
```

**GCP Cloud Run stub** (use when `choices.cloud_provider` is "GCP"):

`devops/working/infra/terraform/main.tf`:

```hcl
terraform {
  required_version = ">= 1.7.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

resource "google_cloud_run_v2_service" "app" {
  name     = var.app_name
  location = var.gcp_region

  template {
    containers {
      image = "${var.image_repository}:${var.image_tag}"
      ports { container_port = var.app_port }
      resources {
        limits = {
          memory = "512Mi"
          cpu    = "1"
        }
      }
    }
    service_account = google_service_account.app.email
  }
}

resource "google_service_account" "app" {
  account_id   = "${var.app_name}-sa"
  display_name = "${var.app_name} service account"
}
```

`devops/working/infra/terraform/variables.tf`:

```hcl
variable "app_name" {
  type        = string
  description = "Application name"
}

variable "environment" {
  type        = string
  description = "Environment: dev, staging, prod"
}

variable "gcp_project" {
  type        = string
  description = "GCP project ID"
}

variable "gcp_region" {
  type    = string
  default = "us-central1"
}

variable "image_repository" {
  type        = string
  description = "Container image repository URL (without tag)"
}

variable "image_tag" {
  type        = string
  description = "Docker image tag to deploy"
}

variable "app_port" {
  type    = number
  default = 8080
}
```

`devops/working/infra/environments/dev.tfvars`:
```hcl
app_name    = "your-app-dev"
environment = "dev"
gcp_region  = "us-central1"
image_tag   = "latest"
```

`devops/working/infra/environments/staging.tfvars`:
```hcl
app_name    = "your-app-staging"
environment = "staging"
gcp_region  = "us-central1"
```

`devops/working/infra/environments/prod.tfvars`:
```hcl
app_name    = "your-app-prod"
environment = "prod"
gcp_region  = "us-central1"
```

**Azure Container Apps stub** (use when `choices.cloud_provider` is "Azure"):

`devops/working/infra/terraform/main.tf`:

```hcl
terraform {
  required_version = ">= 1.7.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = "${var.app_name}-${var.environment}"
  location = var.azure_location
}

resource "azurerm_container_app" "app" {
  name                         = var.app_name
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  ingress {
    external_enabled = true
    target_port      = var.app_port
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  template {
    container {
      name   = var.app_name
      image  = "${var.image_repository}:${var.image_tag}"
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }
}

resource "azurerm_log_analytics_workspace" "main" {
  name                = "${var.app_name}-logs"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "main" {
  name                       = "${var.app_name}-env"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
}
```

`devops/working/infra/terraform/variables.tf`:

```hcl
variable "app_name" {
  type        = string
  description = "Application name"
}

variable "environment" {
  type        = string
  description = "Environment: dev, staging, prod"
}

variable "azure_location" {
  type    = string
  default = "East US"
}

variable "image_repository" {
  type        = string
  description = "Container image repository URL (without tag)"
}

variable "image_tag" {
  type        = string
  description = "Docker image tag to deploy"
}

variable "app_port" {
  type    = number
  default = 3000
}
```

`devops/working/infra/environments/dev.tfvars`:
```hcl
app_name       = "your-app-dev"
environment    = "dev"
azure_location = "East US"
image_tag      = "latest"
```

`devops/working/infra/environments/staging.tfvars`:
```hcl
app_name       = "your-app-staging"
environment    = "staging"
azure_location = "East US"
```

`devops/working/infra/environments/prod.tfvars`:
```hcl
app_name       = "your-app-prod"
environment    = "prod"
azure_location = "East US"
```

---

## Completion

After writing all files, tell the user:

```
Config generation complete. Files written to devops/working/.

Generated:
  ✓ containers/Dockerfile (production, multi-stage)
  ✓ containers/Dockerfile.dev (dev with hot-reload)
  ✓ containers/.dockerignore
  ✓ compose/docker-compose.yml (local dev)
  ✓ compose/docker-compose.team.yml (team dev)
  ✓ compose/docker-compose.prod.yml (prod reference)
  ✓ devcontainer/.devcontainer/devcontainer.json
  ✓ ci/github-actions/ci.yml
  ✓ ci/gitlab-ci/.gitlab-ci.yml
  ✓ ci/circleci/.circleci/config.yml
  ✓ scripts/setup-local.sh
  ✓ scripts/setup-team.sh
  [✓ k8s/ — 4 manifests] (if Kubernetes selected)
  [✓ infra/terraform/ — main.tf, variables.tf, 3 env files] (if cloud infra selected)
```
