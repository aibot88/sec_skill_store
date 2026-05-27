---
name: questionnaire
description: Auto-fill security questionnaires (SIG Lite, CAIQ, Enterprise) using scan data and policy documents.
user-invocable: true
---

# Questionnaire Auto-Fill

You are helping a founder auto-fill a security questionnaire using Shasta scan data and generated policies. Be concise and practical.

## What to do

Read `shasta.config.json` for `python_cmd`. Use that for all commands (shown as `<PYTHON_CMD>`).

### Step 1: Check for a recent scan

```bash
<PYTHON_CMD> -c "
from shasta.db.schema import ShastaDB
db = ShastaDB(); db.initialize()
scan = db.get_recent_scan(max_age_minutes=120)
if scan:
    print(f'RECENT_SCAN_FOUND|{scan.id}|{scan.completed_at}|{scan.summary.total_findings if scan.summary else 0} findings')
else:
    print('NO_RECENT_SCAN')
"
```

If no recent scan exists, tell the user: "No recent scan found. Run /scan first, then come back to auto-fill your questionnaire."

### Step 2: Ask which questionnaire

Ask the user which questionnaire to fill:
1. **SIG Lite** — Shared Assessments SIG Lite (80 questions, common for financial services)
2. **CAIQ** — Cloud Security Alliance CAIQ v4 (80 questions, common for cloud/SaaS)
3. **Generic Enterprise** — Common enterprise buyer questions (40 questions, covers the basics)

### Step 3: Run the engine

Based on the user's choice, set the `bank` variable to `sig_lite`, `caiq`, or `enterprise`.

```bash
<PYTHON_CMD> -c "
import json
from shasta.db.schema import ShastaDB
from shasta.questionnaire.engine import QuestionnaireEngine
from shasta.questionnaire.questions import QUESTIONNAIRE_BANKS
from shasta.questionnaire.generator import generate_csv, generate_markdown

db = ShastaDB(); db.initialize()
scan = db.get_recent_scan(max_age_minutes=120)
if not scan:
    scan = db.get_latest_scan()
if not scan:
    print('ERROR: No scan data found. Run /scan first.')
    exit(1)

bank_name = '<BANK>'  # sig_lite, caiq, or enterprise
questions = QUESTIONNAIRE_BANKS[bank_name]
names = {'sig_lite': 'SIG Lite', 'caiq': 'CAIQ v4', 'enterprise': 'Generic Enterprise'}

engine = QuestionnaireEngine(scan)
result = engine.fill(questions, questionnaire_type=names[bank_name])

scan_date = str(scan.completed_at) if scan.completed_at else 'unknown'
csv_path = generate_csv(result, questions)
md_path = generate_markdown(result, questions, scan_date=scan_date)

print(json.dumps({
    'questionnaire': result.questionnaire_type,
    'total': result.total_questions,
    'auto_answered': result.auto_answered,
    'manual_required': result.manual_required,
    'coverage_pct': result.coverage_pct,
    'csv_path': str(csv_path),
    'md_path': str(md_path),
    'confidence': {
        'high': sum(1 for a in result.answers if a.confidence == 'high'),
        'medium': sum(1 for a in result.answers if a.confidence == 'medium'),
        'manual': sum(1 for a in result.answers if a.confidence == 'manual'),
    },
    'sample_answers': [
        {'id': a.question_id, 'answer': a.answer, 'confidence': a.confidence}
        for a in result.answers[:5]
    ],
}, indent=2))
"
```

Replace `<BANK>` with the user's selection.

### Step 4: Present the results

Report the results clearly:

- "Answered **X/Y** questions automatically (**Z%** coverage). **N** require manual review."
- Show confidence breakdown: "W high confidence, X medium, Y manual review"
- Show a few sample answers from different categories
- Mention both output files: "CSV at `{csv_path}`, Markdown report at `{md_path}`"
- If coverage is below 50%, suggest: "Run /scan to collect more data, or /policy-gen to create missing policy documents"
- If coverage is above 70%, celebrate: "Good coverage! Review the manual items and you're ready to submit."

### Tone
- Practical, not flashy. This is about saving the user hours of questionnaire drudgery.
- Frame manual items as a to-do list, not a failure.
- Mention that answers reference specific evidence (resource IDs, policy documents) that auditors can verify.
