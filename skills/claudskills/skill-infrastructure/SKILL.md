---
name: skill-infrastructure
description: "Use when designing the deterministic health-tooling layer for a skill library, diagnosing why an existing library is decaying invisibly, deciding which categories of automated check to add (inventory, protocol consistency, conflict detection, routing health, drift sentinel), debugging eval-threshold violations across many skills at once, or auditing whether a skill-system has the safety nets a production library needs. Covers the five categories of skill-health tooling, the library-as-database mental model, eval quality patterns (minimum thresholds, contradiction-check pattern, negative-expectation requirement), maintenance workflows triggered by batch skill changes, and the anti-patterns that cause skill libraries to decay until agents loading them get worse over time. Do NOT use for authoring an individual SKILL.md (use `skill-scaffold`), for running the conformance audit on the Skill Graph repo itself (use `graph-audit`), or for general lint rule selection across a codebase (use `lint-overlay`)."
license: MIT
compatibility: "Library- and harness-agnostic. Patterns apply to any skill-style library (Skill Graph, Claude skills, Cursor rules, custom in-house skill systems). Specific tool names in this skill (skill-lint, generate-manifest, routing-eval, drift-sentinel) are concrete examples from the Skill Graph reference implementation -- substitute your library's equivalents."
allowed-tools: Read Grep Bash Edit Write
metadata:
  schema_version: "4"
  version: "1.0.0"
  type: capability
  category: knowledge
  domain: skill-system/health
  scope: portable
  owner: skill-graph-maintainer
  freshness: "2026-05-13"
  drift_check: "{\"last_verified\":\"2026-05-13\",\"truth_source_hashes\":{\"package.json\":\"7a3410a004aea78a2065092e289c0f3cf3c082298804dda6c5829eff22c14b62\",\"bin/skill-graph.js\":\"113a1e01ac7276ac1b5d77a1c32e35a73113da93fc33cfd0caf6db842d2d679f\",\"scripts/skill-lint.js\":\"3a78f75f8921542b91dc619cd41bde29bf379de3c16bdcf3653c854ecbe9fa29\",\"scripts/lib/roots.js\":\"e742efa57b6c33ff1c87034b16a689d1499f6d53c1e6b740f3e9783db7fd557f\",\"scripts/check-protocol-consistency.js\":\"0ff39406d36e7a9e51c176f657f4f426d8bd5a3fe6411d28b9e9a93dc7d89f29\",\"scripts/generate-manifest.js\":\"9d7bbbdae440fdb1763d61ffa7bda10c9efae92359d1c2139d0e971582d59e0e\",\"scripts/skill-graph-drift.js\":\"6b69c25b59c16b477a377e5ab40adb6ff30f72d5a12947772053a6cd16b1f409\",\"scripts/skill-overlap.js\":\"ed642cbc677cc76ec1321300b37d6752337b6b5541c7a9f558fd315d6f934e4b\",\"scripts/skill-graph-routing-eval.js\":\"fffac2858863662bde6bc54c56bb77a219ae93f626e0c8d5886566f998181deb\",\"docs/manifest-field-mapping.md\":\"aca0b7f2d4631be24a3e7daed1a1d207b488f253164a7d514b9db7af21c6177f\"}}"
  eval_artifacts: planned
  eval_state: unverified
  routing_eval: absent
  stability: experimental
  keywords: "[\"skill library health\",\"skill system tooling\",\"skill library decay\",\"skill library maintenance\",\"skill census\",\"skill inventory\",\"frontmatter validation\",\"imperative conflict\",\"skill overlap detection\",\"skill conflict\",\"routing gap\",\"routing miss\",\"routing health\",\"eval threshold\",\"eval minimum\",\"contradiction check\",\"negative expectation\",\"drift sentinel\",\"truth source hash\",\"mirror parity\",\"skill graph health\",\"production skill library\",\"skill linter\",\"skill quality gate\",\"phantom ref\"]"
  examples: "[\"our skill library is growing and we're getting silent decay — eval counts dropping, conflicts emerging — what tooling should we add?\",\"two of our skills give opposite instructions for the same function — how do we detect this automatically?\",\"we keep getting skill-router misses on real user queries — how do we surface and close routing gaps?\",\"design a health-check pipeline for a 200-skill library that runs in CI\",\"what's a reasonable minimum eval count per skill, and how do we enforce it?\",\"our skill mirror in `.claude/skills` keeps drifting from the source — what's the parity check?\",\"we want to add a contradiction-check eval pattern — what does it look like and when do we use it?\",\"skill-overlap-detector flagged 12 imperative conflicts — how do we triage which to fix vs suppress?\"]"
  anti_examples: "[\"scaffold a new SKILL.md for our team's deploy procedure\",\"audit this Skill Graph repo for schema conformance and dangling relation targets\",\"the manifest sample drifted from the generator — find the mismatch\",\"improve this prompt's wording to get better outputs\",\"review this AI-generated PR for correctness\",\"set up ESLint for our TypeScript repo\",\"draft an architecture note explaining why we chose Postgres\"]"
  relations: "{\"boundary\":[{\"skill\":\"skill-scaffold\",\"reason\":\"skill-scaffold owns authoring methodology for one new SKILL.md; skill-infrastructure owns the deterministic health-tooling layer that watches the entire library after authoring\"},{\"skill\":\"graph-audit\",\"reason\":\"graph-audit is the operational audit of one specific library (Skill Graph), scope: codebase; skill-infrastructure is the portable discipline of designing health tooling for any skill library\"},{\"skill\":\"lint-overlay\",\"reason\":\"lint-overlay covers lint-rule selection and gate placement for general codebases; skill-infrastructure covers the skill-system-specific tooling category that includes lint but extends to overlap, routing-gap, drift, and mirror-parity\"},{\"skill\":\"documentation\",\"reason\":\"documentation produces durable prose for human readers; skill-infrastructure designs the deterministic checks that no human reads unless violated\"}],\"related\":[\"skill-scaffold\",\"graph-audit\",\"testing-strategy\"],\"verify_with\":[\"testing-strategy\",\"code-review\"]}"
  grounding: "{\"domain_object\":\"Deterministic health tooling for Skill Graph libraries\",\"grounding_mode\":\"hybrid\",\"truth_sources\":[\"package.json\",\"bin/skill-graph.js\",\"scripts/skill-lint.js\",\"scripts/lib/roots.js\",\"scripts/check-protocol-consistency.js\",\"scripts/generate-manifest.js\",\"scripts/skill-graph-drift.js\",\"scripts/skill-overlap.js\",\"scripts/skill-graph-routing-eval.js\",\"docs/manifest-field-mapping.md\"],\"failure_modes\":[\"health_tooling_categories_missing_from_ci\",\"protocol_mapping_drift\",\"eval_thresholds_become_self_attested\",\"overlap_or_drift_checks_not_run_after_batch_changes\"],\"evidence_priority\":\"repo_code_first\"}"
  portability: "{\"readiness\":\"scripted\",\"targets\":[\"skill-md\"]}"
  lifecycle: "{\"stale_after_days\":90,\"review_cadence\":\"quarterly\"}"
  skill_graph_source_repo: "https://github.com/jacob-balslev/skill-graph"
  skill_graph_protocol: Skill Metadata Protocol v3
  skill_graph_project: Skill Graph
  skill_graph_canonical_skill: skills/skill-infrastructure/SKILL.md
