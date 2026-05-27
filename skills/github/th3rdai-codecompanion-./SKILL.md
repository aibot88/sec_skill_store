# AGENTSKILL — Chat agent first-party app capabilities

**Status:** Plan (implementation-ready)  
**Formal review:** [docs/AGENTSKILL-plan-review.md](docs/AGENTSKILL-plan-review.md) — **Verdict: READY**  
**Goal:** Let the **Chat** agent (and other agent-tool modes where appropriate) invoke **first-party Code Companion features** through **bounded builtin tools**, reusing the same `lib/*` pipelines and security patterns as the UI and HTTP routes—**not** reimplementing prompts or duplicating business logic.

**Related:** `docs/AGENT-APP-CAPABILITIES-ROADMAP.md` (Validate + Planner + optional GSD); `lib/builtin-agent-tools.js`; `lib/tool-call-handler.js`; `lib/chat-post-handler.js`; `server.js` (`POST /api/chat`).

---

## 1. Problem statement

Today, the agent already has **builtins** (terminal, `write_file`, PDF/office, **Validate scan/generate**, **Planner `score_plan`**, optional **browser** suite) plus **MCP** tools. Many other product surfaces (**Review**, **Security / pentest**, **Experiment**, **builder** scoring flows beyond planner, **Create/Build** orchestration) exist only as **UI + dedicated routes** and are **not** callable as structured tools from Chat. Users cannot ask the agent to “run the same review as Review mode” with parity guarantees.

---

## 2. Principles (non-negotiable)

| #   | Principle                                                                                                                                                                                    |
| --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P1  | **Single implementation** — Builtin handlers call **shared `lib/*` service functions** that HTTP routes also call. Routes must **not** duplicate validation logic that builtins skip.        |
| P2  | **No prompt forks** — Review / pentest / experiment text generation continues to use **`lib/prompts.js`** (or existing review/pentest modules), not a second copy for the agent.             |
| P3  | **Security parity** — Path checks, `requireLocalOrApiKey` semantics, payload caps, and **project/chat folder** boundaries match existing APIs; heavy ops respect **abort** and **timeouts**. |
| P4  | **Settings gates** — Each capability family gets an **explicit toggle** (default conservative), consistent with agent terminal / validate / browser.                                         |
| P5  | **Model reality** — Tool calling requires models that emit **`TOOL_CALL:`** reliably; document cloud-model limitations (`lib/auto-model.js` already notes this).                             |

---

## 3. Current inventory (baseline)

