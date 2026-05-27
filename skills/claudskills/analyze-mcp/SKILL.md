---
name: mcp-architect-analyze-mcp
description: "Analyze existing MCP server implementation for optimization opportunities and best practice compliance. 分析現有MCP服務器實現，識別優化機會與最佳實踐合規性。"
disable-model-invocation: true
argument-hint: "\"[path-to-mcp]\""
allowed-tools: "[Read, Glob, Grep, Write]"
---

# Analyze MCP Server

審查現有MCP服務器實現，識別以下改進機會：
- Tool organization improvements
- Token efficiency optimizations
- Progressive discovery enhancements
- Better automation flag usage
- Cross-tool ID systems

## Process

### Step 1: Discover MCP Structure

詢問用戶MCP位置：
- Directory containing MCP server code
- Specific files to analyze
- Running MCP server endpoint (if applicable)

Use Glob and Grep to find:
- Tool definitions
- Server metadata/configuration
- Response formats
- Documentation

### Step 2: Analyze Architecture

Review and assess:

**Tool Organization:**
- [ ] Tools grouped logically?
- [ ] Naming follows verb-noun pattern?
- [ ] Clear categories/domains?
- [ ] Tool count appropriate (not too flat)?

**Token Systems:**
- [ ] Uses IDs for cross-tool references?
- [ ] Avoids repeating data?
- [ ] ID format clear and consistent?

**Progressive Discovery:**
- [ ] Has info/help tool?
- [ ] Progressive detail levels?
- [ ] Clear next steps for users?

**Response Format:**
- [ ] Automation flags present?
- [ ] Human and machine readable?
- [ ] Sparse tables where appropriate?
- [ ] Standard JSON arrays for data?

**Error Handling:**
- [ ] Accepts extra parameters gracefully?
- [ ] Clear error messages?
- [ ] Graceful degradation?

### Step 3: Generate Analysis Report

Create markdown report with:

**Summary:**
```markdown
# MCP Analysis: [server-name]

## Overview
- Tools: X total
- Pattern: [detected pattern]
- Token efficiency: [assessment]
- Progressive discovery: [yes/no]

## Strengths
- [What's working well]

## Opportunities
- [Improvements to consider]

## Recommendations
- [Specific actionable items]
```

**Detailed Findings:**

For each category, provide:
1. **Current state** - What exists now
2. **Assessment** - Good/needs improvement
3. **Recommendation** - Specific changes
4. **Example** - Before/after if applicable
5. **Impact** - Token savings or UX improvement

**Example finding:**

```markdown
### Token Efficiency

**Current:** search tool returns full code blocks (avg 250 tokens per result)

**Assessment:** ⚠️  Wasteful - repeating large code blocks

**Recommendation:** Return IDs with previews, use get_details(id) for full code

**Example:**
Before:
```json
{"results": [{"code": "... 200 lines ..."}]}
```

After:
```json
{"results": [{"id": "r1", "preview": "10 lines"}]}
```

**Impact:** 80% token reduction (250 → 50 tokens per result)
```

### Step 4: Prioritize Recommendations

按影響力排列建議：

**High Impact (implement first):**
- ID systems for cross-tool references (70-90% token savings)
- Progressive detail by confidence (50-70% savings)
- Accept extra parameters (robustness)

**Medium Impact:**
- Info tool for discovery (better UX)
- Automation flags (AI agent friendliness)
- Tool grouping (organization)

**Low Impact (nice to have):**
- Sparse tables in info output
- Consistent naming
- Additional workflows documentation

### Step 5: Output Report

Write analysis to file:
- Default: `./mcp-analysis-{name}.md`
- Ask user for custom path if preferred
- Provide summary of findings

## Analysis Criteria

### Architecture Patterns

識別MCP使用哪種模式：
- Hub-and-Spoke
- CRUD
- Discovery-Detail
- Aggregation
- Pipeline
- Lazy Loading

評估模式是否適合用例。

