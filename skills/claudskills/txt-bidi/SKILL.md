---
name: txt-bidi
description: Handle bidirectional text, right-to-left languages, mixed Arabic/Hebrew/Latin content, writing-direction APIs at every layer, and cursor/selection behavior in bidi text. Covers NSParagraphStyle.baseWritingDirection, the .writingDirection attributed-string key with embedding/override modes, AttributedString.writingDirection, UITextInput.setBaseWritingDirection, SwiftUI .environment(\.layoutDirection), iOS 26 Natural Selection (selectedRanges), Unicode bidi controls (LRM/RLM/LRE/RLE/PDF/FSI/PDI), .natural vs .left/.right alignment, and visual vs logical order. Use when adding RTL support, debugging cursor jumps in mixed content, fixing phone numbers that reorder in Arabic context, migrating to selectedRanges, or making a custom UITextInput view bidi-correct. Trigger on Arabic, Hebrew, RTL, or "cursor moves wrong" even without bidi APIs named. Do NOT use for general localization or locale-aware formatting (out of scope for this repo).
license: MIT
---

# Bidirectional Text and RTL

Authored against iOS 26.x / Swift 6.x / Xcode 26.x.

Bidi correctness is layered. SwiftUI's environment, NSParagraphStyle, the `.writingDirection` attribute, UITextInput, and NSTextContainer each control direction at a different scope; getting RTL right usually means getting the right layer involved, not all of them. The single concept that explains most bidi bugs is the gap between **logical order** (how characters live in storage) and **visual order** (how they end up on screen after the Unicode Bidi Algorithm reorders them) — a single logical position can map to two visual positions at a direction boundary, which is why cursors appear to jump. The patterns below are starting points; before quoting any specific API signature, fetch the current Apple docs via Sosumi (`sosumi.ai/documentation/uikit/uitextinput`) and verify against the actual code, especially when the question involves cursor movement.

Stock UITextView and UITextField handle bidi correctly with `.natural` writing direction. Most "bidi is broken" reports against stock views turn out to be `.left` alignment hardcoded somewhere, or a phone number reordering because no LRM was added. Custom UITextInput views handle bidi only as well as their author writes it.

## Contents

