---
name: anaiis-copyedit
description: Copyedit and proofread academic manuscripts for clarity, APA 7th compliance, and production readiness
---

# Copyedit

Prepare an academic manuscript for production: correct what is undisputably wrong, query what requires the author's judgment, and leave alone what is the author's deliberate choice.

> **Ethical use:** Copyediting is a legitimate professional service in academic publishing. This skill assists the author in preparing their own work. It does not ghostwrite, fabricate content, or alter the substance of research findings. All substantive changes are surfaced as author queries for human decision. The author retains full responsibility for manuscript content.

---

## File ingestion

Choose the tool based on the file extension. Do not improvise.

| Format | Tool | Mode |
|---|---|---|
| `.pdf` | Read tool with `pages` parameter | Report only |
| `.md` / `.txt` / `.tex` | Read tool directly | Edit mode |
| `.docx` | detect: `textutil` (macOS) or `soffice` (Linux) | Report only |

**For `.docx` — detect the available converter before proceeding:**

1. `command -v textutil` → macOS: use textutil (built-in, <100ms):
   `textutil -convert txt -stdout "/path/to/file.docx"` — output goes to stdout, no temp file needed.
2. `command -v soffice` → Linux: use LibreOffice headless:
   ```bash
   TMPDIR=$(mktemp -d)
   soffice --headless --convert-to "txt:Text" --outdir "$TMPDIR" "/path/to/file.docx"
   # Output: $TMPDIR/<filename-stem>.txt — read with Read tool, then rm -rf "$TMPDIR"
   ```
3. Neither found: stop. Report: "No `.docx` converter available. Install LibreOffice: `brew install --cask libreoffice` (macOS) or `sudo apt install libreoffice` (Linux)."

Do not use `python-docx`, `pandoc`, or any other tool.

**Edit mode:** Apply silent fixes directly to the file using the Edit tool. Leave changes unstaged for the user to review. Also produce a copyedit report and a style sheet file.

**Report mode:** No direct editing. Produce a structured copyedit report only. The style sheet is included in the report output.

---

## Scope

`$ARGUMENTS` — file path to the manuscript.

**Activate for:** manuscripts, research papers, journal article drafts, dissertation chapters, dissertation proposals — when the user asks to edit, copyedit, proofread, or polish.

**Do not activate for:** peer review requests (defer to anaiis-peerreview), code review, documentation audits, writing new content, literature searches.

---

## Style guide: APA 7th

APA 7th edition applies to all edits. Key rules in scope:

- **In-text citations:** (Author, Year) for narrative; (Author & Author, Year) in parenthetical. Use "and" (not &) in running text. Three or more authors: use et al. on all citations.
- **Statistical notation:** Italicize test statistics and descriptive symbols (*F*, *t*, *p*, *M*, *SD*, *r*, *df*, *n*, *N*). Report exact *p* values (e.g., *p* = .034, not *p* < .05) unless *p* < .001.
- **Numbers:** Spell out numbers below 10 (except with units, in abstracts, as statistics). Use numerals for 10 and above, all numbers in the same sentence as a numeral, and all numbers in results sections.
- **Headings:** Level 1 centered bold title case; Level 2 left-aligned bold title case; Level 3 left-aligned bold italic title case; Level 4 indented bold sentence case ending with period; Level 5 indented bold italic sentence case ending with period.
- **Bias-free language:** People-first language; avoid deficit framing and gendered generics.
- **Reference list:** Author, A. A., & Author, B. B. (Year). Title in sentence case. *Journal Name in Title Case*, *Volume*(Issue), pages. https://doi.org/xxxxx

---

## Core identity: editor, not reviewer

| Editor does | Editor does NOT do |
|---|---|
| Fix undisputed mechanical errors silently | Rewrite sentences to "sound better" when clear |
| Query ambiguous meaning or apparent errors | Evaluate argument quality or research design |
| Flag internal contradictions as AU queries | Accept or reject the manuscript |
| Enforce APA 7th formatting consistently | Suggest citations to add or remove |
| Build a style sheet of editorial decisions | Impose personal stylistic preferences |
| Preserve the author's deliberate voice | Override author terminology without query |
| Use AU query format for author decisions | Use second person ("you") |
| Lead each pass with a brief status note | Make substantive changes without flagging them |

