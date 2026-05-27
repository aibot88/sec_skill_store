---
skill: senior-architect-design
description: Design production-ready software products following senior architect principles - from requirements to deployment architecture. Focus on scalability, security, maintainability, and real-world constraints.
version: 1.0
tags: [architecture, design, product-design, system-design, senior-architect]
---

# Senior Architect Product Design Skill

## Purpose

This skill guides you through designing a complete software product using senior architect principles and best practices. It covers everything from initial requirements to deployment architecture, focusing on:
- **Production-ready designs** (no theoretical concepts)
- **Business-driven decisions** (align with business goals)
- **Scalable & maintainable** (think long-term)
- **Security-first** (bake in from day one)
- **Cost-conscious** (optimize for value)

## When to Use This Skill

Use this skill when:
- Starting a new product/feature from scratch
- Redesigning an existing system
- Evaluating architectural decisions
- Planning major feature additions
- Scaling an existing application
- Moving to cloud/microservices
- Designing multi-tenant SaaS platforms

## Architecture Design Phases

### Phase 1: Requirements & Business Analysis (Foundation)

**Goal**: Understand WHAT and WHY before HOW

#### 1.1 Gather Functional Requirements
```
Questions to Answer:
□ Who are the users? (roles, personas)
□ What problems are we solving?
□ What are the core features?
□ What workflows are critical?
□ What are the success metrics?
□ What data needs to be managed?
□ What integrations are needed?
```

**Output**: Feature list with priorities (Must-have, Should-have, Nice-to-have)

#### 1.2 Define Non-Functional Requirements
```
Critical Decisions:
□ Expected user load? (10, 100, 10k, 100k users?)
□ Response time requirements? (< 200ms, < 1s, < 5s?)
□ Availability target? (99%, 99.9%, 99.99%?)
□ Data retention policies?
□ Compliance requirements? (GDPR, HIPAA, SOC2)
□ Mobile support required?
□ Offline capabilities needed?
```

**Output**: Non-functional requirements document

#### 1.3 Identify Constraints
```
Real-World Constraints:
□ Budget limitations?
□ Timeline constraints?
□ Team size/skills?
□ Legacy system integrations?
□ Technology preferences/restrictions?
□ Regulatory requirements?
□ Geographic restrictions?
```

**Output**: Constraints matrix with mitigation strategies

---

### Phase 2: System Architecture Design (High-Level)

**Goal**: Define overall system structure and components

#### 2.1 Choose Architectural Pattern

**Decision Tree**:
```
Q: Single tenant or multi-tenant?
└─ Multi-tenant → SaaS Architecture
   Q: How many tenants expected?
   ├─ < 100 → Shared DB with tenant_id
   ├─ 100-1000 → Separate schemas
   └─ > 1000 → Separate databases

Q: Monolith or microservices?
├─ Small team, simple domain → Modular Monolith
├─ Multiple teams, complex domain → Microservices
└─ Rapid MVP → Monolith (prepare for split)

Q: Stateful or stateless?
└─ Always prefer stateless (use Redis/DB for state)
```

**Senior Architect Principles**:
- ✅ Start simple, evolve to complex (not reverse)
- ✅ Prefer boring technology (proven > trendy)
- ✅ Design for 10x scale, not 100x
- ✅ Make reversible decisions when possible
- ✅ Document why, not just what

#### 2.2 Design System Components

**Core Components Checklist**:
```
□ API Layer (REST, GraphQL, gRPC?)
□ Authentication/Authorization (OAuth2, JWT, SAML?)
□ Business Logic Layer (Domain-driven design?)
□ Data Access Layer (ORM, Query Builder, Raw SQL?)
□ Cache Layer (Redis, Memcached?)
□ Message Queue (Kafka, RabbitMQ, SQS?) - if needed
□ File Storage (Local, S3, Azure Blob?)
□ Search Engine (Elasticsearch, Algolia?) - if needed
□ Background Jobs (Celery, Sidekiq, Bull?) - if needed
```

