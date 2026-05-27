---
name: developer-manual-maintainer
description: Údržba a aktualizace Klabis developer manuálu v docs/developerManual/. Použij tento skill kdykoli uživatel řekne "vytvoř developer manuál", "aktualizuj manuál", "doplň manuál o X", "podívej se co se změnilo a aktualizuj manuál", "zkontroluj manuál proti kódu", "syncuj manuál se zdrojákem", nebo žádá změnu ve struktuře/obsahu HTML stránek v docs/developerManual/. Použij ho i proaktivně po větším refactoringu v common modulu nebo framework-like částech members modulu (ActingUser, OAuth2 customizace) — manuál by měl popisovat aktuální API. Nepoužívej pro openspec specifikace, byznys-logiku modulů (events, calendar, members business), README ani jinou dokumentaci.
---

# Developer Manual Maintainer

Tento skill udržuje českou developerskou dokumentaci frameworkových částí Klabisu — `docs/developerManual/`. Manuál cílí na vývojáře se zkušeností Spring/DDD/React, kteří potřebují pochopit Klabis-specific patterny.

## Tři režimy použití

Identifikuj, který režim je relevantní podle vstupu uživatele:

### Režim 1: Vytvoření manuálu od nuly

**Trigger:** uživatel požaduje vytvořit dokumentaci, manuál ještě neexistuje (nebo je explicitně řečeno "udělej znovu").

**Postup:**
1. Spusť `Explore` agenta pro inventář framework features v `common/` a framework-like částech `members/` (viz `references/scope.md`).
2. Předlož uživateli návrh struktury stránek (počet, témata, co vynecháváš). **Nezačínej psát před schválením.**
3. Po schválení postupně vytvoř `style.css` (zkopíruj z `assets/style.css`), `index.html` a každou kapitolu zvlášť.
4. Pro každou kapitolu napřed přečti relevantní zdrojové soubory přes `Read` — signatury musí odpovídat kódu, ne paměti modelu.
5. Po vytvoření zkontroluj všechny křížové odkazy a navigaci `prev/next`.

### Režim 2: Aktualizace na uživatelský request

**Trigger:** uživatel říká "přidej tam X", "přejmenuj sekci", "přesuň Y na stránku Z", "přepiš sekci A".

**Postup:**
1. Identifikuj dotčené stránky podle `references/page-inventory.md`.
2. Pokud jde o přesun mezi stránkami, vždy aktualizuj **všechno najednou**:
   - Zdrojovou stránku (odebrat sekci)
   - Cílovou stránku (přidat sekci ve stejném stylu)
   - `index.html` (description)
   - `01-architecture.html` tabulku subpackages (sloupec "Kapitola")
   - Křížové odkazy v textech (`viz kap. NN`)
   - `prev/next` navigaci, breadcrumbs, čísla v titulech
3. Pokud uživatel přejmenuje stránku, přejmenuj i soubor (`mv`) a aktualizuj všechny `<a href="...">` napříč adresářem.
4. Po dokončení udělej `Grep` na staré odkazy/názvy — ujisti se, že nikde nezůstaly.

### Režim 3: Sync s změnami ve zdrojovém kódu

**Trigger:** uživatel říká "podívej se co se změnilo", "syncuj manuál", nebo automaticky po větším refactoringu, který se jeví relevantní.

**Postup:**

**A) Bez explicitního rozsahu** — projdi všechny commity od posledního commitu, který se týkal manuálu:

```bash
LAST_DOC_COMMIT=$(git log -n 1 --format=%H -- docs/developerManual/)
git log --oneline ${LAST_DOC_COMMIT}..HEAD -- backend/src/main/java/com/klabis/common/ backend/src/main/java/com/klabis/members/
```

**B) S explicitním rozsahem** — uživatel udá commit/branch (např. "od commitu abc123" nebo "od main"):

```bash
git log --oneline <range> -- backend/src/main/java/com/klabis/common/ backend/src/main/java/com/klabis/members/
git diff <range> -- backend/src/main/java/com/klabis/common/ backend/src/main/java/com/klabis/members/
```

**Postup po získání diffu:**
1. Pro každý dotčený soubor zjisti přes `references/scope.md`, jestli jde o framework feature (= patří do manuálu) nebo o byznys-logiku (= ignoruj).
2. Pro framework změny zjisti přes `references/page-inventory.md`, která stránka se jí týká.
3. Přečti aktuální verzi zdrojového souboru (signatury se mohly změnit).
4. Aktualizuj příslušné sekce manuálu — změň signature snippety, popis chování, tabulky enum hodnot.
5. Pokud se objevila zcela nová framework feature (např. nový subpackage v `common/`), zvaž s uživatelem, kam ji přidat.
6. Reportni uživateli stručný přehled co se změnilo a co jsi aktualizoval (případně co jsi vědomě ignoroval jako byznys-logiku).

## Klíčové reference

Než cokoli píšeš nebo měníš, načti si tyto soubory:

- `references/scope.md` — co patří/nepatří do manuálu (rozhodující pro režim 1 a 3).
- `references/page-inventory.md` — mapa stránka → témata → kde v kódu hledat. Použij k najití správné stránky pro změnu.
- `references/html-conventions.md` — konvence HTML/CSS, vocabulary nestandardních bloků (`<aside class="note">`, `<dl class="api-list">`, `<pre class="signature">`, `.toc`, …) s ukázkami.
- `assets/style.css` — kanonický stylesheet. Při režimu 1 se kopíruje do `docs/developerManual/style.css` beze změn. Při změnách v něm vždy aktualizuj `references/html-conventions.md`.

