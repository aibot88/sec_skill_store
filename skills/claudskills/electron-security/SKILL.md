---
name: electron-security
description: Use when working on Electron applications — detected by `electron` in package.json dependencies, presence of `main.ts`/`main.js` entry, or `BrowserWindow` usage in source. Enforces contextIsolation true, nodeIntegration false, CSP, and draggable region discipline. Do NOT use for regular web apps, Node.js CLI tools, or non-Electron desktop frameworks (Tauri, Neutralino, NW.js).
allowed-tools: Read, Edit, Grep, Glob
---

# Electron Security Baseline

Minimální bezpečná konfigurace Electron aplikace. Každý bod je hard rule — ne doporučení.

## Povinné v `BrowserWindow` konfiguraci

- `contextIsolation: true`
- `nodeIntegration: false`
- `sandbox: true` (pokud aplikace nepotřebuje výjimku)
- `webSecurity: true` (default, neměň)
- `preload: path.join(__dirname, 'preload.js')` — API exposuj **jen** přes `contextBridge.exposeInMainWorld`

Detailní minimální příklad: `references/baseline-config.md`.

## CSP (Content Security Policy)

- Vždy nastav `<meta http-equiv="Content-Security-Policy" …>` v renderer HTML **nebo** header přes `session.defaultSession.webRequest.onHeadersReceived`.
- **Zakázáno**: `unsafe-inline`, `unsafe-eval`, `*` v `script-src`.
- Pro dev server (Vite/webpack) povol `'self' ws:` pro HMR — jen v dev buildu, ne v produkci.

Patterny: `references/csp.md`.

## Draggable regions

- `-webkit-app-region: drag` **pouze** na titlebar containers (prázdné oblasti).
- Interaktivní prvky (buttons, inputs, links) uvnitř drag oblasti musí mít `-webkit-app-region: no-drag`.
- Viz pravidlo E041 v `skills/visual-audit/rules/electron.yaml`.

## IPC

- Preload whitelistuje konkrétní kanály — nikdy `ipcRenderer.invoke` free-form z rendereru.
- Main process validuje sender: `if (!event.senderFrame.url.startsWith(trustedPrefix)) return`.

## Když narazíš na porušení

Nefixuj mlčky — vždy uprav kód **a** řekni uživateli konkrétně co bylo špatně a proč (např. „`nodeIntegration: true` v `src/main.ts:42` — rewrite-vulnerability, všechen renderer JS by měl root přístup k Node.js").
