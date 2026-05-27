---
name: sui-zk-login
description: Add Sui zkLogin for Google, Apple, Facebook, or Twitch sign-in. Use when the user mentions zkLogin, social login, or OAuth-based Sui auth.
---

## Preamble (run first)

```bash
# Suiperpower telemetry. Routes through the CLI so projects.json + Convex stay in sync.
# Silent on failure so the skill never blocks. Opt out: SUIPERPOWER_TELEMETRY=off.
#
# AGENT NOTE: when this skill finishes, run the matching completion command:
#   suiperpower track sui-zk-login build completed
# Or use "failed" / "aborted" if it ended that way.
command -v suiperpower >/dev/null 2>&1 && suiperpower track sui-zk-login build started >/dev/null 2>&1 &
true
```

If `TEL_PROMPTED` is `no`, before doing real work, ask the user:

> Help suiperpower get better. We track which skills get used and how long they take. No code, no file paths, no PII. Change anytime in `~/.suiperpower/config.json`.
>
> A) Sure, anonymous
> B) No thanks

Write the answer to `~/.suiperpower/config.json` `telemetryTier` field and create `~/.suiperpower/.telemetry-prompted`. Then continue.

## What this skill does

Adds end-to-end zkLogin to a Sui app. Walks through OAuth provider registration, ephemeral keypair generation, JWT capture, ZK proof retrieval from a prover service, transaction signing, and salt management. Refuses to ship if the demo is a stub; a real OAuth flow must complete and a real transaction must execute under the resulting Sui address.

## When to use it

- The user wants users to sign in with Google, Apple, Facebook, Twitch, Slack, Kakao, or Microsoft instead of a wallet seed phrase.
- The user is building consumer-facing Sui apps where wallet friction kills onboarding.
- The user wants a passwordless Sui address tied to an OAuth identity.

Supported providers (SDK v2): Google, Apple, Facebook, Twitch, AWS (tenant-based), Karrier One, Credenza3 (all networks). Slack, Kakao, Microsoft are devnet only.

## When NOT to use it

- For wallet-first power-user flows, the standard Sui wallet integration is simpler.
- If the user has not picked a project yet, use `find-next-sui-idea` first.
- If the user has not scaffolded a project, use `scaffold-project` first.
- For sponsored gas alone (without OAuth login), use `sponsored-transactions` instead.

If you activated this and the user actually wants something else, consult `skills/SKILL_ROUTER.md` and hand off.

## Inputs

- A Sui project with a frontend (zkLogin is browser-side; pure backend zkLogin is unusual).
- Optional: `.suiperpower/build-context.md`. Read it if present.
- The chosen OAuth provider(s) and the redirect URLs for the app.

If unclear, interview the user for:

