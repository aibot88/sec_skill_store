---
name: skelm
description: Author, run, and operate skelm pipelines — typed TypeScript orchestrations for agentic and deterministic workflows with default-deny permissions. Use when the user mentions skelm, agent permissions, pipeline.ts, AgentPermissions, skelm.config.ts, MCP servers, or wants to scaffold a workflow.
license: MIT
compatibility: Requires Node 20+, pnpm or npm, and the `skelm` package installed globally or as a workspace dependency.
metadata:
  homepage: https://github.com/scottgl9/skelm
  version: "0.3.7"
allowed-tools: Read Edit Write Bash(pnpm:*) Bash(skelm:*) Bash(node:*) Bash(git:*)
---

# skelm Skill

## When to activate

Activate when the user is working in a skelm project, wants to author or modify a `*.pipeline.mts` / `*.workflow.mts` file, asks about `AgentPermissions`, `skelm.config.ts`, MCP server wiring, or wants to run, inspect, or operate a pipeline.

---

## The unit of work

A **pipeline** is a TypeScript file that exports a `pipeline()` call. It has:

- `id` — stable string identifier
- `description` — optional human-readable summary
- `input` / `output` — Zod schemas (validated at run boundaries)
- `steps` — ordered array of `Step` values
- optional `finalize` — transforms accumulated step outputs into the declared output shape

**Step kinds:** `code | llm | agent | parallel | forEach | branch | loop | wait | pipelineStep | idempotent`

Import everything from `'skelm'` (or `'@skelm/core'` in library contexts — `'skelm'` re-exports `'@skelm/core'`).

---

## Authoring a pipeline

Minimal example — one deterministic step:

```ts
import { code, pipeline } from 'skelm'
import { z } from 'zod'

export default pipeline({
  id: 'greet',
  description: 'Greets a user by name.',
  input: z.object({ name: z.string().min(1) }),
  output: z.object({ greeting: z.string() }),
  steps: [
    code({
      id: 'build-greeting',
      run: (ctx) => {
        const { name } = ctx.input as { name: string }
        return { greeting: `hello, ${name}` }
      },
    }),
  ],
})
```

Access prior step outputs via `ctx.steps['step-id']`. Access run metadata via `ctx.run.runId`.

For multi-step composition, LLM inference, and control flow, see [references/pipeline-authoring.md](references/pipeline-authoring.md).

---

## Adding an LLM step

`llm()` is for single-shot inference — chat-completion-style requests with optional structured output. The recommended backend is `'openai'` (the OpenAI factory talks to anything that exposes the OpenAI Chat Completions shape: hosted OpenAI, vLLM, llama.cpp, sglang, ollama with `/v1`):

```ts
import { llm, pipeline } from 'skelm'
import { z } from 'zod'

export default pipeline({
  id: 'classify',
  input: z.object({ text: z.string() }),
  output: z.object({ label: z.string(), confidence: z.number() }),
  steps: [
    llm({
      id: 'classify-text',
      backend: 'openai',
      prompt: (ctx) =>
        `Classify the sentiment and return JSON { label, confidence }:\n${ctx.input.text}`,
      output: z.object({ label: z.string(), confidence: z.number() }),
      maxTokens: 1024,
    }),
  ],
})
```

When `output` is supplied, the runtime requests structured output from the backend and validates the parsed JSON against the schema before recording it.

---

## Adding an agent step

> **Default-deny:** every `AgentPermissions` field defaults to deny when omitted. An agent with no `permissions` block cannot call tools, read files, execute binaries, attach MCP servers, or make network requests.

