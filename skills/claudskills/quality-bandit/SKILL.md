---
name: quality-bandit
triggers:
  - "quality bandit"
description: Bandit 보안 검사 설정 및 관리 스킬. pyproject.toml에 Bandit 설정을 구성하고 보안 취약점을 탐지한다. OWASP, CWE 기반의 보안 검사 환경을 구축한다.
argument-hint: "[init|scan|report] - Bandit 설정 작업"
disable-model-invocation: false
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
model: claude-sonnet-4-6[1m]
context: Bandit 보안 검사 설정 및 관리를 담당한다. pyproject.toml 설정 최적화, 테스트 ID 관리, CWE 매핑을 수행한다.
agent: Bandit 보안 검사 전문가. 프로젝트의 보안 취약점을 탐지하고, 적절한 규칙 세트를 구성한다.
hooks:
  pre_execution: []
  post_execution: []
category: 품질 관리
skill-type: Atomic
references: []
referenced-by:
  - "@skills/setup-quality/SKILL.md"

---
# Bandit 보안 검사 관리

Bandit 보안 검사 환경을 구성하고 관리한다.

## 목적

- Bandit 보안 검사 환경 설정
- 프로젝트별 보안 규칙 최적화
- CWE/OWASP 매핑 관리
- CI/CD 통합

## 사용법

```
/quality-bandit init      # 초기 설정
/quality-bandit scan      # 보안 검사 실행
/quality-bandit report    # 상세 보고서 생성
```

---

## 표준 설정

### pyproject.toml

```toml
# =============================================================================
# Bandit Configuration
# Documentation: https://bandit.readthedocs.io/en/latest/config.html
# =============================================================================

[tool.bandit]
# 검사 대상
targets = ["src"]

# 제외 디렉토리
exclude_dirs = [
    "tests",
    "docs",
    ".venv",
    "build",
    "dist",
]

# 건너뛸 테스트 ID
skips = [
    "B101",  # assert 사용 (테스트에서 필요)
]

# 심각도 필터 (LOW, MEDIUM, HIGH)
# severity = "MEDIUM"

# 신뢰도 필터 (LOW, MEDIUM, HIGH)
# confidence = "MEDIUM"
```

---

## 테스트 ID 및 CWE 매핑

### 주요 테스트 ID

| ID | 설명 | CWE | 심각도 |
|----|------|-----|--------|
| B101 | assert 사용 | CWE-703 | Low |
| B102 | exec 사용 | CWE-78 | Medium |
| B103 | bad file permissions | CWE-732 | Medium |
| B104 | hardcoded bind address | CWE-605 | Medium |
| B105 | hardcoded password | CWE-259 | Low |
| B106 | hardcoded password in function | CWE-259 | Low |
| B107 | hardcoded password default | CWE-259 | Low |
| B108 | hardcoded temp directory | CWE-377 | Medium |
| B110 | try-except-pass | CWE-703 | Low |
| B112 | try-except-continue | CWE-703 | Low |

### 암호화 관련

| ID | 설명 | CWE | 심각도 |
|----|------|-----|--------|
| B303 | MD5 사용 | CWE-327 | Medium |
| B304 | DES 사용 | CWE-327 | High |
| B305 | cipher weak mode | CWE-327 | Medium |
| B306 | mktemp 사용 | CWE-377 | Medium |
| B307 | eval 사용 | CWE-78 | Medium |
| B308 | mark_safe 사용 | CWE-79 | Medium |
| B311 | random (보안용 아님) | CWE-330 | Low |
| B312 | telnetlib 사용 | CWE-319 | High |
| B313-B320 | XML 관련 취약점 | CWE-611 | Medium |

### 인젝션 관련

| ID | 설명 | CWE | 심각도 |
|----|------|-----|--------|
| B601 | paramiko call | CWE-78 | Medium |
| B602 | subprocess_popen_with_shell | CWE-78 | High |
| B603 | subprocess_without_shell_equals_true | CWE-78 | Low |
| B604 | any_other_function_with_shell | CWE-78 | Medium |
| B605 | start_process_with_a_shell | CWE-78 | High |
| B606 | start_process_with_no_shell | CWE-78 | Low |
| B607 | start_process_with_partial_path | CWE-78 | Low |
| B608 | hardcoded_sql_expressions | CWE-89 | Medium |
| B609 | linux_commands_wildcard_injection | CWE-78 | High |
| B610 | django_extra_used | CWE-89 | Medium |
| B611 | django_rawsql_used | CWE-89 | Medium |

---

## 실행 명령

### 기본 검사

```bash
# 기본 검사
uv run bandit -r src/

# 설정 파일 사용
uv run bandit -c pyproject.toml -r src/

# 특정 테스트만
uv run bandit -r src/ -t B602,B608

# 특정 테스트 제외
uv run bandit -r src/ -s B101
```

