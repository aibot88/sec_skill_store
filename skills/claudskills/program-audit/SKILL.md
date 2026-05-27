---
name: solana-program-audit
description: Use this skill when the user wants to audit a Solana or Anchor program for security vulnerabilities — account validation, PDA safety, arithmetic, CPI risks, reinit attacks, and authority confusion. Includes a checklist and the most common bug classes.
---

# Program Audit

## Overview

Solana programs have a uniquely large attack surface because the runtime gives you no defaults. Every account that flows into an instruction is just bytes plus a pubkey — the program is responsible for verifying ownership, signer-ness, type, and any relational invariant between accounts. There is no `msg.sender`, no per-storage-slot access control, and no automatic type tagging on raw `AccountInfo`s. The result is that the most expensive Solana exploits in history (Wormhole $325M, Mango $114M, Cashio $52M) were not novel cryptography breaks — they were missing one-line checks. Anchor closes most of these gaps via constraints, but only if you use them and understand what they prove.

## When to use this skill

- Pre-mainnet review of a new program or a freshly added instruction.
- Post-incident postmortem — reproducing the bug class and sweeping for siblings.
- PR review where account structs or CPI calls changed.
- Migrating an Anchor program across major versions (e.g. 0.29 → 0.30+) where constraint semantics shifted.
- Reading an unfamiliar program before integrating with it via CPI.

## Prerequisites

Install or have access to:

- **Anchor 0.30+** (`avm install 0.30.1 && avm use 0.30.1`) — required for current constraint syntax including `init_if_needed` feature flag.
- **Rust toolchain pinned to the project's `rust-toolchain.toml`** — audits must build the exact binary.
- **`cargo audit`** (`cargo install cargo-audit`) — flags vulnerable crates in `Cargo.lock`.
- **`cargo geiger`** — surfaces `unsafe` usage in dependencies.
- **Semgrep with Solana rules** — `semgrep --config p/solana` covers the common Sealevel patterns.
- **Sec3 X-ray (free tier)** or **Soteria successor** — static analysis tuned for Solana.
- **Otter Sec tooling** — `cargo-otter` for IDL diffing and program comparison.
- **`solana-verify`** — reproducible build verification against deployed bytecode.
- A copy of [coral-xyz/sealevel-attacks](https://github.com/coral-xyz/sealevel-attacks) cloned locally for reference patterns.

## Workflow

Work top-down. Don't open a single instruction until you've mapped the whole program — most exploits chain across instructions.

1. **Map the program surface.** List every instruction, every account in each instruction's `Accounts` struct, every signer, and every CPI call. A whiteboard or a markdown table is fine. This is the artifact you audit against.
2. **For each instruction, enumerate signer requirements.** Every authority transition, fund movement, or state mutation must have a signer whose pubkey is either (a) stored in an account you trust the ownership of, or (b) a PDA derived from trusted seeds. Wormhole-class bugs live here.
3. **For each account, check ownership.** Anchor's `Account<'info, T>` checks owner automatically. Raw `AccountInfo` / `UncheckedAccount` does not — you must add `#[account(owner = expected_program::ID)]` or check `account.owner` manually. SPL token accounts must be owned by the Token program; mints must be owned by the Token program.
4. **For each PDA, verify the seeds + bump are bound to something trusted.** A PDA proves derivation, not authority. If the seeds include a user-controlled pubkey, the PDA is per-user, not global — make sure the instruction expects that. Always store and re-pass the bump; never re-derive at runtime when you can avoid it.
5. **Identify every CPI.** Confirm the target program ID is constrained (`address = some_program::ID` or explicit pubkey check). Confirm signer seeds passed to `invoke_signed` only authorize what this program legitimately controls. Squads, Mango, and Jupiter integrations are common CPI footguns.
6. **Sweep arithmetic.** Every `+`, `-`, `*`, `/` on a balance, share, price, or fee must be `checked_*` (returns `Option`), `saturating_*` (clamps), or a fixed-point lib like `spl-math` or `fixed`. Mango's $114M loss was a price-impact arithmetic bug. `overflow-checks = true` in `Cargo.toml` is not enough — release builds may strip it; explicit checked ops are required.
7. **Inspect account closing.** Closing means: transfer lamports out + zero data + set discriminator to `CLOSED_ACCOUNT_DISCRIMINATOR` (`[u8; 8]` of `0xff`). Use Anchor's `close = recipient` constraint where possible. A non-zeroed account can be revived inside the same transaction and reused.
8. **Hunt reinit attacks.** Any use of `init_if_needed` is a yellow flag. Verify the post-condition: after the call, all fields hold values the caller is authorized to set, regardless of whether the account is new or existing. Prefer separate `init` and `update` instructions.
9. **Audit randomness.** Slot, blockhash, timestamp, and clock sysvar are all predictable or grindable. Use a VRF (Switchboard, ORAO) or a commit-reveal scheme. There is no safe on-chain randomness primitive in Solana itself.
10. **Run automated tools.** `cargo audit`, `semgrep --config p/solana`, Sec3 X-ray. Treat their output as a starting point, not an answer — most static analyzers miss account-confusion bugs because they're shape-correct.
11. **Manual review of authority transitions.** Owner changes, admin transfers, upgrade authority handoffs, multisig threshold changes. These deserve the most paranoid reading because they are usually one-shot and irreversible.
12. **Verify deployed bytecode.** Run `solana-verify verify-from-repo` against the on-chain program ID. An audit of source that doesn't match deployment is theater.

## Common pitfalls

Each pitfall below shows the vulnerable shape and the fix. Code is Anchor 0.30+.

### 1. Missing signer check (Wormhole class)

The Wormhole bridge lost $325M because it accepted a signature-verification account without verifying that the on-chain instruction actually called the secp256k1 sig-verify precompile in the same transaction. The same class shows up any time a program reads a pubkey from an account and trusts it without checking `is_signer`.

```rust
// VULNERABLE — no signer check on `authority`
#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(mut)]
    pub vault: Account<'info, Vault>,
    /// CHECK: trusted... right?
    pub authority: AccountInfo<'info>,
    #[account(mut)]
    pub recipient: SystemAccount<'info>,
}

pub fn withdraw(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
    require_keys_eq!(ctx.accounts.vault.authority, ctx.accounts.authority.key());
    // attacker passes authority pubkey without signing
    transfer_from_vault(&ctx.accounts, amount)
}
```

```rust
// FIXED — Anchor `Signer<'info>` enforces is_signer at deserialize
#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(mut, has_one = authority)]
    pub vault: Account<'info, Vault>,
    pub authority: Signer<'info>,
    #[account(mut)]
    pub recipient: SystemAccount<'info>,
}
```

### 2. Missing owner check on raw accounts

Anchor `Account<'info, T>` checks owner. `UncheckedAccount` / `AccountInfo` does not. SPL token accounts deserialized via `spl_token::state::Account::unpack` will succeed on any 165-byte buffer — including one written by a malicious program.

