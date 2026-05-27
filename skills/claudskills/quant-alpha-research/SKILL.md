---
name: quant-alpha-research
description: "Fail-closed crypto quant alpha research for repo-native Stage 0/0.5 validation, falsification, provider concordance, and promotion decisions. Use to find/validate alpha, execute quant research roadmaps, audit promotion evidence, turn market commentary into hypotheses, or decide if alpha reruns are allowed; Chinese triggers include 寻找新alpha、验证这个alpha、执行量化研究路线图 and synonyms. Do not use for generic finance, CSV/charting, product Stage 0, unrelated provider debugging, or GitHub/frontend work."
---

# Quant Alpha Research

## Overview

Use this skill to turn quant ideas into falsifiable repo-native research work. Prefer rejection-first evidence, current artifacts, small executable slices, and explicit pass/fail reporting over broad brainstorming.

## Operating Stance

- Treat every alpha as false until it survives current data-quality, out-of-sample, holdout, shuffle, cost, and capacity checks.
- Use current repo docs and artifacts as the source of truth. Memory and older reports can orient the search, but must not be treated as current proof.
- If the user asks to execute a roadmap or start Stage 0, do the empirical slice instead of extending architecture discussion.
- If the user asks for analysis-only, keep it analysis-only and avoid file edits.
- If the user asks for read-only validation, do not write to the source repo. Load `references/patterns.md` for the detailed read-only workflow.
- Keep provider coverage, provider concordance, alpha validation, falsification, and promotion status separate.
- Do not bypass live-trading, governance, or promotion boundaries to make a candidate look deployable.
- Protect unrelated user changes. Read `git status` before editing a repo and avoid touching unrelated dirty files.

## Tool Boundary

- Start with read-only commands: `git status`, targeted file reads, `rg`, and artifact inspection.
- Edit only after the user asks for implementation or roadmap execution.
- Never change manifests, promotion state, live-trading config, provider credentials, or canonical-parent labels unless the task explicitly requires it and current gates support it.
- Do not copy secrets, raw private artifacts, or API responses into the skill or public reports.

## Workflow

1. Orient from the current repo.
   - Read the most recent planning docs, candidate reports, promotion cards, and relevant artifacts.
   - Identify the current canonical parent, horizon, data surface, and active blockers.
   - Prefer targeted reads over broad artifact scans.

2. Convert the request into a research contract.
   - State the mechanism, data source, horizon, landing shape, comparison parent, and fail-closed blockers.
   - Choose a narrow first slice that can produce evidence quickly.
   - For external articles or threads, separate source claims from repo-verified conclusions.

3. Choose the landing shape before coding.
   - Consider `gate`, `veto`, `replacement`, `delayed entry`, `capacity haircut`, `sleeve activation`, or `score perturbation`.
   - Prefer selection-layer rules when prior smooth overlays have transmitted weakly or stayed at-par.
   - Require a reason before changing a manifest, canonical parent, or promotion state.

4. Build the smallest Stage 0 that can reject the idea.
   - Reuse repo-native loaders, feature builders, reports, and tests.
   - Write a report or artifact only where the repo already stores quant research evidence.
   - Record coverage, event counts, changed rows, forward returns, costs, and comparison parent metrics.

5. Falsify before optimizing.
   - Run delay, time shuffle, label shuffle, symbol holdout, liquidity-bucket, cost/funding, capacity, and provider-sensitivity checks when relevant.
   - Stop fail-closed if data trust cannot be proved.
   - Do not promote based only on pairwise uplift, attractive Sharpe, or factor-level IC.

6. Report in decision form.
   - Lead with `go`, `no-go`, `watch`, `blocked`, or `research-only`.
   - List exact artifacts, commands run, tests, and remaining blockers.
   - If no credible alpha exists, say so clearly and rank the next falsification or data-unlock step.

7. Verify the research output.
   - Re-run the repo-native tests, reports, or read-only evidence probes needed for the decision.
   - For output-quality checks, compare the answer against current artifacts rather than memory or thesis appeal.

## Decision Tree

- New alpha request: read the current roadmap and canonical parent, then produce one net-new candidate lane plus Stage 0 validation.
- Existing candidate review: start from promotion and falsification artifacts, not from thesis appeal.
- Roadmap execution: treat the document as an execution contract and produce concrete artifacts or runs.
- Provider/data request: separate fill/coverage from concordance/trust, then decide whether alpha reruns are allowed.
- External article/thread: write source-bounded mechanisms, hypotheses, and Stage 0 tests; do not summarize as market commentary only.
- Long-running job status: verify live process state and append-only output growth, not just terminal text.

## References

Load only the reference needed for the current request:

- `references/patterns.md`: repo patterns and anti-patterns from crypto quant-research lanes.
- `references/stage0_and_falsification.md`: required Stage 0 fields, falsification matrix, and promotion blockers.
- `references/output_templates.md`: compact decision-report templates.

## Output Contract

For alpha decisions, include:

- candidate or lane name
- parent/comparator and horizon
- data sources and trust status
- Stage 0 result or blocker
- falsification status
- promotion status
- next executable action

Never collapse `validated`, `passed falsification`, and `promotable` into one label.
