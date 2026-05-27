---
name: fsd-docs
description: >-
  Feature-Sliced Design (FSD) v2.1 공식 문서를 Progressive Disclosure 방식으로 제공하는 지식 스킬.
  레이어/슬라이스/세그먼트, Public API, cross-imports, v2.0→v2.1 pages-first 마이그레이션,
  Next.js·NuxtJS·React Query·SvelteKit·Electron 통합, Authentication·i18n·Types·Theme·SSR 등 실무 가이드를 포함한다.
  사용자가 FSD·Feature-Sliced·레이어 구조·슬라이스·pages-first·FSD 도입/마이그레이션을 언급하거나,
  프론트엔드 폴더 구조·아키텍처 방법론에 대해 질문할 때 참고할 관련 섹션을 references/ 에서 로드해 답한다.
  Triggers — "FSD", "Feature-Sliced", "레이어", "슬라이스", "pages-first", "v2.1 마이그레이션", "FSD 도입", "프론트엔드 아키텍처".
license: MIT
---

# Feature-Sliced Design (FSD) Knowledge Skill

FSD v2.1 공식 문서를 주제별로 분할한 지식 스킬. 본 SKILL.md는 **인덱스 + 라우팅 테이블** 역할만 한다. 실제 지식은 `references/` 의 해당 섹션을 **필요할 때만** 읽어서 사용한다.

## 사용 원칙

1. 사용자가 FSD 관련 질문을 하면 **먼저 아래 라우팅 테이블에서 관련 섹션 1~2개만** 선택해 로드한다. 전체 references 를 한 번에 읽지 않는다.
2. `references/` 의 각 파일은 frontmatter에 `section`, `source`, `license` 를 명시한 독립 md. 줄 수는 170–2400 범위.
3. 답변 시 원문에서 인용한 구절이 있으면 출처를 `references/XX.md` 로 간단히 명시.

## 라우팅 테이블

| 사용자 질문 유형 | 로드할 파일 |
|---|---|
| "FSD가 뭐야?", "개요", "적합한가?" | [`00-overview.md`](references/00-overview.md) |
| "레이어 구조", "app/pages/widgets/features/entities/shared", "Public API 규칙", "슬라이스·세그먼트 정의" | [`01-core-reference.md`](references/01-core-reference.md) |
| "FSD 실제 예제", "처음 만들 때 어떻게", "어떻게 나눠?", "step-by-step" | [`02-tutorial.md`](references/02-tutorial.md) |
| "cross-import 되나?", "같은 레이어 import", "desegmentation", "excessive entities", "routing 어디?" | [`03-cross-imports-and-antipatterns.md`](references/03-cross-imports-and-antipatterns.md) |
| **"v2.0에서 v2.1로 어떻게 옮겨?"**, **"pages-first 마이그레이션"**, "v1→v2", "기존 커스텀 아키텍처에서 FSD로" | [`04-migration.md`](references/04-migration.md) ⭐ |
| "Next.js + FSD", "NuxtJS + FSD", "SvelteKit", "Electron", "React Query 어떻게 배치" | [`05-framework-integrations.md`](references/05-framework-integrations.md) |
| "API 요청 어디 둬?", "인증", "i18n", "타입 어디", "페이지 레이아웃", "테마", "SSR", "모노레포" | [`06-practical-guides.md`](references/06-practical-guides.md) |
| "왜 FSD?", "다른 아키텍처와 비교 (DDD, Clean Architecture, Atomic Design)", "네이밍", "미션/철학", "FAQ" | [`07-philosophy-and-faq.md`](references/07-philosophy-and-faq.md) |

## 자주 묻는 조합

- **"우리 프로젝트에 FSD 도입해도 될까?"** → `00-overview.md` (Is it right for me) + `07-philosophy-and-faq.md` (When not needed)
- **"기존 코드를 FSD로 마이그레이션하려면?"** → `04-migration.md` (Custom → FSD 섹션) + `00-overview.md` (Incremental adoption)
- **"v2.1로 올리려면 얼마나 고쳐야 해?"** → `04-migration.md` (v2.0→v2.1 섹션, 가장 짧음)
- **"FSD에서 Redux/React Query 상태는 어디?"** → `06-practical-guides.md` (Types/API 섹션) + `05-framework-integrations.md` (React Query 섹션)
- **"features와 entities 구분이 애매한데?"** → `03-cross-imports-and-antipatterns.md` (Excessive Entities) + `01-core-reference.md` (Layer definitions)

## 메타데이터

- 문서 버전: FSD v2.1 (현재)
- 원문 출처: https://feature-sliced.design/llms-full.txt
- 수집일: 2026-04-18
- 저작권: © 2018-2025 Feature-Sliced Design. MIT License. [`LICENSE.md`](LICENSE.md) 참조.
- 원문 repo: https://github.com/feature-sliced/documentation

## 갱신

원문이 갱신되면 [`docs-to-md`](../docs-to-md/SKILL.md) 스킬을 이용해 llms-full.txt 를 다시 받고, 이 스킬의 `references/` 파일들을 재추출한다. 추출 range는 섹션 헤딩 기준(`# Overview`, `# Layers`, `# Migration from v2.0 to v2.1` 등)으로 결정.
