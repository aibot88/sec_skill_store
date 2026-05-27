---
name: clanky-konvence
description: Konvence pro psaní a editaci článků v Astro monorepu orlojWeb (hodinarium-eu, horologie-cz). Aktivuje se při editaci .md/.mdx v content/hodinarium-eu/ nebo content/horologie-cz/, při tvorbě/úpravě komponent v apps/*/src/components/, při psaní frontmatteru (perex/tldr, author, references), při vkládání obrázků s creditem, při formátování odkazů (wiki, mapy, PDF), při řešení layoutu článku (hero, float images, mezititulky, single * * *) a při kontrole deploymentu na Cloudflare Pages.
---

# Konvence článků a layoutu — hodinarium-eu / horologie-cz

Tenhle skill drží všechna pravidla, na kterých se s Davidem dohodli pro Astro články spolku ČSH. Default platí pro **hodinarium-eu** (větší archiv, MDX-ready); kde je rozdíl, je explicitně označený jako "horologie-cz" / "hodinarium-eu".

## 1. Frontmatter článku

Aktuální schema (z `apps/hodinarium-eu/src/content.config.ts`):

```yaml
---
title: "..."                    # POVINNÝ; bez **markdown** — frontmatter neparsuje markdown
slug: "..."

# Kategorie podle taxonomie 2026-04 (5 hlavních + kronika jako separátní collection):
category: "sbirka"           # Exponáty spolku (vystavené i depozit)
       | "konstrukce"        # Mechanismy a principy hodin obecně
       | "projekty"          # DIY autorské konstrukce spolku
       | "virtualni-muzeum"  # Zajímavé hodiny mimo sbírku spolku
       | "muzea"             # Sister muzea, přehledy sbírek (Mindelheim, Protivín, …)
       | "zajimavosti"       # Eseje o čase, kalendáře, časoměrné systémy

# Deprecated (postupná migrace; schema je dočasně akceptuje):
       | "decin" | "vezni-hodiny" | "ostatni"

# Pro Kronika (události, fotoreporty) NE category, ale samostatná
# collection v content/kronika/ s vlastním schema (date, typ, …).

originalUrl: "https://hodinarium.eu/...htm"   # legacy zdroj (POVINNÝ)
lastModified: "RFC date | null"
sourceCharset: "windows-1250"
scrapedAt: "ISO timestamp"

tldr: "Stručné shrnutí pro perex"  # OPT — vyrenderuje rámeček "Stručně:"
                                     # Auto-perex byl zrušen (duplikoval 1. paragraf)

author: "Petr Král"             # OPT — byline ho zobrazí jako "P. Král"
                                  # (helper formatAuthor strip "Ing./Dr./Mgr./…")

tags:                           # OPT — řízený whitelist v data/tags.json
  - vezni
  - elektricke
  - 1900s
  - restaurovane
  # Validace: každý tag MUSÍ být ve whitelist, jinak build failne

references:                     # OPT — sekce "Literatura a odkazy" pod článkem
  - title: "Název"
    url: "https://..."          # OPT — bez = jen text
    author: "Autor díla"        # OPT
    year: 2014                  # OPT — number nebo string
    type: kniha | clanek | pdf | odkaz | wiki | mapa   # OPT — default odkaz
    note: "doplňující text"     # OPT

referenceStyle: bullet | numbered  # OPT — default bullet (type-icon)

ogImage: "/img/..."             # OPT — přepíše default OG template
thumbnail: "/img/..."           # OPT — přepíše první-image v atlas/katalog

manualEdit: true                # OPT — flag že článek byl ručně editován
---
```

**Schéma je shared mezi všemi články.** Měnit ho znamená update `content.config.ts` plus migrovat existující články. Před přidáním nového field zkontroluj, jestli ho opravdu chceš mít versioned across všechny stávající.

### Tagy — řízeně rozšiřovatelný whitelist

Whitelist je v `apps/hodinarium-eu/src/data/tags.json`, organizovaný do dimenzí: `typ` (vezni/kapesni/…), `pohon` (mechanicke/elektricke/…), `regulator` (kyvadlo/setrvacka/…), `obdobi` (gotika/…/2000s), `stav` (funkcni/restaurovane/…), `lokace` (sobeslav/decin/cesko/svet/…), `kontext` (kuriozita/akvizice/…), `vyrobce` (prokes/brillie/lenzkirch/…).

**Přidání nového tagu:**
1. Edituj `data/tags.json` — přidej do správné dimenze
2. Update `_meta.updated` na dnešní datum
3. Commit + použij v článku

**Validace:** Zod refine v `content.config.ts` načítá whitelist a ověřuje každý tag. Typo (`atomove` vs `atomicke`) failne build.

**Kdy přidat nový tag:** pokud opakovaně používáš plain text ve více článcích k popisu téhož konceptu. Tagy nejsou pro one-off štítky — jsou pro **systematickou klasifikaci**, která má v budoucnu umožnit `/tagy/<tag>` filter stránku.

## 2. Hero obrázek

**Pravidlo:** první `<img>` v článku se automaticky stane hero (full šířka 72ch sloupce, žádný float, margin-bottom 2.25rem). Logika je v `apps/hodinarium-eu/src/pages/clanky/[slug].astro` (script `setup()`).

- Auto-promote přidá class `img-hero` jen pokud první img **nemá** žádnou z manuálních class: `img-hero` | `img-full` | `img-standalone` | `img-skip-hero`.
- Markdown `![alt](src)` jako první obrázek = automatic hero. **Preferovaný způsob.**
- Pokud chceš první img přeskočit jako hero (např. malou ikonku), přidej `class="img-skip-hero"`.

**Post-hero guard:** za hero MUSÍ následovat text. Skript automaticky:
- Zjistí, zda hned po hero přijde block obsahující jen velký obrázek (img-large/full/standalone/hero) bez textu.
- Pokud ano, **přesune ho** za první následující paragraf s textem (>50 znaků).
- Tj. v MDX můžeš mít dva `![]()` po sobě, JS to vyřeší — nicméně pro stabilitu ideálně **piš v pořadí: hero → text → další obrázek**.

## 2.5. Iniciála — drop cap na začátku článku

**Dvě pravidla, která jdou ruku v ruce:**

1. **První písmeno textu = iniciála** — první znak prvního odstavce se vyrenderuje jako velká dekorativní iniciála (drop cap) v serifovém fontu, brass-bright barva, float left, 4,5em výška, 2 řádky textu vedle ní. Auto via CSS `.drop-cap > p:first-of-type::first-letter` v `global.css`.
2. **První písmena dalších odstavců NEZVÝRAZŇOVAT** — žádný `**bold**`, žádný drop cap, normální typografie. CSS pokrývá záměrně jen první paragraf.

### Co psát v markdownu

Prostý text. Žádný manuální zápis ani zvýraznění iniciály.

```markdown
Chomutovské květinové hodiny stály u vchodu do tehdejšího městského parku…

V dalším odstavci se hodiny popisují podrobněji…

Třetí odstavec pokračuje obvyklou typografií.
```

→ „C" v prvním odstavci se vyrenderuje jako iniciála; „V" a „T" v dalších odstavcích zůstávají normální velikosti.

### Legacy artefakt: `**X**a první pohled` per-paragraph

Mnoho legacy článků z hodinarium.eu importu má **na každém paragrafu** zbytečně bolded první písmeno: `**N**a první pohled`, `**P**oměrně bohatá historie`, `**S**troj byl…`. Tohle je **legacy noise** z původního HTML stylingu — vypadá to jako středověký manuskript, ale na webu zbytečně přitahuje pozornost, kazí čitelnost a porušuje pravidlo 2 výše.

**Pravidlo:** strip manuální `**X**slovo` na začátku paragrafu. CSS drop-cap pokrývá jen **první paragraf** (autorský pattern); ostatní paragrafy mají normální typografii.

Při refactoru existujícího článku regex find-and-replace:
- Hledat: `\*\*([A-ZÁ-Ž])\*\*([a-zá-ž])` na začátku řádky paragrafu
- Nahradit: `$1$2` (sjednotit zpět do plain textu)

Hromadný cleanup je riskový (může chybným regexem zasáhnout i platný bold uprostřed věty) — postupně při dotyku článku.

## 3. Obrázky v textu

| Velikost (z image-sizes.json) | CSS chování | Kdy |
|---|---|---|
| `img-small` (≤ ~200px) | float — alternuje pravo/levo | drobné obrázky v textu |
| `img-medium` (~320px) | float — alternuje pravo/levo | běžné fotky |
| `img-tall` (úzké vysoké) | float — alternuje pravo/levo | portréty, schémata |
| `img-large` (široké) | standalone block, na střed | dokumenty, panoramata |
| `img-full` | standalone, plná šířka článku | manuální override |
| `img-standalone` | standalone, max 480px | manuální override |
| `img-hero` | full šířka článku, no margin top | první obrázek (auto) |

**Rytmus floatable obrázků:** JS counter střídá `img-float-right` / `img-float-left` deterministicky. Photo komponenta (figure.photo) je z rytmu vyloučena — zůstává standalone.

**Mobile (≤600px):** vše standalone — float vypnutý vždy.

### Sofistikovanější float — multi-paragraph + line-height snap

`[slug].astro` skript (krok 1.6) dělá dvě věci pro lepší typografický pocit:

1. **Multi-paragraph float**: `.prose-content p` nemá `overflow: hidden`, takže float pokračuje přes několik odstavců, dokud nenarazí na `clear: both` (h2/h3/hr/.fleuron). Vysoký obrázek tak může obtékat 2–3 paragrafy místo zaseknutí v jednom.

2. **Line-height snap**: po načtení obrázku JS změří jeho rendered výšku, vypočte nejbližší celočíselný násobek `line-height` paragrafu, a mírně resize (max ±20%, jinak skip). Tím obrázek **lícuje s textovým gridem** — žádný poloviční řádek nad/pod. Snap funguje jen na float images (small/medium/tall), nikoli na hero/standalone/Photo.

**Pokud autor chce explicitně ukončit float**, vloží `<div class="clearfix"></div>` před paragraf, který má začínat na novém řádku (přes celou šířku).

### Photo komponenta a float

Photo komponenta (`<figure class="photo">`) **podporuje float** — caption je teď overlay v pravém dolním rohu obrázku, takže s obtékaným textem nekoliduje (žádný flow textu pod caption). JS v ArticleImageBehavior klasifikuje obrázek (small/medium/tall) a propaguje class na figure (ne na img uvnitř); figure je layout container, img fills 100 %. Float se rotuje pravo/levo deterministicky stejně jako u markdown obrázků.

Mobile (≤600 px) figure float vypnuté, caption se vrátí pod obrázek (overlay nad ~320 px wide fotkou je nečitelný).

## 3.5. Popisná karta sbírkového předmětu — `karta` ve frontmatteru

Pro `category: sbirka` články o **konkrétním sbírkovém předmětu** používej structured `karta:` ve frontmatteru. Renderuje se jako definition list (`<dl>`) s brass border vlevo, copper labels v small-caps, hodnoty vpravo. JS ji automaticky přesune **za hero obrázek** (vizuálně: nadpis → hero → karta → text); bez JS zůstává před hero.

```yaml
karta:
  vyrobce: "Jan Prokeš v Sobotce, 1868"
  ram: "klecový z ocelových pásnic"
  krokJicihoStroje: "Grahamovy palety, vlastní konstrukce"
  biciStroje: "čtvrťový a hodinový"
  rozmery: "š 80 × v 68 × h 38 cm"
  kyvadlo: "délka cca 235 cm"
  ciselnik: "smaltovaný, římské číslice"
  pohon: "závaží 12 kg + 8 kg"
  signatura: "Jan Prokeš v Sobotce 1868"
  stav: "po restaurování (Petr Skála, 2003)"
  provenience: "zámek Býchory, ze sbírky pana X"
  extra:
    - { label: "Inventární číslo", value: "ČSH-S-042" }
    - { label: "Lokace", value: "Hodinárium Děčín, vitrína 3" }
```

**Standardní pole** (v pevném pořadí): `vyrobce`, `ram`, `krokJicihoStroje`, `biciStroje`, `rozmery`, `kyvadlo`, `ciselnik`, `pohon`, `signatura`, `stav`, `provenience`. Všechna volitelná, prázdná pole se nerenderují.

**`extra[]`** — pole `{ label, value }` pro nestandardní atributy (inventární čísla, lokace v expozici, …). Renderuje se na konci karty v pořadí, jak je zadáno.

**Kdy kartu doplnit:**
- Vždy pro nový článek o konkrétním exponátu (`category: sbirka`)
- Při review starých `sbirka` článků postupně doplňovat
- **Ne pro:** virtualni-muzeum (cizí exponáty bez vlastních dat), zajimavosti, projekty (jiný layout), konstrukce (obecné), muzea, kronika

Schema je v `apps/hodinarium-eu/src/content.config.ts`, komponenta v `apps/hodinarium-eu/src/components/KartaSbirky.astro`.

## 3.7. Galerie — větší množství obrázků bez textu

**Pravidlo:** ≥2 konsekutivní `img-large` obrázky (každý na samostatné řádce, oddělené prázdným řádkem) → JS automaticky seskupí do `.article-gallery` gridu (auto-fill 200 px sloupce, 4:3 cover crop, sepia hover) s lightbox při kliknutí na thumbnail.

**Krátké caption paragrafy** (text < 120 znaků, žádný `<img>`) **mezi obrázky NEPŘERUŠUJÍ** sekvenci — naopak se připojí k předchozímu obrázku jako `<figcaption>` v galerii. Delší text = obsahový paragraf, sekvenci ukončí.

```markdown
![Fotografie 1](/img/foo/foto_0001.jpg)

Chomutov

![Fotografie 2](/img/foo/foto_0002.jpg)

Květinové hodiny v období protektorátu.

![Fotografie 3](/img/foo/foto_0003.jpg)
```

→ 3 obrázky v gridu, caption pod thumbnailem, klik = lightbox v plné velikosti s prev/next.

**Kdy nechat obrázky standalone (NE galerie):** krátký článek se 2 obrázky, kde každý nese vlastní téma nebo má důkladný popisný text. Stačí 1 obsahový paragraf mezi nimi (>120 znaků) — JS sekvenci ukončí.

**Pro fotoreport / kroniku** s mnoha obrázky tedy stačí psát `![alt](src)` po sobě s případnou krátkou caption — JS se postará o gallery layout a lightbox automaticky.

## 4. Photo komponenta — preferovaný způsob

Cesta: `apps/hodinarium-eu/src/components/Photo.astro`.

**Pravidlo:** **Pro nové obrázky** používat `<Photo />` místo markdown `![alt](src)`. Důvody:
- Konzistentní místo pro credit/copyright caption (overlay v pravém dolním rohu obrázku)
- Bez credit polí se chová jako prostý `<img>` — caption se nerenderuje
- `class` prop se propaguje na `<img>` (img-hero, img-large, atd.)
- Snadno se v budoucnu doplní credit u obrázku, který ho zatím nemá

**Direktivový syntax v .md/.mdx** (po A.11 migraci, Sveltia-compatible — žádné `import` statements):

```markdown
::photo{src="/img/cesta/foo.jpg" alt="Popis pro screen readery" class="img-hero" author="Øyvind Holmstad" authorUrl="https://..." license="CC BY-SA 3.0" licenseUrl="https://..." sourceUrl="https://..." year="2014"}
```

Atributy POVINNĚ jednořádkově (multi-line direktiva nefunguje). Hodnoty vždy v uvozovkách `"..."`. Pro číselné hodnoty (`year`) string syntax `"2014"` — komponenta si to coercuje.

Plugin `@csh/remark-csh-directives` (v `packages/remark-csh-directives/index.mjs`) převádí direktivu na `<Photo />` Astro komponentu při buildu. Komponenta je registrovaná v `apps/hodinarium-eu/src/utils/content-components.ts`.

Pokud `class="img-hero"` nedáš a Photo je první v článku, JS auto-promote ho udělá hero stejně. Manuální `class="img-hero"` je explicit a ani slug.astro skript ho nepřepíše.

### Credit caption — overlay s auto-tone

Caption (autor + licence + zdroj) se renderuje **jako overlay v pravém dolním rohu obrázku** (ne pod ním jako dřív). Barva textu je vybrána automaticky podle jasu pravého dolního rohu obrázku:

- **Světlé pozadí** → čistá černá (`#000`)
- **Tmavé pozadí** → čistá bílá (`#fff`)

Žádné halo / text-shadow — záměrné rozhodnutí. Halo působí synteticky a kazí "filmový" dojem. Plain B/W lépe sedí k periodikálnímu stylu webu; pokud jednou narazíme na fotku, kde to není čitelné, řešíme per-image (manuální tone override v Photo prop, případně přesun na jinou fotku).

Tone se počítá build-time pomocí `sharp` v `scripts/build-image-index.ts` — vyřízne ~30 % × 30 % BR rohu, spočítá průměrný grayscale jas, threshold 140 z 255 oddělí `dark` (světlé pozadí, tmavý text) od `light` (tmavé pozadí, světlý text). Výsledek se uloží jako pole `tone` do `image-sizes.json`. Photo komponenta tone načte a aplikuje class `.credit-tone-dark` / `.credit-tone-light`.

**Kdy přepočítat tone:** vždy po přidání nových obrázků do `public/img/` — `pnpm imgindex:build` regeneruje celý index včetně tone (rebuild ~5 s pro 2700+ obrázků).

**Default fallback:** pokud src není v `image-sizes.json` (např. nový obrázek bez rebuild), default je `light` — světlý text + tmavé halo. Bezpečnější pro neznámá pozadí, většina foto-pozadí má střední/tmavé tóny.

**Mobile (≤600 px):** overlay se vrátí pod obrázek (overlay nad ~320 px wide fotkou je nečitelný). Pak používá výchozí muted barvu textu, žádné halo.

### Co psát do `author`, když původ neznáš

ČSH archiv má často staré fotky bez známého autora. Bezpečné formule:
- **`author="autor neznámý"`** — nejjednodušší, čestné. Vyrenderuje „Foto: autor neznámý".
- **`author="Z archivu ČSH"`** — pokud fotka přišla z vlastního archivu spolku a autor je nedohledatelný.
- **`author="autor neznámý"` + `year={1925}`** — odhadovaný rok přidává historický kontext.
- Plus volitelně `note` v references s textem „Pokud jste autorem této fotografie, kontaktujte nás pro doplnění atribuce." (DMCA-style invitace na nápravu, standard u kulturních archivů).

**Právně:** v ČR autorské právo vzniká automaticky vznikem díla, takže technicky i osiřelé dílo (orphan work) je chráněno. Industry standard pro muzejní/archivní weby je formule výše — neinfrige se tím méně, ale přiznává gap a vytváří kanál pro nápravu. Plně compliant je jen registrace v EUIPO orphan works databázi (Směrnice 2012/28/EU), což je over-engineered pro spolkový web.

## 5. Ikony — Font Awesome ONLY, ŽÁDNÉ emoji

**Generic pravidlo (PLATÍ NAPŘÍČ CELÝM WEBEM):** pro libovolnou UI ikonu **výhradně Font Awesome** (`fa-solid` / `fa-regular` / `fa-brands`). **Emoji glyphy NIKDY** — `📖 📰 🔗 ⚠ ✓ ✗ ⛔ 🟢 …` jsou zakázané (různé renderingy napříč platformami, barevné gradienty, ne-monochromatické, kolize s text typography).

```html
<i class="fa-solid fa-book" aria-hidden="true"></i>
<i class="fa-solid fa-newspaper" aria-hidden="true"></i> Časopis
```

Mapping emoji → Font Awesome viz `~/.claude/projects/-Users-dknespl-Documents-orlojWeb/memory/feedback_ikony_font_awesome.md`.

### 5.1. Konvence ikon u odkazů

| Typ | Stav (k 2026-05-13) | Target (Font Awesome) | Detekce |
|---|---|---|---|
| **Wikipedia / Wikimedia** | **ⓦ** (Unicode v kroužku, text glyph) | → `fa-brands fa-wikipedia-w` | `href*="wikipedia.org/wiki/"`, `href*="wikimedia.org/wiki/"` |
| **Generic external** | **↗\FE0E** (Unicode arrow + text variation selector) | → `fa-solid fa-arrow-up-right-from-square` | jakýkoliv `href^="http"` mimo wiki/mapa/own-domain |
| **Mapa** | pin (SVG, copper) | → `fa-solid fa-location-dot` nebo zachovat SVG | `href*="mapy.cz"`, `openstreetmap.org`, `google.com/maps`, `goo.gl/maps` |
| **Kniha** | ~~📖~~ → `fa-solid fa-book` | (jen v `references:` s `type: kniha`) |
| **PDF** | ~~⤓~~ → `fa-solid fa-file-pdf` nebo `fa-solid fa-download` | (jen v `references:` s `type: pdf`) |
| **Článek (časopis)** | ~~📰~~ → `fa-solid fa-newspaper` | (jen v `references:` s `type: clanek`) |
| **Vlastní doména / relative** | bez ikony | hodinarium.eu, orloj.eu, horologie.cz, `/path` |

**Migrace v plánu** — současný stav (Unicode glyphy ↗ ⓦ a emoji 📖 📰 ⤓) je legacy z předchozího iteračního pattern. Long-term target = výhradně Font Awesome. Při dotyku konkrétní komponenty / utility migrovat na FA. Pro inline odkazy přes CSS `::after` (kde Font Awesome `<i>` element nelze vložit) **vždy s `\FE0E`** (text variation selector) u Unicode šipky, jinak Safari/iOS rendí jako color emoji.

**Aplikace:**
- **Inline v body textu** — CSS automaticky `::after` ikonu, NIC nepřidávat ručně. Aktuálně Unicode glyph; při příští CSS refactor přejít na Font Awesome přes pseudo `::before` font-family hack
- **V references-list** — typed bullet `::before` vlevo, `::after` šipka suppressed (žádný duplikát)
- **V Astro komponentech** — vždy `<i class="fa-solid fa-XXX" aria-hidden="true">`

CSS rules: `apps/hodinarium-eu/src/styles/global.css` sekce „External odkazy — universal konvence ikon".

### 5.1. Wikipedia / Wikimedia Commons odkazy — kam patří

Wiki/commons odkazy primárně do `references:` v frontmatter s `type: wiki`. V textu jen tehdy, když věta organicky odkazuje na pojem (např. „[Hebrejská abeceda](wiki) má specifický číselný systém").

**„Dovětkový" link** (závorka „více ve wiki", „další info na wiki") **vždy** pryč z textu do references.

### 5.2. Odkazy na mapy — kam patří

Odkazy na mapové služby (mapy.cz, google.com/maps, openstreetmap.org, goo.gl/maps) dostávají automatic pin ikonku za textem. Pro hlavní reference patří do `references:` s `type: mapa`.

## 7. PDF embed — PdfPager komponenta

Pro PDF brožury / dokumenty v článku **NE iframe** ale direktiva `::pdf-pager`:

```markdown
::pdf-pager{src="/download/foo.pdf" title="Název dokumentu" pages="76"}
```

PDF.js z jsDelivr CDN, page-by-page navigace, fit-to-width (žádné šedé okraje). Fallback link na stažení/otevření v novém okně, pokud CDN selže nebo JS nepoběží. `pages` je OPT — initial label, finální count dotáhne PDF.js z dokumentu.

## 7a. Přehled všech CSH direktiv

V `.md` i `.mdx` souborech v `content/hodinarium-eu/`. Plugin `@csh/remark-csh-directives` mapuje na Astro komponenty bez `import` statement (Sveltia-friendly):

| Direktiva | Komponenta | Atributy |
|---|---|---|
| `::prs10-live` | PRS10Live | — |
| `::cas-slovem` | CasSlovem | — |
| `::cas-segmentovky` | CasSegmentovky | — |
| `::slunecni-klementinum` | SlunecniHodinyKlementinum | — |
| `::tabor-orloj` | TaborOrloj | — |
| `::zidovske-hodiny` | ZidovskeHodiny | — |
| `::youtube{...}` | YouTube | `id`, `title`, `align`, `ratio` |
| `::pdf-pager{...}` | PdfPager | `src`, `title`, `pages` |
| `::photo{...}` | Photo | `src`, `alt`, `class`, `author`, `authorUrl`, `license`, `licenseUrl`, `sourceUrl`, `year`, `caption` |

**Pravidla direktiv:**
- Bez argumentů → na vlastním řádku: `::prs10-live` (žádné složené závorky)
- S argumenty → vše na jeden řádek: `::name{key="value" key2="value2"}`
- Hodnoty vždy v `"..."` (i čísla jako string — komponenta si coercuje)
- Single colon `:name` (text directive) se rendruje zpět jako text — proto `12:00` v textu nezpůsobí konflikt
- Neznámá direktiva se rendruje zpět jako text + warning v build logu (graceful fallback)

**Registrace nové komponenty:** edituj `packages/remark-csh-directives/index.mjs` (DIRECTIVES map) a `apps/hodinarium-eu/src/utils/content-components.ts` (export map).

## 8. Mezititulky a struktura

- **Mezititulky → markdown `## Heading` (h2) nebo `### Subheading` (h3)**, **nikdy** `**bold paragraph**`. Globální `global.css` h2/h3 styly poskytují jednotný design.
- h2 = serif 500, copper subtle underscore vlevo dole
- h3 = brass 600, menší
- **Sekvenční mezititulek se zachová auto-anchor `id` z slugu nadpisu**

## 9. Horizontální oddělovače

Pravidlo: **vždy jen jeden** `* * *` mezi sekcemi. Vícenásobné `* * *` po sobě (legacy import často) **collapse na jeden**.

Skript `scripts/build-favicon.ts` je příklad; pro hromadný cleanup HRs napříč všemi články použij Python script (frontmatter-aware: ignoruje opening/closing `---` YAML delimiteru).

## 10. Atribuce

**Atribuce** = uvedení autorů, citace původního zdroje a poděkování. Je to umbrella term, který pokrývá tři sémanticky příbuzné věci:

1. **Autor článku** — kdo článek napsal (typicky člen spolku)
2. **Citace zdroje** — odkud byl text převzat (jiný web, kniha, archivní materiál)
3. **Poděkování** — komu vděčíme za informace, fotky, konzultaci, materiály

Všechno tohle patří **mimo hlavní text článku** — v hierarchii:

### a) Autor → `author:` ve frontmatteru → byline pod článkem

```yaml
author: "Petr Král"            # 1 autor
author: "Petr Král a Miroslav Baudisch"   # více autorů jako string
```

Helper `formatAuthor` v `Article.astro` vyrobí display formát „P. Král":
- Strip `Ing.|Dr.|Mgr.|MUDr.|RNDr.|JUDr.|PaedDr.|MgA.|prof.|doc.`
- Vezme první písmeno křestního jména (uppercase) + `". "` + příjmení
- Pokud je první část už iniciála („P." nebo „P"), normalizuje
- Příklady: `Petr Král` → `P. Král`, `Ing. Petr Král` → `P. Král`

Při refactoru existujícího článku **strip atribuci autora z těla** (typický legacy pattern „Petr Král" jako poslední řádek) → přesun do `author:`.

### b) Citace zdroje → `references:` + atribuce paragraf

Pokud byl text **převzat** odjinud (s souhlasem nebo z licence):

1. **`references:`** entry s `type: odkaz` — discoverability v sekci „Literatura a odkazy"
   ```yaml
   references:
     - title: "anatomie-varhan.cz"
       url: "http://anatomie-varhan.cz/"
       type: odkaz
       note: "Zdrojový web — text k článku převzat se souhlasem"
   ```
2. **Atribuce paragraf** na konci článku — explicit human-readable věta:
   ```markdown
   *Text byl převzat se souhlasem z webu [anatomie-varhan.cz](http://anatomie-varhan.cz/) — za poskytnutí děkujeme.*
   ```

### c) Poděkování → atribuce paragraf na konci

Pokud k vzniku článku přispěli další lidé (informace, fotky, konzultace, archivní materiály):

```markdown
*Za informace a konzultaci děkujeme A. Paříkovi, P. Skálovi a S. Marušákovi.*
```

### Slovník atribuce — `Text` / `Foto`, ne `Autor`

V atribuci **nepoužívat** slovo „Autor" (Autor: …, Autor děkuje …) — působí formálně a zatemňuje, čeho se atribuce týká. Místo toho:

- **`Text:`** — autor / původ textu článku
- **`Foto:`** — autor / původ fotek (typicky jen v Photo komponentě, ne v atribuce paragrafu)
- **`Za … děkujeme …`** — poděkování za informace, konzultaci, materiály (žádné „Autor děkuje")
- **`Text byl převzat se souhlasem z …`** — pokud byl text převzat odjinud

### Jména v atribuci — křestní jméno na iniciálu

Stejný formát jako byline: **iniciála křestního jména + tečka + příjmení**, tituly (Ing., Dr., PhDr., …) **strip**.

| Plné jméno | V atribuci |
|---|---|
| `Petr Skála` | `P. Skála` |
| `PhDr. Arno Pařík` | `A. Pařík` |
| `Stanislav Marušák` | `S. Marušák` |
| `akademický sochař Petr Skála` | `P. Skála` |
| `pan Miroslav Malovec` | `M. Malovec` (slovo `pan/paní` strip) |

Důvod: konzistence s byline, vizuální čistota, web čte i internationally — full names s tituly působí překombinovaně.

### Konvence pro atribuce paragraf

- **Italic** (jeden `*` z obou stran)
- Na **konci článku**, oddělený `* * *` od posledního obsahového paragrafu (pokud má článek několik sekcí; krátký jednoduchý článek nemusí mít hr)
- Pokud kombinuje víc typů (autoři + zdroj + poděkování), může být víc paragrafů za sebou — každý italic
- **NEPSAT do těla článku** atribuci, která patří do byline (`author:`), references (`references:`) nebo bottom paragraph

### Příklady (po normalizaci)

```markdown
*Text byl převzat se souhlasem z webu [anatomie-varhan.cz](http://anatomie-varhan.cz/) — za poskytnutí děkujeme.*

*Informace a konzultace poskytli A. Pařík, P. Skála, S. Marušák a další. Všem děkujeme.*

*Za obrázky a informace ke květinovým hodinám v Chomutově a Erlangenu děkujeme paní H. Gemmrigové.*
```

### Co kam patří — quick rule

| Typ | Kam |
|---|---|
| Autor článku (1 osoba ze spolku) | `author:` frontmatter |
| Spoluautor / kolektiv ze spolku | `author: "X a Y"` frontmatter |
| Externí zdroj (převzato) | `references:` + atribuce paragraf (`Text byl převzat …`) |
| Poděkování externím přispěvatelům | atribuce paragraf (`Za … děkujeme …`) |
| Fotokredit (autor obrázku) | `<Photo author="..." />` (ne atribuce paragraf) |

## 11. Perex / abstract

**Pravidlo:** perex se zobrazí **jen když je explicit napsán ve frontmatteru** přes `tldr: "..."`. Renderuje se s prefixem **„Stručně: …"** v rámečku pod nadpisem, před hero.

- **Manuální `tldr`** = vlastní 1–2 věty shrnutí. Mělo by být **odlišné** od prvního paragrafu článku (jinak duplicitní obsah).
- **Bez `tldr`** = článek začne rovnou textem (po hero). Pro krátké článečky a popisy exponátů typicky netřeba.

**Historicky** v jednom kroku byl auto-perex z `catalog.excerpt` pro dlouhé články, ale **byl zrušen** (commit po e760a7e) — duplikoval první paragraf článku. Pokud autor chce perex, musí ho explicit napsat.

**Doporučení pro tldr:**
- Max 2 věty, ideálně 1
- Ne kopírovat začátek prvního paragrafu — naopak abstrakt v jiném stylu (vědečtější, hutnější)
- U článků s historickými fakty: hlavní událost + datum + místo
- U exponátů: typ + původ + zvláštnost

## 12. Title nesmí obsahovat markdown

Frontmatter neparsuje markdown. `title: "**X**"` se vyrenderuje literálně s hvězdičkami v `<h1>`. Strip vždy.

## 13. Hodinarium-eu deployment URL + dev-state indexace

Ke dnešku **2026-04-29** nový Astro web žije na `https://hodinarium-eu.pages.dev`. Doména `hodinarium.eu` je **stále legacy PHP** (Petrovy programy `PRS2.php`, `PRS10_text.php`, `arduino2_polarizace.php`, /download/...).

**Při psaní zpráv pro spolupracovníky:**
- Test URL nového webu → `hodinarium-eu.pages.dev`
- Petrovy legacy PHP endpointy → `hodinarium.eu` nebo `www.orloj.eu`

Po DNS přepnutí tento bod aktualizovat.

### Indexace zablokovaná na pages.dev (dev state, od 2026-05-02)

Dokud běžíme na `*.pages.dev`, **blokujeme indexaci** — nechceme aby Google posílal lidi na dev URL místo ostré domény. Dvě vrstvy:

1. **`<meta name="robots" content="noindex, nofollow">`** + `googlebot` ekvivalent v `Base.astro` obou webů (nejsilnější — Google to respektuje, i když URL objeví z linků).
2. **`Disallow: /`** v `public/robots.txt` obou webů (brání crawl od slušných botů).

Komentáře `<!-- DEV STATE: … -->` v Base.astro a `# DEV STATE` v robots.txt fungují jako waypointy — po DNS switch je vrátit:
- `Base.astro` → smazat oba `<meta name="robots/googlebot">` bloky
- `robots.txt` → vrátit `Allow: /` + `Disallow: /og/` (utility pages)

### Jak to NEbrání vlastnímu testování

Toto blokuje **jen Google indexaci**, ne HTTP fetch:

| Co testuju | Funguje? |
|---|---|
| Vlastní crawler / link audit (lychee, broken-link-checker) | ✅ ignorují robots.txt + neřeší meta noindex |
| Lighthouse / PageSpeed Insights | ✅ fetchne HTML, hodnotí performance |
| Pagefind build, scripts/build-image-index, atd. | ✅ čtou souborový systém / dist |
| Vizuální kontrola v prohlížeči | ✅ |
| **Google Rich Results Test / Search Console** | ❌ — čte `meta robots` a respektuje noindex |
| **Google Search „site:hodinarium-eu.pages.dev"** | ❌ — Google to neindexuje |

**Když opravdu potřebuju otestovat Google rich results:**

1. **Lokálně** přes `pnpm --filter hodinarium-eu dev` — test pomocí veřejného Rich Results URL nepůjde (stejný meta tag), ale lokální dev server můžeš zkoumat přes prohlížeč/devtools.
2. **Dočasně vypnout** — v `Base.astro` zakomentovat 2 řádky `<meta name="robots">` + `<meta name="googlebot">`, deploy, otestovat na `https://search.google.com/test/rich-results`, vrátit. Trvá 1–3 min na CF rebuild.
3. **Toggle přes env var** (zatím není nasazené, kdyby se to dělalo často) — `PUBLIC_ALLOW_INDEXING=true` v CF Pages Preview environment by skipla render meta tagů. Implementuj jen kdyby se test rich results dělal opakovaně.

## 14. Build a deploy

**Cloudflare Pages** spouští `pnpm build` (= `astro check && astro build`). Pokud `astro check` selže (jakákoliv ts chyba), **deploy nedoběhne** a všechny commity od posledního zelené buildu visí.

**Lokálně** vždy `pnpm build` (NE `npx astro build` — ten skipuje `astro check` a propustí ts chyby, které pak rozbijí CF deploy).

Když CF zaseknutý: zkontroluj `Cloudflare dashboard → Pages → hodinarium-eu/horologie-cz → Deployments` na poslední failed build a chybu.

## 15. Migrace existujících článků

Hromadná migrace 200+ legacy `.md` → MDX a strukturní pravidla = velký job. **Nedělat hromadně** — postupně při editaci článku doplnit:
- `author: "..."` ve frontmatter (a strip atribuci z těla)
- `references:` s wiki/mapa/pdf odkazy z těla
- Markdown `![alt](src)` → `<Photo>` u obrázků s atribucí
- `**bold subhead**` → `## subhead`
- Single `* * *` (collapse duplicit)

## 16. Odkazy užitečné pro práci s repem

- `pnpm imgindex:build` (`scripts/build-image-index.ts`) — regeneruje `image-sizes.json` po přidání obrázku do public/img/
- `pnpm catalog:hodinarium` (`scripts/build-catalog.ts`) — generuje `catalog.json` (excerpt, wordCount, year, …); excerpt skipne CSH direktivy (`::photo{...}`, `::prs10-live`, …), JSX bloky a MDX import statements (legacy medailony) → tldr-auto v Article.astro nedostane direktivu jako perex
- `pnpm favicon:build` (`scripts/build-favicon.ts`) — favicon + homescreen ikony z logo-csh.svg
- `python3 scripts/devignette.py file1 file2 …` — inverse-vignette correction pro legacy fotky s ztemnělými rohy. Args: `--strength N` (default 0.4 = +40% jas v rozích), `--in-place` (přepíše vstup; jinak `*_devign.jpg`). Algoritmus: pro každý pixel norm. distance od středu × strength → multiply jas
- Skript pro hromadný cleanup HRs — viz Python inline v conversation history (frontmatter-aware HR collapse)

## 17. Reference style (bullet vs numbered)

`references[]` v article frontmatter podporuje **dva styly** zobrazení, řízené `referenceStyle:` field:

### A) `bullet` (default) — souhrnný seznam pod článkem

Hodí se pro **většinu článků**. Položky se zobrazí jako odrážkový seznam s ikonou podle `type` (W pro wiki, pin pro mapa, 📖 pro kniha, ⤓ pro pdf, § pro článek, · pro odkaz). V těle článku se přímo neodkazuje — reference jsou „další zdroje" nebo „dovětky".

```yaml
referenceStyle: bullet  # nebo neuvedeno (default)
references:
  - title: "Hebrejská abeceda"
    url: "https://cs.wikipedia.org/wiki/Hebrejská_abeceda"
    type: wiki
```

### B) `numbered` — citované reference s anchory

Pro **odborné články s přesnými citacemi**. Položky v references-list se vyrenderují jako `[1]`, `[2]`, …; v textu se odkazuje přes komponentu `<Ref n={N}>`, která vyrenderuje superscript `[N]` → `#ref-N` anchor.

```yaml
referenceStyle: numbered
references:
  - title: "PRS10 manuál"
    url: "https://www.thinksrs.com/downloads/pdfs/manuals/PRS10m.pdf"
    type: pdf
  - title: "About the radioactivity of atomic clocks"
    url: "https://www.thinksrs.com/downloads/pdfs/other%20stuff/PRS10_radioactivity.pdf"
    type: pdf
```

```mdx
import Ref from '../../apps/hodinarium-eu/src/components/Ref.astro';

PRS10 je rubidiový oscilátor<Ref n={1} /> s nízkým fázovým šumem. Radioaktivita
je nižší než u banánu<Ref n={2} />.
```

CSS counter() inkrementuje `[1]`, `[2]`, … u `<li>` v references. `:target` zvýrazní položku, na kterou jsme přišli z `<Ref>`.

### Kdy který styl

| Typ článku | Doporučený styl |
|---|---|
| Popis exponátu, vyprávění, popularizační | `bullet` (default) |
| Technický článek s přesnými citacemi | `numbered` |
| Souhrn legacy webu s odkazy „více na…" | `bullet` |
| Vlastní výzkum / publikace | `numbered` |

Můžeš hybridnout — `referenceStyle: numbered` ale v textu **nepoužít** `<Ref>`. Numbering je tam tak jako tak (jen čtenář nenajde kotvy zpětně). Stejně tak `bullet` styl s `<Ref>` v textu funguje (anchor projde), ale uživatel uvidí `[1]` jako text bez vizuální reference k seznamu.

## 18. Kontrola MD → HTML konverze (legacy import artefakty)

Většina článků pochází z **legacy import** z hodinarium.eu (HTML → markdown přes turndown). Konverze není dokonalá a zanechává artefakty, které **při buildu silently projdou** a vyrenderují se chybně. Při editaci článku **vždy projít** a zkontrolovat:

### Časté artefakty z importu

| Vzor v MDX | Problém | Oprava |
|---|---|---|
| `**[text](url)**word` | bold + link bez whitespace za `**` — markdown to neparsuje jako bold; rendruje se literální `**` | strip bold (`[text](url)` stačí), přidat space před následujícím slovem |
| `**X**text` (bez mezery) | nezavřený bold — všechen následující text je bold až do dalšího `**` | přidat mezeru za uzavírací `**` |
| `***Na text...** ...*` | 3 hvězdičky vlevo, 2 vpravo — italický `Na text...` v bold, ale uzavření asymetrické | Strip nebo přepsat na čisté `*Na text… vůbec.*` (jen italika) |
| `**Co tvoří hodiny hodinami**` na samostatném řádku | bold paragraph místo nadpisu | změnit na `## Co tvoří hodiny hodinami` |
| `* * *` třikrát po sobě | duplicate horizontal rules | collapse na jeden (script v conversation history) |
| `[odkaz na **něco**](url)` | bold uvnitř link textu | OK, funguje, ale často nadbytečné — zvážit strip bold |
| `*[odkaz](url)*` | italika kolem linku | OK, funguje, ale často špatně z importu — zkontrolovat sémantiku |
| `text. ![alt](src)` (image inline na konci paragrafu) | image jako float „lepený" za text | přesunout na samostatný řádek nebo do správné sekce |
| `Petr Král` na konci článku | atribuce v body (legacy pattern) | strip a doplnit `author: "Petr Král"` ve frontmatter |

### Workflow při revizi článku

1. **Otevři live náhled** na pages.dev — porovnej s legacy `hodinarium.eu/<slug>.htm`. Najdi vizuálně rozbité kusy (rozjeté `**`, divné mezery, duplicate `<hr>`).
2. **Strip atribuci z body** (Petr Král / Ing. Petr Král) → `author:` ve frontmatter.
3. **Convert bold subheadings** (`**Title**` na samostatném řádku) → `## Title`.
4. **Promote wiki/mapa odkazy** z body do `references:` (kde věta není organická — typicky „více v…" nebo závorka).
5. **Strip duplicitní `* * *`** — nech jen jeden.
6. **Hero**: pokud první obrázek má atribuci (Wikimedia, archiv), vyměnit `![](src)` → `<Photo>` s credit prop.
7. **Build lokálně** `pnpm build` — `astro check` chytne typed errors; vizuální MD problémy chytí jen lidská kontrola.

### Plánovaná hromadná revize

Existuje **200+ článků** z legacy importu. Hromadný script-based fix je rizikový — heuristika nezvládne semantiku. **Strategie:** revize postupně při dotyku článku (editing trigger), plus jednou za čas „revize sweep" — projít top 20 nejnavštěvovanějších článků (podle analytics, až budou) a procesovat manuálně.

Při revizi **vždy** zachytit specifické artefakty, které se objeví, a doplnit je do tabulky výše — abychom z opakování viděli pattern a mohli pak napsat targeted regex/script.

## 19. Kdy spawnovat `cestina` skill

Při delším českém textu článku (popis, perex, references title, sekce) je užitečné nechat ho zkontrolovat skillem **cestina** — odstraní AI-tells, slovakismy, anglicismy a opravu české typografie (uvozovky, pomlčky, mezery u jednotek).

Triggery: psaní `tldr`, `note` v references, dlouhé sekce v `<Photo>` alt textu, věty s technickým názvoslovím, kde Claude může klouznout do anglicismů.
