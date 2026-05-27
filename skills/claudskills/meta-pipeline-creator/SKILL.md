---
name: meta-pipeline-creator
description: Author or edit pipeline JSON files in pipelines/. Trigger: create a pipeline, automate a workflow, or add tasks to an existing pipeline.
paths:
  - 'pipelines/**'
---

Write all pipeline content in **English**, regardless of the project's primary language.

## Examples

Six reference patterns in `examples/`:

| File | When to use |
|------|-------------|
| `implement__feature-name.yaml` | New implementation — implement → review → test gate → commit. Covers feature, unit-test, and integration-test sub-types; procedures differ (see below). |
| `review-fix__layer__target.yaml` | Existing code review + fix — initial review outside loop, fix-loop pipeline, commit outside |
| `lint-fix__layer__target.yaml` | Lint rule violations — implement + test gate only (no review agent), commit |
| `optimize__skills__target.yaml` | Skill documentation improvement — implement → review → custom validate gate → commit per target. Same structure as implement-feature but with domain-specific procedures and a custom script gate. |
| `optimize__knowledge__target.yaml` | Knowledge file audit — parallel agents per domain (no reviewer, no nested pipeline), commit at end. Commit agent is generic (does not resume an implementer session). |

### `implement` procedure selection

| Pattern | implementer `procedure` | reviewer `procedure` |
|---------|------------------------|---------------------|
| `implement-feature` | _(none — write detailed `task` instead)_ | `arch/review` |
| `implement-unit-test` | `test-unit/implement` | `test-unit/review` |
| `implement-integration-test` | `test-integration/implement` | `arch/review` |

## Before writing

1. Read `src/types/pipeline.ts` — authoritative schema for all task fields.
2. Read the matching example from `examples/` for the chosen pattern.
3. If tasks will use a procedure, read `procedures/<skill>/<name>.md` to confirm required inputs and which tools it calls.

## Naming files

Place new pipelines in `pipelines/` root. **Never** create files inside `pipelines/done/` or any subdirectory.

Filename format: `<pattern>__<layer>__<target>.(json|yaml|yml)`

- `__` separates namespace segments; `-` separates words within a segment
- All lowercase; no underscores within segments, no camelCase

```
❌ pipelines/review-fix/cli/commands-analyze.json   (subdirectory — forbidden)
✅ pipelines/review-fix__cli__commands-analyze.yaml

❌ pipelines/unitTest__fooService.yaml              (camelCase — forbidden)
✅ pipelines/unit-test__foo-service.yaml
```

## Naming tasks

`name` doubles as the resume key — a second run resumes the named session instead of starting fresh.

- Format: `<taskName>-<role>` where role is a noun: `implementer`, `reviewer`, `committer`
  (e.g. `unit-test-foo-service-implementer`, `unit-test-foo-service-reviewer`)
- Stable: no dates or run numbers; unique across all pipelines in the repo

Omit `name` only for stateless or one-shot tasks.

**Reviewer continuity**: when a pipeline has an initial reviewer followed by a loop reviewer, both agents MUST share the same `name`. The loop run resumes the initial session — the reviewer already knows what violations it found and skips re-scanning from scratch. `procedure` is ignored on resume; the flowchart remains in conversation history. Write the loop reviewer's `task` as a re-review instruction, not a repeat of the initial inputs. Do NOT split into `initial-reviewer` / `loop-reviewer` — that forces a cold-start and wastes tokens re-acquiring context.

See `examples/review-fix__layer__target.yaml` for a complete working example.

## `allowed_tools`

Start minimal, then add:

1. Standard tools: `Read`, `Write`, `Edit`, `Bash`
2. MCP tools the procedure calls — full name `mcp__<server>__<tool>` (e.g. `mcp__perclst__ts_test_strategist`). Missing MCP tools stall the run on a permission prompt.

## Procedures

- Set `procedure` when the task description would otherwise duplicate the procedure's flowchart logic.
- Keep `task` minimal — pass only required inputs (e.g. `target_file_path: src/foo.ts`).
- `procedure` applies on session **start** only; ignored on resume.

## Nested pipelines

Use `type: "pipeline"` to group sequences under a named unit. `name` is required (doubles as `rejected.to` target).

Use a nested pipeline when:

- An outer `script` rejection needs to re-run a multi-agent sequence, not just one agent.
- Multiple independent targets each need isolated failure handling.

Multiple targets → sibling `pipeline` tasks at the top level.

## `ng_output_path` (review rejection)

When a review agent should reject the implement agent:

- Pass `ng_output_path: .claude/tmp/<review-agent-name>` in the review agent's `task`.
- Set `rejected` on the review agent pointing to the implement agent.
- The review agent writes rejection feedback to that file; perclst loops back with it as feedback.

**Stale file cleanup**: Add a `script` task as the **first** item in the outer `tasks` array to delete the file before the pipeline runs:

```json
{ "type": "script", "command": "rm -f .claude/tmp/<ng-output-path-name>" }
```

## Script gates and rejection loops

Add a `script` task after each agent (or nested pipeline) that produces testable output:

- `command`: `npm run test:unit` (not `npm run test`)
- `rejected.to`: the agent or pipeline name to fix the failure
- `rejected.max_retries`: 2–3 is usually sufficient
- The referenced `name` must appear **before** the script task in the same `tasks` array

## Commit task

Assign the commit task to the **implement agent** (resume the same named session). Never create a standalone commit agent — the implement agent leaves knowledge after committing and has the full context of what changed and why.

Place the commit agent **outside** the nested pipeline, after the outer script gate. Use the **same `name`** as the implement agent so perclst resumes the existing session.

See `examples/implement__feature-name.yaml` for a complete working example.

## Validation

Before running, verify the file with:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/validate-name.sh pipelines/<name>.yaml
node ${CLAUDE_SKILL_DIR}/scripts/validate-schema.cjs pipelines/<name>.yaml
```

`validate-name.sh` checks filename conventions (placement, extension, `__` separators).
`validate-schema.cjs` parses the file (YAML → JSON if needed) and validates against `schemas/pipeline.schema.json`.

## Running

```bash
perclst run pipelines/<name>.yaml   # YAML recommended (more token-efficient)
perclst run pipelines/<name>.json
```

## Checklist

- [ ] File at `pipelines/<name>.(json|yaml|yml)` — not in `pipelines/done/` or a subdirectory
- [ ] Filename: `__` namespace separators, `-` word separators, all lowercase
- [ ] Every MCP tool called by a procedure is listed in `allowed_tools`
- [ ] `rejected.to` names an existing task in the same `tasks` array scope
- [ ] Task names unique, follow `<taskName>-<role>` convention (role is a noun: `implementer`, `reviewer`, `committer`)
- [ ] `task` text minimal when `procedure` is set
- [ ] Each agent with testable output is followed by a `npm run test:unit` gate
- [ ] Review agents with `ng_output_path` have `rejected` pointing to the implement agent
- [ ] Nested pipeline `name` is set
