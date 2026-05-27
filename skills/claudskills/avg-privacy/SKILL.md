---
name: avg-privacy
description: >-
  Helpt bij het bouwen van privacy-conforme systemen volgens de AVG (Algemene
  Verordening Gegevensbescherming / GDPR), Privacy by Design, Privacy by Default
  en DPIA-vereisten voor Nederlandse overheidsorganisaties. Biedt richtlijnen
  voor gegevensverwerking, rechten van betrokkenen, bewaartermijnen en
  technische privacy-maatregelen. Gebruik deze skill wanneer de gebruiker vraagt
  over 'AVG', 'GDPR', 'privacy', 'persoonsgegevens', 'personal data',
  'gegevensbescherming', 'data protection', 'Privacy by Design',
  'Privacy by Default', 'DPIA', 'gegevensbeschermingseffectbeoordeling',
  'data protection impact assessment', 'verwerkingsregister',
  'register of processing activities', 'verwerkersovereenkomst',
  'data processing agreement', 'Autoriteit Persoonsgegevens',
  'AP', 'functionaris gegevensbescherming', 'FG', 'DPO',
  'data protection officer', 'rechten betrokkenen', 'data subject rights',
  'recht op inzage', 'right of access', 'recht op vergetelheid',
  'right to erasure', 'dataportabiliteit', 'data portability',
  'dataminimalisatie', 'data minimization', 'doelbinding',
  'purpose limitation', 'bewaartermijnen', 'retention periods',
  'toestemming', 'consent', 'grondslag verwerking', 'lawful basis',
  'pseudonimisering', 'pseudonymization', 'anonimisering', 'anonymization',
  'datalek', 'data breach', 'datalekmelding', 'breach notification',
  'BSN', 'burgerservicenummer', 'bijzondere persoonsgegevens',
  'special categories of data', 'profilering', 'profiling',
  'geautomatiseerde besluitvorming', 'automated decision-making',
  of wanneer de gebruiker een systeem privacy-conform wil ontwerpen
  of bouwen volgens de AVG en Nederlandse privacywetgeving.
model: sonnet
allowed-tools:
  - WebFetch(*)
  - Bash(gh api *)
  - Bash(gh search *)
---

# AVG (GDPR) — Privacy by Design voor de overheid

Ontwerp en bouw privacy-conforme overheidssystemen conform de Algemene Verordening Gegevensbescherming (AVG/GDPR) en Nederlandse privacywetgeving.

Bron: [Autoriteit Persoonsgegevens](https://www.autoriteitpersoonsgegevens.nl/) | [AVG-tekst (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | [UAVG](https://wetten.overheid.nl/BWBR0040940)

## Kernprincipes (Art. 5 AVG)

| Principe | Beschrijving | Implementatie |
|----------|-------------|---------------|
| **Rechtmatigheid** | Verwerking op geldige grondslag | Grondslag bepalen vóór bouw |
| **Doelbinding** | Alleen voor bepaald, uitdrukkelijk doel | Doel documenteren in verwerkingsregister |
| **Dataminimalisatie** | Alleen noodzakelijke gegevens | Elk veld kritisch toetsen op noodzaak |
| **Juistheid** | Gegevens actueel en correct houden | Correctiemogelijkheid inbouwen |
| **Opslagbeperking** | Niet langer bewaren dan nodig | Bewaartermijnen per gegevenstype definiëren |
| **Integriteit en vertrouwelijkheid** | Passende beveiliging | Encryptie, toegangscontrole, logging |
| **Verantwoordingsplicht** | Compliance aantoonbaar | Documentatie, audits, DPIA's |

## Grondslagen voor verwerking (Art. 6 AVG)

| Grondslag | Wanneer toepasbaar | Overheid |
|-----------|-------------------|----------|
| **a) Toestemming** | Vrije, specifieke, geïnformeerde, ondubbelzinnige wilsuiting | Beperkt bruikbaar bij overheid (machtsverhouding) |
| **b) Overeenkomst** | Noodzakelijk voor uitvoering overeenkomst | Bijv. bij subsidieovereenkomst |
| **c) Wettelijke verplichting** | Verwerking is wettelijk verplicht | Meest gebruikte grondslag bij overheid |
| **d) Vitaal belang** | Bescherming van leven | Noodsituaties |
| **e) Publieke taak** | Noodzakelijk voor taak van algemeen belang / openbaar gezag | Primaire grondslag voor overheidstaken |
| **f) Gerechtvaardigd belang** | Belang weegt zwaarder dan privacy | **Niet beschikbaar** voor overheid bij uitoefening taken |