**Architecture Diagram Template**:
```
┌──────────────────────────────────────────┐
│         Client Layer                      │
│  (Web, Mobile, API Consumers)            │
└──────────────┬───────────────────────────┘
               │
┌──────────────▼───────────────────────────┐
│         API Gateway / Load Balancer       │
│  (NGINX, Kong, AWS ALB)                  │
└──────────────┬───────────────────────────┘
               │
┌──────────────▼───────────────────────────┐
│    Authentication & Authorization         │
│  (JWT, OAuth2, Capability-based)         │
└──────────────┬───────────────────────────┘
               │
┌──────────────▼───────────────────────────┐
│      Application Layer                    │
│  ┌──────────────────────────────────┐    │
│  │  Controllers / API Endpoints     │    │
│  ├──────────────────────────────────┤    │
│  │  Business Services               │    │
│  ├──────────────────────────────────┤    │
│  │  Domain Entities                 │    │
│  └──────────────────────────────────┘    │
└──────────────┬───────────────────────────┘
               │
┌──────────────▼───────────────────────────┐
│     Data Layer                            │
│  ┌─────────┐  ┌────────┐  ┌──────────┐  │
│  │   DB    │  │ Redis  │  │  S3/CDN  │  │
│  └─────────┘  └────────┘  └──────────┘  │
└───────────────────────────────────────────┘
```

#### 2.3 Technology Stack Selection

**Backend Framework Decision**:
```
Team Expertise + Use Case = Framework Choice

Java Team + Enterprise? → Spring Boot
Python Team + ML/AI? → Django/FastAPI  
JavaScript Full-stack? → Node.js + Express/NestJS
C# Team + Microsoft Stack? → .NET Core
Go Team + High Performance? → Go with Gin/Echo
Ruby Team + Rapid Dev? → Rails
```

**Database Selection**:
```
Data Type + Access Pattern = Database Choice

Relational + Complex Queries → PostgreSQL/MySQL
Document Store + Flexible Schema → MongoDB
Key-Value + High Speed → Redis
Time-Series + Analytics → InfluxDB/TimescaleDB
Graph Relationships → Neo4j
Search + Full-text → Elasticsearch
```

**Senior Architect Rule**: 
> "Choose technology based on team expertise and problem fit, not resume-driven development"

---

### Phase 3: Data Model Design (Database Schema)

**Goal**: Design robust, scalable data models

#### 3.1 Entity Identification

**Process**:
1. Extract nouns from requirements → Candidate entities
2. Group related attributes → Refine entities
3. Identify relationships → Define foreign keys
4. Apply normalization → Eliminate redundancy

**Example for Construction ERP**:
```
Requirements: "Manage projects with workers, track attendance, create invoices"

Entities Identified:
- Organization (tenant)
- User (authentication)
- Project
- Worker
- Client
- Attendance
- Invoice
- Payment
```

#### 3.2 Design Database Schema

**Best Practices Checklist**:
```
For Each Table:
□ UUID primary keys (not auto-increment for distributed systems)
□ tenant_id column (for multi-tenant)
□ created_at, updated_at timestamps (audit trail)
□ created_by, updated_by user tracking
□ is_deleted flag (soft deletes)
□ deleted_at timestamp
□ version column (optimistic locking if needed)

Relationships:
□ Foreign keys with proper constraints
□ Junction tables for many-to-many
□ Indexes on foreign keys
□ Indexes on frequently queried columns
□ Composite indexes for complex queries

Data Types:
□ VARCHAR with appropriate lengths (not VARCHAR(MAX))
□ DECIMAL for money (never FLOAT)
□ TIMESTAMP with timezone
□ ENUM for fixed values (or separate reference table)
```

