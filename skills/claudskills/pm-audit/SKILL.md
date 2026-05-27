---
name: pm-audit
description: >-
  Proactive codebase audit that discovers code quality issues, security
  vulnerabilities, performance problems, and architectural debt using parallel
  analysis agents, then creates well-structured issues in PinkRooster from
  confirmed findings. Use this skill whenever the user wants to audit their
  code, find problems, scan for issues, do a code review of the whole project,
  or says things like "audit the codebase", "find issues", "scan for problems",
  "what's wrong with the code", "check for security issues", "find tech debt",
  "code health check", "quality scan", or "are there any bugs". Also triggers
  when the user asks to analyze code quality and wants actionable tracked issues
  created from the findings, not just a report.
argument-hint: "[--focus quality|security|performance|architecture] [--scope path/to/dir]"
---

# Proactive Codebase Audit

Discover real problems in the codebase by running parallel analysis agents across
multiple domains, then create tracked issues from confirmed findings. This goes
beyond static reports — every finding becomes an actionable, prioritized issue
in the project management system.

The key difference from a code review or analysis report: this skill produces
*tracked work items* that can be scaffolded, assigned, and implemented.

## Step 0: Parse Arguments

Parse `$ARGUMENTS` for flags:

- **`--focus <domain>`**: Limit analysis to one domain: `quality`, `security`,
  `performance`, or `architecture`. Default: all four domains.
- **`--scope <path>`**: Limit analysis to a subdirectory (e.g., `src/dashboard`,
  `src/PinkRooster.Api`). Default: entire project.
- If the user provides a plain description like "check the API for security issues",
  infer `--focus security --scope src/PinkRooster.Api`.

## Step 1: Resolve Project and Load Context

- Current directory: !`pwd`
- Call `mcp__pinkrooster__get_project_status` with `projectPath` set to the directory above
- Extract the `projectId`

Load existing issues to avoid creating duplicates:
1. `mcp__pinkrooster__get_issue_overview` with `projectId` and `stateFilter: "Active"`
2. `mcp__pinkrooster__get_issue_overview` with `projectId` and `stateFilter: "Inactive"`

Compile a deduplication list of existing issue names and descriptions.

## Step 2: Launch Parallel Analysis Agents

Spawn up to 4 Explore agents (one per domain) in parallel. Each agent gets a
focused analysis brief. If `--focus` was specified, only spawn that one domain.

The agents run in the background while you proceed to Step 3.

### Agent Prompts

For each domain, spawn an Agent with `subagent_type: "Explore"` and the following
prompt template (adapted per domain):

**Quality Agent:**
```
Analyze the codebase at {project_path}{scope_suffix} for code quality issues.

Focus on:
- Code duplication (copy-pasted logic, duplicated components)
- Dead code (unused functions, unreachable branches, commented-out code)
- Inconsistent patterns (different approaches to the same problem across files)
- Missing error handling (unhandled promise rejections, empty catch blocks, missing null checks)
- Overly complex functions (deep nesting, long methods, high cyclomatic complexity)
- Naming inconsistencies (mixed conventions, unclear variable names)

For each finding, report:
1. File path and line number(s)
2. What the problem is (specific, not vague)
3. Severity: Critical (causes bugs), Major (maintainability risk), Minor (code smell), Trivial (style)
4. A concrete fix suggestion

Skip trivial style issues that a linter would catch. Focus on problems that
affect correctness, maintainability, or developer productivity.

Write findings to: {output_path}/quality_findings.md
```

