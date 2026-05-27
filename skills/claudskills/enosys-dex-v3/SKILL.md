---
name: enosys-dex-v3
description: >
  Deep reference skill for Enosys DEX V3 (CLMM) development on Flare Network.
  Use this skill whenever Darren asks about: building tools or apps that interact
  with Enosys DEX V3 positions (LP position manager, burn tool, reward checker),
  contract addresses for the Enosys V3 position manager or reward system on Flare,
  how delegation rewards / FlareDrops / APS incentives / rFLR work and how to
  claim them on-chain, writing ethers.js v6 code against the Enosys V3 contracts,
  or any task referencing the dex-v3-main codebase. Trigger on any mention of:
  Enosys V3, CLMM, LP position manager, NonfungiblePositionManager, RewardManager,
  FtsoRewardRedistributor, MonthlyRewardManager, APS incentives, delegation rewards,
  FlareDrops, rFLR, burn NFT position, tokensOwed, or pool registry on Flare.
---

# Enosys DEX V3 — Developer Reference

Source-verified from the `dex-v3-main` repository (Next.js/wagmi frontend).
All addresses, ABIs, and reward mechanics confirmed from source code.

## Quick orientation

Enosys DEX V3 is a Uniswap V3 fork (CLMM) on Flare Network (chainId 14).
Positions are ERC-721 NFTs. Each position can accumulate up to **four** distinct
reward types, each with its own contract and claim method. See `references/rewards.md`
for the full breakdown.

## Network

```
Chain ID:     14 (0xe)
RPC:          https://flare-api.flare.network/ext/C/rpc
Explorer:     https://flare-explorer.flare.network
```

## Core contract addresses (Flare Mainnet)

```javascript
const CONTRACTS = {
  POSITION_MANAGER:          '0xD9770b1C7A6ccd33C75b5bcB1c0078f46bE46657',
  FTSO_REWARD_REDISTRIBUTOR: '0x5a0BfF8Ff1AF1DF28619Fce57d07E3bBb7BAF3d7',
  MONTHLY_REWARD_MANAGER:    '0xef514BCC4ab6226f5666a30d0c4672f00946e3dD',
  EPOCH_MANAGER:             '0x389D610CBB52A2Da635a589013Ba542e807C74f7',
  V3_FACTORY:                '0x17AA157AC8C54034381b840Cb8f6bf7Fc355f0de',
  SWAP_ROUTER:               '0x5FD34090E9b195d8482Ad3CC63dB078534F1b113',
  QUOTER:                    '0x0A32EE3f66cC9E68ffb7cBeCf77bAef03e2d7C56',
  PERMIT2:                   '0xbbeb21bad924f2b4c5ff4c3eb209112a04090838',
}
```

## Minimal ABIs (ethers.js v6 human-readable)

### NonfungiblePositionManager
```javascript
const POSITION_MANAGER_ABI = [
  'function balanceOf(address owner) view returns (uint256)',
  'function tokenOfOwnerByIndex(address owner, uint256 index) view returns (uint256)',
  'function positions(uint256 tokenId) view returns (uint96 nonce, address operator, address token0, address token1, uint24 fee, int24 tickLower, int24 tickUpper, uint128 liquidity, uint256 feeGrowthInside0LastX128, uint256 feeGrowthInside1LastX128, uint128 tokensOwed0, uint128 tokensOwed1)',
  'function collect((uint256 tokenId, address recipient, uint128 amount0Max, uint128 amount1Max) params) returns (uint256 amount0, uint256 amount1)',
  'function burn(uint256 tokenId)',
  'function multicall(bytes[] calldata data) payable returns (bytes[] results)',
]
```

### RewardManager (APS incentives — one instance per pool)
```javascript
const REWARD_MANAGER_ABI = [
  'function getUnclaimed(uint256[] nftIds, uint256 epochsToClaimCnt) view returns (uint256 totalReward)',
  'function claim(uint256[] nftIds, uint256 epochsToClaimCnt, address recipient) returns (uint256)',
  'function rewardToken() view returns (address)',
]
```

