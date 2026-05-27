# Guida Pratica a Claude Code CLI

> **Versione 4.30 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [9. Sicurezza, permessi e guardrail](09-sicurezza.md) | [Index](README.md) | [11. MCP](11-mcp.md) →

---

## 10. Skill: il meccanismo di estensione

Le Skill sono "playbook" specializzati che Claude può consultare automaticamente quando rileva che un certo tipo di task è in gioco. **Importante**: a differenza degli slash command, **le Skill non si invocano con un comando**. Si attivano automaticamente in base alla loro `description`.

### 10.1 Come funziona una Skill

Una Skill è una cartella con un file `SKILL.md` strutturato così:

```markdown
---
name: wordpress-block-builder
description: "Use this skill when building or modifying WordPress
Gutenberg blocks. Triggers on: block.json, @wordpress/scripts,
JSX files in WordPress plugins, Edit/Save components."
---

# WordPress Block Builder

## Convenzioni del progetto
- Usa sempre @wordpress/scripts per il build
- Ogni blocco deve avere block.json, edit.js, save.js, style.scss
- Attributi devono essere tipizzati in block.json

## Pattern consigliati
[...]
```

Il campo `description` determina **quando** Claude userà la Skill. È il pezzo più importante: scrivilo pensando ai trigger concreti del tuo workflow.

Una skill ben fatta sfrutta il **progressive disclosure**: il file `SKILL.md` contiene solo l'indispensabile per attivarla; risorse più pesanti (script Python ausiliari, JSON di configurazione, documenti di riferimento) vivono in cartelle accanto e vengono caricate solo quando Claude decide che servono. Risultato: la skill non gonfia il contesto fino al momento dell'uso effettivo.

### 10.2 Skill native incluse — approfondimento