## Pravidla pro psaní obsahu

Tato pravidla vznikla iterativně z práce s uživatelem na první verzi manuálu. Drž se jich — jejich porušení skoro vždy vede k oprávněnému feedback.

### Cílová audience a styl

- **Audience:** vývojáři se zkušeností Spring Boot, DDD, hexagonální architektury, React/TanStack Query. Rozepisuj **pouze** Klabis-specific věci. Odkazuj na oficiální dokumentaci místo vysvětlování obecných konceptů.
- **Jazyk:** čeština s diakritikou. Technické identifikátory ponech v originále.
- **Tón:** věcný, konkrétní, bez marketingu. Krátké odstavce.
- **Délka:** stránka by se měla vejít kolem 200-300 řádků HTML. Pokud je delší, zvaž rozdělení.

### Ověřování proti kódu

Než napíšeš signature snippet, **vždy** přečti aktuální zdrojový soubor přes `Read`. Modely často halucinují signatury (špatné package, neexistující metody, zastaralé parametry). Konkrétně ověř:

- Package name (např. `Authority` je v `common.users`, ne v `common.security`).
- Modifikátory tříd (final, abstract, sealed).
- Skutečné parametry metod a jejich pořadí.
- Anotace na třídě i parametrech.
- Hodnoty enumů (kompletní seznam, ne paměťový výběr).

Pro nalezení reálných příkladů použití používej `Grep` (např. `grep -rn "@WithKlabisMockUser"`).

### Signature snippety

Krátké — ideálně 5-15 řádků. Pouze interface/anotace/deklarace, **ne** implementační detaily. Cíl je dát vývojáři tvar API, ne celou implementaci.

```html
<pre class="signature"><code>@PrimaryPort
public interface UserService {
    UserId createUser(String username, String email, Set&lt;Authority&gt; authorities);
    UserId createActiveUser(String username, String passwordHash, Set&lt;Authority&gt; authorities);
}</code></pre>
```

### HTML struktura

- Žádné inline styly, žádné `style=` atributy. Veškerou vizuální úpravu řeší `style.css`.
- Pouze sémantické tagy a třídy z vocabulary v `references/html-conventions.md`.
- Každá stránka má stejnou strukturu: `<header class="page-header">` (breadcrumb) → `<main class="page-main"><article>` → `<nav class="page-nav">` (prev/next).
- HTML entity v kódu: `&lt;`, `&gt;`, `&amp;` — generic typy v `<pre>` musí být escapované.

### Křížové odkazy

Pokud odkazuješ na jinou kapitolu, používej formát `kap. NN` (např. `viz kap. 06`) nebo přímý link `<a href="06-security.html">06 · Bezpečnost</a>`. Při přečíslování stránek **vždy** projeď grep:

```bash
grep -rn "kap\. 0[0-9]\|N[N]-[a-z]" docs/developerManual/
```

## Závěr práce

Po jakékoli změně před tím, než řekneš že je hotovo:

1. `ls docs/developerManual/` — ověř, že jsou všechny očekávané soubory.
2. `Grep` na staré názvy stránek/sekcí — nesmí nikde zůstat odkaz na neexistující soubor.
3. Projdi `index.html` — obsah musí odpovídat realitě.
4. Reportni uživateli stručný souhrn co se změnilo.

## Co se z této konverzace ukázalo důležité

- Začni **návrhem struktury pro souhlas**, nepiš rovnou. Uživatel typicky chce konsolidovat do menšího počtu stránek.
- Když uživatel řekne "přesuň X na stránku Y", **vždycky** to znamená i aktualizaci indexu, navigace, tabulek subpackages a křížových odkazů. Nedělej to po částech.
- Frontend specifika patří do samostatné stránky (HAL+FORMS klient, KlabisTable, customizace). Backend a frontend mají vlastní `CLAUDE.md`, kterými se inspiruj.

## Povinné stránky manuálu

Při režimu 1 (vytvoření od nuly) i při větší restrukturalizaci v režimu 2 musí manuál **vždy** obsahovat:

### Index (`index.html`)

Obsah s linky na všechny stránky + krátké description. **Vždy** ho aktualizuj, když se změní názvy/čísla stránek.

### Předpoklady / Onboarding (`00-prerequisites.html`)

Rozcestník pro vývojáře, kteří neumí některou z používaných technologií 

Pravidla pro tuto stránku:
- **Krátké přehledy** — pět vět maximálně k tématu, žádný tutorial.
- **Odkazy na oficiální dokumentaci** (Spring docs, MDN, oficiální readme) — ne na blog posts.
- Uživatel s daným tématem zkušeností tuto sekci přeskočí; tahle stránka existuje pro nově příchozí vývojáře.
- Krátký Klabis-specific kontext (kde se v projektu používá), pokud to dává smysl, ale ne hluboko — to už řeší kapitoly 02+.

Rozdělená do sekcí: backend stack, frontend stack, testovací stack. Při každém přidání nové významné knihovny do projektu (≥ jedna používající kapitola) přidej ji sem.

### Práce s Claude Code (poslední stránka)

Popis OpenSpec workflow, dostupných skills/agents/commands a typických postupů (přidat feature, refactoring, sandbox pravidla). Pomáhá novým vývojářům pochopit, jak v projektu pracovat s asistencí Claude Code.
