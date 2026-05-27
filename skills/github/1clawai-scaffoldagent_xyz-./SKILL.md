---
name: scaffold-agent
description: >-
  How to use the scaffold-agent npm CLI to generate onchain AI agent monorepos
  (Foundry/Hardhat + Next.js/Vite/Python): npx invocation, -y flags, agent.json,
  swarm, 1Claw/Shroud, just commands, and security. Upstream source lives at
  https://github.com/1clawAI/scaffold-agent.
---

# scaffold-agent — AI / agent instructions

This file documents the **`scaffold-agent`** CLI published on npm ([scaffold-agent](https://www.npmjs.com/package/scaffold-agent)). The CLI **generates** new project directories; this repo (scaffoldagent.xyz) is the **documentation website**, not the CLI source tree.

**Upstream reference:** [https://github.com/1clawAI/scaffold-agent](https://github.com/1clawAI/scaffold-agent) — authoritative files there are `AGENTS.md`, `README.md`, and `.cursor/skills/scaffold-agent/`.

---

## What it does

- Interactive (or fully flagged) CLI that scaffolds a **monorepo**: Solidity (**Foundry** or **Hardhat** or none) + app (**Next.js**, **Vite**, or **Python** A2A).
- Optional **1Claw** vault/secrets, **Shroud** LLM proxy, **Ampersend** SDK, multiple **swarm** agent wallets.
- Generated apps follow patterns from [Scaffold-ETH 2](https://github.com/scaffold-eth/scaffold-eth-2) (wagmi, ABIs, `/debug` on Next, etc.) using [Scaffold UI](https://github.com/scaffold-eth/scaffold-ui) packages (`@scaffold-ui/hooks`, `@scaffold-ui/components`, `@scaffold-ui/debug-contracts`).

**Terminology:** **1claw** = [1claw.xyz](https://1claw.xyz) (vault, Shroud). **OpenClaw** ([openclaw.ai](https://openclaw.ai)) is a different product.

---

## Prerequisites

- **Node.js** ≥ 18 and **npm** (for `npx scaffold-agent` and the generated workspace).
- **[just](https://just.systems)** installed on the host (not an npm dependency). Generated repos use a root `justfile` for `just chain`, `just deploy`, `just start`, etc. Without `just`, run the equivalent `npm run` scripts from the generated `README.md`.

---

## Invoke the CLI

```bash
npx scaffold-agent@latest
npx scaffold-agent@latest my-agent    # creates ./my-agent, skips name prompt
scaffold-agent --help                 # full flag list; unknown flags error
scaffold-agent --version
```

---

## Typical flow (generated repo, local chain)

Order matters: the local node must be up before auto-fund / deploy.

1. Scaffold: `npx scaffold-agent@latest my-agent` → `cd my-agent`
2. **Second terminal:** `just chain` (Foundry/Hardhat local RPC, default `http://127.0.0.1:8545`)
3. `just fund` — fund deployer + agent (+ swarm addresses in `public/agents.json` when present)
4. `just deploy` — deploy contracts, refresh ABIs
5. `just start` — frontend / agent dev server (often [http://localhost:3000](http://localhost:3000))

Skip steps 2–4 if you chose **no chain**; configure RPC / `scaffold.config.ts` per generated README.

**Env skips:** `SCAFFOLD_SKIP_NPM_INSTALL=1` or `--skip-npm-install`; `SCAFFOLD_SKIP_AUTO_FUND=1` or `--skip-auto-fund` when scaffolding.

---

## Non-interactive / automation (`-y`)

Use `-y` / `--non-interactive` for CI or agents (no prompts).

- `--env-password` (≥ 6 characters) is **required** when `--secrets` is `oneclaw` or `encrypted`, unless `--secrets none`.
- `--defer-oneclaw-api-key` — skip `ONECLAW_API_KEY` at scaffold time.
- `--oneclaw-intents` — register 1Claw agent with Intents enabled.
- Defaults under `-y` match `scaffold-agent --help` (e.g. Foundry + Next.js + 1Claw Shroud + token billing).

**Shroud + `-y` validation:**

- `--llm oneclaw` with `--secrets none` (or non-oneclaw): supply `--oneclaw-agent-id` and `--oneclaw-agent-api-key`.
- `--shroud-billing provider_api_key`: supply `--shroud-provider-api-key` (vault vs `.env` depends on `--secrets`).

---

## CLI flags (common)

Strict parsing: unknown options **error**. Full list: `scaffold-agent --help`.

| Flag | Notes |
|------|--------|
| `-y` / `--non-interactive` | No prompts |
| `--project <name>` | Or single positional directory name |
| `--secrets` | `oneclaw` \| `encrypted` \| `none` |
| `--env-password` | Required for `oneclaw` / `encrypted` with `-y` (min 6 chars) |
| `--defer-oneclaw-api-key` | Skip user API key at scaffold |
| `--oneclaw-intents` | Register 1Claw agent with Intents enabled (with `-y`) |
| `--llm` | `oneclaw` \| `gemini` \| `openai` \| `anthropic` |
| `--shroud-upstream` | `openai` \| `anthropic` \| `google` \| `gemini` \| `mistral` \| `cohere` \| `openrouter` |
| `--shroud-billing` | `token_billing` \| `provider_api_key` |
| `--shroud-provider-api-key` | Required for `provider_api_key` in `-y` |
| `--oneclaw-agent-id` / `--oneclaw-agent-api-key` | For `oneclaw` LLM when secrets are not `oneclaw` |
| `--chain` | `foundry` \| `hardhat` \| `none` |
| `--framework` | `nextjs` \| `vite` \| `python` |
| `--agent` | `generate` \| `none` |
| `--ampersend` | `yes` \| `no` |
| `--skip-npm-install` | |
| `--skip-auto-fund` | |
| `--swarm <n>` | 1–64 agent wallets; extras in `SWARM_AGENT_KEYS_JSON` |
| `--from-config <file>` | Merge `agent.json`; **CLI overrides file** |
| `--dump-config` | Print merged config JSON to stdout (secrets omitted) |
| `--dump-config-out <file>` | Write that JSON to a file |

---

## `agent.json` (`--from-config` / `--dump-config`)

- Merge with `--from-config <file>`; any flag passed on the CLI **wins** over the file.
- Shape: `project` or `name`, `swarm`, `agents`: `{ "my-agent-id": "preset-label" }`, optional `extra` (written to generated `agent.config.extra.json`), optional `options`: `{ "secrets": "encrypted", … }`.
- Top-level keys may mirror CLI long-option names.

`--dump-config` prints merged JSON (no scaffold). `--dump-config-out` writes the same; **passwords and API keys are omitted** so the file is safe to share.

---

## Swarm (`--swarm`)

- `--swarm <n>` (1–64): multiple generated agent wallets; first remains `AGENT_ADDRESS` / `AGENT_PRIVATE_KEY`; extras in encrypted `SWARM_AGENT_KEYS_JSON`.
- Public roster: `packages/*/public/agents.json` (addresses only).
- Next/Vite: `lib/agent-swarm.tsx`, header picker, `/swarm` page; balances/identity follow selected agent.
- Post-scaffold: `just swarm agents=N` (see generated `justfile`).

---

## Unified network model

`scaffold.config.ts` → `targetNetwork` is the single source of truth for the active EVM network across UI, API routes, and AI agent tools.

- `getActiveNetwork()` resolves `targetNetwork` to a `NetworkDefinition` with `rpcOverrides` applied.
- Agent on-chain tools default `chainId` and `chain` parameters to `getActiveNetwork()`.
- `ONECLAW_CHAIN_NAMES` maps `chainId` → 1Claw slug (e.g. `8453 → "base"`).

---

## Agent on-chain tools (generated repos)

`lib/agent-onchain-tools.ts` — Vercel AI SDK `tool`s in the chat route:

- `list_deployed_contracts` — enumerate addresses from `deployedContracts.ts`.
- `contract_read` — call any view/pure function via RPC (defaults to active network).
- `oneclaw_intent_simulate` — simulate via 1Claw Intents + Tenderly.
- `oneclaw_intent_submit` — submit signed intent to 1Claw TEE.

---

## Generated layout (high level)

After scaffold, expect roughly:

- Root `justfile`, `package.json` (workspaces), `README.md`, `.env` (gitignored), optional `.env.secrets.encrypted`
- `scripts/` — `fund-deployer.mjs`, `swarm-agents.mjs`, `with-secrets.mjs`, `check-network.mjs`, deploy scripts, etc.
- `packages/foundry` or `packages/hardhat` (if chain chosen)
- `packages/nextjs` or `packages/vite` or `packages/python` — chat UI, `/api/chat`, identity/ENS/balances/swarm/debug routes

---

## `just` commands (generated repo)

| Command | Description |
|---------|-------------|
| `just chain` | Local blockchain |
| `just fund` | Fund deployer + agent (+ swarm from `public/agents.json`) |
| `just deploy` | Deploy + ABI generation |
| `just start` | Dev server / agent (runs `check-network` precheck) |
| `just check-network` | Validate `targetNetwork` chainId in `deployedContracts.ts` |
| `just use-network KEY` | Switch `targetNetwork` and run check (ethereum, base, sepolia, baseSepolia, polygon, bnb, localhost) |
| `just accounts` | QR for deployer + agent |
| `just balances` | Balances across configured chains |
| `just generate` | Deployer wallet (+ auto-fund if RPC up) |
| `just swarm agents=N` | Append swarm wallets |
| `just env KEY VALUE` | Upsert `.env` |
| `just enc KEY VALUE` | Update encrypted secrets (password prompt) |
| `just vault PATH VALUE` | 1Claw vault secret |
| `just list-1claw` | List vault and agent UUIDs |
| `just sync-1claw-env` | Write first vault + agent UUIDs to `.env` |
| `just reown PROJECT_ID` | WalletConnect project id → env |
| `just reset` | Re-bootstrap 1Claw vault + agent (**backup `.env` first**) |

---

## LLM providers and models

### Shroud upstreams

| `SHROUD_LLM_PROVIDER` | Default `SHROUD_DEFAULT_MODEL` |
|---|---|
| `openai` | `gpt-4o` |
| `anthropic` | `claude-sonnet-4-20250514` |
| `google` or `gemini` | `gemini-2.0-flash` |
| `mistral` | `mistral-large-latest` |
| `cohere` | `command-r-plus` |
| `openrouter` | `openai/gpt-4o` |

### Direct LLM defaults (not Shroud)

| Provider | Default model | Override |
|---|---|---|
| Gemini | `gemini-2.5-flash` | `GOOGLE_GENERATIVE_AI_MODEL` |
| OpenAI | `gpt-4o` | Edit the generated chat route |
| Anthropic | `claude-sonnet-4-20250514` | Edit the generated chat route |

---

## 1Claw / Shroud (essentials)

- `ONECLAW_AGENT_ID` is a **UUID**, not an Ethereum `0x…` address.
- Shroud docs: [Shroud guide](https://docs.1claw.xyz/docs/guides/shroud). Chat uses `X-Shroud-Agent-Key`, not `Authorization: Bearer` for Shroud.
- `SHROUD_BILLING_MODE`: `token_billing` (1Claw billing) vs `provider_api_key` (BYOK in vault or `SHROUD_PROVIDER_API_KEY`).

---

## Security

- Never commit real keys, agent API keys, or deployer private keys.
- Do not put Ethereum addresses in `ONECLAW_AGENT_ID`.
- Prefer `--dump-config` for shareable config; secrets are stripped.

---

## Links

- npm: [https://www.npmjs.com/package/scaffold-agent](https://www.npmjs.com/package/scaffold-agent)
- GitHub: [https://github.com/1clawAI/scaffold-agent](https://github.com/1clawAI/scaffold-agent)
- Shroud: [https://docs.1claw.xyz/docs/guides/shroud](https://docs.1claw.xyz/docs/guides/shroud)
- SKILL.md (for AI agents): [https://scaffoldagent.xyz/SKILL.md](https://scaffoldagent.xyz/SKILL.md)

---

*Synthesized from upstream (SKILL.md, reference.md, README.md, AGENTS.md). If behavior diverges, trust `scaffold-agent --help` and the upstream repo.*
