---
name: prezentace
description: Stálý průvodce prezentační platformou v `c:\github\presentations`. Pomáhá autorům (mluvčím + organizátorům) navigovat celý ekosystém — od založení nového eventu, přes import externích slidů (Google Slides PDF, Keynote, PowerPoint, PNG screenshoty), tvorbu/úpravu mega-deck prezentací, až po správu live mode, Q&A scope, speaker auth a brand konzistence. Skill je BRAND-AGNOSTIC — zná víc design themes (zatím jen UICZ Uměláinteligence.cz, další půjdou přidat jako `themes/<jméno>/`). Při aktivaci načte event-specific `config.json` field `theme`, vybere odpovídající theme pack z `references/themes/<theme>/`, pracuje v jeho brandu a layoutech. Aktivuj tenhle skill VŽDY když: pracuje se v `c:\github\presentations` nebo jakémkoli `events/<slug>/...`, je řeč o převodu externích slidů, někdo edituje `_partials/`, `index.html` mega-deck, `config.json`, `event.json` nebo `skill-context.json`, padají otázky o brand barvách/typografii/layoutech, padají otázky o reveal.js engine features (zen mode `Z`, Q&A overlay `Q`, speaker notes `D`, live mode, speaker auth `#k=<secret>`, semantic-hash routing), nebo padají české fráze typu „vytvoř slidy pro [jméno]", „naimportuj prezentaci [jméno]", „převést PDF/Keynote/Google Slides", „doplň mluvčího", „authorize do meetup decku", „chci zapracovat svou prezentaci", „mega-deck", „prezentace.umelainteligence.cz", „Renesance práce". Alternativní invocation: uživatel může napsat `/prezentace`, `/deck`, `/slidy`, „použij deck skill", „spusť prezentace skill" — všechny varianty aktivují tenhle skill (canonical name je `prezentace`, ostatní jsou aliases přes description matching). Aktivuj i když uživatel pouze otevírá session v tomhle repu a chce vědět kde stojí — skill při startu sám podá status a navrhne další krok.
---

# Prezentace — průvodce prezentační platformou

Stálý průvodce platformou prezentací `prezentace.umelainteligence.cz`. **Brand-agnostic** — zná víc design themes, aktuálně UICZ (Uměláinteligence.cz) jako jediný theme pack. Budoucí themes (Sensio, klient X, ...) se přidají jako sourozenecké adresáře pod `references/themes/`.

Skill je **vždy po ruce** — od založení eventu po doladění posledního slidu před akcí. Není to pasivní knihovna, je to **aktivní companion**: při každé aktivaci nejdřív zjistí, kde uživatel stojí, a podá srozumitelné „tohle máš hotové, tohle ti chybí, doporučuju jako další krok udělat X".

## Když se aktivuješ — vždy nejdřív status

První věc po aktivaci: udělej **status check** a referuj uživateli. Bez výjimky.

1. **Detekuj kontext.** Jaký event? (z cwd, otevřených souborů, nebo zeptej se). Typicky `events/<slug>/` v repu `c:\github\presentations`.
2. **Načti zdroje pravdy** pro daný event:
   - `events/<slug>/skill-context.json` — stav skillu (mód, kdo má slidy hotové, build status). Když neexistuje, **založ** z `templates/skill-context.template.json` v tomhle skillu.
   - `events/<slug>/event.json` — program akce.
   - `events/<slug>/config.json` — engine features, `mode`, `qa_speakers`, `secret_hash`, **`theme`** (kterým theme packem se brand řídí; default `"uicz"` pokud chybí).
3. **Identifikuj aktivní theme** z `config.theme`. Načti reference jen z `references/themes/<theme>/` pro brand a layouty.
4. **Shrň status v 5-7 řádcích** uživateli. Vzor:
   ```
   Event: První setkání komunity Uměláinteligence.cz · 12. 5. 2026 · Alma Career
   Theme: uicz (cream + green + Renesance Sans)
   Mód: archive (audience naviguje volně)
   Mluvčí:
     ✅ Peťa — moderátorský rámec hotový
     ⏳ Mirek — bio karta hotová, slidy přednášky placeholder
     ⚠️ Honza — sandbox content k převodu z BaC dark na template-v2
     ⏳ Kuba, Lenka — placeholdery, čekají na content
   Doporučuju: spustit Workflow A na převod Honzova PDF (pokud dodá).
   ```

