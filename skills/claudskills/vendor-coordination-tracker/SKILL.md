---
name: vendor-coordination-tracker
description: Tracks every outstanding vendor coordination item across active transactions — inspectors, appraisers, contractors, title companies, lenders, and attorneys — surfacing what has been scheduled, what is pending, and what is blocking a transaction. Use when an agent wants to ensure all third-party coordination is on track across their deals. Triggers on "vendor coordination", "third party status", "what's pending with vendors", "inspector scheduler", "transaction vendor tracker", "who have I not heard back from".
metadata:
  version: 1.0.0
---

# Vendor Coordination Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all transaction-related email threads to find every vendor coordination
item — inspections, appraisals, contractor visits, title searches, lender
approvals, and attorney reviews — tracking what has been confirmed, what is
awaiting a response, and what is blocking a deal from moving forward.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last quarter", "May 2024",
     "since the new contract"). Default: the last 90 days. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [deal_scope] — either "all" (default) or a specific deal or
     property to focus on.
   - [deal_clause] — derived. When [deal_scope] is not "all", set to
     " for [deal_scope]". When [deal_scope] is "all", set to empty
     string.

2. Call search with:
   - query: inspector appraiser contractor title attorney lender mortgage
     schedule confirm appointment repair estimate
     (if [deal_scope] is not "all", append the deal or property to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all real estate transaction email threads from [time_range][deal_clause]. For each active deal, identify every vendor coordination item — inspection appointments, appraisal scheduling, contractor estimates, title searches, lender communication, and attorney reviews. For each item note the vendor type, the property, what was requested, whether it has been confirmed or completed, any outstanding response needed, and whether it is on the critical path to closing.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Vendor coordination tracker across all active real estate transactions",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "coordination_items": {
           "type": "array",
           "description": "List of every vendor coordination item found across active transactions",
           "items": {
             "type": "object",
             "description": "A single vendor coordination item with current status",
             "additionalProperties": false,
             "properties": {
               "property": {
                 "type": "string",
                 "description": "Property address or description this coordination item relates to"
               },
               "vendor_type": {
                 "type": "string",
                 "description": "Type of vendor or third party involved",
                 "enum": [
                   "home_inspector", "appraiser", "contractor", "title_company",
                   "lender", "attorney", "surveyor", "pest_inspector",
                   "stager", "photographer", "other"
                 ]
               },
               "vendor_name": {
                 "type": "string",
                 "description": "Name of the specific vendor or company, empty string if not identified"
               },
               "task": {
                 "type": "string",
                 "description": "Description of what needs to be done or has been requested"
               },
               "status": {
                 "type": "string",
                 "description": "Current status of this coordination item",
                 "enum": [
                   "scheduled", "awaiting_confirmation", "completed",
                   "awaiting_report", "in_progress", "not_yet_contacted",
                   "overdue", "unknown"
                 ]
               },
               "scheduled_date": {
                 "type": "string",
                 "description": "ISO8601 date of the scheduled appointment or deadline, empty string if not set"
               },
               "days_until_scheduled": {
                 "type": "number",
                 "description": "Number of days until the scheduled date, -1 if not set"
               },
               "on_critical_path": {
                 "type": "boolean",
                 "description": "Whether this item must be completed before the transaction can close"
               },
               "blocking_issue": {
                 "type": "string",
                 "description": "Any issue blocking this coordination item from progressing, empty string if none"
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended next step for this coordination item"
               }
             },
             "required": [
               "property", "vendor_type", "vendor_name", "task", "status",
               "scheduled_date", "days_until_scheduled", "on_critical_path",
               "blocking_issue", "recommended_action"
             ]
           }
         },
         "awaiting_response_count": {
           "type": "number",
           "description": "Number of coordination items awaiting a vendor response"
         },
         "critical_path_blocked_count": {
           "type": "number",
           "description": "Number of critical path items that are blocked or overdue"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of overall vendor coordination status and most urgent gaps"
         }
       },
       "required": [
         "as_of", "coordination_items", "awaiting_response_count",
         "critical_path_blocked_count", "summary"
       ]
     }
   }

4. Present critical path items first, ordered by days until scheduled.
   Flag overdue and awaiting confirmation items prominently. Lead with
   critical_path_blocked count and awaiting_response count.

5. Ask: "Would you like me to draft follow-up messages to any vendors
   who have not responded?"
