---
name: hva-thesis-outline
description: Converts a long source document (opdrachtbeschrijving, stage-plan, intern rapport, draft, bedrijfsbrief, onderzoeksnotities) into a properly structured afstudeerrapport-outline following the HvA HBO-ICT richtlijnen (Januari 2024). Use this skill whenever a user mentions HvA, HBO-ICT, Hogeschool van Amsterdam, afstudeerrapport, afstudeerscriptie, BSc thesis, bachelor thesis, thesis outline, afstudeeropdracht, or asks to "structure", "outline", "convert", "turn into a thesis", or "make a thesis skeleton" from any longer document. Also trigger when a student or supervisor shares a draft, stage-report, or project-brief and wants it reorganised into chapters. Produces a Dutch-language outline with the fixed sections (omslag → titelpagina → samenvatting → inhoudsopgave → inleiding → kernhoofdstukken → conclusies → aanbevelingen → bronnenlijst → bijlagen) and pulls existing content from the source into the right places.
---

# HvA HBO-ICT Afstudeerrapport — Outline Skill

## What this skill does

Given a long source document (Dutch or English), produce a **thesis outline** that
conforms to the HvA HBO-ICT "Richtlijnen Afstudeerrapport" (Januari 2024). The
output is a scaffold: each section has a heading, a brief description of what
belongs there (in Dutch, since the thesis itself is in Dutch), and any content
from the source that already fits that section is slotted in underneath.

Sections the source doesn't cover are marked explicitly so the student knows
what's still missing. The skill does **not** invent content, does not write
prose for missing sections, and does not summarise the source in the student's
voice.

## When to use

- Student or supervisor uploads a stage-plan, internal report, opdrachtbrief,
  or early draft and wants it turned into the right structure.
- A long document needs to be reorganised into the fixed HvA chapter order.
- A supervisor wants a quick "gap analysis" showing which required sections are
  already covered and which are empty.

Not for: finished theses that need proofreading, citation formatting only, or
cover-page generation alone.

## Workflow

### 1. Read the source carefully

If the source is a PDF, docx, or other binary, extract the full text first.
Read all of it before writing the outline — partial reading produces a wrong
map of what the source covers.

### 2. Classify the source

Before slotting content, identify what kind of document you are dealing with:

- **Opdrachtomschrijving / stage-brief** — usually feeds into 1.1 (context) and
  1.2 (probleemvraag); rarely has methodologie or resultaten.
- **Tussenrapport / stage-plan** — feeds inleiding + methodologie; conclusies
  usually missing.
- **Onderzoeksdraft** — may already have kernhoofdstukken; needs restructuring
  into the HvA order.
- **Bedrijfsdocumentatie** — mostly context, rarely has probleemvraag.

This classification tells you where most of the existing material will land and
which sections will be mostly `[ONTBREEKT]`.

### 3. Produce the outline

Follow the **vaste volgorde** from the richtlijnen exactly. Items in
parentheses are optional — include them as empty placeholders only if the
source mentions them.

```
1.  Omslag / voorblad
2.  Titelpagina
3.  (Voorwoord)          — alleen opnemen als de bron dit noemt
4.  Samenvatting
5.  Inhoudsopgave         — wordt automatisch gegenereerd; toon als placeholder
6.  Inleiding
7.  Kernhoofdstukken      — decimaal genummerd, begin bij hoofdstuk 2
8.  Conclusies
9.  Aanbevelingen
10. (Noten)
11. Bronnenlijst          — APA of IEEE
12. (Nawoord / reflectie)
13. (Begrippenlijst)
14. Bijlagen              — apart genummerd (Bijlage A, B, C…)
```

### 4. Content placement rules

**Each section has a fixed required-content list per the richtlijnen.** Use
these as the sub-structure:

- **Omslag/voorblad** — titel, (ondertitel), naam bedrijf, auteur, begeleiders (HvA + bedrijf).
- **Titelpagina** — alles van de omslag + studentennummer, plaats & datum, versie, onderwijsinstelling, opleiding, HvA-begeleider, bedrijfsgegevens, stageperiode. Géén citaten, géén dankwoorden.
- **Samenvatting** — max 1 pagina, bevat: onderwerp, probleemomschrijving, probleemvraag, onderzoeksmethode, belangrijkste resultaten, belangrijkste conclusies.
- **Inleiding** — aanleiding, onderwerp/context, probleemstelling, procedure, leeswijzer. Géén "ik/jij/wij".
- **Hoofdstuk 1 — Context van de opdracht**: 1.1 bedrijf/organisatie · 1.2 opdrachtomschrijving · 1.3 analyse van de opdracht · 1.4 probleemvraag · (1.5 definities) · (1.6 randvoorwaarden) · 1.7 deelvragen.
- **Hoofdstuk 2 — (Onderzoeks)methodebeschrijving en -verantwoording**: welke methoden, waarom gekozen, hoe uitgevoerd. Als AI-tools zijn gebruikt: vermeld werkwijze hier en prompts in de bijlagen.
- **Hoofdstuk 3 — Onderzoek naar hoofd- en deelvragen**: één paragraaf per deelvraag.
- **Hoofdstuk 4 — Ontwerp en realisatie** *(indien van toepassing)*: architectuur, keuzes, één voorbeeldtabel/scherm/user story in de tekst, de rest in bijlagen.
- **Hoofdstuk 5 — Testresultaten en evaluatie** *(of: analyse van resultaten)*.
- **(Hoofdstuk 6 — Implementatie / uitvoering)** *(alleen indien relevant)*.
- **Conclusies** — kort antwoord op de probleemvraag, géén nieuwe informatie, tegenwoordige tijd.
- **Aanbevelingen** — duidelijk gescheiden van conclusies; volgen uit de conclusies.
- **Bronnenlijst** — APA of IEEE, consequent één stijl; AI-gebruik wordt hier vermeld.
- **Bijlagen** — apart genummerd (A, B, C…); o.a. reflectie, onderzoeksplan, volledige user stories, prompts aan AI-tools, vragenlijsten.

