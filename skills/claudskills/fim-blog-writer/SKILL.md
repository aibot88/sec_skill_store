---
name: fim-blog-writer
description: Scrive articoli blog in italiano per FIM Insurance Broker, seguendo il tone of voice del sito, la struttura JSON esistente e le regole di compliance IVASS. Usa quando l'utente chiede di "scrivere un articolo", "creare un post blog", "aggiungere contenuto blog", "generare un articolo su [topic]" o simili.
---

# FIM Blog Writer

Skill per scrivere articoli blog in italiano per il sito di FIM Insurance Broker (www.fimbroker.it).

## Contesto di riferimento

- **Target**: famiglie, professionisti, artigiani, PMI, condomini (mercato italiano)
- **Tono**: professionale, relazionale, trasparente, NON corporate, NON freddo
- **Lingua**: esclusivamente italiano
- **Brand claim**: "Broker indipendente: non rappresentiamo compagnie ma solo gli interessi del cliente"
- **Compliance**: IVASS (RUI Sez. B n. B000405449), GDPR, IDD (D.Lgs 68/2018)
- **Sede/contatti**: Via Roma 41, 04012 Cisterna di Latina (LT) — Tel +39 06 96883381 — Email info@fimbroker.it

## Workflow obbligatorio

Quando l'utente chiede un nuovo articolo, segui questi step in ordine.

### 1. Raccogli contesto

- Leggi `fim-broker-website/data/blog-posts.json` per vedere articoli già esistenti ed evitare duplicati
- Leggi `CLAUDE.md` per refresh completo su brand voice e convenzioni
- Se l'utente indica un topic vago, **chiedi chiarimenti** prima di scrivere (target lettore, angolo, keyword primaria)

### 2. Ricerca keyword (se non fornita)

Usa WebSearch per identificare:
- Volume di ricerca stimato per la keyword principale
- Domande correlate (People Also Ask)
- Competitor che già coprono il topic

### 3. Struttura l'articolo

Ogni articolo deve avere questa struttura JSON (identica a quella esistente in `blog-posts.json`):

```json
{
  "slug": "kebab-case-seo-friendly",
  "title": "Titolo con Keyword Principale",
  "excerpt": "1-2 frasi che riassumono il valore dell'articolo per il lettore. Max 180 caratteri.",
  "category": "Auto | Vita | Casa | Salute | Aziendale | Professionisti | Viaggio | Guide",
  "date": "DD Mese YYYY",
  "readTime": "X min",
  "image": "https://images.unsplash.com/photo-XXX?w=1200&q=80&fit=crop&auto=format",
  "sections": [
    {
      "heading": "H2 della sezione",
      "body": "Paragrafo di 100-200 parole in italiano naturale e professionale.",
      "list": ["Bullet 1", "Bullet 2", "..."]
    }
  ]
}
```

**Regole strutturali:**
- 5 sezioni (4 contenuto + 1 CTA finale a FIM)
- Prime 4 sezioni: `heading` + `body` (+ `list` opzionale con 3-7 bullet)
- Ultima sezione: **sempre** una call-to-action verso FIM senza `list`, con telefono/email/link
- Lunghezza totale: 800-1500 parole
- `readTime`: calcolare come `ceil(word_count / 230)` minuti
- `date`: usare la data di oggi in formato "DD Mese YYYY" (mesi in italiano)

### 4. Scrivi contenuto di qualità

**Fai:**
- Usa dati concreti e fonti verificabili (IVASS, ANIA, Gazzetta Ufficiale, stampa di settore)
- Cita normative specifiche con riferimento (es. "D.Lgs 68/2018", "Legge di Bilancio 2024")
- Includi esempi concreti e casi pratici rilevanti per il target italiano
- Usa prima persona plurale ("crediamo", "confrontiamo", "il nostro team")
- Linka internamente ad altre pagine del sito (`/soluzioni/X`, `/servizi/Y`, `/preventivo`, `/prenota-consulenza`)

**Non fare:**
- Non promettere prezzi specifici o garanzie di copertura
- Non raccomandare prodotti di compagnie specifiche
- Non usare anglismi inutili ("leverage", "asset class", "coverage") quando esiste l'italiano
- Non inventare statistiche — se incerto, ometti o marca con [VERIFICARE]
- Non superare le 200 parole per paragrafo

### 5. Scegli categoria e immagine

**Categorie disponibili** (usa una di queste):
- `Auto` — RC auto, moto, veicoli elettrici
- `Vita` — polizze vita, TCM, previdenza complementare
- `Casa` — abitazione, condominio, catastrofi
- `Salute` — sanitaria integrativa, infortuni, LTC
- `Aziendale` — RC aziendale, cyber, D&O, flotte
- `Professionisti` — RC professionale, liberi professionisti
- `Viaggio` — assicurazione viaggio
- `Guide` — articoli educativi, glossario, spiegazioni

**Immagine:**
- Usa Unsplash con URL nel formato `https://images.unsplash.com/photo-XXX?w=1200&q=80&fit=crop&auto=format`
- Scegli foto coerenti col topic, evita cliché bancari/corporate

### 6. Inserisci nel sito

1. Aggiungi il nuovo oggetto **all'inizio** dell'array `posts` in `fim-broker-website/data/blog-posts.json` (così appare come più recente)
2. Aggiungi lo `slug` all'inizio dell'array `blogSlugs` in `fim-broker-website/app/sitemap.ts`
3. Verifica la validità del JSON con `python3 -c "import json; json.load(open('fim-broker-website/data/blog-posts.json'))"`

### 7. Commit e push

- Branch dedicato: `claude/add-blog-<slug-corto>`
- Commit message stile conventional commits: `content: add blog article on <topic>`
- **NON aprire la PR** a meno che l'utente lo chieda esplicitamente
- Alla fine informa l'utente con: URL del branch, conteggio parole, keyword target, link alla PR da creare manualmente

## Esempi di articoli esistenti (riferimento di stile)

Vedi in `fim-broker-website/data/blog-posts.json`:
- `assicurazione-condominio-guida-completa` — guida tecnica con normativa
- `differenza-broker-agente-assicurativo` — articolo educativo con positioning
- `rc-professionale-freelance-partite-iva` — target professionisti
- `polizza-catastrofale-obbligatoria-imprese-2025` — topic normativo

Quando in dubbio sul tono o la lunghezza, imita questi.

## Compliance check finale

Prima di committare, verifica che l'articolo:
- ✅ Non contenga promesse di prezzo specifiche
- ✅ Non raccomandi prodotti di compagnie particolari
- ✅ Citi normative con riferimenti corretti
- ✅ Abbia la CTA finale verso FIM con contatti reali
- ✅ Sia in italiano naturale, senza anglismi inutili
- ✅ Non inventi statistiche (se incerto, ometti)
