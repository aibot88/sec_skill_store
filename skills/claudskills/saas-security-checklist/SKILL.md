---
name: saas-security-checklist
last_verified: 2026-04-02
description: "Security checklist specifically for SaaS applications built with Next.js, Supabase, and Stripe. Covers authentication hardening, Row Level Security, Stripe webhook verification, secrets management, CSRF/CSP/CORS headers, input validation, rate limiting, DSGVO/GDPR compliance, and common anti-patterns found in real SaaS templates. Triggers on: SaaS security, Supabase security, Stripe security, SaaS checklist, secure SaaS, harden SaaS, SaaS audit, Next.js security, Supabase RLS audit, payment security, or any security review of a SaaS application."
---

# SaaS Security Checklist

Sicherheits-Checklist speziell fuer SaaS-Anwendungen mit Next.js, Supabase und Stripe. Jedes Finding referenziert das Repo, in dem das Anti-Pattern gefunden wurde.

**Abgrenzung zum security-scanner Skill:** Der `security-scanner` deckt allgemeine OWASP Top 10 ab. Dieser Skill ist SaaS-spezifisch: Subscription-Autorisierung, Payment-Webhook-Security, Supabase-RLS, Multi-Tenant-Isolation. Fuer vollstaendige Abdeckung BEIDE Skills zusammen verwenden.

---

## Scoring Rubric

Nach Durchlauf der Checklist, Score berechnen:

| Score | Rating | Bedeutung |
|-------|--------|-----------|
| 0-40% | **CRITICAL** | Sofortige Sicherheitsprobleme. NICHT deployen. |
| 40-70% | **NEEDS WORK** | Signifikante Luecken. Vor Production fixen. |
| 70-90% | **SOLID** | Gute Basis. Kleinere Verbesserungen noetig. |
| 90-100% | **HARDENED** | Production-ready Security Posture. |

---

## 1. Authentication Layer

### Kritische Findings aus Repo-Analyse

| Finding | Schwere | Gefunden in |
|---------|---------|-------------|
| Kein Middleware-basierter Route-Schutz, nur Layout-Redirects | KRITISCH | Saas-Kit-supabase |
| Password-Feld als type="text" (Klartext sichtbar) | HOCH | Saas-Kit-supabase |
| Hardcodiertes JWT Secret ("your-secret-key") | KRITISCH | intelligent-rag-service |
| Dummy-Authentifizierung (user/password) | KRITISCH | intelligent-rag-service |
| python-jose (unmaintained seit 2023) | HOCH | scalable-rag-pipeline |
| Deprecated @supabase/auth-helpers-nextjs | HOCH | Saas-Kit-supabase |

### Checklist

- [ ] @supabase/ssr verwendet (NICHT deprecated @supabase/auth-helpers-nextjs)
- [ ] Middleware-basierter Route-Schutz (NICHT nur Layout-Level-Redirects)
- [ ] `getUser()` statt `getSession()` fuer Server-seitige Validierung
- [ ] Alle Password-Felder als type="password"
- [ ] JWT Secrets aus Environment-Variablen (NIEMALS hardcoded)
- [ ] Maintained JWT Library (PyJWT oder joserfc, NICHT python-jose)
- [ ] Session Cookies: HttpOnly, Secure, SameSite=Lax
- [ ] OAuth State-Parameter validiert im Callback
- [ ] MFA-Support mindestens fuer Admin-Accounts
- [ ] Account-Lockout nach N fehlgeschlagenen Versuchen
- [ ] Sicherer Password-Reset-Flow (zeitlich limitierte Tokens)
- [ ] Rate Limiting auf Auth-Endpoints

---

## 2. Row Level Security (Supabase)

### Kritische Findings

| Finding | Schwere | Gefunden in |
|---------|---------|-------------|
| KEIN RLS auf profiles und subscriptions | KRITISCH | Saas-Kit-supabase |
| anon-Rolle hat unnoetige Rechte auf todo_list | MITTEL | supabase-nextjs-template |
| CREATE TRIGGER fuer Profil-Erstellung fehlt in Migration | HOCH | Saas-Kit-supabase |

