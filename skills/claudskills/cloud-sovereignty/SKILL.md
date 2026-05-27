---
name: cloud-sovereignty
description: >-
  Analyseert cloud-architecturen op digitale soevereiniteitsrisico's, met focus
  op de Amerikaanse CLOUD Act, FISA 702, en extraterritoriale jurisdictie.
  Identificeert blootstellingspunten in dataflows, classificeert clouddiensten
  volgens het Nederlandse cloudbeleid (BZK CIO-Rijk), en adviseert BIO2-conforme
  soevereine alternatieven. Gebruik voor technische due diligence, vendor
  assessment, en architectuurreviews van cloud-migraties en SaaS-oplossingen
  met overheidsdata.
  Gebruik deze skill wanneer de gebruiker vraagt over 'CLOUD Act', 'soevereiniteit',
  'digitale soevereiniteit', 'cloud classificatie', 'cloud governance',
  'hyperscaler risico', 'extraterritoriale jurisdictie', 'FISA 702',
  'data residency', 'data lokalisatie', 'soevereine cloud', 'BIO2 cloud',
  'overheidscloud', 'cloud vendor lock-in', 'SaaS soevereiniteit',
  'Amerikaanse cloudwetgeving', 'Patriot Act cloud', 'Executive Order 12333',
  'GAIA-X', 'Franse cloud', 'SecNumCloud', 'EUCS', 'European Cybersecurity Certification',
  'BBN cloud', 'BIO cloud maatregelen', 'vendor assessment overheid',
  'DPIA cloud', 'DPF cloud', 'Data Privacy Framework', 'Schrems cloud',
  'NDS cloud', of wanneer de gebruiker een cloud-architectuur wil toetsen
  op jurisdictierisico's of soevereine alternatieven wil evalueren.
model: sonnet
allowed-tools:
  - WebFetch(*)
  - Bash(gh api *)
  - Bash(gh search *)
---

# Cloud Sovereignty & CLOUD Act Exposure Scan

Analyseer cloud-architecturen op jurisdictierisico's en digitale soevereiniteit. Dit raamwerk combineert technische analyse van dataflows met juridische risico-classificatie volgens het Nederlandse cloudbeleid.

## Drielagenscan

Voer voor elke clouddienst of -architectuur deze scan uit:

```
LAAG 1 — INFRASTRUCTUUR: Wie beheert de fysieke infra?
  ├── Eigendom → jurisdictie van eigendom
  ├── Datacenter locatie → fysieke toegang
  └── Beheerder nationaliteit → personele jurisdictie

LAAG 2 — PLATFORM/DATA: Waar staan de data?
  ├── Data-at-rest locatie(s)
  ├── Encryptiesleutelbeheer (waar liggen de sleutels?)
  └── Backup en DR locaties

LAAG 3 — JURIDISCH/CONTRACTUEEL: Welk recht geldt?
  ├── Toepasselijk recht in contract
  ├── Geschillenbeslechting forum
  ├── Moederbedrijf jurisdictie
  └── Sub-processing keten (waar zitten subverwerkers?)
```

## CLOUD Act — Kernmechanisme

De **Clarifying Lawful Overseas Use of Data Act** (CLOUD Act, 2018) geeft Amerikaanse wetshandhaving de bevoegdheid om data op te vragen van Amerikaanse techbedrijven, **ongeacht waar ter wereld die data is opgeslagen**.

### Werkingsmechanisme

```
Amerikaanse rechtbank/rechter
  └── Uitvaardiging van "warrant" of "subpoena" aan:
      └── Elke "U.S.-based electronic communication service provider"
          └── Moet ALLE data onder zijn "possession, custody, or control" overhandigen
              └── Ongeacht serverlocatie (Amsterdam, Frankfurt, Parijs)
                  └── Bedrijf KAN weigeren, MAAR:
                      └── Comity-analyse (Art. 2703(h)):
                          ├── VS-belang bij toegang
                          ├── Buitenlands belang bij privacy
                          ├── Nationaliteit van data subject
                          └── Mogelijkheid tot conflict via diplomatie
```

### CLOUD Act vs AVG/GDPR — Direct conflict

