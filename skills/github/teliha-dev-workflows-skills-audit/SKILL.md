---
name: Smart Contract Security Audit
description: Deep security analysis for Solidity smart contracts with DeFi context
category: Security
tags: [security, solidity, defi, audit, vulnerability]
---

<!-- AUDIT:START -->

# Smart Contract Security Audit Skill

## When to Use This Skill

This skill automatically activates when:
- Reviewing `.sol` (Solidity) files
- User asks about security or vulnerabilities
- User requests code review of smart contracts
- User mentions "audit" in context of smart contracts

## Audit Process

### Step 1: Initial Analysis

Before diving into vulnerabilities, understand the contract:

1. **Identify Contract Type**
   - Is it an operator, vault, helper, or other contract type?
   - What is its primary purpose?

2. **Map External Dependencies**
   - Which external contracts does it interact with? (EVK, EVC, Uniswap, etc.)
   - Are these dependencies trusted or untrusted?

3. **Identify Trust Boundaries**
   - What functions are public vs internal?
   - Who can call sensitive functions?
   - Where does user input enter the system?

### Step 2: Read the Entire Contract

**CRITICAL**: You MUST read the complete contract code before performing the audit. Never audit based on partial information.

### Step 3: Systematic Vulnerability Check (PARALLEL)

**PARALLELIZATION OPPORTUNITY**: When auditing, run vulnerability categories in parallel:

```
Use the Task tool with parallel subagents for each vulnerability category:

Task 1: Reentrancy Analysis
  - Check all external calls
  - Verify Checks-Effects-Interactions pattern
  - Look for callback vulnerabilities

Task 2: Access Control Analysis
  - Check all public/external functions
  - Verify authorization on sensitive operations
  - Review modifier usage

Task 3: Integer Operations Analysis
  - Check division operations
  - Verify precision handling
  - Look for edge cases

Task 4: External Call Safety Analysis
  - Check return value handling
  - Verify error propagation
  - Review delegatecall usage

Task 5: Token Handling Analysis
  - Check approve patterns
  - Verify transfer return values
  - Check for fee-on-transfer issues

Task 6: Flash Loan / Oracle Analysis
  - Check price manipulation risks
  - Verify oracle staleness checks
  - Review single-block manipulation
```

Each subagent focuses on one vulnerability category with deep analysis.
Results are combined into the final audit report.

**For multiple contracts**: Audit each contract in parallel with separate subagents.

Go through each category below systematically:

## Common Vulnerability Categories

### 1. Reentrancy Attacks

**What to check:**
- [ ] Are state changes made BEFORE external calls? (Checks-Effects-Interactions pattern)
- [ ] Are there any unguarded external calls that could callback into this contract?
- [ ] Does the contract use `nonReentrant` modifiers where appropriate?
- [ ] Could an attacker exploit the call order to drain funds or manipulate state?

**Look for patterns like:**
```solidity
// VULNERABLE
function withdraw() external {
    msg.sender.call{value: balance[msg.sender]}("");  // External call first
    balance[msg.sender] = 0;  // State change after - BAD!
}

// SAFE
function withdraw() external {
    uint256 amount = balance[msg.sender];
    balance[msg.sender] = 0;  // State change first
    msg.sender.call{value: amount}("");  // External call after - GOOD!
}
```

### 2. Access Control

**What to check:**
- [ ] Do all sensitive functions have proper authorization checks?
- [ ] Are there any privileged functions missing access control?
- [ ] Could an attacker call admin-only functions?
- [ ] Is role-based access control implemented correctly?

**For EVK/EVC contracts specifically:**
- [ ] Are operator functions protected by `callThroughEVC` modifier?
- [ ] Is `evc.getCurrentOnBehalfOfAccount()` used to get the correct user?
- [ ] Are vault operations properly authorized via EVC?

**Look for:**
```solidity
// VULNERABLE
function setOwner(address newOwner) external {
    owner = newOwner;  // No access control - BAD!
}

// SAFE
function setOwner(address newOwner) external onlyOwner {
    owner = newOwner;  // Properly protected - GOOD!
}
```

### 3. Integer Operations

**What to check:**
- [ ] Even with Solidity 0.8.24+, are there edge cases with overflow/underflow?
- [ ] Are division operations checked for division by zero?
- [ ] Is division performed before multiplication (precision loss)?
- [ ] Are percentage calculations handled safely?

**Look for:**
```solidity
// PRECISION LOSS
uint256 result = (a / b) * c;  // BAD! Loses precision

// BETTER
uint256 result = (a * c) / b;  // GOOD! Multiply first
```

### 4. External Call Safety

