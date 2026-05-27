---
name: mdx-render
description: Use when converting a finalized 3-Zone chapter YAML (plus optional dashboard.yml) into Docusaurus MDX files — generating frontmatter with authors/ai_assisted/source metadata, importing custom components, placing components in the editor-specified render_order, writing the /appendix dashboard page, and preserving backups of previously written MDX. Also use when deciding which part-XX/ folder a chapter belongs to.
---

# mdx-render

## Overview

파이프라인 최종 단계. 편집·보강 완료된 YAML을 독자가 볼 Docusaurus MDX 파일로 출력한다. Human-only 필드는 커스텀 컴포넌트 `props`로만 전달해 "사람 영역"임이 시각적으로도 드러나게 한다.

**어투와 섹션 이모지:** 렌더링 시 추가하는 H2/H3 헤딩(예: "👃 코드 냄새 맡아보기", "✏️ 개선해보기")과 산문 브릿지는 `writing-voice-ff` 스킬의 역할형 이모지 표와 해요체 원칙을 따른다. 커스텀 컴포넌트 내부 텍스트는 YAML literal 그대로 (어투 가이드 적용 안 함).

## When to Use

- chapter-editor + fe-content-enhancer 산출물이 준비되고 최종 MDX 생성이 필요할 때
- aggregator 대시보드 YAML로 /appendix 페이지를 만들 때
- 기존 MDX를 덮어쓸 때 (백업 포함)

## 출력 파일 위치

| 대상 | 경로 | 매핑 규칙 |
|---|---|---|
| 챕터 MDX | `docs/part-{NN}/ch{XX}.mdx` | 장수 → Part 매핑 표 참조 |
| 부록 대시보드 | `docs/appendix/dashboard.mdx` | 고정 경로 |
| 백업 | `_workspace/_prev/{timestamp}/{원경로}` | 타임스탬프 폴더 |

### 장수 → Part 매핑

| 장수 | Part |
|---|---|
| 1~4 | part-01 |
| 5~9 | part-02 |
| 10~13 | part-03 |
| 14~19 | part-04 |
| 20~24 | part-05 |
| 25~31 | part-06 |
| 32~35 | part-07 |

## Frontmatter 필수 필드

```yaml
---
sidebar_position: 5                       # 장수 그대로
title: "Chapter 5. 고급 변수 종류"         # meta.title 그대로
description: "..."                        # summary.lead 1문장
authors:                                  # opinions 작성 멤버 + devils_advocate 작성자 (중복 제거)
  - Alice
  - diego
ai_assisted:                              # AI가 손댄 섹션만 나열
  - summary
  - code_examples
  - checklist
  - verdict.rationale                     # AI가 초안 제공한 경우만
source: notion-pull
source_page_id: xxx
extracted_at: 2026-04-18T22:30:00+09:00
edited_at: 2026-04-18T22:45:00+09:00
---
```

## 컴포넌트 import (모든 챕터 공통)

```mdx
import Verdict from '@site/src/components/Verdict';
import MemberOpinion from '@site/src/components/MemberOpinion';
import VotingBar from '@site/src/components/VotingBar';
import DevilsAdvocate from '@site/src/components/DevilsAdvocate';
import BestPickCallout from '@site/src/components/BestPickCallout';
```

부록 전용:

```mdx
import VerdictDistribution from '@site/src/components/VerdictDistribution';
import BestDiscussions from '@site/src/components/BestDiscussions';
```

## 챕터 MDX 템플릿 (render_order 준수)

YAML `render_order`가 지정한 순서대로 섹션 출력. 기본값 예시:

```mdx
---
<frontmatter>
---

<imports>

<Verdict rating="🟢 생존" rationale="..." />

## 📝 핵심 요약

{lead}

- {bullets[0]}
- {bullets[1]}
- {bullets[2]}

{bridges.after_summary ?? ''}

<VotingBar average={4.2} votes={{ Alice: 4, Amber: 5, Crong: 3, diego: 4, Jay: 5, Leo: 4, zinii: 3 }} />

## 💻 React/TS 코드 예제

### {code_examples[0].title}

**Before ❌**

```typescript
{code_examples[0].before}
```

**After ✅**

```typescript
{code_examples[0].after}
```

## 🔥 토론 포인트 & 생각해볼 질문

1. {discussion_questions[0]}
2. {discussion_questions[1]}
3. {discussion_questions[2]}

{bridges.before_opinions ?? ''}

## 💬 멤버 의견

<MemberOpinion author="Alice" emoji="🦊" opinion="..." experience="..." />
<MemberOpinion author="Amber" emoji="🐵" opinion="..." experience="..." />
<!-- ... 7명 -->

<DevilsAdvocate author="diego" argument="..." />

## ✅ FE 실전 체크리스트

- [ ] {checklist[0].text} — 관련 ESLint: [`{rule}`]({rule_url})
- [ ] {checklist[1].text}

<BestPickCallout content="..." reason="..." />
```

## 부록 MDX 템플릿

```mdx
---
sidebar_position: 99
title: "📊 스터디 대시보드"
description: "Code Complete 스터디 전체 집계 — 판정 분포, 투표 평균, 베스트 토론"
---

import VerdictDistribution from '@site/src/components/VerdictDistribution';
import BestDiscussions from '@site/src/components/BestDiscussions';

## 스터디 진행 현황

- 진행된 챕터: {chapters_included}
- 참여 멤버: {members_count}명

## ⚖️ 판정 분포

<VerdictDistribution alive={5} evolved={2} dead={1} />

## 📊 투표 요약

- 전체 평균: **{overall_average}** / 5

### 챕터별 평균

| 챕터 | 평균 | 판정 |
|---|---|---|
| ch01 | 4.2 | 🟢 생존 |
| ch02 | 3.5 | 🟡 변형 |

### 최고 평가 TOP 3

1. Chapter 5 — 고급 변수 종류 (4.7)

### 최저 평가 TOP 3

1. Chapter 6 — ... (2.1)

## 💎 베스트 토론

<BestDiscussions items={[...]} />

## 😈 Devil's Advocate 모음

> **ch05 (diego):** ...

## 멤버 활동

| 멤버 | 의견 작성 | 반박 담당 | 투표 제출 |
|---|---|---|---|
| Alice 🦊 | 8 | 1 | 8 |
```

## 렌더 규칙

1. **빈 필드 처리:**
   - `member_opinions`에서 opinion 없는 멤버 → 해당 `<MemberOpinion>` 태그 자체를 생략 (빈 말풍선 금지)
   - `devils_advocate` null → `<DevilsAdvocate>` 섹션 전체 생략
   - `best_pick.content` null → `<BestPickCallout>` 생략
   - `code_examples` 0개 → "💻 React/TS 코드 예제" H2도 생략
2. **MDX 특수문자 이스케이프:** `{`, `}` → `&#123;`, `&#125;` (코드 블록 외)
3. **사이드바 순서:** `sidebar_position`은 장수 그대로. 테마 재배치 시 별도 `sidebars.ts` 수정 (이 스킬 범위 밖)
4. **검증:** 출력 직후 `npm run docusaurus build --dry-run`이 가능한 상태여야 함 (실제 실행은 호출자 책임)

## 백업 규칙

기존 `docs/part-NN/chXX.mdx` 존재 시:
1. `_workspace/_prev/{YYYYMMDD-HHMMSS}/docs/part-NN/chXX.mdx`로 복사
2. 원본 위치 덮어쓰기
3. git 저장소면 diff로도 추적 가능하지만 안전장치 유지

## Common Mistakes

| 실수 | 결과 | 수정 |
|---|---|---|
| `opinion` props 텍스트에 줄바꿈 | JSX 렌더 깨짐 | `\n`을 `{"\n"}` 또는 `<br />`로 |
| authors에 zinii 누락 (opinion 없음) | 기여 없는 사람이 author로 기록 | opinions/advocate 작성자만 authors |
| frontmatter에 ai_assisted 빈 배열 | false 인상 (AI 무개입처럼 보임) | 최소 `[]` 명시, null/생략 금지 |
| sidebar_position을 render_order로 혼동 | 사이드바 순서 뒤죽박죽 | sidebar_position은 항상 장수 |
