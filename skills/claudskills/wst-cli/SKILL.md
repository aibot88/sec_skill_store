---
name: wst-cli
description: CLI para organizar PDFs y libros con metadata generada por IA, búsqueda full-text (SQLite FTS5) y backups a iCloud o S3. Úsala cuando el usuario pida buscar, mostrar, ingestar o respaldar libros/PDFs en su biblioteca wst — por ejemplo "pasame tal libro a mi iPad", "ingestá esta carpeta a mi biblioteca", "mostrame qué libros tengo de Sagan", "hacé backup a iCloud del libro 12".
---

# Skill: biblioteca-digital-wan-shi-tong-wst-cli (wst)

CLI para organizar PDFs/libros con metadata generada por IA, búsqueda full‑text (SQLite FTS) y backups (iCloud/S3).

## Casos de uso (lo que la IA debe hacer)

### Llevar un libro a mi iCloud / iPad

Objetivo: dado un título aproximado, encontrar el libro en la biblioteca y subirlo a iCloud (para que aparezca en iPad).

Flujo recomendado:
1) Buscar el libro por texto.
2) Elegir el resultado correcto por **ID**.
3) Ejecutar backup a iCloud por ID.

Ejemplos:

```bash
wst search "story teller tactics" --format json
wst show 12 --format json
wst backup icloud 12 --format json
```

Instrucciones humanas típicas:
- “lleva de mi biblioteca a mi ipad el libro de *Story Teller Tactics*”
- “pásame a iCloud el libro *Cosmos*”

### Ingestar una carpeta a mi biblioteca

Objetivo: ingestarlo todo desde una carpeta que te indique (por ejemplo Escritorio) y meterlo en la biblioteca.

Ejemplos:

```bash
wst ingest ~/Desktop --format json
wst ingest ~/Desktop --ocr --ocr-language spa --format json
```

Instrucciones humanas típicas:
- “lleva a mi biblioteca los libros que dejé en mi escritorio”
- “ingesta la carpeta Descargas a mi biblioteca”

### Corregir la info de un libro con OCR

Objetivo: cuando un PDF escaneado no tiene texto, correr OCR y luego enriquecer/arreglar metadata.

Flujo recomendado (seguro):
1) OCR del archivo (si aplica).
2) Identificar el documento en la biblioteca.
3) Enriquecer metadata en el documento (o en lote con `fix`).

Ejemplos:

```bash
# 1) OCR al archivo antes de ingestar (si aún no está en la biblioteca)
wst ingest ~/Desktop/scan.pdf --ocr --ocr-language spa --format json

# 2) Si ya está en la biblioteca, ubícalo por búsqueda y enriquece
wst search "topologia" --format json
wst edit 12 --enrich -y --format json
```

Instrucciones humanas típicas:
- “corrige la info del libro X y si es escaneado pásale OCR”
- “¿qué libro de topología tengo en mi biblioteca?”

## Instalación

### pipx (recomendado)

```bash
pipx install wst-library
```

### pip

```bash
pip install wst-library
```

### Extras opcionales

- OCR:

```bash
pip install "wst-library[ocr]"
```

- S3 backup:

```bash
pip install "wst-library[s3]"
```

## Output para humanos vs máquinas

Todos los comandos aceptan `--format human|md|json|yaml` (default `human`).

- `--format human`: pensado para terminal (tablas, mensajes, progreso).
- `--format md|json|yaml`: pensado para automatización.
  - No hay prompts interactivos.
  - La salida es determinística (sin barras de progreso).
  - El payload es estable:
    - Éxito: `{ "ok": true, "data": ... }`
    - Error: `{ "ok": false, "error": { "code": ..., "message": ..., "details": ... } }`

## Comandos principales (no interactivos)

### Listar

```bash
wst list
wst list --format json
wst list --type paper --sort year --format yaml
```

### Buscar

```bash
wst search "machine learning"
wst search "cosmos" --author "Sagan" --format json
```

Ejemplos orientados a preguntas humanas:

```bash
# “¿Qué libro de topología tengo en mi biblioteca?”
wst search "topologia" --format json
wst search "topology" --format json
```

### Mostrar metadata completa

```bash
wst show 3
wst show 3 --format yaml
```

### Ingesta

```bash
wst ingest
wst ingest ~/Downloads/book.pdf
wst ingest --ocr --ocr-language spa
wst ingest --format json
```

Notas:
- `--confirm` es interactivo (pregunta por archivo). Evitar en pipelines.
- `-v/--verbose` imprime logs por archivo (útil para debugging humano).

### OCR

```bash
wst ocr scan.pdf --format json
wst ocr ~/scans -l spa+eng --format yaml
```

### Enriquecer metadata en lote

```bash
wst fix --dry-run --format json
wst fix -y --format yaml
```

## Comandos interactivos (y alternativas scriptables)

### `wst browse`

- Interactivo:

```bash
wst browse
```

- Scriptable (sin prompts):

```bash
wst browse --id 3 --action view --format json
wst browse --query "cosmos" --first --action view --format yaml
wst browse --id 3 --action open --no-launch --format json
wst browse --id 3 --action delete --dry-run --format md
wst browse --id 3 --action delete -y --format json
wst browse --id 3 --action edit --set title="New" --dry-run --format json
wst browse --id 3 --action edit --set title="New" -y --format json
```

### `wst edit`

- Interactivo por defecto:

```bash
wst edit 3
```

- No interactivo:

```bash
wst edit 3 --set title="New title" --dry-run --format json
wst edit 3 --set title="New title" -y --format yaml
wst edit 3 --enrich -y --format json
```

## Backup (consideraciones)

En general, el setup/configuración puede requerir modo humano.

```bash
# S3 configure: interactivo
wst backup s3 --configure --format human

# Backup por ID/título (scriptable)
wst backup s3 3 --format json
wst backup icloud "Cosmos" --format yaml
```

## Reglas para IA (operación segura y reproducible)

- Preferir **IDs** (`wst list`/`wst search`) para seleccionar documentos en vez de títulos aproximados.
- Para instrucciones humanas ambiguas (“llévalo al iPad”), asumir que significa **`backup icloud`**.
- En `--format md|json|yaml`, evitar cualquier comando que requiera prompts; usar `-y`, `--dry-run`, `--set` según corresponda.
- Para acciones potencialmente destructivas:
  - usar `--dry-run` primero cuando exista
  - exigir `-y/--yes` para aplicar
- Para `open/find` desde automatización, usar `--no-launch` para no abrir apps.

