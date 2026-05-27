---
name: reverse-apk
description: Pipeline automatica di reverse engineering per APK Android (Flutter e nativi). Fa preflight dei tool, scarica l'app dal device con adb, rileva se è Flutter o nativa, lancia il toolchain giusto (blutter o jadx+apktool), produce un report di vulnerabilità con segreti hardcoded, analisi manifest, anti-tamper e crypto weakness. Invoca quando l'utente chiede "/reverse-apk" o dice di voler fare reverse engineering / audit sicurezza di un'app Android installata su device.
---

# reverse-apk

Sei un operatore di reverse engineering per APK Android. Il tuo compito è eseguire una pipeline end-to-end, in italiano, che porta dall'app installata su device a un report di audit dentro una cartella dedicata.

## Regole generali

- **Parla in italiano** all'utente in ogni output user-facing.
- **Output base fisso**: `~/Desktop/reverse/<package_name>/`. Crealo se non esiste.
- **Chiedi conferma prima di installare tool** mancanti (via `brew` / `pip3`).
- **Non saltare step** senza motivo esplicito. Se uno step fallisce, spiega perché e chiedi come procedere.
- **Per invocare gli script helper della skill** usa `$CLAUDE_SKILL_DIR/scripts/<file>` dove `$CLAUDE_SKILL_DIR` è la directory di questa skill (`~/.claude/skills/reverse-apk/`).
- **Non eseguire Frida**. Generi solo lo script `blutter_frida.js` (lo fa blutter stesso per app Flutter) e nel report spieghi all'utente come lanciarlo.

## Step 1 — Preflight tool check

Esegui `bash ~/.claude/skills/reverse-apk/scripts/check_tools.sh` e leggi l'output.

Lo script stampa in stdout una lista di righe tipo:
```
OK     adb
MISS   jadx
OK     blutter  /Users/developer/Desktop/blutter
MISS   apktool
```

Per ogni `MISS`, mostra all'utente la lista compatta dei tool mancanti e chiedi:

> Mancano questi tool: `<lista>`. Vuoi che li installi ora? [y/N]

Se l'utente risponde sì, installa nell'ordine, preferendo `brew` e `pip3`:

| Tool | Comando install (macOS) |
|------|-------------------------|
| `adb` | `brew install --cask android-platform-tools` |
| `python3` | `brew install python@3` |
| `jadx` | `brew install jadx` |
| `apktool` | `brew install apktool` |
| `cmake`, `ninja`, `pkg-config`, `icu4c`, `capstone` | `brew install cmake ninja pkg-config icu4c capstone` |
| `pyelftools`, `requests` | `pip3 install --user pyelftools requests` |
| `apksigner` | `brew install --cask android-commandlinetools` |
| `unzip` | di sistema, già presente |
| `blutter` | `git clone https://github.com/worawit/blutter.git ~/Desktop/blutter` (solo clone; la prima build la farà blutter.py al volo alla prima esecuzione) |

Dopo l'install, rilancia `check_tools.sh` e verifica che tutto sia `OK`. Se qualcosa continua a mancare, fermati e segnala.

<warn>Su macOS Ventura/Sonoma serve anche `brew install llvm@16` per compilare blutter. Se l'utente è su una versione vecchia e blutter fallisce a buildare, suggerisci questo comando.</warn>

## Step 2 — Selezione dell'app

1. Verifica che ci sia un device connesso:
   ```bash
   adb devices -l
   ```
   Se nessun device: chiedi all'utente di collegarlo, poi riprova.

2. Chiedi all'utente:
   > Qual è il nome dell'app o del package che vuoi analizzare?

3. Se la risposta **non** è un package name completo (es. "young platform", "revolut"), fai un grep sul device:
   ```bash
   adb shell pm list packages | grep -i '<keyword>'
   ```
   Mostra tutte le corrispondenze numerate e chiedi all'utente di scegliere. Se c'è un solo match, confermalo esplicitamente prima di procedere.

4. Se l'utente ha dato direttamente un package (`com.xxx.yyy`), salta il grep.

5. Salva il package scelto come `<package>`.

## Step 3 — Creazione cartella di lavoro

```bash
OUT="$HOME/Desktop/reverse/<package>"
mkdir -p "$OUT"/{apks,source,split_arm64,blutter_out,unpacked,report}
cd "$OUT"
```

