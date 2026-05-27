---
name: deep-voice-analysis
description: Advanced 47-marker voice analysis engine — analyzes your writing to build a comprehensive Voice Profile for AuthorClaw
author: Writing Secrets
version: 1.0.0
triggers:
  - "analyze my voice"
  - "learn my style"
  - "deep voice analysis"
  - "voice analysis"
  - "writing dna"
  - "clone my style"
  - "study my writing"
permissions:
  - file:read
  - file:write
---

# Deep Voice Analysis — Premium Skill

Advanced writing voice analysis that goes far beyond the free style-clone skill. Analyzes your writing across 47 markers to create a forensic-level Voice Profile.

## What Makes This Different From the Free Style-Clone Skill

The free `style-clone` skill does a basic voice analysis (~10 markers). This premium skill runs a **47-marker deep analysis** that captures the invisible patterns that make YOUR writing yours — the kind of patterns that fool AI detectors because they encode genuine human writing habits.

## The 47 Markers

### Rhythm Markers (12)
1. Average sentence length (words)
2. Sentence length variance (burstiness)
3. Short sentence frequency (1-5 words)
4. Medium sentence frequency (6-15 words)
5. Long sentence frequency (16-25 words)
6. Very long sentence frequency (26+)
7. Paragraph average length (sentences)
8. Paragraph length variance
9. Scene-opening sentence length pattern
10. Chapter-opening sentence length pattern
11. Dialogue line average length
12. Action beat average length

### Vocabulary Markers (10)
13. Vocabulary richness (unique/total word ratio)
14. Perplexity score (word unpredictability)
15. Top 20 signature words (words you overuse — in a good way)
16. Top 10 avoided words (words you never use)
17. Formality level (casual ↔ academic)
18. Jargon/domain-specific vocabulary
19. Curse word frequency and type
20. Sensory word distribution (sight/sound/touch/smell/taste)
21. Emotional vocabulary range
22. Abstract vs. concrete word ratio

### Structural Markers (8)
23. Narrative distance (close/medium/distant POV)
24. Scene-to-sequel ratio
25. Dialogue-to-narrative ratio
26. Description density per scene
27. Flashback/memory frequency
28. Transition style (hard cuts vs. smooth)
29. Chapter hook style (question, action, dialogue, mystery)
30. White space usage (single-line paragraphs as emphasis)

### Dialogue Markers (7)
31. Tag preference (said/asked vs. creative tags)
32. Action beat vs. tag ratio
33. Average dialogue line length
34. Subtext level (direct ↔ heavily implied)
35. Interruption frequency
36. Character voice differentiation score
37. Monologue vs. rapid exchange ratio

### Punctuation & Mechanics (5)
38. Em dash frequency
39. Semicolon frequency
40. Ellipsis frequency
41. Exclamation mark frequency
42. Parenthetical frequency

### Voice & Tone (5)
43. Humor type (dry, sarcastic, physical, dark, witty, none)
44. Humor frequency
45. Emotional register style (body-first, thought-first, action-first)
46. Metaphor/simile density
47. Overall humanness score (AI-detection bypass potential)

## Analysis Process

1. **Intake**: Author provides 5,000+ words (ideal: 20,000+). Multiple samples across scenes/chapters is best.
2. **Tokenize**: Break text into sentences, paragraphs, scenes, dialogue blocks.
3. **Measure**: Calculate all 47 markers with statistical confidence.
4. **Compare**: Benchmark against genre averages to identify what's distinctive.
5. **Generate**: Create the Voice Profile markdown file.
6. **Validate**: Show the author their profile and ask "does this sound like you?"

## Output: Enhanced Voice Profile

Saved to `workspace/soul/VOICE-PROFILE.md` with all 47 markers organized into sections that AuthorClaw's Soul system reads on every interaction.

```markdown
# Voice Profile — Deep Analysis (47 Markers)
## Generated: [date] | Sample size: [N] words

## Humanness Score: [0-100]

## Rhythm
- Avg sentence: [N] words | Variance: [N] (burstiness)
- Distribution: [%] short / [%] medium / [%] long / [%] very long
- Paragraphs: [N] sentences avg
- Openers: [pattern description]

## Vocabulary
- Richness: [score] | Perplexity: [score] | Formality: [level]
- SIGNATURE WORDS (use naturally): [list]
- NEVER USE: [anti-AI words list]
- Sensory bias: [primary sense]

## Structure
- Narrative distance: [level]
- Dialogue ratio: [%] of text
- Description density: [level]
- Chapter hooks: [dominant style]

## Dialogue
- Tags: [preference] | Beats: [frequency]
- Avg line: [N] words | Subtext: [level]
- Voice differentiation: [score]

## Mechanics
- Em dashes: [freq] | Semicolons: [freq]
- Ellipsis: [freq] | Exclamation: [freq]

## Voice
- Humor: [type] at [frequency]
- Emotional style: [body/thought/action]-first
- Metaphor density: [level]

## RULES FOR AI
When writing as this author:
1. Follow the sentence distribution above (this is critical for humanness)
2. Use signature words naturally — don't force them but let them appear
3. NEVER use the avoided words list
4. Match the punctuation profile
5. Keep the narrative distance at [level]
6. Apply the [type] humor at appropriate moments
7. Lead with [body/thought/action] for emotional moments
8. Maintain [level] metaphor density — no more, no less
```

## Commands
- `deep voice analysis` or `analyze my voice deeply` — Start the full 47-marker analysis
- `show voice profile` — Display the current enhanced profile
- `voice check [text]` — Score new text against all 47 markers
- `voice report` — Generate a detailed report comparing recent writing to the profile
- `update voice profile from [text]` — Refine the profile with new sample data
