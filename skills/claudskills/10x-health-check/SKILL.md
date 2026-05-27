---
name: 10x-health-check
description: >
  Run a health check on an existing project: dependency audit, security scan,
  test runner detection, CI/CD evaluation, and missing configuration analysis.
  Maps the three execution gates (pre/in/post) from /10x-bootstrapper to an
  assessment framework for existing codebases. Reads optional
  context/foundation/stack-assessment.md from /10x-stack-assess to focus checks
  on identified gaps. Writes context/foundation/health-check.md with findings,
  prioritized fixes, and an agent-readiness verdict. Use when the user has an
  existing project and wants to verify its health before working with an agent.
  Trigger phrases: "health check", "check my project", "audit my project",
  "is my project healthy", "sprawdź projekt", "audyt projektu",
  "health-check", "project health".
  Use AFTER /10x-stack-assess (brownfield chain), BEFORE agent onboarding (m1-l4).
argument-hint: "[path-to-stack-assessment]"
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
  - TaskCreate
  - TaskUpdate
---

# Kontrola stanu: Audyt istniejącego projektu pod kątem gotowości agenta

Ta umiejętność jest odpowiednikiem `/10x-bootstrapper` dla projektów typu brownfield. Tam, gdzie bootstrapper tworzy nowy projekt i weryfikuje jego strukturę, health-check uruchamia te same trzy bramki wykonawcze (pre/in/post) jako ramy oceny dla istniejącej bazy kodu. Ponownie wykorzystuje wzorzec audytu dla poszczególnych języków z weryfikacji po utworzeniu struktury bootstrapper'a, ale stosuje go jako ruch otwierający, a nie zamykający.

Umiejętność ta znajduje się w łańcuchu brownfield: `/10x-shape → /10x-prd → /10x-stack-assess → /10x-health-check`. Jej jedyne zadanie: audyt stanu zależności projektu, infrastruktury testowej, konfiguracji CI/CD i kompletności konfiguracji, a następnie sporządzenie ustrukturyzowanego raportu z priorytetowymi poprawkami i werdyktem gotowości agenta.

Gdy istnieje `context/foundation/stack-assessment.md` (z `/10x-stack-assess`), health-check łączy swoje ustalenia z lukami w bramkach jakości zidentyfikowanymi w tym pliku. Oba raporty są komplementarne: stack-assess ocenia *wybór stosu* pod kątem bramek jakości; health-check ocenia *stan projektu* pod kątem kryteriów zdrowia operacyjnego.

## Kiedy używać, kiedy pominąć

**Użyj, gdy**: użytkownik ma istniejący projekt i chce zweryfikować jego stan przed rozpoczęciem rozwoju wspomaganego przez agenta. Katalog projektu powinien zawierać rozpoznawalne znaczniki projektu (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `Gemfile`, `composer.json`, `*.csproj`, `pubspec.yaml`).

**Pomiń, gdy**: użytkownik tworzy nowy projekt — `/10x-bootstrapper` uruchamia własne sloty weryfikacyjne. Pomiń również, gdy użytkownik chce tylko oceny bramki jakości stosu bez kontroli stanu operacyjnego — to jest obszar `/10x-stack-assess`.

## Związek z innymi umiejętnościami

- `/10x-stack-assess` — upstream. Tworzy `context/foundation/stack-assessment.md`. Opcjonalne wejście — health-check może działać bez niego, ale raport jest bogatszy, gdy luki są połączone.
- `/10x-bootstrapper` — równoległy greenfield. Te same trzy bramki wykonawcze, inne zastosowanie (weryfikacja struktury vs audyt istniejącego projektu).
- `/10x-shape`, `/10x-prd` — wcześniej w łańcuchu brownfield. Nie są bezpośrednimi wejściami, ale kontekst zakresu zmian z PRD może informować, które części projektu są najważniejsze.

## Wymagane dane wejściowe

1. Istniejąca baza kodu w bieżącym katalogu z co najmniej jednym rozpoznawalnym znacznikiem projektu.

