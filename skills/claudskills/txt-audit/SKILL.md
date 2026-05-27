---
name: txt-audit
description: Review Apple text code for correctness, performance, and modernization risk in a single pass with severity-ranked findings. Covers TextKit 1 fallback triggers, NSTextStorage subclass correctness (edited / changeInLength / batched edits), didProcessEditing character-mutation bugs, deprecated glyph APIs, full-document ensureLayout, missing allowsNonContiguousLayout, NSLinguisticTagger / UIMenuController deprecations, missing performEditingTransaction wrappers on TextKit 2, Writing Tools coordinator gaps (writingToolsIgnoredRangesIn, isWritingToolsActive), String-vs-NSString length confusion in range arithmetic, and main-thread storage rules. Use when a user asks to audit, scan, or review a text editor codebase, when preparing an editor for shipping, when triaging a post-release regression in TextKit code, or when a pull request needs a structured pass focused on text-specific risks.
license: MIT
---

# Apple text audit

Authored against iOS 26.x / Swift 6.x / Xcode 26.x.

This skill drives a fixed-procedure code review: scan the repo for known TextKit, text-input, and Writing Tools risks, rank findings by severity, and report. It's the only skill in this set with a checklist — auditing is a procedure, not a diagnostic exploration. The checklist below is rooted in observed bugs from the other skills; before flagging an item as a finding, open the actual source and confirm the code matches the pattern. Severity is calibrated to *user-visible impact*: P0 means crashes, data loss, or broken behavior; P1 means correctness or performance regressions; P2 means modernization and maintainability. If a TextKit 2 view falls back to TextKit 1 because of one line in a third-party dependency, that's still P0 — Writing Tools degrades and the regression is shipped.

## Contents

