---
name: checklist-release
description: |
  Pre-release verification checklist. 7 phases: code, docs, infra, security, 
  monitoring, deployment, post-deploy. Go/No-Go decision criteria. Severity 
  classification (🔴🟠🟡🟢). Required before every production release.
---

# 🚀 Release Checklist — Предрелизный Чеклист

<purpose>
Финальные проверки перед релизом. Убедись, что ничего не упущено.
</purpose>

---

## Когда Использовать

- Перед каждым релизом в production
- Перед major/minor версиями
- После значительных изменений
- При первом деплое нового сервиса

---

## 📋 Фаза 1: Готовность Кода

### Code Complete

- [ ] Все запланированные фичи реализованы
- [ ] Все @reviewed изменения получили PASS
- [ ] Нет открытых блокирующих багов
- [ ] Feature flags настроены правильно

### Quality Gates

- [ ] Все тесты проходят (unit, integration, e2e)
- [ ] Test coverage на приемлемом уровне
- [ ] Linter/static analysis чистые
- [ ] Build успешен

### Code Review

- [ ] Все изменения прошли code review
- [ ] Критические изменения review двумя reviewers
- [ ] Security review для security-critical изменений

---

## 📋 Фаза 2: Документация

### Technical Documentation

- [ ] `/docs/Architecture.md` актуален
- [ ] API документация обновлена
- [ ] README обновлён (если нужно)
- [ ] CHANGELOG обновлён

### User-Facing (если применимо)

- [ ] Release notes подготовлены
- [ ] User documentation обновлена
- [ ] Migration guide (если breaking changes)

### Internal

- [ ] Runbook / playbook обновлён
- [ ] Monitoring dashboard готов
- [ ] Известные issues задокументированы

---

## 📋 Фаза 3: Инфраструктура

### Environment

- [ ] Staging протестирован и соответствует production
- [ ] Конфигурация production готова
- [ ] Environment variables установлены
- [ ] Secrets доступны и актуальны

### Dependencies

- [ ] Все dependencies зафиксированы (lockfile)
- [ ] Dependencies проверены на уязвимости
- [ ] Нет deprecated packages

### Database

- [ ] Миграции протестированы
- [ ] Rollback миграций работает
- [ ] Backup перед деплоем запланирован
- [ ] Индексы оптимизированы для нового кода

---

## 📋 Фаза 4: Безопасность

### Security Review

- [ ] `checklists/security.md` пройден для критических изменений
- [ ] Нет новых уязвимостей (CVE scan)
- [ ] Permissions/RBAC корректны
- [ ] Audit logging работает

### Secrets

- [ ] Никаких secrets в коде
- [ ] Secrets ротация не нужна / выполнена
- [ ] Доступ к production secrets ограничен

---

## 📋 Фаза 5: Мониторинг и Alerting

### Monitoring

- [ ] Метрики приложения настроены
- [ ] Health checks работают
- [ ] Logging настроен и работает
- [ ] Traces / APM настроены (если есть)

### Alerting

- [ ] Алерты на критические ошибки настроены
- [ ] Алерты на SLA нарушения (latency, errors)
- [ ] Escalation path определён
- [ ] On-call schedule актуален

---

## 📋 Фаза 6: Deployment Plan

### Strategy

- [ ] Deployment strategy выбрана (blue-green, canary, rolling)
- [ ] Canary % определён (если применимо)
- [ ] Время деплоя согласовано

### Rollback

- [ ] Rollback plan готов
- [ ] Rollback протестирован (dry-run)
- [ ] Критерии для rollback определены
- [ ] Ответственный за rollback назначен

### Communication

- [ ] Stakeholders уведомлены
- [ ] Downtime window согласован (если нужен)
- [ ] Status page готов к обновлению

---

## 📋 Фаза 7: Post-Deploy

### Verification

- [ ] Smoke tests проходят в production
- [ ] Ключевые user flows работают
- [ ] Метрики в норме (error rate, latency)
- [ ] Нет аномалий в логах

### Monitoring Period

- [ ] Усиленный мониторинг на X часов
- [ ] Команда доступна для быстрого реагирования

### Completion

- [ ] Релиз отмечен (git tag, release notes)
- [ ] Stakeholders уведомлены о завершении
- [ ] Post-mortem запланирован (если были проблемы)

---

## Go/No-Go Checklist

**Критерии GO:**

| Критерий | Status |
|----------|--------|
| Все тесты проходят | ⬜ |
| Code review PASS | ⬜ |
| Security review PASS | ⬜ |
| Staging validation OK | ⬜ |
| Rollback plan готов | ⬜ |
| Monitoring настроен | ⬜ |
| Team available for support | ⬜ |

**Любой ⬜ = NO-GO**

---

## Severity Levels

| Level | Критерий | Действие |
|-------|----------|----------|
| 🔴 Blocker | Security, data loss, core功能 broken | NO-GO до исправления |
| 🟠 Critical | Major功能 broken, significant regression | NO-GO для major release |
| 🟡 Major | Minor功能 broken, acceptable workaround | GO с известными issues |
| 🟢 Minor | Cosmetic, edge cases | GO |

---

## Quick Reference

```
Release Readiness:

✅ Code      — tests, review, build
✅ Docs      — changelog, api docs
✅ Infra     — env, deps, db
✅ Security  — audit, secrets
✅ Monitoring — alerts, dashboards
✅ Deploy    — strategy, rollback
✅ Post      — verify, monitor

Red Flags:
❌ Failing tests
❌ Missing reviews
❌ No rollback plan
❌ Untested migrations
❌ Missing monitoring
```

---

**Связанные файлы:**

- `checklists/security.md` — детальный security checklist
- `checklists/code-review.md` — code review checklist
- `workflows/feature.md` — feature development workflow

---

**END OF CHECKLIST**
