---
name: env-manager
description: |
  트리거: "환경변수 관리", "env 정리해줘", ".env 만들어줘", "환경변수 설정", "env 파일 생성",
  "시크릿 관리", "secrets manager", "vault", "doppler", "환경변수 검증", "env diff"
  수행: .env, .env.example, 환경변수 문서 일관 관리. 타입 검증 스크립트(Zod/pydantic), 시크릿 관리 도구 연동,
  Git hooks로 .env 커밋 방지, 환경별 diff 비교까지 포함한다.
  출력: .env.example, 검증 스크립트(TS/Python), .gitignore, pre-commit hook, 시크릿 관리 가이드
---
# Environment Variable Manager

## 목적
프로젝트의 환경변수를 체계적으로 관리한다. `.env.example`을 단일 진실 원천으로 유지하고,
환경별 파일 분리, 런타임 타입 검증, Git hook 기반 누출 방지, 시크릿 관리 도구 연동까지 제공한다.

---

## 실행 절차

1. **환경변수 목록 수집**: 코드베이스에서 `process.env.*` / `os.environ` / `getenv` 패턴 스캔
2. **카테고리 분류**: 앱 설정 / 데이터베이스 / 외부 API / 인증 / 인프라 그룹화
3. **민감도 분류**: PUBLIC (빌드 타임 노출 가능) / SECRET (런타임 전용) 구분
4. **`.env.example` 생성**: 주석 포함, 실제 값 없이 예시/설명만 기재
5. **환경별 `.env` 템플릿 생성**: development / staging / production 분리
6. **검증 스크립트 생성**: 앱 시작 전 필수 변수 존재 여부 + 타입 검사
7. **`.gitignore` 및 Git hook 설정**: `.env*` 커밋 방지 자동화
8. **시크릿 관리 도구 연동 가이드 제공** (필요 시)

---

## 출력 형식

### .env.example

```bash
# .env.example
# ============================================================
# 이 파일을 .env.local (개발) 또는 .env (프로덕션)으로 복사하세요.
# 실제 비밀값은 절대 이 파일에 커밋하지 마세요.
# 마지막 업데이트: 2024-01-15 | 담당: @devteam
# ============================================================

# ──────────────────────────────────────────────────────────────
# 앱 기본 설정
# ──────────────────────────────────────────────────────────────
NODE_ENV=development                    # development | staging | production
APP_NAME=MyApp                          # 앱 이름 (로그, 이메일 제목 등에 사용)
APP_URL=http://localhost:3000           # 외부 접근 URL (트레일링 슬래시 없음)
APP_PORT=3000                           # 서버 리스닝 포트
LOG_LEVEL=debug                         # error | warn | info | debug | trace

# ──────────────────────────────────────────────────────────────
# 데이터베이스 (PostgreSQL)
# ──────────────────────────────────────────────────────────────
DATABASE_URL=postgresql://user:password@localhost:5432/myapp_dev
DATABASE_POOL_MIN=2
DATABASE_POOL_MAX=10
DATABASE_POOL_IDLE_TIMEOUT=30000

# ──────────────────────────────────────────────────────────────
# Redis (캐시 / 세션)
# ──────────────────────────────────────────────────────────────
REDIS_URL=redis://localhost:6379
# REDIS_PASSWORD=                       # [SECRET] 프로덕션에서 필수
REDIS_TLS=false                         # 프로덕션에서는 true

# ──────────────────────────────────────────────────────────────
# 인증 / 보안
# ──────────────────────────────────────────────────────────────
JWT_SECRET=                             # [SECRET] 최소 32자 랜덤 문자열 필수
JWT_EXPIRES_IN=7d
SESSION_SECRET=                         # [SECRET] 최소 32자 랜덤 문자열 필수
BCRYPT_ROUNDS=12
ALLOWED_ORIGINS=http://localhost:3000   # CORS 허용 출처 (쉼표 구분)

# ──────────────────────────────────────────────────────────────
# 외부 서비스
# ──────────────────────────────────────────────────────────────
STRIPE_PUBLIC_KEY=pk_test_              # [PUBLIC] 클라이언트 노출 가능
STRIPE_SECRET_KEY=sk_test_             # [SECRET] 서버 전용
STRIPE_WEBHOOK_SECRET=whsec_           # [SECRET]
GOOGLE_CLIENT_ID=                       # [PUBLIC]
GOOGLE_CLIENT_SECRET=                   # [SECRET]
SENTRY_DSN=                             # 오류 추적
```

---

### 환경변수 검증 스크립트

#### TypeScript — Zod 기반

