---
name: txt-measurement
description: Measure rendered size of strings and attributed strings, size views to fit text content, and read per-line metrics from NSLayoutManager and NSTextLayoutManager. Covers boundingRect with NSStringDrawingOptions, NSStringDrawingContext for auto-shrink, sizeThatFits, intrinsicContentSize, usedRect, enumerateLineFragments, usageBoundsForTextContainer, line-fragment typographic bounds, and the lineFragmentPadding/textContainerInset arithmetic that makes measurements match what UITextView actually renders. Use when text clips by a pixel, boundingRect returns a single-line size for multi-line text, a self-sizing UITextView refuses to size, intrinsicContentSize is wrong, or the user needs line counts. Do NOT use for paragraph style, hyphenation, or line height — see txt-line-breaking. Do NOT use for layout invalidation timing — see txt-layout-invalidation.
license: MIT
---

# Text Measurement

Authored against iOS 26.x / Swift 6.x / Xcode 26.x.

Measuring text means asking the typesetter how big a string will be once it lays it out. The right question — single-line size, constrained-width multi-line size, per-line metrics, fit-to-content sizing — picks the right API. The wrong question silently returns a number that disagrees with what UITextView later renders, and the difference is usually 1-2 pixels of clipping. The patterns here are starting points; before quoting any specific API signature, fetch the current Apple docs via Sosumi (`sosumi.ai/documentation/foundation/nsattributedstring/boundingrect(with:options:context:)`) and check that the call site uses the same font, paragraph style, and container insets that the rendering path uses — most measurement bugs are an attribute mismatch, not an API misuse.

The measurement and the render must agree on every relevant attribute: font, line height, line break mode, container width minus `lineFragmentPadding`, and `textContainerInset`. A measurement that uses default attributes against a render that uses a customized paragraph style produces predictable disagreement.

## Contents