### 출력 형식

```bash
# JSON 출력
uv run bandit -r src/ -f json -o bandit-report.json

# HTML 출력
uv run bandit -r src/ -f html -o bandit-report.html

# SARIF 출력 (GitHub 통합)
uv run bandit -r src/ -f sarif -o bandit-report.sarif
```

### 심각도/신뢰도 필터

```bash
# HIGH 심각도만
uv run bandit -r src/ -ll

# MEDIUM 이상
uv run bandit -r src/ -l

# 높은 신뢰도만
uv run bandit -r src/ -ii
```

---

## 프로젝트 유형별 설정

### 1. 웹 애플리케이션 (Django/FastAPI)

```toml
[tool.bandit]
targets = ["src"]
exclude_dirs = ["tests", "migrations"]
skips = ["B101"]

# 특별히 주의할 테스트
# B308: mark_safe (XSS)
# B608: SQL injection
# B610, B611: Django ORM injection
```

### 2. CLI 도구

```toml
[tool.bandit]
targets = ["src"]
exclude_dirs = ["tests"]
skips = [
    "B101",
    "B603",  # subprocess 사용 필요
    "B607",  # partial path 허용
]
```

### 3. Data Science

```toml
[tool.bandit]
targets = ["src"]
exclude_dirs = ["tests", "notebooks"]
skips = [
    "B101",
    "B311",  # random 사용 (ML에서 필요)
]
```

---

## 코드 내 억제

### 라인 수준

```python
subprocess.call(cmd, shell=True)  # nosec B602
```

### 블록 수준

```python
# nosec
def legacy_function():
    # 보안 검사 건너뜀
    pass
```

### 특정 테스트만 억제

```python
eval(user_input)  # nosec B307
```

---

## CI/CD 통합

### GitHub Actions

```yaml
# .github/workflows/security.yml
name: Security Check

on:
  pull_request:
  push:
    branches: [main]

jobs:
  bandit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install bandit
        run: pip install bandit[toml]

      - name: Run bandit
        run: bandit -c pyproject.toml -r src/ -f sarif -o bandit.sarif

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: bandit.sarif
```

### Pre-commit

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/PyCQA/bandit
  rev: 1.8.2
  hooks:
    - id: bandit
      args: ['-c', 'pyproject.toml', '-r', 'src']
      additional_dependencies: ['bandit[toml]']
      stages: [pre-push]
```

---

## 보안 취약점 분류

### OWASP Top 10 매핑

| OWASP | Bandit 테스트 |
|-------|--------------|
| A01 Broken Access Control | B103 |
| A02 Cryptographic Failures | B303, B304, B305 |
| A03 Injection | B602, B608, B609 |
| A05 Security Misconfiguration | B104, B108 |
| A07 Identification Failures | B105, B106, B107 |

### 심각도별 대응

| 심각도 | 대응 |
|--------|------|
| HIGH | 즉시 수정 필요 |
| MEDIUM | 릴리스 전 수정 |
| LOW | 검토 후 결정 |

---

## 일반 취약점 및 수정

### 1. Hardcoded Password (B105-B107)

**문제**:
```python
password = "secretpassword"
```

**수정**:
```python
import os
password = os.environ.get("PASSWORD")
```

### 2. SQL Injection (B608)

**문제**:
```python
query = f"SELECT * FROM users WHERE id = {user_id}"
```

**수정**:
```python
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

### 3. Shell Injection (B602)

**문제**:
```python
subprocess.call(f"ls {user_input}", shell=True)
```

**수정**:
```python
subprocess.call(["ls", user_input], shell=False)
```

### 4. Weak Crypto (B303)

**문제**:
```python
import hashlib
hashlib.md5(password.encode())
```

**수정**:
```python
import hashlib
hashlib.sha256(password.encode())
```

---

## 관련 스킬

| 스킬 | 역할 |
|------|------|
| [@skills/quality-precommit/SKILL.md] | Pre-commit hook 설정 |
| [@skills/quality-ruff/SKILL.md] | Ruff 린터 설정 |
| [@skills/quality-mypy/SKILL.md] | mypy 타입 검사 |
| [@skills/check-python-style/SKILL.md] | 코드 스타일 검증 |

---

## Changelog

| 날짜 | 버전 | 변경 내용 |
|------|------|----------|
| 2026-01-21 | 1.0.0 | 초기 생성 - Bandit 보안 검사 관리 |

## Gotchas (실패 포인트)

- False positive 많음 — `# nosec` 주석은 이유 주석과 함께 사용
- `B104` (hardcoded bind all interfaces) — 개발환경 0.0.0.0은 의도적일 수 있음
- `B101` (assert) — pytest에서 assert 사용은 정상, `tests/` 경로 제외 설정 권장
- severity/confidence 임계값을 팀 기준으로 통일하지 않으면 CI 결과 불일치
