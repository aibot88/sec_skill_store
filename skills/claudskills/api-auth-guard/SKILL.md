---
name: api-auth-guard
description: Use this skill BEFORE creating, editing, or reviewing any file in src/app/api/**/route.ts in the SmartHouse project. Invoke when the task mentions API route, endpoint, backend, /api/, route.ts, NextRequest, middleware, authentication, auth, autoryzacja, token, cron, CRON_SECRET, session, iron-session. This skill enforces that EVERY endpoint has one of three auth mechanisms (iron-session, CRON_SECRET Bearer, or Firebase ID token) before returning data.
---

# API Auth Guard — Obowiązkowa weryfikacja autoryzacji

## Kontekst

Reguła #4 ("Każde API route wymaga auth") w [CLAUDE.md](../../../CLAUDE.md) i [AGENTS.md](../../../AGENTS.md). Brak autoryzacji = bezpośrednie ryzyko wycieku danych mieszkańców i pracowników.

SmartHouse używa **trzech** mechanizmów autoryzacji — każdy endpoint musi mieć dokładnie jeden.

## Trzy dozwolone wzorce auth

### Wzorzec A — iron-session (endpointy UI wywoływane z przeglądarki)

```typescript
import { getSession } from '@/lib/auth';

export async function GET(req: NextRequest) {
  const session = await getSession();
  if (!session?.uid) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  // opcjonalna weryfikacja roli
  if (!session.isAdmin) {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
  }
  // ... logika
}
```

**Kiedy używać:** endpointy wywoływane przez fetch z komponentów React, operacje powiązane z konkretnym użytkownikiem.

**Przykłady w projekcie:** [src/app/api/employees/stats/route.ts](../../../src/app/api/employees/stats/route.ts), [src/app/api/control-cards/route.ts](../../../src/app/api/control-cards/route.ts)

### Wzorzec B — CRON_SECRET Bearer (cron joby, manualne egzekucje przez admin proxy)

```typescript
function authorize(req: NextRequest): boolean {
  const authHeader = req.headers.get('authorization');
  return !!process.env.CRON_SECRET && authHeader === `Bearer ${process.env.CRON_SECRET}`;
}

export async function POST(req: NextRequest) {
  if (!authorize(req)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  // ... logika
}
```

**Kiedy używać:** Firebase Scheduler, alert cron, data-guard, wszelkie automatyczne wywołania.

**Przykład w projekcie:** [src/app/api/alerts/route.ts:7-11](../../../src/app/api/alerts/route.ts#L7-L11)

### Wzorzec C — Admin Proxy (cron wywoływany ręcznie przez admina z UI)

Endpoint admin proxy weryfikuje `getSession().isAdmin`, a następnie wewnętrznie fetchuje chroniony endpoint cron z `CRON_SECRET`. Nigdy nie ujawniaj `CRON_SECRET` klientowi.

## Checklist dla każdego nowego route

Wykonaj **zanim** napiszesz logikę biznesową:

- [ ] Czy endpoint ma funkcję sprawdzającą auth na początku handlera (przed jakimkolwiek odczytem danych)?
- [ ] Czy wszystkie metody HTTP (GET/POST/PUT/DELETE/PATCH) mają auth?
- [ ] Czy przy braku auth zwracasz `401` (nieautoryzowany) lub `403` (brak uprawnień), NIE `500`?
- [ ] Czy zwracany błąd **nie ujawnia** stack trace ani szczegółów implementacji?
- [ ] Czy użyłeś dokładnie jednego z trzech wzorców (A/B/C) — nie mieszanki?
- [ ] Czy rola użytkownika (admin/koordynator/legalizacja) jest sprawdzana dla wrażliwych operacji?

## Antywzorce — natychmiastowy bloker

Jeśli zobaczysz w kodzie któryś z poniższych — zatrzymaj się i zgłoś:

```typescript
// ❌ Brak jakiejkolwiek weryfikacji
export async function GET(req: NextRequest) {
  const data = await getEmployees();
  return NextResponse.json(data);
}

// ❌ Auth tylko w komentarzu ("TODO: add auth")
// TODO: implement auth
export async function POST() { ... }

// ❌ CRON_SECRET w URL query
// /api/cron?secret=xyz  — NIGDY, secret w URL trafia do logów

// ❌ Własny mechanizm auth wymyślony ad-hoc
if (req.headers.get('x-my-custom-token') === 'hardcoded-value') { ... }

// ❌ Sekret hardcodowany w kodzie
const SECRET = 'super-secret-123';  // musi być z env var

// ❌ Zwracanie szczegółów błędu klientowi w prod
return NextResponse.json({ error: err.stack }, { status: 500 });
```

## Rate limiting (dla krytycznych endpointów)

Dla endpointów wykonujących **drogie operacje** (wysyłka push, pisanie do Sheets, cron) rozważ dodanie rate limiting. Na ten moment w projekcie nie ma dedykowanej biblioteki — zaproponuj orchestratorowi dyskusję zanim dodasz.

## Środowiskowe — sekrety

Sekret używany w auth (np. `CRON_SECRET`) musi być:

1. W `.env.local` (dev)
2. W `apphosting.yaml` jako sekret
3. Ustawiony przez `firebase apphosting:secrets:set`

Brak któregokolwiek z trzech miejsc = awaria na produkcji. Szczegóły w [feedback_secrets_both_places](../../memory/feedback_secrets_both_places.md).

## Output dla Orchestratora

```
API_AUTH_AUDIT:
  files_audited:
    - src/app/api/employees/route.ts: ✅ pattern A (iron-session + isAdmin)
    - src/app/api/alerts/run/route.ts: ✅ pattern B (CRON_SECRET)
    - src/app/api/public/something/route.ts: ❌ NO AUTH — BLOCKER
  status: blocked_on_missing_auth | all_green
  action_required: Add auth to src/app/api/public/something/route.ts
```
