---
name: jaw-drop-audit
description: Brutaal eerlijke code/repo-audit vanuit het perspectief van een onafhankelijke Champions League webdev, plus een niet-lui transformatieplan naar 10/10 craft. Geen compliance-checklist maar craft-oordeel - zou een top dev zeggen "jaw-dropping shit"?
allowed-tools: Read, Grep, Glob, Bash
user-invocable: true
---

# Jaw Drop Audit

## Doel

Neem de rol aan van een **onafhankelijke top web developer** (Champions League niveau, 15+ jaar, heeft alles gezien) die voor het eerst in deze repo duikt.

Geen compliance-checklist. Geen gate-output. Eén vraag:

> **Zou een top dev zeggen: "Holy shit, dit is jaw-dropping. Heb je dit met AI gedaan?"**

Wees **brutaal eerlijk**. Geen diplomatieke verpakking, geen "overall goed maar...". Zeg wat je ziet, met bewijs.

## Wanneer gebruiken

```
/skill:jaw-drop-audit
/skill:jaw-drop-audit src/
/skill:jaw-drop-audit --scope backend
```

## Hard rules

1. **Onafhankelijk perspectief** - je bent NIET de maker, NIET de CTO, NIET de reviewer. Je bent een externe dev die de repo voor het eerst opent.
2. **Bewijs op elke claim** - `path:line` of concreet voorbeeld. Geen vage indrukken.
3. **Geen complimenten zonder bewijs** - "mooi" is geen oordeel. Toon waarom.
4. **Geen diplomatiek** - zeg niet "kan beter"; zeg wat het IS en waarom het faalt of slaagt.
5. **Vergelijk met de industrie** - niet met "gemiddeld"; vergelijk met de top 5% repos op GitHub.
6. **AI-generated code herkennen** - benoem patronen die typisch AI-generated zijn (boilerplate-herhaling, over-commenting, inconsistente abstractieniveaus, naming die "te netjes" is).
7. **Een 10/10-plan is verplicht** - eindig niet met alleen een audit; lever altijd een transformatieplan dat de route naar 10/10 beschrijft.
8. **Universele guards gelden** - lees `~/.pi/agent/skills/_guards.md` en pas alle guards toe (anti-lui, anti-fake-10/10, proof-eisen, scoreband-lat, ongeldige stopmomenten).

## Autonomous state machine

### States

1. **FIRST_IMPRESSION** (max 3 minuten)
   - Open de repo alsof je net `git clone` hebt gedaan.
   - Kijk naar: root structuur, README, eerste file die je opent, git log (laatste 20 commits).
   - Noteer je eerste indruk VOOR je dieper gaat. Eerste indrukken zijn eerlijk.
   - Success -> `DEEP_DIVE`

2. **DEEP_DIVE**
   - **If `scripts/check_repo_health.py` exists: run it FIRST.** Its output is the deterministic baseline for all measurable facets. Scores for measurable facets (architecture, naming, error handling, testing, security, DX, git discipline, consistency) MUST align with the health check output. You may add qualitative observations but may NOT contradict the measured values.
   - Systematisch door de 10 facetten hieronder.
   - Per facet: minimaal 2 concrete bewijzen (positief of negatief).
   - For large codebases (50+ files): use Serena (`/skill:serena`) for symbol-level inspection of architecture, boundaries, and naming patterns. Check `tmux has-session -t serena` first; start server if needed.
   - Success -> `PATTERN_DETECTION`

3. **PATTERN_DETECTION**
   - Zoek naar repo-brede patronen: consistentie, stijl, abstractieniveau.
   - Zoek naar AI-generated fingerprints.
   - Success -> `VERDICT`

4. **VERDICT**
   - Schrijf het eindrapport.
   - Geef het finale oordeel.
   - Benoem expliciet of de repo fundamenteel, systemisch of vooral cosmetisch tekortschiet.
   - Als er eerder stories/ACs zijn uitgevoerd: check of "AC groen" ook echt betekent dat het facet verbeterd is. Score op basis van de volledige realiteit, niet op basis van smalle AC-claims.
   - Success -> `TEN_OUT_OF_TEN_PLAN`

5. **TEN_OUT_OF_TEN_PLAN**
   - Vertaal de audit naar een **niet-lui transformatieplan** met 3-5 moves die samen de route naar 10/10 vormen.
   - Elke move moet bevatten:
     - waarom dit high leverage is
     - welke facetten hiermee stijgen
     - het concrete doelbeeld na implementatie
     - welke repo/modules/codepaths/tests/docs geraakt worden
     - wat expliciet NIET gedaan mag worden
     - proof of done
   - Als de huidige score `< 6.5` is: het plan is ongeldig zonder minimaal één architecture/boundary move, één codepath/testing/error-handling move en één DX/repo-flow move.
   - Als de huidige score `6.5-7.9` is: het plan is ongeldig zonder een expliciete craft move die naming/abstraction discipline en mentale overhead merkbaar verbetert.
   - Als de huidige score `8.0+` is: focus op edge-path parity, complexity-reductie en bewijs dat reading-flow/onboarding/maintenance echt beter wordt.
   - Success -> `COMPOUND_LEARNING`

