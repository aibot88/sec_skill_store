---
name: openapi-tool-scaffold
description: |
  OpenAPI 3.x (JSON/YAML) 스펙을 MCP stdio 서버(Python) 코드로 자동 변환하는 스킬.
  외부 REST API를 MCP tool로 빠르게 브릿지할 때 사용.
  인증(Bearer, API Key, OAuth stub) 지원, endpoint별 tool 자동 생성.
  트리거: OpenAPI→MCP 변환, 외부 API MCP 연동, REST API tool 자동화, Python MCP scaffold.
metadata:
  author: misskim
  version: "1.0"
---

# OpenAPI Tool Scaffold

Research → Audit → Rewrite 패턴으로 재작성한 **Python 3.10+ 기반 OpenAPI→MCP 생성 스킬**.

- 입력: OpenAPI 3.x spec (URL 또는 로컬 JSON/YAML)
- 출력: 실행 가능한 MCP stdio 서버 Python 파일
- 핵심: 각 REST endpoint를 MCP tool로 자동 노출

> 외부 툴을 blind install 하지 않고, 공개 패턴을 흡수해 내부 재구현.

## 왜 필요한가?

1. **실제 필요성**: 외부 API 통합 시간을 크게 절약
2. **기존 것으로 충분한가?**: 기존 mcporter류는 있어도 OpenAPI→MCP 자동 코드 생성은 공백 존재
3. **비용 대비 효과**: 추가 SaaS 비용 없이 개발 시간 절감
4. **과대포장 방지**: 기존 구현을 그대로 가져오지 않고 패턴만 흡수

## 포함 파일

```
openapi-tool-scaffold/
├── SKILL.md
├── scripts/
│   └── openapi-to-mcp.py
├── templates/
│   └── mcp_server_stdio.py.tmpl
├── examples/
│   ├── README.md
│   ├── petstore-mcp-server.py
│   ├── todo-mini-openapi.yaml
│   └── todo-mini-mcp-server.py
└── references/
    └── research-audit.md
```

## 빠른 시작

```bash
# 1) Petstore OpenAPI -> MCP 서버 코드 생성
python3 skills/openapi-tool-scaffold/scripts/openapi-to-mcp.py \
  "https://petstore3.swagger.io/api/v3/openapi.json" \
  --output skills/openapi-tool-scaffold/examples/petstore-mcp-server.py \
  --server-name petstore_mcp

# 2) 생성 코드 문법 검사
python3 -m py_compile skills/openapi-tool-scaffold/examples/petstore-mcp-server.py

# 3) MCP 서버 실행 (stdio)
python3 skills/openapi-tool-scaffold/examples/petstore-mcp-server.py
```

## CLI 사용법

```bash
python3 scripts/openapi-to-mcp.py INPUT --output OUTPUT.py [options]
```

옵션:

- `--server-name` : MCP 서버 이름 오버라이드
- `--base-url` : OpenAPI servers보다 우선하는 API base URL
- `--template` : 서버 템플릿 경로 변경
- `--include-deprecated` : deprecated operation 포함
- `--max-tools N` : 생성 tool 수 제한 (0=무제한)

## 인증 패턴 (생성 서버)

생성된 서버는 OpenAPI `components.securitySchemes` + operation/global `security`를 해석해
다음 환경변수를 자동 사용한다.

### 1) Bearer
- `BEARER_TOKEN_<SCHEME_NAME>`
- fallback: `BEARER_TOKEN`

### 2) API Key
- `API_KEY_<SCHEME_NAME>`
- fallback: `API_KEY`
- OpenAPI 정의(`in: header/query/cookie`, `name`)에 맞게 자동 주입

### 3) OAuth (stub)
- `OAUTH_ACCESS_TOKEN_<SCHEME_NAME>`
- fallback: `OAUTH_ACCESS_TOKEN`
- 토큰 자동 발급 플로우는 구현하지 않고, **토큰 주입 스텁**으로 처리

(추가) Basic auth도 지원:
- `BASIC_USERNAME_<SCHEME_NAME>`, `BASIC_PASSWORD_<SCHEME_NAME>`
- fallback: `BASIC_USERNAME`, `BASIC_PASSWORD`

## 생성되는 MCP 메서드

- `initialize`
- `tools/list`
- `tools/call`
- `ping`

stdio 입력은 newline JSON-RPC를 기본으로 처리하며, Content-Length 프레이밍 입력도 수용한다.
출력은 newline JSON-RPC(기본)이며 `MCP_USE_CONTENT_LENGTH=1`로 Content-Length 출력 가능.

## 제한사항

- OpenAPI **3.x만** 지원
- 외부 `$ref` URL dereference는 자동 fetch하지 않음 (로컬 `#/...` 중심)
- complex serialization(style/explode deepObject)은 기본 매핑 수준으로 처리
- OAuth 자동 리프레시/코드교환은 범위 밖 (stub)

## 운영 팁

- 민감 endpoint는 OpenAPI 단계에서 별도 spec 분리 권장
- `--max-tools`로 초기 노출 범위를 좁히고 점진 확장
- 반드시 읽기/쓰기/삭제 endpoint 구분 후 클라이언트 측 승인 정책 추가

## Research/Audit 결과

세부 조사 결과는 `references/research-audit.md` 참고.

핵심 결론:
- 오픈소스는 대부분 TS/Node 또는 특정 플랫폼 편향
- Python 경량/무의존(또는 최소의존) 생성기 수요 존재
- 라이선스는 주로 MIT/Apache-2.0으로 패턴 참조에 적합
- 따라서 내부 Python 재작성 전략이 타당
