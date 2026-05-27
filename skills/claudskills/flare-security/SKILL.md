---
name: flare-security
description: >
  Security-first checklist for Flare-family contract design, deployment, and audit.
  Covers both (1) GENERIC EVM security patterns the user must apply by default —
  Ownable2Step over Ownable, ReentrancyGuardTransient, SafeERC20, CEI, custom
  errors, no tx.origin, bounded loops, pull-over-push, immutable for constructor
  values — and (2) FLARE-SPECIFIC overlays that the generic audit skills don't
  catch: Permit2 chain availability, fee-on-transfer detection, blacklistable
  stablecoin surface, FTSO redistributor proxy upgradeability, basefee floors on
  testnets, public RPC log-range caps, EIP-3855 PUSH0 status. Use whenever you're
  designing or reviewing a contract that will live on Flare/Songbird/Coston2,
  before EVERY mainnet deploy, and as the gate for the `audit` and `audit-contract`
  skills' scope. Trigger on: "security review", "audit checklist", "is this safe
  for Flare", "ownership", "reentrancy", "Permit2 on Songbird", "blacklistable
  token", "FoT detection", "should I use OZ or transient guard".
---

# Flare-Specific Security Standards

This skill has two halves you should read together:

1. **Foundational secure-coding patterns** that apply to every EVM contract, but
   are non-negotiable here. These are the defaults. Deviating from any of them
   without a documented reason should fail review.
2. **Flare-specific overlays** — things the generic `audit` / `audit-contract`
   skills don't catch because they're not chain-aware.

**Philosophy: assume hostile.** Every external surface — function inputs, token
calls, oracle reads, signatures, calldata, RPCs — is adversarial. Defense in
depth always. The audit reports we've seen on Flare contracts are clear: most
real exploits come from token edge cases, signature replay, missing access
control on admin functions, and FTSO/oracle manipulation. None of those are
exotic — all are preventable with the patterns below.

---

## Part 1 — Foundational secure-coding patterns

### Ownership

**ALWAYS use `Ownable2Step` from OpenZeppelin, never `Ownable`.**

```solidity
import {Ownable2Step, Ownable} from "@openzeppelin/contracts/access/Ownable2Step.sol";

contract MyContract is Ownable2Step {
    constructor(address initialOwner) Ownable(initialOwner) { }
}
```

