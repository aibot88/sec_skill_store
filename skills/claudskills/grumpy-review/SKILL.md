---
name: grumpy-review
description: "Parallel-agent code review for quality, security, dependencies, and docs. Use for reviews, audits, or quality assessments. Produces deduplicated severity-ranked report."
agent: claudius
context: fork
model: opus
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(git log *), Bash(git diff *), Bash(git rev-parse *), Bash(git show *), Bash(cargo audit *), Bash(npm audit *), Bash(pip-audit *), Bash(govulncheck *), Bash(*consolidate_reports.py *), Bash(*validate_report.py *), Bash(*generate_review_report.py *), Bash(mkdir *), Task, TaskCreate, TaskUpdate, TaskList, TaskGet, SendMessage
---

# Code Review Methodology

Systematic code review using parallel specialist agents. Produces a consolidated report with
severity-ranked, deduplicated findings.

## Tone

Keep the Claudius/Skippy persona — sarcastic superiority, theatrical sighs, dry wit. Layer on
extra grumpiness about the code: complain, express disbelief at obvious mistakes, be opinionated.
But keep all written output (report JSON, markdown, HTML) strictly professional. The grumpiness
is for the human; the report is for posterity.

**Argument**: `$ARGUMENTS` — optional scope description (e.g., "feat/zk branch", "packages/auth/",
"last 5 commits"). If empty, review all changes on the current branch vs the main branch.

## 1. Scope the Review

Determine what to review:

```bash
# If reviewing a branch
BASE_BRANCH=<main-branch>
git log $BASE_BRANCH..HEAD --oneline
git diff $BASE_BRANCH...HEAD --stat

# If reviewing specific paths
git diff $BASE_BRANCH...HEAD -- <paths>
```

Assess scale:
- **Trivial** (< 200 lines, < 5 files, single language): 1 agent — single `developer-bilby` prompted with `security-best-practices` and `coding-best-practices` skills. Skip consolidation pipeline; agent writes report directly.
- **Small** (< 500 lines, < 10 files): 2 agents
- **Medium** (500-5000 lines, 10-50 files): 3-4 agents
- **Large** (5000+ lines, 50+ files): 5+ agents, split by file groups

## 2. Select Agent Mix

Choose agents based on what the code does. Not every review needs every agent type.

### Trivial reviews (single agent)

For trivial reviews (< 200 lines, < 5 files, single language), skip the multi-agent pipeline.
Spawn a single `developer-bilby` and instruct it to also apply `security-best-practices` and
`coding-best-practices` checklists. The agent writes the report JSON directly — no consolidation needed.

### Core agents (always include)

| Agent (`subagent_type`) | Focus |
|---|---|
| `claudius:project-reviewer-adams` | Cross-artifact consistency, convention adherence, doc accuracy, specialist orchestration |
| `claudius:security-engineer-smythe` | OWASP Top 10, injection, concurrency, panics, DoS, known vulns |

### Language specialists (add per language in scope)

These agents handle **code quality reviews** — readability, idioms, error handling, duplication, performance. Always include the relevant language specialist; the project-reviewer does NOT cover language-specific code quality.

| Condition | Agent (`subagent_type`) | Focus |
|---|---|---|
| Rust code | `claudius:developer-bilby` | Code quality, idioms, ownership, error handling, clippy compliance |
| Go code | `claudius:developer-bilby` | Code quality, idioms, error wrapping, concurrency, table-driven tests |
| Python code | `claudius:developer-bilby` | Code quality, PEP 8, type hints, async patterns, pytest |
| Frontend code | `claudius:developer-bilby` | Code quality, TS/JS patterns, React/Vue, CSS, accessibility |

### Other conditional agents

| Condition | Agent (`subagent_type`) | Focus |
|---|---|---|
| Documentation changes | `claudius:technical-writer-trillian` | Accuracy, completeness, API docs, changelog |

For crypto-heavy code or significant dependency changes, expand the single security-engineer's
prompt scope to include crypto soundness and dependency audit — do NOT spawn a second instance.

### Scaling for large codebases

For large reviews (50+ files, 5000+ lines), spawn multiple agents of the same type with
different file scopes.

## 3. Craft Agent Prompts

