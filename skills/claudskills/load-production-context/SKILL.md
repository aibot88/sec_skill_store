---
name: load-production-context
description: Carica nel contesto corrente la Knowledge Base di produzione cinematografica (MovieMagic Scheduling + MovieMagic Budgeting + Final Draft + produzione italiana compliance + set operations + competitor landscape). Usata dall'orchestrator prima di task su moduli produzione (lib/schedule, lib/odg, lib/budget, lib/screenplay, lib/schedule/compliance) e prima di ogni sessione parlamento. Garantisce che ogni decisione architetturale sia production-aware e tracciabile a pattern MMS/MMB/FD/CCNL concreti.
---

# Skill: load-production-context

## Scopo

PunxFilm Breakdown è un'app di pre-produzione cinematografica che deve rispecchiare l'operatività reale di set italiano. Ogni feature che tocca schedule/budget/ODG/screenplay dev'essere coerente con:

- **MovieMagic Scheduling (MMS)** — industry standard stripboard/DOOD
- **MovieMagic Budgeting (MMB)** — industry standard chart of accounts
- **Final Draft (FDX)** — industry standard screenplay format
- **CCNL Troupe italiano** — turnaround 11h, meal break, overtime
- **L.977/67** — lavoro minori nello spettacolo
- **Permessi italiani** — Comune/Prefettura/Questura/ENAC/ASL/VVFF
- **Competitor landscape** — StudioBinder, Croogloo, Autodesk Flow, Yamdu, Cinelytic

Questa skill **carica in contesto** i file KB per permettere all'orchestrator (e ai subagent) di ragionare con fonti verificate invece che con training generico.

## Quando invocarmi

### Trigger manuale esplicito
- L'utente dice "load production context", "carica KB produzione", "/load-production-context"

### Trigger automatico consigliato (hook opzionale)
L'orchestrator carica questa skill **prima** di task che toccano:

- `lib/schedule/**` (incluso `lib/schedule/compliance/**`)
- `lib/odg/**`
- `lib/budget/**`
- `lib/screenplay/**`
- `lib/parsers/**` (per FDX/PDF screenplay parsing)
- `components/schedule/**`
- `components/odg/**`
- `components/budget/**`

### Trigger obbligatorio
- **Prima di ogni `/convoca-parlamento`**: così tutti i subagent del parliament ragionano allineati sulla stessa KB.
- **Prima di review architettura** che tocca il core workflow screenplay → spoglio → breakdown → PdL → DOOD → ODG → budget.
- **Prima di task di marketing/competitor analysis** che richiede visione competitor.

## Prerequisiti

- Directory `content/knowledge-base/` presente
- 8 file MD KB presenti:
  - `INDEX.md`
  - `moviemagic-scheduling.md`
  - `moviemagic-budgeting.md`
  - `final-draft-screenplay.md`
  - `produzione-italiana-compliance.md`
  - `set-operations-realtime.md`
  - `competitor-landscape.md`
  - `landing-copywriting-apple-style.md`

Se uno o più file mancano, emetto warning ma carico comunque i presenti.

## Flusso

### Step 1 — Read INDEX

Leggo `content/knowledge-base/INDEX.md` per ottenere:
- Mappa agent → KB files (quali file deve leggere quale agent)
- Convenzioni KB (version, updated, sources)
- Trigger di caricamento automatico

### Step 2 — Load all 7 domain files

Carico sequenzialmente:
1. `moviemagic-scheduling.md`
2. `moviemagic-budgeting.md`
3. `final-draft-screenplay.md`
4. `produzione-italiana-compliance.md`
5. `set-operations-realtime.md`
6. `competitor-landscape.md`
7. `landing-copywriting-apple-style.md`

**Cost stimato**: ~10-12K tokens totali (sostenibile per un contesto tipico).

**Loading selettivo**: per task puramente tech (es. refactor `lib/parsers/`), posso caricare solo i 4 file produzione core (1-4) e skippare 5-7 per risparmio token. Per task marketing, carico solo 6-7 + INDEX.

### Step 3 — Context priming

Una volta caricati, l'orchestrator **deve**:

1. **Citare almeno un pattern MMS/MMB/FD/CCNL** ogni volta che propone una decisione architetturale su moduli produzione.

2. **Usare gli Example sections** nei KB file come reference per "pattern giusto vs sbagliato" (vedi sezione "Pattern critici per tech agent" in ogni MD).

3. **Cross-reference tra file KB** quando una decisione coinvolge più domini (es. scheduling change → budget impact + compliance constraint).

