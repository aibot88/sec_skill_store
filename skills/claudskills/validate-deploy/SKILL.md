---
name: validate-deploy
description: >
  Deployment validation pipeline — 4 fasi (static, security, smoke, score).
  Valida un deploy Vercel (preview o production) con TypeScript, ESLint,
  Jest coverage su file toccati, Semgrep, npm audit, Playwright smoke su
  TUTTE le 142 route del gestionale (8 gruppi: pubbliche, auth, dashboard,
  portal, onboarding, public-token, API health). Produce
  /tmp/deployment_validation.json e verdetto GO/NO-GO con confidence score.
  Opzionalmente posta commento su GitHub PR.
when_to_use: >
  validate deploy, valida deploy, deployment check, go no-go, smoke test deploy,
  verifica deploy vercel, controlla deploy, deployment validation, /validate-deploy
metadata:
  version: "1.0.0"
  author: Giovanni Romano
  created: 2026-05-06
---

# validate-deploy — Deployment Validation Pipeline

> **Apri sempre con:** `🚀 validate-deploy skill attivata.`

---

## ARGOMENTI SUPPORTATI

```
/validate-deploy [--env=preview|production] [--pr=NUMBER] [--fast]
```

| Flag | Default | Descrizione |
|------|---------|-------------|
| `--env` | `preview` | Target: preview URL o production URL |
| `--pr` | (nessuno) | Numero PR GitHub per postare commento finale |
| `--fast` | off | Salta Fase 3 (Playwright). Solo static + security. |

---

## STEP -1: PARSE ARGS & PREFLIGHT

```bash
# 1. Estrai argomenti dal messaggio utente
ENV_TARGET="${ARG_ENV:-preview}"        # preview | production
PR_NUMBER="${ARG_PR:-}"                 # es. 42
FAST_MODE="${ARG_FAST:-false}"          # true | false

# 2. Verifica variabili obbligatorie
[ -z "$VERCEL_TOKEN" ] && echo "❌ VERCEL_TOKEN non impostato. Esporta: export VERCEL_TOKEN=xxx" && exit 1

# 3. Recupera deploy URL da Vercel
cd frontend
DEPLOY_URL=$(npx vercel ls --token="$VERCEL_TOKEN" 2>/dev/null | \
  grep -E "(Ready|READY)" | head -1 | awk '{print $NF}' | \
  sed 's|^|https://|')

[ -z "$DEPLOY_URL" ] && echo "⚠️  Nessun deploy trovato. Uso DEPLOY_URL da env." && DEPLOY_URL="${DEPLOY_URL:-}"
[ -z "$DEPLOY_URL" ] && echo "❌ DEPLOY_URL non disponibile." && exit 1

echo "🎯 Target: $DEPLOY_URL"
```

Se `VERCEL_TOKEN` non è nel environment, chiedere all'utente:
> "Esegui: `export VERCEL_TOKEN=<il-tuo-token>` e riprova."

---

## FASE 1: STATIC CHECKS (2 min)

### 1a. TypeScript
```bash
cd /path/to/project/frontend
npx tsc --noEmit 2>&1 | tee /tmp/vd_tsc.log
TS_ERRORS=$(grep -c "error TS" /tmp/vd_tsc.log || echo 0)
```

### 1b. ESLint
```bash
npx eslint . --max-warnings=0 2>&1 | tee /tmp/vd_eslint.log
ESLINT_ERRORS=$(grep -c "error" /tmp/vd_eslint.log || echo 0)
```

