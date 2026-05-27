---
name: ios-app-store-submission
description: Build and submit iOS apps to App Store Connect using fastlane (match/gym/pilot/deliver) or EAS (eas build / eas submit) for native (Swift/SwiftUI/UIKit), React Native, Expo, Flutter, and Capacitor projects. Use when archiving to .xcarchive, validating, uploading to TestFlight, configuring code signing and provisioning, writing ExportOptions.plist, generating or updating PrivacyInfo.xcprivacy, populating App Store Connect metadata, generating screenshots, submitting for App Review, responding to rejections, or routing ITMS-XXXXX errors. Covers first-time submission and update workflows for solo developers with local/CI builds.
---

# iOS App Store Submission

Solo-developer pipeline for shipping iOS apps to the App Store. Two pipeline shapes:

- **Fastlane** — own-your-pipeline, runs locally or on your CI. Right for native (Swift/UIKit) apps and bare React Native / Flutter / Capacitor projects without EAS.
- **EAS Build + Submit** — Expo's hosted pipeline. Right for Expo apps and bare React Native projects already on EAS. Collapses Phases 1–4 into two CLI commands (`eas build`, `eas submit`).

Framework-aware build routing collapses to a single Xcode workspace (or a remote EAS build) before Phase 2; the rest of the pipeline is framework-agnostic.

## Kernel: 11 axioms

1. **Apple changes the rules constantly.** Xcode versions, App Review Guidelines, required-reason APIs, privacy-manifest rules, screenshot specs, and ITMS error codes all drift. The current source of truth is *always* App Store Connect + the live App Review Guidelines + the Xcode release notes for the version you're submitting from — never this skill. Verify before relying on any specific number, key name, or URL in the references.

2. **The `.xcarchive` is the choke point.** Whatever the framework, Phase 2 must produce a valid archive with embedded dSYMs, a Distribution-signed binary, and a matching App Store provisioning profile. After that, the pipeline is identical regardless of framework.

3. **Signing failures masquerade as build failures.** When `gym` or `xcodebuild archive` fails, suspect signing first: certificate expired, profile missing entitlement, bundle ID mismatch, "Automatically manage signing" fighting a manual profile, `match` repo out of sync. Read the *exact* error string in the log, not the build summary. Beware Xcode's *cloud signing*: a first archive can succeed without any local Distribution cert (Apple holds the key), then subsequent archives fail with `No Accounts` / `No signing certificate "iOS Distribution" found` once the cloud session lapses. Always create a local cert before relying on automatic signing for repeat builds — see `references/OPERATOR-PATTERNS.md` OP-4 through OP-6.

4. **Build wrappers hide the truth.** When `match` / `gym` / `pilot` / `deliver` / `eas build` / `eas submit` fail, the underlying `xcodebuild` / `altool` / Apple-API error is in the log somewhere — find it. Don't retry blindly; the wrapper hides the cause. EAS is especially opaque — its local CLI prints "Something went wrong" while the actual ITMS error sits in the EAS dashboard at the submission URL (OP-29). When in doubt, drop a layer: read the raw `xcodebuild`/`altool`/EAS-dashboard log instead of trusting the wrapper's summary.

5. **Validate before upload, every time.** `gym`'s built-in validation (or `xcrun altool --validate-app`) catches ITMS errors locally in 30s. Catching them after upload costs a TestFlight processing round-trip (5–30 min) per fix.

6. **TestFlight is the only honest validation.** "Builds locally" and "validates" are necessary but not sufficient. A build only proves it works once it processes through TestFlight, installs on a real device, and launches without immediate crash.

7. **First-time submission ≠ update.** First-time requires App Store Connect record creation, agreements/tax/banking, primary category, age-rating questionnaire, full screenshot set, and Beta App Review for external TestFlight. Updates can reuse most of that. Route mode before doing work.

8. **Privacy manifest is now load-bearing.** Since May 1, 2024, apps using "required reason APIs" must ship `PrivacyInfo.xcprivacy`. Common third-party SDKs (Firebase, Sentry, RevenueCat, etc.) need their own manifests with valid signatures. Verify at validation time, not after rejection.

9. **Rejections cite a guideline number for a reason.** Read the cited App Review Guideline (e.g. 2.1, 4.3, 5.1.1) verbatim before responding. Replying without addressing the *specific* clause cited is the fastest path to a second rejection. Then scan for similar issues elsewhere in the app before resubmitting.