### Checklist

- [ ] RLS AKTIVIERT auf JEDER Tabelle mit User-Daten
- [ ] SELECT Policies: User kann nur eigene Daten lesen
- [ ] INSERT Policies: user_id wird aus auth.uid() gesetzt, nicht vom Client
- [ ] UPDATE Policies: User kann nur eigene Records aendern
- [ ] DELETE Policies: User kann nur eigene Records loeschen
- [ ] Service Role NUR in server-seitigem Code (Webhooks, Server Actions)
- [ ] anon-Rolle hat MINIMALE Permissions
- [ ] Kein RLS-Bypass via direkten Tabellenzugriff
- [ ] RLS-Policies getestet: Versuch, fremde Daten zu lesen
- [ ] Trigger-Functions nutzen SECURITY DEFINER mit explizitem search_path
- [ ] CREATE TRIGGER Statement in Migrations vorhanden
- [ ] Storage-Buckets mit user-spezifischen Pfaden und RLS

---

## 3. Payment Security (Stripe)

### Checklist

- [ ] STRIPE_SECRET_KEY nur server-side (KEIN NEXT_PUBLIC_ Prefix)
- [ ] Webhook-Signatur auf JEDEM Event verifiziert (constructEvent)
- [ ] Webhook-Endpoint nutzt Raw Body (nicht JSON-parsed) fuer Signatur
- [ ] Idempotente Webhook-Verarbeitung (Event-ID pruefen)
- [ ] Subscription-Status server-side geprueft (nicht client-side)
- [ ] Price IDs gegen erlaubte Liste validiert
- [ ] Customer Portal Session server-side erstellt mit authentifiziertem User
- [ ] Keine Subscription-Daten in localStorage oder Client-State
- [ ] Grace Period bei Payment Failure (nicht sofort sperren)
- [ ] Stripe CLI fuer lokales Webhook-Testing konfiguriert
- [ ] SUPABASE_SERVICE_ROLE_KEY nur in Webhook-Handler, nie im Client

---

## 4. Secrets Management

### Kritische Findings

| Finding | Schwere | Gefunden in |
|---------|---------|-------------|
| AWS Account ID (038462775601) hardcoded in Code und CI | KRITISCH | intelligent-rag-service |
| IAM Role ARN hardcoded in Kubernetes-Manifesten | KRITISCH | intelligent-rag-service |
| JWT Secret als "your-secret-key" im Code | KRITISCH | intelligent-rag-service |
| Default-Secrets in Config-Dateien | HOCH | scalable-rag-pipeline |

### Checklist

- [ ] Alle Secrets in Environment-Variablen (NIEMALS im Code)
- [ ] .env Dateien in .gitignore
- [ ] .env.example mit Placeholder-Werten (nie echte Secrets)
- [ ] Keine AWS Account IDs, ARNs oder API Keys in Code oder CI-Manifesten
- [ ] Production-Secrets in AWS Secrets Manager / Vault / Supabase Vault
- [ ] Secret-Rotation bei Verdacht auf Exposure
- [ ] Git-History clean (git-filter-repo wenn noetig)
- [ ] CI/CD nutzt GitHub Secrets oder Equivalent
- [ ] Keine Secrets in Docker-Images oder Build-Logs
- [ ] SUPABASE_SERVICE_ROLE_KEY nicht in Client-bundles

---

## 5. HTTP Security Headers

### Findings

| Finding | Schwere | Gefunden in |
|---------|---------|-------------|
| Kein CSRF-Schutz | MITTEL | Saas-Kit-supabase |
| Keine CSP-Headers | MITTEL | Saas-Kit-supabase |
| Kein Rate Limiting | MITTEL | Saas-Kit-supabase |

### Checklist

- [ ] Content-Security-Policy Header konfiguriert
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY (oder CSP frame-ancestors)
- [ ] Strict-Transport-Security (HSTS)
- [ ] Referrer-Policy: strict-origin-when-cross-origin
- [ ] Permissions-Policy: Camera, Microphone, Geolocation einschraenken
- [ ] CORS: Explizite Origins, KEIN Wildcard * in Production
- [ ] CSRF-Schutz auf allen state-mutierenden Endpoints

