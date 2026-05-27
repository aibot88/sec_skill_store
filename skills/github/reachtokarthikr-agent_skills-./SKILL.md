# Code Quality Gate Skill

**MANDATORY POST-WRITE CHECKLIST â€” runs after every file is created or modified.**

This skill simulates a professional CI/CD quality gate combining VS Code diagnostics, SonarQube static analysis, vulnerability scanning, security auditing, and performance optimization. It applies to all languages in the stack: T-SQL, C#/.NET, TypeScript/React, HTML/CSS, JSON/config files.

---

## When This Skill Activates

This skill activates **automatically after every code change**. It is not optional.

| Trigger | Example |
|---------|---------|
| New file created | `create_file` for any `.cs`, `.ts`, `.tsx`, `.sql`, `.json`, `.html`, `.css`, `.csproj` |
| File edited | `str_replace` on any code file |
| Bug fix applied | After fixing a reported issue |
| Refactor completed | After restructuring code |
| User says "review" / "check" / "audit" | Explicit quality review request |
| Before delivery to `/mnt/user-data/outputs/` | Final gate before presenting files |

**RULE: Never copy files to `/mnt/user-data/outputs/` until all 6 layers pass with zero Critical/High issues.**

---

## The 6-Layer Quality Gate

Every file change must pass through ALL 6 layers in order. If any layer produces Critical or High severity findings, fix them before proceeding to the next layer. Medium/Low findings should be noted and fixed where practical.

```
Layer 1: VS Code Problems Tab     â†’  Syntax, type errors, warnings
Layer 2: Lint Check (ALL langs)   â†’  ESLint, Roslyn, SQL Lint, Prettier, Stylelint, HTMLHint, JSONLint
Layer 3: SonarQube-Lite Analysis  â†’  Code smells, complexity, duplication, maintainability
Layer 4: Vulnerability Scan       â†’  Dependencies, injection, secrets, data exposure
Layer 5: Security Hardening       â†’  OWASP Top 10, auth/authz, input validation
Layer 6: Optimization & Standards â†’  Performance, best practices, team conventions
```

---

## ARCHITECTURAL MANDATE â€” Stored Procedures ONLY (No Inline SQL, No EF)

**ðŸ”´ CRITICAL RULE â€” NO EXCEPTIONS. This overrides all other patterns. Violations block delivery.**

All database access MUST go through stored procedures called via **Dapper + SpHelper**. The following are **permanently BANNED** in this codebase:

### âŒ BANNED â€” Inline SQL / Raw Queries

```
ðŸ”´ BANNED: conn.QueryAsync<T>("SELECT * FROM Users WHERE Id = @Id", ...)
ðŸ”´ BANNED: conn.ExecuteAsync("INSERT INTO Users (...) VALUES (...)", ...)
ðŸ”´ BANNED: conn.QueryAsync<T>($"SELECT * FROM Users WHERE Email = '{email}'")
ðŸ”´ BANNED: new SqlCommand("SELECT ...", conn)
ðŸ”´ BANNED: SqlCommand.CommandType = CommandType.Text
ðŸ”´ BANNED: FromSqlRaw("SELECT ...")
ðŸ”´ BANNED: FromSqlInterpolated($"SELECT ...")
ðŸ”´ BANNED: Database.ExecuteSqlRaw(...)
ðŸ”´ BANNED: Database.ExecuteSqlInterpolated(...)
ðŸ”´ BANNED: Any string containing SELECT/INSERT/UPDATE/DELETE in C# code
ðŸ”´ BANNED: Dapper calls without CommandType.StoredProcedure â€” must go through SpHelper
```

### âŒ BANNED â€” Entity Framework Core (ALL of it â€” zero tolerance)

```
ðŸ”´ BANNED: DbContext / DbSet<T>
ðŸ”´ BANNED: IEntityTypeConfiguration<T> / Fluent API
ðŸ”´ BANNED: modelBuilder.ApplyConfigurationsFromAssembly(...)
ðŸ”´ BANNED: dbContext.Users.Where(...).ToListAsync()
ðŸ”´ BANNED: dbContext.SaveChangesAsync() / SaveChanges()
ðŸ”´ BANNED: dbContext.Add() / Update() / Remove() / AddRange() / RemoveRange()
ðŸ”´ BANNED: AsNoTracking() (implies EF query)
ðŸ”´ BANNED: Include() / ThenInclude() (EF eager loading)
ðŸ”´ BANNED: EF migrations: dotnet ef migrations add ...
ðŸ”´ BANNED: Microsoft.EntityFrameworkCore NuGet package in any .csproj
ðŸ”´ BANNED: LINQ-to-SQL / LINQ-to-Entities (dbContext.Users.Select(...))
ðŸ”´ BANNED: ExecuteUpdateAsync / ExecuteDeleteAsync (EF 7+ bulk ops)
ðŸ”´ BANNED: HasKey() / HasIndex() / HasOne() / HasMany() / WithOne() / WithMany()
ðŸ”´ BANNED: OnModelCreating() override
ðŸ”´ BANNED: any file named *DbContext.cs, *Context.cs (EF context files)
ðŸ”´ BANNED: Data/Migrations/ folder
```

### âœ… REQUIRED â€” The ONLY Allowed Data Access Pattern

```
âœ… REQUIRED: Dapper + SpHelper â†’ calls stored procedures ONLY
âœ… REQUIRED: CommandType.StoredProcedure on every database call
âœ… REQUIRED: SpHelper.ManageAsync<T>(spName, params)       â†’ INSERT/UPDATE/DELETE via SP
âœ… REQUIRED: SpHelper.GetByIdAsync<T>(spName, id)          â†’ Single record via SP
âœ… REQUIRED: SpHelper.GetListAsync<T>(spName, params)      â†’ Paged list via SP
âœ… REQUIRED: SpHelper.GetWithChildrenAsync<P,C>(spName, id)â†’ Parent+Children via SP
âœ… REQUIRED: DynamicParameters for all SP parameters
âœ… REQUIRED: @CorrelationId + @RequestId injected via SpHelper.WithTracking()
âœ… REQUIRED: Every SP defined in .sql files following _Manage / _Get pattern
âœ… REQUIRED: Repository classes use SpHelper, never direct Dapper or ADO.NET
```

### âœ… Required NuGet Packages (Data Access ONLY these)

```xml
<!-- ALLOWED â€” the ONLY data access packages -->
<PackageReference Include="Dapper" Version="2.*" />
<PackageReference Include="Microsoft.Data.SqlClient" Version="5.*" />

<!-- âŒ BANNED â€” if any of these appear in .csproj, it is a CRITICAL violation -->
<!-- <PackageReference Include="Microsoft.EntityFrameworkCore" /> -->
<!-- <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" /> -->
<!-- <PackageReference Include="Microsoft.EntityFrameworkCore.Design" /> -->
<!-- <PackageReference Include="Microsoft.EntityFrameworkCore.Tools" /> -->
<!-- <PackageReference Include="Microsoft.EntityFrameworkCore.Relational" /> -->
<!-- <PackageReference Include="Microsoft.EntityFrameworkCore.InMemory" /> -->
```

### Detection Commands (MUST run on every C# / .csproj file change)

```bash
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo "   SP-ONLY MANDATE CHECK â€” ZERO TOLERANCE"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
VIOLATIONS=0

# â”€â”€ Inline SQL detection (ðŸ”´ CRITICAL) â”€â”€
echo "--- Checking for inline SQL ---"

if grep -rn "CommandType\.Text" --include="*.cs" 2>/dev/null; then
  echo "ðŸ”´ CRITICAL: CommandType.Text found â€” must use CommandType.StoredProcedure"
  ((VIOLATIONS++))
fi

if grep -rn "FromSqlRaw\|FromSqlInterpolated\|ExecuteSqlRaw\|ExecuteSqlInterpolated" --include="*.cs" 2>/dev/null; then
  echo "ðŸ”´ CRITICAL: Raw SQL via EF methods found"
  ((VIOLATIONS++))
fi

if grep -rn '"SELECT \|"INSERT \|"UPDATE \|"DELETE \|"EXEC ' --include="*.cs" 2>/dev/null; then
  echo "ðŸ”´ CRITICAL: Inline SQL string found in C# code"
  ((VIOLATIONS++))
fi

if grep -rn '\$"SELECT\|\$"INSERT\|\$"UPDATE\|\$"DELETE' --include="*.cs" 2>/dev/null; then
  echo "ðŸ”´ CRITICAL: Interpolated SQL string found â€” SQL injection risk"
  ((VIOLATIONS++))
fi

if grep -rn "new SqlCommand" --include="*.cs" 2>/dev/null; then
  echo "ðŸ”´ CRITICAL: Raw SqlCommand found â€” must use SpHelper"
  ((VIOLATIONS++))
fi

# Direct Dapper without SP type (allowed only inside SpHelper itself)
if grep -rn "\.QueryAsync<\|\.QueryFirstOrDefaultAsync<\|\.ExecuteAsync(" --include="*.cs" 2>/dev/null | grep -v "SpHelper.cs" | grep -v "CommandType.StoredProcedure"; then
  echo "ðŸ”´ CRITICAL: Direct Dapper call outside SpHelper â€” must go through SpHelper"
  ((VIOLATIONS++))
fi

# â”€â”€ Entity Framework detection (ðŸ”´ CRITICAL) â”€â”€
echo "--- Checking for Entity Framework ---"

if grep -rn "DbContext\|DbSet<" --include="*.cs" 2>/dev/null; then
  echo "ðŸ”´ CRITICAL: Entity Framework DbContext/DbSet found"
  ((VIOLATIONS++))
fi

if grep -rn "using Microsoft.EntityFrameworkCore" --include="*.cs" 2>/dev/null; then
  echo "ðŸ”´ CRITICAL: EF Core using directive found"
  ((VIOLATIONS++))
fi

if grep -rn "EntityFrameworkCore" --include="*.csproj" 2>/dev/null; then
  echo "ðŸ”´ CRITICAL: EF Core NuGet package referenced in .csproj"
  ((VIOLATIONS++))
fi

if grep -rn "\.Include(\|\.ThenInclude(" --include="*.cs" 2>/dev/null; then
  echo "ðŸ”´ CRITICAL: EF eager loading (Include/ThenInclude) found"
  ((VIOLATIONS++))
fi

if grep -rn "AsNoTracking\|SaveChangesAsync\|SaveChanges()" --include="*.cs" 2>/dev/null; then
  echo "ðŸ”´ CRITICAL: EF persistence method found"
  ((VIOLATIONS++))
fi

if grep -rn "modelBuilder\|OnModelCreating\|IEntityTypeConfiguration\|HasKey(\|HasIndex(\|HasOne(\|HasMany(" --include="*.cs" 2>/dev/null; then
  echo "ðŸ”´ CRITICAL: EF model configuration / Fluent API found"
  ((VIOLATIONS++))
fi

if grep -rn "ExecuteUpdateAsync\|ExecuteDeleteAsync" --include="*.cs" 2>/dev/null; then
  echo "ðŸ”´ CRITICAL: EF bulk operation found"
  ((VIOLATIONS++))
fi

if find . -name "*DbContext.cs" -o -name "*Context.cs" 2>/dev/null | grep -v "TrackingContext\|HttpContext\|LogContext"; then
  echo "ðŸ”´ CRITICAL: EF Context file found"
  ((VIOLATIONS++))
fi

if [ -d "Data/Migrations" ] || [ -d "Migrations" ]; then
  echo "ðŸ”´ CRITICAL: EF Migrations folder found"
  ((VIOLATIONS++))
fi

# â”€â”€ Verify correct pattern exists â”€â”€
echo "--- Verifying SP-only pattern ---"
grep -rn "CommandType.StoredProcedure" --include="*.cs" 2>/dev/null && echo "âœ… StoredProcedure CommandType found" || echo "âš ï¸ No StoredProcedure calls found"
grep -rn "class SpHelper" --include="*.cs" 2>/dev/null && echo "âœ… SpHelper class found" || echo "âš ï¸ SpHelper not found â€” required"
grep -rn "DynamicParameters" --include="*.cs" 2>/dev/null && echo "âœ… DynamicParameters usage found" || echo "âš ï¸ No DynamicParameters found"
grep -rn "WithTracking" --include="*.cs" 2>/dev/null && echo "âœ… WithTracking (CorrelationId/RequestId injection) found" || echo "âš ï¸ WithTracking not found â€” tracking IDs may be missing"

echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
if [ $VIOLATIONS -gt 0 ]; then
  echo "âŒ SP-ONLY MANDATE: $VIOLATIONS CRITICAL VIOLATIONS â€” DELIVERY BLOCKED"
else
  echo "âœ… SP-ONLY MANDATE: PASSED â€” all data access through stored procedures"
fi
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
```

