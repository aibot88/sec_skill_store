---
name: dictation-cleanup
description: Transform raw speech-to-text dictation into polished prose while preserving the author's natural voice
author: Writing Secrets
version: 1.0.0
triggers:
  - "dictation"
  - "clean up dictation"
  - "speech to text"
  - "transcription cleanup"
  - "dictated text"
  - "voice draft"
  - "raw transcript"
  - "fix dictation"
permissions:
  - file:read
  - file:write
---

# Dictation Cleanup — Premium Skill

Transform messy speech-to-text output into polished, publish-ready prose. Built for authors who dictate their drafts — because dictation is the fastest way to write, but cleaning it up shouldn't take longer than typing it would have.

## The Problem

Speech-to-text gives you something like this:
```
so she walked into the room and um the light was kind of flickering you know
like one of those old fluorescent lights and she could smell something weird
like copper maybe or no more like rust and old pennies and she knew comma she
just knew that something was wrong period new paragraph Marcus was sitting in
the corner but he wasn't really sitting he was more like slumped and his eyes
were open but they weren't seeing anything quote hello question mark close
quote she whispered but even as she said it she knew he wasn't going to answer
```

## What Dictation Cleanup Does

Transforms that into:

```
She walked into the room. The fluorescent light flickered overhead — one of
those old tubes that never quite dies — and something metallic hung in the air.
Copper. No — rust and old pennies.

She knew. She just knew something was wrong.

Marcus sat in the corner. Slumped, really, more than sitting. His eyes were
open but they weren't seeing anything.

"Hello?" she whispered.

Even as she said it, she knew he wasn't going to answer.
```

## Cleanup Levels

### Level 1: Basic (Fastest)
- Fix punctuation (spoken "comma", "period", "new paragraph")
- Remove filler words ("um", "uh", "like", "you know", "so")
- Capitalize and format properly
- Fix obvious speech-to-text errors
- Separate paragraphs

### Level 2: Standard (Recommended)
Everything in Level 1, plus:
- Fix run-on sentences (dictation tends to create them)
- Convert spoken dialogue markers to proper formatting
- Remove verbal tics and repetitions
- Smooth out awkward phrasing while keeping author voice
- Apply Voice Profile for consistency

### Level 3: Deep Polish
Everything in Level 2, plus:
- Restructure rambling passages into tight prose
- Strengthen verb choices (spoken drafts tend toward weak verbs)
- Add sensory detail where dictation was vague
- Balance sentence length variety
- Scene-level pacing adjustment

## Smart Features

### Voice Profile Integration
- Learns YOUR dictation patterns over time
- Knows which "mistakes" are actually your style
- Preserves your natural sentence rhythms
- Adapts to your genre conventions

### Dialogue Detection
- Automatically identifies when you're dictating dialogue vs. narration
- Formats dialogue with proper quotation marks and attribution
- Handles "he said / she said" patterns naturally
- Recognizes character voice shifts

### Dictation Command Recognition
Understands common dictation commands:
- "new paragraph" / "new line" / "break"
- "open quote" / "close quote"
- "comma" / "period" / "exclamation" / "question mark"
- "em dash" / "ellipsis"
- "scratch that" / "delete last sentence"
- "all caps" / "italics" (when supported by STT)
- "note to self" — strips author notes from output

### Batch Processing
- Clean up an entire chapter at once
- Process multiple dictation sessions into a single coherent chapter
- Merge dictation fragments in order
- Track word count before/after (your dictation words → final prose words)

## Statistics & Tracking

After each cleanup:
```
Dictation Cleanup Report
────────────────────────
Raw dictation:    2,847 words
After cleanup:    2,134 words (25% trimmed)
Filler removed:   187 instances
Sentences fixed:  43 run-ons split
Dialogue blocks:  12 formatted
Paragraphs:       8 raw → 23 formatted

Dictation speed:  ~2,800 words/hour (estimated)
Equivalent typing: ~1,400 words/hour
Time saved:       ~45 minutes
```

## Workflow Integration

Works seamlessly with other AuthorClaw skills:
- **Ghostwriter Pro** — Clean dictation → Deep Write polish
- **Book Bible** — Auto-check character names and locations after cleanup
- **Voice Profile** — Cleanup adapts to your established voice markers

## Commands
- `clean dictation` — Process pasted dictation text (Level 2 by default)
- `clean dictation [level 1/2/3]` — Specify cleanup intensity
- `clean dictation file [path]` — Process a saved dictation file
- `batch dictation [folder]` — Clean all dictation files in a folder
- `dictation stats` — Show your dictation patterns and cleanup history
- `set dictation commands` — Customize which spoken commands to recognize
