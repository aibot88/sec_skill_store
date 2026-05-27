---
name: oc-clawhub
description: "Use when the user asks to search, browse, install, or audit ClawHub skills, or says '找 skill', 'search clawhub', '裝 skill', 'install skill', '安全檢查', 'audit skill', 'suggest skills', '推薦 skill', or wants to add new capabilities from ClawHub."
---

# oc-clawhub

## Runtime Configuration

執行前讀取 `setup.json`：
- SSH 連線用 `remote.sshAlias`（以下以 `${SSH_ALIAS}` 表示）
- 遠端路徑用 `remote.openclawPath`（以下以 `${OPENCLAW_PATH}` 表示）
- Workspace 清單從 `agents` 陣列取得（每個 agent 的 `workspaceDir`）

## A. 前置條件

> 執行環境：遠端（SSH）

確認遠端有 `clawhub` CLI：

```bash
ssh ${SSH_ALIAS} 'which clawhub'
```

如果不存在，安裝它：

```bash
ssh ${SSH_ALIAS} 'npm install -g clawhub'
```

安裝失敗則回報錯誤並結束。

## B. 搜尋 ClawHub Skills

> 執行環境：遠端（SSH）→ LOCAL 呈現

### 1. 確認搜尋關鍵字

如果使用者沒有提供關鍵字，用 AskUserQuestion 詢問要搜尋什麼。

### 2. 執行搜尋

```bash
ssh ${SSH_ALIAS} 'clawhub search "<query>"'
```

### 3. 列出已安裝的 skills（參考用）

```bash
# 使用第一個 agent 的 workspace 查詢
ssh ${SSH_ALIAS} 'cd ${OPENCLAW_PATH}/workspace-<workspaceDir> && clawhub list'
```

### 4. 呈現結果

以表格呈現搜尋結果：

```
| # | Skill | 作者 | 說明 |
|---|-------|------|------|
| 1 | ... | ... | ... |
```

提供快捷選項：
- `audit N` — 對第 N 個結果執行安全審查
- `install N` — 對第 N 個結果執行安全審查 + 安裝

## C. 安全審查

> 執行環境：遠端（SSH 取得檔案）→ LOCAL（Claude 分析）→ 遠端（清理）

**安裝前必經此步驟。** 不可跳過。

### 1. 安裝到暫存目錄

```bash
ssh ${SSH_ALIAS} 'mkdir -p /tmp/clawhub-audit && cd /tmp/clawhub-audit && clawhub install <slug>'
```

### 2. 讀取 skill 檔案 [遠端 → LOCAL]

列出暫存目錄中的 SKILL.md 和所有附帶檔案（`.sh`、`.py`、`.js` 等）：

```bash
ssh ${SSH_ALIAS} 'find /tmp/clawhub-audit -type f'
```

對 find 結果中的每個檔案，用 SSH 讀取內容回 LOCAL：

```bash
ssh ${SSH_ALIAS} 'cat /tmp/clawhub-audit/<path>'
```

逐一讀取所有找到的檔案，將內容帶回 LOCAL 供後續分析。

### 3. 七項安全檢查 [LOCAL — Claude 分析已讀取的內容]

依照 `references/security-audit-checklist.md` 中的清單，對讀取到的所有內容逐項檢查（含 blocklist、危險指令、機密存取、網路通訊、寫入範圍、prompt injection、功能合理性）。

### 4. 評級與報告 [LOCAL — Claude 產生報告]

依照 `references/security-audit-checklist.md` 中的評級邏輯和報告模板輸出結果：

- Red：說明哪些項目 FAIL，建議略過
- Yellow：列出 WARN 項目，請使用者決定
- Green：告知可安裝，等使用者確認

### 5. 清理暫存

清理本 skill 建立的暫存目錄（僅 `/tmp/clawhub-audit`，本步驟建立的，可安全刪除）：

```bash
ssh ${SSH_ALIAS} 'rm -rf /tmp/clawhub-audit'
```

## D. 安裝到遠端

> 執行環境：LOCAL（確認）→ 遠端（SSH 安裝）

**前提：** 安全審查已完成，評級為 Green 或使用者已確認 Yellow。Red 評級不可安裝。

### 1. 選擇目標 workspace

用 AskUserQuestion 詢問，選項從 `setup.json` 的 `agents` 陣列動態產生：
- **單一 workspace** — 選擇某個 agent 的 workspace
- **全部 workspace** — 安裝到所有 agent 的 workspace

### 2. 確認安裝（STOP gate）

列出即將執行的操作，**必須等使用者明確確認**才繼續（Law 1 — SSH 安全）。

### 3. 執行安裝

對每個目標 workspace：

```bash
ssh ${SSH_ALIAS} 'cd ${OPENCLAW_PATH}/workspace-<workspaceDir> && clawhub install <slug>'
```

### 4. 驗證

```bash
ssh ${SSH_ALIAS} 'cd ${OPENCLAW_PATH}/workspace-<workspaceDir> && clawhub list'
```

確認新 skill 出現在已安裝清單中。

### 5. 提醒重啟

安裝完成後提醒使用者：

> Skill 已安裝。如果 skill 含有 boot-md 載入的檔案，需要重啟 gateway 才會生效：
> `ssh ${SSH_ALIAS} 'systemctl --user restart ${SERVICE_NAME}'`

## E. 情境建議指引

此段落不是給使用者看的步驟，而是給 Claude 的判斷指引。

**適合在回覆末尾提及 `/oc-clawhub` 的情境：**
- 使用者討論新功能需求，且現有工具無法滿足
- 使用者問「有沒有 skill 可以...」
- 使用者討論工具整合或 agent 能力擴展

**不適合提及的情境：**
- 日常操作、閒聊、debug
- 現有 skill 或工具已能解決
- 使用者正在專注處理其他任務

**格式：** 一句話帶過，例如「如果需要，可以用 `/oc-clawhub` 搜尋 ClawHub 市集看看有沒有相關 skill。」
