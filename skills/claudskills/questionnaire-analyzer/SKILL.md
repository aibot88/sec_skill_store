---
name: questionnaire-analyzer
description: Analyzes vendor security questionnaire responses. Identifies red flags, gaps, and areas requiring follow-up. Supports SIG, CAIQ, and custom questionnaires.
allowed-tools: Read, Glob, Grep
---

# Questionnaire Analyzer

Analyzes vendor security questionnaire responses.

## Capabilities

- **Completeness Check**: Identify missing or incomplete responses
- **Red Flag Detection**: Flag concerning answers
- **Gap Analysis**: Compare responses to requirements
- **Follow-up Generation**: Create targeted follow-up questions

## Supported Questionnaires

### SIG (Standardized Information Gathering)

- SIG Core
- SIG Lite
- Custom SIG variations

### CAIQ (Consensus Assessments Initiative Questionnaire)

- CSA CAIQ v4
- Cloud-specific controls

### Industry-Specific

- HECVAT (Higher Education)
- HITRUST CSF
- Custom organizational questionnaires

## Analysis Output

- Response summary by domain
- Risk findings with severity
- Evidence gaps
- Follow-up questions
- Comparison to baseline expectations

## Red Flag Indicators

- "N/A" responses for critical controls
- Vague or evasive answers
- Missing certifications for data type
- No incident response plan
- Unlimited subcontractor use
