---
name: eresus-python-audit
description: >
  Deep Python-specific security audit skill with 50+ vulnerability class coverage across 7 categories.
  Trigger when auditing Python code: "audit this Python app", "find Python security issues",
  "check Flask/Django for vulnerabilities", "Python SAST review", "check for pickle vulnerabilities",
  "review this FastAPI code". Covers misconfiguration, injection, crypto, XSS, deserialization,
  and ML/AI attack surfaces. Includes scripts/rules.json for programmatic rule lookup.
metadata:
  version: "1.0"
  domain: application-security
  mode: python-audit
  persona: python-security-researcher
---

# Python Security Audit

## Purpose

Perform a comprehensive, depth-first security audit of Python codebases.
This skill provides the complete knowledge of Bandit's 50+ security checks,
organized by category and severity, plus framework-specific patterns for
Django, Flask, FastAPI, and emerging ML/AI attack surfaces.

Use `view_file` and `grep_search` exclusively. No terminal commands.

---

## Audit Workflow

### Phase 1: Reconnaissance

1. Identify the Python framework in use (Django, Flask, FastAPI, Tornado, aiohttp, raw stdlib)
2. Check `requirements.txt` / `pyproject.toml` / `Pipfile` for dangerous dependencies
3. Map entry points: URL routes, CLI commands, message consumers, scheduled tasks
4. Identify configuration files and secrets management approach

### Phase 2: Systematic Check — By Category

Work through each category below. For each check, use `grep_search` to find all instances,
then `view_file` to trace the data flow and confirm exploitability.

---

## B1xx — Miscellaneous Checks

| ID | Name | Severity | What to Search |
|----|------|----------|----------------|
| B101 | `assert_used` | Low | `assert` statements used for security checks (removed with `-O` flag) |
| B102 | `exec_used` | Medium | `exec()` calls — trace if input is user-controlled |
| B103 | `set_bad_file_permissions` | Medium | `os.chmod()` with overly permissive modes (0o777, 0o666) |
| B104 | `hardcoded_bind_all_interfaces` | Medium | Binding to `0.0.0.0` — exposes service on all interfaces |
| B105 | `hardcoded_password_string` | Low | Strings assigned to variables named `password`, `secret`, `key`, `token` |
| B106 | `hardcoded_password_funcarg` | Low | Password-like strings passed as function arguments |
| B107 | `hardcoded_password_default` | Low | Default parameter values containing password-like strings |
| B108 | `hardcoded_tmp_directory` | Low | Hardcoded `/tmp` paths — race conditions, symlink attacks |
| B109 | `password_config_option_not_marked_secret` | Low | Config options with password/secret that aren't marked as sensitive |
| B110 | `try_except_pass` | Low | `except: pass` — silently swallowing errors including security exceptions |
| B111 | `execute_with_run_as_root_equals_true` | Medium | Functions called with `run_as_root=True` |
| B112 | `try_except_continue` | Low | `except: continue` — same problem as B110 |
| B113 | `request_without_timeout` | Medium | `requests.get/post()` without `timeout=` parameter — DoS via hang |

### Audit Depth for B1xx
- B101: Check if `assert` guards authentication or authorization. If so, **HIGH** severity.
- B102: Trace `exec()` input — if user-controlled, escalate to **CRITICAL** (RCE).
- B105/106/107: Check if the hardcoded credentials are for production systems or test fixtures.
- B113: Check all HTTP client calls (`requests`, `httpx`, `urllib3`, `aiohttp`) for timeout.

---

## B2xx — Application/Framework Misconfiguration

| ID | Name | Severity | What to Search |
|----|------|----------|----------------|
| B201 | `flask_debug_true` | High | `app.run(debug=True)` — enables Werkzeug debugger (RCE) |
| B202 | `tarfile_unsafe_members` | High | `tarfile.extractall()` without `filter=` — path traversal via tar |

### Audit Depth for B2xx
- B201: Check if `debug=True` is conditional on environment or always on. Check for `WERKZEUG_DEBUG_PIN`.
- B202: Any `tarfile.open()` + `extractall()` from user-uploaded files = **CRITICAL** path traversal.

---

## B3xx — Dangerous Function Calls (Blacklists)

| ID | Name | Severity | What to Search |
|----|------|----------|----------------|
| B324 | `hashlib` | Medium | Use of `md5()`, `sha1()` for security-sensitive operations (password hashing, integrity) |

### Extended B3xx Checks (Eresus additions)
- `hashlib.md5()` / `hashlib.sha1()` for password storage → escalate to **HIGH**
- Use of `random` module instead of `secrets` for security tokens → **HIGH**
- `string.Template` with user input → potential template injection

---

## B5xx — Cryptography

| ID | Name | Severity | What to Search |
|----|------|----------|----------------|
| B501 | `request_with_no_cert_validation` | High | `requests.get(url, verify=False)` — TLS downgrade |
| B502 | `ssl_with_bad_version` | High | `ssl.SSLContext(ssl.PROTOCOL_SSLv2)` or SSLv3 |
| B503 | `ssl_with_bad_defaults` | Medium | SSLContext with insecure default protocol |
| B504 | `ssl_with_no_version` | Medium | SSLContext created without explicit protocol |
| B505 | `weak_cryptographic_key` | High | RSA < 2048 bits, DSA < 2048 bits, EC < 224 bits |
| B506 | `yaml_load` | Medium | `yaml.load()` without `Loader=SafeLoader` — deserialization RCE |
| B507 | `ssh_no_host_key_verification` | High | Paramiko `set_missing_host_key_policy(AutoAddPolicy)` |
| B508 | `snmp_insecure_version` | Medium | SNMPv1/v2 without authentication |
| B509 | `snmp_weak_cryptography` | Medium | SNMPv3 with weak crypto |

