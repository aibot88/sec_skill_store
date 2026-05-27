# Skill: Code Apps on the Power Platform

## What Are Power Apps Code Apps?

**Code Apps** are a feature of Microsoft Power Apps that let professional developers build enterprise web applications using standard front-end frameworks — **React, Angular, Vue, or any SPA** — and deploy them directly into the Power Platform as first-class Power Apps. The app runs inside the **Power Apps web player** (the Managed Host), inheriting enterprise capabilities like Entra ID authentication, role-based access control, governance, and connector-based data access — without writing any backend plumbing.

> **In short:** Write a modern web app with your favorite tools → deploy it to Power Apps → get identity, data connectors, ALM, and governance for free.

---

## Core Concepts

### 1. The Managed Host

When a Code App runs inside Power Apps, it is embedded in a **Managed Host**. The host provides:

| Capability | What it means |
|---|---|
| **Entra ID SSO** | Users are automatically authenticated via their Microsoft 365 / Entra ID identity — no auth code needed in your app. |
| **Connector Bridge** | Your front-end code can call 1,400+ Power Platform connectors (Dataverse, SharePoint, SQL, REST APIs, custom connectors) through a typed SDK. |
| **Session & Context** | The SDK injects runtime context: current user profile, app metadata, environment info, host session ID. |
| **Governance** | Data Loss Prevention (DLP) policies, environment security roles, and tenant-level controls apply automatically. |
| **ALM** | Code Apps are solution-aware — exportable, importable, and deployable across environments through managed/unmanaged solutions. |

### 2. The Power Apps SDK (`@microsoft/power-apps`)

The npm package `@microsoft/power-apps` is the bridge between your JavaScript/TypeScript code and the Power Platform runtime.

**Key API — `getContext()`**

```ts
import { getContext } from "@microsoft/power-apps/app";

const ctx = await getContext();

// Available context:
ctx.app.appId;          // The Power Apps app ID
ctx.user.fullName;      // Display name of the signed-in user
ctx.user.id;            // Entra Object ID
ctx.host.sessionId;     // Host session identifier
```

- **Inside the host** (deployed or `pac code run`): `getContext()` resolves with live context and enables connector access.
- **Outside the host** (plain `npm run dev`): `getContext()` will reject. Apps should catch this gracefully and fall back to mock data for local development.

### 3. The Vite Plugin (`@microsoft/power-apps-vite`)

The companion dev-dependency `@microsoft/power-apps-vite` provides a Vite plugin that:

- Injects the Power Apps host bootstrap script during development.
- Enables **Local Play** mode when the dev server is started via `pac code run`.
- Configures build output to match the shape the platform expects on `pac code push`.

```ts
// vite.config.ts
import { powerApps } from "@microsoft/power-apps-vite";

export default defineConfig({
  plugins: [react(), tailwindcss(), powerApps()],
});
```

### 4. `power.config.json`

Every Code App has a `power.config.json` at the project root. It ties the local project to a specific Power App registration.

```json
{
  "appId": "92519819-24d5-4a40-8adc-395a6107d090",
  "appDisplayName": "Approval Portal",
  "description": "Multi-step approval workflow portal",
  "environmentId": "Default-239ad743-5c7a-48d4-a28b-89854ee31af4",
  "buildPath": "dist",
  "buildEntryPoint": "index.html",
  "connectionReferences": {},
  "databaseReferences": {}
}
```

| Field | Purpose |
|---|---|
| `appId` | GUID of the registered Power App. |
| `environmentId` | Target Power Platform environment. |
| `buildPath` | Output folder from `vite build` (default: `dist`). |
| `buildEntryPoint` | The HTML entry point inside `buildPath`. |
| `connectionReferences` | Maps connector logical names to connection IDs (populated by `pac code add-data-source`). |
| `databaseReferences` | Maps Dataverse table logical names for typed service generation. |

---

## Developer Workflow

### Prerequisites

- **Node.js LTS** (v18+)
- **Power Platform CLI** (`pac`) — install via `winget install Microsoft.PowerPlatformCLI` or the VS Code extension.
- A Power Platform environment with Code Apps enabled.

### Step-by-step

```bash
# 1. Authenticate to your tenant
pac auth create

# 2. Select the target environment
pac env select --environment <environment-id>

# 3. Scaffold or initialize a code app
pac code init --displayname "My App"

# 4. Install dependencies & run locally
npm install
npm run dev           # plain Vite dev server (mock data, no host)
# — OR —
pac code run          # starts Vite + opens Local Play inside Power Apps host

# 5. Build and deploy
npm run build | pac code push
```

### Local Development Modes

| Mode | Command | Host Available | Connectors Work | Best For |
|---|---|---|---|---|
| **Standalone** | `npm run dev` | ❌ | ❌ | UI development with mock data |
| **Local Play** | `pac code run` | ✅ | ✅ | Full integration testing against live data |
| **Deployed** | `pac code push` | ✅ | ✅ | Production use inside Power Apps |

---

## Connecting to Data

Code Apps access data through **Power Platform connectors**, not direct API calls. This means your front-end never holds secrets or connection strings — the platform handles OAuth token exchange for every connector.

### Adding Dataverse Tables

```bash
pac code add-data-source -a dataverse -t <table-logical-name>
```

This generates a **typed TypeScript service** in `src/generated/services/` with CRUD methods (`.create()`, `.get()`, `.getAll()`, `.update()`, `.delete()`) that mirror the Dataverse Web API.

