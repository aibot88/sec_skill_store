---
name: claude-code-admin
description: "Администрирование Claude Code: OpenTelemetry мониторинг, безопасность, IAM (аутентификация, разрешения, managed settings), управление затратами, аналитика. Триггеры: 'monitoring claude', 'мониторинг claude', 'opentelemetry claude', 'otel', 'security claude', 'безопасность claude', 'IAM', 'access control claude', 'costs claude', 'затраты claude', 'rate limit', 'managed settings', 'enterprise claude', 'analytics claude', 'аналитика claude', 'permission architecture', 'credential management'. НЕ для мониторинга фреймворка — используй deployment."
---

# Администрирование Claude Code

## Мониторинг (OpenTelemetry)

### Быстрая настройка

```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

### Все env переменные мониторинга

| Переменная | Описание | Default |
|-----------|----------|---------|
| `CLAUDE_CODE_ENABLE_TELEMETRY=1` | Включить | Off |
| `OTEL_METRICS_EXPORTER` | `otlp\|prometheus\|console` | — |
| `OTEL_LOGS_EXPORTER` | `otlp\|console` | — |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `grpc\|http/json\|http/protobuf` | — |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | URL коллектора | — |
| `OTEL_EXPORTER_OTLP_HEADERS` | `Authorization=Bearer token` | — |
| `OTEL_METRIC_EXPORT_INTERVAL` | Интервал ms | 60000 |
| `OTEL_LOGS_EXPORT_INTERVAL` | Интервал ms | 5000 |
| `OTEL_LOG_USER_PROMPTS=1` | Логировать промпты | Off |
| `OTEL_RESOURCE_ATTRIBUTES` | `department=eng,team.id=X` | — |

### Метрики

| Метрика | Unit | Описание |
|---------|------|----------|
| `claude_code.session.count` | count | Сессии |
| `claude_code.lines_of_code.count` | count | Строки (added/removed) |
| `claude_code.cost.usage` | USD | Стоимость по модели |
| `claude_code.token.usage` | tokens | Токены (input/output/cache) |
| `claude_code.commit.count` | count | Коммиты |
| `claude_code.pull_request.count` | count | Pull requests |
| `claude_code.code_edit_tool.decision` | count | Accept/reject edits |
| `claude_code.active_time.total` | seconds | Активное время |

### События (Events)

| Событие | Описание |
|---------|----------|
| `claude_code.user_prompt` | Промпт пользователя (скрыт по умолчанию) |
| `claude_code.tool_result` | Результат инструмента (success, duration, error) |
| `claude_code.api_request` | API вызов (model, cost, tokens) |
| `claude_code.api_error` | Ошибка API (status_code, attempt) |
| `claude_code.tool_decision` | Решение по разрешению (tool, decision, source) |

## Безопасность

### Модель разрешений

- **Read-only по умолчанию** — мутации требуют одобрения
- Bash команды → одобрение каждый раз
- File edits → одобрение (можно на сессию)
- Запись только в рабочей директории и поддиректориях

### Встроенная защита

| Механизм | Описание |
|----------|----------|
| Command injection detection | Подозрительный bash → manual approval |
| Prompt injection mitigation | Контекстный анализ, санитизация |
| Network request approval | Сетевые запросы требуют одобрения |
| Error-on-mismatch | Неизвестные команды → manual approval |
| Credential encryption | macOS Keychain шифрование |
| Trust checks | Проверка при первом запуске в новом репо |

### Sandbox

```bash
/sandbox                # Включить изоляцию файловой системы и сети
```

## IAM (Идентификация и доступ)

### Методы аутентификации

| Метод | Описание |
|-------|----------|
| Claude for Teams/Enterprise | SSO, domain capture, RBAC |
| Claude Console | API key, командный биллинг |
| AWS Bedrock | OIDC аутентификация |
| Google Vertex AI | Workload Identity Federation |

### Режимы разрешений (defaultMode)

| Режим | Поведение |
|-------|-----------|
| `default` | Запрос при первом использовании каждого инструмента |
| `acceptEdits` | Авто-одобрение редактирования файлов |
| `plan` | Только чтение (без правок и команд) |
| `dontAsk` | Авто-отклонение (только pre-approved работают) |
| `bypassPermissions` | Пропустить всё (только для безопасных сред) |

### Managed Settings (корпоративные)

Файл `managed-settings.json` в системной директории.
Не может быть переопределён пользователем или проектом.

```json
{
  "permissions": {
    "defaultMode": "default",
    "deny": ["Bash(rm -rf:*)"]
  }
}
```

### Credential Helper

```json
{
  "apiKeyHelper": "./scripts/get-api-key.sh"
}
```

- Автообновление: каждые 5 мин или при HTTP 401
- TTL: `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` (default: 300000)

## Управление затратами

### Отслеживание

```bash
/cost                  # Стоимость текущей сессии
/stats                 # Статистика использования
```

### Средние затраты

| Масштаб | Стоимость |
|---------|-----------|
| 1 разработчик | ~$6/день (средне), <$12/день (90%) |
| Команда | ~$100-200/разработчик/месяц (Sonnet) |

### Рекомендации Rate Limiting (на пользователя)

| Размер команды | TPM | RPM |
|---------------|-----|-----|
| 1-5 | 200k-300k | 5-7 |
| 5-20 | 100k-150k | 2.5-3.5 |
| 20-50 | 50k-75k | 1.25-1.75 |
| 50-100 | 25k-35k | 0.62-0.87 |
| 100-500 | 15k-20k | 0.37-0.47 |
| 500+ | 10k-15k | 0.25-0.35 |

### Оптимизация стоимости

1. **Конкретные промпты** — избегать broad scans
2. **Разбивать задачи** — фокусированные взаимодействия
3. **Очищать контекст** — `/clear` между задачами
4. **Auto-compact** — включён по умолчанию (95%)
5. **Compact hints** — в CLAUDE.md: `When using compact, focus on X`
6. **Лимиты** — `--max-turns`, `--max-budget-usd`

## Источники

- `docs/documentation/Claude Code Docs/4. Администрирование/Мониторинг.md`
- `docs/documentation/Claude Code Docs/4. Администрирование/Безопасность.md`
- `docs/documentation/Claude Code Docs/4. Администрирование/Управление идентификацией и доступом.md`
- `docs/documentation/Claude Code Docs/4. Администрирование/Эффективное управление затратами.md`
- `docs/documentation/Claude Code Docs/4. Администрирование/Аналитика.md`
