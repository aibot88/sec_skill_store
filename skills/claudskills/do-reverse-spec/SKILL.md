---
name: do-reverse-spec
description: "ALWAYS use when extracting functional specifications from existing code that lacks documentation. Supports two perspectives: (1) product-feature specs that analyze multiple source files to describe a product capability from the user's viewpoint, and (2) module-level technical specs for binary formats, protocols, state machines, algorithms, or APIs. Works with natural language ('로직 제어 기능 명세 작성해줘') or slash command arguments. ALWAYS use when user mentions: 역공학 명세, reverse engineering spec, 코드 기반 명세, code-based specification, 기능 명세 추출, extract functional spec, 바이너리 구조 명세, binary structure spec, 프로토콜 명세, protocol specification, 상태 머신 명세, state machine spec, 알고리즘 명세, algorithm specification, 코드에서 문서 생성, generate docs from code, 설계 의도 추출, design intent extraction, 명세서 역공학, spec reverse engineering, 제품 기능 명세, product feature spec, 기능 사양서, functional specification, 동작 명세, behavior specification, 코드 분석 후 명세 작성, 기능 스펙 문서, 사양서 작성. Do NOT use for: API header documentation (use do-apidoc), code quality audit (use plan-quality-audit), data flow tracing without spec output (use plan-dataflow), or designing new function contracts from scratch (use plan-function-spec)."
argument-hint: "[<source-files>] [--scope=product|module] [--type=binary|protocol|fsm|algorithm|api|auto] [--output=<path>] [--target=csharp|python|none]"
user-invokable: true
context: fork
agent: general-purpose
---

<!-- BEGIN: cycle3-body-neutral -->

## 0. 문서 구조 (본 SKILL의 세 층)

1. **도메인 본문 (§1 ~ §N)**: 이 SKILL의 프로토콜.
   잠금 어휘 사용 0건이 `verify-policy --check body-neutrality`로 자동 검증됩니다.
2. **방법론 본문 — 도메인 중립**: Cycle 3에서 `<!-- BEGIN: cycle3-body-neutral -->` ~ `<!-- END: cycle3-body-neutral -->` 마커로 감싸진 영역.
3. **도메인 예시 부록 (§A)**: MCU/MPU/WPF 도메인별 사례.
   SoT(`policies/locked-vocab.json`)에서 `scripts/gen-locked-vocab.mjs`가 자동 생성합니다.

직접 부록을 편집하지 마세요 — `node scripts/gen-locked-vocab.mjs`로 재생성됩니다.

---

# Reverse-Engineering Specification Generator

코드를 분석하여 원래 설계 의도를 역추출하고 고품질 기능 명세서를 생성한다.

## 인자 파싱

사용자 입력에서 다음 인자를 추출한다. `$ARGUMENTS`에 명시적 인자가 없으면 자연어에서 추론한다.

| 인자 | 기본값 | 추론 규칙 |
|------|--------|----------|
| `source-files` | (자동 탐색) | 파일 경로가 명시되면 사용. 없으면 Grep/Glob으로 관련 파일 탐색 |
| `--scope` | `auto` | 파일 지정 → `module`, 기능명만 → `product` |
| `--type` | `auto` | Phase 1에서 코드 패턴으로 자동 감지 |
| `--output` | `Docs/` | 명시 시 해당 경로 사용 |
| `--target` | `none` | `csharp`, `python` 지정 시 구현 가이드 부록 포함 |

## Phase 1: 명세 유형 감지

`--type=auto`이면 대상 소스를 스캔하여 판별한다.

| 유형 | 코드 패턴 |
|------|----------|
| `binary` | struct 캐스팅, memcpy, 오프셋 파싱, CRC/체크섬, delimiter, 매직 넘버 |
| `protocol` | send/receive, 패킷 구조, handshake, ACK/NAK, 프레임 |
| `fsm` | state enum, switch(state), 전이 함수, event dispatch |
| `algorithm` | 수학 공식, 보정 테이블, 필터, 변환 파이프라인, 보간 |
| `api` | init/deinit 생명주기, 콜백 등록, 설정 구조체, 에러 코드 반환 |

`--scope=product`이면 유형 감지를 건너뛰고 관련 소스를 종합 분석한다.

## Phase 2: 코드 분석

3개의 Explore 에이전트를 **병렬로** 실행한다 (Agent 도구 사용, subagent_type=Explore).

