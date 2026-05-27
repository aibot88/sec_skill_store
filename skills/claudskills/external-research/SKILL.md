---
name: "External Research"
description: "Comprehensive external research methodology using web search, URL fetching, and documentation APIs for authoritative, version-aware documentation gathering"
---

# External Research Skill

## Overview

This skill defines the **mandatory methodology** for conducting external research during planning and implementation phases. It ensures that all external knowledge is gathered from authoritative sources, properly validated, version-aware, and correctly cited.

## Why External Research is Critical

### The Problem with Model Memory

Large Language Models have knowledge cutoffs and can hallucinate API details, deprecated patterns, or incorrect version-specific behavior. **Relying solely on model memory for technical implementation details is dangerous and unacceptable.**

Common failure modes when relying on model memory:

| Failure Mode | Example | Consequence |
|--------------|---------|-------------|
| **Outdated APIs** | Using `componentWillMount` in React 18 | Runtime warnings, deprecated code |
| **Version Mismatches** | Assuming FastAPI 0.100+ syntax in 0.95 project | Import errors, crashes |
| **Hallucinated Methods** | Inventing `.toJSON()` on objects that don't have it | Runtime errors |
| **Security Vulnerabilities** | Using outdated authentication patterns | Exploitable code |
| **Incorrect Defaults** | Wrong default parameter values | Subtle bugs |
| **Missing Breaking Changes** | Not knowing about API removals | Production failures |

### The Solution: Verified External Research

By using external research tools, we:

1. **Get current, accurate information** directly from official sources
2. **Verify version compatibility** before writing any code
3. **Discover breaking changes** that model memory doesn't know about
4. **Find security advisories** and best practices
5. **Locate working code examples** from official documentation
6. **Ensure correct API signatures** with proper types and parameters

---

## Research Capabilities

Your environment likely provides these capabilities (tool names vary by platform):

### 1. Web Search (e.g., `search_web`, `@web`, `/web`)

**Purpose**: Discover official documentation, changelogs, breaking changes, security advisories, RFCs, tutorials, and best practices.

**When to Use**:

- Starting research on any external library or framework
- Finding official documentation URLs
- Discovering recent changes, updates, or deprecations
- Locating security advisories or CVEs
- Finding community best practices and patterns
- Researching error messages or edge cases

**Best Practices**:

- Use specific, targeted queries (e.g., "FastAPI 0.110 authentication JWT" not just "FastAPI auth")
- Include version numbers when relevant
- **Include the current year** to filter out outdated content (see Time-Aware Searching below)
- Search for "[library] breaking changes [version]" when upgrading
- Search for "[library] security advisory" for security-sensitive code
- Use the `domain` parameter to prioritize official sources (e.g., `domain: "fastapi.tiangolo.com"`)

**⏰ Time-Aware Searching** (Critical for Relevant Results):

Adding the current year dramatically improves search result relevance:

```
# Without year - may return outdated 2020-2023 content
"FastAPI JWT authentication"

# With year - prioritizes current best practices
"FastAPI JWT authentication 2026"
"React useEffect best practices 2026"
"Python security vulnerabilities 2026"
```

**Why this matters**:

- Libraries update frequently; old tutorials may use deprecated APIs
- Security recommendations evolve constantly
- LLM training data has cutoffs; searching with current year compensates
- Use the script `scripts/get_current_time.py --tips` for query examples

**Query Examples**:

```
Good: "Next.js 14 app router server actions tutorial 2026"
Good: "React 18 useEffect cleanup async 2026"
Good: "Python 3.12 new features type hints"
Bad:  "how to use react"
Bad:  "javascript tutorial"
```

---

### 2. URL Fetching (e.g., `read_url_content`, `WebFetch`, URL Context)

**Purpose**: Fetch and read the actual content of documentation pages, specifications, guides, and reference materials discovered via `search_web`.

**When to Use**:

- After discovering relevant URLs via `search_web`
- Reading official API reference documentation
- Extracting code examples from documentation
- Validating that a URL contains the information you need
- Reading changelogs and migration guides
- Extracting specific parameter details, types, and signatures

**Best Practices**:

- Always read official documentation, not just search snippets
- Extract and note exact API signatures, not paraphrased versions
- Look for code examples you can adapt
- Note any warnings, caveats, or edge cases mentioned
- Check the documentation version matches your target version
- Read multiple sections if needed (installation, usage, API reference)

**What to Extract**:

- Exact function/method signatures with types
- Required vs optional parameters
- Default values
- Return types
- Exception/error types that can be raised
- Code examples (especially official ones)
- Version-specific notes or warnings

