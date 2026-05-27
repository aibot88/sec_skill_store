---
name: ai-media
description: >-
  AI Media Generator — generování produktových fotek a B-roll videí přes fal.ai.
  Expert-level prompting pro food/beverage/FMCG produkty.
  Image gen (FLUX, Seedream) + Image-to-Video (Kling, Veo).
  5-vrstvá prompt anatomie pro konzistentně kvalitní výstupy.
  Trigger: "ai media", "vygeneruj fotku", "rozpohybuj", "B-roll",
  "product shot", "ai obrázek", "ai video", "/ai-media"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# AI Media Generator — expert prompting pro produktovou fotografii a video

## Kdy použít
- Chceš vygenerovat produktovou fotku nebo lifestyle záběr
- Potřebuješ B-roll video z existující produktovky (rozpohybovat produkt)
- Generování atmosférických záběrů pro reklamy (kuchyně, zahrada, akce)
- Batch generování více variant pro A/B testing
- Jakákoliv AI image/video generace pro e-commerce nebo marketing

## Filozofie

Kvalitní AI obrázek nevznikne z jednořádkového promptu. Tento skill ti dává **5-vrstvou strukturu promptu**, která konzistentně produkuje profesionální výsledky — ne náhodné AI artefakty.

## Stack

| Účel | Model | fal.ai ID | Cena |
|------|-------|-----------|------|
| Image — budget | FLUX.1 Dev | `fal-ai/flux/dev` | ~$0.025/img |
| Image — quality | FLUX.2 Pro | `fal-ai/flux-pro/v1.1` | ~$0.035/img |
| Image — food specialist | Seedream 3.0 | `fal-ai/seedream-3` | ~$0.018/img |
| Video — standard I2V | Kling 2.0 | `fal-ai/kling-video/v2/master/image-to-video` | ~$0.065/sec |
| Video — premium I2V | Kling 3.0 | `fal-ai/kling-video/v3/standard/image-to-video` | ~$0.084/sec |

### Setup

```bash
pip install fal-client

# Ulož API klíč (získej na fal.ai)
mkdir -p config/local
echo '{"api_key": "YOUR_FAL_KEY"}' > config/local/fal.json
```

## PROMPT ANATOMIE — 5 vrstev

Každý prompt sestav z těchto 5 vrstev. Prompt MUSÍ být anglicky.

### Vrstva 1: Subject Anchor (CO)
Hlavní subjekt — buď ultra-specifický. Pojmenuj materiály, barvy, tvary.

```
ŠPATNĚ: "a sauce bottle on a table"
DOBŘE: "A 347ml glass bottle with dark green fermented sauce,
        red metal screw cap, cream-colored label with bold logo,
        sitting on aged oak cutting board"
```

**Pro produkty vždy zahrň:**
- Typ obalu (sklo, plast, plechovka, krabice)
- Barvu obsahu/produktu
- Materiál a barvu uzávěru
- Etiketu — barva, typografie, klíčový text
- Rozměr (pomáhá s proporcemi)

### Vrstva 2: Environment & Composition (KDE)
Prostředí, pozadí, kompozice, perspektiva.

| Typ záběru | Environment popis |
|------------|-------------------|
| Hero product | "centered on [surface], [background], [surrounding props]" |
| Lifestyle | "in a [location], [activity happening], [ambient details]" |
| Flat lay | "overhead birds-eye view of [arrangement] on [surface]" |
| Detail/macro | "extreme close-up of [detail], filling the frame" |

**Povrchy pro food:** rustic oak, weathered marble, dark slate, worn butcher block, raw linen cloth, terracotta tile
**Pozadí:** deep charcoal gradient, blurred kitchen, morning garden bokeh, warm brick wall, dark moody void
**Props:** fresh herbs (basil, rosemary, thyme), scattered peppercorns, cherry tomatoes on vine, olive oil drizzle, sea salt flakes, wooden spoon, cast iron skillet

### Vrstva 3: Lighting & Mood (JAK svítí)
Nejdůležitější vrstva pro kvalitu. Buď extrémně specifický.

| Lighting typ | Prompt fráze | Kdy použít |
|-------------|--------------|------------|
| Rembrandt | "Rembrandt lighting from 45° upper left, single key light, deep shadows on right side" | Dramatické hero shoty |
| Window light | "soft diffused natural window light from the left, gentle shadows, no harsh highlights" | Lifestyle, cooking |
| Golden hour | "warm golden hour backlight, long shadows, lens flare peeking through" | Outdoor, garden |
| Studio | "three-point studio lighting, key light from left, fill from right, hair light from above, pure white background" | Clean e-shop produktovky |
| Moody | "single overhead spotlight, deep shadows, chiaroscuro, dark atmospheric mood" | Premium/luxury |
| Practical | "warm tungsten pendant lamp overhead, candlelight on table, mixed warm sources" | Dinner scenes |

