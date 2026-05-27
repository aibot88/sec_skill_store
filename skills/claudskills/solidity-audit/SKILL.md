---
name: solidity-audit
description: >
  Solidity development standards and security auditing. TRIGGER when: working
  with .sol files, foundry.toml, hardhat.config.*, smart contract auditing,
  security review, or vulnerability analysis. Covers Foundry-first development
  patterns, vulnerability taxonomies, and audit methodology. DO NOT TRIGGER
  when: general Ethereum tooling/ecosystem questions (use ethskills skill),
  or Noir/ZK circuits (use noir skill).
metadata:
  author: DROOdotFOO
  version: "1.0.0"
  tags: solidity, audit, security, foundry, smart-contracts, vulnerabilities
---

> **You are a Senior Smart Contract Auditor** -- you assume every external call is hostile, every state transition hides an edge case, and the fuzzer is your most honest colleague.

# solidity-audit

Opinionated Solidity development standards and security auditing methodology.
Foundry-first. Synthesized from community best practices (pashov, cyfrin,
scv-scan, trail of bits, ethskills) and tailored to our workflow.

## What You Get

- Pre-audit reconnaissance (entry-point classification, protocol-type threat profiles)
- Foundry-first development patterns (testing, fuzzing, invariants, forks)
- Vulnerability taxonomy: reentrancy, access control, oracles, flash loans, MEV, weird ERC20s
- Bleeding-edge attack vector database with detect/false-positive pairs
- 5-phase audit methodology with proof-required discipline and FP elimination
- Anti-skip rules preventing false negatives from rationalized dismissals
- Code quality standards (NatSpec, errors, events, gas patterns)
- Live documentation sources (ETHSkills, community references)

## Philosophy

Everything will be attacked. Write code as if the attacker has unlimited
resources, can call any function in any order, and will exploit every
unvalidated assumption. Prove safety through invariant testing, not
optimistic unit tests.

## When to use

This skill activates when writing, reviewing, or auditing Solidity contracts.

## When NOT to use

- For general Ethereum ecosystem/tooling -- use ethskills
- For Noir/ZK circuit work -- use noir
- For non-Solidity languages -- use droo-stack

## See also

- `ethskills` -- for EIP/ERC standard lookup, tool selection, and RPC/explorer reference
- `noir` -- for ZK circuits that integrate with Solidity via verifier contracts
- `zk-x-ray` -- for pre-audit reports on ZK + EVM hybrid protocols (Noir + Solidity)
- `design-ux` -- for smart contract frontend design and transaction UX

## Reading guide

### Development patterns

| Working on                                  | Read                                        |
| ------------------------------------------- | ------------------------------------------- |
| Code quality, NatSpec, errors, events, gas  | [patterns/standards](patterns/standards.md) |
| Foundry testing, fuzzing, invariants, forks | [patterns/foundry](patterns/foundry.md)     |

### Vulnerability knowledge (by severity)

| Category                                        | Read                                                                          |
| ----------------------------------------------- | ----------------------------------------------------------------------------- |
| Reentrancy (classic, cross-function, read-only) | [vulnerabilities/reentrancy](vulnerabilities/reentrancy.md)                   |
| Access control, tx.origin, delegatecall         | [vulnerabilities/access-control](vulnerabilities/access-control.md)           |
| Oracle manipulation, Chainlink, TWAP            | [vulnerabilities/oracle-manipulation](vulnerabilities/oracle-manipulation.md) |
| Flash loan price/governance attacks             | [vulnerabilities/flash-loans](vulnerabilities/flash-loans.md)                 |
| MEV, frontrunning, sandwich protection          | [vulnerabilities/mev](vulnerabilities/mev.md)                                 |
| Weird ERC20 tokens (fee-on-transfer, rebasing)  | [vulnerabilities/weird-erc20](vulnerabilities/weird-erc20.md)                 |
| Bleeding-edge vectors (EIP-7702, precision, proxy) | [vulnerabilities/attack-vectors](vulnerabilities/attack-vectors.md)        |

### Audit workflow

| Task                                         | Read                                                                |
| -------------------------------------------- | ------------------------------------------------------------------- |
| Pre-audit reconnaissance (entry points, threat profiles) | [audit-workflow/pre-audit](audit-workflow/pre-audit.md)   |
| Full audit methodology (5 phases)            | [audit-workflow/methodology](audit-workflow/methodology.md)         |
| Anti-skip rules, proof discipline, FP elimination | [audit-workflow/anti-skip](audit-workflow/anti-skip.md)        |
| Finding report template                      | [audit-workflow/report-template](audit-workflow/report-template.md) |
| Live documentation sources (ETHSkills, etc.) | [live-sources](live-sources.md)                                     |
