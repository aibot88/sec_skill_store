---
name: bookkeeping
description: 記帳系統。解析自然語言記帳指令，寫入 SQLite 資料庫並同步 Beancount 帳本。Use when user wants to record expenses, check spending, query transaction history, or manage accounts. Triggers on keywords like "記帳", "記賬", "花了", "買了", "支出", "收入", amount+category patterns (e.g. "40 飲料", "午餐 200").
---

# Bookkeeping Skill

解析自然語言記帳 → SQLite（source of truth）→ 同步 Beancount。

## 檔案結構

```
bookkeeping/
├── SKILL.md
├── scripts/
│   ├── init_db.py          # 初始化 SQLite
│   ├── add_transaction.py  # 新增交易
│   └── sync_beancount.py   # SQLite → Beancount 全量同步
└── references/
    └── accounts.md         # 帳戶對照表
```

## 資料路徑

- **SQLite:** `~/.openclaw/workspace/ledger/bookkeeping.db`
- **Beancount:** `~/.openclaw/workspace/ledger/main.beancount`

## 核心流程：記帳

1. 收到記帳訊息（如 "40 飲料"、"午餐便當80 飲料40"）
2. 解析出交易列表：每筆含 `date`, `payee`, `narration`, `account`, `amount`
3. 執行 `scripts/add_transaction.py`，傳入原始訊息 + 解析結果（如有提到店家，加 `shop` 欄位）
4. 腳本自動：寫入 SQLite + append Beancount
5. 回覆確認

### 解析規則

- 金額 + 類別：「40 飲料」→ amount=40, narration=飲料
- 類別 + 金額：「午餐 200」→ amount=200, narration=午餐
- 多筆合一：「午餐80 飲料40」→ 兩筆交易，共用同一 message
- 日期預設今天，可指定：「昨天午餐 150」「2/20 加油 1500」
- 帳戶映射見 `references/accounts.md`
- 店家（shop）：用戶有提到才記錄，沒提不強制（如「麥當勞 晚餐169」→ shop=麥當勞）

### 付款方式

- 預設：Assets:Cash
- 可指定：「刷卡 午餐 300」→ Liabilities:CreditCard
- 關鍵字：刷卡/信用卡 → CreditCard，轉帳 → Bank:Checking

## 查詢

- 「今天花了多少」→ 查 SQLite 當日 SUM
- 「這個月飲料花了多少」→ 按 account + 月份查詢
- 「最近的記帳」→ 最近 N 筆

## add_transaction.py 用法

```bash
# 無店家
python3 scripts/add_transaction.py \
  --db ~/.openclaw/workspace/ledger/bookkeeping.db \
  --beancount ~/.openclaw/workspace/ledger/main.beancount \
  --message "40 飲料" \
  --sender "2078364301" \
  --transactions '[{"date":"2026-02-24","payee":"飲料店","narration":"飲料","account":"Expenses:Food:Drinks","amount":40,"currency":"TWD"}]'

# 有店家
python3 scripts/add_transaction.py \
  --db ~/.openclaw/workspace/ledger/bookkeeping.db \
  --beancount ~/.openclaw/workspace/ledger/main.beancount \
  --message "麥當勞 晚餐169" \
  --sender "2078364301" \
  --transactions '[{"date":"2026-02-24","payee":"麥當勞","narration":"晚餐","account":"Expenses:Food:DiningOut","amount":169,"currency":"TWD","shop":"麥當勞"}]'
```

## 注意事項

- SQLite 是 source of truth，Beancount 可由 SQLite 重新生成
- 重複記帳檢查：同一 message 不重複寫入
- Beancount payee 欄位必填（格式：`"payee" "narration"`）
- 相對日期（昨天、上禮拜五）先用 `date` 命令確認再計算
