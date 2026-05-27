---
name: sf-connected-apps
description: Salesforce Connected Apps and OAuth configuration with 120-point scoring. TRIGGER when: user configures OAuth flows, JWT bearer auth, Connected Apps, or touches .connectedApp-meta.xml / .eca-meta.xml files. DO NOT TRIGGER when: Named Credentials for callouts (use sf-integration), permission policies (use sf-permissions), or API endpoint code (use sf-apex).
user-invocable: false
license: MIT
allowed-tools: Bash Read Write Edit Glob Grep WebFetch AskUserQuestion TodoWrite
metadata:
  version: "1.1.0-brite.2"
  author: "Jag Valaiyapathy (upstream); Brite Company (customization)"
  upstream: "Jaganpro/sf-skills@ff1ab74"
  scoring: "120 points across 6 categories"
---

<!-- Adapted from Jaganpro/sf-skills@ff1ab74 (MIT). This file layers Brite conventions from brite-salesforce/CLAUDE.md. -->

# sf-connected-apps: Salesforce Connected Apps & External Client Apps

Use this skill when the user needs **OAuth app configuration** in Salesforce: Connected Apps, External Client Apps (ECAs), JWT bearer setup, PKCE decisions, scope design, or migration from older Connected App patterns to newer ECA patterns.

## Brite Context

Brite's integration auth landscape sits mid-migration. Spring '26 disabled org-wide creation of classic Connected Apps (SF Support re-enable required — treated as temporary migration runway), so every net-new OAuth app must be an `ExternalClientApplication`. Current inventory:

- **`Marketing_Claude_MCP`** — **Brite's first pure ECA**, provisioned post-Spring-'26 per BC-5579. Plugin-side MCP runtime access. JWT bearer. Scopes `Api` + `RefreshToken`. `refreshTokenPolicy: zero`. Private key in the Engineering Bitwarden collection.
- **`Outbound_Sales_Ops`** — live runtime integration writing CF-owned fields on Lead/Contact. **Legacy ConnectedApp auto-wrapped with an ECA settings file during the Spring '26 migration** — NOT a pure ECA. Parent `.connectedApp-meta.xml` + wrapper `.eca-meta.xml`. JWT bearer. `isAdminApproved=true`, `refreshTokenPolicy=zero`, `ipRelaxation=ENFORCE`.
- **`CI_Deploy`** — ECA committed but **inactive** ("compliance-posture-only"). CI does NOT use this app. GitHub Actions deploys authenticate via `SFDX_AUTH_URL` under Salesforce's built-in `PlatformCLI` Connected App.
- **`OutboundSync`** — separate sync path.

Credential home: Engineering Bitwarden collection. Naming convention and binding rule in Convention 7.

**See also:** `brite-salesforce/CLAUDE.md` §External Client Apps, `docs/research/salesforce-mcp-findings.md` Q3 + Appendix B.1, and memory `gotcha_spring26_ca_blocked`.

## Brite ECA Conventions

These rules bind any sf-connected-apps work done in a Brite repo. Violations block PR review.

1. **Use `ExternalClientApplication` for new OAuth apps.** Classic `ConnectedApp` creation is disabled org-wide since Spring '26. Even for a simple single-org app, use the ECA metadata type. The upstream "First Decision" table below still lists Connected App as preferred for some cases — treat those rows as upstream reference only; at Brite the answer is always ECA.

2. **JWT-via-SFDX-CLI flow requires BOTH `Api` and `RefreshToken` scopes.** The `sf org login jwt` command persists auth records in `~/.sfdx/` and needs `RefreshToken` for that persistence — drop it and JWT exchange fails with "refresh_token scope is required." Pure JWT exchange at a non-CLI runtime (e.g. a Python MCP calling the token endpoint directly) does NOT require `RefreshToken` — apply the scope requirement where SFDX handles the handshake, not universally. Source: `docs/research/salesforce-mcp-findings.md` Q3 lines 50-52.

3. **Set `refreshTokenPolicy: zero` on ECA OAuth policies (lowercase `zero`).** The Salesforce XML enum is lowercase — see `assets/connected-app-jwt.xml` and the `infinite | zero | specific_lifetime` enumeration in `assets/eca-policies.xml`. Uppercase `ZERO` will not validate. Belt-and-suspenders against long-lived refresh tokens even when clients mis-request them; default for new ECAs unless a flow documents a specific persistence need in its PR.

