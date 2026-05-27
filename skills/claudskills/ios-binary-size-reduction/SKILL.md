---
name: ios-binary-size-reduction
description: Use when an iOS app binary/app package needs size reduction with risk-aware optimization, security-aware checks, and verifiable build/runtime evaluation so results are safe and repeatable.
---

# iOS Binary Size Reduction

Use this skill for: Swift/Xcode apps where executable and package size are above target and size reduction must preserve app behavior, security, and startup quality.

## 0) Inputs

- `workspace_or_project`: `.xcworkspace` (preferred) or `.xcodeproj`
- `scheme`
- `configuration`: `Release` (default)
- `risk_level`: `low | balanced | aggressive`
- `size_budget_mb`: optional target reduction threshold
- `min_gain_mb`: minimum gain to keep a change (`0.3` MB default)
- `slice_scope`: `all` or explicit family/OS slices

## 1) Guardrails

- Never apply unsafe production runtime settings: `-Ounchecked`, `-enforce-exclusivity=unchecked`, or equivalent safety suppression flags.
- Never remove `dSYM` generation. Keep symbol upload and crash-symbolication verified.
- Do not merge app behavior changes (asset migration, reflection, feature gating) without passing functional gates.
- Use one risk tier at a time; revert immediately on gate failure.
- Before edits, pin environment metadata (`xcodebuild -version`, `swift --version`, destination, git SHA) and rerun the baseline pipeline once as a no-op control.
- Capture and apply settings per target (for example: app target first, then extensions/widgets), not only project-level.

## 2) Baseline capture (required)

Before any mutation:

1. Collect build settings snapshot:
   - `SWIFT_OPTIMIZATION_LEVEL`
   - `SWIFT_COMPILATION_MODE`
   - `DEAD_CODE_STRIPPING`
   - `STRIP_INSTALLED_PRODUCT`
   - `STRIP_SWIFT_SYMBOLS`
   - `LD` / linker flags (`OTHER_LDFLAGS`)
   - `ASSETCATALOG_COMPILER_OPTIMIZATION`
   - `ALWAYS_EMBED_SWIFT_STANDARD_LIBRARIES`
   - `SWIFT_REFLECTION_METADATA_LEVEL`
   - `LD_RUNPATH_SEARCH_PATHS`
2. Capture size baselines from clean Release archive:
   - `ipa` size, app bundle size
   - Mach-O `__TEXT` and section split (`xcrun size -m`)
   - symbol table size, dSYM size
   - symbolication check against one controlled crash sample
3. Capture baseline quality/perf gates:
   - cold launch time and memory peak
   - targeted smoke suite pass/fail
   - launch crash/no-signature regressions
4. Record immutable environment metadata:
   - `xcodebuild -version`, `swift --version`
   - build destination (`-destination`)
   - git `HEAD` and clean/dirty state
   - scheme/configuration and archive variant
5. Use a reproducible baseline command template and reuse it verbatim for repeatability:
   - Workspace:
     `xcodebuild -workspace "$WORKSPACE" -scheme "$SCHEME" -configuration Release -destination "$DESTINATION" -archivePath "$TMP_ARCHIVE" clean archive`
   - Project fallback:
     `xcodebuild -project "$PROJECT" -scheme "$SCHEME" -configuration Release -destination "$DESTINATION" -archivePath "$TMP_ARCHIVE" clean archive`
   - Export:
     `xcodebuild -exportArchive -archivePath "$TMP_ARCHIVE" -exportPath "$TMP_IPA_PATH" -exportOptionsPlist "$EXPORT_OPTIONS"`

## 3) Pass scheduler (default execution order)

### Tier 1 — Conservative

Apply in sequence, keep all gates green.

1. Run a deterministic Release-only pipeline only:
   1) `clean`
   2) `archive` (`-configuration Release`)
   3) fixed-name export of `ipa`
   - Compare only this Release archive pair against future Release artifacts; ignore Debug artifacts and ephemeral caches.
