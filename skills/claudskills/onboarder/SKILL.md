---
name: onboard
description: Verbal-first 5-section interview that captures identity, work context, vault layout, trust preferences, and privacy toggles. Produces a populated user-manifest.json plus an optional staged launchd plist in roughly 25 minutes. Hands off to /adopt when the vault is fresh.
disable-model-invocation: false
argument-hint: "[--resume] [--typed-only] [--section {a|b|c|d|e}] [--retention-on] [--dry-run] [--seed-content <path>] [--skip-auto-author] [--skip-content-seeding] [--auto-author-only-surfaces=<csv>]"
---

# Onboarder

The user-facing entry for `/onboard`. Captures everything the rest of the system reads at runtime — identity, paths, vault layout, scheduled-job preferences — and writes a single `user-manifest.json` so generic skills don't carry per-user content.

## What runs when you type `/onboard`

Five sections, in order. Each takes a few minutes.

| # | Section | Mode | Time | What gets captured |
|---|---|---|---|---|
| A | Welcome and discovery review | Confirm pre-fills (no recording) | ~2 min | Name, email, timezone, candidate vault root, MCP integrations |
| B | Who you are and what you do | Voice 3–5 min OR typed | ~5 min | Role, organization, industry, seniority, active projects, people you work with, working cadence, default audience |
| C | Your knowledge system | Voice 2–4 min OR typed | ~4 min | Vault organizational method, structured-projects flag, fresh vs existing, canonical file types, sensitive-content opt-out |
| D | Trust, privacy, and automation | Voice 2–3 min OR typed | ~3 min | Autonomy level, initial scheduled job, hook preferences |
| E | Final checkboxes | Three binary toggles (no recording) | ~1 min | Auto-commit / memory consolidation / multi-session enabled |

After Section E, an optional **Section F** runs the personalization surfaces — composes a personalized `~/.claude/CLAUDE.md`, seeds memory files, writes a vault `CLAUDE.md`, populates `_tag_prefixes`, generates a starter `doc-dependencies.json`, configures the frontmatter enforcer, and seeds `/architect`'s research topics. With `--seed-content <path>`, Section F also runs the four-stage infer-vault chain over your existing notes.

## Invocation

| Command | Behavior |
|---|---|
| `/onboard` | Full 5-section flow A → B → C → D → E. |
| `/onboard --resume` | Reads `user-manifest.system.phases_completed[]` and continues from the first unfinished section. |
| `/onboard --typed-only` | Skip the voice probe; force typed input on B/C/D. |
| `/onboard --section {id}` | Re-record one section without disturbing the others. |
| `/onboard --retention-on` | Keep transcripts and audio after extraction (default: auto-delete). |
| `/onboard --dry-run` | Walk the flow without writing to live targets; emit unified diffs from the schema bootstrapper. |
| `/onboard --seed-content <path>` | Drive Section F's infer-vault chain over an existing corpus of notes. |

`SessionStart` triggers `/onboard` automatically when `$CLAUDE_HOME/user-manifest.json` is missing. After Section E completes, the skill hands off to `/adopt` if `vault.is_fresh == true` and `paths.vault_root` is null or non-existent.

Three Section F flags propagate from the invocation:

| Flag | Effect |
|---|---|
| `--skip-auto-author` | Skip the seven personalization surfaces. The orchestrator chain still runs if `--seed-content` is set. |
| `--skip-content-seeding` | Skip the orchestrator chain. The seven surfaces still run. |
| `--auto-author-only-surfaces=<csv>` | Run a comma-separated subset (e.g. `=1,3,9`). |

## Per-section pipeline (B / C / D)

For each transcript-mode section, in order:

1. Render the prompt card.
2. Probe the harness for `/voice`. On unavailability or `--typed-only`, swap to typed-textarea.
3. Capture: `/voice` records until you stop; returns transcript text plus an audio path. Transcript lands at `$CLAUDE_HOME/onboarding/transcripts/section-{id}.txt`.
4. Run the section's LLM extraction prompt against `{transcript, schema slice via q-field-map, discovery context from Section A}`. Receive a populated fragment plus a confidence map, source spans, missing-required list, conflicts, and follow-up.
5. Apply confidence gates:

   | Confidence | Behavior |
   |---|---|
   | ≥ 0.85 | Populate silently; field appears confirmed in the summary. |
   | 0.5 – 0.85 | Populate; flag yellow in summary; you accept, edit, or clear. |
   | < 0.5 | Surface as missing; trigger one surgical follow-up; re-extract once. |
   | < 0.5 on a required field after follow-up | **Block section exit.** Summary highlights the field; you type the correction inline before exit. |

