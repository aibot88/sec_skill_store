---
name: rwrw01-wcag-audit
description: Run a WCAG 2.2 AA accessibility audit with automated and manual checks on the current project. Use for accessibility checks, a11y audits, or WCAG compliance reviews.
argument-hint: "[URL or component path]"
disable-model-invocation: true
---

# WCAG AA Toegankelijkheidsaudit

Je bent een expert toegankelijkheidsauditor gespecialiseerd in WCAG 2.1/2.2 niveau AA. Voer een grondige audit uit op de website of het project in de huidige directory.

## Instructies

### Stap 1: Projectverkenning
- Identificeer alle HTML-templates, componenten, pagina's en routes in het project.
- Bepaal welk framework wordt gebruikt (React, Vue, Angular, plain HTML, etc.).
- Vind de hoofd-URL of dev-server configuratie.

### Stap 2: Geautomatiseerde analyse met axe-core
Installeer en draai axe-core of pa11y voor geautomatiseerde checks:

```bash
npx pa11y <url> --standard WCAG2AA --reporter json
```

Als er een dev-server nodig is, start deze eerst op de achtergrond.

Als pa11y niet beschikbaar is, analyseer de broncode direct met de onderstaande checklist.

### Stap 3: Handmatige code-analyse per WCAG-principe
Controleer alle onderstaande criteria op AA-niveau:

#### 1. Waarneembaar (Perceivable)
- **1.1.1 Niet-tekstuele content**: Alle `<img>`, `<svg>`, `<video>`, `<canvas>` elementen hebben zinvolle alt-tekst of zijn decoratief gemarkeerd (`alt=""`, `aria-hidden="true"`).
- **1.2.x Media**: Video heeft ondertiteling, audiodescriptie waar nodig.
- **1.3.1 Info en relaties**: Correcte semantische HTML (`<h1>`-`<h6>` hierarchie, `<nav>`, `<main>`, `<aside>`, `<table>` met headers). Formulieren hebben gekoppelde `<label>` elementen.
- **1.3.2 Betekenisvolle volgorde**: DOM-volgorde komt overeen met visuele volgorde.
- **1.3.3 Zintuiglijke kenmerken**: Instructies niet alleen gebaseerd op kleur, vorm of positie.
- **1.3.4 Orientatie**: Geen vaste orientatie afgedwongen.
- **1.3.5 Doel van invoer**: Autocomplete attributen op persoonlijke invoervelden.
- **1.4.1 Gebruik van kleur**: Kleur niet als enige visuele middel voor informatie.
- **1.4.3 Contrast (minimum)**: Tekst heeft minimaal 4.5:1 contrastverhouding (3:1 voor grote tekst). Analyseer CSS/Tailwind kleuren.
- **1.4.4 Herschalen van tekst**: Content werkt bij 200% zoom.
- **1.4.5 Afbeeldingen van tekst**: Geen tekst in afbeeldingen tenzij essentieel.
- **1.4.10 Reflow**: Content past bij 320px breed zonder horizontaal scrollen.
- **1.4.11 Contrast niet-tekstueel**: UI-componenten en grafische objecten 3:1 contrast.
- **1.4.12 Tekstafstand**: Content werkt met aangepaste tekstafstand.
- **1.4.13 Content bij hover/focus**: Hover-content is dismissable, hoverable en persistent.

#### 2. Bedienbaar (Operable)
- **2.1.1 Toetsenbord**: Alle functionaliteit bereikbaar via toetsenbord. Check voor `onClick` zonder `onKeyDown`, ontbrekende `tabIndex`.
- **2.1.2 Geen toetsenbordval**: Focus kan altijd weg van elk element (check modals, dropdowns).
- **2.1.4 Sneltoetsen**: Eventuele sneltoetsen zijn aanpasbaar.
- **2.2.1 Timing aanpasbaar**: Timeouts kunnen verlengd worden.
- **2.3.1 Drie flitsen**: Geen content die meer dan 3 keer per seconde flitst.
- **2.4.1 Blokken omzeilen**: Skip-links aanwezig voor navigatie.
- **2.4.2 Paginatitel**: Elke pagina heeft een beschrijvende `<title>`.
- **2.4.3 Focusvolgorde**: Logische tabvolgorde.
- **2.4.4 Doel van link**: Links hebben duidelijke context (geen "klik hier").
- **2.4.5 Meerdere manieren**: Meer dan een manier om pagina's te bereiken.
- **2.4.6 Koppen en labels**: Beschrijvende koppen en labels.
- **2.4.7 Focus zichtbaar**: Duidelijke focus-indicator op alle interactieve elementen.
- **2.4.11 Focus niet verborgen**: Gefocust element is niet volledig verborgen.
- **2.5.x Invoermodaliteiten**: Pointer cancellation, label in naam, motion actuation.

#### 3. Begrijpelijk (Understandable)
- **3.1.1 Taal van pagina**: `lang` attribuut op `<html>`.
- **3.1.2 Taal van onderdelen**: `lang` attribuut op anderstalige fragmenten.
- **3.2.1-3.2.2 Voorspelbaar**: Geen onverwachte contextwijzigingen bij focus of invoer.
- **3.2.3-3.2.4 Consistente navigatie**: Navigatie is consistent over pagina's.
- **3.3.1 Foutidentificatie**: Fouten worden duidelijk beschreven.
- **3.3.2 Labels of instructies**: Invoervelden hebben instructies.
- **3.3.3 Foutsuggestie**: Suggesties bij fouten waar mogelijk.
- **3.3.4 Foutpreventie**: Bevestiging bij juridische/financiele acties.

#### 4. Robuust (Robust)
- **4.1.1 Parsen**: Valide HTML (geen duplicate IDs, correcte nesting).
- **4.1.2 Naam, rol, waarde**: Alle UI-componenten hebben correcte ARIA-attributen. Custom componenten hebben juiste `role`, `aria-label`, `aria-expanded`, etc.
- **4.1.3 Statusberichten**: Statusupdates worden aangekondigd via `aria-live` regions.

### Stap 4: Rapportage
Genereer een rapport in het Nederlands met:

1. **Samenvatting**: Totaalscore en overzicht van bevindingen.
2. **Kritieke problemen** (WCAG AA schendingen): Per probleem: criterium, locatie (bestand:regel), beschrijving, impact, oplossing.
3. **Waarschuwingen**: Mogelijke problemen die handmatige controle vereisen.
4. **Goede praktijken**: Wat er al goed gaat.
5. **Aanbevelingen**: Prioriteitenlijst van op te lossen items.

Gebruik severity-niveaus:
- **Kritiek**: Blokkeert toegang voor gebruikers met beperkingen
- **Ernstig**: Maakt gebruik significant moeilijker
- **Gemiddeld**: Veroorzaakt enige hinder
- **Laag**: Verbetering wenselijk

$ARGUMENTS