---

# Skill Infrastructure

## Coverage

- The library-as-database mental model: skill-infrastructure as the linter, integrity checker, and query planner for a SKILL.md library
- Why deterministic, zero-LLM tooling is mandatory for skill libraries (trustworthy enough for CI gates; LLM-based health checks are circular)
- The five categories of skill-health tooling: (1) inventory and frontmatter validation, (2) protocol consistency, (3) conflict detection (overlap, imperative, code duplication, heading overlap), (4) routing health (gap analysis, miss tracking), (5) drift detection (truth-source hashing, mirror parity)
- Eval quality patterns: minimum eval threshold per skill, the contradiction-check eval type, the negative-expectation requirement, valid eval-type taxonomy
- Imperative conflict detection: the same-target-opposite-polarity rule, three-check false-positive suppression, when conflicts indicate scope-tightening vs merging
- Routing gap analysis: how to read a "routing-misses" log, how to distinguish keyword gaps from skill content gaps, signal-hygiene rules to suppress noise
- Maintenance workflows: when to run a full health check, the order in which to run the categories, what to fix before what
- Anti-patterns that cause invisible decay: dirty-tree manifest writes, deletion-as-conflict-resolution, eval-renumbering during cleanup, scope misuse to mask threshold violations
- The verification gate before any batch skill commit: every category clean, every new skill meets eval minimums, every routing change is reflected in the manifest
- Package and workspace-root integrity: the npm CLI entrypoint must dispatch to the same scripts as local development while resolving schemas from the package and skills/manifests from the caller workspace

