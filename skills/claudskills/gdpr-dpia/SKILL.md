---
name: gdpr-dpia
description: >-
  Helpt bij het opstellen en reviewen van Data Protection Impact Assessments
  (DPIA) onder de AVG/GDPR. Genereert DPIA-templates, checkt verwerkingsgrondslagen,
  valideert bewaartermijnen, reviewt verwerkersovereenkomsten, en helpt bij
  het opstellen van een verwerkingsregister. Toegesneden op Nederlandse
  overheidsorganisaties met BIO2 en AP-richtlijnen.
  Gebruik deze skill wanneer de gebruiker vraagt over 'DPIA', 'GEB',
  'gegevensbeschermingseffectbeoordeling', 'privacy impact assessment', 'PIA',
  'AVG verplichtingen', 'verwerkersovereenkomst', 'verwerkingsregister',
  'verwerkingsverantwoordelijke', 'DPO', 'FG', 'functionaris gegevensbescherming',
  'grondslag verwerking', 'gerechtvaardigd belang', 'toestemming', 'bewaartermijn',
  'datalek melden', 'Autoriteit Persoonsgegevens', 'AP boete', 'privacy by design',
  'privacy by default', 'gegevensminimalisatie', 'doelbinding',
  'bijzondere persoonsgegevens', 'BSN', 'doorgifte derde landen',
  of wanneer de gebruiker gegevensbescherming wil implementeren voor een systeem.
model: sonnet
allowed-tools:
  - WebFetch(*)
---

# GDPR / AVG — Data Protection Impact Assessment Helper

Ondersteunt bij het opstellen, reviewen en valideren van DPIA's onder de AVG (Uitvoeringswet AVG, UAVG). Focus op Nederlandse overheidscontext met BIO2-koppeling.

**Wanneer is een DPIA verplicht?** (AVG Art. 35 + UAVG Art. 32)

Een DPIA is verplicht bij verwerkingen met **hoge privacyrisico's**, met name bij:
- Grootschalige verwerking van bijzondere persoonsgegevens (gezondheid, politiek, religie, etc.)
- Grootschalige en systematische monitoring van publiek toegankelijke ruimten (CCTV)
- Geautomatiseerde besluitvorming met rechtsgevolgen (profiling, AI-besluiten)
- Gebruik van nieuwe technologieën (AI, biometrie, IoT op grote schaal)
- Grootschalige verwerking van strafrechtelijke gegevens
- Verwerking van BSN-nummers (verplicht onder UAVG)

Bron: [Autoriteit Persoonsgegevens — DPIA](https://www.autoriteitpersoonsgegevens.nl/themas/basis-avg/praktisch-avg/gegevensbeschermingseffectbeoordeling-dpia) | [AVG Art. 35](https://gdpr-info.eu/art-35-gdpr/)

## DPIA Kernvragen (AP-lijst)

De Autoriteit Persoonsgegevens hanteert deze kernvragen. Beantwoord alle:

| # | Vraag | Concrete invulling |
|---|-------|-------------------|
| **P1** | **Doel**: Waarom worden persoonsgegevens verwerkt? | Specifiek, expliciet en gerechtvaardigd doel. NIET "voor marketing en optimalisatie" |
| **P2** | **Grondslag**: Wat is de wettelijke basis? | Een van de 6 grondslagen: toestemming, overeenkomst, wettelijke verplichting, vitaal belang, publieke taak, gerechtvaardigd belang (NIET voor overheid bij publieke taak) |
| **P3** | **Beoordeling noodzaak en evenredigheid**: Zijn de gegevens noodzakelijk? | Data minimalisatie: niet meer dan nodig; kan het doel met minder data worden bereikt? |
| **P4** | **Risico-inschatting**: Welke risico's zijn er voor betrokkenen? | Impact × Waarschijnlijkheid; scenario's voor datalek, onbevoegde toegang, misbruik |
| **P5** | **Maatregelen**: Hoe worden risico's gemitigeerd? | Technisch (encryptie, pseudonimisering, access control) + organisatorisch (beleid, training, NDA's) |

## DPIA Stappenplan

