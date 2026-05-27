---
name: onda-slides
description: ONDA 공통 템플릿으로 슬라이드 프레젠테이션(HTML + PDF)을 생성한다. 차트, 표, 그리드, AI 이미지 지원. 모디파이어로 simple/wide/dark/en/confidential 조합.
disable-model-invocation: false
argument-hint: "[modifier...] <슬라이드 데이터 또는 지시사항>"
allowed-tools: Bash, Bash(pip3 install *), Bash(python3 *), Bash(npm *), Bash(node *), Read, Write, Edit, Glob, Grep, Agent, AskUserQuestion
---

# ONDA Slides

브랜드 일관 슬라이드를 **마크업만** 작성해서 만든다. CSS / JS / 자동 fit 알고리즘은 모두 `template/` 디렉토리에 분리되어 있고, `build.mjs`가 슬라이드 fragment + 보일러플레이트를 합쳐 self-contained HTML을 생성한다. PDF는 `gen_pdf.mjs`가 Puppeteer + pdf-lib으로 만든다.

## 파일 구조

```
plugins/onda-slides/skills/onda-slides/
├── SKILL.md              ← 본 파일 (컴포넌트 사용법 + 워크플로우)
├── template/
│   ├── base.html         ← HTML skeleton (placeholders)
│   ├── styles.css        ← 모든 CSS — 수정 시 모든 슬라이드 영향
│   └── runtime.js        ← 화면 모드 JS (네비, 풀스크린, auto-fit)
├── build.mjs             ← slides fragment + 템플릿 → 완성 HTML
└── gen_pdf.mjs           ← HTML → PDF
```

**LLM이 작성하는 것**: 슬라이드 마크업 (`<div class="slide">...</div>` 들) — slides fragment 1개 파일.
**LLM이 건드리지 않는 것**: `template/`, `build.mjs`, `gen_pdf.mjs` (디자인 변경 요청이 아니라면).

> **⛔ ASCII 다이어그램·아스키 아트 금지** — 이 스킬은 HTML 슬라이드. `<pre>`나 monospace로 박스/화살표/트리/카드 그림 그리지 말 것. 프로세스/구조/관계는 반드시 정식 컴포넌트(`.flow`, `.g2/.g3`, `.card`, `.svc-badge`, `.dt`)로. 부족하면 inline HTML + `style="..."`로 직접 그려도 OK — 그래도 글자 그림은 금지. 일반 채팅 응답에서 ASCII 다이어그램 쓰는 습관을 슬라이드로 가져오는 실수가 흔하다.

## Input

`$ARGUMENTS` — `[modifier...] <슬라이드 데이터>`

### Modifier (선택, 공백 구분, 맨 앞, 여러 개 조합)

각 modifier는 직교 축이라 자유 조합 가능.

| modifier | 축 | 효과 |
| --- | --- | --- |
| `simple` | 콘텐츠 절제 | 비전문가 대상 콘텐츠 룰 강제 (한 메시지/슬라이드, `.g2`만, 불렛 3개 이하). **CSS는 default와 동일** — 콘텐츠가 절제되어 자동 fit이 큰 폰트를 유지함 |
| `wide` | 화면 비율 | 16:9 (13.33in × 7.5in, PowerPoint/Google Slides 표준). 기본은 A4 landscape |
| `dark` | 테마 | 다크 모드. 야간 행사 / 어두운 발표장 |
| `en` | 언어 | 영문 폰트(Inter). 기본은 Pretendard |
| `confidential` | 보안 표시 | 모든 슬라이드에 대각선 `CONFIDENTIAL` 워터마크 + footer 경고문구. 사외 유출 금지 자료 |

> default 자체에 자동 fit. 슬라이드별 콘텐츠 양에 맞춰 base font-size를 조정한다 (콘텐츠 적으면 큰 폰트 + 정중앙, 많으면 비례 축소).

### 파싱 규칙