### Adding Other Connectors (e.g., Office 365 Users)

```bash
# Find your connection ID
pac connection list

# Add the connector
pac code add-data-source -a "shared_office365users" -c "<connectionId>"
```

A typed service is generated for the connector's operations:

```ts
import { Office365UsersService } from "@/generated/services/Office365UsersService";

const me = await Office365UsersService.MyProfile_V2(
  "id,displayName,jobTitle,userPrincipalName"
);
```

### Mock-First Development Pattern

A best practice for Code Apps is to **start with mock data** and swap to generated services when ready:

```
src/services/
  approval-service.ts   ← mock implementation for local dev
  user-service.ts       ← mock implementation for local dev
src/generated/services/
  ApprovalRequestsService.ts  ← auto-generated after `pac code add-data-source`
  Office365UsersService.ts    ← auto-generated
```

Both follow the same `{ data: T }` response shape, making the swap seamless.

---

## Project Architecture (Recommended)

```
my-code-app/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── ui/              # Base primitives (Button, Card, Dialog…)
│   │   ├── layout/          # App shell (Sidebar, Header)
│   │   └── domain/          # Business-specific components
│   ├── pages/               # Route-level views
│   ├── providers/
│   │   └── PowerProvider.tsx # SDK initialization wrapper
│   ├── services/            # Data access layer (mock or generated)
│   ├── store/               # Client state (Zustand, Redux, etc.)
│   ├── types/               # TypeScript domain models
│   ├── lib/                 # Utilities and helpers
│   ├── App.tsx              # Root component + routing
│   └── main.tsx             # Entry point
├── power.config.json        # Power Apps registration
├── package.json
├── vite.config.ts
└── tsconfig.json
```

### The PowerProvider Pattern

Wrap your app in a provider that calls `getContext()` on mount. This gracefully handles both hosted and standalone modes:

```tsx
export default function PowerProvider({ children }: { children: ReactNode }) {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    getContext()
      .then((ctx) => console.log("SDK ready", ctx.user.fullName))
      .catch(() => console.warn("Running outside host — using mock data"))
      .finally(() => setReady(true));
  }, []);

  if (!ready) return null;
  return <>{children}</>;
}
```

---

## Recommended Tech Stack

| Layer | Recommended | Notes |
|---|---|---|
| **Build Tool** | Vite | Required for `@microsoft/power-apps-vite` plugin |
| **Framework** | React 18+ | Also supports Angular, Vue, or vanilla JS |
| **Language** | TypeScript | Strongly recommended for generated service types |
| **Styling** | Tailwind CSS 4 | Utility-first; pairs well with shadcn/ui |
| **UI Primitives** | shadcn/ui + Radix | Accessible, composable, unstyled components |
| **State** | Zustand | Lightweight; great for medium-complexity apps |
| **Data Fetching** | TanStack React Query | Cache, refetch, and sync connector responses |
| **Routing** | React Router v6 | Standard client-side routing |

---

## Key CLI Commands

| Command | Description |
|---|---|
| `pac code init` | Scaffold a new Code App project |
| `pac code run` | Start local dev server with Power Apps host integration |
| `pac code push` | Build and deploy the app to Power Apps |
| `pac code add-data-source` | Add a connector or Dataverse table and generate typed services |
| `pac auth create` | Authenticate to a Power Platform tenant |
| `pac env select` | Switch the active Power Platform environment |
| `pac connection list` | List available connections in the environment |
| `pac solution export` | Export the app as part of a managed/unmanaged solution |

---

## What You Get for Free (vs. a Standalone SPA)

| Concern | Standalone SPA | Power Apps Code App |
|---|---|---|
| **Authentication** | You implement MSAL / Entra ID | Automatic Entra ID SSO |
| **Authorization** | Custom RBAC | Environment security roles + DLP |
| **API Secrets** | Backend or proxy required | Connector bridge — no secrets in client |
| **Connector Ecosystem** | Build each integration | 1,400+ connectors available |
| **Governance** | DIY | Tenant admin controls, DLP policies |
| **ALM / CI/CD** | Custom pipelines | Solution-aware, `pac` CLI for pipelines |
| **Hosting** | Azure Static Web Apps, etc. | Power Apps web player (managed) |

---

## When to Use Code Apps

✅ **Good fit:**
- Pro-dev teams that want React/Angular/Vue but need enterprise connectors and governance.
- Complex, multi-page LOB apps (approval workflows, dashboards, admin portals).
- Apps that must integrate deeply with Dataverse, SharePoint, or other M365 services.
- Organizations already invested in Power Platform wanting to extend with custom code.

⚠️ **Consider alternatives when:**
- The app is a simple form or CRUD — **Canvas Apps** may be faster.
- The app has no need for Power Platform connectors or governance — a standalone SPA suffices.
- You need server-side rendering (SSR) — Code Apps are client-side only.

---

## Resources

- [Power Apps Code Apps Documentation](https://learn.microsoft.com/en-us/power-apps/developer/code-apps/)
- [Connect to Data](https://learn.microsoft.com/en-us/power-apps/developer/code-apps/how-to/connect-to-data)
- [Connect to Dataverse](https://learn.microsoft.com/en-us/power-apps/developer/code-apps/how-to/connect-to-dataverse)
- [Power Platform CLI Reference](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/)
- [GitHub: PowerAppsCodeApps](https://github.com/microsoft/PowerAppsCodeApps)
