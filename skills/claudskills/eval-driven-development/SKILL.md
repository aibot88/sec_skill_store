---
name: eval-driven-development
description: "Use when reasoning about building language-model-integrated systems by writing evaluations before and alongside the system: the statistical (not binary) nature of LLM evals, the five primitives (dataset, evaluation function, aggregation, iteration loop, regression budget), the judgment-mechanism taxonomy (programmatic, model-graded, human-graded, preference comparison), the difference between system-specific evals and canonical benchmarks (MMLU, HumanEval, BIG-bench, GAIA), how evals drive prompt/model/scaffolding/tooling changes, why Goodhart's Law means higher eval scores are not always improvements, and the offline-eval-vs-production-telemetry distinction. Do NOT use for deterministic unit testing (use testing-strategy), production monitoring (use evaluation or error-tracking), general-software TDD (use testing-strategy), or the construction of individual eval rubrics and task sets (use agent-eval-design — it owns construction; this skill owns the iteration discipline)."
license: MIT
allowed-tools: Read Grep
metadata:
  metadata: "{\"schema_version\":6,\"version\":\"1.0.0\",\"type\":\"capability\",\"category\":\"agent\",\"domain\":\"agent/evaluation\",\"scope\":\"reference\",\"owner\":\"skill-graph-maintainer\",\"freshness\":\"2026-05-16\",\"drift_check\":\"{\\\\\\\"last_verified\\\\\\\":\\\\\\\"2026-05-16\\\\\\\"}\",\"eval_artifacts\":\"planned\",\"eval_state\":\"unverified\",\"routing_eval\":\"absent\",\"comprehension_state\":\"present\",\"stability\":\"experimental\",\"keywords\":\"[\\\\\\\"eval-driven development\\\\\\\",\\\\\\\"LLM evals\\\\\\\",\\\\\\\"evaluation harness\\\\\\\",\\\\\\\"benchmark\\\\\\\",\\\\\\\"HumanEval\\\\\\\",\\\\\\\"MMLU\\\\\\\",\\\\\\\"BIG-bench\\\\\\\",\\\\\\\"GAIA\\\\\\\",\\\\\\\"LLM-as-judge\\\\\\\",\\\\\\\"model-graded eval\\\\\\\",\\\\\\\"pass rate\\\\\\\",\\\\\\\"regression budget\\\\\\\",\\\\\\\"Goodhart's law\\\\\\\",\\\\\\\"golden dataset\\\\\\\",\\\\\\\"reference-free eval\\\\\\\"]\",\"triggers\":\"[\\\\\\\"how do we know this prompt change improved things\\\\\\\",\\\\\\\"should this be an eval or a unit test\\\\\\\",\\\\\\\"the model passes the benchmark but fails in production\\\\\\\",\\\\\\\"what should we measure\\\\\\\",\\\\\\\"the LLM-as-judge gives different scores each run\\\\\\\"]\",\"examples\":\"[\\\\\\\"design an offline eval suite for an LLM-integrated summarization feature before writing the prompt\\\\\\\",\\\\\\\"decide between programmatic grading, model-graded judgment, and human review for a freeform-output eval\\\\\\\",\\\\\\\"explain why MMLU score is a poor predictor of a domain-specific assistant's quality\\\\\\\",\\\\\\\"structure an iteration loop where each prompt change is gated by a regression budget\\\\\\\"]\",\"anti_examples\":\"[\\\\\\\"write unit tests for a deterministic data transformation (use testing-strategy)\\\\\\\",\\\\\\\"set up production alerting on API error rates (use observability)\\\\\\\",\\\\\\\"interpret a specific benchmark's leaderboard (use benchmarking-engine)\\\\\\\"]\",\"relations\":\"{\\\\\\\"related\\\\\\\":[\\\\\\\"tool-call-flow\\\\\\\",\\\\\\\"prompt-injection-defense\\\\\\\",\\\\\\\"testing-strategy\\\\\\\",\\\\\\\"type-safety\\\\\\\",\\\\\\\"agent-eval-design\\\\\\\",\\\\\\\"evaluation\\\\\\\"],\\\\\\\"boundary\\\\\\\":[{\\\\\\\"skill\\\\\\\":\\\\\\\"testing-strategy\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"testing-strategy owns deterministic-software testing where every run is binary pass/fail; this skill owns LLM evaluation where every run is a sample from a distribution and pass-rate is the unit of judgment. The disciplines share vocabulary (suite, gate, regression) but the math underneath differs.\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"tool-call-flow\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"tool-call-flow owns the protocol cycle by which a model invokes tools; this skill owns the discipline of measuring whether that cycle produces correct behavior. Tool-call evals are a specialization of the general pattern.\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"prompt-injection-defense\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"prompt-injection-defense owns the security property; this skill owns the measurement of whether the property holds. Red-team evals against an injection corpus are one application of eval-driven-development.\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"agent-eval-design\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"agent-eval-design owns the construction of evals — task sets, rubrics, graders, hard negatives, traces; this skill owns the development discipline that uses constructed evals to gate every change to prompt, model, retrieval, scaffolding, or tooling. The two compose: agent-eval-design produces the suite; this skill applies it.\\\\\\\"},{\\\\\\\"skill\\\\\\\":\\\\\\\"type-safety\\\\\\\",\\\\\\\"reason\\\\\\\":\\\\\\\"type-safety owns the compile-time property of programs; this skill owns the runtime-distributional property of LLM outputs. They are both validate-at-the-boundary disciplines with different threat models.\\\\\\\"}],\\\\\\\"verify_with\\\\\\\":[\\\\\\\"testing-strategy\\\\\\\",\\\\\\\"agent-eval-design\\\\\\\"]}\",\"mental_model\":\"|\",\"purpose\":\"|\",\"boundary\":\"|\",\"analogy\":\"Eval-driven development is to LLM system engineering what crash-test ratings are to automotive safety — you do not ship a car based on how well it parked in your driveway; you ship it after a battery of standardized tests on representative crash scenarios, with the pass-rate against named criteria as the gating signal. A score of 4.3 stars across the suite is the only defensible claim of 'safer'; a developer's intuition that 'the new model feels smarter' is the unmeasured equivalent of 'I drove it home, it seemed fine.'\",\"misconception\":\"|\",\"concept\":\"{\\\\\\\"definition\\\\\\\":\\\\\\\"Eval-driven development is the practice of building language-model-integrated systems by writing evaluations before and alongside the system, where each evaluation defines a behavioral criterion the system must satisfy on a representative input set, and the suite's aggregated pass-rate signal gates every change to the prompt, model, retrieval, scaffolding, or tooling. Evals are the LLM analog of automated tests for deterministic software with one fundamental difference: LLM evals are statistical (pass-rate over a sampled population) rather than binary (pass/fail per run), because the system under test is itself stochastic. The discipline is the rigorous separation of generation (what the system produces) from judgment (how it is scored) with explicit accounting for the uncertainty in both.\\\\\\\",\\\\\\\"mental_model\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"purpose\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"boundary\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"taxonomy\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"analogy\\\\\\\":\\\\\\\"|\\\\\\\",\\\\\\\"misconception\\\\\\\":\\\\\\\"|\\\\\\\"}\",\"skill_graph_source_repo\":\"https://github.com/jacob-balslev/skill-graph\",\"skill_graph_protocol\":\"Skill Metadata Protocol v5\",\"skill_graph_project\":\"Skill Graph\",\"skill_graph_canonical_skill\":\"skills/eval-driven-development/SKILL.md\"}"
  skill_graph_source_repo: "https://github.com/jacob-balslev/skill-graph"
  skill_graph_protocol: Skill Metadata Protocol v4
  skill_graph_project: Skill Graph
  skill_graph_canonical_skill: skills/eval-driven-development/SKILL.md