### FtsoRewardRedistributor + MonthlyRewardManager (same ABI shape)
```javascript
const FTSO_MONTHLY_ABI = [
  'function getUnclaimed(uint256[] nftIds) view returns (uint256 totalReward)',
  'function claim(uint256[] nftIds, address recipient) returns (uint256 totalReward)',
]
```

### ERC-20
```javascript
const ERC20_ABI = [
  'function symbol() view returns (string)',
  'function decimals() view returns (uint8)',
]
```

## Reward system — how to check and claim

Read `references/rewards.md` for the full mechanics. Summary:

| Reward type        | Contract                   | Check method                          | Condition to check      |
|--------------------|----------------------------|---------------------------------------|-------------------------|
| Swap fees          | POSITION_MANAGER           | `tokensOwed0/1` from `positions()`    | Always                  |
| APS incentives     | per-pool RewardManager     | `getUnclaimed([id], 80)`              | Pool has rewardManagers |
| Delegation (FTSO)  | FTSO_REWARD_REDISTRIBUTOR  | `getUnclaimed([id])`                  | Pool is `native: true`  |
| FlareDrops monthly | MONTHLY_REWARD_MANAGER     | `getUnclaimed([id])`                  | native + chainId === 14 |
| rFLR               | n/a — display only         | via portal.flare.network              | Pool has `rflr: true`   |

> **WFLR pool fallback:** If a pool is missing from the registry, also run FTSO/Monthly
> checks when `token0 === WFLR_ADDR || token1 === WFLR_ADDR`. This catches WFLR-containing
> pools that weren't registered. Always check `isNative || isWflrPool`.
> `WFLR_ADDR = '0x1d80c49bbbcd1c0911346656b529df9e5c2f783d'` (lowercase for comparison)

## Fee growth math (in-range positions)

`tokensOwed0/1` from `positions()` only reflects fees collected at last interaction.
For in-range (active) positions, true pending fees must be reconstructed from the
pool's fee growth accumulators. Use these helpers (ethers.js v6 / vanilla BigInt):

```javascript
const U256 = 1n << 256n

function u256sub(a, b) {
  const r = a - b
  return r < 0n ? r + U256 : r
}

function calcFeeGrowthInside(fgGlobal, lowerFGO, upperFGO, tickLower, tickUpper, tickCurrent) {
  const fgBelow = tickCurrent >= tickLower ? lowerFGO : u256sub(fgGlobal, lowerFGO)
  const fgAbove = tickCurrent <  tickUpper ? upperFGO : u256sub(fgGlobal, upperFGO)
  return u256sub(u256sub(fgGlobal, fgBelow), fgAbove)
}

function calcPendingFeeAmount(liquidity, fgiCurrent, fgiLast) {
  return (liquidity * u256sub(fgiCurrent, fgiLast)) >> 128n
}
```

**Required pool contract calls** (add to `V3_POOL_ABI`):
```javascript
'function feeGrowthGlobal0X128() view returns (uint256)',
'function feeGrowthGlobal1X128() view returns (uint256)',
'function ticks(int24 tick) view returns (uint128 liquidityGross, int128 liquidityNet, uint256 feeGrowthOutside0X128, uint256 feeGrowthOutside1X128, int56 tickCumulativeOutside, uint160 secondsPerLiquidityOutsideX128, uint32 secondsOutside, bool initialized)',
```

Fetch `fgGlobal` from pool, `feeGrowthOutside0/1X128` from `ticks(tickLower)` and `ticks(tickUpper)`, then call `calcFeeGrowthInside`. Compare result against `pos.feeGrowthInside0/1LastX128` from `positions()` using `calcPendingFeeAmount`.

**Claim sequence** (run sequentially, continue on individual failure):
1. Fees → `collect({ tokenId, recipient, amount0Max: MAX_UINT128, amount1Max: MAX_UINT128 })`
2. APS incentives → `rewardManager.claim([tokenId], 10, recipient)` — gas: `min(est*2, 8_000_000)`
3. Delegation → `ftsoRewardRedistributor.claim([tokenId], recipient)` — if native pool
4. Monthly drops → `monthlyRewardManager.claim([tokenId], recipient)` — if native + chainId 14

## Pool registry

