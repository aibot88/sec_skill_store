---
name: expense-bot-architecture
description: Production-ready LINE bot with AI-powered expense tracking using TypeScript, Prisma, and Google Gemini. Comprehensive guide covering backend development, database design, AI integration, security, testing, and deployment.
tags:
  - typescript
  - line-bot
  - ai-integration
  - prisma
  - postgresql
  - architecture
  - production-ready
---

# 🎯 Skills & Technologies

โปรเจค Expense Bot นี้เป็นตัวอย่างที่ดีของการพัฒนา Production-Ready Application โดยครอบคลุมทักษะและเทคโนโลยีหลากหลายด้าน เหมาะสำหรับการเรียนรู้และนำไปประยุกต์ใช้

---

## 🎓 ทักษะที่ได้เรียนรู้

### 1. Backend Development

#### **Node.js + TypeScript**

- Type-safe development ด้วย TypeScript
- Async/Await patterns
- Error handling และ custom error classes
- Environment configuration ด้วย Zod validation
- Graceful shutdown handling

```typescript
// ตัวอย่าง: Type-safe configuration
const configSchema = z.object({
  LINE_CHANNEL_SECRET: z.string(),
  DATABASE_URL: z.string().url(),
  PORT: z.coerce.number().default(3000),
});
```

#### **Express.js Framework**

- RESTful API design
- Middleware architecture
- Route handling
- Request/Response lifecycle
- Error middleware chain

**เรียนรู้:**

- การสร้าง Express app ที่มี structure ดี
- Middleware pattern และการเรียงลำดับ
- Security best practices

---

### 2. Database Management

#### **PostgreSQL + Prisma ORM**

- Relational database design
- Schema modeling ด้วย Prisma
- Type-safe database queries
- Database migrations
- Connection pooling

```prisma
// ตัวอย่าง: Database schema design
model Expense {
  id          String   @id @default(cuid())
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  amount      Float
  category    Category? @relation(fields: [categoryId], references: [id])
  type        ExpenseType

  @@index([userId, date])  // Performance optimization
}
```

**เรียนรู้:**

- การออกแบบ ERD (Entity Relationship Diagram)
- Normalization และ relationship design
- Database indexing strategies
- Migration management

---

### 3. AI/ML Integration

#### **Google Gemini API**

- Large Language Model (LLM) integration
- Prompt engineering
- JSON mode และ structured output
- OCR และ Vision API
- Error handling และ fallback strategies

```typescript
// ตัวอย่าง: AI prompt engineering
const SYSTEM_PROMPT = `
คุณคือผู้ช่วยวิเคราะห์รายรับ-รายจ่าย
- วิเคราะห์ข้อความและแปลงเป็น JSON
- จัดหมวดหมู่อัตโนมัติ
- ตอบกลับเป็น JSON เท่านั้น
`;
```

**เรียนรู้:**

- การ integrate AI service แบบ production-ready
- Prompt engineering techniques
- Fallback parser ด้วย Regex
- Factory pattern สำหรับ multi-provider support

---

### 4. Third-Party API Integration

#### **LINE Messaging API**

- Webhook implementation
- Signature verification (HMAC-SHA256)
- Rich message formatting (Flex Message)
- Reply/Push messaging
- Event handling

**เรียนรู้:**

- การทำงานกับ webhook
- Security verification ด้วย signature
- Message formatting และ UX design
- Real-time messaging patterns

---

### 5. Security & Best Practices

#### **Application Security**

- HMAC signature verification
- Rate limiting (per IP, per endpoint)
- Security headers (Helmet.js)
- Environment variable management
- Input validation ด้วย Zod

```typescript
// ตัวอย่าง: Security layers
app.use(helmet()); // Security headers
app.use(generalRateLimiter); // DDoS protection
app.use(verifyLineSignature); // Auth verification
```

**เรียนรู้:**

- OWASP security principles
- Defense in depth strategy
- Timing attack prevention
- Rate limiting strategies

---

### 6. Software Design Patterns

#### **Patterns Used**

**1. Factory Pattern**

```typescript
function createAIProvider(): AIProvider {
  switch (config.AI_PROVIDER) {
    case "google":
      return new GoogleProvider();
    case "openai":
      return new OpenAIProvider();
  }
}
```

**2. Repository Pattern**

```typescript
// Abstraction ระหว่าง business logic และ data layer
export async function getMonthlySummary(userId: string) {
  const expenses = await prisma.expense.findMany({...})
  return calculateSummary(expenses)
}
```

**3. Middleware Chain**

```typescript
app.post(
  "/webhook",
  rateLimiter, // Layer 1: Rate limit
  verifySignature, // Layer 2: Auth
  asyncHandler(handler) // Layer 3: Business logic
);
```

**เรียนรู้:**

- Clean architecture principles
- Separation of concerns
- Dependency injection
- SOLID principles

---

### 7. Testing & Quality Assurance

#### **Testing Strategy**

- Unit tests ด้วย Jest
- Integration tests
- Mocking dependencies (Prisma, LINE)
- Test coverage reporting
- CI/CD integration

```typescript
// ตัวอย่าง: Unit test
describe("parseFallback", () => {
  it("should parse expense correctly", () => {
    const result = parseFallback("กินข้าว 120");
    expect(result.type).toBe("EXPENSE");
    expect(result.amount).toBe(120);
  });
});
```

