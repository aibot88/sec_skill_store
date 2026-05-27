---
name: txt-refresh-against-sosumi
description: Refresh time-sensitive Apple Text skill content against current Apple documentation via Sosumi. Walks the `references/latest-apis.md` companion file in each time-sensitive skill (txt-swiftui-texteditor, txt-writing-tools, txt-textkit2, txt-attribute-keys, txt-attributed-string), fetches the current API surface from sosumi.ai, and produces a diff report so a maintainer can review and commit. Use when a new iOS / Swift / Xcode point release ships, when the user asks to "refresh the skills against current docs", "sync against WWDC", "update the Apple text skills for the new SDK", "freshen latest-apis.md", or any maintenance trigger. Trigger after WWDC, after Xcode 26.x bumps, or whenever an agent author notices skill content drifting from the current API surface — even when 'maintenance' isn't named. Do NOT use for authoring new skills or rewriting existing ones — that's the job of the per-skill rewrite workflow described in AGENTS.md.
license: MIT
---

# Refresh Apple Text skills against Sosumi

Authored against iOS 26.x / Swift 6.x / Xcode 26.x.

This is a maintenance skill. It produces a diff report against Apple's current documentation; a human maintainer reviews and commits the result. Do not push silent updates without review — Apple sometimes deprecates without changing signatures, and the diff alone won't catch semantic shifts.

## Contents

