---
name: publieke-code
description: >-
  Helpt bij het open-source publiceren van overheidssoftware conform de
  Standard for Public Code, publiccode.yml, REUSE-compliance en de
  Nederlandse open-sourcerichtlijnen. Biedt richtlijnen voor codebase
  governance, licentiekeuze, community-opbouw en publicatie op
  developer.overheid.nl. Gebruik deze skill wanneer de gebruiker vraagt
  over 'publieke code', 'public code', 'Standard for Public Code',
  'publiccode.yml', 'publiccode yaml', 'REUSE', 'REUSE compliance',
  'REUSE-compliant', 'open source overheid', 'open source government',
  'EUPL', 'EUPL licentie', 'EUPL-1.2', 'open source licentie overheid',
  'code publiceren overheid', 'broncode publiceren', 'source code publish',
  'softwarecatalogus', 'developer overheid', 'code.overheid.nl',
  'GitHub overheid', 'GitLab overheid',
  'open source compliance', 'licentiekeuze overheid',
  'open source beleid', 'open source policy',
  'hergebruik software', 'software reuse government',
  'community management open source', 'OSPO', 'OSPO overheid',
  'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md',
  of wanneer de gebruiker overheidssoftware open source wil publiceren
  of wil voldoen aan de Standard for Public Code.
model: sonnet
allowed-tools:
  - WebFetch(*)
  - Bash(gh api *)
  - Bash(gh search *)
---

# Publieke Code — Open Source Publicatie voor de Overheid

Publiceer overheidssoftware als open source conform de Standard for Public Code en Nederlandse richtlijnen.