2. Enable deterministic post-processing: `DEPLOYMENT_POSTPROCESSING = YES`, `STRIP_INSTALLED_PRODUCT = YES`
3. `STRIP_SWIFT_SYMBOLS = YES`
4. `DEAD_CODE_STRIPPING = YES`
5. `SWIFT_COMPILATION_MODE = WholeModule`
6. Remove unused localizations and legacy assets only with an explicit locale/asset inventory
7. `ASSETCATALOG_COMPILER_OPTIMIZATION = space`, prune unused scales/device families; spot-check touched UI flows visually
8. Strip raster metadata (`STRIP_PNG_TEXT = YES`) where legal/compliance requirements allow it
9. Unembed or prune unnecessary resource-heavy bundles

### Tier 2 — Performance/size tradeoff

Only enable if Tier 1 passes.

10. `SWIFT_OPTIMIZATION_LEVEL = -Osize`
11. Enable `LLVM_LTO` (incremental/partial first)
12. Slice pruning: remove unused architectures
13. Set `ALWAYS_EMBED_SWIFT_STANDARD_LIBRARIES = NO` only when precomputed target deployment matrix remains valid (per platform/extension/device family).
14. Dependency minimization pass (SPM/CocoaPods): remove unused targets/features/modules
15. App-thinning report validation and variant-specific packaging checks

### Tier 3 — Conditional / high risk

Enable only with explicit approval when constraints are still missed.
Required preconditions:
- Tier 1 and 2 must have passed two consecutive measured runs.
- Size delta trend must be stable (median repeat variance below configured noise floor).

16. `SWIFT_REFLECTION_METADATA_LEVEL = without-names`, then selective `none`
17. Symbol export hardening (`GCC_SYMBOLS_PRIVATE_EXTERN`, exported/unexported symbol map strategy)
18. Remove aggressive linker retention flags (`-ObjC`, `-all_load`) only after runtime validation
19. Move optional heavy payload to on-demand/background assets strategy
20. Framework split/restructuring or feature-module extraction where architecture allows

## 4) Technique catalogue with trade-off notes

- `P1`: Release-only clean baseline control. Low risk, required for valid deltas.
- `P2`: `DEPLOYMENT_POSTPROCESSING` and `STRIP_INSTALLED_PRODUCT` are deterministic, low-risk size wins.
- `P3`: `STRIP_SWIFT_SYMBOLS = YES` reduces size and improves artifact hygiene; requires strict dSYM retention.
- `P4`: `DEAD_CODE_STRIPPING = YES` gives medium-high size gain; low behavior risk with smoke tests.
- `P5`: Whole-module compilation is strong for dead boundaries; compile time can increase.
- `P6`: Localization pruning gives high ROI only with accurate usage inventory.
- `P7`: Asset catalog optimization is often highest ROI among Tier 1 items; visual regressions possible.
- `P8`: `STRIP_PNG_TEXT = YES` can improve size; preserve legal/compliance metadata.
- `P9`: Resource bundle pruning is strong but UX-sensitive.
- `P10`: `-Osize` is effective for binary shrink; potential hot-path performance regression.
- `P11`: `LLVM_LTO` typically improves size/perf but increases toolchain CPU/time.
- `P12`: Architecture pruning is deterministic if target matrix is validated.
- `P13`: `ALWAYS_EMBED_SWIFT_STANDARD_LIBRARIES = NO` lowers size where safe; verify all target configurations.
- `P14`: Dependency minimization has high value-to-effort, but functional side-effect risk is highest here.
- `P15`: App-thinning validation is low risk, high confidence for deployment compatibility.
- `P16`: Reflection metadata reduction is substantial, may break dynamic reflection users.
  - Validation checklist before and after enabling:
    - `JSONDecoder`/`Decodable` hot paths still roundtrip correctly
    - plugin/discovery paths using runtime type lookup
    - `Mirror` and dynamic cast behavior
    - serialization framework smoke paths (Codable/custom coders)
- `P17`: Export map hardening improves security posture but can break external integrations.
- `P18`: Removing `-ObjC` / `-all_load` is risky if runtime registration depends on it.
- `P19`: On-demand payload can greatly reduce install size; adds runtime fetch and fallback complexity.
- `P20`: Module/framework extraction improves long-term size/control but high refactor risk.

## 5) Security, quality, and performance comparison

