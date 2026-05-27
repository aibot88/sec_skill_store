---
name: spraay-batch-payments
description: Send crypto to multiple recipients in a single transaction across 15 chains. Use when the user asks to batch-send tokens, run payroll, airdrop, distribute bounties, or multi-send on Base, Ethereum, Arbitrum, Polygon, BNB Chain, Avalanche, Solana, Stellar, Bitcoin, XRP Ledger, Stacks, or Bittensor. Supports ETH, ERC-20s, SOL, SPL tokens, XLM, XRP, BTC, TAO, and STX.
license: MIT
metadata:
  author: plagtech
  version: "1.0.0"
---

# Spraay batch payments

Send tokens to up to 200+ recipients in a single transaction. Spraay batch contracts are deployed across 15 chains with a live gateway at `gateway.spraay.app`.

Protocol fee: 0.3% of the total batch amount. Gas savings: ~80% compared to individual transfers.

## When to use

- User wants to send crypto to multiple wallets at once
- User asks about payroll, airdrops, bounty distribution, or DAO payouts
- User mentions "batch payment", "multi-send", "mass transfer", or "spray"
- User needs to pay a list of addresses from a CSV or array

## Batch types

### Native token batch
Send ETH, MATIC, BNB, AVAX, SOL, XLM, XRP, BTC, TAO, or STX to multiple recipients in one transaction.

### ERC-20 / SPL token batch
Send USDC, DAI, WETH, or any ERC-20 token (EVM chains) or SPL token (Solana) to multiple recipients. Automatic approval handling on EVM.

### Equal-amount batch
Send the same amount to every recipient. Specify one amount and a list of addresses.

### Variable-amount batch
Send different amounts to each recipient. Each entry has its own address and amount.

### CSV import batch
Upload a CSV with columns `address,amount` for large-scale distributions (200+ recipients per transaction).

## Supported chains

### EVM chains (smart contract batch)

| Chain | ID | Contract |
|---|---|---|
| Base | 8453 | `0x1646452F98E36A3c9Cfc3eDD8868221E207B5eEC` |
| Ethereum | 1 | `0x15E7aEDa45094DD2E9E746FcA1C726cAd7aE58b3` |
| Arbitrum | 42161 | `0x5be43aA67804aD84fcb890d0AE5F257fb1674302` |
| Polygon | 137 | `0x6d2453ab7416c99aeDCA47CF552695be5789D7ff` |
| BNB Chain | 56 | `0x3093a2951FB77b3beDfB8BA20De645F7413432C1` |
| Avalanche | 43114 | `0x6A41Fb5F5CfE632f9446b548980dA6cE2d75afcC` |
| Unichain | 130 | `0x08fA5D1c16CD6E2a16FC0E4839f262429959E073` |
| Plasma | 6524490 | `0x08fA5D1c16CD6E2a16FC0E4839f262429959E073` |
| BOB | 60808 | `0xEc8599026AE70898391a71c96AA82d4840C2e973` |

All EVM contracts are verified, use OpenZeppelin ReentrancyGuard and Pausable, and support up to 200+ recipients per transaction.

### Non-EVM chains

| Chain | Method |
|---|---|
| Solana | SPL batch via associated token accounts |
| Stellar | Native multi-operation transactions (up to 99 recipients) |
| Bitcoin | PSBT-based multi-output via bitcoinjs-lib + Mempool.space |
| XRP Ledger | Sequential Payment transactions via xrpl.js |
| Bittensor | `utility.batchAll` for atomic multi-transfers |
| Stacks | Clarity contract: `ST7431QK2YMPP3SQYJXZ3GTB6MJVGF07N2EV9R1F.spraay-batch` |

## Gateway endpoint

```
POST https://gateway.spraay.app/api/v1/batch/execute
```

x402 fee: $0.02 USDC per call (paid automatically via the x402 payment protocol on Base).

### Request

```json
{
  "token": "USDC",
  "recipients": [
    { "address": "0xAlice", "amount": "100.00" },
    { "address": "0xBob", "amount": "50.00" },
    { "address": "0xCarol", "amount": "25.00" }
  ]
}
```

- `token` — token symbol (e.g., "USDC", "ETH"). Omit or use "ETH" for native
- `recipients` — array of `{ address, amount }` objects
- Amounts are in human-readable units (not wei/lamports)
- Returns unsigned transaction data for the user's wallet to sign

### Response

The gateway returns transaction data ready for signing. The 0.3% protocol fee is already factored into the transaction.

## Integration

### x402-client (recommended)

```typescript
import { createClient } from "x402-client";

const client = createClient({
  baseUrl: "https://gateway.spraay.app",
  privateKey: process.env.EVM_PRIVATE_KEY
});

const tx = await client.post("/api/v1/batch/execute", {
  token: "USDC",
  recipients: [
    { address: "0xAlice", amount: "100.00" },
    { address: "0xBob", amount: "50.00" }
  ]
});
```

### Spraay dApp (no code)

Users can batch-send directly at [spraay.app](https://spraay.app) — connect wallet, add recipients or upload CSV, and spray.

### MCP server

The `@plagtech/spraay-x402-mcp` server on Smithery wraps all gateway endpoints for MCP-compatible agents.

```bash
npx @smithery/cli install @plagtech/spraay-x402-mcp
```

## Important notes

- The gateway returns unsigned transaction data — the user's wallet must sign and broadcast
- Always confirm recipients, amounts, and total cost with the user before signing
- The 0.3% protocol fee is deducted from the batch amount automatically
- For non-EVM chains, chain-specific transaction formats are returned (PSBT for Bitcoin, XDR for Stellar, etc.)
- The x402 gateway is optimized for Base and Solana USDC

## Resources

- App: https://spraay.app
- Docs: https://docs.spraay.app
- Gateway: https://gateway.spraay.app
- GitHub: https://github.com/plagtech
- MCP: https://smithery.ai/server/@plagtech/spraay-x402-mcp