4. **Aggiornare la KB** se durante il lavoro emerge un pattern produzione non ancora documentato:
   - Aggiungi entry al MD corrispondente
   - Commit separato: `docs(kb): <file> +<topic>`
   - Incrementa `version` nel header

### Step 4 — Subagent briefing

Quando invoco un subagent che dichiara nel frontmatter `reads_knowledge_base: [...]`:
- Passo in automatico i riferimenti ai MD rilevanti nel prompt
- Aspetto che il subagent citi almeno 1 KB file nella sua response (gate di qualità)

## Output

Questa skill NON produce un file output. Il suo effetto è:

1. **Contesto popolato** con KB complete (disponibile per tutti i successivi tool call)
2. **Consapevolezza operativa** — ogni decisione può essere tracciata a un pattern verificato
3. **Consistency tra subagent** — tutti ragionano sullo stesso base di conoscenza

Log info a summary-level:
- Quali file sono stati caricati (count + total size)
- Eventuali file mancanti (warning)
- Version + last updated di ogni file

## Esempi d'uso

### Esempio 1 — Prima di programmare su lib/schedule

**Utente**: "Voglio implementare il T702 Realtime recompute PdL"

**Orchestrator**:
1. Riconosce che T702 tocca `lib/schedule/**`
2. **Invoca automaticamente `/load-production-context`**
3. Ora ha in contesto le KB
4. Procede con design ragionando su:
   - MMS pattern: strip drag → DOOD auto-recompute (stable)
   - CCNL turnaround: hard constraint mai silent
   - Impact stradale: company move → calcolo cost budget (cita KB budget)
5. Giustifica scelte in terms di produzione reale, non solo code hygiene

### Esempio 2 — Prima di convocare parliament

**Utente**: "Convoca parliament 005"

**Orchestrator**:
1. **Invoca `/load-production-context`** (prerequisito)
2. Il contesto è popolato
3. Invoca `/convoca-parlamento`
4. Il parlamento-produzione-agent (e tutti i subagent che inviterà) ragionano su fonti KB verificate
5. Proposte emesse sono **production-grounded**, non astratte

### Esempio 3 — Durante code review

**Utente**: "Review questo refactor di `lib/schedule/build.ts`"

**Orchestrator**:
1. Riconosce il path `lib/schedule/**`
2. **Invoca `/load-production-context`**
3. Review il codice con lente: "questo pattern riflette MMS stripboard mechanics? Il naming è production-coherent? Le funzioni single-responsibility mirror della pipeline screenplay→breakdown→stripboard→DOOD?"

## Troubleshooting

### KB file mancante
Se un file KB non esiste:
- Emetto warning `"KB file <name> missing, reasoning may be incomplete"`
- Carico comunque i presenti
- Suggerisco di aggiungerlo in prossimo sprint (o se critico, creo stub + task in TODO_STATUS)

### KB file outdated
Se `updated` in header è >90 giorni:
- Emetto warning `"KB file <name> updated >90 days ago, may need refresh"`
- Prosegue
- Trigger opzionale skill `/refresh-kb` (T1805, future)

### Context budget
Se i KB totali + task corrente superano token budget:
- Carico priorità: INDEX + file dominio rilevante + competitor-landscape (se marketing task)
- Skippo file meno rilevanti con log warning

## Integration con CLAUDE.md

La sezione "Production Knowledge References" in `CLAUDE.md` (aggiunta in T1701.8) riferisce a questa skill come **protocollo obbligatorio** per task produzione. L'orchestrator deve:

- Caricare KB prima di task produzione (automatico o manuale)
- Citare KB nelle giustificazioni architetturali
- Richiedere ai subagent di fare lo stesso

## Related skills

- `/update-todo` — pre-requisito se lavoro con TODO_STATUS
- `/convoca-parlamento` — lo consuma come prerequisito
- `/refresh-kb` (T1805, future) — aggiornamento KB da fonti esterne
- `/competitor-feature-gap` (T1703, future) — usa `competitor-landscape.md` specificamente

## Version + maintenance

- **Version**: 1.0 (created 2026-04-23 in T1701)
- **Maintained by**: orchestrator + product-architect-agent
- **Update policy**: quando KB files cambiano, questa skill non cambia (è stateless wrapper); quando aggiungo nuovi KB files, aggiorno la lista in Step 2.

## References

- `content/knowledge-base/INDEX.md` — struttura KB
- `CLAUDE.md` §"Production Knowledge References" — protocollo orchestrator
- `TODO_STATUS.md` — roadmap task T1701 creation context
- Plan file: `/Users/simonerossi/.claude/plans/ora-ti-chiedo-di-rippling-tiger.md`
