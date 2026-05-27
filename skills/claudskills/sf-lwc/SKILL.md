---
name: sf-lwc
description: Lightning Web Components (Brite edition) with PICKLES methodology and 165-point scoring. TRIGGER when user creates/edits LWC components, touches lwc/**/*.js, .html, .css, .js-meta.xml files, works in brite-salesforce, asks about wire service, SLDS, Jest LWC tests, the LWC Jest pre-commit hook, Dynamic Forms requiring FLS even for admins (`View All Data` does NOT bypass FLS), Dynamic Forms field-level vs section-level visibility evaluation, Flexipage IndexedDB cache flushing (hard refresh insufficient), the `flexipage:recordHomeTemplateDesktop` two-column template name (NOT `...TwoColTemplateDesktop`), Dynamic Forms DateTime `uiBehavior=readonly` for auto-populated fields, or `@AuraEnabled` security primitives. DO NOT TRIGGER when Apex classes (use sf-apex), Aura components, or Visualforce.
user-invocable: false
license: MIT
metadata:
  version: "2.1.0-brite.1"
  author: "Jag Valaiyapathy (upstream); Brite Company (customization)"
  upstream: "Jaganpro/sf-skills@ff1ab74"
  scoring: "165 points across 8 categories (SLDS 2 + Dark Mode compliant)"
---

<!-- Adapted from Jaganpro/sf-skills@ff1ab74 (MIT). This file layers Brite conventions from brite-salesforce/CLAUDE.md §Engineering Standards (line 43, LWC Jest pre-commit) + §Metadata Authoring (Dynamic Forms + Flexipage gotchas, lines 137-142). -->

# sf-lwc: Lightning Web Components Development (Brite edition)

Use this skill when the user needs **Lightning Web Components**: LWC bundles, wire patterns, Apex/GraphQL integration, SLDS 2 styling, accessibility, performance work, or Jest unit tests.

## Brite Context

Brite's LWC stance:

- **Jest required for all LWCs.** The pre-commit hook runs Jest tests on staged LWC files; any new LWC ships with Jest coverage. Source: `brite-salesforce/CLAUDE.md` §Engineering Standards line 43.
- **Dynamic Forms requires FLS even for admins.** `View All Data` / `Modify All Data` do NOT bypass Field-Level Security. A custom field with no `FieldPermissions` records is invisible in Dynamic Forms — even for System Administrators. Always deploy FLS alongside new fields.
- **Flexipage caches in IndexedDB for hours.** Hard browser refresh does NOT clear it. Three flush options: log out and back in, run `indexedDB.deleteDatabase("actions")` in Chrome console, or open the page in Lightning App Builder and click Save.
- **Two-column template name is `flexipage:recordHomeTemplateDesktop`** — NOT `...TwoColTemplateDesktop` (that name does not exist). Regions: `sidebar` (left) + `main` (right).

**See also:** [sf-apex](../sf-apex/SKILL.md) for `@AuraEnabled` controllers and security primitives; [sf-flow](../sf-flow/SKILL.md) when an LWC embeds in a screen flow; [sf-metadata](../sf-metadata/SKILL.md) for the broader Dynamic Forms / Flexipage gotcha set; [sf-deploy](../sf-deploy/SKILL.md) for FLS-alongside-fields deploy discipline.

## Brite LWC Discipline

These rules are non-negotiable on `brite-salesforce` and must surface during LWC authoring, deploy, and post-deploy verification.

### 1. Jest required for all LWCs

The pre-commit hook runs `npm test` against staged LWC files. Any new LWC ships with Jest coverage. Canonical commands: `npm test`, `npm run test:unit:coverage`. Source: §Engineering Standards line 43.

### 2. Dynamic Forms requires FLS even for admins

`View All Data` / `Modify All Data` do NOT bypass Field-Level Security. Deploy FLS alongside any new field used in a Dynamic Form. If `--source-dir` deploys roll back (e.g., ECA failures), deploy fields and FLS individually with `-m` flags. Source: §Metadata Authoring line 138.

### 3. Field-level vs section-level visibility evaluate differently

Field-level rules (`visibilityRule` on `fieldItem`) evaluate **reactively during editing**. Section-level rules (`visibilityRule` on `fieldSection`) evaluate **only on saved record values**. Use field-level when a field should appear/disappear as the user edits a controlling picklist.

### 4. Flexipage cache lives in IndexedDB and persists for hours

Hard refresh (`Cmd+Shift+R`) does NOT clear it. Flush via:

- log out and back in, OR
- `indexedDB.deleteDatabase("actions")` in Chrome console, OR
- open the page in Lightning App Builder and click Save.

For sandbox dev, consider disabling durable caching: Setup → Session Settings → uncheck "Enable secure and persistent browser caching."

### 5. Two-column template name

`flexipage:recordHomeTemplateDesktop` — NOT `flexipage:recordHomeTwoColTemplateDesktop` (that name does not exist). Regions: `sidebar` (left) + `main` (right). Three-column equivalent: `flexipage:recordHomeThreeColTemplateDesktop` with regions `leftsidebar`, `main`, `rightsidebar`.

### 6. Dynamic Forms `uiBehavior` for DateTime fields — use `readonly`, not `none`

`none` can cause the field to not render. `readonly` is the standard pattern for auto-populated DateTime fields on flexipages.

### 7. LWC security primitives — `@AuraEnabled` runs in user context but does NOT auto-enforce CRUD/FLS