6. Render an inline-edit summary. You can accept, edit fields, re-record the section, or trigger an opt-out.
7. Append a JSONL audit entry: `{section_id, run_id, ts, opt_outs[], confidence_map, source_spans, corrections[], follow_ups[], manifest_paths_written[]}`.
8. Merge the fragment into the populated manifest via `bootstrap-schemas.sh` (atomic temp+rename, per-target validation, idempotent).
9. After Section C completes, `archetype-inference.sh` runs against the B+C transcripts. The archetype label is written to `architect.prior_seed[]`; archetype-seeded canonical file types are appended to `vault.canonical_file_types[]` (deduplicated).
10. If retention is OFF (default), delete transcript and audio. If ON, retain at `$CLAUDE_HOME/onboarding/transcripts/`.

Section A is a deterministic confirmation screen — no transcript, no extraction, no confidence gates. Section E is three deterministic binary toggles.

## Opt-out surfaces (10)

Each opt-out is reachable in-flow from the owning section's summary screen and writes a deterministic manifest record without aborting the section.

| # | Surface | Section | Manifest record |
|---|---|---|---|
| 1 | Discovery (skip filesystem pre-fill) | A | Empty discovery context + `system.opt_outs[]` appends `discovery_skipped`. |
| 2 | Organization | B | `identity.organization: null`. |
| 3 | People capture | B | `people: []` (downstream people-audit skips). |
| 4 | Tool integrations | B | Per-tool `null` flags individual integration blocks. |
| 5 | Vault | C | `vault: null` (downstream vault writes go stub-mode until a vault is created). |
| 6 | Sensitive-content acknowledgement | C | `system.opt_outs[]` appends `sensitive_isolation` (or a user note in `vault.notes`). |
| 7 | Hook output-contract enforcement | D | Advisory-mode install for write-validation hooks. |
| 8 | Session-checkpoint threshold | D | Raise to 55% OR set `CHECKPOINT_DISABLE_OK=1` in `behavioral.hook_preferences`. |
| 9 | Initial scheduled job | D | `orchestration.jobs: []` — no plist written, no staging file. |
| 10 | Observability tripwires | D | Cron monitoring not installed; you can re-enable later via `/setup-job`. |

**Full-opt-out terminal state** (all 10 elected) produces a valid minimal `user-manifest.json` plus a valid empty `orchestration.json` plus zero launchd jobs staged.

## Section F — greenfield personalization

Section F runs **after** the manifest is populated. Every Section F surface reads from manifest fields, so the post-finalize ordering is structural.

### Invocation order

```
A → B → C → D → E → run_finalize → Section F
```

### The seven personalization surfaces

