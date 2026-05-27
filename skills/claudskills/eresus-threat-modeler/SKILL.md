---
name: eresus-threat-modeler
description: >
  Threat modeling skill for new features, services, endpoints, or repositories. Trigger when the user asks to:
  "threat model this", "analyze attack surface", "find abuse cases", "map trust boundaries", "prioritize security review",
  or wants a structured security design review before or alongside coding. Complements eresus-sast-scanner by turning architecture into a prioritized scan plan.
metadata:
  version: "1.0"
  domain: application-security
  mode: design-review
---

# Threat Modeling

## Purpose

Build a practical threat model that helps an AI agent focus security work on the highest-risk paths.
Use it before implementation, during feature review, or when deciding which vulnerability classes and
tests deserve the most attention.

## Core Questions

Always answer:

1. What assets matter here?
2. Who can interact with them?
3. Where does trust change?
4. How could an attacker abuse the feature?
5. Which controls must exist before release?

---

## Workflow

### Step 1: Define Scope

Clarify the target:

- single endpoint or workflow
- feature or service
- whole repository or subsystem

List the important assets: credentials, tokens, money movement, files, PII, admin actions, internal services, signed data, and audit logs.

### Step 2: Map Actors and Entry Points

Identify:

- anonymous users
- authenticated users
- admins/support/internal operators
- third-party systems and webhooks
- scheduled jobs, queues, and background workers

Then list the entry points they can influence: HTTP routes, message queues, uploads, config, headers, mobile deep links, admin tooling, and internal RPC calls.
Include serialized state channels such as cookies, session blobs, cache objects, queue payloads, and import/export formats.

### Step 3: Draw Trust Boundaries

Mark every boundary where data becomes more trusted or more powerful, for example:

- browser to server
- public API to internal service
- user tenant to shared resource
- webhook sender to processing pipeline
- app server to database, cache, filesystem, or cloud metadata service

### Step 4: Enumerate Abuse Cases

For each boundary, ask:

- Can identity be spoofed?
- Can an object/action be accessed without proper authorization?
- Can untrusted input reach code execution, queries, templates, files, or outbound network calls?
- Can untrusted input reach deserializers, object mappers, YAML/XML parsers, or state restore mechanisms?
- Can state transitions be raced, replayed, or skipped?
- Can the feature leak secrets, tokens, or cross-tenant data?
- Can cheap requests trigger expensive work?

### Step 5: Map Abuse Cases to Scan Priorities

Turn each abuse case into:

- likely vulnerability class
- likely source
- likely sink
- files/modules worth scanning first
- controls/tests that should exist

When `eresus-sast-scanner` is available, select the matching vulnerability knowledge files that should be loaded next.

### Step 6: Produce an Actionable Threat Model

End with a prioritized output the user can immediately use:

- top attack paths
- required preventative controls
- required detective controls or logging
- targeted SAST scan plan
- targeted test ideas

---

## Threat Modeling Guardrails

- Distinguish confirmed facts from assumptions.
- Do not treat a threat model as proof of exploitability; it is a prioritization tool.
- Do not focus only on injection bugs; include auth, logic, tenancy, workflow, and abuse-economics risks.
- Do not ignore internal systems; many critical bugs cross "trusted" service boundaries.
- Do not recommend vague controls. Name the precise guard, check, or invariant that should exist.

---

## Output Format

Use:

```markdown
# Threat Model — <scope>

## Assets
<flat list>

## Actors
<flat list>

## Trust Boundaries
<flat list>

## Priority Attack Paths
1. <attack path + impact>
2. <attack path + impact>
3. <attack path + impact>

## Required Controls
<flat list>

## Targeted SAST Plan
<which modules/files to scan and which vulnerability classes to prioritize>

## Test Ideas
<flat list>
```
