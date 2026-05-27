---
name: noir
description: >
  Zero-knowledge circuit design with Noir (Aztec's ZK DSL). TRIGGER when:
  working with .nr files, Nargo.toml, ZK circuits/proofs, Aztec contracts,
  zoir extension, or discussing zero-knowledge proof design. Covers circuit
  architecture, constraint optimization, ZK-specific security, and Aztec
  integration. DO NOT TRIGGER when: only Noir language syntax is needed
  (droo-stack handles that), or working with Solidity (use solidity-audit skill).
metadata:
  author: DROOdotFOO
  version: "1.0.0"
  tags: noir, zk, zero-knowledge, aztec, circuits, proofs, nargo, zoir
---

# noir

Domain knowledge for zero-knowledge circuit design with Noir. For Noir language
syntax patterns (types, modules, generics), see droo-stack's noir-patterns rule.
This skill covers the **why** of ZK: circuit architecture, security pitfalls,
Aztec integration, and testing strategy.

## What You Get

- Circuit architecture and constraint optimization patterns
- ZK-specific security: privacy leaks, oracle safety, nullifier attacks
- Systematic circuit audit methodology (spec-to-constraint mapping, completeness, privacy analysis)
- Aztec contract integration (notes, storage, account abstraction)
- Testing strategy: nargo tests, e2e setup, cross-chain messaging
- Constrained vs unconstrained computation guidance

## When to use

This skill activates when working on ZK circuit design, proof systems, or Aztec
contracts. It complements droo-stack (which covers Noir syntax) with domain
knowledge that requires ZK expertise.

## When NOT to use

- For Noir language syntax only (types, modules, generics) -- use droo-stack
- For Solidity smart contracts -- use solidity-audit
- For general Ethereum tooling -- use ethskills

## See also

- `droo-stack` -- for Noir language syntax (types, modules, generics)
- `solidity-audit` -- for Solidity verifier contracts that consume Noir proofs
- `zk-x-ray` -- for pre-audit reports on ZK + EVM hybrid protocols (Noir + Solidity)
- `ethskills` -- for Ethereum ecosystem tooling and standards

## Reading guide

| Working on                                       | Read                                                    |
| ------------------------------------------------ | ------------------------------------------------------- |
| Circuit design, constraint optimization          | [circuits/constrained](circuits/constrained.md)         |
| Oracle calls, unconstrained computation          | [circuits/unconstrained](circuits/unconstrained.md)     |
| Privacy leaks, public/private input design       | [security/privacy](security/privacy.md)                 |
| Unconstrained return safety, oracle verification | [security/oracle-safety](security/oracle-safety.md)     |
| Circuit audit methodology, spec compliance       | [security/circuit-audit](security/circuit-audit.md)     |
| Aztec-specific attacks: nullifiers, MEV, leakage | [security/aztec-contracts](security/aztec-contracts.md) |
| Aztec contract structure, notes, storage         | [aztec/contracts](aztec/contracts.md)                   |
| Account abstraction, access control, keys        | [aztec/accounts](aztec/accounts.md)                     |
| Testing with nargo, proof vs execution           | [testing/nargo](testing/nargo.md)                       |
| Aztec e2e test setup, accounts, deployment       | [testing/e2e-setup](testing/e2e-setup.md)               |
| Token testing, AuthWit, balance assertions       | [testing/e2e-token](testing/e2e-token.md)               |
| Cross-chain L1/L2, event testing                 | [testing/e2e-messaging](testing/e2e-messaging.md)       |