- Which provider(s) does the target audience use? Google is the safest first pick.
- What is the salt management plan? Self-hosted salt service, Mysten Salt service (`https://salt.api.mystenlabs.com/get_salt`), or per-user-derived salt?
- Mainnet, testnet, or both?
- What is the prover service? Mysten's (`https://prover-dev.mystenlabs.com/v1` for devnet/testnet), self-hosted, or a third-party?
- For production, consider Enoki (Mysten's managed zkLogin service) which handles key management, salt, and proving.

## Outputs

- OAuth provider config (client id, redirect URIs, allowed scopes).
- Frontend zkLogin flow: ephemeral keypair generation, login URL builder, JWT decode, salt fetch, ZK proof fetch, address derivation, transaction signer.
- A live demo: real Google (or chosen provider) login, real Sui address derived, real transaction executed.
- Append to `.suiperpower/build-context.md`:

  ```markdown
  ## sui-zk-login session, <timestamp>
  - provider(s): <list>
  - sample sui address: <0x...>
  - first executed tx digest: <digest>
  - salt service: <self-hosted | Mysten | derived>
  - prover service: <url>
  - open issues: <list>
  ```

The skill never deletes files outside the integration source path without explicit user confirmation.

## Workflow

1. **Context gathering**
   - Read `.suiperpower/build-context.md` if it exists.
   - Confirm provider(s) and redirect URIs.

2. **OAuth registration**
   - Walk the user through registering an OAuth client with each provider.
   - Capture client id and redirect URIs. Document allowed scopes (typically just `openid`).

3. **Ephemeral keypair**
   - Generate an Ed25519 keypair in the browser. Persist in `sessionStorage` with a max validity (a few epochs).
   - Compute the nonce from the ephemeral public key, max epoch, and randomness.

4. **OAuth flow**
   - Build the provider's login URL with the nonce.
   - Redirect the user to the provider, capture the JWT on return.
   - Decode the JWT and verify it locally.

5. **Salt service**
   - Resolve the user's salt. Options: self-hosted salt service, Mysten Salt, deterministic derivation (less private).
   - Document the choice. Salt determines the user's Sui address.

6. **ZK proof**
   - Submit JWT, salt, and ephemeral public key to the prover service. Capture the proof.
   - Cache the proof in `sessionStorage` (proofs are valid until the JWT expires or the max epoch passes).

7. **Address derivation**
   - Derive the user's Sui address from the JWT, salt, and proof.
   - `jwtToAddress(jwt, salt, legacyAddress?)` accepts an optional third boolean. It defaults to `false`. Pass `true` only for backward compatibility with addresses derived under SDK v1.
   - Display the address to the user (truncated form fine).

8. **Sign and execute**
   - Sign a transaction using the ephemeral key plus zkLogin signature.
   - Execute. Capture the digest.

9. **Demo gate**
   - Do not declare done until a real OAuth login completes and a real transaction executes under the derived address.

10. **Writeback**
    - Append session details to `.suiperpower/build-context.md`.

11. **Closing handoff**
    - If `.suiperpower/intent.md` exists and the session was non-trivial (new zkLogin integration, salt service decision, provider list, real signed transaction), recommend `verify-against-intent` as the next step so the auth surface and key-custody choices are checked before shipping.
    - If no `intent.md` exists and the session was non-trivial, surface that gap once: offer `clarify-intent` to backfill, do not force it.

## Production deployment options

The manual flow above gives full control but requires running your own salt service, prover, and key management. For production, consider these managed services:

| Service | What it handles | Docs |
|---|---|---|
| **Enoki** (Mysten Labs) | Managed zkLogin: salt, proving, ephemeral key management, sponsored transactions. Drop-in SDK. | https://docs.enoki.mystenlabs.com |
| **Shinami** (third-party) | zkLogin API, gas station (sponsored txs), Node Service (RPC). Single vendor for auth + gas + infra. | https://docs.shinami.com |

Both remove the need to self-host a prover and salt service. Evaluate based on custody requirements, cost, and vendor preference. The manual flow remains the right choice when you need full control over key material and salt storage.

## Quality gate (anti-slop)

Before reporting done, the skill asks itself the following and refuses to declare success if any answer is no:

- Did the user complete a real OAuth login (not a stubbed JWT) end to end?
- Did a transaction actually execute under the derived Sui address, with a recorded digest?
- Is the salt service decision documented, with an honest note about its privacy and recovery tradeoffs?
- Is the ephemeral keypair scoped to a finite max epoch, not "forever"?
- Is JWT decoding done with verification, not blind trust of the payload?
- Does the integration handle expired ZK proofs by triggering a re-prove rather than silently failing?

If any answer is no, the skill reports the gap and works through it before claiming the integration is complete.

## References

On-demand references (load when relevant to the user's question):

- `references/zklogin-flow.md`: End-to-end flow with code for ephemeral keypair, nonce, JWT capture, and signing.
- `references/zklogin-salt.md`: Salt management options, tradeoffs, and recovery implications.
- `references/zklogin-pitfalls.md`: Expiry, redirect mismatches, prover errors, address derivation gotchas.

Knowledge docs (load when scope expands beyond what is in references):

- `skills/data/sui-knowledge/04-protocols-and-sdks.md`: SDK ecosystem context.

## Use in your agent

- Claude Code: `claude "/suiper:sui-zk-login <your message>"`
- Codex: `codex "/sui-zk-login <your message>"`
- Cursor: paste a chat message that includes a phrase like "add zkLogin", or load `~/.cursor/rules/sui-zk-login.mdc` and reference it.

If you activated this and the user actually wants something else, consult `skills/SKILL_ROUTER.md` and hand off.
