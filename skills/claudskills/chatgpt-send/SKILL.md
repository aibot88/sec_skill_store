---
name: chatgpt-send
description: "Posle zpravu do ChatGPT vlakna pres Playwright CDP — ovlada Edge prohlizec a zapise zpravu primo do ChatGPT input boxu. Pouzij kdyz uzivatel explicitne chce ODESLAT zpravu: 'chatgpt-send', '/chatgpt-send', 'spust chatgpt-send', nebo 'posli [neco] do chatgpt pres playwright/CDP'. Parametry: project= (Legal/Coding/LG13), thread= (URL), message= (text), special= (/github /search). Nepouz: kdyz uzivatel jen mluvi o chatgpt, chce precist odpoved (→ chatgpt-force-read), nebo chce second-opinion (→ chatgpt-ask)."
user-invocable: true
---

# ChatGPT Send — Playwright CDP messenger

## PARAMETRY

| Parametr | Popis | Příklad |
|----------|-------|---------|
| `project` | Název ChatGPT projektu (sidebar) | `Legal`, `LG13`, `Coding` |
| `thread` | URL vlákna nebo název z Recents | `https://chatgpt.com/c/6a04...` nebo `"Skill update request"` |
| `message` | Text zprávy | `"Zkontroluj tento dokument..."` |
| `special` | Speciální příkazy před zprávou | `/github`, `/search`, `/image` |

## CDP AUTOFIX (vždy první krok)

Před každým použitím Playwright ověř CDP port. Pokud nereaguje → automaticky restartuj Edge:

```python
import urllib.request, subprocess, time, sys

def ensure_edge_cdp():
    """Ověří CDP port 9222, při selhání restartuje Edge s debug portem."""
    try:
        urllib.request.urlopen("http://localhost:9222/json/version", timeout=2)
        print("CDP OK")
        return True
    except Exception:
        print("CDP nedostupný — restartuji Edge s --remote-debugging-port=9222...")
        subprocess.run(
            ["powershell", "-Command",
             "Get-Process msedge -ErrorAction SilentlyContinue | Stop-Process -Force"],
            capture_output=True
        )
        time.sleep(2)
        subprocess.Popen([
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "--remote-debugging-port=9222",
            "--profile-directory=Default"
        ])
        time.sleep(5)
        try:
            urllib.request.urlopen("http://localhost:9222/json/version", timeout=3)
            print("Edge restartován, CDP OK")
            return True
        except Exception as e:
            print(f"FATAL: CDP stále nefunguje po restartu: {e}")
            return False

ensure_edge_cdp()
```

## POST-SEND: PŘENÉST EDGE NA PLOCHU

Po odeslání zprávy Edge maximalizuj a přesuň do popředí (aby Tom viděl výsledek):

```python
import subprocess
# Maximalizuj Edge a přesuň do popředí
subprocess.run([
    "powershell", "-Command",
    """
    Add-Type -TypeDefinition '
    using System;using System.Runtime.InteropServices;
    public class Win32 {
        [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
        [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    }'
    $proc = Get-Process msedge | Sort-Object MainWindowHandle -Descending | Select-Object -First 1
    if ($proc -and $proc.MainWindowHandle -ne 0) {
        [Win32]::ShowWindow($proc.MainWindowHandle, 3)  # SW_MAXIMIZE
        [Win32]::SetForegroundWindow($proc.MainWindowHandle)
    }
    """
], capture_output=True)
print("Edge přenesen na plochu (maximalizován)")
```

## EXECUTION