## Opcjonalne dane wejściowe

1. `context/foundation/stack-assessment.md` — jeśli obecny, health-check odwołuje się do luk w bramkach jakości z ustaleniami operacyjnymi.
2. `context/foundation/prd.md` — jeśli obecny i ma `context_type: brownfield`, health-check używa `## Scope of Change` z PRD do priorytetyzacji ustaleń istotnych dla planowanej pracy.

## Początkowa odpowiedź

Gdy ta umiejętność zostanie wywołana:

1. **Jeśli podano argument ścieżki** (np. `/10x-health-check @context/foundation/stack-assessment.md`), usuń początkowe `@`, jeśli jest obecne, i użyj ścieżki jako lokalizacji stack-assessment dla tego uruchomienia. Ocena jest opcjonalnym kontekstem, a nie warunkiem wstępnym.
2. **Jeśli nie podano argumentu**, sprawdź `context/foundation/stack-assessment.md`. Jeśli jest obecny, załaduj go do odwołań. Jeśli nieobecny, kontynuuj bez niego.

## Przepływ pracy

### Krok 0 — Warunek wstępny Cwd

Wykryj znaczniki projektu:

```bash
find . -maxdepth 1 \( -name "package.json" -o -name "Cargo.toml" -o -name "pyproject.toml" -o -name "go.mod" -o -name "Gemfile" -o -name "composer.json" -o -name "*.csproj" -o -name "pubspec.yaml" \) 2>/dev/null
```

Jeśli **nie znaleziono znaczników**, wydrukuj:

```
No project markers found in the current directory. /10x-health-check requires an existing codebase.
If you're starting from scratch, use /10x-bootstrapper after /10x-tech-stack-selector instead.
```

Następnie ZATRZYMAJ.

Jeśli znaleziono znaczniki, wykryj rodzinę języków na podstawie znacznika (ta sama logika wykrywania co w `/10x-stack-assess` Krok 1) i przejdź do Kroku 1.

### Krok 1 — Kontrola wstępna (audyt zależności + plik blokady + bezpieczeństwo)

**Bramka wykonawcza: pre-check.** Przed odczytaniem lub zmianą czegokolwiek w projekcie, przeprowadź audyt drzewa zależności. Odpowiada to bramce przedwykonawczej bootstrapper'a: "jaki jest stan przekazania, zanim zaczniemy działać?"

#### 1a. Obecność pliku blokady

Sprawdź obecność pliku blokady odpowiadającego wykrytej rodzinie języków:

| Rodzina języków | Oczekiwane pliki blokady |
|---|---|
| JS/TS | `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lockb` |
| Python | `poetry.lock`, `uv.lock`, `Pipfile.lock`, `requirements.txt` (słabe — nie jest prawdziwą blokadą) |
| Rust | `Cargo.lock` |
| Go | `go.sum` |
| Ruby | `Gemfile.lock` |
| PHP | `composer.lock` |
| .NET | `packages.lock.json` (NuGet) |
| Dart | `pubspec.lock` |

Jeśli nie znaleziono pliku blokady, oznacz to jako ustalenie:

```
⚠ No lockfile detected. Dependency versions are not pinned — builds are non-reproducible
  and the agent cannot reason about exact dependency state.
  Fix: run <package-manager lock command> to generate a lockfile.
```

#### 1b. Audyt zależności

Przekieruj do narzędzia audytowego ekosystemu według rodziny języków. Tabela przekierowań odpowiada wzorcowi `audit_commands` bootstrapper'a:

| Rodzina języków | Polecenie audytu | Uwagi |
|---|---|---|
| JS/TS | `npm audit --json` | Kończy się niezerowym kodem, gdy istnieją luki w zabezpieczeniach — nie jest to warunek zatrzymania |
| Python | `pip-audit --format json` | Pomija, jeśli pip-audit nie jest zainstalowany |
| Rust | `cargo audit --json` | Pomija, jeśli cargo-audit nie jest zainstalowany |
| Go | `govulncheck -json ./...` | Pomija, jeśli govulncheck nie jest zainstalowany |
| Ruby | `bundle audit check --update` | Czytelne dla człowieka wyjście, analizuj linia po linii |
| PHP | `composer audit --format json` | Wymaga Composer 2.4+ |
| .NET | `dotnet list package --vulnerable --include-transitive` | Czytelne dla człowieka, analizuj pod kątem znaczników ważności |
| Java, Dart | (pomiń) | Brak wbudowanego narzędzia audytowego; zanotuj pominięcie i zalecaj zewnętrzne narzędzia |

Uruchom rozwiązane polecenie z bieżącego katalogu. Zapisz stdout, stderr i kod wyjścia. Kod wyjścia narzędzia audytowego jest informacyjny — health-check NIE zatrzymuje się na niezerowym wyjściu audytu.

