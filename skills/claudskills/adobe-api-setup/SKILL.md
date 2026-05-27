---
name: adobe-api-setup
description: Guide for configuring Adobe AEP and CJA API access with OAuth Server-to-Server authentication. Use when setting up API credentials or troubleshooting OAuth errors (401/403).
---

# Adobe AEP/CJA API Prerequisites

This skill provides guidance on configuring Adobe Experience Platform (AEP) and Customer Journey Analytics (CJA) API access for projects using OAuth Server-to-Server authentication.

## When to Use This Skill

Invoke this skill when:
- Setting up a new project that integrates with Adobe CJA or AEP APIs
- Troubleshooting OAuth authentication failures
- Configuring API credentials for the first time
- Diagnosing 401/403 permission errors

---

## Prerequisites Checklist

Before using Adobe CJA/AEP APIs, ensure:

- [ ] **Adobe Experience Cloud Access** - User account with access to CJA and/or AEP
- [ ] **Adobe Developer Console Access** - Permission to create API integrations
- [ ] **System Administrator or Developer Role** - Required to create OAuth credentials
- [ ] **Product Profile Access** - User must be assigned to appropriate product profiles in Admin Console

---

## Adobe Developer Console Setup

### Step 1: Create a Project

1. Go to [Adobe Developer Console](https://developer.adobe.com/console/)
2. Sign in with your Adobe ID (must have appropriate permissions)
3. Verify you're in the correct organization (top-right dropdown)
4. Click **"Create new project"**
5. Name the project descriptively (e.g., `CJA Integration`, `AEP Data Pipeline`)

### Step 2: Add the CJA API

1. In your project, click **"Add API"**
2. Filter by **"Adobe Experience Platform"** or search for **"Customer Journey Analytics"**
3. Select **"Customer Journey Analytics"**
4. Click **"Next"**
5. Choose **"OAuth Server-to-Server"** authentication
6. Click **"Next"**
7. Select a product profile that has access to your Data Views
8. Click **"Save configured API"**

### Step 3: Add the AEP API (Required)

> **Critical:** The Adobe Experience Platform API must be added to your project even if you're only using CJA. This associates your service account with an Experience Platform product profile, which is required for CJA API authentication.

1. In your project, click **"Add API"** again
2. Search for **"Experience Platform API"** (under Adobe Experience Platform)
3. Select **"Experience Platform API"**
4. Click **"Next"**
5. Choose **"OAuth Server-to-Server"** authentication
6. Click **"Next"**
7. Select a product profile (associates your service account with Experience Platform)
8. Click **"Save configured API"**

### Step 4: Verify Configuration

Your project should now show **two APIs** configured:
- Customer Journey Analytics
- Experience Platform API

Both APIs share the same OAuth credentials (Client ID and Secret).

---

## Required Credentials

Collect these four values from Adobe Developer Console:

| Credential | Location | Format Example |
|------------|----------|----------------|
| **Organization ID** | Top-right of console, or Project Overview | `ABC123DEF456@AdobeOrg` |
| **Client ID** | OAuth Server-to-Server > Credentials | `cm1234567890abcdef...` |
| **Client Secret** | Click "Retrieve client secret" | `p8e-XXXXXXXXXXXX...` |
| **Scopes** | OAuth Server-to-Server > Scopes | Space-separated scope URIs |

> **Security:** Never commit credentials to version control. Use environment variables, secrets managers, or gitignored configuration files.

---

## Configuration Methods

### Method 1: Configuration File (config.json)

```json
{
  "org_id": "ABC123DEF456@AdobeOrg",
  "client_id": "1234567890abcdef1234567890abcdef",
  "secret": "p8e-XXX...",
  "scopes": "your_scopes_from_developer_console"
}
```

**Best for:** Local development, single organization

**Important:** Add `config.json` to `.gitignore`

### Method 2: Environment Variables

```bash
export ORG_ID="ABC123DEF456@AdobeOrg"
export CLIENT_ID="1234567890abcdef1234567890abcdef"
export SECRET="p8e-XXX..."
export SCOPES="your_scopes_from_developer_console"
```

**Best for:** CI/CD pipelines, Docker containers, cloud deployments

### Method 3: .env File

```bash
# .env file (requires python-dotenv)
ORG_ID=ABC123DEF456@AdobeOrg
CLIENT_ID=1234567890abcdef1234567890abcdef
SECRET=p8e-XXX...
SCOPES=your_scopes_from_developer_console
```

**Best for:** Local development with environment variable pattern

---

## OAuth Scopes

OAuth scopes define what permissions the API client has. Copy the exact scopes string from Adobe Developer Console.

### Common Scope Patterns

| API | Typical Scopes |
|-----|---------------|
| CJA Read | `openid, AdobeID, read_organizations, additional_info.projectedProductContext` |
| CJA + AEP | Above plus AEP-specific scopes from your project |

> **Important:** Copy scopes exactly as shown in Developer Console. Incorrect or missing scopes cause `invalid_scope` or `insufficient_scope` errors.

---

## Product Profile Requirements

### CJA Product Profiles

Users and service accounts need appropriate CJA product profiles:

| Profile Type | Permissions |
|--------------|-------------|
| **Data View Access** | Read access to specific Data Views |
| **Component Access** | Access to metrics, dimensions, segments, calculated metrics |
| **Admin** | Full access including configuration |

### AEP Product Profiles

Even for CJA-only projects, an AEP product profile association is required:

1. Go to [Adobe Admin Console](https://adminconsole.adobe.com/)
2. Navigate to **Products** > **Adobe Experience Platform**
3. Select or create a product profile
4. Ensure your service account (from Developer Console) is assigned

---

## Common OAuth Errors and Solutions

### invalid_client

```
OAuth response: {"error": "invalid_client", "error_description": "..."}
```

**Causes:**
- Client ID is incorrect
- Client Secret is incorrect or expired
- Project credentials were regenerated

**Solutions:**
1. Verify Client ID matches Developer Console exactly
2. Re-retrieve Client Secret from Developer Console
3. Check for copy/paste errors (extra spaces, missing characters)

### invalid_scope

```
OAuth response: {"error": "invalid_scope", "error_description": "..."}
```

**Causes:**
- Scopes string doesn't match Developer Console
- Requested scope not authorized for this client

**Solutions:**
1. Copy scopes exactly from Developer Console (OAuth Server-to-Server > Scopes)
2. Don't modify or add scopes manually

### unauthorized_client

```
OAuth response: {"error": "unauthorized_client", "error_description": "..."}
```

**Causes:**
- OAuth Server-to-Server not enabled
- Incorrect credential configuration

**Solutions:**
1. Ensure OAuth Server-to-Server is selected in Developer Console
2. Verify your project has the correct authentication type configured

### 403 Forbidden

```
ERROR - 403 Forbidden
ERROR - Failed to fetch data: 403
```

**Causes:**
- Service account not assigned to required product profiles
- Missing AEP API in project
- Insufficient permissions for requested resource

**Solutions:**
1. Verify both CJA API and AEP API are added to project
2. Check product profile assignments in Admin Console
3. Wait 5-10 minutes after permission changes for propagation

### 401 Unauthorized

```
ERROR - 401 Unauthorized
ERROR - Authentication failed
```

**Causes:**
- Expired or invalid access token
- Credentials changed in Developer Console

**Solutions:**
1. Verify credentials haven't been regenerated
2. Check Client Secret is current
3. Ensure Organization ID is correct

---

## Security Best Practices

1. **Never commit credentials** - Add `config.json`, `.env`, and credential files to `.gitignore`
2. **Use environment variables in CI/CD** - Inject secrets at runtime
3. **Rotate secrets periodically** - Regenerate Client Secret in Developer Console
4. **Principle of least privilege** - Use product profiles with minimum required permissions
5. **Audit access** - Review API usage in Adobe Developer Console

### .gitignore Entries

```gitignore
# Adobe API credentials
config.json
.env

# Credential directories
.cja/
credentials/
```

---

## Quick Reference

### Minimum Configuration

```json
{
  "org_id": "YOUR_ORG_ID@AdobeOrg",
  "client_id": "YOUR_CLIENT_ID",
  "secret": "YOUR_CLIENT_SECRET",
  "scopes": "your_scopes_from_developer_console"
}
```

### Required APIs in Developer Console

1. **Customer Journey Analytics** - For CJA Data View access
2. **Experience Platform API** - Required for authentication (even for CJA-only projects)

### Key URLs

| Resource | URL |
|----------|-----|
| Adobe Developer Console | https://developer.adobe.com/console/ |
| Adobe Admin Console | https://adminconsole.adobe.com/ |
| CJA API Documentation | https://developer.adobe.com/cja-apis/docs/ |
| AEP API Documentation | https://developer.adobe.com/experience-platform-apis/ |

---

## Troubleshooting Checklist

When authentication fails, verify:

- [ ] Organization ID ends with `@AdobeOrg`
- [ ] Client ID copied exactly (no extra spaces)
- [ ] Client Secret is current (not regenerated since last copy)
- [ ] Scopes copied exactly from Developer Console
- [ ] Both CJA API and AEP API added to project
- [ ] OAuth Server-to-Server authentication selected
- [ ] Service account assigned to product profiles in Admin Console
- [ ] Product profiles have appropriate permissions
- [ ] Waited 5-10 minutes after permission changes
