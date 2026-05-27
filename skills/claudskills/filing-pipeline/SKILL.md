---
name: filing-pipeline
description: "Kompletni pipeline pro pripravu pravniho podani. Phase 1 = Build (konsolidace, struktura, zestihleni, podpurne materialy). Phase 2 = Verify (5x seriova kontrola jinou instanci: validation, compliance, opposition, security, legal+law). Phase 3 = 5 LOCKS + send. Trigger: 'filing pipeline', 'priprav podani', 'konsoliduj', 'kontrola podani'."
---

# Filing Pipeline — Kompletni workflow pro pravni podani

Kazde podani projde VSEMI kroky. 5 nezavislych kontrol (jina instance nez autor!) musi odhalit VSE.
Kontroly jdou seriove. Kazda najde chybu → ROVNOU opravi → zapise CHANGELOG → pokracuje.

## Pouziti

Tom rekne: "priprav podani" / "filing pipeline" / "konsoliduj" / "kontrola podani"

---

## PHASE 1: BUILD (instance A)

### 1.1 Inventura
- Nacti vsechny relevantni dokumenty (drafty, verze, analyzy, podklady, Tom notes)
- Identifikuj co uz bylo odeslano (neduplicitat)
- Identifikuj vsechny prilohy, dukazy, podpurne materialy
- Vytvor PREHLED.md s mapou vsech souboru

### 1.2 Konsolidace
- Sluc vice dokumentu do jednoho (pokud je vic zdroju)
- Zachovej nejsilnejsi formulace z kazdeho zdroje
- Odstran duplicity mezi dokumenty
- Co uz bylo odeslano → jen odkaz ("viz doplneni c. 2 ze dne ...")

### 1.3 Struktura a poradi (PRAVNI ARCHITEKTURA)
Nekdo s pravnimi zkusenostmi posklada poradi informaci:

**Doporucena struktura soudniho podani:**
1. **Hlavicka** — sp.zn., ucastnici, datum, adresat, DS
2. **Uvod** — co je toto podani, pravni zaklad (§909), proc soud ma konat
3. **Nove skutecnosti** — chronologicky nebo tematicky, kazda s odkazem na § a dukaz
4. **Pravni argumentace** — § po §, s citaci ze zakona a aplikaci na pripad
5. **Dukazni navrhy** — co navrhujeme provest, co je v prilohach
6. **Petit** — co presne navrhujeme soudu rozhodnout (vykonatelne!)
7. **Prilohy** — cislovane, kazda odkazana v textu

**Umisteni petitu:** Na konci (standard CZ praxe). Ale petit musi byt JASNY — soud musi vedet co presne ma udelat.
**Fallback petit:** Vzdy primarni + subsidiarni + podpurny (3 urovne).
**Uspornost:** Kazda veta musi sdelovat soudu neco noveho. Prazdne vety ven. Opakujici se argumenty sdruzit.

### 1.4 Zestihleni (KRITICKE OTAZKY)
Pro KAZDOU vetu/odstavec:
- **Rika to soudu neco noveho?** Ne → ven
- **Musime to rict?** Je to nutne pro nas navrh? Ne → ven
- **Je to safe?** Muze nam to ublizit? Ano → ven nebo preformulovat
- **Kdybychom to smazali, ublizi to dokumentu?** Ne → ven
- **Rika to VIC nez musime?** Ano → zkratit na minimum
- **Je to v nejlepsim zajmu ditete a jeho vyvoje?** Vse v podani = pro dite, ne proti matce

### 1.5 Prilohy a podpurne materialy
```bash
python L:/LG13/app/agent/skills/filing_pipeline.py attachments --file <doc.md> --json
```
- Kazda priloha v textu = soubor na disku (a naopak)
- PDF existuji a jsou neprazdne
- Prilohy cislovany postupne

