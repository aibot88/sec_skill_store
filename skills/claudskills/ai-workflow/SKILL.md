---
description: Set up LLM workflow discipline for projects that use AI / LLM calls in production or eval suites. Authors an eval-cost-watcher agent that projects token cost BEFORE regression evals run, plus an AI-workflow-discipline rule covering mock-mode placement, fixture freshness, and multi-stage cost accumulation. Optionally a small eval-regression skill stub. Invoke /dotclaude:ai-workflow only when the project actually has AI workflows.
---

# `/dotclaude:ai-workflow` — LLM workflow + cost discipline kit

You are setting up the AI-workflow safety layer — the discipline that prevents night-long eval runs from producing four-figure surprise bills, and that catches the mock-mode-bypass class of bug at the source rather than in the invoice.

The eval-cost-watcher agent is the showpiece. It reads the diff, counts fixtures, projects cost ranges, and suggests cheaper alternatives — all BEFORE the eval runs.

## Phase 1 — Read the project's AI shape

Before any question:

1. **Detect AI SDK presence** — does the project actually have LLM calls?
   ```bash
   grep -rln "@anthropic-ai/sdk\|openai\|@ai-sdk\|@google/generative-ai\|gemini\|claude" \
     package.json Cargo.toml pyproject.toml requirements.txt 2>/dev/null | head
   grep -rn "from anthropic\|from openai\|import.*@anthropic" \
     --include="*.py" --include="*.ts" --include="*.js" . 2>/dev/null | head -10
   ```
   If NO AI dependencies, STOP. Report applicability check failed. Tell the user this skill doesn't apply.

2. **AI workflow directories** — find where prompts / configs / fixtures live:
   ```bash
   find . -type d \( -name "ai" -o -name "llm" -o -name "prompts" -o -name "evals" \
     -o -name "workflows" -o -name "agents" -o -name "fixtures" \) \
     -not -path "*/node_modules/*" 2>/dev/null | head
   find . -path ./node_modules -prune -o \
     \( -name "*.prompt.*" -o -name "*system-prompt*" -o -name "*instruction*" \) \
     -print 2>/dev/null | head
   ```

3. **Eval suite** — find the eval entry points:
   ```bash
   cat package.json 2>/dev/null | grep -A 2 '"scripts"' | grep -E "eval|test:ai|test:llm"
   find . -name "*.eval.*" -o -name "*eval*.py" -o -name "*eval*.ts" \
     -not -path "*/node_modules/*" 2>/dev/null | head
   ls evals/ tests/eval/ tests/llm/ 2>/dev/null
   ```

4. **Model identifiers** — read the config:
   ```bash
   grep -rEn "MODEL_NAME|model.*=.*\"|model: ['\"]|MODEL_ID|model_id" \
     --include="*.ts" --include="*.py" --include="*.json" --include="*.yaml" . \
     2>/dev/null | head -30
   ```
   Note which model tiers the project uses (frontier-large vs frontier-mid vs frontier-fast). Each tier swap is a 5-10× cost multiplier.

5. **Mock mode** — does one exist?
   ```bash
   grep -rn "MOCK_MODE\|MOCK_AI\|mockAi\|dryRun\|mock_response\|AI_MOCK\|FIXTURE_MODE" \
     --include="*.ts" --include="*.py" --include="*.js" . 2>/dev/null | head
   ```
   If yes, note WHERE the mock-mode check fires. Then trace whether ALL entry points to the LLM workflow pass through the mock-aware layer, or whether some bypass it (the war-story pattern at `../examples/the-test-passed-for-the-wrong-reason.md`).

6. **Fixture count + cascade depth** — gauge the cost scale:
   ```bash
   find . -path "*fixtures*" -type f 2>/dev/null | wc -l
   # Read 1-2 workflow files to count cascade stages
   find . -name "*workflow*.ts" -o -name "*pipeline*.ts" -o -name "*cascade*.ts" \
     -not -path "*/node_modules/*" 2>/dev/null | head
   ```

7. **Recent AI-cost-related commits**:
   ```bash
   git log --oneline --grep="cost\|token\|eval\|fixture\|model\|mock" -20
   ```

Build mental model of: what AI architecture (single call / multi-stage cascade / agent loop), what models per stage, what mock-mode coverage looks like, what the eval cost scales with.

## Phase 2 — Interview

Open `interview.md` (same directory). 3-4 questions. Adaptive — skip what Phase 1 already answered.

