---
name: scitex-logging
description: Enhanced Python logging + warnings + exceptions for SciTeX — stdlib-compatible wrapper with SUCCESS/FAIL levels, auto file output, structured category warnings, and a 30+ class `SciTeXError` hierarchy. Public API — logger (`getLogger`, `configure`, `set_level`/`get_level`, `log_to_file`/`enable_file_logging`/`is_file_logging_enabled`/`get_log_path`, `tee`/`Tee`, levels `DEBUG`/`INFO`/`SUCCESS`/`WARNING`/`FAIL`/`ERROR`/`CRITICAL`), warnings (`warn`, `warn_data_loss`, `warn_deprecated`, `warn_performance`, `filterwarnings`, `resetwarnings`, `SciTeXWarning`, `SciTeXDeprecationWarning`, `DataLossWarning`, `PerformanceWarning`, `StyleWarning`, `UnitWarning`), guards (`check_path`, `check_file_exists`, `check_shape_compatibility`), LLM sub-namespace (`scitex_logging.llm`), exception hierarchy (`SciTeXError` root + `IOError`/`LoadError`/`SaveError`/`FileFormatError`/`PathError`/`PathNotFoundError`/`InvalidPathError`/`ConfigurationError`/`ConfigFileNotFoundError`/`ConfigKeyError`/`DataError`/`DTypeError`/`ShapeError`/`AxisError`/`ModelError`/`NNError`/`PlottingError`/`FigureNotFoundError`/`StyleError`/`StatsError`/`ScholarError`/`AuthenticationError`/`DOIResolutionError`/`EnrichmentError`/`BibTeXEnrichmentError`/`PDFDownloadError`/`PDFExtractionError`/`SearchError`/`TemplateError`/`TemplateViolationError`/`TranslatorError`/`TestError`). Env var `SCITEX_LOGGING_LEVEL` sets default level at import. No CLI, no MCP tools. Drop-in replacement for stdlib `logging` + `warnings` + raising `ValueError`/`RuntimeError`/`IOError`, plus ad-hoc `loguru` / `structlog` / `rich.logging` setup + hand-rolled domain exception classes + stdout/stderr tee scripts. Use whenever the user asks to "get a logger for this module", "log SUCCESS or FAIL with a distinct level", "tee stdout to a log file", "raise a typed SciTeX error instead of ValueError", "emit a deprecation or data-loss warning", "validate a path before using it", "configure logging from SCITEX_LOGGING_LEVEL", or mentions `scitex.logging`, `SciTeXError`, `SUCCESS` log level, `Tee`.
user-invocable: false
primary_interface: python
interfaces:
  python: 3
  cli: 0
  mcp: 0
  skills: 2
  hook: 0
  http: 0
---

# scitex-logging

> **Interfaces:** Python ⭐⭐⭐ (primary) · CLI — · MCP — · Skills ⭐⭐ · Hook — · HTTP —

Auto-configured drop-in extension of `logging`:

## Installation & import (two equivalent paths)

The same module is reachable via two install paths. Both forms work at
runtime; which one a user has depends on their install choice.

```python
# Standalone — pip install scitex-logging
import scitex_logging
scitex_logging.getLogger(...)

# Umbrella — pip install scitex
import scitex.logging
scitex.logging.getLogger(...)
```

`pip install scitex-logging` alone does NOT expose the `scitex` namespace;
`import scitex.logging` raises `ModuleNotFoundError`. To use the
`scitex.logging` form, also `pip install scitex`.

See [../../general/02_interface-python-api.md] for the ecosystem-wide
rule and empirical verification table.

- Adds `SUCCESS` and `FAIL` levels on top of DEBUG/INFO/WARNING/ERROR/CRITICAL.
- File logging is on by default; log path via `get_log_path()`.
- Ships a SciTeX-wide **exception hierarchy** (`SciTeXError` and ~30 subclasses)
  plus a `warnings`-style API (`SciTeXWarning` etc.).
- Env var `SCITEX_LOGGING_LEVEL` picks the default level at import time.

## Sub-skills

- [01_quick-start.md](01_quick-start.md) — get a logger, log at any level
- [02_python-api.md](02_python-api.md) — config, levels, warnings, errors

No CLI, no MCP tools.