---

### 3. Documentation APIs (e.g., `context7 MCP`, library-specific APIs)

**Purpose**: Deep, version-aware framework, SDK, and API knowledge with authoritative context. Provides structured documentation queries with version-specific accuracy.

**Tools Available**:

- `mcp_context7_resolve-library-id`: Resolves a library name to a Context7-compatible ID
- `mcp_context7_query-docs`: Queries documentation for a specific library

**When to Use**:

- When you need version-specific API details
- For deep framework knowledge (React, Next.js, FastAPI, etc.)
- When you need accurate, structured API information
- To verify patterns and best practices for specific versions
- When `search_web` results are too general or scattered

**Best Practices**:

1. **Always resolve the library ID first** using `mcp_context7_resolve-library-id`
2. Use specific, detailed queries (not just "how to use X")
3. Include context about what you're trying to accomplish
4. Reference the version you're targeting
5. Use the returned code examples as authoritative references

**Query Examples**:

```
Good: "How to implement JWT authentication middleware in Express.js 4.x"
Good: "React 18 useEffect cleanup function for async operations"
Good: "FastAPI dependency injection with database sessions"
Bad:  "auth"
Bad:  "database"
```

**Library ID Format**: `/org/project` or `/org/project/version`
Examples:

- `/vercel/next.js`
- `/fastapi/fastapi`
- `/facebook/react`
- `/expressjs/express`

---

## Research Methodology

### Step 1: Identify What Needs Research

Before writing any code that uses external libraries, APIs, or frameworks, identify:

- [ ] All external libraries/packages being used
- [ ] The exact versions of each library
- [ ] Specific features or APIs you'll be using
- [ ] Any integrations between libraries
- [ ] Security-sensitive operations (auth, crypto, etc.)

### Step 2: Conduct Systematic Research

For each external dependency:

1. **Resolve library ID** (if using context7)

   ```
   mcp_context7_resolve-library-id("fastapi", "How to create API endpoints with authentication")
   ```

2. **Query official documentation**

   ```
   mcp_context7_query-docs("/fastapi/fastapi", "JWT authentication with OAuth2PasswordBearer")
   ```

3. **Search for additional context**

   ```
   search_web("FastAPI 0.110 JWT authentication best practices", domain: "fastapi.tiangolo.com")
   ```

4. **Read and validate documentation**

   ```
   read_url_content("https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/")
   ```

### Step 3: Document Your Findings

All research must be documented with:

- **Source URL** with section anchors where possible
- **Version number** the documentation applies to
- **Key findings** relevant to your implementation
- **Code examples** extracted from official sources
- **Warnings/caveats** mentioned in the documentation

---

## What You MUST NOT Rely on Model Memory For

❗ **NEVER** assume model memory is accurate for:

| Category | Why It's Dangerous |
|----------|-------------------|
| **Library APIs** | Methods may be renamed, deprecated, or removed between versions |
| **Function Signatures** | Parameter names, types, and defaults change frequently |
| **Version Compatibility** | What works in v2.0 may not exist in v1.5 |
| **Security Practices** | Security recommendations evolve; old patterns become vulnerabilities |
| **Framework Behavior** | Internal behavior changes even when APIs look the same |
| **Default Values** | Defaults can change between versions, causing subtle bugs |
| **Error Handling** | Exception types and error formats change |
| **Configuration Options** | Config keys are added, renamed, or removed |
| **Environment Variables** | Expected env vars change between versions |
| **Database Schemas** | ORM/database patterns evolve significantly |

---

## Research Validation Checklist

Before considering research complete, verify:

### Discovery Validation

- [ ] All external APIs and libraries were discovered using **search_web**
- [ ] Official documentation URLs were located
- [ ] Version-specific documentation was identified

### Content Validation  

- [ ] All referenced documentation pages were read using **read_url_content**
- [ ] API signatures were extracted accurately (not paraphrased)
- [ ] Code examples were found and noted

### Framework Validation

- [ ] Framework or SDK behavior was validated using **context7 MCP** where applicable
- [ ] Version-specific patterns were confirmed
- [ ] Any framework-specific gotchas were identified

### Accuracy Validation

- [ ] Version numbers are explicitly stated for all dependencies
- [ ] No undocumented or assumed behavior exists in the plan
- [ ] All external knowledge has a citation
- [ ] Security implications were researched if applicable

---

## Citation Format

All externally sourced knowledge **MUST** be cited in your plan or documentation.

### Standard Citation Format

