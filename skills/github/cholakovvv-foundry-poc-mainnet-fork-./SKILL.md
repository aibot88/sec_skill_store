---
name: foundry-poc-mainnet-fork
description: Use this skill when the user wants to write a Foundry Proof of Concept (PoC) test that reproduces a smart contract vulnerability against a real deployed protocol on a mainnet fork. Triggers include phrases like "write a PoC", "reproduce this bug with Foundry", "fork mainnet and exploit", "validate this finding on-chain", or when the user provides a vulnerability report alongside deployed contract addresses. This skill is strictly for mainnet-forked, real-contract, end-to-end reproductions on EVM chains. Do NOT use for Hardhat tests, local-state PoCs, fuzz or invariant harnesses against mocks, or non-EVM chains (Solana, Cosmos, Move).
---

# Foundry PoC on Mainnet Fork

## Purpose

Produce one Foundry test file that reproduces a real smart contract vulnerability against real deployed contracts on a forked EVM network. The test must pass, and its passing must prove the vulnerability end-to-end: from the action that first triggers the vulnerable state, through every on-chain step in between, to the final realized impact.

## Reading Order (Mandatory)

Before reading anything else in the repository, read the finding description to completion. Only after the finding is fully read should other files be consulted. In particular:

- Do not read any file in the target PoC directory (typically `test/poc/`) until the finding is classified and the causal chain is written out (see Procedure).
- If a file with the planned output name already exists in the repo, treat it as untrusted until the skill's own classification is complete. Stale or prior-session PoC files may encode causal-chain choices that violate the skill's rules. Do not anchor on them.
- Reference tests for style matching (imports, inheritance, helpers) are read in step 6 of the procedure, not before. Even then, imitate their surface style only. Never imitate their fork-block choice, starting actor, or causal-chain structure without independently verifying those match the current finding's classification.

The order in which files are read shapes Claude's reasoning. Reading an existing PoC before classifying the finding anchors output to that PoC's structure and overrides the skill's rules in practice. Reading the finding first is not optional.

## Required Inputs

Before writing any code, confirm the user has provided:

1. Vulnerability description: root cause, attack path, impact. If the description is short or summary-level, ask for the full finding.
2. Chain: ethereum, arbitrum, base, optimism, polygon, bnb, avalanche, or chain ID.
3. Fork target: `latest`, a specific block number, or a timestamp (if timestamp, ask the user to convert it to a block number, do not guess).
4. Real deployed addresses for every contract in the attack path, labeled by role.

Optional but improves output quality:

5. RPC URL (otherwise use a public default and state which one was used). For pinned block numbers, the RPC must have historical state for that block. Public RPCs like publicnode often lack archive data; drpc.org, mevblocker.io, and eth-pokt.nodies.app retain broader history. If a chosen RPC returns "historical state not available", try a different public endpoint before asking the user for an archive-enabled RPC.
6. Path to the repo's existing test files for style matching.
7. Severity (proceed for High, Medium, Critical; for Low or Info, warn the user that a PoC may not be warranted and confirm before proceeding).

If any of 1, 2, 3, or 4 is missing, stop and ask. Do not guess addresses. Do not assume "mainnet" means Ethereum if the protocol could be on another chain. Do not fabricate a fork block.

## Hard Rules

### Rule 1: Foundry Only

Foundry is the only acceptable framework. If the target repo uses Hardhat, Truffle, or anything else, the PoC is still written in Foundry as a standalone file.

### Rule 2: Real Contracts Only

Every contract the test interacts with must be a real deployed address, bound at the top of the file as a `constant`. Specifically:

- No mock contracts.
- No minimal reimplementations of protocol contracts.
- No stubbed interfaces that diverge from the deployed bytecode.
- Interfaces written in the test file must contain only the function signatures actually called, and those signatures must match the deployed contract exactly.

If a contract required by the attack path is not deployed on the target chain, stop. Do not fabricate a workaround. State the blocker to the user.

Addresses for test-only actors (attacker EOA, recipient) created via `makeAddr` are acceptable and expected. Addresses for protocol contracts, tokens, oracles, governance, and admins must be real.

### Rule 3: Fork Is Mandatory

The first statement inside `setUp()` must be `vm.createSelectFork(...)`. The fork uses the RPC for the correct chain and either the user-specified block or `latest`. State is read from the fork, not constructed locally.

### Rule 4: End-to-End Execution

The test must execute the full vulnerability path from the action that first triggers the vulnerable state to the final realized impact. This is as important as forking mainnet.

**Classify before writing.** Every finding falls into one of three categories, and the category determines where the test starts:

- (a) **Frozen historical impact**: a one-time bad state that already exists on-chain, reached by a past action that cannot be re-executed (block-number progression, a past governance vote, an already-completed migration). Severity comes entirely from the existing frozen state, with no further damage accruing. Forking at the post-vulnerable state is the correct starting point.
- (b) **Forward-looking risk**: the vulnerable state is a pattern that will continue producing new instances as normal protocol operations run. Severity comes from what happens to actors not yet affected. The PoC must reproduce the chain that produces a _new_ instance of the vulnerable state, starting from an actor currently in the safe state. Replaying a past instance is insufficient.
- (a+b) **Both**: some value is already affected and more will be as normal operations continue. The primary test reproduces the forward-looking chain (b). A secondary assertion can reference existing impacted value (a) as additional evidence, but the bulk of the PoC is the (b) chain.

Before writing any code, state the classification out loud in the response to the user: "This finding is category (a)/(b)/(a+b) because [signal]. I will start the test from [actor X] at [fork block Y] where X is still in the safe state and perform [step 1, step 2, ...]."

This statement is mandatory. A PoC that is written without stating the classification first is a rule violation, even if the resulting code is otherwise correct.

**Signals for (b):** phrases like "currently at risk", "will freeze", "any X that does Y", "N actors vulnerable", tables of live protocol entities with counts of affected vs unaffected, references to patterns that repeat on protocol schedule, language about "future" or "new" actors. When any of these appear, default to (b) or (a+b) unless the finding explicitly says the pattern has been patched.

**Identify the first-triggering action.** The first action is not always an attacker call. It may be:

- A malicious actor's on-chain call.
- A normal user action (deposit, withdraw, redeem, rebalance) that happens to put the protocol in a vulnerable state.
- A protocol operation (keeper bot, liquidation, debt reporting, oracle update) that runs on a schedule.
- A governance action or privileged role call.

**Execute every step in order.** If the causal chain is A → B → C → impact, the test must perform A, then B, then C, then show impact. Each step goes through the real contract that performs it on-chain, with the caller that performs it on-chain. No step is skipped because it "would obviously work".

**Off-chain signed messages are legitimate test setup.** Many protocols gate functions behind signatures from privileged signers (KYC verifiers, admins, oracle operators) or user-signed requests (EIP-712 withdrawals, meta-transactions). Using `vm.sign` with a test private key to produce these signatures is allowed and expected. The key condition: the test holder of that private key must have been granted the corresponding on-chain role through a real privileged call earlier in the test (e.g., the protocol admin granting the role via the real on-chain permission-update function), not by pranking the role.

**End at realized impact.** If the bug is about stealing funds, the test must show the funds arriving in the attacker's address. If it is about bricking a contract, the test must show the next legitimate call reverting. If it is about permission escalation, the test must show the escalated permission being exercised to do something previously not possible. If it is about freezing funds, the test must show that after the full causal chain runs, no extraction path works, ideally by attempting recovery at the point it should have been possible and showing it is not.

**Proof shape by impact type:**

- **Theft**: attacker ends with tokens they did not legitimately acquire. Proof is `assertGt(attackerBalAfter, attackerBalBefore)` where `attackerBalBefore` is recorded before the exploit path, or `assertGt(stolen, depositedOrPrincipal)` when the attacker deposited something first. Intermediate assertions on share balances or ownership percentages are helpful but not sufficient; the final assertion encodes the realized token transfer.
- **Pool drain**: combine the attacker-gain assertion above with a pool-state assertion showing the pool's balance of the stolen token dropped to near-zero. `assertLe(poolBalAfter, poolBalBefore / 50)` or similar.
- **Freeze**: attempt the action that should succeed at the point where it is supposed to, and prove it reverts or returns a wrong value. Pair with a log or assertion quantifying the frozen value.
- **DoS**: the next legitimate call reverts or returns zero when it should succeed. Prove by attempting the call and showing the revert.
- **Access control / privilege escalation**: the unauthorized caller executes a previously-gated action. Proof is the state change or emitted event produced by the successful call, not a balance delta.

No `vm.expectRevert` in the core proof of a theft-shape or drain-shape finding. The successful execution is the bug.

**Balance deltas and final-state assertions.** Intermediate assertions during the chain are fine and often helpful, but the final assertions must encode the realized end-state, not a midpoint.

### Rule 5: No Shortcutting Protocol Pipelines

When the vulnerability involves funds moving through a protocol pipeline (liquidation, yield distribution, rebalancing, swap routing, oracle updates, cross-module calls), the test must route funds through the real pipeline, not inject them at the last step.

**Allowed:**

