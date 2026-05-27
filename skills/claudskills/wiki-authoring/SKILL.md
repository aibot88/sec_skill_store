---
name: wiki-authoring
description: >
  Use when authoring or editing pages under /knowledge/ on the lab website
  (paper pages, topic pages, repo pages). Covers required frontmatter fields,
  slug rules, the h1-must-match-title invariant, finding anchors, git commit
  conventions, the wiki_janitor audit, and the preservation rule for category
  and papers_supporting fields.
---

# Lab Wiki Authoring

The lab wiki lives at `https://coleoguy.github.io/knowledge/` in the Jekyll
repo at `~/Desktop/GitHub/coleoguy.github.io/`.

---

## Two Entry Points — Choose the Right One

**1. Ingesting a new paper end-to-end**
Use `ingest_paper_to_wiki`. The pipeline encodes all rules in this document
automatically. You do not need to read this skill for that path.

**2. Any ad-hoc wiki operation** — hand-editing a topic page, fixing a
cross-link, creating a topic from scratch, renaming a paper, splicing in a new
finding, or any change not driven by `ingest_paper_to_wiki`:

**Before writing a single line, call `read_wiki_handoff()`.**

That tool returns the full `WIKI_HANDOFF.md` spec (~260 lines). The rules
in this SKILL.md summarize it; the handoff is authoritative. Writing to
`/knowledge/` without reading the handoff is a reliable way to break the
live landing page.

---

## Directory Structure

```
knowledge/
├── index.md                  ← SINGLE consolidated landing page — do NOT touch
├── papers/
│   └── 10_1534_genetics_117_300382.md   ← DOI-slug filenames
├── topics/
│   └── sex_chromosome_evolution.md
└── repos/
    └── evobiR.md
```

**Critical:** `knowledge/papers/index.md`, `knowledge/topics/index.md`, and
`knowledge/repos/index.md` MUST NOT EXIST. They were deleted intentionally.
The landing page uses Jekyll Liquid to pull all three sections dynamically.
If you create sub-index files, duplicate navigation appears and the site breaks.

---

## Slug Rules

### Paper slugs (DOI-derived)

```
DOI:  10.1534/genetics.117.300382
File: knowledge/papers/10_1534_genetics_117_300382.md
```

Replace every `/` and `.` with `_`. For papers without DOIs, use a lowercase
underscore-separated descriptive slug. Do NOT create new pages with year-letter
slugs (e.g. `2014b.md`) — those are legacy files being migrated by the Canon
rename agent. Do NOT manually rename existing legacy files.

### Topic slugs

Lowercase, underscores, descriptive. Example: `karyotype_evolution`,
`fragile_y_hypothesis`, `sex_chromosome_evolution`.

---

## Required Frontmatter — Paper Pages

Every field must be present. Missing fields cause silent rendering failures.

```yaml
---
layout: default
title: "Full article title exactly as it appears in the paper"
doi: 10.1534/genetics.117.300382     # no https://doi.org/ prefix; empty string if none
fingerprint_sha256: d067836a...       # SHA256 of the source PDF used for grounding
authors: "Blackmon H, Brandvain Y"   # full author string from paper
journal: "Genetics"                  # journal name; empty string if preprint/book
year: 2017                           # integer, not string
topics: [fragile_y_hypothesis, sex_chromosome_evolution, sex_linkage_mutation]
tier: canon                          # canon | standard | peripheral
ingested_at: 2026-04-21T14:53:07.827586+00:00
permalink: /knowledge/papers/SLUG/
---

# Full article title exactly as it appears in the paper
```

---

## Required Frontmatter — Topic Pages

```yaml
---
layout: default
title: "Karyotype Evolution"              # human-readable, title case
topic_slug: karyotype_evolution           # machine slug, matches filename
last_updated: 2026-04-21T18:27:18.651978+00:00
papers_supporting: [10.1534/genetics.117.300382]
permalink: /knowledge/topics/SLUG/
category: "Karyotype evolution"           # REQUIRED — see category map below
---
```

---

## Required Frontmatter — Repo Pages

