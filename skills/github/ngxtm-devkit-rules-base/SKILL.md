# Auto-Skill Detection

> Automatically detect and suggest relevant skills based on user's task

## When to Activate

Before starting ANY coding task, check if a relevant skill exists:

1. **Analyze** the user's request — extract key technologies, patterns, or domains
2. **Search** `skills-compact.json` for matching skill names/descriptions
3. **Suggest** top 1-3 matching skills with name and category
4. **Load** on user confirmation — read full skill from `skills/{name}/SKILL.md`

## Skill Categories

| Code | Category | Examples |
|------|----------|----------|
| `fe` | Frontend | react, vue, nextjs, tailwind, ui/ux |
| `be` | Backend | node, express, nestjs, fastapi, api |
| `db` | Database | postgres, mysql, mongodb, redis, prisma |
| `ai` | AI/ML | llm, agents, rag, mcp, embeddings |
| `ops` | DevOps | docker, k8s, ci/cd, aws, terraform |
| `test` | Testing | jest, playwright, tdd, e2e |
| `sec` | Security | auth, oauth, jwt, owasp, pentest |
| `git` | Git/Workflow | pr, review, commit, branching |
| `mob` | Mobile | react-native, flutter, ios, android |
| `py` | Python | django, flask, fastapi, pandas |
| `go` | Golang | gin, echo, fiber, concurrency |

## How to Search

1. Read `skills-compact.json` — format: `{ "skills": { "name": { "c": "category", "d": "description" } } }`
2. Match skills whose name or description contains user's keywords
3. If no direct match, suggest skills from the matching category
4. On confirmation, read `skills/{skill-name}/SKILL.md`

## Auto-Activate Triggers

| User says... | Suggest skill |
|--------------|---------------|
| "create PR", "pull request" | /git-advanced-workflows |
| "code review" | /code-review |
| "write tests", "add tests" | /test-master |
| "fix bug", "debug" | /systematic-debugging |
| "learn", "teach me" | /learn |
| "react component" | /react-expert |
| "nextjs", "next.js" | /nextjs-best-practices |
| "docker", "container" | /docker-expert |
| "api design" | /api-design-principles |
| "database schema" | /database-design |
| "authentication", "auth" | /auth-implementation-patterns |
| "mcp server" | /mcp-developer |

## Rules

1. **Don't auto-load** — always ask before loading a skill
2. **Max 3 suggestions** — don't overwhelm user
3. **Be concise** — one-line per skill suggestion
4. **Remember context** — if user said "none", don't suggest again for same task
5. **On-demand only** — only read full SKILL.md when user confirms
