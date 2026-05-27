---
name: problem-locating-solving
description: "Use when locating a bug in an unfamiliar codebase, tracing a failure from symptom to source, or choosing between candidate fixes after the symptom is observed but before a patch lands. Covers the locate-to-solve workflow: problem-statement contract, search-space reduction, boundary-based fault localization, good-vs-bad path comparison, binary search through a call chain, minimal repro, root-cause isolation, fix option comparison, blast-radius review, and post-fix verification. Do NOT use for broad task planning once the bug is localized, test-pyramid design, or performance forensics."
license: MIT
compatibility: "Language- and stack-agnostic. The locate-to-solve loop, boundary-localization techniques, and verification rules apply to any software bug investigation; specific tool names (binary search, git bisect, MRE) are illustrative — substitute the equivalents of your stack."
allowed-tools: Read Grep
metadata:
  schema_version: "4"
  version: "1.0.0"
  type: workflow
  category: knowledge
  domain: engineering/debugging
  scope: portable
  owner: skill-graph-maintainer
  freshness: "2026-05-06"
  drift_check: "{\"last_verified\":\"2026-05-06\"}"
  eval_artifacts: planned
  eval_state: unverified
  routing_eval: absent
  stability: experimental
  keywords: "[\"locate a defect in unfamiliar codebase\",\"failing-boundary identification\",\"first failing boundary\",\"find where defect originates\",\"trace symptom backward to source\",\"search-space reduction by symptom type\",\"boundary-based fault localization\",\"locate-to-solve workflow\",\"search-space bounding rules\",\"entry-point tracing technique\",\"differential good-path vs bad-path comparison\",\"binary-search a long call chain\",\"minimal repro for noisy stateful failure\",\"multi-option fix candidate comparison\",\"lowest-blast-radius fix selection\",\"blast-radius comparison between fix candidates\",\"neighbor-path side-effect check\",\"explanation-check on a proposed fix\",\"post-fix reflection prevention promotion\"]"
  examples: "[\"this route returns 500 but I have no idea where the failure starts — walk me through finding the boundary\",\"I have a wrong-total bug — show me how to locate the divergence point\",\"the build broke after a merge but the error trace is a cascade — which file should I open first?\",\"I see the symptom but I am still in discovery — bound the search space for me\",\"two candidate fixes for this null-pointer crash — compare blast radius between them\",\"I have an unfamiliar codebase and need to find where this report is computed wrong\",\"what step in the locate-to-fix workflow did I skip — the bug came back under different inputs\"]"
  anti_examples: "[\"plan the next 6 weeks of work for the team\",\"review this PR for code quality\",\"this endpoint is slow under load — find the bottleneck\",\"scan this repo for OWASP top 10 vulnerabilities\",\"run scientific-method debugging on this stack trace\",\"I see the symptom but cannot find the root cause of this nil panic\",\"classify this failure into a problem class before debugging\",\"pin this regression so the same bug can't slip through again\",\"decide what test pyramid this feature needs\"]"
  relations: "{\"boundary\":[{\"skill\":\"debugging\",\"reason\":\"debugging is the *execution* of one chosen technique against an already-localized bug; problem-locating-solving is the workflow that produces the localization — same 'I have a bug, what do I do?' prompt routes to debugging when the class is known and to problem-locating-solving when localization is needed first\"},{\"skill\":\"testing-strategy\",\"reason\":\"testing-strategy owns the framework for what tests to write to lock in the absence of a bug class (regression suite design, test pyramid, coverage strategy); problem-locating-solving uses a single verification test as one phase of its locate-to-fix workflow but does not own test design — same 'pin this regression' prompt routes to testing-strategy when the question is what test to write, not how to find the bug\"},{\"skill\":\"code-review\",\"reason\":\"code-review evaluates the quality and correctness of a specific change at PR scope (proactive); problem-locating-solving investigates already-broken behaviour (reactive) — both can apply to 'look at this code,' but the routing differs by whether a failure has already been observed\"},{\"skill\":\"refactor\",\"reason\":\"refactor restructures non-broken code for clarity or maintainability; problem-locating-solving finds and fixes broken code — same 'this code needs change' prompt routes by whether the trigger is a failure (locate) or a quality concern (refactor)\"}],\"related\":[\"pattern-recognition\",\"diagnosis\",\"lint-overlay\"],\"verify_with\":[\"tool-call-strategy\",\"context-graph\",\"graph-audit\"]}"
  portability: "{\"readiness\":\"scripted\",\"targets\":[\"skill-md\"]}"
  lifecycle: "{\"stale_after_days\":365,\"review_cadence\":\"quarterly\"}"
  skill_graph_source_repo: "https://github.com/jacob-balslev/skill-graph"
  skill_graph_protocol: Skill Metadata Protocol v3
  skill_graph_project: Skill Graph
  skill_graph_canonical_skill: skills/problem-locating-solving/SKILL.md
  skill_graph_export_description: shortened for Agent Skills 1024-character description limit; canonical source keeps the full routing contract
  skill_graph_canonical_description_length: "1130"