**Why**: a single-step ownership transfer is a critical vulnerability if the
target address is wrong (typo'd, hardware-wallet path mismatch, contract that
can't accept the role). `Ownable2Step` requires the new owner to call
`acceptOwnership()`, eliminating the silent-handoff failure mode. The cost is
two transactions instead of one — non-issue.

For Flare deployments, the **deploy → handoff** dance is:

1. Deploy from a hot EOA (deployer key).
2. Call `transferOwnership(<Ledger or multisig address>)` — this stages the
   pendingOwner.
3. Have the Ledger / multisig call `acceptOwnership()` to finalize.

After step 3, the deployer EOA has zero privileged access. Verify by reading
`owner()` and `pendingOwner()` (must be `0x0` post-handoff).

For multi-role systems, prefer `AccessControl` from OpenZeppelin with explicit
role-grants. Never invent your own role mapping.

### Reentrancy guards

**Use `ReentrancyGuardTransient` (post-EIP-1153, ~2k gas per call) over the
storage-slot `ReentrancyGuard` whenever your `pragma >=0.8.24`.**

```solidity
import {ReentrancyGuardTransient} from "@openzeppelin/contracts/utils/ReentrancyGuardTransient.sol";

contract MyContract is ReentrancyGuardTransient {
    function externalEntry() external nonReentrant {
        // ...
    }
}
```

**Critical: `nonReentrant` MUST come BEFORE all other modifiers in a function's
modifier list.** This ensures the guard is set before any other modifier could
make an external call. Modifier order is not commutative — it executes
left-to-right.

```solidity
// good — guard sets first
function withdraw(uint256 amount) external nonReentrant onlyOwner whenNotPaused {

// BAD — onlyOwner could (in some patterns) hit external code first
function withdraw(uint256 amount) external onlyOwner nonReentrant whenNotPaused {
```

Cross-function reentrancy is the harder case. If two functions touch the SAME
state variable, both must be `nonReentrant`. Read-only reentrancy (a `view`
function returning stale state during a callback) bites view-based price oracles
— mitigate by validating the read against an independent source.

### Token transfers

**Always use `SafeERC20`, never raw `transfer` / `transferFrom`.** Many tokens
on Flare (USDT0, eUSDT, similar Tether forks) don't return `bool` — a raw call
either reverts your transaction at compile-time-bool-decode-fail or silently
proceeds with a stale-state assumption. SafeERC20 handles both.

```solidity
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

using SafeERC20 for IERC20;

IERC20(token).safeTransfer(to, amount);
IERC20(token).safeTransferFrom(from, to, amount);
IERC20(token).forceApprove(spender, amount);  // NEVER plain approve()
```

**Use `forceApprove`, not `approve`.** Some tokens (USDT-family, KNC) reject a
non-zero → non-zero approval transition; `forceApprove` resets to 0 first when
needed.

For **fee-on-transfer tokens** (FLX, FLRFROG on Flare), `safeTransferFrom` does
NOT validate the recipient's balance change matches the requested amount. The
recipient receives strictly less. Patterns for handling FoT:

- **Read balance before/after** if the contract's logic depends on the actual
  transferred amount.
- **Use a probe** to detect FoT rate up front (see `flare-network` for the
  pattern when integrating with V2 routers via Permit2).
- **Document explicitly** in your contract that FoT tokens are not supported,
  and add a require check that compares balance delta to amount.

### Checks-Effects-Interactions (CEI)

**Always**: validate inputs → update state → make external calls. Never reverse
this order.

```solidity
function withdraw(uint256 amount) external nonReentrant {
    // CHECKS
    if (amount == 0) revert MyContract__ZeroAmount();
    if (balances[msg.sender] < amount) revert MyContract__InsufficientBalance();

    // EFFECTS — update state BEFORE the external call
    balances[msg.sender] -= amount;
    emit Withdrawn(msg.sender, amount);

    // INTERACTIONS — last
    IERC20(token).safeTransfer(msg.sender, amount);
}
```

The reentrancy guard is a backstop. CEI is the primary defense. If you find
yourself writing state changes AFTER an external call, stop and refactor.

### Custom errors over require strings

Custom errors with contract-name prefixes:

```solidity
error MyContract__ZeroAmount();
error MyContract__InsufficientBalance(uint256 have, uint256 want);

function f() external {
    if (x == 0) revert MyContract__ZeroAmount();
}
```

**Why prefix with contract name + `__`**: error selector collisions across
contracts confuse decoder libraries when an error bubbles through a multi-hop
revert. Prefixing makes it unambiguous. The `__` is convention to distinguish
from CamelCase variable names.

Custom errors are cheaper at deploy time (no string in bytecode) and at runtime
(4-byte selector + ABI-encoded args vs. variable-length string). They also let
auditors and frontend code decode the EXACT failure with rich data.

### Immutable + constant for unchangeable values

```solidity
contract MyContract {
    uint256 public constant FEE_BPS = 10_000;        // compile-time, free to read
    address public immutable WRAPPED_NATIVE;          // constructor-set, ~3 gas to read

    constructor(address wrappedNative) {
        if (wrappedNative == address(0)) revert MyContract__ZeroAddress();
        WRAPPED_NATIVE = wrappedNative;
    }
}
```

`SLOAD` is 2,100 gas; `immutable` is essentially free (loaded from bytecode).
For a value read 10× per transaction, that's a 21,000-gas savings — meaningful.

Apply `immutable` to: external contract addresses (oracles, wrappers, registries),
deploy-time-known constants (deployer, wrapped-native, fee receivers if fixed).

### Function visibility

* `external` over `public` for functions only called from outside (`calldata`
  args are cheaper than `memory`).
* `internal` over `private` for testability (allow inheriting test contracts to
  override).
* `public` only when both internal and external callers exist.
* Explicit visibility on every state variable. Solidity warns on missing
  visibility but `internal` is cheap to type and removes ambiguity.

### Modifier order (memorize this)

```solidity
function f() external nonReentrant onlyOwner whenNotPaused {
//                    ^1            ^2        ^3
}
```

1. `nonReentrant` — must run first to lock the guard before any other modifier
   could make an external call.
2. Access control (`onlyOwner`, `onlyRole`).
3. State checks (`whenNotPaused`, `whenInitialized`).

Modifiers should NEVER make external calls (except the reentrancy guard's
transient storage write). External calls in modifiers are unauditable and break
the CEI invariant.

### Bounded loops only

**Never** iterate over an unbounded array of user-controlled length. The block
gas limit on Flare-family chains is ~15M; an unbounded loop hits it eventually
and bricks the function.

```solidity
// BAD — user can grow `pending` indefinitely until withdrawAll() reverts
mapping(address => uint256[]) pending;
function withdrawAll() external {
    uint256[] storage list = pending[msg.sender];
    for (uint256 i; i < list.length; ++i) {  // ← unbounded
        // ...
    }
}

// GOOD — pull pattern, batch size enforced
function withdrawSome(uint256 maxCount) external {
    uint256 n = pending[msg.sender].length;
    uint256 stop = maxCount < n ? maxCount : n;
    for (uint256 i; i < stop; ++i) {
        // ...
    }
}
```

Constants for hard caps:

```solidity
uint256 public constant MAX_BATCH_SIZE = 50;
```

### Pull over push for ETH / token transfers

**Never** `transfer` ETH to user-supplied addresses inside a loop. A single
contract recipient that reverts on `receive()` (or `address.transfer`'s 2300-gas
gate) bricks your loop.

```solidity
// BAD — one bad recipient kills the whole batch
for (uint256 i; i < recipients.length; ++i) {
    recipients[i].transfer(amounts[i]);
}

// GOOD — credit balances, let each user pull
for (uint256 i; i < recipients.length; ++i) {
    pendingWithdraw[recipients[i]] += amounts[i];
}
function claim() external nonReentrant {
    uint256 amt = pendingWithdraw[msg.sender];
    if (amt == 0) revert MyContract__NothingToClaim();
    pendingWithdraw[msg.sender] = 0;
    payable(msg.sender).transfer(amt);
}
```

For tokens, the same principle applies but you can wrap individual transfers in
try/catch and redirect failures to a fallback recipient (the "treasury redirect"
pattern when blacklisted tokens block a treasury address).

### Never use `tx.origin` for authentication

`tx.origin` is the EOA at the start of the call chain. Using it for auth lets
any contract the user has approved (or accidentally interacts with) trick the
contract into authorizing as the user. Use `msg.sender` always.

### Don't trust block values for randomness

`block.timestamp`, `block.number`, `blockhash(N)` are all miner-influenceable. Use
Flare's secure random source (`flare-general` documents this). Never use any
block value to gate financial outcomes.

### Use `block.timestamp` only for long intervals

Miners can shift `block.timestamp` by a few seconds. Don't use it for sub-minute
deadlines. For DEX deadlines, ~10 minutes is the standard floor.

### Avoid `selfdestruct` and `delegatecall`

* `selfdestruct` is being deprecated; in EIP-6780 it only works in the same tx
  as deploy. Don't rely on it.
* `delegatecall` to a user-controlled target = full takeover of your contract.
  Even to a "trusted" target it's a major audit-flag pattern. Justify case by
  case with a documented threat model.

### `abi.encode` over `abi.encodePacked` for hashing

`abi.encodePacked` with two dynamic-size inputs (string, bytes, uint256[]) is
hash-collision-vulnerable: `("ab","c")` and `("a","bc")` hash to the same value.
For hashing dynamic data, use `abi.encode` (length-prefixed).

### Validate every external input

* `address(0)` for any address parameter that shouldn't be zero (revert with a
  named error).
