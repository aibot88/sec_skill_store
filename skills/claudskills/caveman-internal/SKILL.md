---
name: caveman-internal
description: >
  Caveman compresso solo per reasoning interno e prompt verso subagent.
  Output finale all'utente resta in italiano naturale (TTS-friendly,
  mobile-friendly). Risparmia token sull'orchestratore senza degradare la
  user experience. Auto-attivo per agenti notch/telegram insieme a orchestrator.
---

# Caveman Internal

## Cosa significa "internal"

A differenza di `caveman-compress` che riscrive file di memoria, e del caveman
"full" che comprime anche l'output, qui il taglio è chirurgico:

- **Reasoning silenzioso** (i tuoi monologhi interni) → caveman
- **Prompt ai subagent via `Agent`** → caveman
- **Tool descriptions/parametri** → invariati
- **Risposta finale all'utente** → italiano pieno, naturale, leggibile

## Regole caveman per la parte interna

- Niente articoli (il/la/un/una/lo/gli) salvo che cambino il senso
- Niente congiunzioni di cortesia ("inoltre", "quindi", "perciò")
- Imperativo > descrittivo: "trova X, ritorna Y" non "potresti cercare X e poi…"
- Numeri e path > parole: `notch.ts:47` non "il file notch alla riga 47"
- Nessuna intro/outro nei prompt subagent

## Perché l'output utente NO

Il notch usa TTS: caveman text suona innaturale e prosodia spezzata. Telegram
mobile: messaggi caveman sono faticosi da leggere oltre 2-3 righe. Il guadagno
in token è sull'orchestratore (che gestisce sessioni lunghe), non sui singoli
output utente che sono già brevi per design.

## Esempio

**Reasoning interno (caveman):**
> ok cerca file. spawn Explore. brief: trova caller di `speakToFile`. ritorna
> path:line. parallelo con altro Explore per config.yaml. sintesi unica.

**Prompt al subagent (caveman):**
> grep `speakToFile` in router/src/. ritorna path:line, no excerpt. max 10 risultati.

**Risposta all'utente (italiano normale):**
> `speakToFile` viene chiamato in 2 punti: `notch.ts:76` e `dashboard/api.ts:142`.
> Vuoi che proceda con la modifica solo nel notch?

## Attivazione

Skill caricato di default per:
- agente `notch` (canale voice)
- agente `jarvis` quando invocato da Telegram/WhatsApp

Sulla CLI normale resta opt-in (utente può chiamare `/caveman` per il caveman
full che comprime anche l'output).
