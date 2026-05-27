---
name: sdd-idea
description: >
  Planning-only skill for SDD projects. SDD builds **web apps** on
  Django + htmx + SQLite + Pico.css in Docker — one stack, the only
  one. Turns a rough idea into PROJECT.md (spec + phased plan) plus a
  project-local tech-stack.md recipe. **Only runs when the
  user explicitly invokes `/sdd-idea`** (with or without accompanying
  text, e.g. `/sdd-idea` or `/sdd-idea хочу сделать трекер книг`). Do
  NOT auto-invoke on natural-language hints like "I have an idea",
  "let's plan an app", "new project", "хочу сделать приложение",
  "давай спроектируем", etc. — those phrases alone are not enough;
  wait for the explicit slash command. Do NOT write code, do NOT
  touch the host environment — outputs are PROJECT.md and tech-stack.md
  (plus versioned PROJECT.v<N>.md backups on rewrite). Hands off to
  /sdd-impl for actual building.
---

# sdd-idea — idea → PROJECT.md

Turn a rough idea into two files: `PROJECT.md` — the spec plus the phased plan — and `tech-stack.md` — a verbatim copy of the stack recipe. **This skill writes no code, touches no environment, runs no commands.** Only output is those two files (plus versioned `PROJECT.v<N>.md` backups when the plan is rewritten). Environment readiness is `/sdd-impl`'s job.

The goal is that the user leaves with a concrete plan, not a vague direction. A weak plan produces a bad project; a solid plan lets `/sdd-impl` move phase-to-phase without constantly re-asking the user what they want.

## What SDD builds

SDD ships exactly one stack: **Django 5 + htmx + SQLite + Pico.css, running in Docker**. Every project — tracker, manager, blog, small internal tool, checklist — is built on this one foundation. The recipe lives in `references/tech-stack.md`; `/sdd-idea` copies it into each new project as `tech-stack.md`, and `/sdd-impl` reads that copy when it builds phases.

SDD does **not** build mobile apps, desktop apps, CLI tools, games, or anything that needs a native toolchain. If the user's idea lands in one of those categories, see Step 3 — in most cases you can still help by reframing the idea as a web MVP that can grow into a native wrap later (PWA → mobile, Tauri wrap → desktop).

## Audience and tone

The user is a vibe coder: building an app for themselves or a small group, not a professional developer. Speak Russian informally ("ты", not "вы"), friendly, short sentences.

All user-facing output and everything written into `PROJECT.md` is Russian. Code and identifiers stay English.

### How to talk about features and screens

When you describe options, screens, or features to the user — in `AskUserQuestion` option descriptions, chat messages, or the `## Как это работает` section of `PROJECT.md` — stick to what the user sees and does. Not how it's coded. One short sentence per option is usually enough; two if absolutely needed.

This rule applies **even when the user's own pitch is heavy on tech terms**. If the user described their idea with "approval-queue" and "workflows", your option descriptions still translate that into everyday language. Echoing their jargon back is noise, not signal — your job is to turn the idea into words a non-coder beside them could follow.