**Agent 1 — 대상 소스 전체 분석**:
- 모든 함수/구조체/전역변수 목록화
- 데이터 흐름, 처리 순서, 검증 로직 추적
- 매직 넘버, 상수, 범위 제약 추출
- scope=product이면 여러 파일의 관계와 전체 기능 흐름 파악

**Agent 2 — 소비/호출측 코드 분석**:
- 결과물이 어디서 어떻게 사용되는지 추적
- 호출자, 콜백, 이벤트 핸들러 분석
- scope=product이면 사용자 인터페이스 관점 동작 흐름 파악

**Agent 3 — 타입/상수/에러 정의 수집**:
- 관련 헤더에서 struct, enum, #define, typedef 수집
- 에러 코드 전체 목록 추출
- 외부 의존성 식별

## Phase 3: 직접 검증 + 불일치 탐지

에이전트 결과를 바탕으로 핵심 구조체/함수를 **Read 도구로 직접 읽어** 교차 확인한다.

중점 확인:
- 코드 주석 vs 실제 구현 불일치 (비트필드 크기, enum 순차 번호 등)
- 문서화되지 않은 암묵적 제약 (고정값, 하드코딩 상수)
- 엣지 케이스 처리 방식

발견된 불일치는 명세서의 "알려진 제한사항" 섹션에 기록한다.

## Phase 4: 문서 품질 전략

### 공통 원칙 (모든 유형 — 하나라도 빠지면 불완전한 명세)
- **RFC 2119 규범적 언어** — 검증 규칙에 반드시 MUST/SHALL/SHOULD를 사용한다. 예: "`signature` 필드는 `0x4C43504C`이어야 한다(**MUST**)." 단순 설명이 아닌 의무 수준을 명확히 표현하는 것이 핵심이다.
- **문서 메타데이터 헤더** — 최상단에 버전/상태/날짜/대상 테이블 배치
- **용어 정의 섹션** — 개요 바로 다음에 반드시 배치. 약어, 도메인 용어, 프로젝트 고유 명칭 정의.
- **검증 규칙 테이블** — 모든 제약 조건을 "조건 + MUST/SHOULD + 위반 시 동작" 형식 테이블로 정리. product scope에서도 설정 범위/유효값 테이블 필수.
- **3-레이어 예제** — (추상 표현 → 필드 테이블 → 실제 데이터). module scope에서 최소 1개 필수.
- **코드 근거** — 모든 수치/규칙에 `소스파일:라인번호` 근거 표시
- **알려진 제한사항 섹션** — Phase 3 발견 사항을 반드시 별도 섹션으로 작성. 없어도 "발견된 제한사항 없음"으로 섹션 유지.

### 유형별 특수 기법

| 유형 | 표현 기법 |
|------|----------|
| `binary` | 오프셋 테이블, ASCII 비트 다이어그램, 어노테이션 hex dump, CRC 상세 |
| `protocol` | 시퀀스 다이어그램(ASCII), 프레임 박스, 타임아웃 규칙 |
| `fsm` | 상태 전이 테이블, ASCII 상태 다이어그램, 이벤트-액션 매트릭스 |
| `algorithm` | 수식, 입출력 범위 테이블, 정밀도 분석, 단위 변환 체인 |
| `api` | 사전/사후 조건, 호출 시퀀스, 에러 흐름도 |
| `product` | 기능 개요, 시스템 블록 다이어그램, 설정 파라미터 테이블 |

## Phase 5: 명세서 작성

유형별 목차 템플릿에 따라 작성한다.

### binary/protocol
```
문서 메타데이터
1. 개요 (목적, 범위)
1.1 용어 정의 (필수)
1.2 규범적 언어 (MUST/SHALL/SHOULD — RFC 2119)
2. 인코딩 규칙 (엔디안, 패딩, 비트필드 배치)
3. 데이터 모델 (타입, enum, 상수)
4. 전체 레이아웃 (ASCII 다이어그램, 파싱 순서)
5~N. 각 구조체 상세 (필드 테이블 + 검증 규칙 + 비트 다이어그램)
N+1. 무결성 검증 (CRC/체크섬)
N+2. 크기 계산 공식
N+3. 알려진 제한사항
부록: 타입 테이블, 에러 코드, 최소 유효 예제(3-레이어), 타겟 언어 가이드
```

