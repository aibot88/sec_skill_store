---
name: transcribir-whatsapp
description: >
  Transcribe audios (notas de voz de WhatsApp y otros formatos: .ogg, .opus,
  .mp3, .m4a, .wav, .webm) a texto en español, y encadena automáticamente
  con el flujo procesos/procesar-audio.md para crear las actividades CRM en
  Holded y actualizar las fichas del brain. Usar SIEMPRE que el usuario
  adjunte uno o varios archivos de audio o pida "transcribe esto", "pásalo a
  texto", "transcribe el audio de X".
---

# transcribir-whatsapp

> Esta skill NO requiere instalación local. Funciona con cualquier Cowork moderno gracias a sus capacidades multimodales nativas. Sergio puede adjuntar audios desde su Mac sin instalar Python ni ffmpeg.

## 1. Gating por rol

Invoca `whoami` al inicio. Según `role`:

| Rol | Permisos |
|---|---|
| `noe`, `sergio` | Permitido. |
| Cualquier otro / `whoami` falla | Abortar: "transcribir-whatsapp solo está autorizado para Noé y Sergio." |

## 2. Formatos soportados

`.ogg`, `.opus`, `.mp3`, `.m4a`, `.wav`, `.webm`.

Si el archivo adjunto pesa **>50 MB**, avisar al usuario antes de procesar (puede tardar más de lo habitual).

## 3. Flujo

1. **Recibir** los audios adjuntos en el chat de Cowork (uno o varios). Si el usuario pega texto en vez de adjuntar audios, saltar al paso 3 — el texto ya es la transcripción.
2. **Transcribir** cada audio a texto literal en español usando las capacidades multimodales nativas de Cowork. Sin instalar nada, sin scripts, sin pre-flight checks.
3. **Encadenar** con [`procesos/procesar-audio.md`](../../procesos/procesar-audio.md) para que el texto transcrito se convierta en actividades CRM en Holded y se propaguen las fichas del brain.
4. **Devolver al usuario** en una sola respuesta:
   - Transcripción literal de cada audio en bloque markdown (`### Audio 1: nombre.ogg` + texto).
   - Tabla resumen de acciones realizadas en Holded (audio → empresa → eventos/tareas/notas/etapa).
   - Slugs de fichas actualizadas en el brain remoto, con el `updatedAt` devuelto por `entity-propagation`.

## 4. Si Cowork no puede transcribir un audio

Causas típicas: archivo corrupto, formato exótico no soportado, audio en otro idioma muy diferente del español.

- Mostrar mensaje claro al usuario: "No he podido transcribir `<nombre>`."
- **NO inventar contenido** ni dejar un placeholder genérico.
- Sugerir reenviar el audio en otro formato (.mp3 o .m4a suelen ser los más robustos).
- Continuar con los demás audios que sí se hayan transcrito correctamente.

## 5. Reglas duras

| Situación | Acción |
|---|---|
| Audio inaudible / sin contenido | Decir: "Audio ilegible, ¿puedes repetirlo?". NO inventar nada. |
| Archivo > 50 MB | Avisar al usuario antes de procesar. |
| Varios audios en una sola tanda | Procesar todos antes de invocar `procesar-audio` (una sola pasada al brain). |
| Usuario pega texto + adjunta audio | Tratar ambos como entradas separadas: el texto ya es transcripción, el audio se transcribe; ambos pasan juntos a `procesar-audio`. |
