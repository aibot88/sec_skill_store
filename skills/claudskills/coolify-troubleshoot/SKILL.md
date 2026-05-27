---
name: coolify-troubleshoot
description: >
  This skill should be used when diagnosing Coolify deployment failures, HTTP errors (502, 504),
  Traefik routing issues, container restart loops, OOM kills, build failures, SSL certificate
  problems, Nixpacks build errors, health check failures, or Coolify self-repair. Trigger when:
  "Coolify 502", "Coolify 504", "Coolify bad gateway", "Traefik error Coolify", "container
  restart loop", "Coolify OOM", "Coolify build failed", "Nixpacks error", "SSL certificate
  Coolify", "Let's Encrypt Coolify", "Coolify not working", "restart Coolify", "Coolify
  update failed", "Coolify unreachable", "Coolify health check", "Coolify debug",
  "Coolify container crash", "Coolify deploy failed".
---

# Coolify Troubleshooting

Diagnostic flows for HTTP errors, container issues, build failures, SSL problems, and Coolify self-repair for v4 self-hosted.

> **Self-Hosted Only**: All diagnostic commands assume self-hosted Coolify v4.x with SSH access to the server. Coolify Cloud users have limited access to container-level debugging.

## Master Diagnostic Decision Tree

```
START: What's the symptom?
│
├─ HTTP error in browser?
│  ├─ 502 Bad Gateway → See "502 Diagnostic Flow"
│  ├─ 504 Gateway Timeout → See "504 Diagnostic Flow"
│  ├─ SSL certificate error → See "SSL Diagnostic Flow"
│  ├─ "404 page not found" → Domain not configured or Traefik misconfigured
│  └─ Traefik "no server" error → Container not running or wrong network
│
├─ Deployment failed?
│  ├─ Build failed → See "Build Failure Diagnosis"
│  └─ Build succeeded but container won't start → See "Container Lifecycle"
│
├─ Container issues?
│  ├─ Restart loop → See "Restart Loop Diagnosis"
│  ├─ OOM killed → See "OOM Diagnosis"
│  └─ Container exited → Check exit code (see table below)
│
├─ Coolify itself is broken?
│  └─ See "Coolify Self-Repair"
│
└─ None of the above?
   └─ Check Coolify server resources (disk, RAM, CPU)
      docker system df
      df -h
      free -m
```

## 502 Bad Gateway — Diagnostic Flow

A 502 means Traefik received the request but could not reach the backend container.

```
502 Bad Gateway
│
├─ 1. Is the container running?
│     docker ps | grep <APP_NAME>
│     ├─ Not running → Check deployment logs in Coolify UI
│     │  └─ Container crashed? Check: docker logs <CONTAINER>
│     └─ Running → Continue
│
├─ 2. Is the container healthy?
│     docker inspect <CONTAINER> | grep -A5 Health
│     ├─ unhealthy → App is running but health check fails
│     │  └─ Check health check path returns 200
│     └─ healthy or no health check → Continue
│
├─ 3. Is the app listening on the right port?
│     docker exec <CONTAINER> curl -s localhost:<PORT>/
│     ├─ Connection refused → App not binding to configured port
│     │  └─ Check PORT env var matches app's listen port
│     └─ Returns response → Container is fine, issue is Traefik → Continue
│
├─ 4. Are Traefik labels correct?
│     docker inspect <CONTAINER> | grep traefik
│     ├─ Missing or wrong labels → Coolify misconfigured routing
│     │  └─ Redeploy the application from Coolify UI
│     └─ Labels look correct → Continue
│
└─ 5. Is Traefik itself healthy?
      docker logs coolify-proxy --tail 50
      └─ Check for error messages about the backend
```

**Common 502 causes (ranked by frequency)**:
1. App crashes on startup — check `docker logs <CONTAINER>`
2. Wrong port — app listens on 8080 but Coolify expects 3000
3. App takes too long to start — Traefik tries to route before app is ready
4. Out of memory — container killed before it can serve requests

## 504 Gateway Timeout — Diagnostic Flow

A 504 means Traefik reached the container, but the response took too long.

