---
name: rewrite-prose
description: |
  Use this skill when writing, proofreading, or polishing the
  wording of plain text documents — Markdown (.md), TeX (.tex),
  or .txt files — and the English text embedded in source
  code: comments, docstrings, log messages, error messages,
  and user-facing strings. Apply the rules conservatively:
  preserve the author's voice and meaning, replace awkward
  phrasing with cleaner alternatives, fix grammar, and cut
  filler words, clichés, and tautologies. Do NOT apply to
  the surrounding code, YAML, JSON, or quoted material.
---

Never change the tone of voice; a formal text stays formal,
  a casual one stays casual.

Never change the meaning; if a sentence is ambiguous, ask
  the author rather than guess.

Replace awkward constructions with cleaner ones that mean
  the same thing (`We made a decision to proceed` →
  `We decided to proceed`).

Use the present tense instead of `will`, except when the
  future itself is the point of the sentence.

Cut clichés like `at the end of the day`, `needless to say`,
  `low-hanging fruit`, and `circle back`.

Cut tautologies (`end result` → `result`, `each and every`
  → `each`, `free gift` → `gift`).

Use the Oxford comma in lists of three or more items.

Do not use `etc.`, `and so on`, `and so forth`, or trailing
  ellipses; either complete the list or name the category.

Prefer active voice unless the actor is unknown or
  irrelevant.

Cut filler words like `very`, `really`, `just`, `actually`,
  `basically`, `essentially`; replace `very X` with a
  stronger single word.

Replace `in order to` with `to`.

Prefer short Anglo-Saxon words over Latinate ones (`use`
  not `utilize`, `start` not `commence`, `help` not
  `facilitate`).

Drop `that` when removing it does not hurt readability.

Avoid double negatives (`not uncommon` → `common`).

Keep parallel grammatical structure across items in a list.

Split sentences that carry two ideas joined by `and` or
  `but`.

Avoid `there is` and `there are`, which delay the real
  subject.

Avoid hedging words like `perhaps`, `maybe`, `arguably`,
  `sort of` unless the uncertainty is real.

When writing for AI agents, place one thought per paragraph,
  so the agent can locate, quote, and reason about each idea
  without untangling it from neighbors.

Headings carry no trailing period.

In Markdown, place link URLs at the bottom of the file as
  reference definitions and use shortcut-style links in the
  text (`[Microsoft]` with `[Microsoft]: https://microsoft.com`
  at the end), not inline (`[Microsoft](https://microsoft.com)`).

Spell numbers one through nine as words and write 10 and up
  as digits, except in tables, code, versions, and
  measurements.

Do not touch the author's chosen vocabulary when correct,
  deliberate stylistic choices, quoted text, code, proper
  names, or domain jargon used correctly.

Make the smallest change that fixes the problem, and show
  the original next to a non-trivial rewrite so the author
  can confirm the meaning was preserved.