## Philosophy

A skill library is only as useful as its worst skill. When agents load stale, conflicting, poorly-routed, or mirror-drifted skills, they get *worse* at tasks — not better. A skill library at scale (50+, certainly 200+) decays invisibly: eval counts drift below minimums, keyword maps miss whole product areas, mirror copies fall out of sync, and two skills start giving opposite instructions for the same function.

The infrastructure exists to catch that decay deterministically, with **zero LLM calls**. Every health check reads files, parses structure, and computes — it does not reason, infer, or hallucinate. That makes the output trustworthy enough to use in CI-style gates. An LLM-based health check is circular: the same probabilistic component that produces the skill library cannot reliably grade its own output.

> If the skill library is a codebase, skill-infrastructure is its combined linter, type-checker, and dead-code detector — always-on, zero-model, CI-safe.

The maintenance commitment is: run a full health check after any batch skill work, fix threshold violations before they reach the gate, and document conflicts before the agents loading those skills are affected.

## The Library-as-Database Mental Model

Treat the skill library as a database and skill-infrastructure as its query planner, integrity checker, and migration-safety net combined.

| Database concept | Skill-library equivalent |
|---|---|
| Schema | SKILL.md frontmatter schema (JSON Schema or equivalent) |
| Constraints | Required fields, eval thresholds, valid enum values |
| Foreign keys | `relations.boundary[]`, `relations.related[]` targets — must point at real skills |
| Indexes | Manifest, routing-keyword map, path-glob inverse index |
| Integrity check | Protocol-consistency tooling (cross-schema parity, sample correctness, generated-field parity) |
| Query planner | Skill router (matches user prompt → skill activation) |
| Replication lag | Mirror parity (`.claude/skills`, `.agents/skills`, harness-specific copies) |
| Dead code | Skills with broken relation targets, phantom routing entries |

Every script in this domain reads files and computes — it does not reason. Output is deterministic, reproducible, and safe to embed in CI gates.

## The Five Categories of Skill-Health Tooling

A production skill library needs all five. Missing any one allows a class of decay through.

### 1. Inventory and Frontmatter Validation

Walks the skill tree, parses every SKILL.md's frontmatter, and validates against the schema.

| Check | Why it matters |
|---|---|
| Required fields present (`name`, `description`, `version`, `type`, `scope`, `owner`, `freshness`) | Missing fields break the manifest generator and the router |
| Field-value enums valid (`type`, `scope`, `eval_state`) | Drift in valid values leaks invalid skills into routing |
| Description-length and quality (≥ 100 chars, contains "Use when X / Do NOT use for Y") | Short or vague descriptions degrade router precision |
| Eval-count per skill (warn at < 7, error at < 3 for non-reference skills) | Under-evaluated skills regress quality undetected |
| Reference-path resolution (every `references/X.md` cited in frontmatter actually exists) | Dangling references mislead the agent at activation time |
| Scope-grounding consistency (`scope: codebase` requires populated `grounding` block) | Codebase claims without grounding can hallucinate file paths |

**Reference implementation:** `scripts/skill-lint.js` in this repo runs T5 per-skill lint covering most of these.

### 2. Protocol Consistency

Cross-checks that the schema, generator, sample manifest, and field-reference docs all agree.

| Check | Failure mode if missing |
|---|---|
| Cross-schema parity (versioned schemas describe the same fields) | Schema bumps silently drop fields |
| Authored-to-generated parity (frontmatter fields match what the generator emits) | Generator drift breaks downstream consumers |
| Sample manifest matches generator output | Sample stales as skills are added |
| Generated field-reference matches authored field-reference | Documentation drift hides field changes |
| Truth invariants on example evals (e.g. truth-source line ranges still resolve) | Eval expectations point at non-existent code |

**Reference implementation:** `scripts/check-protocol-consistency.js` runs C1–C7 protocol checks.

