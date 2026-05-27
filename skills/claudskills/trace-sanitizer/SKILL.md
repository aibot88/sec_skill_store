---
name: trace-sanitizer
description: >
  Export Claude Code, Codex, Gemini CLI, and OpenCode conversation history for TRACED.
  Use when the user asks about exporting conversations, donating to TRACED,
  configuring trace-sanitizer, reviewing PII/secrets in exports, or managing their dataset.
allowed-tools: Bash(trace-sanitizer *), Bash(pip install trace-sanitizer*)
---

<!-- trace-sanitizer-begin -->

# Trace-Sanitizer Skill

## THE RULE

**Every `trace-sanitizer` command outputs `next_steps`. FOLLOW THEM.**

Do not memorize the flow. Do not skip steps. Do not improvise.
Run the command -> read the output -> follow `next_steps`. That's it.

The CLI tracks your stage (1-3: configure -> review -> confirmed).

## Getting Started

Run `trace-sanitizer status` (or `trace-sanitizer prep` for full details) and follow the `next_steps`.

## Output Format

- `trace-sanitizer prep`, `trace-sanitizer config`, `trace-sanitizer status`, and `trace-sanitizer confirm` output pure JSON
- `trace-sanitizer export` outputs human-readable text followed by `---TRACE_SANITIZER_JSON---` and a JSON block
- Always parse the JSON and act on `next_steps`

Key fields:
- `stage` / `stage_number` / `total_stages` -- where you are
- `next_steps` -- follow these in order
- `next_command` -- the single most important command to run next (null if user input needed first)

## PII Audit (Stage 2)

After `trace-sanitizer export`, follow the `next_steps` in the JSON output. The flow is:

1. **Ask the user their full name** -- then grep the export for it
2. **Run the pii_commands** from the JSON output and review results with the user
3. **Ask the user what else to look for** -- company names, client names, employer names, private URLs, other people's names, custom domains, account/org names (Vercel teams, Supabase projects), geographic identifiers, social profiles (LinkedIn, GitHub linked to real names), and any hardware identifiers
4. **Deep manual scan** -- sample ~20 sessions (beginning, middle, end) and look for anything sensitive the regex missed. Check for resume/CV content, browser history, Discord data, and system forensics that could defeat anonymization
5. **Fix and re-export** if anything found: `trace-sanitizer config --redact "string"` then `trace-sanitizer export`
6. **Run `trace-sanitizer confirm` with text attestations** -- pass `--full-name`, `--attest-full-name`, `--attest-sensitive`, and `--attest-manual-scan`. It runs PII scan, verifies attestations, shows project breakdown, and confirms the export.
7. **Donate** -- the export folder contains trajectories.jsonl + CDLA-Permissive-2.0 license. Zip the folder, upload to Google Drive, and share with donate@traced.run

## Commands Reference

```bash
trace-sanitizer status                            # Show current stage and next steps (JSON)
trace-sanitizer prep                              # Discover projects (JSON)
trace-sanitizer prep --source all                 # All sources (Claude + Codex + Gemini + OpenCode)
trace-sanitizer prep --source claude              # Only Claude Code sessions
trace-sanitizer prep --source codex               # Only Codex sessions
trace-sanitizer prep --source gemini              # Only Gemini CLI sessions
trace-sanitizer prep --source opencode            # Only OpenCode sessions
trace-sanitizer confirm --full-name "NAME" --attest-full-name "..." --attest-sensitive "..." --attest-manual-scan "..." # Scan PII, verify attestations, confirm export (JSON)
trace-sanitizer confirm --file /path/to/file.jsonl --full-name "NAME" --attest-full-name "..." --attest-sensitive "..." --attest-manual-scan "..." # Confirm a specific export file
trace-sanitizer list                              # List all projects with exclusion status
trace-sanitizer list --source all                 # List all sources
trace-sanitizer list --source codex               # List only Codex projects
trace-sanitizer config                            # Show current config
trace-sanitizer config --source all               # REQUIRED source scope: claude|codex|gemini|opencode|all
trace-sanitizer config --exclude "a,b"            # Add excluded projects (appends)
trace-sanitizer config --redact "str1,str2"       # Add strings to redact (appends)
trace-sanitizer config --redact-usernames "u1,u2" # Add usernames to anonymize (appends)
trace-sanitizer config --confirm-projects         # Mark project selection as confirmed
trace-sanitizer export                            # Export locally
trace-sanitizer export --source all               # Export all sources
trace-sanitizer export --source codex             # Export only Codex sessions
trace-sanitizer export --source claude            # Export only Claude Code sessions
trace-sanitizer export --source gemini            # Export only Gemini CLI sessions
trace-sanitizer export --source opencode          # Export only OpenCode sessions
trace-sanitizer export --all-projects             # Include everything (ignore exclusions)
trace-sanitizer export --no-thinking              # Exclude extended thinking blocks
trace-sanitizer export -o /path/to/file.jsonl     # Custom output path
trace-sanitizer update-skill claude               # Install/update the trace-sanitizer skill for Claude Code
```

## Gotchas

- **`--exclude`, `--redact`, `--redact-usernames` APPEND** -- they never overwrite. Safe to call repeatedly.
- **Source selection is REQUIRED before export** -- explicitly set `trace-sanitizer config --source claude|codex|gemini|opencode|all` (or pass `--source ...` on export).
- **`trace-sanitizer prep` outputs pure JSON** -- parse it directly.
- **PII audit is critical** -- automated redaction is not foolproof.
- **Large exports take time** -- 500+ sessions may take 1-3 minutes. Use a generous timeout.

## Prerequisite

`command -v trace-sanitizer >/dev/null 2>&1 && echo "trace-sanitizer: installed" || echo "NOT INSTALLED -- run: pip install trace-sanitizer"`

<!-- trace-sanitizer-end -->