---

# Eval-Driven Development

## Coverage

The practice of building language-model-integrated systems by writing evaluations before and alongside the system, and using the eval suite's aggregated pass-rate signal to gate every change. Covers the statistical (not binary) nature of LLM evaluation, the five primitives (dataset, evaluation function, aggregation, iteration loop, regression budget), the judgment-mechanism taxonomy (programmatic / model-graded / human-graded / hybrid), the distinction between system-specific evals and canonical public benchmarks (MMLU, HumanEval, BIG-bench, GAIA, MT-Bench), why higher scores are not always improvements (Goodhart's Law), the difference between offline evals and production telemetry, and the eval-lifecycle archetypes (acceptance, regression, calibration, red-team, cross-model).

## Philosophy

Building LLM-integrated systems without evals is shipping airplanes based on how good the model feels at the desk. The system's behavior is stochastic, the input space is open-ended, and the developer's pet examples are not a representative sample of what users will throw at it. An eval suite is the empirical measurement instrument that lets a team distinguish "the new prompt works better" from "the new prompt works better on the five examples I happened to try."

The discipline's hard part is not writing evals. It is choosing what to measure, encoding the choice into a grader the team agrees with, sampling a dataset that represents production, and resisting the gravitational pull of Goodhart's Law as the eval suite becomes the optimization target. Teams that get this right ship systems whose quality matches their team's stated definition of "good." Teams that get this wrong ship systems that ace evals and disappoint users.

