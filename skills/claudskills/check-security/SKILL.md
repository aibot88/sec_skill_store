---
name: check-security
triggers:
  - "check security"
description: 코드 보안 취약점을 탐지한다. bandit을 사용하여 일반적인 보안 이슈를 검사한다.
argument-hint: "[path] [--severity high|medium|low] - 검사 경로, 최소 심각도"
disable-model-invocation: false
user-invocable: false
allowed-tools:
  - Bash
  - Read
  - Glob
model: claude-sonnet-4-6[1m]
context: Python 코드 보안 검사 스킬이다. bandit을 사용하여 정적 보안 분석을 수행한다.
agent: 당신은 애플리케이션 보안 전문가입니다. OWASP Top 10과 Python 보안 베스트 프랙티스에 정통합니다.
hooks:
  pre_execution: []
  post_execution: []
category: 코드 검증
skill-type: Atomic
references: []
referenced-by:
  - "@skills/code-review/SKILL.md"

---
# check-security

코드 보안 취약점을 탐지하는 스킬.

## 목적

- 보안 취약점 탐지 (bandit)
- 심각도 분류 (HIGH/MEDIUM/LOW)
- CWE 매핑 및 수정 가이드 제공

## 사용법

```
/check-security                          # 전체 코드베이스 검사
/check-security src/                     # 특정 경로 검사
/check-security src/ --severity high     # HIGH만 검사
```

## 검증 규칙

> **상세 규칙**: [@skills/convention-security-hardening/SKILL.md] 스킬 참조 (`@.claude/skills/convention-security-hardening/SKILL.md`)
>
> 이 스킬은 검증 실행 시 [@skills/convention-security-hardening/SKILL.md] 파일을 읽어 최신 규칙을 적용한다.

### 주요 탐지 항목 요약

| 취약점 | Bandit ID | CWE | 심각도 |
|--------|-----------|-----|--------|
| 하드코딩된 비밀번호 | B105, B106 | CWE-259 | HIGH |
| SQL Injection | B608 | CWE-89 | HIGH |
| 안전하지 않은 pickle | B301 | CWE-502 | HIGH |
| exec/eval 사용 | B102, B307 | CWE-78 | MEDIUM |
| 안전하지 않은 해시 (MD5, SHA1) | B303, B324 | CWE-328 | MEDIUM |
| assert 사용 | B101 | CWE-703 | LOW |

## 프로세스

```
/check-security [path]
    |
    v
[Step 1] bandit 설치 확인
    |-- uv pip list | grep bandit
    |-- (없으면) uv pip install bandit
    |
    v
[Step 2] bandit 실행
    |-- bandit -r [path] -f json
    |-- JSON 결과 수집
    |
    v
[Step 3] 결과 파싱
    |-- 심각도 분류 (HIGH/MEDIUM/LOW)
    |-- CWE 매핑
    |
    v
[Step 4] 수정 가이드 추가
    |-- 각 이슈별 권장사항
    |-- 코드 예시 제공
    |
    v
완료
```

## 예제

### 기본 검사

```
User: /check-security src/

Claude:
=== Security Check: src/ ===

[1/2] bandit 실행 중...
> bandit -r src/ -f json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[HIGH] 보안 이슈
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

B105: Hardcoded password
  src/core/config.py:15
  > secret_key = "my_secret_password"

  CWE-259: Use of Hard-coded Password

  Fix: 환경변수로 이동
  ```python
  # Before
  secret_key = "my_secret_password"

  # After
  import os
  secret_key = os.environ.get("SECRET_KEY")
  ```

---

B608: SQL Injection
  src/db/queries.py:23
  > query = f"SELECT * FROM users WHERE id = {user_id}"

  CWE-89: Improper Neutralization of SQL

  Fix: 파라미터화된 쿼리 사용
  ```python
  # Before
  query = f"SELECT * FROM users WHERE id = {user_id}"

  # After
  query = "SELECT * FROM users WHERE id = %s"
  cursor.execute(query, (user_id,))
  ```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[MEDIUM] 보안 이슈
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

B303: Use of insecure MD5 hash
  src/utils/hash.py:8
  > hashlib.md5(data)

  CWE-328: Use of Weak Hash

  Fix: SHA-256 이상 사용
  ```python
  # Before
  hashlib.md5(data)

  # After
  hashlib.sha256(data)
  ```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
요약
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| 심각도 | 개수 |
|--------|------|
| HIGH | 2 |
| MEDIUM | 1 |
| LOW | 0 |

총 3개 보안 이슈 탐지

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
다음 단계
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. HIGH 이슈 즉시 수정 (배포 전 필수)
2. MEDIUM 이슈 수정 권장
3. /quality-bandit setup으로 CI 통합 권장
```

### HIGH만 검사

```
User: /check-security src/ --severity high

Claude:
=== Security Check: src/ (HIGH only) ===

> bandit -r src/ -f json -ll

[HIGH] 2개 이슈 탐지

B105: src/core/config.py:15
B608: src/db/queries.py:23

상세 내용은 기본 검사 참조
```

## 관련 스킬

| 스킬명 | 관계 | 설명 |
|--------|------|------|
| [@skills/code-review/SKILL.md] | 부모 (Composite) | 통합 코드 리뷰 |
| [@skills/quality-bandit/SKILL.md] | 연관 | bandit 설정 관리 |

## Changelog

| 날짜 | 버전 | 변경 내용 |
|------|------|----------|
| 2026-01-22 | 1.1.0 | convention-security-hardening 참조 방식으로 리팩토링 |
| 2026-01-21 | 1.0.0 | 초기 스킬 생성 |

## Gotchas (실패 포인트)

- SQL injection 탐지 시 ORM 사용 코드도 의심 — raw query 여부 확인 필수
- 환경 변수 주입 오탐 — 실제 하드코딩과 환경변수 참조 구분 필요
- bandit -r 없이 실행 시 서브디렉터리 미검사
- `HIGH` severity만 차단, `MEDIUM` 이하는 리뷰 후 결정 권장