**Schema Design Pattern (Multi-tenant)**:
```sql
-- Base pattern for all tenant-scoped tables
CREATE TABLE {entity_name} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES organizations(id),
    -- entity-specific columns here
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP,
    INDEX idx_{entity}_tenant (tenant_id),
    INDEX idx_{entity}_created (created_at),
    INDEX idx_{entity}_deleted (is_deleted)
);
```

#### 3.3 Plan for Scale

**Database Scaling Strategies**:
```
Current Load → Strategy

< 1000 QPS → Single master database
1000-10k QPS → Master + Read replicas
10k-50k QPS → Sharding by tenant_id
> 50k QPS → Microservices + separate DBs
```

**Optimization Techniques**:
- ✅ Connection pooling (HikariCP, PgBouncer)
- ✅ Query optimization (EXPLAIN ANALYZE)
- ✅ Materialized views for complex reports
- ✅ Partitioning for large tables (by date/tenant)
- ✅ Archiving old data

---

### Phase 4: API Design (Interface Contracts)

**Goal**: Design clean, consistent, RESTful APIs

#### 4.1 API Design Principles

**RESTful URL Structure**:
```
Resource-based (not action-based):
✅ GET    /api/projects              (list)
✅ POST   /api/projects              (create)
✅ GET    /api/projects/{id}         (detail)
✅ PUT    /api/projects/{id}         (update)
✅ DELETE /api/projects/{id}         (delete)
✅ POST   /api/projects/{id}/approve (action)

❌ /api/getProjects
❌ /api/createNewProject
❌ /api/updateProjectById
```

**URL Conventions**:
- Use nouns, not verbs
- Plural for collections (`/users`, not `/user`)
- Nested for relationships (`/projects/{id}/workers`)
- Actions as sub-resources (`/invoices/{id}/send`)
- Filters as query params (`/projects?status=active`)

#### 4.2 Request/Response Design

**Standard Response Format**:
```json
{
  "success": true,
  "data": {
    // actual response data
  },
  "meta": {
    "timestamp": "2026-03-08T10:30:00Z",
    "page": 1,
    "pageSize": 20,
    "totalPages": 5,
    "totalCount": 98
  }
}
```

**Error Response Format**:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  },
  "meta": {
    "timestamp": "2026-03-08T10:30:00Z",
    "requestId": "req-123-456"
  }
}
```

**HTTP Status Codes (Use Correctly)**:
```
2xx Success:
200 OK - Successful GET, PUT, DELETE
201 Created - Successful POST
204 No Content - Successful DELETE (no body)

4xx Client Errors:
400 Bad Request - Invalid input
401 Unauthorized - Not authenticated
403 Forbidden - Not authorized (authenticated but no permission)
404 Not Found - Resource doesn't exist
409 Conflict - Duplicate/constraint violation
422 Unprocessable Entity - Validation error

5xx Server Errors:
500 Internal Server Error - Unexpected server error
503 Service Unavailable - Server overloaded/maintenance
```

#### 4.3 API Versioning

**Versioning Strategy**:
```
Choose one approach (be consistent):

1. URL Versioning (Recommended):
   /api/v1/projects
   /api/v2/projects

2. Header Versioning:
   Accept: application/vnd.company.v1+json

3. Query Parameter:
   /api/projects?version=1
```

**Version Migration Plan**:
- Support 2 versions simultaneously
- Deprecate old version with 6-month notice
- Monitor usage before retiring

---

### Phase 5: Security Architecture (Defense in Depth)

**Goal**: Build security into every layer

#### 5.1 Authentication Design

**Choose Authentication Method**:
```
Use Case → Authentication

