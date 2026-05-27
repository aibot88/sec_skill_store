---
name: arch-frontend
description: 프론트엔드 React 구현. Vite, React, Tailwind, 컴포넌트, 페이지, i18n, OAuth UI 관련 구현 시 사용.
argument-hint: [component] (예: login-page, job-form, result-viewer, interview-script)
allowed-tools: Read, Grep, Bash, Write, Edit, Glob
---

# Frontend Architecture Skill

Vite + React + Tailwind CSS 프론트엔드 구현 가이드.

## 반드시 먼저 읽을 문서
1. `docs/architecture/01-overview.md` — 시스템 개요 및 입출력 구조
2. `docs/architecture/05-api-spec.md` — API 엔드포인트 (프론트엔드 호출 대상)
3. `docs/architecture/06-output-spec.md` — 면접 스크립트 뷰 설계

## 기술 스택
- **빌드**: Vite + `@seed-design/vite-plugin` + `@tailwindcss/vite`
- **UI**: React 19 (함수형 컴포넌트 + Hooks) + Seed Design React
- **스타일**: Tailwind CSS 4 + Seed Design CSS + Jittda 브랜드 토큰
- **인증**: OAuth → JWT (메모리 저장)
- **다국어**: react-i18next
- **HTTP**: fetch 또는 axios + Authorization Bearer header
- **디자인 시스템**: `jittda-design-system` 스킬 참조 (Seed Design + 브랜드 토큰)

### Seed Design 컴포넌트 사용법
1. `seed-docs` MCP → `list_react_components` / `get_react_component` 로 조회
2. CLI: `npx @seed-design/cli@latest add ui:{name}` (packages/ui 에서 실행)
3. `packages/ui/src/index.ts`에 export 추가
4. 앱에서 `import { Component } from '@jittda/ui'`

## 주요 페이지

### 1. 로그인 페이지
- Google/GitHub OAuth 버튼
- `{API_URL}/auth/{provider}/login` 으로 리다이렉트
- 콜백 후 `#token=` 에서 JWT 추출

### 2. Job 생성 폼
- 파일 업로드: 이력서(PDF), 포트폴리오(DOCX)
- 텍스트 입력: JD, GitHub URLs, LinkedIn URL
- 선택: 경험 레벨, 출력 언어
- `POST /api/v1/jobs` 호출

### 3. Job 상태 추적
- `GET /api/v1/jobs/{id}` 폴링
- Phase별 진행률 표시 (0~4)
- 실시간 상태 업데이트

### 4. 결과 뷰어 (면접 스크립트)
- 25개 질문 표시 (카테고리별 탭/섹션)
- 접기/펼치기 (Progressive Disclosure)
- 후속질문 분기 (Expert/Mid/Low)
- 키워드 체크리스트
- 용어 설명 툴팁
- 평가 시나리오 (색상 구분)
- on-demand 번역 버튼

## 파일 배치 (pnpm 워크스페이스)
```
jittda/frontend/
├── packages/
│   ├── ui/                          — 공유 디자인 시스템 (@jittda/ui)
│   │   ├── src/
│   │   │   ├── seed-design/ui/      — Seed Design CLI 생성 컴포넌트
│   │   │   ├── styles/
│   │   │   │   ├── index.css        — base.css + tokens + 글로벌 스타일
│   │   │   │   └── tokens.css       — Jittda 브랜드 토큰
│   │   │   └── index.ts             — 컴포넌트 export
│   │   └── seed-design.json
│   ├── public-app/                  — 사용자용 앱 (:3000)
│   │   └── src/
│   │       ├── pages/               — LoginPage, CreateJobPage, ResultPage
│   │       ├── components/          — auth/, job/, interview/, common/
│   │       ├── hooks/               — useAuth, useJob
│   │       └── index.css            — @import tailwindcss + @jittda/ui/styles
│   └── admin-app/                   — 관리자 앱 (:3001)
│       └── src/
│           ├── pages/               — Dashboard, JobList, Analytics
│           ├── components/          — charts/, admin/
│           └── index.css            — @import tailwindcss + @jittda/ui/styles
├── package.json                     — 루트 워크스페이스
├── pnpm-workspace.yaml
└── tsconfig.base.json
```

## 규칙
- JWT는 메모리만 (localStorage/sessionStorage 금지)
- 컴포넌트명: PascalCase
- Tailwind 유틸리티 클래스 우선 (커스텀 CSS 최소화)
- i18n: 모든 사용자 표시 텍스트는 번역 키 사용
- 반응형: mobile-first
