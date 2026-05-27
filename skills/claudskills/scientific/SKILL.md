---
name: scientific
description: Scientific-methodology skills for the SciTeX ecosystem — publication-quality figures, statistics, experiment reproducibility. Distinct from `general/` (which covers package engineering) and per-package skills (which cover package-specific APIs). Load when authoring analysis scripts, preparing figures for manuscripts, or checking scientific rigour of ecosystem output.
user-invocable: false
primary_interface: mixed
tags: [scitex-python, scitex-scientific, scitex-package, research, paper]
invocation:
  - "how should my figure look for a paper"
  - "comparison plot rules"
  - "multi-panel layout standards"
  - "PDF report layout"
  - "which stats test should I use"
context_tokens_total: 1200
canonical-location: scitex-python/src/scitex/_skills/scientific/SKILL.md
---

# SciTeX Scientific Standards

`pip install scitex` — scientific-methodology conventions shared across every ecosystem package that produces research artefacts.

These complement (never duplicate) the engineering rules in [../general/SKILL.md](../general/SKILL.md). General covers *how a package is built*; scientific covers *how the research outputs should look*.

## Sub-skills

### 1. Figures
- [01_figures_01_standards.md](01_figures_01_standards.md) — Universal scientific-figure standards: comparison rules (shared color scale, aligned axes), multi-panel layout, color maps, PDF report layout. Pairs with `figrecipe/21_scientific-figure-patterns.md` for matplotlib code.

### 2. Research project — how a research project *consumes* SciTeX
Project structure split into one leaf per top-level directory:
- [02_research-project_01_project-structure-root.md](02_research-project_01_project-structure-root.md) — Repo-root rules, allowed files, forbidden top-level dirs, `./docs/`, hidden dirs (`.dev`, `.old`, `./.scitex/<pkg-short>/`)
- [02_research-project_02_project-structure-scripts.md](02_research-project_02_project-structure-scripts.md) — `./scripts/` as the primary code location, `@stx.session` entry-point pattern, numbered analysis pipelines
- [02_research-project_03_project-structure-config-and-data.md](02_research-project_03_project-structure-config-and-data.md) — `./config/` YAML tree, `./data/` inputs+intermediate, project-scope `./.scitex/<pkg-short>/`, output discipline
- [02_research-project_04_project-structure-makefile.md](02_research-project_04_project-structure-makefile.md) — `./scripts/makefile/` dispatcher + research-specific targets (run-pipeline / repro / eval)
- [02_research-project_05_project-structure-examples.md](02_research-project_05_project-structure-examples.md) — Numbered examples + `_out/` artefacts; how research-project examples differ from package examples
- [02_research-project_06_project-structure-tests.md](02_research-project_06_project-structure-tests.md) — `tests/scripts/` mandatory parent, allowed subdirs, public/private mirroring, `audit-project` rules
- [02_research-project_07_config-and-parameters.md](02_research-project_07_config-and-parameters.md) — `@stx.session` and the `CONFIG` object (`SDIR_OUT`, `SDIR_RUN`, YAML deep-merge, CLI/env overrides). Use when adding parameters to a script, debugging config resolution, or auditing an experiment for reproducibility.
