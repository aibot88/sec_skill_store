---
name: workflow-adversarial-quality
description: "Full adversarial quality loop — implement, self-attack, parallel verification, quality gates, final validation. 全品質循環：實現、自攻、並行驗證、質量關卡、最終確認. Use when: implement task with quality, run adversarial review, verify code quality, run quality gates, complete workflow task"
disable-model-invocation: true
context: fork
agent: "workflow:task-executor"
---

<!-- CC 2.1 fork decision: workflow driver — runs the full implement / self-attack / parallel verification / gate / validation pipeline across many tool calls and reviewer dispatches. Forking keeps the orchestrator free of intermediate review chatter. Executor: workflow:task-executor (preloads adversarial-quality, context-hygiene, testing-strategy via skills array). -->


# Adversarial Quality Loop

含對抗自審與外部驗證之完整實現循環。

## Overview 概覽

此循環實現完整的 Ralph Wiggum 對抗協作模式：
1. 正向實現（使之運作）
2. 自我對抗審查（尋自身缺陷）
3. 外部對抗驗證（獨立挑戰）
4. 質量關卡（自動化檢查）
5. 最終確認（驗收標準）

**上下文規則**：此技能在子代理內部運行（僅限此任務的全新上下文）。

## Execution Phases 執行階段

### Phase 0: Git Hygiene & TDD Setup

**目標**：從最新代碼出發，建立 TDD 紀律

**步驟**：
1. 拉取最新變更並 rebase 至 main
2. 解決合並衝突
3. 驗證項目構建成功且全部測試通過
4. 規劃 TDD 方法——識別首先撰寫哪些測試

```yaml
git_hygiene:
  before_starting:
    - "git fetch origin"
    - "git rebase origin/main"
    - "resolve any conflicts"
    - "run full test suite - must be green"
    - "build the project - must succeed"

  during_work:
    - "rebase often if main moves forward"
    - "commit small, focused changes"
    - "each commit should build and pass tests"
    - "use conventional commit messages"

  before_completion:
    - "rebase onto latest main one final time"
    - "verify all tests pass after rebase"

tdd_cycle:
  order: "test first, always"
  steps:
    RED: "Write a test that describes the next behavior. Run it. It MUST FAIL (RED). If it passes, the test is wrong."
    GREEN: "Write the MINIMUM code to make the RED test pass. Confirm GREEN."
    REFACTOR: "Clean up code while tests stay GREEN. If any test goes RED, undo immediately."

  violations:
    - "Writing implementation before a RED test exists"
    - "A test that was never seen RED"
    - "Refactoring while any test is RED"

  smoke_tests:
    rule: "Smoke tests ALWAYS use highest fidelity — full e2e, never mocked"

  when_to_skip_tdd:
    - "Pure UI layout changes with no logic"
    - "Configuration-only changes"
    - "Documentation-only changes"
    - "NEVER skip for business logic or data transformations"
```

**輸出**：已清潔、最新之分支，備 TDD 實現

**檢查點**：記錄分支狀態、構建狀態、測試基準數。

### Phase 1: Implementation Planning (5-10% of time)

**目標**：理解範圍、評估結構就緒性、創建驗證清單

**步驟**：
1. 從循環狀態文件讀取任務規格
2. 識別範圍內所有文件（最多5個）
3. 讀取當前文件內容
4. **評估結構就緒性**：現有代碼結構是否自然支持此變更？
   - 使用 LCI 查找相關代碼，理解當前形態
   - 問：新代碼是自然延伸還是補丁？
   - 若存在結構摩擦，在 Phase 2 實現前添加重構步驟
5. 創建實現計劃（含需要時的先重構步驟）
6. 創建驗證清單（含可查找性檢查）
7. 寫入檢查點至狀態文件

**實現者心態**："使其正確運作，置於正確位置，命名可被發現"

**Output**:
```yaml
implementation_plan:
  files_to_change:
    - file: "path/to/file.ts"
      changes: "What needs to change"

  verification_checklist:
    - "Acceptance criterion 1 met"
    - "No type errors"
    - "Tests pass"
    - "No security vulnerabilities"

  estimated_complexity: "Low|Medium|High"
```

**檢查點**：計劃寫入狀態文件。下一階段只讀檢查點摘要，不讀完整實現文件。

### Phase 2: Positive Implementation (30-40% of time)

**目標**：依最佳實踐實現任務

**實現者心態**："使其運作，使其正確"