| Aspect | CLOUD Act | AVG/GDPR (Art. 48) |
|--------|-----------|---------------------|
| Buitenlands verzoek om data | Directe toegang via warrant | **Verboden** — alleen via wederzijdse rechtshulp (MLA) of adequaatheidsbesluit |
| Reikwijdte | Alle data onder "control" van US provider | Alle persoonsgegevens in EU/over EU-burgers |
| Rechtsgrond | Soevereine VS-wet | Grondrechtenhandvest EU + AVG |
| Conflictoplossing | Comity-analyse (rechterlijke belangenafweging) | Art. 48 verbod = absoluut |

**Praktijkconflict:** Een verzoek onder CLOUD Act is expliciet verboden onder AVG Art. 48. Maar de Amerikaanse provider kan in de VS een dwangsom krijgen voor niet-naleving. Dit zet de provider klem tussen twee conflicterende wettelijke verplichtingen.

### Getroffen bedrijven

**Categorie 1 — Direct onder CLOUD Act (zeker):**
- Amazon Web Services (AWS), Microsoft Azure, Google Cloud Platform
- Microsoft 365, Google Workspace
- Salesforce, ServiceNow, Workday
- Slack, Zoom, Dropbox, Box
- Cloudflare, Akamai, Fastly

**Categorie 2 — Indirect risico (sub-processors):**
- Elk EU-bedrijf dat AWS/Azure/GCP gebruikt als IaaS/PaaS onderlaag, zelfs met Europese front-end
- Europese SaaS die op US hyperscalers draait
- Multi-cloud architecturen met US-componenten

**Categorie 3 — Vrijwel geen risico:**
- Volledig Europese owned + operated + jurisdictie stack
- Air-gapped on-premise systemen zonder US vendor dependency

## FISA 702 en Executive Order 12333

Naast de CLOUD Act bestaan er aanvullende Amerikaanse toegangsmechanismen:

### FISA Section 702 (Foreign Intelligence Surveillance Act)

- Geeft NSA/FBI bevoegdheid tot surveillance van niet-Amerikanen in het buitenland
- PRISM-programma: directe toegang tot servers van Google, Microsoft, Apple, Facebook, etc.
- Vernieuwd in 2024 (RISAA Act) tot december 2025
- Omzeilt standaard warrant-vereisten voor buitenlanddoelen

### Executive Order 12333

- Presidentiële executieve order uit 1981 die inlichtingendiensten brede bevoegdheden geeft
- Toegang tot data in transit over trans-Atlantische kabels
- Bulk data collection van niet-Amerikaanse personen
- Geen rechterlijk toezicht vereist (executieve bevoegdheid)

**Cumulatief risico:** CLOUD Act + FISA 702 + EO 12333 = een web van Amerikaanse toegangsmechanismen tot data die in Europa staat opgeslagen, zodra die data onder "control" van een Amerikaanse entiteit valt.

## EU Data Privacy Framework (DPF) — Beperkingen

Het EU-US Data Privacy Framework (juli 2023) vervangt Privacy Shield, maar:

| Beschermt tegen | Beschermt NIET tegen |
|------------------|----------------------|
| Commerciële dataverwerking zonder waarborgen | Nationale veiligheids-toegang (FISA 702, EO 12333) |
| Gebrek aan redress-mechanismen | CLOUD Act warrants |
| Onvoldoende toezicht onder Privacy Shield | Bulk surveillance door inlichtingendiensten |
| | Data onder directe "control" van US provider |

**Conclusie voor overheidsdata:** DPF is onvoldoende waarborg voor Nederlandse overheidsdata. Het lost het fundamentele jurisdictieprobleem niet op.

## EUCS — European Cybersecurity Certification Scheme

Het EU Cloud Services-certificeringsschema (EUCS) is in ontwikkeling onder de EU Cybersecurity Act (2019/881):

| Niveau | Vereisten | Soevereiniteitswaarborg |
|--------|-----------|------------------------|
| **Basic** | Basis cybersecurity | Geen jurisdictie-eisen |
| **Substantial** | Aantoonbare security controls | Beperkte jurisdictie-eisen |
| **High** | Verregaande security + **soevereiniteit** | Data uitsluitend in EU opgeslagen en verwerkt; dienstverlener vrij van niet-EU wetgeving; hoofdkantoor in EU |

**Status (mei 2026):** EUCS nog niet formeel aangenomen. Frankrijk en enkele lidstaten dringen aan op soevereiniteitseisen in 'High'-niveau. NL-positie: ondersteunt EUCS met soevereiniteitsclausules.

