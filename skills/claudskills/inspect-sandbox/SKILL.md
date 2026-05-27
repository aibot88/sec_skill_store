---
name: inspect-sandbox
description: >
    Inspects a Linux container or sandbox environment and produces a structured
    HTML report covering filesystem mounts, process security context, and network
    configuration. Also renders a multi-page landscape A4 PDF of the report for
    inline display and download.
---

# Sandbox Inspector

Automated environment inspection that parses system state into a self-contained HTML viewer with collapsible sections, category filters, and rendered Mermaid diagrams. When running inside the Claude sandbox, the full output is packaged into a downloadable zip that the user can run locally with a single command. A multi-page landscape A4 PDF of all text sections is also rendered via Playwright and presented inline in the chat client.

---

## ⚠️ MANDATORY: Always Use `make inspect`

**`make inspect` MUST always be run.** Never call `sandbox_inspect.sh` or `generate_diagrams.py` directly. The `make inspect` target is the only supported entry point -- it orchestrates the full pipeline in the correct order:

1. **Inspection**: Runs `sandbox_inspect.sh` -> `output/sandbox/report.txt`
2. **Diagrams**: Runs `generate_diagrams.py` -> `output/sandbox/diagram_*.md` + `diagrams.json`
3. **Finalization**: Stops any running server, then serves `inspector.html` directly

Calling scripts individually will produce incomplete or inconsistent output. `make inspect` is the contract -- use it.

---

## Production Workflow

### 1. Run the Inspection

```bash
make inspect
```

This is the only step needed. The full pipeline runs automatically.

### 2. Post-inspection: Sandbox Bundle (IS_SANDBOX=yes)

After `make inspect` completes, check the environment:

```bash
echo "${IS_SANDBOX:-no}"
```

If `IS_SANDBOX=yes`, the HTML viewer cannot be served directly -- there is no browser. Instead, perform steps 3a-3e to build a downloadable zip the user can run locally.

#### 3a. Render Mermaid diagrams

`generate_diagrams.py` writes `.md` files containing fenced Mermaid blocks. These must be rendered to SVG before packaging. In the sandbox, use `mmdc` directly (Docker is unavailable):

```bash
cat > /tmp/puppeteer-config.json << 'EOF'
{
  "executablePath": "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
  "args": ["--no-sandbox", "--disable-setuid-sandbox"]
}
EOF

for md in output/sandbox/diagram_*.md; do
    base="${md%.md}"
    mmdc -i "$md" -o "${base}.svg" --puppeteerConfigFile /tmp/puppeteer-config.json
done
```

`mmdc` produces files named `diagram_<key>-1.svg` (one per diagram block). `generate_diagrams.py` detects this naming automatically -- if the mmdc output files exist on disk it uses `diagram_<key>-1.svg` in `diagrams.json`; if the Docker wrapper naming (`diagram_<key>.svg-1.svg`) is found instead it uses that. This means rendering can happen before or after the diagrams step without manual intervention.

If Chromium is not at the expected path:

```bash
find /opt/pw-browsers -name "chrome" | grep -v headless | head -1
```

#### 3b. Render PDF

Run `screenshot_report.py` from the skill working directory. It patches `inspector.html` to inline all data (bypassing `fetch()`), stubs out mermaid, loads it via `file://` in Playwright/Chromium, then renders all text sections as a single multi-page landscape A4 PDF.

```bash
python3 scripts/screenshot_report.py --out-dir output/sandbox
```

This produces `output/sandbox/sandbox-report.pdf` -- one A4 landscape page per CSS page-break, covering all five text sections (filesystem, security, network, processes, runtime). The diagrams tab is intentionally excluded: its Mermaid SVGs are built for interactive pan/zoom and paginate badly in print.

**Why file:// + inline data?** Playwright's Chromium sandbox blocks loopback connections (`ERR_SOCKET_NOT_CONNECTED`), so an HTTP server on localhost won't work. The script patches `inspector.html` with all report data inlined and a `fetch()` interceptor, loads it as `file://`, renders the PDF, then deletes the patched file.

Optional args:

- `--width 1400` -- viewport width in px before PDF scaling (default: 1400)

If Chromium is not found at the default path (`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`), the script auto-detects it. Manual fallback:

```bash
find /opt/pw-browsers -name "chrome" | grep -v headless | head -1
```

#### 3c. Create `serve.sh`

Write a launcher script to the `output/sandbox/` working directory (it will be promoted to the zip root in step 3e):

```bash
cat > output/sandbox/serve.sh << 'SCRIPT'
#!/usr/bin/env bash
# serve.sh -- Start a local HTTP server to view the sandbox inspection report
# Usage: ./serve.sh [PORT]   (default port: 8080)
# Then open: http://localhost:8080/index.html
set -euo pipefail
PORT="${1:-8080}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Starting sandbox report viewer..."
echo "  URL: http://localhost:${PORT}/index.html"
echo "Press Ctrl+C to stop."
cd "$DIR"
python3 -m http.server "$PORT"
SCRIPT
chmod +x output/sandbox/serve.sh
```

#### 3d. Create `README.md`