- `vm.deal(attacker, 1 ether)` to fund an attacker EOA with gas.
- `deal(token, attacker, 100e18)` to give an attacker a starting capital in a token they could legitimately acquire on mainnet via a swap.
- `vm.prank(user)` to act as a real holder of tokens or shares for a single legitimate action that user could perform.

**Not allowed:**

- `deal(token, protocolContract, amount)` followed by a prank that calls an internal or whitelisted-only function on behalf of that protocol contract. This bypasses the pipeline that would normally produce those tokens in that contract.
- Pranking a privileged role (keeper, liquidator, admin) to call a function when the bug is about what happens downstream of that function, unless the role itself is not the subject of the finding and reproducing the upstream path is genuinely infeasible. In that case, document the limitation explicitly in a comment above the prank.
- Using `vm.store` to place the protocol in a mid-chain state.

**When the real pipeline is too heavy to reproduce** (requires live swap routes, oracle updates, cross-chain messages, time-locked votes), state the limitation explicitly in a single comment above the shortcut, naming what is being simulated and why reproducing it fully is infeasible. The goal is transparency about the gap, not a justification for skipping E2E work that could reasonably be done.

### Rule 6: Pragma And Imports Match The Target

The pragma matches the target contract's compiler version. Imports use the paths present in the target repo if test patterns were provided, otherwise standard Foundry and OpenZeppelin paths.

## Style Rules

- No em-dashes. No "—". No " – ". Use commas or periods.
- Avoid: "crucial", "essentially", "delve", "seamless", "robust", "leverage" (as a verb), "it's important to note", "in summary", "in conclusion", "navigate" (as a metaphor).
- No filler section comments: `// setup`, `// exploit`, `// assert`, `// attack begins here`.
- No summary comment above the test function describing what it does. The test name describes it.
- Inline comments only when they reference something the code cannot express on its own: a specific storage slot, a block-specific condition, a known deployment quirk, a non-obvious reason a call is ordered a specific way, or a documented limitation of what is being simulated vs executed.

## Logging Rules

- `console2.log` is used only to print values that quantify impact or demonstrate state change. Every log has at least two arguments: a label and a value.
- Banned: status strings like `"Exploit successful"`, `"Vulnerability confirmed"`, `"Attack starting"`, `"Step 1 complete"`, and any equivalent.
- No log that duplicates what an assertion already proves on the same line.
- If the bug has no numerical impact to print (pure logic bug with a revert as the proof), zero logs is the correct number.
- No redundant logs that prove the same thing twice with different framings.

## Assertion Rules

