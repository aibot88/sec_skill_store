---
name: spec-driven-qa
description: >
  Validates code quality through spec-driven QA validation with structural anti-skip
  enforcement. Replicates all 6 phases of the DevForgeAI QA workflow using the
  Execute-Verify-Gate pattern at every step. Designed to prevent token optimization
  bias through lean orchestration, fresh-context subagent delegation, and binary CLI
  gate enforcement. Enforces test coverage (95%/85%/80% strict thresholds), detects
  anti-patterns, validates spec compliance, and analyzes code quality metrics. Use when
  validating implementations, ensuring quality standards, or preparing for release.
  Always use this skill when the user runs /qa or mentions QA validation, quality checks,
  or coverage analysis.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - Bash(devforgeai-validate:*)
  - Bash(git:*)
  - Bash(pytest:*)
  - Bash(dotnet:*)
  - Bash(cargo:*)
  - Bash(npm:*)
  - Bash(python:*)
  - Bash(radon:*)
  - Bash(npx:*)
  - Bash(mvn:*)
  - Bash(go:*)
  - Skill
model: opus
effort: High
---

# Spec-Driven QA Validation

Validate story implementations through strict 6-phase QA workflow while enforcing coverage thresholds, anti-pattern detection, and spec compliance.

**Context files are THE LAW:** tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**If ambiguous or conflicts detected: HALT and use AskUserQuestion**

---

## Anti-shortcut policy (ADR-062 / Tier 1.5 / D7)

When encountering obstacles, do not use destructive actions as a shortcut. For example, don't bypass safety checks (e.g. `--no-verify`) or discard unfamiliar files. Specifically for QA gates:

- **Do not bypass conviction gates by manually invoking hook scripts via Bash.** The PostToolUse `conviction-postrecord.sh` is designed to fire automatically when the framework dispatches the `phase-record` Bash call. Piping synthetic JSON to the hook directly forges the evidence trail.
- **Do not `Edit()` subagent worklog files post-hoc** to inject required schema fields (`subagent_id`, `phase_state_checksum`, etc.). Re-invoke the subagent so it produces a compliant worklog naturally.
- **Do not write placeholder content to satisfy substance checks.** Phrases like "placeholder", "to satisfy", "to bypass", "TODO", "TBD", and "filler" are detected and rejected by `conviction.py:_validate_subagent_worklog()` (D3). Writing fake content to satisfy a check that catches fake content is the antipattern the check exists to prevent.
- **Avoid focusing on passing tests and hard-coding.** A passing test on hard-coded inputs is a regression masquerading as success.

If a gate blocks you, the gate is doing its job — fix the underlying gap, do not route around the gate. Per `.claude/rules/workflow/diagnosis-before-fix.md` HALT trigger #5: 3 consecutive BLOCK verdicts on the same `(story_id, phase)` requires `/rca STORY-NNN` invocation before further attempts.

---

## Execution Model

This skill expands inline. After invocation, execute Phase State Initialization immediately (with --mode=${MODE} pass-through). Do not wait passively, ask permission, or offer execution options.

**Self-Check (if ANY box is true = VIOLATION):**

- [ ] Stopping to ask about token budget
- [ ] Stopping to offer execution options
- [ ] Waiting passively for results
- [ ] Asking "should I execute this?"

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase State Initialization now.

---

## Anti-Skip Enforcement Contract

This skill enforces 5 independent anti-skip layers. ALL FIVE must fail for a step to be skipped:

1. **Fresh-context subagent execution** - Subagents run in isolated context without accumulated bias
2. **Binary CLI gates** - `devforgeai-validate phase-check/phase-complete/phase-record` (Python CLI; compiled was the historical name)
3. **Hook enforcement** - Shell scripts in `.claude/hooks/` run outside LLM control
4. **Step registry + artifact verification** - `.claude/hooks/phase-steps-registry.json` tracks every mandatory step
5. **Out-of-band adversarial audit (QA)** - Layer 9 audit module gates QA phases per `audit-policy.yaml` in this skill; runs from a fresh-context judge model and verifies QA findings against actual artifacts (`gaps.json`, anti-pattern findings, coverage reports, regression diffs) using citation-verified evidence (Source: `.claude/rules/workflow/qa-output-fidelity.md`; Source: ADR-059)

For Layer 5 audit gate behavior, see `references/audit-gate.md` (this skill) and shared canonical at `src/claude/scripts/devforgeai_cli/audit/README.md`.

