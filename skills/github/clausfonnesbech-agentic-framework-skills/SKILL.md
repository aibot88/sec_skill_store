---
name: secure-coding-skill
description: >-
  Use this skill to identify and prevent common security vulnerabilities in code. Trigger when
  writing code, reviewing code for security, or assessing vulnerability risks. This skill covers
  injection attacks, authentication flaws, data exposure, and security best practices.
  Essential for writing secure code. Use continuously throughout development to prevent
  vulnerabilities before they reach production.
---

# Secure Coding Skill

## Overview

This skill provides guidance on secure coding practices across multiple languages and frameworks. Use it to identify security vulnerabilities, implement secure patterns, and follow security best practices.

## When to Use This Skill

- Reviewing code for security issues
- Implementing authentication and authorization
- Handling sensitive data
- Validating user input
- Implementing cryptography
- Configuring security settings

## Core Security Principles

### 1. Defense in Depth
- Multiple layers of security controls
- Never rely on a single security mechanism
- Validate at multiple levels (client, API, database)

### 2. Principle of Least Privilege
- Grant minimum required permissions
- Restrict access by default
- Implement role-based access control

### 3. Fail Securely
- Secure defaults
- Fail to secure state on error
- Never bypass security on exceptions

### 4. Never Trust User Input
- Validate all input
- Sanitize data
- Use parameterized queries
- Encode output

### 5. Security by Design
- Consider security from the start
- Threat modeling
- Security requirements in specs

## Common Vulnerabilities & Prevention

### 1. SQL Injection

**Vulnerable Code:**
```python
# ❌ BAD: String concatenation
query = f"SELECT * FROM users WHERE email = '{user_email}'"
cursor.execute(query)

# ❌ BAD: String formatting
query = "SELECT * FROM users WHERE id = %s" % user_id
```

**Secure Code:**
```python
# ✅ GOOD: Parameterized queries (Django ORM)
users = User.objects.filter(email=user_email)

# ✅ GOOD: Parameterized raw SQL
cursor.execute("SELECT * FROM users WHERE email = %s", [user_email])

# ✅ GOOD: FastAPI with SQLAlchemy
stmt = select(User).where(User.email == user_email)
```

### 2. Cross-Site Scripting (XSS)

**Vulnerable Code:**
```python
# ❌ BAD: Rendering unsanitized user input
return f"<div>Hello {user_name}</div>"

# ❌ BAD: mark_safe without sanitization
return mark_safe(f"<p>{user_content}</p>")
```

**Secure Code:**
```python
# ✅ GOOD: Template engine auto-escapes
return render(request, 'greeting.html', {'name': user_name})

# ✅ GOOD: Explicit escaping
from html import escape
return f"<div>Hello {escape(user_name)}</div>"

# ✅ GOOD: Content Security Policy headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
```

### 3. Authentication Issues

**Vulnerable Code:**
```python
# ❌ BAD: Weak password hashing
import hashlib
hashed = hashlib.md5(password.encode()).hexdigest()

# ❌ BAD: Plain text passwords
user.password = password

# ❌ BAD: Predictable session tokens
session_id = str(time.time())
```

**Secure Code:**
```python
# ✅ GOOD: Strong password hashing (Django)
from django.contrib.auth.hashers import make_password, check_password
hashed = make_password(password)  # Uses PBKDF2 by default

# ✅ GOOD: Bcrypt
import bcrypt
hashed =bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# ✅ GOOD: Secure session management
from django.contrib.sessions.backends.db import SessionStore
session = SessionStore()
session.create()  # Cryptographically secure ID
```

### 4. Authorization Bypass

**Vulnerable Code:**
```python
# ❌ BAD: No authorization check
def delete_user(request, user_id):
    User.objects.filter(id=user_id).delete()
    return JsonResponse({'status': 'deleted'})

# ❌ BAD: Client-side authorization only
# Relying on hidden buttons or disabled UI
```

**Secure Code:**
```python
# ✅ GOOD: Server-side authorization
def delete_user(request, user_id):
    if not request.user.is_admin:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    user = get_object_or_404(User, id=user_id)
    if user.team_id != request.user.team_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    
    user.delete()
    return JsonResponse({'status': 'deleted'})

# ✅ GOOD: Decorator-based authorization
@require_admin
@team_member_only
def delete_user(request, user_id):
    # Authorization enforced by decorators
    pass
```

### 5. Insecure Direct Object References (IDOR)

**Vulnerable Code:**
```python
# ❌ BAD: No ownership check
def get_document(request, doc_id):
    doc = Document.objects.get(id=doc_id)
    return JsonResponse(doc.to_dict())
```

**Secure Code:**
```python
# ✅ GOOD: Verify ownership
def get_document(request, doc_id):
    doc = get_object_or_404(
        Document,
        id=doc_id,
        team_id=request.user.team_id  # Verify team access
    )
    return JsonResponse(doc.to_dict())

# ✅ GOOD: Row Level Security (Supabase)
CREATE POLICY "Users can only access their team's documents"
ON documents FOR SELECT
USING (team_id = auth.uid()::text);
```

