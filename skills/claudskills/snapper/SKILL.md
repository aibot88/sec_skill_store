---
name: snapper
description: >
  CDP browser screenshots for capturing authenticated web pages.
  Use when you need pixel-perfect PNG screenshots of authenticated sites like Google Sheets, dashboards, or admin panels.
allowed-tools: "Bash(guppi-snapper:*)"
version: "0.1.2"
author: "Sam Dengler"
license: "MIT"
---

# Snapper — CDP browser screenshot tool

Captures pixel-perfect PNG screenshots of authenticated web pages using Playwright's bundled Chromium with CDP (Chrome DevTools Protocol). Launches a persistent Chromium instance with named profiles so logins survive across sessions.

## Commands

### `guppi-snapper init`

Set up snapper: install Playwright's bundled Chromium and create the directory structure (profiles, extensions). Run once after installing snapper.

### `guppi-snapper start [--profile NAME] [--port PORT]`

Launch Chromium with CDP enabled using a named profile.

**Options:**
- `--profile` / `-p` — profile name (default: `default`)
- `--port` — CDP port (default: `9222`)

### `guppi-snapper status [--port PORT]`

Check if Chromium is running with CDP and show connection info.

**Options:**
- `--port` — CDP port to check (default: `9222`)

### `guppi-snapper stop`

Gracefully shut down the CDP Chromium instance.

### `guppi-snapper capture URL [--output FILE] [--viewport WxH] [--resize WxH] [--wait SECONDS] [--existing] [--port PORT]`

Navigate to a URL and capture a screenshot.

**Arguments:**
- `url` — the URL to capture (or URL pattern with `--existing`)

**Options:**
- `--output` / `-o` — output file path (default: `screenshot.png`)
- `--viewport` / `-v` — viewport dimensions (default: `1400x1365`)
- `--resize` / `-r` — resize to WxH after capture (requires ImageMagick)
- `--wait` / `-w` — seconds to wait after load (default: `5`)
- `--existing` / `-e` — capture an already-open tab matching URL pattern instead of navigating. Preserves cell selection, scroll position, and UI state.
- `--port` — CDP port (default: `9222`)

### `guppi-snapper batch CONFIG_FILE`

Capture multiple screenshots from a YAML config file.

**Arguments:**
- `config_file` — path to YAML config

### `guppi-snapper profile list`

List available profiles with name, last modified, and size.

### `guppi-snapper profile create NAME`

Create a new empty profile directory.

### `guppi-snapper profile delete NAME [--yes]`

Delete a profile directory (with confirmation).

## Examples

```bash
# First-time setup
guppi-snapper init

# Start Chromium with default profile
guppi-snapper start

# Navigate to URL and capture
guppi-snapper capture https://docs.google.com/spreadsheets/d/ID/edit \
  --output sheet.png --viewport 1400x1365 --resize 1120x1092 --wait 8

# Capture existing tab (preserves cell selection state)
guppi-snapper capture spreadsheets \
  --existing --output selected.png --viewport 1400x1365 --resize 1120x1092 --wait 3

# Batch capture from config
guppi-snapper batch screenshots.yaml

# Manage profiles
guppi-snapper profile list
guppi-snapper profile create myproject
```

## Skill Management

```bash
guppi-snapper skill install   # Register with guppi-cli
guppi-snapper skill show      # Display SKILL.md contents
```
