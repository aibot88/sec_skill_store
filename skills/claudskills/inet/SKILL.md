---
name: inet
description: >-
  Overzicht van alle internetstandaarden die internet.nl test.
  Routing naar sub-skills voor web, mail, API en toolbox.
  Triggers: internet.nl, internet standaarden, website compliance,
  mail compliance, internetstandaarden, open standaarden,
  Forum Standaardisatie, pas-toe-of-leg-uit
model: sonnet
allowed-tools:
  - Bash(gh api *)
  - Bash(curl -s *)
  - WebFetch(*)
metadata:
  created-with-ai: "true"
  created-with-model: claude-opus-4-20250514
  created-date: "2025-02-22"
  status: concept
---

> **CONCEPT — Let op:** Deze skill is geen officieel product van internet.nl. De beschrijvingen zijn informatieve samenvattingen — niet de officiële standaarden zelf. De testcriteria op [internet.nl](https://internet.nl) en de definities op [forumstandaardisatie.nl](https://www.forumstandaardisatie.nl/open-standaarden) zijn altijd leidend. Overheidsorganisaties die generatieve AI inzetten dienen te voldoen aan het [Overheidsbreed standpunt voor de inzet van generatieve AI](https://open.overheid.nl/documenten/bc03ce31-0cf1-4946-9c94-e934a62ebe73/file). Zie onze [verantwoording](https://github.com/developer-overheid-nl/skills-marketplace/blob/main/docs/verantwoording.md) en [DISCLAIMER.md](../../DISCLAIMER.md).

**Gebruik deze skill wanneer een gebruiker vraagt naar een overzicht van internetstandaarden,
naar de internet.nl testsuite in het algemeen, of wanneer niet duidelijk is welke sub-skill
van toepassing is. Routeer door naar de juiste sub-skill zodra het domein helder is.**

## Wat is internet.nl?

[Internet.nl](https://internet.nl) is een initiatief van de Nederlandse overheid waarmee
organisaties kunnen testen of hun website en e-mail voldoen aan moderne internetstandaarden.
De standaarden staan op de
[pas-toe-of-leg-uit-lijst van Forum Standaardisatie](https://www.forumstandaardisatie.nl/open-standaarden).

## Sub-skills

| Skill | Wanneer gebruiken | Standaarden |
|-------|-------------------|-------------|
| `/inet-web` | Website testen, HTTPS/TLS instellen, security headers | IPv6, DNSSEC, HTTPS/TLS, HSTS, security headers, security.txt, RPKI |
| `/inet-mail` | E-mail beveiligen, DNS records voor mail | SPF, DKIM, DMARC, STARTTLS, DANE, IPv6, RPKI |
| `/inet-api` | Bulk scans via de API, dashboards bouwen | Batch API v2, authenticatie, resultaten JSON |
| `/inet-toolbox` | Stap-voor-stap implementatie, server configuratie | DNSSEC, HTTPS, DMARC, DKIM, SPF, DANE, IPv6 |

### Routeringsbeslisboom

1. Vraag over **testen** van een website? -> `/inet-web`
2. Vraag over **testen** van e-mail/mailserver? -> `/inet-mail`
3. Vraag over **implementatie/configuratie** van een standaard? -> `/inet-toolbox`
4. Vraag over **bulk scans** of de **API**? -> `/inet-api`
5. Algemene vraag over standaarden? -> Beantwoord hier, verwijs door als nodig

## Standaardencategorieen en Forum Standaardisatie-status

### Webstandaarden

| Standaard | Forum status | Omschrijving |
|-----------|-------------|--------------|
| IPv6 | Verplicht (pas-toe-of-leg-uit) | Internetprotocol versie 6, opvolger van IPv4 |
| DNSSEC | Verplicht (pas-toe-of-leg-uit) | Beveiliging van DNS-naamresolutie tegen manipulatie |
| HTTPS (TLS 1.2/1.3) | Verplicht (pas-toe-of-leg-uit) | Versleutelde verbinding tussen browser en server |
| HSTS | Verplicht (pas-toe-of-leg-uit) | Dwingt browsers HTTPS te gebruiken |
| Security headers | Getest door internet.nl (geen Forum status) | CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy |
| security.txt | Verplicht (pas-toe-of-leg-uit) | Contactinformatie voor beveiligingsonderzoekers (RFC 9116) |
| RPKI | Verplicht (pas-toe-of-leg-uit) | Route Origin Validation, beschermt BGP-routing |

### Mailstandaarden

| Standaard | Forum status | Omschrijving |
|-----------|-------------|--------------|
| SPF | Verplicht (pas-toe-of-leg-uit) | Sender Policy Framework, autoriseert verzendende mailservers |
| DKIM | Verplicht (pas-toe-of-leg-uit) | DomainKeys Identified Mail, digitale handtekening op e-mail |
| DMARC | Verplicht (pas-toe-of-leg-uit) | Domain-based Message Authentication, bouwt voort op SPF+DKIM |
| STARTTLS + DANE | Verplicht (pas-toe-of-leg-uit) | Versleuteling van SMTP-verkeer + DNS-gebaseerde certificaatverificatie |
| IPv6 | Verplicht (pas-toe-of-leg-uit) | Internetprotocol versie 6, bereikbaarheid van MX- en nameservers |
| RPKI | Verplicht (pas-toe-of-leg-uit) | Route Origin Validation voor MX- en nameservers |

## Repositories

De broncode en documentatie staan onder de GitHub-organisatie
[internetstandards](https://github.com/internetstandards):

| Repository | Beschrijving | Licentie |
|-----------|-------------|--------|
| [Internet.nl](https://github.com/internetstandards/Internet.nl) | De internet.nl testsuite (Python/Django) | [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) (code), [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en) (vertalingen) |
| [Internet.nl-API-docs](https://github.com/internetstandards/Internet.nl-API-docs) | Documentatie voor de batch API (v2) | [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en) |
| [toolbox-wiki](https://github.com/internetstandards/toolbox-wiki) | Implementatiegidsen per standaard en platform | [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en) |

## Handige commando's voor repo-exploratie

### Repository-informatie ophalen

```bash
# Lijst van alle repos in de organisatie
gh api orgs/internetstandards/repos --jq '.[].full_name'

# Laatste releases van Internet.nl
gh api repos/internetstandards/Internet.nl/releases --jq '.[0:3][] | "\(.tag_name) - \(.name)"'

# Open issues bekijken
gh api repos/internetstandards/Internet.nl/issues --jq '.[0:5][] | "#\(.number) \(.title)"'
```

### Toolbox-wiki inhoud verkennen

```bash
# Mapstructuur van de toolbox-wiki
gh api repos/internetstandards/toolbox-wiki/git/trees/main?recursive=1 \
  --jq '.tree[] | select(.type=="blob") | .path' | head -30

# Inhoud van een specifiek wiki-bestand ophalen
gh api repos/internetstandards/toolbox-wiki/contents/DNSSEC.md \
  --jq '.content' | base64 -d
```

### API-documentatie verkennen

```bash
# Bestanden in de API-docs repo
gh api repos/internetstandards/Internet.nl-API-docs/git/trees/main?recursive=1 \
  --jq '.tree[] | select(.type=="blob") | .path'
```

## Nuttige links

- [internet.nl](https://internet.nl) - Test je website en e-mail
- [internet.nl/test-site](https://internet.nl/test-site/) - Website testen
- [internet.nl/test-mail](https://internet.nl/test-mail/) - E-mail testen
- [Forum Standaardisatie - Open standaarden](https://www.forumstandaardisatie.nl/open-standaarden)
- [NCSC - Cybersecurity thema's](https://www.ncsc.nl/cybersecurity-themas)

