---
name: ai-prose-humanizer
version: "2.0.0"
description: "Evidence-based editorial pipeline that detects and removes AI writing patterns using a research-grounded rubric, preserves author facts, and gates on high-severity issues."
allowed-tools:
  - Read
  - Write
  - Bash
---

# scholar-editor

**Purpose:** Replace the informal Humanizer two-pass flow with a deterministic three-pass editorial
pipeline (Draft -> Expert Audit -> Final). Grounded in MIT Technology Review (2022) and ArXiv 1906.04043
lexical/statistical cues. Hard fact-lock: any `preserve_facts` token altered or removed sets `blocked=true`.

---

## Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `text` | string | yes | Source text to edit |
| `intent` | string | yes | What the text should accomplish |
| `context` | string | yes | Document type and audience |
| `tone` | string | yes | One of: direct, formal, concise, warm-professional |
| `length` | string | no | Target length: short / medium / long (default: preserve) |
| `preserve_facts` | string[] | yes | Entities, dates, metrics that must appear verbatim in output |
| `domain` | string | yes | One of: technical, academic, marketing, casual, general |
| `seed` | string | no | Determinism seed (default: SCHOLAR_SEED_001) |

```json
{
  "text": "I hope this helps! The API deprecation - a crucial milestone - showcases our vibrant platform evolution.",
  "intent": "Notify the payments team about the API deprecation deadline.",
  "context": "Internal engineering email to the payments team",
  "tone": "direct",
  "length": "short",
  "preserve_facts": ["v1 API", "March 31", "payments team"],
  "domain": "technical",
  "seed": "SCHOLAR_SEED_001"
}
```

---

## Output Schema

| Field | Type | Description |
|---|---|---|
| `subject` | string | Suggested document/email subject |
| `draft` | string | Pass 1 output (minimal rewrite, preserve_facts locked) |
| `audit` | Issue[] | Pass 2 pattern issues from detect_patterns + extract_facts |
| `final` | string | Pass 3 output applying med/low fixes only; null if blocked |
| `applied_rules` | int[] | Pattern IDs whose suggested_fix was applied in Pass 3 |
| `blocked` | bool | true if any audit issue is high severity OR any preserve_facts token missing |
| `changelog` | string[] | One line per edit applied in Pass 3 |

```json
{
  "subject": "v1 API deprecation - action required by March 31",
  "draft": "The v1 API shuts down March 31. The payments team must migrate before then.",
  "audit": [
    {
      "rule_id": 19, "label": "Collaborative Communication Artifacts",
      "span_start": 0, "span_end": 20, "text": "I hope this helps!",
      "severity": "high", "confidence": 0.95,
      "rationale": "Unambiguous chatbot opener.",
      "suggested_fix": "Delete opener; begin with the substantive statement."
    }
  ],
  "final": null,
  "applied_rules": [],
  "blocked": true,
  "changelog": []
}
```

---

## Canonical Prompt Flow

### PASS 1 - Draft

> **Settings:** temperature=0.0, seed={seed}

#### System

```
You are a conservative editorial assistant. Your only job in this pass is to produce
a clean working draft that removes the most obvious AI-writing artifacts while
preserving all facts exactly.

Rules:
- Do NOT alter, omit, or paraphrase any item in PRESERVE_FACTS.
- Make minimal changes: fix only clear AI tells (chatbot openers, sycophancy, obvious
  filler). Do not restructure sentences unless necessary to remove an artifact.
- Do NOT invent examples, statistics, or claims not present in the source text.
- Match TONE exactly.
- Return ONLY the draft text. No preamble, no explanation.
```

#### User

```
INTENT: {intent}
CONTEXT: {context}
TONE: {tone}
DOMAIN: {domain}
PRESERVE_FACTS (do not alter these): {preserve_facts}

SOURCE TEXT:
---
{text}
---

Produce a working draft. Remove chatbot openers (P19), sycophancy (P21), and any
I-hope/here-is communication artifacts. Preserve all facts. Return only the draft text.
```

---

### PASS 2 - Expert Audit

> **Settings:** temperature=0.0, seed={seed}
> Calls `detect_patterns(draft, domain)` and `extract_facts(draft)`.

#### System

```
You are a senior editorial auditor applying the Scholar Editor rubric (24 pattern rules).
Your analysis is grounded in:
- MIT Technology Review (2022): statistical token-probability patterns in AI text
- ArXiv 1906.04043 (Gehrmann et al.): GLTR lexical proxies for low-surprisal generation
- Hunting the Muse: practitioner heuristics for AI writing detection
- East Central faculty resources: classroom detection signals

Conservative policy: confidence < 0.7 -> do not emit an Issue.
Return ONLY valid JSON. No prose outside the JSON object.
```

#### User

```
DOMAIN: {domain}
PRESERVE_FACTS: {preserve_facts_json_array}

DRAFT TEXT TO AUDIT:
---
{draft}
---

TASK:
1. FACT-LOCK PRE-PASS: extract all named entities, dates, numeric claims -> facts_locked
2. DOMAIN CLASSIFICATION: confirm or override DOMAIN hint
3. PATTERN DETECTION: apply all 24 rubric rules; emit Issue for each match
   with confidence >= 0.7; escalate severity per rubric when_high conditions
4. GATING: blocked=true if any severity=="high" OR any preserve_facts token is absent
5. Return exactly:
{
  "issues": [ { "rule_id", "label", "span_start", "span_end", "text",
                "severity", "confidence", "rationale", "suggested_fix" } ],
  "facts_locked": { "entities": [], "dates": [], "numerics": [] },
  "domain_detected": "...",
  "blocked": true|false
}
```

