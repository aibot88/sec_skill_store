---
name: ceo-standards
description: >
  CEO Standards — Security policy, coding standards, performance patterns.
  Load this when reviewing security, writing code, or enforcing quality gates.
---
### 1. 인증 / 인가 (Authentication & Authorization)

**1-1. 인증 필수 원칙**

- 모든 API 엔드포인트는 서버사이드 인증 미들웨어를 통과해야 함
- 퍼블릭 엔드포인트는 명시적 화이트리스트로만 허용 (PUBLIC_ROUTES 배열 관리)
- 클라이언트 사이드 인증 체크는 UX 용도일 뿐, 보안 판단 근거로 사용 금지

**1-2. 토큰 관리**

- JWT는 httpOnly + Secure + SameSite=Strict 쿠키로만 전달
- localStorage, sessionStorage에 토큰 저장 절대 금지
- Access Token 만료: 15분 이하
- Refresh Token: DB 저장 + 단일 사용 후 즉시 rotation
- Refresh Token 만료: 7일 이하, 절대적 만료(absolute expiry) 30일

**1-3. 비밀번호**

- 해싱: argon2id 우선, 차선 bcrypt (cost factor >= 12)
- SHA-256, MD5, 평문 저장 절대 금지
- 비밀번호 최소 요구사항: 8자 이상, 유출 DB(HaveIBeenPwned API) 대조 권장

**1-4. OAuth / SSO**

- state 파라미터 필수 생성 및 검증 (CSRF 방지)
- PKCE (Proof Key for Code Exchange) 적용 권장
- 콜백 URL은 환경변수로 관리, 하드코딩 금지

**1-5. RBAC (Role-Based Access Control)**

- 모든 엔드포인트에 역할 검증 미들웨어 적용
- 역할 체크는 DB 기준 실시간 조회 (캐시 시 TTL <= 5분)
- 리소스 소유권 검증 별도 수행 (자기 데이터만 접근)

**1-6. Rate Limiting**

| 대상            | 제한                |
| --------------- | ------------------- |
| 로그인 시도     | 5회/분/IP           |
| 인증코드 (OTP)  | 3회/10분/계정       |
| 비밀번호 재설정 | 3회/시간/계정       |
| 일반 API        | 60회/분/유저        |
| Webhook 수신    | 300회/분/엔드포인트 |
| 파일 업로드     | 10회/분/유저        |

### 2. 입력 검증 (Input Validation)

**2-1. 원칙**

- 모든 입력은 서버에서 재검증 — 클라이언트 검증은 UX 전용
- 검증 라이브러리: zod (TypeScript) 사용, 스키마를 src/schemas/에 집중 관리
- 검증 실패 시 400 Bad Request + 제네릭 에러 메시지 반환 (내부 상세는 로그에만)

**2-2. Injection 방지**

- SQL Injection: ORM 사용, raw query 시 parameterized query만 허용
- NoSQL Injection: 쿼리 객체에 $ 연산자 포함 여부 검사
- XSS: 사용자 입력 HTML 렌더링 금지, dangerouslySetInnerHTML 사용 금지
- Command Injection: child_process.exec 금지, 필요 시 execFile + 인자 배열만 허용
- Path Traversal: 파일명/경로에 ../, ..\\ 포함 시 즉시 reject
- SSRF: 내부 URL(127.0.0.1, 10.x, 172.16-31.x, 192.168.x, metadata 엔드포인트) 차단

**2-3. 파일 업로드**

- 확장자 화이트리스트 (블랙리스트 금지)
- 서버에서 MIME 타입 검증 (매직 바이트 확인)
- 최대 파일 크기 제한 (기본 10MB, 용도별 조정)
- 업로드 파일명은 UUID로 재생성, 원본 파일명은 메타데이터로만 저장
- 업로드 디렉토리는 웹 루트 외부 또는 오브젝트 스토리지(S3)

### 3. 결제 / 빌링 보안 (Billing Security)

**3-1. 핵심 원칙**

- 가격/할인/세금 계산은 100% 서버사이드 — 클라이언트가 보낸 금액 절대 신뢰 금지
- 구독 상태 판단은 DB 레코드 기준만 사용
- 프론트에서 받은 planId, priceId는 서버에서 유효성 재검증

**3-2. Webhook 보안**

- Webhook 서명(signature) 검증 필수 — 미검증 시 즉시 400 반환
- IP 화이트리스트 추가 적용 권장
- 멱등성(Idempotency): event_id 기반 중복 처리 방지
- Webhook 처리 실패 시 재시도 큐(dead letter queue) 운용

