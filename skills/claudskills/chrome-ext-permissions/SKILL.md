---
name: chrome-ext-permissions
description: >
  This skill should be used when working on Chrome extension permissions or Chrome Web Store
  compliance. Trigger when: declaring extension permissions, "manifest permissions", "activeTab
  vs tabs", "optional_permissions", "host_permissions", "Chrome Web Store rejection",
  "permission minimization", "over-permissioning", "CWS review", "Purple Potassium",
  "extension permission audit", "narrowest permission", "permission warnings",
  "chrome.permissions.request", "permission justification".
---

# Chrome Extension Permissions

The principle of least privilege governs all permission decisions. Request only what the extension actively uses today — never future-proof permissions. Approximately 70% of submitted extensions over-request permissions. Over-permissioning triggers CWS rejections, alarming install warnings, and longer review cycles.

## Permission Decision Rules

### activeTab vs. tabs vs. host_permissions

| Need | Use | Why |
|------|-----|-----|
| Temporary access after user click | `activeTab` | No install warning, minimal scope |
| Read URL/title of tabs without host access | `tabs` | Required for `tab.url`, `tab.title`, `tab.favIconUrl` |
| Persistent access to specific sites | `host_permissions: ["https://example.com/*"]` | Narrow host pattern |
| Access to all sites | `host_permissions: ["<all_urls>"]` | **Last resort** — triggers 3x rejection rate |

`activeTab` grants temporary access to the currently focused tab only after the user explicitly invokes the extension. It requires no install warning. Always prefer it over broad alternatives.

### Common Permission Misconceptions

| Misconception | Reality |
|---------------|---------|
| "Need `tabs` to use `chrome.tabs` API" | Most `chrome.tabs` methods work without the permission |
| "Need `storage` for localStorage" | `storage` is only for `chrome.storage` API, not web storage |
| "Need `cookies` for `document.cookie`" | `cookies` permission is only for `chrome.cookies` API |
| "Need `<all_urls>` to work on any site" | `activeTab` + user action covers most use cases |

## Optional Permissions

Move non-core features to optional permissions. Request at runtime when the feature is activated:

```typescript
// Request permission when user enables a feature
async function enableAdvancedFeature() {
  const granted = await chrome.permissions.request({
    permissions: ['bookmarks'],
    origins: ['https://api.example.com/*'],
  });

  if (granted) {
    // Permission granted — enable feature
  } else {
    // Permission denied — show explanation
  }
}
```

Benefits:
- Reduces alarming install warnings
- Gives users informed control
- Accelerates CWS review
- Permissions can be revoked when feature is disabled

## Host Permission Patterns

Declare in `host_permissions` array (MV3), not in `permissions`:

```json
{
  "host_permissions": [
    "https://api.example.com/*",
    "https://cdn.example.com/*"
  ]
}
```

**Rules:**
- Use exact domains, not wildcards
- Prefer `https://` over `*://`
- Never use `<all_urls>` unless absolutely required
- Move non-essential hosts to `optional_host_permissions`

## Pre-Release Permission Audit

Before every CWS submission:
1. Grep codebase for every `chrome.*` API call — verify each has a matching permission
2. Remove any declared permission not backed by a code path
3. Replace broad permissions with narrower alternatives where possible
4. Test packed `.crx` build to verify exact install warning dialogs
5. Prepare a short video demonstrating how each sensitive permission is used
6. Write clear cause-and-effect justifications for the CWS privacy tab

## CWS Rejection Codes for Permissions

| Code | Name | Trigger |
|------|------|---------|
| Purple Potassium | Excessive Permissions | Unused or overly broad permissions |
| Purple Lithium | User Data Privacy | Missing privacy policy, insecure data handling |
| Purple Copper | Data Transmission | Sensitive data via HTTP or in URL params |

**Warning:** Adding permissions that trigger install warnings will temporarily disable the extension for existing users until they accept the new terms.

## Additional Resources

### Reference Files

- **`references/permission-guide.md`** — Detailed permission-by-permission reference and narrowing strategies
- **`references/cws-rejection-codes.md`** — Complete CWS rejection code taxonomy with prevention strategies
