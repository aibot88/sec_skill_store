---
name: pmcro-project-generator
description: >
  Generates a complete, production-ready PMCR-O Cognitive Architecture .NET 10 Aspire project
  as a downloadable ZIP file. The generated project follows the real PMCRO substrate pattern:
  Aspire AppHost, gRPC-internal / REST-external hybrid, Microsoft Agent Framework (MAF) phase
  services (Planner, Maker, Checker, Reflector, OrchestratorService, OrchestrationApi),
  MCP actuators with three pillars (Tools + Resources + Prompts), Central Package Management,
  Directory.Build.props/targets, SKILL.md per service, and SeedIntent injection.
  Use this skill whenever a user provides a CompanyName, ProjectName, and SeedIntent and wants
  to scaffold a full PMCRO project. Triggers on: "generate PMCRO project", "scaffold cognitive
  architecture", "new PMCRO project", "generate project zip", "dotnet new pmcro", or any
  combination of intent + project name implying a PMCRO scaffold is desired.
compatibility: .NET 10 | C# 14 | Aspire 13.x | MAF 1.0.0-rc2 | MCP 1.2.0 | gRPC | Docker
---

# PMCRO Cognitive Architecture Project Generator v2

Generates a **complete, production-ready** .NET 10 Aspire PMCRO project from three parameters.

## Input Contract

| Parameter | Example | Description |
|-----------|---------|-------------|
| `CompanyName` | `Tooensure` | PascalCase company — becomes namespace root + folder prefix |
| `ProjectName` | `CogArch` | PascalCase project — combined as `CompanyName.ProjectName` everywhere |
| `SeedIntent` | `"Develop PMCR-O Cognitive Architecture"` | Injected into InitFrame, TRAIN-000, SKILL.md files, Directory.Build.props |

If any are missing, ask before generating.

---

## Generation Workflow

1. Confirm all three parameters.
2. Run `scripts/generate_project.py --company X --name Y --intent Z --output /path/`
3. Script produces `CompanyName.ProjectName.zip`.
4. Present the ZIP via `present_files`.

```bash
python3 /path/to/pmcro-v2/scripts/generate_project.py \
  --company "CompanyName" \
  --name "ProjectName" \
  --intent "SeedIntent" \
  --output /mnt/user-data/outputs/
```

---

## What Gets Generated

See `references/project-structure.md` for the complete file tree.

### Architecture

```
External REST (HTTP)
      │
      ▼
OrchestrationApi (:8080)
      │
      │ gRPC (internal)
      ▼
OrchestratorService (:7075)
   │    │    │    │
   │    │    │    └─► ReflectorService (:7074)   [gRPC]
   │    │    └──────► CheckerService (:7073)     [gRPC]
   │    └───────────► MakerService (:7072)       [gRPC]
   └────────────────► PlannerService (:7071)     [gRPC]
                           │
                    MCP Actuators (HTTP)
                    ├── Mcp.FileSystem (:7221)
                    ├── Mcp.Playwright (:7273)
                    └── Mcp.Git       (:7222)
```

### Key Pillars

**Infrastructure:**
- `Directory.Build.props` — net10.0, C# latest, ArtifactsPath, SeedIntent MSBuild property
- `Directory.Build.targets` — SKILL.md → output copy + VerifyPmcroIdentity target
- `Directory.Packages.props` — Central Package Management (ALL versions, no Version= in csproj)
- `.template.config/template.json` — `dotnet new pmcro -company X -name Y -intent Z`

**AppHost (Aspire):**
- All services + MCPs registered with named endpoints
- WaitFor chains: phase agents wait for MCPs; Orchestrator waits for all phases; Api waits for Orchestrator
- `WithEnvironment("SeedIntent", ...)` injected into every service

**Phase Services (gRPC internal, MAF):**
- `CompanyName.ProjectName.Contracts` — shared `.proto` files + generated stubs
- `PlannerService`, `MakerService`, `CheckerService`, `ReflectorService` — each with SKILL.md + gRPC impl
- `OrchestratorService` — governs the loop, issues EXTEND/ACCEPT/ESCALATE/LOOP/INTERRUPT verdicts
- `OrchestrationApi` — sole external REST surface, minimal controller, maps to OrchestratorService gRPC

**MCP Actuators (3-pillar: Tools + Resources + Prompts):**
- `Mcp.FileSystem` — TYPE 1 write + TYPE 2 read, full `LocalFileSystemService`, path sandboxing
- `Mcp.Playwright` — browser automation, `snapshot_page`, `browser_click`, `browser_type`
- `Mcp.Git` — git read (TYPE 2) + write (TYPE 1) operations

**Shared Libraries:**
- `CompanyName.ProjectName.Core` — domain entities, EF DbContext, trail records
- `CompanyName.ProjectName.AI` — `SovereignInference`, `SovereignSkillsProvider`
- `CompanyName.ProjectName.ServiceDefaults` — OpenTelemetry, health checks, service discovery

---

## Laws (Never Violate)

- NEVER add `Version=` to any `<PackageReference>` — all versions in `Directory.Packages.props`
- NEVER hardcode CompanyName or ProjectName — template tokens replace everything
- NEVER add gRPC to an MCP project — MCPs are actuators, not phase agents
- NEVER add Microsoft.Agents.AI to an MCP project
- ALWAYS include SKILL.md in every project with `I AM` declaration
- ALWAYS use `WithToolsFromAssembly()` / `WithResourcesFromAssembly()` / `WithPromptsFromAssembly()`
- ALWAYS classify MCP tools as TYPE 1 (Orchestrator-only write) or TYPE 2 (any cognitive service read)
- ALWAYS use `Stateless = true` on HTTP MCP transport