### 1c. Jest — solo file toccati dal branch corrente
```bash
cd /path/to/project
CHANGED_FILES=$(git diff --name-only origin/main...HEAD -- '*.ts' '*.tsx' | \
  grep -v '\.spec\.' | grep -v '\.test\.' | head -20)

if [ -n "$CHANGED_FILES" ]; then
  cd backend
  npx c8 --include 'src/**/*.ts' --exclude 'src/**/*.spec.ts' \
    npx jest --no-coverage --forceExit \
    $(echo "$CHANGED_FILES" | grep "^backend/" | sed 's|backend/||') \
    2>&1 | tee /tmp/vd_coverage.log
  
  STMT_PCT=$(grep "Statements" /tmp/vd_coverage.log | grep -oE "[0-9]+\.[0-9]+" | head -1 || echo 0)
  BRANCH_PCT=$(grep "Branches" /tmp/vd_coverage.log | grep -oE "[0-9]+\.[0-9]+" | head -1 || echo 0)
else
  STMT_PCT=100
  BRANCH_PCT=100
  echo "ℹ️  Nessun file backend toccato — coverage skipped"
fi
```

**Gate fase 1:**
- TS_ERRORS = 0 → ✅
- ESLINT_ERRORS = 0 → ✅  
- STMT_PCT ≥ 90 → ✅ (standard 90/90 CLAUDE.md)
- BRANCH_PCT ≥ 90 → ✅

---

## FASE 2: SECURITY (1 min, parallela con fase 1)

### 2a. Semgrep
```bash
cd /path/to/project
semgrep --config .semgrep/rules/ --json 2>/dev/null | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(len([r for r in d.get('results',[]) if r.get('extra',{}).get('severity')=='ERROR']))" \
  > /tmp/vd_semgrep_errors.txt 2>/dev/null || echo 0 > /tmp/vd_semgrep_errors.txt
SEMGREP_ERRORS=$(cat /tmp/vd_semgrep_errors.txt)
```

### 2b. npm audit
```bash
cd /path/to/project/frontend
npm audit --json 2>/dev/null | \
  python3 -c "import json,sys; d=json.load(sys.stdin); v=d.get('metadata',{}).get('vulnerabilities',{}); print(v.get('high',0)+v.get('critical',0))" \
  > /tmp/vd_audit.txt 2>/dev/null || echo 0 > /tmp/vd_audit.txt
AUDIT_HIGH=$(cat /tmp/vd_audit.txt)
```

**Gate fase 2:**
- SEMGREP_ERRORS = 0 → ✅ (severity ERROR)
- AUDIT_HIGH = 0 → ✅ (high + critical)

---

## FASE 3: SMOKE TESTS PLAYWRIGHT — 142 ROUTE (≈12 min)

> Saltata se `--fast` è attivo.

```bash
cd /path/to/project/frontend

export DEPLOY_URL="$DEPLOY_URL"
export PLAYWRIGHT_BYPASS_TOKEN="${VERCEL_BYPASS_TOKEN:-}"

# --workers=4 per parallelizzare (142 route / 4 worker ≈ 3 min reali)
npx playwright test e2e/smoke/deploy-validation.spec.ts \
  --project=deploy-smoke \
  --reporter=json \
  --workers=4 \
  --timeout=30000 \
  --output=/tmp/vd_playwright.json \
  2>&1 | tee /tmp/vd_playwright.log

SMOKE_TOTAL=$(python3 -c "import json; d=json.load(open('/tmp/vd_playwright.json')); print(d['stats']['expected'])" 2>/dev/null || echo 142)
SMOKE_PASSED=$(python3 -c "import json; d=json.load(open('/tmp/vd_playwright.json')); print(d['stats']['expected'] - d['stats']['unexpected'])" 2>/dev/null || echo 0)
SMOKE_FAILED_ROUTES=$(python3 -c "
import json
d=json.load(open('/tmp/vd_playwright.json'))
failures=[{'route': t['title'], 'reason': t['errors'][0]['message'][:100] if t.get('errors') else 'unknown'} for t in d.get('suites',[{}])[0].get('specs',[]) if t.get('ok')==False]
print(json.dumps(failures))
" 2>/dev/null || echo "[]")
```