`$ARGUMENTS`를 공백 split 후, **앞에서부터** 위 표 토큰을 modifier로 빨아들인다. 모르는 토큰을 만나면 멈추고 나머지는 슬라이드 데이터.

```
/onda-slides 매출 보고서                  → modifiers=[],          content="매출 보고서"
/onda-slides simple 매출 보고서           → modifiers=[simple],    content="매출 보고서"
/onda-slides simple wide 매출 보고서      → modifiers=[simple,wide], content="..."
/onda-slides wide dark en IR deck         → modifiers=[wide,dark,en], content="IR deck"
/onda-slides confidential 보안 자료        → modifiers=[confidential], content="보안 자료"
/onda-slides wide dark confidential 이사회 → modifiers=[wide,dark,confidential], content="이사회"
/onda-slides 매출 simple                  → modifiers=[], content="매출 simple"
                                           (첫 토큰이 modifier 아니면 즉시 멈춤)
```

## 워크플로우

### Phase 0: 미지정 modifier 차원 → 한 번에 질문

slides는 5개 직교 차원이 있고 각각 default가 있다. `$ARGUMENTS`에 **명시되지 않은 차원**이 하나라도 있으면 슬라이드 작성 전에 **AskUserQuestion 1회 호출**로 미지정 차원을 모아서 묻는다 (`questions` 배열에 N개, N = 미지정 차원 수).

| 차원 | default | modifier 키워드 | 질문 옵션 |
| --- | --- | --- | --- |
| 화면 비율 | A4 landscape | `wide` | `default (A4)` / `wide (16:9, PowerPoint 표준)` |
| 테마 | light | `dark` | `light` / `dark (야간 행사 / 어두운 발표장)` |
| 언어 | 한글 (Pretendard) | `en` | `한글` / `영문 (Inter)` |
| 콘텐츠 스타일 | 전문가/실무자 | `simple` | `default` / `simple (비전문가, 한 메시지/슬라이드, 큰 폰트)` |
| 보안 표시 | 없음 | `confidential` | `없음` / `confidential (대각선 워터마크 + 경고문구)` |

**명시된 차원은 스킵**, 미지정 차원만 questions 배열에 담아 1회 호출. 한 차원당 popup으로 끊어 묻지 말 것 — 마찰 비용. `$ARGUMENTS`에 modifier 토큰이 하나도 없으면 5개 모두 질문.

추측해서 default로 자동 진행 ❌ — 사용자가 직접 선택해야 한다 (특히 `confidential`은 보안 의도라 default 가정 위험).

### Phase 1: 정보 수집

출력 경로 미지정 시 `$PWD`. 파일명은 제목에서 자동 (공백→`_`, 특수문자 제거):
- HTML: `$PWD/{파일명}.html`
- PDF:  `$PWD/{파일명}.pdf`