## NL Cloudbeleid (BZK / CIO-Rijk)

### Cloudclassificatie (BBN/BIO2-afgeleid)

| Classificatie | Data type | Toegestane cloud | Jurisdictie-eis |
|---------------|-----------|-----------------|-----------------|
| **Departementaal vertrouwelijk** | Gevoelig + niet-openbaar | Private cloud of on-premise only | NL/EU jurisdictie, geen niet-EU toegang |
| **Staatsgeheim** | Gerubriceerd | Uitsluitend on-premise, air-gapped | NL soevereiniteit |
| **Persoonsgegevens (bijzonder)** | BSN, medisch, politiek, etc. | Maximaal EU-cloud met aantoonbare waarborgen | EU jurisdictie, verwerkersovereenkomst met jurisdictiegaranties |
| **Niet-gevoelig / openbaar** | Open data, publicaties | Publieke cloud toegestaan | Risico-acceptatie vereist |

### BIO2 Cloud-eisen (5.23)

BIO2-maatregel 5.23.01 vereist een **Cloud Service Provider-beleid** voor selectie, beoordeling, beheer en beëindiging van clouddiensten. Minimumvereisten:

- [ ] CSP-beleid vastgesteld en goedgekeurd door bestuur
- [ ] Cloud risicobeoordeling per dienst (inclusief jurisdictie-analyse)
- [ ] Exitstrategie gedocumenteerd (technisch, contractueel, en financieel)
- [ ] CSP pentest rapporten en audits opgevraagd en beoordeeld
- [ ] Data lifecycle management (waar staat data, hoe wordt het verwijderd?)
- [ ] Auditrecht voor de overheidsorganisatie
- [ ] Sub-verwerkers register actueel en beoordeeld

## Sovereign Alternatieven Scan

### Tier 1 — NL Sovereign (BIO2 high-compliance)

| Oplossing | Type | Jurisdictie | BIO2-fit |
|-----------|------|-------------|----------|
| **Sovereign AI-in-a-Box** (DjimIT) | Turnkey on-prem AI stack | NL | Volledig BIO2-conform |
| **Fundaments** (voorheen Cyso) | NL Sovereign IaaS | NL | BIO2, NEN 7510, ISO 27001 |
| **BIT** | NL IaaS/cloud | NL | BIO2, NEN 7510 |
| **Leafcloud** | NL IaaS (warmtepomp-datacenters) | NL | ISO 27001 |
| **TuxCare** (CloudLinux) | Secure Linux infra | US met EU-entiteiten | Beperkt |

### Tier 2 — EU Sovereign (GDPR + grotendeels NL-cloudbeleid)

| Oplossing | Type | Jurisdictie | Aandachtspunt |
|-----------|------|-------------|---------------|
| **OVHcloud** | EU hyperscaler-alternatief | Frankrijk | SecNumCloud gecertificeerd, geen US entiteit |
| **IONOS Cloud** | EU IaaS | Duitsland | Geen US moeder, BSI C5 |
| **StackIT** (Schwarz Group) | EU IaaS | Duitsland/Duits recht | Lidl/Kaufland moeder |
| **Elastx** | SE IaaS | Zweden | GDPR-compliant, geen US |
| **UpCloud** | FI IaaS | Finland | GDPR, Helsinki HQ |
| **Exoscale** (A1 Digital) | AT/EU IaaS | Oostenrijk/Duitsland | ISO 27001, GEEN US-nexus |

### Tier 3 — EU SaaS met eigen infra

| Oplossing | Type | Jurisdictie | Aandachtspunt |
|-----------|------|-------------|---------------|
| **Nextcloud** | File sync / collab | Duitsland | Self-hosted of EU-only |
| **Hetzner** + **Nextcloud** | IaaS + SaaS | Duitsland | Combinatie volledig EU |
| **OpenProject** | Project management | Duitsland | EU SaaS of on-premise |
| **CryptPad** | Collaborative docs | Frankrijk | Zero-knowledge, open source |

### Rode vlaggen — vermijd voor gevoelige overheidsdata

