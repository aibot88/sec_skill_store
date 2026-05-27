---
name: bfrost-worker-author
description: Scaffold and review a new BFrost worker without touching the core. Use when the user asks to "add a worker", "create a BFrost worker", "build a publisher/producer/consumer for the Item Bus", or otherwise extend BFrost with a new capability. Enforces the worker-first contract — no edits to `src/` outside `src/workers/` and no edits to `web/src/` outside `web/src/workers/`.
---

# BFrost worker author

This skill helps an operator add a new BFrost worker — a producer, a consumer, an assistant tool, a channel adapter, or a model provider — without modifying core code. Every capability in BFrost is a worker. The platform never needs a core change to gain a feature; if a worker can't express what the user wants, that's a contract gap to surface, not a reason to patch `src/`.

## Trigger criteria

Activate this skill when the user asks to:

- create, scaffold, or add a new BFrost worker
- add a producer or consumer to the Item Bus
- add an assistant tool, channel adapter, or model provider
- "publish to X / Mastodon / BlueSky" or any similar new destination
- extend BFrost with a capability that the existing built-in workers don't cover

Do **not** activate this skill for: bug fixes inside an existing worker, modifications to the registry/scheduler/admin server, frontend refactors, or anything that is clearly core work the user has explicitly framed as core.

## Hard rules — non-negotiable

The whole point of BFrost is that adding a feature does not touch the core. While operating under this skill:

1. **Never edit files in `src/` outside `src/workers/`.** No edits to `src/admin-server.ts`, `src/agent.ts`, `src/bot.ts`, `src/cron.ts`, `src/jobs/queue.ts`, `src/jobs/item-bus.ts`, `src/llm.ts`, `src/scheduler.ts`, `src/job-runner.ts`, `src/index.ts`, `src/config.ts`, `src/health.ts`, `src/workers/registry.ts`, `src/workers/validation.ts`, `src/workers/loader.ts`, `src/workers/build.ts`, `src/workers/bootstrap.ts`, `src/workers/storage.ts`, `src/workers/db.ts`, `src/workers/local.ts`, `src/workers/types.ts`, `src/sdk.ts`, or `src/sdk-runtime.ts`. If the worker seems to require it, **stop and surface the contract gap to the user** — do not paper over it with a core edit.

2. **Never edit files in `web/src/` outside `web/src/workers/`.** Worker dashboards live in `web/src/workers/builtin/<id>/dashboard.tsx` (built-in) or ship inside the worker directory as `dashboard.tsx` (local). `web/src/App.tsx`, `web/src/styles.css`, and `web/src/workers/registry.ts` are off-limits.

3. **Prefer local workers under `workers/local/<id>/` for new contributions.** Built-in workers under `src/workers/builtin/` are reserved for reference examples shipped with the platform; only add one when the user explicitly asks for a built-in.

4. **Never bundle a private copy of `react`, `react-dom`, `react/jsx-runtime`, or the `bfrost` SDK.** The host owns those singletons. The build pipeline already externalises them.

5. **Never commit secrets to `worker.json`.** Credentials live in `.env` and are read at runtime. The manifest only declares `secret-reference` fields with placeholder defaults.

6. **Never add code that loads workers from remote URLs.** Loading is local-disk only by design.

If the user explicitly overrides one of these rules, restate the rule, ask the user to confirm with a one-line "yes I want to break this for reason X", and only then proceed. Log the decision in the resulting PR description so a reviewer sees it.

## Workflow

Follow these steps in order. Stop and confirm with the user between any step where the next decision is irreversible (file layout, worker ID, builtin vs local).

### 1. Establish the worker's role

Ask the user, in one short message, only what you cannot infer from context:

- **Producer or consumer?** (or both, or neither — neither = tool/channel/provider worker)
- **What `itemType` does it produce or subscribe to?** If consuming, default to `news.article` and confirm.
- **Does it need credentials?** (Google, X, an HTTP API key, etc.)
- **Does it need a dashboard tab, or only Config-tab settings?**
- **Built-in or local?** Default to local. Only choose built-in if the user names a `core.*` ID and explicitly asks for one.