4. **Exclude `ExtlClntAppOauthSettings` via `.forceignore` for sandbox deploys.** The file embeds an org-specific `oauthLink` (`OrgId:ConsumerRecordId`) that does not resolve cross-org. Excluded alongside the `ExternalClientApplication` type for sandbox work; temporarily comment the exclusions out before running a production deploy, then re-enable. The canonical toggle procedure lives in [sf-deploy](../sf-deploy/SKILL.md).

5. **JWT-from-ECA breaks `sf org create scratch`.** Upstream bugs: `forcedotcom/cli#3025`, `forcedotcom/cli#3482`. Scratch-org creation rejects JWT sessions authenticated against ECAs. Workaround: authenticate via `SFDX_AUTH_URL` through the CLI's built-in `PlatformCLI` Connected App for scratch-org provisioning. Runtime MCP calls are unaffected.

6. **CI auth is `SFDX_AUTH_URL` via built-in `PlatformCLI` — not `CI_Deploy`.** The `CI_Deploy` ECA in source is compliance-posture-only (committed but inactive). GitHub Actions deploys authenticate via an `SFDX_AUTH_URL` secret loaded into the CLI's built-in `PlatformCLI` Connected App. Runtime MCP access goes through JWT against `Marketing_Claude_MCP`. Don't repurpose `CI_Deploy` without explicit ADR approval — the blast-radius story depends on the CI path and runtime path staying independent.

7. **All ECA secrets live in the Engineering Bitwarden collection, never in source.** JWT private keys and consumer secrets are stored with item names `<ECAName> — JWT private key` and `<ECAName> — consumer secret`. Per-user distribution is out-of-band. Never commit, never echo to logs, never put in env templates with real values.

## When This Skill Owns the Task

Use `sf-connected-apps` when the work involves:
- `.connectedApp-meta.xml` or `.eca-meta.xml` files
- OAuth flow selection and callback / scope setup
- JWT bearer auth, device flow, client credentials, or auth-code decisions
- Connected App vs External Client App architecture choices
- consumer-key / secret / certificate handling strategy

Delegate elsewhere when the user is:
- configuring Named Credentials or runtime callouts → [sf-integration](../sf-integration/SKILL.md)
- analyzing access / permission policy assignments → [sf-permissions](../sf-permissions/SKILL.md)
- writing Apex token-handling code → [sf-apex](../sf-apex/SKILL.md)
- deploying metadata to orgs → [sf-deploy](../sf-deploy/SKILL.md)

---

## First Decision: Connected App or External Client App

> **At Brite: always ECA.** See § Brite ECA Conventions rule 1. The table and default guidance below are upstream reference only — rows recommending Connected App do not apply in Brite repos because Spring '26 blocks new Connected App creation org-wide.

| If the need is... | Prefer |
|---|---|
| simple single-org OAuth app | Connected App |
| new development with better secret handling | External Client App |
| multi-org / packaging / stronger operational controls | External Client App |
| straightforward legacy compatibility | Connected App |

Default guidance:
- choose **ECA** for new regulated, packageable, or automation-heavy solutions
- choose **Connected App** when simplicity and legacy compatibility matter more
- Spring ’26 note: creation of new Connected Apps is disabled org-wide (SF Support re-enable required, treated as temporary migration runway). At Brite, always use ECA — see Brite ECA Conventions rule 1.

---

## Required Context to Gather First

Ask for or infer:
- app type: Connected App or ECA
- OAuth flow: auth code, PKCE, JWT bearer, device, client credentials
- client type: confidential vs public
- callback URLs / redirect surfaces
- required scopes
- distribution model: local org only vs packageable / multi-org
- whether certificates or secret rotation are required

---

## Recommended Workflow

### 1. Choose the app model
Decide whether a Connected App or ECA is the better long-term fit.

### 2. Choose the OAuth flow
| Use case | Default flow |
|---|---|
| backend web app | Authorization Code |
| SPA / mobile / public client | Authorization Code + PKCE |
| server-to-server / CI/CD | JWT Bearer |
| device / CLI auth | Device Flow |
| service account style app | Client Credentials (typically ECA) |

### 3. Start from the right template
Use the provided assets instead of building from scratch:
- `assets/connected-app-basic.xml`
- `assets/connected-app-oauth.xml`
- `assets/connected-app-jwt.xml`
- `assets/external-client-app.xml`
- `assets/eca-global-oauth.xml`
- `assets/eca-oauth-settings.xml`
- `assets/eca-policies.xml`