**Already exposed as builtins (when gated):** `run_terminal_cmd`, `write_file`, `view_pdf_pages`, `generate_office_file`, `score_plan`, `validate_scan_project`, `validate_generate_command`, `browse_url`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_scroll`.

**High-value gaps for Chat (proposed builtins or one dispatcher):**

| Feature                                          | Primary reuse surface                                                                             |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| **Review**                                       | `lib/review.js`, `routes/review.js`, `POST /api/review` contract                                  |
| **Security / OWASP scan**                        | `lib/pentest.js` / `routes/pentest.js`, folder + file constraints                                 |
| **Experiment**                                   | `routes/experiment.js`, `lib/experiment-store.js` — **deferred for Chat builtins (v1)**; see §5.4 |
| **Builder score (Prompting / Skillz / Agentic)** | `routes/score.js` → `POST /api/score` with `mode` keys + `lib/builder-schemas.js`                 |
| **GSD (optional)**                               | `lib/gsd-bridge.js` — roadmap Phase 3; allowlist-only, default off                                |

**Explicitly out of scope for v1 (unless product expands):** Replacing **Create/Build wizards** with agent tools (high UX coupling); arbitrary **mode switching** in the renderer from the server (prefer **return structured results** to the model, not “open a tab”).

---

## 4. Architecture options

**Option A — One dispatcher builtin**  
`builtin.invoke_app_skill({ skill: "review.run", payload: { ... } })` with a **central allowlist** map `skill → handler`. Pros: one schema to secure; Cons: large switch, harder to document per-tool in MCP-style lists.

**Option B — One builtin per capability** (recommended for clarity)  
Examples: `review_run`, `pentest_scan_file`, `builder_score` (mode param). Pros: matches existing TOOL_CALL patterns, clearer in logs; Cons: more boilerplate.

**Decision (plan default):** **Option B** for v1–v2; revisit dispatcher only if tool-count explodes.

---

## 5. Phased delivery

### 5.0 Shared implementation pattern (applies to Phase 1+)

- **Do not** invoke Express `router` handlers from builtins (no fake `req`/`res`).
- **Do** extract or add **`lib/*` entrypoints** (e.g. `runReviewJob(...)`, `runPentestSnippetJob(...)`) that:
  - accept **plain objects** + config + **`AbortSignal`** (optional) + Ollama auth bag;
  - perform the same validation as today’s routes (or call existing validators used by routes);
  - call **`reviewCode` / `pentestCode` / …** unchanged for prompt/LLM work.
- **Refactor `routes/review.js` (and others)** to thin wrappers: parse body → validate → call service → map result to HTTP/SSE.

#### 5.0.1 Result envelope (pinned contract — every app-skill builtin returns this)

All Phase 1+ builtins (`review_run`, `pentest_scan`, `pentest_folder`, `builder_score`) return a single JSON object with this shape so the chat agent has a predictable interface across skills:

```jsonc
{
  "ok": true,
  "type": "report-card" | "summary",   // report-card = structured; summary = stream-collapsed text
  "data": { /* schema-validated payload, e.g. ReportCardSchema for review */ },
  "summary": "string",                  // present when type === "summary"
  "truncated": false,                   // true when stream summary was capped
  "model": "qwen3-32k:latest",          // resolved model (echo when "auto")
  "durationMs": 18420
}
```

#### 5.0.2 Error envelope (pinned — replaces ad-hoc `{error: "..."}` shapes)

```jsonc
{
  "ok": false,
  "code": "TOOL_DISABLED" | "AUTH_FAILED" | "TIMEOUT" | "PATH_DENIED" |
          "MODEL_FAILED" | "INVALID_ARGS" | "RATE_LIMITED",
  "message": "human-readable description",
  "hint": "optional next step (e.g. 'enable Settings → Agent → App Skills')"
}
```

The model can switch on `code` to choose recovery behavior; `message` is shown to the user verbatim. **Never** include raw stack traces, file paths beyond what HTTP routes already expose, or secrets.

### 5.1 Phase 1 — Review builtin (`review_run`)

**Contract (aligned with `POST /api/review`):**

| Field                 | Builtin behavior                                                                                                                                                                                                                                                                                                                                                       |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`model`**           | **Required**, same semantics as HTTP body `model`: concrete Ollama name **or** `"auto"`. When `"auto"`, use **`resolveAutoModel`** with **`mode: "review"`** (same as `routes/review.js`). The chat session’s toolbar model is **not** implicitly injected unless the product explicitly maps “chat model → review” later; v1 = **explicit tool args** mirror the API. |
| **`code`**            | **Required** string (inlined source), same as HTTP. Optional v1.1: **`sourcePath`** resolved server-side with **identical path rules** as multi-file review routes (`isWithinBasePath` vs `projectFolder` / configured roots only—**no paths beyond what HTTP allows**).                                                                                               |
| **`filename`**        | Optional; passed through to `reviewCode` `opts.filename`.                                                                                                                                                                                                                                                                                                              |
| **`images`**          | Optional array; same caps as route (max 10).                                                                                                                                                                                                                                                                                                                           |
| **`validateContext`** | Optional; same sourcing pattern as route (`loadValidateReviewContext` / `review-validate-context` pipeline).                                                                                                                                                                                                                                                           |

**Return value:** Same structured shapes as HTTP **report-card** path (`{ type: "report-card", data: … }`). For **chat-fallback** (`reviewCode` returns `type: "chat-fallback"` + stream): v1 builtin either **consumes the stream inside the server** until completion and returns a **single JSON summary** (truncated), or returns **`{ error: "…", hint: "use Review mode for streaming" }`** — pick one in implementation and document in `docs/AGENT-SKILLS.md`.

**Abort / Stop (Critical — current code):**

- `reviewCode` → `chatStructured` in `lib/ollama-client.js` **extracts `abortSignal` from `ollamaOptions` but does not attach it to `fetch`** (only an internal timeout `AbortController` is used). **`chatStream`** does support external `abortSignal`.
- **Required work before/with Phase 1:**
  1. Extend **`chatStructured`** to honor **`abortSignal`**: combine with timeout (e.g. `AbortSignal.any` or linked abort on user signal).
  2. Thread **`opts.abortSignal`** (or `opts.signal`) from **`reviewCode`** / **`reviewFiles`** into the `ollamaOptions` passed to **`chatStructured`** and **`chatStream`**.
  3. Builtin executor passes the **same `AbortSignal` used for the parent `POST /api/chat`** (from `chat-post-handler` / tool loop).
  4. Optionally thread **`req.on("close")`** into HTTP review later for parity (not blocking Chat).

**Tests:** Path traversal denied; with **mocked `chatStructured`**, assert **`abortSignal`** aborts in-flight call; schema validation on success payload — **not** byte-for-byte parity with a live model output.

### 5.2 Phase 2 — Security / pentest (`pentest_*` family)

**HTTP surface today (`routes/pentest.js`):**

| Route                              | Purpose                             | Agent v1                                                                                                                                        |
| ---------------------------------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `POST /api/pentest`                | Single-snippet scan (`pentestCode`) | **In scope** — builtin mirrors caps (model, code, filename, images).                                                                            |
| `POST /api/pentest/folder/preview` | Folder preview                      | **In scope** — optional separate tool or flag; same path rules as UI.                                                                           |
| `POST /api/pentest/folder`         | Folder scan (`pentestFolder`)       | **In scope** — max files / timeout / truncation flags **match Security panel** server limits.                                                   |
| `POST /api/pentest/remediate`      | Remediation / fix generation        | **Out of scope for v1 agent** — high blast radius; only revisit with a **separate, off-by-default** toggle and threat model if product demands. |

Reuse pattern: **`lib/pentest.js`** + thin **`routes/pentest.js`** → shared **`lib/pentest-service.js`** (name TBD) for snippet + folder paths only.

**Tests:** Fixture folder + escape attempts; **no remediate** in default tool list.

### 5.3 Phase 3 — Builder score (`builder_score`)

- **Input:** Same body shape as **`POST /api/score`** (`mode`: `prompting` | `skillz` | `agentic` + fields per `lib/builder-schemas.js`).
- **Reuse:** Single scoring function used by **`routes/score.js`** and builtin.
- **Tests (non-flaky):** Assert **HTTP 200**, **response JSON schema** (categories present, grades parseable), and **error shapes** on invalid payloads. **Do not** assert identical letter grades to a prior run unless Ollama is **mocked/stubbed** in that test.

### 5.4 Phase 4 — Experiment

**Decision:** **Defer** Experiment-from-Chat builtins for **v1**. Full lifecycle stays in **Experiment mode** + `routes/experiment.js` to avoid dual entry points and policy drift (scope, budgets, SSE vs tool rounds).

**Experiment-mode interaction with new builtins:** when `mode === "experiment"`, the new app-skill builtins (`review_run`, `pentest_scan`, `pentest_folder`, `builder_score`) are **not** added to `EXPERIMENT_ALLOWED_BUILTINS` in `lib/tool-call-handler.js`. Experiment runs continue to use the existing tight allowlist (`run_terminal_cmd`, `write_file`, `view_pdf_pages`, `validate_scan_project`, `validate_generate_command`, `score_plan`). This keeps experiment scope/budget semantics intact and avoids surprising agents-inside-experiments with different tools than the experiment author scoped for.

Revisit only with explicit product sign-off and a mini-spec for **idempotency**, **budget**, and **conversation linkage**.

### 5.5 Phase 5 — GSD bridge (optional)

- Follow **`docs/AGENT-APP-CAPABILITIES-ROADMAP.md`** Phase 3: read-only / allowlisted `gsd-bridge` ops, default off.

### Phase 0 — Foundation (1–2 PRs)

- Add **config schema** in `lib/config.js` + **Settings** UI: **master `agentAppSkillsEnabled`** default **`false`**, plus **per-family toggles** (review, pentest, builder_score; remediate absent; experiment absent in v1).
- Register tools in **`getBuiltinTools` / `executeBuiltinTool`** only when the relevant toggle is on.
- **Tests:** config round-trip; unknown tool rejected.

### Phase 0.5 — `chatStructured` abort fix (must land before Phase 1)

Standalone PR — shared infrastructure, not Phase 1 scope creep. Bundling it into the Phase 1 review PR makes that PR harder to review.

- **`lib/ollama-client.js#chatStructured`** — currently destructures `abortSignal` to `_abortSignal` (intentionally unused, line 238) and only attaches the internal timeout controller to fetch. Match `chatComplete`'s pattern (lines 179-181): if `abortSignal` is present, register `addEventListener("abort", () => controller.abort(), {once: true})` so user aborts propagate to the in-flight fetch.
- **`lib/review.js`** — thread `opts.abortSignal` (or `opts.signal`) into the `ollamaOptions` passed to `chatStructured` and `chatStream`.
- **Test (required, not optional):** mock `chatStructured` to delay 2s; issue abort at 100ms; assert the underlying fetch was aborted within 200ms (not 2s).

