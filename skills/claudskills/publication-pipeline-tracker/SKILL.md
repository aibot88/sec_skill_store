---
name: publication-pipeline-tracker
description: Tracks every manuscript, paper, and research output currently in the publication pipeline from email — where each is in the review and submission process, what reviewer feedback is outstanding, what revisions are due, and what co-author actions are needed. Use when a researcher wants a full view of their publication pipeline without checking each journal portal manually. Triggers on "publication pipeline", "manuscript status", "paper submission status", "reviewer feedback", "revisions due", "where are my papers".
metadata:
  version: 1.0.0
---

# Publication Pipeline Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all manuscript and journal-related email threads to map the full
publication pipeline — submission status, editorial decisions, reviewer
feedback received, revision deadlines, co-author contributions outstanding,
and any papers that have gone quiet in the review process.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 12 months", "the last year", "May 2024",
     "since the manuscript was first drafted"). Default: the last 12
     months. Keep the user's natural phrasing for use in the ask input;
     convert to ISO dates separately for the search call.
   - [scope] — either "all" (default) or the name of a specific project
     or journal to focus on.
   - [scope_clause] — derived. When [scope] is not "all", set to " for
     [scope]". When [scope] is "all", set to empty string.

2. Call search with:
   - query: manuscript submission journal review revision accept reject
     decision editor reviewer resubmit under review preprint
     (if [scope] is not "all", append the project or journal name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][scope_clause] related to manuscript submissions and publications. For each paper or manuscript, determine: the title or working title, the target or current journal or venue, the current stage in the submission process, any editorial decision received, reviewer feedback if communicated by email, any revision deadline, co-author actions still required, and whether the paper appears to be progressing or has stalled.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "Publication pipeline tracker across all active manuscripts and submissions",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this report was generated"
   },
   "manuscripts": {
   "type": "array",
   "description": "List of every manuscript in the publication pipeline",
   "items": {
   "type": "object",
   "description": "A single manuscript with full publication pipeline tracking",
   "additionalProperties": false,
   "properties": {
   "working_title": {
   "type": "string",
   "description": "Title or working title of the manuscript"
   },
   "journal_or_venue": {
   "type": "string",
   "description": "Current or target journal or conference venue"
   },
   "submission_type": {
   "type": "string",
   "description": "Type of research output",
   "enum": [
   "journal_article", "conference_paper", "review_article",
   "letter", "preprint", "book_chapter", "technical_report", "other"
   ]
   },
   "stage": {
   "type": "string",
   "description": "Current stage in the publication pipeline",
   "enum": [
   "in_preparation", "internal_review", "submitted",
   "under_review", "major_revision", "minor_revision",
   "accepted", "in_production", "published",
   "rejected_considering_resubmission", "withdrawn", "unknown"
   ]
   },
   "submission_date": {
   "type": "string",
   "description": "ISO8601 date of the most recent submission, empty string if not yet submitted"
   },
   "decision_date": {
   "type": "string",
   "description": "ISO8601 date of the most recent editorial decision, empty string if none received"
   },
   "revision_deadline": {
   "type": "string",
   "description": "ISO8601 deadline for submitting revisions, empty string if not applicable"
   },
   "days_until_revision_deadline": {
   "type": "number",
   "description": "Number of days until the revision deadline, -1 if not applicable"
   },
   "reviewer_feedback_summary": {
   "type": "string",
   "description": "Brief summary of reviewer feedback communicated by email, empty string if not available"
   },
   "co_author_actions_outstanding": {
   "type": "array",
   "description": "Actions still needed from co-authors based on email",
   "items": {
   "type": "string",
   "description": "A single outstanding co-author action"
   }
   },
   "pipeline_health": {
   "type": "string",
   "description": "Overall health of this paper in the pipeline",
   "enum": ["progressing", "revision_due", "stalled", "at_risk", "unknown"]
   },
   "days_since_last_activity": {
   "type": "number",
   "description": "Number of days since the last email activity related to this manuscript"
   }
   },
   "required": [
   "working_title", "journal_or_venue", "submission_type", "stage",
   "submission_date", "decision_date", "revision_deadline",
   "days_until_revision_deadline", "reviewer_feedback_summary",
   "co_author_actions_outstanding", "pipeline_health",
   "days_since_last_activity"
   ]
   }
   },
   "revision_due_count": {
   "type": "number",
   "description": "Number of manuscripts with a pending revision deadline"
   },
   "imminent_revision_count": {
   "type": "number",
   "description": "Number of manuscripts with a revision deadline within the next 14 days"
   },
   "stalled_count": {
   "type": "number",
   "description": "Number of manuscripts that appear to have stalled in the pipeline"
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of the publication pipeline and most urgent items"
   }
   },
   "required": [
   "as_of", "manuscripts", "revision_due_count",
   "imminent_revision_count", "stalled_count", "summary"
   ]
   }
   }

4. Present manuscripts with imminent revision deadlines first, then stalled
   papers, then the rest ordered by stage. Lead with imminent_revision count
   and stalled count.

5. Ask: "Would you like me to draft a co-author action reminder or a
   revision progress update for any of these manuscripts?"