---
name: create-new-funnel
description: Crea una nuova pagina funnel Shopify da zero (advertorial, listicle, quiz, o custom). Guida l'utente attraverso 8 fasi — scelta store, auth + scelta tema, brand identity discovery da una PDP esistente, creazione template page (con o senza header/footer), scelta tipologia funnel, raccolta materiali (competitor + research prodotto + URL PDP per le CTA), costruzione sezioni con modalità sezione-per-sezione/batch/misto, guida immagini. Da usare ogni volta che un membro del team deve pubblicare un funnel pre-PDP su uno degli store configurati.
---

# /create-new-funnel — Orchestrator

Sei una guida passo-passo per creare una pagina funnel Shopify da zero. Il funnel è una **pagina (`templates/page.*`) non un prodotto**: ospita contenuti storytelling / listicle / quiz che portano l'utente a cliccare una CTA verso una PDP esistente.

Segui le 9 fasi **in sequenza**. Non saltare fasi. Usa `AskUserQuestion` come gate tra una fase e la successiva.

## Principi generali

- **🔒 Mai toccare template o sezioni esistenti.** Le PDP e altre page template dello store sono intoccabili. Il funnel vive in file nuovi con prefisso nuovo (mai uguale a uno già presente).
- **Brand-consistent**: i colori e font del funnel vengono **ereditati** da una PDP di riferimento (Fase 3). Non inventare palette/tipografia.
- **CTA → PDP**: tutti i bottoni CTA del funnel puntano all'URL PDP del prodotto fornito in Fase 5. Mai `href="#"` o URL placeholder.
- **Mobile-first**: il traffico funnel è >80% mobile (ads paid). Ogni sezione deve leggersi benissimo a 375px.
- **No framework esterni**: niente Tailwind, Bootstrap, ecc. Solo CSS scoped dentro la sezione, con class-prefix che match del prefisso file.
- **Un push per volta, selettivo**. Mai `theme push` senza `--only`. Il `--only` include SOLO i file del nuovo funnel.
- **Conferma prima di ogni azione irreversibile** (creazione file, push live, rinomina).

## Lettura dello stato iniziale

All'avvio devi trovare il file `config/stores.json` del plugin.

**REGOLA ASSOLUTA** — senza eccezioni, senza interpretazione:

1. **NON creare MAI nessun file dentro `~/.claude/skills/`.** Quella cartella contiene solo i symlink di sviluppo. Se stai per scrivere un file il cui path contiene `.claude/skills/`, fermati subito: è sbagliato.
2. **`stores.json` vive SOLO nella cartella del plugin**, cioè `<plugin-root>/config/stores.json`. Mai altrove.
3. **`stores.example.json` esiste già** nel repo — non va mai creato né copiato dalla skill.

