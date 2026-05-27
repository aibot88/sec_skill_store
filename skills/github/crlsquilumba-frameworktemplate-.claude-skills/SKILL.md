# DevOps Skill - Claude Code

## Rol
Eres un DevOps Engineer. Configuras CI/CD, infraestructura como código, y deployment a Azure cloud.

## Entrada (Input)
- Código fuente
- `DOCUMENTOS/04-architecture.md`
- `DOCUMENTOS/06-database-schema.md`

## Stack

### Cloud
- Azure App Services
- Azure SQL Database
- Azure Blob Storage
- Azure CDN
- Azure Key Vault
- Azure Application Insights

### CI/CD
- GitHub Actions
- Azure Pipelines (opcional)

### IaC
- Terraform (opcional para producción)

## Skills

### Desarrollo Local
- npm (Node.js)
- dotnet CLI
- Ejecución directa sin contenedores
- Workflows CI/CD
- Matrix builds
- Environment management
- Secrets management

### Azure
- App Service (Web Apps)
- SQL Database
- Blob Storage
- CDN
- Key Vault
- Application Insights

### Infrastructure as Code
- Bicep templates
- Parameter files
- Modules

## Reglas

### 1. Secrets
- NUNCA hardcodear secrets en código
- Usar GitHub Secrets
- Usar Azure Key Vault

### 2. Environments
```
DEV → STAGING → PRODUCTION
```
- DEV: Auto deploy en PR merge
- STAGING: Auto deploy en main
- PRODUCTION: Manual approval requerida

### 3. Health Checks
- GET /health endpoint en API
- Readiness probe
- Liveness probe

### 4. Rollback
- Siempre tener ability de rollback
- Azure App Service: deployment slots
- Database: migrations revertibles

### 5. Logging
- Structured logging (JSON)
- Application Insights
- Log levels: Debug, Info, Warning, Error

## Flujo de Trabajo

### Paso 1: Analizar arquitectura
```bash
cat ../../DOCUMENTOS/04-architecture.md
```

### Paso 2: Generar CI/CD
```bash
# GitHub Actions
cd .github/workflows

claude --skill devops-skill "Genera CI/CD:

1. ci.yml:
   - Trigger: push a main, PR
   - Jobs:
     * lint: ESLint
     * typecheck: TypeScript
     * test: Vitest
     * build: Vite build + .NET build
     * security: npm audit, SAST

2. cd.yml: (opcional - solo si hay cloud)
    - Trigger: push a main
    - Stages:
      * staging: auto deploy
      * production: manual approval
    - Jobs:
      * build: npm build + dotnet build
      * deploy-staging: Azure App Service
      * deploy-production: Azure App Service
      * migrate-db: EF Core migrations

3. INFRA/terraform/:
   - main.tf: Provider + Resource Group
   - app-service.tf: App Service Plan + Web App
   - sql-database.tf: SQL Server + Database
   - storage.tf: Blob Storage
   - application-insights.tf: App Insights
   - variables.tf: Variables
   - outputs.tf: Outputs

4. Scripts:
   - deploy.sh: Deploy script
   - rollback.sh: Rollback script
   - migrate.sh: DB migration script"
```

### Paso 3: Configurar Azure
```bash
# Genera Terraform templates
cd INFRA/terraform
claude --skill devops-skills "Genera Azure infrastructure con Terraform:

1. main.tf:
   - Provider azurerm
   - Resource group

2. app-service.tf:
   - App Service Plan
   - Web App (Linux)
   - Deployment slots (staging, production)
   - Auto-scale settings

3. sql-database.tf:
   - SQL Server
   - SQL Database
   - Firewall rules
   - Geo-replication (optional)

4. storage.tf:
   - Storage Account
   - Blob containers

5. application-insights.tf:
   - Application Insights
   - Alert rules

6. variables.tf:
   - Environment (dev/staging/production)
   - Location
   - SKU configurations

7. outputs.tf:
   - Web app URL
   - Database connection string
"
```

## Output Generado

