---
name: canv-extension-author
description: Use when the user asks you to build, edit, or debug a Canv extension. Triggers on "build me a Canv extension", "build me a Canv panel", "build me a fileHandler for X", "add a Canv extension that …", "write an extension for Canv that …", or any explicit request to add UI or functionality to Canv via its extension system. Provides the manifest schema, all six contribution types, runtime constraints, CSP rules, and working recipes.
---

# Canv extension author

You are building an extension for **Canv** — a desktop writing app (Electron + React + TypeScript). Extensions extend Canv's UI via six contribution types: `panel`, `fileHandler`, `command`, `menu`, `statusBar`, `language`. An extension is a directory with `manifest.json` plus entry files; users install via Extensions tab → "Install from folder…".

## When to activate

Activate for:
- Creating a new Canv extension from scratch
- Editing an existing extension in the user's workspace
- Debugging an installed Canv extension

Do **not** activate for unrelated Canv tasks (writing markdown, configuring profiles, switching themes, etc.).

## Workflow

1. **Pick contribution type(s).** Read `contributions/<type>.md` for each type you'll use.
2. **Read `reference/conventions.md` once.** It covers manifest fields, capability declarations, visual rules, and the pre-emit checklist — applies to every extension.
3. **Scaffold the directory.** Default location: `<workspace>/canv-extensions/<extension-id>/`. Confirm with the user if not obvious.
4. **Write `manifest.json` + entry files.** Use `reference/manifest-schema.md` for field-level details.
5. **Third-party libraries** — if the extension needs an npm package:
   - Bundle with esbuild into `vendor/<name>.js` (self-contained ESM):
     ```bash
     npm install <pkg>
     npx esbuild --bundle --format=esm --platform=browser \
       --outfile=vendor/<name>.js node_modules/<pkg>/<entry>
     ```
   - Reference from HTML as `<script type="module" src="./vendor/<name>.js"></script>`.
   - Check `recipes/` first — known-good setups for pdf.js, chart.js, etc. are already there.
6. **Tell the user to install:** Extensions tab → "Install from folder…" → pick the extension dir → trust when prompted → enable.

## Hard constraints

| Rule | Detail |
|------|--------|
| CSP | `script-src 'self' canv-extension://canv-shared`. No CDN scripts. No inline `<script>`. No `onclick="..."`. No `eval`. All JS in separate `.js` files; wire events with `addEventListener`. |
| Capabilities | Every `canv.*` call needs its capability in `manifest.capabilities`. See `reference/canv-api.md` for the mapping. Missing capability = silent runtime failure. |
| Panel location | `"left-sidebar"` or `"bottom-dock"` only. `"right-sidebar"` is rejected. |
| CSS tokens | Use `--canv-*` design tokens from the auto-injected `canv-ui.css`. Never hard-code hex / rgb / system fonts. |
| Icons | `<canv-icon name="...">` only. Never `<img>` or emoji in UI chrome. |
| fileHandler read | `activeDoc.read` is required even for `mode: "viewer"`. |
| Vendor libs | Must live in `vendor/<name>.js`, bundled self-contained. No CDN imports. |

## Testing loop

After scaffolding:
1. Tell the user: open Canv → Extensions tab → Install from folder → pick the dir → trust workspace + extension → enable.
2. **Manifest validation errors** appear in the install consent modal. User reports; you regenerate.
3. **Runtime errors** appear in the extension DevTools (right-click inside the panel → Inspect Extension). User pastes; you iterate.
4. **After any file change:** uninstall + reinstall — Canv copies files at install time; changes are not picked up live.

## Pre-emit checklist

Before reporting done:

- [ ] **ID fields match their regex.** `manifest.id`, `panel.id`, `fileHandler.id`, `statusBar.id` are kebab-case (`/^[a-z][a-z0-9-]{0,63}$/` — lowercase, hyphens OK). `command.id` is dotted-lowercase with NO hyphens (`/^[a-z][a-z0-9]*(?:\.[a-z][a-z0-9]*)*$/` — e.g. `"format.selection"`, NOT `"format-selection"`). See `reference/conventions.md`.
- [ ] Every `canv.*` call has its capability declared in `manifest.capabilities`.
- [ ] Every `contribution.entry` path is a real file in the extension dir.
- [ ] No inline `<script>` or `onclick` attributes — all JS is in external `.js` files.
- [ ] CSS uses only `--canv-*` variables.
- [ ] No emoji in UI chrome (toolbar labels, headings, buttons).
- [ ] `panel.location` is `"left-sidebar"` or `"bottom-dock"`.
- [ ] Third-party libraries are in `vendor/<name>.js`, bundled self-contained.

## Reference index

| File | Purpose |
|------|---------|
| `contributions/panel.md` | Panel contribution — activity-bar tab, iframe lifecycle |
| `contributions/fileHandler.md` | File viewer/editor — byte-level read/write API |
| `contributions/command.md` | Command palette + keybindings |
| `contributions/menu.md` | File-tree context menu items |
| `contributions/statusBar.md` | Status-bar items |
| `contributions/language.md` | CodeMirror language contributions (red trust prompt — read this) |
| `reference/conventions.md` | Manifest fields summary, visual rules, capability mapping |
| `reference/manifest-schema.md` | Full Zod schema including settings + activationEvents |
| `reference/canv-api.md` | Full `canv.*` API surface with capability mapping |
| `reference/csp-and-protocol.md` | CSP details + canv-extension:// protocol |
| `reference/debugging.md` | DevTools, reload, common errors |
| `recipes/` | Working examples: PDF viewer, chart panel, markdown render, word-count status bar |
