---
name: performance-budget
description: Performance budget tanımı + CI enforcement. Web Vitals (LCP/INP/CLS), JS/CSS bundle size, API p95/p99 latency, DB query, memory/CPU, cost budget. PR-time gate (size-limit, Lighthouse CI, k6 threshold). RUM authoritative (CrUX/Datadog/SpeedCurve). Regression detection trend-based.
---

# Performance Budget

## Ortak Doktrin

`agents/shared/severity-rubric.md` ve `agents/shared/escalation-matrix.md`
default-load sayılır (`agents/coordination.md` §11). Bu skill'in çıktısı
**Critical / High / Medium / Low + kanıt** formatında olmak zorunda — spekülatif
Critical yasak. Sahiplik dışı bulgu ilgili agent'a delege; karar yetkisi eşiği
aşılırsa **kullanıcı onayı zorunlu**.

## Felsefe

- **Budget = contract.** Aşılırsa PR red.
- **Production-like measure.** Localhost yanıltıcı; 3G + cold cache + p95/p99.
- **RUM authoritative.** Synthetic early warning; karar real user.
- **Per-page / per-route.** Tek global yanıltıcı.
- **Regression-first.** Trend > absolute.
- **Three-budget rule.** Quantity (request count), Timing (CWV), Cost ($/MB).

## Ne Zaman Kullanılır

- Yeni servis/sayfa go-live (initial budget tanımı)
- Quarterly budget review (production verisi ile revize)
- PR'de "biraz büyüdü" çatışması (objektif gate)
- Frontend regression hunt (LCP/INP regresyon)
- API SLO ihlal sonrası budget review
- Cost optimization (egress/storage budget)

## Workflow

### 1) Discovery — current state

```bash
# Frontend bundle
du -sh dist/* | sort -hr | head -10
npx source-map-explorer dist/main-*.js

# Lighthouse (mobile slow 4G profil)
npx lighthouse https://staging.example.com/checkout \
  --preset=desktop --output=json --output-path=baseline.json
jq '.audits["largest-contentful-paint"].numericValue,
    .audits["interaction-to-next-paint"].numericValue,
    .audits["cumulative-layout-shift"].numericValue' baseline.json

# API
k6 run perf/baseline.js --summary-export=baseline.json
jq '.metrics.http_req_duration["p(95)"], .metrics.http_req_duration["p(99)"]' baseline.json

# DB
psql -c "select query, mean_exec_time, p95_exec_time
         from pg_stat_statements
         order by total_exec_time desc limit 20;"
```

### 2) Budget tanımla (declarative)

`.budgets/checkout.yaml`:

```yaml
page: checkout
owner: "@checkout-team"
review_frequency: quarterly
last_reviewed: 2026-05-09
metrics:
  web_vitals:
    lcp_p75_ms: 2500
    inp_p75_ms: 200
    cls_p75: 0.1
    fcp_p75_ms: 1800
    ttfb_p75_ms: 800
  bundle:
    initial_gzip_kb: 90
    vendor_gzip_kb: 150
    css_initial_gzip_kb: 30
    route_chunk_gzip_kb: 40
  third_party:
    origin_count: 5
    js_gzip_kb: 80
  api:
    GET /api/checkout:
      p95_ms: 300
      p99_ms: 500
    POST /api/checkout/submit:
      p95_ms: 600
      p99_ms: 1000
  database:
    query_p95_ms: 50
    query_p99_ms: 200
    n_plus_1: 0
  cost:
    request_usd: 0.0001
    monthly_cap_usd: 500
regression_threshold_pct: 10
exemptions: []
```

### 3) CI gates

**Bundle (frontend)**:

```yaml
# .github/workflows/perf-budget.yml
- name: size-limit
  run: npx size-limit
- name: bundlemon
  uses: lironer/bundlemon@v3
```

`size-limit.config.js`:

```javascript
module.exports = [
  { path: 'dist/main-*.js', limit: '90 KB', gzip: true },
  { path: 'dist/checkout-*.js', limit: '50 KB', gzip: true },
  { path: 'dist/vendor-*.js', limit: '150 KB', gzip: true },
];
```

**Lighthouse CI per PR**:

```yaml
- name: Lighthouse CI
  run: |
    npm install -g @lhci/cli@0.13.x
    lhci autorun --config=.lighthouserc.json
```

`.lighthouserc.json`:

```json
{
  "ci": {
    "collect": {
      "url": ["http://localhost:3000/checkout"],
      "numberOfRuns": 3,
      "settings": { "preset": "desktop", "throttling": { "cpuSlowdownMultiplier": 4 } }
    },
    "assert": {
      "preset": "lighthouse:recommended",
      "assertions": {
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "interaction-to-next-paint": ["error", { "maxNumericValue": 200 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "total-byte-weight": ["error", { "maxNumericValue": 1500000 }],
        "uses-text-compression": "error",
        "uses-responsive-images": "warn"
      }
    },
    "upload": { "target": "temporary-public-storage" }
  }
}
```

**k6 API threshold**:

```javascript
// perf/budget-checkout.js
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: { smoke: { executor: 'constant-vus', vus: 5, duration: '60s' } },
  thresholds: {
    'http_req_duration{endpoint:get_checkout}': ['p(95)<300', 'p(99)<500'],
    'http_req_duration{endpoint:post_submit}':  ['p(95)<600', 'p(99)<1000'],
    'http_req_failed': ['rate<0.005'],
  },
};

export default function () {
  http.get(`${__ENV.BASE_URL}/api/checkout`, {
    tags: { endpoint: 'get_checkout' },
  });
}
```

