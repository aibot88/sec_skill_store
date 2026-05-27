---
name: endor-ai-sast
description: >
  Fetch and display AI-powered SAST findings from the Endor Labs platform. Default path is
  summary-only (aggregated counts + clusters); full masked listing runs only when the user
  asks to drill down (speed and token use). Use when the user says "AI SAST results",
  "AI SAST findings", "AI static analysis", "endor ai sast", "show AI SAST", or wants
  pre-computed AI-driven code security findings. Do NOT use for running a new SAST scan
  (/endor-sast), viewing general findings (/endor-findings), or explaining a specific CVE
  (/endor-explain).
---

# Endor Labs AI SAST Analysis

Fetch AI-powered static analysis security findings using pre-computed data from the Endor Labs platform.

## Prerequisites

- Endor Labs authenticated (run `/endor-setup` if not)

## Workflow

**Two phases (default: Phase 1 only):**

| Phase | API calls | Purpose |
|-------|-----------|---------|
| **1 — Summary** | **3a** + **3b** only | Severity table + cluster lines. **Minimizes latency and token use.** Do **not** run **3c**. |
| **2 — Detail** | **3c** (on user request) | `spec.explanation`, per-finding locations, data flow, filtered tables. Run only what the user asked for; **prefer a tighter filter** over loading the full list when possible. |

### Step 1: Resolve Namespace

Before making ANY `endorctl api` call, resolve the namespace.

```bash
export ENDOR_NAMESPACE="${ENDOR_NAMESPACE:-$(grep -E '^ENDOR_NAMESPACE:' ~/.endorctl/config.yaml 2>/dev/null | awk '{print $2}' | tr -d '"')}"
echo "ENDOR_NAMESPACE=$ENDOR_NAMESPACE"
```

If empty, run `/endor-setup` to authenticate and set the namespace.

### Step 2: Find the Project UUID

Get the git remote URL, normalize it to HTTPS format, then query for the project. **Only run this after Step 1 succeeds.**

```bash
RAW_URL=$(git remote get-url origin 2>/dev/null)
# Normalize SSH URLs (git@github.com:org/repo.git) to HTTPS (https://github.com/org/repo.git)
if echo "$RAW_URL" | grep -q '^git@'; then
  GIT_URL="https://$(echo "$RAW_URL" | sed 's|^git@||; s|:|/|')"
else
  GIT_URL="$RAW_URL"
fi
npx -y endorctl api list --resource Project -n $ENDOR_NAMESPACE \
  --filter "spec.git.http_clone_url=='$GIT_URL'" \
  --field-mask="uuid,meta.name" 2>&1 | tee /tmp/endor_list_project_output.txt
```

For CLI field paths and parsing gotchas, read references/cli-parsing.md.

Run this command ONCE with the normalized URL. Do NOT retry with URL variations. If the project is not found, see Error Handling.

### Step 3: Fetch AI SAST Findings

Use the **same base filter** on every call below (advanced list API; grouping pattern aligns with `/endor-api` / `endorctl api list` filter syntax).

Base filter (repeat in **3a**, **3b**, and **3c**):

`'context.type == CONTEXT_TYPE_MAIN and spec.project_uuid == "{PROJECT_UUID}" and spec.method == SYSTEM_EVALUATION_METHOD_DEFINITION_AI_SAST'`

#### Step 3a: Severity summary (run first — fast)

One grouped query returns counts per `spec.level` without pulling explanations or large payloads:

```bash
npx -y endorctl api list -r Finding -n $ENDOR_NAMESPACE \
  -f 'context.type == CONTEXT_TYPE_MAIN and spec.project_uuid == "{PROJECT_UUID}" and spec.method == SYSTEM_EVALUATION_METHOD_DEFINITION_AI_SAST' \
  --group-aggregation-paths "spec.level" \
  | tee /tmp/endor_ai_sast_summary.txt
```

Use stdout-only piping to `tee` (do **not** use `2>&1`) so the saved file stays pure JSON for `jq`. Endorctl writes upgrade notices to stderr.

**Short-circuit:** If the grouped response has **no findings** (total count is 0), respond with exactly: `"No AI SAST findings are available for this project at this moment."` — no further explanation. **Do not run Steps 3b or 3c** (there is nothing to drill into).

Total count (for the short-circuit check and the summary **Total** row):

```bash
jq '[(.group_response.groups // {}) | to_entries[] | .value.aggregation_count.count] | add // 0' /tmp/endor_ai_sast_summary.txt
```

