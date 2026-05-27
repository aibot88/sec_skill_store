---
name: nginx-reverse-proxy
description: Nginx reverse proxy patterns for path-based routing, lazy DNS resolution, WebSocket/SSE proxying, OAuth2 auth_request, subpath stripping, and multi-server-block configuration for self-hosted infrastructure behind Cloudflare Tunnel.
allowed-tools: Read, Write, Bash, Edit
category: infrastructure
tags: [nginx, reverse-proxy, websocket, sse, oauth2, load-balancing]
version: 1.0.0
---

# Nginx Reverse Proxy — SOL Server

## Overview

Nginx is the single entry point for all services on the SOL server. It routes ~20 services
through 6 server blocks, differentiating them by path on a single hostname (`sol.massimilianopili.com`).

Internal traffic (Tailscale `100.86.46.84`) and public traffic (Cloudflare Tunnel) are served
by separate server blocks with parallel routes.

Config file: `/data/massimiliano/proxy/nginx.conf`
Docker Compose: `/data/massimiliano/proxy/docker-compose.yml`

## When to Use

- Aggiungere un nuovo servizio dietro nginx
- Debuggare errori 502/404 nel proxy
- Configurare proxying WebSocket o SSE
- Impostare OAuth2 Proxy auth_request per un servizio
- Capire il pattern lazy DNS e perche' e' necessario
- Aggiungere visitor blocking su una route
- Configurare log separati per traffico pubblico

## Server Blocks Architecture

Nginx gestisce 6 server block su porte separate:

| Porta | Scopo | Route principali |
|-------|-------|-----------------|
| `:80` | Tailscale: tutti i servizi | `= /` (dashboard), `/git/`, `/files/`, `/auth/`, `/claude/`, `/api/`, `/server/`, `/mongo/`, `/libsql/`, `/ide/`, `/mq/`, `/kp/`, `/stats/` |
| `:8443` | Tailscale: Keycloak admin | `/auth/` con header porta dedicati |
| `:8081` | Tailscale: pgAdmin + OAuth2 | `/pgadmin/`, `/oauth2/` |
| `:8082` | Tailscale: Portainer + OAuth2 | `/portainer/`, `/oauth2/` con WebSocket |
| `:8090` | Tailscale: Claude Proxy + PKCE | `/v1/`, `/health`, `/auth/realms/` |
| `:8888` | Pubblico (Cloudflare Tunnel) | Tutte le path sopra unificate (escluso libSQL e Artemis console) |

Il traffico pubblico arriva da Cloudflare Tunnel che punta a `nginx:8888`.
Il traffico Tailscale arriva direttamente sulle porte dedicate.

## Key Pattern 1: Lazy DNS Resolution

**CRITICO**: senza questo pattern, nginx crasha allo startup se un qualsiasi container e' spento.

```nginx
http {
    resolver 127.0.0.11 valid=10s;  # Docker embedded DNS, TTL 10s

    location /git/ {
        set $gitea_upstream http://gitea:3000;  # variabile = risoluzione a runtime
        rewrite ^/git/(.*) /$1 break;
        proxy_pass $gitea_upstream;
    }
}
```

Con `proxy_pass http://gitea:3000` (letterale), nginx risolve il DNS allo startup e fallisce
se il container e' spento. Con `set $var`, la risoluzione avviene a runtime: un container
spento causa 502 solo sulla sua route. Dopo un restart di container, nginx aggiorna l'IP
entro 10 secondi (TTL). Se serve subito, ricreare nginx.

**Eccezione**: `host.docker.internal` (claude-proxy, dashboard-api) usa `proxy_pass` diretto
perche' non sono container Docker e non beneficiano del resolver Docker.

## Key Pattern 2: Subpath Prefix Stripping (Pattern A vs Pattern B)

### Pattern A — Strip del prefisso

Il servizio NON gestisce il subpath. `rewrite` rimuove il prefisso prima di inoltrare.

```nginx
location /git/ {
    set $gitea_upstream http://gitea:3000;
    rewrite ^/git/(.*) /$1 break;    # Gitea riceve /user/login, non /git/user/login
    proxy_pass $gitea_upstream;
    # ... standard headers
}
```

Servizi Pattern A: Gitea, File Manager, Claude Proxy, Server API, Dashboard API,
libSQL, code-server, KP Manager

### Pattern B — Prefisso mantenuto

Il servizio gestisce il subpath internamente (SCRIPT_NAME, --base-url, o config propria).

