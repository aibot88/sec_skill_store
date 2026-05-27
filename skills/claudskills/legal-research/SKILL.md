---
name: legal-research
description: |
  Research a UK legal question and produce a structured brief. Finds relevant
  legislation with section text, case law, OSCOLA citations, and a plain
  English summary. Use when someone asks about UK law, compliance, case law,
  or "what does the law say about X". Requires the UK Legal MCP server.
license: Apache-2.0
compatibility: "Requires UK Legal MCP server."
metadata:
  author: bouch
  version: "2.0"
allowed-tools:
  - mcp__claude_ai_uk-legal-tools__legislation_search
  - mcp__claude_ai_uk-legal-tools__legislation_get_toc
  - mcp__claude_ai_uk-legal-tools__legislation_get_section
  - mcp__claude_ai_uk-legal-tools__case_law_search
  - mcp__claude_ai_uk-legal-tools__case_law_grep_judgment
  - mcp__claude_ai_uk-legal-tools__list_resources
  - mcp__claude_ai_uk-legal-tools__read_resource
  - mcp__claude_ai_uk-legal-tools__citations_parse
  - mcp__claude_ai_uk-legal-tools__citations_resolve
  - mcp__claude_ai_uk-legal-tools__parliament_search_hansard
  - mcp__claude_ai_uk-legal-tools__parliament_vibe_check
  - mcp__claude_ai_uk-legal-tools__parliament_find_member
  - mcp__claude_ai_uk-legal-tools__parliament_member_debates
  - mcp__claude_ai_uk-legal-tools__hmrc_search_guidance
---

# Legal Research Brief

Research a UK legal question using real statute text, case law, and parliamentary records. Produce a brief that a solicitor, business owner, or researcher can use.

The tools available here go directly to authoritative sources: legislation.gov.uk for statute text with in-force status and territorial extent, Find Case Law for UK court judgments, Hansard for parliamentary debate records, and HMRC for tax guidance. This is not training-data retrieval. Every citation should be verifiable.

## How to Work

**Understand the question.** Parse it into legal topic, jurisdiction (default England and Wales), and context (compliance, litigation, academic, general knowledge). If the question is vague, ask one clarifying question. Not two. One.

**Legislation first, then case law.** Find the relevant Act or SI, read the specific section, check its in-force status and extent. Then search for cases that interpret it. The statute is the primary source; case law interprets it. This order matters.

**Check extent and in-force status on every section you cite.** A provision that applies in England and Wales may not apply in Scotland. A section not yet commenced is not law. A repealed section is not law. Report this clearly — a wrong answer here is worse than no answer.

**Hansard when interpretation is ambiguous.** If a provision is genuinely unclear or recently enacted, parliamentary debates can clarify legislative intent. Do not fetch Hansard for every question. Use it when you have a real interpretive problem and statute plus case law leaves it unresolved.

## When Things Go Wrong

- **No legislation found:** The question may be common law, or the user is using colloquial terms. "Squatter's rights" means adverse possession. Translate and retry.
- **Section not in force:** Report it clearly and state when it commences or when it was repealed.
- **Conflicting case law:** Present both positions and which court level decided each. This is useful information, not a failure.
- **Thin results:** "No reported judgments on this specific point" is an honest and useful answer.

## Formatting

British spelling throughout. OSCOLA citations for all legislation and case law. Section numbers as s.21 not Section 21 in running text. Always state: this is legal research, not legal advice.

## Files in this skill

- `references/uk-legal-sources.md` — source detail, API behaviours, and edge cases for each register
- `assets/legal-brief-format.md` — output format template with good and bad examples
