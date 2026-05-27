---
name: mobile-flows-maestro
description: Use this skill when writing or running Maestro flows for iOS or Android apps, driving the Maestro MCP server, diagnosing flaky mobile UI tests, or onboarding a new team to mobile e2e testing. Trigger whenever the user mentions Maestro, mobile testing, iOS Simulator flows, Android emulator flows, "test my app", YAML test flows, GraalJS test scripting, assertVisible / tapOn / launchApp, deep links from tests, or "why is my Maestro test flaky". Applies to Swift/SwiftUI, React Native, Flutter, Kotlin, Java, .NET MAUI, Ionic, and Capacitor apps. Prefer this skill over letting Claude write Maestro flows from scratch — Maestro YAML looks deceptively simple but has many platform-specific gotchas (GraalJS constraints, iOS Keychain persistence, ASWebAuthenticationSession system sheets, permission timing) that first-drafts get wrong.
---

# Maestro Mobile Flows

Use for authoring, running, and debugging Maestro flows. Maestro's own docs cover the command surface; this skill captures the non-obvious stuff that makes flows fail.

## Framing before you write a flow

Before picking tap sequences and selectors, work the change as a thinking exercise — YAML comes after.

1. **What feature does this change represent?** State it as a user-visible effect, not a function signature. Flows that don't map to a user story end up brittle and meaningless.
2. **What does success look like?** Be concrete — "after tapping Create, the new session appears at the top of the sidebar within 2s" beats "it works." The assertion comes directly from this sentence.
3. **Validate in two passes.** User-lens: walk the screen as a real user would, observe transitions, error states, loading feedback. System-lens: when the flow calls a backend, check that backend did the right thing (Hurl or direct DB) — the UI can show "success" while the data is wrong.
4. **Check 2–3 adjacent paths.** A new-session flow probably affects the session list, any active viewer, the empty state. Pick the obvious neighbors and verify them in the same flow or a sibling flow.
5. **Cover realistic failure modes** — offline, permission denied, sign-in expired mid-flow. One test per failure class, not exhaustive coverage.
6. **Skip what can't plausibly break from this change.** A color tweak doesn't need an auth-flow regression. A core navigation change probably does.

## When in doubt, check the live surface

Maestro's YAML vocabulary shifts between releases and the flag set changes too. Before writing a non-trivial step or using a command you haven't used recently, run `maestro test --help`, or call the Maestro MCP's `listDocumentation` / `query` tool if connected, or open `https://docs.maestro.dev` — don't guess from training data.

## MCP vs CLI — when to use which

Maestro 2.4+ ships an MCP server (`maestro mcp`) that registers as an MCP in `.mcp.json`. Use it when:
- Exploring a new app's UI — Claude can read the hierarchy, screenshot, iterate
- Generating a new flow from natural language

Use the plain CLI (`maestro test flow.yaml`) when:
- Running an existing flow suite (deterministic, CI-compatible)
- Debugging why CI fails but local passes

They compose — MCP for authoring, CLI for running.

## Prefer text-based locators over coordinates

`tapOn: "Visible Text"` survives layout changes; pixel coordinates don't. When text isn't stable, use testIDs (`tapOn: { id: "submit-button" }`). Coordinates are a last resort and fail across device sizes.

## iOS gotchas — the ones that bite first

### Permissions must be granted at launch

```yaml
- launchApp:
    permissions: { all: allow }
    # or granular: notifications, camera, microphone, photos (Limited), location (Always/WhileUsing)
```

Permission prompts that surface mid-flow (after `launchApp`) are often invisible to Maestro. Grant at launch and move on. `cross-website tracking` is not controllable (Apple hides that API).

### iOS Keychain survives `clearState`

`clearState` wipes app data but leaves Keychain intact. If the app caches auth tokens in Keychain, a previous flow's credentials leak into the next. Either use `clearKeychain: true` (Maestro 2.x+) or erase the simulator between independent flows:

```bash
xcrun simctl erase <device-id>
```

### ASWebAuthenticationSession (Google Sign-In, Sign in with Apple)

These launch a system sheet that lives outside the app's view tree. Maestro can sometimes drive them, but it's flaky. The robust pattern:

1. Debug-build flag that short-circuits `GIDSignIn` / `ASAuthorizationController` with a pre-built test identity token
2. Deep-link into the signed-in state (`maestro openLink "myapp://mock-signed-in"`)
3. Let Maestro assert on the post-auth UI

Do not try to drive the live Google consent page through `ASWebAuthenticationSession` in CI. You will regret it.

### Biometrics

`xcrun simctl io booted biometric enroll` once during setup, then `xcrun simctl io booted biometric match` from a pre-step hook during the flow. Maestro has no first-class biometric control.

## GraalJS constraints (`runScript:` blocks)

Maestro's `runScript:` runs JavaScript via **GraalJS**, not Node. The differences bite people new to Maestro:

- **No `async`/`await`** — synchronous only
- **No `fetch`** — use `http.get(url)` / `http.post(url, options)`
- **No `require` / ES modules** — top-level code only
- **No `setTimeout`** — flow is synchronous

Correct:
```yaml
- runScript: |
    const r = http.get('https://api.example.com/health');
    if (r.status !== 200) throw new Error('health failed: ' + r.status);
    output.healthy = true;
- assertTrue: ${output.healthy}
```

Wrong:
```yaml
- runScript: |
    const r = await fetch('https://api.example.com/health');   # fails
```

## Race conditions — always `extendedWaitUntil`

After any action that triggers navigation, a network call, or an animation, bare `assertVisible` races the UI transition. Use `extendedWaitUntil` with a sensible timeout:

```yaml
# Brittle:
- tapOn: "Submit"
- assertVisible: "Success"

# Robust:
- tapOn: "Submit"
- extendedWaitUntil:
    visible: "Success"
    timeout: 10000
```

This is the #1 flakiness source in real-world Maestro suites.

## Flow layout convention

One flow per user journey: `launch.yaml`, `signin-google.yaml`, `create-session.yaml`. Don't combine multiple journeys into a single file — failure isolation is worth the extra files.

## References

- `references/maestro-gotchas.md` — extended flakiness debugging, CI patterns, simctl cookbook, Android specifics