- [boundingRect: the workhorse](#boundingrect-the-workhorse)
- [Single-line measurement](#single-line-measurement)
- [Auto-shrink with NSStringDrawingContext](#auto-shrink-with-nsstringdrawingcontext)
- [TextKit 1 per-line metrics](#textkit-1-per-line-metrics)
- [TextKit 2 per-line metrics](#textkit-2-per-line-metrics)
- [Sizing views to fit content](#sizing-views-to-fit-content)
- [Common Mistakes](#common-mistakes)
- [References](#references)

## boundingRect: the workhorse

`boundingRect(with:options:context:)` is the right answer for "how big is this attributed string when wrapped to width W." Multi-line measurement requires `.usesLineFragmentOrigin`. Without it, the call measures as a single line ignoring the width constraint, which is the single most common measurement bug. Pair it with `.usesFontLeading` so the height includes the leading the renderer will add — without it the measurement comes back consistently shorter than the rendered text and the next line below clips.

```swift
let rect = attributedString.boundingRect(
    with: CGSize(width: maxWidth, height: .greatestFiniteMagnitude),
    options: [.usesLineFragmentOrigin, .usesFontLeading],
    context: nil)
let measured = CGSize(width: ceil(rect.width), height: ceil(rect.height))
```

`ceil()` is mandatory. The returned rect is fractional. Passing a fractional height to a layout that snaps to integer points clips the descender of the last line. Round up.

The other options are situational. `.usesDeviceMetrics` swaps typographic bounds for actual glyph bounds — useful for pixel-perfect rendering checks, almost never for layout sizing. `.truncatesLastVisibleLine` tells the measurement to apply truncation when the proposed height is the constraint; use this when you constrain height and want the truncated size, not the full content size.

## Single-line measurement

`NSAttributedString.size()` and `NSString.size(withAttributes:)` always return single-line sizes. They ignore any width constraint. Using them for a multi-line label is the bug behind half of "label clips at the bottom" tickets. They are the right answer for badges, single-line chrome, or a width-only check before a multi-line call.

## Auto-shrink with NSStringDrawingContext

For UILabel-style auto-shrink, pass an `NSStringDrawingContext` with `minimumScaleFactor`. After the call, read `actualScaleFactor` for the scale the typesetter used and `totalBounds` for where text actually landed:

```swift
let ctx = NSStringDrawingContext()
ctx.minimumScaleFactor = 0.5

let rect = attributedString.boundingRect(
    with: constrained,
    options: [.usesLineFragmentOrigin, .usesFontLeading],
    context: ctx)

let scale = ctx.actualScaleFactor
let bounds = ctx.totalBounds
```

The shrink only triggers when the unscaled text would not fit; a shrunk-and-fits result is in `totalBounds`, not the returned rect.

`minimumScaleFactor` is single-line in practice. UILabel honors it for one-line text; multi-paragraph or wrap-mode strings ignore it, and `actualScaleFactor` reads back as 1.0 even when the text clips. Once an `NSParagraphStyle` is attached to the run — line height, line break mode, anything paragraph-level — the typesetter often refuses to scale at all (radar://26575435). The reliable path for multi-line shrink-to-fit is to measure at the unscaled font, compute the ratio against the available size yourself, and re-render at a smaller font size. `boundingRect` with `NSStringDrawingContext` is correct for the single-line case; for multi-line, treat its `actualScaleFactor` as advisory at best. See `/skill txt-line-breaking` for the paragraph-style interaction.

## TextKit 1 per-line metrics

When the question is per-line — line counts, line heights, the y-coordinate of the third line — `boundingRect` is too coarse. NSLayoutManager has the metrics. Force layout first, then read; layout is lazy and queries before layout return stale data.

```swift
layoutManager.ensureLayout(for: textContainer)
let usedRect = layoutManager.usedRect(for: textContainer)
```

`usedRect` is the actual area glyphs occupy; the container's full size is the upper bound. For per-line enumeration, walk fragments:

```swift
let fullRange = layoutManager.glyphRange(for: textContainer)
layoutManager.enumerateLineFragments(forGlyphRange: fullRange) {
    rect, usedRect, container, glyphRange, stop in
    // rect: full line fragment (includes leading/trailing padding)
    // usedRect: glyph bounds (tighter)
}
```

For a line count, the same enumeration is the simplest answer — increment a counter inside the closure. There is no `numberOfLines` getter on the layout manager.

## TextKit 2 per-line metrics

TextKit 2 uses `usageBoundsForTextContainer` for total content bounds and `enumerateTextLayoutFragments` for per-fragment metrics. A layout fragment may contain multiple line fragments (`textLineFragments`); a typical paragraph has one layout fragment containing several line fragments.

```swift
textLayoutManager.ensureLayout(for: textLayoutManager.documentRange)
let total = textLayoutManager.usageBoundsForTextContainer

textLayoutManager.enumerateTextLayoutFragments(
    from: textLayoutManager.documentRange.location,
    options: [.ensuresLayout]
) { fragment in
    let frame = fragment.layoutFragmentFrame
    for line in fragment.textLineFragments {
        let bounds = line.typographicBounds
        // line origin is fragment.frame.origin + bounds.origin
    }
    return true
}
```

`enumerateTextLayoutFragments` over the full document defeats the viewport optimization that makes TK2 fast for long documents. If the work needs all fragments, accept the cost; if it only needs visible fragments, scope the enumeration to the viewport.

## Sizing views to fit content

For UITextView, the supported path is `isScrollEnabled = false` plus Auto Layout. With scrolling enabled, `intrinsicContentSize` returns `(.noIntrinsicMetric, .noIntrinsicMetric)` and the view will not size itself. With scrolling disabled, `intrinsicContentSize` returns the full content size and Auto Layout drives the height.

```swift
textView.isScrollEnabled = false
// Auto Layout uses intrinsicContentSize from here on
```

For frame-based layout, ask `sizeThatFits`:

```swift
let fitting = textView.sizeThatFits(
    CGSize(width: maxWidth, height: .greatestFiniteMagnitude))
textView.frame.size.height = fitting.height
```

UITextView adds two amounts on top of the raw text size: `textContainerInset` (default `(8, 0, 8, 0)`) and `lineFragmentPadding` (default 5pt each side). A measurement that ignores either undercuts the actual rendered size:

```swift
let textWidth = container.size.width - 2 * container.lineFragmentPadding
// height of measured text + textView.textContainerInset.top + textView.textContainerInset.bottom
```

For UILabel, `intrinsicContentSize` is reliable; the label internally uses `boundingRect` with the right options.

## Common Mistakes

1. **Missing `.usesLineFragmentOrigin`.** Without it, `boundingRect` measures as a single line and ignores the width constraint. The returned width matches the full string laid out without wrapping; the height is one line. Always include the option for multi-line measurement.

2. **Missing `.usesFontLeading`.** The default measurement omits the font's leading, so the height is consistently shorter than the rendered text. The next view below the label gets clipped from the top. Include the option to match the renderer.

3. **Not calling `ceil()` on the result.** `boundingRect` returns fractional values. A 24.7-point measurement assigned to a 24-point integer-rounded layout clips the last descender. Round up.

4. **Measuring with attributes that disagree with the render.** Default attributes for measurement, customized paragraph style for render — or vice versa — produces a measurement that is correct in isolation and wrong in context. Use the *same* attributes that the rendering path uses, including paragraph style and any overrides.

5. **Forgetting `lineFragmentPadding` and `textContainerInset`.** UITextView's default container subtracts 10pt of horizontal padding (5pt each side) from the usable width, and the view adds 16pt of vertical inset (8pt top + 8pt bottom). A measurement against the raw view bounds is off by these amounts.

6. **Reading layout-manager metrics without forcing layout.** TextKit layout is lazy. `usedRect`, `lineFragmentRect`, and `glyphRange` queries before the next layout pass return values from the previous layout. Call `ensureLayout(for:)` (TK1) or `ensureLayout(for: documentRange)` (TK2) before reading.

7. **Single-line APIs used for multi-line text.** `NSAttributedString.size()` and `NSString.size(withAttributes:)` ignore width constraints and return one-line sizes. They are the right answer for badges and single-line chrome, never for paragraphs.

8. **Self-sizing UITextView with `isScrollEnabled = true`.** With scrolling enabled, `intrinsicContentSize` returns no intrinsic metrics and Auto Layout cannot size the view. Disable scrolling for self-sizing; re-enable only when content exceeds the cap.

9. **Measurement on a background thread.** All TextKit measurement APIs that touch a layout manager must run on the main thread (or, for TK2, the layout queue). Background measurement crashes sporadically with no obvious frame in the offending code.

10. **Trusting `actualScaleFactor` on multi-line text.** `NSStringDrawingContext.minimumScaleFactor` is effectively single-line. Multi-paragraph or wrap-mode strings ignore the shrink; `actualScaleFactor` reads back as 1.0 even when the rendered text clips, and an attached `NSParagraphStyle` defeats it further (radar://26575435). For multi-line auto-shrink, measure at the base font, compute the ratio yourself, and re-render at a smaller size — don't rely on `actualScaleFactor`. See `/skill txt-line-breaking` for the paragraph-style interaction.

## References

- `/skill txt-line-breaking` — paragraph style decisions that change measurement results
- `/skill txt-layout-invalidation` — `ensureLayout` semantics and what makes prior measurements stale
- `/skill txt-viewport-rendering` — viewport-scoped TK2 measurement for long documents
- `/skill txt-core-text` — glyph-level measurement when typesetter-level measurement is not enough
- [NSAttributedString.boundingRect](https://sosumi.ai/documentation/foundation/nsattributedstring/boundingrect(with:options:context:))
- [NSLayoutManager](https://sosumi.ai/documentation/uikit/nslayoutmanager)
- [NSTextLayoutManager](https://sosumi.ai/documentation/uikit/nstextlayoutmanager)