---

# Problem Locating and Solving

## Coverage

End-to-end bug localization workflow: problem-statement construction, search-space reduction by symptom type, boundary-based fault localization (entry-point tracing, differential comparison, binary search, minimal repro, search-before-read), root-cause isolation (symptom vs cause analysis with stop conditions), multi-option fix generation across local-patch / guardrail / structural classes, blast-radius comparison between candidates, implementation rules that bind the fix to a regression-proofing artifact, five verification types (repro test, regression test, neighbor check, blast-radius check, explanation check), and a four-question post-fix reflection that promotes one-off fixes into prevention mechanisms when the class could recur.

## Philosophy

The most common debugging failure is not lack of skill — it is skipping steps. Agents jump from symptom to fix without isolating the root cause, which produces patches that hide bugs instead of removing them. This skill exists for the gap between "something is wrong" and "the right fix is verified."

Every step in the loop has been added because skipping it caused a real false fix. Knowing debugging theory is not enough — you need a repeatable way to find the failing boundary, isolate the actual cause, compare solution options, and prove the fix closes the problem without widening the blast radius. The loop is the process; intuition without the loop produces patches that look like fixes and re-emerge under different inputs two days later.

## Workflow

Use the ordered phases, checklists, and guardrails in the sections below as the canonical workflow for this skill. When multiple subsections describe steps, follow them in the order presented.

## 1. The Locate-to-Solve Loop

Use this loop in order. Skipping steps creates false fixes.

1. Define the problem precisely.
2. Bound the search space.
3. Locate the first failing boundary.
4. Isolate the root cause.
5. Generate multiple fix options.
6. Choose the lowest-blast-radius fix that prevents recurrence.
7. Verify with regression evidence.
8. Reflect on what should now be prevented or documented.

## 2. Problem Statement Contract

Before searching the codebase, write the problem in a concrete form.

| Field | Required question |
| --- | --- |
| What | What is failing? |
| Where | Which route, job, component, file, or workflow shows the failure? |
| When | Under what timing, input, environment, or user state does it happen? |
| Expected | What should happen instead? |
| Actual | What observable result occurs now? |
| Impact | Why does this matter: correctness, UX, security, cost, or trust? |

If one of these is missing, the search space is still too loose.

## 3. Bound the Search Space

Do not search the whole repo emotionally. Reduce the space first.

### Search-space reduction table

| Symptom type | Start boundary | Fastest first move |
| --- | --- | --- |
| Route / API failure | Request handler → service → query | Find the route entry point and first downstream call |
| UI bug | Visible component → state source → async edge | Identify the first component that renders wrong data |
| Data mismatch | Read model → transform → source table | Compare the final number against the nearest prior stage |
| Scheduled job issue | Cron trigger → worker → provider call | Find where the run first diverges from normal logs |
| Build / test failure | First failing file → import chain → config | Start from the first deterministic error, not the last cascade |

### Bounding rules

- Prefer the first failing boundary over the final visible symptom.
- Prefer the smallest reproducible path over the full production path.
- Prefer one confirmed stack trace or failing assertion over broad speculation.
- If you cannot name the likely subsystem, you are still in discovery, not fixing.

## 4. Locate the First Failing Boundary

The critical move is to find the first point where reality stops matching the expected flow.

| Technique | Use when | Result |
| --- | --- | --- |
| Entry-point tracing | You know the failing route or component | Narrows owner path quickly |
| Differential comparison | Good path vs bad path exists | Exposes the divergence point |
| Binary search through the path | Flow has many stages | Cuts search space fast |
| Minimal repro | Failure is noisy or stateful | Produces a smaller truth surface |
| Search-before-read | Codebase is unfamiliar | Finds candidate files without flooding context |

### Boundary questions

- Where is the first bad value observed?
- What was the last known-good step immediately before it?
- Is the failure caused by code, data, environment, or timing?
- What single check would prove which of those four buckets owns it?

## 5. Root Cause Isolation

Symptoms are not causes. A cause explains why the symptom appears.

### Cause-isolation pattern