### Next.js Header-Konfiguration

```typescript
// next.config.ts
const securityHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "X-XSS-Protection", value: "1; mode=block" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
  {
    key: "Content-Security-Policy",
    value: "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://*.supabase.co wss://*.supabase.co https://api.stripe.com;",
  },
];
```

---

## 6. Input Validation

### Checklist

- [ ] Alle API-Inputs validiert mit Zod (Frontend) + Pydantic (Backend)
- [ ] File-Uploads: Typ, Groesse, Inhalt validiert (nicht nur Extension)
- [ ] SQL: ORM oder parametrisierte Queries (NIEMALS String-Concatenation)
- [ ] Kein eval(), kein dangerouslySetInnerHTML ohne Sanitization
- [ ] Rate Limiting auf oeffentlichen Endpoints (Auth, API, Webhooks)
- [ ] Request-Size-Limits konfiguriert
- [ ] User-generierter Content escaped vor Rendering
- [ ] Redirect-URLs validiert (keine Open Redirects)

---

## 7. Dependency Security

### Findings

| Finding | Schwere | Gefunden in |
|---------|---------|-------------|
| Deprecated @supabase/auth-helpers-nextjs | HOCH | Saas-Kit-supabase |
| python-jose unmaintained | HOCH | scalable-rag-pipeline |
| Anthropic SDK 0.8.0 extrem veraltet | MITTEL | scalable-rag-pipeline |
| python-jose fehlt in requirements.txt | HOCH | intelligent-rag-service |
| TypeScript strict: false | HOCH | Saas-Kit-supabase |

### Checklist

- [ ] Keine deprecated Libraries (@supabase/auth-helpers, python-jose, vm2)
- [ ] Keine unmaintained Libraries (letztes Update >2 Jahre)
- [ ] Dependabot oder Renovate konfiguriert
- [ ] Lock Files committed (package-lock.json / pnpm-lock.yaml / poetry.lock)
- [ ] TypeScript strict: true
- [ ] Alle Dependencies in package.json/requirements.txt gelistet
- [ ] `npm audit` / `pip-audit` zeigt keine Critical/High Findings
- [ ] Keine bekannten CVEs in direkten Dependencies

---

## 8. DSGVO/GDPR Compliance

### Findings

| Finding | Schwere | Gefunden in |
|---------|---------|-------------|
| Vercel Analytics + Google Tag Manager eingebaut | MITTEL | supabase-nextjs-template |
| PostHog-Telemetrie standardmaessig aktiv | MITTEL | n8n |
| console.log ueberall (potentiell PII) | MITTEL | Saas-Kit-supabase |

### Checklist

- [ ] Cookie-Consent-Banner VOR jeglichem Tracking
- [ ] Analytics nur nach Consent geladen
- [ ] Kein PII in Logs (Namen, Emails, IPs) -- structlog/Pino, NICHT console.log
- [ ] Daten-Export-Endpoint fuer User (DSGVO Art. 20)
- [ ] Account-Loeschung-Endpoint (DSGVO Art. 17 -- Recht auf Vergessen)
- [ ] Privacy Policy und Terms of Service Seiten vorhanden
- [ ] Auftragsverarbeitungsvertrag mit allen Sub-Prozessoren
- [ ] Server-Standort dokumentiert (EU bevorzugt fuer EU-Kunden)
- [ ] Supabase-Projekt in EU-Region wenn EU-Kunden bedient werden
- [ ] Keine PII an Drittanbieter ohne Consent

---

## 9. Logging & Monitoring

### Findings

| Finding | Schwere | Gefunden in |
|---------|---------|-------------|
| console.log ueberall in Production | MITTEL | Saas-Kit-supabase |
| print() statt Logging-Framework | MITTEL | intelligent-rag-service |
| print() in API main.py | MITTEL | scalable-rag-pipeline |
| Observability definiert aber nicht aufgerufen | MITTEL | scalable-rag-pipeline |