**What to check:**
- [ ] Are return values from external calls properly checked?
- [ ] Are low-level calls (`.call`, `.delegatecall`) error-handled?
- [ ] Could malicious contracts exploit callback functions?
- [ ] Are there unchecked `delegatecall` operations?

**Look for:**
```solidity
// VULNERABLE
token.transfer(recipient, amount);  // Ignores return value - BAD!

// SAFE
require(token.transfer(recipient, amount), "Transfer failed");  // GOOD!

// OR with Solmate/Modern patterns
ERC20(token).transfer(recipient, amount);  // Reverts on failure - GOOD!
```

### 5. Token Handling

**What to check:**
- [ ] Are ERC20 `approve` operations checked for race conditions?
- [ ] Are transfer return values validated?
- [ ] Could token balance be manipulated?
- [ ] Are fee-on-transfer tokens handled correctly?

**Look for:**
```solidity
// APPROVE RACE CONDITION
function updateAllowance(address spender, uint256 amount) external {
    token.approve(spender, amount);  // Vulnerable to race condition
}

// BETTER
function updateAllowance(address spender, uint256 amount) external {
    token.approve(spender, 0);  // Reset first
    token.approve(spender, amount);  // Then set new amount
}
```

### 6. Flash Loan Protection

**What to check:**
- [ ] Could prices be manipulated in a single block/transaction?
- [ ] Are oracles used correctly with staleness checks?
- [ ] Could an attacker profit from flash loan attacks?
- [ ] Are balances checked consistently within a transaction?

## DeFi-Specific Pattern Checks

### 7. EVK/EVC Integration (Project-Specific)

**What to check:**
- [ ] Is `callThroughEVC` modifier used on all operator functions?
- [ ] Is `evc.getCurrentOnBehalfOfAccount(address(0))` used to get the actual user?
- [ ] Is `evc.requireAccountStatusCheck(account)` called at the end of risky operations?
- [ ] Are collaterals enabled via `evc.enableCollateral(account, vault)`?
- [ ] Are controllers enabled via `evc.enableController(account, vault)`?
- [ ] Are vault operations called through `evc.call(vault, account, 0, calldata)`?

**Legitimate EVK patterns to recognize (NOT vulnerabilities):**
```solidity
// GOOD PATTERN - EVC Authentication
modifier callThroughEVC() {
    require(msg.sender == address(evc), "Must call through EVC");
    _;
}

function openPosition(...) external callThroughEVC {
    (address account,) = evc.getCurrentOnBehalfOfAccount(address(0));
    // ... operations on behalf of account ...
    evc.requireAccountStatusCheck(account);  // Health check at end
}
```

### 8. Vault Operations

**What to check:**
- [ ] Are deposit/withdraw operations properly authorized?
- [ ] Is share calculation accurate and resistant to manipulation?
- [ ] Could vault state be manipulated via donation attacks?
- [ ] Are allowances managed correctly?

### 9. Liquidation Logic

**What to check:**
- [ ] Are health factor calculations correct and manipulation-resistant?
- [ ] Could liquidation thresholds be bypassed?
- [ ] Are liquidations protected against frontrunning?
- [ ] Are liquidator profit calculations fair and bounded?

**Look for:**
```solidity
// Check that liquidation logic is sound
function isLiquidatable(address user) public view returns (bool) {
    (uint256 collateral, uint256 debt) = getAccountValues(user);
    uint256 ltv = (debt * 10000) / collateral;  // Check for div by zero!
    return ltv > liquidationThreshold;
}
```

### 10. Swap Integration

**What to check:**
- [ ] Is slippage protection implemented (minAmountOut / maxAmountIn)?
- [ ] Are swap deadlines used to prevent stale transactions?
- [ ] Could MEV bots sandwich attack the swap?
- [ ] Are swap amount calculations correct?

**Look for:**
```solidity
// VULNERABLE - No slippage protection
router.swapExactTokensForTokens(amountIn, 0, path, to, deadline);  // BAD!

// SAFE - Slippage protection
uint256 minOut = expectedOut - (expectedOut * maxSlippage / 10000);
router.swapExactTokensForTokens(amountIn, minOut, path, to, deadline);  // GOOD!
```

## Gas Optimization Issues

**What to check:**
- [ ] Are there unnecessary storage reads? (use memory/stack variables)
- [ ] Are external calls made multiple times when once would suffice?
- [ ] Are loops inefficient or unbounded?
- [ ] Are variables unnecessarily initialized to zero?
- [ ] Could `unchecked` blocks be used for safe operations?