```rust
// VULNERABLE
let token_account = spl_token::state::Account::unpack(&ctx.accounts.user_token.data.borrow())?;
// attacker passes a fake account owned by their own program with crafted bytes
```

```rust
// FIXED — explicit owner check, or use Anchor's TokenAccount type
require_keys_eq!(*ctx.accounts.user_token.owner, anchor_spl::token::ID);
let token_account = spl_token::state::Account::unpack(&ctx.accounts.user_token.data.borrow())?;

// Better: use Anchor's typed wrapper which checks owner for you
// pub user_token: Account<'info, TokenAccount>,
```

### 3. Account confusion / type cosplay (Cashio class)

Cashio lost $52M because the program walked a chain of accounts (`crate_collateral_tokens` → `saber_swap.arrow` → mint) but never validated the mint at the root. The attacker forged fake accounts at every level. The fix is to anchor every cross-account relationship to a trusted root — usually a `has_one` constraint or a PDA derivation that includes the trusted pubkey in its seeds.

```rust
// VULNERABLE — no link between vault and the mint it claims to hold
#[derive(Accounts)]
pub struct Deposit<'info> {
    pub vault: Account<'info, Vault>,
    pub collateral_mint: Account<'info, Mint>, // attacker passes any mint
    #[account(mut, token::mint = collateral_mint)]
    pub user_token: Account<'info, TokenAccount>,
}
```

