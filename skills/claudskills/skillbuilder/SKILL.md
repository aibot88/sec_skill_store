---
name: skillbuilder
description: "Build flawless Claude Code skills. Studies existing skills as reference, ensures correct format, and pushes for genuine intelligence — skills that exploit something specific about how Claude works. SKIP for one-off scripts, prompts, or task helpers."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
effort: high
---

# /skillbuilder

Build Claude Code skills that are genuinely intelligent — not just format-valid, but skills that exploit something specific about how Claude works.

Reference standard: the skills in this repo. Study them before drafting.

| Skill | What it exploits |
|-------|------------------|
| `/stochastic` | LLM variance — poll N runs, aggregate consensus/divergences/outliers |
| `/model-chat` | Disagreement — multi-agent debate surfaces assumptions a single pass misses |
| `/fanout` | Parallelism — independent researchers cover more ground, Opus synthesizes |
| `/autoresearch` | Measurement loops — read code, mutate, measure, keep-or-revert, repeat |

Every good skill exploits something. The question isn't "which of 8 buckets" — it's "what does this skill do that a raw prompt can't?"

## Quality bar

A skill is worth building if:
1. **Reusable** — works across many tasks, not a one-shot
2. **Exploits something** — LLM variance, parallelism, measurement, memory, gates, whatever
3. **Beats a prompt** — materially changes Claude's execution, not just vocabulary
4. **Passes the removal test** — delete the skill, output measurably degrades

If the answer to "what does this exploit" is "nothing, it's just instructions" — that's a prompt, not a skill.

## Anti-patterns

1. **Task helper.** "Skill that writes commit messages." That's a prompt. "Skill that spawns 3 agents to review, vote, kill weak verbs" — that's a skill.
2. **Best-practice list.** Documentation isn't a skill. A checklist that gates SHIP/NOT SHIP is.
3. **Prompt-equivalent.** If a one-shot prompt produces the same output, don't build a skill.
4. **Single-use.** "Skill to set up my repo." That's a script.
5. **Decoration.** Skill exists to feel useful but doesn't change execution.
6. **Token bloat.** SKILL.md > 250 lines of best-practice advice Claude would do anyway.
7. **Generic naming.** `/helper`, `/assistant`, `/improve-X`. Names should name what it does or what it exploits.

## Operations

### `craft` — build a new skill

Input: domain or problem. Output: working `skills/{name}/SKILL.md`.

**Flow:**
1. **Study references.** Read existing skills in this repo. What patterns apply?
2. **Identify the exploit.** What will this skill do that a raw prompt can't? If nothing — stop, recommend a prompt instead.
3. **Draft the skill** following the template below.
4. **Write to disk.** `skills/{name}/SKILL.md`
5. **Report.** Path, what it exploits, restart required.

### `audit` — check an existing skill

Input: skill name or path. Output: **lands** · **needs work** · **kill it**.

**Flow:**
1. Read the SKILL.md.
2. Identify what it exploits. Implicit or missing → needs work.
3. Run anti-patterns 1-7. Any hit → needs work or kill.
4. Removal test: would Claude's output degrade without this skill?
5. Verdict + one move.

### `kill` — diagnose a failing skill

Input: skill name + symptom. Output: fix or kill.

**Flow:**
1. What was it supposed to exploit? Has it drifted?
2. Anti-pattern check.
3. One move: sharpen, narrow, or kill.

## Skill template

```yaml
---
name: {kebab-case}
description: "TRIGGER when {specific signal}. {What it does in one phrase}. SKIP for {anti-domain}."
user-invocable: true
allowed-tools:
  - {minimum needed}
effort: {default | high}
---

# /{name}

{What this skill does. What it exploits — why it beats a raw prompt.}

## Reference

{If applicable: similar skills, shipped products, or patterns this builds on.}

## How it works

{The mechanism. What Claude does differently when this skill is loaded.}

## Anti-patterns

{Domain-specific failure modes to avoid.}

## Output

{What the skill produces. Format, structure, deliverable.}
```

## Frontmatter spec

| Field | Required | Notes |
|-------|----------|-------|
| `name` | yes | kebab-case, matches folder name |
| `description` | yes | TRIGGER when... SKIP for... — this is how Claude decides to load it |
| `user-invocable` | yes | `true` if user can call it directly |
| `allowed-tools` | yes | minimum needed — don't over-grant |
| `effort` | yes | `default` (single-pass) or `high` (spawns agents, long-running) |

## Allowed-tools — minimum needed

- `Read` — almost always
- `Agent` — if it spawns sub-agents
- `Bash` `Glob` `Grep` — for codebase work
- `Write` — only if it persists state
- `WebSearch` `WebFetch` — only if it does live research

Don't grant tools the skill doesn't use.

## Naming

- **Mechanism-named** — `/stochastic`, `/fanout` (names the how)
- **Domain-named** — `/autoresearch`, `/skillbuilder` (names the what)
- **Avoid** — `/helper`, `/assistant`, `/better-X`, `/improve-Y`

## After writing

1. Tell user to restart Claude Code
2. Test: invoke in fresh conversation, verify trigger matches
3. Check: does output beat a raw prompt?

## Voice

- Lead with what it exploits
- Every claim cites a reference (existing skill or shipped product)
- If it's a prompt in disguise, say so
- Short sentences, specific mechanisms
- One skill per run