### Why This Mandate Exists

| Concern | Stored Procedures (âœ… our way) | Inline SQL / EF (âŒ banned) |
|---------|-------------------------------|----------------------------|
| **SQL Injection** | Parameterized by design | Risky string interpolation |
| **Performance** | Cached execution plans, DBA-tunable | Plan recompilation, N+1 queries, lazy loading traps |
| **Request Tracking** | @CorrelationId/@RequestId in every SP call | No tracking â€” invisible to log.RequestLog |
| **Audit Trail** | SP logs START/SUCCESS/ERROR automatically | Changes happen silently, no audit |
| **DBA Control** | DBAs tune queries without code deploys | Locked in compiled C# code |
| **Soft Delete** | Enforced in SP (IsActive = 0, always) | Dev might forget, hard-delete data permanently |
| **Business Logic** | Centralized in SP + service layer | Scattered across EF configs, LINQ, migrations |
| **Schema Changes** | Idempotent .sql scripts, version-controlled | EF migration conflicts, snapshot drift |
| **Consistency** | Same _Manage/_Get pattern everywhere | Mixed patterns, every dev does it differently |
| **Debugging** | grep log.RequestLog by RequestId | No centralized logging, hunt through app logs |

### Correct Architecture Flow

```
React (UI) â†’ API Controller â†’ Service (optional) â†’ Repository â†’ SpHelper â†’ Dapper â†’ Stored Procedure â†’ SQL Server
                                                      â†‘
                                              Uses DynamicParameters
                                              Injects @CorrelationId + @RequestId
                                              CommandType.StoredProcedure ALWAYS
```

**Every data operation follows this chain. No shortcuts. No "just a quick EF query". No "inline SQL is faster for this one case".**

---

## Layer 1 â€” VS Code Problems Tab Simulation

Simulate what VS Code's Problems tab would show: Errors, Warnings, and Information diagnostics. Check every changed file.

### For ALL Languages

| Check | Severity | What to Look For |
|-------|----------|------------------|
| Syntax errors | ðŸ”´ Error | Missing brackets, semicolons, unclosed strings, invalid tokens |
| Undefined references | ðŸ”´ Error | Variables, functions, types, tables used but never declared |
| Type mismatches | ðŸ”´ Error | Assigning string to int, wrong function argument types |
| Unused imports/usings | ðŸŸ¡ Warning | `using System.Linq;` when no LINQ is used |
| Unused variables | ðŸŸ¡ Warning | Declared but never read |
| Unreachable code | ðŸŸ¡ Warning | Code after `return`, `throw`, `RETURN` |
| Deprecated API usage | ðŸŸ¡ Warning | `DateTime` instead of `DateTime2`, `TEXT` instead of `NVARCHAR(MAX)` |
| Missing null checks | ðŸŸ¡ Warning | Nullable types accessed without `?.` or null guard |
| Implicit `any` (TypeScript) | ðŸŸ¡ Warning | Untyped parameters, missing return types |
| Missing `await` | ðŸ”´ Error | Async call without `await` â€” fire-and-forget bug |

### Language-Specific Checks

#### T-SQL
```
âœ… All identifiers resolved (tables, columns, SPs exist or are in context)
âœ… Matching BEGIN/END blocks
âœ… SET NOCOUNT ON present in every SP
âœ… SET XACT_ABORT ON present in _Manage SPs
âœ… GO batch separators between CREATE/ALTER statements
âœ… No SELECT * in production code (list columns explicitly)
âœ… All CASE expressions have matching END
âœ… String literals use N'' prefix for NVARCHAR columns
âœ… No orphaned temp tables (created but never dropped or used)
âœ… THROW has correct 3-param syntax (number, message, state)
```

#### C# / .NET
```
âœ… Namespace matches folder structure
âœ… All interfaces implemented fully
âœ… All abstract methods overridden
âœ… async methods return Task/Task<T>, not void (except event handlers)
âœ… IDisposable types wrapped in using/await using
âœ… No raw Task.Result or .Wait() (deadlock risk)
âœ… CancellationToken accepted and forwarded in async chains
âœ… Nullable reference types handled (no CS8600, CS8601, CS8602 warnings)
âœ… Constructor parameters match DI registrations
âœ… No ambiguous method overloads
ðŸ”´ NO inline SQL strings (SELECT/INSERT/UPDATE/DELETE in C# code)
ðŸ”´ NO Entity Framework (DbContext, DbSet, SaveChanges, Include, migrations)
ðŸ”´ NO raw SqlCommand or CommandType.Text
ðŸ”´ ALL data access through SpHelper â†’ Stored Procedures â†’ Dapper
ðŸ”´ NO EF NuGet packages in .csproj (EntityFrameworkCore.*)
```

#### TypeScript / React
```
âœ… No TypeScript strict mode violations (noImplicitAny, strictNullChecks)
âœ… All imports resolve to existing modules
âœ… JSX elements have matching closing tags
âœ… React hooks follow Rules of Hooks (no conditional hooks, correct deps)
âœ… useEffect cleanup functions present where needed (subscriptions, timers, AbortController)
âœ… Key prop present on mapped elements
âœ… No direct DOM manipulation (use refs instead)
âœ… Event handlers typed correctly (React.ChangeEvent<HTMLInputElement>, etc.)
âœ… Generic type parameters specified (no implicit any on useState<>, useRef<>)
âœ… Exported types match their usage in consuming modules
```

### Validation Commands (run where applicable)

```bash
# TypeScript â€” compile check
npx tsc --noEmit 2>&1 | head -50

# ESLint
npx eslint . --ext .ts,.tsx --format compact 2>&1 | head -50

# .NET build
dotnet build --no-restore 2>&1 | grep -E "(error|warning) [A-Z]{2}[0-9]+" | head -50

# SQL syntax (basic)
# Use sqlcmd dry-run or grep for common syntax errors
grep -n "SELECT \*" *.sql           # No SELECT * in production
grep -n "GETDATE()" *.sql           # Should use SYSUTCDATETIME()
grep -n "= NULL" *.sql              # Should use IS NULL
grep -n "EXEC(" *.sql               # Check for SQL injection in dynamic SQL
```

### Output Format

```
## Layer 1 â€” VS Code Problems Tab
| # | File | Line | Severity | Code | Message |
|---|------|------|----------|------|---------|
| 1 | Users_Manage.sql | 45 | ðŸ”´ Error | SQL001 | Missing SET NOCOUNT ON |
| 2 | UserService.cs | 12 | ðŸŸ¡ Warning | CS8602 | Possible null reference |
| 3 | api.ts | 8 | ðŸŸ¡ Warning | TS6133 | 'response' declared but never used |

**Result: âŒ 1 Error, 2 Warnings â€” fix errors before proceeding**
```

---

## Layer 2 â€” Lint Check (ALL Languages)

**MANDATORY for every file.** Run the appropriate linter for each file type. Fix all errors; warnings should be fixed unless explicitly justified. This layer catches style violations, anti-patterns, and code quality issues that compilers don't flag.

### Installation Commands (run once per session if needed)

```bash
# â”€â”€ TypeScript / React / JavaScript â”€â”€
npm install -D eslint @eslint/js typescript-eslint eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-jsx-a11y 2>/dev/null
npm install -D prettier eslint-config-prettier eslint-plugin-prettier 2>/dev/null

# â”€â”€ CSS / SCSS â”€â”€
npm install -D stylelint stylelint-config-standard stylelint-config-tailwindcss 2>/dev/null

# â”€â”€ HTML â”€â”€
npm install -D htmlhint 2>/dev/null

# â”€â”€ JSON â”€â”€
npm install -D jsonlint-mod 2>/dev/null

# â”€â”€ Markdown â”€â”€
npm install -D markdownlint-cli 2>/dev/null

# â”€â”€ SQL (T-SQL) â”€â”€
npm install -D sql-lint 2>/dev/null
pip install sqlfluff --break-system-packages 2>/dev/null

# â”€â”€ C# / .NET (Roslyn analyzers â€” included in SDK 8+) â”€â”€
# These are built into dotnet build with <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
# Additional: dotnet format for auto-fix
```

