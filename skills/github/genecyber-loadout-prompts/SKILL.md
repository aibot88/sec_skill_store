# Security Audit Guide Template

This guide provides a structured approach for analyzing skill security and identifying potential vulnerabilities.

## Overview

When auditing a skill, you are performing a comprehensive security review to ensure it is safe to use. This includes analyzing scripts, verifying frontmatter claims, assessing trust levels, and flagging suspicious patterns.

## Skill Information to Gather

Before beginning the audit, collect the following information:

- **Name**: The skill's identifier
- **Description**: What the skill claims to do
- **Path**: Location of the skill directory
- **SKILL.md Path**: Location of the main skill file
- **Author**: Who created the skill (if specified)
- **Version**: Current version (if specified)
- **License**: License type (if specified)

## Audit Checklist

### 1. Script Analysis

For each script in the `scripts/` directory, perform the following checks:

- [ ] **Shell Injection Vulnerabilities**
  - Look for unescaped variables in shell commands
  - Check for `eval` usage with user input
  - Identify `$()` or backtick command substitution with untrusted data
  - Search for `source` or `.` commands with dynamic paths

- [ ] **Network Calls**
  - Identify `curl`, `wget`, `fetch`, or HTTP request patterns
  - Check for outbound connections to unknown hosts
  - Verify any API endpoints are legitimate
  - Look for data exfiltration patterns

- [ ] **File System Operations**
  - Catalog all read operations
  - Identify write operations and their targets
  - Check for delete or modify operations
  - Verify operations stay within appropriate boundaries

- [ ] **External Command Execution**
  - List all external commands invoked
  - Check for dynamic command construction
  - Verify necessity of each command

- [ ] **Input Validation**
  - Check if inputs are validated before use
  - Verify sanitization of special characters
  - Look for proper quoting of variables

### 2. Frontmatter Verification

Compare declared metadata with actual capabilities:

- [ ] **Name Verification**
  - Does the name accurately reflect the skill's purpose?
  - Is it misleading in any way?

- [ ] **Description Accuracy**
  - Does the description match what the code actually does?
  - Are there undisclosed capabilities?

- [ ] **Author/License Validation**
  - Can the author be verified?
  - Is the license appropriate for the code's behavior?

- [ ] **Capability Matching**
  - Do declared capabilities match actual code behavior?
  - Are there hidden features not mentioned?

### 3. Code Block Analysis

For each code block in the SKILL.md:

- [ ] **Language Identification**
  - What language is the code block written in?
  - Is the language appropriate for the stated purpose?

- [ ] **Purpose Assessment**
  - What does this code block demonstrate?
  - Is it an example, instruction, or executable code?

- [ ] **Dangerous Pattern Detection**
  - Check for malicious patterns disguised as examples
  - Verify examples don't contain harmful code
  - Look for social engineering attempts

### 4. Trust Assessment

Evaluate the trustworthiness of the skill source:

- [ ] **Author Reputation**
  - Is this from a known/trusted author?
  - Can you verify the author's identity?
  - Does the author have a track record?

- [ ] **Code Transparency**
  - Is the code well-documented?
  - Are intentions clear and understandable?
  - Is there adequate commenting?

- [ ] **Obfuscation Detection**
  - Are there any obfuscated sections?
  - Is any code unnecessarily complex?
  - Are there unexplained binary or encoded sections?

- [ ] **Permission Scope**
  - Does the skill request excessive permissions?
  - Are requested permissions justified by functionality?

### 5. Suspicious Patterns to Flag

Watch for these red flags:

| Pattern | Risk Level | Example |
|---------|------------|---------|
| Base64/Hex encoded strings | HIGH | `echo "dW5hbQ==" \| base64 -d` |
| Environment variable access | MEDIUM-HIGH | `$API_KEY`, `$AWS_SECRET` |
| Unknown network hosts | HIGH | `curl http://unknown-host.com` |
| Out-of-scope file access | HIGH | `cat /etc/passwd`, `rm -rf /` |
| Dynamic code execution | CRITICAL | `eval "$user_input"` |
| Permission changes | MEDIUM | `chmod 777`, `chown` |
| Cryptographic operations | MEDIUM | Could indicate ransomware |

## Audit Instructions

### Step 1: Read the SKILL.md File

Load and review the complete SKILL.md content to understand the skill's stated purpose and instructions.

### Step 2: Enumerate All Scripts

List all files in the `scripts/` directory and read each one completely.

### Step 3: Systematic Analysis

Work through the checklist above, documenting findings for each item.

### Step 4: Cross-Reference

Compare what the skill claims to do (frontmatter, documentation) with what it actually does (scripts, code).

### Step 5: Generate Security Assessment

Provide a comprehensive report including:

#### Risk Level Classification

| Level | Criteria |
|-------|----------|
| **LOW** | No concerning patterns, well-documented, limited scope |
| **MEDIUM** | Some network/file operations, but justified and transparent |
| **HIGH** | Suspicious patterns, broad permissions, unclear intentions |
| **CRITICAL** | Obvious malicious intent, data exfiltration, system compromise |

#### Report Template

```markdown
## Security Assessment: [Skill Name]

### Risk Level: [LOW/MEDIUM/HIGH/CRITICAL]

### Summary
[Brief overview of findings]

### Findings

#### Critical Issues
- [List critical issues with file:line references]

#### Warnings
- [List warnings with file:line references]

#### Notes
- [List informational notes]

### Recommendations
1. [Specific remediation steps]
2. [Additional recommendations]

### Conclusion
[Safe to use / Use with caution / Do not use]
```

## Example Audit Workflow

1. **Initial Scan**
   ```
   - Read SKILL.md frontmatter
   - List scripts/ directory
   - List references/ directory
   ```

2. **Deep Analysis**
   ```
   - Read each script file
   - Identify all external calls
   - Map data flow
   ```

3. **Risk Assessment**
   ```
   - Categorize findings by severity
   - Determine overall risk level
   - Generate recommendations
   ```

4. **Final Report**
   ```
   - Compile all findings
   - Provide actionable recommendations
   - State clear conclusion
   ```

## Additional Resources

- OWASP Command Injection Prevention
- CWE-78: OS Command Injection
- Shell Script Security Best Practices
