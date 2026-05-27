---
name: slint-android
description: >
  Expert guidance for building Android apps with Slint (Rust GUI toolkit). Use this skill whenever
  the user is working on a Slint UI — especially for Android targets — including .slint DSL syntax,
  component architecture, Cargo setup, Android backend configuration (cargo-apk, android-activity),
  Material Design 3 compliance, touch targets, dp/sp units, safe area insets, edge-to-edge layouts,
  dark mode, gestures, and responsive design for multiple Android screen densities. Trigger this skill
  when the user mentions Slint, .slint files, cargo-apk, slint Android, or asks about cross-platform
  Rust UI for mobile. Also trigger for any Android UI design questions involving density-independent
  pixels, Material 3 components, system bar insets, or gesture navigation.
---

# Slint Android Expert Skill

Slint ist ein deklaratives, reaktives GUI-Toolkit in Rust mit einer eigenen DSL (`.slint`-Dateien),
das nativ auf Android (ab v1.5), Desktop und Embedded läuft. Diese Skill-Anleitung deckt sowohl
die Slint-DSL als auch alle relevanten Android-UI-Designregeln ab.

---

## 1. Projekt-Setup: Cargo & Android-Backend

### Minimal Cargo.toml für Android

```toml
[package]
name = "meine-app"
version = "0.1.0"
edition = "2021"

[lib]
# PFLICHT für Android: cdylib
crate-type = ["cdylib"]

[dependencies]
# Slint mit Android-Activity-Backend (v0.6 empfohlen ab Slint 1.6+)
slint = { version = "1.9", features = ["backend-android-activity-06"] }

# Für ältere android-activity 0.5:
# slint = { version = "1.9", features = ["backend-android-activity-05"] }

[build-dependencies]
slint-build = "1.9"
```

### build.rs

```rust
fn main() {
    slint_build::compile("ui/app.slint").unwrap();
}
```

### Entry Point (lib.rs / main.rs)

```rust
// Für Android MUSS der Entry Point android_main heißen (kein fn main)
#[cfg(target_os = "android")]
#[no_mangle]
fn android_main(app: slint::android::AndroidApp) {
    slint::android::init(app).unwrap();
    
    let ui = AppWindow::new().unwrap();
    ui.run().unwrap();
}

// Desktop-Fallback
#[cfg(not(target_os = "android"))]
fn main() {
    let ui = AppWindow::new().unwrap();
    ui.run().unwrap();
}

slint::include_modules!();
```

### Umgebungsvariablen (vor cargo-apk)

```bash
export ANDROID_HOME=$HOME/Android/Sdk
export ANDROID_NDK_ROOT=$HOME/Android/Sdk/ndk/<version>
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk  # JDK 17 empfohlen (NICHT 21)
```

### Build & Deploy

```bash
# Targets installieren
rustup target add aarch64-linux-android   # echtes Gerät
rustup target add x86_64-linux-android    # Emulator

# cargo-apk installieren
cargo install cargo-apk

# Auf Gerät deployen
cargo apk run --target aarch64-linux-android --lib

# Auf Emulator
cargo apk run --target x86_64-linux-android --lib
```

> **Wichtig**: `i-slint-backend-android-activity` folgt KEIN SemVer. Immer mit `= "=x.y.z"` 
> exakt pinnen, wenn direkt als Dependency. Mit dem `features`-Flag am `slint`-Crate ist das 
> automatisch korrekt.

---

## 2. Das .slint DSL – Syntax & Konzepte

### Komponenten-Grundstruktur

```slint
// Imports aus der Standardbibliothek
import { Button, VerticalBox, HorizontalBox, ScrollView } from "std-widgets.slint";
// Material-Style-Widgets (für Android empfohlen)
import { Button, Switch, Slider, CheckBox, ComboBox } from "std-widgets.slint";

// Komponente deklarieren
export component MeinButton inherits Rectangle {
    // Eigenschaften
    in property <string> label: "Klick mich";
    in property <color> button-color: #6750A4;  // Material Primary
    out property <bool> ist-geklickt: false;
    in-out property <int> zaehler: 0;
    
    // Callback deklarieren
    callback geklickt();
    
    // Layout & Aussehen
    width: 200px;
    height: 48px;  // MINIMUM Touch Target!
    background: button-color;
    border-radius: 12px;
    
    Text {
        text: root.label;
        color: white;
        font-size: 14px;
        horizontal-alignment: center;
        vertical-alignment: center;
    }
    
    // Touch-Interaktion
    TouchArea {
        clicked => {
            root.zaehler += 1;
            root.geklickt();
        }
    }
}

// Hauptfenster
export component AppWindow inherits Window {
    title: "Meine Android App";
    // Kein festes width/height setzen – Android passt sich an
    
    VerticalBox {
        padding: 16px;
        spacing: 8px;
        
        MeinButton {
            label: "Los!";
            geklickt => { debug("Button geklickt!"); }
        }
    }
}
```