Apex methods exposed with `@AuraEnabled(cacheable=true)` execute in the calling user's session, so user-level access checks apply — but the annotation alone does NOT enforce CRUD/FLS on DML or SOQL. Enforce explicitly: declare the class `with sharing`, use `WITH SECURITY_ENFORCED` on SOQL, or run `Security.stripInaccessible` / `Schema.DescribeFieldResult` checks before DML. This pairs with sf-apex's broader Apex security guidance.

## When This Skill Owns the Task

Use `sf-lwc` when the work involves:
- `lwc/**/*.js`, `.html`, `.css`, `.js-meta.xml`
- component scaffolding and bundle design
- wire service, Apex integration, GraphQL integration
- SLDS 2, dark mode, and accessibility work
- Jest unit tests for LWC

Delegate elsewhere when the user is:
- writing Apex controllers or business logic first → [sf-apex](../sf-apex/SKILL.md)
- building Flow XML rather than an LWC screen component → [sf-flow](../sf-flow/SKILL.md)
- deploying metadata → [sf-deploy](../sf-deploy/SKILL.md)

---

## Required Context to Gather First

Ask for or infer:
- component purpose and target surface
- data source: LDS, Apex, GraphQL, LMS, or external system via Apex
- whether the user needs tests
- whether the component must run in Flow, App Builder, Experience Cloud, or dashboard contexts
- accessibility and styling expectations

---

## Recommended Workflow

### 1. Choose the right architecture
Use the **PICKLES** mindset:
- prototype
- integrate the right data source
- compose component boundaries
- define interaction model
- use platform libraries
- optimize execution
- enforce security

### 2. Choose the right data access pattern
| Need | Default pattern |
|---|---|
| single-record UI | LDS / `getRecord` |
| simple CRUD form | base record form components |
| complex server query | Apex `@AuraEnabled(cacheable=true)` |
| related graph data | GraphQL wire adapter |
| cross-DOM communication | Lightning Message Service |

### 3. Start from an asset when useful
Use provided assets for:
- basic component bundles
- datatables
- modal patterns
- Flow screen components
- GraphQL components
- LMS message channels
- Jest tests
- TypeScript-enabled components

### 4. Validate for frontend quality
Check:
- accessibility
- SLDS 2 / dark mode compliance
- event contracts
- performance / rerender safety
- Jest coverage when required

### 5. Hand off supporting backend or deploy work
Use:
- [sf-apex](../sf-apex/SKILL.md) for controllers / services
- [sf-deploy](../sf-deploy/SKILL.md) for deployment
- [sf-testing](../sf-testing/SKILL.md) only for Apex-side test loops, not Jest

---

## High-Signal Rules

- prefer platform base components over reinventing controls
- use `@wire` for reactive read-only use cases; imperative calls for explicit actions and DML paths
- do not introduce inaccessible custom UI
- avoid hardcoded colors; use SLDS 2-compatible styling hooks / variables
- avoid rerender loops in `renderedCallback()`
- keep component communication patterns explicit and minimal

---

## Output Format

When finishing, report in this order:
1. **Component(s) created or updated**
2. **Data access pattern chosen**
3. **Files changed**
4. **Accessibility / styling / testing notes**
5. **Next implementation or deploy step**

Suggested shape:

```text
LWC work: <summary>
Pattern: <wire / apex / graphql / lms / flow-screen>
Files: <paths>
Quality: <a11y, SLDS2, dark mode, Jest>
Next step: <deploy, add controller, or run tests>
```

---

## Local Development Server

Preview LWC components locally with hot reload — no deployment needed:

```bash
# Preview LWC components in isolation
sf lightning dev component --target-org <alias>

# Preview a Lightning Experience app locally
sf lightning dev app --target-org <alias>

# Preview an Experience Cloud site locally
sf lightning dev site --target-org <alias>
```

In current SF CLI releases, these Local Dev commands are installed just-in-time the first time you run them. They are long-running processes that open a browser with live preview. Changes to `.js`, `.html`, and `.css` files auto-reload instantly. Requires an active org connection for data and Apex callouts.

---

## Cross-Skill Integration

| Need | Delegate to | Reason |
|---|---|---|
| Apex controller or service | [sf-apex](../sf-apex/SKILL.md) | backend logic |
| embed in Flow screens | [sf-flow](../sf-flow/SKILL.md) | declarative orchestration |
| deploy component bundle | [sf-deploy](../sf-deploy/SKILL.md) | org rollout |
| create metadata like message channels | [sf-metadata](../sf-metadata/SKILL.md) | supporting metadata |

---

## Reference Map

### Start here
- [references/component-patterns.md](references/component-patterns.md)
- [references/slds-design-guide.md](references/slds-design-guide.md)
- [references/lwc-best-practices.md](references/lwc-best-practices.md)
- [references/scoring-and-testing.md](references/scoring-and-testing.md)
- [references/jest-testing.md](references/jest-testing.md)

### Accessibility / performance / state
- [references/accessibility-guide.md](references/accessibility-guide.md)
- [references/performance-guide.md](references/performance-guide.md)
- [references/state-management.md](references/state-management.md)
- [references/template-anti-patterns.md](references/template-anti-patterns.md)

### Integration / advanced features
- [references/lms-guide.md](references/lms-guide.md)
- [references/flow-integration-guide.md](references/flow-integration-guide.md)
- [references/advanced-features.md](references/advanced-features.md)
- [references/async-notification-patterns.md](references/async-notification-patterns.md)
- [references/triangle-pattern.md](references/triangle-pattern.md)
- [assets/](assets/)

---

## Score Guide

| Score | Meaning |
|---|---|
| 150+ | production-ready LWC bundle |
| 125–149 | strong component with minor polish left |
| 100–124 | functional but review recommended |
| < 100 | needs significant improvement |