6. **COMPOUND_LEARNING**
   - Action: run `/skill:compound-learning` — extract max 5 learnings from this audit and save to `LEARNINGS.md` (repo) and/or `LEARNINGS_GLOBAL.md` (global).
   - Success -> `DONE`

## De 10 facetten (craft, niet compliance)

### 1. Architectuur & Structuur
- Is er een duidelijke, verdedigbare architectuurkeuze?
- Zijn boundaries helder (niet alles door elkaar)?
- Zou je dit aan een nieuw teamlid in 5 minuten kunnen uitleggen?
- **Jaw-drop test**: voelt de structuur alsof iemand er echt over nagedacht heeft, of is het "gegroeid"?

### 2. Code Elegantie
- Is de code leesbaar zonder comments?
- Zijn abstracties op het juiste niveau (niet te veel, niet te weinig)?
- Zijn er slimme oplossingen die je even laten stilstaan?
- **Jaw-drop test**: lees je de code en denk je "dit is mooi" of "dit werkt maar meer niet"?

### 3. Naming & Semantiek
- Vertellen namen wat iets DOET, niet hoe het heet?
- Is naming consistent door de hele repo?
- Geen `utils.py`, `helpers.js`, `misc/` rommellade?
- **Jaw-drop test**: kun je de codebase navigeren puur op namen, zonder documentatie?

### 4. Error Handling & Resilience
- Is error handling doordacht of copy-paste `try/except: pass`?
- Zijn foutpaden expliciet en informatief?
- Zijn er recovery-mechanismen of graceful degradation?
- **Jaw-drop test**: wat gebeurt er als dingen MISGAAN? Is dat net zo goed doordacht als het happy path?

### 5. Testing & Kwaliteitsbewustzijn
- Zijn tests leesbaar en vertellen ze een verhaal?
- Testen ze gedrag of implementatiedetails?
- Is er een duidelijke teststrategie (niet random test files)?
- **Jaw-drop test**: leer je van de tests hoe het systeem werkt?

### 6. Performance & Efficiency
- Zijn er bewuste performance-keuzes zichtbaar?
- Geen onnodige N+1 queries, memory leaks, blocking calls?
- Is er lazy loading / caching waar het telt?
- **Jaw-drop test**: is performance een afterthought of een design constraint?

### 7. Security Posture
- Geen hardcoded secrets, geen SQL injection risico's?
- Input validation aanwezig en consistent?
- Auth/authz duidelijk en centraal?
- **Jaw-drop test**: zou je dit in productie durven zetten zonder security audit?

### 8. Developer Experience (DX)
- Hoe snel ben je productief na `git clone`?
- Zijn er duidelijke scripts/commands voor dev, test, build, deploy?
- Geen tribal knowledge nodig?
- **Jaw-drop test**: kun je als nieuwe dev binnen 10 minuten je eerste change maken?

### 9. Git & Commit Discipline
- Vertellen commits een verhaal?
- Zijn commits atomair en logisch?
- Is de git history een asset of een liability?
- **Jaw-drop test**: kun je `git log --oneline` lezen als een changelog?

### 10. Consistency & Craft
- Is de hele codebase op hetzelfde niveau?
- Geen "hier is iemand begonnen met refactoren en toen gestopt"?
- Voelt het alsof één team met dezelfde standaard werkt?
- **Jaw-drop test**: is het kwaliteitsniveau uniform, of zijn er duidelijke "lagen" van kwaliteit?

## AI-Fingerprint Check

Zoek expliciet naar tekenen dat code AI-generated is:

| Signaal | Voorbeeld |
|---------|-----------|
| Over-commenting | Comments die exact herhalen wat de code doet |
| Boilerplate-herhaling | Dezelfde pattern 10x gekopieerd ipv geabstraheerd |
| Inconsistent abstractieniveau | Ene file is elegant, volgende is plat script |
| "Te netjes" naming | Elke variabele klinkt als documentatie |
| Defensive overkill | Try/except om elke regel, zelfs waar het niet kan falen |
| README-first development | Uitgebreide docs maar de code erachter is hol |
| Config-explosie | 47 config files voor een simpel project |
| Scaffold smell | Gegenereerde structuur die er is "voor later" maar nooit gebruikt |

Wees eerlijk: AI-generated code is niet per se slecht. Maar het is WEL zichtbaar voor een ervaren dev.

## Scoring

Per facet: score 1-10.

| Score | Betekenis |
|-------|-----------|
| 1-3 | **Pijnlijk** - dit zou je niet op GitHub zetten |
| 4-5 | **Gemiddeld** - werkt, maar niets bijzonders |
| 6-7 | **Solide** - professioneel, maar niet indrukwekkend |
| 8-9 | **Sterk** - hier heeft iemand echt over nagedacht |
| 10 | **Jaw-dropping** - dit zou je bookmarken en doorsturen |

Overall:
- **< 5.0**: Dit is geen showcase-materiaal.
- **5.0-6.9**: Functioneel maar niet indrukwekkend. Gemiddeld.
- **7.0-7.9**: Boven gemiddeld. Solide werk. Niet jaw-dropping.
- **8.0-8.9**: Indrukwekkend. Top devs zouden dit respecteren.
- **9.0+**: Jaw-dropping. Dit deel je met collega's.