**Security Agent:**
```
Analyze the codebase at {project_path}{scope_suffix} for security vulnerabilities.

Focus on:
- Input validation gaps (user input reaching DB queries, file paths, shell commands without sanitization)
- Authentication/authorization flaws (missing auth checks, privilege escalation paths, insecure token handling)
- Secrets in code (hardcoded API keys, passwords, connection strings outside config)
- Injection risks (SQL injection, XSS, command injection, path traversal)
- Insecure configurations (permissive CORS, missing security headers, debug mode in production configs)
- Dependency vulnerabilities (known CVEs in package versions if package files are present)

For each finding, report:
1. File path and line number(s)
2. The vulnerability type (OWASP category if applicable)
3. Severity: Critical (exploitable, data breach risk), Major (exploitable with conditions), Minor (defense-in-depth gap), Trivial (theoretical risk)
4. Attack scenario (how could this be exploited?)
5. Fix recommendation

Write findings to: {output_path}/security_findings.md
```

**Performance Agent:**
```
Analyze the codebase at {project_path}{scope_suffix} for performance issues.

Focus on:
- N+1 query patterns (database queries inside loops)
- Missing indexes (queries filtering/sorting on non-indexed columns, check EF configurations)
- Unbounded queries (no pagination, no limits on returned results)
- Memory leaks (event handlers not cleaned up, growing collections, unclosed resources)
- Expensive operations in hot paths (regex compilation in loops, repeated serialization, synchronous I/O)
- Missing caching (repeated expensive computations, redundant API calls)
- Frontend: unnecessary re-renders, large bundle imports, unoptimized images

For each finding, report:
1. File path and line number(s)
2. What the performance impact is (quantify if possible: "O(n^2) where n = number of entities")
3. Severity: Critical (user-visible latency), Major (scalability concern), Minor (optimization opportunity), Trivial (micro-optimization)
4. Fix recommendation

Write findings to: {output_path}/performance_findings.md
```

**Architecture Agent:**
```
Analyze the codebase at {project_path}{scope_suffix} for architectural issues.

Focus on:
- Layer violations (direct DB access from controllers, UI components calling repositories)
- Circular dependencies (projects/modules/classes referencing each other in cycles)
- Missing abstractions (concrete types where interfaces should be, tight coupling)
- Inconsistent patterns (some services use pattern A, others use pattern B for the same thing)
- Single responsibility violations (god classes, services doing too many things)
- Configuration drift (inconsistent settings across environments, hardcoded values that should be configurable)
- Missing or outdated documentation for critical architectural decisions

For each finding, report:
1. File path(s) and the architectural boundary being violated
2. What the structural problem is
3. Severity: Critical (blocks future development), Major (increases maintenance cost), Minor (inconsistency), Trivial (style preference)
4. Refactoring recommendation

Write findings to: {output_path}/architecture_findings.md
```

## Step 3: Collect and Deduplicate Findings

As agents complete, read their findings files. Merge all findings into a single
list, then:

1. **Remove duplicates** — if multiple agents found the same issue (e.g., security
   and quality both flag missing input validation), keep the one with higher severity
   and richer description.
2. **Cross-reference with existing issues** — check each finding against the
   deduplication list from Step 1. If an existing issue already covers a finding,
   note it and skip.
3. **Filter noise** — remove findings that are:
   - Too vague to be actionable ("code could be improved")
   - False positives (the code is actually correct, the agent misread it)
   - Already handled by existing tooling (linter rules, CI checks)

   To verify uncertain findings, read the actual code at the reported location
   and confirm the issue is real before including it.

4. **Sort by severity** — Critical first, then Major, Minor, Trivial.

## Step 4: Present Findings and Get Confirmation

Present the consolidated findings to the user. Group by domain for readability.

```
## Audit Results — {N} Finding(s)

**Scope**: {scope or "entire project"}
**Domains analyzed**: {list of domains}
**Agents completed**: {count}/{total}

### Critical ({count})
| # | Domain | Finding | File | Severity |
|---|--------|---------|------|----------|
| 1 | Security | {title} | {file:line} | Critical |

### Major ({count})
| # | Domain | Finding | File | Severity |
|---|--------|---------|------|----------|

### Minor ({count})
...

### Skipped ({count})
- {finding} — already tracked as {existingIssueId}
- {finding} — false positive (verified code is correct)
```

Use `AskUserQuestion` to let the user select which findings to create as issues:

- Question: "Which findings should I create as tracked issues?"
- Header: "Create issues"
- multiSelect: true
- Options: Group findings sensibly — e.g., "All Critical + Major ({N})",
  individual critical findings, "All ({N})", "None"

If there are more than 4 findings to choose from, batch the options:
- "All Critical + Major ({N})" (recommended)
- "All findings ({N})"
- "Let me pick individually" (then ask per-finding)
- "None — just keep the report"

## Step 5: Create Issues

For each confirmed finding, call `mcp__pinkrooster__create_or_update_issue` with:

- `projectId`
- `name`: concise title, e.g., "Security: Missing input validation on project path parameter"
- `description`: comprehensive description including:
  - What the problem is
  - Where it occurs (file path, line numbers)
  - Why it matters (impact, risk)
  - How to fix it (concrete recommendation from the agent)
  - Which analysis domain found it
- `issueType`: mapped from domain:
  - Security findings → `SecurityVulnerability`
  - Performance findings → `PerformanceIssue`
  - Quality findings → `Bug` (if causes incorrect behavior) or `TechnicalDebt` (if maintainability)
  - Architecture findings → `TechnicalDebt`
- `severity`: mapped from finding severity (Critical/Major/Minor/Trivial)
- `priority`: derived from severity:
  - Critical severity → `Critical` priority
  - Major severity → `High` priority
  - Minor severity → `Medium` priority
  - Trivial severity → `Low` priority
- `affectedComponent`: extracted from the file path (e.g., "PinkRooster.Api",
  "Dashboard", "PinkRooster.Mcp")

## Step 6: Report Results

```
## Created {count} Issue(s) from Audit

| # | Issue ID | Domain | Name | Severity | Priority |
|---|----------|--------|------|----------|----------|
| 1 | {issueId} | {domain} | {name} | {severity} | {priority} |
| ... |

### Audit Summary
- **Quality**: {count} finding(s), {created} issue(s) created
- **Security**: {count} finding(s), {created} issue(s) created
- **Performance**: {count} finding(s), {created} issue(s) created
- **Architecture**: {count} finding(s), {created} issue(s) created
- **Skipped**: {count} (duplicates or false positives)

### Next Steps
- Scaffold a fix: `/pm-scaffold {issueId}`
- Triage all issues: `/pm-triage`
- Re-audit after fixes: `/pm-audit`
- View project status: `/pm-status`
```

Use `AskUserQuestion` for follow-up:
- Question: "What would you like to do next?"
- Header: "Next step"
- Options: Scaffold highest-severity issue, Triage all, Done

## Constraints

- **Verification is essential.** Analysis agents can produce false positives. Before
  presenting findings, read the actual code at the reported locations for any
  Critical or Major finding. Only create issues for problems you've confirmed exist.
  Minor/Trivial findings can be presented with lower confidence, but note when you
  haven't verified them.
- **Deduplication before creation.** Always check existing issues. Creating duplicate
  issues is worse than missing one — duplicates fragment work and confuse prioritization.
- **Severity must be justified.** Every Critical or Major finding needs a concrete
  explanation of impact. "This could be bad" is not a justification. "This allows
  unauthenticated users to delete any entity via path traversal" is.
- **Issue descriptions must be self-contained.** Someone reading the issue 6 months
  from now should understand the problem, find the affected code, and know how to
  fix it — without needing to re-run the audit.
- **Scope respect.** If `--scope` is set, agents must only analyze files within
  that directory. Don't let findings bleed across boundaries.
- **Proportional output.** A clean codebase should produce few or no issues — don't
  manufacture problems to fill a quota. If the audit finds nothing significant,
  report that confidently: "No significant issues found across {N} domains."
- **Maximum 10 issues per audit.** If the analysis produces more than 10 findings,
  present only the top 10 by severity and let the user know there are more. They
  can re-run with `--focus` to drill into specific domains.
- **Agent timeout handling.** If an analysis agent takes too long or fails, report
  which domain was incomplete and suggest re-running with `--focus` for that domain.
