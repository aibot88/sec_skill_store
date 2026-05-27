---
name: "csharp-codeql-cwe"
description: "C# CodeQL analysis patterns and CWE mappings for .NET"
domain: "security"
confidence: "high"
source: "manual — authored from canonical references"
---

## Context

CodeQL is a SAST (Static Application Security Testing) tool that analyses code as data. It finds classes of vulnerability reliably but misses logic flaws, business rule violations, and configuration issues. CodeQL output should be treated as:

- A baseline triage starting point, not a complete security review.
- High-confidence findings for the patterns it covers (injection, path traversal, hardcoded credentials).
- A complement to manual review — not a replacement.

## Best used for

All C#/.NET repositories with CodeQL enabled. Use this skill when triaging CodeQL alerts, reviewing PRs with CodeQL findings, deciding which findings require manual investigation, and understanding what CodeQL does **not** cover.

## Primary references

- GitHub Docs — C# queries for CodeQL: <https://docs.github.com/en/code-security/reference/code-scanning/codeql/codeql-queries/csharp-built-in-queries>
- CodeQL for C#: <https://codeql.github.com/docs/codeql-language-guides/codeql-for-csharp/>
- Microsoft Learn — custom CodeQL queries: <https://learn.microsoft.com/en-us/azure/devops/repos/security/github-advanced-security-code-scanning-queries?view=azure-devops>

## Patterns

### C# CodeQL built-in query categories

Key query suites for C#:

- `csharp-security-extended.qls` — full security query suite.
- `csharp-security-and-quality.qls` — security + code quality.

Individual query categories relevant to review:

| CWE | Category | What CodeQL detects |
|-----|----------|---------------------|
| CWE-89 | SQL Injection | User-controlled data reaching raw SQL (string concatenation in EF Core `FromSqlRaw`, Dapper, ADO.NET) |
| CWE-79 | XSS | User-controlled data reaching HTML output without encoding (Razor raw output, `HtmlString`) |
| CWE-22 | Path Traversal | User-controlled data in file system paths (`Path.Combine`, `File.Open`, `Directory.GetFiles`) |
| CWE-611 | XXE | XML parsing with external entity processing enabled (`XmlDocument`, `XmlReader` with unsafe settings) |
| CWE-502 | Insecure Deserialization | `BinaryFormatter`, `JavaScriptSerializer`, `JsonConvert` with type name handling |
| CWE-327 | Broken Crypto | MD5, SHA-1, DES, RC4 usage; `Random` instead of `RandomNumberGenerator` |
| CWE-312 | Cleartext Storage | Sensitive data written to logs, files, or output without encryption |
| CWE-798 | Hardcoded Credentials | String literals resembling passwords, API keys, connection strings in code |
| CWE-918 | SSRF | User-controlled URLs passed to `HttpClient.GetAsync()`, `WebRequest.Create()` |
| CWE-601 | Open Redirect | User-controlled URLs in `Response.Redirect()`, `LocalRedirect()` without validation |
| CWE-1004 | Missing HttpOnly | Cookie creation without `HttpOnly = true` |

### When a CodeQL finding requires manual review

- **SQL injection (CWE-89):** Always verify — CodeQL finds the data flow but the fix (parameterisation) must be confirmed correct.
- **Path traversal (CWE-22):** Verify the full path normalisation chain — `Path.GetFullPath()` alone is insufficient if the result isn't checked against an allowed root.
- **Insecure deserialization (CWE-502):** `BinaryFormatter` is banned in .NET 8+ by default; older code using it should be flagged Critical. `JsonConvert` with `TypeNameHandling.All` is High regardless.
- **Hardcoded credentials (CWE-798):** Check if the finding is a real credential or a test fixture. Real credentials = Critical.

### When custom query/model work is justified

- Large codebase with custom ORM or query builder: CodeQL needs a model for the custom source/sink.
- Custom serialisation libraries: model the deserialise method as a sink.
- Internal framework with non-standard request handling: model entry points as sources.

### CodeQL in CI/CD (operational fit)

- Run on every PR via `github/codeql-action` — catch new findings before merge.
- `security-extended` query suite for thorough coverage.
- Suppress findings only with documented rationale (`// lgtm[cs/sql-injection]` style annotations are deprecated — use `security-alerts` dismissal in GitHub UI with reason).
- Alert triage: High/Critical CodeQL findings should block merge until reviewed.

## Anti-Patterns