---

### 2.1 TypeScript / React â€” ESLint + Prettier

#### Rules (Error = ðŸ”´, Warning = ðŸŸ¡)

| Rule ID | Severity | What It Catches |
|---------|----------|-----------------|
| `@typescript-eslint/no-explicit-any` | ðŸ”´ Error | Using `any` type â€” use `unknown` and narrow |
| `@typescript-eslint/no-unused-vars` | ðŸ”´ Error | Variables/imports declared but never used |
| `@typescript-eslint/no-non-null-assertion` | ðŸŸ¡ Warning | Using `!` non-null assertion â€” prefer optional chaining `?.` |
| `@typescript-eslint/explicit-function-return-type` | ðŸŸ¡ Warning | Public functions missing return type annotation |
| `@typescript-eslint/no-floating-promises` | ðŸ”´ Error | Async call without `await` or `.catch()` â€” fire-and-forget bug |
| `@typescript-eslint/no-misused-promises` | ðŸ”´ Error | Passing async function where sync callback expected |
| `@typescript-eslint/strict-boolean-expressions` | ðŸŸ¡ Warning | Truthy check on non-boolean: `if (str)` instead of `if (str !== '')` |
| `@typescript-eslint/consistent-type-imports` | ðŸŸ¡ Warning | `import type { X }` for type-only imports |
| `@typescript-eslint/no-unnecessary-condition` | ðŸŸ¡ Warning | Condition is always true/false â€” dead code |
| `@typescript-eslint/prefer-nullish-coalescing` | ðŸŸ¡ Warning | Use `??` instead of `\|\|` for null/undefined checks |
| `@typescript-eslint/no-unsafe-assignment` | ðŸ”´ Error | Assigning `any` typed value to typed variable |
| `@typescript-eslint/no-unsafe-member-access` | ðŸ”´ Error | Accessing properties on `any` typed value |
| `@typescript-eslint/no-unsafe-call` | ðŸ”´ Error | Calling `any` typed value as function |
| `@typescript-eslint/no-unsafe-return` | ðŸ”´ Error | Returning `any` from typed function |
| `react/jsx-no-target-blank` | ðŸ”´ Error | `<a target="_blank">` without `rel="noopener noreferrer"` |
| `react/no-array-index-key` | ðŸŸ¡ Warning | Using array index as `key` prop â€” unstable on reorder |
| `react-hooks/rules-of-hooks` | ðŸ”´ Error | Hooks called conditionally or inside loops |
| `react-hooks/exhaustive-deps` | ðŸŸ¡ Warning | Missing dependencies in useEffect/useMemo/useCallback |
| `react/no-danger` | ðŸ”´ Error | Using `dangerouslySetInnerHTML` â€” XSS risk |
| `react/jsx-no-constructed-context-values` | ðŸŸ¡ Warning | Object literal in Context.Provider value â€” re-renders children |
| `react/no-unstable-nested-components` | ðŸŸ¡ Warning | Component defined inside render â€” unmounts/remounts every render |
| `jsx-a11y/alt-text` | ðŸ”´ Error | `<img>` without `alt` attribute |
| `jsx-a11y/click-events-have-key-events` | ðŸŸ¡ Warning | `onClick` without `onKeyDown`/`onKeyUp` |
| `jsx-a11y/no-autofocus` | ðŸŸ¡ Warning | `autoFocus` disrupts screen reader flow |
| `jsx-a11y/anchor-is-valid` | ðŸŸ¡ Warning | `<a>` without valid `href` â€” use `<button>` instead |
| `no-console` | ðŸŸ¡ Warning | `console.log` left in production code |
| `no-debugger` | ðŸ”´ Error | `debugger` statement in production code |
| `no-var` | ðŸ”´ Error | Using `var` â€” use `const` or `let` |
| `prefer-const` | ðŸŸ¡ Warning | `let` when variable is never reassigned |
| `eqeqeq` | ðŸ”´ Error | `==` / `!=` instead of `===` / `!==` |
| `no-eval` | ðŸ”´ Error | `eval()` â€” code injection risk |
| `no-implied-eval` | ðŸ”´ Error | `setTimeout("code")` â€” hidden eval |
| `curly` | ðŸŸ¡ Warning | If/else/for/while without braces |

#### ESLint Config (eslint.config.mjs â€” flat config)

```javascript
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import jsxA11y from 'eslint-plugin-jsx-a11y';
import prettier from 'eslint-config-prettier';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  ...tseslint.configs.stylisticTypeChecked,
  {
    plugins: { react, 'react-hooks': reactHooks, 'jsx-a11y': jsxA11y },
    rules: {
      // â”€â”€ TypeScript â”€â”€
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/no-floating-promises': 'error',
      '@typescript-eslint/no-misused-promises': 'error',
      '@typescript-eslint/consistent-type-imports': 'warn',
      '@typescript-eslint/prefer-nullish-coalescing': 'warn',
      '@typescript-eslint/strict-boolean-expressions': 'warn',
      '@typescript-eslint/no-non-null-assertion': 'warn',
      '@typescript-eslint/explicit-function-return-type': ['warn', { allowExpressions: true }],
      '@typescript-eslint/no-unnecessary-condition': 'warn',
      '@typescript-eslint/no-unsafe-assignment': 'error',
      '@typescript-eslint/no-unsafe-member-access': 'error',
      '@typescript-eslint/no-unsafe-call': 'error',
      '@typescript-eslint/no-unsafe-return': 'error',

      // â”€â”€ React â”€â”€
      'react/jsx-no-target-blank': 'error',
      'react/no-array-index-key': 'warn',
      'react/no-danger': 'error',
      'react/jsx-no-constructed-context-values': 'warn',
      'react/no-unstable-nested-components': 'warn',
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',

      // â”€â”€ Accessibility â”€â”€
      'jsx-a11y/alt-text': 'error',
      'jsx-a11y/click-events-have-key-events': 'warn',
      'jsx-a11y/no-autofocus': 'warn',
      'jsx-a11y/anchor-is-valid': 'warn',

      // â”€â”€ General JS â”€â”€
      'no-console': 'warn',
      'no-debugger': 'error',
      'no-var': 'error',
      'prefer-const': 'warn',
      'eqeqeq': ['error', 'always'],
      'no-eval': 'error',
      'no-implied-eval': 'error',
      'curly': ['warn', 'all'],
    },
    languageOptions: {
      parserOptions: {
        project: true,
        ecmaFeatures: { jsx: true },
      },
    },
    settings: { react: { version: 'detect' } },
  },
  prettier, // Must be last â€” disables formatting rules that conflict with Prettier
);
```

#### Prettier Config (.prettierrc)

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "bracketSpacing": true,
  "jsxSingleQuote": false,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

#### Run Commands

```bash
# Lint check (report only)
npx eslint . --ext .ts,.tsx,.js,.jsx --format stylish 2>&1

# Lint auto-fix
npx eslint . --ext .ts,.tsx,.js,.jsx --fix 2>&1

# Prettier check
npx prettier --check "src/**/*.{ts,tsx,js,jsx,json,css,md}" 2>&1

# Prettier auto-fix
npx prettier --write "src/**/*.{ts,tsx,js,jsx,json,css,md}" 2>&1

# Combined: lint + format check
npx eslint . --ext .ts,.tsx && npx prettier --check "src/**/*.{ts,tsx}"
```

---

### 2.2 C# / .NET â€” Roslyn Analyzers + dotnet-format + EditorConfig

#### Rules (Error = ðŸ”´, Warning = ðŸŸ¡)

| Rule ID | Severity | What It Catches |
|---------|----------|-----------------|
| `CA1001` | ðŸ”´ Error | Type owns disposable field but doesn't implement IDisposable |
| `CA1031` | ðŸŸ¡ Warning | Catching general `Exception` â€” catch specific types |
| `CA1032` | ðŸŸ¡ Warning | Custom exception missing standard constructors |
| `CA1054` | ðŸŸ¡ Warning | URI parameter should be `System.Uri`, not `string` |
| `CA1062` | ðŸ”´ Error | Validate public method arguments for null |
| `CA1063` | ðŸ”´ Error | Implement IDisposable correctly (Dispose pattern) |
| `CA1303` | ðŸŸ¡ Warning | String literal in exception/UI â€” consider resource file for i18n |
| `CA1304` | ðŸŸ¡ Warning | Missing `CultureInfo` or `StringComparison` on string operations |
| `CA1305` | ðŸŸ¡ Warning | Missing `IFormatProvider` â€” use `CultureInfo.InvariantCulture` |
| `CA1707` | ðŸŸ¡ Warning | Identifier contains underscore (non-standard naming) |
| `CA1716` | ðŸŸ¡ Warning | Identifier matches reserved language keyword |
| `CA1812` | ðŸŸ¡ Warning | Internal class never instantiated â€” dead code? |
| `CA1822` | ðŸŸ¡ Warning | Method doesn't access instance data â€” make `static` |
| `CA1848` | ðŸŸ¡ Warning | Use `LoggerMessage.Define` for high-perf logging |
| `CA1860` | ðŸŸ¡ Warning | Prefer `Length > 0` over `Any()` for collections |
| `CA2000` | ðŸ”´ Error | Dispose objects before losing scope |
| `CA2007` | ðŸŸ¡ Warning | Missing `ConfigureAwait(false)` in library code |
| `CA2016` | ðŸ”´ Error | Forward `CancellationToken` to methods that accept it |
| `CA2100` | ðŸ”´ Error | SQL command text from variable â€” SQL injection risk |
| `CA2213` | ðŸ”´ Error | Disposable fields should be disposed |
| `CA2227` | ðŸŸ¡ Warning | Collection property has setter â€” remove setter, use init or readonly |
| `CA2241` | ðŸ”´ Error | Format string argument count mismatch |
| `CA2254` | ðŸŸ¡ Warning | Log message template should not vary between calls |
| `IDE0003` | ðŸŸ¡ Warning | `this.` qualification unnecessary â€” remove |
| `IDE0005` | ðŸŸ¡ Warning | Unnecessary `using` directive â€” remove |
| `IDE0011` | ðŸŸ¡ Warning | Add braces to `if`/`else`/`for`/`while` |
| `IDE0044` | ðŸŸ¡ Warning | Private field can be `readonly` |
| `IDE0055` | ðŸŸ¡ Warning | Formatting rule violation (indentation, spacing) |
| `IDE0058` | â„¹ï¸ Info | Expression value is never used |
| `IDE0060` | ðŸŸ¡ Warning | Unused parameter â€” remove or prefix with `_` |
| `IDE0063` | ðŸŸ¡ Warning | Use simple `using` declaration instead of `using` block |
| `IDE0066` | ðŸŸ¡ Warning | Use switch expression instead of switch statement |
| `IDE0090` | ðŸŸ¡ Warning | Use `new()` target-typed expression |
| `CS8600` | ðŸ”´ Error | Converting null literal to non-nullable type |
| `CS8601` | ðŸ”´ Error | Possible null reference assignment |
| `CS8602` | ðŸ”´ Error | Dereference of possibly null reference |
| `CS8604` | ðŸ”´ Error | Possible null reference argument for parameter |
| `CS8618` | ðŸ”´ Error | Non-nullable property must contain non-null when exiting constructor |
| `CS8625` | ðŸ”´ Error | Cannot convert null literal to non-nullable reference type |
| `ASP0014` | ðŸŸ¡ Warning | Suggest using top-level route registrations |
| `ASP0019` | ðŸŸ¡ Warning | Suggest using IHeaderDictionary.Append |
| **SP-ONLY MANDATE RULES** | | |
| `SP001` | ðŸ”´ Error | **Inline SQL detected** â€” any SELECT/INSERT/UPDATE/DELETE string in C# code |
| `SP002` | ðŸ”´ Error | **Entity Framework detected** â€” DbContext, DbSet, using EF namespace, EF NuGet package |
| `SP003` | ðŸ”´ Error | **Raw SqlCommand** â€” new SqlCommand() or CommandType.Text found |
| `SP004` | ðŸ”´ Error | **Direct Dapper outside SpHelper** â€” Dapper calls must go through SpHelper only |
| `SP005` | ðŸ”´ Error | **EF NuGet reference** â€” EntityFrameworkCore in .csproj |
| `SP006` | ðŸ”´ Error | **EF migration** â€” Migrations folder, dotnet ef command, Add-Migration |
| `SP007` | ðŸ”´ Error | **EF Fluent API** â€” modelBuilder, HasKey, HasOne, OnModelCreating |
| `SP008` | ðŸ”´ Error | **EF persistence** â€” SaveChanges, SaveChangesAsync, Add(), Update(), Remove() on context |
| `SP009` | ðŸ”´ Error | **EF query operators** â€” Include(), ThenInclude(), AsNoTracking() on context |
| `SP010` | ðŸ”´ Error | **FromSqlRaw / ExecuteSqlRaw** â€” raw SQL through EF methods |
| `SP011` | ðŸŸ¡ Warning | **Missing SpHelper** â€” Repository class has no SpHelper dependency |
| `SP012` | ðŸŸ¡ Warning | **Missing WithTracking** â€” SP call without CorrelationId/RequestId injection |
| `ASP0019` | ðŸŸ¡ Warning | Suggest using IHeaderDictionary.Append |