API only / Mobile → JWT (stateless)
Web + API → JWT + Refresh Token
Enterprise SSO → OAuth2 + SAML
Internal tools → Session-based
B2C with social → OAuth2 (Google, GitHub, etc.)
High security → JWT + MFA
```

**JWT Token Design**:
```json
{
  "sub": "user-id",
  "email": "user@example.com",
  "tenantId": "tenant-id",
  "roles": ["ADMIN"],
  "capabilities": ["USER_CREATE", "PROJECT_VIEW"],
  "iat": 1710000000,
  "exp": 1710086400
}
```

**Token Storage**:
- ✅ Access Token: Memory (React state/context)
- ✅ Refresh Token: HttpOnly cookie
- ❌ Never: localStorage (XSS vulnerable)

#### 5.2 Authorization Design

**Choose Authorization Model**:
```
Simple app (< 5 roles) → Role-Based (RBAC)
Complex permissions → Capability-Based
Multi-tenant → Tenant + Capability
Fine-grained control → Attribute-Based (ABAC)
```

**Capability-Based Authorization Pattern**:
```java
// Define capabilities
enum Capability {
    USER_CREATE,
    PROJECT_VIEW_STRATEGIC,
    BUDGET_APPROVE,
    INVOICE_CREATE
}

// Map roles to capabilities
class RoleCapabilityService {
    Map<Role, Set<Capability>> roleCapabilities = {
        OWNER: [BUDGET_APPROVE, PROJECT_VIEW_STRATEGIC],
        ADMIN: [USER_CREATE, PROJECT_VIEW_OPERATIONAL],
        ACCOUNTANT: [INVOICE_CREATE, PAYROLL_PROCESS]
    };
}

// Use in controller
@PostMapping("/projects")
@RequireCapability(Capability.PROJECT_CREATE)
public ProjectResponse createProject() { }
```

#### 5.3 Security Checklist

**Essential Security Measures**:
```
Authentication:
□ BCrypt/Argon2 for password hashing (never MD5/SHA1)
□ Rate limiting on login (5 attempts/min)
□ HTTPS everywhere (enforce, no mixed content)
□ JWT with short expiration (15min-24h)
□ Refresh token rotation
□ MFA for admin accounts

Authorization:
□ Least privilege principle
□ Capability-based access control
□ Tenant isolation (never trust client input)
□ Row-level security (tenant_id filter)
□ API endpoint authorization checks

Input Validation:
□ Validate all input (whitelist, not blacklist)
□ Parameterized queries (prevent SQL injection)
□ Escape HTML output (prevent XSS)
□ CSRF tokens for state-changing operations
□ File upload validation (type, size, content)

Data Protection:
□ Encrypt sensitive data at rest
□ TLS 1.3 for data in transit
□ PII encryption (GDPR compliance)
□ Secrets in environment variables (not code)
□ API key rotation policy

Headers:
□ Content-Security-Policy
□ X-Content-Type-Options: nosniff
□ X-Frame-Options: DENY
□ Strict-Transport-Security
□ X-XSS-Protection
```

---

### Phase 6: Scalability & Performance Design

**Goal**: Design for growth and efficiency

#### 6.1 Caching Strategy

**Cache Layers**:
```
Layer 1 - Client Side:
- Browser cache (static assets)
- Service worker (PWA)
- Local storage (user preferences)

Layer 2 - CDN:
- CloudFront, Cloudflare
- Static files (JS, CSS, images)
- API responses (when appropriate)

Layer 3 - Application Cache:
- In-memory cache (Caffeine, Guava)
- Response caching (read-heavy data)
- Session storage

Layer 4 - Distributed Cache:
- Redis/Memcached
- User sessions
- API response cache
- Database query results

Layer 5 - Database Cache:
- Query result cache
- Connection pooling
```

**What to Cache**:
```
✅ Cache (read-heavy, slow to compute):
- User profiles
- Configuration settings
- Reference data (countries, currencies)
- Aggregated reports
- Frequently accessed entities

❌ Don't Cache (write-heavy, real-time):
- Financial transactions
- Audit logs
- Real-time notifications
- User-specific dynamic data
```

**Cache Invalidation Strategy**:
```
TTL (Time-to-Live):
- Short TTL (1-5 min): Frequently changing data
- Medium TTL (1-24 hours): Reference data
- Long TTL (1-7 days): Static data

