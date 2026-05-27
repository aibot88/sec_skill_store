---
name: intent-recognition
description: "Use BEFORE any tool call that could modify state, touch sensitive targets, rewrite history, install dependencies, publish packages, or expose credentials/environment data. Classifies intent into Passive/Read, Reconnaissance, Modification, or Destructive/Irreversible using operation type plus target sensitivity, then runs Identify / Confirm / Verify before action. Do NOT use for deciding what code to write, executing already-classified work, reactive post-execution guardrails, or defining upstream governance policy."
license: MIT
compatibility: "Runtime-agnostic. The four-tier classification, target-content rule, and Identify/Confirm/Verify sequence apply to any agent harness with tool execution — Claude Code, OpenCode, Cursor, Aider, Copilot Workspace, custom MCP-based agents, or any LLM with shell access."
allowed-tools: Read Grep
metadata:
  schema_version: "4"
  version: "1.0.0"
  type: capability
  category: engineering
  domain: ai-engineering/safety
  scope: portable
  owner: skill-graph-maintainer
  freshness: "2026-05-06"
  drift_check: "{\"last_verified\":\"2026-05-06\"}"
  eval_artifacts: planned
  eval_state: unverified
  routing_eval: absent
  stability: experimental
  keywords: "[\"intent recognition\",\"pre-execution risk classification\",\"four tier action taxonomy\",\"passive read reconnaissance modification destructive\",\"identify confirm verify sequence\",\"destructive operation classification\",\"credential read is reconnaissance\",\"git reset hard is destructive\",\"force push is destructive\",\"lockfile install is high impact\",\"non-destructive alternative\",\"agent action risk assessment\",\"tool call pre-execution gate\",\"reading dotenv is not passive\",\"history rewriting is irreversible\",\"state-changing tool call\",\"agent safety pre-execution\",\"target content elevates tier\"]"
  examples: "[\"the agent is about to run `git reset --hard` — what tier is this and what's the safer alternative?\",\"is reading the `.env` file a Passive operation since nothing mutates?\",\"I'm about to install a new package — what tier does that fit and why?\",\"force-push to main looks like 'just a push' — should I classify it as Modification?\",\"before running `DELETE FROM orders WHERE …`, what's the verification sequence?\",\"the agent classified everything as Modification because there's no exception for credentials\",\"what trigger phrases should activate this skill in our harness?\"]"
  anti_examples: "[\"design the deterministic safety hook that blocks destructive commands\",\"decide whether to use a switch or a chain of ifs\",\"actually execute the migration after we've classified the risk\",\"scan this repo for OWASP top 10 vulnerabilities\",\"review this AI-generated PR for correctness\",\"the loop is stalling — what's the steering signal\"]"
  relations: "{\"boundary\":[{\"skill\":\"owasp-security\",\"reason\":\"owasp-security is a domain audit against a known threat list; intent-recognition is the per-action risk classification that runs immediately before a tool call regardless of domain\"},{\"skill\":\"debugging\",\"reason\":\"debugging investigates a failure that has already happened; intent-recognition prevents one class of failure (destructive action mis-classification) from happening at all\"},{\"skill\":\"code-review\",\"reason\":\"code-review evaluates code-quality of an artefact; intent-recognition evaluates risk of an action about to be performed by a tool\"},{\"skill\":\"version-control\",\"reason\":\"version-control owns the discipline of using git well; intent-recognition specifically classifies which git commands are safe vs destructive at the moment of execution\"},{\"skill\":\"testing-strategy\",\"reason\":\"testing-strategy decides what to test proactively; intent-recognition gates one specific tool call from firing without classification\"}],\"related\":[\"owasp-security\",\"version-control\",\"debugging\"],\"verify_with\":[\"owasp-security\"]}"
  portability: "{\"readiness\":\"scripted\",\"targets\":[\"skill-md\"]}"
  lifecycle: "{\"stale_after_days\":365,\"review_cadence\":\"quarterly\"}"
  skill_graph_source_repo: "https://github.com/jacob-balslev/skill-graph"
  skill_graph_protocol: Skill Metadata Protocol v3
  skill_graph_project: Skill Graph
  skill_graph_canonical_skill: skills/intent-recognition/SKILL.md
---

# Intent Recognition

## Coverage

