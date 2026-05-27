---
name: freelo-api
description: Práce s Freelo.io v1 REST API a webhooky — projekty, tasklists, tasky, subtasks, komentáře, time tracking, work reporty, custom fields, faktury, soubory. Spouštěj vždy když uživatel zmíní Freelo, freelo.io, app.freelo.io, api.freelo.io, integraci s Freelo, automatizaci tasků ve Freelu, time tracking přes API, Freelo webhooky, Freelo Make/Zapier/n8n integraci, nebo Freelo API key. Také pokud kód importuje volání na `api.freelo.io/v1/`. NEspouštěj pro nesouvisející project-management nástroje (Asana, Trello, Jira, ClickUp, Notion).
---

# Freelo API skill

Praktický průvodce Freelo v1 API. Když pomáháš s integrací, automatizací nebo dotazem na endpointy, **vždy nejprve načti relevantní referenci** v `references/` místo dohadování.

## Zdrojová dokumentace

- **Swagger UI:** https://api.freelo.io/docs/v1/freelo-api
- **OpenAPI specs (autoritativní zdroj pravdy):**
  - `references/freelo-api.yaml` — REST API (cca 6300 řádků, plné popisy včetně non-obvious chování)
  - `references/freelo-webhooks.yaml` — webhook spec (1000 řádků)