Write a README to `output/sandbox/` (also promoted to zip root in step 3e). It must cover:

- Full listing of zip contents with a description of each file
- How to run `serve.sh` and open the viewer (`http://localhost:8080/index.html`)
- Alternative server options: `python3 -m http.server`, `npx serve`, VS Code Live Server
- Explicit note that `inspector.html` **must** be served over HTTP -- opening it as a `file://` URL will not work because it uses `fetch()` to load report data
- Note that `report.txt` is available as a plain-text fallback requiring no server

#### 3e. Assemble and zip

**SECURITY CHECK -- do this before zipping:** Scan `output/sandbox/report.txt` for any unredacted secrets before packaging. The inspection script masks known patterns, but operator-injected variables with unusual names may slip through. Run:

```bash
grep -iE '(KEY|TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL|AUTH|API_|_API|PRIVATE)=' output/sandbox/report.txt \
    | grep -v '\*\*\*REDACTED\*\*\*' \
    && echo "WARNING: possible unredacted secrets above -- do NOT zip" \
    || echo "OK: no obvious unredacted secrets found"
```

If the check prints any lines above the warning, manually redact those lines in `report.txt` before proceeding. Never zip or share any artifact that contains unmasked credentials.

The zip must follow this exact directory structure:

```
sandbox-inspection.zip
├── README.md            <- user instructions
├── index.html           <- the HTML viewer
├── serve.sh             <- one-command local server launcher
└── vendor/
    └── js/
        └── mermaid.min.js      <- for rendering the mermaid diagrams
└── output/
    └── sandbox/
        ├── report.txt          <- raw plain-text inspection output
        ├── diagrams.json       <- diagram manifest consumed by inspector.html
        ├── diagram_mounts.md
        ├── diagram_mounts-1.svg
        ├── diagram_runtime.md
        ├── diagram_runtime-1.svg
        ├── diagram_security.md
        ├── diagram_security-1.svg
        └── sandbox-report.pdf  <- multi-page A4 landscape PDF of all text sections
```

`index.html` lives at the zip root and fetches data from the relative path `output/sandbox/` -- this is why the hierarchy matters. `serve.sh` must also be at the root so it serves from the same directory as `index.html`.

Use a staging directory to assemble the layout, then zip from inside it so no extra path prefix is introduced:

```bash
STAGE=/tmp/sandbox-inspection-stage
rm -rf "$STAGE" && mkdir -p "$STAGE/output/sandbox" && mkdir -p "$STAGE/vendor/js"
SRC=output/sandbox

# Promote these to the zip root
cp index.html               "$STAGE/"
cp "$SRC/README.md"         "$STAGE/"
cp "$SRC/serve.sh"          "$STAGE/"
cp vendor/js/mermaid.min.js "$STAGE/vendor/js/"

# Data files stay under output/sandbox/
cp "$SRC/report.txt"         "$STAGE/output/sandbox/"
cp "$SRC/diagrams.json"      "$STAGE/output/sandbox/"
cp "$SRC"/diagram_*.md       "$STAGE/output/sandbox/"
cp "$SRC"/diagram_*-1.svg    "$STAGE/output/sandbox/"
cp "$SRC/sandbox-report.pdf" "$STAGE/output/sandbox/"

cd "$STAGE"
zip -r /mnt/user-data/outputs/sandbox-inspection.zip .
```

### 4. Presenting Results

Always summarise key findings inline regardless of environment: identity & privilege level, Linux capabilities, writable paths, network posture (egress proxy, outbound connectivity), and available runtimes.

**In sandbox** (`IS_SANDBOX=yes`):

1. Present `sandbox-report.pdf` and `sandbox-inspection.zip` via `present_files`. Tell the user to unzip and run `./serve.sh`, then open `http://localhost:8080/index.html`.
2. Rasterise PDF pages with `pdftoppm` and `view` each resulting `.jpg` so the user gets an immediate visual preview in chat without downloading anything:

```bash
pdftoppm -r 120 -jpeg -f 1 -l N output/sandbox/sandbox-report.pdf /tmp/pdf_preview
# then view each /tmp/pdf_preview-*.jpg
```

**Outside sandbox**: use `make inspect` (which stops any stale server first) to launch `inspector.html` directly in the default browser.

---

## How the Downloaded Bundle Works

When the user downloads and unzips `sandbox-inspection.zip` they get a self-contained report package. Here is what each piece does:

**`index.html`** -- the interactive viewer. It loads `output/sandbox/report.txt` and `output/sandbox/diagrams.json` via `fetch()`, parses them into collapsible sections, and renders the Mermaid SVGs inline. Starts in light mode. Has a dark/light toggle. Because it relies on `fetch()` it must be served over HTTP, not opened directly as a file.

**`serve.sh`** -- a minimal Python 3 HTTP server launcher. Running `./serve.sh` (or `./serve.sh 9090` for a custom port) starts serving from the unzipped directory and prints the URL. Requires only Python 3, which is present on any modern Mac, Linux, or WSL environment.

**`output/sandbox/report.txt`** -- the raw plain-text inspection output. Readable in any terminal or text editor without a server. Useful for quick reference or diffing across environments.