---

### PASS 3 - Final

> **Settings:** temperature=0.0, seed={seed}
> Only runs if `blocked == false`.

#### System

```
You are a conservative copy editor. Apply only the suggested fixes for issues with
severity "med" or "low". Do NOT fix or alter any high-severity issue (those require
human review). Do NOT alter any preserve_facts tokens.
Return ONLY: the final text, the list of applied rule IDs, and a changelog (one line per edit).
```

#### User

```
DRAFT:
---
{draft}
---

ISSUES TO FIX (severity med or low only):
{med_low_issues_json}

PRESERVE_FACTS: {preserve_facts}

Apply each suggested_fix. Then return:
{
  "final": "<edited text>",
  "applied_rules": [<ids>],
  "changelog": ["<one line per edit>"]
}
Return only this JSON object.
```

---

## Gating Rules

```yaml
block_on_high_severity: true
# If audit.issues contains any item with severity == "high", set blocked=true.
# Pass 3 does not run. Return audit only.

fact_lock: true
# If any string in preserve_facts is absent from draft or final, set blocked=true.
# This check runs at end of Pass 2 and again at end of Pass 3.
```

---

## Examples

### Short - API notification (technical domain)

**Input:**
```json
{
  "text": "I hope this helps! Here is an overview. The API deprecation - a crucial milestone - showcases our vibrant platform evolution. The future looks bright as we continue this journey toward excellence.",
  "intent": "Notify payments team of v1 API deprecation deadline",
  "context": "Internal engineering email",
  "tone": "direct",
  "preserve_facts": ["v1 API", "March 31", "payments team"],
  "domain": "technical",
  "seed": "SCHOLAR_SEED_001"
}
```

**Expected audit issues (partial):** P19 (high: chatbot opener), P13 (high: em dash), P7 (high: AI vocab), P24 (high: generic conclusion)

**Expected output:**
```json
{
  "subject": "v1 API deprecation - action required by March 31",
  "draft": "The v1 API shuts down March 31. The payments team must migrate before then. See /api/migration for the guide.",
  "audit": [
    {"rule_id": 19, "severity": "high", "text": "I hope this helps!"},
    {"rule_id": 13, "severity": "high", "text": "-"},
    {"rule_id": 7,  "severity": "high", "text": "crucial"},
    {"rule_id": 24, "severity": "high", "text": "The future looks bright"}
  ],
  "final": null,
  "applied_rules": [],
  "blocked": true,
  "changelog": []
}
```

---

### Medium - Stakeholder update (marketing domain)

**Input:**
```json
{
  "text": "Great question! Our Q1 results are in. Additionally, the vibrant interplay between our sales and marketing teams has fostered groundbreaking outcomes. Industry observers have noted our pivotal role. The future is bright.",
  "intent": "Quarterly stakeholder update on Q1 performance",
  "context": "Executive stakeholder email",
  "tone": "warm-professional",
  "preserve_facts": ["Q1", "$4.2M revenue", "23% YoY growth"],
  "domain": "marketing",
  "seed": "SCHOLAR_SEED_001"
}
```

**Expected blocked:** true (P21 sycophancy, P7 AI vocab density, P24 generic conclusion are all high)

**Expected final (if pass 3 ran on med/low only):** Removes filler phrases (P22), rule-of-three (P10), weasel attribution (P5). Preserves Q1, $4.2M revenue, 23% YoY growth verbatim.

---

### Long - Incident summary (technical domain)

**Input:**
```json
{
  "text": "I hope this email finds you well. Here is a comprehensive overview of the March 14 outage. The incident stands as a testament to the enduring challenges of distributed systems. Additionally, our team demonstrated remarkable resilience, highlighting the crucial interplay between monitoring and response. In essence, the future looks bright as we continue this journey toward excellence.",
  "intent": "Post-incident summary for engineering leadership",
  "context": "Post-mortem report",
  "tone": "direct",
  "preserve_facts": ["March 14", "9:41 PM PT", "11:23 PM PT", "4,300 requests", "API tier"],
  "domain": "technical",
  "seed": "SCHOLAR_SEED_001"
}
```

**Expected blocked:** true (P19 chatbot opener, P1 significance inflation, P7 AI vocab, P8 copula avoidance, P24 generic conclusion - all high)

**Expected draft (pass 1 output):** Removes chatbot opener. Preserves all five preserve_facts tokens verbatim.

**Expected final (if unblocked):**
```
The March 14 outage ran from 9:41 PM PT to 11:23 PM PT. 4,300 requests timed out in the API tier.
Root cause: misconfigured load balancer after the 11 PM deploy.
Fix: config rollback at 11:23 PM. Post-mortem at [link]. Deploy checklist updated to catch this configuration class going forward.
```

---

## Version History

| Version | Change |
|---|---|
| 2.0.0 | Add research-grounded patterns P25-P38; add Reference Files section; update load instruction |
| 0.1.0 | Initial Scholar Editor release; replaces Humanizer two-pass flow; adds Expert Audit pass |

---

## Runtime Configuration

```yaml
version: "2.0.0"
temperature: 0.0
seed: SCHOLAR_SEED_001
block_on_high_severity: true
fact_lock: true
humanizer_patterns: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
nick_mode_profile: default
```

Load references/patterns-24.md (P1-P24) and references/patterns-research.md
(P25-P38) before running any pass. Both files are required.

---

## Reference Files

| File | When to load |
|---|---|
| `references/patterns-24.md` | Before Pass 1 in either mode (P1-P24) |
| `references/patterns-research.md` | Before Pass 1 in either mode (P25-P38) |
