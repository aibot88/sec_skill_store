---
name: classroom-setup
description: Google Classroom 연동 초기 설정. 패키지 설치, OAuth 인증을 자동으로 처리합니다.
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
user-invocable: true
---

# Google Classroom 초기 설정

사용자는 OAuth JSON 파일 경로만 알려주면 됩니다. 나머지는 자동으로 처리합니다.

## 경로 규칙

- **CLI 스크립트**: 이 SKILL.md 기준 `../../classroom/classroom.py` (플러그인 루트 기준)
- **인증 데이터**: `~/.config/dgsw-classroom/` (credentials.json, token.pickle)

실행 시 base directory 정보를 이용하여 CLI 경로를 구성합니다:
```
PLUGIN_ROOT = "<Base directory>/../../"
CLI = "<PLUGIN_ROOT>/classroom/classroom.py"
```

## 실행 순서

### 1. Python 패키지 자동 설치

```bash
python3 -c "from googleapiclient.discovery import build" 2>/dev/null || pip3 install google-api-python-client google-auth-oauthlib google-auth-httplib2
```

### 2. credentials.json 확인

```bash
ls ~/.config/dgsw-classroom/credentials.json 2>&1
```

파일이 있으면 → **3단계로 건너뛰기**

파일이 없으면 → AskUserQuestion으로 OAuth JSON 파일 경로를 받습니다:

```
Google Classroom API OAuth 인증 파일이 필요합니다.

GCP Console에서 OAuth 클라이언트 ID(데스크톱 앱)를 만들고
다운로드한 JSON 파일의 경로를 알려주세요.

아직 만들지 않았다면:
1. https://console.cloud.google.com 접속 (학교 계정)
2. 프로젝트 생성 → Classroom API 활성화
3. OAuth 동의 화면 설정 (내부)
4. 사용자 인증 정보 > OAuth 클라이언트 ID > 데스크톱 앱 > JSON 다운로드
```

경로를 받으면 자동 복사:
```bash
mkdir -p ~/.config/dgsw-classroom
cp "<사용자가 입력한 경로>" ~/.config/dgsw-classroom/credentials.json
```

### 3. 인증 실행

Base directory에서 CLI 경로를 구성하여 실행:
```bash
python3 "<PLUGIN_ROOT>/classroom/classroom.py" auth
```

브라우저가 열리면 학교 계정으로 로그인하라고 안내합니다.

### 4. 인증 확인

```bash
python3 "<PLUGIN_ROOT>/classroom/classroom.py" courses
```

수업 목록이 나오면 성공.

### 5. 완료 메시지

```
Google Classroom 연동 완료!

사용법:
- "과제 확인해줘" → 수업별 과제 목록
- "과제 제출해줘" → 과제 제출
- /dgsw-classroom:classroom → 과제 관리 스킬
```

## 오류 대응

### 403 Forbidden
학교 IT 관리자가 API 접근을 차단한 경우. 관리자에게 Google Classroom API 허용 요청 필요.

### credentials.json 형식 오류
OAuth 클라이언트 ID가 "데스크톱 앱" 유형인지 확인.
