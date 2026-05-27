---
name: persona-composer
description: Compose Dutch-context personas on-demand from external trait pools and pre-authored coupled archetype bundles. Returns 1-30 composed personas given optional constraints (domain + role catalog, count, diversity requirements, output format). All output in Dutch. Callable by other skills (ontdek-kansen, business-case-management, user-research) via the Skill tool when they need disposable, domain-relevant persona sets.
argument-hint: "[natural-language request OR JSON constraints block]"
---

# Persona Composer

Je stelt Nederlandse personas samen door **pre-geschreven gekoppelde archetype-bundles** te combineren met **onafhankelijke trait-pools**. Je genereert niet vanaf nul — je assembleert uit catalogi onder `data/`. Output is in het Nederlands tenzij de caller expliciet anders vraagt.

## Kernaanpak

Een persona bestaat uit twee lagen:

1. **Gekoppelde bundels** (12 families): vooraf geschreven clusters van sterk correlerende traits (bv. werk ↔ inkomen ↔ huishouden ↔ woonvorm). Willekeurig combineren van hun onderdelen produceert implausibele mensen, dus ze worden als geheel gekozen.
2. **Onafhankelijke traits**: hobbies, media, tech, attitudes, dieet, sociale stijl, dagelijkse routine. Deze kiezen we per persona uit trait-pools, gefilterd op compatibility-tags.

Compositie = voor elke persona één bundle uit elke familie + onafhankelijke overlay + optionele domein-rol + optionele behavioral layer.

## Input-contract

De caller geeft één van:

### A — Natuurlijke taal
Voorbeeld: "8 NL mantelzorgers, diverse leeftijd, 30% migratie-achtergrond, slim format"

### B — JSON-block (voorkeur voor programmatische aanroep)
```json
{
  "count": 8,
  "domain": "zang" | null,
  "domain_role_catalog": ["zangleraar", "koorlid-beginner", ...] | null,
  "diversity": {
    "age_bands": ["<25", "26-45", "46-65", "65+"],
    "regions": ["G4", "middelgroot", "dorp"],
    "ses": ["laag", "midden", "hoog"],
    "migration_bg_share": 0.25,
    "gender_mix": { "m": 0.45, "v": 0.45, "x": 0.10 }
  },
  "output_format": "full" | "slim" | "narrative-only",
  "behavioral_layer": true | false,
  "return_as": "markdown" | "structured-json",
  "output_dir": "<optional caller-specified path>"
}
```

### Defaults bij ontbrekende velden
| Veld | Default |
|---|---|
| `count` | interview-modus (vraag om count) |
| `domain` | `null` (geen rol-overlay) |
| `diversity` | redelijke spreiding over leeftijd + regio + SES |
| `output_format` | `slim` |
| `behavioral_layer` | `false` |
| `return_as` | `markdown` |
| `output_dir` | `composed-personas/<YYYY-MM-DD-HHmm>/` in caller's cwd |

### Interview-modus
Als input onduidelijk is, vraag **alleen** naar: `count`, `domain` (optioneel), en ruwe `diversity`-wensen. Daarna direct composeren.

## Data-laag

Alle catalogi leven onder `${CLAUDE_PLUGIN_ROOT}/skills/persona-composer/data/`:

```
data/
├── archetype-bundles/             # 12 families, elk met meerdere MD-bundles
│   ├── work-family-housing/
│   ├── faith-routine-worldview/
│   ├── health-work-arrangement/
│   ├── identity-politics-social-trust/
│   ├── education-career-mobility/
│   ├── migration-generation-culture/
│   ├── regional-rootedness/
│   ├── parenthood-partnership-timepoverty/
│   ├── life-stage-transition/
│   ├── expertise-information-trust/
│   ├── caregiving-boundary/
│   └── financial-precarity-coping/
├── independent-traits/
│   ├── hobbies.yaml
│   ├── media-consumption.yaml
│   ├── tech-profile.yaml
│   ├── attitudes-sustainability.yaml
│   ├── attitudes-privacy.yaml
│   ├── attitudes-technology.yaml
│   ├── attitudes-health.yaml
│   ├── attitudes-housing.yaml
│   ├── attitudes-immigration.yaml
│   ├── diet-patterns.yaml
│   ├── social-style.yaml
│   ├── daily-routine-templates.yaml
│   ├── domain-roles/
│   │   └── zang.yaml (+ later andere domeinen)
│   └── names/
│       ├── first-names-nl.yaml
│       ├── first-names-migrant.yaml
│       └── last-names.yaml
└── demographics/
    ├── regions.yaml
    ├── occupations.yaml
    └── income-bands.yaml
```

Laad **selectief** — nooit alle bundles tegelijk inlezen. Eerst de `## Tags` blokjes scannen, dan alleen de geselecteerde bundle volledig lezen.

## Bundle-formaat

Elke bundle is een markdown-file met deze secties:

```markdown
# <bundle-id>: <korte titel>

## Tags
age-band: <min-max of lijst>
region: <G4 / middelgroot / dorp / krimpregio / biblebelt / ...>
urbanization: <1-5>
ses: <laag / midden / hoog / variabel>
household: <single / dual-income-no-kids / gezin-jong / gezin-tiener / empty-nester / single-parent / ...>
housing: <huur-sociaal / huur-vrij / koop-appartement / koop-huis / ouderlijk / ...>
education: <VMBO / MBO / HAVO / HBO / VWO / WO>
migration-bg-compatible: <any / nl-only / migration-1st / migration-2nd / migration-3rd>
variant-hash: <unique-id binnen familie>

## Incompatible-with
- <lijst met bundle-ids of tag-criteria die uitgesloten zijn>

## Narrative building-blocks
### Work
<2-4 zinnen, concreet en NL>

### Family
<2-4 zinnen>

### Housing
<2-4 zinnen>

### Financial picture
<2-4 zinnen>

### Compositie-hooks
Overlay-bias voor onafhankelijke trait-pools:
- hobby: <bias>
- attitudes: <bias>
- media: <bias>
```

## Trait-pool-formaat (YAML)

```yaml
# hobbies.yaml
- id: koorzang
  label: Koorzang (wekelijks, amateur-koor)
  tags:
    age: [26-45, 46-65, 65+]
    ses: [laag, midden, hoog]
    region: [G4, middelgroot, dorp]
    bundle-affinity: [faith-routine-worldview, regional-rootedness]
- id: padel
  label: Padel (2x/week met collega's)
  tags:
    age: [26-45]
    ses: [midden, hoog]
    region: [G4, middelgroot]
```

## Compositie-algoritme

Voor een aanroep met `count = N`:

### Stap 1 — Slot-planning
Verdeel N personas over de diversity-constraints. Bijvoorbeeld `count=8, age_bands=["<25","26-45","46-65","65+"], migration_bg_share=0.25`:
- Slot-plan: 2 × `<25`, 3 × `26-45`, 2 × `46-65`, 1 × `65+`; 2 slots met migratie-bg; regio-verdeling proportioneel
- Elke slot krijgt een constraint-profiel mee

### Stap 2 — Bundle-lock per slot
Voor elke slot:
1. Lees alle `## Tags`-blokken uit alle 12 families (snel, alleen metadata)
2. Filter per familie op compatible bundles voor deze slot
3. Kies één bundle per familie die onderling niet botsen (check `Incompatible-with`)
4. Als geen combinatie mogelijk: relax één constraint (eerst SES, dan regio), en probeer opnieuw

### Stap 3 — Independent overlay
Voor elke slot met gelockte bundles:
1. Lees de trait-pools die nodig zijn
2. Per pool: filter op slot-constraints + bundle-compatibility-tags + `Compositie-hooks` uit de bundels
3. Kies 1 entry (bv. tech-profile) of 2-4 entries (bv. hobbies)

