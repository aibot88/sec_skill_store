---
name: hooks-manager
description: Detect project tech stack and configure Claude Code hooks for mechanical enforcement of linting and security rules. Use this skill when a user wants to set up hooks, configure auto-linting, add security guards, or move from advisory CLAUDE.md rules to mechanical enforcement.
---

# Hooks Manager Skill

**Version**: 1.0.0
**Category**: Enforcement
**Type**: Conversational (generates configuration)
**Duration**: 1-3 minutes

## Purpose

CLAUDE.md rules are advisory -- Claude can ignore them. Hooks are mechanical -- they execute automatically and cannot be bypassed. This skill detects a project's tech stack and available linters, then generates a `.claude/settings.json` with PostToolUse (lint) and PreToolUse (security) hooks configured.

> "The difference between 'I told it not to' and 'it physically cannot' is everything."

## Execution Steps

### Step 1: Locate Hook Scripts

Determine the path to the Artifex hooks directory. Check in order:

1. `~/.claude/hooks/` (if installed via installer)
2. The Artifex repo's `hooks/` directory (if running from source)

Verify both `post-write-lint.sh` and `pre-command-security.sh` exist and are executable. If not found, report the issue and offer to create them.

Set `HOOKS_DIR` to the resolved path for use in settings.json.

### Step 2: Detect Tech Stack

Use Glob and file existence checks to identify the project's technologies:

| File/Pattern | Technology | Linter to check |
|---|---|---|
| `package.json`, `*.js`, `*.ts`, `*.jsx`, `*.tsx` | JavaScript/TypeScript | biome, eslint |
| `*.py`, `pyproject.toml`, `setup.py`, `requirements.txt` | Python | ruff, flake8 |
| `*.sh`, `*.bash` | Shell scripts | shellcheck |
| `*.go`, `go.mod` | Go | go vet |
| `Cargo.toml`, `*.rs` | Rust | cargo clippy |

For each detected technology, check if the corresponding linter is installed:

```bash
command -v biome >/dev/null 2>&1 && echo "biome available" || echo "biome not found"
command -v eslint >/dev/null 2>&1 && echo "eslint available" || echo "eslint not found"
command -v ruff >/dev/null 2>&1 && echo "ruff available" || echo "ruff not found"
command -v flake8 >/dev/null 2>&1 && echo "flake8 available" || echo "flake8 not found"
command -v shellcheck >/dev/null 2>&1 && echo "shellcheck available" || echo "shellcheck not found"
command -v go >/dev/null 2>&1 && echo "go available" || echo "go not found"
command -v cargo >/dev/null 2>&1 && echo "cargo available" || echo "cargo not found"
```

### Step 3: Present Detection Results

Show the user what was detected:

```
Tech Stack Detection
====================

Detected technologies:
  - JavaScript/TypeScript (found package.json, *.ts files)
  - Shell scripts (found *.sh files)

Available linters:
  - eslint (for JS/TS) ........... installed
  - biome (for JS/TS) ............ not found
  - shellcheck (for shell) ....... installed
  - ruff (for Python) ............ not applicable

Hooks to configure:
  1. PostToolUse: Auto-lint after Write/Edit
     - Will run eslint on JS/TS files
     - Will run shellcheck on shell scripts
  2. PreToolUse: Security guard on Bash commands
     - Blocks catastrophic deletes (rm -rf /, ~, $HOME)
     - Blocks force-push to main/master
     - Blocks reading .env files
     - Blocks chmod 777
     - Blocks pipe-to-shell (curl | sh)
```

### Step 4: Check Existing Configuration

Read `.claude/settings.json` if it exists. If it already has hooks configured:

- Show the current hook configuration
- Ask the user whether to merge (add new hooks alongside existing) or replace
- Never silently overwrite existing hooks

If `.claude/settings.json` does not exist, note that it will be created.

### Step 5: Generate Configuration

Create or update `.claude/settings.json` with the hooks configuration:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hook": "HOOKS_DIR/post-write-lint.sh $TOOL_INPUT_FILE $TOOL_OUTPUT_FILE"
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hook": "HOOKS_DIR/pre-command-security.sh $TOOL_INPUT"
      }
    ]
  }
}
```

Replace `HOOKS_DIR` with the actual resolved path from Step 1.

If existing settings have other keys (not hooks), preserve them when writing.

### Step 6: Verify Installation

After writing the configuration:

1. Confirm `.claude/settings.json` was written successfully
2. Show the final configuration to the user
3. Explain what each hook does

### Step 7: Suggest Missing Linters

If any detected technology has no linter available, suggest installation:

| Technology | Recommended linter | Install command |
|---|---|---|
| JavaScript/TypeScript | biome | `npm install --save-dev @biomejs/biome` |
| JavaScript/TypeScript | eslint | `npm install --save-dev eslint` |
| Python | ruff | `pip install ruff` or `brew install ruff` |
| Python | flake8 | `pip install flake8` |
| Shell | shellcheck | `brew install shellcheck` or `apt install shellcheck` |
| Go | go vet | Included with Go installation |
| Rust | cargo clippy | `rustup component add clippy` |

## Customization

If the user asks to customize, support these operations:

### Add a security rule

Ask for:
1. The command pattern to block (regex)
2. The explanation message

Then edit `pre-command-security.sh` to add the new check before the final `exit 0`:

```bash
# User-defined rule: <description>
if echo "$COMMAND" | grep -qE '<pattern>'; then
  block "<explanation>"
fi
```

### Remove a security rule

Show the current rules in `pre-command-security.sh` and ask which to remove. Comment out or delete the corresponding `if` block.

### Add a linter

Ask for:
1. The file extension(s)
2. The linter command
3. The arguments

Then edit `post-write-lint.sh` to add a new case in the `run_lint()` function.

### Disable lint for a file type

Remove or comment out the corresponding case in `post-write-lint.sh`.

## Rules

1. **Never silently overwrite existing configuration.** Always show what will change and ask for confirmation.
2. **Preserve existing settings.json keys.** Only modify the `hooks` section.
3. **Use absolute paths in hook commands.** Relative paths break when the working directory changes.
4. **The lint hook always exits 0.** Lint results are advisory feedback, not gates.
5. **The security hook exits 1 to block.** Security violations are hard stops.
6. **Suggest but do not auto-install linters.** The user decides what to install.