* Bounded ranges on numeric parameters.
* Array length validation when an array's length must equal another's.
* Sanity-check token decimals if they affect math (some tokens have 6, some 24).

### Never silently ignore return values

```solidity
// BAD — returns false on failure for ERC-20s without revert
token.transfer(to, amount);

// GOOD — SafeERC20 reverts on false-return
IERC20(token).safeTransfer(to, amount);

// For low-level calls — always check ok
(bool ok, bytes memory data) = target.call(data);
if (!ok) revert MyContract__CallFailed(target, data);
```

### Front-running mitigations

For any transaction whose value depends on observable state (price, deadline,
nonce), apply at least one of:

1. **Slippage gate** — minimum-output parameter the caller signs.
2. **Deadline** — caller-supplied expiry; fail if `block.timestamp > deadline`.
3. **Commit-reveal** — for high-value actions where front-running would extract
   meaningful value.
4. **Permit2 / EIP-712 signed permits** — bind the spender into the hash so
   replays across contracts are impossible.

### Pause / emergency-stop

Every contract that holds value or controls user funds should have an
owner-callable pause:

```solidity
bool public paused;

modifier whenNotPaused() {
    if (paused) revert MyContract__Paused();
    _;
}

function setPaused(bool paused_) external onlyOwner {
    paused = paused_;
    emit PausedSet(paused_);
}
```

