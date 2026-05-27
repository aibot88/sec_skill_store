---
name: txt-colors
description: Pick text colors that adapt to dark mode, vibrancy, and accessibility settings across UIKit, AppKit, and SwiftUI — semantic label colors, AppKit's textColor vs labelColor split, dark-mode adaptation rules, wide-color (Display P3), HDR/EDR limits for text. Use when text disappears in dark mode, an attributed string defaults to invisible black, an NSTextView body looks dim, you're picking between systemRed and a P3 red, or designing for high-contrast accessibility. Read the actual color initializers and trait responses before reciting fixes — the patterns here describe how color adaptation usually fails, not where the bug is in your code.
license: MIT
---

# Text Colors

Authored against iOS 26.x / Swift 6.x / Xcode 26.x.

Apple's text APIs have semantic colors that adapt to dark mode, vibrancy, and accessibility contrast settings — and a long tail of legacy or hardcoded values that don't. This skill covers which colors adapt, why attributed strings default to a non-adaptive black, the AppKit `textColor`-vs-`labelColor` split (which gets people coming from iOS), and how wide-color and HDR fit into text rendering. The patterns here describe how color adaptation typically fails; before claiming a specific cause, check the call site that constructs the color, the attributed string that stores it, and any explicit overrides on the host view.

A small but recurring trap: `NSAttributedString`'s default foreground is opaque black, not the semantic label color. An attributed string built without an explicit `.foregroundColor` renders fine in light mode and goes invisible in dark mode. Most "text disappears in dark mode" bugs are this, not a TextKit issue.

## Contents