### 6. Sensitive Data Exposure

**Vulnerable Code:**
```python
# ❌ BAD: Logging sensitive data
logger.info(f"User logged in: {email}, password: {password}")

# ❌ BAD: Unencrypted personal data
class User(models.Model):
    ssn = models.CharField(max_length=11)  # Plain text!

# ❌ BAD: Exposing sensitive data in API
def user_profile(request):
    user = request.user
    return JsonResponse({
        'email': user.email,
        'password': user.password,  # Never expose!
        'api_key': user.api_key     # Never expose!
    })
```

**Secure Code:**
```python
# ✅ GOOD: Don't log secrets
logger.info(f"User logged in: {email}")

# ✅ GOOD: Encrypt sensitive fields
from django_cryptography.fields import encrypt
class User(models.Model):
    ssn = encrypt(models.CharField(max_length=11))

# ✅ GOOD: Filter sensitive fields
def user_profile(request):
    user = request.user
    return JsonResponse({
        'email': user.email,
        'name': user.name,
        'role': user.role
        # password and api_key excluded
    })
```

### 7. Path Traversal

**Vulnerable Code:**
```python
# ❌ BAD: User-controlled file paths
def download_file(request, filename):
    path = f"/uploads/{filename}"
    return FileResponse(open(path, 'rb'))
```

**Secure Code:**
```python
# ✅ GOOD: Validate and sanitize paths
import os
from pathlib import Path

def download_file(request, filename):
    # Validate filename
    if '..' in filename or '/' in filename:
        return JsonResponse({'error': 'Invalid filename'}, status=400)
    
    # Use absolute paths and verify
    base_dir = Path('/uploads').resolve()
    file_path = (base_dir / filename).resolve()
    
    # Ensure file is within base directory
    if not file_path.is_relative_to(base_dir):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    return FileResponse(open(file_path, 'rb'))
```

### 8. Command Injection

**Vulnerable Code:**
```python
# ❌ BAD: Shell command with user input
import os
os.system(f"ping {user_input}")

# ❌ BAD: Subprocess with shell=True
import subprocess
subprocess.run(f"ls {user_path}", shell=True)
```

**Secure Code:**
```python
# ✅ GOOD: Use subprocess with list arguments
import subprocess
subprocess.run(['ping', '-c', '1', user_input])

# ✅ GOOD: Validate input first
if not re.match(r'^[\w.-]+$', user_input):
    raise ValueError('Invalid input')
subprocess.run(['ping', '-c', '1', user_input])

# ✅ BETTER: Use libraries instead of shell commands
# Instead of shelling out, use Python libraries
```

### 9. Insecure Deserialization

**Vulnerable Code:**
```python
# ❌ BAD: pickle from untrusted source
import pickle
data = pickle.loads(user_input)

# ❌ BAD: eval on user input
result = eval(user_input)
```

**Secure Code:**
```python
# ✅ GOOD: Use JSON for untrusted data
import json
data = json.loads(user_input)

# ✅ GOOD: Validate structure
import jsonschema
schema = {'type': 'object', 'properties': {...}}
jsonschema.validate(data, schema)

# ✅ GOOD: Never use eval with user input
# Use ast.literal_eval for literals only
from ast import literal_eval
result = literal_eval(user_input)  # Only literals, no code execution
```

### 10. Weak Cryptography

**Vulnerable Code:**
```python
# ❌ BAD: Weak algorithms
import hashlib
hash = hashlib.md5(data.encode()).hexdigest()  # MD5 is broken

# ❌ BAD: Custom crypto
def my_encrypt(data, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

# ❌ BAD: Hardcoded encryption key
SECRET_KEY = "my-secret-key-12345"
```

**Secure Code:**
```python
# ✅ GOOD: Strong hashing
import hashlib
hash = hashlib.sha256(data.encode()).hexdigest()

# ✅ GOOD: Use proven crypto libraries
from cryptography.fernet import Fernet
key = Fernet.generate_key()  # Store securely
cipher = Fernet(key)
encrypted = cipher.encrypt(data.encode())

# ✅ GOOD: Key from environment
import os
SECRET_KEY = os.environ['SECRET_KEY']
if len(SECRET_KEY) < 32:
    raise ValueError('SECRET_KEY must be at least 32 characters')
```

## Input Validation Patterns

### Whitelist Validation (Preferred)

```python
# ✅ GOOD: Only allow known-safe values
ALLOWED_STATUSES = ['open', 'in_progress', 'completed', 'closed']
if status not in ALLOWED_STATUSES:
    raise ValueError(f'Invalid status: {status}')

# ✅ GOOD: Pattern matching
import re
if not re.match(r'^[a-zA-Z0-9_-]+$', username):
    raise ValueError('Invalid username format')

# ✅ GOOD: Type validation
from pydantic import BaseModel, EmailStr, validator

class UserInput(BaseModel):
    email: EmailStr
    age: int
    
    @validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Invalid age')
        return v
```

