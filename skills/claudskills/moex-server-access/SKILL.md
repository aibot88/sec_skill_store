---
name: moex-server-access
description: Безопасная работа с production-сервером Фрейм (таймфрейм.рф) через SSH — деплой файлов, выполнение команд в контейнерах, чтение логов, БД-запросы. Соблюдает rate-limit и fail2ban защиту через single-connection patterns. Триггер когда пользователь говорит «задеплой на сервер», «посмотри логи прода», «выполни SQL на проде», «обнови файл в контейнере», «restart api», «check production», «прод не работает», или просит любое действие требующее SSH к 103.88.243.232.
---

# MOEX Server Access

Шаблон работы с сервером Фрейм для AI-помощников. Сервер защищён жёстким SSH rate-limit и fail2ban — нарушение правил приводит к 24-часовому бану IP.

## ⚠️ КРИТИЧЕСКИЕ ПРАВИЛА (не нарушать!)

### Правило 1: ВСЕГДА используй полный SSH preamble

```bash
ssh -o IdentitiesOnly=yes -o IdentityAgent=none -o ConnectTimeout=20 \
    -i <ПУТЬ_К_КЛЮЧУ> alexgondon@103.88.243.232 "..."
```

**Почему `IdentitiesOnly=yes`**: SSH-агент по умолчанию предлагает все ключи подряд. Каждый ключ = 1 auth attempt. С 3+ ключами в агенте → fail2ban ban на 24 часа после первой команды (из-за `Too many authentication failures`).

### Правило 2: НЕ probe'и сервер

❌ **Плохо**:
```bash
ssh ... "echo ok"          # 1 connection потрачен впустую
ssh ... "hostname"          # ещё одна
ssh ... "<реальная команда>"  # третья — попадает под rate-limit
```

✅ **Хорошо** — для проверки доступности используй HTTPS (порт 443 не рейт-лимитнут):
```bash
curl -sk -o /dev/null -w "%{http_code}\n" "https://103.88.243.232/" \
  -H "Host: xn--80aklbnczmv.xn--p1ai" --max-time 8
# 200 → сервер работает
```

### Правило 3: ОДНА SSH connection на одну операцию

iptables режет если **5+ NEW SSH connections с одного IP за 60 секунд** → DROP пакетов 60 секунд → таймауты.

❌ **Плохо** — 3 отдельные SSH (часто = 3 connection):
```bash
ssh ... "mkdir /tmp/x"
scp file ... :/tmp/x/
ssh ... "docker cp /tmp/x/file container:/path/ && docker restart"
```

✅ **Хорошо** — всё в одном tar-pipe:
```bash
tar -cz file | ssh ... \
  "rm -rf /tmp/x && mkdir /tmp/x && tar -xz -C /tmp/x \
   && docker cp /tmp/x/file container:/path/ \
   && docker restart container && rm -rf /tmp/x"
```

### Правило 4: НЕ retry'ь после `Connection timed out`

Если получил `Connection timed out` — твой IP попал под rate-limit (60s drop) или fail2ban (24h ban). **Повторная попытка в течение минуты обнулит счётчик** и продлит drop ещё на 60s.

**Что делать**:
1. Подожди минуту (`sleep 60` или используй scheduled wakeup)
2. Если timeout повторился — проверь port 22 через `nc -z -w 5 103.88.243.232 22`
3. Если `BLOCKED` — fail2ban забанил, **скажи пользователю** и не retry'ь без unban через VNC

### Правило 5: Для частых операций — HTTP API, не SSH

Если задача "получить данные с прода" — используй HTTPS API на 443 (без лимитов). SSH только когда реально нужен прямой доступ к контейнеру/БД/файлам.

---

## 🔑 SSH Setup (одноразовая настройка)

Получи приватный ключ от администратора (Vadim) — по умолчанию это `~/.ssh/id_ed25519`. Публичный ключ должен быть зарегистрирован в `/home/alexgondon/.ssh/authorized_keys` на сервере.

Проверка работоспособности через **HTTPS** (НЕ SSH):
```bash
curl -sk "https://таймфрейм.рф/health" --max-time 8
# {"status":"ok","database":"ok"} → сервер живой
```