**Podpurne prilohy (forensic materialy):**
| Typ | Popis | Priklad |
|-----|-------|---------|
| Matice strachu | Tabulka: tvrzeni matky vs. dukaz vs. realita | priloha7_dukazni_mapa_strach.pdf |
| Casova osa | Timeline udalosti s datumem a zdrojem | casova_osa_brileni_kontaktu.pdf |
| Karta osob | Kdo je kdo v pripadu (role, DS, kontakt) | — |
| Karta komunikace | Prehled komunikace mezi ucastniky | priloha5_sms_komunikace.pdf |
| Karta dni | Konkretni dny s udalostmi (29.1., 7.4., ...) | — |
| Karta vztahu | Vztahy mezi osobami a institucemi | — |
| Karta pravnich okruhu | Ktere § se vztahuji ke kterym boduum | — |
| Karta souvislosti | Logicke vazby mezi tvrzenimi a dukazy | — |
| Logicka dukazova linka | Tvrzeni → dukaz → zaver (forenzni analyza) | ANALYSIS_legal_v1.md |

**Kdo produkuje forensic materialy:** Phase 1 instance (legal/strat) PRED kontrolami.

**Vystup Phase 1:** Jeden .md soubor, kompletni prilohy + podpurne materialy, PREHLED.md, CHANGELOG.txt inicializovan.

---

## PHASE 2: VERIFY (5x seriova kontrola JINOU instanci)

### KRITICKE PRAVIDLO: Phase 2 NESMI delat stejna instance jako Phase 1!

- Phase 1 (Build) = instance A
- Phase 2 (Verify) = instance B, C, D... (jina session, cisty context)
- Kazda kontrola cte CELY dokument nezavisle
- Pokud instance krouzi/halucinuje → dalsi kontrola to odhali

### SERIE, NE PARALELNE!

Kontroly jdou jedna po druhe. Kazda oprava → do dokumentu → PRED dalsi kontrolou.
1 dokument, postupne cistejsi. Zadny paralelismus.

### Kontrola NEVRACI — rovnou opravi a pokracuje

Najde chybu → OPRAVI v dokumentu → zapise do CHANGELOG → pokracuje.
NEVI jak opravit → zapise WARNING do CHANGELOG → Tom rozhodne na konci.
NIKDY "doporucuji zmenit" nebo "zvazit preformulaci" — bud oprav nebo WARNING pro Toma.

### 1 sdileny CHANGELOG.txt

Kazda kontrola pripise co nasla a co udelala:
```
[2026-04-17 14:30] VALIDATION (instance: strat)
  FOUND: Datum 32.4.2026 neexistuje (radek 45)
  FIXED: Opraveno na 30.4.2026

[2026-04-17 14:35] COMPLIANCE (instance: coder)
  FOUND: Tvrzeni "desitky milionu rocne" bez dukazu (radek 156)
  FIXED: Zmeneno na "nadstandardni zivotni uroven" + navrh dukazu
  WARNING: Tom — chceme zminovat konkretni castky? → rozhodne
```

---

### 2.1 VALIDATION (fakta + administrativa)
```bash
python L:/LG13/app/agent/skills/filing_pipeline.py fact-check --file <doc.md> --json
python L:/LG13/app/agent/skills/filing_pipeline.py admin-check --file <doc.md> --json
```
**Hleda:**
- Neplatna/neexistujici data, data v budoucnosti pro minule udalosti
- Spatna jmena, preklepy v sp.zn., DS ID
- Relativni datumy (vcera, dnes) → absolutni
- Interni markery (TODO, FIXME, DRAFT, NEPOSILAT)
- Chybejici hlavicka, podpis, datum, sp.zn., adresat
- Konzistence dat (stejny den nema 2 ruzna data)
- Font a diakritika — zadne rozbite znaky