**步驟**：
1. 從狀態文件讀取實現計劃（全新上下文）
2. 按正向指令實現變更：
   - ✓ 撰寫清晰可維護代碼
   - ✓ 遵循現有模式
   - ✓ 添加適當錯誤處理
   - ✓ 撰寫全面測試
   - ✓ 添加必要文檔

**正向指令（DO）**：
- **先重構** — 若現有結構不自然支持變更，先修結構，再添代碼
- 使用現有代碼模式
- 變量名描述行為而非實現
- 添加類型注釋
- 處理邊緣情況
- 先寫測試（TDD — Phase 0 的 red/green/refactor 週期）
- 保持函數小而專注
- 複雜邏輯添加注釋
- 遵循安全最佳實踐
- **確保可查找性** — 命名須可被未來開發者搜索發現

**輸出**：實現完成，備對抗審查

**檢查點**：寫入實現摘要，顯式遺忘代碼細節。

### Phase 3: Self-Adversarial Review (15-20% of time)

**目標**：在自身實現中尋找缺陷

**驗證者心態**："破之，尋邊緣情況，質疑假設"

**步驟**：
1. 讀取實現摘要（尚不讀完整代碼）
2. 生成攻擊向量與邊緣情況
3. 讀取實際實現
4. 挑戰每個決策：
   - ❌ What inputs will break this?
   - ❌ What assumptions are unsafe?
   - ❌ What edge cases are missing?
   - ❌ Where can this fail?
   - ❌ What security issues exist?

**Adversarial Challenges**:
```yaml
challenge_categories:
  input_validation:
    - "What if input is null/undefined/empty?"
    - "What if input is extremely large?"
    - "What if input contains special characters?"

  state_management:
    - "What if function called twice concurrently?"
    - "What if state is invalid?"
    - "What if initialization fails?"

  error_handling:
    - "What if network fails?"
    - "What if file doesn't exist?"
    - "What if parse fails?"

  security:
    - "What if input is malicious?"
    - "What if user is unauthorized?"
    - "What secrets could leak?"

  performance:
    - "What if data is huge?"
    - "What if this runs 1000 times?"
    - "What memory could leak?"

  structure_and_findability:
    - "Does the new code live where someone would look for it?"
    - "Do names describe what the code does, not how it does it?"
    - "Would a developer searching for this feature by name find it?"
    - "Did we add code to an existing file that now has incoherent scope?"
    - "Did we refactor first, or did we hack the new code into a bad location?"
    - "Are there cryptic abbreviations not established in the codebase?"

  domain_model:
    - "Does the implementation use canonical terms from docs/DOMAIN.md?"
    - "Are any rejected synonyms present in identifiers, comments, or test names?"
    - "Did this task introduce new domain concepts not yet in DOMAIN.md?"
    - "If this was a bug fix, did it reveal a conceptual misunderstanding? Is it logged?"
    - "Do aggregate, event, and command names match the domain model exactly?"
```

**輸出**：所發現問題清單及已應用修復

**檢查點**：寫入所發現問題，再次遺忘實現。

### Phase 4: Concurrent Adversarial Verification (20-30% of time)

**目標**：兩個專門代理並行運行進行獨立驗證

**模式**：使用 Task 工具同時生成兩個驗證子代理，然後處理結果

#### Prepare Reports Directory (verdict-file channel) 準備報告目錄

Reviewers deliver their decision via **verdict files** under `.dartai/reports/<task-id>/`, not via stdout body. Before dispatching:

```yaml
prepare_reports_dir:
  step_1_clear:
    action: "rm -rf .dartai/reports/<task-id>/"
    why: "Stale-verdict mitigation — a previous run's verdict file would otherwise be parsed as the current gate decision"
  step_2_recreate:
    action: "mkdir -p .dartai/reports/<task-id>/"
  invariant: "Always clear before each Phase 3 entry, even on retry-after-fix"

paths:
  qa-reviewer:           ".dartai/reports/<task-id>/qa.md"
  code-quality-reviewer: ".dartai/reports/<task-id>/quality.md"
  post-task-reviewer:    ".dartai/reports/<task-id>/security.md"
  aggregator:            ".dartai/reports/<task-id>/verdict-summary.kdl"
```

File format is line-oriented per `plugins/dartai/skills/verdict-schema.md` ("Verdict File Delivery") — line 1 `verdict:`, line 2 `confidence:`, then `blocker:` / `advisory:` / `evidence:` lines. The driver gates on file content, not subagent stdout body.