Bron: [Standard for Public Code](https://standard.publiccode.net/) | [REUSE](https://reuse.software/) | [developer.overheid.nl](https://developer.overheid.nl/)

## Waarom publieke code?

| Aspect | Detail |
|--------|--------|
| **Beleid** | "Open, tenzij" — overheidscode is openbaar tenzij er zwaarwegende redenen zijn |
| **Wet** | Wet hergebruik overheidsinformatie (Who); Motie Vendrik (2002) |
| **EU** | Interoperable Europe Act; EU OSPO; Joinup platform |
| **Voordelen** | Hergebruik, transparantie, leveranciersonafhankelijkheid, samenwerking, innovatie |
| **Kader** | Standard for Public Code (Foundation for Public Code) |
| **Licentie** | EUPL-1.2 (aanbevolen), Apache-2.0, MIT |

## Standard for Public Code — criteria

| Criterium | Beschrijving | Vereist |
|----------|-------------|---------|
| **Code in the open** | Repository is publiek toegankelijk | Ja |
| **Bundle policy and source code** | Beleid en code in dezelfde repository | Ja |
| **Create reusable and portable code** | Configureerbaar, geen hardcoded aannames | Ja |
| **Welcome contributors** | CONTRIBUTING.md, CODE_OF_CONDUCT.md, issue templates | Ja |
| **Require review of contributions** | Code review via pull requests | Ja |
| **Document codebase objectives** | README met doel, installatie, gebruik | Ja |
| **Document the code** | Inline documentatie, API-docs | Ja |
| **Use plain English** | Documentatie in het Engels (of tweetalig) | Aanbevolen |
| **Use open standards** | Geen proprietary standaarden of formaten | Ja |
| **Use continuous integration** | CI/CD pipeline die automatisch test en valideert | Ja |
| **Publish with an open license** | Open-source licentie (EUPL, Apache, MIT) | Ja |
| **Make the codebase findable** | publiccode.yml, registratie op softwarecatalogus | Ja |
| **Use a coherent style** | Linting, formattering, style guide | Ja |
| **Document codebase maturity** | Lifecycle status (concept, beta, stable, deprecated) | Ja |

## publiccode.yml

Elke publieke codebase bevat een `publiccode.yml` in de root van de repository:

```yaml
publiccodeYmlVersion: "0.4"

name: Open Zaak
url: "https://github.com/open-zaak/open-zaak"
releaseDate: "2026-02-01"
developmentStatus: stable
softwareType: standalone/backend

description:
  nl:
    shortDescription: "Zaakregistratiecomponent conform ZGW API-standaarden"
    longDescription: >
      Open Zaak is een moderne, open-source implementatie van de
      ZGW API-standaarden voor zaakgericht werken bij gemeenten.
    documentation: "https://open-zaak.readthedocs.io/"
    features:
      - Zaken API
      - Documenten API
      - Catalogi API
      - Besluiten API
      - Autorisaties API

legal:
  license: EUPL-1.2
  mainCopyrightOwner: Dimpact
  repoOwner: open-zaak

maintenance:
  type: community
  contacts:
    - name: Maykin Media
      email: info@maykinmedia.nl

platforms:
  - web
  - linux

categories:
  - case-management
  - document-management

dependsOn:
  open:
    - name: Python
      versionMin: "3.10"
    - name: PostgreSQL
      versionMin: "14"
    - name: Redis

intendedAudience:
  countries:
    - nl
  scope:
    - government

localisation:
  localisationReady: true
  availableLanguages:
    - nl
    - en
```

## REUSE-compliance

REUSE zorgt ervoor dat elke file in de repository duidelijke licentie-informatie heeft.

### REUSE instellen

```bash
# Installeer de REUSE tool
pip install reuse

# Voeg licentie-headers toe aan alle bestanden
reuse annotate --license EUPL-1.2 --copyright "Gemeente Amsterdam" src/**/*.py

# Voeg de licentietekst toe
reuse download EUPL-1.2

# Controleer REUSE-compliance
reuse lint
```

### Bestandsstructuur

```
project/
  LICENSES/
    EUPL-1.2.txt          # Volledige licentietekst
    CC-BY-4.0.txt         # Voor documentatie
    CC0-1.0.txt           # Voor configuratie/data
  .reuse/
    dep5                  # Bulk-licentie-toewijzing
  src/
    app.py                # SPDX header in elk bestand
  docs/
    handleiding.md        # CC-BY-4.0 licentie
  publiccode.yml
  README.md
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  CHANGELOG.md
```

### SPDX-headers

```python
# SPDX-FileCopyrightText: 2026 Gemeente Amsterdam
# SPDX-License-Identifier: EUPL-1.2

"""Zaakregistratie module."""
```

### .reuse/dep5 (bulk-toewijzing)

```
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/

Files: *.json *.yaml *.yml *.toml
Copyright: 2026 Gemeente Amsterdam
License: EUPL-1.2

Files: docs/*
Copyright: 2026 Gemeente Amsterdam
License: CC-BY-4.0

Files: .gitignore .editorconfig
Copyright: 2026 Gemeente Amsterdam
License: CC0-1.0
```

## Licentiekeuze

| Licentie | Type | Aanbevolen voor | Copyleft |
|----------|------|----------------|----------|
| **EUPL-1.2** | Copyleft | Overheidssoftware (aanbevolen) | Ja (weak) |
| **Apache-2.0** | Permissive | Libraries, API-clients | Nee |
| **MIT** | Permissive | Kleine tools, scripts | Nee |
| **CC-BY-4.0** | Creative Commons | Documentatie | N.v.t. |
| **CC0-1.0** | Public Domain | Configuratie, open data | N.v.t. |

### Waarom EUPL-1.2?

| Voordeel | Detail |
|---------|--------|
| **Europees** | Officieel vertaald in alle EU-talen; rechtsgeldig in NL |
| **Compatibel** | Upstream-compatible met GPL, LGPL, AGPL, MPL, EUPL |
| **Copyleft** | Wijzigingen moeten ook open source zijn (beschermt investering) |
| **SaaS** | EUPL copyleft geldt ook bij netwerk-interactie (zoals AGPL) |
| **Geen patentoorlog** | Expliciet patentvergunning |

## Repository-inrichting

### Verplichte bestanden

| Bestand | Inhoud |
|---------|--------|
| `README.md` | Doel, installatie, gebruik, bijdragen, licentie |
| `LICENSE` of `LICENSES/` | Licentietekst(en) |
| `CONTRIBUTING.md` | Hoe bijdragen; review-proces; code of conduct |
| `CODE_OF_CONDUCT.md` | Gedragscode (bijv. Contributor Covenant) |
| `CHANGELOG.md` | Wijzigingslog (Keep a Changelog) |
| `publiccode.yml` | Machine-leesbare metadata |
| `.reuse/dep5` | REUSE bulk-licentietoewijzing |
| `SECURITY.md` | Responsible disclosure beleid |

### GitHub repository template

```bash
# Security policy
cat > SECURITY.md << 'EOF'
# Security Policy

## Responsible Disclosure

Meld beveiligingsproblemen via [security@organisatie.nl](mailto:security@organisatie.nl).

Maak **geen** GitHub issue aan voor beveiligingsproblemen.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 2.x     | Yes       |
| 1.x     | No        |

## Response Time

We streven ernaar om binnen 5 werkdagen te reageren.
EOF
```

## CI/CD voor publieke code

```yaml
# .github/workflows/public-code.yml
name: Public Code Compliance

on: [push, pull_request]

jobs:
  reuse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: fsfe/reuse-action@v4

  publiccode:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate publiccode.yml
        uses: italia/publiccode-parser-action@v2
        with:
          publiccode: publiccode.yml

  standard-for-public-code:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check Standard for Public Code
        run: |
          # Controleer verplichte bestanden
          for f in README.md LICENSE CONTRIBUTING.md CODE_OF_CONDUCT.md CHANGELOG.md publiccode.yml SECURITY.md; do
            if [ ! -f "$f" ] && [ ! -d "LICENSES" ]; then
              echo "ONTBREEKT: $f"
              exit 1
            fi
          done
          echo "Alle verplichte bestanden aanwezig"
```

## Publicatie en vindbaarheid

| Platform | Doel | URL |
|----------|------|-----|
| **developer.overheid.nl** | API- en softwarecatalogus | developer.overheid.nl |
| **Softwarecatalogus (VNG)** | Gemeentelijke software | softwarecatalogus.nl |
| **Joinup (EU)** | Europees hergebruik | joinup.ec.europa.eu |
| **GitHub/GitLab** | Broncode hosting | github.com / gitlab.com |

## Implementatie-checklist

- [ ] **Repository publiek**: code is openbaar op GitHub/GitLab
- [ ] **Licentie**: EUPL-1.2 (of Apache-2.0/MIT) toegepast
- [ ] **REUSE-compliant**: elke file heeft SPDX-header; `reuse lint` slaagt
- [ ] **publiccode.yml**: machine-leesbare metadata in repo-root
- [ ] **README.md**: doel, installatie, gebruik, bijdragen, licentie
- [ ] **CONTRIBUTING.md**: bijdrage-richtlijnen en review-proces
- [ ] **CODE_OF_CONDUCT.md**: gedragscode (Contributor Covenant)
- [ ] **CHANGELOG.md**: wijzigingslog (Keep a Changelog)
- [ ] **SECURITY.md**: responsible disclosure beleid
- [ ] **CI/CD**: pipeline die test, lint en valideert
- [ ] **Code review**: pull request vereist voor alle wijzigingen
- [ ] **Catalogus**: geregistreerd op developer.overheid.nl en/of softwarecatalogus
- [ ] **Documentatie**: installatie, configuratie, API-docs bijgewerkt

## Gerelateerde skills

| Skill | Wanneer te gebruiken |
|-------|---------------------|
| **nora-architectuur** | Verplichte open standaarden en architectuurprincipes |
| **digitoegankelijk** | WCAG-toegankelijkheid voor publieke interfaces |
| **nl-design-system** | Herbruikbare UI-componenten als open source |
| **gemma-common-ground** | Common Ground open-source componenten |

## Meer informatie

- [Standard for Public Code](https://standard.publiccode.net/) | [Criteria](https://standard.publiccode.net/criteria/)
- [Foundation for Public Code](https://publiccode.net/)
- [REUSE](https://reuse.software/) | [REUSE FAQ](https://reuse.software/faq/)
- [EUPL-1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)
- [publiccode.yml standaard](https://yml.publiccode.tools/)
- [developer.overheid.nl](https://developer.overheid.nl/)
- [Joinup (EU)](https://joinup.ec.europa.eu/) — Europees hergebruik platform
- [Open Source beleid Rijksoverheid](https://www.digitaleoverheid.nl/overzicht-van-alle-onderwerpen/open-source/)