**Procedura deterministica** (esegui nell'ordine, senza saltare step):

```bash
# Step A — prova path canonico
test -f "$HOME/Desktop/shopify-pdp-builder/config/stores.json" && echo "FOUND:$HOME/Desktop/shopify-pdp-builder/config/stores.json"

# Step B — risolvi via symlink della skill (se A non ha trovato nulla)
PLUGIN_ROOT=$(dirname "$(dirname "$(readlink "$HOME/.claude/skills/create-new-funnel")")")
test -f "$PLUGIN_ROOT/config/stores.json" && echo "FOUND:$PLUGIN_ROOT/config/stores.json"

# Step C — prova il path plugin standard di Claude Code
test -f "$HOME/.claude/plugins/shopify-pdp-builder/config/stores.json" && echo "FOUND:$HOME/.claude/plugins/shopify-pdp-builder/config/stores.json"
```

Comportamento:

- Se **uno qualsiasi** degli step stampa `FOUND:<path>` → usa quel path con `Read` per leggere `stores.json` e procedi con la Fase 1.
- Se **tutti e tre** falliscono → **FERMATI**. Non scrivere nulla. Chiedi all'utente in chiaro: "Non trovo `config/stores.json`. Dimmi il path assoluto del plugin `shopify-pdp-builder` sul tuo disco." Attendi risposta, poi ricontrolla.

**Mai** usare `Write` o `Edit` per creare `stores.json` o `stores.example.json`. Se manca, è un problema di setup utente, non un file da generare dalla skill.

---

## Fase 1 — Scelta store

Mostra all'utente la lista store configurati. Usa `AskUserQuestion` con un'opzione per store + "Altro".

Se "Altro": chiedi nome, `shopify_domain` (*.myshopify.com), theme ID, path workdir, path env. Aggiungi voce a `stores.json`.

Salva in memoria: `store.name`, `store.shopify_domain`, `store.theme_id`, `store.workdir_path`, `store.env_path`.

---

## Fase 2 — Verifica auth + scelta tema

1. Se `store.env_path` non esiste: guida alla creazione del `.env` (Theme Access token → `shptka_*`). Fonte: `references/auth-pattern.md`.
2. Lancia:
   ```bash
   cd "<store.workdir_path>"
   set -a; source "<store.env_path>"; set +a
   npx @shopify/cli@latest theme list --no-color
   ```
3. Se 401 / Invalid API key: token scaduto, utente rigenera e riprova.
4. **Mostra i temi** parsati: `[live]`, `[unpublished]`, `[development]` con nome + ID.
5. `AskUserQuestion`: "Su quale tema operare?" Default: `[live]` (o `store.theme_id` del config). Opzioni: una per tema.
6. Salva scelta in `store.theme_id` (sovrascrive config per sessione) e `store.theme_name`.
7. **Pull fresco**:
   ```bash
   cd "<store.workdir_path>"
   set -a; source "<store.env_path>"; set +a
   npx @shopify/cli@latest theme pull --theme <store.theme_id> --nodelete
   ```
   Chiedi conferma prima (il pull sovrascrive file locali non pushati).

---

## Fase 3 — Brand identity discovery

Obiettivo: capire palette + tipografia del brand per mantenere il funnel visivamente coerente col resto del sito. Fonte di verità: `references/brand-identity-discovery.md`.

### 3.1 Scelta PDP di riferimento

1. Elenca i `product.*.json` in `<store.workdir_path>/templates/`.
2. `AskUserQuestion`: "Quale PDP usare come riferimento per colori e tipografia?"
   - Mostra i nomi leggibili (es. `berberina-pills`, `crema-borse-occhiaie-pdp`).
   - Se ce n'è uno solo (oltre al default `product.json`) assumilo automaticamente.
3. Salva in `brand.reference_pdp`.

### 3.2 Estrazione automatica

Leggi in parallelo:
- `templates/product.<reference>.json`
- 2-3 sezioni principali referenziate (hero, prima sezione con CTA button)
- `config/settings_data.json` (color_schemes + type_header_font + type_body_font)
- `config/settings_schema.json` (opzionale, per nomi umani dei settings)

Estrai secondo le regole di `brand-identity-discovery.md`:
- **Palette**: `primary`, `primary_text`, `secondary`, `accent`, `text`, `background` (HEX).
- **Tipografia**: `heading_font`, `body_font` (normalizzati da Shopify handle a "Nome, fallback").
- **Stili ricorrenti**: border-radius, shadow, heading weight/style.

### 3.3 Mostra riepilogo e chiedi conferma

Presenta all'utente un blocco leggibile (esempio in `brand-identity-discovery.md`, sezione "Output atteso"). Usa `AskUserQuestion` o chiedi in chiaro:
- "Confermi questo brand profile?" → procedi.
- "Correggo un valore" → l'utente dice cosa cambiare, applica, ripresenta.
- "Cambio PDP di riferimento" → torna a 3.1.

Salva l'oggetto `brand.*` in memoria. Verrà iniettato nelle sezioni in Fase 8.

---

## Fase 4 — Scelta tipo di funnel

**PRIMA di creare il template**, devi sapere che tipo di funnel stiamo costruendo. Tipo e materiali informeranno il nome del template, il prefisso sezioni e la struttura.

`AskUserQuestion`: "Che tipo di funnel stiamo creando?"

Opzioni:
- **Advertorial** — articolo narrativo, storytelling personale che porta a PDP. Target freddo.
- **Listicle** — articolo "N motivi per", benefici ordinati, confronto. Target semi-caldo.
- **Quiz** — domande + risultato personalizzato, engagement-driven. Target freddo.
- **Altro** — descrivi liberamente la struttura, poi forniamo esempi.

Salva in `funnel.type` ∈ {`advertorial`, `listicle`, `quiz`, `other`}.

Carica la struttura base di riferimento da `references/funnel-types.md` per il tipo scelto. Sarà usata come **ipotesi di partenza** in Fase 5; verrà raffinata con gli esempi competitor sempre in Fase 5.

Se `other`: chiedi all'utente una descrizione della struttura che ha in mente (numero sezioni, ordine, ruoli).

---

## Fase 5 — Struttura funnel (URL destinazione + competitor)

**Questa fase serve SOLO a definire la STRUTTURA** del funnel (quante sezioni, in che ordine, con che ruolo). Non chiedere ancora i contenuti del prodotto — quelli vengono nella Fase 6.

### 5.1 URL PDP destinazione (OBBLIGATORIO)

`AskUserQuestion` o chiedi in chiaro: "Qual è l'URL della PDP di destinazione? (dove porteranno tutte le CTA del funnel)"

Esempi:
- `https://nimea-beauty.it/products/crema-borse-occhiaie-ufficiale`
- `https://glowria.com/products/crema-corpo-autoabbronzante-ufficiale`

Valida che:
- Inizia con `https://`.
- Contiene `/products/<slug>`.

Salva in `funnel.cta_url`. Sarà il `href` di **TUTTI** i bottoni CTA del funnel.

### 5.2 Esempi competitor del tipo scelto

Chiedi 2-5 **URL / screenshot** di funnel competitor dello stesso tipo (`funnel.type` di Fase 4). Per ogni esempio chiedi un contesto breve: perché ti piace, cosa copieresti, cosa cambieresti.

Se l'utente non ha esempi: suggerisci Facebook Ads Library, swipefile.com, aggregator tipo advertorial.com. Se l'utente risponde `skip`: procedi con la struttura base di `references/funnel-types.md` per il tipo scelto.

Claude **analizza i competitor** per:
- Confermare/raffinare la struttura di partenza (aggiungere/rimuovere/riordinare sezioni).
- Identificare pattern ricorrenti di hook, problem, proof, CTA.
- Stimare lunghezza/density media (word count per sezione).

### 5.3 Struttura proposta + conferma

Presenta all'utente la **struttura sezioni definitiva** (dopo l'analisi competitor):

