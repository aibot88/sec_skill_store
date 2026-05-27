---
name: zgw-apis
description: >-
  Helpt bij het integreren met ZGW API-standaarden (Zaakgericht Werken) en
  Haal Centraal API's voor Nederlandse overheidsorganisaties. Biedt richtlijnen
  voor de Zaken API, Documenten API, Catalogi API, Besluiten API,
  Klantinteracties API, en Haal Centraal (BRP, BAG, BRK, WOZ). Gebruik deze
  skill wanneer de gebruiker vraagt over 'ZGW', 'zaakgericht werken',
  'Zaken API', 'Documenten API', 'Catalogi API', 'Besluiten API',
  'Autorisaties API', 'Contactmomenten API', 'Klantinteracties API',
  'ZGW API', 'case management API', 'zaaktype', 'zaak aanmaken',
  'document uploaden', 'informatieobject', 'statustype', 'resultaattype',
  'Haal Centraal', 'BRP API', 'BAG API', 'BRK API', 'WOZ API',
  'basisregistratie', 'base registry API', 'personen API', 'adressen API',
  'kadaster API', 'VNG Realisatie', 'VNG standaarden',
  'NL API Design Rules', 'API Design Rules overheid',
  'REST API overheid', 'government REST API', 'Common Ground API',
  'Open Zaak', 'zaaksysteem', 'case system', 'OpenAPI overheid',
  'API-strategie overheid', 'Digikoppeling REST',
  of wanneer de gebruiker wil integreren met Nederlandse overheids-API's
  voor zaakgericht werken of basisregistraties.
model: sonnet
allowed-tools:
  - WebFetch(*)
  - Bash(gh api *)
  - Bash(gh search *)
  - Bash(curl *)
---

# ZGW API-standaarden & Haal Centraal

Integreer met de standaard-API's voor zaakgericht werken en basisregistraties bij de Nederlandse overheid.