### Property-Typen

| Typ | Beispiel |
|-----|---------|
| `int` | `property <int> count: 0;` |
| `float` | `property <float> opacity: 1.0;` |
| `bool` | `property <bool> visible: true;` |
| `string` | `property <string> name: "Hallo";` |
| `color` | `property <color> bg: #FF5722;` |
| `brush` | Gradient oder Farbe |
| `length` | `property <length> size: 48px;` |
| `duration` | `property <duration> anim: 300ms;` |
| `image` | `@image-url("icon.png")` |
| `struct` | Eigene Datentypen |
| `[T]` | Arrays / Models |

### Property-Sichtbarkeit

```slint
in property <T> name;       // Nur von außen setzbar
out property <T> name;      // Nur von innen setzbar  
in-out property <T> name;   // Beide Richtungen
private property <T> name;  // Nur intern
```

### Two-Way Binding

```slint
export component Wrapper inherits Rectangle {
    in-out property <string> text <=> eingabe.text;  // direkte Verlinkung
    eingabe := TextInput {}
}
```

### Callbacks

```slint
export component Beispiel inherits Rectangle {
    callback aktion(string) -> bool;  // Mit Parameter und Rückgabe
    
    aktion(text) => {
        debug("Aktion: " + text);
        true
    }
    
    // Alias
    callback extern-geklickt <=> touch.clicked;
    touch := TouchArea {}
}
```

### Layouts

```slint
// Vertikal
VerticalLayout {
    spacing: 8px;
    padding: 16px;
    alignment: start;  // start | center | end | space-between | space-around
    
    Rectangle { height: 48px; }
    Rectangle { height: 48px; }
}

// Horizontal
HorizontalLayout {
    spacing: 12px;
    Rectangle { width: 50%; }  // Prozentangaben
    Rectangle { horizontal-stretch: 1; }  // Flexibel
}

// Grid
GridLayout {
    Row {
        Rectangle { colspan: 2; }
    }
    Row {
        Rectangle {}
        Rectangle {}
    }
}
```

### Animationen & Übergänge

```slint
Rectangle {
    property <bool> aktiv: false;
    background: aktiv ? #6750A4 : #E8DEF8;
    
    // Eigenschaftsanimation
    animate background {
        duration: 250ms;
        easing: ease-in-out;
    }
    
    // Positionsanimation
    x: aktiv ? 0px : 100px;
    animate x { duration: 300ms; easing: ease-out; }
}
```

### States & Transitions

```slint
Button {
    states [
        pressed when touch.pressed: {
            background: #4A3F8C;
            scale: 0.97;
        }
        hovered when touch.has-hover: {
            background: #7965AF;
        }
    ]
    transitions [
        in pressed: { animate background { duration: 80ms; } }
        out pressed: { animate background { duration: 200ms; } }
    ]
}
```

### Wiederholungen mit `for`

```slint
export component Liste inherits VerticalLayout {
    in property <[string]> eintraege;
    
    for eintrag[i] in eintraege: Rectangle {
        height: 56px;
        Text { text: eintrag; }
    }
}
```

### Globale Singletons

```slint
export global AppTheme {
    in-out property <bool> dark-mode: false;
    in-out property <color> primary: #6750A4;
    in-out property <color> background: dark-mode ? #1C1B1F : #FFFBFE;
}

// Nutzung in Rust:
// AppTheme::get(&ui).set_dark_mode(true);
```

---

## 3. Android-spezifisches UI-Design

### Das wichtigste Prinzip: Density-Independent Pixels (dp)

Android-Geräte haben stark unterschiedliche Pixeldichten. Slint verwendet `px`-Einheiten,
die intern auf der Logikdichte basieren — entsprechend Android dp:

| Android Dichte | DPI | Scale | Slint px ≈ |
|---------------|-----|-------|-----------|
| mdpi (Basis) | 160 | 1x | 1 dp |
| hdpi | 240 | 1.5x | 1.5 dp |
| xhdpi | 320 | 2x | 2 dp |
| xxhdpi | 480 | 3x | 3 dp |
| xxxhdpi | 640 | 4x | 4 dp |

> In Slint gibt es aktuell kein natives dp-System wie in Jetpack Compose. Verwende `self.Window.scale-factor` 
> um den Skalierungsfaktor abzurufen und physische Groessen korrekt zu berechnen.

### Touch-Targets: Die goldene Regel

```slint
// RICHTIG: Mindest-Touch-Target 48x48 (logische Pixel = dp)
TouchableIcon {
    width: max(48px, icon-size);
    height: max(48px, icon-size);
    
    // Sichtbarer Bereich kann kleiner sein
    Image {
        width: 24px; height: 24px;
        horizontal-alignment: center;
        vertical-alignment: center;
    }
}

// FALSCH: Zu kleines Touch-Target
Image {
    width: 16px; height: 16px;
    // TouchArea direkt drauf -> zu klein!
}
```

**Regeln:**
- Minimum: **48x48 px** (ca. 9mm physisch, entspricht 48dp)
- Abstand zwischen Touch-Targets: mindestens **8 px**
- Icons sind typisch 24px, aber Touch-Area muss 48px sein

### Safe Area / System Insets (Android 15+ Edge-to-Edge)

Ab Android 15 (API 35) zeichnet das System Apps standardmaessig edge-to-edge. 
Content darf nicht hinter Status Bar oder Navigationleiste verschwinden.

```slint
// Aktueller Workaround in Slint (natives Inset-API noch in Entwicklung):
// System-Insets über Rust-Backend einlesen und als Properties übergeben

export component SafeWindow inherits Window {
    // Von Rust gesetzt: slint::android::window_insets()
    in property <length> inset-top: 24px;     // Status Bar
    in property <length> inset-bottom: 48px;  // Navigationleiste / Gesture-Bar
    in property <length> inset-left: 0px;
    in property <length> inset-right: 0px;
    
    VerticalLayout {
        // Oben: Status Bar Padding
        Rectangle { height: root.inset-top; }
        
        // Inhalt
        VerticalLayout {
            padding-left: root.inset-left + 16px;
            padding-right: root.inset-right + 16px;
            vertical-stretch: 1;
            
            // ... App-Inhalt ...
        }
        
        // Unten: Navigation Bar Padding
        Rectangle { height: root.inset-bottom; }
    }
}
```

**Rust-Seite (Insets abrufen):**

```rust
// Vereinfachtes Beispiel – echte API variiert nach Slint-Version
#[cfg(target_os = "android")]
fn get_window_insets(app: &slint::android::AndroidApp) -> (f32, f32, f32, f32) {
    // Insets über android-activity API holen
    // top, bottom, left, right in logischen Pixeln
    (24.0, 48.0, 0.0, 0.0) // Fallback-Werte
}
```

### Material Design 3 – die Android-Designsprache

Slint enthält einen **Material-Style** für Widgets (`import { ... } from "std-widgets.slint"` 
mit gesetztem Material-Theme).

**Material 3 Farbsystem:**

```slint
// Material You Farbpalette (light mode)
export global Material3Colors {
    // Primary
    out property <color> primary: #6750A4;
    out property <color> on-primary: #FFFFFF;
    out property <color> primary-container: #EADDFF;
    out property <color> on-primary-container: #21005D;
    
    // Secondary
    out property <color> secondary: #625B71;
    out property <color> on-secondary: #FFFFFF;
    
    // Surface  
    out property <color> surface: #FFFBFE;
    out property <color> on-surface: #1C1B1F;
    out property <color> surface-variant: #E7E0EC;
    
    // Error
    out property <color> error: #B3261E;
    out property <color> on-error: #FFFFFF;
    
    // Dark Mode Varianten
    in property <bool> dark: false;
    out property <color> background: dark ? #1C1B1F : surface;
}
```

**Typografie (Material 3 Type Scale):**

