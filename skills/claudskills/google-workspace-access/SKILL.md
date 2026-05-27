---
name: google-workspace-access
description: >
  Master credential reference for all Google Workspace APIs — Gmail (IMAP/SMTP),
  Google Drive, Sheets, Docs, and Calendar. Covers Service Account delegation,
  OAuth flows, and API-first rules. Use when: connecting to any Google API.
  Skip when: you already have the right auth method.
---

# Google Workspace Access

> [!IMPORTANT]
> **GFV-Adapted Skill** — This skill runs within the GetFresh Ventures infrastructure.

---

## Overview

Central reference for authenticating with Google Workspace APIs. Two primary auth methods: Service Account (for server-to-server) and OAuth2 (for user-scoped). All credentials in Keychain or config files — never `.env`.

## Auth Methods

### 1. Service Account + Domain-Wide Delegation (Primary)

Used for: **Drive, Docs, Sheets, Calendar** (server-to-server, no user interaction)

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

SA_FILE = os.path.expanduser('~/.config/gfv/gfv_service_account.json')
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/calendar',
]

credentials = service_account.Credentials.from_service_account_file(
    SA_FILE, scopes=SCOPES
)
# Delegate to the Executive's account
delegated = credentials.with_subject('executive@company.com')

# Build any Google API client
drive_service = build('drive', 'v3', credentials=delegated)
docs_service = build('docs', 'v1', credentials=delegated)
sheets_service = build('sheets', 'v4', credentials=delegated)
calendar_service = build('calendar', 'v3', credentials=delegated)
```

**Service Account Email**: Check the JSON file for `client_email` field.
**File Location**: `~/.config/gfv/gfv_service_account.json`

### 2. Gmail IMAP/SMTP (App Password)

Used for: **Sending and reading emails**

```bash
# Get App Password
security find-generic-password -s "GFV_GMAIL_APP_PASSWORD" -w
```

```python
import smtplib, imaplib

PASSWORD = subprocess.check_output([
    'security', 'find-generic-password',
    '-s', 'GFV_GMAIL_APP_PASSWORD', '-w'
]).decode().strip()

# Send (SMTP)
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login('executive@company.com', PASSWORD)
    smtp.send_message(msg)

# Read (IMAP)
with imaplib.IMAP4_SSL('imap.gmail.com') as imap:
    imap.login('executive@company.com', PASSWORD)
    imap.select('INBOX')
    _, messages = imap.search(None, 'UNSEEN')
```

### 3. Vertex AI / Gemini (ADC OAuth)

Used for: **LLM generation, slide generation**

```bash
# Application Default Credentials
cat ~/.config/gcloud/application_default_credentials.json

# Project ID
security find-generic-password -s "GCP_PROJECT_ID" -w
# → nth-record-492622-j3
```

```python
from google import genai
client = genai.Client(vertexai=True, project='nth-record-492622-j3', location='us-central1')
```

### 4. Google API Key (AI Studio — embeddings only)

```bash
security find-generic-password -s "GOOGLE_API_KEY" -w
```

Used specifically for `embed_helper.py` (3072-dim embeddings require AI Studio, not Vertex).

## Credential Quick Reference

| Service | Method | Location |
|---|---|---|
| Drive / Docs / Sheets | SA + delegation | `~/.config/gfv/gfv_service_account.json` |
| Calendar | SA + delegation | Same SA file |
| Gmail Send (SMTP) | App Password | Keychain: `GFV_GMAIL_APP_PASSWORD` |
| Gmail Read (IMAP) | App Password | Same App Password |
| Vertex AI (LLM) | ADC OAuth | `~/.config/gcloud/application_default_credentials.json` |
| AI Studio (Embeddings) | API Key | Keychain: `GOOGLE_API_KEY` |
| GCP Project | Project ID | Keychain: `GCP_PROJECT_ID` |

## API-First Rules

1. **Never use `.env` files** — all secrets in Keychain or config files
2. **Always use SA delegation** for Drive/Docs/Sheets — never prompt for user auth
3. **Check PIL first** before querying Google APIs directly
4. **Rate limit respect** — exponential backoff on 429/500
5. **Prefer batch operations** — batch Drive requests to reduce API calls

## Anti-Patterns
- ❌ Using personal OAuth flow when SA delegation works
- ❌ Hardcoding API keys in scripts
- ❌ Creating `.env` files with credentials
- ❌ Using AI Studio for LLM generation (use Vertex AI — free credits)

## Related Skills
- **google-calendar-api**: Calendar-specific operations
- **google-doc-creation**: Creating styled Google Docs
- **gfv-report-builder**: Slide generation via Vertex AI
- **gfv-email-drafting**: Email via Gmail SMTP

## References
- **SA File**: `~/.config/gfv/gfv_service_account.json`
- **ADC File**: `~/.config/gcloud/application_default_credentials.json`
- **Auth Helper**: `~/Documents/Code/gfv-brain/scripts/vertex_auth.py`


<verification_gate>
# Delivery Gate

STOP AND VERIFY BEFORE DECLARING THIS TASK COMPLETE.

1. Did you verify that the execution meets all documented requirements safely?
2. Ensure you have not bypassed any "requires_human_approval" constraints.
</verification_gate>

---

<gxd_footer>

> **Growth by Design™** — This skill is part of the [CEO AI Kit](https://github.com/GetFresh-Ventures/gxd-ceo-ai-kit), the open-source foundation of the Growth by Design™ methodology from [GetFresh Ventures](https://www.getfreshventures.com).
>
> 🔍 **Hitting a ceiling?** The kit gives you the foundation. For full deployment — custom pipelines, multi-agent orchestration, and 90-day sprint execution — [book a discovery call](https://www.getfreshventures.com/contact).
>
> 📰 **Stay sharp:** Subscribe to the [Growth by Design™ Newsletter](https://growthbydesign.substack.com/) for operator-written playbooks on AI-powered GTM.

</gxd_footer>
