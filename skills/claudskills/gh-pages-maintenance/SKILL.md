---
name: gh-pages-maintenance
description: >
  Betrieb und Wartung von GitHub Pages Websites (primär Nuxt 4 SSG-Blogs).
  Verwende diesen Skill für: CI/CD-Workflow verstehen und debuggen; PR-Previews
  einrichten; Umgebungsvariablen und GitHub Secrets verwalten; statische Redirects
  (routeRules) konfigurieren; Google Analytics / AdSense integrieren; DSGVO-Consent
  einrichten; Nuxt Content v3 Schema anpassen; Renovate-PRs beurteilen;
  Blog-Posts und Seiten erstellen.
user-invocable: true
---

# GitHub Pages Sites – Betrieb & Wartung

Dieses Skill-Dokument gilt für statische Websites, die mit **Nuxt 4 SSG** (oder
vergleichbaren Generatoren) auf GitHub Pages deployt werden. Nuxt-spezifische
Abschnitte sind als solche gekennzeichnet.

---

## Typische Projektstruktur (Nuxt 4)

```
content/
  blog/          # Blog-Posts als *.md (Frontmatter: title, date, description, image, categories)
  pages/         # Statische Seiten als *.md (Frontmatter: title, description)
pages/
  index.vue      # Blog-Index (queryCollection('blog'))
  blog/
    [...slug].vue  # Blog-Post-Detail
  [slug].vue       # Statische Seiten
components/
  AdBlock.vue      # Google AdSense – isMounted-Guard gegen SSR-Mismatch
  ConsentBanner.vue # DSGVO-Banner – Cookie + useState('consent')
layouts/
  default.vue    # Header, Footer, ConsentBanner-Slot
app.vue          # <ClientOnly><ConsentBanner /></ClientOnly>
content.config.ts # @nuxt/content v3 Collections + Zod-Schemas
nuxt.config.ts   # Module, runtimeConfig, routeRules (Redirects), highlight langs
renovate.json    # Renovate-Bot-Konfiguration
```

---

## Umgebungsvariablen & Secrets

| Variable | Typ | Beschreibung |
|---|---|---|
| `GOOGLE_ANALYTICS_MEAS_ID` | GitHub Var (`vars.*`) | GA4 Measurement-ID (`G-XXXXXXXXXX`) |
| `GOOGLE_ADSENSE_PUB_ID` | GitHub Var (`vars.*`) | Publisher-ID ohne `ca-`-Präfix (`pub-XXXXXX`) |
| `STATIC_FORMS_KEY` | GitHub Secret (`secrets.*`) | API-Key für Kontaktformular-Dienst |

**Lokal**: `.env`-Datei anlegen (in `.gitignore` eintragen!):
```
GOOGLE_ANALYTICS_MEAS_ID=G-XXXXXXXXXX
GOOGLE_ADSENSE_PUB_ID=pub-XXXXXXXXXXXXXXXX
```

**Muster für Secrets im Build**: Secrets niemals direkt einchecken. Stattdessen
einen Platzhalter im Code verwenden und diesen per `sed` im CI-Schritt ersetzen:
```yaml
- name: Inject API key
  run: sed -i "s/YOUR_API_KEY_PLACEHOLDER/${{ secrets.MY_SECRET }}/g" src/contact.vue
```

---

## CI/CD-Workflow für GitHub Pages

### Standardstruktur (Nuxt / Node.js)