Optional: map enum levels to counts for the summary table (parse `group_response`):

```bash
jq -r '.group_response.groups // {} | to_entries[] | (.key | fromjson | .[] | select(.key=="spec.level") | .value) as $lvl | "\($lvl) \(.value.aggregation_count.count)"' /tmp/endor_ai_sast_summary.txt
```

#### Step 3b: Vulnerability clusters (fast — only if Step 3a shows at least one finding)

Two grouped queries replace parsing the full listing for **cluster counts**, **distinct files per cluster**, and **severity mix per cluster** (for titles like `[Critical/High]`). Run both after **3a** succeeds.

**3b(i)** — Total findings and **distinct file paths** per `meta.description`:

```bash
npx -y endorctl api list -r Finding -n $ENDOR_NAMESPACE \
  -f 'context.type == CONTEXT_TYPE_MAIN and spec.project_uuid == "{PROJECT_UUID}" and spec.method == SYSTEM_EVALUATION_METHOD_DEFINITION_AI_SAST' \
  --group-aggregation-paths "meta.description" \
  --group-unique-count-paths "spec.dependency_file_paths" \
  | tee /tmp/endor_ai_sast_cluster_counts.txt
```

Per-cluster finding count: `aggregation_count.count`. Distinct locations: `unique_counts.spec.dependency_file_paths.count`.

**3b(ii)** — Counts per **`meta.description` × `spec.level`** (derive highest severity present and multi-level labels for Step 4b):

```bash
npx -y endorctl api list -r Finding -n $ENDOR_NAMESPACE \
  -f 'context.type == CONTEXT_TYPE_MAIN and spec.project_uuid == "{PROJECT_UUID}" and spec.method == SYSTEM_EVALUATION_METHOD_DEFINITION_AI_SAST' \
  --group-aggregation-paths "meta.description" \
  --group-aggregation-paths "spec.level" \
  | tee /tmp/endor_ai_sast_cluster_severity.txt
```

Each `group_response.groups` key is a JSON array of `{key, value}` pairs (description and level). Sum `aggregation_count.count` over entries that share the same `meta.description` to match **3b(i)** totals. For each description, note which `FINDING_LEVEL_*` values appear to sort clusters and to label `[Critical]`, `[High]`, `[Critical/High]`, etc.

#### Step 3c: Full findings (Phase 2 only — when the user asks for detail)

**Do not run in the default flow.** Run **3c** only after the user chooses a drill-down (see **Step 4d**). This call pulls large `spec.explanation` text; keep it **scoped** to what they asked for.

**Default 3c command** (entire AI SAST set — use only if they want everything, e.g. "load all findings" or "full report"):

```bash
npx -y endorctl api list -r Finding -n $ENDOR_NAMESPACE \
  -f 'context.type == CONTEXT_TYPE_MAIN and spec.project_uuid == "{PROJECT_UUID}" and spec.method == SYSTEM_EVALUATION_METHOD_DEFINITION_AI_SAST' \
  --field-mask meta.description,spec.explanation,spec.dependency_file_paths,spec.level \
  --list-all \
  | tee /tmp/endor_sast_findings_output.txt
```

**Prefer narrower filters** (append to the base filter with `and ...`) to cut volume and tokens:

| User request | Add to filter (examples) |
|--------------|-------------------------|
| Critical only | `and spec.level==FINDING_LEVEL_CRITICAL` |
| High and Critical | `and spec.level in [FINDING_LEVEL_CRITICAL, FINDING_LEVEL_HIGH]` |
| One cluster / CWE | `and meta.description contains "SQL Injection"` (match substring of the full `meta.description` string) |
| One file | `and spec.dependency_file_paths contains "path/to/file.cs"` (if the API supports `contains` on that field; otherwise run full **3c** and filter in presentation) |

Re-run **3c** when the user’s *next* question needs different fields or a different filter; do not load the full list preemptively.

### Step 4: Present Results

**Phase 1 (default):** Present **4a** and **4b** from **3a** and **3b** only. **Stop** after **4d** (drill-down prompt) — do **not** run **3c**, do **not** show **4c** unless the user continues to Phase 2.

**Phase 2:** After the user answers **4d** (or explicitly asks for detail), run **3c** as needed, then **4c** / full drill-down content. The goal is to answer "what should I worry about?" first with **minimal** API and context size, then pay for detail on demand.

#### 4a: Severity Breakdown