Pause should NEVER affect user-fund-recovery paths. If the contract holds user
tokens and is paused, users must still be able to withdraw what they put in.

---

## Part 2 — Flare-specific overlays

These are the things that bit real Flare deployments and are NOT covered by
generic audit checklists. Apply on top of Part 1 for any contract you ship to
Flare/Songbird/Coston2.

### Permit2 chain availability

The canonical Uniswap Permit2 (`0x000000000022D473030F116dDEE9F6B43aC78BA3`) is
deployed only on **Flare (chain 14)**. NOT on Songbird, NOT on Coston2.

```bash
cast code 0x000000000022D473030F116dDEE9F6B43aC78BA3 --rpc-url <chain>
# Returns full bytecode on Flare; returns 0x on Songbird/Coston2
```

If your contract takes a Permit2 address as an immutable, document this; if it
hardcodes the canonical address, gate deployment on a chain-id check.

For Songbird/Coston2 canary-testing of Permit2-dependent contracts, your only
options are: deploy your own Permit2 (~3000 LOC of Uniswap source — substantial),
mock-only test, or skip canary and validate via Flare fork.

### Fee-on-transfer (FoT) token surface

Multiple tokens on Flare apply a transfer fee — the recipient receives strictly
less than the sender debited. Examples: FLX (`0x22757fb83836e3F9F0F353126cACD3B1Dc82a387`,
~3% FoT), FLRFROG, others.

Threats this creates:
- Your contract calls `transferFrom(user, this, X)` and receives `X * (1-r)`.
- Your contract then calls `safeTransferFrom(this, downstream, X)` — **reverts**
  with `TransferHelper::transferFrom` because you don't have `X` anymore.
- Pair-side V2 swap math may underflow if the actual liquidity received differs
  from what was quoted.

Mitigations:

1. **Probe the FoT rate before encoding the swap calldata** — measure
   `balanceOf(this)` change over a single `transferFrom`, then encode the
   downstream amount as that delta.
2. **Read-and-call pattern in the contract** — `balanceOf(this)` after the input
   transfer to determine the actual amount available, then use that for any
   downstream transfer.
3. **Document non-support** — explicit revert if `received != amount` on input,
   so the user gets a clean failure instead of weird behavior deeper in the call.

### Blacklistable stablecoin surface