### Stap 4 — Domein-rol (optioneel)
Als `domain_role_catalog` opgegeven:
1. Kies één rol uit de catalogus
2. Rol mag 1-2 onafhankelijke traits nudgen (bv. "zangleraar" → zorg dat `koorzang` of `solozang` in hobby-overlay zit)
3. Rol overrult geen bundel. Als rol incompatibel met gelockte bundels → re-roll bundels, niet de rol

### Stap 5 — Naamgeving
Kies voornaam uit juiste namenpool op basis van geboortejaar (afgeleid van leeftijdsband) en migratie-bg-tag. Achternaam uit `last-names.yaml`.

### Stap 6 — Behavioral layer (optioneel)
Als `behavioral_layer: true`: derive 18 behavioral-velden uit de narrative-cluster volgens de derivation-rules (geïnspireerd op `generate-realistic-person`). Label onzekere velden als `inferred` of `speculative`.

### Stap 7 — Plausibility-check
Run `consistency/plausibility-rules.md` + `implausible-combinations.yaml`:
- Hard fails → re-roll bundels
- Soft warns → log in `### Notes` van de persona
- Bij 2x hard fail op dezelfde combo → markeer combo als implausibel, kies andere

### Stap 8 — Render
Genereer markdown in het opgegeven `output_format`:

**`full`** (~20 secties): matcht stijl van bestaande `personas/` files

**`slim`** (13 secties): Background / Demographics / Work / Income & status / Family / Housing / Health & lifestyle / Personality & values / Hobbies & interests / Tech & media / Attitudes / Goals / Pains & frustrations

**`narrative-only`** (~1 paragraaf): één achtergrondalinea + basis-demografie + 1 hobby + 1 attitude

Elke persona krijgt een trailing traceerbaarheidsblok:

```markdown
### Compositie
- work-family-housing: <bundle-id>
- faith-routine-worldview: <bundle-id>
- health-work-arrangement: <bundle-id>
- identity-politics-social-trust: <bundle-id>
- education-career-mobility: <bundle-id>
- migration-generation-culture: <bundle-id>
- regional-rootedness: <bundle-id>
- parenthood-partnership-timepoverty: <bundle-id>
- life-stage-transition: <bundle-id>
- expertise-information-trust: <bundle-id>
- caregiving-boundary: <bundle-id>
- financial-precarity-coping: <bundle-id>
- hobbies: [<ids>]
- media: [<ids>]
- tech: <id>
- attitudes: {sustainability: <stance-id>, privacy: <>, ...}
- diet: <id>
- social-style: <id>
- daily-routine: <id>
- domain-role: <id> (if provided)
- composer-version: 0.1.0
- timestamp: <ISO>
```

### Stap 9 — Schrijven en manifest
Schrijf elk persona-bestand naar `<output_dir>/<slot-nr>_<voornaam>_<achternaam>_<plaats>.md`. Schrijf een `manifest.json`:

```json
{
  "timestamp": "2026-04-20T15:30:00Z",
  "composer_version": "0.1.0",
  "request": { ... original input ... },
  "personas": [
    {
      "slot": 1,
      "file": "1_anouk_de_vries_amsterdam.md",
      "age": 28,
      "region": "G4",
      "ses": "midden-hoog",
      "migration_bg": false,
      "domain_role": "hobby-karaoke",
      "bundles": { "work-family-housing": "wfh-001", ... }
    },
    ...
  ]
}
```

## Beperkingen en grenzen

| Situatie | Gedrag |
|---|---|
| `count > 30` | Weiger: "Composer cap is 30 per call — splits de aanvraag of roep meerdere keren aan" |
| `count < 1` | Weiger |
| `data/` deels ontbreekt | Stop, lijst missing files op |
| Domein opgegeven, `domain-roles/<domein>.yaml` ontbreekt | Ga door zonder rol-overlay, flag in output |
| Diversiteit onhaalbaar (bv. 8 × 85+ × G4 × migratie-bg terwijl geen bundel-combinatie bestaat) | Compose wat mogelijk is, flag tekort in manifest |
| Bundle heeft geen `## Tags` of slecht geformatteerd | Skip die bundle, log waarschuwing |
| Blacklist-combo keert terug in 3 achtereenvolgende re-rolls | Markeer slot als "impossible-under-constraints", vul met best-effort + log |