부족하면 확인:
1. **출력 경로**: 별도 지정 시에만 질문 (기본 `$PWD`)
2. **기본 정보**: 제목, 부제목, 날짜
3. **로고**: 이미지 파일 또는 base64 (없으면 ONDA 공식 로고)
4. **커버 chip 태그** (`.cover-foot .products`): 자료 주제와 관련된 ONDA 제품·기능 2-4개 (예: `ONDA HUB`, `Channel Manager`, `CRS`, `Google FBL`, `PMS`). 자료 성격상 무관하면 생략 가능. 주제로부터 자동 추론 가능 (예: "채널 관리 효율화" → `Channel Manager`, `ONDA HUB`)
5. **슬라이드 내용**: 각 슬라이드 헤더 / 불렛 / 차트 / 표 / 그리드
6. **작성자 정보** (closing 슬라이드용): **모든 필드를 AskUserQuestion 1회 호출로 묻기**. 텍스트로 "이렇게 채웠는데 다르면 말해주세요" 식으로 자동 진행 ❌ — 반드시 AskUserQuestion 옵션/입력.
   - **prefill 소스 우선순위 (이 순서로 체크)**:
     1. 메모리(`user_*`/`feedback_*` 타입에서 사용자 본인으로 식별된 정보) — 사용자가 직접 알려준 신뢰값
     2. global/project CLAUDE.md에 명시된 사용자 정보
     3. 시스템 컨텍스트 user profile (예: `userEmail`)
     4. 현재 대화에서 사용자가 직접 언급한 정보
     5. (마지막 fallback) `git config user.name`/`user.email` — 머신 설정값이라 신뢰도 낮음. 1-4가 모두 비어 있을 때만 조심스럽게 사용. 영문 이름/공용 계정/다른 사람 셋업 가능성 인지하고 AskUserQuestion에서 prefill일 뿐 자동 확정 금지.
   - **prefill도 raw copy일 때만** — 음역(영↔한)·번역·약어 풀이·도메인 추론은 추측 → 빈 값. 필드 언어/스크립트/포맷이 소스와 다르면 무조건 미지.
   - **AskUserQuestion 구성**: 모든 필드(prefill값+미지)를 1회 호출(`questions` 배열)에 담아 1 popup으로. prefill 가능한 필드는 옵션 첫 번째로 그 값 + "직접 입력 →" 옵션 함께. 미지 필드는 자유 입력 + "비워두기" 옵션.
   - **신규 입력값 저장 제안**: 사용자가 직접 입력해서 채운 필드(prefill 1-4 소스에 없던 값)가 있으면, 슬라이드 빌드 직전에 한 번 더 가벼운 질문 — "이 작성자 정보를 global CLAUDE.md(`~/.claude/CLAUDE.md`)에 저장해둘까요? 다음부터는 자동으로 prefill됩니다" → yes면 CLAUDE.md에 사용자 식별 섹션 추가/업데이트, no면 이번만 사용. 한 번 저장되면 다음 호출부터 prefill 1순위(메모리/CLAUDE.md)에서 raw copy로 잡혀 popup 마찰 없음.

### Phase 2: 슬라이드 fragment 작성

`<div class="slide">...</div>` 들을 **연달아만** 담은 fragment 파일을 작성한다. `<html>`, `<head>`, `<body>`, `<style>`, `<script>` 다 빼고 슬라이드 본체만.

`fragment.html` 예:
```html
<div class="slide active" id="s0">
  <div class="cover-accent"></div>
  ...커버 내용...
</div>

<div class="slide" id="s1">
  <div class="accent"></div>
  <div class="hbar"><h2>제목</h2></div>
  <div class="body">...</div>
  <div class="foot">...</div>
</div>
```

→ Write 또는 임시 파일 (`/tmp/slides-XXXX.html`).

### Phase 3: HTML 빌드

```bash
node "${CLAUDE_SKILL_DIR}/build.mjs" <fragment> <output.html> \
  --modifiers simple,wide \
  --title "슬라이드 제목"
```

- `--modifiers`: 쉼표 구분. 생략 시 default
- `--title`: 생략 시 fragment의 첫 `<h1>`/`<h2>`에서 추출

`build.mjs`가 `template/styles.css`와 `template/runtime.js`를 inline으로 박아 self-contained HTML을 만든다.

### Phase 4: PDF 생성

```bash
npm ls puppeteer pdf-lib 2>/dev/null || npm install puppeteer pdf-lib
node "${CLAUDE_SKILL_DIR}/gen_pdf.mjs" <output.html> [output.pdf]
```

`gen_pdf.mjs`는 `<body class="mode-wide">`를 감지해 PDF 페이지 사이즈를 16:9로 자동 전환한다.

### Phase 5: 완료 보고

- HTML 경로 / PDF 경로(용량) / 슬라이드 수
- 브라우저 확인: `file://` URL
- 화면 조작: → / Space / 클릭 (다음), ← (이전), Home/End, **F** (풀스크린)

