---
name: solana-binary-markets
description: Use this skill when the user wants to interact with onchain binary (YES/NO) prediction markets on Solana — trade outcomes, list markets, create new markets, especially for tail-asset / long-tail events. Covers the major Solana prediction venues.
---

# Solana Binary Prediction Markets

## Overview

A **binary market** is a market with exactly two outcomes — YES or NO — that resolves to one of them at a known future time. Each side is represented as a token (YES token / NO token) that pays out **$1 at resolution** if the side wins, **$0 if it loses**. While a market is live, the YES token trades between $0 and $1, and its price is the market's implied probability of YES:

- YES at $0.62 → market thinks YES is 62% likely
- NO at $0.38 → market thinks NO is 38% likely
- YES + NO always sum to ~$1 (minus spread/fees)

Onchain binary markets are useful because they aggregate forecasts into a single, tradeable, oracle-friendly probability that any other smart contract can read. Polymarket popularized them on EVM; in 2025–2026 the action moved to Solana for three reasons (per Helius CEO @mert listing "onchain binary markets, especially for tail assets" as a top-5 Solana priority):

1. **Cheap, fast settlement** — sub-cent fees and ~400ms finality make low-stakes long-tail markets economically viable, which is impossible on Ethereum L1.
2. **Composability** — outcome tokens are SPL tokens, so any AMM, lending market, or vault can use them.
3. **Capital efficiency** — Solana's perp infra (Drift) lets you express a binary view with leverage and cross-collateral, not just spot YES/NO.

### Current major Solana venues (verified May 2026)

| Venue | Model | Best for | SDK |
|---|---|---|---|
| **Drift BET** (`app.drift.trade/bet`) | Perp-style YES/NO with CLOB (price clamped 0–1) | Liquid crypto / macro markets, leverage, cross-collateral | `@drift-labs/sdk` |
| **DFlow → Kalshi** (`pond.dflow.net`) | Tokenized Kalshi markets (real SPL outcome tokens) routed via DFlow JIT router | Thousands of long-tail real-world markets (sports, politics, weather, econ) | REST API (no SDK needed) |
| **Hxro Parimutuel** | Pooled parimutuel — winners split the pool | Short-duration price events (BTC up/down in 5 min), gaming | `@hxronetwork/parimutuelsdk` |

> **Skip these** — they came up in research but are not viable targets:
> - **Monaco Protocol / BetDEX** — SDK repo archived Nov 2025
> - **Limitless** — runs on Base, not Solana
> - **Polymarket** — has not launched a native Solana deployment as of May 2026; the closest thing is Kalshi-on-Solana via DFlow

## When to use this skill

Trigger this skill when the user wants to:

- List active YES/NO markets on Solana
- Place a bet / trade on a binary outcome
- Build a bot that prices, makes markets, or arbitrages prediction markets
- Create a new market for a tail-asset event (e.g., "Will memecoin X be >$0.10 on June 30?")
- Pull probabilities from onchain markets to use as an oracle in another contract
- Decide which venue fits their use case

## Prerequisites

- **Node 20+** (use `node --version` to check)
- **`@solana/web3.js`** — `npm i @solana/web3.js@^1.95`
- **Wallet** — a `Keypair` loaded from a base58 secret or JSON file. Never commit secrets; read from `process.env.SOLANA_SECRET` or a local `~/.config/solana/id.json`.
- **USDC on Solana** at mint `EPjFWdd5AufqSSqeM2qN1xzybapC8GZsdLPi7Ut5GtT` (note: outcome tokens on DFlow settle against this mint). Bridge from Ethereum via Wormhole/CCTP or buy on a Solana DEX — do **not** use the Wormhole-wrapped USDCet, the venues here want canonical Circle USDC.
- **RPC endpoint** — Helius, QuickNode, or Triton. Public mainnet RPC will be rate-limited.
- For DFlow: wallet must complete **Proof KYC** before placing real-money Kalshi trades.
- Per-venue SDKs (install only what you need):
  - Drift: `npm i @drift-labs/sdk @coral-xyz/anchor`
  - Hxro: `npm i @hxronetwork/parimutuelsdk`
  - DFlow: no SDK needed — REST + `@solana/web3.js` for signing

