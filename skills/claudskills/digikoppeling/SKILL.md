---
name: digikoppeling
description: >-
  Helpt bij het implementeren van Digikoppeling voor beveiligde
  system-to-system communicatie tussen overheidsorganisaties. Begeleidt
  bij het kiezen en implementeren van het juiste koppelvlakprofiel
  (REST API, WUS, ebMS2), PKIoverheid-certificaten, OIN-registratie
  en aansluiting op Diginetwerk. Gebruik deze skill wanneer de gebruiker
  vraagt over 'Digikoppeling', 'koppelvlak overheid', 'system-to-system',
  'REST profiel', 'WUS profiel', 'ebMS2 profiel', 'PKIoverheid certificaat',
  'Diginetwerk', 'OIN', 'CPA', 'beveiligde berichtenuitwisseling',
  'MSH', 'MSH configuratie', 'MSH koppeling', 'MSH profiel',
  'Logius koppelvlak', 'SOAP overheid', 'WS-Security overheid',
  'overheid-API beveiliging', 'reliable messaging overheid',
  of wanneer de gebruiker beveiligde berichtenuitwisseling tussen
  overheidssystemen wil implementeren.
model: sonnet
allowed-tools:
  - WebFetch(*)
  - Bash(curl *)
  - Bash(gh api *)
  - Bash(gh search *)
---

# Digikoppeling

Implementeer beveiligde system-to-system communicatie tussen Nederlandse overheidsorganisaties.