**Pro sklo a tekutiny (KRITICKÉ):**
```
"light refracting through the glass bottle, visible liquid texture inside,
 caustic light patterns on the surface behind, subtle condensation droplets
 on the glass surface"
```

### Vrstva 4: Camera & Lens (ČÍM)
Simuluj konkrétní fotografické vybavení.

| Efekt | Prompt fráze |
|-------|-------------|
| Bokeh pozadí | "shot with 85mm f/1.4 lens, creamy bokeh background, razor-sharp subject" |
| Vše ostré | "shot with 35mm f/8, deep depth of field, everything in focus" |
| Macro detail | "100mm macro lens, f/2.8, extreme detail on texture and surface" |
| Wide context | "24mm wide angle, showing full scene with product as focal point" |
| Overhead | "shot directly from above with 50mm lens, flat perspective, no converging lines" |
| Cinematic | "anamorphic 40mm lens, slight oval bokeh, cinematic 2.39:1 crop, film grain" |

### Vrstva 5: Style & Quality Seal (STYL)
Poslední věta — definuje celkový grade.

**Pro produktovky:**
```
"Professional food product photography, editorial quality, published in
Bon Appétit magazine. High resolution, crisp details, natural color grading.
No watermarks, no text artifacts, no AI distortions on the label."
```

**Pro lifestyle:**
```
"Candid documentary photography style, authentic and lived-in feel,
warm earth tone color grade. Shot on medium format Hasselblad.
No staged look, no stock photo feel, no oversaturated colors."
```

**Pro moody/luxury:**
```
"Dark and moody food photography, inspired by Gentl & Hyers studio work.
Rich shadows, selective highlights, matte finish. Museum-quality print resolution.
No flat lighting, no overexposure, no plastic-looking textures."
```

---

## NEGATIVE PROMPTS

Vždy přidej na konec:

**Univerzální:**
```
No watermarks, no signatures, no AI artifacts, no blurry areas,
no distorted text on labels, no extra fingers or limbs.
```

**Pro produktovky navíc:**
```
No incorrect label text, no misspelled words, no warped bottle shape,
no floating objects, no inconsistent lighting direction, no plastic-looking glass.
```

**Pro food navíc:**
```
No unappetizing colors, no raw meat look on cooked food,
no unnaturally perfect arrangements, no stock photo sterility.
```

---

## IMAGE-TO-VIDEO PROMPTING (Kling / Veo)

### Camera Movement Vocabulary

| Pohyb | Prompt | Kdy použít |
|-------|--------|------------|
| Orbit | "Camera slowly orbits around the subject, 30° arc from left to right" | Product hero reveal |
| Push in | "Slow dolly push-in toward the label, smooth and steady" | Detail emphasis |
| Pull back | "Camera gently pulls back revealing the full scene" | Context reveal |
| Crane up | "Camera slowly rises from table level upward, tilting down" | Dramatic product shot |
| Tracking | "Smooth lateral tracking shot from left to right" | Lineup/multiple products |
| Static + zoom | "Locked camera position, very slow zoom in, barely perceptible" | Subtle elegance |

### Environment Animation

Přidej subtilní pohyb prostředí (ne jen kamery):

```
"Wisps of steam gently rising from the food"
"Soft bokeh lights slowly shifting in the background"
"Herbs slightly swaying as if from a gentle breeze"
"Condensation droplet slowly rolling down the glass surface"
"Warm light gradually intensifying, golden hour progression"
"Subtle dust particles floating in the light beam"
```

### Anti-warping pravidla

Pro minimalizaci AI artefaktů ve videu:

1. **Jeden pohyb najednou** — nekombinuj orbit + zoom + pan
2. **"Slow" a "gentle"** — vždy přidej, rychlé pohyby = warping
3. **"The [product] remains perfectly still"** — explicitně řekni co se NEMÁ hýbat
4. **Jednobarevné pozadí** — jednodušší pro model, méně artefaktů
5. **"Maintaining consistent lighting throughout"** — zabrání blikání
6. **"Photorealistic, no morphing, no distortion"** — quality seal pro video

### Video Prompt Template

```
[Camera movement], [speed qualifier].
[Subject description — what stays still].
[Environment animation — what moves subtly].
[Lighting consistency note].
[Quality: "Cinematic product commercial, photorealistic,
no morphing or warping artifacts"]
```

---

## HOTOVÉ PROMPT ŠABLONY

### Image: Hero Product (dark moody)
```
A [product description with materials, colors, packaging details],
centered on a dark weathered oak cutting board. Fresh herbs and ingredients
arranged beside it. Rembrandt lighting from 45° upper left, deep shadows
falling to the right, warm amber key light reflecting through the packaging.
Shot with 85mm f/1.4 lens, razor-sharp focus on the label, creamy dark bokeh
background. Professional food photography, editorial quality for Bon Appétit.
No watermarks, no text artifacts, no distorted label.
```