```slint
// Schriftgroessen in sp (scale-independent pixels = logische px für Text)
// Minimum: 14px für Body-Text
export global TextStyles {
    // Display
    out property <length> display-large: 57px;
    out property <length> display-medium: 45px;
    out property <length> display-small: 36px;
    
    // Headline
    out property <length> headline-large: 32px;
    out property <length> headline-medium: 28px;
    out property <length> headline-small: 24px;
    
    // Title
    out property <length> title-large: 22px;
    out property <length> title-medium: 16px;
    out property <length> title-small: 14px;
    
    // Body (NIE unter 14px!)
    out property <length> body-large: 16px;
    out property <length> body-medium: 14px;
    out property <length> body-small: 12px;   // Nur für Captions!
    
    // Label
    out property <length> label-large: 14px;
    out property <length> label-medium: 12px;
    out property <length> label-small: 11px;
}
```

**Elevation & Schatten (Material 3):**

```slint
// Material 3 verwendet Tonal Elevation statt echte Schatten
component ElevatedCard inherits Rectangle {
    background: #F3EFF4;  // surface + primary overlay bei dp=1
    border-radius: 12px;
    
    // Slint drop-shadow für visuelle Tiefe
    drop-shadow-color: #00000033;
    drop-shadow-blur: 4px;
    drop-shadow-offset-y: 2px;
}
```

### Android Navigation Patterns

```slint
// Bottom Navigation Bar (haeufigstes Muster auf Phones)
export component BottomNavBar inherits Rectangle {
    in property <int> aktiver-tab: 0;
    in property <length> nav-inset: 0px;  // Navigationleisten-Inset
    
    height: 80px + nav-inset;
    background: #FFFBFE;
    
    // Trennlinie oben
    Rectangle {
        height: 1px;
        background: #CAC4D0;
    }
    
    HorizontalLayout {
        padding-bottom: nav-inset;
        
        for tab[i] in ["Startseite", "Suche", "Profil"]: NavItem {
            aktiv: aktiver-tab == i;
            label: tab;
            horizontal-stretch: 1;
        }
    }
}

component NavItem inherits Rectangle {
    in property <bool> aktiv;
    in property <string> label;
    callback geklickt();
    
    height: 80px;
    
    VerticalLayout {
        alignment: center;
        spacing: 4px;
        
        // Icon-Container (48x48 Touch Target)
        Rectangle {
            height: 32px;
            width: 64px;  // "pill" shape
            background: aktiv ? #EADDFF : transparent;
            border-radius: 16px;
            horizontal-alignment: center;
            
            // Icon hier einfuegen
        }
        
        Text {
            text: label;
            font-size: 12px;
            color: aktiv ? #6750A4 : #625B71;
            horizontal-alignment: center;
        }
    }
    
    TouchArea { clicked => { root.geklickt(); } }
}
```

### Scrollable Content

```slint
// Wichtig: ScrollView für langen Content
export component ScrollableScreen inherits Rectangle {
    in property <length> top-padding: 0px;
    in property <length> bottom-padding: 0px;
    
    ScrollView {
        // Wichtig: viewport-height muss gesetzt sein
        viewport-height: content.preferred-height;
        
        content := VerticalLayout {
            padding-top: top-padding + 16px;
            padding-bottom: bottom-padding + 16px;
            padding-left: 16px;
            padding-right: 16px;
            spacing: 12px;
            
            // Inhalt hier
        }
    }
}
```

### Responsive Design für verschiedene Bildschirmgroessen

```slint
export component AdaptivesLayout inherits Window {
    // Kompakt: Phone portrait (< 600px)
    // Medium: Tablet/Foldable (600-840px)
    // Expanded: Tablet landscape (> 840px)
    
    property <bool> ist-kompakt: root.width < 600px;
    property <bool> ist-erweitert: root.width >= 840px;
    
    if ist-kompakt: KompaktesLayout {}
    if !ist-kompakt && !ist-erweitert: MittleresLayout {}
    if ist-erweitert: ErweiterteLayout {}
}
```

### Dark Mode

