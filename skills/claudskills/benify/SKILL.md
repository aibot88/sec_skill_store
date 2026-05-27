---
name: benify
description: Transform text into Ben Church's authentic blog writing voice. Use when the user asks to "benify", "write like Ben", "rewrite in Ben's voice", "make this sound like me", "apply my voice", "convert to my writing style", or needs text transformed into Ben's distinctive conversational-but-substantive blog voice.
allowed-tools: Read, Glob, Grep
---

# Benify

Transform any text into Ben Church's authentic blog voice.

## Process

1. **Load the reference materials.** Read the following files from this project:
   - `.claude/skills/guide/references/writing-like-ben.md` (voice calibration)
   - `.claude/skills/guide/references/nonos.md` (anti-patterns)
   - `.claude/skills/guide/references/selected-examples.md` (calibration examples)
   - `.claude/skills/guide/references/structure-and-grammar.md` (formatting standards)

2. **Read the input.** The user will provide text inline, as a file path, or as `$ARGUMENTS`. Understand the core message, the intended audience, and the content type (tutorial, opinion, thought piece, process/management).

3. **Deslopify first.** Before applying voice, remove all AI slop patterns identified in nonos.md. Clean the text to neutral human-sounding prose. This prevents slop from leaking through the voice transformation.

4. **Determine the writing mode.** Based on the content type, select the appropriate voice register from writing-like-ben.md:
   - **Technical Tutorial** — most structured, clear steps, "By the end" setup, personality in asides
   - **Opinion/Essay** — more flowing, personal anecdotes, bold claims, calls to action
   - **Thought Piece** — philosophical, rhetorical questions, building to a point
   - **Management/Process** — framework-oriented, numbered principles, templates

5. **Apply Ben's voice.** Transform the text following the patterns in writing-like-ben.md:
   - Rewrite the opening to hook immediately (bold claim, controversial statement, or direct problem statement — no throat-clearing)
   - Restructure to follow Why → What → How progression where appropriate
   - Mix short punchy sentences with longer nuanced ones
   - Add bold for key concepts on first introduction
   - Use headers as functional signposts
   - Add conversational asides and parenthetical personality where natural
   - Apply genuine enthusiasm only where the content warrants it
   - Write in first person, conversational tone
   - Use US English and contractions

6. **Quality check.** Compare the output against selected-examples.md. Ask:
   - Does this sound like it came from the same person who wrote those posts?
   - Is the enthusiasm genuine or performed?
   - Are the Ben-isms (Ok so, Let's, Essentially, bold concepts) used naturally and sparingly, not crammed in?
   - Would Ben actually say this, or does it feel like a caricature?

7. **Present the result.** Output:
   - The full rewritten text
   - A brief summary of the key transformations made (3-5 bullet points)

## Rules

- **Don't caricature.** Adding "Ok so" to the beginning and emoji everywhere is not benifying. Use voice markers naturally and sparingly.
- **Don't lose technical accuracy.** Voice transformation must never change the meaning of technical content.
- **Don't force personality where clarity matters.** In code explanations and step-by-step instructions, clarity beats personality.
- **Don't over-benify.** Not every sentence needs a personality marker. Most sentences should just be clear, direct, and natural.
- **Match the content's weight.** A tutorial about setting up a project is lighter than a post about surveillance capitalism. Ben adjusts his tone to the subject.
- **Preserve the reader's trust.** Ben is honest about limits. Don't make claims the original text can't support. Add "I've found" or "in my experience" qualifiers where appropriate.