Build the summary count table from **Step 3a** (map `FINDING_LEVEL_*` to Critical / High / Medium / Low). If you already showed counts from 3a, keep this section brief:

```
## AI SAST Findings Summary

| Severity | Count |
|----------|-------|
| Critical | X     |
| High     | X     |
| Medium   | X     |
| Low      | X     |
| **Total**| **X** |
```

#### 4b: Actionable Groups

Build clusters from **Step 3b**: use **`meta.description`** strings from the grouped responses (not the full **Step 3c** list). **3b(i)** supplies finding counts and distinct file counts (`N findings across M files`). **3b(ii)** supplies which severity levels appear per description — map to short severity labels for each cluster (sort by highest severity present, then by count).

**Short titles:** Use concise names in the output, not full CWE descriptions. Map verbose `meta.description` values to short labels:

| `meta.description` contains | Short title |
|-----|------|
| SQL Command | SQL Injection |
| Cross-site Scripting / Web Page Generation | XSS |
| Code Injection / Generation of Code | Code Injection |
| Path Traversal / Pathname to a Restricted Directory | Path Traversal |
| Authorization Bypass Through User-Controlled Key | Authorization Bypass (IDOR) |
| Missing Authorization / Missing Authentication | Missing Auth |
| Sensitive Information into Log | Sensitive Info in Logs |
| Hard-coded Credentials / Hard-coded Cryptographic | Hard-coded Credentials |
| Cleartext Storage | Cleartext Storage |
| Cleartext Transmission | Cleartext Transmission |
| Exposure of Sensitive Information | Info Disclosure |
| XML External Entity | XXE |
| Server-Side Request Forgery | SSRF |
| NoSQL / MongoDB | NoSQL Injection |
| Cryptographic Signature / Password Hash | Weak Cryptography |
| Deserialization of Untrusted Data | Insecure Deserialization |
| Open Redirect / URL Redirection | Open Redirect |
| Rate Limit | Rate Limit Bypass |
| Privilege Management / Incorrect Authorization | Broken Access Control |
| Denial of Service / Resource Exhaustion / Resource Consumption | DoS |
| Improper Handling of Exceptional Conditions / NULL Pointer | Error Handling |
| Improper Input Validation | Input Validation |
| Business Logic | Business Logic Flaw |
| Unhandled.*Error / Unhandled.*Exception | Unhandled Error |
| Insecure Design | Insecure Design |
| Improper Verification | Improper Verification |
| (anything else) | Use the parenthesized short name if present, otherwise use the full title |

**Only show clusters with 2+ findings.** Sort by highest severity in the group, then by count descending. For each cluster show:

```
### Vulnerability Clusters

- **SQL Injection** (6 findings across 5 files) [Critical] — use parameterized queries across all SQL operations
- **XSS** (8 findings across 7 files) [Critical/High] — audit all uses of bypassSecurityTrustHtml and innerHTML
- **Authorization Bypass (IDOR)** (5 findings across 4 files) [High] — enforce server-side ownership checks in middleware
```

**Remediation suggestions (Phase 1):** Use the **generic** mapping below — one line per cluster. Do **not** run **3c** just to tailor text. After Phase 2, you may refine using `spec.explanation` from **3c**.

| Cluster | Remediation |
|---------|-------------|
| SQL Injection | use parameterized queries across all SQL operations |
| XSS | audit all uses of bypassSecurityTrustHtml and innerHTML; use Angular sanitization |
| Code Injection | remove eval/safeEval usage; use safe alternatives |
| Path Traversal | validate and canonicalize file paths; reject `..` sequences |
| Authorization Bypass (IDOR) | enforce server-side ownership checks in middleware |
| NoSQL Injection | use typed query builders; never concatenate user input into $where clauses |
| Missing Auth | add authentication/authorization middleware to exposed endpoints |
| Sensitive Info in Logs | sanitize error objects before logging; avoid console.log of raw errors |
| Hard-coded Credentials | move secrets to environment variables or a vault |
| Cleartext Storage / Transmission | use httpOnly secure cookies instead of localStorage |
| Info Disclosure | restrict endpoint access and filter sensitive fields from responses |
| SSRF | validate URL scheme and host against an allowlist before server-side fetch |
| XXE | disable external entity processing in XML parser configuration |
| Rate Limit Bypass | use trusted client IP (not X-Forwarded-For) or validate proxy headers |
| Open Redirect | validate redirect targets against an allowlist of trusted domains |
| Weak Cryptography | use bcrypt/scrypt for passwords; verify JWT signatures server-side |
| Insecure Deserialization | use safe loaders (e.g., yaml.safeLoad); validate input schema before parsing |
| DoS | add input size limits and validation before resource allocation |
| Broken Access Control | verify user roles/permissions server-side on every request |
| Error Handling | add null/undefined checks and error boundaries; validate assumptions before dereferencing |
| Input Validation | validate and sanitize all user-controlled input at system boundaries |
| Business Logic Flaw | add server-side validation for business rules; don't trust client-supplied IDs or amounts |
| Unhandled Error | wrap I/O operations in try/catch; handle missing files and failed calls gracefully |
| Insecure Design | enforce resource limits and validate contracts before processing |
| Improper Verification | verify signatures and integrity server-side; don't trust client-decoded tokens |

