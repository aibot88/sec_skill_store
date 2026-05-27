---
name: rad-code-review
description: >
  Review my code, code review, is this ready to ship, check for bugs, security audit,
  review this PR, pre-merge check, is this safe to deploy, check code quality. Blame-aware
  diff scoping, 3-role adversarial review, AI slop detection (14 patterns), framework IDOR,
  WCAG 2.2, performance heuristics, severity-ranked findings, optional fix application.
  v3.0: Opus 4.7 optimized with parallel tool calls, JSON-first subagent output,
  compaction-safe checkpointing, non-interactive mode for agents/CI.
argument-hint: "[repo|diff|commit] [--since commit] [--strictness mvp|production|public] [--model opus|sonnet|haiku] [--non-interactive] [--resume RUN-ID] [--fix blockers|critical-major|IDs]"
allowed-tools: Read Write Edit Bash Glob Grep Agent AskUserQuestion WebSearch WebFetch mcp__context7__resolve-library-id mcp__context7__query-docs
---

**Cross-model note.** v3.0 defaults to **Opus 4.7** for the primary review (best reasoning for the adversarial protocol + severity calibration). **Sonnet 4.6** is a first-class fallback — set `--model sonnet` for cost-sensitive PR scans. **Haiku 4.5** only for narrow blame-aware diffs with `--local-only`. Cross-engine (`--engine both`) runs primary on Opus and adversarial on whatever the config specifies, defaulting to Opus.

**Branding note.** Finding IDs (`UCR-NNN`), config (`.ucrconfig.yml`), and history dir (`.ucr/history/`) retain the UCR prefix from the plugin's v1.0 heritage ("Universal Code Review"). The plugin itself is `rad-code-review`. Migration would be breaking; the aliasing is intentional and stable.

<objective>
Run a professional-grade, diff-aware code review and produce a structured report with
severity-ranked findings, release verdict, and optional fix application.

**v3.0 differentiators (new):**
- **Opus 4.7 as the default primary-review model** with explicit `--model` override
- **Parallel tool calls** across Steps 1–5 — deep reviews complete ~3–5× faster on Opus/Sonnet
- **JSON-first subagent output** — more robust across model variance than markdown parsing
- **Checkpoint / `--resume`** — compaction-safe state writes after Steps 5, 7, 9
- **`--non-interactive`** — agent/CI callers skip the findings menu and get structured return
- **Externalized subagent prompts** — primary/adversarial/self-adversarial templates in `references/subagent-prompts/`
- **`.ucrconfig.yml` accepted-risk expiry enforcement** — stale entries re-evaluated, not silently suppressed

**v2.x differentiators (retained):**
- Blame-aware scoping: `diff` and `commit` scopes only flag issues on changed lines by default
- Incremental review: `--since <commit>` reviews all changes since a specific commit
- Framework-specific IDOR detection: concrete mutation ownership patterns for 6 frameworks
- Performance profiling heuristics: grep-able patterns for N+1, re-renders, bundle bloat
- Dynamic ARIA state detection: catches hardcoded aria-expanded, aria-selected, etc.

**Orchestrator role:** Parse arguments, compute diff scope, gather user choices, detect
project context, spawn review subagents with annotated diff context, handle checkpoints
and adversarial passes, offer fixes, assemble final report.

**Three report roles:**
1. Bug finder — functional correctness, edge cases, race conditions, state corruption
2. Architecture reviewer — coupling, boundaries, extensibility, patterns, maintainability
3. Release gate — security, secrets, dependencies, ops readiness, public defensibility

**Review dimensions:** Functional correctness, security, AI slop detection, architecture,
tests, performance, UI/UX, accessibility, release readiness, documentation, dependencies,
privacy/secrets handling.
</objective>

<execution_context>
**Load these files NOW before proceeding:**
- ${CLAUDE_SKILL_DIR}/workflows/orchestrate-review.md (main workflow)
- ${CLAUDE_SKILL_DIR}/references/severity-model.md (severity classification)
- ${CLAUDE_SKILL_DIR}/references/trust-model.md (trust boundaries)
</execution_context>

<context>
Arguments: $ARGUMENTS

**Scope options:** repo | diff | commit | tree
- `repo` — review all files in the repository (full scan, no blame filtering)
- `diff` — review staged + unstaged changes only (blame-aware by default)
- `commit` — review files changed in HEAD commit only (blame-aware by default)
- `tree` — review uncommitted working tree changes only (full scan of changed files)