```
504 Gateway Timeout
│
├─ Is it a specific endpoint or all requests?
│  ├─ Specific endpoint → Application-level timeout (slow query, external API)
│  │  └─ Profile the endpoint; check database queries, external calls
│  └─ All requests → Container overloaded or unresponsive
│
├─ Check container resource usage:
│  docker stats <CONTAINER> --no-stream
│  ├─ CPU near 100% → App is CPU-bound; scale up or optimize
│  └─ Memory near limit → OOM pressure; increase memory limit
│
└─ Check Traefik timeout configuration:
   Default timeout is 30 seconds
   For long-running requests, increase via Traefik labels or Coolify settings
```

## Container Lifecycle Issues

### Exit Code Reference

| Exit Code | Meaning | Common Cause |
|-----------|---------|-------------|
| 0 | Clean exit | App finished normally (may be wrong for long-running services) |
| 1 | General error | Unhandled exception, missing env var, config error |
| 126 | Permission denied | CMD not executable; check Dockerfile USER and file permissions |
| 127 | Command not found | Wrong start command; binary doesn't exist in image |
| 137 | SIGKILL (OOM) | Container exceeded memory limit |
| 139 | SIGSEGV | Segmentation fault; native module crash |
| 143 | SIGTERM | Graceful shutdown (normal during redeploy) |

### Restart Loop Diagnosis

```bash
# Check restart count
docker inspect <CONTAINER> --format '{{.RestartCount}}'

# Check last exit code
docker inspect <CONTAINER> --format '{{.State.ExitCode}}'

# Check last N log lines (may show crash reason)
docker logs <CONTAINER> --tail 50

# Check if OOM killed
docker inspect <CONTAINER> --format '{{.State.OOMKilled}}'
```

**Resolution by exit code**:
- **Exit 1**: Read the logs — usually a config error or missing env var
- **Exit 137**: Increase memory limit or optimize the app
- **Exit 127**: Fix the start command in Coolify settings
- **Exit 126**: Fix file permissions in Dockerfile

### OOM Kill Confirmation

```bash
# Method 1: Docker inspect
docker inspect <CONTAINER> --format '{{.State.OOMKilled}}'
# Returns "true" if OOM killed

# Method 2: System logs
dmesg | grep -i "oom\|killed" | tail -10

# Method 3: Docker events
docker events --filter 'event=oom' --since '1h'
```

**Fix**: Increase the memory limit in Coolify application settings, or optimize the app to use less memory.

## Build Failure Diagnosis

### Nixpacks Build Failures

| Error Pattern | Cause | Fix |
|--------------|-------|-----|
| `no matching Nix packages` | Nixpacks can't resolve a dependency | Add via `NIXPACKS_PKGS` or `NIXPACKS_APT_PKGS` |
| `npm ERR! code ERESOLVE` | Dependency conflict | Use `npm install --legacy-peer-deps` via `NIXPACKS_INSTALL_CMD` |
| `error: could not find` | Missing system library | Add to `NIXPACKS_APT_PKGS` (e.g., `libvips-dev`) |
| `ENOMEM` during build | Build process ran out of memory | Set `NODE_OPTIONS=--max-old-space-size=2048` |
| `permission denied` | File permission issues in Nix sandbox | Check `.gitignore` isn't excluding needed files |
| `Could not detect language` | No recognizable project file | Set build pack manually or add appropriate manifest file |

### Reading Build Logs

Build logs in Coolify contain both Coolify orchestration output and the actual build output. Focus on:

1. **Skip** the initial "Pulling repository..." and "Starting build..." lines
2. **Look for** the first `ERROR`, `error`, `FAILED`, or non-zero exit code
3. **The actual error** is usually 5-10 lines BEFORE "Build failed" at the end
4. **Ignore** Coolify's wrapper messages; focus on the build tool's output (npm, pip, cargo, etc.)

### Force Clean Build

```bash
# Via Coolify API
curl -X POST "https://<COOLIFY>/api/v1/applications/<UUID>/deploy" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"force": true}'

# Or from Coolify UI: Deploy → "Force Rebuild" toggle
```

Build cache invalidation: Coolify caches Docker layers between builds. A force rebuild ignores the cache entirely.

## SSL Certificate Issues

### Diagnostic Flow