```ts
// src/lib/env.ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'staging', 'production']).default('development'),
  APP_URL: z.string().url(),
  APP_PORT: z.coerce.number().int().min(1).max(65535).default(3000),
  LOG_LEVEL: z.enum(['error', 'warn', 'info', 'debug', 'trace']).default('info'),

  DATABASE_URL: z.string().min(1, 'DATABASE_URL is required'),
  DATABASE_POOL_MIN: z.coerce.number().default(2),
  DATABASE_POOL_MAX: z.coerce.number().default(10),

  REDIS_URL: z.string().default('redis://localhost:6379'),

  JWT_SECRET: z.string().min(32, 'JWT_SECRET must be at least 32 characters'),
  JWT_EXPIRES_IN: z.string().default('7d'),
  SESSION_SECRET: z.string().min(32, 'SESSION_SECRET must be at least 32 characters'),
  BCRYPT_ROUNDS: z.coerce.number().min(10).max(14).default(12),

  STRIPE_SECRET_KEY: z.string().startsWith('sk_').optional(),
  GOOGLE_CLIENT_SECRET: z.string().optional(),
  SENTRY_DSN: z.string().url().optional(),
});

function validateEnv() {
  const result = envSchema.safeParse(process.env);
  if (!result.success) {
    const errors = result.error.issues
      .map((issue) => `  - ${issue.path.join('.')}: ${issue.message}`)
      .join('\n');
    console.error(`\n[ENV ERROR] 환경변수 검증 실패:\n${errors}\n`);
    process.exit(1);
  }
  return result.data;
}

export const env = validateEnv();
export type Env = typeof env;
```

#### Python — pydantic-settings 기반

```python
# src/config.py
from pydantic import AnyHttpUrl, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
    )

    APP_ENV: str = Field(default='development', pattern='^(development|staging|production)$')
    APP_URL: AnyHttpUrl = 'http://localhost:8000'
    APP_PORT: int = Field(default=8000, ge=1, le=65535)

    DATABASE_URL: str = Field(..., description='PostgreSQL connection string')
    REDIS_URL: str = 'redis://localhost:6379'

    JWT_SECRET: SecretStr = Field(..., min_length=32)
    JWT_EXPIRES_MINUTES: int = Field(default=10080)  # 7일

    STRIPE_SECRET_KEY: SecretStr | None = None
    SENTRY_DSN: AnyHttpUrl | None = None

    @field_validator('DATABASE_URL')
    @classmethod
    def validate_db_url(cls, v: str) -> str:
        if not v.startswith(('postgresql://', 'postgres://')):
            raise ValueError('DATABASE_URL must be a PostgreSQL URL')
        return v


settings = Settings()
```

---

### .gitignore 설정

```gitignore
# 환경변수 파일 (모든 .env 변형 제외)
.env
.env.local
.env.development
.env.development.local
.env.staging
.env.staging.local
.env.production
.env.production.local
.env.*.local

# .env.example은 커밋 대상 (실제 값 없음)
!.env.example
```

---

### Git Hook — .env 커밋 방지

```bash
# .git/hooks/pre-commit (또는 husky 설정)
#!/bin/sh
# .env 파일 커밋 방지 훅

FORBIDDEN_FILES=$(git diff --cached --name-only | grep -E '^\.env(\.[^e]|$)')

if [ -n "$FORBIDDEN_FILES" ]; then
  echo ""
  echo "❌ [보안 경고] .env 파일을 커밋하려 했습니다:"
  echo "$FORBIDDEN_FILES"
  echo ""
  echo ".env 파일에는 실제 시크릿이 포함될 수 있습니다."
  echo "커밋을 중단합니다. .env.example만 커밋하세요."
  echo ""
  exit 1
fi
```

**husky 설정 (package.json):**
```json
{
  "husky": {
    "hooks": {
      "pre-commit": "sh .git/hooks/pre-commit"
    }
  }
}
```

**lint-staged와 통합 (`.husky/pre-commit`):**
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# .env 커밋 방지
if git diff --cached --name-only | grep -qE '^\.env(\.[^e]|$)'; then
  echo "❌ .env 파일은 커밋할 수 없습니다. .env.example을 사용하세요."
  exit 1
fi

npx lint-staged
```

---

### 환경별 diff 비교

두 환경의 환경변수 키를 비교하여 누락된 변수를 탐지한다.

```bash
#!/bin/bash
# scripts/env-diff.sh
# 사용법: ./scripts/env-diff.sh .env.example .env.production

FILE_A=${1:-.env.example}
FILE_B=${2:-.env.local}

# 키만 추출 (값 제외, 주석 제외)
keys_a=$(grep -E '^[A-Z_]+=?' "$FILE_A" | cut -d= -f1 | sort)
keys_b=$(grep -E '^[A-Z_]+=?' "$FILE_B" | cut -d= -f1 | sort)