### Audit Depth for B5xx
- B501: Check if cert pinning is used. If `verify=False` is in production code → **CRITICAL**.
- B506: This is a deserialization sink. If input comes from HTTP/file upload → **CRITICAL** RCE.

---

## B6xx — Injection

| ID | Name | Severity | What to Search |
|----|------|----------|----------------|
| B601 | `paramiko_calls` | Medium | Paramiko SSH command execution — trace if command is user-controlled |
| B602 | `subprocess_popen_with_shell_equals_true` | High | `subprocess.Popen(cmd, shell=True)` — command injection |
| B603 | `subprocess_without_shell_equals_true` | Low | `subprocess.Popen(cmd)` without shell — still check input |
| B604 | `any_other_function_with_shell_equals_true` | Medium | Any function with `shell=True` parameter |
| B605 | `start_process_with_a_shell` | High | `os.system()`, `os.popen()` — command injection |
| B606 | `start_process_with_no_shell` | Low | `os.execl()`, `os.execve()` — still trace input |
| B607 | `start_process_with_partial_path` | Low | Process started without full path — PATH hijacking |
| B608 | `hardcoded_sql_expressions` | Medium | SQL strings built with `+` or `%` or f-strings |
| B609 | `linux_commands_wildcard_injection` | High | Commands with `*` glob — wildcard injection (tar, chown, etc.) |
| B610 | `django_extra_used` | Medium | Django `QuerySet.extra()` — raw SQL injection |
| B611 | `django_rawsql_used` | Medium | Django `RawSQL()` — raw SQL injection |
| B612 | `logging_config_insecure_listen` | Medium | `logging.config.listen()` — arbitrary code execution |
| B613 | `trojansource` | High | Unicode bidirectional control characters — trojan source attack |
| B614 | `pytorch_load` | High | `torch.load()` — uses pickle internally, RCE if untrusted |
| B615 | `huggingface_unsafe_download` | High | HuggingFace model downloads without safety checks |

### Audit Depth for B6xx
- B602/B605: Trace the command string backwards. If ANY part is user-controlled → **CRITICAL** RCE.
- B608: Check if the SQL is parameterized elsewhere. Raw f-string SQL = **HIGH** SQLi.
- B609: `tar cf archive.tar *` in `/tmp` with user-created files → argument injection.
- B614: `torch.load()` from user-uploaded model file → **CRITICAL** RCE via pickle.
- B615: ML model supply chain attack — check if `trust_remote_code=True`.

---

## B7xx — XSS / Template Injection

| ID | Name | Severity | What to Search |
|----|------|----------|----------------|
| B701 | `jinja2_autoescape_false` | High | `jinja2.Environment(autoescape=False)` — stored/reflected XSS |
| B702 | `use_of_mako_templates` | Medium | Mako templates — no auto-escaping by default |
| B703 | `django_mark_safe` | Medium | `mark_safe(user_input)` — bypasses Django auto-escaping |
| B704 | `markupsafe_markup_xss` | Medium | `Markup(user_input)` — bypasses escaping |

### Audit Depth for B7xx
- B701: If `autoescape=False` and template renders user input → **CRITICAL** XSS.
- B703: Trace what data is passed to `mark_safe()`. If user-controlled → **HIGH** XSS.

---

## Framework-Specific Deep Checks

### Django
- Check `ALLOWED_HOSTS` configuration (empty = open redirect)
- Check `CSRF_COOKIE_HTTPONLY`, `SESSION_COOKIE_SECURE`, `SECURE_BROWSER_XSS_FILTER`
- Check for `@csrf_exempt` decorators on sensitive views
- Check `DEBUG = True` in production settings
- Check `SECRET_KEY` hardcoded or in version control
- Check `MIDDLEWARE` ordering (SecurityMiddleware should be first)
- Check `AUTH_PASSWORD_VALIDATORS` configuration

### Flask
- Check `SECRET_KEY` generation (must be cryptographically random)
- Check `app.run(debug=True)` in production
- Check for `@app.before_request` authentication enforcement
- Check session cookie configuration (`SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`)
- Check file upload handling (`werkzeug.utils.secure_filename`)

### FastAPI
- Check for missing input validation (`Body()`, `Query()`, `Path()` without constraints)
- Check CORS configuration (`allow_origins=["*"]`)
- Check authentication dependency injection (missing `Depends()`)
- Check `FileResponse` / `StreamingResponse` path traversal
- Check OAuth2 implementation (token validation, scope enforcement)

### ML/AI Attack Surface
- `torch.load()` — pickle-based, RCE from untrusted models
- `transformers.pipeline(trust_remote_code=True)` — arbitrary code execution
- `pickle.loads()` in model serialization pipelines
- Prompt injection in LLM-based applications
- Model poisoning via untrusted training data

---

## Severity Matrix

| Confidence \ Severity | LOW | MEDIUM | HIGH |
|----------------------|-----|--------|------|
| **HIGH** | Info | Medium | Critical |
| **MEDIUM** | Low | Medium | High |
| **LOW** | Info | Low | Medium |

---

## Report Format

For each finding, report:

```
### [B-ID]: [Check Name]

**Severity**: [LOW/MEDIUM/HIGH/CRITICAL]
**Confidence**: [LOW/MEDIUM/HIGH]
**File**: [path]:[line]

**Vulnerable Code**:
[show the code]

**Data Flow**:
[source] → [intermediaries] → [sink]

**Impact**: [what an attacker achieves]
**Remediation**: [specific fix with code example]
**Bandit Reference**: B[xxx]
```

---

## Tooling Constraints

Use ONLY:
- `view_file` — read source code
- `grep_search` — find patterns across the codebase

Do NOT use any terminal commands.