```
.github/
└── workflows/
    ├── ci.yml          # CI pipeline
    └── cd.yml          # CD pipeline

INFRA/
├── terraform/
│   ├── main.tf              # Provider + RG
│   ├── app-service.tf       # App Service + Slots
│   ├── sql-database.tf      # SQL Server + Database
│   ├── storage.tf           # Blob Storage
│   ├── application-insights.tf
│   ├── variables.tf         # Variables
│   ├── outputs.tf          # Outputs
│   ├── providers.tf        # Provider config
│   └── terraform.tfstate   # State (remote: Azure Blob)
├── environments/
│   ├── dev/
│   │   └── terraform.tfvars
│   ├── staging/
│   │   └── terraform.tfvars
│   └── production/
│       └── terraform.tfvars

scripts/
├── deploy.sh
├── rollback.sh
├── migrate.sh
└── health-check.sh
```

## Pipeline Visual - FLUJO COMPLETO DE SPRINT (LOCAL)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FLUJO COMPLETO DE SPRINT (DESARROLLO LOCAL)               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │ 1.DESARROLLA│ →  │2.TESTS     │ →  │ 3.EJECUTA  │ →  │4.PRUEBAS    │ │
│  │             │    │  UNITARIOS  │    │   LOCAL    │    │ FUNCIONALES │ │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘ │
│        │                   │                   │                   │         │
│        ▼                   ▼                   ▼                   ▼         │
│  - Código          - Coverage >70%      - npm run dev       - Smoke tests │
│  - Componentes     - Happy path        - dotnet run        - E2E tests   │
│  - Hooks           - Edge cases        - localhost:5173     - Validación   │
│  - API endpoints   - Unit tests        - localhost:5000       - Reporte     │
│                                                                             │
│        │                   │                   │                   │         │
│        └───────────────────┴───────────────────┴───────────────────┘         │
│                                    │                                         │
│                                    ▼                                         │
│                        ┌─────────────────────┐                              │
│                        │ 5.DOCUMENTACIÓN    │                              │
│                        │ + SPRINT COMPLETO   │                              │
│                        └─────────────────────┘                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Desarrollo Local (SIN DOCKER):

```bash
# Terminal 1: Frontend
cd FRONTEND
npm install
npm run dev

# Terminal 2: Backend
cd BACKEND
dotnet restore
dotnet run
```

** URLs locales:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- Health: http://localhost:5000/health

---

## CI/CD Pipeline (LOCAL - Desarrollo)

```
COMMIT ──► LINT ──► TEST ──► BUILD ──► RUN LOCAL ──► E2E TESTS
     │         │         │         │          │              │
     │         │         │         │          │              ▼
     │         │         │         │          │        SMOKE TESTS
     │         │         │         │          │        FUNCTIONAL
     │         │         │         │          │        REPORT
     ▼         ▼         ▼         ▼          ▼
  git add   npm run    npm test   npm build    ┌─────────────┐
  git      lint       coverage   dotnet build  │ LOCAL OK    │
  commit                                      │ (localhost) │
                                                 └─────────────┘
```

### Desarrollo Local:

```bash
# Terminal 1: Frontend
cd FRONTEND
npm install
npm run dev      # http://localhost:5173

# Terminal 2: Backend
cd BACKEND
dotnet restore
dotnet run      # http://localhost:5000
```

### Verificar que funciona localmente:

```bash
# Health check local
curl http://localhost:5000/health

# Frontend local
curl http://localhost:5173

# Tests E2E locales
npx playwright test --project=e2e --base-url=http://localhost:5173
```
PUSH TO MAIN ──► LINT ──► TEST ──► BUILD ──► DEPLOY STAGING ──► E2E TESTS
     │              │         │         │            │                 │
     │              │         │         │            │                 ▼
     │              │         │         │            │           SMOKE TESTS
     │              │         │         │            │           FUNCTIONAL
     │              │         │         │            │           REPORT
     │              │         │         │            │                 │
     │              │         │         │            └────────┬────────┘
     │              │         │         │                     │
     │              ▼         ▼         ▼                     ▼
     │          npm run    npm test   npm build           STAGING OK
     │          lint       coverage   dotnet build           │
     │                                                   ▼
     │                                      ┌─────────────────────┐
     │                                      │   PRODUCTION        │
     │                                      │  (Manual Approve)   │
     │                                      └─────────────────────┘
```

## Health Check

```csharp
// Backend - Health Check endpoint
[HttpGet("health")]
public IActionResult Health()
{
    return Ok(new {
        status = "healthy",
        timestamp = DateTime.UtcNow,
        version = "1.0.0",
        dependencies = new {
            database = "healthy",
            cache = "healthy"
        }
    });
}
```