#### Dispatch 並行派發（兩者同時）

```yaml
concurrent_dispatch:
  tool: Task
  spawn_simultaneously: true

  agents:
    - subagent_type: "workflow:code-quality-reviewer"
      description: "Review code quality and codebase integration"
      prompt: |
        Review code quality for task [task-id].

        Task: [title]
        Files changed: [list]
        Acceptance criteria: [criteria]

        Focus on: project coherence, best practices, no bloat, no fallbacks/TODOs, code duplication, cleanup and refactoring.
        - What inputs or states will break this?

        Output: write verdict to .dartai/reports/[task-id]/quality.md
        per verdict-schema "Verdict File Delivery" (line-oriented:
        verdict:/confidence:/blocker:/advisory:/evidence:). Stdout ≤5
        lines: verdict-file: <path> then verdict: <pass|fail|warn>.

    - subagent_type: "workflow:qa-reviewer"
      description: "Review test quality and coverage"
      prompt: |
        Review QA and test quality for task [task-id].

        Task: [title]
        Files changed: [list]
        Acceptance criteria: [criteria]

        Focus: Test quality and coverage
        - Assertion quality, edge case coverage, e2e testing
        - TDD compliance (RED/GREEN), test distribution
        - Test isolation, test plan maintenance
        - What critical paths lack tests?
        - Requirements traceability, and testability

        Output: write verdict to .dartai/reports/[task-id]/qa.md per
        verdict-schema "Verdict File Delivery" (line-oriented:
        verdict:/confidence:/blocker:/advisory:/evidence:). Stdout ≤5
        lines: verdict-file: <path> then verdict: <pass|fail|warn>.
```

#### Read Verdicts (file-streaming via Monitor) 經 Monitor 讀裁決

The driver gates on **verdict file content**, not subagent stdout. Stdout is a ≤5-line pointer; the transcript is dropped after the path is captured.

```yaml
verdict_consumption:
  channel: "file"
  reads:
    - ".dartai/reports/<task-id>/quality.md"
    - ".dartai/reports/<task-id>/qa.md"

  preferred_signal: "subagent-completion notification"
  why: "Completion notifications are durable — file-system events alone can drop under load. Parse the verdict file at completion time."

  fallback_signal: "Monitor stream over the verdict file path"
  why: "Harnesses without completion notifications can still react to file appearance/change. Keep the Monitor stream open to catch late writes (e.g. an evidence file the reviewer writes after the verdict file)."

  parse_rule:
    - "Read line 1 — must start with 'verdict:'; extract token (pass/fail/warn)"
    - "Read line 2 — must start with 'confidence:'; extract token (high/med/low)"
    - "Read remaining lines — collect 'blocker:' (required when verdict=fail), 'advisory:', optional trailing 'evidence:'"
    - "Lines starting with '#' are comments; trailing whitespace and blank lines ignored"

  never:
    - "Consume the subagent stdout body into driver context"
    - "Re-dispatch a reviewer just to re-read a verdict — the file is replayable"
```

**Replay**: A gate decision can be reconstructed from the verdict file alone — re-running the gate means re-reading the file, no need to re-dispatch the reviewer.

#### Verification Report Schema 驗證報告模式（每個代理返回此格式）

```yaml
verification_report:
  agent: "code-quality-reviewer|qa-reviewer"
  result: "all_pass|needs_work|critical_security"

  issues_found:
    - severity: "critical|high|medium|low"
      category: "correctness|quality|test-coverage|security|performance"
      description: "What's wrong"
      location: "file:line"
      recommendation: "How to fix"

  positive_findings:
    - "What was done well"

  acceptance_criteria_checked:
    - criterion: "Criterion text"
      met: true|false
      evidence: "How verified"
```

#### Result Handling 結果處理

```yaml
result_routing:
  collect: "Wait for both agents to return before evaluating"

  all_pass:
    trigger: "Both agents return result: all_pass"
    action: "Proceed to Phase 5"

  needs_work:
    trigger: "One or both agents return result: needs_work"
    action: |
      1. Fix all reported issues
      2. Re-dispatch ONLY the agents that returned needs_work (not passing agents)
      3. Pass the same inputs plus a fixes_applied summary
    max_retries: 2
    if_still_failing_after_retries: |
      Write failure report to state file with unresolved issues.
      Return to main loop with status: failed.
```

**檢查點**：寫入所有代理的綜合驗證報告，遺忘實現細節。