```yaml
---
layout: default
title: "evobiR"
repo: github.com/coleoguy/evobiR        # no https:// prefix
language: R
papers_using: [10.1234/..., ...]
permalink: /knowledge/repos/SLUG/
---
```

---

## The h1-Must-Match-Title Invariant

The `title:` field in frontmatter and the `# H1` at the top of the body **must
be identical**. The landing page renders `title:` as the link text; stub titles
like `"2014b"`, `"2020 microsats"`, or `"2016 saga"` are unacceptable.

- Get the real title from CrossRef, PubMed, or the PDF header.
- If the paper has HTML entities in the title (e.g., `<i>Drosophila</i>`), write
  plain text in the `title:` field.
- The body `# H1` should be identical to `title:` — no YAML quotes, no HTML.

---

## Finding Anchors

In paper pages, findings use explicit HTML anchors:

```markdown
<a id="finding-1"></a>
### Finding 1 — [One-sentence summary of the result]

> "Verbatim quote from the paper that grounds this finding." (p. X)

**Why citable:** [one sentence]
**Counter/limitation:** [one sentence]
**Topics:** [sex_chromosome_evolution](/knowledge/topics/sex_chromosome_evolution/),
            [karyotype_evolution](/knowledge/topics/karyotype_evolution/)
```

Anchor IDs are sequential integers (`finding-1`, `finding-2`, ...) per paper.
Cross-references from topic pages use these anchors:

```markdown
[Smith & Jones 2022, Finding 3](/knowledge/papers/10_1234_something/#finding-3)
```

Never use headings or slugified text as anchors — only the explicit
`<a id="finding-N"></a>` form is used.

---

## The Category Field — Single Most Important Rule for Topic Pages

`category:` controls which collapsible group the topic appears in on the
landing page. **A topic without `category:` is invisible to visitors.**

### Preservation Rule

When updating an existing topic page:
1. Read the file first (`read_wiki_topic(slug)` or read from disk)
2. Copy the existing `category:` value into the new version — never drop it
3. Append new DOIs/hashes to `papers_supporting:` — never replace the list
4. Update `last_updated:` to the current UTC ISO timestamp

### Complete Category Map (8 categories)

**Sex chromosomes**
`sex_chromosome_evolution`, `fragile_y_hypothesis`, `sex_linkage_mutation`,
`y_naught_asymmetry`, `sexual_antagonism`, `sexually_antagonistic_selection`,
`meiotic_drive`, `haplodiploidy_evolution`

**Karyotype evolution**
`karyotype_evolution`, `karyotype_evolution_overview`, `chromosome_number_evolution`,
`chromosome_number_optima`, `centromere_type`, `centromere_evolution`,
`holocentric_chromosomes`, `chromosome_fusion`, `karyotype_database`

**Genome structure**
`genome_structure_evolution`, `genome_assembly`, `genome_dynamics`,
`transposable_elements`, `microsatellite_evolution`, `genetic_architecture`

**Insects & Coleoptera**
`coleoptera`, `coleoptera_genomics`, `coleoptera_karyotype`, `bee_genomics`,
`bee_phylogenomics`, `insect_genomics`, `Tribolium`

**Speciation & macroevolution**
`ring_species`, `speciation`, `phylloscopus`, `avian_evolution`,
`avian_hybridization`, `Galliformes`, `uce_phylogenetics`,
`diversification_rates`, `hybridization`, `postzygotic_isolation`,
`reproductive_isolation`, `domestication`, `domestication_genomics`,
`life_history_evolution`, `convergent_evolution`

**Population genetics**
`demographic_inference`, `conservation_genomics`, `conservation_genetics`,
`sequencing_methods`, `coalescent_simulation`, `isolation_by_distance`,
`effective_population_size`, `divergence_time_estimation`, `population_genetics`

**Quantitative genetics & epistasis**
`epistasis`, `line_cross_analysis`, `quantitative_genetics`,
`quantitative_genetics_methods`, `artificial_selection`, `dispersal`,
`selection_and_drift`, `trait_definition`, `comparative_methods`,
`ancestral_state_reconstruction`