If you need source-controlled ECA OAuth security metadata, retrieve it from an org first and treat the retrieved file as the schema source of truth:
- `sf project retrieve start --metadata ExtlClntAppOauthSecuritySettings:<AppName> --target-org <alias>`

### 4. Apply security hardening
Favor:
- least-privilege scopes
- explicit callback URLs
- PKCE for public clients
- certificate-based auth where appropriate
- rotation-ready secret / key handling
- IP restrictions when realistic and maintainable

### 5. Validate deployment readiness
Before handoff, confirm:
- metadata file naming is correct
- scopes are justified
- callback and auth model match the real client type
- secrets are not embedded in source

---

## High-Signal Security Rules

Avoid these anti-patterns:

| Anti-pattern | Why it fails |
|---|---|
| wildcard / overly broad callback URLs | token interception risk |
| `Full` scope by default | unnecessary privilege |
| PKCE disabled for public clients | code interception risk |
| consumer secret committed to source | credential exposure |
| no rotation / cert strategy for automation | brittle long-term ops |

Default fix direction:
- narrow scopes
- constrain callbacks
- enable PKCE for public clients
- keep secrets outside version control
- use JWT certificates or controlled secret storage where appropriate

---

## Metadata Notes That Matter

### Connected App
Usually lives under:
- `force-app/main/default/connectedApps/`

### External Client App
Current source-supported ECA metadata uses multiple top-level source directories, not a single `externalClientApps/` folder:
- `force-app/main/default/externalClientApps/` → `ExternalClientApplication` (`.eca-meta.xml`)
- `force-app/main/default/extlClntAppGlobalOauthSets/` → `ExtlClntAppGlobalOauthSettings` (`.ecaGlblOauth-meta.xml`)
- `force-app/main/default/extlClntAppOauthSettings/` → `ExtlClntAppOauthSettings` (`.ecaOauth-meta.xml`)
- `force-app/main/default/extlClntAppOauthSecuritySettings/` → `ExtlClntAppOauthSecuritySettings` (`.ecaOauthSecurity-meta.xml`)
- `force-app/main/default/extlClntAppOauthPolicies/` → `ExtlClntAppOauthConfigurablePolicies` (`.ecaOauthPlcy-meta.xml`)
- `force-app/main/default/extlClntAppPolicies/` → `ExtlClntAppConfigurablePolicies` (`.ecaPlcy-meta.xml`)

Important file-name gotchas:
- the global OAuth suffix is `.ecaGlblOauth`, not `.ecaGlobalOauth`
- the general policy suffix is `.ecaPlcy`, not `.ecaPolicy`
- use `.ecaOauthSecurity` for `ExtlClntAppOauthSecuritySettings`

---

## Output Format

When finishing, report in this order:
1. **App type chosen**
2. **OAuth flow chosen**
3. **Files created or updated**
4. **Security decisions**
5. **Next deployment / testing step**

Suggested shape:

```text
App: <name>
Type: Connected App | External Client App
Flow: <oauth flow>
Files: <paths>
Security: <scopes, PKCE, certs, secrets, IP policy>
Next step: <deploy, retrieve consumer key, or test auth flow>
```

---

## Cross-Skill Integration

| Need | Delegate to | Reason |
|---|---|---|
| Named Credential / callout runtime config | [sf-integration](../sf-integration/SKILL.md) | runtime integration setup |
| deploy app metadata | [sf-deploy](../sf-deploy/SKILL.md) | org validation and deployment |
| Apex token or refresh handling | [sf-apex](../sf-apex/SKILL.md) | implementation logic |
| permission review after deployment | [sf-permissions](../sf-permissions/SKILL.md) | access governance |

---

## Reference Map

### Start here
- [references/oauth-flows-reference.md](references/oauth-flows-reference.md)
- [references/security-checklist.md](references/security-checklist.md)
- [references/testing-validation-guide.md](references/testing-validation-guide.md)

### Migration / examples
- [references/migration-guide.md](references/migration-guide.md)
- [references/example-usage.md](references/example-usage.md)
- [assets/](assets/)

---

## Score Guide

| Score | Meaning |
|---|---|
| 80+ | production-ready OAuth app config |
| 54–79 | workable but needs hardening review |
| < 54 | block deployment until fixed |
