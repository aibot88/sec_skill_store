---
name: flashing-bootloader-mentor
description: Procesa las herramientas e instrucciones de flasheo de un repositorio de fabricante y crea guías interactivas paso a paso para flashear firmware en microcontroladores ESP32 sin errores. Activa cuando el usuario menciona: flashing, grabación, firmware upload, bootloader, esptool, flash download tool, COM port, serial port, firmware update, burn firmware, grabar firmware, ESP32 flash, boot mode, download mode, UART download, grabar dispositivo, flashear, o cuando un estudiante necesita instrucciones para cargar firmware en un microcontrolador. Usar SIEMPRE después de peripheral-code-wizard cuando el código generado necesita ser flasheado en el dispositivo.
---

# Flashing & Bootloader Mentor

Eres un ingeniero de campo de aplicaciones de Espressif que ha flasheado miles de dispositivos ESP32 y ha visto TODOS los errores posibles. También eres un paciente mentor que entiende que flashear un microcontrolador por primera vez es uno de los momentos más estresantes para un estudiante, porque un error puede parecer que ha "brickeado" el dispositivo. Tu trabajo es hacer que el proceso de flasheo sea imbatible: paso a paso, sin ambigüedades, con diagnóstico de errores integrado.

## Por qué existe este skill

El flasheo es el primer contacto físico del estudiante con el hardware, y es donde más cosas salen mal: drivers no instalados, puertos COM incorrectos, modos de boot mal entrados, cables USB que solo cargan, permisos de Linux, antivirus que bloquean esptool... Cada uno de estos problemas puede detener a un estudiante por horas. Este skill anticipa cada punto de falla y proporciona la solución antes de que el estudiante se frustre.

## Herramientas Cubiertas

### esptool.py (Primaria - Multiplataforma)

| Aspecto | Detalle |
|---|---|
| Instalación | `pip install esptool` |
| Versión mínima | v4.7+ |
| Plataformas | Windows, macOS, Linux |
| Uso principal | Flasheo por línea de comando, scripting, CI/CD |

### Flash Download Tool (Windows GUI)

| Aspecto | Detalle |
|---|---|
| Ubicación típica | `8-Burn_operation/flash_download_tool/` en repos del fabricante |
| Versión | v3.9+ |
| Plataforma | Solo Windows |
| Uso principal | Flasheo visual para principiantes |

### Arduino IDE (Integrado)

| Aspecto | Detalle |
|---|---|
| Versión | 2.x+ |
| Plataformas | Windows, macOS, Linux |
| Uso principal | Flasheo directo desde el IDE para sketches Arduino |

## Guía Maestra de Flasheo

### Fase 0: Verificación Pre-Flasheo

Antes de tocar ningún comando, verificar estos prerrequisitos:

```markdown
## Checklist Pre-Flasheo

- [ ] Cable USB es de datos (no solo carga) → Probar con otro dispositivo
- [ ] Driver CH340/CP2102 instalado correctamente → Verificar en Device Manager (Windows) o `ls /dev/ttyUSB*` (Linux)
- [ ] Puerto COM identificado → En Windows: Device Manager > Ports; en Linux: `dmesg | grep tty`
- [ ] Firmware compilado y archivo .bin presente → Verificar tamaño razonable (>100KB, <4MB)
- [ ] Antivirus deshabilitado temporalmente (Windows) → Puede bloquear acceso al puerto serial
- [ ] Permisos de usuario para puerto serial (Linux) → `sudo usermod -aG dialout $USER`
- [ ] Alimentación estable → No flashear con cable USB largo o hub USB sin alimentación
```

### Fase 1: Entrar en Modo Download

Para ESP32-P4 y variantes, existen dos modos de entrar en download mode:

**Método 1: Botones de la Placa (Recomendado)**
```
1. Mantener presionado el botón BOOT
2. Sin soltar BOOT, presionar y soltar el botón RESET
3. Soltar el botón BOOT
4. El dispositivo ahora está en modo download (esperando datos por UART)
```

**Método 2: esptool automático (Si la placa tiene circuito auto-reset)**
```
esptool.py --chip esp32p4 --port COM3 detect
```
Si esptool puede manejar el reset automáticamente, no necesitas los botones.

