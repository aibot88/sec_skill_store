---
name: scitex-browser
description: Playwright wrappers for scientific web scraping + AI-agent browsing — adds debugging visuals (cursor/click overlays, step markers, grid), popup/cookie handling, PDF capture (including the notoriously-hidden Chrome PDF viewer), resilient click/fill with selector fallbacks, test-monitor fixtures, and browser-session management. Public API (~36 symbols) — sessions (`SyncBrowserSession`, `sync_browser_session`, `create_browser_session_fixture`), PDF capture (`save_as_pdf`, `save_as_pdf_async`, `detect_chrome_pdf_viewer_async`, `click_download_for_chrome_pdf_viewer_async`), resilient interaction (`click_with_fallbacks_async`, `fill_with_fallbacks_async`, `click_center_async`), popup handling (`PopupHandler`, `close_popups_async`, `ensure_no_popups_async`), debugging visuals (`show_cursor_at[_async]`, `show_click_effect[_async]`, `show_step[_async]`, `show_grid_async`, `show_test_result[_async]`, `highlight_element_async`, `inject_visual_effects[_async]`), console logging (`browser_logger`, `collect_console_logs`, `collect_console_logs_detailed`, `format_logs_devtools_style`, `setup_console_interceptor`), test monitoring (`TestMonitor`, `monitor_test`, `create_test_monitor_fixture`, `create_failure_capture_fixture`, `save_failure_artifacts`), environment (`is_playwright_cli_available`). Also supports OAuth/stealth/ZenRows remote-CAPTCHA backends. No CLI, no MCP tools (parent `scitex` umbrella exposes `browser_save_as_pdf` + `capture_screenshot`). Drop-in replacement for raw `playwright.sync_api` / `playwright.async_api` scripts, `selenium` + stealth plugins, hand-rolled popup-close loops, custom Chrome PDF-viewer hacks (`chrome://flags` workarounds), and bespoke `pytest-playwright` fixtures. Use whenever the user asks to "save a webpage as PDF", "download from Chrome's PDF viewer", "click this element with fallback selectors", "handle GDPR/cookie popups", "add cursor/click overlays for debug video", "collect browser console logs DevTools-style", "wrap a test with a browser-session fixture", "set up failure-artifact capture", or mentions `scitex.browser`, Playwright for scientific scraping, AI-agent browser automation.
primary_interface: python
interfaces:
  python: 3
  cli: 0
  mcp: 0
  skills: 2
  hook: 0
  http: 0
---

# scitex-browser

> **Interfaces:** Python ⭐⭐⭐ (primary) · CLI — · MCP — · Skills ⭐⭐ · Hook — · HTTP —

Thin, categorized wrappers around Playwright. Grouped into sub-packages;
each one is a flat import surface re-exported from the top-level
`scitex_browser` namespace.

## Installation & import (two equivalent paths)

The same module is reachable via two install paths. Both forms work at
runtime; which one a user has depends on their install choice.

```python
# Standalone — pip install scitex-browser
import scitex_browser
scitex_browser.save_as_pdf(...)

# Umbrella — pip install scitex
import scitex.browser
scitex.browser.save_as_pdf(...)
```

`pip install scitex-browser` alone does NOT expose the `scitex` namespace;
`import scitex.browser` raises `ModuleNotFoundError`. To use the
`scitex.browser` form, also `pip install scitex`.

See [../../general/02_interface-python-api.md] for the ecosystem-wide
rule and empirical verification table.

## Sub-skills

### Core

* [01_quick-start](01_quick-start.md) — Minimal save-as-pdf / session / visuals
* [02_python-api](02_python-api.md) — Public symbols grouped by sub-package
* [03_session-lifecycle](03_session-lifecycle.md) — Sync/shared sessions, fixtures

### Sub-packages

* [04_debugging-visuals](04_debugging-visuals.md) — Cursor/click/step overlays, console logs
* [05_pdf-capture](05_pdf-capture.md) — `save_as_pdf`, Chrome PDF viewer
* [06_interaction](06_interaction.md) — Resilient click/fill, popup handling
* [07_auth-stealth-remote](07_auth-stealth-remote.md) — OAuth, stealth, ZenRows, CAPTCHA