**Сохрани alias** в `~/.bashrc` или `~/.zshrc` чтобы не печатать длинный preamble:
```bash
alias frame-ssh='ssh -o IdentitiesOnly=yes -o IdentityAgent=none -o ConnectTimeout=20 -i ~/.ssh/id_ed25519 alexgondon@103.88.243.232'
```

---

## 📦 Типичные операции (с готовыми шаблонами)

### Operation 1: Скопировать файл в контейнер + рестарт сервиса

Используй для замены одного backend-файла (Python router, config):

```bash
tar -cz <LOCAL_PATH>/myfile.py | \
  ssh -o IdentitiesOnly=yes -o IdentityAgent=none -o ConnectTimeout=30 \
      -i ~/.ssh/id_ed25519 alexgondon@103.88.243.232 \
  "rm -rf /tmp/dep && mkdir -p /tmp/dep && tar -xz -C /tmp/dep && \
   sudo docker cp /tmp/dep/myfile.py frame-api-1:/app/api/routers/myfile.py && \
   sudo docker restart frame-api-1 && \
   rm -rf /tmp/dep && \
   sleep 6 && \
   sudo docker exec frame-api-1 python3 -c 'import urllib.request; print(urllib.request.urlopen(\"http://localhost:8000/health\").read().decode())'"
```

**Что делает**:
1. Локально tar'ит файл
2. Передаёт через SSH stdin
3. Распаковывает в `/tmp/dep`
4. Копирует в контейнер
5. Рестартит контейнер
6. Чистит `/tmp`
7. Ждёт 6 секунд (FastAPI startup)
8. Проверяет /health

Всё в **одной SSH connection** — не попадает под rate-limit.

### Operation 2: Деплой множества файлов (batch)

Для нескольких файлов одной командой:

```bash
tar -cz \
    api/main.py \
    api/routers/file1.py \
    api/routers/file2.py | \
  ssh -o IdentitiesOnly=yes -o IdentityAgent=none -i ~/.ssh/id_ed25519 \
      alexgondon@103.88.243.232 \
  "rm -rf /tmp/dep && mkdir -p /tmp/dep && tar -xz -C /tmp/dep && \
   sudo docker cp /tmp/dep/api/main.py frame-api-1:/app/api/main.py && \
   sudo docker cp /tmp/dep/api/routers/file1.py frame-api-1:/app/api/routers/file1.py && \
   sudo docker cp /tmp/dep/api/routers/file2.py frame-api-1:/app/api/routers/file2.py && \
   sudo docker restart frame-api-1 && \
   rm -rf /tmp/dep && \
   sleep 6 && \
   sudo docker exec frame-api-1 python3 -c 'import urllib.request; print(urllib.request.urlopen(\"http://localhost:8000/health\").read().decode())'"
```

### Operation 3: Деплой frontend dist (vite build)

```bash
tar -cz -C frontend/dist . | \
  ssh -o IdentitiesOnly=yes -o IdentityAgent=none -i ~/.ssh/id_ed25519 \
      alexgondon@103.88.243.232 \
  "rm -rf /tmp/dist && mkdir -p /tmp/dist && tar -xz -C /tmp/dist && \
   sudo docker cp /tmp/dist/. frame-api-1:/app/frontend/dist/ && \
   rm -rf /tmp/dist && \
   curl -sk 'https://localhost/sw.js' -H 'Host: xn--80aklbnczmv.xn--p1ai' | grep CACHE_NAME | head -1"
```

**Заметь**: frontend dist не требует restart — статика подхватывается на лету.

### Operation 4: Выполнить SQL на production БД

```bash
ssh -o IdentitiesOnly=yes -o IdentityAgent=none -i ~/.ssh/id_ed25519 \
    alexgondon@103.88.243.232 \
  'sudo docker exec frame-db-1 psql -U postgres -d moex_db -c "SELECT COUNT(*) FROM users"'
```

Для длинных multi-line SQL — через stdin:

```bash
cat <<'SQL' | ssh -o IdentitiesOnly=yes -o IdentityAgent=none -i ~/.ssh/id_ed25519 \
    alexgondon@103.88.243.232 'sudo docker exec -i frame-db-1 psql -U postgres -d moex_db'
SELECT u.email, COUNT(ae.event_id) AS events
FROM users u
LEFT JOIN analytics_events ae ON ae.user_id = u.id
WHERE ae.server_ts >= NOW() - INTERVAL '7 days'
GROUP BY u.email
ORDER BY events DESC LIMIT 10;
SQL
```

