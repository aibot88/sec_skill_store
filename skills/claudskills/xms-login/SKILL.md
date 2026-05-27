---
name: xms-login
description: Automates XMS customer service system SSO login via browser automation. Handles navigation to the XMS portal, SSO redirection detection, DOM-based credential injection with event triggering, and login confirmation. Use when the user needs to log into XMS, authenticate with cs-packet.i4px.com, or perform any XMS workflow requiring a valid session.
---

# XMS 登录自动化

## Overview

Automates SSO login for the XMS customer service management system. Unauthenticated users are redirected from `cs-packet.i4px.com` to `sso.i4px.com`. The login form is invisible to the accessibility tree, so credentials must be injected via JavaScript DOM manipulation.

## Login Workflow

### Step 1: Navigate

Open `http://cs.packet.i4px.com/` in the browser.

### Step 2: Window Health Check

Before proceeding, verify the browser window:

1. **Check**: `window.innerWidth + ',' + window.innerHeight`
2. **JS resize**: If broken, `window.moveTo(0,0); window.resizeTo(1440,900)`, wait 2s, recheck
3. **New tab**: `tabs_create_mcp`, check size
4. **Recreate**: Close tabs one by one (`tabs_close_mcp` only accepts single `tabId`), then `tabs_context_mcp` with `createIfEmpty:true`
5. **Small fallback**: 256x116 is functional. DOM operations work. Only abort at `0,0`.

### Step 3: Detect SSO

Check current URL:
- Contains `sso.i4px.com` -> proceed to Step 4
- Already `cs-packet.i4px.com/index` -> already logged in, skip to Step 5

### Step 4: Inject Credentials

```javascript
const username = document.getElementById('username');
const passwordOrg = document.getElementById('passwordOrg');

if (username && passwordOrg) {
  username.value = 'USERNAME';
  passwordOrg.value = 'PASSWORD';

  ['input', 'change', 'keyup'].forEach(evt => {
    username.dispatchEvent(new Event(evt, { bubbles: true }));
    passwordOrg.dispatchEvent(new Event(evt, { bubbles: true }));
  });

  document.getElementById('signbtn').click();
}
```

> Replace USERNAME/PASSWORD with actual credentials. Element IDs are `username`, `passwordOrg`, `signbtn` — not `loginName`, `loginPwd`, or `loginBtn`.

### Step 5: Handle Post-Login Dialogs

After clicking the login button, the system may present additional dialogs before completing the login:

#### 5.1 "Already logged in elsewhere" dialog

If a confirmation dialog appears saying "此账号已在别的地方登录" or similar:

```javascript
const confirmBtn = Array.from(document.querySelectorAll('button, .ant-btn, .next-btn'))
  .find(el => ['是', '确定', '确认', 'OK', 'Yes'].includes(el.textContent.trim()));
if (confirmBtn) confirmBtn.click();
```

**Action**: Click "是" / "确定" to continue login and dismiss the dialog.

#### 5.2 QR code / device verification / slider captcha

If the page shows a QR code scan, mobile device authentication popup, or slider captcha that cannot be completed automatically:

1. **Do NOT retry the login repeatedly**
2. **Notify the user immediately** via IM (e.g., 小Q channel: `978802e0-d724-46b2-841e-70a4ed3c32ae`) with a message like:
   > "XMS login requires manual verification (QR code/device auth). Please complete the verification on your computer and reply to me."
3. **Wait 3 minutes**, then recheck if the page has redirected to `cs-packet.i4px.com/index`
4. If still not redirected, notify again and record error: `last_error = "Login requires manual verification, user notified but not completed within time limit"`

#### 5.3 Login timeout

If the URL does not change within **3 minutes** and no special scenario above occurs:
- Set `last_error = "XMS login timeout"`
- Handle via the outer retry logic

### Step 6: Confirm Login Success

Wait for redirect to `cs-packet.i4px.com/index`. Verify by checking URL and page title.

- If redirected successfully → login complete
- If still on `sso.i4px.com` after handling all dialogs above → record error and retry via outer loop

## Verified Element IDs

| Element | Correct ID | Incorrect (old) |
|---------|------------|-----------------|
| Username input | `username` | `loginName` |
| Password input | `passwordOrg` | `loginPwd` |
| Login button | `signbtn` | `loginBtn` |

## Critical Rules

- **DOM injection only**: The login form is invisible to accessibility trees. `javascript_tool` is the only reliable method.
- **Trigger events**: Setting `.value` alone is insufficient. Always dispatch `input`/`change`/`keyup` events so the frontend framework detects the change.
- **Already logged in**: Always check URL first to avoid unnecessary re-login.
