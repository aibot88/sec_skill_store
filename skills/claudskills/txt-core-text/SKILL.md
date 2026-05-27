---
name: txt-core-text
description: Use Core Text directly — CTLine, CTRun, CTFramesetter, CTTypesetter, CTFont, CTRunDelegate — for glyph-level access, custom typesetting, hit testing outside a text container, font tables, or per-glyph Core Graphics rendering. Use when you need glyph IDs and positions, custom line breaking, drawing text into a CGContext, OpenType feature inspection, or inline non-text elements with custom metrics. Read the actual rendering pipeline (especially the coordinate flip) before reciting fixes — most Core Text bugs are inverted axes or attribute-key type mismatches. Do NOT use when TextKit 2 already exposes the APIs you need — see txt-textkit2.
license: MIT
---

# Core Text

Authored against iOS 26.x / Swift 6.x / Xcode 26.x.

Core Text is the C-API typesetting and font layer that sits directly above Core Graphics. Both TextKit 1 and TextKit 2 render through it — they are clients, not alternatives. This skill covers when to drop down to Core Text directly: TextKit 2 deliberately hides glyph-level access (positions, advances, glyph IDs); custom typesetting or non-standard line breaking needs `CTTypesetter`; per-glyph drawing into a `CGContext` needs `CTLine` or `CTFrame`; font tables and OpenType feature inspection need `CTFont`. The patterns here describe how Core Text usually fails in TextKit-adjacent code — verify against the actual call site, especially the coordinate transform in any `draw(_:)` override.

A practical rule before reaching for Core Text: if TextKit 2's `NSTextLayoutFragment` and `NSTextLineFragment` already expose what you need, stay there. The `txt-textkit2` skill covers fragment geometry. Core Text is the right layer when fragments don't expose individual glyph positions, when you're typesetting outside of an `NSTextContainer`, or when the destination is a `CGContext` you control.

## Contents

