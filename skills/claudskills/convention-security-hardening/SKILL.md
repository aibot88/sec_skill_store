---
name: convention-security-hardening
triggers:
  - "convention security hardening"
description: "보안 강화(Security Hardening) 컨벤션 참조 스킬. 입력 검증, SQL injection 방지, XSS 방지, 암호화, 권한 관리 등 프로덕션 배포 전 필수 보안 조치를 제공한다."
argument-hint: "[영역] - input, sql, web, auth, crypto, all"
disable-model-invocation: false
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
model: claude-sonnet-4-6[1m]
context: |
  프로덕션 환경의 보안 취약점을 사전에 방지하는 가이드를 제공한다.
  OWASP Top 10, CWE 기반의 실질적인 보안 조치를 제시한다.
agent: |
  보안 전문가.
  입력 검증부터 권한 관리까지 체계적인 보안 강화 전략을 제시한다.
hooks:
  pre_execution: []
  post_execution: []
category: 컨벤션 참조
skill-type: Atomic
references: []
referenced-by: []

---
# 보안 강화(Security Hardening) 컨벤션

프로덕션 배포 전 필수 보안 조치.

## 목적

- OWASP Top 10 취약점 방지
- 입력 검증 및 정제
- 데이터 보호 (암호화)
- 접근 제어 (권한 관리)
- 감시 및 로깅

## 사용법

```
/convention-security-hardening [영역]
```

| 영역 | 설명 |
|------|------|
| `input` | 입력 검증 및 정제 |
| `sql` | SQL Injection 방지 |
| `web` | XSS, CSRF 방지 |
| `auth` | 인증 및 권한 관리 |
| `crypto` | 암호화 및 해싱 |
| `all` | 전체 (기본값) |

---

## 1. 입력 검증 (Input Validation)

### 1.1 기본 원칙

**규칙**: 모든 외부 입력을 신뢰하지 않는다 (Whitelist 방식)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""보안 강화 검증 모듈.