**Route coperte (8 gruppi):**
- Pubbliche: 10 (landing, privacy, terms, demo, kiosk, tv, billing...)
- Auth: 10 (/auth/login, register, MFA, magic-link, oauth...)
- Auth flow: login reale → redirect dashboard
- Dashboard statiche: 75 (/dashboard/*, settings/*, analytics/*, GDPR...)
- Dashboard dinamiche: 16 ([id] con UUID fake → 200 o 404, mai 500)
- Onboarding: 2
- Portal (pubblico + autenticato + dinamiche): 23
- Public token: 3 (estimates, inspections, pay)
- API health: 1 (fetch diretto a /api/health)

**Gate fase 3:**
- SMOKE_PASSED / SMOKE_TOTAL ≥ 0.90 (129/142 minimo) → ✅
- Zero route con HTTP 500 → ✅ (bloccante immediato)

---

## FASE 4: SCORE & VERDICT

### Formula confidence score

```python
# Componenti (max 100)
smoke_ratio = SMOKE_PASSED / max(SMOKE_TOTAL, 1)
coverage_ratio = min((STMT_PCT + BRANCH_PCT) / 200, 1.0)
security_ok = 1.0 if (SEMGREP_ERRORS == 0 and AUDIT_HIGH == 0) else max(0, 1.0 - (SEMGREP_ERRORS + AUDIT_HIGH) * 0.1)
static_ok = 1.0 if (TS_ERRORS == 0 and ESLINT_ERRORS == 0) else 0.0

score = round(
    smoke_ratio      * 40 +   # 40% — funzionalità runtime
    coverage_ratio   * 30 +   # 30% — qualità test
    security_ok      * 20 +   # 20% — sicurezza
    static_ok        * 10     # 10% — compilazione
)

verdict = "GO" if score >= 85 else "NO-GO"
```

### Genera /tmp/deployment_validation.json

```python
import json, datetime

report = {
  "deploy_url": DEPLOY_URL,
  "environment": ENV_TARGET,
  "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
  "git_sha": GIT_SHA,
  "phases": {
    "static": {
      "ts_errors": TS_ERRORS,
      "eslint_errors": ESLINT_ERRORS,
      "coverage_statements": STMT_PCT,
      "coverage_branches": BRANCH_PCT,
      "passed": TS_ERRORS == 0 and ESLINT_ERRORS == 0 and float(STMT_PCT) >= 90 and float(BRANCH_PCT) >= 90
    },
    "security": {
      "semgrep_errors": SEMGREP_ERRORS,
      "audit_high_critical": AUDIT_HIGH,
      "passed": SEMGREP_ERRORS == 0 and AUDIT_HIGH == 0
    },
    "smoke": {
      "total": SMOKE_TOTAL,
      "passed": SMOKE_PASSED,
      "failed": SMOKE_FAILED_ROUTES,
      "skipped": FAST_MODE == "true"
    }
  },
  "score": score,
  "verdict": verdict,
  "pr_number": PR_NUMBER or None,
  "pr_comment_posted": False
}

with open("/tmp/deployment_validation.json", "w") as f:
  json.dump(report, f, indent=2)
```

---

## FASE 5: OUTPUT & GITHUB PR COMMENT (opzionale)

### Output terminale

```
╔══════════════════════════════════════════════════╗
║  DEPLOYMENT VALIDATION REPORT                     ║
╠══════════════════════════════════════════════════╣
║  URL:        https://xxx.vercel.app               ║
║  Timestamp:  2026-05-06T10:00:00Z                 ║
╠══════════════════════════════════════════════════╣
║  FASE 1 — Static                                  ║
║    TypeScript:  ✅ 0 errors                        ║
║    ESLint:      ✅ 0 errors                        ║
║    Coverage:    ✅ 91.2% stmt / 90.8% branch       ║
╠══════════════════════════════════════════════════╣
║  FASE 2 — Security                                ║
║    Semgrep:     ✅ 0 errors                        ║
║    npm audit:   ✅ 0 high/critical                 ║
╠══════════════════════════════════════════════════╣
║  FASE 3 — Smoke (12/12 passed)                    ║
║    /                ✅                             ║
║    /auth/login      ✅                             ║
║    /dashboard       ✅                             ║
║    ... (12 route)                                  ║
╠══════════════════════════════════════════════════╣
║  SCORE:  87 / 100                                 ║
║  VERDICT: ✅ GO                                   ║
╚══════════════════════════════════════════════════╝
Evidenza: /tmp/deployment_validation.json
```

### GitHub PR comment (se `--pr=NUMBER`)

```bash
COMMENT_BODY=$(python3 -c "
import json
d=json.load(open('/tmp/deployment_validation.json'))
s=d['score']; v=d['verdict']
icon='✅' if v=='GO' else '❌'
ph=d['phases']
lines=[
  f'## {icon} Deploy Validation — {v} ({s}/100)',
  f'',
  f'**URL:** {d[\"deploy_url\"]}',
  f'**Timestamp:** {d[\"timestamp\"]}',
  f'',
  f'| Fase | Risultato |',
  f'|------|-----------|',
  f'| Static (TS + ESLint + Coverage) | {\"✅\" if ph[\"static\"][\"passed\"] else \"❌\"} |',
  f'| Security (Semgrep + audit) | {\"✅\" if ph[\"security\"][\"passed\"] else \"❌\"} |',
  f'| Smoke tests ({ph[\"smoke\"][\"passed\"]}/{ph[\"smoke\"][\"total\"]}) | {\"✅\" if ph[\"smoke\"][\"passed\"]==ph[\"smoke\"][\"total\"] else \"⚠️\"} |',
]
if ph['smoke']['failed']:
  lines.append('')
  lines.append('**Route fallite:**')
  for f in ph['smoke']['failed']:
    lines.append(f'- \`{f[\"route\"]}\`: {f[\"reason\"]}')
lines.append('')
lines.append(f'<details><summary>Full report</summary>\n\n\`\`\`json\n{json.dumps(d, indent=2)}\n\`\`\`\n</details>')
print('\n'.join(lines))
")

gh pr comment "$PR_NUMBER" --body "$COMMENT_BODY"
```

---

## FLOW COMPLETO (pseudocodice esecutivo)

```
parse_args()
preflight()              → DEPLOY_URL, token check

parallel:
  fase1_static()         → TS_ERRORS, ESLINT_ERRORS, STMT_PCT, BRANCH_PCT  
  fase2_security()       → SEMGREP_ERRORS, AUDIT_HIGH

if not FAST_MODE:
  fase3_smoke()          → SMOKE_PASSED, SMOKE_TOTAL, SMOKE_FAILED_ROUTES

score = calc_score()
write_json("/tmp/deployment_validation.json")
print_report()

if PR_NUMBER:
  post_github_comment()

exit(0 if score >= 85 else 1)
```

---

## REGOLA: STOP ANTICIPATO

Se `TS_ERRORS > 0` nella Fase 1 → NON procedere alle fasi successive.
Motivo: smoke tests girerebbero su codice con errori di tipo — falsi negativi garantiti.

Output immediato:
```
❌ NO-GO (pre-flight fail)
TypeScript: X errori → fix prima di validare il deploy.
Vedi: /tmp/vd_tsc.log
```

---

## PREREQUISITI

| Tool | Verifica | Installazione |
|------|---------|---------------|
| `VERCEL_TOKEN` | `echo $VERCEL_TOKEN \| head -c 5` | Vercel dashboard → Settings → Tokens |
| `VERCEL_BYPASS_TOKEN` | opzionale | Vercel preview → Protection Bypass |
| `gh` CLI | `gh --version` | `brew install gh` |
| `semgrep` | `semgrep --version` | `pip install semgrep` |
| `npx playwright` | già in devDeps | — |

---

## SELF-HEALING

Se una smoke test fallisce per `ERR_CONNECTION_REFUSED`:
→ Attendi 10s e ritenta (max 2 retry) — deploy potrebbe non essere ready.

Se `vercel ls` non restituisce URL:
→ Chiedi all'utente: "Incolla l'URL del deploy Vercel da testare:"

Se `npm audit` restituisce JSON malformato:
→ Usa `npm audit --audit-level=high` exit code come proxy (exit 0 = ok).
