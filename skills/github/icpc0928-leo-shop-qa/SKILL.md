# QA 測試 Skill — Leo Shop (CryptoShop)

> **AI 測試人員請先讀本文件，再讀 `TEST_CASES.md` 取得所有測試案例。**
> 測試完成後，複製 `reports/TEMPLATE.md` 產出報告，Bug 用 `bugs/TEMPLATE.md` 格式記錄。

## 專案概述

這是一個支援加密貨幣支付的電商網站，前後端分離架構。

- **前端**：Next.js 14 (App Router) + TypeScript + Tailwind CSS + DaisyUI v5
- **後端**：Java 25 + Spring Boot + PostgreSQL
- **特色功能**：加密貨幣支付（BTC/ETH/USDT/Polygon）、多語系（中/英）、多幣種、CMS 內容管理

---

## 測試環境

| 項目 | URL |
|------|-----|
| 前台 | https://cryptoshop.aligrich.com |
| 後台 API | https://cryptoshop-api.aligrich.com |
| Admin 後台 | https://cryptoshop.aligrich.com/admin |
| Admin 帳號 | admin@leoshop.com |
| Admin 密碼 | admin123 |

### Admin 登入 API
```bash
curl -s https://cryptoshop-api.aligrich.com/api/admin/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@leoshop.com","password":"admin123"}'
# 回傳 {"token":"..."}
```

### 一般用戶
可在前台 `/register` 自行註冊測試帳號。

---

## 專案結構

### 前端 (`leo-shop/`)
```
src/
├── app/
│   ├── page.tsx                  # 首頁
│   ├── products/page.tsx         # 商品列表
│   ├── products/[slug]/page.tsx  # 商品詳情
│   ├── cart/page.tsx             # 購物車
│   ├── checkout/page.tsx         # 結帳
│   ├── wishlist/page.tsx         # 願望清單
│   ├── account/page.tsx          # 會員中心
│   ├── about/page.tsx            # 關於我們
│   ├── contact/page.tsx          # 聯絡我們
│   ├── faq/page.tsx              # FAQ（從 API 讀取）
│   └── admin/
│       ├── login/page.tsx        # Admin 登入
│       ├── page.tsx              # Dashboard
│       ├── products/page.tsx     # 商品管理
│       ├── categories/page.tsx   # 分類管理
│       ├── orders/page.tsx       # 訂單管理
│       ├── crypto-orders/page.tsx # 加密訂單
│       ├── users/page.tsx        # 用戶管理
│       ├── admin-users/page.tsx  # 管理員管理
│       ├── payment-methods/page.tsx # 支付方式管理
│       ├── settings/page.tsx     # 系統設定
│       ├── banners/page.tsx      # 輪播管理
│       ├── faqs/page.tsx         # FAQ 管理
│       ├── pages/page.tsx        # 頁面管理
│       └── team/page.tsx         # 團隊管理
├── components/                   # 共用元件
├── lib/api.ts                    # API 串接（fetchAPI / fetchAdminAPI）
├── contexts/                     # SiteContext, CurrencyContext
└── config/themes.ts              # 主題設定
```

### 後端 (`leo-shop-api/`)
```
src/main/java/com/leoshop/
├── config/
│   ├── SecurityConfig.java       # 權限設定（哪些 API 需要登入）
│   ├── CorsConfig.java           # CORS（環境變數驅動）
│   └── ScheduledConfig.java      # 排程（匯率自動刷新）
├── controller/                   # 所有 API endpoint
├── model/                        # Entity（對應 DB table）
├── repository/                   # JPA Repository
├── service/                      # 業務邏輯
├── dto/                          # Request/Response DTO
└── security/                     # JWT 驗證
```

---

## API Endpoint 總覽

### Public（不需登入）
| Method | Path | 說明 |
|--------|------|------|
| POST | `/api/auth/register` | 用戶註冊 |
| POST | `/api/auth/login` | 用戶登入 |
| POST | `/api/admin/auth/login` | Admin 登入 |
| GET | `/api/products` | 商品列表（支援 `keyword`, `category`, `page`, `size`, `sort`） |
| GET | `/api/products/{slug}` | 商品詳情 |
| GET | `/api/categories` | 分類列表 |
| GET | `/api/site-info` | 站名 + 基礎幣種 |
| GET | `/api/exchange-rates` | 匯率列表 |
| GET | `/api/payment-methods` | 支付方式列表 |
| GET | `/api/banners` | 輪播列表（啟用中） |
| GET | `/api/faqs` | FAQ 列表（啟用中） |
| GET | `/api/pages/{slug}` | 靜態頁面 |
| GET | `/api/team-members` | 團隊成員（啟用中） |
| GET | `/api/orders/shipping-fee` | 運費資訊 |
| GET | `/uploads/**` | 上傳的圖片 |