Pre-execution action classification for any agent that can call tools with side effects. Defines four tiers — Passive/Read, Reconnaissance, Modification, Destructive/Irreversible — with the operation-and-target rule that determines tier (the target's sensitivity can elevate the tier above what the operation alone implies; reading a `.env` file is Reconnaissance even though no state changes). Specifies the three-step verification sequence (Identify the action and its tier, Confirm the rationale against the active plan, Verify whether a non-destructive alternative exists) that runs before any tier-3 or tier-4 action fires. Names the trigger phrases that should activate the skill. Catalogs the anti-patterns: classifying credential reads as Passive, treating package installs as Passive, skipping classification for familiar commands, classifying force-push as Modification, proceeding with Destructive actions without checking alternatives.

## Philosophy

Agents execute tool calls at machine speed with no undo. Without an explicit pre-execution classification step, `git reset --hard` runs with the same ease as `cat README.md`. The cost of a single misclassified destructive action — wiped uncommitted work, dropped database, force-pushed branch — exceeds the cost of _every_ classification step the agent will ever run. The math is simple: classification is cheap, regret is expensive.

The most subtle failure mode is _target-content elevation_. Reading a file is a Passive operation in the abstract. Reading a `.env` file is Reconnaissance because the _target_ is sensitive — credentials, connection strings, API keys. The tier comes from the combination of operation _and_ target, not the operation alone. A classifier that looks only at the verb misses half the risk surface.

The Identify / Confirm / Verify sequence is the second non-negotiable. _Identify_ surfaces the agent's own reasoning about the action; if the agent can't state the tier and the rationale, it shouldn't fire the tool. _Confirm_ tests the action against the agreed plan — drift between "what we agreed to do" and "what the next tool call will do" is itself a signal. _Verify_ asks whether a safer alternative exists and is the step where most preventable destructive actions get caught.

## 1. The Four-Tier Taxonomy

| Tier | Name                           | Examples                                                                                                                                                                       | Risk                                                      |
| ---- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------- |
| 1    | **Passive / Read**             | View a non-sensitive file, list a directory, grep for a string                                                                                                                 | Low                                                       |
| 2    | **Reconnaissance**             | Read `.env`, view a `credentials.*` file, run a SQL `SELECT` against a sensitive table, list installed packages and versions                                                   | Moderate (information exposure even without state change) |
| 3    | **Modification**               | Write or edit a source file, run a routine `git commit`, run a non-destructive `INSERT` or `UPDATE` with a `WHERE` clause                                                      | Standard                                                  |
| 4    | **Destructive / Irreversible** | `git reset --hard`, `git push --force`, `DROP TABLE`, `TRUNCATE`, `DELETE FROM ...` without `WHERE`, `rm -rf`, `npm publish`, credential rotation, dependency lockfile rewrite | Critical — requires explicit justification                |

Every tool call gets a tier before it fires. No exceptions, including for "familiar" commands.

## 2. Operation-vs-Target Rule

The tier comes from the combination of _operation_ and _target_. The same operation has a different tier depending on what it touches.

| Operation | Generic target              | Sensitive target                                        | Tier shift                                   |
| --------- | --------------------------- | ------------------------------------------------------- | -------------------------------------------- |
| Read      | Source file                 | `.env`, `credentials.*`, private key                    | Passive → Reconnaissance                     |
| Read      | Local DB                    | Production DB or secrets table                          | Passive → Reconnaissance                     |
| Write     | Source file                 | Lockfile, environment config, public-key registry       | Modification → Modification (still standard) |
| Run       | Script with no side effects | Script with side effects (install, deploy, mutate prod) | Passive → Modification or Destructive        |
| Git push  | Topic branch                | Main / master, force-push                               | Modification → Destructive (force-push)      |

When in doubt about the target, classify _up_, not down.

## 3. The Identify / Confirm / Verify Sequence

Before executing any tier-3 or tier-4 tool call:

### Identify

State explicitly:

- The exact action (full command, full target path)
- The classified tier
- The reason this action is needed

If the agent cannot complete this sentence — "I'm about to run X (tier Y) because Z" — it shouldn't fire the tool. Inability to articulate is itself a stop signal.

### Confirm

Check the action against the active plan or task spec:

- Was this action agreed to?
- Does the spec name the same target?
- If the action escalates a previously-agreed tier (e.g., the spec said "modify"; the proposed action is "destroy"), is the escalation explicitly authorized?

Drift between agreed action and proposed action is the signal. The right response to drift is to _re-confirm with the human_, not to proceed.

### Verify

Ask: is there a non-destructive alternative that achieves the same goal?

| Destructive                     | Non-destructive alternative                                        |
| ------------------------------- | ------------------------------------------------------------------ |
| `git reset --hard`              | `git revert` (preserves history) or `git stash` (preserves work)   |
| `git push --force`              | `git push --force-with-lease` (fails if remote moved unexpectedly) |
| `DROP TABLE x`                  | `ALTER TABLE x RENAME TO x_archived_<date>` (reversible)           |
| `DELETE FROM x WHERE condition` | `UPDATE x SET deleted_at = now() WHERE condition` (soft delete)    |
| `rm -rf <dir>`                  | `mv <dir> <dir>.archived.<date>` (still on disk; recoverable)      |
| `npm publish`                   | `npm publish --dry-run` first (sees the package; doesn't push)     |
| Lockfile rewrite                | Smaller dependency change scoped to one package                    |

If a non-destructive alternative exists and the destructive form was not specifically requested, prefer the non-destructive form.

## 4. Trigger Phrases

The skill should activate before any tool call where the agent is about to:

- Modify or write a file (`Write`, `Edit`, `MultiEdit`, `replace_file_content`, …)
- Run a git command that mutates state (`commit`, `push`, `reset`, `rebase`, `merge`, `cherry-pick`, `branch -D`, `tag`, `stash drop`)
- Run a database query that mutates state (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `TRUNCATE`, `ALTER`, `CREATE`)
- Run an install / publish / deploy command (`npm/pnpm/yarn install`, `npm publish`, `vercel deploy`, `cargo publish`, `pip install`, `apt install`, `gh repo edit`)
- Run a shell command with `&&`, `||`, `;`, `|` chains that include any of the above
- Read any file matching `.env*`, `credentials*`, `id_rsa*`, `*.pem`, `*.key`, `secrets.*`, `keystore*`

These triggers are deliberately broad. False positives (classifying a Passive action as needing a tier check) are cheap; false negatives (firing a Destructive command without classification) are the failure mode this skill exists to prevent.

## 5. Anti-Patterns

| Anti-pattern                                                      | Why it fails                                                                                                                          | Correct approach                                                    |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Classifying _all_ reads as Passive                                | A read of `.env` is Reconnaissance — credential exposure is the risk even with no state change                                        | Check operation _and_ target type                                   |
| Treating `npm install` / `pnpm install` as Passive                | Lockfile rewrites and node_modules churn affect reproducibility and can pull in compromised packages                                  | Classify any environment-affecting command as at least Modification |
| Skipping classification for "familiar" commands                   | `git push` is routine; `git push --force origin main` is Destructive — flags change tier                                              | Classify every tool call regardless of familiarity                  |
| Classifying force-push as Modification                            | Force-push rewrites remote history and cannot be `git checkout`-ed back                                                               | Any history-rewriting or unrecoverable action is Destructive        |
| Proceeding with Destructive without checking alternatives         | `git reset --hard` instead of `git revert` is the single most common preventable loss                                                 | Run the Verify step every time                                      |
| Conflating Reconnaissance with Passive because "no state changes" | Information exposure (logging credentials, leaking connection strings into chat history) is itself a state change at the system level | Reconnaissance is its own tier for a reason                         |

## Verification

- [ ] Before any tier-3 or tier-4 tool call, the agent has stated the action, the tier, and the reason in plain text
- [ ] Operation-and-target rule was applied — sensitive targets elevated the tier above what the operation alone would suggest
- [ ] The Confirm step checked the action against the agreed plan; any drift was re-confirmed with the human, not proceeded past
- [ ] The Verify step considered at least one non-destructive alternative and either chose it or named why the destructive form is required
- [ ] No tool call fired without an explicit tier classification — no exceptions for "familiar" commands
- [ ] The trigger-phrase list is the activation contract, not a suggestion: any matching command runs through the sequence

## Do NOT Use When

| Use instead                                                                         | When                                                                                                                                                                              |
| ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A hook-based guardrail (deterministic blocker, e.g. PreToolUse hook in Claude Code) | Setting up _reactive_ / _structural_ enforcement that fires on a pattern match in the harness — that is hook-pattern territory; this skill is the agent-side cognitive classifier |
| A code-quality / code-logic skill                                                   | Deciding _what_ the code should do — implementation correctness rather than action risk                                                                                           |
| Task execution                                                                      | Actually doing the work after classification has cleared the action                                                                                                               |
| `owasp-security`                                                                    | A domain audit against a known threat catalog (Top 10) — that is a class of investigation, not per-action classification                                                          |
| `code-review`                                                                       | Reviewing an artefact for quality — orthogonal to action-risk classification                                                                                                      |
| `version-control`                                                                   | The general discipline of using git well — this skill is the moment-of-execution gate on specific git commands                                                                    |
