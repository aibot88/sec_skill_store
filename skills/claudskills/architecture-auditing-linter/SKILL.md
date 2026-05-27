---
name: architecture-auditing-linter
description: Ensure every project remains compliant with these standards, use the built-in `linter` tool. It scans codebase for violations of the architecture rules using AST parsing.
---

# Architecture Auditing (Linter)
> *"Dont Trust, must verify."*

It scans your code for violations of the architecture rules for logging, pathlib, print, etc. 

### How to use?
The `human-skills` linter accepts numerous tool arguments for different purposes. Below, all available arguments are explained:

allowed_args = {
    "default": ["scan_path", "path", "ignored_path", "ignored_apth", "linter_type"],
    "rest_api": ["scan_path", "path", "ignored_path", "ignored_apth", "linter_type", "ignored_rules"]
}

```json
{
    "tool_name": "linter",
    "tool_args": {
        "scan_path": "Path to the project directory or a specific .py file to audit (REQUIRED).",
        "linter_type": "Linter mode: 'default' (architecture violations) or 'rest_api' (API quality score). Defaults to 'default'.",
        "ignored_path": "Comma-separated list of directory names to skip during scanning (e.g., 'venv, .git, tests').",
        "ignored_rules": "Comma-separated list of rules to skip. Works only in rest_api mode. Example: 'auth_implementation, rate_limiting, caching_strategy'."
    }
}
```

#### 1. Audit entire project 
```bash
human-skills '{
    "tool_name": "linter",
    "tool_args": {
        "linter_type": "default",
        "scan_path": "home/user_name/project/",
        "ignored_path": "venv, .git, tests, configs"
    }
}'
```

#### 2. Audit rest api endpoint 
```bash
human-skills '{
    "tool_name": "linter",
    "tool_args": {
        "linter_type": "rest_api",
        "scan_path": "home/user_name/project/",
        "ignored_path": "venv, .git, tests, configs",
        "ignored_rules": "auth_implementation, rate_limiting, caching_strategy"
    }
}'
```

#### 3. Audit a specific file
```bash
human-skills '{
    "tool_name": "linter",
    "tool_args": {
        "scan_path": "/path/to/your/project/src/services/logic.py"
    }
}'
```



### What it detects in `default` mode?
- ❌ **Logging Violation**: Use of direct `import logging` (Must use `setup_logger`).
- ❌ **Pathlib Violation**: Use of `pathlib` outside `src/config/`.
- ❌ **Manual Dir Creation**: Use of `exist_ok=True` (Must use `ensure_dir`).
- ❌ **Silent Exception**: Use of `except: pass` (Swallowing errors).
- ⚠️ **Print Statements**: Use of `print()` in production-ready code.
- ❌ **Env Access**: Use of `os.environ` or `os.getenv` (Must use `Settings`).
- ❌ **Logger Compliance**: Hardcoded log filenames in `setup_logger`.

### What it detects in `rest_api` mode?
When `linter_type="rest_api"` is used, it evaluates router files based on 12 Enterprise API Best Practices. Some rules may not apply to local or internal tools. Use `ignored_rules` to skip them.

| Analyzer Rule | Description | When to Ignore (`ignored_rules`) |
| :--- | :--- | :--- |
| `auth_implementation` | Checks for authentication tokens, JWT, or `@login_required` decorators. | Ignore for **Local Utilities** (e.g., desktop tools like `epic-adb` running on `127.0.0.1`) or open/public data APIs. |
| `rate_limiting` | Checks for rate limiting mechanisms to prevent abuse. | Ignore for **Local Desktop Tools** or internal microservices sitting behind an API Gateway. |
| `caching_strategy` | Checks for `Cache-Control` headers or Redis usage. | Ignore for APIs that handle **Real-time Data** (like device state or live logs) where caching causes stale data. |
| `pagination_implementation` | Checks for `limit`, `offset`, or `page` parameters. | Ignore for APIs returning small, fixed lists (e.g., categories, active local devices). |
| `retry_logic` | Checks for automated retries on API failures. | Generally useful, but can be ignored if the client-side handles retries exclusively. |
| `input_validation` | Enforces Pydantic/Marshmallow schema validation at the endpoint. | *Should rarely be ignored.* Protects against malformed data. |
| `error_handling` | Detects bare `except Exception:` and enforces specific exception handling. | *Do not ignore.* Essential for debugging. |
| `status_code_usage` | Ensures standard HTTP status codes (200, 400, 500) are used correctly. | *Do not ignore.* |
| `n1_query_detection` | Detects loops containing database queries (N+1 problem). | *Do not ignore.* Critical for performance. |
| `timeout_handling` | Ensures external requests have a defined timeout to prevent hanging. | *Do not ignore.* |
| `endpoint_naming_convention` | Enforces RESTful noun-based naming conventions (e.g., `/users` instead of `/getUsers`). | *Do not ignore.* |
| `http_method_correctness` | Ensures GET for reading, POST for creating, etc. | *Do not ignore.* |

---