#### .editorconfig (place in solution root)

```ini
root = true

# â”€â”€ All files â”€â”€
[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

# â”€â”€ C# files â”€â”€
[*.cs]
# Formatting
csharp_new_line_before_open_brace = all
csharp_new_line_before_else = true
csharp_new_line_before_catch = true
csharp_new_line_before_finally = true
csharp_indent_case_contents = true
csharp_indent_switch_labels = true
csharp_space_after_cast = false
csharp_style_var_for_built_in_types = true:suggestion
csharp_style_var_when_type_is_apparent = true:suggestion

# Naming: private fields _camelCase
dotnet_naming_rule.private_fields_should_be_camel_case.symbols = private_fields
dotnet_naming_rule.private_fields_should_be_camel_case.style = camel_case_underscore
dotnet_naming_rule.private_fields_should_be_camel_case.severity = warning
dotnet_naming_symbols.private_fields.applicable_kinds = field
dotnet_naming_symbols.private_fields.applicable_accessibilities = private
dotnet_naming_style.camel_case_underscore.required_prefix = _
dotnet_naming_style.camel_case_underscore.capitalization = camel_case

# Naming: interfaces I prefix
dotnet_naming_rule.interfaces_begin_with_i.symbols = interfaces
dotnet_naming_rule.interfaces_begin_with_i.style = begins_with_i
dotnet_naming_rule.interfaces_begin_with_i.severity = error
dotnet_naming_symbols.interfaces.applicable_kinds = interface
dotnet_naming_style.begins_with_i.required_prefix = I
dotnet_naming_style.begins_with_i.capitalization = pascal_case

# Naming: async methods end with Async
dotnet_naming_rule.async_methods_end_with_async.symbols = async_methods
dotnet_naming_rule.async_methods_end_with_async.style = ends_with_async
dotnet_naming_rule.async_methods_end_with_async.severity = warning
dotnet_naming_symbols.async_methods.applicable_kinds = method
dotnet_naming_symbols.async_methods.required_modifiers = async
dotnet_naming_style.ends_with_async.required_suffix = Async
dotnet_naming_style.ends_with_async.capitalization = pascal_case

# Code quality
dotnet_diagnostic.CA1001.severity = error
dotnet_diagnostic.CA1062.severity = error
dotnet_diagnostic.CA1063.severity = error
dotnet_diagnostic.CA2000.severity = error
dotnet_diagnostic.CA2016.severity = error
dotnet_diagnostic.CA2100.severity = error
dotnet_diagnostic.CA2213.severity = error
dotnet_diagnostic.CA1031.severity = warning
dotnet_diagnostic.CA1822.severity = warning
dotnet_diagnostic.IDE0005.severity = warning
dotnet_diagnostic.IDE0044.severity = warning
dotnet_diagnostic.IDE0060.severity = warning

# Nullable reference types
dotnet_diagnostic.CS8600.severity = error
dotnet_diagnostic.CS8601.severity = error
dotnet_diagnostic.CS8602.severity = error
dotnet_diagnostic.CS8604.severity = error
dotnet_diagnostic.CS8618.severity = error

# â”€â”€ SQL files â”€â”€
[*.sql]
indent_size = 4
indent_style = space

# â”€â”€ TypeScript / JavaScript â”€â”€
[*.{ts,tsx,js,jsx}]
indent_size = 2

# â”€â”€ JSON â”€â”€
[*.json]
indent_size = 2

# â”€â”€ YAML â”€â”€
[*.{yml,yaml}]
indent_size = 2

# â”€â”€ Markdown â”€â”€
[*.md]
trim_trailing_whitespace = false
```

#### .csproj Analyzer Configuration

```xml
<PropertyGroup>
  <TargetFramework>net8.0</TargetFramework>
  <Nullable>enable</Nullable>
  <ImplicitUsings>enable</ImplicitUsings>
  <TreatWarningsAsErrors>false</TreatWarningsAsErrors>
  <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
  <AnalysisLevel>latest-recommended</AnalysisLevel>
  <EnableNETAnalyzers>true</EnableNETAnalyzers>
</PropertyGroup>
```

#### Run Commands

```bash
# Full build with analyzers (catches Roslyn + nullable + style)
dotnet build --no-restore -warnaserror 2>&1 | head -80

# Format check (dry run â€” reports violations)
dotnet format --verify-no-changes --verbosity diagnostic 2>&1 | head -50

# Format auto-fix
dotnet format 2>&1

# Specific analyzer check
dotnet build /p:EnforceCodeStyleInBuild=true /p:AnalysisLevel=latest-all 2>&1 | grep -E "(error|warning) (CA|CS|IDE|ASP)" | head -50
```

---

### 2.3 T-SQL â€” SQL Lint Rules

#### Rules (Error = ðŸ”´, Warning = ðŸŸ¡)

| Rule ID | Severity | What It Catches |
|---------|----------|-----------------|
| `SQL001` | ðŸ”´ Error | Missing `SET NOCOUNT ON` in stored procedure |
| `SQL002` | ðŸ”´ Error | Missing `SET XACT_ABORT ON` in write procedures (_Manage) |
| `SQL003` | ðŸ”´ Error | `SELECT *` used in production query â€” list columns explicitly |
| `SQL004` | ðŸ”´ Error | `= NULL` comparison â€” must use `IS NULL` / `IS NOT NULL` |
| `SQL005` | ðŸ”´ Error | `GETDATE()` used â€” must use `SYSUTCDATETIME()` for UTC |
| `SQL006` | ðŸ”´ Error | `DATETIME` data type used â€” must use `DATETIME2` |
| `SQL007` | ðŸ”´ Error | Dynamic SQL with string concatenation â€” SQL injection risk |
| `SQL008` | ðŸŸ¡ Warning | Missing `N''` prefix for NVARCHAR string literals |
| `SQL009` | ðŸŸ¡ Warning | Missing explicit constraint names (PK_, FK_, UQ_, DF_, CK_) |
| `SQL010` | ðŸŸ¡ Warning | Missing `GO` batch separator between DDL statements |
| `SQL011` | ðŸŸ¡ Warning | Missing `IF NOT EXISTS` guard on CREATE TABLE/INDEX |
| `SQL012` | ðŸŸ¡ Warning | Missing index on foreign key column |
| `SQL013` | ðŸŸ¡ Warning | `NOLOCK` hint used â€” prefer RCSI at database level |
| `SQL014` | ðŸŸ¡ Warning | Unqualified column names in multi-table query (missing table alias) |
| `SQL015` | ðŸŸ¡ Warning | `TOP` without `ORDER BY` â€” non-deterministic results |
| `SQL016` | ðŸŸ¡ Warning | `IN` subquery â€” prefer `EXISTS` for correlated subqueries |
| `SQL017` | ðŸŸ¡ Warning | `MONEY` / `FLOAT` for currency â€” use `DECIMAL(19,4)` |
| `SQL018` | ðŸŸ¡ Warning | `TEXT` / `IMAGE` deprecated types â€” use `NVARCHAR(MAX)` / `VARBINARY(MAX)` |
| `SQL019` | ðŸ”´ Error | Missing `@CorrelationId` / `@RequestId` as first two SP parameters |
| `SQL020` | ðŸ”´ Error | Missing `log.RequestLog` START/SUCCESS/ERROR logging in SP |
| `SQL021` | ðŸŸ¡ Warning | Missing audit columns (`CreatedBy`, `CreatedAt`, `ModifiedBy`, `ModifiedAt`) |
| `SQL022` | ðŸŸ¡ Warning | Missing `IsActive BIT` soft-delete column |
| `SQL023` | ðŸŸ¡ Warning | Missing semicolon statement terminator |
| `SQL024` | ðŸŸ¡ Warning | Non-SARGable WHERE clause (function on indexed column) |
| `SQL025` | ðŸŸ¡ Warning | Implicit conversion risk (VARCHAR compared to NVARCHAR column) |
| `SQL026` | ðŸŸ¡ Warning | Missing TRY/CATCH in stored procedure |
| `SQL027` | ðŸŸ¡ Warning | Cursor used â€” prefer set-based operations |
| `SQL028` | ðŸŸ¡ Warning | `WHILE` loop â€” consider set-based alternative |
| `SQL029` | ðŸŸ¡ Warning | `VARCHAR(MAX)` used without justification â€” prefer sized `VARCHAR(n)` |
| `SQL030` | ðŸŸ¡ Warning | Table/column name is a reserved keyword |

