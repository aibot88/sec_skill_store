---
id: pulumi-specialist
name: pulumi-specialist
type: skill
version: 1.0.0
domain: [infra]
platform: [pulumi]
task: [debugging, review]
maturity: validated
description: >
  Deep-dive Pulumi stack review, component design, Automation API audit, and
  secrets management. Use for structured investigations of Pulumi stack drift,
  ComponentResource coupling, ESC configuration, and Automation API workflows.
  Triggers on: "Pulumi audit", "stack review", "Automation API review",
  "ComponentResource design", "ESC audit", "Pulumi secrets", "Pulumi testing".
argument-hint: "<stack name, project path, or problem description>"
tools: Read, Grep, Glob, Bash
effort: max
model: opus
---

# Pulumi Specialist

Structured investigation for Pulumi infrastructure codebases. Five phases:
gather context, diagnose, design, recommend, verify.

## Arguments

- `$0` — stack name, project path, or problem description. Required.

---

## Phase 1: Context Gathering

1. Identify the Pulumi project:
   ```bash
   cat Pulumi.yaml
   pulumi stack ls
   ```
2. Inspect the active stack config:
   ```bash
   pulumi config --show-secrets
   pulumi stack output
   ```
3. Glob for Pulumi source files:
   ```bash
   find . -name "*.ts" -o -name "*.py" -o -name "*.go" | grep -v node_modules | sort
   ```
4. Check for Automation API usage:
   ```bash
   grep -r "LocalWorkspace\|RemoteWorkspace\|createStack\|selectStack" . \
     --include="*.ts" --include="*.py" --include="*.go" -l
   ```

---

## Phase 2: Diagnosis

**Stack health:**

```bash
pulumi preview --diff
pulumi stack --show-ids
```

**Resource graph:**

```bash
pulumi stack graph --dependency-graph /tmp/graph.dot
dot -Tsvg /tmp/graph.dot -o /tmp/graph.svg   # if graphviz available
```

**Secret exposure check:**

```bash
pulumi config --show-secrets | grep -i "key\|secret\|password\|token"
pulumi stack output --show-secrets
```

**Test coverage:**

```bash
find . -name "*.test.ts" -o -name "*_test.go" -o -name "test_*.py" | sort
```

---

## Phase 3: Design / Root-Cause Analysis

Map symptoms to causes:

| Symptom                          | Common Causes                                      | Check                                          |
| -------------------------------- | -------------------------------------------------- | ---------------------------------------------- |
| Unexpected resource replace      | Input property changed that triggers replacement   | `pulumi preview --diff` — look for `[replace]` |
| Stack output leaks secret        | Output not marked `secret: true`                   | `pulumi stack output --show-secrets`           |
| ComponentResource missing output | Output not registered in `registerOutputs`         | Check `this.registerOutputs({...})` call       |
| Automation API stack timeout     | Long provisioning, no timeout configured           | Add `OnEvent` handler + timeout options        |
| ESC env not loaded               | `esc env open` not called; ESC not linked to stack | `pulumi config env ls`                         |

Cite `file:line` for every finding.

---

## Phase 4: Recommendations

Output findings in priority order:

```
[CRITICAL] <title>
Resource: <logical name or file:line>
Issue: <one sentence>
Evidence: <preview output or code snippet>
Fix: <specific change, with code diff>
Trade-off: <alternative and its downside, if meaningful>
```

Order: CRITICAL → WARNING → INFO.

---

## Phase 5: Verification

After fixes are applied:

1. `pulumi preview` — zero unexpected changes; no `[replace]` for unintended resources.
2. `pulumi stack output` — no secrets in plaintext output.
3. Unit tests pass: `npm test` / `go test ./...` / `pytest`.
4. For Automation API changes: run the program with `--preview` mode and verify event callbacks fire.
5. For ESC changes: `esc env open <org>/<project>/<env>` and confirm values resolve correctly.

---

## Reference Docs

| File                     | When to use                                                |
| ------------------------ | ---------------------------------------------------------- |
| `stack-design.md`        | Stack topology, StackReference, multi-stack patterns       |
| `component-resources.md` | ComponentResource design, inputs/outputs, lifecycle        |
| `automation-api.md`      | Embedding `pulumi up`/`destroy` in Node/Python/Go          |
| `secrets.md`             | Config secrets, ESC, output sensitivity, encryption        |
| `testing.md`             | Unit mocks, integration tests, Automation API test harness |