```yaml
name: Publish

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: npm
      - run: npm ci
      - run: npm run generate

      # Deploy-Artifact nur bei push auf main
      - uses: actions/upload-pages-artifact@v4
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        with:
          path: .output/public

      # PR-Preview als normales Artifact
      - uses: actions/upload-artifact@v4
        if: github.event_name == 'pull_request'
        with:
          name: pr-preview-${{ github.event.number }}
          path: .output/public
          retention-days: 7

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

### Aktuelle Actions-Versionen (Stand 2026-04-27)

| Action | Version |
|---|---|
| `actions/checkout` | v4 |
| `actions/setup-node` | v4 |
| `actions/upload-pages-artifact` | v4 |
| `actions/upload-artifact` | v4 |
| `actions/deploy-pages` | v4 |

> Renovate hält diese Versionen per `github-actions`-Manager aktuell.

---

## Google AdSense Integration (Nuxt)

AdSense-Slot-IDs sind öffentlich – sie werden in `nuxt.config.ts` via
`runtimeConfig.public` bereitgestellt, nicht als Secret:

```ts
// nuxt.config.ts
runtimeConfig: {
  public: {
    adsensePubId: process.env.GOOGLE_ADSENSE_PUB_ID || '',
    adsenseSlots: {
      left:      'SLOT_ID_LINKS',
      right:     'SLOT_ID_RECHTS',
      bottom:    'SLOT_ID_UNTEN',
      inArticle: 'SLOT_ID_IN_ARTICLE',
    },
  },
},
```

**SSR-Mismatch verhindern**: AdSense-Komponente nur client-seitig rendern:
```vue
<script setup>
const isMounted = ref(false)
onMounted(() => { isMounted.value = true })
</script>
<template>
  <div v-if="isMounted"><!-- AdSense-Code --></div>
</template>
```

---

## Statische Redirects (kein Server → routeRules)

GitHub Pages hat keine Server-seitige Redirect-Möglichkeit. Nuxt generiert
statische Meta-Refresh-Seiten aus `routeRules`:

```ts
// nuxt.config.ts
routeRules: {
  '/alter-pfad':  { redirect: '/neuer-pfad' },
  '/alter-pfad/': { redirect: '/neuer-pfad' },
}
```

**Immer mit und ohne trailing slash eintragen** – Browser senden beide Varianten.

---

## Custom Domain konfigurieren

### 1. CNAME-Datei im Repo anlegen

Die Datei muss im **Root des deploy-Verzeichnisses** landen (bei Nuxt: `public/CNAME`,
bei Jekyll/plain: `CNAME` im Repo-Root). Nuxt kopiert alles aus `public/` unverändert
in das Build-Output.

```bash
# Nuxt-Projekt
echo "www.meine-domain.de" > public/CNAME

# Plain-HTML / Jekyll
echo "www.meine-domain.de" > CNAME
```

Nur **eine** Domain eintragen (kein `https://`, keine trailing newline außer der
automatischen). GitHub überschreibt die Datei andernfalls beim nächsten Deploy nicht.

> **Alternativ**: Domain auch über **Settings → Pages → Custom domain** im
> GitHub-Webinterface eintragen – das legt die `CNAME`-Datei automatisch per Commit
> an. Trotzdem empfohlen, die Datei zusätzlich im Repo zu haben, damit sie bei
> Force-Pushes nicht verloren geht.

---

### 2. DNS-Records beim Domain-Anbieter setzen

#### Apex-Domain (`meine-domain.de` ohne www)

GitHub empfiehlt **beide** Record-Typen (A + AAAA) parallel, damit IPv4 und IPv6
funktionieren:

**A-Records (IPv4) – alle vier eintragen:**
```
@ A 185.199.108.153
@ A 185.199.109.153
@ A 185.199.110.153
@ A 185.199.111.153
```

**AAAA-Records (IPv6) – alle vier eintragen:**
```
@ AAAA 2606:50c0:8000::153
@ AAAA 2606:50c0:8001::153
@ AAAA 2606:50c0:8002::153
@ AAAA 2606:50c0:8003::153
```

#### Subdomain (`www.meine-domain.de`)

```
www CNAME <github-username>.github.io.
```

Für **Organisations-Repos** oder Repos mit anderem Namen:
```
www CNAME <github-username>.github.io.
```
(Das Ziel ist immer `<user>.github.io.`, nicht der Repo-Name – GitHub leitet
intern weiter.)

#### Apex + www gleichzeitig (empfohlen)

Beide Varianten konfigurieren und im GitHub-Settings die Apex-Domain eintragen.
GitHub leitet dann automatisch von `www` auf die Apex um (oder umgekehrt, je nach
Einstellung).

---

### 3. HTTPS / TLS erzwingen

Nachdem DNS propagiert ist (kann bis zu 24 h dauern):

