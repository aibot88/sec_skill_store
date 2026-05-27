---
name: using-git-notes-for-ai-context
description: "Reads, writes, and configures git notes and trailers for AI agent context — attribution, decision reasoning, prompts, and CI/CD metadata. Sets up namespace conventions, hook automation, team sync, and compliance. Use when storing AI attribution in git, setting up git notes for AI tracking, querying constraints or directives before modifying code, configuring notes sync for a team, choosing between git notes and trailers, or when the user mentions git notes, git trailers, AI attribution, AI provenance, Lore protocol, or decision context in commits."
category: Agent Tooling
---

# Using Git Notes for AI Context

Git notes and trailers form a zero-infrastructure metadata layer for AI agent
context. Notes attach post-hoc metadata without changing commit SHAs. Trailers
embed structured key-value pairs inside commit messages.

## Notes vs. trailers

| Scenario | Use |
|----------|-----|
| Known at commit time, concise (<5 lines) | **Trailer** |
| Known at commit time, verbose | **Note** |
| Post-hoc (after commit) | **Note** |
| Attribution data | Note → `ai/attribution` |
| Prompts / sessions | Note → `ai/prompts` |
| Constraints, rejected alternatives, directives | Trailer (Lore protocol) |
| CI/CD output | Note → `ci/*` |
| Deployment records | Note → `deployments` |

**Rule of thumb:** If the metadata should travel with the commit and be visible
in `git log`, use trailers. If the metadata is post-hoc, verbose, or
machine-generated, use notes.

When authoring commits, keep subject/body format aligned with the repository's
commit convention; this skill focuses on metadata structure, storage, and
querying.

## Workflows

Identify the task, then follow the matching workflow.

### Annotating commits with AI context

1. Decide notes vs. trailers using the table above.
2. For **notes** — select the namespace per
   [references/01-core-concepts-and-namespaces.md](references/01-core-concepts-and-namespaces.md)
   §Namespace Scheme:
   ```bash
   git notes --ref=ai/attribution add -m \
     '{"schema":"ai-context/1.0","agent":{"tool":"claude-code","model":"claude-opus-4-6"}}' HEAD
   ```
3. For **trailers** — include footer lines in the commit message during
   commit creation (using your team's normal commit flow), for example:
   ```text
   AI-Agent: claude-code/claude-opus-4-6
   Constraint: Must remain backward-compatible
   ```
4. Verify: `git notes --ref=ai/attribution show HEAD` or
   `git log -1 --format='%(trailers)' HEAD`.
5. To automate, install hooks — see
   [references/03-hooks-scripts-and-automation.md](references/03-hooks-scripts-and-automation.md).

### Querying context before modifying code

1. Harvest existing constraints, directives, and rejected approaches:
   ```bash
   git log --format='%(trailers:key=Constraint,key=Directive,key=Rejected)' -- <file>
   ```
2. Check AI attribution notes:
   ```bash
   for sha in $(git log --format='%H' -- <file>); do
       git notes --ref=ai/attribution show "$sha" 2>/dev/null
   done
   ```
3. Use this context to avoid repeating rejected approaches and honor active
   constraints and directives.

### Setting up git notes infrastructure

1. Configure remote sync:
   ```bash
   git config --add remote.origin.fetch '+refs/notes/*:refs/notes/*'
   git config --add remote.origin.push '+refs/notes/*:refs/notes/*'
   ```
2. Configure rebase survival:
   ```bash
   git config --add notes.rewriteRef "refs/notes/ai/attribution"
   git config notes.rewrite.rebase true
   git config notes.rewrite.amend true
   ```
3. Verify sync works:
   ```bash
   git push origin 'refs/notes/*' --dry-run
   ```
4. Install hooks for automatic annotation — see
   [references/03-hooks-scripts-and-automation.md](references/03-hooks-scripts-and-automation.md).
5. For teams: add onboarding script and namespace governance — see
   [references/04-team-enterprise-and-security.md](references/04-team-enterprise-and-security.md).

### Choosing tools

Default recommendations:

- **Line-level AI attribution**: Git AI (`git ai init`) — broadest agent
  support (12+), rebase survival, open standard.
- **Decision context in commits**: Lore protocol trailers — no tool required,
  just trailer conventions.
- **Both**: They complement each other.

For detailed comparison, see
[references/02-use-cases-and-tools.md](references/02-use-cases-and-tools.md)
§Tool Comparison.

## Essential commands

```bash
# Notes
git notes --ref=ai/attribution add -m 'data' HEAD      # Add
git notes --ref=ai/attribution append -m 'more' HEAD    # Append
git notes --ref=ai/attribution show HEAD                 # Read
git log --show-notes=ai/attribution                      # Show in log

# Trailers (read/query)
git log -1 --format='%(trailers)' HEAD                   # Read all
git log --format='%(trailers:key=Constraint)' -- file    # Filter by key
git log -1 --format=%B HEAD | git interpret-trailers --parse  # Parse raw message

# Sync
git push origin 'refs/notes/*'                           # Push all notes
git fetch origin 'refs/notes/*:refs/notes/*'             # Fetch all notes
```

## Edge cases

- **Namespace conflict**: `refs/notes/ai` (bare) cannot coexist with
  `refs/notes/ai/prompts`. Always use sub-paths like `ai/attribution`.
- **Git AI ref conflict**: Git AI occupies `refs/notes/ai` (bare). If using
  Git AI, use non-`ai/` prefixes for custom namespaces (e.g., `dev/prompts`,
  `dev/decisions`) to avoid ref conflicts.
- **Rebase orphans notes**: Configure `notes.rewriteRef` (see "Setting up"
  workflow). Git AI handles this automatically.
- **Notes not synced by default**: Must configure fetch/push refspecs.
- **One note per namespace per object**: Use `append` to add to existing notes,
  or use separate namespaces.
- **No GitHub/GitLab UI display**: Notes are CLI-only — invisible in web UIs.
- **Merge conflicts under concurrency**: Configure merge strategy per
  namespace — see
  [references/04-team-enterprise-and-security.md](references/04-team-enterprise-and-security.md)
  §Merge Strategies.

## Reference material

- [Core concepts and namespaces](references/01-core-concepts-and-namespaces.md)
  — notes/trailers mechanics, namespace scheme, structured JSON format
- [Use cases and tools](references/02-use-cases-and-tools.md) — Lore protocol,
  session metadata, CI/CD, tool comparison
- [Hooks, scripts, and automation](references/03-hooks-scripts-and-automation.md)
  — post-commit/pre-push hooks, GitHub Actions, aliases, context harvest
- [Team, enterprise, and security](references/04-team-enterprise-and-security.md)
  — remote sync, merge strategies, compliance, redaction, signing, limitations