**`output/sandbox/sandbox-report.pdf`** -- multi-page landscape A4 PDF covering all five text sections. Viewable in any PDF reader without a server. Produced by `screenshot_report.py`.

**`output/sandbox/diagrams.json`** -- manifest that maps diagram keys to their SVG filenames. `index.html` reads this to know which images to display and where.

**`output/sandbox/diagram_*.md`** -- Mermaid source for each diagram. Renderable independently in VS Code (Mermaid Preview extension) or on GitHub.

**`output/sandbox/diagram_*-1.svg`** -- pre-rendered SVG diagrams. Displayed inline by the viewer; also openable standalone in any browser.

---

## Available Targets

| Target          | Action                                                                         |
| :-------------- | :----------------------------------------------------------------------------- |
| `make inspect`  | **Required.** Runs the full pipeline: report -> diagrams -> HTML finalization. |
| `make report`   | Runs the raw shell inspector only -> `output/sandbox/report.txt`.              |
| `make diagrams` | Generates Mermaid diagram `.md` files from the latest report.                  |
| `make serve`    | Starts a local HTTP server at `http://localhost:8080` with auto-reload.        |

---

## Key Artifacts & Output Tree

```text
output/sandbox/
├── report.txt          # Raw plain-text output from the inspector
├── diagram_*.md        # Mermaid source files (one per diagram)
├── diagram_*-1.svg     # Rendered SVG diagrams (mmdc sandbox naming)
├── diagrams.json       # Manifest: key -> {title, md file, svg file}
├── index.html          # Copy of the viewer (synced from inspector.html by make inspect)
├── serve.sh            # Staged here before promotion to zip root
├── README.md           # Staged here before promotion to zip root
└── sandbox-report.pdf  # Multi-page A4 landscape PDF (Playwright)
```

---

## Development & Quality Control

- **Formatting**: `make format` (Black + Isort)
- **Linting**: `make lint` (Ruff with auto-fix)
- **Testing**: `make test` (Pytest with coverage)
- **Cleanup**: `make clean` (removes `output/sandbox/` and venv)
- **Packaging**: `make zip` (bundles the skill source for distribution)

---

## Error Handling & Constraints

- **Venv missing**: `check-venv` target will error. Run `make install` first.
- **Script failures**: if `sandbox_inspect.sh` exits non-zero the pipeline halts -- no partial report.
- **Port conflicts**: `make serve` defaults to `8080`. Override with `PORT=9090 make serve`.
- **PDF failures**: if `screenshot_report.py` fails, the zip can still be produced without the PDF -- note the failure to the user and present the zip anyway. The PDF is additive; it doesn't block the primary deliverable.
- **Diagrams tab excluded from PDF**: the Mermaid SVGs in the diagrams tab are built for interactive pan/zoom and paginate very badly in print (mostly blank pages). This is by design -- the SVGs are fully available in the zip and interactive HTML viewer.
- **Chromium path changed**: the script auto-detects via `find /opt/pw-browsers -name "chrome" | grep -v headless`. If auto-detect fails, update `CHROMIUM_DEFAULT` in the script.
- **Loopback connections blocked**: do NOT use an HTTP server for PDF rendering -- Playwright's Chromium sandbox blocks `ERR_SOCKET_NOT_CONNECTED` on localhost. Always use the file:// + inline-data approach in `screenshot_report.py`.
- **index.html as file://**: will silently fail to load data -- `fetch()` is blocked on `file://` origins in most browsers. Must be served over HTTP.
- **SVG naming mismatch**: `generate_diagrams.py` checks for both `diagram_<key>-1.svg` (mmdc) and `diagram_<key>.svg-1.svg` (Docker wrapper) and writes whichever exists into `diagrams.json`. If neither exists yet (diagrams not yet rendered), it defaults to the mmdc name -- re-run `generate_diagrams.py` after rendering if needed.
- **Blank 1-page PDF**: caused by `inspector.html` loading mermaid via `<script src="vendor/js/mermaid.min.js">`, which cannot resolve as a relative path under `file://`. This aborts app init before `fetch()` fires. Fixed in `screenshot_report.py` by replacing the `<script src=...>` tag with a lightweight stub: `window.mermaid = {initialize(){}, run(){}, contentLoaded(){}}`. The diagrams tab is excluded from the PDF so mermaid doesn't need to work -- it just must not throw. **Do NOT inline the full `mermaid.min.js` as a `<script>` block**: at ~3 MB of minified JS with no newlines, Chromium's PDF renderer treats it as visible body text, producing pages of garbage output.
- **`_in_sandbox()` returning False on Firecracker VMs**: the function checks `IS_SANDBOX` env var first, then `/.dockerenv` and `/run/.containerenv`. Firecracker VMs set `IS_SANDBOX=yes` but have neither marker file. If `_in_sandbox()` returns False incorrectly, the script falls through to `_docker_available()` which crashes if `docker` is not on PATH.
- **`docker` not on PATH crash**: `_docker_available()` guards with `shutil.which("docker")` before invoking it. If docker is absent it returns False cleanly rather than raising `FileNotFoundError`.
