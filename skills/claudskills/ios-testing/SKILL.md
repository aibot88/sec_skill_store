---
name: ios-testing
description: "Invoke any time a user is writing iOS/Swift tests or asking why tests behave a certain way — including XCTest versus Swift Testing (@Test/#expect) choices, async ViewModel tests with @Observable or @Published, snapshot testing across device sizes, mocking protocols for dependency injection, setUp/tearDown lifecycle issues, tests that fail on CI but pass locally, flaky async tests, testing VIPER/TCA/MVVM architectures, and coverage gaps on error paths. The trigger is user intent: they are trying to verify, assert, or validate iOS/Swift behavior in a test context, whether they use the word 'testing' or not."
metadata:
  version: 2.1.3
---

> **Approach: F.I.R.S.T-First, Production-Ready Tests** -- Every test produced by this skill must be Fast, Isolated, Repeatable, Self-validating, and Thorough. Architecture changes to production code and improvements to the test suite both follow phased, low-risk PRs tracked in a `refactoring/` directory.

# iOS Swift Testing

Enterprise-grade testing skill covering 11 areas across all iOS architectures. Opinionated: prescribes Swift Testing (`@Test`/`@Suite`/`#expect`) for all new tests on Xcode 16+, protocol-based mocks with call tracking, F.I.R.S.T compliance checks on every generated test, and architecture-specific patterns for MVVM (UIKit+Combine, SwiftUI+@Observable), VIPER, and TCA.

## Test Distribution Rule

Target: 90% unit tests (mocked, milliseconds) | 8% integration (real DB/network stub) | 2% UI (XCUITest). When in doubt, write a unit test.

## F.I.R.S.T Principles

| Principle | What it means | Violation signal |
|-----------|--------------|-----------------|
| **F**ast | Unit tests should run in milliseconds. Avoid unnecessary waits. | Real `URLSession`, `Thread.sleep`, disk I/O |
| **I**solated | Tests don't share state. Order doesn't matter. | `static var`, `setUp` skipped, test A breaks B |
| **R**epeatable | Same result on any machine, any time. | `Date()`, `UUID()`, random data, time zones |
| **S**elf-validating | Pass or fail -- no log inspection. | `print(result)` with no assertion |
| **T**horough | Happy path + error path + edge cases. | Only green-path tests, 0% error coverage |

## Quick Decision Trees

### "Swift Testing or XCTest?"

```text
Need UI testing?           -> XCTest (XCUITest) only
Need performance testing?  -> XCTest (measure {}) only
Need attachments?          -> XCTest only
Need ObjC support?         -> XCTest only
New unit/integration test? -> Swift Testing (preferred)
Existing XCTest?           -> Migrate incrementally, both coexist
```

### "Which assertion macro?"

```text
Soft check (report + continue)?     -> #expect(expr)
Hard precondition (halt on fail)?   -> try #require(expr)
Unwrap optional + use value?        -> let val = try #require(optional)
Check error thrown?                 -> #expect(throws: Type.self) { }
Check nothing thrown?               -> #expect(throws: Never.self) { }
Record unconditional failure?       -> Issue.record("msg")
```

### "How to test async code?"

```text
@Published + Combine (XCTest)?
  -> dropFirst() + expectation + sink + waitForExpectations

@Observable (XCTest)?
  -> withObservationTracking + expectation + waitForExpectations

@Observable sync?
  -> direct assertion, no waiting needed

Swift Testing + async?
  -> confirmation() for event counting
  -> withCheckedContinuation for completion handlers
  -> for await in stream.prefix(N) for AsyncStream

TCA?
  -> TestStore + await send/receive + TestClock

ViewModel with internal Task {}?
  -> expectation/confirmation or withMainSerialExecutor
```

### "Mock, Stub, or Spy?"

```text
Need to verify method WAS CALLED?     -> Spy/Mock (tracks calls)
Need to provide CANNED RESPONSE?      -> Stub (returns fixed data)
Need BOTH?                            -> Mock = Stub + Spy
System singleton?                     -> Protocol wrapper + inject
1-2 dependency methods?               -> Closure-based injection
3+ methods or call counting?          -> Protocol-based injection
VIPER protocols (many modules)?       -> Sourcery AutoMockable
```