```rust
// FIXED — has_one ties the mint to a value stored on the vault
#[derive(Accounts)]
pub struct Deposit<'info> {
    #[account(has_one = collateral_mint)]
    pub vault: Account<'info, Vault>,
    pub collateral_mint: Account<'info, Mint>,
    #[account(mut, token::mint = collateral_mint)]
    pub user_token: Account<'info, TokenAccount>,
}
```

Anchor also gives every `#[account]` struct an 8-byte discriminator, which prevents passing (say) a `Vault` where a `Config` is expected — but only if you use the typed `Account<'info, T>` wrapper, not raw `AccountInfo`.

### 4. Reinit attack via `init_if_needed`

`init_if_needed` runs `init` if the account is empty, otherwise treats it as existing. Combined with an instruction that lets a user zero an account (via `realloc(0, ..)`, manual lamport drain, or a sloppy close), an attacker can wipe a victim's account and then "reinit" it under their own ownership.

```rust
// VULNERABLE — init_if_needed on a user-keyed account with no signer guard on the existing branch
#[derive(Accounts)]
pub struct OpenOrCreate<'info> {
    #[account(
        init_if_needed,
        payer = user,
        space = 8 + UserPos::INIT_SPACE,
        seeds = [b"pos", user.key().as_ref()],
        bump,
    )]
    pub position: Account<'info, UserPos>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}

pub fn open_or_create(ctx: Context<OpenOrCreate>, owner: Pubkey) -> Result<()> {
    ctx.accounts.position.owner = owner; // overwrites existing owner!
    Ok(())
}
```

```rust
// FIXED — split into init and update, OR guard the "existing" branch
pub fn open_or_create(ctx: Context<OpenOrCreate>, owner: Pubkey) -> Result<()> {
    let pos = &mut ctx.accounts.position;
    // If freshly initialized, `owner` is default Pubkey
    if pos.owner == Pubkey::default() {
        pos.owner = owner;
    } else {
        require_keys_eq!(pos.owner, ctx.accounts.user.key(), ErrorCode::Unauthorized);
        // intentional no-op or scoped update
    }
    Ok(())
}
```

Prefer two instructions (`init_position`, `update_position`) whenever practical.

### 5. Unchecked CPI program ID

Calling into "the token program" via an `AccountInfo` that was never constrained lets an attacker swap in a lookalike program that records the transfer to their own ledger while reporting success.

```rust
// VULNERABLE
pub fn transfer<'info>(
    token_program: AccountInfo<'info>, // not checked!
    from: AccountInfo<'info>,
    to: AccountInfo<'info>,
    authority: AccountInfo<'info>,
    amount: u64,
) -> Result<()> {
    let ix = spl_token::instruction::transfer(token_program.key, from.key, to.key, authority.key, &[], amount)?;
    invoke(&ix, &[from, to, authority, token_program])?;
    Ok(())
}
```

```rust
// FIXED — typed Program<'info, Token> constrains the program ID
#[derive(Accounts)]
pub struct Transfer<'info> {
    #[account(mut)]
    pub from: Account<'info, TokenAccount>,
    #[account(mut)]
    pub to: Account<'info, TokenAccount>,
    pub authority: Signer<'info>,
    pub token_program: Program<'info, Token>, // checks address == spl_token::ID
}
```

### 6. Closed account reuse

Anchor's `close = recipient` constraint zeros the discriminator and drains lamports. Manual close patterns that only drain lamports leave the data intact — and an account with lamports == 0 can be re-funded inside the same transaction (via a CPI) and re-used as if it were live.

```rust
// VULNERABLE — drains lamports but leaves data
pub fn close_position(ctx: Context<ClosePosition>) -> Result<()> {
    let position = &ctx.accounts.position.to_account_info();
    let recipient = &ctx.accounts.recipient.to_account_info();
    **recipient.try_borrow_mut_lamports()? += **position.try_borrow_lamports()?;
    **position.try_borrow_mut_lamports()? = 0;
    Ok(())
}
```

```rust
// FIXED — Anchor close constraint zeros discriminator
#[derive(Accounts)]
pub struct ClosePosition<'info> {
    #[account(mut, close = recipient, has_one = owner)]
    pub position: Account<'info, Position>,
    pub owner: Signer<'info>,
    #[account(mut)]
    pub recipient: SystemAccount<'info>,
}
```

If you must close manually, set the discriminator to `[0xff; 8]` (the closed-account marker) and zero the data before transferring lamports.