## Consistency-regels (kort)

**Hard fails (re-roll):**
- Leeftijd >70 + beroep dat ≥40u fysieke arbeid vereist
- Professioneel atleet + leeftijd >40 (tenzij "gepensioneerd" of "coach")
- "Conservatoriumstudent" + leeftijd >35
- Eigen huis in Amsterdam-centrum + SES laag

**Soft warns (in Notes):**
- SGP-kiezer + Amsterdam-centrum wonen
- Leeftijd <22 + eigen koopwoning
- Migratie-2e-gen + "opgegroeid in Friese krimpregio"

**Blacklist:** zie `consistency/implausible-combinations.yaml`

Volledige set: `consistency/plausibility-rules.md`

## Falingsgedrag

| Situatie | Antwoord |
|---|---|
| Geen input | Interview-modus |
| `count` niet opgegeven | "Hoeveel personas wil je?" |
| Onhaalbare diversiteit | Compose partieel, flag tekort |
| Request buiten scope (bv. "genereer een business case") | "Deze skill stelt personas samen. [Verzoek] valt buiten scope." |

## Self-check

Voordat je de output presenteert:

```
[] Slot-plan dekt de opgegeven diversity-constraints
[] Elke persona heeft 12 bundel-keuzes (één per familie)
[] Elke persona heeft independent-overlays (hobbies, media, tech, attitudes, diet, social, routine)
[] Naamkeuze past bij leeftijdsband en migratie-bg-tag
[] Plausibility-check is gedraaid per persona
[] Geen hard-fail-combinaties in output
[] Elk output-bestand heeft een ### Compositie traceer-footer
[] manifest.json bestaat en matcht de files
[] Output-taal is Nederlands (tenzij caller anders vroeg)
[] Output geschreven naar opgegeven of default output_dir
```

## Voorbeelden

### Voorbeeld 1 — Slim set voor ontdek-kansen zang
**Input** (JSON van caller):
```json
{
  "count": 8,
  "domain": "zang",
  "domain_role_catalog": ["zangleraar","koorlid-beginner","conservatoriumstudent","semi-prof-vocalist","hobby-karaoke","koordirigent","logopedist","stemrevalidatie-volwassene"],
  "diversity": {
    "age_bands": ["<25","26-45","46-65","65+"],
    "regions": ["G4","middelgroot","dorp"],
    "ses": ["laag","midden","hoog"],
    "migration_bg_share": 0.25
  },
  "output_format": "slim",
  "behavioral_layer": false
}
```

**Verwachte acties**: slot-plan → 8 bundel-locks → 8 independent overlays → 8 rollen uit catalogus → render slim → schrijf 8 .md files + manifest.json.

### Voorbeeld 2 — Één enkele persona voor business case
**Input**: `{"count": 1, "output_format": "full", "behavioral_layer": true}`

**Verwachte acties**: één slot, volledige compositie, full render met behavioral layer.

### Voorbeeld 3 — Natuurlijke taal
**Input**: "30 diverse NL volwassenen, narrative-only, geen domein"

**Verwachte acties**: interpreteer naar JSON (count=30, output_format=narrative-only, diversity default), compose, render.

### Voorbeeld 4 — Geen input
**Input**: (niets)

**Verwachte acties**: interview-modus.

### Voorbeeld 5 — Out of scope
**Input**: "Maak een persona en schrijf er meteen een business case voor"

**Verwachte acties**: "Deze skill stelt personas samen. Voor business cases, roep `/business-case-management` aan met de composer-output als input."
