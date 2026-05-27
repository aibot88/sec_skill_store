---
name: solana-agent-wallet
description: Manages Solana agent wallets with encrypted keys and per-agent spend limits. Use when the user needs to create agents, check balances, transfer SOL, request airdrops, list token holdings (Helius), or buy SPL tokens via Jupiter. Teaches tool contracts and security rules for an agentic wallet backend.
metadata: {"openclaw":{"requires":{"env":["MASTER_KEY"]},"primaryEnv":"MASTER_KEY"}}
---

# Solana Agent Wallet

Agent-scoped Solana wallets: one logical agent = one keypair (stored encrypted) and a configurable max spend (SOL). The AI agent is the only interface; it calls tools that read balance, transfer, airdrop, or swap.

## Tool contracts (implement these as OpenClaw tools or HTTP endpoints)

All tools that move funds or create agents must enforce **max_spend** (SOL) and **confirmation** in the agent flow.

| Tool | Purpose | Parameters | Security |
|------|---------|------------|----------|
| `create_agent` | Create agent + wallet in one step | `maxSpend` (number, SOL) | Persist encrypted keys; set agent.max_spend |
| `create_wallet` | Attach a new wallet to existing agent | — | Overwrites previous wallet for that agent |
| `get_balance` | SOL balance for current agent | — | Read-only |
| `get_wallet_address` | Public key for current agent | — | Read-only |
| `transfer_sol` | Send SOL to address | `recipientAddress`, `amount` (SOL) | Enforce amount ≤ max_spend; simulate before send |
| `request_airdrop` | Devnet airdrop | `amount` (optional, SOL, default 0.5, max 2) | Rate-limited by RPC |
| `get_assets_by_owner` | Fungible tokens for an address (Helius) | `ownerAddress`, `page`, `limit` | Read-only; needs HELIUS_API_KEY |
| `analyze_token` | Read-only token analysis (Helius + DexScreener + Jupiter quote) | `mintAddress`, `quoteAmountSol` (optional) | Read-only; surfaces signals and risks, not advice |
| `scout_buy_candidates` | Scout Solana buy candidates on-chain via DexScreener | `searchQuery`, `minLiquidityUsd`, `minVolume24h`, `maxResults`, `deepAnalyzeTopN` (all optional) | Read-only; bounded list of candidates, not recommendations |
| `buy_token` | Buy SPL token with SOL via Jupiter | `mintAddress`, `amountSol` (optional) | Enforce amountSol ≤ max_spend; prefer analyze_token first |

## Security rules for implementation

- **Encryption**: Store per-agent `encrypted_private_key` (AEK-encrypted) and `encrypted_agent_key` (MASTER_KEY-encrypted AEK). Decrypt only in memory when signing; never log or expose raw keys.
- **Spend cap**: Before any `transfer_sol` or `buy_token`, check `amount <= agent.max_spend` (in SOL). Reject and return a clear message if over.
- **Simulation**: For Solana transfers, run `simulateTransaction` before `sendRawTransaction`; abort send if simulation fails.
- **Context**: All state-changing tools require a current **agentId** (from session or user selection). Read-only tools may accept an optional address.

## How the agent should behave

- Confirm transaction details (recipient, amount) with the user before calling `transfer_sol` or `buy_token`. On explicit confirmation (“yes”, “go ahead”, “confirm”), call the tool immediately.
- Always respect `max_spend`; if the user asks to send more than the limit, explain the limit and refuse.
- For token buys: use `get_assets_by_owner` to list tokens for an address, then call `buy_token` per mint with a sensible `amountSol` (e.g. 0.1) within `max_spend`.
- Before buying an unfamiliar mint, call `analyze_token` first and present observable signals (authorities, liquidity, route) with a no-financial-advice disclaimer.
- When the user asks to scout buys (“find tokens”, “scout profitable buys”, “what is hot on-chain”), call `scout_buy_candidates` and present the list as candidates to review, not guaranteed profit. Mainnet only is meaningful; on devnet the list is usually empty.

## Environment / config

- `MASTER_KEY`: 32-byte hex; required to decrypt agent keys for signing.
- `SOLANA_RPC`: Optional; devnet/mainnet URL.
- `HELIUS_API_KEY`: For `get_assets_by_owner`.
- `JUPITER_API_KEY`: For `buy_token`.

Use these as gating in OpenClaw (`metadata.openclaw.requires.env`) so the skill is only loaded when the wallet backend is configured.