**3-3. 감사 로그 (Audit Log)**

- 결제 생성/변경/취소/환불 모든 이벤트 기록
- 로그 필수 필드: userId, action, amount, currency, timestamp, ip, eventId
- 감사 로그는 수정/삭제 불가 (append-only)

**3-4. 크레딧/선불 시스템**

- 잔액 차감은 DB 트랜잭션 내 원자적(atomic) 처리
- 음수 잔액 허용 금지 — CHECK (balance >= 0) 또는 애플리케이션 레벨 검증
- 동시성 제어: SELECT ... FOR UPDATE 또는 optimistic locking

### 4. API 설계 / 보안

**4-1. CORS**

- 허용 도메인 명시적 화이트리스트, `origin: '*'` 절대 금지
- credentials: true 사용 시 와일드카드 origin 불가 (브라우저가 차단)

**4-2. CSRF**

- 상태 변경 요청 (POST/PUT/PATCH/DELETE)에 CSRF 토큰 필수
- SameSite 쿠키 + CSRF 토큰 이중 방어

**4-3. HTTP 보안 헤더 (필수)**

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

**4-4. 응답 보안**

- 에러 응답에 스택트레이스, DB 스키마, 내부 경로 노출 절대 금지
- 프로덕션에서 NODE_ENV=production 필수
- 존재하지 않는 리소스: 404 (id 노출 금지, 열거 공격 방지)
- 인증 실패: 401, 인가 실패: 403 — 메시지는 제네릭

**4-5. API 버전 관리**

- URL prefix 방식: /api/v1/...
- 버전 간 하위 호환성 유지, 강제 마이그레이션 시 최소 6개월 유예

### 5. 데이터 보호

**5-1. 암호화**

- PII(개인정보) 저장: AES-256-GCM 암호화
- 암호화 키: 환경변수 또는 KMS(AWS KMS, GCP KMS 등)에서 관리
- DB 접속: SSL/TLS 필수 (?sslmode=require)
- 전송 구간: HTTPS only, HTTP 리다이렉트 강제

**5-2. 시크릿 관리**

- API Key, 토큰: 해싱 저장 (원문 복원 불필요한 경우)
- 복원 필요 시: AES 암호화 저장
- 평문 저장 절대 금지
- .env 파일은 .gitignore에 반드시 포함
- .env.example 유지: 필수 키 목록 문서화 (값은 비움)
- 프로덕션: Vault / Secret Manager / 환경변수

**5-3. 로그 보안**

- 로그에 출력 금지 항목: 비밀번호, 카드번호, API 키, 토큰, PII
- 민감 필드는 마스킹 처리 (email: j\*\*\*@example.com)
- 로그 보존 기간 정책 수립 (기본 90일, 감사 로그는 3년)

**5-4. 삭제 정책**

- 소프트 딜리트 기본 (deletedAt 컬럼)
- 하드 딜리트는 배치 작업으로만, 감사 로그 필수
- GDPR/개인정보보호법 대응: 사용자 요청 시 30일 이내 완전 삭제 프로세스

### 6. 백엔드 아키텍처 필수 패턴

**6-1. 에러 처리**

- 글로벌 에러 핸들러 미들웨어 필수
- 커스텀 에러 클래스 계층 구조: AppError (base) → ValidationError, AuthError, NotFoundError, ForbiddenError, ConflictError
- try-catch에서 에러 삼키기(swallow) 금지 — 반드시 로깅 또는 재throw
- 비동기 에러: express-async-errors 또는 래퍼 함수로 포착

**6-2. 로깅**

- 구조화 로깅(structured logging): JSON 형태, pino 또는 winston 사용
- 필수 필드: timestamp, level, requestId, userId, action, duration
- Request ID: 모든 요청에 UUID 할당, 로그 전체에 전파
- 로그 레벨: error > warn > info > debug — 프로덕션은 info 이상만

**6-3. DB 설계 원칙**

- 모든 테이블 필수 컬럼: id (UUID), createdAt, updatedAt, deletedAt
- 멀티테넌트: organizationId 기반 row-level 격리
- 인덱스: WHERE 절, JOIN 키, ORDER BY 대상에 반드시 설정
- N+1 쿼리 금지 — include/select 명시적 사용
- 마이그레이션: ORM migration만 사용, 수동 DDL 금지
- 트랜잭션: 복수 테이블 변경 시 반드시 사용

