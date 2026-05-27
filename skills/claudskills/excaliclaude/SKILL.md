---
name: excalicl4ude
description: >
  Sessione interattiva su canvas Excalidraw bidirezionale. Usa questa skill
  quando l'utente vuole discutere visivamente di un'idea, fare brainstorming
  su un canvas, disegnare insieme un'architettura, creare diagrammi
  interattivamente, o collaborare visivamente su qualsiasi concetto. Attiva
  anche quando l'utente dice "apri un canvas", "disegna", "vediamolo
  visivamente", "facciamo uno sketch", "discutiamone su un canvas", "fammi
  vedere", o qualsiasi variante che implichi collaborazione visiva.
---

# ExcaliClaude — Collaborazione Visiva Interattiva

Sei in una sessione di collaborazione visiva con l'umano su un canvas
Excalidraw condiviso. Puoi disegnare, annotare, e comunicare sia visivamente
(sul canvas) sia testualmente (nella sidebar Claude del canvas).

## Protocollo di Interazione

Leggi `references/interaction-protocol.md` per il protocollo completo e
`references/canvas-patterns.md` per i pattern di diagrammi comuni.

### Flusso Base

1. **Apertura** — Quando l'utente chiede di lavorare visivamente, usa
   `open_canvas` con un titolo descrittivo. Si apre una finestra nativa con
   Excalidraw + la sidebar Claude integrata.

2. **Annuncio + Attesa** — Subito dopo l'apertura, usa `wait_for_human`
   con il parametro `message` per presentare la sessione E attendere il
   segnale in una singola chiamata. Esempio:
   ```
   wait_for_human({ message: "Canvas pronto! Disegna la tua idea, poi
   clicca '👀 Claude, guarda!' quando vuoi il mio feedback." })
   ```
   Il tool è **bloccante** (long-poll) e ritorna con summary del canvas +
   eventuale messaggio dell'umano.

3. **Analisi** — Quando ricevi il segnale, analizza lo stato del canvas
   dalla risposta di `wait_for_human` (summary testuale, eventuale
   screenshot, `changed_elements`).

4. **Risposta + Attesa** — Agisci visivamente (`batch_create_elements`,
   `annotate`, `update_element`), poi **termina SEMPRE** con
   `wait_for_human` con `message` che spiega cosa hai fatto. Esempio:
   ```
   wait_for_human({ message: "Ho aggiunto il diagramma dell'architettura.
   Dimmi se vuoi modifiche!" })
   ```

5. **Iterazione** — Torna al punto 3 fino a conclusione.

6. **Salvataggio** — Alla fine, usa `save_session` per salvare il file
   `.excalidraw` nella directory del progetto.

**IMPORTANTE**: usa SEMPRE `wait_for_human` con `message` come ultimo
tool del turno. Non usare `send_message_to_canvas` separatamente — il
parametro `message` di `wait_for_human` lo sostituisce, risparmiando una
chiamata tool.

## Regole Importanti

- **Non monopolizzare il canvas.** Aspetta sempre il segnale dell'umano
  prima di agire, a meno che non ti venga esplicitamente chiesto di
  procedere in autonomia.

- **Comunica prima di agire.** Usa il parametro `message` di
  `wait_for_human` per spiegare cosa hai fatto o cosa farai. L'umano deve
  sapere perché il canvas cambia.

- **Annotazioni, non sovrascritture.** Usa `annotate` con
  `target_element_id` per commentare il lavoro dell'umano senza sovrascriverlo.

- **Differenzia visivamente** i tuoi elementi: usa `#7C5CFC` come
  `strokeColor` e `rgba(124, 92, 252, 0.06)` come `backgroundColor` per le
  tue aggiunte. Lascia colori neutri (stroke `#1e1e1e`) per gli elementi
  dell'umano.

- **Qualità visiva.** Prima di disegnare un diagramma complesso, chiama
  `read_diagram_guide` per caricare la palette semantica e i template di
  layout. Usa `roughness: 0`, `fillStyle: "solid"`, `fontFamily: 2` e
  `roundness: { type: 3 }` per diagrammi tecnici professionali. Scegli i
  colori dalla tabella semantica (Frontend=blu, Backend=viola, DB=verde, ecc.).

- **Token efficiency.** Usa `describe_scene` come default (testo compatto).
  `get_canvas_screenshot` solo quando serve davvero il layout visivo.

- **Salva presto, salva spesso.** Usa `save_session` a milestone importanti
  per evitare perdita di lavoro.

## Tool di Sessione ExcaliClaude

| Tool                     | Quando usarlo                                |
| ------------------------ | -------------------------------------------- |
| `open_canvas`            | Inizio sessione                              |
| `wait_for_human`         | **SEMPRE come ultimo tool del turno** — con `message` per comunicare nella sidebar + attendere il segnale |
| `annotate`               | Commentare un elemento specifico dell'umano  |
| `save_session`           | Salvare come file `.excalidraw`              |
| `get_human_changes`      | Vedere cosa ha modificato l'umano            |
| `list_sessions`          | Se ci sono più canvas aperti                 |
| `close_canvas`           | Fine sessione (con `save: true`)             |

## Tool Excalidraw (dal fork upstream)

Tutti i 26 tool originali di mcp_excalidraw restano disponibili e ora
accettano un parametro `session_id` opzionale (default: sessione attiva):

- Elementi: `create_element`, `update_element`, `delete_element`,
  `get_element`, `batch_create_elements`, `duplicate_elements`,
  `query_elements`
- Layout: `align_elements`, `distribute_elements`, `group_elements`,
  `ungroup_elements`, `lock_elements`, `unlock_elements`
- Export/Import: `export_scene`, `import_scene`, `export_to_image`,
  `export_to_excalidraw_url`, `create_from_mermaid`
- Inspect: `describe_scene`, `get_canvas_screenshot`, `snapshot_scene`,
  `restore_snapshot`, `clear_canvas`, `set_viewport`, `read_diagram_guide`
