---
name: analytic-workbench
description: Use this skill for analytics and data-science workflow setup, exploratory analysis, notebook-first EDA, repo normalization for analysis projects, experiment comparison, AutoML, causal analysis, and promotion from ad hoc exploration into reusable pipelines. Trigger when the user asks for analysis best practices, how to structure an analytics repo, how to organize notebooks and runs, whether to use marimo or Quarto/qmd, how to handle experiment sweeps, how to compare models, or how to make analysis reproducible. Also trigger on phrases such as analytic workbench, EDA, exploratory analysis, notebook workflow, analytics pipeline, reproducible analysis, experiment sweep, hyperparameter comparison, comparison table, marimo, Quarto, qmd, Hamilton, sf-hamilton, dataflow, DAG driver, Hydra, DVC, Kedro, MLflow, AutoML, PyCaret, causal analysis, feature engineering, or model review.
metadata:
  author: kundeng
  version: "1.3.0"
---

# Analytic Workbench

Human-directed, AI-operated analysis. The AI computes; the human steers
through a review surface (marimo notebook or Quarto doc). This is not a batch
pipeline — intermediate findings are presented for redirection at every step.

## Start Here

1. Read `AGENTS.md` or `agents.md` if present
2. If neither exists, create `AGENTS.md` and update `CLAUDE.md` (see below)
3. Inspect the repo before changing structure
4. Separate repo facts from agent assumptions
5. Separate frozen inputs from live pulls

Then establish per area: current mode, likely next mode, **review surface**,
first boundary-sensitive change.

### Fresh Repo Bootstrap

When starting on a repo with no `AGENTS.md`, create one from the initial
prompt and project context. The file anchors all agents to the same workflow
contract.

`AGENTS.md` should contain:

- **Project purpose** — one-paragraph summary derived from the user's request
- **Workflow** — state that this project uses the analytic workbench skill
  with modes `probe → explore → experiment → operate`
- **Current mode** — the mode established in the first `plan` declaration
- **Review surface** — marimo or qmd, chosen at first `plan`
- **Conventions** — module layout (`src/<project>/analysis/`), artifact layout
  (`runs/`, `rawdata/`)
- **Steering rules** — any project-specific constraints from the user's prompt
  (e.g., data sources, review expectations, domain context)

Then ensure `CLAUDE.md` exists and includes a pointer:

```text
See AGENTS.md for project workflow conventions and current mode.
```

If `CLAUDE.md` already exists, append the pointer rather than overwriting.
Update `AGENTS.md` at promote time when modes or conventions change.

## Modes

A mode is a workflow shape, not what you compute. Different areas of work can
be in different modes simultaneously. Every mode has two axes: **what executes
the computation** and **where the human reviews it**.

| Mode | Use when | Execution | Review surface | Read next |
|---|---|---|---|---|
| `probe` | first contact, uncertain framing | bare Python (naming discipline encouraged) | chat + inline figures; marimo optional | this file only |
| `explore` | work worth keeping formally | Hamilton Driver | marimo explore notebook or Quarto EDA doc | `hamilton-guide.md`, `module-conventions.md`, `marimo-patterns.md` |
| `experiment` | reruns, comparisons, sweeps | Hamilton + Hydra | marimo report app or Quarto report + comparison table | `hydra-config.md` |
| `operate` | scale, schedules, team handoff | + orchestrator + MLflow | deployed marimo app or dashboard | `mlflow-guide.md` |

### Execution axis

Each mode adds to the previous — no rewrites.

- **`probe`**: throwaway code, direct fetches. No framework required, but
  **Hamilton naming discipline is always encouraged** — it costs nothing and
  eliminates rewriting at promote. Functions defined in marimo cells can become
  a Hamilton DAG on the fly via `ad_hoc_utils.create_temporary_module()` for
  instant visualization and selective execution. See `hamilton-guide.md` §
  Mode Bridge.
- **`explore`**: pure functions with Hamilton naming discipline. Hamilton Driver
  for automatic DAG resolution, selective execution, visualization, and
  `@check_output` validation.
- **`experiment`**: Hydra for config composition and `--multirun` sweeps.
  Hamilton `@config.when` for variant selection. `.with_cache()` to skip
  redundant upstream computation across reruns.
- **`operate`**: Hamilton runs inside orchestrator tasks (Airflow, Dagster).
  MLflow for experiment tracking. DVC for data versioning and remote storage.

### Review axis

The review surface is what makes this a workbench, not a batch pipeline.
Without it, there is no human steering loop.

