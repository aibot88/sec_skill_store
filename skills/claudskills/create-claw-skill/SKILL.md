---
name: create-claw-skill
description: >
  This skill should be used when the user asks to "create an OpenClaw skill",
  "make a claw skill", "build a skill for OpenClaw", "write a SKILL.md for openclaw",
  "add a skill to openclaw", "generate openclaw skill frontmatter", "create a clawhub skill",
  "port a skill to OpenClaw", "convert a Claude Code skill to claw",
  "migrate my skill to openclaw", or wants to author a new skill or port an existing
  Claude Code skill for the pi-coding-agent / OpenClaw ecosystem.
argument-hint: "[skill|command] [name] - or leave empty to interview"
---

# OpenClaw Skill & Command Generator

Generate well-structured OpenClaw skills or slash commands. Both are SKILL.md files with YAML frontmatter — they share the same structure but differ in how they're triggered and described. OpenClaw uses the AgentSkills spec (pi-coding-agent) with its own frontmatter fields, tool names, and path conventions distinct from Claude Code.

## Phase 0: Fetch Current Documentation

**Before generating**, retrieve the latest OpenClaw skill documentation:

```bash
clawdocs get "tools/skills" --no-header -q
```

Capture any frontmatter fields or options not already listed in `{baseDir}/references/frontmatter-options.md`. If `clawdocs` is unavailable, proceed with current references — they are sufficient. If new fields appear, use them and note the update.

## Phase 1: Understand Requirements

Parse `$ARGUMENTS` for type hint. Users are often unclear on OpenClaw-specific conventions. Interview to gather:

1. **Primary objective** — What should this skill do?
2. **Trigger scenarios** — When should it activate? What exact phrases would a user say?
3. **Inputs/outputs** — What does it receive and produce?
4. **Complexity** — Simple, standard, or complex workflow?
5. **Gating needs** — Does it require specific binaries, env vars, or config keys? (drives `metadata.openclaw.requires.*`)
6. **Execution needs** — Sub-agent delegation via `sessions_spawn`? Command dispatch (bypass model)?

Proceed to Phase 2 when at minimum Objective and Trigger Scenarios are established.

### Port Mode

When the user provides an existing Claude Code skill to port (file path or pasted content), skip the interview and apply this translation sequence:

1. Read the source skill and all its supporting files (scripts, references, examples)
2. **Frontmatter** — Remove invalid fields (`model`, `context`, `agent`, `allowed-tools`, `hooks`, `license`). Add `metadata` with `requires` if scripts need specific binaries. See `{baseDir}/references/frontmatter-options.md` for valid fields.
3. **Tool names** — Apply the translation table from `{baseDir}/references/claw-patterns.md`: `Bash`→`exec`, `Read`→`read`, `Write`→`write`, `Edit`→`edit`, `Glob`/`Grep`→`exec`+`find`/`rg`, `WebSearch`→`web_search`, `WebFetch`→`web_fetch`, `Task`→`sessions_spawn`, `AskUserQuestion`→conversational asking
4. **Paths** — Replace `$CLAUDE_PLUGIN_ROOT` with `{baseDir}`. Remove `@file` injection and bang-backtick references.
5. **Scripts/references** — Copy as-is if they are platform-neutral Python with no Claude Code SDK dependencies. Update any internal tool name references.
6. Proceed directly to Phase 2 Step 7 (Validate) with translated content, then Phase 3 (Deliver).

## Phase 2: Generate

Apply throughout generation: use imperative voice and terse phrasing because every token in a generated skill body costs budget on every invocation. Prefer instruction over example — state the rule with its reasoning so it generalizes to every input.

**Initialize directory first (when creating a new skill directory, not editing an existing file):**

```bash
python3 {baseDir}/scripts/init_claw_skill.py <name> --path <dir> [--resources scripts,references,assets]
```

Exit 0 = directory scaffolded, proceed to Step 1. Exit 1 = naming collision; ask user whether to overwrite or rename.

### Step 1 — Choose type

- **Skills:** Trigger-rich, third-person description ("This skill should be used when..."); auto-triggered by routing
- **Commands:** Concise, verb-first description, under 60 chars; user-invoked via `/` menu
- **Dispatch commands:** `command-dispatch: tool` with `command-tool` — bypasses model entirely, routes directly to a named tool (rare; for pure pass-through cases)

### Step 2 — Write frontmatter

Read `{baseDir}/references/frontmatter-options.md` for the full OpenClaw field catalog, description patterns, and the `metadata` single-line JSON constraint.

Key constraint: **`metadata` must be a single-line JSON object on one line.** Multi-line YAML mappings under `metadata` are not valid in OpenClaw.

**Description density rules:** Keep descriptions under ~400 characters / ~100 tokens (600 chars / 150 tokens absolute max) — they load every session. Per the OpenClaw cost formula, each skill costs `195 + 97 + field lengths` characters in the system prompt; a 10-skill install with verbose descriptions burns significant context on routing metadata alone. Derive trigger phrases from the user's actual words in Phase 1, not paraphrases. See the token budget and trigger derivation principles in `{baseDir}/references/frontmatter-options.md`.