**Let op:** Overheidsorganisaties gebruiken primair grondslag **(c)** of **(e)**. Toestemming (a) is bijna nooit een geschikte grondslag vanwege de ongelijke machtsverhouding.

## Rechten van betrokkenen

| Recht | Art. | Implementatie |
|-------|------|---------------|
| **Informatie** | 13, 14 | Privacyverklaring bij gegevensverzameling |
| **Inzage** | 15 | API/functionaliteit om eigen gegevens op te vragen |
| **Rectificatie** | 16 | Mogelijkheid om onjuiste gegevens te corrigeren |
| **Verwijdering** | 17 | Verwijderfunctionaliteit (met uitzondering voor wettelijke plichten) |
| **Beperking** | 18 | Markering om verwerking tijdelijk te stoppen |
| **Dataportabiliteit** | 20 | Export in machineleesbaar formaat (JSON, CSV) |
| **Bezwaar** | 21 | Mogelijkheid om bezwaar te maken tegen verwerking |
| **Geautomatiseerde besluiten** | 22 | Recht op menselijke tussenkomst bij geautomatiseerde besluiten |

### Reactietermijnen

| Verzoek | Termijn | Verlenging |
|---------|---------|-----------|
| Standaard | 1 maand | Max 2 maanden extra bij complexiteit |
| Kosten | Gratis | Vergoeding mogelijk bij kennelijk ongegrond/buitensporig |

## DPIA — Gegevensbeschermingseffectbeoordeling

Een DPIA is **verplicht** wanneer een verwerking waarschijnlijk een hoog risico inhoudt (Art. 35 AVG).

### Wanneer verplicht?

| Criterium | Voorbeeld |
|-----------|-----------|
| Systematische en uitgebreide beoordeling van personen | Profilering, credit scoring |
| Grootschalige verwerking bijzondere gegevens | Medische dossiers, strafrechtelijke gegevens |
| Grootschalige stelselmatige monitoring | Cameratoezicht, internetmonitoring |
| **Twee of meer criteria AP-lijst** | Kwetsbare personen + grootschalig + nieuwe technologie |

**AP-criteria (minimaal 2 = DPIA verplicht):**
1. Beoordelen of profileren
2. Geautomatiseerde besluitvorming met rechtsgevolgen
3. Stelselmatige monitoring
4. Gevoelige of bijzondere gegevens
5. Grootschalige gegevensverwerking
6. Gekoppelde databases
7. Gegevens over kwetsbare personen (kinderen, werknemers, patiënten)
8. Nieuwe technologieën
9. Blokkering van een recht, dienst of contract

### DPIA-structuur

| Fase | Activiteiten |
|------|-------------|
| **1. Beschrijving** | Doel, aard, omvang en context van de verwerking |
| **2. Noodzaak en proportionaliteit** | Grondslag, doelbinding, dataminimalisatie, bewaartermijnen |
| **3. Risico-inventarisatie** | Risico's voor rechten en vrijheden van betrokkenen |
| **4. Maatregelen** | Technische en organisatorische maatregelen om risico's te mitigeren |
| **5. Restrisico** | Beoordeling restrisico; bij hoog restrisico: voorafgaande raadpleging AP |

## Bijzondere persoonsgegevens (Art. 9 AVG)

Verwerking is in beginsel **verboden**, tenzij een uitzondering van toepassing is:

| Categorie | Uitzonderingen overheid |
|-----------|------------------------|
| Ras of etnische afkomst | Alleen bij wettelijke grondslag (bijv. antidiscriminatie) |
| Politieke opvattingen | Zeer beperkt |
| Religieuze overtuiging | Zeer beperkt |
| Lidmaatschap vakbond | Personeelsadministratie |
| Genetische gegevens | Alleen bij zwaarwegend algemeen belang |
| Biometrische gegevens | Identificatiedoeleinden (bijv. paspoort) |
| Gezondheidsgegevens | Wettelijke grondslag (bijv. WMO, Jeugdwet) |
| Seksuele geaardheid | Zeer beperkt |
| Strafrechtelijke gegevens (Art. 10) | Alleen onder toezicht overheid of bij wettelijke grondslag |

### BSN (Burgerservicenummer)

| Aspect | Regel |
|--------|-------|
| **Gebruik** | Alleen toegestaan bij wettelijke grondslag (Wet algemene bepalingen BSN) |
| **Opslag** | Versleuteld opslaan; niet gebruiken als database-ID |
| **Weergave** | Nooit volledig tonen in UI; maskeer (bijv. ****1234) |
| **Logging** | BSN nooit loggen in applicatielogs |
| **Transport** | Alleen via versleutelde verbinding |

## Privacy by Design — implementatiepatronen

### 1. Dataminimalisatie

```python
# FOUT: alle velden ophalen
user = db.query("SELECT * FROM users WHERE id = ?", user_id)

# GOED: alleen noodzakelijke velden
user = db.query("SELECT name, email FROM users WHERE id = ?", user_id)
```

### 2. Pseudonimisering

```python
import hashlib
import secrets

def pseudonymize_bsn(bsn: str, salt: str) -> str:
    """Pseudonimiseer BSN met HMAC (omkeerbaar met sleutel)."""
    return hashlib.pbkdf2_hmac(
        'sha256',
        bsn.encode(),
        salt.encode(),
        iterations=100_000
    ).hex()

# Salt veilig opslaan, gescheiden van gepseudonimiseerde data
SALT = secrets.token_hex(32)
pseudo_id = pseudonymize_bsn("123456789", SALT)
```

### 3. Bewaartermijnen automatiseren

```python
from datetime import datetime, timedelta

RETENTION_POLICIES = {
    "aanvraag_data": timedelta(days=365 * 5),      # 5 jaar (Awb)
    "logging_data": timedelta(days=365),             # 1 jaar
    "analytics_data": timedelta(days=90),            # 90 dagen
    "sessie_data": timedelta(hours=24),              # 24 uur
}

def cleanup_expired_data(data_type: str):
    """Verwijder gegevens waarvan de bewaartermijn is verstreken."""
    policy = RETENTION_POLICIES[data_type]
    cutoff = datetime.utcnow() - policy
    db.execute(
        f"DELETE FROM {data_type} WHERE created_at < ?",
        cutoff
    )
```

### 4. Toegangslogging

```python
import logging

audit_logger = logging.getLogger("audit")

def log_data_access(user_id: str, resource: str, action: str, fields: list):
    """Log elke toegang tot persoonsgegevens (BIO2 8.15.01)."""
    audit_logger.info(
        "data_access",
        extra={
            "actor": user_id,
            "action": action,
            "resource": resource,
            "fields": fields,
            "timestamp": datetime.utcnow().isoformat(),
            # NOOIT persoonsgegevens zelf loggen
        }
    )
```

### 5. Consent management

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class ConsentStatus(Enum):
    GRANTED = "granted"
    WITHDRAWN = "withdrawn"

@dataclass
class ConsentRecord:
    subject_id: str
    purpose: str
    status: ConsentStatus
    granted_at: datetime
    withdrawn_at: datetime | None = None
    evidence: str = ""  # Hoe toestemming is verkregen

    def is_valid(self) -> bool:
        return self.status == ConsentStatus.GRANTED