- **Pomocné texty:** [Webhooky CZ](https://www.freelo.io/cs/napoveda/webhooky), [Webhooky EN](https://www.freelo.io/en/help/webhooks)

Když potřebuješ detail endpointu, který v této SKILL.md není, **nejprve sáhni do `references/freelo-api.yaml`** (přesný popis polí, validace, chybové hlášky a non-obvious chování — vše je tam zdokumentováno) a teprve pak vymýšlej.

## Základy

| Vlastnost | Hodnota |
|---|---|
| Base URL | `https://api.freelo.io/v1/` |
| Autentizace | HTTP Basic Auth (username = email, password = API key z https://app.freelo.io/profil/nastaveni) |
| Povinný hlavička | `User-Agent: <App_Id> (<email@company.tld>)` — bez ní volání nefunguje |
| Content-Type | `application/json` (krom `/file/upload` → `multipart/form-data`) |
| Encoding | UTF-8 JSON |
| Rate limit | Per-user, dynamický → **NEHARDKÓDUJ limit**. Při `429 Too Many Requests` udělej exponential backoff. |

### Minimální curl příklad

```bash
curl -u lukas@viridium.cz:$FREELO_API_KEY \
     -H 'User-Agent: ViridiumIntegration (lukas@viridium.cz)' \
     -H 'Content-Type: application/json' \
     https://api.freelo.io/v1/users/me
```

### Heslo / API key

Pokud uživatel API key nemá v prostředí, **požádej ho o něj v chatu** (Apple Keychain GUI popup je třeba se vyhnout). Pravděpodobné jméno proměnné: `FREELO_API_KEY`.

## 5 kritických gotchas (čti vždy)

1. **Timestampy nejsou RFC3339.** API posílá *naive ISO8601* bez timezone (např. `2026-04-24T11:12:38`) v **Europe/Prague** (CET/CEST, DST!). Strict parser jako `time.Parse(time.RFC3339, ...)` v Go selže. Webhook payloady **mají** offset (`2026-04-24T15:30:00+02:00`) — jiný formát než REST! Detail v `references/gotchas.md`.
2. **Měna jako string × 100.** `"100025"` = 1000.25. Žádné tečky, čárky, ani floaty. Měny: CZK, EUR, USD.
3. **Stránkování přes `?p=` od 0**, ne 1.
4. **Edit používá `POST`, ne `PUT`/`PATCH`** (historický důvod — týká se task editu, comment editu, work report editu, note editu...).
5. **Mnoho endpointů má skryté side-effecty / non-obvious chování** (např. první komentář na tasku se stane description; `GET /public-link/task/{id}` link **vytvoří** pokud neexistuje; `worker_id` je tichý alias pro `worker`; smart-taskcheck tiše degraduje na simple). Vždy zkontroluj `references/gotchas.md` před voláním nestandardního endpointu.

## Když uživatel chce konkrétní operaci

| Situace | Kam jít |
|---|---|
| Hledám endpoint pro X | `references/endpoints.md` (přehledná tabulka všech endpointů) |
| Detail parametrů, validace, chybové hlášky | `references/freelo-api.yaml` (autoritativní) |
| Webhook setup, registrace, payload struktury | `references/webhooks.md` + `references/freelo-webhooks.yaml` |
| Copy-paste curl/Python příklady běžných tasků | `references/recipes.md` |
| Datové struktury / response shapes | `references/schemas.md` |
| Non-obvious chování, gotchas, alias hacky | `references/gotchas.md` |

## Sumář endpointů (32 resource skupin, ~95 endpointů)

**Projects:** `/projects`, `/all-projects`, `/invited-projects`, `/archived-projects`, `/template-projects`, `/user/{id}/all-projects`, `/project/{id}` (GET/DELETE), `/project/{id}/workers`, `/project/{id}/archive`, `/project/{id}/activate`, `/project/{id}/remove-workers/by-{ids,emails}`, `/project/create-from-template/{id}`

**Project Labels:** `/project-labels/find-available`, `/project-labels/{id}` (POST/DELETE), `/project-labels/{add-to,remove-from}-project/{id}`

**Pinned Items:** `/project/{id}/pinned-items` (GET/POST), `/pinned-item/{id}` (DELETE)

**Tasklists:** `/project/{id}/tasklists` (POST), `/all-tasklists`, `/project/{pid}/tasklist/{tid}/assignable-workers`, `/tasklist/{id}` (GET), `/tasklist/create-from-template/{id}`

**Tasks:** `/project/{pid}/tasklist/{tid}/tasks` (GET/POST), `/all-tasks`, `/tasklist/{id}/finished-tasks`, `/tasks/relations` (POST bulk), `/task/{id}` (GET/POST=edit/DELETE), `/task/{id}/{activate,finish}`, `/task/{id}/move/{tasklist_id}`, `/task/{id}/projects` (multi-project), `/task/{id}/relations`, `/task/{id}/projects/{pid}`, `/task/{id}/description` (GET/POST), `/task/{id}/reminder` (POST/DELETE), `/public-link/task/{id}` (GET/DELETE), `/task/create-from-template/{id}`, `/task/{id}/total-time-estimate` (POST/DELETE), `/task/{id}/users-time-estimates/{uid}` (POST/DELETE)

**Subtasks:** `/task/{id}/subtasks` (GET/POST)

**Task Labels:** `/task-labels` (POST bulk-create), `/task-labels/{add-to,remove-from}-task/{id}`

**Comments:** `/task/{id}/comments` (POST), `/comment/{id}` (POST=edit), `/all-comments`

**Time Tracking:** `/timetracking/{start,stop,edit,status}` — pouze 1 běžící session per user

**Work Reports:** `/work-reports`, `/task/{id}/work-reports` (POST), `/work-reports/{id}` (POST=edit/DELETE)

**Invoicing:** `/issued-invoices`, `/issued-invoice/{id}`, `/issued-invoice/{id}/{reports,reports-json,mark-as-invoiced}`

**Users:** `/users/me`, `/users`, `/users/project-manager-of`, `/users/manage-workers` (POST=invite), `/user/{id}/out-of-office` (GET/POST/DELETE)

**Notifications:** `/all-notifications`, `/notification/{id}/mark-as-{read,unread}`

**Events (audit log):** `/events`

**Files:** `/file/{uuid}` (GET=download), `/file/upload` (POST multipart, max 100 MB), `/all-docs-and-files`

**States:** `/states` (lookup tabulka)

**Custom Fields:** `/custom-field/get-types`, `/custom-field/create/{pid}`, `/custom-field/{rename,delete,restore}/{uuid}`, `/custom-field/add-or-edit-{value,enum-value}`, `/custom-field/delete-value/{uuid}`, `/custom-field-enum/get-for-custom-field/{uuid}`, `/custom-field-enum/{create,change,delete,force-delete}/{uuid}`, `/custom-field/find-by-project/{pid}`

**Notes/Documents:** `/project/{id}/note` (POST), `/note/{id}` (GET/POST/DELETE)

**Search:** `/search` (POST, Elasticsearch-backed, povinný `search_query`)

**Webhooks (management):** `/webhooks` (POST=register), `/webhook/{uuid}` (DELETE)

## Webhook subscription names (11)

`task_created`, `task_edited`, `task_finished`, `task_deleted`, `task_undeleted`, `task_activated`, `task_moved`, `tasklist` (all lifecycle), `comment` (all lifecycle), `note` (= document_*), `workreport` (all lifecycle).

**Bezpečnost:** Freelo **nepodepisuje payloady** (žádný HMAC). Použij unguessable URL path s náhodným tokenem jako capability. Detail v `references/webhooks.md`.

## Když nevíš

1. Sáhni do `references/freelo-api.yaml` přes `Read` na konkrétní řádek (každý endpoint má `summary` + `description` + `## Behavior notes (non-obvious)` sekci).
2. Hledej v souboru `grep -n` na operationId nebo path.
3. Pokud uživatel chce příklad konkrétní operace, kombinuj `references/recipes.md` se schématy z `references/schemas.md`.
4. Pro webhooky vždy načti `references/webhooks.md` — payload formát + retry policy + dedup pattern jsou kritické.
