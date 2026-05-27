---
name: secret-guard
description: Use BEFORE writing API keys/tokens/passwords into code, BEFORE git commit/push, BEFORE creating PR. Blocks accidental leaks of secrets to GitHub. Triggers коммит, push, ключ, токен, secret, api key, .env, credentials, push to github, открой PR, открыть PR, git commit, git push.
allowed-tools: [Read, Edit, Bash, Grep]
model: sonnet
---

# Secret Guard — не отправляем секреты на GitHub

Зашита от классического provoцелого slip'а: API-ключ попадает в код → коммит → push → ключ публично виден в истории git навсегда (даже если потом удалить — он остаётся в reflog'е и в чужих клонах).

## Iron rule

**Никогда** не вписывай в исходный код:
- API-ключи, токены, пароли (даже «временно для теста»),
- секрет-ключи (private keys, JWT secrets, signing keys),
- DB connection strings с паролем,
- AWS access keys, GCP service account JSON,
- HuggingFace / W&B / OpenAI / Anthropic / GitHub tokens.

**Используй env vars** или secret-стор (gh secret, AWS Secrets Manager, dotenv с `.env` в `.gitignore`).

## Паттерны известных секретов (проверять `rg`/`grep` перед commit)

| Сервис | Префикс/regex |
|---|---|
| OpenAI (новый) | `sk-proj-[A-Za-z0-9_-]{20,}` |
| OpenAI (legacy) | `sk-[A-Za-z0-9]{48}` |
| Anthropic | `sk-ant-[A-Za-z0-9_-]{20,}` |
| HuggingFace | `hf_[A-Za-z0-9]{30,}` |
| GitHub PAT | `ghp_[A-Za-z0-9]{36}` |
| GitHub OAuth | `gho_[A-Za-z0-9]{36}` |
| GitHub user-to-server | `ghu_[A-Za-z0-9]{36}` |
| GitHub server-to-server | `ghs_[A-Za-z0-9]{36}` |
| GitHub refresh | `ghr_[A-Za-z0-9]{36}` |
| AWS access key | `AKIA[0-9A-Z]{16}` |
| AWS secret | контекст `aws_secret_access_key.*[A-Za-z0-9/+=]{40}` |
| Slack | `xox[abp]-\d+-\d+-\d+-[a-z0-9]{32}` |
| Google API | `AIza[0-9A-Za-z_-]{35}` |
| Stripe | `sk_live_[0-9a-zA-Z]{24}`, `pk_live_…` |
| W&B | 40-hex после `WANDB_API_KEY` |
| Private key PEM | `-----BEGIN (RSA |EC |OPENSSH |DSA |)?PRIVATE KEY-----` |

## Процедура

### A. Перед записью кода
1. Если пользователь даёт ключ в чат — **не сохраняй его в файл**. Предложи:
   ```bash
   export ANTHROPIC_API_KEY=...        # в shell
   echo "ANTHROPIC_API_KEY=..." >> .env  # в .env (он в .gitignore)
   ```
   В коде:
   ```python
   import os
   key = os.environ["ANTHROPIC_API_KEY"]
   ```
2. Никогда не пиши `key = "sk-..."` в исходник, даже как пример. Используй `key = "sk-PLACEHOLDER"` или `key = "<your-key-here>"`.

### B. Перед `git add` / `git commit`
1. Запустить:
   ```bash
   gitleaks detect --staged --no-banner --redact 2>&1 | head -50
   ```
   Если gitleaks не установлен — fallback regex-скан:
   ```bash
   git diff --cached | rg -nP '(sk-(proj|ant)-|sk-[A-Za-z0-9]{48}|hf_[A-Za-z0-9]{30,}|gh[psour]_[A-Za-z0-9]{36}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|-----BEGIN (RSA |EC |OPENSSH |DSA |)?PRIVATE KEY-----)' || echo "OK"
   ```
2. Если что-то нашлось — **STOP**. Не делать commit. Вернуться к шагу A.
3. Проверить что в diff нет:
   - `.env` (не должен быть закоммичен; если он в diff — добавить в `.gitignore` и `git rm --cached .env`),
   - `*.pem`, `*.key`, `id_rsa`, `id_ed25519`,
   - `credentials.json`, `service-account.json`,
   - hardcoded URL'ов вида `https://user:password@host/db`.

### C. Перед `git push`
1. Если в недавних коммитах `git log -p -5` есть секреты:
   ```bash
   # Если ещё не push'ил — переписать историю
   git reset --soft HEAD~N        # N коммитов назад
   # удалить секрет из файла
   git add . && git commit
   ```
2. Если **уже** push'ил — секрет публичен. Действия:
   - **Сразу отозвать ключ** в панели сервиса (это первое и главное!).
   - Удалить из истории: `git filter-repo --path <file> --invert-paths` (или BFG).
   - Уведомить владельца репо.

### D. Перед открытием PR
1. `gh pr diff` или `git diff main...HEAD` → ещё раз проверить.
2. Никогда не вкладывать .env / credentials.json в PR description / комментарии.

## Что считается «не-секрет»

- Placeholder'ы: `<your-api-key>`, `your_key_here`, `EXAMPLE_KEY`, `xxx`, `placeholder`, `***REDACTED***`.
- Тестовые fixture'ы вида `sk-test-1234567890abcdef` (короткие, явно неработающие).
- Public keys (`*.pub`, `-----BEGIN PUBLIC KEY-----`) — публичные по определению.
- API endpoint'ы без credentials: `https://api.example.com/v1/foo` — это не секрет.

## Связь с другими механизмами

В этом workspace **уже стоят 3 уровня защиты**:

1. **Hook `secret_guard.py`** (Claude Code) — перехватывает `git commit/push` и `Write/Edit` с секретами **до** того как Claude их применит. Возвращает `decision=block`.
2. **Pre-commit hook `gitleaks`** (`.pre-commit-config.yaml`) — git-уровень. Сканирует `git add`'нутые файлы.
3. **`.gitignore`** — `.env`, `*.key`, `*.pem`, `credentials.json` никогда не попадают в diff.

Этот skill — **четвёртый уровень**, инструкция Claude'у. Работает в связке с тремя остальными, но по принципу defense in depth: даже если один уровень обойдён, остальные продолжают работать.

## Hard rules

- Никогда не предлагай пользователю «временно вставить ключ в код».
- Если пользователь сам это пишет — остановить и предложить env var.
- Никогда не делать `git push --force` чтобы «спрятать» закоммиченный секрет на удалённом репо: ключ уже в reflog'е и в кешах сервера. Только revocation помогает.
- Никогда не создавать новые `.env.example` с реальными значениями — только с placeholder'ами.
