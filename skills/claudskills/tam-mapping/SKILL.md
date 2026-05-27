---
name: tam-mapping
description: Build TAM databases from scratch using a 7-phase methodology (Source Discovery → Keyword Expansion → Config → Collection → Dedup → Exclusion → Enrichment hand-off). Triggers "tam map", "build tam", "total addressable market", "scrape industry", "map the market", "build a lead database", "venue partnerships tam", "labs tam", "residential tam", "installer tam". Entity-routed — Nites residential (Google Maps ZIP), Supply installer (SAM.gov + Houzz + state license dbs), Labs venue partnerships (Spider.cloud + AI Ark + Discolike + IcyPeas + BlitzAPI + Prospeo + MillionVerifier). Phase 4.5 cross-workspace EB exclusion is MANDATORY (HARD-FAIL on either workspace unreachable). Phase 5 enrichment is pluggable per ADR-008. Distinct from `list-building` (BC-2717 — assumes a TAM already exists via dbt audience views).
user-invocable: true
allowed-tools: mcp__plugin_marketing_salesforce__*, mcp__plugin_marketing_spider__*, mcp__plugin_marketing_aiark__*, mcp__plugin_marketing_discolike__*, mcp__emailbison-b2b__*, mcp__emailbison-personal__*, WebSearch, WebFetch, Read, Write, Bash
metadata:
  version: 0.1.0
  upstream: Revgrowth1/ai-gtm-workflows + Revgrowth1/tam-map@9f5c72e74b
  category: Outbound Lead Gen
---

# TAM Mapping

A BDR, RevOps operator, or marketing lead with a new motion has two failure modes: spend weeks hand-curating a TAM (slow, inconsistent, miss 30–60% of the market) or run enrichment on a list that's 20–40% already-contacted (waste credits + sender reputation). This skill is the third option — a 7-phase pipeline that constructs a deduped, exclusion-filtered, optionally enriched/tiered TAM CSV ready for `list-building` or `launch-campaign`.

Reference-build calibration anchors (upstream Revgrowth 02): roofing TAM 20K sendable at $15, coffee shop TAM 11K sendable. Use as Nites/Supply scale anchors. Labs-path reference example in `plugins/marketing/references/tam/examples/` (BC-5946).

Three entity routes:

- **Nites residential** — Google Maps ZIP scraping via WebSearch (absorbs Revgrowth 09 local-enrichment).
- **Supply installer** — SAM.gov federal contracts + Houzz + state license databases.
- **Labs venue partnerships** — full 8-provider stack from upstream `Revgrowth1/tam-map`: Spider.cloud crawl + AI Ark + Discolike + IcyPeas → BlitzAPI → Prospeo → MillionVerifier → tier delegation to `icp-scoring` rubric `abc`.

**Distinct from `list-building` (BC-2717):** that skill *consumes* a TAM (assumes a `brite-data-platform` dbt audience view exists). This skill *constructs* one when no audience view exists. If a vertical already has a dbt view, skip this skill and use list-building directly.

---

## Before Starting

**Check for product marketing context first.** If `docs/marketing-context.md` exists, read it for entity-specific ICP and voice context. If the file does not exist, fall through to the missing-file fallback below — **do not proceed with degraded inferred ICPs.** Source taxonomy (Phase 1) and ICP gating (Phase 7) both depend on entity-correct context.

### Entity detection

The skill builds a TAM for ONE Brite entity per invocation (Nites / Supply / Labs). Detection logic when `--entity` is not passed:

| State | Behavior |
|---|---|
| `marketing-context.md` exists with one entity populated | Use it. Print: `Using entity=<X> from marketing-context.md (override with --entity).` Proceed. |
| `marketing-context.md` exists with multiple entities populated | Call `AskUserQuestion` listing the populated entities; user picks one. |
| `marketing-context.md` missing | Call `AskUserQuestion` with three options: (1) Exit and instruct user to run `/marketing:product-marketing-context`, then re-invoke tam-mapping after the file lands (recommended — no in-session pause/resume per user feedback). (2) Pick an entity for this run only with inline `--entity <X>` and `--criteria-file <path>` (does not save context). (3) Cancel. |

### Vertical detection (Labs path)

| State | Behavior |
|---|---|
| `--vertical` matches a pre-loaded playbook | Lazy-load `plugins/marketing/references/vertical-playbooks/{vertical}.md`. 6 pre-loaded: `zoos`, `aquariums`, `casinos`, `hotels-resorts`, `ski-resorts`, `sports-stadiums`. |
| `--vertical` does NOT match a pre-loaded playbook | Treat as custom vertical. Require `--criteria-file <path>` (JSON ICP) OR prompt for inline ICP via `AskUserQuestion`. NEVER silently default. |

### Invocation flags

| Flag | Default | Notes |
|---|---|---|
| `--entity <X>` | (auto-detect) | One of `brite-nites`, `brite-supply`, `brite-labs`. |
| `--vertical <slug>` | (required for Labs; optional for Nites/Supply) | Slug for output dir + Labs playbook lookup. |
| `--criteria-file <path>` | (auto-loaded from playbook for Labs pre-loaded verticals) | JSON criteria; required for custom verticals. |
| `--output-dir <path>` | (auto-derived) | Nites/Supply: `docs/research/tam/{vertical}-{YYYY-MM-DD}/`. Labs: `docs/campaigns/labs/tam/{slug}/`. Path-traversal segments (`..`) and absolute paths outside the worktree root are rejected. |
| `--enrichment-provider <id>` | (read from `${user_config.enrichment_provider}`) | Override per-run. Enum: `blitz_waterfall | brite_cli | brite_mcp | skip` per [ADR-008](../../../../docs/decisions/008-tam-mapping-enrichment-pluggability.md). |
| `--max-records N` | (unset → cost gate fires) | When set and `N >= record count`, gate is skipped (caller pre-approved cost). When `N < record count`, skill stops and reports overflow — does NOT silently truncate. |
| `--resume` | (off) | Force resume from last completed phase based on output-dir file existence. Default behavior (no flag) auto-detects via Operational rule 2 file-existence check. |

