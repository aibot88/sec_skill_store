---
name: cloud-overheid
description: >-
  Helpt bij het beoordelen en implementeren van cloudoplossingen voor
  de Nederlandse overheid conform het rijksbrede cloudbeleid, BIO
  cloud-controls, SLM en de strategische leveranciersbeoordeling.
  Biedt richtlijnen voor risicoafweging, exit-strategie, datasoevereiniteit
  en compliance. Gebruik deze skill wanneer de gebruiker vraagt over
  'cloud overheid', 'cloudbeleid', 'cloud policy government',
  'SaaS overheid', 'IaaS overheid', 'PaaS overheid',
  'cloud risico', 'cloud risk assessment', 'cloud classificatie',
  'BIO cloud', 'BIO cloud controls', 'cloud beveiliging overheid',
  'cloud security government', 'cloudmigratie overheid',
  'cloud migration government', 'exit-strategie cloud',
  'vendor lock-in overheid', 'datasoevereiniteit',
  'data sovereignty', 'cloud first', 'cloud tenzij',
  'SLM', 'Strategisch Leveranciersmanagement',
  'hyperscaler overheid', 'AWS overheid', 'Azure overheid',
  'Google Cloud overheid', 'sovereign cloud',
  'EUCS', 'EU Cloud Certification Scheme',
  'Haven', 'container platform overheid',
  'Kubernetes overheid', 'multicloud overheid',
  of wanneer de gebruiker een clouddienst wil inzetten,
  beoordelen of migreren voor een overheidsorganisatie.
model: sonnet
allowed-tools:
  - WebFetch(*)
  - Bash(gh api *)
  - Bash(gh search *)
---

# Cloud Overheid — Cloudbeleid, Risicoafweging en BIO Cloud Controls

Beoordeel en implementeer cloudoplossingen voor de overheid conform het rijksbrede cloudbeleid en BIO.