USDT0, USDC.e, eUSDT, exUSDT, and similar admin-controlled stablecoins can
freeze any address (including your contract) at the token issuer's discretion.

Implications for your design:

- A blacklisted contract **cannot transfer the token outbound** — pending
  state is stuck.
- Treasury fee splits to a blacklisted treasury address freeze that share — the
  rest of the operation should NOT revert (use try/catch to fall through to a
  redirect).
- **Don't add an admin rescue function** that pulls user-deposited tokens.
  That's a bigger threat than the blacklist itself. Instead document the risk
  and let users avoid the contract for blacklist-prone tokens.

### FTSO redistributor proxy upgradeability

Enosys's `FtsoRewardRedistributorForNft` (the contract you call to claim FTSO
delegation rewards on V3 NFTs) is an upgradeable proxy. The implementation can
change without warning. Implications:

- The interface (function selectors, return shapes) is stable in practice but
  **not guaranteed** in the contract code itself.
- A future upgrade could route claimed rewards somewhere new. Audit-time
  verification is point-in-time only.
- **Always wrap claim calls in try/catch** so a redistributor regression doesn't
  brick your contract's main flow.

```solidity
try IFtsoRewardRedistributorForNft(redistributor).claim(ids, recipient) {
    // ok
} catch {
    // redistributor reverted or mis-routed; continue without rewards
}
```

For per-DEX rotation patterns and recovery via historical addresses, see
`enosys-dex-v3`.

### Native-currency basefee floor

`block.basefee` on Songbird and Coston2 is often **1 wei or 2 wei**. Any
incentive-math gate that uses `basefee * gasEstimate * coverageMultiple` to
require a minimum fee collapses to near-zero on those chains.

If your contract has a fee-incentive-coverage check, add a `minBasefeeWei` floor
(typical: 25 gwei to match Flare's mainnet basefee, owner-tunable up to a hard
cap of 1000 gwei).

```solidity
uint256 effectiveBasefee = block.basefee > minBasefeeWei ? block.basefee : minBasefeeWei;
uint256 required = effectiveBasefee * gasEstimate * minCoverageMultiple;
```

### Public RPC `eth_getLogs` 30-block cap

The public RPC endpoints on Flare/Songbird/Coston2 cap historical log queries to
30 blocks per request. Don't build features that require scanning longer
history off the public RPC.

Workarounds:

1. **Pairwise factory queries via Multicall3** — `factory.getPool(t0, t1, fee)`
   is cheap and scales O(pairs).
2. **Ankr (paid)** — IP-locked or domain-locked keys, lifts to ~5k blocks.
3. **Self-hosted node** — full history, no caps.

### Multicall3 not auto-registered in viem

`Multicall3` lives at `0xcA11bde05977b3631167028862bE2a173976CA11` on every
Flare-family chain, but viem's `defineChain` does NOT auto-add it. If you call
`publicClient.multicall(...)` against a custom-defined chain, it throws silently
with a confusing error. Always register it explicitly:

```ts
defineChain({
  id: 14,
  name: 'Flare',
  // ...
  contracts: {
    multicall3: { address: '0xcA11bde05977b3631167028862bE2a173976CA11', blockCreated: 3002461 },
  },
})
```

### EIP-3855 (PUSH0) status on Coston2

Coston2 emits an EIP-3855 warning when running Solidity 0.8.20+. It's **cosmetic**
— deployments and execution work fine. Don't downgrade `solc` to 0.8.19 over
this warning.

### WFLR transfer hooks

WFLR's `transfer` / `transferFrom` invoke an FTSO delegation-state hook
(`updateAtTokenTransfer`). The hook is **internal state-only on the WFLR
contract itself** — it does NOT call into the recipient. A recipient that
reverts in `receive()`/`fallback()` cannot block delivery. Empirically
verified 2026-05-08 with a Flare-fork test (`WFLR.transfer(evil, 1 ether)`
to a contract whose `receive()` reverts succeeds).