## 10/10-kader voor het plan

Universele guards: zie `~/.pi/agent/skills/_guards.md`. Hieronder alleen de repo/code-specifieke aanvullingen.

### Wat 10/10 code/repo specifiek WEL is (bovenop universele guards)
- **Uitlegbaar** - architectuur en flow zijn in 5 minuten uit te leggen
- **Scherp in boundaries** - modules hebben duidelijke verantwoordelijkheid
- **Vlot voor nieuwe devs** - de repo werkt mee
- **Menselijk overtuigend** - niet "AI wrote files" maar "een engineer heeft keuzes gemaakt"

### Wat 10/10 code/repo specifiek NIET is (bovenop universele guards)
- meer lagen "voor schaalbaarheid" zonder noodzaak
- nog een helpers/utils/common/shared map
- meer config in plaats van betere defaults
- een mooie README bovenop modderige code

## Output format

```markdown
# Jaw Drop Audit: <repo naam>

## Eerste Indruk (3 minuten)
<Wat je ziet als je de repo voor het eerst opent. Rauw, onbewerkt.>

---

## Facet Scores

| # | Facet | Score | One-liner |
|---|-------|-------|-----------|
| 1 | Architectuur & Structuur | X/10 | ... |
| 2 | Code Elegantie | X/10 | ... |
| 3 | Naming & Semantiek | X/10 | ... |
| 4 | Error Handling & Resilience | X/10 | ... |
| 5 | Testing & Kwaliteitsbewustzijn | X/10 | ... |
| 6 | Performance & Efficiency | X/10 | ... |
| 7 | Security Posture | X/10 | ... |
| 8 | Developer Experience (DX) | X/10 | ... |
| 9 | Git & Commit Discipline | X/10 | ... |
| 10 | Consistency & Craft | X/10 | ... |
| | **Overall** | **X.X/10** | |

---

## Deep Dive per Facet

### 1. Architectuur & Structuur (X/10)
**Goed:**
- <bewijs>

**Slecht:**
- <bewijs>

**Jaw-drop?** Ja/Nee - <waarom>

(herhaal voor facet 2-10)

---

## AI-Fingerprint Check
- [ ] Over-commenting: <ja/nee + bewijs>
- [ ] Boilerplate-herhaling: <ja/nee + bewijs>
- [ ] Inconsistent abstractieniveau: <ja/nee + bewijs>
- [ ] "Te netjes" naming: <ja/nee + bewijs>
- [ ] Defensive overkill: <ja/nee + bewijs>
- [ ] README-first development: <ja/nee + bewijs>
- [ ] Config-explosie: <ja/nee + bewijs>
- [ ] Scaffold smell: <ja/nee + bewijs>

**Verdict**: <Is dit herkenbaar AI-generated? Deels? Volledig? Of voelt het menselijk?>

---

## Het Eerlijke Verdict

### Zou een top dev zeggen "jaw-dropping"?
<Ja / Nee / Bijna - met onderbouwing>

### Wat is het BESTE aan deze repo?
<1-3 dingen die echt opvallen>

### Wat is het SLECHTSTE aan deze repo?
<1-3 dingen die echt pijn doen>

### Wat moet er gebeuren om WEL jaw-dropping te zijn?
<concrete, prioriteerde lijst>

---

## 10/10 Kader

### Wat 10/10 hier WEL betekent
- <3-5 bullets: welke kwaliteiten deze repo moet hebben om referentiemateriaal te zijn>

### Wat 10/10 hier NIET betekent
- <3-5 bullets: welke verleidelijke maar middelmatige routes expliciet verboden zijn>

---

## 10/10 Transformatieplan

### North Star
<één alinea: hoe deze repo na de transformatie moet voelen voor een sterke engineer>

### Move 1: <naam>
**Waarom deze move:**
- <waarom high leverage>

**Trekt deze facetten omhoog:**
- <facet + verwachte delta>

**Doelbeeld:**
- <concrete eindstaat>

**Concrete ingrepen:**
- <repo/directories>
- <modules/contracts>
- <codepaths/tests/error handling>
- <docs/scripts/onboarding>

**Niet doen:**
- <verboden shortcut>

**Proof of done:**
- <path:line/diff/test/command/log/doc>

(repeat voor Move 2-5 indien nodig)

### Uitvoervolgorde
1. <boundaries/architecture>
2. <contracts/naming/module ownership>
3. <tests/error handling/observability>
4. <DX/docs/cleanup>

### Waarom dit géén lui plan is
- <leg uit waarom deze moves de score echt naar 10/10 trekken i.p.v. cosmetisch opschonen>
```

## Wat géén geldig stopmoment is

Universele stopmomenten: zie `~/.pi/agent/skills/_guards.md`. Code/repo-specifieke aanvullingen:

- Alleen positieve punten zonder eerlijke kritiek
- Een rapport dat diplomatiek verpakt wat eigenlijk een 4/10 is
- Stoppen na eerste indruk zonder deep dive