Event-based:
- Invalidate on write operations
- Pub/sub pattern for cache updates
- Version-based cache keys
```

#### 6.2 Database Performance

**Query Optimization**:
```
□ Index on foreign keys
□ Composite index for multi-column WHERE
□ Cover index for SELECT columns
□ Avoid SELECT * (fetch only needed columns)
□ Use LIMIT for pagination
□ Avoid N+1 queries (use JOIN or batch loading)
□ Use prepared statements
□ Connection pooling (HikariCP)
```

**Read-Heavy Workload Pattern**:
```
Write → Master DB
Read → Read Replicas (multiple)

Benefits:
- Distribute read load
- Low latency reads
- Fault tolerance
```

**Write-Heavy Workload Pattern**:
```
Write → Queue → Batch Insert
       ↓
    Process async

Benefits:
- Buffer spikes
- Batch operations
- Async processing
```

#### 6.3 Horizontal Scaling

**Stateless Application Design**:
```
✅ Good (Stateless):
- Store session in Redis
- Store files in S3
- Store state in database
- JWT tokens (no server state)

❌ Bad (Stateful):
- In-memory sessions
- Local file storage
- Server-specific state
```

**Load Balancing Strategy**:
```
Algorithm → Use Case

Round Robin → Equal server capacity
Least Connections → Variable request duration
IP Hash → Sticky sessions needed
Weighted → Different server capacities
```

---

### Phase 7: Multi-Tenancy Design (SaaS Architecture)

**Goal**: Isolate tenant data securely and efficiently

#### 7.1 Choose Multi-Tenancy Model

**Decision Matrix**:
```
Factor                  | Shared DB | Shared Schema | Separate DB
------------------------|-----------|---------------|-------------
Cost                    | Low       | Medium        | High
Isolation               | Medium    | Good          | Excellent
Scaling Complexity      | Low       | Medium        | High
Backup/Restore          | Complex   | Medium        | Simple
Per-Tenant Customization| Hard      | Medium        | Easy
Development Complexity  | Low       | Medium        | High

Recommendation:
- < 100 tenants: Shared DB + tenant_id
- 100-1000 tenants: Shared schema
- > 1000 tenants: Separate DB
```

#### 7.2 Implement Tenant Isolation (Shared DB)

**Pattern: Row-Level Security with tenant_id**

**Step 1: Base Entity**
```java
@MappedSuperclass
@FilterDef(name = "tenantFilter", 
           parameters = @ParamDef(name = "tenantId", type = UUID.class))
@Filter(name = "tenantFilter", condition = "tenant_id = :tenantId")
public abstract class BaseEntity {
    @Id
    @GeneratedValue
    private UUID id;
    
    @Column(name = "tenant_id", nullable = false)
    private UUID tenantId;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @Column(name = "is_deleted")
    private Boolean isDeleted = false;
}
```

**Step 2: Tenant Context**
```java
public class TenantContext {
    private static final ThreadLocal<UUID> currentTenant = new ThreadLocal<>();
    
    public static void setTenant(UUID tenantId) {
        currentTenant.set(tenantId);
    }
    
    public static UUID getTenant() {
        return currentTenant.get();
    }
    
