---
name: inet-toolbox
description: >-
  Stap-voor-stap implementatiegidsen uit de internet.nl toolbox-wiki.
  Configuratie van DNSSEC, HTTPS/TLS, DMARC, DKIM, SPF, DANE en IPv6
  op veelgebruikte platformen (BIND, NSD, Nginx, Apache, Postfix).
  Triggers: internet.nl toolbox, DMARC configuratie, DKIM instellen,
  SPF record, DANE opzetten, implementatiegids, DNSSEC instellen,
  Let's Encrypt, certificaat, mailserver configureren
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

**Gebruik deze skill wanneer een gebruiker vraagt hoe een specifieke internetstandaard
stap-voor-stap geimplementeerd moet worden. Genereer werkende configuratie voor het
gevraagde platform. Raadpleeg de toolbox-wiki voor de meest actuele instructies.**

## Overzicht

De [toolbox-wiki](https://github.com/internetstandards/toolbox-wiki) bevat
implementatiegidsen voor alle standaarden die [internet.nl](https://internet.nl) test.
De gidsen zijn geschreven voor veelgebruikte platformen en DNS-providers.

## Toolbox-wiki verkennen

```bash
# Alle bestanden in de toolbox-wiki
gh api repos/internetstandards/toolbox-wiki/git/trees/main?recursive=1 \
  --jq '.tree[] | select(.type=="blob") | .path'

# Specifieke gids ophalen (bijv. DNSSEC)
gh api repos/internetstandards/toolbox-wiki/contents/DNSSEC.md \
  --jq '.content' | base64 -d
```

## Implementatiegidsen

### 1. DNSSEC instellen

DNSSEC beveiligt DNS-antwoorden met cryptografische handtekeningen.

#### BIND 9

```bash
# Stap 1: Zone signing inschakelen
# In named.conf:
zone "example.nl" {
    type master;
    file "/var/lib/bind/example.nl.zone";
    key-directory "/var/lib/bind/keys";
    auto-dnssec maintain;
    inline-signing yes;
};

# Stap 2: Sleutels genereren
cd /var/lib/bind/keys

# KSK (Key Signing Key)
dnssec-keygen -a ECDSAP256SHA256 -f KSK example.nl

# ZSK (Zone Signing Key)
dnssec-keygen -a ECDSAP256SHA256 example.nl

# Stap 3: BIND herladen
rndc reload example.nl

# Stap 4: DS-record publiceren bij registrar
# Haal het DS-record op:
dig DNSKEY example.nl @localhost | dnssec-dsfromkey -f - example.nl
# Voer dit DS-record in bij je domeinregistrar
```

#### NSD

```bash
# NSD gebruikt externe tools voor DNSSEC (bijv. ldns of OpenDNSSEC)

# Met ldns-signzone:
# Stap 1: Sleutels genereren
ldns-keygen -a ECDSAP256SHA256 -k example.nl  # KSK
ldns-keygen -a ECDSAP256SHA256 example.nl      # ZSK

# Stap 2: Zone ondertekenen
ldns-signzone -n example.nl.zone Kexample.nl.+013+*.private

# Stap 3: NSD configureren met gesigneerde zone
# In nsd.conf:
zone:
    name: "example.nl"
    zonefile: "example.nl.zone.signed"

# Stap 4: NSD herladen
nsd-control reload
```

#### Verificatie

```bash
# Controleer of DNSSEC correct is ingesteld
dig DNSKEY example.nl +short +multi
dig DS example.nl +short
dig example.nl +dnssec +short

# Valideer de keten
dig @9.9.9.9 example.nl +dnssec
```

### 2. HTTPS/TLS configureren

#### Let's Encrypt certificaat verkrijgen

```bash
# Certbot installeren (Ubuntu/Debian)
apt install certbot

# Certificaat aanvragen (standalone)
certbot certonly --standalone -d example.nl -d www.example.nl

# Certificaat aanvragen (met Nginx)
certbot --nginx -d example.nl -d www.example.nl

# Certificaat aanvragen (met Apache)
certbot --apache -d example.nl -d www.example.nl

# Automatische vernieuwing testen
certbot renew --dry-run
```

#### Nginx HTTPS-configuratie

```nginx
# /etc/nginx/sites-available/example.nl
server {
    listen 80;
    listen [::]:80;
    server_name example.nl www.example.nl;
    return 301 https://example.nl$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.nl www.example.nl;

    # Certificaten
    ssl_certificate /etc/letsencrypt/live/example.nl/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.nl/privkey.pem;

    # TLS configuratie (NCSC-conform)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/example.nl/chain.pem;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'" always;

    root /var/www/example.nl;
    index index.html;
}
```

#### Apache HTTPS-configuratie

```apache
# /etc/apache2/sites-available/example.nl.conf
<VirtualHost *:80>
    ServerName example.nl
    ServerAlias www.example.nl
    Redirect permanent / https://example.nl/
</VirtualHost>

<VirtualHost *:443>
    ServerName example.nl
    ServerAlias www.example.nl

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/example.nl/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/example.nl/privkey.pem

    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
    SSLHonorCipherOrder off

    SSLUseStapling on

    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    Header always set Content-Security-Policy "default-src 'self'"

    DocumentRoot /var/www/example.nl
</VirtualHost>

SSLStaplingCache shmcb:/var/run/ocsp(128000)
```

### 3. DMARC gefaseerd uitrollen

```bash
# Fase 1: Monitor - verzamel rapportages zonder impact op mailbezorging
# DNS-record aanmaken:
# _dmarc.example.nl. IN TXT "v=DMARC1; p=none; rua=mailto:dmarc@example.nl"

# Wacht 2-4 weken en analyseer de rapporten

# Fase 2: Quarantine op klein percentage
# _dmarc.example.nl. IN TXT "v=DMARC1; p=quarantine; pct=10; rua=mailto:dmarc@example.nl"

# Verhoog geleidelijk: pct=25, pct=50, pct=100

# Fase 3: Reject
# _dmarc.example.nl. IN TXT "v=DMARC1; p=reject; rua=mailto:dmarc@example.nl; adkim=s; aspf=s"
```

**Controleren:**

```bash
# DMARC-record opvragen
dig TXT _dmarc.example.nl +short
```

### 4. DKIM instellen

#### Sleutel genereren en publiceren

```bash
# RSA 2048-bit sleutelpaar genereren
openssl genrsa -out /etc/dkim/example.nl.private 2048
openssl rsa -in /etc/dkim/example.nl.private -pubout -outform DER | base64 -w0

# DNS TXT-record aanmaken met de publieke sleutel:
# selector202602._domainkey.example.nl. IN TXT "v=DKIM1; k=rsa; p=MIIBIjANBgkqhki..."
```

#### Postfix met OpenDKIM

```bash
# OpenDKIM installeren
apt install opendkim opendkim-tools

# Sleutel genereren
opendkim-genkey -b 2048 -d example.nl -D /etc/opendkim/keys/ -s selector202602

# Configuratie: zie /inet-mail reference.md voor volledige config

# Postfix koppelen
# In /etc/postfix/main.cf:
# milter_default_action = accept
# milter_protocol = 6
# smtpd_milters = inet:localhost:8891
# non_smtpd_milters = inet:localhost:8891

# Services herstarten
systemctl restart opendkim
systemctl restart postfix
```

**Controleren:**

```bash
# DKIM-sleutel in DNS controleren
dig TXT selector202602._domainkey.example.nl +short
```

### 5. SPF-record samenstellen

```bash
# Basis SPF-record
# example.nl. IN TXT "v=spf1 mx -all"

# Met specifieke mailprovider
# example.nl. IN TXT "v=spf1 mx include:_spf.google.com -all"
# example.nl. IN TXT "v=spf1 mx include:spf.protection.outlook.com -all"

# Met eigen mailservers
# example.nl. IN TXT "v=spf1 mx a:mail.example.nl ip4:192.0.2.0/24 ip6:2001:db8::/32 -all"
```

**Vuistregels:**
- Maximaal 10 DNS-lookups (elke `include`, `a`, `mx`, `redirect` telt als 1)
- Gebruik `ip4`/`ip6` om lookups te besparen
- Eindig altijd met `-all` (fail) of `~all` (softfail)
- Gebruik `include` voor externe mailproviders

**DNS-lookups tellen:**

```bash
# SPF-record opvragen en includes volgen
dig TXT example.nl +short | grep "v=spf1"

# Elke include is 1 lookup, volg ze recursief
dig TXT _spf.google.com +short
```

### 6. DANE instellen

**Vereisten:** DNSSEC moet actief zijn op het MX-domein.

```bash
# Stap 1: Controleer DNSSEC
dig MX example.nl +dnssec +short

# Stap 2: TLSA-hash genereren van het mailserver-certificaat
openssl s_client -connect mx.example.nl:25 -starttls smtp </dev/null 2>/dev/null | \
  openssl x509 -pubkey -noout | \
  openssl pkey -pubin -outform DER | \
  openssl dgst -sha256 -binary | xxd -p -c 32

# Stap 3: TLSA DNS-record aanmaken
# _25._tcp.mx.example.nl. IN TLSA 3 1 1 <hash-uit-stap-2>

# Stap 4: Controleren
dig TLSA _25._tcp.mx.example.nl +short
```

**Bij certificaatvernieuwing:**
- Als je dezelfde privesleutel hergebruikt: TLSA hoeft niet te veranderen
- Als je een nieuwe sleutel genereert: update het TLSA-record VOOR de vernieuwing

### 7. IPv6 inschakelen

#### DNS-records

```dns
; AAAA-records toevoegen naast bestaande A-records
example.nl.     IN  A     192.0.2.1
example.nl.     IN  AAAA  2001:db8::1
www.example.nl. IN  A     192.0.2.1
www.example.nl. IN  AAAA  2001:db8::1

; Nameservers
ns1.example.nl. IN  A     192.0.2.10
ns1.example.nl. IN  AAAA  2001:db8::10

; Mailservers
mx.example.nl.  IN  A     192.0.2.20
mx.example.nl.  IN  AAAA  2001:db8::20
```

#### Webserver

```nginx
# Nginx luistert standaard op IPv4+IPv6 als je [::] toevoegt
server {
    listen 80;
    listen [::]:80;
    listen 443 ssl;
    listen [::]:443 ssl;
}
```

#### Verificatie

```bash
# AAAA-records controleren
dig AAAA example.nl +short

# IPv6-bereikbaarheid testen
curl -6 -sI https://example.nl | head -5
ping6 example.nl
```

## Repositories

| Repository | Beschrijving | Licentie |
|-----------|-------------|--------|
| [toolbox-wiki](https://github.com/internetstandards/toolbox-wiki) | Implementatiegidsen (bronmateriaal) | [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en) |
| [Internet.nl](https://github.com/internetstandards/Internet.nl) | Testsuite om resultaat te controleren | [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) (code), [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en) (vertalingen) |

## Veelvoorkomende problemen

| Probleem | Oorzaak | Oplossing |
|----------|---------|-----------|
| Let's Encrypt verificatie faalt | Poort 80 niet bereikbaar of DNS niet correct | Controleer firewall en DNS-records |
| DNSSEC-validatie faalt na key rollover | DS bij registrar niet bijgewerkt | Publiceer nieuw DS-record bij registrar |
| DKIM-header niet aanwezig in mail | OpenDKIM draait niet of milter niet gekoppeld | Controleer `systemctl status opendkim` en Postfix milter-config |
| SPF permerror | Meer dan 10 DNS-lookups | Vervang `include` door `ip4`/`ip6` waar mogelijk |
| DANE TLSA mismatch na certificaatvernieuwing | TLSA-record niet bijgewerkt | Gebruik SPKI (selector=1) en hergebruik privesleutel, of update TLSA vooraf |
| IPv6 niet bereikbaar | Firewall blokkeert IPv6 of geen IPv6-adres | Controleer `ip -6 addr` en firewall-regels (ip6tables/nftables) |

## Achtergrondinfo

Zie [reference.md](./reference.md) voor links naar specifieke toolbox-wiki pagina's
en geavanceerde configuraties.