### 3. Conflict Detection

Pairwise comparison across all active skills to surface duplication, contradiction, and structural overlap.

| Dimension | Method | Signal |
|---|---|---|
| Description similarity | Jaccard on word bigrams | > 0.4 = potential duplicate |
| Heading overlap | Shared H2/H3 headings excluding boilerplate | High overlap = structural duplication |
| Code duplication | Identical fenced code blocks > 30 chars | Copy-paste anti-pattern |
| Imperative conflicts | Same target, opposite polarity (ALWAYS vs NEVER) | Agents get contradictory instructions |

**Imperative extraction patterns:**

- Positive: `\b(?:always|must|required|mandatory)\b\s+(.{10,80})/gi`, `\buse\s+(.{5,60})\s+(?:for|when|instead)/gi`
- Negative: `\b(?:never|do\s+not|don't|must\s+not|prohibited)\b\s+(.{10,80})/gi`, `\bdo\s+NOT\s+use\s+(.{5,60})/gi`

**Three-check false-positive suppression** for the most common phantom-conflict sources (e.g. `Do NOT use X` matching as positive `use X`):

1. **Lookbehind check** — if `not`, `never`, `don't`, or `cannot` appears in the 20 characters before a positive match, suppress it
2. **Within-match check** — if `not` appears between the start of the match and the target identifier (extracted via backticks), suppress it
3. **Same-line dedup** — if the target was already extracted as a negative on the current line, suppress any positive extraction for that target

**When a conflict is real vs spurious:**

| Conflict type | Resolution |
|---|---|
| Phantom ref | Routing config maps to a non-existent skill — delete the stale entry |
| Code duplication | One skill owns the example; the other links to it |
| Heading overlap | Acceptable for structural templates; review only the differentiating content |
| Imperative conflict (real) | Scope the instructions more precisely (`always use X` → `always use X in app code`); rarely merge skills |
| Imperative conflict (spurious) | Un-backticking an identifier hides a real boundary ambiguity — fix the skill wording instead |

### 4. Routing Health

Reads the routing-miss log and the routing config to identify where the keyword map fails.

| Input | Purpose |
|---|---|
| Routing-misses log (queries that matched zero skills) | Surface keyword gaps — words users typed that never reached a skill |
| Eval-history log with `failure_category` | Surface skills failing for reasons routing can fix (`skill_not_activated`, `wrong_answer`) |
| Active routing config (`keywordMap`, `labelMap`) | Authoritative truth for what currently routes |

**Output sections:**

1. **Keyword gaps** — words appearing in routing-misses but absent from the active keyword map, sorted by frequency
2. **Eval failure breakdown** — skills with 2+ failures, grouped by failure category
3. **Suggested actions** — `add_keyword` for frequent gaps; `improve_skill` for skills failing for content reasons

**Signal hygiene rules** (suppress these from the suggestion list):

- Low-signal tokens (`v`, `v4`, `skill`, `start`, `events`, `daily`, `log`, `status`, `health`)
- Single-word misses already covered by an existing multi-word phrase (e.g. `error` should not surface if `error recovery` is already mapped)
- Stale historical misses where the full query already routes under the current config
- Synthetic no-match probes used to verify the router's miss path
- Bundle entries (only direct `keywordMap` entries participate in free-text matching)

**Reference implementation:** the routing harness (`scripts/skill-graph-routing-eval.js` in this repo) provides the negative case — verifying that a skill's authored `examples` actually route to it. A real routing-gap report is the symmetric positive case (verifying that real user prompts reach a skill).

### 5. Drift Detection

Detects when the *world the skill claims* has changed without the skill being updated.

| Drift type | Detection |
|---|---|
| Truth-source drift | `drift_check.truth_source_hashes` records SHA-256 of cited files; rerun hashes; mismatch = drift |
| Mirror parity | Hash every `<library>/skills/<name>/SKILL.md` and every `<harness-mirror>/skills/<name>/SKILL.md`; mismatch = drift |
| Stale `freshness` date | Skill has not been touched in > `lifecycle.stale_after_days`; surface for review |
| Tracker → skill drift | Issue tracker references a skill that no longer exists; or skill references a closed issue |

**Reference implementation:** `scripts/skill-graph-drift.js` in this repo records and verifies truth-source hashes against the live files.

