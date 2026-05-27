---
name: lci-agnt-companion
description: "Use when lci is installed and user needs dev server, reverse proxy, browser debugging, screenshots, or accessibility/performance/security audits of running page - points at sibling agnt plugin which lci does not duplicate. lci搜索代碼；運行代碼、觀其所為則用agnt。 Use when: dev server, browser errors, screenshots, a11y/perf/security audit, live DOM interaction."
---

# agnt — the browser and process companion to lci

lci提供亞毫秒代碼搜索及符號智能。**運行代碼並觀察結果**——開發服務器、反向代理、瀏覽器調試、截圖、控制台錯誤、a11y/perf/安全審計——用同一市場的兄弟插件**agnt**。

## When to reach for agnt instead of lci

- "Start the dev server and proxy it so I can see browser errors" → agnt `dev-proxy`
- "Take a screenshot of the current page" → agnt `screenshot`
- "Are there JavaScript errors in the browser right now?" → agnt `check-errors` / `error-monitor`
- "Run an accessibility / performance / SEO / security audit" → agnt `audit-a11y`, `audit-performance`, `audit-seo`, `audit-security`
- "Wireframe this page" → agnt `sketch-mode`
- "Debug this UI interaction" → agnt `browser-debug`
- 任何需要實時渲染DOM而非源碼之事

## Install

agnt與lci同在`standardbeagle-tools`市場：

```
claude mcp add agnt --source ./plugins/agnt
```

或從市場與lci並肩安裝。二插件設計共存——無重疊鉤子，無MCP服務器衝突。

## Typical split in a session

| task | plugin |
|---|---|
| Find where a React component is defined | **lci** |
| Start dev server, reverse proxy, watch browser errors | **agnt** |
| Trace what calls `processPayment()` across the repo | **lci** |
| Screenshot + a11y audit of the rendered page | **agnt** |
| `explore-codebase` before implementing a feature | **lci** |
| `qa-test` / `audit-security` on the running app | **agnt** |

使用lci時若需*運行*代碼並觀察結果，即為引入agnt之信號。
