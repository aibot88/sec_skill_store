---
name: reading-lens
description: Active-reading scaffolding for nonfiction books (EPUB). Parses an EPUB, generates a structured book analysis in the user's Obsidian vault at Read/{Book Name} ({Author})/, with 0. General.md as the book-level overview and one numbered markdown file per chapter containing pre-read brief, the user's own notes section, and post-read synthesis — all through configurable role lenses (e.g. PM, CEO, Entrepreneur). Six sub-skills — `reading-lens:setup` loads an EPUB with lens selection, `reading-lens:brief` generates a pre-read brief for a chapter, `reading-lens:synthesize` generates a post-read synthesis, `reading-lens:overview-redo` regenerates 0. General.md, `reading-lens:lenses` manages global lens presets, `reading-lens:to-notion` mirrors the book to Notion via MCP. Use whenever the user wants deep, structured book analysis, says "analyze this book", "read this book", "reading lens", "book analysis", "pre-read brief", "chapter synthesis", or references an EPUB path. Prefer this skill for any book-study workflow — even when the user doesn't say its name.
---

# Reading Lens

Active-reading scaffolding for nonfiction books. Given an EPUB, produce a structured set of markdown files in the user's Obsidian vault: book-level overview (`0. General.md`), per-chapter pre-read briefs (what to watch for), and per-chapter post-read syntheses (what it meant + contrarian takes + actionable experiments). The user takes their own notes in each chapter file — this skill is scaffolding, never a replacement for the user's own thinking.

## Why This Exists

Reading nonfiction passively leaks most of its value. This skill pre-frames each chapter so the reader knows what to watch for, then produces a synthesis with per-lens takeaways, a contrarian take (what the book overclaims), and concrete experiments worth running. Everything lands in Obsidian, wikilinked, so the vault accumulates into durable knowledge.

## Model & Thinking

- **Default model: Opus 4.7** (`claude-opus-4-7`). This skill does qualitative analysis — use the strongest reasoning model available. Check with `/model`, switch if needed.
- **Use extended thinking** (`<think>` / ultrathinking) for three steps specifically: (1) generating `0. General.md`, (2) generating a post-read synthesis, (3) generating a contrarian take. The quality bar is high — platitudes are a failure mode.

## Sub-commands

| Command | Purpose |
|---------|---------|
| `/reading-lens:setup <epub-path>` | Parse EPUB, resolve lenses, create book folder, generate `0. General.md`, AND generate pre-read briefs + post-read syntheses for every chapter |
| `/reading-lens:brief <N>` | Generate pre-read brief for chapter N (before reading) |
| `/reading-lens:synthesize <N>` | Generate post-read synthesis for chapter N (after reading) |
| `/reading-lens:overview-redo` | Regenerate `0. General.md` for the current book (lenses preserved) |
| `/reading-lens:lenses [action]` | Manage global lens presets: list / add / edit / remove |
| `/reading-lens:to-notion` | Mirror the current book to Notion via Notion MCP |
| `/reading-lens:help` | Show usage |

If the user's intent clearly matches a sub-command but they didn't type the exact syntax, run the matching sub-command. Don't stall on syntax pedantry.

## Configuration

Global settings live in `{SKILL_DIR}/config.yaml`. On first use, verify `vault_path` is set to a real directory — if it still says `/path/to/your/obsidian/vault`, abort and tell the user to edit it.

Config fields:
- `vault_path` — absolute path to the Obsidian vault (required)
- `books_folder` — subfolder name (default `Reads`)
- `global_lenses` — list of `{role, interests}` objects
- `notion_parent_url` — optional, for `:to-notion`

## Vault Structure

```
{vault_path}/{books_folder}/{Book Name} ({Author})/
├── 0. General.md                 # Book-level overview (the "orientation" file)
├── 1. {chapter 1 title}.md       # Chapter notes: brief | my notes | synthesis
├── 2. {chapter 2 title}.md
└── n. {chapter n title}.md
```