### "Which architecture testing pattern?"

```text
MVVM + SwiftUI + @Observable?
  -> references/observable-testing.md + references/async-testing.md

MVVM + UIKit + Combine?
  -> references/xctest-patterns.md (Combine section)

VIPER / Clean Architecture?
  -> references/viper-testing.md

TCA (Composable Architecture)?
  -> references/tca-testing.md

UI Testing?
  -> references/ui-testing.md

Snapshot Testing?
  -> references/snapshot-testing.md
```

## Workflows

### Workflow: Write a New Test Suite

**When:** Adding tests for a new or untested component.

1. Identify the component's protocol (or create one if missing)
2. Create the mock: implement protocol with `stubbed*` returns and `*CallCount` tracking
3. Write test type: `@MainActor struct ViewModelTests` (Swift Testing) or `@MainActor final class ... : XCTestCase`
4. Write the Arrange block: create mock + inject into SUT
5. Write at minimum: success case, error case, edge/empty case
6. Add memory leak detection (`references/enterprise-testing.md`)
7. Run the suite -- all tests must be green before committing

### Workflow: Migrate XCTest Suite to Swift Testing

**When:** Modernizing a legacy test suite on Xcode 16+. Never in same PR as production changes.

1. Read `references/refactoring-workflow.md` -- create migration plan in `refactoring/`
2. Migrate one test file at a time (<=200 lines per PR)
3. Apply mechanical transforms: assertion mapping table in `references/refactoring-workflow.md`
4. DANGER: Check for third-party libraries using XCTAssert under the hood (`references/anti-patterns.md` C5/C6/C7)
5. Replace `setUp`/`tearDown` with stored properties or `init`
6. Add `@Suite("ComponentName")` and descriptive `@Test("does X when Y")` names
7. Mark `@MainActor` on `@Suite` type when testing isolated ViewModels
8. Run full suite -- if flaky under parallel execution, add `@Suite(.serialized)` + log task
9. Update `refactoring/` plan

### Workflow: Audit Existing Test Suite

**When:** First encounter with a legacy test suite, or preparing a quality report.

1. Scan for anti-patterns using `references/anti-patterns.md` detection checklist and grep script
2. Check for framework mixing (C5/C6/C7). When you find C6 (`#expect` in XCTestCase), **also check M6**: is the `#expect` argument a pre-evaluated Bool variable (e.g. `let isValid = ...; #expect(isValid)`)? These are separate issues — M6 persists even after the context is fixed. Always report both.
3. Check for `wait(for:)` deadlocks, real network calls, shared statics
4. Measure test pyramid ratio: count unit vs integration vs UI tests
5. Identify untested ViewModels: grep for `class.*ViewModel` without corresponding `*Tests` file
6. Create `refactoring/test-debt.md` with severity-ranked findings
7. Fix Critical (deadlocks, crashes, silent passes) first

### Workflow: Test Architecture-Specific Code

**When:** Testing VIPER modules, TCA features, or specific architecture patterns.

1. Identify architecture: MVVM (UIKit/SwiftUI), VIPER, TCA, or other
2. Read the corresponding reference file for patterns
3. For VIPER: test Presenter (mock View + Interactor), Interactor (mock Services), Router (spy NavController) (`references/viper-testing.md`)
4. For TCA: use TestStore with `@MainActor`, override dependencies, assert exhaustively (`references/tca-testing.md`)
5. For @Observable MVVM: use `withObservationTracking` or direct sync assertions (`references/observable-testing.md`)
6. For UIKit+Combine MVVM: use `dropFirst()` + sink + scheduler injection (`references/xctest-patterns.md`)

## Code Generation Rules

<critical_rules>
When generating or reviewing tests, every output must be **F.I.R.S.T-compliant, production-ready, and PR-shippable**. ALWAYS:

1. Use Swift Testing (`@Test`/`@Suite`/`#expect`) for new tests -- XCTest only when Xcode 15 or older, or UI/performance testing
2. One concept per test function -- no `and` in test names
3. Mock all external dependencies via protocols -- never use real URLSession, CoreData, or FileManager in unit tests
4. Mark test type `@MainActor` when SUT is `@MainActor`-isolated
5. Add memory leak detection to every ViewModel test
6. Use `try #require()` before unwrapping optionals in test setup
7. Use test data factories (`Item.sample()`) not raw initializers
8. Cover at minimum: success, failure, and empty/edge case
9. Set `.timeLimit(.minutes(1))` on any test that touches async code
10. Put expressions inside `#expect()` -- never pre-evaluate to Bool
11. NEVER use XCTAssert* in @Test functions or #expect in XCTestCase -- silently swallowed
12. For TCA: mutate `$0` in send/receive closures, never use XCTAssertEqual; use case key paths for receive
13. For @Observable: use withObservationTracking for async changes, direct assertion for sync
14. For Combine: always dropFirst(), subscribe BEFORE action, capture value from sink (willSet semantics)
15. Before generating tests, output a brief `<thought>` identifying: what public behaviors to test, what dependencies to mock, which architecture pattern applies, and which F.I.R.S.T principle is most at risk
16. **When diagnosing a test failure or identifying a testing anti-pattern, always attach an explicit severity label** (🔴 Critical / 🟡 High / 🟢 Medium) before explaining the fix. Severity frames urgency for code review — "hangs forever because `wait(for:)` cannot pump the main queue inside an `async` function" is a **🔴 Critical** issue, not a "hmm, worth looking at". Without an explicit label, reviewers can't triage and the finding gets deferred.
</critical_rules>

## Severity Levels for Testing Anti-Patterns

Use this table to classify any test issue you surface — during generation, diagnosis, or review.

| Severity | Meaning | Examples |
|:--------:|---------|----------|
| 🔴 **Critical** | Test hangs, crashes, or lies — produces wrong signal | `wait(for:)` inside `async` (hang), `XCTAssert*` inside `@Test` (silently swallowed), `#expect` inside `XCTestCase` (no-op), real `URLSession` in unit test (flaky + slow), shared mutable `static var` state between tests |
| 🟡 **High** | Test runs but breaks F.I.R.S.T or gives false confidence | Missing `@MainActor` on `@MainActor`-isolated SUT, no `await fulfillment(of:)` for async (timeout race), missing `dropFirst()` on Combine, no memory leak detection on ViewModel, testing only the happy path |
| 🟢 **Medium** | Functional but fragile or hard to maintain | Raw initializers instead of test data factories, `and` in test names, over-mocked boundary, mock over 100 lines, `setUp`/`tearDown` doing unrelated work |

**How to apply:** When answering "why does my test X?" or "what's wrong with this test code?", the response must lead with `🔴 Critical — <short label>` (or High/Medium) before the explanation. If the cause is a hanging async test, it's Critical. If it's a missing `@MainActor`, it's High. Never omit the label.

## Fallback Strategies & Loop Breakers

<fallback_strategies>
When migrating or writing tests, you may hit stubborn issues. If the same problem appears twice, break the loop:

1. **@MainActor isolation compile errors in tests**: Add `@MainActor` to the entire test type declaration -- not just the method. Why: Swift Testing infers isolation from the type, not individual methods. If error persists, wrap assertions in `await MainActor.run { }` as last resort.
2. **Flaky test under Swift Testing parallel execution**: Add `@Suite(.serialized)`. Log a task in `refactoring/` to investigate. Why: Swift Testing runs all tests in ONE PROCESS with cooperative concurrency (unlike XCTest which used separate processes), so shared mutable state causes non-deterministic failures.
3. **Mock grows beyond 100 lines**: Split into focused mocks that implement protocol subsets. Large mocks are a signal that the protocol itself violates Interface Segregation.
4. **Can't inject dependency** (no protocol, no constructor injection): Add the protocol in a separate PR first. Why: mixing dependency extraction with test writing creates large, hard-to-review PRs.
5. **Third-party library uses XCTAssert under the hood**: Keep those tests as XCTestCase until library adds Swift Testing support. Why: XCTAssert silently becomes a no-op inside `@Test` functions -- tests pass even when assertions fail.
6. **TCA TestStore failures don't fail @Test**: Ensure TCA >= 1.12. Why: earlier versions used XCTFail internally, which is silently swallowed in `@Test` context.
7. **confirmation() fails with completion-handler APIs**: Use `withCheckedContinuation` to bridge. Why: `confirmation()` checks the count when its closure *returns*, not when a callback fires later.
</fallback_strategies>