```nginx
location /pgadmin/ {
    set $pgadmin_upstream http://pgadmin:5050;
    proxy_pass $pgadmin_upstream;    # URI passato intero (/pgadmin/...)
}
```

Servizi Pattern B: pgAdmin (`SCRIPT_NAME=/pgadmin`), Portainer (`--base-url /portainer`),
mongo-express (`ME_CONFIG_SITE_BASEURL=/mongo/`), Keycloak (`KC_HTTP_RELATIVE_PATH=/auth`)

**Caso speciale Artemis**: passa `$request_uri` esplicito (`proxy_pass $mq_upstream$request_uri`)

**NOTA**: con `proxy_pass $var` (variabile), nginx NON fa lo strip automatico del prefisso
come con il letterale + trailing slash. Bisogna usare `rewrite ... break` esplicitamente.

## Key Pattern 3: OAuth2 Proxy auth_request

Tre pattern di autenticazione usati nel server:

| Pattern | Meccanismo | Servizi |
|---------|-----------|---------|
| OIDC nativo | Il servizio gestisce auth OIDC direttamente | Gitea, File Manager |
| OAuth2 Proxy auth_request | nginx delega l'auth a OAuth2 Proxy | pgAdmin, Portainer, mongo-express, libSQL, code-server, Artemis, KP Manager |
| JWT Bearer | Il servizio valida il JWT autonomamente | Claude Proxy, Server API, Dashboard API |

### auth_request base

```nginx
location /mongo/ {
    auth_request /oauth2/auth;
    error_page 401 =302 /oauth2/start?rd=$request_uri;

    auth_request_set $user $upstream_http_x_auth_request_user;
    auth_request_set $email $upstream_http_x_auth_request_email;
    proxy_set_header X-Forwarded-User $user;
    proxy_set_header X-Forwarded-Email $email;

    set $mongo_upstream http://mongo-express:8081;
    proxy_pass $mongo_upstream;
    # ... standard headers
}
```

### Due istanze OAuth2 Proxy

- **Tailscale** (`oauth2-proxy:4180`): usata su `:80`, `:8081`, `:8082`
- **Pubblica** (`oauth2-proxy-public:4181`): usata su `:8888`

Ogni server block deve puntare all'istanza corretta. Entrambe richiedono buffer grandi
per i token Keycloak: `proxy_buffer_size 128k; proxy_buffers 4 256k; proxy_busy_buffers_size 256k;`

### Visitor blocking a livello nginx

Per servizi che contengono dati sensibili (password, credenziali):

```nginx
location /kp/ {
    auth_request /oauth2/auth;
    error_page 401 =302 /oauth2/start?rd=$request_uri;

    auth_request_set $auth_user $upstream_http_x_auth_request_preferred_username;

    if ($auth_user = "visitor") {
        return 403;
    }

    set $kp_upstream http://kp-manager:8095;
    rewrite ^/kp/(.*) /$1 break;
    proxy_pass $kp_upstream;
    # ...
}
```

### Portainer redirect speciale (cross-port)

Il callback OAuth2 di Portainer va a `:8081` (stessa porta di pgAdmin), ma la route e' su `:8082`.
Serve un URL assoluto nel redirect:

```nginx
# :8082 — Portainer
error_page 401 =302 /oauth2/start?rd=http://100.86.46.84:8082$request_uri;
```

## Key Pattern 4: WebSocket Proxying

Necessario per servizi con connessioni WebSocket persistenti.

```nginx
location /api/ {
    proxy_pass http://host.docker.internal:7681/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_read_timeout 3600s;    # 1 ora per WS long-lived
    proxy_send_timeout 3600s;
}
```

**Timeout per servizio**:
- Dashboard API (terminal): `3600s` (1 ora)
- Portainer: default (60s, WS usato per aggiornamenti brevi)
- code-server: `86400s` (24 ore, sessioni IDE lunghe)
- GoAccess stats: default (60s, SSE real-time)

**Servizi con WebSocket**: Dashboard API, Portainer, code-server, GoAccess stats

## Key Pattern 5: SSE Streaming

Per API che usano Server-Sent Events (streaming risposte AI):

```nginx
location /claude/ {
    proxy_pass http://host.docker.internal:8091/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    # SSE: disabilitare buffering e cache
    proxy_buffering off;
    proxy_cache off;
    proxy_read_timeout 300s;       # 5 min per singola risposta AI
    chunked_transfer_encoding on;
}
```