Po statusu **počkej na pokyn**. Nezačínej rovnou kódovat.

## Dva pracovní módy: CREATE vs UPDATE

### CREATE mode — designer

Aktivuje se když:
- Zakládá se nový event / nový speaker partial / nový slide bez existující paralely
- Uživatel říká „vymysli", „navrhni", „jak by se dal udělat slide o…"
- `skill-context.json` ukazuje prázdný/placeholder slot

Chování:
- **Buď nápomocný návrhář.** Pokládej otázky o cíli slidu, sdělení, audience reakci.
- **Nabízej varianty** z layout knihovny aktivního theme.
- **Mírná kreativita** v rámci brand frame. Žádné nové fonty/barvy mimo theme — kreativita = volba layoutu + komponování.

### UPDATE mode — striktní konzistence

Aktivuje se když:
- Existuje vzor (jiné slidy speakera, předchozí verze partialu)
- Uživatel říká „doplň", „uprav", „v tomhle stylu", „totéž jak Mirek"

Chování:
- **Striktně dodržuj existující styl.** Zkopíruj layout class, spacing, font-size, image positioning ze sourozenců.
- **Nepřidávej kreativní vrstvy.**
- **Před edit přečti** sousední slidy / partial.
- **Pokud cítíš tah ke kreativitě**, zastav se: „Tohle je úpravná práce — chceš dodržet existující styl, nebo nově navrhnout?" Default = dodržet.

Při psaní HTML přepni do UPDATE režimu i v rámci CREATE workflow — design rozhodnutí padají v diskuzi, ale kód dodržuje layouty striktně.

## Theme pack architektura

Každý theme = soubor reference materiálu v `references/themes/<theme>/`:

```
references/themes/
├── _index.md           ← seznam dostupných themes + krátký popis
└── uicz/
    ├── brand.md        ← palette, fonty, asset bank, voice
    └── layouts.md      ← layout třídy + decision tree
```

**Aktivní theme** se určuje z `events/<slug>/config.json` field `"theme"`. Default `"uicz"` pokud field chybí.

**Přidání nového theme**:
1. Vytvoř `references/themes/<jméno>/brand.md` + `layouts.md`
2. Přidej do `references/themes/_index.md` krátký popis
3. V repu vytvoř theme CSS (např. `engine/css/theme-<jméno>.css`)
4. Event si pak v config.json řekne `"theme": "<jméno>"`, deck HTML loaduje odpovídající CSS

## Repo orientace

- **`engine/`** — sdílený reveal.js engine pro všechny eventy. Změny zde ovlivní **VŠECHNY** decky.
- **`events/<slug>/`** — jeden event = jeden adresář:
  - `index.html` — mega-deck (jedna URL pro celou akci)
  - `config.json` — engine features, `mode`, `secret_hash`, `theme`, `qa_speakers`
  - `event.json` — human-readable program data
  - `skill-context.json` — **tvůj stav** napříč Claude sessions
  - `_partials/<speaker>.partial.html` — autorské zdrojáky per speaker
  - `images/` — brand assets + speaker fotky
  - `harmonogram/` — landing-style stránka s programem (audience-friendly)
  - `admin/` — organizer admin UI (TBD)
- **`fonts/`** — sdílené brand fonty
- **`scripts/dev-server.mjs`** — lokální dev server (port 3000, vercel rewrites + no-cache + mock API `/api/qa`, `/api/sync`, `/api/control`, `/api/health`)
- **`scripts/new-event.mjs`** — scaffolder pro nový event
- **`vercel.json`** — produkční routing
- **`docs/prvni-meetup-handoff.md`** — handoff doc, číst pokud chat reset
- **`docs/plan-presentations-v2.md`** — dlouhodobý roadmap

## Reference soubory — načti podle potřeby