**Examples:**
```solidity
// INEFFICIENT
for (uint256 i = 0; i < array.length; i++) {  // Reads length every iteration
    // ...
}

// OPTIMIZED
uint256 length = array.length;  // Cache in memory
for (uint256 i; i < length;) {  // i defaults to 0, no need to initialize
    // ...
    unchecked { ++i; }  // Safe increment, saves gas
}
```

## Code Quality Issues

**What to check:**
- [ ] Are all function inputs validated?
- [ ] Are error messages clear and helpful?
- [ ] Are events emitted for all significant state changes?
- [ ] Are naming conventions consistent?
- [ ] Is there dead code or unused variables?

### Step 4: Generate Audit Report

After completing the systematic check, generate a comprehensive Markdown audit report.

**Report Location**: Save to `audits/[ContractName]_audit_[YYYY-MM-DD].md`

**Report Structure**:

```markdown
# Smart Contract Security Audit Report

**Contract**: [ContractName]
**Path**: [file/path.sol]
**Date**: [YYYY-MM-DD HH:MM]
**Auditor**: Claude Code Audit Skill

---

## Executive Summary

- **Overall Risk Level**: [CRITICAL/HIGH/MEDIUM/LOW]
- **Total Issues Found**: [count]
  - Critical: [count]
  - High: [count]
  - Medium: [count]
  - Low/Info: [count]

[Brief 2-3 sentence summary of overall contract security]

---

## Findings

### [CRITICAL/HIGH/MEDIUM/LOW] Finding #1: [Descriptive Title]

**Location**: `[filename.sol:line_number]`

**Category**: [Reentrancy/Access Control/Integer/etc.]

**Description**: 
[Detailed explanation of the vulnerability]

**Impact**: 
[What could an attacker do? What's at risk?]

**Recommendation**: 
[Specific steps to fix the issue]

**Vulnerable Code**:
```solidity
// Show the problematic code
```

**Suggested Fix**:
```solidity
// Show how to fix it
```

---

[Repeat for each finding]

---

## Gas Optimization Opportunities

### Optimization #1: [Title]

**Location**: `[filename.sol:line_number]`

**Current Implementation**:
```solidity
// Current code
```

**Optimized Implementation**:
```solidity
// Optimized code
```

**Estimated Gas Savings**: [Approximate savings]

---

## Code Quality Issues

### Issue #1: [Title]

**Location**: `[filename.sol:line_number]`

**Issue**: [Description]

**Recommendation**: [How to improve]

---

## Architecture Review

[High-level observations about:]
- Overall design patterns
- Integration safety with external protocols (EVK, Uniswap, etc.)
- Separation of concerns
- Upgrade patterns (if applicable)
- Emergency procedures

---

## Positive Findings

[What the contract does well from a security perspective:]
- Proper use of established patterns
- Good access control
- Appropriate use of events
- etc.

---

## Conclusion

[Overall assessment including:]
- Summary of main concerns
- Priority of fixes
- Next steps/recommendations
- Overall security posture

---

## Disclaimer

This audit was performed by Claude Code's automated audit skill. While comprehensive, it should not replace a professional security audit by human experts, especially for production contracts handling significant value.
```

### Step 5: Project-Specific Context

**This project's architecture** (from CLAUDE.md):
- **quoteVault**: Quote yield vault (can be collateral or debt)
- **assetVault**: Asset yield vault (can be collateral or debt)

**CRITICAL**: The two vaults use **different underlying tokens** (e.g., quoteVault for USDC and assetVault for WETH).

**Legitimate Patterns** (NOT vulnerabilities):
- `callThroughEVC` modifier for EVC authentication
- `evc.call(vault, account, 0, calldata)` for vault operations on behalf of users
- `evc.requireAccountStatusCheck(account)` at end of operations
- External swap router calls with slippage protection
- Borrowing via EVC then swapping for margin positions
- Single swap per close operation (critical optimization)

**Anti-Patterns to Flag**:
- Direct vault operations without EVC authentication
- Missing `evc.requireAccountStatusCheck()` after position changes
- Swap operations without slippage protection (minAmountOut / maxAmountIn)
- Missing authorization checks on operator functions
- Unchecked external call return values
- Multiple swaps when one swap would suffice (violates single-swap rule)

**Position Management Patterns**:
- **closeLong**: Should use ONE exactInputSwap (asset → quote) to close position
- **closeShort**: Should use ONE exactOutputSwap (quote → asset, exact amount for debt repayment)
- Final user balance should be in quote token (Quote)
- Long positions only have Asset collateral in assetVault
- Short positions only have Quote collateral in quoteVault

<!-- AUDIT:END -->