Words to avoid in user-facing text (they've tripped up real users):

- `стаб`, `заглушка` in the "mock response" sense — just say what the feature does in the MVP: «ответы пока простые, без настоящего AI».
- `payload` — use `данные` or describe the field: «что именно отправляется».
- `endpoint` — describe the action: «кнопка отправляет», «страница обновляется».
- `CRUD` — list the verbs the user cares about: «добавить, посмотреть, поменять, удалить».
- `workflow` — use `сценарий`, `автоматизация`, «последовательность действий».
- `cron`, `Django-Q`, `management-команда` — use «по расписанию», «по таймеру», «скрипт, который запускается сам».
- `middleware`, `fragment`, `swap` in the htmx sense — the user never needs to see these; describe what updates on screen instead.
- `pending` — use «ждёт подтверждения», «в ожидании».
- `queue` as a data-structure word — fine in the everyday sense («список действий на подтверждение»), never as «положить в очередь» / «достать из очереди».
- `мобилка`, `фишка`, `штука` — feels patronizing. Use `мобильное приложение`, `возможность`, or the actual name of the thing.

These anglicisms ARE fine because they read as normal Russian tech speech: `стек`, `фича`, `деплой`, `база` / `БД`, `форма`, `кнопка`, `страница`, `поле`, `интеграция`. The word `миграция` is also fine, but only in the narrow sense of "updating data after the plan changed" — don't stretch it to unrelated contexts.

**Example — same option, bad vs good:**

Bad (this is a real regression):

> Approve-queue (очередь действий). Список pending-действий с JSON-payload и кнопками Approve/Decline. После approve действие уходит в лог (стаб никуда не бьёт).

Good:

> Экран со списком действий, которые ждут подтверждения. У каждого — кнопки «одобрить» и «отклонить». После одобрения запись уходит в историю; на этом этапе действие никуда реально не отправляется.

Same information, half the special words, and the user actually knows what screen they're picking.

## Step 0 — gather context

Before anything else, collect context the user has already put in front of you:

1. **`./docs/` directory — always read it.** If `./docs/` exists in cwd, list its contents and read every text file in it (recursively; skip binaries and anything obviously huge). These are the user's own notes, references, sketches, or drafts for the idea — treat them as authoritative input alongside the chat messages. During the interview, cite specifics from docs ("в `docs/notes.md` ты упомянул X — это всё ещё актуально?") instead of asking questions the docs already answer. Carry what you learned from docs into `PROJECT.md` (the `## Что это`, `## Как это работает`, and `## Данные` sections especially). If `./docs/` is absent, skip silently.

2. **Text passed with the trigger.** The skill can be invoked as `/sdd-idea <описание идеи>` or just `/sdd-idea` on its own. If there is accompanying text, treat it as the user's opening pitch — start the interview from there, don't re-ask "что хочешь построить?". If there is no text, open with one broad question.

**What docs are for, and what they aren't.** Docs tell you *what* the user wants to build — the problem, the people, the data, the constraints. Docs do **not** dictate the stack. If docs mention specific production technologies (Postgres, Redis, Kafka, Kubernetes, a particular AI orchestration framework, "production-grade architecture", a specific cloud), treat those as long-term aspirations, not MVP requirements. The MVP runs on SDD's one stack; nothing else. Detailed production specs in docs are common when the user pasted a corporate document — the job here is to extract the *idea* and propose the *smallest possible web MVP* on top of it. Production-grade infra goes into later phases as "future extension", not Phase 1.

Then go to Step 1.

## Step 1 — existing PROJECT.md

First check: is there a `PROJECT.md` in cwd already?

- **If present:** read it, then `AskUserQuestion` with four options:
  1. Label «Продолжить проект» → tell the user to run `/sdd-impl`, exit without rewriting anything.
  2. Label «Расширить фичей» → tell the user to run `/sdd-feature`, exit.
  3. Label «Поменять что-то в плане или спеке» → tell the user to run `/sdd-change`, exit.
  4. Label «Начать заново» → back up `PROJECT.md` → `PROJECT.v<N>.md` (N = next free integer), then continue to Step 2.
- **If absent:** go to Step 2.

## Step 2 — the interview (5–8 turns)

Ask questions through `AskUserQuestion`. 1–3 related questions per turn, each with **2–4 concrete options** — the tool hard-fails at 5+. When a topic naturally has more answers (six possible field bundles, a long list of features), wrap them into coherent scope bundles instead of a flat list.

> Bad: six checkboxes — «название», «оценка», «год», «жанр», «дата», «заметка». Tool errors out, and the user picks blindly anyway.
>
> Good: three options — «Минимум» (название + оценка + дата), «Стандарт» (+ год + жанр + заметка), «Расширенный» (+ свободные теги, режиссёр, формат). The user picks a coherent shape, not a checklist of fields.

**Mark the recommended option.** When one option is genuinely the better starting point for this user (single-user mode for a personal tool, the standard field set, a simpler theme, declining a heavy integration in MVP), place it **first** and append «(Рекомендуется)» to the label. One «(Рекомендуется)» per question max — it's a real signal, not decoration. The user is free to overrule; the marker just removes the «what would *you* pick?» friction.

Goal: build a clear picture of *what* we're building and *for whom*. **Never ask about the stack** — there's only one, and the user doesn't pick it.

Cover the topics below. Don't skip without good reason — if a topic is clearly inapplicable (e.g. accounts for a personal single-user tool), skip silently and move on.

1. **The problem.** What's broken or missing? Why does it matter? What triggered this idea?
2. **The people.** Who uses it? How tech-savvy? Solo or multiple? How will they find the app?
3. **Core scenario.** Walk through a typical session step-by-step.
4. **Data.** What gets stored? How are records related? Rough shape of each record.
5. **Key actions.** Add / view / edit / delete / search / filter / share — which matter, which don't.
6. **Edge cases.** What if input is garbage? Storage fills up? Two users act at once (if multi-user)?
7. **Look and feel.** What apps/sites is this like in mood? Playful / minimal / data-dense?
8. **Accounts & access.** Login needed? Multiple users? Roles? Public parts vs private?
9. **Integrations.** External APIs? Import/export? Email/notifications?
10. **Priorities.** If you could only ship three features, which? Which are dreams for later?

Conversation rules:
- When the user gets animated on a topic, drill deeper.
- When they answer tersely or deflect, move on.
- Cite their earlier answers ("you said it's just for your family — so login probably isn't critical?").
- Don't introduce jargon the user hasn't used themselves.

## Step 3 — fit check (web or not web?)

By now you know what the user wants. Check whether it's a web app — anything that could sensibly run in a browser on localhost and later behind a URL. Trackers, managers, dashboards, forms, small CRMs, blogs, checklists, internal tools, lightweight games, even simple admin panels for an existing business — all fit.

If the idea doesn't obviously fit a web browser, try to reframe it as a web MVP first. Vibe coders often describe ideas in native terms because that's what they see on their phone, but the underlying *job* usually works fine in a web UI:

- **"Mobile app for X"** → a web app the user opens on their phone. Add `### Будущее расширение` notes about installing as a PWA, or wrapping with Capacitor / rewriting in Flutter later, once the core value is proven.
- **"Desktop app for X"** → a web app run locally via Docker, or hosted somewhere private. Note a future Tauri wrap if the user really wants a binary.
- **"CLI utility"** → if the utility is really a data entry + report flow, a web form + a results page covers it. If it's truly a pipeline or a filter that fits `cat in | tool | out`, SDD isn't the right tool.
- **"A game"** → only viable if it's simple enough to live in a Django template with a bit of JS/htmx. Anything requiring a game engine (Phaser, Unity, canvas physics) is out of scope.

Reframing rules:
- Always try the reframe before declining. Most "mobile" ideas work as mobile-friendly web.
- Confirm the reframe with the user through `AskUserQuestion` before proceeding — don't silently pivot their idea. Example phrasing: «Как раз под твою задачу удобно начать с веба — открывается с телефона без установки, данные на сервере, потом можно превратить в полноценное мобильное приложение. Подойдёт такой путь?»
- If the user insists on a native-only build (no web MVP acceptable) or the idea is genuinely beyond SDD's scope (a 3D game, a kernel module, a trading bot with hard latency budgets), tell them plainly:

  > Такую идею SDD4beginners не закроет — здесь мы собираем веб-приложения на Django. Поищи другой инструмент под этот стек или вернись, если захочешь веб-версию.

  Then exit.

When the idea fits (directly or after a reframe), log one short Russian sentence telling the user what's next. Example:
> Окей, собираем веб-приложение на Django + htmx. С телефона откроется нормально, а если потом захочется, чтобы оно ставилось на телефон как обычное приложение, — добавим PWA-обёртку (это когда сайт ставится в один клик и работает даже без интернета).

Then go to Step 4.

## Step 4 — propose the MVP

Formulate the **minimum version that still solves the core problem**. Not "everything we discussed" — "without which it wouldn't work at all". List included features in 2–4 short lines, plus a separate short list of nice-to-haves you parked.

Confirm via `AskUserQuestion` with three options:

- «Поехали, как есть **(Рекомендуется)**» → continue to Step 4.5.
- «Урезать ещё» → user says what to drop; revise and re-confirm.
- «Добавить из отложенных» → at least one nice-to-have moves into MVP.

If the user picks «Добавить из отложенных», immediately ask a follow-up `AskUserQuestion` (`multiSelect: true`) listing each parked nice-to-have as its own option, so the user picks **explicitly** what moves into MVP. Don't guess — guessing is how a clean 5-phase plan quietly turns into 8.

## Step 4.5 — pre-write summary

Before writing PROJECT.md, summarise the decisions back to the user. Five to seven Russian bullets covering: что строим, для кого, главные сценарии, состав MVP, что отложено, нестандартные риски (если есть). Then one `AskUserQuestion`:

- «Всё верно, пиши план **(Рекомендуется)**» → continue to Step 5.
- «Кое-что не так» → user corrects (one or two things); update the summary and re-confirm.

Why this gate exists: by Step 5 you're holding 5–8 turns of context. A short recap catches drift between «что юзер сказал в первом круге» and «что я собираюсь записать» before it lands on disk. Skip it and you'll write a plan that quietly contradicts the early answers, and the user will only notice when they read PROJECT.md cold.

## Step 5 — write PROJECT.md and copy tech-stack.md

Two files land in the project directory: `PROJECT.md` (spec + phase plan + a short stack summary) and `tech-stack.md` (the full recipe — scaffolding, tests, «do not bring in» list). Downstream skills read `tech-stack.md` from the project directory for everything recipe-related; `PROJECT.md` stays focused on what the user is building.

Structure of `PROJECT.md` — Russian headings, Russian prose inside each section, language-neutral code blocks verbatim. Include only sections that are relevant; skip a section if it doesn't apply (e.g. `## Аккаунты и доступ` for a personal single-user tool).

    # <Название проекта>

    ## Что это
    Two short sentences. First — what the app does (the user-facing job, not the tech).
    Second — who it's for (audience and rough scale). No feature list here; features
    belong in «Как это работает».

    ## Как это работает
    Numbered user flows. Concrete scenes in order: «открываешь главную → видишь … →
    кликаешь … → попадаешь …». Don't re-state features already named in «Что это»;
    show them happening. If a flow branches, branch the numbering — don't summarise.

    ## Данные
    What gets stored, how it's linked (only if relevant).

    ## Аккаунты и доступ
    (only if login matters)

    ## Интеграции
    (only if external APIs/services exist)

    ## Граничные случаи
    What happens when things go wrong.

    ## Открытые вопросы
    Only questions the user actually deferred during the interview («не знаю», «потом
    решим», «если успеем», «опционально»). Don't invent questions to look thorough —
    if the user didn't deflect on a topic, it's not open. If nothing was deferred, omit
    the section entirely.

    ## Стек
    **name:** django-htmx
    **summary:** Django 5 + htmx + SQLite + Pico.css в Docker. Страницы собираются на сервере, есть формы, готовая админка, встроенная база данных.

    ### Будущее расширение (опционально)
    Include this subsection only when one of these concrete triggers fired during the
    interview — not just to look thorough:
    - Public service / many users → Postgres вместо SQLite, регулярные бэкапы, CDN для статики.
    - User mentioned phone use → PWA-обёртка (ставится на телефон в один клик, работает офлайн).
    - User mentioned desktop preference → Tauri-обёртка (бинарник, который запускается локально).
    - User mentioned imports/exports beyond CSV → API или вебхуки.
    - User mentioned scale-out / heavy jobs → фоновые задачи (Django-Q / RQ), Redis-кеш.
    - User mentioned community / social → комментарии, подписки между профилями.

    Two or three friendly Russian bullets max, each pointing a future need at a likely
    later phase or technology. Pick triggers that actually came up.

    ## Фазы

    ### Фаза 1 — Настройка проекта
    **Цель:** <one Russian sentence>
    **Усилие:** Low

    - [ ] <tasks pulled from the django-htmx Phase 1 recipe, translated to Russian>
    - [ ] ...
    - [ ] Проверка: <concrete checkpoint — e.g. «http://localhost:5000 открывается и показывает <Название проекта>»>

    **Тесты Фазы 1:** <derived from the reference's test guidance>

    ### Фаза 2 — <Core scenario title>
    **Цель:** ...
    **Усилие:** Medium

    - [ ] ...

    **Проверка:** ...
    **Тесты Фазы 2:** ...

    (and so on)

    ### Фаза N — Полировка и деплой
    **Цель:** приложение доступно по публичному URL.
    **Усилие:** Low

    - [ ] <deploy tasks — Render.com or Fly.io>
    - [ ] Проверка: приложение открывается по публичной ссылке.

    **Тесты Фазы N:** все предыдущие чекпоинты ещё зелёные.

All prose inside `PROJECT.md` is Russian.

### Copy tech-stack.md into the project

After writing `PROJECT.md`, copy the recipe file into the project directory so downstream skills can find it:

    cp "$HOME/.claude/skills/sdd-idea/references/tech-stack.md" ./tech-stack.md

If `cp` isn't convenient, read the source with `Read` and write the destination with `Write` — the content is small. Byte-for-byte copy; no edits, no translation. This is the only file `/sdd-idea` creates besides `PROJECT.md` and its backups.

### Phase construction rules

- **Target size:** 4–7 phases for a typical idea. Up to 8 when there are many features.
- **Phase 1 is fixed by the stack reference.** Translate its "Phase 1 recipe" steps into tasks — this is a boot-the-container phase: Docker up, Django migrate, home page live.
- **Phase 2 is the core loop.** One end-to-end slice through the most important action. Recipe tracker: "add recipe → see in list". Budget tracker: "enter expense → see balance". Everything else comes later.
- **Vertical slices, not horizontal layers.** Each phase touches the whole stack (model + view + template + tests) for one feature. Do not do "all models first, then all views".
- **Each phase ends in a runnable state.** No "half a feature now, half next time".
- **Last phase is always polish + deploy.** Target: Render.com or Fly.io.
- **Checkpoints are observable, not "it works".** Not "user sees the list" but "open /recipes, click Add, type 'Borscht', submit — should appear on home page".
- **Effort:** Low / Medium / High. Not hours — vibe coders can't calibrate hours.
- **Tests are mandatory.** Every phase has a "Тесты Фазы N" section listing what must be covered by unit tests. 100% coverage on changed files (Django `core/*.py`, excluding migrations/tests/admin/apps) is enforced by `/sdd-impl`.

### Coverage self-check

After writing `PROJECT.md`, mentally walk each MVP item and each "add later" item: **every one must be a task in at least one phase.** If something isn't covered, add a task — don't save a plan with a hole.

### Phase count self-check

Target: 4–7 phases. 8 is the upper limit reserved for genuinely many features. After the plan is laid out, count the phases. If you're at 8 or above, look hard for merges — two adjacent CRUD-ish phases often collapse into one «add + edit + delete + list», search and stats often share a list page so they share a phase. If after honest looking the count is still ≥8, surface that to the user before Step 6 with one short message:

> Получилось <N> фаз — это много, но не критично. Хочешь, попробую слить две — назови, какие выглядят как кандидаты, или предложу варианты сам.

Don't auto-merge — the user might insist on the granularity. But don't pretend an 8-phase plan has the same shape as a 5-phase one either.

## Step 6 — offer next steps

Show a summary: phase titles and one-line checkpoints. Then `AskUserQuestion` with three options:

1. Label «Продолжим интервью» → return to Step 2, focused on what the user wants to deepen ("the data model", "feature X", "edge cases"). After the follow-up, rewrite `PROJECT.md` (old version goes to `PROJECT.v<N>.md`).
2. Label «Поменять план» → no re-interview; user says what to change (split a phase, merge two, reprioritize, move something to "later"), you apply it, rewrite `PROJECT.md` with backup.
3. Label «Поехали, строим!» → the plan is final. Print:

   > Готово. План — в `PROJECT.md`. Запусти `/sdd-impl` — построю Фазу 1 и подниму приложение в браузере.
   >
   > `PROJECT.md` — это твой план: спецификация проекта + фазы с чекбоксами. Можешь открыть и перечитать в любой момент, по нему я и работаю дальше.
   >
   > Когда понадобится:
   > - `/sdd-impl` — собрать следующую фазу (код + тесты + проверка в браузере).
   > - `/sdd-feature` — добавить новую фичу в план (допишу фазы в конец).
   > - `/sdd-change` — поменять что-то в плане: переписать раздел спеки, поправить ещё не построенную фазу, или переделать уже готовое поведение.
   > - `/sdd-undo` — откатить последнюю построенную фазу, если что-то пошло не так.

Options 1 and 2 can be chosen as many times as the user wants — versioning protects previous drafts. **Only «Поехали, строим!» hands off control.**

## What not to do

- Do not touch the host environment — no installs, no version checks, no toolchain probes. Environment readiness lives in `/sdd-impl`; planning shouldn't care.
- Do not create any file other than `PROJECT.md`, its `PROJECT.v<N>.md` backups, and `tech-stack.md`.
- Do not try to do Phase 1's tasks — that's `/sdd-impl`'s job.
- Do not discuss framework, library, or hosting choices with the user. SDD ships one stack; the user ships the app.
- Do not silently pivot a non-web idea into a web app — confirm the reframe through `AskUserQuestion` (see Step 3).
- Do not silently extend the stack with extras the reference doesn't list (no Postgres, no Redis, no Tailwind, no Celery in Phase 1) just because the user's docs mentioned them. Production-grade infra belongs in `### Будущее расширение` and later phases.
- Do not write «ТЫ ДОЛЖЕН» / "YOU MUST" in the plan — the tone is bad for vibe coders.
- Do not ask all-or-nothing questions — always give options.
- Do not draw ASCII diagrams or flowcharts in `PROJECT.md` unless the user explicitly asks.

## Example trigger prompts

> «Хочу сделать приложение для учёта книг, которые читаю. Чтобы можно было ставить
> оценку, писать короткие заметки, и видеть статистику по месяцам.»

Flow: interview → Phase 3 fit check says "web, easy" → MVP proposal → `PROJECT.md` with ~5 phases → user runs `/sdd-impl`.

> «Хочу мобильное приложение, чтобы в зале отмечать подходы и веса.»

Flow: interview → fit check reframes as "веб-трекер, открывается с телефона, позже можно обернуть как PWA" → `AskUserQuestion` confirms the reframe → MVP proposal → `PROJECT.md` with ~5 phases and a `### Будущее расширение` note about mobile wrapping → user runs `/sdd-impl`.

> «Хочу игру 3D про гонки на Unreal Engine.»

Flow: fit check can't reframe — this isn't a web job. Tell the user SDD4beginners doesn't cover it and exit without writing PROJECT.md.
