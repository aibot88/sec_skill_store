---
name: "github-pr-reviewer"
description: "Pre-merge functional reviewer skill. Invoke for GitHub PR quality, contract validation, and release readiness. Do not invoke for deep security audit of auth/secrets/permissions."
---

# GitHub PR Reviewer

## Scope
- Проверка PR по стандарту GitHub: корректность, риски регрессий, готовность к merge.
- Упор на контракты CLI, совместимость JSON/JSONL и тестовое покрытие.

## Когда вызывать
- Перед merge любого нетривиального PR.
- После крупного рефакторинга CLI или parser-слоя.
- При подготовке релизного кандидата.

## Когда не вызывать
- Нужно проверить токены, права API и model auth-поверхность.
- Нужен baseline security hardening без PR-контекста.
- Нужна реализация доменной фичи вместо review.

## Review Protocol
1) Validate scope: понять изменённые модули и user-facing контракты.
2) Check risks: breaking changes, edge-cases, backward compatibility.
3) Check quality gates: unittest, ruff, mypy, coverage.
4) Check docs/runbook: есть ли обновления и rollback path.
5) Produce verdict: approve / request changes / follow-up tasks.

## Mandatory Checks
- CLI contract не сломан:
  - `--json` остаётся JSONL.
  - `--json --json-strict` оставляет только JSONL в `stdout`.
- Тесты добавлены по месту изменения.
- Нет секретов, нет зависимости от `vault/` и локальных приватных путей.
- Изменения воспроизводимы командами проверки.

## Output Format
- Summary: что проверено и что блокирует merge.
- Findings: critical / major / minor.
- Required fixes: список must-fix перед merge.
- Optional follow-ups: что можно перенести в отдельные задачи.
