# Adding a Skill

Step-by-step guide for creating and publishing a new skill in the jitsu-skills ecosystem.

---

## 1. Choose a Persona

Every skill belongs to one of 7 personas. Pick the one that best matches your skill's domain:

| Persona | ID | Domain |
|---------|-----|--------|
| Campaign Ops | `campaign-ops` | Outbound campaigns, lead enrichment, multi-channel sequencing |
| Ship Captain | `ship-captain` | Open source publishing, npm releases, changelogs |
| Guardian | `guardian` | Security auditing, secret scanning, vulnerability detection |
| Machinist | `machinist` | macOS automation, LaunchAgents, Keychain management |
| Architect | `architect` | Full-stack development, database schemas, data visualization |
| Researcher | `researcher` | R&D proposals, citations, research apps |
| Coordinator | `coordinator` | Meeting prep, team updates, cross-tool orchestration |

If none of these fit, propose a new persona in your PR with an `id`, `label`, `icon`, `color`, and `description`. New personas require maintainer approval.

---

## 2. Create the Skill Directory

```bash
mkdir skills/<skill-name>
```

Use kebab-case for the directory name. Keep it descriptive -- `campaign-sequencer`, not `cs`.

---

## 3. Write SKILL.md

Create `skills/<skill-name>/SKILL.md` with YAML frontmatter followed by the markdown body.

### Frontmatter Schema

```yaml
---
name: my-skill-name
description: >
  What this skill does and when to trigger it. Write in third person.
  Must be under 1024 characters. Include trigger phrases so Claude's
  description-matching can auto-activate the skill. Example: "Scans
  git history for committed secrets and credentials. Triggered when
  the user asks to check for leaked keys, audit git history, or scan
  for secrets."
license: AGPL-3.0-or-later
metadata:
  author: your-github-handle
  version: "1.0.0"
  persona: one-of-seven-personas
---
```

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | Must match the directory name. Kebab-case. |
| `description` | Yes | Under 1024 characters. Third person. Include trigger phrases. |
| `license` | Yes | Always `AGPL-3.0-or-later` for core skills. |
| `metadata.author` | Yes | Your GitHub handle. `0xjitsu` for core skills. |
| `metadata.version` | Yes | Semver string in quotes (e.g., `"1.0.0"`). |
| `metadata.persona` | Yes | One of: `campaign-ops`, `ship-captain`, `guardian`, `machinist`, `architect`, `researcher`, `coordinator`. |

### Body Structure

After the closing `---` of the frontmatter, write the skill's instruction body in markdown. Include these sections:

**When to Trigger** -- List the exact phrases and intents that should activate this skill. Be specific. Claude uses description matching, so the more trigger patterns you list, the better auto-activation works.

```markdown
## When to Trigger

Activate this skill when the user:
- Asks to **scan for secrets** or **audit git history**
- Says "check for leaked keys" or "find exposed credentials"
- Is preparing a repository for open source release
```

**Workflow Steps** -- The numbered sequence of actions the skill performs. Be explicit about tool usage, file operations, and decision points.

```markdown
## Workflow

1. Read the project root to identify language and framework
2. Run `grep -r` patterns for common secret formats
3. Present findings grouped by severity
4. Guide the user through remediation
5. Re-scan to verify all issues are resolved
```

**MCP Tools Used** (if any) -- Wrap MCP-dependent sections in `<!-- claude-code-only -->` tags so they get stripped from the portable version.

```markdown
<!-- claude-code-only -->
## MCP Tools

This skill uses the following MCP servers when available:
- **Supabase MCP** -- for schema introspection
- **Sentry MCP** -- for error context
<!-- /claude-code-only -->
```

**Output Format** -- Describe the expected deliverable: a file, a terminal report, a structured JSON object, etc.

**Safety Rules** -- Hard boundaries the skill must never cross. Examples: "Never delete files without confirmation", "Never commit secrets", "Never push to remote without asking".

**Anti-Patterns** -- Common mistakes to avoid. Examples: "Do not run `git add .`", "Do not skip the verification scan", "Do not suggest disabling security checks".