#### Run Commands (bash-based SQL linting)

```bash
# â”€â”€ Critical checks (ðŸ”´ Errors) â”€â”€
echo "=== SQL LINT â€” CRITICAL ==="

# SQL003: SELECT *
grep -rn "SELECT \*" --include="*.sql" | grep -v "EXISTS\s*(SELECT" | grep -v "\-\-" && echo "ðŸ”´ SQL003: SELECT * found"

# SQL004: = NULL
grep -rn "[^!<>]= NULL" --include="*.sql" | grep -v "\-\-" && echo "ðŸ”´ SQL004: = NULL found (use IS NULL)"

# SQL005: GETDATE
grep -rn "GETDATE()" --include="*.sql" | grep -v "\-\-" && echo "ðŸ”´ SQL005: GETDATE() found (use SYSUTCDATETIME())"

# SQL006: DATETIME without 2
grep -rn "DATETIME[^2]" --include="*.sql" | grep -v "DATETIME2" | grep -v "\-\-" && echo "ðŸ”´ SQL006: DATETIME found (use DATETIME2)"

# SQL007: Dynamic SQL concatenation
grep -rn "EXEC\s*(" --include="*.sql" | grep "+" | grep -v "\-\-" && echo "ðŸ”´ SQL007: Dynamic SQL with concatenation"

# SQL019: Missing tracking params
for f in $(grep -rl "CREATE.*PROCEDURE\|ALTER.*PROCEDURE" --include="*.sql"); do
  if ! grep -q "@CorrelationId.*UNIQUEIDENTIFIER" "$f"; then
    echo "ðŸ”´ SQL019: $f â€” Missing @CorrelationId parameter"
  fi
  if ! grep -q "@RequestId.*UNIQUEIDENTIFIER" "$f"; then
    echo "ðŸ”´ SQL019: $f â€” Missing @RequestId parameter"
  fi
done

# SQL001: Missing SET NOCOUNT ON
for f in $(grep -rl "CREATE.*PROCEDURE\|ALTER.*PROCEDURE" --include="*.sql"); do
  if ! grep -q "SET NOCOUNT ON" "$f"; then
    echo "ðŸ”´ SQL001: $f â€” Missing SET NOCOUNT ON"
  fi
done

# â”€â”€ Warning checks (ðŸŸ¡) â”€â”€
echo "=== SQL LINT â€” WARNINGS ==="

# SQL009: Unnamed constraints
grep -rn "PRIMARY KEY\|FOREIGN KEY\|UNIQUE\|DEFAULT\|CHECK" --include="*.sql" | grep -v "CONSTRAINT [A-Z][A-Z]_" | grep -v "\-\-" | head -20

# SQL013: NOLOCK hints
grep -rn "NOLOCK\|WITH\s*(NOLOCK)" --include="*.sql" | grep -v "\-\-" && echo "ðŸŸ¡ SQL013: NOLOCK hint found"

# SQL015: TOP without ORDER BY
grep -rn "SELECT TOP" --include="*.sql" | while read -r line; do
  linenum=$(echo "$line" | cut -d: -f2)
  file=$(echo "$line" | cut -d: -f1)
  if ! sed -n "$((linenum)),\$p" "$file" | head -10 | grep -q "ORDER BY"; then
    echo "ðŸŸ¡ SQL015: $line â€” TOP without ORDER BY"
  fi
done

# SQL023: Missing semicolons
grep -rn "^[[:space:]]*\(SELECT\|INSERT\|UPDATE\|DELETE\|EXEC\)" --include="*.sql" | head -20

echo "=== SQL LINT COMPLETE ==="
```

#### SQLFluff Config (.sqlfluff â€” when using sqlfluff)

```ini
[sqlfluff]
dialect = tsql
templater = raw
max_line_length = 120

[sqlfluff:rules:capitalisation.keywords]
capitalisation_policy = upper

[sqlfluff:rules:capitalisation.identifiers]
capitalisation_policy = pascal

[sqlfluff:rules:aliasing.table]
aliasing = explicit

[sqlfluff:rules:aliasing.column]
aliasing = explicit

[sqlfluff:rules:convention.terminator]
require_final_semicolon = true
```

```bash
# SQLFluff lint
sqlfluff lint --dialect tsql *.sql 2>&1 | head -50

# SQLFluff auto-fix
sqlfluff fix --dialect tsql *.sql 2>&1
```

---

### 2.4 HTML â€” HTMLHint

#### Rules

| Rule | Severity | What It Catches |
|------|----------|-----------------|
| `tagname-lowercase` | ðŸŸ¡ Warning | Tag names should be lowercase |
| `attr-lowercase` | ðŸŸ¡ Warning | Attribute names should be lowercase |
| `attr-value-double-quotes` | ðŸŸ¡ Warning | Attribute values should use double quotes |
| `doctype-first` | ðŸ”´ Error | DOCTYPE must be first line in HTML files |
| `tag-pair` | ðŸ”´ Error | Tags must be paired (no unclosed tags) |
| `spec-char-escape` | ðŸŸ¡ Warning | Special characters must be escaped (`&amp;`, `&lt;`) |
| `id-unique` | ðŸ”´ Error | Duplicate `id` attributes on same page |
| `src-not-empty` | ðŸ”´ Error | `src` / `href` attributes must not be empty |
| `alt-require` | ðŸ”´ Error | `<img>` must have `alt` attribute |
| `title-require` | ðŸŸ¡ Warning | `<html>` should have `<title>` in `<head>` |
| `style-disabled` | ðŸŸ¡ Warning | Inline `style` attribute â€” use CSS classes |
| `inline-script-disabled` | ðŸŸ¡ Warning | Inline `onclick` etc. â€” use event listeners |
| `head-script-disabled` | ðŸŸ¡ Warning | Prefer scripts at bottom of `<body>` or `defer` |
| `input-requires-label` | ðŸ”´ Error | `<input>` must have associated `<label>` |

#### HTMLHint Config (.htmlhintrc)

```json
{
  "tagname-lowercase": true,
  "attr-lowercase": true,
  "attr-value-double-quotes": true,
  "doctype-first": true,
  "tag-pair": true,
  "spec-char-escape": true,
  "id-unique": true,
  "src-not-empty": true,
  "alt-require": true,
  "title-require": true,
  "style-disabled": true,
  "inline-script-disabled": true,
  "input-requires-label": true
}
```

```bash
npx htmlhint "**/*.html" 2>&1 | head -30
```

---

### 2.5 CSS / SCSS â€” Stylelint

#### Rules

| Rule | Severity | What It Catches |
|------|----------|-----------------|
| `color-no-invalid-hex` | ðŸ”´ Error | Invalid hex color value |
| `font-family-no-duplicate-names` | ðŸŸ¡ Warning | Same font listed twice |
| `declaration-no-important` | ðŸŸ¡ Warning | `!important` â€” usually a specificity issue |
| `no-duplicate-selectors` | ðŸŸ¡ Warning | Same selector appears twice in file |
| `no-descending-specificity` | ðŸŸ¡ Warning | Lower specificity rule overrides higher one |
| `selector-no-qualifying-type` | ðŸŸ¡ Warning | `div.class` â€” unnecessary type qualifier |
| `shorthand-property-no-redundant-values` | ðŸŸ¡ Warning | `margin: 10px 10px 10px 10px` â†’ `margin: 10px` |
| `property-no-unknown` | ðŸ”´ Error | Unknown CSS property (typo) |
| `unit-no-unknown` | ðŸ”´ Error | Unknown CSS unit (e.g., `10xp`) |
| `selector-max-id` | ðŸŸ¡ Warning | Avoid ID selectors in stylesheets (specificity) |
| `max-nesting-depth` | ðŸŸ¡ Warning | SCSS nesting > 3 levels deep |
| `no-empty-source` | ðŸŸ¡ Warning | Empty CSS file |

#### Stylelint Config (.stylelintrc.json)

```json
{
  "extends": ["stylelint-config-standard"],
  "rules": {
    "color-no-invalid-hex": true,
    "font-family-no-duplicate-names": true,
    "declaration-no-important": true,
    "no-duplicate-selectors": true,
    "no-descending-specificity": true,
    "property-no-unknown": true,
    "unit-no-unknown": true,
    "selector-max-id": 0,
    "max-nesting-depth": 3,
    "no-empty-source": true
  }
}
```

```bash
npx stylelint "**/*.css" "**/*.scss" 2>&1 | head -30
```

---

### 2.6 JSON â€” JSONLint + Schema Validation

#### Rules

| Rule | Severity | What It Catches |
|------|----------|-----------------|
| Syntax error | ðŸ”´ Error | Invalid JSON (trailing comma, single quotes, comments) |
| Duplicate keys | ðŸ”´ Error | Same key appears twice in same object |
| Schema mismatch | ðŸŸ¡ Warning | `appsettings.json` missing required fields, wrong types |
| Trailing comma | ðŸ”´ Error | `{ "a": 1, }` â€” invalid in standard JSON |
| Single quotes | ðŸ”´ Error | `{'key': 'value'}` â€” JSON requires double quotes |

#### Run Commands

```bash
# Validate all JSON files
for f in $(find . -name "*.json" -not -path "*/node_modules/*"); do
  python3 -c "import json; json.load(open('$f'))" 2>&1 && echo "âœ… $f" || echo "ðŸ”´ $f â€” INVALID JSON"
done

# OR use jsonlint
npx jsonlint-mod --quiet *.json 2>&1
```

---

### 2.7 Markdown â€” markdownlint

#### Rules