**Filename rules.** For both the book folder and chapter filenames, sanitize thus:
- Replace `:` with ` - ` (space-hyphen-space) — preserves readability in titles like `Start: A Parable` → `Start - A Parable`
- Remove `/ \ * ? " < > |`
- Collapse multiple spaces to one, trim leading/trailing whitespace
- Do NOT slugify — preserve capitalization and spaces (this is Obsidian, not URLs)

**Examples.**
- Book `The Lean Startup` by `Eric Ries` → folder `The Lean Startup (Eric Ries)`
- Chapter `Start: A Parable` → file `1. Start - A Parable.md`
- Chapter `What/When/How` → file `3. WhatWhenHow.md` (slashes removed)

## Lens Selection Flow

Executed at the start of every `/reading-lens:setup` after EPUB parsing.

1. Read `global_lenses` from `config.yaml`.
2. If the list is empty: tell the user "No global lenses configured yet. What lenses should I use for this book?" Ask for `role + interests` pairs. Offer to save them globally after the user defines them.
3. If the list is non-empty: present the globals and ask:

   > You have {N} global lenses:
   >   1. {Role 1} — {interests}
   >   2. {Role 2} — {interests}
   >   ...
   >
   > For **{Book Title}**, do you want to:
   >   (a) Use all global lenses
   >   (b) Choose a subset of globals
   >   (c) Define new lenses just for this book (ignoring globals)
   >   (d) Combine a subset of globals + new book-specific lenses

4. Based on the answer, resolve the final lens set. Confirm back to the user before proceeding: "Using these lenses for this book: [list]. Continue?"
5. Store chosen lenses in the book's `0. General.md` frontmatter under `lenses:`. These become the book's frozen lens set — they override globals for this book going forward. Changing globals later does not rewrite this book.

## Update-Don't-Delete Safety

Before writing any file, check if it already exists. Never overwrite silently. Specific rules:

**On `:setup` when the book folder already exists:**

1. List what's there: `0. General.md`, which chapter files, and for each chapter file read the frontmatter to report `brief_generated` and `synthesis_generated` state.
2. Present status and ask:
   > Book already exists at `{path}`. Current state:
   >   - 0. General.md  [generated {date}]
   >   - 1. {title}     [✓ brief, ✓ synthesis]
   >   - 2. {title}     [✓ brief, — no synthesis]
   >   - 3. {title}     [— untouched]
   >
   > What would you like to do?
   >   (a) Skip — leave everything as-is
   >   (b) Fill missing pieces only (generate briefs/syntheses for chapters that lack them)
   >   (c) Regenerate `0. General.md` only (keeps per-book lenses + chapter files)
   >   (d) Add chapters that aren't in the vault yet (EPUB may have more than the folder)
   >   (e) Review and decide file-by-file