**Execute-Verify-Gate Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact action to perform
- **VERIFY:** How to confirm the action happened (Glob, Grep, exit code, Task result)
- **RECORD:** CLI command to record completion (`devforgeai-validate phase-record`)

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary. (Reference: RCA-001, RCA-002, RCA-046)

---

## Validation Modes

### Light (~10K tokens, 2-3 min)
- Build/syntax checks
- Test execution (100% pass required)
- Critical anti-patterns only
- Deferral validation (if deferrals exist)

### Deep (~35K tokens, 8-12 min)
- Complete coverage analysis (95%/85%/80% thresholds -- ADR-010, non-negotiable)
- Comprehensive anti-pattern detection
- Full spec compliance (AC, API, NFRs)
- Code quality metrics
- Security scanning (OWASP Top 10)
- Deferral validation (if deferrals exist)

---

## Parameter Extraction

Extract story ID and mode from conversation context. See `.claude/skills/spec-driven-qa/references/parameter-extraction.md` for the extraction algorithm.

Extraction methods: YAML frontmatter, file reference, explicit statement, status inference.
Default mode: deep (if unable to determine).

## Command Integration

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$STORY_ID` | /qa | Story identifier (STORY-NNN) |
| `$MODE` | /qa | Validation mode (light/deep/auto) |

---

## Phase State Initialization [MANDATORY FIRST]

```bash
devforgeai-validate phase-init ${STORY_ID} --workflow=qa --mode=${MODE} --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "01". |
| 1 | Existing workflow | Resume. Run `devforgeai-validate phase-status ${STORY_ID} --workflow=qa` to get CURRENT_PHASE. |
| 2 | Invalid story ID | HALT. Must match STORY-XXX pattern. |
| 127 | CLI not installed | Continue without enforcement (backward compatibility). |

**Fallback:** If `--mode` is rejected by an older CLI version, fall back to `phase-init` without `--mode` (see phase-01-setup.md Entry Gate).

---

## Phase Orchestration Loop

```
FOR phase_num in [01, 02, 03, 04, 05, 06]:
    phase_id = phase_num

    1. ENTRY GATE:
       IF phase_id == "01": SKIP phase-check (phase-init is the entry gate for Phase 01)
       ELSE: devforgeai-validate phase-check ${STORY_ID} --workflow=qa --from={prev} --to={phase_id} --project-root=.
       IF exit != 0: HALT

    2. LOAD: Read(file_path=".claude/skills/spec-driven-qa/phases/{phase_files[phase_id]}")

    3. EXECUTE: Follow every step in the phase file (EXECUTE-VERIFY-GATE triplets)
       - Each step's EXECUTE instruction tells you exactly what to do
       - Each step's VERIFY instruction tells you how to confirm it happened
       - Each step's RECORD instruction tells you what CLI command to call

    4. RECORD: devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase={phase_id} --project-root=.

    5. EXIT GATE:
       a. AUDIT GATE (precondition):
          devforgeai-validate audit-gate ${STORY_ID} --workflow=qa --phase={phase_id} --project-root=.
          IF exit != 0: HALT (audit infrastructure failure)
          See references/audit-gate.md for behavior matrix.
       b. PHASE COMPLETE:
          devforgeai-validate phase-complete ${STORY_ID} --workflow=qa --phase={phase_id} --checkpoint-passed --project-root=.
          IF exit != 0: HALT (audit verdict failed OR other gate violation)
```

| Phase | Name | File |
|-------|------|------|
| 01 | Setup | `phases/phase-01-setup.md` |
| 02 | Validation | `phases/phase-02-validation.md` |
| 03 | Diff Regression Detection | `phases/phase-03-diff-regression.md` |
| 04 | Analysis | `phases/phase-04-analysis.md` |
| 05 | Reporting | `phases/phase-05-reporting.md` |
| 06 | Cleanup | `phases/phase-06-cleanup.md` |

---

## Required Subagents Per Phase

| Phase | Required Subagents | Enforcement | Audit |
|-------|-------------------|-------------|-------|
| 01 | (none) | N/A | N |
| 02 | (none) | N/A | Y |
| 03 | (none) | N/A | Y |
| 04 | anti-pattern-scanner, test-automator, code-reviewer, security-auditor | BLOCKING (adaptive per story type) | Y |
| 04 | deferral-validator (if deferrals) | CONDITIONAL | Y |
| 04 | diagnostic-analyst (if failures) | CONDITIONAL | Y |
| 05 | qa-result-interpreter | BLOCKING | Y |
| 06 | (none) | N/A | N |