### Token Efficiency Score

Calculate based on:
- Uses ID references: +40 points
- Progressive detail: +30 points
- Selective fields: +15 points
- Flattened schemas: +10 points
- Reference system for repeated values: +5 points

**Score interpretation:**
- 90-100: Excellent
- 70-89: Good
- 50-69: Needs improvement
- <50: Significant issues

### Progressive Discovery Score

- Has info tool: +30 points
- Multiple detail levels: +25 points
- Clear workflows: +20 points
- Category organization: +15 points
- Help/documentation: +10 points

**Score interpretation:**
- 80-100: Excellent discoverability
- 60-79: Good
- 40-59: Basic
- <40: Poor discoverability

## Output Format

**Sparse table summary:**

```
MCP Analysis Summary
====================

Server: code-search
Tools: 12
Pattern: Hub-and-Spoke ✓

Scores
------
Category             | Score | Assessment
-------------------- | ----- | ----------
Token Efficiency     | 85    | Good
Progressive Discovery| 65    | Good
Architecture         | 90    | Excellent
Error Handling       | 40    | Needs improvement

Top 3 Recommendations
---------------------
1. Add error handling for malformed patterns (High impact)
2. Implement info tool for discovery (Medium impact)
3. Use consistent error code format (Medium impact)

Estimated Token Savings: 70-80% with ID system implementation

Full report: ./mcp-analysis-code-search.md
```

## Example Analyses

### Example 1: MCP with No ID System

**Finding:**
```markdown
### Token Efficiency: ⚠️  Needs Improvement (Score: 30/100)

**Issue:** All tools return complete data, no cross-tool references

**Current workflow:**
1. search("User") → Returns full User objects (500 tokens each)
2. User copies entire object to next tool
3. get_details(entire_user_object) → Redundant

**Recommendation:** Implement ID system

**Proposed workflow:**
1. search("User") → Returns [{id: "u1", name: "User", preview: "..."}]
2. get_details("u1") → Returns full details

**Impact:** 85% token reduction (500 → 75 tokens for search results)

**Implementation:**
```typescript
// Add ID generation to search tool
function search(pattern) {
  const results = performSearch(pattern)
  return results.map((r, i) => ({
    id: generateId(i),
    name: r.name,
    preview: r.code.substring(0, 100)
  }))
}

// Update get_details to accept ID
function get_details(id) {
  const full = lookupById(id)
  return full
}
```
```

### Example 2: MCP with Poor Discovery

**Finding:**
```markdown
### Progressive Discovery: ⚠️  Poor (Score: 20/100)

**Issue:** No info tool, users don't know what's available

**Current:** 15 tools, no categorization, no help system

**Recommendation:** Add info tool with categories

**Implementation:**
```typescript
function info(category?: string) {
  if (!category) {
    // Overview
    return {
      categories: [
        {name: "query", count: 3, description: "Search and find"},
        {name: "lookup", count: 5, description: "Get details"},
        {name: "management", count: 4, description: "Create/update/delete"}
      ],
      total: 12,
      next: "Use info(category='query') for tools in category"
    }
  }

  // Category detail
  return getToolsInCategory(category)
}
```

**Impact:** 用戶無需試錯即可發現能力
```

## Additional Resources

> Invoke the `Skill` tool with `skill: mcp-architect:mcp-architecture` — 架構模式深入參考。

> Invoke the `Skill` tool with `skill: mcp-architect:response-optimization` — 響應優化與token效率模式。

> Invoke the `Skill` tool with `skill: mcp-architect:client-guidance` — 錯誤響應漸進增強模式。

## Tips

- **Be specific** - 不只說「提升token效率」，展示具體變更
- **Show examples** - Before/after代碼片段
- **Quantify impact** - Token節省百分比、用戶體驗改進
- **Prioritize** - 聚焦高影響力改進
- **Be constructive** - 以機會而非批評表述

目標：提供可操作的建議，無需完全重寫即可改善MCP。