| Categorie | Voorbeeld | Rode vlag |
|-----------|-----------|-----------|
| **US HQ + US jurisdictie** | AWS, Azure, GCP, Salesforce, ServiceNow, Workday, Slack, Zoom | Direct onder CLOUD Act, FISA 702 |
| **US moeder, EU-dochter** | OVH met US partners, SAP met US hosting | Dataflow-analyse vereist; contractuele barrières onvoldoende |
| **EU SaaS op US hyperscaler** | Franse GovTech op AWS | Infrastructuurlaag = blootstellingspunt |
| **Chinese hyperscalers** | Alibaba Cloud, Huawei Cloud, Tencent Cloud | Chinese inlichtingenwet 2017 (vergelijkbaar met CLOUD Act), andere jurisdictie- en ethische risico's |

## Architectuurpatronen voor soevereiniteit

### Patroon 1 — Full On-Premise (hoogste soevereiniteit)

```
Overheidsorganisatie netwerk
  └── Eigen datacenter of colocatie
      ├── OpenShift / Kubernetes bare-metal
      ├── Ceph of MinIO object storage
      ├── Self-hosted databases (PostgreSQL, etc.)
      ├── Self-hosted AI (Ollama, vLLM, LocalAI)
      └── Eigen key management (HashiCorp Vault, HSM)
```

**Fit:** Departementaal vertrouwelijk, staatsgeheim, bijzondere persoonsgegevens.

### Patroon 2 — EU IaaS + Encryptiebarrière (hoge soevereiniteit)

```
Overheidsorganisatie controleert encryptiesleutels
  └── Data-at-rest: altijd versleuteld (AES-256-GCM, sleutel NIET bij provider)
  └── EU IaaS (bijv. OVH, IONOS, BIT, Fundaments)
      ├── Bring Your Own Key (BYOK)
      ├── HSM of eigen KMS in eigen netwerk
      ├── Versleutelde backups naar apart EU-datacenter
      └── Contractuele auditrecht + exit clause
```

**Fit:** Persoonsgegevens, niet-gerubriceerd vertrouwelijk.

### Patroon 3 — SaaS Wrapper met EU Backend (gemiddelde soevereiniteit)

```
Gebruiker → EU SaaS frontend (Europese B.V.)
              └── Verwerkt metadata en applicatielaag in EU
                  └── Data storage: EU IaaS met BYOK
                      └── GEEN US sub-processors voor primaire data
```

**Fit:** Algemene bedrijfsvoering, niet-gevoelige persoonsgegevens.

## Vendor Assessment Checklist

Gebruik deze checklist bij elke cloud vendor assessment:

### Jurisdictiescan

- [ ] **Moederbedrijf**: In welk land is de ultimate parent company gevestigd?
- [ ] **Contractspartij**: Met welke entiteit is het contract? (check: lokale B.V. of US Inc.?)
- [ ] **Datacenter locaties**: In welke jurisdicties staat de data at rest en in transit?
- [ ] **Toepasselijk recht**: Welk recht is van toepassing op het contract?
- [ ] **Geschillenforum**: Waar worden geschillen beslecht (Amsterdam of Delaware?)?
- [ ] **Sub-verwerkers**: Waar zijn sub-verwerkers gevestigd? Zijn er US-entiteiten in de keten?
- [ ] **Encryptiesleutels**: Waar liggen de encryption keys? Wie beheert ze?
- [ ] **Toegang tot data**: Welke medewerkers (en in welke landen) hebben technische toegang tot data?
- [ ] **DPF-certificering**: Is het bedrijf DPF-gecertificeerd? (niet genoeg, maar wel vereist)
- [ ] **Transparantierapport**: Publiceert de vendor een transparency report over overheidsverzoeken?

### Operationele scan

- [ ] **Pentest rapporten**: Zijn recente pentest rapporten beschikbaar (max 1 jaar oud)?
- [ ] **Audits**: Zijn ISO 27001, SOC 2, of NEN 7510 certificaten actueel en inzichtelijk?
- [ ] **Incident historie**: Zijn er bekende datalekken of CLOUD Act-gerelateerde disclosures?
- [ ] **Data lifecycle**: Hoe wordt data definitief verwijderd bij contracteinde?
- [ ] **Exit plan**: Is er een gedocumenteerde exit strategy met tooling en tijdslijn?
- [ ] **Portabiliteit**: Welk formaat krijgen we onze data terug bij exit?

### Contractuele scan