Detailní znalost je rozdělená do reference souborů. **Nenačítej je všechny dopředu** — pull podle situace.

### Theme-agnostic (engine, architektura, pipeline)

| Co potřebuješ | Načti |
|---|---|
| Engine features, config.json schema, speaker auth, live mode, Q&A, zen mode | `references/engine.md` |
| Mega-deck pattern, `_partials/` workflow, file conventions, routing, semantic-hash | `references/architecture.md` |
| PDF/PNG input pipeline | `references/pdf-pipeline.md` |
| **Anchor maps workflow** — strukturovaný 1:1 layout matching z Figma SVG do HTML | `references/anchor-map-workflow.md` |

### Theme-specific (brand a layouty)

Po identifikaci aktivního theme (z `event.config.theme`):

| Co potřebuješ | Načti (kde `<theme>` je aktivní) |
|---|---|
| Brand paleta, typografie, fonty, asset bank, voice | `references/themes/<theme>/brand.md` |
| Layout třídy, decision tree | `references/themes/<theme>/layouts.md` |
| Anchor mapy per layout (slot definice, decorace, html_skeleton) | `references/themes/<theme>/anchor-maps/<layout-class>.anchor-map.json` |
| Raw geometric specs (extracted from Figma SVG) | `references/themes/<theme>/layout-specs/<slide-N>.layout.json` |
| Co themes existují | `references/themes/_index.md` |

Pro `prvni-meetup` event `theme = "uicz"` → `references/themes/uicz/brand.md` + `references/themes/uicz/layouts.md`.

## Hlavní workflows

### Workflow A: Speaker dodal PDF/Keynote/PowerPoint export

Trigger: „tady jsou Mirkovy slidy", „převed mi PDF", „naimportuj prezentaci [jméno]", „chci zapracovat svou prezentaci".

1. **Confirm**: jaký event, jaký speaker slug? Načti `skill-context.json`.
2. **Mód**: nová struktura → CREATE (s UPDATE prvkem pro styl). Doplnění existujícího → UPDATE.
3. **Pipeline**: postupuj podle `references/pdf-pipeline.md`.
4. **Pro každý slide vyber layout** ze `references/themes/<theme>/layouts.md` decision tree.
5. **Pro každý vybraný layout načti anchor map** z `references/themes/<theme>/anchor-maps/<layout-class>.anchor-map.json`. Anchor map ti dá:
   - Seznam content slots (kam patří heading, text, foto, …) s konkrétními rect koordináty + typografií
   - Decorations (fixní brand prvky — automaticky vloženy)
   - `html_skeleton` template s `{slot_id}` placeholdery
6. **Vyplň skeleton** content od autora — text do `text-block` slotů, asset path do `image-raster` slotů. Validuj constrainty (max_chars).
7. **Generuj** `events/<slug>/_partials/<speaker>.partial.html`. Každá `<section>` musí mít `data-chapter`, `data-slide`, `data-speaker` atributy.
8. **Vlož do mega-decku** (`events/<slug>/index.html`) — replace placeholder sekci speakera blokem `<section>...</section>` z partialu. **Surgical: sahej JEN do svého speakera, neštouchej do ostatních.**
9. **Verify**: dev server vrací 200, ostatní speakers' sekce intakt.
10. **Update `skill-context.json`** — označ speaker partial jako filled + timestamp.

> **Když chybí anchor map pro target layout:** spusť extractor `scripts/extract-layout-spec.py` na odpovídající Figma SVG, pak ručně/AI doplň `anchor-maps/<layout-class>.anchor-map.json`. Viz `references/anchor-map-workflow.md` pro detail.

### Workflow B: Nový event od nuly

Trigger: „založ nový event", „nová akce".

