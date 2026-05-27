---
name: sf-integration
description: Salesforce integration architecture (Brite edition) with 120-point scoring. TRIGGER when user sets up Named Credentials, External Services, REST/SOAP callouts, Platform Events, CDC, touches namedCredential-meta.xml files, works in brite-salesforce, asks about NC PLACEHOLDER URL strategy, the namedCredentials .forceignore exclusion (BC-5609 lesson), Queueable silent-retry diagnostic, Email Bison → OutboundSync sync path, Brite_Base REST integration, or ECA replacement for Connected Apps post-Spring '26. DO NOT TRIGGER when Connected App/OAuth config (use sf-connected-apps), Apex-only logic (use sf-apex), or data import/export (use sf-data).
user-invocable: false
license: MIT
metadata:
  version: "1.2.0-brite.1"
  author: "Jag Valaiyapathy (upstream); Brite Company (customization)"
  upstream: "Jaganpro/sf-skills@ff1ab74"
  scoring: "120 points across 6 categories"
---

<!-- Adapted from Jaganpro/sf-skills@ff1ab74 (MIT). This file layers Brite conventions from brite-salesforce/CLAUDE.md §Engineering Standards (line 45) + §Apex & Automation (lines 182-184) + §External Client Apps (lines 148-152) + namedCredentials/Slack_Webform_Alerts. -->

# sf-integration: Salesforce Integration Patterns Expert (Brite edition)

Use this skill when the user needs **integration architecture and runtime plumbing**: Named Credentials, External Credentials, External Services, REST/SOAP callout patterns, Platform Events, CDC, and event-driven integration design.

## Brite Context

- **Named Credentials are mandatory for outbound callouts** — see Rule 1.
- **NC URLs are PLACEHOLDER per-org** — see Rules 2 and 3 (`Slack_Webform_Alerts` is the canonical example; BC-5609 is the regression).
- **Queueable silent-retry = NC misconfig signature** — see Rule 4.
- **ECAs replace Connected Apps post-Spring '26** — see Rule 7 + sibling [sf-connected-apps](../sf-connected-apps/SKILL.md).

**See also:** [sf-connected-apps](../sf-connected-apps/SKILL.md) for ECA OAuth lifecycle; [sf-apex](../sf-apex/SKILL.md) for the Queueable silent-retry diagnostic in code; [sf-data](../sf-data/SKILL.md) for the Email Bison → OutboundSync → Task data shape; [sf-deploy](../sf-deploy/SKILL.md) for safe NC redeploy sequencing (commenting out `.forceignore` exclusions).

## Brite Integration Discipline

### 1. Named Credentials are mandatory for outbound callouts

No hardcoded endpoints or credentials in Apex, Flow XML, LWC, or anywhere else in source. Auth via External Credentials where supported (newer pattern); legacy NCs still acceptable. Source: §Engineering Standards line 45.

### 2. Source-controlled NC URLs are PLACEHOLDER, not real

Every NC `url` element in `force-app/main/default/namedCredentials/*.namedCredential-meta.xml` carries a placeholder. After deploying a NEW NC or redeploying NC shape changes, manually update the URL in **each** org via Setup → Named Credentials → Edit. Current Brite-active NC requiring per-org URL config: `Slack_Webform_Alerts`. Source: §Apex & Automation line 183.

### 3. `.forceignore` exclusion for NCs is non-negotiable

`namedCredentials/*.namedCredential-meta.xml` lives in `.forceignore` precisely because ongoing `sf project deploy start --source-dir force-app/` runs would silently re-push PLACEHOLDER over the working URL. To deploy a NEW NC or redeploy NC shape changes, **temporarily** comment out the `.forceignore` line, deploy, then restore (same pattern as ConnectedApp/ECA/Prompt/ListView exclusions). BC-5609 post-ship regression: pre-`.forceignore`, Slack callouts failed with the classic 1-original + 3-silent-retry pattern. Source: §Apex & Automation line 183.

### 4. Queueable silent-retry = NC misconfig signature

N consecutive `Completed` Apex jobs for the same class = 1 original + (N-1) silent retries. Jobs show `Completed` because the exception is caught — the diagnostic surface is the duplicate-Completed pattern in the Apex Jobs list, not a Failed status. **Always check the Named Credential endpoint first** when this signature appears (`Slack_Webform_Alerts` → `SlackWebformAlertJob` is the canonical example). See [sf-debug](../sf-debug/SKILL.md) for the full diagnostic walk-through. Source: §Apex & Automation line 182.

### 5. OutboundSync is the canonical Email Bison → Salesforce sync path

Email Bison sends webhook events to OutboundSync, which writes Contact updates and reply events into Salesforce. Skills do **not** subscribe Email Bison webhooks directly. When asked "how do I sync sequence replies into SF?", route to OutboundSync — not direct webhook handlers in Apex. (Architectural decision; OutboundSync is a separate Brite service, deployed outside `brite-salesforce`.)

### 6. Brite_Base REST integration: SF is read-only status mirror

Brite_Base sends WorkOrder/ServiceAppointment status updates to Salesforce via REST. Salesforce does not write back; updates flow only Brite_Base → SF. When designing new WO/SA-related automation, confirm whether the change belongs in Brite_Base (source of truth) or in SF (mirror) before writing Apex.

### 7. ECAs replace Connected Apps post-Spring '26