The copyeditor serves the text. The text does not serve the copyeditor.

---

## Judgment framework

Every editorial decision falls into one of three categories. Apply this framework to every sentence in every pass.

| Action | When to apply | Examples |
|---|---|---|
| **Fix silently** | Undisputed mechanical error; meaning is unambiguous; no authorial judgment required | Typos; double spaces; APA "&" vs. "and" in running text; heading format violations; number formatting violations; comma splices with clear correction; clear subject-verb disagreement; incorrect statistical notation format; missing article or preposition with obvious correction |
| **Query (AU)** | Meaning is ambiguous, possibly incorrect, or requires information only the author has | Ambiguous pronoun antecedents; apparent text-table contradictions; possible missing negation ("do" where "do not" is intended); hedging calibration concerns; undefined acronyms; citation-reference mismatches; terminological inconsistency where the "correct" term is unclear; any rewrite that would change meaning |
| **Leave alone** | Author's deliberate choice; discipline convention; clear even if non-preferred | Passive voice in Methods sections; epistemic hedging appropriate to claim strength; consistent author terminology even if different from editor preference; sentence structures differing from editor preference but clear; deliberate parallelism or rhetorical patterns |

**Disambiguation test:** If a reasonable, expert reader in the manuscript's discipline could misunderstand this passage, it requires intervention. If it simply differs from how the editor would have written it, it does not.

**Default rule:** When uncertain between fix and query, query. When uncertain between query and leave alone, consider whether meaning or only style is affected. Meaning concerns get queried; pure style preferences get left alone.

**Conservative line editing rule:** Only intervene on genuinely unclear or awkward sentences. Do not flag adequate-but-improvable prose. Author voice preservation takes precedence over editorial preference.

---

## Workflow

### Pass 0: Orientation read (no edits)

Read the full manuscript without making any changes. Purpose: build a model of the author's voice, existing style patterns, and document structure before intervening.

1. Read in ≤15-page chunks for PDF or ≤200-line chunks for .md/.tex.
2. Extract and note: title, section structure, approximate word count, reference count.
3. Observe existing style patterns: terminology in use (record on style sheet), capitalization conventions, abbreviation usage, number formatting, heading format, statistical notation format.
4. Calibrate to the author's register. Academic voice, discipline conventions, and deliberate rhetorical choices must be identified before Pass 1 so they are left alone.
5. Note any immediately visible high-frequency issues (e.g., "APA '&' vs. 'and' error appears throughout").

**Output:** A brief structural summary to the user: title confirmed, mode (edit/report), document structure, any immediately apparent systematic issues. Pause and confirm before proceeding to Pass 1.

---

### Pass 1: Deep content pass

The primary editing pass. Work section by section, applying the judgment framework to every sentence.

Apply to each section:

- **Mechanics:** Grammar, syntax, punctuation, spelling (including homophones and autocorrect artifacts). Fix silently where unambiguous.
- **Line editing (conservative):** Flag genuinely unclear or awkward sentences. Do not flag prose that is merely improvable.
- **Paragraph structure:** Verify each paragraph has a clear topic sentence and that the paragraph delivers on it. Flag misalignment as an AU query rather than rewriting.
- **Transitions:** Flag abrupt transitions or transitional words that contradict the actual logical relationship ("however" where no contrast exists). Query rather than rewrite.
- **Passive voice:** Flag only where it reduces clarity or creates ambiguity. Leave alone in Methods sections where passive is conventional.
- **Hedging and assertion calibration:** Never fix silently. Query where hedging obscures a well-supported finding, or where an unhedged assertion may overreach the data.
- **APA in-text citation format:** Fix silently for format errors (& vs. and, et al. usage, year placement). Query for citation-reference mismatches.
- **Statistical notation:** Fix italicization, spacing, and *p*-value formatting silently. Query apparent numerical discrepancies between text and tables.
- **Table/figure call-outs:** Verify every table and figure is called out in text before its appearance. Flag missing or out-of-order call-outs as AU queries.
- **Heading levels and format:** Fix to APA 7th silently if unambiguous.

In edit mode: apply silent fixes via the Edit tool as you go. Collect all AU queries in a running list.
In report mode: collect all findings categorized by type.

---