**6-4. 캐싱 전략**

- 캐시 키 네이밍: {service}:{entity}:{id}
- TTL 필수 설정 — 무기한 캐시 금지
- 캐시 무효화: 데이터 변경 시 관련 캐시 즉시 삭제
- 민감 데이터 캐싱 금지 (토큰, PII, 결제정보)

**6-5. 큐 / 비동기 작업**

- 이메일 발송, Webhook 재시도, 대용량 처리 → 큐 사용
- 동기 API 응답에서 30초 이상 걸리는 작업 처리 금지
- 큐 작업 필수 요소: 재시도 횟수 제한, 타임아웃, dead letter queue
- 멱등성 키로 중복 실행 방지

**6-6. 헬스체크 / 모니터링**

- GET /api/health 엔드포인트 필수 (인증 불필요) — 응답: DB 연결 상태, 캐시 연결 상태, 버전, uptime
- GET /api/health/ready — 트래픽 수신 가능 여부 (readiness probe)
- 에러율 급증 시 알림 설정

### 7. 미들웨어 실행 순서 (권장)

```
1. Request ID 생성
2. 로깅 (요청 시작)
3. CORS
4. 보안 헤더 (helmet)
5. Rate Limiter
6. Body Parser (크기 제한 포함)
7. CSRF 검증
8. 인증 (JWT 검증)
9. 인가 (RBAC)
10. 입력 검증 (zod)
11. 비즈니스 로직 (라우터/컨트롤러)
12. 에러 핸들러
13. 로깅 (요청 완료 + duration)
```

### 8. 코드 레벨 금지 사항

| 금지 항목                       | 이유                    |
| ------------------------------- | ----------------------- |
| eval(), new Function()          | 코드 인젝션             |
| dangerouslySetInnerHTML         | XSS                     |
| child_process.exec()            | 커맨드 인젝션           |
| console.log (프로덕션)          | 구조화 로거 사용        |
| 동적 import에 사용자 입력       | 임의 모듈 로딩          |
| any 타입 남용                   | 타입 안전성 붕괴        |
| // @ts-ignore 무분별 사용       | 타입 에러 은폐          |
| 하드코딩된 시크릿               | 유출 위험               |
| SELECT \*                       | 과다 데이터 노출 + 성능 |
| 동기 파일 I/O (fs.readFileSync) | 이벤트 루프 블로킹      |

### 9. 인프라 / 배포

**9-1. 환경 분리**

- development / staging / production 환경 완전 분리
- 프로덕션 DB에 개발 환경에서 직접 접근 절대 금지
- 환경별 환경변수 독립 관리

**9-2. CI/CD 보안**

- npm audit / pnpm audit CI에서 자동 실행
- critical/high 취약점 발견 시 빌드 실패 처리
- 시크릿은 CI/CD 시크릿 스토어에만 저장 (GitHub Secrets 등)
- 빌드 아티팩트에 .env, node_modules 포함 금지

**9-3. Docker**

- non-root 유저 실행 (USER node)
- 최소 이미지 사용 (node:xx-alpine)
- .dockerignore에 .env, .git, node_modules 포함
- 멀티스테이지 빌드로 빌드 의존성 제거

**9-4. HTTPS / TLS**

- 전 구간 HTTPS 강제 — HTTP → HTTPS 301 리다이렉트
- TLS 1.2 이상만 허용
- 인증서 자동 갱신

### 10. PR 보안 체크리스트

```
□ 새 엔드포인트에 인증 미들웨어 적용했는가?
□ 입력 검증 스키마(zod) 작성했는가?
□ RBAC + 리소스 소유권 검증 적용했는가?
□ 에러 응답에 내부 정보 노출이 없는가?
□ 새 환경변수를 .env.example에 추가했는가?
□ 금지 함수(eval, exec 등)를 사용하지 않았는가?
□ 민감 데이터가 로그에 노출되지 않는가?
□ DB 쿼리에 N+1 문제가 없는가?
□ 캐시 키에 TTL이 설정되었는가?
□ 결제 관련 로직이 서버사이드에서만 처리되는가?
```

---

## 코딩 표준 (Language-Agnostic Core)

### 불변성 (CRITICAL)

항상 새 객체를 생성하고, 기존 객체를 절대 변경하지 않습니다:

```
// 의사 코드
잘못:  modify(original, field, value) → original을 직접 변경
올바름: update(original, field, value) → 변경된 새 복사본 반환
```

### 핵심 원칙

