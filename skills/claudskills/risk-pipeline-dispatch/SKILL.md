---
name: risk-pipeline-risk-pipeline-dispatch
description: "Dispatch risk vector -> reviewer roster + impl/reviewer model + tdd_required. Triggers: s>=- security-reviewer, d>=- data-reviewer, r>=+ reversibility-reviewer, b>=+ full code-quality, u>=+ adds novelty-reviewer + research. Crit axes hard-block. Model routes impl by tier (haiku-4.5/sonnet-4.6/opus-4.7) with crit + u-crit escalation; reviewer one tier down with security/post-task same-tier overrides. TDD when d|s>=- or b|u>=+."
disable-model-invocation: true
---

# risk-pipeline-dispatch

## 概覽 (Overview)

風險向量轉派發規格之技藝。呼叫方：`risk-classify`（Phase 06），在 `risk-budget`（Phase 07）產出 `verdict + task_risk + pipeline_tier` 之後調用。輸入風險向量、裁決、管道層、trivial_bypass 旗、配置，輸出 `pipeline_spec` 對象：審者陣列、impl/reviewer 模型、tdd_required 旗、硬阻增量（human_checkpoint/evidence/artifacts/research_task）。配對表照 spec §Pipeline dispatch line 368–384 字字照辦；模型路由照 line 386–406；TDD 規照 line 408–417。

## 輸入 (Inputs)

呼叫方必供：

- `task_risk: {b, d, s, r, u, scalar, crit_axes}` — 五軸整數（0–3）、總標量、crit 軸名（全名如 `security` 非 `s`）
- `verdict: ok | split_required | refactor_first_required | escalate` — 自 `risk-budget`
- `pipeline_tier: smoke | light | dim_matched | architectural` — 自 classify
- `trivial_bypass: bool` — 前濳八檢結果
- `config.model_routing` — 讀 `.claude/rules/risk.md` frontmatter；缺鍵回退 spec 默認
- `lci_diff` — 供 TDD skip 之 behavior-change 檢（無則保守視為有變動）

## 配對表 (Dim-matched dispatch table)

Spec §Pipeline dispatch line 368–384 十一行照錄：

| Trigger | Reviewer fires | Blocking |
|---|---|---|
| `s >= -` | security-reviewer | yes |
| `s = !` | + human checkpoint | hard-block |
| `d >= -` | data-reviewer | yes |
| `d = !` | + migration dry-run evidence | hard-block |
| `r >= +` | reversibility-reviewer | yes |
| `r = !` | + rollback runbook + canary plan | hard-block |
| `b >= +` | code-quality-reviewer (full) | yes |
| `u >= +` | novelty-reviewer + research task first | yes |
| Any axis `>= -` AND non-trivial | qa-reviewer | yes |
| All axes `.` | no reviewers | smoke |
| Trivial bypass | no reviewers | smoke |

觸發累加：一軸滿多條即多審派發（如 `s!` 兼觸 `s>=-` 與 `s=!`，派 security-reviewer + human_checkpoint）。reviewers 陣列去重。

## 硬阻 (Hard-block augmentations)

crit 軸觸發 hard-block，pipeline_spec 增欄：

| Trigger | Augmentation |
|---|---|
| `s = !` | `human_checkpoint: required` |
| `d = !` | `evidence_required: [migration_dry_run]` |
| `r = !` | `artifacts_required: [rollback_runbook, canary_plan]` |

多硬阻共現則並拼（如 `s!d!` 則 `human_checkpoint + evidence_required`）。`verdict: escalate` 無 crit 軸時亦強置 `human_checkpoint: required`（findability 違反升人工檢）。

## 並行與重試 (Parallel execution + retry)

- 全員審者**並行**發火（`reviewer_parallelism: all_parallel`），無序依。
- **重試**：每失敗審者最多 `2` 次重試，同輸入重發。`retry_policy: {max_retries: 2, scope: failing_only}`——僅失敗者重跑，成者不動。
- 重試後仍失則**硬阻**管道完成，待呼叫方（loop 協調器）決斷（修任務/分拆/升級）。
- 重試機制本身非本技藝實作——此文件僅述策略。實作見 Phase 10/11 loop 協調器。

## 模型路由 — impl (Model routing: implementer)

決策表，由上而下求交：

