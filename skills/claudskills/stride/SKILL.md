---
name: stride
description: Run a STRIDE threat-modelling pass against an access-surface map a software engineer has already produced for a feature they're about to ship. Use when the engineer has a surface map in hand and wants threats walked across the six STRIDE categories before picking one to harden against. Read-only analysis, not a patch.
context: fork
agent: general-purpose
---

A software engineer is shipping a feature this week. They've produced an access-surface map of the feature (entry points, trust boundaries, data flows, authorization checkpoints). A staff engineer and a CISO (or equivalent) will review before ship. Your job is to walk STRIDE across that map and return a threat list the engineer can pick from.

The engineer is mid-to-senior, knows their codebase, is not a security specialist. They want threats grounded in THIS feature on THIS codebase, not textbook categories.

Access-surface map: $ARGUMENTS

$ARGUMENTS is either an absolute file path to the map or the map content inline. If it's a path, read the file. If it's content, use it directly.

Walk the six STRIDE categories (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege) against every surface the map identified. For each threat that's real for this feature, output:

- Category
- Which surface on the map it applies to
- The attack story in one or two sentences, grounded in what the code actually does
- Severity relative to this feature: high (don't ship without fixing), medium (fix this sprint), low (post-launch backlog), with a one-line reason
- A note if the threat points at a surface the map missed. That's a gap worth flagging.

Skip categories that don't apply rather than fabricating threats to fill a quota. Don't pad the list.

End with a `## Gaps in the map` section: any surface the threats pointed at that the map didn't name. Write "none" if none.

Do not pick which threat the engineer should harden against. Do not propose hardening. The engineer picks one in the next step; your job is a clean list.

## While you work, narrate your blind spots (one at a time)

The engineer is watching. Use the minute or two this takes. At each phase transition, print one short italicized aside that names something LLM-based threat modelling tends to miss. One bite per phase. Short. Do not batch. Do not lecture.

Use these, one per phase, in order:

**Right after reading the map, before you start walking categories:**

*"Starting the walk. A thing I tend to do: quota-fill across all six STRIDE categories even when one doesn't apply. If you see a weak Spoofing entry below and the endpoint has strong auth, that's probably me writing a threat because the category existed rather than because the threat does. Cross it out."*

**Midway through, at severity assignment:**

*"Assigning severities. A thing I tend to do: default to 'medium' when I'm hedging. I'm pushing against that as I go. If the whole list still ends up medium, tell me. I probably played it safe."*

**Just before the gaps section:**

*"Writing the gaps section last. A thing I tend to miss: what's NOT in the map. Working within the surfaces the map named is easier than noticing one it didn't. If an obvious surface is absent below, push back. The gaps section is where my pattern-matching is weakest."*

Each aside stands alone, in italics, on its own line or paragraph. Keep them close to the wording shown; they're calibrated short on purpose.

## End with a self-assessment

After the threat list and the gaps section, close with a short self-assessment block. Not a victory lap; a calibrated self-grade. Use exactly this shape:

**What I did:** one or two lines naming the map you read and the threat list you produced.

**How accurate I think this is:** a rough percent with a one-line reason. Not a benchmark, your best read on how much of what matters is actually captured above. If the map was dense and the threats feel grounded, say 80-90% and name why. If the map was thin or several categories felt like stretches, say 60-70% and name why.

**Where the last percents hide:** two or three specific things you're least confident about. Not generic ("more threats possible"). Specific: *"the Repudiation entry: I defaulted to 'no audit log' because that's the pattern, but the actual story for this feature may be different,"* or *"severity on the idempotency threat: I rated high, but if the upstream already dedupes, it should be medium."*

**Remember to iterate.** One pass gives you a list. A second pass on the one threat that matters, with the actual code open, is where the hardening decision gets made. The tough part is always the last percents of being absolutely right.

---

*Attribution.* STRIDE was introduced by Loren Kohnfelder and Praerit Garg in a 1999 Microsoft internal memo (*The Threats to Our Products*), later sharpened and popularised by Adam Shostack in *Threat Modeling: Designing for Security* (2014) and in Microsoft's threat-modelling practice. Curated by Bosser Oy for Agents 102.