3. Never delete files. Never overwrite `## ✍️ My notes` sections (the user's own writing).

**On `:brief N` or `:synthesize N` when the section is already filled:**

- Show the user the current content of `## Pre-read brief` (or `## Post-read synthesis`), say when it was generated, and ask: "Overwrite, keep, or append?" Default to "keep" on any ambiguous response.
- If the user chooses "append", add the new version under a `### Re-generated {ISO-date}` subheader so both versions are preserved.

**On `:overview-redo`:**

- Show current `0. General.md` summary (first paragraph + lens list). Ask: "Regenerate `0. General.md`? Per-book lenses will be preserved. Overwrite? (y/n)". Only proceed on explicit yes.

## Workflow

### `/reading-lens:setup <epub-path>`

1. **Validate.** Check the path exists and ends in `.epub`. Abort with a clear error if not.
2. **Read config.** Load `config.yaml` from the skill directory. If `vault_path` is the default placeholder or not a directory, abort with: "Edit `{SKILL_DIR}/config.yaml` first — set `vault_path`."
3. **Parse EPUB.** Run `python3 {SKILL_DIR}/scripts/parse_epub.py <epub-path>` and capture JSON. On error, surface stderr to the user.
4. **Build book folder path.** `{vault_path}/{books_folder}/{Book Name} ({Author})/`. Sanitize as per filename rules.
5. **Check for existing book.** If the folder exists, run the Update-Don't-Delete flow above.
6. **Resolve lenses.** Run the Lens Selection Flow above.
7. **Detect language for this book.** Check the user's setup invocation message for a language directive (e.g., "do it in Turkish", "yap bunu Türkçe", "auf Deutsch"). If detected, set `language: <code>` for this book (e.g., `tr`, `de`). Default: `en`. Confirm the detected language back to the user before proceeding: *"I'll generate this book's analysis in {Turkish}. Confirm?"* Wait for confirmation, then continue.
8. **Create folder + cache.** Create the book folder. Save parsed EPUB JSON to `{SKILL_DIR}/.cache/{book-folder-name}.json` for fast re-use by `:brief` and `:synthesize`.
9. **Generate `0. General.md` AND extract book-level context for subagents.** Use extended thinking. Source material: title, author, TOC (all chapter titles in order), and sample text (first 6000 chars of chapter 1 + first 6000 chars of chapter 2). Fill the **Book Overview Template** below. Before returning, hold onto three transportable artifacts for step 12 to hand to subagents:
    - **Book thesis** — the core argument in one sentence
    - **Author-voice register** — 2–3 sentences characterizing the author's voice (see close-reading extraction step 4)
    - **Frozen lens list** — as already resolved in step 6
10. **Create chapter stubs.** For each chapter, write a file with frontmatter + the three empty section headers (Pre-read brief, My notes, Post-read synthesis). Include `synthesis_has_notes: false` in the frontmatter.
11. **Warn the user about duration.** Print: "Generating pre-read briefs + post-read syntheses for all {N} chapters in parallel via subagents. This typically takes 5–15 minutes — longer for books with very long chapters or many chapters. Syntheses are generated WITHOUT your reading notes (you haven't read yet) — after you read a chapter and take notes in `## ✍️ My notes`, re-run `/reading-lens:synthesize <N>` to upgrade that chapter's synthesis with your framing." Do not block on a confirmation — proceed.
12. **Generate pre-read briefs AND post-read syntheses for all chapters — in parallel via subagents.** Use Claude Code's `Task` tool to dispatch multiple subagents concurrently. **Batching rule:** aim for each subagent to receive no more than ~100,000 characters of chapter text total (to stay well under subagent context limits). A reasonable default: 4–8 subagents for a 32-chapter book (e.g., 32 chapters → 8 subagents handling 4 chapters each; 16 chapters → 4 subagents handling 4 chapters each; <8 chapters → one subagent). If the book has unusually long chapters (>6k words), drop to 2–3 chapters per subagent. Each subagent receives, in its prompt:

    - Its assigned chapters' titles, numbers, and full text (inline, pulled from the cached EPUB JSON)
    - The book's **author-voice register** extracted in step 9
    - The book's **thesis** extracted in step 9
    - The **frozen lens list** from step 6
    - The book's `language` (from step 7) — subagent generates output in this language
    - The full **Pre-read Brief** and **Post-read Synthesis** templates from the Templates section above
    - The **Close-Reading Extraction Discipline** instructions
    - A direct write mandate — each subagent writes the completed brief and synthesis straight into the corresponding chapter file using the Edit tool

    The orchestrator (main agent) issues all subagent `Task` calls in a **single message** to trigger concurrent execution. See `superpowers:dispatching-parallel-agents` for the fan-out pattern.

    Each subagent, for each assigned chapter:
    1. Runs the close-reading extraction pass (thesis, anchor phrases, defined terms, voice register refinement, structural role)
    2. Fills the Pre-read Brief template
    3. Fills the Post-read Synthesis template, prepending the `> [!info] Generated at setup — no reader notes yet` callout
    4. Updates the chapter file's frontmatter: `brief_generated: <ISO-date>`, `synthesis_generated: <ISO-date>`, `synthesis_has_notes: false`, `status: synthesized`
    5. Returns a short status line: chapter number, success/failure, any warnings

    After all subagents return, the orchestrator verifies every chapter file has both sections filled and reports aggregate completion.

13. **Report.** Tell the user: book title, author, N chapters parsed, briefs generated, syntheses generated (all flagged `synthesis_has_notes: false`), full folder path. Recommend: "Start with chapter 1. After each chapter, fill `## ✍️ My notes` then re-run `/reading-lens:synthesize N` to upgrade that chapter's synthesis."

### `/reading-lens:brief <N>`

1. **Resolve current book.** Find the most recently modified `0. General.md` under `{vault_path}/{books_folder}/`. If multiple books have been touched recently, ask which one.
2. **Read language from `0. General.md` frontmatter.** Generate output in that language. Preserve author-voice register across translation. **Fallback:** if the `language:` field is missing (pre-change book), default to `en` and proceed — don't prompt the user unless they asked for a language switch in their invocation.
3. **Load chapter N.** Read cached EPUB JSON from `{SKILL_DIR}/.cache/`. If missing, tell the user to run `:setup` again.
4. **Check for existing brief.** If `## Pre-read brief` in the chapter file already has content, run the overwrite flow.
5. **Generate brief.** Using the chapter text (truncate to 40000 chars if longer) and the book's per-book lenses (from `0. General.md` frontmatter), produce the **Pre-read Brief** matching the template below.
6. **Write.** Replace the content under `## Pre-read brief` (or append per user choice). Update frontmatter: `brief_generated: <ISO-date>`, `status: briefed`.
7. **Report.** Print a 3-line summary and the path to the chapter file.

### `/reading-lens:synthesize <N>`

1. **Resolve current book.** Same as `:brief`.
2. **Read language from `0. General.md` frontmatter.** Generate output in that language. Preserve author-voice register across translation. **Fallback:** if the `language:` field is missing (pre-change book), default to `en` and proceed.
3. **Load chapter N text** and read the user's content from `## ✍️ My notes` section if present.
4. **Check for existing synthesis.** If `## Post-read synthesis` is filled:
   - If frontmatter says `synthesis_has_notes: false` AND the user has written real content under `## ✍️ My notes` (more than just the placeholder `*(take your notes...)*`), offer a notes-aware upgrade: "Current synthesis was generated at setup from chapter text only. You've since written notes — upgrade the synthesis to weave them in? (y/n)". On yes: overwrite the synthesis, remove the setup `> [!info]` callout, set `synthesis_has_notes: true`, regenerate using notes.
   - Otherwise, run the standard overwrite flow (keep/overwrite/append).
5. **Generate synthesis.** USE EXTENDED THINKING. If `## ✍️ My notes` has real content, reference it ("you noted X — this connects to..."). Produce the **Post-read Synthesis** matching the template below.
6. **Write.** Replace the content under `## Post-read synthesis`. Update frontmatter: `synthesis_generated: <ISO-date>`, `synthesis_has_notes: <true if notes were used, else false>`, `status: synthesized`.
7. **Report.** Print a 3-line summary + flashcard count + path + whether this was a notes-aware generation.

### `/reading-lens:overview-redo`

1. Resolve current book.
2. **Detect language override.** If the user's invocation includes a new language directive, update the `language:` field in frontmatter. Otherwise preserve the existing value. **If the field is missing entirely** (pre-change book), insert `language: en` as part of the regenerated frontmatter unless a new directive says otherwise.
3. Run overwrite flow for `0. General.md`.
4. Preserve existing per-book lenses (from current frontmatter).
5. Use extended thinking. Regenerate the overview with the same source material as setup (TOC + sample from first two chapters).
6. Write, report.

### `/reading-lens:lenses [action]`

Manage `global_lenses` in `config.yaml`.

- `/reading-lens:lenses` or `/reading-lens:lenses list` → print current globals
- `/reading-lens:lenses add` → prompt for `role` + `interests`, append to config
- `/reading-lens:lenses edit <role>` → show current values, prompt for new
- `/reading-lens:lenses remove <role>` → confirm, then remove
- `/reading-lens:lenses reset` → confirm, replace with built-in defaults (PM / CEO / Entrepreneur)

Edit `config.yaml` in place. Preserve comments and formatting.

### `/reading-lens:to-notion`

1. Confirm Notion MCP is connected. If not, tell the user to enable it in settings.
2. Resolve current book.
3. Use `notion_parent_url` from config, or ask the user for the parent page.
4. Create a parent page from `0. General.md` (strip Obsidian wikilinks, convert to plain references).
5. Create one subpage per chapter file.
6. Report Notion URLs.

### `/reading-lens:help`

Print the sub-commands table, vault structure, where to edit config, how to manage lenses, and model recommendation (Opus 4.7).

## Writing Voice

Every section of every brief and synthesis is written as the author speaking directly to the reader. First person throughout. Warm. Flowing. Complexity where earned, not performative.

- **Pre-read framing** — the author is about to walk the reader into the chapter: *"Before you dive in, here's what I'm doing in this chapter…"*
- **Post-read framing** — the author is reflecting with the reader: *"Now that you've made it through, here's what I hoped landed, and here's where I'd give ground to a sharp critic."*

First-person pronouns. Contractions are fine. No em-dash pileups (max one per paragraph; prefer sentence breaks). Plain English when plain English lands harder. Complexity only when the idea earns it.

### Author-character channeling

Each book has a distinct voice register. Fitzpatrick reads different from Kahneman reads different from Taleb. The generator identifies the register during the close-reading pass (see next section) and channels it through every section. Examples of what the register looks like in practice:

| Author | Register to channel |
|---|---|
| Rob Fitzpatrick (*The Mom Test*) | Self-effacing, colloquial ("cool", "awesome", "doomed", "gold dust"), anecdote-driven |
| Daniel Kahneman (*Thinking, Fast and Slow*) | Precise, measured, academic, "my colleague Amos and I" |
| Nassim Taleb (*Antifragile*) | Polemical, erudite, multilingual vocabulary, sardonic asides |
| Atul Gawande (*The Checklist Manifesto*) | Warm, physician-reflective, patient case studies |

The generator must not impose a single house style. Each book should feel genuinely different.

### One explicit voice break

In the post-read synthesis, the **Contrarian Take** section briefly leaves author voice for a critic, then returns. Frame it as:

> *"A sharp reader will push back here, and they'd be right about X —"*

then the specific pushback, concrete and biting. Then back to the author, graciously:

> *"I'd give ground on that. This is where my argument stretches further than my evidence can carry…"*

Every other section stays in author voice.

## Close-Reading Extraction Discipline

**Required workflow step.** Before filling any pre-read or post-read template, the generator runs an internal extraction pass against the chapter text. The extraction output stays internal — it is the scratchpad the generator reasons over, and it does not appear in the chapter file.

Each bullet, term, and per-lens paragraph in the final output must be traceable to extracted material.

### The extraction pass (per chapter)

1. **Thesis** — the one sentence from the chapter that, reduced to ~25 words, survives. Verbatim or close paraphrase.
2. **Anchor phrases** — 8–12 verbatim phrases, metaphors, vivid images, canonical examples. The specific words the author uses ("bulldozer", "toothbrush", "fragile", "gold dust", "earlyvangelist", etc.). Every Watch-For bullet must attach to one.
3. **Defined terms** — 4–8 terms the author actively defines in the chapter, along with the author's own working definition (not a paraphrase). Pulled from the text, not invented.
4. **Author-voice register** — 2–3 sentences characterizing the author's voice in this chapter. Colloquial / academic / polemical / warm / etc. Specific turns of phrase. This register drives every section's voice.
5. **Structural role** — 1–2 sentences on what this chapter does in the book's argument. Example: *"It's the 'why rigor matters' beat before the rules in Ch 4."*

### Enforcement rule

**Do not proceed to template filling until extraction is complete.** Each bullet, term, and per-lens paragraph in the output must be traceable to an extracted item. If a Watch-For bullet has no anchor, if a Key Term has no source in the text, or if a per-lens paragraph has no extracted insight to ground on, return to the extraction pass before writing.

### Where extraction runs

- **`/reading-lens:brief N`** — the main agent runs extraction + generation for the single chapter.
- **`/reading-lens:synthesize N`** — same.
- **`/reading-lens:setup`** — each subagent runs extraction + generation for its assigned chapter batch. The book-level author-voice register (identified during `0. General.md` generation) is passed in as seed context; subagents refine it per chapter.

## Templates

### Book Overview — content for `0. General.md`

```markdown
---
type: book
title: "{title}"
author: "{author}"
source_epub: "{absolute-epub-path}"
status: reading
started: {YYYY-MM-DD}
chapters: {N}
language: {ISO 639-1 code, default: en}
lenses:
  - role: "{Role 1}"
    interests: "{interests}"
  - role: "{Role 2}"
    interests: "{interests}"
tags: [book, reading-lens]
---

# {title}
*by {author}*

> **{one-liner — 1 sentence on what this book is really about, not the marketing blurb}**

## Thesis

{2–3 sentences: the core argument the book is making}

## Why it matters to a builder

{2–3 sentences: why a reader with the configured lenses should read this specifically}

## Key terms this book teaches

- **{term}** — {working definition under 20 words}
- ... (6–10 items)

## Focus prompts — hold these while reading

- [ ] {active-reading question to hold across the whole book}
- ... (4–6 items, checkboxes)

## Per-lens learning

### {Role 1}
{1–2 sentences: what this reader, in this role, stands to gain from this book specifically — not generic "will learn about strategy"}

### {Role 2}
...

(one H3 per lens)

## Converses with

- {other book, framework, or resource} — {1 sentence on the link}
- ... (3–5 items)

## Chapters

- [[1. {chapter 1 title}|1. {chapter 1 title}]]
- [[2. {chapter 2 title}|2. {chapter 2 title}]]
- ...
```

### Chapter Stub (written at setup, sections filled later)

```markdown
---
type: chapter
book: "[[0. General|{book-title}]]"
chapter_number: {N}
chapter_title: "{title}"
word_count: {wc}
status: unread
brief_generated: null
synthesis_generated: null
synthesis_has_notes: false
tags: [chapter, reading-lens]
---

# {N}. {chapter_title}

## Pre-read brief

*(run `/reading-lens:brief {N}` before reading)*

---

## ✍️ My notes

*(take your notes here while reading — this section is never overwritten by the skill)*

---

## Post-read synthesis

*(run `/reading-lens:synthesize {N}` after reading)*
```

### Pre-read Brief — fills `## Pre-read brief`

**Voice:** First person. The author is about to walk the reader into the chapter. See the *Writing Voice* section above. Channel the author-voice register extracted in close-reading step 4.

**Notation:** `[...]` marks a placeholder filled during generation. Placeholder descriptions are plain text — rendered output is plain prose, *not* italic, unless `*…*` is shown literally.

```markdown
> **[Author-voice one-line thesis — their own framing, not a
> summary of what the chapter covers]**

[Paragraph 1: 2–3 sentences. Author's voice. A personal opener —
"here's where I'm about to take you." Introduces the chapter's
concerns in the author's register.]

[Paragraph 2: 2–4 sentences. More explanatory. Gives the reader
enough context to understand what they're about to encounter.
Places the chapter in the book's arc — e.g., "I made the
asymmetric-risk argument back in Chapter 3 — this chapter builds
on that by showing you the three species of bad data I keep
seeing…"]

**Watch for**
- [Phrase-anchored bullet, 1–3 sentences, author voice. Cites a
  specific word, metaphor, anecdote, or moment from the chapter.
  Example: "When I drop the bulldozer metaphor in a bit, I mean
  something very specific — the founder who asks 'do you think
  this is a good idea?' and treats the nod they get as data."]
- [3–5 bullets total. Each grounded in an extracted anchor phrase
  from close-reading step 2.]

**Key terms**
- **Term** — Author-voice definition, 1–2 sentences. The author's
  own working vocabulary. No academic paraphrase. Sourced from
  close-reading step 3.
- [3–6 term→definition pairs total.]

**Questions to hold**
- [ ] [Open philosophical question the chapter raises, framed as
  the author asking the reader to wrestle with it. Not a personal-
  action question — the chapter's unresolved tensions.]
- [ ] [3–5 questions total.]

**Per-lens angles**

*{Role 1}.* [3–5 sentences of flowing author prose, directly
addressed to this lens. Names what the chapter asks of this role
specifically. Depth enough that the reader recognizes themselves
in it. Not a bullet disguised as a paragraph.]

*{Role 2}.* [Same depth, for this lens.]

*{Role N}.* [Same depth, for this lens. Always include every
configured lens as a separate paragraph — never collapse two
lenses into one entry.]
```

**Flexibility rules:**
- If the chapter is structurally a **comparison** (two patterns, two failure modes, before/after dialogue), render Watch For or Key Terms as a 2-column markdown table instead of a bulleted list.
- If the chapter describes a **sequential process**, Watch For may become a numbered list.
- **Per-lens angles never collapse** — always one paragraph per configured lens in the declared order, even if lenses share overlap.
- **Inline wikilinks allowed** when the chapter references an earlier chapter explicitly: `[[3. Talking to customers is hard|Chapter 3]]`.

### Post-read Synthesis — fills `## Post-read synthesis`

**Voice:** First person. The author is reflecting with the reader after the chapter. Channel the author-voice register. The Contrarian Take section is the one explicit voice-break — see *Writing Voice* above.

```markdown
> **[Author-voice one-line core idea — the sentence they'd want
> to survive this chapter]**

[Paragraph 1: 2–3 sentences in author voice. Reflecting on what
was just read together. Example: "Now that you've made it through,
here's what I most hoped landed, and here's why I built the
chapter the way I did."]

[Paragraph 2 (optional, chapter-dependent): 2–3 sentences. Where
the chapter fits in the book's running argument now that it has
done its work.]

**Key takeaways**
- [Substantial bullet, 1–2 sentences per bullet, author voice.
  4–6 total. No clipped labels — each bullet reads as a complete
  thought.]
- [Final bullet names the mental model the chapter builds, as a
  takeaway sentence. Example: "The model I hope you walk away
  with: false positives are asymmetric bets against your own
  runway."]

**Per-lens takeaways**

*{Role 1}.* [3–5 sentences of flowing author prose, directly
addressed to this lens. Monday-morning specific — what changes
in their week because of this chapter. Never a single sentence.]

*{Role 2}.* [Same depth.]

*{Role N}.* [Same depth, one paragraph per configured lens.]

**Contrarian take**

[2–3 paragraphs. Voice break: the critic speaks first.

"A sharp reader will push back here, and they'd be right about X —"
then the specific pushback, concrete and biting. Name the actual
claim that overreaches, not a vague "some might disagree."

Then back to author voice, graciously: "I'd give ground on that.
This is where my argument stretches further than my evidence can
carry…" and a short concession of where the critique lands.]

**Actionable experiments**
- [Concrete experiment a builder could run this quarter, 1–2
  sentences, author voice. 2–3 total. Scaled to a small team's
  reality.]

**Connections**
- **[Other book / framework]** — [1-sentence link in author
  voice. Example: "*Lean Startup* (Ries) — he wrote the
  learning-loop theory; I'm writing the script for what to say
  inside the loop."]
- [3–5 connections total.]

**Flashcards**
- **Q:** [Sharp question that tests the chapter's core move]
  **A:** [Under 30 words.]
- [3–5 pairs total.]
```

## Quality Rules

These rules are not optional. They convert the reading-lens output from a competent book summarizer into a genuinely useful reading companion. Enforce them on every generation.

### Voice and flow

- **Author voice throughout.** First person. Channel the author-voice register identified in close-reading step 4. See the *Writing Voice* section.
- **Flow over friction.** Sentences must read aloud smoothly. No em-dash pileups (max one per paragraph). No noun-stacked Latinate phrases when plain English does the job. Contractions are fine. Complexity only when the idea earns it.
- **No generic MBA platitudes.** Every takeaway must be specific enough that a reader who skipped the chapter could still lose an argument with one who read it. Bad: "focus on customers." Good: "Ries argues the unit of progress is the validated learning cycle — not revenue, users, or ship velocity."

### Grounding

- **Every Watch-For bullet must cite a specific phrase, metaphor, anecdote, or moment from the chapter text.** No unanchored observations. If there's no anchor, cut the bullet.
- **Every Key Term must come from the author's own vocabulary.** Pulled from the chapter text (close-reading step 3), not invented.
- **The close-reading extraction pass is mandatory.** Do not proceed to template filling without it.

### Per-lens rigor

- **Per-lens angles never collapse.** Every configured lens gets its own paragraph (3–5 sentences) in the declared lens order. Never combine two lenses into one line.
- **Lens paragraphs must be role-specific.** If a PM paragraph would read identically as a CEO paragraph, both are wrong. Rewrite until they diverge.
- **Monday-morning specificity in post-read takeaways.** A PM should be able to name one thing that changes in their week because of the chapter. Same for CEO and Entrepreneur.

### Contrarian rigor

- **Contrarian takes must bite.** "Some readers might disagree" is not a contrarian take. Name the specific claim and say why it overreaches, ignores something, or is wrong.
- **The voice-break pattern is required.** The critic speaks first, then the author graciously concedes. See *Writing Voice → One explicit voice break*.

### Other

- **Actionable experiments must fit a small startup.** Not "hire a data science team" — "add an event to track X in the existing analytics for Y feature, run for 2 weeks, compare to the Z cohort."
- **Never fabricate.** If the chapter text is thin or the topic is outside your confidence, say so in-line rather than inventing.
- **Respect the user's notes.** Never modify `## ✍️ My notes`. When generating a notes-aware synthesis upgrade, read the user's content and weave it in — their framing is data.
- **Never delete files. Ever. When in doubt, ask.**
- **Ask before overwriting.** Every regeneration is a deliberate choice, confirmed by the user.

## What This Skill Is NOT

- Not a reading app — reading happens in your EPUB reader of choice.
- Not a summary generator — it's scaffolding around the user's own active reading.
- Not a research agent — it works on one EPUB at a time. Don't web-search unless verifying a specific proper noun.
- Not a general note-taker — other skills (e.g., `no-brainer`) handle general summarization.

## Help Output (`/reading-lens:help`)

When this sub-command is invoked, present:

---

### Reading Lens

Active-reading scaffolding for nonfiction books. Parses an EPUB → generates a structured book analysis in your Obsidian vault.

#### Where things go

`{vault_path}/{books_folder}/{Book Name} ({Author})/`
- `0. General.md` — book overview
- `1. {chapter title}.md` ... `n. {chapter title}.md` — chapter files (brief | your notes | synthesis)

#### Commands

| Command | What it does |
|---------|-------------|
| `/reading-lens:setup <epub-path>` | Start a new book: parse EPUB, choose lenses, generate overview, plus pre-read briefs + post-read syntheses for every chapter |
| `/reading-lens:brief <N>` | Generate pre-read brief for chapter N |
| `/reading-lens:synthesize <N>` | Generate post-read synthesis for chapter N |
| `/reading-lens:overview-redo` | Regenerate `0. General.md` for the current book |
| `/reading-lens:lenses [action]` | Manage global lens presets (list / add / edit / remove / reset) |
| `/reading-lens:to-notion` | Mirror the current book to Notion |

#### Recommended

Use Opus 4.7. Check with `/model`.

#### Setup

Edit `config.yaml` in the skill folder — set `vault_path` and (optionally) edit `global_lenses`.