- **`probe`**: findings presented in chat with inline figures and tables.
  The conversation *is* the review surface. If working in marimo, the
  notebook is both authoring surface and review surface from day one.
- **`explore`**: **marimo notebook** for interactive exploration (widgets,
  filters, drill-down) or **Quarto doc** for staged narrative EDA. The human
  opens the notebook, runs it, reads the AI's interpretation, and redirects.
  See `marimo-patterns.md`.
- **`experiment`**: **marimo report app** loads pre-computed artifacts from
  `runs/`, shows comparison tables, per-run drill-down, and figures. Or a
  **Quarto report** for stakeholder-facing narrative. See `review-workflow.md`.
- **`operate`**: deployed marimo app or dashboard for ongoing monitoring.

Surface choice rule: prefer **marimo** when the human needs to adjust filters,
select runs, or explore interactively. Prefer **Quarto** when the output is a
staged document, decision memo, or polished report.

### Common mistakes

| Mode | Mistake |
|---|---|
| `probe` | over-structuring early; but also: skipping naming discipline that makes promote free |
| `explore` | logic in cells instead of modules; no review surface; skipping Hamilton |
| `experiment` | adding Hydra before repeated runs exist; no comparison table |
| `operate` | adding Kedro/DVC before team handoff is real |

All references are in `references/`.

## Operators

Five operators drive all work, firing from conversational intent. Default
rhythm: `plan -> run -> review -> summary`, with `promote` inserting when the
current mode's wiring is no longer sufficient.

Each operator must produce a visible declaration.

### plan

Set up or revise the workflow. Fires at start of substantive work or direction
change.

```text
Plan
- Area: ...          - Mode: ...
- Likely next mode: ...
- Primary surface: marimo | qmd | chat-only | other
- Review surface: ...
- First boundary-sensitive change: ...
- Steering docs read: ...
```

Add for ML/causal: `Sampling strategy: ...` and
`Target framing: binary | multiclass | regression | ranking | causal`.

For `probe`: `Area, Mode: probe, First probe, Review surface, Risk`.

### run

Execute the next planned step.

```text
Run                          Run outcome
- Area: ...                  - What ran: ...
- Step: ...                  - Output: ...
- Expected output: ...       - Anomaly or caveat: ...
```

### review

Sanity-check outputs before presenting — fires automatically, not on request.
This is where the human sees intermediate results and can redirect.

```text
Review
- Area: ...
- Artifacts reviewed: ...
- Findings: ...
- Caveats: ...
- Verdict: proceed | revise | back up to [phase]
```

The review declaration summarizes what the human will see in the review surface.
At `explore`+, always point the human to the notebook or doc where they can
inspect results interactively — do not make the chat summary the only artifact.

### summary

Report status at natural stopping points.

```text
EDA Update
- Area: ...       - What ran: ...
- Step: ...       - Outcome: ...
- Caveat: ...     - Next step: ...
```

### promote

Advance to a stronger mode. This is where mode transitions happen — probe to
explore when work is worth keeping, explore to experiment when reruns matter.
Transitions can also emerge from user intent (e.g., asking for comparisons).
Transitions are additive wiring, not rewrites.

```text
Promote
- Area: ...             - From mode: ...
- To mode: ...          - What survives: ...
- What changes: ...
```

## Core Workflow

The analytical spine, used within any mode:

```text
Frame -> Acquire -> Profile -> Hypothesize -> Model or Analyze -> Review -> Promote
```

- **Frame**: question, decision, constraints, **review surface choice**
- **Acquire**: data access as workflow shape, not hidden setup
- **Profile**: coverage, missingness, slices, label shape — **present to human**
- **Hypothesize**: likely drivers before over-engineering
- **Model or Analyze**: execute, then **present intermediate results for steering**
- **Review**: findings early enough to redirect — the human inspects the review
  surface and gives feedback
- **Promote**: worth-keeping work into modules, config, runs, reports, and the
  runbook

Backtrack when stuck:
- Unusable data → Acquire or reframe
- All hypotheses fail → Profile with fresh slices
- Suspicious metrics → check leakage before celebrating
- Wrong assumption surfaced → Frame

## Guardrails

- Prefer what is on disk over generic assumptions
- Do not silently change folder layout, artifact semantics, or execution path — breaks resumption and review
- Once structure exists, stop using throwaway snippets — they diverge from the notebook contract
- First live extraction is usually a run artifact, not a frozen input
- Do not split a phase across half-wired surfaces — hides state, blocks promotion
- Do not let AutoML choose the framing — it optimizes whatever metric you hand it
- Match sampling/CV to temporal, grouped, spatial, or event structure — naive splits leak and inflate
- Keep project knowledge in repo docs, not agent memory
- **Present intermediate findings in the review surface** — do not batch everything to the end

