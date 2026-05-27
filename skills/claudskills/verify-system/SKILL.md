---
name: verify-system
description: "End-to-end system health verification. Checks all containers, ports, endpoints, and pipelines (logging, email, auth, socket, worker). Proves the system is truly working, not just running."
argument-hint: ""
---

# /verify-system Skill

## Purpose

Proves that the entire system is **truly working** — not just "containers are up" but every pipeline, every connection, every integration is functional. Run after `/create-new-project` or anytime you need confidence that the system is healthy.

**Philosophy:** Don't say "it's ready" — prove it with evidence.

## Verification Levels

### Level 0: Configuration Sanity

Static checks against `docker-compose.yml` — catch blueprint drift before paying the cost of `docker compose up`. These verify that what infra-agent generated matches what `infra-agent/children/` documents.

#### 0.1 Health-gated dependencies

Every service that talks to a stateful infrastructure dependency (PostgreSQL, RabbitMQ, Redis, Elasticsearch) must wait on `service_healthy`, not `service_started`. `service_started` only proves the container's PID 1 exists — the broker/db may still be in its bootstrap loop, causing first-run connection errors that "auto-recover" but pollute logs and confuse new contributors.

```bash
# Find any depends_on blocks that target stateful services with service_started
grep -nE "(rabbitmq|postgres|db|redis|elasticsearch):\s*$" -A1 docker-compose.yml \
  | grep -B1 "condition: service_started"
```

**Pass:** No matches — every stateful dep uses `service_healthy`.
**Fail diagnostic:** Print the offending service+dependency pairs and recommend flipping to `service_healthy`. See [infra-agent/children/health-checks.md](../../agents/infra-agent/children/health-checks.md) for the canonical pattern.

#### 0.2 Shared .NET project shadow volumes

When the API/Worker/Socket/LogIngest services mount source from host, every referenced .NET project (`Domain`, `Application`, `Infrastructure`, `Logging`, plus any other `.csproj` referenced by a service) needs its `bin/` and `obj/` shadowed by named volumes. Otherwise host-side `dotnet build` (run by a developer on macOS) collides with container-side Linux artefacts and produces mysterious assembly-load failures.

```bash
# For each shared project under src/, both bin and obj volumes must exist
for proj in Domain Application Infrastructure Logging; do
  base=$(echo "$proj" | tr '[:upper:]' '[:lower:]')   # domain, application, infrastructure, logging
  short=${base%ation}                                  # application → applic; tweak as needed per project
  grep -qE "^\s*${base}_bin:|^\s*${short}_bin:" docker-compose.yml || echo "MISSING: ${base}_bin"
  grep -qE "^\s*${base}_obj:|^\s*${short}_obj:" docker-compose.yml || echo "MISSING: ${base}_obj"
done
```

