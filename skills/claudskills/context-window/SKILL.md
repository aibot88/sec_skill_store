---
name: context-window
description: "Use when allocating context-window budget across system, skill-injection, working, and output zones; monitoring context health; deciding when to compact; preserving state before compaction; recovering after compaction; or choosing strategies for 1M, 200K, or 128K context windows. Covers zone budgets, practical model-budget tables, the 80% compaction rule, pre/post-compact protocols, persistence hierarchy, operation token costs, and token-reduction techniques. Do NOT use for deciding what information belongs in the working set (use `context-management`), prompt design (use `prompt-craft`), graph architecture (use `context-graph`), or memory curation."
license: MIT
compatibility: "Provider-agnostic. The zone model, 80% rule, persistence hierarchy, and token-reduction techniques apply across Anthropic, OpenAI, Google, and open-weight contexts of any size. Specific token figures are illustrative — substitute the figures of the model you actually run."
allowed-tools: Read Grep
metadata:
  schema_version: "4"
  version: "1.0.0"
  type: capability
  category: knowledge
  domain: ai-engineering/context
  scope: portable
  owner: skill-graph-maintainer
  freshness: "2026-05-06"
  drift_check: "{\"last_verified\":\"2026-05-06\"}"
  eval_artifacts: planned
  eval_state: unverified
  routing_eval: absent
  stability: experimental
  keywords: "[\"context window management\",\"context budget allocation\",\"80% compaction rule\",\"context health states\",\"pre-compact hook\",\"post-compact recovery\",\"cross-session persistence hierarchy\",\"token consumption per operation\",\"deterministic cli vs mcp tool result tokens\",\"targeted file read offset limit\",\"progressive skill disclosure\",\"count mode exploration\",\"1M context window strategy\",\"200K context window strategy\",\"128K context window strategy\",\"checkpoint before compact\",\"continuation signal\",\"what survives compaction\"]"
  examples: "[\"the agent's tool results are starting to truncate — what state are we in and what should I do next?\",\"I have a 1M-context model — does that mean I can ignore budget management?\",\"the session is at 75% context — should I compact now or finish the current operation first?\",\"I just compacted and lost the decision trail; what should the pre-compact hook have preserved?\",\"the agent reads 5 files looking for a function and burns 100K tokens — what's the right pattern?\",\"I'm running on a 128K-context model — what's the per-task budget I can plan against?\",\"what survives compaction and what doesn't, ranked from most to least durable?\",\"the skill payload is 30K and I haven't even read a file yet — how do I shrink it?\"]"
  anti_examples: "[\"decide what context to load or drop in the working set\",\"design the multi-graph architecture for skills + docs + memory\",\"improve the prompt template the agent uses\",\"curate the durable memory index across sessions\",\"which skill should activate for this query\",\"review this AI-generated PR for correctness\",\"the README has drifted from the actual CLI flags — which wins?\",\"the docs have drifted from the code — which is canonical?\"]"
  relations: "{\"boundary\":[{\"skill\":\"context-management\",\"reason\":\"context-management decides what to load and drop in the working set; context-window is the budget math underneath that decides how much fits and when to compact\"},{\"skill\":\"context-graph\",\"reason\":\"context-graph maps the static topology of skills / docs / memory; context-window is the runtime budget for the part of that topology that is actually loaded\"},{\"skill\":\"tool-call-strategy\",\"reason\":\"tool-call-strategy decides which tool to invoke; context-window decides how much budget the result of that tool is allowed to occupy\"},{\"skill\":\"prompt-craft\",\"reason\":\"prompt-craft is wording / structure of one prompt; context-window is the per-session budget the prompt and its results live within\"}],\"related\":[\"context-management\",\"context-graph\",\"tool-call-strategy\",\"context-engineering\"],\"verify_with\":[\"context-management\"]}"
  portability: "{\"readiness\":\"scripted\",\"targets\":[\"skill-md\"]}"
  lifecycle: "{\"stale_after_days\":180,\"review_cadence\":\"quarterly\"}"
  skill_graph_source_repo: "https://github.com/jacob-balslev/skill-graph"
  skill_graph_protocol: Skill Metadata Protocol v3
  skill_graph_project: Skill Graph
  skill_graph_canonical_skill: skills/context-window/SKILL.md
  skill_graph_export_description: shortened for Agent Skills 1024-character description limit; canonical source keeps the full routing contract
  skill_graph_canonical_description_length: "1352"