---

## 6. Security & operations

- **Rate limits:** Builtin invocations should count against the **same families** as HTTP where feasible (e.g. review already limited under `/api/review` in `server.js`); if in-process only, apply **equivalent limiter keys** in `lib/rate-limiters-config.js` to prevent agent-only burst abuse.
- **Logging:** `skill`, `durationMs`, `truncated`, `errorCode` — no secrets, no raw code in logs beyond length metadata. **Destination (pinned):** write to the existing `app.log` with a `[SKILL_AUDIT]` prefix line per invocation (one line in / one line out). Avoid creating a separate audit file — easier for one-person grep, matches `[TERMINAL]` audit pattern in the same file. The `terminal-audit.log` file remains terminal-specific; do not retrofit other skills into it.
- **Electron vs browser:** Same bindings as existing APIs.

---

## 7. Documentation & UX

- Update **`docs/ENVIRONMENT_VARIABLES.md`** / **`docs/CC-CONFIG.md`** for new keys.
- **`docs/AGENT-SKILLS.md`:** toggles, required tool args (`model`/`code`), abort behavior, “no remediate in v1,” Experiment UI pointer.

---

## 8. Verification checklist (acceptance)

- [ ] With master + family toggles **off**, tools are **absent** from prompt and return disabled if forced.
- [ ] With toggles **on**, each skill returns **deterministic error shapes** matching §5.0.2 envelope (no raw stack to model).
- [ ] All success returns match the §5.0.1 result envelope (`ok`, `type`, `data` | `summary`, `truncated`, `model`, `durationMs`).
- [ ] **Review** builtin uses the same **`reviewCode`** inputs as the service used by **`POST /api/review`** (after extraction).
- [ ] **Pentest** builtins only expose **snippet + folder (+ preview)**; **not** remediate by default.
- [ ] **Stop** in Chat aborts in-flight review/pentest Ollama **`fetch`** once `chatStructured` / streams honor `AbortSignal`. **Test required:** mocked `chatStructured` with a 2s delay; abort at 100ms; assert fetch aborted within 200ms.
- [ ] **Mode === "experiment"** does **not** include any of the new app-skill builtins in `EXPERIMENT_ALLOWED_BUILTINS` (verified by unit test against the registered tool list).
- [ ] `[SKILL_AUDIT]` line in `app.log` per invocation: `skill`, `model`, `durationMs`, `ok`, `code` (on error), `truncated`, no raw code.
- [ ] **Unit + integration** tests; **`npm run validate:fast`** and smoke server per `CLAUDE.md`.

