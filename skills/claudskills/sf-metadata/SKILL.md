---
name: sf-metadata
description: Salesforce metadata generation and querying with 120-point scoring + Brite metadata-authoring discipline (Activity fields, ListView aliases, Kanban Group By cache, Flexipage IndexedDB, Dynamic Forms FLS). TRIGGER when: user creates custom objects, fields, validation rules, or touches .object-meta.xml, .field-meta.xml, .profile-meta.xml, layouts/, listViews/, flexipages/, standardValueSets/ files. DO NOT TRIGGER when: permission set analysis (use sf-permissions), deploying metadata (use sf-deploy), or Flow XML (use sf-flow).
user-invocable: false
license: MIT
metadata:
  version: "1.2.0-brite.1"
  author: "Jag Valaiyapathy (upstream); Brite Company (customization)"
  upstream: "Jaganpro/sf-skills@ff1ab74"
  scoring: "120 points across 6 categories"
---

<!-- Adapted from Jaganpro/sf-skills@ff1ab74 (MIT). This file layers Brite conventions from brite-salesforce/CLAUDE.md §Metadata Authoring (lines 120-143) + §Engineering Standards (lines 37-50). -->

# sf-metadata: Salesforce Metadata Generation and Org Querying

Use this skill when the user needs **metadata definition or org metadata discovery**: custom objects, fields, validation rules, record types, page layouts, permission sets, or schema inspection with `sf` CLI.

## Brite Context

Brite runs all Salesforce metadata out of `brite-salesforce/force-app/main/default/` in SFDX source format at `sourceApiVersion: 65.0`. Authoring discipline is concentrated in `brite-salesforce/CLAUDE.md` §Metadata Authoring (lines 120-143) — 20 bullets covering Activity fields, ListView serialization, PathAssistant/FloatingPanel constraints, Prompt-sandbox exclusion, Kanban Group By cache, Flexipage IndexedDB cache + template names, and Dynamic Forms FLS + visibility semantics. Two §Metadata Authoring bullets (HubSpot email Task migration, `Messaging.SingleEmailMessage` no-EmailMessage-row) are **out of scope here** — they're Apex-runtime / ETL concerns covered by `sf-apex` and `sf-data`.

Brite's authoring posture is **standard-fields-first + permissions-on-permsets-not-profiles**: only the `Minimum Access` profile is tracked in source, so new custom field FLS always lands on permission sets (see `sf-permissions`). API v65.0 is set org-wide; every new metadata file inherits it through `sfdx-project.json`.

**See also:**
- `brite-salesforce/CLAUDE.md` §Metadata Authoring lines 120-143 (source of 20 bullets — 18 in scope, distilled into 17 rules at Rules 5-21 because lines 135+140 merged into Rule 20; 2 out-of-scope per §Brite Context above)
- `brite-salesforce/CLAUDE.md` §Engineering Standards lines 37-50 (SFDX source, API v65, Standard fields first, Minimum Access profile)
- `brite-salesforce/.forceignore` (canonical Prompt-exclusion list)
- `brite-salesforce/docs/plans/bc-1720-prompt-creation-guide.md` (FloatingPanel alternative via Setup UI)
- `plugins/revops/skills/sf-permissions/SKILL.md` (where new-field FLS goes — permset sync discipline)
- `plugins/revops/skills/sf-deploy/SKILL.md` (post-deploy verification — flush caches, re-activate Flows, re-schedule Apex)

## Brite Metadata Conventions

Each rule cites the `brite-salesforce/CLAUDE.md` source line where the convention originates. All anchors verified via `gh api` fetch on 2026-04-20.

### Source format & authoring principles