## Workflow

### Core concepts

**Outcome tokens.** On DFlow/Kalshi, each market mints two SPL tokens: a YES mint and a NO mint. You buy them with USDC at the current market price. At resolution, the winning token redeems 1:1 for USDC; the losing token is worthless. Because they are normal SPL tokens, you can transfer, LP, or borrow against them like any other token.

**AMM vs CLOB.**
- *CLOB (central limit order book)* — Drift BET and DFlow use orderbooks. Tighter spreads, but thin books on tail markets mean you need limit orders, not market orders.
- *AMM* — Some venues use bonding curves (LMSR or constant-product). Prices move continuously with size. Easier liquidity bootstrapping but worse for big tickets.
- *Parimutuel* — Hxro pools all bets and pays winners pro-rata at expiry. No mid-market trading; you only get the final payout ratio.

**Oracle resolution.** Markets resolve when an oracle reports the outcome:
- Drift BET — Drift's keeper network resolves to 0 or 1 based on the market's stated source (e.g., a price reference, a publicly attestable event)
- DFlow/Kalshi — Kalshi is a CFTC-regulated exchange and resolves through its own regulated process; you inherit that resolution onchain
- Hxro — settles against the oracle price feed declared at market creation (typically a Pyth price)

**Pricing as probability.** The YES token's USDC price *is* the probability. To convert:
- `p_yes = yes_price` (in USDC, since YES pays $1)
- `p_no = 1 - p_yes`
- Edge over a "true" model probability `p*`: `edge = p* - p_yes` (buy YES if positive)

### Per-venue: Drift BET

**Listing markets.** Drift represents prediction markets as perp markets where `contractType == Prediction`. Use `DriftClient.getPerpMarketAccounts()` and filter:

```ts
const drift = new DriftClient({ connection, wallet, env: 'mainnet-beta' });
await drift.subscribe();
const allPerps = drift.getPerpMarketAccounts();
const predictionMarkets = allPerps.filter(m => 'prediction' in m.contractType);
```

The oracle price on a prediction market is the implied probability of YES, clamped to [0, 1]. Long = bet YES, Short = bet NO. See `scripts/list-markets.ts` for a runnable example.

**Placing a bet.** Use `DriftClient.placePerpOrder` with `OrderType.LIMIT` and a price between 0 and 1. Market orders work but get filled against the book and can be expensive on thin markets — prefer limits. See `scripts/place-bet.ts`.

**Resolution.** When the market expires, your perp PnL = `(resolution - entry_price) * size` for longs. Close the position with a closing order, or let it auto-settle.

### Per-venue: DFlow + Kalshi

DFlow exposes a REST API; no SDK is needed. Two base URLs (dev — no key required for testing):

- Metadata: `https://dev-prediction-markets-api.dflow.net`
- Trade: `https://dev-quote-api.dflow.net`

Production requires an `x-api-key` header (contact DFlow).

**Listing markets** (browse by category):

```
GET /api/v1/events?seriesTickers=KXEPLGAME&status=active&withNestedMarkets=true
```

Each market in the response has `yesMint`, `noMint`, `yesBid`, `yesAsk`, `noBid`, `noAsk`.

**Buying outcome tokens** — call `/order` with `inputMint=USDC`, `outputMint=<yesMint or noMint>`, `amount` in USDC base units (6 decimals). DFlow returns a base64 transaction; deserialize, sign, and send.

**Redeeming.** After resolution (`result: "yes"` or `"no"`, `redemptionStatus: "open"`), call `/order` again with `inputMint=<winning outcome mint>`, `outputMint=USDC`. Same endpoint handles both buy and redeem — DFlow detects the input.

**Tail-asset coverage.** Kalshi tokenized "thousands" of markets through DFlow in late 2025; this is currently the broadest long-tail surface area on Solana (sports, politics, weather, econ, entertainment).

### Per-venue: Hxro Parimutuel

Best for short-duration price-direction markets:

```ts
import { ParimutuelWeb3, MAINNET_CONFIG } from '@hxronetwork/parimutuelsdk';
const pari = new ParimutuelWeb3(MAINNET_CONFIG, connection);
const contests = await pari.getContests(/* market pubkey */);
```