### 2.2 COMPLIANCE + BEST INTEREST
**AI kontrola (cely text):**
- **Je to v nejlepsim zajmu ditete a jeho vyvoje?** Vsechno musi byt child-first
- **Nerikame moc?** Kazdy argument: musime ho rict? Pomaha petitu?
- **Je vse co rikame safe?** Muze nam to ublizit u soudu?
- **Kdybychom odstavec smazali — ublizi to dokumentu?** Ne → navrhnout smazani
- **Konzistence** s jiz odeslanymi dokumenty (neprotirecit si)
- **Tonalita** — zadne emocionalni slova, zadne napadeni matky, jen fakta pro soud
- **Hedging** ("pravdepodobne", "nejspis") → bud dokazat nebo vynechat
- **Fabulace** — tvrdime neco co nemame podlozeno? → CRITICAL
- Soud dostane co chce — odpoved na vyzvu, ne monolog

### 2.3 OPPOSITION (napadnutelnost protistranou)
**AI kontrola — mysli jako advokat protistrany:**
- Pro KAZDY argument: jak ho protistrana (Mgr. Flaska) napadne?
- Slaba tvrzeni bez dukazu → CRITICAL (bud doplnit dukaz nebo smazat)
- Otocitelne argumenty (muzou se pouzit proti nam) → CRITICAL
- Co protistrana rekne o nasem petitu?
- Mame fallback pokud soud nas argument odmitne?
- **Nahradni reseni** — pokud soud nedá stridavou péci, mame subsidiarni petit?
- **Dukazy** — ke kazdemu tvrzeni existuje dukaz? Je v prilohach?

### 2.4 SECURITY
**Hleda:**
- ZADNE interni poznamky, komentare, versioning v textu pro soud
- ZADNE "P1-1", "oprava bodu 18", "NEPOSILAT", changelog v textu
- ZADNE URL, file paths, system references, AI zmínky
- ZADNE informace prozrazujici strategii (co chystame dal)
- ZADNE informace o instancich, automatizaci, AI asistenci
- PDF metadata (author, creator, title) — nesmi odhalit AI/system
- **Incident 15.4.:** interni "NEPOSILAT" slo soudu
- **Incident 16.4.:** "fakticka oprava bodu 18 — telo v CR" = priznani fabrikace
- Kontrola ze v PDF neni skryty text, komentare, track changes

### 2.5 LEGAL + LAW LIBRARY
```bash
python L:/LG13/app/agent/skills/filing_pipeline.py law-check --file <doc.md> --json
```
**Pouzij law library:** `GET /pl/rag/search?q=&law=&limit=` + `master_index_all_laws.json`
**Pouzij good law.txt:** Tomovy poznamky ke klicovym paragrafum

**Hleda:**
- **Paragrafy** — vsechny § platne (novela NOZ 2026, z. 268/2025 Sb.)
- **Deprecated §** — §452 NIKDY (§465j), §76 OSR (§465j)
- **§869** — odst. 1 (pravomoc) vs odst. 2 (dusledek) — neplest!
- **§465g** — max 3 mesice od vykonatelnosti
- **Novela** — §465a-j = z. 268/2025 Sb. (ne 292/2013 bez novely!)
- **Judikatura** — spravne citovana, existuje, je relevantni
- **Formalni nalezitosti** — dle OSR/ZRS pro dany typ podani
- **Petit** — je vykonatelny? Muze soud realne naridit a vynutit?
- **Jurisdikce** — spravny soud, spravne rizeni, spravna sp.zn.
- **Precedenty** — existuji rozhodnuti na nase tema? Citujeme je?
- **Literatura** — komentarova literatura k § ktere pouzivame

---

## PHASE 2b: FIX — PRAVIDLA KONECNOSTI

Kontrola musi byt prisna ALE konecna. Zadny nekonecny loop.

### Severity
- **CRITICAL** = MUSI se opravit (spatny §, interni marker, fabulace, napadnutelny argument bez dukazu)
- **WARNING** = Tom rozhodne (hedging, tonalita, slaba tvrzeni s castecnym dukazem)
- **INFO** = jen k vedomi, NEOPRAVOVAT

### Oprava ≠ nova verze
- Oprava = minor bump (F1.0 → F1.1), JEN to co kontrola nasla
- NIKDY prepisovat cely dokument kvuli 1 chybe

