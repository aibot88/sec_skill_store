---
name: install-dependencies-rules
description: >
  Usa esta skill SIEMPRE antes de añadir, actualizar o eliminar cualquier
  dependencia en un proyecto Node.js. Aplica a frontend, backend y monorepo.
  Cubre pnpm obligatorio, pin exact sin carets, consulta de última versión
  estable, auditoría post-instalación, protección contra paquetes comprometidos
  con herramientas gratuitas, y configuración de Dependabot para actualizaciones
  controladas.
---

# Reglas de Instalación de Dependencias

## Flujo del agente — cada vez que se instale una dependencia

1. **Evaluar** si la dependencia es necesaria (sección **Antes de instalar**).
2. **Consultar** la última versión estable con `pnpm view` antes de ejecutar `pnpm add`.
3. **Instalar** con pnpm, sin carets, con versión exacta explícita.
4. **Auditar** inmediatamente tras la instalación (`pnpm audit` + `osv-scanner`).
5. **Verificar** que CI corre `pnpm audit --audit-level=high` y `osv-scanner`.
6. **Confirmar** Dependabot configurado para recibir PRs de actualizaciones controladas.

## Cross-referencias

| Skill | Cuándo activar |
|-------|---------------|
| [`basic-workflows`](../basic-workflows/SKILL.md) | Configurar el step de `pnpm audit` en CI y Dependabot en el repositorio |
| [`security`](../backend/security/SKILL.md) | Si la dependencia expone endpoints o maneja datos — revisar implicaciones de seguridad |

---

## Antes de Instalar — Checklist Obligatorio

Antes de ejecutar cualquier `pnpm add`, responder estas preguntas:

| Pregunta | Criterio de aceptación |
|----------|----------------------|
| ¿Es realmente necesaria? | No se puede implementar con API nativa (Node.js / browser) en < 30 líneas |
| ¿Está mantenida? | Última release < 6 meses; issues respondidos; repositorio activo |
| ¿Tiene adopción? | > 10 K descargas semanales en npm |
| ¿Es la versión correcta? | Consultado con `pnpm view <paquete>` (ver sección siguiente) |
| ¿Tiene tipos? | Incluye `.d.ts` o existe `@types/<paquete>` |
| ¿Es tree-shakeable? | Exporta ESM con named imports — no importa el bundle entero |
| ¿Cuánto pesa? | Verificar en [bundlephobia.com](https://bundlephobia.com) — preferir alternativa si el tamaño es excesivo |
| ¿Licencia compatible? | MIT, Apache 2.0, ISC, BSD → OK. GPL → requiere aprobación |
| ¿Está limpia de malware? | Revisar con `osv-scanner` o `socket` antes del merge |

### Consultar metadatos antes de instalar

```bash
# Resumen completo: descripción, versión latest, maintainers, dist-tags
pnpm view <paquete>

# Solo la versión latest
pnpm view <paquete> version

# Todas las versiones publicadas
pnpm view <paquete> versions --json

# Tags disponibles (latest, next, beta)
pnpm view <paquete> dist-tags

# Repositorio, licencia y dependencias directas
pnpm view <paquete> repository license dependencies
```

Instalar **siempre la versión `latest`** salvo que haya razón documentada para una versión anterior.

---

## Instalación Segura

### Reglas de oro

1. **Solo pnpm** — nunca `npm install` ni `yarn add` en el proyecto.
2. **Pin exact, sin carets ni tildes** — `"zod": "3.23.8"` no `"zod": "^3.23.8"`.
3. **Versión explícita** — `pnpm add zod@3.23.8`, no `pnpm add zod` (aunque instale latest, el lockfile queda con `^`).
4. **Separar `dependencies` y `devDependencies`** — usar `-D` para todo lo que no llega a producción.

```bash
# ✅ Correcto — pin exact
pnpm add zod@3.23.8
pnpm add -D vitest@2.1.9

# ❌ Incorrecto — deja caret en package.json
pnpm add zod
pnpm add -D vitest
```

### ¿Por qué no carets?

Un caret (`^`) permite que `pnpm install` en otra máquina o en CI resuelva una versión **minor superior** sin que el equipo lo decida conscientemente. Los ataques de supply chain más frecuentes (ej: `event-stream`, `ua-parser-js`, `colors`) se distribuyen exactamente así: via una versión minor o patch comprometida que entra automáticamente a proyectos con carets.

**En su lugar**: pin exacto + Dependabot crea PRs para cada actualización → el equipo revisa antes de mergear.

### Configurar `.npmrc` para reforzar la regla

```ini
# .npmrc
auto-install-peers=true
strict-peer-dependencies=false
shamefully-hoist=false
resolution-mode=highest
prefer-frozen-lockfile=true
# Impedir que save-prefix="^" entre por defecto
save-exact=true
```

Con `save-exact=true`, `pnpm add zod` guardará `"zod": "3.23.8"` en lugar de `"zod": "^3.23.8"` automáticamente.

### `package.json` — declarar versiones de entorno

```json
{
  "packageManager": "pnpm@9.15.0",
  "engines": {
    "node": ">=20.0.0",
    "pnpm": ">=9.0.0"
  }
}
```

### `.nvmrc` — fijar versión de Node

```
20.18.0
```

---

## Operaciones del Día a Día

Comandos de mantenimiento habitual — no requieren el checklist de instalación nueva:

```bash
# Monorepo — instalar en la raíz del workspace
pnpm add -D -w eslint

# Actualizar dentro del rango declarado en package.json
pnpm update

# Actualizar a la última versión disponible (ignora el pin exacto)
# ⚠️ Correr pnpm audit + tests después
pnpm update --latest
pnpm update react --latest          # paquete específico

# Eliminar una dependencia
pnpm remove lodash

# Ver qué versiones más nuevas existen
pnpm outdated

# Mantenimiento del store global de pnpm
pnpm store prune                    # liberar espacio — versiones sin usar
pnpm dedupe                         # deduplicar entradas del lockfile
```

---

## Auditoría Post-Instalación

Correr **ambas** herramientas tras cada instalación o actualización:

### 1. `pnpm audit` (base de datos npm advisory)

```bash
pnpm audit                        # reporte completo
pnpm audit --audit-level=high     # falla solo en high/critical
pnpm audit --fix                  # aplica overrides automáticos cuando es posible
```

### 2. OSV-Scanner (base de datos OSV de Google — gratuito)

Escanea el `pnpm-lock.yaml` contra la base de datos Open Source Vulnerabilities, más amplia que la de npm:

```bash
# Instalar una vez
brew install osv-scanner           # macOS
# o: go install github.com/google/osv-scanner/cmd/osv-scanner@latest

# Escanear lockfile del proyecto
osv-scanner --lockfile=pnpm-lock.yaml

# Escanear todo el directorio (lockfiles + SBOM)
osv-scanner --recursive .
```

---

## Herramientas de Protección Gratuitas

| Herramienta | Qué detecta | Cómo usar | Gratuita |
|-------------|-------------|-----------|----------|
| `pnpm audit` | CVEs conocidas en npm advisory | `pnpm audit` | ✅ Siempre |
| **OSV-Scanner** (Google) | CVEs en OSV DB (más amplia que npm) | CLI + GitHub Action | ✅ Siempre |
| **Dependabot** (GitHub) | Dependencias desactualizadas con CVEs | `.github/dependabot.yml` | ✅ Repos públicos y privados |
| **Socket.dev** | Paquetes con comportamientos sospechosos (typosquatting, supply chain) | GitHub App + `npx socket` | ✅ App gratuita para repos públicos |
| **Snyk** | CVEs + license compliance | `npx snyk test` | ✅ Tier individual |

### Socket.dev — detección de paquetes comprometidos

Socket analiza el comportamiento del código de un paquete (acceso a red, sistema de archivos, ofuscación) — va más allá de CVEs conocidas.

```bash
# Escanear un paquete antes de instalarlo
npx @socketsecurity/cli npm info <paquete>@<version>
```

GitHub App (gratuita para repos públicos): instalar desde [socket.dev](https://socket.dev) para que revise automáticamente cada PR que modifique `package.json`.

### OSV-Scanner en GitHub Actions

```yaml
# .github/workflows/security.yml
- name: Run OSV-Scanner
  uses: google/osv-scanner-action@v1
  with:
    scan-args: |-
      --lockfile=./pnpm-lock.yaml
```

---

## Dependabot — Actualizaciones Controladas

Con todo pinned exacto, Dependabot es la única puerta de actualización: crea PRs individuales por dependencia que el equipo revisa y mergea.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly        # PRs los lunes, no a diario
      day: monday
      time: "09:00"
    open-pull-requests-limit: 5
    groups:
      dev-deps:
        patterns: ["*"]
        dependency-type: development
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]  # Majors = PR manual
```

Con `groups`, Dependabot agrupa todas las devDeps en un único PR semanal en lugar de docenas de PRs individuales.

---

## CI — Steps Obligatorios de Seguridad

```yaml
- name: Setup pnpm
  uses: pnpm/action-setup@v4
  with:
    version: 9

- name: Install dependencies
  run: pnpm install --frozen-lockfile   # falla si el lockfile no coincide

- name: Audit (npm advisory)
  run: pnpm audit --audit-level=high

- name: OSV-Scanner
  uses: google/osv-scanner-action@v1
  with:
    scan-args: |-
      --lockfile=./pnpm-lock.yaml
```

---

## Overrides y Patches

Cuando una dependencia transitiva tiene una vulnerabilidad y el autor no ha lanzado fix:

```json
// package.json
{
  "pnpm": {
    "overrides": {
      "glob@<9": ">=9.0.0",
      "semver@<7.5.2": ">=7.5.2"
    },
    "patchedDependencies": {
      "buggy-lib@1.2.3": "patches/buggy-lib@1.2.3.patch"
    }
  }
}
```

```bash
# Crear un patch para un bug upstream no resuelto
pnpm patch buggy-lib@1.2.3
pnpm patch-commit <carpeta-temporal>
```

Tras aplicar overrides, verificar con `pnpm audit` y `osv-scanner` — si pasa, el riesgo está mitigado.

---

## Scripts de package.json

Conjunto canónico de scripts para cualquier proyecto del equipo:

```json
{
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "type-check": "tsc --noEmit",
    "test": "vitest",
    "test:ci": "vitest run --coverage",
    "test:e2e": "playwright test",
    "analyze": "ANALYZE=true next build",
    "clean": "rm -rf .next node_modules/.cache",
    "prepare": "husky"
  }
}
```

---

## Reglas Obligatorias

1. **Solo pnpm** — prohibido `npm install`, `yarn add`, `npx install-*` en cualquier proyecto del equipo.
2. **`save-exact=true` en `.npmrc`** — configurado desde el inicio del repositorio.
3. **Pin exact siempre** — sin carets, sin tildes, en `dependencies` y `devDependencies`.
4. **`pnpm view <paquete>` antes de `pnpm add`** — nunca instalar sin verificar latest estable.
5. **`pnpm audit` inmediatamente post-instalación** — no abrir PR con vulnerabilidades high/critical.
6. **`osv-scanner --lockfile` en CI** — step no opcional; falla el pipeline si hay vulnerabilidades.
7. **Dependabot configurado** — desde el commit inicial del repositorio.
8. **`--frozen-lockfile` en CI** — sin excepción; si falla, el developer actualiza el lockfile localmente.
9. **`packageManager` y `engines` declarados** en `package.json`.
10. **No instalar paquetes con < 1 K descargas semanales** sin revisión manual del código fuente.

## Gotchas

- **`pnpm add <paquete>` sin versión** con `save-exact=false` guarda caret — verificar que `.npmrc` tiene `save-exact=true` antes del primer `pnpm add`.
- **`pnpm audit --fix` puede introducir overrides automáticos** que rompen features — revisar el diff de `package.json` tras ejecutarlo.
- **Dependabot no agrupa por defecto** — sin `groups`, genera un PR por dependencia y satura la bandeja de notificaciones.
- **`osv-scanner` en macOS requiere Go o Homebrew** — documentar instalación en `CONTRIBUTING.md` del proyecto.
- **Actualizar Node sin actualizar `.nvmrc`** genera inconsistencias entre dev y CI — los dos se actualizan juntos.
- **Socket.dev GitHub App solo es gratuita para repos públicos** — para repos privados, evaluar tier de pago o usar `npx @socketsecurity/cli` manualmente en revisiones de seguridad periódicas.
- **Dependencias de runtime en `devDependencies`** (o viceversa) rompen builds de producción o inflan el bundle — verificar siempre si la dependencia se usa en runtime.
- **Versiones flotantes** (`"*"` o `"latest"`) en sub-dependencias pueden seguir llegando vía transitive deps — usar `pnpm.overrides` para fijarlas; el lockfile de la app sola no es suficiente.
