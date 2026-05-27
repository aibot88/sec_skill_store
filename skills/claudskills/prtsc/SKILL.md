---
name: prtsc
description: "Podiva se na posledni screenshoty z OneDrive Screenshots slozky a precte jejich obsah pomoci token-free OCR (Windows OCR API nebo Tesseract). Trigger: 'prtsc', '/prtsc', 'podivej se na screenshoty', 'co je na poslednim screenshotu', 'precti posledni screenshot'. Pouzij kdykoli uzivatel chce precist nebo popsat obsah nedavnych screenshotu."
---

# Prtsc — Screenshot reader (token-free OCR)

## PARAMETRY

| Parametr | Default | Popis |
|----------|---------|-------|
| `n` | smart | Bez --n: nejnovější + burst skupina (soubory do 2 min od sebe). S --n X: přesně X souborů. |
| `folder` | viz SCREENSHOT_DIR | Jina slozka (optional) |

## SCREENSHOT DIR

```
L:\OneDrive - Jihočeská univerzita v Českých Budějovicích\Pictures\Screenshots
```

## EXECUTION

### 1. Spust OCR skript (token-free)

```powershell
python L:/LG13/app/agent/skills/prtsc_ocr.py
```

Bez parametrů: smart mode — nejnovější screenshot + burst skupina (soubory do 2 min od sebe).
Explicitní počet: `--n 3` (přepíše smart logiku).

Skript najde soubory, spusti Windows OCR API, vytiskne text.

### 2. Interpretuj vystup

OCR text zobraz Tomovi + pridej kratky kontext (co pravdepodobne screenshot zachycuje).

## OUTPUT FORMAT

```
Screenshot 1 — 2026-05-13 14:32  [nazev souboru]
--- OCR text ---
<extracted text>
---
Kontext: <co je na obrazku>

Screenshot 2 — ...
```

## NOTES

- Pokud skript neexistuje → viz SCRIPT SETUP nize
- Pokud OCR vrati prazdny string → obrazek je graficky (bez textu), rict to Tomovi
- Pokud uzivatel rekne "posledni screenshot" (singular) → bez parametrů (smart vrátí 1 pokud není burst)
- Explicitní počet: `--n X` přepíše smart logiku
- Skript pouziva Windows.Media.Ocr (zero dependencies) s fallback na pytesseract

## BEZPEČNOST

Pokud OCR text obsahuje hesla, čísla karet, přihlašovací údaje — zobraz jen první 2 znaky + `***`, nezobrazuj celý řetězec. Citlivé věci nejdou do logu ani kontextu déle než nutné.

## SCRIPT SETUP

Pokud `L:/LG13/app/agent/skills/prtsc_ocr.py` neexistuje, vytvor ho:

```python
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

SCREENSHOTS_DIR = Path(r"L:\OneDrive - Jihočeská univerzita v Českých Budějovicích\Pictures\Screenshots")


def ocr_windows(image_path: Path) -> str:
    """Windows OCR API — zero dependencies."""
    try:
        import asyncio
        import winsdk.windows.media.ocr as ocr
        import winsdk.windows.graphics.imaging as imaging
        import winsdk.windows.storage as storage

        async def _run():
            file = await storage.StorageFile.get_file_from_path_async(str(image_path))
            stream = await file.open_async(0)
            decoder = await imaging.BitmapDecoder.create_async(stream)
            bitmap = await decoder.get_software_bitmap_async()
            engine = ocr.OcrEngine.try_create_from_user_profile_languages()
            if engine is None:
                engine = ocr.OcrEngine.try_create_from_language(
                    winsdk.windows.globalization.Language("cs-CZ")
                )
            result = await engine.recognize_async(bitmap)
            return result.text if result else ""

        return asyncio.run(_run())
    except Exception:
        return ""


def ocr_tesseract(image_path: Path) -> str:
    """Fallback: Tesseract."""
    try:
        import pytesseract
        from PIL import Image
        return pytesseract.image_to_string(Image.open(image_path), lang='ces+eng')
    except Exception:
        return ""


def ocr_file(image_path: Path) -> str:
    text = ocr_windows(image_path)
    if not text.strip():
        text = ocr_tesseract(image_path)
    return text.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=3)
    parser.add_argument('--folder', default=str(SCREENSHOTS_DIR))
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    folder = Path(args.folder)
    files = sorted(folder.glob('*.png'), key=lambda f: f.stat().st_mtime, reverse=True)[:args.n]

    results = []
    for f in files:
        mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
        text = ocr_file(f)
        results.append({'file': f.name, 'mtime': mtime, 'text': text})

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for i, r in enumerate(results, 1):
            print(f"Screenshot {i} — {r['mtime']}  [{r['file']}]")
            print("--- OCR text ---")
            print(r['text'] if r['text'] else "(zadny text / graficky obsah)")
            print("---\n")


if __name__ == '__main__':
    main()
```