1. **SFDX source format (not MDAPI)** — all metadata under `force-app/main/default/`. Never author in MDAPI shape. [§Engineering Standards line 39]
2. **API version 65.0** — set in `sfdx-project.json` `sourceApiVersion`. All new metadata inherits it; don't override per-file unless cross-org compatibility requires. [§Engineering Standards line 40]
3. **Standard fields first** — exhaust standard Salesforce fields before proposing custom. Especially the FSL standard data model (`Location`, `WorkType`, `WorkOrderLineItem`). [§Engineering Standards line 45]
4. **Permissions go to Permission Sets, never profiles** — only the `Minimum Access` profile is tracked in source. New `CustomField` FLS always lands on permsets (see `sf-permissions` for the 7-permset sync discipline). [§Engineering Standards line 47]

### Metadata API / retrieve-and-deploy authoring constraints

5. **Activity fields live on the `Activity` object** — custom fields on `Task` and `Event` must be authored in `objects/Activity/fields/`. Metadata API rejects `Task` and `Event` as standalone custom-field targets. FLS references still use `Task.Field__c` / `Event.Field__c` at the permset level. [§Metadata Authoring line 122]
6. **Retrieved StandardValueSet may be incomplete** — `sf project retrieve start -m StandardValueSet:X` returns only Salesforce-tracked standard values, not all org values. Deploying an incomplete SVS can strip values. Cross-check record-type `<picklistValues>` references before deploy. [§Metadata Authoring line 123]
7. **Profile XML field ordering must stay alphabetical** — keep `fieldPermissions`, `layoutAssignments`, `recordTypeVisibilities` alphabetical. Metadata API accepts any order on deploy, but `sf project retrieve` rewrites canonical alphabetical and creates spurious diffs otherwise. [§Metadata Authoring line 124]
8. **ListView `<booleanFilter>` must immediately follow `<fullName>`** — before `<columns>`. Same rewrite-on-retrieve gotcha as profiles. [§Metadata Authoring line 125]
9. **ListView column aliases are object-specific** — standard field column names differ by object. LeadSource example: Lead uses `LEAD_SOURCE`, Contact uses `CONTACT.LEAD_SOURCE`, Opportunity uses `OPPORTUNITY.LEAD_SOURCE`. Wrong alias → "Could not resolve list view column" deploy error. Check existing list views on the same object before adding columns. [§Metadata Authoring line 126]
10. **Layout related-list format for custom lookups** — use `{ChildObject}.{LookupField}` (e.g., `Lead.Territory__c`), NOT `{relationshipName}__r`. Standard related lists use their own names (e.g., `RelatedContactList`). [§Metadata Authoring line 127]
11. **Restricted picklist values need RT-level `picklistValues`** — a restricted picklist custom field (e.g., `Lifecycle_Stage__c` using a restricted global value set) needs explicit `<picklistValues>` blocks on each record type, even though the GVS already defines all values. [§Metadata Authoring line 128]

### Setup-UI / declarative-rendering constraints

12. **PathAssistant requires a real record type** — `recordTypeName` is required and must resolve to an actual RT. Objects without RTs (e.g., Contact) cannot deploy PathAssistant via metadata; create through Setup > Path Settings instead. The flexipage `pathAssistant` component itself can still be deployed via metadata. [§Metadata Authoring line 129]
13. **Metadata API supports `FloatingPanel` only on named pages** — `Walkthrough` `displayType` and record-page targets are rejected. Create walkthroughs and record-page prompts through Setup > User Engagement > In-App Guidance. `delayDays` must be 1–30 (not 0). See `brite-salesforce/docs/plans/bc-1720-prompt-creation-guide.md`. [§Metadata Authoring line 130]
14. **Dev sandbox rejects ALL Prompt metadata** — prompts are excluded from sandbox deploys via `.forceignore`. Deploy directly to production and configure prompts manually in sandbox. [§Metadata Authoring line 131]

### Cache + declarative-deployment gaps

