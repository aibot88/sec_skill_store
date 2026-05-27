---
name: tooling-python
description: "Python audit tooling: ruff (linting), mypy (types), bandit (SAST), pip-audit (CVEs), radon (complexity), vulture (dead code), mutmut (mutations). Use during audit phases for Python projects."
---

# Python Audit Tooling

Запуск SAST/quality tools для Python проектов.

## Когда применять

- В audit phases для Python проектов
- После того как `language-detector` определил Python в проекте
- Tools проверены на наличие через `command -v <tool>`

## Tools

### Ruff (linting)

```bash
ruff check . --output-format=json > /tmp/ruff.json 2>/dev/null
```

Установка если нет: `pip install ruff` (recommended) или через `pre-commit`.

Парсить:
- Errors (severity: HIGH-MEDIUM зависит от rule)
- Warnings (severity: LOW)
- Style issues (можно skip если есть formatter)

### MyPy (types)

```bash
mypy --no-incremental --strict --json-report /tmp/mypy-report . 2>/dev/null
```

Если strict ломает - попробовать без `--strict`:
```bash
mypy . --json-report /tmp/mypy-report 2>/dev/null
```

Findings по severity:
- `error` codes - HIGH/MEDIUM
- `note` codes - LOW

Common issues:
- Untyped function definitions in core modules
- `Any` types где должны быть конкретные
- Missing return type annotations

### Bandit (SAST)

```bash
bandit -r src/ -f json -o /tmp/bandit.json --skip B101 2>/dev/null
```

`--skip B101` пропускает `assert_used` - common false positive в Django.

Severity mapping:
- `HIGH` confidence + `HIGH` severity → CRITICAL
- `HIGH` + `MEDIUM` → HIGH
- `MEDIUM` + `MEDIUM` → MEDIUM
- Lower → LOW

Common findings:
- `subprocess_popen_with_shell_equals_true` (B602) - command injection
- `request_without_timeout` (B113)
- `hardcoded_password_string` (B105)

### Pip-audit (CVE check)

```bash
pip-audit --format=json --output=/tmp/pip-audit.json 2>/dev/null
```

Альтернатива: `safety check --json`

Парсить:
- Critical CVEs (CVSS >= 9.0) → BLOCKER (если в production deps)
- High CVEs → CRITICAL
- Medium → HIGH/MEDIUM
- Cross-reference с CISA KEV если возможно

### Radon (complexity)

```bash
# Cyclomatic complexity
radon cc -j -s . > /tmp/radon-cc.json 2>/dev/null

# Maintainability index
radon mi -j . > /tmp/radon-mi.json 2>/dev/null

# Halstead metrics  
radon hal -j . > /tmp/radon-hal.json 2>/dev/null
```

CC thresholds:
- A (1-5): excellent
- B (6-10): good
- C (11-20): acceptable
- D (21-30): high (HIGH finding)
- E (31-40): very high (CRITICAL finding)
- F (40+): critical (BLOCKER finding в hot path)

### Vulture (dead code)

```bash
vulture src/ --min-confidence 80 > /tmp/vulture.txt 2>/dev/null
```

`--min-confidence 80` - чтобы избежать false positives. Vulture часто триггерится на:
- Django ORM relations (used through introspection)
- Pytest fixtures (used by test runner)
- Click command handlers

Use confidence >= 80% only.

### Mutmut (mutation testing - DEEP MODE ONLY)

**Внимание**: медленный (часы для крупного проекта).

```bash
# Setup
mutmut run --paths-to-mutate=src/ --runner='pytest -x'

# Results
mutmut results > /tmp/mutmut-results.txt
mutmut html  # creates html/index.html
```

В deep mode:
- Запускать только на критичных модулях (не всё проект)
- Спросить пользователя подтверждение перед запуском (estimate time first)
- Если timeout > 4 hours - skip и пометить incomplete

### Detect-secrets

```bash
detect-secrets scan --all-files > /tmp/secrets-baseline.json
```

Если базовая история проекта содержит секреты - они попадут в `secrets-baseline.json`. Reviewer должен пересмотреть baseline манyally.

## Output

Сырые outputs в `docs/audit/<TS>/<phase>/tooling-output/python/`.

Парсинг JSON outputs в findings формате (см. `templates/finding.schema.json`).

## Tool unavailability

Если tool не установлен - **не падать**, документировать missing tool в audit report:

```markdown
## Missing tools (Python)

The following tools were not available; coverage of Python audit was reduced:

- bandit: not installed (`pip install bandit`)
- mutmut: not installed; mutation testing skipped
```

## Specific Django/DRF checks

Для Django проектов дополнительно:

```bash
# Django check command
python manage.py check --deploy 2>/dev/null

# Django security check
python manage.py check --tag security 2>/dev/null
```

Эти commands выявляют:
- DEBUG = True в production
- Missing security middleware
- Insecure SECRET_KEY
- HSTS settings

## Environment isolation

Если проект использует virtual env:
- `.venv/` или `venv/` - стандартные пути
- Активировать перед запуском tools (`source .venv/bin/activate`)
- Tools должны видеть установленные dependencies проекта (pip-audit, mypy особенно)