New auth integrations use `ExternalClientApplication` metadata, NOT `ConnectedApp`. ECA OAuth settings split across up to 4 metadata types; the org-local `oauthLink` makes `ExtlClntAppOauthSettings` non-portable cross-org. JWT-from-ECA + `sf org create scratch` is broken (CLI bugs forcedotcom/cli#3025, #3482) — workaround: `SFDX_AUTH_URL` via the CLI's built-in `PlatformCLI` Connected App. See [sf-connected-apps](../sf-connected-apps/SKILL.md) for the 4-active-ECA inventory and full OAuth lifecycle. Source: §External Client Apps lines 148-152.

## When This Skill Owns the Task

Use `sf-integration` when the work involves:
- `.namedCredential-meta.xml` or External Credential metadata
- outbound REST/SOAP callouts
- External Service registration from OpenAPI specs
- Platform Events, CDC, and event-driven architecture
- choosing sync vs async integration patterns

Delegate elsewhere when the user is:
- configuring the OAuth app itself → [sf-connected-apps](../sf-connected-apps/SKILL.md)
- writing Apex-only business logic → [sf-apex](../sf-apex/SKILL.md)
- deploying metadata → [sf-deploy](../sf-deploy/SKILL.md)
- importing/exporting data → [sf-data](../sf-data/SKILL.md)

---

## Required Context to Gather First

Ask for or infer:
- integration style: outbound callout, inbound event, External Service, CDC, platform event
- auth method
- sync vs async requirement
- system endpoint / spec details
- rate limits, retry expectations, and failure tolerance
- whether this is net-new design or repair of an existing integration

---

## Recommended Workflow

### 1. Choose the integration pattern
| Need | Default pattern |
|---|---|
| authenticated outbound API call | Named Credential / External Credential + Apex or Flow |
| spec-driven API client | External Service |
| trigger-originated callout | async callout pattern |
| decoupled event publishing | Platform Events |
| change-stream consumption | CDC |

### 2. Choose the auth model
Prefer secure runtime-managed auth:
- Named Credentials / External Credentials
- OAuth or JWT via the right credential model
- no hardcoded secrets in code

### 3. Generate from the right templates
Use the provided assets under:
- `assets/named-credentials/`
- `assets/external-credentials/`
- `assets/external-services/`
- `assets/callouts/`
- `assets/platform-events/`
- `assets/cdc/`
- `assets/soap/`

### 4. Validate operational safety
Check:
- timeout and retry handling
- async strategy for trigger-originated work
- logging / observability
- event retention and subscriber implications

### 5. Hand off deployment or implementation details
Use:
- [sf-deploy](../sf-deploy/SKILL.md) for deployment
- [sf-apex](../sf-apex/SKILL.md) for deeper service / retry code
- [sf-flow](../sf-flow/SKILL.md) for declarative HTTP callout orchestration

---

## High-Signal Rules

- never hardcode credentials
- do not do synchronous callouts from triggers
- define timeout behavior explicitly
- plan retries for transient failures
- use middleware / event-driven patterns when outbound volume is high
- prefer External Credentials architecture for new development when supported

Common anti-patterns:
- sync trigger callouts
- no retry or dead-letter strategy
- no request/response logging
- mixing auth setup responsibilities with runtime integration design

---

## Output Format

When finishing, report in this order:
1. **Integration pattern chosen**
2. **Auth model chosen**
3. **Files created or updated**
4. **Operational safeguards**
5. **Deployment / testing next step**

Suggested shape:

```text
Integration: <summary>
Pattern: <named credential / external service / event / cdc / callout>
Files: <paths>
Safety: <timeouts, retries, async, logging>
Next step: <deploy, register, test, or implement>
```

---

## Cross-Skill Integration

| Need | Delegate to | Reason |
|---|---|---|
| OAuth app setup | [sf-connected-apps](../sf-connected-apps/SKILL.md) | consumer key / cert / app config |
| advanced callout service code | [sf-apex](../sf-apex/SKILL.md) | Apex implementation |
| declarative HTTP callout / Flow wrapper | [sf-flow](../sf-flow/SKILL.md) | Flow orchestration |
| deploy integration metadata | [sf-deploy](../sf-deploy/SKILL.md) | validation and rollout |
| use integration from Agentforce | [sf-ai-agentscript](../sf-ai-agentscript/SKILL.md) | agent action composition |

---

## Reference Map

### Start here
- [references/named-credentials-guide.md](references/named-credentials-guide.md)
- [references/external-services-guide.md](references/external-services-guide.md)
- [references/callout-patterns.md](references/callout-patterns.md)
- [references/security-best-practices.md](references/security-best-practices.md)

### Event-driven / platform patterns
- [references/event-patterns.md](references/event-patterns.md)
- [references/platform-events-guide.md](references/platform-events-guide.md)
- [references/cdc-guide.md](references/cdc-guide.md)
- [references/event-driven-architecture-guide.md](references/event-driven-architecture-guide.md)
- [references/messaging-api-v2.md](references/messaging-api-v2.md)

### CLI / automation / scoring
- [references/cli-reference.md](references/cli-reference.md)
- [references/named-credentials-automation.md](references/named-credentials-automation.md)
- [references/scoring-rubric.md](references/scoring-rubric.md)
- [assets/](assets/)

---

## Score Guide

| Score | Meaning |
|---|---|
| 108+ | strong production-ready integration design |
| 90–107 | good design with some hardening left |
| 72–89 | workable but needs architectural review |
| < 72 | unsafe / incomplete for deployment |
