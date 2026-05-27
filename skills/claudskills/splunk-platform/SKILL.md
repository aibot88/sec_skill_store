---
name: splunk-platform
description: "Deep skill for Splunk development, administration, SDK/REST integrations, dashboards, UCC add-ons, ITSI automation, SPL2 authoring, and AI-facing tooling. Use for Splunk SDK, REST, jobs/export, SPL, dashboards, packaging, and MCP-backed analysis workflows."
metadata:
  author: kundeng
  version: "1.0.0"
---

# Splunk Platform

Use this as the default skill for Splunk work. It should answer most Splunk
framework-selection questions directly and send you to exactly one or two
reference files for implementation details.

Read only the references that match the task:

- `references/spl2-authoring.md` for writing SPL2 modules, searches, custom functions, types, views, and pipelines
- `references/python-sdk.md` for Python automation, `splunklib`, and result parsing
- `references/javascript-sdk.md` for Node/browser JS SDK work
- `references/rest-search-patterns.md` for raw REST, search jobs, and export patterns
- `references/itsi-implementation.md` for concrete ITSI entity integrations, HEC setup, service onboarding, correlation searches, and notable-event aggregation workflows
- `references/itsi-av-example.md` for a concrete end-to-end ITSI onboarding pattern using entity imports, service templates, and template-linked service imports
- `references/admin-searches.md` for read-only admin/discovery SPL
- `references/ucc-framework.md` for add-ons, modular inputs, setup pages, and alert actions
- `references/dashboard-development.md` for Dashboard Studio and Simple XML (framework selection)
- `references/dashboard-studio-v2-json.md` for Dashboard Studio v2 JSON definition syntax (tokens, tabs, drilldowns, inputs, conditional formatting, chain searches, event handlers)
- `references/mcp-integration.md` for agent-facing Splunk tool design
- `references/platform-admin.md` for install/upgrade/deployment automation
- `references/app-packaging.md` for AppInspect, packaging, and release hygiene

## Start Here

Classify the task before you write code:

1. **SPL2 authoring**: writing SPL2 modules, searches, custom functions, custom types, views, or Edge/Ingest pipelines.
2. **External automation**: Python or JS code talks to Splunk over REST/SDK.
3. **Search/discovery**: SPL inspects indexes, metadata, users, apps, and knowledge objects.
4. **App/add-on engineering**: packaged Splunk app, technical add-on, modular input, alert action, setup UI.
5. **Dashboards/UI**: Dashboard Studio JSON, Simple XML, or legacy SplunkJS/Web Framework.
6. **AI integration**: MCP server or other agent-facing tools over Splunk.
7. **Platform administration**: host deployment, upgrades, distributed topology, app rollout.
8. **ITSI implementation**: entities, services, KPI base searches, service templates, maintenance windows, or notable event aggregation policies.

If the task spans multiple areas, pick the primary deliverable first. A script
that queries Splunk is external automation, not an add-on.

If the user asks whether a Splunk analysis plan "maps to best practices", asks
for "Tier 0" or "Tier 1", or wants to normalize an analytics repo around
Splunk-backed exploration, answer from the perspective of a full analysis
workflow, not just Splunk infrastructure.

## Strong Defaults

- Prefer **Python** for automation, exports, CLIs, notebooks, and agent backends.
- Prefer **JavaScript SDK** only when the surrounding system is already Node/JS or you are in Splunk web-facing code.
- Prefer **raw REST** when you need streaming export semantics, exact endpoint control, or unsupported SDK behavior.
- Prefer **UCC** for new technical add-ons. Do not hand-roll setup pages and REST handlers unless you are maintaining an existing non-UCC app.
- Prefer **Dashboard Studio** for new dashboards.
- Prefer **Simple XML** only for legacy maintenance or when existing app behavior is tightly coupled to XML/tokens.
- Prefer **read-only SPL** for discovery and audits.
- Prefer **ITSI import/search workflows** for bulk entity or service creation before inventing unsupported direct KV-store writes.
- Prefer **narrow MCP tools** over one generic "run any SPL" endpoint.
- Prefer **official automation repos** for platform deployment before inventing custom shell glue.
- Run **AppInspect/package validation** before claiming an app or add-on is shippable.

## What Not To Use