- [ ] **CLOUD Act clausule**: Bevat het contract een jurisdictie- en CLOUD Act-paragraaf?
- [ ] **Auditrecht**: Hebben wij als klant recht op fysieke/logische audit?
- [ ] **Verwerkersovereenkomst**: Is er een AVG-conforme verwerkersovereenkomst?
- [ ] **Melding overheidsverzoeken**: Is de vendor verplicht om buitenlandse overheidsverzoeken te melden? (tenzij verboden door wet — CLOUD Act gag orders!)
- [ ] **Aansprakelijkheid**: Zijn er jurisdictiespecifieke aansprakelijkheidsbepalingen?
- [ ] **Garanties**: Welke garanties geeft de vendor over jurisdictie-onafhankelijkheid?

## DPIA Cloud Aanvulling

Bij een DPIA (AVG) voor clouddiensten, voeg deze cloud-specifieke analyse toe:

1. **Jurisdictie risico-analyse**: Welke landen kunnen juridisch dwingend toegang eisen tot de data?
2. **Dataflow diagram**: Fysieke en logische datastromen met jurisdictie-annotaties
3. **Encryptie-architectuur**: End-to-end encryptie met klant-gecontroleerde sleutels?
4. **Toegangsmatrix**: Wie (personen, rollen, jurisdicties) kan technisch bij de data?
5. **Restrisico**: Welk restrisico op extraterritoriale toegang blijft over na mitigatie?
6. **Acceptatie**: Is het restrisico aanvaardbaar voor de classificatie van de data?

## Specifieke Sectoren

### Rechtspraak

Data van de Rechtspraak (uitspraken, persoonsgegevens in zaken, interne deliberaties) = **maximale soevereiniteitseis**. Concreet:

- **GEEN US hyperscalers** voor primaire systemen
- **GEEN non-EU cloud** voor data met BSN, medische gegevens, strafrechtelijke data
- **On-premise of NL colocatie** voor alle kritieke rechtspraaksystemen
- Zie [rechtspraak-djimit-scheiding.md] voor belangenverstrengelingsaspecten

### Gemeenten (GEMMA)

Gemeenten verwerken BRP, BSN, WMO, jeugdzorg, schuldhulpverlening — allemaal minimaal "bijzondere persoonsgegevens":

- Clouddiensten moeten **aantoonbaar** geen US-jurisdictie-toegang hebben
- GIBIT/AGIBIT-voorwaarden toepassen met soevereiniteitsclausule
- GEMMA cloud-scan gebruiken als onderdeel van vendor assessment
- Common Ground-principe: data bij de bron, niet onnodig kopiëren naar cloud

### Zorg (NEN 7510)

Aanvullend op BIO2 en AVG: NEN 7510-certificering vereist voor cloudverwerkers in de zorg.

## NDS — Nederlandse Digitaliseringsstrategie Context

De NDS benadrukt "regie op eigen data" en "digitale autonomie" als strategische pijlers. De cloud sovereignty scan sluit aan op NDS-doelen:

- **Strategische autonomie**: verminderen afhankelijkheid van niet-EU tech monopolies
- **Publieke waarden**: data-soevereiniteit als randvoorwaarde voor democratische controle
- **Weerbare digitale infrastructuur**: niet afhankelijk van één jurisdictie voor kritieke diensten

## Meer informatie

- [CLOUD Act full text (US Congress)](https://www.congress.gov/bill/115th-congress/house-bill/4943/text)
- [FISA Section 702 — EPIC Summary](https://epic.org/fisa-section-702/)
- [EU-US Data Privacy Framework](https://www.dataprivacyframework.gov/)
- [EUCS — ENISA Cloud Certification](https://www.enisa.europa.eu/topics/cybersecurity-certification/cloud-services)
- [BZK CIO-Rijk — Cloudbeleid](https://www.digitaleoverheid.nl/overzicht-van-alle-onderwerpen/cloud/)
- [BIO2 Cloud-maatregel 5.23](https://www.bio-overheid.nl/)
- [NORA Cloud & SOA](https://www.noraonline.nl/wiki/Cloud)
- [NL NDS — Nederlandse Digitaliseringsstrategie](https://www.nldigital.nl/nederlandse-digitaliseringsstrategie/)
- [GAIA-X — European Sovereign Cloud](https://www.gaia-x.eu/)
- [SecNumCloud — ANSSI France](https://cyber.gouv.fr/actualites/le-label-secnumcloud)
- [Schrems III — NOYB](https://noyb.eu/)
