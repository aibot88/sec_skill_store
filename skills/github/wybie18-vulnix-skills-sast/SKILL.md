---
name: sast
description: 'Strict static code analysis methodology, AST review constraints, taint analysis flow, and definitive checks for injection, authentication, and cryptographic flaws. Use for authoritative SAST testing and secure code review.'
---

# Static Application Security Testing (SAST) Skill

This skill enforces a strict, multi-step methodology for Static Application Security Testing (SAST). It ensures that all testing covers required security boundaries natively in source code without skipping critical details.

## When to Activate
• Running Static Application Security Testing against source code
• Parsing and analyzing AST (Abstract Syntax Tree) patterns for logic flaws
• Identifying Injection, Authentication, or Cryptographic vulnerabilities directly in local files
• Running pre-commit hooks or CI/CD source branch validations

## Security & Pattern Checklist

### 1. Data Flow & Taint Analysis
Evaluate how untrusted data propagates from sources to sinks.

#### ✅ ALWAYS Verify This
- Trace all input sources (e.g., `$_GET`, `req.query`, `sys.argv`, environment variables) through the code syntax tree.
- Verify explicit output encoding or sanitization happens immediately before the sink.
- Ensure strict type casting (e.g., `int()`) is enforced on expected primitive types early in the execution chain.

#### Verification Steps
- [ ] Source-to-sink mapping confirms reachability.
- [ ] Missing sanitization flags explicitly highlight the exact line of failure.
- [ ] Framework-specific auto-escaping contexts (e.g., Jinja2, React) are considered safe unless intentionally bypassed (e.g., `dangerouslySetInnerHTML`, `|safe`).

### 2. Injection Flaws
Do not assume parameterized statements are safe without inspecting their input binding.

#### ❌ NEVER Accept This
- String formatting parameters (`f"{var}"`, `.format(var)`, or `%s`) actively used inside database query execution strings.
- Dynamically built Table or Column names from unpredictable user input without a strict whitelist model.
- Trusting input inside local Operating System command sinks like `subprocess.run(shell=True, ...)`.

#### Verification Steps
- [ ] Ensure [Injection Patterns](./patterns/injection.yaml) match against known vulnerable sinks.
- [ ] Validate strict `?` or `$1` parameter bindings in SQL statements.
- [ ] Unsafe deserialization endpoints (`pickle.loads`, `yaml.unsafe_load`, `eval()`) are immediately flagged and barred.

### 3. Cryptography & Key Management
Hardcoded values and legacy hashes are universally non-compliant.

#### ❌ NEVER Accept This
- MD5, SHA1, DES, or RC4 algorithms used in any new encryption logic.
- Hardcoded Initialization Vectors (IVs) or cryptographic salts deployed statically inside configuration or source files.
- Utilizing mathematically predictable pseudo-random number generators (`Math.random()`, `random.randint()`) for security tokens or session establishment.

#### Verification Steps
- [ ] Ensure [Cryptographic Patterns](./patterns/crypto.yaml) scan strictly flags misconfigurations.
- [ ] Check key generation relies exclusively on CSPRNG libraries (`secrets` module in Python, `crypto.randomBytes` in Node.js).
- [ ] Key lengths meet minimum NIST requirements (e.g., RSA >= 2048, AES >= 256).

### 4. Authentication & Authorization Flows
Business logic mapped natively in the backend logic limits horizontal/vertical escalation.

#### ✅ ALWAYS Test Multiple Contexts
- Ensure middleware correctly enforces role checks before resolving execution route returns.
- Check for hardcoded default credentials or backdoor logic bypasses inside debug `if/else` routes.
- Load appropriate payload constraints: [Auth Patterns](./patterns/auth.yaml)

#### Verification Steps
- [ ] Routes contain mandatory authorized logic constraints (e.g., `@login_required` decorators).
- [ ] Validated JWT logic checks signatures explicitly; `verify=False` parameters are flagged as Critical.

---

## Analysis & Reporting Guide

### Injection Context Isolation
Provide verbatim AST/Source snippets:
- Differentiate between Direct Execution (`os.system(user_input)`) and Indirect Vulnerability (`os.system("ls " + stored_db_value)`).

### Contextual False Positives
- **DO NOT** flag `random()` if it is strictly used for non-security mechanics (e.g., pseudo-randomly assigning UI states, selecting test cases).
- **DO NOT** flag static SQL string concatenation if there is definitively no untrusted input substitution mathematically possible.

## Rules of Engagement
- **Static ONLY**: SAST never executes local code, nor attempts to interact with third-party networks for resolving package dependencies.
- **Reporting Fidelity**: Provide verbatim code snippets, strict trace routes, and map to explicit standardized classifications (CWE-89, CWE-79, CWE-327) using the Vulnix reporting standards.
