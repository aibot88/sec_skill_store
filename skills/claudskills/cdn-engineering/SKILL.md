---
name: cdn-engineering
description: CDN (CloudFront/Cloudflare/Fastly) disipline — cache key composition (URL + Vary + cookie/query whitelist), TTL strategy (s-maxage CDN + max-age browser + stale-while-revalidate + stale-if-error), origin shield, purge (single/wildcard/tag/all), signed URL (CloudFront/Cloudflare/Fastly token), image optimization (AVIF/WebP edge transform), HLS/DASH streaming, multi-CDN failover (DNS health check + RUM routing), edge compute (Workers/Lambda@Edge/Compute@Edge), TLS termination Full(strict), WAF + DDoS, RUM, cost tracking.
---

# CDN Engineering

## Ortak Doktrin

`agents/shared/severity-rubric.md` ve `agents/shared/escalation-matrix.md`
default-load sayılır (`agents/coordination.md` §11). Bu skill'in çıktısı
**Critical / High / Medium / Low + kanıt** formatında olmak zorunda — spekülatif
Critical yasak. Sahiplik dışı bulgu ilgili agent'a delege; karar yetkisi eşiği
aşılırsa **kullanıcı onayı zorunlu**.

## Felsefe

- **Cache key explicit** — default-cached yanıltıcı.
- **TTL doğru ölçü** — s-maxage ≠ max-age.
- **Stale-while-revalidate** edge'de altın standart.
- **Purge eventually consistent** — versioned URL > purge.
- **Origin shield** — origin'i N POP'tan değil 1'den vur.
- **Multi-CDN failover** SaaS-critical.
- **WAF + DDoS edge'de**.

## Ne Zaman Kullanılır

- Yeni site / API CDN onboarding
- Cache hit rate düşük (< %70)
- Origin overwhelmed (egress spike, latency)
- LCP regresyon (CDN miss veya konfig kötü)
- Multi-CDN failover kurulum (vendor outage incident sonrası)
- Image optimization (mobile data savings)
- HLS/DASH video streaming
- Signed URL private content
- Edge compute (A/B at edge, auth)
- Cost optimization (egress, requests)
- WAF + DDoS audit
- TLS cert lifecycle

## Workflow

### 1) Discovery — current state

```bash
# Cache hit rate
curl -I https://acme.com/index.html | grep -i "cf-cache-status\|x-cache\|age"
# CloudFront: X-Cache: Hit from cloudfront
# Cloudflare: cf-cache-status: HIT
# Fastly: x-cache: HIT, HIT

# TTL headers
curl -I https://acme.com/api/products | grep -iE "cache-control|vary|surrogate"
```

CDN dashboard:

- Hit rate per zone / path
- Bandwidth + request count
- p50/p95 RTT per POP
- Error rate

Hedef: > %85 hit rate static; > %60 dynamic.

### 2) Cache key audit

```yaml
# Cloudflare cache rule
cache_key:
  custom_key:
    query_string: { include: [page, size, sort] }     # tracker (utm_*) exclude
    header: { include: [Accept-Encoding, Accept-Language] }
    cookie: { include: [session_id, locale] }
    host: { resolved: true }
  ignore_query_strings_order: true
```

CloudFront equivalent: Cache Policy + Origin Request Policy.

### 3) TTL matrix

Site başına:

| Path | Browser | CDN | SWR | Notes |
|---|---|---|---|---|
| `/_/assets/*` | 1y | 1y | — | immutable versioned |
| `/index.html` | 5 sn | 5 dk | 2 dk | personalization yok |
| `/api/products` | 60 sn | 5 dk | 2 dk | catalog |
| `/api/orders` | 0 | 0 | — | no-store private |
| `/images/*` | 1d | 1y | 10 dk | content-hash URL |
| `/sitemap.xml` | 10 dk | 1 saat | 10 dk | |

Origin'den:

```http
Cache-Control: public, max-age=60, s-maxage=300,
               stale-while-revalidate=120, stale-if-error=86400
Vary: Accept-Encoding, Accept-Language
Surrogate-Key: product-catalog homepage
```

### 4) Origin shield enable

CloudFront:

```json
{
  "OriginShield": {
    "Enabled": true,
    "OriginShieldRegion": "eu-west-1"
  }
}
```

Cloudflare: Argo Tiered Cache settings.
Fastly: Shielding per service config.

### 5) Purge strategy

`Surrogate-Key` header origin'den:

```http
Cache-Control: public, max-age=3600
Surrogate-Key: user-123 product-456 catalog-page
```

Tag-based purge:

```bash
# Cloudflare tag purge
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE/purge_cache" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"tags": ["product-456", "catalog-page"]}'

# Fastly surrogate key
curl -X POST "https://api.fastly.com/service/$SVC/purge/product-456" \
  -H "Fastly-Key: $TOKEN"
```