- **Workflow shape** — single call / multi-stage / eval harness with fixtures? Production or dev-only?
- **Cost ceiling** — what's a "this eval got too expensive" threshold per iteration?
- **Models in use** — providers + tiers per stage (often discoverable from Phase 1; confirm).
- **Past cost surprises** — drives the watcher's safety thresholds.

## Phase 3 — Read the principles

Read these from `../../principles/` SELECTIVELY:

**Always read** (this kit's core):
- `ai-cost-monitoring.md` — the five-step projection methodology

**Cross-reference** (link from the watcher's body, do not re-author):
- `code-review.md` — mock-mode bypass is a code-review pattern; the watcher's mock-coverage check overlaps
- `pre-flight.md` — pre-flight should ask about cost impact for AI-workflow changes

**Read the war-story example** — load-bearing for this skill:
- `../examples/the-test-passed-for-the-wrong-reason.md` — the canonical mock-mode-bypass failure. The watcher's mock-coverage check exists because of this class of bug; the AI-workflow-discipline rule references it.

## Phase 4 — Author the kit

### Agents (in `.claude-staging/agents/`)

- **`eval-cost-watcher.md`** — the pre-eval cost projector
  - Frontmatter: `description:` — derived from `ai-cost-monitoring.md` principle, tuned to THE user's stack
  - Tool surface: `Read, Grep, Glob, Bash` (for `git diff`, file counting, fixture counting). NO `Edit`, NO `Write`, NO ability to actually run the eval — projection is the role, NOT execution.
  - Body sections:
    - The five-step methodology (classify-diff / read-model+temperature / count-fixtures / estimate-tokens / produce-projection)
    - **Project-specific model-tier map** — concrete model identifiers from Phase 1 + their tier classification (frontier-large = `<model-id>`, frontier-mid = `<model-id>`, frontier-fast = `<model-id>`). With a "verify pricing at provider's docs — drifts" note.
    - **Project-specific cascade architecture** — list the stages, the passes per stage, the fixture sets per stage. If the workflow has shape "Stage A (research, 1 pass) → Stage B (synthesis, 2 passes) → Stage C (critic, 1 pass) per fixture × 20 fixtures = 80 calls per full eval," encode that.
    - **Mock-mode coverage map** — for each entry point to the workflow, note whether it respects mock mode. Explicitly flag any that BYPASS it (the war-story pattern). This is the most-load-bearing section: a bypass shipped to production is a four-figure surprise bill waiting to happen.
    - **Cost ceiling + alarm threshold** — derived from the user's interview answer to AI2. The watcher recommends NOT running the eval if the projection exceeds the ceiling without explicit override.
    - Projection-format template (affected stages / model changes / cost range / cheaper alternatives / recommendation)
    - "I do not run the eval" constraint explicit
  - Model: mid-tier reasoning model. The work is diff-classification + arithmetic; doesn't require the heaviest reasoning. Save top-tier for code-review / pre-flight.

### Rules (in `.claude-staging/rules/`)

- **`ai-workflow-discipline.md`** (small rule; author only if helpful for the project's shape)
  - **Mock-mode placement** — single rule: "mock-mode flag is a property of the WORKFLOW, not the route." Cross-reference the war story. Specifically prohibit the pattern where the mock check lives only in the HTTP layer; require the workflow's entry function to check.
  - **Fixture freshness** — when prompts change, fixtures captured against old prompts are stale and produce false-positive eval results. Encode the convention for re-capturing fixtures (manual? scripted? what's the command?).
  - **Multi-stage cost accumulation** — cascade depth × passes × fixtures × output tokens. The cost-watcher does the math; the rule reminds the user that this math compounds.
  - **Model-swap discipline** — tier swaps (frontier-fast → frontier-large) need explicit justification + cost projection. The rule says: "Before swapping the model on any stage, run the watcher."
  - Skip authoring this rule entirely if the project's AI usage is minimal (single call, no cascade, no eval suite) — the watcher carries the load alone.

### Skills (in `.claude-staging/skills/`)

- **`eval-regression/SKILL.md`** (stub — author only if the project has a meaningful eval suite)
  - User-invocable (`/eval-regression`)
  - Wraps the watcher + the actual eval-run command + the result-comparison step
  - Workflow: (1) run cost projection via watcher, (2) prompt user to confirm, (3) run eval against fixture set, (4) compare results to baseline, (5) flag regressions
  - This is a stub if the project doesn't yet have a structured baseline-comparison; the user fills it in as the eval suite matures.
  - Skip entirely if the project has no eval suite (just inline AI calls without a regression harness).

### Hooks

The AI-workflow kit doesn't typically ship hooks. Edit-time hooks would have to read the diff and project cost on EVERY edit; the agent doing that on demand is the right shape. One exception: a pre-eval-run wrapper script could invoke the watcher automatically; that's the `eval-regression` skill's job, not a hook.

## Phase 5 — Stage + present + commit

### Staging

Write everything to `.claude-staging/` first, organized by artifact type.

### Present

Walk the user through:

1. **The kit overview** — what landed (typically 1 agent + maybe 1 rule + maybe 1 skill)
2. **Top 2-3 highlight artifacts** — concrete reasoning. NOT "I added a cost-watcher" but: "Your workflow has <N> stages × <M> passes × <K> fixtures = <total> calls per full eval. Model tier per stage: <list>. Currently your bill for one full eval projects at $<low>-$<high>. The watcher will run pre-eval and bail if any single run exceeds your $<ceiling> threshold."
3. **Mock-mode coverage** — call out explicitly which entry points respect mock mode and which BYPASS it. If you found a bypass, surface it: "Your dev cron at `<path>` calls the workflow directly, bypassing the mock check at `<other-path>`. The war-story pattern. The watcher will flag any change that propagates work through the bypassed path."
4. **What got SKIPPED** — and why. "Skipped `eval-regression` skill because no eval suite found — re-run this skill when you build one."
5. **Model + token-cost note** — eval-cost-watcher uses mid-tier reasoning model and is cheap to invoke (compared to the costs it projects). Worst case it costs $0.10 to prevent a $40 surprise eval — favorable asymmetry.

### Approve → commit

After explicit user approval, move `.claude-staging/` → `.claude/` and commit with structured message:

```
feat(.claude): AI workflow discipline (dotclaude:ai-workflow)

Authored:
- agents:  eval-cost-watcher
- rules:   [ai-workflow-discipline]
- skills:  [eval-regression]

Workflow shape: <single-call / cascade / agent loop>
Models in use: <tier 1 IDs, tier 2 IDs, tier 3 IDs>
Mock-mode coverage: <fully covered / N bypasses flagged>
Per-eval cost projection: $<low>-$<high>
Alarm ceiling: $<user-supplied>
```

## Non-negotiable rules for this flow

1. **Applicability gate is HARD.** If Phase 1 shows no AI SDK dependencies, this skill DOES NOT APPLY. Don't ship a phantom cost-watcher for a project with no AI workflow. Report applicability failure cleanly and stop. The user can re-invoke once AI lands in the codebase.

2. **The watcher does NOT run the eval.** Projection from source files, never from actual model calls. The whole point is to project BEFORE spending; if the watcher itself burns calls to estimate, the asymmetry collapses. Tool surface excludes anything that could invoke the workflow.

3. **Mock-mode coverage is the highest-priority finding.** A workflow that bypasses mock mode is a four-figure surprise bill waiting to fire. If Phase 1 surfaces a bypass, the watcher's body should treat it as an explicit ALWAYS-FLAG finding on any change affecting the bypassed path. Don't bury it; surface it.

4. **Pricing is in a maintained config, not hardcoded.** LLM provider prices change. The watcher's body should reference a maintained config (project-local `ai-pricing.json` or similar) with a "verify against provider's docs" note. NEVER hardcode numbers — they go stale and the watcher's projections become silently wrong.

5. **Projections are ranges, not points.** Different fixtures produce different output lengths. Different inputs produce different cache-hit behavior. The watcher reports `$low - $high` and acknowledges the gap. Single-point estimates that turn out to be 3× off train users to distrust the agent.

6. **Cheaper alternatives are mandatory output.** A projection alone says "this will cost $X." A projection + alternatives says "this will cost $X; here are three ways to get the same signal for less." Always provide the alternatives — subset of fixtures, mock mode (if applicable), skip a cascade stage, run only the affected stage. The user needs the option list to make the run/skip decision.

7. **Tier swaps are called out separately.** Swapping frontier-fast for frontier-large is a 5-10× multiplier on its own — the highest-impact category of change. Don't bury it inside a general projection; the watcher should have a dedicated "Model changes" section that flags swaps explicitly with the multiplier number.

8. **The watcher is cheap; the eval is expensive.** The watcher's own model is mid-tier and its context is bounded. If the watcher itself approaches the cost of the eval it's projecting, the whole abstraction is broken. Watch the watcher's spend during authoring — keep its prompt focused, its context tight, and its model choice modest.