Bron: [Logius — Digikoppeling](https://www.logius.nl/domeinen/gegevensuitwisseling/digikoppeling) | [GitHub](https://github.com/Logius-standaarden/Digikoppeling-Algemeen) | [Forum Standaardisatie](https://forumstandaardisatie.nl/open-standaarden/digikoppeling)

## Overzicht

| | |
|---|---|
| **Wat** | Standaard voor beveiligde elektronische berichtenuitwisseling tussen overheidssystemen |
| **Beheerder** | Logius (uitvoeringsorganisatie van het Ministerie van BZK) |
| **Status** | Verplicht (pas-toe-of-leg-uit) voor organisaties in het publieke domein |
| **Scope** | Closed-data verkeer: systeem-naar-systeem, geen eindgebruikersinteractie |
| **Basis** | PKIoverheid-certificaten voor authenticatie, signing en encryptie |

## Koppelvlakprofielen — vergelijking

Digikoppeling kent drie koppelvlakprofielen. Kies op basis van je use case.

| Kenmerk | REST API | WUS | ebMS2 |
|---------|----------|-----|-------|
| **Stijl** | RESTful HTTP/JSON | SOAP/XML + WS-Security | SOAP/XML + MSH (Message Service Handler) |
| **Communicatie** | Synchroon | Synchroon | Asynchroon |
| **Betrouwbaarheid** | Applicatie-niveau | Applicatie-niveau | MSH-niveau (reliable messaging) |
| **Grote berichten** | Ja (streaming/chunked) | Ja (via Grote Berichten profiel) | Ja (MSH store-and-forward) |
| **Best practices** | NL API Design Rules | WS-I Basic Profile 1.2 | OASIS ebXML Messaging 2.0 |
| **Aanbeveling** | Aanbevolen voor nieuwe koppelvlakken | Bestaande SOAP-integraties | Betrouwbare asynchrone uitwisseling |

## Profielkeuze — beslisboom

```
Nieuw koppelvlak?
├── Ja → Synchroon request-response voldoende?
│   ├── Ja → REST API profiel (aanbevolen)
│   └── Nee → Gegarandeerde aflevering nodig?
│       ├── Ja → ebMS2 profiel
│       └── Nee → REST API profiel met async patroon
└── Nee → Bestaand SOAP-koppelvlak?
    ├── Ja → WUS profiel (onderhoud)
    └── Nee → Bestaand MSH-koppelvlak → ebMS2 profiel (onderhoud)
```

## REST API profiel

Het REST API profiel volgt de NL API Design Rules en gebruikt TLS met PKIoverheid client-certificaten voor authenticatie.

### Python voorbeeld met httpx en client-certificaat

```python
import httpx

# PKIoverheid client-certificaat voor mutual TLS
client_cert = ("client.crt", "client.key")
ca_bundle = "/etc/ssl/certs/staat-der-nederlanden-root.pem"

client = httpx.Client(
    cert=client_cert,
    verify=ca_bundle,
    headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
    },
    timeout=30.0,
)

# Voorbeeld: opvragen gegevens bij andere overheidsorganisatie
response = client.get(
    "https://api.organisatie.nl/v1/resource",
    headers={"X-Correlation-ID": "uuid-voor-traceerbaarheid"},
)
response.raise_for_status()
data = response.json()
```

### Verplichte headers (REST profiel)

| Header | Beschrijving |
|--------|-------------|
| `Content-Type` | `application/json` (verplicht bij request body) |
| `Accept` | `application/json` |
| `X-Correlation-ID` | UUID voor traceerbaarheid over ketens |

## WUS profiel

Het WUS profiel is gebaseerd op SOAP 1.1/1.2 met WS-Security en WS-Addressing. Gebruikt PKIoverheid-certificaten voor ondertekening en encryptie op berichtniveau.

### SOAP-bericht met WS-Security headers

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"
               xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"
               xmlns:wsa="http://www.w3.org/2005/08/addressing">
  <soap:Header>
    <wsa:To>https://service.organisatie.nl/wus/endpoint</wsa:To>
    <wsa:Action>urn:opvragenGegevens</wsa:Action>
    <wsa:MessageID>urn:uuid:a1b2c3d4-e5f6-7890-abcd-ef1234567890</wsa:MessageID>
    <wsse:Security soap:mustUnderstand="1">
      <wsu:Timestamp wsu:Id="TS-1">
        <wsu:Created>2026-02-27T10:00:00Z</wsu:Created>
        <wsu:Expires>2026-02-27T10:05:00Z</wsu:Expires>
      </wsu:Timestamp>
      <wsse:BinarySecurityToken
        ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3"
        EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary"
        wsu:Id="X509-1"><!-- base64-encoded PKIoverheid certificaat --></wsse:BinarySecurityToken>
      <ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
        <!-- XML Signature over Body en Timestamp -->
      </ds:Signature>
    </wsse:Security>
  </soap:Header>
  <soap:Body wsu:Id="Body-1">
    <opvragenGegevensRequest xmlns="urn:example:service">
      <identificatie>123456789</identificatie>
    </opvragenGegevensRequest>
  </soap:Body>
</soap:Envelope>
```

## ebMS2 profiel

Het ebMS2 profiel is gebaseerd op OASIS ebXML Messaging 2.0 en biedt gegarandeerde aflevering via MSH-software (MSH = Message Service Handler). De MSH verzorgt betrouwbare verzending, ontvangstbevestiging en opnieuw proberen bij fouten.

### ebMS2 MessageHeader voorbeeld

```xml
<eb:MessageHeader xmlns:eb="http://www.oasis-open.org/committees/ebxml-msg/schema/msg-header-2_0.xsd"
                  eb:version="2.0"
                  soap:mustUnderstand="1">
  <eb:From>
    <eb:PartyId eb:type="urn:osb:oin">00000001234567890000</eb:PartyId>
    <eb:Role>Zender</eb:Role>
  </eb:From>
  <eb:To>
    <eb:PartyId eb:type="urn:osb:oin">00000009876543210000</eb:PartyId>
    <eb:Role>Ontvanger</eb:Role>
  </eb:To>
  <eb:CPAId>cpa-organisatieA-organisatieB-v1</eb:CPAId>
  <eb:ConversationId>conv-2026-0001</eb:ConversationId>
  <eb:Service>urn:example:gegevensuitwisseling</eb:Service>
  <eb:Action>opvragenGegevens</eb:Action>
  <eb:MessageData>
    <eb:MessageId>msg-a1b2c3d4@organisatieA.nl</eb:MessageId>
    <eb:Timestamp>2026-02-27T10:00:00Z</eb:Timestamp>
  </eb:MessageData>
</eb:MessageHeader>
```

### CPA (Collaboration Protocol Agreement)

Een CPA is een XML-contract tussen twee partijen dat vastlegt:

- **PartyInfo**: OIN en rollen van beide partijen
- **ServiceBinding**: welke services en actions beschikbaar zijn
- **Transport**: endpoints (URL's) en transportprotocol
- **ReliableMessaging**: retries, retry-interval, acknowledgments
- **Security**: welke certificaten voor signing en encryptie

CPA's worden bilateraal uitgewisseld en geconfigureerd in de MSH-software van beide partijen.

## PKIoverheid-certificaten

Digikoppeling vereist PKIoverheid-certificaten voor alle profielen.

| Type | Gebruik | Vereist voor |
|------|---------|-------------|
| **TLS/SSL server** | HTTPS-verbinding, server-authenticatie | Alle profielen |
| **TLS/SSL client** | Mutual TLS, client-authenticatie | REST, WUS |
| **Signing** | Ondertekening van berichten | WUS, ebMS2 |
| **Encryptie** | Versleuteling van berichten (payload) | WUS, ebMS2 (optioneel) |

### Python SSLContext configuratie

```python
import ssl

def create_digikoppeling_ssl_context(
    client_cert: str,
    client_key: str,
    ca_bundle: str = "/etc/ssl/certs/staat-der-nederlanden-root.pem",
) -> ssl.SSLContext:
    """Maak een SSLContext aan voor Digikoppeling mutual TLS."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2

    # Laad PKIoverheid CA-keten voor server-verificatie
    ctx.load_verify_locations(ca_bundle)

    # Laad client-certificaat voor mutual TLS
    ctx.load_cert_chain(certfile=client_cert, keyfile=client_key)

    # Verifieer altijd het servercertificaat
    ctx.check_hostname = True
    ctx.verify_mode = ssl.CERT_REQUIRED

    return ctx
```

## Diginetwerk

Diginetwerk is het besloten netwerk voor gegevensuitwisseling tussen overheidsorganisaties.

| | |
|---|---|
| **Wat** | Besloten IP-netwerk dat overheidsorganisaties onderling verbindt |
| **Beheerder** | Logius |
| **Verplicht voor** | Rijksoverheidsorganisaties (ministeries, uitvoeringsorganisaties) |
| **Optioneel voor** | Gemeenten, provincies, waterschappen (kunnen via Diginetwerk of internet) |
| **Relatie met Digikoppeling** | Digikoppeling over Diginetwerk biedt zowel transport- als berichtbeveiliging |
| **Alternatief** | Digikoppeling via het publieke internet met mutual TLS (voor niet-Rijksoverheid) |

## OIN (Organisatie-Identificatienummer)

Het OIN is de unieke identificatie van een organisatie binnen Digikoppeling.

| | |
|---|---|
| **Formaat** | 20 cijfers (prefix + KvK-nummer of eigen nummering) |
| **Voorbeeld** | `00000001234567890000` |
| **Prefix** | `00000001` = KvK-gebaseerd, `00000002`+ = overig |
| **Registratie** | Via Logius (COR — Centraal OIN Register) |
| **Gebruik** | Identificatie in certificaten, ebMS2 PartyId, logging en autorisatie |

Het OIN wordt opgenomen in het `Subject.serialNumber`-veld van PKIoverheid-certificaten en als `PartyId` in ebMS2-berichten.

## Aansluitproces — 8 stappen

| Stap | Actie | Wie |
|------|-------|-----|
| 1 | **OIN aanvragen** bij Logius (COR) | Organisatie |
| 2 | **PKIoverheid-certificaten** aanvragen bij erkende TSP | Organisatie |
| 3 | **Koppelvlakprofiel kiezen** (REST, WUS of ebMS2) | Organisatie + ketenpartner |
| 4 | **Servicecontract opstellen** (CPA bij ebMS2, API-specificatie bij REST) | Beide partijen |
| 5 | **Netwerktoegang regelen** (Diginetwerk of internet met mTLS) | Organisatie + netwerkbeheer |
| 6 | **Software inrichten** (MSH-software bij ebMS2, API-gateway bij REST) | Organisatie |
| 7 | **Testen op pre-productieomgeving** met ketenpartner | Beide partijen |
| 8 | **Productie**: go-live en monitoring inrichten | Beide partijen |

## Implementatie-checklist

- [ ] **OIN**: OIN aangevraagd en geregistreerd in COR
- [ ] **Certificaten**: PKIoverheid-certificaten aangevraagd (TLS, signing, encryptie)
- [ ] **Profiel**: koppelvlakprofiel gekozen en afgestemd met ketenpartner
- [ ] **TLS 1.2+**: minimaal TLS 1.2 geconfigureerd, onveilige cipher suites uitgeschakeld
- [ ] **Mutual TLS**: client-certificaat configuratie getest
- [ ] **Netwerk**: Diginetwerk-aansluiting geregeld (indien Rijksoverheid)
- [ ] **CPA**: CPA uitgewisseld en geconfigureerd (alleen bij ebMS2)
- [ ] **MSH-software**: MSH-software geconfigureerd en getest (alleen bij ebMS2)
- [ ] **Foutafhandeling**: retry-logica en foutafhandeling geimplementeerd
- [ ] **Logging**: OIN-gebaseerde logging en MSH-traceerbaarheid ingericht
- [ ] **Certificaatbeheer**: verloopdatum monitoring en vernieuwingsproces ingericht
- [ ] **Pre-productie**: end-to-end test met ketenpartner succesvol afgerond

## Gerelateerde skills

| Skill | Wanneer te gebruiken |
|-------|---------------------|
| **nora-architectuur** | NORA-principes en BIO-beveiligingsnormen voor Digikoppeling-implementaties |
| **zgw-apis** | ZGW API-standaarden die over Digikoppeling REST-profiel kunnen communiceren |
| **overheid-authenticatie** | DigiD/eHerkenning voor burger- en bedrijfsauthenticatie (complementair) |
| **sociaal-domein** | Berichtenverkeer in het sociaal domein dat Digikoppeling ebMS2 gebruikt |
| **e-factureren** | E-facturering via Peppol/NLCIUS, kan over Digikoppeling worden uitgewisseld |

## Meer informatie

- [Logius — Digikoppeling](https://www.logius.nl/domeinen/gegevensuitwisseling/digikoppeling) — officieel beheerportaal
- [Digikoppeling op GitHub](https://github.com/Logius-standaarden/Digikoppeling-Algemeen) — specificaties en profielen
- [Forum Standaardisatie — Digikoppeling](https://forumstandaardisatie.nl/open-standaarden/digikoppeling) — pas-toe-of-leg-uit status
- [PKIoverheid](https://www.logius.nl/domeinen/toegang/pkioverheid) — certificaatinformatie en TSP-lijst
- [Diginetwerk](https://www.logius.nl/domeinen/gegevensuitwisseling/diginetwerk) — informatie over het besloten overheidsnetwerk
