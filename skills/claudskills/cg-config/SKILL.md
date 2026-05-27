---
name: cg-config
description: Invoke when the user wants to understand, review, change, or get recommendations for their Cartograph *setup* — the stable preferences that shape every future checkin, search, and install. Fires on "what's my config", "walk me through my setup", "I want X to be the default", "change my settings", "what should my setup be", "how should I configure Cartograph if I want to <intent>", or any intent about defaults/preferences (private widgets by default, switch registries, point Cartograph at a custom engine binary). Does NOT fire when the user wants to take a one-off action on a specific widget. Does NOT fire when the agent just needs to read one config value for its own work — that's a direct MCP tool call.
---

# cg-config — interpret and recommend Cartograph setup

The tools for reading and writing config are already available as MCP
calls. This skill is not about how to use them. It's about how to
**interpret** what the user has and **recommend** coherent setups when
they ask.

The skill runs in one of two modes depending on what the user wants.

- **Briefing mode** — user wants to know what their current setup does.
  Interpret, don't editorialize. See "Briefing mode" below.
- **Recommendation mode** — user wants to know what their setup
  *should* be given an intent. Propose a named profile, explain the
  tradeoff, apply on confirm. See "Recommendation mode" below.

Don't mix the two. If the user opens with a briefing request, don't
drift into recommendations. If they open with an intent, don't deliver
a full briefing first — offer profiles directly.

## Tool boundary

Prefer `cartograph_config` for reading or changing config keys exposed
by the MCP surface. Use the `cartograph` CLI for registry management,
auth state, doctor output, path diagnostics, or settings that are not
currently exposed as MCP tools.

## Agent setup

Config covers Cartograph's own defaults, but the agent also needs to
know Cartograph exists. That lives in the agent's instructions file
(e.g. `CLAUDE.md`, `AGENTS.md`) and is written by the CLI:

    cartograph setup

The command auto-detects the agent, appends Cartograph instructions
to the right file, and never replaces existing content. Useful flags:

- `--agent <name>` force a specific agent when auto-detect is wrong
  or the user works with multiple agents.
- `--file <path>` target a specific file instead of the auto-detected
  one.
- `--print` print the instructions to stdout instead of writing,
  useful when the user wants to review before committing.

When to surface this:

- The user asks how to connect a new agent to Cartograph.
- The user is on an agent that doesn't ship a Cartograph plugin
  (bare CLI, Aider, Cursor without the MCP registered, etc).
- The user reports the agent "doesn't seem to know about widgets"
  despite the MCP being live.

Skip it when the user is already running the Cartograph plugin for
their agent — the plugin ships its own teaching layer and `cartograph
setup` would duplicate it.

## Briefing mode

### Frame the briefing as three workflow questions

Not a setting-by-setting readout. Synthesize the config + registry
list + doctor output into three short paragraphs, in this order:

### 1. "What happens when I check in a widget?"

Reads: `auto-publish`, `publish-registry`, `visibility`, `governance`.

These four combine into one sentence about the user's publishing flow.
Common combinations:

- **auto-publish on, registry=cg:** every checkin pushes to the public
  `cg` community registry. All `cg` widgets are public, so `visibility`
  is inert here — don't pretend it matters. Governance governs whether
  the community can propose changes.
- **auto-publish off, registry=cg:** checkin stays local; publishing is
  a separate manual step. Still public-only when the user chooses to
  push.
- **auto-publish on, registry=<other>:** every checkin pushes to that
  registry honoring `visibility` — private means invited collaborators
  only.
- **auto-publish off, registry=<other>:** checkin stays local; publishing
  is a separate manual step when the user chooses to push.

If the config output flags `visibility.effective=false`, say that
directly — the CLI already encodes the "no-op on cg" rule, trust it.

### 2. "What do you see when I search?"

Reads: `cloud` enabled state, configured registries, `show-unavailable`.

One sentence. Cloud enabled or not; which registry or registries the
user is pulling from; whether results include widgets for languages
they can't actually run.

If only the default `cg` registry is configured, say that directly.
Don't list it as if it were a deliberate choice — it's the default.

### 3. "What runs locally?"

Reads: doctor output (engine availability) + any `paths.*` overrides.

One sentence. Which engines are available, which are missing, and
whether the user has pointed Cartograph at any custom binary
locations. If an engine is missing, mention that widgets in that
language won't validate or install — factual consequence, not a
scolding.

## Recommendation mode

User's intent is the starting point, not the current config. Map the
intent to one or two of the four named profiles below, surface the
tradeoffs, let them pick.

