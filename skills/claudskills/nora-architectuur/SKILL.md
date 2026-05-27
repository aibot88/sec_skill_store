---
name: nora-architectuur
description: >-
  Helpt bij het ontwerpen van overheidssystemen conform de Nederlandse
  Overheid Referentie Architectuur (NORA), inclusief basisprincipes,
  afgeleide principes, informatiebeveiliging (BIO), en de GDI
  (Generieke Digitale Infrastructuur). Biedt richtlijnen voor
  architectuurprincipes, standaarden en voorzieningen. Gebruik deze
  skill wanneer de gebruiker vraagt over 'NORA', 'referentiearchitectuur',
  'enterprise architectuur overheid', 'government architecture',
  'NORA principes', 'basisprincipes overheid', 'afgeleide principes',
  'BIO', 'Baseline Informatiebeveiliging Overheid',
  'informatiebeveiliging overheid', 'information security government',
  'GDI', 'Generieke Digitale Infrastructuur', 'voorzieningen overheid',
  'Diginetwerk', 'Digipoort', 'Digikoppeling', 'Digilevering',
  'Stelsel van Basisregistraties', 'basisregistratie',
  'FORUM standaardisatie', 'pas toe of leg uit',
  'comply or explain', 'open standaarden overheid',
  'lijsten open standaarden', 'verplichte standaard',
  'architectuurprincipe overheid', 'TOGAF overheid', 'ArchiMate overheid',
  'PETRA', 'WILMA', 'ROSA', 'domeinarchitectuur',
  of wanneer de gebruiker een systeem wil ontwerpen volgens
  Nederlandse overheidsarchitectuurprincipes en -standaarden.
model: sonnet
allowed-tools:
  - WebFetch(*)
  - Bash(gh api *)
  - Bash(gh search *)
---

# NORA — Nederlandse Overheid Referentie Architectuur

Ontwerp overheidssystemen conform de NORA-principes, BIO-beveiligingseisen en verplichte open standaarden.