Dispatched in declared order (1, 2, 3, 4, 5, 6, 9 — surfaces 7 and 8 don't exist as separate surfaces):

| # | Surface | Output | Mode |
|---|---|---|---|
| 1 | claude-home `CLAUDE.md` | Composed-prose personalization over the identity-substituted template. | LLM |
| 2 | `$CLAUDE_HOME/projects/<user>/memory/` seeds | LLM-composed enrichment over deterministic frontmatter seeds. | LLM |
| 3 | Vault `CLAUDE.md` | Routing decision tree + tag taxonomy + pre-write checklist. | LLM |
| 4 | `_tag_prefixes[]` | Archetype-keyed tag-namespace registry. | Deterministic |
| 5 | `doc-dependencies.json` | Cascade-rule registry consumed by `pre-write-guard.sh`. | Deterministic |
| 6 | frontmatter-enforce per-capability config | Engagement-aliases and required-field overrides. | Deterministic |
| 9 | Architect `prior_seed[]` + `research_topics[]` | Industry-tuned concerns and search-prompt seeds for `/architect`. | LLM |

Each surface appends `auto-author-log.jsonl` records (`{action, ts, surface, evidence_path, ...}`). Surfaces 3, 4, and 6 are wrapped by a collaborative consultation gate that writes additional `{action: "consult", ...}` records to the same log. The log is heterogeneous JSONL discriminated by the `action` field; there is no separate consultation log file.

### The four-stage infer-vault chain

When `--seed-content <path>` is supplied, Section F invokes the orchestrator after the seven surfaces complete:

```
cluster.sh → propose-taxonomy.sh → import-plan.sh → review-gate.sh
```

Per-stage idempotency uses `state/<stage>.done` markers. On a review-gate stall (interactive review pending), the orchestrator writes `state/review-pending.flag`, exits 64, and surfaces a resume message; you invoke `/onboard --resume` after review and the orchestrator skips completed stages.

For the documented non-interactive flow, Section F sets `REVIEW_GATE_ACCEPT_ON_EOF=1` so `review-gate.sh` doesn't block on its prompt loop.

### Section F idempotency

Each surface records its own done-marker under `$INPUTS_DIR/section-f-state/surface-N.done`. Re-running `/onboard` (or `/onboard --resume`) skips surfaces whose marker exists; the orchestrator inherits per-stage idempotency from its own markers.

## Resume and mid-section quit

| Trigger | Behavior |
|---|---|
| `/onboard --resume` | Read `phases_completed[]`; jump to the first missing section in order. |
| `SessionStart` with no `user-manifest.json` | Auto-invoke `/onboard`; write `phases_completed: []` on first commit. |
| `SessionStart` with `phases_completed[]` non-empty and incomplete | Surface a one-shot resume prompt: "You stopped onboarding mid-flow. Resume from Section {next}?" |
| Mid-section quit | Per-section checkpoint: partial transcript saved; extraction not yet run; `phases_completed[]` is not updated for the unfinished section. Re-record offered on resume. |

The re-record path (`/onboard --section {id}`) discards the named section's current fragment and JSONL audit entry, removes its `phases_completed[]` membership if present, and runs the section pipeline fresh. Other sections are untouched.

## Discovery probes (Section A pre-fills)

Section A pre-fills are sourced from the live host; the skill reads but never writes:

| Probe | Source | Q-ID |
|---|---|---|
| `discovery.name` | `git config --global user.name` | A-1 |
| `discovery.email` | `git config --global user.email` | A-2 |
| `discovery.timezone` | `readlink /etc/localtime \| sed 's\|.*/zoneinfo/\|\|'` (privilege-free, IANA Continent/City form) | A-3 |
| `discovery.vault_root` | Filesystem scan: `~/Documents/*Vault*`, `~/Vault`, `~/Obsidian` | A-4 |
| `discovery.tools.*` | Connected MCP enumeration in `~/.claude/settings.json`; `which code cursor zed nvim` for dev_env | A-CB1..A-CB6 |
| `discovery.platform` | `uname -s` → `O.platform` | (not user-asked) |

If any probe returns null, the field is left empty and you type it inline. Section A's opt-out (#1) skips the entire pre-fill block.

## Initial scheduled job (Section D)

After Section D's schema fragment commits — and unless opt-out #9 was elected — the initial-job-setup flow runs:

1. Read `orchestration.jobs[0].id` from Section D output (`librarian` or `architect`; default applied per `q-field-map.json`).
2. Apply per-job defaults (schedule, log path, idle-watchdog seconds, budget, model, weekend-skip).
3. The 8-question customization sub-flow surfaces these defaults as overrides.
4. Show a dry-run preview: pretty-printed plist plus a human-readable schedule.
5. On confirmation, invoke `installer/render-launchd.sh <job>`.
6. **Write the rendered plist to `$CLAUDE_HOME/Library/LaunchAgents.staging/`** — staging directory only. The skill never calls `launchctl bootstrap` against your live host.
7. Append `$CLAUDE_HOME/onboarding/audit/initial-job-setup.jsonl`.
8. Print: "Onboarding complete. Run `claude system enable-daemon` to activate the staged job."

Activation is deliberately a separate, user-invoked step. Onboarding stages exactly one plist; you decide when (and whether) to enable it.

## Output Contract

Every skill that writes to the user filesystem declares files written, schema types, pre-write validation, and failure mode.

### Files written

| Path | Schema type | Cardinality | Lifecycle |
|---|---|---|---|
| `$CLAUDE_HOME/user-manifest.json` | Populated instance of `user-manifest-schema.json` | Single | Skeleton placed by installer; populated via merge-into-existing semantics. |
| `$CLAUDE_HOME/orchestration.json` | Populated instance of `orchestration-schema.json` | Single | Skeleton placed by installer; `jobs[]` populated from Section D. |
| `$CLAUDE_HOME/Library/LaunchAgents.staging/com.claude-stem.<Label>.plist` | launchd plist (XML; `plutil -lint` validated) | Per scheduled job | Staging only — **never** moved to `~/Library/LaunchAgents/` by this skill. |
| `$CLAUDE_HOME/onboarding/audit/section-{a..e}.jsonl` | JSONL audit | One per section | Append-only. |
| `$CLAUDE_HOME/onboarding/audit/initial-job-setup.jsonl` | JSONL audit | One file | Append-only. |
| `$CLAUDE_HOME/onboarding/transcripts/section-{a..e}.txt` | Raw text | One per recorded section | Auto-deleted after extraction unless `--retention-on`. |
| `$CLAUDE_HOME/onboarding/bootstrap-log.jsonl` | JSONL audit (per-field) | Single | Append-only. |
| `$CLAUDE_HOME/auto-author-log.jsonl` | JSONL audit | Single | Append-only; emitted by Section F surfaces. |

JSONL audit entries strip user-provided strings from diagnostic fields; only structural metadata is recorded.

### Pre-write validation

For every manifest write, in order:

1. **Q-ID legality.** Proposed write paths must resolve via `q-field-map.json` keys. Unknown Q-ID blocks the write.
2. **Schema validation.** `bootstrap-schemas.sh` validates the populated instance against its declared schema (`ajv` on PATH preferred; `jq`-structural fallback otherwise).
3. **Confidence-gate clearance.** Required fields must be ≥ 0.5 OR have an inline-typed correction; otherwise section exit blocks.
4. **Idempotency.** If a target file exists and bytes match the would-write payload, skip rename and audit-log a `skip-identical` record. Bytes-differ without `--force` writes a `<target>.new` sidecar plus a unified diff to stderr; exits 1.
5. **Atomicity.** All writes go through `tmp + rename`; no partial state visible to live readers.
6. **Reference-leak floor.** JSONL audit entries strip user strings; only structural metadata is recorded in audit fields.

### Failure mode — block-and-log

Never "write and hope." On any validation, parse, or IO failure:

1. Roll back all `*.tmp` files in the current run (atomic semantics; live targets remain untouched).
2. Append `{ts, run_id, status: BOOTSTRAP_FAILED, failed_validation_class, remediation_hint}` to `bootstrap-log.jsonl`.
3. Exit non-zero with a structured diagnostic.
4. The section's JSONL audit entry records the failure but does NOT add the section to `phases_completed[]` — `--resume` will retry the section cleanly.

## Hard rules

1. **No `launchctl bootstrap` against your live host.** Production install writes plists to staging only; activation is owned by `claude system enable-daemon`. Test runs use a sandbox-exec profile inside a Lima VM.
2. **One UX, two input modes.** Voice and typed paths share the same prompt card, the same extraction prompt, the same confidence gates, and the same summary screen. Per-section toggle is honored mid-flow.
3. **One surgical follow-up per low-confidence required field.** Never re-interview a section. Never re-record for one field. After one follow-up, the inline-edit summary is the escape hatch; block-and-log if still < 0.5.
4. **Per-section checkpoint after schema-bootstrap merge.** `phases_completed[]` updates only after a successful merge — partial state is unrecoverable but not corrupting.
5. **Transcripts auto-delete by default.** Retention is opt-in via Section E.
6. **Initial-job-setup writes exactly one plist.** Default is `librarian` daily 06:00 weekdays; alternate is `architect` weekly Monday 06:00. Opt-out #9 produces zero plists.
7. **`/adopt` delegation is conditional.** Hand off after Section E only when `vault.is_fresh == true` AND `paths.vault_root` is empty or non-existent. If you have an existing vault, `/adopt` is not invoked automatically.

## Related skills

| Skill | When | What it owns |
|---|---|---|
| `/adopt` | After Section E if `vault.is_fresh == true` AND `paths.vault_root` is empty | Fresh-vault scaffolding (directory tree, seed `CLAUDE.md`, `System Backlog.md`). |
| `/librarian` | Default initial job (Section D) | Daily vault scan, manifest refresh, drift findings. |
| `/architect` | Alternate initial job (Section D); also runs first-time after onboarding completes if `architect.prior_seed` carries an archetype label | Strategic 7-dimension vault analysis. |
| `claude system enable-daemon` | After onboarding completes; user-invoked | Moves the staged plist to `~/Library/LaunchAgents/` and runs `launchctl bootstrap gui/$UID`. |

## See also

- [`onboarding/SKILL.md`](../../onboarding/SKILL.md) — the bootstrap-schemas engine that writes the four schema instances atomically.
- [`docs/personalization-model.md`](../../docs/personalization-model.md) — what's universal, combined, and personal across the auto-author output.
- [`docs/llm-cost-model.md`](../../docs/llm-cost-model.md) — token costs for the four LLM surfaces.
- [`skills/adopt/SKILL.md`](../adopt/SKILL.md) — vault scaffold that consumes the manifest.
