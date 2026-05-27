---
name: pcloud
description: 全面的 pCloud 雲端儲存 API 整合與 SDK 使用指南。適用於建構與 pCloud 互動的應用程式：(1) 檔案上傳/下載/管理、(2) 資料夾操作、(3) OAuth 2.0 認證、(4) 檔案/資料夾分享與公開連結、(5) 媒體串流（影片/音訊/HLS）、(6) 壓縮封存（zip/解壓縮）、(7) 縮圖、(8) 垃圾桶管理、(9) 檔案版本、(10) 收藏集、(11) 上傳連結，或 (12) 使用任何 pCloud SDK（JavaScript、PHP、Java、Swift、C）。
---

# pCloud API 開發技能

## 概述

pCloud 是一個雲端儲存服務，提供 REST 風格的 HTTP JSON API 和二進位協議。主要功能：
- **檔案管理** — 上傳、下載、複製、重新命名、刪除、校驗碼
- **資料夾操作** — 建立、列表（遞迴）、重新命名、刪除、複製
- **分享** — 與其他使用者共享資料夾（檢視/編輯權限）
- **公開連結** — 為檔案和資料夾產生公開下載/串流連結
- **媒體串流** — 直接檔案連結、影片轉碼、音訊串流、HLS
- **壓縮封存** — 在伺服器端建立/解壓縮 ZIP 封存檔
- **縮圖** — 在伺服器端產生圖片/影片縮圖
- **收藏集** — 將檔案組織成虛擬收藏集
- **垃圾桶** — 列表、還原、清除已刪除項目
- **版本** — 列表和還原檔案版本
- **上傳連結** — 建立允許他人上傳到您帳號的連結
- **遠端上傳** — 從 URL 直接下載檔案到 pCloud

## API 端點（資料中心）

> [!IMPORTANT]
> pCloud 運營**兩個資料中心**。根據使用者的資料位置使用正確的主機名稱。

| 位置 | API 主機名稱 | OAuth 主機名稱 |
|------|-------------|----------------|
| 美國（locationid=1） | `api.pcloud.com` | `my.pcloud.com` |
| 歐洲（locationid=2） | `eapi.pcloud.com` | `e.pcloud.com` |

OAuth 授權後，重新導向 URL 會包含 `locationid` 和 `hostname` 參數，指示該使用者應使用哪個 API 端點。**務必儲存並使用每個使用者對應的正確主機名稱。**

## 認證

### OAuth 2.0（推薦）

起始頁面：`https://my.pcloud.com/oauth2/authorize`（美國）或 `https://e.pcloud.com/oauth2/authorize`（歐洲）

**兩種流程：**

1. **授權碼流程**（伺服器應用） — 透過重新導向返回 `code` → 使用 `oauth2_token` 交換 `access_token`
   ```
   GET https://my.pcloud.com/oauth2/authorize?
     client_id=APP_ID&
     response_type=code&
     redirect_uri=REDIRECT_URI&
     state=RANDOM
   ```
   重新導向返回：`?code=XXXXX&locationid=1&hostname=api.pcloud.com`
   然後使用 code + `client_secret` 呼叫 `oauth2_token` 取得 bearer token。

2. **隱式流程**（純客戶端/行動應用） — 直接在重新導向片段中返回 `access_token`
   ```
   GET https://my.pcloud.com/oauth2/authorize?
     client_id=APP_ID&
     response_type=token&
     redirect_uri=REDIRECT_URI
   ```
   重新導向返回：`#access_token=XXXXX&token_type=bearer&locationid=1&hostname=api.pcloud.com`

### 使用認證令牌

在每個 API 呼叫中使用 `Authorization` 標頭傳遞 `access_token`：
```
GET https://api.pcloud.com/listfolder?folderid=0
Authorization: Bearer ACCESS_TOKEN
```

> **警告**：請勿將 token 作為 URL 參數（`?auth=...`）或放在 `multipart/form-data` 欄位中傳遞。如果未使用標頭傳遞 token，pCloud API 可能會靜默拒絕請求或回傳 `2000: Log in failed`。

### 摘要登入（舊式）

