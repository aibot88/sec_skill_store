---
name: fedramp-ssp-expert
description: Expertise on FedRAMP SSP authoring — what the DOCX templates contain, what OSCAL 1.2.0 SSP looks like for FedRAMP, how this plugin fits alongside Compliance Trestle and oscal-cli.
---

# fedramp-ssp expert

You are the guide for turning FedRAMP Rev 5 Word-template SSPs into machine-readable OSCAL 1.2.0.

## What FedRAMP SSP looks like

FedRAMP publishes three Word-template documents that CSPs fill in:

1. **SSP (main template)** — system identification, authorization boundary, inventory, leveraged authorizations, roles, parties. Typically 60-80 pages.
2. **Appendix A (Moderate or High)** — the 323 (Moderate) or 421 (High) NIST 800-53 Rev 5 control responses with FedRAMP-specific additional requirements. Each requirement has status, origination, and implementation narrative fields.
3. **Appendices B–N** — data flow, inventory, separation of duties, IRP, privacy threshold, etc. This plugin does *not* convert these yet.

The DOCX→OSCAL pipeline here consumes the main SSP + Appendix A and produces an OSCAL 1.2.0 SSP JSON covering the most-critical content.

## What the output contains

- `metadata`: system name, authorization path, version, last-modified
- `system-characteristics`: identification, authorization boundary, system information, data types (security objectives for confidentiality/integrity/availability)
- `system-implementation`: users, components, leveraged authorizations, inventory items
- `control-implementation`: 323 implemented-requirements, each with implementation status, control origination, responsible roles, and narrative `by-component` statements
- `back-matter`: resources and references

The output uses FedRAMP-namespaced props (`https://fedramp.gov/ns/oscal`) for fields like implementation-status, control-origination, cloud deployment model.

## When to use this plugin

- **First-time authoring**: you've got FedRAMP templates filled in by your team and need to hand a machine-readable version to your 3PAO or AO.
- **Continuous compliance**: re-run after every DOCX update and diff the OSCAL output — much easier than diffing 80-page Word documents.
- **FedRAMP 20X alignment**: 20X workflows consume OSCAL directly; this is the bridge from traditional Rev 5 SSP authoring to 20X automation.
- **eMASS import**: eMASS supports OSCAL imports for DoD environments.

## When NOT to use this plugin

- You're authoring from scratch with no DOCX source. Use Compliance Trestle for OSCAL-native authoring.
- You need semantic verification against the profile (does this SSP actually implement Moderate?). Use Trestle or an AO review.
- You want Appendix B-N conversion. Not supported yet; file an issue.

## How this plugin composes with others

- **`/oscal:validate`** — pass `--validate` to this plugin, or run `/oscal:validate` manually on the output.
- **`/oscal:convert`** — convert the JSON output to XML for Compliance Trestle or to YAML for human review.
- **`/grc-engineer:gap-assessment --output=oscal-ar`** — produces OSCAL Assessment Results. A full FedRAMP package is SSP + AR + POA&M; this plugin provides the SSP side.
- **Compliance Trestle skills** — the OSCAL authored here round-trips cleanly through Trestle's workflow.

## Common pitfalls

- **Placeholder text**: FedRAMP DOCX templates have `[CSP-specific: ...]` placeholders. If your team hasn't filled them in, the pipeline propagates placeholder text into the OSCAL narratives. Review before submission.
- **Control Origination** must be one of: `sp-system`, `sp-corporate`, `customer-configured`, `customer-provided`, `inherited`, `shared`. Values outside that set fail FedRAMP validation.
- **Leveraged authorization**: if your system is on a leveraged cloud (AWS GovCloud, Azure Government), the SSP must declare the leveraging relationship. The default config assumes AWS GovCloud FedRAMP High P-ATO; override if you're on a different platform.
- **Version drift**: the upstream tool currently targets OSCAL 1.2.0. `/oscal:validate` bundles 1.1.3. These are schema-compatible for the SSP subset used, but if you need strict 1.1.3, set `oscal-version: "1.1.3"` in the output or update the `oscal-cli` schema bundle.

## Non-goals

- **Not a FedRAMP policy authoring tool**: you still need your policies, procedures, and evidence. This generates the control-implementation narrative scaffolding from your DOCX inputs.
- **Not a control-effectiveness validator**: producing a well-formed SSP doesn't mean the controls are effective. Use `/grc-engineer:test-control` + a 3PAO assessment.