### 4) RUM — real user monitoring

```typescript
// src/rum.ts
import { onLCP, onINP, onCLS, onFCP, onTTFB } from 'web-vitals';

function send(metric: { name: string; value: number; id: string }) {
  navigator.sendBeacon('/api/rum', JSON.stringify({
    metric: metric.name,
    value: metric.value,
    id: metric.id,
    url: location.pathname,
    timestamp: Date.now(),
  }));
}

onLCP(send);
onINP(send);
onCLS(send);
onFCP(send);
onTTFB(send);
```

Backend: aggregate Datadog RUM / Mixpanel / SpeedCurve.

Daily dashboard: p75 + p95 per page; >%5 regression alarm.

### 5) Regression detection

```python
# scripts/perf-regression-check.py
import json
import sys

baseline = json.load(open('baseline-7day.json'))
current = json.load(open('pr-build.json'))
threshold = 0.10  # 10%

failed = []
for page, m in current['metrics'].items():
    b = baseline['metrics'].get(page)
    if not b:
        continue
    for metric, value in m.items():
        bval = b.get(metric)
        if not bval:
            continue
        lift = (value - bval) / bval
        if lift > threshold:
            failed.append({
                'page': page, 'metric': metric,
                'baseline': bval, 'current': value, 'lift_pct': lift * 100,
            })

if failed:
    print(json.dumps(failed, indent=2))
    sys.exit(1)
```

PR bot yorum:

```text
Performance Budget Check
- LCP /checkout: 2.1s (budget 2.5s, baseline 2.0s, +5%) — OK
- INP /checkout: 240ms (budget 200ms, baseline 180ms, +33%) — REGRESSION
- Bundle main.js: 95 KB (budget 90 KB, baseline 88 KB, +8%) — OVER BUDGET
- API GET /checkout p95: 280ms (budget 300ms, baseline 250ms, +12%) — REGRESSION

Fail: 2 over budget, 1 regression > 10%.
```

### 6) Exemption & waiver

```yaml
exemptions:
  - metric: bundle_initial_gzip_kb
    route: /admin
    value: 250
    reason: "internal-only, performance non-critical"
    expires: 2026-08-09
    approved_by: "@cto"
```

Waiver 90 gün max; expire renew yoksa otomatik düşer.

### 7) Quarterly review

- Production p75 baseline güncelle (eski budget tutarsız ise revize).
- New page → budget tanım zorunlu.
- 3rd-party audit (ne kadar JS, hangi origin'ler, kim sahip).
- Cost trend kontrol (request başı maliyet, egress).

## Checklist

- [ ] Budget dosyası `.budgets/<page>.yaml` her sayfa için
- [ ] Owner + review frequency atanmış
- [ ] Web Vitals targets (LCP / INP / CLS p75)
- [ ] Bundle size limit (initial + vendor + per-route)
- [ ] API p95/p99 budget per endpoint
- [ ] DB p95/p99 budget + N+1 zero tolerance
- [ ] CI gate (size-limit + Lighthouse CI + k6)
- [ ] RUM kurulu + dashboard
- [ ] Regression detector (trend %10)
- [ ] PR bot yorumu
- [ ] Exemption expire takip (90g max)
- [ ] Quarterly review schedule

## Antipattern

- **Bütçe yok** — söylem var, ölçü yok.
- **Localhost ölçüm** — production-like değil.
- **Synthetic only** — RUM yok, gerçek kullanıcı görmüyor.
- **Global tek budget** — checkout ≠ landing.
- **Median budget** — p95/p99 olmalı.
- **PR-time gate yok** — sonra regress.
- **Bütçe waiver sahipsiz**.
- **CWV ignore** — SEO + UX penalty.
- **3rd-party JS kontrolsüz**.
- **N+1 kabul**.
- **Cost ignore**.
- **Regression alarmı yok**.
- **Owner yok**.

## Örnek Agent Davranışı

```text
User: /perf-budget checkout
Agent (delegate: frontend-performance-auditor + performance-profiler + ci-cd-engineer):
1. Discovery: bundle main 95 KB, vendor 162 KB, LCP 2.8s, INP 240ms, CLS 0.04.
   API GET /checkout p99 510ms, POST submit p99 980ms.
2. Bütçe taslağı: LCP 2.5s, INP 200ms, CLS 0.1, bundle 90/150, API p99 500/1000.
   Mevcut LCP/INP/bundle bütçe aşıyor → 3 issue.
3. CI gate: size-limit + Lighthouse CI + k6 PR.
4. RUM kurulum (web-vitals → Datadog).
5. Regression detector trend %10.
6. .budgets/checkout.yaml owner @checkout-team + quarterly review.
7. Action item: 4 issue (bundle split, INP investigation, RUM kurulum, API p99 tune).
```

## Çıktı Formatı

```markdown
# Performance Budget: <page-or-service>

## Current State (baseline)
- Web Vitals (LCP/INP/CLS p75)
- Bundle (initial/vendor/per-route gzip KB)
- API (p95/p99 per endpoint)
- DB (p95/p99 + N+1 count)
- Cost (request başı USD)

## Budget Definition (`.budgets/<page>.yaml`)

## CI Gate Configuration
- size-limit
- Lighthouse CI assertions
- k6 thresholds

## RUM Setup

## Regression Detector

## Findings (Critical/High/Medium/Low)

## Action Items
| P | Aksiyon | Sahip | Bitiş | Issue |

## Quarterly Review Schedule
```
