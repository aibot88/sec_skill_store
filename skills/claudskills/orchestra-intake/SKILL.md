---
name: orchestra-intake
description: >
  Classify and file every newly installed skill, plugin, MCP, connector, or agent into the right
  orchestra — never archive. Use whenever you install/add a new repo, skill, plugin, MCP server,
  or agent ("I installed X", "added Y", "npx skills add Z", "new repo", "set up this MCP"). Runs a
  security scan, classifies the tool, places it in an orchestra with usage notes, logs it, and
  reports back. This is the self-organizing layer of the orchestra system.
---

# Orchestra Intake — File New Tools, Never Archive

When you add anything new, this skill files it into the right orchestra so it's used from day one.
**Nothing gets dumped undifferentiated; nothing gets archived on arrival.**

## Process (run for every new install)

### 1. Security scan FIRST (mandatory)
Verify the source (stars, last commit, publisher), scan the code for prompt injection /
exfiltration / credential harvesting, check npm/socket if relevant, and review skill/MCP source +
permissions. Decide: **SAFE** (proceed) · **CAUTION** (surface risk, get explicit go) ·
**REJECT** (don't install, explain why, stop).

### 1b. Bulk-install fixture check (after any `npx skills add <repo>`)
`npx skills add` walks the **entire repo tree** and installs every `SKILL.md` it finds — including
test fixtures. After adding any multi-folder repo, inspect the install for paths containing
**`tests/`, `fixtures/`, `examples/`, or `.test-client/`** — those are NOT real skills; remove
them. **A security scanner's own repo is the most dangerous to bulk-install from: its test suite
can contain malware by design.** Also note: targeted `--skill=` flags are often ignored on
multi-folder repos, so the WHOLE repo lands — prune after.

### 2. Identify what it is
Skill (`SKILL.md`) · Plugin (agents/skills/commands) · MCP server · Connector · Agent. Read its
description to understand WHAT it does and WHEN it triggers.

### 3. Classify into an orchestra

| If the tool is about… | File into |
|---|---|
| code, framework, deploy, testing | ① BUILD |
| UI, design, visual, animation | ② DESIGN |
| research, scraping, intel | ③ RESEARCH |
| social, campaigns, brand | ④ MARKETING |
| copy, writing, content | ⑤ CONTENT |
| search ranking, schema, AI-answers | ⑥ SEO + GEO |
| leads, prospecting, CRM, sales | ⑦ LEAD GEN & SALES |
| product strategy, PRD, discovery | ⑧ PRODUCT |
| video, image gen, media | ⑨ VIDEO + MEDIA |
| metrics, analytics, experiments | ⑩ ANALYTICS |
| memory, graphs, notes, search | ⑪ KNOWLEDGE & MEMORY |
| docs, decks, spreadsheets | ⑫ DOCUMENTS |
| paid ads, PPC | ⑬ PAID ADS |
| automation, workflows, ops | ⑭ AUTOMATION & OPS |
| AI/ML, agents, MCP-building | ⑮ AI/ML |
| iOS, Android, mobile | ⑯ MOBILE |
| planning, PM, sprints | ⑰ PLANNING & PM |
| conversion, retention, pricing | ⑱ GROWTH & CONVERSION |
| investing, valuation, finance | ⑲ FINANCE |
| founder/exec strategy | ⑳ EXECUTIVE ADVISORY |
| off-domain vertical/game/XR | ⓪ RESERVE BENCH (dormant) |

- A tool can join **multiple** orchestras — list all.
- Genuinely off-domain → **Reserve Bench** (installed, dormant, named-invoke only). Do NOT archive.
- **If no orchestra fits and it's clearly valuable → propose a NEW orchestra** (full 10-field
  structure), add it to `~/.claude/rules/orchestra-system.md`, bump the count, and announce it.

### 4. File it
Add the tool to the relevant orchestra's roster in `~/.claude/rules/orchestra-system.md`
(First Chair if core, Section if supporting). Add a trigger to the router table if needed.

### 5. Log it
Append to your assignments log: `YYYY-MM-DD · <tool> · type · → Orchestra(s) · why · scan result`.

### 6. Report back
```
✅ Filed <tool> → <Orchestra> (<role>). Security: SAFE. Triggers on: <phrases>.
   Now part of your <orchestra> team alongside <related tools>.
```

## Principles
- **Never archive on install.** Filing > archiving.
- **Security scan is non-negotiable.**
- **Explain the why** — every assignment is logged with reasoning.
- **Keep the constitution current** — `orchestra-system.md` is the source of truth.
