---
name: job-market-intelligence
description: "Uses Claude CLI (WebSearch tool) to find new Data Science and Gen AI job postings across Bengaluru, Hyderabad, Mumbai, and Delhi NCR, scores them by relevance and location weight, stores results in SQLite, generates HTML dashboards, and sends a WhatsApp summary. Use when asked about new job openings, where to apply, or the job market in DS/Gen AI."
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["python3","openclaw"]}}}
---

# Job Market Intelligence Agent

## Description
Use this skill when the user asks to:
- Find new Data Science or Gen AI jobs
- Show where to apply today
- Search for ML / LLM / AI Engineer roles in India
- Check what companies are hiring right now
- Run the job scout manually
- Get a fresh list of job postings

## Tool: find_new_jobs

Runs Claude CLI with the WebSearch tool using the prompt in `prompt.txt`. Claude searches
LinkedIn, Naukri, Glassdoor, and Indeed for recent postings, returns structured JSON, which
is scored by role relevance and location weight, deduplicated against history, stored in
SQLite, rendered as HTML dashboards, and summarised via WhatsApp.

### Usage
```bash
cd /home/zain/zainclaw/job_scout
python3 job_scout.py
```

### Output
- Latest run dashboard: https://claw.mohdzain.com/apply-jobs/latest.html
- All jobs (filterable): https://claw.mohdzain.com/apply-jobs/all.html
- SQLite database: `/home/zain/zainclaw/job_scout/data/jobs.db`
- WhatsApp message with top picks and dashboard links
- Console output with new job count and top picks

### Roles searched
Data Scientist, Gen AI Engineer, ML Engineer, LLM Engineer, AI Researcher

### Locations searched (with relevance weights)
| Location       | Weight |
|----------------|--------|
| Bengaluru      | 0.40   |
| Delhi / NCR    | 0.25   |
| Hyderabad      | 0.20   |
| Mumbai         | 0.15   |
| Remote India   | 0.35   |

### Scoring
- Base score: 50
- Gen AI / LLM in title: +20
- Gen AI / LLM in tags: +12
- ML / DS in title: +10
- Location weight contribution: weight × 30 (e.g., Bengaluru adds +12)
- Remote tag: +5 bonus
- Max score: 100 · Top picks threshold: ≥ 75

### Candidate profile filter
- Target experience: 2–3 years (mid-level individual contributor)
- Skips: fresher, trainee, intern, graduate, campus hire, 0–1 yr roles
- Skips: Lead, Principal, Director, VP, Head of (5+ yr roles)

### Notes
- Runs automatically every other night at 12:00 AM IST via cron
- `applied` status is tracked in the browser via localStorage (no backend needed)
- Jobs are deduplicated by sha256(title + company) across all runs
- Claude CLI invoked via subprocess with `--allowedTools WebSearch`
- Search prompt lives in `prompt.txt` — edit it to tune searches without touching the script
- Requires `CLAUDE_BIN` and `WHATSAPP_NUM` in `.env`
