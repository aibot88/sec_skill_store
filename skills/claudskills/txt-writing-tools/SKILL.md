---
name: txt-writing-tools
description: Integrate Writing Tools into UITextView, NSTextView, custom UITextInput views, or fully custom editors via UIWritingToolsCoordinator. Configure writingToolsBehavior and allowedWritingToolsResultOptions, declare protected ranges via writingToolsIgnoredRangesInEnclosingRange, gate edits with isWritingToolsActive, and pause syncing in willBegin/didEnd. Trigger on 'Apple Intelligence rewrite', 'AI summarize selection', 'compose with AI', 'why won't Writing Tools appear', or 'rewrite is breaking my code blocks' even without UIWritingToolsCoordinator named. Use when Writing Tools is missing from the menu, only the panel mode appears, rewrites corrupt code blocks, the inline animation isn't running, or a custom text engine needs to adopt UIWritingToolsCoordinator. Do NOT use for diagnosing general TextKit 1 fallback symptoms — see txt-fallback-triggers.
license: MIT
---

# Writing Tools Integration

Authored against iOS 26.x / Swift 6.x / Xcode 26.x.

This skill covers wiring Writing Tools into Apple text editors — the configuration knobs on stock views, the delegate hooks that pause your own machinery while a session runs, the protected-range declaration that keeps code blocks safe, and the `UIWritingToolsCoordinator` / `NSWritingToolsCoordinator` adoption path for custom engines. Writing Tools is one of the fastest-moving surfaces in UIKit/AppKit. **Before claiming any specific API signature, delegate name, or behavior mode, fetch the current Apple docs via Sosumi (`sosumi.ai/documentation/uikit/uiwritingtoolscoordinator`, `…/uiwritingtoolsbehavior`, `…/uiwritingtoolsresultoptions`).** The signatures recorded here were verified against Sosumi on 2026-04-29 and the verified surface is pinned in `references/latest-apis.md` — refresh that file via `txt-refresh-against-sosumi` after each Xcode 26.x point release.

If the symptom is *"Writing Tools used to work, now it's panel-only"* or *"some code path made the editor lose inline marks"*, the root cause is usually TextKit 1 fallback. The exhaustive trigger catalog and recovery patterns live in `txt-fallback-triggers`; this skill assumes TextKit 2 is in place and focuses on the integration surface.

## Contents