### 5. Handling gaps

For every required sub-section where the source has **no** content, write:

```
[ONTBREEKT — nog te schrijven door student]
```

For optional sections the source doesn't mention, **omit them entirely**
rather than leaving empty optional sections.

For sub-sections where the source has **partial** content, place what exists
and add:

```
[AANVULLEN — bron dekt alleen X, Y mist nog]
```

### 6. Content slotting — what to pull vs. paraphrase

- **Pull verbatim**: concrete facts — company name, opdrachtgever, dates,
  technical constraints, deelvragen if explicitly phrased, named methodologies.
- **Paraphrase briefly**: long narrative passages → condense to 1–3 bullet
  points in Dutch, so the student sees what's there without it being a
  finished draft.
- **Do NOT invent**: do not extrapolate a probleemvraag if the source does
  not contain one. Do not guess methodologie. Flag as `[ONTBREEKT]`.

### 7. Voice and language

- The outline's **structural labels** (section headings, placement notes) are
  in Dutch — this is a Dutch-language thesis.
- **Pulled source content** stays in its original language inside the outline.
  If the source is English and the final thesis will be Dutch, mark these
  passages with `[VERTALEN]` so the student translates them later.
- **Never use "ik", "jij", "wij"** in the outline's structural notes (the
  richtlijnen forbid it in the thesis itself, except in voorwoord/reflectie).
- **Never write about the student in third person** either ("De
  Afstudeerder…") — this is explicitly prohibited.

### 8. Formatting conventions from the richtlijnen

The outline must itself follow the document conventions the thesis will use,
so the student can carry it straight over:

- **Decimale nummering**: `1`, `1.1`, `1.1.1` — maximum drie niveaus. No Roman numerals.
- **Geen punt of dubbele punt achter een kopje.**
- **Opsommingen**: liggende streepjes (`–` or `-`), not bullets.
- **Getallen**: getallen onder de 20 in woorden; getallen met meeteenheden, data of bedragen altijd in cijfers.
- **Bronverwijzingen**: APA **of** IEEE — kies één stijl en markeer bovenaan de bronnenlijst welke is gekozen. Meng geen stijlen.

### 9. AI-tool disclosure (verplicht per richtlijnen)

The richtlijnen require explicit transparency when AI-tools are used. If the
student used an AI tool (including this skill) for the outline or later
drafting, include in the outline:

- A note under **Hoofdstuk 2 (methoden)** describing the AI-werkwijze.
- A placeholder **Bijlage: AI-prompts en -antwoorden**.
- An APA/IEEE-style source entry for each AI-tool used.

Reference for APA-style AI citation: the HvA library's
"AI gegenereerde content in APA-stijl" page (linked in the richtlijnen).

## Output format

Produce the outline as **Markdown**, so it can be pasted into Word, Google Docs,
or opencode. Structure:

```markdown
# Afstudeerrapport — Outline

*Gegenereerd uit: [bronbestand]. Volgt richtlijnen HvA HBO-ICT, Januari 2024.*

## Dekkingsoverzicht (gap-analyse)

| Sectie | Status | Notitie |
|---|---|---|
| Samenvatting | ONTBREEKT | nog te schrijven |
| 1. Context | GEDEKT | bedrijf en opdracht aanwezig |
| 1.4 Probleemvraag | ONTBREEKT | bron noemt doel, niet de vraag |
| …etc |

---

## 1. Omslag / voorblad
…

## 2. Titelpagina
…

## 3. Samenvatting
[ONTBREEKT — nog te schrijven door student. Max 1 pagina, bevat: …]

## 4. Inleiding
…

## Hoofdstuk 1 — Context van de opdracht

### 1.1 Het bedrijf
*Uit bron:*
- …

### 1.2 Opdrachtomschrijving
*Uit bron:*
- …

### 1.3 Analyse van de opdracht
[ONTBREEKT — nog te schrijven]

### 1.4 Probleemvraag
[AANVULLEN — bron beschrijft doel maar niet de vraag zelf]

…enzovoort…
```

The **dekkingsoverzicht** at the top is mandatory — it is the supervisor's
quick look at what's done and what isn't.

## Do not

- Do not draft the thesis prose for the student. The outline is scaffolding,
  not content.
- Do not invent probleemvragen, deelvragen, methodes, or resultaten.
- Do not rewrite the richtlijnen; follow them exactly as described above.
- Do not switch citation style mid-outline.
- Do not reorder the vaste volgorde — it is fixed.
- Do not include an auto-generated full inhoudsopgave; leave it as a
  placeholder (`[Wordt automatisch gegenereerd in Word]`).

## Quick checklist before delivering the outline

- [ ] Vaste volgorde wordt exact gevolgd?
- [ ] Dekkingsoverzicht / gap-analyse aanwezig?
- [ ] Elke ontbrekende verplichte subsectie expliciet gemarkeerd als `[ONTBREEKT]`?
- [ ] Decimale nummering (max 3 niveaus) consistent?
- [ ] Geen "ik/jij/wij" in structuurnotities?
- [ ] AI-gebruik gemeld (als van toepassing)?
- [ ] Bronverwijzingsstijl APA **of** IEEE gekozen, niet gemixt?
- [ ] Bijlage-nummering apart (A, B, C…) en niet meegenummerd met hoofdstukken?
