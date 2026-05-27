---
name: solana-deploy
description: Use this skill when the user wants to deploy or upgrade a Solana program from devnet to mainnet — verifiable builds, buffer accounts, priority fees, upgrade authority management, IDL upload, program close.
---

# solana-deploy

## Overview

Mainnet deploys are the part of Solana development where things actually break. Program binaries are tens to hundreds of KB, the BPF loader chunks them into ~1 KB transactions, each chunk needs its own signature and a non-expired blockhash, and during congestion validators silently drop unprioritized traffic. A naive `solana program deploy program.so` against mainnet typically dies somewhere in the middle and leaves SOL stuck in a half-written buffer account that the user doesn't know about.

This skill is the safe pipeline: build deterministically with `solana-verify`, write to a named buffer with bounded retries, deploy *from* the buffer (a single small transaction), pay competitive priority fees, transfer authority to a multisig, and submit the verifiable build for public attestation. Every step is recoverable; every failure mode has a known fix.

## When to use this skill

Trigger this skill when the user says any of:

- "Deploy my Solana program to mainnet" / "ship to mainnet"
- "Upgrade the program at `<pubkey>`"
- "My `solana program deploy` keeps failing / hangs / runs out of SOL"
- "I'm seeing `Error: Data writes to account failed` / `Blockhash not found` / `transaction expired`"
- "Make my program verifiable" / "get the verified-build checkmark"
- "Move upgrade authority to a Squads multisig" / "make it immutable"
- "Close my program / buffer and recover SOL"
- "I have an orphaned buffer at `<pubkey>` — how do I recover it?"

