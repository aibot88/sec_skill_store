---
name: jittda-design-system
description: Jittda Design System Context Injection. UI 컴포넌트 생성/수정 시 Seed Design 컴포넌트 + Jittda 브랜드 토큰을 강제 적용.
triggers:
  - UI, component, 컴포넌트
  - Tailwind, 스타일, color, 색상
  - design system, 디자인 시스템
  - Button, Card, Input, Modal
  - Seed Design, seed-design
---

# Jittda Design System — Seed Design + Brand Tokens

> Seed Design(당근마켓) React 컴포넌트 라이브러리 + Jittda 브랜드 2-tier 토큰 아키텍처.
> 이 스킬이 로딩되면, 모든 UI 코드는 아래 규칙을 **절대 규칙(Design Bible)**으로 따른다.

## 워크플로우

```
1. seed-docs MCP로 컴포넌트 검색 → 있으면 Seed Design 컴포넌트 사용
2. 없으면 → Jittda 커스텀 컴포넌트 (Tailwind + Semantic Token)
3. 스타일링: Semantic Token → Scale Token → 절대 금지: 하드코딩
```

---

## 1. Seed Design 컴포넌트 (우선 사용)

### MCP 도구 활용 (seed-docs 서버)

UI 작업 시 **반드시** seed-docs MCP 도구로 먼저 확인:

```
# 컴포넌트 목록 조회
seed-docs → list_react_components

# 특정 컴포넌트 API/사용법
seed-docs → get_react_component { name: "action-button" }

# Foundation 토큰 (색상, 타이포 등)
seed-docs → get_foundation { name: "color/palette" }

# 아이콘 검색
seed-docs → search_icons { query: "arrow" }
```

### CLI로 컴포넌트 추가

```bash
# UI 패키지에서 실행
cd jittda/frontend/packages/ui
npx @seed-design/cli@latest add ui:{component-name}

# 예시
npx @seed-design/cli@latest add ui:alert-dialog
npx @seed-design/cli@latest add ui:tabs
npx @seed-design/cli@latest add ui:snackbar
```

추가된 컴포넌트는 `packages/ui/src/seed-design/ui/` 에 생성되며,
`packages/ui/src/index.ts`에 export 추가 필요.

### 현재 설치된 Seed Design 컴포넌트

| 컴포넌트 | 경로 |
|---------|------|
| ActionButton | `seed-design/ui/action-button.tsx` |
| TextField | `seed-design/ui/text-field.tsx` |
| SelectBox | `seed-design/ui/select-box.tsx` |
| Checkbox | `seed-design/ui/checkbox.tsx` |
| RadioGroup | `seed-design/ui/radio-group.tsx` |
| LoadingIndicator | `seed-design/ui/loading-indicator.tsx` |
| ProgressCircle | `seed-design/ui/progress-circle.tsx` |

전체 카탈로그 → `references/seed-design-catalog.md`

---

## 2. Jittda 브랜드 토큰 (2-Tier)

> 소스: `packages/ui/src/styles/tokens.css`

### Tier 1: Scale Token

```css
/* Navy palette (primary) — 전문성, 신뢰 */
--color-navy-50 ~ --color-navy-950

/* Brand Orange palette (accent) — CTA, 강조 */
--color-brand-50 ~ --color-brand-950

/* Gray (neutral) */
--color-gray-50 ~ --color-gray-950
```

### Tier 2: Semantic Token

| Token | 값 | 용도 |
|-------|---|------|
| `--color-bg-primary` | navy-50 | 페이지 배경 |
| `--color-bg-surface` | white | 카드/섹션 배경 |
| `--color-bg-surface-hover` | navy-100 | 카드 호버 |
| `--color-bg-accent` | brand-500 | CTA 버튼 |
| `--color-bg-accent-hover` | brand-600 | CTA 호버 |
| `--color-bg-brand` | navy-800 | 브랜드 배경 |
| `--color-bg-brand-hover` | navy-700 | 브랜드 호버 |
| `--color-text-primary` | navy-900 | 제목/라벨 |
| `--color-text-secondary` | navy-600 | 본문 텍스트 |
| `--color-text-tertiary` | navy-400 | 힌트/캡션 |
| `--color-text-on-accent` | white | CTA 버튼 위 |
| `--color-text-on-brand` | white | 브랜드 배경 위 |
| `--color-text-accent` | brand-600 | 링크/강조 |
| `--color-border-default` | navy-200 | 기본 테두리 |
| `--color-border-strong` | navy-400 | 강한 테두리 |
| `--color-border-accent` | brand-500 | 포커스/활성 |
| `--color-focus-ring` | navy-800 | 포커스 링 |