- **KISS**: 실제로 동작하는 가장 단순한 해결책 선택. 조기 최적화 금지. 영리함보다 명확함.
- **DRY**: 반복 로직은 공유 함수로 추출. 복사-붙여넣기 드리프트 방지. 반복이 실제일 때만 추상화 도입.
- **YAGNI**: 필요하기 전에 기능이나 추상화를 만들지 않음. 투기적 일반화 금지. 단순하게 시작 후 압력이 실재할 때 리팩토링.

### 파일 조직

```
많은 작은 파일 > 적은 큰 파일
- 높은 응집도, 낮은 결합도
- 300줄 이하 엄수 (GATE-1 자동 차단)
- 초과 즉시 모듈 분리 — 리팩토링 후 재제출
- 기능/도메인 기준 조직 (타입 기준 아님)
```

**300줄 규칙은 협상 불가 (GATE-1 등록 패턴)**
- Worker가 300줄 초과 파일 생성 시 → GATE-1에서 즉시 차단
- CEO가 분리 지시 → Worker가 모듈 분리 후 재제출
- 예외 없음 (설정 파일, 자동 생성 파일 제외)

### 함수 크기

- 50줄 상한
- 한 가지 책임만 담당
- 크면 분할

### 중첩 깊이

- 4단계 상한
- 조건이 쌓이면 early return 사용

### 에러 처리

- 모든 레벨에서 명시적 처리
- UI 코드: 사용자 친화적 메시지
- 서버 코드: 상세 로깅
- 에러 삼키기 절대 금지

### 입력 검증

- 시스템 경계에서 항상 검증
- 스키마 기반 검증 (Zod 등)
- 빠른 실패 + 명확한 에러
- 외부 데이터 절대 신뢰 금지

### 네이밍 규칙

| 대상                       | 규칙                     |
| -------------------------- | ------------------------ |
| 변수, 함수                 | camelCase                |
| Boolean                    | is/has/should/can prefix |
| 인터페이스, 타입, 컴포넌트 | PascalCase               |
| 상수                       | UPPER_SNAKE_CASE         |
| Custom Hooks               | use prefix               |

---

## TypeScript/JavaScript 규칙

- 퍼블릭 API에 명시적 타입 — 로컬 변수는 추론 허용
- 확장 가능한 형상: interface — 유니온/인터섹션/매핑: type
- 애플리케이션 코드에서 any 금지 — 외부 입력은 unknown + 타입 내로잉
- React: props에 named interface, React.FC 금지, 콜백 타입 명시
- 불변성: spread operator, Readonly<T>
- 에러 처리: async/await + try-catch + unknown 내로잉
- 입력 검증: Zod + z.infer<typeof schema> 타입 추론
- 프로덕션에서 console.log 금지 (hook으로 강제)

---

## 웹/프론트엔드 규칙

### Anti-Template 정책

모든 의미 있는 프론트엔드 표면은 아래 10가지 중 최소 4가지를 보여야 합니다:

1. 스케일 대비를 통한 명확한 계층
2. 균일 패딩이 아닌 의도적 리듬
3. 오버랩, 그림자, 표면, 모션을 통한 깊이/레이어링
4. 캐릭터와 페어링 전략이 있는 타이포그래피
5. 장식이 아닌 의미론적 색상 사용
6. 디자인된 hover/focus/active 상태
7. 적절한 곳에서 그리드 깨는 에디토리얼/벤토 구성
8. 시각적 방향에 맞는 텍스처, 그레인, 분위기
9. 산만함이 아닌 흐름 명확화 모션
10. 디자인 시스템의 일부로 취급되는 데이터 시각화

### CSS Custom Properties

모든 디자인 토큰을 변수로 정의합니다. 팔레트, 타이포그래피, 간격을 반복 하드코딩하지 않습니다.

### Semantic HTML

```html
<header>
  <nav aria-label="Main navigation">...</nav>
</header>
<main>
  <section aria-labelledby="hero-heading">
    <h1 id="hero-heading">...</h1>
  </section>
</main>
<footer>...</footer>
```

generic div 스택 대신 semantic element 사용.

### Animation

- Compositor-friendly property만 사용: transform, opacity, clip-path, filter
- Layout-bound property animation 금지: width, height, top, left, margin, padding, border, font-size

### 성능 목표

| Metric | Target  |
| ------ | ------- |
| LCP    | < 2.5s  |
| INP    | < 200ms |
| CLS    | < 0.1   |
| FCP    | < 1.5s  |
| TBT    | < 200ms |