- Every assertion encodes the vulnerability invariant. An assertion that restates a `vm.prank` or confirms the fork block number is noise.
- Prove theft or loss with before/after balance deltas, not absolute balances.
- Prove impact with the final end-state, not an intermediate one.
- Use typed selectors for expected reverts: `vm.expectRevert(Contract.ErrorName.selector)` or `vm.expectRevert(abi.encodeWithSignature("ErrorName()"))`. Use string matching only if the target contract reverts with strings.
- **Assertion messages are CI failure labels, not explanations.** Good: `"timer not reset"`, `"totalSupply nonzero"`, `"no frozen balance"`. Bad: `"timer must advance past first reset"`, `"unlock window must be pushed out"`. If a message reads as a full sentence or contains "must", it is too long. Aim for two to five words that name what failed. Prefer omission over prose.
- **One demonstration per invariant.** If two iterations prove the same pattern, two is enough. A third is redundant. Each repeated iteration must prove a distinct invariant.
- **setUp sanity checks are permitted** for verifying the fork returned the expected mainnet state (token decimals, whitelisting status, pool's value token). Use `assertEq`/`assertFalse` with short labels. These are not proofs of the vulnerability; they protect against fork drift.

## File Template

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity <version matching target>;

import { Test, console2 } from "forge-std/Test.sol";
import { IERC20 } from "openzeppelin-contracts/token/ERC20/IERC20.sol";
// additional imports from the target repo if patterns were provided

interface I<Target> {
    // only functions the PoC calls, signatures matching deployed bytecode
}

contract POC_<FindingID> is Test {
    // Protocol addresses, grouped and labeled by role
    address constant <ROLE_NAME> = 0x...;

    I<Target> target;
    address attacker;

    function setUp() public {
        vm.createSelectFork(vm.envString("<CHAIN>_RPC_URL"), <BLOCK_OR_LATEST>);

        target = I<Target>(<ADDRESS_CONSTANT>);
        attacker = makeAddr("attacker");

        // Minimal state prep the actor could legitimately reach
    }

    function test_<ShortVulnName>() public {
        // Step A: first-triggering action
        // Step B: intermediate real contract calls
        // Step C: final action that realizes impact
        // Assertions encoding the realized end-state
    }
}
```

The numbered comments above are placeholders showing the four E2E phases, not a pattern to copy into output. Real output has no filler comments.

## Procedure

1. Read the finding description in full. Do not open any other file until this is done.
2. Confirm required inputs (see Required Inputs). If anything is missing or ambiguous, ask before writing.
3. **Classify the finding and state the classification out loud** to the user: "(a)/(b)/(a+b) because [signal]. Starting actor: [X]. Fork block: [Y]. Causal chain: [step 1 → step 2 → ... → impact]." This statement must appear before any file-reading or code-writing. Do not skip it.
4. Check whether the proposed fork block places the chosen actor in a pre-vulnerable or post-vulnerable state. For (a), post-vulnerable is correct. For (b) and (a+b), the chosen actor must still be in the safe state at fork time.
5. Confirm every protocol address needed for the chain has been provided. If the finding mentions "N vulnerable actors" or "N single-X vaults" and the addresses of those specific actors are not provided, ask the user which one to start from and get the address.
6. Now, and only now, read reference test files in the repo for style matching (imports, inheritance, helper usage, naming). If a file with the planned output name already exists, either rename or skip it. Do not use it as a template for causal-chain structure.
7. Determine the pragma from the target contract.
8. Bind every protocol address as a named `constant`.
9. Write the minimal interface(s) needed. Signatures must match the deployed ABI.
10. Write `setUp`: fork call first, contract bindings, then only the state prep an actor could legitimately perform and that is outside the causal chain being tested.
11. Write the test function: every step from the chain in step 3, in order, through real contracts, with the real caller for each step. End with assertions that encode the realized end-state.
12. Produce the exact `forge test` command with `-vvvv` for full trace visibility.
13. Run through the Self-Review Checklist before returning output.

## Self-Review Checklist

- [ ] Finding was read in full before any other file in the repo.
- [ ] Classification ((a)/(b)/(a+b)) was stated out loud to the user before coding.
- [ ] For (b) or (a+b) findings, the test starts from an actor currently in the safe state, not from an already-impacted actor.
- [ ] No existing PoC file in the repo was used as a structural template. Reference files were only used for surface style (imports, inheritance, helpers).
- [ ] `vm.createSelectFork` is the first statement in `setUp()`.
- [ ] Every protocol contract is bound as a named `constant` real address.
- [ ] No mock, stub, or minimal reimplementation is declared.
- [ ] Every step in the causal chain is executed through the real contract that performs it on-chain, with the caller that performs it on-chain.
- [ ] No `deal`/prank combination bypasses a pipeline the finding says funds should flow through.
- [ ] Any shortcut around a genuinely infeasible step is documented in a single comment naming what is simulated.
- [ ] The test ends at the realized impact, not a theoretical midpoint.
- [ ] Final assertions encode the end-state of the vulnerability.
- [ ] No banned words, no em-dashes, no filler comments, no status-string logs.
- [ ] Every `console2.log` prints a labeled value and does not duplicate another log or assertion.
- [ ] Assertion messages are two to five words, label-style, no "must", no prose. Omitted where nothing useful can be said briefly.
- [ ] No invariant is proven twice in the same test.
- [ ] Pragma matches the target contract.
- [ ] The test name describes the vulnerability, not the test action.
- [ ] Run command uses `-vvvv` for full traces.

## Output

Return three things, in this order:

1. The complete test file.
2. The exact `forge test` command, including required environment variables and `-vvvv`.
3. Two or three sentences explaining what the passing assertions prove about the vulnerability and the end-to-end impact.

No JSON wrapper, no preamble, no "here is your PoC". Just the file, the command, the explanation. The classification statement from Procedure step 3 appears separately, before the PoC content, not in the PoC itself.

## Reference Examples

The `examples/` folder contains shape-diverse PoCs. Each demonstrates a distinct bug structure:

- `Example_FreezeHistorical.t.sol` — category (a), vulnerable state reached by block progression alone, no causal chain to reproduce
- `Example_RoutingDoS.t.sol` — category (b), adapter logic error causes either DoS revert or fund stranding on every affected swap; proof is a revert plus a separate success-with-stranding test
- `Example_PoolDrainTheft.t.sol` — category (b), decimals mismatch lets attacker mint inflated shares from a trivial deposit; proof is before/after balance delta showing attacker received >98% of pool's principal

When writing a new PoC, match the example closest to the finding's shape for surface-level patterns (interface style, helper functions, assertion shape), but always classify independently and execute the skill's procedure from step 1.
