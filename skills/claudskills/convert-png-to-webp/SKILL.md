---
name: convert-png-to-webp
description: "Use this skill when converting PNG images in a directory tree to lossless WebP in place with `cwebp`, preserving original file timestamps, deleting the source PNG files only after successful conversion, and reporting the processed image count."
license: MIT
metadata:
  author: cssmagic
---

# Convert PNG to WebP

## Purpose

Convert PNG files inside one directory tree to same-location `.webp` files:

- Convert PNG files to lossless WebP.
- Preserve original modification time and, on macOS, creation time.
- Delete each source PNG only after its WebP replacement is complete.
- Report how many PNG files were processed.



## Required Input

Each run needs one directory to process.

If the directory is missing or ambiguous, ask the user for the path before running commands.

Normalize `~` and relative paths to an absolute path before reporting or running the script.



## Defaults

Treat PNG extensions case-insensitively.

Map each PNG to a same-directory, same-basename `.webp` file.

Do not overwrite existing `.webp` files unless the user explicitly allows overwrite behavior. If a mapped `.webp` already exists, report the exact PNG and WebP paths and stop before converting anything.

Reject symlinked PNG files before writing, because deleting a symlink after conversion is easy to misread.



## Prerequisites

Use the official WebP CLI:

```bash
command -v cwebp
```

The bundled script requires Python 3:

```bash
command -v python3
```

On macOS, creation-time preservation requires:

```bash
command -v GetFileInfo
command -v SetFile
```

If those macOS timestamp tools are unavailable, stop before converting anything.



## Workflow

Set the directory from the user's provided path:

```bash
dir="/absolute/path/to/directory"
```

Run the bundled script from this skill directory:

```bash
python3 scripts/convert_png_to_webp.py "$dir"
```

Only pass `--overwrite` if the user explicitly permits replacing existing mapped WebP files:

```bash
python3 scripts/convert_png_to_webp.py --overwrite "$dir"
```

The script performs preflight checks before writing:

- required commands
- directory existence
- existing mapped WebP files
- target path collisions, including case-insensitive collisions
- symlinked PNG files

During conversion, the script writes a temporary WebP beside the source file, syncs timestamps, atomically moves it into place, and only then deletes the source PNG.



## Reporting

Summarize with:

- directory
- PNG files found
- converted WebP files
- deleted original PNG files
- failed files, if any
- timestamp failure count
- whether macOS creation times were synced