The Audit column reflects whether the Layer 5 audit gate runs for the phase. Mode (single/consensus) and fail_mode (closed/open) are defined in `audit-policy.yaml`; this table is binary Y/N per ADR-059.

**Deviation Protocol:** Any skip requires explicit user consent via AskUserQuestion.

---

## Definition of Done Protocol

Deferral validation CANNOT be skipped (RCA-007). Deferred DoD items require user approval, story/ADR references, and deferral-validator subagent validation.

Load protocol details when needed:
```
Read(file_path=".claude/skills/spec-driven-qa/references/dod-protocol.md")
```

---

## State Persistence

**Location:** `devforgeai/workflows/${STORY_ID}-qa-phase-state.json`

---

## Workflow Completion Validation

```
IF completed_count < 6: HALT "WORKFLOW INCOMPLETE - {completed_count}/6 phases"
IF completed_count == 6: "All 6 phases completed - QA workflow validation passed"
```

---

## Success Criteria

**Light:** Build passes, tests pass, no CRITICAL, deferrals valid, <10K tokens
**Deep:** Coverage thresholds met, no CRITICAL/HIGH, spec compliant, quality acceptable, deferrals valid, status="QA Approved", <35K tokens

---

## Reference Files Index

**Local references** (loaded per-phase on demand, NOT consolidated):

| Phase | Reference Files (load via Read from .claude/skills/spec-driven-qa/references/) |
|-------|-----------------------------------------------------------------------------|
| 01 | `parameter-extraction.md`, `phase-0-setup-workflow.md`, `test-isolation-service.md`, `parallel-validation.md` |
| 02 | `traceability-validation-algorithm.md`, `coverage-analysis.md` |
| 03 | `diff-regression-detection.md`, `test-tampering-heuristics.md` |
| 04 | `anti-pattern-detection.md`, `parallel-validation.md`, `spec-compliance-validation.md`, `code-quality-workflow.md`, `dod-protocol.md`, `automation-scripts.md`, `ui-design-validation.md` |
| 05 | `qa-result-formatting-guide.md`, `phase-3-reporting-workflow.md`, `story-update-workflow.md` |
| 06 | `phase-4-cleanup-workflow.md`, `feedback-hooks-workflow.md` |

**Assets:**
- `.claude/skills/spec-driven-qa/assets/config/coverage-thresholds.md`
- `.claude/skills/spec-driven-qa/assets/language-smoke-tests.yaml`
- `.claude/skills/spec-driven-qa/assets/templates/qa-report-template.md`
- `.claude/skills/spec-driven-qa/assets/templates/qa-recommendations-template.md` (Sprint 1; Sprint 2 generator consumes this)
- `.claude/skills/spec-driven-qa/assets/schemas/qa-recommendations-schema.json` (Sprint 1)
- `.claude/skills/spec-driven-qa/assets/traceability-report-template.md`

**Phase 05 output artifacts (three-audience split):**
- `devforgeai/qa/reports/${STORY_ID}-qa-report.md` — prose for humans (Step 5.2; always emitted).
- `devforgeai/qa/reports/${STORY_ID}-gaps.json` — JSON for CI/CD (Step 5.3; emitted only on `overall_status == "FAILED"`).
- `devforgeai/qa/recommendations/${STORY_ID}-qa-recommendations.md` — AI-optimized Markdown+YAML for downstream `/dev --fix` (Step 5.5 via `generate-qa-recommendations` CLI; emitted on every QA completion including PASS_WITH_WARNINGS). See `.claude/skills/spec-driven-qa/references/qa-recommendations-authoring.md`.

**Automation Scripts:**
- `.claude/skills/spec-driven-qa/scripts/generate_coverage_report.py`
- `.claude/skills/spec-driven-qa/scripts/detect_duplicates.py`
- `.claude/skills/spec-driven-qa/scripts/analyze_complexity.py`
- `.claude/skills/spec-driven-qa/scripts/security_scan.py`
- `.claude/skills/spec-driven-qa/scripts/validate_spec_compliance.py`
- `.claude/skills/spec-driven-qa/scripts/generate_test_stubs.py`