Read `references/pools.md` for the full pool list. Key fields per pool entry:
- `native: true` — pool earns delegation rewards + FlareDrops
- `rflr: true` — pool participates in monthly rFLR program (display-only link)
- `rewardManagers: [...]` — APS incentive managers; always use the **last entry** as the active one

```javascript
function findPool(token0, token1, fee, registry) {
  const t0 = token0.toLowerCase(), t1 = token1.toLowerCase()
  return registry.find(p =>
    p.fee === fee &&
    ((p.tokens[0].toLowerCase() === t0 && p.tokens[1].toLowerCase() === t1) ||
     (p.tokens[0].toLowerCase() === t1 && p.tokens[1].toLowerCase() === t0))
  ) || null
}

function getActiveRewardManager(pool) {
  if (!pool?.rewardManagers?.length) return null
  return pool.rewardManagers[pool.rewardManagers.length - 1]
}
```

## Token registry (Flare Mainnet key tokens)

```javascript
const TOKENS = {
  WFLR:  { address: '0x1D80c49BbBCd1C0911346656B529DF9E5c2F783d', decimals: 18 },
  USDT0: { address: '0xe7cd86e13AC4309349F30B3435a9d337750fC82D', decimals: 6  },
  sFLR:  { address: '0x12e605bc104e93B45e1aD99F9e555f659051c2BB', decimals: 18 },
  HLN:   { address: '0x140D8d3649Ec605CF69018C627fB44cCC76eC89f', decimals: 18 },
  APS:   { address: '0xfF56Eb5b1a7FAa972291117E5E9565dA29bc808d', decimals: 18 },
  FXRP:  { address: '0xAd552A648C74D49E10027AB8a618A3ad4901c5bE', decimals: 6  },
  CDP:     { address: '0x6Cd3a5Ba46FA254D4d2E3C2B37350ae337E94a0F', decimals: 18 },
  EUSDT:   { decimals: 6  },
  EETH:    { decimals: 18 },
  EQNT:    { decimals: 18 },
  'USDC.E':{ decimals: 6  },
  USDT_SG: { decimals: 6  },   // "USDT (SG)"
  USDX:    { decimals: 18 },
}
// For unknown tokens, fall back to ERC-20 symbol() + decimals()
```

## Key constants

```javascript
const MAX_UINT128            = 2n ** 128n - 1n
const FEE_TIER_LABELS        = { 100: '0.01%', 500: '0.05%', 3000: '0.30%', 10000: '1.00%' }
const INCENTIVE_EPOCHS_CHECK = 80    // getUnclaimed wide window
const INCENTIVE_EPOCHS_CLAIM = 10    // claim() window
const INCENTIVE_GAS_CAP      = 8_000_000n
const RFLR_PORTAL_URL        = 'https://portal.flare.network'
const EXPLORER_BASE          = 'https://flare-explorer.flare.network'
```

## Burn eligibility

A position NFT can only be burned when ALL of the following are true:
- `liquidity === 0n`
- `tokensOwed0 === 0n` AND `tokensOwed1 === 0n` (swap fees)
- `getUnclaimed([tokenId], 80) === 0n` on its rewardManager (APS)
- `ftsoRewardRedistributor.getUnclaimed([tokenId]) === 0n` (if native pool)
- `monthlyRewardManager.getUnclaimed([tokenId]) === 0n` (if native + Flare)

Re-verify by re-calling `positions(tokenId)` immediately before sending the burn tx.

## App architecture pattern (from dex-v3-main)

The existing frontend splits position rows into two components:
- **InactivePositionRow** — zero-liquidity positions. Uses `tokensOwed0/1` directly (no fee growth math). Loads ~3-4 RPC calls total.
- **ActivePositionRowFull** — positions with liquidity. Runs full fee growth recalculation using feeGrowthGlobal + tick data from pool `slot0` and `ticks()`. Heavier (~15 RPC calls).

The gate component (`ActivePositionRow`) fetches tokenId + position data (2 calls), checks `liquidity === 0n`, and routes to the appropriate component. This is the right pattern to replicate in vanilla JS tools.

## Reference files

- `references/rewards.md` — full reward mechanics, epoch system, gas notes
- `references/pools.md` — complete Flare pool registry (~36 pools) with all addresses and flags
