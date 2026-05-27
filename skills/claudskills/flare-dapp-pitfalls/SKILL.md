---
name: flare-dapp-pitfalls
description: >
  Hard-won, cross-project lessons from building, deploying, and operating Flare-family
  (Flare / Songbird / Coston2) dApps. Use this skill whenever the user is: deploying
  or interacting with a Flare/Songbird/Coston2 contract, building a frontend with
  RainbowKit + Wagmi for Flare chains, writing Foundry fork tests against Flare-family
  state, claiming or rotating FTSO reward redistributors, debugging a stuck or
  silently-failing transaction, choosing RPC endpoints for browser vs server use,
  or troubleshooting MetaMask / wallet connection on Flare. Trigger on any mention of:
  Flare RPC, Songbird canary, Coston2 testnet, FTSO reward claim, WNAT vote-power,
  FlareDrops, FtsoRewardRedistributor, FlaresRewardsRedistributorForNft, Enosys
  redistributor, RainbowKit MetaMask hang, Ankr origin locked, Multicall3 on Flare,
  EIP-150 63/64 gas, eth_getLogs 30-block cap, "why is my Flare contract test failing
  in CI", "why did my claim transaction return zero", "Wrap SGB to WSGB", or any
  question about gotchas specific to Flare-family chains.
---

# Flare dApp Pitfalls — Cross-Project Lessons

This skill captures **gotchas that are NOT in `enosys-contracts`, `enosys-integrations`,
`enosys-dex-v3`, or `solidity`** but cost real time on Flare-family work. Most are
counterintuitive, RPC-/wallet-/gas-shaped, or specific to Flare's FTSO reward
infrastructure.

If something contradicts the existing Enosys skills, the override is documented inline
with the reason — Enosys skills describe what their own private frontends use; this
skill describes what works for **third-party builders** with no privileged RPC access.

---

## 1. Wallet & RainbowKit setup

### Do NOT use RainbowKit's `metaMaskWallet` SDK connector on desktop

This is a **direct correction** to the `enosys-integrations` skill, which lists
`metaMaskWallet` from `@rainbow-me/rainbowkit/wallets` in its recommended set.

`metaMaskWallet` uses the MetaMask SDK, which races a mobile deep-link flow against
extension detection on desktop. It frequently hangs on "Opening MetaMask…" — a
~15-30s blocking dead state where the user can't tell if anything's happening.

**Use `injectedWallet` instead** — RainbowKit renders it as **"Browser Wallet"** in the
picker. It works seamlessly with the MetaMask extension, Rabby, and Brave Wallet
(any EIP-1193 injected provider). For mobile MetaMask users, `walletConnectWallet`
covers them via QR pairing — no SDK connector needed.

```typescript
import {
  injectedWallet,        // ← use this, not metaMaskWallet
  rainbowWallet,
  coinbaseWallet,
  walletConnectWallet,
} from "@rainbow-me/rainbowkit/wallets";

const connectors = connectorsForWallets(
  [
    {
      groupName: "Recommended",
      wallets: [injectedWallet, rainbowWallet, coinbaseWallet, walletConnectWallet],
    },
  ],
  { appName: "Your dApp", projectId: WALLETCONNECT_PROJECT_ID }
);
```

Enosys's own frontends can use `metaMaskWallet` because they're served from a curated
domain set with their own RPC infrastructure; outside that, the MetaMask SDK is
the reason "MetaMask doesn't open" support tickets pile up.

### Wagmi button "dead zone" — track BOTH `isPending` AND `isLoading`

`useWriteContract().isPending` = waiting for wallet to sign (0.5–2s).
`useWaitForTransactionReceipt().isLoading` = tx is in mempool / mining.

Most tutorials only check `isLoading`, which means there's a 0.5–2s dead zone where
the user has clicked the button but MetaMask hasn't opened yet, and the button still
says "Place order". Three-state pattern:

```tsx
const { writeContract, isPending, data: txHash } = useWriteContract();
const { isLoading: isMining, isSuccess } = useWaitForTransactionReceipt({ hash: txHash });

const label = isPending ? "Confirm in wallet…"
            : isMining  ? "Placing order…"
            :             "Place order";
```

Apply this to every write-action button.

---

## 2. RPC endpoints — browser vs server

### Public Flare RPCs cap `eth_getLogs` at 30 blocks