## Confidence Checks

Before finalizing generated or reviewed tests, verify ALL:

```text
[] F.I.R.S.T compliant -- no real network, no shared state, no Date()/UUID(), has assertion, covers error paths
[] Correct framework -- Swift Testing for new code (Xcode 16+), no framework mixing within a function
[] One concept per test -- no "and" in test name, no multiple unrelated assertions
[] Mock protocol-based -- no concrete type dependencies, no URLSession in unit tests
[] @MainActor -- present on test type when SUT is @MainActor
[] Memory leak detection -- addTeardownBlock or makeSUT pattern present
[] Async safety -- await fulfillment(of:) not wait(for:), timeLimit set
[] Test data factory -- Item.sample() pattern, not raw initializers
[] Error path coverage -- at least one test for the failure case
[] Naming -- "test_<method>_<condition>_<expected>" or @Test("does X when Y")
[] No framework mixing -- no XCTAssert in @Test, no #expect in XCTestCase
[] Architecture-specific -- correct patterns for MVVM/VIPER/TCA
```

## Companion Skills

| Test context | Companion skill | When |
|---|---|---|
| Testing `@Observable` / `@MainActor` ViewModels | swiftui-mvvm skill | ViewModel structure, ViewState enum |
| Testing UIKit + Combine ViewModels | uikit-mvvm skill | Combine publisher testing, Coordinator testing |
| Testing async/await and actor-isolated code | swift-concurrency skill | `withMainSerialExecutor`, Clock injection |
| Testing code with GCD/OperationQueue | gcd-operations skill | Dispatch queue mocking |

## References

| Reference | When to Read |
|-----------|-------------|
| `references/rules.md` | Do's and Don'ts quick reference: priority rules and critical anti-patterns |
| `references/swift-testing-framework.md` | @Test, @Suite, #expect, #require, parameterized tests, tags, confirmation(), known issues, coexistence dangers, parallel execution, traits |
| `references/xctest-patterns.md` | XCTestCase structure, mock pattern, memory leak detection, Combine @Published testing, scheduler injection, coordinator testing |
| `references/async-testing.md` | withMainSerialExecutor, await fulfillment, Clock injection, AsyncStream testing, confirmation() semantics, timeout patterns |
| `references/observable-testing.md` | withObservationTracking, willSet semantics, sync vs async @Observable testing, NavigationPath, sheet/cover state |
| `references/viper-testing.md` | Presenter/Interactor/Router testing, weak reference enforcement, module assembly, entity boundaries, mock management |
| `references/tca-testing.md` | TestStore, exhaustive assertions, receive() case key paths, TestClock, dependencies, navigation, @Shared state |
| `references/ui-testing.md` | Page Object Model, waitForExistence, system alerts, launch arguments, deep link testing, screenshots, accessibility audit |
| `references/snapshot-testing.md` | Device pinning, recording modes, CI configuration, SwiftUI hosting, precision settings, multi-strategy |
| `references/integration-testing.md` | URLProtocol mocking, Core Data /dev/null, SwiftData, Keychain protocol wrapper, UserDefaults isolation, system services |
| `references/enterprise-testing.md` | OAuth token refresh, feature flags, analytics spies, deep linking, push notifications, memory leak detection, test data builders, accessibility |
| `references/anti-patterns.md` | Detection checklist with grep patterns, severity-ranked (Critical/High/Medium), framework mixing dangers |
| `references/test-organization.md` | File structure, naming, Test Plans, CI configuration, parallel testing, coverage targets, flaky test quarantine, time budgets |
| `references/refactoring-workflow.md` | Complete assertion mapping table, lifecycle mapping, migration plan, PR sizing, coexistence rules, common mistakes |