### 需要用戶登入（Bearer Token）
| Method | Path | 說明 |
|--------|------|------|
| GET | `/api/orders` | 我的訂單 |
| POST | `/api/orders` | 建立訂單 |
| GET | `/api/addresses` | 地址列表 |
| POST | `/api/addresses` | 新增地址 |
| GET | `/api/wishlist` | 願望清單 |
| GET | `/api/wishlist/ids` | 願望清單 ID 列表 |
| POST | `/api/wishlist/{id}` | 加入/移除願望清單 |
| GET | `/api/user/profile` | 個人資料 |
| PUT | `/api/user/profile` | 更新個人資料 |
| PUT | `/api/user/password` | 修改密碼 |
| POST | `/api/payments/crypto/**` | 加密支付相關 |
| GET | `/api/crypto-orders/**` | 加密訂單 |

### 需要 Admin 登入（Bearer Token + ROLE_ADMIN）
| Method | Path | 說明 |
|--------|------|------|
| GET/POST/PUT/DELETE | `/api/admin/products/**` | 商品 CRUD |
| GET/POST/PUT/DELETE | `/api/admin/categories/**` | 分類 CRUD |
| GET | `/api/admin/orders` | 訂單管理（支援搜尋、篩選、分頁） |
| PATCH | `/api/admin/orders/{id}/status` | 更新訂單狀態 |
| GET | `/api/admin/crypto-orders` | 加密訂單管理 |
| PATCH | `/api/admin/crypto-orders/{id}/confirm` | 手動確認加密訂單 |
| GET/POST/PUT/DELETE | `/api/admin/users/**` | 用戶管理 |
| GET/POST/PUT/DELETE | `/api/admin/admin-users/**` | 管理員管理 |
| GET/PUT | `/api/admin/settings` | 系統設定 |
| GET/POST/PUT/DELETE/PATCH | `/api/admin/banners/**` | 輪播管理 |
| GET/POST/PUT/DELETE/PATCH | `/api/admin/faqs/**` | FAQ 管理 |
| GET/POST/PUT/DELETE/PATCH | `/api/admin/pages/**` | 頁面管理 |
| GET/POST/PUT/DELETE/PATCH | `/api/admin/team-members/**` | 團隊管理 |
| GET/PUT/PATCH | `/api/admin/payment-methods/**` | 支付方式管理 |
| POST | `/api/admin/exchange-rates/refresh` | 刷新匯率 |
| POST | `/api/upload/images` | 圖片上傳 |
| DELETE | `/api/upload/images` | 圖片刪除 |

---

## 測試範圍與案例

### P0 — 核心流程（必測）

#### TC-001：用戶註冊
1. 進入 `/register`
2. 填寫 email、密碼、名字
3. 點擊註冊
4. **預期**：註冊成功，跳轉首頁

#### TC-002：用戶登入
1. 進入 `/login`
2. 輸入已註冊的帳密
3. **預期**：登入成功，跳轉首頁，右上角顯示用戶名

#### TC-003：瀏覽商品
1. 進入 `/products`
2. 使用分類篩選、搜尋關鍵字、切換排序
3. 點擊商品進入詳情頁
4. **預期**：列表正確載入、篩選/搜尋結果正確、詳情頁顯示完整資訊

#### TC-004：加入購物車
1. 在商品詳情頁調整數量
2. 點擊「加入購物車」
3. **預期**：購物車 badge 數量更新、進入購物車頁面能看到商品

#### TC-005：購物車操作
1. 修改商品數量
2. 刪除商品
3. 確認金額計算正確（含運費、免運門檻）
4. **預期**：金額即時更新、刪除正常

#### TC-006：結帳流程
1. 從購物車點「前往結帳」
2. 未登入 → **預期**：跳轉登入頁
3. 已登入 → 填寫/選擇地址
4. 選擇支付方式
5. 提交訂單
6. **預期**：訂單建立成功，顯示訂單資訊

#### TC-007：Admin 登入
1. 進入 `/admin/login`
2. 輸入 admin 帳密
3. **預期**：進入 Dashboard

