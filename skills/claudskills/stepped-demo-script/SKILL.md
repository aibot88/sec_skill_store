---
name: stepped-demo-script
description: Author a self-contained bash script that walks a human through a multi-step demo – pausing between steps so they can read output before proceeding, and asserting expected vs. actual so pass/fail is visible at a glance. Use whenever the user wants a runnable repro, walkthrough, or demonstration with discrete steps: reproducing a bug on a sandbox, showing off correct behavior of an API, narrating a CLI flow, making a script an engineer or a stakeholder can paste into a terminal and run top-to-bottom. Phrases that should trigger: "repro script", "demo script", "case script", "walkthrough", "step-through", "show me the steps", "script I can run to demonstrate", "paste-and-run", "script I can share", "script they can run themselves", "reproduction for the team", "whip one up". This skill owns the *authoring* step even when the subject is a specific product/API (SCAPI, cQuotient/Einstein, GitHub, kubectl, git) – if the output is "a script" and the verb is "write/make/draft/build/generate", this is the right skill. For Salesforce-specific scenario *planning* without writing a script (e.g. "what do I need to call before createOrder", "prereqs for addItemToBasket"), use `dsc-scenario` instead. Not for: non-interactive pipelines (CI, one-shot batch jobs) – those shouldn't pause for human input. Not for: generating the domain-specific payloads themselves (API bodies, SQL, etc.) – that's the user's content; this skill authors the scaffolding around it.
---

# Stepped Demo Script

Compose a single bash file that a human can paste into their terminal and walk through, one step at a time, and see at each step (a) what the script is doing, (b) the command's output, and (c) whether the outcome matched expectations. The reader is often not the author – could be a teammate, a stakeholder, a support engineer on the other side of a ticket – so the script needs to be self-contained, legible without context, and not terrifying to open.

The goal is **authoring velocity**: the user starts most of these from a blank page, and the skill's job is to get them past the blank page with the right bones in place, not to dictate the body.

## When this applies

Trigger when the user wants a runnable script that demonstrates a process by calling out each step and pausing for the reader. Common shapes:

- **API sequence** – a series of cURL calls showing a flow (e.g. auth → create → fetch → verify), often to reproduce a customer-ticket scenario or show off correct vs. broken behavior.
- **CLI walkthrough** – a series of commands in a shell or tool (git, kubectl, a CLI the user is learning or teaching).
- **Mixed** – any sequence where each step is one or two commands whose output the human should look at before moving on.

