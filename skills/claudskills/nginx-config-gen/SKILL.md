---
name: nginx-config-gen
description: |
  트리거: "nginx 설정", "nginx config", "엔진엑스 설정", "리버스 프록시 설정", "ssl 설정"
  수행: Nginx 리버스 프록시·SSL(Let's Encrypt) 설정 생성. 다중 서비스 서브도메인 라우팅 지원
  출력: nginx.conf, 서비스별 server block 파일, docker-compose 통합 설정
---

# Nginx Config Generator

## 목적

리버스 프록시, SSL/TLS 종료, 서브도메인 라우팅, 성능 최적화가 포함된 Nginx 설정을 생성한다.
Let's Encrypt Certbot 연동과 보안 헤더까지 프로덕션 수준으로 완비한다.

## 실행 절차

1. **서비스 구성 파악**: 도메인, 서브도메인, 업스트림 서비스 포트 목록 확인
2. **SSL 전략 결정**: Let's Encrypt 자동 갱신 / 자체 서명 인증서 / 외부 인증서
3. **nginx.conf 생성**: worker, events, http 블록 전역 설정
4. **server block 생성**: 각 서비스별 서브도메인 라우팅 설정
5. **보안 헤더 추가**: HSTS, X-Frame-Options, CSP 등
6. **성능 최적화**: gzip, 캐싱, keepalive 설정
7. **Certbot 연동**: 인증서 발급/갱신 docker-compose 설정 포함

## 출력 형식

### 파일 구조
```
nginx/
  nginx.conf              ← 전역 설정
  conf.d/
    default.conf          ← HTTP → HTTPS 리다이렉트
    app.example.com.conf  ← 메인 앱
    api.example.com.conf  ← API 서버
    admin.example.com.conf← 어드민
  snippets/
    ssl-params.conf       ← SSL 파라미터 공통
    security-headers.conf ← 보안 헤더 공통
    proxy-params.conf     ← 프록시 헤더 공통
```

### nginx.conf 예시

```nginx
# nginx/nginx.conf
user nginx;
worker_processes auto;
worker_rlimit_nofile 65535;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # 로그 형식
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time uct=$upstream_connect_time';

    access_log /var/log/nginx/access.log main buffer=16k flush=5s;

    # 성능 최적화
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout 65;
    keepalive_requests 100;
    types_hash_max_size 4096;
    server_tokens off;  # Nginx 버전 숨김

    # Gzip 압축
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_min_length 1000;
    gzip_types
        text/plain text/css text/javascript application/javascript
        application/json application/xml image/svg+xml font/woff2;

    # 클라이언트 제한
    client_max_body_size 50M;
    client_body_timeout 60s;
    client_header_timeout 60s;

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=30r/m;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

    include /etc/nginx/conf.d/*.conf;
}
```

### 공통 스니펫

```nginx
# nginx/snippets/ssl-params.conf
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers off;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
ssl_session_timeout 1d;
ssl_session_cache shared:MozSSL:10m;
ssl_session_tickets off;
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 1.1.1.1 valid=300s;
resolver_timeout 5s;
```

```nginx
# nginx/snippets/security-headers.conf
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header Content-Security-Policy
    "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' https://fonts.gstatic.com;" always;
```

```nginx
# nginx/snippets/proxy-params.conf
proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_cache_bypass $http_upgrade;
proxy_read_timeout 90s;
proxy_connect_timeout 10s;
```

### 서비스 서버 블록 예시

```nginx
# nginx/conf.d/default.conf
# HTTP → HTTPS 리다이렉트
server {
    listen 80;
    listen [::]:80;
    server_name _;

    # Let's Encrypt 갱신 경로
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}
```

```nginx
# nginx/conf.d/app.example.com.conf
upstream nextjs_app {
    server app:3000;
    keepalive 32;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name example.com www.example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;
    include /etc/nginx/snippets/security-headers.conf;

    # 정적 자산 캐싱 (Next.js _next/static)
    location /_next/static/ {
        proxy_pass http://nextjs_app;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    # API 라우트 rate limiting
    location /api/auth/ {
        limit_req zone=login burst=10 nodelay;
        limit_req_status 429;
        proxy_pass http://nextjs_app;
        include /etc/nginx/snippets/proxy-params.conf;
    }

    location /api/ {
        limit_req zone=api burst=50 nodelay;
        proxy_pass http://nextjs_app;
        include /etc/nginx/snippets/proxy-params.conf;
    }

    location / {
        proxy_pass http://nextjs_app;
        include /etc/nginx/snippets/proxy-params.conf;
    }
}
```

```nginx
# nginx/conf.d/api.example.com.conf
upstream fastapi_backend {
    server backend:8000;
    keepalive 16;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name api.example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;
    include /etc/nginx/snippets/security-headers.conf;

    # CORS 헤더 (OPTIONS preflight)
    location / {
        if ($request_method = OPTIONS) {
            add_header Access-Control-Allow-Origin "https://example.com";
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
            add_header Access-Control-Allow-Headers "Authorization, Content-Type";
            add_header Access-Control-Max-Age 86400;
            return 204;
        }

        limit_req zone=api burst=100 nodelay;
        proxy_pass http://fastapi_backend;
        include /etc/nginx/snippets/proxy-params.conf;
    }
}
```

### Certbot 갱신 docker-compose 스니펫

```yaml
# docker-compose.yml에 추가
  certbot:
    image: certbot/certbot:latest
    volumes:
      - ./certbot/www:/var/www/certbot:rw
      - ./certbot/conf:/etc/letsencrypt:rw
    entrypoint: /bin/sh -c "trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done"
```

```bash
# 최초 인증서 발급
docker compose run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email admin@example.com \
  --agree-tos \
  --no-eff-email \
  -d example.com -d www.example.com -d api.example.com
```

## 사용 예시

**입력:**
> "nginx 설정 만들어줘. example.com은 Next.js 앱, api.example.com은 FastAPI, admin.example.com은 어드민 패널. SSL Let's Encrypt."

**출력:**
- `nginx/nginx.conf` + 공통 스니펫 3개
- `conf.d/` 서버 블록 4개 (default + 3 서비스)
- Certbot 발급 명령어 안내

## 주의사항

- `server_tokens off`로 Nginx 버전 정보 노출 금지
- Rate Limiting은 `/api/auth/` 경로에 별도 zone 적용 (무차별 대입 공격 방지)
- `ssl_session_tickets off` — 세션 티켓 재사용 공격 방지
- WebSocket 프록시 시 `Upgrade`, `Connection` 헤더 반드시 전달
- `add_header`는 `always` 파라미터로 오류 응답에도 헤더 포함
- Let's Encrypt 갱신 전 HTTP 80 포트의 `/.well-known/acme-challenge/` 경로 유지 필수