## Eval Quality Patterns

### The minimum-threshold rule

Every active skill should have at least 7 evals. Most healthy skills carry 9–15 covering happy paths, edge cases, anti-patterns, and contradiction checks. The threshold is a *floor*, not a goal.

**Recommended enforcement:**

- **Error** if `eval_count < 3` (or **warn** for `scope: reference` skills, where the file is documentation more than testable behaviour)
- **Warn** if `eval_count < 7`

Below 7, the skill is statistically under-tested. Below 3, it is effectively un-evaluated.

### The contradiction-check eval type

A `contradiction-check` eval tests that the agent correctly handles a documented exception or boundary condition that a simpler reading of the skill would mishandle. Format:

```json
{
  "id": 5,
  "type": "contradiction-check",
  "grounding": "repo-specific",
  "difficulty": "adversarial",
  "prompt": "Skill A says always use the scoped fetcher. One service uses the unscoped fetcher with an inline comment. Is this wrong?",
  "expected_output": "Not wrong — the unscoped fetcher with an inline justification comment is the documented exception for system-level reads.",
  "expectations": [
    "Correctly identifies the documented exception from the skill's anti-patterns table",
    "Does NOT flag the usage as a bug without reading the inline comment",
    "Distinguishes a system-level exception from a regular violation in application code"
  ]
}
```

Use a contradiction-check when:

- A skill has a documented exception that overrides the general rule
- Two adjacent skills appear to contradict each other but actually operate in different scopes
- A historical false positive or conflict was resolved and the resolution is non-obvious

### The negative-expectation requirement

Every eval case with an `expectations` array must include at least one expectation containing `does not`, `never`, `must not`, `should not`, or `do not`. Without this, evals become pure happy-path tests and miss the failure modes that motivated the skill.

**Recommended enforcement:** the inventory tool flags any eval missing this pattern in a `missingNegativeEvalIds` field of its report.

### Valid eval types

| Type | When to use |
|---|---|
| `knowledge` | Tests a factual claim or pattern from the skill |
| `contradiction-check` | Tests documented exceptions and boundary conditions |
| `browser` | Tests a browser-executable interaction (requires running server) |
| `edge-case` | Tests unusual inputs or rare conditions |
| `business-model` | Tests domain-specific logic (e.g. SaaS billing rules, e-commerce fulfilment) |
| `negative` | Tests refusal or correct non-action |

## Maintenance Workflows

### The full health check sequence

Run after any batch skill work — creating ≥ 3 skills, changing routing config, or modifying skill content across multiple files. Order matters:

```bash
# 1. Inventory snapshot — discover invalid frontmatter, missing fields, broken refs
<inventory tool>

# 2. Protocol consistency — cross-schema, manifest, generated-doc parity
<protocol-consistency tool>

# 3. Conflict detection — overlap, imperatives, code duplication
<conflict tool> --conflicts

# 4. Routing gaps (last 7 days)
<routing-gap tool> --since 7d

# 5. Drift sentinel — truth-source hashes, mirror parity
<drift tool>

# 6. Regenerate manifest + index from the now-clean tree
<manifest generator> --write
```

Review the output of steps 1–5 before running step 6. The manifest and index should reflect a clean state — never write a manifest from a dirty tree.

### Adding evals to an existing skill

1. Read the skill's existing eval set
2. Identify gaps: are all eval types represented? Are there contradiction-checks for documented exceptions?
3. Draft new cases with `id`, `prompt`, `expected_output`, `expectations`, `type`, `grounding`, `difficulty`
4. Ensure every new case has at least one `does not / never / must not` expectation
5. **Append** to the eval array — never renumber existing IDs (eval-history logs reference numeric IDs)
6. Re-run the inventory tool and verify the skill no longer appears in `belowMinimum` or `missingNegativeEvalIds`

### Triaging imperative conflicts

1. Run the conflict tool with `--conflicts --json` to get the structured list
2. For each conflict, identify which skill's instruction is more precise or more scoped
3. Resolve by *narrowing scope*, not by deleting the instruction:
   - "Use X" → "Use X in app code" (narrower)
   - "Always use X" → "Always use X for tenant-scoped data" (specific)
   - Move the negative instruction to an anti-patterns table row that does not start with "Use"
   - Add an inline qualifier (e.g. `// system: <reason>`) that the detector can distinguish