| Condition | Model |
|---|---|
| `trivial_bypass == true` | `haiku-4.5` |
| scalar 0–4 | `haiku-4.5` |
| scalar 5–9 | `sonnet-4.6` |
| scalar 10–14 | `sonnet-4.6` |
| scalar `>= 15` | `opus-4.7` |
| any axis `= !` | `opus-4.7` (override) |
| `u = !` | `opus-4.7` (research phase) |

**優先序明文**：crit 軸覆寫 > scalar 層。即任軸 `= !` 則 `opus-4.7`，無論 scalar 多低（除 `trivial_bypass` 不可能與 crit 共存——前濳檢查 8 安全路徑 + 無 schema 變動皆排除 crit 可能）。配置缺鍵以 spec 默認補。

## 模型路由 — reviewer (Model routing: reviewer)

| Case | Model |
|---|---|
| 默認 | one tier down from impl（地板 `haiku-4.5`） |
| `security-reviewer` | same tier as impl（特例不降） |
| `post-task-reviewer` | same tier as impl（特例不降） |

**tier 階梯**：`haiku-4.5 → sonnet-4.6 → opus-4.7`。「一級下」映射：

- `opus-4.7` → `sonnet-4.6`
- `sonnet-4.6` → `haiku-4.5`
- `haiku-4.5` → `haiku-4.5`（已地板）

其他 reviewer（qa-reviewer、data-reviewer、reversibility-reviewer、novelty-reviewer、code-quality-reviewer）皆走默認規則。

## TDD 必規 (TDD required)

**必備於**任一成：

- `d >= -`（測 migration/transform）
- `s >= -`（測 auth 路徑）
- `b >= +`（回歸面）
- `u >= +`（探索前 pin 行為）

**僅可跳**於全備成：

1. 上四條件**皆**不中（`d == .` 且 `s == .` 且 `b < +` 且 `u < +`）
2. `trivial_bypass == true` **或** 純樣式/文案/配置改動
3. `lci_diff` 示無行為變（無新符號、無函數簽名變、無控制流變；`lci_diff` 不可得時保守視為有變）

**默認**：required。跳 TDD 為顯性 opt-in，非 opt-out。三條任一不成即 `tdd_required: true`。

## 輸出 (pipeline_spec schema)

```yaml
pipeline_spec:
  impl_model: haiku-4.5 | sonnet-4.6 | opus-4.7
  required_reviewers:                # 觸發之審者陣列；無則空陣
    - {name: security-reviewer, model: sonnet-4.6, blocking: true}
    - {name: code-quality-reviewer, model: haiku-4.5, blocking: true}
    - {name: qa-reviewer, model: haiku-4.5, blocking: true}
  reviewer_parallelism: all_parallel
  retry_policy: {max_retries: 2, scope: failing_only}
  tdd_required: true | false
  human_checkpoint: required | false      # s=! 或 verdict=escalate 時 required
  evidence_required: [migration_dry_run]  # d=! 時出；否則省
  artifacts_required: [rollback_runbook, canary_plan]  # r=! 時出；否則省
  research_task_required: true | false    # u>=+ 時 true
  notes: "..."                             # 診斷回退旗，可選
```

欄義：`impl_model` 必出三檔之一。`required_reviewers` 元素含 `name/model/blocking`；reviewer 模型由上節規則獨立計算。`reviewer_parallelism` 恆 `all_parallel`。`retry_policy` 恆 `{2, failing_only}`。`human_checkpoint` 省時等同 `false`。`evidence_required` `artifacts_required` 僅 crit 時出。`research_task_required` `u>=+` 時 true（Phase 11 workflow 創任務）。

## 範例 (Examples)

重用 Phase 07 例三則。

**例 1 — `b.d.s.r.u.` + smoke**（trivial bypass）：

```
task_risk: {b:0, d:0, s:0, r:0, u:0, scalar:0, crit_axes:[]}
pipeline_tier: smoke
trivial_bypass: true

pipeline_spec:
  impl_model: haiku-4.5          # trivial_bypass → haiku
  required_reviewers: []         # "All axes ." 行 → no reviewers
  reviewer_parallelism: all_parallel
  retry_policy: {max_retries: 2, scope: failing_only}
  tdd_required: false            # 四條件皆 false + trivial + 假設 lci_diff 無行為變
  human_checkpoint: false
  research_task_required: false
```

**例 2 — `b+d.s.r.u.` scalar 6**（blast 高）：