CloudFront tag purge yok — invalidation path-based; wildcard:

```bash
aws cloudfront create-invalidation \
  --distribution-id E123 --paths "/products/456" "/catalog/*"
```

Critical update → **versioned URL** (cache-bust) > purge.

### 6) Signed URL

```python
# CloudFront
from botocore.signers import CloudFrontSigner
import datetime

def signed_url(resource: str, expire_seconds: int = 3600) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(seconds=expire_seconds)
    signer = CloudFrontSigner(KEY_PAIR_ID, rsa_sign_func)
    return signer.generate_presigned_url(resource, date_less_than=expire)
```

```javascript
// Cloudflare Workers signed URL
const SECRET = env.SIGN_SECRET;
async function sign(url, expireUnix) {
  const data = `${url}${expireUnix}`;
  const key = await crypto.subtle.importKey(
    'raw', new TextEncoder().encode(SECRET),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign'],
  );
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(data));
  return `${url}?expires=${expireUnix}&signature=${btoa(String.fromCharCode(...new Uint8Array(sig)))}`;
}
```

**Disiplin**: expire ≤ 24h; KMS key rotation 90g; IP allowlist (opsiyonel).

### 7) Image optimization

```html
<picture>
  <source type="image/avif" srcset="
    /image/cat.jpg?w=400&format=avif 1x,
    /image/cat.jpg?w=800&format=avif 2x
  ">
  <source type="image/webp" srcset="
    /image/cat.jpg?w=400&format=webp 1x,
    /image/cat.jpg?w=800&format=webp 2x
  ">
  <img src="/image/cat.jpg?w=400" loading="lazy" alt="cat" width="400" height="300">
</picture>
```

Edge transform:

- Cloudflare Image Resizing (`/cdn-cgi/image/width=400,format=auto/...`)
- Fastly IO
- Cloudinary / Imgix (SaaS)
- AWS Serverless Image Handler (Lambda@Edge)

Origin: single high-res; edge transform + cache.

### 8) HLS/DASH

```nginx
# origin
location /hls/ {
  add_header Cache-Control "public, max-age=5, s-maxage=10";   # manifest
}
location /hls/segments/ {
  add_header Cache-Control "public, max-age=31536000, immutable";  # segment
}
```

Low-latency HLS (LL-HLS): chunked transfer; segment 2-6s; sub-2s glass-to-glass.

### 9) Multi-CDN failover

DNS-level (NS1 / Route 53 / Cedexis):

```yaml
# NS1 weighted + health
records:
  - { answer: cf.acme.com, weight: 70, health_check: cf-health }
  - { answer: fastly.acme.com, weight: 30, health_check: fastly-health }
health_check:
  cf-health: { type: http, url: https://cf.acme.com/_health, interval: 30s }
```

RUM-based routing: client-side beacon → DNS provider hangi POP en hızlı.

### 10) Edge compute örnek

```javascript
// Cloudflare Worker — A/B test at edge
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/checkout') {
      // Consistent assignment per user
      const cookie = request.headers.get('cookie') || '';
      let variant = cookie.match(/exp=([ab])/)?.[1];
      if (!variant) {
        variant = Math.random() < 0.5 ? 'a' : 'b';
      }
      url.pathname = variant === 'b' ? '/checkout-new' : '/checkout';
      const response = await fetch(url, request);
      const newResp = new Response(response.body, response);
      newResp.headers.append('Set-Cookie', `exp=${variant}; Path=/; Max-Age=2592000`);
      return newResp;
    }
    return fetch(request);
  },
};
```

`/experiment-design` skill bağı.

### 11) TLS hardening

```text
[client] --TLS 1.3--> [CDN] --TLS 1.2+--> [origin]
                          Full (strict)
```

Cloudflare SSL mode: **Full (strict)** zorunlu; Flexible yasak.

Origin cert: Cloudflare Origin CA (15 yıl, origin-only) veya Let's Encrypt
ile DNS-01 validation.

### 12) WAF + DDoS + Origin lock

```yaml
# CloudFront — origin custom header (CDN-only allow)
custom_header:
  name: X-CDN-Auth
  value: $SECRET_TOKEN

# origin (nginx)
if ($http_x_cdn_auth != "$SECRET_TOKEN") {
  return 403;
}
```

Cloudflare prefix list IP allowlist (origin SG):

```bash
curl https://api.cloudflare.com/client/v4/ips/v4
# nginx allow + deny all
```

WAF managed rules: OWASP CRS, Bot Management.