1. State the symptom.
2. Ask what immediate condition makes that symptom possible.
3. Ask what created that condition.
4. Stop only when the answer identifies a fixable logic, data, config, or process cause.

### Symptom vs cause table

| Symptom | Likely cause form |
| --- | --- |
| Timeout | Query shape, retry loop, blocking external dependency |
| Wrong total | Missing component, double count, unit mismatch, null semantics |
| Empty UI state | Fetch never ran, filter mismatch, wrong auth or scoping |
| Intermittent failure | Race, stale cache, background mutation, provider variability |
| Build break | Import drift, type-contract break, config mismatch |

If the proposed fix does not explain why the symptom happened, it is probably still a patch.

## 6. Generate More Than One Fix

Do not lock onto the first plausible solution.

| Fix class | Best for | Tradeoff |
| --- | --- | --- |
| Local patch | Clear isolated mistake | Fastest, but may miss recurrence prevention |
| Guardrail | Bad inputs or state transitions | Safer, but may hide deeper issues if overused |
| Structural fix | Repeated or systemic failures | Highest confidence long-term, but higher change cost |

Generate at least two candidate fixes whenever the root cause is not trivial.

### Compare candidate fixes by

- blast radius
- reversibility
- recurrence prevention
- alignment with existing patterns
- verification cost

Pick the option that solves the root cause with the smallest justified surface area.

## 7. Implementation Rules

- Fix the cause, not only the symptom.
- Add the smallest regression-proofing artifact that fits: test, guard, or doc rule.
- Keep the proof close to the fix: failing case before, passing case after.
- If the fix touches a shared pattern, look for sibling sites that may carry the same defect.

## 8. Verification Rules

The fix is not complete until the original failure mode is proven closed.

| Verification type | Question it answers |
| --- | --- |
| Repro test | Can I still trigger the original bug? |
| Regression test | Will this exact class of bug return silently? |
| Neighbor check | Did the fix break adjacent behaviour? |
| Blast-radius check | Did the changed boundary affect another subsystem? |
| Explanation check | Can I explain why this fix works? |

### Verification minimum

1. Reproduce the failure before the fix when possible.
2. Show the failure no longer occurs after the fix.
3. Check one neighbouring path that could regress.
4. Record the root cause in one sentence.

## 9. Reflection and Prevention

After the fix, ask:

- Was this a one-off or a repeated class of issue?
- Should this become an eval, lint rule, or doc rule?
- Did the real delay come from locating the bug or deciding the fix?
- What clue should future agents notice sooner?

If the same class of bug could reasonably recur, promote the learning into a prevention mechanism.

## Verification

- [ ] I can state the problem in concrete expected-vs-actual terms.
- [ ] I have reduced the search space before opening lots of files.
- [ ] I know the first failing boundary, not just the final symptom.
- [ ] I can explain the root cause in one sentence.
- [ ] I considered more than one fix when the cause was non-trivial.
- [ ] I verified the original failure path and one neighbouring path.
- [ ] I captured any new prevention rule if this problem class could recur.

## Do NOT Use When

| Instead, use | Why |
|---|---|
| `debugging` | Executing scientific-method debugging on an already-localized bug. Debugging owns the per-technique RCA loop; this skill owns the workflow that produces the localization. |
| `code-review` | Reviewing not-yet-broken code for quality and correctness. Code-review is proactive at PR scope; this skill is reactive once a failure has been observed. |
| `refactor` | Restructuring code for clarity or maintainability when nothing is broken. Refactor is for healthy code; this skill is for broken code. |
| `diagnosis` | Triaging an unknown failure into a problem class before debugging begins. Diagnosis owns the per-incident triage; this skill owns the locate-to-fix workflow that runs after triage. |
| `pattern-recognition` | Identifying the recurring class behind many bugs and proposing a structural rule. Pattern-recognition feeds prevention into the reflection step of this workflow but does not own the per-bug localization. |
| `lint-overlay` | Adding the lint rule that automates prevention of the bug class. Lint-overlay owns the rule machinery; this skill decides whether a recurring bug warrants a rule. |
| `tool-call-strategy` | Deciding which tool (Grep / Glob / Read) to use during search-space reduction. Tool-call-strategy owns the tool selection; this skill owns the workflow within which the tools are used. |
| `graph-audit` | Performing dependency and structural audits across the codebase graph. Graph-audit owns the structural perspective; this skill owns the per-bug perspective. |
| `context-graph` | Understanding the relationships between files and modules to estimate blast radius. Context-graph owns the relationship model; this skill consumes it during fix-comparison. |