### Sanitization

```python
# ✅ GOOD: Strip dangerous characters
from html import escape
safe_text = escape(user_input)

# ✅ GOOD: Normalize paths
from pathlib import Path
safe_path = Path(user_path).resolve()

# ✅ GOOD: Remove control characters
import re
safe_input = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', user_input)
```

## Secure Configuration

### Django Settings

```python
# ✅ GOOD: Security settings
DEBUG = False  # Never True in production
SECRET_KEY = os.environ['SECRET_KEY']

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

ALLOWED_HOSTS = ['yourdomain.com']  # Never use ['*']

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

### FastAPI Security

```python
# ✅ GOOD: Security dependencies
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Never use ["*"]
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Limit to needed methods
    allow_headers=["*"],
)

# Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Validate token
    user = verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication"
        )
    return user
```

## Security Headers

```python
# ✅ GOOD: Security headers middleware
class SecurityHeadersMiddleware:
    def __init__(self, app):
        self.app = app
    
    def __call__(self, request):
        response = self.app(request)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response
```

## Secrets Management

```python
# ✅ GOOD: Environment variables
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']
API_KEY = os.environ['API_KEY']
SECRET_KEY = os.environ['SECRET_KEY']

# ❌ BAD: Hardcoded secrets
DATABASE_URL = "postgresql://user:password@localhost/db"
API_KEY = "sk-1234567890"
```

## Database Security (Supabase)

```sql
-- ✅ GOOD: Row Level Security
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can only access their team's tasks"
ON tasks FOR ALL
USING (team_id = auth.uid()::text);

-- ✅ GOOD: Specific operation policies
CREATE POLICY "Team admins can delete tasks"
ON tasks FOR DELETE
USING (
  team_id = auth.uid()::text
  AND (SELECT role FROM users WHERE id = auth.uid()) = 'admin'
);
```

## Security Review Checklist

### Authentication & Authorization
- [ ] Strong password hashing (bcrypt, argon2, or PBKDF2)
- [ ] Secure session management
- [ ] JWT tokens properly signed and validated
- [ ] CSRF protection enabled
- [ ] Authorization checked on all endpoints
- [ ] No authentication bypass vulnerabilities

### Input Validation
- [ ] All user inputs validated
- [ ] Whitelist validation where possible
- [ ] Parameterized database queries
- [ ] File uploads validated (type, size, content)
- [ ] Path traversal prevented
- [ ] Command injection prevented

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] TLS/SSL for data in transit
- [ ] Personal data properly protected (GDPR)
- [ ] No sensitive data in logs
- [ ] No sensitive data in URLs or query strings
- [ ] Secure data deletion implemented

### Cryptography
- [ ] Strong algorithms used (AES-256, RSA-2048+)
- [ ] No custom crypto implementations
- [ ] Secure random number generation
- [ ] Proper key management
- [ ] Keys stored in secure vault or env vars

### Error Handling
- [ ] No sensitive info in error messages
- [ ] Stack traces not exposed to users
- [ ] Proper error logging (without secrets)
- [ ] Fail securely on errors

### Configuration
- [ ] Debug mode disabled in production
- [ ] Security headers configured
- [ ] CORS properly configured
- [ ] HTTPS enforced
- [ ] Secure cookie flags set
- [ ] Rate limiting implemented

### Dependencies
- [ ] No known vulnerabilities (check CVE databases)
- [ ] Dependencies up to date
- [ ] Version pinning used
- [ ] Regular security updates

### Secrets
- [ ] No hardcoded secrets
- [ ] All secrets in environment variables
- [ ] .env files in .gitignore
- [ ] Secrets rotation strategy

## Common Security Mistakes to Avoid

1. **Trusting client-side validation** - Always validate on server
2. **Using string concatenation in SQL** - Use parameterized queries
3. **Storing passwords in plain text** - Use strong hashing
4. **Hardcoding secrets** - Use environment variables
5. **Ignoring authorization** - Check permissions on every request
6. **Exposing detailed errors** - Return generic messages to users
7. **Using weak crypto** - Use proven libraries and algorithms
8. **Not updating dependencies** - Regularly update for security patches
9. **Logging sensitive data** - Filter secrets from logs
10. **Allowing arbitrary file uploads** - Validate type, size, and content

## Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OWASP Cheat Sheets: https://cheatsheetseries.owasp.org/
- Django Security: https://docs.djangoproject.com/en/stable/topics/security/
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
- Python Security: https://python.readthedocs.io/en/latest/library/security_warnings.html

## Skill Metadata

**Skill Name:** Secure Coding
**Version:** 1.0
**Last Updated:** February 14, 2026
**Applicable To:** Coding Agent, Code Inspector, Security Agent
**Dependencies:** None
**Related Skills:** secrets-detection-skill.md, dependency-security-skill.md