The hook DOES revert with `SafeMath: subtraction overflow` when a SENDER
has phantom balance (`deal(WFLR, addr, X)` writes the balance slot but
skips the delegation state init). That's a **test-setup pitfall, not a
production DoS surface**.

Test setup correction: use `vm.deal(user, X)` + `vm.prank(user); WFLR.deposit{value:
X}()` instead of `deal(WFLR, user, X)`. The latter writes the balance slot but
skips the delegation state init.

**Implication for audit findings**: claims that protocol-fee `safeTransfer`
of WFLR can be DoS'd by a malicious recipient are **categorically false
positives**. Add a fork test to lock the answer down before re-litigation:

```solidity
function test_WflrSafeTransfer_ToRevertingReceiver_Succeeds() external {
    vm.createSelectFork("flare");
    vm.deal(address(this), 10 ether);
    IWNat(WFLR).deposit{value: 10 ether}();
    address evil = address(new RevertingReceiver()); // receive() reverts
    IERC20(WFLR).safeTransfer(evil, 1 ether);        // succeeds
    assertEq(IERC20(WFLR).balanceOf(evil), 1 ether);
}
```

### Token decimals

Sanity-check decimals at integration time. Common confusions:

| Token | Decimals |
|---|---|
| WFLR / WSGB / WC2FLR | 18 |
| USDT0 / USDC.e / FXRP / eUSDT | 6 |
| YAM-V2-style oddities | 24 |

Math involving cross-decimal tokens MUST normalize. The classic precision-loss
bug is `(a / b) * c` — multiply BEFORE dividing.

### Owner-key threat model on Flare

Standard Flare-family ownership pattern: hardware wallet (Ledger) owner via
Ownable2Step, optionally graduating to a multisig (Safe/Gnosis on Flare).

If `owner()` on a deployed contract is a deployer EOA, that's a one-key
compromise away from total loss. Audit findings should flag this and recommend
ownership handoff before mainnet.

The `owner` controls only what the contract's admin functions allow — review
those individually:
- Pause? Ok if it doesn't lock user funds.
- Set fee parameters? Ok if bounded.
- Withdraw user balances? **Critical finding** — never allow.
- Set new oracle addresses? Risky — needs timelock or multisig at minimum.

### Algebra dynamic-fee snapshot drift

Algebra V1.9+ pools (SparkDEX V4) have plugin-driven dynamic fees that adjust
per-block. If your contract snapshots the fee at order-create time and uses it
for incentive math at fill time, the actual fee may drift (typically modestly,
but during volatility regime changes it can shift meaningfully).

Acceptable as approximation in spam-filter contexts. NOT acceptable when the
fee determines a user's payout — read fresh in that case.

### Algebra `MintParams.deployer = address(0)` only safe for default-deployer pools

Algebra's NPM derives the destination pool via `CREATE2(deployer, salt(t0, t1))`.
Passing `deployer = address(0)` uses the factory's default deployer. If a future
DEX registers pools with a custom deployer, mints with `deployer = address(0)`
silently route to the wrong pool.

Mitigation: pre-mint check that `factory.computePoolAddress(t0, t1)` matches
the user's intended pool address. Revert if not.

### Algebra `communityFee` cuts LP fees BEFORE distribution

`globalState().communityFee` is the protocol's cut taken off LP fees before
distributing to LPs. SparkDEX V4 WFLR/USDT0 has `communityFee = 250` (25%).
Any contract that estimates "LP-fee share to executor" must apply this factor:

```solidity
uint256 lpShareBps = 10_000 - globalState.communityFee * 10;  // communityFee is 1/1000
```

### Frontend-supplied calldata trust

Contracts that take router calldata as a passthrough (sweeper-style designs)
must enforce TWO layers:
1. Router-address allowlist (`isRouter[router]`)
2. Function-selector allowlist (`allowedSelector[router][selector]`)