```markdown
### Relevant Documentation

- [FastAPI Security - OAuth2 with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
  - Version: FastAPI 0.110+
  - Key Content: OAuth2PasswordBearer implementation pattern
  - Why Needed: Required for implementing secure token authentication
  - Sourced via: search_web → read_url_content

- [React useEffect Reference](https://react.dev/reference/react/useEffect)
  - Version: React 18.2
  - Key Content: Cleanup function patterns for async operations
  - Why Needed: Prevent memory leaks in component unmount
  - Sourced via: context7 MCP
```

### Version Context

Always include explicit version numbers:

```markdown
✅ Good: "FastAPI v0.110 OAuth2PasswordBearer"
✅ Good: "React 18.2 useEffect cleanup"
✅ Good: "Next.js 14.1 App Router server actions"

❌ Bad: "FastAPI authentication"
❌ Bad: "React hooks"
❌ Bad: "Next.js routing"
```

---

## Common Research Scenarios

### Scenario 1: Implementing a New Feature with External Library

1. Search for official documentation: `search_web("[library] official docs")`
2. Resolve library ID: `mcp_context7_resolve-library-id("[library]", "[your goal]")`
3. Query specific feature: `mcp_context7_query-docs("[library-id]", "[specific feature]")`
4. Read installation/setup guide: `read_url_content("[docs-url]/getting-started")`
5. Read API reference for your use case: `read_url_content("[docs-url]/api/[feature]")`

### Scenario 2: Upgrading a Dependency

1. Search for changelog: `search_web("[library] changelog [version]")`
2. Search for breaking changes: `search_web("[library] breaking changes [old-version] to [new-version]")`
3. Search for migration guide: `search_web("[library] migration guide [version]")`
4. Read migration documentation: `read_url_content("[migration-guide-url]")`

### Scenario 3: Security-Sensitive Code

1. Search for security best practices: `search_web("[library] security best practices [year]")`
2. Search for security advisories: `search_web("[library] CVE security advisory")`
3. Query secure patterns: `mcp_context7_query-docs("[library-id]", "security authentication encryption")`
4. Read security section of docs: `read_url_content("[docs-url]/security")`

### Scenario 4: Debugging/Error Research

1. Search for the specific error: `search_web("[exact error message]")`
2. Search for common causes: `search_web("[library] [error type] common causes")`
3. Read GitHub issues if relevant: `read_url_content("[github-issue-url]")`
4. Query documentation: `mcp_context7_query-docs("[library-id]", "[error context]")`

---

## Integration with Planning Phase

When using this skill during the planning phase (e.g., with the `plan-feature` workflow):

1. **Phase 3 of planning** should leverage all three tools
2. All documentation links in the plan should be sourced via these tools
3. No API details should be assumed—they must be verified
4. The implementation plan should include citations for all external knowledge
5. Validation commands should include research validation as Level 0

### Example Phase 3 Integration

```markdown
### Phase 3: External Research & Documentation

> 📚 **Using External Research Skill**

**Research Conducted:**

1. **context7 MCP**: Queried `/vercel/next.js` for "App Router authentication patterns"
2. **search_web**: Searched "Next.js 14 middleware authentication JWT"
3. **read_url_content**: Read https://nextjs.org/docs/app/building-your-application/authentication

**Findings:**
- Next.js 14 uses middleware.ts for route protection
- JWT validation should happen in middleware, not in page components
- Server actions can access session via cookies() helper

**Citations:**
- [Next.js Authentication Docs](https://nextjs.org/docs/app/building-your-application/authentication) - v14.1
```

---

## Quality Assurance

### Signs of Good Research

✅ Specific version numbers mentioned
✅ Direct links to official documentation
✅ Exact API signatures extracted (not paraphrased)
✅ Code examples from official sources
✅ Warnings and caveats noted
✅ Multiple sources cross-referenced
✅ Clear citation trail (which tool found what)

### Signs of Inadequate Research

❌ Vague statements like "according to the docs"
❌ No version numbers specified
❌ Paraphrased API signatures
❌ No direct documentation links
❌ Assumed behavior without verification
❌ Single source only
❌ No code examples referenced

---

## Summary

External research is not optional—it is a **mandatory requirement** for producing reliable, maintainable, and secure code. The three tools (`search_web`, `read_url_content`, `context7 MCP`) work together to provide:

1. **Discovery** (search_web) → Find where information lives
2. **Validation** (read_url_content) → Read and extract actual content
3. **Deep Context** (context7 MCP) → Get version-specific, structured knowledge

Always research. Always cite. Always verify. Never assume.