### Image: Hero Product (clean studio)
```
A [product description], centered on pure white background. Three-point studio
lighting, soft shadows beneath the product, clean reflections on the surface.
Shot with 100mm macro lens at f/8, everything tack-sharp, studio product
photography for e-commerce catalog. High resolution, crisp details,
true-to-life colors. No background distractions, no color cast.
```

### Image: Lifestyle Kitchen
```
A person's hands using [product] in a warm kitchen scene with wooden countertop,
blurred copper pots in background, fresh herb garden on windowsill. Soft natural
window light from the right side, steam rising from hot food, shallow depth of
field. Shot on 50mm f/1.8, candid documentary style, authentic lived-in kitchen.
Warm earth tone color grade, not overstyled. No stock photo feel, no AI artifacts.
```

### Image: Flat Lay Ingredients
```
Overhead birds-eye view of cooking ingredients arranged on dark slate surface.
Center: [product, opened/displayed]. Around it: complementary ingredients
arranged aesthetically. Soft even overhead lighting, no harsh shadows,
each item clearly visible. Shot directly from above with 50mm lens, flat
perspective. Clean food styling, editorial recipe photography.
No cluttered composition, no overlapping items obscuring each other.
```

### Video: Product Orbit (from photo)
```
Camera performs a smooth slow orbit around the product, arcing 30 degrees
from left to right over 5 seconds. The product remains perfectly still and
sharp throughout. Soft background light gradually shifts, creating moving
highlights on the surface. Consistent warm lighting, no flickering or color
shifts. Cinematic product commercial, photorealistic, no warping artifacts.
```

### Video: Product Reveal
```
Camera slowly rises from table level, revealing a product lineup on a styled
surface. Gentle crane-up movement, smooth and steady. Background transitions
from blurred to slightly more defined. Warm golden lighting consistent
throughout. Premium product commercial aesthetic, no morphing, photorealistic.
```

---

## PROMPT ITERATION PLAYBOOK

| Problém | Fix |
|---------|-----|
| Obal vypadá plastově | Přidej "real glass/metal material, visible texture, light refraction" |
| Etiketa je nečitelná | Přidej "clean readable label text, sharp typography" |
| Příliš AI look | Přidej "film grain, subtle imperfections, not digitally perfect" |
| Scéna je plochá | Změň lighting na Rembrandt nebo přidej "dramatic chiaroscuro" |
| Jídlo nevypadá chutně | Přidej "appetizing, glistening, fresh, steam rising, just-cooked look" |
| Video se warpuje | Zjednoduš prompt — jeden pohyb, přidej "[product] remains perfectly still" |
| Video je moc statické | Přidej environment animation (steam, bokeh shift, light change) |
| Barvy jsou off | Specifikuj "warm earth tones, [specific color palette]" |
| Pozadí ruší | Přidej "heavily blurred background, f/1.4 bokeh" |

## Spuštění

### Přímé volání fal.ai
```python
import fal_client, os, json

os.environ['FAL_KEY'] = json.load(open('config/local/fal.json'))['api_key']

# Image generation
result = fal_client.subscribe("fal-ai/flux/dev", arguments={
    "prompt": "... your 5-layer prompt ...",
    "image_size": {"width": 1024, "height": 1024},
})
print(result["images"][0]["url"])

# Image-to-Video
result = fal_client.subscribe("fal-ai/kling-video/v2/master/image-to-video", arguments={
    "prompt": "... camera movement prompt ...",
    "image_url": "https://url-to-your-image.jpg",
    "duration": "5",
})
print(result["video"]["url"])
```

### Model selection guide

| Situace | Model | Proč |
|---------|-------|------|
| Quick test / draft | FLUX.1 Dev | Levný, rychlý, dostatečný pro iteraci |
| Finální produktovka | FLUX.2 Pro | Nejlepší detaily, nejmenší artefakty |
| Food/drink specialista | Seedream 3.0 | Trénovaný na food, nejlepší textury jídla |
| Video — spolehlivý | Kling 2.0 | Méně warpingu, konzistentní |
| Video — premium | Kling 3.0 | Lepší detaily, ale občas nestabilní |

## Pravidla

1. Prompt VŽDY anglicky, komunikace s uživatelem v jeho jazyce
2. Před generováním VŽDY ukázat prompt ke schválení
3. Po generování nabídnout iteraci (upravit prompt / další varianta / hotovo)
4. Pro video: jeden pohyb najednou, vždy "slow" a "gentle"
5. Batch generování: max 5 současně (fal.ai rate limit)
6. Zdrojové fotky a výstupy necommituj do gitu

$ARGUMENTS