| Page Type    | JS Budget (gzipped) | CSS Budget |
| ------------ | ------------------- | ---------- |
| Landing page | < 150kb             | < 30kb     |
| App page     | < 300kb             | < 50kb     |
| Microsite    | < 80kb              | < 15kb     |

### 프론트엔드 금지 사항

- localStorage/sessionStorage에 토큰 저장 금지 — httpOnly 쿠키만
- React에서 HTML `<form>` 태그 금지
- dangerouslySetInnerHTML 금지
- 기본 템플릿 UI 출력 금지 — 의도적이고 opinionated한 디자인

---

## 테스트 요구사항

### 최소 커버리지: 80%

### TDD 필수 워크플로우

```
1. 테스트 먼저 작성 (RED)
2. 테스트 실행 — 실패해야 함
3. 최소 구현 작성 (GREEN)
4. 테스트 실행 — 통과해야 함
5. 리팩토링 (IMPROVE)
6. 커버리지 검증 (80%+)
```

### 테스트 유형 (전부 필수)

1. **Unit Tests** — 개별 함수, 유틸리티, 컴포넌트
2. **Integration Tests** — API 엔드포인트, DB 작업
3. **E2E Tests** — 핵심 사용자 플로우

### AAA 패턴 (Arrange/Act/Assert)

```typescript
test('calculates similarity correctly', () => {
  // Arrange
  const vector1 = [1, 0, 0]
  const vector2 = [0, 1, 0]

  // Act
  const similarity = calculateCosineSimilarity(vector1, vector2)

  // Assert
  expect(similarity).toBe(0)
})
```

### 테스트 네이밍

```typescript
test('returns empty array when no items match query', () => {})
test('throws error when API key is missing', () => {})
test('falls back to default when cache is unavailable', () => {})
```

### Integration Test 규칙

- DB를 모킹하지 않음 — 실제 테스트 DB 사용
- 테스트 간 격리 보장

---

## 최초 프로젝트 셋업 절차

CEO가 새 프로젝트에서 첫 번째 지시를 수신했을 때:

```
[FIRST-TIME PROJECT SETUP]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 1: gstack 스킬 확인
  → https://github.com/garrytan/gstack 스킬 설치 여부 확인
  → 미설치 시 설치 → 이미 설치되었으면 패스

Step 2: 레지스트리 초기화
  → ~/.claude/error-registry.md 생성 (없으면)
  → ~/.claude/skill-registry.md 생성 (없으면)
  → ~/.claude/project-registry.md 생성 (없으면)
  → ~/.claude/decision-log.md 생성 (없으면)

Step 3: 하네스 장치 배포
  → DC-DEV-OPS를 통해 ①~⑦ 전부 구축
  → pre-commit hook, lint 규칙, 아키텍처 테스트,
    commit-msg hook, CI/CD 게이트, CODEOWNERS, gc.sh

Step 4: 사업 분류
  → DC-BIZ 호출하여 초기 프로젝트 분류

Step 5: 프로젝트 등록
  → project-registry.md에 초기 PROJECT 항목 생성

Step 6: 에이전트 파일 확인
  → .claude/agents/ 디렉토리에 모든 Worker 에이전트 파일 존재 확인
  → 미존재 시 생성

Step 7: 초기화 보고
  → 사용자에게 초기화 상태 보고
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## AI 추천/생성 기능 품질 검증 규칙

> LLM 프롬프트로 동작하는 기능은 타입 체크만으로는 품질 보장 불가.
> 아래 추가 검증을 반드시 포함한다.

```
[AI 기능 완료 기준 — tsc 통과 외 추가 필수 항목]
□ 프롬프트에 "같은 값 중복 반환 허용" 구문이 없는가?
□ 다중 슬롯 배정 기능은 "서로 다른 값 강제" 규칙이 명시되어 있는가?
□ 서버 사이드 후처리로 AI 응답의 이상값(전체 중복, 빈값) 방어 로직이 있는가?
□ Provider별 모델 분류 힌트가 포함되었는가?
```

---

## 글로벌 금지 규칙

```
❌ DC Agent가 사용자와 직접 소통 — CEO만 사용자와 대화
❌ Builder와 Reviewer가 동일 DC Agent — 역할 분리 원칙 위반
❌ GATE 미통과 산출물 전달 — 품질 보증 불가
❌ Token Optimizer 없이 LARGE/HEAVY 실행 — 컨텍스트 소진 위험
❌ Business Judge 없이 작업 착수 — 사업 타당성 미검증
❌ error-registry 미조회 상태로 작업 시작 — 과거 실수 반복 위험
❌ 버전 태그 없는 산출물 — 추적 불가
❌ 에러 발생 후 GC 미실행 — 방어 체계 미갱신
❌ GATE-5 대상 변경 무단 실행 — 파괴적 변경 사전 승인 필수
❌ 작업 완료 후 보고서 미작성 — 산출물 추적 불가
❌ 에이전트/스킬 미업데이트 상태로 동일 실수 반복 — GC 의무
❌ 임시 파일 미정리 — docs/ 누적 방지
❌ Opus를 단순 작업에 투입 — 비용 낭비
❌ Haiku를 아키텍처/보안 판단에 투입 — 품질 위험
❌ DC-OSS 없이 외부 라이브러리/모델 임의 선택 — 보안/라이선스 미검증
❌ SMALL 업무에 PLANNER Phase(DC-BIZ/PLAN.md/CONTRACT) 강제 — 규모별 축약 경로(9-8) 적용 필수
❌ Worker 배정 시 스킬 명시 지시 없이 "알아서 써라" 묵시적 위임 — PRIMARY 스킬 명시 지시 필수(9-9)
❌ EVALUATOR 리포트 전문을 CEO 컨텍스트에 직접 수신 — 3줄 요약만 받고 파일 별도 저장(9-10)
❌ SMALL 업무에 DC-BIZ Opus 투입 — 규모별 모델 강등 기준(9-12) 적용
❌ 스프린트 파일 docs/ 루트에 무한 누적 — 30일 후 archive/ 이동, 90일 후 삭제(9-13)
❌ LLM 프롬프트 기반 기능 tsc 통과만으로 완료 처리 — 실제 API 응답 품질 검증 필수
❌ AI 추천 기능에서 "같은 모델 중복 허용" 규칙 삽입 — 슬롯마다 다른 모델 배정 원칙 강제
❌ DC Agent가 "TypeScript 통과" 만으로 산출물 제출 — 외부 API 호출 기능은 실 응답 시나리오 검증 포함
❌ `.claude/agents/` 서브에이전트 파일 없이 Worker 역할을 CEO가 직접 수행 — 반드시 해당 에이전트 호출
❌ ecc 스킬을 미리 전부 고정 배정 — CEO가 매 업무마다 상황에 맞게 스킬 선택 (과잉 고정 금지)
❌ 3회 수정 루프 초과 후 미보고 — 에스컬레이션 의무
❌ CEO 자가점검 없이 최종 보고 — 품질 검증 누락
❌ decision-log 미기록 상태로 주요 결정 — 의사결정 추적 불가
❌ 코드 산출물에 하네스 장치(hook/lint/test) 없이 납품 — 프로그래밍적 강제 의무
❌ 프로젝트 최초 셋업 시 하네스 ①~⑦ 미구축 — 전체 구축 필수
❌ 에러 등록 후 gc.sh (또는 동등 수단) 미실행으로 방어 체계 미갱신 — GC 파이프라인 의무
```

---

## 시스템 초기화

```bash
mkdir -p ~/.claude/reports

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[CEO SYSTEM INITIALIZED] v2.0.28"
echo "ERROR-REGISTRY : $(grep -c 'ERROR-ID' ~/.claude/error-registry.md 2>/dev/null || echo 0)건"
echo "SKILL-REGISTRY : $(grep -c 'SKILL-ID' ~/.claude/skill-registry.md 2>/dev/null || echo 0)건"
echo "DECISION-LOG   : $(grep -c 'DEC-' ~/.claude/decision-log.md 2>/dev/null || echo 0)건"
echo "ACTIVE PROJECTS: $(grep -c 'ACTIVE' ~/.claude/project-registry.md 2>/dev/null || echo 0)개"
echo "MODEL TIERS    : Opus(설계·보안·OSS·검토) / Sonnet(개발·분석) / Haiku(리서치·문서·QA)"
echo "DEV WORKERS    : FE / BE / DB / MOB / OPS / INT (병렬)"
echo "SPECIAL WORKERS: BIZ(사업판단) / OSS(자원탐색) / TOK(토큰관리)"
echo "GATE           : 1-5 가동"
echo "SELF-INSPECT   : 활성화"
echo "GC             : 에이전트·스킬 자동 업데이트"
echo "HARNESS IMPL   : 코드 산출물 시 hook/lint/test/CI 자동 구축"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "준비 완료. 지시를 내려주세요."
```
