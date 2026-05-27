---
name: inet-mail
description: >-
  Mailstandaarden getest door internet.nl: SPF (Sender Policy Framework),
  DKIM (DomainKeys Identified Mail), DMARC (Domain-based Message Authentication),
  STARTTLS, DANE (DNS-based Authentication of Named Entities).
  Triggers: mail test, DMARC, DKIM, SPF, STARTTLS, DANE,
  mailserver beveiliging, email security, e-mailbeveiliging,
  mailstandaarden, anti-spoofing
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

**Gebruik deze skill wanneer een gebruiker vraagt over mailstandaarden die internet.nl test,
zoals SPF, DKIM, DMARC, STARTTLS of DANE. Genereer correcte DNS-records en diagnostische
commando's. Verwijs naar `/inet-toolbox` voor stap-voor-stap implementatiegidsen.**

## Overzicht

[Internet.nl](https://internet.nl/test-mail/) test e-maildomeinen op de volgende standaarden.
Alle standaarden staan op de
[pas-toe-of-leg-uit-lijst](https://www.forumstandaardisatie.nl/open-standaarden)
van Forum Standaardisatie.

## De SPF + DKIM + DMARC keten

Deze drie standaarden werken samen om e-mailspoofing tegen te gaan:

1. **SPF** - Welke servers mogen mail versturen namens jouw domein?
2. **DKIM** - Is de e-mail onderweg niet gewijzigd? (digitale handtekening)
3. **DMARC** - Wat moet de ontvanger doen als SPF of DKIM faalt? (beleid + rapportage)

```
Afzender -> SPF controle (IP-adres) ----+
         -> DKIM controle (handtekening) +-> DMARC beleid -> leveren / weigeren / quarantaine
                                              |
                                              +-> Rapportage naar domeineigenaar
```

## Standaarden

### 1. SPF (Sender Policy Framework)

**Wat:** Een DNS TXT-record dat specificeert welke mailservers e-mail mogen versturen
namens een domein.

**Wat test internet.nl:**
- SPF-record aanwezig als DNS TXT-record
- Correcte syntax
- Maximaal 10 DNS-lookups (include, a, mx, redirect)
- Eindigt op `-all` (fail) of `~all` (softfail)

**DNS-record formaat:**

```dns
example.nl. IN TXT "v=spf1 mx a:mail.example.nl ip4:192.0.2.0/24 ip6:2001:db8::/32 include:_spf.google.com -all"
```

**Mechanismen:**

| Mechanisme | Betekenis |
|-----------|-----------|
| `mx` | MX-records van het domein zijn geautoriseerd |
| `a` | A/AAAA-record van het domein is geautoriseerd |
| `a:host` | A/AAAA van specifieke host |
| `ip4:range` | IPv4-adres of -bereik |
| `ip6:range` | IPv6-adres of -bereik |
| `include:domein` | Neem SPF-beleid van ander domein over |
| `redirect=domein` | Gebruik SPF-record van ander domein |

**Qualifiers:**

| Qualifier | Betekenis | Aanbevolen |
|-----------|-----------|------------|
| `+` (default) | Pass | Impliciet; gebruik `-all` als eindregel |
| `-` | Fail (hard) | Ja, als eindregel (`-all`) |
| `~` | Softfail | Acceptabel |
| `?` | Neutral | Nee |

**Testen:**

```bash
# SPF-record opvragen
dig TXT example.nl +short | grep "v=spf1"

# SPF-validatie simuleren (aantal lookups tellen)
dig TXT example.nl +short
# Tel elke include, a, mx, redirect als 1 lookup (max 10)
```

### 2. DKIM (DomainKeys Identified Mail)

**Wat:** Een mechanisme dat e-mail voorziet van een cryptografische handtekening
via een DNS-publicsleutel. De ontvangende mailserver verifieert de handtekening.

**Wat test internet.nl:**
- Minimaal 1 geldige DKIM-handtekening op testmail
- Publieke sleutel beschikbaar via DNS

> **Let op:** Internet.nl controleert alleen of een DKIM-record bestaat; de sleutellengte
> wordt niet getest. Best practice is minimaal 2048-bit RSA.

**DNS-record formaat:**

```dns
selector._domainkey.example.nl. IN TXT "v=DKIM1; k=rsa; p=MIIBIjANBgkqhki..."
```

**Selector:** Een naam die de verzendende server meestuurt in de DKIM-Signature header
(bijv. `google`, `selector1`, `default`). Hiermee kan de ontvanger de juiste publieke
sleutel vinden in DNS.

**Sleutel genereren:**

```bash
# RSA 2048-bit sleutelpaar genereren
openssl genrsa -out dkim_private.pem 2048
openssl rsa -in dkim_private.pem -pubout -out dkim_public.pem

# Publieke sleutel voor DNS (zonder headers, op 1 regel)
openssl rsa -in dkim_private.pem -pubout -outform DER | base64 -w0
```

**Testen:**

```bash
# DKIM-sleutel opvragen (vervang 'selector' door de echte selector)
dig TXT selector._domainkey.example.nl +short

# Veelgebruikte selectors proberen
for sel in google default selector1 selector2 dkim mail; do
  echo "=== $sel ==="
  dig TXT "${sel}._domainkey.example.nl" +short
done
```

### 3. DMARC (Domain-based Message Authentication, Reporting and Conformance)

**Wat:** Een DNS TXT-record dat aangeeft wat ontvangers moeten doen als SPF en/of
DKIM niet slagen, en waar rapportages naartoe moeten.

**Wat test internet.nl:**
- DMARC-record aanwezig op `_dmarc.example.nl`
- Beleid is `quarantine` of `reject` (niet `none` voor productie)
- Rapportage-adres geconfigureerd (rua)

> **Implementatiepad:** Start met `p=none` om rapportages te verzamelen, schakel
> daarna over naar `quarantine` en uiteindelijk `reject`. Internet.nl scoort
> alleen `quarantine` of `reject` als voldoende.

**DNS-record formaat:**

```dns
_dmarc.example.nl. IN TXT "v=DMARC1; p=reject; rua=mailto:dmarc-reports@example.nl; ruf=mailto:dmarc-forensic@example.nl; adkim=s; aspf=s; pct=100"
```

**Parameters:**

| Tag | Betekenis | Waarden |
|-----|-----------|---------|
| `p` | Beleid | `none` / `quarantine` / `reject` |
| `sp` | Beleid voor subdomeinen | `none` / `quarantine` / `reject` |
| `rua` | Aggregaat rapportage-adres | `mailto:adres@example.nl` |
| `ruf` | Forensisch rapportage-adres | `mailto:adres@example.nl` |
| `adkim` | DKIM alignment | `r` (relaxed) / `s` (strict) |
| `aspf` | SPF alignment | `r` (relaxed) / `s` (strict) |
| `pct` | Percentage berichten waarop beleid wordt toegepast | 0-100 |

**Gefaseerde uitrol:**

```dns
; Fase 1: Monitor (alleen rapportage, geen actie)
_dmarc.example.nl. IN TXT "v=DMARC1; p=none; rua=mailto:dmarc@example.nl"

; Fase 2: Quarantine op 10% (test impact)
_dmarc.example.nl. IN TXT "v=DMARC1; p=quarantine; pct=10; rua=mailto:dmarc@example.nl"

; Fase 3: Quarantine op 100%
_dmarc.example.nl. IN TXT "v=DMARC1; p=quarantine; pct=100; rua=mailto:dmarc@example.nl"

; Fase 4: Reject (volledige bescherming)
_dmarc.example.nl. IN TXT "v=DMARC1; p=reject; rua=mailto:dmarc@example.nl; adkim=s; aspf=s"
```

**Testen:**

```bash
# DMARC-record opvragen
dig TXT _dmarc.example.nl +short
```

### 4. STARTTLS

**Wat:** STARTTLS versleutelt SMTP-verkeer tussen mailservers.

**Wat test internet.nl:**
- MX-servers ondersteunen STARTTLS
- TLS 1.2 of hoger (TLS 1.0/1.1 geeft een phase-out waarschuwing; SSL 2.0/3.0 is een harde fout)
- Geldig certificaat
- Geen terugval naar onversleuteld verkeer

**Testen:**

```bash
# MX-records opvragen
dig MX example.nl +short

# STARTTLS testen op MX-server
openssl s_client -connect mx.example.nl:25 -starttls smtp </dev/null 2>/dev/null | \
  grep -E '(Protocol|Cipher|Verify)'
```

### 5. DANE (DNS-based Authentication of Named Entities)

**Wat:** DANE koppelt TLS-certificaten aan DNS via TLSA-records,
beveiligd met DNSSEC. Hiermee wordt de vertrouwensketen versterkt:
niet alleen CA's, maar ook DNS verifieert het certificaat.

**Vereist:** DNSSEC moet actief zijn op het domein.

**Wat test internet.nl:**
- TLSA-records aanwezig voor MX-servers
- Correcte TLSA-parameters
- DNSSEC op het MX-domein

**DNS-record formaat:**

```dns
_25._tcp.mx.example.nl. IN TLSA 3 1 1 <sha256-hash-van-publieke-sleutel>
```

**TLSA-parameters:**

| Veld | Waarde | Betekenis |
|------|--------|-----------|
| Certificate Usage | `3` | DANE-EE (End Entity, aanbevolen voor mail) |
| Selector | `1` | SubjectPublicKeyInfo (publieke sleutel) |
| Matching Type | `1` | SHA-256 hash |

**TLSA-hash genereren:**

```bash
# Hash van het certificaat van de mailserver
openssl s_client -connect mx.example.nl:25 -starttls smtp </dev/null 2>/dev/null | \
  openssl x509 -pubkey -noout | \
  openssl pkey -pubin -outform DER | \
  openssl dgst -sha256 -binary | xxd -p -c 32
```

**Testen:**

```bash
# TLSA-record opvragen
dig TLSA _25._tcp.mx.example.nl +short

# Controleer DNSSEC op MX-domein
dig MX example.nl +dnssec +short
```

## Repositories

| Repository | Beschrijving | Licentie |
|-----------|-------------|--------|
| [Internet.nl](https://github.com/internetstandards/Internet.nl) | Testsuite broncode | [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) (code), [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en) (vertalingen) |
| [toolbox-wiki](https://github.com/internetstandards/toolbox-wiki) | Implementatiegidsen | [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en) |

## Veelvoorkomende problemen

| Probleem | Oorzaak | Oplossing |
|----------|---------|-----------|
| SPF `permerror` | Meer dan 10 DNS-lookups | Verminder `include`-verwijzingen, gebruik `ip4`/`ip6` direct |
| DKIM-verificatie faalt | Verkeerde selector of verlopen sleutel | Controleer selector in e-mailheaders, vergelijk met DNS |
| DMARC `p=none` is onvoldoende | Fase 1 monitoring nog actief | Verschuif naar `p=quarantine` of `p=reject` |
| STARTTLS niet aangeboden | Mailserver niet geconfigureerd | Schakel TLS in op de mailserver |
| DANE TLSA mismatch | Certificaat vernieuwd zonder TLSA-update | Werk TLSA-record bij met hash van nieuw certificaat |

## Achtergrondinfo

Zie [reference.md](./reference.md) voor server-specifieke configuratie (Postfix, Exchange),
key rotation-procedures en DMARC-rapportage-analyse.