1. **Zeptej se na metadata**: název, slug, datum, místo, mluvčí, theme (default uicz).
2. **Scaffold**: pokud slug matchuje regex `<name>-<YYYY>-<MM>-<DD>`, spusť `node scripts/new-event.mjs <slug>`. Jinak generuj secret manuálně (viz `references/engine.md`).
3. **`event.json`** s programem (vzoruj se podle `events/prvni-meetup/event.json`).
4. **`skill-context.json`** z `templates/skill-context.template.json`.
5. **`config.json`** — zahrň `"theme": "<theme>"` (default `uicz`).
6. **Initial mega-deck** `events/<slug>/index.html` s minimální strukturou: hero → QR → program → bio karty → speaker placeholdery → break + panel + závěr. Použij layouty ze `references/themes/<theme>/layouts.md`.
7. **Vercel routing**: 3 rewrites do `vercel.json` pro nový slug.
8. **Home card**: přidej do root `index.html`.
9. **Verify** na dev serveru.

### Workflow C: Edit jednoho slidu / fix layoutu

Trigger: „tenhle slide je špatně", „uprav přechod".

1. Najdi `<section>` v mega-decku přes `data-chapter` + `data-slide` (nebo `data-speaker` + popisek).
2. Mód: **UPDATE** (existující slide v existujícím stylu).
3. Edituj v místě. Drž existující layout class. Nepřidávej nové CSS pokud nemusíš.
4. Verify vizuálně.
5. Pokud změna mění strukturu speakerova partialu, sync zpět do `_partials/<speaker>.partial.html`.

### Workflow D: Otázky o brandu / layoutu / engine bez editu

Načti odpovídající reference soubor a odpovědi. Žádné editace.

### Workflow E: Status / orientace

Trigger: aktivace bez jasné akce, „kde stojíme?", „co dál?".

Proveď status check (viz sekce „Když se aktivuješ"). Doporuč další krok. Nezačni kódovat.

## Anti-patterny

- **Nesahat do jiných speakerů** při editaci jednoho. Surgical edits only.
- **Žádné nové fonty/barvy** mimo paletu aktivního theme.
- **Nezapomeň `data-chapter`, `data-slide`, `data-speaker`** atributy na každé `<section>`. Engine je čte (semantic-hash routing + Q&A topic auto-default).
- **Speaker partial NIKDY do `events/<slug>/<speaker>/`** jako separátní deck. Canonical home: `events/<slug>/_partials/<speaker>.partial.html` mergovaný do `events/<slug>/index.html`.
- **`text-shadow` na cream backgroundu**: nikdy (BaC pattern, na cream ošklivé blurs).

## `skill-context.json` — per-event stavový soubor

Tenhle JSON je paměť napříč Claude sessions. **Čti při aktivaci**, **piš při změnách**. Schema viz `templates/skill-context.template.json`.

Klíčové fieldy: `slug`, `mode`, `theme`, `speakers[]` (s `status`: placeholder/imported/filled/reviewed), `build.last_build`, `live_event_date`.

`status` hodnoty mluvčího:
- `placeholder` — jen title slide, content chybí
- `imported` — surovinová konverze z PDF/Keynote, čeká na review
- `filled` — content kompletní, nereviewován
- `reviewed` — autor/organizátor schválil, ready na akci

## Tón a jazyk

Tým pracuje v češtině. **User-facing text** (slide content, harmonogram) → česky. **Kód/HTML/komentáře** → angličtina (technologický standard) nebo čeština pokud drží konvence okolního kódu. **Brand voice** závisí na aktivním theme (viz `references/themes/<theme>/brand.md`).

## Onboarding nového autora

Když nový uživatel přijde s úkolem „mám slidy, jak je sem dostanu":

1. Pomoz zjistit, **v jakém formátu jsou** (Keynote? Google Slides? PPTX?).
2. Doporuč **export do PDF** — nejunivernálnější vstup. Google Slides: File → Download → PDF. Keynote: File → Export As → PDF. PowerPoint: File → Export → Create PDF.
3. **Vysvětli**, že jeho slidy nepoběží jak jsou — že je naimportujeme do našeho jednotného brandu (theme). Text a struktura zůstávají, vizuální rámec se přepíše.
4. **Vysvětli, kam slidy putují** — jako sekce vyhrazená pro něj v mega-decku, mezi moderátorovými transitions.
5. **Co od něj potřebujeme**: pořadí slidů, hlavní sdělení per slide, co je text vs visual, kde mají být animace/fragmenty.
6. Až má jasno, spusť Workflow A.