### 7. Insecure randomness

```rust
// VULNERABLE — slot is grindable by validators, predictable by anyone
let clock = Clock::get()?;
let winner_idx = (clock.slot % participants.len() as u64) as usize;
```

```rust
// FIXED — use Switchboard or ORAO VRF (commit-reveal also acceptable)
// Caller requests randomness in instruction A, callback in instruction B
let randomness = vrf_account.get_result()?; // [u8; 32]
let winner_idx = (u64::from_le_bytes(randomness[..8].try_into().unwrap()) as usize) % participants.len();
```

### 8. Arithmetic overflow / precision loss (Mango class)

Mango Markets' $114M exploit hinged on manipulating a perp-futures price feed combined with arithmetic that didn't model the resulting position correctly. Even outside that specific bug, plain `a * b / c` on `u64` overflows for moderate prices.

```rust
// VULNERABLE
let value = price * quantity / 1_000_000;
```

```rust
// FIXED — checked + widened intermediate, or fixed-point
let value = (price as u128)
    .checked_mul(quantity as u128).ok_or(ErrorCode::MathOverflow)?
    .checked_div(1_000_000).ok_or(ErrorCode::MathOverflow)?;
let value: u64 = value.try_into().map_err(|_| ErrorCode::MathOverflow)?;
```

### 9. PDA bump not stored or not validated

Re-deriving a bump with `Pubkey::find_program_address` on every instruction is expensive (up to ~1500 CU per try) and lets attackers pass a non-canonical bump if you call `create_program_address` with a user-supplied value.

```rust
// VULNERABLE — accepts any bump the caller provides
#[derive(Accounts)]
#[instruction(bump: u8)]
pub struct Use<'info> {
    #[account(seeds = [b"vault"], bump = bump)] // attacker chooses bump
    pub vault: Account<'info, Vault>,
}
```

```rust
// FIXED — store canonical bump at init, read it back on use
#[account]
pub struct Vault { pub bump: u8, /* ... */ }

#[derive(Accounts)]
pub struct Use<'info> {
    #[account(seeds = [b"vault"], bump = vault.bump)]
    pub vault: Account<'info, Vault>,
}
```

### 10. Missing `mut` constraint

An account that is mutated but not declared `mut` will silently fail at runtime — but the failure mode in older Anchor versions, and in raw Solana, was to allow the read while silently dropping the write. The fix is mechanical but easy to forget on a copy-paste.

```rust
// VULNERABLE
#[derive(Accounts)]
pub struct Increment<'info> {
    pub counter: Account<'info, Counter>, // not mut!
}
```

```rust
// FIXED
#[derive(Accounts)]
pub struct Increment<'info> {
    #[account(mut)]
    pub counter: Account<'info, Counter>,
}
```

## References

- [coral-xyz/sealevel-attacks](https://github.com/coral-xyz/sealevel-attacks) — canonical attack/defense pairs in Anchor.
- [Neodyme — Solana program security](https://workshop.neodyme.io/) — workshop notes and writeups.
- [Helius — A Hitchhiker's Guide to Solana Program Security](https://www.helius.dev/blog/a-hitchhikers-guide-to-solana-program-security)
- [Helius — Solana Hacks, Bugs, and Exploits](https://www.helius.dev/blog/solana-hacks)
- [Sec3 (formerly Soteria)](https://www.sec3.dev/) — static analysis and audit firm.
- [Otter Sec](https://osec.io/) — audit firm; tooling on GitHub at `otter-sec`.
- [Anchor account constraints reference](https://www.anchor-lang.com/docs/references/account-constraints)
- [Zealynx Solana Security Checklist (45 checks)](https://www.zealynx.io/blogs/solana-security-checklist)
- [Cantina — Securing Solana: A Developer's Guide](https://cantina.xyz/blog/securing-solana-a-developers-guide)
- [Halborn — Cashio Hack writeup](https://www.halborn.com/blog/post/explained-the-cashio-hack-march-2022)
- [RareSkills — init_if_needed and the Reinitialization Attack](https://rareskills.io/post/init-if-needed-anchor)

## Detailed checklist

See `references/vulnerability-checklist.md` for the comprehensive audit checklist and `references/anchor-constraints-cheatsheet.md` for an Anchor `#[account(...)]` constraint reference.
