---
name: asset-license-checker
description: Verify license compliance for downloaded 3D assets, textures, HDRIs, fonts before scene build or export.
---

# asset-license-checker

## Purpose
Catch license risk before assets go into a scene that will be rendered, exported, or shipped. This is a planning / validation skill — does not modify assets, does not consult lawyers.

## Quick start
- list every external asset (model, texture, HDRI, font, sound, brushes)
- record source URL + license name + permissions per asset
- flag risk per asset (Pass / Warn / Fail)
- emit asset row table + handoff to scene build only if all rows are Pass or explicitly accepted Warn

## When to use
- after `blender-asset-discovery-planner` produces asset list
- before scene build / mutation / render
- before any export or commercial distribution
- when a previously-used asset's license is unclear

## When not to use
- asset modeling that you author yourself (no third-party license)
- pure planning before assets are sourced
- legal advice (this skill flags risk; it does not give legal opinion)

## Trigger phrases
- "is this license OK"
- "can I use this commercially"
- "what's the license"
- "license check"

## Prerequisites / readiness
- asset list with sources known
- intended use case known (commercial / non-commercial / internal / open-source)
- target license compatibility known (e.g., MIT / CC0 / CC-BY / proprietary)

## Input schema

### Required inputs

| Input | Why it is required |
|---|---|
| Asset list (name + source) | Scope of check |
| Intended use case | Drives compatibility |
| Target attribution policy | Some licenses require attribution |

### Optional inputs

| Input | Use |
|---|---|
| Existing internal license whitelist | Pre-approved sources |
| Brand legal policy | Per-company override rules |

### Assumptions to confirm
- Asset license file or page is publicly readable.
- License version is current (licenses sometimes change).
- The user's intended use is accurately stated.

## Output schema

### Primary output
A per-asset row table: name, source URL, license name, attribution required (Y/N), commercial allowed (Y/N), modification allowed (Y/N), redistribution allowed (Y/N), verdict (Pass / Warn / Fail), notes.

### Secondary output
- attribution lines required (if any)
- assets to remove if Fail
- top-line status

### Evidence / caveat output

```txt
Runtime status: Not Run | Attempted | Produced | Verified | Failed | Blocked / Not Run
Artifact status: Not Run | Not Produced | Produced | Verified | Failed
Evidence used: <links, paths, logs, or "none">
Limitations: <known gaps>
```

## Required laws
- `../../laws/evidence-before-done.md`
- `../../laws/non-blender-user-language.md`
- `../../laws/no-arbitrary-python-interface.md`
- `../../laws/official-runtime-only.md`

## Official runtime boundary

Validation skill — does not modify assets, does not run Blender. Verdicts are based on documented license terms, not legal interpretation. **Not legal advice**: when in doubt, recommend the user consult their legal team.

## Operating procedure
1. Read asset list from `blender-asset-discovery-planner` output.
2. For each asset, look up its license (per `references/license-source-rules.md`).
3. Map license to permissions (commercial / modification / redistribution / attribution).
4. Compare against intended use.
5. Assign verdict per asset.
6. List required attribution lines.
7. Flag assets to remove if Fail.
8. Hand off to scene build only if all Pass / explicitly accepted Warn.

## Decision tree

```txt
License unknown?
  → Fail until source confirmed
"Free for personal use" but commercial intent?
  → Fail
"Free for any use, attribution required" + intended attribution policy = "no attribution"?
  → Fail
"CC0 / public domain"?
  → Pass for any use
"Proprietary / EULA"?
  → Read EULA carefully; default Warn until terms clarified
```

## Playbooks

### Playbook A: Commercial brand campaign
Strict policy: only CC0, MIT, or paid-licensed assets. CC-BY allowed if attribution renders correctly. No CC-BY-NC.

### Playbook B: Internal tool / non-commercial
Most CC variants allowed; flag attribution requirements; track them.

### Playbook C: Open-source pack release
Match the pack's license; for MIT pack, only MIT or more-permissive (CC0) assets.

## Mode handling

### Text-only mode
License rows from asset spec; no actual file inspection.

### Runtime-ready mode
License rows verified from actual asset metadata where available.

### Blocked runtime mode
Skip rows that need file inspection; mark as such.

## Validation checklist
- [ ] Every asset has a row
- [ ] Source URL recorded
- [ ] License name recorded
- [ ] Permissions per row recorded (commercial / modification / redistribution / attribution)
- [ ] Verdict assigned
- [ ] Attribution lines listed
- [ ] Top-line status derived

## Pass / Warn / Fail rubric

| Verdict | Criteria |
|---|---|
| Pass | License explicit + permissions match intended use + attribution handled. |
| Warn | License clear but attribution policy needs verification, or "all rights reserved" with no clear permission. |
| Fail | License missing / contradicts intended use; commercial use of non-commercial license; redistribution requested but not allowed. |

## Failure handling
- License unknown → block asset until clarified.
- Attribution required but no plan to render attribution → block until plan exists.
- "Probably fine" answer → downgrade to Warn; user must accept.

## Troubleshooting

| Problem | Response |
|---|---|
| License page 404 | Block asset; require alternative source. |
| License changed since download | Re-evaluate; assets purchased at older terms usually grandfather, but verify. |
| Mixed-license aggregation (asset bundle with multiple licenses) | Treat each sub-asset separately. |
| AI-generated asset | Verify the AI tool's license terms permit your use case. |

## Best practices
- Record license at acquisition time, not at build time.
- Maintain an internal whitelist for repeat sources.
- Never ship without verifying every external asset's license.
- "Not legal advice" — escalate ambiguity to legal.

## Good examples
- "Asset: hdri-studio.exr, source: polyhaven.com, license: CC0, commercial: Y, attribution: N (CC0). Verdict: Pass."

## Bad examples
- "Asset is from internet." — no source, no license.

## User-facing response template

```txt
Intended use: <commercial / non-commercial / internal / open-source>
Attribution policy: <where attribution will render or "none">

| Asset | Source | License | Comm | Mod | Redist | Attribution | Verdict | Notes |
|---|---|---|---|---|---|---|---|---|

Required attribution lines:
  - <line 1>
  - <line 2>

Assets to remove (Fail): <list or "none">
Top-line: <Pass / Warn / Fail>
Note: not legal advice; escalate ambiguity to legal team.
Limitations: <gaps>
Next: scene build (only if Pass) / asset re-discovery (if Fail)
```

## Anti-patterns
- "Should be fine" verdicts.
- Skipping the attribution plan.
- Treating "all rights reserved" assets as usable.
- Inventing license terms.

## Cross-skill handoff
- Asset discovery → `../blender-asset-discovery-planner/SKILL.md`
- Style consistency → `../asset-style-consistency-checker/SKILL.md`
- Fallback strategy → `../asset-fallback-strategy/SKILL.md`
- Library organization → `../asset-library-organization-planner/SKILL.md`

## Non-goals
- Give legal advice.
- Modify asset files.
- Run Blender.
- Negotiate licenses.

## References
- `references/common-license-mapping.md`
- `references/license-source-rules.md`
- `references/attribution-rendering-patterns.md`
- `../../docs/skill-system.md`