10. **ASC's REST API is undocumented discovery surface.** Apple's published OpenAPI spec lags reality. Field sets expand silently (age rating gains new fields each year — OP-17); some endpoints reject `sort=` parameters that work elsewhere (OP-20); some resources forbid `GET` entirely (OP-18); a few operations require Admin/Account Holder API key roles even when the docs imply App Manager is sufficient (OP-5, OP-26). Don't hardcode field lists or trust last year's schema. PATCH-and-read-errors is the only reliable schema-introspection mechanism. Cache discovered schemas locally with a "last verified" date and re-verify on every release cycle.

11. **TestFlight is not independent of App Store version state.** Apple models versions as "trains" — a train is the set of builds attached to one `CFBundleShortVersionString`. Once a version's train is *approved* on the App Store (released, or pending Manual Release after approval), the train **closes**: Apple refuses new uploads at that version, including TestFlight-only ones. ITMS-90062 + ITMS-90186 fire as a pair when this happens (OP-30). Practical implication: every TestFlight upload after a release requires bumping the version. There is no "TestFlight loop on the same version forever" mode. Pre-flight should query ASC for the latest approved version and refuse to start a build at the same or lower number.

## Automation coverage

The CLI surface and the web-UI surface are distinct, and the manual items are mostly one-time. Know where the boundary is *before* you start; don't burn time looking for a fastlane action that doesn't exist.

### CLI-automated (recurring, every release)

| Step | Fastlane command | EAS command (Expo apps) |
|------|------------------|-------------------------|
| Build IPA (Flutter) | `flutter build ipa --release` | n/a |
| Build IPA (native / RN / Capacitor) | `fastlane gym` | n/a |
| Build IPA (Expo) | n/a | `eas build --platform=ios --profile=production` |
| Sync signing certs / provisioning profiles | `fastlane match` | implicit (EAS-managed credentials) |
| Bump build number | `fastlane increment_build_number` | `autoIncrement: true` in `eas.json` |
| Upload to App Store Connect | `fastlane pilot` (or `xcrun altool` raw) | `eas submit --platform=ios --latest` |
| Metadata (name, description, keywords, URLs) | `fastlane deliver` | not covered — use fastlane deliver, ASC REST API, or web UI |
| Screenshots | `fastlane snapshot` (generate) + `fastlane deliver` (upload) | not covered — same fallbacks |
| Submit for review | `fastlane deliver --submit_for_review true` | not covered — ASC web UI or REST API |

### Web-UI-only (one-time per Apple ID, or one-time per app)

- **Apple Developer Program enrollment** ($99/yr + identity verification) — once per Apple ID
- **Agreements / Tax / Banking** in App Store Connect — once per Apple Developer account
- **First-time app creation** in App Store Connect — `fastlane produce` *can* do this, but most solo devs do it once in the UI and never again
- **Privacy nutrition label questionnaire** — Apple gates this in the ASC web UI; deliver support is evolving but not authoritative
- **Export compliance answers** (encryption questionnaire) — can be pre-answered in `Info.plist` via `ITSAppUsesNonExemptEncryption` for the trivial case; ASC's questionnaire UI is still authoritative for first-time and non-trivial cases
- **Age rating questionnaire** — first submission only, then preserved across updates

Items in the web-UI list belong to Phase 0 (Pre-flight). See `references/PRE-FLIGHT.md` for the full one-time setup walkthrough.

## Quick start

### Pick your pipeline