| Rule | Severity | What It Catches |
|------|----------|-----------------|
| `MD001` | ðŸŸ¡ Warning | Heading increment by more than one level (h1 â†’ h3 skips h2) |
| `MD003` | ðŸŸ¡ Warning | Inconsistent heading style (ATX vs setext) |
| `MD009` | ðŸŸ¡ Warning | Trailing whitespace |
| `MD012` | ðŸŸ¡ Warning | Multiple consecutive blank lines |
| `MD013` | â„¹ï¸ Info | Line length exceeds 120 chars |
| `MD022` | ðŸŸ¡ Warning | Headings should be surrounded by blank lines |
| `MD032` | ðŸŸ¡ Warning | Lists should be surrounded by blank lines |
| `MD033` | ðŸŸ¡ Warning | Inline HTML in markdown (prefer markdown syntax) |
| `MD034` | ðŸŸ¡ Warning | Bare URL (wrap in `<>` or `[text](url)`) |
| `MD041` | ðŸŸ¡ Warning | First line should be a top-level heading |

```bash
npx markdownlint "**/*.md" --ignore node_modules 2>&1 | head -30
```

---

### 2.8 YAML â€” yamllint

```bash
pip install yamllint --break-system-packages 2>/dev/null
yamllint -s . 2>&1 | head -30
```

---

### 2.9 Dockerfile â€” hadolint

```bash
# If Docker files exist
if ls Dockerfile* 2>/dev/null; then
  docker run --rm -i hadolint/hadolint < Dockerfile 2>&1 | head -20
fi
```

---

### Layer 2 Output Format

```
## Layer 2 â€” Lint Check
### TypeScript / React (ESLint + Prettier)
| # | File | Line | Rule | Severity | Message | Auto-Fix? |
|---|------|------|------|----------|---------|-----------|
| 1 | UserCard.tsx | 12 | @typescript-eslint/no-explicit-any | ðŸ”´ Error | Unexpected `any`. Specify a type. | No |
| 2 | api.ts | 34 | @typescript-eslint/no-floating-promises | ðŸ”´ Error | Promise returned but not awaited | No |
| 3 | App.tsx | 5 | prefer-const | ðŸŸ¡ Warning | 'theme' is never reassigned. Use `const`. | âœ… Yes |
| 4 | index.tsx | 1 | @typescript-eslint/consistent-type-imports | ðŸŸ¡ Warning | Use `import type` for type-only imports | âœ… Yes |
Prettier: 2 files need formatting (auto-fixable âœ…)

### C# / .NET (Roslyn + dotnet-format)
| # | File | Line | Rule | Severity | Message | Auto-Fix? |
|---|------|------|------|----------|---------|-----------|
| 1 | UserService.cs | 45 | CA2016 | ðŸ”´ Error | Forward CancellationToken to 'GetAsync' | No |
| 2 | SpHelper.cs | 12 | CS8602 | ðŸ”´ Error | Dereference of possibly null reference | No |
| 3 | Program.cs | 8 | IDE0005 | ðŸŸ¡ Warning | Remove unnecessary using | âœ… Yes |
dotnet-format: 3 files need formatting (auto-fixable âœ…)

### T-SQL (SQL Lint)
| # | File | Line | Rule | Severity | Message | Auto-Fix? |
|---|------|------|------|----------|---------|-----------|
| 1 | Reports_Get.sql | 15 | SQL003 | ðŸ”´ Error | SELECT * â€” list columns explicitly | No |
| 2 | Users_Manage.sql | 88 | SQL023 | ðŸŸ¡ Warning | Missing semicolon terminator | âœ… Yes |

### JSON
All JSON files valid âœ…

### Summary
| Language | ðŸ”´ Errors | ðŸŸ¡ Warnings | Auto-Fixable |
|----------|-----------|-------------|--------------|
| TypeScript/React | 2 | 2 | 2 |
| C# / .NET | 2 | 1 | 1 |
| T-SQL | 1 | 1 | 1 |
| JSON | 0 | 0 | 0 |
| **Total** | **5** | **4** | **4** |

**Result: âŒ 5 Errors found â€” fix all errors before proceeding to Layer 3**
```

---

## Layer 3 â€” SonarQube-Lite Static Analysis

Simulate SonarQube's key rules for reliability, maintainability, and code smells.

### 3.1 Code Smells

| Smell | Severity | Detection |
|-------|----------|-----------|
| **Cognitive Complexity** > 15 | ðŸŸ  High | Nested ifs/loops/switches exceeding 3 levels; long CASE chains |
| **Method too long** > 40 lines | ðŸŸ¡ Medium | Functions/methods/SP blocks exceeding 40 executable lines |
| **Too many parameters** > 7 | ðŸŸ¡ Medium | Functions or SPs with more than 7 business parameters (tracking IDs excluded) |
| **Duplicate code blocks** | ðŸŸ¡ Medium | 6+ lines duplicated across files; copy-pasted WHERE clauses |
| **Dead code** | ðŸŸ¡ Medium | Commented-out code blocks, unreachable branches, unused functions |
| **Magic numbers/strings** | ðŸŸ¡ Medium | Hardcoded values instead of constants: `if (status == 3)`, `"admin"` |
| **Long parameter list** | ðŸŸ¡ Medium | Favor parameter objects over 5+ primitive parameters |
| **Deep nesting** > 3 levels | ðŸŸ¡ Medium | Early return/guard clauses preferred over nested ifs |
| **Empty catch blocks** | ðŸŸ  High | `catch { }` or `catch (Exception) { }` with no logging/re-throw |
| **God class/file** > 300 lines | ðŸŸ¡ Medium | Split into focused, single-responsibility modules |

### 3.2 Reliability

| Rule | Severity | Detection |
|------|----------|-----------|
| Null pointer dereference | ðŸ”´ Critical | Accessing `.Property` on potentially null object |
| Resource leak | ðŸŸ  High | SqlConnection, HttpClient, Stream not disposed |
| Unchecked return value | ðŸŸ¡ Medium | Ignoring return from async calls, .TryParse, etc. |
| Off-by-one errors | ðŸŸ  High | Array bounds, pagination OFFSET calculations |
| Race conditions | ðŸŸ  High | Shared mutable state without synchronization |
| Missing error handling | ðŸŸ  High | No try-catch around I/O operations |
| Infinite loop risk | ðŸ”´ Critical | Loops with no guaranteed exit condition |

### 3.3 Maintainability Rating

Score each file A-E:

| Rating | Criteria |
|--------|----------|
| **A** | â‰¤ 5% of code needs refactoring; no smells above Medium |
| **B** | 6â€“10% needs refactoring; no more than 2 Medium smells |
| **C** | 11â€“20% needs refactoring; has High smells but no Critical |
| **D** | 21â€“50% needs refactoring; has Critical smells |
| **E** | > 50% needs refactoring; fundamental design issues |

### 3.4 Duplication Detection

Flag these patterns:
- **Exact duplicates**: 6+ identical lines across files
- **Structural duplicates**: Same logic with different variable names
- **SQL duplicates**: Repeated WHERE/JOIN patterns that should be a view or CTE
- **Config duplicates**: Same connection strings, URLs in multiple places

### Output Format

```
## Layer 3 â€” SonarQube-Lite Analysis
### Code Smells: 3 found
| # | File | Line | Rule | Severity | Message |
|---|------|------|------|----------|---------|
| 1 | OrderService.cs | 45-120 | S3776 | ðŸŸ  High | Cognitive complexity is 22 (max 15) |
| 2 | Users_Get.sql | 30 | S109 | ðŸŸ¡ Medium | Magic number 200 â€” extract to named constant or parameter |
| 3 | UserList.tsx | 15-89 | S138 | ðŸŸ¡ Medium | Function too long (74 lines, max 40) |

### Duplication: 1 block
| Files | Lines | Duplicate Lines |
|-------|-------|----------------|
| Orders_Get.sql â†” Products_Get.sql | 20-35 â†” 18-33 | 15 lines (pagination pattern) |

### Maintainability: B (92/100)

**Result: âš ï¸ 1 High, 2 Medium â€” fix High before proceeding**
```

---

## Layer 4 â€” Vulnerability Scan

Check for known vulnerability patterns in code and dependencies.

### 4.1 Injection Vulnerabilities

| Type | Language | What to Check |
|------|----------|---------------|
| **SQL Injection** | T-SQL | Dynamic SQL built with string concatenation: `EXEC('SELECT * FROM ' + @TableName)` |
| **SQL Injection** | C# | Raw string interpolation in queries: `$"SELECT * FROM Users WHERE Id = {id}"` |
| **XSS** | React/TS | `dangerouslySetInnerHTML`, unescaped user input in DOM |
| **Command Injection** | C# | `Process.Start()` with user-supplied arguments |
| **Path Traversal** | C#/Node | File operations with unsanitized user input: `File.ReadAllText(userPath)` |
| **LDAP Injection** | C# | Unsanitized input in LDAP queries |
| **NoSQL Injection** | TS/Node | Unvalidated objects passed to MongoDB queries |
| **Header Injection** | C# | User input in HTTP response headers |

### 4.2 Secrets & Credentials Exposure

```
ðŸ”´ CRITICAL â€” scan every file for:
âœ… Hardcoded connection strings with passwords
âœ… API keys in source code (regex: [A-Za-z0-9]{20,} near 'key', 'secret', 'token', 'password')
âœ… Private keys or certificates in code
âœ… Credentials in config files committed to source (appsettings.json with real passwords)
âœ… JWT secrets hardcoded
âœ… Cloud provider access keys (AWS, Azure, GCP patterns)
âœ… Database passwords in plain text
```

**Detection regex patterns:**
```bash
# Secrets detection
grep -rn "password\s*[:=]\s*['\"]" --include="*.cs" --include="*.ts" --include="*.json" --include="*.sql"
grep -rn "connectionstring.*password" --include="*.json" --include="*.config" -i
grep -rn "Bearer [A-Za-z0-9\-._~+/]+" --include="*.cs" --include="*.ts"
grep -rn "sk-[A-Za-z0-9]{20,}" --include="*.cs" --include="*.ts" --include="*.json"
grep -rn "AKIA[A-Z0-9]{16}" --include="*.cs" --include="*.ts" --include="*.json"
```

### 4.3 Dependency Vulnerabilities

```bash
# .NET
dotnet list package --vulnerable 2>&1

# Node/React
npm audit 2>&1 | head -30

# Check for known vulnerable package versions
grep -n "System.Text.Json.*[0-7]\." *.csproj    # Example: < v8 has known issues
```

