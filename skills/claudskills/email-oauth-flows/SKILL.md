---
name: email-oauth-flows
description: Production-ready Gmail and Outlook OAuth integration for Next.js with Supabase. Handles email scopes, token refresh, permission management, and secure API access for sending/reading emails.
effort: medium
license: MIT
---

# Email OAuth Flows

Complete Gmail and Outlook OAuth integration for Next.js applications using Supabase Auth with automatic token refresh and email API access.

## When to Use

Use this skill when building Next.js applications that need:
- Gmail OAuth with email scopes (send, read, modify)
- Outlook/Microsoft OAuth with Microsoft Graph API
- Automatic OAuth token refresh
- Secure storage of email credentials
- Send emails via user's Gmail/Outlook account
- Read emails from user's inbox
- Email drafts and compose functionality

**Don't use this skill if:**
- You only need basic auth (email/password)
- You're using a different email service (SendGrid, AWS SES)
- You don't need user's email account access

## Stack

- Next.js 14+ (App Router)
- Supabase Auth (@supabase/ssr)
- Gmail API (Google OAuth)
- Microsoft Graph API (Azure OAuth)
- TypeScript (strict mode)

## Quick Start

### 1. Install Dependencies

```bash
npm install @supabase/ssr @supabase/supabase-js
npm install -D @project-forge/email-oauth-flows
```

### 2. Configure OAuth Providers in Supabase

**Gmail (Google):**
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create OAuth 2.0 credentials
3. Add scopes: `gmail.send`, `gmail.modify`, `gmail.readonly`
4. Add redirect URI: `https://your-project.supabase.co/auth/v1/callback`
5. Copy Client ID & Secret to Supabase Dashboard

**Outlook (Azure):**
1. Go to [Azure Portal](https://portal.azure.com)
2. Register app in Azure Entra ID
3. Add API permissions: `Mail.Read`, `Mail.ReadWrite`, `Mail.Send`
4. Add redirect URI: `https://your-project.supabase.co/auth/v1/callback`
5. Copy Client ID & Secret to Supabase Dashboard

### 3. Setup Environment Variables

```bash
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 4. Implement Gmail OAuth

```typescript
'use client'

import { signInWithGmail } from '@project-forge/email-oauth-flows/gmail'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

export function GmailConnectButton() {
  const handleConnect = async () => {
    await signInWithGmail(supabase, {
      redirectTo: `${process.env.NEXT_PUBLIC_APP_URL}/auth/callback`,
      scopes: ['gmail.send', 'gmail.modify', 'gmail.readonly'],
    })
  }

  return <button onClick={handleConnect}>Connect Gmail</button>
}
```

### 5. Handle OAuth Callback

```typescript
// app/auth/callback/route.ts
import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get('code')

  if (code) {
    const supabase = createRouteHandlerClient({ cookies })
    await supabase.auth.exchangeCodeForSession(code)
  }

  return NextResponse.redirect(new URL('/dashboard', request.url))
}
```

### 6. Send Email via Gmail API

```typescript
import { sendGmailEmail } from '@project-forge/email-oauth-flows/gmail'

const { data, error } = await sendGmailEmail({
  accessToken: session.provider_token,
  to: 'recipient@example.com',
  subject: 'Hello from Gmail',
  body: 'This email was sent via Gmail API',
})
```

## Key Features

### Gmail OAuth Integration

Request Gmail-specific scopes:

```typescript
await signInWithGmail(supabase, {
  redirectTo: callbackUrl,
  scopes: [
    'gmail.send',        // Send emails
    'gmail.modify',      // Read and modify emails
    'gmail.readonly',    // Read-only access
    'gmail.compose',     // Create drafts
  ],
})
```

### Outlook OAuth Integration

Request Microsoft Graph scopes:

```typescript
await signInWithOutlook(supabase, {
  redirectTo: callbackUrl,
  scopes: [
    'Mail.Send',        // Send emails
    'Mail.ReadWrite',   // Read and write
    'Mail.Read',        // Read-only
  ],
})
```

### Automatic Token Refresh

Tokens are automatically refreshed by Supabase:

```typescript
import { getEmailAccessToken } from '@project-forge/email-oauth-flows'

