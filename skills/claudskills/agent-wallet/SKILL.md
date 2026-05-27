---
name: chaingpt-agent-wallet
description: "Give the AI agent its own EVM wallet with admin-controlled policies the agent CANNOT bypass even under prompt injection. Encrypted keystore (AES-256-GCM, scrypt KDF), policy file the agent has no tool to write, deterministic policy gate on every signing operation, optional local HTTP dashboard. Triggers: agent wallet, give the agent a wallet, agent address, fund the agent, agent autonomy, policy gate, kill switch, agent permissions, bounded autonomy, ERC-4337 alternative, session-key alternative."
---

# ChainGPT Agent Wallet Skill

The agent has its own EOA wallet on every EVM chain it supports. The admin (you, in your shell) sets policies that the agent cannot violate or revoke — even if a malicious prompt convinces the LLM to try.

## Threat model

**The attacker's goal:** prompt-inject the agent to drain its wallet to an attacker address.

**The plugin's defense:** the policy check is in **code, not in the LLM's prompt**. Every `chaingpt_agent_wallet_sign_and_send` call:

1. Loads the policy file fresh from disk (no caching — admin can update mid-session).
2. Runs `checkPolicy(intent)` — pure deterministic code that doesn't see the LLM's context.
3. Refuses if any rule fails, with a clear reason the agent surfaces back to the user.

The attacker can convince the LLM to call `sign_and_send(to=attacker, value=ALL)` — but the tool layer refuses because `attacker` isn't in `allowedToAddresses` or `value` exceeds `maxTxValueWei` or `killSwitch=true`. **The trust boundary is the tool code, not the LLM.**

There is no MCP tool that writes the policy file. The admin edits it directly with a text editor. There is no MCP tool that reads or sets the passphrase. The passphrase lives only in the shell env var.

## Setup (admin steps — done once)

```bash
# 1. Set a strong passphrase BEFORE starting the MCP server (>= 16 chars)
export CHAINGPT_AGENT_WALLET_PASSPHRASE="your-strong-passphrase-here-min-16-chars"

# 2. Start Claude Code / the MCP server in this shell
claude

# 3. Inside Claude, initialize the wallet (one-shot)
> Use chaingpt_agent_wallet_init to set up the agent's wallet
```

This creates two files:

| File | Contents | Who edits it |
|---|---|---|
| `~/.chaingpt-mcp/agent-wallet/keystore.json` | AES-256-GCM encrypted private key | Generated once by the init tool. Never edit by hand. Back it up. |
| `~/.chaingpt-mcp/agent-wallet/policy.json` | Plain JSON rules | **You, the admin, with a text editor.** The agent has NO tool that writes this file. |

Both default to `~/.chaingpt-mcp/agent-wallet/` but can be overridden via `CHAINGPT_KEYSTORE_FILE` and `CHAINGPT_AGENT_POLICY_FILE`.

## Tools

| Tool | Mutates state? | Notes |
|---|---|---|
| `chaingpt_agent_wallet_init` | Creates keystore | One-shot. Refuses if file exists. |
| `chaingpt_agent_wallet_address` | No | Returns the agent's EOA address. Use this to receive funds. |
| `chaingpt_agent_wallet_status` | No | Address + policy digest + kill-switch state. **Run this before any signing.** |
| `chaingpt_agent_wallet_balances` | No | Native-coin balances across requested chains. |
| `chaingpt_agent_wallet_policy` | No (read-only) | Shows the current policy JSON. Cannot modify it. |
| `chaingpt_agent_wallet_sign_and_send` | **Signs + broadcasts a tx** | The only tool that can move funds. Gated by policy. |
| `chaingpt_agent_wallet_serve_ui` | Starts a local HTTP server | Dashboard on `http://127.0.0.1:8787`. Read-only view. |

## Policy file format

Default `policy.json` (lazily created on first read) has `killSwitch: true` — the agent refuses everything until the admin opts in.

Example **production policy** (allow DEX rebalancing on Base, capped at 0.1 ETH/tx, audit memo required):

```json
{
  "version": 1,
  "killSwitch": false,
  "allowedChains": [8453],
  "allowedToAddresses": [
    "0x6352a56caadc4f1e25cd6c75970fa768a3304e64",
    "0x111111125421ca6dc452d289314280a0f8842a65"
  ],
  "blockedToAddresses": [
    "0x0000000000000000000000000000000000000000"
  ],
  "maxTxValueWei": "100000000000000000",
  "maxTxGas": "500000",
  "blockedSelectors": [],
  "requireMemo": true,
  "notes": "Base only, OpenOcean + 1inch routers only, 0.1 ETH cap, memo required for audit",
  "updatedAt": "2026-05-18T20:00:00Z"
}
```

### Field reference

| Field | Type | Behavior when unset | Behavior when set |
|---|---|---|---|
| `killSwitch` | bool | refuses everything (fail-closed) | `true` refuses everything; `false` proceeds to other checks |
| `allowedChains` | int[] | any chain allowed | refuses if `chainId` not in list |
| `allowedToAddresses` | string[] | any address allowed | refuses if `to` not in list (case-insensitive) |
| `blockedToAddresses` | string[] | nothing blocked | refuses if `to` matches (case-insensitive) |
| `maxTxValueWei` | string | no cap | refuses if native `value > max` |
| `maxTxGas` | string | no cap | refuses if `gasLimit > max` |
| `blockedSelectors` | string[] | nothing blocked | refuses if first 4 bytes of `data` match (e.g. `0xa9059cbb` blocks ERC-20 `transfer`) |
| `requireMemo` | bool | no memo required | refuses if the `memo` arg is missing |

