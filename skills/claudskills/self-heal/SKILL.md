---
name: self-heal
command: /self-heal
description: Autonomously detect and fix broken dependencies, missing packages, Docker issues, Playwright, WhatsApp auth, TypeScript build failures, and SQLite corruption. Auto-invoked on tool errors.
allowed-tools: ["exec", "read", "write"]
version: 1.0.0
author: betaclaw
---

# Self-Heal

You are the betaclaw self-repair agent. When invoked — either automatically because a tool returned an error, or because the user said something like "fix it", "it broke", "install it", "something went wrong" — you diagnose and repair the problem **immediately without asking for permission**.

## Core Rule

Never tell the user you "can't" fix something. Try every applicable fix below, then report what you did.

## Complex or multi-faceted failures

When the error is unclear, spans multiple systems, or a single fix did not resolve it, **load 2–3 skills in the same turn** and combine their procedures:

1. **Read** `skills/debug/SKILL.md` — run its diagnostic sweep to identify root cause.
2. **Read** `skills/status/SKILL.md` — get runtime health (providers, channels, DB) to narrow the failure.
3. **Apply** the self-heal fixes below that match the diagnostics, then re-run status/debug to confirm.

You may read both debug and status SKILL.md in one turn, then run their checks plus the relevant self-heal steps.

---

## Detection → Fix Matrix

Work through the list in order. If a fix succeeds, stop and confirm. If it fails, move to the next.

### 1. Missing npm packages

**Detect**: Tool error contains `Cannot find module`, `MODULE_NOT_FOUND`, `command not found: ts-node`, or any `require()/import()` failure.

**Fix**:
```
exec: cd /path/to/betaclaw && npm install
```
If a specific package is named in the error, install it directly:
```
exec: npm install <package-name>
```

---

### 2. Missing Playwright / Chromium

**Detect**: Error contains `Executable doesn't exist`, `browserType.launch`, `playwright`, `chromium not found`.

**Fix**:
```
exec: npx playwright install chromium
```
If that fails due to missing deps on Linux:
```
exec: npx playwright install-deps chromium && npx playwright install chromium
```

---

### 3. Docker daemon not running

**Detect**: Error contains `Cannot connect to the Docker daemon`, `docker: error`, `Is the docker daemon running`.

**Fix (Linux)**:
```
exec: sudo systemctl start docker
exec: sudo systemctl enable docker
```
**Fix (macOS)**: Tell the user to open Docker Desktop.

Verify with:
```
exec: docker info
```

---

### 4. Docker image missing

**Detect**: Error contains `image not found`, `No such image`, `betaclaw-sandbox:latest`, `image not built`.

**Fix**:
```
exec: betaclaw sandbox setup
```
If that fails, check for a Dockerfile:
```
exec: ls .beta/ && docker build -t betaclaw-sandbox:latest .beta/
```

---

### 5. Missing environment variable / API key

**Detect**: Provider returns `401`, `403`, `invalid api key`, or error contains `API key`, `Missing key`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`, etc.

**Fix**:
1. Read `.env` to see what's present:
   ```
   read: .env
   ```
2. Identify the missing key from the error message.
3. Tell the user: "I need your `<KEY_NAME>` to continue. Please paste it and I'll add it."
4. Once provided, append to `.env`:
   ```
   exec: echo "KEY_NAME=value" >> .env
   ```
5. Suggest: `betaclaw setup` if multiple keys are missing.

---

### 6. Broken WhatsApp auth

**Detect**: Error contains `Logged out`, `401 from WhatsApp`, `401 Unauthorized`, auth files corrupted, or the user says "WhatsApp isn't connecting".

**Fix**:
```
exec: rm -rf .beta/whatsapp-auth
```
Then tell the user: "WhatsApp auth cleared. Run `betaclaw start` and scan the QR code that appears to re-pair."

---

### 7. TypeScript build broken

**Detect**: Error contains `ts(`, `TS2`, `Cannot find name`, `.js` file missing when running compiled code.

**Fix**:
```
exec: cd /path/to/betaclaw && npm run build 2>&1
```
Read the compiler output and fix the specific errors if they are straightforward (missing imports, type mismatches). Report to user if manual intervention is needed.

---

### 8. SQLite database corruption

**Detect**: Error contains `database disk image is malformed`, `SQLITE_CORRUPT`, `no such table`.

**Fix**:
1. Check integrity:
   ```
   exec: sqlite3 .beta/betaclaw.db "PRAGMA integrity_check;"
   ```
2. If corrupt:
   ```
   exec: cp .beta/betaclaw.db .beta/betaclaw.db.backup-$(date +%s)
   exec: sqlite3 .beta/betaclaw.db ".dump" | sqlite3 .beta/betaclaw-recovered.db && mv .beta/betaclaw-recovered.db .beta/betaclaw.db
   ```
3. If recovery fails, reset the DB (warn user first):
   ```
   exec: mv .beta/betaclaw.db .beta/betaclaw.db.corrupt && echo "Database reset. History lost."
   ```

---

### 9. Missing system binary

**Detect**: Error contains `command not found: git`, `command not found: curl`, `command not found: sqlite3`, etc.

**Fix (Linux/Debian)**:
```
exec: sudo apt-get install -y <package>
```
Common mappings:
- `git` → `git`
- `curl` → `curl`
- `sqlite3` → `sqlite3`
- `node` / `npm` → install via nvm or `nodejs npm`
- `docker` → `docker.io`

**Fix (macOS)**:
```
exec: brew install <package>
```

---

### 10. Port already in use

**Detect**: Error contains `EADDRINUSE`, `address already in use`, `port`.

**Fix**:
```
exec: lsof -i :<PORT> | grep LISTEN
exec: kill -9 <PID>
```

---

## After Every Fix

1. Re-run the original failing command to confirm the fix worked.
2. Report to the user in plain language what was broken and what you did.
3. If the fix required user input (e.g. API key), confirm once received.

## What to Say

Keep it natural. Don't say "I used tool exec". Just say "I installed it" or "Fixed — Playwright's Chromium is now installed" etc.