### Operation 5: Применить SQL миграцию

```bash
cat /path/to/migration.sql | \
  ssh -o IdentitiesOnly=yes -o IdentityAgent=none -i ~/.ssh/id_ed25519 \
      alexgondon@103.88.243.232 \
  'sudo docker exec -i frame-db-1 psql -U postgres -d moex_db'
```

### Operation 6: Посмотреть логи контейнера

```bash
ssh -o IdentitiesOnly=yes -o IdentityAgent=none -i ~/.ssh/id_ed25519 \
    alexgondon@103.88.243.232 \
  "sudo docker logs frame-api-1 --tail 50 --since 10m 2>&1 | grep -iE 'error|exception|warning' | tail -20"
```

### Operation 7: Установить пакет в контейнер (ephemeral)

⚠️ Это временно — после `docker compose down/up` пакет пропадёт. Для постоянного решения нужно править `requirements.txt` и rebuild image.

```bash
ssh -o IdentitiesOnly=yes -o IdentityAgent=none -i ~/.ssh/id_ed25519 \
    alexgondon@103.88.243.232 \
  "sudo docker exec frame-api-1 pip install --no-cache-dir somepackage && \
   sudo docker restart frame-api-1"
```

### Operation 8: Запустить ad-hoc Python script на проде

Создай файл локально, скопируй и выполни:

```bash
tar -cz /path/to/script.py | \
  ssh -o IdentitiesOnly=yes -o IdentityAgent=none -i ~/.ssh/id_ed25519 \
      alexgondon@103.88.243.232 \
  "rm -rf /tmp/sc && mkdir -p /tmp/sc && tar -xz -C /tmp/sc && \
   sudo docker cp /tmp/sc/path/to/script.py frame-api-1:/tmp/script.py && \
   sudo docker exec frame-api-1 python3 /tmp/script.py && \
   rm -rf /tmp/sc"
```

### Operation 9: Health check после deploy

```bash
ssh -o IdentitiesOnly=yes -o IdentityAgent=none -i ~/.ssh/id_ed25519 \
    alexgondon@103.88.243.232 \
  "echo '--- containers ---' && sudo docker ps --format '{{.Names}} {{.Status}}' | grep frame && \
   echo '--- /health ---' && \
   sudo docker exec frame-api-1 python3 -c 'import urllib.request; print(urllib.request.urlopen(\"http://localhost:8000/health\").read().decode())' && \
   echo '--- SW + index hash ---' && \
   curl -sk 'https://localhost/sw.js' -H 'Host: xn--80aklbnczmv.xn--p1ai' | grep CACHE_NAME | head -1 && \
   curl -sk 'https://localhost/' -H 'Host: xn--80aklbnczmv.xn--p1ai' | grep -oE 'index-[A-Za-z0-9_-]+\\.js' | head -1"
```

---

## 🐛 Troubleshooting

### Симптом: `Permission denied (publickey)`
**Причина**: ключ не зарегистрирован на сервере, или используется не тот.
**Решение**: проверь путь после `-i` и попроси администратора добавить твой публичный ключ в `/home/alexgondon/.ssh/authorized_keys`.

### Симптом: `Too many authentication failures`
**Причина**: SSH агент перебирает все ключи подряд. После 3+ неудачных попыток сервер отключает.
**Решение**: добавь `-o IdentitiesOnly=yes -o IdentityAgent=none` в команду. **ВНИМАНИЕ**: после нескольких подряд таких ошибок IP попадёт в fail2ban на 24 часа.

### Симптом: `Connection timed out` (sshd порт 22)
**Причина А**: rate-limit (5+ NEW connections / 60s) → packet drop на 60 секунд.
**Решение А**: подожди ровно 60 секунд, **не делай retry в loop'e** — это продлит drop.

**Причина Б**: fail2ban забанил IP на 24 часа (после 3+ failed auth).
**Диагностика**: `nc -z -w 5 103.88.243.232 22 && echo OPEN || echo BLOCKED`. Если BLOCKED уже 5+ минут — это fail2ban.
**Решение Б**: попроси администратора (Vadim) разбанить через VNC console TimeWeb:
```bash
fail2ban-client set sshd unbanip <ВАШ_IP>
```