Eval-driven development is not test-driven development with extra noise. It is empirical engineering applied to systems whose behavior is a distribution rather than a value. The vocabulary overlaps; the math underneath does not.

## The Five Primitives In Practice

| Primitive | What it is | Common encoding | Failure mode if neglected |
|---|---|---|---|
| Eval dataset | Curated input examples that represent production | JSONL of `{input, reference}` records; checked into version control | "It works for me" with no shared evidence |
| Evaluation function | Per-example grader producing a score | Python function, model-graded prompt template, or human-review UI | Implicit, undocumented definition of "good" |
| Aggregation | Statistical summary across the dataset | Pass-rate, weighted pass-rate, stratified pass-rate, distribution | Headline number obscures pattern of failure |
| Iteration loop | Eval → diagnose → change → eval | CI-integrated pipeline; eval results in PR comment | Changes ship without measurement |
| Regression budget | Defined acceptable change per metric | Per-eval policy: "must not regress" / "improvement gates merge" / "watchful" | Every change becomes a debate about the headline number |

## Judgment Mechanism Selection

| Mechanism | Best for | Cost per example | Reliability | Watch for |
|---|---|---|---|---|
| Programmatic | Outputs with mechanical correctness (code, JSON validity, exact match) | $0 | Deterministic | Narrow applicability — won't work for freeform output |
| Model-graded | Open-output tasks at scale (summarization, classification, freeform Q&A) | $0.001-$0.10 per grade depending on model | Correlated error with the system being graded | Verbosity bias, position bias in pairwise; calibrate against humans |
| Human-graded | Subjective criteria, calibration runs, ambiguous outputs | $1-$50 per grade depending on annotator | Highest validity; lowest scale | Inter-rater agreement must be measured; one rater is not "humans think" |
| Hybrid | Production systems | Mixed | Mixed | Standard setup: programmatic gates, model-graded scales, human samples calibrate |

A practical default: programmatic checks for the parts you can mechanically verify, model-graded for the open parts, periodic human review to calibrate.

## Iteration Loop Discipline

The eval-driven iteration loop is the development cycle. Run the suite, diagnose failures, identify the change, re-run, gate the change on regression budget.