```
STAP 1: AANLEIDING & SCOPE
├── Voorgenomen verwerking beschrijven
├── Bepalen of DPIA verplicht is (AP-criteria check)
├── Scope: welke data, systemen, processen, partijen?
└── Eerst verantwoordelijke(n) en verwerker(s) identificeren

STAP 2: GEGEVENS INVENTARISEREN
├── Welke persoonsgegevens? (gewoon, bijzonder, BSN, strafrechtelijk)
├── Categorieën betrokkenen (burgers, medewerkers, patiënten, etc.)
├── Bewaartermijnen per gegevenssoort (wettelijk vereist?)
└── Bronnen van de gegevens (van betrokkene zelf, van derden?)

STAP 3: VERWERKING ANALYSEREN
├── Doel(en) van verwerking — specifiek en gerechtvaardigd?
├── Grondslag — welke AVG-grondslag en is deze valide?
├── Noodzaak — is elk gegevenstype noodzakelijk voor het doel?
└── Ontvangers — wie krijgt de data en waarom?

STAP 4: RISICO-ANALYSE
├── Dreigingen identificeren (menselijk, technisch, organisatorisch)
├── Kwetsbaarheden in kaart brengen
├── Impact per dreiging (op privacy, grondrechten, autonomie)
├── Waarschijnlijkheid per dreiging
└── Risicomatrix: Impact × Waarschijnlijkheid

STAP 5: MAATREGELEN BESCHRIJVEN
├── Technische maatregelen (encryptie, pseudonimisering, logging)
├── Organisatorische maatregelen (beleid, training, procedures)
├── Toegangsbeheer (RBAC, need-to-know, MFA)
├── Data lifecycle: hoe wordt data verwijderd?
└── Monitoring: hoe wordt compliance geborgd?

STAP 6: CONCLUSIE & GOEDKEURING
├── Resterende risico's na mitigatie
├── Aanvaardbaar of niet?
├── Advies FG/DPO
├── Goedkeuring door verwerkingsverantwoordelijke
└── Publicatie (aanbevolen, niet verplicht tenzij overheidsorgaan)
```

## Verwerkingsgrondslagen (Art. 6 AVG)

| Grondslag | Wanneer van toepassing | Valkuil |
|-----------|----------------------|---------|
| **Toestemming** (Art. 6(1)(a)) | Vrij, specifiek, geïnformeerd en ondubbelzinnig; intrekbaar | ONGELDIG bij machtsongelijkheid (werkgever-werknemer, overheid-burger = bijna nooit geldig!) |
| **Overeenkomst** (Art. 6(1)(b)) | Noodzakelijk voor uitvoering contract | Alleen strikt noodzakelijke data |
| **Wettelijke verplichting** (Art. 6(1)(c)) | Wet vereist de verwerking | Check: WELKE wet precies? |
| **Vitaal belang** (Art. 6(1)(d)) | Leven of gezondheid in direct gevaar | Alleen acute noodsituaties |
| **Publieke taak** (Art. 6(1)(e)) | Overheid voert publiekrechtelijke taak uit | Meest voorkomend voor overheid; vereist formele taaktoewijzing |
| **Gerechtvaardigd belang** (Art. 6(1)(f)) | Belang organisatie > privacy betrokkene | NIET voor overheid bij uitvoering publieke taak (alleen voor bedrijfsvoering!) |

## DPIA Checklist — Overheid

Aanvullend op de basis DPIA:

- [ ] **BIO2-maatregelen** verwerkt in DPIA (logging, encryptie, toegang, MFA)
- [ ] **IAMA of FRIA** uitgevoerd? (overlap met DPIA — niet dubbel starten)
- [ ] **FG/DPO** geraadpleegd en advies gedocumenteerd
- [ ] **Verwerkersovereenkomst** aanwezig voor elke verwerker
- [ ] **Sub-verwerkers** in kaart en geaccepteerd
- [ ] **Doorgifte derde landen**: Is er een adequaatheidsbesluit of passende waarborgen? (SCC's, BCR's)
- [ ] **Data minimisation** toegepast: welke velden zijn ECHT nodig?
- [ ] **Bewaartermijnen** per gegevenstype vastgesteld — wettelijke basis documenteren
- [ ] **Rechten van betrokkenen** geborgd (inzage, correctie, verwijdering, dataportabiliteit, bezwaar)
- [ ] **Datalekprocedure** ingericht: melden aan AP binnen 72 uur
- [ ] **Privacy by design & default** toegepast in architectuur