```

## Datalek-procedure

### Meldingsplicht

| Situatie | Actie | Termijn |
|----------|-------|---------|
| Datalek geconstateerd | Melden bij AP | **72 uur** na ontdekking |
| Hoog risico voor betrokkenen | Ook melden aan betrokkenen | **Onverwijld** |
| Verwerkersovereenkomst | Verwerker meldt aan verwerkingsverantwoordelijke | **Zonder onredelijke vertraging** |

### Wat melden bij AP?

- Aard van het datalek (welke categorieën gegevens, hoeveel betrokkenen)
- Naam en contactgegevens FG/contactpunt
- Waarschijnlijke gevolgen
- Genomen en voorgestelde maatregelen

## Verwerkingsregister (Art. 30 AVG)

Elke overheidsorganisatie moet een verwerkingsregister bijhouden:

| Veld | Beschrijving |
|------|-------------|
| Naam en contactgegevens | Van de verwerkingsverantwoordelijke, FG |
| Verwerkingsdoeleinden | Specifiek en uitdrukkelijk omschreven |
| Categorieën betrokkenen | Bijv. burgers, medewerkers, klanten |
| Categorieën persoonsgegevens | Bijv. NAW, BSN, gezondheid |
| Categorieën ontvangers | Intern, extern, derde landen |
| Doorgifte buiten EU | Met vermelding van waarborgen |
| Bewaartermijnen | Per categorie gegevens |
| Beveiligingsmaatregelen | Technisch en organisatorisch |

## Implementatie-checklist

- [ ] **Grondslag bepaald**: welke AVG-grondslag geldt voor elke verwerking?
- [ ] **Verwerkingsregister**: alle verwerkingen gedocumenteerd (Art. 30)
- [ ] **DPIA**: uitgevoerd waar verplicht (Art. 35)
- [ ] **Dataminimalisatie**: alleen strikt noodzakelijke gegevens verzamelen en verwerken
- [ ] **Bewaartermijnen**: gedefinieerd per gegevenstype; automatische opschoning
- [ ] **Rechten betrokkenen**: inzage, rectificatie, verwijdering, export geïmplementeerd
- [ ] **Privacyverklaring**: helder, in begrijpelijke taal, actueel
- [ ] **Pseudonimisering**: waar mogelijk gepseudonimiseerd verwerken
- [ ] **Versleuteling**: persoonsgegevens versleuteld in opslag en transport
- [ ] **Toegangslogging**: elke toegang tot persoonsgegevens gelogd (zonder PII in logs)
- [ ] **BSN-bescherming**: alleen bij wettelijke grondslag; versleuteld; niet in logs
- [ ] **Verwerkersovereenkomst**: afgesloten met alle verwerkers (Art. 28)
- [ ] **Datalekprocedure**: procedure ingericht voor melding aan AP binnen 72 uur
- [ ] **FG betrokken**: functionaris gegevensbescherming betrokken bij ontwerp
- [ ] **Privacy by Default**: standaardinstellingen zijn de meest privacy-vriendelijke

## Gerelateerde skills

| Skill | Wanneer te gebruiken |
|-------|---------------------|
| **dpia-assessment** | Volledig DPIA uitvoeren met 7 stappen, AP-criteria, risicomatrix en rapporttemplate |
| **iama-assessment** | IAMA uitvoeren wanneer algoritmen of AI-systemen persoonsgegevens verwerken |
| **algoritmekader** | AI Act vereisten wanneer het systeem algoritmen of AI bevat |
| **overheid-authenticatie** | DigiD/eHerkenning en BSN-verwerking bij authenticatie met persoonsgegevens |
| **llm-security** | OWASP LLM Top 10, PII-filtering en output sanitization voor LLM's |
| **digitale-soevereiniteit** | CLOUD Act, soevereine hosting, BIV-classificatie voor AI-data |
| **sociaal-domein** | Privacy-eisen voor het sociaal domein (bijzondere persoonsgegevens, Suwinet) |

## Meer informatie

- [Autoriteit Persoonsgegevens](https://www.autoriteitpersoonsgegevens.nl/) | [AVG-regelhulp](https://www.autoriteitpersoonsgegevens.nl/nl/zelf-doen/avg-regelhulp)
- [AVG-tekst](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | [UAVG](https://wetten.overheid.nl/BWBR0040940)
- [DPIA-model Rijksoverheid](https://www.rijksoverheid.nl/documenten/rapporten/2017/09/29/model-gegevensbeschermingseffectbeoordeling-rijksdienst)
- [Handleiding AVG Rijksoverheid](https://www.kcbr.nl/beleid-en-regelgeving-ontwikkelen/avg)