## 콘텐츠 원칙 (modifier 별)

### default — 자유 콘텐츠 (자동 fit이 처리)

JS fit이 슬라이드별 base font-size를 조정한다.
- 콘텐츠 적은 슬라이드 → 큰 폰트(불렛 32px, 카드 value 56px) + 정중앙
- 콘텐츠 많은 슬라이드 → 비례 축소 (최소 base 6px)

다만 너무 빽빽하면 글씨가 작아진다. 한 슬라이드에 정보가 정말 많으면 두 슬라이드로 분할이 가독성 좋다.

- 불렛 개수 제한 없음 (단, 7개 넘으면 분할 검토)
- `.g2`, `.g2w`, `.g3`, `.g4` 모두 허용
- 차트 적극 활용 (차트 슬라이드는 fit 대상 제외 — 모델이 적정 양 조정)
- 표 행 수 제한 없음 (너무 많으면 fit으로 작아짐)
- **flow / svc-badge / card.featured / bullet variant 적극 활용** — 글씨 나열 대신 시각화. inline HTML/style도 자유

### simple — 비전문가 대상

숙박업주, 일반 고객 등 큰 화면에서 멀리서 보는 청중. **CSS는 default와 동일**하지만 모델이 콘텐츠 자체를 절제 → 자동 fit이 큰 폰트 유지.

1. **한 슬라이드 = 한 메시지**
2. **불렛 최대 3개**
3. **그리드 `.g2`만** (`.g3`, `.g4`, `.g2w` 금지)
4. **차트 심플**: 범례 최소화, 데이터 포인트 7개 이하
5. **텍스트 짧게**: 불렛 1줄 25자 이내, 키워드
6. **표 행 4개 이하**
7. **한 슬라이드 한 컴포넌트** (불렛/Stat/카드/표/flow 중 하나만)
8. **flow는 최대 4단계** (5+이면 핵심만 추려 단순화)
9. **svc-badge / card.featured / bullet variant**는 가독성 도움 → 적극 사용. inline HTML도 OK

## 컴포넌트 마크업 가이드

### 브랜드 토큰 (참고용 — CSS는 styles.css 고정)

```
Primary Blue   : #004FC5
Dark Text      : #191F28    Body Text      : #333D4B
Secondary Text : #4E5968    Light Text     : #8B95A1
Border         : #E5E8EB    Row Stripe     : #F2F4F6
```

### 슬라이드 구조

3가지 타입: **커버 / 섹션구분 / 콘텐츠**.

#### 커버 슬라이드

```html
<div class="slide active" id="s0">
  <div class="cover-accent"></div>
  <div class="cover-header">
    <img class="onda-logo"
         src="https://cdn.prod.website-files.com/62fc3cdcd1a5bb1370c2d067/63c0a7b567846c336d75f050_onda.svg"
         alt="ONDA" />
    <div class="tagline">Hospitality Connectivity Platform</div>
  </div>
  <div class="cover-body">
    <h1>제목</h1>
    <div class="sub">부제목 설명</div>
    <div class="date">2026.04</div>
  </div>
  <div class="cover-foot">
    <!-- products: 발표 주제와 관련된 ONDA 제품·기능 chip 태그를 2-4개 박는다.
         예: ONDA HUB, CRS, Channel Manager, Google FBL, PMS 등.
         자료 성격상 무관하면 비워둬도 됨 (예: 사내 회의록). -->
    <div class="products">
      <span class="pill">ONDA HUB</span>
      <span class="pill">Channel Manager</span>
      <span class="pill">CRS</span>
    </div>
    <div class="web">onda.me</div>
  </div>
</div>
```

#### 섹션 구분 슬라이드

```html
<div class="slide" id="s1">
  <div class="accent"></div>
  <div class="section-content">
    <h1>01</h1>
    <div class="sub">섹션 제목</div>
  </div>
  <div class="foot">
    <div class="copyright">&copy; ONDA Inc.</div>
    <div class="snum">2 / 8</div>
  </div>
</div>
```

