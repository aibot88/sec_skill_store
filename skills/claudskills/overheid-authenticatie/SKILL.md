---
name: overheid-authenticatie
description: >-
  Helpt bij het implementeren van authenticatie en autorisatie voor
  overheidsdiensten met DigiD, eHerkenning, eIDAS en het Afsprakenstelsel
  Elektronische Toegangsdiensten. Biedt richtlijnen voor SAML, OpenID Connect,
  betrouwbaarheidsniveaus en BSN-verwerking. Gebruik deze skill wanneer de
  gebruiker vraagt over 'DigiD', 'eHerkenning', 'eIDAS', 'inloggen overheid',
  'authenticatie overheid', 'government authentication', 'BSN koppeling',
  'betrouwbaarheidsniveau', 'LOA', 'level of assurance', 'SAML overheid',
  'OpenID Connect overheid', 'OIDC overheid', 'Tvs', 'Toegangsverleningservice',
  'routeringsvoorziening', 'DigiD Machtigen', 'eHerkenning Machtigen',
  'machtiging', 'ketenmachtiging', 'DigiD app', 'DigiD hoog',
  'substantieel', 'hoog betrouwbaarheidsniveau',
  'Logius', 'GDI', 'Generieke Digitale Infrastructuur',
  'SAML artifact', 'SAML metadata', 'BSN ophalen',
  'pseudoniem', 'sectoraal nummer',
  of wanneer de gebruiker DigiD, eHerkenning of overheidsauthenticatie
  wil integreren in een applicatie.
model: sonnet
allowed-tools:
  - WebFetch(*)
  - Bash(gh api *)
  - Bash(gh search *)
---

# DigiD, eHerkenning & eIDAS — Overheidsauthenticatie

Implementeer veilige authenticatie voor overheidsdiensten met DigiD (burgers), eHerkenning (bedrijven) en eIDAS (Europees).