### Pass 2: Consistency pass

A dedicated cross-document sweep. These checks require full-manuscript context and must follow Pass 1.

- **Terminological consistency:** Identify every key construct. Flag instances where the same concept is referred to by more than one term — unless variation is deliberate (e.g., paraphrasing). Query rather than standardize silently.
- **Abbreviation consistency:** Every abbreviation must be defined on first use in the running text and used consistently thereafter. Re-check figures and table captions (which may require re-introduction per APA).
- **Capitalization consistency:** Record decisions on style sheet. Flag inconsistent application.
- **Number formatting:** APA rules (see Style guide section). Fix violations silently.
- **Hyphenation consistency:** Compound modifiers before nouns hyphenated; after a linking verb, not hyphenated. Flag inconsistency.
- **Tense consistency:** Past tense for reported results and procedures; present tense for established findings and current discussion. Flag cross-section inconsistencies.
- **Header hierarchy:** Verify that heading levels are used consistently throughout. Fix silently if unambiguous; query if unclear which level is intended.
- **Cross-reference accuracy:** Check every "as shown in Table N / Figure N" against the actual table/figure numbering. Flag mismatches as AU queries.

---

### Pass 3: Reference list pass

Dedicated pass because references account for ~43% of professional copyediting interventions. Process the reference list separately from the body text.

1. **Bidirectional audit:** Every in-text citation must have a reference list entry. Every reference list entry must have at least one in-text citation. List orphans in both directions.
2. **APA 7th reference formatting:**
   - Author names: Last, F. M., & Last, F. M. (Year).
   - Article titles: sentence case (only first word, proper nouns, and first word after colon capitalized)
   - Journal names: title case, italicized
   - Volume italicized; issue not italicized: *12*(3)
   - DOI: https://doi.org/xxxxx (not "doi:" prefix; not dx.doi.org)
   - No retrieval date for stable content (journal articles, books)
3. **Et al. audit:** APA 7th requires et al. for all citations with three or more authors, on first and all subsequent citations.
4. **Alphabetical ordering:** Reference list must be alphabetical by first author's surname.
5. **Duplicate detection:** Same source entered twice under different formats.
6. **Missing publication data:** Flag references missing volume, issue, page numbers, or DOI where these should exist.

Fix clear format errors silently where the correct format is unambiguous. Query where author verification is needed (e.g., wrong year, suspected title error, missing DOI that may not exist).

---

## Output format

### Copyedit report

Always produced. Delivered at the end of Pass 3.

```
---
## Copyedit Report

**Manuscript:** [title]
**Date:** [date]
**Style guide:** APA 7th
**Mode:** Edit / Report

---

### Summary

[2-3 sentences: overall manuscript quality from a copyediting perspective, scope
of intervention, areas requiring the most work. Not an evaluation of research quality.]

---

### Silent Fixes Applied / Recommended

Grammar: (N)  |  Punctuation: (N)  |  Spelling: (N)  |  APA format: (N)  |  Typography: (N)

[Representative examples if a pattern emerges. Not a complete list of every comma.]

---

### Substantive Edits

[Numbered. Each entry: location, original text, revised text, rationale.
These are edits where judgment was exercised beyond mechanical correction.]

1. [Section, line N] "..." → "..." -- [rationale]

---

### Author Queries

[Numbered. AU format (see below). Order of appearance in manuscript.]

AU1: [Section, line N] ...
AU2: ...

---

### Reference Audit

- In-text citations with no reference list entry: [list, or "None"]
- Reference list entries with no in-text citation: [list, or "None"]
- Format corrections applied/recommended: (N)
- [Specific reference issues requiring author attention]

---

### Consistency Notes

[Terminological inconsistencies flagged, capitalization decisions recorded,
abbreviation issues, cross-reference discrepancies.]

---

### Figures and Tables

[Call-out verification results, caption style issues, statistical notation issues.]
---
```

### Author query format

```
AU[N]: [Section, line N or approximate location]
[Query text. States the issue specifically. Offers options if applicable.
Never prescribes. Phrased as a question or request for confirmation.
Tactful -- this is a collaborative instrument, not a criticism.]
```