Bron: [VNG Realisatie — ZGW API's](https://vng-realisatie.github.io/gemma-zaken/) | [Haal Centraal](https://vng-realisatie.github.io/Haal-Centraal/) | [API Design Rules](https://logius-standaarden.github.io/API-Design-Rules/)

## ZGW API-standaarden — overzicht

De ZGW API's zijn de VNG-standaarden voor zaakgericht werken, onderdeel van de Common Ground-architectuur.

| API | Versie | Beschrijving |
|-----|--------|-------------|
| **Zaken API** | 1.5.x | Aanmaken, bijwerken en opvragen van zaken |
| **Documenten API** | 1.5.x | Beheer van informatieobjecten (documenten) bij zaken |
| **Catalogi API** | 1.3.x | Zaaktypen, statustypen, resultaattypen, informatieobjecttypen |
| **Besluiten API** | 1.1.x | Besluiten koppelen aan zaken |
| **Autorisaties API** | 1.1.x | Autorisatiebeheer voor API-consumers |
| **Klantinteracties API** | 2.0.x | Contactmomenten en klantcontacten bij zaken |

### Referentie-implementatie

**Open Zaak** is de open-source referentie-implementatie van alle ZGW API's: [github.com/open-zaak/open-zaak](https://github.com/open-zaak/open-zaak)

## Zaken API — kernoperaties

### Zaak aanmaken

```http
POST /zaken/api/v1/zaken HTTP/1.1
Host: openzaak.gemeente.nl
Authorization: Bearer {token}
Content-Type: application/json

{
  "bronorganisatie": "123456789",
  "zaaktype": "https://catalogi.gemeente.nl/api/v1/zaaktypen/{uuid}",
  "verantwoordelijkeOrganisatie": "123456789",
  "startdatum": "2026-02-23",
  "omschrijving": "Aanvraag omgevingsvergunning Hoofdstraat 1"
}
```

**Response (201 Created):**
```json
{
  "url": "https://openzaak.gemeente.nl/zaken/api/v1/zaken/{uuid}",
  "uuid": "b7c1e3d4-...",
  "identificatie": "ZAAK-2026-000123",
  "bronorganisatie": "123456789",
  "zaaktype": "https://catalogi.gemeente.nl/api/v1/zaaktypen/{uuid}",
  "startdatum": "2026-02-23",
  "status": null
}
```

### Status wijzigen

```http
POST /zaken/api/v1/statussen HTTP/1.1
Authorization: Bearer {token}
Content-Type: application/json

{
  "zaak": "https://openzaak.gemeente.nl/zaken/api/v1/zaken/{zaak-uuid}",
  "statustype": "https://catalogi.gemeente.nl/api/v1/statustypen/{uuid}",
  "datumStatusGezet": "2026-02-23T10:00:00Z",
  "statustoelichting": "Zaak in behandeling genomen"
}
```

### Zaak opvragen met expand

```http
GET /zaken/api/v1/zaken/{uuid}?expand=status,resultaat,zaaktype HTTP/1.1
Authorization: Bearer {token}
Accept: application/json
```

### Zoeken op kenmerken

```http
GET /zaken/api/v1/zaken?zaaktype=https://...&startdatum__gte=2026-01-01&ordering=-startdatum&page=1 HTTP/1.1
Authorization: Bearer {token}
```

## Documenten API — informatieobjecten

### Document uploaden

```http
POST /documenten/api/v1/enkelvoudiginformatieobjecten HTTP/1.1
Authorization: Bearer {token}
Content-Type: application/json

{
  "bronorganisatie": "123456789",
  "creatiedatum": "2026-02-23",
  "titel": "Aanvraagformulier omgevingsvergunning",
  "auteur": "Jan Jansen",
  "taal": "nld",
  "informatieobjecttype": "https://catalogi.gemeente.nl/api/v1/informatieobjecttypen/{uuid}",
  "inhoud": "base64-encoded-content",
  "formaat": "application/pdf",
  "bestandsnaam": "aanvraag.pdf"
}
```

### Document koppelen aan zaak

```http
POST /zaken/api/v1/zaakinformatieobjecten HTTP/1.1
Authorization: Bearer {token}
Content-Type: application/json

{
  "zaak": "https://openzaak.gemeente.nl/zaken/api/v1/zaken/{zaak-uuid}",
  "informatieobject": "https://documenten.gemeente.nl/api/v1/enkelvoudiginformatieobjecten/{doc-uuid}"
}
```

## Catalogi API — configuratie

### Zaaktypen opvragen

```http
GET /catalogi/api/v1/zaaktypen?catalogus=https://...&status=alles HTTP/1.1
Authorization: Bearer {token}
```

### Statustypen bij een zaaktype

```http
GET /catalogi/api/v1/statustypen?zaaktype=https://catalogi.gemeente.nl/api/v1/zaaktypen/{uuid} HTTP/1.1
Authorization: Bearer {token}
```

## Haal Centraal — basisregistratie-API's

| API | Basisregistratie | Beschrijving |
|-----|-----------------|-------------|
| **BRP Personen** | BRP | Persoonsgegevens (naam, adres, BSN, nationaliteit) |
| **BAG Adressen** | BAG | Adressen en gebouwen (nummeraanduiding, verblijfsobject) |
| **BRK Kadaster** | BRK | Kadastrale gegevens (percelen, eigenaren) |
| **WOZ Waardering** | WOZ | WOZ-waarde van onroerende zaken |
| **HR Handelsregister** | HR | Bedrijfsgegevens (KvK) |

### BRP Personen bevragen

```http
POST /haalcentraal/api/brp/personen HTTP/1.1
Authorization: Bearer {token}
Content-Type: application/json

{
  "type": "RaadpleegMetBurgerservicenummer",
  "burgerservicenummer": ["999993653"],
  "fields": ["naam", "geboorte", "verblijfplaats"]
}
```

**Response:**
```json
{
  "personen": [
    {
      "naam": {
        "voornamen": "Jan",
        "geslachtsnaam": "Jansen"
      },
      "geboorte": {
        "datum": "1990-01-15"
      },
      "verblijfplaats": {
        "verblijfadres": {
          "straat": "Hoofdstraat",
          "huisnummer": 1,
          "postcode": "1234AB",
          "woonplaats": "Amsterdam"
        }
      }
    }
  ]
}
```

### BAG Adressen zoeken

```http
GET /haalcentraal/api/bag/adressen?postcode=1234AB&huisnummer=1 HTTP/1.1
Authorization: Bearer {token}
```

## Authenticatie en autorisatie

### JWT-token voor ZGW API's

ZGW API's gebruiken JWT-tokens met een specifiek claims-formaat:

```python
import jwt
import time

def create_zgw_token(client_id: str, secret: str) -> str:
    """Maak een JWT-token aan voor ZGW API-authenticatie."""
    payload = {
        "iss": client_id,
        "iat": int(time.time()),
        "client_id": client_id,
        "user_id": "",
        "user_representation": ""
    }
    return jwt.encode(payload, secret, algorithm="HS256")
```

### NL API Design Rules — verplichte regels

| Regel | Beschrijving |
|-------|-------------|
| **API-01** | API's zijn RESTful tenzij anders aangewezen |
| **API-03** | API's zijn beveiligd met minimaal transport-level security (TLS) |
| **API-05** | Documenteer API's conform OpenAPI Specification v3.x |
| **API-06** | Gebruik JSON als standaard content-type |
| **API-09** | Gebruik ISO 8601 voor datums en tijden |
| **API-10** | Gebruik standaard HTTP-methoden (GET, POST, PUT, PATCH, DELETE) |
| **API-16** | Gebruik standaard HTTP-statuscodes |
| **API-20** | API's geven gestandaardiseerde foutresponses (RFC 7807) |
| **API-48** | Laat uitbreiden van API-responses toe (`expand` of `fields` parameter) |
| **API-51** | Publiceer API's op developer.overheid.nl |

### RFC 7807 foutresponse

```json
{
  "type": "https://gemeente.nl/fouten/validatie",
  "title": "Validatiefout",
  "status": 400,
  "detail": "Het veld 'startdatum' is verplicht.",
  "instance": "/zaken/api/v1/zaken",
  "invalidParams": [
    {
      "name": "startdatum",
      "code": "required",
      "reason": "Dit veld is vereist."
    }
  ]
}
```

## Paginering

ZGW API's gebruiken page-number paginering:

```http
GET /zaken/api/v1/zaken?page=2&pageSize=100 HTTP/1.1
```

**Response:**
```json
{
  "count": 523,
  "next": "https://openzaak.gemeente.nl/zaken/api/v1/zaken?page=3",
  "previous": "https://openzaak.gemeente.nl/zaken/api/v1/zaken?page=1",
  "results": [...]
}
```

Haal Centraal API's gebruiken cursor- of HAL-paginering met `_links`:

```json
{
  "_embedded": { "adressen": [...] },
  "_links": {
    "self": { "href": "/adressen?page=1" },
    "next": { "href": "/adressen?page=2" }
  }
}
```

## Implementatie-checklist

- [ ] **ZGW-versie**: gebruik de laatste stabiele versie van elke API (controleer VNG-documentatie)
- [ ] **Catalogi eerst**: configureer zaaktypen, statustypen, resultaattypen in Catalogi API vóór gebruik
- [ ] **JWT-authenticatie**: implementeer token-generatie conform ZGW-specificatie
- [ ] **TLS**: alle API-communicatie via HTTPS (NL API Design Rule API-03)
- [ ] **Foutafhandeling**: verwerk RFC 7807 foutresponses correct
- [ ] **Paginering**: verwerk `next`/`previous` links voor grote resultaatsets
- [ ] **Expand**: gebruik `expand` parameter om N+1 queries te voorkomen
- [ ] **Notificaties**: abonneer op ZGW notificaties voor asynchrone verwerking
- [ ] **Audittrail**: audittrail API inschakelen voor traceerbaarheid
- [ ] **BSN-bescherming**: BSN alleen via beveiligde verbinding; niet loggen
- [ ] **Fields**: gebruik `fields` parameter bij Haal Centraal voor dataminimalisatie
- [ ] **OpenAPI**: documenteer eigen API's met OpenAPI v3.x
- [ ] **developer.overheid.nl**: publiceer API op developer.overheid.nl

## Gerelateerde skills

| Skill | Wanneer te gebruiken |
|-------|---------------------|
| **gemma-common-ground** | GEMMA architectuur, Common Ground, NLX/FSC, Haven |
| **mdto-archivering** | MDTO-metadata voor zaakgericht archiveren en e-depot |
| **overheid-authenticatie** | DigiD/eHerkenning voor authenticatie op zaak-portalen |
| **avg-privacy** | Privacy by Design bij verwerking van persoonsgegevens in zaken |
| **nora-architectuur** | NORA-principes en BIO-beveiliging voor API-implementaties |

## Meer informatie

- [VNG ZGW API-standaarden](https://vng-realisatie.github.io/gemma-zaken/) | [GitHub](https://github.com/VNG-Realisatie/gemma-zaken)
- [Open Zaak](https://github.com/open-zaak/open-zaak) — referentie-implementatie
- [Haal Centraal](https://vng-realisatie.github.io/Haal-Centraal/) | [GitHub](https://github.com/VNG-Realisatie/Haal-Centraal)
- [NL API Design Rules](https://logius-standaarden.github.io/API-Design-Rules/)
- [developer.overheid.nl](https://developer.overheid.nl/) — API-catalogus Nederlandse overheid
- [API Design Rules extensies](https://logius-standaarden.github.io/API-Design-Rules/extensions/)
