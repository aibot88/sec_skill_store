---
name: changelog-gen
description: |
  트리거: "changelog", "변경 이력", "릴리즈 노트", "release notes", "CHANGELOG 만들어줘"
  git log 또는 PR/커밋 목록을 분석하여 Keep a Changelog 형식의 CHANGELOG.md를 생성한다.
  버전별 Added/Changed/Deprecated/Removed/Fixed/Security 섹션으로 구조화한다.
  출력: CHANGELOG.md 형식 마크다운 + 버전 범프 권고
---
# Changelog Generator — 변경 이력 자동 생성

## 목적
커밋 메시지, PR 제목, 또는 변경 내용을 분석하여
[Keep a Changelog](https://keepachangelog.com) 형식의 CHANGELOG.md를 생성한다.

## 실행 절차

### 1단계: 변경 내용 수집
```bash
# 마지막 태그 이후 커밋 목록
git log $(git describe --tags --abbrev=0)..HEAD --oneline --no-merges

# 또는 두 태그 사이
git log v1.2.0..v1.3.0 --oneline --no-merges

# PR 머지 포함
git log --merges --pretty=format:"%s" v1.2.0..HEAD
```

### 2단계: 커밋 분류
Conventional Commits 규칙 기반으로 분류:
| 커밋 타입 | Changelog 섹션 |
|-----------|----------------|
| `feat` | Added |
| `perf`, `refactor` | Changed |
| `deprecate` | Deprecated |
| `remove` | Removed |
| `fix` | Fixed |
| `security` | Security |
| `docs`, `test`, `chore` | (내부 변경, 생략 가능) |

### 3단계: 버전 결정 (Semantic Versioning)
- **MAJOR** (x.0.0): Breaking change (`feat!`, `fix!`, `BREAKING CHANGE`)
- **MINOR** (0.x.0): 새 기능 (`feat`)
- **PATCH** (0.0.x): 버그 수정 (`fix`, `security`)

### 4단계: 항목 작성 기준
- 사용자 관점에서 서술 (개발자 내부 용어 최소화)
- 링크: PR 번호 또는 이슈 번호 연결
- 간결하게: 한 줄로 변경 내용 표현

### 5단계: 기존 CHANGELOG.md 병합
- 파일이 이미 있으면 새 버전을 최상단에 추가
- `[Unreleased]` 섹션 패턴을 사용하면 해당 섹션에 누적

## 출력 형식

```
## CHANGELOG.md

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2026-04-01

### Added
- 사용자 프로필 이미지 업로드 기능 (#142)
- 다국어 지원 추가 (영어, 일본어) (#138)
- API 요청 레이트 리밋 헤더 노출 (#135)

### Changed
- 주문 조회 API 응답 속도 40% 개선 (Redis 캐시 적용) (#140)
- 에러 응답 형식 RFC 7807 표준으로 통일 (#133)

### Fixed
- 로그인 만료 후 토큰 갱신 무한 루프 버그 수정 (#144)
- Safari에서 날짜 피커가 표시되지 않는 문제 해결 (#141)

### Security
- JWT 서명 알고리즘 HS256 → RS256 으로 변경 (#139)

## [1.2.1] - 2026-03-15

### Fixed
- 결제 금액 소수점 계산 오류 수정 (#128)

## [1.2.0] - 2026-03-01
...

[Unreleased]: https://github.com/org/repo/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/org/repo/compare/v1.2.1...v1.3.0
[1.2.1]: https://github.com/org/repo/compare/v1.2.0...v1.2.1
```

---

### 버전 범프 권고
- 현재: `v1.2.1`
- 권고: `v1.3.0` (새 기능 2개 포함 → MINOR 버전 업)
- Breaking change: 없음
```

## 사용 예시

**입력:**
```
changelog 만들어줘
feat: 이미지 업로드 추가
fix: 토큰 갱신 버그 수정
security: JWT 알고리즘 변경
```

**출력 예시 (축약):**
```
## [1.3.0] - 2026-04-01

### Added
- 이미지 업로드 기능

### Fixed
- 토큰 갱신 버그 수정

### Security
- JWT 알고리즘 RS256으로 교체

버전 권고: 1.2.0 → 1.3.0 (새 기능 포함, MINOR 범프)
```

## 주의사항
- `chore`, `docs`, `test` 커밋은 기본적으로 생략한다 (사용자 요청 시 포함).
- 커밋 메시지가 Conventional Commits 형식이 아닌 경우 내용 기반으로 유추한다.
- 버전은 권고만 하며 실제 태깅은 사용자가 결정한다.
- 민감한 변경(security fix)은 CVE 번호나 취약점 상세를 포함하지 않는 것이 원칙이다.