Anthropic distribuisce un set di skill ufficiali nel repository pubblico [`github.com/anthropics/skills`](https://github.com/anthropics/skills). Alcune sono bundled con Claude Code, altre vanno installate a parte (vedi [sezione 10.4](#installare-e-gestire-le-skill)). Di seguito le otto skill native più rilevanti, ognuna con metadati di riferimento, una descrizione operativa e un esempio d'uso concreto. Tutte hanno lo stesso autore, lo stesso repository monorepo e licenza Apache 2.0; il campo "Invocazione" indica i trigger tipici a cui Claude reagisce attivando la skill.

#### 10.2.1 pdf

| Chiave | Valore |
|---|---|
| **Autore / repo** | Anthropic — [`github.com/anthropics/skills/pdf`](https://github.com/anthropics/skills/tree/main/pdf) |
| **License** | Apache 2.0 |
| **Invocazione** | Allegati `.pdf`, richieste di estrazione/fill/merge su file PDF |

**Descrizione estesa.** Creazione, estrazione testo, fill di form e merge/split di file PDF. La skill gestisce posizionamento e tipizzazione dei campi quando l'utente indica un template e i dati da inserire. Si attiva in modo automatico quando in conversazione compaiono allegati PDF o quando l'utente chiede operazioni su questo formato.

**Esempio d'uso.**

```bash
> "Apri fattura-2026-04.pdf ed estrai le righe della tabella
   articoli in formato CSV (codice, descrizione, qty, importo)"
```

#### 10.2.2 docx

| Chiave | Valore |
|---|---|
| **Autore / repo** | Anthropic — [`github.com/anthropics/skills/docx`](https://github.com/anthropics/skills/tree/main/docx) |
| **License** | Apache 2.0 |
| **Invocazione** | File `.docx`, richieste di generazione/modifica documenti Word da template |

**Descrizione estesa.** Creazione e modifica di documenti Word con preservazione di stili, intestazioni, tabelle e immagini. Tipica per report periodici prodotti da template aziendali, mantenendo formattazione e layout esistenti pur sostituendo contenuti dinamici.

**Esempio d'uso.**

```bash
> "Apri template-report-mensile.docx e compilalo con i dati
   in stats-aprile.csv. Sostituisci solo i placeholder {{...}},
   lascia inalterato il resto della formattazione."
```

#### 10.2.3 pptx

| Chiave | Valore |
|---|---|
| **Autore / repo** | Anthropic — [`github.com/anthropics/skills/pptx`](https://github.com/anthropics/skills/tree/main/pptx) |
| **License** | Apache 2.0 |
| **Invocazione** | File `.pptx`, richieste di generazione presentazioni o slide deck |

**Descrizione estesa.** Generazione e modifica presentazioni PowerPoint con layout, immagini, tabelle e shape. Particolarmente utile per slide deck ripetitivi (status meeting, training session) generati a partire da scalette in Markdown o JSON.

**Esempio d'uso.**

```bash
> "Genera una presentazione di 8 slide a partire dal file
   training-claude-code.md. Una slide per ogni h2 trovato,
   bullet list dei contenuti sotto."
```

#### 10.2.4 xlsx

| Chiave | Valore |
|---|---|
| **Autore / repo** | Anthropic — [`github.com/anthropics/skills/xlsx`](https://github.com/anthropics/skills/tree/main/xlsx) |
| **License** | Apache 2.0 |
| **Invocazione** | File `.xlsx`, `.csv`, richieste di prospetti / dashboard / tabelle pivot |

**Descrizione estesa.** Fogli Excel con formule, formattazione condizionale, tabelle pivot e grafici. Adatta a dashboard veloci, consolidamenti di dati e prospetti che richiederebbero molto setup manuale in un foglio nuovo.

**Esempio d'uso.**

```bash
> "A partire da vendite-q1.csv genera un xlsx con foglio
   'Dati' (raw), foglio 'Pivot' (pivot per cliente x mese),
   foglio 'Top10' (top 10 articoli con grafico a barre)."
```

#### 10.2.5 frontend-design

| Chiave | Valore |
|---|---|
| **Autore / repo** | Anthropic — [`github.com/anthropics/skills/frontend-design`](https://github.com/anthropics/skills/tree/main/frontend-design) |
| **License** | Apache 2.0 |
| **Invocazione** | Richieste di pagine web, componenti React, layout HTML, landing page |

**Descrizione estesa.** Linee guida e pattern per produrre UI distintive che evitino lo stile "AI generico" (gradienti, ombre eccessive, palette pastello). Spinge Claude verso scelte tipografiche, palette e composizioni più mirate, riducendo la tendenza a default visivi banali.

**Esempio d'uso.**

```bash
> "Crea una landing page React per un nuovo prodotto SaaS
   B2B. Tono professionale, palette sobria, sezioni hero +
   features + pricing + cta. Niente gradienti generici e
   pulsanti 'shiny'."
```

#### 10.2.6 webapp-testing

| Chiave | Valore |
|---|---|
| **Autore / repo** | Anthropic — [`github.com/anthropics/skills/webapp-testing`](https://github.com/anthropics/skills/tree/main/webapp-testing) |
| **License** | Apache 2.0 |
| **Invocazione** | Richieste di "testare" un'app web, smoke test, verifica end-to-end |

**Descrizione estesa.** Test end-to-end di applicazioni web con Playwright in modalità headless. Si attiva quando si chiede a Claude di testare un'app web in esecuzione locale: la skill orchestra navigazione, compilazione form, asserzioni e screenshot di confronto.

**Esempio d'uso.**

```bash
> "Avvia l'app su localhost:3000, naviga su /signup,
   compila il form con dati validi, verifica che dopo
   il submit appaia il messaggio di conferma. Poi ripeti
   con email malformata e verifica l'errore."
```

#### 10.2.7 skill-creator

| Chiave | Valore |
|---|---|
| **Autore / repo** | Anthropic — [`github.com/anthropics/skills/skill-creator`](https://github.com/anthropics/skills/tree/main/skill-creator) |
| **License** | Apache 2.0 |
| **Invocazione** | Richieste esplicite di "creare una skill" o "scaffolding skill" |

**Descrizione estesa.** Meta-skill che intervista l'utente, raccoglie i requisiti e produce una nuova skill (frontmatter, contenuto, eventuali script ausiliari). Punto d'ingresso consigliato per chi non ha mai scritto una skill: Claude pone domande mirate (trigger, formato output, esempi) e genera la cartella `.claude/skills/<nome>/` pronta all'uso.

**Esempio d'uso.**

```bash
> "Voglio creare una skill che mi aiuti a scrivere ADR
   (Architecture Decision Records) coerenti con il template
   del mio team. Aiutami a impostarla con skill-creator."
```

#### 10.2.8 mcp-builder

| Chiave | Valore |
|---|---|
| **Autore / repo** | Anthropic — [`github.com/anthropics/skills/mcp-builder`](https://github.com/anthropics/skills/tree/main/mcp-builder) |
| **License** | Apache 2.0 |
| **Invocazione** | Richieste di scaffolding server MCP o esposizione di un'API esterna |

**Descrizione estesa.** Meta-skill speculare a `skill-creator` ma per server MCP (vedi [sezione 11](#mcp-integrare-servizi-esterni)). Genera lo scaffold di un server MCP a partire da una descrizione dell'API o del servizio da esporre, includendo SDK e struttura di base dei tool.

**Esempio d'uso.**

```bash
> "Costruisci un server MCP che esponga la nostra API
   ticketing interna. Endpoint base: api.mavida.local/v2.
   Operazioni: list_tickets, get_ticket, create_ticket,
   add_comment. Auth via header X-API-Key."
```

> **Nota** — Il sottoinsieme di skill bundled con Claude Code può variare nel tempo. La fonte di verità è sempre il repository ufficiale [`github.com/anthropics/skills`](https://github.com/anthropics/skills), citato anche in Allegato B.

### 10.3 Skill della community: una selezione curata

L'ecosistema produce decine di skill ogni mese e la qualità è molto variabile. Quelle che seguono sono state selezionate con criterio: repository ufficiale di un autore o organizzazione riconoscibile, license open chiara, documentazione adeguata, attività di manutenzione recente. Per ognuna trovi una scheda con i dati essenziali, una descrizione estesa, casi in cui conviene installarla, casi in cui non conviene, una valutazione editoriale e — dove è utile — un esempio d'uso.

> **Disclaimer** — L'ecosistema è in evoluzione molto rapida. Le skill qui selezionate erano attive e ben mantenute al momento della scrittura (maggio 2026); verifica sempre la salute del repo (data ultimo commit, issue aperte, license) prima di installarle.

#### 10.3.1 Superpowers

| Chiave | Valore |
|---|---|
| **Autore / repo** | Jesse Vincent — [`github.com/obra/superpowers`](https://github.com/obra/superpowers) |
| **License** | MIT |
| **Star** | ~173k |
| **Invocazione** | Si attiva su task non banali: feature nuove, bug complessi, refactoring strutturali |

**Descrizione estesa.** Methodology completa per agent: brainstorming → planning → TDD → review → execution. Non una singola skill ma un framework di skill componibili che impone un workflow strutturato, multi-platform (Claude, Cursor, OpenAI Codex, Gemini). Forza Claude a non saltare le fasi di analisi e pianificazione anche quando il task sembrerebbe risolvibile a colpo d'occhio.

**Quando usarla.**

- Sviluppi feature complesse dove "buttarsi nel codice" porta a riscritture
- Vuoi un workflow rigoroso out-of-the-box senza costruirti convenzioni da zero
- Lavori in team dove l'aderenza a una metodologia condivisa è importante

**Quando NON usarla.**

- Devi fare modifiche piccole e localizzate (un bug fix di tre righe non merita brainstorm + plan + TDD)
- Sei abituato a un tuo workflow consolidato e vuoi flessibilità

**Il mio giudizio.** Per chi viene dal pattern "chat + copia-incolla" è un cambio di marcia. Il valore non è nelle singole skill ma nella **disciplina** che impone: pensare prima di scrivere. Funziona meglio se l'adozione è di team — perché un singolo sviluppatore può rapidamente trovarla pesante per i task quotidiani brevi e disabilitarla. Da provare per qualche feature non banale prima di farne la base del proprio workflow.

**Esempio d'uso.** Dopo l'installazione, chiedi a Claude un task non banale (*"Aggiungi autenticazione 2FA al modulo login"*). Superpowers forza la sequenza brainstorm → plan → test-first → implement → review prima di toccare codice.

#### 10.3.2 Vercel Labs Agent Skills

| Chiave | Valore |
|---|---|
| **Autore / repo** | Vercel Labs — [`github.com/vercel-labs/agent-skills`](https://github.com/vercel-labs/agent-skills) |
| **License** | MIT |
| **Star** | ~26k |
| **Invocazione** | Si attiva su file React/Next.js, richieste di code review frontend, audit accessibilità |

**Descrizione estesa.** Pacchetto di 7 skill frontend di alto livello: `react-best-practices` (40+ regole performance), `web-design-guidelines` (100+ regole accessibilità/UX), `react-native-guidelines`, `composition-patterns`, `react-view-transitions`, `vercel-deploy-claimable`. Codifica le regole pubblicate da Vercel Engineering nei suoi best practice doc.

**Quando usarla.**

- Sviluppi React/Next.js professionalmente e vuoi codice rivisto contro standard noti
- Devi fare audit di accessibilità o performance su componenti già scritti
- Lavori con un team che vuole uniformità sullo stack frontend

**Quando NON usarla.**

- Lo stack è diverso da React/Next.js (le regole non si applicano)
- Stai prototipando velocemente e le regole rallentano l'iterazione

**Il mio giudizio.** Più di una skill, è una **guida di stile codificata** che Vercel pubblica gratis. Vale per chi sta dentro l'ecosistema React: se lo sei, l'investimento è zero (un comando di install) e il ritorno è alto (codice più solido al primo colpo). Se non lo sei, è inutile installarla.

**Esempio d'uso.** Durante un review chiedi *"applica `vercel-labs/web-design-guidelines` a tutti i file modificati nell'ultimo commit"*. Claude esegue un audit puntuale (focus state, contrasto colore, gestione errori form, animazioni) producendo un report di issue con riferimento alle regole violate.

#### 10.3.3 WordPress Agent Skills

| Chiave | Valore |
|---|---|
| **Autore / repo** | WordPress (organizzazione ufficiale) — [`github.com/WordPress/agent-skills`](https://github.com/WordPress/agent-skills) |
| **License** | GPL-2.0-or-later |
| **Star** | ~1.4k |
| **Invocazione** | Presenza di `wp-config.php`, plugin/theme files, riferimenti a `block.json` o REST API WP |

**Descrizione estesa.** Bundle di 14 skill di dominio WordPress costruite sulla doc ufficiale, per arginare il problema noto degli LLM che generano pattern WordPress obsoleti (codice da WP 4.x, ACF API deprecate, `query_posts()` al posto di `WP_Query`, ecc.). Include uno skill "router" (`wordpress-router`) che classifica il task e instrada alla skill specifica giusta.

**Quando usarla.**

- Sviluppi plugin o temi WordPress, in particolare con block editor e Interactivity API
- Vuoi codice aderente alla documentazione ufficiale e non a pattern datati
- Lavori su progetti dove la security WordPress è importante (capability, sanitize/escape, nonce)

**Quando NON usarla.**

- Lavori solo su contenuti WordPress (post, page) e non su codice
- Il sito è headless e WP fa solo da CMS via REST/GraphQL (poco beneficio)

**Il mio giudizio.** Per chi fa WordPress quotidianamente è la skill più utile in circolazione. Il problema dei "LLM che generano pattern WP obsoleti" è reale e costoso (ho visto codice generato da AI usare `query_posts()` o ACF v4 nel 2026), e questa skill lo elimina alla radice. Tre stelle su tre per chi lavora WordPress; zero per chi non lo fa.

**Esempio d'uso.** In un progetto WordPress chiedi *"Crea un nuovo blocco Gutenberg per inserire una callout box con icona, titolo e testo"*. `wordpress-router` riconosce il dominio e attiva `wp-block-development`, che impone `block.json` corretto, deprecation handling e security pattern dalla doc ufficiale.

#### 10.3.4 Trail of Bits Skills

| Chiave | Valore |
|---|---|
| **Autore / repo** | Trail of Bits — [`github.com/trailofbits/skills`](https://github.com/trailofbits/skills) |
| **License** | CC-BY-SA-4.0 |
| **Star** | ~5k |
| **Invocazione** | Richieste di security audit, code review per vulnerability assessment, malware analysis |

**Descrizione estesa.** 40+ skill di security per AI-assisted analysis, testing e auditing: smart contract security, code auditing (CodeQL/Semgrep), malware analysis, reverse engineering, mobile security, verification techniques. Trail of Bits è una delle aziende di consulenza security più riconoscibili in ambito open source: queste skill codificano metodologie usate sui loro audit professionali.

**Quando usarla.**

- Devi fare review di codice di terzi prima di integrare una libreria
- Sei security engineer e vuoi orchestrare CodeQL/Semgrep in modo guidato
- Lavori su progetti con esposizione esterna dove il rischio vulnerability è alto

**Quando NON usarla.**

- Stai facendo sviluppo applicativo greenfield senza esposizione critica (overkill)
- Non hai familiarità con i tool sottostanti (CodeQL, Semgrep): la skill orchestra ma il debugging dei falsi positivi richiede competenza

**Il mio giudizio.** Skill seria per un pubblico serio. La license CC-BY-SA-4.0 impone share-alike sui derivati: se modifichi le skill e le ridistribuisci sei vincolato — verifica la compatibilità con i tuoi vincoli aziendali. Per chi fa security è un boost notevole; per il resto è una cassetta degli attrezzi che probabilmente non userai.

**Esempio d'uso.** Prima di integrare una libreria PHP di terze parti chiedi *"Esegui un audit di security sulla cartella `vendor/foo-lib` usando le skill di Trail of Bits. Cerca pattern di SQLi, command injection, insecure deserialization"*. Le skill orchestrano CodeQL/Semgrep e producono un report con file, linea e tipo di vulnerabilità.

#### 10.3.5 Caveman

| Chiave | Valore |
|---|---|
| **Autore / repo** | Julius Brussee — [`github.com/JuliusBrussee/caveman`](https://github.com/JuliusBrussee/caveman) |
| **License** | MIT |
| **Star** | ~24k |
| **Invocazione** | Comandi `/caveman`, `/caveman lite`, `/caveman ultra`; trigger naturali tipo *"talk like caveman"* |

**Descrizione estesa.** Skill che forza Claude a rispondere in stile telegrafico: niente articoli, niente convenevoli, niente hedging, niente meta-commentari. Solo sostanza tecnica. Tre livelli di compressione (`lite`, `full`, `ultra`) per intensità crescente. La skill è chirurgica: comprime la parte discorsiva delle risposte (filler, articoli, frasi di cortesia) ma lascia intatti blocchi di codice, termini tecnici, messaggi di errore citati e commit message.

**Quando usarla.**

- Coding meccanico e ripetitivo (refactoring, debug, linting)
- Sei utente esperto e non hai bisogno del "perché" dettagliato
- Stai orchestrando agent multipli o background task dove l'output verbose è solo rumore
- Sei vicino al limite del tuo piano e vuoi spremere più sessioni

**Quando NON usarla.**

- Stai imparando un nuovo framework: ti serve la pedagogia, il "perché" è il valore
- Stai facendo onboarding su un codebase sconosciuto: vuoi spiegazioni complete
- Stai facendo revisione architetturale: vuoi sfumature, alternative, trade-off

**Il mio giudizio.** Caveman è un caso interessante di **claim virale che vale la pena leggere bene**. Il README promette "75% di token risparmiati" ed è diventato il numero di riferimento del progetto, ma vale la pena disaggregare il dato per capire dove davvero atterra il risparmio sulla tua bolletta:

| Numero | Cosa misura davvero |
|---|---|
| **65%** | Compressione media sull'**output** del modello (range 22-87%, misurato dai benchmark del repo). |
| **0.6-2.5%** | Quota di token che l'output rappresenta sul **totale** di una sessione Claude Code tipica. Il grosso del consumo è input: `CLAUDE.md`, cronologia conversazione, file letti, output di tool. |
| **1-2%** | Risparmio netto sulla bolletta in una **sessione interattiva normale** (output piccolo, input dominante). |
| **fino a 15-25%** | Risparmio in scenari **multi-agent paralleli** o pipeline batch headless, dove l'output diventa una quota maggiore del totale (più subagent che producono testo finale, meno input ripetuto). |

In sintesi: il "75%" virale si applica solo a una fetta minuscola del consumo nella maggior parte delle sessioni umane, mentre i numeri più alti che leggi a giro valgono per scenari particolari — caso non tipico, presentato come tipico. Il prodotto in sé è onesto (open source MIT, benchmark riproducibili nel repo), e il principio è quello che porto via davvero: pensare alla **verbosità dell'AI come a un costo misurabile**. Una volta che inizi a ragionarci, scrivi `CLAUDE.md` più leggeri, prompt più mirati, e l'efficienza cresce anche senza plugin.

**Esempio d'uso.** Risposta normale di Claude (69 token):

> *"The reason your React component is re-rendering is likely because you're creating a new object reference on each render cycle. When you pass an inline object as a prop, React's shallow comparison sees it as a different object every time, which triggers a re-render. I'd recommend using `useMemo` to memoize the object."*

Risposta in modalità Caveman (19 token):

> *"New object ref each render. Inline object prop = new ref = re-render. Wrap in `useMemo`."*

Stessa diagnosi, stessa soluzione, niente imbottitura.

### 10.4 Installare e gestire le skill

Le skill si installano in tre modi a seconda di come sono distribuite.

**Plugin marketplace** — quando una skill è confezionata come plugin (caso tipico per le skill della community più strutturate):

```bash
# Aggiungi il marketplace dell'autore
claude plugin marketplace add owner/repo

# Installa la skill specifica
claude plugin install <skill>@<plugin>
```

**Tool `npx skills`** — per skill standalone distribuite via repo Git:

```bash
# Installa una singola skill da un repo multi-skill
npx skills add anthropics/skills --skill frontend-design

# Installa l'intero pacchetto di skill di un repo
npx skills add vercel-labs/agent-skills
```

**Copia manuale** — per skill custom o sperimentali. Due location possibili:

```
~/.claude/skills/<nome>/SKILL.md       # globale (tutti i progetti)
.claude/skills/<nome>/SKILL.md         # solo questo progetto
```

La risoluzione segue la stessa gerarchia di altre risorse Claude Code: globale come default, locale al progetto come override.

#### Dove cercare skill nuove

L'ecosistema cresce molto velocemente. Le fonti più affidabili a oggi:

- **[`github.com/anthropics/skills`](https://github.com/anthropics/skills)** — repository ufficiale Anthropic, primo posto da controllare
- **[`skills.sh`](https://skills.sh)** — directory pubblica community, indicizza skill di terzi con metadati di base
- **Marketplace plugin pubblici** — gli autori di skill mature spesso pubblicano un marketplace dedicato (Trail of Bits, Vercel Labs, JuliusBrussee per Caveman)
- **Topic GitHub `claude-skills` e `agent-skills`** — utile per esplorazione mirata

Prima di installare qualunque cosa di terzi, leggi la [sezione 10.6](#sicurezza-delle-skill-di-terzi).

### 10.5 Creare una Skill personalizzata

Niente vieta di scrivere le proprie skill: anzi, è il punto in cui Claude Code diventa davvero "tuo". Vediamo un esempio end-to-end di una skill `mavida-wordpress` che codifica le convenzioni del tuo team.

**Step 1 — Scaffolding**:

```bash
# Skill locale al progetto (override) o globale (~/.claude/skills/)
mkdir -p .claude/skills/mavida-wordpress
```

**Step 2 — Scrivere `SKILL.md`** in `.claude/skills/mavida-wordpress/SKILL.md`:

```markdown
---
name: mavida-wordpress
description: "Use this skill when working on Mavida WordPress
projects. Triggers on: presence of wp-config.php, plugin
files in /wp-content/plugins/, theme files, references to
ACF or Block Editor."
---

# Convenzioni Mavida — WordPress

## Build e tooling
- Usa sempre @wordpress/scripts per i blocchi (no webpack custom)
- Composer per le dipendenze PHP, mai upload manuale di librerie
- Versioni minime: PHP 8.2, WordPress 6.4

## Pattern obbligatori
- Tutti i nuovi blocchi devono avere block.json + edit.js + save.js + style.scss
- Sanitize/escape rigorosi: `sanitize_text_field` in input, `esc_html`/`esc_attr` in output
- Nonce su tutte le form e le AJAX action
- Capability check con `current_user_can()` prima di operazioni privilegiate

## Pattern da evitare
- `query_posts()` (deprecato): usare `WP_Query`
- Funzioni che bypassano la cache: `wp_cache_flush()` solo in seed, mai in runtime
- Caricamento di JS via wp_head inline: sempre via `wp_enqueue_script`

## Comandi build comuni
- `npm run build`: build dei blocchi in produzione
- `composer test`: PHPUnit + PHPStan livello 6
- `wp-env start`: ambiente di sviluppo locale
```

**Step 3 — Verifica**: apri Claude Code in un progetto WordPress e chiedi una modifica banale (es. "Aggiungi una metabox al post type Articolo"). Se la skill è scritta bene, vedrai Claude applicare automaticamente le convenzioni (capability check, sanitize, enqueue corretti) senza che tu glielo abbia chiesto esplicitamente.

Per controllare che la skill sia caricata: `/skills list` (o `/help skills` a seconda della versione).

Lo stesso pattern vale per altre skill di team che torneranno utili nel quotidiano:

```
.claude/skills/
├── mavida-wordpress/          # convenzioni WP
│   └── SKILL.md
├── n8n-workflow/              # pattern per workflow N8N
│   └── SKILL.md
└── php-legacy-review/         # checklist refactoring PHP legacy
    └── SKILL.md
```

Una skill ben scritta è un pezzo di "memoria di team" che sopravvive ai cambi di sessione, di sviluppatore e — sempre più spesso — di tooling. Quando un prompt che usi spesso diventa una regola da imporre sistematicamente, è il segnale che vale la pena promuoverlo a skill (vedi anche la riflessione sulla "promozione" del prompt in [sezione 6.8](#promuovere-un-prompt-quando-va-in-claude.md-o-in-custom-command)).

### 10.6 Sicurezza delle skill di terzi

Una skill di terzi è codice che entra a far parte del contesto di Claude e può influenzare le sue decisioni. Non viene eseguita autonomamente — Claude chiede comunque conferma prima di lanciare comandi — ma può **istruire Claude a chiamare tool con effetti reali** (Bash, file system, WebFetch). Trattala come tratteresti una libreria che includi nel `composer.json` o nel `package.json`: con la stessa diligenza.

**Checklist prima di installare una skill di terzi:**

- **Codice review obbligatoria** — leggi `SKILL.md` per intero e ispeziona tutti gli script ausiliari (Python, Bash, JS) presenti nella cartella. Cerca riferimenti a comandi distruttivi, esfiltrazione dati, chiamate a domini esterni non documentate.
- **License compatibile** — verifica che la license della skill sia compatibile con il tuo progetto e con eventuali clausole NDA. CC-BY-SA (come Trail of Bits) impone share-alike sui derivati; GPL-2.0 (come WordPress agent-skills) ha implicazioni copyleft note; MIT (Vercel Labs, Superpowers) è generalmente la più permissiva.
- **Salute del repo** — controlla data ultimo commit, numero di star, rapporto issue aperte/chiuse, presenza di security advisories. Una skill abbandonata da un anno è un rischio per qualunque codebase la usi attivamente.
- **Permessi che richiede** — alcune skill chiedono accesso a tool potenti (Bash unrestricted, WebFetch su domini esterni, scrittura globale). Confrontale con la policy del tuo `settings.json` (vedi [sezione 9](#sicurezza-permessi-e-guardrail)) e respingi quelle che chiedono più di quanto giustifichino.
- **Sandbox in dev** — testa le skill nuove su un progetto throwaway prima di installarle globalmente in `~/.claude/skills/`. Se serve un ulteriore strato di difesa, un hook `PreToolUse` (vedi [sezione 13](#hook-automatizzare-il-lifecycle-di-claude-code)) può bloccare comandi che la skill prova a eseguire fuori dal perimetro consentito.

Lo schema mentale è lo stesso che applicheresti a una dipendenza qualunque: non si include codice che non hai letto, non si fida di un autore solo perché ha tante star, e non si abilita più di quanto serva. La differenza è che qui il "codice" è un'istruzione in linguaggio naturale che Claude leggerà ed eseguirà — e linguaggio naturale è ambiguo per definizione. Doppia attenzione.

---


---

> ← [9. Sicurezza, permessi e guardrail](09-sicurezza.md) | [Index](README.md) | [11. MCP](11-mcp.md) →