### Max 2 pruchody na kontrolu
1. Kontrola najde → opravi → pokracuje
2. Recheck pokud kriticke chyby → PASS nebo eskalace Tom
3. NIKDY 3. pruchod

### Kontroly NEHLEDAJI vylepseni
- Hleda CHYBY, ne "toto by mohlo byt lepsi"
- Zlepseni obsahu = Phase 1. Phase 2 = JEN chyby.

### Celkovy flow (linearni)
```
Phase 1 (inst A) → dokument + prilohy + forensic materialy
  ↓
2.1 Validation (inst B) → cte → opravuje → CHANGELOG → dal
  ↓
2.2 Compliance (inst B) → cte → opravuje → CHANGELOG → dal
  ↓
2.3 Opposition (inst C) → cte → opravuje → CHANGELOG → dal
  ↓
2.4 Security (inst C) → cte → opravuje → CHANGELOG → dal
  ↓
2.5 Legal+Law (inst D) → cte → opravuje → CHANGELOG → dal
  ↓
Regex sanity: filing_pipeline.py full (0 tokenu)
  ↓
Phase 3 (5 LOCKS) → Tom cte CHANGELOG + dokument
```

---

## PHASE 3: 5 LOCKS + SEND

### 3.0 Final verze (F1.0)
- Oznac dokument jako F verzi
- meta.json, CHANGELOG.txt, PDF export

### 3.1 LOCK TOM — Tom precte cely dokument + CHANGELOG. Schvali obsah.
### 3.2 LOCK STRAT — konzistence, zapracovani Tom notes, neprotirecime jinym podanim
### 3.3 LOCK LEGAL — paragrafy, judikatura, diskretnost, compliance
### 3.4 LOCK T002 — datumy, prilohy = odkazum, PDF, fonty, format
### 3.5 LOCK TIME — cekaci lhuta (soud 60+ min, ASAP 5 min jen Tom)

### 3.6 Odeslani
- Matousovo rizeni = odesila VYHRADNE Tom osobne
- Ostatni = t002 po vsech locks
- `python filing_pipeline.py pre-send --draft-id <ID>`

---

## Dashboard integrace

Tlacitka v Drafty tabu (hub.html) — endpoint `POST /pl/skills/run`:
- **Full pipeline** — vsechny regex kontroly
- **Prilohy** — attachment check
- **Fakta** — fact-check
- **Admin** — admin-check
- **Pravo** — law-check
- **Strategie** — strategy/QC
- **Pre-send** — gate check

---

## Skripty a zdroje

| Skript | Typ | Co dela |
|--------|-----|--------|
| `filing_pipeline.py` | Python/regex, 0 tokenu | 6 sub-skills, okamzite |
| `legal_compliance_check.py` | AI (gpt-4.1) | Hloubkova compliance |
| `legal_risk.py` | AI | Risk assessment |
| `final_check.py` | AI | 12-krokovy final check |
| `pre_send_check.py` | Python | Gate check pred odeslanim |

| Zdroj | Cesta |
|-------|-------|
| Law library index | `master_index_all_laws.json` (4020 §) |
| Good law (Tom notes) | `good law.txt` (klicove § s poznamkami) |
| RAG endpoint | `GET /pl/rag/search?q=&law=&limit=` |
| Law library TXT | `C:\Users\tom\Documents\tmonkey_legal\Law_library\CZ_txt\` |

---

## Pravidla

1. **Vzdy VSECH 5 kontrol** — nikdy preskocit
2. **Jina instance nez autor** — kdo psal, ten nekontroluje
3. **Seriove, ne paralelne** — 1 dokument, postupne cistejsi
4. **Najdi → oprav → pokracuj** — zadne vraceni
5. **1 sdileny CHANGELOG** — kazdy pripise
6. **Interni poznamky NIKDY do textu pro soud**
7. **5 LOCKS bez vyjimky**
8. **Matousovo rizeni = Tom odesila osobne**
9. **Chyba = stop + analyza** — zadna zbrkla oprava
10. **Max 2 pruchody na kontrolu** — pak eskalace Tom
