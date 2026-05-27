# Dynamic Layout Report System - LLM Skill Guide

本文件提供 LLM Agent 使用動態佈局報告系統的完整指南。系統採用「**佈局優先，內容填充**」架構，分為兩個階段：

1. **Layout 建立階段** - 設計報告的視覺結構
2. **Content 填充階段** - 依照 Slot 定義填入實際內容

---

## 目錄

1. [系統概述](#1-系統概述)
2. [ID 格式規範](#2-id-格式規範)
3. [Layout 建立指南](#3-layout-建立指南)
4. [Content 填充指南](#4-content-填充指南)
5. [Component 資料格式詳解](#5-component-資料格式詳解)
6. [完整範例](#6-完整範例)
7. [常見錯誤與排除](#7-常見錯誤與排除)

---

## 1. 系統概述

### 1.1 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                    Manager Agent                              │
│  1. GET /capabilities → 了解系統能力與限制                     │
│  2. 設計 Layout 結構（Container + Slot 樹狀結構）             │
│  3. POST /reports → 建立報告，取得 report_id                  │
│  4. 分派 slot_id 給 Sub-agents                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Sub-agents (並行)                          │
│  1. 接收分配的 slot_id 與 component 類型                      │
│  2. 產生對應格式的內容                                        │
│  3. PATCH /reports/{id} → 填入 content                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    完成                                       │
│  - 前端即時渲染 Layout + Content                              │
│  - 可選：POST /reports/{id}/export → 匯出 PDF                 │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 核心概念

| 概念 | 說明 |
|------|------|
| **Layout** | 定義報告的視覺結構，是一棵由 Container 和 Slot 組成的樹 |
| **Container** | 容器節點，可以是 `grid`（網格）或 `flex`（彈性盒），用於排列子節點 |
| **Slot** | 葉子節點，定義內容插槽，每個 Slot 有唯一的 `slot_id` 和指定的 `component` 類型 |
| **Content** | 實際內容，以 `slot_id` 為 key 的 Map 結構，與 Layout 分離儲存 |

---

## 2. ID 格式規範

### 2.1 ULID 格式

所有 ID 使用 **ULID (Universally Unique Lexicographically Sortable Identifier)** 格式：

```
標準 ULID: 01JHEZ8KXJMJ2PQRS3T4UV5WXY (26 字元)
          |---------|---------------|
          Timestamp    Randomness
          (10 chars)   (16 chars)
```

**ULID 字元集**（Crockford's Base32）：
- 允許：`0-9`, `A-H`, `J-K`, `M-N`, `P-T`, `V-Z`
- 不允許：`I`, `L`, `O`, `U`（避免混淆）

### 2.2 ID 類型與前綴

| 類型 | 前綴 | 正則表達式 | 範例 |
|------|------|-----------|------|
| Report | `rpt_` | `^rpt_[0-9A-HJKMNP-TV-Z]{26}$` | `rpt_01JHEZ8KXJMJ2PQRS3T4UV5WXY` |
| Slot | `slot_` | `^slot_[0-9A-HJKMNP-TV-Z]{26}$` | `slot_01JHEZ8KXKMJ2PQRS3T4UV5WX0` |
| Agent | `agt_` | `^agt_[0-9A-HJKMNP-TV-Z]{26}$` | `agt_01JHEZ9ABCMJ2PQRS3T4UV5WX0` |
| Export | `exp_` | `^exp_[0-9A-HJKMNP-TV-Z]{26}$` | `exp_01JHEZABC0MJ2PQRS3T4UV5WX0` |

### 2.3 生成 Slot ID

```javascript
import { ulid } from 'ulid';

// 每個 Slot 必須有唯一的 ID
const slotId = `slot_${ulid()}`;  // slot_01JHEZ8KXKMJ2PQRS3T4UV5WX0
```

---

## 3. Layout 建立指南

### 3.1 Layout 結構

Layout 是一個樹狀結構，使用 **Discriminated Union** 設計：

```typescript
type LayoutNode = ContainerNode | SlotNode;

// 容器節點 - 可包含子節點
interface ContainerNode {
  node_type: 'container';           // 識別為容器
  container_type: 'grid' | 'flex';  // 容器類型
  props: ContainerProps;            // 容器屬性
  children: LayoutNodeWrapper[];    // 子節點陣列
}

// 插槽節點 - 葉子節點
interface SlotNode {
  node_type: 'slot';                // 識別為插槽
  id: string;                       // slot_{ulid} 格式
  component: ComponentType;         // 內容類型
  meta?: SlotMeta;                  // 可選的元資料
}

// 子節點包裝器
interface LayoutNodeWrapper {
  grid_item?: GridItemProps;        // Grid 專用的項目屬性
  node: LayoutNode;                 // 實際節點
}
```

### 3.2 深度限制

**最大深度：2 層**（從 root 開始計算）

```
depth 0: root Container (grid/flex)
    │
    └── depth 1: 可以是 Container 或 Slot
            │
            └── depth 2: 必須是 Slot（不能再有 Container）
```

**範例結構**：
```
Grid (depth 0)
├── Flex (depth 1)
│   ├── Slot: text_h1 (depth 2) ✓
│   └── Slot: markdown (depth 2) ✓
└── Slot: chart_js (depth 1) ✓
```

### 3.3 Container 類型

#### Grid Container（網格佈局）

適合定義主要框架區塊，類似 CSS Grid。

```json
{
  "node_type": "container",
  "container_type": "grid",
  "props": {
    "columns": 12,              // 欄數（建議用 12 欄系統）
    "rows": 2,                  // 列數（可選）
    "gap": "16px",              // 間距
    "padding": "24px"           // 內距
  },
  "children": [...]
}
```

**Grid Item 屬性**（定義在 `LayoutNodeWrapper.grid_item` 中）：

```json
{
  "grid_item": {
    "col_span": 4,              // 跨越 4 欄
    "row_span": 2,              // 跨越 2 列（可選）
    "col_start": 1,             // 從第 1 欄開始（可選）
    "row_start": 1              // 從第 1 列開始（可選）
  },
  "node": { ... }
}
```

#### Flex Container（彈性盒佈局）

適合單向流動排列，類似 CSS Flexbox。

```json
{
  "node_type": "container",
  "container_type": "flex",
  "props": {
    "direction": "column",      // row | column
    "justify": "start",         // start | center | end | space-between | space-around
    "align": "stretch",         // start | center | end | stretch
    "gap": "16px",
    "padding": "16px"
  },
  "children": [...]
}
```

### 3.4 Slot 定義

```json
{
  "node_type": "slot",
  "id": "slot_01JHEZ8KXKMJ2PQRS3T4UV5WX0",
  "component": "markdown",
  "meta": {
    "max_words": 500,
    "prompt_hint": "撰寫產品概述，包含主要功能和目標用戶",
    "required": true
  }
}
```

**Meta 欄位說明**：

| 欄位 | 類型 | 說明 |
|------|------|------|
| `max_words` | number | 字數限制 |
| `prompt_hint` | string | 給 Sub-agent 的生成提示 |
| `required` | boolean | 是否為必填 |

### 3.5 可用的 Component 類型

| Component | 說明 | Data 格式 |
|-----------|------|----------|
| `text_h1` | 一級標題 | `string` |
| `text_h2` | 二級標題 | `string` |
| `text_h3` | 三級標題 | `string` |
| `markdown` | 短 Markdown | `string` |
| `markdown_long` | 長 Markdown | `string` |
| `mermaid` | Mermaid 圖表 | `string` (Mermaid DSL) |
| `chart_js` | Chart.js 圖表 | `object` (Chart.js config) |
| `infographic` | 資訊圖表 | `string` (Infographic DSL) |
| `image_url` | 外部圖片 URL | `string` (URL) |
| `image_base64` | Base64 圖片 | `string` (data URI) |
| `table` | 表格 | `object` |
| `code_block` | 程式碼區塊 | `object` |

### 3.6 Layout 設計建議

**1. 12 欄系統**：使用 12 欄 Grid 作為 root，便於分割版面

```json
{
  "root": {
    "node_type": "container",
    "container_type": "grid",
    "props": { "columns": 12, "gap": "24px" },
    "children": [...]
  }
}
```

**2. 常見版面配置**：

- **全寬**：`col_span: 12`
- **兩欄（1:1）**：`col_span: 6` + `col_span: 6`
- **側邊欄 + 主內容**：`col_span: 3` + `col_span: 9`
- **三欄等寬**：`col_span: 4` × 3

**3. 嵌套原則**：

- 第一層（depth 0）：使用 Grid 定義大框架
- 第二層（depth 1）：使用 Flex 處理區塊內部流動
- 第三層（depth 2）：必須是 Slot

---

## 4. Content 填充指南

### 4.1 Content 狀態

```typescript
type ContentStatus = 'pending' | 'processing' | 'filled' | 'failed';
```

| 狀態 | 說明 | data 值 |
|------|------|--------|
| `pending` | 等待處理 | `null` |
| `processing` | 處理中 | `null` |
| `filled` | 已完成 | 實際內容 |
| `failed` | 失敗 | `null`，需有 `error_msg` |

### 4.2 更新 Content

使用 `PATCH /reports/{report_id}` 更新：

```json
{
  "content": {
    "slot_01JHEZ8KXKMJ2PQRS3T4UV5WX0": {
      "status": "filled",
      "data": "實際內容（格式依 component 類型而定）",
      "generated_by": "agt_01JHEZ9ABCMJ2PQRS3T4UV5WX0",
      "generated_at": "2025-01-14T10:32:00Z"
    }
  }
}
```

### 4.3 填充流程

```
1. 開始處理前（可選）：
   status: "processing", data: null

2. 成功完成：
   status: "filled", data: <實際內容>

3. 失敗時：
   status: "failed", data: null, error_msg: "錯誤說明"
```

---

## 5. Component 資料格式詳解

### 5.1 文字類型（text_h1, text_h2, text_h3）

**格式**：純文字字串

```json
{
  "status": "filled",
  "data": "2025 Q1 產品路線圖"
}
```

### 5.2 Markdown（markdown, markdown_long）

**格式**：Markdown 格式字串

```json
{
  "status": "filled",
  "data": "## 產品概述\n\n我們的產品專注於...\n\n### 主要功能\n\n- 功能一\n- 功能二\n- 功能三"
}
```

### 5.3 Mermaid（mermaid）

**格式**：Mermaid DSL 字串

**支援的圖表類型**：
- `flowchart` / `graph` - 流程圖
- `sequenceDiagram` - 序列圖
- `classDiagram` - 類別圖
- `stateDiagram` - 狀態圖
- `gantt` - 甘特圖
- `pie` - 圓餅圖
- `mindmap` - 心智圖
- `timeline` - 時間軸

**範例**：

```json
{
  "status": "filled",
  "data": "flowchart LR\n    A[需求分析] --> B[設計]\n    B --> C[開發]\n    C --> D[測試]\n    D --> E[上線]"
}
```

```json
{
  "status": "filled",
  "data": "pie title 市場佔有率\n    \"產品A\" : 45\n    \"產品B\" : 30\n    \"產品C\" : 25"
}
```

```json
{
  "status": "filled",
  "data": "gantt\n    title 專案時程\n    dateFormat YYYY-MM-DD\n    section 設計\n    UI設計 :a1, 2025-01-01, 30d\n    section 開發\n    前端 :a2, after a1, 45d\n    後端 :a3, after a1, 60d"
}
```

### 5.4 Chart.js（chart_js）

**格式**：Chart.js 配置物件

**必填欄位**：
- `type` - 圖表類型
- `data` - 資料配置

**支援的圖表類型**：`bar`, `line`, `pie`, `doughnut`, `radar`, `polarArea`, `bubble`, `scatter`

**範例 - 長條圖**：

```json
{
  "status": "filled",
  "data": {
    "type": "bar",
    "data": {
      "labels": ["一月", "二月", "三月", "四月"],
      "datasets": [{
        "label": "銷售額",
        "data": [120, 190, 170, 220],
        "backgroundColor": ["#3b82f6", "#10b981", "#f59e0b", "#ef4444"]
      }]
    },
    "options": {
      "responsive": true,
      "plugins": {
        "title": {
          "display": true,
          "text": "月銷售額統計"
        }
      }
    }
  }
}
```

**範例 - 折線圖**：

```json
{
  "status": "filled",
  "data": {
    "type": "line",
    "data": {
      "labels": ["Week 1", "Week 2", "Week 3", "Week 4"],
      "datasets": [{
        "label": "用戶數",
        "data": [100, 150, 180, 250],
        "borderColor": "#3b82f6",
        "tension": 0.1
      }]
    }
  }
}
```

**範例 - 圓餅圖**：

```json
{
  "status": "filled",
  "data": {
    "type": "pie",
    "data": {
      "labels": ["桌面", "行動裝置", "平板"],
      "datasets": [{
        "data": [55, 35, 10],
        "backgroundColor": ["#3b82f6", "#10b981", "#f59e0b"]
      }]
    }
  }
}
```

### 5.5 Infographic（infographic）

**格式**：Infographic DSL 字串（類似 Mermaid 的宣告式語法）

使用 [AntV Infographic](https://infographic.antv.vision/) 引擎，支援約 200 種內建模板。

**基本語法結構**：

```
infographic <template-name>
data
  title 標題文字
  desc 描述文字
  items
    - label 項目名稱
      value 數值
      desc 說明
theme
  palette #color1 #color2 #color3
```

**常用模板類型**：

| 模板分類 | 模板名稱範例 | 用途 |
|---------|------------|------|
| List | `list-row-simple-horizontal-arrow` | 橫向列表 |
| List | `list-col-simple` | 縱向列表 |
| Pyramid | `pyramid` | 金字塔圖 |
| Funnel | `funnel` | 漏斗圖 |
| Cycle | `cycle` | 循環圖 |
| Comparison | `comparison` | 比較圖 |
| Process | `process-arrow` | 流程圖 |
| Proportion | `proportion-donut` | 比例圖 |

**範例 - 漏斗圖**：

```json
{
  "status": "filled",
  "data": "infographic funnel\ndata\n  title 銷售漏斗\n  items\n    - label 訪問\n      value 1000\n    - label 註冊\n      value 500\n    - label 付費\n      value 100\ntheme\n  palette #3b82f6 #10b981 #f59e0b"
}
```

**範例 - 流程圖**：

```json
{
  "status": "filled",
  "data": "infographic process-arrow\ndata\n  title 開發流程\n  items\n    - label 需求\n      desc 收集與分析需求\n    - label 設計\n      desc 系統架構設計\n    - label 開發\n      desc 編碼實作\n    - label 測試\n      desc 品質驗證"
}
```

**範例 - 列表圖**：

```json
{
  "status": "filled",
  "data": "infographic list-col-simple\ndata\n  title 產品特色\n  items\n    - label 快速\n      value 10x\n      desc 比競品快10倍\n    - label 安全\n      value 100%\n      desc 企業級安全性\n    - label 易用\n      value 5min\n      desc 5分鐘上手"
}
```

> 📖 完整模板列表請參考：https://infographic.antv.vision/learn

### 5.6 Table（table）

**格式**：物件，包含 `headers` 和 `rows`

```json
{
  "status": "filled",
  "data": {
    "headers": ["產品", "Q1", "Q2", "Q3", "Q4"],
    "rows": [
      ["產品A", "100", "120", "150", "180"],
      ["產品B", "80", "90", "100", "110"],
      ["產品C", "50", "60", "70", "85"]
    ]
  }
}
```

### 5.7 Code Block（code_block）

**格式**：物件，包含 `language` 和 `code`

```json
{
  "status": "filled",
  "data": {
    "language": "python",
    "code": "def hello_world():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    hello_world()"
  }
}
```

**常見 language 值**：`javascript`, `typescript`, `python`, `java`, `go`, `rust`, `sql`, `bash`, `json`, `yaml`, `markdown`

### 5.8 Image（image_url, image_base64）

**image_url 格式**：有效的 URL 字串

```json
{
  "status": "filled",
  "data": "https://example.com/images/chart.png"
}
```

**image_base64 格式**：Base64 data URI

```json
{
  "status": "filled",
  "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA..."
}
```

---

## 6. 完整範例

### 6.1 建立報告（Manager Agent）

**Step 1: 設計 Layout**

```json
POST /api/v1/reports
Content-Type: application/json

{
  "title": "2025 Q1 產品分析報告",
  "layout": {
    "root": {
      "node_type": "container",
      "container_type": "grid",
      "props": { "columns": 12, "gap": "24px", "padding": "32px" },
      "children": [
        {
          "grid_item": { "col_span": 12 },
          "node": {
            "node_type": "slot",
            "id": "slot_01JHF0TITLE0000000000000",
            "component": "text_h1",
            "meta": { "prompt_hint": "報告主標題" }
          }
        },
        {
          "grid_item": { "col_span": 8 },
          "node": {
            "node_type": "container",
            "container_type": "flex",
            "props": { "direction": "column", "gap": "16px" },
            "children": [
              {
                "node": {
                  "node_type": "slot",
                  "id": "slot_01JHF0SUMMARY000000000001",
                  "component": "markdown",
                  "meta": { "prompt_hint": "執行摘要，200字以內", "max_words": 200 }
                }
              },
              {
                "node": {
                  "node_type": "container",
                  "container_type": "grid",
                  "props": { "columns": 2, "gap": "16px" },
                  "children": [
                    {
                      "node": {
                        "node_type": "slot",
                        "id": "slot_01JHF0CHART10000000000002",
                        "component": "chart_js",
                        "meta": { "prompt_hint": "季度銷售趨勢圖" }
                      }
                    },
                    {
                      "node": {
                        "node_type": "slot",
                        "id": "slot_01JHF0CHART20000000000003",
                        "component": "chart_js",
                        "meta": { "prompt_hint": "產品類別佔比圓餅圖" }
                      }
                    }
                  ]
                }
              }
            ]
          }
        },
        {
          "grid_item": { "col_span": 4 },
          "node": {
            "node_type": "container",
            "container_type": "flex",
            "props": { "direction": "column", "gap": "16px" },
            "children": [
              {
                "node": {
                  "node_type": "slot",
                  "id": "slot_01JHF0FLOW000000000000004",
                  "component": "mermaid",
                  "meta": { "prompt_hint": "產品開發流程圖" }
                }
              },
              {
                "node": {
                  "node_type": "slot",
                  "id": "slot_01JHF0INFO000000000000005",
                  "component": "infographic",
                  "meta": { "prompt_hint": "關鍵指標資訊圖" }
                }
              }
            ]
          }
        },
        {
          "grid_item": { "col_span": 12 },
          "node": {
            "node_type": "slot",
            "id": "slot_01JHF0TABLE00000000000006",
            "component": "table",
            "meta": { "prompt_hint": "各產品季度銷售數據表" }
          }
        }
      ]
    }
  }
}
```

### 6.2 填充內容（Sub-agents）

**Sub-agent A - 填充標題**：

```json
PATCH /api/v1/reports/rpt_01JHF0RPT0000000000000000
Content-Type: application/merge-patch+json

{
  "content": {
    "slot_01JHF0TITLE0000000000000": {
      "status": "filled",
      "data": "2025 Q1 產品分析報告",
      "generated_by": "agt_01JHF0AGT0000000000000001",
      "generated_at": "2025-01-14T10:30:00Z"
    }
  }
}
```

**Sub-agent B - 填充圖表**：

```json
PATCH /api/v1/reports/rpt_01JHF0RPT0000000000000000
Content-Type: application/merge-patch+json

{
  "content": {
    "slot_01JHF0CHART10000000000002": {
      "status": "filled",
      "data": {
        "type": "line",
        "data": {
          "labels": ["1月", "2月", "3月"],
          "datasets": [{
            "label": "銷售額（萬）",
            "data": [120, 150, 180],
            "borderColor": "#3b82f6",
            "tension": 0.1
          }]
        },
        "options": {
          "responsive": true,
          "plugins": {
            "title": { "display": true, "text": "Q1 銷售趨勢" }
          }
        }
      },
      "generated_by": "agt_01JHF0AGT0000000000000002",
      "generated_at": "2025-01-14T10:31:00Z"
    }
  }
}
```

**Sub-agent C - 填充 Mermaid 流程圖**：

```json
PATCH /api/v1/reports/rpt_01JHF0RPT0000000000000000
Content-Type: application/merge-patch+json

{
  "content": {
    "slot_01JHF0FLOW000000000000004": {
      "status": "filled",
      "data": "flowchart TD\n    A[需求收集] --> B[產品設計]\n    B --> C[開發實作]\n    C --> D[測試驗證]\n    D --> E[上線部署]\n    E --> F[監控優化]",
      "generated_by": "agt_01JHF0AGT0000000000000003",
      "generated_at": "2025-01-14T10:32:00Z"
    }
  }
}
```

**Sub-agent D - 填充 Infographic**：

```json
PATCH /api/v1/reports/rpt_01JHF0RPT0000000000000000
Content-Type: application/merge-patch+json

{
  "content": {
    "slot_01JHF0INFO000000000000005": {
      "status": "filled",
      "data": "infographic list-col-simple\ndata\n  title 關鍵指標\n  items\n    - label 營收成長\n      value +25%\n      desc 較去年同期\n    - label 用戶數\n      value 10K+\n      desc 活躍用戶\n    - label 滿意度\n      value 4.8\n      desc 平均評分",
      "generated_by": "agt_01JHF0AGT0000000000000004",
      "generated_at": "2025-01-14T10:33:00Z"
    }
  }
}
```

---

## 7. 常見錯誤與排除

### 7.1 Layout 驗證錯誤

| 錯誤碼 | 說明 | 解決方案 |
|--------|------|---------|
| `MAX_DEPTH_EXCEEDED` | Layout 深度超過 2 層 | 確保 depth 2 必須是 Slot |
| `DUPLICATE_SLOT_ID` | Slot ID 重複 | 每個 Slot 使用唯一的 ULID |
| `INVALID_SLOT_ID` | Slot ID 格式錯誤 | 使用 `slot_{ulid}` 格式 |

### 7.2 Content 驗證錯誤

| 錯誤碼 | 說明 | 解決方案 |
|--------|------|---------|
| `CONTENT_TYPE_MISMATCH` | 資料格式與 component 不符 | 檢查 data 格式是否正確 |
| `INVALID_SLOT_ID` | Slot ID 不存在於 Layout | 確認 slot_id 存在於 Layout 中 |
| `MISSING_DATA` | `filled` 狀態但無 data | 確保 status 為 filled 時有 data |
| `MISSING_ERROR_MSG` | `failed` 狀態但無 error_msg | 失敗時必須提供 error_msg |

### 7.3 常見 Data 格式錯誤

**chart_js 缺少必要欄位**：
```json
// ❌ 錯誤
{ "data": { "labels": [...], "datasets": [...] } }

// ✅ 正確 - 必須有 type
{ "type": "bar", "data": { "labels": [...], "datasets": [...] } }
```

**infographic 格式錯誤**：
```json
// ❌ 錯誤 - 不是字串
{ "template": "funnel", "data": [...] }

// ✅ 正確 - 必須是 DSL 字串
"infographic funnel\ndata\n  title 標題\n  items\n    - label 項目\n      value 100"
```

**table 缺少 headers 或 rows**：
```json
// ❌ 錯誤
{ "data": [["A", "B"], ["C", "D"]] }

// ✅ 正確
{ "headers": ["Col1", "Col2"], "rows": [["A", "B"], ["C", "D"]] }
```

---

## 附錄：快速參考

### A. Component 資料格式速查表

| Component | Type | 必要欄位 | 範例 |
|-----------|------|---------|------|
| `text_h1/h2/h3` | string | - | `"標題文字"` |
| `markdown` | string | - | `"## 標題\n\n內容"` |
| `mermaid` | string | - | `"flowchart LR\n  A-->B"` |
| `chart_js` | object | `type`, `data` | `{"type":"bar","data":{...}}` |
| `infographic` | string | 開頭為 `infographic ` | `"infographic funnel\ndata\n..."` |
| `table` | object | `headers`, `rows` | `{"headers":[...],"rows":[...]}` |
| `code_block` | object | `language`, `code` | `{"language":"js","code":"..."}` |
| `image_url` | string | 有效 URL | `"https://..."` |
| `image_base64` | string | data URI | `"data:image/png;base64,..."` |

### B. 常用 Layout 模式

**全寬標題 + 兩欄內容**：
```
Grid(12) → [Slot(12), Slot(6), Slot(6)]
```

**側邊欄 + 主內容**：
```
Grid(12) → [Flex(3) → [...], Flex(9) → [...]]
```

**儀表板卡片**：
```
Grid(12) → [Slot(4), Slot(4), Slot(4), Slot(6), Slot(6)]
```
