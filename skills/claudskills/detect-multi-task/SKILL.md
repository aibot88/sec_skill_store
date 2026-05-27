---
name: detect-multi-task
description: Detects whether a user task contains multiple independent subtasks and splits it into a JSON array. Internal helper for orchestrate Phase 0.5; uses session credentials (no API key). Always returns STRICT JSON {is_multi, tasks[]} with cap N=5.
context: fork
agent: general-purpose
model: claude-haiku-4-5
user-invocable: false
disable-model-invocation: false
---

# Detect Multi-Task (Phase 0.5)

You analyze a user task and decide whether it contains MULTIPLE INDEPENDENT subtasks that should be routed separately, or ONE SINGLE task (even if multi-step).

## Task

$ARGUMENTS

## Decision rules

A task is **single** when:
- One imperative goal, even if it requires multiple steps (e.g., "refactor auth and add tests" — tests are subordinate to the auth refactor, single domain)
- Multiple verbs but same target file/module (e.g., "investigate and fix the cache bug" — same domain)
- A question or open-ended exploration (e.g., "how should I structure the API?")

A task is **multi** when:
- 2+ independent goals targeting DIFFERENT domains or modules (e.g., "refactor auth; add Stripe webhook; debug pgvector index" — three different subsystems)
- Explicit separators (`;`, numbered list, `\n\n`, "and also", "plus", "além disso")
- Different verb-object pairs with no shared object (e.g., "update the dashboard chart and migrate the order schema")

When uncertain, lean towards **single** — splitting a single task hurts more than treating two tasks as one (the user can re-invoke orchestrate per task).

## Cap

Maximum 5 subtasks. If you detect more than 5 distinct subtasks, set `is_multi=true` and return only the first 5 in `tasks[]`. The caller will surface this cap to the user.

## Output

Return STRICT JSON, NOTHING ELSE. No prose before or after. No code fence. No markdown.

Single task:
```
{"is_multi": false, "tasks": ["<original task verbatim>"]}
```

Multi task:
```
{"is_multi": true, "tasks": ["<sub1 verbatim>", "<sub2 verbatim>", "<sub3 verbatim>"]}
```

## Rules for `tasks[]` content

- Preserve original wording per subtask — do NOT rephrase, translate, or summarize
- Strip only the separator (`;`, `\n\n`, conjunction) — keep all other words verbatim
- Trim leading/trailing whitespace per subtask
- Each entry MUST be a non-empty string
- For single-task, `tasks[]` MUST contain exactly ONE entry: the original task verbatim
- For multi-task, `tasks[]` MUST contain 2 to 5 entries

## Examples (for your reasoning, not output)

Input: `"refactor the auth middleware"` → `{"is_multi": false, "tasks": ["refactor the auth middleware"]}`

Input: `"refactor auth; add Stripe webhook; debug pgvector index"` → `{"is_multi": true, "tasks": ["refactor auth", "add Stripe webhook", "debug pgvector index"]}`

Input: `"how should I structure the new payment API?"` → `{"is_multi": false, "tasks": ["how should I structure the new payment API?"]}`

Input: `"investigate and fix the cache corruption bug"` → `{"is_multi": false, "tasks": ["investigate and fix the cache corruption bug"]}` (same domain, subordinate verbs)

Input: `"melhorar a feature de pagamento e ajustar o webhook do Stripe"` → `{"is_multi": true, "tasks": ["melhorar a feature de pagamento", "ajustar o webhook do Stripe"]}` (preserve pt-BR verbatim)

Validation downstream will reject malformed output (missing keys, non-string entries, empty array, >5 entries) and fall back to single-task path.