```
Struttura advertorial proposta (11 sezioni, basata su 3 competitor + base):

01. announcement   — top bar urgency/offer
02. hero           — headline + foto protagonista + CTA 1
03. problem-hook   — amplifica dolore, identifica target
04. story          — storia personale (before/after narrativo)
05. solution-intro — presentazione prodotto come risposta
06. how-it-works   — 3 step + ingredienti chiave
07. social-proof   — testimonianze + recensioni
08. faq            — 5-7 obiezioni gestite
09. cta-offer      — offerta + urgency + CTA 2
10. trust-badges   — garanzia / spedizione / pagamenti
11. footer         — disclaimer legale
```

`AskUserQuestion`: "Confermi questa struttura o vuoi modificarla?" — l'utente può aggiungere/rimuovere/riordinare/rinominare.

Salva la lista finale in `funnel.sections_plan` (array ordinato con `nn`, `role`, `notes`).

---

## Fase 6 — Studio prodotto + angle marketing

Questa è la fase **più articolata** del funnel (advertorial in particolare). A differenza della PDP che è "solo" riscrittura testi, qui devi **capire il prodotto in profondità** e scegliere un **angle** (l'angolazione narrativa) che renderà l'advertorial convincente.

L'obiettivo: arrivare a fine fase con abbastanza materiale per scrivere hook + story + proof + obiezioni che girino attorno a un angle chiaro.

### 6.1 Studio della PDP propria

Claude fetcha e legge `funnel.cta_url` (PDP di destinazione, Fase 5.1). Usa `WebFetch` sull'URL per estrarre:
- Nome prodotto esatto come usato sullo store.
- Claim principali (H1, H2, bullet benefici).
- Ingredienti chiave / tecnologia / brevetti citati.
- Proof points già in pagina (numeri, certificazioni, test clinici).
- Prezzo + eventuali varianti/bundle.
- Tono di voce della PDP.

Presenta un riepilogo strutturato all'utente e chiedi **cosa manca / cosa è sbagliato** (spesso le PDP sono ottimizzate per conversione diretta, non per storytelling — l'utente ha info extra).

Salva in `product.*`.

### 6.2 Studio PDP competitor (stessa categoria)

`AskUserQuestion` o chiedi: "Dammi 2-3 URL di PDP competitor nello stesso spazio prodotto."

Per ciascuna: `WebFetch` + estrai claim, ingredienti, proof, pricing, posizionamento.

Obiettivo: capire **come gli altri comunicano lo stesso problema/soluzione** e trovare lo spazio bianco dove il nostro prodotto può differenziarsi.

Output: tabella sintetica competitor vs nostro, con colonne `claim_primario`, `differenziatore`, `prezzo`, `gap`.

### 6.3 Analisi angle competitor + proposta (OBBLIGATORIO)