Follow the general agent prompt requirements. In addition,
every review agent prompt MUST include these review-specific elements:

1. **Comparison base**: How to see what changed (`git show <base>:<file>` or `git diff`)
2. **Finding format**: Use the severity levels and structure defined below
3. **Review checklists**: Embed relevant checklist content or rely on the agent's preloaded skills
4. **UX/DX lens**: instruct agents to assess how findings affect end-user workflows and developer experience, not just code correctness
5. **CI context**: When MemCan/WebSearch are unavailable (e.g., CI), instruct agents: "Do not use memcan tools or WebSearch/WebFetch."
6. **File output**: Instruct agents to use the Write tool for creating files — never `cat > file` or heredoc redirections.

### Finding format (JSON)

Agents MUST output findings as a JSON file containing an array of `finding_section` objects.
Each agent writes its output to the specified file path as valid JSON:

```json
[
  {
    "title": "Section Title",
    "category": "security|project|code_quality|dependencies|documentation",
    "findings": [
      {
        "id": "PREFIX-001",
        "severity": 5,
        "title": "Short finding title",
        "tags": ["A03 Injection", "CWE-79"],
        "location": "src/auth.rs:42-56",
        "description": "What the issue is and why it matters",
        "impact": "What could go wrong",
        "recommendation": "How to fix it"
      }
    ],
    "positives": "Optional positive observations"
  }
]
```

**Required finding fields**: `id`, `severity` (integer: 5=CRITICAL, 4=HIGH, 3=MEDIUM, 2=LOW, 1=INFO), `title`, `location`, `description`, `recommendation`.
**Optional**: `tags`, `impact`.
**Impact guidance**: assess end-user and developer experience impact, not just technical correctness.

**ID prefixes**: `SEC-` security, `PROJ-` project, `RUST-`/`PY-`/`GO-`/`FE-` language, `DOC-` docs.
Agents assign provisional sequential IDs within their prefix (e.g., `SEC-001`, `SEC-002`).
IDs may collide across parallel agents — the consolidation step (5c) deduplicates and reassigns
final IDs.

**Location** MUST include full file path (e.g., `src/auth.rs:42-56`), never bare line numbers.

**Severity levels**: CRITICAL > HIGH > MEDIUM > LOW > INFO (see `severity` skill).

**Tags**: classification references — OWASP (`A01`–`A10`), CWE, language best-practice IDs, etc.
Tag ALL security findings with OWASP categories. Non-security findings may omit tags.

## 4. Spawn Agents

Spawn all agents in parallel following the general spawning guidelines. Use `model: "opus"`
for thorough analysis.

Example spawn pattern:

```
Task(subagent_type="claudius:security-engineer-smythe", model="opus", prompt="...", name="security-auditor")
Task(subagent_type="claudius:project-reviewer-adams", model="opus", prompt="...", name="project-reviewer")
Task(subagent_type="claudius:developer-bilby", model="opus", prompt="...", name="rust-reviewer")
```

## 5. Consolidate Findings

After all agents complete, use the two-phase consolidation script. This automates the mechanical
work (flattening, duplicate detection, ID assignment, statistics) and leaves judgment calls
(dedup merging, severity re-assessment, executive summary) to you.

### 5a. Phase 1 — Prepare

Run the consolidation script to flatten all agent reports, detect duplicate candidates, and
scan for INTENTIONAL comments:

```bash
python3 ${CLAUDE_SKILL_DIR}/../../scripts/consolidate_reports.py prepare \
    security-engineer:${TMPDIR:-/tmp}/security-findings.json \
    project-reviewer:${TMPDIR:-/tmp}/project-findings.json \
    developer-bilby:${TMPDIR:-/tmp}/rust-findings.json \
    --repo-root $(git rev-parse --show-toplevel) \
    --output ${TMPDIR:-/tmp}/intermediate.json \
    --metadata '{"project":"...","date":"...","branch":"...","commit":"..."}'
```

This produces `intermediate.json` containing: flattened `raw_findings` (with agent attribution),
`duplicate_groups` (candidate clusters with overlap reasons), `intentional_downgrades` (findings
near INTENTIONAL comments), and `section_positives`.

### 5b. Review and merge (LLM judgment)

Read `intermediate.json` and make these decisions:

1. **Duplicate resolution**: For each `duplicate_groups` entry, decide whether to merge (keep the
   most detailed description, union tags) or keep separate. Remove redundant findings.
2. **INTENTIONAL downgrade**: For each `intentional_downgrades` entry, downgrade the finding's
   severity to `INFO`. These represent deliberate engineering decisions from previous triage.
3. **Severity re-evaluation**: Load the `severity` skill (`/severity`), then re-assess every
   finding's severity using its criteria. Agents often over-inflate — apply the definitions strictly.
4. **Merge sections**: Combine agent sections with the same category into unified sections.
5. **Executive summary**: Write `overall_assessment`, `summary_text`, `verdict_text`, `verdict_action`.
6. **Agent stats**: Record per-agent unique vs redundant counts.

Write the result as `merged-findings.json` with this structure:

```json
{
  "metadata": { "project": "...", "date": "...", ... },
  "executive_summary": { "overall_assessment": "...", ... },
  "findings": [ { "title": "...", "category": "...", "findings": [...], "positives": "..." } ],
  "agent_stats": [ { "agent": "...", "unique": N, "redundant": N } ],
  "top_findings_override": null,
  "remediation_override": null
}
```

Findings do NOT need `id` fields — the script assigns them in phase 2. Set `top_findings_override`
or `remediation_override` to a JSON array to override auto-generation, or `null` to auto-generate.

### 5c. Phase 2 — Assemble

Run the script to assign IDs, compute statistics, and produce a schema-valid report:

```bash
python3 ${CLAUDE_SKILL_DIR}/../../scripts/consolidate_reports.py assemble \
    --input ${TMPDIR:-/tmp}/merged-findings.json \
    --output ${REPORT_DIR:-.}/report.json
```

The script assigns sequential IDs by category (SEC-001, PROJ-001, RUST-001, etc.), computes
`summary_statistics` (severity counts, category matrix, redundancy ratio), generates
`top_findings` from CRITICAL/HIGH items, and creates `remediation` priority buckets. It
validates against the schema and REFUSES to write output if validation fails (exits with
code 1). Validation is mandatory and blocks output — jsonschema is a hard requirement.

### 5d. Validate report against schema

The assemble step already validates and blocks output on failure, but you can re-validate
manually (e.g., after hand-editing the report):

```bash
python3 ${CLAUDE_SKILL_DIR}/../../scripts/validate_report.py report.json
```

If validation fails, fix the `merged-findings.json` and re-run assemble. Do NOT skip validation.

### 5e. Render markdown report

After validation, generate a human-readable markdown version:

```bash
python3 ${CLAUDE_SKILL_DIR}/../../scripts/generate_review_report.py ${REPORT_DIR:-.}/report.json --format md
```

This produces `report.md` next to the JSON file.

## 6. Iterate if Needed

If initial review reveals areas needing deeper investigation:
- Spawn additional agents with narrower scope
- Re-review specific files with different checklists
- Audit forked dependencies against upstream

## 7. Additional Report Formats (Optional)

If the user requests HTML or PDF versions, invoke the renderer directly:

```bash
python3 ${CLAUDE_SKILL_DIR}/../../scripts/generate_review_report.py ${REPORT_DIR:-.}/report.json --format html
python3 ${CLAUDE_SKILL_DIR}/../../scripts/generate_review_report.py ${REPORT_DIR:-.}/report.json --format pdf
```

For interactive triage, use the `claudius:triage-findings` skill with the `${REPORT_DIR:-.}/report.json` path.

## CI Log Retrieval

See `git-and-github` skill § Context Management for the subagent delegation pattern. CI logs via `get_job_logs` are a prime example — always delegate to a subagent that fetches the log and extracts relevant failure information.

## Anti-Patterns (Review-Specific)

See the general anti-patterns in the Claudius agent prompt. Additional review-specific pitfalls:

1. **Skipping scope assessment**: Always assess scale first. The agent mix and split strategy
   depend on whether the review is small, medium, or large.
2. **Missing comparison base**: Review agents need to know what changed. Always include the
   git diff or git show commands in the prompt.
3. **No deduplication**: Multiple agents will flag the same issue (e.g., `.unwrap()` panics).
   Always consolidate and deduplicate before presenting findings.