---

# Context Window

## Coverage

The quantitative discipline behind an agent's working memory. Allocates the context-window budget across three zones: System (system prompt, rules, tool schemas), Skill Injection (the SKILL.md files auto-loaded for the current task), and Working (conversation, tool results, file contents, agent output). Names the three context health states — `ok` (< 60% used), `compact` (60–80%), `exhausted` (> 80%) — and the **80% compaction rule** that compaction must always trigger before the budget is fully consumed, leaving 20% as the safety margin for finishing the current operation, writing the checkpoint, running the closeout protocol, and emitting the continuation signal. Specifies the pre-compact protocol (commit uncommitted changes, write the continuation signal, update the checkpoint, save state that cannot be re-derived from git or disk) and the post-compact recovery flow (re-injection of git status, active-task reference, recent commits, critical findings). Catalogs typical token consumption per operation type (full file read 20–40K, large tool-result JSON 10–30K, single SKILL injection 3–8K, fixed system overhead) and the five token-reduction techniques: deterministic-CLI over heavy MCP / tool-result paths, targeted file reads with `offset` + `limit` instead of full-file reads, search-before-read (grep first, read the match), progressive skill disclosure (small SKILL.md kept always loaded; large reference files loaded on demand), and count-mode for exploration (count matches, then read the few that matter). Specifies the cross-session persistence hierarchy — git history > files on disk > durable memory > live context — and uses it to decide _what to checkpoint_ before compaction. Lists per-model-class context strategies for 1M, 200K, and 128K windows.

## Philosophy

The context window is the agent's _working memory_. Unlike human memory, it has a hard ceiling — when it fills, information is permanently lost from the live session unless it has been checkpointed somewhere durable. Managing the window is not optional. It is the difference between completing a long task and crashing mid-work with the most recent reasoning gone.

The trap of large windows is the assumption that they are _effectively_ unlimited. A 1M-token window feels infinite until a single 2000-line file read consumes 30K, three of those plus a long tool-result chain pushes past 200K, and the agent is at 60% before any real implementation has happened. The ceiling is real, and it is closer than the headline number suggests. Discipline at 200K is identical to discipline at 1M; only the absolute numbers move.

The 80% rule exists because compaction is _itself_ an operation that needs budget. Hitting 100% mid-operation loses the operation. Compacting at 80% preserves it — the remaining 20% pays for the act of preserving.

## Zone Model

A useful per-session mental partition of the available budget:

| Zone                | Typical share | What lives here                                                          |
| ------------------- | ------------- | ------------------------------------------------------------------------ |
| **System**          | ~5–10%        | System prompt, repo rules, tool schemas, always-loaded directives        |
| **Skill injection** | ~2–5%         | The SKILL.md files auto-loaded by the routing layer for the current task |
| **Working**         | ~85–93%       | Conversation, tool results, file contents, agent output                  |

The exact share varies by model, harness, and task type. The zones are useful because budget breaches show up in different places: a System overrun is a rules / tool-schema problem, a Skill overrun is a routing / over-injection problem, a Working overrun is a context-management / file-read problem. Each has a different remediation.

### Practical budget by model class

Replace these illustrative figures with the actual figures of your runtime — they shift over time and across vendors.

| Model class                                                  | Total context | Typical system overhead | Practical working budget |
| ------------------------------------------------------------ | ------------- | ----------------------- | ------------------------ |
| Frontier 1M-context (Anthropic Opus / Sonnet 1M tier)        | ~1,000,000    | ~70K                    | ~930K                    |
| Frontier 200K-context (default tier of most frontier models) | ~200,000      | ~70K                    | ~130K                    |
| Long-context Haiku class                                     | ~200,000      | ~50K                    | ~150K                    |
| ~128K class (some OpenAI / open-weight)                      | ~128,000      | ~20K                    | ~108K                    |

## Context Health States

| State       | Used budget | Meaning          | Action                                           |
| ----------- | ----------- | ---------------- | ------------------------------------------------ |
| `ok`        | < 60%       | Normal operation | Continue working                                 |
| `compact`   | 60–80%      | Getting crowded  | Plan compaction at the next logical boundary     |
| `exhausted` | > 80%       | Critical         | Stop after the current item, compact immediately |

### The 80% rule

**Always compact at 80% of the working budget — never at 100%.** The remaining 20% is the safety margin for:

- Completing the operation currently in flight
- Writing the checkpoint state
- Running whatever session-closeout / wrap protocol the runtime ships
- Emitting the continuation signal so the next session can resume

Hitting 100% mid-operation loses work. Compacting at 80% preserves it.

## Compaction Protocol

### When to compact

1. Context health reaches `compact` or `exhausted`
2. After completing a logical unit of work (one task, one file, one audit item)
3. Before starting a large new operation that will read many files
4. When tool results begin to truncate (a leading indicator of context pressure)

### Pre-compact checklist

Before triggering compaction:

1. **Commit any uncommitted changes** — git work survives compaction; live context does not.
2. **Write the continuation signal** — the next-session contract: active task, current question, remaining work.
3. **Update any loop or task checkpoint** — advance the recorded phase to the actual phase.
4. **Save critical state** — anything that cannot be re-derived from git history or files on disk goes into a durable artefact now.

### Pre-compact hook

A pre-compact hook is the deterministic enforcer of the checklist. The hook captures, at minimum:

- The active task identifier and the current question
- The agent mode / phase
- The current git branch and the most recent commit hashes
- The current context-health state
- A small bag of custom state (whatever the runtime needs to resume)

Any runtime that supports compaction without a pre-compact hook is _one accidental compaction away from losing the decision trail_. The hook is not optional infrastructure for any session that runs more than a few minutes.

### Post-compact recovery

After compaction, the session-start brief should re-inject:

- Git status (branch, recent commits, dirty files)
- The active task pulled from the continuation signal
- A short summary of the in-progress board state
- Any critical findings recorded in the pre-compact checkpoint

The agent does not re-load the lost conversation. It rebuilds _selectively_ from the durable artefacts.

## Token Consumption Patterns

### What consumes the most context

| Operation                           | Typical tokens | Impact     |
| ----------------------------------- | -------------- | ---------- |
| Full file read (2000 lines)         | 20–40K         | High       |
| Grep results, 50 matches            | 5–10K          | Medium     |
| Tool result, large JSON             | 10–30K         | High       |
| Skill injection, one SKILL.md       | 3–8K           | Low–Medium |
| Agent response, code + explanation  | 2–5K           | Low        |
| System prompt + always-loaded rules | ~50K (fixed)   | Baseline   |

### Five token-reduction techniques

#### 1. Deterministic CLI over heavy tool-result paths

Where the runtime offers both a heavy tool-result path (e.g., a large MCP-style JSON dump) and a deterministic CLI / scripted path that returns the same data shaped tighter, prefer the CLI. The savings can easily be 50–100× per call. The principle: ship structured output through tools the model can read efficiently, not through whatever path the runtime happens to expose by default.

#### 2. Targeted file reads (offset + limit)

```
BAD:  read the whole 2000-line file
      → 30K tokens
GOOD: read 30 lines starting at the function you actually need
      → 500 tokens
```

If a code-search step has already located the relevant lines, _use_ those line numbers. A "read everything because I might need it" pattern is the single biggest avoidable burn.

#### 3. Search before read

```
BAD:  read 5 candidate files looking for a function
      → 100K tokens
GOOD: grep for the function name first, then read 30 lines from the one match
      → 2K tokens
```

The search step costs ~1K tokens and replaces 50–100K of speculative reading.

#### 4. Progressive skill disclosure

Skills should follow a two-tier structure:

- **`SKILL.md`** — the core patterns, the routing-contract description, the verification checklist. Always loaded when the skill is selected. Should fit comfortably in 3–8K tokens.
- **`references/*.md`** — detailed reference material, long examples, deep specifications. Loaded _only_ when explicitly needed.

Only `SKILL.md` is auto-injected. References are loaded by the agent when the task demands the depth.

#### 5. Count mode for exploration

```
BAD:  list every TODO comment in the repo, full match content
      → 50K tokens
GOOD: count first, then read selectively
      grep --count "TODO"                                  → 200 tokens
      grep "TODO" path: src/lib/ --head 10                 → 2K tokens
```

Exploration should be a _count → narrow → read_ sequence, not a single exhaustive read.

## Cross-Session Persistence Hierarchy

What survives a compaction or session restart, ranked from most to least durable:

1. **Git** — code, commits, branches. Permanent.
2. **Files on disk** — checkpoints, continuation signals, structured logs (JSONL is ideal). Persistent until manually deleted.
3. **Durable memory** — index files and topic files in a memory directory consumed by the next session. Persistent and indexed.
4. **Live context** — conversation history, in-flight reasoning, tool results. **Lost on compaction.**