```slint
export global AppTheme {
    // In Rust: slint::platform::SystemTheme (falls verfügbar) abfragen
    in-out property <bool> dark-mode: false;
    
    out property <color> hintergrund: dark-mode ? #1C1B1F : #FFFBFE;
    out property <color> auf-hintergrund: dark-mode ? #E6E1E5 : #1C1B1F;
    out property <color> oberflaeche: dark-mode ? #2B2930 : #FFFBFE;
    out property <color> primaer: dark-mode ? #D0BCFF : #6750A4;
    out property <color> auf-primaer: dark-mode ? #371E73 : #FFFFFF;
}

// In Rust den Dark Mode setzen:
// AppTheme::get(&ui).set_dark_mode(
//     std::env::var("SLINT_COLOR_SCHEME") == Ok("dark".into())
// );
```

---

## 4. Haeufige Muster & Best Practices

### Daten aus Rust an UI übergeben

```slint
// ui/app.slint
export struct Aufgabe {
    id: int,
    titel: string,
    erledigt: bool,
}

export component AppWindow inherits Window {
    in-out property <[Aufgabe]> aufgaben;
    callback aufgabe-erledigt(int);
    callback neue-aufgabe(string);
}
```

```rust
// main.rs
use slint::Model;

let ui = AppWindow::new().unwrap();
let model = std::rc::Rc::new(slint::VecModel::<Aufgabe>::from(vec![
    Aufgabe { id: 1, titel: "Einkaufen".into(), erledigt: false },
]));
ui.set_aufgaben(model.clone().into());
ui.on_aufgabe_erledigt(move |id| {
    // Model updaten
});
```

### Fehlervermeidung: Keine zyklischen Bindings

```slint
// FALSCH: Zyklus
property <int> a: b + 1;
property <int> b: a + 1;  // Endlosschleife!

// RICHTIG: Einseitige Abhängigkeit oder Callbacks
property <int> eingabe: 0;
property <int> ergebnis: eingabe * 2;  // OK
```

### Performance auf Android

- Vermeide sehr tiefe Layout-Verschachtelungen (> 10 Ebenen)
- Nutze `if`/`for` sparsam in animierten Bereichen
- Bilder mit `@image-url` werden zur Kompilierzeit eingebettet
- Für viele Listeneintraege: `VirtualModel` statt direktem Array
- Animationen: Maximal 300ms für major transitions, 80-150ms für micro-interactions

### Keyboard / Software-Tastatur

```slint
// TextInput öffnet automatisch die Soft-Keyboard
TextInput {
    width: parent.width;
    height: 48px;
    placeholder-text: "Suche...";
    input-type: text;  // text | password | number | decimal | email | url | phone
    
    // Auf Eingabe reagieren
    edited => { debug("Text: " + self.text); }
    accepted => { /* Return/Enter */ }
}
```

> **Bekanntes Problem**: `native-activity`-Feature hat eingeschraenkte Keyboard-Unterstützung.
> Für vollstaendige Tastatureingabe `game-activity`-Feature verwenden (benötigt Java-Stubs).

---

## 5. Checkliste vor Android-Deployment

- [ ] `[lib] crate-type = ["cdylib"]` in Cargo.toml gesetzt
- [ ] `backend-android-activity-06` Feature aktiviert
- [ ] Entry Point heisst `android_main`, nicht `main`
- [ ] `slint::android::init(app).unwrap()` als erste Zeile
- [ ] JDK 17 installiert (nicht 21 wegen bekanntem Bug)
- [ ] `ANDROID_HOME`, `ANDROID_NDK_ROOT`, `JAVA_HOME` gesetzt
- [ ] Alle Touch-Targets >= 48x48 px
- [ ] System-Insets (Status Bar, Navigation Bar) berücksichtigt
- [ ] Dark Mode getestet
- [ ] Auf echtem Geraet getestet (nicht nur Emulator)
- [ ] Schriftgroessen >= 14px für Body-Text
- [ ] Farbkontrast >= 4.5:1 (WCAG AA)
- [ ] Scrollbarer Content bei variablen Bildschirmhoehen

---

## 6. Wichtige Links

- Offizielle Doku: https://docs.slint.dev
- Android API: https://docs.slint.dev/latest/docs/rust/slint/android/
- Live Preview: https://slintpad.com
- Slint Material Widgets: `import { ... } from "std-widgets.slint"` mit `SLINT_STYLE=material`
- Beispielprojekte: https://github.com/slint-ui/slint/tree/master/examples
- Material Design 3: https://m3.material.io
