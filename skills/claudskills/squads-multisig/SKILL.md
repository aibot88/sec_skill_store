---
name: solana-squads-multisig
description: Use this skill when the user wants to set up a Squads V4 multisig on Solana — create the multisig, manage members and threshold, propose transactions, approve, and execute. Standard for team treasuries and program upgrade authority.
---

# Squads V4 Multisig

## Overview

Squads is the dominant Solana multisig — the Solana ecosystem's equivalent of Gnosis Safe. The V4 protocol (program ID `SQDS4ep65T869zMMBKyuUq6aD6EgTu8psMjkvj52pCf` on mainnet-beta and devnet) is what real teams use today to secure program upgrade authority, custody team treasuries, hold large LP positions, and run on-chain DAO operations. The TypeScript SDK (`@sqds/multisig`) exposes three flavors of every action — `multisig.instructions.*` (returns an Ix you compose yourself), `multisig.transactions.*` (returns a signed `VersionedTransaction`), and `multisig.rpc.*` (builds, sends, and returns a signature). Most automation should target `multisig.rpc.*` on the backend and `multisig.instructions.*` from a wallet adapter frontend.

## When to use this skill

Trigger this skill when the user wants to:

- Move a program's `upgrade_authority` off a single keypair onto a multisig (the #1 production use case — single-key upgrade authority is the most common source of catastrophic Solana program compromises)
- Set up a 2-of-3, 3-of-5, etc. team treasury for a startup, DAO, or fund
- Custody LP positions, vesting contracts, or token mint authority behind multiple signers
- Programmatically propose / approve / execute multisig transactions from a backend
- Migrate from the Squads webapp UI to scripted operations, or vice versa
- Rotate / add / remove multisig members

If the user wants a single-sig hot wallet, an SPL token mint, or a generic Solana transaction, this is the wrong skill.

## Prerequisites

Pin these. The Squads program has been stable, but the SDK and `@solana/web3.js` v1 vs v2 split means version mismatches cause cryptic runtime errors.

```json
{
  "engines": { "node": ">=20" },
  "dependencies": {
    "@sqds/multisig": "2.1.4",
    "@solana/web3.js": "^1.95.0"
  },
  "devDependencies": {
    "typescript": "^5.4.0",
    "ts-node": "^10.9.0",
    "@types/node": "^20.0.0"
  }
}
```

Notes:

- `@sqds/multisig` 2.1.4 (latest as of May 2026) targets `@solana/web3.js` v1. Do NOT use `@solana/web3.js` v2 (kit) with this SDK — wrong types, wrong `Connection`, wrong `Keypair`.
- A funded keypair on the target cluster. For devnet, `solana airdrop 2` is usually enough for a full create + propose + execute cycle.
- An RPC endpoint. Public devnet (`https://api.devnet.solana.com`) is fine for testing; for mainnet use Helius / Triton / QuickNode.

## Workflow

### 1. Core concepts (memorize these — most bugs come from confusing them)

A Squads multisig has **four distinct PDAs** you will derive:

| PDA | What it is | When you need it |
|---|---|---|
| **Multisig account** (`multisigPda`) | The on-chain account that stores members, threshold, transaction index. Derived from a one-time random `createKey`. | Every call. This is "the multisig." |
| **Vault PDA** (`vaultPda`, by `index`) | The actual signer that holds funds and signs CPIs. **One multisig has many vaults** (index 0, 1, 2, ...). Index 0 is the default. | Funding, sending from the treasury, setting as program upgrade authority. |
| **Transaction PDA** | Holds a proposed transaction's message. | Internal — derived per `transactionIndex`. |
| **Proposal PDA** | Tracks votes (approve / reject / cancel). One per transaction index. | When approving or executing. |

The vault PDA is what you put funds into and what becomes the program upgrade authority — **never the multisig account itself**.

### 2. Create the multisig

`multisig.rpc.multisigCreateV2()` takes:

- `createKey` — a one-time `Keypair` whose pubkey seeds the `multisigPda`. Discard after; not used to sign anything later.
- `creator` — the `Keypair` paying for the create transaction.
- `members[]` — array of `{ key: PublicKey, permissions: Permissions }`. Permissions are bitfields built from `Permission.Initiate | Permission.Vote | Permission.Execute`. Use `Permissions.all()` for full power.
- `threshold` — minimum approvals required (e.g. 2 for 2-of-3).
- `configAuthority` — `null` for an **autonomous** multisig (governs itself via configTransaction); set to a pubkey for a **controlled** multisig where that authority can unilaterally change membership. Most teams want `null`.
- `timeLock` — seconds between approval-reaching-threshold and execution. 0 for none. Use a real timelock (1–24h) for program upgrade authority multisigs.
- `rentCollector` — `null` is fine; set to recover rent from closed transaction accounts.
- `treasury` — the `treasury` field from `ProgramConfig` account; the create-fee goes here.