```
┌─────────┐    ┌──────────┐    ┌──────────────┐    ┌──────────┐
│ Eval    │ -> │ Diagnose │ -> │ Change       │ -> │ Re-run   │
│ baseline│    │ failures │    │ (prompt,     │    │ Eval     │
│         │    │          │    │  model,      │    │          │
│         │    │          │    │  retrieval,  │    │          │
│         │    │          │    │  tooling)    │    │          │
└─────────┘    └──────────┘    └──────────────┘    └──────────┘
                                                          │
                                                          v
                                                ┌──────────────────┐
                                                │ Compare against  │
                                                │ regression budget│
                                                │ Merge / iterate  │
                                                └──────────────────┘
```

The discipline is keeping the suite stable while the system changes. If both move in the same iteration, the comparison anchor is gone and the team is doing parallel experiments.

## Public Benchmarks — Cited For Grounding, Not For Gating

Benchmarks measure cross-system capability against a shared standard. They predict how a model will do on the *exact* tasks the benchmark contains. They do not predict how your specific system, on your specific user inputs, with your specific prompts and retrieval, will perform.

| Benchmark | Measures | Cited for |
|---|---|---|
| MMLU (Hendrycks et al., 2021) | 57 subjects of multiple-choice general knowledge | Breadth of general capability |
| HumanEval (Chen et al., 2021) | 164 programming problems graded by test execution | Code-generation correctness baseline |
| BIG-bench (Srivastava et al., 2022) | 200+ tasks across the long tail of NLP | Breadth of niche capabilities |
| GAIA (Mialon et al., 2023) | General-assistant multi-step tasks with tool use | Realistic agentic-task baseline |
| MT-Bench / Chatbot Arena (Zheng et al., 2023) | Pairwise preference comparison for chat | Human-aligned preference signal |

The right use: pick a model partly on benchmark performance, then build system-specific evals to gate the actual deployment.

## Goodhart's Law In Eval Practice

When the eval becomes the optimization target, the eval ceases to be a good measure. Symptoms:

- Pass-rate climbs while human reviewers' confidence in the system flattens or declines.
- Prompt changes produce phrasings the grader rewards but users dislike (e.g., verbose hedging that scores well on rubric, reads poorly on screen).
- The system memorizes patterns specific to the eval dataset (over-fitting to test cases).
- A held-out evaluation set, scored fresh, shows worse pass-rate than the development set.

Defenses:

- **Hold out a portion of the dataset from active iteration.** Score it periodically; if held-out and development pass-rates diverge, the iteration is over-fitting.
- **Periodically refresh the eval dataset.** Replace some examples with new production-sampled inputs to prevent the dataset from going stale.
- **Calibrate model-graders against humans.** A grader that has drifted from human judgment can produce high pass-rates on outputs humans dislike.
- **Track multiple criteria.** A single headline number is easier to over-fit than a panel of independent measures.

## What This Skill Is Not

This skill is the *concept* of eval-driven development. Specific topics with their own scope:
- The mechanics of running evals in CI/CD pipelines belong to a tooling skill.
- The construction of individual eval rubrics, task sets, graders, and hard negatives belongs to `agent-eval-design`.
- The deterministic testing of non-LLM code belongs to `testing-strategy`.
- The production monitoring of running systems belongs to observability and reliability skills.
- The obra/superpowers `test-driven-development` skill (on skills.sh) is a process-shape workflow skill for general software TDD; this one is the concept-shape complement for the LLM-specific evaluation discipline.

## Verification

After applying this skill, verify:
- [ ] An eval dataset exists, is checked into version control, and is representative of the system's actual production input distribution.
- [ ] Each eval criterion has a defined judgment mechanism (programmatic, model-graded, or human-graded), and the mechanism's known biases are accounted for.
- [ ] Aggregation reports pass-rate with sample size and either a confidence interval or a defined minimum-detectable-change threshold.
- [ ] Each eval has an explicit regression budget: gating (no regression allowed), optimizing (improvement gates merge), or watchful (tracked, not gated).
- [ ] Model-graded evals have been calibrated against human review on a sample within the past quarter (or whatever cadence the team has agreed to).
- [ ] A held-out portion of the dataset is reserved from active iteration and scored periodically to detect over-fitting.
- [ ] The eval suite is integrated into the change workflow — prompt changes, model upgrades, retrieval changes, and tooling changes are all gated by the suite.
- [ ] Public benchmarks (MMLU, HumanEval, etc.) are cited for model-selection grounding but are not the gating decision for system-specific quality.
- [ ] Production telemetry exists separately from the offline eval suite; one is not used as a substitute for the other.
- [ ] The shipping threshold is a product decision documented somewhere, not an emergent average across team opinion.