**Precedence:** kill switch > blockedToAddresses > allowedToAddresses > value caps > gas cap > blockedSelectors > memo. Any single failure refuses the tx.

## Pre-flight checklist

```text
1. chaingpt_agent_wallet_status   # see address + policy digest + kill switch state
2. chaingpt_agent_wallet_balances # confirm funded on the target chain
3. chaingpt_agent_wallet_policy   # read the active rules in full
4. chaingpt_agent_wallet_sign_and_send chain=… to=… valueWei=… data=… memo="…"
```

If the call gets refused with a policy reason: **do not try to work around it from the agent side**. Surface the reason to the admin and let them edit the policy file (or override) themselves.

## Local admin dashboard

```text
> Use chaingpt_agent_wallet_serve_ui
```

Returns a `http://127.0.0.1:8787` URL **and a one-time admin token** printed in the tool output (also saved to `~/.chaingpt-mcp/agent-wallet/.admin-token`, 0600). The token rotates on every restart.

Open the URL in your browser. Paste the admin token at the login screen. The dashboard then shows:

- **Deposit address** with QR code
- **Multi-chain native-coin balances** (refresh page to update)
- **One-click kill switch** — engage or disable, single button
- **Policy JSON editor** — full inline editor, validated server-side, atomic write with `.bak` backup
- **Keystore + policy file paths** for reference

### Why this is safe even though the dashboard CAN edit the policy

Recall the threat model: the attacker controls the LLM via prompt injection. The defenses, in layers:

1. **No MCP tool exposes a write to the policy file.** The LLM literally cannot reach the `savePolicy` function — it's only imported by the localhost HTTP server.
2. **The localhost HTTP server has no client inside the agent.** The plugin has no MCP tool that does arbitrary HTTP POSTs to localhost. The LLM cannot trigger the dashboard's POST endpoints even by trying.
3. **Admin auth required.** Even if a future tool somehow gained HTTP access, every POST endpoint requires a valid session cookie that's only set after the admin pastes the token. The token rotates every restart and lives only in admin-controlled state (env / file with 0600 perms).
4. **Origin + Referer check.** Cross-origin POSTs (CSRF) are rejected. Browsers always set `Origin` on form submits.
5. **Strict schema validation.** Even with a valid session, the policy editor rejects unknown fields, bad chain IDs, malformed addresses, non-integer wei values, etc. Garbage cannot make it onto disk.
6. **Atomic write + `.bak`.** A botched save can't corrupt the policy file mid-write, and the previous version is recoverable.
7. **Bound to `127.0.0.1` only.** Never on `0.0.0.0` — the dashboard is not reachable from other machines on the network.

The single failure mode that would bypass all of this: malware running on the admin's machine that can read the admin token file AND make HTTP requests to localhost. At that point the attacker has shell access and can read the keystore directly; the policy file is no longer the weakest link.

### Dashboard endpoints

| Method | Path | Behavior |
|---|---|---|
| `GET /` | login form (if unauthed) or redirect to /dashboard | — |
| `POST /login` | check admin token, set session cookie, redirect to /dashboard | requires Origin |
| `GET /dashboard` | full admin UI (auth required) | — |
| `GET /api/policy` | current policy JSON | requires session |
| `POST /api/policy` | save new policy after validation | requires session + Origin |
| `POST /api/killswitch` | toggle the kill switch (set=on/off) | requires session + Origin |
| `GET /api/status` | JSON with address + balances + policy digest | requires session |
| `GET /logout` | clear session cookie, redirect to login | — |

## What this skill does NOT do

- **Solana / non-EVM signing.** The agent wallet is EVM-only. Solana program-instruction signing is a separate path not yet wired.
- **Multi-sig.** This is a single EOA. For larger sums use a Safe / Gnosis multi-sig and have the agent's EOA be one signer; the policy still applies to the agent's signing.
- **Session keys / ERC-4337.** Bounded smart-account autonomy is a different model (smart account holds funds, agent gets a revocable session key). This skill is the simpler EOA + policy-file approach; ERC-4337 is a future feature.
- **Recover lost passphrases.** Lose `CHAINGPT_AGENT_WALLET_PASSPHRASE` → the keystore is unrecoverable. There is no recovery path. Back up the passphrase out-of-band (1Password, hardware safe, etc.).
- **Read or change the policy from the agent's tools.** Deliberately. Edit the file with your text editor.

## Funding the agent

1. Get the address: `chaingpt_agent_wallet_address`
2. Send funds from any wallet (CEX withdrawal, MetaMask, hardware wallet, etc.) to that address on any chain the policy allows.
3. Confirm: `chaingpt_agent_wallet_balances chains=[base,arbitrum]`

The agent is now ready to operate within its policy bounds.

## Credit accounting

All agent-wallet tools cost **0 ChainGPT credits**. The wallet is custody-on-the-user's-machine (not custody-via-ChainGPT). The credit funnel comes from upstream tools the user/agent calls (`chaingpt_research_token`, `chaingpt_risk_token`, `chaingpt_intel_token`) before deciding to deploy.

## Reference

- Keystore format: AES-256-GCM with scrypt (N=2^14) KDF. File version 1.
- Default paths: `~/.chaingpt-mcp/agent-wallet/{keystore.json,policy.json}` (override via env).
- File perms: 0600 for keystore, 0700 for parent dir (POSIX).