- **Bare-bones (`xcrun altool` + ASC web UI)** — no extra tooling beyond what ships with Xcode. Right for first submissions and TestFlight-only flows on Flutter, native, RN, or Capacitor projects. Often *shorter* than fastlane setup for a single submission. See [OP-37](references/OPERATOR-PATTERNS.md#op-37-flutter-app--testflight-in-zero-fastlane-lines). Skip to "Bare-bones alternative" below.
- **Fastlane** — own-pipeline, runs locally or on your CI. Right when you've graduated from bare-bones because you're shipping repeated releases, want screenshot/metadata automation, or running CI without Apple ID 2FA. Read "One-time setup" through "Authentication" below.
- **EAS** — Expo's hosted pipeline. Right for Expo apps and bare RN projects already on EAS. Skip to "EAS (Expo / RN-on-EAS)" below.

If `eas.json` exists at project root or `app.config.js` / `app.json` has an `expo:` key, you almost certainly want EAS. Otherwise, default to bare-bones for the first submission and graduate to fastlane when repeat-release pain justifies it.

### One-time setup

```
brew install fastlane           # or: gem install fastlane (Bundler-managed preferred — see references/FASTLANE-SETUP.md)
cd <project>/ios                # for Capacitor: <project>/ios/App
fastlane init
```

`fastlane init` creates `fastlane/Fastfile`, `fastlane/Appfile`, and a `Gemfile`. Edit `Appfile` to set `app_identifier`, `apple_id`, and `team_id` (or wire to ENV — see `references/FASTLANE-SETUP.md`).

### Minimal `Fastfile` lane (all frameworks)

```ruby
default_platform(:ios)

platform :ios do
  lane :release do
    build_app(
      workspace: "<workspace>",      # see Framework router below
      scheme: "<scheme>",
      export_method: "app-store"
    )
    upload_to_app_store(
      submit_for_review: false,    # set true only after you've shipped at least once and trust the lane (Phase 7 irreversibility)
      automatic_release: false,    # set true only when you don't need phased-release control
      force: true
    )
  end
end
```

`build_app` is `gym`'s alias; `upload_to_app_store` is `deliver`'s. The lane runs Phase 2 → Phase 7 in one command.

### Per-release one-liner (after lane is set up)

| Framework | Workspace | Scheme | Release command |
|-----------|-----------|--------|-----------------|
| Native | `MyApp.xcworkspace` | `MyApp` | `cd ios && fastlane release` |
| React Native | `<app>.xcworkspace` | `<app>` | `cd ios && fastlane release` |
| Flutter | `Runner.xcworkspace` | `Runner` | `flutter build ipa --release && cd ios && fastlane release` |
| Capacitor | `App.xcworkspace` | `App` | `npx cap sync ios && cd ios/App && fastlane release` |

### Authentication: App Store Connect API key

Generate at <https://appstoreconnect.apple.com/access/integrations/api> (Keys tab), download the `.p8` to `~/.appstoreconnect/private_keys/AuthKey_<KEY_ID>.p8`, and point fastlane at it via `--api_key_path` or the `Appfile`. Bypasses Apple ID 2FA prompts and is what makes the lane CI-friendly. Sanity-check the credentials before Phase 2 — see PRE-FLIGHT.md "Sanity-check the credentials" — so you discover typos in the *Issuer ID* before a real upload, not during it.

→ See `references/PILOT-AND-TESTFLIGHT.md` for key generation, role selection, and CI integration.

### Bare-bones alternative (no fastlane)

For first submissions and TestFlight-only flows on Flutter, native, RN, or Capacitor projects, the bare-bones path is shorter and uses tooling that ships with Xcode. See [OP-37](references/OPERATOR-PATTERNS.md#op-37-flutter-app--testflight-in-zero-fastlane-lines).

```bash
# 1. Build (Flutter shown; native/RN/Capacitor use `xcodebuild archive` instead; Expo / RN-on-EAS uses `eas build` — see EAS section below)
flutter build ipa --release --export-options-plist=ios/ExportOptions.plist

# 2. Verify bundle ID + version baked into the IPA (OP-36)
unzip -p build/ios/ipa/*.ipa "Payload/Runner.app/Info.plist" | \
  plutil -p - | grep -E "CFBundleIdentifier|CFBundleVersion|CFBundleShortVersion"

# 3. Validate (catches ITMS errors locally in 30s)
xcrun altool --validate-app -f build/ios/ipa/*.ipa -t ios \
  --apiKey <KEY_ID> --apiIssuer <ISSUER_ID>

# 4. Upload
xcrun altool --upload-app -f build/ios/ipa/*.ipa -t ios \
  --apiKey <KEY_ID> --apiIssuer <ISSUER_ID>
```

That gets the binary uploaded. Don't pass `--apiKeyPath` — altool finds the `.p8` by convention from the Key ID. Listing metadata and submit-for-review still happen in the ASC web UI unless you script the ASC API directly (PILOT-AND-TESTFLIGHT.md "Verifying state via API"). For repeat releases, fastlane saves you from that — its value compounds across releases, not on the first one.

For polling the build to `VALID` after upload, use `uv tool run --with pyjwt --with cryptography python <poll script>` — full script in PILOT-AND-TESTFLIGHT.md. Be aware the build is "not yet visible" in the API for ~1–3 min after upload, and small IPAs can skip `PROCESSING` and go straight to `VALID` ([OP-35](references/OPERATOR-PATTERNS.md#op-35-asc-api-build-not-yet-visible-window-build-can-skip-processing-and-go-straight-to-valid)).

### EAS (Expo / RN-on-EAS)

For Expo (and bare-RN-on-EAS) projects, the equivalent is two commands:

```bash
eas build --platform=ios --profile=production --non-interactive --no-wait
# wait 5–10 min for build to finish
eas submit --platform=ios --latest --non-interactive
```

Pre-flight: `submit.production.ios.ascAppId` must be set in `eas.json` for non-interactive submit (OP-28). EAS-managed signing means no local Distribution cert is required — Apple credentials live encrypted on EAS servers.

Like the bare-bones path, this only covers build + TestFlight upload. Metadata and submit-for-review remain in the ASC web UI or `fastlane deliver` / ASC REST API.

→ See `references/EAS-SUBMISSION.md` for the full EAS pipeline including version management, error reading, and migration paths.

## Mode router (read before processing)

> **First-submission strategy:** For the first submission, fill listing metadata, screenshots, age rating, and review information once in the App Store Connect web UI — it's faster than building a `Deliverfile` from scratch. Set up fastlane *after* the first build ships; its real value is repeat releases and CI, not initial setup.

Pick exactly one before starting. Each routes to a different subset of phases.

| Mode | Trigger | Phases run |
|------|---------|------------|
| `first-submission` | App not yet in App Store Connect, never released | 0 → 7 (full) |
| `update` | Existing app, new build/version | 0 → 7, skip ASC record creation + agreements + age rating in 6 |
| `testflight-only` | Internal beta, no Store release planned this cycle | 0 → 5, stop |
| `metadata-only` | Description/screenshots/keywords/privacy change only | 6 → 7, skip 0–5 |
| `resubmission-after-rejection` | Apple rejected previous build | start at `references/REJECTIONS.md`, then resume from earliest affected phase |
| `xcode-version-rebuild` | New Xcode/SDK forces re-archive (e.g. annual iOS bump) | 0 → 7 + Xcode-compat audit at Phase 0 |

## Framework router (Phase 1 only)

Each framework collapses to a buildable Xcode workspace **or a remote EAS build**. After Phase 1, every later phase is framework-agnostic.

| Framework | Pipeline | Pre-Xcode step | Workspace path |
|-----------|----------|----------------|----------------|
| Native (Swift/SwiftUI/UIKit) | fastlane | `bundle exec pod install` if Podfile present; for XcodeGen repos `xcodegen generate` first ([OP-39](references/OPERATOR-PATTERNS.md#op-39-xcodegen-managed-projects-put-signing-config-in-projectyml-never-edit-the-xcodeproj)) | `MyApp.xcworkspace` (or `.xcodeproj` if no Pods, or generated from `project.yml`) |
| React Native (bare, no EAS) | fastlane | `cd ios && bundle exec pod install` | `ios/MyApp.xcworkspace` |
| **Expo (managed)** | **EAS** | `eas build --platform=ios --profile=production` | n/a (cloud build) |
| **Expo (bare) / RN with EAS** | **EAS** (recommended) or fastlane | `eas build` *or* `npx expo prebuild && cd ios && pod install` | n/a *or* `ios/<App>.xcworkspace` |
| Flutter | fastlane | `flutter build ios --release --no-codesign` | `ios/Runner.xcworkspace` |
| Capacitor | fastlane | `npx cap sync ios` | `ios/App/App.xcworkspace` |

**Detection:** if `app.config.js` / `app.json` has an `expo:` key, or `eas.json` exists at project root, treat it as an Expo project and prefer EAS unless there's a strong reason to use fastlane (custom CI runners, air-gapped builds, etc.).

→ See `references/FRAMEWORK-BUILDS.md` for full per-framework command sequences. For EAS specifically, see `references/EAS-SUBMISSION.md`.

## Pipeline

Each phase has a hard gate; do not proceed without the listed evidence.

### Phase 0 — Pre-flight
**Gate:** all items below verified in App Store Connect / Apple Developer portal.

Items required for **all paths** (fastlane + EAS):
- Apple Developer Program enrollment active and paid (renewal date >30 days out)
- Agreements, Tax, and Banking complete in ASC (`first-submission` mode only)
- App Store Connect record exists (in `first-submission` mode: create it now with bundle ID matching the project)
- Bundle ID identical across: project config (Xcode / `app.config.js` / `pubspec.yaml`), provisioning profile, ASC record, `Info.plist`
- `ITSAppUsesNonExemptEncryption` set in `Info.plist` / `app.config.js` `ios.infoPlist` (saves a per-upload questionnaire — OP-24)
- **For `update` mode:** local version (`CFBundleShortVersionString`) is strictly greater than the latest approved version on ASC — ITMS-90062/90186 fires on equal-or-lower (OP-30)

Items required for **fastlane-based pipelines** (native, RN-bare-no-EAS, Flutter, Capacitor):
- Distribution certificate **physically present in login keychain** — verify with `security find-identity -v -p codesigning | grep "Apple Distribution"`. Not just "exists in cloud" — that fails on second archive (OP-4).
- App Store provisioning profile valid for current bundle ID
- Xcode version compatible with the iOS SDK the build will target
- ASC API key generated, `.p8` at `~/.appstoreconnect/private_keys/AuthKey_<KEY_ID>.p8`. Role: App Manager for upload/metadata; Admin if you also need cloud signing (OP-5).
- fastlane installed via Bundler (not global gem)
- `match` repo accessible, certificates synced — only required if using match

Items required for **EAS-based pipelines** (Expo or RN-on-EAS):
- `eas whoami` succeeds (Expo account authenticated)
- `eas.json` exists with `submit.production.ios.ascAppId` set for non-interactive submits (OP-28)
- EAS-managed Distribution cert and provisioning profile valid (auto-managed by EAS; verify with `eas credentials --platform ios` if in doubt)
- ASC API key — EAS auto-generates and manages this on first submit, no local `.p8` needed
- *Skip the local-Distribution-cert keychain check (OP-4) — not applicable to EAS-managed signing*

→ See `references/PRE-FLIGHT.md`, `references/FASTLANE-SETUP.md`, and `references/EAS-SUBMISSION.md`.

### Phase 1 — Framework build
**Gate:** Xcode can open the workspace and build the Release scheme without errors. **Plus: app icon and launch screen are not framework defaults.**
Apply the framework router. Fail fast on dependency-install errors before touching Xcode — they are cheaper to diagnose than archive failures.

**Critical placeholder-asset check** (the silent App Review rejection trap):
- **App icon:** `flutter create` / RN / Capacitor scaffolds ship default placeholder icons that pass binary validation but get rejected at App Review under Guideline 4.0 (OP-1). Visually inspect `ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-1024x1024@1x.png` (or equivalent) before Phase 2. If it's the framework default, regenerate via `flutter_launcher_icons` (Flutter), `react-native-launcher-icon` (RN), or manual replacement.
- **Launch screen:** verify `LaunchScreen.storyboard` has been customized. Default storyboards reference `LaunchImage` from a 68-byte placeholder PNG (OP-2). Either replace `LaunchImage.imageset` with branded artwork, OR rewrite `LaunchScreen.storyboard` to use a solid color + label without an image reference.

→ See `references/FRAMEWORK-BUILDS.md`.

### Phase 2 — Archive (`fastlane gym` or `eas build`)
**Gate:** valid `.xcarchive` with embedded dSYMs at known path, Distribution-signed (fastlane); or FINISHED build with downloadable IPA URL (EAS).

**Fastlane path:**
```
fastlane gym \
  --workspace ios/MyApp.xcworkspace \
  --scheme MyApp \
  --configuration Release \
  --export_method app-store \
  --output_directory build \
  --include_symbols true
```

Or invoke from a `Fastfile` lane (recommended; lets you commit the build config).

**EAS path (Expo apps):**
```
eas build --platform=ios --profile=production --non-interactive --no-wait
# poll eas build:view <id> --json until status=FINISHED (5–10 min)
```

→ See `references/GYM-AND-ARCHIVE.md` for `ExportOptions.plist` templates, manual-signing variants, and `xcodebuild` fallthrough. For EAS, see `references/EAS-SUBMISSION.md`.

### Phase 3 — Validate
**Gate:** validation returns success, all ITMS errors resolved.
`gym` runs validation by default; for explicit local validation:

```
xcrun altool --validate-app \
  --file build/MyApp.ipa \
  --type ios \
  --apiKey <KEY_ID> \
  --apiIssuer <ISSUER_ID>
```

Common validation failures: missing privacy manifest, missing usage descriptions in `Info.plist`, encryption-export-compliance gaps, wrong provisioning profile, deprecated API references.

→ See `references/PRIVACY-MANIFEST.md` and `references/ITMS-ERRORS.md`.

### Phase 4 — Upload (`fastlane pilot` or `eas submit`)
**Gate:** build appears in App Store Connect → TestFlight → Builds, processing complete (~5–30 min).

**Fastlane path:**
```
fastlane pilot upload \
  --ipa build/MyApp.ipa \
  --skip_waiting_for_build_processing false \
  --skip_submission true
```

Use ASC API key (`--api_key_path`) over Apple ID + app-specific password — required in CI, recommended locally.

**EAS path:**
```
eas submit --platform=ios --latest --non-interactive
```

Requires `submit.production.ios.ascAppId` in `eas.json` for non-interactive runs (OP-28). EAS uses an EAS-server-managed ASC API key; no local `.p8` needed. **Apple-side errors are not surfaced in the CLI output** — open the submission URL printed by the CLI to read the actual ITMS error (OP-29).

⚠ **Version train constraint:** the version (`CFBundleShortVersionString`) in this build must be higher than the latest version that has been **approved** on the App Store. This applies even for TestFlight-only uploads — once a version is approved, its build train closes (ITMS-90062 + ITMS-90186, OP-30). Bump the version in `app.config.js` / `pubspec.yaml` / Xcode before re-uploading after an approval.

→ See `references/PILOT-AND-TESTFLIGHT.md` for fastlane and `references/EAS-SUBMISSION.md` for EAS.

### Phase 5 — TestFlight verification
**Gate:** build installs and launches on at least one real device via TestFlight.
- Internal testing (≤100 testers, no review) — use first.
- External testing (≤10K, requires Beta App Review for first build of a version) — only when needed.
- Verify launch, primary user flow, no immediate crash. Crash reports surface in ASC → TestFlight → Crashes.

→ See `references/PILOT-AND-TESTFLIGHT.md`.

### Phase 6 — Metadata
**Gate:** all required ASC fields populated.
- Screenshots cover required device sizes — use `APP_IPHONE_67` for any modern Pro Max (OP-21).
- Age rating filled via web UI or PATCH-iterate (OP-17, OP-18).
- If uploading screenshots via ASC REST API, the 3-step reserve → PUT → commit protocol completes (OP-22).
- **If using EAS:** the build artifact must still be ≤30 days old before Phase 7. EAS garbage-collects after 30 days and you'll have to rebuild (OP-32). Don't sit on metadata for a month.

In `update` mode, skip if metadata is unchanged. In `metadata-only` mode, this is the entry point.

Three paths to fill metadata. Pick once and stick with it:

- **Path A: `fastlane deliver`** — committed-source-of-truth, multi-locale, repeatable. Best for repeat releases / CI.
  ```
  fastlane deliver \
    --skip_binary_upload true \
    --skip_screenshots false \
    --force
  ```

- **Path B: ASC REST API direct** — Python/Ruby/Node script using ASC API key + ES256 JWT. Useful when fastlane is overkill or already in a script. Beware: screenshot upload is a 3-step protocol (reserve → PUT chunks → commit), not a single POST (OP-22). The age rating questionnaire field set expands annually and must be discovered by trial PATCH (OP-17, OP-18). Critical: cloud signing operations need Admin API key role; App Manager is fine for everything else (OP-5).

- **Path C: ASC web UI** — recommended for first submissions. Faster than building a `Deliverfile` from scratch. Web UI also has the only authoritative privacy-nutrition-label questionnaire (deliver support is partial) and the always-current age rating questionnaire schema.

Required (verify in ASC at submission time — specs change): app name (≤30), subtitle (≤30), description (≤4000), keywords (≤100), promotional text (≤170), support URL, privacy policy URL, primary category, age rating, privacy nutrition labels, content rights declaration, copyright, screenshots covering current required device sizes (currently `APP_IPHONE_67` for the largest iPhone bucket — note: `APP_IPHONE_69` is *not* a valid enum despite the iPhone 16 Pro Max being 6.9", see OP-21).

→ See `references/DELIVER-AND-METADATA.md` for full schema and the ASC REST API patterns.

### Phase 7 — Submit for Review
**Gate:** submission accepted by ASC, state moves from `PREPARE_FOR_SUBMISSION` to `WAITING_FOR_REVIEW`. **Note:** "Ready to Submit" status on the *build* (in TestFlight) is not the same as "Submitted" — the build is processed and attachable; the actual review submission is a separate action (OP-13).
- Demo account credentials (if app has any login wall — required, not optional)
- Review notes (explain non-obvious flows, third-party login, server-side feature flags)
- Phased Release (7-day rollout) on/off
- Manual vs Automatic release after approval

```
fastlane deliver \
  --submit_for_review true \
  --automatic_release false \
  --phased_release true \
  --force
```

Or via ASC REST API:
```
POST /v1/reviewSubmissions
POST /v1/reviewSubmissionItems
POST /v1/reviewSubmissions/{id}/actions/submit
```

**This is the irreversible action.** Always require explicit user authorization before firing the final submit POST — never submit programmatically without confirmation.

Verify post-submission via `GET /v1/reviewSubmissions?filter[app]={appId}&filter[platform]=IOS` — should return a record with `state: "WAITING_FOR_REVIEW"` (drop any `sort=` param; some endpoints reject it — OP-20).

→ See `references/DELIVER-AND-METADATA.md` for `submission_information` config + the ASC REST submission flow.

### Phase 8 — Post-review
**Gate:** approved + released, OR rejection handled and resubmission queued.
On rejection: `references/REJECTIONS.md` is the entry point. Read the cited guideline verbatim, reproduce locally, fix root cause, scan for similar issues elsewhere in the app, then resubmit. Do not reply to the rejection until you've done all four.

## References

- `PRE-FLIGHT.md` — Apple Developer / ASC setup, certs, provisioning profiles, bundle ID hygiene.
- `FRAMEWORK-BUILDS.md` — Native / RN / Expo / Flutter / Capacitor pre-iOS-build steps and common dependency-install errors.
- `FASTLANE-SETUP.md` — Bundler-managed install, `Appfile`, lane structure, recommended lanes.
- `EAS-SUBMISSION.md` — EAS Build + Submit pipeline for Expo apps. Configuration, polling, error reading, migration to/from fastlane.
- `MATCH-AND-SIGNING.md` — `fastlane match`, cert storage, sync, manual signing fallback, common signing errors.
- `GYM-AND-ARCHIVE.md` — `gym` config, `ExportOptions.plist` templates, raw `xcodebuild` fallthrough.
- `PILOT-AND-TESTFLIGHT.md` — `pilot` upload, internal/external groups, Beta App Review, processing diagnostics, version-train semantics.
- `DELIVER-AND-METADATA.md` — `deliver` init, metadata directory layout, screenshot generation, localizations.
- `PRIVACY-MANIFEST.md` — `PrivacyInfo.xcprivacy`, required-reason APIs, third-party SDK signatures.
- `ITMS-ERRORS.md` — Catalog of common ITMS-XXXXX errors and resolutions.
- `REJECTIONS.md` — Common guideline numbers, response templates, scan-for-similar workflow.
- `OPERATOR-PATTERNS.md` — Session-mined gotchas in OP-N format (grows over time). Categories: placeholder icon traps, cloud-signing fragility, ASC API quirks, screenshot upload protocol, age rating field discovery, Xcode IB compiler gotchas, EAS-specific traps, Flutter+altool zero-fastlane flow, macOS Python externally-managed traps, XcodeGen/native-Swift signing config, two-stage archive/export signing, ASC create-app limitations and propagation lag.

  **Reading order by project type:**
  - **Any first submission:** OP-1, OP-4, OP-7, OP-17, OP-22
  - **Flutter / `altool` zero-fastlane:** OP-34, OP-35, OP-36, OP-37, OP-38
  - **Expo / EAS:** OP-28, OP-29, OP-30
  - **Native Swift / XcodeGen:** OP-39, OP-40, OP-41, OP-42, OP-43, OP-44, OP-45, OP-46
