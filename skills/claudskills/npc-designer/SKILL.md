---
name: npc-designer
description: Create memorable Dungeons & Dragons NPCs for 5e campaigns, from quick social contacts to villains, patrons, witnesses, rivals, and combat-ready named characters. Use when a DM needs roleplay hooks, table behavior, secrets, leverage, and optional 2024-first mechanics.
compatibility: Offline-friendly. Markdown only. Default to English output.
metadata:
  domain: dnd
  editions: 2024 primary; 2014 fallback
  output: npc-dossier
---

# NPC Designer

Use this skill when the user wants a named character, a recurring ally, a faction contact, a merchant, a villain, a witness, a guide, or a socially rich encounter anchor.

## Core operating rules

- Use the Sage persona only for discussion. Final NPC material must fit the requested fiction, not the robotic analysis voice.
- Default to a **DM-ready dossier**, not a novel. Make the NPC easy to improvise at the table.
- Prefer **D&D 2024** wording for any mechanics. Use **2014** only when requested or required, marked with `⚠️`.
- Default to English for descriptive and roleplaying text.
- Correct grammar, punctuation, and spelling while preserving the NPC's intended voice and characterization.
- Keep names, terminology, and formatting consistent unless the user explicitly changes them.
- Remove strikethrough text, editor comments, meta notes, and unresolved suggestions from the final dossier.
- If the user does not ask for combat mechanics, do not force a full statblock.

## Choose the right depth

### 1. Quick NPC
Use for shopkeepers, guides, witnesses, one-scene contacts.

Include:
- Name and role
- Look and sensory impression
- Demeanor and table voice
- Goal, fear, leverage, and secret
- One useful scene hook

### 2. Spotlight NPC
Use for rivals, patrons, suspects, lieutenants, and recurring cast.

Include everything from Quick NPC, plus:
- Relationships and faction ties
- What they want from the party
- Escalation behavior if ignored or crossed
- A short lore or rumor block
- One or more scene uses

### 3. Combat-ready NPC
Use when the NPC can join battle or lead encounters.

Include a combat package scaled to the request:
- A concise stat profile or full statblock
- Signature combat pattern
- DM Handbook style guidance from `references/NPC-FRAME.md`

## Workflow

1. Identify role, social function, campaign tier, and desired tone.
2. Decide the minimum useful depth.
3. Build distinct play signals: voice, body language, motive, pressure point, and secret.
4. Add table value: why the NPC matters now, how they complicate the story, and what changes if the party helps or opposes them.
5. If combat is requested, attach clean 5e mechanics without overwhelming the dossier.
6. If the NPC includes rules text, use exact 5e terms, explicit conditional phrasing, exact measurements, and the required saving throw format below.

  ```
  **Ability.** *Saving Throw Type:* **DC X**, targets/area. *Failure:* effect. *Success:* effect. *Additional Clauses (if any):* further consequences.
  ```

  Do not deviate from this phrasing, line breaks, or punctuation.

## Default output shape

Use or adapt this order:

1. `## [NPC Name]`
2. Role and one-line summary
3. Appearance and presence
4. Personality and voice
5. Motivation, fear, leverage, secret
6. Relationships and factions
7. How to use at the table
8. Optional combat profile or statblock reference

## References

- NPC structure and DM usage cues: `references/NPC-FRAME.md`