Don't ask the user to invent things `workers/README.md` already specifies (manifest version, API version, lifecycle hooks, storage APIs). Read those from the docs and propose defaults.

### 2. Pick the worker ID

- Local: `local.<short-noun>` (e.g. `local.mastodon-publisher`, `local.bookmark-feeder`).
- Built-in (rare): `core.<category>.<short-noun>` (e.g. `core.publisher.mastodon`).

The ID is permanent — it appears in `worker.<id>.<key>` KV namespaces, `worker_<safeId>_<table>` SQLite table prefixes, and `metadata[id]` Item Bus namespaces. Renaming an ID later orphans state. Choose carefully and confirm with the user before scaffolding.

### 3. Scaffold the directory

Local worker (default):

```
workers/local/<id-without-prefix>/
  worker.json
  src/
    index.ts        ← BackendWorkerModule
  dashboard.tsx     ← only if dashboard.surfaceIds is declared
  README.md         ← what it does, what it produces/consumes, what env vars it reads
```

Built-in worker (only on explicit request):

```
src/workers/builtin/<id>/
  manifest.ts
  module.ts
  job.ts            ← only if it owns a scheduled job
  routes.ts         ← only if it owns admin API routes
  README.md
```

Then read `workers/examples/complete-capability/worker.json` and copy the structure — every field is documented inline.

### 4. Write the manifest

Required: `manifestVersion: 1`, `bfrostApiVersion: "0.1"`, `id`, `name`, `version: "0.1.0"`, `description` (one sentence).

Decision tree:

- **Worker takes scheduled action** → declare `jobs: [...]` with `defaultCron`, `paramsSchema` (Zod), `defaultParams`, optional `prompt`.
- **Worker is callable by the assistant** → declare `tools: [...]` with `inputSchema` and `execute`.
- **Worker reaches a chat surface** → declare `channels: [...]` with capability flags and lifecycle methods.
- **Worker provides an inference backend** → declare `providers: [...]` with capability flags and a `ProviderAdapter`.
- **Worker needs operator config** → declare `dashboard.settings[].fields` with `text` / `textarea` / `number` / `boolean` / `select` / `string-list` / `secret-reference` field types. Use `seedPath` to seed the form from live state.
- **Worker needs credentials** → declare `requiredCredentials` / `optionalCredentials` keyed to the health check the user must satisfy.
- **Worker needs an external binary** → declare `requiredDependencies` / `optionalDependencies`.

For the job runner contract, prompt template, and lifecycle hooks, follow `docs/worker-authoring.md` and copy the matching reference (news for producers, publisher-x or `workers/examples/wordpress-publisher/` for consumers, memory for tools, channels-telegram for channels, providers-lmstudio for providers).

### 5. Wire storage and the Item Bus

- Private state: `import { openWorkerKv, openWorkerDb } from 'bfrost'`. Never reach for a raw better-sqlite3 handle. See `docs/item-bus.md` for shape and migration rules.
- Cross-worker communication: `import { publishItem, listItemsForConsumer, applyConsumerSuccess, applyConsumerFailure, setConsumerMetadata, readConsumerMetadata, withQueueLock, loadQueue, saveQueue } from 'bfrost'`.
- A consumer writes only into `metadata[<its-own-workerId>]`. Never write into another worker's namespace.
- For a producer, choose a stable `itemType` namespace (`<workerId-or-domain>.<noun>`).

### 6. LLM calls

When a worker calls `generateText` (or `streamText`), follow this pattern to stay compatible with local models served by LMStudio:

**Prepend `/no_think` to the user prompt.** Qwen3 and similar local models with extended-thinking mode enabled will otherwise put all their output in the reasoning/thinking block and return an empty `text` field. Other models (OpenAI, Anthropic) silently ignore this prefix.

```ts
const { text } = await generateText({
  model: getChatModel(modelOption),
  system: SYSTEM_PROMPT,
  prompt: '/no_think\n' + buildPrompt(input),
  timeout: config.jobLlmTimeoutMs,
});
```

