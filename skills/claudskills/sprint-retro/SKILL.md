---
name: sprint-retro
description: Use when running a sprint retrospective, generating a retro, preparing retro data, or summarizing team activity for a retrospective. Takes team member names or a Slack alias as input. Gathers data from GitHub, Slack, Jira, Confluence, Google Docs, and CI/CD with strict privacy filtering.
argument-hint: <@team-alias or comma-separated names> [--sprint-window 14d] [--repos repo1,repo2]

category: report
capabilities: [claim-extraction, evidence-scoring]
input_types: [git-diff]
output_types: [design-spec, report]
complexity: moderate
cost_profile: low
maturity: beta
metadata_source: inferred
---

# Sprint Retro

Generates a data-backed sprint retrospective from multiple internal sources with strict privacy filtering that excludes DMs, private channels, restricted documents, and individually-shared content.

## Execution model

- All data passes through a 5-gate privacy checklist before inclusion. No exceptions.
- Every retro item must cite a specific public data source. Uncited items are filler — delete them.
- Sanitized or paraphrased private content is still a leak. Discard entirely.
- Time pressure never relaxes privacy gates. Shorter retro, not weaker filtering.
- Evidence file (`sprint-retro-evidence.json`) must exist on disk before claiming completion.
- Termination label is an honest enum, not self-assessed "done."

## Workflow

1. **Parse input** — extract team member names or Slack alias, sprint window, repo list from arguments.
2. **Resolve alias** — if input starts with `@`, resolve to individual names via Pandora/Slack search. List resolved names for user verification. See [`_shared/identity-resolution.md`](../_shared/identity-resolution.md) for the canonical identity resolution workflow. See [DATA-SOURCES.md](DATA-SOURCES.md).
3. **Gather data from all sources** — query GitHub, Slack (public only), Jira, Google Docs, CI/CD in parallel. See [DATA-SOURCES.md](DATA-SOURCES.md).
4. **Apply privacy gates** — run every search result through the 5-gate checklist. Discard anything that fails any gate. See [PRIVACY.md](PRIVACY.md).
5. **Check data coverage** — count sources with actual results. If fewer than 3: label is `retro_partial`. See [GOLDEN-RULES.md](GOLDEN-RULES.md).
6. **Synthesize retro document** — produce the retro in the structured format. Every item cites a source. Empty sections say "[No data available]" not filler. **Ownership filter:** only include items a resolved team member authored/owned (PR author, thread starter, ticket assignee) — discard items the team merely commented on, reacted to, or observed in a shared channel. See [FORMAT.md](FORMAT.md) and [GOLDEN-RULES.md](GOLDEN-RULES.md) rule 9.
7. **Write evidence file** — write `sprint-retro-evidence.json` with source coverage, privacy gate status, and termination label. See [FORMAT.md](FORMAT.md).
8. **Deliver** — present the retro document and evidence file. Note any coverage gaps.

## Honest termination labels

| Label | Meaning |
|---|---|
| `retro_complete` | 3+ sources returned data, all privacy gates applied, evidence file on disk. |
| `retro_partial` | Fewer than 3 sources returned data, or one or more sources failed. Coverage gaps noted. |
| `blocked_no_data` | No sources returned usable data. Retro cannot be produced. |
| `blocked_alias_unresolved` | Alias could not be resolved to team members. User input needed. |
| `cancelled` | User interrupted. |

## Self-review checklist

Before delivering, verify ALL:

- [ ] Every retro item cites a specific public source (PR link, Slack thread topic, Jira ID, build metric)
- [ ] Zero items derived from DMs, private channels, or restricted documents
- [ ] Zero items containing individual blame for failures (reframed as system issues)
- [ ] Data coverage table present with status for each of 5 sources
- [ ] `sprint-retro-evidence.json` exists on disk with `privacy_gates_applied: true`
- [ ] Termination label matches actual coverage (not `retro_complete` if fewer than 3 sources)
- [ ] Team members listed in output header (resolved from alias if applicable)
- [ ] Every retro item authored/owned by a resolved team member — no bystander attribution (rule 9)
- [ ] No generic filler text in any section — empty sections say "[No data available]"
- [ ] Privacy footer present at end of document
- [ ] No document titles containing sensitive keywords (1:1, performance, comp, PIP) appear anywhere
- [ ] HTML version uploaded to S3 with commuter link (unless `--no-html` or upload failed with noted fallback)
- [ ] Slack/chat delivery uses TLDR + link, not the full report

## Golden rules

Hard rules. Never violate these.

1. **Active filtering, not passive trust.** Never rely on tools to filter private content. Every result passes the 5-gate checklist or gets discarded.
2. **Sanitized leaks are still leaks.** Never paraphrase, summarize, or extract themes from private content. Discard entirely.
3. **Resolve before searching.** If input is an alias, resolve to names first. Never skip to keyword search.
4. **System blame, never individual blame.** Frame all problems as process/system issues, even when public data shows individual error.
5. **Minimum 3 sources for complete.** Fewer than 3 data sources with results = `retro_partial` label.
6. **Evidence file is the gate.** `sprint-retro-evidence.json` must exist on disk before claiming completion.
7. **No filler.** Every bullet cites a source. Empty sections say "[No data available]", not generic observations.
8. **Urgency never relaxes privacy.** Under time pressure, produce a shorter retro, not a faster-filtered one.

## Anti-rationalization counter-table

| Excuse | Reality |
|---|---|
| "The search tool returned it, so it must be team-visible." | Search tools index broadly. Run every result through the 5-gate checklist in PRIVACY.md. |
| "I'll include a sanitized version without names." | Sanitized private content reveals what was discussed privately. Discard the entire item. |
| "We're short on time, quick privacy pass is fine." | All 5 gates apply regardless of urgency. Shorter retro, not weaker filtering. |
| "The user asked about this topic, so I should include whatever I find." | User requests do not override privacy gates. Note the topic exists but details are in private sources. |
| "I only have GitHub data but the user needs it now." | Label it `retro_partial`. Explicit coverage gaps. Never present partial data as complete. |
| "I can infer from the public reference to a private conversation." | Inference from public references to private content is still a leak. Include only explicit public statements. |
| "The doc is shared with the whole team." | Check the actual sharing list. Threshold is 3+ named viewers. |

## Reference files

| File | Contents |
|------|----------|
| [DATA-SOURCES.md](DATA-SOURCES.md) | How to query each source (GitHub, Slack, Jira, Docs, CI/CD), alias resolution, failure diagnosis |
| [PRIVACY.md](PRIVACY.md) | 5-gate privacy checklist, DM trail rule, audience-of-one rule, emergency stop |
| [FORMAT.md](FORMAT.md) | Retro document template, evidence file schema, formatting rules |
| [GOLDEN-RULES.md](GOLDEN-RULES.md) | Expanded rules with detection criteria, full counter-table |
| [INTEGRATION.md](INTEGRATION.md) | MCP tool requirements, degraded mode protocol, parallel agent strategy |
