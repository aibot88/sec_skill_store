---
name: security-infra
version: "1.0.0"
description: |
  Infrastructure security, headers, encryption, and compliance.

  Use when: (1) Configuring security headers (CSP, CORS, HSTS),
  (2) Setting up HTTPS/TLS, (3) Data encryption at rest/transit,
  (4) Implementing compliance (GDPR, PCI-DSS), (5) Secrets management.

  Auto-detects: helmet, csp, cors, hsts, https, tls, ssl, encrypt,
  gdpr, pci-dss, compliance, secret, vault, kms
related:
  - security
  - security-auth
  - devops
---

# Security Infrastructure Skill

Infrastructure security, headers, encryption, and compliance patterns.

## Quick Reference

### Security Headers

| Header | Purpose | Value |
|--------|---------|-------|
| Content-Security-Policy | XSS prevention | Restrict sources |
| X-Frame-Options | Clickjacking | DENY |
| Strict-Transport-Security | Force HTTPS | max-age=31536000 |
| X-Content-Type-Options | MIME sniffing | nosniff |
| Referrer-Policy | Leak prevention | strict-origin |

## Helmet.js Configuration

```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      objectSrc: ["'none'"],
      frameAncestors: ["'none'"],
    },
  },
  hsts: { maxAge: 31536000, includeSubDomains: true },
}));
```

## Encryption (AES-256-GCM)

```typescript
import crypto from 'crypto';

function encrypt(plaintext: string, key: Buffer): EncryptedData {
  const iv = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);

  let ciphertext = cipher.update(plaintext, 'utf8', 'base64');
  ciphertext += cipher.final('base64');

  return {
    ciphertext,
    iv: iv.toString('base64'),
    authTag: cipher.getAuthTag().toString('base64'),
  };
}

function decrypt(data: EncryptedData, key: Buffer): string {
  const decipher = crypto.createDecipheriv(
    'aes-256-gcm',
    key,
    Buffer.from(data.iv, 'base64')
  );
  decipher.setAuthTag(Buffer.from(data.authTag, 'base64'));

  let plaintext = decipher.update(data.ciphertext, 'base64', 'utf8');
  plaintext += decipher.final('utf8');

  return plaintext;
}
```

## Secrets Management

```typescript
// Environment variables (basic)
const apiKey = process.env.API_KEY;

// AWS Secrets Manager
import { SecretsManager } from '@aws-sdk/client-secrets-manager';
const client = new SecretsManager({ region: 'us-east-1' });
const secret = await client.getSecretValue({ SecretId: 'my-secret' });

// HashiCorp Vault
import Vault from 'node-vault';
const vault = Vault({ endpoint: process.env.VAULT_ADDR });
const { data } = await vault.read('secret/data/myapp');
```

## CORS Configuration

```typescript
import cors from 'cors';

app.use(cors({
  origin: ['https://app.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400,
}));
```

## Compliance Checklist

### GDPR Requirements
- [ ] Data minimization - collect only necessary data
- [ ] Consent management - explicit opt-in
- [ ] Right to erasure - delete user data on request
- [ ] Data portability - export user data
- [ ] Breach notification - 72-hour window

### PCI-DSS Requirements
- [ ] Encrypt cardholder data at rest
- [ ] Use TLS 1.2+ for transmission
- [ ] Implement strong access control
- [ ] Regular security testing
- [ ] Maintain security policy

## F5 Quality Gates

| Gate | Requirement |
|------|-------------|
| G4 | Security audit completed |
| G5 | Production hardening verified |
| G5 | Compliance checklist passed |