### fsm
```
문서 메타데이터
1. 개요
1.1 용어 정의 (필수)
1.2 규범적 언어 (MUST/SHALL/SHOULD)
2. 상태 정의 (enum, 각 상태 설명)
3. 이벤트/입력 정의
4. 상태 전이 테이블 (현재 상태 × 이벤트 → 다음 상태 + 액션)
5. 전이 다이어그램 (ASCII)
6. 각 상태 상세 (진입/이탈 액션, 내부 동작)
7. 타이밍 제약 및 에러 처리
8. 알려진 제한사항
부록: 상태 코드 목록, 예제 시나리오
```

### algorithm
```
문서 메타데이터
1. 개요 (목적, 적용 범위)
1.1 용어 정의 (필수)
1.2 규범적 언어 (MUST/SHALL/SHOULD)
2. 입력/출력 정의 (변수, 단위, 범위)
3. 수학적 모델 (공식, 유도)
4. 구현 상세 (이산화, 정밀도, 오버플로우 방지)
5. 보정/캘리브레이션 파라미터
6. 경계값 동작 (0, max, NaN, INFINITY)
7. 알려진 제한사항
부록: 파라미터 테이블, 테스트 벡터
```

### api
```
문서 메타데이터
1. 개요 (모듈 목적, 의존성)
1.1 용어 정의 (필수)
1.2 규범적 언어 (MUST/SHALL/SHOULD)
2. 초기화/해제 생명주기
3. 설정 구조체 상세
4. 공개 함수 레퍼런스 (사전/사후 조건)
5. 내부 상태 모델
6. 에러 처리 및 반환 코드
7. 스레드/ISR 안전성
8. 알려진 제한사항
```

### product (제품 기능)
```
문서 메타데이터
1. 기능 개요 (목적, 사용자 가치)
1.1 용어 정의 (필수)
1.2 규범적 언어 (MUST/SHALL/SHOULD)
2. 시스템 구성 (블록 다이어그램, 관련 모듈)
3. 기능 동작 설명
   3.1 정상 동작 흐름
   3.2 설정 파라미터 및 유효 범위 (검증 규칙 테이블 포함)
   3.3 입출력 인터페이스
4. 상태 및 생명주기
5. 에러/이상 처리
6. 성능 특성 (주기, 지연, 정밀도)
7. 알려진 제한사항 및 한계 (필수 — Phase 3 결과)
8. 관련 기능과의 상호작용
부록: 설정 파라미터 전체 테이블 (범위/기본값/단위), 에러 코드
```

## Phase 6: 교차 검증 루프

작성된 명세서를 소스 코드와 3개 에이전트 **병렬**로 교차 검증한다 (Agent 도구 사용).

**Agent A** — 구조/레이아웃: 필드 오프셋, 크기, 타입, 열거값 일치
**Agent B** — 검증 규칙/로직: 조건, 범위, 에러 코드, 분기 일치
**Agent C** — 예제/공식: 계산 공식, 예제 값, 코드 참조 정확성

각 에이전트는 항목별 Pass/Fail + 일치율(%)을 보고한다.

**루프 규칙**:
1. 전체 일치율 95% 미만 → 불일치 수정 후 해당 섹션만 재검증
2. 최대 3회 반복
3. 95% 이상 → 최종 확정, 결과 요약 출력

## 문서 작성 원칙

1. **코드가 유일한 진실** — 주석이 아닌 실제 코드 동작 기준
2. **근거 명시** — 제약/규칙에 소스파일:라인번호 표시
3. **절대 추측 금지 (최우선 원칙)** — 명세서에 거짓 정보는 심각한 문제를 일으킨다. 코드에서 확인할 수 없는 정보를 절대 지어내지 않는다.
   - 약어 풀네임이 코드/주석에 없으면 약어 그대로 사용 + "(정확한 명칭 미확인)" 표시. "LM"의 풀네임이 코드에 없으면 "Logic Module"이라고 추측 금지.
   - 통신 방식(UART/SPI/Ethernet 등)을 코드에서 직접 확인하지 않고 단정 금지.
   - 존재하지 않는 용어/함수/모듈을 만들어내기 금지. 코드에서 미발견 시 언급하지 않는다.
   - 확인 불가능한 내용이 필요하면 "확인 필요" 또는 "코드에서 미확인"으로 명시.
4. **단순→복잡 전개** — 기본 타입부터 복합 구조로 점진적 설명
5. **검증 가능성** — 모든 수치/공식은 코드에서 검증 가능하도록 구체적 기술
6. **한글 작성** — 설명은 한글, 기술 용어/코드는 원문 유지

<!-- END: cycle3-body-neutral -->