Both layers AND-gated. The selector check is critical — V3's SwapRouter has a
`multicall(bytes[])` that lets calldata chain arbitrary internal calls. **Do
NOT seed `multicall` for any router** unless you've audited the implications.

### Sandwich-floor enforcement on FTSO-anchored swaps

Any time a contract swaps an asset whose price has an FTSO feed (FAsset →
WFLR, WFLR → vault collateral, etc.), the slippage gate should be
**FTSO-anchored**, not pool-quote-anchored. The pattern:

```solidity
// 1. Read the FTSO-implied output for amountIn — the "fair" value.
uint256 ftsoImpliedOut = (amountIn * rateScaled1e36) / 1e36;

// 2. minOut floors at (1 - swapDownsideMaxBps). swapDownsideMaxBps is
//    bounded (typically 50 = 0.5%); never make this caller-controlled.
uint256 minOut = (ftsoImpliedOut * (BPS_DENOM - swapDownsideMaxBps)) / BPS_DENOM;

// 3. Pass minOut to the router AND verify post-swap balance delta.
//    The router enforces minOut against its quote; the balance delta
//    catches FoT tokens that under-deliver while reporting full output.
uint256 wflrBefore = IERC20(WFLR).balanceOf(address(this));
router.exactInput(ExactInputParams({path: path, recipient: address(this), ...}));
uint256 amountOut = IERC20(WFLR).balanceOf(address(this)) - wflrBefore;
if (amountOut < minOut) revert SwapBelowMinOut(amountOut, minOut);
```

**What this defends against**:
- **Sandwich attacks**: a bot pre-positions liquidity to make the router
  pay below FTSO-anchored expectation. Loss is bounded by `swapDownsideMaxBps`
  — typically 0.5% of swap volume. Below that, the swap reverts entirely
  and harvest is retried later.
- **Fee-on-transfer FAsset upgrade**: if a future FAsset proxy upgrade adopts
  FoT, the router-reported `amountOut` would lie. Balance-delta verification
  catches the actual delivered amount.

**Bounded extraction is acceptable**; complete DoS is not. 0.5% is the
break-even point: attackers profit on average less than they spend on LP
fees + gas. Tightening to 0.1% in low-liquidity regimes is fine; loosening
beyond 1% is a finding.

### MEV exposure on owner-only setters

Owner-only parameter setters (`setSwapPath`, `setProtocolFeeBps`, etc.) are
trust-gated by access control, but if the owning multisig is **publicly
executable** (Safe/Gnosis with visible queued transactions, on-chain
governance with mempool-visible voting), an attacker can pre-position
liquidity to extract slippage on the NEXT operation that uses the changed
parameter.

Concrete attack: owner queues `setSwapPath(FXRP, newPath)` switching from a
deep pool to a thinner one. Attacker sees the queued tx, drains the new
pool just before execution, and the next harvest pays the slippage floor.

**Bound**: the same `swapDownsideMaxBps` that protects ordinary swaps.
Attacker cannot force routing through a pool they fully control because
the owner sends the literal path; front-running can't change tx contents.

**Mitigations**:
- Schedule parameter changes during low-balance harvest windows.
- Add a no-harvest-flag for N blocks after the path update.
- For high-stakes parameters, require a timelock (24h+) so the FE can
  display "next harvest will route through new path" warnings.

**Document, don't hide**. List the exposed setters in CLAUDE.md alongside
the bounded extraction estimate. Auditors will flag this otherwise.

---

## Pre-deploy checklist (Flare mainnet)

Run this BEFORE every Flare mainnet broadcast. Don't ship without all green.

- [ ] **Compile clean** — `forge build` no warnings, `forge build --sizes` shows
      all contracts under 24 KB runtime.
- [ ] **Tests pass** — `forge test` (unit) + `forge test --fork-url flare`
      (fork) all green.
- [ ] **Slither clean** — `slither src/ --exclude-informational` reports no
      high or medium findings.