- [UIKit semantic text colors](#uikit-semantic-text-colors)
- [AppKit textColor vs labelColor](#appkit-textcolor-vs-labelcolor)
- [SwiftUI semantic colors](#swiftui-semantic-colors)
- [Dark mode adaptation](#dark-mode-adaptation)
- [Custom dynamic colors and trait response](#custom-dynamic-colors-and-trait-response)
- [Wide color and Display P3](#wide-color-and-display-p3)
- [HDR and EDR for text](#hdr-and-edr-for-text)
- [WCAG contrast](#wcag-contrast)
- [Common Mistakes](#common-mistakes)
- [References](#references)

## UIKit semantic text colors

The label hierarchy expresses primary-to-quaternary emphasis, all adaptive across light and dark:

| Color | Light | Dark | Use for |
|-------|------|------|---------|
| `.label` | Black α1.0 | White α1.0 | Primary text |
| `.secondaryLabel` | #3C3C43 α0.6 | #EBEBF5 α0.6 | Secondary text |
| `.tertiaryLabel` | #3C3C43 α0.3 | #EBEBF5 α0.3 | Tertiary text |
| `.quaternaryLabel` | #3C3C43 α0.18 | #EBEBF5 α0.18 | Disabled, hint |
| `.placeholderText` | #3C3C43 α0.3 | #EBEBF5 α0.3 | Field placeholder |
| `.link` | #007AFF | #0984FF | Tappable links |

The legacy non-adaptive colors `.lightText` and `.darkText` exist on UIColor and don't adapt. They predate the semantic palette and stay constant across light and dark. There is no good reason to reach for them in modern code.

System tint colors all shift slightly between light and dark for contrast; use them rather than fixed RGB:

```swift
// Adapts: #FF3B30 in light, #FF453A in dark
let red = UIColor.systemRed

// Does not adapt: stays #FF3B30 always
let red = UIColor(red: 1.0, green: 0.231, blue: 0.188, alpha: 1.0)
```

## AppKit textColor vs labelColor

AppKit splits "text color" into two semantic names, and the difference matters because of vibrancy:

- `.textColor` — fully opaque (alpha 1.0), no vibrancy. The default for `NSTextView` body content, document text, and anything inside `NSScrollView`-hosted text.
- `.labelColor` — partially transparent (~0.85 alpha), participates in vibrancy. The default for UI chrome — labels in the sidebar, button captions, control names.

They look nearly identical at rest. The difference appears against vibrant backgrounds (sidebar materials, sheets, popovers): `.labelColor` gets blended with the underlying material; `.textColor` does not. For body text in `NSTextView`, `.textColor` is correct. For chrome around the editor, `.labelColor` is correct.

Other relevant AppKit semantic colors:

| Color | Light | Dark | Use for |
|-------|------|------|---------|
| `.textColor` | Black α1.0 | White α1.0 | Body text |
| `.textBackgroundColor` | White α1.0 | #1E1E1E α1.0 | Text view background |
| `.selectedTextColor` | White | White | Selected foreground |
| `.selectedTextBackgroundColor` | #0063E1 | #0050AA | Selection highlight |
| `.placeholderTextColor` | Black α0.25 | White α0.25 | Field placeholder |
| `.linkColor` | #0068DA | #419CFF | Hyperlinks |
| `.controlTextColor` | Black α0.85 | White α0.85 | Control labels |
| `.disabledControlTextColor` | Black α0.25 | White α0.25 | Disabled controls |
| `.unemphasizedSelectedTextColor` | Black | White | Inactive-window selection |

## SwiftUI semantic colors

SwiftUI exposes adaptive foregrounds via `ShapeStyle`:

```swift
Text("Primary").foregroundStyle(.primary)      // ≈ .label
Text("Secondary").foregroundStyle(.secondary)  // ≈ .secondaryLabel
Text("Tertiary").foregroundStyle(.tertiary)    // ≈ .tertiaryLabel
```

To use UIKit/AppKit semantic colors directly in SwiftUI, bridge via the platform initializer:

```swift
Text("Body").foregroundStyle(Color(uiColor: .label))
Text("Body").foregroundStyle(Color(nsColor: .textColor))   // macOS
```

`Color.primary`, `Color.secondary`, `Color.accentColor` are adaptive. `Color.red`, `Color.blue`, etc. are predefined and adapt for contrast across light/dark — they are not the same as fixed RGB.

## Dark mode adaptation

What auto-adapts and what doesn't comes down to whether the color value resolves dynamically at draw time:

- `UILabel.textColor = .label` — re-resolves on every draw, adapts.
- `UITextView` with no explicit color — defaults to `.label` in TextKit 2 mode.
- `NSAttributedString` with `.foregroundColor: UIColor.label` — UIKit re-resolves the dynamic color when drawing.
- `NSAttributedString` with `.foregroundColor: UIColor.red` — fixed RGB, stays the same in light and dark.
- `NSAttributedString` with `.foregroundColor: UIColor.systemRed` — adaptive system tint, shifts.
- SwiftUI `Text` with `foregroundStyle(.primary)` or `foregroundStyle(Color.red)` — adaptive.
- `CALayer.borderColor` (a `CGColor`) — does *not* re-resolve. CGColor has no notion of trait collection.

The default `NSAttributedString` foreground color is opaque black, not `.label`. An attributed string built without an explicit foreground color goes invisible in dark mode:

```swift
// WRONG — defaults to UIColor.black, invisible in dark mode
let str = NSAttributedString(string: "Hello")

// CORRECT — explicit semantic foreground
let str = NSAttributedString(string: "Hello", attributes: [
    .foregroundColor: UIColor.label,
])
```

This is by far the most common "text disappears in dark mode" bug.

## Custom dynamic colors and trait response

`UIColor(dynamicProvider:)` returns a color that re-resolves per trait collection. Use it for adaptive brand colors that aren't in the system palette:

```swift
let brand = UIColor { trait in
    switch trait.userInterfaceStyle {
    case .dark:  UIColor(red: 0.9, green: 0.9, blue: 1.0, alpha: 1)
    default:     UIColor(red: 0.1, green: 0.1, blue: 0.2, alpha: 1)
    }
}
```

The same provider can branch on `accessibilityContrast` for high-contrast support:

```swift
let contrastAware = UIColor { trait in
    if trait.accessibilityContrast == .high {
        return .black
    }
    return UIColor(white: 0.3, alpha: 1.0)
}
```

Apple's semantic colors already adapt to Increase Contrast — `.label` becomes pure black/white, `.secondaryLabel` pulls toward the foreground.

To respond to trait changes in a view that caches `CGColor` (or otherwise needs manual updates), use the iOS 17+ trait-change registration:

```swift
registerForTraitChanges([UITraitUserInterfaceStyle.self]) { (self: Self, _) in
    self.updateColors()
}
```

The pre-iOS 17 hook still works:

```swift
override func traitCollectionDidChange(_ previous: UITraitCollection?) {
    super.traitCollectionDidChange(previous)
    if traitCollection.hasDifferentColorAppearance(comparedTo: previous) {
        updateColors()
    }
}
```

## Wide color and Display P3

Apple's text rendering goes through Core Text into a `CGContext` whose color space matches the backing `CALayer`. On Display P3 hardware (iPhone 7 and later, recent iPads, Macs with P3 panels), the layer uses a P3 color space, and text rendered with P3 colors displays in the wider gamut.

Creating P3 colors:

```swift
// UIKit
let p3 = UIColor(displayP3Red: 1.0, green: 0.1, blue: 0.1, alpha: 1.0)

// AppKit
let p3 = NSColor(displayP3Red: 1.0, green: 0.1, blue: 0.1, alpha: 1.0)

// SwiftUI
let p3 = Color(.displayP3, red: 1.0, green: 0.1, blue: 0.1, opacity: 1.0)
```

`Color(red:green:blue:)` defaults to sRGB — it is *not* P3.

Practical notes for text: P3 reds and greens are visibly more saturated, which can hurt readability on long-form body copy. Use wide-color for accent and brand applications (a logo, a callout color) and stick to sRGB or semantic colors for body text. Contrast ratio matters more than gamut for legibility.

## HDR and EDR for text

Standard text views (UILabel, UITextView, NSTextView, SwiftUI Text) are not an HDR rendering surface in any documented, supported way. Apple's EDR guidance treats 1.0 as reference UI white; pushing text above that creates a glowing appearance that hurts readability and is outside the design intent of the text APIs.

SwiftUI does expose `allowedDynamicRange(_:)` as a view environment using `Image.DynamicRange`, but the documented HDR APIs are centered on image, video, and custom Metal/Core Animation rendering — not text. Custom Metal pipelines can render text into HDR layers using public APIs, but that is special-effect graphics work, not a recommended path for body or UI text.

The practical guidance is to design text contrast for SDR readability and reserve EDR-aware rendering for non-text content.

## WCAG contrast

| Level | Normal text | Large text (18pt+, or 14pt+ bold) |
|-------|-------------|-----------------------------------|
| AA | 4.5:1 | 3:1 |
| AAA | 7:1 | 4.5:1 |

Apple's semantic label colors meet AA on their corresponding backgrounds:

- `.label` on `.systemBackground` reaches roughly 21:1 in light mode and 18:1 in dark.
- `.secondaryLabel` on `.systemBackground` clears AA for normal text.
- `.tertiaryLabel` typically does not meet AA for normal text — appropriate for hint, decorative, or disabled-only use.

Custom palettes need to be checked against both modes plus high-contrast variants. Xcode's Accessibility Inspector and the per-color contrast preview in the asset catalog are the on-device verification path.

## Common Mistakes

1. **Hardcoded `UIColor.black` or fixed RGB instead of `.label`.** The text reads correctly in light mode and disappears in dark. The fix is always `.label` (or `Color.primary` / `NSColor.textColor` on the relevant platform).

   ```swift
   // WRONG
   let attrs: [NSAttributedString.Key: Any] = [.foregroundColor: UIColor.black]

   // CORRECT
   let attrs: [NSAttributedString.Key: Any] = [.foregroundColor: UIColor.label]
   ```

2. **Forgetting that NSAttributedString defaults to opaque black foreground.** No explicit `.foregroundColor` means invisible text in dark mode. Always set the foreground explicitly when building attributed strings — this is the single most common dark-mode text bug.

3. **`.lightText` / `.darkText` for adaptive text.** They look adaptive (the names imply intent) but are fixed RGB. Use the semantic label colors.

4. **macOS body text rendered with `.labelColor`.** `.labelColor` is for chrome and participates in vibrancy. For NSTextView body content, `.textColor` is the right default. The two look identical against opaque backgrounds and diverge inside vibrant materials.

5. **CGColor on a CALayer that needs to adapt.** `CGColor` has no trait collection. A border or shadow set as a `CGColor` from a dynamic `UIColor` captures the resolution at the moment of access; the layer won't update on dark-mode change. Re-resolve in `traitCollectionDidChange` (or via `registerForTraitChanges` on iOS 17+).

6. **Wide-color body copy.** Display P3 reds and greens are visibly more saturated than sRGB. They are great for brand accents and bad for paragraph text. Reserve P3 for accent colors and use sRGB or semantic colors for body.

7. **Not testing Increase Contrast.** Custom palettes that look fine at default contrast can fail WCAG AA when Increase Contrast is on. The Apple semantic colors handle this automatically; custom dynamic colors need explicit `accessibilityContrast == .high` branches.

## References

- `txt-attribute-keys` — `.foregroundColor`, `.backgroundColor`, `.strokeColor` value types and view compatibility
- `txt-attributed-string` — applying colors via AttributedString vs NSAttributedString
- `txt-dynamic-type` — color decisions that interact with content size category
- `txt-accessibility` — VoiceOver and accessibility-driven color overrides
- [UIColor](https://sosumi.ai/documentation/uikit/uicolor)
- [UIColor.label](https://sosumi.ai/documentation/uikit/uicolor/label)
- [NSColor](https://sosumi.ai/documentation/appkit/nscolor)
- [SwiftUI Color](https://sosumi.ai/documentation/swiftui/color)