- Do not build a Splunk app when the real need is an external export script.
- Do not use browser-side JS SDK code to hold long-lived credentials unless there is no server-side alternative.
- Do not default to `oneshot` for large searches.
- Do not expose unrestricted search execution to LLMs.
- Do not create new HTML dashboards or lean on deprecated web framework patterns for greenfield work.
- Do not use write-side SPL commands in automation unless the user explicitly wants state changes.
- Do not assume Splunk Cloud lets you use every REST/admin path that Splunk Enterprise does.
- Do not write directly to ITSI KV store collections; use ITSI REST endpoints or supported import workflows.

## Decision Table

### Need to write SPL2 searches, modules, custom functions, types, or pipelines?

Use `spl2-authoring.md`.

Default: SPL2 for new search work on Splunk 10.2+. Use `from` command with SQL-style
clauses for new searches. Use the module editor for multi-statement work. Use custom
functions and types when building reusable SPL2 resources. Use pipeline patterns for
Edge/Ingest Processor work.

### Need data out of Splunk for analysis, ETL, or a CLI?

Use `python-sdk.md` and `rest-search-patterns.md`.

Default: Python SDK for auth/job lifecycle, raw REST export for large streaming result sets.

### Need to inspect a Splunk instance, inventory objects, or audit config?

Use `admin-searches.md`.

Default: `rest`, `metadata`, and `tstats`. Avoid raw event scans unless you need event content.

### Need to create or update ITSI objects like entities, services, KPI base searches, or event aggregation policies?

Use `itsi-implementation.md` with either `python-sdk.md` or `rest-search-patterns.md`.

Default: prefer supported ITSI import or REST object workflows, not direct KV-store writes. For recurring service/entity onboarding, bias toward saved searches plus `itsiimportobjects`. For event aggregation, define filtering and split-by rules deliberately and keep episode logic explicit.

### Need a Splunk add-on with config UI, modular inputs, or alert actions?

Use `ucc-framework.md` and likely `app-packaging.md`.

Default: UCC. Treat packaging/AppInspect as part of the implementation, not postscript.

### Need a dashboard or dashboard migration?

Use `dashboard-development.md`.

Default: Dashboard Studio for new work; Simple XML for edits inside an existing XML-heavy app.

### Need an MCP server or AI-safe integration?

Use `mcp-integration.md` plus either `python-sdk.md` or `rest-search-patterns.md`.

Default: server-side credentials, read-only-by-default tools, validated SPL.

### Need to install, upgrade, or automate Splunk infrastructure?

Use `platform-admin.md`.

Default: official Splunk automation repos and admin manual concepts, not bespoke scripts first.

## Search Execution Defaults

- Add explicit time bounds.
- Add explicit limits or paging.
- Use `search/jobs` for managed jobs.
- Use export endpoints when you need streaming output and do not need a persistent SID.
- Use SDK job abstractions for moderate searches where polling and result paging are acceptable.
- Keep query construction separate from result handling.

## Enterprise Vs Cloud

- Splunk Enterprise gives broader host/admin access.
- Splunk Cloud often constrains platform-level operations and may require Support enablement for specific REST/API capabilities.
- For app/add-on guidance, always check whether the task is Cloud-safe before recommending local filesystem or admin-server assumptions.
- For ITSI specifically, Enterprise-only filesystem steps like editing `authorize.conf` or `metadata/local.meta` do not translate directly to Splunk Cloud; prefer Splunk Web and documented Cloud-safe admin flows there.

## Knowledge Object Defaults

Treat these as first-class assets:

- saved searches and alerts
- dashboards/views
- macros
- lookups
- field extractions and props/transforms-driven behavior
- data models
- KV store collections

For inventory and audits, start with `admin-searches.md`. For packaging and app
delivery, include those objects intentionally in the app structure and validate
them with `app-packaging.md`.

## Safe Patterns

- Keep auth in env vars or approved secret stores.
- Separate read paths from write paths in code and tool design.
- Scope namespaces deliberately when using REST or SDK config/object APIs.
- Return structured output from automation and MCP tools.
- When in doubt, choose the path that is easiest to reason about operationally:
  Python script > custom REST endpoint > full Splunk app.

## Replaces

This skill subsumes the old:

- `splunk-sdk`
- `splunk-quick-searches`

Keep the shims for backward compatibility, but maintain real guidance here.
