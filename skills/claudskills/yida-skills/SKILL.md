---
name: yida-server-api
description: >
  Yida (宜搭) server-side OpenAPI via DingTalk Open Platform.
  Use when calling Yida APIs from external systems — form CRUD, batch operations,
  process/workflow management, task approval, attachments.
  Authentication via DingTalk OAuth2 access_token.
  Trigger keywords: 宜搭, yida, API, 表單, form, 流程, process, 審批, approval, 服務端, server.
compatibility:
  - claude-code
metadata:
  auth: openapi
  platform: yida
  version: 2.0.0
  tags: [yida, dingtalk, openapi, server, form, process]
---

# 宜搭服務端 API 指南

## 概述

透過釘釘開放平台呼叫宜搭（Yida）服務端 OpenAPI，涵蓋表單 CRUD、批量操作、流程管理、任務審批。

所有 API 的 base URL 為 `https://api.dingtalk.com`，認證方式為釘釘 OAuth2 access_token（詳見 `reference/auth.md`）。

## 認證流程

1. 用 appKey + appSecret 呼叫 `/v1.0/oauth2/accessToken` 取得 token
2. 所有後續請求帶 Header `x-acs-dingtalk-access-token: {token}`
3. Token 有效期 7200 秒，在 7000 秒時刷新

## 環境變數

| 變數 | 用途 | 說明 |
|------|------|------|
| `DINGTALK_CLIENT_ID` | appKey | 釘釘應用 AppKey |
| `DINGTALK_CLIENT_SECRET` | appSecret | 釘釘應用 AppSecret |
| `YIDA_APP_TYPE` | appType | 宜搭應用編碼（如 `APP_XXXX`） |
| `YIDA_SYSTEM_TOKEN` | systemToken | 宜搭應用密鑰 |

## 共通參數

幾乎所有宜搭 API 都需要以下三個參數：

| 參數 | 說明 | 來源 |
|------|------|------|
| `appType` | 應用編碼 | 宜搭應用設定頁 → 應用編碼 |
| `systemToken` | 應用密鑰 | 宜搭應用設定頁 → 服務端密鑰 |
| `userId` | 操作人釘釘 userId | 當前操作者的釘釘用戶 ID |

## 子技能速查

| 技能 | 路徑 | 用途 | 觸發關鍵詞 |
|------|------|------|-----------|
| yida-form-api | `skills/yida-form-api/SKILL.md` | 表單 CRUD、批量操作、高級查詢 | 表單、form、CRUD、查詢、批量、子表 |
| yida-process-api | `skills/yida-process-api/SKILL.md` | 發起/終止流程、審批任務、轉交 | 流程、process、審批、approval、任務 |

## 參考文件速查

| 文件 | 路徑 | 內容 |
|------|------|------|
| 認證 | `reference/auth.md` | access_token 取得、緩存策略、Header 格式 |
| 組件格式 | `reference/component-format.md` | 各組件類型在 formDataJson 中的精確 JSON 格式 |
| 篩選語法 | `reference/filter-syntax.md` | searchFieldJson 結構、運算子、預置字段 |
| 限流配額 | `reference/rate-limits.md` | 月配額、QPS 限制、IP 封禁、重試策略 |

> **Loading trigger**：處理 formDataJson 格式問題時，**必須**讀取 `reference/component-format.md`。撰寫篩選條件時，**必須**讀取 `reference/filter-syntax.md`。

## API 選擇決策樹

| 需求 | 用哪個 API | 子技能 |
|------|-----------|--------|
| 查詢表單數據（不含子表） | searchFormDatas | yida-form-api |
| 查詢表單數據（含子表） | searchFormDataSecondGeneration | yida-form-api |
| 單筆新增/更新/查詢/刪除 | save/update/get/delete FormData | yida-form-api |
| 批量操作 | batchSave/batchUpdate/batchDelete | yida-form-api |
| 發起審批流程 | startInstance | yida-process-api |
| 審批任務（同意/拒絕） | executeTask | yida-process-api |
| 終止流程 | terminateInstance | yida-process-api |
| 查詢流程狀態 | getProcessInstance | yida-process-api |

## 絕對不要

- **NEVER** 混用表單接口和流程接口 — 表單走 `/v2.0/yida/forms/`，流程走 `/v2.0/yida/processes/`，主鍵和返回結構完全不同
- **NEVER** 頻繁呼叫 accessToken 接口 — 緩存 token，在過期前刷新即可
- **NEVER** 忽略 QPS 限制 — 標準版每應用每接口 20 次/秒，IP 維度 20 秒 10,000 次
- **NEVER** 把 formDataJson 當 JSON 物件傳 — 必須是 JSON 字串（`JSON.stringify(obj)`）
- **NEVER** 假設所有組件值格式相同 — 成員是 Array、日期是毫秒時間戳、地址是 Object，格式各異
- **NEVER** 假設有服務端附件上傳 API — 宜搭**沒有**服務端上傳接口，附件只能透過 OSS 直傳（需 cookies 登入態，非 access_token）
