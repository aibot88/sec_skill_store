---
name: production-system-audit
description: Comprehensive system audit methodology for production web applications. Use when auditing systems before launch, identifying technical debt, troubleshooting systematic issues, preparing for security reviews, or creating improvement roadmaps. Systematically audits database schema, API endpoints, external integrations, performance, security, and monitoring across all layers.
---

# Production System Audit

Systematically audit production systems to identify weaknesses, single points of failure, and troubleshooting spots before they become problems.

## When to Use This Skill

- **Pre-production launch** - Audit before going live to catch issues early
- **Technical debt assessment** - Identify accumulated issues in existing systems
- **Systematic troubleshooting** - Debug issues that span multiple layers
- **Security review preparation** - Comprehensive security and reliability audit
- **Scaling preparation** - Identify bottlenecks before traffic increases

## Core Principles

**Systematic, not symptomatic:** Audit all layers methodically, don't just fix visible bugs.

**Severity-based prioritization:** Categorize findings as Critical/High/Medium/Low to guide action.

**Actionable recommendations:** Every finding includes specific fix guidance, not just problem description.

**Comprehensive coverage:** Database → APIs → Integrations → Performance → Security → Monitoring.

## Audit Workflow

### Phase 1: Architecture Audit

Audit the foundational layers: database schema, API endpoints, and core architecture.

**1.1 Database Schema Audit**

Read `/home/ubuntu/skills/production-system-audit/references/database-audit-checklist.md` and systematically check:
- Foreign key constraints and referential integrity
- Indexes on foreign keys and common query patterns
- Unique constraints on natural keys
- Data types, lengths, and NOT NULL constraints
- Timestamps and audit trails
- JSON column usage
- Enum definitions
- Cascading deletes and orphaned record prevention

**1.2 API Endpoint Audit**

Read `/home/ubuntu/skills/production-system-audit/references/api-audit-checklist.md` and systematically check:
- Input validation (Zod schemas, range checks, format validation)
- Error handling (TRPCError usage, appropriate codes, descriptive messages)
- Authentication and authorization (procedure types, ownership checks)
- Rate limiting on expensive operations
- Pagination on list endpoints
- Data sanitization
- Transaction handling
- Response size limits

**Output:** Document all findings with severity, impact, examples, and recommendations.

---

### Phase 2: Integration Audit

Audit external service integrations for reliability and security.

Read `/home/ubuntu/skills/production-system-audit/references/integration-audit-checklist.md` and check each integration:

**Common Integrations to Audit:**
- AI services (Hume AI, OpenAI, etc.)
- Communication services (Twilio, SendGrid, etc.)
- Storage services (S3, Cloudinary, etc.)
- Database services (Supabase, PlanetScale, etc.)
- Payment services (Stripe, PayPal, etc.)

**For each integration, check:**
- Error handling and retry logic
- Timeout configuration
- API key and credential management
- Webhook security (signature verification)
- Resource cleanup (no unbounded accumulation)
- Rate limit handling
- Data validation from external sources
- Webhook reliability (async processing, idempotency)
- Connection pooling
- Service health monitoring

**Output:** Document integration-specific issues with recommendations.

---

### Phase 3: Performance & Scalability Audit

Identify performance bottlenecks and scalability issues.

**3.1 Database Query Performance**

Identify slow queries:
- Full table scans without indexes
- N+1 query problems
- Missing composite indexes for common filters
- Inefficient JOIN operations
- Unbounded result sets

**3.2 API Response Times**

Measure baseline performance:
- Average response times for critical endpoints
- Slow endpoints (>500ms)
- Endpoints without caching that should have it

**3.3 Concurrent Usage**

Identify untested scenarios:
- Multiple users creating resources simultaneously
- Race conditions in status updates
- Concurrent access to shared resources
- Load testing gaps

**Output:** List performance bottlenecks with optimization recommendations.

---

### Phase 4: Monitoring & Observability Audit

