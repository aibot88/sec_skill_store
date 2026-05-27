---
name: ap1-training-tracker
description: IHK Fachinformatiker AP1 Training-Tracker mit 280 Fragen in SQLite-Datenbank. 50 Subnetting-Fragen, interaktives Training, automatische Statistiken. Der Kollege muss nur den Skill-Ordner in sein OpenClaw Workspace kopieren und das Script ausführen.
---

# AP1 Training Tracker v2.0

**280 Fragen** | **50 Subnetting** | **SQLite-basiert**

Professioneller IHK Fachinformatiker AP1 Lern-Tracker – einfach zu installieren, sofort einsatzbereit.

## 📦 Installation (für Kollegen)

```bash
# 1. ZIP entpacken
unzip ap1-training-tracker.zip -d ~/openclaw-workspace/

# 2. Fertig! Das Script ist sofort nutzbar
python3 skills/ap1-training-tracker/scripts/ap1_training.py --help
```

**Das ist alles!** Keine Abhängigkeiten, keine Config, keine API-Keys.

## 📁 Struktur

```
skills/ap1-training-tracker/
├── data/
│   └── questions.db          # 280 Fragen in SQLite
├── scripts/
│   └── ap1_training.py       # Hauptscript
└── SKILL.md                  # Diese Datei
```

## 🚀 Schnellstart

### Tägliche 3 Fragen

```bash
python3 skills/ap1-training-tracker/scripts/ap1_training.py --daily
```

### Antwort speichern (nach jeder Frage)

```bash
python3 skills/ap1-training-tracker/scripts/ap1_training.py --save <id> <antwort> <0|1> <kategorie>

# Beispiel:
python3 skills/ap1-training-tracker/scripts/ap1_training.py --save sub_001 B 1 "IT-Grundlagen"
```

### Statistiken

```bash
python3 skills/ap1-training-tracker/scripts/ap1_training.py --stats      # Woche
python3 skills/ap1-training-tracker/scripts/ap1_training.py --stats-month  # Monat
python3 skills/ap1-training-tracker/scripts/ap1_training.py --stats-all  # Gesamt
```

## 📊 280 Fragen - Verteilung

| Thema | Fragen | Highlights |
|-------|--------|------------|
| IT-Grundlagen | 90 | 50 Subnetting + 20 Netzwerk + 20 OSI/Hardware |
| Software-Entwicklung | 40 | OOP, Git, Debugging, Clean Code |
| Datenbanken | 40 | SQL, Normalisierung, ACID |
| IT-Sicherheit | 40 | VPN, 2FA, Verschlüsselung, Angriffe |
| Projektmanagement | 35 | Scrum, Gantt, Netzplan, Risiko |
| Wirtschaft | 35 | BWL, Steuern, Verträge, Marketing |

**Gesamt: 280 Fragen** ✅

## 🔄 Cron-Job (automatisch täglich)

```yaml
# OpenClaw Cron-Konfiguration
- name: ap1-training
  schedule:
    kind: cron
    expr: "30 9 * * *"  # Täglich 09:30
    tz: "Europe/Berlin"
  payload:
    kind: systemEvent
    text: "CRON_AP1_TRAINING"
  sessionTarget: main
  enabled: true
```

### Ablauf:

1. **09:30 Uhr** → Cron sendet `CRON_AP1_TRAINING`
2. **Ich stelle Frage 1** → Warte auf Antwort
3. **User antwortet** → Speichere mit `--save`
4. **Zeige Ergebnis** → Richtig/Falsch + Erklärung
5. **Frage 2** → Wiederholen
6. **Frage 3** → Wiederholen
7. **Tagesabschluss** → Statistik anzeigen

## 📝 Beispiel-Session

```
📚 FRAGE 1/3
📱 IT-Grundlagen

❓ Wie viele Hosts hat ein /24-Netzwerk?
   A) 254
   B) 256
   C) 512
   D) 1024

User: C

❌ FALSCH! Richtig wäre A) 254
   Erklärung: /24 = 8 Host-Bits = 2^8 - 2 = 254
   (Netz- und Broadcast-Adresse abziehen)

─────────────────────────────

📚 FRAGE 2/3
📱 Software-Entwicklung

❓ Was macht git commit?
   A) Sendet zum Server
   B) Speichert lokal
   C) Löscht Dateien
   D) Erstellt einen Branch

User: B

✅ RICHTIG! git commit speichert Änderungen 
   lokal im Repository.

─────────────────────────────
```