You stake into LONG or SHORT pools before lockout, the pool settles against the Pyth price at expiry, and winners split the losing side pro-rata to their stake. No mid-market trading — your only choices are stake size and side.

### Creating markets for tail assets

- **Drift BET** — market creation is permissioned to Drift governance; submit a proposal in the Drift Discord/forum with a precise resolution source. Best for assets/events with a clean machine-readable settlement.
- **DFlow/Kalshi** — market creation goes through Kalshi (regulated). You cannot self-list; you can request a market via Kalshi's market request flow, and once listed it appears in DFlow.
- **Hxro** — markets are templates parameterized by oracle feed and duration; new templated markets can be deployed permissionlessly if the underlying Pyth feed exists.

For genuinely permissionless tail-asset market creation, none of the major Solana venues are fully open today (May 2026) — this is a real gap and an opportunity. The closest path is Hxro on a new Pyth-listed asset.

## Common pitfalls

1. **Confusing YES token price with probability when the AMM is skewed.** On AMM venues, the displayed "price" can include a curve-dependent skew; the marginal price (what you'd pay for one more token) differs from the average price you actually get for a large order. Always size against the orderbook depth or AMM curve, not the headline number.

2. **Slippage on thin markets.** Tail markets have $hundreds, not $millions, of depth. A $500 market order can move the price 5–20 cents. Use limit orders at your target probability and walk the book gradually. Set `slippageBps` explicitly on DFlow's `/order` (don't trust `auto` on illiquid markets).

3. **Oracle resolution disputes / ambiguity.** Read the resolution source *before* trading. "Will SOL hit $300 by Dec 31" — at which price source, at which timestamp, with what tick? Drift and Kalshi both publish exact resolution criteria; markets where the source is ambiguous have historically taken weeks to resolve and sometimes get voided.

4. **USDC bridging confusion.** Solana has multiple USDC variants. Canonical Circle USDC is `EPjFWdd5AufqSSqeM2qN1xzybapC8GZsdLPi7Ut5GtT`. Wormhole-wrapped USDCet (`A9mUU4qviSctJVPJdBJWkb28deg915LYJKrzQ19ji3FM`) is *not* accepted by Drift BET or DFlow — you must swap to canonical USDC first (Jupiter handles this in one tx).

5. **Market expiry timing.** "Expires Dec 31" usually means UTC midnight, not your local time. Drift BET shows `expiryTs` (unix seconds); DFlow shows `closeTime` and `settleTime` separately — the market stops trading at `closeTime` but pays out at `settleTime`, which can be hours or days later. Don't park capital in a position you can't redeem promptly.

6. **Fee + funding drag (Drift only).** Drift prediction markets are perps, so they accrue funding payments between longs and shorts. On a 6-month market, funding can eat 5–10% of your edge. Use the funding rate as a probability check: persistently positive funding means longs are paying to be long → market expects mean-reversion toward NO.

7. **Outcome token redemption is not automatic.** On DFlow, winning YES/NO tokens sit in your wallet after resolution — you must call the redemption endpoint to convert them to USDC. They won't auto-settle.

## References

- `scripts/list-markets.ts` — fetch and print active Drift BET prediction markets with current YES prices
- `scripts/place-bet.ts` — place a YES or NO bet on a Drift BET market by symbol or market index
- `references/venues-comparison.md` — side-by-side venue comparison table (fees, oracles, market creation, tail-asset support, SDK maturity)
- [Drift BET docs](https://docs.drift.trade/prediction-markets/prediction-markets-intro)
- [Drift TypeScript SDK](https://drift-labs.github.io/protocol-v2/sdk/)
- [DFlow Prediction Markets API](https://pond.dflow.net/llms.txt)
- [QuickNode guide: Trading Kalshi markets via DFlow on Solana](https://www.quicknode.com/guides/solana-development/3rd-party-integrations/kalshi-prediction-markets-with-dflow)
- [Hxro Parimutuel SDK quickstart](https://docs.hxro.network/developers/parimutuel-tooling/parimutuel-typescript-sdk-quickstart)
