# Harmonia Agent — Agent Skill

Binary: `harmonia` | Install: `curl --proto '=https' --tlsv1.2 -sSf https://harmoniis.com/harmonia/install | sh` | Windows: `iwr https://harmoniis.com/harmonia/install.ps1 -UseB | iex`

Distributed evolutionary homoiconic self-improving agent. SBCL Common Lisp core + modular Rust tool ecosystem via CFFI.

## Install

macOS / Linux / FreeBSD:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://harmoniis.com/harmonia/install | sh
```

Windows (PowerShell):
```powershell
iwr https://harmoniis.com/harmonia/install.ps1 -UseB | iex
```

Binary-first install with source-build fallback. Optional overrides:
```bash
HARMONIA_INSTALL_MODE=source curl -sSf https://harmoniis.com/harmonia/install | sh   # force source build
HARMONIA_WITH_SOURCE=1 curl -sSf https://harmoniis.com/harmonia/install | sh          # binary + local source for self-rewrite
```

### Prerequisites

| Dependency | Why | Install |
|---|---|---|
| Rust 1.89+ | Builds tool crates | rustup.rs |
| SBCL | Agent runtime | `brew install sbcl` / `apt install sbcl` |
| Quicklisp | Lisp packages | Auto-installed by `harmonia setup` |

## Setup

```bash
harmonia setup    # interactive wizard
harmonia start    # start agent
harmonia upgrade  # update to latest release
harmonia uninstall
```

### Setup Wizard Steps

1. Creates system workspace at `~/.harmoniis/harmonia/`
2. Asks for user workspace directory (default: `~/workspace`)
3. Verifies SBCL + Quicklisp
4. Bootstraps vault keys from `harmoniis-wallet`
5. Select LLM providers and store API keys in encrypted vault (OpenRouter recommended)
6. Choose evolution profile: `binary-only` | `source-rewrite` | `distributed participant`
7. Git fork URL + optional GitHub PAT (stored in vault)
8. Optional S3 credentials for binary backups (stored in vault)
9. Select frontends to enable + collect frontend credentials (stored in vault)
10. Build and configure everything

**No model selection required.** The backend owns a built-in model pool with pricing. Model selection is automatic via harmonic scoring and evolves over time.

## Configuration

Workspace: `~/.harmoniis/harmonia/` (user data only)

```
~/.harmoniis/harmonia/
├── vault.db          # encrypted secrets (SQLite, AES-256-GCM)
├── config.db         # non-secret configuration (SQLite, config-store v2)
├── metrics.db        # model performance metrics (SQLite, auto-created)
├── config/
│   ├── workspace.sexp
│   └── gateway-frontends.sexp
├── genesis/          # evolution knowledge
├── state/            # runtime state, sockets, caches
└── frontends/        # frontend state and attachments
```

Installed application assets:
- macOS / Linux / FreeBSD: `~/.local/bin/harmonia`, `~/.local/lib/harmonia/`, `~/.local/share/harmonia/`
- Windows: `%LOCALAPPDATA%\Harmonia\bin\`, `%LOCALAPPDATA%\Harmonia\lib\`, `%LOCALAPPDATA%\Harmonia\share\`

Key config files (S-expressions):
- `harmony-policy.sexp` — security, evolution, harmonic routing
- `model-policy.sexp` — harmonic scoring weights for model evolution
- `baseband.sexp` — frontend registry + mesh transport
- `tools.sexp` — tool availability
- `swarm.sexp` — parallel agent orchestration

### Secrets

**Vault** (`vault.db`) — secrets only (API keys, tokens, passwords). AES-256-GCM encryption, component-scoped access policies. Each module reads only its own secrets.

**Config-store** (`config.db`) — all non-secret configuration (URLs, timeouts, paths, modes, feature flags). SQLite-backed with in-memory cache. Component-scoped read/write policies mirror vault's model. Fallback chain: cache → DB → legacy env alias → canonical `HARMONIA_{SCOPE}_{KEY}` → default.

No raw environment variables at runtime except bootstrap paths (`HARMONIA_STATE_ROOT`, `HARMONIA_LIB_DIR`). Setup writes everything directly to vault and config-store.

## Architecture

```
SBCL Common Lisp (Conductor + Memory + Self-Rewrite/Ouroboros)
         │ CFFI
