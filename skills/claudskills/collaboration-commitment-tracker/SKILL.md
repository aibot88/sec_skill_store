---
name: collaboration-commitment-tracker
description: Tracks every commitment made across active research collaborations from email — data sharing promises, co-authorship agreements, analysis contributions, review commitments, and meeting obligations — surfacing those that are unmet or at risk. Use when a researcher wants to hold collaborators accountable and ensure their own commitments are on track. Triggers on "collaboration commitments", "what have collaborators promised", "co-author obligations", "research partnership commitments", "what am I on the hook for with collaborators", "collaboration tracker".
metadata:
  version: 1.0.0
---

# Collaboration Commitment Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans research collaboration email threads to extract every commitment made
by any party — data to be shared, analyses to be run, sections to be written,
reviews to be completed, meetings to be arranged — and tracks whether each
has been fulfilled, is in progress, or has gone silent.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 6 months", "the last 90 days", "May 2024",
     "since the kickoff"). Default: the last 6 months. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [scope] — either "all" (default) or the name of a specific project
     or collaborator to focus on.
   - [scope_clause] — derived. When [scope] is not "all", set to " for
     [scope]". When [scope] is "all", set to empty string.

2. Call search with:
   - query: will send share provide run analysis write review commit
     collaborate joint contribution co-author agree data collaborator
     (if [scope] is not "all", append the project or collaborator name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all research collaboration email threads from [time_range][scope_clause]. For every active collaboration, extract every commitment made by any party — data to be shared, analyses promised, sections to be drafted, review tasks accepted, meeting arrangements, and any other formal or informal obligation. For each commitment note who made it, to whom, when, any deadline given, and whether there is evidence of fulfillment or whether it remains open. Distinguish commitments we made from those made by collaborators.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "Collaboration commitment tracker across all active research partnerships",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this report was generated"
   },
   "commitments": {
   "type": "array",
   "description": "List of every collaboration commitment found across research email threads",
   "items": {
   "type": "object",
   "description": "A single collaboration commitment with context and status",
   "additionalProperties": false,
   "properties": {
   "project": {
   "type": "string",
   "description": "Research project or collaboration this commitment relates to"
   },
   "commitment_description": {
   "type": "string",
   "description": "Clear description of what was committed to"
   },
   "commitment_type": {
   "type": "string",
   "description": "Category of collaboration commitment",
   "enum": [
   "data_sharing", "analysis_contribution", "writing_contribution",
   "peer_review", "meeting_or_call", "feedback_provision",
   "resource_sharing", "co_authorship", "mentoring", "other"
   ]
   },
   "committed_by": {
   "type": "string",
   "description": "Name or role of the person who made this commitment"
   },
   "direction": {
   "type": "string",
   "description": "Whether this is a commitment we made or one made to us",
   "enum": ["our_commitment", "their_commitment", "mutual", "unknown"]
   },
   "made_on": {
   "type": "string",
   "description": "ISO8601 date the commitment was made"
   },
   "due_by": {
   "type": "string",
   "description": "ISO8601 deadline if given, empty string if open-ended"
   },
   "evidence": {
   "type": "string",
   "description": "Quote or paraphrase from email documenting this commitment"
   },
   "status": {
   "type": "string",
   "description": "Current fulfillment status",
   "enum": ["fulfilled", "in_progress", "open", "overdue", "gone_quiet", "unknown"]
   },
   "days_outstanding": {
   "type": "number",
   "description": "Number of days since this commitment was made with no evidence of progress"
   },
   "risk_level": {
   "type": "string",
   "description": "Risk to the collaboration or project if this commitment is not met",
   "enum": ["high", "medium", "low"]
   }
   },
   "required": [
   "project", "commitment_description", "commitment_type",
   "committed_by", "direction", "made_on", "due_by", "evidence",
   "status", "days_outstanding", "risk_level"
   ]
   }
   },
   "our_overdue_count": {
   "type": "number",
   "description": "Number of commitments we made that are overdue"
   },
   "their_overdue_count": {
   "type": "number",
   "description": "Number of commitments made to us that are overdue or gone quiet"
   },
   "by_project": {
   "type": "array",
   "description": "Commitment status summary grouped by research project",
   "items": {
   "type": "object",
   "description": "Commitment summary for a single collaboration",
   "additionalProperties": false,
   "properties": {
   "project": {
   "type": "string",
   "description": "Name of the research project or collaboration"
   },
   "open_count": {
   "type": "number",
   "description": "Number of open commitments in this collaboration"
   },
   "overdue_count": {
   "type": "number",
   "description": "Number of overdue commitments in this collaboration"
   }
   },
   "required": ["project", "open_count", "overdue_count"]
   }
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of collaboration commitment health and most critical gaps"
   }
   },
   "required": [
   "as_of", "commitments", "our_overdue_count",
   "their_overdue_count", "by_project", "summary"
   ]
   }
   }

4. Present our overdue commitments first — these are the most important to
   address — then their overdue or gone-quiet commitments. Lead with
   our_overdue count and their_overdue count.

5. Ask: "Would you like me to draft a follow-up or commitment update email
   for any of these collaborations?"