### 3. Find the vault PDA

```ts
const [vaultPda] = multisig.getVaultPda({ multisigPda, index: 0 });
```

Index 0 is the default vault every multisig has. You can derive vault 1, 2, ... and use them as separate sub-treasuries under the same governance.

### 4. Fund the vault

A vault is a normal PDA from the multisig's perspective — send SOL or SPL tokens to `vaultPda` like any other address. It will not show up in `getMultisigInfo`; check it with `connection.getBalance(vaultPda)`.

### 5. Create a vault transaction

A "vault transaction" is a proposed CPI bundle the vault will sign. You build a `TransactionMessage` whose `payerKey` is the **vault PDA** (not your wallet), with the instructions you want the vault to execute.

```ts
const transferMessage = new TransactionMessage({
  payerKey: vaultPda,
  recentBlockhash: (await connection.getLatestBlockhash()).blockhash,
  instructions: [SystemProgram.transfer({ fromPubkey: vaultPda, toPubkey: dest, lamports })],
});

const newIndex = BigInt(Number(multisigInfo.transactionIndex) + 1);

await multisig.rpc.vaultTransactionCreate({
  connection, feePayer: proposer, multisigPda,
  transactionIndex: newIndex,
  creator: proposer.publicKey,
  vaultIndex: 0,
  ephemeralSigners: 0,
  transactionMessage: transferMessage,
  memo: "Transfer 0.01 SOL",
});
```

### 6. Create the proposal (separate step!)

`vaultTransactionCreate` only stores the message — members can't vote yet. You must call `proposalCreate` at the same `transactionIndex`:

```ts
await multisig.rpc.proposalCreate({ connection, feePayer, multisigPda, transactionIndex: newIndex, creator });
```

Pass `isDraft: true` if you're building a batch and want to add more before activating.

### 7. Approve from each member

Each member with `Permission.Vote` calls `proposalApprove` with their own `Keypair`. The proposal moves to `Approved` state when threshold is reached:

```ts
await multisig.rpc.proposalApprove({ connection, feePayer, multisigPda, transactionIndex: newIndex, member: memberKeypair });
```

### 8. Execute

Any member with `Permission.Execute` can fire it once `Approved`:

```ts
await multisig.rpc.vaultTransactionExecute({
  connection, feePayer: executor, multisigPda,
  transactionIndex: newIndex,
  member: executor.publicKey,
  signers: [executor],
  sendOptions: { skipPreflight: true },
});
```

`skipPreflight: true` is often needed — Squads' CPIs can confuse the simulator into reporting false errors. Confirm the on-chain signature for ground truth.

### 9. Squads webapp (squads.so) vs SDK

Use the **webapp** (`https://v4.squads.so`) when:

- You want a multisig for humans clicking buttons (treasury, DAO ops).
- You need to import existing token accounts visually.
- The signers are using hardware wallets — the webapp's wallet-adapter integration is way better than rolling your own.

Use the **SDK** when:

- You're automating proposal creation from a backend (e.g. scheduled treasury payouts, programmatic vesting unlocks).
- You're integrating multisig flows into your own product UI.
- You need to do batch operations the UI doesn't support (e.g. add 200 members programmatically — pragmatically you wouldn't, but the SDK lets you).

A multisig created via SDK is fully visible / usable in the webapp and vice versa — they're the same on-chain program.

### 10. Best practice: program upgrade authority

The single highest-leverage thing this skill enables. After deploying a program:

1. Create a multisig with at least 3 members, threshold ≥ 2, `timeLock` ≥ 86400 (24h).
2. Derive vault 0.
3. `solana program set-upgrade-authority <PROGRAM_ID> --new-upgrade-authority <VAULT_PDA>`.
4. From then on, every `program deploy` must be proposed as a `BPFLoaderUpgradeable.upgrade` instruction inside a vault transaction, approved, wait out the timelock, then executed.

The timelock means a single compromised key can't push a malicious upgrade in the time it takes to alert your team.

### 11. Best practice: changing membership

Changing members, threshold, or `configAuthority` is **not** a `vaultTransactionCreate` — it's a `configTransactionCreate`. Different PDA, different instruction, different proposal type. Common mistakes:

- Trying to add a member by encoding the SDK's `addMember` instruction inside a vault transaction. Won't work — the multisig account is only writable to itself via `configTransaction`.
- For controlled multisigs (`configAuthority` is set), the config authority can change membership directly without a vote. For autonomous multisigs (the default), member changes require the same threshold vote as any other action.

Always rotate one member at a time and verify the on-chain state between rotations.

## Common pitfalls

1. **Confusing the multisig account with the vault PDA.** The multisig account holds the *governance state* (members, threshold). The vault PDA holds the *money*. They are different addresses. Funding the multisig account does nothing useful. Setting the multisig account as program upgrade authority makes the program unupgradeable. Always use `getVaultPda({ multisigPda, index: 0 })` for anything involving value.

2. **Forgetting that `proposalCreate` is a separate call after `vaultTransactionCreate`.** The SDK splits them so you can build batches as drafts. If you skip `proposalCreate`, no one can vote and you'll get cryptic "proposal not found" errors at the approve step.

3. **Vault index confusion.** Almost every multisig only ever uses index 0. If you're seeing "vault balance is 0" but you funded the vault, you probably funded vault 0 but built the transaction message against vault 1 (or vice versa). The `vaultIndex` passed to `vaultTransactionCreate` MUST match the index used to derive the `payerKey` of the `TransactionMessage`.

4. **Approving before the proposal is in `Active` state.** Plain `proposalCreate` puts the proposal directly into `Active`. But `proposalCreate({ isDraft: true })` (used for batches) leaves it as `Draft` — you must call `proposalActivate` before any approve will succeed. Symptom: `InvalidProposalStatus` error.

5. **Changing members via vaultTransaction instead of configTransaction.** Member / threshold / config-authority changes require `configTransactionCreate` + `configTransactionExecute` — a completely separate flow from value-moving vault transactions. The instructions live under `multisig.rpc.configTransaction*`. See `docs.squads.so/main/development/typescript/instructions/controlled-multisig-instructions`.

6. **Reusing `createKey` keypairs across multisigs.** `createKey` seeds the `multisigPda`. If you accidentally reuse the same `createKey.publicKey`, the second `multisigCreateV2` will fail with "account already exists." Always generate a fresh `Keypair` per multisig.

7. **Reusing member keys across multiple multisigs without rotation.** Each member's signing key is a single point of failure across every multisig it sits on. If wallet X is on 5 multisigs and gets compromised, all 5 are at the threshold-minus-one. Best practice: dedicated hardware-wallet keys per multisig, or at minimum per security domain (treasury vs. upgrade-authority).

8. **`@solana/web3.js` v2 incompatibility.** `@sqds/multisig` 2.1.4 is built against web3.js v1. If your project upgraded to web3.js v2 / kit, you'll get TypeScript errors about `Keypair` and `Connection` types not matching. Either pin web3.js v1 for the multisig surface or wait for an SDK v3.

9. **Treasury vs rentCollector confusion.** `treasury` (required) is the program's fee recipient — set it from `ProgramConfig.treasury`, not your own wallet. `rentCollector` (optional, can be `null`) is where rent flows when transaction accounts close — set it to your multisig vault if you want to recover that rent.

10. **Stale transaction index.** Multisigs track a monotonically incrementing `transactionIndex`. Always read it from `Multisig.fromAccountAddress(...).transactionIndex`, add 1, pass as `BigInt`. Hardcoding `1n` only works for the very first transaction.

## References

- Squads docs: https://docs.squads.so/main/development/typescript/overview
- Squads V4 program source: https://github.com/Squads-Protocol/v4
- Reference TypeScript examples: https://github.com/Squads-Protocol/v4-examples
- TypeDoc API: https://typedoc.squads.so/
- Webapp (mainnet + devnet): https://v4.squads.so
- npm package: https://www.npmjs.com/package/@sqds/multisig (latest 2.1.4)
- Program ID (mainnet + devnet): `SQDS4ep65T869zMMBKyuUq6aD6EgTu8psMjkvj52pCf`

## Example scripts

See `scripts/create-multisig.ts` and `scripts/propose-and-execute.ts`. Both run against devnet out of the box.

```bash
# Setup
npm init -y
npm i @sqds/multisig@2.1.4 @solana/web3.js@^1.95.0
npm i -D typescript ts-node @types/node

# 1. Create the multisig and fund vault 0
npx ts-node scripts/create-multisig.ts

# Copy the printed `MULTISIG_PDA` and paste it into propose-and-execute.ts
# (or set it via env var — see the script).

# 2. Run the full propose -> approve x2 -> execute flow
npx ts-node scripts/propose-and-execute.ts
```