Skip when the script shouldn't pause (CI, cron, piped-to-file), when there's no stepping (a single long command), or when the "demo" is really a tutorial document (that's Markdown, not bash).

## The authoring flow

1. **Elicit the scenario** if it's not already clear from the conversation. You need: what's being demonstrated, in roughly what steps, and whether any of it is misbehavior (so `expect` can surface the mismatch). Don't over-interview – a one-line scenario plus a list of steps is enough to draft.
2. **Pick the closest example** from `examples/` to seed the structure (API sequence or CLI walkthrough). Read the full example before drafting – the shape matters more than any one line.
3. **Start from `templates/minimal.sh`** for new scripts, or extend the chosen example if its shape matches. Never compose a demo script from scratch without the prelude – the constants and helpers in the prelude are the whole point of the skill.
4. **Compose the body from the alphabet** in `references/primitives.md`: `announce`, `section`, `expect`, `pause`, plus the `_jq`/`$c`/`$x` constants. Each step is roughly `announce "what I'm about to do" → <command> → pause`, with an `expect` line afterward if there's an outcome to assert.
5. **Wrap repeated calls in a shell function**, not with a new primitive. If the same cURL shows up twice, lift it into a local function (see `examples/api-sequence.sh`). Functions wrap the command + its `announce`, not the `pause` – pauses stay at the call site so step granularity is controlled by the caller.
6. **Read the draft back** with fresh eyes. The test is whether a reader who's never seen the context can paste the file into their terminal and follow along. If a step's purpose isn't obvious from the `announce` line, fix the `announce`, not the code.

## The prelude

Every script starts with the same block. It's ~15 lines – don't trim it, don't "modernize" it, don't swap it for sourcing a helper. A self-contained script means the reader never has to chase a dependency.

```bash
#!/bin/bash
# --- Demo prelude ----------------------------------------------------
command -v jq >/dev/null 2>&1 && _jq() { jq ${NO_COLOR:+-M} "$@"; } || _jq() { cat; }
c=$'\342\234\205'  # ✅ check
x=$'\342\235\214'  # ❌ cross
if [[ -z "$NO_COLOR" && -t 1 ]]; then
    DIM=$'\033[2m'; BOLD=$'\033[1m'; RESET=$'\033[0m'
else
    DIM=''; BOLD=''; RESET=''
fi
announce() { printf '%s- %s%s\n' "$BOLD" "$*" "$RESET"; }
section()  { printf '\n%s== %s ==%s\n' "$BOLD" "$*" "$RESET"; }
expect()   {
    local e="$1" a="${2-$1}"
    if [[ "$e" == "$a" ]]; then
        printf '%s> expected: %s %s%s\n' "$DIM" "$e" "$c" "$RESET"
    else
        printf '%s> expected: %s %s actual: %s%s\n' "$DIM" "$e" "$x" "$a" "$RESET"
    fi
}
pause() {
    [[ -n "$DEMO_NO_PAUSE" || ! -t 0 ]] && return
    read -rp "<Enter to continue...>" && printf '\033[A\033[2K\n'
}
# ---------------------------------------------------------------------
```

Why each piece is there – you'll want to understand these so you can answer questions and handle edge cases:

- **`_jq`** falls back to `cat` when `jq` isn't installed. JSON responses stay readable either way – no setup instructions needed before running.
- **`$c` / `$x`** are octal escapes for ✅ / ❌. Octal rather than the literal glyph so the script is safe to paste through terminals/editors that mangle non-ASCII. `expect` uses them automatically; expose them directly for hand-rolled lines (mixed-result summaries, rare cases).
- **Color guards** (`NO_COLOR`, `-t 1`) mean the script outputs clean text when piped to a file or when the reader opts out. Respecting `NO_COLOR` is a widely-followed convention and costs one line of setup.
- **`announce`** is the narrator line before a command runs. Bold so it stands out against output.
- **`section`** breaks phases of a demo apart – use it when the script has more than one logical act (e.g. "first as an anonymous user", "now as an authenticated user"). Not every script needs one.
- **`expect`** is polymorphic: one arg means "the demo is showing correct behavior" (`expected: X ✅`); two args means "expected vs. actual differ" (`expected: X ❌ actual: Y`). Don't codify a third "I don't know what's correct" mode – if the author isn't confident enough to state what's expected, the demo isn't ready.
- **`pause`** respects `DEMO_NO_PAUSE=1` for non-interactive runs and auto-skips when stdin isn't a terminal (piping into `bash`, CI). The `\033[A\033[2K\n` sequence moves the cursor up one line and clears it, so the `<Enter to continue...>` prompt doesn't leave a trail in the scrollback.

## Composing the body

Each step is almost always one of three shapes:

**Simple step** (most common):
```bash
announce "Create a basket for cookieId $cookieId"
curl -s -X POST ... | _jq
pause
```

**Step with an assertion** (demo asserts the outcome):
```bash
announce "Fetch recommendations"
get_recs
expect "3 results including pinned item"
pause
```

**Step demonstrating misbehavior** (the whole point of the repro):
```bash
announce "Request with the malformed header"
curl -s ... | _jq
expect "400 bad_request" "500 internal_error"
pause
```

A reusable call lifts into a shell function that includes its own `announce`:

```bash
get_recs() {
    announce "GET /recommendations for cookieId $cookieId"
    curl -s ... | _jq
}
get_recs
expect "3 results"
pause
```

Note the `pause` stays outside the function. This is intentional: the caller owns when the reader gets to read the output, because the same function might be called in a phase where a pause is wanted and another where it isn't.

## Things not to do

- **Don't add a primitive for every shape that appears once.** The alphabet is five functions on purpose. An `info` helper for one-off context lines, a `warn` helper for caveats, a `summary` helper for the last line – each of these is a bare `echo` or `printf` and shouldn't earn a slot. Bloating the prelude makes the reader trace more code before they can read the demo.
- **Don't sweat color for output.** `announce` and `expect` color themselves because they're narrator lines competing with command output. The command output itself (`curl | _jq`, CLI tool output) stays in its default colors – don't wrap it in `$DIM` or similar.
- **Don't mock hostile environments in the prelude.** If the user's demo genuinely needs to run without `bash` v4 features, or on BusyBox, or under `set -u`, call that out to the user – the prelude assumes plain `bash` on a reasonable-enough system (macOS/Linux defaults) and adding portability shims inflates it fast.
- **Don't chain all the steps inside a big function.** Top-level sequential statements are the right shape for a demo. A reader scrolls top-to-bottom and sees the flow. Wrapping everything in `main()` adds a call site the reader has to find.
- **Don't add error handling that changes step semantics.** A failing cURL is often the *point* – `set -e` would mask that. Let each step run and let the reader judge. If a step genuinely must succeed before the next makes sense, the user can inline a check (`|| { echo "..."; exit 1; }`) and the skill shouldn't pre-emptively wire it in.

## Bundled resources

- `templates/minimal.sh` – copy-paste starting point. Prelude + one step + done. Use this when there's no closer example.
- `examples/api-sequence.sh` – unauthenticated GitHub API walkthrough. Demonstrates: `announce`/`expect`/`pause` in a cURL flow, lifting a repeated call into a function, using `section` to split phases, misbehavior mode via two-arg `expect`.
- `examples/cli-walkthrough.sh` – git walkthrough (init → commit → branch → merge-conflict → resolve) in a temp dir. Demonstrates the same primitives applied to non-HTTP commands, and the "demo creates and cleans up its own sandbox" pattern.
- `references/primitives.md` – detailed rationale for each primitive, when to reach for which, and patterns (reusable-call functions, multi-phase scripts, env-variable escape hatches).