**風險權威派遣（authoritative reviewer dispatch when enabled; legacy fallback）**：若風險管道裝且啟，調 `risk-pipeline-dispatch`（或先經 `risk-pipeline:classify` 再取 `pipeline_spec.reviewers`），風險提議之 reviewer 集為權威派發對象；`enabled: false` 時退回既有全套 roster：

```yaml
availability_check:
  required:
    - "plugins/risk-pipeline/skills/risk-pipeline-dispatch.md exists"
    - ".claude/rules/risk.md exists with frontmatter risk_pipeline.enabled == true"
  if_unavailable:
    action: "Skip invocation; write record with risk:{enabled:false}"
    outcome: "Legacy full-roster dispatch drives Phase 4 (fallback path)"

if_available:
  invoke: "risk-pipeline:classify then risk-pipeline-dispatch with {task_risk, verdict, pipeline_tier, trivial_bypass, config}"
  extract: "pipeline_spec.reviewers[]"
  authoritative_action: "Spawn risk-proposed reviewer set; legacy full roster retained as fallback only when enabled:false"
  compare:
    legacy_set: "既有全套 roster（code-quality-reviewer + qa-reviewer）— 僅遙測對比"
    risk_set: "pipeline_spec.reviewers[]（權威派發集）"
    agreement:
      match: "兩集合相等"
      subset: "risk ⊂ legacy（風險提議較少）"
      superset: "risk ⊃ legacy（風險提議較多）"
      diverge: "兩集合既非子亦非超（有差異）"

telemetry_write:
  path: ".workflow/risk-shadow.jsonl"
  append_json_line:
    ts: "<ISO timestamp>"
    event: "review_dispatch"
    task_id: "<task id from state file>"
    legacy_reviewers: ["code-quality-reviewer", "qa-reviewer"]
    risk:
      enabled: true
      verdict: "<from classify>"
      pipeline_tier: "<from classify>"
      scalar: 0
      vector: { b: 0, d: 0, s: 0, r: 0, u: 0, crit_axes: [] }
      required_reviewers: "<pipeline_spec.reviewers[]>"
    reviewer_agreement: "<match|subset|superset|diverge>"
    authoritative: "risk"

if_enabled_do:
  - "Spawn pipeline_spec.reviewers[] as the dispatch roster"
  - "Gate Phase 4 retry logic on risk verdict when verdict != ok"
if_disabled_do:
  - "Spawn full legacy roster (code-quality-reviewer + qa-reviewer)"
  - "Write {authoritative:'legacy'} telemetry record"
```

風險管道缺或禁時，退化為既有全套 roster 派發路徑（legacy fallback）：寫 `{enabled:false, authoritative:'legacy'}` 記錄，既有並行派發路徑不變。

### Phase 4.5: Review for Plan Updates (C-class refactor discovery)

**目標**：將 C 類重構發現作為計劃更新提案發出，不編輯代碼。

**模式**：調用 `dev-standards:review-for-plan-updates`，將提案持久化至 `.workflow/loop-state.json`。

```yaml
invoke:
  tool: Skill
  skill: "dev-standards:review-for-plan-updates"
  input:
    diff: "git diff <task-base>..HEAD"
    rules_dir: ".claude/rules/"

persist:
  file: ".workflow/loop-state.json"
  field: "pending_plan_updates"
  append: "<proposals returned, filtered against .claude/refactor-rejects.txt>"

do_not:
  - "Edit code based on findings"
  - "Decide accept/defer/reject here"
  - "Expand trigger catalog beyond what the skill defines"
```

**檢查點**：提案已寫入狀態文件。下一 tick 的計劃更新呈現（見 `loop-orchestration.md`）處理用戶交互。

---

### Phase 5: Quality Gates (10-15% of time)

**目標**：運行自動化檢查

**步驟**：
1. 運行 linter
2. 運行類型檢查器
3. 運行測試
4. 運行安全掃描器（如可用）
5. 檢查代碼覆蓋率

**Automated Checks**:
```bash
# Linting
npm run lint  # or equivalent

# Type checking
tsc --noEmit  # or equivalent

# Tests
npm test      # or equivalent

# Security
npm audit     # or equivalent

# Coverage
npm run test:coverage  # or equivalent
```

**質量閾值**：
- ✓ 無 linting 錯誤
- ✓ 無類型錯誤
- ✓ 所有測試通過
- ✓ 無嚴重安全問題
- ✓ 新代碼覆蓋率 >= 80%