## Acquisition and DAG Shape

`explore`+ follows `references/module-conventions.md`: pure functions in
`src/<project>/analysis/`, function name = output name, parameter name =
dependency name. These conventions are Hamilton's programming model — the
Driver replaces manual call ordering with automatic DAG resolution.

Read `references/hamilton-guide.md` before writing the first `explore`-mode
driver. Key capabilities by mode:

- **`explore`**: `dr.execute(["node"])` for selective execution,
  `dr.display_all_functions()` for DAG review, `@check_output` for validation
- **`experiment`**: `.with_cache()` for rerun speed, `@config.when` for variant
  selection, Hydra feeds config dict to `driver.Builder().with_config(cfg)`
- **`operate`**: Hamilton materializers for I/O separation, Driver called inside
  orchestrator tasks

Notebooks read saved artifacts, not embed live fetch logic.

## ML and Causal Rules

Read `references/modeling-guardrails.md` before modeling. Key rules:

- Frame target before any model runs — unexamined framing wastes downstream work
- Match sampling/CV to data structure
- AutoML as comparison accelerator after framing, not as problem framing
- Predictive importance is not causal effect — keep claims separate
- Interpretability artifacts for important outputs (`references/interpretability.md`)
- Causal design discipline: `references/causal-analysis.md`

## Reference Guide

Read only what the current mode or task needs.

| Reference | When to read | Key content |
|---|---|---|
| `hamilton-guide.md` | before `explore` driver | Driver, caching, `@config.when`, `@check_output`, visualization |
| `module-conventions.md` | before `explore` code | Pure functions, Hamilton-compatible naming, module layout |
| `marimo-patterns.md` | choosing or building review surface | marimo as frontend; explore notebooks; report apps; widgets |
| `review-workflow.md` | presenting results to human | Review before presenting; surface choice; self-review checklist |
| `environment-setup.md` | packaging, imports, deps | Real package setup; no editor-settings patches |
| `hydra-config.md` | entering `experiment` | Config composition, sweeps, experiment configs |
| `artifact-strategy.md` | repeated outputs, comparisons | Materialize clearly; do not mix frozen inputs with run outputs |
| `modeling-guardrails.md` | before modeling | Framing, sampling, leakage, validation discipline |
| `dvc-guide.md` | data versioning, remote storage | Add at `operate` for large data or team remotes |
| `kedro-guide.md` | team needs YAML data catalog | Optional at `operate`; Hamilton + Hydra cover most use cases |

All references are in `references/`.

## Runbook

The runbook (`runbook.md` at the repo root) is the human-readable reproduction
guide. It is derived from project structure — configs, scripts, notebooks,
runs — not maintained as a separate log.

Generate or update at **promote time**: milestones, handoff requests, or mode
transitions. Rewrite stale sections rather than appending.

Contents:

1. **Prerequisites** — env setup, data acquisition, external tools
2. **Pipeline overview** — ASCII diagram of data flow
3. **Numbered steps** — one per major pipeline step, each with: the exact
   command, expected runtime, and what to inspect afterward (including expected
   results so the reader knows what "correct" looks like)
4. **Configuration reference** — table of config files and what they control
5. **Key directories** — paths, contents, git-tracked or not
6. **Troubleshooting** — known failure modes and fixes

The runbook ties per-run artifacts together: `config.yaml` says what params
were used, `metrics.json` says what happened, the runbook says which command
produced the run, what results to expect, and how to open the review surface.

If `.aw/` bookkeeping is active, note the runbook's last-updated timestamp in
`.aw/status.json`.

## Bookkeeping

Maintain `.aw/` when work continues across sessions:

```text
.aw/
  status.json          # current state across all areas
  stages/
    <area-name>/       # one folder per area of work
      plan.md          # framing and plan revisions
      status.json      # machine-readable state
      review.md        # review notes and approvals
```

Create or advance a stage folder only on mode changes or user-requested
checkpoints. Plan revisions, reruns, and parameter changes belong in the
existing folder, not a new one.

Joining mid-project:
- `.aw/status.json` exists → authoritative
- `stages/` but no root status → reconstruct from folders
- Hydra `conf/`/`multirun/` without `.aw/` → likely `experiment`, confirm
- Notebook + modules, no config management → likely `explore`
- Nothing structured → `probe`
