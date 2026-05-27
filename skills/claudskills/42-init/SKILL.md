---
name: 42-init
description: >
  Bootstrap een klantproject voor 42-SEO-Skills. Vraagt naar profiel
  (content/ecom/technical/full), activeert alleen relevante skills via
  disabledSkills in .claude/settings.local.json, zet auth (.env) op,
  maakt de gedeelde Python venv in ~/.claude/venvs/42-seo/, en prikt
  42-reports/<klant>/ neer. Use when user says "init SEO project",
  "42-init", "setup SEO", "nieuw klantproject", "initialiseer SEO".
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
version: 1.0.0
tags: [init, bootstrap, setup, onboarding]
---

# /42-init — Project Bootstrap

Zet een schoon klantproject op voor gebruik van de 42-SEO-Skills plugin. Zes stappen,
in deze volgorde. Ga pas door naar de volgende stap als de vorige geslaagd is.

---

## Stap 1 — Profiel kiezen

Vraag de gebruiker **één** AskUserQuestion met deze opties:

| Profiel | Voor | Aantal skills |
|---|---|---|
| `content` | Blogs, editorial, thought leadership | 13 |
| `ecom` | Webshops, productpagina's, categorieën | 16 |
| `technical` | Hreflang/sitemap/schema/migrations | 14 |
| `full` | Alles (agency of onbekend) | alle 59 |

Lees het gekozen profiel:
```bash
cat "${CLAUDE_PLUGIN_ROOT}/profiles/<profiel>.json"
```

Parse `skills[]` — die heb je straks nodig voor stap 5.

---

## Stap 2 — Klantnaam

Vraag: "Wat is de naam (slug) van dit project? Bijvoorbeeld: `acme-nl`, `klant-xyz`."

Valideer: alleen `[a-z0-9-]`. Bij hoofdletters of spaties: vervang automatisch en toon
de genormaliseerde vorm ter bevestiging.

Maak aan:
```bash
mkdir -p "42-reports/<klant-slug>"
```

---

## Stap 3 — Auth (.env)

Check of `.env` al bestaat in cwd. Als niet:

```bash
cp "${CLAUDE_PLUGIN_ROOT}/.env.example" .env
```

Lees de lege `.env` in, toon de verplichte velden en vraag welke keys de gebruiker
nu wil invullen. Minimaal nodig voor de gekozen profielen:

- **content / ecom**: `GOOGLE_API_KEY` (Gemini), `DATAFORSEO_LOGIN` + `DATAFORSEO_PASSWORD`
- **technical**: `FIRECRAWL_API_KEY` (alleen als gebruiker Firecrawl gebruikt)
- **full**: alles bovenstaand + `GSC_SERVICE_ACCOUNT_JSON` (pad naar service account file)

Gebruiker kan overslaan ("later") — alleen waarschuwen dat sommige skills dan falen
met duidelijke error.

---

## Stap 4 — Gedeelde Python venv

De venv is **gedeeld** over alle klantprojecten en staat op `~/.claude/venvs/42-seo/`.
Check eerst of hij al bestaat:

```bash
VENV="$HOME/.claude/venvs/42-seo"
if [ ! -d "$VENV" ]; then
  mkdir -p "$HOME/.claude/venvs"
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install --upgrade pip
  "$VENV/bin/pip" install -r "${CLAUDE_PLUGIN_ROOT}/requirements.txt"
fi
```

Als hij wel bestaat: `pip install --upgrade` om nieuwe/bijgewerkte packages uit
`requirements.txt` te installeren (idempotent).

Schrijf daarna een `.envrc` of leg uit hoe te activeren:
```bash
source ~/.claude/venvs/42-seo/bin/activate
```

**Optionele deps** (playwright, spacy, reportlab, etc.): vraag *alleen* bij
profielen die ze nodig hebben. Bijvoorbeeld `playwright` alleen als 42-internal-links
of 42-seo-agi in profiel zit.

---

## Stap 5 — Skill allowlist via disabledSkills

Bereken welke skills **uit moeten staan** op basis van het profiel. Pak alle 59 skills
min de geselecteerde set, en converteer naar glob-patterns waar mogelijk voor
compactheid.

Schrijf `.claude/settings.local.json`:

```bash
mkdir -p .claude
```

Genereer JSON:
```json
{
  "disabledSkills": [
    "42-ecom-*",
    "42-product-titles",
    "42-geo-sales",
    "42-programmatic-seo"
  ],
  "42-init": {
    "profile": "content",
    "client": "<klant-slug>",
    "initializedAt": "<ISO datum>"
  }
}
```

Als er al een `.claude/settings.local.json` is — **merge** in plaats van overschrijven.
Bewaar bestaande keys (bv. permissions, env).

**Belangrijk**: `42-init` zelf mag nooit op de disabled-lijst staan, anders kan de
gebruiker niet her-initialiseren.

---

## Stap 6 — Samenvatting tonen

Toon een korte samenvatting:

```
✓ 42-SEO-Skills geïnitialiseerd voor <klant-slug>

Profiel:     content (13 skills actief)
Venv:        ~/.claude/venvs/42-seo (gedeeld)
Reports:     ./42-reports/<klant-slug>/
Auth:        .env (ingevuld: GOOGLE_API_KEY, DATAFORSEO_*)
             .env (nog leeg: GSC_SERVICE_ACCOUNT_JSON)

Eerste stap: /42-audit <domein>
             of: /42-seo-project start <domein>
```

Herstart-hint tonen: "Herstart je Claude Code-sessie (`/reload`) zodat de
allowlist actief wordt."

---

## Fouten en edge cases

- **Geen `python3`**: waarschuw en stop. Vraag om Python 3.11+ te installeren.
- **venv failure**: toon de foutmelding letterlijk, niet uitleggen alsof het werkt.
- **Geen schrijfrechten in cwd**: stop, vraag om in project-root te staan.
- **Al geïnitialiseerd** (settings.local.json heeft `42-init.profile`): vraag of
  gebruiker wil overschrijven of aanvullen.

---

## Re-init flow

Als `/42-init` opnieuw gedraaid wordt in een project dat al een `42-init`-sectie
heeft in `.claude/settings.local.json`, bied drie opties:

1. **Profiel wijzigen** — overschrijf `disabledSkills`, behoud .env en venv
2. **Alleen deps bijwerken** — skip settings en .env, alleen `pip install -U`
3. **Opnieuw beginnen** — wis settings, .env, reports (met bevestiging!)

---

## Notes voor Claude

- Gebruik **AskUserQuestion** voor alle keuzes, niet free-text prompts
- Voer **bash in project-root** uit (niet `cd` naar plugin-root)
- Verwijs naar scripts met `${CLAUDE_PLUGIN_ROOT}/scripts/...`
- De gedeelde venv beteken dat **alle klantprojecten dezelfde package-versies delen**
  — als een klant een oudere versie nodig heeft, waarschuw en bied aan project-
  lokale venv (`./.venv`) te maken als override