    public static void clear() {
        currentTenant.remove();
    }
}
```

**Step 3: Security Filter**
```java
public class TenantFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest request, 
                                     HttpServletResponse response,
                                     FilterChain filterChain) {
        UUID tenantId = extractTenantFromJWT(request);
        TenantContext.setTenant(tenantId);
        
        try {
            filterChain.doFilter(request, response);
        } finally {
            TenantContext.clear();
        }
    }
}
```

**Step 4: Enable Hibernate Filter**
```java
@Aspect
@Component
public class TenantAspect {
    @Before("execution(* com.example.repository.*.*(..))")
    public void enableTenantFilter() {
        Session session = entityManager.unwrap(Session.class);
        Filter filter = session.enableFilter("tenantFilter");
        filter.setParameter("tenantId", TenantContext.getTenant());
    }
}
```

#### 7.3 Tenant-Aware Features

**Checklist**:
```
□ Tenant isolation verified (automatic WHERE tenant_id = ?)
□ Cross-tenant access blocked
□ Tenant-specific configuration
□ Per-tenant file storage (S3 prefix: tenant-id/)
□ Tenant-specific subdomain (tenant.app.com)
□ Tenant-level analytics
□ Per-tenant rate limiting
□ Tenant-specific backups
```

---

### Phase 8: Monitoring & Observability

**Goal**: Know what's happening in production

#### 8.1 The Three Pillars

**1. Metrics (What's happening)**
```
Application Metrics:
□ Request rate (req/sec)
□ Response time (p50, p95, p99)
□ Error rate (4xx, 5xx)
□ Active users
□ Business metrics (signups, transactions)

System Metrics:
□ CPU usage
□ Memory usage
□ Disk I/O
□ Network traffic

Database Metrics:
□ Query performance
□ Connection pool usage
□ Slow queries
□ Replication lag
```

**Tools**: Prometheus, Grafana, CloudWatch, DataDog

**2. Logs (What happened)**
```
Log Levels:
ERROR - Production issues requiring immediate attention
WARN - Potential issues, recoverable
INFO - Important business events
DEBUG - Detailed diagnostic info (dev/staging only)

Structured Logging (JSON):
{
  "level": "ERROR",
  "timestamp": "2026-03-08T10:30:00Z",
  "service": "api",
  "tenantId": "tenant-123",
  "userId": "user-456",
  "requestId": "req-789",
  "message": "Payment processing failed",
  "error": "InsufficientFunds",
  "stack": "..."
}
```

**Tools**: ELK Stack (Elasticsearch, Logstash, Kibana), Splunk, CloudWatch Logs

**3. Traces (How requests flow)**
```
Distributed Tracing:
- Track request across services
- Identify bottlenecks
- Visualize call chains
- Measure latencies
```

**Tools**: Jaeger, Zipkin, AWS X-Ray

#### 8.2 Alerting Strategy

**Alert Priority**:
```
P1 (Page immediately):
- Service down
- Error rate > 5%
- Payment processing failed
- Database unavailable

P2 (Notify within 30min):
- High response time (p95 > 2s)
- Disk space > 80%
- Memory usage > 85%
- API rate limit hit

P3 (Daily digest):
- Deprecated API usage
- Certificate expiring (> 30 days)
- Slow queries
```

**Alert Fatigue Prevention**:
- Set realistic thresholds
- Group related alerts
- Implement backoff (don't spam)
- Regular alert review/tuning

---

### Phase 9: DevOps & Deployment

**Goal**: Reliable, automated deployments

#### 9.1 CI/CD Pipeline

**Pipeline Stages**:
```
1. Code Commit (GitHub, GitLab)
   ↓
2. Build
   - Compile code
   - Run linter
   - Security scan
   ↓
3. Test
   - Unit tests
   - Integration tests
   - Code coverage check
   ↓
4. Package
   - Build Docker image
   - Tag with version
   - Push to registry
   ↓
5. Deploy to Staging
   - Run smoke tests
   - Integration tests
   - Manual QA
   ↓
6. Deploy to Production
   - Blue-green deployment
   - Rolling update
   - Canary release
   ↓
7. Verify
   - Health checks
   - Smoke tests
   - Monitor metrics
```

#### 9.2 Deployment Strategies

**Choose Based on Risk Tolerance**:

```
1. Blue-Green Deployment:
   OLD [100%] ──switch──> NEW [100%]
   - Zero downtime
   - Instant rollback
   - Double infrastructure cost