#### 콘텐츠 슬라이드

```html
<div class="slide" id="s2">
  <div class="accent"></div>
  <div class="hbar">
    <h2>슬라이드 제목</h2>
    <div class="hdesc">슬라이드 부제 (선택)</div>
  </div>
  <div class="body">
    <!-- 여기에 컴포넌트들. JS가 .body-fit 자동 wrap -->
  </div>
  <div class="foot">
    <div class="copyright">&copy; ONDA Inc.</div>
    <div class="snum">3 / 8</div>
  </div>
</div>
```

#### 클로징 슬라이드 — **항상 마지막에** 추가 (권장)

```html
<!-- s{{LAST}} / {{LAST_INDEX}} / {{TOTAL}}은 실제 숫자로 교체 (예: id="s7", "8 / 8") -->
<div class="slide" id="s{{LAST}}">
  <div class="accent"></div>
  <div class="closing-content">
    <img class="onda-logo"
         src="https://cdn.prod.website-files.com/62fc3cdcd1a5bb1370c2d067/63c0a7b567846c336d75f050_onda.svg"
         alt="ONDA" />
    <div class="thanks">감사합니다</div>
    <div class="closing-author">
      <div class="name">{{작성자 이름}} ({{영문 별칭}})</div>
      <div class="title">{{직책}}, {{회사}}</div>
      <div class="contact">{{이메일}} · {{연락처}}</div>
    </div>
  </div>
  <div class="foot">
    <div class="copyright">&copy; ONDA Inc.</div>
    <div class="snum">{{LAST_INDEX}} / {{TOTAL}}</div>
  </div>
</div>
```