4. Re-run `--conflicts` to confirm the conflict is gone
5. Document the resolution in a conflict log so future audits know it was deliberate

### Fixing invalid frontmatter

| Problem | Fix |
|---|---|
| `scope` field absent | Add the correct value (`portable` / `reference` / `codebase`) |
| `drift_check.last_verified` absent or stale | Add or update to today's ISO date |
| `eval_artifacts` absent | Set to `present` if eval files exist, `planned` if intended, `none` otherwise |
| `keywords` empty or short | Add 5–15 natural-language phrases users would actually type |
| `description` too short | Quote it; require ≥ 100 chars; include trigger phrases and a "Do NOT use for X (use Y)" exclusion |
| `version` absent | Set to `1.0.0` for new skills; bump per semver on substantive change |

After editing, re-run the inventory tool and confirm the skill no longer appears in the invalid-frontmatter list.

## Anti-Patterns

| Anti-pattern | Why it fails | What to do instead |
|---|---|---|
| Running manifest-write on a dirty skill tree | Writes a broken index that downstream consumers trust | Fix all inventory errors first, then regenerate |
| Resolving conflicts by deleting one instruction | Removes useful guidance the agent needs in the right scope | Narrow the scope of the instruction instead |
| Adding evals without negative expectations | Census flags them; they test only happy paths | Every eval must have at least one `does not / never / must not` expectation |
| Renumbering eval IDs during cleanup | Breaks eval-history references that use numeric IDs | Always append; never renumber |
| Un-backticking an identifier to suppress a false positive when the conflict is real | Hides a real boundary ambiguity | Fix the skill wording to accurately reflect the scope |
| Adding routing keywords without a real skill to route to | Creates more broken mappings | Only add keywords that map to an existing skill |
| Treating heading overlap as always wrong | Structural-template skills (model profiles, integration patterns) legitimately share structure | Review the differentiating content instead of restructuring |
| Using `scope: reference` to mask threshold violations | Reference scope downgrades eval-error to warning, hiding real gaps | Use `reference` only for genuine reference docs (contracts, schemas), never to dodge threshold enforcement |
| Producing a thin audit summary after a multi-hour session | A two-hour audit that outputs "5 entities missing evals" has performed a *census*, not an *audit* — 95% of the invested tokens are wasted | Census counts things; audits verify claims against evidence. Every audited skill needs per-claim verdicts (verified / drift) referencing specific file:line evidence |
| Running a "skill loop" without a minimum-output specification | Agents read methodology sections but skip output-format sections, then produce free-form summaries | Before any audit/eval/improvement session, define the output format up front. Templates exist — use them |
| LLM-based health checks instead of deterministic ones | Probabilistic grading of probabilistic content is circular and unreliable | Health-tooling layer is zero-LLM by design. LLMs grade *task output*, not *skill metadata* |

## Verification

Before any batch skill commit, verify:

- [ ] Inventory tool exits with zero critical errors
- [ ] Zero invalid-frontmatter entries
- [ ] Zero broken mappings in routing config
- [ ] All new skills meet the eval minimum (≥ 7, or ≥ 3 with explicit warning acceptance)
- [ ] All new evals include at least one negative expectation
- [ ] Conflict tool shows no NEW conflicts vs baseline
- [ ] Routing-gap report shows no new keyword gaps caused by your changes
- [ ] Manifest generator completed without errors
- [ ] Mirror parity verified if the library replicates to multiple harness directories
- [ ] Skill index header count matches actual skill count

## Do NOT Use When

| Use instead | When |
|---|---|
| `skill-scaffold` | Authoring or restructuring a single new SKILL.md (the contract for one file, not the system around the library) |
| `graph-audit` | Running the conformance audit on this Skill Graph repo specifically (operational), not designing the discipline |
| `lint-overlay` | General-purpose lint-rule selection and gate placement for any codebase, not skill-system-specific tooling |
| `documentation` | Writing prose for a human reader explaining how the skill system works |
| `code-review` | Reviewing a code change to the health-tooling scripts themselves |
| `testing-strategy` | Designing the test pyramid / trophy / honeycomb shape for a non-skill-library codebase |
| `prompt-craft` | Improving the wording of a single skill's prompt or eval prompt |
