---
name: context-checkpoint
description: "Save, compress, version, encrypt, and resume full chat context when approaching token/message limits. Use when the conversation is long, the user says save our progress or context is running out, approaching token limits, resuming a session across chat windows or different AI models, creating named bookmarks, merging parallel chats, or exporting conversation history as knowledge assets. Supports commands like /save, /resume, /resume light, /bookmark, /list bookmarks, /recover_last, /merge, /diff, /export."
metadata:
  author: Himanshu
  version: '2.0'
---

# Context Checkpoint Skill

## When to Use This Skill

Trigger this skill when any of the following are true:

- User says: "save context", "we're running out of tokens", "checkpoint this", "save progress", "I want to continue in a new window"
- User types a slash command: `/save`, `/resume [code]`, `/resume light`, `/bookmark "name"`, `/list bookmarks`, `/recover_last`, `/merge`, `/diff`, `/export`
- Token usage is estimated at >= 80% of the context window (auto-trigger; show dashboard first)
- The conversation has exceeded ~40 messages or ~15,000 words
- A complex task (coding, research, debugging) is mid-flight and must be resumed later

Read the relevant reference files before acting:

| Task | Read |
|------|------|
| Saving context | `references/save-pipeline.md` |
| Compression and forgetting | `references/compression.md` |
| Cross-model resume | `references/cross-model.md` |
| Encryption and privacy | `references/security.md` |
| Versioning and bookmarks | `references/versioning.md` |
| Resume modes and commands | `references/resume-modes.md` |
| Health dashboard | `references/dashboard.md` |
| Analytics and export | `references/analytics.md` |
| Emergency and self-healing | `references/recovery.md` |

---

## Core Commands

| Command | Action |
|---------|--------|
| `/save` | Full save — compress, sign, export `.md` |
| `/save encrypt` | Save with GPG/password encryption to `.md.gpg` |
| `/save light` | Aggressive compression, minimal file size |
| `/resume [code or file]` | Full resume from code or uploaded `.md` |
| `/resume light` | Inject only critical state, skip full transcript |
| `/bookmark "name"` | Create a named checkpoint mid-conversation |
| `/list bookmarks` | Show all bookmarks with token cost and date |
| `/diff v1 v2` | Show what changed between two snapshots |
| `/merge` | Merge two parallel chat contexts |
| `/recover_last` | Emergency recovery of incomplete save |
| `/export pdf or timeline or quiz` | Convert saved context to other formats |
| `/health` | Show token usage dashboard |
| `/expiry 7d` | Set TTL on the next save |

---

## Save Pipeline (Overview)

When `/save` is triggered, follow these steps in order:

### Step 1 — Show Health Dashboard
Before saving, always show the Context Health Dashboard (see `references/dashboard.md`). This lets the user decide compression level.

### Step 2 — Estimate Output Size
Before compressing, tell the user:

> "Saving will produce approximately N characters (~X KB). Choose compression level: `low` (fast, full fidelity) / `medium` (drop low-value turns) / `high` (aggressive summarisation + code hashing)."

Default to `medium` if the user does not respond.

### Step 3 — Compression and Selective Forgetting
Read `references/compression.md`. Drop low-value messages. Optionally hash long code blocks. Produce compressed conversation representation.

### Step 4 — Assemble Checkpoint File
Build `context-checkpoint.md` with this exact top-level structure:

```
# Context Checkpoint: [Title]

Date: [ISO date]
Model: [model name or "unknown"]
Version: [vN — increment on each save]
Checksum: [SHA-256 of Sections 1-6, computed last]
TTL: [expiry date if set, else "none"]
Summary: [one-sentence description]

## 1. Objectives
## 2. Key Decisions and Conclusions
## 3. Artifacts [full code reproduction]
## 4. Current State [what works / broken / last error]
## 5. Open Issues and Next Steps [numbered, priority order]
## 6. Continuation Prompt [paste-ready, model-agnostic]
## 7. Pending Actions [unexecuted tasks, if any]
## 8. Bookmarks Index [named checkpoints, if any]
## 9. Redundancy Block [duplicate of critical facts for self-healing]
## 10. Checksum Block [SHA-256 verification]
```

For format details of each section, see `references/save-pipeline.md`.

### Step 5 — Self-Healing Integrity
Compute SHA-256 of the full file content (Sections 1-9). Write it into Section 10 as:

```
SHA256: <hash>
REDUNDANCY: [repeat 3-5 most critical facts verbatim]
```

See `references/recovery.md` for checksum computation and repair logic.

### Step 6 — Versioning
Save as `context-checkpoint_v[N].md`. Maintain rolling history of last 5 versions. Update `_master_context_index.md` with a one-line entry for this snapshot. See `references/versioning.md`.

### Step 7 — Encryption (if requested)
If `/save encrypt` was used, apply encryption before writing to disk. See `references/security.md`.

### Step 8 — Output and Instructions
Present the file for download. Then tell the user exactly:

1. Download `context-checkpoint_vN.md`
2. Open a new chat window
3. Paste the Continuation Prompt (Section 6) as the first message
4. Then paste or upload the Artifacts section (Section 3)
5. If resuming on a different AI model, paste the model-specific adapter from Section 6 (see `references/cross-model.md`)

---

## Quality Checklist

Before finalising the file, verify every item:

- [ ] Token dashboard was shown before saving
- [ ] Output size was estimated and compression level confirmed
- [ ] All code artifacts reproduced in full — no truncation or placeholder comments
- [ ] Continuation prompt is self-contained and model-agnostic
- [ ] All error messages and tracebacks reproduced exactly
- [ ] Pending actions (unexecuted tool calls) captured in Section 7
- [ ] Checksum written and redundancy block populated
- [ ] Version number incremented; `_master_context_index.md` updated
- [ ] TTL set if user requested expiry
- [ ] Encryption applied if `/save encrypt` was used

---

## Adaptive Behaviour

Track the following across sessions (store in `_master_context_index.md`):

- How often the user actually resumes from saved context
- Average token usage at time of save
- Preferred compression level

If the user has never resumed from a saved context across 5+ saves: stop auto-triggering at 80% — only save when explicitly commanded.
If the user resumes frequently and the save threshold feels late: lower auto-trigger to 70%.
Log the adapted threshold in `_master_context_index.md` under `adaptive_config`.

---

## Emergency Hard Stop

If the token limit is hit unexpectedly mid-response:

1. Immediately save whatever is in the buffer
2. Mark the file header: [INCOMPLETE — possible message loss]
3. Log which messages may be truncated in Section 4 (Current State)
4. Output recovery instructions (see `references/recovery.md`)

---

## Notes

- Never store encryption keys — user provides them each time
- For voice/multimodal sessions, see `references/analytics.md` for audio fingerprint guidance
- The skill works on any AI model — the continuation prompt in Section 6 is always model-agnostic
- For collaborative handovers, generate a read-only summary variant (omit Section 3 raw code if confidential)
