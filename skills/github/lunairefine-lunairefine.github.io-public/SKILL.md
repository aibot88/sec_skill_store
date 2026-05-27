# Taxonomy: Web3 & Smart Contract Security Engineer

## 1. Domain: Smart Contract Development & EVM Architecture
### 1.1. Core Programming
- Solidity (v0.8.x+)
- Solidity Legacy (<0.8.0) Vulnerability Mechanics
- Vyper (Conceptual)
- Yul / Inline Assembly

### 1.2. EVM Architecture & Low-Level Mechanics
- EVM Opcodes & State Transition
- Memory & Storage Layout Analysis
- Calldata & ABI Encoding/Decoding
- Context Execution (Delegatecall, Staticcall, Call)
- Storage Slot Manipulation & Collision Mapping
- Gas Optimization Techniques
- Bytecode Analysis & Reverse Engineering

### 1.3. Smart Contract Standards & Patterns
- Token Standards (ERC-20, ERC-721, ERC-1155, ERC-721A)
- Upgradeable Contracts (Transparent, UUPS, Beacon Proxy)
- Proxy Uninitialization & Storage Collision Mitigation

## 2. Domain: Security, Penetration Testing & Auditing
### 2.1. Audit Methodology & Reconnaissance
- Money Flow & Fund Custody Tracking
- Access Control & Role Mapping
- External Dependency & Trust Assumption Analysis
- State Machine Transition & Execution Flow Control
- Lifecycle Analysis (Initialization to Finalization)

### 2.2. Threat Modeling & Game Theory
- Economic Attack Surface Mapping
- Reward Exploitation & Arbitrage Modeling
- Flash Loan Profit Scenario Simulation
- Staking & Incentive Abuse Logic

### 2.3. Automated Security Tools
- Static Analysis (Slither, Aderyn)
- Symbolic Execution (Mythril)
- Foundry Debugger & Trace Logging
- Custom Script Analyzers

### 2.4. Advanced Testing Methodologies
- Fuzz Testing (Foundry Fuzzing)
- Property-based Testing (Echidna)
- Invariant Validation & Simulation
- Formal Verification (Certora, Halmos)
- Mainnet Fork Integration Testing

### 2.5. Vulnerability Identification (Common Attack Vectors)
- Reentrancy (Cross-function, Cross-contract, Read-only)
- Access Control Bypass
- Integer Overflow / Underflow
- Arithmetic Precision Loss / Rounding Errors
- Spot Price & Oracle Manipulation
- TWAP (Time-Weighted Average Price) Misuse
- Front-running & MEV (Sandwich Attacks, Priority Gas Auctions)
- Unsafe Delegatecall Execution
- Improper State Validation & Double Spend

## 3. Domain: Web3 Integration & Scripting
### 3.1. Libraries & Automation
- Ethers.js / Web3.js
- Viem / Wagmi
- OpenZeppelin Contracts & Libraries
- Node.js Scripting for Blockchain Automation
- CLI Tool Development for On-chain Interaction

### 3.2. Development Frameworks
- Foundry (Forge, Cast, Anvil)
- Hardhat
- Truffle (Legacy Analysis)

### 3.3. Application Layer (Frontend & Backend)
- Next.js / React.js
- Tailwind CSS
- Wallet Integration (MetaMask, WalletConnect)
- RPC Rotation & Multicall Implementation
- Event Listening & Log Decoding
- NFT Metadata (JSON) & IPFS Integration (Pinata)
- Batch Minting & Reveal Mechanisms

## 4. Domain: Data Analysis & Threat Intelligence
### 4.1. On-Chain Analysis
- Wallet Behavior & Address Profiling
- Transaction Pattern & Graph-based Tracking
- Airdrop Sybil Farming Analysis
- Protocol Liquidity Monitoring

## 5. Domain: Infrastructure & Advanced Ecosystems
### 5.1. DevOps & Environment
- Git / GitHub Version Control
- CI/CD pipelines for Smart Contracts
- VPS & Docker Environments
- Custom RPC Node Utilization

### 5.2. Advanced Web3 Protocols
- Account Abstraction (ERC-4337)
- Layer 2 Rollup Architectures (Optimistic: Arbitrum, Optimism; ZK: zkSync, Starknet)
- Cross-chain Bridging Protocols
- Decentralized Finance (DeFi) primitives (AMMs, Liquidity Pools, Yield Farming)