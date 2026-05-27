---
name: ensure-tools
description: Verifies if a required CLI tool is installed and offers to install it. Use when about to execute a command whose binary might not be installed. Trigger: "¿tienes X instalado?", "instala Y si no está", "check dependencies", "setup environment".
user-invocable: false
allowed-tools: Bash(where *) Bash(which *) Bash(winget *) Bash(brew *) Bash(apt *) Bash(node --version) Bash(python --version) Bash(git --version)
---

# Skill: Ensure Tools

## Trigger

Activar cuando necesites verificar si una herramienta, CLI o runtime está disponible antes de usarla.
Ejemplos: "¿tienes X instalado?", "instala Y si no está", "necesito que uses Z", "verifica que tengas Node", "asegúrate de tener Python", "check dependencies", "setup environment"

También activarlo automáticamente cuando Claude vaya a ejecutar un comando cuyo binario podría no estar instalado en el sistema del usuario.

---

## Proceso

### Paso 1: Detectar si la herramienta está disponible

Antes de ejecutar o sugerir instalar, verificar si ya existe:

```bash
# El comando más portable para verificar existencia:
# Windows (PowerShell)
Get-Command <tool> -ErrorAction SilentlyContinue

# Unix/macOS
which <tool> 2>/dev/null || command -v <tool> 2>/dev/null
```

### Paso 2: Si NO está instalada — preguntar al usuario

**Nunca instalar sin confirmación explícita.** Presentar:

```
❓ [tool] no está instalado en tu sistema.
¿Deseas que lo instale ahora?

  [S] Sí, instalar automáticamente
  [N] No, lo instalaré manualmente
  [I] Ver instrucciones de instalación manual

⚠️  Nota: La instalación requiere permisos de administrador / internet.
```

### Paso 3: Si el usuario confirma — instalar con el gestor correcto

Seleccionar el gestor de instalación según el OS y la herramienta:

| Herramienta       | Windows                              | macOS                  | Linux (Debian/Ubuntu)     |
|-------------------|--------------------------------------|------------------------|---------------------------|
| Node.js / npm     | `winget install OpenJS.NodeJS`       | `brew install node`    | `apt install nodejs npm`  |
| Python            | `winget install Python.Python.3`     | `brew install python`  | `apt install python3 pip3`|
| Git               | `winget install Git.Git`             | `brew install git`     | `apt install git`         |
| Docker            | `winget install Docker.DockerDesktop`| `brew install --cask docker` | [Instrucciones Docker] |
| pnpm              | `npm install -g pnpm`                | `npm install -g pnpm`  | `npm install -g pnpm`     |
| Bun               | `npm install -g bun`                 | `brew install bun`     | `curl -fsSL https://bun.sh/install \| bash` |
| uv (Python)       | `pip install uv`                     | `brew install uv`      | `pip install uv`           |
| ruff              | `pip install ruff`                   | `brew install ruff`    | `pip install ruff`         |
| jq                | `winget install jqlang.jq`           | `brew install jq`      | `apt install jq`           |
| Rust / cargo      | `winget install Rustlang.Rust`       | `brew install rust`    | `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh` |
| kubectl           | `winget install Kubernetes.kubectl`  | `brew install kubectl` | [Instrucciones kubectl]   |

### Paso 4: Post-instalación — verificar que funcionó

Después de cada instalación:

```bash
# Verificar versión instalada
<tool> --version
# o
<tool> -v
```

Si la verificación falla después de instalar:
1. Indicar al usuario que puede necesitar reiniciar la terminal (PATH no recargado)
2. Sugerir el comando para recargar el PATH según el OS

---

## Detección del OS

Siempre detectar el OS antes de elegir el comando de instalación:

```python
# Python
import platform
os_name = platform.system()  # 'Windows', 'Darwin', 'Linux'
```

```javascript
// Node.js
const os = require('os');
os.platform()  // 'win32', 'darwin', 'linux'
```

```bash
# Bash/Shell
uname -s  # Darwin, Linux
# Windows: $env:OS en PowerShell
```

---

## Instalaciones que NUNCA se hacen sin confirmación

Sin importar el contexto, estas operaciones siempre requieren aprobación explícita:

- `sudo` / instalaciones globales de sistema
- Modificar `PATH`, `.bashrc`, `.zshrc`, `.profile`
- Instalar gestores de paquetes (Homebrew, Chocolatey, winget)
- Instalar Docker o runtimes de VM
- Instalar extensiones globales de npm/pip (`npm install -g`, `pip install` sin virtualenv)

---

## Formato de Salida al Usuario

Cuando se detecta una herramienta faltante, usar siempre este formato:

```
🔍 Verificando herramientas necesarias...

❌ [tool-name] (v[min-version]+) — No encontrado
✅ [other-tool] v[version] — OK

---
Para continuar necesito instalar: [tool-name]

Comando de instalación para [OS detectado]:
  [comando]

¿Procedo con la instalación? [S/N]
```

---

## ⚠️ Gotchas

- **No asumir el OS** — Siempre detectar antes de sugerir un comando. Un `brew install X` en Windows es inútil.
- **Versiones mínimas** — Algunos proyectos requieren versiones específicas (Node ≥20, Python ≥3.11). Verificar la versión instalada, no solo la existencia.
- **PATH no actualizado** — Después de instalar en Windows con `winget`, el binario puede no estar disponible hasta abrir una nueva terminal. Siempre advertir esto.
- **Permisos en Windows** — `winget` y instalaciones de sistema requieren PowerShell con permisos de administrador. Verificar antes de intentar.
- **Virtualenvs Python** — No instalar paquetes Python globalmente si el proyecto tiene `pyproject.toml` o `requirements.txt`. Siempre usar el entorno virtual del proyecto.
- **`npm install -g` en sistemas con permisos restrictivos** — En Linux/macOS sin configuración de npm, puede requerir `sudo`. Mejor usar nvm o un directorio local.
- **Alternativas a instalar** — Si el usuario rechaza instalar, buscar alternativas. ¿Hay un container Docker? ¿Un paquete npx? ¿Una versión web? Siempre ofrecer un plan B.