**상태 색상**: red(error), green(success), yellow(warning)

---

## 3. 절대 규칙

### MUST
1. **Seed Design 컴포넌트 우선**: 있으면 반드시 사용, 없을 때만 커스텀
2. **모든 색상은 Semantic Token**: `bg-[--color-bg-surface]` (O), `bg-white` (X)
3. **Semantic 없으면 Scale Token**: `bg-navy-500` (차선), hex 하드코딩 (X)
4. **CTA 버튼**: `--color-bg-accent` + hover + glow 효과
5. **브랜드 헤더**: `bg-[--color-bg-brand]` 또는 `from-navy-800 to-brand-500` 그라데이션
6. **포커스 링**: `ring-[--color-focus-ring]`

### MUST NOT
1. Hex/RGB 하드코딩 금지 (tokens.css @theme 제외)
2. 임의 색상 변수 생성 금지
3. `!important` 금지 (접근성 오버라이드 제외)
4. Seed Design에 있는 컴포넌트를 직접 구현 금지

---

## 4. 컴포넌트 패턴 (커스텀)

### Card
```tsx
<div className="bg-[--color-bg-surface] border border-[--color-border-default] rounded-xl shadow-card hover:shadow-card-hover p-5 transition-all">
  <h3 className="text-[--color-text-primary] text-lg font-semibold">제목</h3>
  <p className="text-[--color-text-secondary] text-sm mt-2">설명</p>
</div>
```

### Header Gradient
```tsx
<div className="bg-gradient-to-r from-navy-800 to-brand-500 rounded-xl p-6 text-white">
  <h2 className="text-xl font-bold">섹션 제목</h2>
</div>
```

### Glass Effect
```tsx
<nav className="bg-white/80 backdrop-blur-lg border-b border-[--color-border-default]/50">
```

---

## 5. 타이포그래피

**Font Stack**: `'Pretendard Variable', Pretendard, -apple-system, system-ui, sans-serif`

| Role | Size | Weight |
|------|------|--------|
| Display | 2.25rem (36px) | Bold 700 |
| H1 | 1.875rem (30px) | Semibold 600 |
| H2 | 1.5rem (24px) | Semibold 600 |
| H3 | 1.25rem (20px) | Medium 500 |
| Body Large | 1.125rem (18px) | Regular 400 |
| Body | 1rem (16px) | Regular 400 |
| Body Small | 0.875rem (14px) | Regular 400 |
| Caption | 0.75rem (12px) | Regular 400 |

---

## 6. 검증 체크리스트

코드 작성 후 반드시 확인:

- [ ] Seed Design 컴포넌트가 있는데 직접 구현하지 않았는지
- [ ] Hex/RGB 하드코딩 없음 (tokens.css 제외)
- [ ] CTA 버튼에 `--color-bg-accent` 사용
- [ ] 텍스트에 `--color-text-primary/secondary/tertiary` 사용
- [ ] 포커스 스타일에 `--color-focus-ring` 사용
- [ ] 반응형 간격 (모바일: p-4, 데스크톱: p-6~8)
- [ ] `prefers-reduced-motion` 대응

---

## 7. 파일 참조

| 파일 | 역할 |
|------|------|
| `packages/ui/src/styles/tokens.css` | Scale + Semantic Token 정의 |
| `packages/ui/src/styles/index.css` | base.css + tokens + 글로벌 스타일 |
| `packages/ui/src/seed-design/ui/` | Seed Design CLI 생성 컴포넌트 |
| `packages/ui/src/index.ts` | 컴포넌트 export |
| `packages/ui/seed-design.json` | Seed Design CLI 설정 |
| `packages/*/vite.config.ts` | seedDesignPlugin() + tailwindcss() |
| `references/seed-design-catalog.md` | 전체 컴포넌트 카탈로그 |