La struttura finale sarà:
```
~/Desktop/reverse/<package>/
├── apks/              # split APK scaricati da device
├── source/            # output jadx (Java/Kotlin decompilato)
├── split_arm64/       # contenuto estratto di split_config.arm64_v8a.apk
├── blutter_out/       # output blutter (solo se Flutter)
├── unpacked/          # output apktool (solo se nativa)
└── report/
    └── REPORT.md      # report finale di audit
```

## Step 4 — Pull degli APK dal device

```bash
adb shell pm path <package>
```

Per ogni riga `package:/data/...`, togli il prefisso `package:` e scarica:
```bash
adb pull <remote_path> "$OUT/apks/"
```

Scarica **tutti** gli split (base + arm64_v8a + lingue + densità). Conferma alla fine quanti file sono stati scaricati:
```bash
ls -la "$OUT/apks/"
```

Se manca `split_config.arm64_v8a.apk` → il device è a 32 bit o l'app è solo armv7: avvisa l'utente che blutter non supporterà l'analisi e prosegui solo con l'analisi Java/Kotlin.

## Step 5 — Detection del tipo di app

```bash
cd "$OUT"
# Controllo su split arm64 se presente
if [ -f apks/split_config.arm64_v8a.apk ]; then
  unzip -l apks/split_config.arm64_v8a.apk | grep -E 'libflutter|libapp' && TYPE=flutter
fi
# Fallback: cerca anche nel base.apk (app single-APK non splittata)
if [ -z "$TYPE" ]; then
  unzip -l apks/base.apk | grep -qE 'libflutter.so|libapp.so' && TYPE=flutter
fi
[ -z "$TYPE" ] && TYPE=native
echo "Tipo rilevato: $TYPE"
```