// Always get fresh token (auto-refreshes if expired)
const { accessToken, error } = await getEmailAccessToken(supabase, 'google')

if (!error) {
  // Use token with Gmail/Outlook API
}
```

### Provider Token Storage

Store provider tokens securely in database:

```typescript
// On successful OAuth callback
const session = await supabase.auth.getSession()

if (session.data.session?.provider_token) {
  // Store in database for later use
  await db.emailConnections.create({
    userId: session.data.session.user.id,
    provider: 'google',
    accessToken: session.data.session.provider_token,
    refreshToken: session.data.session.provider_refresh_token,
  })
}
```

### Send Emails

**Gmail:**
```typescript
import { sendGmailEmail } from '@project-forge/email-oauth-flows/gmail'

await sendGmailEmail({
  accessToken,
  to: 'user@example.com',
  subject: 'Hello',
  body: 'Email content',
  html: '<h1>HTML Email</h1>',
})
```

**Outlook:**
```typescript
import { sendOutlookEmail } from '@project-forge/email-oauth-flows/outlook'

await sendOutlookEmail({
  accessToken,
  to: 'user@example.com',
  subject: 'Hello',
  body: 'Email content',
  html: '<h1>HTML Email</h1>',
})
```

### Read Emails

**Gmail:**
```typescript
import { listGmailMessages } from '@project-forge/email-oauth-flows/gmail'

const { messages, error } = await listGmailMessages({
  accessToken,
  maxResults: 10,
  query: 'is:unread',
})
```

**Outlook:**
```typescript
import { listOutlookMessages } from '@project-forge/email-oauth-flows/outlook'

const { messages, error } = await listOutlookMessages({
  accessToken,
  top: 10,
  filter: "isRead eq false",
})
```

## Core API

### Gmail Functions

#### `signInWithGmail(supabase, options)`

Initiate Gmail OAuth flow.

**Parameters:**
- `supabase` - Supabase client
- `options`:
  - `redirectTo` - Callback URL after OAuth
  - `scopes` - Array of Gmail scopes

**Returns:** `Promise<{ data, error }>`

#### `sendGmailEmail(options)`

Send email via Gmail API.

**Parameters:**
- `accessToken` - OAuth access token
- `to` - Recipient email
- `subject` - Email subject
- `body` - Plain text body
- `html?` - HTML body (optional)
- `from?` - Sender (defaults to authenticated user)

**Returns:** `Promise<{ data, error }>`

#### `listGmailMessages(options)`

List Gmail messages.

**Parameters:**
- `accessToken` - OAuth access token
- `maxResults?` - Max messages (default: 10)
- `query?` - Gmail search query

**Returns:** `Promise<{ messages, error }>`

### Outlook Functions

#### `signInWithOutlook(supabase, options)`

Initiate Outlook OAuth flow.

#### `sendOutlookEmail(options)`

Send email via Microsoft Graph API.

#### `listOutlookMessages(options)`

List Outlook messages.

### Token Management

#### `getEmailAccessToken(supabase, provider)`

Get fresh access token (auto-refreshes).

**Parameters:**
- `supabase` - Supabase client
- `provider` - 'google' | 'azure'

**Returns:** `Promise<{ accessToken, error }>`

## Database Schema

Recommended schema for storing email connections:

```sql
CREATE TABLE email_connections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),
    provider TEXT NOT NULL, -- 'google' or 'azure'
    email TEXT NOT NULL,
    access_token TEXT, -- Encrypted
    refresh_token TEXT, -- Encrypted
    scopes TEXT[], -- Granted scopes
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT unique_user_provider_email UNIQUE (user_id, provider, email)
);