Author: taeyang lee
Created: 2026-01-21 16:00(KST, UTC+09:00)
Modified: 2026-01-21 16:00(KST, UTC+09:00)
Version: 1.0.0
"""

import re
from typing import Any
import logging

logger = logging.getLogger(__name__)


def validate_email(email: str) -> bool:
    """이메일 형식을 검증한다.

    Args:
        email (str): 검증할 이메일 주소.

    Returns:
        bool: 유효하면 True, 아니면 False.

    Logics:
        1. 이메일 길이 확인 (최대 254자).
        2. 정규표현식으로 형식 검증.
        3. 실제 메일 서버 존재 확인 (선택).

    Example:
        >>> validate_email('user@example.com')
        True
        >>> validate_email('invalid-email')
        False
    """
    # 길이 확인
    if not email or len(email) > 254:
        return False

    # 정규표현식 (RFC 5322 간소화)
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(pattern, email):
        return False

    logger.info(f"유효한 이메일: {email}")
    return True


def sanitize_string(
    value: str,
    max_length: int = 256,
    allowed_chars: str = r'^[a-zA-Z0-9\s\-_.]*$',
) -> str:
    """문자열을 정제(sanitize)한다.

    Args:
        value (str): 정제할 문자열.
        max_length (int): 최대 길이. 기본값 256.
        allowed_chars (str): 허용 문자 정규표현식.

    Returns:
        str: 정제된 문자열.

    Raises:
        ValueError: 검증 실패 시 발생.

    Logics:
        1. Whitelist 방식으로 허용 문자만 추출.
        2. 길이 제한 적용.
        3. 위험 문자 제거 (스크립트 태그 등).

    Example:
        >>> sanitize_string('<script>alert(1)</script>')
        ''  # 스크립트 태그 제거
    """
    if not isinstance(value, str):
        raise ValueError("입력은 문자열이어야 함")

    # 위험 문자 제거
    value = value.strip()

    # Whitelist 방식 필터링
    if not re.match(allowed_chars, value):
        raise ValueError(
            f"허용되지 않는 문자 포함: {value}"
        )

    # 길이 제한
    if len(value) > max_length:
        raise ValueError(
            f"길이 초과: {len(value)} > {max_length}"
        )

    logger.info(f"정제됨: {value}")
    return value
```

### 1.2 Pydantic을 이용한 검증

```python
from pydantic import BaseModel, EmailStr, constr, Field


class UserInput(BaseModel):
    """사용자 입력 검증 스키마.

    Pydantic으로 입력값 자동 검증.
    """

    # 이메일: 유효한 형식 필수
    email: EmailStr

    # 이름: 3~50자, 문자와 공백만
    name: constr(min_length=3, max_length=50,
                 regex=r'^[a-zA-Z\s]+$')

    # 나이: 18~120
    age: int = Field(ge=18, le=120)

    # 전화번호: 형식 검증
    phone: constr(regex=r'^\d{10,11}$')

    class Config:
        # 여분 필드 거부
        extra = 'forbid'


def process_user_input(data: dict) -> UserInput:
    """사용자 입력을 검증하고 처리한다.

    Args:
        data (dict): 입력 데이터.

    Returns:
        UserInput: 검증된 데이터.

    Raises:
        ValidationError: 검증 실패 시.

    Logics:
        1. Pydantic 모델로 검증.
        2. 실패하면 ValidationError 발생.
        3. 검증 통과시 안전한 데이터 반환.

    Example:
        >>> process_user_input({
        ...     'email': 'user@example.com',
        ...     'name': 'John Doe',
        ...     'age': 25,
        ...     'phone': '01012345678'
        ... })
        # UserInput 객체 반환
    """
    try:
        validated = UserInput(**data)
        logger.info(f"입력 검증 성공: {validated}")
        return validated
    except Exception as e:
        logger.error(f"입력 검증 실패: {e}")
        raise
```

---

## 2. SQL Injection 방지

### 2.1 Parameterized Query (매개변수화 쿼리)

**규칙**: 절대 문자열 연결로 쿼리 작성 금지

```python
import psycopg2
from psycopg2 import sql


def find_user_safe(
    connection,
    email: str,
) -> dict:
    """SQL Injection을 방지하면서 사용자를 찾는다.

    Args:
        connection: DB 연결.
        email (str): 찾을 이메일.

    Returns:
        dict: 사용자 정보.

    Logics:
        1. Parameterized query 사용.
        2. 플레이스홀더(?)에 값 주입.
        3. DB 드라이버가 자동 이스케이프.

    Example:
        >>> # ❌ 나쁜 예 (SQL Injection 취약)
        >>> query = f"SELECT * FROM users WHERE email='{email}'"
        >>> # ✅ 좋은 예 (안전)
        >>> query = "SELECT * FROM users WHERE email=%s"
        >>> cursor.execute(query, (email,))
    """
    # ✅ 올바른 방법: Parameterized query
    cursor = connection.cursor()

    query = sql.SQL(
        "SELECT id, email, name FROM users WHERE email=%s"
    )

    try:
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            return {
                'id': result[0],
                'email': result[1],
                'name': result[2]
            }
        else:
            return None

    except Exception as e:
        logger.error(f"DB 조회 오류: {e}")
        raise

    finally:
        cursor.close()


# ❌ 절대 금지 (SQL Injection 취약)
def find_user_unsafe(connection, email: str):
    """위험한 쿼리 작성 (절대 금지)"""
    cursor = connection.cursor()

    # 이 방법은 SQL Injection 취약점 발생!
    query = f"SELECT * FROM users WHERE email='{email}'"

    cursor.execute(query)
    return cursor.fetchone()
```

**SQL Injection 예시**:
```python
# 정상 입력
email = "user@example.com"
# 쿼리: SELECT * FROM users WHERE email='user@example.com'

# 공격자 입력
email = "' OR '1'='1"
# 쿼리: SELECT * FROM users WHERE email='' OR '1'='1'
# → 모든 사용자 조회 (심각!)
```

---

## 3. XSS (Cross-Site Scripting) 방지

### 3.1 HTML 이스케이핑

**규칙**: 사용자 입력을 HTML에 렌더링하기 전에 이스케이프

```python
from markupsafe import escape
import html


def render_user_comment(
    comment: str,
) -> str:
    """사용자 댓글을 안전하게 렌더링한다.

    Args:
        comment (str): 원본 댓글.

    Returns:
        str: 이스케이프된 HTML.

    Logics:
        1. HTML 특수 문자를 엔티티로 변환.
        2. 스크립트 태그 무효화.
        3. 안전한 HTML 생성.

    Example:
        >>> render_user_comment('<script>alert(1)</script>')
        '&lt;script&gt;alert(1)&lt;/script&gt;'
    """
    # ❌ 위험 (XSS 취약)
    # html_output = f"<p>{comment}</p>"

    # ✅ 안전 (이스케이프)
    safe_comment = escape(comment)
    html_output = f"<p>{safe_comment}</p>"

    return html_output


# 예시
comment = '<script>alert("XSS Attack")</script>'
safe_html = render_user_comment(comment)
print(safe_html)
# 출력: <p>&lt;script&gt;alert(&quot;XSS Attack&quot;)&lt;/script&gt;</p>
```

### 3.2 CSRF (Cross-Site Request Forgery) 방지

**웹 프로젝트에서 필수**

```python
from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = 'your-secret-key'


@app.route('/form', methods=['GET'])
def show_form():
    """CSRF 토큰을 포함한 폼을 표시한다.

    Logics:
        1. 세션에 CSRF 토큰 생성.
        2. 폼에 숨겨진 필드로 토큰 포함.
        3. POST 시 토큰 검증.
    """
    from uuid import uuid4

    # CSRF 토큰 생성 (없으면)
    if '_csrf_token' not in session:
        session['_csrf_token'] = str(uuid4())

    return f"""
    <form method="POST" action="/submit">
        <input type="hidden" name="_csrf_token"
               value="{session['_csrf_token']}">
        <input type="text" name="data">
        <button type="submit">제출</button>
    </form>
    """


@app.route('/submit', methods=['POST'])
def submit_form():
    """CSRF 토큰을 검증한 후 처리한다.

    Logics:
        1. 요청의 토큰 추출.
        2. 세션의 토큰과 비교.
        3. 일치하면 처리, 아니면 거부.
    """
    token = request.form.get('_csrf_token')

    # ✅ CSRF 검증
    if token != session.get('_csrf_token'):
        return "CSRF 토큰 불일치", 403

    # 안전하게 처리
    data = request.form.get('data')
    return f"처리됨: {escape(data)}"
```

---

## 4. 인증 & 권한 관리 (Authentication & Authorization)

### 4.1 비밀번호 해싱

**규칙**: 비밀번호는 평문으로 저장하지 않는다

```python
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt


def hash_password_safe(
    password: str,
    method: str = 'bcrypt',
) -> str:
    """비밀번호를 안전하게 해싱한다.

    Args:
        password (str): 평문 비밀번호.
        method (str): 해싱 방법 ('bcrypt', 'scrypt', 'pbkdf2').

    Returns:
        str: 해싱된 비밀번호.

    Logics:
        1. Bcrypt 또는 scrypt 사용 (느린 알고리즘 권장).
        2. Salt 자동 포함.
        3. 반복 횟수 설정 (기본 12).

    Example:
        >>> hashed = hash_password_safe('MyPassword123!')
        >>> # 저장: UPDATE users SET password=hashed
    """
    if method == 'bcrypt':
        # Bcrypt: 가장 안전한 방법
        hashed = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt(rounds=12)  # 12 라운드
        ).decode('utf-8')
    else:
        # werkzeug (Django 호환)
        hashed = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=16
        )

    return hashed


def verify_password(
    password: str,
    hashed: str,
) -> bool:
    """입력한 비밀번호가 해시된 비밀번호와 일치하는지 확인.

    Args:
        password (str): 입력 비밀번호.
        hashed (str): 저장된 해시.

    Returns:
        bool: 일치하면 True.

    Logics:
        1. 입력 비밀번호를 같은 방식으로 해싱.
        2. 해시 비교 (시간 공격 방지).
    """
    try:
        # Bcrypt 검증
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed.encode('utf-8')
        )
    except Exception:
        # 대체: werkzeug 검증
        return check_password_hash(hashed, password)
```

### 4.2 JWT 기반 토큰 인증

```python
from datetime import datetime, timedelta
import jwt


def create_jwt_token(
    user_id: int,
    email: str,
    secret_key: str,
    expires_in: int = 3600,  # 1시간
) -> str:
    """JWT 토큰을 생성한다.

    Args:
        user_id (int): 사용자 ID.
        email (str): 사용자 이메일.
        secret_key (str): 서명 키 (환경 변수에서).
        expires_in (int): 만료 시간 (초).

    Returns:
        str: JWT 토큰.

    Logics:
        1. 페이로드 생성 (user_id, email, exp).
        2. HS256으로 서명.
        3. 토큰 반환.
    """
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(
            seconds=expires_in
        ),
        'iat': datetime.utcnow()
    }

    token = jwt.encode(
        payload,
        secret_key,
        algorithm='HS256'
    )

    return token


def verify_jwt_token(
    token: str,
    secret_key: str,
) -> dict:
    """JWT 토큰을 검증한다.

    Args:
        token (str): JWT 토큰.
        secret_key (str): 서명 키.

    Returns:
        dict: 페이로드 (user_id, email 등).

    Raises:
        jwt.InvalidTokenError: 토큰 무효 시.

    Logics:
        1. 토큰 서명 검증.
        2. 만료 시간 확인.
        3. 페이로드 반환.
    """
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("토큰 만료됨")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"토큰 무효: {e}")
```

---

## 5. 암호화 (Encryption)

### 5.1 민감한 데이터 암호화

```python
from cryptography.fernet import Fernet
import os


def encrypt_sensitive_data(
    data: str,
    key: str = None,
) -> str:
    """민감한 데이터를 암호화한다.

    Args:
        data (str): 암호화할 데이터.
        key (str): 암호화 키 (없으면 환경변수에서).

    Returns:
        str: 암호화된 데이터 (Base64).

    Logics:
        1. 키 생성 또는 로드.
        2. Fernet으로 대칭 암호화.
        3. 암호문 반환.

    Example:
        >>> encrypted = encrypt_sensitive_data('user_ssn')
        >>> # 저장: UPDATE users SET ssn=encrypted
    """
    if not key:
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            # 키 생성 (첫 실행 시만)
            key = Fernet.generate_key().decode()
            print(f"생성된 키: {key}")

    cipher = Fernet(key.encode())
    encrypted = cipher.encrypt(data.encode())

    return encrypted.decode()


def decrypt_sensitive_data(
    encrypted_data: str,
    key: str = None,
) -> str:
    """암호화된 데이터를 복호화한다.

    Args:
        encrypted_data (str): 암호화된 데이터.
        key (str): 암호화 키.

    Returns:
        str: 평문 데이터.
    """
    if not key:
        key = os.getenv('ENCRYPTION_KEY')

    cipher = Fernet(key.encode())
    decrypted = cipher.decrypt(encrypted_data.encode())

    return decrypted.decode()
```

---

## 6. 보안 체크리스트

구현 후 다음을 확인하세요:

### 프로덕션 배포 전

- [ ] 모든 입력 검증 (Whitelist 방식)
- [ ] SQL Injection 방지 (Parameterized query)
- [ ] XSS 방지 (HTML escape)
- [ ] CSRF 방지 (토큰 검증)
- [ ] 비밀번호 해싱 (Bcrypt/scrypt)
- [ ] HTTPS 필수
- [ ] 비밀키 환경 변수 관리
- [ ] 에러 메시지 최소화 (민감정보 노출 방지)
- [ ] 로깅 보안 감시 활성화
- [ ] Bandit 보안 검사 통과

### 지속적 모니터링

- [ ] 비정상 로그인 감지
- [ ] API 속도 제한 (Rate limiting)
- [ ] 권한 변경 감시
- [ ] 정기 보안 감사

---

## 관련 스킬

| 스킬 | 역할 |
|------|------|
| [@skills/quality-bandit/SKILL.md] | 보안 검사 자동화 |
| [@skills/convention-logging/SKILL.md] | 보안 로깅 |
| [@skills/check-security/SKILL.md] | 보안 취약점 검증 |

---

## 참고

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CWE Top 25: https://cwe.mitre.org/top25/
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework/

---

## Changelog

| 날짜 | 버전 | 변경 내용 |
|------|------|----------|
| 2026-01-21 | 1.0.0 | 초기 생성 - 입력 검증, SQL injection, XSS, 인증, 암호화 |

## Gotchas (실패 포인트)

- SQL injection: f-string으로 쿼리 조합 절대 금지 — parameterized query 사용
- XSS: 사용자 입력을 HTML에 직접 삽입 금지
- secrets를 환경 변수 대신 코드에 하드코딩 시 git history에 영구 기록
- HTTPS 없는 API 엔드포인트에 인증 토큰 전송 금지