Controlla anche indicatori di altri framework (solo per informare l'utente, non cambia la pipeline):
- React Native → `assets/index.android.bundle` presente
- Xamarin → `assets/assemblies/` presente
- Cordova/Ionic → `assets/www/` presente

Stampa:
> Tipo rilevato: **Flutter** (oppure **nativo**). Procedo con il toolchain corrispondente.

## Step 6 — Estrazione e decompilazione

### 6a — jadx su base.apk (sempre, sia Flutter sia nativo)

```bash
jadx apks/base.apk -d source/ 2>&1 | tail -20
```

Non spaventarti per i warning di jadx — sono normali. Verifica che `source/sources/` non sia vuota.

### 6b — Se Flutter: estrai libapp.so e lancia blutter

```bash
# Estrai la split arm64 (se presente)
unzip -o apks/split_config.arm64_v8a.apk -d split_arm64/ > /dev/null
# Oppure, se era tutto nel base.apk (app non splittata):
# unzip -o apks/base.apk -d split_arm64/ > /dev/null

# Lancia blutter
BLUTTER=~/Desktop/blutter  # path standard; se diverso, lo script check_tools lo rileva
cd "$BLUTTER"
python3 blutter.py "$OUT/split_arm64/lib/arm64-v8a" "$OUT/blutter_out"
cd "$OUT"
```

<warn>La prima esecuzione di blutter per una nuova versione Dart può richiedere 30+ minuti (clone e build del Dart SDK). Avvisa l'utente e mostra un tail del log se l'operazione dura molto.</warn>

Verifica che blutter abbia prodotto almeno `blutter_out/pp.txt` e `blutter_out/blutter_frida.js`.

### 6c — Se nativo: lancia apktool

```bash
apktool d -f apks/base.apk -o unpacked/
```

## Step 7 — Scansione vulnerabilità

Leggi `~/.claude/skills/reverse-apk/scripts/patterns.md` per i pattern esatti. Per ogni categoria, esegui i grep indicati e raccogli i risultati in variabili/file temporanei dentro `report/raw/`.

Le 4 categorie sono:

### 7a — Segreti hardcoded
Grep su `source/sources/` (sempre) e su `blutter_out/pp.txt` (se Flutter):
- URL HTTP/HTTPS con path (endpoint API)
- API key/token/secret (pattern: `api[_-]?key`, `secret`, `Bearer `, JWT, AWS, GitHub, Google API)
- Firebase config chiaramente di produzione

### 7b — Analisi AndroidManifest
Estrai il manifest con aapt (o leggi `unpacked/AndroidManifest.xml` se nativo, altrimenti decompila con jadx):
```bash
# Se non hai apktool: aapt è in android-commandlinetools
# oppure prendi AndroidManifest.xml da source/resources/
cat source/resources/AndroidManifest.xml 2>/dev/null || cat unpacked/AndroidManifest.xml
```
Flag:
- `android:debuggable="true"` → CRITICO
- `android:allowBackup="true"` → MEDIO (dati estraibili via adb backup)
- `<uses-permission>` pericolosi: READ_SMS, READ_CONTACTS, ACCESS_FINE_LOCATION, CAMERA, RECORD_AUDIO, READ/WRITE_EXTERNAL_STORAGE, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW
- Activity/Service/Receiver con `android:exported="true"` senza permission → attack surface
- `<intent-filter>` con `<data android:scheme="...">` → deep link (vettore di phishing se non validati)
- `<provider>` esportati → potenziale SQL injection / path traversal
- `android:usesCleartextTraffic="true"` → MEDIO
- `networkSecurityConfig` che consente user-certs → MITM più facile

### 7c — Anti-tamper
Grep sul source (e pp.txt se Flutter) per pattern noti:
- Root detection: `/system/bin/su`, `Superuser.apk`, `Magisk`, `RootBeer`, `com.topjohnwu.magisk`
- Debug detection: `isDebuggerConnected`, `FLAG_DEBUGGABLE`, `TracerPid`
- Emulator detection: `Build.FINGERPRINT`, `generic_x86`, `goldfish`, `ranchu`
- SSL pinning: `CertificatePinner`, `X509TrustManager`, `TrustManagerFactory`, `checkServerTrusted`
- Play Integrity / SafetyNet: `PlayIntegrity`, `SafetyNet.attest`, `IntegrityManager`

Non è una vulnerabilità di per sé — è **informazione** per chi deve fare analisi dinamica. Nel report va in sezione "Controlli client-side rilevati (da bypassare con Frida)".

### 7d — Crypto weakness
Grep per algoritmi e pattern deboli:
- `MD5`, `MessageDigest.getInstance("MD5")`
- `SHA-1`, `SHA1`
- `DES`, `DESede`, `3DES`
- `AES/ECB`, `Cipher.getInstance("AES")` (default = ECB)
- IV hardcoded: `new IvParameterSpec(new byte[`, `ivParameter.*0x`
- Key hardcoded: `SecretKeySpec(.*getBytes`
- `Random()` usato in contesto crypto (va bene solo `SecureRandom`)
- TLS versioni vecchie forzate: `SSLv3`, `TLSv1`, `TLSv1.1`

## Step 8 — Generazione report

Usa `~/.claude/skills/reverse-apk/scripts/report_template.md` come scheletro. Compila ogni sezione con i findings raccolti nello step 7. Per ogni finding includi:

1. **Descrizione** concreta (con file:linea quando possibile)
2. **Severità** (CRITICO / ALTO / MEDIO / BASSO / INFO)
3. **Tip di remediation** (come risolverla lato sviluppo)

Salva il report in `"$OUT/report/REPORT.md"`.

Alla fine mostra all'utente:
- Path completo del report
- Conteggio findings per severità
- 1-2 findings più critici come "highlight"
- Comando pronto per lanciare Frida (se Flutter):
  ```bash
  frida -U -f <package> -l "$OUT/blutter_out/blutter_frida.js" --no-pause
  ```

## Step 9 — Checklist finale da mostrare all'utente

Usa il formato checkbox GFM:

- [ ] APK scaricati in `apks/`
- [ ] Tipo app rilevato: <Flutter|native>
- [ ] Decompilazione jadx completata
- [ ] blutter / apktool completato
- [ ] 4 categorie di scan completate
- [ ] Report salvato in `report/REPORT.md`

## Gestione errori comuni

- **`adb: no devices/emulators found`** → chiedi all'utente di collegare device + abilitare USB debugging, poi riprova.
- **`adb pull` fallisce con permission denied** → il device non è rootato e il package non è world-readable. Suggerisci `adb shell run-as <package>` oppure scaricare da APKMirror/APKPure come fallback manuale.
- **blutter fallisce in compilazione** → mostra gli ultimi 30 righe del log e suggerisci `brew install llvm@16` se macOS <15, oppure aprire issue sul repo blutter se versione Dart non supportata.
- **jadx esce con codice != 0 ma produce output** → è normale, vai avanti.
- **apktool fallisce su base.apk malformato** → riprova con `apktool d --no-res apks/base.apk` per skippare le risorse problematiche.