**Do not set `maxOutputTokens` in the SDK call.** LMStudio's OpenAI-compatible server treats `max_tokens` as part of the total context budget (input + output). If the prompt is large and `max_tokens` is set explicitly, the server may return an empty response when `input_tokens + max_tokens` approaches the context window. Rely on the server-level context length (`LMSTUDIO_CONTEXT_LENGTH`, default 16 384) to provide headroom.

**Cap content excerpts in prompts to ~1000 chars per item.** With a 16 384-token context window and several enriched items in the prompt, full article text (up to 4 000 chars each) will exhaust the budget before the model can generate its response. 1000 chars is enough for relevance judgement. Store the full content in the queue payload for downstream workers that need it.

**Improve the error log on parse failure.** When the model returns something that can't be parsed, log the raw output with clear delimiters before throwing — this makes the problem immediately visible when you re-run the job:

```ts
} catch (err) {
  const preview = text.length > 3000 ? text.slice(0, 3000) + `\n… (truncated, total ${text.length} chars)` : text;
  console.log('[WorkerName] LLM parse error — raw output follows:\n--- LLM OUTPUT BEGIN ---\n' + preview + '\n--- LLM OUTPUT END ---');
  throw new Error(`LLM output not valid: ${err instanceof Error ? err.message : err}`);
}
```

### 8. Tests

Local workers should ship a unit test next to the job/tool that exercises the public manifest contract and any non-trivial parsing or scoring. Built-in workers add a `*.test.ts` next to their `manifest.ts` / `job.ts` — see `news/runs.test.ts` for the pattern.

Run:

```bash
npx tsc --noEmit
npm test
```

before declaring done. Both must pass.

### 9. Verify the worker loads

```bash
npm run build && npm start
```

Then in the dashboard's Workers tab: rescan, find the new worker, enable it, click Run now (if it owns a job), inspect the run, then disable it. If anything fails (manifest validation, compile error, runtime error), the error appears next to the worker row.

### 10. Document

Every worker ships a one-page `README.md` inside its directory covering: what it does, what `itemType` it produces or consumes, which credentials it reads, which env vars it expects, which settings it owns, and any non-obvious operational caveats. Treat this as a hard requirement for the contract — operators rely on it.

## Calibration

- A new producer/consumer worker is usually **one manifest, one job runner, one README, one test, < 300 LOC**. If you find yourself writing more than that, you are probably re-implementing something core already provides. Stop and re-read `workers/README.md`.
- If the proposed worker requires editing the dashboard payload shape, the queue schema, the scheduler, or the registry, **the design is wrong**. Workers contribute slices through declared hooks. Surface the contract gap; do not patch core.

## When stuck

If the worker contract genuinely can't express what the user needs:

1. Stop writing code.
2. State the gap in plain language: "I'd need to write into `metadata[other-worker]` to coordinate, but the contract forbids it" — quote the rule.
3. Offer the user two paths: (a) reshape the worker to fit the contract, (b) open a roadmap issue for a contract extension and pause this work.

Never close the gap by editing core silently. That is exactly the failure mode this skill exists to prevent.

## References

- `workers/README.md` — manifest fields, lifecycle, storage, Item Bus, examples.
- `docs/worker-authoring.md` — consolidated authoring guide (scaffold-to-ship walkthrough).
- `docs/item-bus.md` — Item Bus and per-worker storage reference.
- `workers/examples/simple-job/` — minimal manifest-only worker.
- `workers/examples/research-style-job/` — manifest with health, settings, dashboard route.
- `workers/examples/complete-capability/` — full anatomy reference.
- `workers/examples/wordpress-publisher/` — full consumer worker with backend routes, LLM-driven content generation, configurable prompt, and WP REST integration.
- `workers/examples/dashboard-view/` — runtime-loaded React dashboard view.
- `src/workers/builtin/news/` — reference producer.
- `src/workers/builtin/publisher-x/` — reference consumer.
- `src/workers/builtin/memory/` — reference assistant-tool worker.
- `src/workers/builtin/channels-telegram/` — reference channel worker.
- `src/workers/builtin/providers-lmstudio/` — reference provider worker.
