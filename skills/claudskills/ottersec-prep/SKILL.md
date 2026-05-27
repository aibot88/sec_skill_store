---
name: ottersec-prep
description: Prep a Sui Move package for an OtterSec security audit. Use when the user mentions OtterSec or wants audit prep.
---

## Preamble (run first)

```bash
# Suiperpower telemetry. Routes through the CLI so projects.json + Convex stay in sync.
# Silent on failure so the skill never blocks. Opt out: SUIPERPOWER_TELEMETRY=off.
#
# AGENT NOTE: when this skill finishes, run the matching completion command:
#   suiperpower track ottersec-prep build completed
# Or use "failed" / "aborted" if it ended that way.
command -v suiperpower >/dev/null 2>&1 && suiperpower track ottersec-prep build started >/dev/null 2>&1 &
true
```

If `TEL_PROMPTED` is `no`, before doing real work, ask the user:

> Help suiperpower get better. We track which skills get used and how long they take. No code, no file paths, no PII. Change anytime in `~/.suiperpower/config.json`.
>
> A) Sure, anonymous
> B) No thanks

Write the answer to `~/.suiperpower/config.json` `telemetryTier` field and create `~/.suiperpower/.telemetry-prompted`. Then continue.

## What this skill does

Walks the OtterSec pre-audit checklist on the user's Move package, surfaces the gaps, and produces the engagement package the auditor expects (threat model, architecture diagram outline, test report, known-issues doc). The goal is for audit time to be spent on real findings, not on hygiene noise.

## When to use it

- About to engage OtterSec or another Sui Move auditor.
- Wanting to self-assess audit readiness.
- Preparing the audit-prep portion of a Sui Overflow submission targeting the OtterSec track.

## When NOT to use it

- Pre-MVP code where auditing is premature; use `review-move` for an in-house P0-P3 walk first.
- If the project does not have any Move code yet, use `build-with-move` first.
- For non-Move security questions (frontend XSS, key custody for sponsor wallets), use the relevant build skill.

If you activated this and the user actually wants something else, consult `skills/SKILL_ROUTER.md` and hand off.

## Inputs

- A Sui project with at least one Move package under `move/` or similar.
- Optional: `.suiperpower/build-context.md` and any prior `review-move` output.

If unclear, interview the user for:

- Which packages are in scope for the audit?
- Target deploy: which network, what value at risk?
- Are there parts the user explicitly does not want audited (test scaffolding, prototypes)?
- What is the timeline for the audit and the deploy?

## Outputs

- A filled-in pre-audit checklist (every P0 item answered, P1-P3 documented).
- A `THREAT_MODEL.md` in the project: who is trusted, what are the assets, what are the known risks.
- An architecture summary (which modules talk to which, where capabilities flow).
- A test-coverage report from `sui move test`.
- A `KNOWN_ISSUES.md` listing decisions to ship despite known concerns.
- Append to `.suiperpower/build-context.md`:

  ```markdown
  ## ottersec-prep session, <timestamp>
  - packages in scope: <list>
  - checklist completion: <P0 percent>, <P1 percent>
  - threat model doc: <path>
  - test count: <n>, coverage: <percent>
  - open issues: <list>
  ```

The skill never deletes files outside the integration source path without explicit user confirmation.

## Workflow

1. **Context gathering**
   - Read `.suiperpower/build-context.md` if present.
   - Confirm the package(s) in scope and the deploy target.

2. **P0 walk**
   - Step through every P0 item from `skills/data/guides/security-checklist.md`.
   - For each, mark pass / fail / not-applicable with a one-line note.
   - For fails, propose a fix and let the user decide whether to fix now or document as known.

3. **Capability inventory**
   - List every `*Cap` struct in the package(s).
   - For each, document: who creates it, who holds it, who can pass it to whom, whether it leaks via Display or public read.

4. **Visibility audit**
   - Confirm `public(package)` is the default; `public` is reserved for true cross-package APIs.
   - Flag any leftover `friend` declarations; recommend migration.
   - Confirm `#[test_only]` on test helpers.

5. **Init function audit**
   - Confirm one-time witness pattern intact.
   - Confirm init does not leak capabilities outside its intended distribution.
   - Confirm reinitialization is impossible (no shared init paths that can be re-entered).

6. **Test coverage**
   - Run `sui move test`, capture output.
   - Confirm every public entry function has at least one positive and one expected-failure test (where applicable).

7. **Build cleanliness**
   - Run `sui move build`. Confirm zero warnings.
   - Strip `assert!(false)`, commented-out checks, and `std::debug::print` from production paths.
   - Confirm error codes are named constants, not magic numbers.

8. **Dependency pin**
   - Confirm `Move.toml` uses pinned revs / tags. Reject `main` or floating versions in production deps.

9. **Threat model + known issues**
   - Help the user write `THREAT_MODEL.md` and `KNOWN_ISSUES.md` if absent.
   - Surface assumptions the auditor needs to know.

10. **Engagement package**
    - Compose the audit submission: repo URL, scope, threat model, architecture, test report, checklist, known issues.
    - Surface the OtterSec contact path (`https://osec.io/`).

11. **Writeback**
    - Append session details to `.suiperpower/build-context.md`.

## Quality gate (anti-slop)

Before reporting done, the skill asks itself the following and refuses to declare success if any answer is no:

- Is every P0 item from the security checklist explicitly marked pass / fail / N/A with a note?
- Has every public entry function been mapped to at least one happy-path test and one expected-failure test where applicable?
- Is `THREAT_MODEL.md` non-trivial (assets, trust assumptions, known risks named)?
- Is the capability inventory complete (every `*Cap` listed with holder strategy)?
- Is `Move.toml` pinned, no `main` in production deps?
- Is the engagement package something the user could send to OtterSec today without a follow-up "actually, I forgot..."?

If any answer is no, the skill reports the gap and works through it before claiming the package is audit-ready.

## References

On-demand references (load when relevant to the user's question):

- `references/pre-audit-walkthrough.md`: Item-by-item walk of the checklist with example pass/fail patterns.
- `references/finding-categories.md`: Common findings OtterSec produces, with mitigation patterns.
- `references/threat-model-template.md`: One-page threat-model template.

Knowledge docs (load when scope expands beyond what is in references):

- `skills/data/sui-knowledge/sponsor-docs/ottersec-checklist.md`: Full checklist source.
- `skills/data/guides/security-checklist.md`: P0-P3 reference.

## Use in your agent

- Claude Code: `claude "/suiper:ottersec-prep <your message>"`
- Codex: `codex "/ottersec-prep <your message>"`
- Cursor: paste a chat message that includes a phrase like "prepare for OtterSec audit", or load `~/.cursor/rules/ottersec-prep.mdc` and reference it.

If you activated this and the user actually wants something else, consult `skills/SKILL_ROUTER.md` and hand off.