- [Scope](#scope)
- [Review Checklist](#review-checklist)
- [Reporting findings](#reporting-findings)
- [Common Mistakes](#common-mistakes)
- [References](#references)

## Scope

Audit the Apple text system code in `$ARGUMENTS`. If no arguments are supplied, audit the current workspace for TextKit, UIKit/AppKit text-view, text-input, and Writing Tools issues.

The checklist is an audit pass, not a debugging guide. For symptom-driven debugging where the user starts with broken behavior, route to `txt-textkit-debug`. For the picker decision between TextKit 1 and TextKit 2, route to `txt-textkit-choice`. For the API reference of either stack, route to `txt-textkit1` or `txt-textkit2`.

Scope of a single pass:

- Swift and Objective-C source under the project root.
- Third-party Swift Package Manager dependencies (look for `.layoutManager` access in transitive deps as a fallback risk).
- The text-storage subclasses, text-view controllers, and any class implementing `NSTextStorageDelegate` or `UITextViewDelegate`.
- Out of scope unless explicitly requested: localized strings, asset catalogs, generated code.

## Review Checklist

Walk the items in order. Skip items that don't apply. Each item names a sibling skill where the underlying behavior is documented in depth.

### P0 — broken behavior, crashes, data loss

**1. TextKit 1 fallback triggers.** Search for `.layoutManager` access on `UITextView` or `NSTextView`, including `textContainer.layoutManager`. Any access without a preceding `textLayoutManager == nil` check forces an irreversible fallback to TextKit 1 and breaks Writing Tools inline behavior, viewport layout, and view-based attachments. Audit transitive dependencies, not just app code — many third-party UITextView extensions written before iOS 16 access `layoutManager` unconditionally. Reference: `txt-fallback-triggers`.

**2. Missing `edited()` in `NSTextStorage` subclasses.** Every override of `replaceCharacters(in:with:)` and `setAttributes(_:range:)` must call `edited(_:range:changeInLength:)` with the right mask and delta. Without it, layout managers never learn about changes and the visible symptom is "edit went through but the view didn't update". Reference: `txt-nstextstorage`.

**3. Character mutation in `didProcessEditing`.** The `didProcessEditing` delegate runs after the storage has committed; ranges captured before are stale; mutating characters re-enters the editing lifecycle and crashes. Move character changes to `willProcessEditing`, or restrict the delegate to attribute-only changes. Reference: `txt-nstextstorage`.

**4. Wrong `changeInLength` units.** The delta passed to `edited()` must be NSString length (UTF-16), not Swift `String.count`. They diverge on emoji, ZWJ sequences, and combining marks. Mixing them corrupts the bookkeeping silently — subsequent edits clobber data and "range out of bounds" crashes appear far from the actual bug. Look for `(str as NSString).length - range.length` patterns; flag any `str.count - range.length` in mutation primitives. Reference: `txt-nstextstorage`.

**5. Missing `beginEditing()` / `endEditing()` around batched mutations.** Without batching, each mutation triggers a separate `processEditing()` pass. Beyond the performance hit, ranges captured outside the batch can shift mid-batch as earlier mutations change content; "range out of bounds" crashes during multi-step updates are usually unbatched mutations.

**6. Background-thread `NSTextStorage` access.** Main-thread-confined. Background mutations crash sporadically with no obvious stack frame in the offending code. Look for `DispatchQueue.global` or `Task.detached` blocks that touch text storage; any of those is a P0 unless the surrounding code hops back to main before the mutation.

### P1 — correctness, deprecation, performance

**7. Deprecated glyph APIs without a TextKit 1 guard.** `glyph(at:)`, `glyphRange(forCharacterRange:actualCharacterRange:)`, `numberOfGlyphs`, `drawGlyphs(forGlyphRange:at:)`, `lineFragmentRect(forGlyphAt:effectiveRange:)` are TextKit 1 only. Calling any of them without confirming the editor is on TextKit 1 (via `textLayoutManager == nil`) crashes or silently fails on TextKit 2. Reference: `txt-textkit1`.

**8. `ensureLayout(for: textContainer)` on large documents.** Forces full-document layout — O(document). Use the rect-scoped variant `ensureLayout(forBoundingRect:in:)` over the visible rect, or the range-scoped `ensureLayout(forCharacterRange:)`. Reference: `txt-layout-invalidation`.

**9. Full-document enumeration with `.ensuresLayout` on TextKit 2.** `enumerateTextLayoutFragments(from: documentRange.location, options: [.ensuresLayout])` defeats the viewport optimization. Either drop `.ensuresLayout` or limit the range to the viewport. Reference: `txt-textkit2`.

**10. Missing `allowsNonContiguousLayout` on TextKit 1.** Large documents need it for acceptable scroll performance. `UITextView` enables it by default; `NSTextView` and custom views built on `NSLayoutManager` directly do not. Reference: `txt-textkit1`.

**11. `NSLinguisticTagger` usage.** Replaced by the `NaturalLanguage` framework. Deprecated since iOS 14. Migrate to `NLTagger` / `NLTokenizer`.

**12. Old `UIMenuController` usage.** Replaced by `UIEditMenuInteraction` in iOS 16. Migrate selection menus to the new interaction.

**13. Direct `NSTextStorage` mutations on TextKit 2 without `performEditingTransaction`.** The element tree may not regenerate; the view shows stale content. Wrap all mutations in `contentStorage.performEditingTransaction { … }`. Reference: `txt-nstextstorage`.

**14. Setting fonts in `didProcessEditing`.** Bypasses `fixAttributes` font substitution. Characters with no glyph in the font render as `.notdef` boxes. Move font changes to `willProcessEditing`, or supply explicit fallback fonts in the attribute. Reference: `txt-viewport-rendering`.

### P2 — compatibility, maintainability

**15. Explicit TextKit 1 creation without a documented reason.** `UITextView(usingTextLayoutManager: false)` is the right call when the feature requires glyph access, multi-container layout, `NSTextTable`, or reliable temporary attributes. Without one of those reasons, the view is missing Writing Tools inline and viewport optimization for no benefit. Reference: `txt-textkit-choice`.

**16. Missing `writingToolsIgnoredRangesIn` for code or quote content.** Code blocks and blockquotes should be excluded from Writing Tools rewrites. The default behavior rewrites everything, which corrupts code samples in mixed content.

**17. No `isWritingToolsActive` check before programmatic text changes.** Programmatic edits during a Writing Tools session can corrupt the rewrite. Guard programmatic mutations with the active-state check, or defer them.

**18. `String.count` vs `NSString.length` confusion in range calculations.** `String.count` counts grapheme clusters; `NSString.length` counts UTF-16 code units. Mixing them produces wrong ranges, especially with emoji and complex scripts. Look for arithmetic on `string.count` immediately mixed with `NSRange` values; flag for normalization through `NSRange(swiftRange, in: text)` or `(text as NSString).length`.

**19. Setting transient visual effects (find highlight, transient selection) via `textStorage.addAttribute`.** Modifies the document; persists into copy/paste, undo, and serialization. Use temporary attributes (TextKit 1) or rendering attributes (TextKit 2) for visual-only overlays. Reference: `txt-viewport-rendering`.

**20. `drawInsertionPoint(in:color:turnedOn:)` override on `NSTextView`.** Doesn't trigger fallback, but silently stops being called under TextKit 2. Custom cursor drawing disappears. If the override is present, confirm the view is on TextKit 1 (`UITextView(usingTextLayoutManager: false)` equivalent for NSTextView), or rewrite via `NSTextSelectionDisplayInteraction` / a custom layout fragment.

## Reporting findings

Group findings by severity. For each finding, give a file and line reference, a one-sentence description of the issue, and a one-sentence fix. If the same root cause appears at multiple sites, group them under one finding with the call sites listed underneath.

```
## TextKit Audit Results

### P0 — Critical
- Sources/Editor/TextStorage.swift:42
  Missing edited(_:range:changeInLength:) call in replaceCharacters override.
  Fix: call edited(.editedCharacters, range: range, changeInLength: delta) where delta is (str as NSString).length - range.length.

### P1 — Important
- Sources/Editor/SyntaxHighlighter.swift:88
  layoutManager.ensureLayout(for: textContainer) on a 50K-line document.
  Fix: use ensureLayout(forBoundingRect: visibleRect, in: textContainer) over the visible rect.

### P2 — Improvement
- Sources/Editor/SelectionMenu.swift:14
  Uses UIMenuController; deprecated in iOS 16.
  Fix: migrate to UIEditMenuInteraction.

### Summary
- 17 files scanned
- 5 issues found (1 P0, 2 P1, 2 P2)
- Blind spots: no Objective-C files in scope; Writing Tools configuration not present in this target
```

If no issues are found, say so explicitly and call out residual blind spots — files not scanned, areas the checklist didn't cover, places where confidence is low.

## Common Mistakes

1. **Reporting findings without confirming the code path.** The checklist describes patterns; an actual finding requires the source to match. A `String.count` in arithmetic that never reaches a layout API isn't a bug. Open the file, walk the call site, then report.

2. **Conflating fallback risk with fallback occurrence.** `.layoutManager` access in dead code or behind a `textLayoutManager == nil` guard is not a P0 finding. The risk applies when the access can run on a TextKit 2 view.

3. **Listing every dependency that mentions `layoutManager`.** Many dependencies have read-only diagnostics or use `layoutManager` only after confirming TextKit 1. Flag actual unguarded accesses, not every match for the symbol.

4. **Treating TextKit 1 use as a P1 deprecation.** TextKit 1 is supported and not deprecated; Apple's own apps still use it. The P2 finding (#15) is "explicit TextKit 1 without a documented reason," not "TextKit 1 is bad". If the reason is in scope of the codebase (glyph access, multi-container, tables, syntax highlighting), the finding doesn't apply.

5. **Reporting `ensureLayout(for: textContainer)` as P0.** It's a performance issue, not a correctness one. P1, with a fix to scope the layout call. The same with `.ensuresLayout` enumerations and missing `allowsNonContiguousLayout`.

6. **Skipping the summary's "blind spots" line.** A clean audit with no blind spots called out is suspicious. Note files or areas the checklist didn't cover so the reader knows what was and wasn't reviewed.

## References

- `txt-textkit-debug` — symptom-driven debugging when the user starts with broken behavior, not a code review request
- `txt-fallback-triggers` — full TextKit 1 fallback trigger catalog (drives finding #1)
- `txt-nstextstorage` — storage subclassing and editing lifecycle (drives findings #2-#5, #13)
- `txt-layout-invalidation` — invalidation model (drives findings #8, #9)
- `txt-textkit-choice` — TK1 vs TK2 picker (drives finding #15)
- `txt-textkit1` — TextKit 1 API reference (drives findings #7, #10)
- `txt-textkit2` — TextKit 2 API reference (drives findings #9, #13)
- `txt-viewport-rendering` — fragment geometry and font substitution (drives findings #14, #19)
- [NSTextStorage](https://sosumi.ai/documentation/uikit/nstextstorage)
- [NSTextLayoutManager](https://sosumi.ai/documentation/uikit/nstextlayoutmanager)
- [UIWritingToolsCoordinator](https://sosumi.ai/documentation/uikit/uiwritingtoolscoordinator)