```
SSL Error in Browser
│
├─ 1. Is DNS pointing to the Coolify server?
│     dig <DOMAIN> A    (should show server IP)
│     ├─ Wrong IP → Fix DNS records
│     └─ Correct → Continue
│
├─ 2. Is port 80 open? (Required for HTTP-01 challenge)
│     curl http://<DOMAIN>/.well-known/acme-challenge/test
│     ├─ Connection refused → Firewall blocking port 80
│     │  └─ ufw allow 80/tcp
│     └─ Returns something → Port is open → Continue
│
├─ 3. Check Traefik ACME logs:
│     docker logs coolify-proxy 2>&1 | grep -i "acme\|certificate\|letsencrypt"
│     ├─ Rate limit → Too many cert requests; wait 1 hour
│     ├─ DNS challenge failed → DNS not propagated yet
│     └─ Challenge succeeded but cert not applied → Restart Traefik
│
└─ 4. Force certificate renewal:
      # Restart Traefik to re-trigger ACME
      docker restart coolify-proxy
      # Or delete the ACME storage and restart
      # WARNING: This renews ALL certificates
```

### Let's Encrypt Challenge Types

| Challenge | How It Works | When to Use |
|-----------|-------------|-------------|
| **HTTP-01** (default) | Traefik serves a token on `http://<domain>/.well-known/acme-challenge/` | Standard web apps; port 80 must be open |
| **DNS-01** | TXT record added to DNS | Wildcard certs; port 80 not required; supported DNS providers only |

### Custom Certificates

For non-Let's Encrypt certificates:
1. Upload cert and key files via Coolify UI (Application → SSL settings)
2. Or mount them as volumes and configure Traefik labels manually

## Coolify Self-Repair

### Restart Coolify Without Affecting Apps

```bash
# SSH into the server, then:
cd /data/coolify/source
docker compose restart

# Or restart specific Coolify services:
docker restart coolify          # Main Coolify app
docker restart coolify-proxy    # Traefik reverse proxy
docker restart coolify-realtime # Websocket/realtime service
```

**Running app containers are NOT affected** by restarting Coolify. They continue serving traffic independently.

### Coolify Self-Update

```bash
# Recommended: Use the UI → Settings → Update
# Or from CLI:
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
```

**What can go wrong**:
- Database migration failure → Coolify won't start → check `docker logs coolify`
- Port conflict → another service grabbed Coolify's port
- Docker version incompatibility → rare, but check Docker version requirements

### "Coolify Is Unreachable" Diagnosis

```bash
# 1. Check if Coolify containers are running
docker ps | grep coolify

# 2. Check Coolify logs
docker logs coolify --tail 100

# 3. Check if port 8000 is listening
ss -tlnp | grep 8000

# 4. Check disk space (Coolify fails silently when disk is full)
df -h

# 5. Check if Docker is running
systemctl status docker

# 6. Check server resources
free -m
top -bn1 | head -5
```

## Anti-Patterns

| Anti-Pattern | Consequence |
|-------------|-------------|
| Restarting Coolify as first troubleshooting step | Wastes time; doesn't fix app-level issues |
| Deleting and recreating the app instead of debugging | Loses deployment history, env vars, and volume data |
| Ignoring exit codes and only reading the last log line | Misses the actual root cause |
| Not setting health checks, then wondering why 502s occur during deploys | No health check = no zero-downtime deploys |
| Force-rebuilding every time instead of investigating cache issues | 3-10x slower builds; masks the real problem |
| Exposing debug ports (9229, 5005) in production | Security risk; remote code execution possible |
| Running `docker system prune -a` without checking | Removes all cached images; next build will be very slow |
| Deleting ACME storage to "fix" SSL | Forces renewal of ALL certs; may hit rate limits |

## Related Skills

- **coolify-deploy** — Deployment configuration, build pack selection
- **coolify-security** — Resource limits, OOM prevention
- **coolify-observability** — Monitoring, log drains, alerting
- **coolify-databases** — Database connection issues, OOM

## Additional Resources

### Reference Files

- **`references/traefik-debugging.md`** — Traefik v3 routing diagnosis, label inspection, dynamic config
- **`references/common-errors.md`** — Expanded error pattern table with fixes for 50+ common issues