### 4.4 Data Exposure

| Check | Severity | Details |
|-------|----------|---------|
| Stack traces in API responses | ðŸ”´ Critical | GlobalExceptionMiddleware must catch ALL exceptions |
| Verbose error messages | ðŸŸ  High | Never expose column names, SP names, SQL errors to client |
| Sensitive data in logs | ðŸŸ  High | Don't log passwords, tokens, PII, full credit card numbers |
| Missing HTTPS enforcement | ðŸŸ  High | `app.UseHttpsRedirection()` must be present |
| PII in URL query parameters | ðŸŸ  High | Email, SSN, phone should be in POST body, not GET params |
| Sensitive data in localStorage | ðŸŸ  High | Tokens and PII should use httpOnly cookies or sessionStorage |
| Over-fetching from DB | ðŸŸ¡ Medium | SELECT * returning columns with PII when not needed |

### Output Format

```
## Layer 4 â€” Vulnerability Scan
| # | File | Line | Type | Severity | Finding |
|---|------|------|------|----------|---------|
| 1 | appsettings.json | 5 | Secret | ðŸ”´ Critical | Hardcoded DB password in connection string |
| 2 | SearchController.cs | 22 | SQLi | ðŸ”´ Critical | String interpolation in raw SQL query |
| 3 | UserCard.tsx | 15 | XSS | ðŸŸ  High | dangerouslySetInnerHTML with user-supplied bio |

**Result: âŒ 2 Critical, 1 High â€” MUST fix all before proceeding**
```

---

## Layer 5 â€” Security Hardening (OWASP Top 10)

Map every finding to OWASP 2021 Top 10 categories.

### OWASP Checklist per Language

#### A01: Broken Access Control
```
âœ… Every API endpoint has [Authorize] or explicit [AllowAnonymous]
âœ… Resource-level authorization (user can only access their own data)
âœ… CORS configured for specific origins, never wildcard in production
âœ… SQL SPs accept @UserId for audit â€” verify caller has permission
âœ… No IDOR: user cannot pass another user's ID to access their data
âœ… Anti-CSRF tokens on state-changing operations
âœ… Directory listing disabled on web server
```

#### A02: Cryptographic Failures
```
âœ… Passwords hashed with bcrypt/Argon2, never MD5/SHA1/plain
âœ… Sensitive data encrypted at rest (column encryption, TDE)
âœ… TLS 1.2+ enforced; no HTTP fallback
âœ… Secrets in vault/environment variables, not in source
âœ… No custom cryptography implementations
```

#### A03: Injection
```
âœ… Parameterized queries / stored procedures â€” never string concatenation
âœ… Input validated on both client AND server side
âœ… HTML output encoded to prevent XSS
âœ… File uploads validated (type, size, name sanitization)
âœ… LIKE patterns escaped: user input with %, _, [ chars handled
```

#### A04: Insecure Design
```
âœ… Rate limiting on authentication endpoints
âœ… Account lockout after failed attempts
âœ… Business logic validation server-side (not just UI)
âœ… Proper error handling that doesn't reveal system internals
âœ… Principle of least privilege in DB permissions
```

#### A05: Security Misconfiguration
```
âœ… Debug/development mode disabled in production config
âœ… Default credentials changed
âœ… Unnecessary HTTP methods disabled
âœ… Security headers set: X-Content-Type-Options, X-Frame-Options, CSP
âœ… Stack traces never exposed in production responses
âœ… Swagger/API docs disabled in production
```

#### A06: Vulnerable and Outdated Components
```
âœ… No packages with known CVEs
âœ… Frameworks at supported LTS versions
âœ… No deprecated APIs used (TEXT, IMAGE, DATETIME in SQL Server)
```

#### A07: Identification and Authentication Failures
```
âœ… JWT tokens have reasonable expiry
âœ… Refresh token rotation implemented
âœ… Password complexity enforced
âœ… Session invalidation on logout
âœ… Multi-factor authentication available for admin
```

#### A08: Software and Data Integrity Failures
```
âœ… Input deserialization is validated (no insecure deserialization)
âœ… Package integrity verified (lock files committed)
âœ… No eval() or dynamic code execution with user input
```

#### A09: Security Logging and Monitoring Failures
```
âœ… CorrelationId + RequestId logged on every operation
âœ… Authentication failures logged
âœ… Authorization failures logged
âœ… Input validation failures logged (potential attack detection)
âœ… Sensitive data masked in logs
âœ… Log injection prevented (user input sanitized before logging)
```

#### A10: Server-Side Request Forgery (SSRF)
```
âœ… URL validation on any server-side HTTP requests
âœ… Allowlist for external API calls
âœ… No user-controlled URLs passed to HttpClient without validation
```

### Output Format

```
## Layer 5 â€” Security Hardening (OWASP)
| # | OWASP | File | Line | Severity | Finding | Fix |
|---|-------|------|------|----------|---------|-----|
| 1 | A01 | UsersController.cs | 34 | ðŸ”´ Critical | Missing [Authorize] on DELETE endpoint | Add [Authorize(Roles = "Admin")] |
| 2 | A03 | Reports_Get.sql | 22 | ðŸŸ  High | LIKE pattern not escaping user wildcards | Add ESCAPE clause or sanitize @SearchText |
| 3 | A05 | Program.cs | 48 | ðŸŸ¡ Medium | Swagger enabled in all environments | Wrap in if (app.Environment.IsDevelopment()) |

**Result: âŒ 1 Critical, 1 High, 1 Medium â€” fix Critical and High before proceeding**
```

---

## Layer 6 â€” Optimization & Standards Compliance

### 6.1 Performance Optimization

#### T-SQL Performance
```
âœ… SARGable WHERE clauses â€” no functions on indexed columns
âœ… Appropriate indexes exist for JOIN/WHERE/ORDER BY columns
âœ… Foreign key columns indexed
âœ… OFFSET/FETCH used for pagination (not TOP with subquery)
âœ… ISNULL/COALESCE used correctly (ISNULL is faster for simple cases)
âœ… Temp tables for large sets, table variables for < 100 rows
âœ… No unnecessary DISTINCT (indicates a JOIN issue)
âœ… EXISTS preferred over IN for correlated subqueries
âœ… No implicit conversions in WHERE/JOIN (VARCHAR vs NVARCHAR)
âœ… NOLOCK used sparingly; RCSI preferred
âœ… No cursors â€” use set-based operations
âœ… Computed columns considered for frequently derived values
âœ… Statistics up to date on key columns
```

#### C# / .NET Performance
```
âœ… async/await used throughout I/O paths â€” no sync-over-async
âœ… CancellationToken forwarded through entire call chain
âœ… IAsyncEnumerable for streaming large datasets from SPs
âœ… StringBuilder for string concatenation in loops (> 3 concatenations)
âœ… Span<T> / ReadOnlySpan<T> for parsing and slicing
âœ… No Task.Result / .Wait() (deadlock risk in ASP.NET)
âœ… HttpClient registered via IHttpClientFactory (not new HttpClient())
âœ… SpHelper connection opened/closed per call (Dapper handles pooling)
âœ… SP result sets return only needed columns â€” no SELECT * in SPs
âœ… SP pagination uses OFFSET/FETCH with max PageSize cap (200)
âœ… Dapper QueryMultipleAsync for SPs returning multiple result sets
âœ… DynamicParameters reused efficiently â€” no unnecessary allocations
âœ… Value types (struct/record struct) for small, immutable DTOs
ðŸ”´ NO EF Core â€” no AsNoTracking, no Select() projection, no compiled queries
ðŸ”´ NO inline SQL â€” all data access through SpHelper â†’ Stored Procedures
```

#### React / TypeScript Performance
```
âœ… Components don't re-render unnecessarily (check with React DevTools)
âœ… useMemo/useCallback only where profiling shows benefit â€” not everywhere
âœ… Large lists virtualized (@tanstack/react-virtual)
âœ… Route-based code splitting with lazy() and Suspense
âœ… Images optimized (WebP, lazy loading, appropriate dimensions)
âœ… Bundle size checked â€” no unnecessary large dependencies
âœ… Debounced search input (300ms minimum)
âœ… AbortController used for cancellable fetch requests
âœ… No inline object/array creation in JSX props (causes re-renders)
âœ… TanStack Query caching configured (staleTime, gcTime)
```

### 6.2 Standards Compliance

#### Naming Conventions
| Element | T-SQL | C# | TypeScript/React |
|---------|-------|-----|-----------------|
| Tables | PascalCase plural (`app.Users`) | N/A | N/A |
| Columns | PascalCase (`FirstName`) | PascalCase properties | camelCase (`firstName`) |
| SPs | `{Table}_Manage` / `{Table}_Get` | N/A | N/A |
| Variables | `@CamelCase` | `_camelCase` (private) | `camelCase` |
| Constants | N/A | `PascalCase` | `SCREAMING_SNAKE` or `PascalCase` |
| Interfaces | N/A | `IUserRepository` | `UserCardProps` (no I prefix) |
| Files | `SP_{Name}.sql` | `UserService.cs` | `UserCard.tsx` |
| CSS classes | N/A | N/A | `kebab-case` or Tailwind utilities |

#### Team Convention Checks
```
âœ… Consistent quote style (single quotes in TS, single in SQL strings)
âœ… Consistent indentation (4 spaces for C#/SQL, 2 spaces for TS/React)
âœ… Consistent import ordering (React â†’ third-party â†’ local â†’ types)
âœ… Consistent file organization (feature-based folders)
âœ… Consistent error handling patterns (Result<T> or exception-based â€” pick one)
âœ… No mixed patterns (don't use both Dapper and raw ADO.NET in same project)
âœ… Comment quality â€” complex logic has WHY comments, not WHAT comments
âœ… TODO/FIXME/HACK markers documented with ticket numbers
```

### 6.3 Documentation & Readability
```
âœ… Public APIs have XML doc comments (C#) or JSDoc (TypeScript)
âœ… Complex SQL has inline comments explaining business logic
âœ… README updated when new features/tables/endpoints added
âœ… Breaking changes documented
âœ… API endpoint documentation (Swagger annotations) accurate
```

### Output Format