- [When to run this](#when-to-run-this)
- [Scope: which skills carry latest-apis sidecars](#scope-which-skills-carry-latest-apis-sidecars)
- [Procedure](#procedure)
- [What to look for in the diff](#what-to-look-for-in-the-diff)
- [Common Mistakes](#common-mistakes)
- [References](#references)

## When to run this

The natural cadence is after Apple releases that touch the text stack:

- **Major iOS release** (e.g., iOS 27.0). Always run.
- **Xcode point release** that bumps the SDK (e.g., 26.3 → 26.4). Run if the release notes mention SwiftUI text, AttributedString, TextKit, or Foundation changes.
- **WWDC keynote week.** Run *after* the betas are public, not on keynote day.
- **Spot-check** when an agent or user reports that a skill's API claim no longer compiles — that's evidence of drift, regardless of the calendar.

Don't run this on every commit. The point is to capture deltas at meaningful platform boundaries; running too often produces noise and rebases against an in-flight beta cycle.

## Scope: which skills carry latest-apis sidecars

These five skills are time-sensitive enough to warrant a `references/latest-apis.md` companion. Any of them that lacks the file gets one created on the next run:

- `txt-swiftui-texteditor` — iOS 26+ rich-text TextEditor; `AttributedTextSelection`, `AttributedTextFormattingDefinition`, `AttributedTextValueConstraint`, `transformAttributes(in:body:)`, `replaceSelection(_:withCharacters:)`, `replaceSelection(_:with:)`, `Font.Context`, `Font.resolve(in:)`
- `txt-writing-tools` — `UIWritingToolsCoordinator`, `WritingToolsBehavior`, `WritingToolsAllowedInputOptions`, `writingToolsIgnoredRangesIn`, `isWritingToolsActive`, the willBegin/didEnd lifecycle
- `txt-textkit2` — `NSTextLayoutManager`, `NSTextContentManager`, `NSTextLayoutFragment`, `NSTextLineFragment`, `NSTextViewportLayoutController`, fragment enumeration options
- `txt-attribute-keys` — `NSAttributedString.Key` catalog, value types, view-compatibility footnotes
- `txt-attributed-string` — `AttributedString` API surface, `AttributeScope`, `AttributeContainer`, `MarkdownDecodableAttributedStringKey`, `CodableAttributedStringKey`, scope composition rules

Other skills (`txt-textkit1`, `txt-nstextstorage`, `txt-uitextinput`, etc.) describe stable older APIs and don't carry `latest-apis.md`. They get reviewed during major releases as part of the broader audit, not via this skill.

## Procedure

The work is mechanical — fetch, diff, report — but each step has a gotcha. Apply in order.

### Step 1: Establish baseline

For each in-scope skill, read its current `references/latest-apis.md` (or the SKILL.md if no sidecar exists yet). Capture every Apple API name, signature, and version annotation that appears as a normalized list. This is the baseline.

If a skill doesn't have `references/latest-apis.md`, create one with this template:

```markdown
# Latest API surface — <skill-name>

Authored against iOS 26.x / Swift 6.x / Xcode 26.x. Last refreshed YYYY-MM-DD against Sosumi.

## <Subject group 1>

- `Type.method(arg1:arg2:)` — short description, since: iOS 26.0
- ...

## <Subject group 2>

...

## Signatures verified against Sosumi

| URL | Status | Last fetched |
|---|---|---|
| https://sosumi.ai/documentation/... | 200 | YYYY-MM-DD |
```

Static SKILL.md content stays as the mental model. `latest-apis.md` is the API-signature source of truth.

### Step 2: Fetch current Apple docs

For each API in the baseline, fetch the corresponding Sosumi page. Two routes:

- **MCP server** (preferred when the agent has it configured): call `Sosumi:fetch_documentation` with the API path. Returns clean Markdown.
- **HTTP fetch fallback**: `curl -fsSL https://sosumi.ai/documentation/<framework>/<api>` and parse Markdown.

Verify the URL resolves with HTTP 200 before treating its content as authoritative. A 404 means Apple removed or renamed the symbol — flag for review, don't silently delete from `latest-apis.md`.

If Sosumi itself is down (rare but possible), defer to `xcrun mcpbridge`'s `DocumentationSearch` tool against on-machine Xcode-bundled docs. Note the source in the diff report so the reviewer knows which surface was canonical.

### Step 3: Produce a diff report

For each skill, write a per-skill report at `/tmp/sosumi-refresh-<skill>-<date>.md` containing:

```markdown
# Refresh report: <skill-name> (YYYY-MM-DD)

## New APIs (added since last refresh)
- `Type.newMethod(...)` since iOS 26.x
  - Sosumi: <url>
  - Suggested home in latest-apis.md: <subject group>

## Deprecated / removed APIs
- `Type.oldMethod(...)` deprecated in iOS 26.x, removed in iOS 27.x
  - Migration: see "Old patterns" section per AGENTS.md freshness contract

## Signature changes
- `Type.changedMethod(...)`
  - Was: `(arg1: A, arg2: B) -> R`
  - Now: `(arg1: A, arg2: B?, completion: ...) -> R`
  - Source: <sosumi url>

## URL liveness
- <url>: 200
- <url>: 404 (was 200 last refresh — investigate)

## Suggested edits
[per-section guidance for the human reviewer]
```

Don't auto-apply. The report is for human review.

### Step 4: Apply approved changes

Once the maintainer reviews, apply edits:

- **Add new APIs** to `latest-apis.md` under the right subject group with `since: iOS X.x`.
- **Mark deprecated APIs** in a collapsed `## Old patterns` section per AGENTS.md freshness contract — never inline date conditionals like "if before iOS 26".
- **Update signature changes** in `latest-apis.md`, then check whether SKILL.md references the old shape; update if so.
- **Update the "Last refreshed" timestamp** at the top of `latest-apis.md`.

Commit each skill's update as a separate commit so the history reads cleanly.

### Step 5: Update the freshness banner

If a major release happened (iOS 27.x), update the `Authored against iOS 26.x / Swift 6.x / Xcode 26.x.` line in each refreshed skill's SKILL.md to the new versions. Don't update minor revs (26.3 → 26.4) — those would churn the line on every Xcode point release. Use major boundaries.

## What to look for in the diff

Spot the patterns that aren't pure additions:

- **Renamed type or symbol.** Sosumi will return 404 for the old path and 200 for the new one. The diff report should pair them; treat as a migration entry, not a deletion.
- **Parameter widening or new defaults.** Old call sites still compile but the new shape is preferred. Update the signature in `latest-apis.md` and add a note explaining when to use which form.
- **Availability annotation changes.** A method that was iOS 26.0+ might get backported to 17.0+ in a point release, or vice versa. The since-annotation is part of the source of truth, not just the signature.
- **New protocol conformance** (e.g., `AttributedString` gaining `Sendable`). These don't show up as new API names but unlock new patterns. Flag in the report's "Suggested edits" section.
- **Deprecation reasons.** Sosumi pages include deprecation messages. Capture the *reason* in the report, not just the deprecation flag — that determines whether to suggest a migration or leave the old API documented for legacy callers.

## Common Mistakes

1. **Running on beta-day instead of after public release.** Beta APIs churn and the report becomes noise. Wait until the SDK ships in a public Xcode update.

2. **Treating Sosumi 404 as "API was removed."** Sosumi sometimes lags Apple's renames or restructures by a day or two. Cross-check with `xcrun mcpbridge` or the live `developer.apple.com` page (in a browser, not via fetch) before assuming removal.

3. **Auto-applying changes from the diff report.** The whole point of producing a report is to give a maintainer a chance to spot semantic shifts that signature diffing misses. A method that gained a new parameter often has new behavior the diff alone won't reveal.

4. **Forgetting to bump the freshness banner after a major release.** A skill that says "Authored against iOS 26.x" when iOS 27 has shipped misleads downstream agents. Bumping is part of the procedure, not optional.

5. **Updating SKILL.md instead of `latest-apis.md`.** The static skill content is supposed to age slowly; it explains mental models, not signatures. Rapid-churn signatures live in the sidecar so the SKILL.md remains stable across point releases. If a SKILL.md update is genuinely warranted, that's a separate edit, not part of this refresh.

6. **Writing the diff report straight into the repo.** Reports are ephemeral. Write to `/tmp/` (or a `refresh-reports/` directory git-ignored at the repo root) so the repo doesn't accumulate stale audit trails.

## References

- `txt-apple-docs` — the documentation-pipe skill: how to invoke Sosumi MCP and `xcrun mcpbridge` from agents
- `AGENTS.md` — repo-level authoring rules including the freshness contract that this skill operationalizes
- [Sosumi.ai](https://sosumi.ai/) — the documentation mirror
- [Apple Developer: Giving external agents access to Xcode](https://sosumi.ai/documentation/xcode/giving-external-agents-access-to-xcode) — `xcrun mcpbridge` setup and tool reference
