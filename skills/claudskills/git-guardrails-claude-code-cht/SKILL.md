---
name: git-guardrails-claude-code-cht
description: "設定 Claude Code hooks，在 push、reset --hard、clean、branch -D 等危險 git 指令執行前阻擋。當使用者想防止破壞性 git 操作、加入 git 安全 hooks，或阻擋 git push/reset 時使用。"
---

# Claude Code Git Guardrails

設定 Claude Code hooks，在危險 git 指令執行前阻擋它們。

## 目標

避免 agent 或使用者誤執行會破壞工作狀態的 git 指令，例如 git push、git reset --hard、git clean、git branch -D、git checkout -- path，以及其他會刪除、覆蓋或不可逆改變工作樹的操作。

## 工作流程

1. 檢查目前 repo 是否有 Claude Code hooks 設定。
2. 若沒有，建立 hook 目錄與設定檔。
3. 安裝 scripts/block-dangerous-git.sh 或等價 blocking script。
4. 設定 hook 在 git 指令執行前檢查 command line。
5. 對高風險指令輸出清楚警告並中止。
6. 驗證安全指令可通過，危險指令會被阻擋。

## 設計原則

- 預設保守：不確定是否危險時，要求使用者明確確認。
- 錯誤訊息要說明被阻擋的原因與替代做法。
- 不要阻擋只讀指令，例如 git status、git diff、git log。
- 不要修改使用者未要求的 hooks 或設定。

## 驗證

用安全的 dry-run 或 mock command 測試 matching 邏輯，不要真的執行破壞性 git 指令。
