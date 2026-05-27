---
name: x402-payments
description: >
  Use whenever the user wants to add payments to an API, monetize endpoints, implement x402,
  handle HTTP 402 responses, create paid APIs, set up crypto paywalls, accept USDC, or build
  agent payments. Trigger on: x402, 402 Payment Required, paid API, paywall, micropayments,
  USDC payments, agent payments, monetize API, payment middleware, x402-next, x402-express,
  x402-fetch, Sentinel, payment router, audit trail, budget caps, payment receipts, facilitator.
  Also trigger when turning a free API into paid, adding per-request pricing, or building
  AI agent autonomous payment flows. Covers Base (EVM) and Solana with USDC.
  Covers Chainlink CRE (Chainlink Runtime Environment) workflows triggered by x402 payments.
  Trigger also on: Chainlink CRE, CRE workflow, onchain automation with payments,
  price alerts with x402, Chainlink price feeds with payments, x402 CRE integration,
  paid CRE workflows, monetize Chainlink workflows.
  Even without "x402" mentioned — if they want to charge for API access with crypto or
  build agent payment infrastructure, this skill applies.
---

# x402 Payments

Build paid APIs and agent payment infrastructure using the x402 protocol. Deploy on **Base (EVM)** and/or **Solana** with USDC. Optionally add **Sentinel Payment Router** for multi-endpoint orchestration, budget caps, and cryptographic audit trails.

## How x402 Works

x402 is an open payment protocol (by Coinbase) built on the HTTP 402 status code. Any API can charge per-request in USDC — no API keys, no subscriptions, no accounts. Clients (humans or AI agents) pay at the moment of use, and the server verifies payment before granting access.

```
Client → GET /api/data → Server
Client ← 402 Payment Required (pricing in headers) ← Server
Client → GET /api/data + X-PAYMENT header (signed authorization) → Server
Server → verifies via Facilitator → settles USDC on-chain
Client ← 200 OK (data) ← Server
```

## Decision Tree

When a user asks for x402 help, determine three things:

### 1. Role: Seller or Buyer?

- **Seller** (API provider) — wants to charge money for their endpoints → Server setup
- **Buyer** (API consumer) — wants to call paid endpoints → Client setup
- **Both** — building a system that both serves and consumes paid APIs

### 2. Chain: Base, Solana, or Both?

- **Base (EVM)** — most common, ~98% of x402 volume uses USDC on Base
  → Read `references/base-evm.md`
- **Solana** — growing ecosystem, uses SPL USDC
  → Read `references/solana.md`
- **Both** — V2 packages support multi-chain registration
  → Read both reference files

### 3. Scale: Single endpoint or multi-endpoint orchestration?

- **Simple** (1-3 endpoints, no audit needs) — basic x402 is sufficient
- **Complex** (multiple endpoints, budget caps, audit trails, AI agents making autonomous payments)
  → Add Sentinel Payment Router. Read `references/sentinel-router.md`

### 4. Chainlink CRE integration?

- **Monetize a CRE workflow** — gate a Chainlink CRE workflow behind x402 payments
  → Read `references/chainlink-cre.md`
- **Pay for a CRE workflow** — call x402-gated CRE endpoints as a client or via Sentinel Router
  → Read `references/chainlink-cre.md`
- **Neither** — skip CRE, standard x402 setup covers most cases

## Quick Reference: All Packages

Read `references/packages.md` for the complete package matrix covering V1 (simple) and V2 (modular) packages, with install commands and compatibility notes.

## Quick Start: Seller on Base (Most Common Path)

This is the fastest path — monetize a Next.js API route on Base mainnet:

```bash
npm install x402-next
```

```typescript
// middleware.ts
import { paymentMiddleware } from "x402-next";

export const middleware = paymentMiddleware(
  "0xYourWalletAddress",
  {
    "/api/premium": {
      price: "$0.01",
      network: "base",
      config: { description: "Premium API access" },
    },
  },
  { url: "https://x402.org/facilitator" }
);

export const config = {
  matcher: ["/api/premium/:path*"],
};
```

```typescript
// app/api/premium/route.ts
import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    data: "This endpoint costs $0.01 per call",
    timestamp: Date.now(),
  });
}
```

Deploy to Vercel. Any request without payment gets a 402 with pricing. Clients with valid X-PAYMENT headers get data.

## Quick Start: Buyer on Base

```bash
npm install x402-fetch viem
```

```typescript
import { wrapFetchWithPayment } from "x402-fetch";
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
const wallet = createWalletClient({ account, chain: base, transport: http() });
const paidFetch = wrapFetchWithPayment(wallet);

const response = await paidFetch("https://example.com/api/premium");
const data = await response.json();
```

## Quick Start: Multi-Endpoint with Sentinel Router

```bash
npm install @x402sentinel/router
```

