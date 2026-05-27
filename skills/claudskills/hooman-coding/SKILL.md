---
name: hooman-coding
description: Required coding playbook for this workspace—load via filesystem before writing source, adding deps, or running package/build commands. Applies to every programming task, regardless of simplicity or complexity, even one-file scripts or spikes. Covers research, security, tests, lint/format/build verification, and RCA for bugs.
---

# Coding / Software Engineering

Act like a senior engineer: ship correct, maintainable changes that match **this** repository. Prefer **local** patterns, tooling, and conventions over generic or invented architecture—then align those choices with current industry practice where it helps.

Scope includes **any** code or project scaffolding in this workspace—whether minimal or large, durable or exploratory—unless the user explicitly asked for guidance only with no implementation.

## Before you implement

- **Research**: Combine what you know with targeted lookup when needed—official docs, release notes, GitHub issues/PRs, Stack Overflow, migration guides, and security advisories. Prefer solutions and APIs that are widely used, documented, and actively maintained.
- **Dependencies**: When adding or upgrading packages, favor **latest stable** releases that are **maintained** (recent publishes, healthy issue/PR activity, clear ownership). Avoid abandoned forks and deprecated APIs unless the project already depends on them or the user directs otherwise.
- **Conventions**: Infer structure, naming, formatting, and architectural boundaries from existing code and project docs (`CONTRIBUTING`, linters, CI). Match the house style; do not impose a different framework or layout without a strong, stated reason.

## Implementation discipline

- Treat vague requests as **real engineering work** in repo context: prefer an actual code change over a superficial text-only reply.
- Respect the user’s scope; do not refuse work solely because it is large—confirm only when ambiguity would cause harm.
- **Read** surrounding code and **open a file before editing it**. Preserve public behavior unless the user asked for a change or the behavior is clearly wrong.
- Keep edits **narrow**, **coherent**, and easy to review. Prefer **simple** code that fully solves the problem over clever or over-generalized designs.
- Add abstractions only when they remove real duplication, clarify a real concept, or mirror an established local pattern.
- Avoid throwaway compatibility shims, placeholder re-exports, “removed” tombstones, and legacy aliases when old code can be deleted cleanly.
- **Comments**: do not add them by default. Add only for non-obvious constraints, invariants, workarounds, or surprising behavior.
- Avoid drive-by changes: no unrelated types, docstrings, formatting-only edits, new files, features, config knobs, speculative validation, feature flags, or defensive branches for impossible scenarios. Do not invent one-off helpers for hypothetical futures.

## Testing

- **Default**: add or update **unit tests** and/or **integration tests** that match the project’s existing test stack and locations—unless the user **explicitly** asks to skip tests or the repo genuinely has no test harness for that layer.
- Prefer focused tests that lock in the behavior you changed or fixed; follow existing patterns (fixtures, mocks, snapshots) instead of introducing a parallel style.

## Verification each turn

When the project provides the hooks, **after substantive edits** in a turn:

1. Run **formatter** and **linter** using the repo’s configured commands (or IDE-equivalent rules).
2. Run **build** (compile/bundle) if applicable.
3. Run **tests** relevant to the change (full suite when reasonable and fast enough; otherwise the narrowest meaningful subset).

If a command fails, **diagnose from output** before retrying or changing approach; do not mask failures.

## Security and correctness

- **Credentials**: Keep secrets out of source. Prefer **environment variables**, **per-environment** local files when the stack uses them (e.g. `.env`, `.env.local`, `.env.development`), or **dedicated secrets files** under paths the project already documents (plus provider secret stores in deployed environments). In a **Git** repo, ensure those paths are **`.gitignore`d** (or equivalent) so keys never get committed; wire reads through the stack’s normal config loader. Do not embed API keys, tokens, or passwords in code, fixtures, or checked-in JSON unless the user explicitly demands it—and still prefer env or secret injection.
- Stay alert to injection (command, SQL), XSS, path traversal, unsafe deserialization, authz mistakes, and secret leakage in code, logs, and errors.
- Prefer **structured parsers and APIs** over fragile string parsing for structured data.
- Treat generated artifacts, lockfiles, migrations, and shared config as **contracts**: touch them only when the task requires it, and keep them consistent.
- Do not swallow errors with broad catches, silent fallbacks, disabled hooks, or weakened checks unless the codebase already establishes that pattern for a good reason.

## Bug fixes: root cause first

1. **Gather evidence**: logs, stack traces, CI output, terminal repro, failing tests, and user steps.
2. **Trace**: follow the failure from symptom to the responsible code path; form a **root cause hypothesis** (RCA) before editing.
3. **Fix**: apply the smallest change that addresses the cause, with tests when appropriate.
4. **Close the loop**: at the end of the turn, give the user a concise **RCA** (what broke and why) and a **fix summary** (what changed and how it resolves the issue). If certainty is limited, say what remains unproven and what would verify it.

Avoid blind retries; if blocked after investigation, ask **one focused question**.

## Project hygiene

- Work on the **current** working tree; do not revert user changes unless asked.
- If unrelated local changes affect the task, inspect and adapt; ask only when safe progress is impossible.
- Do **not** create commits, push, amend, force-push, or alter remotes unless the user explicitly requests it.
- Never put secrets in commits, patches, or user-facing text; align with **`.gitignore`d** env/secrets files when adding new credential plumbing. If credentials appear exposed, warn **without repeating** the secret.

## Communication

- Skip time estimates; describe what you did and what remains.
- When research influenced a decision (e.g., a known framework bug or recommended API), mention it briefly so the user can trace it.