Bron: [NORA Online](https://www.noraonline.nl/) | [BIO](https://www.bio-overheid.nl/) | [Forum Standaardisatie](https://www.forumstandaardisatie.nl/)

## NORA — overzicht

NORA is de overkoepelende enterprise-architectuur voor de gehele Nederlandse overheid. Alle domeinarchitecturen zijn ervan afgeleid.

### Domeinarchitecturen

| Architectuur | Domein | Afgeleid van NORA |
|-------------|--------|-------------------|
| **GEMMA** | Gemeenten | Ja |
| **PETRA** | Provincies | Ja |
| **WILMA** | Waterschappen | Ja |
| **ROSA** | Onderwijs | Ja |
| **EAR** | Rijksdienst | Ja |
| **ZIRA** | Zorg en welzijn | Ja |

## Basisprincipes (BP)

De 10 NORA-basisprincipes gelden voor alle overheidsorganisaties:

| # | Principe | Beschrijving | Implicatie voor software |
|---|---------|-------------|-------------------------|
| BP01 | **Proactief** | Afnemers krijgen de dienstverlening waar zij recht op hebben | Automatisch attenderen op rechten/regelingen |
| BP02 | **Vindbaar** | Afnemers kunnen dienstverlening eenvoudig vinden | Publiceren op overheid.nl, API-catalogus |
| BP03 | **Toegankelijk** | Afnemers hebben eenvoudig toegang tot dienstverlening | DigiD/eHerkenning, digitoegankelijk (WCAG) |
| BP04 | **Standaard** | Afnemers ervaren uniformiteit in de dienstverlening | NL Design System, huisstijl, consistente UX |
| BP05 | **Gebundeld** | Afnemers krijgen gebundelde dienstverlening | Integrale dienstverlening, levensgebeurtenissen |
| BP06 | **Transparant** | Afnemers weten wat de overheid doet met hun gegevens | Privacyverklaring, verwerkingsregister, Woo |
| BP07 | **Noodzakelijk** | Afnemers worden niet lastiggevallen met onnodige vragen | Dataminimalisatie, eenmalige gegevensvraag |
| BP08 | **Vertrouwelijk** | Afnemers kunnen erop vertrouwen dat gegevens niet worden misbruikt | AVG, BIO, versleuteling |
| BP09 | **Betrouwbaar** | Afnemers kunnen erop vertrouwen dat de dienst beschikbaar is | SLA's, redundantie, monitoring |
| BP10 | **Ontvankelijk** | Afnemers kunnen input leveren over de dienstverlening | Feedbackmechanisme, klachtenprocedure |

## Afgeleide principes (AP)

Selectie van de belangrijkste afgeleide principes voor softwareontwikkeling:

### Dienstverlening

| # | Principe | Toelichting |
|---|---------|-------------|
| AP01 | **Digitaal tenzij** | Diensten primair digitaal; alternatief kanaal beschikbaar |
| AP02 | **Eenmalige uitvraag** | Gegevens niet opnieuw vragen als ze al bekend zijn bij de overheid |
| AP04 | **Betrouwbare dienst** | 99,5%+ beschikbaarheid; graceful degradation |
| AP05 | **Ontkoppeld** | Componenten zijn losjes gekoppeld; API-first |

### Informatiebeveiliging

| # | Principe | Toelichting |
|---|---------|-------------|
| AP12 | **Beveiligde verbindingen** | TLS 1.2+; PKIoverheid-certificaten |
| AP13 | **Informatiebeveiligingsbeleid** | Conform BIO (NEN-ISO 27001/27002) |
| AP17 | **Controleerbaarheid** | Audittrail van alle significante acties |
| AP40 | **Encryptie** | Persoonsgegevens en gevoelige data versleuteld in opslag en transport |

### Interoperabiliteit

| # | Principe | Toelichting |
|---|---------|-------------|
| AP41 | **Open standaarden** | Gebruik verplichte open standaarden (Forum Standaardisatie) |
| AP42 | **Open data** | Data openbaar tenzij wettelijke uitzondering |
| AP44 | **Herbruikbare componenten** | Gebruik bestaande GDI-voorzieningen |

## BIO — Baseline Informatiebeveiliging Overheid

De BIO is het basisnormenkader voor informatiebeveiliging bij de overheid, gebaseerd op ISO 27001/27002.

### Structuur

| Aspect | Detail |
|--------|--------|
| **Basis** | NEN-ISO/IEC 27001:2017 en 27002:2017 |
| **Scope** | Rijksoverheid, gemeenten, provincies, waterschappen |
| **BBN-niveaus** | Basisbeveiligingsniveaus 1, 2 en 3 |
| **Toezicht** | CIO Rijk, VNG/IBD (gemeenten), IPO (provincies) |

### Basisbeveiligingsniveaus (BBN)

| BBN | Beschrijving | Wanneer | Voorbeeld |
|-----|-------------|---------|-----------|
| **BBN 1** | Basisbescherming openbare informatie | Websites met alleen openbare info | Openbare website |
| **BBN 2** | Standaardbescherming | Vertrouwelijke en persoonsgegevens | Zaaksysteem, HR-systeem |
| **BBN 3** | Verhoogde bescherming | Staatsgeheimen, bijzonder gevoelig | Inlichtingendiensten |

### BIO-maatregelen per categorie

| ISO-hoofdstuk | Onderwerp | Kernmaatregelen |
|---------------|-----------|----------------|
| **5** | Informatiebeveiligingsbeleid | Beleidsdocument, rollen, verantwoordelijkheden |
| **6** | Organisatie | CISO aanstellen, taken en bevoegdheden |
| **7** | Personeel | Screening, bewustwording, geheimhouding |
| **8** | Asset management | Classificatie, eigenaarschap, CMDB |
| **9** | Toegangsbeveiliging | RBAC, least privilege, MFA, wachtwoordbeleid |
| **10** | Cryptografie | TLS 1.2+, AES-256, PKIoverheid |
| **12** | Beveiliging bedrijfsvoering | Patchmanagement, malwarebescherming, logging |
| **13** | Communicatiebeveiliging | Netwerksegmentatie, VPN, Diginetwerk |
| **14** | Systemen acquisitie/ontwikkeling | Secure SDLC, SAST/DAST, dependency scanning |
| **16** | Incidentmanagement | Incidentresponsplan, meldplicht (AP, NCSC) |
| **17** | Bedrijfscontinuiteit | BCP, DR-plan, RPO/RTO |
| **18** | Compliance | Audits, penetratietests, certificering |

### BIO-maatregelen voor softwareontwikkeling (hfst. 14)

| Maatregel | BIO-ref | Beschrijving |
|-----------|---------|-------------|
| **Secure development policy** | 14.2.1 | Richtlijnen voor veilig ontwikkelen |
| **Change control** | 14.2.2 | Wijzigingsbeheer voor applicaties |
| **Technical review** | 14.2.3 | Review na platformwijzigingen |
| **Secure coding** | 14.2.5 | OWASP Top 10 mitigatie, input validation |
| **Secure development environment** | 14.2.6 | Gescheiden OTAP-omgevingen |
| **Security testing** | 14.2.8 | SAST, DAST, penetratietest |
| **System acceptance testing** | 14.2.9 | Beveiligingsacceptatietest |

### BIO compliance in code

```python
# Voorbeeld: logging conform BIO 12.4

import logging
import json
from datetime import datetime

class BIOAuditLogger:
    """Auditlogging conform BIO 12.4 (Basisbeveiligingsniveau 2)."""

    def __init__(self):
        self.logger = logging.getLogger("bio.audit")

    def log_event(
        self,
        event_type: str,
        actor: str,
        resource: str,
        action: str,
        result: str,
        details: dict | None = None,
    ):
        """
        Log een beveiligingsrelevante gebeurtenis.

        BIO 12.4.1: Gebeurtenissen vastleggen met:
        - gebruikersidentificatie (actor)
        - type gebeurtenis (event_type)
        - datum en tijd (automatisch)
        - succes of falen (result)
        - bron van de gebeurtenis (resource)
        """
        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": event_type,
            "actor": actor,          # Gebruikers-ID (NIET BSN)
            "resource": resource,
            "action": action,
            "result": result,         # "success" | "failure" | "denied"
            # NOOIT persoonsgegevens in details
        }
        if details:
            event["details"] = details
        self.logger.info(json.dumps(event))

# Gebruik:
audit = BIOAuditLogger()
audit.log_event(
    event_type="data_access",
    actor="medewerker-12345",
    resource="zaak/ZAAK-2026-001",
    action="read",
    result="success"
)
```

## Verplichte open standaarden (Forum Standaardisatie)

Het Forum Standaardisatie beheert de "pas-toe-of-leg-uit"-lijst van verplichte open standaarden:

### Lijsten

| Lijst | Verplichting | Beschrijving |
|-------|-------------|-------------|
| **Verplicht (pas-toe-of-leg-uit)** | Ja, tenzij onderbouwde uitzondering | Standaarden voor inkoop en gebruik door overheid |
| **Aanbevolen** | Nee, wel gewenst | Goede praktijkstandaarden |

### Selectie verplichte standaarden voor software

| Standaard | Functioneel gebied | Versie |
|-----------|-------------------|--------|
| **TLS** | Internetbeveiliging | 1.2+ (1.3 aanbevolen) |
| **HTTPS** | Webbeveiliging | Verplicht voor alle overheidswebsites |
| **DKIM + DMARC + SPF** | E-mailbeveiliging | Verplicht voor overheidsdomeinen |
| **DNSSEC** | Domeinbeveiliging | Verplicht |
| **IPv6** | Netwerk | Verplicht naast IPv4 (dual-stack) |
| **RPKI** | Routingbeveiliging | Verplicht |
| **NL API Design Rules** | API-ontwerp | Verplicht voor REST API's |
| **OpenAPI 3.x** | API-documentatie | Verplicht voor REST API's |
| **SAML** | Authenticatie | 2.0 |
| **OpenID Connect** | Authenticatie | 1.0 |
| **OAuth 2.0** | Autorisatie | 2.0 |
| **Digikoppeling** | Berichtenuitwisseling | WUS, ebMS, REST profiel |
| **OWMS** | Metadata overheidsinfo | 4.0 |
| **PDF/A** | Documentarchivering | 1b, 2b |
| **ODF** | Documentuitwisseling | 1.2+ |
| **WCAG** | Digitale toegankelijkheid | 2.1 (AA) |
| **SKOS** | Thesauri en taxonomieën | Verplicht voor waardelijsten |
| **GML** | Geo-informatie | 3.2 |
| **WMS/WFS** | Geo-services | 1.3/2.0 |

## GDI — Generieke Digitale Infrastructuur

De GDI is het stelsel van gemeenschappelijke digitale voorzieningen:

| Voorziening | Functie | Beheerder |
|-------------|---------|-----------|
| **DigiD** | Authenticatie burgers | Logius |
| **eHerkenning** | Authenticatie bedrijven | Marktpartijen |
| **MijnOverheid** | Persoonlijke berichten/post | Logius |
| **Digipoort** | Berichtenuitwisseling B2G | Logius |
| **Digikoppeling** | Standaard voor gegevensuitwisseling | Logius |
| **Digilevering** | Gegevenslevering uit basisregistraties | Logius |
| **Diginetwerk** | Besloten overheidsnetwerk | Logius |
| **Stelsel Basisregistraties** | 10 basisregistraties (BRP, BAG, BRK, etc.) | Diverse |
| **developer.overheid.nl** | API-catalogus | KOOP |
| **Standaarden.overheid.nl** | Standaardencatalogus | Forum Standaardisatie |

### Stelsel van Basisregistraties

| Registratie | Afkorting | Gegevens | Houder |
|-------------|-----------|----------|--------|
| Basisregistratie Personen | **BRP** | Persoonsgegevens | RvIG |
| Basisregistratie Adressen en Gebouwen | **BAG** | Adressen, panden | Kadaster |
| Basisregistratie Kadaster | **BRK** | Kadastrale percelen, eigendom | Kadaster |
| Basisregistratie Topografie | **BRT** | Topografische kaarten | Kadaster |
| Basisregistratie Grootschalige Topografie | **BGT** | Gedetailleerde kaarten | SVB-BGT |
| Handelsregister | **HR** | Bedrijven, KvK-nummers | KVK |
| WOZ | **WOZ** | Objectwaardering | Gemeenten |
| Basisregistratie Ondergrond | **BRO** | Bodem, grondwater | TNO |
| Basisregistratie Voertuigen | **BRV** | Voertuigregistratie | RDW |
| Basisregistratie Inkomen | **BRI** | Inkomensverhoudingen | Belastingdienst |

### Digikoppeling-profielen

| Profiel | Protocol | Gebruik |
|---------|----------|--------|
| **WUS** | SOAP/WSDL | Synchrone bevraging (request-response) |
| **ebMS2** | ebXML | Asynchrone berichtenuitwisseling (MSH) |
| **REST** | REST/JSON | Moderne API-communicatie (nieuwste profiel) |
| **Grote Berichten** | HTTPS + MSH | Bestanden >20MB |

## OTAP en Change Management

| Omgeving | Doel | BIO-eis |
|----------|------|---------|
| **Ontwikkel (O)** | Development | Geen productiedata |
| **Test (T)** | Functioneel testen | Geanonimiseerde testdata |
| **Acceptatie (A)** | Gebruikersacceptatie | Geanonimiseerde data; beveiligingstest |
| **Productie (P)** | Live omgeving | Volledige BIO-maatregelen |

## Implementatie-checklist

- [ ] **NORA-basisprincipes**: architectuur getoetst aan de 10 basisprincipes
- [ ] **BIO-classificatie**: basisbeveiligingsniveau (BBN 1/2/3) bepaald
- [ ] **BIO-maatregelen**: alle maatregelen voor het vastgestelde BBN geimplementeerd
- [ ] **Open standaarden**: alle toepasselijke verplichte standaarden uit de "pas-toe-of-leg-uit"-lijst
- [ ] **TLS 1.2+**: alle verbindingen versleuteld met minimaal TLS 1.2
- [ ] **HTTPS**: alle webverkeer via HTTPS; HSTS-header ingesteld
- [ ] **DNSSEC + DKIM + DMARC + SPF**: e-mail- en domeinbeveiliging geconfigureerd
- [ ] **IPv6**: dual-stack (IPv4 + IPv6) ondersteund
- [ ] **Digikoppeling**: gegevensuitwisseling via Digikoppeling-profiel waar vereist
- [ ] **GDI-voorzieningen**: hergebruik van DigiD, eHerkenning, Haal Centraal waar toepasbaar
- [ ] **OTAP-scheiding**: gescheiden omgevingen conform BIO 14.2.6
- [ ] **Auditlogging**: beveiligingsrelevante events gelogd conform BIO 12.4
- [ ] **Penetratietest**: minimaal jaarlijks uitgevoerd door onafhankelijke partij
- [ ] **API Design Rules**: REST API's conform NL API Design Rules + OpenAPI 3.x
- [ ] **Standaardentoets**: architectuur getoetst bij Forum Standaardisatie waar nodig

## Gerelateerde skills

| Skill | Wanneer te gebruiken |
|-------|---------------------|
| **gemma-common-ground** | GEMMA referentiearchitectuur, Common Ground, Open Zaak/Formulieren |
| **zgw-apis** | ZGW API-standaarden, Haal Centraal — invulling van NORA-principes |
| **overheid-authenticatie** | DigiD, eHerkenning — GDI-voorzieningen voor authenticatie |
| **avg-privacy** | AVG/GDPR — privacy-aspecten van de architectuur |
| **llm-security** | OWASP LLM Top 10 beveiligingscontrols |
| **genai-governance** | EU AI Act technische governance-controls |
| **digitoegankelijk** | WCAG toegankelijkheid — verplichte open standaard |

## Meer informatie

- [NORA Online](https://www.noraonline.nl/) | [NORA principes](https://www.noraonline.nl/wiki/Principes)
- [BIO](https://www.bio-overheid.nl/) | [BIO normenkader](https://www.bio-overheid.nl/category/bio-thema)
- [Forum Standaardisatie](https://www.forumstandaardisatie.nl/) | [Standaardenlijst](https://www.forumstandaardisatie.nl/open-standaarden)
- [GDI](https://www.digitaleoverheid.nl/overzicht-van-alle-onderwerpen/generieke-digitale-infrastructuur/) — Generieke Digitale Infrastructuur
- [Logius](https://www.logius.nl/) — beheerder GDI-voorzieningen
- [Digitale Overheid](https://www.digitaleoverheid.nl/) — beleid en strategie
- [NEN-ISO 27001/27002](https://www.nen.nl/iso-iec-27001-2022-nl-304921) — basis voor BIO
- [NCSC beveiligingsrichtlijnen](https://www.ncsc.nl/onderwerpen/ict-beveiligingsrichtlijnen) — aanvullende technische richtlijnen