## 🎯 Interaktiver Modus

Das Script kann auch direkt in Python verwendet werden:

```python
import sys
sys.path.insert(0, 'skills/ap1-training-tracker/scripts')
from ap1_training import get_random_questions, save_attempt, get_stats

# 3 Fragen holen
questions = get_random_questions(3)

# Nach Antwort speichern
save_attempt('sub_001', 'B', True, 'IT-Grundlagen')

# Statistik anzeigen
stats = get_stats()
print(f"{stats['correct']}/{stats['total']}")
```

## 🔧 Technische Details

### SQLite-Tabellen

| Tabelle | Inhalt |
|---------|--------|
| `questions` | 280 Fragen mit Optionen, Lösungen, Erklärungen |
| `learning_attempts` | Alle Antworten mit Zeitstempel |
| `learning_sessions` | Tagesstatistiken |

### Fragen-Format (in SQLite)

```sql
id: sub_001
question: "Wie viele Hosts hat ein /24-Netzwerk?"
options: ["A) 254", "B) 256", "C) 512", "D) 1024"]
correct: A
explanation: "/24 = 8 Host-Bits = 2^8 - 2 = 254 Hosts"
category: IT-Grundlagen
difficulty: medium
```

## 📈 Beispiel-Statistik

```
==================================================
📊 WOCHENSTATISTIK - AP1 Training
==================================================

📊 Ergebnis:
   Gesamt: 21 Fragen
   ✅ Richtig: 17
   ❌ Falsch: 4
   📈 Quote: 81.0%

📚 Nach Themen:
   🟢 IT-Grundlagen: 5/6 (83%)
   🟢 Software-Entwicklung: 4/4 (100%)
   🟡 IT-Sicherheit: 3/5 (60%)

💡 Empfehlung: Mehr üben in IT-Sicherheit!
==================================================
```

## 🎓 Für wen ist das Skill?

- **IHK Fachinformatiker** (Systemintegration oder Anwendungsentwicklung)
- **AP1 Prüfungsvorbereitung**
- **Tägliches Lernen** in kleinen Portionen
- **Lückenanalyse** durch Statistiken

## ⚡ Keine Abhängigkeiten

- ✅ Nur Python 3 Standardbibliothek
- ✅ Keine pip-Installationen nötig
- ✅ Keine API-Keys
- ✅ Keine Internet-Verbindung für Fragen
- ✅ SQLite ist in Python integriert

## 🐛 Fehlerbehebung

### Datenbank nicht gefunden?

```bash
# Prüfe Pfad
ls -la skills/ap1-training-tracker/data/questions.db

# Sollte existieren und ~500KB groß sein
```

### Keine Fragen vorhanden?

```bash
# Datenbank prüfen
sqlite3 skills/ap1-training-tracker/data/questions.db \
  "SELECT COUNT(*) FROM questions;"

# Sollte 280 zurückgeben
```

## 📝 Changelog

### v2.0 (aktuell)
- 280 Fragen (vorher 30)
- 50 Subnetting-Fragen hinzugefügt
- SQLite-Struktur statt Python-Liste
- Eigene Datenbank im Skill-Ordner
- Keine externen Abhängigkeiten

### v1.0
- Erste Version mit 30 Fragen

## 👨‍🏫 Tipps für das Lernen

1. **Täglich üben** → 3 Fragen dauern nur 2-3 Minuten
2. **Fehler analysieren** → Erklärungen lesen
3. **Schwächen identifizieren** → Statistik nutzen
4. **Subnetting wiederholen** → 50 Fragen dafür bereit
5. **Vor der Prüfung** → `--stats-all` für Gesamtüberblick

## 📞 Support

Bei Fragen oder Problemen einfach fragen!

---

*Viel Erfolg bei der AP1-Prüfung!* 🎓🎩
