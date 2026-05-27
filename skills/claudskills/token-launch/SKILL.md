---
name: solana-token-launch
description: Use this skill when the user wants to launch a fungible token on Solana (SPL or Token-2022), set metadata, mint supply, revoke authorities, and optionally add liquidity on Raydium/Meteora/Orca.
---

# Token Launch

## Overview
Solana has two token programs: the original **SPL Token** (`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`) and **Token-2022** (`TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`), a superset that adds optional "extensions" — metadata, transfer fees, interest, confidential transfers, permanent delegate, etc. As of 2026, **Token-2022 with the on-mint Metadata extension is the default for new fungible launches**: it stores name/symbol/URI inside the mint account itself (no separate Metaplex PDA), is supported across Phantom, Jupiter, Raydium, Meteora, and Orca, and is cheaper to deploy. Stick with classic SPL Token only when integrating with old contracts that hardcode the legacy program ID. See `references/token2022-vs-classic.md` for the full comparison.

## When to use this skill
- "Launch a token on Solana" / "create an SPL token"
- "Mint a memecoin" / "make a fungible token with metadata"
- "Deploy a Token-2022 with on-chain metadata"
- "Set up Raydium / Meteora / Orca liquidity for my new token"
- "Revoke mint authority" / "lock LP"

Not for: NFTs (use mpl-core or mpl-token-metadata NFT flow), staking programs, or Anchor program scaffolding.

## Prerequisites

Pin these versions — verified against devnet on 2026-05-18:

```bash
# CLI
solana --version          # agave-cli 3.x (install via https://release.anza.xyz/stable/install)
spl-token --version       # spl-token-cli 5.x

# Node packages (package.json)
{
  "dependencies": {
    "@solana/web3.js": "1.98.0",
    "@solana/spl-token": "0.4.14",
    "@solana/spl-token-metadata": "0.1.6",
    "@metaplex-foundation/mpl-token-metadata": "3.4.0",
    "@irys/upload": "0.0.18",
    "@irys/upload-solana": "0.2.7",
    "bs58": "6.0.0"
  },
  "devDependencies": {
    "typescript": "5.6.3",
    "tsx": "4.19.2",
    "@types/node": "22.9.0"
  }
}
```

Note on web3.js: this skill uses `@solana/web3.js` v1 (1.98.x). The new "kit" (`@solana/kit`, formerly web3.js v2) is faster but the SPL Token Extensions helpers still ship with v1-compatible APIs in 0.4.x. Migrate to kit once `@solana-program/token-2022` reaches feature parity for metadata helpers.

## Workflow

### 1. Create wallet + fund (devnet)

```bash
solana-keygen new -o ~/.config/solana/devnet.json
solana config set --url devnet --keypair ~/.config/solana/devnet.json
solana airdrop 2
solana balance
```

### 2. Create the mint (Token-2022, metadata extension enabled)

CLI path — fastest for a sanity check:

```bash
spl-token --program-2022 create-token \
  --decimals 9 \
  --enable-metadata
# -> Address:  <MINT_ADDRESS>
```

Script path — see `scripts/launch-token.ts` for the programmatic version that builds the `CreateAccount` + `InitializeMetadataPointer` + `InitializeMint` + `InitializeMetadata` instructions in **one atomic transaction** (required ordering — metadata pointer must come before mint init, and TLV-aware sizing must be computed up front).

### 3. Create the associated token account (ATA)

```bash
spl-token create-account <MINT_ADDRESS> --program-2022
```

### 4. Mint initial supply

`--decimals 9` means 1 token = 1_000_000_000 base units. To mint 1,000,000,000 whole tokens:

```bash
spl-token mint <MINT_ADDRESS> 1000000000
```

### 5. Off-chain metadata JSON

The mint's URI must point at a JSON file with this shape (Metaplex Fungible Standard; same schema works for Token-2022 metadata extension):

```json
{
  "name": "My Token",
  "symbol": "MYT",
  "description": "Short description shown in wallets and explorers.",
  "image": "https://gateway.irys.xyz/<IMAGE_TX_ID>",
  "external_url": "https://mytoken.xyz",
  "attributes": []
}
```

### 6. Upload image + metadata to Arweave via Irys

