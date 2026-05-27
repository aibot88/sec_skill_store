---
name: agnt-audit-a11y
description: "\"Run comprehensive accessibility audit on current page. 全面審現頁無障礙性. Use when: audit accessibility, check WCAG compliance, find a11y issues, test screen reader support, review ARIA labels\""
allowed-tools: "[\"mcp__agnt__proxy\", \"mcp__agnt__proxylog\"]"
context: fork
agent: "agnt:browser-debugger"
---

<!-- CC 2.1 fork decision: workflow driver (axe-core run + ARIA + contrast + tab-order + screen-reader simulation = many tool calls). Fork keeps parent loop free of audit detail. Executor: agnt:browser-debugger (preloads accessibility-audit via skills array). -->


藉agnt診斷工具對當前瀏覽器頁面執行完整無障礙稽核。

## 步驟

1. 執行完整無障礙稽核：
   ```
   proxy {action: "exec", id: "dev", code: "__devtool.auditAccessibility()"}
   ```

2. 取Tab鍵順序以查鍵盤導航：
   ```
   proxy {action: "exec", id: "dev", code: "__devtool.getTabOrder()"}
   ```

3. 截圖供參考：
   ```
   proxy {action: "exec", id: "dev", code: "__devtool.screenshot('a11y-audit')"}
   ```

## 稽核檢查內容

### 嚴重問題（錯誤）
- **無alt文字之圖片** — 螢幕閱讀器無法描述圖片
- **無標籤之表單輸入** — 用戶不知輸入什麼
- **無無障礙名稱之按鈕** — 用戶不知按鈕作用
- **空連結** — 無文字內容或aria-label之連結

### 警告
- **無href之連結** — 可能引起導航問題

## 解讀結果

稽核回傳：
- `issues`：找到之無障礙問題陣列
- `count`：問題總數
- `errors`：嚴重問題數
- `warnings`：非嚴重問題數

每個問題含：
- `type`：無障礙違規類型
- `severity`："error" 或 "warning"
- `selector`：定位元素之CSS選擇器
- `message`：問題描述

## 附加診斷工具

更深入無障礙分析：

```
// Get detailed accessibility info for a specific element
proxy {action: "exec", id: "dev", code: "__devtool.getA11yInfo('#element')"}

// Check color contrast between foreground and background
proxy {action: "exec", id: "dev", code: "__devtool.getContrast('rgb(0,0,0)', 'rgb(255,255,255)')"}

// Get what a screen reader would announce for an element
proxy {action: "exec", id: "dev", code: "__devtool.getScreenReaderText('#element')"}
```

## WCAG指南參考

- **4.5:1** — 一般文字所需對比度（AA）
- **3:1** — 大文字所需對比度（AA）
- **7:1** — 增強對比度所需（AAA）