```typescript
import { PaymentRouter } from "@x402sentinel/router";

const router = new PaymentRouter({
  paymentFetch: paidFetch,
  getPaymentInfo: () => null,
  agentId: "my-agent",
  apiKey: "sk_...",
});

const result = await router.execute({
  name: "research-pipeline",
  maxBudgetUsd: "0.05",
  strategy: "parallel",
  endpoints: [
    { label: "email-verify", url: "https://api.example.com/verify?email=test@gmail.com" },
    { label: "dns-lookup",   url: "https://api.example.com/dns?domain=google.com" },
    { label: "ssl-check",    url: "https://api.example.com/ssl?domain=google.com" },
  ],
});

// result.receipt — unified SHA-256 receipt linking all payments
// result.receipt.receiptHash — tamper-proof hash
// result.receipt.sentinelSig — HMAC server signature
```

Read `references/sentinel-router.md` for the full Router API.

## Chainlink CRE Integration

Chainlink CRE (Chainlink Runtime Environment) is a decentralized execution layer for building on-chain/off-chain workflows. x402 is the first AI payments partner for CRE — agents can discover, trigger, and pay for CRE workflows using x402 micropayments.

Use CRE when you need:
- On-chain data writes triggered by x402 payments
- Scheduled monitoring using Chainlink price feeds
- Push notifications when on-chain conditions are met
- Decentralized workflow execution (not just a centralized server)

### Quick Start

1. Set up Express server with `x402-express` middleware (same as the Express example above)
2. Deploy `RuleRegistry` contract on Base Sepolia
3. Create CRE workflow with HTTP trigger (writes on-chain) + Cron trigger (monitors prices)
4. Flow: Agent pays via x402 → server triggers CRE → data written on-chain → cron monitors → notifies

### Key Packages

- Server: `express`, `x402-express`, `x402-fetch`, `ethers`
- CRE: Chainlink CRE CLI + SDK ([install](https://docs.chain.link/cre/getting-started/cli-installation))
- Contract: Solidity ^0.8.0 with CRE receiver interfaces
- Demo: [smartcontractkit/x402-cre-price-alerts](https://github.com/smartcontractkit/x402-cre-price-alerts)

Read `references/chainlink-cre.md` for the complete setup guide, smart contract templates, CRE workflow structure, and CLI commands.

## Mainnet vs Testnet

| | Testnet | Mainnet |
|---|---------|---------|
| **Base** | `base-sepolia` / `eip155:84532` | `base` / `eip155:8453` |
| **Solana** | `solana-devnet` | `solana-mainnet` |
| **Facilitator** | `https://x402.org/facilitator` | `https://x402.org/facilitator` |
| **Token** | Testnet USDC (free from faucets) | Real USDC |

Always start on testnet. Switch to mainnet by changing the network string.

## Key Concepts

- **Facilitator**: Verifies and settles payments on-chain. Public one at `x402.org/facilitator` is free.
- **Scheme**: Payment structure. `exact` = fixed price per request.
- **EIP-3009**: Token standard enabling gasless USDC transfers. Why x402 works primarily with USDC.
- **CAIP-2**: Chain identifier format. `eip155:8453` = Base. `solana:5eykt...` = Solana mainnet.

## Common Patterns

### Multiple routes with different prices
```typescript
export const middleware = paymentMiddleware(
  "0xYourAddress",
  {
    "/api/basic":   { price: "$0.001", network: "base" },
    "/api/premium": { price: "$0.01",  network: "base" },
    "/api/bulk":    { price: "$0.10",  network: "base" },
  },
  facilitator
);
```

### Accept payments on both Base AND Solana (V2)
```typescript
import { paymentProxy, x402ResourceServer } from "@x402/next";
import { HTTPFacilitatorClient } from "@x402/core/server";
import { ExactEvmScheme } from "@x402/evm/exact/server";
import { ExactSvmScheme } from "@x402/svm/exact/server";

const server = new x402ResourceServer(new HTTPFacilitatorClient({ url: "https://x402.org/facilitator" }))
  .register("eip155:8453", new ExactEvmScheme())
  .register("solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp", new ExactSvmScheme());

export const middleware = paymentProxy({
  "/api/data": {
    accepts: [
      { scheme: "exact", price: "$0.01", network: "eip155:8453", payTo: "0xEvmAddress" },
      { scheme: "exact", price: "$0.01", network: "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp", payTo: "SolanaAddress" },
    ],
    description: "Multi-chain premium data",
  },
}, server);
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| 402 but no payment details | Check middleware matcher covers the route |
| "facilitator unreachable" | Verify `https://x402.org/facilitator` is accessible |
| Payment succeeds but 401 | Increase `maxTimeoutSeconds` |
| "EIP-3009 not supported" | Use USDC only |
| Solana tx fails | Check SOL balance for rent + USDC balance for payment |
| V1 vs V2 confusion | V1: `x402-next`. V2: `@x402/next`. Don't mix them |

## Reference Files

- `references/base-evm.md` — Complete Base/EVM setup (V1 + V2)
- `references/solana.md` — Complete Solana setup
- `references/sentinel-router.md` — Payment Router API
- `references/packages.md` — All npm packages
- `references/chainlink-cre.md` — Chainlink CRE workflows + on-chain automation
