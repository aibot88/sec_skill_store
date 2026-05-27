---
name: os-awareness
description: >
  Evita errores por comandos incompatibles verificando SIEMPRE el SO antes de sugerir instalaciones.
  Trigger: "instalar", "upgrade", "apt", "brew", "winget", "configurar sistema", "error de comando".
license: MIT
metadata:
  author: Javier
  version: "1.1"
---

# OS Awareness (Protocolo de Seguridad)

> "Mira antes de saltar: Verifica el entorno antes de sugerir comandos."

Este skill obliga al agente a verificar el Sistema Operativo, la distribución y la arquitectura antes de sugerir comandos de sistema.

## Cuándo Usar

Activa este skill cuando:
- El usuario pide instalar un paquete ("instala node").
- El usuario pide configurar el sistema o actualizar.
- El usuario reporta un error de comando no encontrado.

**No usar cuando:**
- El usuario ya especificó explícitamente su SO en el prompt actual.
- Son comandos universales multiplataforma (`git`, `npm`, `python`).
- Se está operando dentro de un Dockerfile o entorno ya definido.

---

## Patrones Críticos

Las reglas MÁS importantes que el agente DEBE seguir para garantizar la portabilidad.

### Patrón 1: Verificación de Entorno (Look Before You Leap)

**Descripción**: NUNCA asumas que el usuario usa Ubuntu/Linux. Verifica siempre `os-release` o `uname` antes de dar un bloque de instalación.

```bash
# Ejemplo de implementación correcta
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "Distro: $ID"
elif command -v sw_vers >/dev/null; then
    echo "macOS Detected"
else
    uname -s
fi
```

### Patrón 2: Detección de Arquitectura

**Descripción**: Diferenciar entre `amd64` y `arm64` es vital para descargar binarios correctos (ej: GitHub Releases).

```bash
# Ejemplo de verificación
ARCH=$(uname -m)
if [[ "$ARCH" == "aarch64" || "$ARCH" == "arm64" ]]; then
    echo "Usar binario ARM64"
else
    echo "Usar binario AMD64"
fi
```

### Patrón 3: Portabilidad de Shell (Portable Patterns)

**Descripción**: Evita flags de GNU no compatibles con BSD (macOS), como `sed -i` o `date -d`.

```bash
# Ejemplo portable para sed
sed 's/old/new/g' file > file.tmp && mv file.tmp file
```

---

## Árbol de Decisiones

```
¿El usuario pidió un comando de sistema/instalación?
├── SÍ → ¿Sé en qué SO está el usuario (contexto previo)?
│   ├── SÍ → Generar comando para ese SO
│   └── NO → ejecutar script `detect_env.sh` o comandos de sondeo.
└── NO → Continuar ejecución normal.
```

---

## Ejemplos de Código

### ❌ Antipatrón: Asunción Ciega

**Problema**: Asumir `apt` rompe la experiencia en Fedora, macOS o Windows.

```bash
# MAL - No hacer esto
sudo apt install nodejs
```

### ✅ Patrón Correcto: Detección y Adaptación

**Solución**: El agente verifica primero y adapta el comando.

```text
Agente: "Verificaré tu sistema primero..."
(Ejecuta detección -> Detecta Fedora)
Agente: "Para Fedora, usa:"
```

```bash
# BIEN - Hacer esto
sudo dnf install nodejs
```

---

## Comandos Comunes

```bash
# Diagnóstico completo (Script incluido)
./skills/os-awareness/scripts/detect_env.sh

# Verificación rápida de Linux
cat /etc/os-release

# Verificación rápida de macOS
sw_vers

# Verificación de Windows (PowerShell)
$PSVersionTable
```

---

## Tabla de Referencia Rápida

| Sistema Detectado | Gestor Primario | Comando Ejemplo |
|-------------------|-----------------|-----------------|
| **Debian / Ubuntu** | `apt` | `sudo apt install pkg` |
| **Fedora / RHEL** | `dnf` | `sudo dnf install pkg` |
| **MacOS** | `brew` | `brew install pkg` |
| **Windows** | `winget` | `winget install pkg` |
| **Alpine** | `apk` | `apk add pkg` |

---

## Comportamiento del Agente

Cuando trabajes con este skill:

1.  **Primero**: Analiza si el comando solicitado depende del SO.
2.  **Validar**: Si no conoces el SO, emite comandos de verificación (o usa `detect_env.sh`).
3.  **Aplicar**: Selecciona la herramienta adecuada de la Tabla de Referencia.
4.  **Reportar**: Si detectas una arquitectura inusual (ARM), avisa al usuario antes de descargar binarios.