- **Security priority** (best to worse): export hardening (`P17`) → deterministic stripping (`P3`,`P4`) → architecture/asset changes (`P12`,`P7`) → optimization/link choices (`P10`,`P11`) → reflection and linkage edits (`P16`,`P18`).
- **Quality priority** (best): resource and dependency cleanup (`P6`,`P7`,`P14`) → conservative compile/link toggles (`P5`,`P10`,`P11`) → reflection/payload changes (`P16`,`P19`).
- **Perf priority** (best): `P11` and controlled reflection tuning (`P16`) are often neutral to positive; `P10` can hurt hot paths.

## 6) Required validation gates after every pass

1. Size gate: `ipa`, app bundle, `__TEXT`, and install-eligible slices compared against baseline.
2. Functional gate: app launches + critical flows + startup path coverage.
3. Stability gate: controlled crash samples must symbolicate with uploaded dSYM.
4. Runtime gate: post-change launch and memory budgets respected.
5. Security gate: signing, entitlements, and crash-reportability unchanged.
6. Reversion gate: if actual gain < `min_gain_mb` or any gate fails, revert only that pass.

Gate execution rule:
- Run each gate twice (or one warm-up + one measured run at minimum); use median or stable mean for gate decisions.
- If either run is outlier by configured noise floor, rerun once before failing pass.

Default per-pass budgets unless overridden:
- size gain threshold: `min_gain_mb` (or 0.3MB)
- launch: +5% or +100ms
- memory peak: +10MB max
- critical flows: no regressions
- crash sample symbolication: 100%

## 7) Evaluation report format

Produce a single report per run containing:

- `run_id`, `xcode_version`, `swift_version`, `git_sha`, `destination`, `risk_level`
- `run_started_at`, `run_ended_at`, `run_duration_seconds`
- Baseline and final size rows (`ipa`, `app`, `__TEXT`, symbol bytes, dSYM bytes)
- Per-pass table entries:
  - `pass_id`
  - `settings_changed`
  - `size_delta_mb`
  - `cumulative_gain_mb`
  - `pass_started_at`, `pass_ended_at`, `pass_duration_seconds`
  - `pass_status` (`applied`, `reverted`, `skipped`)
  - `security_impact`
  - `quality_impact`
  - `performance_delta`
  - `gate_status`
  - `rollback`
  - `notes`
- Rollback log
- Final recommendation + confidence

## 8) Exit criteria and next-step policy

- Stop on first pass with acceptable reduction while all gates pass.
- If still above target, continue next tier.
- For `low` risk_level, never run `P14` or above without explicit approval.
- For `balanced`, stop at tier 2 unless explicitly authorized.
- For `aggressive`, keep user-informed checkpoints before tier 3.

## 9) Minimal output JSON schema

```json
{
  "run_id": "ios-size-YYYYMMDD-###",
  "xcode_version": "15.x",
  "swift_version": "5.x",
  "git_sha": "",
  "destination": "",
  "risk_level": "low|balanced|aggressive",
  "run_started_at": "2026-03-03T12:00:00Z",
  "run_ended_at": "2026-03-03T12:03:24Z",
  "run_duration_seconds": 204,
  "baseline": {
    "ipa_mb": 0.0,
    "app_mb": 0.0,
    "text_section_mb": 0.0,
    "symbols_mb": 0.0,
    "dsym_mb": 0.0
  },
  "final": {
    "ipa_mb": 0.0,
    "app_mb": 0.0,
    "text_section_mb": 0.0,
    "symbols_mb": 0.0,
    "dsym_mb": 0.0
  },
  "cumulative_gain_mb": 0.0,
  "passes": [
    {
      "id": "P4",
      "gain_mb": 0.0,
      "settings_changed": ["DEAD_CODE_STRIPPING=YES"],
      "size_delta_mb": 0.0,
      "cumulative_gain_mb": 0.0,
      "pass_started_at": "2026-03-03T12:01:00Z",
      "pass_ended_at": "2026-03-03T12:01:42Z",
      "pass_duration_seconds": 42,
      "pass_status": "applied",
      "security": "low|medium|high",
      "quality": "low|medium|high",
      "performance_delta": "improved|neutral|degraded",
      "gate_status": "pass|fail",
      "rollback": false,
      "notes": "reason"
    }
  ]
}
```