- [Direction control by layer](#direction-control-by-layer)
- [Visual versus logical order](#visual-versus-logical-order)
- [Mixed-direction content](#mixed-direction-content)
- [iOS 26 Natural Selection](#ios-26-natural-selection)
- [Alignment in RTL](#alignment-in-rtl)
- [Common Mistakes](#common-mistakes)
- [References](#references)

## Direction control by layer

**SwiftUI environment.** The top-level switch for a SwiftUI hierarchy. Reading `@Environment(\.layoutDirection)` gives the current direction; `.environment(\.layoutDirection, .rightToLeft)` forces it on a subtree. SwiftUI `Text` ignores the `.writingDirection` attributed-string key, so direction control in SwiftUI happens through the environment, not through attributes.

```swift
VStack { ... }
    .environment(\.layoutDirection, .rightToLeft)

Image("arrow")
    .flipsForRightToLeftLayoutDirection(true)
```

**NSParagraphStyle.baseWritingDirection.** The most common control for an attributed string. `.natural` defers to the Unicode Bidi Algorithm rules P2/P3, which pick direction from the first strong directional character. `.leftToRight` and `.rightToLeft` force it. Forcing direction is appropriate when you know the content's language; `.natural` is appropriate for user-supplied text of unknown direction.

**.writingDirection attribute.** For inline overrides within a paragraph, equivalent to Unicode bidi control sequences (LRE/RLE/PDF). The value is an array of `NSNumber` packing direction and format type:

```swift
let ltrEmbed: [NSNumber] = [
    NSNumber(value: NSWritingDirection.leftToRight.rawValue
                  | NSWritingDirectionFormatType.embedding.rawValue)
]
attrString.addAttribute(.writingDirection, value: ltrEmbed, range: range)
```

`.embedding` respects each character's inherent directionality within the override (the typesetter still bidis inside). `.override` forces every character to display in the named direction regardless of inherent direction — used rarely, mostly for showing raw bidi-control text literally.

**UITextInput.** Custom text views set per-range direction at runtime via `setBaseWritingDirection(_:for:)` and read it via `baseWritingDirection(for:in:)`. These methods drive marked text and selection in bidi content; a UITextInput implementation that returns a stale direction will show the cursor in the wrong place.

**AttributedString (iOS 26+).** `AttributedString.writingDirection` exposes the same control as a typed property: `.leftToRight` or `.rightToLeft`.

**NSTextContainer.** `lineFragmentRect(forProposedRect:at:writingDirection:remaining:)` takes the writing direction as a parameter — line fragments advance from the leading edge in that direction. A custom container subclass that ignores the parameter produces lines that advance the wrong way in RTL.

## Visual versus logical order

Logical order is storage order. In a string like `"Hello مرحبا World"`, the Arabic word's characters are stored in their natural reading order (right-to-left in Arabic, which is left-to-right in the string buffer). Visual order is what appears on screen after the Bidi Algorithm reorders the Arabic run to display right-to-left while leaving the Latin runs left-to-right.

A consequence of this gap: **a single cursor position can map to two visual positions** at a direction boundary. Place the caret between the last Latin character and the first Arabic character, and the caret can legitimately appear at the right edge of the Latin run *or* at the left edge of the Arabic run. Pre-iOS 26 selection uses a single contiguous NSRange that follows logical order, so a selection that spans a direction boundary appears visually disjoint — the user sees two highlighted regions for one selection.

Cursor movement in bidi content is therefore inherently non-linear. Right-arrow in mixed content does not always move the visual cursor right. The user's expectation tracks the system's; what looks wrong is usually a UITextInput view that doesn't honor visual movement.

## Mixed-direction content

The Unicode Bidi Algorithm decides direction from the first strong directional character. Numbers and weak characters inherit direction from the surrounding run, which is the source of most "phone number reordered" bugs. The fix is an inline marker:

```swift
// Wrap LTR content inside RTL with LRM markers
let phone = "\u{200E}555-1234\u{200E}"
let line = "اتصل بـ \(phone)"
```

The relevant control characters:

| Char    | Name | Use |
|---------|------|-----|
| U+200E  | LRM (Left-to-Right Mark) | Invisible LTR direction marker |
| U+200F  | RLM (Right-to-Left Mark) | Invisible RTL direction marker |
| U+202A  | LRE (Left-to-Right Embedding) | Start an LTR embedding |
| U+202B  | RLE (Right-to-Left Embedding) | Start an RTL embedding |
| U+202C  | PDF (Pop Directional Formatting) | End an LRE/RLE |
| U+2068  | FSI (First Strong Isolate) | Start an isolate using first-strong direction |
| U+2069  | PDI (Pop Directional Isolate) | End an FSI |

For unknown-direction user content (a username, a title), wrap with FSI/PDI rather than picking a direction:

```swift
let displayName = "\u{2068}\(user.name)\u{2069}"
```

Isolates are preferable to embeddings in modern code: they prevent the inner text from interfering with the surrounding paragraph's bidi resolution, which is almost always what you want.

## iOS 26 Natural Selection

Pre-iOS 26, `selectedRange` is a single NSRange. In bidi text that spans a direction boundary, this produces visually disjoint selections. iOS 26 introduces `selectedRanges: [NSRange]` on UITextView — multiple visually contiguous ranges that together represent the user's selection. The companion delegate method is `textView(_:shouldChangeTextInRanges:replacementStrings:)`.

```swift
textView.selectedRanges  // [NSRange]

func textView(_ textView: UITextView,
              shouldChangeTextInRanges ranges: [NSRange],
              replacementStrings: [String]?) -> Bool {
    return true
}
```

Natural Selection requires TextKit 2. Touching `textView.layoutManager` flips the view to TextKit 1 and disables it. The single-range `selectedRange` still works for source compatibility; it will be deprecated in a future release.

## Alignment in RTL

`.natural` alignment flips with the writing direction: leading-aligned in LTR, trailing-aligned in RTL. `.left` and `.right` are absolute and do not flip. Hardcoded `.left` is the common bug — labels stay left-aligned in an Arabic locale instead of flipping. The fix is `.natural` for body text, leading/trailing constraints for layout.

In a UIKit view inside an Arabic locale, leading is right and trailing is left. SwiftUI's `.leading` and `.trailing` alignments behave the same way. A constraint pinned to `.leading` of the superview lands on the right edge in RTL — the right answer. A constraint pinned to `.left` lands on the left edge in either locale — almost never the right answer.

## Common Mistakes

1. **Hardcoded `.left` or `.right` alignment.** Absolute alignments do not flip. Body text should use `.natural`; layout should use leading/trailing. The symptom is text that looks right in English and stays left-aligned in Arabic.

2. **Phone numbers and digit runs reordering in RTL.** Without an LRM marker, digits inherit from the surrounding RTL run and reorder. Wrap the digit run with LRM (`\u{200E}`) on each side, or with FSI/PDI for unknown-direction content. The same applies to URLs, email addresses, and code identifiers embedded in Arabic or Hebrew prose.

3. **Forgetting that SwiftUI ignores `.writingDirection`.** The attributed-string key is silently ignored by SwiftUI Text. Direction control in SwiftUI flows through the environment (`\.layoutDirection`) or through `AttributedString.writingDirection` on iOS 26+.

4. **Expecting cursor movement to be linear in bidi text.** At direction boundaries, a single logical position maps to two visual positions, and right-arrow does not always move the visual cursor right. A UITextInput view that does not honor visual cursor movement appears broken; the bug is usually in the view, not the input.

5. **Single `selectedRange` in bidi content.** A storage-contiguous range across a direction boundary is visually disjoint — two highlighted bands for one logical selection. Adopt `selectedRanges` on iOS 26+; accept the visual artifact on older OSes or build a custom selection layer.

6. **TextKit 1 used for an editor that needs Natural Selection.** Touching `textView.layoutManager` falls the view back to TextKit 1, which disables `selectedRanges` and any TK2-only direction handling. Audit for any code path that asks for `layoutManager` on a view that should be TK2; replace with `textLayoutManager` or with viewport-aware APIs.

7. **In-app language switching that does not update text direction.** Programmatic locale changes do not reliably propagate to existing text views. The system reacts to system-level language changes; in-app locale switches need view-level direction setting (paragraph style or environment) plus a layout pass.

8. **NSTextView refusing direction change on macOS.** `makeTextWritingDirectionRightToLeft(_:)` requires the view to be first responder and editable. Calling it from elsewhere silently fails.

9. **TextKit 1 glyph rects wrong for RTL.** Some `NSLayoutManager` rect APIs return incorrect geometry for RTL ranges. Precision RTL geometry is more reliable on TextKit 2 or via Core Text.

## References

- `/skill txt-uitextinput` — UITextInput protocol details for custom views (marked text, selection, direction)
- `/skill txt-attribute-keys` — `.writingDirection` attribute key reference
- `/skill txt-selection-menus` — selection UI and edit menu behavior
- `/skill txt-appkit-vs-uikit` — platform differences in RTL support
- [UITextInput](https://sosumi.ai/documentation/uikit/uitextinput)
- [NSParagraphStyle](https://sosumi.ai/documentation/uikit/nsparagraphstyle)
- [NSAttributedString.Key.writingDirection](https://sosumi.ai/documentation/foundation/nsattributedstring/key/writingdirection)
- [AttributedString.writingDirection](https://sosumi.ai/documentation/foundation/attributedstring/writingdirection)
- [SwiftUI EnvironmentValues.layoutDirection](https://sosumi.ai/documentation/swiftui/environmentvalues/layoutdirection)