(Exact short-name convention follows [infra-agent/children/volume-strategy.md](../../agents/infra-agent/children/volume-strategy.md): `domain_bin`, `app_bin`, `infra_bin`, `logging_bin` and their `_obj` siblings. Any project referenced by a `.csproj` ProjectReference inside a service must appear in that service's `volumes:` block AND in the top-level `volumes:` declaration.)

**Pass:** Every shared project has a `_bin` and `_obj` named volume, declared at the top level AND mounted into every service whose csproj references it.
**Fail diagnostic:** List the missing volumes and the affected services. See [infra-agent/children/volume-strategy.md](../../agents/infra-agent/children/volume-strategy.md) — "Type 1: Shadow Volumes".

**Report format:**
```
Level 0 — Configuration:
  ✅ Health-gated deps      All stateful depends_on use service_healthy
  ✅ Shadow volumes         domain/app/infra/logging bin+obj all declared and mounted
  Result: ✅ PASS (2/2 checks)
```

If Level 0 fails, **stop and fix the compose file** before running Level 1+ — runtime checks against a structurally drifted compose file produce noisy false-positives.

### Level 1: Containers Running

Check every container is up and healthy (not just "created" or "restarting"):

```bash
docker compose ps --format "table {{.Name}}\t{{.Status}}"
```

**Pass criteria:**
- All containers show "Up" status
- Health-checked services show "(healthy)"
- No container in "Restarting" or "Exited" state (except init containers like minio-init which are expected to exit)

**Report format:**
```
Level 1 — Containers:
  ✅ wfm-api          Up 2 minutes
  ✅ wfm-db           Up 2 minutes (healthy)
  ✅ wfm-rabbitmq     Up 2 minutes (healthy)
  ✅ wfm-redis        Up 2 minutes (healthy)
  ✅ wfm-elasticsearch Up 2 minutes (healthy)
  ⚪ wfm-minio-init   Exited (expected — one-shot init)
  ... (all containers)
  Result: ✅ PASS (14/14 running)
```

### Level 2: Ports Accessible

For every service with an exposed port, verify TCP connectivity:

```bash
curl -sf -o /dev/null -w "%{http_code}" http://localhost:{port}/
```

**Services to check:**

| Service | Port | Check Method |
|---------|------|-------------|
| API | {api_port} | HTTP GET /api/health/ping |
| Swagger | {api_port} | HTTP GET /swagger/index.html |
| Socket | {socket_port} | HTTP GET (SignalR negotiate) |
| PostgreSQL | {db_port} | docker compose exec db pg_isready |
| RabbitMQ Management | {rmq_mgmt_port} | HTTP GET / |
| Redis | {redis_port} | docker compose exec redis redis-cli ping |
| Elasticsearch | {es_port} | HTTP GET /_cluster/health |
| Kibana | {kibana_port} | HTTP GET /api/status |
| Mailpit | {mailpit_port} | HTTP GET / |
| MinIO Console | {minio_console_port} | HTTP GET / |
| Adminer | {adminer_port} | HTTP GET / |
| Redis Commander | {redis_ui_port} | HTTP GET / |

**Report format:**
```
Level 2 — Ports:
  ✅ API (13000)           HTTP 200
  ✅ Swagger (13000)       HTTP 200
  ✅ PostgreSQL (15432)    pg_isready OK
  ✅ RabbitMQ (25673)      HTTP 200
  ✅ Redis (16379)         PONG
  ✅ Elasticsearch (19200) green
  ✅ Kibana (15601)        HTTP 200
  ✅ Mailpit (18025)       HTTP 200
  ✅ MinIO (19001)         HTTP 200
  ✅ Adminer (18083)       HTTP 200
  ✅ Redis Commander (18082) HTTP 200
  Result: ✅ PASS (12/12 accessible)
```

### Level 3: Application Health

Beyond port accessibility — does the application return **meaningful responses**?

```bash
# API health
curl -sf http://localhost:{api_port}/api/health/ping
# Expected: {"message":"pong","timestamp":"..."}

# Elasticsearch cluster
curl -sf http://localhost:{es_port}/_cluster/health
# Expected: {"status":"green"} or {"status":"yellow"}

# RabbitMQ queues exist
curl -sf -u guest:guest http://localhost:{rmq_mgmt_port}/api/queues
# Expected: logs.elasticsearch and emails.smtp queues listed

# Redis connectivity
docker compose exec redis redis-cli INFO server | head -5
# Expected: redis_version, uptime_in_seconds

# PostgreSQL tables
docker compose exec db psql -U {user} -d {db} -c '\dt'
# Expected: migration history table + any seeded tables
```

**Report format:**
```
Level 3 — Application Health:
  ✅ API health           {"message":"pong"}
  ✅ Elasticsearch        cluster: green, nodes: 1
  ✅ RabbitMQ queues      logs.elasticsearch ✓, emails.smtp ✓
  ✅ Redis                v7.x, uptime: 120s
  ✅ PostgreSQL           tables: __EFMigrationsHistory, Users, AuditLogs
  ✅ Seed data            admin@test.com exists
  Result: ✅ PASS (6/6 healthy)
```

### Level 4: Pipeline Smoke Tests

The most important level. **End-to-end proof** that each pipeline works.

#### 4.1 Logging Pipeline

```
Test: API writes a log → RMQ → LogIngest → Elasticsearch

Steps:
1. Call API endpoint: GET /api/health/ping
2. Wait 5 seconds (batch flush)
3. Query Elasticsearch for the log:
   curl -sf http://localhost:{es_port}/{project}-logs-*/_search?q=ping
4. Verify: log entry exists with service:"api", message contains "ping"
```

**Pass:** Log entry found in Elasticsearch within 10 seconds of API call.

#### 4.2 Email Pipeline

```
Test: API triggers email → RMQ → MailSender → Mailpit

Steps:
1. Call API auth register endpoint (if available) or trigger a test email
   POST /api/auth/register { email: "test-verify@test.com", password: "Test1234!" }
   (This should trigger a welcome email)
2. Wait 5 seconds
3. Check Mailpit for the email:
   curl -sf http://localhost:{mailpit_port}/api/v1/messages
4. Verify: email to test-verify@test.com exists in Mailpit
```

**Pass:** Email visible in Mailpit. If no auth register endpoint yet, skip with note: "Email pipeline ready but no trigger endpoint available yet."

#### 4.3 Auth Pipeline

```
Test: Register → Login → Token → Protected endpoint

Steps:
1. Register: POST /api/auth/register { email, password }
   → Expected: 200 + accessToken + refreshToken
2. Login: POST /api/auth/login { email, password }
   → Expected: 200 + accessToken
3. Use token: GET /api/health/ping with Authorization: Bearer {token}
   → Expected: 200
4. Without token: GET /api/auth/me (if exists)
   → Expected: 401
```

**Pass:** Full auth cycle works. If auth endpoints not yet implemented, skip with note.

#### 4.4 Socket Pipeline

```
Test: Socket connects and API can broadcast

Steps:
1. Check Socket is accepting connections:
   curl -sf http://localhost:{socket_port}/health (if exists)
2. Check Socket logs for "connected to RabbitMQ" or startup messages
3. (Full WebSocket test requires a client — note as manual test)
```

**Pass:** Socket service running and RMQ connected.

#### 4.5 Worker Pipeline

```
Test: Worker job executes on schedule

Steps:
1. Check Worker logs for SampleJob execution:
   docker compose logs worker --tail 20 | grep "SampleJob"
2. Verify: at least one "SampleJob executing" log entry exists
3. If SampleJob calls API: verify the API received the call (check API logs)
```

**Pass:** SampleJob has executed at least once.

#### 4.6 Redis Integration

```
Test: Redis is being used (tokens, settings, etc.)

Steps:
1. Check Redis has keys:
   docker compose exec redis redis-cli DBSIZE
2. If auth exists: register a user, check refresh token in Redis:
   docker compose exec redis redis-cli KEYS "refresh_token:*"
```

**Pass:** Redis has entries (settings seed or tokens).

#### 4.7 MinIO/Storage (if enabled)

```
Test: Default bucket exists

Steps:
1. Check MinIO bucket:
   curl -sf http://localhost:{minio_api_port}/minio/health/ready
2. Or check via mc: docker compose exec minio mc ls local/
```

**Pass:** MinIO healthy and default bucket exists.

---

## Final Report

After all levels complete, produce a comprehensive report:

```
╔══════════════════════════════════════════════════════════════╗
║                    SYSTEM VERIFICATION                       ║
║                    {ProjectName} — {date}                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Level 0 — Configuration:  ✅ PASS  (2/2 static checks)     ║
║  Level 1 — Containers:     ✅ PASS  (14/14 running)         ║
║  Level 2 — Ports:          ✅ PASS  (12/12 accessible)      ║
║  Level 3 — App Health:     ✅ PASS  (6/6 healthy)           ║
║  Level 4 — Pipelines:                                        ║
║    4.1 Logging:            ✅ PASS  (API→RMQ→ES verified)   ║
║    4.2 Email:              ✅ PASS  (email in Mailpit)      ║
║    4.3 Auth:               ✅ PASS  (register→login→token)  ║
║    4.4 Socket:             ✅ PASS  (connected, RMQ linked) ║
║    4.5 Worker:             ✅ PASS  (SampleJob executed)    ║
║    4.6 Redis:              ✅ PASS  (keys present)          ║
║    4.7 Storage:            ✅ PASS  (MinIO ready, bucket OK)║
║                                                              ║
║  OVERALL: ✅ ALL SYSTEMS OPERATIONAL                         ║
║                                                              ║
║  The system is verified and ready for development.           ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  Endpoints:                                                  ║
║    API:        http://localhost:13000                         ║
║    Swagger:    http://localhost:13000/swagger                 ║
║    Kibana:     http://localhost:15601                         ║
║    Mailpit:    http://localhost:18025                         ║
║    RabbitMQ:   http://localhost:25673                         ║
║    MinIO:      http://localhost:19001                         ║
║    Adminer:    http://localhost:18083                         ║
║    Redis UI:   http://localhost:18082                         ║
║                                                              ║
║  Test Credentials:                                           ║
║    Admin: admin@test.com / Admin123!                         ║
╚══════════════════════════════════════════════════════════════╝
```

If any test FAILS:
```
║  4.2 Email:              ❌ FAIL  (no email in Mailpit)     ║
║      → Check: docker compose logs mail-sender               ║
║      → Likely: RMQ topology not declared, or SMTP error     ║
```

Include diagnostic hints for each failure — what to check, what's likely wrong.

---

## Usage

**Standalone:**
```
/verify-system
```

**Called by /create-new-project:**
Phase 4 of project creation automatically runs this skill.

**After changes:**
Run anytime after infrastructure changes, compose updates, or if something feels wrong.

## Important Rules

1. **Wait for services to stabilize.** After `docker compose up`, wait 30-60 seconds before starting verification. Services need time to boot, migrate, connect.
2. **Skip gracefully.** If an endpoint doesn't exist yet (e.g., auth not implemented), skip that test with a note — don't fail the entire verification.
3. **Pipeline tests are the real proof.** Level 1-3 are basic checks. Level 4 proves the system actually works end-to-end.
4. **Log evidence.** For each pipeline test, show the actual log line or response that proves it worked.
5. **Ports from .env.** Read port numbers from `.env` file, don't hardcode. Every project might use different ports.
6. **Init containers are expected to exit.** minio-init, migration runners — these exit after their job. Don't flag them as failures.

## Accumulated Learnings

(Auto-rebuilt by /save-learnings from `learnings/*.md` frontmatter. Do not edit by hand. Initially empty — entries appear as the skill encounters reusable edge cases.)