**CRITICO**: `proxy_buffering off` e' essenziale per SSE. Senza, nginx accumula la risposta
prima di inviarla al client, causando timeout o risposte incomplete.

## Key Pattern 6: Dashboard vs Gitea (Exact Match Priority)

```nginx
# Exact match (priorita' alta): serve la dashboard HTML
location = / {
    root /usr/share/nginx/home;
    rewrite ^ /index.html break;
    default_type text/html;
}

# Prefix match (priorita' bassa): redirige tutto il resto a Gitea
location / {
    return 302 /git$request_uri;
}
```

In nginx, `location = /` (exact match) ha sempre la precedenza su `location /` (prefix match).
Questo permette di servire la dashboard su `/` e redirigere tutto il resto a Gitea.

**WARNING**: NON usare `alias` con `location = /` + direttiva `index`. Bug noto di nginx:
concatena il path dell'alias con "index.html" senza separatore. Usare `root` + `rewrite` come sopra.

## Key Pattern 7: Keycloak Proxy Headers

```nginx
server {
    listen 8443;
    location /auth/ {
        set $keycloak_admin_upstream http://keycloak:8080;
        proxy_pass $keycloak_admin_upstream;
        proxy_set_header Host $http_host;          # $http_host preserva la porta!
        proxy_set_header X-Forwarded-Host $http_host;
        proxy_set_header X-Forwarded-Port 8443;
        proxy_buffer_size 128k;
        proxy_buffers 4 256k;
        proxy_busy_buffers_size 256k;
    }
}
```

**WARNING**: NON usare `proxy_redirect` nei block Keycloak — riscrive TUTTI i Location header
(inclusi callback OAuth2), rompendo il flusso SSO. `KC_HOSTNAME` gestisce gia' i redirect.

`$host` non include la porta, `$http_host` la include. Per porte non-standard serve `$http_host`.

## Key Pattern 8: Multi-User Routing (code-server)

```nginx
map $ide_auth_user $ide_backend {
    "sol_root"   code-server-massimiliano:8080;
    default      "";
}

location /ide/ {
    auth_request /oauth2/auth;
    auth_request_set $ide_auth_user $upstream_http_x_auth_request_preferred_username;

    rewrite ^/ide/(.*) /$1 break;
    proxy_pass http://$ide_backend;    # routing dinamico per utente

    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 86400s;
}
```

`auth_request_set` cattura lo username, la `map` seleziona il container backend corretto.

## Key Pattern 9: Cloudflare Real IP

```nginx
http {
    # Recupera l'IP reale del visitatore dal header Cloudflare
    real_ip_header    CF-Connecting-IP;
    real_ip_recursive on;
    set_real_ip_from  0.0.0.0/0;    # accetta da qualsiasi IP (tunnel locale)
}
```

Senza questo, tutti i log mostrerebbero l'IP del container cloudflared.

## Key Pattern 10: Custom Log Format and Separate Logs

```nginx
log_format main '$remote_addr [$time_local] "$request" $status $body_bytes_sent '
                '"$http_referer" "$http_user_agent" '
                'rt=$request_time ust=$upstream_response_time';

access_log /var/log/nginx/access.log main;     # globale
access_log /var/log/nginx/public.log main;     # server :8888 (log separato)
```

Campi `rt=` e `ust=` utili per diagnosticare latenza. Compatibile con GoAccess.

## Key Pattern 11: Public vs Tailscale (X-Forwarded-Proto)

Sul server block pubblico (:8888), `X-Forwarded-Proto` deve essere `https` esplicito
(HTTPS terminato da Cloudflare). Su Tailscale usare `$scheme` (http).
Senza questo, i callback OAuth2 vengono generati con `http://` invece di `https://`.

## Adding a New Service (Checklist)

1. **Docker Compose**: creare `docker-compose.yml` con `networks: shared: external: true`
2. **Scegliere auth pattern**: OIDC nativo / OAuth2 Proxy auth_request / JWT Bearer / Nessuna
3. **Scegliere subpath pattern**: Pattern A (strip con `rewrite`) o Pattern B (mantieni)
4. **Aggiungere location block** al server block Tailscale (`:80`)
5. **Aggiungere location block** al server block pubblico (`:8888`) se il servizio deve essere esposto
6. **Se OAuth2 Proxy**: aggiungere il location `/oauth2/` se non presente, e usare l'istanza corretta
7. **Se WebSocket**: aggiungere `proxy_http_version 1.1` + header Upgrade/Connection + timeout adeguato
8. **Se SSE**: aggiungere `proxy_buffering off` + `proxy_cache off`
9. **Testare lazy DNS**: spegnere il container, verificare che nginx parta e solo quella route dia 502
10. **Restart nginx**: `cd /data/massimiliano/proxy && docker compose up -d nginx --force-recreate`