After the multi-finding clusters, add a single rollup line for all single-finding types:

```
- *+ N other finding types with 1 finding each (use drill-down to explore)*
```

In Phase 2, use `spec.explanation` to sharpen remediation if it contradicts the generic line.

#### 4c: Critical Findings Detail (Phase 2 — requires **3c** first)

Only after the user asks for per-finding detail (e.g. Critical table, file list, explanations). Run **3c** with `and spec.level==FINDING_LEVEL_CRITICAL` when they want Critical-only — **do not** pull the full finding set unless they ask.

Using **Step 3c** output, show a **compact one-line-per-finding table** for **Critical severity** when that was the ask (for other severities or clusters, filter **3c** accordingly):

```
### Critical Findings

| # | Title | Location | Summary |
|---|-------|----------|---------|
```

- **Title**: short title (use the same short title mapping from Step 4b, not the full CWE description)
- **Location**: value of `spec.dependency_file_paths`
- **Summary**: one-sentence summary extracted from `spec.explanation` (everything after `## Summary`, truncated to the first sentence or ~150 characters)

Sort rows by vulnerability type (group related findings together).

**Title/summary cross-check:** If the `spec.explanation` summary clearly describes a different vulnerability class than `meta.description` suggests (e.g., `meta.description` says "SQL Injection" but the summary describes a MongoDB `$where` NoSQL injection), use the **summary-derived type** for the short title in the table. The summary is closer to the actual finding; `meta.description` can be a rough CWE category that doesn't match the specific issue.

**Do NOT include the Data Flow column** until the user asks for it (Phase 2). Data flow lives under `spec.explanation` (see **4d**).

#### 4d: End Phase 1 — Drill-Down Prompt (always show this after 4a + 4b)

Phase 1 **ends here.** Ask what to load next — **do not** run **3c** until the user replies.

```
---
**Summary only so far** (no explanations or file-level detail loaded — fast / low tokens).

**What should we drill into?** Examples:
- "Critical findings table" → run **3c** with `spec.level==FINDING_LEVEL_CRITICAL`, then **4c**
- "High findings" → **3c** filtered to High (and Critical if they want)
- "Expand XSS cluster" → **3c** with `meta.description contains "Cross-site Scripting"` (match their CWE string from Phase 1)
- "Data flow for finding #3" → run **3c** (narrow filter if they named severity/cluster), locate the finding, paste Data Flow from `spec.explanation`
- "Full explanations for everything" → full **3c** with `--list-all` (expensive — confirm scope if counts are large)
```

#### Phase 2 — After the user chooses

1. Run **3c** with the **smallest** filter that satisfies the request.
2. Present tables or verbatim fields from **3c** output.

Full finding fields for drill-down:

- **Title**: value of `meta.description` — copy verbatim
- **Finding Location**: value of `spec.dependency_file_paths`
- **Severity**: value of `spec.level`
- **Summary**: copy verbatim from `spec.explanation` — everything after `## Summary` up to (but not including) `## Data Flow`
- **Data Flow**: copy verbatim from `spec.explanation` — everything from `## Data Flow` to the end, including all Stage and Location fields

For data source policy, read references/data-sources.md.

## Error Handling

| Error | Action |
|-------|--------|
| Auth error | Run `/endor-setup` |
| License/permission error | Inform user: "AI SAST requires an Endor Labs license. Visit [app.endorlabs.com](https://app.endorlabs.com) or contact your administrator." |
| Project not found | Run `/endor-scan` to onboard the project, then retry `/endor-ai-sast` |
| No findings | Show exact message: "No AI SAST findings are available for this project at this moment." |