### False-confidence traps — things CodeQL does NOT catch

- **IDOR / missing ownership checks:** CodeQL cannot determine whether a user is authorised to access a specific record.
- **Business logic flaws:** CodeQL does not understand the intended behaviour.
- **Missing authorization:** CodeQL can detect `[AllowAnonymous]` but cannot reason about whether authorization is adequate.
- **Race conditions:** most are not detectable statically.
- **JWT misconfiguration:** CodeQL does not evaluate runtime `TokenValidationParameters`.
- **Second-order injection:** data stored to DB then retrieved and used unsanitised in a later request — CodeQL may not trace the full flow.

### Over-reliance on CodeQL

- Treating a clean CodeQL scan as proof of security.
- Skipping manual review because CodeQL reported no findings.
- Dismissing CodeQL alerts without investigation ("probably a false positive").

## Examples

**CodeQL-detected SQL injection (CWE-89):**

```csharp
// BAD — CodeQL will flag this
var query = $"SELECT * FROM Users WHERE Name = '{userInput}'";
var result = context.Users.FromSqlRaw(query).ToList();

// GOOD — parameterised query
var result = context.Users
    .FromSqlRaw("SELECT * FROM Users WHERE Name = {0}", userInput)
    .ToList();
```

**CodeQL-detected path traversal (CWE-22):**

```csharp
// BAD — CodeQL will flag this
var filePath = Path.Combine(uploadsDir, userFileName);
var content = File.ReadAllText(filePath);

// GOOD — validate resolved path is under allowed root
var filePath = Path.GetFullPath(Path.Combine(uploadsDir, userFileName));
if (!filePath.StartsWith(Path.GetFullPath(uploadsDir) + Path.DirectorySeparatorChar))
    throw new UnauthorizedAccessException();
```

**CodeQL-detected insecure deserialization (CWE-502):**

```csharp
// BAD — BinaryFormatter is banned in .NET 8+
var formatter = new BinaryFormatter();
var obj = formatter.Deserialize(stream);

// BAD — TypeNameHandling.All enables type injection
var obj = JsonConvert.DeserializeObject<Payload>(json,
    new JsonSerializerSettings { TypeNameHandling = TypeNameHandling.All });

// GOOD — System.Text.Json (no type-name handling by default)
var obj = JsonSerializer.Deserialize<Payload>(json);
```

## Review cues

- CodeQL alert on a PR → investigate the full data flow, not just the flagged line.
- Multiple alerts of the same CWE → likely a systemic pattern; recommend a codebase-wide fix.
- Alert dismissed without comment → flag for re-review.
- No CodeQL alerts but manual review finds injection → consider custom query.
- Clean scan on a codebase with complex data flows → verify CodeQL models cover the ORM/framework in use.

## Good looks like

- Every PR is scanned with `csharp-security-extended.qls`.
- High/Critical findings block merge and require documented resolution.
- False positives are dismissed in the GitHub UI with a written rationale, not suppressed in code.
- Manual review complements CodeQL — reviewers check for IDOR, business logic, and authorization gaps that CodeQL cannot detect.
- Custom CodeQL models exist for internal frameworks and ORMs.

## Common findings / likely remediations

| Finding | Severity | Likely remediation |
|---------|----------|--------------------|
| SQL injection via string concatenation in `FromSqlRaw` | Critical | Switch to parameterised overload or use LINQ queries |
| `BinaryFormatter` usage | Critical | Replace with `System.Text.Json` or `MessagePack` |
| `JsonConvert` with `TypeNameHandling.All` | High | Remove `TypeNameHandling` or restrict to `TypeNameHandling.None` |
| Path traversal via `Path.Combine` | High | Validate resolved path starts with allowed root directory |
| Hardcoded connection string with password | High | Move to user-secrets (dev), Key Vault (prod) |
| `XmlDocument` without disabling external entities | High | Set `XmlResolver = null` or use `XmlReaderSettings` with `DtdProcessing.Prohibit` |
| Cookie without `HttpOnly` | Medium | Set `HttpOnly = true` on all session/auth cookies |
| MD5/SHA-1 used for security purposes | Medium | Replace with SHA-256+ or use `RandomNumberGenerator` for nonces |
| User-controlled URL in `HttpClient` call (SSRF) | High | Validate URL against allowlist before making outbound request |
| Open redirect via `Response.Redirect` | Medium | Use `LocalRedirect()` or validate URL is relative/same-origin |