**Step fisso, non saltabile.** Dopo aver studiato le PDP competitor (6.2), identifica l'angle dominante prima di chiedere alternative.

1. **Identifica il MAIN ANGLE** usato dai competitor (dalle PDP analizzate in 6.2 + dai funnel competitor di Fase 5.2). L'angle è l'angolazione narrativa — NON un claim, è il frame da cui il prodotto viene raccontato. Esempi:
   - "Ingrediente scientifico esclusivo" (angle scientifico)
   - "Routine naturale di 5 minuti al giorno" (angle lifestyle)
   - "Alternativa economica al trattamento estetico da €300" (angle risparmio)
   - "Before/after reale di persone come te" (angle social proof)
   - "Risolve X in N giorni — garantito" (angle result-driven)

2. **Presenta il main angle** all'utente con evidenze concrete:
   ```
   Dall'analisi competitor emerge questo angle dominante:

   ➤ ANGLE: <frase di 1 riga>
      Evidenze:
      - Competitor A (URL): <frase/claim specifica che lo dimostra>
      - Competitor B (URL): <idem>
      - Funnel competitor X (URL): <idem>
   ```

3. **Chiedi anche gli ads attuali del nostro prodotto**:
   - 1-3 copy ads attualmente girati (headline + body + concept video, se ci sono).
   - Se l'utente risponde `skip`: OK, procedi.

4. **`AskUserQuestion`**: "Vuoi usare questo stesso angle per il nostro funnel?"
   - **Sì, uso questo angle** → salva in `funnel.angle` e procedi a 6.4.
   - **No, proponimi alternative** → vai al punto 5.
   - **Ho un angle mio in mente** → l'utente lo descrive, salva e procedi.

5. Se l'utente chiede alternative: **proponi 2-3 angle alternativi** che sono:
   - Usati in adiacenza (competitor minori, prodotti simili della stessa categoria).
   - Coerenti con i proof points / ingredienti del nostro prodotto (niente angle insostenibili).
   - Differenzianti rispetto al main angle (per evitare "l'ennesima copia di X").

   Ogni alternativa presentata con: nome angle + 1 frase di pitch + perché funzionerebbe meglio del main. Poi `AskUserQuestion` di scelta finale.

Salva in `funnel.angle` — sarà la bussola narrativa di TUTTE le sezioni.

### 6.4 Research prodotto — rifinitura finale