Bron: [Logius — DigiD](https://www.logius.nl/domeinen/toegang/digid) | [eHerkenning](https://www.eherkenning.nl/) | [Afsprakenstelsel ETD](https://afsprakenstelsel.etoegang.nl/)

## Overzicht authenticatiemiddelen

| Middel | Doelgroep | Beheerder | Protocol |
|--------|-----------|-----------|----------|
| **DigiD** | Burgers (BSN-houders) | Logius | SAML 2.0 / OIDC |
| **eHerkenning** | Bedrijven en organisaties | Marktpartijen (via stelsel) | SAML 2.0 / OIDC |
| **eIDAS** | EU-burgers en -bedrijven | Nationaal via eIDAS-koppelpunt | SAML 2.0 |
| **DigiD Machtigen** | Gemachtigden namens burgers | Logius | SAML 2.0 |
| **eHerkenning Machtigen** | Gemachtigden namens bedrijven | Marktpartijen | SAML 2.0 |

## Betrouwbaarheidsniveaus

### DigiD-niveaus

| Niveau | eIDAS-equivalent | Middel | Wanneer gebruiken |
|--------|-----------------|--------|-------------------|
| **Basis** | — | Gebruikersnaam + wachtwoord | Niet-gevoelige informatie |
| **Midden** | Substantieel | + SMS-verificatie of DigiD app | Standaard voor overheidsdiensten |
| **Substantieel** | Substantieel | DigiD app met ID-check | Gevoelige gegevens (medisch, financieel) |
| **Hoog** | Hoog | DigiD app met ID-check + WID-chip | Hoogste zekerheid, wettelijk vereist bij bepaalde diensten |

### eHerkenning-niveaus

| Niveau | eIDAS | Beschrijving | Voorbeeld |
|--------|-------|-------------|-----------|
| **EH1** | — | Basisregistratie | Niet-vertrouwelijke info |
| **EH2** | Laag | Verificatie via sms/e-mail | Meldingen, eenvoudige aanvragen |
| **EH2+** | Substantieel | Tweefactorauthenticatie | Standaard overheidstransacties |
| **EH3** | Substantieel | Strenger identiteitsbewijs | Financiele transacties |
| **EH4** | Hoog | Gekwalificeerd certificaat (PKI) | Juridisch bindende handelingen |

### eIDAS-niveaus (Europees)

| Niveau | Vereiste | Voorbeeld middel |
|--------|---------|-----------------|
| **Laag** | Vermindert risico op misbruik | Gebruikersnaam + wachtwoord |
| **Substantieel** | Vermindert risico op misbruik aanzienlijk | DigiD app, tweefactor |
| **Hoog** | Voorkomt misbruik | ID-kaart met chip, gekwalificeerd certificaat |

## DigiD-integratie

### Architectuur

```
Burger → Browser → Dienstverlener → Logius (DigiD) → BSN-koppelregister
                                  ↕
                          SAML 2.0 / OIDC
```

### SAML 2.0 — Aansluiting

DigiD gebruikt primair SAML 2.0 met het Artifact Binding profiel:

**Stap 1: AuthnRequest**
```xml
<samlp:AuthnRequest
  xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
  ID="_abc123"
  Version="2.0"
  IssueInstant="2026-02-25T10:00:00Z"
  Destination="https://was-preprod1.digid.nl/saml/idp/request_authentication"
  AssertionConsumerServiceURL="https://mijn-dienst.nl/saml/acs"
  ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Artifact">

  <saml:Issuer>https://mijn-dienst.nl/saml/metadata</saml:Issuer>

  <samlp:RequestedAuthnContext Comparison="minimum">
    <saml:AuthnContextClassRef>
      urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport
    </saml:AuthnContextClassRef>
  </samlp:RequestedAuthnContext>
</samlp:AuthnRequest>
```

**Stap 2: ArtifactResolve (back-channel)**
```xml
<samlp:ArtifactResolve
  xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
  ID="_def456"
  Version="2.0"
  IssueInstant="2026-02-25T10:00:05Z"
  Destination="https://was-preprod1.digid.nl/saml/idp/resolve_artifact">

  <saml:Issuer>https://mijn-dienst.nl/saml/metadata</saml:Issuer>
  <samlp:Artifact>AAQAAMh48/1oXIM+...</samlp:Artifact>
</samlp:ArtifactResolve>
```

**Stap 3: Assertion met BSN (response)**

Het BSN wordt geleverd als NameID in de SAML Assertion:
```xml
<saml:Assertion>
  <saml:Subject>
    <saml:NameID>s00000000:123456789</saml:NameID>
    <!-- sectoraal nummer : BSN -->
  </saml:Subject>
  <saml:AuthnStatement AuthnInstant="2026-02-25T10:00:03Z">
    <saml:AuthnContext>
      <saml:AuthnContextClassRef>
        urn:oasis:names:tc:SAML:2.0:ac:classes:MobileTwoFactorContract
      </saml:AuthnContextClassRef>
    </saml:AuthnContext>
  </saml:AuthnStatement>
</saml:Assertion>
```

### DigiD AuthnContextClassRef waarden

| Niveau | AuthnContextClassRef |
|--------|---------------------|
| **Basis** | `urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport` |
| **Midden** | `urn:oasis:names:tc:SAML:2.0:ac:classes:MobileTwoFactorContract` |
| **Substantieel** | `urn:oasis:names:tc:SAML:2.0:ac:classes:Smartcard` |
| **Hoog** | `urn:oasis:names:tc:SAML:2.0:ac:classes:SmartcardPKI` |

### OpenID Connect (nieuwere aansluiting)

DigiD en eHerkenning bieden ook OIDC via de Toegangsverleningservice (Tvs):

```python
# OIDC Discovery endpoint
OIDC_DISCOVERY = "https://tvs.acc.digid.nl/.well-known/openid-configuration"

# Authorization request
AUTH_URL = (
    "https://tvs.acc.digid.nl/authorize"
    "?response_type=code"
    "&client_id=mijn-dienst"
    "&redirect_uri=https://mijn-dienst.nl/callback"
    "&scope=openid+bsn"
    "&state=random-state-value"
    "&nonce=random-nonce-value"
    "&acr_values=urn:oasis:names:tc:SAML:2.0:ac:classes:MobileTwoFactorContract"
)

# Token exchange (back-channel)
import httpx

async def exchange_code(code: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://tvs.acc.digid.nl/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": "https://mijn-dienst.nl/callback",
                "client_id": "mijn-dienst",
                "client_secret": "geheim",
            },
        )
        return response.json()

# Het BSN zit in de id_token claim of via het userinfo endpoint
```

## eHerkenning-integratie

### KvK-nummer en vestigingsnummer

eHerkenning levert na authenticatie:
- **KvK-nummer**: identificatie van de organisatie
- **Vestigingsnummer**: specifieke vestiging (optioneel)
- **Pseudoniem**: uniek per dienst (als geen KvK beschikbaar)

### SAML Assertion eHerkenning

```xml
<saml:Assertion>
  <saml:Subject>
    <saml:NameID Format="urn:oasis:names:tc:SAML:2.0:nameid-format:persistent">
      pseudoniem-abc123
    </saml:NameID>
  </saml:Subject>
  <saml:AttributeStatement>
    <saml:Attribute Name="urn:etoegang:1.9:EntityConcernedID:KvKnr">
      <saml:AttributeValue>12345678</saml:AttributeValue>
    </saml:Attribute>
    <saml:Attribute Name="urn:etoegang:1.9:EntityConcernedID:Vestigingsnr">
      <saml:AttributeValue>000012345678</saml:AttributeValue>
    </saml:Attribute>
    <saml:Attribute Name="urn:etoegang:1.13:attribute:LoA">
      <saml:AttributeValue>urn:etoegang:core:assurance-class:loa3</saml:AttributeValue>
    </saml:Attribute>
  </saml:AttributeStatement>
</saml:Assertion>
```

## BSN-verwerking na authenticatie

```python
from dataclasses import dataclass

@dataclass
class AuthenticatedUser:
    bsn: str | None            # Alleen bij DigiD
    kvk_nummer: str | None     # Alleen bij eHerkenning
    betrouwbaarheidsniveau: str
    sessie_id: str

    def heeft_bsn(self) -> bool:
        return self.bsn is not None

# CRUCIAAL: BSN-bescherming na authenticatie
# 1. BSN NOOIT loggen
# 2. BSN versleuteld opslaan
# 3. BSN niet als database-ID gebruiken
# 4. BSN niet tonen in URL's
# 5. BSN maskeren in UI (****1234)
# 6. BSN alleen beschikbaar bij wettelijke grondslag (Wet algemene bepalingen BSN)
```

## Aansluitproces

### DigiD-aansluiting

| Stap | Activiteit | Doorlooptijd |
|------|-----------|-------------|
| 1 | **PKIoverheid-certificaat** aanschaffen (server + signing) | 1-2 weken |
| 2 | **Aanvraag** indienen bij Logius via Servicecentrum | 1 week |
| 3 | **Metadata** uitwisselen (SAML EntityDescriptor) | — |
| 4 | **Preprod-testen** met testomgeving | 2-4 weken |
| 5 | **Conformiteitstoets** (PEN-test + SAML-test) | 2-4 weken |
| 6 | **Productie-aansluiting** na goedkeuring | 1 week |

### Vereisten voor aansluiting

| Vereiste | Detail |
|----------|--------|
| **PKIoverheid-certificaat** | G1-certificaat voor TLS en SAML-signing |
| **Beveiligingsassessment** | PEN-test door gecertificeerde partij |
| **Toegankelijkheid** | DigiD-koppelvlak moet digitoegankelijk zijn (WCAG 2.1 AA) |
| **Privacyverklaring** | Vermelding DigiD/eHerkenning in privacyverklaring |
| **Incidentprocedure** | 24/7 bereikbaarheid bij beveiligingsincidenten |
| **SLA** | Beschikbaarheidseisen: 99,5% (DigiD), 99,2% (eHerkenning) |

## Sessiemanagement

```python
from datetime import datetime, timedelta

SESSION_CONFIG = {
    "max_session_duration": timedelta(hours=8),  # Absolute timeout
    "idle_timeout": timedelta(minutes=15),        # Inactiviteit (OWASP)
    "digid_session_max": timedelta(minutes=120),  # DigiD-specifiek advies
}

def validate_session(session: dict) -> bool:
    """Valideer sessielevensduur conform DigiD-koppelvlakeisen."""
    now = datetime.utcnow()
    created = session.get("created_at")
    last_active = session.get("last_active")

    if not created or not last_active:
        return False

    # Absolute timeout
    if now - created > SESSION_CONFIG["max_session_duration"]:
        return False

    # Idle timeout
    if now - last_active > SESSION_CONFIG["idle_timeout"]:
        return False

    return True
```

## Testomgevingen

| Omgeving | URL | Beschrijving |
|----------|-----|-------------|
| **DigiD preprod** | `was-preprod1.digid.nl` | Testomgeving met test-BSN's |
| **DigiD simulator** | Lokaal / eigen beheer | Open-source simulators beschikbaar |
| **eHerkenning preprod** | Via leverancier | Testomgeving per makelaar |
| **Tvs acceptatie** | `tvs.acc.digid.nl` | OIDC-testomgeving |

## Implementatie-checklist

- [ ] **Betrouwbaarheidsniveau**: juist niveau bepaald op basis van risicoanalyse en wettelijke eisen
- [ ] **PKIoverheid-certificaat**: geldig G1-certificaat voor TLS en SAML-signing
- [ ] **SAML/OIDC**: correct protocol geimplementeerd conform koppelvlakspecificatie
- [ ] **Metadata**: SAML EntityDescriptor correct geconfigureerd en uitgewisseld
- [ ] **BSN-bescherming**: versleuteld opgeslagen, niet gelogd, niet in URL's, gemaskeerd in UI
- [ ] **Sessiemanagement**: idle timeout (15 min) en absolute timeout geconfigureerd
- [ ] **Single Logout**: SLO geimplementeerd voor correcte sessiebeeindiging
- [ ] **Foutafhandeling**: gebruiksvriendelijke foutpagina's bij authenticatiefouten
- [ ] **Fallback**: helder proces als DigiD/eHerkenning tijdelijk niet beschikbaar is
- [ ] **Logging**: authenticatie-events loggen (ZONDER BSN of persoonsgegevens)
- [ ] **Toegankelijkheid**: inlogschermen voldoen aan WCAG 2.1 AA
- [ ] **PEN-test**: beveiligingstest door gecertificeerde partij uitgevoerd
- [ ] **Privacyverklaring**: gebruik van DigiD/eHerkenning vermeld
- [ ] **Incidentprocedure**: 24/7 bereikbaarheid voor beveiligingsincidenten ingericht

## Gerelateerde skills

| Skill | Wanneer te gebruiken |
|-------|---------------------|
| **avg-privacy** | AVG-eisen voor BSN-verwerking, verwerkingsregister, Privacy by Design |
| **dpia-assessment** | DPIA uitvoeren bij authenticatiesystemen die persoonsgegevens verwerken |
| **nora-architectuur** | BIO-beveiligingseisen en GDI-voorzieningen |
| **zgw-apis** | ZGW API-authenticatie en -autorisatie patronen |
| **digitale-soevereiniteit** | mTLS met PKIoverheid voor soevereine LLM-endpoints |
| **digitoegankelijk** | WCAG-toegankelijkheid voor inlogschermen |

## Meer informatie

- [Logius — DigiD](https://www.logius.nl/domeinen/toegang/digid) | [DigiD koppelvlakspecificatie](https://www.logius.nl/domeinen/toegang/digid/documentatie)
- [eHerkenning](https://www.eherkenning.nl/) | [Afsprakenstelsel ETD](https://afsprakenstelsel.etoegang.nl/)
- [Tvs (OIDC)](https://www.logius.nl/domeinen/toegang/toegangsverleningservice) — Toegangsverleningservice
- [eIDAS-verordening](https://eur-lex.europa.eu/eli/reg/2014/910/oj) | [eIDAS 2.0](https://eur-lex.europa.eu/eli/reg/2024/1183/oj)
- [PKIoverheid](https://www.logius.nl/domeinen/toegang/pkioverheid) — certificaateisen
- [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