---

## 4. Generate Portable Versions

Run the build script from the repo root:

```bash
bash scripts/build-universal.sh
```

This iterates over every `skills/*/SKILL.md` and generates two files per skill:

| File | What it contains | Target platform |
|------|-----------------|-----------------|
| `prompt.txt` | Body only, frontmatter stripped | Claude Chat (paste into Project Instructions), Agent SDK (inject as `systemPrompt`) |
| `prompt-portable.txt` | Body with `<!-- claude-code-only -->` sections also stripped | Prompt marketplaces, harnesses without tool access |

Never edit `prompt.txt` or `prompt-portable.txt` by hand -- they are always regenerated from `SKILL.md`.

---

## 5. Add to Skill Tree

Edit `skills/skill-data.json` to register your skill in the dependency graph.

### Add a Node

Add an entry to the `nodes` array:

```json
{
  "id": "my-skill-name",
  "label": "My Skill Name",
  "persona": "guardian",
  "tier": 1,
  "description": "One-line description of what the skill does",
  "status": "available",
  "prerequisites": ["core"],
  "platforms": ["claude-code", "claude-chat", "agent-sdk"]
}
```

| Field | Values | Notes |
|-------|--------|-------|
| `id` | string | Must match the directory name and SKILL.md `name` |
| `label` | string | Human-readable display name |
| `persona` | string | One of the 7 persona IDs |
| `tier` | `0`, `1`, or `2` | `0` = core (reserved), `1` = standalone (depends only on core), `2` = requires other skills as prerequisites |
| `description` | string | Short description for CLI and tree display |
| `status` | `"available"` or `"locked"` | Use `"available"` for tier-1 skills. `"locked"` for tier-2 skills whose prerequisites are not yet mastered |
| `prerequisites` | array of IDs | Skill IDs this skill depends on. At minimum `["core"]` for tier-1 skills |
| `platforms` | array | Subset of `["claude-code", "claude-chat", "agent-sdk"]`. Use only platforms the skill actually works on |

### Add Edges

Add one edge per prerequisite relationship to the `edges` array:

```json
{ "source": "core", "target": "my-skill-name" }
```

If your skill is tier-2 with multiple prerequisites, add one edge for each:

```json
{ "source": "prerequisite-a", "target": "my-skill-name" },
{ "source": "prerequisite-b", "target": "my-skill-name" }
```

---

## 6. Test Locally

Symlink your skill into the Claude Code skills directory:

```bash
ln -s $(pwd)/skills/my-skill-name ~/.claude/skills/my-skill-name
```

Then start a new Claude Code session and test:

- **Slash command**: Type `/my-skill-name` to invoke it directly
- **Auto-trigger**: Describe a task that matches the trigger phrases in your description -- Claude should auto-detect and activate the skill
- **Verify output**: Confirm the skill follows its workflow, respects safety rules, and produces the expected output format

Also verify the CLI recognizes your skill:

```bash
bun bin/cli.js list   # Should show your skill with correct persona
bun bin/cli.js tree   # Should show your skill in the prerequisite graph
```

---

## 7. Submit a PR

1. **Branch from main**: `git checkout -b skill/my-skill-name`
2. **One skill per PR** -- keep the diff focused
3. **Include all generated files**: `SKILL.md`, `prompt.txt`, `prompt-portable.txt`, and the updated `skill-data.json`
4. **PR checklist**:
   - [ ] `SKILL.md` has valid frontmatter (name, description under 1024 chars, license, metadata)
   - [ ] `bash scripts/build-universal.sh` completes with 0 errors
   - [ ] `bun bin/cli.js list` shows the new skill
   - [ ] `bun bin/cli.js tree` renders the prerequisite graph correctly
   - [ ] Skill tested via symlink in a live Claude Code session
   - [ ] MCP-dependent sections wrapped in `<!-- claude-code-only -->` tags
   - [ ] No secrets, PII, or hardcoded credentials in the skill body
