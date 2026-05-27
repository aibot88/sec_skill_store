---
name: security-alert-monitor
description: Scans email threads for security alert signals — phishing reports, suspicious login notifications, data breach mentions, policy violation flags, vulnerability disclosures, and any language suggesting a security incident may be developing. Use when an IT security team wants an early warning scan across their email communications. Triggers on "security alerts", "security incidents from email", "phishing reports", "suspicious activity", "security signal scan", "what security issues are brewing".
metadata:
  version: 1.0.0
---

# Security Alert Monitor

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Reads email threads for security-relevant signals — phishing reports from
employees, suspicious login or access alerts forwarded to IT, data handling
concerns, vulnerability notifications from vendors, policy violations, and
any pattern suggesting a security issue may be developing or has gone
unaddressed.

---

## Workflow

1. Before calling any tool, collect this value from the user. Offer the
   default and let the user override it; do not invent a value they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 30 days", "the last month", "May 2024",
     "since the phishing campaign"). Default: the last 30 days. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.

2. Call search with:
   - query: phishing suspicious login unauthorized access breach
     vulnerability security alert policy violation data leak malware
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range] for security-relevant signals. Look for: phishing emails reported by employees, suspicious login or access alerts forwarded to IT, data handling concerns or potential breaches mentioned, vulnerability disclosures from vendors or security services, IT policy violations, and any pattern suggesting a security incident may be developing or has not been properly addressed. For each signal note the type, the evidence, who is involved, and urgency.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "Security alert monitor report from email-based signals",
   "additionalProperties": false,
   "properties": {
   "period_from": {
   "type": "string",
   "description": "ISO8601 start date of the period scanned"
   },
   "period_to": {
   "type": "string",
   "description": "ISO8601 end date of the period scanned"
   },
   "alerts": {
   "type": "array",
   "description": "List of every security alert signal found in email threads",
   "items": {
   "type": "object",
   "description": "A single security alert signal with context and urgency",
   "additionalProperties": false,
   "properties": {
   "alert_type": {
   "type": "string",
   "description": "Category of security alert",
   "enum": [
   "phishing_report", "suspicious_login", "unauthorized_access",
   "data_breach_signal", "vulnerability_disclosure", "malware_report",
   "policy_violation", "vendor_security_notice",
   "credential_exposure", "other"
   ]
   },
   "description": {
   "type": "string",
   "description": "Clear description of the security signal and why it is a concern"
   },
   "evidence": {
   "type": "string",
   "description": "Quote or paraphrase from email that surfaces this alert"
   },
   "reported_by": {
   "type": "string",
   "description": "Name or role of the person who reported or surfaced this signal"
   },
   "systems_or_users_affected": {
   "type": "string",
   "description": "Description of which systems or users may be affected, empty string if unknown"
   },
   "date": {
   "type": "string",
   "description": "ISO8601 date when this signal appeared in email"
   },
   "severity": {
   "type": "string",
   "description": "Severity of this security signal",
   "enum": ["critical", "high", "medium", "low"]
   },
   "status": {
   "type": "string",
   "description": "Current handling status of this security alert",
   "enum": [
   "unaddressed", "investigating", "contained",
   "remediated", "monitoring", "false_positive", "unknown"
   ]
   },
   "recommended_action": {
   "type": "string",
   "description": "Recommended immediate action for this security signal"
   }
   },
   "required": [
   "alert_type", "description", "evidence", "reported_by",
   "systems_or_users_affected", "date", "severity",
   "status", "recommended_action"
   ]
   }
   },
   "critical_count": {
   "type": "number",
   "description": "Number of critical severity security alerts"
   },
   "unaddressed_count": {
   "type": "number",
   "description": "Number of security alerts with no evidence of being addressed"
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of the security alert landscape and most urgent items"
   }
   },
   "required": [
   "period_from", "period_to", "alerts",
   "critical_count", "unaddressed_count", "summary"
   ]
   }
   }

4. Present critical and unaddressed alerts first, ordered by severity.
   Lead with critical count and unaddressed count.

5. Tell the user: "For any critical or data breach signals, engage your
   security incident response process immediately rather than relying on
   email triage alone."