1. **Settings → Pages → Custom domain** – die eingetragene Domain verifizieren.
2. Checkbox **"Enforce HTTPS"** aktivieren.
3. GitHub stellt automatisch ein Let's-Encrypt-Zertifikat aus.

**Troubleshooting**:
- `DNS check failed` → TTL abwarten; mit `dig meine-domain.de A` prüfen ob die GitHub-IPs ankommen.
- `Certificate still pending` → bis zu 1 h warten; dann Domain entfernen und neu eintragen.
- `CNAME file missing after deploy` → `public/CNAME` im Repo anlegen (nicht nur im GitHub-UI).

---

## Content erstellen (Nuxt Content v3)

### Neuer Blog-Post

Datei anlegen: `content/blog/<slug>.md`

```markdown
---
title: "Titel des Posts"
date: "2026-04-27"
description: "Kurzbeschreibung für SEO und Index-Karte"
image: "/uploads/bild.jpg"
categories:
  - Kategorie1
  - Kategorie2
---

Inhalt hier...
```

**Neue Frontmatter-Felder** immer im Zod-Schema in `content.config.ts` ergänzen,
sonst `no such column`-Fehler beim Build.

### Neue statische Seite

Datei anlegen: `content/pages/<slug>.md` → Route `/pages/<slug>`.

---

## Tailwind CSS – Versionsabsicherung

`@nuxtjs/tailwindcss` v6 hat `tailwindcss ~3.4` als **reguläre Dependency**
(nicht Peer-Dep). Auf v4 upgraden bricht den Build.

Renovate absichern:
```json
{
  "packageRules": [
    {
      "matchPackageNames": ["tailwindcss"],
      "allowedVersions": "^3.0.0"
    }
  ]
}
```

Entsperren sobald `@nuxtjs/tailwindcss` tailwindcss als `peerDependency` listet:
```bash
cat node_modules/@nuxtjs/tailwindcss/package.json | python3 -c \
  "import json,sys; p=json.load(sys.stdin); \
   print('dep:', p.get('dependencies',{}).get('tailwindcss','none')); \
   print('peer:', p.get('peerDependencies',{}).get('tailwindcss','none'))"
```

---

## Häufige Fehler & Fixes

| Fehler | Ursache | Fix |
|---|---|---|
| `no such column: "date"` | Frontmatter-Feld fehlt im Zod-Schema | Feld in `content.config.ts` ergänzen |
| `queryContent is not defined` | @nuxt/content v2 API-Call | Auf `queryCollection()` migrieren |
| `Hydration mismatch` | Cookie-/Client-abhängige Komponente SSR-seitig gerendert | In `<ClientOnly>` wrappen |
| CI hängt bei `better-sqlite3` | Paket fehlt in devDeps | `better-sqlite3` in `package.json` devDeps eintragen |
| Build bricht nach Renovate-PR | tailwindcss v4 installiert | `tailwindcss` auf `^3.4.17` zurücksetzen |
| Seite deployed, aber Redirect fehlt | trailing slash vergessen | Route mit und ohne `/` in `routeRules` eintragen |
| AdSense zeigt Leeraum in SSR | Komponente server-seitig gerendert | `isMounted`-Guard oder `<ClientOnly>` verwenden |
| `CNAME file missing` nach Deploy | `CNAME` nur im GitHub-UI, nicht im Repo | `public/CNAME` anlegen und committen |
| Custom Domain verloren nach Force-Push | `CNAME`-Datei nicht im Repo | `public/CNAME` mit Domain-Eintrag ins Repo aufnehmen |

---

## Lokale Entwicklung

```bash
npm run dev         # Dev-Server mit HMR
npm run generate    # Statischen Build erzeugen → .output/public/
npx serve .output/public   # Lokale Vorschau des fertigen Builds
```

---

## Commit-Checklist

- [ ] `npm run generate` läuft lokal ohne Fehler durch
- [ ] Neue Frontmatter-Felder in `content.config.ts` Zod-Schema eingetragen
- [ ] Neue Redirects mit **und** ohne trailing slash
- [ ] Keine Secrets oder `.env`-Inhalte eingecheckt
- [ ] API-Key-Platzhalter im Quellcode nicht durch echten Wert ersetzt
