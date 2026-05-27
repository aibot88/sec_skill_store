---
name: project-setup
description: Best Practices Setup fuer neue Projekte — Testing, Linting, Git Hooks, CI/CD, Security
disable-model-invocation: true
---
Richte ein neues Projekt mit Best Practices ein. Arbeite inkrementell — nur einrichten was fehlt, nichts ueberschreiben was bereits existiert.

## 1. Sprache und Framework erkennen

Pruefe welche Dateien im Projektroot existieren, um Sprache und Oekosystem zu bestimmen:

| Datei | Oekosystem |
|-------|-----------|
| `package.json` | Node.js / TypeScript |
| `pyproject.toml` oder `requirements.txt` | Python |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `pubspec.yaml` | Flutter/Dart |
| `composer.json` | PHP |

Falls keine dieser Dateien existiert: den User fragen welche Sprache/Framework genutzt wird.

Falls `package.json` existiert, pruefe zusaetzlich:
- `vue` oder `nuxt` in dependencies → Vue.js Projekt
- `next` in dependencies → Next.js Projekt
- `react` in dependencies → React Projekt
- `svelte` oder `@sveltejs/kit` → Svelte/SvelteKit

## 2. Bestehenden Zustand pruefen

Vor jeder Einrichtung pruefen was schon da ist. Fuer jeden der folgenden Punkte:
- Existiert die Datei/Config bereits? → Ueberspringen oder nur Luecken fuellen
- Gibt es bestehende Patterns? → Diese respektieren und erweitern, nicht ersetzen

Pruefe explizit:
- [ ] `.gitignore` — existiert? Sprachspezifische Eintraege vorhanden?
- [ ] `.env.example` — existiert?
- [ ] `.env.test` — existiert? (Regel aus `rules/testing.md` beachten)
- [ ] Linter-Config — ESLint, Ruff, golangci-lint etc.
- [ ] Formatter-Config — Prettier, Black, gofmt etc.
- [ ] Test-Framework — Vitest, Jest, pytest, go test etc.
- [ ] Git Hooks — Husky, pre-commit, Shell-Scripts in `.git/hooks/`
- [ ] CI/CD — `.github/workflows/`, `.gitlab-ci.yml` etc.
- [ ] `CLAUDE.md` — existiert im Projektroot?

## 3. .gitignore einrichten/erweitern

Falls `.gitignore` nicht existiert: erstellen. Falls sie existiert: nur fehlende Eintraege ergaenzen.

**Immer enthalten:**
```
.env
.env.*
!.env.example
.DS_Store
```

**Sprachspezifisch ergaenzen:**

Node.js:
```
node_modules/
dist/
.next/
.nuxt/
.output/
coverage/
*.tsbuildinfo
```

Python:
```
__pycache__/
*.pyc
.venv/
venv/
.mypy_cache/
.ruff_cache/
htmlcov/
.coverage
```

Go:
```
bin/
vendor/
```

Rust:
```
target/
```

PHP:
```
vendor/
```

## 4. Environment-Dateien

### .env.example
Falls nicht vorhanden: `.env.example` erstellen mit allen benoetigten Variablen (ohne Werte), basierend auf vorhandenen `.env`-Dateien oder dem Code. Kommentare hinzufuegen die beschreiben wofuer jede Variable ist.

### .env.test
Falls nicht vorhanden und ein E2E-Test-Setup existiert oder geplant ist:
- Template aus `~/.claude/templates/env.test.example` kopieren
- `.env.test` in `.gitignore` sicherstellen (Regel aus `rules/testing.md`)

### .env.local
Nicht erstellen — das macht der Entwickler selbst. Nur sicherstellen dass `.env.local` in `.gitignore` steht.

## 5. Linting und Formatting einrichten

Nur einrichten falls noch KEIN Linter/Formatter konfiguriert ist.

