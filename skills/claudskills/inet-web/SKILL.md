---
name: inet-web
description: >-
  Webstandaarden getest door internet.nl: HTTPS, TLS 1.2/1.3, HSTS,
  DNSSEC voor websites, IPv6 dual-stack, RPKI route origin validation,
  security headers (CSP, X-Frame-Options, X-Content-Type-Options,
  Referrer-Policy), security.txt (RFC 9116).
  Triggers: web test, HTTPS, TLS, HSTS, DNSSEC website,
  security headers, security.txt, IPv6, RPKI, webstandaarden,
  website testen, Content-Security-Policy
model: sonnet
allowed-tools:
  - Bash(gh api *)
  - Bash(curl -s *)
  - Bash(dig *)
  - Bash(openssl *)
  - WebFetch(*)
metadata:
  created-with-ai: "true"
  created-with-model: claude-opus-4-20250514
  created-date: "2025-02-22"
  status: concept
---

> **CONCEPT — Let op:** Deze skill is geen officieel product van internet.nl. De beschrijvingen zijn informatieve samenvattingen — niet de officiële standaarden zelf. De testcriteria op [internet.nl](https://internet.nl) en de definities op [forumstandaardisatie.nl](https://www.forumstandaardisatie.nl/open-standaarden) zijn altijd leidend. Overheidsorganisaties die generatieve AI inzetten dienen te voldoen aan het [Overheidsbreed standpunt voor de inzet van generatieve AI](https://open.overheid.nl/documenten/bc03ce31-0cf1-4946-9c94-e934a62ebe73/file). Zie onze [verantwoording](https://github.com/developer-overheid-nl/skills-marketplace/blob/main/docs/verantwoording.md) en [DISCLAIMER.md](../../DISCLAIMER.md).

**Gebruik deze skill wanneer een gebruiker vraagt over webstandaarden die internet.nl test,
zoals HTTPS/TLS, DNSSEC, IPv6, RPKI, security headers of security.txt. Genereer
standaard-conforme configuratie en diagnostische commando's.**

## Overzicht

[Internet.nl](https://internet.nl/test-site/) test websites op de volgende standaarden.
Alle standaarden staan op de
[pas-toe-of-leg-uit-lijst](https://www.forumstandaardisatie.nl/open-standaarden)
van Forum Standaardisatie.

## Standaarden

### 1. IPv6

**Wat:** Internetprotocol versie 6 met 128-bit adressen. Websites moeten bereikbaar
zijn via zowel IPv4 als IPv6 (dual-stack).

**Waarom verplicht:** IPv4-adressen raken op. De overheid moet vooroplopen in de
transitie naar IPv6. Staat op de pas-toe-of-leg-uit-lijst.

**Wat test internet.nl:**
- AAAA-record aanwezig voor het domein
- Webserver bereikbaar via IPv6
- Nameservers bereikbaar via IPv6

**Testen:**

```bash
# AAAA-record opvragen
dig AAAA example.nl +short

# Nameserver IPv6 controleren
dig NS example.nl +short | while read ns; do dig AAAA "$ns" +short; done

# Bereikbaarheid testen
curl -6 -sI https://example.nl | head -5
```

### 2. DNSSEC

**Wat:** DNS Security Extensions beveiligt DNS-antwoorden met cryptografische
handtekeningen zodat manipulatie (DNS spoofing) detecteerbaar is.

**Waarom verplicht:** Zonder DNSSEC kan een aanvaller DNS-antwoorden vervalsen
en gebruikers naar een frauduleuze site leiden.

**Wat test internet.nl:**
- Zone is gesigneerd
- DS-record aanwezig bij de registrar
- Geldige RRSIG-handtekeningen
- Correcte ketenvalidatie (trust chain)

**Testen:**

```bash
# DNSSEC-validatie controleren
dig example.nl +dnssec +short

# DS-record opvragen bij de parent zone
dig DS example.nl +short

# Volledige validatieketen
dig example.nl +trace +dnssec | grep -E '(RRSIG|DS|DNSKEY)'
```

### 3. HTTPS / TLS

**Wat:** TLS (Transport Layer Security) versleutelt het verkeer tussen browser en
server. Internet.nl vereist TLS 1.2 of 1.3 met sterke cipher suites.

**Waarom verplicht:** Beschermt vertrouwelijkheid en integriteit van communicatie.
Zie ook de [NCSC TLS Security Guidelines (2025-05)](https://www.ncsc.nl/en/transport-layer-security/ICT-beveiligingsrichtlijnen-voor-TLS).

**Wat test internet.nl:**
- HTTPS bereikbaar en redirect van HTTP naar HTTPS
- TLS 1.2 of hoger (TLS 1.0/1.1 geeft een phase-out waarschuwing; SSL 2.0/3.0 is een harde fout)
- Sterke cipher suites (geen RC4, 3DES, NULL, export ciphers)
- Geldig certificaat (keten, geldigheid, hostnaam)
- OCSP stapling (getest als niet-scorende melding)

**Testen:**

```bash
# TLS-versie en cipher suite controleren
openssl s_client -connect example.nl:443 -tls1_3 </dev/null 2>/dev/null | \
  grep -E '(Protocol|Cipher|Verify)'

# Controleer dat TLS 1.0/1.1 niet werkt
openssl s_client -connect example.nl:443 -tls1 </dev/null 2>&1 | grep -i error

# Certificaatdetails
openssl s_client -connect example.nl:443 </dev/null 2>/dev/null | \
  openssl x509 -noout -subject -issuer -dates

# OCSP stapling
openssl s_client -connect example.nl:443 -status </dev/null 2>/dev/null | \
  grep -A5 "OCSP Response"
```

**Nginx-configuratie:**

```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    ssl_certificate /etc/letsencrypt/live/example.nl/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.nl/privkey.pem;

    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/example.nl/chain.pem;
}

# HTTP -> HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name example.nl;
    return 301 https://$host$request_uri;
}
```

**Apache-configuratie:**

```apache
<VirtualHost *:443>
    SSLEngine on
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
    SSLHonorCipherOrder off

    SSLCertificateFile /etc/letsencrypt/live/example.nl/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/example.nl/privkey.pem

    SSLUseStapling on
</VirtualHost>

SSLStaplingCache shmcb:/var/run/ocsp(128000)

<VirtualHost *:80>
    Redirect permanent / https://example.nl/
</VirtualHost>
```

### 4. HSTS

**Wat:** HTTP Strict Transport Security dwingt browsers om alleen HTTPS te gebruiken
via een response header.

**Wat test internet.nl:**
- `Strict-Transport-Security` header aanwezig
- `max-age` minimaal 31536000 (1 jaar)

**Testen:**

```bash
# HSTS-header controleren
curl -sI https://example.nl | grep -i strict-transport
```

**Configuratie (Nginx):**

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

**Configuratie (Apache):**

```apache
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
```

### 5. Security headers

**Wat:** HTTP response headers die browsers instrueren hoe om te gaan met content,
framing en referrer-informatie.

**Wat test internet.nl:**
- `Content-Security-Policy` (CSP)
- `X-Frame-Options`
- `X-Content-Type-Options`
- `Referrer-Policy`

**Testen:**

```bash
# Alle security headers controleren
curl -sI https://example.nl | grep -iE '(content-security|x-frame|x-content-type|referrer-policy|strict-transport)'
```

**Configuratie (Nginx):**

```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; frame-ancestors 'none'" always;
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

**Configuratie (Apache):**

```apache
Header always set Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; frame-ancestors 'none'"
Header always set X-Frame-Options "DENY"
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
```

### 6. security.txt

**Wat:** Een gestandaardiseerd bestand (RFC 9116) op `/.well-known/security.txt`
waarmee beveiligingsonderzoekers weten hoe ze kwetsbaarheden kunnen melden.

**Waarom verplicht:** Staat op de pas-toe-of-leg-uit-lijst. De overheid moet een
Coordinated Vulnerability Disclosure (CVD) beleid hebben.

**Wat test internet.nl:**
- Bestand bereikbaar op `/.well-known/security.txt`
- Verplichte velden: `Contact`, `Expires`
- Digitaal ondertekend (PGP) is aanbevolen

**Testen:**

```bash
# security.txt ophalen
curl -s https://example.nl/.well-known/security.txt
```

**Voorbeeldbestand:**

```text
Contact: https://example.nl/security
Contact: mailto:security@example.nl
Expires: 2027-01-01T00:00:00.000Z
Preferred-Languages: nl, en
Canonical: https://example.nl/.well-known/security.txt
Policy: https://example.nl/responsible-disclosure
```

### 7. RPKI

**Wat:** Resource Public Key Infrastructure maakt Route Origin Validation (ROV)
mogelijk. Hiermee wordt gecontroleerd of BGP-aankondigingen legitiem zijn via
Route Origin Authorisations (ROA's).

**Waarom verplicht:** Beschermt tegen BGP-hijacking waarbij verkeer via een
kwaadwillende partij wordt omgeleid.

**Wat test internet.nl:**
- ROA-record aanwezig voor het IP-adres van de webserver
- ROA is geldig (valid, niet invalid of unknown)

**Testen:**

```bash
# IP-adres opvragen en RPKI-status controleren
ip=$(dig A example.nl +short | head -1)
curl -s "https://stat.ripe.net/data/rpki-validation/data.json?resource=${ip}" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['status'])"
```

> RPKI/ROA wordt geconfigureerd bij je hostingpartij of IP-toewijzer (RIPE NCC).
> Neem contact op met je hoster om een ROA aan te maken.

## Repositories

| Repository | Beschrijving | Licentie |
|-----------|-------------|--------|
| [Internet.nl](https://github.com/internetstandards/Internet.nl) | Testsuite broncode (Python/Django) | [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) (code), [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en) (vertalingen) |
| [toolbox-wiki](https://github.com/internetstandards/toolbox-wiki) | Implementatiegidsen per standaard | [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en) |

## Veelvoorkomende problemen

| Probleem | Oorzaak | Oplossing |
|----------|---------|-----------|
| TLS 1.0/1.1 nog actief | Oude serversoftware of configuratie | Schakel TLS 1.0/1.1 expliciet uit (geeft phase-out waarschuwing bij internet.nl) |
| Geen HSTS-header | Header niet geconfigureerd of overschreven | Voeg `Strict-Transport-Security` header toe met `always` directive |
| CSP blokkeert content | Te strikt beleid | Begin met `Content-Security-Policy-Report-Only` en verfijn |
| DNSSEC-validatie faalt | DS-record niet bijgewerkt na key rollover | Controleer DS bij registrar, vergelijk met DNSKEY |
| Geen AAAA-record | Server of DNS heeft geen IPv6 | Configureer IPv6 op server, voeg AAAA-record toe |
| security.txt verlopen | `Expires`-datum verstreken | Werk het bestand bij met een nieuwe datum (max 1 jaar vooruit) |
| RPKI invalid | ROA komt niet overeen met BGP-aankondiging | Controleer ROA bij je hoster, pas prefix/ASN aan |

## Achtergrondinfo

Zie [reference.md](./reference.md) voor uitgebreide protocol-details, server-specifieke
configuraties en verwijzingen naar NCSC-factsheets.