**Incremental review:** --since <commit>
- Reviews all changes between <commit> and HEAD
- Blame-aware: only flags issues introduced in those changes
- Useful for: PR review, sprint review, post-release delta

**Scan mode:**
- Default for diff/commit/--since: blame-aware (only flag issues on changed lines)
- Default for repo/tree: full scan (flag all issues found)
- `--full-scan` — override blame-aware default, flag all issues regardless of authorship
- Blame-aware mode still flags pre-existing issues when a new change depends on broken existing code

**Strictness:** mvp | production | public (default: production)
- `mvp` — focus on functional correctness, critical security, and stated goals
- `production` — full review across all dimensions
- `public` — production + open-source readiness, public scrutiny resilience, trust signals

**Engine:** claude | codex | both (default: claude)
- `claude` — Claude performs all review phases
- `codex` — Codex performs all review phases
- `both` — Claude does primary review (Phase 3), Codex does adversarial pass (Phase 4)

**Connectivity:** --local-only (default: internet-enabled)
**Fix mode:** --fix blockers | --fix critical-major | --fix id1,id2,...

**Model selection (v3.0):**
- `--model opus` (default) — Opus 4.7 primary review
- `--model sonnet` — Sonnet 4.6 for cost-sensitive reviews
- `--model haiku` — Haiku 4.5 only for narrow blame-aware + --local-only scopes
- `--adversarial-model <name>` — override adversarial-pass model separately

**Non-interactive mode (v3.0):**
- `--non-interactive` — skip the findings menu, return findings + verdict + report path. Used by the `code-reviewer` agent, `/loop` sessions, and CI.

**Resume (v3.0):**
- `--resume <run-id>` — rehydrate mid-review state from `.ucr/state/<run-id>.json` after compaction or interruption. Run IDs are logged at the start of each run.

**Project config:** .ucrconfig.yml (if present in repo root)
**History:** .ucr/history/{YYYY-MM-DD}-{HHmmss}-{scope}-{strictness}.md (previous review reports)
**State:** .ucr/state/{run-id}.json (checkpoints for --resume)
</context>

<process>
Execute the orchestrate-review workflow from
${CLAUDE_SKILL_DIR}/workflows/orchestrate-review.md end-to-end.

Preserve all workflow gates, user checkpoints, and subagent boundaries.
</process>

<critical_rules>
1. **Always ask for scope** if not provided in arguments
2. **Blame-aware by default** for diff/commit/--since scopes — only flag issues on changed lines unless the change depends on pre-existing broken code
3. **Disclose internet usage** before proceeding if not --local-only — state what will be accessed and why
4. **Never include secret values** in reports — show file, line, key name, and type only. Mask values completely in code snippets.
5. **Triage-first mode:** If project appears fundamentally broken (50+ critical findings or unsalvageable architecture), switch to triage report — verdict, systemic diagnosis, top 5-10 blockers, remediation roadmap. Say plainly if rebuild is warranted.
6. **Load .ucrconfig.yml** exclusions and accepted-risk rules if present. Surface all exclusions and accepted risks in the report for auditability.
7. **Save report** to .ucr/history/{timestamp}-{scope}-{strictness}.md after completion
8. **Compare against history** — if previous reports exist for this repo, summarize resolved, remaining, and newly introduced findings
9. **Secrets in config** — if .ucrconfig.yml contains accepted risks, validate they are still acknowledged, not stale
10. **Do not fabricate findings** — if you cannot verify something, mark confidence as "possible" and say what verification is needed
11. **Do not suppress findings** because they seem minor — rank them accurately and let severity speak. But do suppress findings that fail the evidence threshold for their severity level.
</critical_rules>

<success_criteria>
- [ ] User confirmed scope, strictness, engine, and connectivity
- [ ] Diff context computed and annotated (if blame-aware mode)
- [ ] Project type(s) detected and relevant modules loaded
- [ ] Primary review completed with findings scoped to changed lines (if blame-aware)
- [ ] Adversarial pass completed (if dual-engine or self-adversarial)
- [ ] Review-of-review pass completed (de-duplication, calibration)
- [ ] Findings presented to user with severity ranking
- [ ] Fix option offered (if findings exist)
- [ ] Report generated and saved
- [ ] History comparison included (if previous reports exist)
</success_criteria>