-- RLS Policies
ALTER TABLE email_connections ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own connections"
ON email_connections FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own connections"
ON email_connections FOR INSERT
WITH CHECK (auth.uid() = user_id);
```

## Security Best Practices

### 1. Never Expose Access Tokens

```typescript
// ❌ Bad - Sending token to client
return NextResponse.json({ accessToken: token })

// ✅ Good - Keep token server-side
const { data } = await sendEmail({ accessToken: token, ... })
return NextResponse.json({ success: true })
```

### 2. Use Server-Side Token Refresh

```typescript
// Always use server-side Supabase client
import { createServerClient } from '@supabase/ssr'

const supabase = createServerClient(...)
const { accessToken } = await getEmailAccessToken(supabase, 'google')
```

### 3. Request Minimal Scopes

```typescript
// ❌ Bad - Requesting all scopes
scopes: ['gmail.full_access']

// ✅ Good - Only what you need
scopes: ['gmail.send', 'gmail.readonly']
```

### 4. Encrypt Stored Tokens

Use Supabase Vault or encrypt tokens before storing in database.

### 5. Handle Revoked Permissions

```typescript
try {
  await sendEmail(...)
} catch (error) {
  if (error.status === 401) {
    // Token revoked - ask user to reconnect
    await promptReconnect()
  }
}
```

## Important Notes

### Google OAuth Verification

**CRITICAL:** Google requires app verification for sensitive scopes like `gmail.send`.

**Steps:**
1. During development, add test users in Google Cloud Console
2. For production, submit app for verification (can take 4-6 weeks)
3. Without verification, only test users can authorize

### Microsoft Graph Requirements

Users must have:
- Microsoft 365 license
- Exchange Online mailbox
- Proper admin consent for app permissions

## Testing

### Local Development

Use ngrok for OAuth callbacks:

```bash
ngrok http 3000
# Update redirect URIs with ngrok URL
```

### Test Scopes

Verify granted scopes:

```typescript
const session = await supabase.auth.getSession()
const grantedScopes = session.data.session?.provider_token
// Check if required scopes are present
```

## Examples

The skill includes 5 production examples:

1. **Gmail Connect Button** (`examples/01-gmail-connect.tsx`)
   - OAuth flow with Gmail
   - Scope selection
   - Error handling

2. **Send Email via Gmail** (`examples/02-send-gmail.ts`)
   - Compose and send
   - HTML emails
   - Attachments

3. **Outlook Integration** (`examples/03-outlook-connect.tsx`)
   - Microsoft OAuth
   - Graph API setup

4. **Token Refresh** (`examples/04-token-refresh.ts`)
   - Automatic refresh
   - Error recovery

5. **Email Dashboard** (`examples/05-email-dashboard.tsx`)
   - List messages
   - Multi-provider support
   - Pagination

## Troubleshooting

**OAuth redirect not working?**
- Verify redirect URI matches exactly in provider console
- Check NEXT_PUBLIC_APP_URL is correct
- Ensure callback route exists

**Access token expired?**
- Use `getEmailAccessToken()` instead of stored token
- Check refresh_token is being saved
- Verify `access_type: 'offline'` is set

**Gmail API returns 403?**
- Check app verification status
- Verify scopes are granted
- Add user to test users list

**Outlook API returns 401?**
- Verify Microsoft 365 license
- Check admin consent for scopes
- Verify mailbox exists

## References

For implementation details, see:
- `references/GMAIL_OAUTH.md` - Gmail OAuth setup guide
- `references/OUTLOOK_OAUTH.md` - Microsoft Graph setup guide
- `references/TOKEN_MANAGEMENT.md` - Token refresh patterns

## License

MIT - See LICENSE file for details

---

**Documentation Version:** 1.0.0
**Last Updated:** 2026-01-17
**Skill Compatibility:** Claude Code 2.1+, Claude Desktop, Claude.ai Pro/Max