## Do NOT Use When

| Instead of this skill | Use | Why |
|---|---|---|
| Writing deterministic unit tests for non-LLM code | `testing-strategy` | testing-strategy owns binary pass/fail testing; this skill owns distributional measurement |
| Designing individual eval rubrics, task sets, graders, hard negatives | `agent-eval-design` | agent-eval-design owns eval construction; this skill owns the iteration discipline that uses constructed evals |
| Setting up production monitoring, alerting, or telemetry | `evaluation` (general framing) or `error-tracking` | those own runtime measurement of deployed systems; this skill owns offline pre-deployment measurement |
| Reasoning about the protocol cycle of tool calls | `tool-call-flow` | tool-call-flow owns the cycle; eval-driven development can measure tool-call correctness as one criterion |
| Defending against prompt injection | `prompt-injection-defense` | prompt-injection-defense owns the security property; this skill can measure whether the defense holds |
| General software TDD process | the obra/superpowers `test-driven-development` skill or `testing-strategy` | TDD is process-shape for general software; this skill is concept-shape for the LLM-specific evaluation discipline |

## Key Sources

- Hendrycks, D., Burns, C., Basart, S., Zou, A., Mazeika, M., Song, D., & Steinhardt, J. (2021). ["Measuring Massive Multitask Language Understanding"](https://arxiv.org/abs/2009.03300). The MMLU benchmark paper; foundational reference for cross-system general-knowledge evaluation.
- Chen, M., Tworek, J., Jun, H., Yuan, Q., et al. (2021). ["Evaluating Large Language Models Trained on Code"](https://arxiv.org/abs/2107.03374). The HumanEval benchmark paper; foundational for code-generation evaluation.
- Srivastava, A., et al. (2022). ["Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models"](https://arxiv.org/abs/2206.04615). The BIG-bench paper; canonical reference for breadth-of-capability evaluation across 200+ tasks.
- Mialon, G., Fourrier, C., Swift, C., Wolf, T., LeCun, Y., & Scialom, T. (2023). ["GAIA: A Benchmark for General AI Assistants"](https://arxiv.org/abs/2311.12983). The GAIA benchmark paper; canonical reference for evaluating multi-step assistant tasks with tool use.
- Zheng, L., Chiang, W.-L., et al. (2023). ["Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"](https://arxiv.org/abs/2306.05685). The MT-Bench paper; canonical reference for LLM-as-judge methodology, including known biases.
- OpenAI. [Evals framework on GitHub](https://github.com/openai/evals). Open-source framework for writing and running LLM evals; documents the practical mechanics of the discipline.
- Anthropic. [Building evals — Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/skills/classification) and [Evaluation guide](https://docs.anthropic.com/en/docs/test-and-evaluate/develop-tests). Practitioner-oriented guidance on building eval suites.
- UK AI Safety Institute. [Inspect: An open-source evaluation framework](https://inspect.ai-safety-institute.org.uk/). Open framework purpose-built for capability and safety evaluations of LLMs.
- Goodhart, C. (1975). "Problems of Monetary Management: The U.K. Experience." The origin of Goodhart's Law as commonly cited; "when a measure becomes a target, it ceases to be a good measure."
- Liang, P., et al. (2022). ["Holistic Evaluation of Language Models"](https://arxiv.org/abs/2211.09110). The HELM framework paper; argues for multi-metric eval across many dimensions as a counter to single-metric Goodharting.