**Poziomy ważności** (takie same jak w weryfikacji po utworzeniu struktury bootstrapper'a):

- KRYTYCZNE (CVSS >= 9.0) — wyświetlaj w tekście
- WYSOKIE (CVSS 7.0–8.9) — wyświetlaj w tekście
- UMIARKOWANE (CVSS 4.0–6.9) — tylko loguj
- NISKIE (CVSS < 4.0) — tylko loguj

Dla narzędzi z natywną ważnością (npm-audit, cargo-audit, govulncheck) użyj etykiety narzędzia. Dla narzędzi bez natywnej ważności, domyślnie ustaw UMIARKOWANE, chyba że zalecenie wyraźnie wskazuje KRYTYCZNE lub WYSOKIE.

Gdy narzędzie rozróżnia zależności bezpośrednie od przechodnich, wyświetl podział. Bezpośrednie ustalenia są natychmiastowo możliwe do działania; przechodnie ustalenia są doradcze.

#### 1c. Sprawdzenie przestarzałych zależności

Jeśli rodzina języków to obsługuje, uruchom szybkie sprawdzenie przestarzałości:

| Rodzina języków | Polecenie | Co pokazuje |
|---|---|---|
| JS/TS | `npm outdated --json` | Aktualna vs pożądana vs najnowsza dla każdego pakietu |
| Python | `pip list --outdated --format json` | Aktualna vs najnowsza |
| Rust | `cargo outdated --root-deps-only` (jeśli zainstalowane) | Przestarzałe bezpośrednie zależności |
| Ruby | `bundle outdated --only-explicit` | Przestarzałe bezpośrednie gemy |

To sprawdzenie jest informacyjne — wyświetl luki w głównych wersjach i pakiety, które są więcej niż 2 główne wersje w tyle. Nie zgłaszaj każdej drobnej aktualizacji wersji.

**Tryb awaryjny dla wszystkich kroków 1a–1c**: OSTRZEŻ I KONTYNUUJ. Jeśli narzędzie nie jest zainstalowane, zaloguj pominięcie i kontynuuj. Jeśli wywołanie sieciowe zakończy się niepowodzeniem, zaloguj częściowe wyjście i kontynuuj. Nigdy nie zatrzymuj się na ustaleniu kontroli wstępnej.

Wyświetl jedną linię podsumowania po zakończeniu kontroli wstępnej:

```
Pre-check: <lockfile status>. Audit: <C> CRITICAL, <H> HIGH, <M> MODERATE, <L> LOW.
Outdated: <N> packages with major version gaps.
```

### Krok 2 — Kontrola wewnętrzna (runner testów, CI/CD, konfiguracja)

**Bramka wykonawcza: in-check.** Analiza tylko do odczytu infrastruktury testowej projektu, potoku CI/CD i kompletności konfiguracji. Odpowiada to bramce wewnętrznej bootstrapper'a: "jak wygląda środowisko wykonawcze?"

#### 2a. Wykrywanie i stan runnera testów

Wykryj runner testów z plików konfiguracyjnych:

| Rodzina języków | Źródła wykrywania | Runnery testów |
|---|---|---|
| JS/TS | `package.json` scripts/devDeps, `vitest.config.*`, `jest.config.*`, `playwright.config.*`, `cypress.config.*` | Vitest, Jest, Playwright, Cypress, Mocha |
| Python | `pyproject.toml [tool.pytest]`, `setup.cfg [tool:pytest]`, `tox.ini`, `pytest.ini` | pytest, unittest, tox |
| Rust | `Cargo.toml` (wbudowany `cargo test`) | cargo test |
| Go | (wbudowany `go test`) | go test |
| Ruby | `Gemfile` deps, `.rspec`, `Rakefile` | RSpec, Minitest |
| PHP | `phpunit.xml*`, `composer.json` deps | PHPUnit, Pest |
| .NET | `*.csproj` references | xUnit, NUnit, MSTest |

Jeśli wykryto runner testów, spróbuj uruchomić suchy przebieg, aby zweryfikować, czy testy mogą się wykonać:

```bash
# JS/TS examples:
npx vitest run --reporter=json 2>&1 | head -50  # Vitest
npx jest --listTests 2>&1 | head -20             # Jest

# Python:
python -m pytest --collect-only 2>&1 | tail -5   # pytest

# Rust:
cargo test --no-run 2>&1 | tail -10              # cargo test

# Go:
go test -list '.*' ./... 2>&1 | head -20         # go test
```

Wyświetl ustalenia:

- **Wykryto runner testów + testy działają**: zgłoś liczbę testów, jeśli dostępna, zanotuj nazwę runnera
- **Wykryto runner testów + testy nie działają**: oznacz jako ustalenie z błędem
- **Nie wykryto runnera testów**: oznacz jako znaczące ustalenie — agent nie może zweryfikować własnych zmian

#### 2b. Ocena konfiguracji CI/CD

Sprawdź pliki konfiguracyjne CI/CD:

```bash
find . -maxdepth 2 \( -name ".github" -o -name ".gitlab-ci.yml" -o -name "Jenkinsfile" -o -name ".circleci" -o -name "cloudbuild.yaml" -o -name "bitbucket-pipelines.yml" -o -name ".travis.yml" \) 2>/dev/null
```

Jeśli znaleziono konfigurację CI, odczytaj ją i oceń pokrycie:

| Etap | Co sprawdzić |
|---|---|
| Lint | Czy jest etap lintowania? (eslint, ruff, clippy, rubocop, phpstan itp.) |
| Test | Czy jest etap testowania? Czy pasuje do wykrytego runnera testów? |
| Build | Czy jest etap budowania/kompilacji? |
| Type check | Czy jest etap sprawdzania typów? (tsc, mypy, pyright itp.) |
| Security | Czy jest etap skanowania bezpieczeństwa? (npm audit, Snyk, CodeQL, Dependabot itp.) |

Wyświetl podsumowanie pokrycia:

```
CI/CD: <provider> detected. Stages: lint <✓/✗>, test <✓/✗>, build <✓/✗>,
type-check <✓/✗>, security <✓/✗>.
```

Jeśli nie znaleziono konfiguracji CI, zanotuj to jako element kategorii B — uczeń skonfiguruje CI w późniejszej lekcji dotyczącej infrastruktury. Nie oznaczaj tego jako pilnego ustalenia.

#### 2c. Brakujące pliki konfiguracyjne

Sprawdź typowe konfiguracje deweloperskie:

| Plik | Cel | Ważność, jeśli brakuje |
|---|---|---|
| `.editorconfig` | Spójne formatowanie w różnych edytorach | niska |
| `.prettierrc*` / `biome.json` (JS/TS) | Formatowanie kodu | średnia (jeśli nie skonfigurowano formatowania) |
| `.eslintrc*` / `eslint.config.*` (JS/TS) | Lintowanie | średnia |
| `tsconfig.json` z `strict: true` (TS) | Ścisłość typów | wysoka (jeśli projekt TS bez strict) |
| `.gitignore` | Wykluczenia śledzonych plików | wysoka |
| `.env.example` / `.env.template` | Dokumentacja zmiennych środowiskowych | niska |
| `CLAUDE.md` / `AGENTS.md` | Pliki instrukcji agenta | Kategoria B — omówione w onboardingu agenta |

Wyświetl brakujące pliki pogrupowane według ważności.

**Tryb awaryjny dla wszystkich kroków 2a–2c**: OSTRZEŻ I KONTYNUUJ. Analiza tylko do odczytu nie powinna się nie powieść, ale jeśli odczyt pliku zakończy się błędem lub suchy przebieg zawiesi się, przechwyć, co możesz, i przejdź dalej.

Wyświetl jedną linię podsumowania po zakończeniu kontroli wewnętrznej:

```
In-check: test runner <detected/not detected>, CI <provider/not detected>,
<N> configuration gaps (<H> high, <M> medium, <L> low).
```

### Krok 3 — Kontrola końcowa (ocena + rekomendacje)

**Bramka wykonawcza: post-check.** Syntetyzuj ustalenia z kontroli wstępnej i wewnętrznej w werdykt gotowości agenta i priorytetową listę poprawek. Odpowiada to bramce pokonawczej bootstrapper'a: "jaki jest stan po ocenie wszystkiego?"

#### 3a. Odwołanie do stack-assessment

Jeśli istnieje `context/foundation/stack-assessment.md`, odczytaj go i połącz ustalenia:

- Jeśli stack-assess zidentyfikował błąd bramki jakości (np. "typed: fail"), a health-check nie znalazł sprawdzania typów w CI → wzmocnij: "stosowi brakuje bezpieczeństwa typów ORAZ CI nie wymusza typów — kompensacja jest podwójnie ważna"
- Jeśli stack-assess zidentyfikował strategie kompensacji → sprawdź, czy istnieją zalecane wpisy w pliku instrukcji (czy `CLAUDE.md` / `AGENTS.md` są obecne? Czy zawierają zalecane reguły?)
- Jeśli stack-assess wydał werdykt `ready-with-compensation`, ale brakuje wpisów kompensacyjnych → oznacz jako lukę

#### 3b. Określ ogólny stan zdrowia

Na podstawie wszystkich ustaleń:

- **healthy**: brak krytycznych/wysokich ustaleń audytu, wykryty i działający runner testów, brak luk konfiguracyjnych o wysokiej ważności w kategorii A.
- **needs-attention**: niektóre ustalenia kategorii A, ale wszystkie możliwe do rozwiązania. Typowe: kilka wysokich zaleceń audytu, brak formatowania lub brak ścisłości typów.
- **critical-issues**: krytyczne ustalenia audytu, brak runnera testów lub wiele luk kategorii A o wysokiej ważności. Agent będzie miał trudności bez przygotowania.

Ustalenia kategorii B (brak CI, brak AGENTS.md, brak konfiguracji wdrożenia) **nie** wpływają na werdykt — są oczekiwane na tym etapie i zostaną rozwiązane w późniejszych lekcjach. Projekt może być `healthy` bez potoku CI, jeśli ma działający runner testów, czyste zależności i dobrą lokalną konfigurację.

Werdykt jest informacyjny, a nie blokujący. Nawet `critical-issues` oznacza "poświęć czas na poprawki kategorii A, zanim spodziewasz się płynnej współpracy z agentem", a nie "porzuć projekt".

#### 3c. Priorytetowa lista poprawek

Podziel ustalenia na dwie kategorie:

**Kategoria A — Napraw przed pracą agenta** (możliwe do działania teraz):

1. **Krytyczne luki w zabezpieczeniach** — napraw przed jakąkolwiek pracą wspomaganą przez agenta, która dotyka dotkniętych ścieżek kodu
2. **Brak runnera testów** — agent nie może zweryfikować własnych zmian; zainstaluj i skonfiguruj go
3. **Brak pliku blokady** — niereprodukowalne kompilacje podważają niezawodność agenta
4. **Wysokie ustalenia audytu** — przejrzyj i załataj lub zaakceptuj ryzyko
5. **Brak ścisłości typów** (TS bez strict, Python bez mypy) — agent generuje mniej niezawodny kod
6. **Brak formatowania/lintowania** — styl wyjścia agenta będzie niespójny
7. **Przestarzałe zależności z dużymi lukami** — potencjalne zmiany powodujące niezgodność podczas aktualizacji
8. **Brak .editorconfig / .env.example** — wygoda, nie blokujące

**Kategoria B — Rozwiązane w nadchodzących lekcjach** (potwierdź, nie alarmuj):

Te ustalenia są prawdziwe, ale uczeń skonfiguruje je w nadchodzących krokach. Przedstaw je jako "następne w kolejce", a nie jako problemy:

- **Brak potoku CI** → omówione w lekcji dotyczącej infrastruktury/wdrożenia. Zanotuj lukę, wskaż przyszłość: "Skonfigurujesz CI w nadchodzącej lekcji. Na razie pokrycie lokalnego runnera testów jest tym, co ma znaczenie dla współpracy z agentem."
- **Brak plików instrukcji agenta** (CLAUDE.md / AGENTS.md) → omówione w lekcji dotyczącej onboardingu agenta. Nie zalecaj ich tworzenia teraz: "Onboarding agenta przeprowadzi Cię przez ich tworzenie z odpowiednią zawartością. Generowanie zaślepki teraz byłoby przedwczesne."
- **Brak konfiguracji wdrożenia** → omówione w lekcji dotyczącej infrastruktury. Potwierdź, nie priorytetyzuj.

Gdy kontrola stanu działa samodzielnie (poza łańcuchem kursu), wszystkie ustalenia trafiają na jedną listę rankingową bez podziału A/B — kontekst kursu ma zastosowanie tylko wtedy, gdy użytkownik przechodzi przez łańcuch brownfield. Podczas uruchamiania w łańcuchu kursu 10xDevs, wzbogacaj odwołania do przodu o tytuły lekcji i linki:
- onboarding agenta = [Agent Onboarding: Agents.md, AI Rules i feedback loops (M1L4)](https://platforma.przeprogramowani.pl/external/10xdevs-3/m1-l4)
- infrastruktura i CI/CD = [Sprint Zero z Agentem: infrastruktura, walking skeleton i pierwszy deploy (M1L5)](https://platforma.przeprogramowani.pl/external/10xdevs-3/m1-l5)

Każdy wpis poprawki (w obu kategoriach) musi zawierać:

- Co jest nie tak (ustalenie)
- Dlaczego ma to znaczenie dla przepływów pracy agenta (wpływ)
- Co z tym zrobić (konkretne polecenie lub działanie naprawcze, lub lekcja, która to obejmuje)
- Szacowany wysiłek: szybki (< 5 min), umiarkowany (15–30 min), znaczący (> 1 godzina) lub **nadchodząca lekcja** dla elementów kategorii B

### Krok 4 — Zapisz health-check.md

Sprawdź kolizję:

```bash
test -f context/foundation/health-check.md
```

Jeśli plik istnieje, zapytaj:

AskUserQuestion:
- question: "context/foundation/health-check.md already exists. How would you like to proceed?"
  header: "Collision"
  options:
  - label: "Overwrite (Recommended)"
    description: "Replace the existing health check. The prior version is lost unless committed."
  - label: "Save as health-check-v2.md"
    description: "Preserve history. New report lands at the next available version slot."
  - label: "Abort"
    description: "Exit without writing. The conversation findings are preserved in chat only."
  multiSelect: false

Zbuduj plik wyjściowy zgodnie z `references/health-check-schema.md`.

Zapisz do `context/foundation/health-check.md` (tworząc `context/foundation/`, jeśli nie istnieje).

Po zapisie wydrukuj podsumowanie końcowe:

```
═══════════════════════════════════════════════════════════
  KONTROLA STANU ZAKOŃCZONA
═══════════════════════════════════════════════════════════

  Projekt:        <nazwa projektu>
  Stan:           <healthy | needs-attention | critical-issues>
  Ustalenia audytu: <C> KRYTYCZNE, <H> WYSOKIE
  Runner testów:    <wykryty (nazwa runnera) | nie wykryty>
  CI/CD:          <dostawca | nie wykryty>
  Poprawki:       <N> zalecane (<Q> szybkie, <M> umiarkowane, <S> znaczące)

  ► Raport:       context/foundation/health-check.md
  ► Dalej:        Onboarding agenta — zarówno greenfield, jak i brownfield
                  ścieżki zbiegają się z równoważnymi artefaktami kontekstu.
═══════════════════════════════════════════════════════════
```

ZATRZYMAJ. Nie przechodź automatycznie do żadnej następnej umiejętności.

## Wyjście

Zapisany pojedynczy plik: `context/foundation/health-check.md` (lub `health-check-vN.md`, jeśli wybrano wersjonowany zapis).

## Referencje

- `references/health-check-schema.md` — kształt `context/foundation/health-check.md`.

## Krytyczne zabezpieczenia

1. **Cwd jest warunkiem wstępnym.** Umiejętność wymaga istniejącej bazy kodu z rozpoznawalnymi znacznikami projektu. Brak oceny wyłącznie na podstawie kontekstu rozmowy.

2. **Analiza tylko do odczytu.** Kontrola stanu nigdy nie modyfikuje projektu. Brak `npm audit fix`, brak `pip install --upgrade`, brak automatycznej poprawki. Sugerowanie poprawek w raporcie jest w porządku; ich uruchamianie wykracza poza zakres.

3. **OSTRZEŻ I KONTYNUUJ na każdej gałęzi.** Żadne ustalenie nie zatrzymuje umiejętności. KRYTYCZNE luki w zabezpieczeniach, brakujące runnery testów, brak CI — wszystkie pojawiają się jako ustalenia z zaleceniami, nigdy jako blokady. Użytkownik decyduje, co i kiedy naprawić.

4. **Priorytetyzuj według wpływu agenta.** Lista poprawek jest uporządkowana według wpływu na przepływy pracy agenta, a nie według ogólnej ważności. Brak runnera testów ma większe znaczenie dla agenta niż NISKIE zalecenie audytu, ponieważ agent nie może zweryfikować własnych zmian bez testów.

5. **Konkretne poprawki, a nie ogólne porady.** Każde zalecenie musi zawierać konkretne polecenie lub działanie. "Dodaj testy" nie jest poprawką; "Uruchom `npm init vitest@latest`, aby skonfigurować Vitest, a następnie dodaj skrypt testowy do package.json" jest poprawką.

6. **Odwołaj się do stack-assessment, jeśli dostępne.** Jeśli użytkownik najpierw uruchomił `/10x-stack-assess`, kontrola stanu musi połączyć ustalenia z lukami w bramkach jakości. Oba raporty są komplementarne — nie duplikuj analizy bramki, odwołaj się do niej.

7. **Etykiety wewnętrzne umiejętności pozostają wewnętrzne.** Rozmawiając z użytkownikiem, nigdy nie odwołuj się do numerów kroków, nazw bramek jako terminów technicznych ani wewnętrznych nazw pól. Używaj prostego języka: "audyt zależności", "sprawdzenie infrastruktury testowej", "ogólny stan zdrowia".

8. **Świadomość kontekstu kursu.** Kontrola stanu znajduje się na ścieżce nauki. Brak CI/CD, brak AGENTS.md i brak konfiguracji wdrożenia to oczekiwane luki na tym etapie — przedstaw je jako "następne w kolejce", a nie jako błędy. Werdykt nie może karać ucznia za rzeczy, których jeszcze nie nauczono.

9. **Tylko uniwersalny język.** Brak prywatnych ścieżek skarbca lub brandingu specyficznego dla organizacji w dostarczanej treści.