### The four profiles

**1. Local-only.**
*"I want Cartograph as a local widget manager. No sharing."*
- `cloud=false`, `auto-publish=false`, `show-unavailable=false`
- Everything stays on disk. Useful for exploration, air-gapped
  machines, or corporate environments that can't reach external
  networks.

**2. Community contributor.**
*"I want to pull from the public library and push back when I've
polished something."*
- `cloud=true`, `publish-registry=cg`, `auto-publish=false`,
  `governance=open`
- `visibility` is moot on cg. The `auto-publish=false` gives the user
  a review window before each push.

**3. Eager contributor.**
*"Everything I check in should be public immediately."*
- Same as Community contributor but `auto-publish=true`.
- Tradeoff to name out loud: zero friction, but also zero "wait I
  wasn't done yet" window — every successful checkin becomes a public
  release on cg.

**4. Organization member.**
*"I work at a company hosting its own registry. I want widgets to go
there by default, privately."*
- `cloud=true`, `<org prefix>` added via registry add,
  `publish-registry=<org>`, `visibility=private`,
  `auto-publish=false`
- The only profile where `visibility` is load-bearing. Requires the
  user to know (or ask) their org's registry URL.

### Conversation shape

1. **Narrow based on what the user said.** Don't list all four. If
   they said "I want everything private" offer 1 and 4. If they said
   "I want to share publicly" offer 2 and 3. If they said "help me
   set up" ask a clarifying question first.
2. **Describe each offered profile in three lines:** name, the one
   intent sentence, the concrete settings.
3. **Name the tradeoff for each.** Don't pretend there isn't one.
4. **User picks one** or says none fit.
5. **Show the diff** between current config and the profile — only
   what would change. Four changed keys is more trustworthy than
   "apply this profile" as an opaque operation.
6. **Apply on confirmation**, one setting at a time (same discipline
   as Briefing mode's change loop).

### Integration with Briefing mode

If the user finished a briefing and their current config looks
incoherent (cloud off but auto-publish on, overriding paths for
engines that don't exist, etc), the briefing may end with: *"If you
want to walk through a clean setup, I can suggest profiles."* That's
a hand-off into Recommendation mode, not an editorial push.

Never flip into recommendation mode unprompted in the middle of a
briefing.

## Semantics you need to carry

The briefing depends on knowing what each setting actually controls.
Short reference:

- **auto-publish**: whether successful checkin automatically publishes
  to `publish-registry`. Off means publishing is manual.
- **visibility**: default public/private on the target registry. On
  `cg` this is a no-op (all `cg` widgets are public). On other
  registries, private means invited-only.
- **governance**: whether community members can propose changes to
  published widgets. `open` allows proposals, `protected` restricts
  edits to the owner.
- **publish-registry**: prefix of the registry that receives publishes.
  Defaults to `cg`. Custom prefixes route to user-added registries.
- **cloud**: whether Cartograph queries cloud registries at all.
  Disabled means library is local-only.
- **show-unavailable**: whether search includes widgets whose language
  engine isn't installed here. They surface but can't install until
  the engine is present.
- **auto-update**: whether Cartograph nudges the user about new CLI
  releases.
- **paths.&lt;binary&gt;**: override PATH lookup for a specific engine
  binary. Only meaningful when auto-detection fails.

## The change loop (both modes)

In Briefing mode: after the three paragraphs, ask "anything here you
want to change?" and enter the change loop.

In Recommendation mode: after the user confirms a profile, enter the
change loop for the settings the profile changes.

For each change request:

1. Restate the intent in one sentence so the user can correct you.
2. Apply it.
3. Surface any warning the CLI returns (e.g. "visibility is a no-op
   on cg") without rephrasing — the CLI's wording is the source of
   truth.
4. Move to the next change.

One change at a time. Don't batch.

## Scope

This skill explains **what the user has configured**. It does not
teach the end-to-end publishing workflow, proposal review, or
widget-first planning. If the user moves into those areas, let the
conversation end cleanly — this skill doesn't follow them there.

## What not to do

- Don't read every setting aloud in a briefing; synthesize into the
  three paragraphs.
- Don't explain what a setting *could* be unless the user is asking
  to change it.
- Don't editorialize. State mechanics, let the user decide.
- Don't invent defaults. The config output surfaces them.
- Don't list all four profiles when the user has already named an
  intent — narrow first.
- Don't apply a profile as an opaque operation. Show the diff
  (current → new) for each key that changes.
- Don't drift between modes mid-conversation. Briefing stays a
  briefing; recommendations are opt-in.
