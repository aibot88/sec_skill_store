---
name: clasp-master
description: >
  Full-stack CLASP (Command Line Apps Script) orchestration — from local dev to deployed Google Workspace automation.
  Use this skill whenever the user mentions clasp, Apps Script CLI, GAS local development, deploying Google Apps Script,
  syncing scripts with Drive, automating Sheets/Docs/Forms/Slides from the terminal, Google Workspace automation via code,
  or any workflow that involves clasp push/pull/deploy/run. Also trigger when the user says things like
  "quiero automatizar con AppScript", "deploy un script de Sheets", "versionar mi Apps Script", or
  "conectar clasp a Drive/Notion/Calendar". This skill covers installation, auth, multi-account, project lifecycle,
  version/deployment management, remote execution, TypeScript, Git integration, .claspignore, MCP mode, and enterprise
  patterns (ADC, service accounts). When in doubt, use this skill.
---

# CLASP Master

CLASP (Command Line Apps Script Projects) es el puente entre desarrollo local profesional y el ecosistema Google Workspace.
Con clasp, Apps Script deja de ser un editor de browser y se convierte en un proyecto versionable, deployable desde CI/CD,
y orquestable desde agentes.

---

## 1. INSTALACIÓN Y PREREQS

```bash
# Verificar Node.js (requiere >= v6, recomendado >= 18)
node -v && npm -v

# Instalar clasp globalmente
npm install -g @google/clasp

# Verificar instalación
clasp -v

# Habilitar Apps Script API (REQUERIDO antes de cualquier operación)
# https://script.google.com/home/usersettings → "Google Apps Script API" → ON
```

> ⚠️ **CRÍTICO**: La Google Apps Script API debe estar habilitada en la cuenta antes de `clasp login`.

---

## 2. AUTENTICACIÓN

```bash
clasp login                    # Abre browser para auth OAuth
clasp login --no-localhost     # Para entornos SSH/headless
clasp logout

# Multi-cuenta
clasp login --user personal
clasp login --user enterprise
clasp clone <scriptId> --user enterprise
clasp push --user enterprise
```

Credenciales en `~/.clasprc.json` (default) y `~/.clasprc.<user>.json` (named).

```bash
# OAuth client propio (enterprise)
clasp login --creds client_secret.json --user mykey

# Application Default Credentials (ADC / Service Account)
clasp push --adc
# Nota: SAs no pueden ser dueños de scripts — script debe estar compartido como Editor
```

---

## 3. GESTIÓN DE PROYECTOS

```bash
# Crear
clasp create --title "Mi Script" --type standalone
clasp create --title "Mi Script" --type sheets
clasp create --title "Mi Script" --type docs
clasp create --title "Mi Script" --type forms
clasp create --title "Mi Script" --type slides
clasp create --title "Mi Web App" --type webapp
clasp create --title "Mi Add-on" --type addon

# Clonar: Apps Script editor → Project Settings → Script ID
clasp clone <scriptId>
clasp clone <scriptId> --rootDir ./src

# Otros
clasp list       # Lista todos los proyectos
clasp open       # Abre en script.google.com
clasp open --webapp
clasp open --deploymentId <id>
```

---

## 4. SINCRONIZACIÓN

```bash
clasp pull                          # Descarga del proyecto
clasp pull --versionNumber 3        # Versión específica
clasp push                          # Sube archivos locales
clasp push --watch                  # Watch mode (dev loop)
clasp push -f                       # Force push
```

> ⚠️ **REGLA DE ORO**: No editar simultáneamente local Y script.google.com.

Estructura de directorios — clasp convierte automáticamente:
```
# Local:              → script.google.com:
src/utils/strings.gs → utils/strings.gs
src/Code.gs          → Code.gs
```

---

## 5. ARCHIVOS DE CONFIGURACIÓN

### `.clasp.json`
```json
{
  "scriptId": "1BxAbCdEfGhIjKlMnOpQrStUvWxYz_abc123",
  "rootDir": "./src",
  "projectId": "my-gcp-project-id",
  "fileExtension": "ts",
  "filePushOrder": ["src/init.ts", "src/Code.ts"]
}
```

### `.claspignore`
```
node_modules/**
.git/**
**/*.test.ts
README.md
.env
```
> `.claspignore` usa `multimatch`, diferente de `.gitignore` para directorios.

---

## 6. VERSIONES Y DEPLOYMENTS

```bash
clasp version "v1.0 - initial release"          # Crea versión
clasp versions                                   # Lista versiones

clasp deploy                                     # Deploy HEAD
clasp deploy --versionNumber 2 --description "hotfix"
clasp deployments                                # Lista deployments
clasp undeploy <deploymentId>
clasp undeploy --all
clasp redeploy <deploymentId> <version> "desc"
```