- [ ] **Owner is not the deployer EOA** — `transferOwnership` to Ledger /
      multisig + `acceptOwnership` complete. Verify via `owner()` and
      `pendingOwner()` reads.
- [ ] **`Ownable2Step`** used (not `Ownable`). Verify by reading the bytecode
      dispatch table for `pendingOwner()` / `acceptOwnership()` selectors.
- [ ] **Reentrancy guards present** on every state-changing external function
      that makes external calls or could be re-entered.
- [ ] **CEI compliance** verified — state changes BEFORE external calls in
      every function.
- [ ] **SafeERC20 + forceApprove** used for every token interaction.
- [ ] **No `tx.origin`** in source.
- [ ] **No unbounded loops** over user-controlled data.
- [ ] **Pause + emergency stop** present and tested.
- [ ] **Custom errors** prefixed with contract name + `__`.
- [ ] **`flare-network` registry consulted** — chain IDs, RPC endpoints, token
      addresses match what you're deploying against.
- [ ] **Permit2 chain availability** — if your contract depends on Permit2,
      verified deployed on the target chain.
- [ ] **FoT-token surface considered** — design either supports them or
      explicitly reverts on FoT input.
- [ ] **Blacklistable token surface considered** — if you hold blacklistable
      tokens (USDT0, USDC.e, eUSDT), the design has no admin rescue path AND
      treasury fee paths use try/catch redirects.
- [ ] **Basefee floor** present in any incentive-math (if you have one).
- [ ] **Audit run** — `audit` (checklist) + `audit-contract` (adversarial)
      both completed; findings either fixed or accepted with documented
      reasoning.
- [ ] **Verification dry-run** — after deploy, contract verifies cleanly on
      both `flare-explorer` and `flarescan` (use the commands in
      `flare-network`).

## Audit run instructions

Two skills to run, in order:

### 1. `/audit src/MyContract.sol`

Checklist-driven, 115+ items, SWC classification, weird-ERC20 catalogue. This
is the systematic baseline review.

### 2. `/audit-contract src/MyContract.sol`

Adversarial multi-agent attack. Auto-selects 5–7 specialist attackers based on
the contract's surface (signature handling → signatures agent; external calls →
reentrancy agent; ERC-20 interactions → ERC20-edge-cases agent; multi-party
flows → economic agent; etc.). Writes Foundry PoC tests for any CRITICAL or
HIGH findings.

**For Flare deployments specifically, after the two audit skills run**, reread
this skill's Part 2 to verify the Flare-specific overlays are addressed —
especially Permit2, FoT, blacklistable tokens, and basefee floor. Those items
won't be in the generic audit output.

For a `Full Audit` workflow that combines both audit skills with gas optimization
and test extension, see the `/Full Audit` block at the top of the project's
`CLAUDE.md` — it sequences `audit` → `audit-contract` → `gas-optimize` →
`test-foundry` against a single target file and consolidates findings into one
ranked report.

## Threat model summary (one-page)

| Threat | Defense | Skill section |
|---|---|---|
| Re-entry | `nonReentrant` first + CEI | Part 1 |
| Owner-key compromise | `Ownable2Step` + Ledger/multisig + bounded admin powers | Part 1 |
| Token weirdness (no-return, FoT, blacklist) | `SafeERC20` + balance-delta checks + try/catch on fee paths | Parts 1 + 2 |
| Signature replay | EIP-712 with chainId + nonce + spender binding | Part 1 |
| Front-running | Slippage + deadline + Permit2 | Part 1 |
| Block-value manipulation | Don't use for randomness or short timing | Part 1 |
| Permit2 chain gap | Verify availability + chain-id gate | Part 2 |
| Algebra dynamic fees | Read fresh OR document drift acceptance | Part 2 |
| FTSO redistributor changes | try/catch wrap + historical-allowlist recovery | Part 2 |
| Public RPC log limits | Use Multicall3 / Ankr / self-hosted | Part 2 |
| MEV / sandwich | Slippage + deadline + commit-reveal for high-value | Part 1 |