```
task_risk: {b:2 (effective 3 after amp), d:0, s:0, r:0, u:0, scalar:6, crit_axes:[]}
pipeline_tier: light
trivial_bypass: false

觸發分析：
- b >= +（b=3）→ code-quality-reviewer (full)
- 任軸 >= - AND 非 trivial → qa-reviewer
- s/d/r/u 皆 < 觸發閾 → 其他 reviewer 不派

pipeline_spec:
  impl_model: sonnet-4.6         # scalar 5-9
  required_reviewers:
    - {name: code-quality-reviewer, model: haiku-4.5, blocking: true}   # 一級下
    - {name: qa-reviewer, model: haiku-4.5, blocking: true}
  reviewer_parallelism: all_parallel
  retry_policy: {max_retries: 2, scope: failing_only}
  tdd_required: true             # b >= + 觸
  human_checkpoint: false
  research_task_required: false
```

**例 3 — `b+d.s!r-u.` scalar 19 + crit security + escalate**：

```
task_risk: {b:2, d:0, s:3, r:1, u:0, scalar:19, crit_axes:[security]}
verdict: escalate
pipeline_tier: architectural
trivial_bypass: false

觸發分析：
- s >= -（s=3）→ security-reviewer
- s = ! → human_checkpoint
- r >= +（r=1? no, r=1=-，不觸 r>=+ 閾 2）→ 無 reversibility-reviewer
  ※ 重審：r=1 即 `-` 級，`r >= +` 需 r>=2。此例 r 不觸。
- b >= +（b=2）→ code-quality-reviewer
- 任軸 >= - → qa-reviewer
- u < + → 無 novelty；無 research_task

pipeline_spec:
  impl_model: opus-4.7           # crit 軸覆寫
  required_reviewers:
    - {name: security-reviewer, model: opus-4.7, blocking: true}        # same-tier
    - {name: code-quality-reviewer, model: sonnet-4.6, blocking: true}  # 一級下
    - {name: qa-reviewer, model: sonnet-4.6, blocking: true}
  reviewer_parallelism: all_parallel
  retry_policy: {max_retries: 2, scope: failing_only}
  tdd_required: true             # s >= -, b >= + 皆觸
  human_checkpoint: required     # s=! crit + escalate 雙觸
  research_task_required: false
  notes: "crit_security hard-block"
```

## 錯誤與回退 (Error + fallback)

- **配置 `model_routing` 缺**：用 spec §Model routing 默認（上節表格所載）；`notes: "model_routing_fallback"`。
- **審者名未注於代理註冊表**（Phase 14 未落地前可能）：降級為 `code-quality-reviewer`，記 warning `notes: "reviewer <name> unregistered, downgraded"`。呼叫方不阻。
- **`verdict == escalate` 無 crit 軸**（findability 違反所致）：仍強置 `human_checkpoint: required`；reviewer 集全派架構層羅盤（security+data+reversibility+novelty+qa+code-quality）。
- **`pipeline_tier: smoke` 與任一觸發條件衝突**（前濳應排除，但程式漏洞可能致）：記 integrity violation 警告，**守保守**——reviewers 發火，忽略 smoke 層 bypass。`notes: "integrity_violation_smoke_vs_trigger"`。
- **`lci_diff` 不可得**於 TDD skip 判斷：保守視為有行為變，`tdd_required: true`。

## 依賴 (Dependencies)

- **消費**：`risk-budget`（Phase 07，已建，task `spRTJjH4LPHS`）之 `task_risk + verdict`。
- **被調**：`risk-classify`（Phase 06，已建，task `bjKHROwLCMaq`）——Phase 06 當前使用 dispatch fallback stub，本技藝落地後 classify 可移除 fallback。
- **審者名引**：spec §Reviewer roster line 357–367 七員（`code-quality-reviewer`、`qa-reviewer`、`post-task-reviewer` 三舊；`security-reviewer`、`data-reviewer`、`reversibility-reviewer`、`novelty-reviewer` 四新）。四新者代理體 Phase 14（`emlONCR1TRH4`）創建；本技藝僅引名，不實作。
- **配置**：`.claude/rules/risk.md` frontmatter 之 `model_routing` 塊（Phase 09，已建）。
- **loop 協調**：重試機制、research 任務創建、hook 觸發皆 Phase 10（dartai）/ Phase 11（workflow）/ Phase 04（PostToolUse hook）之責，本技藝不實作。
