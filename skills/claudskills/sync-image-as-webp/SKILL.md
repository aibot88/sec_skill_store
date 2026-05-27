---
name: sync-image-as-webp
description: Use this skill when converting a source directory tree of PNG files to lossless WebP with `cwebp`, copying all non-PNG files unchanged, preserving directory structure, and syncing macOS creation and modification timestamps (if possible).
license: MIT
metadata:
  author: cssmagic
---

# Sync Image As WebP

## Purpose

Convert a source directory into a target directory while preserving structure:

- Convert PNG files to same-name `.webp` using lossless WebP.
- Copy all non-PNG files unchanged.
- Sync empty directories.
- Sync target file creation time and modification time from source files.
- Verify file, directory, timestamp, and item-count differences.



## Required Inputs

Each run needs:

- Source directory
- Target directory

If either directory is missing or ambiguous, ask the user for the missing path before running commands.

Do not infer a target directory from the source directory unless the user explicitly asks for that behavior.

After paths are known, normalize `~` and relative paths to absolute paths before reporting or running destructive-looking operations.



## Defaults

Use these mappings:

- Source PNG file -> target `.webp`
- Source non-PNG file -> target same filename
- Source directory -> target same relative directory

Treat PNG extensions case-insensitively.

Never delete files.

Do not overwrite existing mapped target files unless the user explicitly allows overwrite behavior.

Reject the run before writing if multiple source files map to the same target path.

Reject the run before writing if the target directory is inside the source directory.



## Prerequisites

Prefer the official WebP CLI:

```bash
command -v cwebp
```

The bundled script requires Python 3:

```bash
command -v python3
```

On macOS, creation-time syncing uses:

```bash
command -v GetFileInfo
command -v SetFile
```

If creation-time syncing is unavailable, continue the run and tell the user in the final report that only modification times were synced.



## Workflow

Set source and target directories from the user's provided paths:

```bash
src="/absolute/path/to/source"
dst="/absolute/path/to/target"
```

Run the bundled script from this skill directory:

```bash
python3 scripts/sync_image_as_webp.py "$src" "$dst"
```

Only pass `--overwrite` if the user explicitly permits replacing existing mapped target files:

```bash
python3 scripts/sync_image_as_webp.py --overwrite "$src" "$dst"
```

The script performs preflight checks before writing:

- target path collisions, including case-insensitive collisions
- existing mapped target files, unless `--overwrite` is used
- target directory nested inside source directory
- target directory paths that already exist as files



## Verification

The script verifies and reports:

- expected target files exist
- PNG conversion and copy command failures
- modification-time parity
- macOS creation-time parity when available
- source and target directory differences
- target-only files



## Reporting

Summarize with:

- source directory
- target directory
- PNG converted count
- non-PNG copied count
- directories created count if relevant
- missing target count
- timestamp diff counts
- command failure count
- whether creation times were synced
- any source-only or target-only directories/files

If creation times were not synced, explicitly tell the user that only modification times were preserved.
