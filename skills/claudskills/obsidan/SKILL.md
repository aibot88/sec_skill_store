---
name: obsidan
description: 自動化 Obsidian 筆記庫與 KM 核心知識庫 (OneDrive) 的同步與結構化管理。
---

# Obsidian 數位大腦同步技能

此技能專門用來管理 Obsidian 筆記庫，並將其與你的 `KM 核心知識庫 (OneDrive)` 進行無縫同步。

## 核心功能

1. **結構同步**：掃描 `/Users/dwaynejohnson/Library/CloudStorage/OneDrive-個人/Documents/00_KM_核心知識庫` 並在 Obsidian 庫中自動建立一致的目錄結構。
2. **筆記轉化**：將 KM 庫中的 Markdown 檔案自動同步至 Obsidian 指定目錄。
3. **編碼檢查**：確保 Obsidian 中的分類與 OneDrive 的「兩位數編碼」體系完全一致。

## 使用範例

- 「將最近的 KM 執行報告同步到我的 Obsidian」
- 「檢查 Obsidian 與 OneDrive 的目錄結構是否一致」
- 「在 Obsidian 中為這個項目建立一個新的筆記」

## 歸檔路徑
預設 Obsidian 庫路徑（需用戶指定）：`/Users/dwaynejohnson/Documents/ObsidianVault/`
KM 核心路徑：`/Users/dwaynejohnson/Library/CloudStorage/OneDrive-個人/Documents/00_KM_核心知識庫/`

## 執行邏輯
本技能調用 `run_shell_command` 執行 `rsync` 或 `cp` 指令進行物理同步，並透過 `grep_search` 確保內容的一致性。