**若關卡失敗**：修復問題後重新運行

**檢查點**：寫入質量報告，遺忘細節。

### Phase 5b: Post-Task Deep Review

**目標**：質量關卡通過後進行深度順序審查

**模式**：派發單個後任務審查代理

```yaml
post_task_dispatch:
  tool: Task

  agent:
    subagent_type: "workflow:post-task-reviewer"
    description: "Deep review for [task-id]"
    prompt: |
      Run post-task deep review for task [task-id].

      Task: [title]
      Files changed: [list]
      Acceptance criteria: [criteria]

      The fast adversarial gate and quality gates already passed.
      Run all four phases: security audit, in-depth code, PM/docs, replan.

      Output: write verdict to .dartai/reports/[task-id]/security.md
      per verdict-schema "Verdict File Delivery" (line-oriented:
      verdict:/confidence:/blocker:/advisory:/evidence:). Use evidence:
      for the multi-phase report — depth almost always lands there.
      Stdout ≤5 lines: verdict-file: <path> then verdict: <pass|fail|warn>.

  read_verdict:
    channel: "file"
    path: ".dartai/reports/[task-id]/security.md"
    preferred_signal: "subagent-completion notification"
    fallback_signal: "Monitor stream over the verdict file path"
    why: |
      Same file-streaming channel as Phase 3. The driver parses the
      verdict file fresh on completion (or on Monitor notification);
      the subagent stdout body is dropped after the path is captured.
```

**結果處理**：
```yaml
post_task_routing:
  pass:
    action: "Apply replan recommendations, proceed to Phase 6"

  needs_work:
    action: "Fix issues, proceed to Phase 6"
    note: "Non-blocking issues become follow-up tasks"

  fail:
    action: "Fix critical issues (security, concurrency)"
    max_retries: 1

  critical_security:
    action: "STOP - write security-halt report"
```

**檢查點**：將後任務發現與重新規劃寫入狀態文件。

### Phase 5.5: Lightweight Cite Verify (post-commit, pre-Done)

**目標**：commit 已寫、PR body 已生，標記 Done 之前對引用作輕量核驗。完整四層核驗（Tier 3，含 URL 取回）為 `citation-verifier` 任務 `qvd3VBUROdw2` 之職責；此處僅捕顯然破損之引用。

Cite: mcp-architect `citation-verification-pattern`（commit 44bf8e0）、brainstorming PROVENANCE-CONTRACT（commit ebd136a）、dev-standards `multi-source-for-load-bearing-claims`（commit 9ab9c47）。

**步驟**：
1. 解析 commit message 與 PR body 中之所有引用
2. 按引用形式運行對應檢查（見下表）
3. 顯然破損之引用：派發單次重試子代理重新生成；仍失敗則於完成評論中浮現，不阻塞
4. 將每條引用之結果（pass/fail/skipped/fixed-on-retry）寫入完成評論審計記錄

```yaml
cite_forms:
  file_path_line:    # "<path>:<line>" or "<path>:<start-end>"
    verify: "file exists; line in range; range start <= end"
    obviously_broken: "file missing | line out of range | negative/zero line"

  symbol:            # "function foo" | "class Bar" | "Type.member"
    verify: "mcp__lci__search returns ≥1 match of cited kind"
    obviously_broken: "zero matches | matches but no kind match"
    skip_if: "lci MCP unavailable → mark cite as 'skipped:lci-unavailable'"

  git_sha:           # "git:<sha>" or 7+-char hex in commit context
    verify: "git rev-parse --verify <sha>^{commit} exits 0"
    obviously_broken: "rev-parse fails | sha < 7 chars"

  web_url:           # http(s)://...
    verify: "SKIP at this tier"
    note: "URL liveness/content match is Tier 3 (citation-verifier qvd3VBUROdw2)"

  memory_id:         # "memory:<id>"
    verify: "~/.claude/projects/<project-slug>/memory/<id>.md exists"
    obviously_broken: "memory file missing at resolved path"
```

**"顯然破損" 之定義**：僅當 form-specific 檢查返回明確負面（檔不存在、行越界、sha 無效、memory 缺失、lci 零命中）。歧義情況（lci 多命中、無清楚匹配）**不**算顯然破損 — Tier 3 處理。