**เรียนรู้:**

- Test-driven development (TDD)
- Mocking strategies
- Test organization
- Coverage analysis

---

### 8. DevOps & Deployment

#### **Docker & Containerization**

- Dockerfile optimization
- Multi-stage builds
- Docker Compose orchestration
- Environment management
- Container networking

```dockerfile
# ตัวอย่าง: Multi-stage build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
```

**เรียนรู้:**

- Container best practices
- Build optimization
- Production deployment
- Environment isolation

---

### 9. Logging & Monitoring

#### **Winston Logger**

- Structured logging
- Log levels management
- JSON formatting
- Production logging strategies

```typescript
logger.info("Expense saved", {
  userId: user.id,
  amount: 120,
  category: "อาหาร",
});
```

**เรียนรู้:**

- Observability principles
- Structured logging
- Log aggregation
- Error tracking

---

### 10. Code Quality & Maintenance

#### **Tools & Practices**

- **Prettier** - Code formatting
- **Husky** - Git hooks
- **Lint-staged** - Pre-commit validation
- **TypeScript** - Type safety
- **ESLint** - Code linting

**เรียนรู้:**

- Code style consistency
- Pre-commit workflows
- Team collaboration
- Maintainable codebase

---

## 🛠️ Technology Stack Summary

### Core Technologies

| Category  | Technology     | Purpose               |
| --------- | -------------- | --------------------- |
| Runtime   | Node.js 18+    | JavaScript runtime    |
| Language  | TypeScript 5.x | Type-safe development |
| Framework | Express.js 5.x | Web framework         |
| Database  | PostgreSQL 14+ | Relational database   |
| ORM       | Prisma 7.x     | Database toolkit      |

### AI & APIs

| Service     | Technology         | Purpose            |
| ----------- | ------------------ | ------------------ |
| AI Provider | Google Gemini API  | Text parsing & OCR |
| Messaging   | LINE Messaging API | Chat interface     |

### Security & Quality

| Tool               | Purpose           |
| ------------------ | ----------------- |
| Helmet.js          | Security headers  |
| Express Rate Limit | DDoS protection   |
| Zod                | Schema validation |
| Jest               | Testing framework |
| Winston            | Logging           |

### DevOps

| Tool           | Purpose                       |
| -------------- | ----------------------------- |
| Docker         | Containerization              |
| Docker Compose | Multi-container orchestration |
| Husky          | Git hooks                     |
| Prettier       | Code formatting               |

---

## 📚 Learning Resources

### Recommended Study Path

#### Level 1: Foundations

1. **TypeScript Basics**
   - Type system, interfaces, generics
   - Type-safe async/await
2. **Express.js Fundamentals**
   - Routing, middleware, error handling
   - Request/response lifecycle

3. **Database Design**
   - SQL basics
   - Relational modeling
   - Prisma schema

#### Level 2: Intermediate

1. **Design Patterns**
   - Factory, Repository, Singleton
   - Middleware chain pattern
2. **Security**
   - OWASP Top 10
   - Authentication/Authorization
   - Rate limiting

3. **Testing**
   - Unit vs Integration tests
   - Mocking strategies
   - Coverage goals

#### Level 3: Advanced

1. **Architecture**
   - Clean architecture
   - Separation of concerns
   - Scalability patterns

2. **AI Integration**
   - LLM prompt engineering
   - Multi-provider abstraction
   - Fallback strategies

3. **Production**
   - Docker deployment
   - Logging & monitoring
   - Graceful shutdown

---

## 🎯 Key Takeaways

### What Makes This Project Special?

✅ **Production-Ready Code**

- Security layers
- Error handling
- Graceful shutdown
- Structured logging

✅ **Clean Architecture**

- Separation of concerns
- Design patterns
- Type safety
- Testability

✅ **Modern Stack**

- TypeScript
- Prisma ORM
- Docker
- AI integration

✅ **Real-World Application**

- Webhook handling
- Third-party APIs
- Database operations
- Message formatting

---

## 💡 Skills Transferable to Other Projects

1. **Backend Development** → Any Node.js API project
2. **Database Design** → E-commerce, CMS, SaaS applications
3. **AI Integration** → Chatbots, Content generation, Data analysis
4. **Security Practices** → All web applications
5. **Testing** → Any software project
6. **Docker** → Microservices, Cloud deployment
7. **Design Patterns** → Large-scale applications

---

## 🚀 Next Steps for Learning

1. **Extend the Project**
   - Add budget tracking
   - Create analytics dashboard
   - Implement data export

2. **Try Different Technologies**
   - Swap Google AI → OpenAI/Anthropic
   - Add Redis caching
   - Implement GraphQL

3. **Deploy to Production**
   - Deploy to cloud (AWS, GCP, Azure)
   - Set up CI/CD pipeline
   - Monitor with APM tools

4. **Contribute to Docs**
   - Write tutorials
   - Create video guides
   - Share learnings

---

**Built with ❤️ for learning and growth**

📖 See also: [Architecture](../../docs/ARCHITECTURE.md) | [Testing Guide](../../docs/TESTING_GUIDE.md) | [Workshop](../../docs/WORKSHOP.md)