### Node.js / TypeScript
```bash
npm install -D eslint prettier eslint-config-prettier
```
- `eslint.config.js` (Flat Config, ESLint 9+) erstellen mit sinnvollen Defaults
- `.prettierrc` erstellen: `{ "semi": false, "singleQuote": true }`
- `.prettierignore` erstellen mit Build-Outputs
- Falls TypeScript: `eslint-plugin-@typescript-eslint` ergaenzen
- Scripts in `package.json` ergaenzen:
  ```json
  "lint": "eslint .",
  "lint:fix": "eslint . --fix",
  "format": "prettier --write .",
  "format:check": "prettier --check ."
  ```

### Python
```bash
pip install ruff  # oder in pyproject.toml als dev-dependency
```
- `[tool.ruff]` Sektion in `pyproject.toml` ergaenzen falls nicht vorhanden
- Ruff-Defaults: `line-length = 120`, `select = ["E", "F", "I", "W"]`

### Go
- Keine Installation noetig — `gofmt` und `go vet` sind built-in
- Optional: `golangci-lint` empfehlen fuer erweiterte Checks

### PHP
```bash
composer require --dev squizlabs/php_codesniffer friendsofphp/php-cs-fixer
```

## 6. Testing einrichten

Nur einrichten falls noch KEIN Test-Framework konfiguriert ist.

### Node.js / TypeScript

**Unit Tests — Vitest bevorzugen (bei Vite-Projekten), sonst Jest:**
```bash
npm install -D vitest @vitest/coverage-v8
```
- `vitest.config.ts` erstellen (oder in `vite.config.ts` integrieren)
- Coverage-Threshold setzen:
  ```ts
  test: {
    coverage: {
      provider: 'v8',
      thresholds: { lines: 80, branches: 80, functions: 80, statements: 80 }
    }
  }
  ```
- Scripts in `package.json`:
  ```json
  "test": "vitest run",
  "test:watch": "vitest",
  "test:coverage": "vitest run --coverage"
  ```

**E2E Tests — Playwright:**
```bash
npm install -D @playwright/test
npx playwright install
```
- `playwright.config.ts` erstellen mit sinnvollen Defaults
- `.env.test` Credentials nutzen (siehe `rules/testing.md`)
- `tests/` Verzeichnis erstellen falls nicht vorhanden

### Python
```bash
pip install pytest pytest-cov  # oder als dev-dependency in pyproject.toml
```
- `[tool.pytest.ini_options]` in `pyproject.toml` ergaenzen
- `tests/` Verzeichnis erstellen falls nicht vorhanden

### Go
- Keine Installation noetig — `go test` ist built-in
- `*_test.go` Dateien empfehlen neben dem zu testenden Code

## 7. Git Hooks einrichten

Nur einrichten falls noch KEINE Git Hooks konfiguriert sind.

### Node.js — Husky + lint-staged
```bash
npm install -D husky lint-staged
npx husky init
```

**pre-commit Hook** (`.husky/pre-commit`):
```bash
npx lint-staged
```

**lint-staged Config** in `package.json`:
```json
"lint-staged": {
  "*.{ts,tsx,js,jsx}": ["eslint --fix", "prettier --write"],
  "*.{json,md,yml,yaml}": ["prettier --write"]
}
```

**pre-push Hook** (`.husky/pre-push`) — nur erstellen falls Tests und Typecheck eingerichtet:
```bash
npm run typecheck 2>/dev/null; npm test
```

`package.json` Script sicherstellen:
```json
"prepare": "husky"
```

### Python — pre-commit Framework
```bash
pip install pre-commit
```

`.pre-commit-config.yaml` erstellen:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

```bash
pre-commit install
```

### Go / Rust / andere
Einfache Shell-Scripts in `.git/hooks/` erstellen:

**pre-commit:**
```bash
#!/bin/sh
# Go: gofmt + go vet
# Rust: cargo fmt --check + cargo clippy
```

Ausfuehrbar machen: `chmod +x .git/hooks/pre-commit`

## 8. CI/CD Pipeline

Nur erstellen falls noch KEINE CI-Config existiert.