## Bewaartermijnen — Overheidscontext

| Type gegeven | Minimale bewaartermijn | Wettelijke basis |
|-------------|----------------------|-----------------|
| **Financiële administratie** | 7 jaar | Belastingwetgeving |
| **Personeelsdossiers** | 2 jaar na uitdiensttreding (basis) + 7 jaar fiscal | UAVG + Belastingwet |
| **Bouwvergunningen** | Altijd (onbeperkt) | Wabo / Omgevingswet |
| **BRP-gegevens** | Volgens BRP-regels, na overlijden naar archief | Wet BRP |
| **Rechtspraak uitspraken** | Permanent bewaren | Archiefwet |
| **Medische gegevens** | 15 jaar (WGBO) of 20 jaar (sommige specialismen) | WGBO |
| **Camerabeelden openbare ruimte** | Max 4 weken (tenzij incident) | AP-richtlijn |
| **Sollicitatiegegevens** | 4 weken na einde procedure (of max 1 jaar met toestemming) | AP-richtlijn |
| **Logbestanden beveiliging** | Minimaal 3 jaar (BIO2 5.28.01) | BIO2 |

**Check:** Is elke bewaartermijn wettelijk onderbouwd? "Voor de zekerheid" is geen geldige grond.

## Verwerkersovereenkomst Checklist

Elke verwerker (externe partij die persoonsgegevens verwerkt namens jou) vereist een verwerkersovereenkomst (Art. 28 AVG):

- [ ] **Voorwerp en duur** van de verwerking
- [ ] **Aard en doel** van de verwerking
- [ ] **Type persoonsgegevens** en categorieën betrokkenen
- [ ] **Instructie**: verwerker handelt ALLEEN volgens instructies verantwoordelijke
- [ ] **Geheimhouding**: verwerker en medewerkers verplicht tot geheimhouding
- [ ] **Beveiliging**: passende technische en organisatorische maatregelen (Art. 32)
- [ ] **Sub-verwerkers**: alleen met voorafgaande schriftelijke toestemming
- [ ] **Datalekken**: bijstand bij meldplicht (72u)
- [ ] **DPIA-ondersteuning**: verwerker helpt bij DPIA
- [ ] **Rechten betrokkenen**: verwerker ondersteunt bij inzage/correctie/verwijdering
- [ ] **Data verwijdering/devolutie** bij einde contract
- [ ] **Auditrecht**: verantwoordelijke mag audits uitvoeren bij verwerker
- [ ] **Doorgifte derde landen**: expliciet regelen indien van toepassing

## Verwerkingsregister Minimum Veldlijst

Het verwerkingsregister (Art. 30 AVG) is wettelijk verplicht. Per verwerking minimaal opnemen:

- Naam en contactgegevens verwerkingsverantwoordelijke (en FG)
- Doeleinden van de verwerking
- Categorieën betrokkenen
- Categorieën persoonsgegevens
- Categorieën ontvangers (incl. derde landen)
- Bewaartermijnen (of criteria)
- Technische en organisatorische beveiligingsmaatregelen
- Doorgifte aan derde landen (met waarborgen)

## Boetes

| Overtreding | Maximum | Voorbeeld |
|------------|---------|-----------|
| Basisinbreuken (Art. 83(4)) | €10M of 2% | Geen verwerkingsregister, geen FG, onvoldoende beveiliging |
| Zware inbreuken (Art. 83(5)) | €20M of 4% | Geen grondslag, schending rechten betrokkenen, doorgifte zonder waarborgen |

Voor de overheid: de AP kan ook **bestuursdwang** toepassen.

## Meer informatie

- [AP — DPIA](https://www.autoriteitpersoonsgegevens.nl/themas/basis-avg/praktisch-avg/gegevensbeschermingseffectbeoordeling-dpia)
- [AP — DPIA-model](https://www.autoriteitpersoonsgegevens.nl/documenten/model-gegevensbeschermingseffectbeoordeling-rijksdienst)
- [EUR-Lex — AVG](https://eur-lex.europa.eu/legal-content/NL/TXT/?uri=CELEX:32016R0679)
- [GDPR.eu — Complete guide](https://gdpr.eu/)
- [Rijksoverheid — Privacy by design](https://www.digitaleoverheid.nl/overzicht-van-alle-onderwerpen/privacy/)
