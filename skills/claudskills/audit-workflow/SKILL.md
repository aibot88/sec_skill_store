---
name: audit-workflow
description: Workflow полного health check проекта. Architecture → Security → Quality → Report → (Fix). Use before major release or onboarding.
---

# Audit Workflow

Полный health check проекта.

## Последовательность

1. **Senior-Reviewer** — архитектура (SOLID, Clean Architecture, зависимости)
2. **Security-Auditor** — безопасность (Firebase rules, auth, секреты)
3. **Reviewer** — качество кода (DRY, сложность, долг)
4. **Documenter** — consolidated report + health score (0–10)
5. (опционально) — автофикс критичных issues после подтверждения

## Когда использовать

- Перед мажорным релизом
- При онбординге в новый кодбейс
- Периодический health check

## Связь с командами

Используется в `/audit`.