**Intensional over extensional** — state the rule with its reasoning rather than listing examples that imply the rule. An intensional rule generalizes to every input the skill will encounter; an extensional list only covers the shapes shown.

### Step 3 — Validate description discoverability

Before writing the body, verify the description will route correctly. Mentally generate:

1. **3 should-trigger prompts** — realistic user messages that should activate this skill. Include at least one naive phrasing from a user who has never heard of the skill.
2. **3 should-NOT-trigger prompts** — messages in adjacent domains that are close but should not activate. These test whether the description is too broad.

Evaluate: does the description cover all should-trigger prompts? Would it plausibly reject the should-NOT-trigger prompts? If coverage is weak, revise the description — add missing trigger phrases, tighten language to exclude adjacent domains, or add a negative trigger ("Not for X").

This step catches routing misses before the rest of the skill is built. Proceed when description coverage is adequate.

### Step 4 — Write body

**Construction rules:**
- State objective explicitly in first sentence
- Use imperative voice ("Analyze", "Generate", "Identify") — no first-person ("I will", "I am")
- Context only when necessary for understanding
- XML tags only for complex structured data
- No "When to Use This Skill" section — body loads only after triggering; routing guidance there is never read by the routing decision
- Avoid headers deeper than H3 — deep nesting signals content that belongs in `references/`, not `SKILL.md`
- `{baseDir}` is the path variable for skill-relative file references (substituted before model sees the skill body)

Both skills and commands follow the same body pattern:

```markdown
# Name

Brief overview (1-2 sentences).

## Process
1. Step one (imperative voice)
2. Step two
3. Step three
```

**Dynamic Content:**

| Syntax | Purpose |
|--------|---------|
| `$ARGUMENTS` | All arguments as string |
| `$1`, `$2`, `$3` | Positional arguments |
| `{baseDir}` | Absolute path to skill directory (substituted at load time) |

Note: `@file` injection and bang-backtick command expansion are Claude Code features specific to Claude Code's skill loader implementation — the pi-coding-agent skill loader only supports `{baseDir}` path substitution and does not implement these extensions. Do not use them in generated OpenClaw skills.

### Step 5 — Script opportunity scan

Read `{baseDir}/references/script-patterns.md` and apply the five signal patterns to every workflow step in the skill being generated:

| Signal | Question | If yes → |
|--------|----------|----------|
| **Repeated Generation** | Does any step produce the same structure with different params across invocations? | Parameterized script in `scripts/` |
| **Unclear Tool Choice** | Does any step combine multiple operations in a fragile sequence naturally expressible as one function? | Script the procedure |
| **Rigid Contract** | Can you write `--help` text for this step right now without ambiguity? | CLI candidate |
| **Dual-Use Potential** | Would a user want to run this step from the terminal, outside the skill workflow? | Design as proper CLI from the start |
| **Consistency Critical** | Must this step produce bit-for-bit identical output for identical inputs? | Script — never LLM generation |

For each identified script candidate:
1. Choose the archetype from `{baseDir}/references/script-patterns.md` (init/validate/transform/package/query)
2. Scaffold the script in `scripts/` using the Python template from `{baseDir}/references/script-patterns.md`
3. Wire it into SKILL.md with: trigger condition, exact invocation using `exec` tool, output interpretation

**Wiring rule:** A script reference must state *when* to invoke (trigger condition), *how* to invoke (exact command with flags), and *what to do* with the result (exit code handling, which output fields matter).

Scripts are invoked via the `exec` tool (not `Bash`). Reference paths using `{baseDir}/scripts/script.py`.

### Step 6 — Check delegation

Read `{baseDir}/references/claw-patterns.md` for delegation patterns, `sessions_spawn` usage, cross-skill reference conventions, and tool group translations (Claude Code → OpenClaw tool name mapping).

Scan for existing resources before finalizing:

```
Review available OpenClaw skills (check ~/.openclaw/skills/ and workspace/skills/)
For each workflow step, ask: "Do we already have this?"
```

**Common delegation patterns:**
- To invoke another OpenClaw skill: tell the model to read `{baseDir}/../<other-skill>/SKILL.md` via the `read` tool, or instruct the user to type `/<other-skill-name>`
- For background delegation: use `sessions_spawn` (non-blocking; result announced back to chat)
- Documentation lookups: `exec: clawdocs get "<slug>" --no-header -q`

There is no `Skill` tool in OpenClaw — skills are invoked by the routing model, not programmatically from within another skill.

### Step 7 — Validate

When generating a new skill directory (not editing an existing single file):

```bash
python3 {baseDir}/scripts/validate_claw_skill.py <skill-directory> --output json
```

Exit 0 = proceed to Phase 3. Exit 1 = parse the `errors` array; each entry has `field`, `message`, `severity`. Resolve all `critical` and `major` items before writing to disk.

### Explain Your Choices

When presenting the generated skill/command to the user, briefly explain:
- **What you set and why** — "Added `metadata.openclaw.requires.bins: [jq]` because the skill calls jq in a subprocess"
- **What you excluded and why** — "Left `user-invocable` at default (true), `command-dispatch` omitted (skill routes through model)"
- **Add more trigger phrases if routing misses expected inputs**

