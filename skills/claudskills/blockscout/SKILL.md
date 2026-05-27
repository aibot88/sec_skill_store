---
name: blockscout
description: >
  Blockscout MCP tool reference for on-chain data queries. Covers all 16 tools:
  address info, transactions, token transfers, NFTs, contract ABI/source,
  read-only calls, ENS resolution, and block data across 8+ chains.
  TRIGGER when: user asks about on-chain data, contract state, token balances,
  transaction history, ENS lookup, NFT holdings, or uses blockscout MCP tools.
  DO NOT TRIGGER when: user asks about crypto market prices or trading volume
  (use coingecko skill), or writing Solidity code (use solidity-audit skill).
metadata:
  author: DROOdotFOO
  version: "1.0.0"
  tags: blockscout, blockchain, onchain, mcp, ethereum, web3
---

# Blockscout MCP

On-chain data queries via Blockscout MCP server (already configured).
16 tools across address intelligence, transactions, contracts, and blocks.

## Chain support

**EVM-only.** Blockscout covers 90+ EVM chains. Not available for native Solana
or Tron -- use CoinGecko contract endpoints for token data on those chains.

**Solana via Neon EVM**: Chain 245022934 covers the Neon EVM layer on Solana
(EVM-compatible contracts deployed on Solana).

### Common chain IDs

| Chain | ID | Chain | ID |
|-------|----|-------|----|
| Ethereum | 1 | Arbitrum One | 42161 |
| Polygon | 137 | OP Mainnet | 10 |
| Base | 8453 | zkSync Era | 324 |
| Gnosis | 100 | Scroll | 534352 |
| Celo | 42220 | Mode | 34443 |
| Neon EVM (Solana) | 245022934 | Filecoin | 314 |

Default: Ethereum (1). Use `get_chains_list` to discover all 90+ supported chains.

## Reference

| File | Topic |
|------|-------|
| [tools-reference.md](tools-reference.md) | All 16 tools grouped by category |
| [usage-patterns.md](usage-patterns.md) | Common workflows, pagination, error handling |

## What You Get

- Reference documentation for all 16 Blockscout MCP tools covering address intelligence, transactions, contracts, and block data.
- Chain ID lookup tables and common usage patterns for querying on-chain state across 90+ EVM chains.
- Pagination handling, error recovery, and time-based query guidance for efficient data retrieval.

## See also

- `coingecko` -- market prices, volumes, DEX pools, trending tokens
- `sentinel` -- automated contract monitoring with alert rules
- `ethskills` -- framework selection, RPC providers, EIP/ERC standards
- `solidity-audit` -- smart contract security patterns and audit methodology