### Plattform erkennen
- `.github/` Verzeichnis → GitHub Actions
- `.gitlab-ci.yml` → GitLab CI
- Falls unklar: den User fragen

### GitHub Actions Template

`.github/workflows/ci.yml` erstellen mit diesen Stages:

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # === Sprachspezifisch anpassen ===

      # Node.js:
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm run format:check
      - run: npx tsc --noEmit  # falls TypeScript
      - run: npm run test:coverage
      - run: npm run build
      - run: npm audit --audit-level=moderate

      # Python:
      # - uses: actions/setup-python@v5
      # - run: pip install -e ".[dev]"
      # - run: ruff check .
      # - run: pytest --cov --cov-fail-under=80

      # Go:
      # - uses: actions/setup-go@v5
      # - run: golangci-lint run
      # - run: go test -race -coverprofile=coverage.out ./...
```

**WICHTIG:** Nur die Sprach-Bloecke einkommentieren die zum Projekt passen. Die anderen entfernen.

### GitLab CI Template

`.gitlab-ci.yml` analog erstellen mit `stages: [lint, test, build]`.

## 9. Security Basics

### Dependency Scanning
Je nach Oekosystem passenden Audit-Befehl empfehlen und in CI einbauen:

| Oekosystem | Befehl |
|-----------|--------|
| Node.js | `npm audit --audit-level=moderate` |
| Python | `pip audit` (via `pip-audit` Package) |
| Go | `govulncheck ./...` |
| Rust | `cargo audit` |
| PHP | `composer audit` |

### Secret Scanning im Pre-commit Hook
Optional empfehlen — nicht automatisch installieren:
- `gitleaks` — Go-basiert, schnell, gut fuer pre-commit
- `detect-secrets` — Python-basiert, von Yelp

Dem User die Option vorstellen und nur installieren wenn gewuenscht.

## 10. Projekt-Dokumentation

### CLAUDE.md
Falls nicht vorhanden: `CLAUDE.md` im Projektroot erstellen mit:
- Projektname und kurze Beschreibung
- Erkannter Tech-Stack
- Wichtige Befehle (`dev`, `build`, `test`, `lint`)
- Projektstruktur-Ueberblick
- Konventionen (Commit-Style, Branch-Strategie falls erkennbar)

### README.md
Falls nicht vorhanden: `README.md` mit Setup-Anleitung erstellen:
- Voraussetzungen
- Installation
- Development Server starten
- Tests ausfuehren
- Umgebungsvariablen (Verweis auf `.env.example`)

## 11. Verifikation

Nach dem Setup alle eingerichteten Tools testen:

```bash
# Lint testen
npm run lint  # oder ruff check . oder golangci-lint run

# Formatter testen
npm run format:check  # oder ruff format --check . oder gofmt -l .

# Tests testen (falls Tests existieren)
npm test  # oder pytest oder go test ./...

# Git Hook testen
echo "test" >> /dev/null && git add -A && git diff --cached --stat
# (nur pruefen dass der Hook greift, nicht tatsaechlich committen)
```

Ergebnisse dem User zeigen. Bei Fehlern: beheben oder erklaeren warum sie auftreten.

## 12. Zusammenfassung

Am Ende dem User eine Uebersicht zeigen:

```
Projekt-Setup Zusammenfassung:
- Sprache/Framework: [erkannt]
- .gitignore: [erstellt/erweitert/bereits vorhanden]
- .env.example: [erstellt/bereits vorhanden]
- Linting: [ESLint/Ruff/...] [eingerichtet/bereits vorhanden]
- Formatting: [Prettier/Ruff/...] [eingerichtet/bereits vorhanden]
- Tests: [Vitest/pytest/...] [eingerichtet/bereits vorhanden]
- Git Hooks: [Husky/pre-commit/...] [eingerichtet/bereits vorhanden]
- CI/CD: [GitHub Actions/GitLab CI] [erstellt/bereits vorhanden]
- CLAUDE.md: [erstellt/bereits vorhanden]
- README.md: [erstellt/bereits vorhanden]
```
