---
name: git-bisect-auto
description: git bisect로 특정 코드가 추가/제거된 commit을 자동으로 찾기. file content 변경 시점, function 추가/제거, feature 도입 시점을 찾을 때 사용. binary search로 자동 검색하며 manual good/bad marking 불필요.
version: 1.0.0
---

# Git Bisect Auto
git bisect binary search로 특정 content가 추가/제거된 정확한 commit 자동 탐색

## 1. Execution Method

**CRITICAL**: Always run from the project root directory (where .git exists), NOT from the skill directory.

When this skill activates, you'll see:
```
Base directory for this skill: /path/to/.claude/skills/git-bisect-auto
```

Use this base directory to execute the script with python:
```bash
python <BASE_DIR>/scripts/bisect_auto.py --file <FILE> --pattern <PATTERN>
```

**Template for all commands**:
```bash
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py [OPTIONS]
```

Example:
```bash
# Run from your project root, NOT from skill directory
# Your current directory must be the git repository root
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py \
  --file client/pyproject.toml \
  --pattern 'version = "0.1.41"' \
  --good develop
```

## 2. 전제조건
- git repository에서 실행
- Python 3.6+
- git CLI (PATH에 존재)

## 3. 핵심 기능
bisect_auto.py 실행: --file FILE --pattern PATTERN

### 3-1. 사용 시점
- "When was function X added to file Y?"
- "Find when this code was introduced"
- "Which commit removed feature Z?"
- "When did file X change to include pattern Y?"
- Bug/feature 도입 시점 추적

### 3-2. 동작 방식 (Automated Binary Search)
1. `git bisect` 자동 시작
2. Good commit 자동 탐색 (pattern이 없는 commit)
3. Bisection point마다 file content 체크
4. Pattern 존재 여부로 good/bad 자동 marking
5. Culprit commit 식별
6. Repository를 original state로 복원

Manual intervention 불필요 - script가 모든 단계 자동 처리

## 4. 기본 사용법

**NOTE**: Replace `~/.claude/skills/git-bisect-auto` with the actual Base directory shown when skill activates.

### 4-1. 코드 추가 시점 찾기
```bash
# Function 추가 시점
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py \
  --file src/main.js --pattern "function calculateTotal()"

# Import 추가 시점
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py \
  --file app/models.py --pattern "from django.db import models"

# Configuration 추가 시점
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py \
  --file config.yaml --pattern "database:"
```

Output 예시:
```
🎯 FOUND THE CULPRIT COMMIT!
Commit: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
Short: a1b2c3d
Subject: Add database configuration
Date: 2025-01-15 14:30:00 +0900
```

### 4-2. 코드 제거 시점 찾기
`--removal` flag 사용
```bash
# Function 제거 시점
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py \
  --file src/utils.js --pattern "function oldHelper()" --removal

# Feature 삭제 시점
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py \
  --file README.md --pattern "Legacy API" --removal
```

### 4-3. 정규식 검색
`--regex` flag 사용
```bash
# Database configuration 추가 (regex)
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py \
  --file config.yaml --pattern "database:.*host" --regex

# Error handling 추가
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py \
  --file src/api.ts --pattern "try\s*\{.*catch" --regex

# Class 도입 시점
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py \
  --file app.py --pattern "class\s+User.*:" --regex
```

### 4-4. Good Commit 수동 지정
`--good` flag로 known good commit 제공하여 검색 속도 향상
```bash
# Known good commit부터 시작
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py \
  --file src/main.c --pattern "void newFunction()" --good abc123

# Tag 사용
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py \
  --file package.json --pattern "react-router" --good v1.0.0
```

## 5. 옵션

### 5-1. 전체 옵션
```bash
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py --help
# Required:
  --file FILE         검사할 file path
  --pattern PATTERN   검색할 string 또는 regex pattern
# Optional:
  --regex            pattern을 regex로 처리
  --good HASH        Good commit hash (미지정 시 자동 탐색)
  --max-search N     Good commit 검색 범위 (기본값: 100)
  --removal          Pattern REMOVAL 시점 찾기 (기본: 추가 시점)
```

### 5-2. 검색 범위 제어
최근 50개 commit만 검색:
```bash
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py \
  --file src/app.js --pattern "feature" --max-search 50
```

## 6. 예시

### 6-1. Bug 도입 시점 디버깅
```bash
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py \
  --file src/calculator.js --pattern "// FIXME: division by zero"
```

### 6-2. Feature 추가 추적
```bash
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py \
  --file src/auth.ts --pattern "passport.authenticate" --regex
```

### 6-3. Dependency 제거 추적
```bash
python ~/.claude/skills/git-bisect-auto/scripts/bisect_auto.py \
  --file package.json --pattern "jquery" --removal
```

## 7. Error Handling

### 7-1. Git repository 아님
`fatal: not a git repository`
해결: git repository에서 실행

### 7-2. Pattern이 존재하지 않음
`Cannot bisect - pattern doesn't exist in current commit!`
해결: Pattern 확인 및 HEAD에 존재하는지 검증. 제거된 content는 `--removal` 사용

### 7-3. Pattern이 항상 존재
`Could not find a suitable good commit!`
해결: `--good`으로 older commit 지정하거나 `--max-search` 증가

### 7-4. File이 존재하지 않음
`File doesn't exist in this commit`
해결: File rename/delete 확인. git log로 file history 추적

## 8. Script 동작 원리
scripts/bisect_auto.py가 자동으로:
1. 현재 branch/commit 저장
2. `git bisect` 시작
3. Good commit 자동 탐색 또는 사용자 지정 사용
4. Bisect loop:
   - File content에서 pattern 체크
   - Good/bad marking
   - 다음 bisection point로 자동 checkout
5. Culprit commit 식별
6. `git bisect reset` 실행
7. Original branch/commit으로 복원

안전성:
- 완료/에러 시 자동으로 `git bisect reset`
- Working directory 파일 수정 안 함
- Commit 생성 안 함
- Read-only 작업

## 9. References
[references/git-bisect-guide.md](~/llms/skills/git-bisect-auto/references/git-bisect-guide.md) - git bisect manual, advanced techniques, troubleshooting
