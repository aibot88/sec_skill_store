---
name: macos-fda-grant-helper
description: Interactive helper for granting macOS Full Disk Access (FDA) to a launchd-spawned binary. TRIGGERS - full disk access, fda grant, TCC permission, "Maccy DB unreadable", "operation not permitted" on sandbox-protected paths, launchd binary needs file access
---

# macOS Full Disk Access Grant Walkthrough

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

> **What this skill is for**: when a launchd-spawned binary (or any non-interactive process) needs to read sandbox-protected paths like `~/Library/Containers/<app>/Data/...`, macOS TCC will deny the access until that specific binary is added to the **Full Disk Access** allowlist in System Settings → Privacy & Security → Full Disk Access. We cannot grant this programmatically — Apple's design — but we can automate everything **up to** the manual click.

## Why this exists

Discovered iter 21 (2026-05-19) after the iter-20 fleet heartbeat finally surfaced a **32-day-old chronic failure** in `com.terryli.maccy-backup`. The launchd job had been failing daily with `"Maccy DB unreadable"` since 2026-04-17. Root cause: the spawn binary `~/eon/iterm2-scripts/bin/maccy-backup/maccy-backup-runner` was not in the FDA allowlist. Interactive shells (iTerm2, Warp, Terminal, mise binaries) all WERE — that's why running the script manually from a terminal succeeds, hiding the problem from casual debugging.

Without this helper, the click-path is buried four levels deep in System Settings, and the absolute binary path has to be typed by hand. The helper makes it a 30-second manual operation instead of "10 minutes of fumbling, abandoned, fails for another week."

## How it works

`fda-grant-walkthrough` performs four steps:

1. **Resolves** the binary path to its absolute canonical form (System Settings stores absolute paths)
2. **Checks** the current TCC database for an existing grant (fast-exits if already granted)
3. **Copies** the absolute path to the macOS clipboard via `pbcopy`
4. **Opens** System Settings directly to the FDA pane via `x-apple.systempreferences://...`

The user then clicks **+** → Cmd+Shift+G → Cmd+V → Enter → select binary → toggle ON → authenticate.

After the grant, `--check` mode confirms the new state without opening any UI.

## Usage

```bash
# Full walkthrough — opens UI, copies path
fda-grant-walkthrough ~/eon/iterm2-scripts/bin/maccy-backup/maccy-backup-runner

# Check-only — useful in scripts / CI / heartbeat-class probes
if fda-grant-walkthrough --check /path/to/binary; then
    echo "FDA already granted — proceed"
else
    echo "FDA needed — see exit code 3"
fi
```

### Exit codes

| Exit | Meaning                                                                     |
| ---- | --------------------------------------------------------------------------- |
| 0    | Binary already has FDA (or walkthrough launched successfully)               |
| 1    | Usage error (no path given, etc.)                                           |
| 2    | Binary does not exist or is not executable                                  |
| 3    | (--check only) Binary does NOT have FDA, OR caller lacks FDA to read TCC.db |

## Install

```bash
ln -sf "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/devops-tools/skills/macos-fda-grant-helper/scripts/fda-grant-walkthrough.sh" ~/.local/bin/fda-grant-walkthrough
```

## Worked example — fixing the chronic maccy-backup failure

```bash
# 1. Run the walkthrough (System Settings opens; path on clipboard)
fda-grant-walkthrough ~/eon/iterm2-scripts/bin/maccy-backup/maccy-backup-runner

# 2. In Settings: + → Cmd+Shift+G → Cmd+V → Enter → toggle ON → Touch ID

# 3. Verify the grant landed
fda-grant-walkthrough --check ~/eon/iterm2-scripts/bin/maccy-backup/maccy-backup-runner

# 4. Restart the failing launchd job and watch for green
launchctl kickstart -p gui/$(id -u)/com.terryli.maccy-backup
tail -f ~/.local/state/maccy-backup/logs/backup-$(date +%Y%m%d).log

# 5. Tomorrow morning, fleet heartbeat (iter 20) should drop from WARN to INFO
#    because failed_services no longer includes com.terryli.maccy-backup=1
```

## Why we can't fully automate the grant

macOS TCC enforces a human-authenticated boundary on FDA changes. There's no public API for `tccutil` to ADD entries — only RESET them. Even MDM (Mobile Device Management) profiles can pre-authorize FDA only for system-distributed apps, not for arbitrary user-compiled binaries. The walkthrough is therefore the optimum: 95% automated (path resolution, clipboard, UI navigation), 5% manual (the click + Touch ID).

## When to use this skill

- A launchd job is failing with "Operation not permitted" or "DB unreadable" or "permission denied" on paths under `~/Library/Containers/`
- A compiled Swift/Go binary needs to read app-private files (Maccy clipboard DB, Messages chat DB, Mail mbox, etc.)
- You want a scripted way to check whether a given binary has FDA without opening any UI (use `--check`)

## Related

- iter-20 fleet daily heartbeat — surfaced maccy-backup as the test case for this helper
- macOS Privacy & Security framework: [Apple docs](https://support.apple.com/guide/mac-help/control-access-to-files-and-folders-on-mac-mchld5a35146/mac)
- TCC database schema: <https://rainforest.engineering/2021-02-09-macos-tcc/>

## Post-Execution Reflection

After granting FDA via this helper, check:

1. **Did `--check` confirm the grant?** — Run after toggling ON; if it still returns exit 3, the toggle may not have stuck (try toggling OFF/ON again with auth).
2. **Did the dependent launchd job recover?** — Kickstart the job and verify the next log line shows the protected path was read successfully.
3. **Does the fleet heartbeat reflect the fix the next morning?** — The iter-20 heartbeat reports failed services; a successful FDA grant should drop the entry within a day.