**Bioinformatics & tools**
`bioinformatics_tools`, `model_organism_databases`, `cavefish_genomics`,
`circadian_rhythm_evolution`

For new slugs not in this map, assign the closest category. If nothing fits,
use `"Bioinformatics & tools"` as a catch-all and flag the new slug in the
commit message. Never leave `category:` empty.

---

## Non-Destructive Update Protocol (tealc:auto markers)

Topic page bodies use HTML comment markers to separate Tealc-managed content
from Heath-authored notes:

```
<!-- tealc:auto-start -->
# Topic Title

## Current understanding
(synthesized prose — regenerated on every update)

## Supporting evidence
...
<!-- tealc:auto-end -->

## My personal notes
Heath's hand-written content — preserved across every Tealc update.
```

- Content **inside** the markers: Tealc-managed; regenerated on each update
- Content **outside** the markers: Tealc-never-touches; preserved always
- **Legacy pages** (no markers): treated as all-auto; wrapped in markers on
  next update (one-time migration)

When writing code that updates topic pages, use the helpers in
`agent/jobs/wiki_pipeline.py`:
1. `_read_existing_topic_page()` — get full body
2. `_split_body_by_markers(body)` — returns `(before, auto, after, had_markers)`
3. Pass only the `auto` region to the topic writer
4. `_splice_auto_region(new_auto, existing_body)` — reassemble the final body

---

## Git Commit Convention

All wiki commits must be prefixed `[tealc]`:

```
[tealc] ingest 10.1093/g3journal/jkaf217 — achiasmatic meiosis
[tealc] update topic: sex_chromosome_evolution — add Smith 2025 findings
[tealc] fix: restore category: field on karyotype_database topic
```

**One logical unit per commit.** Do not batch unrelated paper ingestions or
unrelated topic updates into a single commit. The prefix makes wiki-related
history filterable via `git log --grep='\[tealc\]'`.

---

## wiki_janitor Weekly Audit

`wiki_janitor.py` runs **Mondays at 8am Central**. It produces a briefing
summarizing:
- Stub titles (paper pages with year-letter slugs as title values)
- Missing `category:` fields on topic pages
- Title/H1 drift (title: field and # H1 no longer match)
- Broken slug cross-links
- Orphaned topic references (papers list a topic slug that has no topic file)
- Cross-link candidates (findings that should link to each other)

If Heath asks "what's the wiki status?", pull the latest `wiki_janitor`
briefing via `run_scheduled_job("wiki_janitor")` rather than re-auditing
manually. The briefing is the authoritative current state.

---

## Pre-Commit Verification Checklist

Run from `~/Desktop/GitHub/coleoguy.github.io/` before any push:

```bash
# 1. No topic files missing category
grep -rL 'category:' knowledge/topics/*.md

# 2. Sub-index files must not exist
ls knowledge/papers/index.md knowledge/topics/index.md knowledge/repos/index.md 2>&1
# Expected: "No such file or directory" for all three

# 3. Title must match H1 in paper files
python3 - <<'EOF'
import re, os
errors = []
for f in sorted(os.listdir("knowledge/papers")):
    if not f.endswith(".md") or f == "index.md": continue
    text = open(f"knowledge/papers/{f}").read()
    fm = re.search(r'^title:\s*"(.*?)"', text, re.MULTILINE)
    h1 = re.search(r'^# (.+)$', text, re.MULTILINE)
    if fm and h1 and fm.group(1).strip() != h1.group(1).strip():
        errors.append(f"{f}: title≠h1")
for e in errors: print(e)
if not errors: print("OK — all titles match h1")
EOF
```

---

## Tool Summary

| Task | Tool |
|------|------|
| Ingest a new paper end-to-end | `ingest_paper_to_wiki` |
| Any ad-hoc wiki edit | `read_wiki_handoff()` first, then edit |
| Read a topic page | `read_wiki_topic(slug)` |
| List all topic pages | `list_wiki_topics()` |
| Check wiki status / audit | latest `wiki_janitor` briefing |
| Fetch full handoff spec | `read_wiki_handoff()` |