```ts
import { Uploader } from "@irys/upload";
import { Solana } from "@irys/upload-solana";

const irys = await Uploader(Solana).withWallet(secretKeyBs58);
const imageReceipt = await irys.uploadFile("./logo.png");
// imageReceipt.id -> use in metadata JSON's "image" field
const metaReceipt = await irys.upload(JSON.stringify(metadata), {
  tags: [{ name: "Content-Type", value: "application/json" }],
});
const uri = `https://gateway.irys.xyz/${metaReceipt.id}`;
```

Funding: `irys.fund(irys.utils.toAtomic(0.01))` (SOL) buys ~10 MB of permanent storage. Pay once, hosted forever.

### 7. Attach metadata to the mint

If you used `--enable-metadata` at create time, run:

```bash
spl-token initialize-metadata <MINT_ADDRESS> "My Token" "MYT" "https://gateway.irys.xyz/<META_TX_ID>"
```

The script in `scripts/launch-token.ts` does this in the same transaction as mint creation.

### 8. Revoke mint authority (one-way; locks supply forever)

```bash
spl-token authorize <MINT_ADDRESS> mint --disable
```

Do this only after you have minted the final supply. There is **no undo**. Many projects revoke right after step 4 to signal "supply is fixed" to investors.

### 9. Freeze authority — keep vs revoke

- **Revoke** if you want maximum trust (DEX listings, memecoin launches, decentralization signaling).
- **Keep** if you need the ability to freeze sanctioned addresses (stablecoins, RWA, compliance-bound tokens).

```bash
spl-token authorize <MINT_ADDRESS> freeze --disable
```

### 10. LP options (deposit liquidity on a DEX)

| DEX | Pool Type | Best For | Pool Creation Cost | Notes |
|---|---|---|---|---|
| **Raydium CPMM** | x*y=k constant product | New launches, memecoins, broad accessibility | ~0.15 SOL | Default starting point. Jupiter routes through it heavily. CPMM accepts Token-2022 (CLMM does not, as of 2026-05). |
| **Meteora DLMM** | Dynamic bins, concentrated | Memecoins post-launch, dynamic fees (0.15%–15%) | ~0.1 SOL | Great for volatile assets; bin-based concentrated liquidity reduces IL with active management. |
| **Orca Whirlpools** | Concentrated, tick-based | Stable pairs, established tokens, capital-efficient LPs | ~0.05 SOL | Cleanest UI. Supports Token-2022 with most extensions; check `transferFeeConfig` compatibility before listing. |

Typical launch playbook: seed initial liquidity on Raydium CPMM, then mirror on Meteora DLMM once you have organic volume.

### 11. Lock LP tokens

After creating a pool you receive LP tokens. Choices:

- **Burn LP** (Raydium "Burn & Earn"): irreversible, strongest trust signal, gives up future LP fee claims unless using Raydium's fee-claim wrapper.
- **Lock LP via Streamflow**: time-locked, immutable, non-cancelable, generates a public proof link. Standard for memecoins targeting 6–12 month locks.
- **Lock LP via Team Finance**: cross-chain UX, slightly higher fees, supports Solana since 2024.

Streamflow CLI/SDK: https://docs.streamflow.finance — typical lock takes <60 seconds via UI.

## Common pitfalls

1. **Wrong program ID**: `TOKEN_PROGRAM_ID` (classic) vs `TOKEN_2022_PROGRAM_ID`. The ATA derivation differs by program. Passing the wrong one to `getAssociatedTokenAddressSync` silently returns an unusable address.
2. **Metadata pointer ordering**: `InitializeMetadataPointer` must be emitted **before** `InitializeMint`, and `InitializeMetadata` (which writes the TLV data) must come **after** the mint is initialized. Putting all four (CreateAccount, MetadataPointer init, Mint init, Metadata init) in one atomic transaction is the only safe pattern.
3. **Mint account size**: with extensions you cannot use `MINT_SIZE` (the classic 82 bytes). You must use `getMintLen([ExtensionType.MetadataPointer])` and then *additionally* fund rent for the TLV metadata bytes (`pack(tokenMetadata).length + TYPE_SIZE + LENGTH_SIZE`). Underfunding causes a confusing "account too small" error mid-transaction.
4. **Revoking to the wrong account**: `spl-token authorize <MINT> mint --disable` revokes; `spl-token authorize <MINT> mint <NEW_PUBKEY>` *transfers* it. Typo a pubkey here and the supply is now controlled by a black-hole address (or an attacker's). Always double-check with `spl-token display <MINT>` afterward.
5. **Metadata URI not pinned**: hosting the JSON on your own server (or an unpinned IPFS gateway) means wallets show a broken token after your server expires. Use Irys/Arweave (permanent) or Shadow Drive (rented but persistent). Never use raw IPFS without a pinning service.
6. **Decimals mismatch**: most fungibles use 9 decimals (matches SOL convention). Some Jupiter routes and UIs assume 6 (USDC convention). Pick deliberately — you cannot change decimals after `InitializeMint`.
7. **Transfer fee extension breaks DEXes**: enabling `TransferFeeConfig` on Token-2022 will break Raydium CLMM and several aggregators. As of 2026-05, only Raydium CPMM, Meteora DLMM, Orca Whirlpools, and Jupiter v6 reliably route fee-on-transfer tokens. Test on devnet before mainnet.

## References

- SPL Token program: https://spl.solana.com/token
- Token-2022 (Token Extensions): https://spl.solana.com/token-2022
- Token-2022 metadata pointer guide: https://solana.com/developers/guides/token-extensions/metadata-pointer
- Metaplex Token Metadata: https://developers.metaplex.com/token-metadata
- Metaplex + Token-2022: https://developers.metaplex.com/token-metadata/token-2022
- `@solana/spl-token` (npm): https://www.npmjs.com/package/@solana/spl-token
- `@solana/spl-token-metadata` (npm): https://www.npmjs.com/package/@solana/spl-token-metadata
- Irys SDK setup: https://docs.irys.xyz/build/d/sdk/setup
- Raydium SDK v2: https://github.com/raydium-io/raydium-sdk-V2
- Meteora DLMM SDK: https://docs.meteora.ag/dlmm/dlmm-sdk
- Orca Whirlpools SDK: https://dev.orca.so/
- Streamflow token lock: https://docs.streamflow.finance/official-streamflow-docs/basics/token-lock

## Example script
See `scripts/launch-token.ts` for a complete end-to-end launch on devnet (mint creation, ATA, supply mint, metadata, optional authority revoke).
