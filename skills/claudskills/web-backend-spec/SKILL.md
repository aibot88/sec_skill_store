---
name: web-backend-spec
description: Augment a sprint's SPEC.md with a Backend section (API contract, data model changes, authn/authz, validation, observability, contract test plan) tailored to the detected stack (Express/Fastify/Next/FastAPI/Django/Go/Rails/etc). Coordinator-only — does not write production code. Pauses for user confirmation. Run before /magi:tasks.
disable-model-invocation: true
---

# /magi:web-backend-spec — backend elaboration

You are the coordinator. Add a backend-specific section to a sprint's
SPEC.md. **You do not write production code.** Read
`references/domain/web/backend.md` before starting.

## 0. Preflight

```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-}"
[[ -z "$PLUGIN_ROOT" ]] && PLUGIN_ROOT="$(cd "$(dirname "$BASH_SOURCE[0]")/../.." 2>/dev/null && pwd)"
USER_CONFIG="$HOME/.config/magi-workflow/config.json"
```

If config missing → tell user to run `/magi:setup`.


## 0.5. State preflight (auto-refuse if not allowed)

```bash
STATE_JSON=$(bash "$PLUGIN_ROOT/scripts/shared/detect-state.sh")
blocked=$(jq -r '.disallowed_skills["web-backend-spec"] // empty' <<<"$STATE_JSON")
if [[ -n "$blocked" ]]; then
  reason=$(jq -r '.disallowed_skills["web-backend-spec"].reason' <<<"$STATE_JSON")
  suggest=$(jq -r '.disallowed_skills["web-backend-spec"].suggest' <<<"$STATE_JSON")
  echo "Cannot run /magi:web-backend-spec: $reason"
  echo "Suggested: $suggest"
  exit 1
fi
```

`--force` skips preflight (advanced/recovery only).

## 1. Locate sprint + spec

Find the sprint folder (default: most recent; or `--sprint <num>-<slug>`).
The folder must contain a plan-equivalent file. Identify which exists
(priority order):

- If SPEC.md exists → use SPEC.md as the target.
- If only PLAN.md exists → use PLAN.md as the target. Do NOT rename or
  "upgrade" PLAN.md to SPEC.md — that is a separate decision the user
  makes via `/magi:plan`, not forced by web-* skills.
- If only TICKET.md exists → use TICKET.md as the target.
- If none exists → abort and tell the user to run `/magi:plan` first.

## 2. Detect stack

Per `references/domain/web/backend.md` "Stack discovery". Capture:

- Web framework (Express / Fastify / Next route handlers / FastAPI / Django / Rails / Go net/http / etc.)
- Language (TS / Python / Go / Rust / Ruby)
- ORM (Prisma / TypeORM / SQLAlchemy / GORM / Active Record)
- DB (Postgres / MySQL / SQLite / Mongo / Redis)
- Auth scheme (JWT / session / OAuth proxy)
- API style (REST / GraphQL / gRPC / tRPC)
- Background jobs (BullMQ / Sidekiq / Celery / Cloud Tasks / k8s CronJob)

Ask the user once if anything is ambiguous.

## 3. Identify backend-relevant scope

Read PLAN/SPEC. Pick out the items that need backend work:

- New endpoints or fields
- Schema changes (new table, new column, index, constraint)
- New external integration (third-party API, webhook)
- New authn/authz rule
- New background job
- New SLA / performance constraint

Out-of-scope items (pure UI, infra-only) are skipped here.

## 4. Generate the Backend section

Following `references/domain/web/backend.md` "Deliverable" structure:

### a. API contract — write SCHEMA FIRST

For REST: produce an OpenAPI excerpt (inline, or as `magi/<num>-<slug>/openapi.yaml`).
For GraphQL: SDL excerpt.

Cover the fields in the reference's "Contract review checklist":
- Versioning, pagination, filtering, errors, idempotency, rate limits, CORS, auth scopes.

### b. Data model changes

If the schema changes:

- Migration plan (file names, order, dependencies)
- Online migration strategy if the table is populated
- Indexes & constraints
- Rollback strategy
- Backup taken first? (yes for irreversible changes)

### c. Authn/authz matrix

Per endpoint:

| Endpoint | Method | Auth required? | Roles/scopes | Ownership rule |
|----------|--------|----------------|--------------|----------------|
| `/v1/users/:id` | GET | yes | `users:read` | self OR admin |
| ... | | | | |

### d. Validation & safety

- Validation library (zod / yup / pydantic / validator).
- Sanitisation rules for user-generated content.
- Path traversal / SQL injection / XSS / CSRF surfaces.
- What gets logged vs masked.

### e. Idempotency & retries

For mutating endpoints: idempotency-key support; replay window; storage.

### f. Observability

Per endpoint or per feature:
- Structured log fields
- Metrics (counter, latency p50/p95/p99, error rate)
- Trace span shape
- Alert thresholds

### g. Test plan

Three layers from the reference:
- Unit (business logic, validators)
- Integration (DB roundtrip, transaction)
- Contract (OpenAPI / SDL conformance test) — use template from reference

Include the exact test command(s).

### h. Open questions

What's unresolved?

## 5. Append to the target document

Append under `## Backend` top-level heading in whichever plan-equivalent
file was identified in §1 (SPEC.md, PLAN.md, or TICKET.md). If a Backend
section exists, ask before overwriting / merging.

If the API contract is large, write it to `magi/<num>-<slug>/openapi.yaml` or
`magi/<num>-<slug>/schema.graphql` and link from SPEC.md.

## 6. Optional: scaffold contract test

If the project has the relevant test framework (vitest+supertest,
pytest+httpx, etc.), offer to create a contract test stub at
`tests/api/<feature-slug>.contract.test.ts` (or the project's convention).
Use the template in the reference. Selectors / payloads stay as TODOs.

Confirm with the user before creating files.

## 7. Stop and hand off

Show the user:
- Diff of SPEC.md (Backend section + linked schema files)
- Whether a contract-test stub was created
- Top 3 open questions

Recommend next step:
- `/magi:tasks` if SPEC is complete.
- `/magi:web-frontend-spec` / `.infra.plan` / `.ci.spec` if relevant.
- `/magi:review-plan` for multi-model review.

## Argument parsing

- `--sprint <num>-<slug>` — explicit sprint folder.
- `--api-style rest|graphql|grpc|trpc` — skip detection.
- `--scaffold-test` — auto-create contract test stub.
- `--no-scaffold` — never create files outside the sprint dir.
- `--openapi <path>` — append to an existing OpenAPI file rather than create new.

## Conventions

- **Contract first**: write the schema before discussing implementation.
- **One Backend section per SPEC.md** — iterate by editing in place.
- Backfill plans for populated tables are mandatory; do not let them slide.
- Authz matrix: never approve `(none)` for a mutating endpoint without
  explicit justification (e.g., webhook with HMAC verification).
- For very thin changes (e.g., adding a single optional field to an
  existing endpoint), tell the user this skill is overkill and recommend
  inline edits to SPEC.md.