### 13) RUM kurulum

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/web-vitals/4/web-vitals.iife.js"></script>
<script>
window.webVitals.onLCP(({value}) => beacon('lcp', value));
window.webVitals.onINP(({value}) => beacon('inp', value));
window.webVitals.onCLS(({value}) => beacon('cls', value));
</script>
```

Beacon → CDN edge logger (Cloudflare Analytics, Datadog RUM).

### 14) Cost dashboard

| Metric | Threshold | Alert |
|---|---|---|
| Cache hit rate | < %70 | warn; < %50 page |
| Bandwidth / 24h | baseline +%20 | warn |
| Egress USD / day | baseline +%30 | page |
| Image transform / day | quota %80 | warn |

`/cost-review` skill bağı.

## Checklist

- [ ] Cache hit rate baseline + alarm (< %70 warn)
- [ ] Cache key composition explicit (cookie + query whitelist)
- [ ] TTL matrix per path
- [ ] Cache-Control + Vary + Surrogate-Key origin header
- [ ] Origin shield enabled
- [ ] Purge strategy (tag-based; versioned URL > purge critical)
- [ ] Signed URL private content (expire ≤ 24h + key rotation)
- [ ] Image optimization edge transform (AVIF/WebP)
- [ ] HLS/DASH manifest vs segment ayrı TTL
- [ ] Multi-CDN failover (DNS health + RUM routing) SaaS-critical
- [ ] Edge compute (A/B, auth, geo redirect; CPU < 50ms)
- [ ] TLS Full (strict); origin cert managed
- [ ] WAF + DDoS managed rules + custom
- [ ] Origin IP private (CDN allowlist only)
- [ ] RUM (LCP/INP/CLS) edge logging
- [ ] Cost dashboard (egress + requests + transform)
- [ ] Quarterly cost + cache hit review

## Antipattern

- **Cache-Control eksik** (provider default).
- **Vary yok** (auth/encoding leak).
- **Tüm cookie cache key'de**.
- **Tüm query param cache key'de** (utm_* tracker flood).
- **Purge'e güven** (eventually consistent).
- **`no-cache` ≠ `no-store` karıştırma**.
- **Origin shield kapalı**.
- **Cache hit rate ölçüm yok**.
- **Edge ↔ origin plaintext** (Flexible mode).
- **Origin IP public** (direct DDoS bypass).
- **Signed URL expire > 24h**.
- **Image runtime resize her request**.
- **Single CDN SaaS-critical**.
- **WAF rules custom-only OWASP kapalı**.
- **Edge compute > 50ms CPU**.
- **TLS cert manuel renew**.
- **Tag-based purge yok** (wildcard hammer).
- **Static asset versioning yok** (?v= query → cache key flood).
- **RUM yok**.

## Örnek Agent Davranışı

```text
User: /cdn-review acme.com
Agent (platform-engineer + frontend-performance-auditor + security-reviewer):

1. Current state:
   - Cloudflare zone, free plan
   - Cache hit rate %52 ⚠ (target > %85 static)
   - Egress 8.2 TB / ay → $640
   - LCP p75 mobile 3.2s (target 2.5s)

2. Cache key audit: tüm cookie + tüm query param cache key'de
   (utm_source/utm_medium flood) → hit rate düşük.

3. TTL audit: 22 endpoint Cache-Control eksik; 8 endpoint `Cache-Control:
   no-cache` (yanlış; `no-store` istiyorlar).

4. Vary audit: 14 endpoint Vary yok; Authorization leak riski.

5. Origin shield kapalı; her POP origin'e vurar → N× egress.

6. Image optimization yok; JPEG full-res 7MB hero.

7. TLS Flexible mode (edge→origin HTTP). MITM riski.

8. Origin IP public; DDoS bypass mümkün.

9. RUM yok.

10. WAF managed rules kapalı; sadece custom 3 rule.

Findings:
- Critical: TLS Flexible (edge→origin plaintext)
- Critical: Origin IP public (no CDN allowlist)
- Critical: WAF managed rules disabled
- High: Cache hit rate %52 (cache key cookie/query flood)
- High: 14 endpoint Vary missing (auth leak)
- High: Origin shield disabled (N× egress + $$$)
- High: 22 endpoint Cache-Control missing
- Medium: Image not optimized (AVIF/WebP yok)
- Medium: Multi-CDN failover yok
- Medium: RUM yok
- Low: Static asset query versioning (?v=) cache flood

Action items: 11 issue + 4-week roadmap, projected cost -%45,
LCP improvement → < 2.5s.
```

## Çıktı Formatı

```markdown
# CDN Review: <site | service>

## Current state
- Provider + plan
- Cache hit rate
- Egress + requests
- LCP/INP (RUM if available)

## Cache key audit

## TTL matrix per path

## Origin shield + purge strategy

## Signed URL (varsa private content)

## Image / HLS / DASH

## Multi-CDN failover

## Edge compute (varsa)

## TLS + WAF + DDoS + Origin lock

## RUM + Cost dashboard

## Findings (Critical/High/Medium/Low)

## Action Items
| P | Aksiyon | Sahip | Bitiş |
```