### Checklist

- [ ] Kein console.log/print() in Production-Code
- [ ] Structured Logging (structlog fuer Python, Pino fuer Node.js)
- [ ] Kein PII in Log-Output
- [ ] Auth-Events geloggt (Login, Logout, Failed Attempts, Password Reset)
- [ ] Payment-Events geloggt (Subscription Changes, Webhook Failures)
- [ ] Error Tracking (Sentry) mit PII Scrubbing aktiviert
- [ ] Alerting fuer: Auth-Anomalien, Webhook-Failures, Subscription-Fehler
- [ ] Observability tatsaechlich eingebunden (nicht nur definiert)

---

## 10. Frontend Security

### Checklist

- [ ] Kein dangerouslySetInnerHTML ohne DOMPurify Sanitization
- [ ] Keine sensitiven Daten in localStorage (Tokens, PII)
- [ ] API Keys mit NEXT_PUBLIC_ Prefix sind wirklich public-safe
- [ ] STRIPE_SECRET_KEY hat KEINEN NEXT_PUBLIC_ Prefix
- [ ] Error Messages leaken keine internen Details
- [ ] Source Maps deaktiviert in Production
- [ ] Keine Credentials in Frontend-Bundles
- [ ] Image-Quellen via next/image mit allowedDomains

---

## 11. Infrastructure Security

### Checklist

- [ ] HTTPS everywhere (kein HTTP in Production)
- [ ] Environment-spezifische Konfiguration (dev/staging/prod)
- [ ] Kein Debug Mode in Production
- [ ] Datenbank-Verbindung verschluesselt (SSL)
- [ ] Backup-Strategie fuer Datenbank
- [ ] Incident Response Plan dokumentiert
- [ ] Deployment via CI/CD (kein manuelles Deployment)
- [ ] Keine Default-Credentials in Production

---

## 12. Multi-Tenancy Security (wenn zutreffend)

### Checklist

- [ ] Tenant-Isolation auf Datenbank-Ebene (RLS mit Org-ID)
- [ ] Kein Cross-Tenant Data Leakage
- [ ] Tenant-ID in jedem Query validiert
- [ ] Admin-Aktionen auf eigenen Tenant beschraenkt
- [ ] Invite-System validiert Email-Domain (wenn gewuenscht)
- [ ] Tenant-Wechsel invalidiert Cache

---

## Quick Audit Command

Fuer eine schnelle erste Einschaetzung:

```bash
# 1. Check for hardcoded secrets
grep -rn "sk_live\|sk_test\|whsec_\|secret.*=.*['\"]" --include="*.ts" --include="*.tsx" --include="*.py" src/ app/ api/

# 2. Check for console.log in production code
grep -rn "console\.log\|console\.error" --include="*.ts" --include="*.tsx" src/ app/ | grep -v "node_modules" | grep -v ".test."

# 3. Check for missing RLS
# In Supabase SQL Editor:
SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND NOT rowsecurity;

# 4. Check for deprecated packages
npm ls @supabase/auth-helpers-nextjs 2>/dev/null && echo "DEPRECATED: auth-helpers found"
pip list 2>/dev/null | grep python-jose && echo "DEPRECATED: python-jose found"

# 5. Check TypeScript strict mode
grep '"strict"' tsconfig.json

# 6. Check for type="text" on password fields
grep -rn 'type="text"' --include="*.tsx" src/ app/ | grep -i pass
```

---

## Output Format

Nach der Audit, fasse so zusammen:

```
## SaaS Security Audit

**Score:** X/100 (RATING)
**Datum:** YYYY-MM-DD

### Kritische Findings (sofort fixen)
1. [Finding + Repo-Referenz]
2. ...

### Hohe Findings (vor Production fixen)
1. [Finding]
2. ...

### Mittlere Findings (nach Launch fixen)
1. [Finding]
2. ...

### Positiv (bereits gut)
1. [Was bereits richtig gemacht wird]
2. ...

### Empfohlene Reihenfolge
1. [Wichtigstes Fix zuerst]
2. ...
```