- [Stock UITextView and NSTextView](#stock-uitextview-and-nstextview)
- [Protected ranges](#protected-ranges)
- [Activity lifecycle](#activity-lifecycle)
- [Custom UITextInput views](#custom-uitextinput-views)
- [UIWritingToolsCoordinator for custom engines](#uiwritingtoolscoordinator-for-custom-engines)
- [PresentationIntent for structure hints](#presentationintent-for-structure-hints)
- [macOS specifics](#macos-specifics)
- [Common Mistakes](#common-mistakes)
- [References](#references)

## Stock UITextView and NSTextView

`UITextView` and `NSTextView` get Writing Tools automatically on systems with Apple Intelligence enabled. The integration surface is two properties and a handful of delegate methods.

`UIWritingToolsBehavior` has four cases: `.none`, `.default`, `.limited`, `.complete`. `.default` is a request that lets the system pick a level; the property's *resolved* value at read time is one of the concrete cases (`.complete` for the full inline experience, `.limited` for panel-only, `.none` for off). Don't compare against `.default` after assignment — read the actual resolved value instead.

```swift
// Request the system's best (usually inline) experience
textView.writingToolsBehavior = .default

// Request the inline experience explicitly — proofreading marks, animated rewrites
textView.writingToolsBehavior = .complete

// Panel-only — popover with no inline marks
textView.writingToolsBehavior = .limited

// Disable Writing Tools entirely on this view
textView.writingToolsBehavior = .none
```

`allowedWritingToolsResultOptions` (type `UIWritingToolsResultOptions`, an `OptionSet`) declares which content kinds Writing Tools may produce as output. The instance options are `.plainText`, `.richText`, `.list`, and `.table`. There is also a static type property `.presentationIntent` that, when set as the option set's value, implies all the other content kinds and switches Writing Tools to `PresentationIntent`-based output for structured documents.

```swift
// Plain editor — only plain-text rewrites
textView.allowedWritingToolsResultOptions = .plainText

// Rich editor — accept rich text and lists; do NOT include .table on UITextView
textView.allowedWritingToolsResultOptions = [.plainText, .richText, .list]

// Structured editor that consumes PresentationIntent runs
textView.allowedWritingToolsResultOptions = .presentationIntent
```

`UITextView` raises `NSInvalidArgumentException` if `.table` is included in the options set. If you need table rewrites, you're outside the stock view's scope — adopt `UIWritingToolsCoordinator` on a custom engine instead. AppKit's `NSTextView.allowedWritingToolsResultOptions` accepts `.table`.

The full inline experience requires TextKit 2. A `UITextView` instantiated with `usingTextLayoutManager: true` gets the inline experience; `false` is limited to the panel. Once a TextKit 2 view falls back to TextKit 1 (any access to `layoutManager`), the fallback is permanent — see `txt-fallback-triggers`.

Apple Intelligence must be enabled in Settings for Writing Tools to appear at all. A view with no Writing Tools menu entry on a real device is most likely on a device without AI enabled; this is a system-level state, not a code bug.

## Protected ranges

Writing Tools rewrites prose. Code blocks, quoted citations, machine-generated sections, and other "do not touch" regions need to be declared via `textView(_:writingToolsIgnoredRangesInEnclosingRange:)`. The delegate is called with the enclosing range Writing Tools is about to operate on; return the sub-ranges to exclude as `[NSValue]` (each wrapping an `NSRange` via `NSValue(range:)`).

```swift
func textView(_ textView: UITextView,
              writingToolsIgnoredRangesInEnclosingRange enclosingRange: NSRange) -> [NSValue] {
    let codeBlockPattern = try! NSRegularExpression(pattern: "```[\\s\\S]*?```")
    let matches = codeBlockPattern.matches(
        in: textView.text,
        range: enclosingRange
    )
    return matches.map { NSValue(range: $0.range) }
}
```

Returned ranges must be in NSRange (UTF-16) units relative to the text view's own string, not relative to `enclosingRange`. If the editor stores semantic ranges in a separate model (parsed Markdown AST, syntax-tree nodes), translate them at the boundary using `NSRange(swiftRange, in: text)` before wrapping in `NSValue`.

For systems where the user can mark regions explicitly (a "preserve" toggle, an `<inv>`-style escape sequence, semantic styling), translate those user marks into the returned ranges here. The delegate runs every time a session starts; it doesn't need to be cached.

## Activity lifecycle

Two delegate methods bracket a Writing Tools session. Use them to pause anything that would conflict with Writing Tools mutating the text underneath: collaborative-editing pushes, server syncs, undo coalescing, autosave timers, syntax re-highlighting, model invalidation.

```swift
func textViewWritingToolsWillBegin(_ textView: UITextView) {
    syncEngine.pause()
    undoManager?.disableUndoRegistration()
}

func textViewWritingToolsDidEnd(_ textView: UITextView) {
    undoManager?.enableUndoRegistration()
    syncEngine.resume()
}
```

While a session is running, programmatic edits to the text should check `textView.isWritingToolsActive` first and skip the edit (or queue it for after `didEnd`). Writing into the text storage during an active session corrupts the rewrite preview and can leave the view in a state where the user's accept/reject choice replays the wrong content.

`isWritingToolsActive` is a transient flag — true between `willBegin` and `didEnd`, false otherwise. Treat it as a runtime guard, not a configuration switch.

## Custom UITextInput views

A custom view that conforms to `UITextInput` (but isn't `UITextView`) can pick up Writing Tools through the standard text interactions. Add a `UITextInteraction` and the callout-bar entry appears automatically.

```swift
class CustomTextView: UIView, UITextInput {
    let textInteraction = UITextInteraction(for: .editable)

    override init(frame: CGRect) {
        super.init(frame: frame)
        textInteraction.textInput = self
        addInteraction(textInteraction)
    }
}
```

`UITextInteraction` covers selection UI, edit menus, and Writing Tools. The view must also implement the full `UITextInput` surface (marked text, selection rects, line geometry) for the rewrite to land correctly — see `txt-uitextinput` for the protocol's required methods.

If you only need the edit menu and selection without Writing Tools, use `UITextSelectionDisplayInteraction` and `UIEditMenuInteraction` separately. `UITextInteraction` is the bundled experience.

## UIWritingToolsCoordinator for custom engines

For text engines that don't conform to `UITextInput` — game UIs, code editors with custom layout, fully custom rendering — `UIWritingToolsCoordinator` is the integration surface. The coordinator conforms to `UIInteraction` and is added via `addInteraction(_:)`. The host adopts the nested protocol `UIWritingToolsCoordinator.Delegate` (it lives inside the coordinator class, not as a top-level `UIWritingToolsCoordinatorDelegate`). All delegate methods are **completion-handler based**, not Swift `async`.

```swift
final class CustomEditorView: UIView {
    private var coordinator: UIWritingToolsCoordinator!

    override init(frame: CGRect) {
        super.init(frame: frame)
        coordinator = UIWritingToolsCoordinator(delegate: self)
        addInteraction(coordinator)
    }
}

extension CustomEditorView: UIWritingToolsCoordinator.Delegate {
    func writingToolsCoordinator(
        _ coordinator: UIWritingToolsCoordinator,
        requestsContextsFor scope: UIWritingToolsCoordinator.ContextScope,
        completion: @escaping ([UIWritingToolsCoordinator.Context]) -> Void
    ) {
        let context = makeContext(for: scope)
        completion([context])
    }

    func writingToolsCoordinator(
        _ coordinator: UIWritingToolsCoordinator,
        replace range: NSRange,
        in contextWithIdentifier: UUID,
        proposedText: NSAttributedString,
        reason: UIWritingToolsCoordinator.TextReplacementReason,
        animationParameters: UIWritingToolsCoordinator.AnimationParameters?,
        completion: @escaping () -> Void
    ) {
        applyReplacement(proposedText, in: range, contextID: contextWithIdentifier)
        completion()
    }

    func writingToolsCoordinator(
        _ coordinator: UIWritingToolsCoordinator,
        willChangeTo newState: UIWritingToolsCoordinator.State,
        completion: @escaping () -> Void
    ) {
        switch newState {
        case .inactive:             resumeNormalEditing()
        case .noninteractive:       pauseEditing()
        case .interactiveResting:   showRestingUI()
        case .interactiveStreaming: showStreamingUI()
        @unknown default:           break
        }
        completion()
    }
}
```

`UIWritingToolsCoordinator.State` has four documented cases: `.inactive` (no session), `.noninteractive` (system is preparing a non-interactive rewrite), `.interactiveResting` (the user is in an interactive session, idle between streams), `.interactiveStreaming` (a stream is animating in). Note the lowercase `.noninteractive` — no inner capital. Always include `@unknown default` because the enum has gained cases on past releases.

`UIWritingToolsCoordinator.Context` is a class — not a struct with a value initializer. Construct it through the methods Apple provides (typically by returning a model-built context to the `requestsContextsFor:completion:` callback). The coordinator reports the range it actually used through `Context.resolvedRange`; there is no nested `TextRange` type on the coordinator.

For animated previews, implement `writingToolsCoordinator(_:requestsPreviewFor:of:in:completion:)` (returning a preview image and rect) and `writingToolsCoordinator(_:requestsUnderlinePathsFor:in:completion:)` (note: `requestsUnderlinePaths`, plural) returning bezier paths for proofreading marks. Without these, Writing Tools still works but loses the inline animation that distinguishes it from the panel mode.

The `preferredBehavior` / `behavior` and `preferredResultOptions` / `resultOptions` pairs work like the stock view's settings — you assign the preferred level, and the coordinator reports the level the system actually granted.

`NSWritingToolsCoordinator` is the AppKit equivalent with the same delegate pattern. On AppKit, attach via `nsView.writingToolsCoordinator = NSWritingToolsCoordinator(delegate: self)` rather than an `addInteraction` call.

## PresentationIntent for structure hints

Writing Tools makes better decisions when the document declares its structure. `PresentationIntent` on `AttributedString` runs marks ranges as headings, code blocks, block quotes, lists. Code-block intent in particular tells Writing Tools to leave the region alone without an explicit `writingToolsIgnoredRangesInEnclosingRange:` callback for it.

```swift
var doc = AttributedString("My Document")
doc.presentationIntent = .header(level: 1)

var code = AttributedString("let x = 1")
code.presentationIntent = .codeBlock(languageHint: "swift")
```

For Markdown editors, the parser already produces `PresentationIntent` runs — see `txt-markdown`. For custom storage, set the intent at insertion time so it travels with the content.

## macOS specifics

`NSTextView` exposes `writingToolsBehavior: NSWritingToolsBehavior` and `allowedWritingToolsResultOptions: NSWritingToolsResultOptions` mirroring the UIKit shape. The delegate methods `textViewWritingToolsWillBegin(_:)` and `textViewWritingToolsDidEnd(_:)` take the `NSTextView` itself (matching the UIKit signature), not a `Notification`. Protected ranges flow through `textView(_:writingToolsIgnoredRangesInEnclosingRange:)` returning `[NSValue]`, identical to UIKit.

`NSTextView` does accept `.table` in `allowedWritingToolsResultOptions` (UITextView does not). For older macOS custom views without a coordinator path, `NSServicesMenuRequestor` is the fallback — declaring the view as a valid pasteboard sender and reader exposes Writing Tools through the Services menu rather than as an inline experience. New custom editors should adopt `NSWritingToolsCoordinator`.

## Common Mistakes

1. **Editing storage during an active session.** Programmatic edits while `isWritingToolsActive` is true corrupt the rewrite preview and can crash the view on accept/reject. Gate every programmatic edit with `guard !textView.isWritingToolsActive else { return }`.

2. **Returning `[NSRange]` from `writingToolsIgnoredRangesInEnclosingRange:`.** The signature returns `[NSValue]`. Wrap each range with `NSValue(range:)` before returning. Returning the wrong type causes the delegate to be ignored silently — Writing Tools will rewrite the regions you thought were protected.

3. **Comparing against `.default` after assignment.** `.default` is a request, not a resolved value. Read the actual case (`.complete`, `.limited`, `.none`) instead of comparing against `.default`.

4. **Including `.table` in `UITextView.allowedWritingToolsResultOptions`.** Raises `NSInvalidArgumentException`. UITextView only accepts plain text, rich text, and lists. NSTextView accepts table.

5. **Forgetting protected ranges for code blocks or quotes.** Without the ignored-ranges delegate, Writing Tools rewrites code, citations, and machine-generated content. Either set ranges explicitly or use `PresentationIntent.codeBlock(...)` so the system skips them.

6. **TextKit 1 fallback removing the inline experience.** Writing Tools degrades to panel-only when the underlying view drops to TextKit 1. The trigger is usually unrelated code (a third-party library accessing `layoutManager`) — see `txt-fallback-triggers`. Set a symbolic breakpoint on `_UITextViewEnablingCompatibilityMode` to find the offending call.

7. **Treating `UIWritingToolsCoordinator.State` as exhaustive.** The enum has gained cases on past releases. Use `@unknown default` to avoid breaking when a new state ships. The four current cases are `.inactive`, `.noninteractive`, `.interactiveResting`, `.interactiveStreaming`.

8. **Adopting a top-level `UIWritingToolsCoordinatorDelegate` protocol.** That type doesn't exist. The delegate protocol is nested as `UIWritingToolsCoordinator.Delegate`.

9. **Writing `async` delegate methods.** The published surface uses completion-handler-based methods (`(_:requestsContextsFor:completion:)`, `(_:replace:in:proposedText:reason:animationParameters:completion:)`, etc.). Convert to `async` at the call site if your codebase prefers it (`withCheckedContinuation`), but the conformance has to match the protocol.

10. **Assuming Writing Tools is always available.** It requires Apple Intelligence enabled. A device without AI enabled won't show the menu entry no matter how the view is configured. Don't treat its absence as a configuration bug without checking the device state.

## References

- `references/latest-apis.md` — verified Apple API surface for Writing Tools; refresh after Xcode 26.x point releases via `txt-refresh-against-sosumi`
- `txt-fallback-triggers` — exhaustive TextKit 1 fallback trigger catalog and recovery
- `txt-textkit2` — TextKit 2 layout manager APIs and viewport
- `txt-uitextinput` — full UITextInput protocol implementation for custom views
- `txt-attributed-string` — `AttributedString` and `PresentationIntent`
- `txt-markdown` — Markdown parsing into `PresentationIntent` runs
- [UIWritingToolsCoordinator](https://sosumi.ai/documentation/uikit/uiwritingtoolscoordinator)
- [UIWritingToolsCoordinator.Delegate](https://sosumi.ai/documentation/uikit/uiwritingtoolscoordinator/delegate-swift.protocol)
- [UIWritingToolsCoordinator.State](https://sosumi.ai/documentation/uikit/uiwritingtoolscoordinator/state)
- [UIWritingToolsBehavior](https://sosumi.ai/documentation/uikit/uiwritingtoolsbehavior)
- [UIWritingToolsResultOptions](https://sosumi.ai/documentation/uikit/uiwritingtoolsresultoptions)
- [UITextView writingToolsBehavior](https://sosumi.ai/documentation/uikit/uitextview/writingtoolsbehavior)
- [NSWritingToolsCoordinator](https://sosumi.ai/documentation/appkit/nswritingtoolscoordinator)
- [PresentationIntent](https://sosumi.ai/documentation/foundation/presentationintent)
- [UITextInteraction](https://sosumi.ai/documentation/uikit/uitextinteraction)