Consolida in bullet veloci (l'utente può completare/correggere quello che Claude ha estratto):

- **Nome prodotto** esatto (da PDP).
- **Ingredienti chiave** (3-5, con effetto specifico legato all'angle scelto).
- **Claim principali** (3-5, formulati in linea con l'angle).
- **Target audience**: chi, età, problema specifico (non generico).
- **Differenziazione vs competitor** (dal gap di 6.2).
- **Proof points**: numeri, test, recensioni reali, certificazioni, testimoni.
- **Obiezioni tipiche** che l'advertorial deve gestire (3-5, dalla Facebook Ads Library o da commenti reali).

Se uno di questi campi è debole, Claude lo segnala esplicitamente ("Proof points: nessun numero concreto — l'advertorial sarà meno convincente. Vuoi aggiungerne?").

### 6.5 Brand assets extra

Chiedi:
- Logo URL CDN (se diverso da quello del tema).
- Eventuali foto prodotto custom, mockup, loghi certificazioni da usare.

Se `skip`: usa solo quelli estraibili da tema + PDP.

### 6.6 Riepilogo finale prima del template

Mostra un blocco compatto:
- Tipo funnel + struttura confermata (N sezioni, da Fase 5.3).
- Angle scelto (una frase).
- 3 claim centrali.
- 3 proof points.
- 3 obiezioni da gestire.
- URL CTA.
- Palette + tipografia (richiama `brand.*` da Fase 3).

`AskUserQuestion`: "Tutto chiaro, procedo con la creazione del template?"

---

## Fase 7 — Creazione template funnel

Ora che conosci tipo + materiali, puoi creare il template con un nome sensato.

### 7.1 Scelta partenza

`AskUserQuestion`: "Partire da zero o duplicare un template page esistente?"
- **Da zero** (default, caso tipico).
- **Duplica** esistente (se il team ha già un funnel "buono" da cui partire).

Se duplica: riusa il flusso della Fase 3 di `/create-new-pdp` (lista `page.*.json`, prefisso, duplicazione sezioni). Fonte: `references/section-naming.md`.

### 7.2 Nome nuovo template

`AskUserQuestion`: "Nome del nuovo template funnel?"

Proponi 2-3 default intelligenti che combinano **slug prodotto** (dedotto da `funnel.cta_url` di Fase 5.3) + **tipo funnel** (`funnel.type` di Fase 4). Esempi:

- Prodotto `crema-borse-occhiaie` + tipo `advertorial` → `crema-borse-occhiaie-advertorial`
- Prodotto `berberina-pills` + tipo `listicle` → `berberina-pills-listicle`
- Prodotto `crema-rassodante` + tipo `quiz` → `crema-rassodante-quiz`

Vincoli:
- Kebab-case, solo `[a-z0-9-]`.
- Valida che `<workdir>/templates/page.<nome>.json` NON esista.

Salva in `funnel.template_name`.

### 7.3 Layout — header/footer on/off

`AskUserQuestion`: "Mantenere header e footer Shopify?"

Opzioni:
- **No, chromeless (Recommended)** → pagina full-screen senza navbar/footer. Layout: `theme.chromeless` (se supportato) o custom.
- **Sì, tema standard** → header + footer del tema sempre visibili. Layout: `theme`.

Fonte: `references/page-template-layout.md`.

Se l'utente sceglie chromeless:
- Verifica con `Glob` o `ls` se esiste `<workdir>/layout/theme.chromeless.liquid`.
- Se NO: chiedi all'utente se vuole (a) creare un layout custom chromeless ora, (b) procedere con `theme` e poi decidere, (c) usare nome layout diverso.
- Se SÌ: usa direttamente `"layout": "theme.chromeless"`.

Salva in `funnel.layout`.

### 7.4 Prefisso sezioni

Proponi un prefisso di default derivato da `funnel.template_name` (vedi `references/section-naming.md`, sezione "Naming per FUNNEL"):
- `crema-borse-occhiaie-advertorial` → `cbo-adv-` (esplicita) o `cbo-` (breve).
- `berberina-listicle` → `bl-` o `bb-lst-`.

`AskUserQuestion`: "Prefisso sezioni: `<default>`? (conferma o alternativo)"

Salva in `funnel.prefix`.

### 7.5 Generazione template scheletro

Scrivi `templates/page.<funnel.template_name>.json` con scheletro minimo:

```json
{
  "sections": {},
  "order": [],
  "layout": "<funnel.layout>"
}
```

(Le sezioni verranno aggiunte progressivamente in Fase 8.)

Se si è scelta la duplicazione da template esistente (7.1): applica la logica di duplicazione della Fase 3 PDP e salta i punti seguenti.

### 7.6 Push selettivo template

```bash
cd "<store.workdir_path>"
set -a; source "<store.env_path>"; set +a
npx @shopify/cli@latest theme push \
  --theme <store.theme_id> --nodelete --allow-live \
  --only "templates/page.<funnel.template_name>.json"
```

### 7.7 Istruzioni manuali Page in Admin

Mostra all'utente:

```
Ora crea la Page in Shopify Admin:
1. Admin → Online Store → Pages → Add page
2. Title: "<titolo visibile della pagina>"
3. Content: lascialo vuoto (le sezioni vengono dal template)
4. In "Theme template" (sidebar destra): seleziona `<funnel.template_name>`
5. Save
6. Torna qui e dimmi lo slug della page (es. `scopri-autoabbronzante`)
```

Salva lo slug in `funnel.page_slug`. URL live: `https://<store.shopify_domain>/pages/<funnel.page_slug>`.

---

## Fase 8 — Costruzione sezioni

### 8.0 Scelta modalità di lavoro (obbligatoria)

`AskUserQuestion`: "Come vuoi lavorare sulle sezioni?"

**Opzione A — Sezione per sezione (Recommended per prima PDP)**
Per ogni sezione: crea file → push → verifica live → conferma → prossima sezione.
Più lento ma sicuro.

**Opzione B — Batch**
Crea tutte le sezioni in parallelo → mostra preview completa → l'utente approva una volta → push finale unico.
Più veloce ma meno granulare.

**Opzione C — Misto leggero**
Checkpoint intermedi solo sulle sezioni complesse (hero, CTA offer, quiz-wrapper). Sezioni semplici (FAQ, footer, closing) passano in batch senza conferma individuale.
Compromesso consigliato per utenti già rodati.

Salva scelta in `funnel.build_mode` ∈ {`A`, `B`, `C`}.

### 8.1 Pianifica la lista sezioni

In base a:
- Struttura confermata in Fase 5.3 (`funnel.sections_plan`).
- Angle scelto in Fase 6.3 (`funnel.angle`).

Produci una lista esplicita con nome file + ruolo + note:

```
Struttura pianificata (es. advertorial, prefisso `aa-`):

01. sections/aa-01-announcement.liquid  → announcement bar
02. sections/aa-02-hero.liquid          → hero advertorial
03. sections/aa-03-problem.liquid       → problem hook
04. sections/aa-04-story.liquid         → storia personale
05. sections/aa-05-solution.liquid      → intro prodotto
06. sections/aa-06-how-it-works.liquid  → come funziona + ingredienti
07. sections/aa-07-proof.liquid         → social proof
08. sections/aa-08-faq.liquid           → obiezioni
09. sections/aa-09-cta-offer.liquid     → CTA + offer
10. sections/aa-10-trust-badges.liquid  → badge garanzia
11. sections/aa-11-footer.liquid        → footer disclaimer
```

`AskUserQuestion` di conferma/modifica. L'utente può aggiungere, rimuovere, riordinare, rinominare sezioni.

### 8.2 Regole per ogni sezione costruita

Per ogni `sections/<funnel.prefix><NN>-<ruolo>.liquid`:

1. **Markup mobile-first**, poi `@media (min-width: 768px)` per desktop. Classi scoped con prefisso che matcha il nome file (es. tutte le classi dentro `aa-02-hero.liquid` iniziano con `.aa-02`).
2. **Stili inline** nel file `.liquid` dentro `<style>` scoped (no `assets/*.css` esterni a meno che sia strettamente necessario). Usa valori di `brand.*`:
   - Bottoni CTA: `background: <brand.primary>`, `color: <brand.primary_text>`, `border-radius: <brand.button_radius>`, hover più scuro.
   - Headline: `font-family: <brand.heading_font>`, `font-weight: <brand.heading_weight>`.
   - Body: `font-family: <brand.body_font>`, `color: <brand.text>`.
3. **Testi** dal research di Fase 6.4 + angle di Fase 6.3 + ispirazione competitor di Fase 5.2, con density/lunghezza coerente al ruolo (vedi `references/funnel-types.md`).
4. **Bottoni CTA** puntano a `<funnel.cta_url>` con `<a class="<prefix>__cta" href="<funnel.cta_url>">`. Ripeti la CTA almeno 2 volte nel funnel (hero + closing minimo).
5. **Tutto editabile dal theme editor — regola fissa**. Ogni sezione funnel nasce editabile: testi, immagini, CTA sono `section.settings.*` / `block.settings.*` nello schema, mai hardcoded nel markup. Fonte: `references/section-schema-patterns.md`.
   - **Testi**: `type: "text"` per singola riga, `type: "textarea"` per multiriga semplice, `type: "richtext"` per paragrafi con inline bold/italic/link (l'editor mostra WYSIWYG).
   - **Immagini**: `type: "image_picker"`. Mai `<img src="https://cdn..."` hardcoded. Render via `{{ section.settings.<id> | image_url: width: <W> }}` per responsive automatico Shopify.
   - **CTA**: coppia `type: "url"` + `type: "text"` per ciascun bottone. `href` iniziale default = `funnel.cta_url` (Fase 5.1).
   - **Liste ripetibili** (FAQ, benefit cards, testimonial, reason cards listicle, domande quiz): usa `blocks` con `type` dedicato e `max_blocks` sensato. Iterazione via `{% for block in section.blocks %}` nel markup.
   - **Default** sensati: ogni setting/block ha default popolato dal research/angle di Fase 6, così la pagina live mostra già contenuto reale subito dopo il push, senza passare dall'editor.
   - **Placeholder immagini**: l'`image_picker` resta senza default (o con default placeholder SVG data-uri). Il markup gestisce lo stato "vuoto":
     ```liquid
     {% if section.settings.hero_image %}
       <img src="{{ section.settings.hero_image | image_url: width: 1600 }}" alt="{{ section.settings.hero_image.alt }}" loading="lazy">
     {% else %}
       <img src="data:image/svg+xml,%3Csvg…%3E" alt="IMG_PLACEHOLDER_02_hero">
     {% endif %}
     ```
6. **Schema Liquid completo** (esempio minimo, estendi con tutti i settings/blocks della sezione):
   ```liquid
   {% schema %}
   {
     "name": "<NOME LEGGIBILE SEZIONE>",
     "tag": "section",
     "class": "<prefix>-<NN>",
     "settings": [
       { "type": "text", "id": "heading", "label": "Titolo", "default": "…" },
       { "type": "richtext", "id": "body", "label": "Testo", "default": "<p>…</p>" },
       { "type": "image_picker", "id": "hero_image", "label": "Immagine hero" },
       { "type": "url", "id": "cta_url", "label": "Link CTA", "default": "<funnel.cta_url>" },
       { "type": "text", "id": "cta_label", "label": "Testo CTA", "default": "Scopri di più" }
     ],
     "presets": [
       { "name": "<NOME LEGGIBILE SEZIONE>" }
     ]
   }
   {% endschema %}
   ```
7. **Aggiorna il template JSON** `templates/page.<funnel.template_name>.json`:
   - Aggiungi la sezione al blocco `sections`:
     ```json
     "<NN>": { "type": "<funnel.prefix><NN>-<ruolo>", "settings": {} }
     ```
   - Aggiungi la chiave all'array `order` nella posizione giusta.

### 8.3 Workflow per Opzione A (sezione per sezione)

Loop sulle sezioni in ordine 01→N:

1. Crea il file `.liquid` con `Write`.
2. Aggiorna `templates/page.<funnel.template_name>.json` aggiungendo la nuova sezione (usa `Edit` o `Read`+`Write`).
3. Push selettivo:
   ```bash
   cd "<store.workdir_path>"
   set -a; source "<store.env_path>"; set +a
   npx @shopify/cli@latest theme push \
     --theme <store.theme_id> --nodelete --allow-live \
     --only "sections/<funnel.prefix><NN>-<ruolo>.liquid" \
     --only "templates/page.<funnel.template_name>.json"
   ```
4. Chiedi all'utente di aprire `https://<store.shopify_domain>/pages/<funnel.page_slug>` e confermare mobile+desktop.
5. Gestisci aggiustamenti minimi (typo, font-size, spacing) in loop finché confermato.
6. **Prima di passare alla sezione successiva**, chiedi esplicitamente con `AskUserQuestion`:

   "Sezione confermata. Come vuoi procedere con le restanti N sezioni?"
   - **Continua sezione-per-sezione** → ripeti il ciclo dal punto 1 sulla prossima sezione.
   - **Passa a batch (completa tutte le restanti insieme)** → switcha al workflow 8.4 (Opzione B batch) per le sezioni ancora da fare. Il progresso sulle sezioni già confermate resta intatto.
   - **Passa a misto leggero** → switcha al workflow 8.5 (Opzione C) per le sezioni ancora da fare.

   Rispetta la scelta. Non dare per scontato che l'utente voglia finire in una modalità solo perché ha iniziato così.

### 8.4 Workflow per Opzione B (batch)

1. Crea TUTTI i file `.liquid` in parallelo (multiple `Write` nel singolo messaggio).
2. Scrivi il `templates/page.<funnel.template_name>.json` definitivo con tutte le sezioni ordinate.
3. Mostra all'utente un **diff-preview** testuale della struttura e i punti chiave di ogni sezione (headline + primo paragrafo). Non dump di tutto il markup.
4. Aspetta approvazione globale o correzioni puntuali.
5. Push selettivo unico con `--only` di tutti i file (template + sezioni in un comando).
6. Utente verifica live.
7. Aggiustamenti successivi: passa automaticamente a modalità sezione-per-sezione per i fix puntuali.

### 8.5 Workflow per Opzione C (misto leggero)

1. Identifica sezioni "complesse" (hero, problem, solution, proof, cta-offer, quiz-wrapper, result) vs "semplici" (announcement, trust-badges, faq, footer, disclaimer).
2. Per le complesse: workflow A (checkpoint individuale).
3. Per le semplici: crea in batch, push unico intermedio senza conferma per ciascuna.
4. A fine fase: pull completo live, utente verifica tutto insieme.

### 8.6 Verifica no-regressioni

Prima di ogni push: conferma a te stesso di non aver aperto/modificato per sbaglio file esistenti fuori dal prefisso `<funnel.prefix>`. Se è successo: stop, ripristina, riprova.

---

## Fase 9 — Guida immagini

Le sezioni sono tutte editabili: ogni immagine è un `image_picker` nello schema. L'utente le carica **dal theme editor**, non via URL CDN incollato in chat. Fonte: `references/funnel-image-specs.md` (specs) + `references/section-schema-patterns.md` (pattern editor).

Per ogni sezione con uno o più `image_picker`:

1. Identifica dal markup/schema quante immagini servono e il ruolo di ciascuna (grep `image_picker` nello schema della sezione).
2. Genera il brief:
   ```
   Sezione: <prefix>-<NN>-<ruolo>.liquid
   Immagini richieste: <N>
   
   Per ogni immagine:
     - Ruolo: <es. "hero lifestyle protagonista + emozione">
     - Ratio: <4:5>
     - Dimensioni: <1200×1500>
     - Peso max: 150 KB (.webp)
     - Campo theme editor: "<label del image_picker>"
   ```
3. Istruzioni utente:
   ```
   1. Apri il theme editor: Admin → Online Store → Themes → Customize (tema <store.theme_name>).
   2. Nel top-left picker seleziona Pages → <titolo pagina funnel>.
   3. Nella sidebar sezioni click su <prefix>-<NN>-<ruolo>.
   4. Per ogni campo immagine: click → Select image → Upload → salva.
   5. Save del theme editor.
   ```
4. L'utente conferma in chat quando ha fatto.
5. Nessun push necessario: le immagini si salvano lato Shopify come setting del template, non nel file `.liquid`.
6. Chiedi conferma visiva sull'URL live della page.

Modalità di gestione: la stessa `funnel.build_mode` di Fase 8 (A singola / B batch / C misto) — l'utente può fare tutte le immagini di tutte le sezioni in un passaggio unico nell'editor, poi checkpoint visivo finale.

---

## Verifica finale

Checklist chiusura:
- [ ] Template `templates/page.<funnel.template_name>.json` pushato e sincronizzato.
- [ ] Tutte le sezioni pushate, schema Liquid senza errori.
- [ ] URL live funzionante: `https://<store.shopify_domain>/pages/<funnel.page_slug>`.
- [ ] Mobile 375px: tutte le sezioni leggibili, bottoni cliccabili, testi non troncati.
- [ ] Desktop 1440px: layout si espande correttamente, max-width container coerente.
- [ ] Palette + tipografia coerenti con `brand.*` (spot check visivo vs PDP di riferimento).
- [ ] Tutte le CTA cliccate → portano a `<funnel.cta_url>` (PDP prodotto).
- [ ] Tutti gli `image_picker` delle sezioni hanno un'immagine assegnata dal theme editor (no fallback placeholder SVG visibili).
- [ ] DevTools console: no errori Liquid, no 404 su immagini.
- [ ] Header/footer come da scelta (chromeless = assenti, theme = presenti).

Chiedi conferma su ciascun check. Se qualcosa fallisce: torna alla fase corrispondente, fix, re-push.

Quando tutto ✓: dichiara il funnel pronto. Suggerisci:
- Impostare UTM tracking sugli URL degli ads che porteranno qui.
- Configurare Meta Pixel / Google Analytics sulla pagina (via theme settings o code injection).
- Testare un click CTA end-to-end (dalla page al PDP al checkout).

## Troubleshooting rapido

| Sintomo                                         | Causa                                          | Fix                                                                |
|-------------------------------------------------|------------------------------------------------|--------------------------------------------------------------------|
| La page live mostra ancora header/footer        | Layout non chromeless o tema senza theme.chromeless | Verifica `"layout"` nel template JSON; crea layout custom se manca |
| Bottoni non portano al prodotto                 | `href` vuoto o `#` in qualche sezione           | Grep `href="` nelle sezioni, verifica tutti = `<funnel.cta_url>`    |
| Font non coerente col resto del sito            | `brand.*` non applicato a tutte le sezioni      | Ri-scansiona i `.liquid` e inserisci `font-family: <brand.heading_font>` negli h1/h2 |
| Sezione invisibile live                         | Non aggiunta all'`order` del template JSON      | Apri `templates/page.<nome>.json`, verifica array `order`           |
| Push fallisce con Liquid syntax error           | Schema malformato, brace unmatched              | Leggi error line, `Edit` puntuale, ri-push                         |
| Mobile text overflow                            | Font-size fissi in px anziché clamp             | Sostituisci con `clamp(1rem, 4vw, 1.5rem)` o media query           |

## File correlati (references)

- `references/auth-pattern.md` — `.env`, Theme Access token, verifica connessione.
- `references/selective-push.md` — comando push + flag.
- `references/section-naming.md` — convenzioni prefissi (con sezione funnel).
- `references/funnel-types.md` — struttura advertorial / listicle / quiz / other.
- `references/brand-identity-discovery.md` — come leggere colori/font da una PDP.
- `references/page-template-layout.md` — schema page template, chromeless vs theme.
- `references/funnel-image-specs.md` — dimensioni/ratio per ruolo sezione.
- `references/section-schema-patterns.md` — pattern schema editabile: tipi di setting, blocks, richtext, image_picker, default sensati.
