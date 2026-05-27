# Coding Standards & Architecture

## Architecture Rules
- Use Repository pattern for database access.
- Use Service layer for business logic.
- Keep FastAPI endpoints slim and focused.
- All database operations must be async.

## LangChain Best Practices
- Use Structured Tools for predictable output.
- Implement memory support for contextual chat.
- Always validate tool inputs with Pydantic.

## Supabase Integration
- Never execute raw SQL from the AI.
- Use the official Supabase client library.
- Enforce RLS policies on all tables.

## Security & Validation
- Sanitize all user inputs before processing.
- Log all tool calls and errors.
- Require confirmation for destructive operations.

## Naming Conventions
- Use snake_case for Python functions/variables.
- Use PascalCase for React components.
- Use camelCase for TypeScript variables.
