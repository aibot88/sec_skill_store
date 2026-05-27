---
name: auditing-seo
description: Analyzes a single web page URL for SEO quality, identifying issues with title tags, meta descriptions, heading structure, and content. Use when the user says "audit this page", "check SEO for", or "analyze this URL for SEO". Outputs a structured audit report with prioritized fixes.
argument-hint: [url]
---

# SEO Page Auditing SOP

## Execution Steps

### Step 1: Fetch Page Content
Use `read_url_content` to fetch and read the raw content of `$ARGUMENTS` (the URL provided by the user).

### Step 2: Analyze On-Page SEO Elements
Check and score each of the following elements:
- **Title Tag:** Present? Under 60 characters? Contains primary keyword?
- **Meta Description:** Present? Under 160 characters? Has a call-to-action?
- **H1:** Exactly one H1 present? Does it match the topic of the title?
- **Heading Hierarchy:** Is H2 > H3 structure logical and sequential?
- **Image Alt Text:** Do all `<img>` tags have descriptive alt attributes?
- **Internal Links:** Are there at least 2 internal links present?

### Step 3: Compile Prioritized Fix List
Organize the findings into 3 tiers:
- **Critical:** Issues that directly harm rankings (e.g., missing title, no H1).
- **Important:** Issues that limit performance (e.g., meta description too long).
- **Suggestions:** Nice-to-have improvements.

### Step 4: Validate Completeness
Review the audit against the elements in Step 2. If any element was skipped or could not be assessed, note it explicitly. Re-check that every Critical item has a specific, actionable fix.

### Step 5: Deliver the Report
Output the full audit as a formatted Markdown table with: Element | Status | Current Value | Recommended Fix.