### Source manifest + TAMConfig location

Both written to the resolved `--output-dir`:

- **Nites/Supply path:** `docs/research/tam/{vertical}-{YYYY-MM-DD}/{manifest.json,tam-config.json}`.
- **Labs path:** `docs/campaigns/labs/tam/{slug}/{icp.json,tam-config.json}`.

The skill writes; downstream consumers read.

### Enrichment-provider selection

Read in priority order (per [ADR-008](../../../../docs/decisions/008-tam-mapping-enrichment-pluggability.md) §Unset resolution order):

1. `--enrichment-provider <id>` flag if passed.
2. `${user_config.enrichment_provider}` from plugin.json `userConfig` if explicitly set.
3. **Auto-detect** (when both above are unset):
   1. Check for brite-enrichment MCP registration in the active session → use `brite_mcp`.
   2. Else check for brite-enrichment CLI at `$BRITE_DATA_PLATFORM/services/enrichment/cli.py` → use `brite_cli`.
   3. Else fall through to `blitz_waterfall`.
4. `skip` is never auto-selected; it must be passed explicitly.

The resolved provider is logged at skill invocation so the user sees which path ran (e.g., `[tam-mapping] enrichment_provider=blitz_waterfall (auto-detected; brite-enrichment MCP not registered, $BRITE_DATA_PLATFORM unset)`). See the canonical 4-row enum table in [§3 Phase 5](#phase-5--enrichment-hand-off-pluggable) for per-value implementation and fallback messages.

### Resume detection

Per Operational rule 2 (below), if `--output-dir` already exists with partial output, the skill detects the resume point via file existence in this stable order and continues from the next missing file:

1. `manifest.json` (Phase 1)
2. `tam-config.json` (Phase 2)
3. Per-source `businesses.csv` (Nites/Supply) OR `companies.jsonl` (Labs) (Phase 3)
4. `crawled.jsonl` (Labs only — Phase 3 spider sub-step)
5. `all_sources_deduped.csv` (Phase 4)
6. `net_new_leads.csv` (Nites/Supply) OR both `excluded.jsonl` AND `companies-net-new.jsonl` (Labs — both files required for Phase 4.5 to be considered complete) (Phase 4.5)
7. `enriched.jsonl` (Phase 5)
8. `verified.jsonl` (Labs only — Phase 6)
9. `verified-flat.csv` (Labs only — Phase 7 reshape; required by icp-scoring `abc` contract)
10. `tier-{a,b,c}.csv` + `catch-all.csv` (Labs only — Phase 7)

The skill NEVER restarts from Phase 1 when resume state exists. Stop the file-existence loop at the first missing file; do not check subsequent entries.

---

## Methodology

Adapted from [Revgrowth1/ai-gtm-workflows workflow 02 (MIT)](https://github.com/Revgrowth1/ai-gtm-workflows/tree/main/workflows/02-tam-mapping) for the 7-phase scaffolding, [workflow 09 (MIT)](https://github.com/Revgrowth1/ai-gtm-workflows/tree/main/workflows/09-local-enrichment) for the Nites Phase 3 Google Maps ZIP method, and [Revgrowth1/tam-map@9f5c72e74b (MIT)](https://github.com/Revgrowth1/tam-map) for the Labs-path 8-provider stack. Brite departures annotated inline as `# Brite departure: ...`. See `plugins/marketing/references/tam/UPSTREAM.md` (BC-5946) for per-file port attribution.

### Phase 1 — Source Discovery

Research every data source across **16 categories** (literal taxonomy, in order):

1. Government / regulatory
2. Federal contracts (SAM.gov)
3. Industry associations
4. Manufacturer / vendor directories
5. Company databases (IcyPeas)
6. Local / maps
7. Review platforms
8. Social platforms
9. Business directories
10. Awards / rankings
11. Job boards
12. Events / conferences
13. Investor / funding
14. Open data
15. Marketplace / aggregator
16. Academic / research

**Output:** `manifest.json` listing every researched source with `{name, type, url, category, est_record_count, access_method}`.

**Entity routing in this phase:**

- **Nites/Supply:** Use the Revgrowth 02 taxonomy + `plugins/marketing/references/research-processes/` (BC-5823) for source-discovery query templates.
- **Labs:** Adds AI Ark + Discolike + IcyPeas to the taxonomy (their MCPs feed directly into Phase 3 collection rather than producing a separate manifest entry).

**Open-tracking-OFF reminder.** Emit this verbatim string in Phase 1 output (sender-reputation rule):

```
OPEN-TRACKING DISABLED — sender-reputation rule, see §Brite Implementation → Architectural rules
```

### Phase 1.5 — Keyword Expansion

Discover adjacent keywords sharing the same TAM. Primary keyword alone often misses 30–60% of market.

**MANDATORY:** Use IcyPeas `free-count` queries before pulling. Counts are free; pulls cost credits. Query each candidate keyword for total result count; rank by count and adjacency to the primary; commit only the top 5–10 to Phase 3 collection.

Cross-keyword dedup happens later in Phase 4 (Tier 1 domain match catches duplicate companies surfaced by multiple keywords). This phase only expands the keyword set.

### Phase 2 — Config Generation

Build `TAMConfig` JSON from `manifest.json`. Schema:

```jsonc
{
  "vertical_name": "<string>",
  "entity": "brite-nites | brite-supply | brite-labs",
  "keywords": ["string", "..."],
  "naics_codes": ["6-digit-string", "..."],
  "sources": [
    { "name": "<string>", "type": "<string>", "config": { /* per-source */ } }
  ],
  "output_dir": "<string>",
  "enrichment_provider": "blitz_waterfall | brite_cli | brite_mcp | skip"
}
```

**`enrichment_provider` reads from `${user_config.enrichment_provider}` (ADR-008 §swap-path mechanics).** The skill never hardcodes the value. Override via `--enrichment-provider <id>` flag.

### Phase 3 — Collection (entity-routed)

Three sub-routes — pick the one matching `entity`:

#### 3a. Nites residential — Google Maps ZIP scraping

(absorbs Revgrowth workflow 09)

- Tool: `WebSearch` (NOT Serper — cost reason; WebSearch is in `allowed-tools`).
- Query template: `<keyword> "<city or ZIP>"` per ZIP per priority.
- Initial implementation: 100–500 priority ZIPs per campaign (acceptable trade-off vs full 40K-ZIP traversal; split out if needed for scale).
- Output: `{output_dir}/{source}/businesses.csv` per source.

#### 3b. Supply installer

- Tool: `WebSearch` + `WebFetch` for SAM.gov federal contracts, Houzz directory, state license databases.
- Query templates per source documented in `plugins/marketing/references/research-processes/` (BC-5823).
- Output: same unified `businesses.csv` schema.

#### 3c. Labs venue partnerships — 4-provider parallel discovery

Run in parallel; merge + dedup by domain at completion.

| Provider | Tool | Script reference | Pagination |
|---|---|---|---|
| Spider.cloud | `mcp__plugin_marketing_spider__*` | `plugins/marketing/scripts/tam-map/spider_crawl.py` | crawls homepage + `/about` + `/contact` |
| AI Ark | `mcp__plugin_marketing_aiark__*` | `plugins/marketing/scripts/tam-map/aiark_client.py` + `aiark-mcp.js` | paginated, no stated rate limit |
| Discolike | `mcp__plugin_marketing_discolike__*` | `plugins/marketing/scripts/tam-map/discolike_client.py` + `discolike-mcp.js` | offset-based, X-Total-Count header |
| IcyPeas | `Bash` → `python plugins/marketing/scripts/tam-map/icypeas_client.py --icp ./output/{slug}/icp.json` | (no MCP — script-only per BC-5946) | max 100/page |

Output:

- `companies.jsonl` — merged + deduped firmographic records.
- `crawled.jsonl` — Spider crawl results overlay (tech signals, summarized homepage content).

#### Unified `businesses.csv` schema (Nites/Supply)

| Column | Type | Required | Notes |
|---|---|---|---|
| `domain` | string | yes | Normalized lowercase, `www.` stripped |
| `company_name` | string | yes | Free-text |
| `state` | string | yes | 2-char US state code |
| `address` | string | no | Free-text |
| `city` | string | no | |
| `zip` | string | no | 5-digit |
| `phone` | string | no | Will be normalized in Phase 4 |
| `email` | string | no | Optional pre-enrichment |
| `industry` | string | no | |
| `employees` | integer | no | |
| `source` | string | yes | Which scraper produced this row |
| `source_url` | string | no | |

#### Labs `companies.jsonl` schema

`{ "domain": "...", "company_name": "...", "linkedin_url": "...", "geo": "...", "tech_signals": [...], "source": "spider|aiark|discolike|icypeas", ... }`. Per-provider columns vary; the merger normalizes shared keys (`domain`, `company_name`, `geo`, `source`); provider-specific keys preserved as namespaced (`spider_*`, `aiark_*`, etc.).

### Phase 4 — Dedup

3-tier algorithm (in order):

1. **Tier 1 — domain match.** Exact match on normalized domain (lowercase, strip `www.`, strip trailing `/`).
2. **Tier 2 — company name + state.** Token-set Jaccard ≥ 0.85 on company name + exact state match. Catches DBA aliases.
3. **Tier 3 — phone match.** Normalized phone (strip non-digits, last 10 digits). Catches franchise locations sharing a phone tree.

**Output:**

- `all_sources_deduped.csv` — deduped TAM.
- `dedup_stats.json` — per-tier reduction counts:
  ```jsonc
  {
    "input_rows": 12300,
    "tier_1_domain_dedup_removed": 1200,
    "tier_2_name_state_dedup_removed": 450,
    "tier_3_phone_dedup_removed": 80,
    "output_rows": 10570
  }
  ```

### Phase 4.5 — Exclusion (**MANDATORY — never skipped**)

> **Procedure mirrored by [list-building § Workflow 2](../list-building/SKILL.md) (BC-2717) for its Sources 2 + 3 (dbt audience CSV, manual CSV) paths. Keep in sync — when one changes, audit the other.**

> **HARD-FAIL rule.** If either Email Bison workspace is unreachable (auth failure, network timeout after 3 retries, missing token), the skill HALTS and reports which workspace failed. Does NOT silent-skip and DOES NOT proceed to Phase 5. Reason: Phase 5 enrichment costs real money (BlitzAPI + Prospeo + MillionVerifier per-record); running it on already-contacted leads wastes credits.

Steps:

1. **Availability checks (issue all 3 in parallel as a single tool-batch — ALL THREE MUST PASS — HARD-FAIL):**
   - `mcp__emailbison-b2b__get_active_workspace_info`.
   - `mcp__emailbison-personal__get_active_workspace_info`.
   - `mcp__plugin_marketing_salesforce__run_soql_query` with `SELECT Id FROM User LIMIT 1` (per `plugins/marketing/tools/integrations/salesforce.md` — `get_username` is NOT a valid liveness check).
2. Bulk pagination via `mcp__emailbison-b2b__list_leads` AND `mcp__emailbison-personal__list_leads`. Both workspaces.
3. Salesforce union query:
   ```sql
   SELECT Id, Email, Domain__c FROM Contact WHERE Domain__c IN (...)
   /* + */
   SELECT Id, Email, Domain__c FROM Lead WHERE Domain__c IN (...)
   ```
4. Merge into a domain-level exclusion set.
5. Filter `all_sources_deduped.csv` against exclusion set.

**Output:**

- Nites/Supply: `net_new_leads.csv`.
- Labs: `excluded.jsonl` (the rows that DID match exclusion are recorded for transparency; the surviving rows continue forward as `companies.jsonl` minus matches, written to a fresh `companies-net-new.jsonl`).
- Plus `exclusion_stats.json`:
  ```jsonc
  {
    "input_rows": 10570,
    "eb_b2b_excluded": 1900,
    "eb_personal_excluded": 320,
    "sf_contact_excluded": 850,
    "sf_lead_excluded": 280,
    "total_excluded": 3350,
    "output_rows": 7220,
    "exclusion_rate_pct": 31.7
  }
  ```

Typical exclusion rate: 20–40% (scoping doc cites 31.7% average).

### Phase 5 — Enrichment Hand-off (pluggable)

Pluggable per [ADR-008](../../../../docs/decisions/008-tam-mapping-enrichment-pluggability.md). Provider selection follows the resolution order in §Before Starting → Enrichment-provider selection.

| `enrichment_provider` | Implementation | Status |
|---|---|---|
| `blitz_waterfall` | Shells to `python plugins/marketing/scripts/tam-map/enrich_waterfall.py --in <input> --out enriched.jsonl` (BlitzAPI 5 req/s serialized, Prospeo fallback max 20 workers) | **Default. Production-ready.** |
| `brite_cli` | Shells to `services/enrichment/cli.py` in brite-data-platform | Pending repo wiring; falls through to `blitz_waterfall` if repo missing locally |
| `brite_mcp` | Calls `mcp__plugin_marketing_enrichment__*` (brite-enrichment MCP) | **Pending BC-5537/5538 GA.** Currently NOT in `allowed-tools`; falls through to `blitz_waterfall` with `pending BC-5537/5538 GA` message |
| `skip` | No enrichment — pass through unenriched | Opt-in for testing or for handing off to BC-2717 list-building (which has its own enrichment pre-flight) |

**Pre-flight (all providers):**

1. **Email-verification credit check.** Read MillionVerifier balance.
2. **Volume-vs-budget cost estimate** (Labs path uses BlitzAPI + Prospeo + MillionVerifier per-record costs):
   ```
   estimated enrichment cost: $X.XX for N records (BlitzAPI: $A, Prospeo: $B, MillionVerifier: $C)
   ```
   This verbatim string MUST appear in output before any enrichment call (grep test in evals).
3. **Cost gate.** Use `AskUserQuestion` to confirm BEFORE invocation if cost > $20 (configurable threshold per `--max-records` interaction; see §Before Starting).
4. **API availability** — read-only ping to each provider's auth endpoint.

**Adaptive email waterfall (within `blitz_waterfall`):**

- Sample 100–200 records. Run BlitzAPI → Prospeo waterfall on the sample. Measure hit rate.
- If sample hit rate < 30%, skill warns and asks user to confirm before committing the full waterfall.
- If sample hit rate ≥ 30%, proceed with the full list.

**Post-enrichment verification:**

- Keep records with verification status `valid`. Drop `unknown`, `error`, `disposable`, `invalid`.
- Output: `enriched.jsonl`.

> **Labs path note.** The `catch_all` boolean flag is produced downstream in Phase 6 (SMTP verify), not here — Phase 5 has no source of catch-all signal. Nites/Supply paths terminate after Phase 5 without the catch-all distinction; their downstream consumers (BC-2717 / BC-5826) handle SMTP verify on their own schedule.

**Pattern-based recovery anti-rule.** Do NOT try `info@<domain>`, `contact@<domain>`, `hello@<domain>` for single-location businesses. Upstream tested 10 patterns × 15,934 domains = 0 hits. Single-location TAMs (Nites Google Maps, many Supply local installers, many Labs venues) almost never use generic mailboxes.

**Entity routing exit:**

- **Nites/Supply:** Phase 5 is the final phase. Hand off to `list-building` (BC-2717) when further enrichment needed, or directly to `launch-campaign` (BC-5826).
- **Labs:** Continue to Phase 6.

### Phase 6 — SMTP Verify (**Labs only**)

> Nites/Supply paths skip this phase. Downstream consumers (BC-2717 or BC-5826) handle SMTP verification.

- Tool: `Bash` → `python plugins/marketing/scripts/tam-map/verify_smtp.py --in enriched.jsonl --out verified.jsonl`.
- Throughput: 160 req/sec (MillionVerifier rate limit).
- Filter result codes:
  - **Keep** code `1` (`valid`).
  - **Keep** code `2` (`catch_all`) — but flag with `catch_all=true` so Phase 7 can route them to a separate output file.
  - **Drop** codes `3`–`6` (`unknown`, `error`, `disposable`, `invalid`).
- Output: `verified.jsonl` with explicit `catch_all` boolean column.

**Catch-all isolation rule (non-negotiable).** `catch_all=true` rows are kept in `verified.jsonl` so Phase 7 can route them to a separate output file. They are NEVER mixed into the tier-A/B/C CSVs. This is a user-explicit requirement for the tam-map port.

### Phase 7 — Tier + Segment delegation (**Labs only**)

> Delegates to `icp-scoring` (BC-5831) with `--rubric abc`. tam-mapping does NOT run a classifier itself.

**Pre-tier filter — Operational rule 1 (No free-email providers in B2B output).** BEFORE delegation, filter `verified.jsonl` rows whose email domain is one of `gmail.com` / `yahoo.com` / `hotmail.com` / `outlook.com` / `icloud.com`. Route them to `personal-contacts.csv` for manual outreach. NEVER include them in tier-A/B/C CSVs.

**Reshape — JSONL → flat CSV with top-level `catch_all` (REQUIRED before delegation).** Per icp-scoring's `abc` delegation contract (BC-5831 SKILL.md § "Tam-mapping delegation contract"), the caller (this skill) owns the JSONL→CSV reshape. `verified.jsonl` from Phase 6 nests the catch-all flag under `record.smtp.catch_all`; icp-scoring `abc` requires a flat CSV with a top-level `catch_all` column and stops with `missing required column 'catch_all' for --rubric abc` if absent. Before invoking the delegation call below, write `verified-flat.csv` with these columns: `domain`, `company_name` (if present), `industry` (if present), `employees` (if present), `geography` (if present), `catch_all` (boolean, flattened from `smtp.catch_all`). Free-email rows already routed to `personal-contacts.csv` in the prior step are excluded from `verified-flat.csv`.

> **Note on the two icp-scoring upstream feeders.** `verified-flat.csv` (6 cols, this file) and list-building's `enriched_leads.csv` (16 cols, BC-2717) are deliberately different shapes. tam-mapping emits the *tier-classification-only* feeder (just what icp-scoring `abc` needs to score); list-building emits the *fully-enriched* feeder (also includes contact-level columns). Both satisfy icp-scoring's required column set; downstream consumers needing contact-level fields (e.g., `launch-campaign`'s post-icp-scoring step) MUST consume from list-building's `enriched_leads.csv`, not from this `verified-flat.csv`.

**Delegation call:**

```
icp-scoring \
  --rubric abc \
  --max-records <N> \
  --output-dir docs/campaigns/labs/tam/{slug}/ \
  --criteria-file docs/campaigns/labs/tam/{slug}/icp.json
```

icp-scoring reads `verified-flat.csv` from `--output-dir` as input. Per icp-scoring's `abc` mode contract, the prompt template is read verbatim from `plugins/marketing/references/tam/fit-scoring.md` — not inlined here. When upstream tam-map updates the prompt, we re-port to `fit-scoring.md` and both skills inherit.

**Returns:**

- `tier-a.csv` — strong-fit prospects.
- `tier-b.csv` — secondary-fit prospects.
- `tier-c.csv` — weak/exploratory-fit prospects.
- `catch-all.csv` — `catch_all=true` rows scored separately (per icp-scoring abc mode contract).
- `report.md` — counts, drop reasons, top firmographic patterns.

The 4-CSV split is the contract `launch-campaign` (BC-5826) and `list-building` (BC-2717) consume.

---

## Brite Implementation

### Tools this skill calls

Organized by phase + reason:

| What the skill needs to do | MCP server / tool | Repo or system | Reason (ADR / source) |
|---|---|---|---|
| Phase 3a Nites — scrape Google Maps ZIP | `WebSearch` | Public web | Revgrowth 09 + cost (no Serper) |
| Phase 3b Supply — federal contracts + dirs | `WebSearch` + `WebFetch` | SAM.gov, Houzz, state license dbs | Revgrowth 02 |
| Phase 3c Labs — web crawl | `mcp__plugin_marketing_spider__*` | Spider.cloud | tam-map upstream; registered BC-5947 |
| Phase 3c Labs — firmographic discovery | `mcp__plugin_marketing_aiark__*` | AI Ark | tam-map upstream; registered BC-5947 |
| Phase 3c Labs — lookalike expansion | `mcp__plugin_marketing_discolike__*` | Discolike | tam-map upstream; registered BC-5947 |
| Phase 3c Labs — keyword search | `Bash` → `icypeas_client.py` | IcyPeas | BC-5946 (script-only — no MCP wrapper) |
| Phase 4.5 — workspace 1 exclusion | `mcp__emailbison-b2b__list_leads` | Email Bison b2b workspace | ADR 2a (sole sequencer) |
| Phase 4.5 — workspace 2 exclusion | `mcp__emailbison-personal__list_leads` | Email Bison personal workspace | ADR 2a — two-workspace requirement (per BC-5832 scope) |
| Phase 4.5 — SF exclusion | `mcp__plugin_marketing_salesforce__run_soql_query` | brite-salesforce (production org) | ADR 2a (CRM SoR) |
| Phase 5 — enrichment (default) | `Bash` → `enrich_waterfall.py` | BlitzAPI + Prospeo | ADR-008 default `blitz_waterfall` |
| Phase 5 — enrichment (future swap) | `mcp__plugin_marketing_enrichment__*` | brite-enrichment | ADR-008 + BC-5537/5538 (NOT in `allowed-tools` until GA) |
| Phase 6 — SMTP verify (Labs) | `Bash` → `verify_smtp.py` | MillionVerifier | tam-map upstream |
| Phase 7 — tier delegation (Labs) | invoke `icp-scoring` skill | n/a (in-plugin delegation) | BC-5831 + tam-map-port-policy.md §4 |
| Cross-repo handbook reads | `Bash` → `gh api repos/Brite-Nites/handbook/contents/...` | Brite-Nites/handbook (private repo) | `reference_handbook_access.md` (Context7 doesn't resolve private repo) |

### Architectural rules that apply

- **MCP-cap exception ratified.** Marketing plugin runs 4 plugin-level MCPs today (`salesforce`, `spider`, `aiark`, `discolike`) — within the ~5–6 advisory cap. Per BC-5945 §1, measurement methodology applies on each addition. Do not remove MCPs to "fix" perceived capacity issues; verify startup-latency `< 2s` and context-budget `< 500 tokens` deltas vs clean baseline before adding more.
- **Open tracking OFF.** Per upstream tam-map self-check #2: trackers trash sender reputation. Reminder emitted in Phase 1 output (verbatim string above).
- **Phase 4.5 exclusion HARD-FAILS** if either workspace unreachable. See §3 Phase 4.5 — never silent-skip; never single-workspace fallback.
- **Catch-all isolation non-negotiable** (Labs path). `catch-all.csv` is ALWAYS separate from `tier-{a,b,c}.csv`. User-explicit requirement.
- **No free-email providers in B2B output** (Operational rule 1; Labs path). Filter `gmail` / `yahoo` / `hotmail` / `outlook` / `icloud` before Phase 7 tier delegation.
- **Incremental saves + resume from last completed phase** (Operational rule 2). Each phase writes its output before advancing. Resume detects via file-existence in stable order.

### Cross-skill boundaries

- **Owns:** TAM database construction. Source discovery. Keyword expansion. 3-tier dedup. Cross-workspace EB exclusion. Phase 5 hand-off orchestration. Entity-aware routing (Nites/Supply/Labs).
- **Receives from:** User invocation with `--entity` + `--vertical`. Optional `gtm-strategy` output for segment/ICP inputs.
- **Hands off to (entity-specific):**
  - **Nites/Supply** → `list-building` (BC-2717) when further enrichment needed, or directly to `launch-campaign` (BC-5826).
  - **Labs** → `icp-scoring` (BC-5831, Phase 7 delegation, `--rubric abc`) → `launch-campaign` (BC-5826) or `list-building` (BC-2717).
- **Does not own:**
  - Audience-view design in dbt → `brite-data-platform`.
  - Per-prospect enrichment beyond waterfall coverage → BC-2727.
  - List-to-campaign config → `launch-campaign`.
  - ICP scoring itself → delegated to `icp-scoring`.

---

## MCP Tool Reference

Workflows grouped by phase, not by server. See [`plugins/marketing/tools/integrations/`](../../tools/integrations/) for the integration guides per provider.

### Workflow 1 — Phase 3 Labs collection (parallel discovery)

1. **Availability checks (issue all 4 in parallel as a single tool-batch):**
   - `mcp__plugin_marketing_spider__spider_get_credits` — confirms auth + balance.
   - AI Ark MCP liveness (lightest tool — see `plugins/marketing/tools/integrations/ai-ark.md` for the canonical liveness call).
   - Discolike MCP liveness (see `plugins/marketing/tools/integrations/discolike.md`).
   - IcyPeas: a free `count` query against a stub keyword (the script `icypeas_client.py` does not currently expose a dedicated healthcheck flag — see `plugins/marketing/tools/integrations/icypeas.md` for the canonical free-count probe shape; if missing, file a follow-up to add `--healthcheck` to the script).
2. On any failure, stop and report which provider failed.
3. Run all 4 providers in parallel against the keyword set from Phase 1.5.
4. Merge JSONL outputs; dedup by domain inline (Tier 1 only — full 3-tier dedup happens in Phase 4).

### Workflow 2 — Phase 4.5 cross-workspace + SF exclusion

See [§3 Phase 4.5](#phase-45--exclusion-mandatory--never-skipped) for the full step list (5 steps: 3-probe availability check, dual-workspace `list_leads` pagination, SF Contact + Lead union SOQL, merge + filter, write `net_new_leads.csv` or `excluded.jsonl` + `exclusion_stats.json`). This Workflow entry exists to confirm tool routing — the canonical procedure is in §3 Phase 4.5.

### Workflow 3 — Phase 5 enrichment (provider-routed via Bash)

1. Resolve `enrichment_provider` per §Before Starting (priority: `--enrichment-provider` flag → `${user_config.enrichment_provider}` → `blitz_waterfall`).
2. Switch on enum per [§3 Phase 5 enum table](#phase-5--enrichment-hand-off-pluggable). The table is the canonical source for each provider's invocation, fallback message, and status.
3. **Cost gate** before invocation (see §3 Phase 5 — verbatim string + `AskUserQuestion` if > $20).

### Workflow 4 — Phase 6 SMTP verify (Labs)

1. `Bash` → `python plugins/marketing/scripts/tam-map/verify_smtp.py --in enriched.jsonl --out verified.jsonl`.
2. Filter result codes 1 + 2 (with explicit `catch_all` flag); drop 3–6.

### Workflow 5 — Phase 7 tier delegation (Labs)

1. **Pre-filter** `verified.jsonl` for free-email domains → `personal-contacts.csv` (Operational rule 1).
2. **Reshape** remaining `verified.jsonl` rows to `verified-flat.csv` with a top-level `catch_all` column (flattened from `smtp.catch_all`). icp-scoring `abc` requires flat CSV with `catch_all` as a top-level column per its delegation contract (BC-5831).
3. Invoke `icp-scoring` skill with `--rubric abc --max-records <N> --output-dir <slug-dir> --criteria-file <icp.json>`.
4. icp-scoring reads `verified-flat.csv` and the prompt template at `plugins/marketing/references/tam/fit-scoring.md` (single source of truth).
5. Returns 4 CSVs + `report.md`.

**MCP confirmation gates (out-of-scope reminders):**

- Email Bison `import_leads_to_campaign`, `resume_campaign`, `unsubscribe_lead`, `blacklist_lead`, `archive_campaign`, `enable_warmup`, `remove_email_from_blocklist`, `remove_domain_from_blocklist` — these all have MCP-level confirmation gates per the Email Bison integration guide. tam-mapping does NOT call these (handed off to launch-campaign).
- IcyPeas paid `find-companies` is preceded by free `count-companies` per anti-slop rule 2.

---

## Operational Runbook

### Task 1 — Brite Nites residential TAM build

**Preconditions:**

- `docs/marketing-context.md` exists and identifies entity `brite-nites`.
- `--vertical <slug>` chosen (e.g., `austin-municipalities`).
- Output dir auto-derived: `docs/research/tam/{vertical}-{YYYY-MM-DD}/`.

**Steps (Phases 1 → 5):**

1. Phase 1 source discovery → `manifest.json`.
2. Phase 1.5 IcyPeas free-count keyword expansion.
3. Phase 2 TAMConfig generation (writes `tam-config.json` with `enrichment_provider` from userConfig).
4. Phase 3a Google Maps ZIP scraping via `WebSearch` → per-source `businesses.csv`.
5. Phase 4 dedup → `all_sources_deduped.csv` + `dedup_stats.json`.
6. **Phase 4.5 exclusion (MANDATORY — both EB workspaces + SF) → `net_new_leads.csv` + `exclusion_stats.json`.**
7. Phase 5 enrichment via resolved provider → `enriched.jsonl` (or `--enrichment-provider skip` to pass through).
8. **Hand off** to `list-building` (BC-2717) or directly to `launch-campaign` (BC-5826).

**Expected output dir contents:**

```
docs/research/tam/{vertical}-{YYYY-MM-DD}/
├── manifest.json
├── tam-config.json
├── {source}/businesses.csv     # one per Phase 3 scraper
├── all_sources_deduped.csv
├── dedup_stats.json
├── net_new_leads.csv
├── exclusion_stats.json
└── enriched.jsonl              # if Phase 5 ran
```

**Error handling:**

- Any MCP availability failure halts.
- EB workspace unreachable → HARD-FAIL with which workspace failed.
- Phase 5 cost > $20 without `--max-records` pre-approval → `AskUserQuestion` confirmation gate.

### Task 2 — Brite Supply installer TAM build

**Preconditions:**

- `marketing-context.md` exists with `brite-supply` entity populated.
- `--vertical <slug>` chosen (e.g., `landscape-installers-tx`).

**Steps:** mirror Task 1 but Phase 3b uses SAM.gov + Houzz + state license databases (`WebSearch` + `WebFetch`) instead of Google Maps. Phases 4, 4.5, 5 unchanged.

**Hand off to** BC-2717 (typical for Supply because installer enrichment often needs further per-prospect work).

### Task 3 — Brite Labs venue partnerships TAM build (full tam-map path, all 7 phases)

**Preconditions:**

- `marketing-context.md` exists with `brite-labs` entity populated.
- `--vertical` matches one of the 6 pre-loaded playbooks (`zoos`, `aquariums`, `casinos`, `hotels-resorts`, `ski-resorts`, `sports-stadiums`) OR user provides `--criteria-file`.
- Output dir auto-derived: `docs/campaigns/labs/tam/{slug}/`.
- BOTH EB workspaces must be reachable (HARD-FAIL otherwise).

**Steps (Phases 1 → 7):**

1. Phase 1 source discovery — Labs taxonomy adds AI Ark + Discolike + IcyPeas.
2. Phase 1.5 keyword expansion (IcyPeas free-count).
3. Phase 2 TAMConfig generation; lazy-load `plugins/marketing/references/vertical-playbooks/{vertical}.md` → write `icp.json`.
4. Phase 3c parallel discovery (Spider + AI Ark + Discolike + IcyPeas) → `companies.jsonl` + `crawled.jsonl`.
5. Phase 4 dedup → `all_sources_deduped.csv` (also kept as `.jsonl` for Labs continuity).
6. **Phase 4.5 exclusion (MANDATORY) → `excluded.jsonl` + `companies-net-new.jsonl`.**
7. **Cost gate** + Phase 5 enrichment → `enriched.jsonl`.
8. Phase 6 SMTP verify → `verified.jsonl`.
9. **Free-email filter** (Operational rule 1) → `personal-contacts.csv` separated.
10. **JSONL→CSV reshape** → `verified-flat.csv` with top-level `catch_all` column (per icp-scoring `abc` contract).
11. Phase 7 tier delegation to `icp-scoring --rubric abc` → `tier-a.csv`, `tier-b.csv`, `tier-c.csv`, `catch-all.csv`, `report.md`.
12. **Hand off** to `launch-campaign` (BC-5826) or `list-building` (BC-2717).

**Expected output dir contents:**

```
docs/campaigns/labs/tam/{slug}/
├── icp.json
├── tam-config.json
├── companies.jsonl
├── crawled.jsonl
├── all_sources_deduped.csv (or .jsonl)
├── excluded.jsonl
├── companies-net-new.jsonl
├── enriched.jsonl
├── verified.jsonl
├── personal-contacts.csv
├── verified-flat.csv
├── tier-a.csv
├── tier-b.csv
├── tier-c.csv
├── catch-all.csv
└── report.md
```

### Task 4 — Resume an interrupted run

**Preconditions:**

- A previous run's output directory exists with partial output.

**Steps:**

1. Skill reads `--output-dir` and runs the file-existence check in stable order (see §Before Starting → Resume detection).
2. Resume from the first missing file's phase.
3. **NEVER restart from Phase 1.**
4. If `--resume` flag is passed, force resume even when state could be ambiguous (e.g., partial JSONL writes — the skill validates the last record line and resumes from the next).

**Expected output:** pipeline continues; no duplicate work; final output dir contents match Task 1/2/3 expectations for the active entity.

---

## Health Scoring Rubric

| Score | Criteria |
|------:|----------|
| 10 | Runs the entity-correct phase route end-to-end. Cites all 16 source categories in Phase 1 manifest. Phase 4.5 exclusion runs against BOTH EB workspaces + SF, HARD-FAILS on missing token. Cost gate fires before Phase 5. Open-tracking-OFF reminder emitted verbatim. Catch-all isolation enforced (Labs). Free-email filter applied (Labs). Resume detection works without restarting from Phase 1. References ADR-008 for enrichment pluggability. Cross-links to BC-2717 / BC-5826 / BC-5831 are present. |
| 7-9 | Same as 10 but skips one verification — e.g. forgets the open-tracking reminder, OR skips the cost gate, OR runs Phase 4.5 against only one EB workspace. Output is functional but missing one architectural rule. |
| 4-6 | Runs the phases but skips Phase 4.5 entirely OR mixes catch-all into tier CSVs OR uses pattern-based email recovery on single-location businesses OR restarts from Phase 1 on resume. Functional but violates a core rule. |
| 1-3 | Hallucinates source taxonomy. Calls unregistered MCP servers (e.g., `mcp__plugin_marketing_enrichment__*` before BC-5538 GA). Skips IcyPeas free-count and pulls credits blind. Outputs `gmail`/`yahoo` addresses in tier CSVs. Hard-fails silently. |

---

## Anti-Slop Guardrails

- Do not generate generic marketing jargon ("synergy", "leverage", "best-in-class").
- Do not fabricate statistics, case studies, or testimonials — always attribute to a source.
- Do not produce output that ignores `docs/marketing-context.md`.
- Do not recommend tools the plugin does not have access to (no hallucinated MCP servers, no assumed local clones).
- **Always run Phase 4.5 exclusion against BOTH EB workspaces + SF.** Never skip — costs real money to enrich already-contacted leads.
- **Always run IcyPeas `count` queries before paid `find-companies`.** Counts are free; pulls cost credits.
- **Always emit unified `businesses.csv` schema from every Phase 3 Nites/Supply scraper** (and the JSONL equivalent for Labs). Schema variance breaks Phase 4 dedup.
- **Always dedup before enrichment.** Never enrich a pre-dedup TAM.
- **Never use pattern-based email recovery (`info@`, `contact@`, `hello@`) on single-location businesses.** Upstream tested 10 patterns × 15,934 domains = 0 hits.
- **Never mix catch-all rows into tier-A/B/C.csv (Labs path).** `catch-all.csv` is ALWAYS a separate file. User-explicit requirement.
- **Never include free-email-provider rows (`gmail.com`, `yahoo.com`, `hotmail.com`, `outlook.com`, `icloud.com`) in tier-A/B/C.csv (Labs path).** Sender-reputation rule. Route to `personal-contacts.csv` instead.

---

## Behavioral Tests

### Tier 1 — Free assertions (5)

1. Given user invokes "build a TAM for Nites residential in the Austin metro", output must walk through Phases 1, 1.5, 2, 3, 4, 4.5, 5 and explicitly skip Phases 6 + 7 (Labs-only).
2. Given user invokes "build a Labs zoos TAM", output must walk all 7 phases and explicitly cite the lazy-load step `plugins/marketing/references/vertical-playbooks/zoos.md`.
3. Output sample tier-A/B/C rows must NOT contain free-email domains (`gmail.com`, `yahoo.com`, `hotmail.com`, `outlook.com`, `icloud.com`).
4. Given a vertical with no playbook (e.g., "build a Labs TAM for breweries"), output must accept `--criteria-file` or interactive ICP entry as fallback — NOT silently fail.
5. Given a resume scenario ("the last run died at Phase 5"), output must detect the resume point from file-existence and NOT restart from Phase 1.

### Tier 2 — Tool-assisted (7)

6. If `docs/marketing-context.md` exists, output must reference Brite entity from that file in the Phase 1 manifest.
7. If `mcp__emailbison-b2b__get_active_workspace_info` returns auth failure, skill HARD-FAILS at Phase 4.5 — does NOT proceed to Phase 5.
8. If `mcp__emailbison-personal__get_active_workspace_info` returns auth failure (with b2b OK), skill STILL HARD-FAILS at Phase 4.5 — both must succeed.
9. If `${user_config.enrichment_provider}` is `brite_mcp` and the MCP is unavailable, output emits "pending BC-5537/5538 GA" message and falls through to `blitz_waterfall`.
10. If `${user_config.enrichment_provider}` is `skip`, Phase 5 short-circuits; downstream Phases 6+7 still run for Labs.
11. Open-tracking-OFF reminder appears as verbatim string `OPEN-TRACKING DISABLED` in Phase 1 output (grep test in evals).
12. Cost-estimate string `estimated enrichment cost:` appears in output before any Phase 5 enrichment call (grep test in evals).