The recommended agent backend is `'pi'` (the [pi coding-agent SDK](https://www.npmjs.com/package/@earendil-works/pi-coding-agent), via `@skelm/pi` → `createPiSdkBackend`). The CLI's `pi` config key wires up the **RPC** backend; for the SDK backend, register an instance.

```ts
// skelm.config.ts
import { defineConfig } from 'skelm'
import { createPiSdkBackend } from '@skelm/pi'

export default defineConfig({
  backends: { agent: 'pi' },
  instances: [createPiSdkBackend({ id: 'pi' })],
})
```

Minimal agent step with explicit permissions:

```ts
import { agent, pipeline } from 'skelm'
import { z } from 'zod'

export default pipeline({
  id: 'ticket-to-pr',
  input: z.object({ ticketId: z.string() }),
  output: z.object({ prUrl: z.string() }),
  steps: [
    agent({
      id: 'implement',
      backend: 'pi',
      prompt: (ctx) =>
        `Implement ticket ${(ctx.input as { ticketId: string }).ticketId}. Return JSON {prUrl}.`,
      permissions: {
        allowedTools:       ['gh.*'],                      // GitHub CLI tools (prefix match)
        allowedExecutables: ['git'],
        allowedMcpServers:  ['github'],
        allowedSkills:      [],
        fsRead:             ['./'],
        fsWrite:            ['./src/', '/tmp/'],
        networkEgress:      { allowHosts: ['api.github.com'] },
      },
      output: z.object({ prUrl: z.string() }),
      workspace: { mode: 'ephemeral', cleanup: 'on-run-end' },
      maxTurns: 8,
    }),
  ],
})
```

For full `agent()` options, workspace modes, MCP wiring, and multi-turn control, see [references/agent-step.md](references/agent-step.md).

---

## Permissions are part of the API

The permission model has these dimensions. Every field is optional and defaults to deny.

| Dimension   | Field                              | Description                                          |
|-------------|------------------------------------|------------------------------------------------------|
| Profile     | `profile`                          | Named profile from `skelm.config.ts` to apply first  |
| Tool        | `allowedTools` / `deniedTools`     | Tool ids; `'gh.*'` is sugar for prefix match; `'*'` allows everything |
| Executable  | `allowedExecutables`               | Binaries allowed for any exec/bash tool              |
| MCP server  | `allowedMcpServers`                | MCP server ids the agent may attach                  |
| Skill       | `allowedSkills`                    | Skill ids the agent may load                         |
| Secret      | `allowedSecrets`                   | Secret names the step may resolve via `SecretResolver` |
| Network     | `networkEgress`                    | `'allow'` \| `'deny'` \| `{ allowHosts: [...] }`     |
| FS read     | `fsRead`                           | Path roots the agent may read                        |
| FS write    | `fsWrite`                          | Path roots the agent may write                       |
| Approval    | `approval`                         | `{ on: PermissionDimension[], rememberFor?: number }` — gate dimensions on human approval |

**Composition is intersection-only.** Project defaults → permission profile → step-level permissions. Each layer can only narrow, never widen. If a project default denies network and a step sets `networkEgress: 'allow'`, the resolved policy is still deny.

Named profiles in `skelm.config.ts`:

```ts
defaults: {
  permissionProfiles: {
    'read-only':  { fsRead: ['./'], networkEgress: 'deny' },
    'full-write': { fsRead: ['./'], fsWrite: ['./'], networkEgress: 'allow' },
  },
}
```

Apply a profile in a step: `permissions: { profile: 'read-only', allowedTools: ['rg'] }` — the step's allowedTools are still intersected with the profile.

See [references/permissions.md](references/permissions.md) for the full enforcement model.

---

## Project layout

```
my-project/
├── skelm.config.ts          # Required for gateway and agent steps
├── workflows/
│   └── hello.workflow.mts    # One pipeline per file
├── package.json             # { "dependencies": { "skelm": "^0.3.7", "zod": "^4" } }
└── tsconfig.json
```

Pipeline files may be named `*.workflow.{mts,ts}` or `*.pipeline.{mts,ts}` — the discovery glob in `skelm.config.ts` decides what gets registered.

For `skelm.config.ts` shape and all config options, see [references/config.md](references/config.md).

---

## Running and inspecting

```bash
# Run once, pass input as JSON
skelm run ./workflows/ticket-to-pr.workflow.mts --input '{"ticketId":"PROJ-42"}'

# Run with input from file
skelm run ./workflows/ticket-to-pr.workflow.mts --input-file input.json

# Run a workflow project by directory (resolves skelm.config `entrypoint`,
# else index.workflow.mts, else the single workflow file in the dir)
skelm run ./builder --input '{"spec":"..."}'

# List discovered pipelines
skelm list

# Describe a pipeline (human-readable or mermaid diagram)
skelm describe <workflow-id-or-path>
skelm describe <workflow-id-or-path> --format mermaid

# View run history
skelm history --last 10 --json
```

Full CLI reference at [references/cli.md](references/cli.md). Exit codes: `0` ok, `1` CLI error, `2` schema validation, `3` run failed, `4` cancelled, `5` wait timeout, `6` permission denied.

---

## The gateway is the trust boundary

The gateway owns all security-critical infrastructure: permission resolution, secret resolution, audit log, approval gating. **Never write permission enforcement in pipeline or step code** — call gateway helpers or use `TrustEnforcer` from `@skelm/core` only in tests and demos.

```bash
skelm gateway start            # foreground; SIGTERM/Ctrl-C drains and exits
skelm gateway status           # shows pid / url / state
skelm gateway stop             # stop a running gateway
skelm gateway install --systemd  # install ~/.config/systemd/user/skelm-gateway.service
```

Agent steps are enforced by the gateway at dispatch time. A step that declares `allowedMcpServers: ['github']` cannot attach any other server, regardless of what the backend requests. See [references/gateway.md](references/gateway.md).

---

## Tests are not optional

Every behavior change ships with tests. For permission paths:

- **Default-deny fixture** — prove the action is denied when the permission field is omitted.
- **Explicit-deny fixture** — prove the action is denied when the field is present but excludes the target.
- Both fixtures are required, not one or the other.

```bash
pnpm check   # build → typecheck → lint → unit → guards → adversarial → contract → doc-links
```

Never claim a task done until `pnpm check` is green.

---

## Common pitfalls

- **Widening at step level** — setting `networkEgress: 'allow'` in a step when the project default is `deny` has no effect. Intersection always wins.
- **Missing Zod schema** — `input` / `output` are validated at run boundaries; omitting them skips validation silently.
- **`agent()` with an unregistered backend** — the step fails at runtime if `backend` references an id with no matching entry under `backends:` and no matching instance in `instances:`. The pi SDK backend in particular must be added to `instances:` (the CLI's `pi` shorthand wires the RPC variant only).
- **Editing `dist/`** — generated files; never edit. Run `pnpm build` to regenerate.
- **Step id collisions inside `parallel()`** — sibling ids must be unique; the runtime tracks uniqueness globally per run.

---

## Scaffold a new pipeline

```bash
bash skill/skelm/scripts/new-pipeline.sh my-pipeline "What this pipeline does"
```

This copies `assets/pipeline.template.ts` to `./my-pipeline.pipeline.mts` and substitutes the id and description. Use `assets/agent-pipeline.template.ts` for pipelines that include an agent step.