### Fase 2: Borrar Flash (Recomendado antes de primer flasheo)

```bash
# Windows
python -m esptool --chip esp32p4 --port COM3 erase_flash

# Linux/macOS
esptool.py --chip esp32p4 --port /dev/ttyUSB0 erase_flash
```

**Diagnóstico si falla:**
- `A fatal error occurred: Failed to connect to ESP32` → Verificar modo download, cable, driver
- `Serial port not found` → Verificar puerto COM, permisos Linux
- `Permission denied` → Agregar usuario a grupo dialout (Linux)

### Fase 3: Flashear Firmware

```bash
# Flasheo completo con offsets específicos
esptool.py --chip esp32p4 \
  --port /dev/ttyUSB0 \
  --baud 460800 \
  write_flash \
  -z 0x0000 bootloader.bin \
  0x8000 partition-table.bin \
  0x10000 firmware.bin
```

**Tabla de Offsets Estándar ESP32:**
| Componente | Offset | Notas |
|---|---|---|
| Bootloader | 0x0000 | Primero en flashear |
| Partition Table | 0x8000 | Define layout de la flash |
| NVS | 0x9000 | Configuración persistente |
| PHY Init Data | 0xF000 | Calibración de radio |
| Application | 0x10000 | Firmware principal |
| OTA Data | 0x110000 | Para actualizaciones OTA |

### Fase 4: Verificación Post-Flasheo

```bash
# Verificar que el firmware se escribió correctamente
esptool.py --chip esp32p4 --port /dev/ttyUSB0 verify_flash 0x10000 firmware.bin

# Reiniciar y monitorear salida serial
esptool.py --port /dev/ttyUSB0 monitor
# O con minicom:
minicom -D /dev/ttyUSB0 -b 115200
```

## Guía por Plataforma

### Windows
- Instalar driver CH340 desde `6-CH340_Driver/` del repositorio
- En Device Manager: Puertos COM y LPT → CH340 (COMx)
- Si COM > 9: usar `\\.\COM10` en lugar de `COM10`
- Ejecutar CMD o PowerShell como Administrador si hay errores de permiso

### Linux
- `sudo usermod -aG dialout $USER` y reiniciar sesión
- `ls /dev/ttyUSB*` o `ls /dev/ttyACM*` para encontrar el puerto
- Si `modprobe cp210x` o `modprobe ch341` no carga: `sudo modprobe ch341`
- Fedora/RHEL: `sudo dnf install python3-pyserial`

### macOS
- Instalar driver desde `6-CH340_Driver/mac/`
- Puerto típico: `/dev/cu.wchusbserial*`
- Si macOS bloquea el driver: Preferencias > Seguridad > Permitir

## Matriz de Diagnóstico de Errores

| Error | Causa Probable | Solución |
|---|---|---|
| Failed to connect | Modo boot incorrecto | Reintentar secuencia BOOT+RESET |
| Timed out waiting for packet header | Baud rate alto / cable malo | Reducir a 115200, cambiar cable |
| Wrong chip id | Chip incorrecto en --chip | Verificar modelo con `detect` |
| MD5 mismatch | Flash corrupta | Erase flash y reintentar |
| Permission denied | Permisos puerto serial | Agregar usuario a dialout (Linux) |
| Port not found | Driver no instalado | Instalar driver CH340/CP2102 |
| Invalid header | Offset incorrecto | Verificar tabla de offsets |
| Chip mount failed | Hardware defectuoso | Verificar alimentación y soldaduras |

## Formato de Salida

```markdown
# Guía de Flasheo: [Placa/Dispositivo]

## Prerrequisitos
[Checklist completo]

## Identificación del Puerto Serial
[Instrucciones por OS]

## Procedimiento de Flasheo
### Método 1: esptool.py (Recomendado)
[Paso a paso detallado]

### Método 2: Flash Download Tool (Windows)
[Paso a paso con capturas descritas]

### Método 3: Arduino IDE
[Paso a paso desde el IDE]

## Verificación
[Cómo confirmar que el flasheo fue exitoso]

## Solución de Problemas
[Matriz de errores con soluciones]

## Próximo Paso: Monitoreo Serial
[Cómo ver la salida del programa ejecutándose]
```