| Chain | Public RPC | `eth_getLogs` cap |
|---|---|---|
| Flare | `https://flare-api.flare.network/ext/C/rpc` | **30 blocks** |
| Songbird | `https://songbird-api.flare.network/ext/C/rpc` | **30 blocks** |
| Coston2 | `https://coston2-api.flare.network/ext/C/rpc` | **30 blocks** |

If your frontend depends on historical log scans (e.g. "find all my orders"), the
public RPC will throw `block range too wide`. Either:

- Use **Multicall3 + per-id pairwise reads** instead of log scans (e.g.
  `factory.getPool(t0, t1, fee)` over a curated token list).
- Use **Ankr** (paid tier) — lifts to ~5,000 blocks per request.
- Run a **self-hosted node**.

Plan for the public-RPC `eth_getLogs` cap from day one — assume 30 blocks is your
default and design history-dependent features around that.

### Ankr's API key is origin-locked for browser safety

The Ankr key in `NEXT_PUBLIC_ANKR_KEY` is **domain-locked** to the production hostname
(plus `localhost:3000` for dev). This is correct browser hygiene — anyone can read
the key from your build output, so origin lock prevents abuse.

Side effect: server-side calls (curl, `forge script`, indexers, executor bots) will
hit `Origin not allowed (-32079)`. **Generate a separate IP-locked Ankr key** for
server use; don't try to share the browser key.

### Multicall3 canonical address — same on all three Flare chains

```
0xcA11bde05977b3631167028862bE2a173976CA11
```

Live on Flare (14), Songbird (19), and Coston2 (114). Any dApp doing batched reads
should use it instead of N parallel `eth_call`s.

`aggregate3(allowFailure=true)` is the workhorse — lets one call fail without
killing the batch. **Use it for permissionless writes too**, but only when the target
function doesn't gate on `msg.sender`. Functions that credit `msg.sender` (executor
shares, etc.) cannot be multicalled because Multicall3 becomes the apparent caller.

### EIP-3855 (PUSH0) warning on Coston2 is cosmetic

Forge will print:
```
Warning: EIP-3855 is not supported in one or more of the RPCs used.
Unsupported Chain IDs: 114.
```

Deployments still succeed. **Don't downgrade `solc` to 0.8.19** to silence it —
0.8.20+ targets PUSH0 and Coston2 handles it fine in practice; the RPC just
doesn't advertise the EIP.

---

## 3. Gas: EIP-150 63/64 rule + `try/catch`

The single biggest source of "looks-successful but did nothing" bugs on Flare.

**The rule**: when contract A calls contract B, EVM forwards `min(gasleft, callerLimit)`
where `callerLimit = floor(63/64 × gasleft)`. The remaining 1/64 stays with A.

**Why it bites with `try/catch`**: many Flare contracts wrap external calls in
`try/catch` with a **reserved inner gas budget** (e.g. `B.foo{gas: 10_000_000}()`).
The `gas:` clause is a *ceiling*; the actual forwarded amount is
`min(10_000_000, 63/64 × gasleft)`. If the OUTER tx didn't have enough gas to forward
10M, the inner call gets less, OOGs silently, the `try/catch` swallows the revert,
and the outer tx succeeds with no observable effect.

**MetaMask and `eth_estimateGas` cannot trace through `try/catch`** — the estimator
sees the outer revert path of "did anything", not the inner OOG, so wallets routinely
under-estimate. Your transactions confirm but pay zero out.

**Fix**: pin outer gas explicitly when wrapping a call with a reserved inner budget.
Rule of thumb: `outer ≥ ceil(inner × 64/63) + outer_overhead_estimate`. For a 10M
inner cap, pin **at least 12M** outer — use 14M to be safe.

```typescript
// Wagmi pattern: pin gas on the write to escape estimateGas under-budgeting
writeContract({
  address: lom,
  abi,
  functionName: "claimDelegationRewards",
  args: [orderId],
  gas: 12_000_000n,   // ← outer pin; protects the 10M REWARD_CLAIM_GAS_CAP forward
});
```

Anywhere you see a contract pattern like:

```solidity
try IExternal(target).foo{gas: INNER_CAP}() returns (...) { ... }
catch { /* swallow */ }
```

assume estimateGas will under-budget the outer call. Always pin gas on the frontend.