- [Architecture overview](#architecture-overview)
- [CTLine — the common entry point](#ctline--the-common-entry-point)
- [CTRun — glyph-level access](#ctrun--glyph-level-access)
- [CTFramesetter and CTFrame](#ctframesetter-and-ctframe)
- [CTTypesetter — custom line breaking](#cttypesetter--custom-line-breaking)
- [CTFont — metrics, glyphs, features](#ctfont--metrics-glyphs-features)
- [CTRunDelegate — inline custom metrics](#ctrundelegate--inline-custom-metrics)
- [Coordinate system and the flip](#coordinate-system-and-the-flip)
- [Bridging TextKit and attribute keys](#bridging-textkit-and-attribute-keys)
- [Common Mistakes](#common-mistakes)
- [References](#references)

## Architecture overview

```
CTFramesetter   (factory)
  └─ CTTypesetter   (line breaking)
       └─ CTFrame   (laid-out region)
            └─ CTLine   (one visual line)
                 └─ CTRun   (contiguous glyphs sharing attributes)
                      └─ CGGlyph[]  (glyph IDs)
                      └─ CGPoint[]  (positions, line-relative)
                      └─ CGSize[]   (advances)
```

Available since iOS 3.2 and macOS 10.5. Core Text uses Core Foundation types (`CFAttributedString`, `CFArray`, `CFRange`); `NSAttributedString` is toll-free bridged on both platforms.

Thread safety: font types (`CTFont`, `CTFontDescriptor`, `CTFontCollection`) are thread-safe and can be shared across threads. Layout types (`CTTypesetter`, `CTFramesetter`, `CTRun`, `CTLine`, `CTFrame`) are not — use them on a single thread per object.

## CTLine — the common entry point

For most TextKit-adjacent work, `CTLine` is the right entry point. It typesets an attributed string into one visual line and exposes the geometry you actually want — typographic bounds, hit testing, per-glyph positions.

```swift
let attributed = NSAttributedString(string: "Hello world",
    attributes: [.font: UIFont.systemFont(ofSize: 16)])
let line = CTLineCreateWithAttributedString(attributed)

// Typographic bounds (used for line height calculations)
var ascent: CGFloat = 0, descent: CGFloat = 0, leading: CGFloat = 0
let typographicWidth = CTLineGetTypographicBounds(line, &ascent, &descent, &leading)
let lineHeight = ascent + descent + leading

// Image bounds (actual rendered pixels — accounts for descenders/diacritics)
let context = UIGraphicsGetCurrentContext()!
let imageBounds = CTLineGetImageBounds(line, context)

// Hit testing: viewport point → string index
let stringIndex = CTLineGetStringIndexForPosition(line, CGPoint(x: 50, y: 0))

// Caret positioning: string index → x offset along the line
let xOffset = CTLineGetOffsetForStringIndex(line, 3, nil)
```

`CTLine` ignores any `NSParagraphStyle` line break, paragraph spacing, or wrapping — it produces exactly one line regardless of width. For wrapped multi-line layout, use `CTFramesetter` or `CTTypesetter`.

## CTRun — glyph-level access

A `CTRun` is a contiguous sequence of glyphs sharing identical attributes. Walking the runs of a `CTLine` is how you get individual glyph IDs, positions, and advances:

```swift
let runs = CTLineGetGlyphRuns(line) as! [CTRun]

for run in runs {
    let count = CTRunGetGlyphCount(run)
    let fullRange = CFRange(location: 0, length: count)

    var glyphs = [CGGlyph](repeating: 0, count: count)
    CTRunGetGlyphs(run, fullRange, &glyphs)

    var positions = [CGPoint](repeating: .zero, count: count)
    CTRunGetPositions(run, fullRange, &positions)

    var advances = [CGSize](repeating: .zero, count: count)
    CTRunGetAdvances(run, fullRange, &advances)

    // Map each glyph back to a UTF-16 string index in the original attributed string
    var stringIndices = [CFIndex](repeating: 0, count: count)
    CTRunGetStringIndices(run, fullRange, &stringIndices)

    let attrs = CTRunGetAttributes(run) as! [NSAttributedString.Key: Any]
    let font = attrs[.font] as! CTFont
}
```

Glyph-to-character mapping is not 1:1: ligatures produce fewer glyphs than characters; Arabic and Devanagari can produce more glyphs than characters. `CTRunGetStringIndices` is the canonical bridge — never compute it from `glyphCount`.

Positions are line-relative. To draw or hit-test in document coordinates, add the line's origin (from `CTFrameGetLineOrigins`) and the host frame's origin.

## CTFramesetter and CTFrame

For laying out attributed text into a rectangular or path-shaped region:

```swift
let framesetter = CTFramesetterCreateWithAttributedString(attributed)

// Suggest the size needed for a given width constraint.
let constraint = CGSize(width: 300, height: .greatestFiniteMagnitude)
let suggestedSize = CTFramesetterSuggestFrameSizeWithConstraints(
    framesetter,
    CFRange(location: 0, length: 0),  // 0 length means "all of the string"
    nil,
    constraint,
    nil
)

let path = CGPath(rect: CGRect(origin: .zero, size: suggestedSize), transform: nil)
let frame = CTFramesetterCreateFrame(
    framesetter,
    CFRange(location: 0, length: 0),
    path,
    nil
)

let lines = CTFrameGetLines(frame) as! [CTLine]
var origins = [CGPoint](repeating: .zero, count: lines.count)
CTFrameGetLineOrigins(frame, CFRange(location: 0, length: lines.count), &origins)

// Draw the entire laid-out frame in one call
CTFrameDraw(frame, context)
```

`CTFrameGetLineOrigins` returns origins in Core Text's bottom-left coordinate space — see [Coordinate system and the flip](#coordinate-system-and-the-flip).

## CTTypesetter — custom line breaking

When you need to control where lines break — for justified ragged-right layout, custom hyphenation, or non-rectangular layout — `CTTypesetter` is the lower level under `CTFramesetter`:

```swift
let typesetter = CTTypesetterCreateWithAttributedString(attributed)

var start: CFIndex = 0
let length = CFAttributedStringGetLength(attributed)

while start < length {
    // Suggest where to break for a target width
    let breakLength = CTTypesetterSuggestLineBreak(typesetter, start, 300.0)

    // Or the cluster-aware variant for CJK and complex scripts
    // let breakLength = CTTypesetterSuggestClusterBreak(typesetter, start, 300.0)

    let line = CTTypesetterCreateLine(typesetter, CFRange(location: start, length: breakLength))
    // Position and draw the line at the appropriate y-coordinate
    start += breakLength
}
```

The two suggest functions differ in what they consider an acceptable break point. `SuggestLineBreak` follows standard line-breaking rules; `SuggestClusterBreak` accepts breaks at every grapheme cluster boundary, which produces tighter packing for CJK content where every character can theoretically wrap.

## CTFont — metrics, glyphs, features

```swift
let uiFont = UIFont.systemFont(ofSize: 16)
let ctFont = CTFontCreateWithName(uiFont.fontName as CFString, uiFont.pointSize, nil)

let ascent = CTFontGetAscent(ctFont)
let descent = CTFontGetDescent(ctFont)
let leading = CTFontGetLeading(ctFont)
let unitsPerEm = CTFontGetUnitsPerEm(ctFont)

// Character → glyph mapping
var characters: [UniChar] = Array("A".utf16)
var glyphs = [CGGlyph](repeating: 0, count: characters.count)
CTFontGetGlyphsForCharacters(ctFont, &characters, &glyphs, characters.count)

// Glyph bounding rectangles
var rects = [CGRect](repeating: .zero, count: glyphs.count)
CTFontGetBoundingRectsForGlyphs(ctFont, .default, glyphs, &rects, glyphs.count)

// Glyph outline path — useful for custom CG rendering
if let path = CTFontCreatePathForGlyph(ctFont, glyphs[0], nil) {
    context.addPath(path)
    context.fillPath()
}

// OpenType features (small caps, alternate glyphs, etc.)
let features = CTFontCopyFeatures(ctFont) as? [[String: Any]] ?? []
```

`CTFontCreatePathForGlyph` is the entry point for custom per-glyph drawing — outline animation, glyph distortion, glyph fills with `CGGradient`. The path is in the font's design space; scale by `pointSize / unitsPerEm` to convert to point space.

## CTRunDelegate — inline custom metrics

`CTRunDelegate` lets you reserve a chunk of width inside a line of text for non-text content while keeping Core Text's typesetting in charge of line breaking:

```swift
var callbacks = CTRunDelegateCallbacks(
    version: kCTRunDelegateCurrentVersion,
    dealloc: { _ in },
    getAscent: { _ in 20 },     // height above baseline
    getDescent: { _ in 5 },      // depth below baseline
    getWidth: { _ in 30 }        // horizontal space reserved
)

let delegate = CTRunDelegateCreate(&callbacks, nil)!
let attrs: [NSAttributedString.Key: Any] = [
    kCTRunDelegateAttributeName as NSAttributedString.Key: delegate,
]
let placeholder = NSAttributedString(string: "\u{FFFC}", attributes: attrs)
```

The delegate reserves space; you draw the actual content at the run's position after layout. This is the building block under `NSTextAttachment` — but it is closer to the metal and lets you draw whatever you want at the reserved location.

## Coordinate system and the flip

Core Text uses Core Graphics's bottom-left-origin coordinate system. UIKit uses top-left origin. Drawing Core Text directly into a UIKit `CGContext` requires flipping the context, and forgetting the flip is the most common Core Text mistake — text either renders upside-down or at a wrong y position.

```swift
override func draw(_ rect: CGRect) {
    guard let context = UIGraphicsGetCurrentContext() else { return }

    // Required: reset and flip
    context.textMatrix = .identity
    context.translateBy(x: 0, y: bounds.height)
    context.scaleBy(x: 1, y: -1)

    CTLineDraw(line, context)
    // or CTFrameDraw(frame, context)
}
```

`textMatrix` persists between drawing calls — leaving a non-identity matrix from a previous operation causes the next Core Text drawing to be transformed unexpectedly. Always reset it before drawing.

`CTFrameGetLineOrigins` returns origins in Core Text coordinates. Converting to UIKit coordinates means flipping the y axis against the frame height:

```swift
for (i, line) in lines.enumerated() {
    let uikitBaselineY = frameRect.height - origins[i].y
}
```

## Bridging TextKit and attribute keys

Most TextKit-adjacent work bridges `NSAttributedString` into Core Text — toll-free bridging means no copy:

```swift
let cf = attributedString as CFAttributedString
let line = CTLineCreateWithAttributedString(cf)
```

Font bridging is platform-dependent. On macOS, `NSFont` and `CTFont` are toll-free bridged:

```swift
let ct = nsFont as CTFont
let ns = ctFont as NSFont
```

On iOS, `UIFont` and `CTFont` are *not* toll-free bridged. Construct explicitly:

```swift
let ct = CTFontCreateWithName(uiFont.fontName as CFString, uiFont.pointSize, nil)
let ui = UIFont(name: CTFontCopyPostScriptName(ctFont) as String, size: CTFontGetSize(ctFont))!
```

Attribute key types diverge between Core Text and UIKit/AppKit. The same conceptual attribute uses different keys and different value types:

| Purpose | Core Text key | UIKit/AppKit key |
|---------|---------------|-----------------|
| Font | `kCTFontAttributeName` (CTFont) | `.font` (UIFont/NSFont) |
| Foreground color | `kCTForegroundColorAttributeName` (CGColor) | `.foregroundColor` (UIColor/NSColor) |
| Paragraph style | `kCTParagraphStyleAttributeName` (CTParagraphStyle) | `.paragraphStyle` (NSParagraphStyle) |
| Kern | `kCTKernAttributeName` | `.kern` |

`UIFont` happens to wrap a `CTFont` internally, so the UIKit `.font` key works in Core Text. `UIColor` and `CGColor` are different types, so `.foregroundColor: UIColor.red` does *not* work for Core Text foreground — the run renders in default color. For attributed strings constructed for direct Core Text use, use the `kCT*` keys with their expected value types.

## Common Mistakes

1. **Forgetting the coordinate flip.** Core Text draws bottom-left; UIKit is top-left. Without resetting `textMatrix` and flipping, text renders upside-down or off-screen. Always set `context.textMatrix = .identity`, translate by `bounds.height`, and scale y by -1 at the start of any `draw(_:)` that calls Core Text. `textMatrix` also persists between calls — leaving a non-identity matrix from earlier code transforms subsequent Core Text drawing unexpectedly.

2. **Treating string indices as Swift Character indices.** `CTRunGetStringIndices` returns UTF-16 code unit offsets matching `NSString`. A single emoji can span 2-4 UTF-16 units; combining marks add more. Convert via `String.Index(utf16Offset:in:)` if you need a Swift index.

3. **`UIFont` and `CTFont` interchangeable on iOS.** They aren't toll-free bridged on iOS (only on macOS, where `NSFont` and `CTFont` are bridged). The UIKit `.font` attribute happens to work in Core Text because UIFont's storage is a CTFont, but `CTFont as UIFont` doesn't compile. Construct explicitly with `UIFont(name:size:)` or `CTFontCreateWithName`.

4. **`UIColor` for `kCTForegroundColorAttributeName`.** That key wants `CGColor`. A `UIColor` value silently fails — the run renders in the default (black) foreground. Use `uiColor.cgColor`. The `.foregroundColor` UIKit key is a different attribute and works in TextKit; it does not work for direct Core Text drawing.

5. **One-glyph-per-character assumption.** Ligatures produce fewer glyphs than characters; complex scripts (Arabic, Devanagari) produce more glyphs than characters. Don't compute string indices from glyph indices arithmetically — use `CTRunGetStringIndices`.

6. **`CTFrame` used for single-line layout.** `CTLine` does the same job in one call without the framesetter overhead. Reach for `CTFramesetter` when you need wrapped multi-line layout, `CTLine` for one-line measurement and drawing.

7. **`NSParagraphStyle` and `CTParagraphStyle` treated as the same type.** `NSParagraphStyle` wraps `CTParagraphStyle` internally, but the C-struct API and the Objective-C property API are different APIs. When building an attributed string for direct Core Text use, construct a `CTParagraphStyle`.

## References

- `txt-textkit2` — TextKit 2 fragment APIs that often suffice without dropping to Core Text
- `txt-textkit1` — `NSLayoutManager` glyph APIs (still available when TextKit 1 is acceptable)
- `txt-viewport-rendering` — fragment geometry and the rendering pipeline
- `txt-attachments` — `NSTextAttachment` is the higher-level wrapper around `CTRunDelegate`
- [Core Text overview](https://sosumi.ai/documentation/coretext)
- [CTLine](https://sosumi.ai/documentation/coretext/ctline)
- [CTFramesetter](https://sosumi.ai/documentation/coretext/ctframesetter)
- [CTTypesetter](https://sosumi.ai/documentation/coretext/cttypesetter)
- [CTFont](https://sosumi.ai/documentation/coretext/ctfont)
- [CTRunDelegate](https://sosumi.ai/documentation/coretext/ctrundelegate)