```python
from playwright.sync_api import sync_playwright
import time, sys, urllib.request, subprocess
sys.stdout.reconfigure(encoding='utf-8')

# --- PARAMETRY (vyplň před spuštěním) ---
PROJECT  = None          # např. "Legal" — None = bez projektu
THREAD   = None          # URL nebo None = nový chat
MESSAGE  = "..."         # zpráva
SPECIAL  = None          # např. "/github" — None = bez speciálního příkazu
SS_PATH  = "C:/Users/tom/AppData/Local/Temp/chatgpt_send.png"
# ----------------------------------------

# 0. CDP autofix (vždy první)
def ensure_edge_cdp():
    try:
        urllib.request.urlopen("http://localhost:9222/json/version", timeout=2)
        return True
    except Exception:
        print("CDP nedostupný — restartuji Edge...")
        subprocess.run(["powershell","-Command","Get-Process msedge -ErrorAction SilentlyContinue | Stop-Process -Force"], capture_output=True)
        time.sleep(2)
        subprocess.Popen([r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe","--remote-debugging-port=9222","--profile-directory=Default"])
        time.sleep(5)
        return True

ensure_edge_cdp()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    ctx = browser.contexts[0]

    # 1. Najdi nebo otevři tab (cap enforced; send = tab stays open for Tom)
    import sys as _s; _s.path.insert(0,'L:/LG13/app/agent')
    from chatgpt_tab_manager import get_or_open_tab
    page, _obu = get_or_open_tab(ctx, THREAD if (THREAD and THREAD.startswith('http')) else None)

    # 2. Navigace
    if THREAD and THREAD.startswith("http"):
        page.goto(THREAD, timeout=20000)
    elif PROJECT:
        page.goto("https://chatgpt.com/", timeout=20000)
        page.wait_for_timeout(3000)
        page.evaluate(f'''() => {{
            const items = [...document.querySelectorAll("nav a, [data-testid*=project], li")];
            const match = items.find(el => el.textContent.includes("{PROJECT}"));
            if (match) match.click();
        }}''')
        page.wait_for_timeout(2000)
        page.evaluate('''() => {
            const btn = [...document.querySelectorAll("button,a")].find(el =>
                el.textContent.includes("New chat") || el.textContent.includes("Nový chat"));
            if (btn) btn.click();
        }''')
    else:
        page.goto("https://chatgpt.com/", timeout=20000)

    page.wait_for_timeout(4000)

    # 3. Pošli special command pokud je zadán
    if SPECIAL:
        page.evaluate('document.querySelector("#prompt-textarea")?.focus()')
        page.wait_for_timeout(300)
        page.keyboard.type(SPECIAL)
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)

    # 4. Pošli zprávu
    page.evaluate('document.querySelector("#prompt-textarea")?.focus()')
    page.wait_for_timeout(300)
    page.keyboard.type(MESSAGE)
    page.wait_for_timeout(500)
    page.keyboard.press("Enter")
    print(f"Sent: {MESSAGE[:80]}...")

    # 5. Čekej na odpověď
    for _ in range(40):
        time.sleep(1)
        if "/c/" in page.url:
            break
    page.wait_for_timeout(10000)

    # 6. Screenshot
    page.screenshot(path=SS_PATH)
    print(f"Screenshot: {SS_PATH}")
    print(f"Thread URL: {page.url}")

# 7. Přenést Edge na plochu (maximalizovat)
subprocess.run(["powershell","-Command","""
    Add-Type -TypeDefinition 'using System;using System.Runtime.InteropServices;public class W{[DllImport("user32.dll")]public static extern bool ShowWindow(IntPtr h,int n);[DllImport("user32.dll")]public static extern bool SetForegroundWindow(IntPtr h);}'
    $p=Get-Process msedge|Sort MainWindowHandle -Desc|Select -First 1
    if($p -and $p.MainWindowHandle -ne 0){[W]::ShowWindow($p.MainWindowHandle,3);[W]::SetForegroundWindow($p.MainWindowHandle)}
"""], capture_output=True)
print("Edge maximalizován na ploše")
```

## VÝSTUP

```
Sent: <zpráva>
Screenshot: C:/Users/tom/AppData/Local/Temp/chatgpt_send.png
Thread URL: https://chatgpt.com/c/<id>
```

## AUTO-CHOICE (60s timeout)

Pokud skill čeká na uživatelský vstup (chybí project/thread/message) a uživatel neodpoví:
- Zobraz: "Chybí parametr X. Default: [konkrétní default]. Pokračuji za 60s..."
- Po 60s bez odpovědi → použij default, neptat se znovu
- Default pro message: neposílat, FAIL s hláškou "message required"
- Default pro project/thread: nový chat bez projektu

**Nikdy nečekej indefinitely — to blokuje celou instanci.**

## NOTES

- Pokud Edge nemá CDP port → viz PREREKVIZITY
- `/github` se musí zadat jako první zpráva v novém vlákně (ChatGPT aktivuje tool)
- Pro `/github` pošli nejdřív URL repo souboru jako druhou zprávu
- TM ingest zachytí odpověď automaticky a doručí atom do instance stacku
- Výsledek odpoví do legal stacku pokud GPT vrátí `to: [lik]` v LG13_META