---

## 9. Resolved product / design decisions

| Topic                    | Decision                                                                                                                                                    |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Defaults**             | Master **`agentAppSkillsEnabled: false`**; per-family toggles; builtins appear only when master **and** family are on.                                      |
| **Paths**                | **Same as HTTP today** — no expansion beyond `routes/review.js` / `routes/pentest.js` + `lib/file-browser` rules (`isWithinBasePath`, project/chat folder). |
| **Experiment from Chat** | **Deferred (v1)** — use Experiment mode UI.                                                                                                                 |
| **Tool naming**          | Prefer **`builtin.review_run`**, **`builtin.pentest_scan`**, etc., for log grep consistency with existing builtins.                                         |

---

## 10. Implementation notes matrix (quick reference)

| Skill (v1)       | Shared lib entry                       | Abort                                                                | Rate limit                |
| ---------------- | -------------------------------------- | -------------------------------------------------------------------- | ------------------------- |
| `review_run`     | Service → `reviewCode` / `reviewFiles` | Yes — after `chatStructured` fix                                     | Align with `/api/review`  |
| `pentest_scan`   | Service → `pentestCode`                | Via `chatStream` / pentest paths as today + extend structured if any | Align with `/api/pentest` |
| `pentest_folder` | Service → `pentestFolder`              | Same                                                                 | Align with folder route   |
| `builder_score`  | Service → score handler                | If score uses Ollama, thread signal same as route                    | Align with `/api/score`   |

---

## 11. References

- `docs/AGENT-APP-CAPABILITIES-ROADMAP.md`
- `lib/builtin-agent-tools.js`, `lib/tool-call-handler.js`, `lib/chat-post-handler.js`
- `lib/review.js`, `lib/ollama-client.js` (`chatStructured`, `chatStream`)
- `routes/review.js`, `routes/pentest.js`, `routes/score.js`, `server.js`
- `.planning/ROADMAP.md` (agent phases alignment)

---

## Document history

| Date       | Change                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-05-01 | Initial AGENTSKILL plan (Chat agent first-party capabilities).                                                                                                                                                                                                                                                                                                                                                                                 |
| 2026-05-01 | Resolved Critical/Major review items: Review contract, abort wiring, pentest enumeration, builder tests, service extraction, Experiment deferral, defaults/paths/naming. Status → implementation-ready.                                                                                                                                                                                                                                        |
| 2026-05-01 | Final plan-reviewer pass (post-v1.6.32): pinned **§5.0.1 result envelope** + **§5.0.2 error envelope**; added **Phase 0.5** (`chatStructured` abort fix as standalone PR before Phase 1); pinned **§6 audit log destination** (`app.log` `[SKILL_AUDIT]` prefix); pinned **§5.4 experiment-mode interaction** (new builtins NOT in `EXPERIMENT_ALLOWED_BUILTINS`); elevated abort-test from "improvement" to **§8 acceptance checklist** item. |