**Workflow prod:**
```bash
clasp push
clasp version "v2.1 - new feature X"
clasp deploy --versionNumber 3 --description "Production v2.1"
```

---

## 7. EJECUCIÓN REMOTA (`clasp run`)

```bash
# Setup: asociar GCP Project + OAuth Client ID Desktop
clasp login --creds client_secret.json --user runkey --use-project-scopes
# Agregar projectId al .clasp.json

clasp run                        # Prompt interactivo
clasp run helloWorld             # Función específica
clasp run myFunction -- arg1
```

---

## 8. LOGS

```bash
clasp logs                 # StackDriver recientes (solo console.log, NO Logger.log)
clasp logs --watch         # Streaming tiempo real
clasp logs --simplified
```

---

## 9. TYPESCRIPT

```bash
npm install -D @types/google-apps-script typescript
```

```json
// .clasp.json
{ "scriptId": "...", "rootDir": "./src", "fileExtension": "ts" }

// tsconfig.json
{ "compilerOptions": { "target": "ES2019", "lib": ["ES2019"], "strict": false } }
```

---

## 10. GIT INTEGRATION

```bash
# pre-push hook
#!/bin/bash
$(which clasp) push

chmod +x .git/hooks/pre-push
```

```bash
# Multi-env con clasp-env
npm install -D clasp-env
# package.json:
# "push:dev":  "clasp-env --folder src --scriptId DEV_ID && clasp push -w"
# "push:prod": "clasp-env --folder src --scriptId PROD_ID && clasp push"
```
> Agregar `.clasp.json` a `.gitignore` en setups multi-env.

---

## 11. MCP MODE (integración con agentes)

```bash
# Configurar como MCP server (Gemini CLI, Claude Code):
clasp mcp --transport stdio

# mcp_settings.json:
{
  "mcpServers": {
    "clasp": { "command": "clasp", "args": ["mcp", "--transport", "stdio"] }
  }
}
```
> Prerequisito: `clasp login` previo. Project dir se especifica en cada tool call.

---

## 12. WORKFLOWS COMUNES

```bash
# Script nuevo desde cero
mkdir mi-automation && cd mi-automation
clasp login
clasp create --title "Mi Automation" --type sheets
clasp pull
# ... editar localmente ...
clasp push
clasp version "v1.0"
clasp deploy --versionNumber 1 --description "Producción"

# Tomar control de script existente
mkdir proyecto && cd proyecto
clasp clone <scriptId>
git init && git add . && git commit -m "init: clonar proyecto existente"

# CI/CD (GitHub Actions):
# npm install -g @google/clasp
# echo $CLASP_RC > ~/.clasprc.json
# clasp push && clasp version "Build $SHA" && clasp deploy ...
```

---

## 13. TROUBLESHOOTING

| Error | Causa | Solución |
|-------|-------|----------|
| `Apps Script API has not been used` | API deshabilitada | Habilitar en script.google.com/home/usersettings |
| `Permission denied` | Sin acceso | Verificar que el script esté compartido |
| `clasp push` sobreescribe cambios | Edición dual | Nunca editar en ambos lados |
| `command not found: clasp` en hooks | PATH no disponible | Usar path absoluto: `$(which clasp)` |
| `Script API executable not published` | Sin deploy | `clasp deploy` primero |
| Logs vacíos | Usando `Logger.log` | Cambiar a `console.log` para StackDriver |

---

## REFERENCIA RÁPIDA

```
clasp login / logout / login --no-localhost / login --user <n>
clasp create --title "X" --type [standalone|sheets|docs|forms|slides|webapp|addon]
clasp clone <scriptId> | clasp list | clasp open [--webapp]
clasp pull [--versionNumber N] | clasp push [-f] [--watch]
clasp version "desc" | clasp versions
clasp deploy [--versionNumber N] [--description "desc"]
clasp deployments | clasp undeploy <id> | clasp redeploy <id> <v> "desc"
clasp run [functionName] | clasp logs [--watch]
clasp status | clasp mcp --transport stdio
```

---

## NOTA AUTOLIFE / CHEF COGNITIVO

- **clasp + MCP mode** = Apps Script ejecutable desde Claude/Gemini directamente
- **clasp + GitHub Actions** = CI/CD completo para GAS
- **clasp run** = invocar funciones GAS desde scripts locales (bridge Python/Node ↔ GAS)
- **Enterprise logging**: `console.log` + `clasp logs --watch` + StackDriver = traza completa

Ver `references/appsscript-manifest.md` para detalles del manifest y OAuth scopes.