**Retry protocol**:
```yaml
retry_on_broken_cite:
  budget: 1  # one retry per broken cite
  dispatch:
    tool: Task
    subagent_type: "general-purpose"
    prompt: |
      Cite "[broken-cite]" failed lightweight verification (form: X, reason: Y).
      Re-derive corrected cite from the same intended source.
      Return {status: "corrected", cite: "..."} or {status: "ungrounded", explanation: "..."}.
  on_corrected: "Replace cite in completion comment (NOT in pushed commit)"
  on_ungrounded: "Surface in comment as 'broken cite (ungrounded after retry)'; do NOT block Done"
```

**驗收**：
```yaml
pass_if:
  - all_cites_parsed: true
  - per_cite_outcome_recorded: true
  - completion_comment_includes_cite_audit: true
fail_if:
  - cite_parser_crashed: true   # impl bug, not cite bug
  - retry_budget_exceeded: true # >1 retry/cite = protocol violation
note: "Broken cites surviving retry do NOT trigger fail_if — they surface and the task still moves to Done."
```

**Tier 分層說明**：
- Tier 1（此階段）：cheap shape checks（file/line/sha/memory/lci）— 每任務必跑
- Tier 2（既有）：commit provenance presence — Phase 4 reviewer 處理
- Tier 3（延後至 `citation-verifier` 任務 `qvd3VBUROdw2`）：URL liveness、content match、語義符合、多源印證

**檢查點**：將 cite 審計結果寫入狀態文件，遺忘 cite 細節。

### Phase 6: Final Validation (5-10% of time)

**目標**：驗證驗收標準已達成

**步驟**：
1. 從任務規格讀取驗收標準
2. 讀取所有檢查點報告
3. 驗證每個標準：
   - 實現佐證
   - 驗證佐證
   - 質量關卡佐證
4. 生成完成報告

**驗證清單**：
```yaml
final_validation:
  - criterion: "Each acceptance criterion"
    met: true|false
    evidence:
      - "Implementation: ..."
      - "Verified: ..."
      - "Tests: ..."

  overall_result: "complete|incomplete"
```

**完成報告**：
```yaml
completion_report:
  task_id: "task-3"
  status: "completed|failed"

  summary: "One sentence summary"

  acceptance_criteria_met: true|false
  verification_passed: true|false
  quality_gates_passed: true|false

  stats:
    files_changed: 3
    lines_added: 150
    lines_removed: 45
    tests_added: 5
    issues_found: 8
    issues_fixed: 8

  iterations: 2
  adjustments:
    - "Added validation helper function"

  total_time: "25m 30s"

  recommendation: "Mark complete and proceed"
```

**寫入狀態文件**：更新循環狀態為完成

## Context Management 上下文管理

貫穿此循環：

**階段之間**：
```yaml
context_barriers:
  technique: "Write checkpoint, explicitly forget, read next phase"

  example: |
    # End of Phase 2
    Write implementation summary to state file
    Explicitly state: "Discarding implementation details for fresh review"

    # Start of Phase 3
    Read only implementation summary (NOT full code yet)
    Generate adversarial test cases
    THEN read full code with adversarial mindset
```

**子代理內部**：
```yaml
context_accumulation:
  allowed: "Yes - this is a single task execution"
  why: "Need continuity within task phases"
  limit: "One task only (1-5 files, 1-2 hours max)"
```

**子代理之間**：
```yaml
context_isolation:
  enforced: "Yes - when spawning code-quality-reviewer, qa-reviewer, and post-task-reviewer"
  why: "Independent verification requires fresh eyes"
  mechanism: "Task tool spawns separate subagents concurrently"
```

## Adjustments and Learning 調整與學習

執行中追蹤調整：

```yaml
adjustments:
  types:
    - added_test: "Added test case not in original plan"
    - modified_scope: "Changed file scope (within 5 file limit)"
    - clarified_criteria: "Asked user for clarification"
    - added_dependency: "Needed helper function"

  recording: "Write to state file for loop orchestrator"

  impact: "Main loop updates task list if needed"
```

## Failure Modes 失敗模式

若循環在任意階段失敗：

```yaml
failure_handling:
  record:
    failed_at: "phase_name"
    reason: "What went wrong"
    attempted_fixes: "What was tried"

  decision:
    retry: "If fixable (e.g., test failure)"
    skip: "If task ill-defined"
    stop: "If critical issue (e.g., security)"

  return_to_main_loop: "With failure report in state file"
```

## Usage 使用說明

此技能由 `workflow:task-executor` 代理調用，以運行任務的完整品質循環。

見 `loop-orchestration.md` 瞭解此技能如何融入整體循環。