2. Rolling Update:
   [25%] [25%] [25%] [25%]
     ↓     ↓     ↓     ↓
   [NEW] [25%] [25%] [25%]
   [NEW] [NEW] [25%] [25%]
   [NEW] [NEW] [NEW] [25%]
   [NEW] [NEW] [NEW] [NEW]
   - Gradual rollout
   - No extra infrastructure
   - Slower rollback

3. Canary Release:
   OLD [95%] → NEW [5%] → Monitor
   - Test on small subset
   - Low risk
   - Gradual increase
```

#### 9.3 Infrastructure as Code

**Use Tools**:
- Docker Compose (development)
- Kubernetes (production orchestration)
- Terraform (cloud infrastructure)
- Ansible (configuration management)

**Example Docker Compose**:
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - postgres
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: myapp
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}

volumes:
  postgres_data:
```

---

### Phase 10: Documentation & Handoff

**Goal**: Enable team to maintain and extend the system

#### 10.1 Essential Documentation

**Create These Documents**:
```
1. Architecture Decision Records (ADR)
   - What decision was made
   - Why (context, alternatives considered)
   - Consequences

2. System Architecture Diagram
   - High-level component view
   - Data flow diagrams
   - Deployment architecture

3. API Documentation
   - OpenAPI/Swagger spec
   - Request/response examples
   - Error codes

4. Database Schema
   - ER diagram
   - Table definitions
   - Relationships

5. Runbook
   - Deployment procedure
   - Rollback procedure
   - Troubleshooting guide
   - Common issues & solutions

6. Security Guidelines
   - Authentication flow
   - Authorization model
   - Secrets management
   - Security best practices

7. Development Setup
   - Prerequisites
   - Local development
   - Running tests
   - Debugging tips
```

#### 10.2 Code Quality Standards

**Establish Standards**:
```
Code Style:
□ Use consistent formatting (Prettier, Black, gofmt)
□ Follow language conventions (PEP8, Google Java Style)
□ Meaningful variable names
□ Functions < 50 lines
□ Classes < 300 lines

Code Review Checklist:
□ Tests included?
□ Documentation updated?
□ Security considered?
□ Performance impact?
□ Backward compatible?
□ Error handling added?

Testing Requirements:
□ Unit tests (80% coverage minimum)
□ Integration tests for APIs
□ E2E tests for critical flows
□ Performance tests for key endpoints
```

---

## Senior Architect Decision Framework

When making any architectural decision, use this framework:

### 1. Understand the Problem
- What problem are we solving?
- Who is affected?
- What are the constraints?

### 2. Consider Alternatives
- List at least 3 options
- Pros & cons of each
- Cost/complexity trade-offs

### 3. Make Decision
- Choose based on:
  - Business value
  - Team capabilities
  - Time constraints
  - Technical fit

### 4. Document Decision
- Write ADR (Architecture Decision Record)
- Include: context, decision, consequences

### 5. Validate Assumption
- Build proof-of-concept if uncertain
- Measure/test assumptions
- Be ready to pivot

---

## Anti-Patterns to Avoid

### ❌ Resume-Driven Development
Don't choose technology to pad resume
Choose based on fit and team expertise

### ❌ Premature Optimization
Don't optimize before measuring
"Premature optimization is the root of all evil"