### Симптом: HTTPS работает (https://таймфрейм.рф/), но SSH нет
**Причина**: точно fail2ban (HTTPS на 443, SSH на 22).
**Решение**: см. выше — VNC unban.

### Симптом: команда возвращает SPA HTML вместо JSON
**Причина**: endpoint не существует или nginx fallback.
**Решение**: проверь URL, должен быть `/api/...` (не `/something/api`). Если 404 — endpoint удалили / переименовали.

### Симптом: `permission denied while trying to connect to the Docker daemon socket`
**Причина**: ходишь как user без прав на docker (alexgondon → нужен `sudo`).
**Решение**: префиксуй все docker-команды через `sudo`: `sudo docker exec ...`, `sudo docker cp ...`. В шаблонах выше уже учтено.

---

## 🗺️ Project structure (что где)

### Сервер
- **IP**: `103.88.243.232`
- **Домен**: `xn--80aklbnczmv.xn--p1ai` (punycode для `таймфрейм.рф`)
- **User**: `alexgondon` (UID 1000, в группах sudo+docker, NOPASSWD)

### Контейнеры
- `frame-api-1` — FastAPI (Python 3.11), путь `/app/`
- `frame-db-1` — PostgreSQL 16, db: `moex_db`, user: `postgres`
- `frame-redis-1` — Redis для cache + SSE
- `frame-orchestrator-1` — main_orchestrator.py — cron-like джобы
- `frame-nginx-1` — reverse proxy (HTTPS termination)
- `frame-tg-bot-1` — Telegram bot (если был)

### Структура `/app/` в frame-api-1
- `/app/api/` — FastAPI код (main.py, routers/)
- `/app/frontend/dist/` — собранный фронтенд (статика, SW, index.html)
- `/app/Commodity/`, `/app/Funds/`, `/app/OI/`, `/app/Macro/`, `/app/Candles/` — fetch-скрипты
- `/app/main_orchestrator.py` — оркестратор

### Главные таблицы БД
- `users` (id, email, role, ...) — пользователи
- `analytics_events` — лог событий пользователей
- `candles` (secid, interval, begin_time, ohlc) — свечи акций/фьючерсов
- `index_data` (secid, trade_date, close, ...) — индексы + commodity
- `instruments` — каталог тикеров
- `funds` + `fund_data` — паевые фонды + СЧА
- `mv_heatmap_stocks` (materialized view) — карта рынка

### Endpoints на 443 (HTTPS — без rate-limit)
- `GET /health` — общая проверка
- `GET /api/instruments` — список инструментов
- `GET /api/heatmap/stocks` — карта рынка
- `GET /api/seasonality/yearly?secid=X` — годовая сезонность
- `GET /api/openapi.json` — OpenAPI схема (полный список endpoints)

---

## 🔐 Что НЕ делать на проде

- ❌ Не запускай `npm run build` на сервере — 4GB RAM, OOM
- ❌ Не делай `docker compose down` без согласования — это reset state контейнеров (потерянные ephemeral pip installs, например)
- ❌ Не редактируй файлы в контейнерах напрямую через `docker exec ... vim` — git перестанет быть source of truth
- ❌ Не запускай `git push --force` к main без согласования
- ❌ Не пиши credentials (.env, БД-пароли) в commit messages или логи

---

## 📖 Reference: одна команда — один источник правды

**Если ты AI-помощник** — этот блок твоё священное правило:

```bash
# ШАБЛОН ОПЕРАЦИИ С ПРОДОМ (template)
tar -cz <ЛОКАЛЬНЫЕ_ФАЙЛЫ> | \
  ssh -o IdentitiesOnly=yes -o IdentityAgent=none -o ConnectTimeout=30 \
      -i ~/.ssh/id_ed25519 alexgondon@103.88.243.232 \
  "rm -rf /tmp/op && mkdir -p /tmp/op && tar -xz -C /tmp/op && \
   <ОПЕРАЦИИ> && \
   rm -rf /tmp/op && \
   <ВЕРИФИКАЦИЯ>"
```

**Принципы**:
1. ВСЕГДА `IdentitiesOnly=yes` + `IdentityAgent=none` + `-i <KEY>`
2. ОДНА SSH connection на операцию — все шаги через `&&`
3. Cleanup `/tmp/op` в конце
4. Verification ВНУТРИ той же connection (не отдельным `ssh`)
5. При ошибке — НЕ retry, спроси пользователя