#### TC-008：商品管理 CRUD
1. 新增商品（含圖片上傳）
2. 編輯商品
3. 刪除商品
4. **預期**：前台即時反映變更

### P1 — 管理功能

#### TC-009：訂單管理
1. 搜尋訂單（關鍵字、日期範圍、狀態篩選）
2. 查看訂單詳情
3. 更新訂單狀態
4. **預期**：搜尋結果正確、狀態變更成功

#### TC-010：CMS 輪播管理
1. 新增輪播（含圖片上傳、背景色設定）
2. 編輯輪播
3. 停用/啟用
4. 刪除
5. **預期**：前台首頁即時反映

#### TC-011：CMS FAQ 管理
1. 新增 FAQ
2. 編輯
3. 調整排序
4. 停用/啟用
5. **預期**：前台 `/faq` 即時反映

#### TC-012：系統設定
1. 修改站名
2. 修改基礎幣種
3. 修改運費/免運門檻
4. **預期**：前台標題、價格、運費即時反映

#### TC-013：支付方式管理
1. 啟用/停用支付方式
2. 修改匯率
3. 刷新匯率（CoinGecko）
4. **預期**：結帳頁面反映變更

#### TC-014：用戶管理
1. 查看用戶列表
2. 搜尋用戶
3. **預期**：列表載入正確

#### TC-015：願望清單
1. 未登入點愛心 → **預期**：跳轉登入
2. 已登入加入願望清單
3. 進入 `/wishlist` 查看
4. 移除商品
5. **預期**：操作正常、即時反映

### P2 — 邊界與安全

#### TC-016：權限測試
1. 未帶 Token 打 admin API → **預期**：401
2. 一般用戶 Token 打 admin API → **預期**：403
3. 過期 Token 操作 → **預期**：前端自動跳轉登入

#### TC-017：輸入驗證
1. 商品價格輸入負數 / 0 / 文字
2. 商品名稱空白
3. 搜尋特殊字元（`' " < > & \`）
4. 圖片上傳非圖片檔案
5. 圖片上傳超過 5MB
6. **預期**：適當的錯誤提示，不產生 500 錯誤

#### TC-018：多語系
1. 切換到英文
2. 各頁面文字是否正確翻譯
3. 切回中文
4. **預期**：語言切換正常，無缺漏

#### TC-019：多幣種
1. 切換不同幣種（TWD / USD / EUR 等）
2. 商品價格是否正確換算
3. **預期**：價格即時更新、符號正確

#### TC-020：RWD 響應式
1. 桌面 (1920px)
2. 平板 (768px)
3. 手機 (375px)
4. **預期**：排版正常、按鈕可點擊、無溢出

---

## 測試方式

### UI 測試
使用 `browser` 工具操作前台和後台頁面，用 `snapshot` 檢查頁面狀態。

### API 測試
使用 `exec` 工具執行 curl 指令直接打 API，驗證回傳格式和狀態碼。

```bash
# 範例：取得商品列表
curl -s https://cryptoshop-api.aligrich.com/api/products?page=0&size=5

# 範例：Admin 操作（帶 Token）
TOKEN=$(curl -s https://cryptoshop-api.aligrich.com/api/admin/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@leoshop.com","password":"admin123"}' | jq -r '.token')

curl -s https://cryptoshop-api.aligrich.com/api/admin/orders \
  -H "Authorization: Bearer $TOKEN"
```

---

## 回報格式

每個測試案例回報：

```
### TC-XXX：測試名稱
- **狀態**：✅ PASS / ❌ FAIL / ⚠️ WARN
- **步驟**：（重現步驟，FAIL 時必填）
- **預期**：XXX
- **實際**：XXX
- **截圖**：（如有）
- **備註**：（改善建議等）
```

最終產出一份彙整表：
```
| 編號 | 測試項目 | 優先級 | 狀態 | 備註 |
|------|---------|--------|------|------|
| TC-001 | 用戶註冊 | P0 | ✅ | |
| TC-002 | 用戶登入 | P0 | ❌ | 密碼錯誤無提示 |
```

---

## 注意事項

- 測試站資料可以隨意新增修改刪除
- 加密貨幣支付流程在測試站無法真正驗證上鏈，只測 UI 流程
- 圖片上傳後存在 `/uploads/products/` 目錄
- 後端用 JPA `ddl-auto: update`，schema 變更自動套用
- 前端 `NEXT_PUBLIC_API_URL` 是 build time 變數，改了需要 rebuild