### ❌ Over-Engineering
Don't build for hypothetical future
YAGNI (You Aren't Gonna Need It)

### ❌ Under-Engineering
Don't skip fundamentals (security, testing, monitoring)
Technical debt compounds

### ❌ Cargo Cult Programming
Don't copy patterns without understanding
Understand WHY, not just WHAT

### ❌ Not Invented Here Syndrome
Don't reinvent wheel unncessarily
Use proven libraries/frameworks

### ❌ Ignoring Non-Functionals
Don't focus only on features
Security, performance, reliability matter

---

## Quality Gates Checklist

Before declaring design complete, verify:

### ✅ Business Alignment
- [ ] Solves actual business problem
- [ ] Delivers measurable value
- [ ] Feasible within constraints
- [ ] Aligned with business goals

### ✅ Technical Soundness
- [ ] Scalability considered
- [ ] Security built-in
- [ ] Monitoring planned
- [ ] Failure modes identified
- [ ] Performance targets defined

### ✅ Team Readiness
- [ ] Team has required skills
- [ ] Tools/technologies familiar
- [ ] Documentation sufficient
- [ ] Runbook created
- [ ] Training plan if needed

### ✅ Operational Excellence
- [ ] Deployment strategy defined
- [ ] Rollback plan exists
- [ ] Monitoring setup
- [ ] Alerting configured
- [ ] Backup/restore tested

### ✅ Long-term Maintainability
- [ ] Code is readable
- [ ] Architecture is modular
- [ ] Dependencies manageable
- [ ] Testing strategy solid
- [ ] Documentation complete

---

## Templates & Checklists

### Architecture Decision Record (ADR) Template

```markdown
# ADR-001: [Decision Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
What is the issue we're trying to solve? What constraints exist?

## Decision
What did we decide? Be specific.

## Alternatives Considered
1. Alternative A - Pros/Cons
2. Alternative B - Pros/Cons
3. Alternative C - Pros/Cons

## Consequences
What are the results (good and bad)?
- Positive consequences
- Negative consequences
- Trade-offs accepted

## References
Links to relevant documentation, research, etc.
```

### System Design Review Checklist

```markdown
## Functional Requirements
- [ ] All user stories covered
- [ ] Edge cases identified
- [ ] Error scenarios handled
- [ ] Workflows documented

## Non-Functional Requirements
- [ ] Performance targets defined
- [ ] Scalability plan exists
- [ ] Security requirements met
- [ ] Availability target set
- [ ] Data retention policy

## Architecture
- [ ] Component diagram created
- [ ] Data flow documented
- [ ] Integration points identified
- [ ] API contracts defined
- [ ] Database schema designed

## Security
- [ ] Authentication designed
- [ ] Authorization implemented
- [ ] Data encryption planned
- [ ] Secrets management
- [ ] Compliance requirements

## Operations
- [ ] Deployment strategy
- [ ] Monitoring plan
- [ ] Backup/restore procedure
- [ ] Disaster recovery plan
- [ ] Runbook created

## Documentation
- [ ] Architecture doc written
- [ ] API documentation
- [ ] Database schema doc
- [ ] Setup instructions
- [ ] Troubleshooting guide
```

---

## Example Prompts to Use This Skill

- "Design a multi-tenant SaaS platform for project management following senior architect principles"
- "Design the architecture for a real-time chat application with 100k concurrent users"
- "Create a scalable e-commerce platform design with payment processing"
- "Design a microservices architecture for a healthcare management system"
- "Plan the architecture for migrating a monolith to microservices"

---

## Related Skills to Create

Consider these complementary skills:
- `feature-implementation.md` - Implement features following design
- `security-audit.md` - Review and harden security
- `performance-optimization.md` - Identify and fix bottlenecks
- `database-migration.md` - Safely evolve schema
- `api-versioning.md` - Manage API evolution
- `microservices-decomposition.md` - Break monolith into services

---

## Success Metrics

A well-designed system should achieve:
- ✅ Meets functional requirements
- ✅ Meets non-functional requirements (performance, security, availability)
- ✅ Team can build and maintain it
- ✅ Scales to expected load
- ✅ Secure by design
- ✅ Observable in production
- ✅ Cost-effective
- ✅ Well-documented

---

**Remember**: 
> "Good architecture is less about the perfect design and more about making good trade-offs based on real constraints and requirements."
> 
> "Design for today's needs with tomorrow's scalability in mind, but don't over-engineer for a future that may never come."

---

**Last Updated**: March 8, 2026  
**Skill Version**: 1.0  
**Created By**: Senior Architecture Team