### WNAT's transfer hooks are invisible to `eth_estimateGas`

A related variant that doesn't need any `try/catch` to bite you. WNAT (`WFLR`,
`WSGB`, `WC2FLR`) fires per-transfer vote-power hooks: every `transfer` and
`transferFrom` calls `updateAtTokenTransfer` on each registered delegate /
governance contract to refresh checkpoints. Those hooks consume real gas — often
75k-200k per hook — and their cost depends on the recipient's delegation graph,
which `eth_estimateGas` can't see through.

Symptom: a contract whose execution path ends with `WNAT.transfer(user, amount)`
runs cleanly through all its accounting and external calls, then OOGs inside the
final WNAT transfer. The 63/64 rule kicks in at the tail: by the time the outer
call has spent most of the budget on the upstream work, only a sliver is
forwarded into WNAT's hooks. The first hook clears, the second OOGs, the whole
tx reverts with no useful reason. Wallets under-estimate because the hook gas
isn't reachable from a standard simulation.

This matters anywhere your contract pays the user in wrapped-native at the end
of a multi-step flow — vault redemptions, claim-and-forward patterns, batch
exits that ultimately settle in WNAT. The fix is the same as the `try/catch`
case: **pin outer gas on the frontend**. Default to 10M-12M on Flare/Songbird.

```typescript
writeContract({
  address: vault,
  abi,
  functionName: "withdraw",
  args: [assets, receiver, owner],
  gas: 12_000_000n,   // ← absorbs WNAT vote-power hooks at the tail
});
```

General rule: when pinning gas for any contract write, lean high. The downside
of pinning too high is "wallet shows a slightly scary number"; the downside of
pinning too low is "tx silently OOGs, user pays gas anyway, you ship a hotfix."

### `block.basefee` is essentially zero on cheap Flare-family chains

Coston2 basefee = 1 wei. Songbird basefee = 2 wei. Flare basefee ≈ 25 gwei.

If you're building anti-spam economics that gate on
`required = basefee × gasEstimate × multiplier`, the gate **collapses to zero on the
cheap chains** unless you floor `basefee` at something like 25 gwei. Treat
`max(block.basefee, MIN_BASEFEE)` as the effective basefee, with `MIN_BASEFEE`
configurable but capped (don't let owner set it to 1000 ETH and brick the system).

---

## 4. WNAT, FTSO, and Enosys's redistributor naming churn

WNAT (wrapped FLR / SGB / C2FLR) holders earn **FTSO delegation rewards** and
historically **FlareDrops**. Pools, vaults, and limit-order contracts that hold WNAT
need to harvest these on behalf of users.

### `vm.deal()` corrupts WNAT vote-power state in fork tests

WNAT is not a vanilla ERC-20 — it has FTSO vote-power checkpoints. `vm.deal(addr, X)`
sets the balance directly without updating the checkpoint. The next time *any* address
tries to `safeTransfer` WNAT (even one unrelated to your test), the call reverts with
**`STF`** (SafeTransferFrom) or similar, because the checkpoint is internally
inconsistent.

**Fix**: in fork tests, fund accounts via the deposit path:

```solidity
vm.deal(alice, 10_000 ether);          // give alice native FLR/SGB
vm.prank(alice);
(bool ok,) = WNAT.call{value: 10_000 ether}(abi.encodeWithSignature("deposit()"));
require(ok, "WNAT deposit failed");    // alice now has WNAT, checkpoint correct
```

`deal(token, addr, amount)` (the `forge-std` helper, lowercase) works fine for
**non-WNAT** ERC-20s like USDT0, USDC, FXRP — just not for WNAT itself.

**WNAT recipient-side reverts CANNOT block transfers**. The hook only updates
internal state on the WNAT contract; it does not call into the recipient. A
contract whose `receive()` and `fallback()` both `revert("blocked")` still
receives WNAT successfully. Empirically confirmed against live Flare WFLR
2026-05-08 — useful to know when an audit tries to flag a `safeTransfer(WFLR, ...)`
to an unknown recipient as a DoS vector.

### FTSO reward-claim gas blows past naive estimates

A long-held NFT position with many accrued FTSO epochs can require **7M+ gas** just
to claim its rewards. One real Enosys V3 NFT on Flare was observed consuming
**7.67M gas** on a single `claim` call — and that was an active mid-life NFT, not the
worst case.

When designing an `executeBatch` or `cancelOrder` path that auto-claims rewards
before burn, reserve **at least 10M inner gas** for the claim and pin outer gas
accordingly. Provide a recovery path (e.g. `claimDelegationRewardsFull(orderId)`)
that forwards all caller gas with no inner cap, so users with overflowing NFTs
have an out.

### Enosys redistributor rotation — naming chaos, same ABI

As of 2026-04, three different redistributor contracts have existed on Flare. **They
share the same ABI shape but are not interchangeable.**

| Contract | Address | Status | Handles |
|---|---|---|---|
| `FlaresRewardsRedistributorForNft` | `0x4410B821Fa1041D242f2C199C0EA78E4A5f15F19` | **Legacy** | FTSO + FlareDrops (NFT-aware) |
| `FtsoRewardRedistributorForNft` | `0x5a0BfF8Ff1AF1DF28619Fce57d07E3bBb7BAF3d7` | **Current Flare** | FTSO delegation only |
| `FtsoRewardRedistributorForAddress` | `0x45aAa2e37B89f7514DF69FA084f381C67891C381` | Different ABI! | FTSO for naked WNAT delegations |

On Songbird, `FtsoRewardRedistributorForNft` lives at `0x421294D3eb38c87390fc7f1442623f5b7DBc5b86`.

**Critical**: `FtsoRewardRedistributorForAddress` takes `address[]` not `uint256[]`
in its `claim` function. **Never register it on a contract that expects an
NFT-aware redistributor** — the selector mismatch will revert every claim call.

FlareDrops are no longer routed through any of the LOM-claimable redistributors;
that path moved to a separate Enosys-handled flow in the 2026-04 rotation.

### How to identify the live redistributor for a given DEX

1. Check if it's a proxy (EIP-1967 implementation slot
   `0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc`).