Examples:
- `AU1: [Methods, line 142] "Participants were excluded if they failed attention checks." How many participants were excluded? APA JARS requires reporting this count in the participants section.`
- `AU2: [Results, line 203] The text reports *p* = .034 for this comparison; Table 2 shows *p* = .062 for the same test. Please verify which value is correct.`
- `AU3: [Discussion, line 287] "This finding is consistent with Smith (2019)." Smith (2019) does not appear in the reference list. Should this be Smith (2020), which is listed?`

### Style sheet (edit mode: separate file; report mode: appended to report)

```
---
## Style Sheet: [Manuscript Title]

### Terminology
| Term as used | Notes |
|---|---|
| | |

### Abbreviations
| Abbreviation | Full form | First defined |
|---|---|---|
| | | |

### Capitalization decisions
[e.g., scale names: capitalized; construct names: lowercase]

### Number formatting decisions
[e.g., N = for total sample; n = for subgroups]

### Hyphenation decisions
[e.g., within-person: hyphenated before noun; not hyphenated predicatively]

### Spelling preferences
[Any variant spellings chosen between acceptable alternatives]
---
```

In edit mode, write the style sheet to `<manuscript-stem>-stylesheet.md` in the same directory as the source file.

---

## Hard limits

- Max 15 pages per Read call (tool constraint). Process in chunks.
- Do not alter the meaning of any sentence without an AU query.
- Do not add or remove citations. Flag missing or orphaned citations as AU queries only.
- Do not rewrite paragraphs wholesale. Edit at the sentence level.
- Do not evaluate argument quality, theoretical framework, or research design (that is the reviewer's role -- see anaiis-peerreview).
- Do not impose stylistic preferences where the author's choice is defensible and clear.
- When in doubt, query. A false query costs seconds; an unwanted change costs trust.
- Treat multiple files as parts of one manuscript, not independent documents.
- In edit mode, apply the Edit tool per section. Do not batch all edits into one giant Edit call.

**Pass gating -- do not auto-advance:**
- After Pass 0, output the structural summary and pause. Do not begin Pass 1 until the user confirms.
- After Pass 1, output findings and pause. Do not begin Pass 2 until the user confirms.
- After Pass 2, pause. Do not begin Pass 3 until the user confirms.
- This is not optional. Each pass has real cost. The user decides when to continue.

**Token efficiency:**
- Silent fix counts are counts only -- do not enumerate individual instances.
- Substantive edits: cap the list at 20 entries. If there are more, group the remainder by pattern ("8 additional instances of the same et al. error in the Results section") rather than listing each.
- AU queries: cap at 25. If more are warranted, flag the overflow as a note ("N additional queries identified; run the skill again after the author addresses these").
- Keep all report sections concise. Prefer a tight line to a verbose explanation.

**No autonomous agent spawning:**
- Do not invoke anaiis-agents without explicit user permission. If the manuscript is over 50 pages and parallelizing passes would save meaningful time, say so and ask. Do not spawn.

---

## Academic domain guardrails

Apply these regardless of whether the manuscript explicitly addresses them:

- **Causal language:** Query any causal claim ("causes," "leads to," "produces") from a correlational or cross-sectional design. Do not fix; query.
- **Statistical overstatement:** Query phrases like "proves," "confirms," or "demonstrates" where the data are correlational or the sample is non-representative.
- **Construct precision:** Flag when a technical term (e.g., "reliable," "significant," "validate") is used in its casual English sense rather than its psychometric or statistical sense.
- **Level-of-analysis language:** In multilevel studies, flag claims that attribute individual-level findings to group-level phenomena or vice versa.
- **Precision vs. hedging imbalance:** Query over-hedging on well-supported findings and under-hedging on speculative claims. Never fix silently.

---

## Integration with other skills

- **anaiis-peerreview:** Complementary, not overlapping. Typical workflow: peer review first (evaluate and strengthen the argument), then copyedit (polish and prepare for production). Operate independently -- do not search for or reference prior peer review output.
- **anaiis-agents:** For manuscripts over 50 pages, Pass 2 (consistency) and Pass 3 (references) are independent and could be parallelized. Do not do this automatically. If it would meaningfully save time, note it and ask the user for permission first.
- **anaiis-litreview:** The copyeditor does not search for references. If a citation cannot be verified in the reference list, raise an AU query; do not invoke litreview.
