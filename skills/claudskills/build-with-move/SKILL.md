---
name: build-with-move
description: Author Sui Move modules and packages with a senior Move dev as your pair. Use when the user wants to write, build, author, add, or scaffold Move code, smart contracts, or Sui programs at the module or function level, in any phrasing.
---

## Preamble (run first)

```bash
# Suiperpower telemetry. Routes through the CLI so projects.json + Convex stay in sync.
# Silent on failure so the skill never blocks. Opt out: SUIPERPOWER_TELEMETRY=off.
#
# AGENT NOTE: when this skill finishes, run the matching completion command:
#   suiperpower track build-with-move build completed
# Or use "failed" / "aborted" if it ended that way.
command -v suiperpower >/dev/null 2>&1 && suiperpower track build-with-move build started >/dev/null 2>&1 &
true
```

If `TEL_PROMPTED` is `no`, before doing real work, ask the user:

> Help suiperpower get better. We track which skills get used and how long they take. No code, no file paths, no PII. Change anytime in `~/.suiperpower/config.json`.
>
> A) Sure, anonymous
> B) No thanks

Write the answer to `~/.suiperpower/config.json` `telemetryTier` field and create `~/.suiperpower/.telemetry-prompted`. Then continue.

## What this skill does

Pairs with the user to author Sui Move modules and packages. It treats Move as a different mental model from Solidity or Rust on accounts (it is), pushes the user toward Sui-native patterns (Objects, capabilities, PTBs), and refuses to ship code that lacks tests for public entry points.

## When to use it

- The user wants to write Move code (a module, a function, a test).
- The user is stuck on a Move compilation error.
- The user is migrating EVM or Solana logic to Sui Move and needs the right primitives.
- The user has a Move package and wants to extend it.

## When NOT to use it

- If the user has not picked a project yet, use `find-next-sui-idea` first.
- If the user has not scaffolded a project, use `scaffold-project` first.
- If the user is composing transactions across modules, use `ptb-composer`.
- If the user is debugging a runtime error from a deployed package, use `debug-move`.
- If the user wants a security review, use `review-move`.

If you activated this skill and the user actually wants something else, consult `skills/SKILL_ROUTER.md` and hand off.

## Inputs

- An existing Move project (a directory with `Move.toml` and `sources/`), or a fresh intent the user describes.
- Optional: `.suiperpower/build-context.md` from `scaffold-project`. Read it if present.
- Optional: `.suiperpower/idea-context.md` if the user is starting from an idea.

If neither context file exists, interview the user for:

- What does the package do in one sentence?
- What Objects does it own or share?
- What capabilities are required for state-changing functions?
- What entry points does it expose to PTBs?

## Outputs

- One or more `.move` files under `sources/` of the project.
- Updated `Move.toml` if dependencies changed.
- One or more test files under `tests/` covering each public function.
- Append a record of what was built to `.suiperpower/build-context.md`:

  ```markdown
  ## build-with-move session, <timestamp>
  - module: <module-name>
  - functions added: <names>
  - tests added: <names>
  - dependencies added: <names>
  - open issues: <list>
  ```

The skill never deletes files outside `sources/` and `tests/` without explicit user confirmation.

## Workflow

1. **Context gathering**
   - Read `.suiperpower/build-context.md` if it exists.
   - If the project has `Move.toml`, list its current modules and dependencies.
   - Confirm the user's intent in one sentence before writing any code.

2. **Design pass (object model first)**
   - Identify which Objects this module creates or modifies.
   - Decide owned vs shared vs immutable for each.
   - Identify capabilities needed (TreasuryCap, AdminCap, custom).
   - Sketch the entry points the user will call.
   - Walk the design back to the user. Adjust before writing code.

3. **Implementation**
   - Write the module(s) following the conventions in `references/move-syntax-cheatsheet.md`.
   - Use OpenZeppelin Sui libraries where applicable (see `skills/data/sui-knowledge/sponsor-docs/openzeppelin-sui.md`). Do not hand-roll access control if OZ provides it.
   - Avoid the pitfalls listed in `references/common-move-pitfalls.md`.
   - Keep functions small. One responsibility per function.

4. **Tests**
   - Every public entry point gets at least one positive test.
   - Capability-gated entry points get an "expected failure" test for the unauthorized call.
   - Use `sui::test_scenario` for scenarios involving multiple addresses.
   - If the user asks to skip tests, push back. Explain that submission preflight will fail without tests.

5. **Build**
   - Run `sui move build` and resolve any errors.
   - If the user is on a non-current Sui CLI version, surface the version mismatch.

6. **Writeback**
   - Append session details to `.suiperpower/build-context.md`.
   - List any open issues you intentionally left for follow-up.

7. **Closing handoff**
   - If `.suiperpower/intent.md` exists and the session was non-trivial (new module, new sponsor integration, or material changes to public functions), recommend `verify-against-intent` as the next step so drift is caught before shipping.
   - If no `intent.md` exists and the session was non-trivial, surface that gap once: offer `clarify-intent` to backfill, do not force it.

## Quality gate (anti-slop)

Before reporting done, the skill asks itself the following and refuses to declare success if any answer is no:

- Is there a non-trivial test for every public function I added or modified?
- Does `sui move build` complete without errors?
- Did I avoid any `unsafe`, commented-out assertions, or capability-leakage patterns?
- Did I capitalize Object, Move, PTB consistently in any user-facing text I produced?
- Is the design walked back to the user, not just code-dumped?
- Are dependencies pinned (no floating versions in `Move.toml`)?

If any answer is no, the skill reports the gap and works through it before claiming the session is complete.

## References

On-demand references (load when relevant to the user's question):

- `references/move-syntax-cheatsheet.md`: Concise syntax reference for Move on Sui (Objects, abilities, capabilities, witness pattern, init function).
- `references/common-move-pitfalls.md`: Mistakes that look right and break (mismatched abilities, leaked capabilities, off-by-one with version increments).
- `references/package-manifest-example.md`: A canonical `Move.toml` with current Mysten dependencies and pinned versions.

Knowledge docs (load when scope expands beyond what is in references):

- `skills/data/sui-knowledge/03-move-and-objects.md`: Full Move plus object model reference.
- `skills/data/sui-knowledge/sponsor-docs/openzeppelin-sui.md`: When to use OZ Sui libs, which modules exist.

## Use in your agent

- Claude Code: `claude "/suiper:build-with-move <your message>"`
- Codex: `codex "/build-with-move <your message>"`
- Cursor: paste a chat message that includes a phrase like "write a Move module", or load `~/.cursor/rules/build-with-move.mdc` and reference it.

If you activated this and the user actually wants something else, consult `skills/SKILL_ROUTER.md` and hand off.