### Template: nuovo servizio con OAuth2 Proxy (Pattern A)

```nginx
# Nel server block :80 (Tailscale)
location /newservice/ {
    auth_request /oauth2/auth;
    error_page 401 =302 /oauth2/start?rd=$request_uri;

    auth_request_set $user $upstream_http_x_auth_request_user;
    auth_request_set $email $upstream_http_x_auth_request_email;
    proxy_set_header X-Forwarded-User $user;
    proxy_set_header X-Forwarded-Email $email;

    set $newservice_upstream http://newservice-container:PORT;
    rewrite ^/newservice/(.*) /$1 break;
    proxy_pass $newservice_upstream;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# Nel server block :8888 (Pubblico) — stessa cosa ma con:
# - $oauth2pub_upstream (porta 4181, non 4180)
# - X-Forwarded-Proto https (non $scheme)
```

## Best Practices

1. **Sempre lazy DNS** (`set $var` + `proxy_pass $var`) per i container Docker
2. **Buffer grandi** (`proxy_buffer_size 128k`) per le route Keycloak (header con token grandi)
3. **Timeout WebSocket**: minimo `3600s` per connessioni WebSocket persistenti
4. **SSE**: sempre `proxy_buffering off` per endpoint di streaming
5. **Mai `nginx -s reload`** con config bind-mounted (problema inode) — sempre `--force-recreate`
6. **`$http_host`** (non `$host`) quando la porta deve essere preservata negli header
7. **`X-Forwarded-Proto https`** esplicito sul server block pubblico (:8888)
8. **`client_max_body_size 0`** per servizi con upload illimitato (File Manager)
9. **`client_max_body_size 512m`** per Gitea (upload repo LFS/release)
10. **GoAccess Origin**: normalizzare `Origin` header per GoAccess WebSocket (`proxy_set_header Origin`)

## Troubleshooting

| Sintomo | Causa probabile | Fix |
|---------|----------------|-----|
| **502 Bad Gateway** | Container spento o nginx ha cachato DNS stale | Verificare container attivo, attendere 10s o `--force-recreate` nginx |
| **404 Not Found** | Manca `rewrite` per servizio Pattern A | Aggiungere `rewrite ^/path/(.*) /$1 break;` prima di `proxy_pass` |
| **500 sulla home** | Bug `alias` + `index` | Usare `root` + `rewrite ^ /index.html break;` |
| **OAuth2 loop infinito** | Manca location `/oauth2/` nello stesso server block | Aggiungere il block OAuth2 Proxy sulla stessa porta |
| **WebSocket fallisce** | Mancano header Upgrade/Connection | Aggiungere `proxy_http_version 1.1` + `Upgrade` + `Connection "upgrade"` |
| **SSE non arriva in streaming** | `proxy_buffering` attivo (default) | Aggiungere `proxy_buffering off; proxy_cache off;` |
| **Keycloak redirect rotto** | `proxy_redirect` nel block Keycloak | Rimuovere `proxy_redirect`, KC_HOSTNAME gestisce i redirect |
| **IP sbagliato nei log** | Manca `real_ip_header CF-Connecting-IP` | Verificare che sia a livello `http {}` |
| **OAuth2 error 500** | Buffer troppo piccoli per token | Aggiungere `proxy_buffer_size 128k` nel block `/oauth2/` |
| **Porta persa negli header** | `$host` al posto di `$http_host` | Usare `$http_host` per preservare la porta |

### Comandi diagnostici

```bash
# Verificare container sulla rete shared
docker network inspect shared --format '{{range .Containers}}{{.Name}} {{end}}'

# Restart nginx (unico metodo sicuro con bind mount)
cd /data/massimiliano/proxy && docker compose up -d nginx --force-recreate

# Testare configurazione nginx (sintassi)
docker exec nginx nginx -t

# Log nginx in tempo reale
docker logs nginx -f --tail 50

# Verificare che la risoluzione DNS funzioni
docker exec nginx nslookup gitea 127.0.0.11
```
