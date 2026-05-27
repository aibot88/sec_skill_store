---
name: property-testing
description: >
  Property-based and generative testing across the polyglot stack.
  TRIGGER when: user asks about property-based testing, generative testing,
  QuickCheck, Hypothesis, proptest, StreamData, fast-check, fuzzing test
  inputs, or finding edge cases that example tests miss.
  DO NOT TRIGGER when: user asks about TDD workflow (use tdd), mutation
  testing (use tdd), load testing (use performance-profiler), or security
  fuzzing (use security-audit).
metadata:
  author: DROOdotFOO
  version: "1.0.0"
  tags: property-testing, generative, quickcheck, hypothesis, proptest, fuzzing, edge-cases
---

> **You are a Senior Test Architect** -- you distrust example-based tests that only prove the author's assumptions, and you design properties that let the machine find the bugs you didn't imagine.

# property-testing

Property-based testing (PBT) generates random inputs, checks that properties
hold for all of them, and shrinks failures to minimal counterexamples. It finds
edge cases that hand-written examples miss.

## What You Get

- Property definitions for the target code (roundtrip, invariant, oracle, metamorphic)
- Custom generators tailored to the domain, not just random noise
- Deterministic CI configuration (fixed seeds, bounded examples)
- Shrunk counterexamples with reproduction commands

## When PBT Beats Example Tests

| Use PBT | Stick with examples |
|---------|---------------------|
| Parsers, serializers (roundtrip property) | Simple CRUD operations |
| Sorting, filtering (invariant properties) | UI rendering |
| State machines, protocols (model-based) | Integration tests with external services |
| Numeric algorithms (oracle: compare to reference) | Code where the property restates the implementation |
| Any function with a large input space | Glue code with minimal logic |

**The litmus test:** Can you state what should be true for ALL inputs without
restating the implementation? If yes, use PBT. If the property is just
`assert f(x) == implementation(x)`, you are testing nothing.

## Workflow

### 1. Identify properties

Before writing any generators, identify what properties the code should satisfy.
See `properties.md` for the full taxonomy. Common starting points:

- **Roundtrip**: `decode(encode(x)) == x`
- **Invariant**: `len(sort(xs)) == len(xs)`
- **Idempotent**: `f(f(x)) == f(x)`
- **Commutative**: `f(a, b) == f(b, a)` (when applicable)

### 2. Build generators

Use the language's built-in generators first. Only build custom generators
when the input domain has constraints (e.g., valid email addresses, balanced
trees). See `generators.md`.

### 3. Write the property test

```python
# Python (Hypothesis)
from hypothesis import given, settings
import hypothesis.strategies as st

@given(st.lists(st.integers()))
@settings(max_examples=200, derandomize=True)
def test_sort_preserves_length(xs):
    assert len(sorted(xs)) == len(xs)
```

```rust
// Rust (proptest)
proptest! {
    #[test]
    fn sort_preserves_length(xs: Vec<i32>) {
        let sorted = sort(&xs);
        prop_assert_eq!(sorted.len(), xs.len());
    }
}
```

```elixir
# Elixir (StreamData)
property "sort preserves length" do
  check all xs <- list_of(integer()) do
    assert length(Enum.sort(xs)) == length(xs)
  end
end
```

### 4. Run, shrink, fix

When a property fails, the framework shrinks the input to the minimal
counterexample. See `shrinking.md` for debugging strategies.

### 5. Lock the seed for CI

Every PBT run must be reproducible. Set a fixed seed and bounded example
count in CI. Allow unbounded exploration in local development.

## Tools by Language

| Language | Library | Install | Seed flag |
|----------|---------|---------|-----------|
| Python | Hypothesis | `pip install hypothesis` | `@settings(derandomize=True)` |
| Rust | proptest | `proptest = "1"` in Cargo.toml | `PROPTEST_SEED=<n>` env var |
| Elixir | StreamData | `{:stream_data, "~> 1.0", only: :test}` | `--seed <n>` in mix test |
| TypeScript | fast-check | `npm i -D fast-check` | `fc.assert(prop, { seed })` |
| Go | gopter | `go get github.com/leanovate/gopter` | `gopter.DefaultGenParameters().Seed(n)` |
| Haskell | QuickCheck | `cabal install QuickCheck` | `quickCheckWith stdArgs{replay=Just(seed,0)}` |

## Relationship to TDD

PBT fits into the TDD workflow as a validation step after the incremental loop:

```
Phase 1: Planning
Phase 2: Tracer Bullet (one example test)
Phase 3: Incremental Loop (example tests, RED-GREEN)
Phase 3.5: Property Testing  <-- YOU ARE HERE
Phase 4: Mutation Testing (see tdd skill)
Phase 5: Refactor
```

PBT and mutation testing target different gaps:
- PBT: "does the code handle inputs I didn't think of?"
- Mutation testing: "would my tests catch a bug if one were introduced?"

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Property just restates the implementation | Find a different angle: roundtrip, invariant, comparison to reference |
| Generator produces invalid domain inputs | Add `assume()` / `filter()` or build a custom generator |
| Tests are slow (>30s) | Reduce `max_examples`, use `@settings(deadline=None)` only locally |
| Flaky CI from non-deterministic seeds | Always set `derandomize=True` or equivalent in CI |
| Only testing pure functions | Use model-based testing for stateful systems |

## Reading guide

| Topic | File |
|-------|------|
| Property taxonomy with examples | `properties.md` |
| Custom generator patterns | `generators.md` |
| Shrinking and debugging failures | `shrinking.md` |

## See also

- `tdd` -- red-green-refactor workflow; PBT extends Phase 3
- `tdd` (mutation-testing sub-file) -- complementary validation (tests the tests, not the input space)
