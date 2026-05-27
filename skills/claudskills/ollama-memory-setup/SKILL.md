---
name: ollama-memory-setup
description: "Sets up local semantic memory search for OpenClaw using Ollama + nomic-embed-text. Use when: (1) memory_search returns 'node-llama-cpp is missing' or 'Local embeddings unavailable' error, (2) user wants local/private embeddings without external API keys (OpenAI, Gemini, Voyage), (3) setting up memory search for the first time on macOS or Linux, (4) node-llama-cpp fails to install or build. Fixes the common node-llama-cpp installation failure by routing through Ollama's OpenAI-compatible embedding API instead of a local binary."
---

# Ollama Memory Setup

Enables semantic memory search in OpenClaw using Ollama locally — no API keys, no cloud, fully private.

## Wann verwenden?

Nutze diesen Skill wenn `memory_search` folgende Fehler wirft:

- `node-llama-cpp is missing (or failed to install)`
- `Local embeddings unavailable`
- `Cannot find package 'node-llama-cpp'`
- `optional dependency node-llama-cpp is missing`

Oder wenn du Embeddings lokal halten willst ohne externe APIs (OpenAI, Gemini, Voyage).

## Verwendung

### Automatisch (empfohlen)

```bash
# Setup-Script ausführen
bash ~/.openclaw/workspace/skills/ollama-memory-setup/scripts/setup.sh

# OpenClaw neu starten
openclaw gateway restart
```

### Manuell (Schritt für Schritt)

```bash
# 1. Ollama installieren
brew install ollama                    # macOS
curl -fsSL https://ollama.com/install.sh | sh  # Linux

# 2. Ollama starten (macOS: als Service, startet automatisch)
brew services start ollama

# 3. Embedding-Modell laden (~270MB, einmalig)
ollama pull nomic-embed-text

# 4. OpenClaw konfigurieren
openclaw config set agents.defaults.memorySearch.provider ollama
openclaw config set agents.defaults.memorySearch.model nomic-embed-text
openclaw config set agents.defaults.memorySearch.remote.baseUrl http://localhost:11434
openclaw config set agents.defaults.memorySearch.enabled true

# 5. Neu starten
openclaw gateway restart
```

## Aufstellen

Keine API-Keys nötig. Voraussetzungen:

- **macOS:** Homebrew installiert (`brew --version`)
- **Linux:** curl installiert, systemd empfohlen
- **Ollama Version:** >= 0.18.0
- **Speicher:** ~300MB für das nomic-embed-text Modell

## Verifizieren

Nach dem Neustart in einer frischen Session testen:

```
memory_search("test")
```

Erwartete Antwort enthält `"provider": "ollama"` — nicht `disabled: true`.

## Warum nomic-embed-text?

`nomic-embed-text` ist ein spezialisiertes Embedding-Modell (nicht für Chat):
- Klein (~270MB vs. mehrere GB für Chat-Modelle)
- Schnell (~50ms pro Anfrage auf moderner Hardware)
- Hohe Qualität für semantische Suche
- Kostenlos, Open Source (Apache 2.0)

Alternativer Modellname für ältere Ollama-Versionen: `nomic-embed-text:latest`

## Fehlersuche

Siehe `references/troubleshooting.md` für häufige Probleme wie:
- Ollama startet nicht
- memory_search bleibt deaktiviert nach Setup
- macOS: Ollama stoppt nach Neustart
- Linux: Systemd-Service einrichten