2. Call `getUnclaimed([<known-active-NFT-id>])`. The active redistributor returns
   non-zero for active NFTs; legacy or wrong ones return 0 even for active NFTs.
3. NFT id `1` is usually a safe probe — if it returns 0 from one redistributor and
   non-zero from another, the non-zero one is current.

### `RewardManager` ≠ Redistributor

Enosys's `RewardManager` (e.g. Songbird `0xa997E5FD…` for DEX-level pool incentives)
has a **different signature** from the NFT redistributors:
`claim(uint256[] ids, uint256 epochsToClaimCnt, address recipient)` — note the extra
`epochsToClaimCnt` parameter. A contract expecting the redistributor ABI will revert
on selector mismatch if you wire `RewardManager` in by accident.

### Coston2's redistributor returns 0 even for live NFTs

Coston2 has the FTSO contracts deployed but rewards aren't flowing — `getUnclaimed`
always returns 0. Order/fill flow works for development; reward-path testing has
to happen on Songbird or Flare. Don't waste time debugging "no rewards" on Coston2.

---

## 5. Foundry / fork-test patterns

### Fork tests must self-skip when CI runs without `--fork-url`

`forge test` runs every test by default. Tests that bake real mainnet addresses into
`setUp()` will fail with `call to non-contract address 0x…` when CI runs without
fork. Cleanest fix: gate on `block.chainid`.

```solidity
function setUp() public {
    // Fork-only test: skip in default (non-forked) CI runs.
    // Run locally with: forge test --fork-url flare --match-contract MyTest -vvv
    if (block.chainid == 31337) {
        vm.skip(true);
        return;
    }
    // …rest of setUp using real Flare addresses
}
```

`31337` is Anvil's default chain ID (also Foundry's default test chain). On a real
fork (`14`/`19`/`114`) the guard is a no-op. `vm.skip(true)` requires a recent
forge-std (post-1.8); use `return;` alone if that's unavailable but you'll see a
"setUp succeeded but no tests ran" warning.

### Stack-too-deep in deploy scripts → extract to internal helpers

Foundry scripts often accumulate locals in `run()`: env-var reads, factory
references, address parsing. Yul codegen hits "variable too deep in stack." Fix by
extracting groups of locals to internal helpers:

```solidity
function run() external {
    address deployed = _deployCore();
    _applyTreasuryAndFeeSplit(deployed);
    _applyPricingConfig(deployed);
    // ...
}

function _applyTreasuryAndFeeSplit(address mgr) internal { /* scoped locals */ }
function _applyPricingConfig(address mgr) internal { /* scoped locals */ }
```