15. **Kanban Group By dropdown caches stale field metadata** — newly-deployed picklist fields on standard objects (Contact, etc.) do NOT immediately appear in the Lightning UI's Kanban Settings > Group By dropdown, even when FLS, GVS, and records are all in place. Force a refresh by **adding the field to a page layout** for the affected object and deploying — the layout change flushes the UI cache. Sandbox caches less aggressively than prod. Verified against `Contact.Lead_Status__c` (BC-4734, 2026-04-07). [§Metadata Authoring line 132]
16. **Kanban Group By selection is NOT deployable** — there is no `KanbanView` sObject in the Tooling API and no `kanbanGroupingField` element in `ListView` metadata. The selection lives at the UI layer, is per-list-view, and must be configured manually in each org via gear > Kanban Settings. Sandbox refreshes lose it. Document manual steps for any list view that should default to kanban. [§Metadata Authoring line 133]
17. **Flexipage record-page assignments are NOT deployable as org defaults** — `FlexipageAssignment` for org-wide defaults is not a metadata type. Use `actionOverrides` in app metadata files (e.g., `Business_Development.app-meta.xml`) to assign record pages per-app. Without this, each sandbox refresh requires manual Lightning App Builder activation. [§Metadata Authoring line 137]
18. **Flexipage two-column template is `flexipage:recordHomeTemplateDesktop`** — NOT `flexipage:recordHomeTwoColTemplateDesktop` (that name does not exist). Regions: `sidebar` (left) and `main` (right). Three-column template: `flexipage:recordHomeThreeColTemplateDesktop` with regions `leftsidebar`, `main`, `rightsidebar`. [§Metadata Authoring line 138]
19. **Flexipage changes cached in IndexedDB for hours** — after deploying flexipage changes, Lightning caches the old definition in IndexedDB (`actions` database). Hard refresh (`Cmd+Shift+R`) does NOT clear it. To see changes: log out and back in, run `indexedDB.deleteDatabase("actions")` in Chrome console, or open the page in Lightning App Builder and click Save. For sandbox, disable durable caching via Setup > Session Settings. [§Metadata Authoring line 139]

### Dynamic Forms — field-level semantics + FLS

20. **Dynamic Forms visibility + `uiBehavior` semantics** — field-level rules (`visibilityRule` on `fieldItem`) evaluate reactively during editing; section-level rules (`visibilityRule` on `fieldSection`) evaluate only on saved record values. Use field-level for fields that should appear/disappear as the user edits a controlling picklist. For auto-populated DateTime fields on flexipages, use `uiBehavior: readonly` (not `none`) — `none` can cause the field not to render. Other lifecycle date fields use `readonly` as the standard pattern. [§Metadata Authoring lines 135 + 140]
21. **Dynamic Forms requires FLS even for System Administrators** — `View All Data` / `Modify All Data` do NOT bypass Field-Level Security. A custom field with no `FieldPermissions` records on any permission set or profile is hidden by Dynamic Forms, even for admins. Always deploy FLS alongside new fields. If `--source-dir` deploys roll back (e.g., ECA failures), deploy field metadata and FLS individually with `-m` flags. [§Metadata Authoring line 136]

## When This Skill Owns the Task

Use `sf-metadata` when the work involves:
- object, field, validation rule, record type, layout, profile, or permission-set metadata
- `.object-meta.xml`, `.field-meta.xml`, `.profile-meta.xml`, and related metadata files
- describing schema before coding or Flow work
- generating metadata XML from requirements

Delegate elsewhere when the user is:
- analyzing permission access rather than defining metadata → [sf-permissions](../sf-permissions/SKILL.md)
- deploying metadata → [sf-deploy](../sf-deploy/SKILL.md)
- editing Flow XML → [sf-flow](../sf-flow/SKILL.md)

---

## Required Context to Gather First

Ask for or infer:
- whether the user wants **generation** or **querying**
- metadata type(s) involved
- target object / field / package directory
- target org alias if querying is required
- whether new custom objects or fields should also include **permission-set / FLS generation**

Unless the user explicitly opts out, assume new custom objects or fields need permission-set follow-up.

---

## Recommended Workflow

### 1. Choose the mode
| Mode | Use when |
|---|---|
| generation | the user wants new or updated metadata XML |
| querying | the user needs object / field / metadata discovery |