The hierarchy drives the pre-compact checklist: anything that lives only at level 4 needs to be promoted to levels 1–3 _before_ compaction, or it is gone.

### Planning for compaction

When starting a complex multi-step task:

1. Break it into subtasks each of which can complete inside one context window
2. After each subtask: commit + update checkpoint + write continuation signal
3. If a subtask risks exceeding the budget mid-flight, split further or read fewer files

The rhythm is: small unit → commit → checkpoint → next unit. Compaction becomes a routine boundary instead of a crisis.

## Per-Model-Class Strategies

| Model class                                 | Typical task sizing                                     | Compaction cadence      | Key disciplines                                                         |
| ------------------------------------------- | ------------------------------------------------------- | ----------------------- | ----------------------------------------------------------------------- |
| 1M context (frontier Opus / Sonnet 1M tier) | 5–10 file reads + full implementation per session       | After 3–4 complex tasks | Progressive skill disclosure; targeted reads still required             |
| 200K context (default frontier tier)        | 2–4 file reads + one focused implementation per session | After every 2 tasks     | Aggressive search-before-read; skill targeting; offset+limit reads      |
| Long-context Haiku class                    | 2–3 file reads per task                                 | After every task        | Minimise skill payload; targeted labels only; commit between tasks      |
| ~128K class                                 | 1 task per session                                      | Hard boundary           | Count-mode first; read only essentials; one verification step at a time |

A 1M window is not a license to ignore the rules — it just shifts the breaking point further out. Apply the same discipline; the budget math just lets you run longer between compactions.

## Anti-Patterns

| Anti-pattern                                             | Why it fails                                                               | Correct                                                                            |
| -------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Reading entire large files when 30 lines would do        | Burns 20–40K per file with no benefit                                      | Use `offset` + `limit`                                                             |
| Loading every available skill regardless of task         | Skill injection should be 2–5%, not 25%                                    | Use targeted routing labels; trust the routing layer                               |
| Ignoring the `compact` health signal                     | Skipping past 80% guarantees a 100% loss event sooner or later             | Compact at the next logical boundary once `compact` triggers                       |
| Compacting without a pre-compact checkpoint              | The decision trail is lost; the next session re-derives wrong              | Always run the pre-compact checklist; keep the hook always-on                      |
| Letting tool results dump unstructured JSON into context | A 30K tool result evicts 30K of useful conversation                        | Wrap heavy results in a CLI / script that returns the shape you need               |
| Speculative reads ("I might need this")                  | Speculation has the same cost as evidence-based reads, with worse outcomes | Read on evidence; if you cannot name _what you'll do with the file_, don't read it |
| Treating the 1M window as effectively unlimited          | A complex task crosses 60% in minutes; the ceiling is real                 | Apply the same discipline at 1M as at 200K; the budget just stretches              |

## Verification

- [ ] The current context-health state has been correctly classified as `ok`, `compact`, or `exhausted` based on actual usage estimates
- [ ] The pre-compact checklist has been followed before any compaction (commit, continuation signal, checkpoint, custom state)
- [ ] A pre-compact hook is installed and runs deterministically — compaction is never invoked without it firing
- [ ] File reads use `offset` + `limit` targeting for any file beyond ~200 lines
- [ ] The session prefers deterministic CLI / scripted tool paths over heavy MCP-style result dumps where both exist
- [ ] No compaction has been triggered at 100% — the 80% rule has been respected
- [ ] What needs to survive the session has been promoted from live context to git / files / durable memory before any compaction
- [ ] The active model's actual context budget (not assumed budget) is the planning baseline

## Do NOT Use When

| Use instead             | When                                                                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `context-management`    | Deciding _what_ to load, keep, or drop from the working set — the qualitative side of context health                                 |
| `context-graph`         | Designing the multi-graph architecture (skills + docs + memory + scripts) — the topology, not the runtime budget                     |
| `prompt-craft`          | Writing or improving a prompt — wording, structure, format constraints                                                               |
| A memory-curation skill | Curating cross-session persistent memory files, pruning the memory index                                                             |
| `tool-call-strategy`    | Choosing which tool to call next — context-window decides the _budget_ for the call's result, not whether the call is the right call |
| `code-review`           | Reviewing AI-generated code — orthogonal concern                                                                                     |
| `context-engineering`   | Designing the system-level information architecture — context-engineering is upstream of this skill                                  |
