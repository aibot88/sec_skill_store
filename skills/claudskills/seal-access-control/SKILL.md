---
name: seal-access-control
description: Integrate Seal threshold encryption and access control on Sui. Use when the user mentions Seal.
---

## Preamble (run first)

```bash
# Suiperpower telemetry. Routes through the CLI so projects.json + Convex stay in sync.
# Silent on failure so the skill never blocks. Opt out: SUIPERPOWER_TELEMETRY=off.
#
# AGENT NOTE: when this skill finishes, run the matching completion command:
#   suiperpower track seal-access-control build completed
# Or use "failed" / "aborted" if it ended that way.
command -v suiperpower >/dev/null 2>&1 && suiperpower track seal-access-control build started >/dev/null 2>&1 &
true
```

If `TEL_PROMPTED` is `no`, before doing real work, ask the user:

> Help suiperpower get better. We track which skills get used and how long they take. No code, no file paths, no PII. Change anytime in `~/.suiperpower/config.json`.
>
> A) Sure, anonymous
> B) No thanks

Write the answer to `~/.suiperpower/config.json` `telemetryTier` field and create `~/.suiperpower/.telemetry-prompted`. Then continue.

## What this skill does

Integrates Seal into a Sui project so the user can encrypt data client-side and control decryption through Move access policies on chain. Picks the right access pattern (allowlist, subscription, token-gate, time-lock, etc.), writes the Move policy module with `seal_approve` functions, wires up the `@mysten/seal` TS SDK for encrypt and decrypt, and verifies a real round-trip before declaring done.

## When to use it

- The project needs access-controlled encryption tied to on-chain state (NFT gate, allowlist, subscription, DAO vote).
- The user wants to encrypt Walrus blobs so only authorized users can decrypt.
- The user needs time-locked encryption (content becomes public after a deadline).
- The user is building gated content, encrypted NFTs, secret ballots, or private user data.

## When NOT to use it

- If the user has not picked a project yet, use `find-next-sui-idea` first.
- If the user has not scaffolded a project, use `scaffold-project` first.
- If the user only needs Walrus storage without encryption, use `walrus-storage` instead.
- If the user wants simple single-user AES encryption with a user-held key, that does not need Seal. Point them to standard AES-GCM and skip this skill.
- If the user wants to write raw Move without encryption, use `build-with-move`.

If you activated this and the user actually wants something else, consult `skills/SKILL_ROUTER.md` and hand off.

## Inputs

- A Sui project (Move package and/or TS frontend).
- Optional: `.suiperpower/build-context.md` from `scaffold-project`. Read it if present.
- The access control requirement: who should be able to decrypt and under what conditions.

If unclear, interview the user for:

- What data is being encrypted? (blobs, messages, documents, NFT content)
- Who should be able to decrypt? (specific addresses, NFT holders, paid subscribers, anyone after a date)
- Will encrypted data live on Walrus or elsewhere?
- Is there an existing Move package to extend, or start fresh?

## Outputs

- A Move module with one or more `seal_approve` entry functions implementing the access policy.
- TS integration code using `@mysten/seal` for encrypt and decrypt flows.
- A working SessionKey flow with personal message signing.
- Optional: Walrus integration for storing encrypted blobs (uses `walrus-storage` patterns).
- Append to `.suiperpower/build-context.md`:

  ```markdown
  ## seal-access-control session, <timestamp>
  - pattern: <whitelist | subscription | account_based | private_data | tle | voting | key_request>
  - policy module: <module::name>
  - seal_approve functions: <names>
  - package id (testnet): <id or pending>
  - walrus integration: <yes | no>
  - open issues: <list>
  ```

## Workflow

1. **Context gathering**
   - Read `.suiperpower/build-context.md` if it exists.
   - Confirm the user's access control requirement and who should decrypt.
   - Check if the project already has Move modules or a TS frontend.

2. **Pick the access pattern**
   - Use the decision table below. Confirm the choice with the user before writing code.
   - If none of the standard patterns fit, compose from multiple or write a custom `seal_approve` function.

3. **Write the Move policy module**
   - Implement `seal_approve` entry functions following the Seal convention (see `references/seal-patterns.md`).
   - Every `seal_approve` function: name starts with `seal_approve`, first param is `id: vector<u8>`, must not modify state.
   - Add admin functions if the pattern requires setup (e.g., allowlist add/remove, subscription creation).
   - Write at least one Move test that verifies the policy grants and denies correctly.