Identify gaps in logging, error tracking, and health checks.

**4.1 Logging Gaps**

Check for missing logging:
- External API call success/failure rates
- File upload/download operations
- User action tracking
- Performance metrics (response times, query times)
- Security events (login attempts, permission denials)

**4.2 Error Tracking**

Assess current error tracking:
- Centralized error tracking (Sentry, etc.)
- Error aggregation and alerting
- Error rate monitoring
- Stack trace capture

**4.3 Health Checks**

Identify missing health checks:
- Database connection health
- External service availability (Hume AI, Twilio, S3, etc.)
- Disk space, memory usage
- `/api/health` endpoint with dependency checks

**Output:** Monitoring and observability improvement plan.

---

### Phase 5: Security Audit

Identify security vulnerabilities and compliance gaps.

**5.1 Input Validation**

Check for missing validation:
- Phone number formats
- Email formats
- Code/identifier formats
- File upload types and sizes
- User-provided content sanitization

**5.2 Data Sanitization**

Check for XSS and injection risks:
- User-provided content displayed as HTML
- Script content not sanitized
- SQL injection prevention (parameterized queries)
- No eval() or dangerous functions

**5.3 API Security**

Check for security gaps:
- Rate limiting on all endpoints
- Request size limits
- Webhook signature verification
- HTTPS enforcement
- CORS configuration

**Output:** Security findings with remediation steps.

---

## Deliverables

### 1. Comprehensive Audit Report

Use the template at `/home/ubuntu/skills/production-system-audit/templates/audit-report-template.md`.

**Structure:**
- Executive Summary (overall health, issue counts)
- Phase 1: Architecture Audit (database, APIs)
- Phase 2: Integration Audit (external services)
- Phase 3: Performance & Scalability
- Phase 4: Monitoring & Observability
- Phase 5: Security Audit
- Summary of Findings (categorized by severity)
- Recommended Action Plan (4-week roadmap)
- Troubleshooting Guide (common failure scenarios)

### 2. Prioritized Improvement Roadmap

**Week 1:** Critical and high-priority issues  
**Week 2:** Medium-priority issues (performance, monitoring)  
**Week 3:** Medium-priority issues (security, reliability)  
**Week 4:** Low-priority issues (nice-to-haves, cleanup)

### 3. Troubleshooting Guide

Document common failure scenarios with:
- Symptoms (what user sees)
- Possible causes
- Debugging steps
- Prevention strategies

---

## Severity Classification

Use consistent severity levels across all findings:

**🔴 CRITICAL** - System broken, data loss possible, security breach  
*Fix immediately (same day)*

**🔴 HIGH** - Data integrity risk, major functionality broken, significant security gap  
*Fix within 1 week*

**🟡 MEDIUM** - Performance degradation, poor UX, moderate security risk  
*Fix within 1 month*

**🟢 LOW** - Minor issues, nice-to-haves, limited impact  
*Fix when convenient*

---

## Tips

**Start broad, then deep:** Audit all areas at high level first, then dive deep into problem areas.

**Use checklists systematically:** Don't skip items—systematic coverage catches hidden issues.

**Provide examples:** Every finding should include code snippet or scenario showing the problem.

**Be specific in recommendations:** "Add foreign key constraints" is better than "improve data integrity."

**Test your findings:** Verify issues exist before documenting (run queries, test endpoints).

**Consider the audience:** Technical findings for engineers, executive summary for leadership.

---

## Common Gotchas

**Don't just audit code:** Also check deployment config, environment variables, DNS, SSL certs.

**Don't ignore "working" systems:** Just because it works doesn't mean it's correct (e.g., missing FK constraints).

**Don't assume test coverage:** Verify tests exist and pass for critical paths.

**Don't skip documentation:** Undocumented systems are harder to maintain and debug.

**Don't forget cleanup:** Temporary resources, expired codes, old configs—all accumulate over time.
