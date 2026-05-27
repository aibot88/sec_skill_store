---
name: nuclei-scan
description: 살아있는 호스트에 nuclei로 알려진 취약점 패턴을 스캔한다. exposure, misconfig, token, secret 태그 위주. BBP 가용성 침해 방지를 위해 rate limit 필수.
---

# Nuclei 스캔

## 개요
살아있는 호스트에 대해 nuclei 템플릿으로 알려진 패턴을 스캔한다.
BBP에서는 가용성 침해가 금지되므로 rate limit을 반드시 설정한다.

## 입력
- `LIVE_HOSTS`: live_hosts.txt 경로
- `OUT`: 출력 디렉토리

## 템플릿 업데이트
```bash
nuclei -update-templates
```

## Phase 1 — 정보 노출 스캔 (안전)
```bash
nuclei -l $LIVE_HOSTS \
  -tags "exposure,config,misconfig,token,secret,info" \
  -severity "critical,high,medium,low" \
  -rate-limit 10 \
  -timeout 10 \
  -o $OUT/nuclei_exposure.txt \
  -silent
```

## Phase 2 — 기술스택 탐지
```bash
nuclei -l $LIVE_HOSTS \
  -tags "tech" \
  -rate-limit 20 \
  -o $OUT/nuclei_tech.txt \
  -silent
```

## Phase 3 — 서브도메인 탈취 탐지
```bash
nuclei -l $LIVE_HOSTS \
  -tags "takeover,cname,dns" \
  -severity "critical,high" \
  -rate-limit 10 \
  -o $OUT/nuclei_takeover.txt \
  -silent
```

## Phase 4 — CVE 스캔 (선택적)
```bash
# 최근 1년 CVE만, rate limit 강하게
nuclei -l $LIVE_HOSTS \
  -tags "cve" \
  -severity "critical,high" \
  -rate-limit 5 \
  -o $OUT/nuclei_cve.txt \
  -silent
```

## 출력 파일
- `nuclei_exposure.txt` — 정보 노출
- `nuclei_tech.txt` — 기술스택
- `nuclei_takeover.txt` — 서브도메인 탈취 후보
- `nuclei_cve.txt` — CVE 패턴 매칭

## BBP 준수 사항
- `-rate-limit 10` 이하로 유지
- `-severity critical,high` 위주
- DoS 유발 템플릿 제외: `-exclude-tags dos,fuzz`
- active scan 태그 제외: `-exclude-tags intrusive`