## Phase 3: Deliver

### Output Paths

| Type | Location | When active |
|------|----------|-------------|
| Workspace skill | `<workspace>/skills/<name>/` | Next session in that workspace |
| Managed skill | `~/.openclaw/skills/<name>/` | Shared across all agents on this machine |

Skills are session-snapshotted — changes take effect on the next new session, not the current one.

### Write and Confirm

Before writing:
```
Writing to: [path]
This will [create new / overwrite existing] file.
Proceed?
```

### After Creation

Summarize what was created:
- Name and type
- Path and when it takes effect
- How to invoke/trigger
- Suggested test scenario

### Publish to ClawHub

Invoke only when the user explicitly requests distribution:

```bash
clawhub publish <skill-directory> --slug <slug> --version X.Y.Z --tags latest
```

Exit 0 = published. Exit 1 = validation or auth failure; read stdout for details.

## Phase 4: Evaluate

Score the generated skill/command:

| Dimension | Criteria |
|-----------|----------|
| **Clarity (0-10)** | Instructions unambiguous, objective clear |
| **Precision (0-10)** | Appropriate specificity without over-constraint |
| **Efficiency (0-10)** | Token economy — maximum value per token |
| **Completeness (0-10)** | Covers requirements without gaps or excess |
| **Usability (0-10)** | Practical, actionable, appropriate for target use |

**Target: 9.0/10.0.** If below, refine once addressing the weakest dimension, then deliver.

Re-run `validate_claw_skill.py` after any revisions and verify the validation checklist below before finalizing.

## Degrees of Freedom

| Level | When to Use | Format |
|-------|-------------|--------|
| **High freedom** | Multiple valid approaches, context-dependent decisions | Text instructions, heuristics |
| **Medium freedom** | Preferred pattern exists, some variation acceptable | Pseudocode, scripts with parameters |
| **Low freedom** | Fragile operations, consistency critical, specific sequence required | Exact scripts, few parameters |

## Quality Standards

**Format Economy:**
- Simple task → direct instruction, no sections
- Moderate task → light organization with headers
- Complex task → full semantic structure

**Remove ruthlessly:** Filler phrases, obvious implications, redundant framing, excessive politeness

## Validation Checklist

Before finalizing an OpenClaw skill or command:

**Structure:**
- [ ] SKILL.md exists with valid YAML frontmatter
- [ ] Frontmatter has `name` and `description` fields
- [ ] `metadata` field (if present) is single-line JSON on one line
- [ ] Markdown body is present and substantial
- [ ] Referenced files actually exist

**Description Quality:**
- [ ] Uses third person ("This skill should be used when...")
- [ ] Includes specific trigger phrases users would say (verbatim)
- [ ] Trigger phrases derived from user's actual words, not formalized paraphrases
- [ ] Under ~400 chars (~100 tokens); 600 chars (~150 tokens) absolute max
- [ ] Negative triggers present if adjacent skills could false-trigger
- [ ] Lists concrete scenarios ("create X", "configure Y")
- [ ] Not vague or generic

**OpenClaw Correctness:**
- [ ] No Claude Code-only fields: no `model`, `context`, `agent`, `allowed-tools`, `hooks`, `license`
- [ ] No Claude Code tool names referenced in body: no `Bash`, `WebSearch`, `WebFetch`, `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Task`, `Skill`, `AskUserQuestion`, `EnterPlanMode`, `ExitPlanMode`
- [ ] Uses OpenClaw tool names: `exec`, `read`, `write`, `edit`, `web_search`, `web_fetch`, `sessions_spawn`
- [ ] Uses `{baseDir}` for skill-relative paths (not `$CLAUDE_PLUGIN_ROOT`)
- [ ] Output path is OpenClaw workspace (`<workspace>/skills/`) or managed (`~/.openclaw/skills/`)

**Content Quality:**
- [ ] Body uses imperative/infinitive form, not second person
- [ ] Body is focused and lean (1,500–2,000 words ideal, <5k max)
- [ ] Detailed content moved to `references/`
- [ ] Scripts are executable and documented
- [ ] Script opportunities identified via five signal patterns
- [ ] Script references in SKILL.md include trigger condition, invocation (`exec`), output handling
- [ ] Consistency-critical steps are scripted, not left to LLM re-generation

**Progressive Disclosure:**
- [ ] Core concepts in SKILL.md
- [ ] Detailed docs in `references/`
- [ ] Utilities in `scripts/`
- [ ] SKILL.md references these resources
- [ ] `examples/` present if skill produces user-adaptable output (see `{baseDir}/examples/sample-command/SKILL.md` for a minimal command example)

## Error Handling

| Issue | Action |
|-------|--------|
| Unclear requirements | Ask clarifying questions before generating |
| Missing context | Request usage examples or target scenarios from user |
| Path issues | Verify target directory exists; let `init_claw_skill.py` create it |
| Type unclear | Default to skill (auto-triggered) if user hasn't specified |
| `clawdocs` unavailable | Proceed with current references — they are sufficient |

---

Execute phases sequentially. Always fetch current documentation first.