Do **not** use this skill for: writing program code (separate Anchor/program-design concern), localnet/devnet smoke tests where failure costs nothing, or SPL token deploys (those aren't BPF programs).

## Prerequisites

Verified versions used throughout this skill. Pin these; do not float to latest.

```bash
# 1. Agave CLI (the maintained Solana validator + CLI fork from Anza).
#    Pin to a known-good 2.x or 3.x release. As of this skill: agave 3.0.10.
#    Confirm the current stable tag at https://github.com/anza-xyz/agave/releases
sh -c "$(curl -sSfL https://release.anza.xyz/v3.0.10/install)"
agave-install update
solana --version    # → solana-cli 3.0.10 (2.1.x is also fine if you've pinned older)

# 2. Anchor (only if the program uses Anchor; 0.30+ or 1.0+ required for IDL v2 + correct buffer handling)
avm install 0.31.0 && avm use 0.31.0
anchor --version

# 3. solana-verify (deterministic builds + OtterSec remote submission)
cargo install solana-verify --locked --version 0.4.15
solana-verify --version

# 4. Docker — REQUIRED by `solana-verify build`. Must be running.
docker --version && docker info >/dev/null

# 5. Mainnet RPC that does not rate-limit deploys. Public api.mainnet-beta.solana.com
#    will fail under any real load. Use Helius, Triton, QuickNode, or your own node.
solana config set --url https://mainnet.helius-rpc.com/?api-key=<KEY>

# 6. SOL in the deploy keypair (see Step 12 for sizing). Rule of thumb:
#    6-8 SOL liquid for a typical 250 KB program. Buffer rent is refunded on success.
solana balance
```

Before any destructive command, **confirm cluster + signer**:

```bash
solana config get   # check RPC URL and keypair path
solana address      # confirm signer
```

If `solana config get` shows `localhost` or `devnet` while the user said "mainnet," stop and ask.

## Workflow

### Step 1 — Verifiable build with `solana-verify`

Build inside Docker so the resulting `.so` is bit-for-bit reproducible. Never run `anchor build` or `cargo build-sbf` after this — the host toolchain will produce a different hash and break verification.

```bash
# Single-program workspace:
solana-verify build

# Multi-program workspace — name the lib explicitly:
solana-verify build --library-name my_program

# Output lands in target/deploy/<lib>.so. Print the hash:
solana-verify get-executable-hash target/deploy/my_program.so
```

Save that hash — you'll compare it after deploy. The helper `scripts/verify-build.sh` wraps this with Docker + Cargo.lock pre-flight checks.

### Step 2 — Pre-flight: size, rent, balance, cluster

```bash
SO=target/deploy/my_program.so
SIZE=$(wc -c < "$SO")
# Programs are stored at 2x size to leave room for upgrades.
echo "Program size: $SIZE bytes"
solana rent $((SIZE * 2))         # prints rent-exempt minimum in lamports + SOL
solana balance
solana config get | grep 'RPC URL'
```

If balance is below `rent + 0.5 SOL`, top up. SOL spent on a failed deploy is recoverable, but only if you can identify the buffer pubkey — which is why Step 3 matters.

### Step 3 — Generate a named buffer keypair (deterministic, recoverable)

A named buffer keypair is the single most important habit in this skill. If `write-buffer` dies halfway, you can resume; if you abandon it, you can close it to recover SOL. With an ephemeral buffer, both are impossible.

```bash
solana-keygen new --no-bip39-passphrase --silent -o buffer.json --force
BUFFER=$(solana address -k buffer.json)
echo "Buffer pubkey: $BUFFER"   # write this down NOW, before anything else
```

### Step 4 — `write-buffer` with retries (the long step)

This is where ~95% of deploy failures happen. The helper `scripts/deploy-with-retries.sh` runs this loop; the bare command:

```bash
solana program write-buffer "$SO" \
  --buffer buffer.json \
  --buffer-authority ~/.config/solana/deploy.json \
  --with-compute-unit-price 100000 \
  --max-sign-attempts 1000 \
  --use-rpc
```

Flag notes:
- `--with-compute-unit-price 100000` — 100k micro-lamports per CU. Adjust for live congestion (Step 7).
- `--max-sign-attempts 1000` — how many times the CLI re-signs with a fresh blockhash when chunks don't land. The default (5) is far too low for mainnet.
- `--use-rpc` — send through your configured RPC instead of validator TPU. Required on most paid RPCs.
- Re-running the same command with the same `buffer.json` **resumes** from the last successfully written chunk. Do not generate a new buffer just because the first try failed.

### Step 5 — Set buffer authority to the deploy signer

Default behavior usually sets buffer authority to the current keypair, but be explicit when a hardware wallet or multisig will sign the final deploy. The buffer authority must equal the signer of `deploy --buffer` in Step 6.

```bash
solana program set-buffer-authority "$BUFFER" \
  --new-buffer-authority $(solana address)
```

### Step 6 — Deploy from buffer

This is a single, small transaction. It almost always lands first try.

**Initial deploy** (new program ID — `--program-id` is a keypair file):

```bash
solana program deploy \
  --buffer "$BUFFER" \
  --program-id ./target/deploy/my_program-keypair.json \
  --upgrade-authority ~/.config/solana/deploy.json \
  --with-compute-unit-price 100000 \
  --max-sign-attempts 50 \
  --use-rpc
```

**Upgrade** (existing program — `--program-id` is the pubkey, no keypair):

```bash
solana program deploy \
  --buffer "$BUFFER" \
  --program-id <EXISTING_PROGRAM_PUBKEY> \
  --upgrade-authority ~/.config/solana/deploy.json \
  --with-compute-unit-price 100000 \
  --use-rpc
```

On success, the buffer is consumed and its rent rolls into the program data account — no buffer cleanup needed.

### Step 7 — Priority fees, calibrated

50k–500k micro-lamports/CU is the practical range. Default `--with-compute-unit-price 0` gets you silently dropped during any mainnet stress event. Always query a live estimate before sending:

```bash
curl https://mainnet.helius-rpc.com/?api-key=$HELIUS_KEY \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"getPriorityFeeEstimate",
       "params":[{"accountKeys":["BPFLoaderUpgradeab1e11111111111111111111111"],
                  "options":{"priorityLevel":"High"}}]}' \
  | jq -r '.result.priorityFeeEstimate'
```

Use 1.5x the "High" recommendation for the deploy. If congestion is extreme (>1M micro-lamports/CU), wait an hour rather than pay — deploys are not time-sensitive.

### Step 8 — Retry patterns on failure

| Symptom | Cause | Fix |
|---|---|---|
| `Error: Data writes to account failed` after N chunks | Blockhash expired mid-batch | Re-run the same `write-buffer` command — it resumes from the last written offset because `buffer.json` is reused. |
| Hangs at "Sending transactions..." with no progress | RPC dropping txs / congestion | Bump `--with-compute-unit-price` 2–5x, keep `--use-rpc`, switch to a paid RPC if you're on the public endpoint. |
| `Account already in use` on `deploy` | Program ID keypair was used previously | Pick a fresh program-id keypair, or use the existing program ID via the upgrade flow. |
| `insufficient funds for rent` | Underestimated rent | Top up; `solana program show <id>` reveals the gap. |
| `signer authority does not match` on `deploy --buffer` | Buffer authority ≠ deploy signer | Re-run Step 5 with the correct authority. |
| Stale blockhash from `--use-rpc` | RPC node behind tip | Switch RPC endpoints (Helius/Triton/QuickNode rotate well). |

### Step 9 — Upload IDL (Anchor only)

The IDL is published to a PDA so frontends and explorers can decode instructions. With Anchor 0.30+:

```bash
# Initial publish:
anchor idl init <PROGRAM_ID> \
  --filepath target/idl/my_program.json \
  --provider.cluster mainnet

# Subsequent updates:
anchor idl upgrade <PROGRAM_ID> \
  --filepath target/idl/my_program.json \
  --provider.cluster mainnet
```

If the IDL is >10 KB (common for Anchor 0.30+ which inlines doc comments), use the buffer flow:

```bash
anchor idl write-buffer <PROGRAM_ID> --filepath target/idl/my_program.json
anchor idl set-buffer <PROGRAM_ID> --buffer <IDL_BUFFER_PUBKEY>
```

Anchor 0.30+ auto-closes the IDL buffer after a successful `set-buffer` and refunds its rent.

### Step 10 — Transfer upgrade authority to Squads (or multisig of choice)

Single-key upgrade authority on a mainnet program is the most common high-severity audit finding. Move it as soon as the deploy is verified working.

```bash
# SQUADS_VAULT_PDA = the vault PDA of your Squads multisig
solana program set-upgrade-authority <PROGRAM_ID> \
  --new-upgrade-authority <SQUADS_VAULT_PDA> \
  --skip-new-upgrade-authority-signer-check
```

`--skip-new-upgrade-authority-signer-check` is required because the multisig PDA has no private key and cannot sign acceptance. Squads accepts ownership on-chain via the loader. Confirm with `solana program show <PROGRAM_ID>` before celebrating. See `references/authority-management.md` for the multisig vs. immutable decision tree.

### Step 11 — Submit verifiable build to OtterSec

This is what gives users the verified-build checkmark in Solscan / SolanaFM / Solana Explorer.

```bash
# Local verification — confirms on-chain bytes match your repo at the given commit.
solana-verify verify-from-repo \
  -u mainnet-beta \
  --program-id <PROGRAM_ID> \
  https://github.com/<owner>/<repo> \
  --commit-hash $(git rev-parse HEAD) \
  --library-name my_program \
  --mount-path .

# Remote submission — queues a fresh build by OtterSec workers and posts the result on-chain.
solana-verify remote submit-job \
  --program-id <PROGRAM_ID> \
  --uploader $(solana address)
```

The remote worker rebuilds in the same Docker image; status shows up in explorers within ~10 minutes. Also submit a PR to the [Solana Verified Builds registry](https://github.com/solana-foundation/verified-builds) for higher-visibility listing.

### Step 12 — Close program / buffer to recover SOL

```bash
# Recover SOL from a stuck/abandoned buffer:
solana program close <BUFFER_PUBKEY> --bypass-warning

# Close every buffer owned by the current keypair (be careful — also matches old ones):
solana program show --buffers --buffer-authority $(solana address)
solana program close --buffers --bypass-warning

# Close a deployed program permanently (cannot be undone, program ID burned forever):
solana program close <PROGRAM_ID> --bypass-warning
```

**SOL estimation rule of thumb:** for any program of size `S` bytes,

```
deploy_cost_SOL  ≈ (S * 2 * 0.00000696) + 0.5     # initial deploy
upgrade_cost_SOL ≈ 0.5                            # buffer rent only, refunded on success
```

A 200 KB program: ~3 SOL initial, ~0.5 SOL per upgrade. A 300 KB program: ~4.5 SOL initial. Buffer rent is refunded when the deploy consumes the buffer, so steady-state cost across many upgrades is small. Closing a program returns the rent portion to the close authority — useful for deprecation cleanup.

## Common pitfalls

1. **Orphaned buffer account.** The most expensive bug. You ran `solana program write-buffer` without `--buffer buffer.json`, the deploy died, and now there's a multi-SOL account no one tracks. Always use a named buffer keypair (Step 3). Find existing ones: `solana program show --buffers --buffer-authority $(solana address)`. Recover: `solana program close <PUBKEY> --bypass-warning`.

2. **Priority fee too low during congestion.** Default `--with-compute-unit-price 0` gets you silently dropped during any stress event (memecoin launches, NFT mints, IPO days). Always set at least 10,000 micro-lamports; query Helius `getPriorityFeeEstimate` for live numbers and use 1.5x the "High" recommendation.

3. **Lost upgrade authority.** Three flavors, all unrecoverable: (a) keypair file deleted with no backup, (b) `--final` set on mainnet "to test the command," (c) authority transferred to a typo'd pubkey. The BPF Upgradeable Loader has no recovery oracle — the program is frozen at its current bytecode forever. See `references/authority-management.md`.

4. **IDL larger than transaction limit.** Anchor 0.30+ inlines doc comments, easily pushing IDLs past the 1232-byte tx limit. `anchor idl init` will silently fail or partially write. Use `anchor idl write-buffer` + `anchor idl set-buffer`, mirroring the program buffer flow.

5. **Non-reproducible build.** Running `anchor build` or `cargo build-sbf` between `solana-verify build` and verification submission. The host toolchain's rustc / solana-sdk versions almost certainly don't match the Docker image, so OtterSec verification fails with a hash mismatch. Only ever build through `solana-verify build`.

6. **`Cargo.lock` drift.** `solana-verify` requires `Cargo.lock` in the repo root and uses it to pin every dependency. If `Cargo.lock` is gitignored (Rust *library* default), the remote build resolves different deps and hashes differ. **Commit `Cargo.lock` for any program crate.**

7. **Wrong cluster.** `solana config set --url devnet` is sticky across shells. Confirm with `solana config get` immediately before `solana program deploy`. Deploying mainnet code to devnet wastes a keypair slot; deploying devnet code to mainnet wastes real money. A shell prompt that shows the current cluster is worth setting up.

8. **Buffer authority ≠ deploy signer.** When the upgrade authority is a hardware wallet or multisig, the buffer must also be owned by that key — otherwise `deploy --buffer` fails with `signer authority does not match`. Set this explicitly with `solana program set-buffer-authority` (Step 5) before the final deploy.

9. **Free public RPC for the actual deploy.** `api.mainnet-beta.solana.com` rate-limits aggressively; you'll see far more blockhash failures than necessary. Any free tier from Helius / QuickNode / Triton handles deploys reliably.

## References

- `scripts/verify-build.sh` — wraps `solana-verify build` with Docker + Cargo.lock pre-flight checks, prints hash for later comparison.
- `scripts/deploy-with-retries.sh` — `write-buffer` with bounded retries + auto-resume on partial writes, then `deploy --buffer`, with orphan recovery instructions on failure.
- `references/authority-management.md` — single-key vs. multisig vs. immutable decision guide; lost-authority recovery checklist.
- [Solana docs — Deploying Programs](https://solana.com/docs/programs/deploying)
- [Solana docs — Verified Builds](https://solana.com/docs/programs/verified-builds)
- [Agave CLI — Deploy a Program](https://docs.anza.xyz/cli/examples/deploy-a-program)
- [Ellipsis-Labs/solana-verifiable-build](https://github.com/Ellipsis-Labs/solana-verifiable-build) / [solana-foundation fork](https://github.com/solana-foundation/solana-verifiable-build)
- [Helius — How to Land Transactions on Solana](https://www.helius.dev/blog/how-to-land-transactions-on-solana)
- [Helius — Priority Fee API](https://www.helius.dev/docs/priority-fee-api)
- [Squads — Managing Program Upgrades with a Multisig](https://squads.so/blog/solana-multisig-program-upgrades-management)