Each helper gets its own stack window, so depth resets at every call boundary.

### `forge fmt --check` is strictly enforced in CI — pre-format before pushing

If your repo's CI runs `forge fmt --check`, every column-alignment difference
fails the run. The formatter has strong opinions about:

- Single-space between type and identifier (`uint24 fee` not `uint24   fee`)
- Single-space inside `require(cond, "msg")` (no double-space alignment)
- Multi-line return tuples in interface definitions
- Brace placement on multi-modifier function declarations

**Before opening a PR, run `forge fmt`** and commit. The formatter is deterministic;
its output is the only formatting CI accepts.

### Scope contract CI to contract-relevant paths

Don't run the full `forge build + test` pipeline on doc-only or frontend-only
commits. Path-filter the workflow:

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'test/**'
      - 'script/**'
      - 'lib/**'
      - 'foundry.toml'
      - 'remappings.txt'
      - '.github/workflows/test.yml'
  pull_request:
    paths: [ … same … ]
  workflow_dispatch:
```

Frontend-only / docs-only PRs no longer trigger contract CI.

---

## 6. Frontend UX — Flare-specific patterns

### Native ↔ wrapped-native shortcut paths in swap UIs

The DEX has no `native ↔ wrapped` pool — and shouldn't. When a user picks native
on one side and wrapped native on the other (FLR↔WFLR, SGB↔WSGB, C2FLR↔WC2FLR),
**bypass the router entirely** and call the WNAT contract:

- `WNAT.deposit{value: amount}()` — wraps native → WNAT, 1:1, no slippage, no fee
- `WNAT.withdraw(amount)` — unwraps WNAT → native, 1:1

No approval needed for either direction. Show a dedicated info panel ("This is a
1:1 wrap, no slippage applies") instead of the usual route/fee/min-received display
because there's nothing to slip.

### Auto-wrap before token operations that need WNAT

When the user holds bare native but the contract needs wrapped (e.g. a limit order
selling `WSGB` when the user only has `SGB`), don't make them go to the swap tab
and back. Detect the deficit and offer a one-click wrap inline:

```tsx
{nativeBalance >= shortfall && wrappedBalance < requiredAmount && (
  <Banner tone="info">
    Wrap needed: you have {nativeBalance} {native}, need {shortfall} more {wrapped}.
    <Button onClick={wrapShortfall}>Wrap {shortfall} {native} → {wrapped}</Button>
  </Banner>
)}
```

Refresh the wrapped-balance read after `WNAT.deposit` confirms; the order
flow proceeds to Approve and Create automatically.

### Favicon cache is famously sticky

After changing your site's favicon, browsers cache it independently from the page.
Hard-refresh (Ctrl+Shift+R) usually misses the favicon. Tell users (and yourself):

- DevTools → Application → "Clear site data" → reload, OR
- Open in incognito to verify the new icon ships

In Next.js App Router, `app/icon.png` replaces `app/favicon.ico`. **`git rm` the old
`favicon.ico`** when migrating, otherwise CI re-checks it out and serves both;
browsers then pick whichever they cached first.

---

## 7. Deployment, CREATE addresses, and Ledger handoff

### CREATE determinism: same EOA + same nonce ⇒ same address on every chain

If you deploy with the same EOA and the same nonce on Flare and Songbird, you'll
get **the same contract address on both chains**. This is normal, not a bug.
They are entirely separate contracts with separate state and separate storage.

Useful pattern: pre-image the deploy address (offline `keccak256(rlp([sender, nonce]))`),
share it in advance for indexer config, and deploy to each chain when ready.

### Ownable2Step + Ledger pattern

Don't deploy directly from a Ledger — `forge script --ledger` is supported but the
sequence of `registerDex`, `setFeeSplit`, `setTreasury2`, etc. that follow the
constructor is annoying with hardware-wallet confirms.

**Pattern**: deploy from a fresh hot EOA, do all post-deploy configuration, then
hand off via OpenZeppelin's `Ownable2Step`:

1. Hot EOA: `forge script Deploy.s.sol --broadcast` — deploys + registers DEXes + sets fees.
2. Hot EOA: `cast send <contract> 'transferOwnership(address)' <ledger>` — stages the Ledger as `pendingOwner`.
3. Ledger: `cast send <contract> 'acceptOwnership()' --ledger` — completes the handoff.

After step 3 the hot EOA loses all admin power. Use `Ownable2Step` (not `Ownable`)
so a typo in the Ledger address can't permanently brick admin access — the new
owner has to actively accept.

### GitHub Pages + branch protection rules

If you're deploying a frontend via `peaceiris/actions-gh-pages@v4`, the workflow
**force-pushes** to the `gh-pages` branch (`force_orphan: true` or otherwise). If
you have a branch ruleset blocking force-push, the workflow fails with:

```
remote: error: GH013: Repository rule violations found
```

Two ways to fix:
1. Edit the ruleset to **exclude `gh-pages`** from force-push protection.
2. Add the GitHub Actions bot to the ruleset's bypass list.

### Personal Access Tokens + workflow files

A PAT without `workflow` scope cannot push changes to `.github/workflows/*`:

```
remote: error: refusing to allow a Personal Access Token to create or update
workflow `.github/workflows/test.yml` without `workflow` scope
```

Fix: add `workflow` scope to the PAT, OR make workflow file edits via the GitHub
web editor, OR push from a token/key that has the scope. For automation
(Claude Code, CI bots, etc.) this is a gotcha worth flagging early.

### GitBook ↔ GitHub sync

GitBook's **green "Connected" button is OAuth only** — that proves identity, not
repo access. If after connecting, GitBook's Account dropdown shows "No items"
when you try to add a repo, you also need to install the **GitBook GitHub App**:

1. From GitBook's repo-picker page, click "Install the GitHub app".
2. Choose `Only select repositories` and pick the doc repo.
3. Refresh GitBook — the dropdown now lists the repo.

Both OAuth and the App install are required.

---

## 8. Quick reference card

| Question | Answer |
|---|---|
| RainbowKit MetaMask hangs | Use `injectedWallet`, not `metaMaskWallet` |
| Server-side Ankr fails with -32079 | Browser key is origin-locked; generate IP-locked key for servers |
| `eth_getLogs` block range too wide | Public Flare RPCs cap at 30 blocks; switch to Multicall3 + pairwise reads or Ankr |
| Multicall3 address | `0xcA11bde05977b3631167028862bE2a173976CA11` on Flare/Songbird/Coston2 |
| Tx confirmed but did nothing | EIP-150 63/64 + `try/catch` + missing outer gas pin |
| Wallet under-estimates a `try/catch` call | Pin `gas:` on the write; `eth_estimateGas` can't trace through |
| Tx OOGs inside `WNAT.transfer` at the tail | Pin outer gas (10M-12M); vote-power hooks aren't traced by estimateGas |
| `cancelOrder` reverts with `STF` | `vm.deal` corrupted WNAT checkpoint; use `WNAT.deposit()` |
| FTSO claim returns 0 unexpectedly | Outer gas under-pinned, OR rewards stranded on rotated-away redistributor |
| Anti-spam gate too lenient on cheap chain | Floor `block.basefee` at e.g. 25 gwei before sizing the gate |
| CI fails with `call to non-contract address 0x…` | Fork test running without `--fork-url`; gate setUp on `block.chainid == 31337` |
| `forge fmt --check` in CI fails | Run `forge fmt` and commit |
| Ledger handoff bricked admin? | Use `Ownable2Step`, not `Ownable` |

---

## When this skill applies

Trigger this skill on Flare-family work that involves any of:

- Frontend wallet integration (especially RainbowKit + Wagmi)
- RPC choice between public, Ankr, or self-hosted
- Foundry fork tests against Flare/Songbird/Coston2
- FTSO reward claims, redistributor rotation, or "why does my claim return 0"
- Ledger or multisig deploy handoff
- CI failures on contract-touching repos
- Any "transaction confirmed but nothing happened" debugging session
- Dollar-cost decisions about gas estimation when `try/catch` is in the call path

For Enosys-specific contract addresses and DEX V3 patterns, use `enosys-contracts`
and `enosys-dex-v3`. For frontend integration boilerplate, use `enosys-integrations`
(but with the wallet-list correction noted above). This skill is the **third-party
builder's pitfall list** — what you can't learn from looking at someone else's
working code, only by hitting the bug yourself.