### 2. Start from templates or CLI describe data
For generation, use the assets under:
- `assets/objects/`
- `assets/fields/`
- `assets/permission-sets/`
- `assets/profiles/`
- `assets/record-types/`
- `assets/validation-rules/`
- `assets/layouts/`

For querying, prefer `sf` metadata and `sobject describe` commands.

Recent SDR/CLI support worth knowing when reading older examples: `CnfgItemSourceDefinition`, `ExtlClntAppOauthSecuritySettings`, and `UIBundle` are now source-supported under their current names. See [references/metadata-types-reference.md](references/metadata-types-reference.md).

### 3. Validate metadata quality
Check:
- naming conventions
- structural correctness
- field-type fit
- security / FLS implications
- downstream deployment dependencies

### 4. Plan permission impact by default
When new custom fields or objects are created:
- default to generating or updating a Permission Set unless the user opts out
- include `fieldPermissions` for **eligible custom fields**
- note any metadata categories that are excluded because Salesforce treats them as system-managed or always-available
- remember that object CRUD alone does **not** make custom fields visible

### 5. Hand off deployment
Use [sf-deploy](../sf-deploy/SKILL.md) when the user needs the metadata rolled out.

---

## High-Signal Rules

- field-level security is often the hidden blocker after deployment
- **object permissions ≠ field permissions**
- prefer permission sets over profile-centric access patterns
- generate Permission Set follow-up by default for new custom objects and fields
- include `fieldPermissions` for eligible custom fields instead of leaving FLS as a manual afterthought
- avoid hardcoded IDs in formulas or metadata logic
- validation rules should have intentional bypass strategy when operationally necessary
- create metadata before attempting Flow or data tasks that depend on it

---

## Output Format

When finishing, report in this order:
1. **Metadata created or queried**
2. **Files created or updated**
3. **Key schema/security decisions**
4. **Permission / layout follow-ups**
5. **Deploy next step**

Suggested shape:

```text
Metadata task: <generate / query>
Items: <objects, fields, rules, layouts, permsets>
Files: <paths>
Notes: <naming, field types, security, dependencies>
Next step: <deploy, assign permset, or verify in Setup>
```

---

## Cross-Skill Integration

| Need | Delegate to | Reason |
|---|---|---|
| deploy metadata | [sf-deploy](../sf-deploy/SKILL.md) | rollout and validation |
| build Flows on new schema | [sf-flow](../sf-flow/SKILL.md) | declarative automation |
| build Apex on new schema | [sf-apex](../sf-apex/SKILL.md) | code against metadata |
| analyze permission access after creation | [sf-permissions](../sf-permissions/SKILL.md) | access auditing |
| seed data after deploy | [sf-data](../sf-data/SKILL.md) | test data creation |

---

## Reference Map

### Start here
- [references/field-and-cli-reference.md](references/field-and-cli-reference.md)
- [references/metadata-types-reference.md](references/metadata-types-reference.md)
- [references/naming-conventions.md](references/naming-conventions.md)
- [references/orchestration.md](references/orchestration.md)

### Security / scoring / examples
- [references/fls-best-practices.md](references/fls-best-practices.md)
- [references/permset-auto-generation.md](references/permset-auto-generation.md)
- [references/best-practices-scoring.md](references/best-practices-scoring.md)
- [references/field-types-guide.md](references/field-types-guide.md)
- [references/field-types-example.md](references/field-types-example.md)
- [references/custom-object-example.md](references/custom-object-example.md)
- [references/permission-set-example.md](references/permission-set-example.md)
- [references/profile-permission-guide.md](references/profile-permission-guide.md)
- [references/sf-cli-commands.md](references/sf-cli-commands.md)
- [assets/](assets/)

---

## Score Guide

| Score | Meaning |
|---|---|
| 108+ | strong production-ready metadata |
| 96–107 | good metadata with minor review items |
| 84–95 | acceptable but validate carefully |
| < 84 | block deployment until corrected |
