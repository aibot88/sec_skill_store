---
name: legal-ip-software
description: "Proprietà intellettuale su software — diritto italiano ed europeo. MODO A interna: OSS compliance policy, SBOM process (SPDX/CycloneDX), IP register aziendale, invention assignment, clean room procedure, trade secret protection protocol (artt. 98-99 CPI + D.Lgs. 63/2018), AI usage policy. MODO B contrattuale: IP Assignment clausole complete, license agreement proprietaria, SaaS subscription con IP, OSS disclosure annex, AI-generated output ownership clause + training data clause, trademark license, trade secret in NDA, patent RAND/FRAND, CLA contributor. Copre LDA 633/1941 artt. 64-bis/ter/quater + art. 12-bis (dipendenti) + art. 110 (cessione), brevetti CII art. 45 CPI + EPO G 1/19 (10/3/2021), OSS SPDX/GPL/MIT/Apache2/BSL, AI-generated (Cass. 1107/2023 Biancheri + L. 132/2025 art. 25), TDM opt-out art. 70-septies LDA. Giurisprudenza chiave: Kadrey v Meta, Getty v Stability UK 4/11/2025, Bartz v Anthropic. Attivati su LDA, art. 64-bis, art. 12-bis, SIAE, CII brevetto, art. 45 CPI, SPDX, GPL, SBOM, trade secrets art. 98 CPI, Cass. 1107/2023, TDM opt-out, training data, AI-generated."
---

# legal-ip-software — Proprietà intellettuale su software

Skill specialistica per IP software. Coordinata con `legal-contratti-software-it` (clausole) e `legal-ai-act-ue` (output IA).

## Quadro normativo

### Diritto autore software — LDA 633/1941

- **Artt. 64-bis / 64-ter / 64-quater LDA** (D.Lgs. 518/1992 + Dir. 2009/24/CE)
- **Art. 12-bis** — dipendenti (datore titolare automatico diritti economici)
- **Art. 110** — cessione scritta per consulenti esterni
- **Art. 64-quater** — **decompilazione per interoperabilità NON derogabile** contrattualmente
- Durata: **70 anni** post mortem auctoris
- **SIAE Pubblico Registro Software** — non costitutivo, €126,62

### Brevetti CII (Computer-Implemented Inventions)

- **Art. 45 CPI** esclude "software in quanto tali"
- EPO Guidelines "further technical effect" richiesto
- **EPO Enlarged Board G 1/19 (10/3/2021)** — simulazioni brevettabili se producono effetto tecnico

### Segreti commerciali

- **D.Lgs. 63/2018** + **artt. 98-99 CPI**
- Requisiti: segretezza, valore economico, **misure ragionevoli di protezione**
- **Art. 121-ter CPI** — poteri di secretazione in processo

### OSS (Open Source Software)

- **Copyleft forte**: GPL, AGPL
- **Permissive**: MIT, Apache 2.0, BSD, ISC
- **Source-available NON OSS**: BSL (Business Source License), SSPL
- **Incompatibilità nota**: GPL2 + Apache 2.0 (risolta GPL3)

### AI-generated ownership

- **Cass. civ. I ord. 1107/2023 Biancheri**: tutela **solo se apporto umano prevalente**
- **L. 132/2025 art. 25** — coerente con orientamento italiano
- **Nuovo art. 70-septies LDA** — TDM con regime **opt-out**

### Contenzioso internazionale IA

- **Kadrey v. Meta** (N.D. Cal. 2025) — fair use
- **Getty v. Stability UK** [2025] EWHC 2863 (Ch) — 4/11/2025
- **Bartz v. Anthropic** — **$1.5B settlement** 2025
- **NYT v. OpenAI** — pending

## Modalità A — Interna

Templates:
- `oss-compliance-policy.md`
- `sbom-process.md` (SPDX/CycloneDX)
- `ip-register-aziendale.md`
- `invention-assignment-dipendenti.md` (art. 12-bis)
- `clean-room-procedure.md`
- `trade-secret-protection-protocol.md` (artt. 98-99 CPI)
- `ai-usage-policy-interna.md`

## Modalità B — Contrattuale

Templates:
- `ip-assignment-clause.md` (art. 110 LDA)
- `license-agreement-proprietaria.md`
- `saas-subscription-ip.md`
- `oss-disclosure-annex.md`
- `ai-generated-output-ownership.md`
- `training-data-clause.md` (no-training / opt-in)
- `trademark-license.md`
- `trade-secret-nda.md`
- `patent-rand-frand.md`
- `cla-contributor.md`

## Script specifici

- `scripts/license_compatibility_checker.py` — SPDX-based con COPYLEFT_LICENSES + INCOMPATIBLE_PAIRS
- `scripts/copyright_notice_generator.py`
- `scripts/sbom_analyzer.py` — SPDX + CycloneDX
- `scripts/trademark_search_helper.py` — EUIPO + UIBM + WIPO

**MVP v0.2.0**: stub `{"status": "TODO Fase 2"}`.

## Output strutturato

```xml
<output_ip>
  <tipologia>copyright_sw|brevetto_CII|trade_secret|trademark|oss_compliance|ai_ownership</tipologia>
  <rischi_licenza>copyleft|incompatibilità|missing_attribution</rischi_licenza>
  <azioni_ip_register>nuove voci da registrare</azioni_ip_register>
  <contenzioso_potenziale>NYT/Getty/Kadrey analogie</contenzioso_potenziale>
</output_ip>
```

## Fonti ufficiali

- UIBM (brevetti italiani)
- EPO (brevetti europei)
- EUIPO (marchi/design UE)
- SIAE (software registry)
- WIPO (convenzioni internazionali)
- OSI (licensing definitions): https://opensource.org
- SPDX: https://spdx.dev
- CycloneDX: https://cyclonedx.org
- OpenSSF: https://openssf.org

## Dipendenze

`depends_on: [legal-common-ita, legal-contratti-software-it]`