Bron: [Rijkscloudbeleid](https://www.digitaleoverheid.nl/overzicht-van-alle-onderwerpen/cloud/) | [BIO](https://www.bio-overheid.nl/) | [Haven](https://haven.commonground.nl/)

## Cloudbeleid overheid

| Aspect | Detail |
|--------|--------|
| **Rijksbeleid** | "Cloud, tenzij" — cloud is de standaard tenzij er zwaarwegende redenen zijn |
| **VNG** | Gemeentelijk cloudbeleid conform BIO en Common Ground |
| **Scope** | SaaS, PaaS, IaaS en hybride omgevingen |
| **Toezicht** | CIO Rijk, BIT (Bureau ICT-toetsing) |
| **Kader** | BIO (BBN2/BBN3), NCSC-richtlijnen, AVG, AI Act |
| **EU** | EUCS (EU Cloud Certification Scheme) in ontwikkeling |

### Cloud-eerste principes

| Principe | Betekenis |
|---------|-----------|
| **Cloud, tenzij** | Gebruik cloud tenzij risico's onaanvaardbaar zijn |
| **Public, tenzij** | Gebruik public cloud tenzij data-classificatie dit niet toelaat |
| **Multicloud** | Voorkom afhankelijkheid van een enkele leverancier |
| **Open standaarden** | Gebruik open standaarden voor portabiliteit |
| **Data in EU** | Persoonsgegevens en gevoelige overheidsdata binnen de EU |

## Risicoafweging cloudmigratie

### Stap 1: Dataclassificatie

| Classificatie | Voorbeelden | Cloud-opties |
|--------------|-------------|-------------|
| **Openbaar** | Open data, publicaties | Public cloud (SaaS/IaaS) |
| **Departementaal vertrouwelijk** | Interne notities, conceptbeleid | Public cloud met encryptie |
| **Staatsgeheim - Confidentieel** | Gevoelig beleid, persoonsgegevens (bijzonder) | Private/sovereign cloud of on-premises |
| **Staatsgeheim - Geheim/Zeer geheim** | Inlichtingen, defensie | On-premises (geen cloud) |

### Stap 2: BIO-classificatie (BBN)

| BBN | Beschrijving | Cloud-eisen |
|-----|-------------|------------|
| **BBN1** | Basis | Standaard cloudbeveiliging voldoende |
| **BBN2** | Verhoogd (standaard voor overheid) | Aanvullende controls: encryptie, logging, RBAC |
| **BBN3** | Hoog | Strenge eisen: sovereign cloud, HSM, audit |

### Stap 3: Risicobeoordeling

```
Data-classificatie + BBN → Risiconiveau
    |
    +-- Laag risico → Public cloud toegestaan
    |   (open data, BBN1)
    |
    +-- Midden risico → Public cloud met maatregelen
    |   (intern, BBN2, persoonsgegevens)
    |   Maatregelen: encryptie, BYOK, EU-regio, DPA
    |
    +-- Hoog risico → Private/sovereign cloud
    |   (bijzondere persoonsgegevens, BBN3)
    |
    +-- Zeer hoog risico → Geen cloud
        (staatsgeheim)
```

## BIO cloud controls

Aanvullende BIO-maatregelen voor cloudgebruik (bovenop standaard BIO):

| Domein | Control | BBN2 | BBN3 |
|--------|---------|------|------|
| **Governance** | Cloud-exitstrategie vastgesteld | Verplicht | Verplicht |
| **Governance** | Strategisch leveranciersmanagement (SLM) | Verplicht | Verplicht |
| **Governance** | Risicoanalyse cloudgebruik | Verplicht | Verplicht |
| **Identiteit** | MFA voor cloud-beheertoegang | Verplicht | Verplicht |
| **Identiteit** | Federatieve identiteit (SSO) | Aanbevolen | Verplicht |
| **Data** | Encryptie at rest (AES-256) | Verplicht | Verplicht |
| **Data** | Encryptie in transit (TLS 1.2+) | Verplicht | Verplicht |
| **Data** | Bring Your Own Key (BYOK) | Aanbevolen | Verplicht |
| **Data** | Datalocatie EU/EER | Verplicht | Verplicht |
| **Data** | Geen toegang door buitenlandse overheden (CLOUD Act) | Risicoafweging | Verplicht |
| **Logging** | Cloudaudit-logging | Verplicht | Verplicht |
| **Logging** | SIEM-integratie | Aanbevolen | Verplicht |
| **Netwerk** | Netwerksegmentatie | Verplicht | Verplicht |
| **Netwerk** | WAF/DDoS-bescherming | Verplicht | Verplicht |
| **Continuiteit** | Backup met encryptie | Verplicht | Verplicht |
| **Continuiteit** | Multi-regio beschikbaarheid | Aanbevolen | Verplicht |
| **Supply chain** | Subverwerkers inzichtelijk | Verplicht | Verplicht |

## SaaS-beoordelingskader

```python
from dataclasses import dataclass
from enum import Enum

class Risico(Enum):
    LAAG = "laag"
    MIDDEN = "midden"
    HOOG = "hoog"
    ZEER_HOOG = "zeer_hoog"

@dataclass
class SaaSBeoordeling:
    naam: str
    leverancier: str
    dataclassificatie: str
    bbn: int
    persoonsgegevens: bool
    bijzondere_gegevens: bool
    data_in_eu: bool
    encryptie_at_rest: bool
    encryptie_in_transit: bool
    mfa_beheer: bool
    exit_strategie: bool
    verwerkersovereenkomst: bool
    subverwerkers_inzichtelijk: bool
    cloud_act_risico: bool

    @property
    def risico(self) -> Risico:
        if self.bijzondere_gegevens and not self.data_in_eu:
            return Risico.ZEER_HOOG
        if self.bbn >= 3:
            return Risico.HOOG
        if self.persoonsgegevens and (self.cloud_act_risico or not self.data_in_eu):
            return Risico.HOOG
        if self.persoonsgegevens:
            return Risico.MIDDEN
        return Risico.LAAG

    @property
    def toegestaan(self) -> bool:
        verplicht = [
            self.encryptie_at_rest,
            self.encryptie_in_transit,
            self.mfa_beheer,
            self.exit_strategie,
        ]
        if self.persoonsgegevens:
            verplicht.extend([
                self.verwerkersovereenkomst,
                self.data_in_eu,
                self.subverwerkers_inzichtelijk,
            ])
        return all(verplicht) and self.risico != Risico.ZEER_HOOG

    def rapport(self) -> str:
        status = "TOEGESTAAN" if self.toegestaan else "NIET TOEGESTAAN"
        return f"{self.naam} ({self.leverancier}): {status} - risico: {self.risico.value}"
```

## Exit-strategie

Elke cloudoplossing vereist een gedocumenteerde exit-strategie:

| Aspect | Vereiste |
|--------|---------|
| **Data-export** | Alle data exporteerbaar in open formaat (JSON, CSV, SQL) |
| **Data-verwijdering** | Leverancier verwijdert alle data na exit (bewijs) |
| **Doorlooptijd** | Maximale doorlooptijd voor migratie gedefinieerd |
| **Kosten** | Exit-kosten vooraf vastgelegd in contract |
| **Alternatief** | Ten minste 1 alternatieve leverancier geidentificeerd |
| **Portabiliteit** | Gebruik open standaarden; vermijd proprietary API's |
| **Testmigratie** | Jaarlijkse test-exit om haalbaarheid te valideren |

## Haven — Container Platform Standaard

| Aspect | Detail |
|--------|--------|
| **Wat** | Standaard voor Kubernetes-platforms bij de overheid |
| **Doel** | Portabiliteit tussen cloud- en on-premises-omgevingen |
| **Beheerder** | VNG / Common Ground |
| **Basis** | Kubernetes + aanvullende security- en compliance-eisen |
| **Certificering** | Haven-compliant platforms worden gecertificeerd |

```yaml
# Haven-compliant Kubernetes deployment voorbeeld
apiVersion: apps/v1
kind: Deployment
metadata:
  name: zaaksysteem
  labels:
    app: zaaksysteem
    haven.commonground.nl/compliant: "true"
spec:
  replicas: 2
  selector:
    matchLabels:
      app: zaaksysteem
  template:
    metadata:
      labels:
        app: zaaksysteem
    spec:
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: zaaksysteem
          image: registry.organisatie.nl/zaaksysteem:v2.1.0
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
          resources:
            limits:
              memory: "512Mi"
              cpu: "500m"
            requests:
              memory: "256Mi"
              cpu: "250m"
          ports:
            - containerPort: 8080
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
```

## Verwerkersovereenkomst cloud

| Clausule | Vereiste |
|----------|---------|
| **Doel** | Concreet beschreven; geen verwerking voor eigen doel leverancier |
| **Subverwerkers** | Lijst bijgehouden; voorafgaande toestemming bij wijziging |
| **Datalocatie** | EU/EER; expliciet benoemen welke regio's |
| **Audit** | Recht op audit door verwerkingsverantwoordelijke |
| **Datalekmelding** | Melding aan opdrachtgever binnen 24 uur (strenger dan AVG 72 uur) |
| **Einde contract** | Data-retournering en -verwijdering met bewijs |
| **Beveiliging** | Minimaal BIO BBN2; ISO 27001 certificering |

## Implementatie-checklist

- [ ] **Dataclassificatie**: alle data geclassificeerd (openbaar/vertrouwelijk/staatsgeheim)
- [ ] **BIO-classificatie**: BBN-niveau vastgesteld
- [ ] **Risicoanalyse**: cloudspecifieke risicobeoordeling uitgevoerd
- [ ] **Datalocatie**: bevestigd dat data in EU/EER wordt opgeslagen
- [ ] **Encryptie**: at rest (AES-256) en in transit (TLS 1.2+) geactiveerd
- [ ] **BYOK**: Bring Your Own Key ingericht (BBN3: verplicht)
- [ ] **MFA**: multi-factor authenticatie voor alle beheertoegang
- [ ] **Logging**: cloud-auditlogging geactiveerd en gekoppeld aan SIEM
- [ ] **Verwerkersovereenkomst**: afgesloten conform AVG Art. 28
- [ ] **Subverwerkers**: lijst inzichtelijk; wijzigingsprocedure afgesproken
- [ ] **Exit-strategie**: gedocumenteerd; data-export getest; alternatief geidentificeerd
- [ ] **DPIA**: uitgevoerd als persoonsgegevens worden verwerkt
- [ ] **SLM**: strategisch leveranciersmanagement ingericht
- [ ] **Haven**: bij Kubernetes: Haven-compliant deployment

## Gerelateerde skills

| Skill | Wanneer te gebruiken |
|-------|---------------------|
| **nora-architectuur** | BIO-beveiligingseisen en verplichte open standaarden |
| **avg-privacy** | AVG-eisen voor cloudverwerking van persoonsgegevens |
| **dpia-assessment** | DPIA uitvoeren bij cloudmigratie met persoonsgegevens |
| **gemma-common-ground** | Haven container platform en Common Ground architectuur |
| **digitale-soevereiniteit** | CLOUD Act, soevereine hosting, data residency voor AI-workloads |
| **overheid-authenticatie** | DigiD/eHerkenning in cloudomgevingen |

## Meer informatie

- [Rijkscloudbeleid](https://www.digitaleoverheid.nl/overzicht-van-alle-onderwerpen/cloud/)
- [BIO](https://www.bio-overheid.nl/) | [BIO cloudthema](https://www.bio-overheid.nl/category/cloud)
- [Haven](https://haven.commonground.nl/) — container platform standaard
- [NCSC cloudrichtlijnen](https://www.ncsc.nl/onderwerpen/public-cloud)
- [ENISA Cloud Security Guide](https://www.enisa.europa.eu/topics/cloud-and-big-data/cloud-security)
- [EUCS](https://www.enisa.europa.eu/topics/certification/enisa-cloud-services-scheme) — EU Cloud Certification Scheme
