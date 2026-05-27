---
name: wa-setup
description: Stage 1. Sign up at Wasender, get a Personal Access Token, create a WhatsApp session, scan the QR with the user's phone, and verify the connection works end-to-end. Saves credentials to .env.
---

# wa-setup — Connect WhatsApp via Wasender

Goal: by the end of this skill, the user has a working Wasender session, a phone connected by QR scan, and a `.env` file with all credentials saved. **You do every technical step.** The user just signs up, holds their phone, scans a QR.

**Speak Hebrew to the user.**

## Step 0 — Frame what's about to happen

Tell the user (in Hebrew):

> נחבר עכשיו את הוואטסאפ שלך לשירות שנקרא **Wasender**. זה השירות שמאפשר לבוט לקרוא ולשלוח הודעות בשמך.
>
> חשוב שתדע:
> - **המספר שתחבר צריך להיות מספר נפרד** — מספר ייעודי לבוט (חדש, או SIM ישנה שלא בשימוש). זה לא חובה, אבל זה הכי בטוח. ❗ זה לא הוואטסאפ הרשמי לעסקים — יש סיכון תיאורטי לחסימה אם משתמשים במספר אישי.
> - **עלות**: ניסיון חינם של 3 ימים, אחרי זה $6 לחודש למספר אחד.
>
> מוכן להתחיל?

Wait for confirmation.

## Step 1 — Sign up at Wasender

Tell the user:

> 1. פתח את הדפדפן וגש ל: **https://wasenderapi.com**
> 2. לחץ על **Sign Up** והשלם הרשמה (אימייל + סיסמה).
> 3. אמת את האימייל.
> 4. אחרי שנכנסת — תגיד לי "**מחובר**" ונמשיך.

Wait until the user confirms.

## Step 2 — Get the Personal Access Token (PAT)

Tell the user:

> מצוין. עכשיו ניצור **Personal Access Token** — מפתח שיאפשר לי לנהל בשמך את החיבורים לוואטסאפ.
>
> 1. גש ל: **https://wasenderapi.com/settings/tokens**
> 2. לחץ **Create New Token**, תן לו שם (למשל "claude-code-builder").
> 3. **העתק את המחרוזת** שתופיע — זו ההזדמנות היחידה שלך לראות אותה.
> 4. הדבק את המחרוזת כאן בצ'אט.

When the user pastes the token:

1. **Do not echo it back.**
2. Read the existing `.env` file at the project root if it exists. If not, create it.
3. Add or update the line `WASENDER_PAT=<the token>`.
4. Make sure `.env` is in `.gitignore`. If not, add it.
5. Confirm to the user:

> מעולה. שמרתי את ה-PAT ב-`.env` מקומית (לא מועלה ל-Git, אל דאגה). עכשיו ניצור את החיבור עצמו.

## Step 3 — Create a WhatsApp session via API

Ask the user for the phone number they'll connect:

> איזה מספר טלפון תרצה לחבר? (פורמט בינלאומי עם +, למשל `+972501234567`)

Validate format. Then ask:

> איך נקרא לחיבור הזה? (למשל "הסוכן של רינת")

Then make the API call. Use Bash with curl. **Pull the PAT from `.env`, never hardcode it in your prompt or output.**

```bash
curl -sX POST "https://www.wasenderapi.com/api/whatsapp-sessions" \
  -H "Authorization: Bearer $WASENDER_PAT" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"$SESSION_NAME\",
    \"phone_number\": \"$PHONE_NUMBER\",
    \"account_protection\": true,
    \"log_messages\": true,
    \"webhook_enabled\": false
  }"
```

(Webhook URL is registered later in `wa-deploy` once we have a public URL.)

The response shape:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "api_key": "75075a7bf6417bff59e76fb...",
    "webhook_secret": "fb61be92ddb7935e0cedcec58e470f6c",
    "status": "need_scan",
    "phone_number": "+972501234567"
  }
}
```

Parse the response. Save to `.env`:
```
WASENDER_SESSION_ID=<id>
WASENDER_API_KEY=<api_key>
WASENDER_WEBHOOK_SECRET=<webhook_secret>
WASENDER_PHONE=<phone_number>
```

Also update `.wa-state.json`:
```json
{ "wasender_session_id": <id>, "wasender_phone": "<phone>" }
```

If the API returns `success: false`, surface the error message in Hebrew and stop. Common errors:
- 401: PAT is invalid → ask the user to regenerate.
- 422: phone number format → ask again with valid E.164.
- 402: plan limit reached → tell the user to upgrade.

## Step 4 — Connect the session and fetch the QR

```bash
curl -sX POST "https://www.wasenderapi.com/api/whatsapp-sessions/$WASENDER_SESSION_ID/connect" \
  -H "Authorization: Bearer $WASENDER_PAT"