```
## Layer 6 â€” Optimization & Standards
| # | File | Line | Category | Severity | Finding | Recommendation |
|---|------|------|----------|----------|---------|----------------|
| 1 | Orders_Get.sql | 44 | Perf | ðŸŸ¡ Medium | Non-SARGable: WHERE YEAR(OrderDate) = 2024 | Use date range: >= '2024-01-01' AND < '2025-01-01' |
| 2 | UserService.cs | 28 | Perf | ðŸŸ¡ Medium | Missing CancellationToken forwarding | Add CancellationToken ct parameter |
| 3 | UserList.tsx | 12 | Perf | â„¹ï¸ Info | Search input not debounced | Add useDebounce(300ms) hook |
| 4 | api.ts | 5 | Standards | â„¹ï¸ Info | Inconsistent import ordering | Group: react â†’ third-party â†’ @/ local â†’ types |

**Result: âœ… 0 Critical/High â€” 2 Medium, 2 Info (recommended fixes)**
```

---

## Final Gate Summary Template

After all 6 layers run, produce this summary:

```
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
           CODE QUALITY GATE â€” FINAL REPORT
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

Files Checked: 5
Languages: T-SQL, C#, TypeScript/React

â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Check                        â”‚ Status â”‚ Issues     â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ ðŸ›ï¸ SP-Only Mandate           â”‚ âœ… Pass â”‚ No EF/Inlineâ”‚
â”‚ 1. VS Code Problems Tab      â”‚ âœ… Pass â”‚ 0E 2W 0I  â”‚
â”‚ 2. Lint Check (ALL langs)    â”‚ âœ… Pass â”‚ 0E 3W 1I  â”‚
â”‚ 3. SonarQube-Lite Analysis   â”‚ âœ… Pass â”‚ 0C 1H 2M  â”‚
â”‚ 4. Vulnerability Scan        â”‚ âœ… Pass â”‚ 0C 0H 1M  â”‚
â”‚ 5. Security (OWASP)          â”‚ âœ… Pass â”‚ 0C 0H 2M  â”‚
â”‚ 6. Optimization & Standards  â”‚ âœ… Pass â”‚ 0C 0H 3M  â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ OVERALL                      â”‚ âœ… PASS â”‚ 0C 1H 11M â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

Legend: C=Critical, H=High, M=Medium, E=Error, W=Warning, I=Info

SP-Only Mandate:
  âœ… No Entity Framework detected (no DbContext, DbSet, EF NuGet packages)
  âœ… No inline SQL detected (no raw SELECT/INSERT/UPDATE/DELETE in C#)
  âœ… All data access via SpHelper â†’ Stored Procedures â†’ Dapper
  âœ… @CorrelationId + @RequestId injected via WithTracking()

Gate Criteria:
  âœ… SP-Only Mandate passed
  âœ… Zero Critical findings across all layers
  âœ… Zero Errors in Layer 1 + Layer 2
  âš ï¸  1 High in Layer 3 â€” accepted (tracked in findings below)
  
Remaining Findings (Medium/Low â€” fix when practical):
  1. [L2] App.tsx:5 â€” prefer-const: 'theme' never reassigned â†’ use const
  2. [L3] OrderService.cs:45 â€” Cognitive complexity 18 â†’ refactor to extract methods
  3. [L4] package.json â€” lodash 4.17.20 has prototype pollution fix in 4.17.21
  4. ...

âœ… GATE PASSED â€” files cleared for delivery to /mnt/user-data/outputs/
```

---

## Gate Decision Rules

| Findings | Decision |
|----------|----------|
| ðŸ›ï¸ SP-Only Mandate violated (EF or inline SQL found) | âŒ **BLOCKED** â€” rewrite to use SpHelper + SPs, no exceptions |
| ðŸ”´ Any Critical (any layer) | âŒ **BLOCKED** â€” fix immediately, re-run gate |
| ðŸ”´ Any Error in Layer 1 or Layer 2 | âŒ **BLOCKED** â€” code won't compile/run or fails lint |
| ðŸŸ  High findings only | âš ï¸ **CONDITIONAL** â€” fix if straightforward; document if accepted |
| ðŸŸ¡ Medium and below only | âœ… **PASS** â€” deliver, note findings for future improvement |
| No findings | âœ… **CLEAN PASS** â€” deliver immediately |

---

## Integration with Existing Skills

This quality gate works alongside the existing tech-stack skills:

| After This Skill Runs... | This Gate Checks... |
|--------------------------|---------------------|
| **mssql** (T-SQL skill) | SP has @CorrelationId/@RequestId, SET NOCOUNT ON, idempotent DDL, proper indexing, no SELECT *, UTC dates, audit columns, soft delete |
| **dotnet** (.NET skill) | **ðŸ›ï¸ SP-Only Mandate** (no EF, no inline SQL, all access via SpHelper), TrackingContext injected, GlobalExceptionMiddleware present, no leaked stack traces, Serilog configured, CancellationToken forwarded, ApiResponse<T> wrapper used, Dapper + Microsoft.Data.SqlClient ONLY |
| **react** (React skill) | X-Correlation-Id sent, X-Request-Id read, ErrorBoundary wrapping routes, ErrorFallback shows requestId not stack trace, hooks follow rules, proper TypeScript strict mode |

### Cross-Stack Consistency Checks
```
âœ… T-SQL SP parameter names match C# DynamicParameters.Add() names
âœ… SP result set column names match C# DTO property names (case-insensitive via Dapper)
âœ… API response shape matches TypeScript interface definitions
âœ… API route naming matches React api.ts URL constants
âœ… Error codes thrown in SP (50001, 50002...) handled in C# service layer
âœ… Filter parameters (PageNumber, PageSize, SortColumn) consistent across all 3 layers
âœ… CorrelationId + RequestId present in: SP params â†’ C# SpHelper â†’ API headers â†’ React apiClient â†’ ErrorFallback
âœ… NO EF Core anywhere â€” no DbContext, no migrations, no EF NuGet packages
âœ… ALL .cs repository files inject SpHelper, not DbContext
âœ… ALL data operations: Repository â†’ SpHelper.ManageAsync/GetByIdAsync/GetListAsync â†’ SP
âœ… NO inline SQL in any .cs file â€” zero tolerance
```

---

## Execution Workflow

When running this gate, follow this exact workflow:

```
1. IDENTIFY changed files
   â†’ List all files created or modified in this session

2. RUN SP-ONLY MANDATE CHECK (before all layers â€” instant blocker)
   â†’ For .cs files: scan for inline SQL, EF Core, raw SqlCommand
   â†’ For .csproj files: scan for EntityFrameworkCore NuGet packages
   â†’ If ANY violation found: âŒ BLOCKED â€” rewrite to use SpHelper + SPs
   â†’ This check is NON-NEGOTIABLE â€” no exceptions, no workarounds

3. RUN Layer 1 (VS Code Problems)
   â†’ For each file: syntax check, type check, reference check
   â†’ Use bash tools where possible (tsc --noEmit, dotnet build)
   â†’ If ANY ðŸ”´ Error: STOP, fix, re-check

4. RUN Layer 2 (Lint Check â€” ALL languages)
   â†’ TypeScript/React: npx eslint + npx prettier --check
   â†’ C#/.NET: dotnet build (Roslyn analyzers) + dotnet format --verify-no-changes
   â†’ C#/.NET: SP001-SP012 rules (inline SQL, EF detection, SpHelper verification)
   â†’ T-SQL: bash grep checks for SQL001-SQL030 rules + sqlfluff lint
   â†’ HTML: npx htmlhint
   â†’ CSS: npx stylelint
   â†’ JSON: python3 json.load validation / npx jsonlint-mod
   â†’ Markdown: npx markdownlint
   â†’ Auto-fix where possible (eslint --fix, prettier --write, dotnet format)
   â†’ If ANY ðŸ”´ Error after auto-fix: STOP, manual fix, re-check

5. RUN Layer 3 (SonarQube-Lite)
   â†’ For each file: complexity, smells, duplication, maintainability rating
   â†’ If ANY ðŸ”´ Critical: STOP, fix, re-check

6. RUN Layer 4 (Vulnerability Scan)
   â†’ For each file: injection patterns, secrets scan, dependency audit
   â†’ If ANY ðŸ”´ Critical: STOP, fix, re-check

7. RUN Layer 5 (Security / OWASP)
   â†’ For each file: auth, input validation, data exposure, headers
   â†’ If ANY ðŸ”´ Critical: STOP, fix, re-check

8. RUN Layer 6 (Optimization & Standards)
   â†’ For each file: performance, naming, conventions, documentation
   â†’ Note findings but don't block on Medium/Low

9. PRODUCE Final Gate Summary
   â†’ Table with all 6 layers + SP-only mandate status
   â†’ List remaining Medium/Low findings
   â†’ âœ… PASS / âŒ BLOCKED decision

9. IF PASSED: copy to /mnt/user-data/outputs/
   IF BLOCKED: fix issues and re-run from the failed layer
```

---

## Quick-Reference Severity Guide

| Severity | Icon | Action | Examples |
|----------|------|--------|----------|
| ðŸ”´ Critical | ðŸ”´ | **Must fix now** â€” blocks delivery | SQL injection, hardcoded secrets, missing auth, syntax errors, null pointer crash |
| ðŸŸ  High | ðŸŸ  | **Should fix** â€” significant risk or smell | Empty catch blocks, resource leaks, cognitive complexity > 20, missing HTTPS |
| ðŸŸ¡ Medium | ðŸŸ¡ | **Fix when practical** â€” quality improvement | Unused variables, long methods, missing comments, non-optimal indexes |
| â„¹ï¸ Info | â„¹ï¸ | **Note for awareness** â€” nice-to-have | Import ordering, minor naming inconsistencies, potential micro-optimizations |

---

## Output Delivery

1. **This gate runs AFTER code is written** â€” it is the last step before delivery
2. **Run ALL 6 layers** â€” no skipping, no shortcuts
3. **Layer 2 (Lint) must auto-fix first** â€” run `eslint --fix`, `prettier --write`, `dotnet format` before reporting remaining issues
4. **Produce the Final Gate Summary** in every response where files are delivered
5. **Block delivery on Critical/Error findings** â€” fix first, then re-run
6. **Document accepted findings** â€” Medium/Low issues noted for future improvement
7. **Cross-reference with tech-stack skills** â€” ensure mssql/dotnet/react conventions followed
8. **Include lint config files** â€” when creating new projects, generate `.eslintrc`/`eslint.config.mjs`, `.prettierrc`, `.editorconfig`, `.stylelintrc.json`, `.htmlhintrc`, `.sqlfluff` alongside source code
9. **The gate report is shown inline in the chat** â€” not as a separate file (unless user requests it)