1. 呼叫 `getdigest` 取得摘要
2. 呼叫 `userinfo`，帶 `getauth=1&logout=1&username=EMAIL&digest=DIGEST&passworddigest=SHA1(PASSWORD+SHA1(USERNAME_LOWERCASE)+DIGEST)&authexpire=SECONDS`
3. 回應包含 `auth` 令牌

## HTTP JSON 協議

### 請求格式

所有方法接受 `GET` 和 `POST`。基底 URL：`https://api.pcloud.com/METHOD_NAME`

```bash
# GET 請求
curl -s -H "Authorization: Bearer TOKEN" "https://api.pcloud.com/listfolder?folderid=0"

# POST 請求
curl -s -X POST "https://api.pcloud.com/listfolder" \
  -H "Authorization: Bearer TOKEN" \
  -d "folderid=0"
```

### 回應格式

```json
// 成功
{ "result": 0, ... }

// 錯誤
{ "result": 2000, "error": "Log in required." }
```

### 檔案上傳

使用 `POST` 搭配 `multipart/form-data`。參數必須在檔案之前：
```bash
curl -s -X POST "https://api.pcloud.com/uploadfile" \
  -H "Authorization: Bearer TOKEN" \
  -F "folderid=0" \
  -F "file=@/path/to/file.jpg"
```

可在單一請求中上傳多個檔案。設定 `renameifexists=1` 以避免覆寫。

## 全域參數

這些可選參數適用於所有方法（在個別方法文件中省略）：
- `authexpire` — 令牌到期秒數（登入時）
- `authinactiveexpire` — 閒置 N 秒後到期
- `device` — 裝置識別字串

## 核心概念

### 識別碼
- **資料夾**：`folderid`（整數）或 `path`（字串）。根目錄始終為 `folderid=0`
- **檔案**：`fileid`（整數）或 `path`（字串）
- `folderid`/`fileid` 和 `path` 都可接受；若兩者都提供，`folderid`/`fileid` 優先

### 中繼資料結構

每個檔案/資料夾都會回傳中繼資料物件：
```json
{
  "name": "file.jpg",
  "isfolder": false,
  "fileid": 1729212,
  "parentfolderid": 0,
  "size": 73269,
  "contenttype": "image/jpeg",
  "category": 1,
  "created": "Wed, 02 Oct 2013 14:29:11 +0000",
  "modified": "Wed, 02 Oct 2013 14:29:11 +0000",
  "hash": 10681749967730527559,
  "isshared": false,
  "ismine": true,
  "thumb": true,
  "icon": "image"
}
```

**分類**：0=未分類、1=圖片、2=影片、3=音訊、4=文件、5=封存檔

## 常用工作流程

### 列出資料夾內容
```bash
curl -s -H "Authorization: Bearer TOKEN" "https://api.pcloud.com/listfolder?folderid=0&recursive=1"
```

### 上傳檔案
```bash
curl -s -H "Authorization: Bearer TOKEN" -F "folderid=0" -F "file=@photo.jpg" \
  https://api.pcloud.com/uploadfile
```

### 取得下載連結
```bash
curl -s -H "Authorization: Bearer TOKEN" "https://api.pcloud.com/getfilelink?fileid=123"
# 回傳：{ "hosts": ["c123.pcloud.com"], "path": "/cfZka..." }
# 下載 URL：https://c123.pcloud.com/cfZka...
```

### 分享資料夾
```bash
curl -s -H "Authorization: Bearer TOKEN" "https://api.pcloud.com/sharefolder?folderid=123&mail=user@example.com&permissions=edit"
```

### 建立公開連結
```bash
curl -s -H "Authorization: Bearer TOKEN" "https://api.pcloud.com/getfilepublink?fileid=123"
```

## 詳細參考

按需載入這些參考資料：

- **所有 API 方法（依分類）**：參閱 [api-methods.md](references/api-methods.md) 取得完整方法參考含參數和說明
- **SDK 設定與使用**：參閱 [sdks.md](references/sdks.md) 取得 JavaScript、PHP、Java、Swift、C SDK 詳情
- **錯誤碼**：參閱 [error-codes.md](references/error-codes.md) 取得錯誤碼表和疑難排解