echo "=== $FILE_A에 있지만 $FILE_B에 없는 키 (누락) ==="
comm -23 <(echo "$keys_a") <(echo "$keys_b")

echo ""
echo "=== $FILE_B에 있지만 $FILE_A에 없는 키 (추가됨) ==="
comm -13 <(echo "$keys_a") <(echo "$keys_b")

echo ""
echo "=== 빈 값인 필수 변수 ($FILE_B) ==="
grep -E '^[A-Z_]+=$' "$FILE_B" | cut -d= -f1
```

---

### 시크릿 관리 도구 연동 가이드

#### AWS Secrets Manager
```bash
# 시크릿 저장
aws secretsmanager create-secret \
  --name "myapp/production/jwt-secret" \
  --secret-string "$(openssl rand -hex 32)"

# 앱에서 읽기 (Node.js)
import { SecretsManagerClient, GetSecretValueCommand } from "@aws-sdk/client-secrets-manager";

const client = new SecretsManagerClient({ region: "ap-northeast-2" });
const response = await client.send(new GetSecretValueCommand({
  SecretId: "myapp/production/jwt-secret",
}));
const secret = response.SecretString;
```

#### HashiCorp Vault
```bash
# 시크릿 저장
vault kv put secret/myapp/production \
  jwt_secret=$(openssl rand -hex 32) \
  db_password=mypassword

# 앱에서 읽기
vault kv get -field=jwt_secret secret/myapp/production
```

#### Doppler (권장 — 가장 간단)
```bash
# CLI 설치 및 연동
brew install dopplerhq/cli/doppler
doppler login
doppler setup  # 프로젝트 선택

# 환경변수 주입하여 실행
doppler run -- npm start
doppler run -- python manage.py runserver

# .env 파일로 내보내기
doppler secrets download --no-file --format env > .env.production
```

#### GitHub Actions Secrets 연동
```yaml
# .github/workflows/deploy.yml
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  JWT_SECRET: ${{ secrets.JWT_SECRET }}
  STRIPE_SECRET_KEY: ${{ secrets.STRIPE_SECRET_KEY }}
```

---

### 비밀 생성 명령어

```bash
# 32자 랜덤 시크릿 (JWT, Session 등)
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
python -c "import secrets; print(secrets.token_hex(32))"
openssl rand -hex 32

# UUID 형식
node -e "console.log(require('crypto').randomUUID())"
python -c "import uuid; print(uuid.uuid4())"
```

---

### 배포 전 환경변수 보안 체크리스트

```markdown
## 배포 전 체크리스트

### 필수 확인
- [ ] .env 파일이 .gitignore에 포함
- [ ] pre-commit hook 또는 git-secrets 설치됨
- [ ] JWT_SECRET, SESSION_SECRET이 32자 이상 랜덤값
- [ ] 데이터베이스 비밀번호가 강력한 값으로 변경됨
- [ ] Stripe/결제 키가 라이브(live) 키로 교체됨
- [ ] BCRYPT_ROUNDS가 12 이상
- [ ] DB_SSL=true (프로덕션)
- [ ] ALLOWED_ORIGINS에 실제 도메인만 포함
- [ ] LOG_LEVEL이 error 또는 warn (프로덕션)
- [ ] NEXT_PUBLIC_* / VITE_* 변수에 시크릿 미포함

### 시크릿 관리 도구
- [ ] AWS Secrets Manager / Vault / Doppler 중 하나 사용
- [ ] GitHub Actions Secrets에 프로덕션 값 등록됨
- [ ] 팀원 전원이 시크릿 접근 방법 공유됨
```

---

## 사용 예시

**입력:**
> "Next.js + PostgreSQL + Redis + Stripe + Google OAuth 프로젝트 환경변수 파일 만들어줘."

**출력:**
- `.env.example` — 모든 변수 주석 포함
- `src/lib/env.ts` — Zod 검증 스키마
- `scripts/env-diff.sh` — 환경별 diff 스크립트
- `.git/hooks/pre-commit` — 커밋 방지 훅
- `.gitignore` 스니펫
- 보안 체크리스트

---

## 주의사항
- `.env.example`에는 실제 비밀값 절대 포함 금지 — 형식/예시 값만 기재
- `[SECRET]` 주석으로 민감 변수 명시적 표시
- `NEXT_PUBLIC_*` / `VITE_*` 접두사 변수는 클라이언트 번들에 포함됨 — 시크릿 사용 금지
- `DATABASE_URL`은 개별 변수보다 단일 연결 문자열 선호 (ORM 호환성)
- 프로덕션 환경에서는 반드시 AWS Secrets Manager / Vault / Doppler 중 하나를 사용한다
- `git-secrets` 또는 `truffleHog`를 CI 파이프라인에 추가하여 자동 탐지 권장