4. **Integrate the TS SDK**
   - Install `@mysten/seal` and `@mysten/sui`.
   - Initialize `SealClient` with testnet key server config (see `references/seal-quickstart.md`).
   - Wire the encrypt flow: build identity from policy object + nonce, call `client.encrypt()`.
   - Wire the decrypt flow: create `SessionKey`, get personal message signature from wallet, build `seal_approve` PTB, call `client.decrypt()`.

5. **Walrus integration (if applicable)**
   - Encrypt data via Seal, upload ciphertext to Walrus, store `blobId` on chain.
   - On retrieval: fetch ciphertext from Walrus, decrypt via Seal after policy check.
   - See `walrus-storage` skill and `references/seal-quickstart.md` for the canonical pattern.

6. **Test the round-trip**
   - Encrypt real data, store it (Walrus or local), decrypt with an authorized identity.
   - Verify the decrypted bytes match the original plaintext.
   - Test denial: attempt decryption with an unauthorized identity and confirm it fails.

7. **Writeback**
   - Append session details to `.suiperpower/build-context.md`.

8. **Closing handoff**
   - If `.suiperpower/intent.md` exists and the session was non-trivial (new module, new sponsor integration, or material changes to public functions), recommend `verify-against-intent` as the next step so drift is caught before shipping.
   - If no `intent.md` exists and the session was non-trivial, surface that gap once: offer `clarify-intent` to backfill, do not force it.

## Decision table: which pattern to pick

| Use case | Pattern | Module |
|---|---|---|
| Admin controls who can decrypt | `whitelist` | Admin-managed address allowlist |
| Paid, time-limited access | `subscription` | Fee + TTL, auto-expires |
| Encrypt to a specific address | `account_based` | Only that address decrypts |
| Creator-only private data | `private_data` | Only the object creator decrypts |
| Content unlocks after a date | `tle` (time-lock) | Anyone decrypts after timestamp |
| Secret ballot / sealed-bid auction | `voting` | Threshold decryption after vote closes |
| Delegated access via witness | `key_request` | Third party grants access on behalf |

If the user's requirement spans two patterns (e.g., allowlist that expires), compose them in a single module. The `seal_approve` convention is flexible enough for custom logic.

## Quality gate (anti-slop)

Before reporting done, the skill asks itself the following and refuses to declare success if any answer is no:

- Does the Move policy module compile with `sui move build`?
- Does every `seal_approve` function follow the convention (name prefix, `id: vector<u8>` first param, no state mutation)?
- Did the round-trip test actually encrypt, store, retrieve, and decrypt real data?
- Was denial tested (unauthorized identity fails to decrypt)?
- Is `verifyKeyServers` documented as `false` for dev and `true` for production?
- If Walrus is involved, does the ciphertext actually live on Walrus, not just in local memory?
- Is SessionKey TTL explicitly set, not silently defaulted?

If any answer is no, the skill reports the gap and works through it before claiming the integration is complete.

## References

On-demand references (load when relevant to the user's question):

- `references/seal-quickstart.md`: SealClient init, encrypt, decrypt, SessionKey, Walrus integration recipes.
- `references/seal-patterns.md`: All 7 Move access patterns with `seal_approve` function signatures and when to use each.
- `references/seal-pitfalls.md`: Common mistakes with Seal integration and how to avoid them.

Knowledge docs (load when scope expands beyond what is in references):

- `skills/data/sui-knowledge/sponsor-docs/walrus.md`: Walrus concepts and integration for encrypted blob storage.

External docs (fetch at runtime for the latest API surface):

- Seal SDK: https://sdk.mystenlabs.com/seal
- Seal repo and examples: https://github.com/MystenLabs/seal
- Seal blog post: https://blog.sui.io/seal-programmable-access-control/

## Use in your agent

- Claude Code: `claude "/suiper:seal-access-control <your message>"`
- Codex: `codex "/seal-access-control <your message>"`
- Cursor: paste a chat message that includes a phrase like "encrypt with Seal" or "gated content", or load `~/.cursor/rules/seal-access-control.mdc` and reference it.

If you activated this and the user actually wants something else, consult `skills/SKILL_ROUTER.md` and hand off.