```

Then poll for the QR:
```bash
curl -sX GET "https://www.wasenderapi.com/api/whatsapp-sessions/$WASENDER_SESSION_ID/qrcode" \
  -H "Authorization: Bearer $WASENDER_PAT"
```

Response: `{"success":true,"data":{"qrCode":"2@DfzdTHe..."}}` — the `qrCode` value is the **raw WhatsApp QR string**, not an image.

**Render it as an image so the user can scan.** Use Python:

```bash
python -c "
import qrcode, sys, os
qr_str = os.environ['QR_STR']
img = qrcode.make(qr_str)
img.save('wa-qr.png')
print('saved wa-qr.png')
"
```

If `qrcode` isn't installed, run `pip install qrcode[pil]` first. Save the image to the project root as `wa-qr.png` and tell the user:

> הקוד מוכן! נשמר אצלך כאן: `wa-qr.png`
>
> עכשיו:
> 1. פתח את הוואטסאפ בטלפון שאתה רוצה לחבר.
> 2. הגדרות → מכשירים מקושרים → קישור מכשיר.
> 3. סרוק את הקובץ `wa-qr.png`.
>
> ⏱️ הקוד תקף ל-45 שניות. אם פג תוקף, אגיד לך ונייצר חדש.

## Step 5 — Wait for connection

Poll status every 3 seconds for up to 90 seconds:
```bash
curl -sX GET "https://www.wasenderapi.com/api/status" \
  -H "Authorization: Bearer $WASENDER_API_KEY"
```

Response: `{"success":true,"data":{"status":"connected"|"connecting"|"need_scan"|"disconnected"}}`

- `connected` → success, move to step 6.
- `need_scan` after 45s → QR expired. Re-fetch QR, regenerate `wa-qr.png`, ask user to scan again.
- `disconnected` → ask user if they want to retry from the start.

When connected, **delete `wa-qr.png`** (no need to leave it lying around) and tell the user:

> 🎉 חובר! המספר {phone} מחובר עכשיו דרך Wasender.

## Step 6 — End-to-end verification

Send a test message **from the bot back to itself** (or to a number the user provides) to confirm outbound works.

Ask:
> רוצה לשלוח הודעת בדיקה? אני אשלח "שלום מהבוט שלך 👋" למספר שתבחר. שלח לי את המספר (פורמט +).

Then:
```bash
curl -sX POST "https://www.wasenderapi.com/api/send-message" \
  -H "Authorization: Bearer $WASENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"to\":\"$TEST_NUMBER\",\"text\":\"שלום מהבוט שלך 👋\"}"
```

Verify response has `success: true` and `data.msgId`. Ask the user:

> קיבלת את ההודעה?

If yes — done. If no — diagnose: check status endpoint, check rate limit headers, check sender format.

## Step 7 — Update state and hand back

Update `.wa-state.json`:
```json
{
  "current_stage": "characterize",
  "completed_stages": ["setup"],
  "last_updated": "<ISO 8601>"
}
```

Tell the user:

> נהדר! החיבור עובד. השלב הבא הוא לעצב את **האישיות** של הבוט — מה השם שלו, מי הוא משרת, איך הוא מדבר, מה מותר ומה אסור.
>
> מוכן להמשיך לשלב **הגדרת אופי הבוט** (`/wa` ישלוף אותך לשם)?

Hand back to `/wa` orchestrator.

## Common pitfalls and how to handle

- **PAT pasted with spaces or quotes.** Strip whitespace and surrounding quotes before saving.
- **User on free tier hits "1 request per minute" limit.** When polling status, respect 3-second intervals — don't burst. If 429 returned, wait longer.
- **User has a previously deleted session with the same phone.** The create call may return an error about duplicate phone. Tell the user we'll re-use the existing session — call `GET /api/whatsapp-sessions` (with PAT) to list, find the matching one, and adopt its `id`/`api_key`/`webhook_secret`.
- **`qrcode` Python lib not installed.** Install via pip silently first; only mention it to the user if install fails.
- **Webhook secret missing from response.** This shouldn't happen on a fresh session, but if it does, regenerate via `PUT /api/whatsapp-sessions/{id}` with `regenerate_webhook_secret: true` (verify against current docs if needed).
