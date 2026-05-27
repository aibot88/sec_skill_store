---
name: robotframework
description: "Use this skill for general Robot Framework work: authoring `.robot` suites, tasks, keywords, variables, resource files, execution, dry runs, tags, Rebot/Libdoc usage, and Python test-library patterns. Trigger when the user mentions Robot Framework, `.robot` files, keywords, libraries, resource files, tasks, listeners, Libdoc, Rebot, or Robot Framework syntax and execution."
metadata:
  author: kundeng
  version: "2.1.0"
---

# Robot Framework

Use this skill for general Robot Framework authoring, refactoring, execution,
and Python library work.

This is the broad Robot Framework skill. It is not `wise-rpa-bdd`, which is
for browser-extraction-oriented BDD/RPA suites with a fixed generic-keyword
contract.

## Start Here

Classify the task first:

1. **Suite work**: write or refactor `.robot` suites
2. **Keyword design**: extract or reshape user keywords and resources
3. **Execution**: run `robot`, `--dryrun`, tags, Rebot, pabot
4. **Library work**: create or edit Python libraries
5. **Framework extension**: listeners, remote libraries, dynamic APIs

Pick the narrowest layer that solves the problem.

## Strong Defaults

- Prefer `.robot` suites plus resource files before Python libraries.
- Prefer high-level user keywords over repeated low-level calls.
- Prefer `*** Test Cases ***` unless the work is genuinely task/RPA shaped.
- Prefer `Test Template` when many rows share one interaction shape.
- Prefer `robot --dryrun` as the first validation step.
- Prefer Python libraries when suite logic starts hiding business intent.

## Core Model

Choose the right layer:

- **suite file**: scenario intent and visible assertions
- **resource file**: shared domain flows, imports, and reusable keywords
- **Python library**: external-system mechanics, parsing, retries, heavy logic

If the suite starts reading like general-purpose program code, move logic down
into Python.

## What Good Looks Like

Good Robot Framework code usually has:

- short test/task bodies
- intention-revealing user keywords
- shared flows in resources instead of copy-paste
- variables in the right place for their scope
- clear execution commands

Bad Robot Framework code usually has:

- giant inline test cases
- one keyword that hides the whole scenario
- duplicated low-level steps across files
- nested control flow doing data shaping in `.robot`
- environment values hardcoded in the suite

## Fast Heuristics

- If a test repeats the same 4-8 steps with different values, use a template or
  shared keyword.
- If multiple suites share the same vocabulary, move it into a resource file.
- If you need nested loops, conditionals, retries, or parsing, use Python.
- If a value varies by environment, do not hardcode it in the suite.
- If the keyword name tries to describe an entire workflow, split it.

## Decision Table

| Need | Default |
|---|---|
| Reusable flow in `.robot` | user keyword or resource file |
| Shared imports / variables / keywords | resource file |
| Same-shape tests with different rows | `Test Template` |
| Heavy data logic or external APIs | Python library |
| Fast structure validation | `robot --dryrun` |
| Merge or regenerate reports | `rebot` |
| Parallel runs | `pabot` |
| Library docs | `libdoc` |

## Working Pattern

When implementing:

1. choose suite vs resource vs library
2. shape the suite body around behavior, not mechanics
3. factor repeated flows into keywords
4. validate with `robot --dryrun`
5. run the narrowest real selection possible

## Read Next

- `references/syntax.md` for exact grammar, variables, control structures,
  `RETURN`, BDD prefixes, continuation rows, and `__init__.robot`
- `references/authoring.md` for suite layout, templates, resources, BDD style,
  variable placement, and refactor boundaries
- `references/execution.md` for `robot`, tag selection, reserved tags,
  argument files, pabot, output files, and Rebot
- `references/library-authoring.md` for Python libraries, decorators, type
  conversion, listeners, dynamic/hybrid APIs, remote libraries, and Libdoc