작성자 정보 채우는 절차 (Phase 1 #6 참고):
1. prefill 소스 우선순위: 메모리 → CLAUDE.md → 시스템 user profile → 현재 대화 → (마지막 fallback) `git config`. git config는 머신 설정이라 신뢰도 낮음 — 1-4 비어있을 때만, 자동 확정 금지
2. raw copy일 때만 prefill — 음역/번역/추론은 추측이라 미지 처리
3. **모든 필드를 AskUserQuestion 1회 호출에 담아 prefill+확인** — prefill값은 옵션 첫 번째 + "직접 입력" 옵션, 미지는 자유 입력
4. "그럴듯한 값으로 채우고 다르면 말해주세요" 식 자동 진행 ❌

`build.mjs`는 클로징 슬라이드 누락 시 **경고만** 출력하고 빌드는 진행 — 강제 아님.

### 컴포넌트

```html
<!-- 섹션 타이틀 -->
<div class="stitle">섹션 제목</div>

<!-- 불렛 (강조: <span class="hl">...</span>) -->
<ul class="bl">
  <li>일반 항목</li>
  <li>강조: <span class="hl">키워드</span> 포함</li>
</ul>

<!-- 카드 + 그리드 -->
<div class="g3">
  <div class="card">
    <div class="card-title">카드 제목</div>
    <div class="card-value">1,234</div>
    <div class="card-desc">설명</div>
  </div>
  <!-- ... -->
</div>

<!-- Stat 바 -->
<div class="stats">
  <div class="stat-item">
    <div class="stat-num">37K+</div>
    <div class="stat-label">Properties</div>
  </div>
  <div class="stat-divider"></div>
  <div class="stat-item">
    <div class="stat-num">71+</div>
    <div class="stat-label">Channels</div>
  </div>
</div>

<!-- 표 -->
<table class="dt">
  <thead><tr><th>항목</th><th>값</th></tr></thead>
  <tbody>
    <tr><td>데이터</td><td>값</td></tr>
  </tbody>
</table>

<!-- Pill -->
<span class="pill">태그</span>

<!-- 구분선 -->
<div class="divider"></div>

<!-- Flow 다이어그램 (프로세스/구조/경로 시각화) -->
<!-- variant: 기본(outline) / .alt(solid blue) / .accent(orange) / .muted(gray) -->
<div class="flow">
  <div class="flow-step muted">Opera PMS</div>
  <span class="flow-arrow">→</span>
  <div class="flow-step">블루웨이브</div>
  <span class="flow-arrow">→</span>
  <div class="flow-step alt">ONDA</div>
  <span class="flow-arrow">→</span>
  <div class="flow-step">Google Hotel Center</div>
  <span class="flow-arrow">→</span>
  <div class="flow-step accent">shillahotels.com</div>
</div>
<!-- step에 부가설명 넣을 때 -->
<div class="flow-step alt">
  ONDA<span class="flow-desc">수수료 차감</span>
</div>

<!-- 추천 카드 + 코너 배지 ("권장" / "BEST" 등) -->
<div class="g2">
  <div class="card">
    <div class="card-title">옵션 A: Google Maps 전용</div>
    <div class="card-value">3.0%</div>
    <div class="card-desc">거래액 기준 수수료</div>
    <ul class="bl">
      <li class="check">Google Maps Official Website 노출</li>
      <li class="check">투숙 완료 건 기준 정산</li>
      <li class="dim">네이버 지도 노출</li>
      <li class="dim">카카오맵 노출</li>
    </ul>
  </div>
  <div class="card featured">
    <span class="card-badge">권장</span>
    <div class="card-title">옵션 B: 3대 맵서비스 패키지</div>
    <div class="card-value">2.0% / 10% / 10%</div>
    <div class="card-desc">Google / 네이버 / 카카오</div>
    <ul class="bl">
      <li class="check">Google Maps Official Website (2.0%)</li>
      <li class="check">네이버 지도 호텔 검색 (10.0%)</li>
      <li class="check">카카오맵 호텔 검색 (10.0%)</li>
    </ul>
  </div>
</div>

<!-- 서비스 아이콘 배지 (헤더 위 브랜드 라벨) -->
<!-- variant: .google / .naver / .kakao / 미지정(기본 blue) -->
<div class="svc-badge">
  <span class="svc-icon google">G</span> Google Maps
</div>
<div class="svc-badge">
  <span class="svc-icon naver">N</span> 네이버 지도
</div>
<div class="svc-badge">
  <span class="svc-icon kakao">K</span> 카카오맵
</div>
```

#### 이미지 그리드 (스크린샷 비교 등)

`.slide-img`(컨테이너 폭 맞춤, max-height 26em)를 `.g2/.g3/.g4` 안에 넣어 mobile 스크린샷 2-4개를 나란히 배치:

```html
<div class="g3">
  <img class="slide-img" src="screenshot-1.png" alt="검색 결과">
  <img class="slide-img" src="screenshot-2.png" alt="상세 화면">
  <img class="slide-img" src="screenshot-3.png" alt="예약 옵션">
</div>
```

#### Custom inline HTML/style — 자유롭게 활용

위 컴포넌트로 부족하면 **inline HTML + `style="..."`** 직접 작성 OK. 단, 색상/폰트는 브랜드 토큰(`#004FC5`, `#FF8C42`, Pretendard 등)을 따를 것. 빈번하게 재사용되는 패턴은 `template/styles.css`에 정식 컴포넌트로 승격.

예: 두 줄 강조 박스, 비대칭 layout, 특별한 코너 ribbon — 모두 inline 가능.

#### ⛔ ASCII 다이어그램 절대 금지

`<pre>`, monospace, `─│┌┐└┘├┤┬┴┼` 박스 문자, `→←↑↓` 화살표만 단독 등으로 **글자로 그림 그리는 모든 행위 금지**. 일반 채팅 응답이나 마크다운 문서에서 ASCII 박스/플로우/트리를 쓰는 습관을 슬라이드로 옮겨 오는 실수가 흔하다 (다른 AI agent가 이 스킬 호출할 때 특히).

| 의도 | ❌ ASCII | ✅ 정식 마크업 |
| --- | --- | --- |
| 프로세스/순서 | `[A] → [B] → [C]` | `<div class="flow">` + `.flow-step` |
| 구조/계층 | `┌─A─┐ ├─B─┤` | `.g2/.g3` + `.card` |
| 비교/대조 | `\| A \| B \|` (정렬한 텍스트) | `<table class="dt">` 또는 `.g2`+카드 |
| 라벨/뱃지 | `[Google]` `[Naver]` | `.svc-badge` 또는 `.pill` |
| 강조 박스 | `╔══╗ ║...║ ╚══╝` | inline HTML + `style="border:1px solid #004FC5"` |

이유: ASCII는 (1) Pretendard에서 정렬 깨짐 (2) auto-fit이 monospace 길이 못 맞춤 (3) 브랜드 일관성 무너짐 (4) PDF 캡처 후 픽셀화. inline HTML이라도 항상 div/span + style이지 `<pre>`로 그림 그리지 말 것.

### 그리드 클래스

| 클래스 | 컬럼 | 용도 |
| --- | --- | --- |
| `.g2`  | 1fr 1fr           | 좌우 비교 (2등분) |
| `.g2w` | 1.15fr 0.85fr     | 좌측 강조 (텍스트 + 차트) |
| `.g3`  | 1fr 1fr 1fr       | 카드 3개 |
| `.g4`  | 1fr 1fr 1fr 1fr   | 카드 4개 (밀도 높음) |

simple 모드는 `.g2`만 허용.

## Chart.js

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
```

```javascript
Chart.defaults.font.family = "'Pretendard Variable', 'Pretendard', sans-serif";
Chart.defaults.font.size = 14;          // 차트 슬라이드는 fit 대상 제외 → 절대값
Chart.defaults.plugins.legend.display = false;
Chart.defaults.animation.duration = 0;  // 필수 — PDF 캡처 시 빈 차트 방지

// 색상 팔레트
// Primary: #004FC5, Secondary: #4A90D9, Tertiary: #A0C4F1
// Accent: #FF8C42, Gray: #C8CDD5

// 수평 바 — 라벨 잘림 방지
options: {
  indexAxis: 'y',
  responsive: true,
  maintainAspectRatio: false,
  scales: { y: { ticks: { autoSkip: false } } }
}
```

차트 컨테이너에 명시적 height (예: `style="height: 360px"`) 필수 — `flex:1`은 print에서 무시됨.

## AI 이미지 (Gemini)

`GEMINI_API_KEY`가 환경변수 또는 `.env`에 있을 때:

```bash
pip3 install google-genai python-dotenv 2>/dev/null
python3 "${CLAUDE_SKILL_DIR}/../../gemini-image/skills/gemini-image/generate_images.py" \
  --prompt "프롬프트" --filename "slide-img.png" --outdir "/tmp" --ratio "16:9"
IMG_B64=$(base64 -i /tmp/slide-img.png)
```

**삽입**:
```html
<!-- 텍스트 + 이미지 (2열) -->
<div class="g2">
  <div>
    <ul class="bl">
      <li>핵심 포인트</li>
    </ul>
  </div>
  <div>
    <img class="slide-img" src="data:image/png;base64,{IMG_B64}" alt="...">
  </div>
</div>

<!-- 전면 이미지 (.body 대신 .slide 직속) -->
<div class="slide" id="s4">
  <div class="accent"></div>
  <img class="slide-img-full" src="data:image/png;base64,{IMG_B64}" alt="...">
  <div class="foot">...</div>
</div>
```

**프롬프트 팁**:
- ONDA 블루(#004FC5)를 포함하면 통일감
- "professional, clean, minimal, business presentation style"
- 한글 텍스트는 피하고 HTML로 오버레이
- `--ratio 16:9`

## 로고

기본은 ONDA 공식 로고:
```
https://cdn.prod.website-files.com/62fc3cdcd1a5bb1370c2d067/63c0a7b567846c336d75f050_onda.svg
```
- 커버: `<img class="onda-logo" src="위_URL" alt="ONDA">` (height: 28px 자동)
- Footer 텍스트: `© ONDA Inc.`

커스텀 로고 제공 시 base64로 인라인. GitHub private repo는:
```bash
gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | base64 -d
```

## 삽질 방지 체크리스트

| 항목 | 설명 |
| --- | --- |
| ⛔ ASCII 다이어그램 금지 | `<pre>`/monospace로 박스·화살표·트리 그리지 말 것. 정식 `.flow`/`.g2-4`/`.card`/`.dt`/`.svc-badge` 또는 inline HTML+style만 사용 |
| `<div class="slide active" id="s0">` | **첫 슬라이드만 active** — JS show(0)이 동기화하지만 페이지 로드 직후 깜빡임 방지 |
| 첫 슬라이드 = 커버 권장 | 다른 타입을 첫 슬라이드로 둘 때도 `class="slide active"` 필수 |
| 모든 콘텐츠 슬라이드에 `.foot` | copyright + 슬라이드 번호 |
| 모든 콘텐츠 슬라이드에 `.accent` | 상단 5px 블루 라인 |
| `.body`는 항상 콘텐츠 슬라이드에만 | 커버/섹션은 `.body` 없음 |
| 마지막 슬라이드 = `.closing-content` | "감사합니다" + 작성자 정보 (권장 — 누락 시 build.mjs 경고만) |
| 커버 `.cover-foot .products` 채움 | 자료 주제 관련 ONDA 제품 chip 2-4개 (예: `ONDA HUB`, `CRS`). 비워두면 footer 좌측이 휑함 |
| URL hash 동기화 | 페이지 이동 시 `#1`, `#2` … 로 자동 갱신 — 링크 공유 가능 |
| 양 끝 wrap-around 없음 | →/← 키와 클릭 모두 첫·마지막에서 멈춤 (hash 공유 안정성 우선, v2.0.0+) |
| 키보드 단축키 | `←/→` 페이지, `Home/End`, `F` 풀스크린 |
| 차트 컨테이너 height 명시 | `style="height: 360px"` |
| Chart.js `animation.duration: 0` | PDF 캡처 시 빈 차트 방지 |
| Chart.js `autoSkip: false` | 수평 바 라벨 자동 생략 방지 |
| simple 모드 콘텐츠 룰 | 불렛 3개, `.g2`만, 한 메시지/슬라이드, 1줄 25자 |
| en 모드 폰트 | `build.mjs`가 자동으로 Inter CDN link 추가 |
| wide 모드 PDF | `gen_pdf.mjs`가 자동 16:9 페이지 |

## Error handling

- puppeteer/pdf-lib 미설치 → `npm install puppeteer pdf-lib`
- 차트 빈 채로 캡처 → `animation.duration: 0` + 대기 시간 증가
- SVG 로고 렌더링 실패 → PNG로 변환
- GitHub private repo 접근 불가 → `gh auth status`
- Pretendard 미로드 → CDN URL 확인, `networkidle0` 대기

## 디자인 변경 요청 시

LLM이 슬라이드 마크업 외에 디자인 토큰 / 레이아웃 / fit 알고리즘을 바꿔야 할 때:

- 색상 / 폰트 / spacing → `template/styles.css`
- 키보드 / 풀스크린 / fit 알고리즘 → `template/runtime.js`
- HTML 골격 / placeholder → `template/base.html`
- 빌드 인자 / modifier 처리 → `build.mjs`

수정 후 반드시 모든 modifier 조합으로 빌드 + 화면 모드 + PDF 검증.