Rust .so Libraries (Core + Tools + Backend + Frontends)
```

### Core Crates
phoenix (hot-reload/recovery), ouroboros (self-rewrite), vault (encrypted secrets), memory (persistent + compression), http, s3, git-ops, rust-forge (runtime compilation), cron-scheduler, push (webhooks), recovery, fs, parallel-agents, harmonic-matrix, config-store, tailnet, gateway.

### Backend — Model Pool Protocol
Each LLM provider is a separate backend crate implementing the standardised provider protocol (`harmonia-provider-protocol`):

| Backend | Crate | API Style |
|---|---|---|
| OpenRouter | `harmonia-openrouter` | OpenAI-compatible gateway (routes all) |
| OpenAI | `harmonia-openai` | OpenAI native |
| Anthropic | `harmonia-anthropic` | Anthropic Messages API |
| xAI (Grok) | `harmonia-xai` | OpenAI-compatible + reasoning |
| Google AI Studio | `harmonia-google-ai-studio` | Google Generative AI REST |
| Google Vertex AI | `harmonia-google-vertex` | Vertex AI REST + Bearer token |
| Amazon Bedrock | `harmonia-amazon-bedrock` | AWS CLI bedrock-runtime converse |
| Groq | `harmonia-groq` | OpenAI-compatible |
| Alibaba (Qwen) | `harmonia-alibaba` | OpenAI-compatible (DashScope) |

The backend exposes a standardised **model offerings protocol** via FFI:

| FFI Function | Returns | Purpose |
|---|---|---|
| `harmonia_openrouter_list_models()` | JSON array | All available models with pricing, quality, speed, tags |
| `harmonia_openrouter_select_model(task_hint)` | Model ID | Best model for task category via pool scoring |
| `harmonia_openrouter_complete(prompt, model)` | Text | Complete with explicit model (or empty for auto-select) |
| `harmonia_openrouter_complete_for_task(prompt, task_hint)` | Text | Complete with task-aware model selection |

**Initial model pool** (bootstrap tier — cheapest/fastest):

| Model | Tier | USD/1K in | USD/1K out | Tags |
|---|---|---|---|---|
| google/gemini-3.1-flash-lite-preview | micro | 0.00025 | 0.0015 | fast, memory-ops, casual |
| deepseek/deepseek-chat-v3.1:free | free | 0.0 | 0.0 | reasoning, casual |
| qwen/qwen3-coder:free | free | 0.0 | 0.0 | coding, execution |
| qwen/qwen3.5-flash-02-23 | lite | 0.0 | 0.0 | fast, coding, execution, reasoning |
| minimax/minimax-m2.5 | lite | 0.0003 | 0.0012 | balanced, memory-ops, casual |
| amazon/nova-micro-v1 | micro | 0.000035 | 0.00014 | fast, routing |

Higher tiers (orchestration, software-dev) available via `harmonia_openrouter_select_model("orchestration")`.

Task hints: `orchestration`, `execution`, `memory-ops`, `coding`, `reasoning`, `casual`, `software-dev`.

Performance is measured per-request (latency, success) and written to the SQLite `metrics.db` database (resolved via config-store `global/state-root`). Four tables:
- `models` — full model catalogue (290+ models synced from OpenRouter API + hardcoded), with per-token pricing, context length, modality
- `llm_perf` — every LLM backend call (backend, model, latency_ms, success, pricing)
- `parallel_tasks` — parallel-agent task completions (cost, verification)
- `tmux_events` — tmux CLI agent lifecycle events (spawn, input, approve, deny, kill) with `cost_usd` and `duration_ms` tracking

On init, the OpenRouter backend syncs the full model catalogue from `https://openrouter.ai/api/v1/models` (background thread). All hardcoded backend offerings are also registered. The `models` table is the agent's single source of truth for what models exist and what they cost.

### Metrics Query FFI

The orchestrator queries the metrics database via FFI. The agent can run **arbitrary SELECT SQL** for maximum flexibility:

| FFI Function | Returns | Purpose |
|---|---|---|
| `harmonia_metrics_query_json(sql)` | JSON array | Run any SELECT query, get results as JSON |
| `harmonia_metrics_query_sexp(sql)` | S-expression | Run any SELECT query, get results as s-expression plists |
| `harmonia_metrics_sync_models(api_key)` | Count or -1 | Sync model catalogue from OpenRouter API |
| `harmonia_metrics_model_stats(model)` | S-expression | Per-model stats: count, success-rate, avg-latency, pricing |
| `harmonia_metrics_best_models(backend, limit)` | S-expression list | Top-performing models ranked by success rate + speed |
| `harmonia_metrics_llm_report()` | S-expression | Full LLM backend performance report |
| `harmonia_metrics_tmux_report()` | S-expression | Tmux agent event summary |
| `harmonia_metrics_telemetry_digest()` | S-expression | Combined digest for harmonic orchestration decisions |
| `harmonia_metrics_bridge_routes(since_ts)` | S-expression | Recent LLM perf as route entries for harmonic matrix |

Example SQL queries the agent can run:
```sql
-- Cheapest models with >8K context
SELECT id, name, usd_per_tok_in, usd_per_tok_out, context_length
FROM models WHERE context_length > 8000 ORDER BY usd_per_tok_in ASC LIMIT 20

-- Best performing models in last hour
SELECT model, COUNT(*) n, AVG(CAST(success AS REAL)) sr, AVG(latency_ms) lat
FROM llm_perf WHERE ts > unixepoch()-3600 GROUP BY model ORDER BY sr DESC, lat ASC

-- Cost analysis by provider
SELECT provider, COUNT(*) models, MIN(usd_per_tok_in) cheapest_in, MIN(usd_per_tok_out) cheapest_out
FROM models WHERE usd_per_tok_in > 0 GROUP BY provider ORDER BY cheapest_in ASC
```

### Tools
browser (Chrome CDP with stealth anti-detection), search-exa (neural), search-brave, hfetch (secure HTTP), zoom (meeting automation).

### Voice Backends
voice-router dispatches to: whisper (STT via Groq/OpenAI), elevenlabs (TTS).

### Frontends (hot-pluggable via dlopen)
TUI (always on), MQTT, Telegram, Slack, Discord, Signal (signal-cli bridge), WhatsApp, iMessage (BlueBubbles), Mattermost, Nostr, Email (IMAP/SMTP), Tailscale mesh.

## Security

Two-layer model:
1. **Security Kernel** (deterministic, non-bypassable) — typed signal dispatch, policy gate for privileged ops, taint propagation, safe parsers.
2. **Adaptive Security Shell** — dissonance scoring (18 injection patterns), harmonic routing, component-scoped vault policies.

Policy gate blocks privileged ops if signal has external taint or lacks `:owner`/`:authenticated` label.

## Evolution Profiles

- `binary-only` — use released binaries, no self-modification
- `source-rewrite` — agent can edit and recompile its own source
- `distributed participant` — participate in cross-instance evolution

## LLM Model Routing

14 model profiles from micro (nova-micro) to frontier (claude-opus-4.6, gpt-5). No "default model" — model selection is **task-aware and score-based**:
- Different models for orchestration, coding, memory-ops, casual
- Round-robin through pool initially to gather performance data
- Harmonic-matrix evolves selection based on measured latency, success rate, and cost
- Scoring weights: completion 30%, correctness 20%, speed 12%, price 12%, token-efficiency 10%, orchestration-efficiency 10%, experience 6%

## Platforms

macOS (Apple Silicon / Intel), Linux (x86_64 / aarch64), FreeBSD, Windows.

## License

Harmonia Community License 1.0 (HCL-1.0). Free for all use — individuals, freelancers, companies. Only restriction: hosting Harmonia as a managed service for third parties requires a commercial license. Contact license@harmoniis.com.

## Build from Source

```bash
git clone https://github.com/harmoniis/harmonia.git && cd harmonia
bazel build //...   # or: cargo build --release
bazel test //...    # or: cargo test --workspace
```

Source: https://github.com/harmoniis/harmonia
Docs: https://harmoniis.com/docs/harmonia/overview
Marketplace: https://harmoniis.com/skill.md
